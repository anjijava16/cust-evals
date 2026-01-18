# Multi-Framework Support

Custom Evals is designed to handle evaluation patterns from **three major frameworks**: RAGAS, DeepEval, and Phoenix Evals.

## 🎯 Framework Coverage Overview

| Framework | Focus | Our Support | Tracing | Status |
|-----------|-------|-------------|---------|--------|
| **RAGAS** | RAG evaluation | ✅ Core metrics | - | Phase 1 Complete |
| **DeepEval** | Comprehensive LLM eval | ✅ Key metrics | - | Phase 1 Complete |
| **Phoenix Evals** | Production eval + observability | ✅ API patterns | ✅ OpenTelemetry | Integrated |

---

## 1. RAGAS Support

### What We Support (Phase 1 ✅)

| RAGAS Metric | Custom Evals | Status | Notes |
|--------------|--------------|--------|-------|
| **Faithfulness** | `FaithfulnessEvaluator` | ✅ | Statement-level verification |
| **Answer Relevancy** | `AnswerRelevancyEvaluator` | ✅ | Query-answer alignment |
| **Context Precision** | - | 🚧 Phase 2 | Planned |
| **Context Recall** | - | 🚧 Phase 2 | Planned |

### Usage Example

```python
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")

# RAGAS-style Faithfulness
faithfulness = FaithfulnessEvaluator(llm)
score = faithfulness.evaluate({
    "input": "What is the capital?",
    "output": "Paris is the capital of France.",
    "context": "Paris is the capital of France."
})

# RAGAS-style Answer Relevancy
relevancy = AnswerRelevancyEvaluator(llm)
score = relevancy.evaluate({
    "input": "What is the capital?",
    "output": "Paris is the capital of France."
})
```

### Key Features from RAGAS

✅ **Reference-free evaluation** - No ground truth needed
✅ **Statement-level analysis** - Breaks down responses
✅ **Research-backed** - Based on RAGAS concepts
✅ **RAG-optimized** - Specifically for RAG systems

---

## 2. DeepEval Support

### What We Support (Phase 1 ✅)

| DeepEval Metric | Custom Evals | Status | Notes |
|-----------------|--------------|--------|-------|
| **Faithfulness** | `FaithfulnessEvaluator` | ✅ | RAG grounding check |
| **Answer Relevancy** | `AnswerRelevancyEvaluator` | ✅ | Query relevance |
| **Hallucination** | `HallucinationEvaluator` | ✅ | Context-based detection |
| **Correctness** | `CorrectnessEvaluator` | ✅ | GT comparison |
| **Context Precision** | - | 🚧 Phase 2 | Planned |
| **Context Recall** | - | 🚧 Phase 2 | Planned |
| **Context Relevancy** | - | 🚧 Phase 2 | Planned |
| **Bias** | - | 🚧 Phase 3 | Planned |
| **Toxicity** | - | 🚧 Phase 3 | Planned |
| **G-Eval** | - | 🚧 Phase 4 | Future |

**DeepEval has 50+ metrics** - We support the most common RAG and general evaluation metrics.

### Usage Example

```python
from custom.evals import (
    FaithfulnessEvaluator,
    HallucinationEvaluator,
    CorrectnessEvaluator
)
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")

# DeepEval-style Faithfulness
faithfulness = FaithfulnessEvaluator(llm)
score = faithfulness.evaluate({...})

# DeepEval-style Hallucination
hallucination = HallucinationEvaluator(llm)
score = hallucination.evaluate({...})

# DeepEval-style Correctness
correctness = CorrectnessEvaluator(llm)
score = correctness.evaluate({
    "input": "What is 2+2?",
    "output": "4",
    "expected": "4"
})
```

### Key Features from DeepEval

✅ **Comprehensive metrics** - RAG + general evaluation
✅ **LLM-as-judge** - Uses LLMs for evaluation
✅ **Flexible ground truth** - Works with/without
✅ **Binary + scored** - Returns both label and score

---

## 3. Phoenix Evals Support

### What We Support ✅

| Phoenix Feature | Custom Evals | Status | Notes |
|-----------------|--------------|--------|-------|
| **Two-layer API** | `evaluate()` / `_evaluate()` | ✅ | Same pattern |
| **Async support** | `async_evaluate()` | ✅ | Thread pool default |
| **describe() method** | `describe()` | ✅ | Introspection |
| **Ground truth flexibility** | Flexible GT | ✅ | Multiple field names |
| **Score object** | `Score` dataclass | ✅ | Compatible structure |
| **OpenTelemetry tracing** | ✅ Via `tracing.py` | ✅ | **NEW!** |
| **Pydantic validation** | Basic validation | ⚠️ | Simpler than Phoenix |

### Usage Example

```python
from custom.evals import HallucinationEvaluator, initialize_tracing
from custom.evals.llm import LLM

# Phoenix-style tracing (NEW!)
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces"
)

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

# Phoenix-style API
score = evaluator.evaluate({...})  # Traced!

# Phoenix-style async
score = await evaluator.async_evaluate({...})

# Phoenix-style introspection
description = evaluator.describe()
```

### Key Features from Phoenix

✅ **Two-layer API** - Clean separation of public/internal
✅ **Async evaluation** - Concurrent processing
✅ **OpenTelemetry tracing** - **Same as Phoenix!**
✅ **describe() introspection** - Runtime metadata
✅ **Score standardization** - Consistent return type

---

## 🔥 NEW: Phoenix Tracing Integration

### What Is It?

Custom Evals now **integrates with Phoenix (Arize)** using OpenTelemetry for distributed tracing.

**Same tracing as Phoenix Evals!**

### Quick Start

```python
# 1. Install tracing dependencies
pip install -e ".[tracing]"

# 2. Start Phoenix
python -m phoenix.server.main serve

# 3. Initialize tracing
from custom.evals import initialize_tracing

initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces"
)

# 4. All evaluations are now traced!
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

score = evaluator.evaluate({...})  # Automatically traced in Phoenix!
```

### What Gets Traced

Every evaluation sends a span to Phoenix with:
- Evaluator name, type, direction
- LLM model and provider
- Ground truth availability
- Result label and score
- Timing information

**View in Phoenix UI:** http://localhost:6006

### Benefits

- 📊 **Visualize** evaluation flows
- 🔍 **Debug** issues
- ⏱️ **Monitor** performance
- 📈 **Analyze** patterns
- 🎯 **Track** usage

See **[TRACING_GUIDE.md](TRACING_GUIDE.md)** for complete documentation.

---

## 📊 Complete Metrics Comparison

### Current Support (Phase 1)

| Metric | Type | RAGAS | DeepEval | Phoenix | Our Status |
|--------|------|-------|----------|---------|-----------|
| **Faithfulness** | RAG | ✅ | ✅ | ✅ | ✅ Implemented |
| **Answer Relevancy** | RAG | ✅ | ✅ | ✅ | ✅ Implemented |
| **Hallucination** | General | - | ✅ | ✅ | ✅ Implemented |
| **Correctness** | General | - | ✅ | ✅ | ✅ Implemented |
| **Relevance** | General | - | - | ✅ | ✅ Implemented |
| **Coherence** | General | - | - | ✅ | ✅ Implemented |
| **Exact Match** | Code | - | - | ✅ | ✅ Implemented |
| **Sentiment** | Code | - | - | - | ✅ Implemented |
| **Custom Accuracy** | Code | - | - | - | ✅ Implemented |

**Total: 9 evaluators** (3 code-based, 6 LLM-based)

### Planned Support (Future Phases)

**Phase 2: Context Evaluation** 🚧
- Context Precision (RAGAS, DeepEval)
- Context Recall (RAGAS, DeepEval)
- Context Relevancy (DeepEval)

**Phase 3: Safety Metrics** 🚧
- Bias Detection (DeepEval)
- Toxicity Detection (DeepEval)

**Phase 4: Advanced** 🔮
- G-Eval custom metrics (DeepEval)
- Multi-turn conversation (DeepEval)
- Agentic metrics (DeepEval)

---

## 🎯 Usage Patterns

### Pattern 1: RAGAS-style RAG Evaluation

```python
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")

# Core RAGAS metrics
faithfulness = FaithfulnessEvaluator(llm)
relevancy = AnswerRelevancyEvaluator(llm)

# Evaluate RAG response
rag_input = {
    "input": query,
    "output": generated_answer,
    "context": retrieved_context
}

faith_score = faithfulness.evaluate(rag_input)
rel_score = relevancy.evaluate(rag_input)

print(f"Faithfulness: {faith_score.label} ({faith_score.score})")
print(f"Relevancy: {rel_score.label} ({rel_score.score})")
```

### Pattern 2: DeepEval-style Comprehensive Evaluation

```python
from custom.evals import (
    FaithfulnessEvaluator,
    HallucinationEvaluator,
    AnswerRelevancyEvaluator,
    CoherenceEvaluator
)

# Multiple DeepEval-inspired evaluators
evaluators = {
    "faithfulness": FaithfulnessEvaluator(llm),
    "hallucination": HallucinationEvaluator(llm),
    "relevancy": AnswerRelevancyEvaluator(llm),
    "coherence": CoherenceEvaluator(llm)
}

# Run all evaluations
results = {}
for name, evaluator in evaluators.items():
    score = evaluator.evaluate(eval_input)
    results[name] = {"label": score.label, "score": score.score}
```

### Pattern 3: Phoenix-style with Tracing

```python
from custom.evals import initialize_tracing, HallucinationEvaluator
from custom.evals.llm import LLM

# Enable Phoenix tracing
initialize_tracing(
    service_name="my-rag-app",
    phoenix_endpoint="http://localhost:6006/v1/traces"
)

# Phoenix-style evaluation (automatically traced)
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

score = evaluator.evaluate(eval_input)

# View traces in Phoenix UI
# http://localhost:6006
```

---

## 🏗️ Architecture Alignment

### Common Patterns Across All Frameworks

✅ **LLM-as-judge** - Use LLMs to evaluate LLM outputs
✅ **Reference-free** - Evaluate without ground truth when possible
✅ **Structured output** - JSON schema for consistency
✅ **Flexible input** - Multiple field name support
✅ **Async support** - Concurrent evaluation
✅ **Observability** - Tracing and monitoring

### What Makes Each Unique

**RAGAS:**
- RAG-specific focus
- Research-backed formulas
- Simple, core metrics

**DeepEval:**
- Comprehensive metric library (50+)
- G-Eval framework
- Safety and agentic metrics

**Phoenix Evals:**
- Production-grade
- OpenTelemetry integration
- Tight Phoenix (Arize) integration

**Custom Evals:**
- Combines best of all three
- Phoenix tracing ✅
- Simple POC architecture
- Easy to extend

---

## 📈 Roadmap

### ✅ Phase 1 Complete (Current)

- Core RAG metrics (Faithfulness, Answer Relevancy)
- General evaluation (Hallucination, Correctness, Relevance, Coherence)
- Code-based metrics (Exact Match, Sentiment, Accuracy)
- Phoenix tracing integration 🔥
- Comprehensive documentation

### 🚧 Phase 2 (Next)

- Context Precision evaluator
- Context Recall evaluator
- Context Relevancy evaluator
- Enhanced tracing attributes

### 🚧 Phase 3 (Future)

- Bias detection
- Toxicity detection
- Summarization quality
- More safety metrics

### 🔮 Phase 4 (Long-term)

- G-Eval framework for custom metrics
- Multi-turn conversation evaluation
- Agentic task evaluation
- Advanced Phoenix integrations

---

## 🎓 Learn More

**Documentation:**
- [Getting Started](docs/getting-started.md)
- [Framework Comparison](FRAMEWORK_COMPARISON.md)
- [Tracing Guide](TRACING_GUIDE.md) 🔥
- [RAG Evaluators](docs/evaluators/rag-specific.md)

**Examples:**
- [Basic Usage](examples/basic_usage.py)
- [RAG Evaluation](examples/rag_evaluation.py)
- [Tracing Example](examples/tracing_example.py) 🔥

**External Resources:**
- [RAGAS Documentation](https://docs.ragas.io/)
- [DeepEval Documentation](https://deepeval.com/)
- [Phoenix Documentation](https://docs.arize.com/phoenix)

---

## ✅ Summary

**Custom Evals handles evaluations from all three major frameworks:**

1. ✅ **RAGAS** - RAG evaluation metrics (Faithfulness, Answer Relevancy)
2. ✅ **DeepEval** - Comprehensive LLM evaluation (key metrics)
3. ✅ **Phoenix Evals** - API patterns + OpenTelemetry tracing 🔥

**Key Features:**
- 9 evaluators (Phase 1)
- Phoenix tracing integration 🔥
- Reference-free evaluation
- Flexible ground truth
- Async support
- Comprehensive docs

**Future:**
- Extending to 15+ evaluators
- More RAGAS metrics
- More DeepEval metrics
- Enhanced Phoenix integration

**Your framework is ready to handle all three evaluation paradigms! 🎉**
