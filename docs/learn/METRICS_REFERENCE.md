# Complete LLM Evaluation Metrics Reference

**Comprehensive catalog of ALL evaluation metrics covered in lessons 1-20**

---

## 📚 Overview

This reference provides a complete catalog of evaluation metrics for:
- Text Generation Quality
- LLM Safety & Alignment
- RAG Systems
- Agent Systems
- Task-Specific Evaluation
- Human-Centered Quality
- Efficiency & Performance

**Total Metrics Covered**: 100+ comprehensive evaluation metrics

---

## 🎯 Quick Metric Selector

### By Use Case

| Use Case | Primary Metrics | See Lesson |
|----------|----------------|------------|
| **Question Answering** | Exact Match, Token F1, Semantic Accuracy | 15, 19 |
| **Code Generation** | Pass@K, Execution Accuracy, Syntax Correctness | 19 |
| **Summarization** | ROUGE-1/2/L, Coherence, Completeness | 15, 19 |
| **Translation** | BLEU, METEOR, Fluency | 15 |
| **RAG Systems** | Faithfulness, Retrieval Recall@K, Answer Correctness | 4, 12, 17 |
| **Agent Systems** | Task Success Rate, Tool Accuracy, Error Recovery | 13, 18 |
| **Safety Evaluation** | Toxicity, Hallucination, Refusal Accuracy | 10, 16 |
| **Production Deployment** | Latency (P95), Throughput, Cost/Request | 20 |

---

## 📊 1. Text Quality & Similarity Metrics

**Source**: Lesson 15

###  1.1 N-Gram Based Metrics

#### **BLEU (Bilingual Evaluation Understudy)**
- **Purpose**: Machine translation, text generation
- **Range**: 0.0 - 1.0 (higher is better)
- **Formula**: BP × exp(Σ wn × log pn)
- **Use When**: Precise matching needed
- **Avoid When**: Creative writing, open-ended generation
- **Lesson**: 15

#### **ROUGE (Recall-Oriented Understudy for Gisting Evaluation)**
- **Variants**: ROUGE-1, ROUGE-2, ROUGE-L
- **Purpose**: Summarization, content coverage
- **Range**: 0.0 - 1.0 (higher is better)
- **Formula**: Recall-based n-gram overlap
- **Use When**: Summarization tasks
- **Lesson**: 15

#### **METEOR (Metric for Evaluation of Translation with Explicit ORdering)**
- **Purpose**: Translation with synonym support
- **Range**: 0.0 - 1.0 (higher is better)
- **Features**: Stemming, synonyms, paraphrases
- **Use When**: Paraphrasing evaluation
- **Lesson**: 15

### 1.2 Model-Based Metrics

#### **Perplexity**
- **Purpose**: Language model quality
- **Range**: 1 - ∞ (lower is better)
- **Formula**: exp(-1/N × Σ log P(wi))
- **Use When**: Comparing language models
- **Lesson**: 15

#### **BERTScore** (Mentioned)
- **Purpose**: Semantic similarity
- **Method**: Embedding-based comparison
- **Use When**: Meaning over surface form
- **Lesson**: 15

#### **BLEURT** (Mentioned)
- **Purpose**: Learned evaluation metric
- **Method**: Fine-tuned BERT
- **Use When**: High correlation with humans needed
- **Lesson**: 15

---

## 2. Safety & Alignment Metrics

**Source**: Lesson 16

### 2.1 Toxicity Detection

#### **Toxicity Score**
- **Range**: 0.0 - 1.0 (lower is better)
- **Categories**:
  - Hate speech
  - Profanity
  - Threats
  - Sexual content
  - Insults
  - Identity attacks
- **Threshold**: < 0.5 for safe content
- **Lesson**: 16

### 2.2 Truthfulness

#### **Hallucination Rate**
- **Range**: 0.0 - 1.0 (lower is better)
- **Detection Methods**:
  - Fact-checking
  - Citation verification
  - Consistency checking
  - Confidence calibration
- **Target**: < 5% for factual queries
- **Lesson**: 16

### 2.3 Alignment

#### **Refusal Accuracy**
- **Components**: True Positives, False Positives, True Negatives, False Negatives
- **Metrics**: Precision, Recall, F1
- **Target**: > 95% accuracy
- **Use When**: Safety-critical applications
- **Lesson**: 16

#### **Instruction-Following Rate**
- **Range**: 0.0 - 1.0 (higher is better)
- **Checks**: Format, Length, Content, Style, Structure
- **Target**: > 90% compliance
- **Lesson**: 16

### 2.4 Bias & Fairness

**Source**: Lessons 10, 16

#### **Bias Score**
- **Types**: Gender, Racial, Cultural, Socioeconomic
- **Methods**: Counterfactual testing, Stereotype detection
- **Target**: < 20% disparity
- **Lesson**: 10, 16

#### **Demographic Parity**
- **Formula**: max_rate - min_rate
- **Target**: < 20% difference
- **Lesson**: 10

---

## 3. RAG-Specific Metrics

**Source**: Lessons 4, 12, 17

### 3.1 Retrieval Metrics

#### **Recall@K**
- **Formula**: |relevant ∩ top_k| / |relevant|
- **Range**: 0.0 - 1.0 (higher is better)
- **Target**: > 0.8 at K=5
- **Lesson**: 4, 17

#### **Precision@K**
- **Formula**: |relevant ∩ top_k| / K
- **Range**: 0.0 - 1.0 (higher is better)
- **Target**: > 0.6 at K=5
- **Lesson**: 4, 17

#### **Mean Reciprocal Rank (MRR)**
- **Formula**: 1 / rank_of_first_relevant
- **Range**: 0.0 - 1.0 (higher is better)
- **Use When**: First result quality matters
- **Lesson**: 17

#### **NDCG (Normalized Discounted Cumulative Gain)**
- **Purpose**: Graded relevance + ranking
- **Range**: 0.0 - 1.0 (higher is better)
- **Target**: > 0.7 at K=5
- **Lesson**: 17

#### **Hit Rate@K**
- **Formula**: (queries with ≥1 relevant in top K) / total_queries
- **Use When**: Any relevant result is sufficient
- **Lesson**: 17

#### **Coverage**
- **Formula**: |retrievable_docs| / |corpus_size|
- **Purpose**: Retrieval system breadth
- **Lesson**: 17

### 3.2 Grounding & Faithfulness

#### **Faithfulness Score**
- **Range**: 0.0 - 1.0 (higher is better)
- **Formula**: |supported_claims| / |total_claims|
- **Target**: > 0.95
- **Lesson**: 12, 17

#### **Groundedness**
- **Purpose**: No hallucinated information
- **Target**: 100% (no hallucinated entities)
- **Lesson**: 17

#### **Attribution Accuracy**
- **Formula**: |correct_citations| / |total_citations|
- **Range**: 0.0 - 1.0 (higher is better)
- **Lesson**: 17

#### **Citation Precision/Recall**
- **Precision**: Correct citations / Total citations
- **Recall**: Correct citations / Required citations
- **Lesson**: 17

### 3.3 Answer Quality

#### **Answer Correctness**
- **Components**: Exact match, Word overlap, Semantic similarity
- **Target**: > 0.8
- **Lesson**: 17

#### **Answer Relevance**
- **Formula**: |question_keywords ∩ answer| / |question_keywords|
- **Target**: > 0.8
- **Lesson**: 17

#### **Answer Completeness**
- **Formula**: |covered_aspects| / |expected_aspects|
- **Target**: > 0.8
- **Lesson**: 17

#### **Answer Consistency**
- **Purpose**: No self-contradictions
- **Target**: 100% consistency
- **Lesson**: 17

### 3.4 Context Quality

#### **Context Relevance**
- **Purpose**: Retrieved docs match query
- **Target**: > 0.7 average relevance
- **Lesson**: 17

#### **Context Utilization Ratio**
- **Formula**: |utilized_docs| / |retrieved_docs|
- **Purpose**: Measure context usage
- **Lesson**: 17

#### **Context Redundancy**
- **Range**: 0.0 - 1.0 (lower is better)
- **Purpose**: Detect duplicate information
- **Target**: < 0.5
- **Lesson**: 17

#### **Noise Sensitivity**
- **Purpose**: Robustness to irrelevant context
- **Target**: < 0.3 degradation
- **Lesson**: 17

---

## 4. Agent System Metrics

**Source**: Lessons 13, 18

### 4.1 Task Success

#### **Task Success Rate**
- **Formula**: |successful_tasks| / |total_tasks|
- **Target**: > 85%
- **Lesson**: 18

#### **Goal Completion Rate**
- **Formula**: |completed_goals| / |total_goals|
- **Target**: > 90%
- **Lesson**: 18

#### **Subtask Completion Rate**
- **Formula**: |completed_subtasks| / |planned_subtasks|
- **Purpose**: Granular progress tracking
- **Lesson**: 18

#### **Plan Accuracy**
- **Formula**: |correct_steps| / |planned_steps|
- **Target**: > 70%
- **Lesson**: 18

### 4.2 Reasoning & Planning

#### **Reasoning Correctness**
- **Range**: 0.0 - 1.0 (higher is better)
- **Target**: > 0.8
- **Lesson**: 18

#### **Step Accuracy**
- **Formula**: |successful_steps| / |total_steps|
- **Target**: > 0.9
- **Lesson**: 18

#### **Logical Consistency**
- **Purpose**: No contradictions in reasoning
- **Target**: 100% consistent
- **Lesson**: 18

#### **Tool Selection Accuracy**
- **Formula**: |appropriate_tools| / |selected_tools|
- **Target**: > 0.85
- **Lesson**: 18

### 4.3 Tool & Environment Interaction

#### **Tool Invocation Precision**
- **Formula**: TP / (TP + FP)
- **Target**: > 0.8
- **Lesson**: 18

#### **Tool Invocation Recall**
- **Formula**: TP / (TP + FN)
- **Target**: > 0.8
- **Lesson**: 18

#### **API Call Success Rate**
- **Formula**: |successful_calls| / |total_calls|
- **Target**: > 95%
- **Lesson**: 18

#### **Error Recovery Rate**
- **Formula**: |recovered_errors| / |total_errors|
- **Target**: > 70%
- **Lesson**: 18

#### **Environment Constraint Violations**
- **Formula**: |violations| / |total_actions|
- **Target**: 0% violations
- **Lesson**: 18

### 4.4 Autonomy & Efficiency

#### **Steps to Completion**
- **Metric**: Actual steps vs Optimal steps
- **Target**: < 50% overhead
- **Lesson**: 18

#### **Time to Completion**
- **Metric**: Actual duration vs Expected duration
- **Target**: < 2x expected
- **Lesson**: 18

#### **Cost per Task**
- **Components**: Token cost + API cost
- **Purpose**: Resource consumption tracking
- **Lesson**: 18

#### **Redundant Action Rate**
- **Formula**: (consecutive_repeats + duplicates) / total_actions
- **Target**: < 20%
- **Lesson**: 18

### 4.5 Robustness & Reliability

#### **Failure Rate**
- **Formula**: |failed_tasks| / |total_tasks|
- **Target**: < 10%
- **Lesson**: 18

#### **Recovery Time**
- **Metric**: Average time to recover from errors
- **Target**: < 30 seconds
- **Lesson**: 18

#### **Prompt Sensitivity**
- **Purpose**: Stability across prompt variations
- **Target**: > 80% consistency
- **Lesson**: 18

#### **Long-Horizon Stability**
- **Purpose**: Performance over extended tasks
- **Target**: < 20% degradation
- **Lesson**: 18

### 4.6 Human-in-the-Loop

#### **Human Intervention Rate**
- **Formula**: |interventions| / |total_actions|
- **Target**: < 10%
- **Lesson**: 18

#### **Override Frequency**
- **Formula**: |overridden_decisions| / |total_decisions|
- **Target**: < 15%
- **Lesson**: 18

#### **User Satisfaction**
- **Scale**: 1-5
- **Target**: > 4.0/5.0
- **Lesson**: 18

---

## 5. Task-Specific Metrics

**Source**: Lesson 19

### 5.1 QA & Extraction

#### **Exact Match (EM)**
- **Range**: 0 or 1 (binary)
- **Target**: > 80% for extractive QA
- **Use When**: Precise matching required
- **Lesson**: 19

#### **Token-level F1**
- **Formula**: 2 × (Precision × Recall) / (Precision + Recall)
- **Target**: > 85%
- **Standard For**: SQuAD benchmark
- **Lesson**: 19

#### **Semantic Accuracy**
- **Purpose**: Meaning-based evaluation
- **Method**: Embeddings or NLI
- **Target**: > 0.8 similarity
- **Lesson**: 19

### 5.2 Code Generation

#### **Pass@K**
- **Formula**: |problems_with_≥1_passing_solution| / |total_problems|
- **Variants**: Pass@1, Pass@10, Pass@100
- **Target**: Pass@1 > 40% (difficult tasks)
- **Lesson**: 19

#### **Execution Accuracy**
- **Components**:
  - Syntax Correctness
  - Runtime Success
  - Test Pass Rate
  - Output Correctness
- **Target**: > 70% test pass rate
- **Lesson**: 19

### 5.3 Human-Centered

#### **Helpfulness**
- **Range**: 0.0 - 1.0 (higher is better)
- **Factors**: Addresses question, Actionable, Appropriate length
- **Target**: > 0.7
- **Lesson**: 19

#### **Correctness / Factual Accuracy**
- **Purpose**: Truthfulness of information
- **Target**: > 0.9
- **Lesson**: 19

#### **Coherence**
- **Purpose**: Logical flow and consistency
- **Target**: > 0.8
- **Lesson**: 19

#### **Fluency**
- **Purpose**: Natural, grammatical language
- **Target**: > 0.8
- **Lesson**: 19

#### **Relevance**
- **Purpose**: Addresses the question/topic
- **Target**: > 0.8
- **Lesson**: 19

#### **Completeness**
- **Purpose**: Comprehensive coverage
- **Target**: > 0.8
- **Lesson**: 19

---

## 6. Efficiency & Performance Metrics

**Source**: Lesson 20

### 6.1 Latency

#### **Time to First Token (TTFT)**
- **Unit**: milliseconds
- **Target**: < 500ms (interactive)
- **Purpose**: Perceived responsiveness
- **Lesson**: 20

#### **Time Per Output Token (TPOT)**
- **Unit**: milliseconds
- **Purpose**: Streaming speed
- **Lesson**: 20

#### **End-to-End Latency**
- **Unit**: seconds
- **Target**: < 2s (most use cases)
- **Lesson**: 20

#### **Latency Percentiles**
- **Metrics**: P50, P95, P99
- **Purpose**: Tail latency monitoring
- **Lesson**: 20

### 6.2 Throughput

#### **Requests Per Second (RPS)**
- **Unit**: requests/second
- **Target**: > 10 RPS per instance
- **Lesson**: 20

#### **Tokens Per Second**
- **Unit**: tokens/second
- **Purpose**: Processing capacity
- **Lesson**: 20

#### **Concurrent Request Capacity**
- **Metric**: Max stable concurrency
- **Target**: Depends on infrastructure
- **Lesson**: 20

#### **Queue Time**
- **Unit**: seconds
- **Target**: < 1 second (P95)
- **Lesson**: 20

### 6.3 Token Usage & Cost

#### **Input Tokens per Request**
- **Purpose**: Prompt efficiency tracking
- **Lesson**: 20

#### **Output Tokens per Request**
- **Purpose**: Generation length tracking
- **Lesson**: 20

#### **Total Tokens**
- **Formula**: Input tokens + Output tokens
- **Purpose**: Total resource consumption
- **Lesson**: 20

#### **Cost per Request**
- **Formula**: (Input_tokens × Input_price) + (Output_tokens × Output_price)
- **Purpose**: Budget management
- **Lesson**: 20

#### **Cost per User/Session**
- **Purpose**: Per-user cost tracking
- **Lesson**: 20

### 6.4 Context Window

#### **Context Window Utilization**
- **Formula**: Used_tokens / Max_tokens
- **Target**: 60-80% (optimal range)
- **Avoid**: > 90% (truncation risk)
- **Lesson**: 20

#### **Truncation Rate**
- **Formula**: |truncated_requests| / |total_requests|
- **Target**: < 10%
- **Lesson**: 20

#### **Context Efficiency**
- **Formula**: |useful_tokens| / |used_tokens|
- **Purpose**: Wasted context detection
- **Lesson**: 20

---

## 📈 Metrics by Evaluation Stage

### Development Phase
1. **Functionality**: Exact Match, Token F1, Task Success Rate
2. **Quality**: BLEU, ROUGE, Coherence, Helpfulness
3. **Safety**: Toxicity, Hallucination (basic checks)

### Pre-Production Testing
1. **Performance**: Latency (P95), Throughput
2. **Robustness**: Adversarial testing, Prompt sensitivity
3. **Cost**: Token usage, Cost per request
4. **Safety**: Comprehensive toxicity, Bias, Refusal accuracy

### Production Monitoring
1. **Real-time**: Latency percentiles, Error rate, Cost
2. **Batch**: Hallucination rate, Quality scores
3. **User**: Satisfaction, Intervention rate, Feedback

---

## 🎯 Metric Selection Framework

### Step 1: Identify Task Type
- QA: Exact Match, Token F1
- Generation: BLEU, ROUGE, Coherence
- Code: Pass@K, Execution Accuracy
- RAG: Faithfulness, Retrieval metrics
- Agent: Task Success, Tool Accuracy

### Step 2: Add Safety Metrics
- Toxicity (all tasks)
- Hallucination (factual tasks)
- Bias (user-facing tasks)

### Step 3: Add Efficiency Metrics
- Latency (all production)
- Cost (all production)
- Throughput (high-traffic)

### Step 4: Add Human-Centered
- Helpfulness (user-facing)
- Satisfaction (all user-facing)
- Relevance (all tasks)

---

## 📊 Metric Comparison Charts

### Precision vs Recall Focus

| Metric | Type | Use Case |
|--------|------|----------|
| **BLEU** | Precision | Translation |
| **ROUGE** | Recall | Summarization |
| **Exact Match** | Precision | Extractive QA |
| **Token F1** | Balanced | General QA |
| **Pass@K** | Recall | Code (multiple attempts) |

### Speed vs Accuracy Trade-offs

| Metric Category | Speed | Accuracy | Cost |
|----------------|-------|----------|------|
| **N-gram (BLEU/ROUGE)** | ⚡⚡⚡ Fast | ⭐⭐ Basic | 💰 Free |
| **Embedding (BERTScore)** | ⚡⚡ Medium | ⭐⭐⭐⭐ Great | 💰💰 Medium |
| **LLM-as-Judge** | ⚡ Slow | ⭐⭐⭐⭐⭐ Best | 💰💰💰 High |
| **Human Eval** | 🐌 Very Slow | ⭐⭐⭐⭐⭐ Best | 💰💰💰💰 Very High |

---

## 🛠️ Implementation Resources

### Python Libraries

```python
# Text metrics
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
from bert_score import score as bert_score

# Safety
from detoxify import Detoxify
from perspective import PerspectiveAPI

# RAG
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

# Custom (this repo)
from custom.evals import Evaluator
```

### Recommended Tools

**Text Quality**:
- NLTK, spaCy (n-gram metrics)
- Hugging Face Transformers (BERTScore, BLEURT)

**Safety**:
- Detoxify, Perspective API
- Custom LLM-as-judge

**RAG**:
- RAGAS framework
- LangChain evaluation module
- Custom metrics (Lesson 17)

**Production**:
- Prometheus (metrics collection)
- Grafana (dashboards)
- LangSmith, Langfuse (LLM observability)

---

## 📚 Cross-Reference

| Metric | Primary Lesson | Also In | Related Lessons |
|--------|---------------|---------|-----------------|
| **BLEU** | 15 | - | 2 (basics) |
| **Exact Match** | 19 | 2 | - |
| **Faithfulness** | 17 | 12 | 4 (RAG basics) |
| **Toxicity** | 16 | - | 10 (bias) |
| **Task Success** | 18 | 13 | - |
| **Latency** | 20 | 6 | - |

---

## 🎓 Learning Path

### Beginner (Weeks 1-2)
- Simple metrics: Exact Match, Token F1 (Lesson 2, 19)
- Basic RAG: Precision/Recall (Lesson 4)
- Introduction to safety (Lesson 10)

### Intermediate (Weeks 3-4)
- Advanced text: BLEU, ROUGE (Lesson 15)
- Complete RAG: Faithfulness, Grounding (Lesson 17)
- Safety depth: Toxicity, Hallucination (Lesson 16)

### Advanced (Weeks 5-6)
- Agent systems (Lesson 18)
- Human-centered metrics (Lesson 19)
- Production efficiency (Lesson 20)

### Expert (Week 7+)
- Statistical rigor (Lesson 8)
- Adversarial testing (Lesson 9)
- Benchmark creation (Lesson 11)
- Prompt optimization (Lesson 14)

---

## 📞 Support & Updates

**Questions?**
- Review specific lesson code
- Check `/examples` directory
- Read lesson KEY TAKEAWAYS sections

**Updates**:
- This reference covers all metrics as of Lesson 20
- New metrics will be added in future lessons
- Check lesson files for latest implementations

---

**Last Updated**: 2026-01-18
**Version**: 1.0
**Total Metrics**: 100+
**Total Lessons**: 20
**Total Lines**: ~15,000+ lines of code

**You now have access to the most comprehensive LLM evaluation metric catalog! 🎓**
