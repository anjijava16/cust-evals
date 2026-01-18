# Evaluation Framework Comparison

Comparison of **cust-evals** with **DeepEval** and **RAGAS** frameworks to identify valuable metrics to add.

## Executive Summary

**What We Have**: 7 evaluators (3 code-based, 4 LLM-based)
**What to Add**: RAG-specific metrics (Faithfulness, Answer Relevancy, Context Precision/Recall/Relevancy), Bias, Toxicity

---

## Framework Overview

### cust-evals (Our Framework)
- **Type**: POC evaluation framework inspired by Phoenix Evals
- **Focus**: General LLM evaluation with flexible ground truth support
- **Architecture**: Two-layer API (public/internal methods), decorator pattern for code metrics
- **Providers**: OpenAI, Anthropic
- **Key Features**: Sync/async evaluation, describe() introspection, flexible ground truth

### DeepEval
- **Type**: Open-source LLM evaluation framework
- **Focus**: Comprehensive LLM testing with 50+ metrics
- **Architecture**: LLM-as-judge with chain-of-thoughts (CoT)
- **Key Features**: G-Eval custom metrics, RAG evaluation, agentic metrics, multi-turn metrics, safety metrics
- **Source**: [GitHub - confident-ai/deepeval](https://github.com/confident-ai/deepeval)

### RAGAS
- **Type**: Reference-free RAG evaluation framework
- **Focus**: RAG pipeline evaluation
- **Architecture**: LLM-as-judge, reference-free evaluation
- **Key Features**: Research-backed metrics, integration with popular tools
- **Source**: [RAGAS Documentation](https://docs.ragas.io/en/stable/)

---

## Metric Comparison

| Metric Category | cust-evals | DeepEval | RAGAS | Priority to Add |
|-----------------|------------|----------|-------|-----------------|
| **General Evaluation** |
| Hallucination | ✅ | ✅ | - | - |
| Correctness | ✅ | - | - | - |
| Relevance | ✅ | - | - | - |
| Coherence | ✅ | - | - | - |
| Exact Match | ✅ | - | - | - |
| Sentiment | ✅ | ✅ Toxicity/Bias | - | ⭐ Add Toxicity/Bias |
| Custom Accuracy | ✅ | - | - | - |
| **RAG-Specific Metrics** |
| Faithfulness | ❌ | ✅ | ✅ | ⭐⭐⭐ High Priority |
| Answer Relevancy | ❌ | ✅ | ✅ | ⭐⭐⭐ High Priority |
| Context Precision | ❌ | ✅ | ✅ | ⭐⭐ Medium Priority |
| Context Recall | ❌ | ✅ | ✅ | ⭐⭐ Medium Priority |
| Context Relevancy | ❌ | ✅ | - | ⭐⭐ Medium Priority |
| **Advanced Metrics** |
| G-Eval (Custom) | ❌ | ✅ | - | ⭐ Low Priority (complex) |
| Task Completion | ❌ | ✅ | - | ⭐ Low Priority |
| Tool Correctness | ❌ | ✅ | - | ⭐ Low Priority |
| Bias Detection | ❌ | ✅ | - | ⭐⭐ Medium Priority |
| Toxicity Detection | ❌ | ✅ | - | ⭐⭐ Medium Priority |
| Summarization | ❌ | ✅ | - | ⭐ Low Priority |
| **Multi-turn Metrics** |
| Knowledge Retention | ❌ | ✅ | - | - |
| Conversation Completeness | ❌ | ✅ | - | - |
| Conversation Relevancy | ❌ | ✅ | - | - |
| Role Adherence | ❌ | ✅ | - | - |

---

## Detailed Metric Descriptions

### 1. Faithfulness ⭐⭐⭐

**What it is**: Measures whether the generated response contains hallucinations relative to the retrieval context.

**DeepEval Implementation**:
- Evaluates if LLM output is grounded in retrieval context
- Uses LLM-as-judge
- Binary or scored output

**RAGAS Implementation**:
- Breaks answer into statements
- Verifies each statement against context
- Formula: `Faithfulness = (# statements supported by context) / (# total statements)`

**Why add it**: Critical for RAG systems. Different from our HallucinationEvaluator which evaluates against context but doesn't break down into statements.

**Ground Truth**: Not required (reference-free)

---

### 2. Answer Relevancy ⭐⭐⭐

**What it is**: Measures how relevant the generated answer is to the input query.

**DeepEval Implementation**:
- Evaluates prompt template effectiveness
- Checks if output is helpful and relevant

**RAGAS Implementation**:
- Reference-free evaluation
- Uses LLM-as-judge
- Focuses on query-answer alignment

**Why add it**: Our RelevanceEvaluator checks context-to-query relevance, but this checks answer-to-query relevance (different focus).

**Ground Truth**: Not required (reference-free)

---

### 3. Context Precision ⭐⭐

**What it is**: Measures whether retrieved context is ranked correctly (most relevant first).

**DeepEval Implementation**:
- Evaluates reranker performance
- Checks if relevant nodes are ranked higher

**RAGAS Implementation**:
- Proportion of retrieved context that's actually relevant
- Focuses on retrieval quality

**Why add it**: Useful for RAG evaluation, measures retrieval precision.

**Ground Truth**: May require (RAGAS uses it)

---

### 4. Context Recall ⭐⭐

**What it is**: Measures if retrieval context contains all information needed for ideal output.

**DeepEval Implementation**:
- Evaluates embedding model quality
- Checks completeness of retrieval

**RAGAS Implementation**:
- **Only metric that requires ground truth**
- Formula: `Context Recall = (# statements in GT that can be attributed to context) / (# total statements in GT)`

**Why add it**: Complements Context Precision, measures retrieval completeness.

**Ground Truth**: Required

---

### 5. Context Relevancy ⭐⭐

**What it is**: Measures how relevant the retrieval context is to the input query.

**DeepEval Implementation**:
- Evaluates chunk size and top-K settings
- Checks for irrelevant information

**Why add it**: Different from our RelevanceEvaluator (which is more general).

**Ground Truth**: Not required (reference-free)

---

### 6. Bias Detection ⭐⭐

**What it is**: Detects biased content in LLM outputs.

**DeepEval Implementation**:
- LLM-as-judge
- Checks for various bias types (gender, racial, political, etc.)

**Why add it**: Important for safety and fairness, not covered by our metrics.

**Ground Truth**: Not required (reference-free)

---

### 7. Toxicity Detection ⭐⭐

**What it is**: Detects toxic or harmful content in LLM outputs.

**DeepEval Implementation**:
- LLM-as-judge
- Checks for offensive, harmful, or inappropriate content

**Why add it**: Critical for production safety, extends our sentiment_score metric.

**Ground Truth**: Not required (reference-free)

---

## Recommended Implementation Plan

### Phase 1: Core RAG Metrics (High Priority)

1. **FaithfulnessEvaluator** ⭐⭐⭐
   - Reference-free
   - Breaks answer into statements
   - Verifies each against context
   - Extends our HallucinationEvaluator with statement-level analysis

2. **AnswerRelevancyEvaluator** ⭐⭐⭐
   - Reference-free
   - Evaluates answer-to-query alignment
   - Complements our RelevanceEvaluator

### Phase 2: Context Evaluation Metrics (Medium Priority)

3. **ContextPrecisionEvaluator** ⭐⭐
   - May require ground truth
   - Evaluates retrieval precision
   - Useful for RAG tuning

4. **ContextRecallEvaluator** ⭐⭐
   - Requires ground truth
   - Evaluates retrieval completeness
   - Pairs with ContextPrecision

5. **ContextRelevancyEvaluator** ⭐⭐
   - Reference-free
   - Evaluates context-query relevance
   - More specific than our RelevanceEvaluator

### Phase 3: Safety Metrics (Medium Priority)

6. **BiasEvaluator** ⭐⭐
   - Reference-free
   - Detects bias in outputs
   - Important for production safety

7. **ToxicityEvaluator** ⭐⭐
   - Reference-free
   - Detects harmful content
   - Critical for safety

---

## Implementation Strategy

### Architecture Considerations

**Fits Our Pattern**:
- All these metrics follow our LLMEvaluator base class pattern
- Most are reference-free (matches our design)
- Use LLM-as-judge (we already support this)

**New Capabilities Needed**:
- **Statement extraction**: For Faithfulness metric
- **Multiple context support**: For Context metrics (need to handle list of retrieved documents)
- **Ranking evaluation**: For Context Precision

### Code Structure

```python
# Phase 1: Core RAG Metrics
class FaithfulnessEvaluator(LLMEvaluator):
    NAME = "faithfulness"
    DIRECTION = "maximize"
    REQUIRES_GROUND_TRUTH = False
    CHOICES = {"faithful": 1.0, "unfaithful": 0.0}
    # Statement-level verification

class AnswerRelevancyEvaluator(LLMEvaluator):
    NAME = "answer_relevancy"
    DIRECTION = "maximize"
    REQUIRES_GROUND_TRUTH = False
    CHOICES = {"relevant": 1.0, "irrelevant": 0.0}
    # Query-answer alignment check

# Phase 2: Context Evaluation
class ContextPrecisionEvaluator(LLMEvaluator):
    NAME = "context_precision"
    DIRECTION = "maximize"
    REQUIRES_GROUND_TRUTH = True  # Optional
    # Multiple contexts support needed

class ContextRecallEvaluator(LLMEvaluator):
    NAME = "context_recall"
    DIRECTION = "maximize"
    REQUIRES_GROUND_TRUTH = True  # Required
    # Verify GT statements in contexts

class ContextRelevancyEvaluator(LLMEvaluator):
    NAME = "context_relevancy"
    DIRECTION = "maximize"
    REQUIRES_GROUND_TRUTH = False
    # Context-query relevance

# Phase 3: Safety Metrics
class BiasEvaluator(LLMEvaluator):
    NAME = "bias"
    DIRECTION = "minimize"
    REQUIRES_GROUND_TRUTH = False
    CHOICES = {"unbiased": 0.0, "biased": 1.0}

class ToxicityEvaluator(LLMEvaluator):
    NAME = "toxicity"
    DIRECTION = "minimize"
    REQUIRES_GROUND_TRUTH = False
    CHOICES = {"non_toxic": 0.0, "toxic": 1.0}
```

---

## Comparison Summary

### What Makes cust-evals Unique

✅ **Clean two-layer API** (evaluate/\_evaluate pattern)
✅ **Flexible ground truth** (works with or without)
✅ **Simple decorator pattern** for code metrics
✅ **Async support** with thread pool
✅ **Introspection** via describe()
✅ **Multi-provider support** (OpenAI, Anthropic)

### What We Can Learn from DeepEval

1. **Comprehensive metric library** (50+ metrics)
2. **G-Eval framework** for custom criteria
3. **Agentic and multi-turn metrics**
4. **Safety metrics** (bias, toxicity)
5. **Threshold-based success** (0.5 default)

### What We Can Learn from RAGAS

1. **Reference-free evaluation** (we already do this!)
2. **RAG-specific focus**
3. **Statement-level analysis** for faithfulness
4. **Research-backed formulas**
5. **Simple integration**

---

## Next Steps

### Immediate Actions

1. ✅ Create this comparison document
2. ⬜ Implement Phase 1 metrics (Faithfulness, Answer Relevancy)
3. ⬜ Add examples for RAG evaluation
4. ⬜ Update documentation

### Future Enhancements

1. Add Phase 2 metrics (Context Precision/Recall/Relevancy)
2. Add Phase 3 metrics (Bias, Toxicity)
3. Consider G-Eval framework for custom metrics
4. Add multi-turn conversation metrics
5. Add agentic metrics

---

## References

### DeepEval
- [GitHub - confident-ai/deepeval](https://github.com/confident-ai/deepeval)
- [DeepEval Documentation](https://deepeval.com)
- [RAG Evaluation Metrics Guide](https://www.confident-ai.com/blog/rag-evaluation-metrics-answer-relevancy-faithfulness-and-more)
- [LLM Evaluation Metrics Ultimate Guide](https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation)

### RAGAS
- [RAGAS Documentation](https://docs.ragas.io/en/stable/)
- [Available Metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
- [Metrics Overview](https://docs.ragas.io/en/stable/concepts/metrics/overview/)
- [Beginner's Guide to RAGAS Score](https://www.projectpro.io/article/ragas-score-llm/1156)
- [Arxiv Paper](https://arxiv.org/abs/2309.15217)

### General
- [Top 5 RAG Evaluation Platforms in 2026](https://www.getmaxim.ai/articles/top-5-rag-evaluation-platforms-in-2026/)
- [RAG Evaluation: 2026 Metrics and Benchmarks](https://labelyourdata.com/articles/llm-fine-tuning/rag-evaluation)

---

## Conclusion

**cust-evals is well-positioned** to add valuable metrics from DeepEval and RAGAS. Our architecture already supports:
- Reference-free evaluation ✅
- LLM-as-judge pattern ✅
- Flexible ground truth ✅
- Clean API design ✅

**Priority additions**:
1. ⭐⭐⭐ **Faithfulness** - Core RAG metric
2. ⭐⭐⭐ **Answer Relevancy** - Core RAG metric
3. ⭐⭐ **Context Precision/Recall** - RAG optimization
4. ⭐⭐ **Bias/Toxicity** - Safety metrics

With these additions, **cust-evals will have comprehensive coverage** of LLM evaluation needs including general evaluation, RAG-specific metrics, and safety checks.
