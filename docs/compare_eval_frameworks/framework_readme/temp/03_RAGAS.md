# RAGAS: The Gold Standard for RAG Evaluation

**Type**: Python Library | **License**: Apache 2.0 (Open Source) | **Year**: 2023

---

## Quick Overview

RAGAS (Retrieval-Augmented Generation Assessment) is the **premier framework for evaluating RAG systems**, built from the ground up with research-backed metrics specifically designed for RAG pipelines. It's the go-to choice when you need to evaluate both retrieval quality and generation quality in a unified framework.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | RAG-specific evaluation only |
| **Setup Time** | ⚡ 5 minutes |
| **Learning Curve** | Easy |
| **Dependencies** | Minimal (LangChain, OpenAI) |
| **Cost** | Free (OSS) + LLM API costs |
| **Best For** | Teams building RAG systems |

---

## Key Strengths

### ✅ Advantages

1. **Best-in-Class RAG Metrics**
   - **Faithfulness**: Measures if answers are grounded in retrieved context (anti-hallucination)
   - **Answer Relevancy**: Evaluates how well answers address the question
   - **Context Precision**: Assesses quality of retrieved contexts
   - **Context Recall**: Measures retrieval coverage
   - **Answer Correctness**: Compares against ground truth
   - **Answer Similarity**: Semantic similarity to expected answers

2. **Research-Backed Methodology**
   - Based on peer-reviewed research paper (arXiv:2309.15217)
   - Scientifically validated metrics
   - Continuously improved based on academic research
   - Citation: "RAGAS: Automated Evaluation of Retrieval Augmented Generation"

3. **Purpose-Built for RAG**
   - Designed specifically for RAG evaluation (not adapted from general metrics)
   - Understands the two-stage RAG pipeline (retrieval + generation)
   - Evaluates retrieval and generation independently and holistically
   - Tests end-to-end RAG quality

4. **Easy to Use**
   - Simple dataset-based API
   - Batch evaluation out of the box
   - Works with any RAG implementation
   - Minimal boilerplate code

5. **Framework Agnostic**
   - Works with LangChain, LlamaIndex, Haystack
   - Works with custom RAG implementations
   - No vendor lock-in
   - Bring your own RAG system

6. **LLM-as-Judge Approach**
   - Uses LLMs to evaluate quality (GPT-4, Claude, etc.)
   - More nuanced than rule-based metrics
   - Can handle complex, open-ended answers
   - Correlates well with human judgment

### ⚠️ Limitations

1. **RAG-Only Focus**
   - Not suitable for non-RAG use cases
   - No agent evaluation metrics
   - No general LLM evaluation beyond RAG
   - Limited for chatbot or tool-using systems

2. **Requires LLM API Costs**
   - Needs OpenAI or compatible API for evaluation
   - Can get expensive at scale (>10K evaluations/month)
   - No offline evaluation mode
   - Dependent on external LLM providers

3. **No Built-in Observability**
   - No dashboard or visualization
   - No trace collection
   - No production monitoring
   - Requires external tools for visualization

4. **Limited Customization**
   - Pre-defined metric implementations
   - Hard to modify core metrics
   - Not designed for custom evaluation criteria
   - Less flexible than general frameworks

5. **Ground Truth Requirements**
   - Some metrics require ground truth data
   - Need labeled datasets for full evaluation
   - Can't fully evaluate without reference answers
   - Dataset preparation overhead

---

## vs Other Frameworks

### vs Custom-Evals

| Aspect | RAGAS | Custom-Evals |
|--------|-------|--------------|
| **Scope** | RAG-only | General + RAG |
| **RAG Metrics** | ✅✅ Best | ✅ Good |
| **Flexibility** | Medium | High |
| **Multi-Framework** | ⚠️ Limited | ✅ 17+ |
| **Code Metrics** | ❌ No | ✅ Yes |
| **Learning Curve** | Easier | Easy |
| **Customization** | Limited | Extensive |

**Choose RAGAS if**: You're 100% focused on RAG evaluation and want the best RAG metrics

**Choose Custom-Evals if**: You need flexibility beyond RAG or want multi-framework support

---

### vs Phoenix Evals

| Aspect | RAGAS | Phoenix |
|--------|-------|---------|
| **Setup** | Simpler | More complex |
| **Observability** | ❌ None | ✅✅ Excellent |
| **RAG Metrics** | ✅✅ Best | ✅ Good |
| **Server Required** | No | Yes (for UI) |
| **Tracing** | No | Core feature |
| **Use Case** | Evaluation | Observability + Eval |
| **Dataset Support** | ✅ Native | Manual |

**Choose RAGAS if**: You want best-in-class RAG metrics without infrastructure overhead

**Choose Phoenix if**: You need full observability and tracing for production RAG systems

---

### vs ARES (Automated RAG Evaluation System)

| Aspect | RAGAS | ARES |
|--------|-------|------|
| **Approach** | LLM-as-judge | Synthetic data + classifiers |
| **Setup** | Simple | Complex |
| **Ground Truth** | Some metrics need it | Generates synthetic |
| **Metrics** | 6+ RAG metrics | 3 core metrics |
| **Model Training** | No | Yes (trains classifiers) |
| **Maturity** | Production-ready | Research/experimental |
| **Documentation** | Excellent | Academic |

**Choose RAGAS if**: You want production-ready, well-documented RAG evaluation

**Choose ARES if**: You're in research and want to generate synthetic test data

---

### vs DeepEval

| Aspect | RAGAS | DeepEval |
|--------|-------|----------|
| **RAG Focus** | ✅✅ Core | ⚠️ One of many |
| **RAG Metrics** | 6+ specialized | 4-5 general |
| **Test Framework** | Manual | Pytest integration |
| **Scope** | RAG-only | Multi-purpose |
| **Research Backing** | Strong | Limited |
| **Best Use** | RAG evaluation | General testing |

**Choose RAGAS if**: RAG is your primary use case and you want specialized metrics

**Choose DeepEval if**: You want pytest integration and general-purpose evaluation

---

## When to Choose RAGAS

### ✅ Perfect For

1. **RAG System Evaluation**
   - Building Q&A systems with retrieval
   - Document search and answer generation
   - Knowledge base chatbots
   - Enterprise search + summarization

2. **Retrieval Quality Testing**
   - Evaluating vector search quality
   - Testing embedding models
   - Comparing different retrieval strategies
   - Optimizing chunk size and overlap

3. **Answer Quality Assessment**
   - Preventing hallucinations (faithfulness metric)
   - Ensuring relevance to user queries
   - Validating answer correctness
   - Measuring semantic similarity

4. **RAG Research & Optimization**
   - Academic research on RAG systems
   - Benchmarking RAG approaches
   - A/B testing different RAG configurations
   - Hyperparameter tuning for RAG

5. **Production RAG Monitoring**
   - Batch evaluation of production outputs
   - Regression testing for RAG changes
   - Quality assurance for RAG deployments
   - Dataset-based validation

### ❌ Not Ideal For

1. **Non-RAG LLM Applications**
   - Pure chatbots without retrieval
   - Code generation systems
   - General text generation
   - Agent-based systems (unless RAG-powered)

2. **Real-Time Evaluation**
   - No built-in observability
   - Better suited for batch evaluation
   - Use Phoenix or LangSmith for real-time

3. **Extensive Customization Needs**
   - Hard to modify core metrics
   - Limited extensibility compared to Custom-Evals
   - Pre-defined evaluation approach

4. **Zero LLM API Budget**
   - Requires LLM API for evaluation
   - No offline evaluation mode
   - Consider code-based metrics instead

---

## Pricing

### Cost Breakdown

| Component | Cost |
|-----------|------|
| **Framework** | 💰 **Free** (Apache 2.0 License) |
| **LLM API** | ~$0.01-0.10 per evaluation |
| **Infrastructure** | None required |
| **Support** | Community (GitHub, Discord) |

### Detailed Cost Analysis

#### Per Evaluation Cost

Using **GPT-4o-mini** (recommended):
- **Input tokens**: ~500-1000 tokens (question + answer + contexts)
- **Output tokens**: ~100-200 tokens (reasoning)
- **Cost per eval**: ~$0.001-0.005 per metric
- **Full suite (5 metrics)**: ~$0.005-0.025 per sample

Using **GPT-4**:
- **Cost per eval**: ~$0.01-0.05 per metric
- **Full suite**: ~$0.05-0.25 per sample

#### Monthly Cost Estimates

| Evaluations/Month | GPT-4o-mini | GPT-4 |
|-------------------|-------------|-------|
| 1,000 | $5-25 | $50-250 |
| 10,000 | $50-250 | $500-2,500 |
| 100,000 | $500-2,500 | $5,000-25,000 |
| 1,000,000 | $5,000-25,000 | $50,000-250,000 |

### Cost Optimization Tips

1. **Use GPT-4o-mini for most evaluations** (~10x cheaper than GPT-4)
2. **Sample your dataset** - evaluate 10% for quick feedback
3. **Selective metrics** - only run metrics you need
4. **Batch evaluation** - more efficient than one-by-one
5. **Cache ground truth** - avoid re-computing baselines

---

## Quick Start

### Installation

```bash
# Basic installation
pip install ragas

# With LangChain support (recommended)
pip install ragas langchain-openai

# With all dependencies
pip install ragas langchain-openai datasets pandas
```

### 5-Minute Example

```python
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

# Prepare your RAG evaluation data
data = {
    "question": [
        "What is the capital of France?",
        "Who invented the telephone?"
    ],
    "answer": [
        "The capital of France is Paris.",
        "Alexander Graham Bell invented the telephone in 1876."
    ],
    "contexts": [
        ["Paris is the capital and largest city of France."],
        ["The telephone was invented by Alexander Graham Bell in 1876."]
    ],
    "ground_truth": [
        "Paris",
        "Alexander Graham Bell"
    ]
}

# Convert to RAGAS dataset format
dataset = Dataset.from_dict(data)

# Run evaluation with core metrics
results = evaluate(
    dataset,
    metrics=[
        faithfulness,        # Are answers grounded in context?
        answer_relevancy,    # Do answers address the question?
        context_precision,   # Are retrieved contexts relevant?
        context_recall       # Are all necessary contexts retrieved?
    ]
)

# View results
print(f"Faithfulness: {results['faithfulness']:.3f}")
print(f"Answer Relevancy: {results['answer_relevancy']:.3f}")
print(f"Context Precision: {results['context_precision']:.3f}")
print(f"Context Recall: {results['context_recall']:.3f}")
```

**Output:**
```
Faithfulness: 0.950
Answer Relevancy: 0.987
Context Precision: 0.923
Context Recall: 0.956
```

---

## Advanced Usage Examples

### 1. Faithfulness Evaluation (Anti-Hallucination)

```python
from ragas.metrics import faithfulness

# Test if answers are grounded in retrieved context
data = {
    "question": ["What are the health benefits of exercise?"],
    "answer": [
        "Regular exercise improves cardiovascular health, strengthens muscles, "
        "boosts mental well-being, and helps maintain healthy weight."
    ],
    "contexts": [[
        "Exercise has numerous health benefits including improved heart health, "
        "stronger muscles, better mood, and weight management."
    ]]
}

dataset = Dataset.from_dict(data)
results = evaluate(dataset, metrics=[faithfulness])

print(f"Faithfulness: {results['faithfulness']:.3f}")
# Score closer to 1.0 = better grounding in context
```

**Why Faithfulness Matters:**
- Prevents hallucinations in RAG systems
- Ensures answers are based on retrieved documents
- Critical for factual domains (medical, legal, financial)
- Builds user trust in your RAG application

---

### 2. Retrieval Quality Evaluation

```python
from ragas.metrics import context_precision, context_recall

# Evaluate your retrieval system
data = {
    "question": ["What are Python's main features?"],
    "answer": [
        "Python features simple syntax, dynamic typing, extensive libraries, "
        "and strong community support."
    ],
    "contexts": [[
        "Python is a high-level language with simple, readable syntax.",
        "Python features dynamic typing and automatic memory management.",
        "Python has a vast ecosystem of libraries and frameworks.",
        "Python has a large and active developer community.",
        "Python was created by Guido van Rossum."  # Less relevant
    ]],
    "ground_truth": [
        "Python features include simple syntax, dynamic typing, extensive libraries."
    ]
}

dataset = Dataset.from_dict(data)
results = evaluate(dataset, metrics=[context_precision, context_recall])

print(f"Context Precision: {results['context_precision']:.3f}")
# Are retrieved contexts relevant to answering the question?

print(f"Context Recall: {results['context_recall']:.3f}")
# Did we retrieve all necessary information?
```

**Optimization Guide:**
- **High Precision, Low Recall**: Increase number of retrieved chunks
- **Low Precision, High Recall**: Improve ranking/reranking
- **Both Low**: Improve embedding model or chunk strategy

---

### 3. Answer Quality Evaluation

```python
from ragas.metrics import answer_relevancy, answer_correctness

data = {
    "question": ["How does machine learning differ from traditional programming?"],
    "answer": [
        "Machine learning allows systems to learn patterns from data automatically, "
        "while traditional programming requires explicit rule-based instructions."
    ],
    "contexts": [[
        "Traditional programming uses explicit rules coded by developers.",
        "Machine learning systems learn patterns from training data.",
        "ML models can improve performance with more data."
    ]],
    "ground_truth": [
        "Machine learning learns from data, traditional programming uses explicit rules."
    ]
}

dataset = Dataset.from_dict(data)
results = evaluate(
    dataset,
    metrics=[answer_relevancy, answer_correctness]
)

print(f"Answer Relevancy: {results['answer_relevancy']:.3f}")
# Does answer address the question?

print(f"Answer Correctness: {results['answer_correctness']:.3f}")
# Is answer factually correct vs ground truth?
```

---

### 4. Comparative RAG Evaluation (A/B Testing)

```python
# Compare two different RAG configurations

# Configuration A: Basic retrieval
config_a = {
    "question": ["What causes climate change?"],
    "answer": ["Climate change is caused by greenhouse gas emissions."],
    "contexts": [["Greenhouse gases trap heat in the atmosphere."]],
    "ground_truth": ["Human greenhouse gas emissions cause climate change."]
}

# Configuration B: Enhanced retrieval
config_b = {
    "question": ["What causes climate change?"],
    "answer": [
        "Climate change is primarily caused by human activities that release "
        "greenhouse gases, particularly burning fossil fuels and deforestation."
    ],
    "contexts": [[
        "Human activities release greenhouse gases into the atmosphere.",
        "Burning fossil fuels is the main source of CO2 emissions.",
        "Deforestation reduces CO2 absorption by trees."
    ]],
    "ground_truth": ["Human greenhouse gas emissions cause climate change."]
}

# Evaluate both
dataset_a = Dataset.from_dict(config_a)
dataset_b = Dataset.from_dict(config_b)

metrics = [faithfulness, answer_correctness, context_recall]
results_a = evaluate(dataset_a, metrics=metrics)
results_b = evaluate(dataset_b, metrics=metrics)

print("\nConfiguration A:")
print(f"  Faithfulness: {results_a['faithfulness']:.3f}")
print(f"  Correctness: {results_a['answer_correctness']:.3f}")
print(f"  Context Recall: {results_a['context_recall']:.3f}")

print("\nConfiguration B:")
print(f"  Faithfulness: {results_b['faithfulness']:.3f}")
print(f"  Correctness: {results_b['answer_correctness']:.3f}")
print(f"  Context Recall: {results_b['context_recall']:.3f}")

# Configuration B should score higher on all metrics
```

---

### 5. Batch Production Evaluation

```python
import pandas as pd
from ragas import evaluate

# Load production data (from your logs, database, etc.)
production_data = pd.read_csv('rag_outputs.csv')

# Convert to RAGAS format
dataset = Dataset.from_pandas(production_data)

# Run comprehensive evaluation
results = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
        answer_correctness
    ]
)

# Aggregate results
print("\nProduction RAG Quality Report:")
print(f"Samples Evaluated: {len(production_data)}")
print(f"Average Faithfulness: {results['faithfulness']:.3f}")
print(f"Average Relevancy: {results['answer_relevancy']:.3f}")
print(f"Average Context Precision: {results['context_precision']:.3f}")
print(f"Average Context Recall: {results['context_recall']:.3f}")
print(f"Average Correctness: {results['answer_correctness']:.3f}")

# Flag low-quality samples for review
low_faithfulness = results.scores[results.scores['faithfulness'] < 0.7]
print(f"\nLow Faithfulness Samples: {len(low_faithfulness)}")
```

---

### 6. Custom LLM Configuration

```python
from langchain_anthropic import ChatAnthropic
from ragas.llms import LangchainLLMWrapper

# Use Claude instead of GPT-4
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key="your-api-key"
)

# Wrap for RAGAS
ragas_llm = LangchainLLMWrapper(llm)

# Evaluate with Claude
results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy],
    llm=ragas_llm
)
```

**LLM Provider Comparison:**
- **GPT-4o-mini**: Fastest, cheapest, good quality
- **GPT-4**: Best quality, slower, expensive
- **Claude 3.5 Sonnet**: Excellent reasoning, good for complex eval
- **Claude 3 Haiku**: Fast, cheap, decent quality

---

## Architecture Highlights

### Design Principles

1. **RAG-First Design**: Every metric designed specifically for RAG evaluation
2. **Dataset-Centric**: Batch evaluation over streaming
3. **LLM-as-Judge**: Uses LLM intelligence for nuanced evaluation
4. **Research-Backed**: Based on academic research and validation
5. **Simple API**: Minimal boilerplate, maximum clarity

### Core Metrics Explained

#### 1. Faithfulness (Groundedness)
```
Faithfulness = Number of factual claims supported by context / Total claims
```
- **Purpose**: Prevent hallucinations
- **How it works**: LLM extracts claims from answer, checks each against context
- **Score range**: 0.0 (all hallucinations) to 1.0 (fully grounded)
- **Best for**: Medical, legal, financial domains where accuracy is critical

#### 2. Answer Relevancy
```
Relevancy = Semantic similarity between question and answer
```
- **Purpose**: Ensure answers address the question
- **How it works**: LLM generates questions from answer, measures similarity
- **Score range**: 0.0 (irrelevant) to 1.0 (perfectly relevant)
- **Best for**: Q&A systems, customer support bots

#### 3. Context Precision
```
Precision = Sum of (Relevance of context @ rank k) / Total contexts
```
- **Purpose**: Measure retrieval ranking quality
- **How it works**: Checks if relevant contexts are ranked higher
- **Score range**: 0.0 (poor ranking) to 1.0 (perfect ranking)
- **Best for**: Optimizing reranking algorithms

#### 4. Context Recall
```
Recall = Sentences in ground truth attributable to contexts / Total GT sentences
```
- **Purpose**: Measure retrieval coverage
- **How it works**: Checks if all needed information was retrieved
- **Score range**: 0.0 (missed everything) to 1.0 (retrieved everything)
- **Best for**: Ensuring comprehensive retrieval

#### 5. Answer Correctness
```
Correctness = Weighted(Factual similarity + Semantic similarity)
```
- **Purpose**: Compare answer to ground truth
- **How it works**: Combines factual and semantic comparison
- **Score range**: 0.0 (wrong) to 1.0 (correct)
- **Best for**: Benchmarking against labeled datasets

#### 6. Answer Similarity
```
Similarity = Semantic similarity(Answer, Ground Truth)
```
- **Purpose**: Measure semantic closeness to expected answer
- **How it works**: Embedding-based similarity
- **Score range**: 0.0 (different) to 1.0 (identical)
- **Best for**: When exact correctness is too strict

---

## Comparison Summary

### Unique Advantages

1. ⭐ **Best RAG metrics** - Gold standard for RAG evaluation
2. 🎓 **Research-backed** - Academic validation and peer review
3. 🎯 **Purpose-built for RAG** - Not adapted from general metrics
4. 📊 **Comprehensive coverage** - Retrieval + generation + end-to-end
5. 🚀 **Easy to use** - Simple API, minimal setup
6. 🔓 **Framework agnostic** - Works with any RAG implementation

### Trade-offs

1. RAG-only focus (not for general LLM evaluation)
2. Requires LLM API costs for evaluation
3. No built-in observability or dashboards
4. Limited customization compared to general frameworks
5. Some metrics require ground truth data

### RAGAS vs The Competition

| Feature | RAGAS | Custom-Evals | Phoenix | ARES | DeepEval |
|---------|-------|--------------|---------|------|----------|
| **RAG Metrics** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ |
| **General Eval** | ❌ | ✅ | ✅ | ❌ | ✅ |
| **Setup Time** | 5 min | 5 min | 15 min | 30 min | 10 min |
| **LLM Cost** | Medium | Medium | Medium | Low | Medium |
| **Observability** | ❌ | ⚠️ | ✅✅ | ❌ | ⚠️ |
| **Research Backing** | ✅✅ | ⚠️ | ⚠️ | ✅✅ | ⚠️ |

---

## Migration Examples

### From Custom-Evals

```python
# Custom-Evals approach
from custom.evals import FaithfulnessEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
faithfulness_eval = FaithfulnessEvaluator(llm)
relevance_eval = RelevanceEvaluator(llm)

# Evaluate one at a time
score1 = faithfulness_eval.evaluate({
    "input": question,
    "output": answer,
    "context": context
})
score2 = relevance_eval.evaluate({
    "input": question,
    "output": answer
})

# ===== RAGAS approach =====
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

# Batch evaluation with multiple metrics
data = {
    "question": [question],
    "answer": [answer],
    "contexts": [[context]]
}
dataset = Dataset.from_dict(data)
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy])

# Access all scores at once
print(results['faithfulness'])
print(results['answer_relevancy'])
```

**Migration Benefits:**
- Batch evaluation is faster
- Multiple metrics in one call
- Better for large-scale evaluation
- RAG-specific metrics more accurate

---

### From Phoenix Evals

```python
# Phoenix approach
from phoenix.evals import (
    RAGRelevancyEvaluator,
    HallucinationEvaluator,
)

rag_relevancy = RAGRelevancyEvaluator()
hallucination = HallucinationEvaluator()

# Evaluate with Phoenix
relevance_score = rag_relevancy.evaluate(
    input=question,
    output=answer
)
hallucination_score = hallucination.evaluate(
    input=question,
    output=answer,
    context=context
)

# ===== RAGAS approach =====
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness

data = {
    "question": [question],
    "answer": [answer],
    "contexts": [[context]]
}
dataset = Dataset.from_dict(data)

# Faithfulness = inverse of hallucination
results = evaluate(dataset, metrics=[answer_relevancy, faithfulness])
```

**Why Migrate:**
- RAGAS has more RAG-specific metrics
- Better research backing
- Simpler API for batch evaluation
- No server required

---

### From DeepEval

```python
# DeepEval approach
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric
)

test_case = LLMTestCase(
    input=question,
    actual_output=answer,
    retrieval_context=[context],
    expected_output=ground_truth
)

relevancy = AnswerRelevancyMetric()
faithfulness = FaithfulnessMetric()

relevancy.measure(test_case)
faithfulness.measure(test_case)

# ===== RAGAS approach =====
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness

data = {
    "question": [question],
    "answer": [answer],
    "contexts": [[context]],
    "ground_truth": [ground_truth]
}
dataset = Dataset.from_dict(data)
results = evaluate(dataset, metrics=[answer_relevancy, faithfulness])
```

**Key Differences:**
- RAGAS: Dataset-centric (better for batches)
- DeepEval: Test-centric (better for pytest)
- RAGAS has more mature RAG metrics
- DeepEval has broader scope (agents, etc.)

---

### From LangChain's Built-in Evaluators

```python
# LangChain approach
from langchain.evaluation import (
    QAEvalChain,
    ContextQAEvalChain,
)

qa_eval_chain = QAEvalChain.from_llm(llm)
context_qa_eval_chain = ContextQAEvalChain.from_llm(llm)

# Evaluate
qa_result = qa_eval_chain.evaluate(
    {"question": question, "answer": answer, "result": ground_truth}
)

# ===== RAGAS approach =====
from ragas import evaluate
from ragas.metrics import answer_correctness, faithfulness

data = {
    "question": [question],
    "answer": [answer],
    "contexts": [[context]],
    "ground_truth": [ground_truth]
}
dataset = Dataset.from_dict(data)
results = evaluate(dataset, metrics=[answer_correctness, faithfulness])
```

**Why RAGAS is Better:**
- More specialized RAG metrics
- Better research foundation
- Cleaner API for batch evaluation
- Works with any framework (not just LangChain)

---

## Real-World Use Cases

### 1. Production Quality Monitoring

```python
# Monitor your production RAG system weekly
import pandas as pd
from datetime import datetime

# Pull last week's production data
prod_data = get_production_rag_data(start_date="2024-01-01")

# Convert to RAGAS format
dataset = Dataset.from_pandas(prod_data)

# Evaluate
results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision]
)

# Alert if quality drops
if results['faithfulness'] < 0.85:
    send_alert(f"Faithfulness dropped to {results['faithfulness']:.2f}")

# Log metrics
log_metrics({
    "date": datetime.now(),
    "faithfulness": results['faithfulness'],
    "relevancy": results['answer_relevancy'],
    "samples": len(prod_data)
})
```

---

### 2. Embedding Model Comparison

```python
# Compare different embedding models for your RAG system
from ragas import evaluate
from ragas.metrics import context_precision, context_recall

# Test data
questions = ["What is machine learning?", ...]
ground_truths = ["Machine learning is...", ...]

# Retrieve with different embeddings
contexts_openai = retrieve_with_openai_embeddings(questions)
contexts_cohere = retrieve_with_cohere_embeddings(questions)
contexts_sentence = retrieve_with_sentence_transformers(questions)

# Evaluate each
models = {
    "OpenAI": contexts_openai,
    "Cohere": contexts_cohere,
    "Sentence-BERT": contexts_sentence
}

for model_name, contexts in models.items():
    data = {
        "question": questions,
        "answer": ground_truths,  # Use GT as answer for retrieval eval
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data)
    results = evaluate(dataset, metrics=[context_precision, context_recall])

    print(f"\n{model_name}:")
    print(f"  Precision: {results['context_precision']:.3f}")
    print(f"  Recall: {results['context_recall']:.3f}")
```

---

### 3. RAG Hyperparameter Tuning

```python
# Find optimal chunk size and overlap
chunk_sizes = [256, 512, 1024, 2048]
overlaps = [0, 50, 100, 200]

best_score = 0
best_config = None

for chunk_size in chunk_sizes:
    for overlap in overlaps:
        # Re-chunk your documents
        rag_system = RAGSystem(chunk_size=chunk_size, overlap=overlap)

        # Generate test outputs
        outputs = rag_system.process_batch(test_questions)

        # Evaluate
        dataset = create_dataset(test_questions, outputs)
        results = evaluate(
            dataset,
            metrics=[faithfulness, context_recall]
        )

        score = (results['faithfulness'] + results['context_recall']) / 2

        if score > best_score:
            best_score = score
            best_config = (chunk_size, overlap)

print(f"Best config: chunk_size={best_config[0]}, overlap={best_config[1]}")
print(f"Score: {best_score:.3f}")
```

---

## Resources

### Official Documentation
- **Main Docs**: https://docs.ragas.io/
- **Getting Started**: https://docs.ragas.io/en/latest/getstarted/
- **Metrics Guide**: https://docs.ragas.io/en/latest/concepts/metrics/
- **API Reference**: https://docs.ragas.io/en/latest/references/

### Research & Papers
- **RAGAS Paper**: https://arxiv.org/abs/2309.15217
  - Title: "RAGAS: Automated Evaluation of Retrieval Augmented Generation"
  - Authors: Shahul Es, Jithin James, et al.
  - Year: 2023
  - Citation: arXiv:2309.15217 [cs.CL]

### Code Examples
- **Official Examples**: https://github.com/explodinggradients/ragas/tree/main/examples
- **Local Example**: `docs/compare_eval_frameworks/ragas_example.py`
- **Notebooks**: https://docs.ragas.io/en/latest/getstarted/rag_evaluation.html

### Community
- **GitHub**: https://github.com/explodinggradients/ragas
- **Discord**: https://discord.gg/5djav8GGNZ
- **Issues**: https://github.com/explodinggradients/ragas/issues
- **Discussions**: https://github.com/explodinggradients/ragas/discussions

### Integration Guides
- **LangChain**: https://docs.ragas.io/en/latest/howtos/integrations/langchain.html
- **LlamaIndex**: https://docs.ragas.io/en/latest/howtos/integrations/llamaindex.html
- **Haystack**: https://docs.ragas.io/en/latest/howtos/integrations/haystack.html

### Tutorials
- **Blog**: https://blog.ragas.io/
- **Video Tutorials**: https://www.youtube.com/results?search_query=ragas+evaluation
- **Community Tutorials**: Various blog posts and Medium articles

---

## Verdict

**RAGAS is the gold standard for RAG evaluation, offering the most comprehensive and research-backed metrics specifically designed for retrieval-augmented generation systems.**

**Rating**: ⭐⭐⭐⭐⭐ (5/5 for RAG evaluation)

### Choose RAGAS if you value:
- ✅ Best-in-class RAG metrics
- ✅ Research-backed methodology
- ✅ Easy-to-use API
- ✅ Comprehensive RAG coverage
- ✅ Framework-agnostic evaluation
- ✅ Strong community and docs

### Choose alternatives if you need:
- ❌ General LLM evaluation → Custom-Evals, DeepEval
- ❌ Real-time observability → Phoenix, LangSmith
- ❌ Agent evaluation → Custom-Evals, LangSmith
- ❌ Pytest integration → DeepEval
- ❌ No LLM API costs → Rule-based metrics

---

## Decision Matrix

### Use RAGAS when:
✅ Building RAG systems (Q&A, document search, knowledge bases)
✅ Need to prevent hallucinations (faithfulness is critical)
✅ Evaluating retrieval quality (embeddings, chunking, ranking)
✅ Benchmarking RAG approaches in research
✅ Running batch evaluations on datasets
✅ Cost is reasonable (~$0.01 per sample acceptable)

### Don't use RAGAS when:
❌ Building non-RAG applications (chatbots, agents, code generation)
❌ Need real-time evaluation with tracing
❌ Require extensive customization of metrics
❌ Zero budget for LLM API calls
❌ Need built-in dashboards and visualization

---

## Quick Reference Card

```python
# Installation
pip install ragas langchain-openai

# Basic Usage
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

data = {
    "question": ["Your question"],
    "answer": ["Model's answer"],
    "contexts": [["Retrieved context"]],
    "ground_truth": ["Expected answer"]  # Optional
}

dataset = Dataset.from_dict(data)
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy])

# Core Metrics
faithfulness         # Prevents hallucinations (0-1)
answer_relevancy     # Question-answer alignment (0-1)
context_precision    # Ranking quality (0-1)
context_recall       # Retrieval coverage (0-1)
answer_correctness   # Accuracy vs ground truth (0-1)
answer_similarity    # Semantic similarity (0-1)

# Cost Estimate
# ~$0.005-0.025 per sample with GPT-4o-mini
# ~$0.05-0.25 per sample with GPT-4
```

---

**Next Steps**:
1. [Read the Deep Dive](framework_readme/03_RAGAS_README.md) (coming soon)
2. [Compare All Frameworks](Compare_All_Eval_Frameworks.md)
3. [Try the Example Code](ragas_example.py)
4. [View Framework Index](FRAMEWORKS_INDEX.md)

**Related**:
- [Custom-Evals Comparison](01_Custom_Evals.md)
- [Phoenix Comparison](02_Phoenix.md) (coming soon)
- [ARES Comparison](04_ARES.md) (coming soon)

---

*Last Updated: January 2026*
*RAGAS Version: 0.1.x*
*Maintained by: Custom-Evals Team*
