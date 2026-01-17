# Ground Truth Handling Guide

## Overview

Evaluators in this framework support **flexible ground truth handling**:

1. **Reference-Free Evaluators**: Don't need ground truth (e.g., hallucination detection, coherence)
2. **Reference-Based Evaluators**: Require ground truth (e.g., correctness, exact match)
3. **Optional Ground Truth**: Work with or without ground truth (e.g., exact_match)

This flexibility allows the same framework to work in:
- **Production**: Where ground truth is not available
- **Testing**: Where ground truth is available for validation

## Evaluator Categories

### 1. Reference-Free Evaluators (No Ground Truth Needed)

These evaluators assess quality without comparing to a reference answer.

| Evaluator | What It Checks | Use Case |
|-----------|---------------|----------|
| `HallucinationEvaluator` | Whether output is factual based on context | Production RAG systems |
| `RelevanceEvaluator` | Whether context is relevant to query | Document retrieval evaluation |
| `CoherenceEvaluator` | Whether text is logical and consistent | Content quality checks |
| `sentiment_score` | Sentiment of text | Content moderation |

**Example**:
```python
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

# No ground truth needed - evaluates against context
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital.",
    "context": "Paris is France's capital city."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# factual: The response is supported by the context
```

### 2. Reference-Based Evaluators (Ground Truth Required)

These evaluators compare the output against a known correct answer.

| Evaluator | What It Checks | Use Case |
|-----------|---------------|----------|
| `CorrectnessEvaluator` | Whether output matches expected answer | Testing with labeled data |

**Example**:
```python
from custom.evals import CorrectnessEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CorrectnessEvaluator(llm)

# WITH ground truth - works correctly
eval_input = {
    "input": "What is 2+2?",
    "output": "4",
    "expected": "4"  # Ground truth
}
score = evaluator.evaluate(eval_input)
print(f"{score.label} ({score.score})")
# correct (1.0)

# WITHOUT ground truth - returns error
eval_input = {
    "input": "What is 2+2?",
    "output": "4"
    # Missing 'expected' field
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# no_ground_truth: correctness requires ground truth data (expected value)
```

### 3. Optional Ground Truth Evaluators

These work with or without ground truth, but provide limited functionality without it.

| Evaluator | What It Checks | Behavior Without Ground Truth |
|-----------|---------------|------------------------------|
| `exact_match` | Binary string equality | Returns score of 0.0 with "no_ground_truth" label |
| `custom_accuracy` | String equality with normalization | Returns score of 0.0 with "no_ground_truth" label |

**Example**:
```python
from custom.evals import exact_match

# WITH ground truth
eval_input = {"output": "Paris", "expected": "Paris"}
score = exact_match(eval_input)
print(f"{score.label} ({score.score})")
# match (1.0)

# WITHOUT ground truth
eval_input = {"output": "Paris"}
score = exact_match(eval_input)
print(f"{score.label} ({score.score})")
# no_ground_truth (0.0)
```

## Production vs Testing Scenarios

### Production Mode (No Ground Truth)

In production, you typically don't have ground truth answers. Use reference-free evaluators:

```python
from custom.evals import HallucinationEvaluator, RelevanceEvaluator, CoherenceEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")

# Evaluate production responses
def evaluate_production_response(question, answer, context):
    results = {}

    # Check for hallucinations
    hallucination_eval = HallucinationEvaluator(llm)
    results['hallucination'] = hallucination_eval.evaluate({
        "input": question,
        "output": answer,
        "context": context
    })

    # Check context relevance
    relevance_eval = RelevanceEvaluator(llm)
    results['relevance'] = relevance_eval.evaluate({
        "input": question,
        "context": context
    })

    # Check answer coherence
    coherence_eval = CoherenceEvaluator(llm)
    results['coherence'] = coherence_eval.evaluate({
        "output": answer
    })

    return results

# Production usage
results = evaluate_production_response(
    question="What is the weather?",
    answer="It's sunny and 75 degrees.",
    context="Current conditions: Sunny, 75°F."
)

for metric, score in results.items():
    print(f"{metric}: {score.label} ({score.score})")
```

### Testing Mode (With Ground Truth)

In testing, you have labeled data with correct answers. Use all evaluators:

```python
from custom.evals import (
    CorrectnessEvaluator,
    HallucinationEvaluator,
    exact_match
)
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")

# Evaluate test dataset with ground truth
def evaluate_test_dataset(test_data):
    results = []

    correctness_eval = CorrectnessEvaluator(llm)
    hallucination_eval = HallucinationEvaluator(llm)

    for item in test_data:
        item_results = {}

        # Exact match (fast, deterministic)
        item_results['exact_match'] = exact_match({
            "output": item['output'],
            "expected": item['ground_truth']
        })

        # LLM-based correctness (semantic comparison)
        item_results['correctness'] = correctness_eval.evaluate({
            "input": item['question'],
            "output": item['output'],
            "expected": item['ground_truth']
        })

        # Hallucination check
        if 'context' in item:
            item_results['hallucination'] = hallucination_eval.evaluate({
                "input": item['question'],
                "output": item['output'],
                "context": item['context']
            })

        results.append(item_results)

    return results

# Test dataset with ground truth
test_data = [
    {
        "question": "What is 2+2?",
        "output": "4",
        "ground_truth": "4",
        "context": "Basic arithmetic: 2+2=4"
    },
    {
        "question": "Capital of France?",
        "output": "Paris",
        "ground_truth": "Paris",
        "context": "Paris is the capital of France."
    }
]

results = evaluate_test_dataset(test_data)
```

## Checking Ground Truth Availability

All LLM evaluators check for ground truth using the `_check_ground_truth` method:

```python
def _check_ground_truth(self, eval_input: Dict[str, Any]) -> bool:
    """Check if ground truth data is available."""
    ground_truth_fields = ["expected", "reference", "ground_truth", "target", "label"]
    return any(field in eval_input and eval_input[field] is not None
               for field in ground_truth_fields)
```

Supported ground truth field names:
- `expected`
- `reference`
- `ground_truth`
- `target`
- `label`

**Example**:
```python
# All these work - uses any recognized ground truth field
exact_match({"output": "A", "expected": "A"})
exact_match({"output": "A", "reference": "A"})
exact_match({"output": "A", "ground_truth": "A"})
exact_match({"output": "A", "target": "A"})
```

## Metadata: has_ground_truth Flag

All scores include a `has_ground_truth` flag in metadata:

```python
from custom.evals import exact_match

# With ground truth
score = exact_match({"output": "Paris", "expected": "Paris"})
print(score.metadata['has_ground_truth'])  # True

# Without ground truth
score = exact_match({"output": "Paris"})
print(score.metadata['has_ground_truth'])  # False
```

This helps in:
- Filtering results
- Understanding score reliability
- Debugging evaluation pipelines

## Best Practices

### 1. Choose the Right Evaluator

```python
# Production (no ground truth) - use reference-free
HallucinationEvaluator  # Check factuality against context
RelevanceEvaluator      # Check context relevance
CoherenceEvaluator      # Check text quality

# Testing (with ground truth) - use reference-based
CorrectnessEvaluator    # Semantic correctness comparison
exact_match             # Exact string matching
custom_accuracy         # Normalized string matching
```

### 2. Handle Missing Ground Truth Gracefully

```python
from custom.evals import CorrectnessEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CorrectnessEvaluator(llm)

def safe_evaluate(eval_input):
    score = evaluator.evaluate(eval_input)

    # Check if evaluation was successful
    if score.label == "no_ground_truth":
        print(f"⚠️  Skipping: {score.explanation}")
        return None

    return score

# This will skip gracefully
result = safe_evaluate({
    "input": "What is 2+2?",
    "output": "4"
    # Missing 'expected'
})
```

### 3. Batch Processing with Mixed Ground Truth

```python
import pandas as pd

def evaluate_dataset(df, evaluator):
    """Evaluate dataset, handling missing ground truth."""
    results = []

    for idx, row in df.iterrows():
        score = evaluator.evaluate(row.to_dict())

        results.append({
            'index': idx,
            'score': score.score,
            'label': score.label,
            'has_ground_truth': score.metadata.get('has_ground_truth', False)
        })

    return pd.DataFrame(results)

# Dataset with mixed ground truth availability
df = pd.DataFrame([
    {"output": "A", "expected": "A"},  # Has ground truth
    {"output": "B"},                    # No ground truth
    {"output": "C", "expected": "C"},  # Has ground truth
])

results = evaluate_dataset(df, exact_match)

# Filter to only items with ground truth
valid_results = results[results['has_ground_truth'] == True]
print(f"Accuracy: {valid_results['score'].mean():.2%}")
```

### 4. Conditional Evaluation Pipeline

```python
def smart_evaluate(eval_input):
    """Choose evaluators based on available data."""
    results = {}

    # Always run reference-free evaluators
    if 'context' in eval_input:
        results['hallucination'] = hallucination_eval.evaluate(eval_input)
        results['relevance'] = relevance_eval.evaluate(eval_input)

    # Only run reference-based if ground truth available
    if any(field in eval_input for field in ['expected', 'ground_truth']):
        results['correctness'] = correctness_eval.evaluate(eval_input)
        results['exact_match'] = exact_match(eval_input)

    return results
```

## Summary Table

| Evaluator | Ground Truth | Production | Testing | Returns Error if Missing GT |
|-----------|--------------|------------|---------|----------------------------|
| `HallucinationEvaluator` | Not needed | ✅ | ✅ | No |
| `RelevanceEvaluator` | Not needed | ✅ | ✅ | No |
| `CoherenceEvaluator` | Not needed | ✅ | ✅ | No |
| `sentiment_score` | Not needed | ✅ | ✅ | No |
| `CorrectnessEvaluator` | **Required** | ❌ | ✅ | Yes |
| `exact_match` | Optional | ⚠️ | ✅ | No (returns 0.0) |
| `custom_accuracy` | Optional | ⚠️ | ✅ | No (returns 0.0) |

Legend:
- ✅ Recommended
- ⚠️ Works but limited functionality
- ❌ Not applicable

## Examples

See `examples/ground_truth_examples.py` for complete working examples.

```bash
# Run ground truth examples (requires API key)
export OPENAI_API_KEY="your-key"
python examples/ground_truth_examples.py
```
