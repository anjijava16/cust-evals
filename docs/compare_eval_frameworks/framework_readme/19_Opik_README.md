# Opik: The Complete Deep-Dive Guide

**Version**: 1.0.0 | **Updated**: January 2026 | **License**: Open Source (Apache 2.0)

---

## Table of Contents

1. [Introduction & Overview](#1-introduction--overview)
2. [Complete Architecture](#2-complete-architecture)
3. [Installation & Setup](#3-installation--setup)
4. [Core Concepts](#4-core-concepts)
5. [Complete Examples Section](#5-complete-examples-section)
6. [Advanced Usage](#6-advanced-usage)
7. [Best Practices](#7-best-practices)
8. [Integration Guide](#8-integration-guide)
9. [Troubleshooting](#9-troubleshooting)
10. [API Reference](#10-api-reference)
11. [Performance & Optimization](#11-performance--optimization)
12. [Security Considerations](#12-security-considerations)
13. [References & Resources](#13-references--resources)

---

## 1. Introduction & Overview

### 1.1 What is Opik?

Opik is an open-source platform developed by Comet ML for building, testing, and optimizing generative AI applications from prototype to production. It provides comprehensive tracing, evaluation, and prompt optimization for RAG systems, agents, chatbots, and more. As a unified observability and evaluation platform, Opik serves as the centralized hub for monitoring LLM applications throughout their entire lifecycle.

**Core Philosophy:**
- **Open Source First**: Apache 2.0 licensed with full self-hosting capabilities
- **Production Ready**: Built for real-world deployments at scale
- **Developer Experience**: Simple SDK with powerful observability
- **Lifecycle Coverage**: From prototyping to production monitoring

### 1.2 Key Features

#### Comprehensive Tracing
- **Distributed Tracing**: Track LLM calls, chains, and complex workflows
- **Multi-Turn Conversations**: Thread-based conversation tracking
- **Cost Tracking**: Monitor spending across all LLM providers
- **Multimodal Support**: Log images, videos, audio, and documents
- **Real-Time Monitoring**: Live trace streaming and analysis

#### Advanced Evaluation
- **50+ Built-in Metrics**: Hallucination, relevance, context precision/recall
- **LLM-as-Judge**: Automated evaluation with configurable models
- **Agent Evaluation**: Task completion, tool correctness, trajectory accuracy
- **Multi-Turn Evaluation**: Conversation quality assessment
- **Custom Metrics**: Build domain-specific evaluators

#### Prompt Engineering
- **Centralized Library**: Version-controlled prompt management
- **Playground**: Interactive testing environment
- **AI-Powered Optimization**: Automated prompt generation and improvement
- **MCP Server Integration**: Direct Cursor IDE integration
- **A/B Testing**: Compare prompt variations systematically

#### Production Monitoring
- **Real-Time Rules**: Automated evaluation on production traces
- **Guardrails**: Prevent unsafe outputs before serving
- **Anonymizers**: Protect sensitive data automatically
- **Custom Dashboards**: Visualize key metrics
- **Alert System**: Proactive anomaly detection

#### Gateway & Management
- **Centralized Gateway**: Route requests across LLM providers
- **Provider Abstraction**: Switch providers without code changes
- **Cost Optimization**: Smart routing based on cost/performance
- **Rate Limiting**: Prevent API quota exhaustion

### 1.3 When to Use Opik

**Perfect For:**
- Teams wanting full control with self-hosting
- Organizations requiring open-source solutions
- Projects needing comprehensive agent evaluation
- Teams using diverse LLM frameworks (50+ integrations)
- Cost-conscious teams needing detailed spending analysis
- Multi-provider deployments requiring unified monitoring

**Not Ideal For:**
- Simple single-prompt applications
- Teams exclusively using one framework (framework-specific tool may suffice)
- Projects with minimal evaluation requirements
- Teams avoiding deployment/infrastructure management

### 1.4 Comparison Matrix

| Feature | Opik | LangSmith | Phoenix | Langfuse | Braintrust |
|---------|------|-----------|---------|----------|------------|
| **Open Source** | ✅ Full | ❌ No | ✅ Yes | ✅ Yes | ⚠️ Limited |
| **Self-Hosting** | ✅ Complete | ⚠️ Enterprise | ✅ Yes | ✅ Yes | ⚠️ Enterprise |
| **Agent Evaluation** | ✅✅ Advanced | ✅ Good | ⚠️ Limited | ⚠️ Basic | ✅ Good |
| **Gateway** | ✅ Built-in | ❌ No | ❌ No | ❌ No | ❌ No |
| **Multimodal** | ✅ Full | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | ✅ Good |
| **Integrations** | ✅✅ 50+ | ✅✅ Many | ✅ Good | ✅ Good | ✅ Good |
| **Cost** | Free | Freemium | Free | Free + Cloud | Freemium |
| **Guardrails** | ✅ Built-in | ⚠️ External | ❌ No | ❌ No | ⚠️ Limited |
| **AI Optimizer** | ✅ Yes | ⚠️ Limited | ❌ No | ❌ No | ⚠️ Basic |
| **Conversation Eval** | ✅✅ Native | ✅ Good | ⚠️ Limited | ✅ Good | ✅ Good |

---

## 2. Complete Architecture

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Your Application                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  RAG System  │  │    Agents    │  │   Chatbots   │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                  │                  │         │
│         └──────────────────┼──────────────────┘         │
│                            ▼                            │
│                   ┌────────────────┐                    │
│                   │   Opik SDK     │                    │
│                   │  @track()      │                    │
│                   └────────┬───────┘                    │
└────────────────────────────┼────────────────────────────┘
                             ▼
        ┌────────────────────────────────────┐
        │     Opik Platform (Self-hosted     │
        │         or Cloud)                  │
        ├────────────────────────────────────┤
        │  ┌──────────────────────────────┐  │
        │  │    API Layer (REST/gRPC)     │  │
        │  └──────────────┬───────────────┘  │
        │                 ▼                   │
        │  ┌──────────────────────────────┐  │
        │  │    Backend Services          │  │
        │  │  • Trace Ingestion           │  │
        │  │  • Evaluation Engine         │  │
        │  │  • Prompt Management         │  │
        │  │  • Gateway Routing           │  │
        │  │  • Alert System              │  │
        │  └──────────────┬───────────────┘  │
        │                 ▼                   │
        │  ┌──────────────────────────────┐  │
        │  │    Data Layer                │  │
        │  │  • ClickHouse (Analytics)    │  │
        │  │  • MinIO (Attachments)       │  │
        │  │  • PostgreSQL (Metadata)     │  │
        │  └──────────────┬───────────────┘  │
        └─────────────────┼──────────────────┘
                          ▼
        ┌────────────────────────────────────┐
        │         Frontend UI                │
        │  • Trace Explorer                  │
        │  • Evaluation Dashboard            │
        │  • Prompt Playground               │
        │  • Analytics & Charts              │
        └────────────────────────────────────┘
```

### 2.2 Data Model

**Hierarchical Structure:**

```python
Project
├── Traces (Complete execution paths)
│   ├── Trace ID
│   ├── Input/Output
│   ├── Metadata
│   ├── Duration
│   ├── Cost
│   └── Spans (Individual operations)
│       ├── Span ID
│       ├── Parent Span ID
│       ├── Type (llm, tool, chain)
│       ├── Input/Output
│       ├── Metadata
│       └── Feedback Scores
├── Threads (Conversation sequences)
│   ├── Thread ID
│   └── Multiple Traces (ordered)
├── Datasets (Test collections)
│   ├── Dataset Items
│   └── Expected Outputs
└── Experiments (Evaluation runs)
    ├── Experiment ID
    ├── Dataset Reference
    └── Results/Metrics
```

### 2.3 Component Breakdown

**SDK Components:**
- **Decorator (@track)**: Automatic instrumentation
- **Client (Opik())**: Manual logging interface
- **Context Managers**: Lifecycle-aware tracing
- **Framework Wrappers**: Pre-built integrations
- **Batching Engine**: Background transmission

**Platform Components:**
- **Trace Ingestion**: High-throughput data pipeline
- **Evaluation Engine**: Parallel metric computation
- **Prompt Library**: Version-controlled storage
- **Gateway**: Multi-provider routing
- **Guardrails**: Real-time content filtering
- **Analytics Engine**: Query and aggregation

---

## 3. Installation & Setup

### 3.1 Cloud Setup (Fastest)

**Step 1: Create Account**
```bash
# Visit https://www.comet.com/opik
# Sign up for free account
```

**Step 2: Install Python SDK**
```bash
pip install opik
```

**Step 3: Configure**
```bash
opik configure
# Follow prompts to enter API key and workspace
```

**Step 4: Verify Installation**
```python
from opik import track

@track
def hello_opik(name: str):
    return f"Hello, {name}!"

result = hello_opik("World")
print(result)
# Check traces at: https://www.comet.com/opik/<your-workspace>
```

### 3.2 TypeScript Setup

**Installation:**
```bash
npm install opik
# or
yarn add opik
```

**Configuration:**
```bash
npx opik-ts configure
# Enter API key when prompted
```

**Basic Usage:**
```typescript
import { Opik } from "opik";

const client = new Opik();

const trace = client.trace({
  name: "my-app",
  input: { prompt: "What is AI?" },
  output: { response: "AI is..." },
});

trace.end();
await client.flush(); // Ensure data is sent
```

### 3.3 Self-Hosted Deployment

**Docker Compose (Development):**
```bash
# Clone repository
git clone https://github.com/comet-ml/opik.git
cd opik/deployment/docker-compose

# Start services
docker-compose up -d

# Access UI at http://localhost:5173
```

**Kubernetes (Production):**
```bash
# Add Helm repository
helm repo add opik https://comet-ml.github.io/opik
helm repo update

# Install with custom values
helm install opik opik/opik \
  --set persistence.enabled=true \
  --set ingress.enabled=true \
  --set ingress.host=opik.yourdomain.com

# Configure SDK to use self-hosted instance
export OPIK_URL_OVERRIDE=https://opik.yourdomain.com
```

**Environment Variables:**
```bash
# API Configuration
export OPIK_API_KEY="your-api-key"
export OPIK_WORKSPACE="your-workspace"
export OPIK_URL_OVERRIDE="https://custom-instance.com"  # Optional

# Project Configuration
export OPIK_PROJECT_NAME="my-project"  # Default project

# Performance Tuning
export OPIK_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
export OPIK_BATCH_SIZE="100"  # Traces per batch
export OPIK_FLUSH_INTERVAL="10"  # Seconds

# Disable Tracking (for testing)
export OPIK_TRACK_DISABLE="true"  # Python only
```

### 3.4 Framework-Specific Setup

**OpenAI Integration:**
```python
from opik.integrations.openai import track_openai
from openai import OpenAI

# Wrap client
client = OpenAI(api_key="...")
client = track_openai(client)

# All calls now automatically traced
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**LangChain Integration:**
```python
from opik.integrations.langchain import OpikTracer
from langchain.chains import LLMChain

# Create tracer
tracer = OpikTracer()

# Use in chain
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(input_text, callbacks=[tracer])
```

**LangGraph Integration:**
```python
from opik.integrations.langgraph import track_langgraph
from langgraph.graph import StateGraph

# Wrap graph
graph = StateGraph(...)
graph = track_langgraph(graph)

# Execution automatically traced
result = graph.invoke({"input": "..."})
```

---

## 4. Core Concepts

### 4.1 Traces

**Definition:** A trace represents the complete execution path of your LLM application, capturing all operations from start to finish.

**Key Properties:**
- **Unique ID**: Globally unique identifier
- **Project**: Organization/categorization
- **Input/Output**: Request and response data
- **Metadata**: Custom tags, user IDs, session info
- **Duration**: Total execution time
- **Cost**: Cumulative LLM spending
- **Feedback Scores**: User ratings or automated metrics

**Creating Traces:**

```python
from opik import Opik

client = Opik()

# Method 1: Decorator (automatic)
@track(project_name="my-app")
def my_function(input_text):
    return process(input_text)

# Method 2: Manual (explicit control)
trace = client.trace(
    name="user-query",
    input={"query": "What is AI?"},
    metadata={"user_id": "user123", "session": "abc"},
    tags=["production", "chatbot"]
)

# ... processing ...

trace.update(
    output={"answer": "AI is..."},
    feedback_scores=[{"name": "quality", "value": 0.95}]
)
trace.end()

# Method 3: Context Manager (automatic cleanup)
with opik.start_as_current_trace(name="my-trace") as trace:
    # Operations here
    result = process_data()
    trace.update(output={"result": result})
# Automatically ended when exiting context
```

### 4.2 Spans

**Definition:** Spans represent individual operations within a trace, such as LLM calls, tool invocations, or processing steps.

**Span Types:**
- **llm**: Language model calls
- **tool**: External tool/API invocations
- **chain**: Sequential operations
- **retriever**: Document retrieval
- **general**: Other operations

**Creating Spans:**

```python
# Within a traced function
@track
def rag_pipeline(query):
    # Each function call creates a nested span
    context = retrieve_context(query)  # Span 1
    answer = generate_answer(query, context)  # Span 2
    return answer

@track
def retrieve_context(query):
    # Implementation
    return ["doc1", "doc2"]

@track(type="llm")
def generate_answer(query, context):
    # LLM call
    return "answer"

# Manual spans
trace = client.trace(name="rag")
with trace.span(
    name="retrieval",
    type="retriever",
    input={"query": query}
) as span:
    results = vector_db.search(query)
    span.update(output={"documents": results})
```

### 4.3 Threads

**Definition:** Threads group multiple traces into conversation sequences, enabling multi-turn interaction tracking.

**Use Cases:**
- Chatbot conversations
- Multi-step agent tasks
- Long-running sessions

**Creating Threads:**

```python
import uuid

# Create consistent thread ID for conversation
thread_id = str(uuid.uuid4())

# First message
@track(metadata={"thread_id": thread_id})
def process_message_1(user_input):
    return "Response 1"

# Second message (same thread)
@track(metadata={"thread_id": thread_id})
def process_message_2(user_input):
    return "Response 2"

# View as conversation in Opik UI
```

### 4.4 Projects

**Definition:** Projects organize traces, experiments, and datasets into logical groups.

**Setting Projects:**

```python
# Method 1: Environment variable (global)
import os
os.environ["OPIK_PROJECT_NAME"] = "my-project"

# Method 2: Decorator parameter
@track(project_name="specific-project")
def my_function():
    pass

# Method 3: Client initialization
client = Opik(project_name="client-project")
```

### 4.5 Datasets

**Definition:** Collections of test cases with inputs and expected outputs for systematic evaluation.

**Creating Datasets:**

```python
from opik import Opik

client = Opik()

# Create dataset
dataset = client.create_dataset(
    name="qa-dataset",
    description="Customer support QA pairs"
)

# Add items
dataset.add_items([
    {
        "input": {"question": "How do I reset my password?"},
        "expected_output": {"answer": "Visit /reset-password..."}
    },
    {
        "input": {"question": "What are your hours?"},
        "expected_output": {"answer": "9am-5pm EST"}
    }
])

# Load for evaluation
dataset = client.get_dataset(name="qa-dataset")
```

### 4.6 Experiments

**Definition:** Evaluation runs that systematically test your application against a dataset.

**Running Experiments:**

```python
from opik import evaluate

# Define evaluation task
def eval_task(dataset_item):
    question = dataset_item["input"]["question"]
    answer = my_app(question)
    return {"answer": answer}

# Run experiment
experiment = evaluate(
    experiment_name="v1-baseline",
    dataset=dataset,
    task=eval_task,
    scoring_metrics=[
        hallucination_metric(),
        answer_relevance_metric()
    ]
)

# View results
print(f"Average score: {experiment.average_score}")
```

### 4.7 Feedback Scores

**Definition:** Quantitative or qualitative assessments attached to traces or spans.

**Types:**
- **Numerical**: 0-1 scores (e.g., 0.87)
- **Boolean**: Pass/fail
- **Categorical**: Labels/classifications

**Adding Feedback:**

```python
# During trace creation
trace.update(feedback_scores=[
    {"name": "quality", "value": 0.92},
    {"name": "relevance", "value": 0.88},
    {"name": "safe", "value": 1.0}
])

# After trace completion (e.g., user feedback)
client.add_feedback_score(
    trace_id="trace-123",
    name="user_rating",
    value=5.0,
    category_name="user_feedback"
)
```

---

## 5. Complete Examples Section

### 5.1 Basic RAG System

```python
from opik import track
from opik.integrations.openai import track_openai
from openai import OpenAI
import chromadb

# Initialize clients
openai_client = track_openai(OpenAI(api_key="..."))
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("docs")

@track(project_name="rag-demo")
def rag_query(question: str):
    """Complete RAG pipeline with automatic tracing."""

    # Step 1: Retrieve context (auto-traced as span)
    context = retrieve_context(question)

    # Step 2: Generate answer (auto-traced as span)
    answer = generate_answer(question, context)

    return answer

@track(type="retriever")
def retrieve_context(question: str) -> list[str]:
    """Retrieve relevant documents."""
    results = collection.query(
        query_texts=[question],
        n_results=3
    )
    return results["documents"][0]

@track(type="llm")
def generate_answer(question: str, context: list[str]) -> str:
    """Generate answer using LLM."""
    context_str = "\n".join(context)

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Context: {context_str}"},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content

# Usage
answer = rag_query("What is machine learning?")
print(answer)
# View trace at Opik UI with full span breakdown
```

### 5.2 Agent with Tool Calling

```python
from opik import track
import json

@track(project_name="agent-demo")
def agent(task: str):
    """Multi-step agent with tool calls."""

    # Plan (LLM)
    plan = create_plan(task)

    # Execute tools
    results = []
    for step in plan["steps"]:
        result = execute_tool(step["tool"], step["params"])
        results.append(result)

    # Synthesize
    final_answer = synthesize_results(task, results)

    return final_answer

@track(type="llm")
def create_plan(task: str) -> dict:
    """Create execution plan."""
    # LLM call to generate plan
    return {
        "steps": [
            {"tool": "search", "params": {"query": "..."}},
            {"tool": "calculate", "params": {"expr": "..."}}
        ]
    }

@track(type="tool")
def execute_tool(tool_name: str, params: dict):
    """Execute specific tool."""
    if tool_name == "search":
        return web_search(params["query"])
    elif tool_name == "calculate":
        return evaluate(params["expr"])
    # ... more tools

@track
def web_search(query: str) -> list[dict]:
    """Search the web."""
    # Implementation
    return [{"title": "Result 1", "url": "..."}]

@track(type="llm")
def synthesize_results(task: str, results: list) -> str:
    """Combine results into final answer."""
    # LLM synthesis
    return "Final answer based on results..."

# Usage
answer = agent("What's the current stock price of AAPL?")
```

### 5.3 Multi-Turn Chatbot

```python
from opik import track
import uuid

class Chatbot:
    def __init__(self, project_name="chatbot"):
        self.project = project_name
        self.thread_id = str(uuid.uuid4())
        self.conversation_history = []

    @track(project_name="chatbot")
    def chat(self, user_message: str) -> str:
        """Process single message."""

        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Generate response with context
        response = self.generate_response(
            user_message,
            self.conversation_history
        )

        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response

    @track(
        type="llm",
        metadata=lambda self: {"thread_id": self.thread_id}
    )
    def generate_response(self, message: str, history: list) -> str:
        """Generate response using LLM."""
        from opik.integrations.openai import track_openai
        from openai import OpenAI

        client = track_openai(OpenAI())

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=history
        )

        return response.choices[0].message.content

# Usage
bot = Chatbot()
print(bot.chat("Hello!"))
print(bot.chat("What's the weather like?"))
print(bot.chat("Thanks!"))
# All messages grouped by thread_id in Opik UI
```

### 5.4 Evaluation Pipeline

```python
from opik import Opik, evaluate
from opik.evaluation.metrics import (
    hallucination_metric,
    answer_relevance_metric
)

client = Opik()

# Create dataset
dataset = client.create_dataset(
    name="qa-eval",
    description="QA evaluation set"
)

dataset.add_items([
    {
        "input": {"question": "What is Python?"},
        "expected_output": {
            "answer": "Python is a high-level programming language..."
        }
    },
    {
        "input": {"question": "What is machine learning?"},
        "expected_output": {
            "answer": "Machine learning is a subset of AI..."
        }
    }
])

# Define task
def qa_task(item):
    question = item["input"]["question"]
    answer = my_qa_system(question)  # Your implementation
    return {"answer": answer}

# Run evaluation
results = evaluate(
    experiment_name="baseline-v1",
    dataset=dataset,
    task=qa_task,
    scoring_metrics=[
        hallucination_metric(),
        answer_relevance_metric()
    ]
)

# Analyze results
print(f"Average hallucination score: {results.mean('hallucination')}")
print(f"Average relevance score: {results.mean('answer_relevance')}")

# Compare experiments
experiment_v2 = evaluate(
    experiment_name="improved-v2",
    dataset=dataset,
    task=improved_qa_task,
    scoring_metrics=[
        hallucination_metric(),
        answer_relevance_metric()
    ]
)

# View comparison in Opik UI
```

### 5.5 Production Monitoring

```python
from opik import track
from opik.integrations.openai import track_openai
from openai import OpenAI
import time

# Initialize
client = track_openai(OpenAI())

@track(
    project_name="production",
    metadata=lambda **kwargs: {
        "user_id": kwargs.get("user_id"),
        "environment": "prod",
        "timestamp": time.time()
    }
)
def production_endpoint(query: str, user_id: str):
    """Production endpoint with monitoring."""

    try:
        # Process query
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": query}]
        )

        answer = response.choices[0].message.content

        # Log cost
        cost = calculate_cost(response.usage)

        return {
            "answer": answer,
            "cost": cost,
            "status": "success"
        }

    except Exception as e:
        # Error tracking
        return {
            "error": str(e),
            "status": "error"
        }

def calculate_cost(usage):
    """Calculate LLM cost."""
    input_cost = usage.prompt_tokens * 0.00003  # Example rate
    output_cost = usage.completion_tokens * 0.00006
    return input_cost + output_cost

# Usage
result = production_endpoint(
    query="What is AI?",
    user_id="user_12345"
)

# Monitor in Opik:
# - Real-time traces
# - Cost tracking
# - Error rates
# - Latency percentiles
```

### 5.6 Custom Metric Example

```python
from opik.evaluation.metrics import base_metric, score_result

@base_metric
def custom_factuality_metric(output: str, expected_output: str, **kwargs):
    """Custom metric for factuality checking."""

    from opik.integrations.openai import track_openai
    from openai import OpenAI

    client = track_openai(OpenAI())

    # Use LLM as judge
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Rate factuality from 0-1. Output only the number."
            },
            {
                "role": "user",
                "content": f"Output: {output}\nExpected: {expected_output}"
            }
        ]
    )

    score = float(response.choices[0].message.content.strip())

    return score_result(
        name="factuality",
        value=score,
        reason=f"Factuality score based on comparison"
    )

# Use in evaluation
results = evaluate(
    experiment_name="with-custom-metric",
    dataset=dataset,
    task=my_task,
    scoring_metrics=[
        custom_factuality_metric()
    ]
)
```

---

## 6. Advanced Usage

### 6.1 Gateway Configuration

**Setting Up Multi-Provider Gateway:**

```python
from opik.gateway import OpikGateway

# Initialize gateway
gateway = OpikGateway(
    api_key="opik-key",
    providers={
        "openai": {"api_key": "sk-..."},
        "anthropic": {"api_key": "sk-ant-..."},
        "google": {"api_key": "..."}
    },
    routing_strategy="cost-optimized"  # or "latency-optimized", "quality-first"
)

# Use gateway (automatically routes to best provider)
response = gateway.chat.completions.create(
    messages=[{"role": "user", "content": "Hello"}],
    model="gpt-4o",  # Can be overridden by routing
    fallback_models=["claude-3-5-sonnet", "gemini-2.0-flash"]
)

# Automatic failover and load balancing
```

### 6.2 Guardrails Implementation

```python
from opik.guardrails import ContentGuardrail, create_guardrail

# Pre-built guardrails
guardrail = ContentGuardrail(
    check_pii=True,
    check_toxicity=True,
    check_prompt_injection=True,
    threshold=0.8
)

@track
@guardrail.protect
def protected_endpoint(user_input: str):
    """Endpoint with guardrails."""
    # Process only if guardrails pass
    response = generate_response(user_input)
    return response

# Custom guardrail
@create_guardrail
def custom_business_rule(input_text: str, output_text: str):
    """Custom validation logic."""

    # Check for prohibited terms
    prohibited = ["confidential", "internal"]

    for term in prohibited:
        if term in output_text.lower():
            return {
                "passed": False,
                "reason": f"Output contains prohibited term: {term}"
            }

    return {"passed": True}

# Apply
@custom_business_rule.protect
def business_endpoint(query):
    return process(query)
```

### 6.3 Advanced Evaluation Strategies

**Pairwise Comparison:**

```python
from opik import evaluate
from opik.evaluation.metrics import pairwise_comparison_metric

# Compare two models
baseline_results = evaluate(
    experiment_name="baseline-gpt-4",
    dataset=dataset,
    task=lambda item: gpt4_task(item)
)

improved_results = evaluate(
    experiment_name="improved-gpt-4o",
    dataset=dataset,
    task=lambda item: gpt4o_task(item)
)

# Pairwise comparison
comparison = pairwise_comparison_metric(
    baseline=baseline_results,
    improved=improved_results,
    metric="quality"
)

print(f"Win rate: {comparison.win_rate}")
print(f"Statistical significance: {comparison.p_value < 0.05}")
```

**Multi-Turn Evaluation:**

```python
from opik.evaluation.metrics import conversation_coherence_metric

# Evaluate conversations
def conversation_task(item):
    """Multi-turn task."""
    thread_id = str(uuid.uuid4())
    responses = []

    for turn in item["input"]["turns"]:
        response = chatbot.process(
            turn,
            thread_id=thread_id
        )
        responses.append(response)

    return {"conversation": responses}

results = evaluate(
    experiment_name="chatbot-eval",
    dataset=conversation_dataset,
    task=conversation_task,
    scoring_metrics=[
        conversation_coherence_metric(),
        conversation_relevance_metric()
    ]
)
```

### 6.4 Batch Processing

```python
from opik import Opik
import asyncio

client = Opik()

# Batch trace creation
traces = [
    client.trace(
        name=f"batch-{i}",
        input={"query": f"Query {i}"},
        output={"answer": f"Answer {i}"}
    )
    for i in range(1000)
]

# Efficient batch ending
for trace in traces:
    trace.end()

# Flush to ensure delivery
client.flush()

# Async batch processing
async def process_batch(items):
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)

@track
async def process_item(item):
    # Async processing
    result = await llm_call(item)
    return result
```

### 6.5 Real-Time Evaluation Rules

```python
from opik.rules import create_rule, AlertAction

# Create real-time evaluation rule
rule = create_rule(
    name="quality-threshold",
    condition="metrics.quality < 0.7",
    action=AlertAction(
        type="email",
        recipients=["team@company.com"],
        message="Quality threshold breached"
    ),
    enabled=True
)

# Rule automatically evaluates production traces
# and triggers alerts when condition matches

# Cost anomaly detection
cost_rule = create_rule(
    name="cost-spike",
    condition="cost > 0.50",  # Per trace
    action=AlertAction(
        type="slack",
        webhook_url="https://hooks.slack.com/...",
        message="High cost trace detected"
    )
)
```

### 6.6 Custom Anonymizers

```python
from opik.anonymizers import create_anonymizer
import re

@create_anonymizer
def email_anonymizer(text: str):
    """Anonymize email addresses."""
    return re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '[EMAIL]',
        text
    )

@create_anonymizer
def ssn_anonymizer(text: str):
    """Anonymize SSNs."""
    return re.sub(
        r'\b\d{3}-\d{2}-\d{4}\b',
        '[SSN]',
        text
    )

# Apply to traces
@track(
    anonymizers=[email_anonymizer, ssn_anonymizer]
)
def process_sensitive_data(text: str):
    """Process with automatic anonymization."""
    return analyze(text)

# PII is automatically removed before logging
```

---

## 7. Best Practices

### 7.1 Tracing Best Practices

**DO:**
- Use decorators for automatic instrumentation
- Apply consistent project naming
- Include metadata (user_id, session_id, environment)
- Use thread_id for conversations
- Call flush() in short-lived scripts
- Set appropriate span types (llm, tool, retriever)

**DON'T:**
- Log sensitive data without anonymization
- Create traces synchronously in hot paths
- Skip error handling in traced functions
- Use flush=True in production (performance impact)
- Create traces for every tiny operation

**Example:**

```python
# GOOD
@track(
    project_name="prod-chatbot",
    metadata=lambda user_id: {
        "user_id": user_id,
        "env": "production"
    }
)
def handle_message(message: str, user_id: str):
    return process(message)

# BAD
def handle_message(message, user_id):
    trace = client.trace(name="trace")  # Missing context
    result = process(message)  # No error handling
    trace.end()
    client.flush()  # Don't flush on every request!
    return result
```

### 7.2 Evaluation Best Practices

**Dataset Management:**
- Start with 20-50 high-quality examples
- Version datasets for reproducibility
- Include edge cases and failures
- Update datasets based on production issues
- Balance dataset across use case categories

**Metric Selection:**
- Use multiple complementary metrics
- Include both automated and human evaluation
- Start with pre-built metrics
- Create custom metrics for domain-specific needs
- Track cost and latency alongside quality

**Experiment Strategy:**
```python
# Good experiment workflow
1. Baseline evaluation
baseline = evaluate(
    experiment_name="baseline-v1.0",
    dataset=dataset,
    task=current_system,
    scoring_metrics=metrics
)

2. Make changes
# Improve prompt, switch model, etc.

3. Re-evaluate
improved = evaluate(
    experiment_name="improved-v1.1",
    dataset=dataset,  # Same dataset!
    task=improved_system,
    scoring_metrics=metrics  # Same metrics!
)

4. Compare results
delta = improved.average_score - baseline.average_score
print(f"Improvement: {delta:+.2%}")

5. Only deploy if statistically significant
if improved.p_value < 0.05 and delta > 0.05:
    deploy_to_production()
```

### 7.3 Production Monitoring

**Key Metrics to Track:**
- **Quality Metrics**: Automated scores on production data
- **Cost Metrics**: Per-request and aggregate spending
- **Latency Metrics**: P50, P95, P99 response times
- **Error Rates**: Failed requests and exceptions
- **User Feedback**: Thumbs up/down, ratings

**Alerting Strategy:**

```python
# Set up comprehensive alerts
alerts = [
    {
        "name": "quality-drop",
        "condition": "avg(quality) < 0.7 over 1 hour",
        "severity": "high"
    },
    {
        "name": "cost-spike",
        "condition": "sum(cost) > $100 over 1 hour",
        "severity": "medium"
    },
    {
        "name": "high-latency",
        "condition": "p95(latency) > 5s",
        "severity": "high"
    },
    {
        "name": "error-rate",
        "condition": "error_rate > 5% over 15 minutes",
        "severity": "critical"
    }
]
```

### 7.4 Cost Optimization

**Strategies:**

1. **Use Gateway Smart Routing**:
```python
# Route to cheapest provider meeting quality threshold
gateway = OpikGateway(routing_strategy="cost-optimized")
```

2. **Cache Expensive Operations**:
```python
from functools import lru_cache

@track
@lru_cache(maxsize=1000)
def expensive_llm_call(prompt: str):
    return client.chat.completions.create(...)
```

3. **Batch Requests**:
```python
# Process in batches instead of individual calls
results = client.batch.create(
    input_file_id="...",
    model="gpt-4o"
)
```

4. **Use Smaller Models for Simple Tasks**:
```python
def route_by_complexity(query: str):
    if is_simple(query):
        return call_gpt_4o_mini(query)  # Cheaper
    else:
        return call_gpt_4o(query)  # More capable
```

### 7.5 Security Best Practices

**API Key Management:**
```python
# GOOD: Use environment variables
import os
api_key = os.getenv("OPIK_API_KEY")

# BAD: Hardcode keys
api_key = "sk-..."  # Never do this!
```

**Data Privacy:**
```python
# Apply anonymization
@track(anonymizers=[pii_anonymizer])
def process_user_data(text):
    return analyze(text)

# Or manually sanitize
@track
def safe_process(text):
    sanitized = remove_pii(text)
    return analyze(sanitized)
```

**Access Control:**
- Use role-based access control (RBAC)
- Rotate API keys regularly
- Use separate projects for different teams
- Enable audit logging
- Restrict self-hosted instance access

---

## 8. Integration Guide

### 8.1 Framework Integrations

**LangChain:**
```python
from opik.integrations.langchain import OpikTracer
from langchain.chains import ConversationalRetrievalChain

tracer = OpikTracer(project_name="langchain-app")

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever
)

# Automatic tracing
result = chain(
    {"question": "...", "chat_history": []},
    callbacks=[tracer]
)
```

**LangGraph:**
```python
from opik.integrations.langgraph import track_langgraph
from langgraph.graph import StateGraph

graph = StateGraph(State)
# ... build graph ...

# Wrap for tracing
graph = track_langgraph(graph, project_name="langgraph-agent")

# All node executions traced
result = graph.invoke({"input": "..."})
```

**CrewAI:**
```python
from opik.integrations.crewai import track_crewai
from crewai import Crew, Agent, Task

# Wrap crew
crew = Crew(agents=[...], tasks=[...])
crew = track_crewai(crew, project_name="crewai-app")

# Automatic tracing
result = crew.kickoff()
```

**AutoGen:**
```python
from opik.integrations.autogen import OpikCallback
import autogen

callback = OpikCallback(project_name="autogen-app")

agent = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": [...]},
    callbacks=[callback]
)

# Traced conversations
agent.initiate_chat(user_proxy, message="...")
```

### 8.2 LLM Provider Integrations

**OpenAI:**
```python
from opik.integrations.openai import track_openai
from openai import OpenAI

client = track_openai(OpenAI(api_key="..."))

# All calls traced
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...]
)
```

**Anthropic:**
```python
from opik.integrations.anthropic import track_anthropic
from anthropic import Anthropic

client = track_anthropic(Anthropic(api_key="..."))

# Traced
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[...]
)
```

**Google Gemini:**
```python
from opik.integrations.google import track_gemini
import google.generativeai as genai

genai.configure(api_key="...")
model = track_gemini(genai.GenerativeModel("gemini-2.0-flash"))

response = model.generate_content("...")
```

**AWS Bedrock:**
```python
from opik.integrations.bedrock import track_bedrock
import boto3

bedrock = boto3.client("bedrock-runtime")
bedrock = track_bedrock(bedrock)

response = bedrock.invoke_model(
    modelId="anthropic.claude-3-sonnet",
    body=json.dumps({...})
)
```

### 8.3 RAG Integrations

**LlamaIndex:**
```python
from opik.integrations.llamaindex import OpikCallback
from llama_index.core import VectorStoreIndex

callback = OpikCallback(project_name="llamaindex-rag")

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(callbacks=[callback])

response = query_engine.query("What is RAG?")
```

**ChromaDB:**
```python
from opik import track
import chromadb

@track(type="retriever")
def retrieve_from_chroma(query: str):
    collection = chromadb.Client().get_collection("docs")
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    return results["documents"][0]
```

### 8.4 Voice Agent Integration

**LiveKit:**
```python
from opik.integrations.livekit import track_livekit
from livekit import rtc

# Wrap LiveKit agent
agent = track_livekit(
    livekit_agent,
    project_name="voice-agent"
)

# Voice interactions automatically traced
await agent.start()
```

### 8.5 Low-Code Platform Integrations

**Dify:**
```yaml
# In Dify workflow, add HTTP node
POST https://api.comet.com/opik/v1/traces
Headers:
  Authorization: Bearer ${OPIK_API_KEY}
Body:
  {
    "name": "dify-workflow",
    "input": "{{input}}",
    "output": "{{output}}"
  }
```

**Langflow:**
```python
# Add Opik component to Langflow
from opik import track
from langflow.custom import CustomComponent

class OpikTracedComponent(CustomComponent):
    @track
    def build(self, input_value: str):
        # Component logic
        return self.process(input_value)
```

**n8n:**
```json
{
  "nodes": [
    {
      "type": "n8n-nodes-base.httpRequest",
      "name": "Log to Opik",
      "parameters": {
        "url": "https://api.comet.com/opik/v1/traces",
        "method": "POST",
        "body": {
          "name": "n8n-workflow",
          "input": "={{ $json.input }}",
          "output": "={{ $json.output }}"
        }
      }
    }
  ]
}
```

---

## 9. Troubleshooting

### 9.1 Common Issues

**Issue: Traces Not Appearing**

```python
# Problem: Traces not sent
@track
def my_function():
    return "result"

my_function()
# Script exits before traces sent!

# Solution: Add flush
from opik import Opik
client = Opik()

my_function()
client.flush()  # Wait for traces to send
```

**Issue: API Key Errors**

```bash
# Check configuration
opik configure --verify

# Or test programmatically
from opik import Opik

try:
    client = Opik()
    print("✓ API key valid")
except Exception as e:
    print(f"✗ API key error: {e}")
```

**Issue: Self-Hosted Connection Fails**

```python
# Verify URL override
import os
print(os.getenv("OPIK_URL_OVERRIDE"))

# Test connection
import requests
response = requests.get(
    f"{os.getenv('OPIK_URL_OVERRIDE')}/api/health"
)
print(response.status_code)  # Should be 200
```

### 9.2 Performance Issues

**High Latency:**

```python
# Problem: Synchronous tracing blocking requests
@track
def slow_endpoint(query):
    # Trace blocking execution
    return process(query)

# Solution: Traces are async by default, but ensure batching
from opik import Opik

client = Opik()
# Increase batch size for higher throughput
os.environ["OPIK_BATCH_SIZE"] = "500"
```

**Memory Issues:**

```python
# Problem: Large outputs consuming memory
@track
def process_large_data():
    huge_result = generate_gigabytes_of_data()
    return huge_result  # Stored in memory for tracing!

# Solution: Truncate or summarize large outputs
@track
def process_large_data():
    huge_result = generate_gigabytes_of_data()
    summary = summarize(huge_result)
    return summary  # Only log summary
```

### 9.3 Integration Issues

**LangChain Callback Not Working:**

```python
# Problem: Callback not triggered
from opik.integrations.langchain import OpikTracer
tracer = OpikTracer()
chain.run(input)  # No traces!

# Solution: Pass callbacks explicitly
chain.run(input, callbacks=[tracer])

# Or set as global
from langchain.callbacks import set_handler
set_handler(tracer)
```

**OpenAI Wrapper Conflicts:**

```python
# Problem: Multiple wrappers conflict
from opik.integrations.openai import track_openai
from other_tool import wrap_openai

client = wrap_openai(OpenAI())
client = track_openai(client)  # May not work!

# Solution: Only use one wrapper or check compatibility
client = track_openai(OpenAI())  # Opik first
# Other tools should support already-wrapped clients
```

### 9.4 Debugging Tools

**Enable Debug Logging:**

```python
import logging
import os

# Set environment variable
os.environ["OPIK_LOG_LEVEL"] = "DEBUG"

# Or configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("opik")
logger.setLevel(logging.DEBUG)
```

**Trace Verification:**

```python
from opik import Opik

client = Opik()

# Manual trace with verification
trace = client.trace(
    name="debug-trace",
    input={"test": "data"}
)
print(f"Trace ID: {trace.id}")

trace.end()
client.flush()

# Check in UI: https://www.comet.com/opik/<workspace>/traces/<trace-id>
```

---

## 10. API Reference

### 10.1 Decorator API

**@track**

```python
from opik import track

@track(
    name: Optional[str] = None,              # Trace/span name
    project_name: Optional[str] = None,       # Project assignment
    type: Optional[str] = None,               # Span type: llm, tool, chain
    metadata: Optional[dict | Callable] = None,  # Custom metadata
    tags: Optional[list[str]] = None,         # Tags
    capture_input: bool = True,               # Log input
    capture_output: bool = True,              # Log output
    anonymizers: Optional[list] = None        # Data anonymizers
)
def my_function(...):
    pass
```

### 10.2 Client API

**Opik()**

```python
from opik import Opik

client = Opik(
    api_key: Optional[str] = None,            # Defaults to env var
    workspace: Optional[str] = None,          # Workspace name
    project_name: Optional[str] = None,       # Default project
    url: Optional[str] = None                 # Custom instance URL
)
```

**Methods:**

```python
# Trace management
trace = client.trace(
    name: str,
    input: dict,
    output: Optional[dict] = None,
    metadata: Optional[dict] = None,
    tags: Optional[list[str]] = None
)

# Dataset management
dataset = client.create_dataset(name: str, description: str)
dataset = client.get_dataset(name: str)
datasets = client.list_datasets()

# Project management
project = client.create_project(name: str)
projects = client.list_projects()

# Feedback
client.add_feedback_score(
    trace_id: str,
    name: str,
    value: float,
    category_name: Optional[str] = None
)

# Flush pending traces
client.flush(timeout: float = 30.0)
```

### 10.3 Trace API

```python
# Update trace
trace.update(
    output: Optional[dict] = None,
    feedback_scores: Optional[list[dict]] = None,
    metadata: Optional[dict] = None
)

# Create span
span = trace.span(
    name: str,
    type: Optional[str] = None,
    input: Optional[dict] = None,
    output: Optional[dict] = None
)

# End trace
trace.end()
```

### 10.4 Evaluation API

**evaluate()**

```python
from opik import evaluate

results = evaluate(
    experiment_name: str,                     # Experiment identifier
    dataset: Dataset,                         # Test dataset
    task: Callable,                           # Function to evaluate
    scoring_metrics: list[Metric],            # Metrics to compute
    experiment_config: Optional[dict] = None, # Config metadata
    nb_samples: Optional[int] = None          # Limit dataset size
)
```

**Built-in Metrics:**

```python
from opik.evaluation.metrics import (
    hallucination_metric,
    answer_relevance_metric,
    context_precision_metric,
    context_recall_metric,
    summarization_coherence_metric,
    compliance_risk_metric,
    moderation_metric
)

# Usage
metric = hallucination_metric(threshold=0.8)
```

### 10.5 Context Managers

```python
from opik import start_as_current_trace, start_as_current_span

# Trace context
with start_as_current_trace(
    name="my-trace",
    project_name="project"
) as trace:
    # Operations
    result = process()
    trace.update(output={"result": result})
# Automatically ended

# Span context
with start_as_current_span(
    name="my-span",
    type="llm"
) as span:
    result = llm_call()
    span.update(output={"result": result})
```

---

## 11. Performance & Optimization

### 11.1 Batching Configuration

**Optimal Settings:**

```python
import os

# High-throughput applications
os.environ["OPIK_BATCH_SIZE"] = "1000"
os.environ["OPIK_FLUSH_INTERVAL"] = "30"  # seconds

# Low-latency applications
os.environ["OPIK_BATCH_SIZE"] = "100"
os.environ["OPIK_FLUSH_INTERVAL"] = "5"

# Default (balanced)
# BATCH_SIZE: 100
# FLUSH_INTERVAL: 10
```

### 11.2 Network Optimization

**Connection Pooling:**

```python
from opik import Opik

# Reuse client instance
client = Opik()

# Good: Single client for all requests
@track
def handler1():
    pass

@track
def handler2():
    pass

# Bad: Creating new client each time
def bad_handler():
    client = Opik()  # Don't do this repeatedly!
    # ...
```

**Compression:**

```python
# Enable gzip compression (automatic in SDK)
import os
os.environ["OPIK_COMPRESSION"] = "gzip"
```

### 11.3 Data Size Management

**Truncation:**

```python
@track
def process_large_input(data: str):
    # Problem: Large inputs/outputs
    result = analyze(data)
    return result  # Could be megabytes!

# Solution: Truncate
@track
def process_large_input(data: str):
    result = analyze(data)

    # Truncate for logging
    truncated_result = result[:10000] + "..." if len(result) > 10000 else result
    return truncated_result
```

**Selective Logging:**

```python
@track(
    capture_input=False,   # Don't log input
    capture_output=True    # Only log output
)
def privacy_sensitive_function(secret_data):
    return process(secret_data)
```

### 11.4 Cost Optimization

**Token Usage Tracking:**

```python
@track
def track_tokens(prompt: str):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    # Automatically logged by Opik OpenAI integration:
    # - prompt_tokens
    # - completion_tokens
    # - total_tokens
    # - estimated_cost

    return response.choices[0].message.content
```

**Provider Cost Comparison:**

```python
from opik.analytics import get_cost_by_provider

# Analyze costs across providers
costs = get_cost_by_provider(
    project_name="my-app",
    start_date="2026-01-01",
    end_date="2026-01-18"
)

print(f"OpenAI: ${costs['openai']:.2f}")
print(f"Anthropic: ${costs['anthropic']:.2f}")
print(f"Google: ${costs['google']:.2f}")

# Identify expensive queries
expensive_traces = get_traces(
    project_name="my-app",
    filter="cost > 0.50",
    sort="cost DESC",
    limit=10
)
```

### 11.5 Self-Hosted Performance

**Database Tuning (ClickHouse):**

```yaml
# clickhouse-config.yaml
max_memory_usage: 10000000000  # 10 GB
max_threads: 8
max_execution_time: 300  # 5 minutes
```

**Storage Optimization:**

```yaml
# Retention policies
traces:
  retention_days: 90

metrics:
  retention_days: 180

datasets:
  retention_days: 365
```

---

## 12. Security Considerations

### 12.1 Data Privacy

**PII Anonymization:**

```python
from opik.anonymizers import (
    email_anonymizer,
    phone_anonymizer,
    ssn_anonymizer,
    ip_address_anonymizer
)

@track(
    anonymizers=[
        email_anonymizer,
        phone_anonymizer,
        ssn_anonymizer
    ]
)
def process_user_data(text: str):
    return analyze(text)

# Input/output automatically anonymized before logging
```

**Custom Anonymization:**

```python
from opik.anonymizers import create_anonymizer
import re

@create_anonymizer
def credit_card_anonymizer(text: str):
    """Anonymize credit card numbers."""
    return re.sub(
        r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
        '[CREDIT_CARD]',
        text
    )
```

### 12.2 Access Control

**API Key Rotation:**

```bash
# Generate new key in Opik UI
# Update environment
export OPIK_API_KEY="new-key-..."

# Revoke old key in UI
```

**Project-Based Access:**

```python
# Separate projects for different teams/environments
dev_client = Opik(project_name="dev")
staging_client = Opik(project_name="staging")
prod_client = Opik(project_name="production")

# Configure RBAC in self-hosted:
# - Read-only for developers
# - Write access for services
# - Admin access for DevOps
```

### 12.3 Compliance

**GDPR Compliance:**

```python
# Right to erasure
client.delete_traces(
    filter=f"metadata.user_id = '{user_id}'"
)

# Data export
user_data = client.export_traces(
    filter=f"metadata.user_id = '{user_id}'",
    format="json"
)
```

**SOC 2 Considerations:**
- Enable audit logging
- Use encrypted connections (HTTPS/TLS)
- Implement access controls
- Regular key rotation
- Data retention policies

### 12.4 Network Security

**Self-Hosted Security:**

```yaml
# Kubernetes deployment with security
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opik
spec:
  template:
    spec:
      containers:
      - name: opik
        securityContext:
          runAsNonRoot: true
          readOnlyRootFilesystem: true
          capabilities:
            drop: ["ALL"]

      # Network policies
      networkPolicy:
        ingress:
          - from:
            - podSelector:
                matchLabels:
                  app: trusted-services
```

---

## 13. References & Resources

### 13.1 Official Documentation

- **Official Docs**: https://www.comet.com/docs/opik/
- **API Reference**: https://www.comet.com/docs/opik/api-reference
- **GitHub Repository**: https://github.com/comet-ml/opik
- **Changelog**: https://github.com/comet-ml/opik/releases

### 13.2 Community

- **Discord**: https://discord.gg/opik-community
- **GitHub Issues**: https://github.com/comet-ml/opik/issues
- **Stack Overflow**: Tag: `opik`
- **Twitter/X**: @CometML

### 13.3 Example Projects

**GitHub Examples:**
- https://github.com/comet-ml/opik/tree/main/examples
- RAG evaluation examples
- Agent monitoring examples
- Multi-framework integrations

**Notebooks:**
- Quickstart notebook
- Advanced evaluation techniques
- Production monitoring setup

### 13.4 Integration Guides

- LangChain integration guide
- LangGraph agent tracing
- OpenAI function calling
- CrewAI multi-agent systems
- LiveKit voice agents

### 13.5 Blog Posts & Tutorials

- "Getting Started with Opik"
- "Evaluating RAG Systems"
- "Production LLM Monitoring"
- "Cost Optimization Strategies"
- "Building Custom Metrics"

### 13.6 Comparison Resources

- Opik vs LangSmith comparison
- Opik vs Phoenix comparison
- Open-source evaluation tools comparison
- When to use which tool

### 13.7 Video Resources

- YouTube: Opik overview and demos
- Conference talks on LLM observability
- Webinars on production LLM ops

---

## Appendix A: Quick Reference

### Installation
```bash
pip install opik
opik configure
```

### Basic Tracing
```python
from opik import track

@track
def my_function(input: str):
    return process(input)
```

### Evaluation
```python
from opik import evaluate
from opik.evaluation.metrics import hallucination_metric

results = evaluate(
    experiment_name="test",
    dataset=dataset,
    task=my_task,
    scoring_metrics=[hallucination_metric()]
)
```

### Key Concepts
- **Trace**: Complete execution path
- **Span**: Individual operation
- **Thread**: Conversation sequence
- **Dataset**: Test collection
- **Experiment**: Evaluation run

---

## Appendix B: Migration Guide

### From LangSmith

```python
# LangSmith
from langsmith import Client
client = Client()

# Opik equivalent
from opik import Opik
client = Opik()

# LangSmith tracing
@traceable
def my_function():
    pass

# Opik tracing
@track
def my_function():
    pass
```

### From Phoenix

```python
# Phoenix
import phoenix as px
px.launch_app()

# Opik (cloud or self-hosted)
from opik import Opik
client = Opik()
# UI at: https://www.comet.com/opik/
```

### From Weights & Biases

```python
# W&B
import wandb
wandb.init(project="my-project")
wandb.log({"metric": value})

# Opik
from opik import track

@track(project_name="my-project")
def my_function():
    # Automatic logging
    return result
```

---

**End of Opik Deep-Dive Guide**

For the latest updates, visit: https://www.comet.com/docs/opik/
