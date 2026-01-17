# RAG-Specific Evaluators

RAG-specific evaluators are designed for evaluating Retrieval-Augmented Generation (RAG) systems. Inspired by **DeepEval** and **RAGAS** frameworks, these metrics assess how well your RAG pipeline performs.

## Overview

| Evaluator | Purpose | Ground Truth | Inspired By |
|-----------|---------|--------------|-------------|
| **FaithfulnessEvaluator** | Verify response is grounded in context | Not required | DeepEval, RAGAS |
| **AnswerRelevancyEvaluator** | Check answer addresses query | Not required | DeepEval, RAGAS |

**Coming Soon (Phase 2):**
- ContextPrecisionEvaluator
- ContextRecallEvaluator
- ContextRelevancyEvaluator

---

## FaithfulnessEvaluator

Evaluates whether a generated response is fully grounded in the provided retrieval context, without hallucinations.

### Concept

**Faithfulness** measures if all statements in the response can be verified from the retrieval context. Unlike general hallucination detection, this focuses on statement-level verification specifically for RAG systems.

### Usage

```python
from custom.evals import FaithfulnessEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = FaithfulnessEvaluator(llm)

# Faithful response (all statements supported by context)
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France. It's located on the Seine River.",
    "context": "Paris is the capital and largest city of France, located on the Seine River in northern France."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: faithful: All statements are supported by the context...

# Unfaithful response (contains unsupported information)
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France with a population of exactly 12 million people.",
    "context": "Paris is the capital and largest city of France."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: unfaithful: The specific population figure is not in the context...
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input` | str | Yes | The user query/question |
| `output` | str | Yes | The generated response from RAG |
| `context` | str | Yes | The retrieved context/documents |

### Configuration

```python
NAME = "faithfulness"
DIRECTION = "maximize"  # Higher is better
REQUIRES_GROUND_TRUTH = False  # Reference-free
CHOICES = {
    "faithful": 1.0,     # All statements grounded in context
    "unfaithful": 0.0,   # Contains unsupported information
}
```

### Return Value

```python
Score(
    score=1.0 | 0.0,           # 1.0=faithful, 0.0=unfaithful
    name="faithfulness",
    label="faithful" | "unfaithful",
    explanation="Statement-level verification details",
    kind="llm",
    direction="maximize",
    metadata={
        "model": "gpt-4o-mini",
        "has_ground_truth": False
    }
)
```

### How It Works

The evaluator:
1. **Breaks down** the response into individual statements/claims
2. **Verifies** each statement against the retrieval context
3. **Checks** if any information goes beyond the context
4. **Returns** faithful if all statements are supported

### When to Use

✅ **Good for:**
- RAG system evaluation
- Fact-checking against retrieved documents
- Preventing hallucinations in production
- Measuring retrieval quality impact

❌ **Not good for:**
- Without retrieval context
- Non-RAG systems (use HallucinationEvaluator)
- Real-time critical paths (has LLM latency)

### Difference from HallucinationEvaluator

| Feature | FaithfulnessEvaluator | HallucinationEvaluator |
|---------|----------------------|------------------------|
| **Focus** | RAG-specific, statement-level | General hallucination detection |
| **Approach** | Verifies each claim | Overall assessment |
| **Use Case** | RAG pipelines | General LLM outputs |
| **Prompt** | RAG-optimized | General-purpose |

### Examples

#### Example 1: Completely Faithful

```python
eval_input = {
    "input": "What is machine learning?",
    "output": "Machine learning is a subset of AI that enables systems to learn from data.",
    "context": "Machine learning is a branch of artificial intelligence that allows computers to learn from data without being explicitly programmed."
}
score = evaluator.evaluate(eval_input)
# Result: faithful (1.0)
# Explanation: Both statements are supported by the context
```

#### Example 2: Partially Unfaithful

```python
eval_input = {
    "input": "What is machine learning?",
    "output": "Machine learning is a subset of AI. It was invented in 1997 by John Smith.",
    "context": "Machine learning is a branch of artificial intelligence."
}
score = evaluator.evaluate(eval_input)
# Result: unfaithful (0.0)
# Explanation: The invention date and inventor are not in the context
```

#### Example 3: Elaboration Without Facts

```python
eval_input = {
    "input": "What is photosynthesis?",
    "output": "Photosynthesis is how plants make food using sunlight, which is an amazing process.",
    "context": "Photosynthesis is the process by which plants convert light into energy."
}
score = evaluator.evaluate(eval_input)
# Result: faithful (1.0)
# Explanation: "amazing" is subjective but the facts are grounded
```

---

## AnswerRelevancyEvaluator

Evaluates whether the generated answer directly addresses the input query and provides relevant information.

### Concept

**Answer Relevancy** measures how well the response answers the specific question asked. Unlike context relevance (which checks if context helps answer), this checks if the answer itself is on-topic.

### Usage

```python
from custom.evals import AnswerRelevancyEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = AnswerRelevancyEvaluator(llm)

# Relevant answer
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: relevant: Directly answers the question...

# Irrelevant answer
eval_input = {
    "input": "What is the capital of France?",
    "output": "France is a country in Europe with many beautiful cities and landmarks."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: irrelevant: Doesn't provide the requested information...
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input` | str | Yes | The user query/question |
| `output` | str | Yes | The generated response to evaluate |

**Note:** `context` is not required for answer relevancy.

### Configuration

```python
NAME = "answer_relevancy"
DIRECTION = "maximize"  # Higher is better
REQUIRES_GROUND_TRUTH = False  # Reference-free
CHOICES = {
    "relevant": 1.0,     # Answer addresses the query
    "irrelevant": 0.0,   # Answer doesn't address the query
}
```

### Return Value

```python
Score(
    score=1.0 | 0.0,           # 1.0=relevant, 0.0=irrelevant
    name="answer_relevancy",
    label="relevant" | "irrelevant",
    explanation="Reasoning about answer-query alignment",
    kind="llm",
    direction="maximize",
    metadata={
        "model": "gpt-4o-mini",
        "has_ground_truth": False
    }
)
```

### How It Works

The evaluator checks:
1. Does the answer **directly address** the query?
2. Does it provide **useful information** for the question?
3. Is it **focused and on-topic** (not rambling)?
4. Does it include the **key information** requested?

### When to Use

✅ **Good for:**
- RAG answer quality evaluation
- Prompt engineering validation
- Detecting off-topic responses
- Measuring RAG pipeline effectiveness

❌ **Not good for:**
- Context relevance (use RelevanceEvaluator)
- Correctness checking (use CorrectnessEvaluator)
- Without a clear query

### Difference from RelevanceEvaluator

| Feature | AnswerRelevancyEvaluator | RelevanceEvaluator |
|---------|-------------------------|-------------------|
| **Evaluates** | Answer to query | Context to query |
| **Focus** | Response quality | Retrieval quality |
| **Input** | query + answer | query + context |
| **Use Case** | Answer evaluation | Retrieval evaluation |

### Examples

#### Example 1: Perfectly Relevant

```python
eval_input = {
    "input": "What is the population of Tokyo?",
    "output": "Tokyo has a population of approximately 14 million people."
}
score = evaluator.evaluate(eval_input)
# Result: relevant (1.0)
# Explanation: Directly answers the specific question
```

#### Example 2: Partially Relevant

```python
eval_input = {
    "input": "What is the population of Tokyo?",
    "output": "Tokyo is the capital of Japan and is a major metropolitan area."
}
score = evaluator.evaluate(eval_input)
# Result: irrelevant (0.0)
# Explanation: Provides related info but doesn't answer the question
```

#### Example 3: Off-Topic

```python
eval_input = {
    "input": "What is the population of Tokyo?",
    "output": "The Eiffel Tower is located in Paris, France."
}
score = evaluator.evaluate(eval_input)
# Result: irrelevant (0.0)
# Explanation: Completely unrelated to the query
```

#### Example 4: Verbose but Relevant

```python
eval_input = {
    "input": "What is Python?",
    "output": "Python is a high-level, interpreted programming language known for its simplicity and versatility. It's widely used in data science, web development, and automation."
}
score = evaluator.evaluate(eval_input)
# Result: relevant (1.0)
# Explanation: Comprehensive answer that addresses the query
```

---

## RAG Evaluation Workflow

Here's how to evaluate a complete RAG system:

```python
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")

# Initialize evaluators
faithfulness = FaithfulnessEvaluator(llm)
answer_relevancy = AnswerRelevancyEvaluator(llm)
context_relevance = RelevanceEvaluator(llm)

def evaluate_rag_response(query, retrieved_context, generated_answer):
    """Comprehensive RAG evaluation."""
    results = {}

    # 1. Context Relevance: Is the retrieved context relevant to the query?
    results["context_relevance"] = context_relevance.evaluate({
        "input": query,
        "context": retrieved_context
    })

    # 2. Faithfulness: Is the answer grounded in the context?
    results["faithfulness"] = faithfulness.evaluate({
        "input": query,
        "output": generated_answer,
        "context": retrieved_context
    })

    # 3. Answer Relevancy: Does the answer address the query?
    results["answer_relevancy"] = answer_relevancy.evaluate({
        "input": query,
        "output": generated_answer
    })

    return results

# Example usage
query = "What is the capital of France?"
context = "Paris is the capital and largest city of France."
answer = "Paris is the capital of France."

scores = evaluate_rag_response(query, context, answer)

print(f"Context Relevance: {scores['context_relevance'].label}")
print(f"Faithfulness: {scores['faithfulness'].label}")
print(f"Answer Relevancy: {scores['answer_relevancy'].label}")
```

---

## Batch RAG Evaluation

Evaluate multiple RAG responses efficiently:

```python
import asyncio
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

async def evaluate_rag_batch(test_cases):
    llm = LLM(provider="openai", model="gpt-4o-mini")
    faithfulness = FaithfulnessEvaluator(llm)
    relevancy = AnswerRelevancyEvaluator(llm)

    results = []
    for test_case in test_cases:
        # Evaluate faithfulness and relevancy concurrently
        faith_task = faithfulness.async_evaluate({
            "input": test_case["query"],
            "output": test_case["answer"],
            "context": test_case["context"]
        })
        rel_task = relevancy.async_evaluate({
            "input": test_case["query"],
            "output": test_case["answer"]
        })

        faith_score, rel_score = await asyncio.gather(faith_task, rel_task)

        results.append({
            "query": test_case["query"],
            "faithfulness": faith_score.score,
            "relevancy": rel_score.score
        })

    return results

# Usage
test_cases = [
    {
        "query": "What is ML?",
        "context": "Machine learning is...",
        "answer": "Machine learning is..."
    },
    # ... more test cases
]

results = asyncio.run(evaluate_rag_batch(test_cases))
```

---

## Comparison with Other Frameworks

### DeepEval

Our implementation is inspired by DeepEval's RAG metrics:
- Similar **Faithfulness** concept
- Similar **Answer Relevancy** approach
- Compatible **reference-free** design

### RAGAS

Our implementation aligns with RAGAS metrics:
- **Faithfulness** matches RAGAS concept
- **Answer Relevancy** similar to RAGAS implementation
- Same **no ground truth** philosophy

See **[Framework Comparison](../framework-comparison.md)** for detailed comparison.

---

## Best Practices

### 1. Use Both Metrics Together

Always evaluate both faithfulness and relevancy:

```python
# Good: Comprehensive evaluation
faithfulness_score = faithfulness.evaluate(eval_input)
relevancy_score = relevancy.evaluate(eval_input)

if faithfulness_score.label == "faithful" and relevancy_score.label == "relevant":
    print("✓ High-quality RAG response")
```

### 2. Set Quality Thresholds

```python
MIN_FAITHFULNESS = 0.9
MIN_RELEVANCY = 0.8

def is_good_response(faith_score, rel_score):
    return (
        faith_score >= MIN_FAITHFULNESS and
        rel_score >= MIN_RELEVANCY
    )
```

### 3. Monitor Over Time

Track metrics to identify RAG pipeline issues:

```python
import pandas as pd

results = []
for query, context, answer in dataset:
    scores = evaluate_rag_response(query, context, answer)
    results.append({
        "faithfulness": scores["faithfulness"].score,
        "relevancy": scores["answer_relevancy"].score
    })

df = pd.DataFrame(results)
print(f"Avg Faithfulness: {df['faithfulness'].mean():.2f}")
print(f"Avg Relevancy: {df['relevancy'].mean():.2f}")
```

### 4. Use for A/B Testing

Compare different RAG configurations:

```python
# Test different retrieval strategies
results_bm25 = evaluate_with_retriever(bm25_retriever)
results_vector = evaluate_with_retriever(vector_retriever)

print(f"BM25 Faithfulness: {results_bm25['faithfulness']}")
print(f"Vector Faithfulness: {results_vector['faithfulness']}")
```

---

## Future Additions (Phase 2)

Coming soon:

1. **ContextPrecisionEvaluator** - Evaluate ranking quality
2. **ContextRecallEvaluator** - Measure retrieval completeness
3. **ContextRelevancyEvaluator** - More specific context evaluation

See **[Framework Comparison](../framework-comparison.md)** for roadmap.

---

## Next Steps

- **[Framework Comparison](../framework-comparison.md)** - Compare with DeepEval/RAGAS
- **[Examples](../examples.md)** - RAG evaluation examples
- **[LLM-Based Evaluators](llm-based.md)** - General LLM evaluators
- **[API Reference](../api-reference.md)** - Complete API docs
