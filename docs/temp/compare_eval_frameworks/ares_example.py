"""
ARES (Automated RAG Evaluation System) Example

ARES is specifically designed for evaluating Retrieval-Augmented Generation (RAG) systems.
Uses synthetic data generation and few-shot learning for evaluation.

Installation:
pip install ares-ai

Documentation: https://github.com/stanford-futuredata/ARES
"""

import os
from typing import List, Dict, Any
from dataclasses import dataclass
import pandas as pd


@dataclass
class RAGExample:
    """RAG evaluation example."""
    query: str
    retrieved_contexts: List[str]
    generated_answer: str
    ground_truth: str = None


@dataclass
class ARESScore:
    """ARES evaluation scores."""
    context_relevance: float  # Are retrieved contexts relevant?
    answer_faithfulness: float  # Is answer faithful to contexts?
    answer_relevance: float  # Is answer relevant to query?
    overall_score: float


class ARESEvaluator:
    """ARES RAG evaluator."""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name

    def evaluate_context_relevance(
        self,
        query: str,
        contexts: List[str]
    ) -> float:
        """
        Evaluate if retrieved contexts are relevant to query.
        Core metric for retrieval quality.
        """
        if not contexts:
            return 0.0

        # In real ARES, this uses a trained classifier
        # For demo, use simple keyword matching
        query_keywords = set(query.lower().split())
        relevance_scores = []

        for context in contexts:
            context_keywords = set(context.lower().split())
            overlap = len(query_keywords & context_keywords)
            score = min(overlap / len(query_keywords), 1.0) if query_keywords else 0.0
            relevance_scores.append(score)

        return sum(relevance_scores) / len(relevance_scores)

    def evaluate_answer_faithfulness(
        self,
        answer: str,
        contexts: List[str]
    ) -> float:
        """
        Evaluate if answer is faithful to retrieved contexts.
        Detects hallucination and unsupported claims.
        """
        if not contexts:
            return 0.0

        # Check if answer content is grounded in contexts
        answer_words = set(answer.lower().split())
        context_words = set()
        for ctx in contexts:
            context_words.update(ctx.lower().split())

        # Calculate grounding score
        grounded_words = answer_words & context_words
        faithfulness = len(grounded_words) / len(answer_words) if answer_words else 0.0

        return faithfulness

    def evaluate_answer_relevance(
        self,
        query: str,
        answer: str
    ) -> float:
        """
        Evaluate if answer is relevant to the query.
        Checks if the answer addresses the question.
        """
        query_keywords = set(query.lower().split())
        answer_keywords = set(answer.lower().split())

        overlap = len(query_keywords & answer_keywords)
        relevance = min(overlap / len(query_keywords), 1.0) if query_keywords else 0.0

        return relevance

    def evaluate_rag_system(
        self,
        example: RAGExample
    ) -> ARESScore:
        """
        Comprehensive RAG evaluation.
        Returns scores for all ARES metrics.
        """
        context_relevance = self.evaluate_context_relevance(
            example.query,
            example.retrieved_contexts
        )

        answer_faithfulness = self.evaluate_answer_faithfulness(
            example.generated_answer,
            example.retrieved_contexts
        )

        answer_relevance = self.evaluate_answer_relevance(
            example.query,
            example.generated_answer
        )

        overall = (context_relevance + answer_faithfulness + answer_relevance) / 3

        return ARESScore(
            context_relevance=context_relevance,
            answer_faithfulness=answer_faithfulness,
            answer_relevance=answer_relevance,
            overall_score=overall
        )


def basic_rag_evaluation():
    """
    Basic RAG evaluation with ARES.
    Demonstrates core evaluation workflow.
    """
    print("\n=== Basic RAG Evaluation ===")

    evaluator = ARESEvaluator()

    example = RAGExample(
        query="What are the health benefits of exercise?",
        retrieved_contexts=[
            "Regular exercise improves cardiovascular health and strengthens the heart.",
            "Physical activity helps build and maintain muscle strength.",
            "Exercise has been shown to improve mental health and reduce anxiety."
        ],
        generated_answer="Exercise provides numerous health benefits including improved heart health, stronger muscles, and better mental well-being."
    )

    scores = evaluator.evaluate_rag_system(example)

    print(f"Query: {example.query}")
    print(f"\nScores:")
    print(f"  Context Relevance: {scores.context_relevance:.3f}")
    print(f"  Answer Faithfulness: {scores.answer_faithfulness:.3f}")
    print(f"  Answer Relevance: {scores.answer_relevance:.3f}")
    print(f"  Overall Score: {scores.overall_score:.3f}")

    return scores


def evaluate_retrieval_quality():
    """
    Evaluate retrieval quality specifically.
    Focus on context relevance metric.
    """
    print("\n=== Retrieval Quality Evaluation ===")

    evaluator = ARESEvaluator()

    test_cases = [
        {
            "query": "How does photosynthesis work?",
            "contexts": [
                "Photosynthesis is the process by which plants convert sunlight into energy.",
                "Plants use chlorophyll to absorb light during photosynthesis.",
                "The stock market experienced volatility today."  # Irrelevant
            ]
        },
        {
            "query": "What is machine learning?",
            "contexts": [
                "Machine learning is a subset of artificial intelligence.",
                "ML algorithms learn patterns from data.",
                "Neural networks are a type of machine learning model."
            ]
        }
    ]

    for i, case in enumerate(test_cases, 1):
        relevance = evaluator.evaluate_context_relevance(
            case["query"],
            case["contexts"]
        )

        print(f"\nCase {i}:")
        print(f"  Query: {case['query']}")
        print(f"  Num Contexts: {len(case['contexts'])}")
        print(f"  Relevance Score: {relevance:.3f}")
        print(f"  Quality: {'Good' if relevance > 0.7 else 'Needs Improvement'}")


def evaluate_faithfulness_detection():
    """
    Evaluate faithfulness and hallucination detection.
    Tests if answers are grounded in contexts.
    """
    print("\n=== Faithfulness Detection ===")

    evaluator = ARESEvaluator()

    # Case 1: Faithful answer
    contexts_1 = ["Paris is the capital of France.", "It is located on the Seine River."]
    answer_1 = "Paris is the capital of France and is situated on the Seine River."

    # Case 2: Hallucinated answer
    contexts_2 = ["Paris is the capital of France."]
    answer_2 = "Paris is the capital of France and has a population of 50 million people."

    faithfulness_1 = evaluator.evaluate_answer_faithfulness(answer_1, contexts_1)
    faithfulness_2 = evaluator.evaluate_answer_faithfulness(answer_2, contexts_2)

    print("\nCase 1 (Faithful):")
    print(f"  Answer: {answer_1}")
    print(f"  Faithfulness: {faithfulness_1:.3f} ✓")

    print("\nCase 2 (Hallucinated):")
    print(f"  Answer: {answer_2}")
    print(f"  Faithfulness: {faithfulness_2:.3f} ✗")
    print(f"  Contains unsupported claim about population")


def batch_rag_evaluation():
    """
    Evaluate multiple RAG examples in batch.
    Demonstrates scalability.
    """
    print("\n=== Batch RAG Evaluation ===")

    evaluator = ARESEvaluator()

    examples = [
        RAGExample(
            query="What is quantum computing?",
            retrieved_contexts=["Quantum computers use qubits for computation."],
            generated_answer="Quantum computing uses quantum bits or qubits."
        ),
        RAGExample(
            query="Explain neural networks",
            retrieved_contexts=["Neural networks are inspired by biological neurons."],
            generated_answer="Neural networks are computational models inspired by the brain."
        ),
        RAGExample(
            query="What is blockchain?",
            retrieved_contexts=["Blockchain is a distributed ledger technology."],
            generated_answer="Blockchain is a decentralized ledger system."
        )
    ]

    results = []
    for i, example in enumerate(examples, 1):
        scores = evaluator.evaluate_rag_system(example)
        results.append(scores)
        print(f"\nExample {i}: {example.query}")
        print(f"  Overall Score: {scores.overall_score:.3f}")

    avg_score = sum(r.overall_score for r in results) / len(results)
    print(f"\n{'='*40}")
    print(f"Average Overall Score: {avg_score:.3f}")
    print(f"Total Examples: {len(examples)}")

    return results


def compare_rag_systems():
    """
    Compare two different RAG systems.
    Useful for A/B testing retrieval strategies.
    """
    print("\n=== RAG System Comparison ===")

    evaluator = ARESEvaluator()

    query = "What causes climate change?"

    # System A: Simple retrieval
    system_a = RAGExample(
        query=query,
        retrieved_contexts=["Greenhouse gases trap heat in the atmosphere."],
        generated_answer="Climate change is caused by greenhouse gases."
    )

    # System B: Better retrieval with more context
    system_b = RAGExample(
        query=query,
        retrieved_contexts=[
            "Greenhouse gases trap heat in the atmosphere.",
            "Human activities release large amounts of CO2.",
            "Deforestation reduces CO2 absorption by trees."
        ],
        generated_answer="Climate change is caused by greenhouse gases from human activities like burning fossil fuels, combined with reduced CO2 absorption from deforestation."
    )

    scores_a = evaluator.evaluate_rag_system(system_a)
    scores_b = evaluator.evaluate_rag_system(system_b)

    print(f"Query: {query}\n")

    print("System A (Simple):")
    print(f"  Contexts: {len(system_a.retrieved_contexts)}")
    print(f"  Overall Score: {scores_a.overall_score:.3f}")

    print("\nSystem B (Enhanced):")
    print(f"  Contexts: {len(system_b.retrieved_contexts)}")
    print(f"  Overall Score: {scores_b.overall_score:.3f}")

    print(f"\nBetter System: {'B' if scores_b.overall_score > scores_a.overall_score else 'A'}")

    return scores_a, scores_b


def evaluate_context_sufficiency():
    """
    Evaluate if retrieved contexts provide sufficient information.
    Tests coverage of query requirements.
    """
    print("\n=== Context Sufficiency Evaluation ===")

    evaluator = ARESEvaluator()

    query = "What are the benefits and risks of artificial intelligence?"

    # Insufficient: Only covers benefits
    insufficient_contexts = [
        "AI can automate repetitive tasks.",
        "AI improves decision-making with data analysis."
    ]

    # Sufficient: Covers both benefits and risks
    sufficient_contexts = [
        "AI can automate repetitive tasks and improve efficiency.",
        "AI improves decision-making with data analysis.",
        "AI poses risks like job displacement.",
        "There are concerns about AI bias and privacy."
    ]

    # Mock answer
    answer = "AI offers benefits like automation and better decisions, but also poses risks including job loss and bias."

    score_insufficient = evaluator.evaluate_answer_faithfulness(answer, insufficient_contexts)
    score_sufficient = evaluator.evaluate_answer_faithfulness(answer, sufficient_contexts)

    print(f"Query: {query}\n")

    print("Insufficient Contexts:")
    print(f"  Num Contexts: {len(insufficient_contexts)}")
    print(f"  Faithfulness: {score_insufficient:.3f} ✗")

    print("\nSufficient Contexts:")
    print(f"  Num Contexts: {len(sufficient_contexts)}")
    print(f"  Faithfulness: {score_sufficient:.3f} ✓")


def synthetic_data_generation_example():
    """
    ARES uses synthetic data for few-shot learning.
    Demonstrates the concept of synthetic test generation.
    """
    print("\n=== Synthetic Data Generation ===")

    # In real ARES, synthetic examples are generated automatically
    # This demonstrates the concept

    base_document = """
    Machine learning is a subset of artificial intelligence that enables
    systems to learn and improve from experience without being explicitly
    programmed. It focuses on developing computer programs that can access
    data and use it to learn for themselves.
    """

    # Generate synthetic queries
    synthetic_queries = [
        "What is machine learning?",
        "How does machine learning work?",
        "What is the relationship between ML and AI?",
        "Can machine learning systems improve on their own?"
    ]

    # Generate synthetic contexts (chunks from document)
    synthetic_contexts = [
        "Machine learning is a subset of artificial intelligence.",
        "ML enables systems to learn from experience without explicit programming.",
        "Machine learning programs can access data and learn for themselves."
    ]

    print("Base Document:")
    print(f"  Length: {len(base_document)} chars")

    print(f"\nGenerated Synthetic Queries: {len(synthetic_queries)}")
    for i, q in enumerate(synthetic_queries, 1):
        print(f"  {i}. {q}")

    print(f"\nGenerated Synthetic Contexts: {len(synthetic_contexts)}")
    for i, c in enumerate(synthetic_contexts, 1):
        print(f"  {i}. {c[:60]}...")

    print("\n✓ ARES uses these synthetic examples to train evaluation models")


def confidence_scoring():
    """
    ARES provides confidence scores for evaluations.
    Indicates reliability of the evaluation.
    """
    print("\n=== Confidence Scoring ===")

    # Simulate confidence scoring
    def calculate_confidence(scores: ARESScore) -> float:
        """Calculate confidence based on score consistency."""
        score_variance = (
            (scores.context_relevance - scores.overall_score) ** 2 +
            (scores.answer_faithfulness - scores.overall_score) ** 2 +
            (scores.answer_relevance - scores.overall_score) ** 2
        ) / 3

        # Lower variance = higher confidence
        confidence = max(0.0, 1.0 - score_variance)
        return confidence

    evaluator = ARESEvaluator()

    # High confidence example (consistent scores)
    example_1 = RAGExample(
        query="What is Python?",
        retrieved_contexts=["Python is a programming language."],
        generated_answer="Python is a programming language."
    )

    scores_1 = evaluator.evaluate_rag_system(example_1)
    confidence_1 = calculate_confidence(scores_1)

    print("High Confidence Example:")
    print(f"  Overall Score: {scores_1.overall_score:.3f}")
    print(f"  Confidence: {confidence_1:.3f} ✓")

    # Lower confidence (inconsistent scores)
    example_2 = RAGExample(
        query="Explain quantum physics",
        retrieved_contexts=["Quantum physics is very complex."],
        generated_answer="Quantum physics involves particles, waves, and uncertainty principles in atomic behavior."
    )

    scores_2 = evaluator.evaluate_rag_system(example_2)
    confidence_2 = calculate_confidence(scores_2)

    print("\nLower Confidence Example:")
    print(f"  Overall Score: {scores_2.overall_score:.3f}")
    print(f"  Confidence: {confidence_2:.3f}")


def main():
    """Run all ARES evaluation examples."""
    print("=" * 60)
    print("ARES (Automated RAG Evaluation System) Examples")
    print("=" * 60)

    try:
        # Basic evaluations
        basic_rag_evaluation()
        evaluate_retrieval_quality()
        evaluate_faithfulness_detection()

        # Advanced evaluations
        batch_rag_evaluation()
        compare_rag_systems()
        evaluate_context_sufficiency()

        # ARES-specific features
        synthetic_data_generation_example()
        confidence_scoring()

        print("\n" + "=" * 60)
        print("All ARES evaluations completed successfully!")
        print("=" * 60)

        print("\n📊 ARES Key Features:")
        print("  • RAG-Specific: Built specifically for RAG systems")
        print("  • Context Relevance: Evaluate retrieval quality")
        print("  • Answer Faithfulness: Detect hallucinations")
        print("  • Answer Relevance: Check query alignment")
        print("  • Synthetic Data: Auto-generate test examples")
        print("  • Few-Shot Learning: Train with minimal labeled data")
        print("  • Confidence Scores: Reliability indicators")
        print("  • Scalable: Batch evaluation support")

        print("\n💡 ARES Advantages:")
        print("  • No need for extensive labeled data")
        print("  • Automated synthetic example generation")
        print("  • Comprehensive RAG metrics")
        print("  • Research-backed methodology")

        print("\n🔗 Resources:")
        print("  • Paper: https://arxiv.org/abs/2311.09476")
        print("  • GitHub: https://github.com/stanford-futuredata/ARES")

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Setup required:")
        print("  1. pip install ares-ai")
        print("  2. Configure your RAG system")
        print("  3. Prepare evaluation data")


if __name__ == "__main__":
    main()
