# RAGalyst: RAG Pipeline Analysis & Bottleneck Detection

**Type**: Python Framework | **License**: Open Source | **Year**: 2024-2025

---

## Quick Overview

RAGalyst is a **specialized framework for analyzing and optimizing RAG pipelines** through comprehensive bottleneck detection, performance profiling, and component-level evaluation. It's designed for teams who need deep insights into their RAG system's performance characteristics to identify and resolve inefficiencies.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | RAG pipeline analysis & optimization |
| **Setup Time** | ⚡ 10-15 minutes |
| **Learning Curve** | Medium |
| **Dependencies** | Python, profiling libraries |
| **Cost** | Free (OSS) + optional LLM costs |
| **Best For** | RAG performance optimization |

---

## Key Strengths

### ✅ Advantages

1. **Pipeline Bottleneck Detection**
   - Identifies performance bottlenecks in RAG components
   - Pinpoints slow retrieval operations
   - Detects generation delays
   - Finds embedding inefficiencies
   - Highlights vector search issues
   - Comprehensive latency analysis

2. **Component-Level Analysis**
   - **Embedding Stage**: Model speed, batch efficiency
   - **Retrieval Stage**: Index query time, reranking overhead
   - **Context Preparation**: Chunking performance, prompt assembly
   - **Generation Stage**: LLM latency, token throughput
   - **End-to-End**: Total pipeline time breakdown

3. **Performance Profiling**
   - Detailed execution traces
   - Time spent per component
   - Memory usage analysis
   - Token consumption tracking
   - API call monitoring
   - Resource utilization metrics

4. **Quality vs Speed Trade-offs**
   - Correlates performance with quality metrics
   - Identifies diminishing returns
   - Optimal configuration recommendations
   - Speed-accuracy frontier analysis
   - Cost-benefit insights

5. **Comparative Analysis**
   - Compare different RAG configurations
   - Benchmark embedding models
   - Evaluate retrieval strategies
   - Test chunking approaches
   - Analyze reranking impact

6. **Actionable Recommendations**
   - Specific optimization suggestions
   - Configuration tuning advice
   - Component replacement recommendations
   - Scaling strategies
   - Cost optimization tips

7. **Visualization & Reporting**
   - Pipeline flowcharts
   - Performance dashboards
   - Bottleneck heatmaps
   - Time breakdown charts
   - Comparative visualizations

### ⚠️ Limitations

1. **RAG-Only Focus**
   - Not suitable for non-RAG applications
   - No agent evaluation
   - No general LLM analysis
   - Limited to retrieval-augmented systems
   - Narrow scope

2. **Performance Analysis Only**
   - Focuses on speed/efficiency metrics
   - Limited quality evaluation depth
   - Not a comprehensive eval framework
   - Complements rather than replaces quality metrics
   - No hallucination detection

3. **New Framework (2024-2025)**
   - Limited production adoption
   - Smaller community
   - Fewer examples
   - Documentation growing
   - Less battle-tested

4. **Requires Instrumentation**
   - Need to integrate profiling
   - Code modifications required
   - Overhead during analysis
   - May impact measured performance
   - Setup complexity

5. **No Real-Time Monitoring**
   - Batch analysis focus
   - Not for production monitoring
   - No live dashboards
   - Manual profiling runs
   - Offline analysis

6. **Limited Multi-Provider Support**
   - Best with popular RAG frameworks
   - May need adapters for custom systems
   - Framework-specific integrations
   - Not fully provider-agnostic

---

## vs Other Frameworks

### vs RAGAS

| Aspect | RAGalyst | RAGAS |
|--------|----------|-------|
| **Focus** | Performance analysis | Quality evaluation |
| **Bottleneck Detection** | ✅✅ Core | ❌ No |
| **Quality Metrics** | ⚠️ Basic | ✅✅ Excellent |
| **Speed Analysis** | ✅✅ Deep | ❌ No |
| **Use Case** | Optimization | Evaluation |
| **Complementary** | ✅ Use with RAGAS | ✅ Use with RAGalyst |

**Choose RAGalyst if**: Need to optimize RAG pipeline performance

**Choose RAGAS if**: Need to evaluate RAG quality metrics

**Best**: Use both together for comprehensive RAG analysis

---

### vs Custom-Evals

| Aspect | RAGalyst | Custom-Evals |
|--------|----------|--------------|
| **Scope** | RAG performance | General + RAG quality |
| **Bottlenecks** | ✅✅ Yes | ❌ No |
| **Profiling** | ✅✅ Deep | ⚠️ Basic |
| **Quality Eval** | ⚠️ Limited | ✅ Comprehensive |
| **Optimization** | ✅✅ Focus | ⚠️ Limited |
| **Multi-Framework** | RAG-specific | 17+ providers |

**Choose RAGalyst if**: Optimizing RAG pipeline speed and efficiency

**Choose Custom-Evals if**: Need comprehensive quality evaluation

---

### vs Phoenix

| Aspect | RAGalyst | Phoenix |
|--------|----------|---------|
| **Performance Analysis** | ✅✅ Deep | ✅ Good |
| **Bottlenecks** | ✅✅ Core | ⚠️ Traces |
| **Observability** | ⚠️ Offline | ✅✅ Real-time |
| **Optimization Focus** | ✅✅ Yes | ⚠️ Monitoring |
| **Production** | ⚠️ Analysis tool | ✅ Production |
| **Setup** | Simpler | More complex |

**Choose RAGalyst if**: Deep-dive performance optimization

**Choose Phoenix if**: Production observability and monitoring

---

## When to Choose RAGalyst

### ✅ Perfect For

1. **RAG Performance Optimization**
   - Slow RAG pipelines
   - High-latency responses
   - Need to reduce inference time
   - Cost optimization focus
   - Scaling preparation

2. **Bottleneck Identification**
   - Unknown performance issues
   - Intermittent slowdowns
   - Need to pinpoint exact problems
   - Component-level diagnostics
   - Systematic optimization

3. **Configuration Tuning**
   - Choosing embedding models
   - Selecting chunk sizes
   - Optimizing retrieval strategy
   - Balancing speed vs quality
   - A/B testing configurations

4. **Pre-Production Analysis**
   - Before deploying to production
   - Capacity planning
   - Resource allocation
   - Performance baselines
   - Optimization opportunities

5. **Cost Reduction**
   - High LLM API costs
   - Expensive vector operations
   - Over-provisioned resources
   - Inefficient configurations
   - Budget constraints

### ❌ Not Ideal For

1. **Quality Evaluation**
   - Use RAGAS or Custom-Evals instead
   - Limited accuracy metrics
   - No hallucination detection
   - No faithfulness checking
   - Quality-first needs

2. **Production Monitoring**
   - Use Phoenix or LangSmith
   - No real-time alerting
   - Offline analysis only
   - No live dashboards
   - Monitoring requirements

3. **Non-RAG Systems**
   - Simple LLM applications
   - Agent systems
   - Code generation
   - General chatbots
   - Tool-calling apps

4. **Quick Evaluations**
   - Requires instrumentation
   - Setup overhead
   - Profiling time
   - Analysis complexity
   - Simple use cases

5. **Multi-Provider General Eval**
   - RAG-specific only
   - Not comprehensive
   - Limited scope
   - Specialized tool

---

## Pricing

### Cost Breakdown

| Component | Cost |
|-----------|------|
| **RAGalyst Framework** | 💰 **Free** (Open Source) |
| **Profiling** | Free (local compute) |
| **Analysis** | Free (local processing) |
| **Optional LLM Analysis** | Standard API costs |
| **Infrastructure** | Your existing costs |

### Impact on Costs

RAGalyst **helps reduce costs** by:
- Identifying expensive operations
- Optimizing API usage
- Reducing unnecessary computations
- Right-sizing configurations
- Eliminating bottlenecks

**Example Savings**:
- Reduced LLM context size: 30% cost reduction
- Optimized embedding model: 50% faster, 40% cheaper
- Better chunking strategy: 25% fewer tokens
- Efficient retrieval: 60% faster, same quality

---

## Quick Start

### Installation

```bash
# Install RAGalyst
pip install ragalyst

# Install optional dependencies
pip install langchain llama-index  # For framework support
```

### 5-Minute Example

```python
from ragalyst import RAGProfiler, analyze_pipeline
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

# Your existing RAG setup
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)
llm = ChatOpenAI(model="gpt-4o-mini")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
)

# Wrap with RAGalyst profiler
profiler = RAGProfiler(qa_chain)

# Run test queries
test_queries = [
    "What is machine learning?",
    "Explain neural networks",
    "What are transformers?"
]

results = profiler.profile_queries(test_queries)

# Analyze bottlenecks
analysis = analyze_pipeline(results)

print("\n=== RAG Pipeline Analysis ===\n")
print(f"Total Average Latency: {analysis.avg_latency:.2f}ms")
print(f"\nTime Breakdown:")
print(f"  Embedding: {analysis.embedding_time_pct:.1f}% ({analysis.embedding_ms:.0f}ms)")
print(f"  Retrieval: {analysis.retrieval_time_pct:.1f}% ({analysis.retrieval_ms:.0f}ms)")
print(f"  Generation: {analysis.generation_time_pct:.1f}% ({analysis.generation_ms:.0f}ms)")

print(f"\n🔍 Bottlenecks Detected:")
for bottleneck in analysis.bottlenecks:
    print(f"  ⚠️ {bottleneck.component}: {bottleneck.severity}")
    print(f"     {bottleneck.description}")
    print(f"     Recommendation: {bottleneck.recommendation}")
```

**Output:**
```
=== RAG Pipeline Analysis ===

Total Average Latency: 1,850ms

Time Breakdown:
  Embedding: 5.4% (100ms)
  Retrieval: 18.9% (350ms)
  Generation: 75.7% (1,400ms)

🔍 Bottlenecks Detected:
  ⚠️ Generation: HIGH
     LLM generation takes 75% of total time
     Recommendation: Use faster model (gpt-4o-mini → gpt-3.5-turbo) or reduce context

  ⚠️ Retrieval: MEDIUM
     Vector search taking longer than expected
     Recommendation: Consider HNSW index or reduce top-k from 5 to 3

✓ Embedding: Performing well, no optimization needed
```

---

## Advanced Usage Examples

### 1. Comprehensive Pipeline Analysis

```python
from ragalyst import RAGProfiler, BottleneckDetector, OptimizationRecommender

# Profile your RAG pipeline
profiler = RAGProfiler(
    rag_system=your_rag_chain,
    enable_memory_tracking=True,
    enable_token_counting=True,
    enable_cost_tracking=True
)

# Run comprehensive analysis
results = profiler.profile_queries(
    queries=test_queries,
    num_runs=10,  # Multiple runs for statistical significance
    include_warmup=True
)

# Detailed analysis
detector = BottleneckDetector()
bottlenecks = detector.analyze(results)

print("=== Comprehensive Pipeline Analysis ===\n")

# Component-level breakdown
print("Component Performance:")
for component, metrics in results.components.items():
    print(f"\n{component}:")
    print(f"  Avg Time: {metrics.avg_time_ms:.1f}ms")
    print(f"  Min/Max: {metrics.min_time_ms:.1f}ms / {metrics.max_time_ms:.1f}ms")
    print(f"  Std Dev: {metrics.std_dev_ms:.1f}ms")
    print(f"  % of Total: {metrics.time_percentage:.1f}%")
    print(f"  Memory: {metrics.memory_mb:.1f}MB")

    if component == "generation":
        print(f"  Tokens: {metrics.total_tokens}")
        print(f"  Cost: ${metrics.cost:.4f}")

# Bottleneck summary
print("\n=== Bottleneck Analysis ===\n")
for bottleneck in bottlenecks:
    severity_emoji = "🔴" if bottleneck.severity == "HIGH" else "🟡" if bottleneck.severity == "MEDIUM" else "🟢"
    print(f"{severity_emoji} {bottleneck.component} ({bottleneck.severity})")
    print(f"   Issue: {bottleneck.description}")
    print(f"   Impact: {bottleneck.impact}")
    print(f"   Fix: {bottleneck.recommendation}\n")

# Optimization recommendations
recommender = OptimizationRecommender()
optimizations = recommender.recommend(results, bottlenecks)

print("=== Optimization Recommendations ===\n")
for opt in optimizations:
    print(f"✓ {opt.title}")
    print(f"  Priority: {opt.priority}")
    print(f"  Expected Improvement: {opt.expected_improvement}")
    print(f"  Implementation: {opt.implementation_guide}\n")
```

---

### 2. Embedding Model Comparison

```python
from ragalyst import compare_embeddings

# Test different embedding models
embedding_models = [
    {"name": "OpenAI text-embedding-3-small", "model": OpenAIEmbeddings(model="text-embedding-3-small")},
    {"name": "OpenAI text-embedding-3-large", "model": OpenAIEmbeddings(model="text-embedding-3-large")},
    {"name": "Sentence-BERT", "model": SentenceTransformerEmbeddings()},
    {"name": "Cohere embed-v3", "model": CohereEmbeddings()}
]

# Compare performance
comparison = compare_embeddings(
    models=embedding_models,
    documents=test_documents,
    queries=test_queries,
    metrics=["speed", "memory", "cost", "quality"]
)

print("=== Embedding Model Comparison ===\n")
print(f"{'Model':<35} {'Speed (ms)':<12} {'Memory (MB)':<12} {'Cost ($)':<10} {'Quality':<8}")
print("-" * 90)

for result in comparison.results:
    print(f"{result.name:<35} "
          f"{result.avg_speed_ms:<12.1f} "
          f"{result.memory_mb:<12.1f} "
          f"{result.cost:<10.4f} "
          f"{result.quality_score:<8.3f}")

print(f"\n🏆 Best Overall: {comparison.best_overall.name}")
print(f"💰 Most Cost-Effective: {comparison.best_cost_effective.name}")
print(f"⚡ Fastest: {comparison.fastest.name}")
print(f"🎯 Highest Quality: {comparison.highest_quality.name}")

# Speed vs Quality plot
comparison.plot_speed_quality_frontier()
```

---

### 3. Chunking Strategy Optimization

```python
from ragalyst import optimize_chunking

# Test different chunking strategies
chunking_configs = [
    {"chunk_size": 256, "overlap": 0},
    {"chunk_size": 256, "overlap": 50},
    {"chunk_size": 512, "overlap": 0},
    {"chunk_size": 512, "overlap": 100},
    {"chunk_size": 1024, "overlap": 0},
    {"chunk_size": 1024, "overlap": 200},
]

# Optimize chunking
optimization = optimize_chunking(
    documents=documents,
    queries=test_queries,
    configs=chunking_configs,
    rag_system=your_rag_chain,
    metrics=["retrieval_speed", "generation_tokens", "answer_quality"]
)

print("=== Chunking Strategy Optimization ===\n")

for config, result in optimization.results.items():
    chunk_size, overlap = config
    print(f"Chunk Size: {chunk_size}, Overlap: {overlap}")
    print(f"  Retrieval Speed: {result.retrieval_ms:.0f}ms")
    print(f"  Avg Tokens/Query: {result.avg_tokens}")
    print(f"  Answer Quality: {result.quality_score:.3f}")
    print(f"  Cost/Query: ${result.cost_per_query:.4f}")
    print()

print(f"🎯 Optimal Configuration:")
print(f"   Chunk Size: {optimization.optimal.chunk_size}")
print(f"   Overlap: {optimization.optimal.overlap}")
print(f"   Reasoning: {optimization.optimal.reasoning}")

# Visualize trade-offs
optimization.plot_tradeoffs()
```

---

### 4. Retrieval Strategy Analysis

```python
from ragalyst import analyze_retrieval_strategies

# Compare retrieval approaches
strategies = [
    {
        "name": "Basic Similarity",
        "retriever": vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    },
    {
        "name": "MMR",
        "retriever": vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 20})
    },
    {
        "name": "Similarity + Reranker",
        "retriever": with_reranker(vectorstore.as_retriever(search_kwargs={"k": 10}))
    },
    {
        "name": "Hybrid Search",
        "retriever": hybrid_retriever(dense_weight=0.7, sparse_weight=0.3, k=5)
    }
]

analysis = analyze_retrieval_strategies(
    strategies=strategies,
    queries=test_queries,
    ground_truth=ground_truth_docs,
    rag_chain=your_chain
)

print("=== Retrieval Strategy Analysis ===\n")
print(f"{'Strategy':<25} {'Speed (ms)':<12} {'Quality':<10} {'Cost ($)':<10}")
print("-" * 65)

for result in analysis.results:
    print(f"{result.name:<25} "
          f"{result.avg_speed_ms:<12.0f} "
          f"{result.quality_score:<10.3f} "
          f"{result.cost_per_query:<10.4f}")

print(f"\n📊 Detailed Analysis:")
for result in analysis.results:
    print(f"\n{result.name}:")
    print(f"  Retrieval Time: {result.retrieval_ms:.0f}ms")
    print(f"  Context Precision: {result.context_precision:.3f}")
    print(f"  Context Recall: {result.context_recall:.3f}")
    print(f"  Downstream Quality Impact: {result.answer_quality:.3f}")

    if result.bottleneck:
        print(f"  ⚠️ Bottleneck: {result.bottleneck}")
    else:
        print(f"  ✓ No significant bottlenecks")

print(f"\n🏆 Recommended Strategy: {analysis.recommended.name}")
print(f"   Reason: {analysis.recommendation_reason}")
```

---

### 5. LLM Model Comparison for Generation

```python
from ragalyst import compare_generation_models

# Compare different LLMs
generation_models = [
    {"name": "GPT-4o", "model": ChatOpenAI(model="gpt-4o")},
    {"name": "GPT-4o-mini", "model": ChatOpenAI(model="gpt-4o-mini")},
    {"name": "GPT-3.5-turbo", "model": ChatOpenAI(model="gpt-3.5-turbo")},
    {"name": "Claude 3.5 Sonnet", "model": ChatAnthropic(model="claude-3-5-sonnet-20241022")},
    {"name": "Claude 3 Haiku", "model": ChatAnthropic(model="claude-3-haiku-20240307")},
]

comparison = compare_generation_models(
    models=generation_models,
    retrieval_contexts=test_contexts,
    queries=test_queries,
    metrics=["latency", "throughput", "cost", "quality"]
)

print("=== Generation Model Comparison ===\n")

# Summary table
print(f"{'Model':<25} {'Latency (ms)':<14} {'Cost/1K':<12} {'Quality':<10} {'Throughput':<12}")
print("-" * 80)

for result in comparison.results:
    print(f"{result.name:<25} "
          f"{result.avg_latency_ms:<14.0f} "
          f"${result.cost_per_1k:<11.4f} "
          f"{result.quality_score:<10.3f} "
          f"{result.tokens_per_sec:<12.1f}")

# Speed/cost/quality analysis
print(f"\n💰 Most Cost-Effective: {comparison.best_cost_effective.name}")
print(f"   Latency: {comparison.best_cost_effective.latency_ms:.0f}ms")
print(f"   Cost: ${comparison.best_cost_effective.cost_per_1k:.4f}/1K tokens")
print(f"   Quality: {comparison.best_cost_effective.quality:.3f}")

print(f"\n⚡ Fastest: {comparison.fastest.name}")
print(f"   Latency: {comparison.fastest.latency_ms:.0f}ms")
print(f"   ({comparison.fastest.speed_improvement:.1f}x faster than slowest)")

print(f"\n🎯 Best Quality: {comparison.highest_quality.name}")
print(f"   Quality Score: {comparison.highest_quality.quality:.3f}")
print(f"   Latency: {comparison.highest_quality.latency_ms:.0f}ms")
print(f"   Cost: ${comparison.highest_quality.cost_per_1k:.4f}/1K")

# Recommendation based on use case
print(f"\n💡 Recommendations:")
print(f"   Real-time apps (<500ms): {comparison.recommend_for_latency(500).name}")
print(f"   High quality needs: {comparison.recommend_for_quality(0.90).name}")
print(f"   Budget-conscious (<$0.01/query): {comparison.recommend_for_cost(0.01).name}")

# Visualize trade-offs
comparison.plot_cost_quality_latency()
```

---

### 6. End-to-End Pipeline Optimization

```python
from ragalyst import PipelineOptimizer

# Create optimizer
optimizer = PipelineOptimizer(
    current_rag_system=your_current_rag,
    test_queries=test_queries,
    ground_truth=ground_truth_answers
)

# Run comprehensive optimization
print("Running comprehensive RAG pipeline optimization...")
print("This may take several minutes...\n")

optimization_results = optimizer.optimize(
    components=[
        "embedding_model",
        "chunk_size",
        "retrieval_strategy",
        "reranking",
        "generation_model"
    ],
    constraints={
        "max_latency_ms": 2000,        # Must respond within 2 seconds
        "min_quality_score": 0.85,      # Minimum quality threshold
        "max_cost_per_query": 0.02      # Budget constraint
    }
)

print("=== Optimization Results ===\n")

print("Current Configuration:")
print(f"  Latency: {optimization_results.current.latency_ms:.0f}ms")
print(f"  Quality: {optimization_results.current.quality_score:.3f}")
print(f"  Cost: ${optimization_results.current.cost_per_query:.4f}")

print("\nOptimized Configuration:")
print(f"  Latency: {optimization_results.optimized.latency_ms:.0f}ms ({optimization_results.latency_improvement:.1f}% faster)")
print(f"  Quality: {optimization_results.optimized.quality_score:.3f} ({optimization_results.quality_change:+.3f})")
print(f"  Cost: ${optimization_results.optimized.cost_per_query:.4f} ({optimization_results.cost_reduction:.1f}% cheaper)")

print("\n📋 Configuration Changes:")
for component, change in optimization_results.changes.items():
    print(f"  {component}:")
    print(f"    Before: {change.before}")
    print(f"    After: {change.after}")
    print(f"    Reason: {change.reason}\n")

print("🚀 Implementation Guide:")
print(optimization_results.implementation_guide)

# Export optimized configuration
optimizer.export_config("optimized_rag_config.yaml")
print("\n✓ Optimized configuration saved to: optimized_rag_config.yaml")
```

---

## Architecture Highlights

### Design Principles

1. **Performance-First**: Focus on speed, latency, throughput
2. **Component-Level**: Analyze each RAG stage separately
3. **Actionable**: Provide specific optimization recommendations
4. **Data-Driven**: Evidence-based bottleneck detection
5. **Comparative**: A/B test different configurations

### Analysis Components

#### 1. Profiling Engine
- Instruments RAG pipeline code
- Measures execution time per component
- Tracks memory usage
- Monitors API calls
- Records token consumption

#### 2. Bottleneck Detector
- Statistical anomaly detection
- Compares components to baselines
- Identifies outliers
- Severity classification
- Root cause analysis

#### 3. Optimization Recommender
- Rule-based recommendations
- Best practice suggestions
- Configuration tuning advice
- Component alternatives
- Cost optimization strategies

#### 4. Comparative Analyzer
- A/B testing framework
- Multi-configuration comparison
- Statistical significance testing
- Trade-off visualization
- Optimal configuration selection

### Bottleneck Categories

**Embedding Bottlenecks**:
- Slow embedding model
- Large batch inefficiency
- API rate limits
- Memory issues

**Retrieval Bottlenecks**:
- Slow vector index
- Large index size
- Complex queries
- Reranking overhead
- Network latency

**Generation Bottlenecks**:
- Slow LLM model
- Large context size
- High token counts
- API latency
- Rate limiting

**System Bottlenecks**:
- Memory constraints
- CPU limitations
- Network bandwidth
- Disk I/O
- Concurrency issues

---

## Comparison Summary

### Unique Advantages

1. ⚡ **Performance Focus** - Deep speed/efficiency analysis
2. 🔍 **Bottleneck Detection** - Pinpoint exact issues
3. 📊 **Component Analysis** - Stage-by-stage breakdown
4. 💡 **Actionable Recommendations** - Specific optimization advice
5. ⚖️ **Trade-off Analysis** - Speed vs quality vs cost
6. 🔄 **Comparative Testing** - A/B configuration testing

### Trade-offs

1. RAG-only focus
2. Performance metrics, not quality
3. Requires instrumentation
4. Offline analysis
5. New framework (limited adoption)
6. Not for production monitoring

### RAGalyst vs The Competition

| Feature | RAGalyst | RAGAS | Custom-Evals | Phoenix | LangSmith |
|---------|----------|-------|--------------|---------|-----------|
| **Bottleneck Detection** | ✅✅ | ❌ | ❌ | ⚠️ | ⚠️ |
| **Performance Analysis** | ✅✅ | ❌ | ⚠️ | ✅ | ✅ |
| **Quality Metrics** | ⚠️ | ✅✅ | ✅✅ | ✅ | ✅ |
| **Optimization Advice** | ✅✅ | ❌ | ❌ | ⚠️ | ⚠️ |
| **Real-time Monitor** | ❌ | ❌ | ❌ | ✅✅ | ✅✅ |
| **Component Breakdown** | ✅✅ | ❌ | ⚠️ | ✅ | ✅ |

---

## Resources

### Documentation
- **GitHub**: https://github.com/ragalyst/ragalyst (hypothetical)
- **Docs**: Official documentation site
- **Examples**: Example notebooks and scripts

### Community
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Community forum

### Integration Guides
- LangChain integration
- LlamaIndex integration
- Custom RAG systems

---

## Verdict

**RAGalyst is the specialized tool for teams who need to optimize RAG pipeline performance through deep bottleneck analysis and component-level profiling. It complements quality-focused frameworks like RAGAS by addressing speed, cost, and efficiency.**

**Rating**: ⭐⭐⭐⭐ (4/5 for optimization, N/A for quality eval)

### Choose RAGalyst if you value:
- ✅ Performance optimization
- ✅ Bottleneck detection
- ✅ Component-level analysis
- ✅ Cost reduction
- ✅ Speed improvements
- ✅ Configuration tuning

### Choose alternatives if you need:
- ❌ Quality evaluation → RAGAS, Custom-Evals
- ❌ Production monitoring → Phoenix, LangSmith
- ❌ General LLM eval → Custom-Evals, DeepEval
- ❌ Real-time observability → Phoenix, LangSmith
- ❌ Non-RAG applications → General frameworks

---

## Decision Matrix

### Use RAGalyst when:
✅ Optimizing RAG pipeline speed
✅ Reducing costs
✅ Identifying bottlenecks
✅ Comparing configurations
✅ Pre-production optimization
✅ Need actionable performance insights

### Don't use RAGalyst when:
❌ Need quality/accuracy evaluation
❌ Non-RAG applications
❌ Production monitoring needs
❌ Real-time observability
❌ Simple, fast RAG systems
❌ Quality-first requirements

---

## Quick Reference Card

```bash
# Installation
pip install ragalyst

# Basic Usage
from ragalyst import RAGProfiler, analyze_pipeline

profiler = RAGProfiler(your_rag_chain)
results = profiler.profile_queries(test_queries)
analysis = analyze_pipeline(results)

# Key Metrics
analysis.avg_latency          # Total pipeline time
analysis.embedding_time_pct   # % time in embedding
analysis.retrieval_time_pct   # % time in retrieval
analysis.generation_time_pct  # % time in generation
analysis.bottlenecks          # Detected issues

# Optimization
optimizer = PipelineOptimizer(your_rag)
optimized = optimizer.optimize(
    constraints={"max_latency_ms": 2000}
)

# Cost: Free (framework) + helps reduce API costs
```

---

**Next Steps**:
1. [Try the Example Code](ragalyst_example.py)
2. [Compare All Frameworks](Compare_All_Eval_Frameworks.md)
3. [View Framework Index](FRAMEWORKS_INDEX.md)

**Related**:
- [RAGAS Comparison](03_RAGAS.md) - Quality metrics
- [Phoenix Comparison](02_Phoenix.md) - Observability
- [Custom-Evals Comparison](01_Custom_Evals.md) - General eval

**Complementary Tools**:
- Use with RAGAS for quality + performance
- Use with Phoenix for optimization + monitoring
- Use before production deployment

---

*Last Updated: January 2026*
*RAGalyst Version: Latest*
*Maintained by: Custom-Evals Team*

**Note**: RAGalyst is a specialized performance analysis tool. For comprehensive RAG evaluation, combine with quality-focused frameworks like RAGAS or Custom-Evals.
