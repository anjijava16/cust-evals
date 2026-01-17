# Custom Evals Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Custom Evals POC                         │
│                                                              │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │  Code-Based      │        │   LLM-Based      │          │
│  │  Evaluators      │        │   Evaluators     │          │
│  └──────────────────┘        └──────────────────┘          │
│           │                           │                     │
│           └───────────┬───────────────┘                     │
│                       │                                     │
│                ┌──────▼──────┐                              │
│                │    Score    │                              │
│                │   Object    │                              │
│                └─────────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Core Components

```
┌─────────────────────────────────────────────────────────────┐
│ evaluators.py                                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │ @dataclass Score                             │          │
│  │  - score: float                              │          │
│  │  - name: str                                 │          │
│  │  - label: Optional[str]                      │          │
│  │  - explanation: Optional[str]                │          │
│  │  - kind: Literal["code","llm","human",...]   │          │
│  │  - direction: Literal["maximize","minimize"] │          │
│  │  - metadata: Dict[str, Any]                  │          │
│  └──────────────────────────────────────────────┘          │
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │ create_evaluator(name, kind, direction)      │          │
│  │  - Decorator for code-based metrics          │          │
│  │  - Handles field mapping                     │          │
│  │  - Injects metadata                          │          │
│  └──────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### 2. Code-Based Metrics

```
┌─────────────────────────────────────────────────────────────┐
│ metrics/                                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  exact_match.py                                             │
│  ┌────────────────────────────────────────┐                │
│  │ @create_evaluator(name="exact_match")  │                │
│  │ def exact_match(output, expected):     │                │
│  │     return Score(score=...)            │                │
│  └────────────────────────────────────────┘                │
│                                                              │
│  sentiment.py                                               │
│  ┌────────────────────────────────────────┐                │
│  │ @create_evaluator(name="sentiment")    │                │
│  │ def sentiment_score(text):             │                │
│  │     return Score(score=...)            │                │
│  └────────────────────────────────────────┘                │
│                                                              │
│  accuracy.py                                                │
│  ┌────────────────────────────────────────┐                │
│  │ @create_evaluator(name="accuracy")     │                │
│  │ def custom_accuracy(output, expected): │                │
│  │     return Score(score=...)            │                │
│  └────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### 3. LLM Infrastructure

```
┌─────────────────────────────────────────────────────────────┐
│ llm/wrapper.py                                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │ LLM(provider, model)                         │          │
│  │                                              │          │
│  │  ├─ generate_text(prompt) → str             │          │
│  │  │                                           │          │
│  │  └─ generate_object(prompt, schema) → dict  │          │
│  │                                              │          │
│  │  Providers:                                  │          │
│  │  ┌────────────┐  ┌──────────────┐           │          │
│  │  │  OpenAI    │  │  Anthropic   │           │          │
│  │  │  gpt-4o    │  │  claude-3    │           │          │
│  │  └────────────┘  └──────────────┘           │          │
│  └──────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### 4. LLM-Based Evaluators

```
┌─────────────────────────────────────────────────────────────┐
│ llm_evaluators.py                                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │ class LLMEvaluator (Base)                    │          │
│  │  - llm: LLM                                  │          │
│  │  - NAME: str                                 │          │
│  │  - PROMPT_TEMPLATE: str                      │          │
│  │  - CHOICES: Dict[str, float]                 │          │
│  │  - DIRECTION: str                            │          │
│  │                                              │          │
│  │  def evaluate(eval_input) → Score           │          │
│  │    1. Render prompt                          │          │
│  │    2. Call LLM                               │          │
│  │    3. Parse response                         │          │
│  │    4. Return Score                           │          │
│  └──────────────────────────────────────────────┘          │
│                                                              │
│  Implementations:                                           │
│  ┌─────────────────────┐                                   │
│  │ HallucinationEvaluator                                  │
│  │  CHOICES: factual=0.0, hallucinated=1.0                 │
│  │  Inputs: input, output, context                         │
│  └─────────────────────┘                                   │
│                                                              │
│  ┌─────────────────────┐                                   │
│  │ CorrectnessEvaluator                                    │
│  │  CHOICES: correct=1.0, incorrect=0.0                    │
│  │  Inputs: input, output, expected                        │
│  └─────────────────────┘                                   │
│                                                              │
│  ┌─────────────────────┐                                   │
│  │ RelevanceEvaluator                                      │
│  │  CHOICES: relevant=1.0, irrelevant=0.0                  │
│  │  Inputs: input, context                                 │
│  └─────────────────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Code-Based Evaluation Flow

```
User Input
   │
   ├─ {"output": "Paris", "expected": "Paris"}
   │
   ▼
create_evaluator wrapper
   │
   ├─ Apply field_mapping (if provided)
   ├─ Merge extra_kwargs
   │
   ▼
Evaluator Function
   │
   ├─ Execute evaluation logic
   ├─ Return Score object
   │
   ▼
Wrapper Post-Processing
   │
   ├─ Inject name, kind, direction
   ├─ Return final Score
   │
   ▼
Score Object
   │
   └─ score: 1.0, name: "exact_match", label: "match"
```

### LLM-Based Evaluation Flow

```
User Input
   │
   ├─ {"input": "Q?", "output": "A", "context": "C"}
   │
   ▼
LLM Evaluator
   │
   ├─ Render PROMPT_TEMPLATE with input vars
   │
   ▼
LLM.generate_object()
   │
   ├─ Send prompt to LLM API
   ├─ Parse structured response
   │   {"label": "factual", "explanation": "..."}
   │
   ▼
Process Response
   │
   ├─ Map label → score using CHOICES
   ├─ Extract explanation
   │
   ▼
Score Object
   │
   └─ score: 0.0, label: "factual", explanation: "..."
      kind: "llm", metadata: {"model": "gpt-4o-mini"}
```

## Extensibility Points

### 1. Adding Code-Based Metrics

```python
# Step 1: Create file
# src/custom/evals/metrics/my_metric.py

from ..evaluators import Score, create_evaluator

@create_evaluator(name="my_metric", kind="code")
def my_metric(input_param: str) -> Score:
    # Your logic here
    return Score(score=...)

# Step 2: Export
# src/custom/evals/metrics/__init__.py
from .my_metric import my_metric
__all__ = [..., "my_metric"]

# Step 3: Export in main
# src/custom/evals/__init__.py
from .metrics import my_metric
__all__ = [..., "my_metric"]
```

### 2. Adding LLM-Based Evaluators

```python
# Add to src/custom/evals/llm_evaluators.py

class MyEvaluator(LLMEvaluator):
    NAME = "my_evaluator"
    DIRECTION = "maximize"
    CHOICES = {
        "good": 1.0,
        "bad": 0.0,
    }
    PROMPT_TEMPLATE = """
    Evaluate: {text}
    Respond with label and explanation...
    """

# Export in src/custom/evals/__init__.py
from .llm_evaluators import MyEvaluator
__all__ = [..., "MyEvaluator"]
```

### 3. Adding LLM Providers

```python
# Add to src/custom/evals/llm/wrapper.py

class LLM:
    def __init__(self, provider, model, **kwargs):
        if provider == "new_provider":
            self.client = NewProviderClient(**kwargs)
        # ...

    def _new_provider_generate_text(self, prompt, **kwargs):
        # Implementation
        pass
```

## Design Patterns

### 1. Decorator Pattern
Used for code-based evaluators to inject metadata and handle field mapping.

### 2. Strategy Pattern
LLM class uses different strategies (OpenAI/Anthropic) for the same interface.

### 3. Template Method Pattern
LLMEvaluator defines the evaluation algorithm, subclasses provide specifics.

### 4. Factory Pattern
`create_evaluator` acts as a factory for creating evaluator functions.

## Dependencies

```
Core:
├── pandas (data manipulation)
├── pydantic (validation)
└── typing-extensions (type hints)

LLM Support:
├── openai>=1.0.0 (OpenAI API)
└── anthropic>=0.18.0 (Anthropic API)

Testing:
└── pytest>=7.0.0 (unit tests)
```

## Performance Considerations

### Code-Based Metrics
- **Fast**: Milliseconds per evaluation
- **No API calls**: Runs locally
- **Scalable**: Can process thousands per second

### LLM-Based Evaluators
- **Slow**: 1-3 seconds per evaluation
- **API dependent**: Network latency + LLM processing
- **Cost**: $0.001-0.01 per evaluation (varies by model)
- **Rate limits**: Typically 100-500 RPM

### Optimization Strategies
1. **Use cheaper models** for simple tasks (gpt-4o-mini, claude-haiku)
2. **Batch requests** to reduce overhead
3. **Cache results** for repeated evaluations
4. **Use code-based metrics** when possible

## Security Considerations

1. **API Keys**: Store in environment variables, never in code
2. **Input Validation**: Validate user inputs before sending to LLM
3. **Rate Limiting**: Implement to prevent abuse
4. **Cost Monitoring**: Track API usage to prevent unexpected bills

## Future Architecture

```
Planned Enhancements:
├── Async Support
│   └── asyncio for concurrent evaluations
├── Caching Layer
│   └── Redis/SQLite for response caching
├── Rate Limiter
│   └── Token bucket algorithm
├── Tracing
│   └── OpenTelemetry integration
└── More Providers
    ├── Vertex AI
    ├── Bedrock
    └── Azure OpenAI
```

---

This architecture provides a solid foundation for building production-ready evaluation systems while remaining simple and easy to understand.
