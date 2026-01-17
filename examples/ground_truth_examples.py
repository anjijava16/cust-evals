"""Examples showing evaluators with and without ground truth data."""

import os

from custom.evals import (
    CoherenceEvaluator,
    CorrectnessEvaluator,
    HallucinationEvaluator,
    RelevanceEvaluator,
    exact_match,
)
from custom.evals.llm import LLM


def check_api_keys():
    """Check if API keys are available."""
    has_openai = "OPENAI_API_KEY" in os.environ
    has_anthropic = "ANTHROPIC_API_KEY" in os.environ

    if not (has_openai or has_anthropic):
        print("⚠️  No API keys found!")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
        return None

    if has_openai:
        return ("openai", "gpt-4o-mini")
    elif has_anthropic:
        return ("anthropic", "claude-3-haiku-20240307")


def example_code_based_with_without_ground_truth():
    """Example: Code-based metrics with and without ground truth."""
    print("=" * 70)
    print("Example 1: Code-Based Metrics - Ground Truth Handling")
    print("=" * 70)

    # Test 1: WITH ground truth
    print("\nTest 1: WITH Ground Truth")
    print("-" * 70)
    eval_input = {"output": "Paris", "expected": "Paris"}
    score = exact_match(eval_input)
    print(f"Input: {eval_input}")
    print(f"Result: {score.label} (score: {score.score})")
    print(f"Explanation: {score.explanation}")
    print(f"Has ground truth: {score.metadata.get('has_ground_truth', False)}")

    # Test 2: WITHOUT ground truth
    print("\nTest 2: WITHOUT Ground Truth")
    print("-" * 70)
    eval_input = {"output": "Paris"}
    score = exact_match(eval_input)
    print(f"Input: {eval_input}")
    print(f"Result: {score.label} (score: {score.score})")
    print(f"Explanation: {score.explanation}")
    print(f"Has ground truth: {score.metadata.get('has_ground_truth', False)}")


def example_reference_free_evaluators():
    """Example: LLM evaluators that don't need ground truth."""
    print("\n" + "=" * 70)
    print("Example 2: Reference-Free LLM Evaluators")
    print("=" * 70)

    provider_info = check_api_keys()
    if not provider_info:
        return

    provider, model = provider_info
    print(f"\nUsing: {provider} / {model}")

    llm = LLM(provider=provider, model=model)

    # Test 1: Hallucination Detection (no ground truth needed)
    print("\n" + "-" * 70)
    print("Test 1: Hallucination Detection (Reference-Free)")
    print("-" * 70)
    evaluator = HallucinationEvaluator(llm)
    eval_input = {
        "input": "What is the capital of France?",
        "output": "Paris is the capital of France.",
        "context": "Paris is the capital and largest city of France."
    }
    print(f"Input: {eval_input['input']}")
    print(f"Output: {eval_input['output']}")
    print(f"Context: {eval_input['context'][:60]}...")
    print("\n⏳ Evaluating...")

    score = evaluator.evaluate(eval_input)
    print(f"✓ Result: {score.label} (score: {score.score})")
    print(f"  Explanation: {score.explanation}")
    print(f"  Has ground truth: {score.metadata.get('has_ground_truth', False)}")

    # Test 2: Relevance Evaluation (no ground truth needed)
    print("\n" + "-" * 70)
    print("Test 2: Relevance Evaluation (Reference-Free)")
    print("-" * 70)
    evaluator = RelevanceEvaluator(llm)
    eval_input = {
        "input": "What is Python?",
        "context": "Python is a high-level programming language known for its simplicity."
    }
    print(f"Question: {eval_input['input']}")
    print(f"Context: {eval_input['context']}")
    print("\n⏳ Evaluating...")

    score = evaluator.evaluate(eval_input)
    print(f"✓ Result: {score.label} (score: {score.score})")
    print(f"  Explanation: {score.explanation}")
    print(f"  Has ground truth: {score.metadata.get('has_ground_truth', False)}")

    # Test 3: Coherence Evaluation (no ground truth needed)
    print("\n" + "-" * 70)
    print("Test 3: Coherence Evaluation (Reference-Free)")
    print("-" * 70)
    evaluator = CoherenceEvaluator(llm)
    eval_input = {
        "output": "Paris is the capital of France. It has many famous museums like the Louvre. The Eiffel Tower is an iconic landmark."
    }
    print(f"Text: {eval_input['output'][:80]}...")
    print("\n⏳ Evaluating...")

    score = evaluator.evaluate(eval_input)
    print(f"✓ Result: {score.label} (score: {score.score})")
    print(f"  Explanation: {score.explanation}")
    print(f"  Has ground truth: {score.metadata.get('has_ground_truth', False)}")


def example_ground_truth_required_evaluators():
    """Example: LLM evaluators that require ground truth."""
    print("\n" + "=" * 70)
    print("Example 3: Ground Truth Required Evaluators")
    print("=" * 70)

    provider_info = check_api_keys()
    if not provider_info:
        return

    provider, model = provider_info
    print(f"\nUsing: {provider} / {model}")

    llm = LLM(provider=provider, model=model)
    evaluator = CorrectnessEvaluator(llm)

    # Test 1: WITH ground truth (works correctly)
    print("\n" + "-" * 70)
    print("Test 1: WITH Ground Truth (Correctness Evaluation)")
    print("-" * 70)
    eval_input = {
        "input": "What is 2 + 2?",
        "output": "4",
        "expected": "4"
    }
    print(f"Question: {eval_input['input']}")
    print(f"Output: {eval_input['output']}")
    print(f"Expected: {eval_input['expected']}")
    print("\n⏳ Evaluating...")

    score = evaluator.evaluate(eval_input)
    print(f"✓ Result: {score.label} (score: {score.score})")
    print(f"  Explanation: {score.explanation}")
    print(f"  Has ground truth: {score.metadata.get('has_ground_truth', False)}")

    # Test 2: WITHOUT ground truth (returns error)
    print("\n" + "-" * 70)
    print("Test 2: WITHOUT Ground Truth (Returns Error)")
    print("-" * 70)
    eval_input = {
        "input": "What is 2 + 2?",
        "output": "4"
        # No 'expected' field
    }
    print(f"Question: {eval_input['input']}")
    print(f"Output: {eval_input['output']}")
    print(f"Expected: <not provided>")
    print("\n⏳ Evaluating...")

    score = evaluator.evaluate(eval_input)
    print(f"✗ Result: {score.label} (score: {score.score})")
    print(f"  Explanation: {score.explanation}")
    print(f"  Has ground truth: {score.metadata.get('has_ground_truth', False)}")


def example_production_vs_testing():
    """Example: Production (no ground truth) vs Testing (with ground truth)."""
    print("\n" + "=" * 70)
    print("Example 4: Production vs Testing Scenarios")
    print("=" * 70)

    provider_info = check_api_keys()
    if not provider_info:
        return

    provider, model = provider_info
    print(f"\nUsing: {provider} / {model}")

    llm = LLM(provider=provider, model=model)

    print("\n" + "-" * 70)
    print("PRODUCTION MODE: No ground truth available")
    print("-" * 70)
    print("Use reference-free evaluators:")
    print("  ✓ HallucinationEvaluator")
    print("  ✓ RelevanceEvaluator")
    print("  ✓ CoherenceEvaluator")

    # Production example
    hallucination_eval = HallucinationEvaluator(llm)
    prod_input = {
        "input": "What is the weather like?",
        "output": "The weather is sunny with temperatures around 75°F.",
        "context": "Current weather: Sunny, 75°F, light breeze."
    }
    print(f"\nProduction Input: {prod_input['input']}")
    print(f"Response: {prod_input['output']}")
    print("⏳ Evaluating...")

    score = hallucination_eval.evaluate(prod_input)
    print(f"✓ Hallucination Check: {score.label} ({score.score})")

    print("\n" + "-" * 70)
    print("TESTING MODE: Ground truth available")
    print("-" * 70)
    print("Can use all evaluators:")
    print("  ✓ CorrectnessEvaluator (requires ground truth)")
    print("  ✓ HallucinationEvaluator")
    print("  ✓ RelevanceEvaluator")
    print("  ✓ exact_match")

    # Testing example
    correctness_eval = CorrectnessEvaluator(llm)
    test_input = {
        "input": "What is 5 * 6?",
        "output": "30",
        "expected": "30"
    }
    print(f"\nTest Input: {test_input['input']}")
    print(f"Response: {test_input['output']}")
    print(f"Ground Truth: {test_input['expected']}")
    print("⏳ Evaluating...")

    score = correctness_eval.evaluate(test_input)
    print(f"✓ Correctness Check: {score.label} ({score.score})")


def example_summary_table():
    """Summary table of evaluators and ground truth requirements."""
    print("\n" + "=" * 70)
    print("Summary: Evaluator Ground Truth Requirements")
    print("=" * 70)

    print("\n┌─────────────────────────────┬───────────────────┬─────────────┐")
    print("│ Evaluator                   │ Ground Truth Req? │ Type        │")
    print("├─────────────────────────────┼───────────────────┼─────────────┤")
    print("│ exact_match                 │ Optional          │ Code        │")
    print("│ sentiment_score             │ No                │ Code        │")
    print("│ custom_accuracy             │ Optional          │ Code        │")
    print("├─────────────────────────────┼───────────────────┼─────────────┤")
    print("│ HallucinationEvaluator      │ No                │ LLM         │")
    print("│ RelevanceEvaluator          │ No                │ LLM         │")
    print("│ CoherenceEvaluator          │ No                │ LLM         │")
    print("│ CorrectnessEvaluator        │ YES (Required)    │ LLM         │")
    print("└─────────────────────────────┴───────────────────┴─────────────┘")

    print("\n📝 Notes:")
    print("  • 'Optional' = Works with or without ground truth")
    print("  • 'No' = Reference-free, doesn't use ground truth")
    print("  • 'YES' = Requires ground truth to function")


if __name__ == "__main__":
    print("\n🎯 Ground Truth Handling Examples")
    print("=" * 70)

    example_code_based_with_without_ground_truth()
    example_reference_free_evaluators()
    example_ground_truth_required_evaluators()
    example_production_vs_testing()
    example_summary_table()

    print("\n" + "=" * 70)
    print("✓ All examples completed!")
    print("=" * 70)
