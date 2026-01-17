# LLM-Based Evaluators

LLM-based evaluators use language models as judges to evaluate outputs. They're more flexible than code-based metrics and can understand semantic meaning, context, and nuance.

## Overview

| Evaluator | Purpose | Ground Truth | Provider Support |
|-----------|---------|--------------|------------------|
| **HallucinationEvaluator** | Detect hallucinations | Not required | OpenAI, Anthropic |
| **CorrectnessEvaluator** | Assess correctness | Required | OpenAI, Anthropic |
| **RelevanceEvaluator** | Evaluate relevance | Not required | OpenAI, Anthropic |
| **CoherenceEvaluator** | Check coherence | Not required | OpenAI, Anthropic |

All evaluators support both **sync** and **async** evaluation.

---

## HallucinationEvaluator

Detects whether a response contains hallucinated information based on provided context.

### Usage

```python
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

# Factual response
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France.",
    "context": "Paris is the capital and largest city of France."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: factual: The response accurately states...

# Hallucinated response
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital with 20 million people.",
    "context": "Paris is the capital of France."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: hallucinated: The population figure is not supported...
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input` | str | Yes | The input query/question |
| `output` | str | Yes | The response to evaluate |
| `context` | str | Yes | The context/grounding information |

### Configuration

```python
NAME = "hallucination"
DIRECTION = "minimize"  # Lower is better
REQUIRES_GROUND_TRUTH = False
CHOICES = {
    "factual": 0.0,        # Good: no hallucination
    "hallucinated": 1.0,   # Bad: contains hallucination
}
```

### Return Value

```python
Score(
    score=0.0 | 1.0,           # 0.0=factual, 1.0=hallucinated
    name="hallucination",
    label="factual" | "hallucinated",
    explanation="Detailed reasoning from LLM",
    kind="llm",
    direction="minimize",
    metadata={
        "model": "gpt-4o-mini",
        "has_ground_truth": False
    }
)
```

### When to Use

✅ **Good for:**
- RAG systems with retrieval context
- Fact-checking against provided information
- Detecting unsupported claims

❌ **Not good for:**
- Without context (use CorrectnessEvaluator instead)
- Real-time applications (has LLM latency)

---

## CorrectnessEvaluator

Assesses whether an output correctly answers the input question compared to an expected answer.

### Usage

```python
from custom.evals import CorrectnessEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CorrectnessEvaluator(llm)

# Correct answer
eval_input = {
    "input": "What is 2 + 2?",
    "output": "4",
    "expected": "4"
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.score}")
# Output: correct: 1.0

# Incorrect answer
eval_input = {
    "input": "What is 2 + 2?",
    "output": "5",
    "expected": "4"
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.score}")
# Output: incorrect: 0.0

# Missing ground truth
eval_input = {
    "input": "What is 2 + 2?",
    "output": "4"
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: no_ground_truth: correctness requires ground truth data
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input` | str | Yes | The input query/question |
| `output` | str | Yes | The response to evaluate |
| `expected` | str | Yes | The expected/correct answer |

**Note:** `expected` can also be named `reference`, `ground_truth`, `target`, or `label`.

### Configuration

```python
NAME = "correctness"
DIRECTION = "maximize"  # Higher is better
REQUIRES_GROUND_TRUTH = True  # Must have expected answer
CHOICES = {
    "correct": 1.0,      # Good: matches expected
    "incorrect": 0.0,    # Bad: doesn't match
}
```

### Return Value

```python
Score(
    score=1.0 | 0.0,           # 1.0=correct, 0.0=incorrect
    name="correctness",
    label="correct" | "incorrect" | "no_ground_truth",
    explanation="Detailed reasoning from LLM",
    kind="llm",
    direction="maximize",
    metadata={
        "model": "gpt-4o-mini",
        "has_ground_truth": True
    }
)
```

### When to Use

✅ **Good for:**
- Testing with known answers
- Semantic equivalence checking
- QA system evaluation

❌ **Not good for:**
- Production without ground truth
- Without expected answers

---

## RelevanceEvaluator

Evaluates whether provided context is relevant to the input question.

### Usage

```python
from custom.evals import RelevanceEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = RelevanceEvaluator(llm)

# Relevant context
eval_input = {
    "input": "What is Python?",
    "context": "Python is a high-level programming language."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: relevant: Context directly addresses Python programming

# Irrelevant context
eval_input = {
    "input": "What is Python?",
    "context": "The Eiffel Tower is in Paris."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: irrelevant: Context is about Paris, not Python
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input` | str | Yes | The input query/question |
| `context` | str | Yes | The context to evaluate |

### Configuration

```python
NAME = "relevance"
DIRECTION = "maximize"  # Higher is better
REQUIRES_GROUND_TRUTH = False
CHOICES = {
    "relevant": 1.0,     # Good: context is relevant
    "irrelevant": 0.0,   # Bad: context is not relevant
}
```

### When to Use

✅ **Good for:**
- RAG retrieval evaluation
- Context quality checking
- Search result relevance

❌ **Not good for:**
- Answer relevance (use AnswerRelevancyEvaluator)
- Without context

---

## CoherenceEvaluator

Assesses whether text is coherent and logically consistent.

### Usage

```python
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(llm)

# Coherent text
eval_input = {
    "output": "Paris is the capital of France. It's located on the Seine River."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: coherent: Text has logical flow...

# Incoherent text
eval_input = {
    "output": "Paris is blue. The cat runs fast. Tomorrow was yesterday."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: incoherent: Text lacks logical connection...
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `output` | str | Yes | The text to evaluate |

### Configuration

```python
NAME = "coherence"
DIRECTION = "maximize"  # Higher is better
REQUIRES_GROUND_TRUTH = False
CHOICES = {
    "coherent": 1.0,     # Good: text is logical
    "incoherent": 0.0,   # Bad: text is confusing
}
```

### When to Use

✅ **Good for:**
- Generated text quality
- Story/essay coherence
- Logical flow checking

❌ **Not good for:**
- Factual accuracy (use HallucinationEvaluator)
- Short text (< 2 sentences)

---

## Common Methods

All LLM evaluators share these methods:

### evaluate()

Synchronous evaluation:

```python
score = evaluator.evaluate(eval_input)
```

### async_evaluate()

Asynchronous evaluation:

```python
score = await evaluator.async_evaluate(eval_input)
```

### describe()

Get evaluator metadata:

```python
description = evaluator.describe()
print(description)
# {
#     'name': 'hallucination',
#     'kind': 'llm',
#     'direction': 'minimize',
#     'requires_ground_truth': False,
#     'choices': {'factual': 0.0, 'hallucinated': 1.0},
#     'model': 'gpt-4o-mini',
#     'provider': 'openai'
# }
```

---

## Async Batch Evaluation

Evaluate multiple inputs concurrently:

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

scores = asyncio.run(evaluate_batch())
print(f"Evaluated {len(scores)} inputs")
```

---

## Provider Configuration

### OpenAI

```python
from custom.evals.llm import LLM

llm = LLM(
    provider="openai",
    model="gpt-4o-mini",      # Fast and cheap
    # model="gpt-4o",         # More capable
    # model="gpt-4-turbo",    # Alternative
    api_key="sk-..."          # Optional if OPENAI_API_KEY is set
)
```

### Anthropic

```python
from custom.evals.llm import LLM

llm = LLM(
    provider="anthropic",
    model="claude-3-haiku-20240307",   # Fast and cheap
    # model="claude-3-sonnet-20240229", # Balanced
    # model="claude-3-opus-20240229",   # Most capable
    api_key="sk-ant-..."               # Optional if ANTHROPIC_API_KEY is set
)
```

---

## Comparison Table

| Evaluator | Ground Truth | Use Case | Speed | Cost |
|-----------|--------------|----------|-------|------|
| **Hallucination** | Not required | RAG fact-checking | ~1-2s | Low |
| **Correctness** | Required | QA with answers | ~1-2s | Low |
| **Relevance** | Not required | Context evaluation | ~1-2s | Low |
| **Coherence** | Not required | Text quality | ~1-2s | Low |

---

## Best Practices

### 1. Choose the Right Model

- **Development/Testing**: Use `gpt-4o-mini` or `claude-3-haiku` (fast, cheap)
- **Production**: Consider `gpt-4o` or `claude-3-sonnet` (more accurate)

### 2. Use Async for Batches

```python
# Don't do this (sequential)
scores = [evaluator.evaluate(inp) for inp in inputs]

# Do this instead (concurrent)
scores = await asyncio.gather(*[
    evaluator.async_evaluate(inp) for inp in inputs
])
```

### 3. Handle Errors

```python
try:
    score = evaluator.evaluate(eval_input)
    if score.label == "no_ground_truth":
        print("Warning: Missing ground truth")
except Exception as e:
    print(f"Evaluation failed: {e}")
```

### 4. Cache Results

LLM evaluation is expensive. Cache results when possible:

```python
import json

def cached_evaluate(evaluator, eval_input, cache_file="cache.json"):
    # Load cache
    try:
        with open(cache_file) as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = {}

    # Generate key
    key = json.dumps(eval_input, sort_keys=True)

    # Check cache
    if key in cache:
        return cache[key]

    # Evaluate
    score = evaluator.evaluate(eval_input)

    # Save to cache
    cache[key] = score.score
    with open(cache_file, "w") as f:
        json.dump(cache, f)

    return score
```

---

## Next Steps

- **[RAG-Specific Evaluators](rag-specific.md)** - For RAG systems
- **[LLM Integration](../llm-integration.md)** - LLM configuration
- **[API Reference](../api-reference.md)** - Complete API docs
- **[Examples](../examples.md)** - More examples
