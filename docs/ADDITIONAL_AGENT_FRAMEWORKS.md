# Additional Agent Frameworks - Complete Guide

This guide covers 4 additional agent frameworks with comprehensive examples and testing using custom-evals.

## Table of Contents

- [Overview](#overview)
- [Framework Examples](#framework-examples)
  - [Autogen](#autogen-microsoft)
  - [CrewAI](#crewai)
  - [OpenAI Assistants API](#openai-assistants-api)
  - [PydanticAI](#pydanticai)
- [Quick Comparison](#quick-comparison)
- [Best Practices](#best-practices)

---

## Overview

This document covers **4 additional agent frameworks**:

1. **Autogen** (Microsoft) - Multi-agent conversations
2. **CrewAI** - Role-based agent orchestration
3. **OpenAI Assistants API** - Official OpenAI agents with tools
4. **PydanticAI** - Type-safe agents with Pydantic

All examples include comprehensive testing with custom-evals metrics.

---

## Framework Examples

### Autogen (Microsoft)

**File**: `examples/autogen_agent_example.py`

**Description**:
Microsoft's framework for building multi-agent conversational systems with support for code execution and function calling.

**Key Features**:
- Multi-agent conversations
- Code execution capabilities
- Function calling
- Group chat management
- Human-in-the-loop support

**Quick Start**:

```bash
# Install
pip install pyautogen

# Run
export OPENAI_API_KEY="your-key"
python examples/autogen_agent_example.py
```

**Example Code**:

```python
import autogen
from autogen import AssistantAgent, UserProxyAgent
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

# Configure LLM
llm_config = {
    "config_list": [{
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }],
    "temperature": 0,
}

# Create assistant
assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="You are a helpful AI assistant."
)

# Create user proxy
user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    code_execution_config={"work_dir": "workspace"}
)

# Initiate conversation
user_proxy.initiate_chat(
    assistant,
    message="What is machine learning?"
)

# Get response
conversation = user_proxy.chat_messages[assistant]
response = conversation[-1]["content"]

# Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)
score = evaluator.evaluate({
    "input": "What is machine learning?",
    "output": response
})

print(f"Coherence: {score.label} ({score.score:.2f})")
```

**Test Suites**:

1. **Two-Agent System**: Simple assistant + user proxy
2. **Group Chat**: Multi-agent collaboration
3. **Function Calling**: Agent with custom functions
4. **Quality Gates**: Automated quality checks

**Use Cases**:
- Conversational AI with code execution
- Multi-agent problem solving
- Automated task execution
- Research assistants with tool access

---

### CrewAI

**File**: `examples/crewai_agent_example.py`

**Description**:
Framework for orchestrating role-based AI agents in sequential or hierarchical processes.

**Key Features**:
- Role-based agent design
- Task delegation
- Sequential/hierarchical processes
- Specialized agent roles
- Team collaboration

**Quick Start**:

```bash
# Install
pip install crewai

# Run
export OPENAI_API_KEY="your-key"
python examples/crewai_agent_example.py
```

**Example Code**:

```python
from crewai import Agent, Task, Crew, Process
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

# Create agents
researcher = Agent(
    role="Research Analyst",
    goal="Gather comprehensive information",
    backstory="You are an experienced research analyst...",
    verbose=True,
    llm="gpt-4o-mini"
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging content",
    backstory="You are a skilled content writer...",
    verbose=True,
    llm="gpt-4o-mini"
)

# Create tasks
research_task = Task(
    description="Research artificial intelligence trends",
    agent=researcher,
    expected_output="Comprehensive research findings"
)

writing_task = Task(
    description="Write an article based on research",
    agent=writer,
    expected_output="Well-written article",
    context=[research_task]
)

# Create crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential
)

# Execute
result = crew.kickoff()

# Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)
score = evaluator.evaluate({
    "input": "Write about AI trends",
    "output": str(result)
})

print(f"Coherence: {score.label} ({score.score:.2f})")
```

**Test Suites**:

1. **Simple Crew**: 2-agent research & writing
2. **Specialized Crew**: 4-agent business analysis
3. **Quality Gates**: Production readiness checks
4. **Crew Comparison**: Simple vs specialized

**Use Cases**:
- Content creation workflows
- Business analysis
- Research projects
- Multi-step task automation

---

### OpenAI Assistants API

**File**: `examples/openai_assistants_example.py`

**Description**:
Official OpenAI API for building assistants with persistent threads, function calling, and code interpreter.

**Key Features**:
- Persistent conversation threads
- Function calling
- Code interpreter
- File handling
- Built-in knowledge retrieval

**Quick Start**:

```bash
# Install
pip install openai>=1.0.0

# Run
export OPENAI_API_KEY="your-key"
python examples/openai_assistants_example.py
```

**Example Code**:

```python
from openai import OpenAI
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM
import time

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create assistant
assistant = client.beta.assistants.create(
    name="General Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4o-mini"
)

# Create thread
thread = client.beta.threads.create()

# Add message
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is quantum computing?"
)

# Run assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Wait for completion
while run.status in ["queued", "in_progress"]:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

# Get response
if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value

    # Evaluate
    eval_llm = LLM(provider="openai", model="gpt-4o-mini")
    evaluator = CoherenceEvaluator(eval_llm)
    score = evaluator.evaluate({
        "input": "What is quantum computing?",
        "output": response
    })

    print(f"Coherence: {score.label} ({score.score:.2f})")

# Cleanup
client.beta.threads.delete(thread.id)
client.beta.assistants.delete(assistant.id)
```

**Function Calling Example**:

```python
# Define functions
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }
]

# Create assistant with functions
assistant = client.beta.assistants.create(
    name="Weather Assistant",
    instructions="You help with weather queries.",
    model="gpt-4o-mini",
    tools=functions
)

# Handle function calls in run loop
if run.status == "requires_action":
    tool_calls = run.required_action.submit_tool_outputs.tool_calls

    tool_outputs = []
    for tool_call in tool_calls:
        if tool_call.function.name == "get_weather":
            # Execute function
            result = get_weather(city="San Francisco")
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": result
            })

    # Submit outputs
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=tool_outputs
    )
```

**Test Suites**:

1. **Simple Assistant**: Q&A interactions
2. **Function Calling**: Tool integration
3. **Code Interpreter**: Data analysis tasks

**Use Cases**:
- Customer support chatbots
- Personal assistants
- Data analysis tools
- Q&A systems with context

---

### PydanticAI

**File**: `examples/pydanticai_agent_example.py`

**Description**:
Pydantic's framework for building type-safe, production-grade AI agents with structured outputs.

**Key Features**:
- Type-safe agent development
- Structured outputs with Pydantic models
- Tool/function calling with validation
- Async/sync support
- Full Pydantic integration

**Quick Start**:

```bash
# Install
pip install pydantic-ai pydantic>=2.0

# Run
export OPENAI_API_KEY="your-key"
python examples/pydanticai_agent_example.py
```

**Example Code**:

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM

# Define structured output
class WeatherInfo(BaseModel):
    city: str = Field(description="City name")
    temperature: str = Field(description="Temperature")
    condition: str = Field(description="Weather condition")

# Create agent
agent = Agent(
    'openai:gpt-4o-mini',
    system_prompt="You are a helpful assistant."
)

# Add tool
@agent.tool
async def get_weather(ctx: RunContext[None], city: str) -> WeatherInfo:
    """Get weather for a city."""
    # Simulated weather data
    return WeatherInfo(
        city=city,
        temperature="72°F",
        condition="Sunny"
    )

# Run agent
import asyncio

async def run_agent():
    result = await agent.run("What's the weather in San Francisco?")
    response = result.data

    # Evaluate
    eval_llm = LLM(provider="openai", model="gpt-4o-mini")
    evaluator = CoherenceEvaluator(eval_llm)
    score = evaluator.evaluate({
        "input": "What's the weather in San Francisco?",
        "output": str(response)
    })

    print(f"Coherence: {score.label} ({score.score:.2f})")

asyncio.run(run_agent())
```

**Structured Output Example**:

```python
from pydantic import BaseModel, Field
from typing import List

class AnalysisResult(BaseModel):
    """Structured analysis result."""
    summary: str = Field(description="Summary")
    key_points: List[str] = Field(description="Key points")
    recommendations: List[str] = Field(description="Recommendations")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")

# Create agent with structured output
agent = Agent(
    'openai:gpt-4o-mini',
    result_type=AnalysisResult,
    system_prompt="You are an analyst."
)

# Run analysis
result = await agent.run("Analyze AI in healthcare")
analysis: AnalysisResult = result.data

print(f"Summary: {analysis.summary}")
print(f"Key Points: {len(analysis.key_points)}")
print(f"Confidence: {analysis.confidence}")
```

**Test Suites**:

1. **Simple Agent**: Basic Q&A
2. **Tool-Based Agent**: Function calling
3. **Structured Output**: Pydantic models
4. **Quality Gates**: Type-safe evaluation

**Use Cases**:
- Type-safe agent development
- Structured data extraction
- API-driven agents
- Production LLM applications

---

## Quick Comparison

| Feature | Autogen | CrewAI | OpenAI Assistants | PydanticAI |
|---------|---------|--------|-------------------|------------|
| **Multi-Agent** | ✅ Built-in | ✅ Role-based | ❌ Single agent | ✅ Custom |
| **Code Execution** | ✅ Native | ❌ No | ✅ Interpreter | ❌ No |
| **Function Calling** | ✅ Yes | ⚠️  Limited | ✅ Native | ✅ Yes |
| **Structured Output** | ❌ No | ❌ No | ❌ No | ✅ Pydantic |
| **Persistent Threads** | ❌ No | ❌ No | ✅ Built-in | ❌ No |
| **Type Safety** | ⚠️  Partial | ⚠️  Partial | ⚠️  Partial | ✅ Full |
| **Learning Curve** | Medium | Low | Low | Medium |
| **Best For** | Research & Dev | Content/Business | Production Apps | Type-Safe Apps |

---

## Best Practices

### 1. Choosing the Right Framework

**Use Autogen when**:
- Need multi-agent conversations
- Require code execution
- Building research assistants
- Iterative problem solving

**Use CrewAI when**:
- Role-based workflows
- Content creation
- Business processes
- Sequential tasks

**Use OpenAI Assistants when**:
- Building production chatbots
- Need persistent context
- Official OpenAI support preferred
- File handling required

**Use PydanticAI when**:
- Type safety is critical
- Structured outputs needed
- Building APIs
- Production LLM apps

### 2. Evaluation Strategy

**All Frameworks**:
```python
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM

eval_llm = LLM(provider="openai", model="gpt-4o-mini")

evaluators = {
    "coherence": CoherenceEvaluator(eval_llm),
    "relevance": RelevanceEvaluator(eval_llm),
    "toxicity": ToxicityEvaluator(eval_llm)
}

# Evaluate response
scores = {}
for name, evaluator in evaluators.items():
    score = evaluator.evaluate({
        "input": query,
        "output": response
    })
    scores[name] = score

# Check quality
for metric, score in scores.items():
    print(f"{metric}: {score.label} ({score.score:.2f})")
```

### 3. Quality Gates

```python
# Define thresholds
QUALITY_THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
    "toxicity": 0.2  # Lower is better
}

# Check gates
def check_quality_gates(scores):
    for metric, threshold in QUALITY_THRESHOLDS.items():
        score_value = scores[metric].score

        if metric == "toxicity":
            if score_value > threshold:
                return False, f"{metric} too high"
        else:
            if score_value < threshold:
                return False, f"{metric} too low"

    return True, "All gates passed"

passed, message = check_quality_gates(scores)
print(f"Quality Check: {'✅' if passed else '❌'} {message}")
```

### 4. Error Handling

```python
def run_agent_safely(agent, message):
    """Run agent with comprehensive error handling."""
    try:
        result = agent.run(message)

        if not result.get("success"):
            print(f"❌ Agent failed: {result.get('error')}")
            return None

        # Evaluate
        scores = evaluate(message, result["response"])

        # Check quality
        passed, msg = check_quality_gates(scores)
        if not passed:
            print(f"⚠️  Quality gate failed: {msg}")

        return result

    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None
```

### 5. Testing Pattern

```python
def test_agent_framework(agent_class, test_cases):
    """Standard testing pattern for any framework."""
    agent = agent_class()
    results = []

    for test_case in test_cases:
        # Run
        result = agent.run(test_case["input"])

        if not result["success"]:
            continue

        # Evaluate
        scores = agent.evaluate(
            test_case["input"],
            result["response"]
        )

        # Validate
        passed = all(
            score.score >= 0.7
            for score in scores.values()
            if score.name != "toxicity"
        )

        results.append({
            "input": test_case["input"],
            "passed": passed,
            "scores": scores
        })

    # Summary
    pass_rate = sum(r["passed"] for r in results) / len(results)
    print(f"Pass Rate: {pass_rate:.1%}")

    return results
```

---

## Installation Summary

```bash
# All frameworks
pip install pyautogen crewai openai>=1.0.0 pydantic-ai pydantic>=2.0

# Individual frameworks
pip install pyautogen        # Autogen
pip install crewai           # CrewAI
pip install openai>=1.0.0    # OpenAI Assistants
pip install pydantic-ai pydantic>=2.0  # PydanticAI

# Custom evals
cd cust-evals
pip install -e ".[dev]"
```

---

## Running Examples

```bash
# Set API key
export OPENAI_API_KEY="your-key"

# Run individual examples
python examples/autogen_agent_example.py
python examples/crewai_agent_example.py
python examples/openai_assistants_example.py
python examples/pydanticai_agent_example.py
```

---

## Summary

You now have **4 additional agent frameworks** with:
- ✅ Production-ready examples
- ✅ Comprehensive testing
- ✅ Custom-evals integration
- ✅ Quality gates
- ✅ Best practices

**Total Agent Frameworks Covered**: 8
1. LangChain ReAct
2. LangGraph
3. Multi-Agent System
4. Google Vertex AI
5. **Autogen** 🆕
6. **CrewAI** 🆕
7. **OpenAI Assistants** 🆕
8. **PydanticAI** 🆕

For complete RAG examples, see [AGENTS_AND_RAG_GUIDE.md](AGENTS_AND_RAG_GUIDE.md).

**Happy Testing! 🚀**
