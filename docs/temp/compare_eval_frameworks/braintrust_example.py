"""
Braintrust Evaluation Example

Braintrust is an AI product evaluation platform with excellent developer experience.
It provides automatic versioning, dataset management, CI/CD integration, and real-time evaluation.

Installation:
pip install braintrust

Documentation: https://www.braintrust.dev/docs
"""

import os
from braintrust import Eval, init_logger, current_span, traced
from typing import List, Dict, Any
import time


def setup_braintrust():
    """Initialize Braintrust."""
    # Set API key
    api_key = os.getenv("BRAINTRUST_API_KEY", "")

    # Initialize logger (creates project if doesn't exist)
    logger = init_logger(project="llm-evaluation-examples")

    print("✓ Braintrust initialized")
    print(f"  View at: https://www.braintrust.dev/")

    return logger


def basic_evaluation_example():
    """
    Basic evaluation with Braintrust.
    Simple scoring of model outputs.
    """
    print("\n=== Basic Evaluation Example ===")

    @traced
    def qa_model(question: str) -> str:
        """Simple Q&A model with tracing."""
        answers = {
            "What is AI?": "Artificial Intelligence is the simulation of human intelligence by machines.",
            "What is ML?": "Machine Learning is a subset of AI that enables systems to learn from data.",
            "What is DL?": "Deep Learning is a subset of ML that uses neural networks with multiple layers."
        }
        return answers.get(question, "I don't know.")

    def accuracy_scorer(output: str, expected: str) -> float:
        """Score based on keyword overlap."""
        output_words = set(output.lower().split())
        expected_words = set(expected.lower().split())

        if not expected_words:
            return 0.0

        overlap = output_words.intersection(expected_words)
        score = len(overlap) / len(expected_words)

        return score

    # Run evaluation
    eval_result = Eval(
        "Basic Q&A Evaluation",
        data=[
            {
                "input": "What is AI?",
                "expected": "Artificial Intelligence machine simulation"
            },
            {
                "input": "What is ML?",
                "expected": "Machine Learning AI subset data"
            },
            {
                "input": "What is DL?",
                "expected": "Deep Learning neural networks layers"
            }
        ],
        task=lambda input: qa_model(input["input"]),
        scores=[
            lambda output, expected: accuracy_scorer(output, expected["expected"])
        ]
    )

    print("\n✓ Evaluation completed:")
    print(f"  Test cases: {len(eval_result)}")
    print(f"  Automatic versioning enabled")
    print(f"  Results logged to Braintrust")

    return eval_result


def dataset_management_example():
    """
    Manage evaluation datasets in Braintrust.
    Datasets are versioned and reusable.
    """
    print("\n=== Dataset Management Example ===")

    # Define evaluation dataset
    evaluation_dataset = [
        {
            "input": "Explain quantum computing",
            "expected": "Quantum computing uses quantum mechanics principles like superposition and entanglement",
            "category": "technology",
            "difficulty": "advanced"
        },
        {
            "input": "What is photosynthesis?",
            "expected": "Photosynthesis is the process plants use to convert light into chemical energy",
            "category": "science",
            "difficulty": "basic"
        },
        {
            "input": "Define machine learning",
            "expected": "Machine learning is a type of AI that learns from data without explicit programming",
            "category": "technology",
            "difficulty": "intermediate"
        }
    ]

    print("✓ Dataset created:")
    print(f"  Total examples: {len(evaluation_dataset)}")
    print(f"  Categories: {set(item['category'] for item in evaluation_dataset)}")
    print(f"  Difficulty levels: {set(item['difficulty'] for item in evaluation_dataset)}")
    print(f"  Dataset automatically versioned")

    return evaluation_dataset


def custom_scoring_example():
    """
    Create custom scoring functions.
    Multiple scoring dimensions for comprehensive evaluation.
    """
    print("\n=== Custom Scoring Example ===")

    def relevance_scorer(output: str, expected: Dict) -> Dict[str, Any]:
        """Score answer relevance."""
        question_keywords = set(expected["input"].lower().split())
        answer_keywords = set(output.lower().split())

        relevant = question_keywords.intersection(answer_keywords)
        score = len(relevant) / len(question_keywords) if question_keywords else 0.0

        return {
            "name": "relevance",
            "score": score,
            "metadata": {
                "relevant_keywords": list(relevant),
                "total_question_keywords": len(question_keywords)
            }
        }

    def completeness_scorer(output: str, expected: Dict) -> Dict[str, Any]:
        """Score answer completeness."""
        min_length = 20
        ideal_length = 100

        length = len(output)
        score = min(length / ideal_length, 1.0) if length >= min_length else 0.0

        return {
            "name": "completeness",
            "score": score,
            "metadata": {
                "length": length,
                "meets_minimum": length >= min_length
            }
        }

    def factual_accuracy_scorer(output: str, expected: Dict) -> Dict[str, Any]:
        """Score factual accuracy based on expected answer."""
        expected_answer = expected["expected"].lower()
        output_lower = output.lower()

        # Check if key concepts from expected answer appear in output
        expected_concepts = set(expected_answer.split())
        output_concepts = set(output_lower.split())

        matched = expected_concepts.intersection(output_concepts)
        score = len(matched) / len(expected_concepts) if expected_concepts else 0.0

        return {
            "name": "factual_accuracy",
            "score": score,
            "metadata": {
                "matched_concepts": list(matched),
                "total_concepts": len(expected_concepts)
            }
        }

    # Test the scorers
    test_output = "Machine learning is a subset of artificial intelligence that learns patterns from data."
    test_expected = {
        "input": "What is machine learning?",
        "expected": "Machine learning is AI that learns from data"
    }

    relevance = relevance_scorer(test_output, test_expected)
    completeness = completeness_scorer(test_output, test_expected)
    accuracy = factual_accuracy_scorer(test_output, test_expected)

    print("✓ Custom scoring results:")
    print(f"  Relevance: {relevance['score']:.2f}")
    print(f"  Completeness: {completeness['score']:.2f}")
    print(f"  Factual Accuracy: {accuracy['score']:.2f}")
    print("\nAll scores tracked with metadata in Braintrust")

    return {
        "relevance": relevance,
        "completeness": completeness,
        "factual_accuracy": accuracy
    }


def prompt_comparison_example():
    """
    Compare different prompt versions.
    A/B test prompts to find best performer.
    """
    print("\n=== Prompt Comparison Example ===")

    # Define prompt variants
    prompts = {
        "basic": "Answer the question: {question}",
        "detailed": "You are a knowledgeable AI assistant. Provide a clear and accurate answer to the following question: {question}",
        "concise": "Provide a brief, accurate answer: {question}",
        "expert": "As an expert, provide a comprehensive answer with key concepts: {question}"
    }

    @traced
    def generate_with_prompt(question: str, prompt_template: str, variant_name: str) -> Dict[str, Any]:
        """Generate answer using specific prompt variant."""
        prompt = prompt_template.format(question=question)

        # Simulate different quality based on prompt
        quality_scores = {
            "basic": 0.70,
            "detailed": 0.85,
            "concise": 0.75,
            "expert": 0.90
        }

        answer = f"Answer generated using {variant_name} prompt template."
        quality = quality_scores[variant_name]

        # Log to current span
        span = current_span()
        if span:
            span.log(
                metadata={
                    "prompt_variant": variant_name,
                    "prompt_length": len(prompt),
                    "simulated_quality": quality
                }
            )

        return {
            "answer": answer,
            "variant": variant_name,
            "quality": quality
        }

    # Compare prompt variants
    test_question = "What is the difference between AI and ML?"
    results = []

    print("\nComparing prompt variants:")
    for variant, template in prompts.items():
        result = generate_with_prompt(test_question, template, variant)
        results.append(result)
        print(f"  {variant}: quality={result['quality']:.2f}")

    best_variant = max(results, key=lambda x: x['quality'])

    print(f"\n✓ Prompt comparison completed:")
    print(f"  Variants tested: {len(prompts)}")
    print(f"  Best performer: {best_variant['variant']} ({best_variant['quality']:.2f})")
    print(f"  Full comparison in Braintrust UI")

    return results


def regression_detection_example():
    """
    Detect performance regressions.
    Compare current model against baseline.
    """
    print("\n=== Regression Detection Example ===")

    # Baseline performance (from previous run)
    baseline_scores = {
        "accuracy": 0.85,
        "relevance": 0.82,
        "completeness": 0.80
    }

    # Current performance (simulated)
    current_scores = {
        "accuracy": 0.83,  # Slight regression
        "relevance": 0.86,  # Improvement
        "completeness": 0.79  # Slight regression
    }

    print("Performance comparison:")
    print(f"\n{'Metric':<15} {'Baseline':<10} {'Current':<10} {'Change':<10} {'Status'}")
    print("-" * 55)

    regressions = []
    improvements = []

    for metric in baseline_scores.keys():
        baseline = baseline_scores[metric]
        current = current_scores[metric]
        change = current - baseline
        change_pct = (change / baseline) * 100

        status = "🟢 OK" if change >= -0.02 else "🔴 REGRESSION"

        if change < -0.02:
            regressions.append(metric)
        elif change > 0.02:
            improvements.append(metric)

        print(f"{metric:<15} {baseline:<10.2f} {current:<10.2f} {change:+.2f} ({change_pct:+.1f}%)  {status}")

    print(f"\n✓ Regression detection:")
    print(f"  Metrics tracked: {len(baseline_scores)}")
    print(f"  Regressions: {len(regressions)} {regressions if regressions else ''}")
    print(f"  Improvements: {len(improvements)} {improvements if improvements else ''}")
    print(f"  Braintrust automatically tracks changes between runs")

    return {
        "baseline": baseline_scores,
        "current": current_scores,
        "regressions": regressions,
        "improvements": improvements
    }


def real_time_evaluation_example():
    """
    Real-time evaluation during model inference.
    Evaluate production traffic on-the-fly.
    """
    print("\n=== Real-Time Evaluation Example ===")

    logger = setup_braintrust()

    @traced
    def production_qa_system(question: str) -> Dict[str, Any]:
        """Production Q&A system with real-time evaluation."""
        start_time = time.time()

        # Simulate model inference
        answer = f"Generated answer for: {question}"

        # Calculate latency
        latency = time.time() - start_time

        # Real-time scoring
        quality_score = 0.85  # In production, use actual scoring
        relevance_score = 0.90

        # Log metrics
        span = current_span()
        if span:
            span.log(
                scores={
                    "quality": quality_score,
                    "relevance": relevance_score
                },
                metadata={
                    "latency_ms": latency * 1000,
                    "model": "gpt-4",
                    "environment": "production"
                }
            )

        return {
            "answer": answer,
            "quality": quality_score,
            "relevance": relevance_score,
            "latency_ms": latency * 1000
        }

    # Simulate production requests
    requests = [
        "What is climate change?",
        "How does blockchain work?",
        "Explain neural networks"
    ]

    print("\nSimulating production traffic:")
    for i, question in enumerate(requests, 1):
        result = production_qa_system(question)
        print(f"  Request {i}: quality={result['quality']:.2f}, latency={result['latency_ms']:.1f}ms")

    print(f"\n✓ Real-time evaluation:")
    print(f"  Requests processed: {len(requests)}")
    print(f"  All metrics logged in real-time")
    print(f"  Monitor live in Braintrust dashboard")

    return requests


def ci_cd_integration_example():
    """
    CI/CD integration for automated testing.
    Run evals in your deployment pipeline.
    """
    print("\n=== CI/CD Integration Example ===")

    print("CI/CD Integration Setup:\n")

    print("1. GitHub Actions Example:")
    print("""
    name: Evaluate Model
    on: [push]
    jobs:
      evaluate:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - name: Run Braintrust Eval
            env:
              BRAINTRUST_API_KEY: ${{ secrets.BRAINTRUST_API_KEY }}
            run: |
              pip install braintrust
              python run_evaluation.py
    """)

    print("\n2. Evaluation Script (run_evaluation.py):")
    print("""
    from braintrust import Eval

    result = Eval(
        "CI Evaluation",
        data=load_test_data(),
        task=lambda x: model.predict(x["input"]),
        scores=[accuracy_scorer, quality_scorer]
    )

    # Fail CI if scores below threshold
    if result.summary["accuracy"] < 0.85:
        raise Exception("Model accuracy below threshold")
    """)

    print("\n✓ CI/CD Integration benefits:")
    print("  • Automatic evaluation on every commit")
    print("  • Block deployments on regressions")
    print("  • Track model performance over time")
    print("  • Team visibility into changes")
    print("  • Reproducible evaluation runs")

    return True


def automatic_versioning_example():
    """
    Automatic versioning of models and experiments.
    Track every change automatically.
    """
    print("\n=== Automatic Versioning Example ===")

    @traced
    def model_v1(question: str) -> str:
        """Model version 1."""
        return "Basic answer from v1"

    @traced
    def model_v2(question: str) -> str:
        """Model version 2 - improved."""
        return "Improved answer from v2 with more detail"

    @traced
    def model_v3(question: str) -> str:
        """Model version 3 - optimized."""
        return "Optimized answer from v3 with best practices"

    versions = [
        ("v1", model_v1),
        ("v2", model_v2),
        ("v3", model_v3)
    ]

    print("Testing model versions:")
    test_question = "What is machine learning?"

    for version_name, model_func in versions:
        answer = model_func(test_question)
        print(f"  {version_name}: {answer[:50]}...")

    print(f"\n✓ Automatic versioning:")
    print(f"  Versions tracked: {len(versions)}")
    print(f"  Each version automatically logged")
    print(f"  Compare versions in Braintrust UI")
    print(f"  Git commit info automatically captured")
    print(f"  Rollback to any version anytime")

    return versions


def experiment_comparison():
    """
    Compare multiple experiments side-by-side.
    Find best configuration for your use case.
    """
    print("\n=== Experiment Comparison Example ===")

    def run_experiment(config: Dict[str, Any]) -> Dict[str, Any]:
        """Run experiment with specific configuration."""
        # Simulate experiment results
        base_score = 0.75
        temp_boost = config["temperature"] * 0.1
        token_penalty = (config["max_tokens"] - 100) / 1000

        score = base_score + temp_boost - token_penalty

        return {
            "config": config,
            "accuracy": min(score, 0.95),
            "latency_ms": config["max_tokens"] * 2,  # Simulated
            "cost_per_1k": 0.03 * (config["max_tokens"] / 100)
        }

    # Different experiment configurations
    experiments = [
        {"name": "baseline", "temperature": 0.7, "max_tokens": 100},
        {"name": "creative", "temperature": 0.9, "max_tokens": 150},
        {"name": "precise", "temperature": 0.3, "max_tokens": 100},
        {"name": "verbose", "temperature": 0.7, "max_tokens": 200}
    ]

    print("\nExperiment Results:")
    print(f"{'Name':<12} {'Accuracy':<10} {'Latency':<12} {'Cost'}")
    print("-" * 50)

    results = []
    for exp in experiments:
        result = run_experiment(exp)
        results.append(result)

        print(f"{exp['name']:<12} {result['accuracy']:<10.2f} {result['latency_ms']:<12.0f} ${result['cost_per_1k']:.4f}")

    # Find best by accuracy
    best = max(results, key=lambda x: x['accuracy'])

    print(f"\n✓ Experiment comparison:")
    print(f"  Experiments run: {len(experiments)}")
    print(f"  Best accuracy: {best['config']['name']} ({best['accuracy']:.2f})")
    print(f"  Full comparison in Braintrust dashboard")

    return results


def main():
    """Run all Braintrust examples."""
    print("=" * 60)
    print("Braintrust Evaluation Examples")
    print("=" * 60)

    try:
        # Initialize
        setup_braintrust()

        # Basic evaluation
        basic_evaluation_example()
        dataset_management_example()

        # Scoring
        custom_scoring_example()

        # Advanced features
        prompt_comparison_example()
        regression_detection_example()
        real_time_evaluation_example()

        # Integration
        ci_cd_integration_example()
        automatic_versioning_example()
        experiment_comparison()

        print("\n" + "=" * 60)
        print("All Braintrust examples completed successfully!")
        print("=" * 60)

        print("\n📊 Braintrust Key Features:")
        print("  • Automatic Versioning: Track every change automatically")
        print("  • Dataset Management: Organized, reusable test sets")
        print("  • Custom Scoring: Build any evaluation metric")
        print("  • Prompt Comparison: A/B test prompt variants")
        print("  • Regression Detection: Catch performance drops")
        print("  • Real-time Evaluation: Evaluate production traffic")
        print("  • CI/CD Integration: Automate evaluations in pipeline")
        print("  • Experiment Tracking: Compare configurations")
        print("  • Beautiful UI: Intuitive dashboard and visualizations")
        print("  • Excellent DX: Developer-friendly API")

        print("\n💡 Braintrust Use Cases:")
        print("  • Continuous model evaluation")
        print("  • Prompt engineering and optimization")
        print("  • A/B testing different configurations")
        print("  • Regression testing before deployment")
        print("  • Production monitoring and alerting")
        print("  • Dataset management and versioning")
        print("  • Team collaboration on evaluations")
        print("  • Historical performance tracking")

        print("\n🚀 Getting Started:")
        print("  1. Sign up: https://www.braintrust.dev/")
        print("  2. Get API key from dashboard")
        print("  3. Install: pip install braintrust")
        print("  4. Set key: export BRAINTRUST_API_KEY='your-key'")
        print("  5. Run evaluations with Eval()")

        print("\n🎯 Why Braintrust:")
        print("  • Best-in-class developer experience")
        print("  • Automatic versioning (no manual tracking)")
        print("  • Fast iteration on prompts and models")
        print("  • Production-ready with CI/CD support")
        print("  • Beautiful, intuitive UI")
        print("  • Strong community and documentation")

    except Exception as e:
        print(f"\nNote: {e}")
        print("\nSetup required:")
        print("  1. Sign up at https://www.braintrust.dev/")
        print("  2. Get API key from dashboard")
        print("  3. Install: pip install braintrust")
        print("  4. Set environment variable:")
        print("     export BRAINTRUST_API_KEY='your-api-key'")
        print("\nThese examples demonstrate Braintrust's capabilities.")


if __name__ == "__main__":
    main()
