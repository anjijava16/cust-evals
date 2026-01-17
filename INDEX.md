# Custom Evals - Documentation Index

Welcome to Custom Evals! This index helps you find the right documentation for your needs.

## 🚀 Getting Started

**New to Custom Evals?** Start here:
1. [README.md](README.md) - Overview and quick start
2. [QUICKSTART.md](QUICKSTART.md) - Installation and basic usage
3. [examples/basic_usage.py](examples/basic_usage.py) - Working examples

## 📚 Core Documentation

### General Documentation

| File | Description | When to Read |
|------|-------------|--------------|
| [README.md](README.md) | Main documentation with overview | First read |
| [QUICKSTART.md](QUICKSTART.md) | Quick installation and usage | Getting started |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | What was built and why | Understanding scope |
| [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) | Recent changes and features | After updates |

### Technical Documentation

| File | Description | When to Read |
|------|-------------|--------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture and design | Understanding internals |
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | Project structure and patterns | Contributing |
| [README_EVALUATE_DETAILS.md](README_EVALUATE_DETAILS.md) | Complete evaluator methods guide | Using evaluators |

### Feature-Specific Guides

| File | Description | When to Read |
|------|-------------|--------------|
| [LLM_GUIDE.md](LLM_GUIDE.md) | LLM integration and usage | Using LLM evaluators |
| [GROUND_TRUTH_GUIDE.md](GROUND_TRUTH_GUIDE.md) | Ground truth handling | Production vs testing |
| [FRAMEWORK_COMPARISON.md](FRAMEWORK_COMPARISON.md) | Comparison with DeepEval/RAGAS | Understanding differences |

## 🎯 Find What You Need

### I want to...

**Learn the basics**
→ [README.md](README.md) + [QUICKSTART.md](QUICKSTART.md)

**Use code-based metrics**
→ [QUICKSTART.md](QUICKSTART.md) + [examples/basic_usage.py](examples/basic_usage.py)

**Use LLM evaluators**
→ [LLM_GUIDE.md](LLM_GUIDE.md) + [examples/llm_evaluation.py](examples/llm_evaluation.py)

**Evaluate RAG systems** (NEW!)
→ [FRAMEWORK_COMPARISON.md](FRAMEWORK_COMPARISON.md) + [examples/rag_evaluation.py](examples/rag_evaluation.py)

**Understand evaluator methods**
→ [README_EVALUATE_DETAILS.md](README_EVALUATE_DETAILS.md)

**Handle ground truth data**
→ [GROUND_TRUTH_GUIDE.md](GROUND_TRUTH_GUIDE.md) + [examples/ground_truth_examples.py](examples/ground_truth_examples.py)

**Compare with other frameworks** (NEW!)
→ [FRAMEWORK_COMPARISON.md](FRAMEWORK_COMPARISON.md)

**Understand the architecture**
→ [ARCHITECTURE.md](ARCHITECTURE.md) + [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

**See what changed recently**
→ [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)

**Contribute to the project**
→ [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) + [ARCHITECTURE.md](ARCHITECTURE.md)

## 📁 Directory Structure

```
cust-evals/
├── README.md                      ← Start here!
├── QUICKSTART.md                  ← Installation guide
├── INDEX.md                       ← You are here
│
├── Documentation/
│   ├── LLM_GUIDE.md              ← LLM usage
│   ├── GROUND_TRUTH_GUIDE.md     ← Ground truth handling
│   ├── README_EVALUATE_DETAILS.md ← Evaluator methods (645 lines!)
│   ├── ARCHITECTURE.md            ← System architecture
│   ├── PROJECT_OVERVIEW.md        ← Project structure
│   ├── IMPLEMENTATION_SUMMARY.md  ← What was built
│   └── CHANGES_SUMMARY.md         ← Recent changes
│
├── src/custom/evals/              ← Source code
│   ├── __init__.py
│   ├── evaluators.py              ← Score class, decorator
│   ├── llm_evaluators.py          ← LLM evaluators
│   ├── llm/                       ← LLM infrastructure
│   │   ├── wrapper.py             ← LLM class
│   │   └── prompts.py             ← Prompt templates
│   └── metrics/                   ← Code-based metrics
│       ├── exact_match.py
│       ├── sentiment.py
│       └── accuracy.py
│
├── examples/                      ← Working examples
│   ├── basic_usage.py             ← Code metrics
│   ├── llm_evaluation.py          ← LLM evaluators
│   └── ground_truth_examples.py   ← Ground truth
│
└── tests/                         ← Unit tests
    └── test_metrics.py
```

## 📖 Documentation by Topic

### Evaluators

**Overview**
- [README.md](README.md) - All evaluators listed

**Code-Based Metrics**
- `exact_match` - Binary comparison
- `sentiment_score` - Sentiment analysis
- `custom_accuracy` - Accuracy with normalization

**LLM-Based Evaluators - General**
- `HallucinationEvaluator` - Detect hallucinations
- `CorrectnessEvaluator` - Check correctness
- `RelevanceEvaluator` - Assess relevance
- `CoherenceEvaluator` - Check coherence

**LLM-Based Evaluators - RAG (NEW!)**
- `FaithfulnessEvaluator` - Verify response is grounded in context
- `AnswerRelevancyEvaluator` - Check answer-query relevance

### Evaluator Methods

**Complete Guide**
→ [README_EVALUATE_DETAILS.md](README_EVALUATE_DETAILS.md)

**Public API Methods**
- `evaluate()` - Main sync evaluation
- `async_evaluate()` - Async evaluation
- `describe()` - Get metadata

**Internal Methods**
- `_evaluate()` - Core logic
- `_async_evaluate()` - Async logic
- `_check_ground_truth()` - GT checking
- `_create_output_schema()` - Schema creation

### Ground Truth

**Complete Guide**
→ [GROUND_TRUTH_GUIDE.md](GROUND_TRUTH_GUIDE.md)

**Categories**
- Reference-Free (no GT needed)
- Reference-Based (GT required)
- Optional GT (works both ways)

**Examples**
→ [examples/ground_truth_examples.py](examples/ground_truth_examples.py)

### LLM Integration

**Complete Guide**
→ [LLM_GUIDE.md](LLM_GUIDE.md)

**Topics Covered**
- Setup and configuration
- Supported providers (OpenAI, Anthropic)
- Text generation
- Structured output
- Creating custom evaluators
- Best practices

**Examples**
→ [examples/llm_evaluation.py](examples/llm_evaluation.py)

### Architecture

**System Architecture**
→ [ARCHITECTURE.md](ARCHITECTURE.md)

**Topics Covered**
- Component architecture
- Data flow diagrams
- Design patterns
- Extensibility points
- Performance considerations

**Project Structure**
→ [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

## 🎓 Learning Paths

### Path 1: Beginner

1. Read [README.md](README.md)
2. Follow [QUICKSTART.md](QUICKSTART.md)
3. Run [examples/basic_usage.py](examples/basic_usage.py)
4. Try code-based metrics
5. Experiment with your own data

### Path 2: LLM User

1. Read [README.md](README.md)
2. Set up API keys
3. Read [LLM_GUIDE.md](LLM_GUIDE.md)
4. Run [examples/llm_evaluation.py](examples/llm_evaluation.py)
5. Try different evaluators
6. Read [GROUND_TRUTH_GUIDE.md](GROUND_TRUTH_GUIDE.md)

### Path 3: Advanced User

1. Read [README_EVALUATE_DETAILS.md](README_EVALUATE_DETAILS.md)
2. Read [ARCHITECTURE.md](ARCHITECTURE.md)
3. Understand internal methods
4. Create custom evaluators
5. Contribute improvements

### Path 4: Contributor

1. Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
2. Read [ARCHITECTURE.md](ARCHITECTURE.md)
3. Understand design patterns
4. Review existing code
5. Submit enhancements

## 🔍 Quick Reference

### Common Tasks

**Evaluate with code-based metric**
```python
from custom.evals import exact_match
score = exact_match({"output": "A", "expected": "A"})
```
→ [QUICKSTART.md](QUICKSTART.md)

**Evaluate with LLM**
```python
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)
score = evaluator.evaluate(eval_input)
```
→ [LLM_GUIDE.md](LLM_GUIDE.md)

**Get evaluator info**
```python
description = evaluator.describe()
```
→ [README_EVALUATE_DETAILS.md](README_EVALUATE_DETAILS.md)

**Async evaluation**
```python
score = await evaluator.async_evaluate(eval_input)
```
→ [README_EVALUATE_DETAILS.md](README_EVALUATE_DETAILS.md)

**Handle ground truth**
```python
# With GT
eval_input = {"output": "A", "expected": "A"}

# Without GT (reference-free)
eval_input = {"output": "A", "context": "C"}
```
→ [GROUND_TRUTH_GUIDE.md](GROUND_TRUTH_GUIDE.md)

## 📊 Documentation Stats

- **Total files**: 10 markdown files (NEW: FRAMEWORK_COMPARISON.md)
- **Total lines**: 3,600+ lines
- **Longest doc**: README_EVALUATE_DETAILS.md (645 lines)
- **Examples**: 4 working examples (NEW: rag_evaluation.py)
- **Evaluators documented**: 9 (NEW: Faithfulness, Answer Relevancy)

## 🆘 Need Help?

**Can't find what you need?**
1. Check [README.md](README.md) - Main overview
2. Search this INDEX.md for keywords
3. Check [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) for recent updates

**Still stuck?**
- Review examples in `examples/` directory
- Check source code docstrings
- Read method signatures in source files

## ✨ Happy Evaluating!

Start with [README.md](README.md) and explore from there!
