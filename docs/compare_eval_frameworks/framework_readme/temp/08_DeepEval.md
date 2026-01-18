# DeepEval: The pytest-Native LLM Testing Framework

**Type**: Python Framework | **License**: Apache-2.0 (Open Source) | **Year**: 2022+

---

## Quick Overview

DeepEval is the **industry-standard LLM evaluation framework** designed for **maximum CI/CD integration**. Trusted by OpenAI, Google, Adobe, and Walmart, it brings pytest-style testing to LLM applications with 50+ research-backed metrics and native pytest integration.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | Testing & CI/CD integration |
| **Setup Time** | 10 minutes |
| **Learning Curve** | Easy (if familiar with pytest) |
| **Dependencies** | Moderate |
| **Cost** | Free (OSS) + Optional Confident AI Platform |
| **Best For** | Teams prioritizing testing workflows |

---

## Key Strengths

### Advantages

1. **Native Pytest Integration**
   - `assert_test()` API mirrors pytest patterns
   - `deepeval test run` command for enhanced pytest features
   - Seamless CI/CD pipeline integration
   - Familiar testing patterns for developers
   - 8+ optional configuration flags for customization

2. **Industry-Leading CI/CD Support**
   - GitHub Actions ready with templates
   - GitLab, Jenkins, CircleCI compatible
   - Pre-deployment quality gates
   - Automated regression detection
   - Test result tracking via Confident AI

3. **Comprehensive Metrics Library**
   - 50+ research-backed metrics out-of-the-box
   - 7 metric categories: Custom, RAG, Agentic, Multi-Turn, Safety, Image, General
   - **G-Eval**: Natural language criteria for subjective scoring
   - **DAG**: Decision-tree approach for objective evaluation
   - **QAG**: Question-Answer Generation for close-ended scoring
   - Multi-modal support (text, image, audio)

4. **Advanced Red-Teaming Capabilities**
   - 40+ LLM vulnerability detection
   - 10+ attack enhancement strategies
   - Security categories: BFLA, BOLA, RBAC, SSRF
   - Safety categories: Illegal activity, graphic content
   - Automated jailbreak testing
   - OWASP Top 10 for LLMs alignment
   - NIST AI Risk Management compliance

5. **Test Case Management**
   - LLMTestCase for single-turn evaluations
   - ConversationalTestCase for multi-turn
   - Golden datasets for regression testing
   - Synthetic data generation
   - EvaluationDataset for batch testing

6. **Component-Level Tracing**
   - `@observe()` decorator for white-box testing
   - LLM tracing for complex workflows
   - Individual component evaluation
   - Production monitoring capabilities
   - Test case updates within traces

7. **Production-Ready**
   - Used by Fortune 500 companies
   - Confident AI cloud platform available
   - Experiment tracking and comparison
   - Online monitoring and alerting
   - Human feedback integration

### Limitations

1. **Infrastructure Overhead**
   - More dependencies than minimal frameworks
   - Optional cloud platform adds complexity
   - Requires API keys for most metrics

2. **Learning Curve**
   - More concepts to learn vs simple evaluators
   - Test case abstraction adds layer
   - Tracing decorator pattern requires understanding

3. **Opinionated Structure**
   - Strong pytest coupling (by design)
   - Test case objects required
   - Less flexible than custom implementations

---

## vs Other Frameworks

### vs Custom-Evals

| Aspect | DeepEval | Custom-Evals |
|--------|----------|--------------|
| **Test Integration** | Native pytest | Manual testing |
| **CI/CD** | Best-in-class | Works well |
| **Metrics Library** | 50+ built-in | Core set + extensible |
| **Dependencies** | Moderate | Minimal |
| **Flexibility** | Medium | Higher |
| **Red-Teaming** | Built-in 40+ vulnerabilities | Manual implementation |
| **Dashboard** | Confident AI platform | External (Phoenix) |
| **Learning Curve** | Medium | Easy |

**Choose DeepEval if**: You need pytest integration and comprehensive CI/CD
**Choose Custom-Evals if**: You want minimal dependencies and maximum flexibility

---

### vs RAGAS

| Aspect | DeepEval | RAGAS |
|--------|----------|-------|
| **Scope** | General + RAG + Agents | RAG-focused |
| **Testing** | Pytest native | Evaluation-focused |
| **CI/CD** | Excellent | Good |
| **Metrics** | 50+ (all types) | RAG-specific |
| **Multi-Turn** | Built-in support | Limited |
| **Red-Teaming** | 40+ vulnerabilities | Not included |
| **Agentic** | Native support | Not included |

**Choose DeepEval if**: You need comprehensive testing beyond RAG
**Choose RAGAS if**: You're 100% focused on RAG evaluation with research-backed metrics

---

### vs OpenAI Evals

| Aspect | DeepEval | OpenAI Evals |
|--------|----------|--------------|
| **Maintenance** | Active (2024+) | Archived |
| **Pytest** | Native integration | Not included |
| **Metrics** | 50+ modern | Limited |
| **CI/CD** | Best-in-class | Basic |
| **Multi-Modal** | Text, image, audio | Primarily text |
| **Red-Teaming** | Built-in | Manual |
| **Community** | Growing | Legacy |

**Choose DeepEval if**: You need modern, maintained framework
**Choose OpenAI Evals if**: You're maintaining legacy systems only

---

### vs LangSmith

| Aspect | DeepEval | LangSmith |
|--------|----------|-----------|
| **Infrastructure** | Optional cloud | Required cloud |
| **Cost** | Free OSS + optional platform | Platform subscription |
| **Pytest** | Native | Not native |
| **CI/CD** | Excellent | Good |
| **Observability** | Via Confident AI | Built-in |
| **Vendor Lock-in** | Low (OSS core) | Medium |
| **Red-Teaming** | Built-in | Limited |

**Choose DeepEval if**: You want pytest-native testing with OSS core
**Choose LangSmith if**: You're heavily invested in LangChain ecosystem

---

## When to Choose DeepEval

### Perfect For

1. **CI/CD-Focused Teams**
   - Automated testing in pipelines
   - Pre-deployment quality gates
   - GitHub Actions, GitLab CI, Jenkins
   - Regression detection across releases
   - Test-driven LLM development

2. **pytest Users**
   - Teams already using pytest
   - Familiar testing patterns
   - Easy integration with existing test suites
   - Standard test discovery and execution
   - Fixture and parameterization support

3. **Comprehensive Testing Requirements**
   - Single-turn and multi-turn evaluations
   - Component-level and end-to-end testing
   - RAG, agents, and chatbot testing
   - Multi-modal applications
   - Security and safety testing

4. **Enterprise Security**
   - Red-teaming requirements
   - Vulnerability scanning (40+ types)
   - Compliance with OWASP, NIST
   - Attack simulation and jailbreak testing
   - Safety risk assessment

5. **Teams Wanting Best of Both Worlds**
   - Open-source framework + optional platform
   - Local testing + cloud tracking
   - Free for development + paid for production
   - Self-hosted or cloud deployment

### Not Ideal For

1. **Minimal Dependency Requirements**
   - DeepEval has moderate dependencies
   - Consider Custom-Evals for lightweight needs

2. **Non-pytest Workflows**
   - Teams not using pytest patterns
   - Prefer simple evaluation scripts
   - Custom testing frameworks

3. **Maximum Flexibility**
   - Highly customized evaluation logic
   - Non-standard testing patterns
   - Framework-agnostic requirements

---

## Pricing

### Cost Breakdown

| Component | Cost |
|-----------|------|
| **DeepEval Framework** | Free (Apache-2.0 License) |
| **LLM API** | Pay per evaluation (~$0.001-0.01 each) |
| **Confident AI - Free** | Free forever (1 project, 1 user) |
| **Confident AI - Starter** | ~$30/user/month |
| **Confident AI - Premium** | ~$80/user/month |

### Typical Monthly Costs

| Evaluations/Month | Framework Cost | LLM API Cost | Confident AI | Total |
|-------------------|----------------|--------------|--------------|-------|
| 1,000 | $0 | $1-10 | $0 (Free tier) | $1-10 |
| 10,000 | $0 | $10-100 | $0-30 | $10-130 |
| 100,000 | $0 | $100-1,000 | $30-80 | $130-1,080 |

### Confident AI Platform Features

**Free Tier**:
- 1 project, 1 user
- Basic test tracking
- Experiment comparison
- Public community support

**Starter Tier (~$30/user/month)**:
- Multiple projects
- Extended data retention
- Team collaboration
- Email support

**Premium Tier (~$80/user/month)**:
- Advanced observability
- Human feedback integration
- SSO (Single Sign-On)
- Priority support
- HIPAA/GDPR compliance
- Self-hosting options (AWS, Azure, GCP)

**Note**: Core DeepEval framework is free forever. Confident AI platform is optional.

---

## Quick Start

### Installation

```bash
# Install DeepEval
pip install -U deepeval

# Optional: Login to Confident AI for cloud features
deepeval login
```

### 5-Minute pytest Example

Create `test_example.py`:

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

def test_answer_relevancy():
    # Define test case
    test_case = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital of France, known for the Eiffel Tower."
    )

    # Define metric with threshold
    metric = AnswerRelevancyMetric(threshold=0.7)

    # Assert test passes
    assert_test(test_case, [metric])
```

Run with DeepEval:

```bash
deepeval test run test_example.py
```

### Multi-Turn Conversation Example

```python
from deepeval import assert_test
from deepeval.test_case import Turn, ConversationalTestCase
from deepeval.metrics import ConversationalGEval

def test_chatbot_professionalism():
    # Define conversation
    test_case = ConversationalTestCase(
        turns=[
            Turn(role="user", content="What is DeepEval?"),
            Turn(role="assistant", content="DeepEval is an open-source LLM evaluation framework."),
            Turn(role="user", content="How do I install it?"),
            Turn(role="assistant", content="Simply run: pip install -U deepeval")
        ]
    )

    # Define custom G-Eval metric
    professionalism_metric = ConversationalGEval(
        name="Professionalism",
        criteria="Determine whether the assistant maintained professional tone throughout.",
        threshold=0.7
    )

    assert_test(test_case, [professionalism_metric])
```

### Custom G-Eval Metric

```python
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

def test_medical_accuracy():
    # Define custom criteria with G-Eval
    medical_accuracy = GEval(
        name="Medical Accuracy",
        criteria="Assess if the medical advice is accurate and safe based on medical guidelines.",
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT
        ],
        threshold=0.8,
        model="gpt-4o"  # Use specific model for evaluation
    )

    test_case = LLMTestCase(
        input="I have persistent cough and fever. What should I do?",
        actual_output="See a doctor if symptoms persist for more than 3 days or worsen.",
        expected_output="Consult healthcare professional for persistent symptoms."
    )

    assert_test(test_case, [medical_accuracy])
```

### RAG Evaluation Example

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric
)

def test_rag_pipeline():
    test_case = LLMTestCase(
        input="What are the symptoms of COVID-19?",
        actual_output="Common symptoms include fever, cough, and fatigue.",
        retrieval_context=[
            "COVID-19 symptoms: fever, dry cough, tiredness.",
            "Less common symptoms: aches, sore throat, diarrhea."
        ]
    )

    # Evaluate multiple RAG dimensions
    metrics = [
        AnswerRelevancyMetric(threshold=0.7),
        FaithfulnessMetric(threshold=0.8),
        ContextualRelevancyMetric(threshold=0.6)
    ]

    assert_test(test_case, metrics)
```

### Component-Level Testing with Tracing

```python
from deepeval.tracing import observe, update_current_span
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

@observe()
def my_rag_pipeline(query: str):
    # Retrieval component
    @observe(metrics=[ContextualRelevancyMetric()])
    def retrieve(query: str):
        contexts = ["Retrieved doc 1", "Retrieved doc 2"]
        update_current_span(
            test_case=LLMTestCase(
                input=query,
                retrieval_context=contexts
            )
        )
        return contexts

    # Generation component
    @observe(metrics=[AnswerRelevancyMetric()])
    def generate(query: str, contexts: list):
        response = f"Based on context: {contexts[0]}"
        update_current_span(
            test_case=LLMTestCase(
                input=query,
                actual_output=response
            )
        )
        return response

    contexts = retrieve(query)
    return generate(query, contexts)

# Run component-level evaluation
result = my_rag_pipeline("What is DeepEval?")
```

### Red-Teaming Example

```python
from deepeval.red_teaming import RedTeamer
from deepeval.vulnerability import (
    Vulnerability,
    VulnerabilityType
)

# Define target LLM application
def banking_chatbot(prompt: str) -> str:
    # Your LLM application logic
    return "How can I help with your banking needs?"

# Initialize red teamer
red_teamer = RedTeamer(
    target_callback=banking_chatbot,
    vulnerabilities=[
        VulnerabilityType.BFLA,  # Function bypass
        VulnerabilityType.BOLA,  # Object access
        VulnerabilityType.PII_LEAK,  # Data privacy
        VulnerabilityType.JAILBREAK  # Safety bypass
    ],
    attacks_per_vulnerability=5
)

# Run red team scan
results = red_teamer.scan()

# Review vulnerabilities found
for vuln in results.vulnerabilities:
    print(f"Vulnerability: {vuln.type}")
    print(f"Severity: {vuln.severity}")
    print(f"Attack: {vuln.attack}")
    print(f"Response: {vuln.response}")
```

---

## CI/CD Integration

### GitHub Actions Workflow

Create `.github/workflows/deepeval.yml`:

```yaml
name: LLM Unit Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install Poetry
        run: curl -sSL https://install.python-poetry.org | python3 -

      - name: Install dependencies
        run: poetry install --no-root

      - name: Run DeepEval tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          CONFIDENT_API_KEY: ${{ secrets.CONFIDENT_API_KEY }}
        run: poetry run deepeval test run test_llm_app.py

      - name: Upload test results (optional)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: deepeval-results
          path: .deepeval/
```

### GitLab CI Example

Create `.gitlab-ci.yml`:

```yaml
test_llm:
  stage: test
  image: python:3.10
  before_script:
    - pip install poetry
    - poetry install --no-root
  script:
    - poetry run deepeval test run test_llm_app.py
  variables:
    OPENAI_API_KEY: $OPENAI_API_KEY
    CONFIDENT_API_KEY: $CONFIDENT_API_KEY
  only:
    - main
    - merge_requests
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any

    environment {
        OPENAI_API_KEY = credentials('openai-api-key')
        CONFIDENT_API_KEY = credentials('confident-api-key')
    }

    stages {
        stage('Setup') {
            steps {
                sh 'pip install poetry'
                sh 'poetry install --no-root'
            }
        }

        stage('Run LLM Tests') {
            steps {
                sh 'poetry run deepeval test run test_llm_app.py'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '.deepeval/**/*', allowEmptyArchive: true
        }
    }
}
```

### Best Practices for CI/CD

1. **Use `deepeval test run` instead of `pytest`**
   - Provides 8+ specialized flags
   - Better error handling for LLM evaluations
   - Automatic retry logic for API failures

2. **Store API keys in secrets**
   - Never commit keys to repository
   - Use GitHub Secrets, GitLab Variables, etc.
   - Rotate keys regularly

3. **Run on key branches**
   - Main/master branch
   - Development branches
   - All pull requests

4. **Track results in Confident AI**
   - Compare across releases
   - Detect regressions automatically
   - Share results with team

5. **Set appropriate thresholds**
   - Start conservative (0.6-0.7)
   - Tighten as needed (0.8+)
   - Balance quality vs speed

---

## Architecture Highlights

### Design Principles

1. **Pytest-Native**: Built on pytest foundation for familiar testing patterns
2. **Test-First**: Encourages test-driven LLM development
3. **Component-Aware**: White-box testing via tracing decorators
4. **Security-First**: Built-in red-teaming and vulnerability scanning
5. **Platform-Optional**: Works standalone or with Confident AI cloud

### Key Components

```
deepeval/
├── test_case.py          # LLMTestCase, ConversationalTestCase
├── assert_test.py        # Pytest-style assertions
├── metrics/
│   ├── answer_relevancy.py
│   ├── faithfulness.py
│   ├── contextual_relevancy.py
│   ├── g_eval.py         # Custom criteria evaluation
│   ├── dag.py            # Decision tree evaluation
│   └── [50+ metrics]
├── red_teaming/
│   ├── vulnerabilities.py  # 40+ vulnerability types
│   ├── attacks.py          # Attack strategies
│   └── scanner.py          # Automated scanning
├── tracing/
│   ├── observe.py        # @observe decorator
│   └── span.py           # Span management
└── dataset/
    ├── golden.py         # Golden test cases
    └── synthetic.py      # Data generation
```

### Evaluation Approaches

**1. End-to-End Evaluation**
- Black-box testing
- Complete application testing
- Single-turn and multi-turn
- Minimal setup required

**2. Component-Level Evaluation**
- White-box testing
- Individual component testing
- Tracing-based
- Production monitoring

### Metric Categories

1. **Custom Metrics**: G-Eval, DAG, custom implementations
2. **RAG Metrics**: Answer relevancy, faithfulness, contextual relevancy
3. **Agentic Metrics**: Tool usage, task completion, multi-hop reasoning
4. **Multi-Turn Metrics**: Conversation quality, coherence, knowledge retention
5. **Safety Metrics**: Bias, toxicity, PII detection
6. **Image Metrics**: Visual quality, text-image alignment
7. **General Purpose**: Hallucination, JSON validation, summarization

### Integration Ecosystem

**Supported Frameworks**:
- LangChain / LangGraph
- LlamaIndex
- Pydantic AI
- CrewAI
- OpenAI SDK
- Anthropic SDK
- Google Gemini
- Custom implementations

**Supported LLM Providers**:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)
- Azure OpenAI
- Ollama (local models)
- Custom LLM implementations

---

## Comparison Summary

### Unique Advantages

1. Native pytest integration for familiar testing patterns
2. Industry-leading CI/CD support with templates
3. Comprehensive 50+ metric library
4. Built-in red-teaming with 40+ vulnerability types
5. Test case management and regression tracking
6. Component-level tracing for white-box testing
7. Multi-modal evaluation (text, image, audio)
8. Optional cloud platform without vendor lock-in

### Trade-offs

1. More dependencies than minimal frameworks
2. Learning curve for tracing patterns
3. Opinionated test case structure
4. Moderate setup complexity

### When DeepEval Excels

1. **CI/CD Pipelines**: Best-in-class integration
2. **Pytest Workflows**: Native compatibility
3. **Comprehensive Testing**: 50+ metrics out-of-box
4. **Security Testing**: Built-in red-teaming
5. **Enterprise Adoption**: Production-proven
6. **Team Collaboration**: Cloud platform available

---

## Migration Path

### From Custom-Evals

```python
# Custom-Evals
from custom.evals import AnswerRelevancyEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = AnswerRelevancyEvaluator(llm)
score = evaluator.evaluate({"input": query, "output": response})

# DeepEval
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

def test_answer_relevancy():
    test_case = LLMTestCase(input=query, actual_output=response)
    metric = AnswerRelevancyMetric(threshold=0.7)
    assert_test(test_case, [metric])
```

### From RAGAS

```python
# RAGAS
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy]
)

# DeepEval
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric

def test_rag():
    test_case = LLMTestCase(
        input=query,
        actual_output=response,
        retrieval_context=contexts
    )
    metrics = [
        FaithfulnessMetric(threshold=0.7),
        AnswerRelevancyMetric(threshold=0.7)
    ]
    assert_test(test_case, metrics)
```

### From OpenAI Evals

```python
# OpenAI Evals (deprecated)
# Complex YAML-based configuration
# Limited to OpenAI models
# Manual test execution

# DeepEval (modern)
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import GEval

def test_with_custom_criteria():
    metric = GEval(
        name="Helpfulness",
        criteria="Is the response helpful and actionable?",
        threshold=0.7
    )
    test_case = LLMTestCase(
        input="How do I reset my password?",
        actual_output="Click 'Forgot Password' and follow email instructions."
    )
    assert_test(test_case, [metric])
```

---

## Resources

### Official Documentation

- **Main Site**: [deepeval.com](https://deepeval.com/)
- **Documentation**: [deepeval.com/docs/getting-started](https://deepeval.com/docs/getting-started)
- **Metrics Guide**: [deepeval.com/docs/metrics-introduction](https://deepeval.com/docs/metrics-introduction)
- **CI/CD Guide**: [deepeval.com/docs/evaluation-unit-testing-in-ci-cd](https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd)
- **Red Teaming**: [deepeval.com/guides/guides-red-teaming](https://deepeval.com/guides/guides-red-teaming)
- **GitHub**: [github.com/confident-ai/deepeval](https://github.com/confident-ai/deepeval)
- **PyPI**: [pypi.org/project/deepeval](https://pypi.org/project/deepeval/)

### Confident AI Platform

- **Platform**: [confident-ai.com](https://www.confident-ai.com/)
- **Login**: `deepeval login` via CLI
- **Features**: Experiment tracking, regression detection, team collaboration

### Red Teaming Resources

- **DeepTeam Framework**: [trydeepteam.com](https://www.trydeepteam.com/)
- **DeepTeam Docs**: [trydeepteam.com/docs/getting-started](https://www.trydeepteam.com/docs/getting-started)
- **Vulnerabilities**: [trydeepteam.com/docs/red-teaming-vulnerabilities](https://www.trydeepteam.com/docs/red-teaming-vulnerabilities)
- **GitHub**: [github.com/confident-ai/deepteam](https://github.com/confident-ai/deepteam)

### Community & Learning

- **GitHub Issues**: [github.com/confident-ai/deepeval/issues](https://github.com/confident-ai/deepeval/issues)
- **Blog**: [confident-ai.com/blog](https://www.confident-ai.com/blog)
- **CI/CD Tutorial**: [How to Evaluate RAG Applications in CI/CD Pipelines](https://www.confident-ai.com/blog/how-to-evaluate-rag-applications-in-ci-cd-pipelines-with-deepeval)
- **DataCamp Guide**: [Evaluate LLMs Effectively Using DeepEval](https://www.datacamp.com/tutorial/deepeval)

### Comparison Resources

- **vs Custom-Evals**: [01_Custom_Evals.md](01_Custom_Evals.md)
- **vs RAGAS**: [02_RAGAS.md](02_RAGAS.md)
- **vs All Frameworks**: [Compare_All_Eval_Frameworks.md](Compare_All_Eval_Frameworks.md)

---

## Verdict

**DeepEval is the best choice for teams prioritizing CI/CD integration, pytest workflows, and comprehensive testing with built-in security scanning.**

**Rating**: ⭐⭐⭐⭐⭐ (5/5 for CI/CD and testing)

### Choose DeepEval if you value:

- Native pytest integration and familiar testing patterns
- Best-in-class CI/CD pipeline support
- Comprehensive 50+ metric library
- Built-in red-teaming and security scanning
- Test case management and regression tracking
- Component-level tracing for complex systems
- Optional cloud platform without lock-in
- Production-proven at enterprise scale

### Choose alternatives if you need:

- Minimal dependencies → Custom-Evals
- RAG-only focus → RAGAS
- Maximum flexibility → Custom-Evals
- Heavy LangChain integration → LangSmith
- No pytest requirement → Custom-Evals, Phoenix

---

**Next**: [Compare All Frameworks](Compare_All_Eval_Frameworks.md) | [Custom-Evals vs DeepEval Deep Dive](01_Custom_Evals.md)
