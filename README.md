# Custom Evals - Multi-Framework LLM Evaluation

A lightweight, comprehensive evaluation framework for LLM outputs with support for **17+ agent frameworks** and multi-framework evaluation patterns.

**🔥 NEW: 17+ Agent Framework Integrations with Custom-Evals!**

---

## ⚡ Quick Start

### Installation

```bash
# Basic installation
pip install -e .

# With LLM support (recommended)
pip install -e ".[dev]"

# With Phoenix tracing (optional)
pip install -e ".[dev,tracing]"
```

### 30-Second Example

```python
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM

# Initialize LLM and evaluator
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(llm)

# Evaluate output
score = evaluator.evaluate({
    "input": "What is AI?",
    "output": "AI is artificial intelligence, enabling machines to perform intelligent tasks."
})

print(f"{score.label}: {score.explanation}")
# Output: coherent: The response provides a clear, logical explanation...
```

---

## 📚 Documentation

### 🚀 Getting Started

- **[Quick Start Guide](guides/QUICKSTART.md)** - Get up and running in 5 minutes
- **[Agents & RAG Quick Start](guides/AGENTS_RAG_QUICKSTART.md)** - Agent and RAG integration guide
- **[Practical Examples Guide](guides/PRACTICAL_EXAMPLES_GUIDE.md)** - Production-ready examples

### 📖 User Guides

- **[LLM Integration Guide](guides/LLM_GUIDE.md)** - OpenAI, Anthropic, and other providers
- **[Ground Truth Guide](guides/GROUND_TRUTH_GUIDE.md)** - Flexible ground truth handling
- **[Tracing Guide](guides/TRACING_GUIDE.md)** - Optional Phoenix tracing with OpenTelemetry
- **[Non-LLM Evaluation Guide](docs/NON_LLM_EVALUATION_GUIDE.md)** - AWS Textract, OCR, and document extraction (NEW)
- **[Textract Quick Start](docs/TEXTRACT_QUICKSTART.md)** - Get started with AWS Textract in 5 minutes (NEW)

### 🔍 Reference Documentation

- **[Architecture](reference/ARCHITECTURE.md)** - System design and core concepts
- **[Framework Comparison](reference/FRAMEWORK_COMPARISON.md)** - Compare with RAGAS, DeepEval, Phoenix
- **[Framework Support](reference/FRAMEWORK_SUPPORT.md)** - Multi-framework evaluation patterns
- **[Project Overview](reference/PROJECT_OVERVIEW.md)** - Complete project structure
- **[Documentation Index](reference/INDEX.md)** - Full documentation index

### 🤖 Agent Frameworks (17+ Integrations)

**[📦 Framework Index →](docs/FRAMEWORK_INDEX.md)** - Complete list of all supported frameworks

#### Cloud Platform Frameworks
- **[AWS Strands Agents](docs/frameworks/aws-strands.md)** - AWS Bedrock + Claude
- **[Google ADK](docs/frameworks/google-adk.md)** - Gemini models
- **[Databricks Agent Bricks](docs/frameworks/databricks-agent-bricks.md)** - MLflow integration

#### Microsoft Ecosystem
- **[Microsoft Agent Framework](docs/frameworks/microsoft-agent-framework.md)** - Enterprise agents
- **[Semantic Kernel](docs/frameworks/semantic-kernel.md)** - Plugin system
- **[Autogen](docs/frameworks/autogen.md)** - Multi-agent conversations

#### LangChain & LlamaIndex
- **[LangGraph](docs/frameworks/langgraph.md)** - Stateful workflows
- **[LlamaIndex Workflows](docs/frameworks/llamaindex-workflows.md)** - Event-driven agents
- **[LangChain RAG](docs/frameworks/langchain-rag.md)** - RAG applications
- **[LlamaIndex RAG](docs/frameworks/llamaindex-rag.md)** - Data indexing

#### OpenAI Frameworks
- **[OpenAI Agents Framework](docs/frameworks/openai-agents-framework.md)** - Official patterns
- **[OpenAI Agents SDK](docs/frameworks/openai-agents.md)** - Function calling
- **[OpenAI Assistants](docs/frameworks/openai-assistants.md)** - Persistent threads
- **[OpenAI Swarm](docs/frameworks/openai-swarm.md)** - Lightweight multi-agent

#### Other Frameworks
- **[Agno](docs/frameworks/agno.md)** - Multi-agent systems at scale
- **[CrewAI](docs/frameworks/crewai.md)** - Role-based agents
- **[Pydantic AI](docs/frameworks/pydanticai.md)** - Type-safe agents

---

## 🎯 Key Features

### Evaluators

**Code-Based Metrics:**
- **Exact Match** - Binary comparison
- **Sentiment Score** - Sentiment analysis
- **Custom Accuracy** - Flexible accuracy with normalization

**OCR/Document Extraction Metrics:** (NEW - for non-LLM services like AWS Textract)
- **Text Extraction Accuracy** - Fuzzy string matching
- **Character Error Rate (CER)** - Character-level accuracy
- **Word Error Rate (WER)** - Word-level accuracy
- **Bounding Box IoU** - Spatial accuracy for OCR
- **Confidence Threshold** - Quality gating
- **Field Detection Accuracy** - Form field detection (F1 score)

**LLM-Based Evaluators:**
- **Coherence** - Logical flow and consistency
- **Relevance** - Context-query relevance
- **Correctness** - Factual accuracy
- **Hallucination** - Detect hallucinations
- **Toxicity** - Harmful content detection
- **Faithfulness** (RAG) - Grounding in context
- **Answer Relevancy** (RAG) - Answer-query relevance

### Supported LLM Providers

```python
from custom.evals.llm import LLM

# OpenAI
llm = LLM(provider="openai", model="gpt-4o-mini")

# Anthropic
llm = LLM(provider="anthropic", model="claude-3-haiku-20240307")
```

### Multi-Framework Support

- **✅ RAGAS** - RAG evaluation metrics (Faithfulness, Answer Relevancy)
- **✅ DeepEval** - Comprehensive LLM evaluation patterns
- **✅ Phoenix Evals** - API patterns + optional OpenTelemetry tracing

---

## 📊 Agent Framework Integration

Custom Evals integrates with **17+ agent frameworks** for comprehensive evaluation:

### Example: Evaluate Any Agent

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

# Initialize evaluators
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
coherence = CoherenceEvaluator(eval_llm)
relevance = RelevanceEvaluator(eval_llm)

# Run your agent (any framework)
query = "What is machine learning?"
response = your_agent.run(query)  # LangChain, CrewAI, OpenAI, etc.

# Evaluate
coherence_score = coherence.evaluate({"input": query, "output": response})
relevance_score = relevance.evaluate({"input": query, "output": response})

print(f"Coherence: {coherence_score.label} ({coherence_score.score:.2f})")
print(f"Relevance: {relevance_score.label} ({relevance_score.score:.2f})")
```

**See [Framework Index](docs/FRAMEWORK_INDEX.md) for all 17+ supported frameworks!**

---

## 🔬 Examples

### Quick Examples

```bash
# Code-based metrics
python examples/basic_usage.py

# LLM-based evaluators
export OPENAI_API_KEY="your-key"
python examples/llm_evaluation.py

# RAG evaluation
python examples/rag_evaluation.py

# AWS Textract/OCR evaluation (NEW)
python examples/textract_evaluation_example.py
```

### Production-Ready Agent Examples

**22 test suites, 2,700+ lines of code:**

```bash
# LangGraph Agent - Stateful workflow
python examples/langgraph_agent_example.py

# LangChain Agent - ReAct pattern
python examples/langchain_agent_example.py

# Multi-Agent System - 4 specialized agents
python examples/multi_agent_example.py

# RAG System - LangChain + Qdrant
python examples/rag_langchain_qdrant.py
```

**Full documentation: [Practical Examples Guide](guides/PRACTICAL_EXAMPLES_GUIDE.md)**

---

## 🏗️ Project Structure

```
cust-evals/
├── README.md                   # 👈 You are here
│
├── guides/                     # 📖 User guides
│   ├── QUICKSTART.md
│   ├── AGENTS_RAG_QUICKSTART.md
│   ├── LLM_GUIDE.md
│   ├── GROUND_TRUTH_GUIDE.md
│   ├── TRACING_GUIDE.md
│   └── PRACTICAL_EXAMPLES_GUIDE.md
│
├── reference/                  # 📚 Technical reference
│   ├── ARCHITECTURE.md
│   ├── FRAMEWORK_COMPARISON.md
│   ├── FRAMEWORK_SUPPORT.md
│   ├── PROJECT_OVERVIEW.md
│   └── INDEX.md
│
├── docs/                       # 📦 Complete documentation
│   ├── FRAMEWORK_INDEX.md     # Index of all 17+ frameworks
│   ├── frameworks/            # Individual framework guides
│   │   ├── aws-strands.md
│   │   ├── google-adk.md
│   │   ├── langgraph.md
│   │   ├── semantic-kernel.md
│   │   └── ... (12+ more)
│   ├── getting-started.md
│   ├── examples.md
│   ├── api-reference.md
│   └── evaluators/
│       ├── code-based.md
│       ├── llm-based.md
│       └── rag-specific.md
│
├── src/custom/evals/          # 🔧 Core library
│   ├── evaluators.py
│   ├── llm_evaluators.py
│   ├── llm/
│   │   └── wrapper.py
│   └── metrics/
│
├── examples/                   # 💡 Working examples
│   ├── basic_usage.py
│   ├── llm_evaluation.py
│   ├── langgraph_agent_example.py
│   ├── aws_strands_agents_example.py
│   ├── google_adk_example.py
│   └── ... (20+ examples)
│
└── tests/                      # ✅ Test suite (150+ tests)
```

---

## 🎓 Core Concepts

### Score Object

All evaluators return a standardized `Score`:

```python
Score(
    score=0.85,                    # Numeric score (0.0-1.0)
    name="coherence",              # Metric name
    label="coherent",              # Categorical label
    explanation="...",             # Human-readable explanation
    kind="llm",                    # Evaluator type
    direction="maximize",          # Optimization direction
    metadata={}                    # Additional metadata
)
```

### Quality Thresholds

Standard thresholds across all frameworks:

```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,    # Minimum coherence score
    "relevance": 0.7,    # Minimum relevance score
    "correctness": 0.7,  # Minimum correctness score
    "toxicity": 0.2      # Maximum toxicity (lower is better)
}
```

---

## 🔥 Optional: Phoenix Tracing

**Tracing is completely optional.** The framework works perfectly without it.

```python
# WITHOUT tracing (default)
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(llm)
score = evaluator.evaluate({...})  # Works perfectly!

# WITH tracing (optional, for observability)
from custom.evals import initialize_tracing
initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")
score = evaluator.evaluate({...})  # Now traced in Phoenix UI!
```

**[📖 Tracing Guide →](guides/TRACING_GUIDE.md)**

---

## 📖 Full Documentation

### MkDocs Site

```bash
mkdocs serve
# Visit: http://127.0.0.1:8000
```

### Documentation Links

- **User Guides**: [`guides/`](guides/)
- **Reference**: [`reference/`](reference/)
- **Agent Frameworks**: [`docs/frameworks/`](docs/frameworks/)
- **Complete Docs**: [`docs/`](docs/)

---

## 🤝 Contributing

See **[Contributing Guide](docs/contributing.md)**

---

## 📝 License

MIT

---

## 🔗 Quick Links

| Category | Link |
|----------|------|
| **Quick Start** | [guides/QUICKSTART.md](guides/QUICKSTART.md) |
| **Agent Frameworks** | [docs/FRAMEWORK_INDEX.md](docs/FRAMEWORK_INDEX.md) |
| **Examples** | [guides/PRACTICAL_EXAMPLES_GUIDE.md](guides/PRACTICAL_EXAMPLES_GUIDE.md) |
| **Architecture** | [reference/ARCHITECTURE.md](reference/ARCHITECTURE.md) |
| **API Reference** | [docs/api-reference.md](docs/api-reference.md) |
| **MkDocs Site** | `mkdocs serve` |

---

**Total Agent Frameworks**: 17+
**Total Examples**: 20+ working examples
**Total Tests**: 150+ comprehensive tests
**Documentation**: 300KB+ comprehensive guides

**Ready to evaluate your LLM outputs? [Get Started →](guides/QUICKSTART.md)**
