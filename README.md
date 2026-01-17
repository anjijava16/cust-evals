# Custom Evals - Multi-Framework Evaluation

A lightweight evaluation framework for LLM outputs, supporting evaluation patterns from **RAGAS**, **DeepEval**, and **Phoenix Evals**.

**🔥 NEW: Phoenix (Arize) Tracing Integration via OpenTelemetry!**

## 🎯 Multi-Framework Support

Custom Evals supports evaluation patterns from:
- **✅ RAGAS** - RAG evaluation metrics (Faithfulness, Answer Relevancy)
- **✅ DeepEval** - Comprehensive LLM evaluation (key metrics implemented)
- **✅ Phoenix Evals** - API patterns + **OpenTelemetry tracing** 🔥

See **[FRAMEWORK_SUPPORT.md](FRAMEWORK_SUPPORT.md)** for complete details.

## Features

This framework includes **code-based** and **LLM-based** evaluators:

### Code-Based Metrics
- **Exact Match**: Binary comparison of output vs expected
- **Sentiment Score**: Sentiment analysis of text output
- **Custom Accuracy**: Flexible accuracy metric with normalization

### LLM-Based Evaluators

**General Evaluation:**
- **HallucinationEvaluator**: Detect hallucinations in grounded responses
- **CorrectnessEvaluator**: Assess correctness of answers
- **RelevanceEvaluator**: Evaluate context relevance
- **CoherenceEvaluator**: Assess text coherence and logical consistency

**RAG-Specific Evaluation:**
- **FaithfulnessEvaluator**: Check if response is grounded in retrieval context (inspired by DeepEval/RAGAS)
- **AnswerRelevancyEvaluator**: Evaluate answer-to-query relevance (inspired by DeepEval/RAGAS)

### 🔥 Phoenix (Arize) Tracing (Optional - NEW!)

**Tracing is completely optional.** The framework works perfectly end-to-end without it.

If you want observability with Phoenix, enable OpenTelemetry tracing:

```python
from custom.evals import initialize_tracing, HallucinationEvaluator
from custom.evals.llm import LLM

# Option 1: WITHOUT tracing (default)
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)
score = evaluator.evaluate({...})  # Works perfectly!

# Option 2: WITH tracing (optional, for observability)
initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")
score = evaluator.evaluate({...})  # Now traced in Phoenix UI!
```

**Benefits of tracing (when enabled):**
- 📊 Visualize evaluation flows in Phoenix
- 🔍 Debug performance issues
- ⏱️ Monitor production usage
- 📈 Analyze patterns

See **[TRACING_GUIDE.md](TRACING_GUIDE.md)** for setup and **[docs/tracing.md](docs/tracing.md)** for complete guide.

## Installation

```bash
# Basic installation
pip install -e .

# With LLM support (recommended)
pip install -e ".[dev]"

# With Phoenix tracing (optional - only if you want observability)
pip install -e ".[dev,tracing]"
```

**Note:** Tracing is completely optional. The framework works perfectly with just `pip install -e ".[dev]"`

## Quick Start

### Code-Based Metrics

```python
from custom.evals import exact_match, sentiment_score, custom_accuracy

# Example 1: Exact Match
eval_input = {"output": "Paris", "expected": "Paris"}
score = exact_match(eval_input)
print(score)  # Score(score=1.0, name='exact_match', ...)

# Example 2: Sentiment Score
eval_input = {"text": "I love this product! It's amazing!"}
score = sentiment_score(eval_input)
print(score)  # Score(score=0.9, name='sentiment', ...)

# Example 3: Custom Accuracy
eval_input = {"output": " Paris ", "expected": "paris"}
score = custom_accuracy(eval_input, normalize=True)
print(score)  # Score(score=1.0, name='accuracy', ...)
```

### LLM-Based Evaluators

**Note**: Requires API keys. Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` environment variable.

```python
from custom.evals import HallucinationEvaluator, CorrectnessEvaluator
from custom.evals.llm import LLM

# Initialize LLM (supports OpenAI and Anthropic)
llm = LLM(provider="openai", model="gpt-4o-mini")

# Example 1: Hallucination Detection
evaluator = HallucinationEvaluator(llm)
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France.",
    "context": "Paris is the capital and largest city of France."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: factual: The response accurately states that Paris is the capital...

# Example 2: Correctness Evaluation
evaluator = CorrectnessEvaluator(llm)
eval_input = {
    "input": "What is 2 + 2?",
    "output": "4",
    "expected": "4"
}
score = evaluator.evaluate(eval_input)
print(f"{score.label} (score: {score.score})")
# Output: correct (score: 1.0)

# Example 3: Relevance Evaluation
from custom.evals import RelevanceEvaluator

evaluator = RelevanceEvaluator(llm)
eval_input = {
    "input": "What is Python?",
    "context": "Python is a high-level programming language."
}
score = evaluator.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: relevant: The context directly addresses the question...

# Example 4: RAG Evaluation (NEW!)
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator

# Faithfulness: Check if response is grounded in context
faithfulness = FaithfulnessEvaluator(llm)
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France. It's located on the Seine River.",
    "context": "Paris is the capital and largest city of France, located on the Seine River."
}
score = faithfulness.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: faithful: All statements verified from context...

# Answer Relevancy: Check if answer addresses the query
relevancy = AnswerRelevancyEvaluator(llm)
eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France."
}
score = relevancy.evaluate(eval_input)
print(f"{score.label}: {score.explanation}")
# Output: relevant: Answer directly addresses the query...
```

## 🎯 Practical Examples (NEW!)

**4 production-ready examples with full testing** (2,700+ lines, 22 test suites):

### Agent Examples

```bash
# LangGraph Agent - Stateful workflow with tools
python examples/langgraph_agent_example.py

# LangChain Agent - ReAct agent with multiple tools
python examples/langchain_agent_example.py

# Multi-Agent System - 4 specialized agents with orchestration
python examples/multi_agent_example.py
```

### RAG Examples

```bash
# LangChain RAG + Qdrant - PDF processing, vector DB, RAG evaluation
python examples/rag_langchain_qdrant.py
```

**See [PRACTICAL_EXAMPLES_GUIDE.md](PRACTICAL_EXAMPLES_GUIDE.md) for complete documentation!**

---

## Running Basic Examples

```bash
# Code-based metrics
python examples/basic_usage.py

# LLM-based evaluators (requires API key)
export OPENAI_API_KEY="your-key-here"
python examples/llm_evaluation.py

# RAG evaluation
python examples/rag_evaluation.py

# Ground truth handling examples
python examples/ground_truth_examples.py
```

## Supported LLM Providers

### OpenAI
```python
from custom.evals.llm import LLM

llm = LLM(
    provider="openai",
    model="gpt-4o-mini",  # or gpt-4o, gpt-4-turbo, etc.
    api_key="your-key"    # optional, uses env var by default
)
```

### Anthropic
```python
from custom.evals.llm import LLM

llm = LLM(
    provider="anthropic",
    model="claude-3-haiku-20240307",  # or claude-3-sonnet, claude-3-opus
    api_key="your-key"                # optional, uses env var by default
)
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

### Quick Links

- **[Getting Started](docs/getting-started.md)** - Installation and quick start guide
- **[Examples](docs/examples.md)** - Working code examples for all evaluators
- **[API Reference](docs/api-reference.md)** - Complete API documentation

### Evaluators

- **[Code-Based Metrics](docs/evaluators/code-based.md)** - exact_match, sentiment_score, custom_accuracy
- **[LLM-Based Evaluators](docs/evaluators/llm-based.md)** - General LLM evaluation
- **[RAG-Specific Evaluators](docs/evaluators/rag-specific.md)** - RAG system evaluation (NEW!)

### Integration Guides (NEW!)

**Works with ALL frameworks!**

- **[Agents & Multi-Agent Systems](docs/agents-integration.md)** - LangChain agents, LlamaIndex agents, CrewAI, custom agents
- **[RAG Applications](docs/rag-integration.md)** - LangChain RAG, LlamaIndex RAG, custom RAG pipelines
- **[LLM Applications](docs/llm-app-integration.md)** - Chatbots, Q&A systems, summarization, classification

### Advanced Topics

- **[LLM Integration](docs/llm-integration.md)** - LLM setup and configuration
- **[Phoenix Tracing](docs/tracing.md)** - Optional OpenTelemetry tracing with Phoenix (NEW!)
- **[Ground Truth Handling](docs/ground-truth.md)** - Flexible ground truth support
- **[Architecture](docs/architecture.md)** - System design and patterns
- **[Framework Comparison](docs/framework-comparison.md)** - Compare with DeepEval, RAGAS, Phoenix Evals

### Testing

- **[Testing Guide](docs/testing.md)** - Comprehensive test suite (150+ tests) (NEW!)

### Contributing

- **[Contributing Guide](docs/contributing.md)** - How to add new evaluators

**[📖 View Full Documentation →](docs/README.md)**

## Project Structure

```
cust-evals/
├── docs/                       # 📚 Complete documentation
│   ├── README.md              # Documentation landing page
│   ├── getting-started.md     # Installation & quick start
│   ├── examples.md            # Code examples
│   ├── api-reference.md       # API documentation
│   ├── evaluators/            # Evaluator documentation
│   │   ├── code-based.md      # Code-based metrics
│   │   ├── llm-based.md       # LLM evaluators
│   │   └── rag-specific.md    # RAG evaluators
│   ├── llm-integration.md     # LLM setup
│   ├── ground-truth.md        # Ground truth guide
│   ├── architecture.md        # System architecture
│   ├── framework-comparison.md # Framework comparison
│   └── contributing.md        # Contributing guide
├── src/custom/evals/
│   ├── __init__.py
│   ├── evaluators.py          # Core Score class and decorator
│   ├── llm_evaluators.py      # LLM-based evaluators (6 evaluators)
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── wrapper.py         # LLM wrapper (OpenAI, Anthropic)
│   │   └── prompts.py         # Prompt template system
│   └── metrics/
│       ├── exact_match.py     # Binary comparison
│       ├── sentiment.py       # Sentiment analysis
│       └── accuracy.py        # Flexible accuracy
├── examples/
│   ├── basic_usage.py         # Code-based metrics examples
│   ├── llm_evaluation.py      # LLM evaluator examples
│   ├── rag_evaluation.py      # RAG evaluation examples (NEW!)
│   └── ground_truth_examples.py # Ground truth examples
├── tests/
│   └── test_metrics.py
├── README.md                   # Main README
├── INDEX.md                    # Documentation index
└── pyproject.toml
```

## Architecture

### Score Object

All evaluators return a standardized `Score` object:

```python
Score(
    score=0.85,                    # Numeric score (0.0-1.0)
    name="hallucination",          # Metric name
    label="factual",               # Categorical label
    explanation="...",             # Human-readable explanation
    kind="llm",                    # Evaluator type (code/llm/human/heuristic)
    direction="minimize",          # Optimization direction
    metadata={"model": "gpt-4o"}   # Additional metadata
)
```

### Creating Custom Evaluators

**Code-Based Metric**:
```python
from custom.evals import Score, create_evaluator

@create_evaluator(name="word_count", kind="code")
def word_count_metric(text: str, max_words: int) -> Score:
    """Check if text is within word limit."""
    count = len(text.split())
    within_limit = count <= max_words
    return Score(
        score=float(within_limit),
        label="valid" if within_limit else "too_long",
        explanation=f"Text has {count} words (max: {max_words})"
    )
```

**LLM-Based Evaluator**:
```python
from custom.evals.llm_evaluators import LLMEvaluator

class ToxicityEvaluator(LLMEvaluator):
    NAME = "toxicity"
    DIRECTION = "minimize"
    CHOICES = {"toxic": 1.0, "non_toxic": 0.0}
    PROMPT_TEMPLATE = """Evaluate if this text is toxic:

    <text>
    {text}
    </text>

    Is this text toxic or non-toxic?"""
```

## Batch Evaluation

```python
import pandas as pd
from custom.evals import exact_match

# Create dataset
df = pd.DataFrame({
    "prediction": ["Paris", "London", "Tokyo"],
    "ground_truth": ["Paris", "Paris", "Tokyo"]
})

# Evaluate
scores = []
for _, row in df.iterrows():
    score = exact_match({
        "output": row["prediction"],
        "expected": row["ground_truth"]
    })
    scores.append(score.score)

df["score"] = scores
print(f"Accuracy: {df['score'].mean():.2%}")
```

## Comparison with Phoenix Evals

| Feature | Phoenix Evals | Custom Evals (POC) |
|---------|--------------|-------------------|
| Code Metrics | 6+ | 3 (exact_match, sentiment, accuracy) |
| LLM Evaluators | 10+ | 3 (hallucination, correctness, relevance) |
| LLM Providers | OpenAI, Anthropic, Vertex, Bedrock, etc. | OpenAI, Anthropic |
| Async Support | ✓ | ✗ |
| Batch Processing | ✓ | Manual |
| Structured Output | ✓ | ✓ |
| Prompt Templates | Advanced (mustache/f-string) | Simple (f-string) |
| Tracing | OpenTelemetry | ✗ |

## Next Steps

- [ ] Add async support for LLM evaluators
- [ ] Add more LLM providers (Vertex AI, Bedrock, etc.)
- [ ] Implement rate limiting
- [ ] Add caching for LLM responses
- [ ] Add more evaluation metrics
- [ ] Add visualization tools
- [ ] Add OpenTelemetry tracing

## License

MIT
