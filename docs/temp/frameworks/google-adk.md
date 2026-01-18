# Google ADK with Custom-Evals

## Overview

Google ADK (Agent Development Kit) is Google's official Python framework for building AI agents with Gemini models. Available at https://github.com/google/adk-python, it provides a streamlined approach to creating intelligent agents with function calling, multi-agent orchestration, and state management capabilities.

**Key Features**:
- **Gemini Integration**: Native support for Gemini 1.5 Flash, Gemini 1.5 Pro, and other Google AI models
- **Function Tools**: Decorator-based tool creation with automatic schema generation
- **AgentRunner**: Centralized execution engine for running agents
- **Multi-Agent Support**: Coordinate multiple specialized agents in workflows
- **State Management**: Built-in conversation history and context tracking
- **Custom-Evals Integration**: Full support for Phoenix custom-evals evaluation framework

**Use Cases**:
- Google Cloud-based AI applications
- Multi-modal AI agents (text, images, audio)
- Enterprise knowledge management systems
- Automated research and analysis workflows
- Customer support automation

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Google API key with Gemini access
- OpenAI API key (for custom-evals)

### Install Dependencies

```bash
pip install google-adk
```

### Environment Setup

Set up your API keys:

```bash
export GOOGLE_API_KEY="your-google-api-key"

# For custom-evals (optional but recommended)
export OPENAI_API_KEY="your-openai-api-key"
```

### Verify Installation

```python
from google_adk import Agent, AgentRunner

# Test basic functionality
agent = Agent(
    name="test",
    model="gemini-1.5-flash",
    instructions="You are a test agent."
)

runner = AgentRunner(api_key="your-google-api-key")
print("✅ Google ADK installed successfully")
```

---

## Quick Start

### Simple Agent Example

```python
import os
from google_adk import Agent, AgentRunner

# Create agent
agent = Agent(
    name="assistant",
    model="gemini-1.5-flash",
    instructions="You are a helpful AI assistant."
)

# Create runner
runner = AgentRunner(api_key=os.getenv("GOOGLE_API_KEY"))

# Run agent
result = runner.run(agent=agent, input="What is artificial intelligence?")
print(result.output)
```

### Agent with Function Tools

```python
from google_adk import Agent, AgentRunner
from google_adk.tools import function_tool

# Define tools using decorator
@function_tool
def get_weather(location: str) -> str:
    """Get current weather for a location.

    Args:
        location: City name (e.g., 'San Francisco', 'New York')

    Returns:
        Weather information including temperature and conditions
    """
    weather_data = {
        "San Francisco": "Sunny, 72°F with light breeze",
        "New York": "Cloudy, 65°F with chance of rain",
        "London": "Foggy, 55°F"
    }
    return weather_data.get(location, f"Weather data not available for {location}")

@function_tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression.

    Args:
        expression: Mathematical expression (e.g., '25 * 4')

    Returns:
        Calculation result
    """
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Create agent with tools
agent = Agent(
    name="assistant",
    model="gemini-1.5-flash",
    instructions="You are a helpful assistant with access to tools.",
    tools=[get_weather, calculate]
)

# Run agent
runner = AgentRunner(api_key=os.getenv("GOOGLE_API_KEY"))
result = runner.run(agent=agent, input="What's the weather in Tokyo and calculate 25 * 8?")
print(result.output)
```

---

**Created**: 2026-01-17
**Status**: Production Ready
**Framework Version**: Latest (google-adk from GitHub)
**Custom-Evals**: Fully Integrated

_For complete documentation including Architecture, Multi-Agent Systems, Custom-Evals Integration, Testing Examples, Best Practices, Troubleshooting, and Resources, see the full example at `examples/google_adk_example.py`._
