# Langfuse: Production LLM Observability & Evaluation Platform

**Type**: Cloud Platform + Open Source | **License**: MIT (Self-hosted) / Commercial (Cloud) | **Year**: 2023

---

## Quick Overview

Langfuse is an **open-source** LLM observability and evaluation platform with a focus on production monitoring, prompt management, and cost tracking. Unlike vendor-locked solutions, Langfuse offers both cloud and self-hosted options with full feature parity.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | Production observability + evaluation |
| **Setup Time** | 10-20 minutes (Cloud) / 30-60 minutes (Self-hosted) |
| **Learning Curve** | Medium (Easy with decorators) |
| **Dependencies** | Cloud or Docker (self-hosted) |
| **Cost** | Free tier (50K obs) + Paid tiers / Self-hosted (free) |
| **Best For** | Production monitoring, cost tracking, open-source first |

---

## Key Strengths

### ✅ Advantages

1. **Open Source with Full Features**
   - MIT licensed core platform
   - Self-hostable with Docker
   - No feature restrictions in OSS version
   - Community-driven development
   - Transparent roadmap

2. **Best-in-Class Cost Tracking**
   - Automatic cost calculation per model
   - Token usage tracking
   - Cost breakdown by user, session, tag
   - Budget alerts and monitoring
   - Cost optimization insights
   - Historical cost trends

3. **Production Observability**
   - End-to-end trace visualization
   - Real-time monitoring dashboard
   - Latency tracking per component
   - Error tracking and debugging
   - Search and filter traces
   - Custom metadata and tags
   - Session-based grouping

4. **Prompt Management & Versioning**
   - Centralized prompt library
   - Version control for prompts
   - A/B test different versions
   - Track performance by version
   - Roll back to previous versions
   - Prompt variables and templates
   - Integration with code via API

5. **Multi-Framework Support**
   - Framework-agnostic design
   - Native integrations: LangChain, LlamaIndex, LiteLLM
   - OpenTelemetry support
   - Direct API for any framework
   - Python and JavaScript SDKs
   - REST API for any language

6. **Human-in-the-Loop Features**
   - User feedback collection (thumbs up/down)
   - Custom scoring and annotations
   - Manual review queues
   - Feedback aggregation and analysis
   - Comment threads on traces
   - Collaborative evaluation

7. **Dataset & Evaluation Management**
   - Dataset creation and versioning
   - Experiment tracking
   - A/B testing support
   - LLM-as-judge evaluators
   - Code-based evaluators
   - Batch evaluation runs
   - Performance comparisons

8. **Developer Experience**
   - Simple decorator-based tracing (`@observe`)
   - Automatic instrumentation
   - Clean Python API
   - Rich UI with filtering
   - API for programmatic access
   - Comprehensive documentation

### ⚠️ Limitations

1. **Learning Curve**
   - More concepts to learn than simple libraries
   - Requires understanding of tracing/observability
   - Self-hosting requires DevOps knowledge

2. **Cloud Dependency (Cloud Version)**
   - Hosted traces sent to Langfuse servers
   - Data privacy considerations
   - Network latency for trace ingestion
   - (Mitigated by self-hosting option)

3. **Resource Requirements (Self-hosted)**
   - Requires PostgreSQL database
   - Redis for queuing
   - Docker/Kubernetes setup
   - Maintenance overhead

4. **Smaller Ecosystem**
   - Newer than LangSmith
   - Fewer third-party integrations
   - Smaller community (growing rapidly)

---

## vs Other Frameworks

### vs LangSmith

| Aspect | Langfuse | LangSmith |
|--------|----------|-----------|
| **Open Source** | ✅ Yes (MIT) | ❌ No |
| **Self-Hosted** | ✅ Free | ❌ Enterprise only |
| **Cost Tracking** | Excellent | Good |
| **Framework Focus** | Framework-agnostic | LangChain-first |
| **Pricing (Cloud)** | Starts $59/month (Hobby) | Starts $39/user/month |
| **Free Tier** | 50K observations | 5K traces |
| **Prompt Management** | Built-in | Built-in |
| **Dataset Management** | Good | Excellent |
| **Community** | Growing (OSS) | Large (LangChain) |
| **Vendor Lock-in** | None (can self-host) | Yes |

**Choose Langfuse if**: You want open-source, self-hosting option, or framework-agnostic approach
**Choose LangSmith if**: You're deeply invested in LangChain and want managed solution

---

### vs Custom-Evals

| Aspect | Langfuse | Custom-Evals |
|--------|----------|--------------|
| **Infrastructure** | Platform (cloud/self-hosted) | None required |
| **Observability** | Comprehensive | Optional (via Phoenix) |
| **Dashboard** | Built-in (rich UI) | External tools |
| **Cost Tracking** | Automatic | Manual |
| **Dataset Storage** | Cloud/database | User-managed |
| **Prompt Management** | Built-in | None |
| **Learning Curve** | Medium | Easy |
| **Dependencies** | Platform | Minimal |
| **Flexibility** | Medium | High |
| **Setup Effort** | More | Less |

**Choose Langfuse if**: You need production observability with UI and cost tracking
**Choose Custom-Evals if**: You want lightweight, no infrastructure, maximum flexibility

---

### vs Braintrust

| Aspect | Langfuse | Braintrust |
|--------|----------|-----------|
| **Open Source** | ✅ Yes | ❌ No |
| **Self-Hosted** | ✅ Yes | ❌ No |
| **Developer DX** | Good | Excellent |
| **Cost Tracking** | Excellent | Good |
| **CI/CD Integration** | Good | Excellent |
| **Free Tier** | 50K observations | 10K evaluations |
| **Pricing (Paid)** | $59/month | $100/month |
| **Automatic Versioning** | Manual | Automatic |
| **Prompt Management** | Built-in | Built-in |
| **Dataset Management** | Good | Excellent |

**Choose Langfuse if**: You want open-source, self-hosting, or lower pricing
**Choose Braintrust if**: You prioritize developer experience and automatic versioning

---

### vs Arize Phoenix

| Aspect | Langfuse | Arize Phoenix |
|--------|----------|---------------|
| **Type** | Cloud + OSS platform | OSS + Enterprise |
| **Deployment** | Cloud or self-hosted | Local server or cloud |
| **Setup Complexity** | Medium | Medium |
| **Cost Tracking** | Excellent | Basic |
| **Prompt Management** | Built-in | None |
| **Dataset Management** | Built-in | External |
| **Evaluation** | Integrated | Separate package |
| **Human Feedback** | UI-based | API-based |
| **ML Scope** | LLM-focused | Broader ML |
| **Free Tier (Cloud)** | 50K observations | N/A (OSS only) |

**Choose Langfuse if**: You want integrated platform with prompt management and cost tracking
**Choose Arize Phoenix if**: You want broader ML monitoring or prefer local-first approach

---

## When to Choose Langfuse

### ✅ Perfect For

1. **Production LLM Applications**
   - Need comprehensive observability
   - Real-time monitoring requirements
   - Cost tracking and optimization
   - Error detection and debugging
   - Performance monitoring

2. **Teams Valuing Open Source**
   - Want to self-host
   - Need data sovereignty
   - Want to avoid vendor lock-in
   - Prefer transparent development
   - Need to modify/extend platform

3. **Multi-Framework Environments**
   - Using multiple LLM frameworks
   - Framework-agnostic approach
   - Need consistent monitoring across all systems
   - Want flexibility to switch frameworks

4. **Cost-Conscious Organizations**
   - Need detailed cost tracking
   - Optimizing LLM expenses
   - Multiple users needing access
   - Want lower per-user costs
   - Self-hosting to eliminate cloud costs

5. **Prompt Engineering Teams**
   - Active prompt experimentation
   - Need version control
   - A/B testing prompts
   - Track performance by prompt
   - Collaborative prompt development

6. **Human Feedback Workflows**
   - Collecting user feedback
   - Manual quality review
   - Annotation and scoring
   - Continuous improvement loops
   - Team collaboration on evaluation

### ❌ Not Ideal For

1. **Simple Evaluation Needs**
   - Lightweight evaluation sufficient
   - No need for observability platform
   - Consider: Custom-Evals, RAGAS

2. **Zero Infrastructure Requirement**
   - Cannot use cloud services
   - Cannot self-host
   - Consider: Custom-Evals (no infrastructure)

3. **Heavy LangChain Integration**
   - 100% LangChain-based
   - Want deepest LangChain integration
   - Consider: LangSmith

4. **Automatic Versioning Priority**
   - Need automatic dataset versioning
   - Want zero-config versioning
   - Consider: Braintrust, Weave

---

## Pricing

### Cloud Pricing Tiers (2026)

| Tier | Price | Observations | Users | Retention | Best For |
|------|-------|--------------|-------|-----------|----------|
| **Free** | $0 | 50,000/month | Unlimited | 30 days | Individuals, prototypes |
| **Hobby** | $59/month | 200,000/month | Unlimited | 3 months | Small teams, side projects |
| **Pro** | $499/month | 2M/month | Unlimited | 12 months | Growing teams, production |
| **Team** | Custom | Custom | Unlimited | Custom | Large teams, enterprises |

### Self-Hosted Option

| Tier | Price | Features | Support |
|------|-------|----------|---------|
| **Self-Hosted** | **FREE** | All features | Community |
| **Enterprise Support** | Custom | All features | Dedicated support + SLA |

### Additional Details

**What counts as an observation?**
- 1 trace = 1 observation
- Nested spans don't count separately
- Generations (LLM calls) are part of traces

**Included in all tiers:**
- Unlimited users
- Full prompt management
- Dataset management
- Human feedback collection
- API access
- All core features

### Cost Comparison Examples

**Example 1: Small Team (100K observations/month)**
- **Langfuse Free**: $0 (if under 50K)
- **Langfuse Hobby**: $59/month
- **LangSmith Plus (3 users)**: $117/month + trace costs
- **Braintrust**: Likely free tier

**Example 2: Medium Team (500K observations/month)**
- **Langfuse Pro**: $499/month (unlimited users)
- **LangSmith Plus (10 users)**: $390/month + ~$225 trace costs = ~$615/month
- **Braintrust**: ~$100/month + overages

**Example 3: Self-Hosted (Any scale)**
- **Langfuse**: $0 (infrastructure costs only)
- **LangSmith**: Not available
- **Braintrust**: Not available

### Typical Monthly Costs

| Usage Level | Cloud Cost | Self-Hosted Cost |
|-------------|------------|------------------|
| **< 50K obs** | $0 (Free tier) | Infrastructure only (~$20-50) |
| **200K obs** | $59 (Hobby) | Infrastructure only (~$50-100) |
| **2M obs** | $499 (Pro) | Infrastructure only (~$100-300) |
| **10M+ obs** | Custom (Team) | Infrastructure only (~$300-1000) |

**Note**: Self-hosted costs depend on infrastructure (AWS, GCP, on-premise)

---

## Quick Start

### Cloud Setup (5 Minutes)

```bash
# Install Langfuse SDK
pip install langfuse

# Install with specific integrations
pip install langfuse langchain  # For LangChain
pip install langfuse openai     # For OpenAI
pip install langfuse litellm    # For LiteLLM
```

### Configuration

```python
import os
from langfuse import Langfuse

# Set environment variables
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"  # or your self-hosted URL

# Initialize client
langfuse = Langfuse()
print("✓ Connected to Langfuse")
```

### Basic Tracing Example

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Create a trace
trace = langfuse.trace(
    name="qa_pipeline",
    user_id="user_123",
    metadata={"environment": "production"}
)

# Add LLM generation
generation = trace.generation(
    name="answer_question",
    model="gpt-4o-mini",
    model_parameters={"temperature": 0.7},
    input="What is machine learning?",
    output="Machine learning is a subset of AI that learns from data.",
    usage={"prompt_tokens": 10, "completion_tokens": 15}
)

# Add evaluation score
generation.score(
    name="quality",
    value=0.95,
    comment="High quality, accurate response"
)

print("✓ Trace logged to Langfuse")
```

### Decorator-Based Tracing (Recommended)

```python
from langfuse.decorators import observe, langfuse_context

@observe()
def retrieve_documents(query: str):
    """Automatically traced function."""
    docs = ["Doc 1", "Doc 2", "Doc 3"]
    langfuse_context.update_current_observation(
        output={"documents": docs}
    )
    return docs

@observe()
def generate_answer(query: str, docs: list):
    """Another traced function."""
    answer = f"Answer based on {len(docs)} documents"
    langfuse_context.update_current_observation(
        model="gpt-4",
        input={"query": query, "docs": docs},
        output=answer
    )
    return answer

@observe()
def qa_pipeline(query: str):
    """Main pipeline - nested traces automatically handled."""
    docs = retrieve_documents(query)
    answer = generate_answer(query, docs)
    return answer

# Use normally - tracing happens automatically
result = qa_pipeline("What is AI?")
```

### LangChain Integration

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langfuse.callback import CallbackHandler

# Initialize Langfuse callback
langfuse_handler = CallbackHandler()

# Create chain
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer this question: {question}"
)
chain = LLMChain(llm=llm, prompt=prompt)

# Run with automatic tracing
result = chain.run(
    question="What is quantum computing?",
    callbacks=[langfuse_handler]
)

print("✓ Chain execution traced in Langfuse")
```

---

## Self-Hosted Setup

### Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/langfuse/langfuse.git
cd langfuse

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Start services
docker-compose up -d

# Access at http://localhost:3000
```

### Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  langfuse-server:
    image: langfuse/langfuse:latest
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/langfuse
      NEXTAUTH_URL: http://localhost:3000
      NEXTAUTH_SECRET: your-secret-key
      SALT: your-salt-key
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: langfuse
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Kubernetes Deployment

```yaml
# Available via Helm chart
helm repo add langfuse https://langfuse.github.io/langfuse-helm
helm install langfuse langfuse/langfuse

# Or use official Kubernetes manifests
kubectl apply -f https://raw.githubusercontent.com/langfuse/langfuse/main/k8s/deployment.yaml
```

---

## Key Features Deep Dive

### 1. Cost Tracking

**Automatic Cost Calculation:**
```python
trace = langfuse.trace(name="cost_tracking")

generation = trace.generation(
    name="gpt4_call",
    model="gpt-4",
    usage={
        "prompt_tokens": 1000,
        "completion_tokens": 500,
        "total_tokens": 1500
    }
)

# Langfuse automatically calculates costs based on model pricing
# View in dashboard:
# - Cost per trace
# - Cost per user
# - Cost per tag
# - Cost trends over time
```

**Cost Analytics:**
- Real-time cost monitoring
- Budget alerts
- Cost breakdown by model, user, session
- Historical trends
- Optimization recommendations
- Export for billing

### 2. Prompt Management

**Create and Version Prompts:**
```python
# Via UI or API
langfuse.create_prompt(
    name="qa_system_prompt",
    prompt="Answer the question: {{question}}",
    version=1,
    metadata={"created_by": "team_lead"}
)

# Fetch in code
prompt = langfuse.get_prompt("qa_system_prompt", version=2)
filled_prompt = prompt.compile(question="What is AI?")

# Use with LLM
response = llm.generate(filled_prompt)

# Track which prompt version was used
trace.generation(
    prompt=prompt,
    output=response
)
```

**Features:**
- Version control
- A/B testing
- Performance tracking per version
- Roll back to previous versions
- Collaborative editing
- Variables and templates

### 3. Human Feedback

**Collect User Feedback:**
```python
# User provides feedback (thumbs up/down)
generation.score(
    name="user_feedback",
    value=1.0,  # 1.0 = positive, 0.0 = negative
    comment="Very helpful response"
)

# Add detailed annotations
trace.update(
    metadata={
        "user_comment": "Great explanation!",
        "feedback_type": "positive"
    }
)
```

**Feedback Workflows:**
- Annotation queues in UI
- Manual review and scoring
- Team collaboration
- Feedback aggregation
- Performance tracking based on feedback

### 4. Dataset Management

**Create Evaluation Datasets:**
```python
# Create dataset
dataset = langfuse.create_dataset(
    name="qa_benchmark",
    description="Quality assurance test set"
)

# Add examples
dataset.create_item(
    input={"question": "What is AI?"},
    expected_output="Artificial Intelligence",
    metadata={"category": "definitions"}
)

# Run evaluation
for item in dataset.items:
    result = qa_system(item.input)

    # Link result to dataset
    langfuse.trace(
        name="evaluation_run",
        dataset_item=item,
        output=result
    )
```

### 5. Session Tracking

**Track Multi-Turn Conversations:**
```python
session_id = "session_abc123"

# Turn 1
trace1 = langfuse.trace(
    name="turn_1",
    session_id=session_id,
    user_id="user_456"
)
trace1.generation(
    input="Hello",
    output="Hi! How can I help?"
)

# Turn 2
trace2 = langfuse.trace(
    name="turn_2",
    session_id=session_id,
    user_id="user_456"
)
trace2.generation(
    input="What is ML?",
    output="Machine learning is..."
)

# View entire session in UI grouped together
```

---

## Architecture Highlights

### System Architecture

```
Langfuse Platform
├── Web Application (Next.js)
│   ├── Dashboard & Analytics
│   ├── Trace Explorer
│   ├── Prompt Management
│   ├── Dataset Management
│   └── User Management
│
├── API Server
│   ├── Ingestion API (traces, events)
│   ├── Query API (dashboard)
│   ├── Prompt API
│   └── Dataset API
│
├── Database (PostgreSQL)
│   ├── Traces & Observations
│   ├── Prompts & Versions
│   ├── Datasets & Items
│   └── Users & Organizations
│
├── Queue (Redis)
│   ├── Async processing
│   ├── Cost calculations
│   └── Aggregations
│
└── SDKs
    ├── Python SDK
    ├── JavaScript SDK
    └── REST API
```

### Integration Architecture

```
Your Application
        │
        ├── Direct SDK
        │   └── langfuse.trace()
        │
        ├── Decorators
        │   └── @observe()
        │
        ├── LangChain
        │   └── CallbackHandler
        │
        ├── LlamaIndex
        │   └── LlamaIndexCallback
        │
        ├── OpenAI SDK
        │   └── observeOpenAI()
        │
        └── OpenTelemetry
                │
                └── Langfuse Platform
                        │
                        ├── Trace Storage
                        ├── Cost Calculation
                        ├── Analytics
                        └── UI/API Access
```

---

## Comparison Summary

### Unique Advantages
1. ⚡ Open source with full self-hosting option (MIT license)
2. 💰 Best-in-class cost tracking and analytics
3. 🔓 No vendor lock-in (can self-host entirely)
4. 🎯 Framework-agnostic design
5. 📝 Built-in prompt management and versioning
6. 👥 Unlimited users on all tiers
7. 🆓 Generous free tier (50K observations)
8. 🛠️ Self-hosted option is completely free

### Trade-offs
1. Requires platform setup (cloud or self-hosted)
2. Learning curve for observability concepts
3. Self-hosting requires infrastructure management
4. Smaller ecosystem than LangSmith

---

## Best Practices

### 1. Tracing Strategy
```python
# Use decorators for automatic tracing
@observe()
def my_function():
    pass

# Add context with metadata
@observe(metadata={"team": "research"})
def research_task():
    pass

# Update during execution
langfuse_context.update_current_observation(
    output=result,
    metadata={"quality": "high"}
)
```

### 2. Cost Management
- Tag traces by feature/team for cost attribution
- Set up alerts for unusual spending
- Regular cost reviews
- Optimize based on cost analytics
- Use cheaper models where appropriate

### 3. Prompt Management
- Version all prompts centrally
- Test prompt changes before production
- Track performance by version
- Use A/B testing for optimization
- Document prompt changes

### 4. Dataset Management
- Maintain golden test sets
- Version datasets for reproducibility
- Regular dataset updates
- Use production data to enhance datasets
- Track performance over time

### 5. Team Collaboration
- Use tags for organization
- Set up annotation workflows
- Regular feedback review
- Share insights via dashboard
- Document evaluation criteria

---

## Migration Guide

### From LangSmith

```python
# LangSmith
from langsmith import Client, traceable

@traceable
def my_function():
    pass

# Langfuse
from langfuse.decorators import observe

@observe()
def my_function():
    pass
```

### From Custom Logging

```python
# Before: Custom logging
import logging
logging.info(f"LLM call: {prompt} -> {response}")

# After: Langfuse
from langfuse import Langfuse
langfuse = Langfuse()

trace = langfuse.trace(name="llm_call")
trace.generation(
    input=prompt,
    output=response,
    model="gpt-4",
    usage=usage
)
```

---

## Resources

### Documentation
- **Official Docs**: https://langfuse.com/docs
- **API Reference**: https://langfuse.com/docs/api
- **Self-Hosting Guide**: https://langfuse.com/docs/deployment/self-host
- **Cookbook**: https://langfuse.com/docs/cookbook

### Code Examples
- **GitHub Repository**: https://github.com/langfuse/langfuse
- **Example Projects**: https://github.com/langfuse/langfuse-examples
- **Integrations**: https://langfuse.com/docs/integrations

### Community
- **GitHub Discussions**: https://github.com/langfuse/langfuse/discussions
- **Discord**: https://discord.gg/7NXusRtqYU
- **Twitter**: @langfuse

### Video Tutorials
- Getting Started Guide
- Self-Hosting Tutorial
- Prompt Management Deep Dive
- Cost Optimization Strategies

---

## Verdict

**Langfuse is the best choice for teams wanting production-grade observability with the flexibility of open source, excellent cost tracking, and no vendor lock-in.**

**Rating**: ⭐⭐⭐⭐⭐ (5/5 for open source + cost tracking)

### Choose Langfuse if you value:
- ✅ Open source and self-hosting options
- ✅ Excellent cost tracking and analytics
- ✅ Framework-agnostic approach
- ✅ No vendor lock-in
- ✅ Unlimited users at all price points
- ✅ Built-in prompt management
- ✅ Production observability
- ✅ Generous free tier

### Choose alternatives if you need:
- ❌ Deepest LangChain integration → LangSmith
- ❌ Automatic versioning → Braintrust, Weave
- ❌ Zero infrastructure → Custom-Evals
- ❌ Best developer DX → Braintrust
- ❌ W&B integration → Weave

---

**Next**: [Compare Weave](16_Weave.md) | [Compare All Frameworks](Compare_All_Eval_Frameworks.md)

---

## Example Integration

See comprehensive code examples in [langfuse_example.py](langfuse_example.py)
