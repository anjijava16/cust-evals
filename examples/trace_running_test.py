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

# Enable tracing + metrics using gRPC (recommended for Phoenix)
initialize_tracing(
    phoenix_endpoint="http://localhost:4317",  # Phoenix gRPC endpoint
    metrics_enabled=True,
    protocol="grpc"  # Use gRPC for full Phoenix support
)

# Use evaluators normally
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

# Metrics automatically recorded!
score = evaluator.evaluate({
    "input": "What is AI?",
    "output": "AI is artificial intelligence.",
    "context": "AI stands for artificial intelligence."
})
print(f"Score: {score.score}, Label: {score.label}")

# IMPORTANT: Shutdown tracing to flush all data to Phoenix
print("\nFlushing traces and metrics to Phoenix...")
shutdown_tracing()
print("✓ Done! Check Phoenix UI: http://localhost:6006/projects")