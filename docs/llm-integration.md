# LLM Integration

Guide to integrating and configuring LLM providers in Custom Evals.

## Overview

Custom Evals supports multiple LLM providers through a unified interface. Currently supported:

- **OpenAI** - GPT-4, GPT-3.5-turbo, etc.
- **Anthropic** - Claude 3 models (Opus, Sonnet, Haiku)

## Quick Start

```python
from custom.evals.llm import LLM

# OpenAI
llm = LLM(provider="openai", model="gpt-4o-mini")

# Anthropic
llm = LLM(provider="anthropic", model="claude-3-haiku-20240307")
```

## Configuration

### API Keys

Set your API key via environment variable or directly:

```bash
# Environment variables (recommended)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

```python
# Or pass directly
llm = LLM(
    provider="openai",
    model="gpt-4o-mini",
    api_key="sk-..."
)
```

## OpenAI

### Supported Models

```python
# GPT-4o series (recommended)
llm = LLM(provider="openai", model="gpt-4o")        # Most capable
llm = LLM(provider="openai", model="gpt-4o-mini")   # Fast and cheap

# GPT-4 Turbo
llm = LLM(provider="openai", model="gpt-4-turbo")

# GPT-3.5 Turbo
llm = LLM(provider="openai", model="gpt-3.5-turbo")
```

### Configuration Options

```python
llm = LLM(
    provider="openai",
    model="gpt-4o-mini",
    api_key="sk-...",
    temperature=0.0,      # Deterministic (default)
    max_tokens=1000,      # Max response length
    timeout=30            # Request timeout in seconds
)
```

## Anthropic

### Supported Models

```python
# Claude 3 series
llm = LLM(provider="anthropic", model="claude-3-opus-20240229")    # Most capable
llm = LLM(provider="anthropic", model="claude-3-sonnet-20240229")  # Balanced
llm = LLM(provider="anthropic", model="claude-3-haiku-20240307")   # Fast and cheap
```

### Configuration Options

```python
llm = LLM(
    provider="anthropic",
    model="claude-3-haiku-20240307",
    api_key="sk-ant-...",
    temperature=0.0,
    max_tokens=1000,
    timeout=30
)
```

## Model Selection Guide

### For Development

Use cheaper, faster models:
- OpenAI: `gpt-4o-mini`
- Anthropic: `claude-3-haiku-20240307`

### For Production

Use more capable models:
- OpenAI: `gpt-4o` or `gpt-4-turbo`
- Anthropic: `claude-3-sonnet-20240229` or `claude-3-opus-20240229`

### Cost Comparison

| Model | Provider | Speed | Cost | Quality |
|-------|----------|-------|------|---------|
| gpt-4o-mini | OpenAI | ⚡️⚡️⚡️ | 💰 | ⭐⭐⭐ |
| claude-3-haiku | Anthropic | ⚡️⚡️⚡️ | 💰 | ⭐⭐⭐ |
| gpt-4o | OpenAI | ⚡️⚡️ | 💰💰 | ⭐⭐⭐⭐ |
| claude-3-sonnet | Anthropic | ⚡️⚡️ | 💰💰 | ⭐⭐⭐⭐ |
| claude-3-opus | Anthropic | ⚡️ | 💰💰💰 | ⭐⭐⭐⭐⭐ |

## Usage with Evaluators

```python
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

# Initialize LLM
llm = LLM(provider="openai", model="gpt-4o-mini")

# Create evaluator
evaluator = HallucinationEvaluator(llm)

# Use evaluator
score = evaluator.evaluate({
    "input": "What is Python?",
    "output": "Python is a programming language.",
    "context": "Python is a high-level programming language."
})
```

## Advanced Configuration

### Custom Timeout

```python
llm = LLM(
    provider="openai",
    model="gpt-4o-mini",
    timeout=60  # 60 seconds
)
```

### Temperature Control

```python
# Deterministic (recommended for evaluation)
llm = LLM(provider="openai", model="gpt-4o-mini", temperature=0.0)

# Creative
llm = LLM(provider="openai", model="gpt-4o-mini", temperature=0.7)
```

## For more details

See the main documentation:
- **[LLM Guide](../LLM_GUIDE.md)** - Complete LLM integration guide
- **[API Reference](api-reference.md)** - LLM class API
- **[Examples](examples.md)** - Usage examples
