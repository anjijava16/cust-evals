# Weave: The Complete Deep-Dive Guide

**Version**: 1.0.0 | **Updated**: January 2026 | **License**: Apache 2.0

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

### 1.1 What is Weave?

Weave is Weights & Biases' lightweight experiment tracking toolkit specifically designed for LLM applications. It brings the battle-tested W&B experimentation infrastructure to the world of prompts, chains, and agents. Built by the team behind the leading ML experiment platform, Weave inherits best-in-class visualization, versioning, and collaboration features.

**Core Philosophy:**
- **Experiment Everything**: Track prompts, models, and configs with automatic versioning
- **Lightweight & Fast**: Simple decorators, minimal code changes
- **Visualization First**: Rich UI for comparing runs and debugging failures
- **W&B Ecosystem**: Seamless integration with W&B's full platform

### 1.2 Key Features

#### Automatic Tracking
- **Decorator-Based**: `@weave.op()` decorator tracks function calls automatically
- **Versioning**: Automatic versioning of prompts, models, and datasets
- **Call Graph**: Visual trace of execution flow
- **Type System**: Rich type system for tracking complex objects

#### Experiment Management
- **Run Comparison**: Side-by-side comparison of different prompts/models
- **Dataset Management**: Version and track evaluation datasets
- **Model Registry**: Centralized model and prompt registry
- **Reproducibility**: Automatically track all dependencies

#### Evaluation Framework
- **Built-in Evaluators**: Common LLM metrics (hallucination, toxicity, etc.)
- **Custom Scorers**: Easy to define domain-specific metrics
- **Batch Evaluation**: Efficient evaluation over datasets
- **Leaderboards**: Automatic ranking of model variants

#### Visualization
- **Interactive UI**: Explore traces, compare runs, debug failures
- **Rich Media**: Display images, audio, text with formatting
- **Collaborative**: Share experiments with team
- **Export**: Download data for further analysis

### 1.3 When to Use Weave

**Perfect For:**
- ML/AI researchers iterating on prompts and models
- Teams already using Weights & Biases for training
- Projects requiring rigorous experiment tracking
- Organizations needing reproducibility and governance
- Rapid prototyping with production-grade tracking
- Teams wanting best-in-class visualization

**Not Ideal For:**
- Simple scripts (overhead not justified)
- Production monitoring only (use Langfuse or Phoenix)
- Teams not invested in W&B ecosystem
- Minimal tracking requirements

### 1.4 Comparison Matrix

| Feature | Weave | Phoenix | Langfuse | LangSmith | MLflow |
|---------|-------|---------|----------|-----------|--------|
| **Experiment Focus** | ✅✅ Excellent | ⚠️ Limited | ⚠️ Limited | ✅ Good | ✅✅ Excellent |
| **Visualization** | ✅✅ Best-in-class | ✅ Good | ✅ Good | ✅ Good | ⚠️ Basic |
| **Versioning** | ✅✅ Automatic | ⚠️ Manual | ⚠️ Manual | ✅ Built-in | ✅ Built-in |
| **LLM-Specific** | ✅ Yes | ✅✅ Yes | ✅✅ Yes | ✅✅ Yes | ⚠️ Generic |
| **Setup Time** | 5 min | 5 min | 15 min | 5 min | 10 min |
| **Self-Hosting** | ❌ No | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| **Cost** | Free + W&B | Free | Free + Cloud | Subscription | Free |
| **ML Integration** | ✅✅ Native | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | ✅✅ Native |
| **Production Monitoring** | ⚠️ Limited | ✅✅ Excellent | ✅✅ Excellent | ✅ Good | ⚠️ Limited |

---

## 2. Complete Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Your LLM Application                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Python Functions with @weave.op() decorator          │ │
│  │  - prompt_fn()                                         │ │
│  │  - model.predict()                                     │ │
│  │  - evaluate()                                          │ │
│  └──────────────┬─────────────────────────────────────────┘ │
│                 │                                            │
│                 │ Automatic tracking                         │
│                 ▼                                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Weave Client (Local)                                  │ │
│  │  - Captures inputs/outputs                             │ │
│  │  - Computes versions                                   │ │
│  │  - Builds call graph                                   │ │
│  └──────────────┬─────────────────────────────────────────┘ │
└─────────────────┼──────────────────────────────────────────┘
                  │ HTTPS
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Weights & Biases Platform                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Storage     │  │  Versioning  │  │  Search      │      │
│  │  (Traces)    │  │  (Objects)   │  │  & Query     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                           │                                  │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │  Weave UI (Web)                                        │ │
│  │  - Trace visualization                                 │ │
│  │  - Run comparison                                      │ │
│  │  - Interactive debugging                               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Core Components

#### Weave Operations (@weave.op)
```python
# Core tracking primitive
@weave.op()
def my_function(input):
    # Automatically tracked:
    # - Input values
    # - Output values
    # - Execution time
    # - Nested calls
    # - Versions
    return output
```

#### Weave Objects
```python
# Versioned objects
class MyModel(weave.Model):
    prompt: str
    temperature: float

    @weave.op()
    def predict(self, input: str) -> str:
        # Prediction logic
        return result

# Automatic versioning on attribute changes
```

#### Call Graph
```
Root Call: chat_pipeline(user_input)
├── Call: retrieve_context(query)
│   ├── Call: embed_text(query) → [0.1, 0.2, ...]
│   └── Call: search_vectors(embedding) → [doc1, doc2]
├── Call: rerank(query, documents)
│   └── Call: score_relevance(query, doc) → 0.95
└── Call: generate_response(context, query)
    └── Call: openai.chat.completions.create() → "Answer..."
```

### 2.3 Type System

```python
# Weave's rich type system
weave.types.String
weave.types.Number
weave.types.Boolean
weave.types.List[T]
weave.types.Dict[K, V]
weave.types.Object  # Custom objects
weave.types.Image   # Images with previews
weave.types.Audio   # Audio playback
weave.types.Video   # Video playback
```

---

## 3. Installation & Setup

### 3.1 Installation

```bash
# Install Weave
pip install weave

# With all integrations
pip install weave[all]

# With specific integrations
pip install weave openai anthropic
pip install weave langchain
pip install weave llama-index

# Verify installation
python -c "import weave; print(weave.__version__)"
```

### 3.2 Quick Start

```python
import weave
import os

# Set W&B API key (get from https://wandb.ai/settings)
os.environ["WANDB_API_KEY"] = "your-key-here"

# Initialize Weave (creates a new project)
weave.init("my-llm-project")

# Start tracking
@weave.op()
def hello_weave(name: str) -> str:
    return f"Hello, {name}!"

# Call function (automatically tracked)
result = hello_weave("World")
print(result)

# View in UI
print("View traces at: https://wandb.ai/your-username/my-llm-project")
```

### 3.3 Configuration

```python
import weave

# Full configuration
weave.init(
    project="my-project",
    entity="my-team",  # W&B team name

    # Settings
    settings={
        "anonymous": False,
        "mode": "online",  # or "offline"
        "save_code": True,  # Save code version
        "quiet": False,     # Reduce logging
    }
)

# Environment variables
# WANDB_API_KEY=xxx
# WANDB_PROJECT=my-project
# WANDB_ENTITY=my-team
# WANDB_MODE=online
```

---

## 4. Core Concepts

### 4.1 Operations (@weave.op)

Operations are the fundamental tracking unit in Weave.

```python
import weave
from openai import OpenAI

weave.init("operations-demo")
client = OpenAI()

@weave.op()
def simple_completion(prompt: str) -> str:
    """Simple completion - automatically tracked"""
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Call it - creates a "call" in Weave
result = simple_completion("What is 2+2?")

# Nested operations
@weave.op()
def parent_operation(query: str) -> dict:
    """Nested calls create call graph"""

    # These are also tracked
    context = retrieve_context(query)
    answer = generate_answer(query, context)

    return {"query": query, "answer": answer}

@weave.op()
def retrieve_context(query: str) -> list:
    return ["context1", "context2"]

@weave.op()
def generate_answer(query: str, context: list) -> str:
    prompt = f"Context: {context}\nQuestion: {query}"
    return simple_completion(prompt)
```

### 4.2 Models (Versioned Objects)

Models are versioned, reusable components.

```python
import weave
from typing import List

class RAGPipeline(weave.Model):
    """Versioned RAG pipeline"""

    # Attributes are versioned
    system_prompt: str
    temperature: float
    top_k: int
    model_name: str = "gpt-4-turbo-preview"

    @weave.op()
    def predict(self, query: str) -> dict:
        """Main prediction method"""

        # Retrieve
        docs = self.retrieve(query)

        # Generate
        answer = self.generate(query, docs)

        return {
            "answer": answer,
            "sources": [d["id"] for d in docs]
        }

    @weave.op()
    def retrieve(self, query: str) -> List[dict]:
        """Retrieve relevant documents"""
        # Retrieval logic
        return [
            {"id": "doc1", "content": "Content 1"},
            {"id": "doc2", "content": "Content 2"}
        ][:self.top_k]

    @weave.op()
    def generate(self, query: str, docs: List[dict]) -> str:
        """Generate answer from documents"""
        context = "\n".join([d["content"] for d in docs])

        from openai import OpenAI
        client = OpenAI()

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
            ],
            temperature=self.temperature
        )

        return response.choices[0].message.content

# Create instance (automatically versioned)
pipeline_v1 = RAGPipeline(
    system_prompt="You are a helpful assistant",
    temperature=0.7,
    top_k=3
)

# Use it
result = pipeline_v1.predict("What is machine learning?")

# Modify attributes → new version automatically
pipeline_v2 = RAGPipeline(
    system_prompt="You are an expert ML researcher",  # Changed!
    temperature=0.7,
    top_k=3
)

# Both versions are tracked and comparable
```

### 4.3 Datasets

```python
import weave

weave.init("dataset-demo")

# Create dataset
dataset = weave.Dataset(
    name="qa-eval-set",
    rows=[
        {"question": "What is ML?", "expected": "Machine Learning is..."},
        {"question": "What is AI?", "expected": "Artificial Intelligence is..."},
        {"question": "What is NLP?", "expected": "Natural Language Processing is..."}
    ]
)

# Publish dataset (versioned)
weave.publish(dataset)

# Use dataset
for row in dataset.rows:
    print(f"Q: {row['question']}")
    print(f"A: {row['expected']}\n")

# Update dataset → new version
dataset_v2 = weave.Dataset(
    name="qa-eval-set",
    rows=dataset.rows + [
        {"question": "What is DL?", "expected": "Deep Learning is..."}
    ]
)
weave.publish(dataset_v2)
```

### 4.4 Evaluation

```python
import weave
from openai import OpenAI

weave.init("evaluation-demo")
client = OpenAI()

# Define model
class SimpleQA(weave.Model):
    model_name: str = "gpt-3.5-turbo"

    @weave.op()
    def predict(self, question: str) -> str:
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content

# Define scorer
@weave.op()
def exact_match(expected: str, model_output: str) -> dict:
    """Exact match scorer"""
    match = expected.strip().lower() == model_output.strip().lower()
    return {"match": match, "score": 1.0 if match else 0.0}

@weave.op()
def length_scorer(expected: str, model_output: str) -> dict:
    """Check if response is reasonable length"""
    return {
        "length": len(model_output),
        "score": 1.0 if len(model_output) > 10 else 0.0
    }

# Create evaluation dataset
dataset = weave.Dataset(
    name="qa-dataset",
    rows=[
        {"question": "What is 2+2?", "expected": "4"},
        {"question": "Capital of France?", "expected": "Paris"},
        {"question": "Largest planet?", "expected": "Jupiter"}
    ]
)
weave.publish(dataset)

# Run evaluation
model = SimpleQA(model_name="gpt-3.5-turbo")

evaluation = weave.Evaluation(
    dataset=dataset,
    scorers=[exact_match, length_scorer]
)

# Evaluate model
results = evaluation.evaluate(model)

print(f"Results: {results}")
# View detailed results in Weave UI
```

---

## 5. Complete Examples Section

### Example 1: Basic Function Tracking

**Use Case**: Track any Python function with minimal code changes

```python
import weave
import time
from typing import List

# Initialize
weave.init("basic-tracking")

@weave.op()
def process_text(text: str) -> dict:
    """Process text and extract features"""

    time.sleep(0.1)  # Simulate processing

    return {
        "length": len(text),
        "words": len(text.split()),
        "uppercase_ratio": sum(1 for c in text if c.isupper()) / len(text) if text else 0
    }

@weave.op()
def batch_process(texts: List[str]) -> List[dict]:
    """Process multiple texts"""

    results = []
    for text in texts:
        result = process_text(text)
        results.append(result)

    return results

# Usage
if __name__ == "__main__":
    # Single call
    result = process_text("Hello World! This is a TEST.")
    print(f"Single result: {result}")

    # Batch call
    texts = [
        "First text here",
        "Second TEXT with CAPS",
        "Third text is longer with more words"
    ]

    batch_results = batch_process(texts)
    print(f"\nBatch results: {batch_results}")

    print("\nView traces in Weave UI:")
    print("https://wandb.ai/<your-username>/basic-tracking")

# View in Weave UI:
# - Call graph showing batch_process → process_text (3x)
# - Execution times for each call
# - Input/output values
# - Automatic versioning
```

**Weave UI View:**
```
Call: batch_process(texts=[...])  [354ms]
├── Call: process_text("First text here")  [102ms]
│   Input: "First text here"
│   Output: {"length": 15, "words": 3, "uppercase_ratio": 0.07}
├── Call: process_text("Second TEXT with CAPS")  [101ms]
│   Input: "Second TEXT with CAPS"
│   Output: {"length": 22, "words": 4, "uppercase_ratio": 0.36}
└── Call: process_text("Third text...")  [103ms]
    Input: "Third text is longer with more words"
    Output: {"length": 38, "words": 7, "uppercase_ratio": 0.03}
```

### Example 2: Prompt Versioning and A/B Testing

**Use Case**: Compare different prompt versions systematically

```python
import weave
from openai import OpenAI
from typing import List

weave.init("prompt-versions")
client = OpenAI()

# Define prompt as a versioned model
class Summarizer(weave.Model):
    """Versioned summarization model"""

    system_prompt: str
    max_words: int
    temperature: float

    @weave.op()
    def predict(self, text: str) -> str:
        """Summarize text"""

        user_prompt = f"Summarize in max {self.max_words} words:\n\n{text}"

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature
        )

        return response.choices[0].message.content

# Create different versions
summarizer_v1 = Summarizer(
    system_prompt="You are a helpful assistant that summarizes text concisely.",
    max_words=50,
    temperature=0.3
)

summarizer_v2 = Summarizer(
    system_prompt="You are an expert editor. Create clear, informative summaries.",
    max_words=50,
    temperature=0.5  # More creative
)

summarizer_v3 = Summarizer(
    system_prompt="You are a technical writer. Summarize with key points.",
    max_words=75,  # Allow longer summaries
    temperature=0.3
)

# Test text
article = """
Artificial intelligence (AI) is transforming industries across the globe.
From healthcare to finance, AI systems are enabling unprecedented efficiency
and innovation. Machine learning algorithms can now diagnose diseases, predict
market trends, and even create art. However, concerns about bias, privacy,
and job displacement remain significant challenges that society must address.
"""

# Test all versions
@weave.op()
def compare_versions(text: str, models: List[Summarizer]) -> dict:
    """Compare multiple model versions"""

    results = {}
    for i, model in enumerate(models, 1):
        summary = model.predict(text)
        results[f"v{i}"] = {
            "summary": summary,
            "length": len(summary.split())
        }

    return results

if __name__ == "__main__":
    models = [summarizer_v1, summarizer_v2, summarizer_v3]

    comparison = compare_versions(article, models)

    for version, result in comparison.items():
        print(f"\n=== Version {version} ===")
        print(f"Summary: {result['summary']}")
        print(f"Word count: {result['length']}")

    print("\n✅ View comparison in Weave UI")
    print("Compare versions side-by-side with inputs/outputs")

# Weave UI Features:
# - Side-by-side comparison of all 3 versions
# - Automatic diff highlighting
# - Version history timeline
# - Performance metrics per version
```

**Weave UI Comparison:**
```
Summarizer Versions Comparison

Version 1 (temperature=0.3, max=50):
"AI transforms industries globally, improving efficiency in healthcare
and finance. ML diagnoses diseases and predicts trends, but concerns
about bias and jobs persist."
Words: 27 | Time: 1.2s | Cost: $0.003

Version 2 (temperature=0.5, max=50):  ← More creative
"AI revolutionizes multiple sectors worldwide. While enabling diagnostic
breakthroughs and market predictions, it raises important questions
about fairness, privacy, and employment."
Words: 24 | Time: 1.3s | Cost: $0.003

Version 3 (temperature=0.3, max=75):  ← Longer allowed
"AI is transforming global industries including healthcare and finance
through machine learning applications. Key benefits include disease
diagnosis and market prediction. Critical challenges: algorithmic bias,
data privacy, and workforce displacement require societal solutions."
Words: 38 | Time: 1.4s | Cost: $0.004

Winner: Version 3 (most comprehensive)
```

### Example 3: LLM Chain with Automatic Tracking

**Use Case**: Track complex multi-step LLM workflows

```python
import weave
from openai import OpenAI
from typing import List, Dict

weave.init("llm-chains")
client = OpenAI()

class ResearchAssistant(weave.Model):
    """Multi-step research assistant"""

    model_name: str = "gpt-4-turbo-preview"

    @weave.op()
    def research(self, topic: str) -> dict:
        """Complete research pipeline"""

        # Step 1: Generate research questions
        questions = self.generate_questions(topic)

        # Step 2: Answer each question
        answers = []
        for question in questions:
            answer = self.answer_question(question)
            answers.append({"question": question, "answer": answer})

        # Step 3: Synthesize findings
        synthesis = self.synthesize(topic, answers)

        return {
            "topic": topic,
            "questions": questions,
            "qa_pairs": answers,
            "synthesis": synthesis
        }

    @weave.op()
    def generate_questions(self, topic: str) -> List[str]:
        """Generate research questions"""

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{
                "role": "user",
                "content": f"Generate 3 important research questions about: {topic}"
            }],
            temperature=0.8
        )

        # Parse questions (simplified)
        text = response.choices[0].message.content
        questions = [q.strip() for q in text.split('\n') if q.strip() and ('?' in q)]

        return questions[:3]

    @weave.op()
    def answer_question(self, question: str) -> str:
        """Answer a research question"""

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{
                "role": "user",
                "content": f"Provide a detailed answer to: {question}"
            }],
            temperature=0.3
        )

        return response.choices[0].message.content

    @weave.op()
    def synthesize(self, topic: str, qa_pairs: List[dict]) -> str:
        """Synthesize all findings"""

        qa_text = "\n\n".join([
            f"Q: {pair['question']}\nA: {pair['answer']}"
            for pair in qa_pairs
        ])

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{
                "role": "user",
                "content": f"""Based on this research about "{topic}":

{qa_text}

Provide a comprehensive summary of the key findings."""
            }],
            temperature=0.5
        )

        return response.choices[0].message.content

if __name__ == "__main__":
    assistant = ResearchAssistant(model_name="gpt-4-turbo-preview")

    print("Starting research...")
    result = assistant.research("quantum computing")

    print(f"\n=== Research on: {result['topic']} ===\n")

    print("Questions:")
    for i, q in enumerate(result['questions'], 1):
        print(f"{i}. {q}")

    print(f"\n{len(result['qa_pairs'])} questions answered")

    print(f"\nSynthesis:\n{result['synthesis'][:200]}...")

    print("\n✅ View complete call graph in Weave UI")

# Weave UI Shows:
# research()  [12.5s]
# ├── generate_questions()  [2.1s]
# │   └── openai.chat.completions.create()  [1.9s]
# ├── answer_question() × 3  [8.2s total]
# │   ├── openai.chat.completions.create()  [2.7s]
# │   ├── openai.chat.completions.create()  [2.8s]
# │   └── openai.chat.completions.create()  [2.7s]
# └── synthesize()  [2.2s]
#     └── openai.chat.completions.create()  [2.0s]
```

### Example 4: Dataset Evaluation with Multiple Scorers

**Use Case**: Evaluate model on dataset with multiple metrics

```python
import weave
from openai import OpenAI
from typing import Dict

weave.init("model-evaluation")
client = OpenAI()

# Define model to evaluate
class QAModel(weave.Model):
    """Question answering model"""

    system_prompt: str
    model_name: str = "gpt-3.5-turbo"

    @weave.op()
    def predict(self, question: str) -> str:
        """Answer a question"""

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": question}
            ]
        )

        return response.choices[0].message.content

# Define scorers
@weave.op()
def exact_match_scorer(expected: str, model_output: str) -> Dict:
    """Check exact match"""
    match = expected.strip().lower() == model_output.strip().lower()
    return {"exact_match": 1.0 if match else 0.0}

@weave.op()
def contains_scorer(expected: str, model_output: str) -> Dict:
    """Check if expected answer is contained in output"""
    contained = expected.lower() in model_output.lower()
    return {"contains": 1.0 if contained else 0.0}

@weave.op()
def length_scorer(expected: str, model_output: str) -> Dict:
    """Score based on length similarity"""
    expected_len = len(expected.split())
    output_len = len(model_output.split())

    ratio = min(expected_len, output_len) / max(expected_len, output_len)

    return {
        "length_similarity": ratio,
        "output_words": output_len,
        "expected_words": expected_len
    }

@weave.op()
def llm_judge_scorer(expected: str, model_output: str) -> Dict:
    """Use LLM to judge quality"""

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{
            "role": "user",
            "content": f"""Score this answer on a scale of 0-1:

Expected: {expected}
Actual: {model_output}

Return only a number between 0 and 1."""
        }],
        temperature=0.0
    )

    try:
        score = float(response.choices[0].message.content.strip())
        score = max(0.0, min(1.0, score))  # Clamp to [0, 1]
    except:
        score = 0.5  # Default if parsing fails

    return {"llm_judge_score": score}

# Create evaluation dataset
dataset = weave.Dataset(
    name="qa-benchmark",
    rows=[
        {
            "question": "What is the capital of France?",
            "expected": "Paris"
        },
        {
            "question": "What is 2 + 2?",
            "expected": "4"
        },
        {
            "question": "Who wrote Romeo and Juliet?",
            "expected": "William Shakespeare"
        },
        {
            "question": "What is the largest planet in our solar system?",
            "expected": "Jupiter"
        },
        {
            "question": "What year did World War II end?",
            "expected": "1945"
        }
    ]
)
weave.publish(dataset)

if __name__ == "__main__":
    # Create model variants
    model_concise = QAModel(
        system_prompt="Answer in one word or phrase.",
        model_name="gpt-3.5-turbo"
    )

    model_detailed = QAModel(
        system_prompt="Provide a detailed answer.",
        model_name="gpt-3.5-turbo"
    )

    model_gpt4 = QAModel(
        system_prompt="Answer accurately and concisely.",
        model_name="gpt-4-turbo-preview"
    )

    # Create evaluation
    evaluation = weave.Evaluation(
        dataset=dataset,
        scorers=[
            exact_match_scorer,
            contains_scorer,
            length_scorer,
            llm_judge_scorer
        ]
    )

    # Evaluate all models
    print("Evaluating model_concise...")
    results_concise = evaluation.evaluate(model_concise)

    print("Evaluating model_detailed...")
    results_detailed = evaluation.evaluate(model_detailed)

    print("Evaluating model_gpt4...")
    results_gpt4 = evaluation.evaluate(model_gpt4)

    print("\n✅ Evaluation complete!")
    print("View detailed results and leaderboard in Weave UI")

# Weave UI Leaderboard:
# Model              | Exact Match | Contains | Length Sim | LLM Judge | Avg
# -------------------|-------------|----------|------------|-----------|-----
# model_gpt4         | 0.80        | 0.95     | 0.88       | 0.92      | 0.89
# model_concise      | 0.60        | 0.85     | 0.65       | 0.75      | 0.71
# model_detailed     | 0.40        | 0.90     | 0.45       | 0.82      | 0.64
```

**Weave UI Evaluation View:**
```
Evaluation: qa-benchmark
Models: 3 | Dataset: 5 examples | Scorers: 4

Leaderboard:
┌─────────────────┬──────────────┬──────────┬────────────┬───────────┐
│ Model           │ Exact Match  │ Contains │ Length Sim │ LLM Judge │
├─────────────────┼──────────────┼──────────┼────────────┼───────────┤
│ model_gpt4      │ 0.80 ✅      │ 0.95 ✅  │ 0.88 ✅    │ 0.92 ✅   │
│ model_concise   │ 0.60         │ 0.85     │ 0.65       │ 0.75      │
│ model_detailed  │ 0.40         │ 0.90     │ 0.45       │ 0.82      │
└─────────────────┴──────────────┴──────────┴────────────┴───────────┘

Click any cell to see example predictions
```

### Example 5: RAG System with Tracing

**Use Case**: Debug and optimize RAG pipeline with full visibility

```python
import weave
from openai import OpenAI
from typing import List, Dict
import numpy as np

weave.init("rag-system")
client = OpenAI()

class Document(weave.Object):
    """Document object with metadata"""
    id: str
    content: str
    metadata: Dict

class RAGSystem(weave.Model):
    """Complete RAG system with tracking"""

    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4-turbo-preview"
    top_k: int = 3
    rerank: bool = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Simulated document store
        self.documents = [
            Document(
                id=f"doc-{i}",
                content=f"Document {i} with relevant content about topic {i % 3}",
                metadata={"topic": i % 3, "length": 100 + i * 10}
            )
            for i in range(10)
        ]

    @weave.op()
    def query(self, question: str) -> Dict:
        """Main query endpoint"""

        # Step 1: Embed query
        query_embedding = self.embed_text(question)

        # Step 2: Retrieve candidates
        candidates = self.retrieve(query_embedding, k=self.top_k * 2)

        # Step 3: Rerank (optional)
        if self.rerank:
            final_docs = self.rerank_documents(question, candidates)
        else:
            final_docs = candidates[:self.top_k]

        # Step 4: Generate answer
        answer = self.generate_answer(question, final_docs)

        return {
            "question": question,
            "answer": answer,
            "sources": [d.id for d in final_docs],
            "num_candidates": len(candidates)
        }

    @weave.op()
    def embed_text(self, text: str) -> List[float]:
        """Embed text using OpenAI"""

        response = client.embeddings.create(
            model=self.embedding_model,
            input=text
        )

        embedding = response.data[0].embedding

        # Log embedding stats
        weave.log({
            "embedding_dim": len(embedding),
            "embedding_norm": float(np.linalg.norm(embedding))
        })

        return embedding

    @weave.op()
    def retrieve(self, query_embedding: List[float], k: int) -> List[Document]:
        """Retrieve top-k documents"""

        # Simulate vector search
        # In production: query Pinecone, Weaviate, etc.

        scores = []
        for doc in self.documents:
            # Mock similarity score
            score = np.random.random()
            scores.append((doc, score))

        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)

        retrieved = [doc for doc, score in scores[:k]]

        # Log retrieval metrics
        weave.log({
            "retrieved_count": len(retrieved),
            "top_score": scores[0][1] if scores else 0,
            "score_distribution": [s for _, s in scores[:k]]
        })

        return retrieved

    @weave.op()
    def rerank_documents(self, query: str, documents: List[Document]) -> List[Document]:
        """Rerank documents for relevance"""

        # Simulate reranking with LLM
        # In production: use Cohere rerank, cross-encoder, etc.

        scored = []
        for doc in documents:
            score = self.relevance_score(query, doc)
            scored.append((doc, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        reranked = [doc for doc, score in scored[:self.top_k]]

        # Log reranking impact
        weave.log({
            "reranked_count": len(reranked),
            "score_improvement": 0.15  # Mock
        })

        return reranked

    @weave.op()
    def relevance_score(self, query: str, document: Document) -> float:
        """Score document relevance"""

        # Simplified scoring
        # In production: use actual reranking model

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"""Score relevance (0-1):
Query: {query}
Document: {document.content}
Return only a number."""
            }],
            temperature=0.0
        )

        try:
            score = float(response.choices[0].message.content.strip())
        except:
            score = 0.5

        return max(0.0, min(1.0, score))

    @weave.op()
    def generate_answer(self, question: str, documents: List[Document]) -> str:
        """Generate answer from documents"""

        # Build context
        context = "\n\n".join([
            f"[{doc.id}] {doc.content}"
            for doc in documents
        ])

        response = client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": "Answer based on provided documents. Cite sources using [doc-id]."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}"
                }
            ],
            temperature=0.3
        )

        answer = response.choices[0].message.content

        # Log generation metrics
        weave.log({
            "answer_length": len(answer),
            "tokens_used": response.usage.total_tokens,
            "context_docs": len(documents)
        })

        return answer

if __name__ == "__main__":
    # Test different configurations

    # Config 1: With reranking
    rag_with_rerank = RAGSystem(
        top_k=3,
        rerank=True,
        llm_model="gpt-4-turbo-preview"
    )

    # Config 2: Without reranking
    rag_no_rerank = RAGSystem(
        top_k=3,
        rerank=False,
        llm_model="gpt-4-turbo-preview"
    )

    # Config 3: Cheaper model
    rag_cheap = RAGSystem(
        top_k=2,
        rerank=False,
        llm_model="gpt-3.5-turbo"
    )

    question = "What are the key topics covered in the documents?"

    print("Testing RAG configurations...\n")

    print("=== With Reranking ===")
    result1 = rag_with_rerank.query(question)
    print(f"Answer: {result1['answer'][:100]}...")
    print(f"Sources: {result1['sources']}\n")

    print("=== Without Reranking ===")
    result2 = rag_no_rerank.query(question)
    print(f"Answer: {result2['answer'][:100]}...")
    print(f"Sources: {result2['sources']}\n")

    print("=== Cheaper Model ===")
    result3 = rag_cheap.query(question)
    print(f"Answer: {result3['answer'][:100]}...")
    print(f"Sources: {result3['sources']}\n")

    print("✅ View detailed traces in Weave UI")
    print("Compare: latency, costs, source quality")

# Weave UI RAG Trace:
# query()  [4.5s]
# ├── embed_text()  [0.3s]
# │   Embedding dim: 1536
# ├── retrieve()  [0.1s]
# │   Retrieved: 6 docs
# │   Top score: 0.95
# ├── rerank_documents()  [2.1s]
# │   ├── relevance_score(doc-1)  [0.7s]
# │   ├── relevance_score(doc-2)  [0.7s]
# │   └── relevance_score(doc-3)  [0.7s]
# │   Final: 3 docs
# └── generate_answer()  [2.0s]
#     Context: 3 docs
#     Tokens: 450
#     Answer length: 120
```

### Example 6: Custom Metrics and Logging

**Use Case**: Track domain-specific metrics

```python
import weave
from openai import OpenAI
from typing import Dict, List
import json

weave.init("custom-metrics")
client = OpenAI()

class MetricsTracker:
    """Track custom business metrics"""

    @weave.op()
    def track_conversation(self, messages: List[Dict], user_id: str) -> Dict:
        """Track conversation with custom metrics"""

        # Generate response
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages
        )

        assistant_message = response.choices[0].message.content

        # Calculate custom metrics
        metrics = self.calculate_metrics(messages, assistant_message)

        # Log metrics to Weave
        weave.log({
            "user_id": user_id,
            **metrics,
            "model": "gpt-4-turbo-preview",
            "tokens": response.usage.total_tokens
        })

        return {
            "response": assistant_message,
            "metrics": metrics
        }

    @weave.op()
    def calculate_metrics(self, messages: List[Dict], response: str) -> Dict:
        """Calculate custom metrics"""

        # Conversation depth
        turn_count = len([m for m in messages if m["role"] == "user"])

        # Response characteristics
        response_words = len(response.split())
        response_sentences = response.count('.') + response.count('!') + response.count('?')

        # Sentiment (mock - use actual sentiment analyzer)
        sentiment = self.analyze_sentiment(response)

        # Topic detection (mock - use actual topic model)
        topics = self.detect_topics(response)

        # Engagement score (custom business logic)
        engagement = self.calculate_engagement(response_words, response_sentences, sentiment)

        return {
            "turn_count": turn_count,
            "response_words": response_words,
            "response_sentences": response_sentences,
            "avg_words_per_sentence": response_words / max(response_sentences, 1),
            "sentiment": sentiment,
            "topics": topics,
            "engagement_score": engagement
        }

    @weave.op()
    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Classify sentiment as positive, neutral, or negative:\n{text}"
            }]
        )

        sentiment = response.choices[0].message.content.strip().lower()

        if "positive" in sentiment:
            return "positive"
        elif "negative" in sentiment:
            return "negative"
        else:
            return "neutral"

    @weave.op()
    def detect_topics(self, text: str) -> List[str]:
        """Detect topics"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"List 2-3 main topics (comma-separated):\n{text}"
            }]
        )

        topics_str = response.choices[0].message.content.strip()
        topics = [t.strip() for t in topics_str.split(',')]

        return topics[:3]

    @weave.op()
    def calculate_engagement(self, words: int, sentences: int, sentiment: str) -> float:
        """Calculate engagement score (0-1)"""

        # Custom business logic
        base_score = min(words / 100, 1.0) * 0.5  # Length contribution

        sentence_score = min(sentences / 10, 1.0) * 0.3  # Completeness

        sentiment_score = {
            "positive": 0.2,
            "neutral": 0.1,
            "negative": 0.0
        }.get(sentiment, 0.1)

        return base_score + sentence_score + sentiment_score

if __name__ == "__main__":
    tracker = MetricsTracker()

    # Test conversations
    conversations = [
        {
            "user_id": "user-1",
            "messages": [
                {"role": "user", "content": "Tell me about machine learning"}
            ]
        },
        {
            "user_id": "user-2",
            "messages": [
                {"role": "user", "content": "What is AI?"},
                {"role": "assistant", "content": "AI is artificial intelligence..."},
                {"role": "user", "content": "Can you explain neural networks?"}
            ]
        }
    ]

    for conv in conversations:
        print(f"\n=== Conversation: {conv['user_id']} ===")

        result = tracker.track_conversation(
            messages=conv["messages"],
            user_id=conv["user_id"]
        )

        print(f"Response: {result['response'][:100]}...")
        print(f"\nMetrics:")
        print(json.dumps(result["metrics"], indent=2))

    print("\n✅ View custom metrics in Weave UI")

# Weave UI Custom Metrics Dashboard:
# - Engagement score distribution
# - Sentiment breakdown
# - Topic clusters
# - User segmentation by metrics
# - Time series of custom metrics
```

### Example 7: Integration with LangChain

**Use Case**: Track LangChain chains with Weave

```python
import weave
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

weave.init("langchain-integration")

# Weave automatically tracks LangChain operations
# when you wrap them with @weave.op() or use weave.op()

class LangChainPipeline(weave.Model):
    """LangChain pipeline with Weave tracking"""

    model_name: str = "gpt-4-turbo-preview"
    temperature: float = 0.7

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize LangChain components
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("user", "{question}")
        ])

        self.chain = (
            {"question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    @weave.op()
    def predict(self, question: str) -> str:
        """Run LangChain chain"""

        # LangChain operations are automatically tracked
        result = self.chain.invoke(question)

        return result

    @weave.op()
    def batch_predict(self, questions: List[str]) -> List[str]:
        """Batch predictions"""

        results = self.chain.batch(questions)

        return results

if __name__ == "__main__":
    pipeline = LangChainPipeline()

    # Single prediction
    answer = pipeline.predict("What is the meaning of life?")
    print(f"Answer: {answer}\n")

    # Batch predictions
    questions = [
        "What is 2+2?",
        "Capital of France?",
        "Largest ocean?"
    ]

    answers = pipeline.batch_predict(questions)

    for q, a in zip(questions, answers):
        print(f"Q: {q}")
        print(f"A: {a}\n")

    print("✅ View LangChain traces in Weave UI")

# Weave tracks:
# - Chain structure
# - Prompt templates
# - LLM calls
# - Output parsing
# - All automatically!
```

### Example 8: Streaming Responses

**Use Case**: Track streaming LLM responses

```python
import weave
from openai import OpenAI
from typing import Iterator

weave.init("streaming-demo")
client = OpenAI()

class StreamingAssistant(weave.Model):
    """Assistant with streaming support"""

    model_name: str = "gpt-4-turbo-preview"

    @weave.op()
    def stream_response(self, prompt: str) -> str:
        """Stream response and track final output"""

        stream = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        full_response = ""

        print("Streaming response: ", end="", flush=True)

        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                print(content, end="", flush=True)

        print("\n")

        # Weave tracks the final complete output
        return full_response

if __name__ == "__main__":
    assistant = StreamingAssistant()

    response = assistant.stream_response(
        "Write a haiku about programming"
    )

    print(f"\nFinal response tracked: {len(response)} chars")
    print("✅ View in Weave UI")

# Weave tracks the complete response
# even though it was streamed to user
```

### Example 9: Error Tracking and Debugging

**Use Case**: Track errors and debug failures

```python
import weave
from openai import OpenAI
from typing import Optional

weave.init("error-tracking")
client = OpenAI()

class RobustPipeline(weave.Model):
    """Pipeline with error handling"""

    max_retries: int = 3

    @weave.op()
    def process(self, text: str) -> dict:
        """Process with error handling"""

        try:
            result = self.risky_operation(text)
            return {"success": True, "result": result}

        except Exception as e:
            # Weave automatically tracks exceptions
            error_info = {
                "success": False,
                "error_type": type(e).__name__,
                "error_message": str(e)
            }

            # Log additional context
            weave.log({
                "input_length": len(text),
                "retry_count": self.max_retries
            })

            return error_info

    @weave.op()
    def risky_operation(self, text: str) -> str:
        """Operation that might fail"""

        if len(text) < 5:
            raise ValueError("Text too short")

        if "error" in text.lower():
            raise RuntimeError("Triggered error keyword")

        # Normal processing
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": text}]
        )

        return response.choices[0].message.content

if __name__ == "__main__":
    pipeline = RobustPipeline()

    test_cases = [
        "Hi",  # Too short - will error
        "This is a test error",  # Contains "error" - will error
        "What is machine learning?"  # Valid
    ]

    for text in test_cases:
        print(f"\nProcessing: {text}")
        result = pipeline.process(text)

        if result["success"]:
            print(f"✅ Success: {result['result'][:50]}...")
        else:
            print(f"❌ Error: {result['error_type']}")
            print(f"   Message: {result['error_message']}")

    print("\n✅ View error traces in Weave UI")
    print("Filter by status:error to see all failures")

# Weave UI shows:
# - Error traces highlighted in red
# - Stack traces captured
# - Input that caused error
# - Error rate metrics
# - Time to error
```

### Example 10: Production Monitoring

**Use Case**: Monitor production deployment

```python
import weave
from openai import OpenAI
from typing import Dict
from datetime import datetime
import time

weave.init("production-monitoring")
client = OpenAI()

class ProductionService(weave.Model):
    """Production service with monitoring"""

    model_name: str = "gpt-4-turbo-preview"

    @weave.op()
    def handle_request(
        self,
        user_id: str,
        request_data: Dict
    ) -> Dict:
        """Handle production request"""

        start_time = time.time()

        # Log request metadata
        weave.log({
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "request_type": request_data.get("type"),
            "environment": "production"
        })

        try:
            # Process request
            response = self.process(request_data)

            # Calculate latency
            latency = time.time() - start_time

            # Log success metrics
            weave.log({
                "status": "success",
                "latency_seconds": latency,
                "response_length": len(response.get("text", ""))
            })

            return {
                "success": True,
                "response": response,
                "latency": latency
            }

        except Exception as e:
            latency = time.time() - start_time

            # Log error metrics
            weave.log({
                "status": "error",
                "error_type": type(e).__name__,
                "latency_seconds": latency
            })

            return {
                "success": False,
                "error": str(e),
                "latency": latency
            }

    @weave.op()
    def process(self, data: Dict) -> Dict:
        """Process request"""

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{
                "role": "user",
                "content": data.get("query", "")
            }]
        )

        return {
            "text": response.choices[0].message.content,
            "tokens": response.usage.total_tokens
        }

if __name__ == "__main__":
    service = ProductionService()

    # Simulate production traffic
    requests = [
        {"user_id": f"user-{i}", "request_data": {"type": "query", "query": f"Question {i}"}}
        for i in range(10)
    ]

    print("Simulating production traffic...\n")

    for req in requests:
        result = service.handle_request(**req)

        status = "✅" if result["success"] else "❌"
        print(f"{status} {req['user_id']}: {result['latency']:.2f}s")

        time.sleep(0.1)  # Rate limiting

    print("\n✅ View production metrics in Weave UI:")
    print("- Request volume")
    print("- Latency distribution (p50, p95, p99)")
    print("- Error rate")
    print("- Per-user analytics")
```

---

## 6. Advanced Usage

### 6.1 Custom Types

```python
import weave
from dataclasses import dataclass
from typing import List

@dataclass
class CustomResult(weave.Object):
    """Custom result type"""
    score: float
    items: List[str]
    metadata: dict

@weave.op()
def produce_custom_result() -> CustomResult:
    """Return custom type"""
    return CustomResult(
        score=0.95,
        items=["a", "b", "c"],
        metadata={"version": "1.0"}
    )

# Weave automatically serializes and displays custom types
```

### 6.2 Filtering and Querying

```python
# Query traces in UI:
# - Filter by status: status:error
# - Filter by duration: duration:>5s
# - Filter by user: user_id:user-123
# - Filter by date: created:>2024-01-01

# Programmatic querying (coming soon)
# traces = weave.get_traces(
#     filter={"status": "error"},
#     limit=100
# )
```

### 6.3 Export and Analysis

```python
# Export data from UI:
# - JSON export for all traces
# - CSV export for tabular data
# - Python API (planned)

# Analyze in notebooks:
# import weave
# client = weave.init("my-project")
# traces = client.get_traces()
# df = traces.to_pandas()
# df.plot(x="timestamp", y="latency")
```

---

## 7. Best Practices

### 7.1 Operation Granularity

```python
# DO: Track meaningful operations
@weave.op()
def rag_pipeline(query):  # ✅
    docs = retrieve(query)  # ✅ Tracked
    answer = generate(docs)  # ✅ Tracked
    return answer

# DON'T: Track every tiny function
@weave.op()
def add(a, b):  # ❌ Too granular
    return a + b
```

### 7.2 Model Versioning

```python
# DO: Use Model class for reusable components
class MyPipeline(weave.Model):  # ✅
    prompt: str
    temperature: float

    @weave.op()
    def predict(self, input):
        ...

# DON'T: Use plain functions for models
@weave.op()  # ❌ Not versioned
def my_pipeline(input, prompt, temperature):
    ...
```

### 7.3 Dataset Management

```python
# DO: Version datasets
dataset_v1 = weave.Dataset(name="eval-set", rows=[...])
weave.publish(dataset_v1)

# Later: Update and publish new version
dataset_v2 = weave.Dataset(name="eval-set", rows=[...])
weave.publish(dataset_v2)

# Both versions are preserved and comparable
```

---

## 8. Integration Guide

### 8.1 Framework Integrations

**OpenAI:**
```python
import weave
from openai import OpenAI

weave.init("openai-project")

# OpenAI calls are automatically tracked when inside @weave.op()
@weave.op()
def call_openai():
    client = OpenAI()
    response = client.chat.completions.create(...)
    return response
```

**Anthropic:**
```python
import weave
from anthropic import Anthropic

weave.init("anthropic-project")

@weave.op()
def call_anthropic():
    client = Anthropic()
    message = client.messages.create(...)
    return message
```

### 8.2 CI/CD Integration

```yaml
# .github/workflows/eval.yml
name: Evaluate Model
on: [push]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install weave
      - run: python run_evaluation.py
        env:
          WANDB_API_KEY: ${{ secrets.WANDB_API_KEY }}
```

---

## 9. Troubleshooting

### 9.1 Common Issues

**Traces not appearing:**
```python
# Ensure you called weave.init()
weave.init("my-project")

# Check you're using @weave.op()
@weave.op()  # Don't forget this!
def my_function():
    ...
```

**Slow performance:**
```python
# Reduce tracking granularity
# Don't track utility functions
# Track high-level operations only
```

---

## 10. API Reference

### 10.1 Core Functions

```python
# Initialize
weave.init(project: str, entity: str = None, settings: dict = None)

# Decorators
@weave.op(name: str = None)

# Types
weave.Model  # Base class for versioned models
weave.Object  # Base class for tracked objects
weave.Dataset  # Dataset container

# Publishing
weave.publish(obj)  # Publish versioned object

# Logging
weave.log(dict)  # Log custom metrics
```

---

## 11. Performance & Optimization

### 11.1 Performance Impact

- Minimal overhead: <5ms per operation
- Async upload: Non-blocking
- Batched: Multiple calls bundled

### 11.2 Scale

- Millions of calls tracked
- Gigabytes of data supported
- Fast UI even with large datasets

---

## 12. Security Considerations

### 12.1 Data Privacy

```python
# Sanitize sensitive data
@weave.op()
def process_user_data(user_data):
    # Redact PII before processing
    sanitized = redact_pii(user_data)
    return process(sanitized)
```

### 12.2 Access Control

- W&B team access controls
- Private projects
- SSO for enterprise

---

## 13. References & Resources

### 13.1 Official Links

- Website: https://wandb.ai/site/weave
- Documentation: https://weave-docs.wandb.ai
- GitHub: https://github.com/wandb/weave
- Community: https://wandb.me/slack

### 13.2 Pricing

- Free tier: Unlimited projects
- Team tier: Starting at $50/user/month
- Enterprise: Custom pricing

### 13.3 Comparison

**vs MLflow:**
- Weave: Modern, LLM-focused
- MLflow: Traditional ML focus

**vs LangSmith:**
- Weave: Open experimentation
- LangSmith: Production monitoring

---

## Conclusion

Weave brings Weights & Biases' industry-leading experiment tracking to LLM applications. Its automatic tracking, powerful versioning, and beautiful visualization make it ideal for teams iterating on prompts and models. The seamless W&B integration means your LLM work lives alongside your traditional ML experiments.

**Key Strengths:**
- Best-in-class visualization
- Automatic versioning
- Simple decorator API
- W&B ecosystem integration
- Experiment comparison

**Best For:**
- ML/AI researchers
- Teams using W&B
- Prompt engineering
- Model comparison
- Reproducible experiments

Start experimenting today with `pip install weave`!
