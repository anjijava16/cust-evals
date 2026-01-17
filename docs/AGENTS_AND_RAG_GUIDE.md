# Agents and RAG Systems - Comprehensive Testing Guide

This guide provides complete examples for testing AI agent frameworks and RAG applications using the custom-evals evaluation framework.

## Table of Contents

- [Overview](#overview)
- [Agent Examples](#agent-examples)
  - [LangChain ReAct Agent](#langchain-react-agent)
  - [LangGraph Stateful Agent](#langgraph-stateful-agent)
  - [Multi-Agent System](#multi-agent-system)
  - [Google Vertex AI Agents](#google-vertex-ai-agents)
- [RAG Examples](#rag-examples)
  - [LangChain RAG with Qdrant](#langchain-rag-with-qdrant)
  - [LlamaIndex RAG with Qdrant](#llamaindex-rag-with-qdrant)
- [Evaluation Metrics](#evaluation-metrics)
- [Best Practices](#best-practices)

---

## Overview

This documentation covers **6 production-ready examples** demonstrating:

1. **4 Agent Frameworks**:
   - LangChain ReAct Agent
   - LangGraph Stateful Agent
   - Multi-Agent System (Orchestrated)
   - Google Vertex AI Agents

2. **2 RAG Systems**:
   - LangChain + Qdrant RAG
   - LlamaIndex + Qdrant RAG

All examples include comprehensive testing with custom-evals metrics.

---

## Agent Examples

### LangChain ReAct Agent

**File**: `examples/langchain_agent_example.py`

**Features**:
- ReAct (Reasoning + Acting) pattern
- Multiple tools: database search, calculations, weather, product catalog
- Multi-step reasoning capabilities
- Ground truth evaluation

**Quick Start**:

```bash
# Install dependencies
pip install langchain langchain-openai

# Set API key
export OPENAI_API_KEY="your-key"

# Run example
python examples/langchain_agent_example.py
```

**Example Code**:

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

# Create agent
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run agent
result = agent_executor.invoke({"input": "What is Alice's role?"})
response = result["output"]

# Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = RelevanceEvaluator(eval_llm)
score = evaluator.evaluate({
    "input": "What is Alice's role?",
    "output": response
})

print(f"Relevance: {score.label} ({score.score:.2f})")
```

**Test Cases**:

1. **Basic Queries**: Single tool usage
2. **Multi-Step Reasoning**: Complex queries requiring multiple tools
3. **Ground Truth Evaluation**: Comparing against expected answers
4. **Quality Gates**: Automated quality thresholds
5. **Hallucination Detection**: Checking factual accuracy
6. **Batch Evaluation**: Regression testing

**Evaluation Metrics**:
- Coherence
- Relevance
- Correctness
- Toxicity
- Hallucination

---

### LangGraph Stateful Agent

**File**: `examples/langgraph_agent_example.py`

**Features**:
- Stateful workflow with graph-based execution
- Tool integration with conditional edges
- Message history management
- Streaming support

**Quick Start**:

```bash
# Install dependencies
pip install langgraph langchain-openai

# Run example
export OPENAI_API_KEY="your-key"
python examples/langgraph_agent_example.py
```

**Example Code**:

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from custom.evals import CoherenceEvaluator, ToxicityEvaluator

class AgentState(TypedDict):
    messages: list
    next_action: str

# Create graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))
workflow.add_conditional_edges("agent", should_continue)
graph = workflow.compile()

# Run agent
result = graph.invoke(initial_state)
response = result["messages"][-1].content

# Evaluate
evaluator = CoherenceEvaluator(eval_llm)
score = evaluator.evaluate({
    "input": query,
    "output": response
})
```

**Test Cases**:

1. **Single Query**: Weather information
2. **Multiple Queries**: Comprehensive testing
3. **Context-Aware Evaluation**: Using retrieval context
4. **Quality Gates**: Production readiness checks
5. **Batch Evaluation**: Performance testing

---

### Multi-Agent System

**File**: `examples/multi_agent_example.py`

**Features**:
- 4 specialized agents: Research, Analysis, Writer, Reviewer
- Orchestrated workflow: Research → Analyze → Write → Review
- Agent collaboration and handoffs
- Complex task decomposition

**Quick Start**:

```bash
# Install dependencies
pip install langchain-openai

# Run example
export OPENAI_API_KEY="your-key"
python examples/multi_agent_example.py
```

**Architecture**:

```
┌─────────────────────────────────────────────────┐
│              Orchestrator                       │
└─────────────────────────────────────────────────┘
         │                │               │
    ┌────▼────┐     ┌────▼────┐    ┌────▼────┐
    │Research │     │Analysis │    │ Writer  │
    │ Agent   │────▶│ Agent   │───▶│ Agent   │
    └─────────┘     └─────────┘    └────┬────┘
                                        │
                                   ┌────▼────┐
                                   │Reviewer │
                                   │ Agent   │
                                   └─────────┘
```

**Example Code**:

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator

# Create multi-agent orchestrator
orchestrator = MultiAgentOrchestrator()

# Run complete workflow
result = orchestrator.run_research_workflow("quantum computing")

# Result includes outputs from all agents
research = result["results"]["research"]
analysis = result["results"]["analysis"]
writing = result["results"]["writing"]
review = result["results"]["review"]

# Evaluate final output
scores = orchestrator.evaluate_workflow(
    topic=result["topic"],
    final_content=result["final_content"]
)

for metric, score in scores.items():
    print(f"{metric}: {score.label} ({score.score:.2f})")
```

**Test Cases**:

1. **Individual Agents**: Test each agent separately
2. **Complete Workflow**: End-to-end pipeline
3. **Multiple Workflows**: Different topics
4. **Quality Gates**: Production thresholds
5. **Agent Collaboration**: Information flow analysis

---

### Google Vertex AI Agents

**File**: `examples/google_vertex_agent_example.py`

**Features**:
- Vertex AI Gemini models with function calling
- Multi-agent routing system
- Customer service, technical support, and sales agents
- Google Cloud integration

**Quick Start**:

```bash
# Install dependencies
pip install google-cloud-aiplatform

# Set up GCP
export GOOGLE_CLOUD_PROJECT="your-project-id"
gcloud auth application-default login

# Run example
export OPENAI_API_KEY="your-key"  # For evaluations
python examples/google_vertex_agent_example.py
```

**Example Code**:

```python
from vertexai.generative_models import GenerativeModel, FunctionDeclaration, Tool
from custom.evals import RelevanceEvaluator, ToxicityEvaluator

# Define function declarations
get_product_info = FunctionDeclaration(
    name="get_product_info",
    description="Get product information by ID",
    parameters={...}
)

# Create agent with tools
tools = Tool(function_declarations=[get_product_info, ...])
model = GenerativeModel("gemini-1.5-flash", tools=[tools])

# Run agent with function calling
chat = model.start_chat()
response = chat.send_message(query)

# Handle function calls
if response.function_call:
    result = execute_function(response.function_call)
    response = chat.send_message(function_response(result))

# Evaluate
scores = evaluate(query, response.text)
```

**Multi-Agent Routing**:

```python
# Create specialized agents
customer_service_agent = GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="You are a customer service agent..."
)

technical_support_agent = GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="You are a technical support agent..."
)

# Router agent
router = GenerativeModel("gemini-1.5-flash", system_instruction="...")
route = router.generate_content(query).text

# Route to appropriate agent
agent = agents[route]
response = agent.generate_content(query)
```

**Test Cases**:

1. **Basic Agent**: Function calling with tools
2. **Multi-Agent System**: Routing to specialized agents
3. **Comprehensive Evaluation**: Quality metrics

---

## RAG Examples

### LangChain RAG with Qdrant

**File**: `examples/rag_langchain_qdrant.py`

**Features**:
- PDF processing and text extraction
- OpenAI embeddings
- Qdrant vector database
- RetrievalQA chain
- RAG-specific evaluation (Faithfulness, Answer Relevancy)

**Quick Start**:

```bash
# Install dependencies
pip install langchain langchain-openai qdrant-client pypdf reportlab

# Run example
export OPENAI_API_KEY="your-key"
python examples/rag_langchain_qdrant.py
```

**Example Code**:

```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator

# 1. Load and split PDF
loader = PyPDFLoader("document.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# 2. Create embeddings and vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Qdrant.from_documents(
    chunks,
    embeddings,
    path="./qdrant_data",
    collection_name="documents"
)

# 3. Create QA chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# 4. Query
result = qa_chain({"query": "What is machine learning?"})
answer = result["result"]
context = "\n\n".join([doc.page_content for doc in result["source_documents"]])

# 5. Evaluate with RAG-specific metrics
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

# Faithfulness: Is answer grounded in context?
faithfulness_eval = FaithfulnessEvaluator(eval_llm)
faith_score = faithfulness_eval.evaluate({
    "input": query,
    "output": answer,
    "context": context
})
print(f"Faithfulness: {faith_score.label} ({faith_score.score:.2f})")

# Answer Relevancy: Does answer address the question?
relevancy_eval = AnswerRelevancyEvaluator(eval_llm)
rel_score = relevancy_eval.evaluate({
    "input": query,
    "output": answer
})
print(f"Answer Relevancy: {rel_score.label} ({rel_score.score:.2f})")
```

**Test Cases**:

1. **PDF Processing**: Document loading and chunking
2. **RAG System Setup**: Indexing and QA chain creation
3. **Basic Queries**: Standard question answering
4. **RAG Evaluation**: Faithfulness and relevancy metrics
5. **Quality Gates**: Production readiness thresholds
6. **Ground Truth**: Expected answer verification

**RAG-Specific Metrics**:
- **Faithfulness**: Ensures answers are grounded in retrieved context
- **Answer Relevancy**: Checks if answer addresses the question
- **Hallucination**: Detects unsupported claims
- **Coherence**: Evaluates response quality

---

### LlamaIndex RAG with Qdrant

**File**: `examples/rag_llamaindex_qdrant.py`

**Features**:
- Document loading from multiple formats
- SentenceSplitter for chunking
- Qdrant vector store integration
- Query engine with response synthesis
- Multi-document reasoning

**Quick Start**:

```bash
# Install dependencies
pip install llama-index llama-index-vector-stores-qdrant llama-index-embeddings-openai qdrant-client

# Run example
export OPENAI_API_KEY="your-key"
python examples/rag_llamaindex_qdrant.py
```

**Example Code**:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator

# 1. Configure settings
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)

# 2. Load documents
reader = SimpleDirectoryReader("./documents")
documents = reader.load_data()

# 3. Create Qdrant vector store
qdrant_client = QdrantClient(path="./qdrant_data")
vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="documents"
)

# 4. Create index
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# 5. Create query engine
query_engine = index.as_query_engine(
    similarity_top_k=3,
    response_mode="compact"
)

# 6. Query
response = query_engine.query("What is natural language processing?")
answer = str(response)
context = "\n\n".join([node.text for node in response.source_nodes])

# 7. Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

faithfulness_eval = FaithfulnessEvaluator(eval_llm)
faith_score = faithfulness_eval.evaluate({
    "input": query,
    "output": answer,
    "context": context
})

relevancy_eval = AnswerRelevancyEvaluator(eval_llm)
rel_score = relevancy_eval.evaluate({
    "input": query,
    "output": answer
})

print(f"Faithfulness: {faith_score.label} ({faith_score.score:.2f})")
print(f"Answer Relevancy: {rel_score.label} ({rel_score.score:.2f})")
```

**Test Cases**:

1. **Document Loading**: Multi-format document processing
2. **RAG Setup**: Index creation with Qdrant
3. **Basic Queries**: Question answering
4. **RAG Evaluation**: Comprehensive metrics
5. **Quality Gates**: Threshold validation
6. **Multi-Document Reasoning**: Cross-document queries
7. **Batch Evaluation**: Performance testing

---

## Evaluation Metrics

### Agent Metrics

| Metric | Description | Use Case |
|--------|-------------|----------|
| **Coherence** | Logical flow and structure | All agent responses |
| **Relevance** | On-topic and addresses query | Query-response pairs |
| **Correctness** | Factual accuracy | Ground truth comparison |
| **Toxicity** | Harmful content detection | Safety checks |
| **Hallucination** | Unsupported claims | Context-based validation |

### RAG-Specific Metrics

| Metric | Description | Use Case |
|--------|-------------|----------|
| **Faithfulness** | Answer grounded in context | RAG factual accuracy |
| **Answer Relevancy** | Addresses the question | RAG relevance |
| **Hallucination** | Claims not in context | RAG fact-checking |
| **Coherence** | Response quality | RAG output quality |

### Evaluation Example

```python
from custom.evals import (
    FaithfulnessEvaluator,
    AnswerRelevancyEvaluator,
    CoherenceEvaluator,
    HallucinationEvaluator
)
from custom.evals.llm import LLM

# Initialize evaluators
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

evaluators = {
    "faithfulness": FaithfulnessEvaluator(eval_llm),
    "answer_relevancy": AnswerRelevancyEvaluator(eval_llm),
    "coherence": CoherenceEvaluator(eval_llm),
    "hallucination": HallucinationEvaluator(eval_llm)
}

# Evaluate RAG response
scores = {}
for name, evaluator in evaluators.items():
    score = evaluator.evaluate({
        "input": question,
        "output": answer,
        "context": context  # For faithfulness and hallucination
    })
    scores[name] = score
    print(f"{name}: {score.label} ({score.score:.2f})")
    print(f"  Explanation: {score.explanation}\n")
```

---

## Best Practices

### 1. Agent Testing

**Test Coverage**:
- ✅ Single tool usage
- ✅ Multi-step reasoning
- ✅ Edge cases and error handling
- ✅ Quality gates with thresholds
- ✅ Batch regression testing

**Quality Thresholds**:
```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,      # Minimum coherence
    "relevance": 0.7,      # Minimum relevance
    "toxicity": 0.2,       # Maximum toxicity (lower is better)
}
```

**Example Test**:
```python
def test_agent_quality_gates():
    agent = create_agent()

    for query in test_queries:
        result = agent.run(query)
        scores = agent.evaluate(query, result["response"])

        # Check quality gates
        for metric, threshold in QUALITY_THRESHOLDS.items():
            assert scores[metric].score >= threshold, \
                f"{metric} below threshold: {scores[metric].score} < {threshold}"
```

### 2. RAG Testing

**Test Coverage**:
- ✅ Document processing and chunking
- ✅ Retrieval accuracy
- ✅ Answer faithfulness
- ✅ Answer relevancy
- ✅ Multi-document reasoning
- ✅ Ground truth validation

**RAG Quality Thresholds**:
```python
RAG_QUALITY_THRESHOLDS = {
    "faithfulness": 0.8,      # High bar for factual accuracy
    "answer_relevancy": 0.7,  # Answer should be relevant
    "coherence": 0.7,          # Answer should be coherent
}
```

**Example Test**:
```python
def test_rag_quality_gates():
    rag = create_rag_system()

    for test_case in test_cases:
        result = rag.query(test_case["question"])
        scores = rag.evaluate(
            test_case["question"],
            result["answer"],
            result["context"]
        )

        # Check RAG-specific quality gates
        for metric, threshold in RAG_QUALITY_THRESHOLDS.items():
            assert scores[metric].score >= threshold, \
                f"{metric} below threshold: {scores[metric].score} < {threshold}"
```

### 3. Multi-Agent Testing

**Workflow Validation**:
- ✅ Individual agent testing
- ✅ Agent collaboration and handoffs
- ✅ Information flow analysis
- ✅ End-to-end workflow testing

**Example Test**:
```python
def test_multi_agent_workflow():
    orchestrator = MultiAgentOrchestrator()

    # Run complete workflow
    result = orchestrator.run_research_workflow(topic)

    # Validate each stage
    assert result["results"]["research"].success
    assert result["results"]["analysis"].success
    assert result["results"]["writing"].success
    assert result["results"]["review"].success

    # Evaluate final output
    scores = orchestrator.evaluate_workflow(topic, result["final_content"])

    for metric, score in scores.items():
        assert score.score >= THRESHOLDS[metric]
```

### 4. Continuous Testing

**Regression Testing**:
```python
def test_batch_evaluation():
    """Regression test for multiple queries."""
    system = create_system()

    test_queries = load_test_suite()
    results = []

    for query in test_queries:
        result = system.run(query)
        scores = system.evaluate(query, result["response"])
        results.append({
            "query": query,
            "scores": scores,
            "passed": all(s.score >= threshold for s in scores.values())
        })

    # Calculate pass rate
    pass_rate = sum(r["passed"] for r in results) / len(results)
    assert pass_rate >= 0.8, f"Pass rate too low: {pass_rate:.1%}"
```

### 5. Production Monitoring

**Key Metrics to Track**:
- Average coherence score
- Average relevance score
- Average faithfulness score (for RAG)
- Average answer relevancy score (for RAG)
- Toxicity rate
- Hallucination rate
- Response time
- Success rate

**Example Monitoring**:
```python
import pandas as pd

def monitor_production_quality(queries, responses, contexts):
    """Monitor production quality metrics."""
    results = []

    for query, response, context in zip(queries, responses, contexts):
        scores = evaluate(query, response, context)
        results.append({
            "timestamp": datetime.now(),
            "coherence": scores["coherence"].score,
            "relevance": scores["relevance"].score,
            "faithfulness": scores["faithfulness"].score,
            "answer_relevancy": scores["answer_relevancy"].score
        })

    df = pd.DataFrame(results)

    # Calculate statistics
    print("Production Quality Metrics:")
    print(f"  Average Coherence: {df['coherence'].mean():.2f}")
    print(f"  Average Relevance: {df['relevance'].mean():.2f}")
    print(f"  Average Faithfulness: {df['faithfulness'].mean():.2f}")
    print(f"  Average Answer Relevancy: {df['answer_relevancy'].mean():.2f}")

    # Alert if metrics drop
    if df['faithfulness'].mean() < 0.7:
        alert("Faithfulness score dropped below threshold!")
```

---

## Running All Examples

```bash
# Set up environment
export OPENAI_API_KEY="your-openai-key"
export GOOGLE_CLOUD_PROJECT="your-gcp-project"  # For Vertex AI example

# Run agent examples
python examples/langchain_agent_example.py
python examples/langgraph_agent_example.py
python examples/multi_agent_example.py
python examples/google_vertex_agent_example.py

# Run RAG examples
python examples/rag_langchain_qdrant.py
python examples/rag_llamaindex_qdrant.py
```

---

## Dependencies

### Agent Examples
```bash
# LangChain Agent
pip install langchain langchain-openai

# LangGraph Agent
pip install langgraph langchain-openai

# Multi-Agent System
pip install langchain-openai

# Google Vertex AI Agents
pip install google-cloud-aiplatform
```

### RAG Examples
```bash
# LangChain RAG
pip install langchain langchain-openai qdrant-client pypdf reportlab

# LlamaIndex RAG
pip install llama-index llama-index-vector-stores-qdrant llama-index-embeddings-openai qdrant-client pypdf
```

### Custom Evals
```bash
pip install -e ".[dev]"
```

---

## Summary

This guide provides comprehensive examples for:

- **4 Agent Frameworks**: LangChain, LangGraph, Multi-Agent, Vertex AI
- **2 RAG Systems**: LangChain + Qdrant, LlamaIndex + Qdrant
- **Production Testing**: Quality gates, batch evaluation, monitoring
- **Comprehensive Metrics**: Agent and RAG-specific evaluations

All examples include:
- ✅ Complete working code
- ✅ Multiple test cases
- ✅ Quality gate validation
- ✅ Evaluation with custom-evals
- ✅ Production-ready patterns

For more information, see:
- [Custom Evals README](../README.md)
- [API Reference](api-reference.md)
- [Framework Comparison](framework-comparison.md)
