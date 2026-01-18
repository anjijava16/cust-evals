# Microsoft Agent Framework with Custom-Evals

## Overview

Microsoft Agent Framework is Microsoft's production-ready framework for building enterprise AI agents. It provides robust agent configuration, runtime management, and tool integration with a focus on reliability, security, and scalability.

**Key Features**:
- **AgentConfig**: Structured agent configuration and management
- **AgentRuntime**: Production-grade execution environment
- **Tool System**: Extensible tool classes with JSON schema support
- **Multi-Agent Collaboration**: Orchestrate multiple specialized agents
- **State Management**: Built-in conversation and context tracking
- **Custom-Evals Integration**: Full support for Phoenix custom-evals evaluation framework

**Use Cases**:
- Enterprise AI assistants
- Customer service automation
- Data analysis and reporting
- Knowledge management systems
- Business process automation

---

## Installation

### Prerequisites
- Python 3.10 or higher
- OpenAI API key
- Microsoft Agent Framework library

### Install Dependencies

```bash
pip install microsoft-agents
```

### Environment Setup

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### Verify Installation

```python
from microsoft_agents import Agent, AgentConfig
from microsoft_agents.runtime import AgentRuntime

config = AgentConfig(name="test", instructions="Test agent", model="gpt-4o-mini")
agent = Agent(config=config)
print("✅ Microsoft Agent Framework installed successfully")
```

---

## Quick Start

### Simple Agent Example

```python
import os
from microsoft_agents import Agent, AgentConfig
from microsoft_agents.runtime import AgentRuntime

# Create agent config
config = AgentConfig(
    name="assistant",
    instructions="You are a helpful AI assistant.",
    model="gpt-4o-mini"
)

# Create agent
agent = Agent(config=config)

# Create runtime
runtime = AgentRuntime(api_key=os.getenv("OPENAI_API_KEY"))

# Run agent
result = runtime.run(agent=agent, input="What is artificial intelligence?")
print(result.output)
```

### Agent with Tools

```python
from microsoft_agents import Agent, AgentConfig, Tool

class WeatherTool(Tool):
    """Tool for weather information."""

    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get current weather for a location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name (e.g., 'San Francisco')"
                    }
                },
                "required": ["location"]
            }
        )

    def execute(self, location: str) -> str:
        """Execute weather lookup."""
        weather_data = {
            "San Francisco": "Sunny, 72°F",
            "New York": "Cloudy, 65°F",
            "London": "Rainy, 55°F"
        }
        return weather_data.get(location, f"Weather data not available for {location}")

# Create agent with tool
config = AgentConfig(
    name="assistant",
    instructions="You are a helpful assistant with access to tools.",
    model="gpt-4o-mini",
    tools=[WeatherTool()]
)

agent = Agent(config=config)
runtime = AgentRuntime(api_key=os.getenv("OPENAI_API_KEY"))

result = runtime.run(agent=agent, input="What's the weather in New York?")
print(result.output)
```

---

## Architecture

### Core Components

**1. AgentConfig**
- Structured agent configuration
- Defines name, instructions, model, and tools
- Immutable configuration object

**2. Agent**
- Main agent class created from config
- Manages execution and tool calling
- Maintains conversation state

**3. Tool**
- Base class for creating custom tools
- JSON schema definition for parameters
- `execute()` method for tool logic

**4. AgentRuntime**
- Execution environment for agents
- Manages API connections and authentication
- Handles request/response lifecycle

### Tool Creation Pattern

```python
class CustomTool(Tool):
    """Custom tool template."""

    def __init__(self):
        super().__init__(
            name="tool_name",
            description="What the tool does",
            parameters={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param1"]
            }
        )

    def execute(self, param1: str) -> str:
        """Execute tool logic."""
        # Implement tool functionality
        return f"Result for {param1}"
```

---

## Multi-Agent Systems

### Multi-Agent Collaboration Example

```python
class MultiAgentMicrosoftSystem:
    """Multi-agent collaboration system."""

    def __init__(self):
        # Create specialized agents
        research_config = AgentConfig(
            name="researcher",
            instructions="You are a research specialist. Gather comprehensive information.",
            model="gpt-4o-mini",
            tools=[SearchTool()]
        )
        self.research_agent = Agent(config=research_config)

        analysis_config = AgentConfig(
            name="analyst",
            instructions="You are an analysis expert. Extract key insights.",
            model="gpt-4o-mini"
        )
        self.analysis_agent = Agent(config=analysis_config)

        writer_config = AgentConfig(
            name="writer",
            instructions="You are a technical writer. Create clear summaries.",
            model="gpt-4o-mini"
        )
        self.writer_agent = Agent(config=writer_config)

        # Create runtime
        self.runtime = AgentRuntime(api_key=os.getenv("OPENAI_API_KEY"))

    def run_workflow(self, topic: str):
        """Run multi-agent workflow."""
        # Step 1: Research
        research_result = self.runtime.run(
            agent=self.research_agent,
            input=f"Research information about: {topic}"
        )

        # Step 2: Analysis
        analysis_result = self.runtime.run(
            agent=self.analysis_agent,
            input=f"Analyze this research: {research_result.output}"
        )

        # Step 3: Writing
        writing_result = self.runtime.run(
            agent=self.writer_agent,
            input=f"Create a summary about {topic} based on: {analysis_result.output}"
        )

        return {
            "research": research_result.output,
            "analysis": analysis_result.output,
            "final_output": writing_result.output
        }

# Usage
system = MultiAgentMicrosoftSystem()
result = system.run_workflow("Azure Cloud Services")
print(result["final_output"])
```

---

## Custom-Evals Integration

### Complete Evaluation System

```python
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM

class EvaluatedMicrosoftAgent:
    """Microsoft agent with evaluation capabilities."""

    def __init__(self):
        # Create agent
        config = AgentConfig(
            name="assistant",
            instructions="You are a helpful assistant.",
            model="gpt-4o-mini",
            tools=[WeatherTool(), SearchTool()]
        )
        self.agent = Agent(config=config)
        self.runtime = AgentRuntime(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run_and_evaluate(self, query: str, expected: str = None):
        """Run agent and evaluate response."""
        # Run agent
        result = self.runtime.run(agent=self.agent, input=query)
        response = result.output

        # Evaluate
        scores = {}
        for name, evaluator in self.evaluators.items():
            eval_input = {"input": query, "output": response}

            if name == "correctness" and expected:
                eval_input["expected"] = expected

            score = evaluator.evaluate(eval_input)
            scores[name] = score

        return {"response": response, "scores": scores}

# Usage
agent = EvaluatedMicrosoftAgent()
result = agent.run_and_evaluate("What is machine learning?")

print(f"Response: {result['response'][:200]}...\n")
print("Evaluation Scores:")
for metric, score in result['scores'].items():
    print(f"  {metric.capitalize()}: {score.label} ({score.score:.2f})")
```

### Quality Thresholds
- Coherence: ≥ 0.7
- Relevance: ≥ 0.7
- Correctness: ≥ 0.7
- Toxicity: ≤ 0.2

---

## Best Practices

### 1. Configuration Management
**Use immutable configuration objects**:
```python
# ✅ Good: Structured configuration
config = AgentConfig(
    name="assistant",
    instructions="Clear instructions",
    model="gpt-4o-mini",
    tools=[tool1, tool2]
)
agent = Agent(config=config)

# ❌ Bad: Ad-hoc configuration
agent = Agent(name="assistant", instructions="...", model="...", tools=[...])
```

### 2. Tool Design
**Keep tools focused and well-documented**:
```python
class WeatherTool(Tool):
    """Well-documented weather tool."""

    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get current weather for a specific location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name (e.g., 'San Francisco', 'New York')"
                    }
                },
                "required": ["location"]
            }
        )

    def execute(self, location: str) -> str:
        """Execute weather lookup with error handling."""
        try:
            return self.get_weather_data(location)
        except Exception as e:
            return f"Error: {str(e)}"
```

### 3. Error Handling
**Implement comprehensive error handling**:
```python
def run_agent_safely(runtime, agent, query):
    """Run agent with error handling."""
    try:
        result = runtime.run(agent=agent, input=query)
        return result.output
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
```

### 4. Multi-Agent Coordination
**Use clear agent roles and responsibilities**:
```python
# ✅ Good: Specialized agents
researcher = Agent(config=AgentConfig(
    name="researcher",
    instructions="You specialize in research. Gather factual information."
))

analyst = Agent(config=AgentConfig(
    name="analyst",
    instructions="You specialize in analysis. Extract insights from data."
))
```

---

## Resources

### Official Documentation
- **Microsoft Agent Framework**: Check Microsoft documentation for latest info
- **Azure AI**: https://azure.microsoft.com/en-us/solutions/ai/

### Example Files
- **Complete Example**: `examples/microsoft_agent_framework_example.py` (18KB)
- **Test Suites**: 5 comprehensive tests covering all use cases
- **Custom-Evals Integration**: Full evaluation implementation

### Phoenix Custom-Evals
- **Evaluators**: CoherenceEvaluator, RelevanceEvaluator, CorrectnessEvaluator, ToxicityEvaluator
- **LLM Integration**: Support for OpenAI, Anthropic, and other providers

---

## Quick Reference

### Installation
```bash
pip install microsoft-agents
export OPENAI_API_KEY="your-openai-api-key"
```

### Basic Agent
```python
from microsoft_agents import Agent, AgentConfig
from microsoft_agents.runtime import AgentRuntime

config = AgentConfig(name="assistant", instructions="You are helpful.", model="gpt-4o-mini")
agent = Agent(config=config)
runtime = AgentRuntime(api_key=os.getenv("OPENAI_API_KEY"))
result = runtime.run(agent=agent, input="Your query here")
```

### With Tool
```python
class MyTool(Tool):
    def __init__(self):
        super().__init__(name="my_tool", description="Tool description", parameters={...})

    def execute(self, param: str) -> str:
        return f"Result for {param}"

config = AgentConfig(name="assistant", model="gpt-4o-mini", tools=[MyTool()])
```

---

**Created**: 2026-01-17
**Status**: Production Ready
**Framework Version**: Latest
**Custom-Evals**: Fully Integrated
