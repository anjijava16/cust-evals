# Code-Based Metrics

Code-based metrics are deterministic evaluators that run locally without requiring LLM API calls. They're fast, free, and perfect for basic validation.

## Overview

| Metric | Purpose | Ground Truth | Speed |
|--------|---------|--------------|-------|
| **exact_match** | Binary comparison | Optional | ⚡️ Instant |
| **sentiment_score** | Sentiment analysis | Not required | ⚡️ Instant |
| **custom_accuracy** | Flexible accuracy | Optional | ⚡️ Instant |

---

## exact_match

Binary comparison of output vs expected value.

### Usage

```python
from custom.evals import exact_match

# With ground truth
eval_input = {"output": "Paris", "expected": "Paris"}
score = exact_match(eval_input)
print(score.score)  # 1.0 (match)

# Without ground truth (returns error score)
eval_input = {"output": "Paris"}
score = exact_match(eval_input)
print(score.label)  # "no_ground_truth"
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `output` | str | Yes | The generated output to evaluate |
| `expected` | str | Optional | The expected/ground truth value |

### Return Value

```python
Score(
    score=1.0,              # 1.0 if match, 0.0 if no match
    name="exact_match",
    label="match" | "no_match" | "no_ground_truth",
    explanation="...",
    kind="code",
    direction="maximize",
    metadata={"has_ground_truth": True/False}
)
```

### When to Use

✅ **Good for:**
- Testing exact outputs (classification labels, short answers)
- Binary pass/fail evaluation
- Quick validation in unit tests

❌ **Not good for:**
- Long-form text (too strict)
- Semantic equivalence (doesn't understand meaning)
- Flexible matching

### Examples

```python
# Example 1: Classification label
eval_input = {"output": "positive", "expected": "positive"}
score = exact_match(eval_input)
# Score: 1.0, Label: "match"

# Example 2: Case sensitive
eval_input = {"output": "Paris", "expected": "paris"}
score = exact_match(eval_input)
# Score: 0.0, Label: "no_match"

# Example 3: With field mapping
eval_input = {"prediction": "Paris", "target": "Paris"}
score = exact_match(eval_input, field_mapping={
    "output": "prediction",
    "expected": "target"
})
# Score: 1.0, Label: "match"
```

---

## sentiment_score

Simple keyword-based sentiment analysis.

### Usage

```python
from custom.evals import sentiment_score

# Positive sentiment
eval_input = {"text": "I love this product! It's amazing!"}
score = sentiment_score(eval_input)
print(score.label)  # "positive"
print(score.score)  # 0.9

# Negative sentiment
eval_input = {"text": "I hate this. It's terrible."}
score = sentiment_score(eval_input)
print(score.label)  # "negative"
print(score.score)  # 0.1

# Neutral sentiment
eval_input = {"text": "This is a product."}
score = sentiment_score(eval_input)
print(score.label)  # "neutral"
print(score.score)  # 0.5
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | str | Yes | The text to analyze |

### Return Value

```python
Score(
    score=0.0-1.0,           # 0.0=negative, 0.5=neutral, 1.0=positive
    name="sentiment",
    label="positive" | "negative" | "neutral",
    explanation="Sentiment analysis based on keyword matching",
    kind="code",
    direction="neutral",
    metadata={}
)
```

### How It Works

Uses simple keyword matching:
- **Positive keywords**: love, great, excellent, amazing, wonderful, fantastic, good, best, happy
- **Negative keywords**: hate, terrible, awful, bad, worst, horrible, poor, disappointed

Score calculation:
- Positive: `0.5 + (0.5 * positive_words / total_words)`
- Negative: `0.5 - (0.5 * negative_words / total_words)`
- Neutral: `0.5` (no keywords found)

### When to Use

✅ **Good for:**
- Quick sentiment checks
- Simple feedback classification
- Prototyping

❌ **Not good for:**
- Nuanced sentiment (use LLM evaluators)
- Sarcasm or irony
- Context-dependent sentiment

### Examples

```python
# Example 1: Strong positive
eval_input = {"text": "This is amazing! I love it! Excellent work!"}
score = sentiment_score(eval_input)
# Score: ~0.9, Label: "positive"

# Example 2: Mixed sentiment (net positive)
eval_input = {"text": "It's good but has some bad aspects"}
score = sentiment_score(eval_input)
# Score: ~0.5-0.6, Label: "neutral" or "positive"

# Example 3: Field mapping
eval_input = {"output": "I love this!"}
score = sentiment_score(eval_input, field_mapping={"text": "output"})
# Score: ~0.9, Label: "positive"
```

---

## custom_accuracy

Flexible accuracy metric with optional text normalization.

### Usage

```python
from custom.evals import custom_accuracy

# Basic usage
eval_input = {"output": "Paris", "expected": "Paris"}
score = custom_accuracy(eval_input)
print(score.score)  # 1.0

# With normalization (case-insensitive, strip whitespace)
eval_input = {"output": " PARIS ", "expected": "paris"}
score = custom_accuracy(eval_input, normalize=True)
print(score.score)  # 1.0

# Without normalization
score = custom_accuracy(eval_input, normalize=False)
print(score.score)  # 0.0
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `output` | str | Yes | The generated output to evaluate |
| `expected` | str | Optional | The expected/ground truth value |
| `normalize` | bool | No (default: False) | Enable text normalization |

### Normalization

When `normalize=True`:
- Converts to lowercase
- Strips leading/trailing whitespace
- Removes extra spaces

```python
" PARIS " → "paris"
"New  York" → "new york"
```

### Return Value

```python
Score(
    score=1.0 | 0.0,
    name="accuracy",
    label="correct" | "incorrect" | "no_ground_truth",
    explanation="...",
    kind="code",
    direction="maximize",
    metadata={
        "has_ground_truth": True/False,
        "normalized": True/False
    }
)
```

### When to Use

✅ **Good for:**
- Case-insensitive matching
- Flexible short answer evaluation
- Testing with various formats

❌ **Not good for:**
- Semantic equivalence
- Long-form text
- Multi-word flexible matching

### Examples

```python
# Example 1: Case-insensitive
eval_input = {"output": "LONDON", "expected": "London"}
score = custom_accuracy(eval_input, normalize=True)
# Score: 1.0

# Example 2: Whitespace handling
eval_input = {"output": "  New York  ", "expected": "New York"}
score = custom_accuracy(eval_input, normalize=True)
# Score: 1.0

# Example 3: Without ground truth
eval_input = {"output": "Paris"}
score = custom_accuracy(eval_input)
# Score: 0.0, Label: "no_ground_truth"

# Example 4: Field mapping
eval_input = {"prediction": "Paris", "target": "paris"}
score = custom_accuracy(
    eval_input,
    field_mapping={"output": "prediction", "expected": "target"},
    normalize=True
)
# Score: 1.0
```

---

## Common Patterns

### Batch Evaluation

```python
import pandas as pd
from custom.evals import exact_match, custom_accuracy

# Load dataset
df = pd.DataFrame({
    "prediction": ["A", "B", "C"],
    "ground_truth": ["A", "B", "D"]
})

# Evaluate each row
scores = []
for _, row in df.iterrows():
    score = exact_match({
        "output": row["prediction"],
        "expected": row["ground_truth"]
    })
    scores.append(score.score)

df["score"] = scores
print(f"Accuracy: {df['score'].mean():.2f}")
```

### Combining Multiple Metrics

```python
from custom.evals import exact_match, sentiment_score, custom_accuracy

def evaluate_output(output, expected):
    """Evaluate output with multiple metrics."""
    results = {}

    # Exact match
    results["exact_match"] = exact_match({
        "output": output,
        "expected": expected
    }).score

    # Case-insensitive accuracy
    results["accuracy"] = custom_accuracy({
        "output": output,
        "expected": expected
    }, normalize=True).score

    # Sentiment (just for output)
    results["sentiment"] = sentiment_score({
        "text": output
    }).label

    return results

# Usage
results = evaluate_output("Paris", "paris")
print(results)
# {'exact_match': 0.0, 'accuracy': 1.0, 'sentiment': 'neutral'}
```

### Field Mapping

All code-based metrics support field mapping:

```python
# Your data format
eval_input = {
    "model_output": "Paris",
    "ground_truth_label": "Paris"
}

# Map to evaluator's expected fields
field_mapping = {
    "output": "model_output",
    "expected": "ground_truth_label"
}

score = exact_match(eval_input, field_mapping=field_mapping)
```

---

## Comparison

| Feature | exact_match | sentiment_score | custom_accuracy |
|---------|-------------|-----------------|-----------------|
| **Ground Truth** | Optional | Not needed | Optional |
| **Case Sensitive** | Yes | N/A | Configurable |
| **Normalization** | No | No | Yes |
| **Use Case** | Exact comparison | Sentiment analysis | Flexible matching |
| **Speed** | ⚡️ Instant | ⚡️ Instant | ⚡️ Instant |
| **Cost** | Free | Free | Free |

---

## Next Steps

- **[LLM-Based Evaluators](llm-based.md)** - For semantic evaluation
- **[RAG-Specific Evaluators](rag-specific.md)** - For RAG systems
- **[API Reference](../api-reference.md)** - Complete API docs
- **[Examples](../examples.md)** - More code examples
