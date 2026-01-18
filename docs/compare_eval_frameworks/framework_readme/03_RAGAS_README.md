# RAGAS - Comprehensive Deep Dive Guide
## Retrieval Augmented Generation Assessment

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

### What is RAGAS?

RAGAS (Retrieval Augmented Generation Assessment) is a specialized evaluation framework designed specifically for assessing the quality and performance of Retrieval-Augmented Generation (RAG) systems. It provides reference-free evaluation metrics that can assess RAG pipelines without requiring human-labeled ground truth data.

**Key Features:**
- Reference-free evaluation metrics
- Component-level RAG assessment (retrieval + generation)
- LLM-as-judge evaluation approach
- Multiple specialized metrics for RAG systems
- Integration with major RAG frameworks
- Automated test set generation
- Batch evaluation capabilities
- Synthetic data generation

**Core Metrics:**
1. **Faithfulness**: Measures factual consistency with retrieved context
2. **Answer Relevancy**: Assesses how relevant the answer is to the question
3. **Context Precision**: Evaluates if relevant items are ranked higher
4. **Context Recall**: Measures if all relevant information is retrieved
5. **Context Relevancy**: Checks if retrieved context is relevant to the question
6. **Answer Semantic Similarity**: Compares semantic similarity to ground truth
7. **Answer Correctness**: Combines semantic and factual accuracy

### Why RAGAS?

**Advantages:**
1. **RAG-Specific**: Purpose-built for RAG pipeline evaluation
2. **Reference-Free**: No need for expensive labeled datasets
3. **Component Isolation**: Evaluate retrieval and generation independently
4. **Production-Ready**: Easy integration into CI/CD pipelines
5. **Framework Agnostic**: Works with any RAG implementation
6. **Automated**: Minimal manual intervention required
7. **Research-Backed**: Based on academic research and best practices

**When to Use RAGAS:**
- You're building or optimizing a RAG system
- You need to measure retrieval quality
- You want to detect hallucinations in generated answers
- You need automated evaluation for continuous testing
- You want to compare different RAG configurations
- You need component-level debugging

**When to Consider Alternatives:**
- You need general LLM evaluation (not RAG-specific)
- You have extensive human-labeled ground truth
- You need real-time evaluation (RAGAS uses LLM calls)
- You require domain-specific custom metrics beyond RAG

---

## Architecture & Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAGAS Architecture                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      RAG Application                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Question   │→ │  Retriever   │→ │  Generator   │→ Answer │
│  └──────────────┘  └──────┬───────┘  └──────┬───────┘         │
│                           │                  │                  │
│                     Retrieved Docs     Generated Answer         │
└───────────────────────────┼──────────────────┼──────────────────┘
                            │                  │
                            ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RAGAS Evaluation                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Evaluation Dataset                       │  │
│  │  - Questions                                              │  │
│  │  - Retrieved Contexts                                     │  │
│  │  - Generated Answers                                      │  │
│  │  - Ground Truth (optional)                                │  │
│  └─────────────────────────┬────────────────────────────────┘  │
│                            │                                   │
│                            ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Metric Computation Engine                    │  │
│  │                                                           │  │
│  │  ┌─────────────────┐  ┌─────────────────┐               │  │
│  │  │  Retrieval      │  │  Generation     │               │  │
│  │  │  Metrics        │  │  Metrics        │               │  │
│  │  │                 │  │                 │               │  │
│  │  │  - Context      │  │  - Faithfulness │               │  │
│  │  │    Precision    │  │  - Answer       │               │  │
│  │  │  - Context      │  │    Relevancy    │               │  │
│  │  │    Recall       │  │  - Correctness  │               │  │
│  │  │  - Context      │  │  - Similarity   │               │  │
│  │  │    Relevancy    │  │                 │               │  │
│  │  └────────┬────────┘  └────────┬────────┘               │  │
│  │           │                    │                         │  │
│  └───────────┼────────────────────┼─────────────────────────┘  │
│              │                    │                            │
│              └──────────┬─────────┘                            │
│                         ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              LLM-as-Judge Evaluator                       │  │
│  │  (OpenAI GPT-4, Claude, etc.)                            │  │
│  └─────────────────────────┬────────────────────────────────┘  │
│                            │                                   │
│                            ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Results Aggregation                      │  │
│  │  - Per-question scores                                    │  │
│  │  - Aggregate statistics                                   │  │
│  │  - Component breakdown                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Metric Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAGAS Metrics Taxonomy                       │
└─────────────────────────────────────────────────────────────────┘

1. RETRIEVAL METRICS (Assess Retriever Quality)
   │
   ├── Context Precision
   │   ├── Input: Question, Retrieved Contexts, Ground Truth
   │   ├── Measures: Ranking quality of retrieved documents
   │   └── Output: Score 0-1 (higher = better ranking)
   │
   ├── Context Recall
   │   ├── Input: Ground Truth, Retrieved Contexts
   │   ├── Measures: Coverage of ground truth in retrieved docs
   │   └── Output: Score 0-1 (higher = more complete)
   │
   └── Context Relevancy
       ├── Input: Question, Retrieved Contexts
       ├── Measures: Relevance of retrieved docs to question
       └── Output: Score 0-1 (higher = more relevant)

2. GENERATION METRICS (Assess Generator Quality)
   │
   ├── Faithfulness
   │   ├── Input: Answer, Retrieved Contexts
   │   ├── Measures: Factual consistency with contexts
   │   └── Output: Score 0-1 (higher = less hallucination)
   │
   ├── Answer Relevancy
   │   ├── Input: Question, Answer
   │   ├── Measures: How well answer addresses question
   │   └── Output: Score 0-1 (higher = more relevant)
   │
   ├── Answer Semantic Similarity
   │   ├── Input: Answer, Ground Truth
   │   ├── Measures: Semantic similarity to ground truth
   │   └── Output: Score 0-1 (higher = more similar)
   │
   └── Answer Correctness
       ├── Input: Answer, Ground Truth
       ├── Measures: Combined semantic + factual accuracy
       └── Output: Score 0-1 (weighted combination)

3. END-TO-END METRICS
   │
   └── RAGAS Score
       ├── Input: All component metrics
       ├── Calculation: Harmonic mean of individual metrics
       └── Output: Single score representing overall quality
```

### Evaluation Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  RAGAS Evaluation Pipeline                      │
└─────────────────────────────────────────────────────────────────┘

Step 1: Data Preparation
   ↓
   [Question, Contexts, Answer, Ground Truth (optional)]
   ↓
Step 2: Metric Selection
   ↓
   Select applicable metrics based on available data
   ↓
Step 3: LLM-based Evaluation
   ↓
   For each metric:
     ├─> Generate evaluation prompt
     ├─> Call LLM judge
     ├─> Parse response
     └─> Extract score
   ↓
Step 4: Score Aggregation
   ↓
   Combine individual metric scores
   ↓
Step 5: Results Generation
   ↓
   [Scores DataFrame, Statistics, Insights]
```

### Component Details

#### 1. Dataset Structure

```python
from datasets import Dataset

# RAGAS expects Hugging Face Dataset format
evaluation_dataset = Dataset.from_dict({
    "question": [
        "What is machine learning?",
        "How does RAG work?"
    ],
    "contexts": [
        ["Machine learning is a subset of AI...", "ML algorithms learn from data..."],
        ["RAG combines retrieval and generation...", "It uses vector databases..."]
    ],
    "answer": [
        "Machine learning is a method where computers learn from data.",
        "RAG retrieves relevant documents and uses them to generate answers."
    ],
    "ground_truth": [  # Optional
        "Machine learning enables computers to learn without explicit programming.",
        "RAG enhances LLM responses by retrieving relevant context first."
    ]
})
```

#### 2. Metric Computation

```python
# Faithfulness Metric Computation Process
1. Extract claims from answer
   "Python was created in 1991 by Guido van Rossum"
   → Claims: ["Python was created in 1991", "Python was created by Guido van Rossum"]

2. Verify each claim against contexts
   For each claim:
     - Check if supported by contexts
     - Mark as supported/unsupported

3. Calculate score
   Faithfulness = (Supported Claims) / (Total Claims)
```

#### 3. LLM Judge Integration

```python
# RAGAS uses LLM as judge for evaluation
LLM Judge Process:
   1. Format evaluation prompt with template
   2. Call LLM API (OpenAI, Azure OpenAI, etc.)
   3. Parse structured response
   4. Extract numeric score or label
   5. Return evaluation result

Supported LLMs:
   - OpenAI (GPT-3.5, GPT-4)
   - Azure OpenAI
   - Anthropic Claude
   - Google PaLM
   - Open-source models via LangChain
```

---

## Installation & Setup

### Prerequisites

**System Requirements:**
- Python 3.8 or higher
- pip or conda package manager
- OpenAI API key (or alternative LLM provider)
- 2GB RAM minimum
- Internet connection for LLM API calls

### Installation Methods

#### Method 1: Basic Installation (PyPI)

```bash
# Install RAGAS from PyPI
pip install ragas

# Install with specific versions
pip install ragas==0.1.0

# Upgrade to latest version
pip install --upgrade ragas
```

#### Method 2: Installation with Optional Dependencies

```bash
# Install with all optional dependencies
pip install ragas[all]

# Install with specific integrations
pip install ragas[langchain]
pip install ragas[llama-index]
```

#### Method 3: Development Installation

```bash
# Clone repository
git clone https://github.com/explodinggradients/ragas.git
cd ragas

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

#### Method 4: Conda Installation

```bash
# Create conda environment
conda create -n ragas-env python=3.10
conda activate ragas-env

# Install RAGAS
pip install ragas

# Install additional dependencies
conda install pandas numpy
```

### Environment Setup

#### Configure LLM Provider

```bash
# .env file
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://api.openai.com/v1  # Optional for custom endpoints

# For Azure OpenAI
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# For Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-...
```

```python
# Load environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# Verify API key is loaded
print(f"API Key configured: {bool(os.getenv('OPENAI_API_KEY'))}")
```

### Basic Setup and Verification

```python
# basic_setup.py
"""
Basic RAGAS setup and verification
"""

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset
import os

# Verify installation
print(f"RAGAS version: {ragas.__version__}")

# Check API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment")

# Create sample dataset
sample_data = {
    "question": ["What is the capital of France?"],
    "contexts": [["France is a country in Europe. Its capital is Paris."]],
    "answer": ["The capital of France is Paris."],
    "ground_truth": ["Paris is the capital of France."]
}

dataset = Dataset.from_dict(sample_data)

# Run evaluation
print("Running test evaluation...")
result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ]
)

print("\nResults:")
print(result)
print("\n✓ RAGAS setup successful!")
```

```bash
# Run setup verification
python basic_setup.py
```

### Custom LLM Configuration

```python
# custom_llm_setup.py
"""
Configure RAGAS with custom LLM settings
"""

from ragas.llms import LangchainLLM
from langchain_openai import ChatOpenAI
from ragas.embeddings import LangchainEmbeddings
from langchain_openai import OpenAIEmbeddings

# Configure custom LLM
custom_llm = LangchainLLM(
    ChatOpenAI(
        model="gpt-4",
        temperature=0.0,
        max_tokens=1000,
        timeout=60,
        max_retries=3
    )
)

# Configure custom embeddings
custom_embeddings = LangchainEmbeddings(
    OpenAIEmbeddings(
        model="text-embedding-3-small"
    )
)

# Use in evaluation
from ragas.metrics import faithfulness

# Set custom LLM for metric
faithfulness.llm = custom_llm
faithfulness.embeddings = custom_embeddings
```

### Azure OpenAI Setup

```python
# azure_openai_setup.py
"""
Configure RAGAS with Azure OpenAI
"""

import os
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from ragas.llms import LangchainLLM
from ragas.embeddings import LangchainEmbeddings

# Configure Azure OpenAI LLM
azure_llm = LangchainLLM(
    AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01",
        deployment_name="gpt-4",
        temperature=0.0
    )
)

# Configure Azure OpenAI Embeddings
azure_embeddings = LangchainEmbeddings(
    AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01",
        deployment_name="text-embedding-3-small"
    )
)

# Apply to metrics
from ragas.metrics import faithfulness, answer_relevancy

faithfulness.llm = azure_llm
faithfulness.embeddings = azure_embeddings
answer_relevancy.llm = azure_llm
answer_relevancy.embeddings = azure_embeddings
```

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV OPENAI_API_KEY=""
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python", "evaluate_rag.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  ragas-evaluator:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
      - ./results:/app/results
```

```bash
# Build and run
docker-compose up --build
```

---

## Core Concepts

### 1. Evaluation Metrics

RAGAS provides several metrics, each designed to assess different aspects of RAG systems.

#### Faithfulness

Measures the factual consistency of the answer with the retrieved contexts.

**Definition:**
```
Faithfulness = (Number of supported claims) / (Total number of claims)
```

**How it works:**
1. Extract all claims/statements from the generated answer
2. For each claim, check if it's supported by retrieved contexts
3. Calculate ratio of supported claims

**Example:**

```python
from ragas.metrics import faithfulness
from datasets import Dataset

data = {
    "question": ["Who created Python?"],
    "contexts": [["Python was created by Guido van Rossum in 1991."]],
    "answer": ["Python was created by Guido van Rossum in 1995."]
}

dataset = Dataset.from_dict(data)
score = faithfulness.score(dataset)

# Low score because year "1995" is not supported by context "1991"
print(f"Faithfulness: {score}")  # ~0.5 (one claim correct, one incorrect)
```

**Use Cases:**
- Detect hallucinations
- Ensure factual accuracy
- Verify answer is grounded in retrieved docs

#### Answer Relevancy

Measures how relevant the answer is to the posed question.

**Definition:**
```
Answer Relevancy = (Semantic similarity between question and answer) / (Normalization factor)
```

**How it works:**
1. Generate multiple questions from the answer
2. Calculate semantic similarity between generated and original question
3. Average similarities as relevancy score

**Example:**

```python
from ragas.metrics import answer_relevancy

data = {
    "question": ["What is the capital of France?"],
    "answer": ["Paris is known for the Eiffel Tower and museums."],  # Indirect answer
    "contexts": [["France is a country. Paris is its capital."]]
}

dataset = Dataset.from_dict(data)
score = answer_relevancy.score(dataset)

# Medium score because answer talks about Paris but doesn't directly state it's the capital
print(f"Answer Relevancy: {score}")
```

**Use Cases:**
- Ensure answer directly addresses question
- Detect when answers go off-topic
- Improve response targeting

#### Context Precision

Measures if relevant items are ranked higher in the retrieved contexts.

**Definition:**
```
Context Precision = (Sum of precision@k for relevant items) / (Total relevant items)
```

**How it works:**
1. Identify which retrieved contexts are relevant (using ground truth)
2. Check ranking position of relevant contexts
3. Calculate precision focusing on high-ranked items

**Example:**

```python
from ragas.metrics import context_precision

data = {
    "question": ["What is machine learning?"],
    "contexts": [[
        "ML is a subset of AI.",  # Relevant - ranked #1
        "The weather is sunny today.",  # Not relevant - ranked #2
        "ML algorithms learn from data."  # Relevant - ranked #3
    ]],
    "ground_truth": ["Machine learning is AI that learns from data."]
}

dataset = Dataset.from_dict(data)
score = context_precision.score(dataset)

# Medium score because relevant items are not all at top
print(f"Context Precision: {score}")
```

**Use Cases:**
- Optimize retrieval ranking
- Improve vector search configuration
- Fine-tune retrieval models

#### Context Recall

Measures if all relevant information from ground truth is present in retrieved contexts.

**Definition:**
```
Context Recall = (Ground truth sentences in contexts) / (Total ground truth sentences)
```

**How it works:**
1. Break ground truth into atomic sentences
2. Check if each sentence is supported by retrieved contexts
3. Calculate ratio of covered sentences

**Example:**

```python
from ragas.metrics import context_recall

data = {
    "question": ["What is Python used for?"],
    "contexts": [[
        "Python is used for web development.",
        "Python is used for data science."
    ]],
    "ground_truth": ["Python is used for web development, data science, and automation."]
}

dataset = Dataset.from_dict(data)
score = context_recall.score(dataset)

# ~0.67 score (2 out of 3 use cases covered)
print(f"Context Recall: {score}")
```

**Use Cases:**
- Assess retrieval completeness
- Tune top_k parameter
- Evaluate chunking strategies

#### Context Relevancy

Measures the relevance of retrieved contexts to the question.

**Definition:**
```
Context Relevancy = (Relevant sentences in contexts) / (Total sentences in contexts)
```

**How it works:**
1. Extract all sentences from retrieved contexts
2. Classify each sentence as relevant/irrelevant to question
3. Calculate ratio of relevant sentences

**Example:**

```python
from ragas.metrics import context_relevancy

data = {
    "question": ["What is the capital of France?"],
    "contexts": [[
        "France is in Europe.",  # Somewhat relevant
        "Paris is the capital of France.",  # Highly relevant
        "I like pizza."  # Not relevant
    ]]
}

dataset = Dataset.from_dict(data)
score = context_relevancy.score(dataset)

# ~0.67 score (2 out of 3 sentences relevant)
print(f"Context Relevancy: {score}")
```

**Use Cases:**
- Filter noisy retrieved documents
- Improve retrieval precision
- Reduce context length for LLM

#### Answer Semantic Similarity

Measures semantic similarity between generated answer and ground truth.

**Definition:**
```
Semantic Similarity = cosine_similarity(embedding(answer), embedding(ground_truth))
```

**How it works:**
1. Generate embeddings for answer and ground truth
2. Calculate cosine similarity
3. Return similarity score

**Example:**

```python
from ragas.metrics import answer_similarity

data = {
    "question": ["What is 2+2?"],
    "answer": ["The sum of two and two is four."],
    "ground_truth": ["2+2 equals 4."]
}

dataset = Dataset.from_dict(data)
score = answer_similarity.score(dataset)

# High score because meaning is same despite different wording
print(f"Semantic Similarity: {score}")  # ~0.9
```

**Use Cases:**
- Compare against reference answers
- Evaluate semantic equivalence
- Augment human evaluation

#### Answer Correctness

Combines semantic similarity with factual correctness.

**Definition:**
```
Answer Correctness = (w1 × Semantic Similarity) + (w2 × Factual Correctness)
```

**How it works:**
1. Calculate semantic similarity (as above)
2. Calculate factual correctness (F1 score of facts)
3. Weighted combination of both scores

**Example:**

```python
from ragas.metrics import answer_correctness

data = {
    "question": ["Who founded Microsoft?"],
    "answer": ["Microsoft was founded by Bill Gates and Paul Allen in 1975."],
    "ground_truth": ["Bill Gates and Paul Allen founded Microsoft."]
}

dataset = Dataset.from_dict(data)
score = answer_correctness.score(dataset)

# High score: semantically similar AND factually correct
print(f"Answer Correctness: {score}")
```

**Use Cases:**
- Comprehensive answer evaluation
- Balance semantic and factual accuracy
- Final quality assessment

### 2. Dataset Format

RAGAS uses Hugging Face Dataset format:

```python
from datasets import Dataset

# Required fields vary by metric
evaluation_data = {
    # Required for all metrics
    "question": ["What is AI?", "What is ML?"],

    # Required for generation metrics
    "answer": [
        "AI is intelligence demonstrated by machines.",
        "ML is a subset of AI that learns from data."
    ],

    # Required for retrieval & faithfulness metrics
    "contexts": [
        [
            "Artificial Intelligence (AI) is machine intelligence.",
            "AI systems can perform tasks that typically require human intelligence."
        ],
        [
            "Machine Learning is a method of data analysis.",
            "ML is a type of AI that learns from data."
        ]
    ],

    # Optional but required for some metrics (context_recall, answer_similarity, etc.)
    "ground_truth": [
        "AI refers to the simulation of human intelligence in machines.",
        "Machine learning is a branch of AI focused on learning from data."
    ]
}

dataset = Dataset.from_dict(evaluation_data)
```

### 3. Evaluation Process

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

# Define metrics to evaluate
metrics = [
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
]

# Run evaluation
result = evaluate(
    dataset=dataset,
    metrics=metrics,
    llm=custom_llm,  # Optional: use custom LLM
    embeddings=custom_embeddings,  # Optional: use custom embeddings
)

# Access results
print(result)  # Pandas DataFrame with scores
print(result.to_pandas())
```

### 4. Test Data Generation

RAGAS can generate synthetic test data:

```python
from ragas.testset import TestsetGenerator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas.testset.synthesizers import default_query_distribution

# Configure generator
generator = TestsetGenerator.from_llm(
    llm=ChatOpenAI(model="gpt-4"),
    embedding_model=OpenAIEmbeddings()
)

# Generate from documents
from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader("./docs")
documents = loader.load()

# Generate test set
testset = generator.generate(
    documents=documents,
    test_size=50,  # Number of test cases
    query_distribution=default_query_distribution
)

# Convert to dataset
dataset = testset.to_dataset()
```

---

## Production-Ready Examples

### Example 1: Basic RAG Evaluation

```python
# basic_rag_evaluation.py
"""
Basic RAG system evaluation with RAGAS
Demonstrates: Simple evaluation workflow, all core metrics
"""

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    context_relevancy,
    answer_similarity,
    answer_correctness
)
from datasets import Dataset
import pandas as pd

def create_evaluation_dataset():
    """Create sample RAG evaluation dataset"""
    data = {
        "question": [
            "What is the capital of France?",
            "Who invented the telephone?",
            "What is photosynthesis?",
            "When did World War II end?",
        ],
        "contexts": [
            [
                "France is a country in Western Europe.",
                "Paris is the capital and largest city of France.",
                "Paris is known for the Eiffel Tower."
            ],
            [
                "Alexander Graham Bell was a Scottish-born inventor.",
                "Bell is credited with inventing the telephone in 1876.",
                "Thomas Edison invented the phonograph."
            ],
            [
                "Photosynthesis is a process used by plants.",
                "Plants convert light energy into chemical energy.",
                "This process produces oxygen and glucose."
            ],
            [
                "World War II was a global war from 1939 to 1945.",
                "The war ended with the surrender of Germany and Japan.",
                "Germany surrendered in May 1945, Japan in September 1945."
            ]
        ],
        "answer": [
            "The capital of France is Paris, a major European city known for culture and art.",
            "Alexander Graham Bell invented the telephone in 1876.",
            "Photosynthesis is the process by which plants convert sunlight into energy, producing oxygen.",
            "World War II ended in 1945 with the surrender of Axis powers."
        ],
        "ground_truth": [
            "Paris is the capital of France.",
            "The telephone was invented by Alexander Graham Bell.",
            "Photosynthesis is how plants convert light energy to chemical energy.",
            "World War II ended in 1945."
        ]
    }

    return Dataset.from_dict(data)

def run_evaluation():
    """Run comprehensive RAG evaluation"""
    print("Creating evaluation dataset...")
    dataset = create_evaluation_dataset()

    print(f"Dataset size: {len(dataset)}")
    print("\nRunning evaluation...")

    # Define metrics
    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
        context_relevancy,
        answer_similarity,
        answer_correctness
    ]

    # Evaluate
    result = evaluate(
        dataset=dataset,
        metrics=metrics
    )

    # Display results
    print("\n" + "="*70)
    print("EVALUATION RESULTS")
    print("="*70)

    df = result.to_pandas()

    # Overall scores
    print("\nOverall Scores:")
    for metric in metrics:
        score = df[metric.name].mean()
        print(f"  {metric.name}: {score:.4f}")

    # Per-question breakdown
    print("\nPer-Question Scores:")
    print(df.to_string(index=False))

    # Save results
    df.to_csv("rag_evaluation_results.csv", index=False)
    print("\n✓ Results saved to rag_evaluation_results.csv")

    return result

if __name__ == "__main__":
    result = run_evaluation()
```

### Example 2: LangChain RAG Evaluation

```python
# langchain_rag_evaluation.py
"""
Evaluate a LangChain RAG system with RAGAS
Demonstrates: Integration with LangChain, end-to-end pipeline evaluation
"""

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall
from datasets import Dataset
import os

class RAGSystem:
    """LangChain-based RAG system"""

    def __init__(self, docs_path: str):
        self.docs_path = docs_path
        self.vectorstore = None
        self.qa_chain = None
        self._setup()

    def _setup(self):
        """Setup RAG components"""
        # Load documents
        loader = TextLoader(self.docs_path)
        documents = loader.load()

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        splits = text_splitter.split_documents(documents)

        # Create vector store
        embeddings = OpenAIEmbeddings()
        self.vectorstore = FAISS.from_documents(splits, embeddings)

        # Create QA chain
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )

    def query(self, question: str) -> dict:
        """Query RAG system"""
        result = self.qa_chain({"query": question})
        return {
            "answer": result["result"],
            "contexts": [doc.page_content for doc in result["source_documents"]]
        }

def prepare_sample_doc(file_path: str):
    """Create sample document for testing"""
    content = """
    Machine Learning Overview

    Machine learning is a subset of artificial intelligence (AI) that enables
    systems to learn and improve from experience without being explicitly programmed.

    Types of Machine Learning:
    1. Supervised Learning: Learning from labeled data
    2. Unsupervised Learning: Finding patterns in unlabeled data
    3. Reinforcement Learning: Learning through trial and error

    Applications:
    - Image recognition
    - Natural language processing
    - Recommendation systems
    - Autonomous vehicles

    Key Algorithms:
    - Neural networks
    - Decision trees
    - Support vector machines
    - Random forests
    """

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)

def evaluate_rag_system():
    """Evaluate RAG system using RAGAS"""
    # Setup
    docs_path = "./data/ml_overview.txt"
    prepare_sample_doc(docs_path)

    # Initialize RAG system
    print("Initializing RAG system...")
    rag = RAGSystem(docs_path)

    # Test questions
    test_questions = [
        {
            "question": "What is machine learning?",
            "ground_truth": "Machine learning is a subset of AI that enables systems to learn from experience."
        },
        {
            "question": "What are the types of machine learning?",
            "ground_truth": "The main types are supervised learning, unsupervised learning, and reinforcement learning."
        },
        {
            "question": "What are applications of machine learning?",
            "ground_truth": "Applications include image recognition, NLP, recommendation systems, and autonomous vehicles."
        }
    ]

    # Query RAG system
    print("Querying RAG system...")
    results = []
    for test in test_questions:
        result = rag.query(test["question"])
        results.append({
            "question": test["question"],
            "answer": result["answer"],
            "contexts": result["contexts"],
            "ground_truth": test["ground_truth"]
        })

    # Create dataset
    dataset_dict = {
        "question": [r["question"] for r in results],
        "answer": [r["answer"] for r in results],
        "contexts": [r["contexts"] for r in results],
        "ground_truth": [r["ground_truth"] for r in results]
    }
    dataset = Dataset.from_dict(dataset_dict)

    # Evaluate
    print("\nEvaluating with RAGAS...")
    evaluation_result = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy, context_recall]
    )

    # Display results
    print("\n" + "="*70)
    print("RAG SYSTEM EVALUATION RESULTS")
    print("="*70)

    df = evaluation_result.to_pandas()
    print("\nMetric Scores:")
    for col in df.columns:
        if col not in ["question", "answer", "contexts", "ground_truth"]:
            print(f"  {col}: {df[col].mean():.4f}")

    print("\nDetailed Results:")
    print(df[["question", "faithfulness", "answer_relevancy", "context_recall"]].to_string(index=False))

    return evaluation_result

if __name__ == "__main__":
    result = evaluate_rag_system()
```

### Example 3: Batch Evaluation Pipeline

```python
# batch_evaluation_pipeline.py
"""
Batch evaluation pipeline for multiple RAG configurations
Demonstrates: Comparing different RAG setups, A/B testing
"""

from typing import List, Dict
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset
import pandas as pd
from dataclasses import dataclass

@dataclass
class RAGConfiguration:
    """RAG configuration parameters"""
    name: str
    top_k: int
    chunk_size: int
    chunk_overlap: int
    model: str

class BatchEvaluator:
    """Batch evaluation for multiple RAG configurations"""

    def __init__(self, test_questions: List[Dict]):
        self.test_questions = test_questions
        self.results = []

    def evaluate_configuration(self,
                              config: RAGConfiguration,
                              rag_responses: List[Dict]) -> Dict:
        """Evaluate single RAG configuration"""
        print(f"\nEvaluating configuration: {config.name}")
        print(f"  top_k={config.top_k}, chunk_size={config.chunk_size}, model={config.model}")

        # Prepare dataset
        dataset_dict = {
            "question": [q["question"] for q in self.test_questions],
            "answer": [r["answer"] for r in rag_responses],
            "contexts": [r["contexts"] for r in rag_responses],
            "ground_truth": [q["ground_truth"] for q in self.test_questions]
        }
        dataset = Dataset.from_dict(dataset_dict)

        # Evaluate
        result = evaluate(
            dataset=dataset,
            metrics=[faithfulness, answer_relevancy, context_precision]
        )

        # Extract scores
        df = result.to_pandas()
        scores = {
            "configuration": config.name,
            "faithfulness": df["faithfulness"].mean(),
            "answer_relevancy": df["answer_relevancy"].mean(),
            "context_precision": df["context_precision"].mean(),
            "overall": (df["faithfulness"].mean() +
                       df["answer_relevancy"].mean() +
                       df["context_precision"].mean()) / 3,
            "config_params": {
                "top_k": config.top_k,
                "chunk_size": config.chunk_size,
                "chunk_overlap": config.chunk_overlap,
                "model": config.model
            }
        }

        self.results.append(scores)
        return scores

    def compare_configurations(self) -> pd.DataFrame:
        """Compare all evaluated configurations"""
        if not self.results:
            raise ValueError("No configurations evaluated yet")

        # Create comparison DataFrame
        comparison = pd.DataFrame(self.results)

        # Sort by overall score
        comparison = comparison.sort_values("overall", ascending=False)

        return comparison

    def generate_report(self) -> str:
        """Generate evaluation report"""
        comparison = self.compare_configurations()

        report = []
        report.append("="*80)
        report.append("RAG CONFIGURATION COMPARISON REPORT")
        report.append("="*80)

        report.append(f"\nTotal Configurations Evaluated: {len(self.results)}")
        report.append(f"Test Questions: {len(self.test_questions)}")

        report.append("\n" + "-"*80)
        report.append("RANKINGS (by overall score)")
        report.append("-"*80)

        for idx, row in comparison.iterrows():
            report.append(f"\n#{comparison.index.get_loc(idx) + 1}: {row['configuration']}")
            report.append(f"  Overall Score: {row['overall']:.4f}")
            report.append(f"  Faithfulness: {row['faithfulness']:.4f}")
            report.append(f"  Answer Relevancy: {row['answer_relevancy']:.4f}")
            report.append(f"  Context Precision: {row['context_precision']:.4f}")
            report.append(f"  Parameters: top_k={row['config_params']['top_k']}, "
                         f"chunk_size={row['config_params']['chunk_size']}, "
                         f"model={row['config_params']['model']}")

        # Best configuration
        best = comparison.iloc[0]
        report.append("\n" + "="*80)
        report.append("RECOMMENDED CONFIGURATION")
        report.append("="*80)
        report.append(f"Configuration: {best['configuration']}")
        report.append(f"Score: {best['overall']:.4f}")
        report.append(f"Parameters: {best['config_params']}")

        return "\n".join(report)

def mock_rag_query(question: str, config: RAGConfiguration) -> Dict:
    """Mock RAG query for demonstration"""
    # In production, this would call your actual RAG system
    mock_responses = {
        "What is machine learning?": {
            "answer": "Machine learning is a subset of AI that learns from data.",
            "contexts": [
                "ML is a type of artificial intelligence.",
                "ML systems learn from experience and data.",
                "Common ML tasks include classification and regression."
            ]
        },
        "What are neural networks?": {
            "answer": "Neural networks are computing systems inspired by biological neural networks.",
            "contexts": [
                "Neural networks consist of layers of interconnected nodes.",
                "They are used for pattern recognition.",
                "Deep learning uses multi-layer neural networks."
            ]
        }
    }

    return mock_responses.get(question, {
        "answer": "Information not found.",
        "contexts": ["No relevant context available."]
    })

def main():
    """Run batch evaluation"""
    # Test questions with ground truth
    test_questions = [
        {
            "question": "What is machine learning?",
            "ground_truth": "Machine learning is a subset of AI that enables systems to learn from data."
        },
        {
            "question": "What are neural networks?",
            "ground_truth": "Neural networks are computing systems inspired by biological brains."
        }
    ]

    # Define configurations to test
    configurations = [
        RAGConfiguration(
            name="Config-A (Small chunks, high k)",
            top_k=5,
            chunk_size=200,
            chunk_overlap=20,
            model="gpt-3.5-turbo"
        ),
        RAGConfiguration(
            name="Config-B (Large chunks, low k)",
            top_k=3,
            chunk_size=500,
            chunk_overlap=50,
            model="gpt-3.5-turbo"
        ),
        RAGConfiguration(
            name="Config-C (Medium chunks, medium k, better model)",
            top_k=4,
            chunk_size=350,
            chunk_overlap=35,
            model="gpt-4"
        )
    ]

    # Initialize evaluator
    evaluator = BatchEvaluator(test_questions)

    # Evaluate each configuration
    for config in configurations:
        # Query RAG system with this config (mocked for demo)
        responses = [mock_rag_query(q["question"], config) for q in test_questions]

        # Evaluate
        evaluator.evaluate_configuration(config, responses)

    # Generate report
    report = evaluator.generate_report()
    print("\n" + report)

    # Save comparison
    comparison = evaluator.compare_configurations()
    comparison.to_csv("rag_config_comparison.csv", index=False)
    print("\n✓ Comparison saved to rag_config_comparison.csv")

if __name__ == "__main__":
    main()
```

### Example 4: Synthetic Test Generation

```python
# synthetic_test_generation.py
"""
Generate synthetic test sets using RAGAS
Demonstrates: Automatic test data creation from documents
"""

from ragas.testset import TestsetGenerator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from ragas.testset.synthesizers import default_query_distribution
import os

def create_sample_documents(docs_dir: str):
    """Create sample documents for test generation"""
    os.makedirs(docs_dir, exist_ok=True)

    docs = {
        "python_basics.txt": """
        Python Programming Basics

        Python is a high-level, interpreted programming language known for its simplicity.
        Created by Guido van Rossum and first released in 1991.

        Key Features:
        - Easy to learn and read
        - Dynamically typed
        - Supports multiple programming paradigms
        - Extensive standard library

        Common Uses:
        - Web development (Django, Flask)
        - Data analysis (Pandas, NumPy)
        - Machine learning (TensorFlow, PyTorch)
        - Automation and scripting
        """,

        "data_structures.txt": """
        Python Data Structures

        Lists: Ordered, mutable sequences
        - Created with square brackets: [1, 2, 3]
        - Support indexing and slicing
        - Dynamic sizing

        Dictionaries: Key-value mappings
        - Created with curly braces: {'key': 'value'}
        - Fast lookup by key
        - Keys must be immutable

        Sets: Unordered collections of unique elements
        - Created with curly braces: {1, 2, 3}
        - Support set operations (union, intersection)
        - Automatically remove duplicates

        Tuples: Ordered, immutable sequences
        - Created with parentheses: (1, 2, 3)
        - Cannot be modified after creation
        - More memory efficient than lists
        """,

        "functions.txt": """
        Python Functions

        Functions are reusable blocks of code that perform specific tasks.

        Defining Functions:
        def function_name(parameters):
            # function body
            return result

        Function Features:
        - Support default parameters
        - Accept variable number of arguments (*args, **kwargs)
        - Can return multiple values
        - Support lambda (anonymous) functions

        Example:
        def add(a, b):
            return a + b

        result = add(5, 3)  # Returns 8
        """
    }

    for filename, content in docs.items():
        with open(os.path.join(docs_dir, filename), 'w') as f:
            f.write(content)

def generate_testset(docs_dir: str, test_size: int = 10):
    """Generate synthetic test set from documents"""
    print(f"Loading documents from {docs_dir}...")

    # Load documents
    loader = DirectoryLoader(docs_dir, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()

    print(f"Loaded {len(documents)} documents")

    # Configure generator
    print("Configuring test generator...")
    generator = TestsetGenerator.from_llm(
        llm=ChatOpenAI(model="gpt-4", temperature=0.3),
        embedding_model=OpenAIEmbeddings(model="text-embedding-3-small")
    )

    # Generate testset
    print(f"Generating {test_size} test cases...")
    testset = generator.generate(
        documents=documents,
        test_size=test_size,
        query_distribution=default_query_distribution,
        with_debugging_logs=True
    )

    return testset

def analyze_testset(testset):
    """Analyze generated testset"""
    df = testset.to_pandas()

    print("\n" + "="*70)
    print("GENERATED TESTSET ANALYSIS")
    print("="*70)

    print(f"\nTotal test cases: {len(df)}")

    # Question types distribution
    if "question_type" in df.columns:
        print("\nQuestion Type Distribution:")
        print(df["question_type"].value_counts())

    # Sample questions
    print("\nSample Generated Questions:")
    for idx, row in df.head(5).iterrows():
        print(f"\n{idx + 1}. {row['question']}")
        if "ground_truth" in df.columns:
            print(f"   Ground Truth: {row['ground_truth'][:100]}...")

    return df

def save_testset(testset, output_path: str):
    """Save testset to file"""
    df = testset.to_pandas()
    df.to_csv(output_path, index=False)
    print(f"\n✓ Testset saved to {output_path}")

    # Also save as JSON for better readability
    json_path = output_path.replace('.csv', '.json')
    df.to_json(json_path, orient='records', indent=2)
    print(f"✓ Testset saved to {json_path}")

def main():
    """Main execution"""
    docs_dir = "./docs_for_testgen"
    output_path = "./generated_testset.csv"

    # Create sample documents
    print("Creating sample documents...")
    create_sample_documents(docs_dir)

    # Generate testset
    testset = generate_testset(docs_dir, test_size=15)

    # Analyze
    analyze_testset(testset)

    # Save
    save_testset(testset, output_path)

if __name__ == "__main__":
    main()
```

### Example 5: Component-Level Evaluation

```python
# component_level_evaluation.py
"""
Evaluate RAG components separately (retriever vs generator)
Demonstrates: Isolated component testing, bottleneck identification
"""

from ragas import evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    context_relevancy,
    faithfulness,
    answer_relevancy
)
from datasets import Dataset
import pandas as pd
from typing import Dict, List

class ComponentEvaluator:
    """Evaluate RAG components independently"""

    def __init__(self):
        self.retrieval_metrics = [
            context_precision,
            context_recall,
            context_relevancy
        ]

        self.generation_metrics = [
            faithfulness,
            answer_relevancy
        ]

    def evaluate_retriever(self, dataset: Dataset) -> Dict:
        """Evaluate only the retrieval component"""
        print("Evaluating Retriever Component...")

        result = evaluate(
            dataset=dataset,
            metrics=self.retrieval_metrics
        )

        df = result.to_pandas()

        scores = {
            "context_precision": df["context_precision"].mean(),
            "context_recall": df["context_recall"].mean(),
            "context_relevancy": df["context_relevancy"].mean(),
            "retrieval_score": (
                df["context_precision"].mean() +
                df["context_recall"].mean() +
                df["context_relevancy"].mean()
            ) / 3
        }

        return scores

    def evaluate_generator(self, dataset: Dataset) -> Dict:
        """Evaluate only the generation component"""
        print("Evaluating Generator Component...")

        result = evaluate(
            dataset=dataset,
            metrics=self.generation_metrics
        )

        df = result.to_pandas()

        scores = {
            "faithfulness": df["faithfulness"].mean(),
            "answer_relevancy": df["answer_relevancy"].mean(),
            "generation_score": (
                df["faithfulness"].mean() +
                df["answer_relevancy"].mean()
            ) / 2
        }

        return scores

    def identify_bottleneck(self,
                           retrieval_scores: Dict,
                           generation_scores: Dict) -> str:
        """Identify which component needs improvement"""
        retrieval_score = retrieval_scores["retrieval_score"]
        generation_score = generation_scores["generation_score"]

        if retrieval_score < 0.7 and generation_score >= 0.7:
            return "RETRIEVER (poor document retrieval)"
        elif generation_score < 0.7 and retrieval_score >= 0.7:
            return "GENERATOR (poor answer quality despite good retrieval)"
        elif retrieval_score < 0.7 and generation_score < 0.7:
            return "BOTH (both components need improvement)"
        else:
            return "NONE (system performing well)"

    def generate_component_report(self,
                                  retrieval_scores: Dict,
                                  generation_scores: Dict) -> str:
        """Generate component evaluation report"""
        bottleneck = self.identify_bottleneck(retrieval_scores, generation_scores)

        report = []
        report.append("="*70)
        report.append("COMPONENT-LEVEL EVALUATION REPORT")
        report.append("="*70)

        report.append("\nRETRIEVAL COMPONENT:")
        report.append(f"  Context Precision: {retrieval_scores['context_precision']:.4f}")
        report.append(f"  Context Recall: {retrieval_scores['context_recall']:.4f}")
        report.append(f"  Context Relevancy: {retrieval_scores['context_relevancy']:.4f}")
        report.append(f"  Overall Retrieval Score: {retrieval_scores['retrieval_score']:.4f}")

        report.append("\nGENERATION COMPONENT:")
        report.append(f"  Faithfulness: {generation_scores['faithfulness']:.4f}")
        report.append(f"  Answer Relevancy: {generation_scores['answer_relevancy']:.4f}")
        report.append(f"  Overall Generation Score: {generation_scores['generation_score']:.4f}")

        report.append("\nBOTTLENECK IDENTIFICATION:")
        report.append(f"  {bottleneck}")

        report.append("\nRECOMMENDATIONS:")
        if "RETRIEVER" in bottleneck:
            report.append("  - Improve vector search (tune similarity threshold)")
            report.append("  - Optimize chunk size and overlap")
            report.append("  - Consider hybrid search (keyword + semantic)")
            report.append("  - Fine-tune embedding model")
        if "GENERATOR" in bottleneck:
            report.append("  - Improve prompts for better answer generation")
            report.append("  - Use more capable LLM model")
            report.append("  - Add few-shot examples to prompts")
            report.append("  - Implement answer verification step")

        return "\n".join(report)

def create_test_dataset():
    """Create test dataset with varied quality"""
    data = {
        "question": [
            "What is Python?",
            "Who created Python?",
            "What is a Python list?",
        ],
        "contexts": [
            # Good retrieval
            [
                "Python is a high-level programming language.",
                "Python is known for its simple syntax.",
                "Python was created by Guido van Rossum."
            ],
            # Poor retrieval (irrelevant contexts)
            [
                "JavaScript is a web programming language.",
                "Java is used for enterprise applications.",
                "C++ is a systems programming language."
            ],
            # Medium retrieval
            [
                "Python has various data structures.",
                "Lists are mutable sequences in Python.",
                "Dictionaries store key-value pairs."
            ]
        ],
        "answer": [
            # Good answer
            "Python is a high-level programming language known for its simple and readable syntax.",
            # Poor answer (hallucination despite bad context)
            "Python was created by Guido van Rossum in 1991.",
            # Medium answer
            "A Python list is a data structure that can store multiple items."
        ],
        "ground_truth": [
            "Python is a high-level programming language.",
            "Guido van Rossum created Python.",
            "A Python list is a mutable sequence that can contain multiple elements."
        ]
    }

    return Dataset.from_dict(data)

def main():
    """Run component-level evaluation"""
    # Create dataset
    dataset = create_test_dataset()

    # Initialize evaluator
    evaluator = ComponentEvaluator()

    # Evaluate components
    print("="*70)
    print("Starting Component-Level Evaluation")
    print("="*70 + "\n")

    retrieval_scores = evaluator.evaluate_retriever(dataset)
    print("\n")
    generation_scores = evaluator.evaluate_generator(dataset)

    # Generate report
    report = evaluator.generate_component_report(retrieval_scores, generation_scores)
    print("\n" + report)

    # Save scores
    all_scores = {**retrieval_scores, **generation_scores}
    pd.DataFrame([all_scores]).to_csv("component_scores.csv", index=False)
    print("\n✓ Scores saved to component_scores.csv")

if __name__ == "__main__":
    main()
```

I'll continue with more examples in the next response. The file is getting long, so I'll create separate responses for each README to stay within token limits.