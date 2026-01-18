from custom.evals import initialize_tracing, HallucinationEvaluator
from custom.evals.llm import LLM
import time
import os
import subprocess

# Load environment variables from zsh profile
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

print("=" * 80)
print("DEBUG TEST - Tracing + Metrics with Console Export")
print("=" * 80)

# Enable tracing + metrics + console export for debugging
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces",
    metrics_enabled=True,
    console_export=True,  # This will show traces/metrics in console
    metrics_export_interval=5000  # Export every 5 seconds instead of 30
)

print("\n✓ Tracing initialized with console export enabled")
print("  - Traces will be printed to console")
print("  - Metrics export every 5 seconds\n")

# Use evaluators normally
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

print("Running evaluation...")
score = evaluator.evaluate({
    "input": "What is AI?",
    "output": "AI is artificial intelligence.",
    "context": "AI stands for artificial intelligence."
})

print(f"\n✓ Evaluation completed:")
print(f"  - Score: {score.score}")
print(f"  - Label: {score.label}")
print(f"  - Explanation: {score.explanation}")

print("\n" + "=" * 80)
print("Waiting 10 seconds for metrics to be exported...")
print("=" * 80)
print("You should see console output above showing:")
print("  1. Trace spans being exported")
print("  2. Metrics being exported")
print("\nIf you don't see console output, there may be an issue with OpenTelemetry.")
print("=" * 80)

# Wait for metrics to be exported (export interval is 5 seconds)
time.sleep(10)

print("\n✓ Test complete! Check:")
print("  1. Console output above for traces/metrics")
print("  2. Phoenix UI: http://localhost:6006/projects")
