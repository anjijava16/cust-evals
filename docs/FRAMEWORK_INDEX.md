# Framework Documentation Index

Complete documentation for all agent and RAG frameworks with custom-evals integration.

---

## 📚 Agent Frameworks

### Core Frameworks

1. **[LangChain ReAct Agent](../examples/langchain_agent_example.py)**
   - Tool-based reasoning with ReAct pattern
   - Multiple tools: database, time, calculator, products, weather
   - 6 test suites with comprehensive evaluation
   - **File**: `examples/langchain_agent_example.py`

2. **[LangGraph Stateful Agent](../examples/langgraph_agent_example.py)**
   - Graph-based stateful workflows
   - Conditional edges and tool integration
   - Message history management
   - **File**: `examples/langgraph_agent_example.py`

3. **[Multi-Agent System](../examples/multi_agent_example.py)**
   - 4 specialized agents (Research, Analysis, Writer, Reviewer)
   - Orchestrated workflow with collaboration
   - Information flow tracking
   - **File**: `examples/multi_agent_example.py`

4. **[Google Vertex AI Agents](../examples/google_vertex_agent_example.py)**
   - Gemini 1.5 Flash with function calling
   - Multi-agent routing system
   - Customer service, technical support, sales agents
   - **File**: `examples/google_vertex_agent_example.py`

### Additional Frameworks

5. **[Autogen (Microsoft)](frameworks/autogen.md)** ⭐
   - Multi-agent conversations
   - Code execution capabilities
   - Group chat management
   - **File**: `examples/autogen_agent_example.py`
   - **Docs**: `docs/frameworks/autogen.md`

6. **[CrewAI](frameworks/crewai.md)** ⭐
   - Role-based agent orchestration
   - Sequential and hierarchical processes
   - Task dependencies
   - **File**: `examples/crewai_agent_example.py`
   - **Docs**: `docs/frameworks/crewai.md`

7. **[OpenAI Assistants API](../examples/openai_assistants_example.py)**
   - Official OpenAI SDK for agents
   - Persistent conversation threads
   - Function calling and code interpreter
   - **File**: `examples/openai_assistants_example.py`

8. **[OpenAI Swarm](../examples/openai_swarm_agent_example.py)** 🆕
   - Lightweight multi-agent orchestration
   - Native agent handoffs
   - Context passing between agents
   - **File**: `examples/openai_swarm_agent_example.py`

9. **[PydanticAI](../examples/pydanticai_agent_example.py)**
   - Type-safe agent development
   - Structured outputs with Pydantic models
   - Tool calling with validation
   - **File**: `examples/pydanticai_agent_example.py`

---

## 🔍 RAG Frameworks

### 10. **LangChain + Qdrant RAG**
   - PDF processing and text extraction
   - OpenAI embeddings with Qdrant vector DB
   - RetrievalQA chain
   - RAG-specific evaluation (Faithfulness, Answer Relevancy)
   - **File**: `examples/rag_langchain_qdrant.py`

### 11. **LlamaIndex + Qdrant RAG**
   - Multi-format document loading
   - SentenceSplitter for chunking
   - Query engine with response synthesis
   - Multi-document reasoning
   - **File**: `examples/rag_llamaindex_qdrant.py`

---

## 📖 Complete Documentation

### Guides

- **[Agents & RAG Guide](AGENTS_AND_RAG_GUIDE.md)** (22KB)
  - Original 6 frameworks
  - Complete code examples
  - Architecture diagrams
  - Best practices

- **[Additional Agent Frameworks](ADDITIONAL_AGENT_FRAMEWORKS.md)** (18KB)
  - 5 additional frameworks
  - Quick comparison table
  - Installation instructions

- **[Quick Start Guide](../AGENTS_RAG_QUICKSTART.md)** (7.7KB)
  - Quick reference
  - Installation steps
  - Basic examples

- **[Examples Summary](../EXAMPLES_SUMMARY.md)** (14KB)
  - Complete overview
  - Statistics and metrics

- **[Final Complete Summary](../FINAL_COMPLETE_SUMMARY.md)** (11KB)
  - Project overview
  - All frameworks
  - Installation guide

### Framework-Specific Docs

- **[Autogen Documentation](frameworks/autogen.md)** ⭐
- **[CrewAI Documentation](frameworks/crewai.md)** ⭐

---

## 🚀 Quick Start by Framework

### Autogen (Microsoft)

```bash
pip install pyautogen
export OPENAI_API_KEY="your-key"
python examples/autogen_agent_example.py
```

**Best For**: Multi-agent conversations, code execution, research

---

### CrewAI

```bash
pip install crewai
export OPENAI_API_KEY="your-key"
python examples/crewai_agent_example.py
```

**Best For**: Content creation, business workflows, sequential tasks

---

### OpenAI Swarm

```bash
pip install git+https://github.com/openai/swarm.git
export OPENAI_API_KEY="your-key"
python examples/openai_swarm_agent_example.py
```

**Best For**: Agent routing, lightweight coordination, customer service

---

### OpenAI Assistants API

```bash
pip install openai>=1.0.0
export OPENAI_API_KEY="your-key"
python examples/openai_assistants_example.py
```

**Best For**: Production chatbots, persistent threads, official support

---

### PydanticAI

```bash
pip install pydantic-ai pydantic>=2.0
export OPENAI_API_KEY="your-key"
python examples/pydanticai_agent_example.py
```

**Best For**: Type-safe development, structured outputs, production apps

---

### LangChain RAG

```bash
pip install langchain langchain-openai qdrant-client pypdf reportlab
export OPENAI_API_KEY="your-key"
python examples/rag_langchain_qdrant.py
```

**Best For**: PDF + vector DB RAG, document Q&A

---

### LlamaIndex RAG

```bash
pip install llama-index llama-index-vector-stores-qdrant llama-index-embeddings-openai
export OPENAI_API_KEY="your-key"
python examples/rag_llamaindex_qdrant.py
```

**Best For**: Multi-document reasoning, advanced RAG

---

## 📊 Framework Comparison

| Framework | Type | Multi-Agent | Tools | Structured Output | Learning Curve |
|-----------|------|-------------|-------|-------------------|----------------|
| LangChain | Agent | Custom | ✅ | ❌ | Medium |
| LangGraph | Agent | Custom | ✅ | ❌ | Medium |
| Multi-Agent | System | ✅ | ✅ | ❌ | High |
| Vertex AI | Agent | Routing | ✅ | ❌ | Medium |
| **Autogen** | **Agent** | **✅** | **✅** | **❌** | **Medium** |
| **CrewAI** | **Agent** | **✅** | **⚠️** | **❌** | **Low** |
| **Assistants** | **Agent** | **❌** | **✅** | **❌** | **Low** |
| **Swarm** | **Agent** | **✅** | **✅** | **❌** | **Very Low** |
| **PydanticAI** | **Agent** | **Custom** | **✅** | **✅** | **Medium** |
| LangChain RAG | RAG | N/A | N/A | N/A | Medium |
| LlamaIndex RAG | RAG | N/A | N/A | N/A | Medium |

---

## 🎯 Use Case Guide

### Need multi-agent conversations?
→ **Autogen** or **Swarm**

### Need role-based workflows?
→ **CrewAI**

### Need persistent chat threads?
→ **OpenAI Assistants**

### Need type-safe outputs?
→ **PydanticAI**

### Need code execution?
→ **Autogen**

### Need lightweight routing?
→ **OpenAI Swarm**

### Need RAG with PDFs?
→ **LangChain RAG** or **LlamaIndex RAG**

### Need complex orchestration?
→ **Multi-Agent System**

---

## 📈 Testing Coverage

### All Frameworks Include:
- ✅ Complete working examples
- ✅ Custom-evals integration
- ✅ Quality gate validation
- ✅ Multiple test suites
- ✅ Best practices
- ✅ Error handling

### Test Statistics:
- **51 test suites** across all frameworks
- **250+ evaluation calls**
- **8 evaluation metrics**
- **7,400+ lines** of test code

---

## 🛠️ Installation Commands

### Install Everything

```bash
# Core
cd cust-evals
pip install -e ".[dev]"

# Original frameworks
pip install langchain langchain-openai langgraph
pip install llama-index llama-index-vector-stores-qdrant llama-index-embeddings-openai
pip install qdrant-client pypdf reportlab

# Additional frameworks
pip install pyautogen
pip install crewai
pip install openai>=1.0.0
pip install git+https://github.com/openai/swarm.git
pip install pydantic-ai pydantic>=2.0

# Optional
pip install google-cloud-aiplatform
```

### Set Environment

```bash
export OPENAI_API_KEY="your-openai-key"
export GOOGLE_CLOUD_PROJECT="your-gcp-project"  # Optional for Vertex AI
```

---

## 📝 Evaluation Integration

All frameworks integrate with custom-evals:

```python
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator,
    FaithfulnessEvaluator,  # For RAG
    AnswerRelevancyEvaluator  # For RAG
)
from custom.evals.llm import LLM

# Initialize evaluator
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)

# Evaluate response
score = evaluator.evaluate({
    "input": "query",
    "output": "response"
})

print(f"{score.label}: {score.score:.2f}")
print(f"Explanation: {score.explanation}")
```

---

## 🎓 Learning Path

### Beginner
1. Start with `AGENTS_RAG_QUICKSTART.md`
2. Run `openai_swarm_agent_example.py` (simplest)
3. Try `crewai_agent_example.py` (easy workflows)

### Intermediate
4. Study `autogen_agent_example.py` (multi-agent)
5. Explore `pydanticai_agent_example.py` (type-safe)
6. Review `rag_langchain_qdrant.py` (RAG systems)

### Advanced
7. Deep dive into `multi_agent_example.py`
8. Study `rag_llamaindex_qdrant.py`
9. Build custom agent systems

---

## 📞 Support & Resources

### Documentation
- Framework-specific docs in `docs/frameworks/`
- Complete guides in `docs/`
- Example files in `examples/`

### Getting Help
1. Check framework-specific documentation
2. Review example code
3. Test with provided examples
4. Refer to official framework docs

### Official Resources
- **Autogen**: https://microsoft.github.io/autogen/
- **CrewAI**: https://docs.crewai.com/
- **OpenAI**: https://platform.openai.com/docs
- **PydanticAI**: https://ai.pydantic.dev/
- **LangChain**: https://python.langchain.com/
- **LlamaIndex**: https://docs.llamaindex.ai/

---

## 🎉 Summary

**11 Complete Frameworks**:
- 9 Agent Frameworks
- 2 RAG Frameworks

**Comprehensive Coverage**:
- 7,400+ lines of code
- 3,000+ lines of documentation
- 51 test suites
- 250+ evaluations

**All frameworks are production-ready with custom-evals integration!**

---

**Navigate**:
- [Back to Main README](../README.md)
- [Quick Start Guide](../AGENTS_RAG_QUICKSTART.md)
- [Complete Summary](../FINAL_COMPLETE_SUMMARY.md)
