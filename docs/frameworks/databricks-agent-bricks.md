# Databricks Agent Bricks SDK with Custom-Evals

## Overview

Databricks Agent Bricks SDK is an MLflow-integrated framework for building production AI agents on the Databricks platform. It provides seamless integration with Databricks services, automatic experiment tracking, and enterprise-grade agent management.

**Key Features**:
- **MLflow Integration**: Automatic experiment tracking and model logging
- **Agent Tracking**: Built-in tracking of agent executions and metrics
- **Tool System**: Function-based tool creation with decorators
- **Multi-Agent Workflows**: Data-focused multi-agent orchestration
- **Databricks Integration**: Native integration with Databricks services
- **Custom-Evals Integration**: Full support for Phoenix custom-evals evaluation framework

**Use Cases**:
- Data analysis and ML workflows on Databricks
- Automated data pipeline management
- ML model evaluation and monitoring
- Enterprise data agent systems
- Production AI applications with MLflow tracking

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Databricks account (optional for local development)
- OpenAI API key
- MLflow

### Install Dependencies

```bash
pip install databricks-agents mlflow
```

### Environment Setup

```bash
# For Databricks integration (optional)
export DATABRICKS_HOST="your-databricks-host"
export DATABRICKS_TOKEN="your-databricks-token"

# For OpenAI models
export OPENAI_API_KEY="your-openai-api-key"
```

### Verify Installation

```python
from databricks.agents import Agent, Tool
from databricks.agents.runtime import AgentRuntime
import mlflow

print("✅ Databricks Agent Bricks SDK installed successfully")
```

---

## Quick Start

### Simple Agent Example

```python
import os
from databricks.agents import Agent, Tool
from databricks.agents.runtime import AgentRuntime
import mlflow

# Set MLflow experiment
mlflow.set_experiment("my_agent_experiment")

# Define a tool
def get_weather(location: str) -> str:
    """Get current weather for a location."""
    weather_data = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Cloudy, 65°F",
        "London": "Rainy, 55°F"
    }
    return weather_data.get(location, f"Weather data not available for {location}")

# Create tool
weather_tool = Tool.from_function(get_weather)

# Create agent
agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant.",
    tools=[weather_tool],
    model="gpt-4o-mini"
)

# Create runtime
runtime = AgentRuntime()

# Run agent with MLflow tracking
with mlflow.start_run():
    result = runtime.run(agent=agent, input="What's the weather in New York?")
    mlflow.log_param("query", "What's the weather in New York?")
    mlflow.log_param("response", result.output)
    print(result.output)
```

### Agent with Multiple Tools

```python
def search_data(query: str) -> str:
    """Search data catalog for information."""
    data_catalog = {
        "databricks": "Databricks is a unified analytics platform.",
        "mlflow": "MLflow is an open-source platform for ML lifecycle.",
        "spark": "Apache Spark is a unified analytics engine."
    }
    query_lower = query.lower()
    for key, value in data_catalog.items():
        if key in query_lower:
            return value
    return f"No data found for: {query}"

def get_dataset_info(dataset_name: str) -> str:
    """Get information about a dataset."""
    datasets = {
        "sales": {"rows": 10000, "columns": 15, "size": "2.5GB"},
        "customers": {"rows": 5000, "columns": 10, "size": "1.2GB"}
    }
    info = datasets.get(dataset_name.lower())
    if info:
        return json.dumps(info)
    return f"Dataset {dataset_name} not found"

# Create agent with multiple tools
agent = Agent(
    name="data_assistant",
    instructions="You are a data analysis assistant.",
    tools=[
        Tool.from_function(search_data),
        Tool.from_function(get_dataset_info)
    ],
    model="gpt-4o-mini"
)

runtime = AgentRuntime()

with mlflow.start_run():
    result = runtime.run(
        agent=agent,
        input="Get info on sales dataset and explain Databricks"
    )
    mlflow.log_metric("tool_calls", len(result.tool_calls) if hasattr(result, 'tool_calls') else 0)
    print(result.output)
```

---

## Architecture

### Core Components

**1. Agent**
- Main agent class with MLflow integration
- Configures model, instructions, and tools
- Automatic tracking of executions

**2. Tool**
- Created from Python functions using `Tool.from_function()`
- Automatic schema generation from function signatures
- Seamless integration with agent execution

**3. AgentRuntime**
- Execution environment for agents
- Manages API connections and tool execution
- Integrates with MLflow for tracking

**4. MLflow Integration**
- Automatic experiment tracking
- Parameter and metric logging
- Model versioning and artifact storage

### Tool Creation Pattern

```python
# Simple function-based tool
def my_tool(param1: str, param2: int = 10) -> str:
    """Tool description.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
    
    Returns:
        Result description
    """
    return f"Processing {param1} with {param2}"

# Convert to tool
tool = Tool.from_function(my_tool)

# Use in agent
agent = Agent(
    name="assistant",
    instructions="You are helpful.",
    tools=[tool],
    model="gpt-4o-mini"
)
```

---

## Multi-Agent Systems

### Multi-Agent Data Workflow Example

```python
class MultiAgentDatabricksSystem:
    """Multi-agent system for data workflows."""

    def __init__(self):
        # Create specialized agents
        self.data_agent = Agent(
            name="data_analyst",
            instructions="You are a data analyst. Analyze data and provide insights.",
            tools=[Tool.from_function(search_data), Tool.from_function(get_dataset_info)],
            model="gpt-4o-mini"
        )

        self.ml_agent = Agent(
            name="ml_engineer",
            instructions="You are an ML engineer. Explain ML concepts.",
            model="gpt-4o-mini"
        )

        self.report_agent = Agent(
            name="report_writer",
            instructions="You are a report writer. Create clear reports.",
            model="gpt-4o-mini"
        )

        # Create runtime
        self.runtime = AgentRuntime()

    def run_workflow(self, topic: str):
        """Run multi-agent workflow with MLflow tracking."""
        with mlflow.start_run():
            # Step 1: Data Analysis
            data_result = self.runtime.run(
                agent=self.data_agent,
                input=f"Analyze data related to: {topic}"
            )

            # Step 2: ML Engineering
            ml_result = self.runtime.run(
                agent=self.ml_agent,
                input=f"Provide ML insights for: {data_result.output}"
            )

            # Step 3: Report Writing
            report_result = self.runtime.run(
                agent=self.report_agent,
                input=f"Create a report about {topic} based on: {ml_result.output}"
            )

            # Log to MLflow
            mlflow.log_param("topic", topic)
            mlflow.log_param("agents_used", "data_analyst,ml_engineer,report_writer")

            return {
                "data_analysis": data_result.output,
                "ml_insights": ml_result.output,
                "final_output": report_result.output
            }

# Usage
system = MultiAgentDatabricksSystem()
result = system.run_workflow("Customer Segmentation Analysis")
print(result["final_output"])
```

---

## Custom-Evals Integration

### Complete Evaluation System with MLflow Logging

```python
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM
import mlflow

class EvaluatedDatabricksAgent:
    """Databricks agent with evaluation and MLflow tracking."""

    def __init__(self):
        # Create agent
        self.agent = Agent(
            name="databricks_assistant",
            instructions="You are a helpful assistant.",
            tools=[Tool.from_function(get_weather), Tool.from_function(search_data)],
            model="gpt-4o-mini"
        )

        self.runtime = AgentRuntime()
        mlflow.set_experiment("agent_evaluation")

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run_and_evaluate(self, query: str, expected: str = None):
        """Run agent and evaluate with MLflow logging."""
        # Run agent
        with mlflow.start_run():
            mlflow.log_param("input", query)

            result = self.runtime.run(agent=self.agent, input=query)
            response = result.output

            mlflow.log_param("output", response)

            # Evaluate
            scores = {}
            with mlflow.start_run(nested=True):
                for name, evaluator in self.evaluators.items():
                    eval_input = {"input": query, "output": response}

                    if name == "correctness" and expected:
                        eval_input["expected"] = expected

                    score = evaluator.evaluate(eval_input)
                    scores[name] = score

                    # Log to MLflow
                    mlflow.log_metric(f"{name}_score", score.score)
                    mlflow.log_param(f"{name}_label", score.label)

            return {"response": response, "scores": scores}

# Usage
agent = EvaluatedDatabricksAgent()
result = agent.run_and_evaluate("What is MLflow?")

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

### 1. MLflow Experiment Management
**Organize experiments properly**:
```python
# ✅ Good: Set experiment name
mlflow.set_experiment("agent_production_v1")

with mlflow.start_run(run_name="user_query_001"):
    result = runtime.run(agent=agent, input=query)
    mlflow.log_param("query", query)
    mlflow.log_metric("response_length", len(result.output))
```

### 2. Tool Function Design
**Use type hints and docstrings**:
```python
# ✅ Good: Complete function with types and docs
def get_dataset_info(dataset_name: str) -> str:
    """Get information about a dataset.
    
    Args:
        dataset_name: Name of the dataset to query
    
    Returns:
        JSON string with dataset information
    """
    # Implementation
    return json.dumps(dataset_info)
```

### 3. Error Handling with MLflow
**Log errors to MLflow**:
```python
with mlflow.start_run():
    try:
        result = runtime.run(agent=agent, input=query)
        mlflow.log_param("status", "success")
    except Exception as e:
        mlflow.log_param("status", "error")
        mlflow.log_param("error_message", str(e))
        raise
```

### 4. Metric Tracking
**Track agent performance metrics**:
```python
with mlflow.start_run():
    start_time = time.time()
    result = runtime.run(agent=agent, input=query)
    execution_time = time.time() - start_time
    
    mlflow.log_metric("execution_time_seconds", execution_time)
    mlflow.log_metric("tool_calls", len(result.tool_calls))
    mlflow.log_metric("response_tokens", len(result.output.split()))
```

---

## Resources

### Official Documentation
- **Databricks**: https://www.databricks.com/
- **MLflow**: https://mlflow.org/
- **Agent Bricks SDK**: Check Databricks documentation

### Example Files
- **Complete Example**: `examples/databricks_agent_bricks_example.py` (19KB)
- **Test Suites**: 5 comprehensive tests covering all use cases
- **Custom-Evals Integration**: Full evaluation implementation with MLflow

### Phoenix Custom-Evals
- **Evaluators**: CoherenceEvaluator, RelevanceEvaluator, CorrectnessEvaluator, ToxicityEvaluator
- **LLM Integration**: Support for OpenAI, Anthropic, and other providers

---

## Quick Reference

### Installation
```bash
pip install databricks-agents mlflow
export OPENAI_API_KEY="your-openai-api-key"
```

### Basic Agent
```python
from databricks.agents import Agent, Tool
from databricks.agents.runtime import AgentRuntime
import mlflow

mlflow.set_experiment("my_experiment")
agent = Agent(name="assistant", instructions="You are helpful.", model="gpt-4o-mini")
runtime = AgentRuntime()

with mlflow.start_run():
    result = runtime.run(agent=agent, input="Your query here")
```

### With Tool
```python
def my_function(param: str) -> str:
    """Function description."""
    return f"Result for {param}"

tool = Tool.from_function(my_function)
agent = Agent(name="assistant", tools=[tool], model="gpt-4o-mini")
```

---

**Created**: 2026-01-17
**Status**: Production Ready
**Framework Version**: Latest
**Custom-Evals**: Fully Integrated
**MLflow**: Integrated
