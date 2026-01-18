"""Test tracing with console output to debug."""
from custom.evals import initialize_tracing, shutdown_tracing, HallucinationEvaluator
from custom.evals.llm import LLM
import os
import subprocess

# Load environment variables
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
print("Tracing Test with Console Export")
print("=" * 80)

# Enable tracing + metrics + console export
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces",
    metrics_enabled=True,
    console_export=True  # This will show what's being sent
)

print("\nRunning evaluation...")
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

score = evaluator.evaluate({
    "input": "What is AI?",
    "output": "AI is artificial intelligence.",
    "context": "AI stands for artificial intelligence."
})

print(f"\nScore: {score.score}, Label: {score.label}")
print("\n" + "=" * 80)
print("Shutting down and flushing to Phoenix...")
print("(Watch for console exports above)")
print("=" * 80)

shutdown_tracing()
print("\n✓ Done!")
