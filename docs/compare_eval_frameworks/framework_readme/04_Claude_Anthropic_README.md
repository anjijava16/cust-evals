# Claude (Anthropic): Advanced LLM-as-Judge Evaluation

**Type**: LLM API + Evaluation Capability | **License**: Proprietary (API) | **Year**: 2023

---

## Quick Overview

Claude by Anthropic is a **state-of-the-art LLM** that excels as an evaluator. With advanced reasoning, long context windows (200K tokens), and strong instruction-following, Claude is increasingly used as an LLM-as-judge for evaluating other AI systems.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | LLM-as-Judge, Custom Evaluation |
| **Setup Time** | ⚡ 2 minutes |
| **Learning Curve** | Easy (if familiar with LLMs) |
| **Dependencies** | Anthropic API key only |
| **Cost** | Pay-per-token (competitive) |
| **Best For** | Complex reasoning, nuanced evaluation |

---

## Key Strengths

### ✅ Advantages

1. **Superior Reasoning**
   - Strong analytical capabilities
   - Nuanced judgment
   - Consistent evaluation criteria
   - Excellent for complex tasks

2. **Long Context Window**
   - Claude 3/3.5: 200K tokens
   - Evaluate entire conversations
   - Multi-document analysis
   - Long-form content assessment

3. **Constitutional AI**
   - Built-in ethical guidelines
   - Reduced bias in evaluation
   - Consistent value alignment
   - Transparent reasoning

4. **High Reliability**
   - Low hallucination rate
   - Consistent scoring
   - Predictable behavior
   - Strong instruction following

5. **Maximum Flexibility**
   - Custom evaluation criteria
   - Any scoring rubric
   - Domain-specific evaluation
   - Adapt to any use case

6. **Fast Iteration**
   - No training required
   - Instant evaluation
   - Easy prompt modification
   - Rapid experimentation

### ⚠️ Limitations

1. **API Dependency**
   - Requires internet connection
   - Subject to API availability
   - Rate limits apply
   - External service dependency

2. **Cost Scaling**
   - Expensive at high volumes
   - Long evaluations = more tokens
   - Cost grows with complexity
   - Not free like OSS frameworks

3. **No Built-in Framework**
   - No evaluation library
   - Manual prompt engineering
   - DIY result aggregation
   - No dashboards or UI

4. **Latency**
   - Network round-trip time
   - Slower than code-based metrics
   - Not ideal for real-time needs
   - Batch evaluation better

5. **Prompt Engineering Required**
   - Need to craft good prompts
   - Inconsistent prompts = inconsistent results
   - Requires iteration
   - Domain expertise helpful

---

## vs Other Frameworks

### vs Custom-Evals
| Aspect | Claude API | Custom-Evals |
|--------|------------|--------------|
| **Framework** | None (just API) | Complete library |
| **LLM Choice** | Claude only | Any LLM |
| **Flexibility** | Maximum | High |
| **Ready to Use** | Need prompts | Built-in evaluators |
| **Cost** | Per token | Framework free + LLM |

**Choose Claude API if**: You want maximum control and custom criteria
**Choose Custom-Evals if**: You want ready-made evaluators

---

### vs OpenAI GPT-4
| Aspect | Claude | GPT-4 |
|--------|--------|-------|
| **Context Window** | 200K tokens | 128K tokens |
| **Reasoning** | Excellent | Excellent |
| **Cost (Input)** | $3/1M tokens | $2.50/1M tokens |
| **Cost (Output)** | $15/1M tokens | $10/1M tokens |
| **Bias** | Constitutional AI | Standard |
| **Consistency** | Very high | High |

**Choose Claude if**: Long context, ethical evaluation, nuanced reasoning
**Choose GPT-4 if**: Lower cost, function calling, tool use

---

### vs RAGAS (LLM Evaluators)
| Aspect | Claude API | RAGAS |
|--------|------------|-------|
| **Framework** | None | Complete |
| **RAG Focus** | General | Specialized |
| **Customization** | Unlimited | Template-based |
| **Setup** | Minimal | Moderate |
| **Cost** | Higher | Lower (uses cheaper models) |

**Choose Claude API if**: Need custom evaluation beyond RAG
**Choose RAGAS if**: Standard RAG evaluation is sufficient

---

### vs DeepEval (LLM Judges)
| Aspect | Claude API | DeepEval |
|--------|------------|----------|
| **Framework** | None | Complete |
| **Test Integration** | Manual | Pytest |
| **Evaluators** | Custom | Built-in |
| **Flexibility** | Maximum | High |
| **Learning Curve** | Low | Moderate |

**Choose Claude API if**: Want DIY approach with best reasoning
**Choose DeepEval if**: Want framework with test integration

---

## When to Choose Claude

### ✅ Perfect For

1. **Complex Evaluation Criteria**
   - Nuanced judgment required
   - Domain-specific evaluation
   - Multi-dimensional scoring
   - Subjective quality assessment

2. **Long-Form Content**
   - Evaluate entire documents
   - Multi-turn conversations
   - Book chapters or articles
   - Comprehensive context needed

3. **Custom Use Cases**
   - Novel evaluation scenarios
   - Industry-specific metrics
   - Research experiments
   - No existing framework fits

4. **High-Stakes Evaluation**
   - Critical decision-making
   - Need explanation of scores
   - Audit trail important
   - Consistency crucial

5. **Ethical Evaluation**
   - Safety assessment
   - Bias detection
   - Harmful content detection
   - Value alignment checking

6. **Rapid Prototyping**
   - Quick experimentation
   - No framework setup
   - Iterate on criteria fast
   - Test evaluation approach

### ❌ Not Ideal For

1. **High-Volume Evaluation**
   - Millions of evaluations
   - Cost prohibitive
   - Latency concerns
   - Better to use code metrics

2. **Real-Time Evaluation**
   - Need instant feedback
   - Sub-second latency required
   - Production API calls
   - Use code-based metrics

3. **Budget Constraints**
   - Limited budget
   - Cost-per-eval matters
   - Use cheaper models
   - Or code-based metrics

4. **Offline/Air-Gapped**
   - No internet access
   - Security restrictions
   - Can't use external APIs
   - Use local models

---

## Pricing

### Claude API Pricing (2024)

#### Claude 3.5 Sonnet (Recommended for Evals)
| Token Type | Cost |
|------------|------|
| **Input** | $3 per 1M tokens |
| **Output** | $15 per 1M tokens |
| **Cache Write** | $3.75 per 1M tokens |
| **Cache Read** | $0.30 per 1M tokens |

#### Claude 3 Haiku (Budget Option)
| Token Type | Cost |
|------------|------|
| **Input** | $0.25 per 1M tokens |
| **Output** | $1.25 per 1M tokens |

#### Claude 3 Opus (Highest Quality)
| Token Type | Cost |
|------------|------|
| **Input** | $15 per 1M tokens |
| **Output** | $75 per 1M tokens |

### Cost Calculator

**Typical evaluation**: 500 input tokens + 100 output tokens

| Model | Cost/Eval | 1K Evals | 10K Evals | 100K Evals |
|-------|-----------|----------|-----------|------------|
| **Haiku** | $0.0002 | $0.20 | $2 | $20 |
| **Sonnet** | $0.003 | $3 | $30 | $300 |
| **Opus** | $0.015 | $15 | $150 | $1,500 |

### Cost Optimization Strategies

1. **Use Prompt Caching**: 10x cheaper for repeated context
2. **Batch Evaluations**: Fewer API calls
3. **Use Haiku**: For simpler evaluations
4. **Filter First**: Use code metrics to filter, LLM for edge cases
5. **Sample**: Evaluate subset, not everything

---

## Quick Start

### Installation

```bash
# Install Anthropic SDK
pip install anthropic
```

### Basic Evaluation

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

def evaluate_response(query: str, response: str) -> dict:
    """Evaluate a response using Claude as judge."""

    prompt = f"""You are an expert evaluator. Assess the following response.

Query: {query}
Response: {response}

Evaluate on these criteria:
1. Accuracy: Is the response factually correct?
2. Relevance: Does it answer the query?
3. Clarity: Is it clear and well-written?
4. Completeness: Is it thorough enough?

Provide:
- Score for each criterion (1-5)
- Overall score (1-5)
- Brief explanation

Format as JSON:
{{
    "accuracy": 5,
    "relevance": 5,
    "clarity": 4,
    "completeness": 5,
    "overall": 5,
    "explanation": "..."
}}"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text

# Use it
result = evaluate_response(
    query="What is the capital of France?",
    response="Paris is the capital of France."
)
print(result)
```

### Structured Output Evaluation

```python
import json
from anthropic import Anthropic

client = Anthropic()

def evaluate_with_rubric(input_text: str, output_text: str, rubric: dict) -> dict:
    """Evaluate using a custom rubric."""

    criteria_text = "\n".join([
        f"- {name}: {desc}"
        for name, desc in rubric.items()
    ])

    prompt = f"""Evaluate the following output based on these criteria:

{criteria_text}

Input: {input_text}
Output: {output_text}

Rate each criterion on a scale of 1-5.
Provide JSON with scores and explanation.

{{
    "scores": {{"criterion1": 5, "criterion2": 4, ...}},
    "overall": 4.5,
    "explanation": "..."
}}"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse JSON from response
    response_text = message.content[0].text
    # Extract JSON (handle markdown code blocks)
    if "```json" in response_text:
        json_str = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        json_str = response_text.split("```")[1].split("```")[0]
    else:
        json_str = response_text

    return json.loads(json_str.strip())

# Custom rubric
rubric = {
    "accuracy": "Response is factually correct",
    "relevance": "Response addresses the input directly",
    "helpfulness": "Response provides useful information",
    "safety": "Response is safe and appropriate"
}

result = evaluate_with_rubric(
    input_text="How do I make a cake?",
    output_text="Mix flour, eggs, sugar, and bake at 350F for 30 minutes.",
    rubric=rubric
)

print(f"Overall: {result['overall']}")
print(f"Scores: {result['scores']}")
```

### Batch Evaluation

```python
from typing import List, Dict
import asyncio
from anthropic import AsyncAnthropic

async def evaluate_batch(
    test_cases: List[Dict[str, str]],
    client: AsyncAnthropic
) -> List[dict]:
    """Evaluate multiple cases in parallel."""

    async def evaluate_one(case: dict) -> dict:
        prompt = f"""Evaluate this response:
Query: {case['query']}
Response: {case['response']}

Rate 1-5 for relevance and accuracy.
Return JSON: {{"relevance": X, "accuracy": Y}}"""

        message = await client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=256,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(message.content[0].text)

    # Run all evaluations concurrently
    tasks = [evaluate_one(case) for case in test_cases]
    results = await asyncio.gather(*tasks)

    return results

# Use it
async def main():
    client = AsyncAnthropic()

    test_cases = [
        {"query": "Capital of France?", "response": "Paris"},
        {"query": "Capital of Spain?", "response": "Madrid"},
        {"query": "Capital of Italy?", "response": "Rome"},
    ]

    results = await evaluate_batch(test_cases, client)

    for case, result in zip(test_cases, results):
        print(f"{case['query']}: {result}")

asyncio.run(main())
```

### With Prompt Caching (Cost Optimization)

```python
# Use prompt caching for repeated context
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert evaluator...",
        },
        {
            "type": "text",
            "text": f"Here is the evaluation rubric:\n{long_rubric}",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": f"Evaluate: {case}"}
    ]
)

# Subsequent calls with same system context:
# - First call: Normal price
# - Next calls (within 5 min): 90% discount on cached tokens!
```

---

## High-Level Architecture

### Overview

Claude-as-Judge operates as an LLM-powered evaluation system where Claude itself serves as the evaluator. Unlike traditional evaluation frameworks with built-in metrics, Claude provides a flexible API-based approach where evaluation logic is embedded in prompts.

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Your Evaluation System                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Evaluation Orchestrator                     │   │
│  │  • Test case management                                  │   │
│  │  • Prompt generation                                     │   │
│  │  • Result aggregation                                    │   │
│  │  • Error handling & retries                              │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Evaluation Data Preparation                    │   │
│  │  • Input: Questions/Prompts                              │   │
│  │  • Output: AI responses to evaluate                      │   │
│  │  • Context: Supporting documents (optional)              │   │
│  │  • Rubric: Evaluation criteria                           │   │
│  │  • Ground Truth: Reference answers (optional)            │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │                                        │
└─────────────────────────┼────────────────────────────────────────┘
                          │ HTTPS
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Anthropic API                                 │
│                    (api.anthropic.com)                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                API Gateway                               │   │
│  │  • Authentication (API key validation)                   │   │
│  │  • Rate limiting (tier-based)                            │   │
│  │  • Request routing                                       │   │
│  │  • Load balancing                                        │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Claude Model Inference                      │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  Model Selection                                   │  │   │
│  │  │  • Claude 3.5 Sonnet (recommended for evals)       │  │   │
│  │  │  • Claude 3 Opus (highest quality)                 │  │   │
│  │  │  • Claude 3 Haiku (cost-effective)                 │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  Prompt Processing                                 │  │   │
│  │  │  • System prompt interpretation                    │  │   │
│  │  │  • Context window management (200K tokens)         │  │   │
│  │  │  • Prompt caching (for repeated contexts)          │  │   │
│  │  │  • Constitutional AI filters                       │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  Inference Engine                                  │  │   │
│  │  │  • Token generation                                │  │   │
│  │  │  • Reasoning & analysis                            │  │   │
│  │  │  • Structured output generation                    │  │   │
│  │  │  • JSON formatting                                 │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Response Processing                         │   │
│  │  • Token counting (prompt + completion)                 │   │
│  │  • Cost calculation                                      │   │
│  │  • Response formatting                                   │   │
│  │  • Streaming support (optional)                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────┬────────────────────────────────────────┘
                          │ HTTPS Response
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Your Evaluation System                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Response Parsing & Validation               │   │
│  │  • JSON extraction                                       │   │
│  │  • Score validation (check ranges)                       │   │
│  │  • Error handling (malformed responses)                  │   │
│  │  • Retry logic (if needed)                               │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Results Storage & Analysis                  │   │
│  │  • Individual scores per test case                       │   │
│  │  • Aggregate statistics                                  │   │
│  │  • Explanations & reasoning                              │   │
│  │  • Performance metrics (latency, cost)                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Evaluation Orchestrator

**Purpose**: Manages the evaluation workflow

**Responsibilities**:
- Load and prepare test cases
- Generate evaluation prompts
- Make API calls to Claude
- Handle rate limiting and retries
- Aggregate results

**Implementation**:
```python
class ClaudeEvaluator:
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def evaluate_batch(self, test_cases: List[dict], rubric: dict) -> List[dict]:
        results = []
        for case in test_cases:
            result = self.evaluate_single(case, rubric)
            results.append(result)
        return results
```

#### 2. Prompt Engineering Layer

**Purpose**: Craft effective evaluation prompts

**Key Components**:
- **System Prompts**: Define Claude's role as evaluator
- **Evaluation Criteria**: Clear, measurable criteria
- **Output Format**: Structured JSON for easy parsing
- **Few-Shot Examples**: Optional examples for consistency

**Pattern**:
```python
def create_evaluation_prompt(input: str, output: str, criteria: dict) -> str:
    return f"""You are an expert evaluator. Assess the following AI response.

INPUT: {input}
OUTPUT: {output}

EVALUATION CRITERIA:
{format_criteria(criteria)}

Provide scores (1-5) and explanation in JSON format:
{{
    "scores": {{"criterion1": X, "criterion2": Y, ...}},
    "overall": X.X,
    "explanation": "detailed reasoning..."
}}"""
```

#### 3. Claude API Client

**Purpose**: Interface with Anthropic's API

**Features**:
- **Authentication**: API key management
- **Model Selection**: Choose appropriate Claude version
- **Configuration**: Temperature, max_tokens, etc.
- **Streaming**: Real-time response streaming (optional)
- **Caching**: Prompt caching for cost optimization

**SDK Integration**:
```python
import anthropic

client = anthropic.Anthropic(api_key="your-key")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    temperature=0,  # Deterministic for evaluation
    messages=[{"role": "user", "content": evaluation_prompt}]
)
```

#### 4. Response Parser

**Purpose**: Extract and validate evaluation results

**Functionality**:
- **JSON Extraction**: Handle markdown code blocks
- **Score Validation**: Ensure scores are in valid range
- **Error Detection**: Catch malformed responses
- **Fallback Logic**: Retry or use default values

**Implementation**:
```python
def parse_evaluation_response(response_text: str) -> dict:
    # Extract JSON from potential markdown formatting
    if "```json" in response_text:
        json_str = response_text.split("```json")[1].split("```")[0]
    else:
        json_str = response_text

    result = json.loads(json_str.strip())

    # Validate scores
    for key, value in result.get("scores", {}).items():
        if not 1 <= value <= 5:
            raise ValueError(f"Score {key}={value} out of range")

    return result
```

### Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Evaluation Data Flow                        │
└─────────────────────────────────────────────────────────────┘

1. PREPARATION PHASE
   ┌──────────────────────────────────────────┐
   │ Test Cases                               │
   │ • Questions                              │
   │ • AI outputs to evaluate                 │
   │ • Context documents (optional)           │
   │ • Ground truth (optional)                │
   └──────────────────┬───────────────────────┘
                      │
                      ▼
2. PROMPT CONSTRUCTION
   ┌──────────────────────────────────────────┐
   │ Evaluation Prompt                        │
   │ • System: Role definition                │
   │ • Criteria: What to measure              │
   │ • Format: JSON structure                 │
   │ • Examples: Few-shot (optional)          │
   └──────────────────┬───────────────────────┘
                      │
                      ▼
3. API REQUEST
   ┌──────────────────────────────────────────┐
   │ Claude API Call                          │
   │ • Model: claude-3-5-sonnet-20241022      │
   │ • Temperature: 0 (deterministic)         │
   │ • Max tokens: 2048                       │
   │ • Messages: [evaluation prompt]          │
   └──────────────────┬───────────────────────┘
                      │
                      ▼
4. INFERENCE
   ┌──────────────────────────────────────────┐
   │ Claude Processing                        │
   │ • Analyze input & output                 │
   │ • Apply evaluation criteria              │
   │ • Generate reasoning                     │
   │ • Format as JSON                         │
   └──────────────────┬───────────────────────┘
                      │
                      ▼
5. RESPONSE PARSING
   ┌──────────────────────────────────────────┐
   │ Extract & Validate                       │
   │ • Parse JSON from response               │
   │ • Validate score ranges                  │
   │ • Extract explanations                   │
   │ • Calculate tokens & cost                │
   └──────────────────┬───────────────────────┘
                      │
                      ▼
6. AGGREGATION
   ┌──────────────────────────────────────────┐
   │ Results Analysis                         │
   │ • Per-case scores                        │
   │ • Aggregate statistics (mean, median)    │
   │ • Distribution analysis                  │
   │ • Cost & latency tracking                │
   └──────────────────────────────────────────┘
```

### Evaluation Patterns

#### 1. Single-Dimension Scoring
```python
# Simple yes/no or 1-5 scoring
"Is this response accurate? Answer: Yes/No"
"Rate this response 1-5 for relevance"
```

#### 2. Multi-Dimension Scoring
```python
# Multiple criteria evaluated together
"Evaluate on: accuracy, relevance, clarity, safety"
```

#### 3. Comparative Evaluation
```python
# Compare two outputs
"Which response is better? A or B? Explain why."
```

#### 4. Chain-of-Thought Evaluation
```python
# Get reasoning before score
"Think step-by-step about this response's quality.
Then provide a score."
```

#### 5. Few-Shot Evaluation
```python
# Provide examples
"Here are examples of good responses: ...
Now evaluate this one: ..."
```

### Integration Patterns

#### Pattern 1: Direct API Integration
```python
# Simplest approach - direct API calls
import anthropic

client = anthropic.Anthropic()

def evaluate(input_text, output_text):
    prompt = create_evaluation_prompt(input_text, output_text)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return parse_response(response)
```

#### Pattern 2: Async Batch Evaluation
```python
# Efficient parallel evaluation
import asyncio
from anthropic import AsyncAnthropic

async def evaluate_batch(test_cases):
    client = AsyncAnthropic()
    tasks = [evaluate_single(case, client) for case in test_cases]
    results = await asyncio.gather(*tasks)
    return results
```

#### Pattern 3: Framework Integration
```python
# Integrate with evaluation frameworks
from custom.evals import BaseEvaluator

class ClaudeEvaluator(BaseEvaluator):
    def evaluate(self, data: dict) -> dict:
        # Use Claude as judge within framework
        response = self.client.messages.create(...)
        return parse_response(response)
```

#### Pattern 4: Caching for Cost Optimization
```python
# Use prompt caching for repeated contexts
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert evaluator...",
        },
        {
            "type": "text",
            "text": f"Evaluation rubric:\n{rubric}",
            "cache_control": {"type": "ephemeral"}  # Cache this
        }
    ],
    messages=[{"role": "user", "content": f"Evaluate: {case}"}]
)
# Subsequent calls within 5 min get 90% discount on cached tokens
```

### Best Practices

1. **Clear Criteria**: Define exactly what you're measuring
2. **Consistent Format**: Use same prompt structure
3. **Temperature 0**: For consistency in evaluation
4. **JSON Output**: Easy to parse and aggregate
5. **Error Handling**: Catch malformed responses
6. **Prompt Versioning**: Track prompt changes
7. **Validation**: Check scores are in expected range
8. **Cost Tracking**: Monitor token usage and costs
9. **Batching**: Use async for parallel evaluation
10. **Caching**: Leverage prompt caching for repeated contexts

---

## Advanced Patterns

### Rubric-Based Evaluation

```python
class ClaudeEvaluator:
    def __init__(self, api_key: str, rubric: dict):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.rubric = rubric

    def create_prompt(self, input_text: str, output_text: str) -> str:
        criteria = "\n".join([
            f"{i+1}. {name}: {desc} (1-5 scale)"
            for i, (name, desc) in enumerate(self.rubric.items())
        ])

        return f"""Evaluate this AI response using the following rubric:

{criteria}

Input: {input_text}
Output: {output_text}

Provide scores and explanation in JSON format:
{{
    "scores": {{{", ".join([f'"{k}": X' for k in self.rubric.keys()])}}},
    "overall": X.X,
    "explanation": "..."
}}"""

    def evaluate(self, input_text: str, output_text: str) -> dict:
        prompt = self.create_prompt(input_text, output_text)

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        return self._parse_response(message.content[0].text)

    def _parse_response(self, text: str) -> dict:
        # Extract and parse JSON
        if "```json" in text:
            json_str = text.split("```json")[1].split("```")[0]
        else:
            json_str = text

        return json.loads(json_str.strip())

# Usage
evaluator = ClaudeEvaluator(
    api_key="your-key",
    rubric={
        "accuracy": "Factually correct information",
        "relevance": "Directly answers the question",
        "clarity": "Clear and easy to understand",
        "completeness": "Thorough and comprehensive",
        "safety": "Safe and appropriate content"
    }
)

result = evaluator.evaluate(
    input_text="Explain quantum computing",
    output_text="Quantum computing uses qubits..."
)
```

### Comparative Evaluation

```python
def compare_responses(query: str, response_a: str, response_b: str) -> dict:
    """Compare two responses and pick the better one."""

    prompt = f"""Compare these two responses to the same query:

Query: {query}

Response A: {response_a}

Response B: {response_b}

Which response is better? Consider:
- Accuracy
- Relevance
- Clarity
- Completeness

Provide:
1. Winner (A or B)
2. Confidence (1-5)
3. Reasoning

JSON format:
{{
    "winner": "A",
    "confidence": 5,
    "reasoning": "..."
}}"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(message.content[0].text)
```

---

## Integration with Evaluation Frameworks

### With Custom-Evals

```python
from custom.evals import BaseEvaluator
from anthropic import Anthropic

class ClaudeAsJudge(BaseEvaluator):
    """Use Claude as evaluator in Custom-Evals framework."""

    def __init__(self, api_key: str, criteria: str):
        self.client = Anthropic(api_key=api_key)
        self.criteria = criteria

    def evaluate(self, data: dict) -> dict:
        prompt = f"""Evaluate based on: {self.criteria}

Input: {data.get('input', '')}
Output: {data['output']}

Rate 1-5 and explain. JSON format:
{{"score": X, "reasoning": "..."}}"""

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        result = json.loads(message.content[0].text)

        return {
            "score": result["score"],
            "label": "excellent" if result["score"] >= 4 else "good" if result["score"] >= 3 else "poor",
            "reason": result["reasoning"]
        }

# Use in Custom-Evals
evaluator = ClaudeAsJudge(
    api_key="your-key",
    criteria="Response is accurate and helpful"
)

score = evaluator.evaluate({
    "input": "What is AI?",
    "output": "AI is artificial intelligence..."
})
```

---

## Comparison Summary

### Unique Advantages
1. 🧠 Superior reasoning and judgment
2. 📚 200K token context window
3. 🎯 Maximum flexibility for custom criteria
4. ⚖️ Constitutional AI for ethical evaluation
5. 🔒 High consistency and reliability
6. ⚡ Fast to get started

### Trade-offs
1. Higher cost at scale
2. API dependency
3. No built-in framework
4. Manual prompt engineering
5. Latency considerations

---

## Resources

### Documentation
- **Official Docs**: https://docs.anthropic.com/
- **API Reference**: https://docs.anthropic.com/en/api/
- **Prompt Engineering**: https://docs.anthropic.com/en/docs/prompt-engineering
- **Prompt Library**: https://docs.anthropic.com/en/prompt-library/

### Research Papers
- **Constitutional AI**: https://arxiv.org/abs/2212.08073
- **Claude 3 Model Card**: https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf
- **Evaluating AI Systems**: https://www.anthropic.com/research

### Tools & SDKs
- **Python SDK**: https://github.com/anthropics/anthropic-sdk-python
- **TypeScript SDK**: https://github.com/anthropics/anthropic-sdk-typescript
- **Claude Console**: https://console.anthropic.com/

### Community
- **Support**: support@anthropic.com
- **Discord**: https://discord.gg/anthropic
- **Newsletter**: https://www.anthropic.com/newsletter

---

## Verdict

**Claude is the best choice for teams needing maximum flexibility, complex reasoning, and custom evaluation criteria without framework constraints.**

**Rating**: ⭐⭐⭐⭐½ (4.5/5 for flexibility)

### Choose Claude if you value:
- ✅ Superior reasoning ability
- ✅ Long context windows
- ✅ Custom evaluation criteria
- ✅ Ethical AI evaluation
- ✅ Fast experimentation
- ✅ No framework overhead

### Choose alternatives if you need:
- ❌ Built-in evaluation library → Custom-Evals, RAGAS
- ❌ Low-cost high-volume → Code-based metrics
- ❌ No API dependency → Local models
- ❌ Framework integration → LangSmith, DeepEval

---

**Next**: [Compare All Frameworks](Compare_All_Eval_Frameworks.md) | [Try Custom-Evals](01_Custom_Evals.md)
