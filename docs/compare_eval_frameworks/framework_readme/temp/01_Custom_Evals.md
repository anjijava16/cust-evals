# Custom-Evals: Lightweight Multi-Framework LLM Evaluation

**Type**: Python Library | **License**: MIT (Open Source) | **Year**: 2024

---

## Quick Overview

Custom-Evals is a modern, lightweight evaluation framework designed for **maximum flexibility** and **minimal dependencies**. It works seamlessly with 17+ agent frameworks and provides both code-based and LLM-based evaluators.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | Multi-framework support, flexibility |
| **Setup Time** | ⚡ 5 minutes |
| **Learning Curve** | Easy |
| **Dependencies** | Minimal |
| **Cost** | Free (OSS) + LLM API costs |
| **Best For** | Teams wanting maximum control |

---

## Key Strengths

### ✅ Advantages

1. **Lightweight Architecture**
   - Minimal dependencies
   - No required infrastructure
   - Works with any LLM provider
   - Optional tracing (not forced)

2. **Multi-Framework Support**
   - Works with 17+ agent frameworks
   - LangChain, LangGraph, LlamaIndex
   - OpenAI, Anthropic, Google
   - CrewAI, AWS, Microsoft frameworks

3. **Flexible Ground Truth**
   - Smart detection of reference data
   - Works with or without ground truth
   - Multiple field name support

4. **Dual Evaluation Modes**
   - **Code-based**: Exact match, sentiment, accuracy
   - **LLM-based**: Coherence, relevance, hallucination, faithfulness

5. **Production-Ready**
   - 150+ comprehensive tests
   - Type-safe with proper typing
   - Both sync and async support
   - Clean, Pythonic API

6. **Extensible**
   - Easy to add custom evaluators
   - Plugin architecture
   - No framework lock-in

### ⚠️ Limitations

1. **Newer Framework**
   - Smaller community compared to established tools
   - Less third-party integrations (growing)

2. **Manual Dataset Management**
   - No built-in dataset storage
   - User manages their own data

3. **Basic Visualization**
   - Relies on external tools for dashboards
   - No built-in UI (intentional design choice)

---

## vs Other Frameworks

### vs RAGAS
| Aspect | Custom-Evals | RAGAS |
|--------|--------------|-------|
| **Scope** | General + RAG | RAG-only |
| **Flexibility** | High | Medium |
| **Ground Truth** | Optional | Required for some metrics |
| **Multi-Framework** | ✅ 17+ | ⚠️ Limited |
| **Code Metrics** | ✅ Yes | ❌ No |

**Choose Custom-Evals if**: You need flexibility beyond RAG
**Choose RAGAS if**: You're 100% focused on RAG evaluation

---

### vs DeepEval
| Aspect | Custom-Evals | DeepEval |
|--------|--------------|----------|
| **Test Integration** | Manual | Pytest |
| **Dependencies** | Minimal | Moderate |
| **Flexibility** | Higher | Medium |
| **CI/CD** | Works well | Better integration |
| **Dashboard** | External | Built-in (optional) |

**Choose Custom-Evals if**: You want minimal overhead
**Choose DeepEval if**: You need tight pytest integration

---

### vs LangSmith
| Aspect | Custom-Evals | LangSmith |
|--------|--------------|-----------|
| **Infrastructure** | None | Cloud platform |
| **Cost** | LLM only | Platform + LLM |
| **Observability** | Optional (Phoenix) | Built-in |
| **Data Storage** | User-managed | Cloud |
| **Vendor Lock-in** | None | LangSmith account |

**Choose Custom-Evals if**: You want control and portability
**Choose LangSmith if**: You're using LangChain and want full observability

---

### vs Phoenix Evals
| Aspect | Custom-Evals | Phoenix |
|--------|--------------|---------|
| **Server Required** | No | Yes (for UI) |
| **Tracing** | Optional | Core feature |
| **Setup** | Simpler | More complex |
| **Observability** | Basic | Excellent |
| **Dependencies** | Fewer | More |

**Choose Custom-Evals if**: You want lightweight without server
**Choose Phoenix if**: Observability is critical

---

## When to Choose Custom-Evals

### ✅ Perfect For

1. **Multi-Framework Environments**
   - Using multiple agent frameworks
   - Need consistent evaluation across different systems
   - Want framework-agnostic evaluation

2. **Research & Experimentation**
   - Rapid prototyping
   - Custom evaluation criteria
   - No vendor lock-in needed

3. **Minimal Dependencies**
   - Containerized deployments
   - Edge computing
   - Resource-constrained environments

4. **Maximum Control**
   - Custom evaluation logic
   - Own dataset management
   - Full control over infrastructure

5. **Startups & Small Teams**
   - Fast iteration
   - Low overhead
   - Easy to understand and extend

### ❌ Not Ideal For

1. **Need Built-in Dashboard**
   - Custom-Evals doesn't provide UI
   - Use Phoenix, LangSmith, or Langfuse instead

2. **Heavy LangChain Integration**
   - LangSmith is better integrated
   - Though Custom-Evals still works well

3. **Enterprise Observability**
   - Need comprehensive production monitoring
   - Consider Langfuse or LangSmith

---

## Pricing

### Cost Breakdown

| Component | Cost |
|-----------|------|
| **Framework** | 💰 **Free** (MIT License) |
| **LLM API** | Pay per evaluation (~$0.001-0.01 each) |
| **Infrastructure** | None required |
| **Support** | Community (GitHub) |

### Typical Monthly Costs

| Evaluations/Month | Estimated Cost |
|-------------------|----------------|
| 1,000 | $1-10 |
| 10,000 | $10-100 |
| 100,000 | $100-1,000 |
| 1,000,000 | $1,000-10,000 |

**Note**: Costs depend on LLM provider (OpenAI, Anthropic) and model choice (mini vs full)

---

## Quick Start

### Installation

```bash
# Basic installation
pip install custom-evals

# With LLM support (recommended)
pip install custom-evals[dev]

# With tracing (optional)
pip install custom-evals[dev,tracing]
```

### 5-Minute Example

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

# Initialize LLM
llm = LLM(provider="openai", model="gpt-4o-mini")

# Create evaluators
coherence = CoherenceEvaluator(llm)
relevance = RelevanceEvaluator(llm)

# Evaluate
response = "Paris is the capital of France."
query = "What is the capital of France?"

coherence_score = coherence.evaluate({
    "output": response
})

relevance_score = relevance.evaluate({
    "input": query,
    "output": response
})

print(f"Coherence: {coherence_score.label} ({coherence_score.score})")
print(f"Relevance: {relevance_score.label} ({relevance_score.score})")
```

---

## Architecture Highlights

### Design Principles

1. **Minimal Dependencies**: Only essential libraries
2. **Optional Everything**: Tracing, observability all opt-in
3. **Framework Agnostic**: Works with any LLM framework
4. **Extensible**: Easy to add custom evaluators
5. **Type Safe**: Full type hints throughout

### Key Components

```
custom.evals/
├── evaluators.py          # Base classes
├── llm_evaluators.py      # LLM-based evaluators
├── llm/
│   └── wrapper.py         # LLM provider abstraction
├── metrics/
│   ├── exact_match.py     # Code-based metrics
│   ├── sentiment.py
│   └── accuracy.py
└── tracing.py             # Optional OpenTelemetry
```

---

## Comparison Summary

### Unique Advantages
1. ⚡ Lightest weight framework
2. 🔧 Maximum flexibility
3. 🎯 Multi-framework support (17+)
4. 🚀 No infrastructure required
5. 🔓 Zero vendor lock-in
6. 📦 Minimal dependencies

### Trade-offs
1. Manual dataset management
2. No built-in dashboard
3. Smaller community
4. Less hand-holding

---

## Migration Path

### From RAGAS
```python
# RAGAS
from ragas import evaluate
results = evaluate(dataset, metrics=[faithfulness])

# Custom-Evals
from custom.evals import FaithfulnessEvaluator
evaluator = FaithfulnessEvaluator(llm)
score = evaluator.evaluate({"input": q, "output": a, "context": ctx})
```

### From DeepEval
```python
# DeepEval
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
metric = AnswerRelevancyMetric()
metric.measure(test_case)

# Custom-Evals
from custom.evals import AnswerRelevancyEvaluator
evaluator = AnswerRelevancyEvaluator(llm)
score = evaluator.evaluate({"input": input, "output": output})
```

---

## Resources

### Documentation
- **Main Docs**: [README.md](../../README.md)
- **Quick Start**: [guides/QUICKSTART.md](../../guides/QUICKSTART.md)
- **Deep Dive**: [framework_readme/01_Custom_Evals_README.md](framework_readme/01_Custom_Evals_README.md)

### Examples
- Basic Usage: `examples/basic_usage.py`
- LLM Evaluation: `examples/llm_evaluation.py`
- RAG Evaluation: `examples/rag_evaluation.py`
- Agent Evaluation: `examples/*_agent_example.py`

### Community
- **GitHub**: [Your Repository]
- **Issues**: [GitHub Issues]
- **Discussions**: [GitHub Discussions]

---

## Verdict

**Custom-Evals is the best choice for teams wanting maximum flexibility, minimal dependencies, and multi-framework support without vendor lock-in.**

**Rating**: ⭐⭐⭐⭐⭐ (5/5 for flexibility)

### Choose Custom-Evals if you value:
- ✅ Lightweight architecture
- ✅ Framework flexibility
- ✅ No vendor lock-in
- ✅ Easy customization
- ✅ Minimal overhead

### Choose alternatives if you need:
- ❌ Built-in dashboard → Phoenix, LangSmith
- ❌ Heavy LangChain integration → LangSmith
- ❌ Pytest integration → DeepEval
- ❌ RAG-only focus → RAGAS

---

**Next**: [Read the Deep Dive](framework_readme/01_Custom_Evals_README.md) | [Compare All Frameworks](Compare_All_Eval_Frameworks.md)
