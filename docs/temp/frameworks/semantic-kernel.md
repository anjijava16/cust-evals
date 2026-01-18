# Semantic Kernel (Microsoft) with Custom-Evals

## Overview

Semantic Kernel is Microsoft's SDK for integrating AI into applications with a powerful plugin system and planner architecture. It provides a kernel-based framework for orchestrating AI capabilities with extensive plugin support, memory management, and multi-step planning.

**Key Features**:
- **Kernel Architecture**: Centralized AI orchestration with kernel-based design
- **Plugin System**: Extensible plugins with `@kernel_function` decorator
- **AI Services**: Support for OpenAI, Azure OpenAI, and other providers
- **Planners**: Automatic multi-step workflow planning (SequentialPlanner, ActionPlanner)
- **Memory Management**: Built-in semantic memory and context management
- **Custom-Evals Integration**: Full support for Phoenix custom-evals evaluation framework

**Use Cases**:
- Enterprise AI applications
- Multi-step automated workflows
- Knowledge management systems
- Intelligent automation with planning
- Microsoft ecosystem AI integration

---

## Installation

### Prerequisites
- Python 3.10 or higher
- OpenAI API key (or Azure OpenAI)
- Semantic Kernel library

### Install Dependencies

```bash
pip install semantic-kernel
```

### Environment Setup

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### Verify Installation

```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

kernel = sk.Kernel()
print("✅ Semantic Kernel installed successfully")
```

---

## Quick Start

### Simple Agent Example

```python
import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

# Create kernel
kernel = sk.Kernel()

# Add AI service
kernel.add_service(
    OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

# Create chat function
async def run_agent():
    chat_function = kernel.add_function(
        prompt="{{$input}}\n\nYou are a helpful assistant.",
        function_name="chat",
        plugin_name="ChatPlugin"
    )
    
    result = await kernel.invoke(chat_function, input="What is artificial intelligence?")
    print(result)

# Run
import asyncio
asyncio.run(run_agent())
```

### Agent with Plugins

```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

class WeatherPlugin:
    """Plugin for weather information."""

    @sk.kernel_function(
        name="get_weather",
        description="Get current weather for a location"
    )
    def get_weather(self, location: str) -> str:
        """Get weather for a location."""
        weather_data = {
            "San Francisco": "Sunny, 72°F",
            "New York": "Cloudy, 65°F",
            "London": "Rainy, 55°F"
        }
        return weather_data.get(location, f"Weather data not available for {location}")

class MathPlugin:
    """Plugin for mathematical operations."""

    @sk.kernel_function(
        name="calculate",
        description="Calculate mathematical expressions"
    )
    def calculate(self, expression: str) -> str:
        """Calculate expression."""
        try:
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error: {str(e)}"

# Create kernel with plugins
kernel = sk.Kernel()

# Add AI service
kernel.add_service(
    OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

# Add plugins
kernel.add_plugin(WeatherPlugin(), "Weather")
kernel.add_plugin(MathPlugin(), "Math")

# Run agent
async def run_with_plugins():
    chat_function = kernel.add_function(
        prompt="{{$input}}\n\nYou are a helpful assistant with access to tools.",
        function_name="chat",
        plugin_name="ChatPlugin"
    )
    
    result = await kernel.invoke(
        chat_function,
        input="What's the weather in Tokyo and calculate 25 * 4?"
    )
    print(result)

asyncio.run(run_with_plugins())
```

---

## Architecture

### Core Components

**1. Kernel**
- Central orchestration component
- Manages AI services, plugins, and memory
- Coordinates function execution

**2. Plugins**
- Collections of related functions
- Decorated with `@kernel_function`
- Automatically registered with kernel

**3. AI Services**
- Connectors to AI providers (OpenAI, Azure OpenAI)
- Configurable model selection
- Support for multiple concurrent services

**4. Planners**
- Automatic workflow planning
- SequentialPlanner for multi-step tasks
- ActionPlanner for single-step optimization

**5. Memory**
- Semantic memory for context storage
- Vector-based similarity search
- Persistent conversation history

### Plugin Creation Pattern

```python
import semantic_kernel as sk

class MyPlugin:
    """Custom plugin for specific functionality."""

    @sk.kernel_function(
        name="function_name",
        description="What this function does (used by AI to decide when to call it)"
    )
    def my_function(self, param1: str, param2: str = "default") -> str:
        """Function implementation.
        
        Args:
            param1: Description of first parameter
            param2: Description of second parameter (optional)
        
        Returns:
            Result description
        """
        # Implement functionality
        return f"Processed {param1} with {param2}"

# Use in kernel
kernel.add_plugin(MyPlugin(), "MyPlugin")
```

---

## Multi-Agent Systems

### Multi-Agent with Planner

```python
from semantic_kernel.planning import SequentialPlanner

class SemanticKernelMultiAgent:
    """Multi-agent system with planner."""

    def __init__(self):
        # Create kernel
        self.kernel = sk.Kernel()

        # Add AI service
        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        # Add plugins
        self.kernel.add_plugin(WeatherPlugin(), "Weather")
        self.kernel.add_plugin(KnowledgePlugin(), "Knowledge")
        self.kernel.add_plugin(MathPlugin(), "Math")

        # Create planner
        self.planner = SequentialPlanner(self.kernel)

    async def run_workflow(self, goal: str):
        """Run multi-step workflow with planner."""
        # Create plan
        plan = await self.planner.create_plan(goal)

        # Execute plan
        result = await plan.invoke(self.kernel)

        return {
            "goal": goal,
            "plan_steps": len(plan._steps) if hasattr(plan, '_steps') else 0,
            "final_output": str(result),
            "planner": "SequentialPlanner"
        }

# Usage
system = SemanticKernelMultiAgent()
result = asyncio.run(system.run_workflow(
    "Get the weather in San Francisco and explain Semantic Kernel"
))
print(result["final_output"])
```

---

## Custom-Evals Integration

### Complete Evaluation System

```python
import asyncio
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM

class EvaluatedSemanticKernelAgent:
    """Semantic Kernel agent with evaluation."""

    def __init__(self, model: str = "gpt-4o-mini"):
        # Create kernel
        self.kernel = sk.Kernel()

        # Add AI service
        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id=model,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        # Add plugins
        self.kernel.add_plugin(WeatherPlugin(), "Weather")
        self.kernel.add_plugin(MathPlugin(), "Math")

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    async def run_and_evaluate(self, query: str, expected: str = None):
        """Run agent and evaluate response."""
        # Create chat function
        chat_function = self.kernel.add_function(
            prompt="{{$input}}\n\nYou are a helpful assistant with access to tools.",
            function_name="chat",
            plugin_name="ChatPlugin"
        )

        # Run agent
        result = await self.kernel.invoke(chat_function, input=query)
        response = str(result)

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
agent = EvaluatedSemanticKernelAgent()
result = asyncio.run(agent.run_and_evaluate("What is machine learning?"))

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

### 1. Plugin Organization
**Group related functions into plugins**:
```python
# ✅ Good: Focused plugin
class WeatherPlugin:
    @sk.kernel_function(name="get_weather", description="Get weather")
    def get_weather(self, location: str) -> str:
        return self.fetch_weather(location)
    
    @sk.kernel_function(name="get_forecast", description="Get forecast")
    def get_forecast(self, location: str, days: int) -> str:
        return self.fetch_forecast(location, days)

# ❌ Bad: Unrelated functions in one plugin
class UtilityPlugin:
    @sk.kernel_function(name="get_weather", ...)
    def get_weather(self, location: str): ...
    
    @sk.kernel_function(name="send_email", ...)
    def send_email(self, to: str): ...  # Unrelated to weather
```

### 2. Function Descriptions
**Write clear, descriptive function descriptions**:
```python
# ✅ Good: Clear description
@sk.kernel_function(
    name="calculate",
    description="Calculate the result of a mathematical expression like '5 + 3' or '10 * 2'"
)
def calculate(self, expression: str) -> str:
    ...

# ❌ Bad: Vague description
@sk.kernel_function(name="calculate", description="Does math")
def calculate(self, expression: str) -> str:
    ...
```

### 3. Async/Await Usage
**Always use async/await with Semantic Kernel**:
```python
# ✅ Good: Async execution
async def run_agent():
    result = await kernel.invoke(function, input=query)
    return result

result = asyncio.run(run_agent())

# ❌ Bad: Attempting sync execution
result = kernel.invoke(function, input=query)  # Won't work correctly
```

### 4. Planner Usage
**Use planners for complex multi-step tasks**:
```python
from semantic_kernel.planning import SequentialPlanner

# Create planner
planner = SequentialPlanner(kernel)

# Let planner determine steps
goal = "Research AI trends, analyze the data, and create a summary report"
plan = await planner.create_plan(goal)
result = await plan.invoke(kernel)
```

### 5. Error Handling
**Implement error handling in plugin functions**:
```python
@sk.kernel_function(name="safe_calculate", description="Calculate safely")
def safe_calculate(self, expression: str) -> str:
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {str(e)}"
```

---

## Resources

### Official Documentation
- **Semantic Kernel**: https://learn.microsoft.com/en-us/semantic-kernel/
- **GitHub**: https://github.com/microsoft/semantic-kernel
- **Python Docs**: https://learn.microsoft.com/en-us/semantic-kernel/get-started/quick-start-guide?pivots=programming-language-python

### Example Files
- **Complete Example**: `examples/semantic_kernel_example.py` (19KB)
- **Test Suites**: 5 comprehensive tests covering all use cases
- **Custom-Evals Integration**: Full evaluation implementation

### Phoenix Custom-Evals
- **Evaluators**: CoherenceEvaluator, RelevanceEvaluator, CorrectnessEvaluator, ToxicityEvaluator
- **LLM Integration**: Support for OpenAI, Anthropic, and other providers

---

## Quick Reference

### Installation
```bash
pip install semantic-kernel
export OPENAI_API_KEY="your-openai-api-key"
```

### Basic Agent
```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

kernel = sk.Kernel()
kernel.add_service(OpenAIChatCompletion(service_id="chat", ai_model_id="gpt-4o-mini", api_key=api_key))

async def run():
    function = kernel.add_function(prompt="{{$input}}\n\nYou are helpful.", function_name="chat")
    result = await kernel.invoke(function, input="Your query")
    print(result)

asyncio.run(run())
```

### With Plugin
```python
class MyPlugin:
    @sk.kernel_function(name="my_func", description="Does something")
    def my_func(self, param: str) -> str:
        return f"Result for {param}"

kernel.add_plugin(MyPlugin(), "MyPlugin")
```

### With Planner
```python
from semantic_kernel.planning import SequentialPlanner

planner = SequentialPlanner(kernel)
plan = await planner.create_plan("Your multi-step goal")
result = await plan.invoke(kernel)
```

---

**Created**: 2026-01-17
**Status**: Production Ready
**Framework Version**: Latest
**Custom-Evals**: Fully Integrated
