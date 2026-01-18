# Custom Evals - Project Overview

## Summary

This is a lightweight POC (Proof of Concept) evaluation framework inspired by Phoenix Evals. It demonstrates how to build a flexible, extensible system for evaluating LLM outputs with standardized scoring.

## Project Structure

```
cust-evals/
├── src/custom/evals/                    # Main package
│   ├── __init__.py                      # Package exports
│   ├── evaluators.py                    # Core evaluation framework
│   │   ├── Score (dataclass)            # Standardized score object
│   │   └── create_evaluator (decorator) # Evaluator creator
│   └── metrics/                         # Evaluation metrics
│       ├── __init__.py
│       ├── exact_match.py               # Binary string comparison
│       ├── sentiment.py                 # Sentiment analysis (keyword-based)
│       └── accuracy.py                  # Accuracy with normalization
│
├── examples/
│   └── basic_usage.py                   # Usage examples
│
├── tests/
│   └── test_metrics.py                  # Unit tests
│
├── pyproject.toml                       # Package configuration
├── README.md                            # Main documentation
├── QUICKSTART.md                        # Quick start guide
└── .gitignore                           # Git ignore rules
```

## Key Components

### 1. Score Object (`evaluators.py`)

Standardized scoring structure:
```python
@dataclass
class Score:
    score: float                  # Numeric score (0.0-1.0)
    name: str                     # Metric name
    label: Optional[str]          # Categorical label
    explanation: Optional[str]    # Human-readable explanation
    direction: Literal[...]       # maximize/minimize/neutral
    kind: Literal[...]            # code/llm/human/heuristic
    metadata: Dict[str, Any]      # Additional data
```

### 2. Evaluator Decorator (`evaluators.py`)

Decorator pattern for creating evaluators:
```python
@create_evaluator(name="my_metric", kind="code")
def my_metric(output: str, expected: str) -> Score:
    # Your evaluation logic
    return Score(score=...)
```

Features:
- Field mapping support
- Extra kwargs support
- Automatic Score wrapping
- Metadata management

### 3. Metrics

#### Exact Match (`exact_match.py`)
- Binary string comparison
- No normalization
- Returns 1.0 or 0.0

#### Sentiment Score (`sentiment.py`)
- Keyword-based sentiment analysis
- Returns 0.0-1.0 (negative to positive)
- Labels: positive, negative, neutral
- Note: Simple POC implementation

#### Custom Accuracy (`accuracy.py`)
- String comparison with normalization
- Options: lowercase, strip whitespace
- Flexible for different use cases

## Design Patterns

### 1. Decorator Pattern
```python
@create_evaluator(name="...", kind="...")
def evaluator_func(...) -> Score:
    ...
```
Benefits:
- Clean, declarative syntax
- Automatic metadata injection
- Consistent interface

### 2. Field Mapping
```python
eval_input = {"prediction": "A", "ground_truth": "A"}
field_mapping = {"output": "prediction", "expected": "ground_truth"}
score = exact_match(eval_input, field_mapping=field_mapping)
```
Benefits:
- Flexible input formats
- Reusable metrics
- No data transformation needed

### 3. Extra Kwargs
```python
eval_input = {"output": "A", "expected": "a"}
score = custom_accuracy(eval_input, normalize=True)
```
Benefits:
- Runtime configuration
- Metric parameterization
- No wrapper functions needed

## Comparison with Phoenix Evals

| Feature | Phoenix Evals | Custom Evals (POC) |
|---------|--------------|-------------------|
| Metrics | 10+ (hallucination, relevance, etc.) | 3 (exact_match, sentiment, accuracy) |
| LLM Support | Multiple providers (OpenAI, Anthropic, etc.) | None (code-based only) |
| Async Support | Yes | No |
| Batch Processing | Yes | Manual (with pandas) |
| Templates | Extensive prompt templates | Not included |
| Tracing | OpenTelemetry integration | Not included |
| Complexity | Full-featured production library | Minimal POC |

## Extension Points

### 1. Add New Metrics

Create a new file in `src/custom/evals/metrics/`:
```python
from ..evaluators import Score, create_evaluator

@create_evaluator(name="my_new_metric", kind="code")
def my_new_metric(input_param: str) -> Score:
    # Your logic here
    return Score(score=...)
```

Export in `metrics/__init__.py`:
```python
from .my_new_metric import my_new_metric

__all__ = [..., "my_new_metric"]
```

### 2. Add LLM-based Evaluation

```python
from ..evaluators import Score, create_evaluator
import openai

@create_evaluator(name="llm_judge", kind="llm")
def llm_judge(output: str, criteria: str) -> Score:
    # Call LLM API
    response = openai.chat.completions.create(...)
    # Parse response and return Score
    return Score(score=..., explanation=...)
```

### 3. Add Async Support

```python
import asyncio

async def async_evaluate_batch(eval_inputs, evaluator):
    tasks = [evaluator(input) for input in eval_inputs]
    return await asyncio.gather(*tasks)
```

### 4. Add DataFrame Evaluation

```python
import pandas as pd

def evaluate_dataframe(df, evaluator, input_cols, **kwargs):
    scores = []
    for _, row in df.iterrows():
        eval_input = {col: row[col] for col in input_cols}
        score = evaluator(eval_input, **kwargs)
        scores.append(score.to_dict())
    return pd.DataFrame(scores)
```

## Usage Patterns

### Pattern 1: Direct Evaluation
```python
from custom.evals import exact_match

result = exact_match({"output": "A", "expected": "A"})
```

### Pattern 2: With Field Mapping
```python
result = exact_match(
    {"pred": "A", "truth": "A"},
    field_mapping={"output": "pred", "expected": "truth"}
)
```

### Pattern 3: With Extra Parameters
```python
from custom.evals import custom_accuracy

result = custom_accuracy(
    {"output": " A ", "expected": "a"},
    normalize=True,
    lowercase=True
)
```

### Pattern 4: Batch Processing
```python
import pandas as pd
from custom.evals import exact_match

df = pd.DataFrame({
    "output": ["A", "B", "C"],
    "expected": ["A", "B", "D"]
})

scores = []
for _, row in df.iterrows():
    score = exact_match({"output": row["output"], "expected": row["expected"]})
    scores.append(score.score)

df["score"] = scores
accuracy = df["score"].mean()
```

## Testing

Run tests:
```bash
cd cust-evals
pip install pytest
pytest tests/ -v
```

Test coverage:
- Score object creation and serialization
- Each metric with various inputs
- Field mapping functionality
- Normalization options
- Edge cases

## Next Steps for Production

1. **Add LLM Integration**
   - OpenAI adapter
   - Anthropic adapter
   - Generic LLM wrapper

2. **Add More Metrics**
   - Hallucination detection
   - Relevance scoring
   - Code evaluation
   - SQL evaluation

3. **Add Async Support**
   - Async evaluators
   - Batch processing
   - Rate limiting

4. **Add Visualization**
   - Score distribution plots
   - Confusion matrices
   - Error analysis

5. **Add Caching**
   - Result caching
   - LLM response caching

6. **Add Logging/Tracing**
   - OpenTelemetry integration
   - Evaluation tracking
   - Performance monitoring

## License

MIT
