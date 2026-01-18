# TruLens: Deep Dive Guide

## Table of Contents

- [Introduction](#introduction)
- [Architecture Overview](#architecture-overview)
- [Installation and Setup](#installation-and-setup)
- [Core Concepts](#core-concepts)
- [Production-Ready Examples](#production-ready-examples)
- [Advanced Usage](#advanced-usage)
- [Best Practices](#best-practices)
- [Integration Guide](#integration-guide)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)
- [Performance](#performance)
- [Security](#security)
- [References](#references)

---

## Introduction

### What is TruLens?

TruLens is an **observability and evaluation framework** specifically designed for LLM applications, with deep focus on **RAG (Retrieval-Augmented Generation)** systems. It provides comprehensive instrumentation, feedback functions, and analytics for understanding and improving LLM application behavior.

**Key Characteristics:**

- **Deep Observability**: Automatic instrumentation of LLM application internals
- **Feedback Functions**: Modular evaluation components for quality assessment
- **RAG-Focused**: Specialized tools for retrieval and generation evaluation
- **Real-time Tracking**: Live monitoring of application behavior
- **Chain Tracing**: Complete visibility into multi-step LLM workflows
- **Ground Truth Management**: Compare predictions against golden datasets
- **Dashboard**: Interactive UI for exploring traces and metrics
- **Provider Agnostic**: Works with any LLM or vector database

### Why Use TruLens?

**Strengths:**

1. **Comprehensive Instrumentation**: Automatic tracking of all LLM interactions
2. **RAG Specialization**: Best-in-class tools for RAG system evaluation
3. **Feedback Function Library**: 20+ pre-built evaluation functions
4. **Custom Feedback**: Easy to create domain-specific evaluators
5. **Visual Dashboard**: Intuitive interface for exploring results
6. **Production Ready**: Handles scale and performance requirements
7. **Integration Friendly**: Works with LangChain, LlamaIndex, and custom apps
8. **Open Source**: Transparent, extensible, community-driven

**Ideal Use Cases:**

- RAG system development and optimization
- LLM application debugging and monitoring
- Production observability for LLM services
- A/B testing different prompts or models
- Quality assurance for LLM outputs
- Understanding retrieval effectiveness
- Tracking hallucinations and groundedness
- Multi-step chain analysis

### Framework Philosophy

TruLens design principles:

1. **Observability First**: You can't improve what you can't measure
2. **Zero Code Instrumentation**: Automatic tracking with minimal changes
3. **Modular Evaluation**: Compose feedback functions like building blocks
4. **RAG Excellence**: Deep understanding of retrieval-generation patterns
5. **Developer Experience**: Easy to integrate, understand, and extend
6. **Production Grade**: Performance and reliability for real workloads
7. **Open Ecosystem**: Works with all major LLM frameworks

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      TruLens Framework                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Application Instrumentation Layer              │  │
│  │  ┌─────────────┬──────────────┬──────────────────────┐  │  │
│  │  │  LangChain  │  LlamaIndex  │  Custom Apps         │  │  │
│  │  │  Wrapper    │  Wrapper     │  (TruCustomApp)      │  │  │
│  │  └─────────────┴──────────────┴──────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│         │                                                        │
│         ↓                                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Recording & Tracing Engine                  │  │
│  │  - Automatic span creation                               │  │
│  │  - Input/output capture                                  │  │
│  │  - Metadata extraction                                   │  │
│  │  - Timing & cost tracking                                │  │
│  │  - Chain decomposition                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│         │                                                        │
│         ↓                                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Feedback Function Engine                    │  │
│  │  ┌────────────┬────────────┬────────────┬───────────┐   │  │
│  │  │ Groundedness│ Relevance  │ Coherence  │ Custom    │   │  │
│  │  │ Language    │ Sentiment  │ Toxicity   │ Functions │   │  │
│  │  │ Question    │ Context    │ Answer     │           │   │  │
│  │  │ Statement   │ Retrieval  │ Similarity │           │   │  │
│  │  └────────────┴────────────┴────────────┴───────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│         │                                                        │
│         ↓                                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                Storage Layer                             │  │
│  │  - SQLite (local)                                        │  │
│  │  - PostgreSQL (production)                               │  │
│  │  - Record storage                                        │  │
│  │  - Feedback storage                                      │  │
│  │  - Ground truth storage                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│         │                                                        │
│         ↓                                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Analytics & Dashboard                       │  │
│  │  - Streamlit UI                                          │  │
│  │  - Record explorer                                       │  │
│  │  - Metric visualization                                  │  │
│  │  - Feedback aggregation                                  │  │
│  │  - Comparative analysis                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Application Wrappers

TruLens provides automatic instrumentation through wrappers:

**TruChain (LangChain)**
```python
from trulens_eval import TruChain
from langchain.chains import RetrievalQA

chain = RetrievalQA.from_chain_type(...)
tru_chain = TruChain(chain, app_id="my_rag_app")

with tru_chain as recording:
    result = chain.run("What is AI?")
```

**TruLlama (LlamaIndex)**
```python
from trulens_eval import TruLlama
from llama_index import VectorStoreIndex

index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()
tru_llama = TruLlama(query_engine, app_id="llama_app")

with tru_llama as recording:
    response = query_engine.query("What is AI?")
```

**TruCustomApp (Custom Applications)**
```python
from trulens_eval import TruCustomApp
from trulens_eval.tru_custom_app import instrument

class MyRAG:
    @instrument
    def retrieve(self, query: str) -> list:
        # Retrieval logic
        return docs

    @instrument
    def generate(self, query: str, context: list) -> str:
        # Generation logic
        return response

app = MyRAG()
tru_app = TruCustomApp(app, app_id="custom_rag")
```

#### 2. Feedback Functions

Modular evaluation components:

```python
from trulens_eval.feedback import Feedback
from trulens_eval.feedback.provider.openai import OpenAI

provider = OpenAI()

# Groundedness: Is the response supported by context?
f_groundedness = Feedback(
    provider.groundedness_measure_with_cot_reasons
).on_input_output()

# Answer Relevance: Does the answer address the question?
f_answer_relevance = Feedback(
    provider.relevance
).on_input_output()

# Context Relevance: Is retrieved context relevant to query?
f_context_relevance = Feedback(
    provider.context_relevance
).on_input().on(TruChain.select_context()).aggregate(np.mean)
```

#### 3. Recording System

Captures complete execution traces:

- **Records**: Complete trace of application execution
- **Spans**: Individual steps within a trace
- **Metadata**: Costs, latency, model info
- **Inputs/Outputs**: All data flowing through the system
- **Feedback**: Evaluation results attached to records

#### 4. Dashboard

Interactive Streamlit interface:

```bash
trulens-eval run
```

Features:
- Record browser with filtering
- Metric trends and distributions
- Feedback function results
- Comparative analysis
- Cost and latency tracking
- Export capabilities

---

## Installation and Setup

### Installation

**Basic Installation:**
```bash
pip install trulens-eval
```

**With Specific Providers:**
```bash
# With OpenAI
pip install trulens-eval[openai]

# With LangChain
pip install trulens-eval[langchain]

# With LlamaIndex
pip install trulens-eval[llama-index]

# With all extras
pip install trulens-eval[all]
```

**Development Installation:**
```bash
git clone https://github.com/truera/trulens.git
cd trulens/trulens_eval
pip install -e ".[dev]"
```

### Environment Setup

**.env Configuration:**
```bash
# LLM Provider API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
HUGGINGFACE_API_KEY=hf_...

# Database (optional, defaults to SQLite)
TRULENS_DATABASE_URL=postgresql://user:pass@localhost/trulens

# Dashboard Port (optional)
TRULENS_PORT=8501

# Logging
TRULENS_LOG_LEVEL=INFO
```

### Initial Configuration

**Basic Setup:**
```python
from trulens_eval import Tru

# Initialize with default SQLite database
tru = Tru()

# Or with custom database
tru = Tru(database_url="postgresql://localhost/trulens")

# Reset database (development only)
tru.reset_database()
```

**Provider Setup:**
```python
from trulens_eval.feedback.provider.openai import OpenAI
from trulens_eval.feedback.provider.hugs import Huggingface
import os

# OpenAI provider
openai_provider = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_engine="gpt-4"
)

# Huggingface provider
hugs_provider = Huggingface(
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)
```

### Verification

**Test Installation:**
```python
from trulens_eval import Tru
from trulens_eval.feedback import Feedback
from trulens_eval.feedback.provider.openai import OpenAI

# Initialize
tru = Tru()
print(f"TruLens version: {tru.version}")

# Test feedback function
provider = OpenAI()
feedback = Feedback(provider.relevance).on_input_output()
print("Setup successful!")
```

---

## Core Concepts

### 1. Records and Traces

**Record**: Complete execution trace of a single application run

```python
from trulens_eval import TruChain

tru_chain = TruChain(chain, app_id="my_app")

with tru_chain as recording:
    result = chain.run("What is machine learning?")

# Access the record
record = recording.get()
print(f"Record ID: {record.record_id}")
print(f"Input: {record.main_input}")
print(f"Output: {record.main_output}")
print(f"Cost: ${record.cost.total_cost}")
print(f"Latency: {record.latency}s")
```

**Trace Structure:**
```python
# Records contain hierarchical trace data
record.calls  # List of all function calls
record.calls[0].stack  # Call stack
record.calls[0].args  # Arguments
record.calls[0].rets  # Return values
record.calls[0].perf  # Performance metrics
```

### 2. Feedback Functions

**Creating Feedback Functions:**

```python
from trulens_eval.feedback import Feedback
from trulens_eval.feedback.provider.openai import OpenAI

provider = OpenAI()

# Simple feedback on input/output
f_relevance = Feedback(
    provider.relevance,
    name="Answer Relevance"
).on_input_output()

# Feedback on specific parts using selectors
f_context_relevance = Feedback(
    provider.context_relevance,
    name="Context Relevance"
).on_input().on(
    TruChain.select_context()
).aggregate(np.mean)

# Custom feedback function
def custom_length_check(text: str) -> float:
    """Returns 1.0 if text is between 50-200 chars"""
    length = len(text)
    if 50 <= length <= 200:
        return 1.0
    return 0.0

f_length = Feedback(
    custom_length_check,
    name="Appropriate Length"
).on_output()
```

**Feedback Aggregation:**
```python
import numpy as np

# Aggregate multiple context relevance scores
f_context = Feedback(
    provider.context_relevance
).on_input().on(
    TruChain.select_context()
).aggregate(np.mean)  # or np.min, np.max, custom function
```

### 3. Selectors

**Path-based Selection:**

Selectors extract specific data from records:

```python
from trulens_eval.schema import Select

# Input and output
Select.RecordInput  # Main input
Select.RecordOutput  # Main output

# LangChain specific
TruChain.select_context()  # Retrieved context
TruChain.select_source_nodes()  # Source documents

# Custom paths
Select.RecordCalls.retriever.args.query  # Query to retriever
Select.RecordCalls.llm.rets  # LLM responses
```

**Using Selectors in Feedback:**
```python
# Feedback on retrieved context
f_context_rel = Feedback(
    provider.context_relevance
).on(Select.RecordInput).on(
    TruChain.select_context()
)

# Feedback on specific chain step
f_retrieval_quality = Feedback(
    custom_retrieval_scorer
).on(Select.RecordCalls.retriever.rets)
```

### 4. Providers

**Available Providers:**

```python
from trulens_eval.feedback.provider import OpenAI, AzureOpenAI
from trulens_eval.feedback.provider import Huggingface, LiteLLM
from trulens_eval.feedback.provider import Bedrock

# OpenAI
openai = OpenAI(model_engine="gpt-4")

# Azure OpenAI
azure = AzureOpenAI(
    deployment_name="gpt-4",
    api_version="2023-05-15"
)

# Huggingface
hugs = Huggingface(model_engine="facebook/bart-large-mnli")

# Bedrock
bedrock = Bedrock(model_id="anthropic.claude-v2")
```

**Provider Methods:**

Common feedback functions:
- `relevance(prompt, response)` - Answer relevance
- `sentiment(text)` - Sentiment analysis
- `moderation(text)` - Content moderation
- `context_relevance(question, context)` - Context quality
- `groundedness(source, statement)` - Factual grounding
- `coherence(text)` - Text coherence
- `conciseness(text)` - Response conciseness

### 5. Ground Truth

**Managing Golden Datasets:**

```python
from trulens_eval import Tru

tru = Tru()

# Add ground truth examples
tru.add_ground_truth(
    app_id="my_rag_app",
    input="What is machine learning?",
    expected_output="Machine learning is a subset of AI...",
    metadata={"category": "definitions"}
)

# Batch add from dataset
ground_truths = [
    {"input": "Q1", "expected_output": "A1"},
    {"input": "Q2", "expected_output": "A2"}
]

for gt in ground_truths:
    tru.add_ground_truth(
        app_id="my_rag_app",
        **gt
    )

# Retrieve ground truths
gts = tru.get_ground_truths(app_id="my_rag_app")
```

**Ground Truth Evaluation:**
```python
from trulens_eval.feedback import GroundTruthAgreement

# Create ground truth feedback
f_groundtruth = GroundTruthAgreement(
    ground_truth=tru.get_ground_truths(app_id="my_rag_app")
).on_input_output()

# Add to app
tru_app = TruChain(
    chain,
    app_id="my_rag_app",
    feedbacks=[f_groundtruth]
)
```

---

## Production-Ready Examples

### Example 1: Complete RAG Monitoring System

**Scenario:** Production RAG with comprehensive observability

```python
"""
Complete RAG monitoring with TruLens
- Automatic instrumentation
- Multiple feedback functions
- Real-time dashboard
- Cost tracking
"""

import os
import numpy as np
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

from trulens_eval import Tru, TruChain, Feedback
from trulens_eval.feedback.provider.openai import OpenAI
from trulens_eval.schema import FeedbackMode

# Initialize TruLens
tru = Tru()
tru.reset_database()

# Build RAG System
class ProductionRAG:
    def __init__(self, docs_path: str):
        # Load and process documents
        loader = DirectoryLoader(docs_path, glob="**/*.txt")
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)

        # Create vector store
        embeddings = OpenAIEmbeddings()
        self.vectorstore = FAISS.from_documents(texts, embeddings)

        # Create QA chain
        llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0
        )

        self.chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 4}
            ),
            return_source_documents=True
        )

    def query(self, question: str) -> dict:
        return self.chain({"query": question})

# Initialize RAG
rag = ProductionRAG("./knowledge_base")

# Setup Feedback Functions
provider = OpenAI()

# 1. Answer Relevance
f_answer_relevance = (
    Feedback(
        provider.relevance_with_cot_reasons,
        name="Answer Relevance"
    )
    .on_input()
    .on_output()
)

# 2. Context Relevance
f_context_relevance = (
    Feedback(
        provider.context_relevance_with_cot_reasons,
        name="Context Relevance"
    )
    .on_input()
    .on(TruChain.select_context())
    .aggregate(np.mean)
)

# 3. Groundedness
f_groundedness = (
    Feedback(
        provider.groundedness_measure_with_cot_reasons,
        name="Groundedness"
    )
    .on(TruChain.select_context())
    .on_output()
)

# 4. Custom: Answer Completeness
def answer_completeness(output: str) -> float:
    """Check if answer is complete (50-500 chars, ends with punctuation)"""
    if not output:
        return 0.0

    length = len(output)
    ends_properly = output.strip()[-1] in '.!?'

    length_score = 1.0 if 50 <= length <= 500 else 0.5
    ending_score = 1.0 if ends_properly else 0.7

    return (length_score + ending_score) / 2

f_completeness = (
    Feedback(
        answer_completeness,
        name="Answer Completeness"
    )
    .on_output()
)

# 5. Custom: Retrieval Diversity
def retrieval_diversity(context: list) -> float:
    """Measure diversity of retrieved documents"""
    if not context or len(context) < 2:
        return 1.0

    # Simple diversity: check for repeated content
    unique_content = set(c[:100] for c in context)
    return len(unique_content) / len(context)

f_diversity = (
    Feedback(
        retrieval_diversity,
        name="Retrieval Diversity"
    )
    .on(TruChain.select_context())
)

# Create TruChain with all feedbacks
tru_rag = TruChain(
    rag.chain,
    app_id="production_rag_v1",
    feedbacks=[
        f_answer_relevance,
        f_context_relevance,
        f_groundedness,
        f_completeness,
        f_diversity
    ],
    feedback_mode=FeedbackMode.WITH_APP  # Run feedback immediately
)

# Production Query Function
def query_with_monitoring(question: str) -> dict:
    """Query RAG with full monitoring"""
    with tru_rag as recording:
        result = rag.chain({"query": question})

    # Get record with feedback
    record = recording.get()

    # Log metrics
    print(f"\nQuery: {question}")
    print(f"Answer: {result['result'][:200]}...")
    print(f"\nMetrics:")
    print(f"  Cost: ${record.cost.total_cost:.4f}")
    print(f"  Latency: {record.latency:.2f}s")
    print(f"\nFeedback Scores:")

    feedback_results = tru.get_feedback(record_id=record.record_id)
    for fb in feedback_results:
        print(f"  {fb.name}: {fb.result:.3f}")

    return result

# Example queries
queries = [
    "What are the key features of our product?",
    "How do I troubleshoot connection issues?",
    "What's the pricing structure?",
    "Tell me about security features"
]

for query in queries:
    query_with_monitoring(query)
    print("\n" + "="*80 + "\n")

# Get aggregated metrics
records_df = tru.get_records_and_feedback(app_ids=["production_rag_v1"])
print("\nAggregated Metrics:")
print(records_df[[
    'app_id',
    'input',
    'output',
    'Answer Relevance',
    'Context Relevance',
    'Groundedness',
    'Answer Completeness',
    'Retrieval Diversity',
    'total_cost',
    'latency'
]].describe())

# Launch dashboard for visual analysis
print("\nLaunching dashboard...")
tru.run_dashboard()
```

### Example 2: Multi-Model RAG Comparison

**Scenario:** Compare different LLM models for RAG

```python
"""
Compare GPT-4, GPT-3.5, and Claude for RAG performance
"""

import os
from typing import List, Dict
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI, ChatAnthropic

from trulens_eval import Tru, TruChain, Feedback
from trulens_eval.feedback.provider.openai import OpenAI
import numpy as np

tru = Tru()

# Shared vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local("./vectorstore", embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Model configurations
models = {
    "gpt4": {
        "llm": ChatOpenAI(model_name="gpt-4", temperature=0),
        "app_id": "rag_gpt4"
    },
    "gpt35": {
        "llm": ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        "app_id": "rag_gpt35"
    },
    "claude": {
        "llm": ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0),
        "app_id": "rag_claude"
    }
}

# Create chains for each model
chains = {}
tru_chains = {}

provider = OpenAI()

# Setup feedback functions
feedbacks = [
    Feedback(provider.relevance, name="Relevance").on_input_output(),
    Feedback(provider.groundedness_measure_with_cot_reasons, name="Groundedness")
        .on(TruChain.select_context()).on_output(),
    Feedback(provider.context_relevance, name="Context Relevance")
        .on_input().on(TruChain.select_context()).aggregate(np.mean)
]

for model_name, config in models.items():
    # Create chain
    chain = RetrievalQA.from_chain_type(
        llm=config["llm"],
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    chains[model_name] = chain

    # Wrap with TruLens
    tru_chains[model_name] = TruChain(
        chain,
        app_id=config["app_id"],
        feedbacks=feedbacks
    )

# Test questions
test_questions = [
    "What is machine learning?",
    "Explain neural networks",
    "How does gradient descent work?",
    "What's the difference between supervised and unsupervised learning?",
    "Describe the transformer architecture"
]

# Run comparison
print("Running multi-model comparison...\n")

results = {model: [] for model in models.keys()}

for question in test_questions:
    print(f"Question: {question}")

    for model_name, tru_chain in tru_chains.items():
        with tru_chain as recording:
            result = chains[model_name]({"query": question})

        record = recording.get()
        results[model_name].append({
            "question": question,
            "answer": result["result"],
            "cost": record.cost.total_cost,
            "latency": record.latency,
            "record_id": record.record_id
        })

        print(f"  {model_name}: {result['result'][:100]}...")

    print()

# Analyze results
import pandas as pd

print("\n" + "="*80)
print("COMPARISON RESULTS")
print("="*80 + "\n")

for model_name in models.keys():
    print(f"\n{model_name.upper()} Performance:")

    df = tru.get_records_and_feedback(app_ids=[models[model_name]["app_id"]])

    print(f"  Average Relevance: {df['Relevance'].mean():.3f}")
    print(f"  Average Groundedness: {df['Groundedness'].mean():.3f}")
    print(f"  Average Context Relevance: {df['Context Relevance'].mean():.3f}")
    print(f"  Average Cost: ${df['total_cost'].mean():.4f}")
    print(f"  Average Latency: {df['latency'].mean():.2f}s")
    print(f"  Total Cost: ${df['total_cost'].sum():.4f}")

# Generate comparison report
comparison_df = pd.DataFrame()

for model_name in models.keys():
    df = tru.get_records_and_feedback(app_ids=[models[model_name]["app_id"]])
    model_summary = pd.DataFrame({
        'Model': [model_name],
        'Avg_Relevance': [df['Relevance'].mean()],
        'Avg_Groundedness': [df['Groundedness'].mean()],
        'Avg_Context_Relevance': [df['Context Relevance'].mean()],
        'Avg_Cost': [df['total_cost'].mean()],
        'Avg_Latency': [df['latency'].mean()],
        'Total_Cost': [df['total_cost'].sum()]
    })
    comparison_df = pd.concat([comparison_df, model_summary], ignore_index=True)

print("\n\nComparison Summary:")
print(comparison_df.to_string(index=False))

# Identify winner
comparison_df['Score'] = (
    comparison_df['Avg_Relevance'] * 0.3 +
    comparison_df['Avg_Groundedness'] * 0.3 +
    comparison_df['Avg_Context_Relevance'] * 0.2 -
    comparison_df['Avg_Cost'] * 10 -  # Penalize cost
    comparison_df['Avg_Latency'] * 0.05  # Penalize latency
)

winner = comparison_df.loc[comparison_df['Score'].idxmax()]
print(f"\n\nRecommended Model: {winner['Model']}")
print(f"  Quality Score: {winner['Score']:.3f}")
print(f"  Cost/Query: ${winner['Avg_Cost']:.4f}")
print(f"  Latency: {winner['Avg_Latency']:.2f}s")

# Launch dashboard
tru.run_dashboard()
```

### Example 3: Custom App Instrumentation

**Scenario:** Instrument a custom RAG application

```python
"""
Custom RAG implementation with TruLens instrumentation
"""

import os
from typing import List, Dict, Tuple
import openai
from trulens_eval import TruCustomApp, Tru, Feedback
from trulens_eval.tru_custom_app import instrument
from trulens_eval.feedback.provider.openai import OpenAI
import numpy as np

class CustomRAGSystem:
    """Custom RAG with full instrumentation"""

    def __init__(self, vector_db, embedding_model: str = "text-embedding-ada-002"):
        self.vector_db = vector_db
        self.embedding_model = embedding_model
        self.openai_client = openai.OpenAI()

    @instrument
    def embed_query(self, query: str) -> List[float]:
        """Embed query for retrieval"""
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=query
        )
        return response.data[0].embedding

    @instrument
    def retrieve_documents(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> List[Dict]:
        """Retrieve relevant documents"""
        # Simulate vector DB search
        results = self.vector_db.search(query_embedding, top_k=top_k)
        return results

    @instrument
    def rerank_documents(
        self,
        query: str,
        documents: List[Dict]
    ) -> List[Dict]:
        """Rerank documents for relevance"""
        # Simple reranking based on keyword overlap
        def score_doc(doc):
            query_words = set(query.lower().split())
            doc_words = set(doc['text'].lower().split())
            overlap = len(query_words & doc_words)
            return overlap

        scored_docs = [
            {**doc, 'rerank_score': score_doc(doc)}
            for doc in documents
        ]

        return sorted(
            scored_docs,
            key=lambda x: x['rerank_score'],
            reverse=True
        )

    @instrument
    def build_context(self, documents: List[Dict]) -> str:
        """Build context from documents"""
        context_parts = [
            f"Document {i+1}: {doc['text']}"
            for i, doc in enumerate(documents[:3])
        ]
        return "\n\n".join(context_parts)

    @instrument
    def generate_response(
        self,
        query: str,
        context: str
    ) -> str:
        """Generate response using LLM"""
        prompt = f"""Answer the question based on the provided context.

Context:
{context}

Question: {query}

Answer:"""

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        return response.choices[0].message.content

    @instrument
    def query(self, question: str) -> Tuple[str, Dict]:
        """Complete RAG pipeline"""
        # Embed query
        query_embedding = self.embed_query(question)

        # Retrieve documents
        documents = self.retrieve_documents(query_embedding, top_k=5)

        # Rerank
        reranked_docs = self.rerank_documents(question, documents)

        # Build context
        context = self.build_context(reranked_docs)

        # Generate response
        answer = self.generate_response(question, context)

        # Return answer and metadata
        metadata = {
            "num_docs_retrieved": len(documents),
            "num_docs_used": min(3, len(reranked_docs)),
            "top_rerank_score": reranked_docs[0]['rerank_score'] if reranked_docs else 0
        }

        return answer, metadata

# Mock vector DB for demo
class MockVectorDB:
    def __init__(self):
        self.documents = [
            {"id": 1, "text": "Machine learning is a subset of AI that learns from data."},
            {"id": 2, "text": "Neural networks are computing systems inspired by biological neural networks."},
            {"id": 3, "text": "Deep learning uses multi-layer neural networks for complex pattern recognition."},
            {"id": 4, "text": "Supervised learning trains on labeled data."},
            {"id": 5, "text": "Unsupervised learning finds patterns in unlabeled data."}
        ]

    def search(self, embedding: List[float], top_k: int = 5) -> List[Dict]:
        # Return random subset for demo
        import random
        return random.sample(self.documents, min(top_k, len(self.documents)))

# Initialize
tru = Tru()
vector_db = MockVectorDB()
rag_system = CustomRAGSystem(vector_db)

# Setup feedback functions
provider = OpenAI()

feedbacks = [
    Feedback(
        provider.relevance,
        name="Answer Relevance"
    ).on_input().on_output(),

    Feedback(
        provider.groundedness_measure_with_cot_reasons,
        name="Groundedness"
    ).on(
        CustomRAGSystem.build_context.rets  # Context from build_context
    ).on_output(),

    # Custom feedback on retrieval
    Feedback(
        lambda docs: len(docs) >= 3,  # At least 3 docs retrieved
        name="Sufficient Retrieval"
    ).on(CustomRAGSystem.retrieve_documents.rets),

    # Custom feedback on reranking
    Feedback(
        lambda docs: docs[0]['rerank_score'] > 0 if docs else False,
        name="Effective Reranking"
    ).on(CustomRAGSystem.rerank_documents.rets)
]

# Wrap with TruCustomApp
tru_rag = TruCustomApp(
    rag_system,
    app_id="custom_rag_instrumented",
    feedbacks=feedbacks
)

# Run queries
questions = [
    "What is machine learning?",
    "Explain neural networks",
    "What's the difference between supervised and unsupervised learning?"
]

print("Running Custom RAG with Full Instrumentation\n")

for question in questions:
    print(f"Question: {question}")

    with tru_rag as recording:
        answer, metadata = rag_system.query(question)

    record = recording.get()

    print(f"Answer: {answer}")
    print(f"Metadata: {metadata}")
    print(f"Cost: ${record.cost.total_cost:.4f}")
    print(f"Latency: {record.latency:.2f}s")

    # Get feedback
    feedback_results = tru.get_feedback(record_id=record.record_id)
    print("Feedback:")
    for fb in feedback_results:
        print(f"  {fb.name}: {fb.result}")

    print("\n" + "="*80 + "\n")

# Analyze all records
df = tru.get_records_and_feedback(app_ids=["custom_rag_instrumented"])
print("Summary Statistics:")
print(df[['Answer Relevance', 'Groundedness', 'total_cost', 'latency']].describe())

# Launch dashboard
tru.run_dashboard()
```

### Example 4: Feedback Function Deep Dive

**Scenario:** Comprehensive feedback function library

```python
"""
Complete catalog of TruLens feedback functions
"""

import numpy as np
from trulens_eval import Tru, TruChain, Feedback
from trulens_eval.feedback.provider.openai import OpenAI
from trulens_eval.feedback.provider.hugs import Huggingface
from trulens_eval.feedback import GroundTruthAgreement

tru = Tru()
openai_provider = OpenAI()
hugs_provider = Huggingface()

# ============================================================================
# CORE FEEDBACK FUNCTIONS
# ============================================================================

# 1. RELEVANCE: Does output address input?
f_relevance = Feedback(
    openai_provider.relevance,
    name="Relevance"
).on_input_output()

f_relevance_cot = Feedback(
    openai_provider.relevance_with_cot_reasons,
    name="Relevance with CoT"
).on_input_output()

# 2. GROUNDEDNESS: Is output supported by context?
f_groundedness = Feedback(
    openai_provider.groundedness_measure_with_cot_reasons,
    name="Groundedness"
).on(TruChain.select_context()).on_output()

# 3. CONTEXT RELEVANCE: Is context relevant to input?
f_context_relevance = Feedback(
    openai_provider.context_relevance,
    name="Context Relevance"
).on_input().on(TruChain.select_context()).aggregate(np.mean)

f_context_relevance_cot = Feedback(
    openai_provider.context_relevance_with_cot_reasons,
    name="Context Relevance with CoT"
).on_input().on(TruChain.select_context()).aggregate(np.mean)

# ============================================================================
# LANGUAGE QUALITY
# ============================================================================

# 4. COHERENCE: Is text logically coherent?
f_coherence = Feedback(
    openai_provider.coherence,
    name="Coherence"
).on_output()

f_coherence_cot = Feedback(
    openai_provider.coherence_with_cot_reasons,
    name="Coherence with CoT"
).on_output()

# 5. CONCISENESS: Is response appropriately concise?
f_conciseness = Feedback(
    openai_provider.conciseness,
    name="Conciseness"
).on_output()

f_conciseness_cot = Feedback(
    openai_provider.conciseness_with_cot_reasons,
    name="Conciseness with CoT"
).on_output()

# 6. CORRECTNESS: Is response factually correct?
f_correctness = Feedback(
    openai_provider.correctness,
    name="Correctness"
).on_input().on_output()

f_correctness_cot = Feedback(
    openai_provider.correctness_with_cot_reasons,
    name="Correctness with CoT"
).on_input().on_output()

# ============================================================================
# SENTIMENT & TONE
# ============================================================================

# 7. SENTIMENT: Positive, negative, or neutral?
f_sentiment = Feedback(
    openai_provider.sentiment,
    name="Sentiment"
).on_output()

f_sentiment_cot = Feedback(
    openai_provider.sentiment_with_cot_reasons,
    name="Sentiment with CoT"
).on_output()

# 8. MODERATION: Contains harmful content?
f_moderation = Feedback(
    openai_provider.moderation,
    name="Moderation"
).on_output()

# ============================================================================
# HUGGINGFACE MODELS
# ============================================================================

# 9. LANGUAGE MATCH: Is response in expected language?
f_language = Feedback(
    hugs_provider.language_match,
    name="Language Match"
).on_output()

# 10. TOXICITY: Using specialized toxicity model
f_toxicity = Feedback(
    hugs_provider.toxicity,
    name="Toxicity"
).on_output()

# 11. POSITIVE SENTIMENT: Using sentiment model
f_positive_sentiment = Feedback(
    hugs_provider.positive_sentiment,
    name="Positive Sentiment"
).on_output()

# ============================================================================
# CUSTOM FEEDBACK FUNCTIONS
# ============================================================================

# 12. LENGTH CHECK
def appropriate_length(text: str, min_len: int = 50, max_len: int = 500) -> float:
    """Check if text length is appropriate"""
    length = len(text)
    if min_len <= length <= max_len:
        return 1.0
    elif length < min_len:
        return length / min_len
    else:
        return max_len / length

f_length = Feedback(
    appropriate_length,
    name="Appropriate Length"
).on_output()

# 13. QUESTION ANSWERING COMPLETENESS
def qa_completeness(question: str, answer: str) -> float:
    """Check if answer addresses all parts of question"""
    # Simple heuristic: check for question words
    question_words = {'what', 'why', 'how', 'when', 'where', 'who'}
    q_lower = question.lower()

    questions_asked = sum(1 for qw in question_words if qw in q_lower)
    if questions_asked == 0:
        return 1.0

    # Check if answer has sufficient content
    answer_sentences = answer.count('.') + answer.count('!') + answer.count('?')

    # Heuristic: at least one sentence per question word
    return min(answer_sentences / questions_asked, 1.0)

f_qa_completeness = Feedback(
    qa_completeness,
    name="QA Completeness"
).on_input().on_output()

# 14. CODE DETECTION
def contains_code(text: str) -> float:
    """Detect if response contains code"""
    code_indicators = ['```', 'def ', 'class ', 'import ', 'function', '() {', '=>']
    return 1.0 if any(ind in text for ind in code_indicators) else 0.0

f_code_detection = Feedback(
    contains_code,
    name="Contains Code"
).on_output()

# 15. STRUCTURED FORMAT
def has_structured_format(text: str) -> float:
    """Check if response is well-structured"""
    # Check for lists, paragraphs, headers
    has_bullets = any(line.strip().startswith(('-', '*', '•'))
                     for line in text.split('\n'))
    has_numbers = any(line.strip()[0].isdigit() and line.strip()[1:3] in ['. ', ') ']
                     for line in text.split('\n') if line.strip())
    has_paragraphs = text.count('\n\n') >= 1

    structure_score = sum([has_bullets, has_numbers, has_paragraphs]) / 3
    return structure_score

f_structure = Feedback(
    has_structured_format,
    name="Structured Format"
).on_output()

# 16. CITATION CHECK
def has_citations(output: str, context: list) -> float:
    """Check if output references context"""
    if not context:
        return 1.0

    # Simple check: does output mention doc numbers or sources?
    citation_patterns = ['source', 'document', 'according to', 'references']
    has_citation_language = any(pattern in output.lower()
                                 for pattern in citation_patterns)

    return 1.0 if has_citation_language else 0.5

f_citations = Feedback(
    has_citations,
    name="Has Citations"
).on_output().on(TruChain.select_context())

# 17. RETRIEVAL QUALITY
def retrieval_quality(context: list, min_docs: int = 3) -> float:
    """Check if enough documents retrieved"""
    if not context:
        return 0.0

    num_docs = len(context)
    quality_score = min(num_docs / min_docs, 1.0)

    # Bonus for diversity (simple check)
    if num_docs >= 2:
        unique_starts = len(set(doc[:50] for doc in context))
        diversity_score = unique_starts / num_docs
        quality_score = (quality_score + diversity_score) / 2

    return quality_score

f_retrieval_quality = Feedback(
    retrieval_quality,
    name="Retrieval Quality"
).on(TruChain.select_context())

# 18. GROUND TRUTH COMPARISON
# Assumes ground truths are added to TruLens
f_ground_truth = GroundTruthAgreement(
    ground_truth=tru.get_ground_truths(),
    provider=openai_provider
).on_input_output()

# ============================================================================
# AGGREGATE FEEDBACK COLLECTIONS
# ============================================================================

# Collection 1: Basic RAG Evaluation
basic_rag_feedbacks = [
    f_relevance,
    f_groundedness,
    f_context_relevance
]

# Collection 2: Comprehensive Quality Assessment
comprehensive_feedbacks = [
    f_relevance_cot,
    f_groundedness,
    f_context_relevance_cot,
    f_coherence,
    f_correctness,
    f_qa_completeness,
    f_structure
]

# Collection 3: Safety & Moderation
safety_feedbacks = [
    f_moderation,
    f_toxicity,
    f_sentiment
]

# Collection 4: RAG-Specific
rag_specific_feedbacks = [
    f_context_relevance,
    f_groundedness,
    f_retrieval_quality,
    f_citations
]

# Collection 5: Production Monitoring
production_feedbacks = [
    f_relevance,
    f_groundedness,
    f_moderation,
    f_length,
    f_structure
]

print("Feedback Function Library Loaded")
print(f"Total feedback functions defined: 18")
print(f"Pre-configured collections: 5")
```

### Example 5: A/B Testing Framework

**Scenario:** A/B test different prompts and configurations

```python
"""
A/B testing framework for RAG configurations
"""

import os
from typing import List, Dict
from dataclasses import dataclass
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate

from trulens_eval import Tru, TruChain, Feedback
from trulens_eval.feedback.provider.openai import OpenAI
import numpy as np
import pandas as pd

@dataclass
class ExperimentConfig:
    """Configuration for an A/B test variant"""
    name: str
    app_id: str
    prompt_template: str
    temperature: float
    top_k: int
    model: str

class ABTestFramework:
    """Framework for running A/B tests on RAG configurations"""

    def __init__(self, vectorstore_path: str):
        self.tru = Tru()

        # Load shared vector store
        embeddings = OpenAIEmbeddings()
        self.vectorstore = FAISS.load_local(vectorstore_path, embeddings)

        # Setup feedback functions
        provider = OpenAI()
        self.feedbacks = [
            Feedback(provider.relevance, name="Relevance").on_input_output(),
            Feedback(provider.groundedness_measure_with_cot_reasons, name="Groundedness")
                .on(TruChain.select_context()).on_output(),
            Feedback(provider.context_relevance, name="Context Relevance")
                .on_input().on(TruChain.select_context()).aggregate(np.mean)
        ]

        self.experiments = {}
        self.results = {}

    def create_experiment(self, config: ExperimentConfig):
        """Create a new experiment variant"""

        # Create prompt
        prompt = PromptTemplate(
            template=config.prompt_template,
            input_variables=["context", "question"]
        )

        # Create LLM
        llm = ChatOpenAI(
            model_name=config.model,
            temperature=config.temperature
        )

        # Create retriever
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": config.top_k}
        )

        # Create chain
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

        # Wrap with TruLens
        tru_chain = TruChain(
            chain,
            app_id=config.app_id,
            feedbacks=self.feedbacks
        )

        self.experiments[config.name] = {
            "config": config,
            "chain": chain,
            "tru_chain": tru_chain
        }

    def run_experiment(self, test_questions: List[str]):
        """Run all experiments on test questions"""

        print(f"Running A/B Test with {len(self.experiments)} variants")
        print(f"Test questions: {len(test_questions)}\n")

        for variant_name, experiment in self.experiments.items():
            print(f"Testing variant: {variant_name}")

            tru_chain = experiment["tru_chain"]
            chain = experiment["chain"]
            results = []

            for question in test_questions:
                with tru_chain as recording:
                    result = chain({"query": question})

                record = recording.get()
                results.append({
                    "question": question,
                    "answer": result["result"],
                    "record_id": record.record_id,
                    "cost": record.cost.total_cost,
                    "latency": record.latency
                })

            self.results[variant_name] = results
            print(f"  Completed {len(results)} queries\n")

    def analyze_results(self) -> pd.DataFrame:
        """Analyze and compare experiment results"""

        comparison_data = []

        for variant_name, experiment in self.experiments.items():
            config = experiment["config"]
            app_id = config.app_id

            # Get records and feedback
            df = self.tru.get_records_and_feedback(app_ids=[app_id])

            # Calculate metrics
            variant_metrics = {
                "Variant": variant_name,
                "Model": config.model,
                "Temperature": config.temperature,
                "Top_K": config.top_k,
                "Avg_Relevance": df["Relevance"].mean(),
                "Avg_Groundedness": df["Groundedness"].mean(),
                "Avg_Context_Relevance": df["Context Relevance"].mean(),
                "Avg_Cost": df["total_cost"].mean(),
                "Avg_Latency": df["latency"].mean(),
                "Total_Cost": df["total_cost"].sum(),
                "Num_Queries": len(df)
            }

            comparison_data.append(variant_metrics)

        comparison_df = pd.DataFrame(comparison_data)

        # Calculate composite score
        comparison_df["Quality_Score"] = (
            comparison_df["Avg_Relevance"] * 0.35 +
            comparison_df["Avg_Groundedness"] * 0.35 +
            comparison_df["Avg_Context_Relevance"] * 0.30
        )

        # Calculate cost-adjusted score
        max_cost = comparison_df["Avg_Cost"].max()
        comparison_df["Cost_Efficiency"] = (
            1 - (comparison_df["Avg_Cost"] / max_cost)
        ) if max_cost > 0 else 1

        comparison_df["Overall_Score"] = (
            comparison_df["Quality_Score"] * 0.7 +
            comparison_df["Cost_Efficiency"] * 0.3
        )

        return comparison_df.sort_values("Overall_Score", ascending=False)

    def print_report(self):
        """Print comprehensive comparison report"""

        results_df = self.analyze_results()

        print("\n" + "="*100)
        print("A/B TEST RESULTS")
        print("="*100 + "\n")

        print("QUALITY METRICS:")
        print(results_df[[
            "Variant",
            "Avg_Relevance",
            "Avg_Groundedness",
            "Avg_Context_Relevance",
            "Quality_Score"
        ]].to_string(index=False))

        print("\n\nCOST & PERFORMANCE:")
        print(results_df[[
            "Variant",
            "Avg_Cost",
            "Total_Cost",
            "Avg_Latency",
            "Cost_Efficiency"
        ]].to_string(index=False))

        print("\n\nCONFIGURATION:")
        print(results_df[[
            "Variant",
            "Model",
            "Temperature",
            "Top_K"
        ]].to_string(index=False))

        print("\n\nOVERALL RANKING:")
        print(results_df[[
            "Variant",
            "Quality_Score",
            "Cost_Efficiency",
            "Overall_Score"
        ]].to_string(index=False))

        winner = results_df.iloc[0]
        print(f"\n\nRECOMMENDED VARIANT: {winner['Variant']}")
        print(f"  Quality Score: {winner['Quality_Score']:.3f}")
        print(f"  Cost Efficiency: {winner['Cost_Efficiency']:.3f}")
        print(f"  Overall Score: {winner['Overall_Score']:.3f}")
        print(f"  Avg Cost: ${winner['Avg_Cost']:.4f}")
        print(f"  Avg Latency: {winner['Avg_Latency']:.2f}s")

# Example usage
ab_test = ABTestFramework("./vectorstore")

# Define experiment variants
variants = [
    ExperimentConfig(
        name="baseline_gpt4",
        app_id="ab_test_baseline_gpt4",
        prompt_template="""Use the following context to answer the question.

Context: {context}

Question: {question}

Answer:""",
        temperature=0,
        top_k=3,
        model="gpt-4"
    ),

    ExperimentConfig(
        name="detailed_gpt4",
        app_id="ab_test_detailed_gpt4",
        prompt_template="""You are a helpful assistant. Use the provided context to give a detailed, well-structured answer.

Context: {context}

Question: {question}

Provide a comprehensive answer with:
1. Direct answer to the question
2. Supporting details from the context
3. Any relevant clarifications

Answer:""",
        temperature=0.3,
        top_k=5,
        model="gpt-4"
    ),

    ExperimentConfig(
        name="concise_gpt35",
        app_id="ab_test_concise_gpt35",
        prompt_template="""Answer briefly using the context.

Context: {context}

Question: {question}

Brief Answer:""",
        temperature=0,
        top_k=3,
        model="gpt-3.5-turbo"
    ),

    ExperimentConfig(
        name="balanced_gpt4",
        app_id="ab_test_balanced_gpt4",
        prompt_template="""Based on the context, provide a clear and accurate answer.

Context: {context}

Question: {question}

Answer (2-3 sentences):""",
        temperature=0.2,
        top_k=4,
        model="gpt-4"
    )
]

# Create experiments
for variant in variants:
    ab_test.create_experiment(variant)

# Test questions
test_questions = [
    "What is machine learning?",
    "How do neural networks work?",
    "Explain the concept of overfitting",
    "What's the difference between AI and ML?",
    "Describe supervised learning"
]

# Run experiments
ab_test.run_experiment(test_questions)

# Analyze and report
ab_test.print_report()

# Launch dashboard for visual comparison
ab_test.tru.run_dashboard()
```

### Example 6: Real-time Production Monitoring

**Scenario:** Production deployment with alerting

```python
"""
Production monitoring with alerts for RAG system
"""

import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

from trulens_eval import Tru, TruChain, Feedback
from trulens_eval.feedback.provider.openai import OpenAI
from trulens_eval.schema import FeedbackMode

@dataclass
class AlertThreshold:
    """Alert threshold configuration"""
    metric_name: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    window_size: int = 10  # Number of recent records to check

@dataclass
class Alert:
    """Alert information"""
    timestamp: datetime
    metric_name: str
    current_value: float
    threshold_value: float
    severity: str  # "warning" or "critical"
    message: str

class ProductionMonitor:
    """Production monitoring with alerting"""

    def __init__(
        self,
        app_id: str,
        alert_email: Optional[str] = None,
        smtp_config: Optional[Dict] = None
    ):
        self.app_id = app_id
        self.tru = Tru()
        self.alert_email = alert_email
        self.smtp_config = smtp_config
        self.alerts: List[Alert] = []

        # Setup feedback
        provider = OpenAI()
        self.feedbacks = [
            Feedback(provider.relevance, name="Relevance").on_input_output(),
            Feedback(provider.groundedness_measure_with_cot_reasons, name="Groundedness")
                .on(TruChain.select_context()).on_output(),
            Feedback(provider.moderation, name="Safety").on_output()
        ]

        # Default alert thresholds
        self.thresholds = [
            AlertThreshold("Relevance", min_value=0.7),
            AlertThreshold("Groundedness", min_value=0.7),
            AlertThreshold("Safety", min_value=0.9),
            AlertThreshold("total_cost", max_value=0.10),
            AlertThreshold("latency", max_value=5.0)
        ]

    def create_monitored_chain(self, chain):
        """Wrap chain with monitoring"""
        return TruChain(
            chain,
            app_id=self.app_id,
            feedbacks=self.feedbacks,
            feedback_mode=FeedbackMode.WITH_APP
        )

    def check_thresholds(self):
        """Check if recent records violate thresholds"""

        # Get recent records
        df = self.tru.get_records_and_feedback(app_ids=[self.app_id])

        if df.empty:
            return

        # Check each threshold
        for threshold in self.thresholds:
            recent_records = df.tail(threshold.window_size)

            if threshold.metric_name not in recent_records.columns:
                continue

            metric_values = recent_records[threshold.metric_name].dropna()

            if metric_values.empty:
                continue

            avg_value = metric_values.mean()

            # Check min threshold
            if threshold.min_value is not None and avg_value < threshold.min_value:
                severity = "critical" if avg_value < threshold.min_value * 0.8 else "warning"
                alert = Alert(
                    timestamp=datetime.now(),
                    metric_name=threshold.metric_name,
                    current_value=avg_value,
                    threshold_value=threshold.min_value,
                    severity=severity,
                    message=f"{threshold.metric_name} below threshold: {avg_value:.3f} < {threshold.min_value}"
                )
                self.alerts.append(alert)
                self._send_alert(alert)

            # Check max threshold
            if threshold.max_value is not None and avg_value > threshold.max_value:
                severity = "critical" if avg_value > threshold.max_value * 1.5 else "warning"
                alert = Alert(
                    timestamp=datetime.now(),
                    metric_name=threshold.metric_name,
                    current_value=avg_value,
                    threshold_value=threshold.max_value,
                    severity=severity,
                    message=f"{threshold.metric_name} above threshold: {avg_value:.3f} > {threshold.max_value}"
                )
                self.alerts.append(alert)
                self._send_alert(alert)

    def _send_alert(self, alert: Alert):
        """Send alert notification"""

        print(f"\n{'='*80}")
        print(f"ALERT [{alert.severity.upper()}] - {alert.timestamp}")
        print(f"{'='*80}")
        print(alert.message)
        print(f"Current Value: {alert.current_value:.3f}")
        print(f"Threshold: {alert.threshold_value:.3f}")
        print(f"{'='*80}\n")

        # Send email if configured
        if self.alert_email and self.smtp_config:
            try:
                self._send_email_alert(alert)
            except Exception as e:
                print(f"Failed to send email alert: {e}")

    def _send_email_alert(self, alert: Alert):
        """Send email notification"""

        subject = f"[{alert.severity.upper()}] RAG System Alert: {alert.metric_name}"

        body = f"""
Alert Details:
--------------
Timestamp: {alert.timestamp}
App ID: {self.app_id}
Metric: {alert.metric_name}
Current Value: {alert.current_value:.3f}
Threshold: {alert.threshold_value:.3f}
Severity: {alert.severity}

Message: {alert.message}

Please investigate and take corrective action.
"""

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.smtp_config["from"]
        msg["To"] = self.alert_email

        with smtplib.SMTP(self.smtp_config["host"], self.smtp_config["port"]) as server:
            if self.smtp_config.get("use_tls"):
                server.starttls()
            if self.smtp_config.get("username"):
                server.login(
                    self.smtp_config["username"],
                    self.smtp_config["password"]
                )
            server.send_message(msg)

    def get_health_status(self) -> Dict:
        """Get current system health status"""

        df = self.tru.get_records_and_feedback(app_ids=[self.app_id])

        if df.empty:
            return {"status": "unknown", "message": "No data available"}

        # Check recent performance
        recent = df.tail(20)

        health = {
            "status": "healthy",
            "timestamp": datetime.now(),
            "total_queries": len(df),
            "recent_queries": len(recent),
            "metrics": {}
        }

        # Check each metric
        for threshold in self.thresholds:
            if threshold.metric_name not in recent.columns:
                continue

            values = recent[threshold.metric_name].dropna()
            if values.empty:
                continue

            avg_value = values.mean()
            health["metrics"][threshold.metric_name] = {
                "current": avg_value,
                "min_threshold": threshold.min_value,
                "max_threshold": threshold.max_value
            }

            # Check health
            if threshold.min_value and avg_value < threshold.min_value:
                health["status"] = "degraded"
            if threshold.max_value and avg_value > threshold.max_value:
                health["status"] = "degraded"

        # Check for critical issues
        critical_alerts = [a for a in self.alerts[-10:] if a.severity == "critical"]
        if critical_alerts:
            health["status"] = "critical"
            health["critical_alerts"] = len(critical_alerts)

        return health

    def generate_report(self) -> str:
        """Generate monitoring report"""

        df = self.tru.get_records_and_feedback(app_ids=[self.app_id])
        health = self.get_health_status()

        report = f"""
{'='*80}
PRODUCTION MONITORING REPORT
{'='*80}

App ID: {self.app_id}
Report Time: {datetime.now()}
System Status: {health['status'].upper()}

QUERY STATISTICS:
-----------------
Total Queries: {health.get('total_queries', 0)}
Recent Queries (last 20): {health.get('recent_queries', 0)}

PERFORMANCE METRICS:
--------------------
"""

        for metric_name, metric_data in health.get("metrics", {}).items():
            report += f"\n{metric_name}:"
            report += f"\n  Current Avg: {metric_data['current']:.3f}"
            if metric_data['min_threshold']:
                report += f"\n  Min Threshold: {metric_data['min_threshold']:.3f}"
            if metric_data['max_threshold']:
                report += f"\n  Max Threshold: {metric_data['max_threshold']:.3f}"
            report += "\n"

        # Recent alerts
        recent_alerts = self.alerts[-5:]
        if recent_alerts:
            report += "\nRECENT ALERTS:\n--------------\n"
            for alert in recent_alerts:
                report += f"\n[{alert.severity.upper()}] {alert.timestamp}"
                report += f"\n  {alert.message}\n"

        report += f"\n{'='*80}\n"

        return report

# Example usage
def main():
    # Initialize monitor
    monitor = ProductionMonitor(
        app_id="production_rag_v1",
        alert_email="team@company.com",
        smtp_config={
            "host": "smtp.gmail.com",
            "port": 587,
            "use_tls": True,
            "from": "alerts@company.com",
            "username": os.getenv("SMTP_USER"),
            "password": os.getenv("SMTP_PASS")
        }
    )

    # Setup RAG chain
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local("./vectorstore", embeddings)

    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )

    # Create monitored chain
    monitored_chain = monitor.create_monitored_chain(chain)

    # Simulate production queries
    queries = [
        "What is machine learning?",
        "Explain neural networks",
        "How does backpropagation work?",
        "What's the difference between AI and ML?",
        "Describe deep learning"
    ]

    print("Running production queries with monitoring...")

    for i, query in enumerate(queries):
        print(f"\nQuery {i+1}/{len(queries)}: {query}")

        with monitored_chain as recording:
            result = chain({"query": query})

        print(f"Answer: {result['result'][:100]}...")

        # Check thresholds after each query
        monitor.check_thresholds()

    # Generate and print report
    print(monitor.generate_report())

    # Check health status
    health = monitor.get_health_status()
    print(f"\nFinal Health Status: {health['status']}")

    # Launch dashboard
    monitor.tru.run_dashboard()

if __name__ == "__main__":
    main()
```

### Example 7: LlamaIndex Integration

**Scenario:** TruLens with LlamaIndex for advanced RAG

```python
"""
TruLens integration with LlamaIndex
"""

import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage
)
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever

from trulens_eval import Tru, TruLlama, Feedback
from trulens_eval.feedback.provider.openai import OpenAI
import numpy as np

class LlamaIndexRAG:
    """Advanced RAG with LlamaIndex and TruLens"""

    def __init__(self, docs_path: str, persist_dir: str = "./storage"):
        self.tru = Tru()
        self.persist_dir = persist_dir

        # Setup LLM and embeddings
        llm = LlamaOpenAI(model="gpt-4", temperature=0)
        embed_model = OpenAIEmbedding()

        # Create service context
        self.service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
            node_parser=SimpleNodeParser.from_defaults(chunk_size=512)
        )

        # Load or create index
        if os.path.exists(persist_dir):
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
            self.index = load_index_from_storage(
                storage_context,
                service_context=self.service_context
            )
            print("Loaded existing index")
        else:
            documents = SimpleDirectoryReader(docs_path).load_data()
            self.index = VectorStoreIndex.from_documents(
                documents,
                service_context=self.service_context
            )
            self.index.storage_context.persist(persist_dir=persist_dir)
            print("Created new index")

    def create_query_engine(
        self,
        similarity_top_k: int = 3,
        response_mode: str = "compact"
    ):
        """Create query engine with custom settings"""

        # Create retriever
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=similarity_top_k
        )

        # Create response synthesizer
        response_synthesizer = get_response_synthesizer(
            service_context=self.service_context,
            response_mode=response_mode
        )

        # Create query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer
        )

        return query_engine

    def create_monitored_engine(
        self,
        app_id: str,
        similarity_top_k: int = 3,
        response_mode: str = "compact"
    ):
        """Create query engine with TruLens monitoring"""

        query_engine = self.create_query_engine(
            similarity_top_k=similarity_top_k,
            response_mode=response_mode
        )

        # Setup feedback functions
        provider = OpenAI()

        feedbacks = [
            Feedback(
                provider.relevance,
                name="Answer Relevance"
            ).on_input_output(),

            Feedback(
                provider.context_relevance_with_cot_reasons,
                name="Context Relevance"
            ).on_input().on(
                TruLlama.select_source_nodes()
            ).aggregate(np.mean),

            Feedback(
                provider.groundedness_measure_with_cot_reasons,
                name="Groundedness"
            ).on(
                TruLlama.select_source_nodes()
            ).on_output()
        ]

        # Wrap with TruLens
        tru_query_engine = TruLlama(
            query_engine,
            app_id=app_id,
            feedbacks=feedbacks
        )

        return tru_query_engine, query_engine

# Example usage
def main():
    # Initialize RAG
    rag = LlamaIndexRAG(docs_path="./documents")

    # Create monitored engines with different configurations
    configs = [
        {"app_id": "llama_compact_k3", "similarity_top_k": 3, "response_mode": "compact"},
        {"app_id": "llama_refine_k5", "similarity_top_k": 5, "response_mode": "refine"},
        {"app_id": "llama_tree_k4", "similarity_top_k": 4, "response_mode": "tree_summarize"}
    ]

    engines = {}
    for config in configs:
        tru_engine, engine = rag.create_monitored_engine(**config)
        engines[config["app_id"]] = {"tru_engine": tru_engine, "engine": engine}

    # Test questions
    questions = [
        "What are the main concepts in machine learning?",
        "Explain how neural networks learn",
        "What is the purpose of backpropagation?"
    ]

    # Run queries on all engines
    for question in questions:
        print(f"\n{'='*80}")
        print(f"Question: {question}")
        print(f"{'='*80}\n")

        for app_id, eng_dict in engines.items():
            print(f"\nConfiguration: {app_id}")

            tru_engine = eng_dict["tru_engine"]
            engine = eng_dict["engine"]

            with tru_engine as recording:
                response = engine.query(question)

            record = recording.get()

            print(f"Answer: {response.response[:200]}...")
            print(f"Sources: {len(response.source_nodes)} nodes")
            print(f"Cost: ${record.cost.total_cost:.4f}")
            print(f"Latency: {record.latency:.2f}s")

    # Compare results
    print("\n\n" + "="*80)
    print("CONFIGURATION COMPARISON")
    print("="*80 + "\n")

    for app_id in [c["app_id"] for c in configs]:
        df = rag.tru.get_records_and_feedback(app_ids=[app_id])
        print(f"\n{app_id}:")
        print(f"  Avg Answer Relevance: {df['Answer Relevance'].mean():.3f}")
        print(f"  Avg Context Relevance: {df['Context Relevance'].mean():.3f}")
        print(f"  Avg Groundedness: {df['Groundedness'].mean():.3f}")
        print(f"  Avg Cost: ${df['total_cost'].mean():.4f}")
        print(f"  Avg Latency: {df['latency'].mean():.2f}s")

    # Launch dashboard
    rag.tru.run_dashboard()

if __name__ == "__main__":
    main()
```

### Example 8: Advanced Custom Feedback Functions

**Scenario:** Domain-specific feedback functions

```python
"""
Advanced custom feedback functions for specific domains
"""

import re
from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from trulens_eval import Tru, TruChain, Feedback
from trulens_eval.feedback.provider.openai import OpenAI

# ============================================================================
# MEDICAL DOMAIN FEEDBACK FUNCTIONS
# ============================================================================

class MedicalFeedback:
    """Feedback functions for medical/healthcare RAG"""

    @staticmethod
    def contains_disclaimer(response: str) -> float:
        """Check if medical advice includes appropriate disclaimer"""
        disclaimer_phrases = [
            "consult",
            "doctor",
            "physician",
            "healthcare provider",
            "medical professional",
            "not a substitute for",
            "seek medical advice"
        ]

        response_lower = response.lower()
        disclaimer_count = sum(
            1 for phrase in disclaimer_phrases
            if phrase in response_lower
        )

        # At least 2 disclaimer phrases
        return min(disclaimer_count / 2.0, 1.0)

    @staticmethod
    def avoids_definitive_diagnosis(response: str) -> float:
        """Check that response avoids definitive medical diagnosis"""
        problematic_phrases = [
            "you have",
            "you definitely",
            "you are diagnosed",
            "you must have"
        ]

        response_lower = response.lower()
        has_problematic = any(
            phrase in response_lower
            for phrase in problematic_phrases
        )

        return 0.0 if has_problematic else 1.0

    @staticmethod
    def cites_medical_sources(output: str, context: List[str]) -> float:
        """Check if response cites medical context appropriately"""
        if not context:
            return 0.5

        # Check for citation indicators
        citation_patterns = [
            r"according to",
            r"studies show",
            r"research indicates",
            r"based on",
            r"evidence suggests"
        ]

        has_citations = any(
            re.search(pattern, output, re.IGNORECASE)
            for pattern in citation_patterns
        )

        return 1.0 if has_citations else 0.6

# ============================================================================
# LEGAL DOMAIN FEEDBACK FUNCTIONS
# ============================================================================

class LegalFeedback:
    """Feedback functions for legal RAG"""

    @staticmethod
    def contains_legal_disclaimer(response: str) -> float:
        """Check for legal disclaimer"""
        disclaimer_phrases = [
            "not legal advice",
            "consult an attorney",
            "consult a lawyer",
            "for informational purposes",
            "seek legal counsel"
        ]

        response_lower = response.lower()
        has_disclaimer = any(
            phrase in response_lower
            for phrase in disclaimer_phrases
        )

        return 1.0 if has_disclaimer else 0.0

    @staticmethod
    def cites_statutes(response: str) -> float:
        """Check if response cites specific statutes or codes"""
        # Look for statute patterns: § 123, USC 456, CFR 789
        statute_patterns = [
            r'§\s*\d+',
            r'\d+\s+U\.?S\.?C\.?\s+\d+',
            r'\d+\s+CFR\s+\d+',
            r'Section\s+\d+'
        ]

        citations_found = sum(
            len(re.findall(pattern, response, re.IGNORECASE))
            for pattern in statute_patterns
        )

        return min(citations_found / 2.0, 1.0)

    @staticmethod
    def avoids_specific_advice(response: str) -> float:
        """Ensure no specific legal advice is given"""
        advice_phrases = [
            "you should",
            "you must",
            "i recommend you",
            "i advise you"
        ]

        response_lower = response.lower()
        gives_advice = any(
            phrase in response_lower
            for phrase in advice_phrases
        )

        return 0.0 if gives_advice else 1.0

# ============================================================================
# FINANCIAL DOMAIN FEEDBACK FUNCTIONS
# ============================================================================

class FinancialFeedback:
    """Feedback functions for financial RAG"""

    @staticmethod
    def contains_risk_disclosure(response: str) -> float:
        """Check for investment risk disclosure"""
        risk_phrases = [
            "past performance",
            "not guarantee",
            "risk",
            "may lose",
            "consult a financial advisor",
            "not financial advice"
        ]

        response_lower = response.lower()
        risk_mentions = sum(
            1 for phrase in risk_phrases
            if phrase in response_lower
        )

        return min(risk_mentions / 2.0, 1.0)

    @staticmethod
    def includes_numbers_correctly(response: str) -> float:
        """Check that financial numbers are formatted correctly"""
        # Find all numbers in response
        numbers = re.findall(r'\$?[\d,]+\.?\d*%?', response)

        if not numbers:
            return 1.0  # No numbers to check

        # Check formatting
        correctly_formatted = 0
        for num in numbers:
            # Check for proper comma placement in thousands
            if ',' in num:
                # Should be every 3 digits
                parts = num.replace('$', '').replace('%', '').split(',')
                if all(len(part) == 3 for part in parts[1:]):
                    correctly_formatted += 1
            else:
                correctly_formatted += 1

        return correctly_formatted / len(numbers)

    @staticmethod
    def appropriate_timeframe_context(response: str) -> float:
        """Check if financial information includes timeframe"""
        timeframe_indicators = [
            'year',
            'month',
            'quarter',
            'annually',
            'monthly',
            'as of',
            '202',  # Year indicator
            'current',
            'recent'
        ]

        response_lower = response.lower()
        has_timeframe = any(
            indicator in response_lower
            for indicator in timeframe_indicators
        )

        return 1.0 if has_timeframe else 0.5

# ============================================================================
# TECHNICAL DOCUMENTATION FEEDBACK FUNCTIONS
# ============================================================================

class TechnicalFeedback:
    """Feedback functions for technical documentation RAG"""

    @staticmethod
    def includes_code_examples(response: str) -> float:
        """Check if technical response includes code examples"""
        code_indicators = [
            '```',
            'example:',
            'for example',
            '`',
            'def ',
            'class ',
            'function'
        ]

        has_code = any(
            indicator in response.lower()
            for indicator in code_indicators
        )

        return 1.0 if has_code else 0.5

    @staticmethod
    def proper_code_formatting(response: str) -> float:
        """Check if code blocks are properly formatted"""
        code_blocks = re.findall(r'```[\s\S]*?```', response)

        if not code_blocks:
            return 1.0  # No code blocks to check

        properly_formatted = sum(
            1 for block in code_blocks
            if '\n' in block  # Multi-line code blocks
        )

        return properly_formatted / len(code_blocks)

    @staticmethod
    def includes_step_by_step(response: str) -> float:
        """Check for step-by-step instructions"""
        # Look for numbered steps or bullet points
        has_numbers = bool(re.search(r'^\s*\d+[\.\)]\s+', response, re.MULTILINE))
        has_bullets = bool(re.search(r'^\s*[-*•]\s+', response, re.MULTILINE))

        if has_numbers or has_bullets:
            # Count steps
            steps = len(re.findall(r'^\s*[\d\-*•]+[\.\)]*\s+', response, re.MULTILINE))
            return min(steps / 3.0, 1.0)  # Expect at least 3 steps

        return 0.5

    @staticmethod
    def appropriate_technical_depth(
        question: str,
        response: str
    ) -> float:
        """Ensure response matches technical depth of question"""
        # Simple heuristic: advanced questions should get detailed answers
        advanced_indicators = [
            'how does',
            'explain',
            'architecture',
            'implementation',
            'internal',
            'advanced'
        ]

        question_lower = question.lower()
        is_advanced = any(
            indicator in question_lower
            for indicator in advanced_indicators
        )

        if is_advanced:
            # Expect detailed response (longer, with technical terms)
            technical_terms = len(re.findall(
                r'\b[a-z]+(?:[A-Z][a-z]*)+\b',  # camelCase or PascalCase
                response
            ))
            word_count = len(response.split())

            detail_score = min(word_count / 200, 1.0)
            technical_score = min(technical_terms / 5, 1.0)

            return (detail_score + technical_score) / 2

        return 1.0  # Basic questions are fine with any length

# ============================================================================
# SEMANTIC SIMILARITY FEEDBACK
# ============================================================================

class SemanticFeedback:
    """Advanced semantic similarity feedback"""

    @staticmethod
    def answer_context_alignment(
        answer: str,
        context: List[str],
        threshold: float = 0.3
    ) -> float:
        """Measure semantic alignment between answer and context"""
        if not context:
            return 0.5

        try:
            # Combine all context
            combined_context = " ".join(context)

            # Calculate TF-IDF similarity
            vectorizer = TfidfVectorizer(max_features=100)
            tfidf_matrix = vectorizer.fit_transform([combined_context, answer])

            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

            # Normalize above threshold
            if similarity < threshold:
                return 0.0

            return min((similarity - threshold) / (1 - threshold), 1.0)

        except:
            return 0.5

    @staticmethod
    def query_answer_semantic_match(
        query: str,
        answer: str
    ) -> float:
        """Measure how well answer semantically matches query intent"""
        try:
            vectorizer = TfidfVectorizer(max_features=50)
            tfidf_matrix = vectorizer.fit_transform([query, answer])

            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

            return similarity

        except:
            return 0.5

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def create_domain_specific_feedbacks(domain: str) -> List[Feedback]:
    """Create feedback functions for specific domain"""

    if domain == "medical":
        return [
            Feedback(
                MedicalFeedback.contains_disclaimer,
                name="Medical Disclaimer"
            ).on_output(),

            Feedback(
                MedicalFeedback.avoids_definitive_diagnosis,
                name="Avoids Diagnosis"
            ).on_output(),

            Feedback(
                MedicalFeedback.cites_medical_sources,
                name="Cites Sources"
            ).on_output().on(TruChain.select_context())
        ]

    elif domain == "legal":
        return [
            Feedback(
                LegalFeedback.contains_legal_disclaimer,
                name="Legal Disclaimer"
            ).on_output(),

            Feedback(
                LegalFeedback.cites_statutes,
                name="Cites Statutes"
            ).on_output(),

            Feedback(
                LegalFeedback.avoids_specific_advice,
                name="Avoids Specific Advice"
            ).on_output()
        ]

    elif domain == "financial":
        return [
            Feedback(
                FinancialFeedback.contains_risk_disclosure,
                name="Risk Disclosure"
            ).on_output(),

            Feedback(
                FinancialFeedback.includes_numbers_correctly,
                name="Number Formatting"
            ).on_output(),

            Feedback(
                FinancialFeedback.appropriate_timeframe_context,
                name="Timeframe Context"
            ).on_output()
        ]

    elif domain == "technical":
        return [
            Feedback(
                TechnicalFeedback.includes_code_examples,
                name="Code Examples"
            ).on_output(),

            Feedback(
                TechnicalFeedback.proper_code_formatting,
                name="Code Formatting"
            ).on_output(),

            Feedback(
                TechnicalFeedback.includes_step_by_step,
                name="Step-by-Step"
            ).on_output(),

            Feedback(
                TechnicalFeedback.appropriate_technical_depth,
                name="Technical Depth"
            ).on_input().on_output()
        ]

    else:
        raise ValueError(f"Unknown domain: {domain}")

# Demo
if __name__ == "__main__":
    print("Domain-Specific Feedback Functions Loaded")
    print("\nAvailable domains:")
    print("  - medical")
    print("  - legal")
    print("  - financial")
    print("  - technical")

    # Example: Create medical feedback functions
    medical_feedbacks = create_domain_specific_feedbacks("medical")
    print(f"\nMedical domain feedback functions: {len(medical_feedbacks)}")
    for fb in medical_feedbacks:
        print(f"  - {fb.name}")
```

---

## Advanced Usage

### Custom Provider Implementation

Create custom feedback provider:

```python
from trulens_eval.feedback.provider.base import LLMProvider

class CustomProvider(LLMProvider):
    """Custom feedback provider"""

    def __init__(self, model_url: str, api_key: str):
        self.model_url = model_url
        self.api_key = api_key

    def _create_chat_completion(
        self,
        prompt: str,
        **kwargs
    ) -> str:
        """Call custom LLM API"""
        # Implementation here
        pass

    def relevance(self, prompt: str, response: str) -> float:
        """Custom relevance implementation"""
        eval_prompt = f"""
        Rate the relevance of the response to the prompt on a scale of 0-1.

        Prompt: {prompt}
        Response: {response}

        Relevance score:"""

        result = self._create_chat_completion(eval_prompt)
        return float(result.strip())
```

### Batch Evaluation

Evaluate large datasets:

```python
from trulens_eval import Tru
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

def batch_evaluate(
    app_chain,
    test_cases: pd.DataFrame,
    max_workers: int = 5
):
    """Batch evaluate test cases"""

    tru = Tru()

    def evaluate_single(row):
        with app_chain as recording:
            result = app_chain.app({"query": row["input"]})
        return recording.get()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        records = list(executor.map(evaluate_single, test_cases.iterrows()))

    return tru.get_records_and_feedback(app_ids=[app_chain.app_id])
```

### Database Management

Custom database configuration:

```python
from trulens_eval import Tru
from sqlalchemy import create_engine

# PostgreSQL for production
database_url = "postgresql://user:pass@localhost:5432/trulens"
tru = Tru(database_url=database_url)

# Custom engine configuration
engine = create_engine(
    database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

tru = Tru(database_engine=engine)

# Database operations
tru.reset_database()  # Clear all data
tru.migrate_database()  # Apply migrations
```

### Dashboard Customization

Configure dashboard:

```python
from trulens_eval import Tru

tru = Tru()

# Launch with custom configuration
tru.run_dashboard(
    port=8080,
    force=True,  # Force start even if port in use
    _dev="path/to/dev/dashboard"  # Use development dashboard
)
```

---

## Best Practices

### 1. Instrumentation Strategy

**Start Minimal, Expand Gradually:**

```python
# Phase 1: Basic instrumentation
feedbacks_phase1 = [
    Feedback(provider.relevance).on_input_output()
]

# Phase 2: Add RAG-specific
feedbacks_phase2 = feedbacks_phase1 + [
    Feedback(provider.groundedness).on(context).on_output(),
    Feedback(provider.context_relevance).on_input().on(context)
]

# Phase 3: Add custom domain feedback
feedbacks_phase3 = feedbacks_phase2 + custom_feedbacks
```

### 2. Feedback Function Selection

**Choose Based on Use Case:**

- **RAG Systems**: groundedness, context_relevance, answer_relevance
- **Conversational**: coherence, sentiment, appropriateness
- **Safety-Critical**: moderation, toxicity, bias
- **Production**: relevance, latency, cost

### 3. Performance Optimization

**Async Feedback Execution:**

```python
from trulens_eval.schema import FeedbackMode

# Run feedback asynchronously
tru_chain = TruChain(
    chain,
    app_id="async_app",
    feedbacks=feedbacks,
    feedback_mode=FeedbackMode.DEFERRED  # Don't block on feedback
)
```

**Batch Processing:**

```python
# Process feedback in batches
tru.run_feedback_functions(
    record_ids=record_ids,
    feedback_functions=feedbacks
)
```

### 4. Cost Management

**Track and Budget:**

```python
# Monitor costs
records_df = tru.get_records_and_feedback(app_ids=["my_app"])

total_cost = records_df["total_cost"].sum()
avg_cost_per_query = records_df["total_cost"].mean()

print(f"Total Cost: ${total_cost:.2f}")
print(f"Avg Cost/Query: ${avg_cost_per_query:.4f}")

# Set cost alerts
if avg_cost_per_query > 0.10:
    alert("High cost per query!")
```

### 5. Data Management

**Regular Cleanup:**

```python
from datetime import datetime, timedelta

# Delete old records
cutoff_date = datetime.now() - timedelta(days=30)

# Get old records
old_records = tru.db.query_records(
    filter_timestamp_before=cutoff_date
)

# Archive before deleting
tru.export_records(old_records, "archive.json")

# Delete
for record in old_records:
    tru.delete_record(record.record_id)
```

### 6. Testing Strategy

**Staged Rollout:**

```python
# 1. Development: All feedback, detailed logging
dev_tru_chain = TruChain(
    chain,
    app_id="dev",
    feedbacks=all_feedbacks,
    feedback_mode=FeedbackMode.WITH_APP
)

# 2. Staging: Essential feedback only
staging_tru_chain = TruChain(
    chain,
    app_id="staging",
    feedbacks=essential_feedbacks,
    feedback_mode=FeedbackMode.WITH_APP
)

# 3. Production: Deferred feedback
prod_tru_chain = TruChain(
    chain,
    app_id="prod",
    feedbacks=prod_feedbacks,
    feedback_mode=FeedbackMode.DEFERRED
)
```

---

## Integration Guide

### LangChain Integration

```python
from langchain.chains import LLMChain, SequentialChain
from trulens_eval import TruChain

# Simple chain
llm_chain = LLMChain(llm=llm, prompt=prompt)
tru_chain = TruChain(llm_chain, app_id="simple_chain")

# Sequential chain
sequential = SequentialChain(chains=[chain1, chain2])
tru_sequential = TruChain(sequential, app_id="sequential")

# Agent
from langchain.agents import create_react_agent
agent = create_react_agent(llm, tools, prompt)
tru_agent = TruChain(agent, app_id="agent")
```

### LlamaIndex Integration

```python
from llama_index.core import VectorStoreIndex
from trulens_eval import TruLlama

# Query engine
query_engine = index.as_query_engine()
tru_query_engine = TruLlama(query_engine, app_id="llama_app")

# Chat engine
chat_engine = index.as_chat_engine()
tru_chat_engine = TruLlama(chat_engine, app_id="llama_chat")
```

### FastAPI Integration

```python
from fastapi import FastAPI
from trulens_eval import Tru, TruChain

app = FastAPI()
tru = Tru()

@app.post("/query")
async def query_endpoint(question: str):
    with tru_chain as recording:
        result = chain({"query": question})

    record = recording.get()

    return {
        "answer": result["result"],
        "record_id": record.record_id,
        "cost": record.cost.total_cost
    }
```

---

## Troubleshooting

### Common Issues

**Issue: Selectors not working**

```python
# Wrong: Using string path
f = Feedback(provider.relevance).on("input").on("output")

# Correct: Using Select class
from trulens_eval.schema import Select
f = Feedback(provider.relevance).on(Select.RecordInput).on(Select.RecordOutput)

# Or use helper methods
f = Feedback(provider.relevance).on_input_output()
```

**Issue: Feedback not running**

```python
# Check feedback mode
tru_chain = TruChain(
    chain,
    feedbacks=feedbacks,
    feedback_mode=FeedbackMode.WITH_APP  # Ensure feedback runs
)

# Manually run feedback
tru.run_feedback_functions(
    record_ids=[record_id],
    feedback_functions=feedbacks
)
```

**Issue: Database connection errors**

```python
# Reset database
tru = Tru()
tru.reset_database()

# Or specify different database
tru = Tru(database_url="sqlite:///./custom_trulens.db")
```

---

## API Reference

### Core Classes

**Tru:**
- `__init__(database_url, database_engine)`
- `reset_database()`
- `add_app(app)`
- `add_feedback(feedback_results)`
- `get_records_and_feedback(app_ids)`
- `run_dashboard(port, force)`

**TruChain:**
- `__init__(app, app_id, feedbacks, feedback_mode)`
- `__call__(*args, **kwargs)`
- `with_record(func)`
- `get_records()`

**Feedback:**
- `__init__(impl, name)`
- `on(selector)`
- `on_input()`, `on_output()`, `on_input_output()`
- `aggregate(func)`

---

## Performance

### Benchmarks

- **Instrumentation Overhead**: ~50-100ms per call
- **Feedback Function Latency**: ~1-3s per LLM-based feedback
- **Dashboard Load Time**: <2s for 1000 records
- **Database Query**: <100ms for typical queries

### Optimization Tips

1. **Use Deferred Mode in Production**
2. **Batch Feedback Execution**
3. **Limit Feedback Functions to Essential Ones**
4. **Use PostgreSQL for Scale**
5. **Archive Old Records Regularly**

---

## Security

### API Key Management

```python
import os
from dotenv import load_dotenv

load_dotenv()

provider = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

### Database Security

```python
# Use environment variables
database_url = os.getenv("TRULENS_DATABASE_URL")
tru = Tru(database_url=database_url)

# Enable SSL for PostgreSQL
database_url = "postgresql://user:pass@host:5432/db?sslmode=require"
```

---

## References

### Official Resources

- **GitHub**: https://github.com/truera/trulens
- **Documentation**: https://www.trulens.org/
- **Examples**: https://github.com/truera/trulens/tree/main/examples

### Key Papers

- "TruLens: Feedback Functions for LLM Applications" (2023)
- "Evaluating RAG Systems with TruLens" (2024)

### Community

- **Discord**: https://discord.gg/trulens
- **Twitter**: @TruEra

---

**Last Updated**: 2024
**TruLens Version**: 0.22.0+
**Minimum Python**: 3.8+
