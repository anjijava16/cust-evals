# LangSmith: The Complete Deep-Dive Guide

**Version**: 1.0.0 | **Updated**: January 2026 | **License**: Commercial (Freemium)

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

### 1.1 What is LangSmith?

LangSmith is LangChain's production-grade platform for building, testing, evaluating, and monitoring LLM applications. Developed by the creators of LangChain and LangGraph, it provides best-in-class integration with the LangChain ecosystem while supporting other frameworks through OpenTelemetry. LangSmith serves as the unified platform for the entire LLM application lifecycle—from prototype to production.

**Core Philosophy:**
- **End-to-End Coverage**: From development to production monitoring
- **LangChain Native**: Seamless integration with LangChain and LangGraph
- **Production Ready**: Enterprise-grade reliability and compliance
- **Developer First**: Intuitive UX with powerful capabilities

### 1.2 Key Features

#### Comprehensive Observability
- **Distributed Tracing**: Complete request visualization across all components
- **Real-Time Monitoring**: Live dashboard with metrics and alerts
- **Cost Tracking**: Token-level cost analysis by model, user, and feature
- **Error Tracking**: Automatic error detection with stack traces
- **Performance Metrics**: Latency breakdown and throughput analysis

#### Advanced Evaluation
- **Dataset Management**: Version-controlled test sets with cloud storage
- **LLM-as-Judge**: Automated evaluation with configurable models
- **Code-Based Evaluators**: Custom Python/TypeScript evaluation logic
- **Pairwise Comparison**: Side-by-side model and prompt comparison
- **Statistical Testing**: Confidence intervals and significance tests
- **Regression Detection**: Automated alerts for quality degradation

#### Prompt Engineering
- **Visual Playground**: Interactive prompt testing environment
- **Version Control**: Git-like versioning for prompts
- **Template Variables**: Dynamic prompts with Jinja2/Mustache
- **Multi-Model Testing**: Compare GPT-4, Claude, Gemini simultaneously
- **Commit Messages**: Track why changes were made

#### Human-in-the-Loop
- **Annotation Queues**: Organized workflow for manual review
- **Custom Rubrics**: Define scoring criteria for evaluators
- **Team Collaboration**: Multi-user annotation with conflict resolution
- **Feedback Collection**: Production user feedback integration
- **Inter-Annotator Agreement**: Track consistency across reviewers

#### Production Deployment
- **Agent Servers**: Deploy LangGraph agents at scale
- **Streaming Support**: Real-time response streaming
- **Double-Texting**: Handle concurrent user inputs
- **Custom Auth**: Integrate with existing auth systems
- **Load Balancing**: Automatic scaling and distribution

#### Enterprise Features
- **Compliance**: SOC 2 Type 2, HIPAA, GDPR certified
- **SSO Integration**: SAML and OAuth support
- **RBAC**: Fine-grained role-based permissions
- **Audit Logs**: Complete activity tracking
- **Self-Hosting**: Full platform deployment on your infrastructure

### 1.3 When to Use LangSmith

**Perfect For:**
- Teams using LangChain or LangGraph as primary framework
- Production applications requiring comprehensive observability
- Organizations needing enterprise compliance (HIPAA, SOC 2)
- Teams wanting managed evaluation datasets and versioning
- Companies requiring human-in-the-loop evaluation workflows
- Projects needing prompt version control and A/B testing
- Enterprises requiring SSO and advanced access control
- Applications needing statistical experiment comparison

**Not Ideal For:**
- Budget-constrained projects (free tier limited to 5K traces)
- Teams not using LangChain (better framework-specific options exist)
- Simple evaluation needs (lightweight libraries sufficient)
- Projects requiring fully open-source solutions
- Applications needing complete data sovereignty without Enterprise tier

### 1.4 Comparison Matrix

| Feature | LangSmith | Langfuse | Phoenix | Opik | Braintrust |
|---------|-----------|----------|---------|------|------------|
| **LangChain Integration** | ✅✅ Native | ✅ Good | ✅ Good | ✅ Good | ✅ Good |
| **Self-Hosting** | ⚠️ Enterprise | ✅ Open | ✅ Open | ✅ Open | ⚠️ Enterprise |
| **Dataset Management** | ✅✅ Excellent | ✅ Good | ⚠️ Basic | ✅ Good | ✅ Good |
| **Human Annotation** | ✅✅ Built-in | ✅ Good | ⚠️ Limited | ✅ Good | ✅ Good |
| **Statistical Testing** | ✅ Built-in | ❌ No | ❌ No | ⚠️ Basic | ✅ Yes |
| **Prompt Playground** | ✅✅ Excellent | ✅ Good | ❌ No | ✅ Good | ✅ Good |
| **Agent Deployment** | ✅ Native | ❌ No | ❌ No | ❌ No | ❌ No |
| **Free Tier** | 5K traces | Unlimited | Unlimited | Unlimited | Usage-based |
| **Cost** | $39/user/mo | $59 flat | Free | Free | Freemium |
| **Compliance** | SOC2, HIPAA | SOC2, GDPR | None | None | SOC2 |

---

## 2. Complete Architecture

### 2.1 System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                      Your Application                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  LangChain   │  │  LangGraph   │  │   Custom     │         │
│  │  Application │  │    Agent     │  │   Services   │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                 │
│                            │                                    │
│                   LangSmith SDK                                 │
│              (@traceable, callbacks)                            │
└────────────────────────────┬───────────────────────────────────┘
                             │ HTTPS/gRPC
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                    LangSmith Platform                          │
│                    (Cloud or Self-Hosted)                      │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │               API Gateway & Auth Layer                   │  │
│  │  • Authentication (API keys, SSO)                        │  │
│  │  • Rate limiting                                         │  │
│  │  • Request routing                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│  ┌──────────────────────────┴──────────────────────────────┐  │
│  │                  Core Services                           │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │  │
│  │  │  Tracing    │  │ Evaluation  │  │  Datasets   │     │  │
│  │  │  Service    │  │   Engine    │  │   Manager   │     │  │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │  │
│  │         │                 │                 │            │  │
│  │  ┌──────┴──────┬─────────┴─────────┬───────┴──────┐     │  │
│  │  │  Prompt     │   Annotation      │  Deployment  │     │  │
│  │  │  Manager    │     Queue         │   Service    │     │  │
│  │  └─────────────┴───────────────────┴──────────────┘     │  │
│  └──────────────────────────┬──────────────────────────────┘  │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Data Layer                            │  │
│  │  • PostgreSQL (metadata, config)                        │  │
│  │  • ClickHouse (traces, events, analytics)               │  │
│  │  • Redis (caching, queues)                              │  │
│  │  • S3/Object Storage (artifacts, datasets)              │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬───────────────────────────────────┘
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                       Frontend UI                              │
│  • Trace Explorer (search, filter, drill-down)                │
│  • Evaluation Dashboard (metrics, comparisons)                │
│  • Prompt Playground (test, version, deploy)                  │
│  • Annotation Interface (manual review)                       │
│  • Dataset Manager (import, export, version)                  │
│  • Analytics & Reports (cost, usage, performance)            │
└────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Model

**Hierarchical Structure:**

```python
Project
├── Traces (Complete execution paths)
│   ├── Trace ID (UUID)
│   ├── Name
│   ├── Input/Output
│   ├── Metadata (tags, user_id, etc.)
│   ├── Start/End Time
│   ├── Runs (Execution steps)
│   │   ├── Run ID
│   │   ├── Run Type (llm, chain, tool, retriever)
│   │   ├── Parent Run ID
│   │   ├── Input/Output
│   │   ├── Tokens (prompt_tokens, completion_tokens)
│   │   ├── Cost
│   │   ├── Latency
│   │   ├── Error (if any)
│   │   └── Feedback (scores, comments)
│   └── Feedback
│       ├── Feedback ID
│       ├── Key (e.g., "quality", "relevance")
│       ├── Score (numeric or boolean)
│       └── Comment (optional text)
├── Datasets (Test collections)
│   ├── Dataset ID
│   ├── Name & Description
│   ├── Version
│   ├── Examples
│   │   ├── Example ID
│   │   ├── Inputs (dict)
│   │   ├── Outputs (dict, optional)
│   │   └── Metadata
│   └── Splits (train, test, val)
├── Experiments (Evaluation runs)
│   ├── Experiment ID
│   ├── Dataset Reference
│   ├── Evaluators Used
│   ├── Results
│   │   ├── Per-example scores
│   │   ├── Aggregate metrics
│   │   └── Statistical analysis
│   └── Comparison Data
└── Prompts (Version-controlled templates)
    ├── Prompt ID
    ├── Name & Description
    ├── Versions
    │   ├── Version Number
    │   ├── Template String
    │   ├── Model Config
    │   ├── Commit Message
    │   └── Created At
    └── Deployments
        ├── Environment (dev, staging, prod)
        └── Active Version
```

### 2.3 Component Breakdown

**SDK Components:**
- **Client**: Main interface for API interaction
- **Traceable Decorator**: Auto-instrumentation for Python functions
- **Callback Handlers**: LangChain integration points
- **OpenTelemetry Bridge**: Framework-agnostic tracing
- **Async Support**: Non-blocking trace submission
- **Batching**: Efficient network utilization

**Platform Services:**
- **Ingestion API**: High-throughput trace ingestion
- **Query Engine**: Fast trace search and filtering
- **Evaluation Engine**: Parallel metric computation
- **Annotation Service**: Human review workflows
- **Prompt Registry**: Version control and deployment
- **Analytics Engine**: Aggregation and reporting

### 2.4 Data Flow Architecture

#### Tracing Flow

```
Application Execution
        ↓
┌───────────────────────────────────────────────────────────────┐
│  1. TRACE CAPTURE                                             │
│     • @traceable decorator intercepts function calls          │
│     • LangChain callbacks auto-capture chain execution        │
│     • OpenTelemetry spans for custom instrumentation          │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  2. LOCAL PROCESSING                                          │
│     • Build trace tree (parent-child relationships)           │
│     • Capture inputs, outputs, metadata                       │
│     • Calculate latency and token counts                      │
│     • Add tags and custom metadata                            │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  3. BATCHING & SERIALIZATION                                  │
│     • Queue traces in memory buffer                           │
│     • Batch multiple traces for efficiency                    │
│     • Serialize to JSON format                                │
│     • Compress payloads                                       │
└───────────────────────┬───────────────────────────────────────┘
                        │ HTTPS POST
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  4. API INGESTION                                             │
│     • Authenticate request (API key)                          │
│     • Validate payload format                                 │
│     • Route to ingestion service                              │
│     • Return acknowledgment                                   │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  5. DATA STORAGE                                              │
│     • Write to ClickHouse (traces, runs, events)              │
│     • Store metadata in PostgreSQL                            │
│     • Cache recent traces in Redis                            │
│     • Save artifacts to S3 (large payloads)                   │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  6. INDEXING & AGGREGATION                                    │
│     • Build search indices                                    │
│     • Compute aggregate metrics                               │
│     • Generate cost summaries                                 │
│     • Trigger alerts if configured                            │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  7. UI VISUALIZATION                                          │
│     • Display in Trace Explorer                               │
│     • Update dashboards                                       │
│     • Show in analytics views                                 │
│     • Available for querying                                  │
└───────────────────────────────────────────────────────────────┘
```

#### Evaluation Flow

```
Dataset Preparation
        ↓
┌───────────────────────────────────────────────────────────────┐
│  1. EXPERIMENT SETUP                                          │
│     • Select dataset                                          │
│     • Choose evaluators (LLM-as-judge, code-based)            │
│     • Configure evaluation parameters                         │
│     • Define comparison baseline (optional)                   │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  2. PARALLEL EXECUTION                                        │
│     • Load dataset examples                                   │
│     • Run target system on each example                       │
│     • Execute in parallel with concurrency control            │
│     • Capture outputs and intermediate traces                 │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  3. EVALUATOR EXECUTION                                       │
│     │                                                         │
│     ├─► LLM-as-Judge Evaluators                              │
│     │   • Format evaluation prompts                           │
│     │   • Call LLM API (GPT-4, Claude, etc.)                  │
│     │   • Parse scores from responses                         │
│     │                                                         │
│     ├─► Code-Based Evaluators                                 │
│     │   • Execute Python/TypeScript functions                 │
│     │   • Compare against ground truth                        │
│     │   • Calculate metrics (accuracy, BLEU, etc.)            │
│     │                                                         │
│     └─► Custom Evaluators                                     │
│         • User-defined evaluation logic                       │
│         • External API calls if needed                        │
│         • Arbitrary scoring functions                         │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  4. SCORE AGGREGATION                                         │
│     • Collect scores from all evaluators                      │
│     • Calculate aggregate statistics                          │
│     • Compute confidence intervals                            │
│     • Run statistical significance tests                      │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  5. RESULTS STORAGE                                           │
│     • Save experiment results                                 │
│     • Link to individual traces                               │
│     • Store comparison data                                   │
│     • Generate summary reports                                │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  6. VISUALIZATION & ANALYSIS                                  │
│     • Display in Experiments dashboard                        │
│     • Show per-example breakdowns                             │
│     • Compare against baselines                               │
│     • Export results (CSV, JSON)                              │
└───────────────────────────────────────────────────────────────┘
```

#### Feedback Loop Flow

```
Production Traces
        ↓
┌───────────────────────────────────────────────────────────────┐
│  1. CAPTURE PRODUCTION DATA                                   │
│     • Real user interactions traced                           │
│     • All inputs/outputs recorded                             │
│     • Metadata includes user_id, session_id                   │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  2. FEEDBACK COLLECTION                                       │
│     │                                                         │
│     ├─► Implicit Feedback                                     │
│     │   • Thumbs up/down from users                           │
│     │   • Star ratings                                        │
│     │   • Usage patterns                                      │
│     │                                                         │
│     └─► Explicit Feedback                                     │
│         • Human annotations                                   │
│         • Expert reviews                                      │
│         • Quality scores                                      │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  3. ANNOTATION QUEUE                                          │
│     • Queue high-value traces for review                      │
│     • Assign to team members                                  │
│     • Apply custom rubrics                                    │
│     • Track inter-annotator agreement                         │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  4. DATASET ENRICHMENT                                        │
│     • Add annotated traces to datasets                        │
│     • Create train/test splits                                │
│     • Version datasets                                        │
│     • Label edge cases                                        │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  5. ITERATIVE IMPROVEMENT                                     │
│     • Run experiments on enriched datasets                    │
│     • Identify failure patterns                               │
│     • Test prompt improvements                                │
│     • Validate changes before deployment                      │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  6. DEPLOYMENT & MONITORING                                   │
│     • Deploy improved version                                 │
│     • Monitor performance metrics                             │
│     • A/B test against baseline                               │
│     • Continuous evaluation                                   │
└───────────────────────────────────────────────────────────────┘
```

### 2.5 LLM Provider Architecture

LangSmith supports multiple LLM providers through a unified interface:

```
┌────────────────────────────────────────────────────────────────┐
│                    LangSmith Platform                          │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              LLM Abstraction Layer                       │ │
│  │  • Unified interface for all providers                   │ │
│  │  • Automatic retry and error handling                    │ │
│  │  • Rate limit management                                 │ │
│  │  • Cost tracking per provider                            │ │
│  └──────────────────────┬───────────────────────────────────┘ │
│                         │                                      │
│         ┌───────────────┼───────────────┬─────────────────┐   │
│         │               │               │                 │   │
│         ▼               ▼               ▼                 ▼   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐│
│  │  OpenAI  │    │ Anthropic│    │  Google  │    │  Custom  ││
│  │   GPT-4  │    │  Claude  │    │  Gemini  │    │  Models  ││
│  │ GPT-3.5  │    │  Opus    │    │   PaLM   │    │  (Local) ││
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘│
└────────────────────────────────────────────────────────────────┘
```

**Key Features:**
- **Provider-Agnostic**: Switch models without code changes
- **Automatic Tracking**: All calls automatically traced
- **Cost Attribution**: Track costs by model, user, feature
- **Retry Logic**: Built-in exponential backoff
- **Fallback Support**: Automatic failover to backup models

---

## 3. Installation & Setup

### 3.1 Cloud Setup (5 Minutes)

**Step 1: Create Account**
```bash
# Visit https://smith.langchain.com
# Sign up with email (no credit card required)
# Free tier: 5,000 traces/month
```

**Step 2: Get API Key**
```bash
# Navigate to Settings → API Keys
# Click "Create API Key"
# Copy the key (starts with "lsv2_...")
```

**Step 3: Install SDK**

**Python:**
```bash
pip install langsmith langchain langchain-openai
```

**TypeScript:**
```bash
npm install langsmith langchain @langchain/openai
```

**Step 4: Configure Environment**

```bash
# Add to .env or export
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY="lsv2_pt_..."
export LANGCHAIN_PROJECT="my-project"  # Optional, defaults to "default"

# For production
export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
```

**Step 5: Verify Setup**

**Python:**
```python
from langsmith import Client

# Test connection
client = Client()
print(f"✓ Connected to LangSmith")
print(f"Projects: {[p.name for p in client.list_projects()]}")
```

**TypeScript:**
```typescript
import { Client } from "langsmith";

const client = new Client();
console.log("✓ Connected to LangSmith");
```

### 3.2 Self-Hosted Setup (Enterprise)

**Prerequisites:**
- Kubernetes cluster (or Docker Compose for dev)
- PostgreSQL 13+
- Redis
- Object storage (S3-compatible)
- TLS certificates

**Docker Compose (Development):**

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: langsmith
      POSTGRES_PASSWORD: changeme
      POSTGRES_DB: langsmith
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  langsmith-backend:
    image: langchain/langsmith-backend:latest
    environment:
      DATABASE_URL: postgresql://langsmith:changeme@postgres:5432/langsmith
      REDIS_URL: redis://redis:6379
      API_KEY_SALT: your-secret-salt
      JWT_SECRET: your-jwt-secret
      S3_ENDPOINT: http://minio:9000
      S3_ACCESS_KEY: minioadmin
      S3_SECRET_KEY: minioadmin
    ports:
      - "1984:1984"
    depends_on:
      - postgres
      - redis

  langsmith-frontend:
    image: langchain/langsmith-frontend:latest
    environment:
      BACKEND_URL: http://langsmith-backend:1984
    ports:
      - "3000:80"
    depends_on:
      - langsmith-backend

  minio:
    image: minio/minio:latest
    command: server /data
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  redis_data:
  minio_data:
```

**Start Services:**
```bash
docker-compose up -d

# Create admin user
docker-compose exec langsmith-backend python manage.py create_admin \
  --email admin@company.com \
  --password secure-password

# Access UI at http://localhost:3000
```

**Kubernetes Deployment:**

```yaml
# values.yaml for Helm chart
replicaCount: 3

database:
  host: postgres.database.svc.cluster.local
  port: 5432
  name: langsmith
  existingSecret: langsmith-db-secret

redis:
  host: redis.cache.svc.cluster.local
  port: 6379

storage:
  type: s3
  bucket: langsmith-artifacts
  region: us-east-1
  existingSecret: langsmith-s3-secret

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: langsmith.company.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: langsmith-tls
      hosts:
        - langsmith.company.com

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

resources:
  limits:
    cpu: 2000m
    memory: 4Gi
  requests:
    cpu: 1000m
    memory: 2Gi
```

**Deploy:**
```bash
# Add Helm repo (Enterprise customers only)
helm repo add langchain https://langchain-ai.github.io/helm-charts
helm repo update

# Install
helm install langsmith langchain/langsmith \
  -f values.yaml \
  --namespace langsmith \
  --create-namespace

# Configure SDK to use self-hosted
export LANGCHAIN_ENDPOINT="https://langsmith.company.com"
export LANGCHAIN_API_KEY="your-api-key"
```

### 3.3 Framework-Specific Setup

**LangChain (Python):**
```python
# Automatic tracing - no code changes needed!
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "lsv2_..."

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence

# All of this is automatically traced
llm = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm

result = chain.invoke({"topic": "programming"})
# View trace at https://smith.langchain.com
```

**LangGraph (Python):**
```python
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

# Automatic tracing for agents
graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))
# ... build graph

app = graph.compile()

# All executions automatically traced
result = app.invoke({"messages": [HumanMessage(content="Help me")]})
```

**Non-LangChain Frameworks:**
```python
from langsmith import traceable
from openai import OpenAI

client = OpenAI()

@traceable(
    name="my-llm-call",
    run_type="llm",
    project_name="my-project"
)
def call_openai(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Usage automatically traced
result = call_openai("Hello!")
```

---

## 4. Core Concepts

### 4.1 Traces

**Definition:** A trace represents the complete execution path of your application from start to finish, capturing all operations and their relationships.

**Key Properties:**
- **Trace ID**: Unique identifier (UUID)
- **Project**: Organization/categorization
- **Name**: Human-readable identifier
- **Input/Output**: Request and response data
- **Metadata**: Custom tags (user_id, session, etc.)
- **Start/End Time**: Execution timeline
- **Runs**: Child operations (see below)

**Creating Traces:**

```python
from langsmith import Client

client = Client()

# Method 1: Auto-tracing (LangChain)
# Just set environment variables - traces created automatically

# Method 2: Manual tracing (non-LangChain)
from langsmith import traceable

@traceable(name="my-function", project_name="my-project")
def my_function(input_data: dict):
    # Your logic here
    result = process(input_data)
    return result

# Method 3: Context manager
from langsmith.run_trees import RunTree

root = RunTree(
    name="my-trace",
    run_type="chain",
    inputs={"query": "What is AI?"},
    project_name="my-project"
)

# ... do work ...

root.end(outputs={"answer": "AI is..."})
root.post()
```

### 4.2 Runs

**Definition:** Runs represent individual operations within a trace, such as LLM calls, tool invocations, or component executions.

**Run Types:**
- **llm**: Language model calls
- **chain**: Sequence of operations
- **tool**: External tool/API calls
- **retriever**: Document retrieval operations
- **embedding**: Embedding generation
- **prompt**: Prompt formatting
- **parser**: Output parsing

**Run Hierarchy:**

```python
Trace: User Query Processing
├── Run: Input Validation (chain)
├── Run: Context Retrieval (retriever)
│   └── Run: Embedding Query (embedding)
├── Run: Generate Response (llm)
│   ├── Prompt tokens: 250
│   ├── Completion tokens: 150
│   ├── Cost: $0.0012
│   └── Latency: 1.2s
└── Run: Format Output (parser)
```

**Manual Run Creation:**

```python
from langsmith import traceable

@traceable(run_type="retriever")
def retrieve_context(query: str) -> list[str]:
    """Retrieve relevant documents."""
    results = vector_db.search(query, k=5)
    return results

@traceable(run_type="llm")
def generate_answer(query: str, context: list[str]) -> str:
    """Generate answer using LLM."""
    response = llm.invoke(f"Context: {context}\nQuery: {query}")
    return response

@traceable(run_type="chain", name="rag-pipeline")
def rag_pipeline(query: str) -> str:
    """Complete RAG pipeline."""
    # Each function call creates a nested run
    context = retrieve_context(query)
    answer = generate_answer(query, context)
    return answer
```

### 4.3 Datasets

**Definition:** Collections of test cases with inputs and optionally expected outputs, used for systematic evaluation.

**Dataset Structure:**

```python
{
    "name": "customer-support-qa",
    "description": "Customer support Q&A pairs",
    "examples": [
        {
            "id": "uuid-1",
            "inputs": {"question": "How do I reset my password?"},
            "outputs": {"answer": "Click 'Forgot Password'..."},
            "metadata": {"category": "auth", "difficulty": "easy"}
        },
        {
            "id": "uuid-2",
            "inputs": {"question": "What are your refund policies?"},
            "outputs": {"answer": "We offer 30-day refunds..."},
            "metadata": {"category": "billing", "difficulty": "medium"}
        }
    ]
}
```

**Creating Datasets:**

```python
from langsmith import Client

client = Client()

# Method 1: Create from list
dataset = client.create_dataset(
    dataset_name="qa-dataset",
    description="Q&A evaluation set"
)

examples = [
    {
        "inputs": {"question": "What is Python?"},
        "outputs": {"answer": "Python is a programming language..."}
    },
    {
        "inputs": {"question": "What is machine learning?"},
        "outputs": {"answer": "ML is a subset of AI..."}
    }
]

for example in examples:
    client.create_example(
        dataset_id=dataset.id,
        inputs=example["inputs"],
        outputs=example["outputs"]
    )

# Method 2: Upload from CSV
import pandas as pd

df = pd.DataFrame({
    "question": ["Q1", "Q2", "Q3"],
    "answer": ["A1", "A2", "A3"]
})

dataset = client.upload_dataframe(
    df=df,
    name="csv-dataset",
    input_keys=["question"],
    output_keys=["answer"]
)

# Method 3: Create from production traces
# Filter traces in UI, then click "Add to Dataset"
```

**Versioning Datasets:**

```python
# Clone dataset for new version
dataset_v2 = client.clone_dataset(
    source_dataset_id=dataset.id,
    target_dataset_name="qa-dataset-v2"
)

# Update examples
client.update_example(
    example_id="uuid-1",
    inputs={"question": "Updated question"},
    outputs={"answer": "Updated answer"}
)
```

### 4.4 Experiments

**Definition:** Evaluation runs that systematically test your application against a dataset, computing metrics and enabling comparison.

**Experiment Components:**
- **Dataset**: Test cases to evaluate
- **Target Function**: System under test
- **Evaluators**: Metrics to compute
- **Results**: Per-example and aggregate scores

**Running Experiments:**

```python
from langsmith import Client, evaluate
from langsmith.evaluation import EvaluationResult
from langsmith.schemas import Run, Example

client = Client()

# Define your system
def qa_system(inputs: dict) -> dict:
    question = inputs["question"]
    answer = my_llm_call(question)
    return {"answer": answer}

# Define evaluators
def correctness_evaluator(run: Run, example: Example) -> EvaluationResult:
    predicted = run.outputs.get("answer", "")
    expected = example.outputs.get("answer", "")

    # Simple exact match
    score = 1.0 if predicted.lower() == expected.lower() else 0.0

    return EvaluationResult(
        key="correctness",
        score=score
    )

def relevance_evaluator(run: Run, example: Example) -> EvaluationResult:
    # LLM-as-judge
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o")
    prompt = f"""Rate the relevance of this answer (0-1):
    Question: {example.inputs['question']}
    Answer: {run.outputs['answer']}
    """

    score = float(llm.invoke(prompt).content.strip())

    return EvaluationResult(
        key="relevance",
        score=score
    )

# Run experiment
results = evaluate(
    qa_system,
    data="qa-dataset",
    evaluators=[correctness_evaluator, relevance_evaluator],
    experiment_prefix="qa-eval-v1",
    description="Baseline evaluation",
    metadata={"model": "gpt-4o", "temperature": 0.7}
)

# View results
print(f"Correctness: {results['correctness'].mean():.2f}")
print(f"Relevance: {results['relevance'].mean():.2f}")
```

### 4.5 Feedback

**Definition:** Ratings, scores, or comments attached to runs, used for evaluation, monitoring, and human review.

**Feedback Types:**
- **Numeric**: 0-1 scores (e.g., 0.85)
- **Binary**: Thumbs up/down (1 or 0)
- **Categorical**: Labels (e.g., "good", "bad", "excellent")
- **Textual**: Comments and explanations

**Adding Feedback:**

```python
from langsmith import Client

client = Client()

# Method 1: Programmatic feedback
client.create_feedback(
    run_id="run-uuid",
    key="quality",
    score=0.9,
    comment="Excellent response"
)

# Method 2: User feedback from production
def handle_user_rating(run_id: str, thumbs_up: bool):
    client.create_feedback(
        run_id=run_id,
        key="user_rating",
        score=1.0 if thumbs_up else 0.0
    )

# Method 3: Automated feedback (from evaluators)
# Evaluators automatically create feedback during evaluate()

# Query feedback
feedbacks = client.list_feedback(run_ids=["run-uuid"])
for fb in feedbacks:
    print(f"{fb.key}: {fb.score}")
```

### 4.6 Prompts

**Definition:** Version-controlled prompt templates with configuration, enabling rollback, A/B testing, and collaboration.

**Prompt Components:**
- **Template**: String with variables (e.g., "Answer: {question}")
- **Model Config**: Model name, temperature, etc.
- **Version**: Auto-incremented version number
- **Commit Message**: Why this change was made
- **Deployments**: Which version is active in each environment

**Using Prompts:**

```python
from langsmith import Client

client = Client()

# Create prompt
client.push_prompt(
    prompt_name="qa-prompt",
    object={
        "template": "You are a helpful assistant.\n\nQuestion: {question}\nAnswer:",
        "model": "gpt-4o",
        "temperature": 0.7
    },
    message="Initial version"
)

# Pull and use prompt
prompt = client.pull_prompt("qa-prompt")

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(**prompt.config)
response = llm.invoke(prompt.format(question="What is AI?"))

# Update prompt (creates new version)
client.push_prompt(
    prompt_name="qa-prompt",
    object={
        "template": "You are an expert.\n\nQ: {question}\nA:",
        "model": "gpt-4o",
        "temperature": 0.5
    },
    message="Improved prompt and lowered temperature"
)

# Specific version
prompt_v1 = client.pull_prompt("qa-prompt:1")
prompt_v2 = client.pull_prompt("qa-prompt:2")
```

### 4.7 Annotation Queues

**Definition:** Organized workflows for human review of runs, enabling team collaboration and manual quality assessment.

**Queue Operations:**

```python
# Create annotation queue (via UI or API)
# Add runs to queue based on filters:
# - Random sampling (10% of production)
# - Low confidence scores (score < 0.7)
# - Error cases (status == "error")
# - User-reported issues (feedback == "thumbs_down")

# Team reviews runs in queue:
# - Rate on custom rubrics
# - Add comments
# - Classify (correct/incorrect)
# - Escalate to expert reviewers

# Export annotations to dataset
# annotations → new dataset → re-evaluate system
```

---

## 5. Complete Examples Section

### 5.1 Basic RAG System with LangChain

```python
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Configure LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "lsv2_..."
os.environ["LANGCHAIN_PROJECT"] = "rag-demo"

# Load and split documents
documents = [...]  # Your documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# Create vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings
)

# Create RAG chain
llm = ChatOpenAI(model="gpt-4o", temperature=0)

prompt = PromptTemplate(
    template="""Use the following context to answer the question.

Context: {context}

Question: {question}

Answer:""",
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    chain_type_kwargs={"prompt": prompt}
)

# Query (automatically traced)
result = qa_chain.invoke({"query": "What is machine learning?"})
print(result["result"])

# View trace at https://smith.langchain.com/<workspace>/rag-demo
# You'll see:
# - RetrievalQA chain execution
# - Retriever run with 3 documents
# - LLM call with context and question
# - Token counts and costs
# - Latency breakdown
```

### 5.2 LangGraph Agent with Tools

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# Configure tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "agent-demo"

# Define tools
@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    # Implementation
    return f"Search results for: {query}"

@tool
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression."""
    return eval(expression)

tools = [search_web, calculate]

# Define agent state
class AgentState(TypedDict):
    messages: Annotated[list, "The messages in the conversation"]

# Define agent logic
llm = ChatOpenAI(model="gpt-4o").bind_tools(tools)

def call_model(state: AgentState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return "end"
    return "continue"

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)
workflow.add_edge("tools", "agent")

app = workflow.compile()

# Use agent (automatically traced)
inputs = {"messages": [HumanMessage(content="Search for Python tutorials then calculate 15 * 23")]}
result = app.invoke(inputs)

print(result["messages"][-1].content)

# LangSmith trace shows:
# - Agent node: LLM decides to use search_web tool
# - Tools node: search_web execution
# - Agent node: LLM decides to use calculate tool
# - Tools node: calculate execution
# - Agent node: LLM provides final answer
# Each step with timing, input/output, costs
```

### 5.3 Dataset-Driven Evaluation

```python
from langsmith import Client, evaluate
from langsmith.evaluation import EvaluationResult
from langsmith.schemas import Run, Example
from langchain_openai import ChatOpenAI

client = Client()

# Create dataset
dataset = client.create_dataset(
    dataset_name="math-qa",
    description="Math question answering"
)

math_examples = [
    {
        "inputs": {"question": "What is 15 + 27?"},
        "outputs": {"answer": "42"}
    },
    {
        "inputs": {"question": "Calculate 8 * 9"},
        "outputs": {"answer": "72"}
    },
    {
        "inputs": {"question": "What is 100 / 4?"},
        "outputs": {"answer": "25"}
    }
]

for ex in math_examples:
    client.create_example(
        dataset_id=dataset.id,
        inputs=ex["inputs"],
        outputs=ex["outputs"]
    )

# Define system under test
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def math_qa_system(inputs: dict) -> dict:
    question = inputs["question"]
    response = llm.invoke(f"Solve: {question}. Give only the numeric answer.")
    return {"answer": response.content.strip()}

# Define evaluators
def exact_match(run: Run, example: Example) -> EvaluationResult:
    """Check if answer exactly matches expected."""
    predicted = run.outputs["answer"]
    expected = example.outputs["answer"]

    return EvaluationResult(
        key="exact_match",
        score=1.0 if predicted == expected else 0.0
    )

def numeric_accuracy(run: Run, example: Example) -> EvaluationResult:
    """Check if numeric value is correct (handles formatting)."""
    import re

    pred_num = re.findall(r'-?\d+\.?\d*', run.outputs["answer"])
    exp_num = re.findall(r'-?\d+\.?\d*', example.outputs["answer"])

    if pred_num and exp_num:
        score = 1.0 if float(pred_num[0]) == float(exp_num[0]) else 0.0
    else:
        score = 0.0

    return EvaluationResult(
        key="numeric_accuracy",
        score=score
    )

# Run evaluation
results = evaluate(
    math_qa_system,
    data="math-qa",
    evaluators=[exact_match, numeric_accuracy],
    experiment_prefix="math-qa-gpt4o-mini",
    description="Baseline with GPT-4o-mini"
)

print(f"Exact Match: {results['exact_match'].mean():.2%}")
print(f"Numeric Accuracy: {results['numeric_accuracy'].mean():.2%}")

# Compare with different model
llm_4o = ChatOpenAI(model="gpt-4o", temperature=0)

def math_qa_system_4o(inputs: dict) -> dict:
    question = inputs["question"]
    response = llm_4o.invoke(f"Solve: {question}. Give only the numeric answer.")
    return {"answer": response.content.strip()}

results_4o = evaluate(
    math_qa_system_4o,
    data="math-qa",
    evaluators=[exact_match, numeric_accuracy],
    experiment_prefix="math-qa-gpt4o",
    description="Comparison with GPT-4o"
)

# Compare experiments in UI
# Navigate to Experiments tab to see side-by-side comparison
```

### 5.4 Production Monitoring with Feedback

```python
from langsmith import Client, traceable
from langchain_openai import ChatOpenAI
import uuid

client = Client()
llm = ChatOpenAI(model="gpt-4o")

# Configure project
os.environ["LANGCHAIN_PROJECT"] = "production-chatbot"

@traceable(
    name="chatbot-response",
    run_type="chain",
    metadata=lambda user_id, session_id: {
        "user_id": user_id,
        "session_id": session_id,
        "environment": "production"
    }
)
def generate_response(message: str, user_id: str, session_id: str) -> dict:
    """Generate chatbot response with monitoring."""

    try:
        response = llm.invoke(message)

        return {
            "response": response.content,
            "status": "success",
            "error": None
        }

    except Exception as e:
        return {
            "response": "I'm having trouble right now. Please try again.",
            "status": "error",
            "error": str(e)
        }

# Production usage
user_id = "user_12345"
session_id = str(uuid.uuid4())

# Generate response
result = generate_response(
    message="What is machine learning?",
    user_id=user_id,
    session_id=session_id
)

print(result["response"])

# Collect user feedback
def collect_user_feedback(run_id: str, thumbs_up: bool, comment: str = None):
    """Collect feedback from user."""

    client.create_feedback(
        run_id=run_id,
        key="user_rating",
        score=1.0 if thumbs_up else 0.0,
        comment=comment
    )

# Simulate user feedback
# (In real app, capture run_id and allow user to rate)
# run_id = get_latest_run_id()  # From LangSmith
# collect_user_feedback(run_id, thumbs_up=True, comment="Very helpful!")

# Monitor in LangSmith:
# 1. Filter by project="production-chatbot"
# 2. View traces filtered by user_id or session_id
# 3. Check feedback scores over time
# 4. Set up alerts for low feedback or high errors
# 5. Add low-rated responses to annotation queue for review
```

### 5.5 Prompt Version Control and A/B Testing

```python
from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

client = Client()

# Version 1: Initial prompt
prompt_v1 = {
    "template": "Answer the question concisely.\n\nQuestion: {question}",
    "model": "gpt-4o-mini",
    "temperature": 0.7
}

client.push_prompt(
    prompt_name="qa-prompt",
    object=prompt_v1,
    message="Initial version"
)

# Version 2: Improved prompt
prompt_v2 = {
    "template": "You are a helpful AI assistant. Provide a clear, concise answer.\n\nQuestion: {question}\n\nAnswer:",
    "model": "gpt-4o-mini",
    "temperature": 0.5
}

client.push_prompt(
    prompt_name="qa-prompt",
    object=prompt_v2,
    message="Added context and lowered temperature"
)

# Version 3: Different model
prompt_v3 = {
    "template": "You are a helpful AI assistant. Provide a clear, concise answer.\n\nQuestion: {question}\n\nAnswer:",
    "model": "gpt-4o",
    "temperature": 0.5
}

client.push_prompt(
    prompt_name="qa-prompt",
    object=prompt_v3,
    message="Upgraded to GPT-4o for better quality"
)

# A/B test: Compare versions
def test_prompt_version(version_num: int, questions: list[str]):
    """Test specific prompt version."""

    prompt_config = client.pull_prompt(f"qa-prompt:{version_num}")
    llm = ChatOpenAI(**prompt_config.config)

    results = []
    for q in questions:
        response = llm.invoke(prompt_config.format(question=q))
        results.append(response.content)

    return results

test_questions = [
    "What is Python?",
    "Explain machine learning",
    "How does the internet work?"
]

# Test all versions
for version in [1, 2, 3]:
    print(f"\n=== Testing Version {version} ===")
    results = test_prompt_version(version, test_questions)
    for q, a in zip(test_questions, results):
        print(f"Q: {q}\nA: {a}\n")

# Compare in LangSmith UI:
# 1. Navigate to Prompts
# 2. Select "qa-prompt"
# 3. View version history
# 4. Compare performance metrics across versions
# 5. Deploy best performing version

# Deploy to production
client.update_prompt_deployment(
    prompt_name="qa-prompt",
    version=3,  # Deploy v3
    environment="production"
)
```

### 5.6 Custom LLM-as-Judge Evaluator

```python
from langsmith.evaluation import EvaluationResult
from langsmith.schemas import Run, Example
from langchain_openai import ChatOpenAI
import json

def create_llm_judge_evaluator(criteria: str, scale: str = "1-5"):
    """Factory for creating LLM-as-judge evaluators."""

    def llm_judge(run: Run, example: Example) -> EvaluationResult:
        """Evaluate using LLM as judge."""

        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        prompt = f"""You are an expert evaluator. Rate the following output.

Criteria: {criteria}
Scale: {scale} (higher is better)

Input: {example.inputs}
Expected Output: {example.outputs if example.outputs else 'N/A'}
Actual Output: {run.outputs}

Provide your rating and brief reasoning in JSON format:
{{
    "score": <number on {scale} scale>,
    "reasoning": "<brief explanation>"
}}"""

        response = llm.invoke(prompt)
        result = json.loads(response.content)

        # Normalize to 0-1 scale
        if scale == "1-5":
            normalized_score = (result["score"] - 1) / 4
        elif scale == "0-10":
            normalized_score = result["score"] / 10
        else:
            normalized_score = result["score"]

        return EvaluationResult(
            key=criteria.replace(" ", "_").lower(),
            score=normalized_score,
            comment=result["reasoning"]
        )

    return llm_judge

# Create custom evaluators
accuracy_evaluator = create_llm_judge_evaluator(
    criteria="Factual accuracy",
    scale="1-5"
)

helpfulness_evaluator = create_llm_judge_evaluator(
    criteria="Helpfulness to user",
    scale="1-5"
)

clarity_evaluator = create_llm_judge_evaluator(
    criteria="Clarity and readability",
    scale="1-5"
)

# Use in evaluation
from langsmith import evaluate

results = evaluate(
    your_system,
    data="your-dataset",
    evaluators=[
        accuracy_evaluator,
        helpfulness_evaluator,
        clarity_evaluator
    ],
    experiment_prefix="comprehensive-eval"
)

print(f"Accuracy: {results['factual_accuracy'].mean():.2f}")
print(f"Helpfulness: {results['helpfulness_to_user'].mean():.2f}")
print(f"Clarity: {results['clarity_and_readability'].mean():.2f}")
```

---

## 6. Advanced Usage

### 6.1 Distributed Tracing Across Services

```python
# Service A (API)
from langsmith import traceable
from langsmith.run_trees import RunTree
import httpx

@traceable(name="api-handler", run_type="chain")
def handle_request(user_input: str) -> dict:
    """API endpoint handler."""

    # Get current run ID for passing to downstream services
    run_tree = RunTree.get_current_run_tree()
    parent_run_id = run_tree.trace_id if run_tree else None

    # Call downstream service with trace context
    response = httpx.post(
        "http://worker-service/process",
        json={"input": user_input},
        headers={"X-LangSmith-Trace-ID": parent_run_id}
    )

    return response.json()

# Service B (Worker)
from langsmith import Client
from langsmith.run_trees import RunTree

client = Client()

def process_task(request):
    """Worker service processing."""

    # Extract parent trace ID from headers
    parent_trace_id = request.headers.get("X-LangSmith-Trace-ID")

    # Create child run under parent trace
    root = RunTree(
        name="worker-processing",
        run_type="chain",
        inputs=request.json(),
        parent_run_id=parent_trace_id
    )

    # Processing logic
    result = expensive_computation(request.json()["input"])

    root.end(outputs={"result": result})
    root.post()

    return {"result": result}

# Now traces span across services!
```

### 6.2 Sampling Strategy for High-Volume Apps

```python
import random
from langsmith import traceable

def should_trace() -> bool:
    """Decide whether to trace this request."""
    # Sample 10% of requests
    return random.random() < 0.10

@traceable(
    name="high-volume-endpoint",
    enabled=should_trace  # Conditional tracing
)
def handle_request(data):
    """Handle high-volume requests with sampling."""
    return process(data)

# Alternative: Sample based on criteria
def smart_sampling() -> bool:
    """Sample strategically."""
    # Always trace:
    # - Errors
    # - Slow requests (>5s)
    # - First request from new users
    # - Random 1% sample

    is_error = check_if_error()
    is_slow = check_if_slow()
    is_new_user = check_if_new_user()
    is_random_sample = random.random() < 0.01

    return is_error or is_slow or is_new_user or is_random_sample

@traceable(enabled=smart_sampling)
def smart_traced_function(data):
    return process(data)
```

### 6.3 Custom Metadata and Tags

```python
from langsmith import traceable
import time

@traceable(
    name="api-call",
    metadata=lambda user_id, request_type, **kwargs: {
        "user_id": user_id,
        "request_type": request_type,
        "timestamp": time.time(),
        "version": "v2.1.0",
        "region": "us-east-1"
    },
    tags=lambda user_id, request_type: [
        f"user:{user_id}",
        f"type:{request_type}",
        "production"
    ]
)
def api_endpoint(user_id: str, request_type: str, payload: dict):
    """API with rich metadata."""
    return process(payload)

# Usage
result = api_endpoint(
    user_id="user_12345",
    request_type="search",
    payload={"query": "machine learning"}
)

# In LangSmith UI, filter by:
# - metadata.user_id = "user_12345"
# - tags includes "type:search"
# - metadata.version = "v2.1.0"
```

### 6.4 Error Tracking and Alerting

```python
from langsmith import traceable, Client
import logging

client = Client()
logger = logging.getLogger(__name__)

@traceable(name="critical-operation", run_type="chain")
def critical_operation(data):
    """Operation with error tracking."""

    try:
        result = risky_operation(data)
        return {"status": "success", "result": result}

    except Exception as e:
        logger.error(f"Critical operation failed: {e}")

        # Error is automatically captured in trace
        # Set up alert in LangSmith UI:
        # 1. Navigate to Monitoring → Alerts
        # 2. Create alert: "error_rate > 5% over 15 minutes"
        # 3. Notify via: Slack, Email, PagerDuty

        raise  # Re-raise to preserve error in trace

# Configure alerts in UI:
# - Error rate threshold
# - Latency P95 threshold
# - Cost spike detection
# - Quality score drop
```

### 6.5 Batch Evaluation with Concurrency

```python
from langsmith import Client, evaluate
from concurrent.futures import ThreadPoolExecutor
import asyncio

client = Client()

# Async system for faster evaluation
async def async_qa_system(inputs: dict) -> dict:
    """Async version for concurrent evaluation."""
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o")
    response = await llm.ainvoke(inputs["question"])
    return {"answer": response.content}

# Evaluate with concurrency
results = evaluate(
    async_qa_system,
    data="large-dataset",  # 1000s of examples
    evaluators=[accuracy_evaluator, relevance_evaluator],
    experiment_prefix="large-scale-eval",
    max_concurrency=10,  # Run 10 evaluations in parallel
    description="Large-scale evaluation with concurrency"
)

# For even faster evaluation: use batch API
def batch_qa_system(inputs_list: list[dict]) -> list[dict]:
    """Batch processing for efficiency."""
    from openai import OpenAI

    client = OpenAI()

    # Create batch file
    batch_requests = [
        {
            "custom_id": f"request-{i}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [{"role": "user", "content": inp["question"]}]
            }
        }
        for i, inp in enumerate(inputs_list)
    ]

    # Submit batch (50% cheaper, 24hr turnaround)
    batch = client.batches.create(
        input_file_id=upload_batch_file(batch_requests),
        endpoint="/v1/chat/completions"
    )

    # Poll for completion
    while batch.status != "completed":
        time.sleep(60)
        batch = client.batches.retrieve(batch.id)

    # Return results
    return parse_batch_results(batch)
```

### 6.6 Integration with CI/CD

```python
# tests/test_qa_system.py
import pytest
from langsmith import Client, evaluate
from langsmith.evaluation import EvaluationResult

client = Client()

def test_qa_system_quality():
    """CI/CD test for QA system quality."""

    # Run evaluation
    results = evaluate(
        qa_system,
        data="qa-test-set",
        evaluators=[correctness_evaluator, relevance_evaluator],
        experiment_prefix="ci-test",
        blocking=True  # Wait for completion
    )

    # Assert quality thresholds
    assert results["correctness"].mean() >= 0.90, "Correctness below threshold"
    assert results["relevance"].mean() >= 0.85, "Relevance below threshold"

    # Compare to baseline
    baseline_experiment = client.read_experiment(experiment_name="baseline")
    assert results["correctness"].mean() >= baseline_experiment.results["correctness"], \
        "Regression detected: quality worse than baseline"

# Run in CI/CD:
# pytest tests/test_qa_system.py --langsmith-api-key=$LANGSMITH_API_KEY
```

```yaml
# .github/workflows/eval.yml
name: LLM Evaluation

on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run evaluations
        env:
          LANGCHAIN_API_KEY: ${{ secrets.LANGSMITH_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          pytest tests/test_qa_system.py -v

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: evaluation-results
          path: evaluation_results.json
```

---

## 7. Best Practices

### 7.1 Tracing Strategy

**DO:**
- Enable tracing selectively per environment
  ```python
  # Development: trace everything
  if os.getenv("ENV") == "development":
      os.environ["LANGCHAIN_TRACING_V2"] = "true"

  # Production: sample strategically
  if os.getenv("ENV") == "production":
      os.environ["LANGCHAIN_TRACING_V2"] = "true" if should_trace() else "false"
  ```

- Use meaningful project names
  ```python
  # Good
  os.environ["LANGCHAIN_PROJECT"] = "chatbot-production"

  # Bad
  os.environ["LANGCHAIN_PROJECT"] = "test"
  ```

- Add rich metadata
  ```python
  @traceable(
      metadata=lambda user_id, **kwargs: {
          "user_id": user_id,
          "feature": "search",
          "version": "v2.0",
          "experiment": "new_ranking"
      }
  )
  def search_endpoint(user_id, query):
      pass
  ```

**DON'T:**
- Trace every request in high-volume production (use sampling)
- Log sensitive data (PII, credentials, secrets)
- Create too many projects (use tags/metadata instead)
- Ignore error handling in traced functions

### 7.2 Dataset Management

**Maintaining Quality Datasets:**

1. **Start Small, Iterate**
   ```python
   # Begin with 20-50 high-quality examples
   # Expand based on failure modes
   ```

2. **Version Datasets**
   ```python
   # Clone before major changes
   dataset_v2 = client.clone_dataset(
       source_dataset_id=dataset_v1.id,
       target_dataset_name="qa-dataset-v2.0"
   )
   ```

3. **Curate from Production**
   ```python
   # Export interesting cases from production traces
   # Filter: low scores, user-reported issues, edge cases
   ```

4. **Balance Difficulty**
   ```python
   # Include:
   # - Easy cases (baseline)
   # - Medium cases (typical)
   # - Hard cases (stress test)
   # - Edge cases (corner cases)
   ```

5. **Regular Updates**
   ```python
   # Monthly review:
   # - Add new patterns from production
   # - Remove outdated examples
   # - Update expected outputs
   ```

### 7.3 Evaluation Workflow

**Systematic Evaluation Process:**

```python
# 1. Define success metrics
metrics = {
    "accuracy": 0.90,  # Must be >90% correct
    "relevance": 0.85,  # Must be >85% relevant
    "latency": 2.0,  # Must be <2s
    "cost": 0.01  # Must be <$0.01 per query
}

# 2. Create baseline
baseline = evaluate(
    current_system,
    data="test-dataset",
    evaluators=all_evaluators,
    experiment_prefix="baseline"
)

# 3. Iterate and experiment
for experiment_name, system_variant in experiments.items():
    results = evaluate(
        system_variant,
        data="test-dataset",
        evaluators=all_evaluators,
        experiment_prefix=experiment_name
    )

    # Compare to baseline
    if results > baseline and meets_thresholds(results, metrics):
        print(f"✓ {experiment_name} is better!")
    else:
        print(f"✗ {experiment_name} did not improve")

# 4. Statistical validation
# Use LangSmith UI to check:
# - Confidence intervals
# - Statistical significance
# - Per-category performance

# 5. Production rollout
# - Deploy winning variant
# - Monitor with same metrics
# - Compare production vs test performance
```

### 7.4 Cost Management

**Optimization Strategies:**

1. **Monitor Spending**
   ```python
   # Use LangSmith dashboard to track:
   # - Cost per model
   # - Cost per user/feature
   # - Cost trends over time
   # - Most expensive queries
   ```

2. **Use Cheaper Models for Simple Tasks**
   ```python
   def route_by_complexity(query):
       if is_simple(query):
           return gpt_4o_mini.invoke(query)  # $0.15/1M tokens
       else:
           return gpt_4o.invoke(query)  # $2.50/1M tokens
   ```

3. **Cache Responses**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=1000)
   def cached_llm_call(prompt: str):
       return llm.invoke(prompt)
   ```

4. **Set Token Limits**
   ```python
   llm = ChatOpenAI(
       model="gpt-4o",
       max_tokens=500,  # Prevent runaway costs
       timeout=30  # Prevent slow requests
   )
   ```

5. **Batch Processing**
   ```python
   # Use OpenAI Batch API for 50% discount
   # Trade latency (24hr) for cost savings
   ```

### 7.5 Team Collaboration

**Multi-User Workflows:**

1. **Project Organization**
   ```python
   # Separate projects by:
   # - Team (chatbot-team, search-team)
   # - Environment (dev, staging, prod)
   # - Feature (feature-x-experiment)
   ```

2. **Shared Datasets**
   ```python
   # Create team-wide golden datasets
   # Share across experiments
   # Version control for reproducibility
   ```

3. **Annotation Queues**
   ```python
   # Divide annotation work:
   # - Expert reviewers for complex cases
   # - Team members for routine review
   # - Track inter-annotator agreement
   ```

4. **Prompt Collaboration**
   ```python
   # Use prompt commit messages
   client.push_prompt(
       "qa-prompt",
       object=prompt_v2,
       message="@jane improved clarity based on user feedback"
   )
   ```

5. **RBAC**
   ```python
   # Configure role-based access:
   # - Viewers: See traces and experiments
   # - Editors: Create datasets, run evaluations
   # - Admins: Manage team, configure settings
   ```

---

## 8. Integration Guide

### 8.1 LangChain Integration

**Zero-Config Tracing:**

```python
# Just set environment variables - that's it!
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "lsv2_..."

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Everything is automatically traced
llm = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
chain = prompt | llm

result = chain.invoke({"topic": "AI"})
# Trace automatically appears in LangSmith!
```

**Custom Callbacks:**

```python
from langsmith import Client
from langchain.callbacks.tracers import LangChainTracer

client = Client()
tracer = LangChainTracer(project_name="custom-project")

# Use in chain
result = chain.invoke(
    {"topic": "AI"},
    config={"callbacks": [tracer]}
)
```

### 8.2 LangGraph Integration

**Automatic Agent Tracing:**

```python
from langgraph.graph import StateGraph

# Build graph
workflow = StateGraph(AgentState)
# ... add nodes and edges ...
app = workflow.compile()

# Tracing enabled via environment variables
# Each node execution creates a span
# Tool calls are nested spans
# Full agent trajectory visible
result = app.invoke({"messages": [...]})
```

### 8.3 OpenAI Integration (Without LangChain)

```python
from langsmith import traceable
from openai import OpenAI

client = OpenAI()

@traceable(name="openai-call", run_type="llm")
def call_openai(prompt: str) -> str:
    """Trace OpenAI calls."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Automatically traced
result = call_openai("Hello!")
```

### 8.4 Anthropic Integration

```python
from langsmith import traceable
from anthropic import Anthropic

anthropic_client = Anthropic()

@traceable(name="claude-call", run_type="llm")
def call_claude(prompt: str) -> str:
    """Trace Claude calls."""
    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

result = call_claude("Hello!")
```

### 8.5 CrewAI Integration

```python
from crewai import Crew, Agent, Task
from langsmith.run_helpers import traceable

@traceable(run_type="chain")
def run_crew(inputs: dict):
    """Trace CrewAI execution."""

    agent = Agent(
        role="Researcher",
        goal="Research topics",
        backstory="Expert researcher"
    )

    task = Task(
        description=inputs["task"],
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()

    return {"result": result}

# Trace crew execution
result = run_crew({"task": "Research AI trends"})
```

### 8.6 AutoGen Integration

```python
from langsmith import traceable
import autogen

config_list = [{"model": "gpt-4o", "api_key": "..."}]

@traceable(name="autogen-conversation")
def run_autogen_conversation(task: str):
    """Trace AutoGen multi-agent conversation."""

    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config={"config_list": config_list}
    )

    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10
    )

    # Start conversation
    user_proxy.initiate_chat(assistant, message=task)

    return {"result": "completed"}

result = run_autogen_conversation("Write a Python function to sort a list")
```

### 8.7 LlamaIndex Integration

```python
from llama_index.core import VectorStoreIndex
from llama_index.core.callbacks import CallbackManager
from langsmith import Client

client = Client()

# Create LangSmith callback
from llama_index.callbacks.langsmith import LangsmithCallbackHandler

langsmith_handler = LangsmithCallbackHandler(
    project_name="llamaindex-rag"
)

callback_manager = CallbackManager([langsmith_handler])

# Use in index
index = VectorStoreIndex.from_documents(
    documents,
    callback_manager=callback_manager
)

query_engine = index.as_query_engine()
response = query_engine.query("What is AI?")
# Automatically traced in LangSmith
```

---

## 9. Troubleshooting

### 9.1 Common Issues

**Issue: Traces Not Appearing**

```python
# Problem: Environment variables not set
# Solution: Verify configuration

import os
print(f"Tracing enabled: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"API key set: {bool(os.getenv('LANGCHAIN_API_KEY'))}")
print(f"Project: {os.getenv('LANGCHAIN_PROJECT', 'default')}")

# If missing, set them:
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "lsv2_..."
```

**Issue: API Key Errors**

```python
# Test API key validity
from langsmith import Client

try:
    client = Client()
    projects = list(client.list_projects())
    print(f"✓ API key valid. {len(projects)} projects found.")
except Exception as e:
    print(f"✗ API key error: {e}")
    print("Get a new key at: https://smith.langchain.com/settings")
```

**Issue: Slow Trace Ingestion**

```python
# Problem: Traces sent synchronously
# Solution: Use async mode (default in SDK)

# SDK batches traces automatically in background
# But in short-lived scripts, add flush:

from langsmith import Client
client = Client()

# ... your code ...

client.flush()  # Wait for traces to send before exit
```

**Issue: Missing Nested Spans**

```python
# Problem: Nested @traceable decorators not working
# Solution: Ensure traceable context propagation

from langsmith import traceable

@traceable(name="parent")  # ✓ Parent trace
def parent():
    child()  # ✓ Will create nested span
    return "done"

@traceable(name="child")
def child():
    return "child result"

# Make sure both functions are decorated
```

### 9.2 Performance Issues

**High Memory Usage:**

```python
# Problem: Storing large trace data in memory
# Solution: Reduce payload sizes

@traceable
def process_large_data(data: str):
    # Don't log huge strings
    if len(data) > 10000:
        # Log summary instead
        summary = data[:1000] + f"... ({len(data)} chars)"
        return process(data)  # Process full data
    return process(data)
```

**Network Latency:**

```python
# Problem: Synchronous trace submission blocks execution
# Solution: SDK handles async automatically, but verify

import os

# Ensure async mode (default)
# Traces sent in background thread
# No blocking

# For faster tests, disable tracing:
os.environ["LANGCHAIN_TRACING_V2"] = "false"
```

### 9.3 Dataset Issues

**Upload Failures:**

```python
# Problem: Large CSV upload fails
# Solution: Batch uploads

import pandas as pd
from langsmith import Client

client = Client()

# Read large CSV
df = pd.read_csv("large_dataset.csv")

# Upload in batches
batch_size = 100
for i in range(0, len(df), batch_size):
    batch = df[i:i+batch_size]

    try:
        client.upload_dataframe(
            df=batch,
            name=f"large-dataset-batch-{i//batch_size}",
            input_keys=["input"],
            output_keys=["output"]
        )
        print(f"✓ Uploaded batch {i//batch_size}")
    except Exception as e:
        print(f"✗ Failed batch {i//batch_size}: {e}")
```

### 9.4 Evaluation Issues

**Timeout Errors:**

```python
# Problem: Evaluation takes too long
# Solution: Increase timeout, reduce concurrency

from langsmith import evaluate

results = evaluate(
    your_function,
    data="large-dataset",
    evaluators=evaluators,
    max_concurrency=5,  # Reduce from default 10
    client=Client(timeout=300)  # 5 minute timeout
)
```

**Evaluator Errors:**

```python
# Problem: Custom evaluator crashes
# Solution: Add error handling

from langsmith.evaluation import EvaluationResult
from langsmith.schemas import Run, Example

def safe_evaluator(run: Run, example: Example) -> EvaluationResult:
    """Evaluator with error handling."""
    try:
        # Your evaluation logic
        score = compute_score(run, example)

        return EvaluationResult(
            key="my_metric",
            score=score
        )

    except Exception as e:
        # Return 0 on error, log for debugging
        print(f"Evaluator error: {e}")
        return EvaluationResult(
            key="my_metric",
            score=0.0,
            comment=f"Error: {str(e)}"
        )
```

### 9.5 Self-Hosted Issues

**Database Connection Errors:**

```bash
# Problem: Cannot connect to PostgreSQL
# Solution: Check connection string

# Verify format:
# postgresql://username:password@host:port/database

# Test connection:
psql "postgresql://langsmith:password@localhost:5432/langsmith"

# Check network:
telnet postgres-host 5432
```

**Frontend Not Loading:**

```bash
# Problem: UI shows blank page
# Solution: Check backend URL

# Verify backend URL in frontend env:
docker logs langsmith-frontend | grep BACKEND_URL

# Should be: http://langsmith-backend:1984

# Test backend health:
curl http://langsmith-backend:1984/health
```

---

## 10. API Reference

### 10.1 Client Class

```python
from langsmith import Client

client = Client(
    api_url: str = "https://api.smith.langchain.com",  # API endpoint
    api_key: str = None,  # Defaults to LANGCHAIN_API_KEY env var
    timeout: int = 60,  # Request timeout in seconds
    web_url: str = None  # Web UI URL for links
)
```

**Methods:**

```python
# Projects
client.create_project(project_name: str, description: str = None)
client.list_projects()
client.delete_project(project_name: str)

# Datasets
client.create_dataset(
    dataset_name: str,
    description: str = None,
    data_type: str = "kv"  # key-value
)
client.list_datasets()
client.read_dataset(dataset_name: str)
client.delete_dataset(dataset_name: str)
client.clone_dataset(source_dataset_id: str, target_dataset_name: str)

# Examples
client.create_example(
    dataset_id: str,
    inputs: dict,
    outputs: dict = None,
    metadata: dict = None
)
client.list_examples(dataset_id: str)
client.update_example(example_id: str, ...)
client.delete_example(example_id: str)

# Runs (Traces)
client.list_runs(
    project_name: str = None,
    start_time: datetime = None,
    end_time: datetime = None,
    filter: str = None,  # e.g., "eq(name, 'my-run')"
    limit: int = 100
)
client.read_run(run_id: str)
client.share_run(run_id: str)  # Returns shareable URL

# Feedback
client.create_feedback(
    run_id: str,
    key: str,
    score: float = None,
    value: Any = None,
    comment: str = None
)
client.list_feedback(run_ids: list[str] = None)

# Prompts
client.push_prompt(
    prompt_name: str,
    object: dict,  # Template and config
    message: str = None  # Commit message
)
client.pull_prompt(prompt_identifier: str)  # name or name:version
client.list_prompts()

# Other
client.upload_dataframe(
    df: pd.DataFrame,
    name: str,
    input_keys: list[str],
    output_keys: list[str] = None
)
```

### 10.2 Traceable Decorator

```python
from langsmith import traceable

@traceable(
    name: str = None,  # Run name (defaults to function name)
    run_type: str = None,  # llm, chain, tool, retriever, etc.
    project_name: str = None,  # Override default project
    metadata: dict | Callable = None,  # Static dict or callable
    tags: list[str] | Callable = None,  # Static list or callable
    enabled: bool | Callable = True,  # Conditional tracing
    reduce_fn: Callable = None  # For generators/streams
)
def my_function(...):
    pass
```

**Examples:**

```python
# Basic
@traceable
def simple_function(input: str):
    return process(input)

# With type
@traceable(run_type="llm")
def llm_call(prompt: str):
    return llm.invoke(prompt)

# With metadata
@traceable(metadata={"version": "v2.0"})
def versioned_function(input: str):
    return process(input)

# Dynamic metadata
@traceable(metadata=lambda user_id: {"user_id": user_id})
def user_specific(user_id: str, data: str):
    return process(data)

# Conditional tracing
@traceable(enabled=lambda: random.random() < 0.1)  # 10% sampling
def sampled_function(input: str):
    return process(input)
```

### 10.3 Evaluate Function

```python
from langsmith import evaluate

results = evaluate(
    target: Callable,  # Function to evaluate
    data: str | list,  # Dataset name or list of examples
    evaluators: list[Callable],  # List of evaluator functions
    experiment_prefix: str = None,  # Experiment name prefix
    description: str = None,  # Experiment description
    metadata: dict = None,  # Experiment metadata
    max_concurrency: int = 10,  # Parallel evaluation limit
    client: Client = None,  # Custom client
    num_repetitions: int = 1,  # Run each example N times
    blocking: bool = True  # Wait for completion
) -> ExperimentResults
```

**Returns:**

```python
class ExperimentResults:
    experiment_name: str
    results: dict[str, list[float]]  # Metric scores

    def mean(metric: str) -> float:
        """Average score for metric."""

    def median(metric: str) -> float:
        """Median score for metric."""

    def std(metric: str) -> float:
        """Standard deviation for metric."""
```

### 10.4 Evaluation Result

```python
from langsmith.evaluation import EvaluationResult

def my_evaluator(run, example):
    return EvaluationResult(
        key: str,  # Metric name
        score: float = None,  # Numeric score (0-1 recommended)
        value: Any = None,  # Any value (string, bool, etc.)
        comment: str = None,  # Explanation
        correction: dict = None,  # Suggested correction
        evaluator_info: dict = None  # Metadata about evaluator
    )
```

### 10.5 Run Tree (Manual Tracing)

```python
from langsmith.run_trees import RunTree

# Create root trace
root = RunTree(
    name: str,  # Run name
    run_type: str,  # llm, chain, tool, etc.
    inputs: dict,  # Input data
    project_name: str = None,  # Project
    tags: list[str] = None,  # Tags
    extra: dict = None  # Metadata
)

# Create child run
child = root.create_child(
    name: str,
    run_type: str,
    inputs: dict
)

# End run
root.end(
    outputs: dict = None,  # Output data
    error: str = None  # Error message if failed
)

# Post to LangSmith
root.post()

# Alternative: context manager
with RunTree(...) as run:
    # Do work
    result = process()
    run.outputs = {"result": result}
# Automatically ended and posted
```

---

## 11. Performance & Optimization

### 11.1 Trace Overhead

**Measurement:**

```python
import time
from langsmith import traceable

def baseline_function(input_data):
    return process(input_data)

@traceable
def traced_function(input_data):
    return process(input_data)

# Measure overhead
iterations = 1000

start = time.time()
for _ in range(iterations):
    baseline_function("test")
baseline_time = time.time() - start

start = time.time()
for _ in range(iterations):
    traced_function("test")
traced_time = time.time() - start

overhead = (traced_time - baseline_time) / iterations * 1000
print(f"Overhead per call: {overhead:.2f}ms")
# Typical: <1ms per traced function
```

**Optimization:**

```python
# 1. Reduce trace payloads
@traceable
def optimized_function(large_data: str):
    # Don't log full data if too large
    if len(large_data) > 10000:
        # Log summary
        return process(large_data)
    return process(large_data)

# 2. Sample high-volume functions
@traceable(enabled=lambda: random.random() < 0.01)  # 1% sample
def high_volume_function(data):
    return process(data)

# 3. Disable tracing for testing
import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"
```

### 11.2 Batch Operations

**Efficient Dataset Operations:**

```python
from langsmith import Client

client = Client()

# Batch create examples
examples = [
    {"inputs": {"q": f"Question {i}"}, "outputs": {"a": f"Answer {i}"}}
    for i in range(1000)
]

# More efficient than individual create_example calls
client.create_examples(
    dataset_id=dataset.id,
    examples=examples
)
```

### 11.3 Caching

**Response Caching:**

```python
from functools import lru_cache
import hashlib
import json

def cache_key(inputs: dict) -> str:
    """Generate cache key from inputs."""
    return hashlib.md5(json.dumps(inputs, sort_keys=True).encode()).hexdigest()

# In-memory cache
_cache = {}

@traceable
def cached_llm_call(inputs: dict) -> dict:
    """LLM call with caching."""

    key = cache_key(inputs)

    if key in _cache:
        return _cache[key]

    result = llm.invoke(inputs)
    _cache[key] = result

    return result

# Or use Redis for distributed caching
import redis

redis_client = redis.Redis(host='localhost', port=6379)

@traceable
def redis_cached_llm_call(inputs: dict) -> dict:
    """LLM call with Redis caching."""

    key = f"llm:{cache_key(inputs)}"

    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)

    result = llm.invoke(inputs)
    redis_client.setex(key, 3600, json.dumps(result))  # 1 hour TTL

    return result
```

### 11.4 Database Optimization (Self-Hosted)

**PostgreSQL Tuning:**

```sql
-- Increase shared buffers for better caching
ALTER SYSTEM SET shared_buffers = '4GB';

-- Increase work memory for complex queries
ALTER SYSTEM SET work_mem = '64MB';

-- Increase parallel workers
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;

-- Create indexes on frequent queries
CREATE INDEX idx_runs_project_name ON runs(project_name);
CREATE INDEX idx_runs_start_time ON runs(start_time);
CREATE INDEX idx_runs_status ON runs(status);
CREATE INDEX idx_feedback_run_id ON feedback(run_id);

-- Vacuum regularly
VACUUM ANALYZE;
```

**ClickHouse Tuning (for analytics):**

```xml
<!-- config.xml -->
<clickhouse>
  <max_memory_usage>10000000000</max_memory_usage>
  <max_threads>8</max_threads>

  <!-- Optimize for analytics queries -->
  <merge_tree>
    <max_bytes_before_external_sort>10000000000</max_bytes_before_external_sort>
  </merge_tree>
</clickhouse>
```

### 11.5 Network Optimization

**Connection Pooling:**

```python
from langsmith import Client
import httpx

# Custom HTTP client with connection pooling
http_client = httpx.Client(
    limits=httpx.Limits(
        max_connections=100,
        max_keepalive_connections=20
    ),
    timeout=60.0
)

client = Client(http_client=http_client)
```

---

## 12. Security Considerations

### 12.1 API Key Management

**Best Practices:**

```python
# ✓ Good: Use environment variables
import os
api_key = os.getenv("LANGCHAIN_API_KEY")

# ✓ Good: Use secret management
from azure.keyvault.secrets import SecretClient
api_key = secret_client.get_secret("langsmith-api-key").value

# ✗ Bad: Hardcode keys
api_key = "lsv2_pt_..."  # Never do this!

# ✗ Bad: Commit to git
# config.py
LANGCHAIN_API_KEY = "lsv2_..."  # Don't commit secrets!
```

**Key Rotation:**

```bash
# 1. Create new API key in LangSmith UI
# 2. Update environment variables
export LANGCHAIN_API_KEY="new-key"

# 3. Test new key
python -c "from langsmith import Client; Client().list_projects()"

# 4. Revoke old key in UI
```

### 12.2 Data Privacy

**Sensitive Data Handling:**

```python
import re

def sanitize_pii(text: str) -> str:
    """Remove PII from text."""
    # Email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)

    # Phone numbers
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)

    # SSN
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)

    # Credit cards
    text = re.sub(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[CC]', text)

    return text

@traceable
def secure_processing(user_input: str):
    """Process data with PII removal."""
    # Sanitize before processing
    clean_input = sanitize_pii(user_input)

    result = process(clean_input)

    # Also sanitize output
    clean_output = sanitize_pii(result)

    return clean_output
```

**Disable Tracing for Sensitive Operations:**

```python
import os

@traceable(enabled=False)  # Never trace this function
def handle_payment(card_info: dict):
    """Process payment - never trace."""
    return process_payment(card_info)

# Or conditionally disable
sensitive_mode = os.getenv("SENSITIVE_MODE") == "true"

@traceable(enabled=not sensitive_mode)
def conditional_tracing(data):
    return process(data)
```

### 12.3 Access Control

**Role-Based Permissions (Enterprise):**

```python
# Configure in LangSmith UI:

# Roles:
# - Viewer: Read-only access to traces and experiments
# - Editor: Can create datasets, run evaluations
# - Admin: Full access including team management

# Project-level permissions:
# - Public: Anyone in org can see
# - Private: Only specific users/teams
```

**API Key Scoping:**

```python
# Create limited-scope API keys:
# - Read-only keys for CI/CD
# - Project-specific keys
# - Time-limited keys for contractors
```

### 12.4 Compliance

**GDPR Compliance:**

```python
from langsmith import Client

client = Client()

# Right to erasure: Delete user data
def delete_user_data(user_id: str):
    """Delete all data for a user."""

    # Find all runs for user
    runs = client.list_runs(
        filter=f'eq(metadata."user_id", "{user_id}")'
    )

    # Delete runs
    for run in runs:
        client.delete_run(run.id)

    # Also delete from datasets
    # ... (similar process)

# Data export: Export user data
def export_user_data(user_id: str) -> dict:
    """Export all data for a user."""

    runs = client.list_runs(
        filter=f'eq(metadata."user_id", "{user_id}")'
    )

    return {
        "runs": [run.dict() for run in runs],
        "feedback": [...]  # Export feedback
    }
```

**HIPAA Compliance (Enterprise):**

- Use self-hosted deployment in compliant infrastructure
- Enable encryption at rest and in transit
- Implement audit logging
- Configure data retention policies
- Sign BAA (Business Associate Agreement) with LangChain

### 12.5 Network Security

**Self-Hosted Security:**

```yaml
# Kubernetes network policies
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: langsmith-network-policy
spec:
  podSelector:
    matchLabels:
      app: langsmith
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: trusted-services
    ports:
    - protocol: TCP
      port: 1984
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
```

**TLS Configuration:**

```yaml
# Ingress with TLS
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: langsmith-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - langsmith.company.com
    secretName: langsmith-tls
  rules:
  - host: langsmith.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: langsmith-backend
            port:
              number: 1984
```

---

## 13. References & Resources

### 13.1 Official Documentation

- **Main Docs**: https://docs.langchain.com/langsmith
- **API Reference**: https://api.smith.langchain.com/redoc
- **Python SDK**: https://github.com/langchain-ai/langsmith-sdk
- **TypeScript SDK**: https://github.com/langchain-ai/langsmithjs

### 13.2 Tutorials & Guides

**Getting Started:**
- [Quick Start Guide](https://docs.langchain.com/langsmith/quickstart)
- [Tracing Tutorial](https://docs.langchain.com/langsmith/tutorials/tracing)
- [Evaluation Tutorial](https://docs.langchain.com/langsmith/tutorials/evaluation)

**Advanced:**
- [Prompt Engineering with LangSmith](https://docs.langchain.com/langsmith/guides/prompts)
- [Production Monitoring](https://docs.langchain.com/langsmith/guides/monitoring)
- [Human-in-the-Loop Evaluation](https://docs.langchain.com/langsmith/guides/annotation)

### 13.3 Example Projects

**GitHub Examples:**
- https://github.com/langchain-ai/langsmith-cookbook
- RAG evaluation examples
- Agent monitoring examples
- Multi-framework integrations

### 13.4 Community

- **Discord**: https://discord.gg/langchain
- **Twitter**: [@LangChainAI](https://twitter.com/LangChainAI)
- **YouTube**: [LangChain YouTube Channel](https://www.youtube.com/@LangChainAI)
- **Blog**: https://blog.langchain.dev

### 13.5 Pricing & Plans

- **Pricing Page**: https://www.langchain.com/pricing
- **Free Tier**: 5,000 traces/month
- **Plus**: $39/user/month (10K traces, extended features)
- **Enterprise**: Custom pricing (self-hosting, compliance, dedicated support)

### 13.6 Support

- **Email**: support@langchain.com
- **Enterprise Support**: Contact sales for SLA-backed support
- **Community Forum**: https://github.com/langchain-ai/langchain/discussions

---

## Appendix A: Quick Reference

### Installation
```bash
pip install langsmith langchain langchain-openai
```

### Environment Setup
```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY="lsv2_..."
export LANGCHAIN_PROJECT="my-project"
```

### Basic Tracing
```python
# LangChain: Automatic
from langchain_openai import ChatOpenAI
llm = ChatOpenAI()
llm.invoke("Hello")  # Automatically traced

# Non-LangChain: Use decorator
from langsmith import traceable

@traceable
def my_function(input: str):
    return process(input)
```

### Evaluation
```python
from langsmith import evaluate

results = evaluate(
    your_function,
    data="dataset-name",
    evaluators=[evaluator1, evaluator2]
)
```

---

## Appendix B: Comparison with Alternatives

### LangSmith vs Langfuse

| Aspect | LangSmith | Langfuse |
|--------|-----------|----------|
| **Best For** | LangChain users | Framework-agnostic |
| **Self-Hosting** | Enterprise only | Free (open source) |
| **Free Tier** | 5K traces | Unlimited (self-host) |
| **Dataset Mgmt** | Excellent | Good |
| **Deployment** | Native agent deployment | No |
| **Prompt Mgmt** | Built-in playground | Basic versioning |

### LangSmith vs Phoenix

| Aspect | LangSmith | Phoenix |
|--------|-----------|---------|
| **Deployment** | Cloud SaaS | Local/self-hosted |
| **Cost** | $39/user/mo | Free |
| **LangChain** | Native | Via OpenInference |
| **Evaluation** | Comprehensive | Basic |
| **Use Case** | Production | Development |

### LangSmith vs Weights & Biases

| Aspect | LangSmith | W&B |
|--------|-----------|-----|
| **Focus** | LLM apps | ML experiments |
| **Tracing** | Built-in | Limited |
| **Agents** | Native support | No |
| **Research** | Limited | Excellent |
| **Cost** | Per user | Per seat |

---

**End of LangSmith Deep-Dive Guide**

For the latest updates, visit: https://docs.langchain.com/langsmith
