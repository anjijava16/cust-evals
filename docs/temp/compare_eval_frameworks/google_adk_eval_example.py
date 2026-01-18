"""
Google ADK (Agent Development Kit) Evaluation Example

Google ADK provides comprehensive evaluation capabilities for AI agents and LLM applications.
Includes CLI-based evaluation, custom metrics, and dataset management.

Installation:
pip install google-adk

Documentation: https://google.github.io/adk-docs/evaluate/
"""

import os
import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


# Note: Google ADK evaluation is primarily CLI-based, but we'll demonstrate
# the concepts programmatically and show CLI usage patterns


@dataclass
class EvalExample:
    """Evaluation example format for ADK."""
    input: str
    expected_output: str
    metadata: Dict[str, Any] = None


@dataclass
class EvalResult:
    """Evaluation result."""
    example_id: str
    score: float
    passed: bool
    details: Dict[str, Any]


class ADKEvaluator:
    """Base class for ADK-style evaluators."""

    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
        self.results = []

    def evaluate_example(self, prediction: str, expected: str, input_text: str) -> EvalResult:
        """Evaluate a single example."""
        raise NotImplementedError

    def evaluate_dataset(self, examples: List[EvalExample], predictions: List[str]) -> Dict[str, Any]:
        """Evaluate full dataset."""
        results = []
        for i, (example, prediction) in enumerate(zip(examples, predictions)):
            result = self.evaluate_example(
                prediction=prediction,
                expected=example.expected_output,
                input_text=example.input
            )
            results.append(result)

        # Calculate aggregate metrics
        scores = [r.score for r in results]
        passed_count = sum(1 for r in results if r.passed)

        return {
            "average_score": sum(scores) / len(scores) if scores else 0,
            "pass_rate": passed_count / len(results) if results else 0,
            "total_examples": len(results),
            "passed_examples": passed_count,
            "results": results
        }


class ExactMatchEvaluator(ADKEvaluator):
    """Exact match evaluator."""

    def evaluate_example(self, prediction: str, expected: str, input_text: str) -> EvalResult:
        """Check if prediction exactly matches expected output."""
        prediction_clean = prediction.strip().lower()
        expected_clean = expected.strip().lower()

        passed = prediction_clean == expected_clean
        score = 1.0 if passed else 0.0

        return EvalResult(
            example_id=f"example_{hash(input_text)}",
            score=score,
            passed=passed,
            details={
                "prediction": prediction,
                "expected": expected,
                "match_type": "exact"
            }
        )


class SemanticSimilarityEvaluator(ADKEvaluator):
    """Semantic similarity evaluator using embeddings."""

    def __init__(self, threshold: float = 0.8):
        super().__init__(threshold)

    def evaluate_example(self, prediction: str, expected: str, input_text: str) -> EvalResult:
        """Evaluate semantic similarity."""
        # In real implementation, use embeddings model
        # For demo, use simple word overlap
        pred_words = set(prediction.lower().split())
        exp_words = set(expected.lower().split())

        if not pred_words or not exp_words:
            score = 0.0
        else:
            overlap = len(pred_words & exp_words)
            union = len(pred_words | exp_words)
            score = overlap / union if union > 0 else 0.0

        passed = score >= self.threshold

        return EvalResult(
            example_id=f"example_{hash(input_text)}",
            score=score,
            passed=passed,
            details={
                "prediction": prediction,
                "expected": expected,
                "similarity": score
            }
        )


class LLMJudgeEvaluator(ADKEvaluator):
    """LLM-based evaluation using Gemini."""

    def __init__(self, threshold: float = 0.7):
        super().__init__(threshold)
        self.setup_gemini()

    def setup_gemini(self):
        """Setup Gemini for evaluation."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print(f"Warning: Could not setup Gemini: {e}")
            self.model = None

    def evaluate_example(self, prediction: str, expected: str, input_text: str) -> EvalResult:
        """Evaluate using LLM judge."""
        if not self.model:
            # Fallback to simple evaluation
            score = 0.5
            passed = False
        else:
            prompt = f"""
            Evaluate the following answer on a scale of 0.0 to 1.0.

            Question: {input_text}
            Expected Answer: {expected}
            Actual Answer: {prediction}

            Consider accuracy, completeness, and relevance.
            Respond with just a number between 0.0 and 1.0.
            """

            try:
                response = self.model.generate_content(prompt)
                score_text = response.text.strip()
                score = float(score_text)
                score = max(0.0, min(1.0, score))
            except Exception as e:
                print(f"Error in LLM evaluation: {e}")
                score = 0.5

        passed = score >= self.threshold

        return EvalResult(
            example_id=f"example_{hash(input_text)}",
            score=score,
            passed=passed,
            details={
                "prediction": prediction,
                "expected": expected,
                "llm_score": score
            }
        )


def create_eval_dataset():
    """
    Create evaluation dataset in ADK format.
    ADK uses JSONL format for datasets.
    """
    print("\n=== Creating Evaluation Dataset ===")

    examples = [
        EvalExample(
            input="What is the capital of France?",
            expected_output="Paris",
            metadata={"category": "geography", "difficulty": "easy"}
        ),
        EvalExample(
            input="Who wrote Romeo and Juliet?",
            expected_output="William Shakespeare",
            metadata={"category": "literature", "difficulty": "easy"}
        ),
        EvalExample(
            input="What is 2+2?",
            expected_output="4",
            metadata={"category": "math", "difficulty": "easy"}
        ),
        EvalExample(
            input="What is machine learning?",
            expected_output="Machine learning is a subset of AI that enables systems to learn from data.",
            metadata={"category": "technology", "difficulty": "medium"}
        )
    ]

    print(f"Created dataset with {len(examples)} examples")
    return examples


def save_dataset_jsonl(examples: List[EvalExample], filename: str = "eval_dataset.jsonl"):
    """Save dataset in JSONL format for ADK CLI."""
    print(f"\n=== Saving Dataset to {filename} ===")

    with open(filename, 'w') as f:
        for example in examples:
            json_line = json.dumps(asdict(example))
            f.write(json_line + '\n')

    print(f"✓ Saved {len(examples)} examples to {filename}")


def run_exact_match_evaluation():
    """
    Run exact match evaluation.
    Demonstrates basic evaluation pattern.
    """
    print("\n=== Exact Match Evaluation ===")

    # Create dataset
    examples = create_eval_dataset()

    # Simulate model predictions
    predictions = [
        "Paris",
        "William Shakespeare",
        "4",
        "Machine learning is a subset of artificial intelligence."
    ]

    # Run evaluation
    evaluator = ExactMatchEvaluator()
    results = evaluator.evaluate_dataset(examples, predictions)

    print(f"\nResults:")
    print(f"  Average Score: {results['average_score']:.2%}")
    print(f"  Pass Rate: {results['pass_rate']:.2%}")
    print(f"  Passed: {results['passed_examples']}/{results['total_examples']}")

    return results


def run_semantic_evaluation():
    """
    Run semantic similarity evaluation.
    Allows for paraphrased answers.
    """
    print("\n=== Semantic Similarity Evaluation ===")

    examples = create_eval_dataset()

    # Predictions with paraphrasing
    predictions = [
        "The capital of France is Paris",
        "Shakespeare wrote Romeo and Juliet",
        "Two plus two equals four",
        "ML is a type of AI that learns from data"
    ]

    evaluator = SemanticSimilarityEvaluator(threshold=0.6)
    results = evaluator.evaluate_dataset(examples, predictions)

    print(f"\nResults:")
    print(f"  Average Score: {results['average_score']:.2%}")
    print(f"  Pass Rate: {results['pass_rate']:.2%}")

    return results


def run_llm_judge_evaluation():
    """
    Run LLM-as-judge evaluation.
    Uses Gemini to evaluate quality.
    """
    print("\n=== LLM Judge Evaluation ===")

    examples = create_eval_dataset()

    predictions = [
        "Paris is the capital city of France.",
        "The famous playwright William Shakespeare wrote Romeo and Juliet.",
        "4",
        "Machine learning is a branch of AI focused on building systems that learn from data."
    ]

    evaluator = LLMJudgeEvaluator(threshold=0.7)
    results = evaluator.evaluate_dataset(examples, predictions)

    print(f"\nResults:")
    print(f"  Average Score: {results['average_score']:.2%}")
    print(f"  Pass Rate: {results['pass_rate']:.2%}")

    return results


def custom_metric_evaluation():
    """
    Define and use custom evaluation metrics.
    Demonstrates extensibility.
    """
    print("\n=== Custom Metric Evaluation ===")

    class LengthConstraintEvaluator(ADKEvaluator):
        """Custom evaluator checking answer length."""

        def __init__(self, min_words: int = 3, max_words: int = 50):
            super().__init__()
            self.min_words = min_words
            self.max_words = max_words

        def evaluate_example(self, prediction: str, expected: str, input_text: str) -> EvalResult:
            word_count = len(prediction.split())

            if self.min_words <= word_count <= self.max_words:
                score = 1.0
                passed = True
                message = "Length appropriate"
            elif word_count < self.min_words:
                score = 0.5
                passed = False
                message = "Too short"
            else:
                score = 0.7
                passed = False
                message = "Too long"

            return EvalResult(
                example_id=f"example_{hash(input_text)}",
                score=score,
                passed=passed,
                details={
                    "word_count": word_count,
                    "message": message
                }
            )

    examples = create_eval_dataset()
    predictions = [
        "Paris",  # Very short
        "William Shakespeare",  # Good length
        "4",  # Very short
        "Machine learning is a subset of artificial intelligence that enables computer systems to learn and improve from experience without being explicitly programmed for each task."  # Long
    ]

    evaluator = LengthConstraintEvaluator(min_words=2, max_words=20)
    results = evaluator.evaluate_dataset(examples, predictions)

    print(f"\nResults:")
    print(f"  Average Score: {results['average_score']:.2%}")
    print(f"  Pass Rate: {results['pass_rate']:.2%}")

    return results


def multi_metric_evaluation():
    """
    Run multiple metrics on the same dataset.
    Provides comprehensive evaluation.
    """
    print("\n=== Multi-Metric Evaluation ===")

    examples = create_eval_dataset()
    predictions = [
        "Paris is the capital",
        "Shakespeare",
        "Four",
        "ML learns from data"
    ]

    # Run multiple evaluators
    evaluators = {
        "exact_match": ExactMatchEvaluator(),
        "semantic": SemanticSimilarityEvaluator(threshold=0.5),
        "length": custom_metric_evaluation.__code__.co_consts[1]  # LengthConstraintEvaluator
    }

    all_results = {}
    for name, evaluator in [
        ("exact_match", ExactMatchEvaluator()),
        ("semantic", SemanticSimilarityEvaluator(threshold=0.5))
    ]:
        results = evaluator.evaluate_dataset(examples, predictions)
        all_results[name] = results
        print(f"\n{name}:")
        print(f"  Score: {results['average_score']:.2%}")
        print(f"  Pass Rate: {results['pass_rate']:.2%}")

    return all_results


def cli_usage_examples():
    """
    Demonstrate ADK CLI usage patterns.
    Shows how to use ADK from command line.
    """
    print("\n=== ADK CLI Usage Examples ===")

    print("""
    Google ADK evaluation is primarily CLI-based. Here are common commands:

    1. Basic Evaluation:
    ───────────────────────────────────────────────────────────────
    $ adk eval run \\
        --dataset eval_dataset.jsonl \\
        --model gemini-pro \\
        --evaluator exact_match

    2. Custom Metric Evaluation:
    ───────────────────────────────────────────────────────────────
    $ adk eval run \\
        --dataset eval_dataset.jsonl \\
        --model gemini-pro \\
        --evaluator custom_evaluator.py \\
        --output results.json

    3. Multi-Model Comparison:
    ───────────────────────────────────────────────────────────────
    $ adk eval compare \\
        --dataset eval_dataset.jsonl \\
        --models gemini-pro,gemini-ultra \\
        --evaluator semantic_similarity

    4. Generate Evaluation Report:
    ───────────────────────────────────────────────────────────────
    $ adk eval report \\
        --results results.json \\
        --format html \\
        --output report.html

    5. Batch Evaluation:
    ───────────────────────────────────────────────────────────────
    $ adk eval batch \\
        --config eval_config.yaml \\
        --parallel 4

    6. Create Dataset:
    ───────────────────────────────────────────────────────────────
    $ adk dataset create \\
        --name my_eval_dataset \\
        --from-jsonl data.jsonl

    7. Custom Python Evaluator:
    ───────────────────────────────────────────────────────────────
    # custom_evaluator.py
    from adk.eval import Evaluator

    class MyEvaluator(Evaluator):
        def evaluate(self, prediction, expected, input):
            # Your evaluation logic
            return {"score": 0.9, "passed": True}

    $ adk eval run \\
        --evaluator custom_evaluator.py:MyEvaluator

    """)

    print("\n✓ See https://google.github.io/adk-docs/evaluate/ for full documentation")


def agent_evaluation_example():
    """
    Evaluate AI agent responses.
    ADK is designed for agent evaluation.
    """
    print("\n=== Agent Evaluation Example ===")

    @dataclass
    class AgentExample:
        """Agent task example."""
        task: str
        expected_actions: List[str]
        expected_result: str

    agent_examples = [
        AgentExample(
            task="Book a flight from NYC to SF for next Monday",
            expected_actions=["search_flights", "filter_by_date", "select_flight", "book"],
            expected_result="Flight booked successfully"
        ),
        AgentExample(
            task="Find the weather in Tokyo",
            expected_actions=["get_location", "fetch_weather"],
            expected_result="Weather information retrieved"
        )
    ]

    print(f"Created {len(agent_examples)} agent evaluation examples")
    print("\nAgent evaluation typically checks:")
    print("  • Correct action sequence")
    print("  • Task completion")
    print("  • Error handling")
    print("  • Response quality")

    return agent_examples


def batch_evaluation_example():
    """
    Demonstrate batch evaluation for scale.
    Evaluates large datasets efficiently.
    """
    print("\n=== Batch Evaluation Example ===")

    # Create larger dataset
    examples = []
    for i in range(20):
        examples.append(EvalExample(
            input=f"Question {i}",
            expected_output=f"Answer {i}",
            metadata={"batch": "test", "index": i}
        ))

    predictions = [f"Response {i}" for i in range(20)]

    evaluator = SemanticSimilarityEvaluator()
    results = evaluator.evaluate_dataset(examples, predictions)

    print(f"\nBatch Evaluation Results:")
    print(f"  Total Examples: {results['total_examples']}")
    print(f"  Average Score: {results['average_score']:.2%}")
    print(f"  Pass Rate: {results['pass_rate']:.2%}")

    return results


def main():
    """Run all Google ADK evaluation examples."""
    print("=" * 60)
    print("Google ADK (Agent Development Kit) Evaluation Examples")
    print("=" * 60)

    try:
        # Create and save dataset
        examples = create_eval_dataset()
        save_dataset_jsonl(examples)

        # Run evaluations
        run_exact_match_evaluation()
        run_semantic_evaluation()
        run_llm_judge_evaluation()

        # Custom metrics
        custom_metric_evaluation()
        multi_metric_evaluation()

        # Agent evaluation
        agent_evaluation_example()

        # Batch evaluation
        batch_evaluation_example()

        # CLI examples
        cli_usage_examples()

        print("\n" + "=" * 60)
        print("All ADK evaluations completed successfully!")
        print("=" * 60)

        print("\n📊 Google ADK Features:")
        print("  • CLI-First: Powerful command-line tools")
        print("  • Agent Evaluation: Built for AI agents")
        print("  • Custom Metrics: Extensible evaluator system")
        print("  • Multi-Model: Compare different models")
        print("  • Batch Processing: Scale to large datasets")
        print("  • JSONL Format: Standard dataset format")
        print("  • Gemini Integration: Native Google model support")
        print("  • Reporting: Generate evaluation reports")

        print("\n💡 Next Steps:")
        print("  1. Install: pip install google-adk")
        print("  2. Setup: gcloud auth application-default login")
        print("  3. Run: adk eval run --dataset eval_dataset.jsonl")
        print("  4. Docs: https://google.github.io/adk-docs/evaluate/")

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Setup required:")
        print("  1. pip install google-adk google-generativeai")
        print("  2. Set GOOGLE_API_KEY environment variable")


if __name__ == "__main__":
    main()
