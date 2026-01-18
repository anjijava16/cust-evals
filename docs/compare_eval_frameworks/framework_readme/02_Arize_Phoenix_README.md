# Arize Phoenix - Comprehensive Deep Dive Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture & Design](#architecture--design)
3. [Installation & Setup](#installation--setup)
4. [Core Concepts](#core-concepts)
5. [Production-Ready Examples](#production-ready-examples)
6. [Advanced Usage](#advanced-usage)
7. [Best Practices](#best-practices)
8. [Integration Guide](#integration-guide)
9. [Troubleshooting](#troubleshooting)
10. [API Reference](#api-reference)
11. [Performance & Security](#performance--security)
12. [References & Resources](#references--resources)

---

## Introduction

### What is Arize Phoenix?

Arize Phoenix is an open-source observability and evaluation platform specifically designed for Large Language Model (LLM) applications. Built on OpenTelemetry standards, Phoenix provides comprehensive tracing, monitoring, and evaluation capabilities for AI systems in production.

**Key Features:**
- OpenTelemetry-based distributed tracing for LLM applications
- Real-time observability with visual trace inspection
- Built-in LLM evaluation metrics (relevance, hallucination, toxicity)
- Support for RAG (Retrieval-Augmented Generation) evaluation
- Integration with major LLM frameworks (LangChain, LlamaIndex, DSPy)
- Embeddings analysis and drift detection
- No-code UI for trace exploration and analysis
- Self-hosted or cloud deployment options

**Use Cases:**
- Production LLM application monitoring
- RAG pipeline optimization
- Prompt engineering and testing
- Model performance evaluation
- Debugging complex agent workflows
- Cost and latency tracking
- Quality assurance for LLM outputs

### Why Phoenix?

**Advantages:**
1. **Open Standards**: Built on OpenTelemetry, ensuring vendor neutrality
2. **Framework Agnostic**: Works with any LLM provider or framework
3. **Real-time Visibility**: Live trace inspection without deployment delays
4. **Comprehensive Metrics**: Pre-built evaluators for common LLM tasks
5. **Developer-Friendly**: Intuitive UI and simple API integration
6. **Production-Ready**: Handles high-volume production workloads
7. **Open Source**: Free to use with active community support

**When to Use Phoenix:**
- You need OpenTelemetry-compatible LLM observability
- You want framework-agnostic tracing solutions
- You require real-time production monitoring
- You need to debug complex multi-step LLM workflows
- You want to evaluate RAG system performance
- You need embeddings drift detection

**When to Consider Alternatives:**
- You need only basic logging (use native logging)
- You're locked into a specific vendor ecosystem
- You need advanced security compliance features (consider enterprise solutions)

---

## Architecture & Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Phoenix Architecture                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  LangChain   │  │  LlamaIndex  │  │   Custom     │         │
│  │     App      │  │     App      │  │     App      │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
│         └──────────────────┴──────────────────┘                  │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │  Phoenix SDK     │
                    │  (Instrumentor)  │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────┐
│ OpenTelemetry  │  │   Phoenix       │  │  Exporters  │
│    Tracer      │  │   Evaluators    │  │  (OTLP)     │
└───────┬────────┘  └────────┬────────┘  └──────┬──────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                    Phoenix Server                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Collector  │→ │   Storage    │→ │   Query      │          │
│  │   (OTLP)     │  │   Engine     │  │   Engine     │          │
│  └──────────────┘  └──────────────┘  └──────┬───────┘          │
│                                              │                   │
└──────────────────────────────────────────────┼───────────────────┘
                                               │
┌──────────────────────────────────────────────▼───────────────────┐
│                    Phoenix UI                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Traces     │  │  Evaluations │  │  Embeddings  │          │
│  │   Viewer     │  │   Dashboard  │  │   Analysis   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└──────────────────────────────────────────────────────────────────┘
```

### Component Architecture

#### 1. Instrumentation Layer

**Phoenix Instrumentor:**
```python
from phoenix.otel import register

# Auto-instrumentation for popular frameworks
tracer_provider = register(
    project_name="my-llm-app",
    endpoint="http://localhost:6006/v1/traces"
)
```

**Supported Integrations:**
- **LangChain**: Automatic tracing of chains, agents, tools
- **LlamaIndex**: Query engine and retrieval tracing
- **OpenAI**: Direct API call instrumentation
- **Anthropic**: Claude API tracing
- **DSPy**: Program and module tracing
- **Custom**: Manual span creation for any code

#### 2. Trace Collection

**OpenTelemetry Protocol (OTLP):**
```
Application → OTLP Exporter → Phoenix Collector → Storage

Trace Structure:
├── Root Span (LLM Chain)
│   ├── Child Span (Retrieval)
│   │   ├── Embedding Generation
│   │   └── Vector Search
│   ├── Child Span (LLM Call)
│   │   ├── Prompt Formatting
│   │   ├── API Request
│   │   └── Response Parsing
│   └── Child Span (Output Processing)
```

#### 3. Storage & Query Engine

**Data Model:**
```python
Trace {
    trace_id: UUID
    project_name: String
    start_time: Timestamp
    end_time: Timestamp
    status: Enum[SUCCESS, ERROR]
    spans: List[Span]
    attributes: Dict[String, Any]
    evaluations: List[Evaluation]
}

Span {
    span_id: UUID
    parent_span_id: Optional[UUID]
    name: String
    span_kind: Enum[LLM, RETRIEVAL, CHAIN, TOOL]
    start_time: Timestamp
    end_time: Timestamp
    attributes: {
        input: {
            value: String,
            mime_type: String
        },
        output: {
            value: String,
            mime_type: String
        },
        llm: {
            model_name: String,
            token_count: {
                prompt: Integer,
                completion: Integer,
                total: Integer
            },
            invocation_parameters: Dict
        }
    }
    events: List[Event]
    status: SpanStatus
}
```

#### 4. Evaluation Engine

**Evaluator Pipeline:**
```
Trace Data → Evaluator Selection → LLM-as-Judge → Metric Computation → Storage

Built-in Evaluators:
- Hallucination Detection
- Relevance Assessment
- Toxicity Screening
- QA Correctness
- Summarization Quality
- Code Generation Quality
```

#### 5. UI & Visualization

**Phoenix UI Components:**
- Trace Timeline View
- Span Details Inspector
- Metrics Dashboard
- Embeddings Visualizer (UMAP/t-SNE)
- Search & Filter Interface
- Evaluation Results Display

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Trace Collection Flow                        │
└─────────────────────────────────────────────────────────────────┘

1. Application Execution
   ↓
2. Phoenix Instrumentation captures spans
   ↓
3. Spans enriched with attributes (I/O, tokens, model)
   ↓
4. OTLP Exporter batches and sends to Phoenix Server
   ↓
5. Phoenix Collector receives and validates
   ↓
6. Storage Engine persists traces
   ↓
7. Query Engine indexes for fast retrieval
   ↓
8. UI fetches and displays in real-time
   ↓
9. Evaluators run asynchronously on traces
   ↓
10. Evaluation results linked to traces

┌─────────────────────────────────────────────────────────────────┐
│                    Evaluation Flow                              │
└─────────────────────────────────────────────────────────────────┘

1. Trace completes and stored
   ↓
2. Evaluation trigger (auto/manual)
   ↓
3. Evaluator retrieves trace data
   ↓
4. LLM-as-Judge API call with evaluation template
   ↓
5. Parse LLM response for score/label
   ↓
6. Store evaluation result with trace_id
   ↓
7. UI updates with evaluation badge
```

### Deployment Architectures

#### Local Development Setup

```
┌─────────────────────────────────────────────────────┐
│              Developer Machine                      │
│                                                     │
│  ┌──────────────┐         ┌──────────────┐         │
│  │  Application │────────>│   Phoenix    │         │
│  │  (localhost) │         │   Server     │         │
│  │              │<────────│ (localhost)  │         │
│  └──────────────┘         └──────┬───────┘         │
│                                  │                  │
│                           ┌──────▼───────┐         │
│                           │  Browser     │         │
│                           │  (Phoenix UI)│         │
│                           └──────────────┘         │
└─────────────────────────────────────────────────────┘
```

#### Production Cloud Deployment

```
┌─────────────────────────────────────────────────────────────────┐
│                    Production Environment                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐
│  Application     │         │  Application     │
│  Instance 1      │         │  Instance N      │
└────────┬─────────┘         └────────┬─────────┘
         │                            │
         └────────────┬───────────────┘
                      │
              ┌───────▼────────┐
              │  Load Balancer │
              └───────┬────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
┌────────▼─────────┐    ┌─────────▼────────┐
│ Phoenix Server 1 │    │ Phoenix Server 2 │
│  (Collector)     │    │  (Collector)     │
└────────┬─────────┘    └─────────┬────────┘
         │                         │
         └────────────┬────────────┘
                      │
              ┌───────▼────────┐
              │  PostgreSQL    │
              │  (Trace Store) │
              └───────┬────────┘
                      │
              ┌───────▼────────┐
              │  Phoenix UI    │
              │  (Web Server)  │
              └────────────────┘
```

---

## Installation & Setup

### Prerequisites

**System Requirements:**
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended for production)
- 10GB disk space for trace storage
- Network access for OTLP export

**Dependencies:**
- OpenTelemetry SDK
- gRPC (for OTLP export)
- Compatible LLM frameworks (optional)

### Installation Methods

#### Method 1: Basic Installation (Recommended for Start)

```bash
# Install Phoenix server and client
pip install arize-phoenix

# Install with specific framework support
pip install "arize-phoenix[langchain]"
pip install "arize-phoenix[llama-index]"
pip install "arize-phoenix[openai]"

# Install all integrations
pip install "arize-phoenix[all]"
```

#### Method 2: Development Installation

```bash
# Clone repository
git clone https://github.com/Arize-ai/phoenix.git
cd phoenix

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

#### Method 3: Docker Installation

```bash
# Pull Phoenix image
docker pull arizephoenix/phoenix:latest

# Run Phoenix server
docker run -p 6006:6006 -p 4317:4317 arizephoenix/phoenix:latest

# With persistent storage
docker run -p 6006:6006 -p 4317:4317 \
  -v phoenix-data:/phoenix/data \
  arizephoenix/phoenix:latest
```

#### Method 4: Docker Compose (Production)

```yaml
# docker-compose.yml
version: '3.8'

services:
  phoenix:
    image: arizephoenix/phoenix:latest
    ports:
      - "6006:6006"  # UI
      - "4317:4317"  # OTLP gRPC
      - "4318:4318"  # OTLP HTTP
    environment:
      - PHOENIX_WORKING_DIR=/data
      - PHOENIX_PORT=6006
      - PHOENIX_GRPC_PORT=4317
    volumes:
      - phoenix-data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6006/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=phoenix
      - POSTGRES_USER=phoenix
      - POSTGRES_PASSWORD=phoenix_secret
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  phoenix-data:
  postgres-data:
```

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f phoenix

# Stop services
docker-compose down
```

### Starting Phoenix Server

#### Local Development Server

```python
# Method 1: Python API
import phoenix as px

# Launch Phoenix in notebook
session = px.launch_app()

# Launch with custom port
session = px.launch_app(port=6007)

# Launch with specific project
session = px.launch_app(project_name="my-project")
```

```bash
# Method 2: Command Line
python -m phoenix.server.main serve

# With custom configuration
python -m phoenix.server.main serve \
  --host 0.0.0.0 \
  --port 6006 \
  --grpc-port 4317

# Background mode
nohup python -m phoenix.server.main serve > phoenix.log 2>&1 &
```

#### Environment Variables

```bash
# .env file for Phoenix configuration
PHOENIX_PORT=6006
PHOENIX_GRPC_PORT=4317
PHOENIX_HOST=0.0.0.0
PHOENIX_WORKING_DIR=/data/phoenix
PHOENIX_SQL_DATABASE_URL=postgresql://user:pass@localhost/phoenix
PHOENIX_ENABLE_AUTH=false
PHOENIX_LOG_LEVEL=INFO

# Load environment
export $(cat .env | xargs)
```

### Client Configuration

#### Basic Setup

```python
# app.py
import os
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Set up Phoenix endpoint
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "http://localhost:6006"

# Configure tracer
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(
    SimpleSpanProcessor(
        OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces")
    )
)

# Register instrumentation
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
```

#### Advanced Setup with Custom Configuration

```python
# config.py
from dataclasses import dataclass
from typing import Optional
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from phoenix.otel import register

@dataclass
class PhoenixConfig:
    """Phoenix configuration settings"""
    endpoint: str = "http://localhost:6006"
    project_name: str = "default"
    environment: str = "development"
    service_version: str = "1.0.0"
    batch_size: int = 512
    max_export_batch_size: int = 512
    max_queue_size: int = 2048
    export_timeout_millis: int = 30000

def setup_phoenix(config: PhoenixConfig) -> TracerProvider:
    """
    Configure Phoenix with production-ready settings

    Args:
        config: Phoenix configuration object

    Returns:
        Configured TracerProvider instance
    """
    # Define resource attributes
    resource = Resource(attributes={
        SERVICE_NAME: config.project_name,
        "service.version": config.service_version,
        "deployment.environment": config.environment,
    })

    # Create tracer provider
    tracer_provider = TracerProvider(resource=resource)

    # Configure OTLP exporter with batching
    otlp_exporter = OTLPSpanExporter(
        endpoint=f"{config.endpoint}/v1/traces",
        timeout=config.export_timeout_millis // 1000,
    )

    # Add batch span processor for performance
    span_processor = BatchSpanProcessor(
        otlp_exporter,
        max_queue_size=config.max_queue_size,
        max_export_batch_size=config.max_export_batch_size,
        export_timeout_millis=config.export_timeout_millis,
    )

    tracer_provider.add_span_processor(span_processor)

    return tracer_provider

# Usage
config = PhoenixConfig(
    endpoint="http://phoenix.example.com:6006",
    project_name="production-rag-app",
    environment="production",
)

tracer_provider = setup_phoenix(config)
```

### Framework Integration Setup

#### LangChain Integration

```python
# langchain_setup.py
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

# Register Phoenix
tracer_provider = register(
    project_name="langchain-app",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrument LangChain
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

# Now all LangChain operations are traced
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4")
prompt = PromptTemplate.from_template("What is {topic}?")
chain = LLMChain(llm=llm, prompt=prompt)

# This will be traced in Phoenix
result = chain.run(topic="quantum computing")
```

#### LlamaIndex Integration

```python
# llamaindex_setup.py
from phoenix.otel import register
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor

# Register Phoenix
tracer_provider = register(
    project_name="llamaindex-app",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrument LlamaIndex
LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)

# Now all LlamaIndex operations are traced
from llama_index import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# This will be traced in Phoenix
response = query_engine.query("What is the main topic?")
```

#### OpenAI Direct Integration

```python
# openai_setup.py
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
import openai

# Register Phoenix
tracer_provider = register(
    project_name="openai-app",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrument OpenAI
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

# Now all OpenAI calls are traced
client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ]
)
```

### Verification & Testing

```python
# test_phoenix_setup.py
import time
from phoenix.otel import register
from opentelemetry import trace

# Setup
tracer_provider = register(
    project_name="test-project",
    endpoint="http://localhost:6006/v1/traces"
)

tracer = trace.get_tracer(__name__)

def test_basic_tracing():
    """Test basic trace creation"""
    with tracer.start_as_current_span("test-span") as span:
        span.set_attribute("test.type", "verification")
        span.set_attribute("test.timestamp", time.time())

        # Simulate work
        time.sleep(0.1)

        span.add_event("Test event occurred")

    print("✓ Basic tracing works")

def test_nested_spans():
    """Test nested span creation"""
    with tracer.start_as_current_span("parent-span") as parent:
        parent.set_attribute("span.level", "parent")

        with tracer.start_as_current_span("child-span-1") as child1:
            child1.set_attribute("span.level", "child")
            time.sleep(0.05)

        with tracer.start_as_current_span("child-span-2") as child2:
            child2.set_attribute("span.level", "child")
            time.sleep(0.05)

    print("✓ Nested spans work")

def test_error_handling():
    """Test error capture in spans"""
    try:
        with tracer.start_as_current_span("error-span") as span:
            span.set_attribute("test.will_fail", True)
            raise ValueError("Test error")
    except ValueError as e:
        print(f"✓ Error handling works: {e}")

if __name__ == "__main__":
    test_basic_tracing()
    test_nested_spans()
    test_error_handling()

    print("\n✓ All tests passed!")
    print(f"View traces at: http://localhost:6006")
```

```bash
# Run verification
python test_phoenix_setup.py

# Check Phoenix UI
open http://localhost:6006
```

### Troubleshooting Setup Issues

#### Issue 1: Phoenix Server Won't Start

```bash
# Check if port is already in use
lsof -i :6006

# Kill existing process
kill -9 <PID>

# Try alternative port
python -m phoenix.server.main serve --port 6007
```

#### Issue 2: Traces Not Appearing

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check endpoint configuration
import os
print(f"Phoenix endpoint: {os.getenv('PHOENIX_COLLECTOR_ENDPOINT')}")

# Verify exporter is sending
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
tracer_provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)
```

#### Issue 3: Network Connection Issues

```bash
# Test Phoenix server connectivity
curl http://localhost:6006/healthz

# Test OTLP endpoint
curl -X POST http://localhost:6006/v1/traces \
  -H "Content-Type: application/json" \
  -d '{"resourceSpans":[]}'

# Check firewall rules
sudo ufw status
```

---

## Core Concepts

### 1. Traces and Spans

**Trace:**
A trace represents the complete journey of a request through your LLM application, from input to output.

```python
# Trace structure example
{
    "trace_id": "7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c",
    "project_name": "rag-chatbot",
    "start_time": "2024-01-15T10:30:00.000Z",
    "end_time": "2024-01-15T10:30:05.234Z",
    "duration_ms": 5234,
    "status": "OK",
    "root_span": {
        "span_id": "1a2b3c4d5e6f7a8b",
        "name": "ChatChain.invoke"
    }
}
```

**Span:**
A span represents a single operation within a trace (e.g., LLM call, retrieval, tool use).

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

# Create a span
with tracer.start_as_current_span("document_retrieval") as span:
    # Add attributes
    span.set_attribute("retrieval.query", "What is quantum computing?")
    span.set_attribute("retrieval.top_k", 5)

    # Perform operation
    results = retrieve_documents(query)

    # Add results
    span.set_attribute("retrieval.num_results", len(results))
    span.set_attribute("retrieval.relevance_scores", [r.score for r in results])
```

**Span Types in Phoenix:**

1. **LLM Span**: Represents an LLM API call
```python
{
    "span_kind": "LLM",
    "attributes": {
        "llm.model_name": "gpt-4",
        "llm.input_messages": [...],
        "llm.output_messages": [...],
        "llm.token_count.prompt": 150,
        "llm.token_count.completion": 200,
        "llm.token_count.total": 350
    }
}
```

2. **Retriever Span**: Represents document retrieval
```python
{
    "span_kind": "RETRIEVER",
    "attributes": {
        "retrieval.documents": [...],
        "retrieval.query": "search query",
        "retrieval.top_k": 5
    }
}
```

3. **Chain Span**: Represents a sequence of operations
```python
{
    "span_kind": "CHAIN",
    "attributes": {
        "chain.type": "sequential",
        "chain.steps": ["retrieval", "llm", "post_process"]
    }
}
```

4. **Tool Span**: Represents tool/function execution
```python
{
    "span_kind": "TOOL",
    "attributes": {
        "tool.name": "calculator",
        "tool.description": "Performs calculations",
        "tool.parameters": {"operation": "multiply", "args": [5, 7]}
    }
}
```

### 2. Instrumentation

**Automatic Instrumentation:**
Phoenix provides automatic instrumentation for popular frameworks.

```python
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

# One-line setup
register(project_name="my-app")
LangChainInstrumentor().instrument()

# All LangChain operations now automatically traced
```

**Manual Instrumentation:**
For custom code or unsupported frameworks.

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def custom_rag_pipeline(query: str):
    # Create parent span
    with tracer.start_as_current_span("rag_pipeline") as pipeline_span:
        pipeline_span.set_attribute("input.query", query)

        # Retrieval step
        with tracer.start_as_current_span("retrieval") as retrieval_span:
            docs = retrieve_documents(query)
            retrieval_span.set_attribute("num_docs", len(docs))

        # LLM step
        with tracer.start_as_current_span("llm_generation") as llm_span:
            llm_span.set_attribute("llm.model", "gpt-4")
            response = generate_response(query, docs)
            llm_span.set_attribute("output.length", len(response))

        pipeline_span.set_attribute("status", "success")
        return response
```

**Span Attributes Best Practices:**

```python
# Input/Output
span.set_attribute("input.value", user_query)
span.set_attribute("output.value", response)
span.set_attribute("input.mime_type", "text/plain")

# LLM specific
span.set_attribute("llm.model_name", "gpt-4")
span.set_attribute("llm.temperature", 0.7)
span.set_attribute("llm.max_tokens", 500)
span.set_attribute("llm.token_count.prompt", 150)
span.set_attribute("llm.token_count.completion", 200)

# Retrieval specific
span.set_attribute("retrieval.query", query)
span.set_attribute("retrieval.top_k", 5)
span.set_attribute("retrieval.documents", [doc.id for doc in docs])

# Metadata
span.set_attribute("user.id", user_id)
span.set_attribute("session.id", session_id)
span.set_attribute("metadata.version", "1.0.0")
```

### 3. Evaluations

**Evaluator Types:**

Phoenix provides built-in LLM-as-judge evaluators for common metrics.

```python
from phoenix.evals import (
    HallucinationEvaluator,
    RelevanceEvaluator,
    QAEvaluator,
    ToxicityEvaluator,
    SummarizationEvaluator
)

# Hallucination Detection
hallucination_evaluator = HallucinationEvaluator(
    model_name="gpt-4"
)

# Evaluate if output is grounded in context
result = hallucination_evaluator.evaluate(
    input="What is the capital of France?",
    output="The capital of France is Paris.",
    context="France is a country in Europe. Its capital is Paris."
)
# result: {"label": "factual", "score": 1.0, "explanation": "..."}

# Relevance Evaluation
relevance_evaluator = RelevanceEvaluator(
    model_name="gpt-4"
)

result = relevance_evaluator.evaluate(
    input="What is quantum computing?",
    output="Quantum computing uses quantum mechanics...",
    context="Quantum computing is a type of computation..."
)
# result: {"label": "relevant", "score": 1.0}
```

**Running Evaluations on Traces:**

```python
import phoenix as px
import pandas as pd

# Load traces from Phoenix
client = px.Client()
traces_df = client.get_trace_dataset(
    project_name="my-app",
    start_time="2024-01-01",
    end_time="2024-01-31"
)

# Run evaluations
from phoenix.evals import run_evals

results = run_evals(
    dataframe=traces_df,
    evaluators=[
        HallucinationEvaluator(model_name="gpt-4"),
        RelevanceEvaluator(model_name="gpt-4")
    ],
    provide_explanation=True
)

# Upload results back to Phoenix
client.log_evaluations(results)
```

**Custom Evaluators:**

```python
from phoenix.evals import LLMEvaluator
from phoenix.evals.templates import ClassificationTemplate

# Define custom template
custom_template = ClassificationTemplate(
    rails=["compliant", "non_compliant"],
    template="""
    You are evaluating compliance with company policy.

    Policy: {policy}
    Response: {response}

    Determine if the response complies with the policy.
    """,
    explanation_template="Explain your reasoning:"
)

# Create evaluator
compliance_evaluator = LLMEvaluator(
    model_name="gpt-4",
    template=custom_template
)

# Use evaluator
result = compliance_evaluator.evaluate(
    policy="Always include disclaimers",
    response="Here is my answer. Disclaimer: ..."
)
```

### 4. Projects

Projects organize traces by application or environment.

```python
# Register with project name
from phoenix.otel import register

# Development project
register(project_name="my-app-dev")

# Production project
register(project_name="my-app-prod")

# Feature branch project
register(project_name="my-app-feature-xyz")
```

**Project Management via API:**

```python
import phoenix as px

client = px.Client()

# List projects
projects = client.list_projects()

# Get project details
project = client.get_project("my-app-prod")

# Delete project
client.delete_project("my-app-old")
```

### 5. Embeddings Analysis

Phoenix can analyze embeddings for drift detection and clustering.

```python
import phoenix as px
import pandas as pd

# Prepare embeddings data
embeddings_df = pd.DataFrame({
    "text": ["document 1", "document 2", ...],
    "embedding": [embedding_vector_1, embedding_vector_2, ...],
    "timestamp": [timestamp_1, timestamp_2, ...],
    "label": ["category_a", "category_b", ...]
})

# Launch Phoenix with embeddings
schema = px.Schema(
    embedding_feature_column_names=["embedding"],
    prediction_label_column_name="label"
)

px.launch_app(
    primary=px.Dataset(embeddings_df, schema=schema),
    name="Embeddings Analysis"
)
```

**Drift Detection:**

```python
# Compare two time periods
baseline_df = embeddings_df[embeddings_df["timestamp"] < "2024-01-01"]
production_df = embeddings_df[embeddings_df["timestamp"] >= "2024-01-01"]

px.launch_app(
    primary=px.Dataset(production_df, schema=schema),
    reference=px.Dataset(baseline_df, schema=schema),
    name="Drift Analysis"
)
```

### 6. OpenTelemetry Concepts

Phoenix is built on OpenTelemetry standards.

**Key OTel Concepts:**

1. **Context Propagation**: Traces maintain context across async operations
```python
from opentelemetry import context

# Context is automatically propagated
with tracer.start_as_current_span("parent"):
    async_task()  # Child spans inherit context
```

2. **Baggage**: Key-value pairs propagated across spans
```python
from opentelemetry import baggage

# Set baggage
ctx = baggage.set_baggage("user_id", "12345")

# Access in child spans
user_id = baggage.get_baggage("user_id")
```

3. **Semantic Conventions**: Standardized attribute names
```python
# Following OpenInference semantic conventions
span.set_attribute("llm.model_name", "gpt-4")  # Standard
span.set_attribute("model", "gpt-4")  # Non-standard
```

---

## Production-Ready Examples

### Example 1: Basic RAG Pipeline with Tracing

```python
# basic_rag_with_phoenix.py
"""
Basic RAG pipeline with Phoenix tracing
Demonstrates: Document retrieval, LLM generation, full observability
"""

import os
from typing import List
import openai
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace

# Setup Phoenix
register(
    project_name="basic-rag-pipeline",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrument OpenAI
OpenAIInstrumentor().instrument()

# Initialize
client = openai.OpenAI()
tracer = trace.get_tracer(__name__)

# Mock document store
DOCUMENTS = [
    "Python is a high-level programming language.",
    "Machine learning is a subset of artificial intelligence.",
    "RAG stands for Retrieval-Augmented Generation.",
    "Vector databases store embeddings for similarity search.",
    "OpenTelemetry provides observability for distributed systems."
]

def get_embedding(text: str) -> List[float]:
    """Get embedding for text"""
    with tracer.start_as_current_span("get_embedding") as span:
        span.set_attribute("input.text", text)

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        embedding = response.data[0].embedding
        span.set_attribute("embedding.dimension", len(embedding))
        return embedding

def retrieve_documents(query: str, top_k: int = 3) -> List[str]:
    """Retrieve relevant documents"""
    with tracer.start_as_current_span("retrieve_documents") as span:
        span.set_attribute("retrieval.query", query)
        span.set_attribute("retrieval.top_k", top_k)

        # Get query embedding
        query_embedding = get_embedding(query)

        # Mock similarity search (in production, use vector DB)
        # For demo, return first top_k documents
        results = DOCUMENTS[:top_k]

        span.set_attribute("retrieval.num_results", len(results))
        span.set_attribute("retrieval.documents", results)

        return results

def generate_response(query: str, context_docs: List[str]) -> str:
    """Generate response using LLM"""
    with tracer.start_as_current_span("generate_response") as span:
        span.set_attribute("llm.model_name", "gpt-3.5-turbo")

        # Build context
        context = "\n".join(f"- {doc}" for doc in context_docs)

        # Create prompt
        prompt = f"""Answer the question based on the context below.

Context:
{context}

Question: {query}

Answer:"""

        span.set_attribute("input.prompt", prompt)

        # Call LLM
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )

        answer = response.choices[0].message.content

        span.set_attribute("output.answer", answer)
        span.set_attribute("llm.token_count.prompt", response.usage.prompt_tokens)
        span.set_attribute("llm.token_count.completion", response.usage.completion_tokens)

        return answer

def rag_pipeline(query: str) -> dict:
    """Complete RAG pipeline"""
    with tracer.start_as_current_span("rag_pipeline") as span:
        span.set_attribute("pipeline.query", query)

        try:
            # Step 1: Retrieve
            context_docs = retrieve_documents(query, top_k=3)

            # Step 2: Generate
            answer = generate_response(query, context_docs)

            span.set_attribute("pipeline.status", "success")

            return {
                "query": query,
                "answer": answer,
                "context": context_docs
            }

        except Exception as e:
            span.set_attribute("pipeline.status", "error")
            span.set_attribute("pipeline.error", str(e))
            span.record_exception(e)
            raise

if __name__ == "__main__":
    # Test queries
    queries = [
        "What is RAG?",
        "Explain Python programming",
        "What is machine learning?"
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        result = rag_pipeline(query)
        print(f"Answer: {result['answer']}")
        print(f"Context used: {len(result['context'])} documents")

    print(f"\n✓ View traces at: http://localhost:6006")
```

### Example 2: LangChain Agent with Phoenix

```python
# langchain_agent_with_phoenix.py
"""
LangChain agent with tool usage and Phoenix tracing
Demonstrates: Agent reasoning, tool calls, error handling
"""

import os
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

# Setup Phoenix
register(
    project_name="langchain-agent",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrument LangChain
LangChainInstrumentor().instrument()

# Define tools
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions"""
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def word_counter(text: str) -> str:
    """Count words in text"""
    word_count = len(text.split())
    return f"The text contains {word_count} words"

def string_reverser(text: str) -> str:
    """Reverse a string"""
    return text[::-1]

# Create tools list
tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for mathematical calculations. Input should be a valid Python expression."
    ),
    Tool(
        name="WordCounter",
        func=word_counter,
        description="Counts the number of words in a text. Input should be a text string."
    ),
    Tool(
        name="StringReverser",
        func=string_reverser,
        description="Reverses a string. Input should be a text string."
    )
]

# Create agent
llm = ChatOpenAI(model="gpt-4", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools. Use them when needed."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    max_iterations=5
)

def run_agent_query(query: str) -> dict:
    """Run agent on query with full tracing"""
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print('='*60)

    try:
        result = agent_executor.invoke({"input": query})

        print(f"\nAnswer: {result['output']}")
        print(f"Steps taken: {len(result.get('intermediate_steps', []))}")

        return result

    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    # Test queries
    queries = [
        "What is 15 multiplied by 37?",
        "How many words are in this sentence: 'The quick brown fox jumps over the lazy dog'?",
        "Reverse the string 'Hello World'",
        "Calculate 25 + 17, then tell me how many words are in the result",
    ]

    for query in queries:
        run_agent_query(query)

    print(f"\n✓ View agent traces at: http://localhost:6006")
```

### Example 3: LlamaIndex RAG with Evaluations

```python
# llamaindex_rag_with_evaluations.py
"""
LlamaIndex RAG system with Phoenix tracing and evaluations
Demonstrates: Document indexing, querying, automated evaluation
"""

import os
from pathlib import Path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import phoenix as px
from phoenix.otel import register
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.evals import (
    HallucinationEvaluator,
    RelevanceEvaluator,
    run_evals
)

# Setup Phoenix
register(
    project_name="llamaindex-rag-evals",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrument LlamaIndex
LlamaIndexInstrumentor().instrument()

# Configure LlamaIndex
Settings.llm = OpenAI(model="gpt-4", temperature=0.1)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# Paths
DOCS_PATH = "./data/documents"
STORAGE_PATH = "./storage"

def create_index(docs_path: str, force_rebuild: bool = False):
    """Create or load vector index"""
    storage_path = Path(STORAGE_PATH)

    if not force_rebuild and storage_path.exists():
        print("Loading existing index...")
        storage_context = StorageContext.from_defaults(persist_dir=str(storage_path))
        index = load_index_from_storage(storage_context)
    else:
        print("Creating new index...")

        # Load documents
        documents = SimpleDirectoryReader(docs_path).load_data()
        print(f"Loaded {len(documents)} documents")

        # Create index
        index = VectorStoreIndex.from_documents(documents, show_progress=True)

        # Persist
        index.storage_context.persist(persist_dir=str(storage_path))

    return index

def query_with_evaluation(index, query: str, client: px.Client):
    """Query index and run evaluations"""
    print(f"\nQuery: {query}")

    # Create query engine
    query_engine = index.as_query_engine(
        similarity_top_k=3,
        response_mode="compact"
    )

    # Execute query (traced automatically)
    response = query_engine.query(query)

    print(f"Response: {response}")
    print(f"Source nodes: {len(response.source_nodes)}")

    # Get trace data
    traces_df = client.get_trace_dataset(
        project_name="llamaindex-rag-evals",
        limit=1  # Get latest trace
    )

    if not traces_df.empty:
        # Run evaluations
        print("\nRunning evaluations...")

        # Hallucination check
        hallucination_eval = HallucinationEvaluator(model_name="gpt-4")
        hallucination_results = run_evals(
            dataframe=traces_df,
            evaluators=[hallucination_eval],
            provide_explanation=True
        )

        # Relevance check
        relevance_eval = RelevanceEvaluator(model_name="gpt-4")
        relevance_results = run_evals(
            dataframe=traces_df,
            evaluators=[relevance_eval],
            provide_explanation=True
        )

        # Log evaluations back to Phoenix
        client.log_evaluations(hallucination_results)
        client.log_evaluations(relevance_results)

        print("✓ Evaluations complete")

    return response

def main():
    """Main execution"""
    # Create sample documents if needed
    docs_path = Path(DOCS_PATH)
    docs_path.mkdir(parents=True, exist_ok=True)

    if not list(docs_path.glob("*.txt")):
        print("Creating sample documents...")
        sample_docs = {
            "python.txt": "Python is a high-level programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991.",
            "ml.txt": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
            "rag.txt": "Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation to produce more accurate and contextual responses."
        }

        for filename, content in sample_docs.items():
            (docs_path / filename).write_text(content)

    # Create index
    index = create_index(str(docs_path))

    # Create Phoenix client
    client = px.Client()

    # Test queries
    queries = [
        "What is Python?",
        "Explain machine learning",
        "What does RAG stand for?",
        "Who created Python?"
    ]

    for query in queries:
        query_with_evaluation(index, query, client)

    print(f"\n✓ View traces and evaluations at: http://localhost:6006")

if __name__ == "__main__":
    main()
```

### Example 4: Multi-Step Agent Workflow

```python
# multi_step_agent_workflow.py
"""
Complex multi-step agent workflow with Phoenix tracing
Demonstrates: Sequential operations, error recovery, conditional logic
"""

import os
from typing import List, Dict, Any
from opentelemetry import trace
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
import openai

# Setup
register(project_name="multi-step-workflow")
OpenAIInstrumentor().instrument()

tracer = trace.get_tracer(__name__)
client = openai.OpenAI()

class ResearchAgent:
    """Agent that performs multi-step research"""

    def __init__(self):
        self.client = openai.OpenAI()

    def decompose_question(self, question: str) -> List[str]:
        """Break complex question into sub-questions"""
        with tracer.start_as_current_span("decompose_question") as span:
            span.set_attribute("input.question", question)

            prompt = f"""Break down this complex question into 3-5 simpler sub-questions:

Question: {question}

Return as a numbered list."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )

            # Parse sub-questions
            sub_questions = [
                line.strip()
                for line in response.choices[0].message.content.split('\n')
                if line.strip() and line[0].isdigit()
            ]

            span.set_attribute("output.num_subquestions", len(sub_questions))
            span.set_attribute("output.subquestions", sub_questions)

            return sub_questions

    def answer_subquestion(self, subquestion: str) -> str:
        """Answer a single sub-question"""
        with tracer.start_as_current_span("answer_subquestion") as span:
            span.set_attribute("input.subquestion", subquestion)

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Provide concise, factual answers."},
                    {"role": "user", "content": subquestion}
                ],
                temperature=0.5,
                max_tokens=150
            )

            answer = response.choices[0].message.content
            span.set_attribute("output.answer", answer)

            return answer

    def synthesize_answers(self, question: str, sub_qa: List[Dict[str, str]]) -> str:
        """Synthesize sub-answers into final answer"""
        with tracer.start_as_current_span("synthesize_answers") as span:
            span.set_attribute("input.question", question)
            span.set_attribute("input.num_subquestions", len(sub_qa))

            # Build context from sub-answers
            context = "\n\n".join([
                f"Q: {qa['question']}\nA: {qa['answer']}"
                for qa in sub_qa
            ])

            prompt = f"""Based on the following sub-questions and answers, provide a comprehensive answer to the main question.

Main Question: {question}

Sub-Questions and Answers:
{context}

Comprehensive Answer:"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )

            final_answer = response.choices[0].message.content
            span.set_attribute("output.final_answer", final_answer)

            return final_answer

    def research(self, question: str) -> Dict[str, Any]:
        """Execute complete research workflow"""
        with tracer.start_as_current_span("research_workflow") as span:
            span.set_attribute("workflow.question", question)

            try:
                # Step 1: Decompose
                print("Step 1: Decomposing question...")
                sub_questions = self.decompose_question(question)
                print(f"  Generated {len(sub_questions)} sub-questions")

                # Step 2: Answer each sub-question
                print("Step 2: Answering sub-questions...")
                sub_qa = []
                for i, subq in enumerate(sub_questions, 1):
                    print(f"  Answering {i}/{len(sub_questions)}")
                    answer = self.answer_subquestion(subq)
                    sub_qa.append({"question": subq, "answer": answer})

                # Step 3: Synthesize
                print("Step 3: Synthesizing final answer...")
                final_answer = self.synthesize_answers(question, sub_qa)

                span.set_attribute("workflow.status", "success")

                return {
                    "question": question,
                    "sub_questions": sub_questions,
                    "sub_answers": sub_qa,
                    "final_answer": final_answer
                }

            except Exception as e:
                span.set_attribute("workflow.status", "error")
                span.record_exception(e)
                raise

def main():
    agent = ResearchAgent()

    questions = [
        "How does climate change affect global food security?",
        "What are the key differences between quantum and classical computing?",
    ]

    for question in questions:
        print(f"\n{'='*70}")
        print(f"QUESTION: {question}")
        print('='*70)

        result = agent.research(question)

        print("\n--- Sub-Questions ---")
        for i, subq in enumerate(result['sub_questions'], 1):
            print(f"{i}. {subq}")

        print("\n--- Final Answer ---")
        print(result['final_answer'])

    print(f"\n✓ View workflow traces at: http://localhost:6006")

if __name__ == "__main__":
    main()
```

### Example 5: Streaming Responses with Tracing

```python
# streaming_with_phoenix.py
"""
Streaming LLM responses with Phoenix tracing
Demonstrates: Token-by-token streaming, incremental updates
"""

import os
from typing import Iterator
from opentelemetry import trace
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
import openai

# Setup
register(project_name="streaming-example")
OpenAIInstrumentor().instrument()

tracer = trace.get_tracer(__name__)
client = openai.OpenAI()

def stream_response(prompt: str, model: str = "gpt-4") -> Iterator[str]:
    """Stream LLM response token by token"""
    with tracer.start_as_current_span("stream_response") as span:
        span.set_attribute("llm.model_name", model)
        span.set_attribute("input.prompt", prompt)
        span.set_attribute("llm.streaming", True)

        collected_chunks = []
        collected_messages = []

        # Create streaming request
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            stream=True
        )

        # Process stream
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                chunk_text = chunk.choices[0].delta.content
                collected_chunks.append(chunk_text)
                collected_messages.append(chunk_text)
                yield chunk_text

        # Log complete response
        full_response = ''.join(collected_chunks)
        span.set_attribute("output.response", full_response)
        span.set_attribute("output.num_chunks", len(collected_chunks))
        span.set_attribute("output.length", len(full_response))

def chat_with_streaming(user_message: str):
    """Chat with streaming response"""
    print(f"\nUser: {user_message}")
    print("Assistant: ", end="", flush=True)

    full_response = ""
    for chunk in stream_response(user_message):
        print(chunk, end="", flush=True)
        full_response += chunk

    print("\n")
    return full_response

def main():
    prompts = [
        "Explain quantum computing in simple terms.",
        "Write a haiku about artificial intelligence.",
        "What are the benefits of exercise?",
    ]

    for prompt in prompts:
        chat_with_streaming(prompt)

    print(f"✓ View streaming traces at: http://localhost:6006")

if __name__ == "__main__":
    main()
```

### Example 6: Batch Processing with Phoenix

```python
# batch_processing_with_phoenix.py
"""
Batch processing multiple requests with Phoenix tracing
Demonstrates: Parallel processing, aggregated metrics, error handling
"""

import os
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from opentelemetry import trace
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
import openai
import time

# Setup
register(project_name="batch-processing")
OpenAIInstrumentor().instrument()

tracer = trace.get_tracer(__name__)
client = openai.OpenAI()

def process_single_item(item: Dict[str, str], item_id: int) -> Dict:
    """Process a single item"""
    with tracer.start_as_current_span(f"process_item_{item_id}") as span:
        span.set_attribute("item.id", item_id)
        span.set_attribute("item.type", item['type'])
        span.set_attribute("input.text", item['text'])

        start_time = time.time()

        try:
            # Process based on type
            if item['type'] == 'summarize':
                prompt = f"Summarize in one sentence: {item['text']}"
            elif item['type'] == 'sentiment':
                prompt = f"What is the sentiment (positive/negative/neutral): {item['text']}"
            elif item['type'] == 'classify':
                prompt = f"Classify this text into a category: {item['text']}"
            else:
                raise ValueError(f"Unknown type: {item['type']}")

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=100
            )

            result = response.choices[0].message.content
            duration = time.time() - start_time

            span.set_attribute("output.result", result)
            span.set_attribute("processing.duration_ms", duration * 1000)
            span.set_attribute("processing.status", "success")

            return {
                "item_id": item_id,
                "input": item['text'],
                "type": item['type'],
                "output": result,
                "duration": duration,
                "status": "success"
            }

        except Exception as e:
            duration = time.time() - start_time
            span.set_attribute("processing.status", "error")
            span.set_attribute("processing.error", str(e))
            span.record_exception(e)

            return {
                "item_id": item_id,
                "input": item['text'],
                "type": item['type'],
                "output": None,
                "duration": duration,
                "status": "error",
                "error": str(e)
            }

def batch_process(items: List[Dict[str, str]], max_workers: int = 5) -> List[Dict]:
    """Process batch of items in parallel"""
    with tracer.start_as_current_span("batch_process") as span:
        span.set_attribute("batch.size", len(items))
        span.set_attribute("batch.max_workers", max_workers)

        start_time = time.time()
        results = []

        # Process in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_item = {
                executor.submit(process_single_item, item, i): i
                for i, item in enumerate(items)
            }

            # Collect results as they complete
            for future in as_completed(future_to_item):
                item_id = future_to_item[future]
                try:
                    result = future.result()
                    results.append(result)
                    print(f"✓ Processed item {item_id + 1}/{len(items)}")
                except Exception as e:
                    print(f"✗ Failed item {item_id + 1}/{len(items)}: {e}")

        # Sort by item_id
        results.sort(key=lambda x: x['item_id'])

        # Calculate metrics
        total_duration = time.time() - start_time
        successful = sum(1 for r in results if r['status'] == 'success')
        failed = len(results) - successful
        avg_duration = sum(r['duration'] for r in results) / len(results)

        span.set_attribute("batch.total_duration_s", total_duration)
        span.set_attribute("batch.successful", successful)
        span.set_attribute("batch.failed", failed)
        span.set_attribute("batch.avg_item_duration_s", avg_duration)

        return results

def main():
    # Sample batch items
    items = [
        {
            "type": "summarize",
            "text": "Artificial intelligence is transforming industries by automating tasks, improving decision-making, and enabling new capabilities that were previously impossible."
        },
        {
            "type": "sentiment",
            "text": "I absolutely loved this product! It exceeded all my expectations and the customer service was fantastic."
        },
        {
            "type": "classify",
            "text": "The new MacBook Pro features an M3 chip, 16GB RAM, and a stunning Retina display."
        },
        {
            "type": "summarize",
            "text": "Climate change is causing global temperatures to rise, leading to more extreme weather events, rising sea levels, and threats to biodiversity worldwide."
        },
        {
            "type": "sentiment",
            "text": "This restaurant was disappointing. The food was cold and the service was slow."
        },
        {
            "type": "classify",
            "text": "The Federal Reserve announced an interest rate hike of 0.25% to combat inflation."
        },
    ]

    print(f"Processing batch of {len(items)} items...\n")

    results = batch_process(items, max_workers=3)

    # Display results
    print("\n" + "="*70)
    print("BATCH RESULTS")
    print("="*70)

    for result in results:
        print(f"\nItem {result['item_id'] + 1}:")
        print(f"  Type: {result['type']}")
        print(f"  Input: {result['input'][:50]}...")
        if result['status'] == 'success':
            print(f"  Output: {result['output']}")
            print(f"  Duration: {result['duration']:.2f}s")
        else:
            print(f"  Error: {result['error']}")

    # Summary
    successful = sum(1 for r in results if r['status'] == 'success')
    print(f"\n{'='*70}")
    print(f"Summary: {successful}/{len(results)} successful")
    print(f"✓ View batch traces at: http://localhost:6006")

if __name__ == "__main__":
    main()
```

### Example 7: Custom Evaluation Pipeline

```python
# custom_evaluation_pipeline.py
"""
Custom evaluation pipeline with Phoenix
Demonstrates: Custom evaluators, evaluation workflows, metric aggregation
"""

import os
from typing import List, Dict, Any
import pandas as pd
import phoenix as px
from phoenix.evals import (
    LLMEvaluator,
    run_evals,
    HallucinationEvaluator,
    RelevanceEvaluator
)
from phoenix.evals.templates import ClassificationTemplate
from opentelemetry import trace
from phoenix.otel import register

# Setup
register(project_name="custom-evaluations")
tracer = trace.get_tracer(__name__)

# Custom evaluator templates
FACTUALITY_TEMPLATE = ClassificationTemplate(
    rails=["factual", "partially_factual", "non_factual"],
    template="""
    Evaluate the factual accuracy of the assistant's response.

    Context: {context}
    Response: {response}

    Determine if the response is:
    - factual: All claims are supported by the context
    - partially_factual: Some claims are supported
    - non_factual: Claims contradict or are unsupported by context
    """,
    explanation_template="Explain which specific claims are factual or non-factual:"
)

COMPLETENESS_TEMPLATE = ClassificationTemplate(
    rails=["complete", "partial", "incomplete"],
    template="""
    Evaluate if the response completely addresses the question.

    Question: {question}
    Response: {response}

    Determine if the response is:
    - complete: Fully addresses all aspects of the question
    - partial: Addresses some but not all aspects
    - incomplete: Fails to adequately address the question
    """,
    explanation_template="Explain what aspects are missing or incomplete:"
)

TONE_TEMPLATE = ClassificationTemplate(
    rails=["professional", "casual", "inappropriate"],
    template="""
    Evaluate the tone and professionalism of the response.

    Response: {response}

    Classify the tone as:
    - professional: Appropriate business/technical communication
    - casual: Friendly but may lack professionalism
    - inappropriate: Unprofessional or problematic language
    """,
    explanation_template="Explain the tone assessment:"
)

class EvaluationPipeline:
    """Custom evaluation pipeline"""

    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.evaluators = self._setup_evaluators()

    def _setup_evaluators(self) -> Dict[str, LLMEvaluator]:
        """Setup all evaluators"""
        return {
            "hallucination": HallucinationEvaluator(model_name=self.model_name),
            "relevance": RelevanceEvaluator(model_name=self.model_name),
            "factuality": LLMEvaluator(
                model_name=self.model_name,
                template=FACTUALITY_TEMPLATE
            ),
            "completeness": LLMEvaluator(
                model_name=self.model_name,
                template=COMPLETENESS_TEMPLATE
            ),
            "tone": LLMEvaluator(
                model_name=self.model_name,
                template=TONE_TEMPLATE
            )
        }

    def evaluate_response(self,
                         question: str,
                         response: str,
                         context: str) -> Dict[str, Any]:
        """Evaluate a single response"""
        with tracer.start_as_current_span("evaluate_response") as span:
            span.set_attribute("evaluation.question", question)

            results = {}

            # Run hallucination check
            hallucination_result = self.evaluators["hallucination"].evaluate(
                input=question,
                output=response,
                context=context
            )
            results["hallucination"] = hallucination_result

            # Run relevance check
            relevance_result = self.evaluators["relevance"].evaluate(
                input=question,
                output=response,
                context=context
            )
            results["relevance"] = relevance_result

            # Run factuality check
            factuality_result = self.evaluators["factuality"].evaluate(
                question=question,
                response=response,
                context=context
            )
            results["factuality"] = factuality_result

            # Run completeness check
            completeness_result = self.evaluators["completeness"].evaluate(
                question=question,
                response=response
            )
            results["completeness"] = completeness_result

            # Run tone check
            tone_result = self.evaluators["tone"].evaluate(
                response=response
            )
            results["tone"] = tone_result

            # Log metrics
            for eval_name, eval_result in results.items():
                span.set_attribute(f"evaluation.{eval_name}.label", eval_result.get("label"))
                span.set_attribute(f"evaluation.{eval_name}.score", eval_result.get("score"))

            return results

    def evaluate_batch(self,
                      test_cases: List[Dict[str, str]]) -> pd.DataFrame:
        """Evaluate batch of test cases"""
        with tracer.start_as_current_span("evaluate_batch") as span:
            span.set_attribute("batch.size", len(test_cases))

            all_results = []

            for i, test_case in enumerate(test_cases):
                print(f"Evaluating {i+1}/{len(test_cases)}...")

                results = self.evaluate_response(
                    question=test_case["question"],
                    response=test_case["response"],
                    context=test_case["context"]
                )

                # Flatten results
                flat_result = {
                    "question": test_case["question"],
                    "response": test_case["response"],
                    "context": test_case["context"]
                }

                for eval_name, eval_result in results.items():
                    flat_result[f"{eval_name}_label"] = eval_result.get("label")
                    flat_result[f"{eval_name}_score"] = eval_result.get("score")
                    flat_result[f"{eval_name}_explanation"] = eval_result.get("explanation")

                all_results.append(flat_result)

            df = pd.DataFrame(all_results)
            return df

    def generate_report(self, results_df: pd.DataFrame) -> str:
        """Generate evaluation report"""
        report = []
        report.append("=" * 80)
        report.append("EVALUATION REPORT")
        report.append("=" * 80)
        report.append(f"\nTotal test cases: {len(results_df)}")

        # Metrics for each evaluator
        evaluator_names = ["hallucination", "relevance", "factuality", "completeness", "tone"]

        for eval_name in evaluator_names:
            label_col = f"{eval_name}_label"
            if label_col in results_df.columns:
                report.append(f"\n{eval_name.upper()}:")
                label_counts = results_df[label_col].value_counts()
                for label, count in label_counts.items():
                    percentage = (count / len(results_df)) * 100
                    report.append(f"  {label}: {count} ({percentage:.1f}%)")

        # Pass rate (hallucination=factual AND relevance=relevant)
        if "hallucination_label" in results_df.columns and "relevance_label" in results_df.columns:
            passed = (
                (results_df["hallucination_label"] == "factual") &
                (results_df["relevance_label"] == "relevant")
            ).sum()
            pass_rate = (passed / len(results_df)) * 100
            report.append(f"\nOverall Pass Rate: {passed}/{len(results_df)} ({pass_rate:.1f}%)")

        return "\n".join(report)

def main():
    # Sample test cases
    test_cases = [
        {
            "question": "What is the capital of France?",
            "response": "The capital of France is Paris, known for the Eiffel Tower and the Louvre Museum.",
            "context": "France is a country in Western Europe. Its capital is Paris, home to iconic landmarks like the Eiffel Tower."
        },
        {
            "question": "What is Python used for?",
            "response": "Python is used for web development, data science, artificial intelligence, and automation.",
            "context": "Python is a versatile programming language used in web development, data analysis, machine learning, and scripting."
        },
        {
            "question": "Who invented the telephone?",
            "response": "Thomas Edison invented the telephone in 1876.",
            "context": "Alexander Graham Bell is credited with inventing the telephone in 1876. Thomas Edison invented the phonograph."
        },
        {
            "question": "What causes climate change?",
            "response": "It's getting warmer.",
            "context": "Climate change is primarily caused by greenhouse gas emissions from human activities like burning fossil fuels, deforestation, and industrial processes."
        }
    ]

    # Run evaluation pipeline
    pipeline = EvaluationPipeline(model_name="gpt-4")

    print("Running evaluation pipeline...\n")
    results_df = pipeline.evaluate_batch(test_cases)

    # Generate report
    report = pipeline.generate_report(results_df)
    print("\n" + report)

    # Save results
    results_df.to_csv("evaluation_results.csv", index=False)
    print("\n✓ Results saved to evaluation_results.csv")

    # Connect to Phoenix to log results
    try:
        client = px.Client()
        client.log_evaluations(results_df)
        print("✓ Results logged to Phoenix")
    except Exception as e:
        print(f"Note: Could not log to Phoenix: {e}")

    print(f"✓ View evaluations at: http://localhost:6006")

if __name__ == "__main__":
    main()
```

### Example 8: Production Monitoring Dashboard

```python
# production_monitoring.py
"""
Production monitoring with Phoenix
Demonstrates: Real-time metrics, alerting, performance tracking
"""

import os
from typing import Dict, List, Any
from datetime import datetime, timedelta
import pandas as pd
import phoenix as px
from opentelemetry import trace
from phoenix.otel import register

# Setup
register(project_name="production-monitoring")
tracer = trace.get_tracer(__name__)

class ProductionMonitor:
    """Monitor production LLM application"""

    def __init__(self, project_name: str, phoenix_endpoint: str = "http://localhost:6006"):
        self.project_name = project_name
        self.client = px.Client(endpoint=phoenix_endpoint)

    def get_metrics(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get metrics for time window"""
        with tracer.start_as_current_span("get_metrics") as span:
            span.set_attribute("time_window_hours", time_window_hours)

            # Calculate time range
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=time_window_hours)

            # Fetch traces
            traces_df = self.client.get_trace_dataset(
                project_name=self.project_name,
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat()
            )

            if traces_df.empty:
                return {"error": "No data available"}

            # Calculate metrics
            metrics = {
                "total_requests": len(traces_df),
                "success_rate": self._calculate_success_rate(traces_df),
                "avg_latency_ms": self._calculate_avg_latency(traces_df),
                "p95_latency_ms": self._calculate_p95_latency(traces_df),
                "p99_latency_ms": self._calculate_p99_latency(traces_df),
                "total_tokens": self._calculate_total_tokens(traces_df),
                "avg_tokens_per_request": self._calculate_avg_tokens(traces_df),
                "error_rate": self._calculate_error_rate(traces_df),
                "requests_per_hour": len(traces_df) / time_window_hours,
            }

            # Log metrics
            for key, value in metrics.items():
                span.set_attribute(f"metric.{key}", value)

            return metrics

    def _calculate_success_rate(self, df: pd.DataFrame) -> float:
        """Calculate success rate"""
        if "status" in df.columns:
            success = (df["status"] == "OK").sum()
            return (success / len(df)) * 100
        return 0.0

    def _calculate_avg_latency(self, df: pd.DataFrame) -> float:
        """Calculate average latency"""
        if "latency_ms" in df.columns:
            return df["latency_ms"].mean()
        return 0.0

    def _calculate_p95_latency(self, df: pd.DataFrame) -> float:
        """Calculate P95 latency"""
        if "latency_ms" in df.columns:
            return df["latency_ms"].quantile(0.95)
        return 0.0

    def _calculate_p99_latency(self, df: pd.DataFrame) -> float:
        """Calculate P99 latency"""
        if "latency_ms" in df.columns:
            return df["latency_ms"].quantile(0.99)
        return 0.0

    def _calculate_total_tokens(self, df: pd.DataFrame) -> int:
        """Calculate total tokens used"""
        if "llm.token_count.total" in df.columns:
            return df["llm.token_count.total"].sum()
        return 0

    def _calculate_avg_tokens(self, df: pd.DataFrame) -> float:
        """Calculate average tokens per request"""
        if "llm.token_count.total" in df.columns:
            return df["llm.token_count.total"].mean()
        return 0.0

    def _calculate_error_rate(self, df: pd.DataFrame) -> float:
        """Calculate error rate"""
        if "status" in df.columns:
            errors = (df["status"] != "OK").sum()
            return (errors / len(df)) * 100
        return 0.0

    def check_alerts(self, metrics: Dict[str, Any]) -> List[str]:
        """Check for alert conditions"""
        alerts = []

        # Alert thresholds
        thresholds = {
            "success_rate_min": 95.0,
            "error_rate_max": 5.0,
            "p95_latency_max_ms": 5000,
            "p99_latency_max_ms": 10000,
        }

        # Check success rate
        if metrics.get("success_rate", 100) < thresholds["success_rate_min"]:
            alerts.append(
                f"⚠️  Low success rate: {metrics['success_rate']:.1f}% "
                f"(threshold: {thresholds['success_rate_min']}%)"
            )

        # Check error rate
        if metrics.get("error_rate", 0) > thresholds["error_rate_max"]:
            alerts.append(
                f"⚠️  High error rate: {metrics['error_rate']:.1f}% "
                f"(threshold: {thresholds['error_rate_max']}%)"
            )

        # Check P95 latency
        if metrics.get("p95_latency_ms", 0) > thresholds["p95_latency_max_ms"]:
            alerts.append(
                f"⚠️  High P95 latency: {metrics['p95_latency_ms']:.0f}ms "
                f"(threshold: {thresholds['p95_latency_max_ms']}ms)"
            )

        # Check P99 latency
        if metrics.get("p99_latency_ms", 0) > thresholds["p99_latency_max_ms"]:
            alerts.append(
                f"⚠️  High P99 latency: {metrics['p99_latency_ms']:.0f}ms "
                f"(threshold: {thresholds['p99_latency_max_ms']}ms)"
            )

        return alerts

    def generate_dashboard(self, metrics: Dict[str, Any], alerts: List[str]) -> str:
        """Generate dashboard display"""
        dashboard = []
        dashboard.append("=" * 80)
        dashboard.append(f"PRODUCTION MONITORING DASHBOARD - {self.project_name}")
        dashboard.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        dashboard.append("=" * 80)

        # Alerts section
        if alerts:
            dashboard.append("\n🚨 ALERTS:")
            for alert in alerts:
                dashboard.append(f"  {alert}")
        else:
            dashboard.append("\n✅ No alerts")

        # Metrics section
        dashboard.append("\n📊 METRICS:")
        dashboard.append(f"  Total Requests: {metrics.get('total_requests', 0):,}")
        dashboard.append(f"  Success Rate: {metrics.get('success_rate', 0):.2f}%")
        dashboard.append(f"  Error Rate: {metrics.get('error_rate', 0):.2f}%")
        dashboard.append(f"  Requests/Hour: {metrics.get('requests_per_hour', 0):.1f}")

        dashboard.append("\n⏱️  LATENCY:")
        dashboard.append(f"  Average: {metrics.get('avg_latency_ms', 0):.0f}ms")
        dashboard.append(f"  P95: {metrics.get('p95_latency_ms', 0):.0f}ms")
        dashboard.append(f"  P99: {metrics.get('p99_latency_ms', 0):.0f}ms")

        dashboard.append("\n🔢 TOKENS:")
        dashboard.append(f"  Total: {metrics.get('total_tokens', 0):,}")
        dashboard.append(f"  Avg per Request: {metrics.get('avg_tokens_per_request', 0):.0f}")

        dashboard.append("\n" + "=" * 80)

        return "\n".join(dashboard)

    def run_monitoring_cycle(self, time_window_hours: int = 24):
        """Run one monitoring cycle"""
        print("Running monitoring cycle...")

        # Get metrics
        metrics = self.get_metrics(time_window_hours)

        if "error" in metrics:
            print(f"Error: {metrics['error']}")
            return

        # Check alerts
        alerts = self.check_alerts(metrics)

        # Display dashboard
        dashboard = self.generate_dashboard(metrics, alerts)
        print(dashboard)

        return metrics, alerts

def main():
    # Initialize monitor
    monitor = ProductionMonitor(
        project_name="production-app",  # Change to your project name
        phoenix_endpoint="http://localhost:6006"
    )

    # Run monitoring
    monitor.run_monitoring_cycle(time_window_hours=24)

    print(f"\n✓ View detailed traces at: http://localhost:6006")

if __name__ == "__main__":
    main()
```

---

## Advanced Usage

### Custom Span Processors

Create custom span processors for specialized handling:

```python
from opentelemetry.sdk.trace import SpanProcessor, ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter
from typing import Optional
import logging

class FilteringSpanProcessor(SpanProcessor):
    """Custom processor that filters spans"""

    def __init__(self, exporter: SpanExporter, filter_func):
        self.exporter = exporter
        self.filter_func = filter_func
        self.logger = logging.getLogger(__name__)

    def on_start(self, span: ReadableSpan, parent_context):
        """Called when span starts"""
        pass

    def on_end(self, span: ReadableSpan):
        """Called when span ends"""
        # Apply filter
        if self.filter_func(span):
            self.exporter.export([span])
        else:
            self.logger.debug(f"Filtered out span: {span.name}")

    def shutdown(self):
        """Shutdown processor"""
        self.exporter.shutdown()

    def force_flush(self, timeout_millis: int = 30000):
        """Force flush"""
        self.exporter.force_flush(timeout_millis)

# Usage
def should_export_span(span: ReadableSpan) -> bool:
    """Filter function - only export LLM spans"""
    return span.attributes.get("llm.model_name") is not None

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

tracer_provider = TracerProvider()
exporter = OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces")
processor = FilteringSpanProcessor(exporter, should_export_span)
tracer_provider.add_span_processor(processor)
```

### Custom Instrumentation for Any Framework

```python
from functools import wraps
from opentelemetry import trace
from typing import Callable, Any

tracer = trace.get_tracer(__name__)

def trace_function(
    span_name: Optional[str] = None,
    attributes: Optional[Dict[str, Any]] = None
):
    """Decorator to trace any function"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = span_name or func.__name__

            with tracer.start_as_current_span(name) as span:
                # Add default attributes
                span.set_attribute("function.name", func.__name__)
                span.set_attribute("function.module", func.__module__)

                # Add custom attributes
                if attributes:
                    for key, value in attributes.items():
                        span.set_attribute(key, value)

                # Add arguments as attributes
                if args:
                    span.set_attribute("function.args", str(args))
                if kwargs:
                    span.set_attribute("function.kwargs", str(kwargs))

                try:
                    result = func(*args, **kwargs)
                    span.set_attribute("function.status", "success")
                    return result
                except Exception as e:
                    span.set_attribute("function.status", "error")
                    span.record_exception(e)
                    raise

        return wrapper
    return decorator

# Usage
@trace_function(attributes={"custom.key": "value"})
def my_custom_function(x, y):
    return x + y

result = my_custom_function(5, 7)  # Automatically traced
```

### Distributed Tracing Across Services

```python
# service_a.py - Parent service
from opentelemetry import trace
from opentelemetry.propagate import inject
from phoenix.otel import register
import requests

register(project_name="service-a")
tracer = trace.get_tracer(__name__)

def call_service_b(data):
    """Call service B with trace context"""
    with tracer.start_as_current_span("call_service_b") as span:
        span.set_attribute("target.service", "service-b")

        # Prepare headers with trace context
        headers = {}
        inject(headers)  # Injects W3C Trace Context

        # Call service B
        response = requests.post(
            "http://service-b:8000/process",
            json=data,
            headers=headers
        )

        span.set_attribute("response.status_code", response.status_code)
        return response.json()

# service_b.py - Child service
from opentelemetry import trace
from opentelemetry.propagate import extract
from phoenix.otel import register
from flask import Flask, request

register(project_name="service-b")
tracer = trace.get_tracer(__name__)
app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process():
    """Process request with parent trace context"""
    # Extract trace context from headers
    context = extract(request.headers)

    # Create span with parent context
    with tracer.start_as_current_span("process_request", context=context) as span:
        data = request.json
        span.set_attribute("request.data", str(data))

        # Process...
        result = {"status": "processed"}

        return result
```

### Dynamic Sampling

```python
from opentelemetry.sdk.trace.sampling import (
    Sampler,
    SamplingResult,
    Decision
)
from opentelemetry.trace import SpanKind
import random

class CustomSampler(Sampler):
    """Custom sampler with dynamic rules"""

    def __init__(self, default_rate: float = 0.1):
        self.default_rate = default_rate

    def should_sample(self, parent_context, trace_id, name, kind, attributes, links, trace_state):
        """Determine if span should be sampled"""

        # Always sample errors
        if attributes and attributes.get("error") is True:
            return SamplingResult(
                decision=Decision.RECORD_AND_SAMPLE,
                attributes=attributes
            )

        # Always sample slow requests
        if attributes and attributes.get("latency_ms", 0) > 1000:
            return SamplingResult(
                decision=Decision.RECORD_AND_SAMPLE,
                attributes=attributes
            )

        # Sample LLM spans at higher rate
        if kind == SpanKind.CLIENT and attributes.get("llm.model_name"):
            sample_rate = 0.5  # 50%
        else:
            sample_rate = self.default_rate

        # Random sampling
        if random.random() < sample_rate:
            return SamplingResult(
                decision=Decision.RECORD_AND_SAMPLE,
                attributes=attributes
            )

        return SamplingResult(
            decision=Decision.DROP,
            attributes=attributes
        )

    def get_description(self):
        return "CustomSampler"

# Use custom sampler
from opentelemetry.sdk.trace import TracerProvider

tracer_provider = TracerProvider(sampler=CustomSampler(default_rate=0.1))
```

---

## Best Practices

### 1. Span Design

**Do's:**
- Keep span names descriptive but concise
- Use hierarchical naming (e.g., "rag.retrieval", "rag.generation")
- Include relevant attributes for debugging
- Set status codes appropriately
- Record exceptions when they occur

**Don'ts:**
- Don't include PII in span names or attributes
- Don't create too many tiny spans (performance impact)
- Don't forget to end spans (use context managers)
- Don't log sensitive data

```python
# Good span design
with tracer.start_as_current_span("document_retrieval") as span:
    span.set_attribute("retrieval.query_id", query_id)
    span.set_attribute("retrieval.top_k", 5)
    span.set_attribute("retrieval.vector_db", "pinecone")

    try:
        docs = retrieve(query)
        span.set_attribute("retrieval.num_results", len(docs))
        span.set_status(StatusCode.OK)
    except Exception as e:
        span.record_exception(e)
        span.set_status(StatusCode.ERROR, str(e))
        raise
```

### 2. Attribute Naming Conventions

Follow OpenInference semantic conventions:

```python
# LLM attributes
span.set_attribute("llm.model_name", "gpt-4")
span.set_attribute("llm.invocation_parameters", json.dumps(params))
span.set_attribute("llm.token_count.prompt", 150)
span.set_attribute("llm.token_count.completion", 200)
span.set_attribute("llm.token_count.total", 350)

# Input/Output
span.set_attribute("input.value", user_input)
span.set_attribute("input.mime_type", "text/plain")
span.set_attribute("output.value", response)
span.set_attribute("output.mime_type", "text/plain")

# Retrieval
span.set_attribute("retrieval.documents", json.dumps(doc_ids))
span.set_attribute("retrieval.query", query_text)

# Metadata
span.set_attribute("metadata.user_id", user_id)
span.set_attribute("metadata.session_id", session_id)
```

### 3. Performance Optimization

```python
# Use batch span processor for better performance
from opentelemetry.sdk.trace.export import BatchSpanProcessor

processor = BatchSpanProcessor(
    exporter,
    max_queue_size=2048,
    max_export_batch_size=512,
    export_timeout_millis=30000,
)

# Use sampling for high-volume applications
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased Sampler

sampler = TraceIdRatioBasedSampler(rate=0.1)  # Sample 10%
tracer_provider = TracerProvider(sampler=sampler)

# Minimize attribute serialization overhead
# Bad: serializing large objects
span.set_attribute("large_object", json.dumps(large_dict))

# Good: only log essential info
span.set_attribute("object.size", len(large_dict))
span.set_attribute("object.type", type(large_dict).__name__)
```

### 4. Error Handling

```python
from opentelemetry.trace import StatusCode

def traced_operation():
    with tracer.start_as_current_span("operation") as span:
        try:
            result = risky_operation()
            span.set_status(StatusCode.OK)
            return result
        except ValueError as e:
            # Log exception to span
            span.record_exception(e)
            span.set_status(StatusCode.ERROR, "Invalid value")
            # Re-raise or handle
            raise
        except Exception as e:
            span.record_exception(e)
            span.set_status(StatusCode.ERROR, "Unexpected error")
            raise
```

### 5. Security & Privacy

```python
# Sanitize PII before logging
import re

def sanitize_pii(text: str) -> str:
    """Remove PII from text"""
    # Remove emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    # Remove phone numbers
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    # Remove credit cards
    text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CREDIT_CARD]', text)
    return text

with tracer.start_as_current_span("user_query") as span:
    # Sanitize before logging
    sanitized_input = sanitize_pii(user_input)
    span.set_attribute("input.value", sanitized_input)
```

### 6. Testing with Phoenix

```python
# test_with_phoenix.py
import pytest
from phoenix.otel import register
from opentelemetry import trace

@pytest.fixture(scope="session")
def phoenix_tracer():
    """Setup Phoenix for tests"""
    tracer_provider = register(
        project_name="test-project",
        endpoint="http://localhost:6006/v1/traces"
    )
    return trace.get_tracer(__name__)

def test_rag_pipeline(phoenix_tracer):
    """Test RAG pipeline with tracing"""
    with phoenix_tracer.start_as_current_span("test_rag") as span:
        result = rag_pipeline("test query")

        # Assertions
        assert result is not None
        assert len(result['answer']) > 0

        # Add test metadata
        span.set_attribute("test.name", "test_rag_pipeline")
        span.set_attribute("test.passed", True)
```

---

## Integration Guide

### Integration with Popular Frameworks

#### FastAPI Integration

```python
# fastapi_phoenix_app.py
from fastapi import FastAPI, Request
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import openai

# Setup Phoenix
register(project_name="fastapi-app")
OpenAIInstrumentor().instrument()

app = FastAPI()

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

tracer = trace.get_tracer(__name__)
client = openai.OpenAI()

@app.post("/chat")
async def chat(request: Request):
    """Chat endpoint with tracing"""
    body = await request.json()
    user_message = body.get("message")

    with tracer.start_as_current_span("chat_endpoint") as span:
        span.set_attribute("request.message", user_message)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        answer = response.choices[0].message.content
        span.set_attribute("response.answer", answer)

        return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Celery Integration

```python
# celery_phoenix_tasks.py
from celery import Celery
from phoenix.otel import register
from opentelemetry import trace
from opentelemetry.instrumentation.celery import CeleryInstrumentor

# Setup
register(project_name="celery-tasks")
CeleryInstrumentor().instrument()

app = Celery('tasks', broker='redis://localhost:6379')
tracer = trace.get_tracer(__name__)

@app.task
def process_document(doc_id: str):
    """Process document with tracing"""
    with tracer.start_as_current_span("process_document") as span:
        span.set_attribute("document.id", doc_id)

        # Processing logic...
        result = {"status": "processed", "doc_id": doc_id}

        span.set_attribute("result.status", "success")
        return result
```

#### Streamlit Integration

```python
# streamlit_phoenix_app.py
import streamlit as st
from phoenix.otel import register
from opentelemetry import trace
import openai

# Setup Phoenix (only once)
if 'phoenix_initialized' not in st.session_state:
    register(project_name="streamlit-app")
    st.session_state.phoenix_initialized = True

tracer = trace.get_tracer(__name__)
client = openai.OpenAI()

st.title("Chat with Phoenix Tracing")

user_input = st.text_input("Your message:")

if st.button("Send"):
    with tracer.start_as_current_span("streamlit_chat") as span:
        span.set_attribute("user.input", user_input)

        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )

            answer = response.choices[0].message.content
            st.write(answer)

            span.set_attribute("assistant.response", answer)

st.markdown("[View traces in Phoenix](http://localhost:6006)")
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Traces Not Appearing in Phoenix UI

**Symptoms:**
- Application runs without errors
- No traces visible in Phoenix UI

**Solutions:**

```python
# 1. Verify Phoenix server is running
# Check: http://localhost:6006

# 2. Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# 3. Check endpoint configuration
import os
print(os.getenv("PHOENIX_COLLECTOR_ENDPOINT"))

# 4. Test with console exporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
tracer_provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# 5. Verify instrumentation is active
from opentelemetry import trace
print(trace.get_tracer_provider())
```

#### Issue 2: High Memory Usage

**Symptoms:**
- Application memory grows over time
- OutOfMemory errors

**Solutions:**

```python
# 1. Use batch processor with limits
from opentelemetry.sdk.trace.export import BatchSpanProcessor

processor = BatchSpanProcessor(
    exporter,
    max_queue_size=2048,  # Limit queue size
    max_export_batch_size=512,
    schedule_delay_millis=5000,  # Export every 5s
)

# 2. Implement sampling
from opentelemetry.sdk.trace.sampling import TraceIdRatioBasedSampler

sampler = TraceIdRatioBasedSampler(rate=0.1)  # Sample 10%

# 3. Limit attribute sizes
def truncate_attribute(value: str, max_length: int = 1000) -> str:
    if len(value) > max_length:
        return value[:max_length] + "... (truncated)"
    return value

span.set_attribute("large_text", truncate_attribute(large_text))
```

#### Issue 3: Performance Impact

**Symptoms:**
- Application slowdown after adding tracing
- Increased latency

**Solutions:**

```python
# 1. Use async/background export
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Batch processor exports asynchronously
processor = BatchSpanProcessor(exporter)

# 2. Reduce span creation
# Only trace high-level operations, not every function

# 3. Optimize attribute serialization
# Don't serialize large objects
span.set_attribute("object.id", obj.id)  # Good
# span.set_attribute("object", json.dumps(large_obj))  # Bad

# 4. Use sampling for high-throughput applications
```

#### Issue 4: Missing LLM Token Counts

**Symptoms:**
- LLM calls traced but no token information

**Solutions:**

```python
# Ensure you're using compatible instrumentation
from openinference.instrumentation.openai import OpenAIInstrumentor

# Must instrument BEFORE creating OpenAI client
OpenAIInstrumentor().instrument()

client = openai.OpenAI()  # Create client after instrumentation

# For custom LLM calls, manually add token info
span.set_attribute("llm.token_count.prompt", response.usage.prompt_tokens)
span.set_attribute("llm.token_count.completion", response.usage.completion_tokens)
span.set_attribute("llm.token_count.total", response.usage.total_tokens)
```

---

## API Reference

### Phoenix Client API

```python
import phoenix as px

# Create client
client = px.Client(endpoint="http://localhost:6006")

# Get traces
traces_df = client.get_trace_dataset(
    project_name="my-project",
    start_time="2024-01-01T00:00:00Z",
    end_time="2024-01-31T23:59:59Z",
    limit=1000
)

# Get evaluations
evals_df = client.get_evaluations(
    project_name="my-project",
    trace_id="abc123"
)

# Log evaluations
client.log_evaluations(
    evaluations_df,
    eval_name="custom_eval"
)

# List projects
projects = client.list_projects()

# Delete project
client.delete_project("old-project")
```

### Tracer API

```python
from opentelemetry import trace

tracer = trace.get_tracer(
    instrumenting_module_name="my_app",
    instrumenting_library_version="1.0.0"
)

# Create span
with tracer.start_as_current_span("operation") as span:
    # Set attributes
    span.set_attribute("key", "value")

    # Add event
    span.add_event("event_name", {"attr": "value"})

    # Record exception
    try:
        risky_operation()
    except Exception as e:
        span.record_exception(e)

    # Set status
    from opentelemetry.trace import StatusCode
    span.set_status(StatusCode.OK)
```

### Evaluator API

```python
from phoenix.evals import (
    HallucinationEvaluator,
    RelevanceEvaluator,
    QAEvaluator,
    run_evals
)

# Create evaluator
evaluator = HallucinationEvaluator(
    model_name="gpt-4",
    temperature=0.0
)

# Evaluate single example
result = evaluator.evaluate(
    input="question",
    output="answer",
    context="context"
)

# Batch evaluation
results_df = run_evals(
    dataframe=traces_df,
    evaluators=[evaluator],
    provide_explanation=True,
    concurrency=5
)
```

---

## Performance & Security

### Performance Optimization

**1. Batch Processing:**
```python
from opentelemetry.sdk.trace.export import BatchSpanProcessor

processor = BatchSpanProcessor(
    exporter,
    max_queue_size=2048,
    max_export_batch_size=512,
    schedule_delay_millis=5000,
)
```

**2. Sampling:**
```python
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio

sampler = ParentBasedTraceIdRatio(0.1)  # Sample 10%
```

**3. Resource Limits:**
```python
span.set_attribute("text", text[:1000])  # Truncate large attributes
```

### Security Best Practices

**1. PII Sanitization:**
```python
def sanitize_pii(text):
    # Remove sensitive information
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    return text

span.set_attribute("input", sanitize_pii(user_input))
```

**2. Authentication:**
```python
# Use API keys for Phoenix Cloud
os.environ["PHOENIX_API_KEY"] = "your-api-key"
```

**3. Network Security:**
```bash
# Use HTTPS in production
export PHOENIX_COLLECTOR_ENDPOINT="https://phoenix.example.com"
```

---

## References & Resources

### Official Documentation
- **Phoenix Documentation**: https://docs.arize.com/phoenix
- **OpenTelemetry Python**: https://opentelemetry.io/docs/instrumentation/python/
- **OpenInference Spec**: https://github.com/Arize-ai/openinference

### GitHub Repositories
- **Phoenix**: https://github.com/Arize-ai/phoenix
- **OpenInference Instrumentation**: https://github.com/Arize-ai/openinference

### Tutorials & Guides
- **Getting Started Guide**: https://docs.arize.com/phoenix/quickstart
- **LangChain Integration**: https://docs.arize.com/phoenix/tracing/integrations-tracing/langchain
- **LlamaIndex Integration**: https://docs.arize.com/phoenix/tracing/integrations-tracing/llamaindex
- **Custom Instrumentation**: https://docs.arize.com/phoenix/tracing/how-to-tracing/manual-instrumentation

### Video Resources
- **Phoenix Introduction**: YouTube - Arize AI Channel
- **OpenTelemetry for LLMs**: Conf42 talks
- **RAG Observability**: LLM Engineering conferences

### Blog Posts
- **Arize AI Blog**: https://arize.com/blog
- **LLM Observability Patterns**: Arize AI technical blog
- **Production LLM Monitoring**: Engineering best practices

### Community
- **Discord**: Arize AI Community Discord
- **GitHub Discussions**: https://github.com/Arize-ai/phoenix/discussions
- **Slack**: Phoenix Users Slack Channel

### Academic Papers
- **OpenTelemetry for Distributed Tracing** (2020)
- **LLM Evaluation Metrics** - Various papers on hallucination detection, relevance assessment

### Tools & Extensions
- **Phoenix VS Code Extension**: Real-time trace viewing
- **Phoenix CLI**: Command-line tools for Phoenix
- **Grafana Integration**: Visualize Phoenix metrics in Grafana

### Related Technologies
- **OpenTelemetry**: https://opentelemetry.io
- **W3C Trace Context**: https://www.w3.org/TR/trace-context/
- **LangChain**: https://python.langchain.com
- **LlamaIndex**: https://docs.llamaindex.ai

---

## Conclusion

Arize Phoenix provides comprehensive observability for LLM applications through OpenTelemetry-based tracing, built-in evaluations, and real-time monitoring. Its framework-agnostic design, production-ready features, and developer-friendly interface make it an excellent choice for teams building and monitoring AI applications at scale.

**Key Takeaways:**
- Use Phoenix for production LLM monitoring and debugging
- Leverage OpenTelemetry standards for vendor-neutral observability
- Implement automated evaluations for quality assurance
- Follow best practices for performance and security
- Integrate with your existing tech stack seamlessly

For questions, issues, or contributions, visit the Phoenix GitHub repository or join the community Discord.

---

**Last Updated**: 2024-01-18
**Version**: 1.0
**Author**: Phoenix Documentation Team
**License**: Apache 2.0
