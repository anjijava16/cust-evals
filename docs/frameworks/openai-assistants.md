# OpenAI Assistants API - Persistent AI Assistants

## Overview

**OpenAI Assistants API** is the official OpenAI SDK for building AI assistants with persistent conversation threads, function calling, and code interpreter capabilities.

**Key Features**:
- Persistent conversation threads
- Function calling
- Code interpreter
- File uploads and retrieval
- Official OpenAI support
- Production-ready

**Example File**: `examples/openai_assistants_example.py`

---

## Installation

```bash
pip install openai>=1.0.0
```

---

## Quick Start

### Simple Assistant

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Create assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a helpful math tutor. Answer questions clearly.",
    model="gpt-4o-mini"
)

# Create thread
thread = client.beta.threads.create()

# Add message
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is 25 * 4?"
)

# Run assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Wait for completion
import time
while run.status in ["queued", "in_progress"]:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

# Get response
messages = client.beta.threads.messages.list(thread_id=thread.id)
response = messages.data[0].content[0].text.value
print(response)
```

---

## Function Calling

### Add Tools to Assistant

```python
# Define function
def get_weather(location: str) -> str:
    """Get weather for a location."""
    weather_data = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Cloudy, 65°F"
    }
    return weather_data.get(location, "Weather data not available")

# Create assistant with function
assistant = client.beta.assistants.create(
    name="Weather Assistant",
    instructions="You help users get weather information.",
    model="gpt-4o-mini",
    tools=[{
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
)

# Run with function calling
thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What's the weather in San Francisco?"
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Handle function calls
while run.status in ["queued", "in_progress", "requires_action"]:
    if run.status == "requires_action":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        tool_outputs = []

        for tool_call in tool_calls:
            if tool_call.function.name == "get_weather":
                import json
                args = json.loads(tool_call.function.arguments)
                result = get_weather(args["location"])
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": result
                })

        # Submit tool outputs
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )

    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

# Get final response
messages = client.beta.threads.messages.list(thread_id=thread.id)
response = messages.data[0].content[0].text.value
```

---

## Code Interpreter

### Enable Code Execution

```python
# Create assistant with code interpreter
assistant = client.beta.assistants.create(
    name="Data Analyst",
    instructions="You analyze data and create visualizations.",
    model="gpt-4o-mini",
    tools=[{"type": "code_interpreter"}]
)

# Create thread and ask for analysis
thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Calculate the sum of numbers 1 to 100 and show me the result."
)

# Run with code interpreter
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

# Get response (includes code execution results)
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
```

---

## Thread Management

### Persistent Conversations

```python
# Create thread once
thread = client.beta.threads.create()
thread_id = thread.id  # Store this for later

# Continue conversation across multiple sessions
def continue_conversation(thread_id: str, message: str):
    """Add message to existing thread."""
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant.id
    )

    # Wait and get response
    while run.status in ["queued", "in_progress"]:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value

# Use it
response1 = continue_conversation(thread_id, "What is Python?")
response2 = continue_conversation(thread_id, "Tell me more about it")  # Maintains context
```

---

## Evaluation with Custom-Evals

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

# Run assistant
# ... (create and run assistant as shown above)

# Get response
messages = client.beta.threads.messages.list(thread_id=thread.id)
response = messages.data[0].content[0].text.value

# Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

coherence = CoherenceEvaluator(eval_llm)
score = coherence.evaluate({
    "input": "What is machine learning?",
    "output": response
})

relevance = RelevanceEvaluator(eval_llm)
rel_score = relevance.evaluate({
    "input": "What is machine learning?",
    "output": response
})

print(f"Coherence: {score.label} ({score.score:.2f})")
print(f"Relevance: {rel_score.label} ({rel_score.score:.2f})")
print(f"Explanation: {score.explanation}")
```

---

## Testing Examples

### Test Simple Assistant

```python
def test_simple_assistant():
    system = SimpleAssistant()

    result = system.run("What is artificial intelligence?")

    assert result["success"]
    assert len(result["response"]) > 0
    assert result["thread_id"] is not None

    scores = system.evaluate(
        "What is artificial intelligence?",
        result["response"]
    )

    assert scores["coherence"].score >= 0.7
    assert scores["relevance"].score >= 0.7
```

### Test Function Calling

```python
def test_function_calling():
    system = FunctionCallingAssistant()

    result = system.run("What's the stock price of AAPL?")

    assert result["success"]
    assert "function_calls" in result
    assert len(result["function_calls"]) > 0
    assert "$" in result["response"]  # Contains price

    scores = system.evaluate(
        "What's the stock price of AAPL?",
        result["response"]
    )

    assert scores["relevance"].score >= 0.7
```

### Test Code Interpreter

```python
def test_code_interpreter():
    system = CodeInterpreterAssistant()

    result = system.run("Calculate the factorial of 10")

    assert result["success"]
    assert "3628800" in str(result["response"])  # Correct factorial

    scores = system.evaluate(
        "Calculate the factorial of 10",
        result["response"]
    )

    assert scores["correctness"].score >= 0.8
```

---

## Best Practices

### 1. Assistant Configuration

```python
# Good: Clear instructions and appropriate tools
assistant = client.beta.assistants.create(
    name="Customer Support Bot",
    instructions="""You are a helpful customer support assistant.
    - Be polite and professional
    - Use available tools to look up information
    - Provide accurate answers
    - Escalate complex issues to human agents""",
    tools=[{"type": "function", "function": {...}}],
    model="gpt-4o-mini"
)

# Avoid: Vague instructions
assistant = client.beta.assistants.create(
    name="Bot",
    instructions="Help users",
    model="gpt-4o-mini"
)
```

### 2. Error Handling

```python
def run_assistant_safely(thread_id, assistant_id, max_retries=3):
    """Run assistant with error handling."""
    for attempt in range(max_retries):
        try:
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )

            # Wait for completion with timeout
            timeout = 60  # seconds
            elapsed = 0
            while run.status in ["queued", "in_progress"]:
                if elapsed > timeout:
                    raise TimeoutError("Assistant run timed out")
                time.sleep(1)
                elapsed += 1
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )

            if run.status == "completed":
                return run
            else:
                raise Exception(f"Run failed with status: {run.status}")

        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 3. Thread Cleanup

```python
# Delete old threads to save resources
def cleanup_old_threads(days_old=30):
    """Delete threads older than specified days."""
    threads = client.beta.threads.list()
    for thread in threads.data:
        # Check thread age and delete if old
        client.beta.threads.delete(thread.id)
```

### 4. Function Schema Design

```python
# Good: Clear, well-documented function
{
    "type": "function",
    "function": {
        "name": "get_order_status",
        "description": "Retrieve the current status of a customer order by order ID",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The unique order identifier (e.g., 'ORD-12345')"
                }
            },
            "required": ["order_id"]
        }
    }
}
```

---

## Use Cases

### Customer Support Chatbot

```python
# Persistent support conversations
assistant = client.beta.assistants.create(
    name="Support Bot",
    instructions="Help customers with orders, returns, and product info",
    tools=[...],  # Order lookup, inventory check, etc.
    model="gpt-4o-mini"
)
```

### Personal Assistant

```python
# Multi-session personal assistant
assistant = client.beta.assistants.create(
    name="Personal Assistant",
    instructions="Help user manage tasks, calendar, and reminders",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini"
)
```

### Data Analysis Bot

```python
# Code interpreter for data analysis
assistant = client.beta.assistants.create(
    name="Data Analyst",
    instructions="Analyze data and create visualizations",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini"
)
```

---

## Quality Gates

```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
    "correctness": 0.8,
    "toxicity": 0.2
}

def validate_assistant_output(result, scores):
    """Validate assistant output meets quality standards."""
    if not result.get("success"):
        return False, "Assistant execution failed"

    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric in scores:
            if metric == "toxicity":
                if scores[metric].score > threshold:
                    return False, f"High toxicity detected"
            else:
                if scores[metric].score < threshold:
                    return False, f"{metric} below threshold"

    return True, "All checks passed"
```

---

## Troubleshooting

### Issue: Run stuck in "in_progress"

**Solution**: Add timeout and retry logic

```python
timeout = 60
start_time = time.time()
while run.status in ["queued", "in_progress"]:
    if time.time() - start_time > timeout:
        client.beta.threads.runs.cancel(thread_id=thread.id, run_id=run.id)
        raise TimeoutError("Run timed out")
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
```

### Issue: Function not being called

**Solution**: Improve function descriptions and parameter schemas

```python
# Make description very clear about when to use the function
"description": "Use this function when the user asks about order status, shipping, or delivery"
```

### Issue: High API costs

**Solution**: Use gpt-4o-mini and implement caching

```python
# Use mini model for most tasks
model="gpt-4o-mini"

# Cache frequently accessed threads locally
```

---

## Resources

- **Official Docs**: https://platform.openai.com/docs/assistants
- **API Reference**: https://platform.openai.com/docs/api-reference/assistants
- **Example File**: `examples/openai_assistants_example.py`
- **OpenAI Cookbook**: https://cookbook.openai.com/

---

## Next Steps

1. Install OpenAI SDK: `pip install openai>=1.0.0`
2. Run example: `python examples/openai_assistants_example.py`
3. Create your first assistant
4. Experiment with function calling
5. Build a persistent chatbot

**See Also**:
- [OpenAI Swarm](openai-swarm.md) - Multi-agent coordination
- [Autogen](autogen.md) - Multi-agent conversations
- [PydanticAI](pydanticai.md) - Type-safe agents
