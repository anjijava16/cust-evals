# Autogen (Microsoft) - Multi-Agent Conversations

## Overview

**Autogen** is Microsoft's framework for building multi-agent conversational AI systems with support for code execution and automated problem-solving.

**Key Features**:
- Multi-agent conversations
- Code execution capabilities
- Group chat management
- Function calling
- Human-in-the-loop support

**Example File**: `examples/autogen_agent_example.py`

---

## Installation

```bash
pip install pyautogen
```

---

## Quick Start

### Simple Two-Agent System

```python
import autogen
from autogen import AssistantAgent, UserProxyAgent

# Configure LLM
llm_config = {
    "config_list": [{
        "model": "gpt-4o-mini",
        "api_key": "your-openai-key",
    }],
    "temperature": 0,
}

# Create assistant agent
assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="You are a helpful AI assistant."
)

# Create user proxy (executes code and represents user)
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # No human input for automation
    max_consecutive_auto_reply=3,
    code_execution_config={
        "work_dir": "autogen_workspace",
        "use_docker": False,
    }
)

# Initiate conversation
user_proxy.initiate_chat(
    assistant,
    message="What is machine learning?"
)

# Get response
conversation = user_proxy.chat_messages[assistant]
response = conversation[-1]["content"]
print(response)
```

---

## Multi-Agent Group Chat

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Create specialized agents
researcher = AssistantAgent(
    name="researcher",
    llm_config=llm_config,
    system_message="You are a research specialist."
)

analyst = AssistantAgent(
    name="analyst",
    llm_config=llm_config,
    system_message="You are a data analyst."
)

writer = AssistantAgent(
    name="writer",
    llm_config=llm_config,
    system_message="You are a technical writer."
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    code_execution_config=False
)

# Create group chat
groupchat = GroupChat(
    agents=[user_proxy, researcher, analyst, writer],
    messages=[],
    max_round=10
)

# Create manager
manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

# Run group conversation
user_proxy.initiate_chat(
    manager,
    message="Research and write about AI trends"
)
```

---

## Function Calling

```python
def get_stock_price(symbol: str) -> str:
    """Get stock price for a symbol."""
    prices = {
        "AAPL": "$185.50",
        "GOOGL": "$142.30"
    }
    return prices.get(symbol, f"Price not available")

# Create assistant with functions
assistant = AssistantAgent(
    name="financial_assistant",
    llm_config=llm_config,
    system_message="You help with financial information."
)

# Register functions
assistant.register_function(
    function_map={
        "get_stock_price": get_stock_price
    }
)

# Use assistant
user_proxy.initiate_chat(
    assistant,
    message="What's the price of AAPL?"
)
```

---

## Code Execution

```python
# Enable code execution
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": False,  # Set True for safer execution
        "timeout": 60,
    }
)

# Ask agent to write and execute code
user_proxy.initiate_chat(
    assistant,
    message="Calculate the sum of numbers from 1 to 100"
)
```

---

## Evaluation with Custom-Evals

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

# Run agent
user_proxy.initiate_chat(assistant, message="What is AI?")

# Get response
conversation = user_proxy.chat_messages[assistant]
response = conversation[-1]["content"]

# Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

coherence = CoherenceEvaluator(eval_llm)
score = coherence.evaluate({
    "input": "What is AI?",
    "output": response
})

print(f"Coherence: {score.label} ({score.score:.2f})")
print(f"Explanation: {score.explanation}")
```

---

## Testing Examples

### Test Two-Agent System

```python
def test_two_agent():
    system = AutogenTwoAgentSystem()

    result = system.run("Explain quantum computing")

    assert result["success"]
    assert len(result["response"]) > 0

    scores = system.evaluate(
        "Explain quantum computing",
        result["response"]
    )

    assert scores["coherence"].score >= 0.7
    assert scores["relevance"].score >= 0.7
```

### Test Group Chat

```python
def test_group_chat():
    system = AutogenGroupChatSystem()

    result = system.run("Research AI in healthcare")

    assert result["success"]
    assert result["total_messages"] > 2

    scores = system.evaluate(
        "Research AI in healthcare",
        result["response"]
    )

    assert all(s.score >= 0.7 for s in scores.values())
```

---

## Best Practices

### 1. Conversation Management

```python
# Limit auto-replies to prevent infinite loops
user_proxy = UserProxyAgent(
    name="user_proxy",
    max_consecutive_auto_reply=5,  # Max 5 auto-replies
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "")
)
```

### 2. Code Execution Safety

```python
# Use Docker for safe code execution
code_execution_config={
    "work_dir": "workspace",
    "use_docker": True,  # Safer!
    "timeout": 60,
}
```

### 3. Group Chat Control

```python
# Control conversation flow
groupchat = GroupChat(
    agents=[user_proxy, agent1, agent2],
    messages=[],
    max_round=10,  # Limit rounds
    speaker_selection_method="auto"  # or "manual", "round_robin"
)
```

### 4. Error Handling

```python
def run_agent_safely(assistant, user_proxy, message):
    try:
        user_proxy.initiate_chat(assistant, message=message)
        conversation = user_proxy.chat_messages[assistant]
        return conversation[-1]["content"]
    except Exception as e:
        print(f"Error: {e}")
        return None
```

---

## Use Cases

### Research Assistant

```python
research_assistant = AssistantAgent(
    name="research_assistant",
    llm_config=llm_config,
    system_message="""You are a research assistant.
    Help users with research tasks, data analysis, and insights."""
)
```

### Code Generation

```python
coding_assistant = AssistantAgent(
    name="coding_assistant",
    llm_config=llm_config,
    system_message="""You are a coding assistant.
    Write clean, efficient code with explanations."""
)
```

### Problem Solving

```python
# Multi-agent problem solving
groupchat = GroupChat(
    agents=[problem_analyzer, solution_designer, code_writer, tester],
    messages=[],
    max_round=20
)
```

---

## Quality Gates

```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
    "toxicity": 0.2
}

def check_quality(scores):
    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric == "toxicity":
            if scores[metric].score > threshold:
                return False
        else:
            if scores[metric].score < threshold:
                return False
    return True
```

---

## Troubleshooting

### Issue: Infinite conversation loops

**Solution**: Set `max_consecutive_auto_reply` and use termination conditions

```python
user_proxy = UserProxyAgent(
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "")
)
```

### Issue: Code execution errors

**Solution**: Use Docker and set proper timeouts

```python
code_execution_config={
    "use_docker": True,
    "timeout": 60
}
```

### Issue: High API costs

**Solution**: Limit conversation rounds and cache responses

```python
groupchat = GroupChat(
    agents=agents,
    max_round=5  # Limit rounds
)
```

---

## Resources

- **Official Docs**: https://microsoft.github.io/autogen/
- **GitHub**: https://github.com/microsoft/autogen
- **Example File**: `examples/autogen_agent_example.py`
- **API Reference**: See custom-evals integration

---

## Next Steps

1. Install Autogen: `pip install pyautogen`
2. Run example: `python examples/autogen_agent_example.py`
3. Study multi-agent patterns
4. Experiment with code execution
5. Build your own agent system

**See Also**:
- [CrewAI](crewai.md) - Role-based orchestration
- [OpenAI Swarm](openai-swarm.md) - Lightweight coordination
- [Multi-Agent System](multi-agent.md) - Custom orchestration
