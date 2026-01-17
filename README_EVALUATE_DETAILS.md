```markdown
# Evaluator Methods and Architecture

Complete guide to evaluator methods, patterns, and internal architecture.

## Table of Contents
1. [Evaluator Method Overview](#evaluator-method-overview)
2. [Method Descriptions](#method-descriptions)
3. [Usage Patterns](#usage-patterns)
4. [Async vs Sync](#async-vs-sync)
5. [Internal Architecture](#internal-architecture)
6. [Advanced Topics](#advanced-topics)

---

## Evaluator Method Overview

### Public API Methods

These are the methods you call as a user:

| Method | Type | Description | Returns |
|--------|------|-------------|---------|
| `evaluate(eval_input)` | Sync | Main evaluation method | `Score` |
| `async_evaluate(eval_input)` | Async | Async variant of evaluate | `Score` |
| `describe()` | Sync | Get evaluator metadata | `Dict[str, Any]` |

### Internal Methods

These are implementation details (prefix with `_`):

| Method | Type | Description | Override? |
|--------|------|-------------|-----------|
| `_evaluate(eval_input)` | Sync | Core evaluation logic | Optional |
| `_async_evaluate(eval_input)` | Async | Async evaluation logic | Optional |
| `_check_ground_truth(eval_input)` | Sync | Check if GT available | Optional |
| `_create_output_schema()` | Sync | Create LLM output schema | Rarely |

---

## Method Descriptions

### 1. evaluate()

**Primary synchronous evaluation method.**

```python
def evaluate(self, eval_input: Dict[str, Any]) -> Score:
    """Main evaluation method (synchronous).

    Args:
        eval_input: Dictionary with evaluation inputs

    Returns:
        Score with judgment
    """
```

**Example**:
```python
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

eval_input = {
    "input": "What is the capital?",
    "output": "Paris is the capital.",
    "context": "Paris is France's capital."
}

# Synchronous evaluation
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
```

**Workflow**:
1. Call `evaluate()` (public API)
2. Internally calls `_evaluate()` (implementation)
3. Returns `Score` object

---

### 2. async_evaluate()

**Primary asynchronous evaluation method.**

```python
async def async_evaluate(self, eval_input: Dict[str, Any]) -> Score:
    """Main evaluation method (asynchronous).

    Args:
        eval_input: Dictionary with evaluation inputs

    Returns:
        Score with judgment
    """
```

**Example**:
```python
import asyncio
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

async def evaluate_many(eval_inputs):
    llm = LLM(provider="openai", model="gpt-4o-mini")
    evaluator = HallucinationEvaluator(llm)

    # Evaluate concurrently
    tasks = [evaluator.async_evaluate(inp) for inp in eval_inputs]
    scores = await asyncio.gather(*tasks)

    return scores

# Run async evaluation
eval_inputs = [
    {"input": "Q1", "output": "A1", "context": "C1"},
    {"input": "Q2", "output": "A2", "context": "C2"},
]
scores = asyncio.run(evaluate_many(eval_inputs))
```

**Workflow**:
1. Call `async_evaluate()` (public async API)
2. Internally calls `_async_evaluate()` (async implementation)
3. By default, runs `_evaluate()` in thread pool
4. Returns `Score` object

---

### 3. describe()

**Get evaluator metadata and configuration.**

```python
def describe(self) -> Dict[str, Any]:
    """Return a description of this evaluator.

    Returns:
        Dictionary with evaluator metadata
    """
```

**Example**:
```python
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

# Get evaluator description
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

**Use Cases**:
- Documentation generation
- API introspection
- Debugging
- Configuration validation

---

### 4. _evaluate() (Internal)

**Core synchronous evaluation logic.**

```python
def _evaluate(self, eval_input: Dict[str, Any]) -> Score:
    """Internal evaluation logic (synchronous).

    This is where the actual evaluation happens.
    """
```

**Override Example**:
```python
class MyCustomEvaluator(LLMEvaluator):
    NAME = "custom"
    CHOICES = {"good": 1.0, "bad": 0.0}
    PROMPT_TEMPLATE = "Evaluate: {text}"

    def _evaluate(self, eval_input: Dict[str, Any]) -> Score:
        """Custom evaluation logic."""
        # Your custom implementation
        text = eval_input.get("text", "")

        # Custom logic here
        is_good = len(text) > 10

        return Score(
            score=1.0 if is_good else 0.0,
            name=self.name,
            label="good" if is_good else "bad",
            kind="llm",
            direction=self.direction
        )
```

---

### 5. _async_evaluate() (Internal)

**Core asynchronous evaluation logic.**

By default, runs `_evaluate()` in a thread pool. Override for true async:

```python
async def _async_evaluate(self, eval_input: Dict[str, Any]) -> Score:
    """Internal async evaluation logic."""
    # Default: Run sync version in thread pool
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, self._evaluate, eval_input)
```

**Override for True Async**:
```python
class MyAsyncEvaluator(LLMEvaluator):
    async def _async_evaluate(self, eval_input: Dict[str, Any]) -> Score:
        """True async implementation."""
        # Use async LLM methods
        prompt = self.PROMPT_TEMPLATE.format(**eval_input)
        schema = self._create_output_schema()

        # Assuming LLM has async methods (not in our POC yet)
        # response = await self.llm.async_generate_object(prompt, schema)

        # For now, we fall back to thread pool
        return await super()._async_evaluate(eval_input)
```

---

### 6. _check_ground_truth() (Internal)

**Check if ground truth data is available.**

```python
def _check_ground_truth(self, eval_input: Dict[str, Any]) -> bool:
    """Check if ground truth data is available."""
    ground_truth_fields = ["expected", "reference", "ground_truth", "target", "label"]
    return any(field in eval_input and eval_input[field] is not None
               for field in ground_truth_fields)
```

**Override Example**:
```python
class MyEvaluator(LLMEvaluator):
    def _check_ground_truth(self, eval_input: Dict[str, Any]) -> bool:
        """Custom ground truth check."""
        # Always consider reference-free
        return False

        # Or check specific fields
        return "my_custom_gt_field" in eval_input
```

---

## Usage Patterns

### Pattern 1: Simple Synchronous Evaluation

```python
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

score = evaluator.evaluate({
    "input": "Question?",
    "output": "Answer.",
    "context": "Context."
})

print(f"Result: {score.label} ({score.score})")
```

### Pattern 2: Batch Evaluation

```python
import pandas as pd

# Load dataset
df = pd.DataFrame({
    "question": ["Q1", "Q2", "Q3"],
    "answer": ["A1", "A2", "A3"],
    "context": ["C1", "C2", "C3"]
})

# Evaluate each row
scores = []
for _, row in df.iterrows():
    score = evaluator.evaluate({
        "input": row["question"],
        "output": row["answer"],
        "context": row["context"]
    })
    scores.append(score.score)

df["hallucination_score"] = scores
print(f"Average: {df['hallucination_score'].mean():.2f}")
```

### Pattern 3: Async Concurrent Evaluation

```python
import asyncio

async def evaluate_batch_async(evaluator, eval_inputs):
    """Evaluate multiple inputs concurrently."""
    tasks = [evaluator.async_evaluate(inp) for inp in eval_inputs]
    scores = await asyncio.gather(*tasks)
    return scores

# Usage
eval_inputs = [
    {"input": "Q1", "output": "A1", "context": "C1"},
    {"input": "Q2", "output": "A2", "context": "C2"},
    {"input": "Q3", "output": "A3", "context": "C3"},
]

scores = asyncio.run(evaluate_batch_async(evaluator, eval_inputs))
```

### Pattern 4: Conditional Evaluation

```python
def smart_evaluate(eval_input):
    """Choose evaluator based on available data."""
    results = {}

    # Always run reference-free evaluators
    if "context" in eval_input:
        hallucination_eval = HallucinationEvaluator(llm)
        results["hallucination"] = hallucination_eval.evaluate(eval_input)

    # Only run if ground truth available
    if "expected" in eval_input:
        correctness_eval = CorrectnessEvaluator(llm)
        results["correctness"] = correctness_eval.evaluate(eval_input)

    return results
```

### Pattern 5: Error Handling

```python
def safe_evaluate(evaluator, eval_input):
    """Evaluate with error handling."""
    try:
        score = evaluator.evaluate(eval_input)

        # Check for errors
        if score.label in ["no_ground_truth", "error"]:
            print(f"⚠️  Evaluation failed: {score.explanation}")
            return None

        return score

    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

# Usage
score = safe_evaluate(evaluator, eval_input)
if score:
    print(f"✓ Success: {score.label}")
```

---

## Async vs Sync

### When to Use Sync

- **Simple scripts**: Quick one-off evaluations
- **Sequential processing**: When order matters
- **Debugging**: Easier to debug and trace
- **Small datasets**: < 100 items

**Example**:
```python
# Sync - simple and straightforward
for item in dataset:
    score = evaluator.evaluate(item)
    print(score)
```

### When to Use Async

- **Large datasets**: > 100 items
- **API rate limits**: Concurrent requests with built-in backoff
- **Performance**: Need faster evaluation
- **Integration**: Using async frameworks (FastAPI, etc.)

**Example**:
```python
# Async - faster for large datasets
async def evaluate_all(items):
    tasks = [evaluator.async_evaluate(item) for item in items]
    return await asyncio.gather(*tasks)

scores = asyncio.run(evaluate_all(dataset))
```

### Performance Comparison

```python
import time
import asyncio

# Sync evaluation
start = time.time()
scores_sync = [evaluator.evaluate(item) for item in dataset]
sync_time = time.time() - start
print(f"Sync: {sync_time:.2f}s")

# Async evaluation
start = time.time()
scores_async = asyncio.run(asyncio.gather(*[
    evaluator.async_evaluate(item) for item in dataset
]))
async_time = time.time() - start
print(f"Async: {async_time:.2f}s")
print(f"Speedup: {sync_time / async_time:.1f}x")
```

---

## Internal Architecture

### Method Call Flow

```
User Code
   │
   ├─ evaluator.evaluate(input)
   │     │
   │     ├─ Validation
   │     ├─ Field mapping (if needed)
   │     │
   │     └─ self._evaluate(input)  ← Internal implementation
   │           │
   │           ├─ Check ground truth
   │           ├─ Render prompt
   │           ├─ Call LLM
   │           └─ Return Score
   │
   └─ score: Score object
```

### Async Method Call Flow

```
User Code
   │
   ├─ await evaluator.async_evaluate(input)
   │     │
   │     ├─ Validation
   │     ├─ Field mapping (if needed)
   │     │
   │     └─ await self._async_evaluate(input)
   │           │
   │           ├─ Run in thread pool (default)
   │           │   └─ self._evaluate(input)
   │           │
   │           └─ Return Score
   │
   └─ score: Score object
```

### Class Hierarchy

```
LLMEvaluator (Base)
   │
   ├─ evaluate()                  # Public API
   ├─ async_evaluate()            # Public async API
   ├─ describe()                  # Introspection
   │
   ├─ _evaluate()                 # Internal implementation
   ├─ _async_evaluate()           # Internal async implementation
   ├─ _check_ground_truth()       # Helper
   └─ _create_output_schema()     # Helper
```

---

## Advanced Topics

### Custom Evaluator Implementation

```python
from custom.evals.llm_evaluators import LLMEvaluator
from custom.evals import Score

class ToxicityEvaluator(LLMEvaluator):
    """Custom evaluator for detecting toxic content."""

    NAME = "toxicity"
    DIRECTION = "minimize"
    REQUIRES_GROUND_TRUTH = False
    CHOICES = {
        "toxic": 1.0,
        "non_toxic": 0.0,
    }
    PROMPT_TEMPLATE = """Evaluate if this text is toxic:

    <text>
    {text}
    </text>

    Is it toxic or non-toxic?"""

    def _check_ground_truth(self, eval_input):
        """Toxicity doesn't use ground truth."""
        return False

# Usage
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = ToxicityEvaluator(llm)

score = evaluator.evaluate({"text": "I hate you!"})
print(f"{score.label}: {score.score}")
```

### Batch Evaluation with Progress

```python
from tqdm import tqdm

def evaluate_with_progress(evaluator, eval_inputs):
    """Evaluate with progress bar."""
    scores = []
    for eval_input in tqdm(eval_inputs, desc="Evaluating"):
        score = evaluator.evaluate(eval_input)
        scores.append(score)
    return scores

# Usage
scores = evaluate_with_progress(evaluator, dataset)
```

### Caching Evaluations

```python
import json
import hashlib

class CachedEvaluator:
    """Wrapper to cache evaluation results."""

    def __init__(self, evaluator, cache_file="eval_cache.json"):
        self.evaluator = evaluator
        self.cache_file = cache_file
        self.cache = self._load_cache()

    def _load_cache(self):
        try:
            with open(self.cache_file) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f)

    def _cache_key(self, eval_input):
        """Generate cache key from input."""
        key_str = json.dumps(eval_input, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()

    def evaluate(self, eval_input):
        """Evaluate with caching."""
        key = self._cache_key(eval_input)

        if key in self.cache:
            print("Cache hit!")
            cached = self.cache[key]
            return Score(**cached)

        # Cache miss - evaluate
        score = self.evaluator.evaluate(eval_input)

        # Save to cache
        self.cache[key] = score.to_dict()
        self._save_cache()

        return score

# Usage
cached_eval = CachedEvaluator(evaluator)
score = cached_eval.evaluate(eval_input)  # Evaluates
score = cached_eval.evaluate(eval_input)  # Cache hit!
```

---

## Summary

### Key Takeaways

1. **Two-Layer API**: Public (`evaluate`) and internal (`_evaluate`)
2. **Sync and Async**: Both supported, async runs in thread pool by default
3. **Introspection**: Use `describe()` to get evaluator metadata
4. **Extensibility**: Override `_evaluate()` or `_check_ground_truth()` for custom behavior
5. **Ground Truth**: Handled automatically, evaluators declare requirements

### Method Cheat Sheet

| Want to... | Use... |
|-----------|--------|
| Evaluate one item | `evaluator.evaluate(input)` |
| Evaluate many items concurrently | `await evaluator.async_evaluate(input)` |
| Get evaluator info | `evaluator.describe()` |
| Customize evaluation | Override `_evaluate()` |
| Check ground truth | Override `_check_ground_truth()` |
| Add true async support | Override `_async_evaluate()` |

---

## References

- Main README: `README.md`
- LLM Guide: `LLM_GUIDE.md`
- Ground Truth Guide: `GROUND_TRUTH_GUIDE.md`
- Architecture: `ARCHITECTURE.md`

For more examples, see `examples/` directory.
```
