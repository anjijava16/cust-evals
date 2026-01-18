# Braintrust: The Complete Deep-Dive Guide

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

### 1.1 What is Braintrust?

Braintrust is the developer-first platform for building AI products. Founded by former Google and Meta engineers, it's designed around the insight that AI development is fundamentally different from traditional software—it requires constant experimentation, evaluation, and iteration. Braintrust provides best-in-class DX (developer experience) with an opinionated but flexible workflow.

**Core Philosophy:**
- **Developer Experience First**: Beautiful API, instant feedback, joy to use
- **Production-Ready**: Built for real products, not just experiments
- **Evaluation-Driven**: Every change validated against comprehensive test suites
- **Git-Like Workflow**: Familiar branching, diffing, and version control concepts

### 1.2 Key Features

#### Evaluation Framework
- **Flexible Scoring**: Built-in scorers + custom evaluators
- **Comparison View**: Side-by-side diff of any two versions
- **Statistical Significance**: Know if changes actually matter
- **Rich Visualizations**: Interactive tables, charts, and summaries

#### Prompt Playground
- **Interactive Testing**: Test prompts in real-time
- **Version Control**: Every prompt change tracked automatically
- **Template Variables**: Dynamic prompts with Jinja2/Mustache
- **Multi-Model**: Compare GPT-4, Claude, Gemini side-by-side

#### Production Monitoring
- **Real-Time Logging**: Stream production traces
- **Cost Tracking**: Token-level cost analytics
- **Error Detection**: Automatic anomaly detection
- **User Feedback**: Integrate thumbs up/down, ratings

#### Dataset Management
- **Smart Datasets**: Version-controlled evaluation sets
- **Export/Import**: CSV, JSONL, or API
- **Deduplication**: Automatic detection of similar examples
- **Active Learning**: Suggest examples to add based on model failures

#### Developer Experience
- **Fast UI**: Sub-second response times
- **TypeScript SDK**: Full type safety
- **VS Code Extension**: Inline evaluation results
- **CLI Tools**: Terminal-based workflows

### 1.3 When to Use Braintrust

**Perfect For:**
- Startups building AI features requiring fast iteration
- Teams wanting best-in-class developer experience
- Projects needing rigorous evaluation workflows
- Organizations requiring production monitoring + eval
- Engineers who love great tooling
- Rapid prototyping with production quality

**Not Ideal For:**
- Pure research (Weights & Biases better suited)
- Heavy LangChain users (LangSmith more integrated)
- Teams needing self-hosted solutions (enterprise only)
- Minimal evaluation requirements

### 1.4 Comparison Matrix

| Feature | Braintrust | LangSmith | Phoenix | Langfuse | Weave |
|---------|------------|-----------|---------|----------|-------|
| **Developer UX** | ✅✅ Best | ✅ Good | ⚠️ Basic | ✅ Good | ✅ Good |
| **Evaluation Focus** | ✅✅ Core | ✅ Good | ⚠️ Limited | ⚠️ Limited | ✅ Good |
| **Prompt Playground** | ✅✅ Best | ✅ Good | ❌ No | ⚠️ Basic | ⚠️ Basic |
| **Version Diffing** | ✅✅ Excellent | ✅ Good | ❌ No | ⚠️ Basic | ✅ Good |
| **Speed** | ✅✅ Fastest | ✅ Fast | ✅ Fast | ✅ Fast | ✅ Fast |
| **Multi-Model** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Self-Hosting** | ⚠️ Enterprise | ❌ No | ✅ Yes | ✅ Yes | ❌ No |
| **Cost** | Free + Usage | Subscription | Free | Free + Cloud | Free |
| **Statistical Testing** | ✅ Built-in | ⚠️ Limited | ❌ No | ❌ No | ⚠️ Basic |
| **TypeScript** | ✅✅ First-class | ✅ Good | ⚠️ Limited | ✅ Good | ⚠️ Limited |

---

## 2. Complete Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Your Application Code                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Python/TS/JS with Braintrust SDK                      │ │
│  │  - bt.eval() for evaluation                            │ │
│  │  - bt.traced() for production logging                  │ │
│  │  - bt.prompt() for prompt management                   │ │
│  └──────────────┬─────────────────────────────────────────┘ │
│                 │                                            │
└─────────────────┼──────────────────────────────────────────┘
                  │ HTTPS API
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Braintrust Platform (Cloud)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Evaluation  │  │   Prompts    │  │   Logging    │      │
│  │  Engine      │  │  Registry    │  │  Pipeline    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                           │                                  │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │  Analytics & Visualization Engine                      │ │
│  │  - Statistical analysis                                │ │
│  │  - Diff computation                                    │ │
│  │  - Real-time dashboards                                │ │
│  └────────────────────────┬───────────────────────────────┘ │
│                           │                                  │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │  Web UI (React)                                        │ │
│  │  - Evaluation results                                  │ │
│  │  - Prompt playground                                   │ │
│  │  - Production monitoring                               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Core Workflow

```
1. Develop
   ├── Write prompt/model
   ├── Create evaluation dataset
   └── Define scorers

2. Evaluate
   ├── Run bt.eval() locally
   ├── View results in UI
   └── Compare with baseline

3. Iterate
   ├── Modify prompt/model
   ├── Re-evaluate
   └── View diff

4. Deploy
   ├── Promote winning version
   ├── Deploy to production
   └── Monitor with bt.traced()

5. Monitor
   ├── Track production metrics
   ├── Collect edge cases
   └── Add to eval dataset

6. Repeat
   └── Continuous improvement
```

### 2.3 Key Concepts Diagram

```
Project
├── Experiments (git-like commits)
│   ├── Experiment A (baseline)
│   ├── Experiment B (prompt v2)
│   └── Experiment C (new model)
│
├── Datasets (versioned)
│   ├── Dataset v1 (50 examples)
│   └── Dataset v2 (100 examples)
│
├── Prompts (versioned)
│   ├── Prompt v1 (original)
│   ├── Prompt v2 (refined)
│   └── Prompt v3 (production)
│
└── Traces (production logs)
    ├── Request 1 (user-123)
    ├── Request 2 (user-456)
    └── ...
```

---

## 3. Installation & Setup

### 3.1 Installation

```bash
# Python
pip install braintrust

# Node.js
npm install braintrust

# TypeScript
npm install braintrust
npm install --save-dev @types/braintrust

# Verify installation
braintrust --version
```

### 3.2 Quick Start (Python)

```python
import braintrust
import os

# Set API key (get from https://braintrust.dev)
os.environ["BRAINTRUST_API_KEY"] = "your-key-here"

# Or login interactively
braintrust.login()

# Initialize project
project = braintrust.init(
    project="my-first-project",
    api_key=os.environ.get("BRAINTRUST_API_KEY")
)

# Log some data
project.log(
    inputs={"question": "What is 2+2?"},
    output="4",
    expected="4",
    scores={"correctness": 1.0}
)

print("View results at: https://braintrust.dev")
```

### 3.3 Quick Start (TypeScript)

```typescript
import { init, log } from "braintrust";

// Initialize project
const project = init({
  project: "my-first-project",
  apiKey: process.env.BRAINTRUST_API_KEY,
});

// Log data
log({
  inputs: { question: "What is 2+2?" },
  output: "4",
  expected: "4",
  scores: { correctness: 1.0 },
});
```

### 3.4 Configuration

```python
import braintrust

# Full configuration
project = braintrust.init(
    project="my-project",
    api_key="...",

    # Experiment metadata
    experiment="prompt-v2",
    description="Testing new prompt template",
    metadata={
        "author": "alice@example.com",
        "model": "gpt-4-turbo",
        "temperature": 0.7
    },

    # Dataset
    dataset=braintrust.load_dataset(
        project="my-project",
        name="eval-set-v1"
    ),

    # Options
    open=True,  # Open UI after eval
    update=True,  # Update existing experiment
)
```

---

## 4. Core Concepts

### 4.1 Projects

Projects are top-level containers.

```python
import braintrust

# Create/open project
project = braintrust.init(project="customer-support-bot")

# Projects contain:
# - Experiments (evaluation runs)
# - Datasets (test sets)
# - Prompts (templates)
# - Traces (production logs)
```

### 4.2 Experiments

Experiments are individual evaluation runs, like git commits.

```python
import braintrust

# Run experiment
project = braintrust.init(
    project="my-project",
    experiment="baseline",  # Name this run
    metadata={"version": "1.0"}
)

# Log results
for example in dataset:
    output = model.predict(example["input"])
    project.log(
        inputs=example["input"],
        output=output,
        expected=example["expected"],
        scores={"accuracy": compute_accuracy(output, example["expected"])}
    )

# Experiments are automatically compared
```

### 4.3 Datasets

Datasets are versioned collections of test cases.

```python
import braintrust

# Create dataset
dataset = braintrust.init_dataset(
    project="my-project",
    name="qa-eval-set",
    description="QA evaluation examples"
)

# Add examples
examples = [
    {
        "input": {"question": "What is ML?"},
        "expected": "Machine Learning is...",
        "metadata": {"difficulty": "easy"}
    },
    {
        "input": {"question": "Explain backpropagation"},
        "expected": "Backpropagation is...",
        "metadata": {"difficulty": "hard"}
    }
]

for example in examples:
    dataset.insert(**example)

# Use dataset in evaluation
eval_dataset = braintrust.load_dataset(
    project="my-project",
    name="qa-eval-set"
)
```

### 4.4 Scorers

Scorers evaluate outputs.

```python
import braintrust
from braintrust import Score

# Simple scorer
def exact_match(output, expected):
    """Binary exact match"""
    return Score(
        name="exact_match",
        score=1.0 if output == expected else 0.0
    )

# Scorer with metadata
def semantic_similarity(output, expected):
    """Compute semantic similarity"""
    similarity = compute_similarity(output, expected)

    return Score(
        name="semantic_similarity",
        score=similarity,
        metadata={
            "output_length": len(output),
            "expected_length": len(expected)
        }
    )

# LLM-based scorer
from openai import OpenAI
client = OpenAI()

def llm_judge(output, expected, input):
    """Use LLM as judge"""

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{
            "role": "user",
            "content": f"""Score this answer (0-1):

Question: {input['question']}
Expected: {expected}
Actual: {output}

Return only a number."""
        }]
    )

    score = float(response.choices[0].message.content.strip())

    return Score(
        name="llm_judge",
        score=score,
        metadata={"model": "gpt-4-turbo-preview"}
    )
```

### 4.5 Prompts

Prompts are versioned templates.

```python
import braintrust
from braintrust import Prompt

# Create prompt in UI or via API
prompt = braintrust.load_prompt(
    project="my-project",
    slug="customer-support-prompt"
)

# Use prompt
messages = prompt.build(
    question="How do I reset my password?",
    user_name="Alice"
)

# Messages rendered with template variables
# Auto-versioned and tracked
```

---

## 5. Complete Examples Section

### Example 1: Basic Evaluation

**Use Case**: Evaluate a simple QA model

```python
import braintrust
from openai import OpenAI
from braintrust import Eval

# Initialize
client = OpenAI()

# Define task
def qa_task(input):
    """Answer questions"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer questions concisely."},
            {"role": "user", "content": input["question"]}
        ]
    )

    return response.choices[0].message.content

# Define scorer
def exact_match(output, expected):
    """Check exact match"""
    match = output.strip().lower() == expected.strip().lower()
    return 1.0 if match else 0.0

# Create dataset
dataset = [
    {
        "input": {"question": "What is 2+2?"},
        "expected": "4"
    },
    {
        "input": {"question": "Capital of France?"},
        "expected": "Paris"
    },
    {
        "input": {"question": "Largest planet?"},
        "expected": "Jupiter"
    }
]

# Run evaluation
if __name__ == "__main__":
    Eval(
        project="qa-basic",
        experiment="gpt-3.5-turbo",
        data=dataset,
        task=qa_task,
        scores=[exact_match]
    )

    print("✅ View results at: https://braintrust.dev")

# Output:
# qa-basic/gpt-3.5-turbo
# ========================================
# exact_match:   0.67 (2/3)
#
# View details at: https://braintrust.dev/...
```

**Braintrust UI View:**
```
Experiment: gpt-3.5-turbo

Overall Scores:
├── exact_match: 0.67 (2/3)

Examples (3):
┌─────────┬─────────────────────────┬──────────┬──────────┬──────────┐
│ Input   │ Output                  │ Expected │ Match    │ Score    │
├─────────┼─────────────────────────┼──────────┼──────────┼──────────┤
│ 2+2?    │ 4                       │ 4        │ ✅       │ 1.0      │
│ Capital?│ Paris                   │ Paris    │ ✅       │ 1.0      │
│ Planet? │ Jupiter is the largest  │ Jupiter  │ ❌       │ 0.0      │
└─────────┴─────────────────────────┴──────────┴──────────┴──────────┘

Failed Examples (1):
- Largest planet? → "Jupiter is the largest" vs "Jupiter"
  Issue: Model added extra words
```

### Example 2: Prompt Comparison

**Use Case**: Compare two prompt versions

```python
import braintrust
from openai import OpenAI
from braintrust import Eval

client = OpenAI()

# Define prompts
PROMPT_V1 = "Answer the question concisely."

PROMPT_V2 = """You are a helpful assistant. Answer the question accurately and concisely.
Provide just the answer without extra explanation."""

# Create task functions
def task_v1(input):
    """V1: Simple prompt"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT_V1},
            {"role": "user", "content": input["question"]}
        ]
    )
    return response.choices[0].message.content

def task_v2(input):
    """V2: Detailed prompt"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT_V2},
            {"role": "user", "content": input["question"]}
        ]
    )
    return response.choices[0].message.content

# Scorers
def exact_match(output, expected):
    """Exact match scorer"""
    return 1.0 if output.strip().lower() == expected.strip().lower() else 0.0

def length_check(output, expected):
    """Check if output is concise"""
    output_words = len(output.split())
    expected_words = len(expected.split())

    # Penalize if output is >2x expected length
    if output_words > expected_words * 2:
        return 0.5
    return 1.0

# Dataset
dataset = [
    {"input": {"question": "What is 2+2?"}, "expected": "4"},
    {"input": {"question": "Capital of France?"}, "expected": "Paris"},
    {"input": {"question": "Largest planet?"}, "expected": "Jupiter"},
    {"input": {"question": "Speed of light?"}, "expected": "299,792,458 m/s"},
    {"input": {"question": "Boiling point of water?"}, "expected": "100°C"},
]

if __name__ == "__main__":
    # Evaluate V1
    print("Evaluating Prompt V1...")
    Eval(
        project="prompt-comparison",
        experiment="prompt-v1",
        data=dataset,
        task=task_v1,
        scores=[exact_match, length_check]
    )

    # Evaluate V2
    print("Evaluating Prompt V2...")
    Eval(
        project="prompt-comparison",
        experiment="prompt-v2",
        data=dataset,
        task=task_v2,
        scores=[exact_match, length_check]
    )

    print("\n✅ View side-by-side comparison in Braintrust UI")
    print("Navigate to: https://braintrust.dev")
```

**Braintrust UI Comparison:**
```
Prompt Comparison: V1 vs V2

Overall Scores:
                 │ V1    │ V2    │ Δ      │
─────────────────┼───────┼───────┼────────┤
exact_match      │ 0.60  │ 0.80  │ +0.20 ✅│
length_check     │ 0.70  │ 0.90  │ +0.20 ✅│
─────────────────┴───────┴───────┴────────┘

Statistical Significance: p < 0.05 ✅

Example Diff (Largest planet):
V1: "Jupiter is the largest planet in our solar system"
V2: "Jupiter"
Expected: "Jupiter"

Winner: Prompt V2 (+0.20 average improvement)
```

### Example 3: RAG Evaluation

**Use Case**: Evaluate RAG system with multiple metrics

```python
import braintrust
from openai import OpenAI
from braintrust import Eval
from typing import Dict, List

client = OpenAI()

# Simulated document store
DOCUMENTS = {
    "doc1": "Python is a high-level programming language.",
    "doc2": "Machine learning is a subset of AI.",
    "doc3": "Neural networks are inspired by biological brains.",
    "doc4": "Data science involves statistics and programming.",
    "doc5": "APIs allow different software to communicate."
}

class RAGSystem:
    """Simple RAG system"""

    def __init__(self, top_k: int = 3):
        self.top_k = top_k

    def retrieve(self, query: str) -> List[str]:
        """Retrieve relevant documents"""
        # Simplified retrieval (mock)
        # In production: use vector search

        # For demo, return first top_k docs
        return list(DOCUMENTS.values())[:self.top_k]

    def generate(self, query: str, context: List[str]) -> str:
        """Generate answer from context"""

        context_str = "\n".join(context)

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "Answer based on provided context only."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context_str}\n\nQuestion: {query}"
                }
            ]
        )

        return response.choices[0].message.content

    def query(self, question: str) -> Dict:
        """Complete RAG pipeline"""

        docs = self.retrieve(question)
        answer = self.generate(question, docs)

        return {
            "answer": answer,
            "sources": docs,
            "num_sources": len(docs)
        }

# Define task
rag_system = RAGSystem(top_k=3)

def rag_task(input):
    """RAG task"""
    result = rag_system.query(input["question"])
    return result["answer"]

# Define scorers
def answer_correctness(output, expected):
    """Check if answer is correct"""

    # Use LLM to judge correctness
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{
            "role": "user",
            "content": f"""Is this answer correct? (Yes/No)

Expected: {expected}
Actual: {output}

Return only Yes or No."""
        }]
    )

    result = response.choices[0].message.content.strip().lower()
    return 1.0 if "yes" in result else 0.0

def answer_completeness(output, expected):
    """Check if answer is complete"""

    # Check length and detail
    output_words = len(output.split())

    if output_words < 10:
        return 0.5  # Too short

    if output_words > 100:
        return 0.7  # Too long

    return 1.0  # Good length

def groundedness(output, expected, input):
    """Check if answer is grounded in sources"""

    # This would check citations in production
    # For demo, simplified check

    has_citation = "[" in output or "doc" in output.lower()

    return 1.0 if has_citation else 0.5

# Dataset
dataset = [
    {
        "input": {"question": "What is Python?"},
        "expected": "Python is a high-level programming language"
    },
    {
        "input": {"question": "What is machine learning?"},
        "expected": "Machine learning is a subset of AI"
    },
    {
        "input": {"question": "What are neural networks?"},
        "expected": "Neural networks are inspired by biological brains"
    },
    {
        "input": {"question": "What is data science?"},
        "expected": "Data science involves statistics and programming"
    }
]

if __name__ == "__main__":
    Eval(
        project="rag-evaluation",
        experiment="rag-v1",
        data=dataset,
        task=rag_task,
        scores=[
            answer_correctness,
            answer_completeness,
            groundedness
        ],
        metadata={
            "top_k": 3,
            "model": "gpt-4-turbo-preview"
        }
    )

    print("✅ View comprehensive RAG metrics in Braintrust UI")
```

**Braintrust UI RAG Dashboard:**
```
RAG Evaluation Results

Overall Scores (4 examples):
├── answer_correctness: 0.75 (3/4)
├── answer_completeness: 0.88
├── groundedness: 0.62
└── Average: 0.75

Performance by Question Type:
├── Definitions: 0.83 ✅
├── Explanations: 0.67 ⚠️

Issues Detected:
├── Low groundedness (38% missing citations)
└── Incomplete answer on "data science"

Recommendations:
1. Add citation formatting to prompt
2. Increase context window
3. Improve retrieval for "data science" queries
```

### Example 4: Model Comparison (GPT-4 vs Claude)

**Use Case**: Compare different models systematically

```python
import braintrust
from openai import OpenAI
from anthropic import Anthropic
from braintrust import Eval

openai_client = OpenAI()
anthropic_client = Anthropic()

# Define tasks for different models
def gpt4_task(input):
    """GPT-4 Turbo"""
    response = openai_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input["prompt"]}
        ]
    )
    return response.choices[0].message.content

def gpt35_task(input):
    """GPT-3.5 Turbo"""
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input["prompt"]}
        ]
    )
    return response.choices[0].message.content

def claude_task(input):
    """Claude 3 Sonnet"""
    response = anthropic_client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": input["prompt"]}
        ]
    )
    return response.content[0].text

# Scorers
def quality_score(output, expected):
    """LLM-based quality scorer"""

    response = openai_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{
            "role": "user",
            "content": f"""Rate this answer's quality (0-1):

Expected: {expected}
Actual: {output}

Consider accuracy, completeness, and clarity.
Return only a number between 0 and 1."""
        }],
        temperature=0.0
    )

    return float(response.choices[0].message.content.strip())

def conciseness_score(output, expected):
    """Check conciseness"""

    output_words = len(output.split())
    expected_words = len(expected.split())

    ratio = output_words / expected_words if expected_words > 0 else 1

    # Prefer outputs within 0.5x - 1.5x expected length
    if 0.5 <= ratio <= 1.5:
        return 1.0
    elif ratio < 0.5:
        return 0.5  # Too short
    else:
        return max(0.0, 1.0 - (ratio - 1.5) * 0.2)  # Penalize verbosity

# Dataset
dataset = [
    {
        "input": {"prompt": "Explain quantum computing in simple terms"},
        "expected": "Quantum computing uses quantum mechanics principles..."
    },
    {
        "input": {"prompt": "What is the difference between AI and ML?"},
        "expected": "AI is the broader concept, ML is a subset..."
    },
    {
        "input": {"prompt": "How does a neural network learn?"},
        "expected": "Neural networks learn through backpropagation..."
    },
    {
        "input": {"prompt": "What is an API?"},
        "expected": "An API allows different software to communicate..."
    },
    {
        "input": {"prompt": "Explain REST in one sentence"},
        "expected": "REST is an architectural style for web services..."
    }
]

if __name__ == "__main__":
    # Evaluate all models
    models = [
        ("gpt-4-turbo", gpt4_task),
        ("gpt-3.5-turbo", gpt35_task),
        ("claude-3-sonnet", claude_task)
    ]

    for model_name, task_fn in models:
        print(f"\nEvaluating {model_name}...")

        Eval(
            project="model-comparison",
            experiment=model_name,
            data=dataset,
            task=task_fn,
            scores=[quality_score, conciseness_score],
            metadata={"model": model_name}
        )

    print("\n✅ View model comparison in Braintrust UI")
    print("See leaderboard and statistical significance")
```

**Braintrust Model Comparison:**
```
Model Comparison Leaderboard

                    │ GPT-4    │ GPT-3.5  │ Claude 3 │
────────────────────┼──────────┼──────────┼──────────┤
quality_score       │ 0.92 ⭐  │ 0.78     │ 0.85     │
conciseness_score   │ 0.85     │ 0.70     │ 0.88 ⭐  │
────────────────────┼──────────┼──────────┼──────────┤
Average             │ 0.89 🥇  │ 0.74 🥉  │ 0.87 🥈  │

Statistical Significance:
├── GPT-4 vs GPT-3.5: p < 0.01 ✅
├── GPT-4 vs Claude: p = 0.23 (not significant)
└── Claude vs GPT-3.5: p < 0.05 ✅

Cost Analysis:
├── GPT-4: $0.12 per eval
├── GPT-3.5: $0.02 per eval  ← Cheapest
├── Claude: $0.08 per eval

Recommendation:
- Production: GPT-4 (best quality)
- Development: GPT-3.5 (cost-effective)
- Alternative: Claude 3 (good balance)
```

### Example 5: Production Monitoring

**Use Case**: Log production requests and monitor quality

```python
import braintrust
from openai import OpenAI
from datetime import datetime

client = OpenAI()

# Initialize for logging (not evaluation)
logger = braintrust.init_logger(
    project="chatbot-production",
    api_key=os.environ.get("BRAINTRUST_API_KEY")
)

class ProductionChatbot:
    """Production chatbot with logging"""

    def __init__(self):
        self.client = OpenAI()

    def chat(self, user_id: str, message: str) -> dict:
        """Handle chat request"""

        start_time = datetime.now()

        # Generate response
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )

        assistant_message = response.choices[0].message.content
        latency = (datetime.now() - start_time).total_seconds()

        # Log to Braintrust
        logger.log(
            inputs={
                "user_id": user_id,
                "message": message,
                "timestamp": start_time.isoformat()
            },
            output=assistant_message,
            metadata={
                "model": "gpt-4-turbo-preview",
                "latency_seconds": latency,
                "tokens": response.usage.total_tokens,
                "cost": self.calculate_cost(response.usage)
            },
            tags=["production", "chatbot"]
        )

        return {
            "response": assistant_message,
            "latency": latency
        }

    def add_user_feedback(self, log_id: str, feedback: dict):
        """Add user feedback to logged request"""

        logger.update_span(
            span_id=log_id,
            scores={
                "user_rating": feedback.get("rating", 0) / 5.0,  # 0-1 scale
                "helpful": 1.0 if feedback.get("helpful") else 0.0
            },
            metadata={
                "feedback_timestamp": datetime.now().isoformat(),
                "feedback_comment": feedback.get("comment")
            }
        )

    def calculate_cost(self, usage) -> float:
        """Calculate cost"""
        # GPT-4 Turbo pricing
        input_cost = usage.prompt_tokens * 0.00001
        output_cost = usage.completion_tokens * 0.00003
        return input_cost + output_cost

if __name__ == "__main__":
    chatbot = ProductionChatbot()

    # Simulate production traffic
    requests = [
        {"user_id": "user-1", "message": "How do I reset my password?"},
        {"user_id": "user-2", "message": "What are your business hours?"},
        {"user_id": "user-3", "message": "I need help with my order"},
    ]

    for req in requests:
        print(f"\nUser: {req['message']}")

        result = chatbot.chat(
            user_id=req["user_id"],
            message=req["message"]
        )

        print(f"Bot: {result['response'][:100]}...")
        print(f"Latency: {result['latency']:.2f}s")

    print("\n✅ View production logs in Braintrust UI")
    print("Monitor: latency, costs, user feedback")

# Braintrust Production Dashboard:
# - Real-time request stream
# - Latency p50/p95/p99
# - Cost tracking
# - User feedback aggregation
# - Anomaly detection
```

### Example 6: Dataset Management

**Use Case**: Build and version evaluation datasets

```python
import braintrust
from typing import List, Dict

# Create new dataset
def create_initial_dataset():
    """Create initial evaluation dataset"""

    dataset = braintrust.init_dataset(
        project="qa-system",
        name="eval-set",
        description="QA evaluation examples v1"
    )

    examples = [
        {
            "input": {"question": "What is Python?"},
            "expected": "Python is a programming language",
            "metadata": {"category": "programming", "difficulty": "easy"}
        },
        {
            "input": {"question": "Explain machine learning"},
            "expected": "Machine learning is...",
            "metadata": {"category": "AI", "difficulty": "medium"}
        }
    ]

    for example in examples:
        dataset.insert(**example)

    print(f"✅ Created dataset with {len(examples)} examples")

    return dataset

# Add examples from production failures
def add_production_failures():
    """Add failed production examples to dataset"""

    dataset = braintrust.load_dataset(
        project="qa-system",
        name="eval-set"
    )

    # Get failed traces from production
    # (In real app, query Braintrust API)

    new_examples = [
        {
            "input": {"question": "What is quantum computing?"},
            "expected": "Quantum computing uses quantum mechanics...",
            "metadata": {
                "source": "production_failure",
                "user_id": "user-123",
                "date": "2026-01-18"
            }
        }
    ]

    for example in new_examples:
        dataset.insert(**example)

    print(f"✅ Added {len(new_examples)} examples from production")

# Export dataset
def export_dataset():
    """Export dataset to CSV"""

    dataset = braintrust.load_dataset(
        project="qa-system",
        name="eval-set"
    )

    # Export to CSV
    dataset.export("eval_set.csv")

    print("✅ Exported to eval_set.csv")

# Import dataset
def import_dataset():
    """Import dataset from CSV"""

    dataset = braintrust.init_dataset(
        project="qa-system",
        name="eval-set-imported"
    )

    # Import from CSV
    dataset.import_csv("eval_set.csv")

    print("✅ Imported dataset")

if __name__ == "__main__":
    # Workflow
    create_initial_dataset()
    add_production_failures()
    export_dataset()

    print("\n✅ View dataset in Braintrust UI")
```

### Example 7: Custom Scorers with Context

**Use Case**: Create sophisticated scorers using all available context

```python
import braintrust
from openai import OpenAI
from braintrust import Eval, Score
from typing import Dict, Any

client = OpenAI()

# Scorer with full context
def comprehensive_scorer(output: str, expected: str, input: Dict, metadata: Dict = None) -> Score:
    """Comprehensive scorer using all available data"""

    # Access input fields
    question = input.get("question", "")
    difficulty = metadata.get("difficulty", "unknown") if metadata else "unknown"

    # Check correctness
    is_correct = expected.lower() in output.lower()

    # Check completeness based on difficulty
    min_length = {"easy": 20, "medium": 50, "hard": 100}.get(difficulty, 30)
    is_complete = len(output) >= min_length

    # Calculate score
    if is_correct and is_complete:
        score = 1.0
    elif is_correct:
        score = 0.7
    elif is_complete:
        score = 0.3
    else:
        score = 0.0

    return Score(
        name="comprehensive",
        score=score,
        metadata={
            "correct": is_correct,
            "complete": is_complete,
            "length": len(output),
            "difficulty": difficulty
        }
    )

# Multi-aspect scorer returning multiple scores
def multi_aspect_scorer(output: str, expected: str, input: Dict) -> Dict[str, Score]:
    """Return multiple scores"""

    scores = {}

    # Accuracy
    scores["accuracy"] = Score(
        name="accuracy",
        score=1.0 if expected.lower() in output.lower() else 0.0
    )

    # Clarity (using LLM)
    clarity_response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{
            "role": "user",
            "content": f"Rate clarity (0-1): {output}"
        }],
        temperature=0.0
    )

    scores["clarity"] = Score(
        name="clarity",
        score=float(clarity_response.choices[0].message.content.strip())
    )

    # Conciseness
    word_count = len(output.split())
    conciseness = max(0.0, 1.0 - (word_count - 50) / 100) if word_count > 50 else 1.0

    scores["conciseness"] = Score(
        name="conciseness",
        score=conciseness,
        metadata={"word_count": word_count}
    )

    return scores

# Dataset with metadata
dataset = [
    {
        "input": {"question": "What is 2+2?"},
        "expected": "4",
        "metadata": {"difficulty": "easy", "category": "math"}
    },
    {
        "input": {"question": "Explain relativity"},
        "expected": "Relativity describes...",
        "metadata": {"difficulty": "hard", "category": "physics"}
    }
]

# Task
def simple_task(input):
    """Simple QA task"""
    return f"Answer to {input['question']}"

if __name__ == "__main__":
    Eval(
        project="custom-scorers",
        experiment="multi-aspect",
        data=dataset,
        task=simple_task,
        scores=[comprehensive_scorer, multi_aspect_scorer]
    )

    print("✅ View multi-aspect scoring in Braintrust UI")
```

### Example 8: Async Evaluation (High Performance)

**Use Case**: Evaluate large datasets quickly with async

```python
import braintrust
from openai import AsyncOpenAI
from braintrust import Eval
import asyncio

client = AsyncOpenAI()

# Async task
async def async_task(input):
    """Async QA task"""

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer concisely."},
            {"role": "user", "content": input["question"]}
        ]
    )

    return response.choices[0].message.content

# Scorer
def exact_match(output, expected):
    """Exact match"""
    return 1.0 if output.strip() == expected.strip() else 0.0

# Large dataset
dataset = [
    {
        "input": {"question": f"What is {i}+{i}?"},
        "expected": str(i + i)
    }
    for i in range(100)  # 100 examples
]

if __name__ == "__main__":
    # Async evaluation (much faster)
    Eval(
        project="async-eval",
        experiment="parallel-v1",
        data=dataset,
        task=async_task,
        scores=[exact_match],
        max_concurrency=10  # Run 10 at a time
    )

    print("✅ Async evaluation completed")
    print("View performance metrics in Braintrust UI")

# Performance:
# Sequential: ~200 seconds
# Async (10 concurrent): ~25 seconds
# 8x speedup!
```

### Example 9: Prompt Templates and Variables

**Use Case**: Use versioned prompt templates with variables

```python
import braintrust
from openai import OpenAI

client = OpenAI()

# Define prompt template in Braintrust UI or via SDK
# Template stored with name: "customer-support"
# Template content:
"""
You are a {{tone}} customer support agent for {{company}}.

Customer question: {{question}}

Provide a {{response_style}} response.
"""

# Load and use prompt
def use_prompt_template(question: str) -> str:
    """Use versioned prompt template"""

    # Load prompt
    prompt = braintrust.load_prompt(
        project="support-bot",
        slug="customer-support",
        version="latest"  # or specific version like "v2"
    )

    # Build with variables
    messages = prompt.build(
        tone="friendly and professional",
        company="Acme Inc",
        question=question,
        response_style="detailed but concise"
    )

    # Use with OpenAI
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages
    )

    return response.choices[0].message.content

# Compare prompt versions
def compare_prompt_versions(question: str):
    """Compare different prompt versions"""

    versions = ["v1", "v2", "v3"]
    results = {}

    for version in versions:
        prompt = braintrust.load_prompt(
            project="support-bot",
            slug="customer-support",
            version=version
        )

        messages = prompt.build(
            tone="friendly",
            company="Acme",
            question=question,
            response_style="concise"
        )

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages
        )

        results[version] = response.choices[0].message.content

    return results

if __name__ == "__main__":
    question = "How do I return a product?"

    # Use latest prompt
    answer = use_prompt_template(question)
    print(f"Answer: {answer}\n")

    # Compare versions
    print("Comparing prompt versions...")
    results = compare_prompt_versions(question)

    for version, answer in results.items():
        print(f"\n{version}: {answer[:100]}...")

    print("\n✅ View prompt versions and comparison in Braintrust UI")
```

### Example 10: Integration with CI/CD

**Use Case**: Run evaluations in CI/CD pipeline

```python
# evaluation_script.py
import braintrust
from openai import OpenAI
from braintrust import Eval
import sys

client = OpenAI()

def qa_task(input):
    """QA task"""
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": input["question"]}]
    )
    return response.choices[0].message.content

def quality_scorer(output, expected):
    """Quality check"""
    # Simplified for demo
    return 1.0 if expected.lower() in output.lower() else 0.0

# Load dataset
dataset = braintrust.load_dataset(
    project="ci-cd-eval",
    name="smoke-tests"
)

if __name__ == "__main__":
    # Run evaluation
    result = Eval(
        project="ci-cd-eval",
        experiment=f"ci-run-{os.environ.get('CI_COMMIT_SHA', 'local')}",
        data=dataset,
        task=qa_task,
        scores=[quality_scorer],
        metadata={
            "ci_commit": os.environ.get("CI_COMMIT_SHA"),
            "ci_branch": os.environ.get("CI_BRANCH"),
            "ci_pipeline": os.environ.get("CI_PIPELINE_ID")
        }
    )

    # Check if evaluation passed threshold
    avg_score = result.summary["quality_scorer"]["mean"]
    threshold = 0.8

    if avg_score < threshold:
        print(f"❌ Evaluation failed: {avg_score:.2f} < {threshold}")
        sys.exit(1)  # Fail CI
    else:
        print(f"✅ Evaluation passed: {avg_score:.2f} >= {threshold}")
        sys.exit(0)  # Pass CI
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
          pip install braintrust openai

      - name: Run evaluation
        env:
          BRAINTRUST_API_KEY: ${{ secrets.BRAINTRUST_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          CI_COMMIT_SHA: ${{ github.sha }}
          CI_BRANCH: ${{ github.ref }}
          CI_PIPELINE_ID: ${{ github.run_id }}
        run: |
          python evaluation_script.py

      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '✅ LLM evaluation passed! View results: https://braintrust.dev'
            })
```

---

## 6. Advanced Usage

### 6.1 Statistical Analysis

Braintrust automatically computes statistical significance when comparing experiments.

```python
# Braintrust computes:
# - T-tests for score differences
# - Confidence intervals
# - P-values
# - Effect sizes

# View in UI to see if improvements are statistically significant
```

### 6.2 Custom Visualizations

```python
# Export data for custom analysis
import pandas as pd

# Get experiment data (via UI export or API)
# Analyze in Jupyter notebooks
# Create custom plots
```

### 6.3 Hooks and Callbacks

```python
# (Coming soon in Braintrust SDK)
# Add hooks for custom processing

def on_example_complete(result):
    """Called after each example"""
    if result.score < 0.5:
        notify_team(result)

Eval(
    project="my-project",
    data=dataset,
    task=my_task,
    hooks={"on_example_complete": on_example_complete}
)
```

---

## 7. Best Practices

### 7.1 Dataset Management

```python
# DO: Version datasets
# DO: Include metadata (difficulty, category)
# DO: Add production failures to datasets
# DO: Keep datasets < 1000 examples for fast iteration

# DON'T: Hardcode datasets in code
# DON'T: Mix different task types in one dataset
```

### 7.2 Experiment Naming

```python
# DO: Use descriptive names
Eval(experiment="prompt-v2-increased-temperature")

# DON'T: Use generic names
Eval(experiment="test1")  # ❌
```

### 7.3 Scorer Design

```python
# DO: Return Score objects with metadata
def my_scorer(output, expected):
    return Score(
        name="my_score",
        score=0.85,
        metadata={"details": "..."}
    )

# DO: Create multiple focused scorers
# DON'T: Create one giant scorer for everything
```

---

## 8. Integration Guide

### 8.1 Framework Integrations

Braintrust works with any Python/JS code. No special integrations needed.

```python
# Works with:
# - Raw OpenAI/Anthropic/Google
# - LangChain
# - LlamaIndex
# - Autogen
# - Any custom code
```

### 8.2 Production Logging

```python
# Use bt.traced() for production
from braintrust import traced

@traced
def production_endpoint(request):
    """Automatically logged"""
    return process(request)
```

---

## 9. Troubleshooting

### 9.1 Common Issues

**Slow evaluations:**
```python
# Use async tasks
# Increase max_concurrency
Eval(..., max_concurrency=20)
```

**API key issues:**
```python
# Check environment variable
import os
print(os.environ.get("BRAINTRUST_API_KEY"))

# Or pass explicitly
braintrust.init(api_key="your-key")
```

---

## 10. API Reference

### 10.1 Core Functions

```python
# Initialization
braintrust.init(project, experiment, api_key)
braintrust.init_logger(project, api_key)
braintrust.init_dataset(project, name)

# Evaluation
braintrust.Eval(project, experiment, data, task, scores)

# Logging
logger.log(inputs, output, expected, scores, metadata)

# Prompts
braintrust.load_prompt(project, slug, version)

# Datasets
braintrust.load_dataset(project, name)
```

---

## 11. Performance & Optimization

### 11.1 Evaluation Speed

- Async tasks: 10-20x faster
- Concurrent execution
- Optimized for large datasets

### 11.2 Cost Optimization

- Use cheaper models for scoring (GPT-3.5)
- Cache LLM judgments
- Sample large datasets

---

## 12. Security Considerations

### 12.1 API Keys

```python
# Store in environment variables
# Never commit to git
# Use secrets management in production
```

### 12.2 Data Privacy

```python
# Sanitize PII before logging
# Use Braintrust enterprise for data residency
# Enable audit logs
```

---

## 13. References & Resources

### 13.1 Official Links

- Website: https://braintrust.dev
- Documentation: https://braintrust.dev/docs
- GitHub: https://github.com/braintrustdata/braintrust-sdk
- Discord: https://discord.gg/braintrust

### 13.2 Pricing

- Free: 1M observations/month
- Pro: $49/month (10M observations)
- Team: $199/month (100M observations)
- Enterprise: Custom pricing

### 13.3 Comparison

**vs LangSmith:**
- Braintrust: Evaluation-first, better DX
- LangSmith: Production-first, LangChain native

**vs Weave:**
- Braintrust: Better UI, faster
- Weave: W&B integration, more ML-focused

---

## Conclusion

Braintrust delivers the best developer experience for building AI products. Its evaluation-driven workflow, beautiful UI, and production-ready monitoring make it ideal for teams that value both speed and quality. The focus on statistical rigor ensures you ship improvements that actually matter.

**Key Strengths:**
- Best-in-class developer experience
- Evaluation-driven workflow
- Statistical significance testing
- Fast, beautiful UI
- Production monitoring

**Best For:**
- Startups building AI features
- Teams valuing great tooling
- Evaluation-focused workflows
- Rapid iteration
- Production deployments

Start building better AI products with `pip install braintrust`!
