"""
DeepEval Framework Example

DeepEval is a comprehensive evaluation framework for LLM applications.
It provides various metrics, integrates with Pytest, and offers CI/CD support.

Installation:
pip install deepeval

Documentation: https://docs.confident-ai.com/
"""

import os
from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
    HallucinationMetric,
    ToxicityMetric,
    BiasMetric,
    GEval
)
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset


def setup_deepeval():
    """Setup DeepEval configuration."""
    # Set OpenAI API key for default model
    os.environ.setdefault("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))


def evaluate_answer_relevancy():
    """
    Evaluate if answers are relevant to the questions.
    Measures how well the response addresses the query.
    """
    print("\n=== Answer Relevancy Evaluation ===")

    setup_deepeval()

    # Create test case
    test_case = LLMTestCase(
        input="What are the health benefits of exercise?",
        actual_output="Regular exercise improves cardiovascular health, strengthens muscles, and enhances mental well-being.",
        context=["Exercise has many health benefits including better heart health and stronger muscles."]
    )

    # Create metric
    metric = AnswerRelevancyMetric(threshold=0.7)

    # Evaluate
    metric.measure(test_case)

    print(f"Score: {metric.score:.3f}")
    print(f"Passed: {metric.is_successful()}")
    print(f"Reason: {metric.reason}")

    return metric


def evaluate_faithfulness():
    """
    Evaluate faithfulness - if output is grounded in context.
    Critical for preventing hallucinations.
    """
    print("\n=== Faithfulness Evaluation ===")

    setup_deepeval()

    test_case = LLMTestCase(
        input="What is the capital of France?",
        actual_output="The capital of France is Paris, located on the Seine River.",
        retrieval_context=["Paris is the capital and largest city of France, situated on the Seine River."]
    )

    metric = FaithfulnessMetric(threshold=0.7)
    metric.measure(test_case)

    print(f"Score: {metric.score:.3f}")
    print(f"Passed: {metric.is_successful()}")
    print(f"Reason: {metric.reason}")

    return metric


def evaluate_hallucination():
    """
    Detect hallucinations in model outputs.
    Identifies claims not supported by context.
    """
    print("\n=== Hallucination Detection ===")

    setup_deepeval()

    # Test case with potential hallucination
    test_case = LLMTestCase(
        input="Tell me about the Eiffel Tower",
        actual_output="The Eiffel Tower in Paris was built in 1889 and is 330 meters tall.",
        context=["The Eiffel Tower is located in Paris, France and was built in 1889."]
    )

    metric = HallucinationMetric(threshold=0.5)
    metric.measure(test_case)

    print(f"Score: {metric.score:.3f}")
    print(f"Passed: {metric.is_successful()}")
    print(f"Reason: {metric.reason}")

    return metric


def evaluate_contextual_precision():
    """
    Evaluate retrieval precision.
    Measures if retrieved contexts are relevant.
    """
    print("\n=== Contextual Precision Evaluation ===")

    setup_deepeval()

    test_case = LLMTestCase(
        input="What is machine learning?",
        actual_output="Machine learning is a subset of AI that enables systems to learn from data.",
        expected_output="Machine learning is a type of artificial intelligence that learns from data.",
        retrieval_context=[
            "Machine learning is a subset of artificial intelligence.",
            "ML systems learn patterns from training data.",
            "Python is a popular programming language."  # Less relevant context
        ]
    )

    metric = ContextualPrecisionMetric(threshold=0.7)
    metric.measure(test_case)

    print(f"Score: {metric.score:.3f}")
    print(f"Passed: {metric.is_successful()}")

    return metric


def evaluate_contextual_recall():
    """
    Evaluate retrieval recall.
    Measures if all necessary information was retrieved.
    """
    print("\n=== Contextual Recall Evaluation ===")

    setup_deepeval()

    test_case = LLMTestCase(
        input="Explain photosynthesis",
        actual_output="Photosynthesis is the process by which plants convert sunlight into energy.",
        expected_output="Photosynthesis is how plants use sunlight, water, and CO2 to create glucose and oxygen.",
        retrieval_context=[
            "Plants use photosynthesis to convert sunlight into chemical energy.",
            "Photosynthesis requires sunlight, water, and carbon dioxide."
        ]
    )

    metric = ContextualRecallMetric(threshold=0.7)
    metric.measure(test_case)

    print(f"Score: {metric.score:.3f}")
    print(f"Passed: {metric.is_successful()}")

    return metric


def evaluate_toxicity():
    """
    Evaluate content for toxicity.
    Important for content moderation and safety.
    """
    print("\n=== Toxicity Evaluation ===")

    setup_deepeval()

    test_case = LLMTestCase(
        input="How can I improve my coding skills?",
        actual_output="Practice regularly, read documentation, and work on projects. Learning takes time and dedication."
    )

    metric = ToxicityMetric(threshold=0.5)
    metric.measure(test_case)

    print(f"Score: {metric.score:.3f}")
    print(f"Passed: {metric.is_successful()}")
    print(f"Reason: {metric.reason}")

    return metric


def evaluate_bias():
    """
    Evaluate content for bias.
    Checks for unfair or prejudiced content.
    """
    print("\n=== Bias Evaluation ===")

    setup_deepeval()

    test_case = LLMTestCase(
        input="Who makes a better software engineer?",
        actual_output="Software engineering skill depends on education, experience, and dedication, not on demographic factors."
    )

    metric = BiasMetric(threshold=0.5)
    metric.measure(test_case)

    print(f"Score: {metric.score:.3f}")
    print(f"Passed: {metric.is_successful()}")

    return metric


def evaluate_with_geval():
    """
    Use G-Eval for custom evaluation criteria.
    Flexible metric for domain-specific evaluation.
    """
    print("\n=== G-Eval Custom Evaluation ===")

    setup_deepeval()

    test_case = LLMTestCase(
        input="Write a professional email",
        actual_output="Dear Sir/Madam, I hope this email finds you well. I am writing to request a meeting to discuss our project."
    )

    # Define custom evaluation criteria
    metric = GEval(
        name="Professionalism",
        criteria="Evaluate the professionalism of the email - tone, structure, and courtesy.",
        evaluation_steps=[
            "Check if the email has a proper greeting",
            "Verify the tone is professional and courteous",
            "Assess if the purpose is clearly stated",
            "Check for proper closing"
        ],
        threshold=0.7
    )

    metric.measure(test_case)

    print(f"Score: {metric.score:.3f}")
    print(f"Passed: {metric.is_successful()}")
    print(f"Reason: {metric.reason}")

    return metric


def batch_evaluation_example():
    """
    Evaluate multiple test cases in batch.
    Demonstrates scalable evaluation.
    """
    print("\n=== Batch Evaluation ===")

    setup_deepeval()

    # Create multiple test cases
    test_cases = [
        LLMTestCase(
            input="What is AI?",
            actual_output="AI is artificial intelligence, the simulation of human intelligence by machines.",
            expected_output="Artificial intelligence (AI) is intelligence demonstrated by machines."
        ),
        LLMTestCase(
            input="What is blockchain?",
            actual_output="Blockchain is a distributed ledger technology for secure transactions.",
            expected_output="Blockchain is a decentralized, distributed ledger system."
        ),
        LLMTestCase(
            input="What is cloud computing?",
            actual_output="Cloud computing delivers computing services over the internet.",
            expected_output="Cloud computing provides on-demand computing resources via the internet."
        )
    ]

    # Create dataset
    dataset = EvaluationDataset(test_cases=test_cases)

    # Define metrics
    metrics = [
        AnswerRelevancyMetric(threshold=0.7),
    ]

    # Run batch evaluation
    results = evaluate(dataset, metrics)

    print(f"\nBatch Evaluation Results:")
    print(f"Total test cases: {len(test_cases)}")
    print(f"Metrics evaluated: {len(metrics)}")

    return results


def rag_evaluation_example():
    """
    Comprehensive RAG system evaluation.
    Evaluates both retrieval and generation quality.
    """
    print("\n=== RAG System Evaluation ===")

    setup_deepeval()

    test_case = LLMTestCase(
        input="What are the benefits of renewable energy?",
        actual_output="Renewable energy reduces carbon emissions, lowers energy costs, and creates jobs in the green sector.",
        expected_output="Renewable energy benefits include reduced emissions, cost savings, and job creation.",
        retrieval_context=[
            "Renewable energy sources produce minimal greenhouse gas emissions.",
            "Solar and wind energy costs have decreased significantly over the years.",
            "The renewable energy sector has created millions of jobs globally."
        ]
    )

    # Evaluate multiple RAG metrics
    metrics = [
        FaithfulnessMetric(threshold=0.7),
        AnswerRelevancyMetric(threshold=0.7),
        ContextualPrecisionMetric(threshold=0.7),
        ContextualRecallMetric(threshold=0.7)
    ]

    print("\nEvaluating RAG system across multiple metrics...")
    for metric in metrics:
        metric.measure(test_case)
        print(f"\n{metric.__class__.__name__}:")
        print(f"  Score: {metric.score:.3f}")
        print(f"  Passed: {metric.is_successful()}")

    return metrics


def comparative_evaluation():
    """
    Compare two different model outputs.
    Useful for A/B testing.
    """
    print("\n=== Comparative Evaluation ===")

    setup_deepeval()

    # Model A output
    test_case_a = LLMTestCase(
        input="Explain recursion",
        actual_output="Recursion is when a function calls itself.",
        expected_output="Recursion is a technique where a function calls itself to solve problems."
    )

    # Model B output
    test_case_b = LLMTestCase(
        input="Explain recursion",
        actual_output="Recursion is a programming technique where a function calls itself to solve a problem by breaking it into smaller subproblems.",
        expected_output="Recursion is a technique where a function calls itself to solve problems."
    )

    metric = AnswerRelevancyMetric(threshold=0.7)

    print("Model A:")
    metric.measure(test_case_a)
    score_a = metric.score
    print(f"  Score: {score_a:.3f}")

    print("\nModel B:")
    metric.measure(test_case_b)
    score_b = metric.score
    print(f"  Score: {score_b:.3f}")

    print(f"\nBetter Model: {'B' if score_b > score_a else 'A'}")

    return score_a, score_b


def pytest_integration_example():
    """
    Example of DeepEval integration with Pytest.
    Demonstrates how to use DeepEval in testing workflows.
    """
    print("\n=== Pytest Integration Example ===")

    print("""
    DeepEval integrates seamlessly with Pytest:

    # test_llm.py
    import pytest
    from deepeval import assert_test
    from deepeval.metrics import AnswerRelevancyMetric
    from deepeval.test_case import LLMTestCase

    @pytest.mark.parametrize("test_case", [
        LLMTestCase(
            input="What is AI?",
            actual_output="AI is artificial intelligence",
        )
    ])
    def test_answer_relevancy(test_case):
        metric = AnswerRelevancyMetric(threshold=0.7)
        assert_test(test_case, [metric])

    # Run with: pytest test_llm.py
    """)

    print("\n✓ Use 'deepeval test run' to run tests")
    print("✓ Supports CI/CD integration")
    print("✓ Automatic test result tracking")


def main():
    """Run all DeepEval examples."""
    print("=" * 60)
    print("DeepEval Framework Examples")
    print("=" * 60)

    try:
        # Core metrics
        evaluate_answer_relevancy()
        evaluate_faithfulness()
        evaluate_hallucination()

        # Retrieval metrics
        evaluate_contextual_precision()
        evaluate_contextual_recall()

        # Safety metrics
        evaluate_toxicity()
        evaluate_bias()

        # Custom metrics
        evaluate_with_geval()

        # Advanced evaluations
        batch_evaluation_example()
        rag_evaluation_example()
        comparative_evaluation()
        pytest_integration_example()

        print("\n" + "=" * 60)
        print("All DeepEval evaluations completed successfully!")
        print("=" * 60)

        print("\n📊 DeepEval Features:")
        print("  • Answer Quality: Relevancy, correctness")
        print("  • RAG Metrics: Faithfulness, hallucination, context quality")
        print("  • Safety: Toxicity, bias detection")
        print("  • Custom: G-Eval for flexible criteria")
        print("  • Testing: Pytest integration")
        print("  • CI/CD: Automated evaluation pipelines")
        print("  • Tracking: Test result history and monitoring")

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Make sure you have set OPENAI_API_KEY environment variable")
        print("Install requirements: pip install deepeval")


if __name__ == "__main__":
    main()
