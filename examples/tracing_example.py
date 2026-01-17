"""Example usage of tracing with Phoenix (Arize).

This example shows how to use OpenTelemetry tracing to send
evaluation traces to Phoenix for observability.

Prerequisites:
1. Install tracing dependencies: pip install -e ".[tracing]"
2. Start Phoenix locally:
   ```bash
   python -m phoenix.server.main serve
   ```
   Phoenix will run on http://localhost:6006

3. Set API key:
   export OPENAI_API_KEY="your-key"
"""

import os
from custom.evals import (
    initialize_tracing,
    HallucinationEvaluator,
    FaithfulnessEvaluator,
    AnswerRelevancyEvaluator,
)
from custom.evals.llm import LLM

print("=" * 80)
print("Custom Evals with Phoenix Tracing")
print("=" * 80)

# Step 1: Initialize tracing
print("\n1. Initializing tracing...")
initialize_tracing(
    enabled=True,
    service_name="custom-evals-demo",
    phoenix_endpoint="http://localhost:6006/v1/traces",  # Phoenix collector endpoint
    console_export=False  # Set to True for console debugging
)
print("✓ Tracing initialized")
print("  - Service: custom-evals-demo")
print("  - Phoenix: http://localhost:6006")
print("\nOpen http://localhost:6006 in your browser to see traces!")

# Step 2: Initialize LLM and evaluators
print("\n2. Initializing evaluators...")
llm = LLM(provider="openai", model="gpt-4o-mini")

hallucination_eval = HallucinationEvaluator(llm)
faithfulness_eval = FaithfulnessEvaluator(llm)
relevancy_eval = AnswerRelevancyEvaluator(llm)
print("✓ Evaluators ready")

# Step 3: Run evaluations (will be traced)
print("\n3. Running evaluations (traces sent to Phoenix)...")
print("-" * 80)

test_cases = [
    {
        "name": "Faithful Response",
        "eval_input": {
            "input": "What is the capital of France?",
            "output": "Paris is the capital of France.",
            "context": "Paris is the capital and largest city of France."
        }
    },
    {
        "name": "Hallucinated Response",
        "eval_input": {
            "input": "What is the capital of France?",
            "output": "Paris is the capital with 20 million people.",
            "context": "Paris is the capital of France."
        }
    },
    {
        "name": "Relevant Answer",
        "eval_input": {
            "input": "What is machine learning?",
            "output": "Machine learning is a subset of AI that enables systems to learn from data.",
            "context": "Machine learning is a branch of artificial intelligence."
        }
    }
]

for i, test_case in enumerate(test_cases, 1):
    print(f"\nTest Case {i}: {test_case['name']}")

    # Run multiple evaluations (all traced)
    if "context" in test_case["eval_input"]:
        # Hallucination evaluation
        hall_score = hallucination_eval.evaluate(test_case["eval_input"])
        print(f"  Hallucination: {hall_score.label} ({hall_score.score})")

        # Faithfulness evaluation (RAG-specific)
        faith_score = faithfulness_eval.evaluate(test_case["eval_input"])
        print(f"  Faithfulness: {faith_score.label} ({faith_score.score})")

    # Answer relevancy (doesn't need context)
    rel_score = relevancy_eval.evaluate({
        "input": test_case["eval_input"]["input"],
        "output": test_case["eval_input"]["output"]
    })
    print(f"  Answer Relevancy: {rel_score.label} ({rel_score.score})")

# Step 4: Check Phoenix UI
print("\n" + "=" * 80)
print("✓ Evaluations complete!")
print("=" * 80)
print("\n🔍 View traces in Phoenix:")
print("   1. Open: http://localhost:6006")
print("   2. Click on 'Traces' tab")
print("   3. Filter by service: 'custom-evals-demo'")
print("\nYou should see:")
print("   - Each evaluation as a span")
print("   - Evaluator name, model, provider")
print("   - Input/output attributes")
print("   - Scores and labels")
print("   - Timing information")
print("\n" + "=" * 80)

# Example of custom tracing
print("\nBonus: Custom traced function example")
print("-" * 80)

from custom.evals import traced

@traced("custom_evaluation_pipeline")
def my_evaluation_pipeline(inputs):
    """Custom evaluation pipeline with tracing."""
    results = []
    for inp in inputs:
        score = hallucination_eval.evaluate(inp)
        results.append({
            "input": inp["input"],
            "label": score.label,
            "score": score.score
        })
    return results

# This function call will create a span in Phoenix
custom_inputs = [
    {
        "input": "What is Python?",
        "output": "Python is a programming language.",
        "context": "Python is a high-level programming language."
    }
]

results = my_evaluation_pipeline(custom_inputs)
print(f"✓ Custom pipeline traced: {len(results)} evaluations")
print(f"  Result: {results[0]['label']} ({results[0]['score']})")

print("\n" + "=" * 80)
print("Check Phoenix UI to see the custom pipeline span!")
print("=" * 80)
