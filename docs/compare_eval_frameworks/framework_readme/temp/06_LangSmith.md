# LangSmith: Enterprise LLM Observability & Evaluation Platform

**Type**: Cloud Platform | **License**: Commercial (Freemium) | **Year**: 2023

---

## Quick Overview

LangSmith is LangChain's production-grade platform for **debugging, testing, evaluating, and monitoring** LLM applications. It provides best-in-class integration with LangChain/LangGraph while supporting other frameworks through OpenTelemetry.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | Production LLM observability + evaluation |
| **Setup Time** | 15-30 minutes |
| **Learning Curve** | Medium (Easy for LangChain users) |
| **Dependencies** | Cloud platform (or self-hosted) |
| **Cost** | Free tier (5K traces) + Paid tiers |
| **Best For** | LangChain apps, production monitoring |

---

## Key Strengths

### ✅ Advantages

1. **Best-in-Class LangChain Integration**
   - Native support for LangChain and LangGraph
   - Automatic tracing with `@traceable` decorator
   - Deep integration with LCEL (LangChain Expression Language)
   - First-class support for agents, chains, and tools
   - Zero-config tracing for LangChain apps

2. **Production Observability**
   - End-to-end request tracing
   - Token usage and cost tracking
   - Latency monitoring
   - Error tracking and debugging
   - Real-time dashboard
   - Search and filter traces

3. **Comprehensive Dataset Management**
   - Centralized dataset storage in cloud
   - Version control for test sets
   - CSV/JSON import/export
   - Dataset sharing across teams
   - Programmatic dataset creation
   - Dataset versioning and history

4. **Human-in-the-Loop Evaluation**
   - Annotation queues for manual review
   - Thumbs up/down feedback
   - Custom scoring rubrics
   - Team collaboration features
   - Feedback collection from production
   - Pairwise comparison UI

5. **Advanced A/B Testing**
   - Compare multiple models side-by-side
   - Experiment tracking and comparison
   - Statistical significance testing
   - Cost/latency/quality trade-off analysis
   - Automated regression detection
   - Historical performance tracking

6. **Flexible Evaluation System**
   - LLM-as-judge evaluators
   - Code-based custom evaluators
   - Composite evaluators
   - Pre-built evaluator templates
   - Evaluation on production data
   - Batch evaluation support

7. **Enterprise Features**
   - SOC 2 Type 2 compliant
   - HIPAA and GDPR compliant
   - SSO/SAML authentication
   - Role-based access control (RBAC)
   - Self-hosted deployment options
   - Dedicated support

8. **Multi-Framework Support**
   - Native: LangChain, LangGraph
   - OpenTelemetry: Anthropic, OpenAI, AutoGen, CrewAI
   - Framework-agnostic tracing
   - Custom instrumentation support

### ⚠️ Limitations

1. **Commercial Platform**
   - Free tier limited (5K traces/month)
   - Costs can scale with usage
   - Cloud dependency (unless self-hosted)
   - Vendor lock-in for datasets

2. **LangChain Bias**
   - Best features for LangChain ecosystem
   - Other frameworks require more setup
   - Documentation heavily LangChain-focused

3. **Learning Curve**
   - More complex than simple libraries
   - Requires understanding of platform concepts
   - Team onboarding needed

4. **Data Privacy Concerns**
   - Production data sent to cloud (unless self-hosted)
   - Requires trust in third-party service
   - May not suit highly regulated industries (without Enterprise)

---

## vs Other Frameworks

### vs Custom-Evals

| Aspect | LangSmith | Custom-Evals |
|--------|-----------|--------------|
| **Infrastructure** | Cloud platform required | None required |
| **Cost** | Platform + LLM | LLM only |
| **Observability** | Built-in, comprehensive | Optional (via Phoenix) |
| **Dataset Storage** | Cloud (managed) | User-managed |
| **LangChain Integration** | Native, seamless | Works but manual |
| **Learning Curve** | Medium | Easy |
| **Vendor Lock-in** | Yes (datasets, traces) | None |
| **Human Feedback** | Built-in UI | External tools |
| **Production Monitoring** | Excellent | Basic |
| **Multi-Framework** | Via OpenTelemetry | Native (17+ frameworks) |

**Choose LangSmith if**: You use LangChain and need production observability
**Choose Custom-Evals if**: You want lightweight, vendor-independent evaluation

---

### vs TruLens

| Aspect | LangSmith | TruLens |
|--------|-----------|---------|
| **Focus** | Production + Evaluation | Observability + Evaluation |
| **Deployment** | Cloud or self-hosted | Local or cloud |
| **LangChain** | Native integration | Plugin-based |
| **Cost** | Freemium SaaS | Open source + optional cloud |
| **Human Feedback** | Built-in UI | Limited |
| **Enterprise** | Full support | Growing |
| **RAG Evaluation** | Good | Excellent |
| **Dataset Management** | Excellent | Basic |
| **A/B Testing** | Built-in | Manual |

**Choose LangSmith if**: You need managed platform with team collaboration
**Choose TruLens if**: You want open source with strong RAG evaluation

---

### vs Langfuse

| Aspect | LangSmith | Langfuse |
|--------|-----------|----------|
| **Origin** | LangChain team | Independent |
| **LangChain Focus** | Primary | Framework-agnostic |
| **Self-Hosted** | Enterprise only | Free (open source) |
| **Pricing** | $39/user/month | $59 flat (Hobby) |
| **Dataset Management** | Excellent | Good |
| **Evaluation** | Comprehensive | Good |
| **Human Feedback** | Built-in | Built-in |
| **A/B Testing** | Native | Via prompts |
| **Compliance** | SOC2, HIPAA, GDPR | SOC2, GDPR |
| **Community** | LangChain ecosystem | Growing independent |

**Choose LangSmith if**: You're deeply invested in LangChain
**Choose Langfuse if**: You want open-source option or multi-framework focus

---

### vs Arize Phoenix

| Aspect | LangSmith | Arize Phoenix |
|--------|-----------|---------------|
| **Type** | Cloud-first platform | Open source + enterprise |
| **Setup** | Cloud signup | Local server |
| **LangChain** | Native | Via OpenInference |
| **Cost** | Paid tiers | Free (self-host) |
| **Evaluation** | Built-in | Separate evals package |
| **Human Feedback** | UI-based | API-based |
| **Deployment** | Cloud/self-hosted | Local/cloud |
| **ML Monitoring** | LLM-focused | Broader ML scope |

**Choose LangSmith if**: You want managed SaaS with minimal setup
**Choose Arize Phoenix if**: You want open source with broader ML capabilities

---

## When to Choose LangSmith

### ✅ Perfect For

1. **LangChain/LangGraph Applications**
   - Using LangChain as primary framework
   - Complex agent applications
   - LCEL-based chains
   - Need seamless integration

2. **Production Monitoring**
   - Need real-time observability
   - Cost and latency tracking
   - Error monitoring
   - Performance optimization

3. **Team Collaboration**
   - Multiple developers
   - Shared datasets
   - Collaborative evaluation
   - Human-in-the-loop workflows

4. **Enterprise Requirements**
   - Compliance needs (SOC2, HIPAA, GDPR)
   - SSO/SAML authentication
   - Role-based access control
   - Dedicated support

5. **A/B Testing & Experimentation**
   - Comparing multiple models
   - Prompt versioning
   - Statistical analysis
   - Regression detection

6. **Dataset Management**
   - Centralized test sets
   - Version control for data
   - Team sharing
   - Historical tracking

### ❌ Not Ideal For

1. **Budget-Conscious Projects**
   - Free tier may be insufficient
   - Costs scale with usage
   - Consider open-source alternatives

2. **Non-LangChain Frameworks**
   - Better options for other frameworks
   - More setup required
   - Not leveraging core strengths

3. **Highly Regulated Industries**
   - Data sovereignty concerns
   - Unless using self-hosted Enterprise
   - May prefer fully self-hosted solutions

4. **Simple Evaluation Needs**
   - Platform may be overkill
   - Lighter libraries sufficient
   - No need for full observability

---

## Pricing

### Pricing Tiers (2026)

| Tier | Price | Traces/Month | Retention | Best For |
|------|-------|--------------|-----------|----------|
| **Developer (Free)** | $0 | 5,000 | 14 days | Personal projects, prototyping |
| **Plus** | $39/user/month | 10,000 | 14 days + extended | Small teams (up to 10 users) |
| **Enterprise** | Custom | Custom | Custom | Large teams, compliance needs |

### Additional Costs

| Item | Price | Notes |
|------|-------|-------|
| **Base Traces** | $0.50 per 1K | 14-day retention |
| **Extended Traces** | $5.00 per 1K | 400-day retention |
| **Trace Upgrade** | $4.50 per 1K | Upgrade base to extended |
| **LangSmith Deployment** | Included (Plus) | 1 free dev-sized deployment |

### Typical Monthly Costs

| Usage Level | Estimated Cost |
|-------------|----------------|
| **Individual (Free)** | $0 (up to 5K traces) |
| **Small Team (3 users)** | $117/month + traces |
| **Medium Team (10 users)** | $390/month + traces |
| **Large Team** | Custom (Enterprise) |

### Cost Comparison

**Example**: 50,000 traces/month with 3 users
- Base cost: $117 (3 x $39)
- Traces: $20 (40K additional traces x $0.50/1K)
- **Total**: ~$137/month

### Discounts Available
- Startup discounts for eligible companies
- Education discounts for academic institutions
- Non-profit pricing
- Annual commitment discounts

---

## Quick Start

### Installation

```bash
# Install LangSmith SDK
pip install langsmith

# Install with LangChain (recommended)
pip install langchain langsmith langchain-openai
```

### Setup (5 Minutes)

```python
import os
from langsmith import Client

# 1. Sign up at smith.langchain.com (free, no credit card)
# 2. Get API key from settings
# 3. Set environment variables

os.environ["LANGSMITH_API_KEY"] = "your-api-key"
os.environ["LANGSMITH_TRACING"] = "true"  # Enable tracing
os.environ["LANGSMITH_PROJECT"] = "my-project"  # Optional project name

# Initialize client
client = Client()
print("LangSmith connected!")
```

### Basic Evaluation Example

```python
from langsmith import Client, evaluate
from langsmith.evaluation import EvaluationResult
from langsmith.schemas import Example, Run

client = Client()

# 1. Create a dataset
dataset = client.create_dataset("qa-dataset")

# Add examples
client.create_example(
    inputs={"question": "What is the capital of France?"},
    outputs={"answer": "Paris"},
    dataset_id=dataset.id
)

# 2. Define your model/system
def qa_system(inputs: dict) -> dict:
    question = inputs["question"]
    # Your LLM call here
    answer = "Paris"  # Replace with actual LLM
    return {"answer": answer}

# 3. Create evaluator
def correctness_evaluator(run: Run, example: Example) -> EvaluationResult:
    predicted = run.outputs.get("answer", "")
    expected = example.outputs.get("answer", "")
    is_correct = predicted.lower() == expected.lower()

    return EvaluationResult(
        key="correctness",
        score=1.0 if is_correct else 0.0
    )

# 4. Run evaluation
results = evaluate(
    qa_system,
    data=dataset.name,
    evaluators=[correctness_evaluator],
    experiment_prefix="qa-eval"
)

print(f"Results: {results}")
```

### Automatic Tracing (LangChain)

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# No additional code needed - tracing is automatic!
llm = ChatOpenAI(model="gpt-4o-mini")

prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer this question: {question}"
)

chain = LLMChain(llm=llm, prompt=prompt)

# This will automatically appear in LangSmith dashboard
result = chain.run(question="What is machine learning?")
```

### Custom Function Tracing

```python
from langsmith import traceable

@traceable(name="custom-qa-system")
def my_qa_system(question: str) -> str:
    # Your custom logic here
    # Will be traced automatically
    return f"Answer to: {question}"

# Use normally - tracing happens automatically
answer = my_qa_system("What is AI?")
```

---

## Architecture Highlights

### Core Components

```
LangSmith Platform
├── Tracing & Observability
│   ├── Automatic instrumentation
│   ├── Request flow visualization
│   ├── Token/cost tracking
│   └── Error monitoring
│
├── Dataset Management
│   ├── Dataset storage & versioning
│   ├── Example management
│   ├── Import/export (CSV, JSON)
│   └── Team sharing
│
├── Evaluation System
│   ├── LLM-as-judge evaluators
│   ├── Code-based evaluators
│   ├── Composite evaluators
│   └── Batch evaluation
│
├── Human Feedback
│   ├── Annotation queues
│   ├── Scoring rubrics
│   ├── Pairwise comparison
│   └── Team collaboration
│
├── Experimentation
│   ├── A/B testing
│   ├── Prompt versioning
│   ├── Model comparison
│   └── Regression detection
│
└── Deployment
    ├── Agent servers
    ├── API endpoints
    ├── Scaling & load balancing
    └── Production monitoring
```

### Integration Architecture

```
Your Application
        │
        ├── LangChain/LangGraph (native)
        │   └── Automatic tracing
        │
        ├── Other Frameworks (OpenTelemetry)
        │   ├── Anthropic
        │   ├── OpenAI
        │   ├── AutoGen
        │   └── CrewAI
        │
        ├── Custom Functions (@traceable)
        │
        └── LangSmith SDK
                │
                ├── Trace data → Cloud/Self-hosted
                ├── Datasets → Centralized storage
                ├── Evaluations → Results & metrics
                └── Feedback → Annotation queues
```

---

## Key Features Deep Dive

### 1. Production Observability

**What You Get:**
- Full request traces with all intermediate steps
- Token usage and cost per request
- Latency breakdown by component
- Error tracking with stack traces
- Search and filter capabilities
- Real-time dashboard

**Use Cases:**
- Debug production issues
- Optimize costs
- Monitor performance
- Track error rates
- Understand user behavior

### 2. Dataset Management

**Capabilities:**
- Create datasets programmatically or via UI
- Import from CSV, JSON, or code
- Version control for test sets
- Share datasets across teams
- Clone and fork datasets
- Export for external use

**Best Practices:**
- Maintain golden datasets for regression testing
- Use versioning for experiments
- Share datasets for collaboration
- Regular dataset updates

### 3. Human-in-the-Loop Evaluation

**Features:**
- Annotation queues for manual review
- Custom scoring rubrics
- Thumbs up/down feedback
- Text comments
- Pairwise comparisons
- Inter-annotator agreement tracking

**Workflow:**
1. Production traces → Annotation queue
2. Team reviews and scores
3. Feedback used for evaluation
4. Results tracked over time

### 4. A/B Testing

**Capabilities:**
- Compare 2+ models/prompts
- Statistical significance testing
- Cost/latency/quality metrics
- Win rate calculation
- Historical comparison
- Automated alerts on regression

**Example Use Cases:**
- GPT-4 vs Claude comparison
- Prompt A vs Prompt B
- New model version validation
- Cost optimization testing

### 5. LLM-as-Judge Evaluation

**Built-in Evaluators:**
- Correctness
- Relevance
- Coherence
- Faithfulness (RAG)
- Helpfulness
- Harmlessness

**Custom Evaluators:**
```python
from langchain_openai import ChatOpenAI
from langsmith.evaluation import EvaluationResult

def custom_evaluator(run: Run, example: Example) -> EvaluationResult:
    llm = ChatOpenAI(model="gpt-4")

    prompt = f"""
    Evaluate this response on [criteria]:
    Input: {example.inputs}
    Output: {run.outputs}
    Expected: {example.outputs}

    Score 0.0-1.0:
    """

    score = float(llm.invoke(prompt).content)

    return EvaluationResult(
        key="custom_metric",
        score=score
    )
```

---

## Comparison Summary

### Unique Advantages
1. Best LangChain/LangGraph integration (seamless)
2. Enterprise-grade observability and monitoring
3. Comprehensive dataset management with versioning
4. Built-in human-in-the-loop evaluation UI
5. Advanced A/B testing and experimentation
6. Production-ready with compliance certifications
7. Managed deployment options

### Trade-offs
1. Commercial platform with usage-based costs
2. Optimized for LangChain (other frameworks require more effort)
3. Cloud dependency for most features
4. Vendor lock-in for datasets and traces
5. Learning curve for full feature utilization

---

## Migration Guide

### From Custom-Evals

```python
# Custom-Evals
from custom.evals import CoherenceEvaluator, LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(llm)
score = evaluator.evaluate({"output": response})

# LangSmith
from langsmith import Client, evaluate
from langsmith.evaluation import EvaluationResult

def coherence_evaluator(run: Run, example: Example) -> EvaluationResult:
    # Your coherence logic here
    return EvaluationResult(key="coherence", score=0.8)

results = evaluate(
    your_function,
    data="dataset-name",
    evaluators=[coherence_evaluator]
)
```

### From TruLens

```python
# TruLens
from trulens_eval import TruChain, Feedback
from trulens_eval.feedback import Groundedness

feedback = Feedback(groundedness_provider.groundedness)
tru_recorder = TruChain(chain, feedbacks=[feedback])

# LangSmith
from langsmith import traceable, evaluate

@traceable
def your_chain(inputs):
    # Your chain logic
    return outputs

# Evaluation happens via evaluate() function
results = evaluate(
    your_chain,
    data=dataset,
    evaluators=[groundedness_evaluator]
)
```

---

## Best Practices

### 1. Tracing Strategy
- Enable tracing selectively (not all environments)
- Use project names for organization
- Tag traces with metadata
- Set sampling rate for high-volume apps

### 2. Dataset Management
- Maintain versioned golden datasets
- Regular dataset updates with production examples
- Use descriptive names and tags
- Export datasets for backup

### 3. Evaluation Workflow
- Start with simple evaluators, add complexity
- Use LLM-as-judge for subjective criteria
- Combine multiple evaluators for comprehensive assessment
- Track evaluation metrics over time

### 4. Cost Management
- Monitor trace volume
- Use sampling for high-traffic apps
- Set up alerts for unusual usage
- Consider extended retention selectively

### 5. Team Collaboration
- Use projects to organize work
- Share datasets across team
- Leverage annotation queues
- Regular review of feedback

---

## Resources

### Documentation
- **Official Docs**: [docs.langchain.com/langsmith](https://docs.langchain.com/langsmith)
- **API Reference**: [python.langchain.com/docs/langsmith](https://python.langchain.com/docs/langsmith/)
- **Pricing Details**: [langchain.com/pricing](https://www.langchain.com/pricing)

### Examples
- Basic Evaluation: See quick start above
- LangChain Integration: [langsmith_eval_example.py](langsmith_eval_example.py)
- Advanced Workflows: [LangSmith docs](https://docs.langchain.com/langsmith)

### Community
- **GitHub**: [langchain-ai/langchain](https://github.com/langchain-ai/langchain)
- **Discord**: LangChain Discord server
- **Twitter**: [@LangChainAI](https://twitter.com/LangChainAI)

### Learning Resources
- LangSmith YouTube tutorials
- LangChain documentation
- Community blog posts
- Weekly office hours

---

## Verdict

**LangSmith is the best choice for teams using LangChain/LangGraph who need production-grade observability, comprehensive evaluation, and team collaboration features.**

**Rating**: ⭐⭐⭐⭐⭐ (5/5 for LangChain integration)

### Choose LangSmith if you value:
- ✅ Seamless LangChain/LangGraph integration
- ✅ Production monitoring and observability
- ✅ Managed dataset storage and versioning
- ✅ Human-in-the-loop evaluation UI
- ✅ Enterprise compliance and support
- ✅ Team collaboration features
- ✅ A/B testing and experimentation

### Choose alternatives if you need:
- ❌ Fully open source → TruLens, Custom-Evals
- ❌ Framework-agnostic focus → Langfuse, Custom-Evals
- ❌ Zero-cost solution → Custom-Evals, Phoenix
- ❌ Self-hosted by default → Langfuse (OSS)
- ❌ RAG-specific evaluation → RAGAS, TruLens

---

**Next**: [Compare All Frameworks](Compare_All_Eval_Frameworks.md) | [TruLens Comparison](09_TruLens.md)

---

## Sources

- [Plans and Pricing - LangChain](https://www.langchain.com/pricing)
- [LangGraph Pricing Guide - ZenML Blog](https://www.zenml.io/blog/langgraph-pricing)
- [The True Cost of LangSmith - MetaCTO](https://www.metacto.com/blogs/the-true-cost-of-langsmith-a-comprehensive-pricing-integration-guide)
- [LangSmith Pricing Plans - AgentsAPIs](https://agentsapis.com/langchain/langsmith-pricing/)
- [LangSmith Documentation](https://docs.langchain.com/langsmith)
