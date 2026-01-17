# OpenAI Swarm - Lightweight Multi-Agent Orchestration

## Overview

**OpenAI Swarm** is an experimental, lightweight multi-agent coordination framework from OpenAI. It focuses on agent handoffs and context passing for building scalable multi-agent systems.

**Key Features**:
- Lightweight agent coordination
- Native agent handoffs
- Context passing between agents
- Triage/routing patterns
- Simple, ergonomic API
- Built on OpenAI models

**Example File**: `examples/openai_swarm_agent_example.py`

---

## Installation

```bash
pip install git+https://github.com/openai/swarm.git
```

**Note**: Swarm is experimental and requires OpenAI API access.

---

## Quick Start

### Simple Two-Agent Swarm

```python
from swarm import Swarm, Agent

# Create agents
sales_agent = Agent(
    name="Sales Agent",
    instructions="You help customers with product purchases and sales inquiries.",
    model="gpt-4o-mini"
)

support_agent = Agent(
    name="Support Agent",
    instructions="You help customers with technical support issues.",
    model="gpt-4o-mini"
)

# Create client
client = Swarm()

# Run conversation
messages = [{"role": "user", "content": "I want to buy a product"}]
response = client.run(agent=sales_agent, messages=messages)

print(response.messages[-1]["content"])
```

---

## Agent Handoffs

### Transfer Functions

```python
def transfer_to_sales():
    """Transfer conversation to sales agent."""
    return sales_agent

def transfer_to_support():
    """Transfer conversation to support agent."""
    return support_agent

# Triage agent with transfer functions
triage_agent = Agent(
    name="Triage Agent",
    instructions="""You are a customer service triage agent.
    Route customers to the appropriate specialist.""",
    functions=[transfer_to_sales, transfer_to_support],
    model="gpt-4o-mini"
)

# Client automatically handles handoffs
response = client.run(
    agent=triage_agent,
    messages=[{"role": "user", "content": "My product is broken"}]
)

# Swarm will transfer to support_agent automatically
```

---

## Context Passing

### Passing Context Between Agents

```python
def transfer_to_analyst(order_id: str, customer_name: str):
    """Transfer to analyst with context."""
    return Agent(
        name="Data Analyst",
        instructions=f"""You are analyzing order {order_id} for customer {customer_name}.
        Provide detailed insights.""",
        model="gpt-4o-mini"
    )

customer_service = Agent(
    name="Customer Service",
    instructions="Help customers and gather information",
    functions=[transfer_to_analyst],
    model="gpt-4o-mini"
)

# Context is automatically passed through function parameters
response = client.run(
    agent=customer_service,
    messages=[{"role": "user", "content": "Analyze order #12345 for John Smith"}]
)
```

---

## Tool Functions

### Adding Tools to Agents

```python
def get_order_status(order_id: str) -> str:
    """Get the status of an order."""
    orders = {
        "12345": "Shipped - Arriving Tomorrow",
        "67890": "Processing"
    }
    return orders.get(order_id, "Order not found")

def check_inventory(product_name: str) -> str:
    """Check product inventory."""
    inventory = {
        "laptop": "5 in stock",
        "mouse": "Out of stock"
    }
    return inventory.get(product_name.lower(), "Product not found")

# Agent with tools
agent = Agent(
    name="Customer Service",
    instructions="Help customers with orders and inventory",
    functions=[get_order_status, check_inventory],
    model="gpt-4o-mini"
)

response = client.run(
    agent=agent,
    messages=[{"role": "user", "content": "What's the status of order 12345?"}]
)
```

---

## Multi-Agent Routing System

### Complete Routing Example

```python
from swarm import Swarm, Agent

# Create specialized agents
def transfer_to_billing():
    return billing_agent

def transfer_to_technical():
    return technical_agent

def transfer_to_general():
    return general_agent

billing_agent = Agent(
    name="Billing Specialist",
    instructions="Handle billing, payments, and invoices",
    model="gpt-4o-mini"
)

technical_agent = Agent(
    name="Technical Support",
    instructions="Provide technical assistance and troubleshooting",
    model="gpt-4o-mini"
)

general_agent = Agent(
    name="General Support",
    instructions="Handle general inquiries",
    model="gpt-4o-mini"
)

# Triage agent
triage = Agent(
    name="Triage",
    instructions="""Route customers to the appropriate department:
    - Billing issues → Billing Specialist
    - Technical problems → Technical Support
    - General questions → General Support""",
    functions=[transfer_to_billing, transfer_to_technical, transfer_to_general],
    model="gpt-4o-mini"
)

# Run
client = Swarm()
response = client.run(
    agent=triage,
    messages=[{"role": "user", "content": "I have a billing question"}]
)
```

---

## Evaluation with Custom-Evals

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM
from swarm import Swarm, Agent

# Run swarm
agent = Agent(name="Assistant", instructions="Be helpful", model="gpt-4o-mini")
client = Swarm()
response = client.run(
    agent=agent,
    messages=[{"role": "user", "content": "Explain quantum computing"}]
)

# Get final response
final_message = response.messages[-1]["content"]

# Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

coherence = CoherenceEvaluator(eval_llm)
score = coherence.evaluate({
    "input": "Explain quantum computing",
    "output": final_message
})

relevance = RelevanceEvaluator(eval_llm)
rel_score = relevance.evaluate({
    "input": "Explain quantum computing",
    "output": final_message
})

print(f"Coherence: {score.label} ({score.score:.2f})")
print(f"Relevance: {rel_score.label} ({rel_score.score:.2f})")
```

---

## Testing Examples

### Test Simple Swarm

```python
def test_simple_swarm():
    system = SimpleSwarm()

    result = system.run("What is machine learning?")

    assert result["success"]
    assert len(result["response"]) > 0
    assert result["agent_name"] == "Assistant"

    scores = system.evaluate(
        "What is machine learning?",
        result["response"]
    )

    assert scores["coherence"].score >= 0.7
    assert scores["relevance"].score >= 0.7
```

### Test Multi-Agent Routing

```python
def test_routing():
    system = MultiAgentSwarm()

    # Test routing to sales
    result = system.run("I want to buy a laptop")
    assert "sales" in result["final_agent"].lower()

    # Test routing to support
    result = system.run("My device is broken")
    assert "support" in result["final_agent"].lower()

    # Evaluate
    scores = system.evaluate("I want to buy a laptop", result["response"])
    assert all(s.score >= 0.7 for s in scores.values())
```

---

## Best Practices

### 1. Clear Agent Instructions

```python
# Good: Specific, actionable instructions
agent = Agent(
    name="Sales Agent",
    instructions="""You are a sales specialist for electronics.
    - Help customers find the right products
    - Provide accurate pricing and availability
    - Be friendly and professional
    - Transfer to support for technical issues""",
    model="gpt-4o-mini"
)

# Avoid: Vague instructions
agent = Agent(
    name="Agent",
    instructions="Help customers",
    model="gpt-4o-mini"
)
```

### 2. Efficient Transfer Functions

```python
# Good: Return agent with context
def transfer_with_context(customer_id: str):
    return Agent(
        name="Account Manager",
        instructions=f"Handle customer {customer_id}",
        model="gpt-4o-mini"
    )

# Good: Simple transfer
def transfer_to_support():
    return support_agent
```

### 3. Tool Function Design

```python
# Good: Clear function with type hints
def get_order(order_id: str) -> str:
    """Get order details by ID.

    Args:
        order_id: The order ID to look up

    Returns:
        Order status and details
    """
    return f"Order {order_id}: Shipped"

# The docstring helps the LLM understand when to use the function
```

### 4. Message History Management

```python
# Keep conversation history
messages = [{"role": "user", "content": "Hello"}]

response = client.run(agent=agent, messages=messages)

# Add response to history for continuity
messages.extend(response.messages)

# Continue conversation
response = client.run(agent=agent, messages=messages)
```

---

## Use Cases

### Customer Service Routing

```python
# Multi-tier support system
triage → [sales, support, billing, returns]
```

### Sales Workflow

```python
# Lead qualification to closing
lead_qualifier → product_specialist → pricing_agent → closer
```

### Technical Support

```python
# Escalation workflow
tier1_support → tier2_support → engineering
```

### Content Creation

```python
# Multi-step content workflow
researcher → writer → editor → publisher
```

---

## Quality Gates

```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
    "toxicity": 0.2
}

def validate_swarm_output(response, scores):
    """Validate Swarm output meets quality standards."""
    if not response.get("success"):
        return False, "Swarm execution failed"

    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric in scores:
            if metric == "toxicity":
                if scores[metric].score > threshold:
                    return False, f"High toxicity: {scores[metric].score:.2f}"
            else:
                if scores[metric].score < threshold:
                    return False, f"{metric} below threshold"

    return True, "All checks passed"
```

---

## Performance Tips

### 1. Minimize Agent Count

```python
# Good: 2-4 agents for most use cases
triage → [sales, support]

# Avoid: Too many agents (slower, more expensive)
triage → [agent1, agent2, ..., agent10]
```

### 2. Use Appropriate Models

```python
# Simple routing: Use gpt-4o-mini
triage = Agent(name="Triage", model="gpt-4o-mini", ...)

# Complex reasoning: Use gpt-4
analyst = Agent(name="Analyst", model="gpt-4", ...)
```

### 3. Batch Similar Requests

```python
# Process multiple similar requests together
for query in customer_queries:
    response = client.run(agent=agent, messages=[{"role": "user", "content": query}])
```

---

## Troubleshooting

### Issue: Agents not transferring correctly

**Solution**: Ensure transfer functions are included in agent's `functions` list

```python
# Correct
triage = Agent(
    name="Triage",
    instructions="Route customers",
    functions=[transfer_to_sales, transfer_to_support],  # Include functions!
    model="gpt-4o-mini"
)
```

### Issue: Context not passing between agents

**Solution**: Use function parameters to pass context

```python
def transfer_to_agent(customer_id: str, order_id: str):
    """Pass context via parameters."""
    return Agent(
        name="Agent",
        instructions=f"Handle customer {customer_id}, order {order_id}",
        model="gpt-4o-mini"
    )
```

### Issue: Infinite handoff loops

**Solution**: Add clear instructions about when NOT to transfer

```python
agent = Agent(
    name="Support",
    instructions="""Handle technical support.
    Only transfer to sales for purchasing questions.
    Do NOT transfer back to triage.""",
    model="gpt-4o-mini"
)
```

---

## Comparison with Other Frameworks

| Feature | Swarm | Autogen | CrewAI |
|---------|-------|---------|--------|
| Complexity | Very Low | Medium | Low |
| Multi-Agent | ✅ | ✅ | ✅ |
| Agent Handoffs | ✅ Native | Custom | Limited |
| Code Execution | ❌ | ✅ | ❌ |
| Learning Curve | Very Low | Medium | Low |
| Best For | Routing, Customer Service | Research, Code | Workflows |

---

## Resources

- **GitHub**: https://github.com/openai/swarm
- **OpenAI Cookbook**: https://cookbook.openai.com/
- **Example File**: `examples/openai_swarm_agent_example.py`
- **API Docs**: https://platform.openai.com/docs

---

## Next Steps

1. Install Swarm: `pip install git+https://github.com/openai/swarm.git`
2. Run example: `python examples/openai_swarm_agent_example.py`
3. Create a simple triage agent
4. Experiment with agent handoffs
5. Build a multi-agent routing system

**See Also**:
- [Autogen](autogen.md) - Multi-agent conversations
- [CrewAI](crewai.md) - Role-based orchestration
- [OpenAI Assistants](openai-assistants.md) - Persistent threads
