# MLflow: Deep Dive Guide

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

### What is MLflow?

MLflow is an **open-source platform for managing the end-to-end machine learning lifecycle**. While not exclusively an LLM evaluation framework, MLflow has become essential for LLM application development through its experiment tracking, model registry, and evaluation capabilities.

**Key Characteristics:**

- **Experiment Tracking**: Track parameters, metrics, and artifacts
- **Model Registry**: Centralized model storage and versioning
- **Model Deployment**: Deploy models to various platforms
- **LLM Evaluation**: Specialized tools for evaluating LLMs
- **Prompt Engineering**: Track and version prompts
- **UI Dashboard**: Visual interface for exploring experiments
- **Integration**: Works with all major ML frameworks
- **Open Source**: Vendor-neutral and extensible

### Why Use MLflow for LLM Evaluation?

**Strengths:**

1. **Comprehensive Tracking**: Log everything about your experiments
2. **Built-in LLM Evaluators**: Pre-built metrics for common LLM tasks
3. **Prompt Versioning**: Track prompt changes over time
4. **Model Comparison**: Easy comparison of different models
5. **Production Ready**: Battle-tested in production environments
6. **Ecosystem**: Large community and extensive integrations
7. **Flexibility**: Use for experimentation and production
8. **Cost Tracking**: Monitor API costs across experiments

**Ideal Use Cases:**

- LLM model comparison and selection
- Prompt engineering experiments
- Fine-tuning experiment tracking
- RAG system evaluation
- Production model monitoring
- A/B testing for LLM applications
- Team collaboration on ML projects
- Model versioning and governance

### Framework Philosophy

MLflow design principles:

1. **Open**: Works with any ML library or framework
2. **Modular**: Use components independently
3. **Scalable**: From laptop to data center
4. **Reproducible**: Track everything needed to reproduce results
5. **Collaborative**: Share experiments across teams
6. **Production-Focused**: Bridge research and production
7. **Simple**: Easy to get started, powerful when needed

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                       MLflow Platform                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  MLflow Tracking                             │  │
│  │  - Run management                                            │  │
│  │  - Parameter logging                                         │  │
│  │  - Metric logging                                            │  │
│  │  - Artifact storage                                          │  │
│  │  - Metadata database                                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ↓                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  MLflow Models                               │  │
│  │  - Model packaging                                           │  │
│  │  - Model flavors (sklearn, pytorch, custom, etc.)           │  │
│  │  - Model signature                                           │  │
│  │  - Environment capture                                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ↓                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  MLflow Model Registry                       │  │
│  │  - Model versioning                                          │  │
│  │  - Stage transitions (staging, production)                   │  │
│  │  - Model lineage                                             │  │
│  │  - Annotations and metadata                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ↓                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │               MLflow Evaluate (LLM Focus)                    │  │
│  │  ┌────────────┬────────────┬────────────┬──────────────┐    │  │
│  │  │ Built-in   │  Custom    │  LLM-as-   │  Statistical │    │  │
│  │  │ Metrics    │  Metrics   │  Judge     │  Metrics     │    │  │
│  │  └────────────┴────────────┴────────────┴──────────────┘    │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ↓                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  MLflow Deployments                          │  │
│  │  - Deployment to various platforms                           │  │
│  │  - Serving infrastructure                                    │  │
│  │  - Batch inference                                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ↓                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   MLflow UI                                  │  │
│  │  - Experiment comparison                                     │  │
│  │  - Metric visualization                                      │  │
│  │  - Artifact browser                                          │  │
│  │  - Model registry UI                                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Tracking Server

**Storage Options:**

```python
import mlflow

# Local file system (development)
mlflow.set_tracking_uri("file:///path/to/mlruns")

# Remote server (production)
mlflow.set_tracking_uri("http://mlflow-server:5000")

# Database backend
mlflow.set_tracking_uri("postgresql://user:pass@host:5432/mlflow")

# Databricks
mlflow.set_tracking_uri("databricks")
```

**Run Management:**

```python
# Start a run
with mlflow.start_run(run_name="experiment_1"):
    # Log parameters
    mlflow.log_param("model", "gpt-4")
    mlflow.log_param("temperature", 0.7)

    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("latency", 1.2)

    # Log artifacts
    mlflow.log_artifact("model_output.txt")
    mlflow.log_dict(config, "config.json")
```

#### 2. MLflow Evaluate for LLMs

**Built-in Evaluators:**

```python
import mlflow

# Evaluate LLM
results = mlflow.evaluate(
    model="openai:/gpt-4",
    data=eval_data,
    model_type="text",
    evaluators=["toxicity", "flesch_kincaid"],
)

# LLM-as-judge evaluation
results = mlflow.evaluate(
    model=my_model,
    data=eval_data,
    evaluators=[
        "relevance",  # Uses LLM to judge relevance
        "groundedness",  # Checks groundedness in context
        "answer_correctness"  # Evaluates answer quality
    ]
)
```

#### 3. Model Registry

**Model Registration:**

```python
# Log model
with mlflow.start_run():
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=my_llm_model,
        registered_model_name="MyLLMApp"
    )

# Register existing model
model_uri = "runs:/run_id/model"
mlflow.register_model(
    model_uri=model_uri,
    name="MyLLMApp"
)

# Transition model stage
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="MyLLMApp",
    version=1,
    stage="Production"
)
```

#### 4. Experiments

**Experiment Organization:**

```python
# Create experiment
experiment_id = mlflow.create_experiment(
    name="LLM_Prompt_Optimization",
    artifact_location="s3://my-bucket/mlflow",
    tags={"team": "ml", "project": "chatbot"}
)

# Set active experiment
mlflow.set_experiment("LLM_Prompt_Optimization")

# Get experiment info
experiment = mlflow.get_experiment(experiment_id)
print(f"Name: {experiment.name}")
print(f"Artifact Location: {experiment.artifact_location}")
```

---

## Installation and Setup

### Installation

**Basic Installation:**
```bash
pip install mlflow
```

**With Extras:**
```bash
# With database support
pip install mlflow[sqlserver,postgresql]

# With cloud storage
pip install mlflow[s3,azure,gcs]

# With LLM extras
pip install mlflow[genai]

# Full installation
pip install mlflow[extras]
```

**Start Tracking Server:**
```bash
# Local with SQLite
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5000

# With PostgreSQL
mlflow server \
  --backend-store-uri postgresql://user:pass@localhost/mlflow \
  --default-artifact-root s3://my-bucket/mlflow \
  --host 0.0.0.0
```

### Environment Setup

**.env Configuration:**
```bash
# Tracking
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=default

# Storage
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
MLFLOW_S3_ENDPOINT_URL=https://s3.amazonaws.com

# Database
MLFLOW_BACKEND_STORE_URI=postgresql://user:pass@localhost/mlflow

# LLM Provider Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Project Structure

**MLproject File:**
```yaml
name: llm_evaluation

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      model: {type: string, default: "gpt-3.5-turbo"}
      temperature: {type: float, default: 0.7}
      dataset: {type: string, default: "eval_data.json"}
    command: "python evaluate.py --model {model} --temperature {temperature} --dataset {dataset}"

  evaluate:
    parameters:
      model_uri: {type: string}
      dataset: {type: string}
    command: "python evaluate_model.py --model-uri {model_uri} --dataset {dataset}"
```

### Verification

**Test Installation:**
```python
import mlflow

print(f"MLflow version: {mlflow.__version__}")

# Test tracking
mlflow.set_tracking_uri("http://localhost:5000")

with mlflow.start_run():
    mlflow.log_param("test", "value")
    mlflow.log_metric("metric", 1.0)

print("MLflow setup successful!")
```

---

## Core Concepts

### 1. Runs and Experiments

**Creating Runs:**

```python
import mlflow
import time

# Simple run
with mlflow.start_run():
    mlflow.log_param("model", "gpt-4")
    mlflow.log_metric("score", 0.95)

# Nested runs
with mlflow.start_run(run_name="parent_run"):
    mlflow.log_param("experiment_type", "ablation")

    for i in range(3):
        with mlflow.start_run(run_name=f"child_run_{i}", nested=True):
            mlflow.log_param("variant", i)
            mlflow.log_metric("accuracy", 0.9 + i * 0.01)

# Resume existing run
run_id = "existing_run_id"
with mlflow.start_run(run_id=run_id):
    mlflow.log_metric("additional_metric", 0.88)
```

**Experiment Management:**

```python
# Create with tags
experiment_id = mlflow.create_experiment(
    name="Prompt_Engineering_v2",
    tags={
        "version": "2.0",
        "team": "ml-research",
        "priority": "high"
    }
)

# Set experiment
mlflow.set_experiment("Prompt_Engineering_v2")

# Get all experiments
experiments = mlflow.search_experiments()
for exp in experiments:
    print(f"{exp.name}: {exp.experiment_id}")

# Search runs in experiment
runs = mlflow.search_runs(
    experiment_ids=[experiment_id],
    filter_string="metrics.accuracy > 0.9",
    order_by=["metrics.accuracy DESC"]
)
```

### 2. Logging

**Parameter Logging:**

```python
# Log single parameter
mlflow.log_param("learning_rate", 0.001)

# Log multiple parameters
mlflow.log_params({
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 0.9
})

# Log nested parameters
mlflow.log_param("model.type", "gpt-4")
mlflow.log_param("model.provider", "openai")
```

**Metric Logging:**

```python
# Log single metric
mlflow.log_metric("accuracy", 0.95)

# Log multiple metrics
mlflow.log_metrics({
    "accuracy": 0.95,
    "precision": 0.93,
    "recall": 0.96,
    "f1": 0.945
})

# Log metric over time (for training curves)
for epoch in range(100):
    loss = train_epoch()
    mlflow.log_metric("loss", loss, step=epoch)

# Log with timestamp
mlflow.log_metric("latency", 1.2, step=0, timestamp=int(time.time() * 1000))
```

**Artifact Logging:**

```python
# Log file
mlflow.log_artifact("model_output.txt")

# Log directory
mlflow.log_artifacts("outputs/")

# Log dict as JSON
mlflow.log_dict({"config": "value"}, "config.json")

# Log text
mlflow.log_text("Generated response...", "response.txt")

# Log figure
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
mlflow.log_figure(fig, "plot.png")

# Log model
mlflow.pyfunc.log_model("model", python_model=my_model)
```

### 3. Model Management

**Logging Models:**

```python
import mlflow.pyfunc

class LLMWrapper(mlflow.pyfunc.PythonModel):
    """Custom LLM wrapper"""

    def load_context(self, context):
        """Load model dependencies"""
        import openai
        self.client = openai.OpenAI()

    def predict(self, context, model_input):
        """Generate predictions"""
        prompts = model_input["prompt"]
        responses = []

        for prompt in prompts:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            responses.append(response.choices[0].message.content)

        return responses

# Log model
with mlflow.start_run():
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=LLMWrapper(),
        pip_requirements=["openai>=1.0.0"],
        signature=mlflow.models.infer_signature(
            {"prompt": ["test"]},
            ["response"]
        )
    )
```

**Model Registry:**

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model
model_uri = "runs:/run_id/model"
model_details = mlflow.register_model(
    model_uri=model_uri,
    name="LLMChatbot"
)

# Update model description
client.update_registered_model(
    name="LLMChatbot",
    description="Production chatbot model using GPT-4"
)

# Create new version
client.create_model_version(
    name="LLMChatbot",
    source=model_uri,
    run_id=run_id
)

# Transition stage
client.transition_model_version_stage(
    name="LLMChatbot",
    version=2,
    stage="Production",
    archive_existing_versions=True
)

# Add tags
client.set_model_version_tag(
    name="LLMChatbot",
    version=2,
    key="validation_status",
    value="passed"
)

# Get latest version
latest_version = client.get_latest_versions("LLMChatbot", stages=["Production"])[0]
```

### 4. LLM Evaluation

**Built-in Evaluators:**

```python
import mlflow
import pandas as pd

# Prepare evaluation data
eval_data = pd.DataFrame({
    "inputs": ["What is AI?", "Explain ML"],
    "ground_truth": ["AI is artificial intelligence", "ML is machine learning"]
})

# Define model
def model(inputs):
    # Your model prediction logic
    return predictions

# Evaluate
results = mlflow.evaluate(
    model=model,
    data=eval_data,
    model_type="text",
    evaluators=[
        "exact_match",
        "toxicity",
        "flesch_kincaid_grade_level",
        "ari_grade_level"
    ],
    evaluator_config={
        "col_mapping": {
            "inputs": "inputs",
            "targets": "ground_truth"
        }
    }
)

print(results.metrics)
print(results.tables)
```

**LLM-as-Judge:**

```python
# Use LLM to evaluate responses
results = mlflow.evaluate(
    model=my_model,
    data=eval_data,
    model_type="text",
    evaluators=[
        mlflow.metrics.genai.relevance(),
        mlflow.metrics.genai.faithfulness(),
        mlflow.metrics.genai.answer_correctness()
    ]
)
```

### 5. Custom Metrics

**Define Custom Metrics:**

```python
from mlflow.metrics import make_metric

def custom_metric_fn(predictions, targets, metrics):
    """Custom metric function"""
    scores = []
    for pred, target in zip(predictions, targets):
        # Custom scoring logic
        score = calculate_score(pred, target)
        scores.append(score)
    return {"score": sum(scores) / len(scores)}

# Create metric
custom_metric = make_metric(
    eval_fn=custom_metric_fn,
    greater_is_better=True,
    name="custom_score"
)

# Use in evaluation
results = mlflow.evaluate(
    model=model,
    data=eval_data,
    extra_metrics=[custom_metric]
)
```

---

## Production-Ready Examples

### Example 1: Complete LLM Experiment Tracking

**Scenario:** Track prompt engineering experiments

```python
"""
Complete MLflow experiment tracking for LLM applications
- Prompt versioning
- Parameter tracking
- Cost monitoring
- Performance metrics
"""

import mlflow
import openai
from typing import Dict, List
import time
import json

class LLMExperimentTracker:
    """Track LLM experiments with MLflow"""

    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name

        # Set up MLflow
        mlflow.set_tracking_uri("http://localhost:5000")
        mlflow.set_experiment(experiment_name)

        # OpenAI client
        self.client = openai.OpenAI()

    def run_experiment(
        self,
        prompts: List[str],
        test_inputs: List[str],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict:
        """Run complete experiment"""

        with mlflow.start_run(run_name=f"{model}_temp{temperature}"):
            # Log parameters
            mlflow.log_params({
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "num_prompts": len(prompts),
                "num_test_inputs": len(test_inputs)
            })

            # Log prompts
            for i, prompt in enumerate(prompts):
                mlflow.log_text(prompt, f"prompts/prompt_{i}.txt")

            results = []
            total_cost = 0
            total_latency = 0

            # Test each prompt
            for prompt_idx, prompt in enumerate(prompts):
                prompt_results = []

                for input_idx, test_input in enumerate(test_inputs):
                    # Run inference
                    start_time = time.time()

                    try:
                        response = self.client.chat.completions.create(
                            model=model,
                            messages=[
                                {"role": "system", "content": prompt},
                                {"role": "user", "content": test_input}
                            ],
                            temperature=temperature,
                            max_tokens=max_tokens
                        )

                        latency = time.time() - start_time

                        # Extract results
                        output = response.choices[0].message.content
                        tokens_used = response.usage.total_tokens

                        # Calculate cost (approximate)
                        cost = self._calculate_cost(model, tokens_used)

                        total_cost += cost
                        total_latency += latency

                        result = {
                            "prompt_idx": prompt_idx,
                            "input_idx": input_idx,
                            "input": test_input,
                            "output": output,
                            "latency": latency,
                            "tokens": tokens_used,
                            "cost": cost
                        }

                        prompt_results.append(result)

                        # Log per-inference metrics
                        mlflow.log_metric(
                            f"prompt_{prompt_idx}_latency",
                            latency,
                            step=input_idx
                        )

                    except Exception as e:
                        print(f"Error: {e}")
                        continue

                results.extend(prompt_results)

                # Log prompt-level metrics
                avg_latency = sum(r["latency"] for r in prompt_results) / len(prompt_results)
                mlflow.log_metric(f"prompt_{prompt_idx}_avg_latency", avg_latency)

            # Log aggregate metrics
            mlflow.log_metrics({
                "total_cost": total_cost,
                "avg_latency": total_latency / len(results),
                "total_tokens": sum(r["tokens"] for r in results),
                "cost_per_request": total_cost / len(results)
            })

            # Save detailed results
            mlflow.log_dict(
                {"results": results},
                "detailed_results.json"
            )

            # Evaluate quality metrics
            quality_metrics = self._evaluate_quality(results)
            mlflow.log_metrics(quality_metrics)

            return {
                "results": results,
                "metrics": {
                    "total_cost": total_cost,
                    "avg_latency": total_latency / len(results),
                    **quality_metrics
                }
            }

    def _calculate_cost(self, model: str, tokens: int) -> float:
        """Calculate cost based on model and tokens"""
        # Approximate pricing (as of 2024)
        pricing = {
            "gpt-4": {
                "input": 0.03 / 1000,
                "output": 0.06 / 1000
            },
            "gpt-3.5-turbo": {
                "input": 0.0015 / 1000,
                "output": 0.002 / 1000
            }
        }

        if model in pricing:
            # Simplified: assume 50/50 split
            avg_price = (pricing[model]["input"] + pricing[model]["output"]) / 2
            return tokens * avg_price

        return 0.0

    def _evaluate_quality(self, results: List[Dict]) -> Dict:
        """Evaluate quality metrics"""
        metrics = {}

        # Average output length
        avg_length = sum(len(r["output"]) for r in results) / len(results)
        metrics["avg_output_length"] = avg_length

        # Response time consistency
        latencies = [r["latency"] for r in results]
        metrics["latency_std"] = sum((l - sum(latencies)/len(latencies))**2 for l in latencies) ** 0.5 / len(latencies)

        return metrics

    def compare_experiments(self, run_ids: List[str]) -> Dict:
        """Compare multiple experiments"""
        from mlflow.tracking import MlflowClient

        client = MlflowClient()
        comparison = {}

        for run_id in run_ids:
            run = client.get_run(run_id)

            comparison[run_id] = {
                "params": run.data.params,
                "metrics": run.data.metrics,
                "start_time": run.info.start_time,
                "end_time": run.info.end_time
            }

        return comparison

# ============================================================================
# USAGE EXAMPLE
# ============================================================================

def main():
    """Main execution"""

    # Initialize tracker
    tracker = LLMExperimentTracker("Prompt_Engineering_Experiments")

    # Define prompts to test
    prompts = [
        "You are a helpful assistant. Answer concisely.",
        "You are an expert assistant. Provide detailed, accurate answers.",
        "You are a friendly assistant. Answer in a conversational tone."
    ]

    # Test inputs
    test_inputs = [
        "What is machine learning?",
        "Explain neural networks",
        "How does backpropagation work?"
    ]

    # Run experiments with different configurations
    configs = [
        {"model": "gpt-4", "temperature": 0.0},
        {"model": "gpt-4", "temperature": 0.7},
        {"model": "gpt-3.5-turbo", "temperature": 0.7}
    ]

    run_ids = []

    for config in configs:
        print(f"\nRunning experiment: {config}")

        results = tracker.run_experiment(
            prompts=prompts,
            test_inputs=test_inputs,
            **config
        )

        run = mlflow.active_run()
        run_ids.append(run.info.run_id)

        print(f"Run ID: {run.info.run_id}")
        print(f"Total Cost: ${results['metrics']['total_cost']:.4f}")
        print(f"Avg Latency: {results['metrics']['avg_latency']:.2f}s")

    # Compare experiments
    print("\n" + "="*80)
    print("EXPERIMENT COMPARISON")
    print("="*80)

    comparison = tracker.compare_experiments(run_ids)

    for run_id, data in comparison.items():
        print(f"\nRun: {run_id}")
        print(f"  Model: {data['params']['model']}")
        print(f"  Temperature: {data['params']['temperature']}")
        print(f"  Total Cost: ${data['metrics']['total_cost']:.4f}")
        print(f"  Avg Latency: {data['metrics']['avg_latency']:.2f}s")

if __name__ == "__main__":
    main()
```

### Example 2: RAG System Evaluation with MLflow

**Scenario:** Comprehensive RAG evaluation

```python
"""
RAG system evaluation with MLflow
- Retrieval metrics
- Generation metrics
- End-to-end evaluation
"""

import mlflow
import pandas as pd
from typing import List, Dict
import numpy as np

class RAGEvaluator:
    """Evaluate RAG systems with MLflow"""

    def __init__(self, experiment_name: str):
        mlflow.set_experiment(experiment_name)

    def evaluate_rag(
        self,
        rag_system,
        eval_dataset: pd.DataFrame,
        run_name: str = "rag_evaluation"
    ) -> Dict:
        """Comprehensive RAG evaluation"""

        with mlflow.start_run(run_name=run_name):
            # Log system configuration
            config = rag_system.get_config()
            mlflow.log_params(config)

            results = []

            for idx, row in eval_dataset.iterrows():
                query = row["query"]
                expected_answer = row["expected_answer"]
                expected_context = row.get("expected_context", None)

                # Run RAG
                start_time = mlflow.utils.time.time()

                rag_output = rag_system.query(query)

                latency = mlflow.utils.time.time() - start_time

                # Extract components
                retrieved_docs = rag_output["retrieved_documents"]
                generated_answer = rag_output["answer"]
                metadata = rag_output.get("metadata", {})

                # Evaluate retrieval
                retrieval_metrics = self._evaluate_retrieval(
                    query=query,
                    retrieved_docs=retrieved_docs,
                    expected_context=expected_context
                )

                # Evaluate generation
                generation_metrics = self._evaluate_generation(
                    query=query,
                    answer=generated_answer,
                    expected_answer=expected_answer,
                    context=retrieved_docs
                )

                # Combined result
                result = {
                    "query_idx": idx,
                    "query": query,
                    "answer": generated_answer,
                    "latency": latency,
                    "num_retrieved": len(retrieved_docs),
                    **retrieval_metrics,
                    **generation_metrics
                }

                results.append(result)

                # Log per-query metrics
                for metric, value in result.items():
                    if isinstance(value, (int, float)):
                        mlflow.log_metric(f"query_{idx}_{metric}", value)

            # Calculate aggregate metrics
            aggregate_metrics = self._calculate_aggregate_metrics(results)
            mlflow.log_metrics(aggregate_metrics)

            # Log detailed results
            results_df = pd.DataFrame(results)
            mlflow.log_table(results_df, "evaluation_results.json")

            # Generate visualizations
            self._generate_visualizations(results_df)

            return {
                "results": results,
                "aggregate_metrics": aggregate_metrics
            }

    def _evaluate_retrieval(
        self,
        query: str,
        retrieved_docs: List[str],
        expected_context: str = None
    ) -> Dict:
        """Evaluate retrieval quality"""

        metrics = {}

        # Number of documents retrieved
        metrics["num_retrieved"] = len(retrieved_docs)

        # Average document length
        metrics["avg_doc_length"] = np.mean([len(doc) for doc in retrieved_docs])

        # Diversity (unique starts)
        if len(retrieved_docs) > 1:
            unique_starts = len(set(doc[:100] for doc in retrieved_docs))
            metrics["retrieval_diversity"] = unique_starts / len(retrieved_docs)
        else:
            metrics["retrieval_diversity"] = 1.0

        # Relevance to query (simple overlap)
        query_words = set(query.lower().split())
        relevance_scores = []

        for doc in retrieved_docs:
            doc_words = set(doc.lower().split())
            overlap = len(query_words & doc_words)
            relevance_scores.append(overlap / len(query_words) if query_words else 0)

        metrics["avg_retrieval_relevance"] = np.mean(relevance_scores) if relevance_scores else 0

        # Context match (if expected context provided)
        if expected_context:
            best_match = max(
                self._calculate_overlap(expected_context, doc)
                for doc in retrieved_docs
            ) if retrieved_docs else 0

            metrics["context_match_score"] = best_match

        return metrics

    def _evaluate_generation(
        self,
        query: str,
        answer: str,
        expected_answer: str,
        context: List[str]
    ) -> Dict:
        """Evaluate generation quality"""

        metrics = {}

        # Answer length
        metrics["answer_length"] = len(answer)

        # Similarity to expected (simple overlap)
        metrics["answer_similarity"] = self._calculate_overlap(
            expected_answer,
            answer
        )

        # Groundedness (answer supported by context)
        combined_context = " ".join(context)
        metrics["groundedness"] = self._calculate_overlap(
            answer,
            combined_context
        )

        # Query relevance
        metrics["query_relevance"] = self._calculate_overlap(
            query,
            answer
        )

        return metrics

    def _calculate_overlap(self, text1: str, text2: str) -> float:
        """Calculate word overlap between texts"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        overlap = len(words1 & words2)
        return overlap / max(len(words1), len(words2))

    def _calculate_aggregate_metrics(self, results: List[Dict]) -> Dict:
        """Calculate aggregate metrics"""

        metrics = {}

        # Numeric metrics
        numeric_fields = [
            "latency",
            "num_retrieved",
            "retrieval_diversity",
            "avg_retrieval_relevance",
            "answer_length",
            "answer_similarity",
            "groundedness",
            "query_relevance"
        ]

        for field in numeric_fields:
            values = [r[field] for r in results if field in r]
            if values:
                metrics[f"avg_{field}"] = np.mean(values)
                metrics[f"std_{field}"] = np.std(values)
                metrics[f"min_{field}"] = np.min(values)
                metrics[f"max_{field}"] = np.max(values)

        return metrics

    def _generate_visualizations(self, results_df: pd.DataFrame):
        """Generate and log visualizations"""

        import matplotlib.pyplot as plt

        # Latency distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(results_df["latency"], bins=20)
        ax.set_xlabel("Latency (s)")
        ax.set_ylabel("Count")
        ax.set_title("Query Latency Distribution")
        mlflow.log_figure(fig, "latency_distribution.png")
        plt.close()

        # Metrics scatter
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        axes[0, 0].scatter(results_df["num_retrieved"], results_df["answer_similarity"])
        axes[0, 0].set_xlabel("Num Retrieved")
        axes[0, 0].set_ylabel("Answer Similarity")

        axes[0, 1].scatter(results_df["groundedness"], results_df["answer_similarity"])
        axes[0, 1].set_xlabel("Groundedness")
        axes[0, 1].set_ylabel("Answer Similarity")

        axes[1, 0].scatter(results_df["retrieval_diversity"], results_df["groundedness"])
        axes[1, 0].set_xlabel("Retrieval Diversity")
        axes[1, 0].set_ylabel("Groundedness")

        axes[1, 1].scatter(results_df["latency"], results_df["answer_similarity"])
        axes[1, 1].set_xlabel("Latency")
        axes[1, 1].set_ylabel("Answer Similarity")

        plt.tight_layout()
        mlflow.log_figure(fig, "metrics_scatter.png")
        plt.close()

# ============================================================================
# USAGE EXAMPLE
# ============================================================================

class SimpleRAG:
    """Simple RAG system for testing"""

    def __init__(self, retriever, generator):
        self.retriever = retriever
        self.generator = generator

    def query(self, query: str) -> Dict:
        """Process RAG query"""
        # Retrieve
        docs = self.retriever.retrieve(query, top_k=5)

        # Generate
        context = "\n".join(docs)
        answer = self.generator.generate(query, context)

        return {
            "retrieved_documents": docs,
            "answer": answer,
            "metadata": {}
        }

    def get_config(self) -> Dict:
        """Get configuration"""
        return {
            "retriever_type": "simple",
            "generator_model": "gpt-4",
            "top_k": 5
        }

def main():
    """Main execution"""

    # Create evaluation dataset
    eval_data = pd.DataFrame({
        "query": [
            "What is machine learning?",
            "Explain neural networks",
            "How does backpropagation work?"
        ],
        "expected_answer": [
            "Machine learning is a subset of AI",
            "Neural networks are computational models",
            "Backpropagation is an algorithm for training"
        ]
    })

    # Create RAG system (mocked for example)
    class MockRetriever:
        def retrieve(self, query, top_k=5):
            return [f"Document {i} about {query}" for i in range(top_k)]

    class MockGenerator:
        def generate(self, query, context):
            return f"Answer to {query} based on context"

    rag_system = SimpleRAG(MockRetriever(), MockGenerator())

    # Evaluate
    evaluator = RAGEvaluator("RAG_Evaluation")
    results = evaluator.evaluate_rag(
        rag_system=rag_system,
        eval_dataset=eval_data,
        run_name="rag_baseline"
    )

    print("\nEvaluation Results:")
    print(f"Average Latency: {results['aggregate_metrics']['avg_latency']:.2f}s")
    print(f"Average Answer Similarity: {results['aggregate_metrics']['avg_answer_similarity']:.2f}")
    print(f"Average Groundedness: {results['aggregate_metrics']['avg_groundedness']:.2f}")

if __name__ == "__main__":
    main()
```

(Due to length, continuing in next part...)
