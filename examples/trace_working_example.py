"""Working example of tracing with Phoenix - FIXED VERSION"""
from custom.evals import initialize_tracing, shutdown_tracing, HallucinationEvaluator
from custom.evals.llm import LLM
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
print("Phoenix Tracing - Working Example")
print("=" * 80)

# Initialize tracing with correct settings
# - gRPC protocol (Phoenix default)
# - Port 4317 (not 6006 - that's for UI only)
# - Metrics disabled (Phoenix OTLP doesn't support metrics)
initialize_tracing(
    phoenix_endpoint="http://localhost:4317",
    metrics_enabled=False,  # Phoenix doesn't support OTLP metrics
    protocol="grpc"
)

print("\nRunning evaluation...")
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

# Run multiple evaluations to generate more trace data
test_cases = [
    {
        "input": "What is AI?",
        "output": "AI is artificial intelligence.",
        "context": "AI stands for artificial intelligence."
    },
    {
        
        "input": "What is the capital of France?",
        "output": "Paris is the capital of France.",
        "context": "Paris is the capital and largest city of France."
    },
    {
        "input": "What is Python?",
        "output": "Python is a high-level programming language.",
        "context": "Python is an interpreted, high-level programming language."
    }
]

print(f"\nRunning {len(test_cases)} evaluations...")
for i, test_case in enumerate(test_cases, 1):
    score = evaluator.evaluate(test_case)
    print(f"  {i}. Score: {score.score}, Label: {score.label}")

print("\n" + "=" * 80)
print("Flushing traces to Phoenix...")
print("(This ensures all traces are sent before the program exits)")
print("=" * 80)

# CRITICAL: Call shutdown_tracing() to flush all traces
shutdown_tracing()

print("\n✓ Done!")
print(f"\nView traces in Phoenix:")
print(f"  → http://localhost:6006/projects")
print(f"\nYou should see {len(test_cases)} evaluation traces with:")
print(f"  - Evaluator: hallucination")
print(f"  - Model: gpt-4o-mini")
print(f"  - Labels and scores")
