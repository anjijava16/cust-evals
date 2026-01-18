# MLflow: ML Lifecycle Management with LLM Evaluation

**Type**: ML Platform + Experiment Tracking | **License**: Apache 2.0 (Open Source) | **Year**: 2018

---

## Quick Overview

MLflow is a **comprehensive ML lifecycle platform** that includes experiment tracking, model management, and deployment. Starting with v2.8.0, MLflow added native LLM evaluation capabilities, making it a unified solution for traditional ML and LLM workflows.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | ML lifecycle, experiment tracking |
| **Setup Time** | ⚡ 15-25 minutes |
| **Learning Curve** | Moderate to Steep |
| **Dependencies** | MLflow server, storage backend |
| **Cost** | Free (OSS) + Databricks option |
| **Best For** | ML teams, experiment tracking |

---

## Key Strengths

### ✅ Advantages

1. **Complete ML Lifecycle**
   - Experiment tracking
   - Model registry
   - Model serving
   - Artifact storage
   - Version control
   - A/B testing support

2. **LLM-Native Features (v2.8+)**
   - Prompt engineering tracking
   - LLM evaluation metrics
   - Model comparison
   - Token usage tracking
   - Latency monitoring
   - Cost tracking

3. **Experiment Tracking**
   - Track all experiments
   - Compare runs easily
   - Reproduce experiments
   - Share results with team
   - Automatic logging
   - Rich UI dashboard

4. **Model Registry**
   - Centralized model storage
   - Version management
   - Stage transitions (staging/prod)
   - Model lineage
   - Approval workflows
   - Metadata tracking

5. **Enterprise Ready**
   - Scales to large teams
   - Multi-user support
   - Authentication & authorization
   - Audit logging
   - Integration with Databricks
   - Production deployment

6. **Multi-Framework Support**
   - Traditional ML (sklearn, XGBoost)
   - Deep Learning (PyTorch, TensorFlow)
   - LLMs (OpenAI, HuggingFace)
   - LangChain integration
   - Custom models

### ⚠️ Limitations

1. **LLM Features Newer**
   - LLM support added recently (2023)
   - Less mature than core features
   - Documentation still evolving
   - Fewer LLM-specific examples

2. **Complex Setup**
   - Server infrastructure required
   - Storage backend needed (S3, etc.)
   - Database for metadata
   - More moving parts
   - Steeper learning curve

3. **Heavy Infrastructure**
   - Not lightweight
   - Resource intensive
   - Overkill for simple projects
   - More ops overhead

4. **Limited RAG Evaluation**
   - Basic RAG metrics
   - Not as comprehensive as RAGAS/TruLens
   - More focused on general LLM eval
   - Less retrieval-specific features

5. **UI-Centric**
   - Less programmatic API
   - More click-through workflows
   - Better for interactive use
   - CI/CD integration more complex

6. **Learning Curve**
   - Many concepts to learn
   - Experiment tracking paradigm
   - Model registry concepts
   - Takes time to master

---

## vs Other Frameworks

### vs Custom-Evals
| Aspect | MLflow | Custom-Evals |
|--------|--------|--------------|
| **Scope** | Full ML lifecycle | Evaluation only |
| **Infrastructure** | Server required | None |
| **Experiment Tracking** | Excellent | Manual |
| **Setup Complexity** | High | Low |
| **Flexibility** | Medium | High |
| **Use Case** | Enterprise ML | Lightweight eval |

**Choose MLflow if**: You need full ML lifecycle management
**Choose Custom-Evals if**: You just need evaluation without overhead

---

### vs Phoenix
| Aspect | MLflow | Phoenix |
|--------|--------|---------|
| **Primary Focus** | ML lifecycle | Observability |
| **LLM Maturity** | Growing | Mature |
| **OTEL Support** | Limited | Native |
| **Experiment Tracking** | Excellent | Basic |
| **Model Registry** | Yes | No |
| **Learning Curve** | Steeper | Moderate |

**Choose MLflow if**: You need experiment tracking + model management
**Choose Phoenix if**: You want LLM-focused observability

---

### vs LangSmith
| Aspect | MLflow | LangSmith |
|--------|--------|-----------|
| **Open Source** | ✅ Yes | ❌ No |
| **ML Support** | Traditional + LLM | LLM only |
| **Model Registry** | Yes | No |
| **LangChain Integration** | Good | Native |
| **Cost** | Free (self-host) | Paid |
| **Maturity** | Very mature | Growing |

**Choose MLflow if**: You need traditional ML + LLM in one platform
**Choose LangSmith if**: LangChain-focused with managed service

---

### vs Weights & Biases
| Aspect | MLflow | W&B |
|--------|--------|-----|
| **Open Source** | ✅ Yes | ❌ No (client only) |
| **Self-Hosting** | Easy | Difficult |
| **UI Quality** | Good | Excellent |
| **LLM Features** | Growing | Mature |
| **Cost** | Free | Free tier + paid |
| **Enterprise** | Good | Excellent |

**Choose MLflow if**: Want OSS and self-hosting
**Choose W&B if**: Want best-in-class UI and don't mind cost

---

## When to Choose MLflow

### ✅ Perfect For

1. **Enterprise ML Teams**
   - Multiple ML projects
   - Team collaboration
   - Model governance
   - Centralized tracking
   - Production deployment

2. **Experiment-Heavy Workflows**
   - Many experiments to track
   - Compare multiple approaches
   - Hyperparameter tuning
   - Systematic optimization
   - Reproducibility critical

3. **Model Lifecycle Management**
   - Model versioning needed
   - Stage management (dev/staging/prod)
   - Approval workflows
   - Model lineage tracking
   - Deployment automation

4. **Traditional ML + LLM**
   - Both ML and LLM projects
   - Unified platform desired
   - Consistent workflows
   - Shared infrastructure

5. **Databricks Users**
   - Already using Databricks
   - Native integration
   - Managed MLflow
   - Enterprise support

6. **LLM Prompt Engineering**
   - Track prompt variations
   - Compare prompt performance
   - Version prompts
   - Share best prompts
   - Systematic optimization

### ❌ Not Ideal For

1. **Simple Projects**
   - Single model/experiment
   - No team collaboration
   - Overhead not justified
   - Prefer lightweight

2. **Pure LLM Observability**
   - Need real-time tracing
   - Deep observability focus
   - Phoenix/TruLens better suited

3. **Quick Prototyping**
   - Want fast iteration
   - Minimal setup time
   - Exploration phase
   - No tracking needed yet

4. **RAG-Specific Evaluation**
   - Deep RAG metrics needed
   - RAGAS/TruLens more specialized
   - MLflow RAG support basic

5. **Minimal Infrastructure**
   - Can't run server
   - No storage backend
   - Want zero setup
   - Prefer code-only

---

## Pricing

### Cost Breakdown

| Component | Self-Hosted | Databricks (Managed) |
|-----------|-------------|----------------------|
| **MLflow Software** | 💰 **Free** | Included |
| **Tracking Server** | Your compute | Included |
| **Artifact Storage** | Your storage (S3/Azure) | Included |
| **Database** | Your DB (Postgres/MySQL) | Included |
| **Support** | Community | Enterprise |
| **Advanced Features** | OSS features | Enterprise features |

### Self-Hosted Monthly Costs

| Scale | Storage | Compute | Database | Est. Total |
|-------|---------|---------|----------|------------|
| **Small Team** (1-5 users) | $10-20 | $20-50 | $10-20 | $40-90 |
| **Medium Team** (5-20 users) | $50-100 | $100-200 | $50-100 | $200-400 |
| **Large Team** (20+ users) | $200-500 | $500-1000 | $200-500 | $900-2000 |

### Databricks Managed MLflow

Included with Databricks subscription:
- **Standard**: Included in workspace
- **Premium**: + advanced features
- **Enterprise**: + advanced governance

Contact Databricks for pricing

### Artifact Storage Costs

- **S3**: $0.023 per GB/month
- **Azure Blob**: $0.018 per GB/month
- **GCS**: $0.020 per GB/month

**Typical usage**: 10-100 GB for small/medium teams

---

## Quick Start

### Installation

```bash
# Install MLflow
pip install mlflow

# With LLM evaluation
pip install mlflow[llm]

# Full installation
pip install mlflow[extras]
```

### Start MLflow Server

```bash
# Simple local server
mlflow server --host 0.0.0.0 --port 5000

# With backend storage
mlflow server \
  --backend-store-uri postgresql://user:pass@localhost/mlflow \
  --default-artifact-root s3://my-mlflow-bucket/ \
  --host 0.0.0.0 \
  --port 5000
```

Access UI at: http://localhost:5000

### Basic Experiment Tracking

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

# Set tracking URI
mlflow.set_tracking_uri("http://localhost:5000")

# Create/set experiment
mlflow.set_experiment("my-experiment")

# Start run
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)

    # Train model
    model = RandomForestClassifier(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)

    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)

    # Log model
    mlflow.sklearn.log_model(model, "model")
```

### LLM Evaluation

```python
import mlflow
from mlflow.metrics.genai import answer_relevance, faithfulness

# Set experiment
mlflow.set_experiment("llm-evaluation")

# Define your LLM function
def my_llm(inputs):
    import openai
    client = openai.OpenAI()

    responses = []
    for input_text in inputs["questions"]:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": input_text}]
        )
        responses.append(response.choices[0].message.content)

    return responses

# Create evaluation dataset
eval_data = {
    "questions": [
        "What is MLflow?",
        "How does MLflow track experiments?",
        "What is a model registry?"
    ],
    "ground_truth": [
        "MLflow is an open-source platform for managing ML lifecycle...",
        "MLflow tracks experiments by logging parameters, metrics, and artifacts...",
        "A model registry is a centralized repository for storing ML models..."
    ]
}

# Evaluate
with mlflow.start_run():
    results = mlflow.evaluate(
        model=my_llm,
        data=eval_data,
        targets="ground_truth",
        model_type="question-answering",
        evaluators="default",
        extra_metrics=[
            answer_relevance,
            faithfulness
        ]
    )

    print(results.metrics)
    print(results.tables)
```

### LLM as Judge

```python
import mlflow

# Custom LLM-as-judge metric
from mlflow.metrics.genai import make_genai_metric

# Define evaluation prompt
judge_prompt = """
Evaluate the quality of the response.

Question: {input}
Response: {output}
Ground Truth: {ground_truth}

Rate the response on a scale of 1-5 for accuracy.
Output only the number.
"""

# Create custom metric
accuracy_metric = make_genai_metric(
    name="accuracy",
    definition="Accuracy of response compared to ground truth",
    grading_prompt=judge_prompt,
    model="openai:/gpt-4",
    grading_context_columns=["ground_truth"],
    parameters={"temperature": 0.0},
    aggregations=["mean", "std"],
    greater_is_better=True
)

# Use in evaluation
with mlflow.start_run():
    results = mlflow.evaluate(
        model=my_llm,
        data=eval_data,
        model_type="text",
        extra_metrics=[accuracy_metric]
    )
```

---

## Architecture Highlights

### Core Components

```
MLflow Architecture:
┌─────────────────────────────────────┐
│   MLflow UI (React)                 │
│   - Experiment comparison           │
│   - Run details                     │
│   - Model registry                  │
│   - Artifact viewer                 │
└─────────────────────────────────────┘
              ↑
┌─────────────────────────────────────┐
│   MLflow Tracking Server            │
│   - REST API                        │
│   - Run management                  │
│   - Metric storage                  │
│   - Artifact routing                │
└─────────────────────────────────────┘
       ↑              ↑
┌────────────┐  ┌─────────────┐
│ Backend    │  │ Artifact    │
│ Store      │  │ Store       │
│ (DB)       │  │ (S3/Azure)  │
└────────────┘  └─────────────┘
       ↑
┌─────────────────────────────────────┐
│   MLflow Client (Python)            │
│   - mlflow.log_param()              │
│   - mlflow.log_metric()             │
│   - mlflow.log_model()              │
│   - mlflow.evaluate()               │
└─────────────────────────────────────┘
```

### Key Concepts

1. **Experiments**: Group related runs
2. **Runs**: Single execution with tracked metrics
3. **Parameters**: Input configurations
4. **Metrics**: Output measurements
5. **Artifacts**: Files (models, plots, data)
6. **Tags**: Metadata for organization
7. **Models**: Registered, versioned models

---

## Advanced Features

### 1. Model Registry

```python
import mlflow.pyfunc

# Train and log model
with mlflow.start_run():
    model = train_model()
    mlflow.sklearn.log_model(model, "model")

    # Register model
    run_id = mlflow.active_run().info.run_id
    model_uri = f"runs:/{run_id}/model"

    mlflow.register_model(
        model_uri=model_uri,
        name="my-llm-model"
    )

# Transition to staging
from mlflow.tracking import MlflowClient

client = MlflowClient()
client.transition_model_version_stage(
    name="my-llm-model",
    version=1,
    stage="Staging"
)

# Load model from registry
model = mlflow.pyfunc.load_model("models:/my-llm-model/Staging")
predictions = model.predict(data)
```

### 2. Prompt Tracking

```python
import mlflow

mlflow.set_experiment("prompt-engineering")

# Track different prompts
prompts = {
    "v1": "Answer this question: {question}",
    "v2": "You are a helpful assistant. Question: {question}",
    "v3": "Provide a detailed answer to: {question}"
}

for prompt_version, prompt_template in prompts.items():
    with mlflow.start_run(run_name=prompt_version):
        # Log prompt
        mlflow.log_param("prompt_template", prompt_template)

        # Evaluate
        responses = []
        for question in test_questions:
            prompt = prompt_template.format(question=question)
            response = llm.generate(prompt)
            responses.append(response)

        # Log metrics
        avg_length = sum(len(r) for r in responses) / len(responses)
        mlflow.log_metric("avg_response_length", avg_length)

        # Log sample responses
        mlflow.log_text("\n\n".join(responses), "sample_responses.txt")
```

### 3. A/B Testing

```python
import mlflow

# Track multiple model variants
models = {
    "gpt-3.5-turbo": lambda q: openai_call("gpt-3.5-turbo", q),
    "gpt-4": lambda q: openai_call("gpt-4", q),
    "claude-3": lambda q: anthropic_call("claude-3", q),
}

for model_name, model_fn in models.items():
    with mlflow.start_run(run_name=model_name):
        mlflow.log_param("model", model_name)

        # Evaluate
        results = mlflow.evaluate(
            model=model_fn,
            data=eval_data,
            model_type="text",
            evaluators="default"
        )

        # Compare in UI
        mlflow.log_metrics(results.metrics)
```

### 4. Cost Tracking

```python
import mlflow
from openai import OpenAI

client = OpenAI()

with mlflow.start_run():
    total_cost = 0
    total_tokens = 0

    for question in questions:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}]
        )

        # Track usage
        tokens = response.usage.total_tokens
        cost = tokens * 0.00003  # $0.03 per 1K tokens

        total_tokens += tokens
        total_cost += cost

    # Log aggregates
    mlflow.log_metric("total_tokens", total_tokens)
    mlflow.log_metric("total_cost", total_cost)
    mlflow.log_metric("avg_cost_per_query", total_cost / len(questions))
```

### 5. LangChain Integration

```python
import mlflow
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

mlflow.langchain.autolog()  # Auto-log LangChain runs

with mlflow.start_run():
    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate.from_template("Answer: {question}")
    chain = LLMChain(llm=llm, prompt=prompt)

    # Automatically logged!
    result = chain.run(question="What is MLflow?")

    # MLflow captures:
    # - Prompt template
    # - Model params (temperature, etc.)
    # - Input/output
    # - Latency
```

---

## LLM-Specific Features

### Built-in LLM Metrics

```python
from mlflow.metrics.genai import (
    answer_relevance,
    answer_similarity,
    answer_correctness,
    faithfulness,
    toxicity,
)

# Use in evaluation
results = mlflow.evaluate(
    model=my_llm,
    data=eval_data,
    model_type="question-answering",
    extra_metrics=[
        answer_relevance,      # How relevant is answer to question?
        answer_similarity,     # How similar to ground truth?
        answer_correctness,    # Is it correct?
        faithfulness,          # Is it faithful to context?
        toxicity,              # Is it toxic?
    ]
)
```

### Token Usage Tracking

```python
import mlflow

with mlflow.start_run():
    # Track token usage automatically
    mlflow.langchain.autolog()

    response = chain.run(query)

    # Or manually
    mlflow.log_metric("prompt_tokens", usage.prompt_tokens)
    mlflow.log_metric("completion_tokens", usage.completion_tokens)
    mlflow.log_metric("total_tokens", usage.total_tokens)
```

### Latency Monitoring

```python
import mlflow
import time

with mlflow.start_run():
    start = time.time()

    response = llm.generate(prompt)

    latency = time.time() - start
    mlflow.log_metric("latency_seconds", latency)
```

---

## Comparison Summary

### Unique Advantages
1. 🏗️ Complete ML lifecycle platform
2. 📊 Excellent experiment tracking
3. 📦 Model registry and versioning
4. 🚀 Production deployment support
5. 👥 Enterprise team collaboration
6. 🔓 Open source and mature

### Trade-offs
1. Heavy infrastructure
2. Steeper learning curve
3. LLM features newer
4. More setup complexity
5. Resource intensive
6. Overkill for simple projects

---

## Resources

### Documentation
- **Official Docs**: https://mlflow.org/docs/latest/index.html
- **LLM Features**: https://mlflow.org/docs/latest/llms/index.html
- **LLM Evaluation**: https://mlflow.org/docs/latest/llms/llm-evaluate/index.html
- **Model Registry**: https://mlflow.org/docs/latest/model-registry.html

### Tutorials
- **Quickstart**: https://mlflow.org/docs/latest/getting-started/index.html
- **LLM Tracking**: https://mlflow.org/docs/latest/llms/llm-tracking/index.html
- **Prompt Engineering**: https://mlflow.org/docs/latest/llms/prompt-engineering/index.html

### GitHub
- **MLflow Repository**: https://github.com/mlflow/mlflow
- **Examples**: https://github.com/mlflow/mlflow/tree/master/examples
- **LLM Examples**: https://github.com/mlflow/mlflow/tree/master/examples/llms

### Integrations
- **LangChain**: https://mlflow.org/docs/latest/llms/langchain/index.html
- **OpenAI**: https://mlflow.org/docs/latest/llms/openai/index.html
- **HuggingFace**: https://mlflow.org/docs/latest/models.html#huggingface-transformers

### Community
- **Slack**: https://mlflow.org/slack
- **Mailing List**: https://groups.google.com/forum/#!forum/mlflow-users
- **GitHub Issues**: https://github.com/mlflow/mlflow/issues

---

## Verdict

**MLflow is the best choice for ML teams needing comprehensive experiment tracking, model management, and unified traditional ML + LLM workflows.**

**Rating**: ⭐⭐⭐⭐½ (4.5/5 for enterprise ML)

### Choose MLflow if you value:
- ✅ Complete ML lifecycle management
- ✅ Experiment tracking
- ✅ Model registry
- ✅ Team collaboration
- ✅ Traditional ML + LLM
- ✅ Enterprise features

### Choose alternatives if you need:
- ❌ Lightweight evaluation only → Custom-Evals, RAGAS
- ❌ LLM-specific observability → Phoenix, TruLens
- ❌ Deep RAG metrics → TruLens, RAGAS
- ❌ Minimal setup → Custom-Evals
- ❌ Real-time tracing → Phoenix, LangSmith

---

**Next**: [Compare All Frameworks](Compare_All_Eval_Frameworks.md) | [Try Custom-Evals](01_Custom_Evals.md)
