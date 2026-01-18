# TruLens: Deep RAG & Agent Observability with Evaluation

**Type**: Observability Platform + Evaluation Library | **License**: MIT (Open Source) | **Year**: 2020

---

## Quick Overview

TruLens (formerly TruEra) is an **observability and evaluation platform** specializing in RAG and agent applications. It provides deep instrumentation for intermediate steps, making it excellent for debugging complex AI workflows.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | RAG observability, intermediate steps |
| **Setup Time** | ⚡ 15-20 minutes |
| **Learning Curve** | Moderate to Steep |
| **Dependencies** | TruLens server, SQLite/Postgres |
| **Cost** | Free (OSS) + Enterprise option |
| **Best For** | RAG debugging, agent evaluation |

---

## Key Strengths

### ✅ Advantages

1. **Deep RAG Instrumentation**
   - Track every retrieval step
   - Evaluate context relevance
   - Groundedness checking
   - Answer relevance scoring
   - Context utilization analysis

2. **Intermediate Step Tracking**
   - Inspect agent reasoning
   - Tool usage monitoring
   - Chain-of-thought visibility
   - Multi-hop reasoning traces
   - Decision point analysis

3. **Comprehensive RAG Metrics**
   - **Context Relevance**: Retrieved docs quality
   - **Groundedness**: Response grounded in context
   - **Answer Relevance**: Response addresses query
   - **Hallucination Detection**: Identifies fabrications
   - Custom feedback functions

4. **Multi-Framework Support**
   - LangChain deep integration
   - LlamaIndex support
   - Custom apps via decorators
   - Framework-agnostic base

5. **Rich Dashboard**
   - Interactive UI
   - Trace visualization
   - Leaderboard comparisons
   - Metric trends over time
   - Export capabilities

6. **Feedback Functions**
   - LLM-based evaluators
   - Embedding similarity
   - Custom Python functions
   - Async evaluation
   - Flexible providers

### ⚠️ Limitations

1. **Complex Setup**
   - Steeper learning curve
   - More configuration needed
   - Decorator pattern can be confusing
   - Documentation scattered

2. **Performance Overhead**
   - Instrumentation adds latency
   - Database writes for every trace
   - Memory usage for long sessions
   - Can slow development

3. **RAG-Heavy Focus**
   - Optimized for RAG use cases
   - Agent support but less mature
   - General LLM eval less focus
   - May be overkill for simple cases

4. **Database Requirement**
   - SQLite or Postgres needed
   - Data management overhead
   - Backup/migration concerns
   - Can grow large quickly

5. **Limited Cloud Option**
   - Primarily self-hosted
   - Enterprise cloud available
   - No free cloud tier
   - More infrastructure work

6. **OTEL Support Limited**
   - Not OpenTelemetry native
   - Custom instrumentation
   - Less ecosystem compatibility
   - Migration friction

---

## vs Other Frameworks

### vs Phoenix
| Aspect | TruLens | Phoenix |
|--------|---------|---------|
| **OTEL Native** | ❌ No | ✅ Yes |
| **RAG Focus** | Stronger | Balanced |
| **UI Quality** | Good | Excellent |
| **Setup** | More complex | Simpler |
| **Intermediate Steps** | Excellent | Good |
| **Database** | Required | Optional |

**Choose TruLens if**: Deep RAG analysis is critical
**Choose Phoenix if**: Want OTEL-native with simpler setup

---

### vs LangSmith
| Aspect | TruLens | LangSmith |
|--------|---------|-----------|
| **Open Source** | ✅ Yes | ❌ No |
| **RAG Metrics** | More advanced | Good |
| **LangChain Integration** | Excellent | Native |
| **Cost** | Free (self-host) | Paid service |
| **Feedback Functions** | More flexible | Good |

**Choose TruLens if**: Want OSS with advanced RAG metrics
**Choose LangSmith if**: Prefer managed service with LangChain

---

### vs Custom-Evals
| Aspect | TruLens | Custom-Evals |
|--------|---------|--------------|
| **Observability** | Excellent | Basic |
| **Setup Complexity** | High | Low |
| **RAG Metrics** | Advanced | Good |
| **Dependencies** | Heavy | Minimal |
| **Flexibility** | Medium | High |

**Choose TruLens if**: RAG observability is priority
**Choose Custom-Evals if**: Want lightweight flexibility

---

### vs RAGAS
| Aspect | TruLens | RAGAS |
|--------|---------|-------|
| **Observability** | Excellent | None |
| **RAG Metrics** | More comprehensive | Focused set |
| **Learning Curve** | Steeper | Easier |
| **Dashboard** | Built-in | External |
| **Setup** | More complex | Simpler |

**Choose TruLens if**: Need observability + evaluation
**Choose RAGAS if**: Just need RAG metrics quickly

---

## When to Choose TruLens

### ✅ Perfect For

1. **Complex RAG Systems**
   - Multi-step retrieval
   - Re-ranking pipelines
   - Hybrid search
   - Query transformation
   - Context fusion

2. **RAG Debugging**
   - Poor response quality
   - Identify retrieval issues
   - Context relevance problems
   - Hallucination sources
   - Optimization opportunities

3. **Agent Development**
   - Track agent reasoning
   - Tool usage patterns
   - Multi-turn interactions
   - Decision visualization
   - Performance bottlenecks

4. **Production Monitoring**
   - Track RAG performance
   - Monitor quality metrics
   - Identify regressions
   - User feedback integration
   - A/B testing RAG configs

5. **Research & Experimentation**
   - Compare RAG approaches
   - Evaluate retrievers
   - Test different embeddings
   - Prompt engineering
   - Systematic optimization

6. **LangChain Heavy Users**
   - Deep LangChain integration
   - Chain inspection
   - LCEL support
   - Memory tracking

### ❌ Not Ideal For

1. **Simple Applications**
   - Basic question answering
   - No retrieval involved
   - Single LLM call
   - Overhead not justified

2. **Minimal Dependencies**
   - Want lightweight
   - Avoid database
   - No UI needed
   - Prefer code-only

3. **Non-RAG Use Cases**
   - Pure text generation
   - Classification tasks
   - Non-retrieval workflows
   - Other tools better suited

4. **Quick Prototyping**
   - Just want fast eval
   - Don't need observability
   - Minimize setup time
   - Prefer simpler tools

---

## Pricing

### Cost Breakdown

| Component | Self-Hosted | TruEra Enterprise |
|-----------|-------------|-------------------|
| **TruLens Software** | 💰 **Free** | - |
| **Infrastructure** | Your costs | Included |
| **Database** | Your costs | Managed |
| **Support** | Community | Enterprise |
| **Advanced Features** | Limited | Full |
| **Team Collaboration** | Basic | Advanced |

### Self-Hosted Monthly Costs

| Usage Level | Storage | Compute | Est. Total |
|-------------|---------|---------|------------|
| **Small** (1K traces/mo) | ~500 MB | Small VM | $10-20 |
| **Medium** (10K traces/mo) | ~5 GB | Medium VM | $50-100 |
| **Large** (100K traces/mo) | ~50 GB | Large VM | $200-400 |

### TruEra Enterprise

Contact TruEra for enterprise pricing:
- **Team**: $1,000-5,000/month
- **Enterprise**: Custom pricing
- Includes managed infrastructure, support, advanced features

**Note**: OSS version is fully functional and free

---

## Quick Start

### Installation

```bash
# Install TruLens
pip install trulens-eval

# With specific integrations
pip install trulens-eval[langchain]
pip install trulens-eval[llama-index]

# Full installation
pip install trulens-eval[all]
```

### Initialize TruLens

```python
from trulens_eval import Tru

# Initialize (creates SQLite database)
tru = Tru()

# Or use PostgreSQL
# tru = Tru(database_url="postgresql://user:pass@localhost/trulens")

# Launch dashboard
tru.run_dashboard()
# Opens at http://localhost:8501
```

### Basic LangChain Example

```python
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from trulens_eval import TruChain, Feedback, OpenAI as TruOpenAI

# Create your LangChain app
prompt = PromptTemplate.from_template("Answer this question: {question}")
llm = OpenAI(temperature=0.9)
chain = LLMChain(llm=llm, prompt=prompt)

# Setup feedback functions (evaluators)
provider = TruOpenAI()

# Answer relevance feedback
f_answer_relevance = Feedback(
    provider.relevance,
    name="Answer Relevance"
).on_input_output()

# Create TruChain wrapper
tru_chain = TruChain(
    chain,
    app_id="my_qa_app",
    feedbacks=[f_answer_relevance]
)

# Use it - automatically tracked!
with tru_chain as recording:
    response = chain.run(question="What is machine learning?")

print(response)

# View in dashboard
tru.run_dashboard()
```

### RAG Example with Context

```python
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from trulens_eval import Feedback, Select

# Create RAG chain
vectorstore = Chroma.from_documents(documents, OpenAIEmbeddings())
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=vectorstore.as_retriever()
)

# Advanced feedback functions
provider = TruOpenAI()

# Context relevance - are retrieved docs relevant?
f_context_relevance = Feedback(
    provider.context_relevance,
    name="Context Relevance"
).on(Select.RecordCalls.retriever.invoke.rets[:].page_content).aggregate(lambda scores: sum(scores) / len(scores))

# Groundedness - is response grounded in context?
f_groundedness = Feedback(
    provider.groundedness_measure_with_cot_reasons,
    name="Groundedness"
).on(Select.RecordCalls.retriever.invoke.rets[:].page_content).on_output()

# Answer relevance - does response address query?
f_answer_relevance = Feedback(
    provider.relevance,
    name="Answer Relevance"
).on_input_output()

# Wrap with TruChain
tru_qa = TruChain(
    qa_chain,
    app_id="my_rag_app",
    feedbacks=[f_context_relevance, f_groundedness, f_answer_relevance]
)

# Use it
with tru_qa as recording:
    response = qa_chain.run("What are the benefits of solar energy?")

# Access results programmatically
records, feedback = tru.get_records_and_feedback(app_ids=["my_rag_app"])
print(records)
print(feedback)
```

### Custom App (Non-LangChain)

```python
from trulens_eval import TruCustomApp, instrument

class MyRAGApp:
    @instrument
    def retrieve(self, query: str) -> list:
        # Your retrieval logic
        docs = vector_store.search(query, k=5)
        return docs

    @instrument
    def generate(self, query: str, docs: list) -> str:
        # Your generation logic
        context = "\n".join(docs)
        response = llm.generate(f"Context: {context}\nQuery: {query}")
        return response

    def query(self, question: str) -> str:
        docs = self.retrieve(question)
        response = self.generate(question, docs)
        return response

# Wrap with TruCustomApp
app = MyRAGApp()
tru_app = TruCustomApp(
    app,
    app_id="custom_rag",
    feedbacks=[f_context_relevance, f_groundedness, f_answer_relevance]
)

# Use it
with tru_app as recording:
    result = app.query("What is quantum computing?")
```

---

## Architecture Highlights

### Design Principles

1. **Instrumentation-First**: Deep tracking of execution
2. **Feedback Functions**: Flexible evaluation system
3. **Framework Integration**: Deep LangChain/LlamaIndex support
4. **Database-Backed**: Persistent storage of traces
5. **Visualization**: Rich dashboard for exploration

### Core Components

```
TruLens Architecture:
┌─────────────────────────────────────┐
│   Dashboard (Streamlit UI)         │
│   - Trace visualization             │
│   - Metric trends                   │
│   - Leaderboards                    │
│   - Comparisons                     │
└─────────────────────────────────────┘
              ↑
┌─────────────────────────────────────┐
│   TruLens Core                      │
│   - Record storage                  │
│   - Feedback execution              │
│   - Query interface                 │
└─────────────────────────────────────┘
              ↑
┌─────────────────────────────────────┐
│   Instrumentation Layer             │
│   - TruChain (LangChain)            │
│   - TruLlama (LlamaIndex)           │
│   - TruCustomApp                    │
│   - @instrument decorator           │
└─────────────────────────────────────┘
              ↑
┌─────────────────────────────────────┐
│   Your Application                  │
│   - LangChain chains                │
│   - LlamaIndex engines              │
│   - Custom Python code              │
└─────────────────────────────────────┘
```

### Feedback Function System

```python
# Feedback function anatomy
feedback = Feedback(
    provider.metric_function,  # Evaluation function
    name="Metric Name"
).on(selector)  # What to evaluate

# Selectors specify what to evaluate
.on_input()                    # Input to app
.on_output()                   # Output from app
.on_input_output()             # Both
.on(Select.RecordCalls.retriever.invoke.rets)  # Specific component
```

---

## Advanced Features

### 1. Custom Feedback Functions

```python
from trulens_eval import Feedback
from typing import List

# Custom Python function
def custom_length_check(text: str) -> float:
    """Check if response is appropriate length."""
    length = len(text)
    if 50 <= length <= 500:
        return 1.0
    elif length < 50:
        return 0.5
    else:
        return 0.7

f_length = Feedback(
    custom_length_check,
    name="Response Length"
).on_output()

# LLM-based custom feedback
def custom_tone_check(output: str) -> float:
    """Check if tone is professional."""
    prompt = f"Rate professionalism of: {output}\nScore 0-1:"
    score = llm.evaluate(prompt)
    return float(score)

f_tone = Feedback(
    custom_tone_check,
    name="Professional Tone"
).on_output()
```

### 2. Aggregate Functions

```python
# Average multiple context chunks
f_context_relevance = Feedback(
    provider.context_relevance
).on(
    Select.RecordCalls.retriever.invoke.rets[:].page_content
).aggregate(
    lambda scores: sum(scores) / len(scores)
)

# Minimum score (strictest)
f_groundedness = Feedback(
    provider.groundedness
).on(
    Select.RecordCalls.retriever.invoke.rets[:].page_content
).aggregate(min)

# All must pass
f_safety = Feedback(
    provider.safety_check
).on(
    Select.RecordCalls.retriever.invoke.rets[:].page_content
).aggregate(lambda scores: all(s > 0.8 for s in scores))
```

### 3. Comparative Evaluation

```python
# Run multiple versions
apps = {
    "v1_gpt3": TruChain(chain_v1, app_id="v1"),
    "v2_gpt4": TruChain(chain_v2, app_id="v2"),
}

# Evaluate same queries
for query in test_queries:
    for version, app in apps.items():
        with app as recording:
            response = app.app.run(query)

# Compare in dashboard
tru.run_dashboard()
# View leaderboard comparing v1 vs v2
```

### 4. Async Feedback

```python
# Run feedback async (doesn't block app)
tru_app = TruChain(
    chain,
    app_id="my_app",
    feedbacks=[f_answer_relevance],
    feedback_mode="deferred"  # or "with_app" (default)
)

# App returns immediately, feedback runs in background
with tru_app as recording:
    response = chain.run(query)
# Response returned, feedback still running

# Check feedback later
records, feedback = tru.get_records_and_feedback(app_ids=["my_app"])
```

### 5. Ground Truth Evaluation

```python
from trulens_eval import GroundTruthAgreement

# Setup ground truth
ground_truth = {
    "What is AI?": "Artificial Intelligence is...",
    "What is ML?": "Machine Learning is...",
}

# Ground truth feedback
f_groundtruth = GroundTruthAgreement(
    ground_truth,
    provider=provider
).on_input_output()

tru_app = TruChain(
    chain,
    app_id="app_with_gt",
    feedbacks=[f_groundtruth]
)
```

---

## RAG-Specific Features

### RAG Triad Metrics

The three core RAG metrics:

```python
from trulens_eval import Feedback, Select, TruOpenAI

provider = TruOpenAI()

# 1. Context Relevance
# Are retrieved documents relevant to the query?
f_context_relevance = Feedback(
    provider.context_relevance,
    name="Context Relevance"
).on_input().on(
    Select.RecordCalls.retriever.invoke.rets[:].page_content
).aggregate(lambda scores: sum(scores) / len(scores))

# 2. Groundedness
# Is the response grounded in the retrieved context?
f_groundedness = Feedback(
    provider.groundedness_measure_with_cot_reasons,
    name="Groundedness"
).on(
    Select.RecordCalls.retriever.invoke.rets[:].page_content
).on_output()

# 3. Answer Relevance
# Does the answer address the query?
f_answer_relevance = Feedback(
    provider.relevance,
    name="Answer Relevance"
).on_input_output()
```

### Retrieval Evaluation

```python
# Evaluate retriever quality
f_retrieval_precision = Feedback(
    provider.context_relevance_with_cot_reasons,
    name="Retrieval Precision"
).on_input().on(
    Select.RecordCalls.retriever.invoke.rets[:].page_content
).aggregate(lambda scores: sum(1 for s in scores if s > 0.5) / len(scores))

# Evaluate retrieval diversity
def diversity_score(docs: List[str]) -> float:
    """Measure diversity of retrieved documents."""
    # Custom logic to compute diversity
    unique_topics = len(set(extract_topics(docs)))
    return min(unique_topics / len(docs), 1.0)

f_diversity = Feedback(
    diversity_score,
    name="Retrieval Diversity"
).on(Select.RecordCalls.retriever.invoke.rets[:].page_content)
```

---

## Integration Examples

### LlamaIndex

```python
from llama_index.core import VectorStoreIndex
from trulens_eval import TruLlama

# Create LlamaIndex app
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Wrap with TruLlama
tru_query_engine = TruLlama(
    query_engine,
    app_id="llama_index_app",
    feedbacks=[f_context_relevance, f_groundedness, f_answer_relevance]
)

# Use it
with tru_query_engine as recording:
    response = query_engine.query("What is the main topic?")
```

### LangChain LCEL

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# LCEL chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Wrap with TruChain
tru_rag = TruChain(
    rag_chain,
    app_id="lcel_rag",
    feedbacks=[f_context_relevance, f_groundedness, f_answer_relevance]
)

with tru_rag as recording:
    response = rag_chain.invoke("What is the answer?")
```

---

## Comparison Summary

### Unique Advantages
1. 🔍 Best-in-class RAG observability
2. 🎯 Comprehensive RAG metrics
3. 🔬 Deep intermediate step tracking
4. 🎨 Rich visualization dashboard
5. 🔧 Flexible feedback functions
6. 🔓 Open source option

### Trade-offs
1. Steeper learning curve
2. More setup complexity
3. Database dependency
4. RAG-heavy focus
5. Performance overhead
6. Not OTEL native

---

## Resources

### Documentation
- **Official Docs**: https://www.trulens.org/
- **GitHub**: https://github.com/truera/trulens
- **Quickstart**: https://www.trulens.org/quickstart/
- **API Reference**: https://www.trulens.org/reference/

### Guides
- **RAG Evaluation**: https://www.trulens.org/cookbook/rag_evaluation/
- **Feedback Functions**: https://www.trulens.org/guides/feedback/
- **LangChain Integration**: https://www.trulens.org/guides/langchain/
- **LlamaIndex Integration**: https://www.trulens.org/guides/llamaindex/

### Examples
- **Example Notebooks**: https://github.com/truera/trulens/tree/main/examples
- **RAG Triad**: https://www.trulens.org/cookbook/rag_triad/

### Research
- **RAG Evaluation Paper**: https://arxiv.org/abs/2309.15217
- **TruEra Research**: https://truera.com/resources/

### Community
- **Slack**: https://www.trulens.org/slack/
- **GitHub Issues**: https://github.com/truera/trulens/issues
- **GitHub Discussions**: https://github.com/truera/trulens/discussions

---

## Verdict

**TruLens is the best choice for teams building complex RAG systems who need deep observability and comprehensive evaluation metrics.**

**Rating**: ⭐⭐⭐⭐⭐ (5/5 for RAG evaluation)

### Choose TruLens if you value:
- ✅ Deep RAG observability
- ✅ Intermediate step tracking
- ✅ Comprehensive RAG metrics
- ✅ Rich visualization
- ✅ LangChain/LlamaIndex integration
- ✅ Open source option

### Choose alternatives if you need:
- ❌ Lightweight setup → Custom-Evals, RAGAS
- ❌ OpenTelemetry native → Phoenix
- ❌ Managed service → LangSmith
- ❌ Non-RAG focus → Custom-Evals, DeepEval
- ❌ Simpler learning curve → RAGAS

---

**Next**: [Compare All Frameworks](Compare_All_Eval_Frameworks.md) | [Try Custom-Evals](01_Custom_Evals.md)
