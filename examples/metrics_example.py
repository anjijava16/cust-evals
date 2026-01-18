"""Example usage of metrics with Phoenix (Arize).

This example demonstrates how to use OpenTelemetry metrics to collect
and export evaluation metrics to Phoenix for monitoring and analysis.

Prerequisites:
1. Install tracing dependencies: pip install -e ".[tracing]"
2. Start Phoenix locally:
   ```bash
   python -m phoenix.server.main serve
   ```
   Phoenix will run on http://localhost:6006

3. Set API key:
   export OPENAI_API_KEY="your-key"

What metrics are collected:
- evals.evaluations.total: Counter of total evaluations (by evaluator, label, model)
- evals.score: Histogram of evaluation scores (distribution)
- evals.latency.seconds: Histogram of evaluation latencies (distribution)
"""

import os
import time
from custom.evals import (
    initialize_tracing,
    HallucinationEvaluator,
    FaithfulnessEvaluator,
    AnswerRelevancyEvaluator,
)
from custom.evals.llm import LLM
from custom.evals.tracing import (
    record_counter,
    record_histogram,
    get_meter
)

print("=" * 80)
print("Custom Evals with Phoenix Metrics")
print("=" * 80)

# Step 1: Initialize tracing AND metrics
print("\n1. Initializing tracing and metrics...")
initialize_tracing(
    enabled=True,
    service_name="custom-evals-metrics-demo",
    phoenix_endpoint="http://localhost:6006/v1/traces",
    console_export=False,  # Set to True to see metrics in console
    metrics_enabled=True,  # Enable metrics collection
    metrics_export_interval=10000  # Export every 10 seconds (faster for demo)
)
print("✓ Tracing and metrics initialized")
print("  - Service: custom-evals-metrics-demo")
print("  - Phoenix: http://localhost:6006")
print("  - Metrics export interval: 10 seconds")
print("\nOpen http://localhost:6006 in your browser to see traces and metrics!")

# Step 2: Initialize LLM and evaluators
print("\n2. Initializing evaluators...")
llm = LLM(provider="openai", model="gpt-4o-mini")

hallucination_eval = HallucinationEvaluator(llm)
faithfulness_eval = FaithfulnessEvaluator(llm)
relevancy_eval = AnswerRelevancyEvaluator(llm)
print("✓ Evaluators ready")

# Step 3: Run evaluations (metrics will be automatically collected)
print("\n3. Running evaluations (metrics collected automatically)...")
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
    },
    {
        "name": "Another Faithful Response",
        "eval_input": {
            "input": "What is Python?",
            "output": "Python is a high-level programming language.",
            "context": "Python is a high-level programming language known for its simplicity."
        }
    },
    {
        "name": "Borderline Relevant",
        "eval_input": {
            "input": "How does photosynthesis work?",
            "output": "Plants use sunlight to create energy.",
            "context": "Photosynthesis converts light energy into chemical energy."
        }
    }
]

# Run evaluations multiple times to generate more metrics data
num_iterations = 2
print(f"\nRunning {num_iterations} iterations of {len(test_cases)} test cases...")
print(f"Total evaluations: {num_iterations * len(test_cases) * 3}")

for iteration in range(num_iterations):
    print(f"\n--- Iteration {iteration + 1}/{num_iterations} ---")

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test Case {i}: {test_case['name']}")

        # Run multiple evaluations (all automatically record metrics)
        if "context" in test_case["eval_input"]:
            # Hallucination evaluation
            hall_score = hallucination_eval.evaluate(test_case["eval_input"])
            print(f"    Hallucination: {hall_score.label} ({hall_score.score})")

            # Faithfulness evaluation
            faith_score = faithfulness_eval.evaluate(test_case["eval_input"])
            print(f"    Faithfulness: {faith_score.label} ({faith_score.score})")

        # Answer relevancy
        rel_score = relevancy_eval.evaluate({
            "input": test_case["eval_input"]["input"],
            "output": test_case["eval_input"]["output"]
        })
        print(f"    Answer Relevancy: {rel_score.label} ({rel_score.score})")

print("\n" + "=" * 80)
print("✓ Evaluations complete!")
print("=" * 80)

# Step 4: Custom metrics example
print("\n4. Custom metrics example...")
print("-" * 80)
print("Recording custom application metrics...")

# Example: Record custom counters
record_counter(
    "app.evaluations.batch_complete",
    value=1,
    attributes={"batch_size": len(test_cases) * num_iterations}
)

# Example: Record custom histogram
record_histogram(
    "app.batch_duration",
    value=15.5,
    attributes={"unit": "seconds"}
)

# Example: Using the meter directly for advanced metrics
meter = get_meter()
if meter:
    # Create a custom counter
    custom_counter = meter.create_counter(
        name="app.custom_events",
        description="Custom event counter",
        unit="1"
    )
    custom_counter.add(5, {"event_type": "demo"})

    # Create a custom histogram
    custom_histogram = meter.create_histogram(
        name="app.processing_time",
        description="Processing time histogram",
        unit="ms"
    )
    custom_histogram.record(250.5, {"operation": "batch_processing"})

    print("✓ Custom metrics recorded")
else:
    print("⚠ Metrics not available (disabled or OTel not installed)")

print("\n" + "=" * 80)
print("Metrics Collection Summary")
print("=" * 80)
print("\n📊 Automatic Metrics (recorded by evaluators):")
print("   1. evals.evaluations.total")
print("      - Type: Counter")
print("      - Description: Total number of evaluations")
print("      - Labels: evaluator, label, model, provider")
print("      - Use: Track evaluation volume over time")
print("")
print("   2. evals.score")
print("      - Type: Histogram")
print("      - Description: Distribution of evaluation scores")
print("      - Labels: evaluator, label, model, provider")
print("      - Use: Analyze score distributions, identify patterns")
print("")
print("   3. evals.latency.seconds")
print("      - Type: Histogram")
print("      - Description: Evaluation latency in seconds")
print("      - Labels: evaluator, label, model, provider")
print("      - Use: Monitor performance, identify slow evaluations")

print("\n📈 Custom Metrics (recorded manually):")
print("   1. app.evaluations.batch_complete")
print("   2. app.batch_duration")
print("   3. app.custom_events")
print("   4. app.processing_time")

print("\n" + "=" * 80)
print("🔍 View metrics in Phoenix:")
print("=" * 80)
print("   1. Open: http://localhost:6006")
print("   2. Navigate to the 'Metrics' or 'Monitoring' section")
print("   3. Filter by service: 'custom-evals-metrics-demo'")
print("")
print("You should see:")
print("   - Counter metrics: Total evaluations by evaluator type")
print("   - Histogram metrics: Score and latency distributions")
print("   - Time series graphs: Metrics over time")
print("   - Percentiles: P50, P95, P99 latencies")
print("   - Aggregations: By label, model, evaluator")

print("\n" + "=" * 80)
print("⏱  Waiting 15 seconds for metrics to export...")
print("=" * 80)
print("(Metrics export every 10 seconds)")

# Wait for metrics to export (metrics are exported periodically)
time.sleep(15)

print("\n✓ Metrics should now be visible in Phoenix!")
print("\n" + "=" * 80)
print("💡 Tips:")
print("=" * 80)
print("   - Metrics are aggregated over time windows")
print("   - Use labels/attributes to filter and group metrics")
print("   - Histograms show distributions (not just averages)")
print("   - Combine metrics with traces for full observability")
print("   - Set up alerts based on metric thresholds")
print("")
print("Example queries to try in Phoenix:")
print("   - Average score by evaluator")
print("   - P95 latency by model")
print("   - Evaluation rate (evals/second)")
print("   - Error rate (by label='error')")
print("   - Score distribution per evaluator")
print("\n" + "=" * 80)
