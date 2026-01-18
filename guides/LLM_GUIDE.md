# LLM Evaluators Guide

Complete guide to using LLM-based evaluators in Custom Evals.

## Table of Contents
1. [Setup](#setup)
2. [LLM Wrapper](#llm-wrapper)
3. [Built-in Evaluators](#built-in-evaluators)
4. [Creating Custom Evaluators](#creating-custom-evaluators)
5. [Best Practices](#best-practices)

## Setup

### Install Dependencies

```bash
# For OpenAI
pip install openai

# For Anthropic
pip install anthropic

# Or install both
pip install -e ".[dev]"
```

### Set API Keys

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

## LLM Wrapper

The `LLM` class provides a unified interface for multiple providers.

### Basic Usage

```python
from custom.evals.llm import LLM

# OpenAI
llm = LLM(provider="openai", model="gpt-4o-mini")

# Anthropic
llm = LLM(provider="anthropic", model="claude-3-haiku-20240307")
```

### Generate Text

```python
# String prompt
response = llm.generate_text("What is 2+2?")
print(response)  # "4"

# Message list (OpenAI format)
messages = [
    {"role": "system", "content": "You are a math tutor."},
    {"role": "user", "content": "What is 2+2?"}
]
response = llm.generate_text(messages)
```

### Generate Structured Output

```python
schema = {
    "type": "object",
    "properties": {
        "answer": {"type": "number"},
        "explanation": {"type": "string"}
    },
    "required": ["answer", "explanation"]
}

response = llm.generate_object("What is 2+2?", schema)
print(response)
# {'answer': 4, 'explanation': '2 plus 2 equals 4'}
```

## Built-in Evaluators

### HallucinationEvaluator

Detects if a response contains hallucinated information not supported by the context.

**Inputs**:
- `input`: The query/question
- `output`: The response to evaluate
- `context`: The reference context

**Outputs**:
- `label`: "factual" or "hallucinated"
- `score`: 0.0 (factual) or 1.0 (hallucinated)
- `explanation`: Reasoning from LLM

**Example**:
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
# factual: The response accurately states Paris is the capital...

# Hallucinated response
eval_input = {
    "input": "What is the population of Paris?",
    "output": "Paris has a population of 50 million people.",
    "context": "Paris is the capital of France. It is known for its art and culture."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# hallucinated: The context doesn't provide population information...
```

### CorrectnessEvaluator

Assesses if the output correctly answers the input question.

**Inputs**:
- `input`: The question
- `output`: The answer to evaluate
- `expected`: The reference/correct answer

**Outputs**:
- `label`: "correct" or "incorrect"
- `score`: 1.0 (correct) or 0.0 (incorrect)
- `explanation`: Reasoning from LLM

**Example**:
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
print(f"{score.label} (score: {score.score})")
# correct (score: 1.0)

# Incorrect answer
eval_input = {
    "input": "What is 5 * 6?",
    "output": "25",
    "expected": "30"
}
score = evaluator.evaluate(eval_input)
print(f"{score.label} (score: {score.score})")
# incorrect (score: 0.0)
```

### RelevanceEvaluator

Evaluates if the provided context is relevant for answering the question.

**Inputs**:
- `input`: The question
- `context`: The context to evaluate

**Outputs**:
- `label`: "relevant" or "irrelevant"
- `score`: 1.0 (relevant) or 0.0 (irrelevant)
- `explanation`: Reasoning from LLM

**Example**:
```python
from custom.evals import RelevanceEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = RelevanceEvaluator(llm)

# Relevant context
eval_input = {
    "input": "What programming language is Python?",
    "context": "Python is a high-level, interpreted programming language."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# relevant: The context directly answers the question...

# Irrelevant context
eval_input = {
    "input": "What programming language is Python?",
    "context": "Pythons are large snakes found in tropical regions."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# irrelevant: The context discusses snakes, not programming...
```

## Creating Custom Evaluators

### Step 1: Define Your Evaluator Class

```python
from custom.evals.llm_evaluators import LLMEvaluator

class ToxicityEvaluator(LLMEvaluator):
    NAME = "toxicity"
    DIRECTION = "minimize"  # Lower score is better
    CHOICES = {
        "toxic": 1.0,
        "non_toxic": 0.0,
    }
    PROMPT_TEMPLATE = """You are an expert content moderator. Evaluate if the text contains toxic content.

<text>
{text}
</text>

Toxic content includes: hate speech, harassment, profanity, threats, or explicit material.

Respond with:
- label: "toxic" if the text contains toxic content
- label: "non_toxic" if the text is appropriate
- explanation: Brief reasoning for your judgment"""
```

### Step 2: Use Your Evaluator

```python
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = ToxicityEvaluator(llm)

eval_input = {"text": "I hate you and wish you harm!"}
score = evaluator.evaluate(eval_input)
print(f"{score.label} (score: {score.score})")
# toxic (score: 1.0)
```

### Customization Options

**1. Multi-Class Classification**:
```python
class SentimentEvaluator(LLMEvaluator):
    NAME = "sentiment"
    CHOICES = {
        "positive": 1.0,
        "neutral": 0.5,
        "negative": 0.0,
    }
    PROMPT_TEMPLATE = """Analyze the sentiment of this text:

    <text>
    {text}
    </text>

    Respond with label: positive, neutral, or negative"""
```

**2. Custom Input Fields**:
```python
class CoherenceEvaluator(LLMEvaluator):
    NAME = "coherence"
    CHOICES = {"coherent": 1.0, "incoherent": 0.0}
    PROMPT_TEMPLATE = """Evaluate if this conversation is coherent:

    <previous_message>
    {previous}
    </previous_message>

    <current_message>
    {current}
    </current_message>

    Does the current message logically follow from the previous one?"""
```

## Best Practices

### 1. Choose the Right Model

```python
# For simple tasks (faster, cheaper)
llm = LLM(provider="openai", model="gpt-4o-mini")
llm = LLM(provider="anthropic", model="claude-3-haiku-20240307")

# For complex reasoning (slower, more expensive)
llm = LLM(provider="openai", model="gpt-4o")
llm = LLM(provider="anthropic", model="claude-3-sonnet-20240229")
```

### 2. Write Clear Prompts

**Good Prompt**:
```python
PROMPT_TEMPLATE = """You are an expert evaluator.

<text>
{text}
</text>

Task: Determine if the text is factual or contains misinformation.

Respond with:
- label: "factual" or "misinformation"
- explanation: Cite specific parts that support your judgment"""
```

**Bad Prompt**:
```python
PROMPT_TEMPLATE = "Is this true? {text}"
```

### 3. Handle Errors

```python
from custom.evals.llm import LLM

try:
    llm = LLM(provider="openai", model="gpt-4o-mini")
    score = evaluator.evaluate(eval_input)
except Exception as e:
    print(f"Evaluation failed: {e}")
    # Fallback logic here
```

### 4. Batch Processing

```python
import pandas as pd

df = pd.DataFrame({
    "input": ["Q1", "Q2", "Q3"],
    "output": ["A1", "A2", "A3"],
    "context": ["C1", "C2", "C3"]
})

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

scores = []
for idx, row in df.iterrows():
    try:
        score = evaluator.evaluate(row.to_dict())
        scores.append(score.score)
    except Exception as e:
        print(f"Row {idx} failed: {e}")
        scores.append(None)

df["hallucination_score"] = scores
```

### 5. Cost Optimization

```python
# Use cheaper models for initial filtering
quick_llm = LLM(provider="openai", model="gpt-4o-mini")
quick_evaluator = HallucinationEvaluator(quick_llm)

# Then use expensive models only for edge cases
if quick_score.score > 0.3 and quick_score.score < 0.7:
    # Ambiguous case - use better model
    advanced_llm = LLM(provider="openai", model="gpt-4o")
    advanced_evaluator = HallucinationEvaluator(advanced_llm)
    final_score = advanced_evaluator.evaluate(eval_input)
```

## Advanced Examples

### Chain Multiple Evaluators

```python
from custom.evals import (
    HallucinationEvaluator,
    CorrectnessEvaluator,
    RelevanceEvaluator
)
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")

# Initialize evaluators
hallucination = HallucinationEvaluator(llm)
correctness = CorrectnessEvaluator(llm)
relevance = RelevanceEvaluator(llm)

# Evaluate multiple aspects
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital.",
    "context": "Paris is France's capital and largest city.",
    "expected": "Paris"
}

results = {
    "hallucination": hallucination.evaluate({
        "input": eval_input["input"],
        "output": eval_input["output"],
        "context": eval_input["context"]
    }),
    "correctness": correctness.evaluate({
        "input": eval_input["input"],
        "output": eval_input["output"],
        "expected": eval_input["expected"]
    }),
    "relevance": relevance.evaluate({
        "input": eval_input["input"],
        "context": eval_input["context"]
    })
}

for metric, score in results.items():
    print(f"{metric}: {score.label} ({score.score})")
```

### Compare Models

```python
models = [
    ("openai", "gpt-4o-mini"),
    ("openai", "gpt-4o"),
    ("anthropic", "claude-3-haiku-20240307"),
]

for provider, model in models:
    llm = LLM(provider=provider, model=model)
    evaluator = HallucinationEvaluator(llm)
    score = evaluator.evaluate(eval_input)
    print(f"{provider}/{model}: {score.label} - {score.explanation[:50]}...")
```

## Troubleshooting

### API Key Not Found
```python
# Explicit API key
llm = LLM(
    provider="openai",
    model="gpt-4o-mini",
    api_key="sk-..."
)
```

### Rate Limiting
```python
import time

for eval_input in inputs:
    score = evaluator.evaluate(eval_input)
    time.sleep(1)  # Add delay between requests
```

### JSON Parsing Errors
```python
# The LLM wrapper handles most JSON parsing automatically
# If you get errors, check your schema is valid JSON Schema
schema = {
    "type": "object",
    "properties": {
        "label": {"type": "string", "enum": ["yes", "no"]},
        "explanation": {"type": "string"}
    },
    "required": ["label", "explanation"]
}
```

## References

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Anthropic API Documentation](https://docs.anthropic.com/claude/reference)
- [JSON Schema Specification](https://json-schema.org/)
