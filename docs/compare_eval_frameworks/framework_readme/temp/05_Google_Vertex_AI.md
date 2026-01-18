# Google Vertex AI Gen AI Evaluation: Enterprise-Grade GCP Native Evaluation

**Type**: Cloud Service | **License**: Commercial (GCP) | **Year**: 2023

---

## Quick Overview

Google Vertex AI Gen AI Evaluation Service is **Google Cloud Platform's native evaluation solution** for LLM applications, tightly integrated with Gemini models and GCP infrastructure. It's the go-to choice for organizations already invested in the Google Cloud ecosystem who need enterprise-grade evaluation with minimal setup.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | General LLM evaluation + RAG |
| **Setup Time** | ⚡ 10 minutes (with GCP account) |
| **Learning Curve** | Easy-Medium |
| **Dependencies** | Google Cloud Platform |
| **Cost** | Pay-per-use (Gemini throughput) |
| **Best For** | GCP-native enterprises |

---

## Key Strengths

### ✅ Advantages

1. **GCP Native Integration**
   - Seamless integration with Vertex AI platform
   - Works out-of-the-box with Gemini models
   - No additional infrastructure needed
   - Built into Google Cloud Console
   - Native support for GCP authentication and IAM

2. **Comprehensive Metrics Suite**
   - **Model-based metrics**: Fluency, coherence, safety, groundedness
   - **Statistical metrics**: ROUGE (n, L, Lsum), BLEU
   - **Specialized ML metrics**: COMET, MetricX
   - **RAG metrics**: Groundedness, context relevance
   - **Q&A metrics**: Quality, relevance, helpfulness, correctness
   - **Tool metrics**: Function call validity, parameter matching
   - **Custom metrics**: PointwiseMetric and PairwiseMetric

3. **Gemini-Powered Evaluation**
   - Uses Gemini 2.5 Flash as default judge model
   - Benefits from Google's latest LLM advances
   - Consistent evaluation quality
   - Optimized for Google's model ecosystem

4. **Enterprise-Ready**
   - Built-in authentication and security (OAuth 2.0)
   - SOC 2, ISO 27001 compliance
   - Data residency options
   - Enterprise support from Google Cloud
   - SLA guarantees for production use

5. **Flexible Evaluation Options**
   - REST API for programmatic access
   - Python SDK for easy integration
   - Batch evaluation support
   - Custom evaluation criteria via templates
   - Both reference-based and reference-free metrics

6. **Pairwise Comparison Support**
   - A/B testing built-in
   - Compare baseline vs candidate models
   - Side-by-side evaluation
   - Automated preference scoring

### ⚠️ Limitations

1. **GCP Vendor Lock-in**
   - Requires Google Cloud Platform account
   - Tied to GCP infrastructure
   - Migration to other platforms is complex
   - Dependent on GCP pricing changes

2. **Cost Considerations**
   - Consumes Gemini 2.5 Flash throughput
   - Can get expensive at scale
   - Separate charges for COMET and MetricX
   - No free tier for evaluation service
   - Cost not transparent upfront

3. **Limited Local Development**
   - Requires internet connectivity
   - No offline evaluation mode
   - Must authenticate with GCP
   - Not ideal for laptop-only development

4. **Initial Propagation Delay**
   - First API calls may be slower
   - Cold start issues
   - Throughput limits on first use
   - Needs warm-up period

5. **Documentation Gaps**
   - Some metrics poorly documented
   - Limited community examples
   - Fewer third-party tutorials vs open-source
   - Enterprise focus reduces public knowledge base

6. **Gemini Dependency**
   - Evaluation quality tied to Gemini models
   - Limited model choice for judging
   - Can't use other LLM providers for evaluation
   - Subject to Gemini availability and rate limits

---

## vs Other Frameworks

### vs Custom-Evals

| Aspect | Vertex AI | Custom-Evals |
|--------|-----------|--------------|
| **Scope** | General + RAG | General + RAG + Code |
| **Setup** | GCP account required | Pip install only |
| **Infrastructure** | Managed cloud | Local-first |
| **Multi-Framework** | GCP-only | 17+ frameworks |
| **Cost** | Pay-per-use | Free (OSS) + API costs |
| **Customization** | Limited | Extensive |
| **Enterprise Features** | ✅✅ Excellent | ⚠️ Basic |

**Choose Vertex AI if**: You're on GCP and need enterprise features with managed infrastructure

**Choose Custom-Evals if**: You want flexibility, local development, or multi-cloud support

---

### vs RAGAS

| Aspect | Vertex AI | RAGAS |
|--------|-----------|-------|
| **RAG Metrics** | ✅ Good | ✅✅ Best-in-class |
| **Platform** | Cloud-only | Local + Cloud |
| **Setup** | More complex | Simpler |
| **Vendor** | Google-only | Framework-agnostic |
| **Cost Model** | Throughput-based | Per-eval API cost |
| **Research Backing** | Limited | Strong |
| **Customization** | Medium | Limited |

**Choose Vertex AI if**: You're committed to GCP and need enterprise features

**Choose RAGAS if**: You want best-in-class RAG metrics without vendor lock-in

---

### vs LangSmith

| Aspect | Vertex AI | LangSmith |
|--------|-----------|-----------|
| **Platform** | GCP-only | Multi-cloud |
| **Observability** | Limited | ✅✅ Excellent |
| **Tracing** | Basic | Advanced |
| **Cost** | GCP throughput | Subscription |
| **LangChain Integration** | Manual | Native |
| **Real-time Monitoring** | Limited | Core feature |
| **Dataset Management** | Basic | Advanced |

**Choose Vertex AI if**: You're on GCP and primarily need evaluation

**Choose LangSmith if**: You need full observability with LangChain integration

---

## When to Choose Vertex AI

### ✅ Perfect For

1. **GCP-Native Organizations**
   - Already using Google Cloud Platform
   - Using Vertex AI for model deployment
   - Committed to GCP ecosystem
   - Need unified billing and management

2. **Gemini Model Users**
   - Building applications with Gemini models
   - Need evaluation aligned with Gemini
   - Want consistent Google model ecosystem
   - Testing Gemini performance

3. **Enterprise Requirements**
   - Need SOC 2 / ISO 27001 compliance
   - Require SLA guarantees
   - Need enterprise support
   - Want managed infrastructure

4. **Production LLM Applications**
   - Deploying at scale on GCP
   - Need automated quality assurance
   - Require reliable evaluation service
   - Want minimal operational overhead

5. **A/B Testing & Model Comparison**
   - Comparing different model versions
   - Testing prompt variations
   - Evaluating retrieval strategies
   - Pairwise preference evaluation

### ❌ Not Ideal For

1. **Multi-Cloud Environments**
   - Using AWS or Azure
   - Need cloud-agnostic solutions
   - Want to avoid vendor lock-in
   - Require portability

2. **Local Development**
   - Developing offline
   - Want laptop-only evaluation
   - Need fast iteration without API calls
   - Limited internet connectivity

3. **Cost-Sensitive Projects**
   - Small budget for evaluation
   - Need cost predictability
   - Want to minimize cloud spend
   - Prefer open-source solutions

4. **Non-GCP Model Users**
   - Using OpenAI, Anthropic, or other providers
   - Need evaluation for non-Google models
   - Want provider flexibility
   - Testing various model providers

5. **Research & Experimentation**
   - Need extensive customization
   - Want to modify evaluation metrics
   - Require algorithmic transparency
   - Prefer open-source frameworks

---

## Pricing

### Cost Breakdown

| Component | Cost |
|-----------|------|
| **Evaluation Service** | Included with GCP |
| **Model-based Metrics** | Gemini 2.5 Flash throughput |
| **COMET/MetricX** | Separate ML model usage (preview: free) |
| **Statistical Metrics** | Free (ROUGE, BLEU) |
| **Infrastructure** | None (managed service) |

### Detailed Cost Analysis

#### Gemini 2.5 Flash Throughput Pricing
(as of January 2026, subject to change)

**Input Pricing:**
- Standard: ~$0.075 per 1M tokens
- Long context: ~$0.15 per 1M tokens

**Output Pricing:**
- Standard: ~$0.30 per 1M tokens
- Long context: ~$0.60 per 1M tokens

#### Per Evaluation Cost Estimates

**Single Evaluation** (using model-based metrics):
- Input tokens: ~1,000-2,000 (question + answer + context)
- Output tokens: ~100-500 (evaluation reasoning)
- Cost per eval: ~$0.001-0.003

**Multiple Metrics** (5 metrics):
- Cost per sample: ~$0.005-0.015

#### Monthly Cost Estimates

| Evaluations/Month | Statistical Only | With Model Metrics |
|-------------------|------------------|-------------------|
| 1,000 | $0 | $5-15 |
| 10,000 | $0 | $50-150 |
| 100,000 | $0 | $500-1,500 |
| 1,000,000 | $0 | $5,000-15,000 |

### Cost Optimization Tips

1. **Use statistical metrics when possible** - ROUGE and BLEU are free
2. **Batch evaluations** - More efficient than one-by-one
3. **Sample your dataset** - Evaluate subset for quick feedback
4. **Monitor throughput usage** - Set budget alerts in GCP
5. **Use appropriate context length** - Avoid long context pricing when not needed
6. **Cache results** - Avoid re-evaluating same samples

---

## Quick Start

### Prerequisites

```bash
# Install Google Cloud SDK
# Follow: https://cloud.google.com/sdk/docs/install

# Install Vertex AI SDK
pip install google-cloud-aiplatform

# Authenticate
gcloud auth application-default login

# Set project
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_REGION=us-central1
```

### 5-Minute Example

```python
import vertexai
from vertexai.preview.evaluation import EvalTask

# Initialize Vertex AI
vertexai.init(
    project="your-project-id",
    location="us-central1"
)

# Prepare evaluation data
eval_dataset = [
    {
        "question": "What is the capital of France?",
        "prediction": "The capital of France is Paris.",
        "reference": "Paris",
        "context": "France is a country in Western Europe. Its capital city is Paris."
    }
]

# Create evaluation task
eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=[
        "exact_match",
        "question_answering_quality",
        "question_answering_relevance",
        "groundedness"
    ],
    experiment="quick-start-eval"
)

# Run evaluation
result = eval_task.evaluate()

# View results
print(f"Exact Match: {result.summary_metrics['exact_match']:.3f}")
print(f"QA Quality: {result.summary_metrics['question_answering_quality']:.3f}")
print(f"Relevance: {result.summary_metrics['question_answering_relevance']:.3f}")
print(f"Groundedness: {result.summary_metrics['groundedness']:.3f}")
```

**Output:**
```
Exact Match: 1.000
QA Quality: 0.950
Relevance: 0.980
Groundedness: 0.975
```

---

## Advanced Usage Examples

### 1. RAG System Evaluation

```python
from vertexai.preview.evaluation import EvalTask
import vertexai

vertexai.init(project="your-project-id", location="us-central1")

# RAG evaluation dataset
eval_dataset = [
    {
        "question": "What are the health benefits of exercise?",
        "context": "Regular exercise improves cardiovascular health, "
                  "strengthens muscles, and enhances mental well-being.",
        "prediction": "Exercise provides benefits including improved heart health, "
                     "stronger muscles, and better mental health.",
        "reference": "Exercise benefits cardiovascular health, muscle strength, "
                    "and mental wellness."
    }
]

# Comprehensive RAG metrics
eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=[
        "groundedness",                     # Anti-hallucination
        "question_answering_quality",       # Overall quality
        "question_answering_relevance",     # Relevance to question
        "question_answering_helpfulness",   # Helpfulness
        "coherence",                        # Internal consistency
        "fluency",                          # Language quality
        "fulfillment"                       # Complete answer
    ],
    experiment="rag-comprehensive-eval"
)

result = eval_task.evaluate(model="gemini-1.5-pro")

print("\nRAG Evaluation Results:")
for metric, score in result.summary_metrics.items():
    print(f"  {metric}: {score:.3f}")

# Check for issues
if result.summary_metrics['groundedness'] < 0.8:
    print("\n⚠️ Warning: Low groundedness - potential hallucination")

if result.summary_metrics['question_answering_relevance'] < 0.7:
    print("\n⚠️ Warning: Low relevance - answer may be off-topic")
```

---

### 2. Summarization Evaluation

```python
# Evaluate text summarization
eval_dataset = [
    {
        "reference": "AI transforms industries through automation and data insights.",
        "prediction": "Artificial intelligence is revolutionizing various sectors "
                     "by automating processes and providing data-driven insights.",
        "context": "Artificial intelligence is revolutionizing various sectors "
                  "by automating processes, enhancing decision-making, and "
                  "providing data-driven insights that were previously impossible."
    }
]

eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=[
        "rouge_1",      # Unigram overlap
        "rouge_2",      # Bigram overlap
        "rouge_l",      # Longest common subsequence
        "bleu",         # N-gram precision
        "coherence",    # Logical flow
        "fluency",      # Language quality
        "summarization_quality"  # Overall summary quality
    ],
    experiment="summarization-eval"
)

result = eval_task.evaluate(
    model="gemini-1.5-pro",
    prompt_template="Summarize: {context}"
)

print(f"ROUGE-1: {result.summary_metrics['rouge_1']:.3f}")
print(f"ROUGE-L: {result.summary_metrics['rouge_l']:.3f}")
print(f"BLEU: {result.summary_metrics['bleu']:.3f}")
print(f"Coherence: {result.summary_metrics['coherence']:.3f}")
```

---

### 3. Pairwise Model Comparison (A/B Testing)

```python
# Compare two model outputs
eval_dataset = [
    {
        "prompt": "Explain quantum computing",
        "baseline_prediction": "Quantum computing uses quantum mechanics.",
        "candidate_prediction": "Quantum computing leverages quantum mechanical "
                               "phenomena like superposition and entanglement to "
                               "perform computations that are infeasible for "
                               "classical computers."
    }
]

eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=[
        "pairwise_question_answering_quality",
        "pairwise_summarization_quality"
    ],
    experiment="ab-test-eval"
)

result = eval_task.evaluate()

winner = result.summary_metrics.get('pairwise_winner', 'unknown')
quality_score = result.summary_metrics.get('pairwise_question_answering_quality', 0)

print(f"Preferred Model: {winner}")
print(f"Quality Advantage: {quality_score:.3f}")

if winner == "CANDIDATE":
    print("\n✅ Candidate model performs better")
else:
    print("\n⚠️ Baseline model performs better or equal")
```

---

### 4. Custom Evaluation Criteria

```python
# Define custom evaluation metric
custom_metric_template = """
Evaluate the technical accuracy of the response about programming.

Response: {prediction}
Reference: {reference}

Rate from 1-5:
1 = Incorrect or misleading
3 = Partially correct
5 = Fully accurate and technically sound

Consider:
- Factual correctness
- Technical precision
- Code examples (if any)
- Best practices mentioned

Provide score and brief explanation.
"""

eval_dataset = [
    {
        "prediction": "Python uses dynamic typing, allowing variables to change "
                     "types at runtime. This provides flexibility but requires "
                     "careful testing.",
        "reference": "Python is dynamically typed, meaning variable types are "
                    "determined at runtime."
    }
]

eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=[
        {
            "metric_name": "technical_accuracy",
            "metric_prompt_template": custom_metric_template
        }
    ],
    experiment="custom-metric-eval"
)

result = eval_task.evaluate(model="gemini-1.5-pro")

print(f"Technical Accuracy: {result.summary_metrics['technical_accuracy']:.3f}")
```

---

### 5. Safety & Toxicity Evaluation

```python
# Evaluate content safety
eval_dataset = [
    {
        "prediction": "I'd be happy to help you with your programming question. "
                     "Let me explain the concept clearly."
    },
    {
        "prediction": "That's a great question about data structures. Here's how "
                     "it works..."
    }
]

eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=[
        "safety"  # Checks for harmful, toxic, or inappropriate content
    ],
    experiment="safety-eval"
)

result = eval_task.evaluate()

safety_score = result.summary_metrics.get('safety', 0)
print(f"Safety Score: {safety_score:.3f}")

if safety_score > 0.95:
    print("✅ Content is safe")
elif safety_score > 0.80:
    print("⚠️ Minor safety concerns")
else:
    print("❌ Safety issues detected - review required")
```

---

### 6. Tool/Function Calling Evaluation

```python
# Evaluate function call accuracy
eval_dataset = [
    {
        "function_call_prediction": {
            "name": "get_weather",
            "parameters": {
                "location": "San Francisco",
                "units": "celsius"
            }
        },
        "function_call_reference": {
            "name": "get_weather",
            "parameters": {
                "location": "San Francisco",
                "units": "celsius"
            }
        }
    }
]

eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=[
        "tool_call_valid",          # Is call syntactically valid?
        "tool_name_match",          # Correct function name?
        "tool_parameter_key_match", # Correct parameter names?
        "tool_parameter_kv_match"   # Correct parameter values?
    ],
    experiment="tool-call-eval"
)

result = eval_task.evaluate()

print("Function Call Evaluation:")
print(f"  Valid: {result.summary_metrics['tool_call_valid']:.3f}")
print(f"  Name Match: {result.summary_metrics['tool_name_match']:.3f}")
print(f"  Param Keys: {result.summary_metrics['tool_parameter_key_match']:.3f}")
print(f"  Param Values: {result.summary_metrics['tool_parameter_kv_match']:.3f}")
```

---

### 7. Batch Evaluation with REST API

```python
import requests
import os
import json

# REST API endpoint
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = "us-central1"
url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}:evaluateInstances"

# Get OAuth token
access_token = os.popen("gcloud auth print-access-token").read().strip()

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Evaluation request
payload = {
    "instances": [
        {
            "prediction": "Paris is the capital of France.",
            "reference": "Paris",
        }
    ],
    "metrics": [
        {"type": "exact_match"},
        {"type": "rouge_l"}
    ]
}

response = requests.post(url, headers=headers, json=payload)
results = response.json()

print("REST API Evaluation Results:")
print(json.dumps(results, indent=2))
```

---

## Architecture Highlights

### Design Principles

1. **Cloud-Native**: Built for GCP infrastructure and scalability
2. **Managed Service**: No infrastructure to maintain
3. **Gemini-Powered**: Leverages Google's latest LLM technology
4. **Enterprise-Grade**: SOC 2, ISO compliance, SLA support
5. **Flexible**: REST API + Python SDK

### Available Metrics Explained

#### Model-Based Metrics (Uses Gemini 2.5 Flash)

**PointwiseMetric**: Custom single-response evaluation
- Define your own criteria
- Score individual responses
- Flexible scoring scale
- Use case: Domain-specific quality

**PairwiseMetric**: Custom comparison evaluation
- Compare two responses
- Determine preference
- Relative scoring
- Use case: A/B testing

**Fluency**: Language quality and naturalness
- Grammatical correctness
- Natural phrasing
- Readability
- Score: 1-5

**Coherence**: Logical consistency
- Internal logic
- Topic coherence
- Flow between sentences
- Score: 1-5

**Safety**: Harmful content detection
- Toxicity check
- Harmful language
- Inappropriate content
- Score: 0-1 (higher = safer)

**Groundedness**: Context grounding
- Claims supported by context
- Hallucination detection
- Factual accuracy
- Score: 0-1

**Fulfillment**: Instruction following
- Meets requirements
- Completeness
- Follows instructions
- Score: 0-1

#### Statistical Metrics (No API cost)

**ROUGE Variants**:
- `rouge_1`: Unigram overlap
- `rouge_2`: Bigram overlap
- `rouge_l`: Longest common subsequence
- `rouge_lsum`: Summary-level ROUGE
- Score: 0-1

**BLEU**: N-gram precision
- Translation quality
- Text similarity
- Multiple n-gram sizes
- Score: 0-1

**Exact Match**: Binary correctness
- Perfect match required
- Case-sensitive option
- Score: 0 or 1

#### Specialized ML Metrics

**COMET**: Translation quality
- ML-based metric
- Trained on human judgments
- Multiple languages
- Score: varies

**MetricX**: Advanced quality
- Google's proprietary metric
- Multi-dimensional quality
- State-of-the-art performance
- Score: varies

#### Q&A Specific Metrics

**question_answering_quality**: Overall QA quality
**question_answering_relevance**: Answer relevance
**question_answering_helpfulness**: Answer helpfulness
**question_answering_correctness**: Factual correctness

#### Tool/Function Metrics

**tool_call_valid**: Syntactic validity
**tool_name_match**: Function name correctness
**tool_parameter_key_match**: Parameter name accuracy
**tool_parameter_kv_match**: Parameter value accuracy

---

## Comparison Summary

### Unique Advantages

1. ⭐ **GCP Native** - Seamless integration with Google Cloud
2. 🚀 **Enterprise-Ready** - SOC 2, ISO compliance, SLA support
3. 🤖 **Gemini-Powered** - Latest Google LLM technology
4. 📊 **Comprehensive Metrics** - 20+ built-in metrics
5. 💰 **Predictable Costs** - Pay only for what you use
6. 🔒 **Secure** - Enterprise-grade security and compliance

### Trade-offs

1. GCP vendor lock-in
2. Internet connectivity required
3. Cost can scale with usage
4. Less community knowledge vs open-source
5. Limited to Gemini for evaluation judging
6. Cold start delays on first use

### Vertex AI vs The Competition

| Feature | Vertex AI | Custom-Evals | RAGAS | LangSmith | DeepEval |
|---------|-----------|--------------|-------|-----------|----------|
| **GCP Integration** | ✅✅ | ❌ | ❌ | ⚠️ | ❌ |
| **Enterprise** | ✅✅ | ⚠️ | ❌ | ✅ | ⚠️ |
| **Setup** | Medium | Easy | Easy | Easy | Easy |
| **Cost** | Throughput | API | API | Subscription | API |
| **Offline Mode** | ❌ | ✅ | ✅ | ❌ | ✅ |
| **Customization** | Medium | High | Low | Medium | High |
| **RAG Metrics** | ✅ | ✅ | ✅✅ | ✅ | ✅ |

---

## Migration Examples

### From Custom-Evals to Vertex AI

```python
# Custom-Evals approach
from custom.evals import RelevanceEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = RelevanceEvaluator(llm)

score = evaluator.evaluate({
    "input": "What is Python?",
    "output": "Python is a programming language."
})

# ===== Vertex AI approach =====
import vertexai
from vertexai.preview.evaluation import EvalTask

vertexai.init(project="your-project-id", location="us-central1")

eval_dataset = [{
    "question": "What is Python?",
    "prediction": "Python is a programming language."
}]

eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=["question_answering_relevance"],
    experiment="migration-eval"
)

result = eval_task.evaluate()
score = result.summary_metrics['question_answering_relevance']
```

**Migration Benefits:**
- Managed infrastructure (no servers)
- Enterprise compliance out-of-the-box
- Integrated with GCP ecosystem
- Better for production deployments

---

### From RAGAS to Vertex AI

```python
# RAGAS approach
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

data = {
    "question": ["What is AI?"],
    "answer": ["AI is artificial intelligence."],
    "contexts": [["Artificial intelligence is machine intelligence."]]
}
dataset = Dataset.from_dict(data)
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy])

# ===== Vertex AI approach =====
import vertexai
from vertexai.preview.evaluation import EvalTask

vertexai.init(project="your-project-id", location="us-central1")

eval_dataset = [{
    "question": "What is AI?",
    "prediction": "AI is artificial intelligence.",
    "context": "Artificial intelligence is machine intelligence."
}]

eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=[
        "groundedness",  # Similar to faithfulness
        "question_answering_relevance"  # Similar to answer_relevancy
    ],
    experiment="ragas-migration"
)

result = eval_task.evaluate(model="gemini-1.5-pro")
```

**Why Migrate:**
- Already on GCP
- Need enterprise features
- Want managed evaluation service
- Require compliance certifications

---

## Real-World Use Cases

### 1. Production RAG Quality Monitoring

```python
import vertexai
from vertexai.preview.evaluation import EvalTask
import pandas as pd
from datetime import datetime

vertexai.init(project="your-project-id", location="us-central1")

# Load production logs
prod_logs = pd.read_csv("rag_production_logs.csv")

# Convert to evaluation format
eval_dataset = [
    {
        "question": row['user_query'],
        "prediction": row['model_response'],
        "context": row['retrieved_context']
    }
    for _, row in prod_logs.iterrows()
]

# Weekly quality check
eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=[
        "groundedness",
        "question_answering_quality",
        "question_answering_relevance",
        "coherence"
    ],
    experiment=f"prod-monitoring-{datetime.now().strftime('%Y-%m-%d')}"
)

result = eval_task.evaluate(model="gemini-1.5-pro")

# Alert on quality degradation
groundedness = result.summary_metrics['groundedness']
if groundedness < 0.85:
    send_alert(f"⚠️ Groundedness dropped to {groundedness:.2f}")

# Log to monitoring system
log_to_datadog({
    "timestamp": datetime.now(),
    "groundedness": groundedness,
    "qa_quality": result.summary_metrics['question_answering_quality'],
    "samples_evaluated": len(eval_dataset)
})
```

---

### 2. Gemini Model Version Comparison

```python
# Compare Gemini 1.5 Pro vs Gemini 1.5 Flash
test_prompts = load_test_prompts()

# Generate responses from both models
pro_responses = generate_with_model("gemini-1.5-pro", test_prompts)
flash_responses = generate_with_model("gemini-1.5-flash", test_prompts)

# Pairwise comparison
eval_dataset = [
    {
        "prompt": prompt,
        "baseline_prediction": flash_resp,
        "candidate_prediction": pro_resp
    }
    for prompt, flash_resp, pro_resp in zip(
        test_prompts, flash_responses, pro_responses
    )
]

eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=["pairwise_question_answering_quality"],
    experiment="gemini-version-comparison"
)

result = eval_task.evaluate()

winner_count = sum(
    1 for r in result.metrics_table.iterrows()
    if r[1]['pairwise_winner'] == 'CANDIDATE'
)

print(f"Gemini 1.5 Pro won {winner_count}/{len(test_prompts)} comparisons")
print(f"Quality advantage: {result.summary_metrics['pairwise_question_answering_quality']:.3f}")
```

---

## Resources

### Official Documentation
- **Main Docs**: https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/evaluation
- **Quickstart**: https://cloud.google.com/vertex-ai/docs/generative-ai/evaluation/quickstart
- **Metrics Reference**: https://cloud.google.com/vertex-ai/docs/generative-ai/evaluation/metrics
- **API Reference**: https://cloud.google.com/python/docs/reference/aiplatform/latest

### Setup & Authentication
- **GCP SDK**: https://cloud.google.com/sdk/docs/install
- **Authentication**: https://cloud.google.com/docs/authentication
- **IAM Permissions**: https://cloud.google.com/vertex-ai/docs/general/access-control

### Code Examples
- **Official Examples**: https://github.com/GoogleCloudPlatform/vertex-ai-samples
- **Local Example**: `docs/compare_eval_frameworks/google_vertex_eval_example.py`
- **Colab Notebooks**: https://cloud.google.com/vertex-ai/docs/tutorials

### Pricing & Billing
- **Pricing Calculator**: https://cloud.google.com/products/calculator
- **Gemini Pricing**: https://cloud.google.com/vertex-ai/generative-ai/pricing
- **Cost Management**: https://cloud.google.com/billing/docs

### Support
- **GCP Support**: https://cloud.google.com/support
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/google-vertex-ai
- **Issue Tracker**: https://issuetracker.google.com/

---

## Verdict

**Google Vertex AI Gen AI Evaluation is the premier choice for enterprises deeply invested in the Google Cloud ecosystem, offering enterprise-grade evaluation with seamless Gemini integration and managed infrastructure.**

**Rating**: ⭐⭐⭐⭐ (4/5 for GCP users, 2/5 for multi-cloud)

### Choose Vertex AI if you value:
- ✅ GCP native integration
- ✅ Enterprise compliance (SOC 2, ISO)
- ✅ Gemini model ecosystem
- ✅ Managed infrastructure
- ✅ SLA guarantees
- ✅ Minimal operational overhead

### Choose alternatives if you need:
- ❌ Multi-cloud support → Custom-Evals, DeepEval
- ❌ Best RAG metrics → RAGAS
- ❌ Full observability → LangSmith, Phoenix
- ❌ Local development → Custom-Evals, RAGAS
- ❌ Open-source flexibility → Custom-Evals, DeepEval
- ❌ Lower costs → Open-source alternatives

---

## Decision Matrix

### Use Vertex AI when:
✅ Committed to GCP ecosystem
✅ Using Gemini models
✅ Need enterprise compliance
✅ Want managed infrastructure
✅ Deploying production applications on GCP
✅ Have GCP budget allocated

### Don't use Vertex AI when:
❌ Multi-cloud or cloud-agnostic architecture
❌ Need offline/local evaluation
❌ Limited budget or cost-sensitive
❌ Want open-source flexibility
❌ Need extensive customization
❌ Using non-Google model providers primarily

---

## Quick Reference Card

```python
# Installation
pip install google-cloud-aiplatform

# Authentication
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT=your-project-id

# Basic Usage
import vertexai
from vertexai.preview.evaluation import EvalTask

vertexai.init(project="your-project-id", location="us-central1")

eval_dataset = [{
    "question": "Your question",
    "prediction": "Model's answer",
    "reference": "Expected answer",
    "context": "Retrieved context"
}]

eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=["groundedness", "question_answering_quality"],
    experiment="my-eval"
)

result = eval_task.evaluate(model="gemini-1.5-pro")

# Core Metrics
groundedness                    # Anti-hallucination
question_answering_quality      # Overall quality
question_answering_relevance    # Relevance
rouge_l, bleu                   # Statistical similarity
safety                          # Content safety
coherence, fluency              # Language quality

# Cost: ~$0.001-0.003 per evaluation with model metrics
```

---

**Next Steps**:
1. [Try the Example Code](google_vertex_eval_example.py)
2. [Compare All Frameworks](Compare_All_Eval_Frameworks.md)
3. [View Framework Index](FRAMEWORKS_INDEX.md)

**Related**:
- [Custom-Evals Comparison](01_Custom_Evals.md)
- [RAGAS Comparison](03_RAGAS.md)
- [LangSmith Comparison](06_LangSmith.md)

---

*Last Updated: January 2026*
*Vertex AI Gen AI Evaluation Version: Latest*
*Maintained by: Custom-Evals Team*
