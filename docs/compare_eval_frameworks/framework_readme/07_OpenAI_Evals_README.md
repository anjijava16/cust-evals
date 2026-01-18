# OpenAI Evals: Deep Dive Guide

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

### What is OpenAI Evals?

OpenAI Evals is an open-source framework for evaluating Large Language Models (LLMs) and systems built with them. Developed and maintained by OpenAI, it provides a standardized, reproducible way to measure model performance across a wide variety of tasks.

**Key Characteristics:**

- **CLI-First Design**: Primary interface is command-line, making it ideal for automation and CI/CD
- **Standardized Format**: YAML-based evaluation definitions ensure consistency
- **Community-Driven**: Large collection of community-contributed evaluations
- **Extensible Architecture**: Easy to create custom evaluation types
- **Reproducible**: Deterministic evaluation runs for reliable comparisons
- **Multi-Model Support**: Evaluate any OpenAI model or compatible API

### Why Use OpenAI Evals?

**Strengths:**

1. **Reproducibility**: Standardized format ensures evaluations can be replicated
2. **Community Evals**: Access to hundreds of pre-built evaluations
3. **CLI Automation**: Easy integration into automated workflows
4. **Extensibility**: Create custom evaluation logic while maintaining standardization
5. **Model Comparison**: Built-in support for comparing different models
6. **Open Source**: Full transparency and community contributions

**Ideal Use Cases:**

- Regression testing during model development
- Comparing different models or model versions
- Benchmarking on standard tasks
- Creating reproducible evaluation datasets
- CI/CD integration for LLM applications
- Research and academic studies requiring reproducibility

### Framework Philosophy

OpenAI Evals embodies several key principles:

1. **Standardization Over Flexibility**: Trade some flexibility for reproducibility
2. **Declarative Configuration**: Define what to evaluate, not how
3. **Separation of Concerns**: Evaluation logic separate from test data
4. **Community Collaboration**: Share and reuse evaluations
5. **Scientific Rigor**: Emphasis on reproducible results

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenAI Evals Framework                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────┐      ┌──────────────┐      ┌────────────┐ │
│  │    CLI     │─────→│ Eval Registry│─────→│  Samplers  │ │
│  │  Interface │      │   & Config   │      │   (Data)   │ │
│  └────────────┘      └──────────────┘      └────────────┘ │
│         │                    │                     │        │
│         ↓                    ↓                     ↓        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Evaluation Runner                         │ │
│  │  - Orchestrates eval execution                         │ │
│  │  - Manages model interactions                          │ │
│  │  │  - Handles retries and rate limiting                │ │
│  └────────────────────────────────────────────────────────┘ │
│         │                                                   │
│         ↓                                                   │
│  ┌─────────────────────┬──────────────────────────────────┐ │
│  │  Evaluation Types   │   Completion Functions           │ │
│  │  ─────────────────  │   ───────────────────────────    │ │
│  │  • Match           │   • Direct Model Calls            │ │
│  │  • Includes        │   • Chain-of-Thought             │ │
│  │  • FuzzyMatch      │   • Function Calling             │ │
│  │  • ModelGraded     │   • Custom Completion Fns        │ │
│  │  • Custom          │                                   │ │
│  └─────────────────────┴──────────────────────────────────┘ │
│         │                                                   │
│         ↓                                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Results & Reporting                       │ │
│  │  - Metrics aggregation                                 │ │
│  │  - Log file generation                                 │ │
│  │  - Summary statistics                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Evaluation Registry

Central registry that stores:
- Evaluation definitions (YAML files)
- Sampler configurations
- Model specifications
- Custom completion functions

#### 2. Samplers

Data sources for evaluations:
- **JSONL Samplers**: Load test cases from JSONL files
- **CSV Samplers**: Load from CSV files
- **Custom Samplers**: Programmatic data generation

#### 3. Evaluation Types

Different evaluation methodologies:
- **Match**: Exact string matching
- **Includes**: Check if output contains specific text
- **FuzzyMatch**: Approximate string matching
- **ModelGraded**: Use another model to grade outputs
- **Custom**: User-defined evaluation logic

#### 4. Completion Functions

How to generate responses:
- **Direct Generation**: Standard model completion
- **Chain-of-Thought**: Multi-step reasoning
- **Function Calling**: Use function/tool calling APIs
- **Custom Logic**: Any Python function

#### 5. CLI Interface

Primary way to interact:
```bash
oaieval <model> <eval_name> [options]
```

### Data Flow

```
Test Data (JSONL/CSV)
        ↓
    Sampler
        ↓
Evaluation Runner
        ↓
Completion Function → Model API
        ↓
    Response
        ↓
Evaluation Type → Scoring Logic
        ↓
    Results → Log Files & Reports
```

---

## Installation and Setup

### Prerequisites

**System Requirements:**
- Python 3.8 or higher
- pip or conda package manager
- OpenAI API key (or compatible API)
- 2GB+ free disk space for logs

**Recommended Environment:**
- Unix-like system (Linux, macOS) for best CLI experience
- Virtual environment (venv, conda)
- Git for cloning the repository

### Installation Methods

#### Method 1: pip Install (Recommended for Users)

```bash
# Install from PyPI
pip install evals

# Verify installation
oaieval --help
```

#### Method 2: Install from Source (Recommended for Developers)

```bash
# Clone the repository
git clone https://github.com/openai/evals.git
cd evals

# Install in editable mode
pip install -e .

# Verify installation
oaieval --help
```

#### Method 3: Docker Installation

```bash
# Build Docker image
docker build -t openai-evals .

# Run evaluation
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY openai-evals \
  oaieval gpt-3.5-turbo my_eval
```

### Environment Configuration

#### 1. Set API Keys

```bash
# OpenAI API Key (required)
export OPENAI_API_KEY="sk-..."

# For Azure OpenAI
export AZURE_OPENAI_KEY="..."
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"

# For other compatible APIs
export OPENAI_API_BASE="https://api.alternative.com/v1"
```

#### 2. Configure Logging

```bash
# Set log directory (default: /tmp/evallogs)
export EVALS_LOG_DIR="$HOME/evals/logs"

# Set log level
export EVALS_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
```

#### 3. Create Configuration File

Create `~/.config/evals/config.yaml`:

```yaml
# Model defaults
default_model: gpt-3.5-turbo

# API configuration
api:
  timeout: 60
  max_retries: 3
  retry_delay: 1.0

# Logging
logging:
  level: INFO
  format: json

# Parallel execution
concurrency:
  max_workers: 10
  rate_limit: 50  # requests per minute
```

### Project Structure Setup

#### Create Standard Directory Layout

```bash
# Create project structure
mkdir -p my_evals/{evals,data,completion_fns,results}

# evals/: Evaluation definitions (YAML)
# data/: Test datasets (JSONL, CSV)
# completion_fns/: Custom completion functions
# results/: Evaluation results and logs
```

#### Example Project Structure

```
my_evals/
├── evals/
│   ├── registry.yaml          # Eval registry
│   ├── my_qa_eval.yaml        # Q&A evaluation
│   └── my_classify_eval.yaml  # Classification eval
├── data/
│   ├── qa_samples.jsonl       # Test data
│   └── classify_samples.jsonl
├── completion_fns/
│   ├── __init__.py
│   └── custom_cot.py          # Custom completion
├── results/
│   └── .gitkeep
└── requirements.txt
```

### Validation

#### Test Installation

```bash
# Run a simple test
echo '{"input": [{"role": "user", "content": "What is 2+2?"}], "ideal": "4"}' > test.jsonl

# Create minimal eval
cat > test_eval.yaml << EOF
test_eval:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: test.jsonl
EOF

# Run evaluation
oaieval gpt-3.5-turbo test_eval

# Check logs
ls -lh /tmp/evallogs/
```

### Common Installation Issues

#### Issue 1: Import Errors

```bash
# Problem: Cannot import evals
# Solution: Ensure proper installation
pip uninstall evals
pip install evals --no-cache-dir

# Or for development
pip install -e . --force-reinstall
```

#### Issue 2: API Key Not Found

```bash
# Problem: OpenAI API key not detected
# Solution: Set environment variable
export OPENAI_API_KEY="sk-..."

# Or use .env file
echo 'OPENAI_API_KEY=sk-...' > .env
source .env
```

#### Issue 3: Permission Errors

```bash
# Problem: Cannot write to /tmp/evallogs
# Solution: Set custom log directory
export EVALS_LOG_DIR="$HOME/evals/logs"
mkdir -p $EVALS_LOG_DIR
```

---

## Core Concepts

### 1. Evaluations

An **evaluation** is a complete test suite for a specific task.

**Anatomy of an Evaluation:**

```yaml
# evals/my_eval.yaml
my_eval:
  # Evaluation class to use
  class: evals.elsuite.basic.match:Match

  # Arguments for the evaluation
  args:
    # Data source
    samples_jsonl: my_data.jsonl

    # Number of samples to use
    num_few_shot: 0

    # Additional options
    max_tokens: 100
```

**Key Properties:**

- **ID**: Unique identifier (e.g., `my_eval`)
- **Class**: Python class implementing evaluation logic
- **Args**: Configuration for the evaluation
- **Metadata**: Description, tags, version info

### 2. Samplers

**Samplers** provide test data to evaluations.

#### JSONL Sampler

Most common format:

```jsonl
{"input": [{"role": "user", "content": "What is AI?"}], "ideal": "Artificial Intelligence"}
{"input": [{"role": "user", "content": "What is ML?"}], "ideal": "Machine Learning"}
```

**Field Descriptions:**
- `input`: The prompt (can be string or message list)
- `ideal`: Expected/correct answer(s)
- Additional fields can be used for metadata

#### CSV Sampler

Alternative format:

```csv
input,ideal
"What is AI?","Artificial Intelligence"
"What is ML?","Machine Learning"
```

#### Programmatic Sampler

```python
# custom_sampler.py
from evals.api import DummyCompletionFn
from evals.elsuite.basic.match import Match

class CustomSampler:
    def __init__(self):
        self.samples = [
            {"input": "Question 1", "ideal": "Answer 1"},
            {"input": "Question 2", "ideal": "Answer 2"},
        ]

    def __iter__(self):
        return iter(self.samples)
```

### 3. Evaluation Types

#### Match (Exact Match)

Tests for exact string equality:

```yaml
my_match_eval:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: data.jsonl
```

Example data:
```jsonl
{"input": "Capital of France?", "ideal": "Paris"}
```

#### Includes

Tests if output contains expected text:

```yaml
my_includes_eval:
  class: evals.elsuite.basic.includes:Includes
  args:
    samples_jsonl: data.jsonl
```

Example data:
```jsonl
{"input": "Name European capitals", "ideal": ["Paris", "London", "Berlin"]}
```

#### FuzzyMatch

Allows approximate matching:

```yaml
my_fuzzy_eval:
  class: evals.elsuite.basic.fuzzy_match:FuzzyMatch
  args:
    samples_jsonl: data.jsonl
    match_threshold: 0.8  # 80% similarity required
```

#### ModelGraded

Uses another model to grade outputs:

```yaml
my_graded_eval:
  class: evals.elsuite.modelgraded.classify:ModelGradedSpec
  args:
    samples_jsonl: data.jsonl
    eval_type: cot_classify  # Chain-of-thought classification
    prompt: |
      Evaluate if the answer is correct.
      Question: {input}
      Answer: {output}
      Correct Answer: {ideal}

      Is the answer correct? [Yes/No]
```

### 4. Completion Functions

**Completion functions** define how to generate model responses.

#### Default Completion

Standard API call:

```yaml
# Uses default completion function
# Just specifies model in CLI
```

```bash
oaieval gpt-3.5-turbo my_eval
```

#### Chain-of-Thought Completion

Multi-step reasoning:

```python
# completion_fns/cot.py
from evals.completion_fns import CompletionFnSpec

class ChainOfThoughtCompletionFn(CompletionFnSpec):
    def __call__(self, prompt, **kwargs):
        # Step 1: Reasoning
        reasoning_prompt = f"{prompt}\n\nLet's think step by step:"
        reasoning = self.completion_fn(reasoning_prompt)

        # Step 2: Final answer
        final_prompt = f"{reasoning}\n\nTherefore, the answer is:"
        answer = self.completion_fn(final_prompt)

        return answer
```

Register in YAML:

```yaml
my_cot_eval:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: data.jsonl
    completion_fn: completion_fns.cot:ChainOfThoughtCompletionFn
```

#### Function Calling Completion

```python
# completion_fns/function_calling.py
from evals.completion_fns import CompletionFnSpec

class FunctionCallingCompletionFn(CompletionFnSpec):
    def __init__(self, tools, **kwargs):
        super().__init__(**kwargs)
        self.tools = tools

    def __call__(self, prompt, **kwargs):
        # Call with function definitions
        response = self.completion_fn(
            prompt,
            tools=self.tools,
            tool_choice="auto"
        )

        # Execute function calls
        if response.tool_calls:
            results = self.execute_tools(response.tool_calls)
            # Second call with results
            final = self.completion_fn(
                prompt,
                messages=[...],  # Include function results
            )
            return final

        return response
```

### 5. Metrics and Scoring

#### Built-in Metrics

**Match Evaluation:**
- `accuracy`: Percentage of exact matches
- `boostrap_std`: Bootstrap standard deviation

**Includes Evaluation:**
- `f1_score`: F1 score for included terms
- `precision`: Precision of included terms
- `recall`: Recall of included terms

**ModelGraded Evaluation:**
- Custom metrics based on grading prompt
- `accuracy`: If grader returns binary yes/no
- `score`: If grader returns numerical score

#### Custom Metrics

```python
# custom_metrics.py
from evals.api import CompletionFn
from evals.eval import Eval
from evals.record import RecorderBase

class CustomMetricEval(Eval):
    def eval_sample(self, sample, rng):
        # Get model response
        response = self.completion_fn(
            prompt=sample["input"],
            temperature=0.0,
        )

        # Custom scoring logic
        output = response.get_completions()[0]
        ideal = sample["ideal"]

        # Calculate custom metric
        score = self.custom_score_function(output, ideal)

        # Record result
        self.record_match(
            correct=score > 0.7,
            expected=ideal,
            picked=output,
            score=score
        )

    def custom_score_function(self, output, ideal):
        # Implement custom scoring
        return 0.0  # Return score in [0, 1]
```

### 6. Registry System

The **registry** manages all evaluations, samplers, and completion functions.

#### Evaluation Registry

```yaml
# evals/registry.yaml

# Define evaluation
my_qa_eval:
  class: evals.elsuite.basic.match:Match
  description: "Question answering evaluation"
  tags: ["qa", "factual"]
  args:
    samples_jsonl: qa_data.jsonl

# Another evaluation
my_summarization_eval:
  class: evals.elsuite.modelgraded.fact:Fact
  description: "Summarization quality"
  tags: ["summarization"]
  args:
    samples_jsonl: summary_data.jsonl
```

#### Programmatic Registry

```python
from evals.registry import Registry

# Get global registry
registry = Registry()

# Get evaluation by ID
eval_spec = registry.get_eval("my_qa_eval")

# Get completion function
completion_fn = registry.make_completion_fn("gpt-3.5-turbo")

# List all evaluations
all_evals = registry.get_evals()
```

---

## Production-Ready Examples

### Example 1: Basic Q&A Evaluation

**Goal**: Evaluate model on factual question answering.

#### Step 1: Create Test Data

```jsonl
{"input": [{"role": "user", "content": "What is the capital of France?"}], "ideal": "Paris"}
{"input": [{"role": "user", "content": "What is 2 + 2?"}], "ideal": "4"}
{"input": [{"role": "user", "content": "Who wrote Romeo and Juliet?"}], "ideal": "William Shakespeare"}
{"input": [{"role": "user", "content": "What is the largest planet in our solar system?"}], "ideal": "Jupiter"}
{"input": [{"role": "user", "content": "What is the speed of light?"}], "ideal": "299,792,458 meters per second"}
```

Save as `data/qa_basic.jsonl`.

#### Step 2: Create Evaluation Definition

```yaml
# evals/qa_basic.yaml
qa_basic:
  class: evals.elsuite.basic.match:Match
  description: "Basic factual Q&A test"
  tags: ["qa", "factual", "basic"]
  args:
    samples_jsonl: data/qa_basic.jsonl
    num_few_shot: 0
    max_tokens: 50
```

#### Step 3: Run Evaluation

```bash
# Run with GPT-3.5
oaieval gpt-3.5-turbo qa_basic

# Run with GPT-4
oaieval gpt-4 qa_basic

# Run with custom settings
oaieval gpt-3.5-turbo qa_basic --max_samples 10 --record_path results/qa_basic_run1.jsonl
```

#### Step 4: Analyze Results

```python
# analyze_results.py
import json

def analyze_eval_results(log_file):
    with open(log_file) as f:
        data = [json.loads(line) for line in f]

    # Extract final metrics
    final_report = [d for d in data if d.get("type") == "final_report"][0]

    print(f"Accuracy: {final_report['accuracy']:.2%}")
    print(f"Total Samples: {final_report['num_samples']}")
    print(f"Correct: {final_report['num_correct']}")

    # Analyze failures
    failures = [d for d in data if d.get("type") == "match" and not d.get("correct")]

    print(f"\nFailures ({len(failures)}):")
    for fail in failures:
        print(f"  Input: {fail['prompt']}")
        print(f"  Expected: {fail['expected']}")
        print(f"  Got: {fail['sampled']}")
        print()

# Usage
analyze_eval_results("/tmp/evallogs/latest/results.jsonl")
```

### Example 2: Multiple Choice Evaluation

**Goal**: Evaluate model on multiple choice questions.

#### Step 1: Create Test Data

```jsonl
{"input": [{"role": "user", "content": "What is the capital of France?\nA) London\nB) Paris\nC) Berlin\nD) Madrid\n\nAnswer with just the letter."}], "ideal": "B"}
{"input": [{"role": "user", "content": "What is 15 * 7?\nA) 95\nB) 105\nC) 115\nD) 125\n\nAnswer with just the letter."}], "ideal": "B"}
{"input": [{"role": "user", "content": "Which gas do plants absorb from the atmosphere?\nA) Oxygen\nB) Nitrogen\nC) Carbon Dioxide\nD) Hydrogen\n\nAnswer with just the letter."}], "ideal": "C"}
```

Save as `data/multiple_choice.jsonl`.

#### Step 2: Create Evaluation

```yaml
# evals/multiple_choice.yaml
multiple_choice:
  class: evals.elsuite.basic.match:Match
  description: "Multiple choice questions"
  tags: ["multiple_choice", "qa"]
  args:
    samples_jsonl: data/multiple_choice.jsonl
    num_few_shot: 0
    max_tokens: 1
```

#### Step 3: Run Evaluation

```bash
oaieval gpt-3.5-turbo multiple_choice --record_path results/mc_results.jsonl
```

### Example 3: RAG System Evaluation

**Goal**: Evaluate a RAG system with context-based Q&A.

#### Step 1: Create Test Data with Context

```jsonl
{"input": [{"role": "system", "content": "Answer based on the provided context."}, {"role": "user", "content": "Context: Python was created by Guido van Rossum and first released in 1991.\n\nQuestion: Who created Python?"}], "ideal": ["Guido van Rossum", "van Rossum"]}
{"input": [{"role": "system", "content": "Answer based on the provided context."}, {"role": "user", "content": "Context: The Eiffel Tower was built in 1889 and stands 324 meters tall.\n\nQuestion: How tall is the Eiffel Tower?"}], "ideal": ["324 meters", "324m"]}
```

Save as `data/rag_eval.jsonl`.

#### Step 2: Create Includes Evaluation

```yaml
# evals/rag_eval.yaml
rag_eval:
  class: evals.elsuite.basic.includes:Includes
  description: "RAG system evaluation"
  tags: ["rag", "qa", "context"]
  args:
    samples_jsonl: data/rag_eval.jsonl
    num_few_shot: 0
    max_tokens: 100
```

#### Step 3: Run Evaluation

```bash
oaieval gpt-3.5-turbo rag_eval
```

### Example 4: Code Generation Evaluation

**Goal**: Evaluate code generation capabilities.

#### Step 1: Create Test Data

```jsonl
{"input": [{"role": "user", "content": "Write a Python function to calculate factorial. Only provide the function code."}], "ideal": ["def factorial", "if n == 0", "return", "n * factorial(n-1)"]}
{"input": [{"role": "user", "content": "Write a Python function to check if a string is a palindrome. Only provide the function code."}], "ideal": ["def is_palindrome", "return", "== [::-1]"]}
```

Save as `data/code_gen.jsonl`.

#### Step 2: Create Evaluation

```yaml
# evals/code_gen.yaml
code_gen:
  class: evals.elsuite.basic.includes:Includes
  description: "Code generation evaluation"
  tags: ["code", "generation"]
  args:
    samples_jsonl: data/code_gen.jsonl
    max_tokens: 300
```

#### Step 3: Run Evaluation

```bash
oaieval gpt-3.5-turbo code_gen
```

### Example 5: Model-Graded Evaluation

**Goal**: Use GPT-4 to grade GPT-3.5 responses for quality.

#### Step 1: Create Test Data

```jsonl
{"input": [{"role": "user", "content": "Explain quantum computing to a 10-year-old."}], "ideal": "A simple, clear explanation using analogies appropriate for children"}
{"input": [{"role": "user", "content": "What are the pros and cons of remote work?"}], "ideal": "Balanced discussion of advantages and disadvantages"}
```

Save as `data/quality_eval.jsonl`.

#### Step 2: Create Model-Graded Evaluation

```yaml
# evals/quality_eval.yaml
quality_eval:
  class: evals.elsuite.modelgraded.classify:ModelGradedSpec
  description: "Quality evaluation using GPT-4"
  tags: ["quality", "model_graded"]
  args:
    samples_jsonl: data/quality_eval.jsonl
    eval_type: cot_classify
    modelgraded_spec: quality_spec

quality_spec:
  prompt: |
    You are evaluating the quality of an AI assistant's response.

    User Question: {input}
    Assistant Response: {output}
    Expected Quality: {ideal}

    Evaluate the response on:
    1. Clarity and coherence
    2. Accuracy and relevance
    3. Completeness
    4. Appropriateness for the intended audience

    Let's think step by step about the quality.

    Then, provide your final evaluation as one of:
    [EXCELLENT] - Meets all criteria excellently
    [GOOD] - Meets most criteria well
    [FAIR] - Adequate but has issues
    [POOR] - Fails to meet criteria
  choice_strings: ["EXCELLENT", "GOOD", "FAIR", "POOR"]
  eval_model: gpt-4
```

#### Step 3: Run Evaluation

```bash
# GPT-3.5 being evaluated by GPT-4
oaieval gpt-3.5-turbo quality_eval
```

### Example 6: Chain-of-Thought Evaluation

**Goal**: Evaluate reasoning with explicit chain-of-thought.

#### Step 1: Create Custom Completion Function

```python
# completion_fns/cot_completion.py
from evals.completion_fns.openai import OpenAIChatCompletionFn
from typing import Any, Dict

class ChainOfThoughtCompletion(OpenAIChatCompletionFn):
    """Forces chain-of-thought reasoning."""

    def __call__(self, prompt, **kwargs) -> Dict[str, Any]:
        # Modify prompt to encourage CoT
        if isinstance(prompt, str):
            cot_prompt = f"{prompt}\n\nLet's think step by step:"
        else:
            # Message list format
            cot_prompt = prompt + [
                {"role": "user", "content": "Let's think step by step:"}
            ]

        # Call parent implementation
        return super().__call__(cot_prompt, **kwargs)
```

#### Step 2: Register Completion Function

```yaml
# evals/cot_reasoning.yaml
cot_reasoning:
  class: evals.elsuite.basic.includes:Includes
  description: "Chain-of-thought reasoning evaluation"
  tags: ["reasoning", "cot"]
  args:
    samples_jsonl: data/reasoning.jsonl
    completion_fn: completion_fns.cot_completion:ChainOfThoughtCompletion
```

#### Step 3: Create Test Data

```jsonl
{"input": "If a train travels 60 miles in 1 hour, how far will it travel in 3.5 hours at the same speed?", "ideal": ["210", "210 miles"]}
{"input": "A shirt costs $40 after a 20% discount. What was the original price?", "ideal": ["$50", "50"]}
```

Save as `data/reasoning.jsonl`.

#### Step 4: Run Evaluation

```bash
oaieval gpt-3.5-turbo cot_reasoning
```

### Example 7: Batch Model Comparison

**Goal**: Compare multiple models on the same evaluation.

#### Create Comparison Script

```bash
#!/bin/bash
# compare_models.sh

EVAL_NAME="qa_basic"
MODELS=("gpt-3.5-turbo" "gpt-4" "gpt-4-turbo-preview")

echo "Running model comparison for $EVAL_NAME"
echo "========================================"

for model in "${MODELS[@]}"; do
    echo "Evaluating $model..."
    oaieval "$model" "$EVAL_NAME" \
        --record_path "results/${EVAL_NAME}_${model//:/_}.jsonl" \
        --log_to_file "logs/${EVAL_NAME}_${model//:/_}.log"
    echo "Completed $model"
    echo "---"
done

echo "All evaluations complete!"
echo "Running analysis..."

python analyze_comparison.py results/${EVAL_NAME}_*.jsonl
```

#### Create Analysis Script

```python
# analyze_comparison.py
import json
import sys
from pathlib import Path
from typing import Dict, List

def extract_metrics(log_file: Path) -> Dict:
    """Extract key metrics from evaluation log."""
    with open(log_file) as f:
        data = [json.loads(line) for line in f]

    final_report = next(
        (d for d in data if d.get("type") == "final_report"),
        {}
    )

    return {
        "model": log_file.stem.split("_")[-1],
        "accuracy": final_report.get("accuracy", 0),
        "num_samples": final_report.get("num_samples", 0),
        "num_correct": final_report.get("num_correct", 0),
    }

def compare_models(log_files: List[Path]):
    """Compare metrics across models."""
    results = [extract_metrics(f) for f in log_files]

    # Sort by accuracy
    results.sort(key=lambda x: x["accuracy"], reverse=True)

    print("\nModel Comparison Results")
    print("=" * 60)
    print(f"{'Model':<30} {'Accuracy':<15} {'Correct/Total'}")
    print("-" * 60)

    for r in results:
        accuracy_pct = r["accuracy"] * 100
        print(f"{r['model']:<30} {accuracy_pct:>6.2f}%        "
              f"{r['num_correct']}/{r['num_samples']}")

    print("=" * 60)

if __name__ == "__main__":
    log_files = [Path(f) for f in sys.argv[1:]]
    compare_models(log_files)
```

#### Run Comparison

```bash
chmod +x compare_models.sh
./compare_models.sh
```

### Example 8: CI/CD Integration

**Goal**: Integrate evaluations into CI/CD pipeline.

#### GitHub Actions Workflow

```yaml
# .github/workflows/eval.yml
name: LLM Evaluation

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  evaluate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install evals openai
          pip install -e .

      - name: Run evaluations
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          # Run critical evaluations
          oaieval gpt-3.5-turbo qa_basic \
            --record_path results/qa_basic.jsonl

          oaieval gpt-3.5-turbo code_gen \
            --record_path results/code_gen.jsonl

      - name: Check thresholds
        run: |
          python scripts/check_thresholds.py \
            --results results/ \
            --min_accuracy 0.80

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: eval-results
          path: results/

      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(
              fs.readFileSync('results/summary.json', 'utf8')
            );

            const comment = `## Evaluation Results

            - QA Accuracy: ${(results.qa_accuracy * 100).toFixed(1)}%
            - Code Gen Accuracy: ${(results.code_accuracy * 100).toFixed(1)}%

            ${results.passed ? '✅ All checks passed' : '❌ Some checks failed'}
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

#### Threshold Checking Script

```python
# scripts/check_thresholds.py
import argparse
import json
import sys
from pathlib import Path
from typing import Dict

def check_evaluation_thresholds(
    results_dir: Path,
    min_accuracy: float
) -> bool:
    """Check if evaluation results meet minimum thresholds."""

    passed = True
    summary = {}

    for result_file in results_dir.glob("*.jsonl"):
        with open(result_file) as f:
            data = [json.loads(line) for line in f]

        final_report = next(
            (d for d in data if d.get("type") == "final_report"),
            {}
        )

        eval_name = result_file.stem
        accuracy = final_report.get("accuracy", 0)

        summary[f"{eval_name}_accuracy"] = accuracy

        if accuracy < min_accuracy:
            print(f"❌ {eval_name}: {accuracy:.2%} < {min_accuracy:.2%}")
            passed = False
        else:
            print(f"✅ {eval_name}: {accuracy:.2%} >= {min_accuracy:.2%}")

    # Write summary
    summary["passed"] = passed
    with open(results_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    return passed

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--min_accuracy", type=float, default=0.8)
    args = parser.parse_args()

    passed = check_evaluation_thresholds(
        args.results,
        args.min_accuracy
    )

    sys.exit(0 if passed else 1)
```

### Example 9: Few-Shot Evaluation

**Goal**: Compare zero-shot vs few-shot performance.

#### Step 1: Create Few-Shot Examples

```jsonl
{"input": "Translate to French: Hello", "ideal": "Bonjour"}
{"input": "Translate to French: Goodbye", "ideal": "Au revoir"}
{"input": "Translate to French: Thank you", "ideal": "Merci"}
{"input": "Translate to French: Please", "ideal": "S'il vous plaît"}
{"input": "Translate to French: Good morning", "ideal": "Bonjour"}
```

Save as `data/translation.jsonl`.

#### Step 2: Create Evaluations with Different Few-Shot Counts

```yaml
# evals/translation_0shot.yaml
translation_0shot:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: data/translation.jsonl
    num_few_shot: 0

# evals/translation_2shot.yaml
translation_2shot:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: data/translation.jsonl
    num_few_shot: 2

# evals/translation_5shot.yaml
translation_5shot:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: data/translation.jsonl
    num_few_shot: 5
```

#### Step 3: Run Comparison

```bash
# Compare few-shot configurations
for shots in 0 2 5; do
    echo "Testing ${shots}-shot..."
    oaieval gpt-3.5-turbo translation_${shots}shot \
        --record_path results/translation_${shots}shot.jsonl
done

# Analyze results
python analyze_fewshot.py
```

### Example 10: Custom Evaluation Class

**Goal**: Create fully custom evaluation logic.

#### Step 1: Create Custom Evaluator

```python
# custom_evals/semantic_similarity.py
from typing import Any, Dict
from evals.api import CompletionFn
from evals.eval import SolverEval
from evals.record import RecorderBase
from sentence_transformers import SentenceTransformer, util

class SemanticSimilarityEval(SolverEval):
    """Evaluate semantic similarity of responses."""

    def __init__(
        self,
        completion_fns: list[CompletionFn],
        samples_jsonl: str,
        similarity_threshold: float = 0.8,
        *args,
        **kwargs
    ):
        super().__init__(completion_fns, *args, **kwargs)
        self.samples_jsonl = samples_jsonl
        self.similarity_threshold = similarity_threshold

        # Load semantic similarity model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def eval_sample(self, sample: Dict[str, Any], rng):
        """Evaluate a single sample."""
        # Get model response
        result = self.completion_fn(
            prompt=sample["input"],
            temperature=0.0,
        )
        output = result.get_completions()[0]

        # Calculate semantic similarity
        ideal = sample["ideal"]
        output_embedding = self.model.encode(output, convert_to_tensor=True)
        ideal_embedding = self.model.encode(ideal, convert_to_tensor=True)

        similarity = util.cos_sim(output_embedding, ideal_embedding).item()

        # Record result
        correct = similarity >= self.similarity_threshold

        self.record_match(
            correct=correct,
            expected=ideal,
            picked=output,
            score=similarity
        )

    def run(self, recorder: RecorderBase):
        """Run the evaluation."""
        samples = self.get_samples()

        for sample in samples:
            self.eval_sample(sample, None)

        # Record final metrics
        return {
            "accuracy": self.get_metrics()["accuracy"],
            "mean_similarity": self.get_metrics()["mean_score"],
        }
```

#### Step 2: Register Custom Evaluation

```yaml
# evals/semantic_similarity.yaml
semantic_similarity:
  class: custom_evals.semantic_similarity:SemanticSimilarityEval
  description: "Semantic similarity evaluation"
  args:
    samples_jsonl: data/paraphrase_eval.jsonl
    similarity_threshold: 0.8
```

#### Step 3: Create Test Data

```jsonl
{"input": "What is machine learning?", "ideal": "Machine learning is a subset of AI that enables systems to learn from data"}
{"input": "Explain neural networks", "ideal": "Neural networks are computing systems inspired by biological neural networks"}
```

Save as `data/paraphrase_eval.jsonl`.

#### Step 4: Run Evaluation

```bash
# Install additional dependency
pip install sentence-transformers

# Run evaluation
oaieval gpt-3.5-turbo semantic_similarity
```

---

## Advanced Usage

### Multi-Turn Conversations

Evaluate multi-turn dialogue:

```jsonl
{"input": [
  {"role": "user", "content": "Hi, I need help with Python"},
  {"role": "assistant", "content": "Hello! I'd be happy to help with Python. What do you need?"},
  {"role": "user", "content": "How do I read a file?"}
], "ideal": ["open(", "read(", "with open"]}
```

### Conditional Evaluation

Evaluate based on sample metadata:

```python
class ConditionalEval(Eval):
    def eval_sample(self, sample, rng):
        # Check metadata
        difficulty = sample.get("metadata", {}).get("difficulty", "easy")

        # Use different thresholds
        if difficulty == "hard":
            threshold = 0.6
        else:
            threshold = 0.8

        # Evaluate with appropriate threshold
        score = self.evaluate_response(sample)
        correct = score >= threshold

        self.record_match(correct=correct, score=score)
```

### Parallel Evaluation

Speed up evaluations with parallelization:

```bash
# Set max workers
export EVALS_THREADS=10

# Run evaluation (automatically parallelized)
oaieval gpt-3.5-turbo my_eval
```

### Custom Sampling Strategies

Implement custom sampling:

```python
from evals.registry import Registry

class StratifiedSampler:
    """Sample evenly across difficulty levels."""

    def __init__(self, samples, samples_per_difficulty=10):
        self.samples_by_difficulty = self.group_by_difficulty(samples)
        self.samples_per_difficulty = samples_per_difficulty

    def group_by_difficulty(self, samples):
        grouped = {}
        for sample in samples:
            difficulty = sample.get("metadata", {}).get("difficulty", "medium")
            if difficulty not in grouped:
                grouped[difficulty] = []
            grouped[difficulty].append(sample)
        return grouped

    def __iter__(self):
        for difficulty, samples in self.samples_by_difficulty.items():
            # Sample evenly from each difficulty
            sampled = random.sample(
                samples,
                min(len(samples), self.samples_per_difficulty)
            )
            yield from sampled
```

### Result Aggregation

Aggregate results across multiple runs:

```python
import json
from pathlib import Path
from typing import List
import pandas as pd

def aggregate_eval_results(log_dir: Path) -> pd.DataFrame:
    """Aggregate results from multiple evaluation runs."""

    results = []

    for log_file in log_dir.glob("**/results.jsonl"):
        with open(log_file) as f:
            data = [json.loads(line) for line in f]

        # Extract final report
        final_report = next(
            (d for d in data if d.get("type") == "final_report"),
            {}
        )

        # Extract metadata
        metadata = next(
            (d for d in data if d.get("spec")),
            {}
        )

        results.append({
            "eval_name": metadata.get("eval_name"),
            "model": metadata.get("model"),
            "accuracy": final_report.get("accuracy"),
            "num_samples": final_report.get("num_samples"),
            "timestamp": metadata.get("timestamp"),
        })

    return pd.DataFrame(results)

# Usage
df = aggregate_eval_results(Path("/tmp/evallogs"))
print(df.groupby("model")["accuracy"].mean())
```

### Dynamic Sample Generation

Generate samples programmatically:

```python
from evals.data import get_jsonl
import random

class DynamicSampler:
    """Generate samples on the fly."""

    def __init__(self, num_samples=100):
        self.num_samples = num_samples

    def generate_math_problem(self):
        """Generate a random math problem."""
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        op = random.choice(["+", "-", "*"])

        if op == "+":
            answer = a + b
        elif op == "-":
            answer = a - b
        else:
            answer = a * b

        return {
            "input": f"What is {a} {op} {b}?",
            "ideal": str(answer)
        }

    def __iter__(self):
        for _ in range(self.num_samples):
            yield self.generate_math_problem()
```

### Evaluation Chaining

Chain multiple evaluations:

```python
# chain_evals.py
import subprocess
from typing import List

def run_eval_chain(model: str, eval_names: List[str]):
    """Run a chain of evaluations sequentially."""

    results = {}

    for eval_name in eval_names:
        print(f"Running {eval_name}...")

        # Run evaluation
        result = subprocess.run(
            ["oaieval", model, eval_name],
            capture_output=True,
            text=True
        )

        # Check success
        if result.returncode != 0:
            print(f"❌ {eval_name} failed")
            results[eval_name] = {"status": "failed", "error": result.stderr}
        else:
            print(f"✅ {eval_name} passed")
            results[eval_name] = {"status": "passed"}

    return results

# Usage
eval_chain = [
    "qa_basic",
    "code_gen",
    "reasoning",
    "safety"
]

results = run_eval_chain("gpt-3.5-turbo", eval_chain)
```

---

## Best Practices

### 1. Evaluation Design

#### Keep Test Sets Clean

```python
# BAD: Overlapping train and test data
train_data = load_data("all_data.jsonl")
test_data = train_data[:100]  # First 100 samples

# GOOD: Separate train and test splits
train_data = load_data("train.jsonl")
test_data = load_data("test.jsonl")  # Completely separate
```

#### Use Representative Samples

```yaml
# BAD: Only easy examples
samples_jsonl: easy_only.jsonl

# GOOD: Balanced difficulty distribution
samples_jsonl: balanced_difficulty.jsonl
# With stratified sampling
```

#### Version Your Evaluations

```yaml
# Include version in eval name
qa_basic_v1:
  class: evals.elsuite.basic.match:Match
  description: "QA evaluation v1 - initial version"
  args:
    samples_jsonl: data/qa_v1.jsonl

qa_basic_v2:
  class: evals.elsuite.basic.match:Match
  description: "QA evaluation v2 - added harder questions"
  args:
    samples_jsonl: data/qa_v2.jsonl
```

### 2. Data Management

#### Organize Test Data

```
data/
├── qa/
│   ├── basic.jsonl
│   ├── advanced.jsonl
│   └── expert.jsonl
├── code/
│   ├── python.jsonl
│   ├── javascript.jsonl
│   └── sql.jsonl
└── reasoning/
    ├── logical.jsonl
    └── mathematical.jsonl
```

#### Document Data Provenance

```jsonl
{"input": "Question", "ideal": "Answer", "metadata": {"source": "wikipedia", "date": "2024-01-01", "verified": true}}
```

#### Validate Test Data

```python
def validate_eval_data(jsonl_file):
    """Validate evaluation data format."""

    required_fields = ["input", "ideal"]

    with open(jsonl_file) as f:
        for i, line in enumerate(f, 1):
            try:
                sample = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Line {i}: Invalid JSON - {e}")
                continue

            # Check required fields
            for field in required_fields:
                if field not in sample:
                    print(f"Line {i}: Missing required field '{field}'")

            # Validate input format
            if isinstance(sample["input"], list):
                for msg in sample["input"]:
                    if "role" not in msg or "content" not in msg:
                        print(f"Line {i}: Invalid message format")
```

### 3. Model Configuration

#### Use Consistent Settings

```python
# Define standard configurations
EVAL_CONFIGS = {
    "deterministic": {
        "temperature": 0.0,
        "top_p": 1.0,
        "seed": 42
    },
    "creative": {
        "temperature": 0.7,
        "top_p": 0.9,
    },
    "conservative": {
        "temperature": 0.3,
        "presence_penalty": 0.1,
    }
}
```

#### Handle Rate Limits

```python
# Set reasonable concurrency
export EVALS_THREADS=5  # Don't overwhelm API

# Add delays between requests
export EVALS_SEQUENTIAL=true  # For strict rate limiting
```

### 4. Result Analysis

#### Statistical Significance

```python
from scipy import stats

def compare_models_significance(results1, results2):
    """Test if difference between models is significant."""

    # Extract accuracy scores
    scores1 = [r["correct"] for r in results1]
    scores2 = [r["correct"] for r in results2]

    # Perform t-test
    t_stat, p_value = stats.ttest_ind(scores1, scores2)

    print(f"T-statistic: {t_stat:.3f}")
    print(f"P-value: {p_value:.3f}")

    if p_value < 0.05:
        print("Difference is statistically significant")
    else:
        print("Difference is not statistically significant")
```

#### Error Analysis

```python
def analyze_errors(log_file):
    """Detailed error analysis."""

    with open(log_file) as f:
        data = [json.loads(line) for line in f]

    errors = [d for d in data if d.get("type") == "match" and not d.get("correct")]

    # Categorize errors
    error_types = {
        "wrong_answer": [],
        "formatting": [],
        "incomplete": [],
        "hallucination": [],
    }

    for error in errors:
        # Categorization logic
        output = error.get("sampled", "")
        expected = error.get("expected", "")

        if len(output) < len(expected) * 0.5:
            error_types["incomplete"].append(error)
        elif not any(word in output.lower() for word in expected.lower().split()):
            error_types["hallucination"].append(error)
        else:
            error_types["wrong_answer"].append(error)

    # Report
    for error_type, instances in error_types.items():
        print(f"{error_type}: {len(instances)} errors")
```

### 5. Performance Optimization

#### Batch Processing

```python
# Process multiple samples in parallel
export EVALS_THREADS=10
oaieval gpt-3.5-turbo large_eval
```

#### Sample Efficiently

```bash
# Limit samples for quick testing
oaieval gpt-3.5-turbo my_eval --max_samples 50

# Use full dataset for final evaluation
oaieval gpt-3.5-turbo my_eval
```

#### Cache Results

```python
# Use consistent record paths for caching
oaieval gpt-3.5-turbo my_eval \
    --record_path results/cached_run.jsonl

# Reuse results for analysis without re-running
```

### 6. Maintenance

#### Regular Updates

```bash
# Update evals framework
pip install --upgrade evals

# Update community evals
cd evals
git pull origin main
```

#### Monitor Costs

```python
def estimate_eval_cost(
    num_samples: int,
    avg_prompt_tokens: int,
    avg_completion_tokens: int,
    model: str = "gpt-3.5-turbo"
):
    """Estimate cost of running evaluation."""

    # Pricing (as of 2024)
    prices = {
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},  # per 1K tokens
        "gpt-4": {"input": 0.03, "output": 0.06},
    }

    model_price = prices.get(model, prices["gpt-3.5-turbo"])

    input_cost = (avg_prompt_tokens * num_samples / 1000) * model_price["input"]
    output_cost = (avg_completion_tokens * num_samples / 1000) * model_price["output"]

    total_cost = input_cost + output_cost

    print(f"Estimated cost for {num_samples} samples:")
    print(f"  Input: ${input_cost:.2f}")
    print(f"  Output: ${output_cost:.2f}")
    print(f"  Total: ${total_cost:.2f}")

    return total_cost
```

---

## Integration Guide

### LangChain Integration

```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

# Create LangChain chain
llm = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("Answer this question: {question}")
chain = LLMChain(llm=llm, prompt=prompt)

# Wrap for OpenAI Evals
from evals.completion_fns import CompletionFnSpec

class LangChainCompletionFn(CompletionFnSpec):
    def __init__(self, chain, **kwargs):
        super().__init__(**kwargs)
        self.chain = chain

    def __call__(self, prompt, **kwargs):
        # Extract question from prompt
        if isinstance(prompt, list):
            question = prompt[-1]["content"]
        else:
            question = prompt

        # Run chain
        result = self.chain.run(question=question)

        return {"choices": [{"message": {"content": result}}]}

# Register and use
completion_fn = LangChainCompletionFn(chain)
```

### LlamaIndex Integration

```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from evals.completion_fns import CompletionFnSpec

class LlamaIndexCompletionFn(CompletionFnSpec):
    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        self.query_engine = index.as_query_engine()

    def __call__(self, prompt, **kwargs):
        # Extract query
        if isinstance(prompt, list):
            query = prompt[-1]["content"]
        else:
            query = prompt

        # Query index
        response = self.query_engine.query(query)

        return {
            "choices": [{
                "message": {
                    "content": str(response)
                }
            }]
        }

# Setup
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

# Use with evals
completion_fn = LlamaIndexCompletionFn(index)
```

### Hugging Face Integration

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from evals.completion_fns import CompletionFnSpec

class HuggingFaceCompletionFn(CompletionFnSpec):
    def __init__(self, model_name, **kwargs):
        super().__init__(**kwargs)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def __call__(self, prompt, **kwargs):
        # Format prompt
        if isinstance(prompt, list):
            formatted = self.tokenizer.apply_chat_template(
                prompt,
                tokenize=False
            )
        else:
            formatted = prompt

        # Generate
        inputs = self.tokenizer(formatted, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=100)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {
            "choices": [{
                "message": {
                    "content": response
                }
            }]
        }

# Usage
completion_fn = HuggingFaceCompletionFn("meta-llama/Llama-2-7b-chat-hf")
```

### Azure OpenAI Integration

```python
# Set Azure environment variables
export AZURE_OPENAI_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export OPENAI_API_TYPE="azure"
export OPENAI_API_VERSION="2023-05-15"

# Create Azure-compatible completion function
from evals.completion_fns.openai import OpenAIChatCompletionFn

class AzureCompletionFn(OpenAIChatCompletionFn):
    def __init__(self, deployment_name, **kwargs):
        super().__init__(model=deployment_name, **kwargs)
        self.deployment_name = deployment_name
```

### MLflow Integration

```python
import mlflow
from mlflow.tracking import MlflowClient

def run_eval_with_mlflow(model_name, eval_name):
    """Run evaluation and log to MLflow."""

    with mlflow.start_run(run_name=f"{eval_name}_{model_name}"):
        # Log parameters
        mlflow.log_param("model", model_name)
        mlflow.log_param("eval", eval_name)

        # Run evaluation
        result = subprocess.run(
            ["oaieval", model_name, eval_name,
             "--record_path", "temp_results.jsonl"],
            capture_output=True,
            text=True
        )

        # Parse results
        with open("temp_results.jsonl") as f:
            data = [json.loads(line) for line in f]

        final_report = next(
            (d for d in data if d.get("type") == "final_report"),
            {}
        )

        # Log metrics
        mlflow.log_metric("accuracy", final_report.get("accuracy", 0))
        mlflow.log_metric("num_samples", final_report.get("num_samples", 0))

        # Log artifact
        mlflow.log_artifact("temp_results.jsonl")

# Usage
run_eval_with_mlflow("gpt-3.5-turbo", "qa_basic")
```

### Weights & Biases Integration

```python
import wandb

def run_eval_with_wandb(model_name, eval_name):
    """Run evaluation and log to W&B."""

    # Initialize run
    run = wandb.init(
        project="llm-evals",
        name=f"{eval_name}_{model_name}",
        config={
            "model": model_name,
            "eval": eval_name,
        }
    )

    # Run evaluation
    result = subprocess.run(
        ["oaieval", model_name, eval_name,
         "--record_path", "temp_results.jsonl"],
        capture_output=True
    )

    # Parse and log results
    with open("temp_results.jsonl") as f:
        data = [json.loads(line) for line in f]

    # Log metrics
    final_report = next(
        (d for d in data if d.get("type") == "final_report"),
        {}
    )

    wandb.log({
        "accuracy": final_report.get("accuracy"),
        "num_samples": final_report.get("num_samples"),
    })

    # Log artifact
    wandb.save("temp_results.jsonl")

    run.finish()

# Usage
run_eval_with_wandb("gpt-3.5-turbo", "qa_basic")
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Module Not Found

**Problem:**
```
ModuleNotFoundError: No module named 'evals'
```

**Solutions:**
```bash
# Reinstall evals
pip uninstall evals
pip install evals

# Or install from source
git clone https://github.com/openai/evals.git
cd evals
pip install -e .

# Verify
python -c "import evals; print(evals.__version__)"
```

#### Issue 2: Evaluation Not Found

**Problem:**
```
Error: Evaluation 'my_eval' not found in registry
```

**Solutions:**
```bash
# Check registry path
echo $EVALS_REGISTRY_PATH

# Set registry path
export EVALS_REGISTRY_PATH=/path/to/evals

# List available evaluations
oaieval --list

# Verify YAML syntax
python -c "import yaml; yaml.safe_load(open('evals/my_eval.yaml'))"
```

#### Issue 3: API Key Errors

**Problem:**
```
Error: OpenAI API key not found
```

**Solutions:**
```bash
# Set API key
export OPENAI_API_KEY="sk-..."

# Verify key is set
echo $OPENAI_API_KEY

# Check key is valid
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### Issue 4: Rate Limiting

**Problem:**
```
Error: Rate limit exceeded
```

**Solutions:**
```bash
# Reduce concurrency
export EVALS_THREADS=1

# Add delay between requests
export EVALS_SEQUENTIAL=true

# Use tier-appropriate model
oaieval gpt-3.5-turbo my_eval  # Higher rate limits than GPT-4
```

#### Issue 5: JSON Parsing Errors

**Problem:**
```
JSONDecodeError: Expecting value: line 1 column 1
```

**Solutions:**
```bash
# Validate JSONL file
python -c "
import json
with open('data.jsonl') as f:
    for i, line in enumerate(f, 1):
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            print(f'Line {i}: {e}')
"

# Fix common issues
# - Ensure one JSON object per line
# - No trailing commas
# - Proper quote escaping
```

#### Issue 6: Memory Issues

**Problem:**
```
MemoryError: Unable to allocate array
```

**Solutions:**
```bash
# Limit samples
oaieval gpt-3.5-turbo my_eval --max_samples 100

# Process in batches
split -l 100 large_data.jsonl batch_

# Reduce logging verbosity
export EVALS_LOG_LEVEL=WARNING
```

### Debugging Techniques

#### Enable Debug Logging

```bash
export EVALS_LOG_LEVEL=DEBUG
oaieval gpt-3.5-turbo my_eval 2>&1 | tee debug.log
```

#### Inspect Evaluation Spec

```python
from evals.registry import Registry

registry = Registry()
spec = registry.get_eval("my_eval")

print("Class:", spec.cls)
print("Args:", spec.args)
print("Metadata:", spec.metadata)
```

#### Test with Single Sample

```bash
# Create minimal test
echo '{"input": "test", "ideal": "test"}' > test.jsonl

# Run on single sample
oaieval gpt-3.5-turbo test_eval --max_samples 1
```

#### Validate Completion Function

```python
from evals.registry import Registry

registry = Registry()
completion_fn = registry.make_completion_fn("gpt-3.5-turbo")

# Test call
result = completion_fn(
    prompt=[{"role": "user", "content": "Hello"}],
    temperature=0.0
)

print(result)
```

### Performance Issues

#### Slow Evaluations

**Diagnosis:**
```bash
# Time evaluation
time oaieval gpt-3.5-turbo my_eval

# Profile
python -m cProfile -o profile.stats oaieval_script.py
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(20)"
```

**Solutions:**
- Increase concurrency: `export EVALS_THREADS=10`
- Use faster model: `gpt-3.5-turbo` instead of `gpt-4`
- Reduce max_tokens in eval config
- Cache results for repeated analysis

#### High API Costs

**Diagnosis:**
```python
def estimate_tokens(text):
    """Rough token estimate."""
    return len(text.split()) * 1.3

# Analyze dataset
total_tokens = 0
with open("data.jsonl") as f:
    for line in f:
        sample = json.loads(line)
        prompt = str(sample["input"])
        total_tokens += estimate_tokens(prompt)

print(f"Estimated input tokens: {total_tokens:,}")
```

**Solutions:**
- Use cheaper model for initial testing
- Limit samples during development
- Optimize prompts for brevity
- Use caching for repeated evaluations

---

## API Reference

### CLI Commands

#### oaieval

Main command for running evaluations:

```bash
oaieval [OPTIONS] MODEL EVAL_NAME
```

**Arguments:**
- `MODEL`: Model identifier (e.g., `gpt-3.5-turbo`, `gpt-4`)
- `EVAL_NAME`: Name of evaluation from registry

**Options:**
- `--max_samples N`: Limit to N samples
- `--record_path PATH`: Save results to PATH
- `--log_to_file PATH`: Save logs to PATH
- `--registry_path PATH`: Use custom registry
- `--debug`: Enable debug logging
- `--dry_run`: Validate without running
- `--list`: List available evaluations

**Examples:**
```bash
# Basic usage
oaieval gpt-3.5-turbo qa_basic

# With options
oaieval gpt-4 code_gen --max_samples 50 --record_path results.jsonl

# List evaluations
oaieval --list
```

### Python API

#### Registry

```python
from evals.registry import Registry

registry = Registry()

# Get evaluation spec
spec = registry.get_eval("eval_name")

# Create completion function
completion_fn = registry.make_completion_fn("gpt-3.5-turbo")

# List evaluations
all_evals = registry.get_evals()
```

#### Evaluation Base Class

```python
from evals.eval import Eval

class MyCustomEval(Eval):
    def __init__(self, completion_fns, samples_jsonl, **kwargs):
        super().__init__(completion_fns, **kwargs)
        self.samples_jsonl = samples_jsonl

    def eval_sample(self, sample, rng):
        """Evaluate a single sample."""
        # Get model response
        result = self.completion_fn(
            prompt=sample["input"],
            temperature=0.0
        )

        output = result.get_completions()[0]

        # Score output
        correct = self.score_output(output, sample["ideal"])

        # Record result
        self.record_match(
            correct=correct,
            expected=sample["ideal"],
            picked=output
        )

    def score_output(self, output, ideal):
        """Custom scoring logic."""
        return output.strip().lower() == ideal.strip().lower()
```

#### Completion Functions

```python
from evals.completion_fns import CompletionFnSpec
from evals.completion_fns.openai import OpenAIChatCompletionFn

# Use built-in
completion_fn = OpenAIChatCompletionFn(model="gpt-3.5-turbo")

# Create custom
class MyCompletionFn(CompletionFnSpec):
    def __call__(self, prompt, **kwargs):
        # Custom completion logic
        return {
            "choices": [{
                "message": {
                    "content": "response text"
                }
            }]
        }
```

#### Recording Results

```python
from evals.record import RecorderBase, record_match

# Record match result
record_match(
    correct=True,
    expected="ideal answer",
    picked="model answer",
    score=0.95
)

# Record custom metric
recorder = RecorderBase.get_recorder()
recorder.record_event("custom_metric", value=0.8)
```

### Configuration Files

#### Evaluation YAML

```yaml
eval_id:
  # Required: Evaluation class
  class: evals.elsuite.basic.match:Match

  # Optional: Metadata
  description: "Description of evaluation"
  tags: ["tag1", "tag2"]
  version: "1.0"

  # Required: Arguments
  args:
    samples_jsonl: data/samples.jsonl
    num_few_shot: 0
    max_tokens: 100

    # Optional: Completion function
    completion_fn: custom.completion:MyCompletionFn

    # Custom arguments
    custom_arg: value
```

#### Sampler Formats

**JSONL:**
```jsonl
{"input": "prompt text", "ideal": "expected output"}
{"input": [{"role": "user", "content": "message"}], "ideal": "expected"}
```

**CSV:**
```csv
input,ideal
"prompt 1","output 1"
"prompt 2","output 2"
```

---

## Performance

### Benchmarking

#### Evaluation Speed

Typical performance (approximate):

| Configuration | Samples/Minute | Notes |
|--------------|----------------|-------|
| Sequential | 10-20 | `EVALS_THREADS=1` |
| Parallel (5 workers) | 40-80 | `EVALS_THREADS=5` |
| Parallel (10 workers) | 60-120 | `EVALS_THREADS=10` |
| GPT-3.5-turbo | 1.5x faster | vs GPT-4 |
| GPT-4-turbo | 1.2x faster | vs GPT-4 |

#### Token Processing

| Model | Tokens/Second | Max Tokens |
|-------|---------------|------------|
| GPT-3.5-turbo | ~100-150 | 4,096 |
| GPT-4 | ~40-60 | 8,192 |
| GPT-4-turbo | ~80-120 | 128,000 |

### Optimization Strategies

#### 1. Parallel Processing

```bash
# Optimal for most cases
export EVALS_THREADS=10

# For rate-limited scenarios
export EVALS_THREADS=3
```

#### 2. Batch Sampling

```python
# Process samples in batches
class BatchedSampler:
    def __init__(self, samples, batch_size=10):
        self.samples = samples
        self.batch_size = batch_size

    def __iter__(self):
        for i in range(0, len(self.samples), self.batch_size):
            yield self.samples[i:i + self.batch_size]
```

#### 3. Model Selection

```bash
# Development: Use faster, cheaper model
oaieval gpt-3.5-turbo my_eval

# Production: Use more capable model
oaieval gpt-4 my_eval

# Cost-sensitive: Use mini models
oaieval gpt-3.5-turbo-0125 my_eval
```

#### 4. Caching

```python
import functools
from hashlib import md5

@functools.lru_cache(maxsize=1000)
def cached_completion(prompt_hash, model):
    """Cache completions by prompt hash."""
    # Actual completion call
    return completion_fn(prompt)

# Use cached version
def eval_with_cache(prompt, model):
    prompt_hash = md5(str(prompt).encode()).hexdigest()
    return cached_completion(prompt_hash, model)
```

### Monitoring

#### Track Evaluation Progress

```python
from tqdm import tqdm

class ProgressEval(Eval):
    def run(self, recorder):
        samples = self.get_samples()

        for sample in tqdm(samples, desc="Evaluating"):
            self.eval_sample(sample, None)

        return self.get_metrics()
```

#### Resource Usage

```bash
# Monitor CPU/memory
watch -n 1 'ps aux | grep oaieval'

# Track API usage
# (Check OpenAI dashboard for real-time usage)
```

---

## Security

### API Key Management

#### Best Practices

```bash
# ❌ BAD: Hardcode in scripts
OPENAI_API_KEY="sk-..."

# ✅ GOOD: Use environment variables
export OPENAI_API_KEY="sk-..."

# ✅ BETTER: Use .env file (not committed to git)
echo "OPENAI_API_KEY=sk-..." > .env
source .env

# ✅ BEST: Use secrets manager
# (e.g., AWS Secrets Manager, HashiCorp Vault)
```

#### Gitignore Configuration

```gitignore
# .gitignore
.env
*.jsonl
/tmp/evallogs/
results/
*.log
```

### Data Privacy

#### Sanitize Test Data

```python
def sanitize_sample(sample):
    """Remove sensitive information from samples."""

    # Remove PII patterns
    import re

    text = str(sample)

    # Remove emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)

    # Remove phone numbers
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)

    # Remove SSN
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)

    return text
```

#### Secure Logging

```python
# Disable sensitive logging
export EVALS_LOG_PROMPTS=false

# Or filter logs programmatically
def filter_sensitive_logs(log_file):
    """Remove sensitive info from logs."""
    with open(log_file) as f:
        data = [json.loads(line) for line in f]

    filtered = []
    for entry in data:
        # Remove prompt content
        if "prompt" in entry:
            entry["prompt"] = "[REDACTED]"

        filtered.append(entry)

    with open(log_file + ".filtered", "w") as f:
        for entry in filtered:
            f.write(json.dumps(entry) + "\n")
```

### Access Control

#### Restrict Evaluation Access

```python
# role_based_eval.py
ALLOWED_EVALS = {
    "developer": ["qa_basic", "code_gen"],
    "researcher": ["qa_basic", "code_gen", "advanced_reasoning"],
    "admin": ["*"],  # All evaluations
}

def check_permission(user_role, eval_name):
    """Check if user can run evaluation."""
    allowed = ALLOWED_EVALS.get(user_role, [])

    if "*" in allowed or eval_name in allowed:
        return True

    raise PermissionError(f"User role '{user_role}' cannot run '{eval_name}'")
```

### Audit Logging

```python
import logging
from datetime import datetime

def audit_log_eval(user, model, eval_name, results):
    """Log evaluation runs for auditing."""

    audit_logger = logging.getLogger("audit")
    audit_logger.setLevel(logging.INFO)

    handler = logging.FileHandler("audit.log")
    audit_logger.addHandler(handler)

    audit_logger.info({
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "model": model,
        "eval": eval_name,
        "accuracy": results.get("accuracy"),
        "num_samples": results.get("num_samples"),
    })
```

---

## References

### Official Documentation

1. **OpenAI Evals GitHub Repository**
   - URL: https://github.com/openai/evals
   - Description: Official source code and documentation
   - Content: Installation, examples, contribution guide

2. **OpenAI Evals Documentation**
   - URL: https://github.com/openai/evals/tree/main/docs
   - Description: Detailed documentation and guides
   - Content: Evaluation types, custom evaluators, best practices

3. **OpenAI API Documentation**
   - URL: https://platform.openai.com/docs
   - Description: API reference for models used in evals
   - Content: Model specifications, rate limits, pricing

### Community Resources

4. **OpenAI Community Forum**
   - URL: https://community.openai.com/
   - Description: Community discussions and support
   - Content: Tips, troubleshooting, evaluation strategies

5. **OpenAI Evals Registry**
   - URL: https://github.com/openai/evals/tree/main/evals/registry
   - Description: Community-contributed evaluations
   - Content: 100+ pre-built evaluations

### Research Papers

6. **"Language Models are Few-Shot Learners" (GPT-3 Paper)**
   - Authors: Brown et al., 2020
   - URL: https://arxiv.org/abs/2005.14165
   - Relevance: Foundation for evaluation methodologies

7. **"Evaluating Large Language Models Trained on Code"**
   - Authors: Chen et al., 2021
   - URL: https://arxiv.org/abs/2107.03374
   - Relevance: Code evaluation techniques (HumanEval dataset)

8. **"Training Language Models to Follow Instructions" (InstructGPT)**
   - Authors: Ouyang et al., 2022
   - URL: https://arxiv.org/abs/2203.02155
   - Relevance: Instruction-following evaluation

9. **"Holistic Evaluation of Language Models (HELM)"**
   - Authors: Liang et al., 2022
   - URL: https://arxiv.org/abs/2211.09110
   - Relevance: Comprehensive evaluation framework

10. **"Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"**
    - Authors: Zheng et al., 2023
    - URL: https://arxiv.org/abs/2306.05685
    - Relevance: Model-graded evaluation methodology

### Tutorial Videos

11. **"Getting Started with OpenAI Evals"**
    - Platform: YouTube
    - Creator: OpenAI Developer
    - URL: Search "OpenAI Evals tutorial"
    - Content: Installation, basic usage, creating custom evals

12. **"Building Custom Evaluations for LLMs"**
    - Platform: YouTube
    - Creator: AI Engineering
    - Content: Advanced evaluation patterns

### Blog Posts

13. **"Introducing OpenAI Evals"**
    - URL: https://openai.com/blog/
    - Description: Official announcement and overview
    - Content: Motivation, architecture, community involvement

14. **"Best Practices for LLM Evaluation"**
    - Various ML blogs (Towards Data Science, Medium)
    - Content: Practical tips from practitioners

15. **"How to Evaluate RAG Systems"**
    - Multiple sources
    - Content: RAG-specific evaluation strategies

### Tools and Libraries

16. **sentence-transformers**
    - URL: https://www.sbert.net/
    - Purpose: Semantic similarity evaluation
    - Integration: Custom evaluators

17. **ROUGE / BLEU**
    - Package: `rouge-score`, `sacrebleu`
    - Purpose: Text generation metrics
    - Integration: Custom scoring functions

18. **pytest**
    - URL: https://pytest.org/
    - Purpose: Integration testing
    - Integration: Evaluation in test suites

### Example Repositories

19. **OpenAI Evals Examples**
    - URL: https://github.com/openai/evals/tree/main/examples
    - Content: Example evaluations and completion functions

20. **Community Eval Collections**
    - Various GitHub repositories
    - Search: "openai evals custom"
    - Content: Real-world evaluation implementations

### Related Frameworks

21. **EleutherAI LM Evaluation Harness**
    - URL: https://github.com/EleutherAI/lm-evaluation-harness
    - Comparison: Alternative evaluation framework
    - Differences: Focus on open models, more academic

22. **BIG-bench**
    - URL: https://github.com/google/BIG-bench
    - Comparison: Large-scale benchmark suite
    - Differences: More comprehensive, less flexible

23. **HELM (Holistic Evaluation of Language Models)**
    - URL: https://crfm.stanford.edu/helm/
    - Comparison: Stanford's comprehensive eval framework
    - Differences: Research-focused, extensive metrics

### Standards and Specifications

24. **JSON Lines (JSONL) Specification**
    - URL: https://jsonlines.org/
    - Relevance: Data format for evaluations

25. **OpenAPI/ChatML Format**
    - URL: https://github.com/openai/openai-python
    - Relevance: Message format for chat models

### Courses and Training

26. **"Evaluating and Debugging Generative AI"** (DeepLearning.AI)
    - Platform: Coursera / DeepLearning.AI
    - Content: Systematic evaluation approaches

27. **"LLMOps: Deploying and Maintaining LLMs"**
    - Various platforms
    - Content: Production evaluation strategies

### Datasets

28. **MMLU (Massive Multitask Language Understanding)**
    - URL: https://github.com/hendrycks/test
    - Purpose: Comprehensive knowledge evaluation

29. **TruthfulQA**
    - URL: https://github.com/sylinrl/TruthfulQA
    - Purpose: Truthfulness evaluation

30. **HumanEval**
    - URL: https://github.com/openai/human-eval
    - Purpose: Code generation evaluation

### Conferences and Events

31. **NeurIPS - Datasets and Benchmarks Track**
    - URL: https://neurips.cc/
    - Relevance: Latest evaluation methodologies

32. **EMNLP / ACL**
    - Focus: NLP evaluation techniques
    - Relevance: Academic evaluation standards

---

## Conclusion

OpenAI Evals provides a robust, standardized framework for evaluating LLMs with emphasis on reproducibility and community collaboration. Its CLI-first design makes it ideal for automation and CI/CD integration, while its extensibility allows for custom evaluation logic.

**Key Takeaways:**

1. **Standardization**: Consistent format ensures reproducible results
2. **Community**: Large collection of pre-built evaluations
3. **Automation**: CLI interface perfect for CI/CD
4. **Extensibility**: Easy to create custom evaluators
5. **Open Source**: Full transparency and community contributions

**When to Use OpenAI Evals:**

- Need reproducible, standardized evaluations
- Building CI/CD pipelines for LLM applications
- Want to leverage community evaluations
- Comparing different models systematically
- Academic research requiring reproducibility

**When to Consider Alternatives:**

- Need rich dashboards (consider TruLens, LangSmith)
- Want pytest integration (consider DeepEval)
- Focus on RAG systems (consider RAGAS)
- Need production observability (consider Langfuse)

OpenAI Evals excels at providing a solid foundation for systematic LLM evaluation with strong emphasis on reproducibility and standardization.

---

**Document Version:** 1.0
**Last Updated:** 2024-01-18
**Author:** AI Evaluation Team
**License:** MIT
