"""Examples of LLM-based evaluation."""

import os

from custom.evals import CorrectnessEvaluator, HallucinationEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM


import os
import subprocess

command = "source ~/.zprofile && env"
proc = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    shell=True,
    executable="/bin/zsh"
)

for line in proc.stdout:
    key, _, value = line.decode().partition("=")
    os.environ[key] = value.strip()

def check_api_keys():
    """Check if API keys are available."""
    has_openai = "OPENAI_API_KEY" in os.environ
    has_anthropic = "ANTHROPIC_API_KEY" in os.environ

    if not (has_openai or has_anthropic):
        print("⚠️  No API keys found!")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
        print("\nExample:")
        print("  export OPENAI_API_KEY='your-key-here'")
        return None

    if has_openai:
        return ("openai", "gpt-4o-mini")
    elif has_anthropic:
        return ("anthropic", "claude-3-haiku-20240307")


def example_hallucination_evaluation():
    """Example: Hallucination detection."""
    print("=" * 70)
    print("Example 1: Hallucination Detection")
    print("=" * 70)

    provider_info = check_api_keys()
    if not provider_info:
        return

    provider, model = provider_info
    print(f"\nUsing: {provider} / {model}\n")

    # Initialize LLM and evaluator
    llm = LLM(provider=provider, model=model)
    print(f" LLM initialized: {llm.provider} / {llm.model} {llm.generate_text("wekcine")}\n")
    evaluator = HallucinationEvaluator(llm)

    # Test case 1: Factual response
    print("Test 1: Factual Response")
    print("-" * 70)
    eval_input = {
        "input": "What is the capital of France?",
        "output": "The capital of France is Paris.",
        "context": "Paris is the capital and largest city of France. It is located in the north-central part of the country."
    }
    print(f"Question: {eval_input['input']}")
    print(f"Response: {eval_input['output']}")
    print(f"Context: {eval_input['context'][:60]}...")

    score = evaluator.evaluate(eval_input)
    print(f"\n✓ Result: {score.label} (score: {score.score})")
    print(f"  Explanation: {score.explanation}")

    # Test case 2: Hallucinated response
    print("\n" + "=" * 70)
    print("Test 2: Hallucinated Response")
    print("-" * 70)
    eval_input = {
        "input": "What is the population of Paris?",
        "output": "The population of Paris is 50 million people.",
        "context": "Paris is the capital and largest city of France. It has beautiful architecture and museums."
    }
    print(f"Question: {eval_input['input']}")
    print(f"Response: {eval_input['output']}")
    print(f"Context: {eval_input['context']}")

    score = evaluator.evaluate(eval_input)
    print(f"\n✓ Result: {score.label} (score: {score.score})")
    print(f"  Explanation: {score.explanation}")


def example_correctness_evaluation():
    """Example: Correctness assessment."""
    print("\n" + "=" * 70)
    print("Example 2: Correctness Evaluation")
    print("=" * 70)

    provider_info = check_api_keys()
    if not provider_info:
        return

    provider, model = provider_info
    print(f"\nUsing: {provider} / {model}\n")

    # Initialize LLM and evaluator
    llm = LLM(provider=provider, model=model)
    evaluator = CorrectnessEvaluator(llm)

    test_cases = [
        {
            "input": "What is 2 + 2?",
            "output": "4",
            "expected": "4"
        },
        {
            "input": "What is the chemical symbol for water?",
            "output": "H2O",
            "expected": "H2O"
        },
        {
            "input": "What is 5 * 6?",
            "output": "25",
            "expected": "30"
        }
    ]

    for i, eval_input in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print("-" * 70)
        print(f"Question: {eval_input['input']}")
        print(f"Output: {eval_input['output']}")
        print(f"Expected: {eval_input['expected']}")

        score = evaluator.evaluate(eval_input)
        print(f"\n✓ Result: {score.label} (score: {score.score})")
        print(f"  Explanation: {score.explanation}")


def example_relevance_evaluation():
    """Example: Relevance assessment."""
    print("\n" + "=" * 70)
    print("Example 3: Relevance Evaluation")
    print("=" * 70)

    provider_info = check_api_keys()
    if not provider_info:
        return

    provider, model = provider_info
    print(f"\nUsing: {provider} / {model}\n")

    # Initialize LLM and evaluator
    llm = LLM(provider=provider, model=model)
    evaluator = RelevanceEvaluator(llm)

    test_cases = [
        {
            "name": "Relevant context",
            "input": "What programming language is Python?",
            "context": "Python is a high-level, interpreted programming language known for its simplicity and readability."
        },
        {
            "name": "Irrelevant context",
            "input": "What programming language is Python?",
            "context": "The Python is a family of nonvenomous snakes found in Africa, Asia, and Australia."
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 70)
        print(f"Question: {test_case['input']}")
        print(f"Context: {test_case['context'][:80]}...")

        eval_input = {
            "input": test_case["input"],
            "context": test_case["context"]
        }
        score = evaluator.evaluate(eval_input)
        print(f"\n✓ Result: {score.label} (score: {score.score})")
        print(f"  Explanation: {score.explanation}")


def example_batch_llm_evaluation():
    """Example: Batch evaluation with LLM."""
    print("\n" + "=" * 70)
    print("Example 4: Batch LLM Evaluation")
    print("=" * 70)

    provider_info = check_api_keys()
    if not provider_info:
        return

    provider, model = provider_info
    print(f"\nUsing: {provider} / {model}\n")

    try:
        import pandas as pd

        # Sample dataset
        data = {
            "question": [
                "What is 2+2?",
                "What is the capital of France?",
                "What is H2O?",
            ],
            "answer": [
                "4",
                "Paris",
                "Water",
            ],
            "reference": [
                "4",
                "Paris",
                "Water",
            ]
        }
        df = pd.DataFrame(data)

        print("Dataset:")
        print(df)
        print()

        # Initialize evaluator
        llm = LLM(provider=provider, model=model)
        evaluator = CorrectnessEvaluator(llm)

        # Evaluate each row
        scores = []
        labels = []
        explanations = []

        for idx, row in df.iterrows():
            print(f"Evaluating {idx + 1}/{len(df)}...", end="\r")
            eval_input = {
                "input": row["question"],
                "output": row["answer"],
                "expected": row["reference"]
            }
            score = evaluator.evaluate(eval_input)
            scores.append(score.score)
            labels.append(score.label)
            explanations.append(score.explanation)

        df["correctness_score"] = scores
        df["correctness_label"] = labels
        df["explanation"] = explanations

        print("\nResults:")
        print(df[["question", "answer", "correctness_label", "correctness_score"]])
        print(f"\nAccuracy: {df['correctness_score'].mean():.2%}")

    except ImportError:
        print("\n[pandas not installed - skipping batch evaluation example]")


if __name__ == "__main__":
    print("\n🚀 LLM-Based Evaluation Examples")
    print("=" * 70)

    example_hallucination_evaluation()
    example_correctness_evaluation()
    example_relevance_evaluation()
    example_batch_llm_evaluation()

    print("\n" + "=" * 70)
    print("✓ All examples completed!")
    print("=" * 70)
