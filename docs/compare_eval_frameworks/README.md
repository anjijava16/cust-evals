# LLM Evaluation Frameworks Comparison

This directory contains comprehensive examples of various LLM evaluation frameworks. Each example is a standalone, runnable script demonstrating the framework's key features and capabilities.

## 📋 Table of Contents

- [Overview](#overview)
- [Frameworks Included](#frameworks-included)
- [Quick Comparison](#quick-comparison)
- [Detailed Framework Descriptions](#detailed-framework-descriptions)
- [Installation Instructions](#installation-instructions)
- [Use Case Guide](#use-case-guide)
- [Running the Examples](#running-the-examples)

---

## Overview

Evaluating Large Language Models (LLMs) is crucial for:
- **Quality Assurance**: Ensuring outputs meet standards
- **Regression Testing**: Detecting performance degradation
- **Model Selection**: Comparing different models or versions
- **Production Monitoring**: Tracking real-world performance
- **Safety & Compliance**: Detecting harmful or biased content

This collection showcases 17 major evaluation frameworks, each with unique strengths.

---

## Frameworks Included

| Framework | File | Focus Area |
|-----------|------|------------|
| **Arize Phoenix** | `arize_phoenix_example.py` | General LLM evaluation with pre-built evaluators |
| **RAGAS** | `ragas_example.py` | RAG-specific evaluation metrics |
| **Claude/Anthropic** | `claude_anthropic_eval_example.py` | LLM-as-judge using Claude |
| **Google Vertex AI** | `google_vertex_eval_example.py` | GCP-native evaluation with Gemini |
| **LangSmith** | `langsmith_eval_example.py` | LangChain integration & observability |
| **OpenAI Evals** | `openai_evals_example.py` | Standardized eval framework |
| **DeepEval** | `deepeval_example.py` | Pytest integration & CI/CD |
| **TruLens** | `trulens_example.py` | Observability & tracking |
| **Google ADK** | `google_adk_eval_example.py` | Agent evaluation & CLI-based workflow |
| **MLflow** | `mlflow_llm_eval_example.py` | ML lifecycle & experiment tracking |
| **MCPEval** | `mcpeval_example.py` | Model Context Protocol & tool use evaluation |
| **ARES** | `ares_example.py` | Automated RAG evaluation with synthetic data |
| **RAGalyst** | `ragalyst_example.py` | RAG pipeline analysis & bottleneck detection |
| **Langfuse** | `langfuse_example.py` | Production observability & prompt management |
| **Weights & Biases Weave** | `wandb_weave_example.py` | Experiment tracking, LLM tracing & artifact logging |
| **Braintrust** | `braintrust_example.py` | AI product evaluation with excellent DX |
| **Humanloop** | `humanloop_example.py` | Human-in-the-loop evaluation & prompt management |

---

## Quick Comparison

### By Primary Use Case

| Use Case | Recommended Framework(s) |
|----------|-------------------------|
| **RAG Systems** | RAGAS, ARES, RAGalyst, TruLens, Arize Phoenix |
| **General LLM Eval** | Claude, OpenAI Evals, DeepEval, MLflow, Braintrust |
| **Production Monitoring** | Langfuse, LangSmith, TruLens, Arize Phoenix, Humanloop |
| **CI/CD Integration** | DeepEval, OpenAI Evals, MLflow, Braintrust |
| **LangChain Apps** | LangSmith, TruLens, Langfuse |
| **GCP/Vertex AI** | Google Vertex AI, Google ADK |
| **Safety & Toxicity** | Claude, Arize Phoenix, DeepEval |
| **Custom Metrics** | Claude, OpenAI Evals, TruLens, Google ADK, Weave |
| **Agent Evaluation** | Google ADK, MCPEval |
| **Tool/Function Calling** | MCPEval |
| **Pipeline Analysis** | RAGalyst, TruLens |
| **Experiment Tracking** | MLflow, Langfuse, Weave, Braintrust |
| **Prompt Management** | Langfuse, LangSmith, Humanloop, Weave |
| **Human Feedback** | Humanloop, Langfuse, LangSmith |
| **A/B Testing** | Humanloop, Braintrust, Weave |

### By Key Features

| Feature | Frameworks |
|---------|------------|
| **Pre-built Metrics** | Arize Phoenix, RAGAS, ARES, DeepEval, Vertex AI |
| **LLM-as-Judge** | Claude, Arize Phoenix, LangSmith, MLflow, Weave |
| **Dashboard/UI** | TruLens, LangSmith, Langfuse, Arize Phoenix, MLflow, Weave, Braintrust, Humanloop |
| **Observability** | TruLens, LangSmith, Langfuse, RAGalyst, Weave |
| **RAG-Specific** | RAGAS, ARES, RAGalyst, TruLens, Arize Phoenix |
| **Open Source** | RAGAS, ARES, OpenAI Evals, DeepEval, TruLens, MLflow, Weave |
| **Testing Framework** | DeepEval (Pytest), OpenAI Evals, MLflow, Braintrust |
| **Cloud-Native** | Vertex AI (GCP), LangSmith, Langfuse, Google ADK, Weave |
| **CLI-First** | Google ADK, OpenAI Evals |
| **Agent/Tool Evaluation** | Google ADK, MCPEval |
| **Synthetic Data** | ARES |
| **Prompt Management** | Langfuse, LangSmith, Humanloop, Weave |
| **Cost Tracking** | Langfuse, LangSmith, Weave |
| **Human Feedback** | Humanloop, Langfuse, LangSmith |
| **Automatic Versioning** | Braintrust, Weave, Langfuse |
| **Experiment Comparison** | Weave, Braintrust, MLflow, Langfuse |

---

## Detailed Framework Descriptions

### 1. Arize Phoenix Evals

**Best For**: Comprehensive evaluation with minimal setup

**Key Features**:
- Pre-built evaluators (hallucination, relevance, toxicity, Q&A)
- Supports multiple LLM providers
- Easy integration with existing workflows
- DataFrame-based interface

**Metrics**:
- Hallucination detection
- Relevance scoring
- Q&A correctness
- Toxicity detection
- Custom LLM evaluators

**Example Use**:
```python
from phoenix.evals import HallucinationEvaluator, OpenAIModel

model = OpenAIModel(model="gpt-4")
evaluator = HallucinationEvaluator(model)
results = evaluator.evaluate(data)
```

**Pros**:
- Easy to use
- Comprehensive metric library
- Good documentation

**Cons**:
- Requires external LLM API (costs)
- Limited customization vs building from scratch

---

### 2. RAGAS (Retrieval-Augmented Generation Assessment)

**Best For**: RAG system evaluation

**Key Features**:
- RAG-specific metrics
- Evaluates both retrieval and generation
- Works with any RAG implementation
- Dataset-based evaluation

**Metrics**:
- Faithfulness (groundedness)
- Answer relevancy
- Context precision (retrieval quality)
- Context recall (retrieval coverage)
- Answer similarity & correctness

**Example Use**:
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy]
)
```

**Pros**:
- Purpose-built for RAG
- Comprehensive RAG metrics
- Easy to use

**Cons**:
- RAG-focused (limited for non-RAG tasks)
- Requires OpenAI or similar LLM API

---

### 3. Claude/Anthropic Evals

**Best For**: Flexible LLM-as-judge evaluation

**Key Features**:
- Use Claude as an evaluator
- Highly flexible evaluation criteria
- Strong reasoning capabilities
- No additional framework needed

**Metrics**:
- Response quality (accuracy, completeness, clarity)
- Hallucination detection
- Relevance assessment
- Safety & harmfulness
- Factual consistency
- Code quality
- Instruction following
- Custom rubrics

**Example Use**:
```python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": evaluation_prompt}]
)
```

**Pros**:
- Extremely flexible
- Strong reasoning for complex evaluations
- No additional framework to learn
- Great for custom criteria

**Cons**:
- API costs for evaluations
- Need to design good evaluation prompts
- Less standardization vs frameworks

---

### 4. Google Vertex AI Gen AI Evaluation

**Best For**: GCP users, Gemini model evaluation

**Key Features**:
- Native GCP integration
- Gemini-based evaluation
- Enterprise-grade infrastructure
- Multiple built-in metrics

**Metrics**:
- ROUGE, BLEU (summarization)
- Exact match, F1 (Q&A)
- Groundedness
- Safety
- Instruction following
- Pairwise comparison
- Custom metrics

**Example Use**:
```python
from vertexai.preview.evaluation import EvalTask

eval_task = EvalTask(
    dataset=data,
    metrics=["groundedness", "safety"]
)
results = eval_task.evaluate(model="gemini-1.5-pro")
```

**Pros**:
- Native GCP integration
- Enterprise support
- Gemini models included
- Comprehensive metrics

**Cons**:
- GCP-specific
- Requires GCP account & setup
- Less portable than open-source options

---

### 5. LangSmith

**Best For**: LangChain applications, production monitoring

**Key Features**:
- Deep LangChain integration
- Full observability & tracing
- Dataset management
- Human-in-the-loop evaluation
- A/B testing support
- Production monitoring

**Metrics**:
- Custom evaluators
- LLM-as-judge
- Correctness, relevance
- Any custom metric

**Example Use**:
```python
from langsmith import evaluate
from langsmith.evaluation import EvaluationResult

def my_evaluator(run, example):
    # Custom evaluation logic
    return EvaluationResult(score=0.9)

results = evaluate(
    my_function,
    data=dataset,
    evaluators=[my_evaluator]
)
```

**Pros**:
- Excellent LangChain integration
- Production monitoring
- Great dashboard
- Dataset management
- Human feedback integration

**Cons**:
- Requires LangSmith account
- Best suited for LangChain apps
- Paid service for full features

---

### 6. OpenAI Evals

**Best For**: Standardized evaluation, reproducibility

**Key Features**:
- Open-source framework
- CLI-based workflow
- Standardized format
- Community-contributed evals
- Multiple evaluation types

**Evaluation Types**:
- Exact match
- Includes (content presence)
- Model-graded
- Closed Q&A (multiple choice)
- Fuzzy match
- Custom evaluators

**Example Use**:
```bash
# CLI usage
oaievals gpt-3.5-turbo my_eval

# Programmatic usage
from my_eval import MatchEval
results = MatchEval(test_cases).run_eval()
```

**Pros**:
- Open source
- Standardized format
- CLI-based (easy automation)
- Community support

**Cons**:
- Primarily CLI-based
- Less feature-rich than newer frameworks
- Requires understanding of eval format

---

### 7. DeepEval

**Best For**: Testing workflows, CI/CD integration

**Key Features**:
- Pytest integration
- CI/CD ready
- Comprehensive metrics
- Test result tracking
- G-Eval for custom criteria

**Metrics**:
- Answer relevancy
- Faithfulness
- Hallucination detection
- Context precision & recall
- Toxicity & bias
- G-Eval (custom)

**Example Use**:
```python
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="What is AI?",
    actual_output="AI is artificial intelligence"
)

metric = AnswerRelevancyMetric(threshold=0.7)
metric.measure(test_case)
```

**Pros**:
- Pytest integration
- Great for CI/CD
- Comprehensive metrics
- Test tracking

**Cons**:
- Opinionated testing approach
- Requires buying into their framework

---

### 8. TruLens

**Best For**: Observability, intermediate step tracking

**Key Features**:
- Full observability & tracing
- Track intermediate steps
- Visual dashboard
- Custom feedback functions
- A/B testing
- Real-time monitoring

**Metrics**:
- Answer relevance
- Context relevance
- Groundedness
- Custom feedback functions
- Any metric you can define

**Example Use**:
```python
from trulens_eval import TruBasicApp, Feedback
from trulens_eval.feedback.provider.openai import OpenAI

provider = OpenAI()

f_relevance = Feedback(
    provider.relevance
).on_input_output()

tru_app = TruBasicApp(
    my_function,
    feedbacks=[f_relevance]
)

with tru_app as recording:
    result = my_function("query")
```

**Pros**:
- Excellent observability
- Track all intermediate steps
- Visual dashboard
- Flexible custom metrics

**Cons**:
- Requires wrapping your functions
- Dashboard needs to be run separately
- Learning curve for complex setups

---

### 9. Google ADK (Agent Development Kit)

**Best For**: Agent evaluation, CLI-based workflows

**Key Features**:
- CLI-first design for automation
- Agent-specific evaluation
- Custom evaluator framework
- JSONL dataset format
- Multi-model comparison
- Gemini integration

**Metrics**:
- Exact match
- Semantic similarity
- LLM-as-judge
- Custom metrics
- Agent task completion

**Example Use**:
```bash
# CLI usage
adk eval run --dataset eval_dataset.jsonl --model gemini-pro

# Programmatic usage
evaluator = ExactMatchEvaluator()
results = evaluator.evaluate_dataset(examples, predictions)
```

**Pros**:
- Powerful CLI tools
- Built for agents
- Google model integration
- Extensible evaluator system

**Cons**:
- Primarily CLI-focused
- Requires GCP familiarity
- Less documentation than mature frameworks

---

### 10. MLflow LLM Evaluate

**Best For**: ML lifecycle management, experiment tracking

**Key Features**:
- Full ML lifecycle tracking
- Experiment comparison
- Model registry integration
- Artifact logging
- Built-in and custom metrics
- Web UI dashboard

**Metrics**:
- Toxicity, flesch-kincaid
- Answer relevance, correctness, faithfulness
- Custom metrics via make_metric()
- Any evaluator you define

**Example Use**:
```python
import mlflow

with mlflow.start_run():
    results = mlflow.evaluate(
        model=qa_model,
        data=eval_data,
        targets="ground_truth",
        model_type="question-answering"
    )
```

**Pros**:
- Comprehensive ML tracking
- Great experiment comparison
- Artifact management
- Visual dashboard
- Integration with ML ecosystem

**Cons**:
- More ML-focused than LLM-specific
- Requires understanding MLflow concepts
- Additional overhead for simple evals

---

### 11. MCPEval (Model Context Protocol Evaluation)

**Best For**: Function calling, tool use, MCP-compliant systems

**Key Features**:
- Tool selection evaluation
- Argument accuracy checking
- Sequence adherence testing
- Context usage evaluation
- Error handling assessment
- Efficiency metrics

**Metrics**:
- Tool selection accuracy
- Argument correctness
- Sequence compliance
- Context utilization
- Error recovery
- Call efficiency

**Example Use**:
```python
from mcpeval import MCPEvaluator, ToolCall

evaluator = MCPEvaluator(tools)
result = evaluator.evaluate_tool_selection(
    task=task,
    expected_tools=expected,
    actual_tool_calls=actual
)
```

**Pros**:
- Purpose-built for tool/function calling
- Comprehensive tool evaluation
- Agent-friendly metrics
- Extensible framework

**Cons**:
- Narrow focus (tool use only)
- Newer framework
- Limited community resources

---

### 12. ARES (Automated RAG Evaluation System)

**Best For**: RAG evaluation with synthetic data

**Key Features**:
- RAG-specific metrics
- Synthetic data generation
- Few-shot learning approach
- Research-backed methodology
- Minimal labeled data needed
- Confidence scoring

**Metrics**:
- Context relevance (retrieval quality)
- Answer faithfulness (groundedness)
- Answer relevance (query alignment)
- Overall RAG score

**Example Use**:
```python
from ares import ARESEvaluator, RAGExample

evaluator = ARESEvaluator()
scores = evaluator.evaluate_rag_system(example)
# Returns: context_relevance, answer_faithfulness, answer_relevance
```

**Pros**:
- RAG-optimized metrics
- Synthetic data generation
- Minimal labeling required
- Research-backed approach
- Confidence scores

**Cons**:
- RAG-only focus
- Newer framework
- Less mature ecosystem
- Limited integrations

---

### 13. RAGalyst

**Best For**: RAG pipeline analysis and optimization

**Key Features**:
- Component-level analysis
- Bottleneck identification
- Latency profiling
- Quality score breakdown
- Configuration comparison
- Performance recommendations

**Metrics**:
- Retrieval precision & recall
- Generation relevance, faithfulness, coherence
- Context utilization
- Component latency
- End-to-end quality

**Example Use**:
```python
from ragalyst import RAGalystEvaluator

evaluator = RAGalystEvaluator()
retrieval_metrics = evaluator.evaluate_retrieval(...)
generation_metrics = evaluator.evaluate_generation(...)
report = evaluator.analyze_pipeline(retrieval_metrics, generation_metrics)
# Returns: bottlenecks, recommendations
```

**Pros**:
- Detailed pipeline analysis
- Bottleneck detection
- Component-level metrics
- Actionable recommendations
- Performance optimization focus

**Cons**:
- RAG-specific
- Requires instrumentation
- Less standardized format
- Smaller community

---

### 14. Langfuse

**Best For**: Production monitoring, prompt management

**Key Features**:
- Full observability & tracing
- Prompt version control
- User feedback collection
- Cost tracking
- Session tracking
- Dataset management
- Real-time monitoring
- Web dashboard

**Metrics**:
- Custom scoring
- LLM-as-judge
- User feedback ratings
- Any metric you define

**Example Use**:
```python
from langfuse import Langfuse
from langfuse.decorators import observe

@observe()
def qa_function(question):
    # Automatically traced
    return answer

# Add scores
generation.score(name="quality", value=0.9)
```

**Pros**:
- Production-ready observability
- Prompt management & versioning
- User feedback integration
- Cost tracking
- Excellent dashboard
- Session tracking

**Cons**:
- Requires cloud account
- More observability than evaluation
- Learning curve for full features
- Paid plans for scale

---

### 15. Weights & Biases Weave

**Best For**: Experiment tracking, LLM application development

**Key Features**:
- Automatic tracing with decorators
- Model versioning and tracking
- Dataset management and versioning
- Custom evaluator framework
- Evaluation pipelines
- Artifact logging
- Experiment comparison tools
- Rich visualization UI

**Metrics**:
- Custom evaluators
- LLM-as-judge
- Any metric you define
- Comparison across experiments

**Example Use**:
```python
import weave

weave.init("project-name")

@weave.op()
def qa_model(question: str) -> str:
    # Automatically traced
    return answer

# Run evaluation
evaluation = weave.Evaluation(
    dataset=test_data,
    scorers=[accuracy_scorer, quality_scorer]
)
results = evaluation.evaluate(qa_model)
```

**Pros**:
- Seamless W&B integration
- Automatic tracing and versioning
- Python-first API
- Excellent for experiment tracking
- Rich visualization dashboard
- Works with any LLM provider

**Cons**:
- Requires W&B account
- More focused on tracking than evaluation metrics
- Learning curve for W&B ecosystem

---

### 16. Braintrust

**Best For**: AI product evaluation with excellent developer experience

**Key Features**:
- Automatic versioning (git-like)
- Dataset management
- Real-time evaluation
- CI/CD integration
- Regression detection
- Custom scoring functions
- Prompt comparison
- Beautiful UI with great UX

**Metrics**:
- Custom scorers
- Accuracy, relevance, quality
- Any metric you define
- Automatic comparison between runs

**Example Use**:
```python
from braintrust import Eval

result = Eval(
    "My Evaluation",
    data=test_data,
    task=lambda x: model(x["input"]),
    scores=[accuracy_scorer, quality_scorer]
)
```

**Pros**:
- Best-in-class developer experience
- Automatic versioning (no manual tracking)
- Fast iteration cycle
- Excellent CI/CD support
- Great for regression testing
- Intuitive UI

**Cons**:
- Requires Braintrust account
- Newer platform (smaller community)
- Limited pre-built metrics

---

### 17. Humanloop

**Best For**: Human-in-the-loop evaluation, prompt management

**Key Features**:
- Human feedback collection
- Prompt versioning and management
- A/B testing
- Preference ranking
- Collaborative evaluation (multi-reviewer)
- Production monitoring
- Quality scoring framework
- Dataset curation

**Metrics**:
- Human ratings (1-5 scale)
- Preference rankings
- Quality scores (multi-dimensional)
- Custom evaluation criteria
- User satisfaction metrics

**Example Use**:
```python
from humanloop import Humanloop

client = Humanloop(api_key="your-key")

# Create prompt
prompt = client.prompts.create(
    project="qa-assistant",
    template="Answer: {{question}}"
)

# Collect human feedback
feedback = client.feedback.create(
    generation_id=gen_id,
    rating=4,
    comment="Good response"
)
```

**Pros**:
- Human feedback at center
- Excellent prompt management
- Great for team collaboration
- Built-in A/B testing
- Intuitive for non-technical users
- Production monitoring

**Cons**:
- Requires human evaluators
- Slower than automated evaluation
- Requires Humanloop account
- Less emphasis on automated metrics

---

## Installation Instructions

### Arize Phoenix
```bash
pip install arize-phoenix-evals openai pandas
```

### RAGAS
```bash
pip install ragas langchain-openai datasets
```

### Claude/Anthropic
```bash
pip install anthropic
```

### Google Vertex AI
```bash
pip install google-cloud-aiplatform

# Authentication
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

### LangSmith
```bash
pip install langsmith langchain-openai

# Set API keys
export LANGSMITH_API_KEY="your-api-key"
```

### OpenAI Evals
```bash
pip install evals openai
```

### DeepEval
```bash
pip install deepeval
```

### TruLens
```bash
pip install trulens-eval
```

### Google ADK
```bash
pip install google-adk google-generativeai

# Authentication
export GOOGLE_API_KEY="your-google-api-key"
```

### MLflow
```bash
pip install mlflow openai

# Start MLflow UI
mlflow ui
```

### MCPEval
```bash
pip install mcp
```

### ARES
```bash
pip install ares-ai
```

### RAGalyst
```bash
pip install ragalyst pandas
```

### Langfuse
```bash
pip install langfuse

# Setup (get keys from https://cloud.langfuse.com)
export LANGFUSE_PUBLIC_KEY="your-public-key"
export LANGFUSE_SECRET_KEY="your-secret-key"
```

### Weights & Biases Weave
```bash
pip install weave

# Login to W&B
wandb login

# Set project (optional)
export WANDB_PROJECT="your-project-name"
```

### Braintrust
```bash
pip install braintrust

# Setup (get key from https://www.braintrust.dev/)
export BRAINTRUST_API_KEY="your-api-key"
```

### Humanloop
```bash
pip install humanloop

# Setup (get key from https://humanloop.com/)
export HUMANLOOP_API_KEY="your-api-key"
```

### Common Requirements
Most frameworks need an LLM API key:
```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export GOOGLE_API_KEY="your-google-key"
```

---

## Use Case Guide

### Choose Your Framework by Scenario

#### Scenario 1: Building a RAG System
**Recommended**: RAGAS, TruLens

RAGAS provides RAG-specific metrics out of the box. TruLens offers great observability to debug retrieval and generation separately.

#### Scenario 2: Testing in CI/CD Pipeline
**Recommended**: DeepEval, OpenAI Evals

DeepEval integrates with Pytest. OpenAI Evals has CLI support for automation.

#### Scenario 3: Production Monitoring
**Recommended**: LangSmith, TruLens

Both offer real-time tracking, dashboards, and alerting capabilities.

#### Scenario 4: Custom Domain-Specific Evaluation
**Recommended**: Claude, TruLens

Claude allows flexible evaluation prompts. TruLens allows custom feedback functions.

#### Scenario 5: Quick Evaluation Without Much Setup
**Recommended**: Arize Phoenix, DeepEval

Both have pre-built metrics that work out of the box with minimal configuration.

#### Scenario 6: Evaluating LangChain Applications
**Recommended**: LangSmith, TruLens

LangSmith is built by LangChain team. TruLens has excellent LangChain support.

#### Scenario 7: Enterprise/GCP Environment
**Recommended**: Google Vertex AI

Native GCP integration, enterprise support, and compliance features.

#### Scenario 8: Safety & Content Moderation
**Recommended**: Claude, Arize Phoenix, DeepEval

All have strong toxicity, bias, and safety detection capabilities.

---

## Running the Examples

Each example is self-contained and can be run independently.

### General Steps:

1. **Set API Keys**:
```bash
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
# ... other keys as needed
```

2. **Install Requirements**:
```bash
# For a specific framework
pip install arize-phoenix-evals openai

# Or install all (warning: large install)
pip install arize-phoenix-evals ragas anthropic \
    google-cloud-aiplatform langsmith evals deepeval trulens-eval
```

3. **Run an Example**:
```bash
python arize_phoenix_example.py
python ragas_example.py
python claude_anthropic_eval_example.py
# ... etc
```

### Example Run Outputs:

Each script will:
- ✅ Demonstrate key features of the framework
- ✅ Run multiple evaluation examples
- ✅ Print results to console
- ✅ Show scores and metrics
- ✅ Provide commentary on results

---

## Comparison Matrix

### Feature Comparison

| Framework | RAG Focus | LLM Judge | Dashboard | Open Source | Testing Integration | Cost |
|-----------|-----------|-----------|-----------|-------------|-------------------|------|
| **Arize Phoenix** | ✅ | ✅ | ✅ | ✅ | ⚠️ | API costs |
| **RAGAS** | ✅✅ | ✅ | ❌ | ✅ | ⚠️ | API costs |
| **Claude** | ⚠️ | ✅✅ | ❌ | ✅ | ⚠️ | API costs |
| **Vertex AI** | ⚠️ | ✅ | ⚠️ | ❌ | ⚠️ | GCP costs |
| **LangSmith** | ⚠️ | ✅ | ✅✅ | ❌ | ⚠️ | Service + API |
| **OpenAI Evals** | ❌ | ✅ | ❌ | ✅ | ⚠️ | API costs |
| **DeepEval** | ✅ | ✅ | ⚠️ | ✅ | ✅✅ | API costs |
| **TruLens** | ✅ | ✅ | ✅✅ | ✅ | ⚠️ | API costs |
| **Google ADK** | ⚠️ | ✅ | ❌ | ✅ | ⚠️ | API/GCP |
| **MLflow** | ⚠️ | ✅ | ✅ | ✅ | ✅ | Free |
| **MCPEval** | ❌ | ❌ | ❌ | ✅ | ⚠️ | Free |
| **ARES** | ✅✅ | ✅ | ❌ | ✅ | ⚠️ | API costs |
| **RAGalyst** | ✅✅ | ❌ | ⚠️ | ✅ | ⚠️ | Free |
| **Langfuse** | ⚠️ | ✅ | ✅✅ | ✅ | ⚠️ | Freemium |
| **Weave** | ⚠️ | ✅ | ✅✅ | ✅ | ⚠️ | Freemium |
| **Braintrust** | ⚠️ | ✅ | ✅✅ | ✅ | ✅✅ | Freemium |
| **Humanloop** | ❌ | ⚠️ | ✅✅ | ✅ | ⚠️ | Freemium |

Legend: ✅ Yes/Good, ✅✅ Excellent, ⚠️ Partial/Limited, ❌ No/Not Focused

### Ease of Use vs Flexibility

```
High Flexibility
    ^
    |
    |    Claude
    |                          TruLens
    |
    |              OpenAI Evals
    |                              LangSmith
    |
    |
    |        Vertex AI      DeepEval
    |
    |            Phoenix
    |                      RAGAS
    |
    +--------------------------------> Ease of Use
  Hard                              Easy
```

---

## Best Practices

### 1. Start Simple
Begin with pre-built metrics from frameworks like RAGAS or DeepEval before building custom evaluations.

### 2. Combine Frameworks
You can use multiple frameworks together:
- RAGAS for RAG metrics
- Claude for custom domain evaluation
- TruLens for observability

### 3. Version Your Evaluations
Track evaluation code and datasets in version control alongside your models.

### 4. Automate
Integrate evaluations into CI/CD pipelines for regression testing.

### 5. Monitor in Production
Use frameworks like LangSmith or TruLens to track real-world performance.

### 6. Human Evaluation
Combine automated evals with human review for critical applications.

---

## Additional Resources

### Documentation Links
- **Arize Phoenix**: https://docs.arize.com/phoenix/
- **RAGAS**: https://docs.ragas.io/
- **Claude**: https://docs.anthropic.com/
- **Vertex AI**: https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/evaluation
- **LangSmith**: https://docs.smith.langchain.com/
- **OpenAI Evals**: https://github.com/openai/evals
- **DeepEval**: https://docs.confident-ai.com/
- **TruLens**: https://www.trulens.org/
- **Google ADK**: https://google.github.io/adk-docs/evaluate/
- **MLflow**: https://mlflow.org/docs/latest/llms/llm-evaluate/
- **MCPEval**: https://modelcontextprotocol.io/
- **ARES**: https://github.com/stanford-futuredata/ARES
- **RAGalyst**: https://github.com/ragalyst/ragalyst
- **Langfuse**: https://langfuse.com/docs
- **Weights & Biases Weave**: https://wandb.me/weave
- **Braintrust**: https://www.braintrust.dev/docs
- **Humanloop**: https://humanloop.com/docs

### Community
- Most frameworks have active GitHub discussions
- Join Discord/Slack communities for support
- Check framework-specific forums

---

## Contributing

To add more examples or improve existing ones:
1. Follow the existing format
2. Include comprehensive comments
3. Demonstrate multiple features
4. Keep examples self-contained
5. Update this README

---

## License

These examples are provided for educational purposes. Each framework has its own license - please check the respective framework documentation.

---

## Summary

Each framework has unique strengths:

### Core Evaluation
- **Need RAG evaluation?** → RAGAS, ARES, or RAGalyst
- **Want maximum flexibility?** → Claude
- **General LLM evaluation?** → DeepEval or OpenAI Evals
- **Testing in CI/CD?** → DeepEval or MLflow
- **Want quick setup?** → Arize Phoenix

### Specialized
- **Agent evaluation?** → Google ADK or MCPEval
- **Tool/function calling?** → MCPEval
- **Pipeline optimization?** → RAGalyst
- **Synthetic data generation?** → ARES

### Production & MLOps
- **Need observability?** → Langfuse, TruLens, LangSmith, or Weave
- **Prompt management?** → Humanloop, Langfuse, or LangSmith
- **ML lifecycle tracking?** → MLflow or Weave
- **Cost tracking?** → Langfuse, LangSmith, or Weave
- **Experiment tracking?** → Weave, Braintrust, or MLflow
- **Human feedback?** → Humanloop, Langfuse, or LangSmith
- **A/B testing?** → Humanloop, Braintrust, or Weave
- **Best DX?** → Braintrust or Weave

### Platform-Specific
- **Using LangChain?** → LangSmith or Langfuse
- **On GCP?** → Vertex AI or Google ADK
- **Need CLI tools?** → Google ADK or OpenAI Evals

**Pro Tip**: Start with one framework that matches your primary use case, then expand to others as needed. Many teams use 2-3 frameworks in combination.

### Popular Combinations

1. **RAG System**: RAGAS (metrics) + Langfuse (production monitoring) + RAGalyst (optimization)
2. **Agent System**: Google ADK (agent eval) + MCPEval (tool evaluation) + Langfuse (observability)
3. **General LLM App**: DeepEval (testing) + MLflow (experiments) + Langfuse (production)
4. **Enterprise**: Vertex AI (evaluation) + Google ADK (agents) + Langfuse (monitoring)
5. **Experiment-Driven**: Weave (tracking) + Braintrust (evaluation) + Humanloop (feedback)
6. **Prompt Engineering**: Humanloop (human feedback) + Braintrust (A/B testing) + Weave (versioning)
7. **Fast Iteration**: Braintrust (evaluation) + Weave (experiments) + Humanloop (refinement)
