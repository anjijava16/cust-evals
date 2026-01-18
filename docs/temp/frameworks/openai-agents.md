# OpenAI Agents SDK - Core Function Calling

## Overview

**OpenAI Agents SDK** demonstrates building AI agents using the core OpenAI ChatCompletion API with function calling. This is the foundational approach for creating stateless agents with tool execution.

**Key Features**:
- Function/tool calling with ChatCompletion API
- Stateless agent pattern (simpler than Assistants)
- Multi-turn conversations with tool execution
- Direct control over message flow
- Production-ready and flexible

**Example File**: `examples/openai_agent_example.py`

---

## Installation

```bash
pip install openai>=1.0.0
```

---

## Quick Start

### Simple Function Calling Agent

```python
from openai import OpenAI
import json

client = OpenAI(api_key="your-api-key")

# Define a tool function
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

# Define tool schema
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name"
                }
            },
            "required": ["location"]
        }
    }
}]

# Create conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather in San Francisco?"}
]

# Call API with tools
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Check if function was called
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    # Execute function
    result = get_weather(**function_args)

    # Add function result to conversation
    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": function_name,
        "content": result
    })

    # Get final response
    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    print(final_response.choices[0].message.content)
```

---

## Multi-Turn Function Calling

### Handling Multiple Tool Calls

```python
def run_agent(user_message: str, tools: list, available_functions: dict):
    """Run agent with multi-turn function calling."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]

    max_iterations = 5
    for iteration in range(max_iterations):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:
            # Add assistant message
            messages.append(assistant_message)

            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Execute function
                function_to_call = available_functions[function_name]
                result = function_to_call(**function_args)

                # Add result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": result
                })
        else:
            # No more tool calls, return final response
            return assistant_message.content

    return "Max iterations reached"
```

---

## Multiple Tools

### Agent with Multiple Functions

```python
# Define multiple tools
def get_weather(location: str) -> str:
    """Get weather."""
    return f"Weather in {location}: Sunny, 72°F"

def calculate(expression: str) -> str:
    """Calculate math expression."""
    return f"{expression} = {eval(expression)}"

def search_database(query: str) -> str:
    """Search database."""
    return f"Results for {query}: [information here]"

# Map functions
available_functions = {
    "get_weather": get_weather,
    "calculate": calculate,
    "search_database": search_database
}

# Define tool schemas
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "Search database for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    }
]

# Agent can now use all three tools
response = run_agent(
    "What's the weather in Tokyo and calculate 25 * 4?",
    tools,
    available_functions
)
```

---

## Evaluation with Custom-Evals

### Comprehensive Evaluation

```python
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM

# Run agent
query = "What's the weather in San Francisco?"
response = run_agent(query, tools, available_functions)

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
        "input": query,
        "output": response
    })
    scores[name] = score
    print(f"{name.capitalize()}: {score.label} ({score.score:.2f})")
    print(f"  Explanation: {score.explanation}")
```

---

## Testing Examples

### Test Function Calling

```python
def test_function_calling():
    """Test that agent calls the right function."""
    query = "What's the weather in New York?"
    result = run_agent(query, tools, available_functions)

    assert "weather" in result.lower()
    assert "New York" in result or "sunny" in result.lower()

    # Evaluate
    scores = evaluate(query, result)
    assert scores["relevance"].score >= 0.7

def test_multi_step():
    """Test multi-step reasoning."""
    query = "Get the weather in London and calculate 100 / 5"
    result = run_agent(query, tools, available_functions)

    # Should mention both weather and calculation
    assert "weather" in result.lower() or "London" in result
    assert "20" in result  # Result of 100/5

    scores = evaluate(query, result)
    assert scores["coherence"].score >= 0.7
```

---

## Best Practices

### 1. Clear Function Descriptions

```python
# Good: Detailed description
{
    "name": "get_order_status",
    "description": "Retrieve the current status of a customer order. Use this when the user asks about order status, shipping, tracking, or delivery information.",
    "parameters": {...}
}

# Avoid: Vague description
{
    "name": "get_order",
    "description": "Get order",
    "parameters": {...}
}
```

### 2. Validate Function Arguments

```python
def get_weather(location: str) -> str:
    """Get weather with validation."""
    # Validate input
    if not location or not isinstance(location, str):
        return "Error: Invalid location"

    # Get weather
    weather_data = {...}
    return weather_data.get(location, "Location not found")
```

### 3. Handle Errors Gracefully

```python
def calculate(expression: str) -> str:
    """Safe calculation."""
    try:
        # Validate expression
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters"

        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### 4. Limit Iterations

```python
# Prevent infinite loops
max_iterations = 5
for iteration in range(max_iterations):
    # ... function calling logic
    if no_more_tool_calls:
        break
```

---

## Use Cases

### Data Retrieval Agent

```python
# Agent that fetches data from multiple sources
tools = [get_database, get_api, get_file]
agent = OpenAIFunctionAgent(tools=tools)
```

### Calculation Agent

```python
# Agent for mathematical operations
tools = [calculate, convert_units, statistical_analysis]
agent = OpenAIFunctionAgent(tools=tools)
```

### Information Lookup

```python
# Agent for searching and retrieving information
tools = [search_docs, query_database, web_search]
agent = OpenAIFunctionAgent(tools=tools)
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
                    return False, f"High {metric}"
            else:
                if scores[metric].score < threshold:
                    return False, f"Low {metric}"

    return True, "All checks passed"
```

---

## Troubleshooting

### Issue: Function not being called

**Solution**: Improve function description and examples

```python
{
    "name": "get_weather",
    "description": "Get current weather. Use this when user asks about weather, temperature, forecast, or conditions in a location.",
    "parameters": {...}
}
```

### Issue: Wrong arguments passed

**Solution**: Add detailed parameter descriptions

```python
"parameters": {
    "type": "object",
    "properties": {
        "location": {
            "type": "string",
            "description": "City name (e.g., 'San Francisco', 'New York', 'London'). Do not include country unless ambiguous."
        }
    }
}
```

### Issue: Infinite loops

**Solution**: Set max_iterations and add termination logic

```python
max_iterations = 5
for i in range(max_iterations):
    if not assistant_message.tool_calls:
        break  # Exit when no more tools needed
```

---

## Comparison with Other OpenAI Options

| Feature | Core SDK | Assistants API | Swarm |
|---------|----------|----------------|-------|
| Complexity | Low | Medium | Very Low |
| State Management | Manual | Automatic (Threads) | Custom |
| Function Calling | ✅ | ✅ | ✅ |
| Persistent Context | Manual | ✅ Built-in | Manual |
| Code Interpreter | ❌ | ✅ | ❌ |
| Multi-Agent | Custom | ❌ | ✅ |
| Best For | Custom agents | Chatbots | Routing |

---

## Resources

- **OpenAI API Docs**: https://platform.openai.com/docs/guides/function-calling
- **Function Calling Guide**: https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models
- **Example File**: `examples/openai_agent_example.py`

---

## Next Steps

1. Install OpenAI: `pip install openai>=1.0.0`
2. Run example: `python examples/openai_agent_example.py`
3. Define your own functions
4. Experiment with multi-turn conversations
5. Add custom evaluation

**See Also**:
- [OpenAI Assistants](openai-assistants.md) - Persistent threads
- [OpenAI Swarm](openai-swarm.md) - Multi-agent coordination
- [PydanticAI](pydanticai.md) - Type-safe agents
