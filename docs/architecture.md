# Architecture

System architecture and design patterns of Custom Evals.

## Overview

Custom Evals is built with simplicity and extensibility in mind, following proven patterns from Phoenix Evals while adding flexibility for RAG evaluation.

## Component Architecture

```
Custom Evals
├── Core
│   ├── Score (dataclass)
│   └── create_evaluator (decorator)
├── Code-Based Metrics
│   ├── exact_match
│   ├── sentiment_score
│   └── custom_accuracy
├── LLM Infrastructure
│   ├── LLM (wrapper class)
│   └── LLMEvaluator (base class)
└── Evaluators
    ├── General
    │   ├── HallucinationEvaluator
    │   ├── CorrectnessEvaluator
    │   ├── RelevanceEvaluator
    │   └── CoherenceEvaluator
    └── RAG-Specific
        ├── FaithfulnessEvaluator
        └── AnswerRelevancyEvaluator
```

## Design Patterns

### 1. Two-Layer API Pattern

Public methods delegate to internal implementation:

```python
class LLMEvaluator:
    # Public API
    def evaluate(self, eval_input):
        return self._evaluate(eval_input)  # Delegates to internal

    # Internal implementation (can override)
    def _evaluate(self, eval_input):
        # Core logic here
        pass
```

**Benefits:**
- Clear public interface
- Easy to override internals
- Consistent behavior across evaluators

### 2. Decorator Pattern

Code-based metrics use decorators:

```python
@create_evaluator(name="my_metric", direction="maximize")
def my_metric(output: str, expected: str) -> Score:
    # Metric logic
    return Score(...)
```

**Benefits:**
- Minimal boilerplate
- Consistent Score return type
- Field mapping support built-in

### 3. Strategy Pattern

LLM provider abstraction:

```python
class LLM:
    def __init__(self, provider, model):
        if provider == "openai":
            self.client = OpenAI(...)
        elif provider == "anthropic":
            self.client = Anthropic(...)

    def generate_text(self, prompt):
        # Unified interface across providers
        pass
```

**Benefits:**
- Easy to add new providers
- Consistent interface
- Provider-agnostic evaluators

### 4. Template Method Pattern

Base class defines algorithm, subclasses provide specifics:

```python
class LLMEvaluator:
    def _evaluate(self, eval_input):
        # 1. Check ground truth (can override)
        has_gt = self._check_ground_truth(eval_input)

        # 2. Render prompt
        prompt = self.PROMPT_TEMPLATE.format(**eval_input)

        # 3. Get LLM response
        response = self.llm.generate_object(prompt, schema)

        # 4. Return Score
        return Score(...)
```

**Benefits:**
- Consistent evaluation flow
- Easy to customize specific steps
- Reusable common logic

## Data Flow

### Code-Based Metric Flow

```
User Input Dict
    ↓
Field Mapping (optional)
    ↓
Metric Function
    ↓
Score Object
```

### LLM Evaluator Flow

```
User Input Dict
    ↓
Ground Truth Check
    ↓
Prompt Rendering
    ↓
LLM API Call
    ↓
JSON Parsing
    ↓
Score Object
```

## Extensibility Points

### 1. Custom Code-Based Metric

```python
from custom.evals import create_evaluator, Score

@create_evaluator(name="my_metric")
def my_metric(output: str) -> Score:
    # Your logic
    return Score(score=1.0, label="good")
```

### 2. Custom LLM Evaluator

```python
from custom.evals.llm_evaluators import LLMEvaluator

class MyEvaluator(LLMEvaluator):
    NAME = "my_evaluator"
    CHOICES = {"good": 1.0, "bad": 0.0}
    PROMPT_TEMPLATE = "Evaluate: {text}"
```

### 3. Custom LLM Provider

Extend the LLM class:

```python
class LLM:
    def __init__(self, provider, model, **kwargs):
        if provider == "my_provider":
            self.client = MyProvider(...)
```

## Ground Truth Architecture

```python
class LLMEvaluator:
    def _check_ground_truth(self, eval_input):
        # Check multiple field names
        gt_fields = ["expected", "reference", "ground_truth", "target", "label"]
        return any(f in eval_input for f in gt_fields)

    def _evaluate(self, eval_input):
        has_gt = self._check_ground_truth(eval_input)

        if self.REQUIRES_GROUND_TRUTH and not has_gt:
            return Score(label="no_ground_truth", ...)

        # Continue evaluation
```

**Benefits:**
- Flexible field naming
- Clear GT requirements
- Graceful degradation

## Async Architecture

```python
class LLMEvaluator:
    async def async_evaluate(self, eval_input):
        return await self._async_evaluate(eval_input)

    async def _async_evaluate(self, eval_input):
        # Default: Run sync in thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._evaluate, eval_input)
```

**Benefits:**
- Async support without code duplication
- Easy batch evaluation
- Backwards compatible

## Performance Considerations

### Caching

LLM evaluations are expensive. Consider caching:

```python
import functools

@functools.lru_cache(maxsize=1000)
def cached_evaluate(input_hash):
    return evaluator.evaluate(input_dict)
```

### Batching

Use async for concurrent evaluation:

```python
scores = await asyncio.gather(*[
    evaluator.async_evaluate(inp) for inp in inputs
])
```

### Model Selection

- Development: Use cheaper models (gpt-4o-mini, claude-3-haiku)
- Production: Use better models (gpt-4o, claude-3-sonnet)

## For more details

See the main documentation:
- **[Architecture](../ARCHITECTURE.md)** - Complete architecture doc
- **[Project Overview](../PROJECT_OVERVIEW.md)** - Project structure
- **[API Reference](api-reference.md)** - API documentation
