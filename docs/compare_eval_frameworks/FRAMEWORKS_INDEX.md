# LLM Evaluation Frameworks - Complete Index

**Navigation guide to all 18 evaluation framework comparisons and deep-dive documentation.**

---

## Quick Navigation

| # | Framework | Comparison | Deep Dive | Type | Focus |
|---|-----------|-----------|-----------|------|-------|
| 1 | **Custom-Evals** | [Compare](01_Custom_Evals.md) | [Deep Dive](framework_readme/01_Custom_Evals_README.md) | Library | Multi-framework |
| 2 | Arize Phoenix | [Compare](02_Arize_Phoenix.md) | [Deep Dive](framework_readme/02_Arize_Phoenix_README.md) | Platform | General LLM |
| 3 | RAGAS | [Compare](03_RAGAS.md) | [Deep Dive](framework_readme/03_RAGAS_README.md) | Library | RAG |
| 4 | Claude/Anthropic | [Compare](04_Claude_Anthropic.md) | [Deep Dive](framework_readme/04_Claude_Anthropic_README.md) | API | LLM-as-Judge |
| 5 | Google Vertex AI | [Compare](05_Google_Vertex_AI.md) | [Deep Dive](framework_readme/05_Google_Vertex_AI_README.md) | Platform | Enterprise GCP |
| 6 | LangSmith | [Compare](06_LangSmith.md) | [Deep Dive](framework_readme/06_LangSmith_README.md) | Platform | LangChain |
| 7 | OpenAI Evals | [Compare](07_OpenAI_Evals.md) | [Deep Dive](framework_readme/07_OpenAI_Evals_README.md) | CLI/Library | Standard |
| 8 | DeepEval | [Compare](08_DeepEval.md) | [Deep Dive](framework_readme/08_DeepEval_README.md) | Testing | CI/CD |
| 9 | TruLens | [Compare](09_TruLens.md) | [Deep Dive](framework_readme/09_TruLens_README.md) | Platform | Observability |
| 10 | Google ADK | [Compare](10_Google_ADK.md) | [Deep Dive](framework_readme/10_Google_ADK_README.md) | CLI | Agents |
| 11 | MLflow | [Compare](11_MLflow.md) | [Deep Dive](framework_readme/11_MLflow_README.md) | Platform | ML Lifecycle |
| 12 | MCPEval | [Compare](12_MCPEval.md) | [Deep Dive](framework_readme/12_MCPEval_README.md) | Library | Tool Calling |
| 13 | ARES | [Compare](13_ARES.md) | [Deep Dive](framework_readme/13_ARES_README.md) | Library | RAG/Synthetic |
| 14 | RAGalyst | [Compare](14_RAGalyst.md) | [Deep Dive](framework_readme/14_RAGalyst_README.md) | Library | RAG Analysis |
| 15 | Langfuse | [Compare](15_Langfuse.md) | [Deep Dive](framework_readme/15_Langfuse_README.md) | Platform | Production |
| 16 | Weave (W&B) | [Compare](16_Weave.md) | [Deep Dive](framework_readme/16_Weave_README.md) | Platform | Experiments |
| 17 | Braintrust | [Compare](17_Braintrust.md) | [Deep Dive](framework_readme/17_Braintrust_README.md) | Platform | AI Products |
| 18 | Humanloop | [Compare](18_Humanloop.md) | [Deep Dive](framework_readme/18_Humanloop_README.md) | Platform | Human Feedback |

---

## Browse by Category

### 📦 By Type

#### Lightweight Libraries
- [Custom-Evals](01_Custom_Evals.md) - Multi-framework, minimal deps
- [RAGAS](03_RAGAS.md) - RAG-specific
- [MCPEval](12_MCPEval.md) - Tool calling
- [OpenAI Evals](07_OpenAI_Evals.md) - Standardized

#### Full Platforms
- [Arize Phoenix](02_Arize_Phoenix.md) - General LLM + observability
- [LangSmith](06_LangSmith.md) - LangChain integration
- [Langfuse](15_Langfuse.md) - Production monitoring
- [Weave](16_Weave.md) - Experiment tracking
- [Braintrust](17_Braintrust.md) - AI product development
- [Humanloop](18_Humanloop.md) - Human-in-the-loop
- [TruLens](09_TruLens.md) - Observability
- [MLflow](11_MLflow.md) - ML lifecycle

#### Cloud Platforms
- [Google Vertex AI](05_Google_Vertex_AI.md) - GCP native
- [Google ADK](10_Google_ADK.md) - Agent development

#### Specialized Tools
- [RAGAS](03_RAGAS.md) - RAG evaluation
- [ARES](13_ARES.md) - RAG + synthetic data
- [RAGalyst](14_RAGalyst.md) - RAG optimization
- [MCPEval](12_MCPEval.md) - Function calling
- [DeepEval](08_DeepEval.md) - Testing/CI/CD

#### API-Based
- [Claude/Anthropic](04_Claude_Anthropic.md) - LLM-as-judge

---

### 🎯 By Use Case

#### RAG Systems
1. [RAGAS](03_RAGAS.md) - Best RAG metrics
2. [ARES](13_ARES.md) - RAG + synthetic data
3. [RAGalyst](14_RAGalyst.md) - Pipeline optimization
4. [Custom-Evals](01_Custom_Evals.md) - Flexible RAG eval
5. [TruLens](09_TruLens.md) - RAG debugging

#### Agent Evaluation
1. [Google ADK](10_Google_ADK.md) - Agent-specific
2. [MCPEval](12_MCPEval.md) - Tool calling
3. [Custom-Evals](01_Custom_Evals.md) - Multi-framework agents

#### Production Monitoring
1. [Langfuse](15_Langfuse.md) - Comprehensive observability
2. [LangSmith](06_LangSmith.md) - LangChain apps
3. [Arize Phoenix](02_Arize_Phoenix.md) - General monitoring
4. [TruLens](09_TruLens.md) - Detailed tracing
5. [Weave](16_Weave.md) - Experiment + production

#### CI/CD Integration
1. [DeepEval](08_DeepEval.md) - Pytest integration
2. [Braintrust](17_Braintrust.md) - Regression testing
3. [Custom-Evals](01_Custom_Evals.md) - Flexible testing
4. [OpenAI Evals](07_OpenAI_Evals.md) - CLI automation

#### Experiment Tracking
1. [Weave](16_Weave.md) - W&B integration
2. [MLflow](11_MLflow.md) - ML lifecycle
3. [Braintrust](17_Braintrust.md) - AI products
4. [Langfuse](15_Langfuse.md) - LLM experiments

#### Human-in-the-Loop
1. [Humanloop](18_Humanloop.md) - Human feedback focus
2. [Langfuse](15_Langfuse.md) - User feedback
3. [LangSmith](06_LangSmith.md) - Collaborative eval

---

### 💰 By Cost Model

#### Free & Open Source
- [Custom-Evals](01_Custom_Evals.md) - MIT license
- [RAGAS](03_RAGAS.md) - Apache 2.0
- [OpenAI Evals](07_OpenAI_Evals.md) - MIT
- [DeepEval](08_DeepEval.md) - Apache 2.0
- [TruLens](09_TruLens.md) - MIT
- [Google ADK](10_Google_ADK.md) - Apache 2.0
- [MLflow](11_MLflow.md) - Apache 2.0
- [MCPEval](12_MCPEval.md) - MIT
- [ARES](13_ARES.md) - Apache 2.0
- [RAGalyst](14_RAGalyst.md) - Apache 2.0

#### Freemium (Open Source + Cloud)
- [Langfuse](15_Langfuse.md) - Self-host or cloud
- [Weave](16_Weave.md) - Open SDK + cloud
- [Arize Phoenix](02_Arize_Phoenix.md) - Open source + enterprise

#### Commercial (Freemium)
- [LangSmith](06_LangSmith.md) - Free tier + paid
- [Braintrust](17_Braintrust.md) - Free tier + paid
- [Humanloop](18_Humanloop.md) - Free tier + paid

#### Enterprise/Cloud Only
- [Google Vertex AI](05_Google_Vertex_AI.md) - GCP pay-per-use
- [Claude/Anthropic](04_Claude_Anthropic.md) - API pricing

---

## Document Structure

Each framework has two documents:

### 1. Comparison Document (`XX_FrameworkName.md`)
- **Overview**: Quick summary and key info
- **Strengths & Weaknesses**: Pros/cons analysis
- **vs Custom-Evals**: Direct comparison
- **vs Other Frameworks**: How it compares
- **When to Choose**: Decision criteria
- **Pricing**: Cost breakdown
- **Quick Start**: Basic setup

### 2. Deep Dive Document (`framework_readme/XX_FrameworkName_README.md`)
- **Complete Architecture**: Technical deep-dive
- **Installation & Setup**: Detailed instructions
- **Core Concepts**: Key terminology and patterns
- **Complete Examples**: 5-10 production-ready examples
- **Advanced Usage**: Complex scenarios
- **Best Practices**: Expert recommendations
- **Integration Guide**: With other tools
- **Troubleshooting**: Common issues
- **API Reference**: Key APIs and methods
- **References**: Papers, blogs, videos, tutorials

---

## How to Use This Index

### For Quick Decisions
1. Check the **Complete Comparison**: [Compare_All_Eval_Frameworks.md](Compare_All_Eval_Frameworks.md)
2. Browse by category above
3. Read comparison docs for top 2-3 choices

### For Deep Understanding
1. Read comparison doc first
2. If interested, dive into the detailed README
3. Try the examples provided
4. Check reference materials

### For Specific Use Cases
1. Find your use case in "Browse by Category"
2. Review the recommended frameworks
3. Compare them side-by-side
4. Choose based on your requirements

---

## Additional Resources

- **[Complete Comparison](Compare_All_Eval_Frameworks.md)**: Side-by-side comparison of all 18 frameworks
- **[Examples Directory](../../examples/)**: Working code examples
- **[Custom-Evals Documentation](../../README.md)**: Main project docs

---

## Contributing

Found an issue or want to add information?
- Open an issue in the repository
- Submit a pull request with updates
- Share your experience with these frameworks

---

**Last Updated**: January 2026
**Frameworks Covered**: 18
**Documentation Pages**: 36+ (18 comparisons + 18 deep dives)

---

## Framework Versions Documented

| Framework | Version | Date |
|-----------|---------|------|
| Custom-Evals | 0.1.0 | Jan 2026 |
| Arize Phoenix | 4.x | Jan 2026 |
| RAGAS | 0.1.x | Jan 2026 |
| Claude API | Latest | Jan 2026 |
| Vertex AI | Latest | Jan 2026 |
| LangSmith | Latest | Jan 2026 |
| OpenAI Evals | Latest | Jan 2026 |
| DeepEval | 0.21.x | Jan 2026 |
| TruLens | 0.x | Jan 2026 |
| Google ADK | Latest | Jan 2026 |
| MLflow | 2.x | Jan 2026 |
| MCPEval | Latest | Jan 2026 |
| ARES | Latest | Jan 2026 |
| RAGalyst | Latest | Jan 2026 |
| Langfuse | 2.x | Jan 2026 |
| Weave | Latest | Jan 2026 |
| Braintrust | Latest | Jan 2026 |
| Humanloop | Latest | Jan 2026 |

---

**Happy Evaluating!** 🚀
