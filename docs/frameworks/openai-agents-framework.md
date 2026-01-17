# OpenAI Agents Framework - Official Agent Framework

## Overview

**OpenAI Agents Framework** is the official framework from OpenAI for building production-grade AI agents with advanced capabilities including handoffs, routing, and multi-agent collaboration.

**Key Features**:
- Official OpenAI framework (`openai-agents-python`)
- Native agent handoffs and routing
- Function tools with @function_tool decorator
- Multi-agent collaboration
- Built on OpenAI models (GPT-4, GPT-4o-mini)
- Production-ready architecture

**Official Documentation**: https://openai.github.io/openai-agents-python/

**Example File**: `examples/openai_agents_framework_example.py`

---

## Installation

```bash
pip install openai-agents
pip install openai>=1.0.0
```

**Set up API Key**:
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

---

## Quick Start

### Simple Agent

```python
from agents import Agent, Runner, function_tool

# Define a tool
@function_tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

# Create agent
agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant.",
    tools=[get_weather],
    model="gpt-4o-mini"
)

# Create runner
runner = Runner(api_key="your-api-key")

# Run agent
result = runner.run(
    agent=agent,
    messages=[{"role": "user", "content": "What's the weather in SF?"}]
)

# Get response
for msg in result.messages:
    if msg.role == "assistant" and msg.content:
        print(msg.content)
```

---

## Function Tools

### Define Tools with Decorator

```python
from agents import function_tool

@function_tool
def search_database(query: str) -> str:
    """Search knowledge database.

    Args:
        query: The search query

    Returns:
        Relevant information from database
    """
    db = {
        "python": "Python is a programming language...",
        "ai": "AI is artificial intelligence..."
    }
    return db.get(query.lower(), "No information found")

@function_tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression.

    Args:
        expression: Math expression (e.g., '25 * 4')

    Returns:
        Calculation result
    """
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Agent with multiple tools
agent = Agent(
    name="helper",
    instructions="You have tools for searching and calculations.",
    tools=[search_database, calculate],
    model="gpt-4o-mini"
)
```

---

## Agent Handoffs

### Multi-Agent Routing

```python
from agents import Agent, Runner
from agents.extensions.handoff import Handoff

# Create specialized agents
sales_agent = Agent(
    name="sales_agent",
    instructions="You help with purchases and pricing.",
    model="gpt-4o-mini"
)

support_agent = Agent(
    name="support_agent",
    instructions="You help with technical issues.",
    model="gpt-4o-mini"
)

# Create triage agent with handoffs
triage_agent = Agent(
    name="triage",
    instructions="""Route customers to the right agent:
    - For purchases/pricing → Transfer to sales_agent
    - For technical issues → Transfer to support_agent
    """,
    handoffs=[
        Handoff(agent=sales_agent),
        Handoff(agent=support_agent)
    ],
    model="gpt-4o-mini"
)

# Run with routing
runner = Runner(api_key="your-api-key")
result = runner.run(
    agent=triage_agent,
    messages=[{"role": "user", "content": "I need technical support"}]
)

# Agent automatically routes to support_agent
```

---

## Advanced Multi-Agent System

### Complete Workflow

```python
from agents import Agent, Runner
from agents.extensions.handoff import Handoff

# Research Agent
research_agent = Agent(
    name="researcher",
    instructions="Research topics and gather information.",
    tools=[search_database],
    model="gpt-4o-mini"
)

# Analysis Agent
analysis_agent = Agent(
    name="analyst",
    instructions="Analyze research and extract insights.",
    model="gpt-4o-mini"
)

# Writer Agent
writer_agent = Agent(
    name="writer",
    instructions="Create clear summaries from analysis.",
    model="gpt-4o-mini"
)

# Coordinator with sequential handoffs
coordinator = Agent(
    name="coordinator",
    instructions="""Coordinate a research workflow:
    1. Start with researcher for information gathering
    2. Hand off to analyst for analysis
    3. Finally to writer for summary
    """,
    handoffs=[
        Handoff(agent=research_agent),
        Handoff(agent=analysis_agent),
        Handoff(agent=writer_agent)
    ],
    model="gpt-4o-mini"
)

# Run workflow
runner = Runner(api_key="your-api-key")
result = runner.run(
    agent=coordinator,
    messages=[{"role": "user", "content": "Research quantum computing"}]
)
```

---

## Evaluation with Custom-Evals

### Comprehensive Evaluation

```python
from agents import Agent, Runner, function_tool
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM

# Create and run agent
agent = Agent(
    name="assistant",
    instructions="You are helpful.",
    model="gpt-4o-mini"
)

runner = Runner(api_key="your-api-key")
result = runner.run(
    agent=agent,
    messages=[{"role": "user", "content": "Explain neural networks"}]
)

# Extract response
response_text = ""
for msg in result.messages:
    if msg.role == "assistant" and msg.content:
        response_text = msg.content

# Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

evaluators = {
    "coherence": CoherenceEvaluator(eval_llm),
    "relevance": RelevanceEvaluator(eval_llm),
    "correctness": CorrectnessEvaluator(eval_llm),
    "toxicity": ToxicityEvaluator(eval_llm)
}

scores = {}
for name, evaluator in evaluators.items():
    score = evaluator.evaluate({
        "input": "Explain neural networks",
        "output": response_text
    })
    scores[name] = score
    print(f"{name.capitalize()}: {score.label} ({score.score:.2f})")
```

---

## Testing Examples

### Test Simple Agent

```python
def test_simple_agent():
    """Test basic agent functionality."""
    agent = Agent(
        name="test_agent",
        instructions="You are helpful.",
        model="gpt-4o-mini"
    )

    runner = Runner(api_key=os.getenv("OPENAI_API_KEY"))
    result = runner.run(
        agent=agent,
        messages=[{"role": "user", "content": "What is AI?"}]
    )

    assert len(result.messages) > 0
    assert any(msg.role == "assistant" for msg in result.messages)

def test_tool_calling():
    """Test agent with tools."""
    @function_tool
    def get_weather(location: str) -> str:
        return f"Sunny in {location}"

    agent = Agent(
        name="weather_agent",
        instructions="Help with weather.",
        tools=[get_weather],
        model="gpt-4o-mini"
    )

    runner = Runner(api_key=os.getenv("OPENAI_API_KEY"))
    result = runner.run(
        agent=agent,
        messages=[{"role": "user", "content": "Weather in NYC?"}]
    )

    # Verify tool was called
    tool_called = False
    for msg in result.messages:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            tool_called = True

    assert tool_called

def test_handoffs():
    """Test multi-agent handoffs."""
    agent1 = Agent(name="agent1", instructions="First agent")
    agent2 = Agent(name="agent2", instructions="Second agent")

    triage = Agent(
        name="triage",
        instructions="Route to agent2",
        handoffs=[Handoff(agent=agent1), Handoff(agent=agent2)]
    )

    runner = Runner(api_key=os.getenv("OPENAI_API_KEY"))
    result = runner.run(
        agent=triage,
        messages=[{"role": "user", "content": "Help me"}]
    )

    assert len(result.messages) > 0
```

---

## Best Practices

### 1. Clear Agent Instructions

```python
# Good: Specific and actionable
agent = Agent(
    name="support_agent",
    instructions="""You are a technical support specialist.
    - Help users troubleshoot issues
    - Provide step-by-step solutions
    - Transfer to engineering for complex bugs
    - Be patient and professional
    """,
    model="gpt-4o-mini"
)

# Avoid: Vague instructions
agent = Agent(
    name="agent",
    instructions="Help users",
    model="gpt-4o-mini"
)
```

### 2. Tool Documentation

```python
# Good: Well-documented tool
@function_tool
def search_orders(customer_id: str, status: str = None) -> str:
    """Search customer orders.

    Args:
        customer_id: The customer ID to search for
        status: Optional order status filter (e.g., 'shipped', 'pending')

    Returns:
        List of orders matching criteria as JSON string
    """
    # Implementation
    pass

# The docstring helps the LLM understand when and how to use the tool
```

### 3. Handoff Strategy

```python
# Good: Clear handoff logic
triage = Agent(
    name="triage",
    instructions="""Analyze customer request and route:
    - Billing questions → billing_agent
    - Technical issues → support_agent
    - General questions → info_agent
    Be specific about which agent to use.
    """,
    handoffs=[
        Handoff(agent=billing_agent),
        Handoff(agent=support_agent),
        Handoff(agent=info_agent)
    ]
)
```

### 4. Error Handling

```python
def run_agent_safely(agent, messages, max_retries=3):
    """Run agent with error handling."""
    runner = Runner(api_key=os.getenv("OPENAI_API_KEY"))

    for attempt in range(max_retries):
        try:
            result = runner.run(agent=agent, messages=messages)
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Retry {attempt + 1}: {e}")
            time.sleep(2 ** attempt)
```

---

## Use Cases

### Customer Service Routing

```python
# Multi-tier support with handoffs
triage → [tier1_support, tier2_support, engineering]
```

### Sales Workflow

```python
# Lead to conversion pipeline
lead_qualifier → product_specialist → sales_closer
```

### Content Creation

```python
# Multi-stage content workflow
researcher → writer → editor → publisher
```

---

## Quality Gates

```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
    "correctness": 0.7,
    "toxicity": 0.2
}

def validate_agent_output(query, response, scores):
    """Validate agent output quality."""
    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric in scores:
            if metric == "toxicity":
                if scores[metric].score > threshold:
                    return False, f"High toxicity"
            else:
                if scores[metric].score < threshold:
                    return False, f"Low {metric}"

    return True, "All checks passed"
```

---

## Troubleshooting

### Issue: Tools not being called

**Solution**: Improve tool docstrings and descriptions

```python
@function_tool
def get_weather(location: str) -> str:
    """Get current weather for a location.

    Use this when user asks about weather, temperature, conditions, or forecast.

    Args:
        location: City name (e.g., 'San Francisco', 'New York')

    Returns:
        Weather information including temperature and conditions
    """
    # Implementation
```

### Issue: Handoffs not working

**Solution**: Make handoff instructions explicit

```python
triage = Agent(
    instructions="""You MUST transfer to the appropriate agent:
    - For sales questions: USE sales_agent handoff
    - For support issues: USE support_agent handoff
    Do not answer directly - always transfer.
    """,
    handoffs=[Handoff(agent=sales_agent), Handoff(agent=support_agent)]
)
```

### Issue: High API costs

**Solution**: Use gpt-4o-mini and limit message history

```python
# Use mini model
agent = Agent(name="agent", model="gpt-4o-mini", ...)

# Limit conversation history
messages = messages[-10:]  # Keep last 10 messages only
```

---

## Comparison with Other Frameworks

| Feature | OpenAI Agents | Swarm | Assistants | Core SDK |
|---------|---------------|-------|------------|----------|
| Official Framework | ✅ | ✅ | ✅ | ✅ |
| Handoffs | ✅✅ | ✅ | ❌ | Custom |
| Function Tools | ✅✅ | ✅ | ✅ | ✅ |
| State Management | ✅ | Manual | ✅ Threads | Manual |
| Learning Curve | Low-Medium | Very Low | Low | Low |
| Best For | Production agents | Simple routing | Chatbots | Custom agents |

---

## Resources

- **Official Docs**: https://openai.github.io/openai-agents-python/
- **GitHub**: https://github.com/openai/openai-agents-python
- **OpenAI Platform**: https://platform.openai.com/
- **Example File**: `examples/openai_agents_framework_example.py`

---

## Next Steps

1. Install: `pip install openai-agents`
2. Run example: `python examples/openai_agents_framework_example.py`
3. Create your first agent with tools
4. Experiment with handoffs
5. Build a multi-agent system

**See Also**:
- [OpenAI Swarm](openai-swarm.md) - Lightweight alternative
- [OpenAI Assistants](openai-assistants.md) - Thread-based agents
- [OpenAI Agents SDK](openai-agents.md) - Core function calling
