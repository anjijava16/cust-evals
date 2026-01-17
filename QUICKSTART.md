# Quick Start Guide

## Installation

```bash
cd cust-evals
pip install -e .
```

## Run Examples

```bash
# Run all examples
python examples/basic_usage.py

# Run tests (requires pytest)
pip install pytest
pytest tests/ -v
```

## Usage Examples

### 1. Exact Match Evaluation

```python
from custom.evals import exact_match

# Basic usage
eval_input = {"output": "Paris", "expected": "Paris"}
score = exact_match(eval_input)
print(f"Score: {score.score}")  # 1.0
print(f"Label: {score.label}")  # "match"

# With field mapping
eval_input = {"prediction": "Tokyo", "ground_truth": "Tokyo"}
field_mapping = {"output": "prediction", "expected": "ground_truth"}
score = exact_match(eval_input, field_mapping=field_mapping)
```

### 2. Sentiment Analysis

```python
from custom.evals import sentiment_score

eval_input = {"text": "I love this product! It's amazing!"}
score = sentiment_score(eval_input)
print(f"Score: {score.score}")     # 0.8 (high = positive)
print(f"Sentiment: {score.label}")  # "positive"
```

### 3. Custom Accuracy (with normalization)

```python
from custom.evals import custom_accuracy

# With normalization (default)
eval_input = {"output": " Paris ", "expected": "paris"}
score = custom_accuracy(eval_input)
print(f"Score: {score.score}")  # 1.0 (normalized match)

# Without normalization
score = custom_accuracy(eval_input, normalize=False)
print(f"Score: {score.score}")  # 0.0 (exact string doesn't match)
```

### 4. Batch Evaluation with Pandas

```python
import pandas as pd
from custom.evals import exact_match

# Create dataset
data = {
    "prediction": ["Paris", "London", "Tokyo", "Berlin"],
    "ground_truth": ["Paris", "Paris", "Tokyo", "Berlin"],
}
df = pd.DataFrame(data)

# Evaluate each row
scores = []
for _, row in df.iterrows():
    eval_input = {
        "output": row["prediction"],
        "expected": row["ground_truth"],
    }
    score = exact_match(eval_input)
    scores.append(score.score)

df["score"] = scores
print(f"Accuracy: {df['score'].mean():.2%}")  # 75.00%
```

### 5. Create Your Own Metric

```python
from custom.evals import Score, create_evaluator

@create_evaluator(name="length_check", kind="code")
def length_check(text: str, max_length: int) -> Score:
    """Check if text is within max length."""
    within_limit = len(text) <= max_length
    return Score(
        score=float(within_limit),
        label="valid" if within_limit else "too_long",
        explanation=f"Text has {len(text)} chars (max: {max_length})"
    )

# Use it
eval_input = {"text": "Hello", "max_length": 10}
score = length_check(eval_input)
print(score)
```

## Score Object

All evaluators return a `Score` object with:

- `score` (float): Numeric score value (typically 0.0 to 1.0)
- `name` (str): Metric name
- `label` (str, optional): Categorical label
- `explanation` (str, optional): Human-readable explanation
- `direction` (str): "maximize", "minimize", or "neutral"
- `kind` (str): "code", "llm", "human", or "heuristic"
- `metadata` (dict): Additional information

## Architecture Overview

```
cust-evals/
├── src/custom/evals/
│   ├── evaluators.py          # Base Score class and decorator
│   └── metrics/
│       ├── exact_match.py     # Binary comparison
│       ├── sentiment.py       # Sentiment analysis
│       └── accuracy.py        # Normalized accuracy
├── examples/
│   └── basic_usage.py         # Usage examples
└── tests/
    └── test_metrics.py        # Unit tests
```

## Key Features

1. **Decorator Pattern**: Easy metric creation with `@create_evaluator`
2. **Field Mapping**: Flexible input field remapping
3. **Standardized Scores**: All metrics return `Score` objects
4. **Metadata Support**: Store additional context with scores
5. **Extensible**: Simple to add new metrics

## Next Steps

- Add more metrics in `src/custom/evals/metrics/`
- Integrate with LLM providers (OpenAI, Anthropic) for LLM-based evaluation
- Add async support for batch evaluation
- Create visualization tools for evaluation results
