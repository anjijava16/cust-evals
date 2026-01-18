"""
Langfuse Evaluation and Observability Example

Langfuse provides LLM observability, tracing, and evaluation with a focus on
production monitoring, prompt management, and user feedback collection.

Installation:
pip install langfuse

Documentation: https://langfuse.com/docs
"""

import os
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from typing import List, Dict, Any
import time


def setup_langfuse():
    """Initialize Langfuse client."""
    langfuse = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    )
    print("✓ Langfuse client initialized")
    return langfuse


def basic_trace_example():
    """
    Basic tracing with Langfuse.
    Tracks LLM calls and application flow.
    """
    print("\n=== Basic Trace Example ===")

    langfuse = setup_langfuse()

    # Create a trace
    trace = langfuse.trace(
        name="qa_chain",
        user_id="user_123",
        metadata={"environment": "production"}
    )

    # Add generation (LLM call)
    generation = trace.generation(
        name="answer_question",
        model="gpt-3.5-turbo",
        model_parameters={"temperature": 0.7, "max_tokens": 150},
        input="What is machine learning?",
        output="Machine learning is a subset of AI that learns from data.",
        usage={"prompt_tokens": 10, "completion_tokens": 15, "total_tokens": 25}
    )

    # Add score/evaluation
    generation.score(
        name="quality",
        value=0.9,
        comment="High quality response"
    )

    print("✓ Trace created and logged to Langfuse")
    print(f"  Trace ID: {trace.id}")
    print(f"  View at: https://cloud.langfuse.com/traces/{trace.id}")

    return trace


@observe()
def qa_with_retrieval(question: str) -> str:
    """
    Q&A function with automatic tracing using decorator.
    Langfuse automatically tracks this function.
    """
    # Simulate retrieval
    langfuse_context.update_current_observation(
        name="retrieval",
        input=question
    )

    retrieved_docs = [
        "Machine learning uses algorithms to learn from data.",
        "ML is a subset of artificial intelligence."
    ]

    langfuse_context.update_current_observation(
        output={"documents": retrieved_docs}
    )

    # Simulate generation
    langfuse_context.update_current_observation(
        name="generation",
        model="gpt-4",
        input={"question": question, "context": retrieved_docs}
    )

    answer = "Machine learning is a subset of AI that uses algorithms to learn from data."

    langfuse_context.update_current_observation(
        output=answer
    )

    return answer


def decorator_tracing_example():
    """
    Automatic tracing using decorators.
    Simplifies instrumentation.
    """
    print("\n=== Decorator Tracing Example ===")

    question = "What is machine learning?"
    answer = qa_with_retrieval(question)

    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print("✓ Automatically traced with @observe decorator")

    return answer


def evaluate_with_scores():
    """
    Add evaluation scores to traces.
    Track quality metrics.
    """
    print("\n=== Evaluation with Scores ===")

    langfuse = setup_langfuse()

    # Create trace
    trace = langfuse.trace(name="evaluated_qa")

    # Simulate generation
    generation = trace.generation(
        name="answer",
        model="gpt-4",
        input="Explain quantum computing",
        output="Quantum computing uses quantum bits to perform complex calculations."
    )

    # Add multiple scores
    scores = [
        {"name": "accuracy", "value": 0.85, "comment": "Factually correct"},
        {"name": "relevance", "value": 0.9, "comment": "Directly addresses question"},
        {"name": "completeness", "value": 0.7, "comment": "Could be more detailed"}
    ]

    for score in scores:
        generation.score(**score)

    print("✓ Multiple evaluation scores added:")
    for score in scores:
        print(f"  • {score['name']}: {score['value']} - {score['comment']}")

    return trace


def dataset_evaluation():
    """
    Evaluate using datasets in Langfuse.
    Systematic evaluation with test sets.
    """
    print("\n=== Dataset Evaluation ===")

    langfuse = setup_langfuse()

    # Create dataset
    dataset_name = "qa_test_set"

    print(f"Creating dataset: {dataset_name}")

    # Add examples to dataset (in practice, done via UI or API)
    examples = [
        {
            "input": "What is AI?",
            "expected_output": "Artificial Intelligence",
            "metadata": {"category": "definition"}
        },
        {
            "input": "What is ML?",
            "expected_output": "Machine Learning",
            "metadata": {"category": "definition"}
        }
    ]

    print(f"✓ Dataset prepared with {len(examples)} examples")
    print("  Run evaluations via Langfuse UI or API")

    # In production, you would:
    # 1. Create dataset items via API
    # 2. Run your model on each item
    # 3. Link traces to dataset runs
    # 4. Add scores to compare performance

    return examples


def user_feedback_collection():
    """
    Collect and track user feedback.
    Important for production systems.
    """
    print("\n=== User Feedback Collection ===")

    langfuse = setup_langfuse()

    # Create trace
    trace = langfuse.trace(
        name="user_interaction",
        user_id="user_456"
    )

    generation = trace.generation(
        name="assistant_response",
        model="gpt-4",
        input="How do I reset my password?",
        output="To reset your password, click the 'Forgot Password' link on the login page."
    )

    # Simulate user providing feedback
    # User clicks thumbs up/down
    user_rating = 1.0  # 1.0 for positive, 0.0 for negative

    generation.score(
        name="user_feedback",
        value=user_rating,
        comment="User found response helpful",
        data_type="NUMERIC"
    )

    # Add additional feedback details
    trace.update(
        metadata={
            "user_feedback_text": "Very helpful, solved my issue!",
            "feedback_timestamp": time.time()
        }
    )

    print("✓ User feedback collected:")
    print(f"  Rating: {'Positive' if user_rating > 0.5 else 'Negative'}")
    print(f"  Feedback: Very helpful, solved my issue!")

    return trace


def prompt_management_example():
    """
    Manage prompts in Langfuse.
    Version control for prompts.
    """
    print("\n=== Prompt Management ===")

    langfuse = setup_langfuse()

    # In Langfuse, you can:
    # 1. Create named prompts in the UI
    # 2. Version them
    # 3. Fetch and use them in code

    # Simulated prompt fetching
    print("Prompt Management Features:")
    print("  • Create prompts in Langfuse UI")
    print("  • Version control for prompts")
    print("  • A/B test different prompt versions")
    print("  • Track performance by prompt version")
    print("  • Roll back to previous versions")

    # Example usage (requires prompt created in UI):
    # prompt = langfuse.get_prompt("qa_system_prompt", version=2)
    # response = call_llm(prompt.compile(question="What is AI?"))

    print("\n✓ Centralized prompt management with version control")


def session_tracking():
    """
    Track multi-turn conversations.
    Group related interactions.
    """
    print("\n=== Session Tracking ===")

    langfuse = setup_langfuse()

    session_id = "session_789"

    # Turn 1
    trace1 = langfuse.trace(
        name="turn_1",
        session_id=session_id,
        user_id="user_123"
    )
    trace1.generation(
        name="response_1",
        input="Hello",
        output="Hi! How can I help you today?"
    )

    # Turn 2
    trace2 = langfuse.trace(
        name="turn_2",
        session_id=session_id,
        user_id="user_123"
    )
    trace2.generation(
        name="response_2",
        input="What is machine learning?",
        output="Machine learning is a subset of AI."
    )

    print(f"✓ Multi-turn conversation tracked:")
    print(f"  Session ID: {session_id}")
    print(f"  Turns: 2")
    print(f"  View full conversation in Langfuse UI")

    return session_id


def cost_tracking():
    """
    Track LLM costs.
    Monitor expenses by model and user.
    """
    print("\n=== Cost Tracking ===")

    langfuse = setup_langfuse()

    trace = langfuse.trace(name="cost_tracking_example")

    # Track generation with usage
    generation = trace.generation(
        name="gpt4_call",
        model="gpt-4",
        input="Long prompt...",
        output="Detailed response...",
        usage={
            "prompt_tokens": 1000,
            "completion_tokens": 500,
            "total_tokens": 1500
        }
    )

    # Langfuse automatically calculates costs based on model pricing
    estimated_cost = 0.03 * (1000 / 1000) + 0.06 * (500 / 1000)  # GPT-4 pricing

    print("✓ Cost tracking enabled:")
    print(f"  Model: gpt-4")
    print(f"  Tokens: 1500 (1000 prompt + 500 completion)")
    print(f"  Estimated Cost: ${estimated_cost:.4f}")
    print("  View aggregate costs in Langfuse dashboard")

    return trace


def llm_as_judge_evaluation():
    """
    Use LLM as judge with Langfuse.
    Automated quality evaluation.
    """
    print("\n=== LLM as Judge Evaluation ===")

    langfuse = setup_langfuse()

    # Original generation
    trace = langfuse.trace(name="llm_judge_eval")

    generation = trace.generation(
        name="answer",
        input="What is the capital of France?",
        output="The capital of France is Paris."
    )

    # Use LLM to evaluate
    # In practice, call GPT-4 to evaluate
    judge_prompt = """
    Evaluate this Q&A on a scale of 0-1 for accuracy:
    Question: What is the capital of France?
    Answer: The capital of France is Paris.
    """

    # Simulated judge score
    judge_score = 1.0

    generation.score(
        name="llm_judge_accuracy",
        value=judge_score,
        comment="Evaluated by GPT-4 judge"
    )

    print("✓ LLM judge evaluation:")
    print(f"  Score: {judge_score}")
    print(f"  Judge: GPT-4")
    print(f"  Metric: Accuracy")

    return trace


def experiment_comparison():
    """
    Compare different experiments/configurations.
    A/B testing and variant comparison.
    """
    print("\n=== Experiment Comparison ===")

    langfuse = setup_langfuse()

    experiments = ["baseline", "improved_prompt", "different_model"]

    for exp_name in experiments:
        trace = langfuse.trace(
            name=f"qa_{exp_name}",
            tags=[exp_name],
            metadata={"experiment": exp_name}
        )

        # Simulate different performance
        scores = {
            "baseline": 0.7,
            "improved_prompt": 0.85,
            "different_model": 0.8
        }

        generation = trace.generation(
            name="answer",
            input="Test question",
            output=f"Answer from {exp_name}"
        )

        generation.score(
            name="quality",
            value=scores[exp_name]
        )

    print("✓ Experiments created:")
    for exp_name, score in scores.items():
        print(f"  • {exp_name}: {score}")

    print("\n  Compare in Langfuse dashboard using tags/metadata")

    return experiments


def production_monitoring():
    """
    Production monitoring setup.
    Track real-time performance.
    """
    print("\n=== Production Monitoring ===")

    print("Production Monitoring Features:")
    print("  • Real-time trace ingestion")
    print("  • Latency monitoring")
    print("  • Error rate tracking")
    print("  • Cost analytics")
    print("  • User feedback aggregation")
    print("  • Model performance trends")
    print("  • Alerting (via integrations)")

    print("\n✓ Langfuse provides comprehensive production observability")


def main():
    """Run all Langfuse examples."""
    print("=" * 60)
    print("Langfuse Evaluation and Observability Examples")
    print("=" * 60)

    try:
        # Basic features
        basic_trace_example()
        decorator_tracing_example()
        evaluate_with_scores()

        # Datasets and evaluation
        dataset_evaluation()
        llm_as_judge_evaluation()

        # Production features
        user_feedback_collection()
        session_tracking()
        cost_tracking()
        prompt_management_example()

        # Advanced
        experiment_comparison()
        production_monitoring()

        print("\n" + "=" * 60)
        print("All Langfuse examples completed successfully!")
        print("=" * 60)

        print("\n📊 Langfuse Key Features:")
        print("  • Tracing: Full observability of LLM calls")
        print("  • Evaluation: Score and evaluate outputs")
        print("  • Datasets: Manage test sets")
        print("  • User Feedback: Collect production feedback")
        print("  • Prompt Management: Version control prompts")
        print("  • Cost Tracking: Monitor LLM expenses")
        print("  • Sessions: Track multi-turn conversations")
        print("  • Dashboard: Visual analytics")
        print("  • Production Ready: Built for scale")

        print("\n💡 Langfuse Use Cases:")
        print("  • Production LLM monitoring")
        print("  • Quality tracking and improvement")
        print("  • Cost optimization")
        print("  • Prompt engineering and testing")
        print("  • User feedback collection")
        print("  • Debugging and troubleshooting")
        print("  • Experiment comparison")

        print("\n🚀 Getting Started:")
        print("  1. Sign up: https://cloud.langfuse.com")
        print("  2. Get API keys from dashboard")
        print("  3. Install: pip install langfuse")
        print("  4. Add tracing to your code")
        print("  5. View traces in dashboard")

    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Setup required:")
        print("  1. Sign up at https://cloud.langfuse.com")
        print("  2. Get API keys")
        print("  3. Set environment variables:")
        print("     export LANGFUSE_PUBLIC_KEY='your_public_key'")
        print("     export LANGFUSE_SECRET_KEY='your_secret_key'")
        print("  4. pip install langfuse")


if __name__ == "__main__":
    main()
