"""
TruLens Evaluation Framework Example

TruLens provides evaluation and tracking for LLM applications with a focus on
transparency and observability. Great for RAG systems and LLM chains.

Installation:
pip install trulens-eval

Documentation: https://www.trulens.org/
"""

import os
from trulens_eval import Tru, Feedback, TruChain, Select
from trulens_eval.app import App
from trulens_eval.feedback.provider.openai import OpenAI as TruOpenAI
import numpy as np


def setup_trulens():
    """Initialize TruLens."""
    # Initialize TruLens
    tru = Tru()
    tru.reset_database()  # Reset for demo purposes
    return tru


def create_feedback_functions():
    """
    Create feedback functions for evaluation.
    These are the metrics TruLens will track.
    """
    print("\n=== Creating Feedback Functions ===")

    # Initialize provider (OpenAI for evaluations)
    provider = TruOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Define feedback functions
    feedbacks = {
        "answer_relevance": Feedback(
            provider.relevance,
            name="Answer Relevance"
        ).on_input_output(),

        "context_relevance": Feedback(
            provider.qs_relevance,
            name="Context Relevance"
        ).on_input().on(Select.RecordCalls.retrieve.rets[:]),

        "groundedness": Feedback(
            provider.groundedness_measure_with_cot_reasons,
            name="Groundedness"
        ).on(Select.RecordCalls.retrieve.rets[:]).on_output(),

        "toxicity": Feedback(
            provider.moderation_not_toxic,
            name="Toxicity Check"
        ).on_output()
    }

    print("Created feedback functions:")
    for name in feedbacks.keys():
        print(f"  • {name}")

    return feedbacks


def evaluate_simple_qa():
    """
    Evaluate a simple Q&A function.
    Demonstrates basic TruLens evaluation.
    """
    print("\n=== Simple Q&A Evaluation ===")

    tru = setup_trulens()
    provider = TruOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Simple Q&A function
    def qa_function(question: str) -> str:
        """Simple Q&A function to evaluate."""
        answers = {
            "what is machine learning?": "Machine learning is a subset of AI that learns from data.",
            "what is python?": "Python is a high-level programming language.",
            "what is ai?": "AI is artificial intelligence."
        }
        return answers.get(question.lower(), "I don't know.")

    # Create feedback function
    f_answer_relevance = Feedback(
        provider.relevance,
        name="Answer Relevance"
    ).on_input_output()

    # Wrap function with TruLens
    from trulens_eval.tru_basic_app import TruBasicApp

    tru_qa = TruBasicApp(
        qa_function,
        app_id="Simple_QA",
        feedbacks=[f_answer_relevance]
    )

    # Run evaluations
    questions = [
        "What is machine learning?",
        "What is Python?",
        "What is AI?"
    ]

    print("\nRunning evaluations...")
    with tru_qa as recording:
        for question in questions:
            answer = qa_function(question)
            print(f"Q: {question}")
            print(f"A: {answer}")

    print("\n✓ Evaluations tracked in TruLens")
    return tru_qa


def evaluate_rag_system():
    """
    Evaluate a RAG (Retrieval-Augmented Generation) system.
    Tracks retrieval quality and generation quality separately.
    """
    print("\n=== RAG System Evaluation ===")

    tru = setup_trulens()
    provider = TruOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Simple RAG system
    class SimpleRAG:
        def __init__(self):
            self.knowledge_base = {
                "ml": "Machine learning is a subset of AI that enables systems to learn from data without explicit programming.",
                "python": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
                "ai": "Artificial Intelligence is the simulation of human intelligence by machines."
            }

        def retrieve(self, query: str) -> list:
            """Retrieve relevant documents."""
            query_lower = query.lower()
            relevant_docs = []

            if "machine learning" in query_lower or "ml" in query_lower:
                relevant_docs.append(self.knowledge_base["ml"])
            if "python" in query_lower:
                relevant_docs.append(self.knowledge_base["python"])
            if "ai" in query_lower or "artificial intelligence" in query_lower:
                relevant_docs.append(self.knowledge_base["ai"])

            return relevant_docs if relevant_docs else ["No relevant information found."]

        def generate(self, query: str, contexts: list) -> str:
            """Generate answer from contexts."""
            if not contexts or contexts[0] == "No relevant information found.":
                return "I don't have information about that."

            # Simple generation - just return first context
            return contexts[0]

        def query(self, question: str) -> str:
            """Full RAG pipeline."""
            contexts = self.retrieve(question)
            answer = self.generate(question, contexts)
            return answer

    # Create RAG instance
    rag = SimpleRAG()

    # Create comprehensive feedback functions for RAG
    f_answer_relevance = Feedback(
        provider.relevance,
        name="Answer Relevance"
    ).on_input().on_output()

    f_context_relevance = Feedback(
        provider.qs_relevance,
        name="Context Relevance"
    ).on_input().on(Select.RecordCalls.retrieve.rets[:])

    f_groundedness = Feedback(
        provider.groundedness_measure_with_cot_reasons,
        name="Groundedness"
    ).on(Select.RecordCalls.retrieve.rets[:]).on_output()

    # Wrap RAG with TruLens
    from trulens_eval.tru_basic_app import TruBasicApp

    tru_rag = TruBasicApp(
        rag.query,
        app_id="Simple_RAG",
        feedbacks=[f_answer_relevance, f_groundedness]
    )

    # Run RAG evaluations
    questions = [
        "What is machine learning?",
        "Explain Python programming",
        "Tell me about artificial intelligence"
    ]

    print("\nRunning RAG evaluations...")
    with tru_rag as recording:
        for question in questions:
            answer = rag.query(question)
            print(f"Q: {question}")
            print(f"A: {answer[:100]}...")

    print("\n✓ RAG evaluations tracked")
    return tru_rag


def evaluate_chain_of_thought():
    """
    Evaluate chain-of-thought reasoning.
    Tracks intermediate reasoning steps.
    """
    print("\n=== Chain-of-Thought Evaluation ===")

    tru = setup_trulens()
    provider = TruOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Chain-of-thought function
    class ChainOfThought:
        def step1_analyze(self, question: str) -> str:
            """Analyze the question."""
            return f"Analysis: The question asks about {question}"

        def step2_retrieve(self, analysis: str) -> str:
            """Retrieve information."""
            return "Retrieved information: [relevant context]"

        def step3_synthesize(self, question: str, info: str) -> str:
            """Synthesize final answer."""
            return f"Based on the analysis, the answer is: [synthesized response]"

        def reason(self, question: str) -> str:
            """Full reasoning chain."""
            analysis = self.step1_analyze(question)
            info = self.step2_retrieve(analysis)
            answer = self.step3_synthesize(question, info)
            return answer

    cot = ChainOfThought()

    # Create feedback for each step
    f_relevance = Feedback(
        provider.relevance,
        name="Overall Relevance"
    ).on_input().on_output()

    # Wrap with TruLens
    from trulens_eval.tru_basic_app import TruBasicApp

    tru_cot = TruBasicApp(
        cot.reason,
        app_id="Chain_of_Thought",
        feedbacks=[f_relevance]
    )

    # Run evaluation
    print("\nRunning chain-of-thought evaluation...")
    with tru_cot as recording:
        result = cot.reason("How does photosynthesis work?")
        print(f"Result: {result}")

    print("\n✓ Chain-of-thought tracked")
    return tru_cot


def custom_feedback_function():
    """
    Create custom feedback functions.
    Demonstrates extensibility of TruLens.
    """
    print("\n=== Custom Feedback Function ===")

    def word_count_feedback(text: str) -> float:
        """Custom feedback: Check if response has appropriate length."""
        word_count = len(text.split())
        if 10 <= word_count <= 100:
            return 1.0
        elif word_count < 10:
            return 0.5
        else:
            return 0.7

    def contains_keywords_feedback(question: str, answer: str) -> float:
        """Custom feedback: Check if answer contains key terms from question."""
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        overlap = len(question_words & answer_words)
        return min(overlap / max(len(question_words), 1), 1.0)

    # Create Feedback objects
    f_word_count = Feedback(
        word_count_feedback,
        name="Word Count Check"
    ).on_output()

    f_keywords = Feedback(
        contains_keywords_feedback,
        name="Keyword Presence"
    ).on_input().on_output()

    print("\n✓ Custom feedback functions created")
    print("  • Word Count Check")
    print("  • Keyword Presence")

    return [f_word_count, f_keywords]


def aggregate_metrics_example():
    """
    Example of aggregating metrics across multiple runs.
    Useful for understanding overall system performance.
    """
    print("\n=== Aggregate Metrics Example ===")

    tru = setup_trulens()

    # Simulate multiple evaluation runs
    print("\nSimulating evaluation runs...")

    # In practice, you would:
    # 1. Run multiple evaluations with tru_app
    # 2. Use tru.get_leaderboard() to see aggregate metrics
    # 3. Use tru.get_records_and_feedback() for detailed analysis

    print("""
    TruLens Aggregation Features:

    # Get leaderboard of all apps
    leaderboard = tru.get_leaderboard()

    # Get detailed records
    records, feedback = tru.get_records_and_feedback(app_ids=["app_id"])

    # Calculate statistics
    mean_score = feedback["relevance"].mean()
    std_score = feedback["relevance"].std()

    # View in dashboard
    tru.run_dashboard()  # Opens web UI at localhost:8501
    """)

    print("\n✓ Use tru.run_dashboard() to view metrics visually")


def comparative_evaluation():
    """
    Compare multiple systems or model versions.
    Useful for A/B testing and model selection.
    """
    print("\n=== Comparative Evaluation ===")

    tru = setup_trulens()
    provider = TruOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # System A: Simple responses
    def system_a(question: str) -> str:
        return "Simple answer."

    # System B: Detailed responses
    def system_b(question: str) -> str:
        return "Detailed answer with more context and explanation."

    # Create feedback
    f_relevance = Feedback(
        provider.relevance,
        name="Relevance"
    ).on_input_output()

    # Wrap both systems
    from trulens_eval.tru_basic_app import TruBasicApp

    tru_system_a = TruBasicApp(
        system_a,
        app_id="System_A",
        feedbacks=[f_relevance]
    )

    tru_system_b = TruBasicApp(
        system_b,
        app_id="System_B",
        feedbacks=[f_relevance]
    )

    # Evaluate both
    test_questions = [
        "What is AI?",
        "Explain machine learning"
    ]

    print("\nEvaluating System A...")
    with tru_system_a as recording:
        for q in test_questions:
            system_a(q)

    print("Evaluating System B...")
    with tru_system_b as recording:
        for q in test_questions:
            system_b(q)

    print("\n✓ Both systems evaluated")
    print("✓ Compare in dashboard: tru.run_dashboard()")

    return tru_system_a, tru_system_b


def main():
    """Run all TruLens examples."""
    print("=" * 60)
    print("TruLens Evaluation Framework Examples")
    print("=" * 60)

    try:
        # Setup
        create_feedback_functions()

        # Basic evaluations
        evaluate_simple_qa()
        evaluate_rag_system()
        evaluate_chain_of_thought()

        # Advanced features
        custom_feedback_function()
        aggregate_metrics_example()
        comparative_evaluation()

        print("\n" + "=" * 60)
        print("All TruLens evaluations completed successfully!")
        print("=" * 60)

        print("\n📊 TruLens Features:")
        print("  • Answer Quality: Relevance, groundedness")
        print("  • RAG Evaluation: Context relevance, retrieval quality")
        print("  • Observability: Track all intermediate steps")
        print("  • Custom Metrics: Build your own feedback functions")
        print("  • Dashboard: Visual analytics (tru.run_dashboard())")
        print("  • Comparison: A/B testing and leaderboards")
        print("  • Guardrails: Real-time monitoring and alerts")

        print("\n💡 View results:")
        print("  from trulens_eval import Tru")
        print("  tru = Tru()")
        print("  tru.run_dashboard()  # Opens at localhost:8501")

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Make sure you have set OPENAI_API_KEY environment variable")
        print("Install requirements: pip install trulens-eval")


if __name__ == "__main__":
    main()
