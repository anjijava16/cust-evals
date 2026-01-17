# API Reference

Complete API reference for Custom Evals framework.

## Core Classes

### Score

The standard result object returned by all evaluators.

```python
@dataclass
class Score:
    score: float
    name: str = "score"
    label: Optional[str] = None
    explanation: Optional[str] = None
    direction: Literal["maximize", "minimize", "neutral"] = "maximize"
    kind: Literal["code", "llm", "human", "heuristic"] = "code"
    metadata: Dict[str, Any] = field(default_factory=dict)
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `score` | float | Numerical score (typically 0.0 to 1.0) |
| `name` | str | Name of the evaluator |
| `label` | Optional[str] | Classification label (e.g., "correct", "faithful") |
| `explanation` | Optional[str] | Human-readable explanation of the score |
| `direction` | str | "maximize" (higher is better), "minimize" (lower is better), or "neutral" |
| `kind` | str | Type of evaluator: "code", "llm", "human", or "heuristic" |
| `metadata` | Dict | Additional information (model name, ground truth availability, etc.) |

#### Example

```python
Score(
    score=1.0,
    name="exact_match",
    label="match",
    explanation="Output matches expected value",
    direction="maximize",
    kind="code",
    metadata={"has_ground_truth": True}
)
```

---

### LLM

Unified interface for LLM providers.

```python
class LLM:
    def __init__(
        self,
        provider: Literal["openai", "anthropic"],
        model: str,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """Initialize LLM client."""
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider` | str | Yes | "openai" or "anthropic" |
| `model` | str | Yes | Model identifier |
| `api_key` | str | No | API key (uses environment variable if not provided) |
| `**kwargs` | Any | No | Additional provider-specific parameters |

#### Methods

##### generate_text()

Generate text completion.

```python
def generate_text(
    self,
    prompt: Union[str, List[Dict[str, str]]],
    **kwargs
) -> str:
    """Generate text from prompt."""
```

##### generate_object()

Generate structured JSON output.

```python
def generate_object(
    self,
    prompt: Union[str, List[Dict[str, str]]],
    schema: Dict[str, Any],
    **kwargs
) -> Dict[str, Any]:
    """Generate structured output matching schema."""
```

#### Example

```python
from custom.evals.llm import LLM

# Initialize
llm = LLM(provider="openai", model="gpt-4o-mini")

# Text generation
text = llm.generate_text("Hello, how are you?")

# Structured generation
schema = {
    "type": "object",
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "negative"]},
        "confidence": {"type": "number"}
    }
}
result = llm.generate_object("Analyze sentiment: I love this!", schema)
# {'sentiment': 'positive', 'confidence': 0.95}
```

---

## Decorators

### @create_evaluator

Decorator for creating code-based evaluators.

```python
def create_evaluator(
    name: str,
    kind: Literal["code", "llm", "human", "heuristic"] = "code",
    direction: Literal["maximize", "minimize", "neutral"] = "maximize"
):
    """Create an evaluator from a function."""
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | Required | Name of the evaluator |
| `kind` | str | "code" | Type of evaluator |
| `direction` | str | "maximize" | Score direction |

#### Example

```python
from custom.evals import create_evaluator, Score

@create_evaluator(name="my_metric", direction="maximize")
def my_metric(output: str, expected: str) -> Score:
    correct = output == expected
    return Score(
        score=float(correct),
        label="match" if correct else "no_match"
    )

# Use with dict input
score = my_metric({"output": "A", "expected": "A"})

# Use with field mapping
score = my_metric(
    {"prediction": "A", "target": "A"},
    field_mapping={"output": "prediction", "expected": "target"}
)
```

---

## LLM Evaluator Base Class

### LLMEvaluator

Base class for all LLM-based evaluators.

```python
class LLMEvaluator:
    def __init__(self, llm: LLM):
        """Initialize evaluator with LLM instance."""
```

#### Class Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `NAME` | str | Evaluator name |
| `PROMPT_TEMPLATE` | str | Prompt template string |
| `CHOICES` | Dict[str, float] | Label to score mapping |
| `DIRECTION` | str | Score direction |
| `REQUIRES_GROUND_TRUTH` | bool | Whether ground truth is required |

#### Public Methods

##### evaluate()

Synchronous evaluation.

```python
def evaluate(self, eval_input: Dict[str, Any]) -> Score:
    """Evaluate input and return Score."""
```

##### async_evaluate()

Asynchronous evaluation.

```python
async def async_evaluate(self, eval_input: Dict[str, Any]) -> Score:
    """Async evaluation returning Score."""
```

##### describe()

Get evaluator metadata.

```python
def describe(self) -> Dict[str, Any]:
    """Return evaluator description."""
```

Returns:
```python
{
    "name": str,
    "kind": str,
    "direction": str,
    "requires_ground_truth": bool,
    "choices": Dict[str, float],
    "model": str,
    "provider": str
}
```

#### Internal Methods (For Subclassing)

##### _evaluate()

Override for custom evaluation logic.

```python
def _evaluate(self, eval_input: Dict[str, Any]) -> Score:
    """Internal sync evaluation logic."""
```

##### _async_evaluate()

Override for custom async logic.

```python
async def _async_evaluate(self, eval_input: Dict[str, Any]) -> Score:
    """Internal async evaluation logic."""
```

##### _check_ground_truth()

Override for custom ground truth checking.

```python
def _check_ground_truth(self, eval_input: Dict[str, Any]) -> bool:
    """Check if ground truth is available."""
```

##### _create_output_schema()

Override for custom output schema.

```python
def _create_output_schema(self) -> Dict[str, Any]:
    """Create JSON schema for LLM output."""
```

#### Example: Custom Evaluator

```python
from custom.evals.llm_evaluators import LLMEvaluator
from custom.evals import Score

class ToxicityEvaluator(LLMEvaluator):
    NAME = "toxicity"
    DIRECTION = "minimize"
    REQUIRES_GROUND_TRUTH = False
    CHOICES = {
        "toxic": 1.0,
        "non_toxic": 0.0
    }
    PROMPT_TEMPLATE = """
    Evaluate if this text is toxic:
    <text>{text}</text>
    Is it toxic or non_toxic?
    """

    def _check_ground_truth(self, eval_input):
        return False  # Reference-free

# Usage
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = ToxicityEvaluator(llm)
score = evaluator.evaluate({"text": "I hate you!"})
```

---

## Code-Based Metrics

### exact_match()

```python
def exact_match(
    eval_input: Dict[str, Any],
    field_mapping: Optional[Dict[str, str]] = None,
    **extra_kwargs: Any
) -> Score
```

### sentiment_score()

```python
def sentiment_score(
    eval_input: Dict[str, Any],
    field_mapping: Optional[Dict[str, str]] = None,
    **extra_kwargs: Any
) -> Score
```

### custom_accuracy()

```python
def custom_accuracy(
    eval_input: Dict[str, Any],
    field_mapping: Optional[Dict[str, str]] = None,
    normalize: bool = False,
    **extra_kwargs: Any
) -> Score
```

---

## LLM-Based Evaluators

All LLM evaluators share the same interface:

### HallucinationEvaluator

```python
from custom.evals import HallucinationEvaluator

evaluator = HallucinationEvaluator(llm)
score = evaluator.evaluate({
    "input": str,
    "output": str,
    "context": str
})
```

### CorrectnessEvaluator

```python
from custom.evals import CorrectnessEvaluator

evaluator = CorrectnessEvaluator(llm)
score = evaluator.evaluate({
    "input": str,
    "output": str,
    "expected": str  # Required
})
```

### RelevanceEvaluator

```python
from custom.evals import RelevanceEvaluator

evaluator = RelevanceEvaluator(llm)
score = evaluator.evaluate({
    "input": str,
    "context": str
})
```

### CoherenceEvaluator

```python
from custom.evals import CoherenceEvaluator

evaluator = CoherenceEvaluator(llm)
score = evaluator.evaluate({
    "output": str
})
```

### FaithfulnessEvaluator

```python
from custom.evals import FaithfulnessEvaluator

evaluator = FaithfulnessEvaluator(llm)
score = evaluator.evaluate({
    "input": str,
    "output": str,
    "context": str
})
```

### AnswerRelevancyEvaluator

```python
from custom.evals import AnswerRelevancyEvaluator

evaluator = AnswerRelevancyEvaluator(llm)
score = evaluator.evaluate({
    "input": str,
    "output": str
})
```

---

## Field Mapping

All evaluators support field mapping to adapt to your data format:

```python
# Your data
eval_input = {
    "model_output": "Paris",
    "ground_truth_label": "Paris"
}

# Map to evaluator fields
field_mapping = {
    "output": "model_output",
    "expected": "ground_truth_label"
}

score = exact_match(eval_input, field_mapping=field_mapping)
```

---

## Ground Truth Field Names

Evaluators recognize multiple field names for ground truth:

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

---

## Async Support

All LLM evaluators support async evaluation:

```python
import asyncio

# Single async evaluation
score = await evaluator.async_evaluate(eval_input)

# Batch async evaluation
tasks = [evaluator.async_evaluate(inp) for inp in inputs]
scores = await asyncio.gather(*tasks)
```

---

## Error Handling

### Missing Ground Truth

When ground truth is required but not provided:

```python
score = correctness_evaluator.evaluate({
    "input": "What is 2+2?",
    "output": "4"
    # Missing 'expected' field
})

# Returns error score
assert score.label == "no_ground_truth"
assert score.score == 0.0
```

### Missing Required Fields

When required fields are missing:

```python
score = evaluator.evaluate({
    "output": "Paris"
    # Missing 'input' or 'context'
})

# Returns error score
assert score.label == "error"
assert "Missing required input field" in score.explanation
```

---

## Type Hints

```python
from typing import Dict, Any, Optional, Literal
from dataclasses import dataclass

# Score type
Score: dataclass

# Evaluator input
EvalInput = Dict[str, Any]

# Field mapping
FieldMapping = Optional[Dict[str, str]]

# Score direction
Direction = Literal["maximize", "minimize", "neutral"]

# Evaluator kind
Kind = Literal["code", "llm", "human", "heuristic"]

# LLM provider
Provider = Literal["openai", "anthropic"]
```

---

## Next Steps

- **[Examples](examples.md)** - Working code examples
- **[Evaluators](evaluators/code-based.md)** - Evaluator documentation
- **[LLM Integration](llm-integration.md)** - LLM setup
- **[Ground Truth](ground-truth.md)** - Ground truth handling
