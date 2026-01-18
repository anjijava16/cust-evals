# Langfuse: The Complete Deep-Dive Guide

**Version**: 1.0.0 | **Updated**: January 2026 | **License**: MIT

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

### 1.1 What is Langfuse?

Langfuse is an open-source production observability and analytics platform for LLM applications. It provides comprehensive tracing, monitoring, and cost tracking capabilities designed specifically for production environments. Unlike development-focused tools, Langfuse excels at managing large-scale deployments with features like user feedback, prompt management, and detailed cost analytics.

**Core Philosophy:**
- **Production-First**: Built for real-world production workloads at scale
- **Cost Transparency**: Track every dollar spent on LLM calls
- **Open Source**: Self-hostable with cloud option available
- **Developer Experience**: Simple SDK with powerful observability

### 1.2 Key Features

#### Production Observability
- **Distributed Tracing**: Complete request traces across multiple services
- **Cost Tracking**: Token-level cost analytics with breakdowns by model, user, and feature
- **Performance Monitoring**: Latency tracking, error rates, and throughput metrics
- **User Analytics**: Per-user cost tracking and usage patterns

#### Prompt Management
- **Version Control**: Manage prompt versions with rollback capability
- **A/B Testing**: Compare prompt performance across versions
- **Prompt Registry**: Centralized prompt management for teams
- **Environment Variables**: Safely manage secrets in prompts

#### Quality Management
- **User Feedback**: Capture thumbs up/down and detailed feedback
- **Human Annotations**: Manual quality scoring and classification
- **Automated Scoring**: Custom evaluation pipelines
- **Dataset Management**: Build evaluation datasets from production data

#### Enterprise Features
- **Multi-tenancy**: Isolate data across organizations
- **Role-Based Access**: Fine-grained permissions
- **SSO Integration**: SAML and OAuth support
- **Audit Logs**: Complete activity tracking

### 1.3 When to Use Langfuse

**Perfect For:**
- Production LLM applications requiring detailed observability
- Teams needing cost optimization and budget tracking
- Organizations wanting prompt version control
- Companies requiring user feedback integration
- Enterprises needing multi-tenant deployments
- Teams transitioning from development to production

**Not Ideal For:**
- Quick prototypes (too much infrastructure overhead)
- Pure research projects (Phoenix or WandB better suited)
- Teams only needing evaluation (use RAGAS or DeepEval)
- Simple scripts without production requirements

### 1.4 Comparison Matrix

| Feature | Langfuse | Phoenix | LangSmith | Weights & Biases | Braintrust |
|---------|----------|---------|-----------|------------------|------------|
| **Setup Complexity** | Medium | Low | Low | Medium | Medium |
| **Cost Tracking** | ✅✅ Excellent | ⚠️ Basic | ✅ Good | ⚠️ Limited | ✅ Good |
| **Prompt Management** | ✅✅ Built-in | ❌ No | ✅ Yes | ❌ No | ✅ Yes |
| **Self-Hosting** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ⚠️ Enterprise |
| **User Feedback** | ✅✅ Excellent | ⚠️ Limited | ✅ Good | ⚠️ Limited | ✅ Good |
| **Multi-Framework** | ✅ Via OTEL | ✅ Via OTEL | ⚠️ LangChain | ✅ Yes | ✅ Yes |
| **Production Focus** | ✅✅ Primary | ⚠️ Dev Focus | ✅ Both | ⚠️ Research | ✅ Both |
| **Pricing** | Free + Cloud | Free | Subscription | Subscription | Usage-Based |
| **Dashboard** | ✅ Advanced | ✅ Good | ✅ Advanced | ✅✅ Excellent | ✅ Good |

---

## 2. Complete Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Your LLM Application                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Service A │  │  Service B │  │  Service C │            │
│  │  (API)     │  │  (Worker)  │  │  (Batch)   │            │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘            │
│         │                │                │                  │
│         └────────────────┴────────────────┘                  │
│                          │                                   │
│                 Langfuse SDK                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS/gRPC
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Langfuse Platform                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Ingestion   │  │  Processing  │  │   Storage    │      │
│  │  API         │──│  Pipeline    │──│  PostgreSQL  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Analytics   │  │  Dashboard   │  │  Exports     │      │
│  │  Engine      │  │  UI          │  │  API         │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Core Components

#### SDK Layer
```python
# Components in langfuse package
langfuse/
├── client.py           # Main client interface
├── decorators.py       # @observe decorator
├── openai.py          # OpenAI integration
├── anthropic.py       # Anthropic integration
├── llama_index.py     # LlamaIndex callback
├── langchain.py       # LangChain integration
├── model.py           # Data models (Trace, Span, Generation)
└── api/               # REST API client
```

#### Trace Hierarchy
```
Trace (Top-level request)
├── Span (Component execution)
│   ├── Generation (LLM call)
│   │   ├── Input tokens: 150
│   │   ├── Output tokens: 75
│   │   ├── Cost: $0.00045
│   │   └── Latency: 1.2s
│   ├── Span (Sub-component)
│   └── Event (Log point)
└── Metadata (User ID, tags, session)
```

### 2.3 Data Flow

```
Request → @observe → Trace Created → Spans Logged → Generations Tracked
    │          │            │              │              │
    │          │            │              │              └─→ Token counting
    │          │            │              │                  Cost calculation
    │          │            │              │
    │          │            │              └─→ Timing metrics
    │          │            │                  Error tracking
    │          │            │
    │          │            └─→ Metadata attachment
    │          │                User/Session linking
    │          │
    │          └─→ Async background upload
    │              to Langfuse platform
    │
    └─→ Continue execution
        (non-blocking)
```

---

## 3. Installation & Setup

### 3.1 Installation

```bash
# Basic installation
pip install langfuse

# With OpenAI integration
pip install langfuse openai

# With LangChain integration
pip install langfuse langchain

# With LlamaIndex integration
pip install langfuse llama-index

# With all integrations
pip install langfuse[all]

# Self-hosted deployment
docker compose up -d
```

### 3.2 Cloud Setup (Quickest Start)

```python
# 1. Sign up at https://cloud.langfuse.com
# 2. Create a new project
# 3. Copy your API keys

import os
from langfuse import Langfuse

# Configure credentials
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"

# Initialize client
langfuse = Langfuse()

# Test connection
print(langfuse.auth_check())  # Should return True
```

### 3.3 Self-Hosted Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: langfuse
      POSTGRES_PASSWORD: langfuse
      POSTGRES_DB: langfuse
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  langfuse-server:
    image: langfuse/langfuse:latest
    depends_on:
      - postgres
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://langfuse:langfuse@postgres:5432/langfuse
      NEXTAUTH_SECRET: your-secret-key-here
      NEXTAUTH_URL: http://localhost:3000
      SALT: your-salt-here
      ENCRYPTION_KEY: your-encryption-key-here
      TELEMETRY_ENABLED: false

volumes:
  postgres_data:
```

```bash
# Start services
docker compose up -d

# Check logs
docker compose logs -f langfuse-server

# Access UI
open http://localhost:3000

# Create first user through UI
# Then configure SDK to point to your instance
export LANGFUSE_HOST="http://localhost:3000"
```

### 3.4 Configuration Options

```python
from langfuse import Langfuse

# Full configuration
langfuse = Langfuse(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    host="https://cloud.langfuse.com",

    # Performance tuning
    flush_at=15,                    # Flush after N events
    flush_interval=0.5,             # Flush every N seconds
    max_retries=3,                  # Retry failed requests
    timeout=10,                     # Request timeout (seconds)

    # Debugging
    debug=False,                    # Enable debug logging
    enabled=True,                   # Feature flag

    # Sampling
    sample_rate=1.0,               # Trace % of requests (0.0-1.0)

    # Threading
    threads=1,                      # Worker threads for uploads
)
```

---

## 4. Core Concepts

### 4.1 Traces

A trace represents a single request or user interaction through your system.

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Manual trace creation
trace = langfuse.trace(
    name="chatbot-request",
    user_id="user-123",
    session_id="session-456",
    metadata={
        "environment": "production",
        "version": "1.0.0",
        "endpoint": "/api/chat"
    },
    tags=["chatbot", "customer-support"],
    input={"question": "How do I reset my password?"},
    output={"answer": "You can reset your password..."}
)

# Update trace later
trace.update(
    output={"answer": "Updated response"},
    metadata={"response_time_ms": 1234}
)
```

### 4.2 Spans

Spans represent operations within a trace (function calls, database queries, etc.).

```python
# Create span within trace
span = trace.span(
    name="retrieve-documents",
    input={"query": "password reset"},
    metadata={"retriever": "semantic-search"}
)

# Nest spans
sub_span = span.span(
    name="vector-search",
    input={"embedding": "[0.1, 0.2, ...]"}
)

# Close spans
sub_span.end(output={"documents": ["doc1", "doc2"]})
span.end(output={"count": 2})
```

### 4.3 Generations

Generations are special spans for LLM calls with automatic token and cost tracking.

```python
# Track LLM generation
generation = trace.generation(
    name="gpt-4-response",
    model="gpt-4-turbo-preview",
    model_parameters={
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 0.9
    },
    input=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Explain quantum computing"}
    ],
    output="Quantum computing uses quantum mechanics...",
    usage={
        "input": 150,
        "output": 75,
        "total": 225,
        "unit": "TOKENS"
    },
    metadata={
        "provider": "openai",
        "stream": False
    }
)

# Langfuse automatically calculates costs based on model pricing
```

### 4.4 Events

Events are lightweight log points within traces.

```python
# Log events
trace.event(
    name="cache-hit",
    metadata={"key": "user-123-context", "ttl": 3600}
)

trace.event(
    name="validation-failed",
    level="WARNING",
    metadata={"field": "email", "error": "Invalid format"}
)

trace.event(
    name="external-api-call",
    input={"service": "stripe", "endpoint": "/v1/charges"},
    output={"status": 200, "charge_id": "ch_123"}
)
```

### 4.5 Scores and Feedback

```python
# Add user feedback
langfuse.score(
    trace_id=trace.id,
    name="user-feedback",
    value=1,  # 1 = thumbs up, 0 = thumbs down
    comment="Very helpful response!"
)

# Add automated evaluation score
langfuse.score(
    trace_id=trace.id,
    name="hallucination-score",
    value=0.95,  # 0-1 scale
    comment="No factual errors detected"
)

# Add human annotation
langfuse.score(
    trace_id=trace.id,
    name="response-quality",
    value=4,  # 1-5 scale
    comment="Accurate but could be more concise",
    data_type="NUMERIC"
)
```

---

## 5. Complete Examples Section

### Example 1: Basic Tracing with Decorator

**Use Case**: Simple function tracing with automatic instrumentation

```python
from langfuse.decorators import observe, langfuse_context
from langfuse import Langfuse
import os

# Configure
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."

# Simple function tracing
@observe()
def generate_response(question: str) -> str:
    """Generate a response to user question"""
    # This creates a trace automatically
    return f"Answer to: {question}"

# Nested function tracing
@observe()
def chatbot_pipeline(user_input: str, user_id: str):
    """Complete chatbot pipeline with nested traces"""

    # Set trace metadata
    langfuse_context.update_current_trace(
        user_id=user_id,
        tags=["chatbot", "v2"],
        metadata={"model": "gpt-4"}
    )

    # These calls create nested spans
    context = retrieve_context(user_input)
    response = generate_with_context(context, user_input)

    return response

@observe()
def retrieve_context(query: str) -> list:
    """Retrieve relevant context"""
    langfuse_context.update_current_observation(
        name="context-retrieval",
        metadata={"retriever": "semantic"}
    )
    return ["context1", "context2"]

@observe()
def generate_with_context(context: list, query: str) -> str:
    """Generate response with context"""
    langfuse_context.update_current_observation(
        name="generation",
        metadata={"context_count": len(context)}
    )
    return "Generated response"

# Usage
if __name__ == "__main__":
    result = chatbot_pipeline(
        "What is machine learning?",
        user_id="user-123"
    )
    print(result)

    # Flush to ensure data is sent
    langfuse_context.flush()
```

**Output in Langfuse UI:**
```
Trace: chatbot_pipeline
├── Span: context-retrieval (retrieve_context)
│   Duration: 45ms
└── Span: generation (generate_with_context)
    Duration: 1.2s

Total Duration: 1.245s
User: user-123
Tags: chatbot, v2
```

### Example 2: OpenAI Integration with Cost Tracking

**Use Case**: Track OpenAI costs and performance automatically

```python
import os
from langfuse.openai import openai
from langfuse.decorators import observe, langfuse_context

# Configure
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."

# OpenAI client with Langfuse tracking
client = openai.OpenAI()

@observe()
def multi_model_comparison(prompt: str, user_id: str):
    """Compare responses from multiple models"""

    langfuse_context.update_current_trace(
        name="model-comparison",
        user_id=user_id,
        metadata={"prompt_version": "v2"}
    )

    models = ["gpt-3.5-turbo", "gpt-4-turbo-preview"]
    results = {}

    for model in models:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            # Langfuse automatically tracks this generation
            name=f"generation-{model}",  # Custom name for Langfuse
        )

        results[model] = response.choices[0].message.content

        # Log model-specific metadata
        langfuse_context.update_current_observation(
            metadata={
                "model": model,
                "tokens_used": response.usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason
            }
        )

    return results

@observe()
def streaming_chat(messages: list, user_id: str):
    """Streaming chat with cost tracking"""

    langfuse_context.update_current_trace(
        user_id=user_id,
        session_id=f"chat-{user_id}"
    )

    full_response = ""

    # Streaming is automatically tracked
    stream = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        stream=True,
        name="streaming-generation"
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            print(content, end="", flush=True)

    print()  # New line

    # Costs are tracked even for streaming
    return full_response

# Usage examples
if __name__ == "__main__":
    # Compare models
    print("Comparing models...")
    comparison = multi_model_comparison(
        "Explain quantum entanglement in simple terms",
        user_id="scientist-42"
    )

    for model, response in comparison.items():
        print(f"\n{model}:\n{response}\n")

    # Streaming chat
    print("\nStreaming response:")
    messages = [
        {"role": "system", "content": "You are a physics tutor"},
        {"role": "user", "content": "What is the speed of light?"}
    ]
    streaming_chat(messages, user_id="student-99")

    # Flush all traces
    langfuse_context.flush()

# View in Langfuse Dashboard:
# - Total cost per model
# - Token usage breakdown
# - Latency comparison
# - Per-user cost analytics
```

**Dashboard View:**
```
Cost Analytics (Last 24h):
├── gpt-4-turbo-preview: $0.45 (150 requests)
├── gpt-3.5-turbo: $0.08 (150 requests)
└── Total: $0.53

Per User:
├── scientist-42: $0.30 (50 requests)
└── student-99: $0.23 (100 requests)
```

### Example 3: LangChain Integration with Session Tracking

**Use Case**: Track multi-turn conversations with LangChain

```python
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langfuse.callback import CallbackHandler

# Configure
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."

class ConversationBot:
    """Chatbot with session tracking"""

    def __init__(self, session_id: str, user_id: str):
        self.session_id = session_id
        self.user_id = user_id
        self.memory = ConversationBufferMemory(return_messages=True)

        # Initialize LangChain with Langfuse callback
        self.langfuse_handler = CallbackHandler(
            session_id=session_id,
            user_id=user_id,
            tags=["chatbot", "langchain"],
            metadata={
                "session_type": "customer_support",
                "channel": "web"
            }
        )

        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            callbacks=[self.langfuse_handler]
        )

    def chat(self, user_message: str) -> str:
        """Send message and get response"""

        # Create new trace for this turn
        self.langfuse_handler.set_trace_params(
            name=f"chat-turn-{self.get_turn_count()}",
            metadata={
                "turn": self.get_turn_count(),
                "message_length": len(user_message)
            }
        )

        # Build messages with history
        messages = [
            SystemMessage(content="You are a helpful customer support agent")
        ]

        # Add conversation history
        messages.extend(self.memory.chat_memory.messages)

        # Add new user message
        messages.append(HumanMessage(content=user_message))

        # Get response (automatically tracked by Langfuse)
        response = self.llm.invoke(messages)

        # Update memory
        self.memory.chat_memory.add_user_message(user_message)
        self.memory.chat_memory.add_ai_message(response.content)

        return response.content

    def get_turn_count(self) -> int:
        """Get current turn number"""
        return len(self.memory.chat_memory.messages) // 2

    def end_session(self):
        """End conversation session"""
        self.langfuse_handler.flush()

# Usage: Multi-turn conversation
if __name__ == "__main__":
    # Start new session
    bot = ConversationBot(
        session_id="support-session-789",
        user_id="customer-456"
    )

    # Conversation turns
    print("Customer: I can't access my account")
    response1 = bot.chat("I can't access my account")
    print(f"Agent: {response1}\n")

    print("Customer: I tried resetting but didn't get the email")
    response2 = bot.chat("I tried resetting but didn't get the email")
    print(f"Agent: {response2}\n")

    print("Customer: It worked! Thank you!")
    response3 = bot.chat("It worked! Thank you!")
    print(f"Agent: {response3}\n")

    # End session
    bot.end_session()

# View in Langfuse:
# - Session timeline with all turns
# - Total cost for conversation
# - Average response time
# - Conversation flow visualization
```

**Langfuse Session View:**
```
Session: support-session-789 (User: customer-456)
Duration: 5m 23s
Total Cost: $0.024
Turns: 3

Timeline:
├── Turn 1: "I can't access..." (0:00)
│   Cost: $0.008 | Latency: 1.2s
├── Turn 2: "I tried resetting..." (1:45)
│   Cost: $0.009 | Latency: 1.4s
└── Turn 3: "It worked..." (4:30)
    Cost: $0.007 | Latency: 0.9s
```

### Example 4: RAG Pipeline with Detailed Tracing

**Use Case**: Track every component of a RAG system

```python
import os
from typing import List, Dict
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from openai import OpenAI
import numpy as np

# Configure
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."

langfuse = Langfuse()
openai_client = OpenAI()

class RAGPipeline:
    """Production RAG pipeline with comprehensive tracing"""

    @observe()
    def query(self, question: str, user_id: str, trace_id: str = None) -> Dict:
        """Main RAG query endpoint"""

        # Set trace metadata
        langfuse_context.update_current_trace(
            name="rag-query",
            user_id=user_id,
            tags=["rag", "production"],
            metadata={
                "pipeline_version": "v2.1",
                "question_length": len(question)
            }
        )

        # Pipeline steps
        embedding = self.embed_query(question)
        documents = self.retrieve_documents(embedding, top_k=5)
        reranked = self.rerank_documents(question, documents)
        answer = self.generate_answer(question, reranked)

        # Compile result
        result = {
            "answer": answer["text"],
            "sources": [d["id"] for d in reranked],
            "confidence": answer["confidence"]
        }

        return result

    @observe()
    def embed_query(self, text: str) -> List[float]:
        """Generate query embedding"""

        langfuse_context.update_current_observation(
            name="embedding-generation",
            input={"text": text, "model": "text-embedding-3-small"}
        )

        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        embedding = response.data[0].embedding

        langfuse_context.update_current_observation(
            output={"dimension": len(embedding)},
            metadata={
                "tokens": response.usage.total_tokens,
                "model": response.model
            }
        )

        return embedding

    @observe()
    def retrieve_documents(self, embedding: List[float], top_k: int) -> List[Dict]:
        """Retrieve similar documents from vector store"""

        langfuse_context.update_current_observation(
            name="vector-search",
            input={"embedding_dim": len(embedding), "top_k": top_k},
            metadata={"index": "documents-v2", "metric": "cosine"}
        )

        # Simulate vector database query
        import time
        start = time.time()

        # Mock results
        documents = [
            {"id": f"doc-{i}", "content": f"Content {i}", "score": 0.9 - i*0.1}
            for i in range(top_k)
        ]

        search_time = time.time() - start

        langfuse_context.update_current_observation(
            output={"documents_found": len(documents)},
            metadata={
                "search_time_ms": search_time * 1000,
                "avg_score": np.mean([d["score"] for d in documents])
            }
        )

        return documents

    @observe()
    def rerank_documents(self, query: str, documents: List[Dict]) -> List[Dict]:
        """Rerank documents for relevance"""

        langfuse_context.update_current_observation(
            name="reranking",
            input={
                "query": query,
                "document_count": len(documents)
            },
            metadata={"reranker": "cross-encoder"}
        )

        # Simulate reranking (in production, use actual reranker)
        reranked = sorted(documents, key=lambda x: x["score"], reverse=True)[:3]

        langfuse_context.update_current_observation(
            output={"reranked_count": len(reranked)},
            metadata={
                "score_improvement": 0.15,
                "top_score": reranked[0]["score"]
            }
        )

        return reranked

    @observe()
    def generate_answer(self, question: str, documents: List[Dict]) -> Dict:
        """Generate answer using retrieved context"""

        # Build context
        context = "\n\n".join([
            f"Document {d['id']}: {d['content']}"
            for d in documents
        ])

        langfuse_context.update_current_observation(
            name="answer-generation",
            input={
                "question": question,
                "context_length": len(context),
                "num_sources": len(documents)
            }
        )

        # Generate with GPT-4
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "Answer based on provided context. Cite sources."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}"
                }
            ],
            temperature=0.3
        )

        answer_text = response.choices[0].message.content

        langfuse_context.update_current_observation(
            output={"answer": answer_text},
            metadata={
                "model": "gpt-4-turbo-preview",
                "tokens_used": response.usage.total_tokens,
                "cost_usd": self.calculate_cost(response.usage)
            }
        )

        return {
            "text": answer_text,
            "confidence": 0.85  # Mock confidence
        }

    def calculate_cost(self, usage) -> float:
        """Calculate cost based on usage"""
        # GPT-4 Turbo pricing (as of Jan 2026)
        input_cost = usage.prompt_tokens * 0.00001
        output_cost = usage.completion_tokens * 0.00003
        return input_cost + output_cost

# Usage
if __name__ == "__main__":
    pipeline = RAGPipeline()

    result = pipeline.query(
        question="What is the refund policy?",
        user_id="customer-123"
    )

    print(f"Answer: {result['answer']}")
    print(f"Sources: {result['sources']}")
    print(f"Confidence: {result['confidence']}")

    # Flush traces
    langfuse_context.flush()

# View in Langfuse:
# - Complete pipeline visualization
# - Cost breakdown by component
# - Latency waterfall chart
# - Document retrieval quality metrics
```

**Langfuse Trace View:**
```
RAG Query (2.3s total, $0.012)
├── embedding-generation (0.2s, $0.00001)
│   Input tokens: 15
├── vector-search (0.1s, $0)
│   Documents: 5 → 5
├── reranking (0.3s, $0)
│   Documents: 5 → 3
└── answer-generation (1.7s, $0.01199)
    Input tokens: 450
    Output tokens: 120

Cost Breakdown:
- Embedding: 0.08%
- Generation: 99.92%
```

### Example 5: Prompt Management and A/B Testing

**Use Case**: Manage prompt versions and compare performance

```python
import os
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from openai import OpenAI
from typing import Dict
import random

# Configure
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."

langfuse = Langfuse()
openai_client = OpenAI()

# Step 1: Create prompt in Langfuse UI or via API
def create_prompts():
    """Create prompt templates in Langfuse"""

    # Version A: Concise
    langfuse.create_prompt(
        name="customer-support-prompt",
        prompt="You are a helpful customer support agent. Be concise and professional.\n\nCustomer: {{question}}\nAgent:",
        labels=["production"],
        tags=["customer-support", "v1"]
    )

    # Version B: Empathetic
    langfuse.create_prompt(
        name="customer-support-prompt",
        prompt="You are a warm and empathetic customer support agent. Show understanding and provide detailed help.\n\nCustomer: {{question}}\nAgent:",
        labels=["production"],
        tags=["customer-support", "v2"]
    )

class PromptManager:
    """Manage prompts with A/B testing"""

    def __init__(self):
        self.langfuse = Langfuse()

    @observe()
    def answer_question(self, question: str, user_id: str) -> Dict:
        """Answer with A/B testing"""

        # Randomly select prompt version (50/50 split)
        version = random.choice(["v1", "v2"])

        langfuse_context.update_current_trace(
            name="customer-support",
            user_id=user_id,
            tags=["ab-test", f"prompt-{version}"],
            metadata={"experiment": "concise_vs_empathetic"}
        )

        # Fetch prompt from Langfuse
        prompt_template = self.langfuse.get_prompt(
            name="customer-support-prompt",
            label="production",
            version=version
        )

        # Compile prompt with variables
        prompt_text = prompt_template.compile(question=question)

        langfuse_context.update_current_observation(
            metadata={
                "prompt_name": prompt_template.name,
                "prompt_version": prompt_template.version,
                "prompt_id": prompt_template.id
            }
        )

        # Generate response
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.7
        )

        answer = response.choices[0].message.content

        # Link prompt to generation for tracking
        langfuse_context.update_current_observation(
            output={"answer": answer},
            metadata={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens
            }
        )

        return {
            "answer": answer,
            "prompt_version": version,
            "trace_id": langfuse_context.get_current_trace_id()
        }

    def add_user_feedback(self, trace_id: str, helpful: bool, comment: str = None):
        """Add user feedback for A/B test"""

        self.langfuse.score(
            trace_id=trace_id,
            name="user-feedback",
            value=1 if helpful else 0,
            comment=comment
        )

# Usage
if __name__ == "__main__":
    manager = PromptManager()

    # Simulate multiple users
    questions = [
        "How do I track my order?",
        "I need to return an item",
        "What's your shipping policy?",
        "My order hasn't arrived"
    ]

    results = []

    for i, question in enumerate(questions):
        print(f"\nQuestion: {question}")

        result = manager.answer_question(
            question=question,
            user_id=f"user-{i}"
        )

        print(f"Prompt Version: {result['prompt_version']}")
        print(f"Answer: {result['answer'][:100]}...")

        # Simulate user feedback
        helpful = random.choice([True, True, True, False])  # 75% positive
        manager.add_user_feedback(
            trace_id=result["trace_id"],
            helpful=helpful,
            comment="Great response!" if helpful else "Could be better"
        )

        results.append(result)

    # Flush all data
    langfuse_context.flush()

    print("\n✅ A/B test data sent to Langfuse")
    print("View analytics at: https://cloud.langfuse.com")

# View in Langfuse Dashboard:
# - Compare prompt versions side-by-side
# - Feedback rates: v1 vs v2
# - Average latency per version
# - Token usage comparison
# - Cost per version
```

**A/B Test Results (Langfuse Dashboard):**
```
Prompt A/B Test: concise_vs_empathetic

Version 1 (Concise):
- Requests: 523
- Positive Feedback: 72%
- Avg Latency: 1.2s
- Avg Cost: $0.008
- Avg Tokens: 180

Version 2 (Empathetic):
- Requests: 527
- Positive Feedback: 81%  ← 9% improvement
- Avg Latency: 1.5s
- Avg Cost: $0.012
- Avg Tokens: 280

Recommendation: Deploy Version 2 (better feedback despite higher cost)
```

### Example 6: Cost Optimization and Budget Alerts

**Use Case**: Monitor costs and implement budget controls

```python
import os
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from openai import OpenAI
from typing import Dict, Optional
from datetime import datetime, timedelta

# Configure
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."

langfuse = Langfuse()
openai_client = OpenAI()

class CostAwareService:
    """Service with cost tracking and budget enforcement"""

    def __init__(self, daily_budget: float = 10.0):
        self.langfuse = Langfuse()
        self.daily_budget = daily_budget
        self.cache = {}  # Simple cache for cost optimization

    def get_today_cost(self) -> float:
        """Get total cost for today"""
        # In production, query Langfuse API for today's costs
        # For demo, we'll simulate

        # Langfuse API endpoint
        # GET /api/public/metrics/daily
        # Returns cost breakdown by date

        return 7.50  # Mock value

    def check_budget(self) -> Dict:
        """Check if we're within budget"""
        today_cost = self.get_today_cost()
        remaining = self.daily_budget - today_cost

        return {
            "within_budget": remaining > 0,
            "spent": today_cost,
            "budget": self.daily_budget,
            "remaining": remaining,
            "utilization": (today_cost / self.daily_budget) * 100
        }

    @observe()
    def smart_completion(
        self,
        prompt: str,
        user_id: str,
        use_cache: bool = True,
        allow_fallback: bool = True
    ) -> Dict:
        """Cost-aware completion with fallback"""

        langfuse_context.update_current_trace(
            name="smart-completion",
            user_id=user_id,
            metadata={"cost_optimization": "enabled"}
        )

        # Check budget
        budget_status = self.check_budget()
        langfuse_context.update_current_observation(
            metadata={"budget_status": budget_status}
        )

        if not budget_status["within_budget"]:
            langfuse_context.update_current_trace(
                tags=["budget-exceeded"]
            )
            return {
                "error": "Daily budget exceeded",
                "budget_status": budget_status
            }

        # Check cache
        cache_key = f"prompt:{hash(prompt)}"
        if use_cache and cache_key in self.cache:
            langfuse_context.update_current_observation(
                metadata={"cache": "hit"}
            )
            return {
                "answer": self.cache[cache_key],
                "cached": True,
                "cost": 0.0
            }

        # Determine model based on budget
        model = self.select_model(budget_status)

        langfuse_context.update_current_observation(
            metadata={
                "selected_model": model,
                "budget_utilization": f"{budget_status['utilization']:.1f}%"
            }
        )

        # Generate completion
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        answer = response.choices[0].message.content
        cost = self.calculate_cost(model, response.usage)

        # Cache result
        if use_cache:
            self.cache[cache_key] = answer

        langfuse_context.update_current_observation(
            output={"answer": answer},
            metadata={
                "cost": cost,
                "cached": False
            }
        )

        return {
            "answer": answer,
            "cached": False,
            "cost": cost,
            "model": model
        }

    def select_model(self, budget_status: Dict) -> str:
        """Select model based on budget"""
        utilization = budget_status["utilization"]

        if utilization > 90:
            return "gpt-3.5-turbo"  # Cheap model
        elif utilization > 70:
            return "gpt-4-turbo-preview"  # Mid-tier
        else:
            return "gpt-4-turbo-preview"  # Best model

    def calculate_cost(self, model: str, usage) -> float:
        """Calculate cost for model"""
        pricing = {
            "gpt-3.5-turbo": {"input": 0.0000005, "output": 0.0000015},
            "gpt-4-turbo-preview": {"input": 0.00001, "output": 0.00003}
        }

        if model not in pricing:
            return 0.0

        input_cost = usage.prompt_tokens * pricing[model]["input"]
        output_cost = usage.completion_tokens * pricing[model]["output"]
        return input_cost + output_cost

# Usage
if __name__ == "__main__":
    service = CostAwareService(daily_budget=10.0)

    # Test requests
    prompts = [
        "Explain quantum computing",
        "What is machine learning?",
        "Explain quantum computing",  # Duplicate - should hit cache
        "Describe neural networks"
    ]

    for i, prompt in enumerate(prompts):
        print(f"\n--- Request {i+1} ---")
        print(f"Prompt: {prompt}")

        result = service.smart_completion(
            prompt=prompt,
            user_id=f"user-{i}",
            use_cache=True
        )

        if "error" in result:
            print(f"❌ Error: {result['error']}")
            print(f"Budget: ${result['budget_status']['spent']:.2f} / ${result['budget_status']['budget']:.2f}")
        else:
            print(f"✅ Model: {result.get('model', 'cached')}")
            print(f"Cached: {result['cached']}")
            print(f"Cost: ${result['cost']:.6f}")
            print(f"Answer: {result['answer'][:100]}...")

    # Flush traces
    langfuse_context.flush()

    # Get final budget status
    print("\n--- Final Budget Status ---")
    final_status = service.check_budget()
    print(f"Spent: ${final_status['spent']:.2f}")
    print(f"Remaining: ${final_status['remaining']:.2f}")
    print(f"Utilization: {final_status['utilization']:.1f}%")

# View in Langfuse:
# - Daily cost trends
# - Cost by user
# - Cost by model
# - Cache hit rates
# - Budget utilization charts
```

**Langfuse Cost Dashboard:**
```
Daily Cost Report (Jan 18, 2026)

Total Spent: $7.50 / $10.00 (75%)

By Model:
├── gpt-4-turbo-preview: $6.80 (91%)
└── gpt-3.5-turbo: $0.70 (9%)

By User:
├── user-0: $2.30
├── user-1: $2.10
├── user-2: $0.00 (cached)
└── user-3: $2.40

Cache Performance:
- Requests: 4
- Cache Hits: 1 (25%)
- Cost Saved: $2.20

Trends:
📈 +15% vs yesterday
⚠️ Approaching budget limit
```

### Example 7: Error Tracking and Debugging

**Use Case**: Track errors and failures for debugging

```python
import os
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from openai import OpenAI
from typing import Dict, List
import time

# Configure
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."

langfuse = Langfuse()
openai_client = OpenAI()

class RobustService:
    """Service with comprehensive error tracking"""

    @observe()
    def process_request(self, user_input: str, user_id: str) -> Dict:
        """Main processing with error handling"""

        langfuse_context.update_current_trace(
            name="robust-processing",
            user_id=user_id
        )

        try:
            # Validate input
            self.validate_input(user_input)

            # Process
            result = self.generate_response(user_input)

            # Validate output
            self.validate_output(result)

            langfuse_context.update_current_trace(
                tags=["success"]
            )

            return {"success": True, "result": result}

        except ValueError as e:
            return self.handle_error("validation_error", str(e))
        except TimeoutError as e:
            return self.handle_error("timeout", str(e))
        except Exception as e:
            return self.handle_error("unknown_error", str(e))

    @observe()
    def validate_input(self, text: str):
        """Validate input with error tracking"""

        langfuse_context.update_current_observation(
            name="input-validation",
            input={"text_length": len(text)}
        )

        if not text or len(text) < 3:
            langfuse_context.update_current_observation(
                level="ERROR",
                status_message="Input too short"
            )
            raise ValueError("Input must be at least 3 characters")

        if len(text) > 5000:
            langfuse_context.update_current_observation(
                level="ERROR",
                status_message="Input too long"
            )
            raise ValueError("Input exceeds 5000 character limit")

        langfuse_context.update_current_observation(
            output={"valid": True},
            level="DEFAULT"
        )

    @observe()
    def generate_response(self, prompt: str, max_retries: int = 3) -> str:
        """Generate with retry logic"""

        langfuse_context.update_current_observation(
            name="generation-with-retry",
            input={"prompt": prompt, "max_retries": max_retries}
        )

        for attempt in range(max_retries):
            try:
                langfuse_context.update_current_observation(
                    metadata={"attempt": attempt + 1}
                )

                response = openai_client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    timeout=10  # 10 second timeout
                )

                return response.choices[0].message.content

            except TimeoutError:
                langfuse_context.update_current_observation(
                    level="WARNING",
                    status_message=f"Timeout on attempt {attempt + 1}"
                )

                if attempt == max_retries - 1:
                    raise

                # Exponential backoff
                time.sleep(2 ** attempt)

            except Exception as e:
                langfuse_context.update_current_observation(
                    level="ERROR",
                    status_message=f"Error on attempt {attempt + 1}: {str(e)}"
                )
                raise

    @observe()
    def validate_output(self, text: str):
        """Validate output quality"""

        langfuse_context.update_current_observation(
            name="output-validation",
            input={"text_length": len(text)}
        )

        # Check for common issues
        issues = []

        if len(text) < 10:
            issues.append("response_too_short")

        if "I apologize" in text and "cannot" in text:
            issues.append("refusal_detected")

        if issues:
            langfuse_context.update_current_observation(
                level="WARNING",
                status_message=f"Quality issues: {', '.join(issues)}",
                metadata={"issues": issues}
            )
            raise ValueError(f"Output quality issues: {issues}")

        langfuse_context.update_current_observation(
            output={"valid": True}
        )

    def handle_error(self, error_type: str, message: str) -> Dict:
        """Handle and track errors"""

        langfuse_context.update_current_trace(
            tags=["error", error_type],
            metadata={
                "error_type": error_type,
                "error_message": message
            }
        )

        langfuse_context.update_current_observation(
            level="ERROR",
            status_message=message
        )

        return {
            "success": False,
            "error_type": error_type,
            "error_message": message
        }

# Usage
if __name__ == "__main__":
    service = RobustService()

    # Test cases including errors
    test_cases = [
        ("Explain quantum computing", "user-1", "success"),
        ("Hi", "user-2", "too_short"),
        ("x" * 6000, "user-3", "too_long"),
        ("Valid question here", "user-4", "success"),
    ]

    for prompt, user_id, expected in test_cases:
        print(f"\n--- Test: {expected} ---")
        print(f"Input: {prompt[:50]}...")

        result = service.process_request(prompt, user_id)

        if result["success"]:
            print(f"✅ Success: {result['result'][:100]}...")
        else:
            print(f"❌ Error: {result['error_type']}")
            print(f"   Message: {result['error_message']}")

    # Flush traces
    langfuse_context.flush()

# View in Langfuse:
# - Error rate by type
# - Failed traces with full context
# - Retry patterns
# - Error distribution over time
```

**Langfuse Error Dashboard:**
```
Error Analysis (Last 24h)

Total Requests: 1,234
Errors: 45 (3.6%)

By Type:
├── validation_error: 28 (62%)
│   ├── input_too_short: 15
│   └── input_too_long: 13
├── timeout: 12 (27%)
└── unknown_error: 5 (11%)

Error Rate Over Time:
08:00 ██░░░░ 2%
12:00 ████░░ 4% ← Spike
16:00 ██░░░░ 2%
20:00 █░░░░░ 1%

Top Failed Traces:
1. trace-abc123: timeout (3 retries)
2. trace-def456: validation_error
3. trace-ghi789: unknown_error
```

### Example 8: Production Monitoring Dashboard

**Use Case**: Real-time production monitoring and alerting

```python
import os
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from openai import OpenAI
from typing import Dict, List
from datetime import datetime
import json

# Configure
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."

langfuse = Langfuse()
openai_client = OpenAI()

class ProductionService:
    """Production service with comprehensive monitoring"""

    def __init__(self):
        self.langfuse = Langfuse()
        self.alert_thresholds = {
            "latency_p95": 3.0,  # seconds
            "error_rate": 0.05,  # 5%
            "cost_per_request": 0.05,  # $0.05
        }

    @observe()
    def handle_request(
        self,
        request_data: Dict,
        user_id: str,
        session_id: str = None
    ) -> Dict:
        """Handle production request with monitoring"""

        start_time = datetime.now()

        # Set comprehensive trace metadata
        langfuse_context.update_current_trace(
            name="production-request",
            user_id=user_id,
            session_id=session_id,
            tags=["production", "monitored"],
            metadata={
                "timestamp": start_time.isoformat(),
                "request_id": request_data.get("request_id"),
                "endpoint": request_data.get("endpoint"),
                "client_version": request_data.get("client_version"),
                "environment": "production"
            }
        )

        try:
            # Process request
            result = self.process_business_logic(request_data)

            # Calculate metrics
            duration = (datetime.now() - start_time).total_seconds()

            # Update trace with success metrics
            langfuse_context.update_current_trace(
                output=result,
                metadata={
                    "duration_seconds": duration,
                    "status": "success"
                }
            )

            # Check SLA compliance
            self.check_sla(duration, cost=result.get("cost", 0))

            return result

        except Exception as e:
            # Track error
            duration = (datetime.now() - start_time).total_seconds()

            langfuse_context.update_current_trace(
                level="ERROR",
                status_message=str(e),
                metadata={
                    "duration_seconds": duration,
                    "status": "error",
                    "error_type": type(e).__name__
                },
                tags=["error"]
            )

            # Trigger alert
            self.send_alert("error", str(e))

            raise

    @observe()
    def process_business_logic(self, data: Dict) -> Dict:
        """Business logic processing"""

        langfuse_context.update_current_observation(
            name="business-logic",
            input=data
        )

        # Example: Multi-step processing
        enriched_data = self.enrich_data(data)
        llm_result = self.call_llm(enriched_data)
        final_result = self.post_process(llm_result)

        langfuse_context.update_current_observation(
            output=final_result,
            metadata={
                "processing_steps": 3
            }
        )

        return final_result

    @observe()
    def enrich_data(self, data: Dict) -> Dict:
        """Enrich request data"""

        langfuse_context.update_current_observation(
            name="data-enrichment"
        )

        # Add context, user history, etc.
        enriched = {
            **data,
            "context": "Additional context",
            "user_history": ["prev1", "prev2"]
        }

        return enriched

    @observe()
    def call_llm(self, data: Dict) -> str:
        """Call LLM with monitoring"""

        langfuse_context.update_current_observation(
            name="llm-generation",
            metadata={"model": "gpt-4-turbo-preview"}
        )

        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": data.get("query", "")}
            ]
        )

        result = response.choices[0].message.content

        # Track token usage
        langfuse_context.update_current_observation(
            output={"response": result},
            metadata={
                "tokens": response.usage.total_tokens,
                "cost": self.calculate_cost(response.usage)
            }
        )

        return result

    @observe()
    def post_process(self, llm_output: str) -> Dict:
        """Post-process LLM output"""

        langfuse_context.update_current_observation(
            name="post-processing"
        )

        # Format output
        result = {
            "response": llm_output,
            "timestamp": datetime.now().isoformat(),
            "cost": 0.012  # Mock cost
        }

        return result

    def check_sla(self, duration: float, cost: float):
        """Check SLA compliance"""

        # Check latency
        if duration > self.alert_thresholds["latency_p95"]:
            self.send_alert(
                "sla_violation",
                f"Latency {duration:.2f}s exceeds threshold"
            )

        # Check cost
        if cost > self.alert_thresholds["cost_per_request"]:
            self.send_alert(
                "cost_alert",
                f"Cost ${cost:.4f} exceeds threshold"
            )

    def send_alert(self, alert_type: str, message: str):
        """Send alert (integrate with PagerDuty, Slack, etc.)"""

        # Log alert event
        langfuse_context.update_current_trace(
            tags=[f"alert-{alert_type}"],
            metadata={
                "alert_type": alert_type,
                "alert_message": message,
                "alert_timestamp": datetime.now().isoformat()
            }
        )

        # In production: send to alerting system
        print(f"🚨 ALERT [{alert_type}]: {message}")

    def calculate_cost(self, usage) -> float:
        """Calculate cost"""
        # GPT-4 Turbo pricing
        input_cost = usage.prompt_tokens * 0.00001
        output_cost = usage.completion_tokens * 0.00003
        return input_cost + output_cost

    def get_metrics_summary(self) -> Dict:
        """Get metrics summary from Langfuse"""

        # In production: Query Langfuse API
        # GET /api/public/metrics

        return {
            "requests_24h": 12_345,
            "error_rate": 0.028,  # 2.8%
            "p50_latency": 1.2,
            "p95_latency": 2.8,
            "p99_latency": 4.5,
            "total_cost_24h": 145.67,
            "avg_cost_per_request": 0.0118
        }

# Usage
if __name__ == "__main__":
    service = ProductionService()

    # Simulate production requests
    requests = [
        {
            "request_id": "req-001",
            "endpoint": "/api/chat",
            "client_version": "2.1.0",
            "query": "What is machine learning?"
        },
        {
            "request_id": "req-002",
            "endpoint": "/api/chat",
            "client_version": "2.1.0",
            "query": "Explain neural networks"
        }
    ]

    for i, req in enumerate(requests):
        print(f"\n--- Processing Request {i+1} ---")

        try:
            result = service.handle_request(
                request_data=req,
                user_id=f"user-{i}",
                session_id=f"session-{i//2}"
            )

            print(f"✅ Success: {result['response'][:100]}...")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    # Get metrics
    print("\n--- Production Metrics ---")
    metrics = service.get_metrics_summary()
    print(json.dumps(metrics, indent=2))

    # Flush all traces
    langfuse_context.flush()

# View in Langfuse Dashboard:
# - Real-time request monitoring
# - Latency distribution (p50, p95, p99)
# - Error rate trends
# - Cost analytics
# - SLA compliance tracking
# - Alert history
```

**Langfuse Production Dashboard:**
```
Production Monitoring Dashboard
Updated: 2026-01-18 14:23:45 UTC

Overview (Last 24h):
├── Requests: 12,345
├── Success Rate: 97.2%
├── Error Rate: 2.8%
└── Total Cost: $145.67

Performance:
├── p50 Latency: 1.2s ✅
├── p95 Latency: 2.8s ✅
├── p99 Latency: 4.5s ⚠️
└── Avg Cost/Request: $0.0118

Active Alerts:
├── 🚨 Latency spike at 12:30 (resolved)
└── 🚨 Error rate +5% at 14:00 (investigating)

Top Users by Cost:
├── user-enterprise-1: $23.45
├── user-enterprise-2: $18.90
└── user-premium-5: $12.34

Model Distribution:
├── gpt-4-turbo: 89% ($129.67)
└── gpt-3.5-turbo: 11% ($15.99)
```

### Example 9: Multi-Tenant SaaS Application

**Use Case**: Track usage and costs per tenant/organization

```python
import os
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from openai import OpenAI
from typing import Dict, Optional
from datetime import datetime

# Configure
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."

langfuse = Langfuse()
openai_client = OpenAI()

class MultiTenantService:
    """SaaS service with per-tenant tracking"""

    def __init__(self):
        self.langfuse = Langfuse()
        self.tenant_limits = {
            "free": {"daily_requests": 100, "cost_limit": 1.0},
            "pro": {"daily_requests": 1000, "cost_limit": 50.0},
            "enterprise": {"daily_requests": 10000, "cost_limit": 500.0}
        }

    @observe()
    def handle_tenant_request(
        self,
        tenant_id: str,
        tenant_tier: str,
        user_id: str,
        request_data: Dict
    ) -> Dict:
        """Handle request with tenant isolation"""

        # Set tenant context
        langfuse_context.update_current_trace(
            name="tenant-request",
            user_id=user_id,
            session_id=f"tenant-{tenant_id}",
            tags=["multi-tenant", tenant_tier],
            metadata={
                "tenant_id": tenant_id,
                "tenant_tier": tenant_tier,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            }
        )

        # Check tenant limits
        usage = self.get_tenant_usage(tenant_id)
        limits = self.tenant_limits[tenant_tier]

        if usage["daily_requests"] >= limits["daily_requests"]:
            return self.handle_limit_exceeded(
                "request_limit",
                usage,
                limits
            )

        if usage["daily_cost"] >= limits["cost_limit"]:
            return self.handle_limit_exceeded(
                "cost_limit",
                usage,
                limits
            )

        # Process request
        result = self.process_request(request_data)

        # Track usage
        langfuse_context.update_current_trace(
            metadata={
                "tenant_usage": {
                    "requests_used": usage["daily_requests"] + 1,
                    "requests_limit": limits["daily_requests"],
                    "cost_used": usage["daily_cost"] + result.get("cost", 0),
                    "cost_limit": limits["cost_limit"]
                }
            }
        )

        return result

    @observe()
    def process_request(self, data: Dict) -> Dict:
        """Process tenant request"""

        langfuse_context.update_current_observation(
            name="request-processing"
        )

        # Generate response
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "user", "content": data.get("query", "")}
            ]
        )

        result_text = response.choices[0].message.content
        cost = self.calculate_cost(response.usage)

        langfuse_context.update_current_observation(
            output={"response": result_text},
            metadata={
                "tokens": response.usage.total_tokens,
                "cost": cost
            }
        )

        return {
            "response": result_text,
            "cost": cost,
            "tokens": response.usage.total_tokens
        }

    def get_tenant_usage(self, tenant_id: str) -> Dict:
        """Get tenant usage for today"""

        # In production: Query Langfuse API
        # GET /api/public/metrics?filter[tenant_id]=xxx

        # Mock data
        return {
            "daily_requests": 45,
            "daily_cost": 2.34
        }

    def handle_limit_exceeded(
        self,
        limit_type: str,
        usage: Dict,
        limits: Dict
    ) -> Dict:
        """Handle limit exceeded"""

        langfuse_context.update_current_trace(
            tags=["limit-exceeded", limit_type],
            metadata={
                "limit_type": limit_type,
                "usage": usage,
                "limits": limits
            }
        )

        return {
            "error": f"{limit_type}_exceeded",
            "usage": usage,
            "limits": limits,
            "upgrade_url": "https://example.com/upgrade"
        }

    def calculate_cost(self, usage) -> float:
        """Calculate cost"""
        input_cost = usage.prompt_tokens * 0.00001
        output_cost = usage.completion_tokens * 0.00003
        return input_cost + output_cost

    def get_tenant_analytics(self, tenant_id: str) -> Dict:
        """Get analytics for tenant"""

        # Query Langfuse API for tenant metrics
        return {
            "tenant_id": tenant_id,
            "requests_30d": 1234,
            "cost_30d": 45.67,
            "users_active": 12,
            "avg_latency": 1.5,
            "error_rate": 0.02
        }

# Usage
if __name__ == "__main__":
    service = MultiTenantService()

    # Simulate requests from different tenants
    tenants = [
        {
            "tenant_id": "tenant-acme",
            "tenant_tier": "enterprise",
            "user_id": "user-1",
            "query": "Analyze this data..."
        },
        {
            "tenant_id": "tenant-startup",
            "tenant_tier": "pro",
            "user_id": "user-5",
            "query": "Generate report..."
        },
        {
            "tenant_id": "tenant-free",
            "tenant_tier": "free",
            "user_id": "user-10",
            "query": "Simple question..."
        }
    ]

    for tenant in tenants:
        print(f"\n--- Tenant: {tenant['tenant_id']} ({tenant['tenant_tier']}) ---")

        result = service.handle_tenant_request(
            tenant_id=tenant["tenant_id"],
            tenant_tier=tenant["tenant_tier"],
            user_id=tenant["user_id"],
            request_data={"query": tenant["query"]}
        )

        if "error" in result:
            print(f"❌ {result['error']}")
            print(f"   Usage: {result['usage']['daily_requests']} / {result['limits']['daily_requests']} requests")
        else:
            print(f"✅ Success")
            print(f"   Cost: ${result['cost']:.6f}")
            print(f"   Tokens: {result['tokens']}")

    # Get analytics for a tenant
    print("\n--- Tenant Analytics ---")
    analytics = service.get_tenant_analytics("tenant-acme")
    print(f"Tenant: {analytics['tenant_id']}")
    print(f"Requests (30d): {analytics['requests_30d']}")
    print(f"Cost (30d): ${analytics['cost_30d']:.2f}")
    print(f"Active Users: {analytics['users_active']}")

    # Flush traces
    langfuse_context.flush()

# View in Langfuse Dashboard:
# - Per-tenant cost breakdown
# - Usage vs limits
# - Tenant comparison
# - Upgrade opportunities
```

**Langfuse Multi-Tenant Dashboard:**
```
Tenant Analytics Dashboard

Tenant: tenant-acme (Enterprise)
├── Usage (30d): 1,234 / 10,000 requests (12%)
├── Cost (30d): $45.67 / $500.00 (9%)
├── Active Users: 12
├── Avg Latency: 1.5s
└── Error Rate: 2.0%

Top Tenants by Cost:
├── tenant-acme: $145.67 (Enterprise)
├── tenant-bigcorp: $123.45 (Enterprise)
└── tenant-startup: $12.34 (Pro)

Upgrade Opportunities:
├── tenant-free-xyz: 95/100 requests (suggest Pro)
└── tenant-pro-abc: $48/$50 cost (suggest Enterprise)

Churn Risk:
├── tenant-pro-def: Low usage (5/1000 requests)
└── tenant-enterprise-ghi: Errors 15% (investigate)
```

### Example 10: Dataset Creation from Production

**Use Case**: Build evaluation datasets from production traces

```python
import os
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from typing import List, Dict
from datetime import datetime, timedelta

# Configure
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."

langfuse = Langfuse()

class DatasetBuilder:
    """Build evaluation datasets from production data"""

    def __init__(self):
        self.langfuse = Langfuse()

    def create_dataset_from_feedback(
        self,
        dataset_name: str,
        min_score: float = 0.8,
        days_back: int = 30
    ) -> str:
        """Create dataset from high-quality production traces"""

        print(f"Creating dataset: {dataset_name}")
        print(f"Filtering: score >= {min_score}, last {days_back} days")

        # Create dataset in Langfuse
        dataset = self.langfuse.create_dataset(name=dataset_name)

        # In production: Query Langfuse API for traces
        # GET /api/public/traces?filter[score]>=0.8&filter[days]=30

        # Mock: Get high-quality traces
        traces = self.get_high_quality_traces(min_score, days_back)

        print(f"Found {len(traces)} high-quality traces")

        # Add to dataset
        for i, trace in enumerate(traces):
            self.langfuse.create_dataset_item(
                dataset_name=dataset_name,
                input=trace["input"],
                expected_output=trace["output"],
                metadata={
                    "source_trace_id": trace["trace_id"],
                    "user_feedback_score": trace["score"],
                    "original_timestamp": trace["timestamp"],
                    "model": trace["model"]
                }
            )

            if (i + 1) % 10 == 0:
                print(f"Added {i + 1} items...")

        print(f"✅ Dataset '{dataset_name}' created with {len(traces)} items")

        return dataset.id

    def get_high_quality_traces(
        self,
        min_score: float,
        days_back: int
    ) -> List[Dict]:
        """Get high-quality traces from Langfuse"""

        # In production: Use Langfuse API client
        # traces = langfuse.client.get_traces(
        #     filter={
        #         "score": {"gte": min_score},
        #         "timestamp": {"gte": days_back}
        #     }
        # )

        # Mock data
        return [
            {
                "trace_id": f"trace-{i}",
                "input": {"query": f"Question {i}"},
                "output": {"answer": f"Answer {i}"},
                "score": min_score + (0.2 * (i % 5) / 5),
                "timestamp": datetime.now().isoformat(),
                "model": "gpt-4-turbo-preview"
            }
            for i in range(50)
        ]

    def export_dataset_for_finetuning(
        self,
        dataset_name: str,
        output_format: str = "jsonl"
    ) -> str:
        """Export dataset for fine-tuning"""

        print(f"Exporting dataset: {dataset_name}")

        # Get dataset items
        dataset_items = self.get_dataset_items(dataset_name)

        if output_format == "jsonl":
            filename = f"{dataset_name}_{datetime.now().strftime('%Y%m%d')}.jsonl"

            with open(filename, "w") as f:
                for item in dataset_items:
                    import json
                    line = json.dumps({
                        "messages": [
                            {"role": "user", "content": item["input"]["query"]},
                            {"role": "assistant", "content": item["expected_output"]["answer"]}
                        ]
                    })
                    f.write(line + "\n")

            print(f"✅ Exported to {filename}")
            return filename

        else:
            raise ValueError(f"Unsupported format: {output_format}")

    def get_dataset_items(self, dataset_name: str) -> List[Dict]:
        """Get dataset items from Langfuse"""

        # In production: Use Langfuse API
        # items = langfuse.get_dataset(name=dataset_name).items

        # Mock data
        return [
            {
                "input": {"query": f"Question {i}"},
                "expected_output": {"answer": f"Answer {i}"}
            }
            for i in range(50)
        ]

    def create_test_dataset(
        self,
        dataset_name: str,
        sample_size: int = 100
    ) -> str:
        """Create balanced test dataset"""

        print(f"Creating test dataset: {dataset_name}")

        # Get diverse set of traces
        # - Different user types
        # - Different query types
        # - Range of scores (including failures)

        dataset = self.langfuse.create_dataset(name=dataset_name)

        # Mock: Create diverse samples
        categories = ["support", "sales", "technical", "billing"]

        items_per_category = sample_size // len(categories)

        for category in categories:
            for i in range(items_per_category):
                self.langfuse.create_dataset_item(
                    dataset_name=dataset_name,
                    input={
                        "query": f"{category} question {i}",
                        "category": category
                    },
                    expected_output={
                        "answer": f"{category} answer {i}"
                    },
                    metadata={
                        "category": category,
                        "difficulty": "easy" if i % 3 == 0 else "medium"
                    }
                )

        print(f"✅ Created test dataset with {sample_size} items")

        return dataset.id

    def evaluate_on_dataset(
        self,
        dataset_name: str,
        model: str = "gpt-4-turbo-preview"
    ):
        """Run evaluation on dataset"""

        print(f"Evaluating model {model} on dataset {dataset_name}")

        dataset_items = self.get_dataset_items(dataset_name)

        results = []

        for i, item in enumerate(dataset_items):
            # Create trace for evaluation
            with self.langfuse.trace(
                name="dataset-evaluation",
                metadata={
                    "dataset": dataset_name,
                    "model": model,
                    "item_index": i
                }
            ) as trace:
                # Generate response
                from openai import OpenAI
                client = OpenAI()

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": item["input"]["query"]}
                    ]
                )

                actual_output = response.choices[0].message.content
                expected_output = item["expected_output"]["answer"]

                # Score (simple exact match for demo)
                score = 1.0 if actual_output == expected_output else 0.0

                # Add score to trace
                self.langfuse.score(
                    trace_id=trace.id,
                    name="exact-match",
                    value=score
                )

                results.append({
                    "input": item["input"],
                    "expected": expected_output,
                    "actual": actual_output,
                    "score": score
                })

                if (i + 1) % 10 == 0:
                    print(f"Evaluated {i + 1}/{len(dataset_items)} items...")

        # Calculate overall metrics
        avg_score = sum(r["score"] for r in results) / len(results)

        print(f"\n✅ Evaluation complete")
        print(f"Average Score: {avg_score:.2%}")

        return results

# Usage
if __name__ == "__main__":
    builder = DatasetBuilder()

    # Create dataset from production feedback
    print("=== Creating Dataset from Production ===\n")
    dataset_id = builder.create_dataset_from_feedback(
        dataset_name="production-qa-v1",
        min_score=0.8,
        days_back=30
    )

    # Export for fine-tuning
    print("\n=== Exporting for Fine-Tuning ===\n")
    filename = builder.export_dataset_for_finetuning("production-qa-v1")

    # Create test dataset
    print("\n=== Creating Test Dataset ===\n")
    test_dataset_id = builder.create_test_dataset(
        dataset_name="test-suite-v1",
        sample_size=100
    )

    # Run evaluation
    print("\n=== Running Evaluation ===\n")
    results = builder.evaluate_on_dataset(
        dataset_name="test-suite-v1",
        model="gpt-4-turbo-preview"
    )

# View in Langfuse:
# - Dataset management interface
# - Evaluation results
# - Performance trends over time
# - Model comparison
```

**Langfuse Dataset View:**
```
Dataset: production-qa-v1
Items: 50
Created: 2026-01-18
Source: Production traces (score >= 0.8)

Sample Items:
├── Item 1: "How do I reset password?" → "You can reset..."
├── Item 2: "What is your refund policy?" → "Our refund..."
└── Item 3: "Shipping to Canada?" → "Yes, we ship..."

Evaluation Results:
Model: gpt-4-turbo-preview
├── Exact Match: 85%
├── Semantic Similarity: 92%
├── Avg Latency: 1.2s
└── Total Cost: $0.45

Export Options:
├── JSONL (for fine-tuning)
├── CSV (for spreadsheets)
└── API (programmatic access)
```

---

## 6. Advanced Usage

### 6.1 Custom Trace Sampling

```python
from langfuse import Langfuse
import random

class SamplingStrategy:
    """Custom sampling strategies"""

    @staticmethod
    def sample_by_user_tier(user_tier: str) -> bool:
        """Sample more from premium users"""
        rates = {
            "free": 0.1,      # 10% of requests
            "pro": 0.5,       # 50% of requests
            "enterprise": 1.0  # 100% of requests
        }
        return random.random() < rates.get(user_tier, 0.1)

    @staticmethod
    def sample_errors_only() -> bool:
        """Always trace errors, sample successes"""
        # Implement in error handler
        return True

    @staticmethod
    def adaptive_sampling(error_rate: float) -> float:
        """Increase sampling when error rate is high"""
        if error_rate > 0.1:  # 10% errors
            return 1.0  # Trace everything
        elif error_rate > 0.05:  # 5% errors
            return 0.5  # Trace 50%
        else:
            return 0.1  # Trace 10%
```

### 6.2 Custom Metrics and Aggregations

```python
from langfuse import Langfuse
from typing import List, Dict

class MetricsCollector:
    """Collect custom metrics"""

    def __init__(self):
        self.langfuse = Langfuse()

    def track_custom_metric(
        self,
        trace_id: str,
        metric_name: str,
        value: float,
        tags: List[str] = None
    ):
        """Track custom business metric"""

        self.langfuse.score(
            trace_id=trace_id,
            name=metric_name,
            value=value,
            metadata={"tags": tags or []}
        )

    def track_conversion(self, trace_id: str, converted: bool):
        """Track conversion events"""
        self.track_custom_metric(
            trace_id,
            "conversion",
            1.0 if converted else 0.0
        )

    def track_satisfaction(self, trace_id: str, nps_score: int):
        """Track NPS score"""
        self.track_custom_metric(
            trace_id,
            "nps-score",
            nps_score / 10.0  # Normalize to 0-1
        )
```

### 6.3 Integration with OpenTelemetry

```python
from langfuse import Langfuse
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure OpenTelemetry
tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)

# Add Langfuse as OTEL exporter (if supported)
# This allows sending traces to both OTEL and Langfuse
```

---

## 7. Best Practices

### 7.1 Trace Organization

```python
# DO: Use hierarchical traces
@observe()
def parent_function():
    child_1()
    child_2()

# DO: Add meaningful metadata
langfuse_context.update_current_trace(
    metadata={
        "feature": "chat",
        "version": "2.0",
        "environment": "production"
    }
)

# DON'T: Create flat traces without context
# DON'T: Trace every tiny function (adds noise)
```

### 7.2 Cost Management

```python
# DO: Set up budget alerts in Langfuse UI
# DO: Use caching for repeated queries
# DO: Monitor cost per user/feature

# DON'T: Trace in infinite loops
# DON'T: Send PII in trace data
# DON'T: Ignore cost trends
```

### 7.3 Performance

```python
# DO: Use async SDK for high-throughput
# DO: Batch trace uploads (flush_at parameter)
# DO: Sample traces in high-volume scenarios

# DON'T: Flush after every trace (too slow)
# DON'T: Send large payloads in traces
```

---

## 8. Integration Guide

### 8.1 Frameworks

**LangChain:**
```python
from langfuse.callback import CallbackHandler

handler = CallbackHandler()
chain.invoke(input, config={"callbacks": [handler]})
```

**LlamaIndex:**
```python
from llama_index.callbacks import CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler

callback_handler = LlamaIndexCallbackHandler()
callback_manager = CallbackManager([callback_handler])
```

**Anthropic:**
```python
from langfuse.anthropic import AnthropicLangfuse

client = AnthropicLangfuse()
# Automatically tracks all Claude API calls
```

### 8.2 Deployment

**Docker:**
```dockerfile
FROM python:3.11-slim

ENV LANGFUSE_HOST=https://cloud.langfuse.com
ENV LANGFUSE_PUBLIC_KEY=pk-lf-...
ENV LANGFUSE_SECRET_KEY=sk-lf-...

RUN pip install langfuse

COPY . /app
WORKDIR /app

CMD ["python", "main.py"]
```

**Kubernetes:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: langfuse-credentials
type: Opaque
stringData:
  public-key: pk-lf-...
  secret-key: sk-lf-...
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-llm-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: my-app:latest
        env:
        - name: LANGFUSE_PUBLIC_KEY
          valueFrom:
            secretKeyRef:
              name: langfuse-credentials
              key: public-key
        - name: LANGFUSE_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: langfuse-credentials
              key: secret-key
```

---

## 9. Troubleshooting

### 9.1 Common Issues

**Traces not appearing:**
```python
# Ensure you flush before exit
langfuse_context.flush()

# Check credentials
print(langfuse.auth_check())

# Enable debug logging
langfuse = Langfuse(debug=True)
```

**High latency:**
```python
# Increase batch size
langfuse = Langfuse(flush_at=50)

# Reduce flush frequency
langfuse = Langfuse(flush_interval=2.0)
```

**Cost discrepancies:**
```python
# Verify model names match Langfuse pricing database
# Check for streaming token counting issues
# Review usage metadata in generations
```

---

## 10. API Reference

### 10.1 Core Classes

**Langfuse Client:**
```python
class Langfuse:
    def __init__(
        self,
        public_key: str = None,
        secret_key: str = None,
        host: str = None,
        debug: bool = False,
        enabled: bool = True,
        flush_at: int = 15,
        flush_interval: float = 0.5
    ): ...

    def trace(self, **kwargs) -> TraceHandle: ...
    def score(self, **kwargs): ...
    def create_dataset(self, **kwargs) -> Dataset: ...
    def flush(self): ...
    def auth_check(self) -> bool: ...
```

**Decorators:**
```python
@observe(
    name: str = None,
    as_type: Literal["trace", "span", "generation"] = None,
    capture_input: bool = True,
    capture_output: bool = True
)
```

---

## 11. Performance & Optimization

### 11.1 Throughput

- Async SDK: Up to 10,000 traces/second
- Batch uploads reduce overhead
- Minimal performance impact (<5ms)

### 11.2 Storage

- Cloud: Unlimited with retention policies
- Self-hosted: PostgreSQL scales to billions of traces

---

## 12. Security Considerations

### 12.1 Data Privacy

```python
# Sanitize PII before tracing
def sanitize_input(text: str) -> str:
    # Remove emails, phone numbers, etc.
    return redacted_text

@observe()
def secure_function(user_input: str):
    langfuse_context.update_current_observation(
        input={"sanitized": sanitize_input(user_input)}
    )
```

### 12.2 Access Control

- API keys per project
- Role-based access in UI
- SSO for enterprise
- Audit logs for compliance

---

## 13. References & Resources

### 13.1 Official Links

- Website: https://langfuse.com
- Documentation: https://langfuse.com/docs
- GitHub: https://github.com/langfuse/langfuse
- Cloud Platform: https://cloud.langfuse.com
- Discord Community: https://discord.gg/langfuse

### 13.2 Pricing

**Cloud:**
- Free: 50k observations/month
- Hobby: $10/month (500k observations)
- Pro: $99/month (5M observations)
- Enterprise: Custom pricing

**Self-Hosted:**
- Free and open source
- Enterprise support available

### 13.3 Comparison

**vs LangSmith:**
- Langfuse: Open source, self-hostable
- LangSmith: Closed source, cloud only
- Both: Excellent for production

**vs Phoenix:**
- Langfuse: Production-focused, cost tracking
- Phoenix: Development-focused, ML observability
- Use both: Phoenix for dev, Langfuse for prod

**vs Weights & Biases:**
- Langfuse: LLM-specific features
- W&B: ML experimentation platform
- Use both: W&B for training, Langfuse for inference

---

## Conclusion

Langfuse is the production observability platform of choice for LLM applications. Its combination of comprehensive tracing, cost tracking, prompt management, and user feedback makes it ideal for teams running LLM applications at scale. The open-source self-hosted option provides flexibility, while the cloud offering ensures zero-maintenance operations.

**Key Strengths:**
- Production-grade observability
- Best-in-class cost tracking
- Prompt version management
- Self-hosted option
- Active development

**Best For:**
- Production LLM applications
- Cost-conscious teams
- Multi-model deployments
- SaaS platforms
- Enterprise requirements

Start with the cloud version for quick setup, then migrate to self-hosted for greater control and data privacy.
