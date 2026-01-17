# Getting Started with Custom Evals

This guide will help you get started with Custom Evals in minutes.

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Basic Installation

```bash
cd cust-evals
pip install -e .
```

### With LLM Support

To use LLM-based evaluators, install with optional dependencies:

```bash
pip install -e ".[dev]"
```

This includes:
- `openai` - For OpenAI models (GPT-4, GPT-3.5)
- `anthropic` - For Anthropic models (Claude)

### With Phoenix Tracing (Optional)

**Tracing is completely optional.** The framework works perfectly without it.

If you want observability with Phoenix (Arize), install tracing dependencies:

```bash
pip install -e ".[dev,tracing]"
```

This adds:
- `opentelemetry-api` - OpenTelemetry API
- `opentelemetry-sdk` - OpenTelemetry SDK
- `opentelemetry-exporter-otlp` - OTLP exporter for Phoenix

See **[Phoenix Tracing Guide](../TRACING_GUIDE.md)** for setup and usage.

### Verify Installation

```python
from custom.evals import exact_match, Score
print("✓ Installation successful!")
```

---

## Quick Start

### 1. Code-Based Metrics (No API Keys Required)

Code-based metrics run locally and don't require any API keys.

```python
from custom.evals import exact_match, sentiment_score, custom_accuracy

# Example 1: Exact Match
eval_input = {"output": "Paris", "expected": "Paris"}
score = exact_match(eval_input)
print(f"Match: {score.score}")  # Output: 1.0

# Example 2: Sentiment Analysis
eval_input = {"text": "I love this product!"}
score = sentiment_score(eval_input)
print(f"Sentiment: {score.label}")  # Output: positive

# Example 3: Custom Accuracy with Normalization
eval_input = {"output": " PARIS ", "expected": "paris"}
score = custom_accuracy(eval_input, normalize=True)
print(f"Accuracy: {score.score}")  # Output: 1.0
```

### 2. LLM-Based Evaluators (Requires API Keys)

#### Set Up API Keys

Choose one provider:

**OpenAI:**
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

**Anthropic:**
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

#### Use LLM Evaluators

```python
from custom.evals import HallucinationEvaluator, CorrectnessEvaluator
from custom.evals.llm import LLM

# Initialize LLM
llm = LLM(provider="openai", model="gpt-4o-mini")

# Example 1: Hallucination Detection
evaluator = HallucinationEvaluator(llm)
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France.",
    "context": "Paris is the capital and largest city of France."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")

# Example 2: Correctness Evaluation
evaluator = CorrectnessEvaluator(llm)
eval_input = {
    "input": "What is 2 + 2?",
    "output": "4",
    "expected": "4"
}
score = evaluator.evaluate(eval_input)
print(f"Correct: {score.score}")  # Output: 1.0
```

### 3. RAG Evaluation (New!)

```python
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")

# Faithfulness: Is the response grounded in context?
faithfulness = FaithfulnessEvaluator(llm)
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France. It's located on the Seine River.",
    "context": "Paris is the capital and largest city of France, located on the Seine River."
}
score = faithfulness.evaluate(eval_input)
print(f"Faithful: {score.label}")  # Output: faithful

# Answer Relevancy: Does the answer address the query?
relevancy = AnswerRelevancyEvaluator(llm)
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France."
}
score = relevancy.evaluate(eval_input)
print(f"Relevant: {score.label}")  # Output: relevant
```

### 4. Phoenix Tracing (Optional)

**Tracing is completely optional.** The framework works end-to-end without it.

If you want to enable Phoenix tracing for observability:

```python
from custom.evals import initialize_tracing, HallucinationEvaluator
from custom.evals.llm import LLM

# Step 1: Initialize tracing (optional, only if you want observability)
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces"  # Your Phoenix endpoint
)

# Step 2: Use evaluators normally (now automatically traced!)
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France.",
    "context": "Paris is the capital of France."
}

score = evaluator.evaluate(eval_input)  # This is now traced in Phoenix UI!
print(f"{score.label}")
```

**Without tracing:** Just skip the `initialize_tracing()` call. Everything works the same!

See **[Phoenix Tracing Guide](../TRACING_GUIDE.md)** for complete documentation.

---

## Running Examples

We provide several working examples:

```bash
# Code-based metrics (no API key needed)
python examples/basic_usage.py

# LLM evaluators (requires API key)
export OPENAI_API_KEY="your-key"
python examples/llm_evaluation.py

# RAG evaluation (requires API key)
python examples/rag_evaluation.py

# Ground truth handling
python examples/ground_truth_examples.py

# Phoenix tracing (optional - requires tracing dependencies and Phoenix running)
pip install -e ".[dev,tracing]"
python -m phoenix.server.main serve  # In a separate terminal
python examples/tracing_example.py
```

---

## Understanding the Score Object

All evaluators return a `Score` object:

```python
@dataclass
class Score:
    score: float              # Numerical score (0.0 to 1.0)
    name: str                 # Evaluator name
    label: Optional[str]      # Classification label
    explanation: Optional[str] # Reasoning
    kind: str                 # "code", "llm", "human", "heuristic"
    direction: str            # "maximize", "minimize", "neutral"
    metadata: Dict[str, Any]  # Additional info
```

Example:
```python
score = exact_match({"output": "Paris", "expected": "Paris"})

print(score.score)        # 1.0
print(score.label)        # "match"
print(score.explanation)  # "Output matches expected value"
print(score.kind)         # "code"
print(score.direction)    # "maximize"
```

---

## Supported LLM Providers

### OpenAI

```python
from custom.evals.llm import LLM

llm = LLM(
    provider="openai",
    model="gpt-4o-mini",      # or "gpt-4o", "gpt-4-turbo"
    api_key="your-key"        # optional if OPENAI_API_KEY is set
)
```

### Anthropic

```python
from custom.evals.llm import LLM

llm = LLM(
    provider="anthropic",
    model="claude-3-haiku-20240307",  # or "claude-3-sonnet", "claude-3-opus"
    api_key="your-key"                # optional if ANTHROPIC_API_KEY is set
)
```

---

## Async Evaluation

For better performance with multiple evaluations:

```python
import asyncio
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

async def evaluate_batch():
    llm = LLM(provider="openai", model="gpt-4o-mini")
    evaluator = HallucinationEvaluator(llm)

    inputs = [
        {"input": "Q1", "output": "A1", "context": "C1"},
        {"input": "Q2", "output": "A2", "context": "C2"},
        {"input": "Q3", "output": "A3", "context": "C3"},
    ]

    # Evaluate concurrently
    tasks = [evaluator.async_evaluate(inp) for inp in inputs]
    scores = await asyncio.gather(*tasks)

    return scores

# Run
scores = asyncio.run(evaluate_batch())
```

---

## Next Steps

Now that you're set up, explore:

1. **[Examples](examples.md)** - More detailed examples
2. **[Code-Based Metrics](evaluators/code-based.md)** - Learn about code metrics
3. **[LLM-Based Evaluators](evaluators/llm-based.md)** - Learn about LLM evaluators
4. **[RAG-Specific Evaluators](evaluators/rag-specific.md)** - Learn about RAG evaluation
5. **[API Reference](api-reference.md)** - Complete API documentation

---

## Troubleshooting

### Import Errors

If you get import errors:
```bash
pip install -e ".[dev]"
```

### API Key Issues

Make sure your API key is set:
```bash
# Check if set
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# Set if needed
export OPENAI_API_KEY="your-key"
```

### Module Not Found

Make sure you're in the correct directory:
```bash
cd cust-evals
pip install -e .
```

---

**Ready for more?** → [Examples](examples.md) or [API Reference](api-reference.md)
