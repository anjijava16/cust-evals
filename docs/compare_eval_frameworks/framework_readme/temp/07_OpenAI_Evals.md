# OpenAI Evals: Community-Driven Evaluation Framework

**Type**: CLI Tool + Python Library | **License**: MIT (Open Source) | **Year**: 2023

---

## Quick Overview

OpenAI Evals is an **open-source evaluation framework** designed for evaluating LLMs with a CLI-first approach. It emphasizes standardized formats, reproducibility, and community contributions of evaluation datasets.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | Standardized evals, reproducibility |
| **Setup Time** | ⚡ 10 minutes |
| **Learning Curve** | Moderate |
| **Dependencies** | OpenAI API (primarily) |
| **Cost** | Free (OSS) + API costs |
| **Best For** | Model comparison, community benchmarks |

---

## Key Strengths

### ✅ Advantages

1. **CLI-First Design**
   - Run evals from command line
   - Scriptable and automatable
   - Easy CI/CD integration
   - No Python code required for basic use

2. **Standardized Format**
   - JSONL dataset format
   - Consistent structure
   - Easy to share evaluations
   - Reproducible results

3. **Community Evals**
   - 100+ pre-built evaluations
   - Community-contributed datasets
   - Diverse evaluation scenarios
   - Growing library of benchmarks

4. **Model Comparison**
   - Compare multiple models
   - A/B testing built-in
   - Statistical analysis
   - Structured result format

5. **Multiple Eval Types**
   - **Match**: Exact matching
   - **Includes**: Substring matching
   - **Fuzzy Match**: Approximate matching
   - **Model-graded**: LLM-as-judge
   - **Custom**: Define your own

6. **Registry System**
   - Register custom evaluations
   - Reusable eval definitions
   - Version control friendly
   - Share across teams

### ⚠️ Limitations

1. **OpenAI-Centric**
   - Primarily designed for OpenAI models
   - Other providers require workarounds
   - API dependency required
   - Not truly model-agnostic

2. **Complex Setup**
   - Registry system learning curve
   - YAML configuration required
   - Directory structure matters
   - Documentation can be unclear

3. **Limited Evaluator Types**
   - Fewer built-in evaluators than competitors
   - RAG evaluations basic
   - No advanced metrics out-of-box
   - Mostly classification-focused

4. **Dataset Management**
   - Manual JSONL file management
   - No built-in dataset hosting
   - Version control for datasets DIY
   - Can get messy at scale

5. **No UI or Visualization**
   - Command-line output only
   - External tools needed for viz
   - Results in JSON/log files
   - Manual analysis required

6. **Documentation Gaps**
   - Some features underdocumented
   - Examples can be outdated
   - Community support variable
   - Steep learning curve

---

## vs Other Frameworks

### vs Custom-Evals
| Aspect | OpenAI Evals | Custom-Evals |
|--------|--------------|--------------|
| **CLI Focus** | Strong | Minimal |
| **Standardization** | High | Flexible |
| **Setup** | Complex | Simple |
| **Model Support** | OpenAI-first | Multi-provider |
| **Community** | Large | Growing |
| **Code Required** | No (for basic) | Yes |

**Choose OpenAI Evals if**: You want standardized, reproducible benchmarks
**Choose Custom-Evals if**: You want flexibility and multi-provider support

---

### vs DeepEval
| Aspect | OpenAI Evals | DeepEval |
|--------|--------------|----------|
| **CLI** | Primary interface | Available |
| **Testing Framework** | Custom | Pytest |
| **Evaluators** | Basic | Comprehensive |
| **Learning Curve** | Steeper | Moderate |
| **Model Support** | OpenAI-first | Multi-provider |

**Choose OpenAI Evals if**: You want CLI-first with OpenAI
**Choose DeepEval if**: You want pytest integration and more evaluators

---

### vs LangSmith
| Aspect | OpenAI Evals | LangSmith |
|--------|--------------|-----------|
| **Open Source** | ✅ Yes | ❌ No |
| **UI Dashboard** | ❌ No | ✅ Yes |
| **Observability** | ❌ No | ✅ Yes |
| **Dataset Storage** | Local JSONL | Cloud |
| **Cost** | API only | Platform + API |

**Choose OpenAI Evals if**: You want OSS and CLI-based
**Choose LangSmith if**: You want managed service with UI

---

### vs RAGAS
| Aspect | OpenAI Evals | RAGAS |
|--------|--------------|-------|
| **Focus** | General | RAG-specific |
| **CLI** | Strong | Weak |
| **RAG Metrics** | Basic | Advanced |
| **Format** | JSONL | DataFrame |
| **Community Evals** | Large | Growing |

**Choose OpenAI Evals if**: General benchmarking and standardization
**Choose RAGAS if**: Deep RAG evaluation needed

---

## When to Choose OpenAI Evals

### ✅ Perfect For

1. **Model Comparison**
   - Compare GPT-4 vs GPT-3.5
   - A/B test different prompts
   - Benchmark new models
   - Track model improvements

2. **Standardized Benchmarks**
   - Reproducible evaluations
   - Share results with team
   - Industry-standard benchmarks
   - Academic research

3. **CI/CD Pipelines**
   - Automated eval runs
   - Command-line integration
   - Git-friendly format
   - Pre-commit/pre-deploy checks

4. **Community Contributions**
   - Use existing eval datasets
   - Contribute new evaluations
   - Build on community work
   - Standardized format for sharing

5. **OpenAI-Heavy Workflows**
   - Primarily using OpenAI models
   - Leverage OpenAI API
   - Model-graded evals with GPT-4
   - Official OpenAI support

### ❌ Not Ideal For

1. **Multi-Provider Use**
   - Need to evaluate Claude, Gemini, etc.
   - Requires hacks for non-OpenAI
   - Better tools available

2. **Interactive Development**
   - Want real-time feedback
   - Prefer notebooks
   - Need visual debugging
   - UI-driven workflows

3. **Complex RAG Evaluation**
   - Deep retrieval analysis
   - Context relevance metrics
   - Better specialized tools exist

4. **Minimal Setup Desired**
   - Want plug-and-play
   - Avoid registry complexity
   - Simple Python API preferred

---

## Pricing

### Cost Breakdown

| Component | Cost |
|-----------|------|
| **Framework** | 💰 **Free** (MIT License) |
| **OpenAI API** | Pay per token |
| **Infrastructure** | None required |
| **Support** | Community (GitHub) |

### Typical Evaluation Costs

Depends on:
- Model used (GPT-4 vs GPT-3.5)
- Number of test cases
- Eval type (match vs model-graded)

| Eval Type | Cost/Test | 1K Tests | 10K Tests |
|-----------|-----------|----------|-----------|
| **Match** (no API) | $0 | $0 | $0 |
| **Model-graded (3.5)** | $0.001 | $1 | $10 |
| **Model-graded (4)** | $0.01 | $10 | $100 |

### Cost Optimization

1. **Use Match-based evals**: Free, no API calls
2. **Sample datasets**: Evaluate subset first
3. **Use GPT-3.5**: Cheaper model-graded evals
4. **Batch evaluations**: Efficient API usage
5. **Cache model outputs**: Reuse when possible

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/openai/evals
cd evals

# Install with pip
pip install -e .

# Or install from PyPI
pip install evals
```

### Set API Key

```bash
export OPENAI_API_KEY="your-api-key"
```

### Run a Pre-Built Eval

```bash
# Run a community eval
oaieval gpt-3.5-turbo test-match

# Compare two models
oaieval gpt-4,gpt-3.5-turbo test-match

# Run specific eval
oaieval gpt-4 coqa

# With custom settings
oaieval gpt-4 coqa --max_samples 100
```

### Create Custom Dataset

Create `my_eval.jsonl`:

```jsonl
{"input": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is 2+2?"}], "ideal": "4"}
{"input": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Capital of France?"}], "ideal": "Paris"}
{"input": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Largest planet?"}], "ideal": "Jupiter"}
```

### Register Custom Eval

Create `evals/registry/evals/my_eval.yaml`:

```yaml
my_eval:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: my_eval.jsonl
```

### Run Custom Eval

```bash
oaieval gpt-3.5-turbo my_eval
```

---

## Architecture Highlights

### Core Components

```
OpenAI Evals Architecture:
┌─────────────────────────────────────┐
│   CLI (oaieval command)             │
│   - Argument parsing                │
│   - Model selection                 │
│   - Output formatting               │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Registry System                   │
│   - Eval definitions (YAML)         │
│   - Model configs                   │
│   - Dataset references              │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Eval Classes                      │
│   - Match, Includes, FuzzyMatch     │
│   - ModelGraded                     │
│   - Custom evaluators               │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Completion Functions              │
│   - OpenAI API calls                │
│   - Response handling               │
│   - Retry logic                     │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Results Recording                 │
│   - JSON output                     │
│   - Metrics aggregation             │
│   - Event logging                   │
└─────────────────────────────────────┘
```

### Directory Structure

```
evals/
├── evals/
│   ├── registry/
│   │   ├── evals/           # Eval definitions
│   │   ├── completion_fns/  # Model configs
│   │   └── data/            # JSONL datasets
│   ├── elsuite/             # Eval implementations
│   │   ├── basic/           # Match, includes, etc.
│   │   ├── modelgraded/     # LLM-as-judge
│   │   └── custom/          # Custom evals
│   └── cli/                 # CLI implementation
└── scripts/                 # Utility scripts
```

---

## Evaluation Types

### 1. Match (Exact)

```yaml
my_match_eval:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: questions.jsonl
```

```jsonl
{"input": "What is 2+2?", "ideal": "4"}
```

### 2. Includes (Substring)

```yaml
my_includes_eval:
  class: evals.elsuite.basic.includes:Includes
  args:
    samples_jsonl: questions.jsonl
```

```jsonl
{"input": "Name a primary color", "ideal": ["red", "blue", "yellow"]}
```

### 3. Fuzzy Match

```yaml
my_fuzzy_eval:
  class: evals.elsuite.basic.fuzzy_match:FuzzyMatch
  args:
    samples_jsonl: questions.jsonl
```

Allows approximate matching with edit distance.

### 4. Model-Graded

```yaml
my_modelgraded_eval:
  class: evals.elsuite.modelgraded.fact:Fact
  args:
    samples_jsonl: questions.jsonl
    eval_type: cot_classify
    modelgraded_spec: fact
```

```jsonl
{"input": "Explain quantum computing", "ideal": "Quantum computing uses quantum bits that can be in superposition..."}
```

Uses GPT-4 to grade responses.

### 5. Custom Evaluator

```python
# evals/elsuite/custom/my_eval.py
import evals
from evals.api import CompletionFn

class MyCustomEval(evals.Eval):
    def __init__(self, completion_fns, samples_jsonl, *args, **kwargs):
        super().__init__(completion_fns, *args, **kwargs)
        self.samples_jsonl = samples_jsonl

    def eval_sample(self, sample, *args):
        prompt = sample["input"]
        result = self.completion_fn(
            prompt=prompt,
            temperature=0.0,
        )

        sampled = result.get_completions()[0]

        # Custom scoring logic
        correct = self.custom_check(sampled, sample["ideal"])

        evals.record.record_match(
            correct=correct,
            expected=sample["ideal"],
            sampled=sampled,
        )

    def custom_check(self, response, expected):
        # Your custom logic here
        return response.lower().strip() == expected.lower().strip()
```

Register in YAML:

```yaml
my_custom_eval:
  class: evals.elsuite.custom.my_eval:MyCustomEval
  args:
    samples_jsonl: my_data.jsonl
```

---

## Advanced Usage

### Model Comparison

```bash
# Compare multiple models
oaieval gpt-4,gpt-3.5-turbo,gpt-3.5-turbo-16k my_eval

# Results show performance for each model
```

### Sampling & Randomization

```bash
# Run on subset
oaieval gpt-4 my_eval --max_samples 100

# Randomize sample order
oaieval gpt-4 my_eval --random_seed 42
```

### Custom Completion Function

Create `custom_completion.yaml`:

```yaml
custom-gpt-4:
  class: evals.completion_fns.openai:OpenAIChatCompletionFn
  args:
    model: gpt-4
    extra_options:
      temperature: 0.5
      max_tokens: 500
```

Use it:

```bash
oaieval custom-gpt-4 my_eval
```

### Results Analysis

```python
import json
import pandas as pd

# Load results
with open('/tmp/evallogs/results.jsonl') as f:
    results = [json.loads(line) for line in f]

# Convert to DataFrame
df = pd.DataFrame(results)

# Analyze
accuracy = df['correct'].mean()
print(f"Accuracy: {accuracy:.2%}")

# Per-category analysis
df.groupby('category')['correct'].mean()
```

---

## Best Practices

### 1. Dataset Organization

```
evals/registry/data/
├── my_project/
│   ├── factual_qa.jsonl
│   ├── creative_writing.jsonl
│   └── reasoning.jsonl
```

### 2. Version Control

```yaml
# Include version in eval name
my_eval_v1:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: my_eval_v1.jsonl

my_eval_v2:
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: my_eval_v2.jsonl
```

### 3. Metadata in Samples

```jsonl
{"input": "Question?", "ideal": "Answer", "metadata": {"category": "science", "difficulty": "easy"}}
```

### 4. Reusable Templates

```yaml
# Base template
base_qa_eval: &base_qa
  class: evals.elsuite.basic.match:Match
  args:
    samples_jsonl: null

# Specific evals
science_qa:
  <<: *base_qa
  args:
    samples_jsonl: science_qa.jsonl

history_qa:
  <<: *base_qa
  args:
    samples_jsonl: history_qa.jsonl
```

---

## Integration Examples

### With CI/CD

```yaml
# .github/workflows/eval.yml
name: Run Evals
on: [push]

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install evals
        run: pip install evals
      - name: Run evaluations
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          oaieval gpt-3.5-turbo my_eval
      - name: Check results
        run: python scripts/check_eval_results.py
```

### Programmatic Usage

```python
import evals
from evals.api import run_eval

# Run eval programmatically
result = run_eval(
    completion_fn="gpt-3.5-turbo",
    eval_name="my_eval",
    record_path="/tmp/results.jsonl"
)

print(f"Accuracy: {result['accuracy']}")
```

---

## Community Evals

### Available Benchmarks

- **CoQA**: Conversational question answering
- **TruthfulQA**: Truthfulness evaluation
- **HumanEval**: Code generation
- **MMLU**: Massive multitask language understanding
- **GSM8K**: Grade school math
- **HellaSwag**: Commonsense reasoning

### Browse Community Evals

```bash
# List all available evals
python -c "from evals.registry import Registry; r = Registry(); print(r.get_evals().keys())"

# Or check the registry directory
ls evals/registry/evals/
```

### Contributing Your Eval

1. Create dataset (JSONL)
2. Create eval definition (YAML)
3. Test locally
4. Submit PR to OpenAI/evals repo
5. Community benefits from your work

---

## Comparison Summary

### Unique Advantages
1. 🖥️ CLI-first design
2. 📋 Standardized JSONL format
3. 🌍 Large community of evals
4. 🔄 Easy model comparison
5. 🏗️ Reproducible benchmarks
6. 🔓 Open source and free

### Trade-offs
1. OpenAI-centric design
2. Complex registry system
3. No UI or visualization
4. Limited evaluator types
5. Steeper learning curve
6. Manual dataset management

---

## Resources

### Documentation
- **Official Docs**: https://github.com/openai/evals/tree/main/docs
- **GitHub**: https://github.com/openai/evals
- **Quickstart**: https://github.com/openai/evals/blob/main/docs/run-evals.md
- **Custom Evals Guide**: https://github.com/openai/evals/blob/main/docs/custom-eval.md

### Examples
- **Community Evals**: https://github.com/openai/evals/tree/main/evals/registry/evals
- **Sample Datasets**: https://github.com/openai/evals/tree/main/evals/registry/data
- **Model Configs**: https://github.com/openai/evals/tree/main/evals/registry/completion_fns

### Research & Papers
- **Evals Announcement**: https://openai.com/blog/evals
- **Contributing Guide**: https://github.com/openai/evals/blob/main/CONTRIBUTING.md

### Community
- **GitHub Issues**: https://github.com/openai/evals/issues
- **GitHub Discussions**: https://github.com/openai/evals/discussions
- **Pull Requests**: https://github.com/openai/evals/pulls

---

## Verdict

**OpenAI Evals is the best choice for teams wanting standardized, CLI-based evaluations with strong reproducibility and community benchmarks.**

**Rating**: ⭐⭐⭐⭐ (4/5 for standardization)

### Choose OpenAI Evals if you value:
- ✅ CLI-first workflows
- ✅ Standardized formats
- ✅ Model comparison
- ✅ Community benchmarks
- ✅ Reproducibility
- ✅ OpenAI models

### Choose alternatives if you need:
- ❌ Multi-provider support → Custom-Evals
- ❌ UI dashboard → Phoenix, LangSmith
- ❌ Rich evaluators → RAGAS, DeepEval
- ❌ Simpler setup → Custom-Evals
- ❌ RAG focus → RAGAS, TruLens

---

**Next**: [Compare All Frameworks](Compare_All_Eval_Frameworks.md) | [Try Custom-Evals](01_Custom_Evals.md)
