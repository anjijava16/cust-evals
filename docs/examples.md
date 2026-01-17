# Examples

Working code examples for Custom Evals.

## Running Examples

All examples are located in the `examples/` directory:

```bash
cd cust-evals

# Code-based metrics (no API key needed)
python examples/basic_usage.py

# LLM evaluators (requires API key)
export OPENAI_API_KEY="your-key"
python examples/llm_evaluation.py

# RAG evaluation (requires API key)
python examples/rag_evaluation.py

# Ground truth handling
python examples/ground_truth_examples.py
```

## Code-Based Metrics

See [`examples/basic_usage.py`](../examples/basic_usage.py)

```python
from custom.evals import exact_match, sentiment_score, custom_accuracy

# Example 1: Exact Match
eval_input = {"output": "Paris", "expected": "Paris"}
score = exact_match(eval_input)
print(f"Match: {score.score}")  # 1.0

# Example 2: Sentiment Analysis
eval_input = {"text": "I love this product!"}
score = sentiment_score(eval_input)
print(f"Sentiment: {score.label}")  # positive

# Example 3: Custom Accuracy with Normalization
eval_input = {"output": " PARIS ", "expected": "paris"}
score = custom_accuracy(eval_input, normalize=True)
print(f"Accuracy: {score.score}")  # 1.0
```

## LLM-Based Evaluators

See [`examples/llm_evaluation.py`](../examples/llm_evaluation.py)

```python
from custom.evals import HallucinationEvaluator, CorrectnessEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")

# Hallucination Detection
evaluator = HallucinationEvaluator(llm)
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France.",
    "context": "Paris is the capital and largest city of France."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")

# Correctness Evaluation
evaluator = CorrectnessEvaluator(llm)
eval_input = {
    "input": "What is 2 + 2?",
    "output": "4",
    "expected": "4"
}
score = evaluator.evaluate(eval_input)
print(f"Correct: {score.score}")  # 1.0
```

## RAG Evaluation

See [`examples/rag_evaluation.py`](../examples/rag_evaluation.py)

```python
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")

# Faithfulness Evaluation
faithfulness = FaithfulnessEvaluator(llm)
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France. It's located on the Seine River.",
    "context": "Paris is the capital and largest city of France, located on the Seine River."
}
score = faithfulness.evaluate(eval_input)
print(f"Faithful: {score.label}")

# Answer Relevancy Evaluation
relevancy = AnswerRelevancyEvaluator(llm)
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France."
}
score = relevancy.evaluate(eval_input)
print(f"Relevant: {score.label}")

# Batch Evaluation
rag_test_cases = [
    {
        "input": "What is ML?",
        "output": "Machine learning is a subset of AI.",
        "context": "Machine learning is a branch of AI."
    },
    # ... more cases
]

for test_case in rag_test_cases:
    faith_score = faithfulness.evaluate(test_case)
    rel_score = relevancy.evaluate(test_case)
    print(f"Faithfulness: {faith_score.label}, Relevancy: {rel_score.label}")
```

## Ground Truth Handling

See [`examples/ground_truth_examples.py`](../examples/ground_truth_examples.py)

```python
from custom.evals import exact_match, CorrectnessEvaluator

# With ground truth
eval_input = {"output": "Paris", "expected": "Paris"}
score = exact_match(eval_input)
print(score.label)  # "match"

# Without ground truth
eval_input = {"output": "Paris"}
score = exact_match(eval_input)
print(score.label)  # "no_ground_truth"

# Reference-free evaluator (doesn't need GT)
hallucination_eval = HallucinationEvaluator(llm)
score = hallucination_eval.evaluate({
    "input": "What is Python?",
    "output": "Python is a language.",
    "context": "Python is a programming language."
})
# Works without ground truth!
```

## Async Evaluation

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
print(f"Evaluated {len(scores)} inputs")
```

## Batch Processing with Pandas

```python
import pandas as pd
from custom.evals import exact_match

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
print(f"Accuracy: {df['score'].mean():.2f}")  # 0.67
```

## Field Mapping

```python
from custom.evals import exact_match

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

## Evaluator Introspection

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

## Next Steps

- **[Code-Based Metrics](evaluators/code-based.md)** - Code metrics docs
- **[LLM-Based Evaluators](evaluators/llm-based.md)** - LLM evaluators docs
- **[RAG-Specific Evaluators](evaluators/rag-specific.md)** - RAG evaluators docs
- **[API Reference](api-reference.md)** - Complete API docs
