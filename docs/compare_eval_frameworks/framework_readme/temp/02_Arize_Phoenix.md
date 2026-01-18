# Arize Phoenix: OpenTelemetry-Native LLM Observability & Evals

**Type**: Observability Platform + Evaluation Library | **License**: Elastic License 2.0 (OSS) | **Year**: 2023

---

## Quick Overview

Arize Phoenix is an **observability-first platform** that combines production monitoring with LLM evaluation. Built on OpenTelemetry standards, it provides automatic tracing, span instrumentation, and a powerful UI for debugging LLM applications.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | Observability + Evaluation |
| **Setup Time** | ⚡ 10-15 minutes |
| **Learning Curve** | Moderate |
| **Dependencies** | OpenTelemetry, Phoenix Server |
| **Cost** | Free (OSS) + Cloud option |
| **Best For** | Production observability & debugging |

---

## Key Strengths

### ✅ Advantages

1. **OpenTelemetry Native**
   - Industry-standard instrumentation
   - Automatic trace collection
   - Span-level evaluation
   - Works with OTEL ecosystem

2. **Excellent Observability**
   - Real-time trace visualization
   - Interactive UI dashboard
   - Span timeline view
   - Token usage tracking
   - Latency analysis

3. **Auto-Instrumentation**
   - One-line setup for major frameworks
   - LangChain, LlamaIndex, OpenAI
   - DSPy, Bedrock, Vertex AI
   - Minimal code changes required

4. **Comprehensive Evals**
   - LLM-as-judge evaluators
   - Code-based metrics
   - RAG-specific evaluators
   - Custom template support

5. **Local-First Development**
   - Run Phoenix server locally
   - No cloud dependency for dev
   - Export data for analysis
   - Privacy-friendly

6. **Production Ready**
   - Cloud-hosted option available
   - Scales to high volumes
   - Team collaboration features
   - Persistent storage

### ⚠️ Limitations

1. **Server Requirement**
   - Must run Phoenix server
   - Additional infrastructure overhead
   - More complex deployment

2. **OpenTelemetry Complexity**
   - Steeper learning curve
   - OTEL configuration can be tricky
   - More moving parts

3. **Resource Usage**
   - Server consumes memory/CPU
   - Storage for traces grows quickly
   - Network overhead for tracing

4. **UI-Centric**
   - Less suitable for programmatic workflows
   - Better for interactive debugging
   - Not ideal for CI/CD pipelines

---

## vs Other Frameworks

### vs Custom-Evals
| Aspect | Phoenix | Custom-Evals |
|--------|---------|--------------|
| **Observability** | Excellent | Basic |
| **Server Required** | Yes | No |
| **Setup Complexity** | Higher | Lower |
| **UI Dashboard** | Built-in | External |
| **Dependencies** | More | Minimal |
| **Tracing** | Core feature | Optional |

**Choose Phoenix if**: Observability and debugging are priorities
**Choose Custom-Evals if**: You want lightweight without server overhead

---

### vs LangSmith
| Aspect | Phoenix | LangSmith |
|--------|---------|-----------|
| **Open Source** | ✅ Yes | ❌ No |
| **Cloud Hosting** | Optional | Required |
| **OTEL Native** | ✅ Yes | ⚠️ Limited |
| **Framework Lock-in** | None | LangChain |
| **Cost** | Free (self-host) | Paid tiers |

**Choose Phoenix if**: You want OSS observability with OTEL
**Choose LangSmith if**: Heavy LangChain usage and prefer managed service

---

### vs TruLens
| Aspect | Phoenix | TruLens |
|--------|---------|---------|
| **OTEL Support** | Native | Limited |
| **UI Quality** | Modern | Functional |
| **Setup** | Simpler | More complex |
| **RAG Focus** | Balanced | Heavy |
| **Intermediate Steps** | Yes | Excellent |

**Choose Phoenix if**: You want OTEL-native with clean UI
**Choose TruLens if**: Deep RAG chain inspection is critical

---

### vs Langfuse
| Aspect | Phoenix | Langfuse |
|--------|---------|----------|
| **Self-Hosting** | Easier | More complex |
| **OTEL Native** | Yes | No (custom) |
| **Prompt Management** | Limited | Excellent |
| **Analytics** | Good | Better |
| **Learning Curve** | Moderate | Steeper |

**Choose Phoenix if**: You want OTEL standard and simpler setup
**Choose Langfuse if**: You need advanced prompt management

---

## When to Choose Phoenix

### ✅ Perfect For

1. **Production Observability**
   - Monitor LLM applications in real-time
   - Debug production issues
   - Track performance metrics
   - Identify bottlenecks

2. **OpenTelemetry Environments**
   - Already using OTEL
   - Need standard instrumentation
   - Want ecosystem compatibility
   - Multi-service architectures

3. **Team Collaboration**
   - Share traces with team
   - Interactive debugging sessions
   - Visual exploration of traces
   - Stakeholder demos

4. **RAG & Agent Systems**
   - Multi-step workflows
   - Complex retrieval pipelines
   - Agent decision tracking
   - Context relevance evaluation

5. **Development & Testing**
   - Local Phoenix server
   - Iterate on prompts
   - Test different models
   - Compare responses

### ❌ Not Ideal For

1. **Serverless Constraints**
   - Cannot run Phoenix server
   - Very resource-constrained
   - Prefer stateless evaluation

2. **Simple Batch Evaluation**
   - Just need eval scores
   - No need for UI
   - Prefer programmatic only

3. **CI/CD Pipelines**
   - Need lightweight testing
   - No UI interaction
   - Fast feedback loops

4. **Minimal Dependencies**
   - Want zero infrastructure
   - Avoid server management
   - Edge deployments

---

## Pricing

### Cost Breakdown

| Component | Self-Hosted | Arize Cloud |
|-----------|-------------|-------------|
| **Phoenix Software** | 💰 **Free** | - |
| **Infrastructure** | Your compute costs | Included |
| **Storage** | Your storage costs | Included |
| **Support** | Community | Enterprise |
| **Team Features** | Limited | Full |

### Self-Hosted Monthly Costs

| Traces/Month | Storage | Compute | Total Estimate |
|--------------|---------|---------|----------------|
| 10,000 | ~1 GB | Small VM | $10-20 |
| 100,000 | ~10 GB | Medium VM | $50-100 |
| 1,000,000 | ~100 GB | Large VM | $200-500 |

### Arize Cloud Pricing

Contact Arize for enterprise pricing. Typically starts at:
- **Starter**: Free tier available
- **Team**: $500-2,000/month
- **Enterprise**: Custom pricing

**Note**: Self-hosted is completely free, you only pay for infrastructure

---

## Quick Start

### Installation

```bash
# Install Phoenix
pip install arize-phoenix

# With OpenAI support
pip install arize-phoenix[openai]

# With evals
pip install arize-phoenix[evals]

# Full installation
pip install 'arize-phoenix[openai,evals,llama-index,langchain]'
```

### Start Phoenix Server

```python
import phoenix as px

# Launch Phoenix in notebook
session = px.launch_app()

# Or launch in background
px.launch_app(port=6006)
```

### Auto-Instrumentation (LangChain)

```python
from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Setup OTEL
endpoint = "http://127.0.0.1:6006/v1/traces"
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter(endpoint))
)

# Auto-instrument LangChain
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

# Now all LangChain calls are automatically traced!
from langchain.chains import LLMChain
from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9)
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run("What is LLM observability?")
```

### Run Evaluations

```python
from phoenix.evals import (
    OpenAIModel,
    llm_classify,
    RelevanceEvaluator,
    HallucinationEvaluator
)

# Initialize model
model = OpenAIModel(model="gpt-4o-mini")

# Evaluate relevance
relevance_eval = RelevanceEvaluator(model)
result = relevance_eval.evaluate(
    input="What is the capital of France?",
    output="Paris is the capital of France.",
)

print(f"Relevance: {result.label} (score: {result.score})")

# Evaluate hallucination
hallucination_eval = HallucinationEvaluator(model)
result = hallucination_eval.evaluate(
    input="What is the capital of France?",
    output="Paris is the capital of France.",
    context="France is a country in Europe. Paris is its capital city."
)

print(f"Hallucination: {result.label}")
```

### Batch Evaluation from Traces

```python
import phoenix as px

# Get traces from Phoenix
client = px.Client()
df = px.active_session().get_spans_dataframe()

# Extract data
queries = df["attributes.input.value"].tolist()
responses = df["attributes.output.value"].tolist()

# Run batch evaluation
from phoenix.evals import llm_classify

results = llm_classify(
    dataframe=df,
    model=model,
    template=RelevanceEvaluator.template,
    rails=["relevant", "irrelevant"],
)

# Add results back to Phoenix
client.log_evaluations(results)
```

---

## Architecture Highlights

### Design Principles

1. **OpenTelemetry Native**: Built on industry standards
2. **Observability First**: Tracing is core, not optional
3. **Separation of Concerns**: Server, instrumentation, evals separate
4. **Extensible**: Custom evaluators and templates
5. **Local & Cloud**: Run anywhere

### Key Components

```
Phoenix Stack:
┌─────────────────────────────────────┐
│   Phoenix UI (React Dashboard)     │
│   - Trace visualization             │
│   - Span timeline                   │
│   - Evaluation results              │
└─────────────────────────────────────┘
              ↑
┌─────────────────────────────────────┐
│   Phoenix Server (Python)           │
│   - OTLP endpoint                   │
│   - Trace storage                   │
│   - Query API                       │
└─────────────────────────────────────┘
              ↑
┌─────────────────────────────────────┐
│   OpenTelemetry SDK                 │
│   - Auto-instrumentation            │
│   - Span creation                   │
│   - Context propagation             │
└─────────────────────────────────────┘
              ↑
┌─────────────────────────────────────┐
│   Your LLM Application              │
│   - LangChain, LlamaIndex, etc.     │
│   - Custom code                     │
└─────────────────────────────────────┘
```

### Instrumentation Libraries

```python
# Available instrumentations
openinference.instrumentation.langchain
openinference.instrumentation.llama_index
openinference.instrumentation.openai
openinference.instrumentation.dspy
openinference.instrumentation.bedrock
openinference.instrumentation.vertexai
```

---

## Advanced Features

### 1. Custom Evaluators

```python
from phoenix.evals import OpenAIModel
from phoenix.evals.templates import ClassificationTemplate

# Define custom template
custom_template = ClassificationTemplate(
    rails=["accurate", "inaccurate"],
    template="""
Given the query and response, determine if the response is factually accurate.

Query: {input}
Response: {output}
Reference: {reference}

Classify as: accurate or inaccurate
""",
)

# Use in evaluation
model = OpenAIModel(model="gpt-4o-mini")
results = llm_classify(
    dataframe=df,
    template=custom_template,
    model=model,
)
```

### 2. Span-Level Evaluation

```python
from opentelemetry import trace

# Evaluate specific spans
client = px.Client()
spans_df = client.get_spans_dataframe()

# Filter to specific span types
llm_spans = spans_df[spans_df["span_kind"] == "LLM"]

# Evaluate just LLM outputs
results = llm_classify(
    dataframe=llm_spans,
    model=model,
    template=template,
)
```

### 3. Export & Analysis

```python
# Export traces to DataFrame
df = px.active_session().get_spans_dataframe()

# Export to Parquet
df.to_parquet("traces.parquet")

# Analysis with pandas
import pandas as pd

# Average latency by span type
latency_by_type = df.groupby("span_kind")["latency_ms"].mean()

# Token usage
total_tokens = df["attributes.llm.token_count.total"].sum()
```

---

## Integration Examples

### OpenAI Direct

```python
from openinference.instrumentation.openai import OpenAIInstrumentor

OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)
# Automatically traced!
```

### LlamaIndex

```python
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor

LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)

from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What is AI?")
# Automatically traced with retrieval steps!
```

### DSPy

```python
from openinference.instrumentation.dspy import DSPyInstrumentor

DSPyInstrumentor().instrument(tracer_provider=tracer_provider)

import dspy

dspy.settings.configure(lm=lm)
module = MyDSPyModule()
result = module(input="question")
# All DSPy steps traced!
```

---

## Comparison Summary

### Unique Advantages
1. 🔭 Best-in-class observability
2. 📊 OpenTelemetry native
3. 🎨 Modern, intuitive UI
4. 🔌 One-line auto-instrumentation
5. 🏠 Local-first development
6. 🔓 Open source (self-hostable)

### Trade-offs
1. Server infrastructure required
2. More complex setup than lightweight tools
3. Resource overhead for tracing
4. Learning curve for OTEL concepts

---

## Real-World Use Cases

### 1. Production Monitoring
```python
# Track all production LLM calls
# Identify slow queries
# Monitor token usage
# Alert on errors
```

### 2. Prompt Engineering
```python
# Compare different prompts
# Visualize response quality
# Track version performance
# A/B test prompts
```

### 3. RAG Debugging
```python
# Inspect retrieved documents
# Evaluate context relevance
# Track retrieval latency
# Debug poor responses
```

### 4. Agent Development
```python
# Visualize agent decision tree
# Track tool usage
# Evaluate reasoning steps
# Optimize agent flow
```

---

## Resources

### Documentation
- **Official Docs**: https://docs.arize.com/phoenix/
- **GitHub**: https://github.com/Arize-ai/phoenix
- **Quickstart**: https://docs.arize.com/phoenix/quickstart
- **API Reference**: https://docs.arize.com/phoenix/api/

### Papers & Research
- **OpenInference Spec**: https://github.com/Arize-ai/openinference
- **OTEL Semantic Conventions**: https://opentelemetry.io/docs/

### Examples
- **Example Notebooks**: https://github.com/Arize-ai/phoenix/tree/main/tutorials
- **LangChain Integration**: https://docs.arize.com/phoenix/tracing/integrations-tracing/langchain
- **LlamaIndex Integration**: https://docs.arize.com/phoenix/tracing/integrations-tracing/llamaindex

### Community
- **GitHub Issues**: https://github.com/Arize-ai/phoenix/issues
- **Slack Community**: https://arize-ai.slack.com/
- **YouTube Tutorials**: https://www.youtube.com/@ArizeAI

---

## Verdict

**Phoenix is the best choice for teams prioritizing observability, using OpenTelemetry, and wanting a powerful UI for debugging LLM applications.**

**Rating**: ⭐⭐⭐⭐⭐ (5/5 for observability)

### Choose Phoenix if you value:
- ✅ Production observability
- ✅ OpenTelemetry native
- ✅ Beautiful UI dashboard
- ✅ Auto-instrumentation
- ✅ Open source option

### Choose alternatives if you need:
- ❌ Zero infrastructure → Custom-Evals
- ❌ Managed cloud service → LangSmith
- ❌ Lighter weight → Custom-Evals, UpTrain
- ❌ CI/CD integration → DeepEval

---

**Next**: [Compare All Frameworks](Compare_All_Eval_Frameworks.md) | [Try Custom-Evals](01_Custom_Evals.md)
