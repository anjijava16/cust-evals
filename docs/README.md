# Custom Evals Documentation

Welcome to the **Custom Evals** documentation! This is a lightweight, flexible evaluation framework for LLM outputs, inspired by Phoenix Evals and enhanced with metrics from DeepEval and RAGAS.

## 📚 Documentation Structure

### Getting Started
- **[Installation & Quick Start](getting-started.md)** - Get up and running in minutes
- **[Examples](examples.md)** - Working code examples for all evaluators

### Evaluators
- **[Code-Based Metrics](evaluators/code-based.md)** - exact_match, sentiment_score, custom_accuracy
- **[LLM-Based Evaluators](evaluators/llm-based.md)** - General LLM evaluation (hallucination, correctness, relevance, coherence)
- **[RAG-Specific Evaluators](evaluators/rag-specific.md)** - RAG system evaluation (faithfulness, answer relevancy)

### API Reference
- **[Core API](api-reference.md)** - Score class, create_evaluator decorator, evaluator methods
- **[LLM Integration](llm-integration.md)** - LLM class, supported providers, configuration

### Integration Guides
- **[Agents Integration](agents-integration.md)** - Integrate with AI agents and multi-agent systems (LangChain, LlamaIndex, CrewAI, custom agents)
- **[RAG Integration](rag-integration.md)** - Integrate with RAG applications (LangChain RAG, LlamaIndex RAG, custom RAG)
- **[LLM App Integration](llm-app-integration.md)** - Integrate with simple LLM applications (chatbots, Q&A, summarization, classification)

### Advanced Topics
- **[Phoenix Tracing (Optional)](tracing.md)** - OpenTelemetry tracing for observability with Phoenix (Arize)
- **[Ground Truth Handling](ground-truth.md)** - Flexible ground truth support for production and testing
- **[Architecture](architecture.md)** - System design, patterns, and extensibility
- **[Framework Comparison](framework-comparison.md)** - How we compare to DeepEval, RAGAS, Phoenix Evals

### Testing
- **[Testing Guide](testing.md)** - Comprehensive test suite documentation (150+ tests)

### Contributing
- **[Contributing Guide](contributing.md)** - How to add new evaluators and metrics

---

## 🚀 Quick Links

### For New Users
1. Start with **[Getting Started](getting-started.md)**
2. Try **[Examples](examples.md)**
3. Explore **[Code-Based Metrics](evaluators/code-based.md)**

### For Agent Projects
1. Read **[Agents Integration](agents-integration.md)**
2. Works with **ALL frameworks** (LangChain, LlamaIndex, CrewAI, custom)
3. Multi-agent system evaluation included

### For RAG Applications
1. Read **[RAG Integration](rag-integration.md)**
2. See **[RAG-Specific Evaluators](evaluators/rag-specific.md)**
3. Works with **ALL RAG frameworks**

### For LLM Applications
1. Read **[LLM App Integration](llm-app-integration.md)**
2. Use **[LLM-Based Evaluators](evaluators/llm-based.md)**
3. Covers chatbots, Q&A, summarization, classification

### For Testing & Quality
1. Read **[Testing Guide](testing.md)**
2. Run tests: `pytest`
3. Check coverage: `pytest --cov=custom.evals`

### For Contributors
1. Read **[Architecture](architecture.md)**
2. Check **[Contributing Guide](contributing.md)**
3. Review **[API Reference](api-reference.md)**

---

## 📊 What's Included

### 9 Evaluators

**Code-Based (3)**
- Exact Match - Binary comparison
- Sentiment Score - Sentiment analysis
- Custom Accuracy - Flexible accuracy with normalization

**LLM-Based (4)**
- Hallucination Evaluator - Detect hallucinations
- Correctness Evaluator - Assess correctness
- Relevance Evaluator - Evaluate relevance
- Coherence Evaluator - Check coherence

**RAG-Specific (2)**
- Faithfulness Evaluator - Verify grounding in context
- Answer Relevancy Evaluator - Check answer-query relevance

### Key Features

✅ **Flexible Ground Truth** - Works with or without ground truth data
✅ **Async Support** - Concurrent evaluation with async methods
✅ **Multi-Provider** - OpenAI and Anthropic support
✅ **Phoenix Evals Compatible** - Similar API design
✅ **RAG Optimized** - Metrics from DeepEval and RAGAS
✅ **Optional Tracing** - Phoenix (Arize) tracing via OpenTelemetry (completely optional)
✅ **Extensible** - Easy to add custom evaluators

---

## 🔗 External Resources

- **[Phoenix Evals](https://github.com/Arize-ai/phoenix)** - Original inspiration
- **[DeepEval](https://deepeval.com)** - RAG metrics inspiration
- **[RAGAS](https://docs.ragas.io)** - RAG evaluation framework
- **[GitHub Repository](https://github.com/your-repo/cust-evals)** - Source code

---

## 💡 Need Help?

1. Check the **[Getting Started](getting-started.md)** guide
2. Browse **[Examples](examples.md)**
3. Read **[API Reference](api-reference.md)**
4. Open an issue on GitHub

---

## 📝 License

This is a proof-of-concept evaluation framework. See LICENSE for details.

---

**Ready to get started?** → [Installation & Quick Start](getting-started.md)
