# Learn LLM Evaluation - From Basics to Advanced

**A comprehensive, hands-on learning path for LLM evaluation.**

Start from zero knowledge and progressively build expertise in evaluating Large Language Models, RAG systems, and production applications.

---

## 📚 What You'll Learn

By completing this learning path, you will:

✅ **Understand** what LLM evaluation is and why it matters
✅ **Implement** various evaluation metrics (exact match, similarity, LLM-as-judge)
✅ **Evaluate** RAG systems (retrieval + generation)
✅ **Build** custom metrics for your specific needs
✅ **Deploy** evaluation in production systems
✅ **Use** the cust-evals framework effectively
✅ **Compare** and choose between evaluation frameworks
✅ **Master** 100+ specialized metrics (text quality, safety, RAG, agents, efficiency)
✅ **Apply** statistical rigor and production best practices
✅ **Optimize** for performance, cost, and quality simultaneously

---

## 🎯 Who Is This For?

- **Beginners**: Never evaluated an LLM before? Start here!
- **Developers**: Building LLM applications and need quality assurance
- **ML Engineers**: Want to measure and improve model performance
- **Data Scientists**: Need systematic evaluation approaches
- **Product Teams**: Want to track LLM quality over time

**Prerequisites**:
- Basic Python knowledge
- Familiarity with LLMs (used ChatGPT/Claude)
- No evaluation experience required!

---

## 📖 Learning Path

### Complete the lessons in order for the best learning experience:

### Foundation Track (Lessons 1-7)

| Lesson | Topic | Time | Difficulty |
|--------|-------|------|------------|
| **[01](01_basics_what_is_evaluation.py)** | What is LLM Evaluation? | 15 min | ⭐ Beginner |
| **[02](02_simple_metrics.py)** | Simple Evaluation Metrics | 20 min | ⭐ Beginner |
| **[03](03_llm_as_judge.py)** | LLM-as-Judge Evaluation | 25 min | ⭐⭐ Intermediate |
| **[04](04_rag_evaluation.py)** | RAG System Evaluation | 30 min | ⭐⭐ Intermediate |
| **[05](05_custom_metrics.py)** | Building Custom Metrics | 30 min | ⭐⭐ Intermediate |
| **[06](06_production_patterns.py)** | Production Evaluation | 25 min | ⭐⭐⭐ Advanced |
| **[07](07_using_cust_evals.py)** | Using Cust-Evals Framework | 20 min | ⭐⭐ Intermediate |

**Foundation Track Time**: ~2.5 hours

### Advanced Track (Lessons 8-14)

| Lesson | Topic | Time | Difficulty |
|--------|-------|------|------------|
| **[08](08_statistical_evaluation.py)** | Statistical Evaluation & Significance | 50 min | ⭐⭐⭐ Advanced |
| **[09](09_adversarial_testing.py)** | Adversarial Testing & Robustness | 45 min | ⭐⭐⭐ Advanced |
| **[10](10_bias_fairness_evaluation.py)** | Bias and Fairness Evaluation | 45 min | ⭐⭐⭐ Advanced |
| **[11](11_benchmark_creation.py)** | Benchmark Creation & Dataset Curation | 50 min | ⭐⭐⭐ Advanced |
| **[12](12_advanced_rag_patterns.py)** | Advanced RAG Patterns | 50 min | ⭐⭐⭐ Advanced |
| **[13](13_multi_agent_evaluation.py)** | Multi-Agent System Evaluation | 50 min | ⭐⭐⭐ Advanced |
| **[14](14_prompt_optimization.py)** | Prompt Optimization via Evaluation | 50 min | ⭐⭐⭐ Advanced |

**Advanced Track Time**: ~6 hours

### Expert Metrics Track (Lessons 15-20)

| Lesson | Topic | Time | Difficulty |
|--------|-------|------|------------|
| **[15](15_advanced_text_metrics.py)** | Advanced Text Quality & Similarity | 60 min | ⭐⭐⭐ Advanced |
| **[16](16_safety_alignment_evaluation.py)** | Safety, Alignment & Toxicity | 55 min | ⭐⭐⭐ Advanced |
| **[17](17_rag_metrics_deep_dive.py)** | RAG Metrics Deep Dive | 65 min | ⭐⭐⭐ Advanced |
| **[18](18_agent_systems_evaluation.py)** | Agent Systems Evaluation | 70 min | ⭐⭐⭐ Advanced |
| **[19](19_task_specific_human_metrics.py)** | Task-Specific & Human-Centered Metrics | 60 min | ⭐⭐⭐ Advanced |
| **[20](20_efficiency_performance_metrics.py)** | Efficiency & Performance Metrics | 55 min | ⭐⭐⭐ Advanced |

**Expert Metrics Track Time**: ~6 hours

**Total Time (All Lessons)**: ~14.5 hours

---

## 🚀 Getting Started

### Option 1: Interactive Learning (Recommended)

Run each lesson as a Python script for an interactive learning experience:

```bash
# Start from the beginning
cd docs/learn
python 01_basics_what_is_evaluation.py

# Follow prompts and complete each lesson
python 02_simple_metrics.py
python 03_llm_as_judge.py
# ... and so on
```

Each lesson:
- Explains concepts clearly
- Shows working code examples
- Includes demonstrations
- Provides practice exercises
- Builds on previous lessons

### Option 2: Read-Through

If you prefer reading first:

1. Open each `.py` file in your editor
2. Read through the code and comments
3. Run sections individually to experiment
4. Modify examples to test your understanding

---

## 📝 Detailed Lesson Overview

### Lesson 1: What is LLM Evaluation? (Beginner)
**File**: `01_basics_what_is_evaluation.py`

**What You'll Learn**:
- Why evaluate LLMs?
- What makes a response "good"?
- Your first evaluation function
- The evaluation process
- Key concepts and terminology

**Key Takeaways**:
- Evaluation = systematically measuring LLM quality
- Start simple (even string matching is valuable!)
- Follow a process: Prepare → Run → Evaluate → Analyze → Improve

**Perfect for**: Absolute beginners, anyone new to LLM evaluation

---

### Lesson 2: Simple Evaluation Metrics (Beginner)
**File**: `02_simple_metrics.py`

**What You'll Learn**:
- Exact match metrics
- Contains/substring checking
- Word overlap and similarity
- Length and format validation
- Keyword presence checking
- Combining multiple metrics

**Key Takeaways**:
- Different metrics for different use cases
- Combine metrics for holistic evaluation
- Trade-offs between strictness and flexibility

**Hands-On**: Implement 5+ different metrics and see them in action

---

### Lesson 3: LLM-as-Judge Evaluation (Intermediate)
**File**: `03_llm_as_judge.py`

**What You'll Learn**:
- Using LLMs to evaluate LLMs
- Writing effective evaluation prompts
- Quality judgment patterns
- Comparative evaluation
- Hallucination detection
- Best practices and pitfalls

**Key Takeaways**:
- LLM-as-judge handles nuance and complexity
- Good prompts = good evaluations
- Use for subjective criteria
- Always request reasoning

**Requirements**: Understanding of LLM APIs (optional - examples use simulations)

---

### Lesson 4: RAG System Evaluation (Intermediate)
**File**: `04_rag_evaluation.py`

**What You'll Learn**:
- What is RAG and why evaluate it differently?
- Retrieval metrics (precision, recall, F1)
- Generation metrics (faithfulness, relevance)
- End-to-end RAG evaluation
- Component-level analysis

**Key Takeaways**:
- RAG = Retrieval + Generation (evaluate both!)
- Retrieval quality affects generation quality
- Track which component is failing
- Optimize the weak component

**Perfect for**: Anyone building RAG applications

---

### Lesson 5: Building Custom Metrics (Intermediate)
**File**: `05_custom_metrics.py`

**What You'll Learn**:
- Designing custom evaluators
- Domain-specific metrics (medical, legal, etc.)
- Safety and compliance checking
- Performance metrics (latency, cost)
- Combining custom metrics
- Testing and validation

**Key Takeaways**:
- Custom metrics for unique requirements
- Follow design principles (clear, measurable, actionable)
- Test thoroughly before deploying
- Document your metrics well

**Hands-On**: Build 4+ custom evaluators from scratch

---

### Lesson 6: Production Evaluation Patterns (Advanced)
**File**: `06_production_patterns.py`

**What You'll Learn**:
- Batch vs real-time evaluation
- Monitoring and alerting
- A/B testing for model comparison
- Human-in-the-loop patterns
- Production best practices

**Key Takeaways**:
- Different strategies for dev vs production
- Automate everything
- Monitor continuously, alert on anomalies
- Use A/B testing for changes

**Perfect for**: Deploying evaluation in production systems

---

### Lesson 7: Using the Cust-Evals Framework (Intermediate)
**File**: `07_using_cust_evals.py`

**What You'll Learn**:
- Using the custom evaluation framework
- Pre-built evaluators
- Creating custom evaluators
- Tracing and observability
- Metrics collection
- Integration patterns
- Configuration and best practices

**Key Takeaways**:
- Leverage pre-built components
- Extend for custom needs
- Enable tracing for debugging
- Integrate with your stack

**Perfect for**: Using this repository's evaluation framework

---

### Lesson 8: Statistical Evaluation & Significance (Advanced)
**File**: `08_statistical_evaluation.py`

**What You'll Learn**:
- Statistical hypothesis testing (t-tests, p-values)
- Confidence intervals for evaluation scores
- Sample size determination
- Bootstrap methods for robust estimation
- Variance analysis
- Comparing model versions rigorously

**Key Takeaways**:
- Use statistical tests to validate improvements
- Calculate confidence intervals to quantify uncertainty
- Determine adequate sample sizes before testing
- Apply bootstrap methods when assumptions don't hold
- Make data-driven decisions with statistical rigor

**Hands-On**: Implement t-tests, confidence intervals, bootstrap sampling

---

### Lesson 9: Adversarial Testing & Robustness (Advanced)
**File**: `09_adversarial_testing.py`

**What You'll Learn**:
- Input perturbations (typos, case changes, whitespace)
- Edge case generation and testing
- Adversarial question crafting
- Robustness scoring frameworks
- Failure mode analysis
- Security testing for LLMs

**Key Takeaways**:
- Test beyond happy paths
- Systematically generate edge cases
- Measure system robustness quantitatively
- Identify failure modes before production
- Build resilient systems through adversarial testing

**Hands-On**: Create perturbation functions, build robustness test suites

---

### Lesson 10: Bias and Fairness Evaluation (Advanced)
**File**: `10_bias_fairness_evaluation.py`

**What You'll Learn**:
- Gender, racial, and cultural bias detection
- Counterfactual testing methodology
- Fairness metrics (demographic parity, equal opportunity)
- Stereotype detection in outputs
- Bias mitigation strategies
- Responsible AI evaluation

**Key Takeaways**:
- Bias evaluation is multi-dimensional
- Use counterfactual testing to reveal bias
- Multiple fairness metrics may conflict
- Systematic detection before deployment
- Document bias findings and mitigation efforts

**Hands-On**: Implement bias detectors, run counterfactual tests, measure fairness

---

### Lesson 11: Benchmark Creation & Dataset Curation (Advanced)
**File**: `11_benchmark_creation.py`

**What You'll Learn**:
- Benchmark design principles
- Dataset diversity and balance requirements
- Quality assurance checks for datasets
- Test set construction strategies
- Versioning and maintenance practices
- Professional documentation standards

**Key Takeaways**:
- Good benchmarks are representative, diverse, and balanced
- Quality checks prevent data issues
- Stratified sampling ensures coverage
- Version benchmarks like code
- Documentation is critical for benchmark adoption

**Hands-On**: Design custom benchmarks, implement quality checks, version datasets

---

### Lesson 12: Advanced RAG Patterns (Advanced)
**File**: `12_advanced_rag_patterns.py`

**What You'll Learn**:
- Multi-hop reasoning evaluation
- Iterative retrieval assessment
- Hybrid search comparison (semantic + keyword)
- Query decomposition testing
- Re-ranking effectiveness measurement
- Complex RAG architecture evaluation

**Key Takeaways**:
- Advanced RAG requires specialized evaluation
- Multi-hop reasoning needs step-by-step validation
- Hybrid search should outperform individual methods
- Measure improvement at each stage
- Always compare to simpler baselines

**Hands-On**: Evaluate multi-hop systems, test hybrid retrieval, optimize re-ranking

---

### Lesson 13: Multi-Agent System Evaluation (Advanced)
**File**: `13_multi_agent_evaluation.py`

**What You'll Learn**:
- Agent communication quality metrics
- Task coordination evaluation
- Consensus building assessment
- System-level performance measurement
- Emergent behavior detection
- Inter-agent dependency analysis

**Key Takeaways**:
- Evaluate at multiple levels (agent, interaction, system)
- Communication quality affects overall performance
- Coordination overhead must justify benefits
- System-level metrics capture emergent properties
- Compare to single-agent baselines

**Hands-On**: Measure communication quality, evaluate coordination, assess consensus

---

### Lesson 14: Prompt Optimization via Evaluation (Advanced)
**File**: `14_prompt_optimization.py`

**What You'll Learn**:
- Systematic prompt testing frameworks
- A/B testing methodology for prompts
- Iterative refinement strategies
- Few-shot example selection optimization
- Prompt version management
- Data-driven prompt engineering

**Key Takeaways**:
- Replace guessing with systematic testing
- Use A/B tests with statistical validation
- Version prompts like code
- Optimize few-shot examples empirically
- Continuous improvement through evaluation
- Let data guide prompt refinements

**Hands-On**: Build prompt testing framework, run A/B tests, optimize iteratively

---

### Lesson 15: Advanced Text Quality & Similarity Metrics (Advanced)
**File**: `15_advanced_text_metrics.py`

**What You'll Learn**:
- BLEU Score (n-gram precision with brevity penalty)
- ROUGE variants (ROUGE-1, ROUGE-2, ROUGE-L)
- METEOR Score (synonym-aware matching)
- Perplexity for language model quality
- BERTScore and embedding-based metrics
- BLEURT and learned evaluation metrics
- When to use each metric

**Key Takeaways**:
- N-gram metrics (BLEU, ROUGE) for reference-based evaluation
- METEOR handles synonyms better than simple n-gram overlap
- Perplexity measures fluency and language model quality
- Embedding-based metrics capture semantic similarity
- Different metrics optimized for different tasks (translation vs summarization)
- Combine multiple metrics for comprehensive evaluation

**Hands-On**: Implement BLEU, ROUGE, METEOR, Perplexity with working demos

**Perfect for**: NLP tasks, summarization, translation, text generation quality

---

### Lesson 16: Safety, Alignment & Toxicity Evaluation (Advanced)
**File**: `16_safety_alignment_evaluation.py`

**What You'll Learn**:
- Multi-dimensional toxicity detection
- Hallucination detection and fact-checking
- Refusal accuracy (true/false positives/negatives)
- Instruction-following rate measurement
- Bias detection in outputs
- Safety metric aggregation
- Production safety monitoring

**Key Takeaways**:
- Toxicity is multi-dimensional (hate, threats, profanity, identity attacks)
- Hallucination detection requires fact verification and context checking
- Refusal systems need balanced accuracy (not over/under-refusing)
- Instruction-following evaluates format, length, content, style compliance
- Safety metrics are critical for production deployment
- Always combine automated checks with human review

**Hands-On**: Build toxicity detector, hallucination checker, refusal evaluator

**Perfect for**: Safety-critical applications, content moderation, responsible AI

---

### Lesson 17: RAG Metrics Deep Dive (Advanced)
**File**: `17_rag_metrics_deep_dive.py`

**What You'll Learn**:
- Complete retrieval metrics (Recall@K, Precision@K, MRR, NDCG, Hit Rate, Coverage)
- Grounding metrics (Faithfulness, Groundedness, Attribution Accuracy)
- Answer quality metrics (Correctness, Relevance, Completeness, Consistency)
- Context quality metrics (Relevance, Utilization, Redundancy, Noise Sensitivity)
- End-to-end RAG evaluation framework
- Component-level debugging and optimization

**Key Takeaways**:
- RAG evaluation requires metrics at multiple levels (retrieval, grounding, generation, context)
- NDCG considers ranking quality, not just binary relevance
- Faithfulness ensures answers stay grounded in retrieved context
- Context utilization measures efficiency of retrieval
- Always evaluate retrieval and generation separately for debugging
- Noise sensitivity tests robustness to irrelevant context

**Hands-On**: Implement complete RAG evaluation suite with all 15+ metrics

**Perfect for**: RAG systems, Q&A applications, knowledge bases, document search

---

### Lesson 18: Agent Systems Comprehensive Evaluation (Advanced)
**File**: `18_agent_systems_evaluation.py`

**What You'll Learn**:
- Task success metrics (Success Rate, Goal Completion, Plan Accuracy)
- Reasoning evaluation (Correctness, Step Accuracy, Logical Consistency)
- Tool interaction metrics (Selection Accuracy, API Success, Error Recovery)
- Efficiency metrics (Steps to Completion, Time, Cost, Redundancy)
- Robustness metrics (Failure Rate, Recovery Time, Prompt Sensitivity)
- Human-in-loop metrics (Intervention Rate, Override Frequency, Satisfaction)
- Multi-dimensional agent evaluation framework

**Key Takeaways**:
- Agent evaluation requires task, reasoning, tool, efficiency, and robustness metrics
- Track subtask completion for complex multi-step goals
- Tool selection accuracy is critical for autonomous agents
- Error recovery capability separates good from great agents
- Long-horizon stability tests agent performance over extended tasks
- Human intervention rate indicates autonomy level

**Hands-On**: Build complete agent evaluation framework with 20+ metrics

**Perfect for**: Autonomous agents, tool-using LLMs, multi-step task systems

---

### Lesson 19: Task-Specific & Human-Centered Metrics (Advanced)
**File**: `19_task_specific_human_metrics.py`

**What You'll Learn**:
- Exact Match (EM) for precise answers
- Token-level F1 Score for partial credit
- Pass@K for code generation (multiple attempts)
- Execution Accuracy with test cases
- Semantic Accuracy beyond exact matching
- Human-centered metrics (Helpfulness, Correctness, Coherence, Fluency, Relevance, Completeness)
- Combining task-specific with human judgment

**Key Takeaways**:
- Task-specific metrics provide precise measurement for specialized domains
- Token F1 gives partial credit for partially correct answers
- Pass@K allows multiple attempts (standard for code generation)
- Execution testing is ground truth for code correctness
- Human-centered metrics capture subjective quality dimensions
- Combine automated metrics with human evaluation for best results

**Hands-On**: Implement EM, Token F1, Pass@K, Execution, Human metrics

**Perfect for**: Q&A systems, code generation, task-specific applications

---

### Lesson 20: Efficiency & Performance Metrics (Advanced)
**File**: `20_efficiency_performance_metrics.py`

**What You'll Learn**:
- Latency metrics (TTFT, TPOT, End-to-End, Percentiles)
- Throughput metrics (RPS, Tokens/sec, Concurrent Capacity)
- Token usage and cost tracking
- Context window utilization and efficiency
- Performance profiling and bottleneck identification
- Cost optimization strategies
- Production performance monitoring

**Key Takeaways**:
- TTFT (Time to First Token) critical for user experience
- TPOT (Time Per Output Token) measures generation efficiency
- Track P95/P99 latency, not just averages
- Cost per request = (input_tokens × input_price + output_tokens × output_price)
- Context utilization should be 50-80% for efficiency
- Monitor throughput to prevent bottlenecks
- Optimize for cost-quality tradeoff, not just quality

**Hands-On**: Implement latency tracking, cost calculator, throughput monitor

**Perfect for**: Production systems, cost optimization, performance tuning

---

## 📘 Advanced Topics & Metrics Reference

### Advanced Topics Guide

For a comprehensive synthesis of all advanced lessons (8-14), including:
- Integration patterns
- Learning paths by goal
- Evaluation metrics matrix
- Common pitfalls and solutions
- Production deployment strategies

**See**: [ADVANCED_TOPICS.md](ADVANCED_TOPICS.md)

### Comprehensive Metrics Reference

For a complete catalog of all 100+ evaluation metrics across lessons 15-20:
- Quick metric selector by use case
- Complete metrics catalog organized by category
- Implementation formulas and code references
- Target thresholds and best practices
- Metrics comparison charts
- Cross-references to lesson implementations

**See**: [METRICS_REFERENCE.md](METRICS_REFERENCE.md)

This reference covers:
- **Text Quality**: BLEU, ROUGE, METEOR, Perplexity, BERTScore, BLEURT
- **Safety & Alignment**: Toxicity, Hallucination, Refusal, Instruction-Following, Bias
- **RAG Systems**: 15+ retrieval, grounding, answer, and context metrics
- **Agent Systems**: 20+ task, reasoning, tool, efficiency, and robustness metrics
- **Task-Specific**: Exact Match, Token F1, Pass@K, Execution, Semantic Accuracy
- **Human-Centered**: Helpfulness, Correctness, Coherence, Fluency, Relevance, Completeness
- **Efficiency**: Latency (TTFT, TPOT), Throughput, Token Usage, Cost, Context Utilization

---

## 🛠️ Installation & Setup

### Basic Setup (Lessons 1-2)

No installation needed! Lessons 1-2 use only Python standard library.

```bash
python 01_basics_what_is_evaluation.py
python 02_simple_metrics.py
```

### Advanced Lessons Setup (Lessons 3-7)

For lessons using LLM APIs or the framework:

```bash
# Install the custom evaluation framework
cd ../..  # Go to repository root
pip install -e .

# Or install dependencies individually
pip install openai anthropic  # For LLM-as-judge lessons
```

### Optional: API Keys

For lessons that use actual LLM APIs (you can run without them using simulations):

```bash
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
```

---

## 📊 Learning Paths by Role

### For Beginners (Never Evaluated Before)
**Foundation Track**:
1. Lesson 1: Basics → Understand the fundamentals
2. Lesson 2: Simple Metrics → Hands-on practice
3. Lesson 3: LLM-as-Judge → Level up your skills
4. Lesson 7: Use Framework → Apply to real projects

**Time**: ~2 hours | **Outcome**: Can run basic evaluations

**Advanced Track** (After foundation):
5. Lesson 8: Statistical Evaluation → Data-driven decisions
6. Lesson 14: Prompt Optimization → Systematic improvement

**Time**: ~3.5 hours | **Outcome**: Production-ready skills

**Expert Metrics** (Optional specialization):
7. Lesson 19: Task-Specific Metrics → Domain expertise
8. Lesson 20: Efficiency Metrics → Cost optimization

**Total Time**: ~5.5 hours | **Outcome**: Complete evaluation skillset

---

### For Developers (Building LLM Apps)
**Foundation Track**:
1. Lesson 1: Basics → Quick foundation
2. Lesson 2: Simple Metrics → Practical metrics
3. Lesson 4: RAG Evaluation → If building RAG
4. Lesson 6: Production → Deploy evaluation
5. Lesson 7: Use Framework → Integrate framework

**Time**: ~2.5 hours | **Outcome**: Integrated evaluation

**Advanced Track** (After foundation):
6. Lesson 8: Statistical Evaluation → Validate improvements
7. Lesson 9: Adversarial Testing → Ensure robustness
8. Lesson 12: Advanced RAG → Sophisticated patterns
9. Lesson 14: Prompt Optimization → Continuous improvement

**Time**: ~5 hours | **Outcome**: Expert-level implementation

**Expert Metrics** (For production excellence):
10. Lesson 16: Safety Evaluation → Responsible deployment
11. Lesson 17: RAG Metrics → Complete RAG mastery
12. Lesson 20: Efficiency Metrics → Cost & performance

**Total Time**: ~8.5 hours | **Outcome**: Production excellence with metrics mastery

---

### For ML Engineers (Optimizing Models)
**Foundation Track**:
1. Lessons 1-2: Foundation → Quick review
2. Lesson 3: LLM-as-Judge → Sophisticated evaluation
3. Lesson 5: Custom Metrics → Domain-specific
4. Lesson 6: Production → A/B testing, monitoring
5. Lesson 7: Framework → Advanced tooling

**Time**: ~2.5 hours | **Outcome**: Framework mastery

**Advanced Track** (After foundation):
6. Lesson 8: Statistical Evaluation → Rigorous testing
7. Lesson 9: Adversarial Testing → Find edge cases
8. Lesson 11: Benchmark Creation → Professional benchmarks
9. Lesson 14: Prompt Optimization → Systematic tuning

**Time**: ~5 hours | **Outcome**: Advanced evaluation skills

**Expert Metrics** (For complete mastery):
10. Lesson 15: Text Quality Metrics → BLEU, ROUGE, METEOR
11. Lesson 16: Safety Metrics → Comprehensive safety
12. Lesson 19: Task-Specific Metrics → Domain precision
13. Lesson 20: Efficiency Metrics → Performance tuning
14. All expert lessons (15-20) → Complete metrics mastery

**Total Time**: ~11.5 hours | **Outcome**: World-class evaluation expert

---

### For Product Teams (Quality Tracking)
**Foundation Track**:
1. Lesson 1: Basics → Understand evaluation
2. Lesson 2: Simple Metrics → Practical measures
3. Lesson 6: Production → Monitoring dashboards
4. Lesson 7: Framework → Implement tracking

**Time**: ~1.5 hours | **Outcome**: Quality monitoring

**Advanced Track** (After foundation):
5. Lesson 8: Statistical Evaluation → Data-driven decisions
6. Lesson 10: Bias Evaluation → Responsible AI
7. Lesson 11: Benchmark Creation → Quality standards

**Total Time**: ~4 hours | **Outcome**: Comprehensive quality systems

---

### For AI Safety & Ethics Engineers
**Foundation Track**:
1. Lessons 1-3: Basics → Foundation
2. Lesson 5: Custom Metrics → Safety metrics

**Time**: ~1.5 hours | **Outcome**: Basic safety evaluation

**Advanced Track** (Focus):
3. Lesson 10: Bias & Fairness → Core expertise
4. Lesson 9: Adversarial Testing → Safety testing
5. Lesson 8: Statistical Evaluation → Rigorous measurement
6. Lesson 11: Benchmark Creation → Fairness benchmarks

**Time**: ~3.5 hours | **Outcome**: Advanced safety skills

**Expert Metrics** (Critical for safety):
7. Lesson 16: Safety & Toxicity Evaluation → Complete safety suite
8. Lesson 15: Text Quality Metrics → Output quality assurance
9. Lesson 19: Human-Centered Metrics → User impact assessment

**Total Time**: ~7 hours | **Outcome**: Comprehensive AI safety expertise

---

### For RAG System Specialists
**Foundation Track**:
1. Lessons 1-4: Basics → RAG foundation
2. Lesson 7: Framework → RAG tools

**Time**: ~2 hours | **Outcome**: Basic RAG evaluation

**Advanced Track** (Focus):
3. Lesson 12: Advanced RAG Patterns → Expertise
4. Lesson 8: Statistical Evaluation → Validate improvements
5. Lesson 11: Benchmark Creation → RAG benchmarks
6. Lesson 9: Adversarial Testing → Edge cases

**Time**: ~3.5 hours | **Outcome**: Advanced RAG evaluation

**Expert Metrics** (Essential for RAG mastery):
7. Lesson 17: RAG Metrics Deep Dive → Complete 15+ RAG metrics
8. Lesson 15: Text Quality Metrics → Generation quality
9. Lesson 20: Efficiency Metrics → RAG performance optimization

**Total Time**: ~7 hours | **Outcome**: World-class RAG evaluation expert

---

### For Multi-Agent System Engineers
**Foundation Track**:
1. Lessons 1-7: Complete foundation

**Time**: ~2.5 hours | **Outcome**: Basic evaluation skills

**Advanced Track** (Focus):
2. Lesson 13: Multi-Agent Evaluation → Core expertise
3. Lesson 8: Statistical Evaluation → System metrics
4. Lesson 11: Benchmark Creation → Agent scenarios
5. Lesson 14: Prompt Optimization → Agent prompts

**Time**: ~3.5 hours | **Outcome**: Advanced multi-agent skills

**Expert Metrics** (For agent systems mastery):
6. Lesson 18: Agent Systems Evaluation → Complete 20+ agent metrics
7. Lesson 19: Task-Specific Metrics → Task success measurement
8. Lesson 20: Efficiency Metrics → Agent performance optimization

**Total Time**: ~7 hours | **Outcome**: Agent evaluation expert

---

## 🎯 After Completing the Lessons

### After Foundation Track (Lessons 1-7):

You can now:
✅ Understand evaluation fundamentals
✅ Implement basic metrics
✅ Use LLM-as-judge patterns
✅ Evaluate RAG systems
✅ Build custom metrics
✅ Deploy production evaluation
✅ Use evaluation frameworks

**Next**: Choose advanced lessons based on your role/goals

---

### After Advanced Track (Lessons 8-14):

You are now an **LLM Evaluation Expert** with:
✅ Statistical rigor in analysis
✅ Adversarial testing capabilities
✅ Bias detection expertise
✅ Professional benchmark creation skills
✅ Advanced RAG evaluation mastery
✅ Multi-agent system evaluation knowledge
✅ Systematic prompt optimization abilities

**Achievement Unlocked**: 🎓 **Evaluation Expert**

---

### After Expert Metrics Track (Lessons 15-20):

You are now a **World-Class Metrics Specialist** with mastery of:
✅ 100+ specialized evaluation metrics across all domains
✅ Advanced text quality metrics (BLEU, ROUGE, METEOR, Perplexity)
✅ Comprehensive safety evaluation (Toxicity, Hallucination, Refusal, Instruction-Following)
✅ Complete RAG evaluation suite (15+ retrieval, grounding, answer, context metrics)
✅ Agent systems evaluation framework (20+ task, reasoning, tool, robustness metrics)
✅ Task-specific metrics (Exact Match, Token F1, Pass@K, Execution Accuracy)
✅ Human-centered evaluation (Helpfulness, Correctness, Coherence, Fluency, Relevance)
✅ Efficiency & performance optimization (Latency, Throughput, Cost, Context Utilization)

**Achievement Unlocked**: 🏆 **Metrics Master** - World-Class Evaluation Expertise

---

### Next Steps:

1. **Practice**: Apply lessons to your own LLM projects
2. **Deep Dive**: Read [ADVANCED_TOPICS.md](ADVANCED_TOPICS.md) for integration patterns
3. **Metrics Reference**: Read [METRICS_REFERENCE.md](METRICS_REFERENCE.md) for complete metrics catalog
4. **Compare Frameworks**: Check out `/docs/compare_eval_frameworks/`
5. **Read Examples**: Explore `/examples/` for real implementations
6. **Use cust-evals**: Integrate the framework into your workflow
7. **Build**: Create domain-specific benchmarks (Lesson 11)
8. **Optimize**: Apply systematic prompt optimization (Lesson 14)
9. **Master Metrics**: Implement specialized metrics for your domain (Lessons 15-20)
10. **Contribute**: Share your custom evaluators and benchmarks!

### Additional Resources:

- **Framework Comparison**: `../compare_eval_frameworks/` - Compare 14 evaluation frameworks
- **Examples**: `../../examples/` - Real-world usage examples
- **Source Code**: `../../src/custom/evals/` - Framework implementation
- **Tests**: `../../tests/` - Testing patterns and examples

---

## 💡 Tips for Success

### Do's ✅
- Complete lessons in order (they build on each other)
- Run the code, don't just read it
- Experiment and modify examples
- Take notes on key concepts
- Apply to your own projects
- Review lessons when needed

### Don'ts ❌
- Don't skip lessons (you'll miss important concepts)
- Don't just copy-paste code (understand it!)
- Don't rush (take time to experiment)
- Don't skip practice exercises
- Don't hesitate to revisit earlier lessons

---

## 📚 Quick Reference

### Common Metrics Cheat Sheet

| Metric | Use When | Pros | Cons |
|--------|----------|------|------|
| **Exact Match** | Need precise answers | Simple, clear | Too strict |
| **Contains** | Key info extraction | Flexible | Misses errors |
| **Word Overlap** | Paraphrasing OK | Balanced | Ignores order |
| **LLM-as-Judge** | Complex/subjective | Nuanced | Costs money |
| **Faithfulness** | RAG systems | Prevents hallucination | Needs context |
| **Relevance** | Q&A systems | Ensures usefulness | Subjective |
| **BLEU/ROUGE** | Translation/summarization | Reference-based, standard | Needs references |
| **Pass@K** | Code generation | Allows multiple attempts | Needs test cases |
| **Toxicity Score** | Safety evaluation | Multi-dimensional | False positives |
| **TTFT/TPOT** | Latency optimization | User experience focused | Needs profiling |

### When to Use Which Evaluation

| Situation | Recommended Approach |
|-----------|---------------------|
| **Math/Code** | Exact match or execution testing (Lesson 19) |
| **Q&A** | Token F1 + LLM-as-judge + Helpfulness (Lesson 19) |
| **RAG** | Recall@K + NDCG + Faithfulness + Answer Correctness (Lesson 17) |
| **Summarization** | ROUGE-L + METEOR + LLM-as-judge (Lesson 15) |
| **Translation** | BLEU + METEOR + human evaluation (Lesson 15) |
| **Safety** | Toxicity + Hallucination + Refusal Accuracy (Lesson 16) |
| **Agents** | Task Success + Tool Accuracy + Error Recovery (Lesson 18) |
| **Production** | Latency (TTFT/TPOT) + Cost + Throughput + Quality (Lesson 20) |

### Expert Metrics Quick Selector

| Domain | Key Metrics | Lesson |
|--------|-------------|--------|
| **Text Quality** | BLEU, ROUGE, METEOR, Perplexity | [15](15_advanced_text_metrics.py) |
| **Safety** | Toxicity, Hallucination, Refusal, Instruction-Following | [16](16_safety_alignment_evaluation.py) |
| **RAG** | Recall@K, NDCG, Faithfulness, Answer Correctness | [17](17_rag_metrics_deep_dive.py) |
| **Agents** | Task Success, Tool Accuracy, Error Recovery | [18](18_agent_systems_evaluation.py) |
| **Task-Specific** | EM, Token F1, Pass@K, Execution Accuracy | [19](19_task_specific_human_metrics.py) |
| **Efficiency** | TTFT, TPOT, Throughput, Cost, Context Utilization | [20](20_efficiency_performance_metrics.py) |

---

## 🤝 Getting Help

**Questions or Issues?**
- Check the lesson comments (heavily documented!)
- Review earlier lessons for foundational concepts
- Look at `/examples/` for working implementations
- Check `/docs/compare_eval_frameworks/` for framework-specific guidance

**Found a Bug or Have a Suggestion?**
- Open an issue in the repository
- Submit a pull request with improvements
- Share your custom evaluators with the community

---

## 🏆 Completion Certificates

### Foundation Track Certificate (Lessons 1-7)

Once you've completed the foundation track, you'll have:

✅ **Foundational Knowledge**: Understanding of evaluation principles
✅ **Practical Skills**: Ability to implement various metrics
✅ **Framework Expertise**: Experience with evaluation frameworks
✅ **Production Ready**: Knowledge to deploy in real systems
✅ **Portfolio**: Custom evaluators you've built

**You're now equipped to evaluate any LLM system!** ⭐

---

### Advanced Track Certificate (Lessons 8-14)

After completing the advanced track, you'll have:

✅ **Statistical Rigor**: Hypothesis testing and confidence intervals
✅ **Robustness Testing**: Adversarial evaluation capabilities
✅ **Fairness Expertise**: Bias detection and mitigation
✅ **Benchmark Creation**: Professional dataset curation skills
✅ **Advanced Patterns**: RAG, multi-agent, and prompt optimization

**You're now an LLM Evaluation Expert!** 🎓

---

### Expert Metrics Track Certificate (Lessons 15-20)

After mastering the expert metrics track, you'll have:

✅ **100+ Metrics Mastery**: Complete evaluation toolkit across all domains
✅ **Text Quality**: BLEU, ROUGE, METEOR, Perplexity implementations
✅ **Safety Expertise**: Toxicity, hallucination, refusal evaluation
✅ **RAG Mastery**: Complete 15+ metric suite for retrieval systems
✅ **Agent Evaluation**: 20+ metrics for autonomous systems
✅ **Efficiency Optimization**: Latency, cost, and performance tuning

**You're now a World-Class Metrics Specialist!** 🏆

---

## 📈 Learning Path Progression

```
Level 0: Never Evaluated
    ↓
┌─────────────────────────────────┐
│   FOUNDATION TRACK (1-7)        │
├─────────────────────────────────┤
│ Lesson 1: Understanding Basics  │
│ Lesson 2: Simple Metrics         │
│ Lesson 3: LLM-as-Judge          │
│ Lesson 4: RAG Evaluation        │
│ Lesson 5: Custom Metrics        │
│ Lesson 6: Production Patterns   │
│ Lesson 7: Framework Usage       │
└─────────────────────────────────┘
    ↓
Level 5: Competent Evaluator ⭐
    ↓
┌─────────────────────────────────┐
│   ADVANCED TRACK (8-14)         │
├─────────────────────────────────┤
│ Lesson 8: Statistical Methods   │
│ Lesson 9: Adversarial Testing   │
│ Lesson 10: Bias & Fairness      │
│ Lesson 11: Benchmark Creation   │
│ Lesson 12: Advanced RAG         │
│ Lesson 13: Multi-Agent Systems  │
│ Lesson 14: Prompt Optimization  │
└─────────────────────────────────┘
    ↓
Level 10: Evaluation Expert! 🎓
    ↓
┌─────────────────────────────────┐
│   EXPERT METRICS TRACK (15-20)  │
├─────────────────────────────────┤
│ Lesson 15: Text Quality Metrics │
│ Lesson 16: Safety & Toxicity    │
│ Lesson 17: RAG Metrics Suite    │
│ Lesson 18: Agent Evaluation     │
│ Lesson 19: Task-Specific Metrics│
│ Lesson 20: Efficiency & Perf    │
└─────────────────────────────────┘
    ↓
Level 15: Metrics Master! 🏆
    ↓
World-Class Evaluation & Research Leadership
```

### Skill Progression

| Level | After Completing | Skills Acquired | Ready For |
|-------|-----------------|-----------------|-----------|
| **0** | - | No evaluation knowledge | Learning |
| **2** | Lessons 1-3 | Basic evaluation, simple metrics | Simple projects |
| **5** | Lessons 1-7 | Full foundation, framework usage | Production deployment |
| **7** | Lessons 1-10 | + Statistics, robustness, fairness | Critical systems |
| **10** | Lessons 1-14 | Complete evaluation mastery | Research, leadership |
| **15** | Lessons 1-20 | 100+ metrics, world-class expertise | Industry expert, cutting-edge research |

---

## 🎉 Start Learning Now!

```bash
cd docs/learn
python 01_basics_what_is_evaluation.py
```

**Happy Learning! 🚀**

Remember: Everyone starts somewhere. Take it one lesson at a time, practice consistently, and you'll become an evaluation expert before you know it!

---

## 📄 License

These educational materials are provided for learning purposes. Feel free to use, modify, and share!

---

**Last Updated**: 2026-01-18
**Version**: 3.0 (with Expert Metrics Track)
**Content**: 20 lessons (7 foundation + 7 advanced + 6 expert metrics)
**Difficulty Levels**: ⭐ Beginner | ⭐⭐ Intermediate | ⭐⭐⭐ Advanced
**Total Metrics**: 100+ specialized evaluation metrics across all domains

---

## 📝 Version History

### Version 3.0 (2026-01-18)
- 🏆 **NEW**: Expert Metrics Track (Lessons 15-20) - 100+ specialized metrics
- 📊 Lesson 15: Advanced Text Quality & Similarity Metrics (BLEU, ROUGE, METEOR, Perplexity)
- 🛡️ Lesson 16: Safety, Alignment & Toxicity Evaluation (Toxicity, Hallucination, Refusal)
- 🔍 Lesson 17: RAG Metrics Deep Dive (15+ retrieval, grounding, answer, context metrics)
- 🤖 Lesson 18: Agent Systems Evaluation (20+ task, reasoning, tool, robustness metrics)
- 🎯 Lesson 19: Task-Specific & Human-Centered Metrics (EM, F1, Pass@K, Execution)
- ⚡ Lesson 20: Efficiency & Performance Metrics (Latency, Throughput, Cost, Context)
- 📘 Added METRICS_REFERENCE.md - Comprehensive catalog of all 100+ metrics
- 🎓 Three-tier learning path: Foundation → Advanced → Expert Metrics
- 📈 Updated skill progression to Level 15 (Metrics Master)
- 🗺️ Enhanced learning paths by role with expert metrics track
- 📚 Expanded quick reference with expert metrics selector
- 🏆 Three completion certificates (Foundation ⭐, Advanced 🎓, Expert 🏆)
- ⏱️ Total learning time: ~14.5 hours for complete mastery

### Version 2.0 (2026-01-18)
- ✨ Added Advanced Track (Lessons 8-14)
- ✨ Added ADVANCED_TOPICS.md comprehensive guide
- 📚 Expanded learning paths by role
- 🎯 Added skill progression matrix
- 📊 Updated total content to 14 lessons

### Version 1.0 (2026-01-17)
- 🎉 Initial release with Foundation Track (Lessons 1-7)
- 📖 Basic to intermediate evaluation concepts
- 🛠️ Framework integration guide
