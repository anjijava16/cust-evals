# Contributing to Custom Evals

Guide for adding new evaluators and metrics to Custom Evals.

## Adding Code-Based Metrics

### Step 1: Create the Metric Function

```python
# src/custom/evals/metrics/my_metric.py

from typing import Optional
from ..evaluators import Score, create_evaluator

@create_evaluator(name="my_metric", kind="code", direction="maximize")
def my_metric(output: str, expected: Optional[str] = None) -> Score:
    """Your metric description.

    Args:
        output: The generated output
        expected: Optional ground truth

    Returns:
        Score object
    """
    # Your logic here
    is_correct = output == expected

    return Score(
        score=float(is_correct),
        label="correct" if is_correct else "incorrect",
        explanation=f"Output {'matches' if is_correct else 'does not match'} expected",
        metadata={"has_ground_truth": expected is not None}
    )
```

### Step 2: Export the Metric

```python
# src/custom/evals/__init__.py

from .metrics.my_metric import my_metric

__all__ = [
    # ... existing exports
    "my_metric",
]
```

### Step 3: Add Tests

```python
# tests/test_my_metric.py

from custom.evals import my_metric

def test_my_metric_correct():
    score = my_metric({"output": "A", "expected": "A"})
    assert score.score == 1.0
    assert score.label == "correct"

def test_my_metric_incorrect():
    score = my_metric({"output": "A", "expected": "B"})
    assert score.score == 0.0
    assert score.label == "incorrect"
```

### Step 4: Document

Add documentation to `docs/evaluators/code-based.md`.

## Adding LLM-Based Evaluators

### Step 1: Create the Evaluator Class

```python
# src/custom/evals/llm_evaluators.py

class MyEvaluator(LLMEvaluator):
    """Evaluator for [purpose].

    Example:
        >>> from custom.evals import MyEvaluator
        >>> from custom.evals.llm import LLM
        >>>
        >>> llm = LLM(provider="openai", model="gpt-4o-mini")
        >>> evaluator = MyEvaluator(llm)
        >>> score = evaluator.evaluate({"text": "..."})
    """

    NAME = "my_evaluator"
    DIRECTION = "maximize"  # or "minimize"
    REQUIRES_GROUND_TRUTH = False  # or True
    CHOICES = {
        "good": 1.0,
        "bad": 0.0,
    }
    PROMPT_TEMPLATE = """You are an expert evaluator.

    <text>
    {text}
    </text>

    Evaluate the text and respond with:
    - label: "good" or "bad"
    - explanation: Brief reasoning
    """

    def _check_ground_truth(self, eval_input: Dict[str, Any]) -> bool:
        """Override if needed."""
        return False  # Reference-free
```

### Step 2: Export the Evaluator

```python
# src/custom/evals/__init__.py

from .llm_evaluators import (
    # ... existing
    MyEvaluator,
)

__all__ = [
    # ... existing
    "MyEvaluator",
]
```

### Step 3: Add Tests

```python
# tests/test_my_evaluator.py

from custom.evals import MyEvaluator
from custom.evals.llm import LLM

def test_my_evaluator():
    llm = LLM(provider="openai", model="gpt-4o-mini")
    evaluator = MyEvaluator(llm)

    score = evaluator.evaluate({"text": "Good example"})
    assert score.name == "my_evaluator"
    assert score.label in ["good", "bad"]
```

### Step 4: Document

Add documentation to `docs/evaluators/llm-based.md` or `docs/evaluators/rag-specific.md`.

## Adding Examples

### Create Example File

```python
# examples/my_example.py

"""Example usage of MyEvaluator."""

from custom.evals import MyEvaluator
from custom.evals.llm import LLM

# Initialize
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = MyEvaluator(llm)

# Example 1: Good case
print("Example 1: Good case")
score = evaluator.evaluate({"text": "This is good"})
print(f"Result: {score.label} ({score.score})")

# Example 2: Bad case
print("\nExample 2: Bad case")
score = evaluator.evaluate({"text": "This is bad"})
print(f"Result: {score.label} ({score.score})")

# Example 3: Describe
print("\nExample 3: Describe")
description = evaluator.describe()
print(description)
```

### Update README

Add the example to `README.md`:

```markdown
## Running Examples

```bash
python examples/my_example.py
```
```

## Documentation Guidelines

### Code Documentation

Use clear docstrings:

```python
def my_function(arg1: str, arg2: int) -> Score:
    """One-line summary.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Score object with evaluation result

    Example:
        >>> score = my_function("test", 42)
        >>> print(score.label)
        "good"
    """
```

### Markdown Documentation

Follow this structure:

```markdown
# Title

Brief description.

## Usage

```python
# Code example
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `param1` | str | Yes | Description |

## Return Value

Description of return value.

## Examples

### Example 1: Basic Usage

```python
# Code
```

### Example 2: Advanced Usage

```python
# Code
```

## When to Use

✅ Good for:
- Use case 1
- Use case 2

❌ Not good for:
- Anti-pattern 1
- Anti-pattern 2
```

## Best Practices

### 1. Follow Existing Patterns

Look at existing evaluators for consistency:
- HallucinationEvaluator for LLM evaluators
- exact_match for code metrics

### 2. Add Type Hints

```python
from typing import Dict, Any, Optional

def my_function(
    eval_input: Dict[str, Any],
    option: Optional[str] = None
) -> Score:
    pass
```

### 3. Handle Errors Gracefully

```python
try:
    # Evaluation logic
    pass
except KeyError as e:
    return Score(
        score=0.0,
        label="error",
        explanation=f"Missing field: {e}"
    )
```

### 4. Support Field Mapping

Use the decorator for code metrics:

```python
@create_evaluator(name="my_metric")
def my_metric(output: str) -> Score:
    # Field mapping handled automatically
    pass
```

### 5. Test Thoroughly

Write tests for:
- Normal cases
- Edge cases
- Error cases
- With/without ground truth

## Adding to Documentation

### 1. Update docs/README.md

Add to the evaluator list.

### 2. Create Detailed Doc

Add to `docs/evaluators/` with full examples.

### 3. Update CHANGES_SUMMARY.md

Document your addition.

### 4. Update INDEX.md

Add navigation links.

## Questions?

- Check existing code for patterns
- Read the [Architecture](architecture.md) guide
- Look at [API Reference](api-reference.md)
- Review existing [Examples](examples.md)

## Ready to Contribute?

1. Create your evaluator
2. Add tests
3. Document it
4. Submit a pull request!
