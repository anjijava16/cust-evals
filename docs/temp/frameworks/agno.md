# Agno Framework Integration

**Official Documentation**: https://docs.agno.com/
**GitHub**: https://github.com/agno-agi/agno
**Installation**: `pip install agno anthropic`

---

## 🎯 Overview

**Agno** is a comprehensive multi-agent system framework designed for building, running, and managing agents at scale. It provides a unified platform for agent orchestration, workflow automation, knowledge management, and human-in-the-loop interactions.

### Key Features

✅ **Multi-Agent Systems** - Teams for coordinated workflows
✅ **Workflow Automation** - Conditional, parallel, and iterative execution
✅ **Knowledge Management** - RAG with vector databases
✅ **Memory & Sessions** - Persistent conversation state
✅ **Tool Integration** - MCP (Model Context Protocol) support
✅ **Structured I/O** - Pydantic model validation
✅ **Multimodal** - Images, audio, video, files
✅ **Human-in-the-Loop** - User confirmation and input
✅ **Reasoning Support** - Chain-of-thought for advanced models
✅ **Tracing & Evaluation** - Built-in observability

---

## 📦 Installation

```bash
# Basic installation
pip install agno anthropic

# With additional features
pip install agno anthropic mcp 'fastapi[standard]' sqlalchemy

# For Custom-Evals integration
pip install agno anthropic openai

# Set API keys
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"  # For evaluators
```

---

## 🚀 Quick Start

### Basic Agent

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get current weather for a location."""
    weather_data = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Cloudy, 65°F"
    }
    return weather_data.get(location, "Weather data not available")

agent = Agent(
    name="Research Assistant",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=[
        "You are a helpful research assistant.",
        "Provide accurate, concise information.",
    ],
    tools=[get_weather],
    markdown=True,
)

response = agent.run("What's the weather in San Francisco?")
print(response.content)
```

### Multi-Agent System with Teams

```python
from agno.agent import Agent
from agno.team import Team
from agno.models.anthropic import Claude

# Create specialized agents
researcher = Agent(
    name="Researcher",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["Research and gather information"],
    tools=[search_tool],
)

analyst = Agent(
    name="Analyst",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["Analyze data and provide insights"],
    tools=[calculate_tool],
)

# Create team
team = Team(
    name="Research Team",
    agents=[researcher, analyst],
    instructions=["Collaborate to provide comprehensive responses"],
)

response = team.run("Research machine learning and analyze trends")
print(response.content)
```

---

## 🔧 Tool Definition

Agno supports multiple tool definition patterns:

### Python Decorator Pattern

```python
from agno.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information.

    Args:
        query: Search query string

    Returns:
        Search results
    """
    # Implementation
    return f"Results for: {query}"

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: Math expression (e.g., "2 + 2")

    Returns:
        Calculation result
    """
    result = eval(expression)
    return f"Result: {result}"
```

### Toolkit Pattern

```python
from agno.toolkit import Toolkit

class DataToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="data_toolkit")

    @tool
    def fetch_data(self, source: str) -> str:
        """Fetch data from source."""
        return f"Data from {source}"

    @tool
    def process_data(self, data: str) -> str:
        """Process data."""
        return f"Processed: {data}"
```

### MCP Integration

```python
from agno.tools.mcp import MCPTools

agent = Agent(
    name="MCP Agent",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[
        MCPTools(
            transport="streamable-http",
            url="https://docs.agno.com/mcp"
        )
    ],
)
```

---

## 📊 Custom-Evals Integration

### Evaluated Agent Pattern

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM

class AgnoEvaluatedAgent:
    def __init__(self):
        # Create Agno agent
        self.agent = Agent(
            name="Research Assistant",
            model=Claude(id="claude-sonnet-4-5"),
            instructions=["You are a helpful assistant"],
            tools=[get_weather, search_web],
            markdown=True,
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

        # Quality thresholds
        self.thresholds = {
            "coherence": 0.7,
            "relevance": 0.7,
            "correctness": 0.7,
            "toxicity": 0.2  # Lower is better
        }

    def run(self, query: str) -> str:
        """Run agent and return response."""
        response = self.agent.run(query)
        return response.content if hasattr(response, "content") else str(response)

    def evaluate(self, query: str, response: str) -> dict:
        """Evaluate response using Custom-Evals."""
        scores = {}
        for name, evaluator in self.evaluators.items():
            score = evaluator.evaluate({
                "input": query,
                "output": response
            })
            scores[name] = score
        return scores

    def run_and_evaluate(self, query: str) -> dict:
        """Run agent and evaluate response."""
        response = self.run(query)
        scores = self.evaluate(query, response)
        return {
            "query": query,
            "response": response,
            "scores": scores
        }

    def validate_quality_gates(self, scores: dict) -> bool:
        """Validate quality thresholds."""
        for metric, threshold in self.thresholds.items():
            score_value = scores[metric].score

            if metric == "toxicity":
                if score_value > threshold:
                    return False
            else:
                if score_value < threshold:
                    return False

        return True
```

### Usage Example

```python
agent = AgnoEvaluatedAgent()

# Run and evaluate
result = agent.run_and_evaluate("What is machine learning?")

print(f"Response: {result['response']}")
print("\nEvaluation Scores:")
for metric, score in result['scores'].items():
    print(f"  {metric}: {score.score:.2f} - {score.label}")

# Validate quality gates
passed = agent.validate_quality_gates(result['scores'])
print(f"\nQuality Gates: {'✅ PASSED' if passed else '❌ FAILED'}")
```

---

## 🔄 Multi-Agent Evaluation

```python
from agno.team import Team

class AgnoMultiAgentSystem:
    def __init__(self):
        # Create specialized agents
        self.researcher = Agent(
            name="Researcher",
            model=Claude(id="claude-sonnet-4-5"),
            instructions=["Research and gather information"],
            tools=[search_tool],
        )

        self.analyst = Agent(
            name="Analyst",
            model=Claude(id="claude-sonnet-4-5"),
            instructions=["Analyze data and provide insights"],
            tools=[calculate_tool],
        )

        # Create team
        self.team = Team(
            name="Research Team",
            agents=[self.researcher, self.analyst],
            instructions=["Collaborate for comprehensive responses"],
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, query: str) -> str:
        """Run multi-agent team."""
        response = self.team.run(query)
        return response.content if hasattr(response, "content") else str(response)

    def evaluate(self, query: str, response: str) -> dict:
        """Evaluate team response."""
        scores = {}
        for name, evaluator in self.evaluators.items():
            score = evaluator.evaluate({
                "input": query,
                "output": response
            })
            scores[name] = score
        return scores

# Usage
system = AgnoMultiAgentSystem()
response = system.run("Research AI and calculate trends")
scores = system.evaluate(query, response)
```

---

## 📈 Advanced Features

### Knowledge Management (RAG)

```python
from agno.knowledge.vector_db import VectorDb
from agno.agent import Agent

agent = Agent(
    name="Knowledge Agent",
    model=Claude(id="claude-sonnet-4-5"),
    knowledge=VectorDb(
        collection="documents",
        path="./knowledge_base"
    ),
)
```

### Memory and Sessions

```python
from agno.db.sqlite import SqliteDb

agent = Agent(
    name="Stateful Agent",
    model=Claude(id="claude-sonnet-4-5"),
    db=SqliteDb(db_file="agent_memory.db"),
    add_history_to_context=True,
    session_id="user_123",
)
```

### Structured Output

```python
from pydantic import BaseModel
from agno.agent import Agent

class WeatherResponse(BaseModel):
    location: str
    temperature: float
    condition: str

agent = Agent(
    name="Weather Agent",
    model=Claude(id="claude-sonnet-4-5"),
    response_model=WeatherResponse,
)
```

### Reasoning Support

```python
agent = Agent(
    name="Reasoning Agent",
    model=Claude(id="claude-sonnet-4-5"),
    reasoning=True,  # Enable chain-of-thought
)
```

---

## ✅ Quality Thresholds

```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,    # Minimum coherence score
    "relevance": 0.7,    # Minimum relevance score
    "correctness": 0.7,  # Minimum correctness score
    "toxicity": 0.2      # Maximum toxicity (lower is better)
}

def validate_quality_gates(scores: dict) -> bool:
    """Validate response against quality thresholds."""
    for metric, threshold in QUALITY_THRESHOLDS.items():
        score_value = scores[metric].score

        if metric == "toxicity":
            if score_value > threshold:
                return False
        else:
            if score_value < threshold:
                return False

    return True
```

---

## 📊 Evaluation Metrics

Custom-Evals provides comprehensive metrics for Agno agents:

### Coherence Evaluator
- **Threshold**: ≥ 0.7
- **Measures**: Logical flow and consistency
- **Use Case**: Ensure responses are well-structured

### Relevance Evaluator
- **Threshold**: ≥ 0.7
- **Measures**: Query-response relevance
- **Use Case**: Validate response addresses query

### Correctness Evaluator
- **Threshold**: ≥ 0.7
- **Measures**: Factual accuracy
- **Use Case**: Ensure accurate information

### Toxicity Evaluator
- **Threshold**: ≤ 0.2 (lower is better)
- **Measures**: Harmful content
- **Use Case**: Filter inappropriate responses

---

## 🧪 Testing Patterns

### Test Suite 1: Simple Agent
```python
agent = AgnoEvaluatedAgent()
result = agent.run_and_evaluate("What is AI?")
passed = agent.validate_quality_gates(result['scores'])
```

### Test Suite 2: Tool Usage
```python
queries = [
    "What's the weather in NYC?",
    "Search for machine learning",
    "Calculate 15 * 24"
]
for query in queries:
    result = agent.run_and_evaluate(query)
    # Validate tool was used correctly
```

### Test Suite 3: Multi-Agent System
```python
system = AgnoMultiAgentSystem()
response = system.run("Complex query requiring multiple agents")
scores = system.evaluate(query, response)
```

### Test Suite 4: Quality Gates
```python
scenarios = [
    ("High quality", "Explain AI"),
    ("Technical", "Time complexity of quicksort"),
    ("Creative", "Why is sky blue")
]
for name, query in scenarios:
    result = agent.run_and_evaluate(query)
    passed = agent.validate_quality_gates(result['scores'])
```

### Test Suite 5: Batch Evaluation
```python
queries = ["Query 1", "Query 2", "Query 3", ...]
results = [agent.run_and_evaluate(q) for q in queries]

# Aggregate metrics
for metric in ["coherence", "relevance", "correctness"]:
    scores = [r['scores'][metric].score for r in results]
    print(f"{metric}: avg={sum(scores)/len(scores):.3f}")
```

---

## 🎓 Best Practices

### 1. Use Specialized Agents
```python
# ✅ Good: Create specialized agents for different tasks
researcher = Agent(name="Researcher", tools=[search_tool])
analyst = Agent(name="Analyst", tools=[calc_tool])
team = Team(agents=[researcher, analyst])
```

### 2. Implement Quality Gates
```python
# ✅ Good: Validate all responses
result = agent.run_and_evaluate(query)
if not agent.validate_quality_gates(result['scores']):
    alert_quality_failure(query, result)
```

### 3. Leverage Memory
```python
# ✅ Good: Use persistent memory for context
agent = Agent(
    name="Stateful Agent",
    db=SqliteDb(db_file="memory.db"),
    add_history_to_context=True,
)
```

### 4. Monitor Metrics
```python
# ✅ Good: Track metrics over time
for query in test_queries:
    result = agent.run_and_evaluate(query)
    log_metrics_to_monitoring(result['scores'])
```

---

## 🔗 Resources

- **Official Documentation**: https://docs.agno.com/
- **GitHub Repository**: https://github.com/agno-agi/agno
- **Example Code**: `examples/agno_example.py`
- **Custom-Evals**: See [LLM-Based Evaluators](../evaluators/llm-based.md)

---

## 📝 Complete Example

See [`examples/agno_example.py`](../../examples/agno_example.py) for a complete working example with:
- Simple Agno agent with tools
- Multi-agent system with Teams
- Full Custom-Evals integration
- 5 comprehensive test suites
- Quality gates validation
- Batch evaluation

```bash
# Run the example
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
python examples/agno_example.py
```

---

**Created**: 2026-01-17
**Framework Version**: Agno latest
**Custom-Evals**: Fully integrated
**Test Coverage**: 5 comprehensive test suites
