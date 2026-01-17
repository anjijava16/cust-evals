# Ground Truth Handling

Guide to flexible ground truth support in Custom Evals.

## Overview

Custom Evals supports flexible ground truth handling:
- **Reference-Free**: Evaluators that don't need ground truth
- **Reference-Based**: Evaluators that require ground truth
- **Optional Ground Truth**: Evaluators that work both ways

## Evaluator Categories

### Reference-Free (No Ground Truth Needed)

These evaluators work without expected outputs:

| Evaluator | Use Case |
|-----------|----------|
| **HallucinationEvaluator** | Check against context |
| **RelevanceEvaluator** | Context-query relevance |
| **CoherenceEvaluator** | Text coherence |
| **FaithfulnessEvaluator** | RAG faithfulness |
| **AnswerRelevancyEvaluator** | Answer-query relevance |
| **sentiment_score** | Sentiment analysis |

```python
# No expected value needed
eval_input = {
    "input": "What is Python?",
    "output": "Python is a programming language.",
    "context": "Python is a high-level language."
}
score = hallucination_evaluator.evaluate(eval_input)
```

### Reference-Based (Ground Truth Required)

These evaluators require expected outputs:

| Evaluator | Use Case |
|-----------|----------|
| **CorrectnessEvaluator** | Compare to expected answer |

```python
# Expected value required
eval_input = {
    "input": "What is 2+2?",
    "output": "4",
    "expected": "4"  # Required
}
score = correctness_evaluator.evaluate(eval_input)
```

### Optional Ground Truth

These evaluators work with or without ground truth:

| Evaluator | Behavior |
|-----------|----------|
| **exact_match** | Returns error score if missing |
| **custom_accuracy** | Returns error score if missing |

```python
# With ground truth
score = exact_match({"output": "A", "expected": "A"})  # Works

# Without ground truth
score = exact_match({"output": "A"})  # Returns no_ground_truth score
```

## Supported Field Names

Multiple field names are recognized for ground truth:

- `expected`
- `reference`
- `ground_truth`
- `target`
- `label`

```python
# All of these work
eval_input = {"output": "A", "expected": "A"}
eval_input = {"output": "A", "reference": "A"}
eval_input = {"output": "A", "ground_truth": "A"}
eval_input = {"output": "A", "target": "A"}
eval_input = {"output": "A", "label": "A"}
```

## Production vs Testing

### Production (No Ground Truth)

Use reference-free evaluators:

```python
from custom.evals import HallucinationEvaluator, FaithfulnessEvaluator

# Evaluate production responses
score = hallucination_evaluator.evaluate({
    "input": user_query,
    "output": model_response,
    "context": retrieved_context
})
```

### Testing (With Ground Truth)

Use reference-based evaluators:

```python
from custom.evals import CorrectnessEvaluator, exact_match

# Evaluate against test set
score = correctness_evaluator.evaluate({
    "input": test_query,
    "output": model_response,
    "expected": test_answer
})
```

## Metadata Flag

All scores include `has_ground_truth` in metadata:

```python
score = evaluator.evaluate(eval_input)
print(score.metadata['has_ground_truth'])  # True or False
```

## For more details

See the main documentation:
- **[Ground Truth Guide](../GROUND_TRUTH_GUIDE.md)** - Complete ground truth guide
- **[Examples](../examples/ground_truth_examples.py)** - Working examples
