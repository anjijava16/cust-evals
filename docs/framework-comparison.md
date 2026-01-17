# Framework Comparison

Comparison of Custom Evals with other popular evaluation frameworks.

## Overview

This document compares Custom Evals with:
- **Phoenix Evals** - Our inspiration
- **DeepEval** - Comprehensive LLM evaluation
- **RAGAS** - RAG-focused evaluation

## Quick Comparison

| Feature | Custom Evals | Phoenix Evals | DeepEval | RAGAS |
|---------|--------------|---------------|----------|-------|
| **Code Metrics** | 3 | Many | Few | Few |
| **LLM Evaluators** | 6 | Many | 50+ | 4 core |
| **RAG Specific** | 2 | Yes | Yes | Yes (primary focus) |
| **Ground Truth** | Flexible | Flexible | Required | Optional |
| **Async Support** | ✅ | ✅ | ✅ | ✅ |
| **Providers** | OpenAI, Anthropic | Many | Many | Many |
| **Complexity** | Low (POC) | Medium | Medium | Low-Medium |

## Custom Evals vs Phoenix Evals

### Similarities

✅ Two-layer API (evaluate/_evaluate)
✅ Score object structure
✅ Flexible ground truth
✅ Async support
✅ describe() method

### Differences

| Feature | Custom Evals | Phoenix Evals |
|---------|--------------|---------------|
| **Scope** | POC with 9 evaluators | Production with many evaluators |
| **Tracing** | None | OpenTelemetry integrated |
| **Validation** | Basic | Pydantic models |
| **Maturity** | POC | Production-ready |

## Custom Evals vs DeepEval

### What We Learned

From DeepEval, we adopted:
- Faithfulness evaluation concept
- Answer relevancy approach
- Reference-free design for RAG

### What's Different

| Feature | Custom Evals | DeepEval |
|---------|--------------|----------|
| **Focus** | POC for RAG + general | Comprehensive evaluation |
| **Metrics** | 9 core metrics | 50+ metrics |
| **G-Eval** | Not implemented | ✅ Custom metrics framework |
| **Safety** | Not yet | ✅ Bias, toxicity |
| **Agentic** | Not yet | ✅ Task completion, tool correctness |

## Custom Evals vs RAGAS

### What We Learned

From RAGAS, we adopted:
- Reference-free RAG evaluation
- Statement-level faithfulness
- Research-backed approach

### What's Different

| Feature | Custom Evals | RAGAS |
|---------|--------------|-------|
| **Scope** | General + RAG | RAG-focused |
| **RAG Metrics** | 2 (Phase 1) | 4 core metrics |
| **General Eval** | ✅ More general evaluators | Limited |
| **Integration** | Standalone | Integrates with many tools |

## Metric Comparison

### General Evaluation

| Metric | Custom Evals | Phoenix | DeepEval | RAGAS |
|--------|--------------|---------|----------|-------|
| Hallucination | ✅ | ✅ | ✅ | - |
| Correctness | ✅ | ✅ | - | - |
| Relevance | ✅ | ✅ | - | - |
| Coherence | ✅ | ✅ | - | - |

### RAG Evaluation

| Metric | Custom Evals | Phoenix | DeepEval | RAGAS |
|--------|--------------|---------|----------|-------|
| Faithfulness | ✅ | ✅ | ✅ | ✅ |
| Answer Relevancy | ✅ | ✅ | ✅ | ✅ |
| Context Precision | ⬜ Phase 2 | ✅ | ✅ | ✅ |
| Context Recall | ⬜ Phase 2 | ✅ | ✅ | ✅ |

### Safety Metrics

| Metric | Custom Evals | Phoenix | DeepEval | RAGAS |
|--------|--------------|---------|----------|-------|
| Bias | ⬜ Phase 3 | ✅ | ✅ | - |
| Toxicity | ⬜ Phase 3 | ✅ | ✅ | - |

## When to Use Each

### Use Custom Evals When

✅ Building a POC or MVP
✅ Need simple, lightweight evaluation
✅ Want flexibility without complexity
✅ Learning evaluation concepts

### Use Phoenix Evals When

✅ Need production-grade evaluation
✅ Want OpenTelemetry tracing
✅ Need comprehensive metrics
✅ Building on Phoenix ecosystem

### Use DeepEval When

✅ Need extensive metric library
✅ Want G-Eval custom metrics
✅ Need agentic evaluation
✅ Require safety metrics

### Use RAGAS When

✅ Focused on RAG systems only
✅ Want research-backed metrics
✅ Need integration with many tools
✅ Prefer reference-free approach

## Future Roadmap

Custom Evals plans to add (from DeepEval/RAGAS):

**Phase 2: Context Evaluation**
- ContextPrecisionEvaluator
- ContextRecallEvaluator
- ContextRelevancyEvaluator

**Phase 3: Safety**
- BiasEvaluator
- ToxicityEvaluator

**Phase 4: Advanced (Maybe)**
- G-Eval framework
- Multi-turn conversation
- Agentic metrics

## Complete Comparison

See the full comparison document:
- **[Complete Framework Comparison](../FRAMEWORK_COMPARISON.md)** - Detailed analysis

## Next Steps

- **[Getting Started](getting-started.md)** - Start using Custom Evals
- **[RAG Evaluators](evaluators/rag-specific.md)** - RAG evaluation docs
- **[Examples](examples.md)** - Working examples
