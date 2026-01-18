# Agents & RAG Quick Start Guide

Quick reference for testing agent frameworks and RAG applications with custom-evals.

## 📦 Installation

```bash
# Install custom-evals
cd cust-evals
pip install -e ".[dev]"

# For agent examples
pip install langchain langchain-openai langgraph

# For RAG examples
pip install langchain langchain-openai qdrant-client pypdf reportlab
pip install llama-index llama-index-vector-stores-qdrant llama-index-embeddings-openai

# For Vertex AI (optional)
pip install google-cloud-aiplatform
```

## 🚀 Quick Examples

### Agent Testing

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from custom.evals import RelevanceEvaluator, CoherenceEvaluator
from custom.evals.llm import LLM

# Create agent
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

# Run agent
result = executor.invoke({"input": "What is the weather?"})

# Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
relevance = RelevanceEvaluator(eval_llm)
score = relevance.evaluate({
    "input": "What is the weather?",
    "output": result["output"]
})

print(f"Relevance: {score.label} ({score.score:.2f})")
```

### RAG Testing

```python
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

# Create RAG
embeddings = OpenAIEmbeddings()
vectorstore = Qdrant.from_documents(docs, embeddings, path="./data")
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    retriever=vectorstore.as_retriever()
)

# Query
result = qa({"query": "What is ML?"})
answer = result["result"]
context = "\n".join([d.page_content for d in result["source_documents"]])

# Evaluate RAG-specific metrics
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

faithfulness = FaithfulnessEvaluator(eval_llm)
faith_score = faithfulness.evaluate({
    "input": "What is ML?",
    "output": answer,
    "context": context
})

relevancy = AnswerRelevancyEvaluator(eval_llm)
rel_score = relevancy.evaluate({
    "input": "What is ML?",
    "output": answer
})

print(f"Faithfulness: {faith_score.label} ({faith_score.score:.2f})")
print(f"Answer Relevancy: {rel_score.label} ({rel_score.score:.2f})")
```

## 📊 Evaluation Metrics

### For Agents

```python
from custom.evals import (
    CoherenceEvaluator,      # Logical flow
    RelevanceEvaluator,      # On-topic
    CorrectnessEvaluator,    # Factual accuracy
    ToxicityEvaluator,       # Safety
    HallucinationEvaluator   # Unsupported claims
)
```

### For RAG Systems

```python
from custom.evals import (
    FaithfulnessEvaluator,      # Grounded in context
    AnswerRelevancyEvaluator,   # Addresses question
    HallucinationEvaluator,     # Fact-checking
    CoherenceEvaluator          # Quality
)
```

## 🎯 Quality Gates

```python
# Define thresholds
QUALITY_THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
    "faithfulness": 0.8,  # High bar for RAG
    "toxicity": 0.2        # Lower is better
}

# Test with quality gates
def test_with_quality_gates(query, response, context=None):
    scores = evaluate(query, response, context)

    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric not in scores:
            continue

        score_value = scores[metric].score

        if metric == "toxicity":
            passed = score_value <= threshold
        else:
            passed = score_value >= threshold

        if not passed:
            print(f"❌ {metric} failed: {score_value:.2f}")
            return False

    print("✅ All quality gates passed!")
    return True
```

## 📚 Complete Examples

### 1. LangChain Agent

```bash
python examples/langchain_agent_example.py
```

**Features**: ReAct pattern, multiple tools, multi-step reasoning

### 2. LangGraph Agent

```bash
python examples/langgraph_agent_example.py
```

**Features**: Stateful workflow, graph execution, conditional edges

### 3. Multi-Agent System

```bash
python examples/multi_agent_example.py
```

**Features**: 4 specialized agents, orchestrated workflow, collaboration

### 4. Google Vertex AI Agents

```bash
export GOOGLE_CLOUD_PROJECT="your-project"
python examples/google_vertex_agent_example.py
```

**Features**: Gemini models, function calling, multi-agent routing

### 5. LangChain RAG + Qdrant

```bash
python examples/rag_langchain_qdrant.py
```

**Features**: PDF processing, vector DB, RetrievalQA, RAG evaluation

### 6. LlamaIndex RAG + Qdrant

```bash
python examples/rag_llamaindex_qdrant.py
```

**Features**: Document loading, query engine, multi-doc reasoning

## 🧪 Test Patterns

### Basic Test

```python
def test_basic():
    result = system.run(query)
    assert result["success"]
    print(f"Response: {result['response']}")
```

### With Evaluation

```python
def test_with_eval():
    result = system.run(query)
    scores = system.evaluate(query, result["response"])

    assert scores["relevance"].score >= 0.7
    assert scores["coherence"].score >= 0.7
```

### Batch Testing

```python
def test_batch():
    results = []
    for query in test_queries:
        result = system.run(query)
        scores = system.evaluate(query, result["response"])
        results.append(scores)

    avg_score = sum(r["coherence"].score for r in results) / len(results)
    assert avg_score >= 0.7
```

### RAG Testing

```python
def test_rag():
    result = rag.query(question)
    scores = rag.evaluate(
        question,
        result["answer"],
        result["context"]
    )

    # RAG-specific checks
    assert scores["faithfulness"].score >= 0.8
    assert scores["answer_relevancy"].score >= 0.7
```

## 📖 Full Documentation

- **[Complete Guide](docs/AGENTS_AND_RAG_GUIDE.md)** - Comprehensive documentation
- **[API Reference](docs/api-reference.md)** - Full API documentation
- **[Examples](docs/examples.md)** - Code examples

## 🔑 Environment Setup

```bash
# Required
export OPENAI_API_KEY="your-openai-key"

# Optional (for Vertex AI)
export GOOGLE_CLOUD_PROJECT="your-gcp-project"
gcloud auth application-default login

# Optional (for Phoenix tracing)
# Start Phoenix server first: phoenix server
export PHOENIX_ENDPOINT="http://localhost:6006/v1/traces"
```

## 💡 Tips

1. **Start Simple**: Begin with basic queries before multi-step reasoning
2. **Use Quality Gates**: Define thresholds for production readiness
3. **Batch Test**: Run regression tests regularly
4. **Monitor Metrics**: Track evaluation scores over time
5. **RAG-Specific**: Use Faithfulness and Answer Relevancy for RAG systems
6. **Context Matters**: Always provide context for hallucination checks

## 🆘 Troubleshooting

**Issue**: Import errors
```bash
pip install -e ".[dev]"
```

**Issue**: API key not found
```bash
export OPENAI_API_KEY="your-key"
```

**Issue**: Qdrant connection error
```bash
# Using local storage (default)
# Data stored in ./qdrant_data or ./llamaindex_qdrant_data
```

**Issue**: Vertex AI authentication
```bash
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

## 🎓 Learning Path

1. Start with **basic_usage.py** to understand code metrics
2. Try **llm_evaluation.py** for LLM-based evaluators
3. Run **langchain_agent_example.py** for agent testing
4. Explore **rag_langchain_qdrant.py** for RAG systems
5. Study **multi_agent_example.py** for complex workflows
6. Review **AGENTS_AND_RAG_GUIDE.md** for best practices

## 📞 Support

- [GitHub Issues](https://github.com/anthropics/claude-code/issues)
- [Documentation](docs/)
- [Examples](examples/)

---

**Ready to start testing?** Pick an example and run it! 🚀
