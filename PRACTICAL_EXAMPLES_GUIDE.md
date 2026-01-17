# Practical Examples Guide - Agents & RAG with Custom Evals

This guide provides comprehensive, production-ready examples for integrating Custom Evals with agents, multi-agent systems, and RAG applications.

## 📚 Table of Contents

- [Overview](#overview)
- [Agent Examples](#agent-examples)
  - [LangGraph Agent](#1-langgraph-agent)
  - [LangChain Agent](#2-langchain-agent)
  - [Multi-Agent System](#3-multi-agent-system)
- [RAG Examples](#rag-examples)
  - [LangChain RAG with Qdrant](#4-langchain-rag-with-qdrant)
- [Installation](#installation)
- [Running Examples](#running-examples)
- [Testing Patterns](#testing-patterns)
- [Best Practices](#best-practices)

---

## Overview

This repository contains **4 comprehensive, production-ready examples** demonstrating how to:

✅ **Build agents** with LangGraph and LangChain
✅ **Create multi-agent systems** with agent collaboration
✅ **Implement RAG** with Qdrant vector database and PDF processing
✅ **Evaluate everything** with custom-evals at every step
✅ **Test thoroughly** with comprehensive test suites

### What's Included

| Example | File | Lines | Tests | Status |
|---------|------|-------|-------|--------|
| **LangGraph Agent** | `langgraph_agent_example.py` | 550+ | 5 | ✅ Complete |
| **LangChain Agent** | `langchain_agent_example.py` | 700+ | 6 | ✅ Complete |
| **Multi-Agent System** | `multi_agent_example.py` | 750+ | 6 | ✅ Complete |
| **LangChain RAG + Qdrant** | `rag_langchain_qdrant.py` | 700+ | 5 | ✅ Complete |
| **Total** | **4 files** | **2,700+ lines** | **22 tests** | ✅ **Production Ready** |

---

## Agent Examples

### 1. LangGraph Agent

**File**: `examples/langgraph_agent_example.py`

**What It Demonstrates**:
- ✅ Creating a LangGraph agent with stateful workflow
- ✅ Tool definition and binding
- ✅ Agent execution with state management
- ✅ Evaluation with custom-evals (Coherence, Relevance, Toxicity)
- ✅ 5 comprehensive test suites

**Key Features**:
```python
# LangGraph agent with tools
class LangGraphAgent:
    - StateGraph workflow
    - Tool nodes (Weather, Wikipedia, Calculator)
    - Conditional routing
    - Custom-evals integration

# Evaluation after each agent run
scores = agent.evaluate(query, response)
# Returns: coherence, relevance, toxicity scores
```

**Test Suites Included**:
1. **Single Query Test** - Basic agent functionality
2. **Multiple Queries Test** - Comprehensive testing across queries
3. **Context-Aware Evaluation** - Hallucination detection with context
4. **Quality Gates** - Automated quality thresholds
5. **Batch Evaluation** - Regression testing

**How to Run**:
```bash
export OPENAI_API_KEY="your-key"
python examples/langgraph_agent_example.py
```

**Expected Output**:
```
🚀 LangGraph Agent Example with Custom Evals Testing
================================================================

TEST 1: Single Query - Weather Information
----------------------------------------------------------------
📝 Query: What's the weather like in San Francisco?
🤖 Agent Response: The weather in San Francisco is Sunny, 72°F

📊 Evaluation Scores:
  • Coherence: coherent (0.95)
  • Relevance: relevant (0.90)
  • Toxicity: not_toxic (0.05)

✅ All tests completed successfully!
```

---

### 2. LangChain Agent

**File**: `examples/langchain_agent_example.py`

**What It Demonstrates**:
- ✅ Creating a LangChain ReAct agent
- ✅ Multiple tools (Search, Calculator, Weather, Database)
- ✅ Tool selection and reasoning
- ✅ Ground truth evaluation with CorrectnessEvaluator
- ✅ 6 comprehensive test suites

**Key Features**:
```python
# LangChain ReAct agent
class LangChainAgent:
    - ReAct reasoning pattern
    - 4 different tools
    - AgentExecutor with error handling
    - Ground truth validation

# Evaluation with ground truth
scores = agent.evaluate(query, response, expected="360")
# Returns: coherence, relevance, toxicity, correctness
```

**Test Suites Included**:
1. **Single Tool Usage** - Weather tool test
2. **Multi-Tool Usage** - Complex queries with multiple tools
3. **Ground Truth Evaluation** - Calculator accuracy testing
4. **Tool Selection** - Agent reasoning quality
5. **Quality Monitoring** - Production threshold checks
6. **Batch Regression** - Comprehensive test suite

**How to Run**:
```bash
export OPENAI_API_KEY="your-key"
python examples/langchain_agent_example.py
```

**Expected Output**:
```
🚀 LangChain Agent Example with Custom Evals Testing
================================================================

TEST 1: Single Tool Usage - Weather Query
----------------------------------------------------------------
📝 Query: What's the weather like in San Francisco?

> Entering new AgentExecutor chain...
I should use the Weather tool to get this information.
Action: Weather
Action Input: San Francisco
Observation: Weather in San Francisco: Sunny, 72°F with clear skies
Thought: I now know the final answer
Final Answer: The weather in San Francisco is Sunny, 72°F with clear skies

📊 Evaluation Scores:
  • Coherence: coherent (0.92)
  • Relevance: relevant (0.95)
  • Toxicity: not_toxic (0.02)

✅ All tests completed successfully!
```

---

### 3. Multi-Agent System

**File**: `examples/multi_agent_example.py`

**What It Demonstrates**:
- ✅ Multiple specialized agents (Research, Analysis, Summary, Recommendation)
- ✅ Agent collaboration and handoffs
- ✅ Workflow orchestration
- ✅ Individual agent evaluation
- ✅ System-wide evaluation
- ✅ 6 comprehensive test suites

**Key Features**:
```python
# Multi-agent orchestrator
class MultiAgentOrchestrator:
    - ResearchAgent: Information gathering
    - AnalysisAgent: Data analysis
    - SummaryAgent: Synthesis
    - RecommendationAgent: Action items

# Workflow execution with evaluation at each step
workflow = orchestrator.run_research_workflow(topic)
# Each agent's output is evaluated
# Overall workflow quality is assessed
```

**Agent Workflow**:
```
Topic → ResearchAgent → AnalysisAgent → SummaryAgent → RecommendationAgent → Final Output
         ↓               ↓                ↓              ↓
      Evaluate        Evaluate         Evaluate       Evaluate
```

**Test Suites Included**:
1. **Single Workflow** - Complete 4-agent workflow
2. **Agent Comparison** - Compare individual agent performance
3. **Workflow Variations** - Test different topics
4. **Handoff Quality** - Evaluate agent-to-agent information transfer
5. **Production Monitoring** - Real-time quality tracking
6. **Error Handling** - Edge case testing

**How to Run**:
```bash
export OPENAI_API_KEY="your-key"
python examples/multi_agent_example.py
```

**Expected Output**:
```
🚀 Multi-Agent System with Custom Evals Testing
================================================================

TEST 1: Single Multi-Agent Workflow
----------------------------------------------------------------
🎯 Topic: The impact of AI on healthcare

🔍 Step 1: Research Agent - Gathering information...
   Response: AI is transforming healthcare through...

🔬 Step 2: Analysis Agent - Analyzing research...
   Response: Key insights from the research include...

📝 Step 3: Summary Agent - Creating summary...
   Response: In summary, AI in healthcare enables...

💡 Step 4: Recommendation Agent - Generating recommendations...
   Response: Recommendations for healthcare organizations...

================================================================
📊 Workflow Evaluation
================================================================

Average Scores Across All Agents:
  • Coherence: 0.91
  • Relevance: 0.88
  • Hallucination: 0.15

Quality Gates:
  • Coherence: ✅ PASS
  • Relevance: ✅ PASS
  • Hallucination: ✅ PASS
  • Overall: ✅ PASS

✅ All tests completed successfully!
```

---

## RAG Examples

### 4. LangChain RAG with Qdrant

**File**: `examples/rag_langchain_qdrant.py`

**What It Demonstrates**:
- ✅ PDF document loading and processing
- ✅ Text chunking with RecursiveCharacterTextSplitter
- ✅ Embedding creation with OpenAI embeddings
- ✅ Vector storage in Qdrant database
- ✅ RetrievalQA chain with custom prompts
- ✅ RAG-specific evaluation (Faithfulness, Answer Relevancy)
- ✅ 5 comprehensive test suites

**Key Features**:
```python
# LangChain RAG with Qdrant
class LangChainQdrantRAG:
    - PDF loading with PyPDFLoader
    - Text splitting (500 char chunks, 50 overlap)
    - OpenAI embeddings (text-embedding-3-small)
    - Qdrant vector store (in-memory or persistent)
    - RetrievalQA chain
    - RAG-specific evaluators

# Evaluation with retrieved context
scores = rag.evaluate(question, answer, context)
# Returns: faithfulness, answer_relevancy, coherence, hallucination
```

**RAG Pipeline**:
```
PDF → Load → Split → Embed → Qdrant → Query → Retrieve → Generate → Evaluate
                                        ↓
                                   Vector Store
```

**Test Suites Included**:
1. **Single Query** - Basic RAG functionality
2. **Multiple Queries** - Test across different query types
3. **Quality Gates** - RAG-specific quality thresholds
4. **Retrieval Quality** - Analyze retrieval accuracy
5. **Batch Evaluation** - Comprehensive RAG testing

**How to Run**:
```bash
# Install dependencies
pip install qdrant-client pypdf reportlab

# Run example
export OPENAI_API_KEY="your-key"
python examples/rag_langchain_qdrant.py
```

**Expected Output**:
```
🚀 LangChain RAG with Qdrant - Custom Evals Testing
================================================================

✅ Created sample PDF: /tmp/tmpxyz123.pdf

TEST 1: Single Query RAG Evaluation
----------------------------------------------------------------

📄 Loading PDF: /tmp/tmpxyz123.pdf
   Loaded 3 pages
   Created 45 text chunks

🔄 Creating vector store in Qdrant...
   ✅ Vector store created with 45 documents

🔗 Creating RetrievalQA chain...
   ✅ QA chain created

❓ Question: What are the three main types of machine learning?

🤖 Answer: The three main types of machine learning are:
1. Supervised Learning - uses labeled datasets
2. Unsupervised Learning - works with unlabeled data
3. Reinforcement Learning - trains agents through rewards

📚 Retrieved 3 source documents

📊 RAG Evaluation:
  • Faithfulness: faithful (0.95)
    → Answer is fully grounded in retrieved context
  • Answer Relevancy: relevant (0.92)
    → Answer directly addresses the question
  • Coherence: coherent (0.94)
    → Response is well-structured and logical
  • Hallucination: factual (0.05)
    → No hallucinated information detected

✅ All tests completed successfully!
```

---

## Installation

### Prerequisites

```bash
# Core dependencies
pip install langchain langchain-community langchain-openai
pip install langgraph
pip install openai anthropic

# RAG dependencies
pip install qdrant-client
pip install pypdf
pip install reportlab  # For creating sample PDFs

# Custom Evals
cd /path/to/cust-evals
pip install -e ".[dev]"

# Optional: Phoenix tracing
pip install -e ".[dev,tracing]"
```

### Environment Setup

```bash
# Required
export OPENAI_API_KEY="your-openai-key"

# Optional (for Anthropic models)
export ANTHROPIC_API_KEY="your-anthropic-key"

# Optional (for Phoenix tracing)
# Start Phoenix server first: phoenix serve
# Then set endpoint (defaults to http://localhost:6006/v1/traces)
```

---

## Running Examples

### Quick Start - Run All Tests

```bash
# Run each example to see all tests
python examples/langgraph_agent_example.py
python examples/langchain_agent_example.py
python examples/multi_agent_example.py
python examples/rag_langchain_qdrant.py
```

### Run Individual Tests

You can modify the `main()` function in each file to run specific tests:

```python
# In langchain_agent_example.py
def main():
    # Comment out tests you don't want to run
    test_single_tool_usage()
    # test_multi_tool_usage()
    # test_with_ground_truth()
    # etc.
```

### Custom Configuration

Each example supports customization:

```python
# Change LLM model
llm = ChatOpenAI(
    model="gpt-4",  # Use GPT-4 instead of gpt-4o-mini
    temperature=0.3  # Adjust creativity
)

# Change quality thresholds
THRESHOLDS = {
    "coherence": 0.8,  # Stricter threshold
    "relevance": 0.75,
}

# Adjust retrieval parameters (RAG)
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}  # Retrieve 5 documents instead of 3
)
```

---

## Testing Patterns

### Pattern 1: Single Evaluation

**Use Case**: Quick sanity check

```python
# Run agent
result = agent.run(query)

# Evaluate
scores = agent.evaluate(query, result["response"])

# Check
if scores["coherence"].label == "coherent":
    print("✅ Agent working correctly")
```

### Pattern 2: Multiple Evaluations

**Use Case**: Comprehensive testing

```python
test_cases = [
    {"query": "Question 1", "expected": "Answer 1"},
    {"query": "Question 2", "expected": "Answer 2"},
]

results = []
for case in test_cases:
    result = agent.run(case["query"])
    scores = agent.evaluate(
        case["query"],
        result["response"],
        expected=case["expected"]
    )
    results.append(scores)

# Analyze results
pass_rate = sum(1 for r in results if all_passed(r)) / len(results)
```

### Pattern 3: Quality Gates

**Use Case**: Production readiness

```python
THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
}

result = agent.run(query)
scores = agent.evaluate(query, result["response"])

# Check thresholds
for metric, threshold in THRESHOLDS.items():
    if scores[metric].score < threshold:
        print(f"❌ Failed: {metric}")
        # Take action: log, alert, retry, etc.
```

### Pattern 4: Batch Regression

**Use Case**: Regression testing

```python
# Baseline results (from previous version)
baseline_results = load_baseline()

# Current results
current_results = run_test_suite()

# Compare
for i, (baseline, current) in enumerate(zip(baseline_results, current_results)):
    if current.score < baseline.score - 0.1:  # 10% regression
        print(f"⚠️  Regression detected in test {i}")
```

### Pattern 5: Production Monitoring

**Use Case**: Real-time monitoring

```python
def monitor_agent(agent, query):
    """Monitor agent in production."""

    # Run
    result = agent.run(query)

    # Evaluate
    scores = agent.evaluate(query, result["response"])

    # Log
    log_to_monitoring_system(query, result, scores)

    # Alert on issues
    if scores["coherence"].score < 0.7:
        send_alert("Low coherence detected")

    return result
```

---

## Best Practices

### 1. Always Evaluate

```python
# ❌ Bad: No evaluation
result = agent.run(query)
return result["response"]

# ✅ Good: Always evaluate
result = agent.run(query)
scores = agent.evaluate(query, result["response"])
log_scores(scores)
return result["response"]
```

### 2. Use Multiple Metrics

```python
# ❌ Bad: Single metric
coherence_score = agent.evaluate(query, response)

# ✅ Good: Multiple metrics
scores = {
    "coherence": coherence_eval.evaluate(...),
    "relevance": relevance_eval.evaluate(...),
    "hallucination": hallucination_eval.evaluate(...)
}
```

### 3. Set Quality Thresholds

```python
# ✅ Good: Define clear thresholds
THRESHOLDS = {
    "coherence": 0.7,      # Minimum acceptable
    "relevance": 0.7,
    "hallucination": 0.3,  # Maximum acceptable
}

# Check before returning to user
if not meets_thresholds(scores, THRESHOLDS):
    # Retry, use fallback, or alert
    pass
```

### 4. Test Thoroughly

```python
# ✅ Good: Comprehensive test suite
def test_agent():
    # Basic functionality
    test_single_query()

    # Edge cases
    test_empty_input()
    test_very_long_input()

    # Quality gates
    test_quality_thresholds()

    # Performance
    test_batch_evaluation()
```

### 5. Monitor Production

```python
# ✅ Good: Production monitoring
class MonitoredAgent:
    def run(self, query):
        result = self.agent.run(query)
        scores = self.evaluate(query, result)

        # Log metrics
        self.metrics.log(scores)

        # Alert on issues
        if scores["coherence"].score < 0.7:
            self.alerting.send_alert()

        return result
```

---

## Summary

### What You Get

✅ **4 Production-Ready Examples** (2,700+ lines of code)
✅ **22 Comprehensive Test Suites** across all examples
✅ **Complete Custom Evals Integration** at every step
✅ **Agent Examples**: LangGraph, LangChain, Multi-Agent
✅ **RAG Example**: LangChain + Qdrant + PDF processing
✅ **Testing Patterns**: Single, batch, regression, monitoring
✅ **Best Practices**: From development to production

### Quick Reference

| Want to... | Use Example | File |
|------------|-------------|------|
| **Build a stateful agent** | LangGraph Agent | `langgraph_agent_example.py` |
| **Create a ReAct agent** | LangChain Agent | `langchain_agent_example.py` |
| **Build multi-agent system** | Multi-Agent | `multi_agent_example.py` |
| **Implement RAG with PDFs** | LangChain RAG | `rag_langchain_qdrant.py` |

### Next Steps

1. **Run the examples**: Start with `langgraph_agent_example.py`
2. **Modify for your needs**: Adapt the code to your use case
3. **Add your own tests**: Extend the test suites
4. **Deploy to production**: Use the monitoring patterns

---

## 🎉 Congratulations!

You now have **production-ready, tested examples** for:
- ✅ Agent evaluation (LangGraph, LangChain, Multi-Agent)
- ✅ RAG evaluation (LangChain + Qdrant + PDFs)
- ✅ Comprehensive testing at every step
- ✅ Quality monitoring and gates

**All with Custom Evals integration from development to production!** 🚀

---

For more information:
- **Integration Guides**: [docs/agents-integration.md](docs/agents-integration.md), [docs/rag-integration.md](docs/rag-integration.md)
- **Testing Guide**: [docs/testing.md](docs/testing.md)
- **Full Documentation**: [docs/README.md](docs/README.md)
