# Weave: W&B's LLM Evaluation & Experiment Tracking

**Type**: Cloud Platform | **License**: Commercial (Freemium) | **Year**: 2023

---

## Quick Overview

Weave is **Weights & Biases' (W&B)** toolkit for tracking, evaluating, and versioning LLM applications. It brings W&B's proven experiment tracking methodology to the world of LLMs, with automatic versioning, evaluation pipelines, and seamless integration with the W&B ecosystem.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | Experiment tracking + evaluation + versioning |
| **Setup Time** | 10-15 minutes |
| **Learning Curve** | Easy (familiar to W&B users) |
| **Dependencies** | W&B account (cloud) |
| **Cost** | Free tier + Pro ($50/user) + Custom |
| **Best For** | Teams already using W&B, experiment tracking |

---

## Key Strengths

### ✅ Advantages

1. **Automatic Versioning**
   - Code, data, and configs versioned automatically
   - Every function call tracked and versioned
   - Model versions captured automatically
   - Dataset versions tracked
   - Reproducibility by default
   - No manual versioning needed

2. **Seamless W&B Integration**
   - Works with existing W&B projects
   - Unified dashboard with ML experiments
   - Shared infrastructure
   - Single login for all W&B tools
   - Leverages W&B's proven platform
   - Team collaboration features

3. **Experiment Tracking Excellence**
   - Compare multiple runs side-by-side
   - Hyperparameter tracking
   - Metric visualization
   - Performance trends
   - Historical comparison
   - Configuration diffing

4. **Simple Python-First API**
   - Decorator-based tracking (`@weave.op()`)
   - Minimal boilerplate
   - Pythonic design
   - Type hints support
   - Clean, intuitive API
   - Easy to learn

5. **Model Class Pattern**
   - Structured model definitions
   - Automatic version control
   - Prediction tracking
   - Configuration management
   - Reusable components
   - Clean architecture

6. **Dataset Management**
   - Versioned datasets
   - Reusable test sets
   - Dataset diffing
   - Programmatic creation
   - Version history
   - Easy sharing

7. **Evaluation Pipelines**
   - Custom evaluators
   - Batch evaluation
   - Multiple metrics simultaneously
   - Evaluation versioning
   - Result comparison
   - Statistical analysis

8. **Rich Visualization**
   - Interactive UI
   - Trace exploration
   - Comparison views
   - Performance charts
   - Distribution plots
   - Custom dashboards

### ⚠️ Limitations

1. **W&B Ecosystem Lock-in**
   - Requires W&B account
   - Cloud-dependent (no self-hosting)
   - Tied to W&B platform
   - Pricing tied to W&B

2. **Not Open Source**
   - Proprietary platform
   - No self-hosting option
   - Limited extensibility
   - Vendor dependency

3. **Cost Scaling**
   - Free tier limited
   - Per-user pricing can add up
   - Large teams = higher costs
   - Usage-based overages possible

4. **Limited LLM-Specific Features**
   - No built-in prompt management
   - Basic cost tracking
   - Less LLM-focused than alternatives
   - More general-purpose

5. **Learning Curve for Non-W&B Users**
   - Need to learn W&B ecosystem
   - Multiple concepts to understand
   - Not as lightweight as simple libraries

---

## vs Other Frameworks

### vs Langfuse

| Aspect | Weave | Langfuse |
|--------|-------|----------|
| **Open Source** | ❌ No | ✅ Yes (MIT) |
| **Self-Hosted** | ❌ No | ✅ Yes |
| **Automatic Versioning** | ✅ Excellent | ⚠️ Manual |
| **Cost Tracking** | Basic | Excellent |
| **Prompt Management** | ❌ None | ✅ Built-in |
| **W&B Integration** | ✅ Native | ❌ None |
| **Experiment Tracking** | Excellent | Good |
| **Free Tier** | Limited | 50K observations |
| **Pricing** | $50/user/month | $59/month (flat) |
| **Developer DX** | Excellent | Good |
| **Vendor Lock-in** | Yes (W&B) | No (can self-host) |

**Choose Weave if**: You use W&B, want automatic versioning, prioritize experiment tracking
**Choose Langfuse if**: You want open source, cost tracking, or self-hosting

---

### vs Braintrust

| Aspect | Weave | Braintrust |
|--------|-------|-----------|
| **Automatic Versioning** | ✅ Yes | ✅ Yes |
| **Developer DX** | Excellent | Best-in-class |
| **CI/CD Integration** | Good | Excellent |
| **Dataset Management** | Good | Excellent |
| **Experiment Tracking** | Excellent | Good |
| **W&B Integration** | ✅ Native | ❌ None |
| **Free Tier** | Limited | 10K evaluations |
| **Pricing (Paid)** | $50/user | $100/month |
| **Open Source** | ❌ No | ❌ No |
| **Best For** | W&B users, experiments | DX, CI/CD, evaluations |

**Choose Weave if**: You use W&B and prioritize experiment tracking
**Choose Braintrust if**: You want best DX and strong CI/CD integration

---

### vs LangSmith

| Aspect | Weave | LangSmith |
|--------|-------|-----------|
| **LangChain Focus** | ❌ Framework-agnostic | ✅ LangChain-first |
| **Automatic Versioning** | ✅ Yes | ⚠️ Manual |
| **Observability** | Good | Excellent |
| **Dataset Management** | Good | Excellent |
| **Prompt Management** | ❌ None | ✅ Built-in |
| **Cost Tracking** | Basic | Good |
| **Experiment Tracking** | Excellent | Good |
| **W&B Integration** | ✅ Native | ❌ None |
| **Free Tier** | Limited | 5K traces |
| **Pricing** | $50/user | $39/user |

**Choose Weave if**: You use W&B and want automatic versioning
**Choose LangSmith if**: You use LangChain and want comprehensive observability

---

### vs Custom-Evals

| Aspect | Weave | Custom-Evals |
|--------|-------|--------------|
| **Infrastructure** | W&B Cloud | None |
| **Dependencies** | W&B account | Minimal |
| **Experiment Tracking** | Excellent | Manual |
| **Automatic Versioning** | Yes | No |
| **Dashboard** | Rich UI | External |
| **Cost** | Free tier + paid | LLM API only |
| **Flexibility** | Medium | High |
| **Learning Curve** | Medium | Easy |
| **Setup Effort** | Medium | Minimal |

**Choose Weave if**: You need experiment tracking and versioning with UI
**Choose Custom-Evals if**: You want lightweight, no infrastructure, maximum flexibility

---

## When to Choose Weave

### ✅ Perfect For

1. **Existing W&B Users**
   - Already using Weights & Biases
   - Unified ML + LLM tracking
   - Single platform for all experiments
   - Leveraging existing infrastructure
   - Team already trained on W&B

2. **Experiment-Heavy Workflows**
   - A/B testing multiple configurations
   - Hyperparameter optimization
   - Comparing many model variants
   - Tracking performance trends
   - Systematic experimentation

3. **Automatic Versioning Needs**
   - Want reproducibility by default
   - Don't want manual version management
   - Need to track code + data + config
   - Auditing and compliance requirements
   - Research reproducibility

4. **Teams Prioritizing Collaboration**
   - Multiple team members
   - Shared experiment visibility
   - Collaborative evaluation
   - Centralized results
   - Team dashboards

5. **Prompt Engineering & Testing**
   - Testing many prompt variants
   - Tracking prompt evolution
   - Comparing prompt performance
   - Version control for prompts (via code)
   - Systematic prompt optimization

6. **Model Comparison**
   - Comparing multiple models
   - Side-by-side evaluation
   - Performance benchmarking
   - Cost vs quality analysis
   - Historical comparisons

### ❌ Not Ideal For

1. **No W&B Experience**
   - Learning curve for W&B concepts
   - Consider simpler alternatives first
   - Alternative: Custom-Evals, RAGAS

2. **Self-Hosting Requirements**
   - No self-hosting option
   - Cloud-only platform
   - Alternative: Langfuse (OSS)

3. **Cost-Conscious Small Teams**
   - Per-user pricing adds up
   - Free tier may be insufficient
   - Alternative: Langfuse, Custom-Evals

4. **Heavy Prompt Management Needs**
   - No built-in prompt management
   - Need centralized prompt library
   - Alternative: Langfuse, LangSmith, Humanloop

5. **Detailed Cost Tracking**
   - Basic cost tracking only
   - Need granular cost analytics
   - Alternative: Langfuse

---

## Pricing

### Pricing Tiers (2026)

| Tier | Price | Features | Best For |
|------|-------|----------|----------|
| **Free** | $0 | Limited storage, public projects | Individuals, open source |
| **Pro** | $50/user/month | 100GB storage, private projects, priority support | Small teams, startups |
| **Teams** | Custom | Enterprise features, SSO, SLA | Medium teams |
| **Enterprise** | Custom | Dedicated support, custom contracts | Large organizations |

### Free Tier Details

**Included:**
- Unlimited projects (public)
- Unlimited runs
- 100GB storage limit
- Basic features
- Community support

**Limitations:**
- Public projects only
- Limited storage
- No SSO
- No SLA

### Pro Tier Details ($50/user/month)

**Included:**
- Private projects
- 100GB storage per user
- Priority support
- Advanced features
- Team collaboration
- All Weave features

**Best for:**
- Small to medium teams (2-10 users)
- Private/commercial projects
- Production use cases

### Cost Comparison Examples

**Example 1: Individual (Free Tier)**
- **Weave**: $0 (if public projects OK)
- **Langfuse**: $0 (up to 50K observations)
- **Custom-Evals**: $0 + LLM costs

**Example 2: Team of 5**
- **Weave**: $250/month (5 × $50)
- **Langfuse**: $59-499/month (flat rate, unlimited users)
- **Braintrust**: ~$100/month
- **LangSmith**: $195/month (5 × $39)

**Example 3: Team of 20**
- **Weave**: $1,000/month (20 × $50)
- **Langfuse**: $499/month (flat rate, unlimited users)
- **LangSmith**: $780/month (20 × $39)

### Additional Costs

**W&B Platform Costs:**
- If not already using W&B for ML
- Need to factor in overall W&B costs
- Shared infrastructure across ML/LLM projects

**Storage Overages:**
- Additional storage if exceeding limits
- Typically $0.10-0.50 per GB/month

### Typical Monthly Costs

| Team Size | Estimated Cost | Notes |
|-----------|----------------|-------|
| **1 user (free)** | $0 | Public projects |
| **1 user (pro)** | $50 | Private projects |
| **5 users** | $250 | Small team |
| **10 users** | $500 | Medium team |
| **20+ users** | Custom | Enterprise pricing |

---

## Quick Start

### Installation

```bash
# Install Weave
pip install weave

# For complete W&B integration
pip install wandb weave

# Login to W&B (first time only)
wandb login
```

### Basic Setup (5 Minutes)

```python
import weave

# Initialize Weave (connects to W&B)
weave.init("my-llm-project")

print("✓ Weave initialized and connected to W&B")
```

### Basic Tracing Example

```python
import weave

# Initialize
weave.init("llm-evaluation")

# Decorate functions to automatically track
@weave.op()
def qa_model(question: str) -> str:
    """Simple Q&A function - automatically tracked."""
    answers = {
        "What is AI?": "Artificial Intelligence is machine intelligence.",
        "What is ML?": "Machine Learning learns from data."
    }
    return answers.get(question, "I don't know.")

# Call function - automatically traced
question = "What is AI?"
answer = qa_model(question)

print(f"Q: {question}")
print(f"A: {answer}")
print("✓ Automatically tracked in Weave")
```

### Model Class Pattern (Recommended)

```python
import weave
from typing import List, Dict

weave.init("rag-evaluation")

class RAGModel(weave.Model):
    """RAG system with automatic versioning."""

    model_name: str
    temperature: float

    @weave.op()
    def retrieve(self, query: str) -> List[str]:
        """Retrieve relevant documents."""
        # Your retrieval logic
        docs = ["Doc 1", "Doc 2", "Doc 3"]
        return docs

    @weave.op()
    def generate(self, query: str, context: List[str]) -> str:
        """Generate answer from context."""
        # Your generation logic
        answer = f"Answer based on {len(context)} documents"
        return answer

    @weave.op()
    def predict(self, query: str) -> Dict:
        """Full pipeline - automatically versioned."""
        documents = self.retrieve(query)
        answer = self.generate(query, documents)

        return {
            "query": query,
            "answer": answer,
            "context": documents
        }

# Create model instance
model = RAGModel(
    model_name="gpt-4",
    temperature=0.7
)

# Use model - everything tracked and versioned
result = model.predict("What is machine learning?")
print(f"Answer: {result['answer']}")
print("✓ Model version, inputs, outputs all tracked")
```

### Dataset & Evaluation Example

```python
import weave

weave.init("evaluation-project")

# Create evaluation dataset
dataset = weave.Dataset(
    name="qa_test_set",
    rows=[
        {
            "question": "What is AI?",
            "expected": "Artificial Intelligence"
        },
        {
            "question": "What is ML?",
            "expected": "Machine Learning"
        }
    ]
)

# Publish dataset (versioned automatically)
weave.publish(dataset)

# Define model
@weave.op()
def qa_model(question: str) -> str:
    return "AI is Artificial Intelligence"

# Define evaluator
@weave.op()
def accuracy_evaluator(expected: str, actual: str) -> dict:
    """Evaluate answer accuracy."""
    score = 1.0 if expected.lower() in actual.lower() else 0.0
    return {"accuracy": score}

# Create evaluation
evaluation = weave.Evaluation(
    dataset=dataset.rows,
    scorers=[accuracy_evaluator]
)

# Run evaluation
results = evaluation.evaluate(qa_model)

print("✓ Evaluation completed and tracked")
print(f"  Results: {results}")
```

---

## Key Features Deep Dive

### 1. Automatic Versioning

**How It Works:**
```python
import weave

weave.init("auto-versioning")

class MyModel(weave.Model):
    """Model configuration is versioned automatically."""
    model_name: str
    temperature: float

    @weave.op()
    def predict(self, input: str) -> str:
        # Code changes are tracked
        # Configuration is versioned
        # Predictions are logged
        return f"Response using {self.model_name}"

# Version 1
model_v1 = MyModel(model_name="gpt-4", temperature=0.7)
result1 = model_v1.predict("test")

# Version 2 (different config)
model_v2 = MyModel(model_name="gpt-4", temperature=0.9)
result2 = model_v2.predict("test")

# Both versions tracked separately
# Can compare performance across versions
# Full reproducibility
```

**Benefits:**
- No manual version tracking
- Automatic code versioning
- Configuration capture
- Full reproducibility
- Easy comparison

### 2. Experiment Tracking

**Compare Experiments:**
```python
import weave

weave.init("experiments")

@weave.op()
def run_experiment(config: dict):
    """Run experiment with config."""
    model = create_model(config)
    results = evaluate_model(model)
    return results

# Run multiple experiments
configs = [
    {"model": "gpt-4", "temp": 0.3},
    {"model": "gpt-4", "temp": 0.7},
    {"model": "gpt-4", "temp": 0.9},
]

for config in configs:
    results = run_experiment(config)
    # Each run tracked separately
    # Compare in UI

# View comparison in Weave dashboard:
# - Side-by-side results
# - Performance trends
# - Configuration differences
```

### 3. Custom Evaluators

**Build Custom Scoring:**
```python
import weave

@weave.op()
def relevance_scorer(question: str, answer: str) -> dict:
    """Custom relevance evaluator."""
    question_words = set(question.lower().split())
    answer_words = set(answer.lower().split())

    overlap = question_words.intersection(answer_words)
    score = len(overlap) / len(question_words) if question_words else 0.0

    return {
        "relevance": score,
        "matched_words": list(overlap)
    }

@weave.op()
def completeness_scorer(answer: str) -> dict:
    """Check answer completeness."""
    min_length = 20
    score = min(len(answer) / 100, 1.0)

    return {
        "completeness": score,
        "length": len(answer),
        "meets_minimum": len(answer) >= min_length
    }

# Use in evaluation
evaluation = weave.Evaluation(
    dataset=test_dataset,
    scorers=[relevance_scorer, completeness_scorer]
)

results = evaluation.evaluate(my_model)
```

### 4. Prompt Versioning (via Code)

**Track Prompt Evolution:**
```python
import weave

# Prompts as versioned code
class PromptV1(weave.Model):
    @weave.op()
    def format(self, question: str) -> str:
        return f"Answer: {question}"

class PromptV2(weave.Model):
    @weave.op()
    def format(self, question: str) -> str:
        return f"You are a helpful assistant. Answer: {question}"

class PromptV3(weave.Model):
    @weave.op()
    def format(self, question: str) -> str:
        return f"Expert assistant. Detailed answer: {question}"

# Test all versions
prompts = [PromptV1(), PromptV2(), PromptV3()]

for i, prompt in enumerate(prompts, 1):
    formatted = prompt.format("What is AI?")
    # Each version tracked separately
    # Compare performance in UI
```

### 5. W&B Integration

**Unified ML + LLM Tracking:**
```python
import wandb
import weave

# Initialize both (shared infrastructure)
wandb.init(project="unified-ml-llm")
weave.init("unified-ml-llm")

# Track ML metrics with W&B
wandb.log({"accuracy": 0.95, "loss": 0.05})

# Track LLM operations with Weave
@weave.op()
def llm_task():
    pass

# Single dashboard for:
# - Traditional ML metrics
# - LLM traces
# - Model performance
# - Experiments
```

---

## Architecture Highlights

### System Architecture

```
Weave Platform (W&B Cloud)
├── Core W&B Infrastructure
│   ├── User Authentication
│   ├── Project Management
│   ├── Storage Layer
│   └── API Layer
│
├── Weave Components
│   ├── Automatic Versioning Engine
│   ├── Trace Collection & Storage
│   ├── Evaluation Pipeline
│   ├── Dataset Management
│   └── Comparison Tools
│
├── Web UI
│   ├── Trace Explorer
│   ├── Experiment Comparison
│   ├── Evaluation Results
│   ├── Dataset Viewer
│   └── Performance Charts
│
└── Python SDK
    ├── @weave.op() decorator
    ├── weave.Model class
    ├── weave.Dataset
    └── weave.Evaluation
```

### Integration Flow

```
Your Application
        │
        ├── @weave.op() decorated functions
        │
        ├── weave.Model subclasses
        │
        └── Direct API calls
                │
                └── Weave SDK
                        │
                        ├── Automatic versioning
                        ├── Trace capture
                        ├── Artifact logging
                        │
                        └── W&B Cloud
                                │
                                ├── Storage
                                ├── Analytics
                                └── UI/API
```

---

## Comparison Summary

### Unique Advantages
1. ⚡ Automatic versioning (code + data + config)
2. 🔬 Excellent experiment tracking
3. 🔗 Seamless W&B integration
4. 📊 Rich visualization and comparison tools
5. 🐍 Clean Python-first API
6. 🏗️ Model class pattern for structure
7. 📈 Proven W&B infrastructure
8. 👥 Strong team collaboration features

### Trade-offs
1. Requires W&B account (cloud-only)
2. Not open source
3. Per-user pricing model
4. No built-in prompt management
5. Basic cost tracking
6. Vendor lock-in to W&B

---

## Best Practices

### 1. Use Model Classes

```python
# Good: Structured, versioned
class MySystem(weave.Model):
    config: dict

    @weave.op()
    def predict(self, input):
        pass

# Avoid: Unstructured functions
@weave.op()
def unstructured_prediction(input):
    pass
```

### 2. Version Datasets

```python
# Create versioned datasets
dataset_v1 = weave.Dataset(name="test_set_v1", rows=data)
weave.publish(dataset_v1)

# Update dataset → new version automatically
dataset_v2 = weave.Dataset(name="test_set_v2", rows=updated_data)
weave.publish(dataset_v2)
```

### 3. Use Custom Evaluators

```python
# Build domain-specific evaluators
@weave.op()
def domain_specific_scorer(output, expected):
    # Your custom logic
    return {"score": score, "details": details}
```

### 4. Leverage Experiment Comparison

```python
# Run systematic experiments
for config in configs:
    model = MyModel(**config)
    results = evaluate(model)
    # Compare all runs in UI
```

### 5. Tag and Organize

```python
# Use metadata for organization
@weave.op()
def my_function():
    weave.log({"experiment": "prompt_optimization", "version": "v2"})
```

---

## Migration Guide

### From Manual Tracking

```python
# Before: Manual logging
results = {"accuracy": 0.85}
with open("results.json", "w") as f:
    json.dump(results, f)

# After: Automatic with Weave
@weave.op()
def evaluate_model():
    results = {"accuracy": 0.85}
    return results  # Automatically tracked
```

### From Other Platforms

```python
# From LangSmith
from langsmith import traceable

@traceable
def my_func():
    pass

# To Weave
import weave

@weave.op()
def my_func():
    pass
```

---

## Resources

### Documentation
- **Official Docs**: https://wandb.me/weave
- **W&B Docs**: https://docs.wandb.ai/
- **API Reference**: https://weave-docs.wandb.ai/

### Code Examples
- **GitHub**: https://github.com/wandb/weave
- **Example Projects**: https://weave-docs.wandb.ai/examples
- **Integration Examples**: [wandb_weave_example.py](wandb_weave_example.py)

### Community
- **W&B Community**: https://community.wandb.ai/
- **Discord**: W&B Discord server
- **GitHub Issues**: https://github.com/wandb/weave/issues

### Video Tutorials
- Getting Started with Weave
- Weave for LLM Evaluation
- Experiment Tracking Best Practices
- Integration with W&B

---

## Verdict

**Weave is the best choice for teams already using Weights & Biases who want automatic versioning, excellent experiment tracking, and seamless integration with their existing ML infrastructure.**

**Rating**: ⭐⭐⭐⭐☆ (4/5 for W&B users, 3/5 for non-W&B users)

### Choose Weave if you value:
- ✅ Automatic versioning (code + data + config)
- ✅ Excellent experiment tracking
- ✅ W&B integration
- ✅ Clean Python API
- ✅ Rich visualization
- ✅ Team collaboration
- ✅ Proven infrastructure
- ✅ Reproducibility by default

### Choose alternatives if you need:
- ❌ Open source → Langfuse, Custom-Evals
- ❌ Self-hosting → Langfuse
- ❌ Cost tracking → Langfuse
- ❌ Prompt management → Langfuse, Humanloop, LangSmith
- ❌ No W&B account → Custom-Evals, RAGAS
- ❌ Lower costs for large teams → Langfuse

---

**Next**: [Compare Braintrust](17_Braintrust.md) | [Compare All Frameworks](Compare_All_Eval_Frameworks.md)

---

## Example Integration

See comprehensive code examples in [wandb_weave_example.py](wandb_weave_example.py)
