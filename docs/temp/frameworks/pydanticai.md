# PydanticAI - Type-Safe Agent Development

## Overview

**PydanticAI** is Pydantic's framework for building production-grade AI agents with type safety, structured outputs, and validation powered by Pydantic models.

**Key Features**:
- Type-safe agent development
- Structured outputs with Pydantic models
- Tool calling with validation
- Async and sync support
- Multi-model support
- Production-ready architecture

**Example File**: `examples/pydanticai_agent_example.py`

---

## Installation

```bash
pip install pydantic-ai pydantic>=2.0
```

---

## Quick Start

### Simple Agent

```python
from pydantic_ai import Agent

# Create agent
agent = Agent(
    'openai:gpt-4o-mini',
    system_prompt='You are a helpful assistant.'
)

# Run agent (sync)
result = agent.run_sync('What is machine learning?')
print(result.data)

# Run agent (async)
import asyncio

async def main():
    result = await agent.run('What is machine learning?')
    print(result.data)

asyncio.run(main())
```

---

## Structured Outputs

### Define Pydantic Models

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# Define output schema
class WeatherInfo(BaseModel):
    city: str = Field(description="City name")
    temperature: str = Field(description="Temperature")
    condition: str = Field(description="Weather condition")
    humidity: int | None = Field(None, description="Humidity percentage")

# Create agent with structured output
agent = Agent(
    'openai:gpt-4o-mini',
    result_type=WeatherInfo,
    system_prompt='Extract weather information from user queries.'
)

# Run - returns typed Pydantic model
result = agent.run_sync('The weather in San Francisco is sunny, 72 degrees')
weather: WeatherInfo = result.data

print(f"City: {weather.city}")
print(f"Temperature: {weather.temperature}")
print(f"Condition: {weather.condition}")
```

---

## Tool Calling

### Add Tools to Agent

```python
from pydantic_ai import Agent, RunContext

# Define tools as functions
def get_stock_price(symbol: str) -> str:
    """Get current stock price for a symbol."""
    prices = {
        "AAPL": "$185.50",
        "GOOGL": "$142.30",
        "MSFT": "$378.90"
    }
    return prices.get(symbol.upper(), "Symbol not found")

def calculate_portfolio(symbols: list[str]) -> dict:
    """Calculate total portfolio value."""
    total = 0
    for symbol in symbols:
        # Simplified calculation
        total += 100  # Mock value
    return {"total_value": f"${total}", "count": len(symbols)}

# Create agent with tools
agent = Agent(
    'openai:gpt-4o-mini',
    system_prompt='You help with stock information.',
    tools=[get_stock_price, calculate_portfolio]
)

# Agent automatically calls tools when needed
result = agent.run_sync("What's the price of AAPL?")
print(result.data)
```

---

## Context and State

### Using RunContext

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

# Define context/state
@dataclass
class UserContext:
    user_id: str
    name: str
    preferences: dict

def get_user_info(ctx: RunContext[UserContext]) -> str:
    """Get information about the current user."""
    return f"User: {ctx.deps.name} (ID: {ctx.deps.user_id})"

def get_preference(ctx: RunContext[UserContext], key: str) -> str:
    """Get user preference."""
    return ctx.deps.preferences.get(key, "Not set")

# Create agent
agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=UserContext,
    tools=[get_user_info, get_preference]
)

# Run with context
user = UserContext(
    user_id="123",
    name="Alice",
    preferences={"theme": "dark", "language": "en"}
)

result = agent.run_sync("What's my theme preference?", deps=user)
print(result.data)
```

---

## Multi-Step Workflows

### Chain Multiple Agents

```python
from pydantic import BaseModel
from pydantic_ai import Agent

# Step 1: Research
class ResearchResult(BaseModel):
    topic: str
    findings: list[str]
    sources: list[str]

research_agent = Agent(
    'openai:gpt-4o-mini',
    result_type=ResearchResult,
    system_prompt='You are a research specialist.'
)

# Step 2: Analysis
class AnalysisResult(BaseModel):
    summary: str
    key_insights: list[str]
    recommendations: list[str]

analysis_agent = Agent(
    'openai:gpt-4o-mini',
    result_type=AnalysisResult,
    system_prompt='You analyze research and provide insights.'
)

# Workflow
async def research_workflow(topic: str):
    # Research
    research = await research_agent.run(f"Research {topic}")

    # Analysis
    analysis = await analysis_agent.run(
        f"Analyze these findings: {research.data.findings}"
    )

    return {
        "research": research.data,
        "analysis": analysis.data
    }

# Run
import asyncio
result = asyncio.run(research_workflow("quantum computing"))
```

---

## Validation and Error Handling

### Built-in Pydantic Validation

```python
from pydantic import BaseModel, Field, field_validator

class OrderRequest(BaseModel):
    product_id: str = Field(min_length=3, max_length=20)
    quantity: int = Field(gt=0, le=100)
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')

    @field_validator('product_id')
    @classmethod
    def validate_product_id(cls, v: str) -> str:
        if not v.startswith('PROD-'):
            raise ValueError('Product ID must start with PROD-')
        return v

# Agent with validation
agent = Agent(
    'openai:gpt-4o-mini',
    result_type=OrderRequest,
    system_prompt='Extract order information from user input.'
)

try:
    result = agent.run_sync('I want to order PROD-12345, quantity 5, email: user@example.com')
    order: OrderRequest = result.data
    print(f"Valid order: {order}")
except Exception as e:
    print(f"Validation error: {e}")
```

---

## Evaluation with Custom-Evals

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM
from pydantic_ai import Agent

# Run agent
agent = Agent('openai:gpt-4o-mini', system_prompt='You are helpful.')
result = agent.run_sync('Explain neural networks')

response = result.data

# Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

coherence = CoherenceEvaluator(eval_llm)
score = coherence.evaluate({
    "input": "Explain neural networks",
    "output": response
})

relevance = RelevanceEvaluator(eval_llm)
rel_score = relevance.evaluate({
    "input": "Explain neural networks",
    "output": response
})

print(f"Coherence: {score.label} ({score.score:.2f})")
print(f"Relevance: {rel_score.label} ({rel_score.score:.2f})")
```

---

## Testing Examples

### Test Simple Agent

```python
def test_simple_agent():
    system = SimplePydanticAgent()

    result = system.run("What is artificial intelligence?")

    assert result["success"]
    assert len(result["response"]) > 0

    scores = system.evaluate(
        "What is artificial intelligence?",
        result["response"]
    )

    assert scores["coherence"].score >= 0.7
```

### Test Structured Output

```python
def test_structured_output():
    system = StructuredOutputAgent()

    result = system.run("Weather in NYC is sunny, 68 degrees, 65% humidity")

    assert result["success"]
    assert isinstance(result["data"], dict)
    assert "city" in result["data"]
    assert "temperature" in result["data"]

    # Validate Pydantic model
    weather = WeatherInfo(**result["data"])
    assert weather.city == "NYC"
```

### Test Tool Calling

```python
def test_tool_agent():
    system = ToolBasedAgent()

    result = system.run("What's the stock price of AAPL?")

    assert result["success"]
    assert "function_calls" in result
    assert len(result["function_calls"]) > 0
    assert "$" in result["response"]

    scores = system.evaluate(
        "What's the stock price of AAPL?",
        result["response"]
    )

    assert scores["correctness"].score >= 0.8
```

---

## Best Practices

### 1. Define Clear Models

```python
# Good: Well-documented Pydantic model
class ProductInfo(BaseModel):
    """Product information from database."""
    id: str = Field(description="Unique product ID", min_length=3)
    name: str = Field(description="Product name")
    price: float = Field(description="Price in USD", gt=0)
    in_stock: bool = Field(description="Availability status")

    @field_validator('price')
    @classmethod
    def round_price(cls, v: float) -> float:
        return round(v, 2)

# Avoid: Minimal validation
class Product(BaseModel):
    id: str
    name: str
    price: float
```

### 2. Use Type Hints

```python
# Good: Full type hints
def get_order(order_id: str) -> dict[str, Any]:
    """Get order details."""
    return {"id": order_id, "status": "shipped"}

# Type hints help PydanticAI understand the tool
agent = Agent(
    'openai:gpt-4o-mini',
    tools=[get_order]
)
```

### 3. Handle Async Properly

```python
# Good: Proper async handling
async def process_requests(requests: list[str]):
    agent = Agent('openai:gpt-4o-mini')
    tasks = [agent.run(req) for req in requests]
    results = await asyncio.gather(*tasks)
    return results

# Run
asyncio.run(process_requests(['query1', 'query2']))
```

### 4. Use Retries

```python
from pydantic_ai import Agent

agent = Agent(
    'openai:gpt-4o-mini',
    retries=3  # Retry on failure
)
```

---

## Use Cases

### Data Extraction

```python
# Extract structured data from text
class InvoiceData(BaseModel):
    invoice_number: str
    date: str
    total: float
    items: list[str]

agent = Agent(
    'openai:gpt-4o-mini',
    result_type=InvoiceData,
    system_prompt='Extract invoice information.'
)
```

### API Integration

```python
# Type-safe API calls
class APIRequest(BaseModel):
    endpoint: str
    method: str
    params: dict

agent = Agent(
    'openai:gpt-4o-mini',
    result_type=APIRequest,
    system_prompt='Convert user requests to API calls.'
)
```

### Form Processing

```python
# Process form inputs with validation
class RegistrationForm(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(ge=18, le=120)

agent = Agent(
    'openai:gpt-4o-mini',
    result_type=RegistrationForm
)
```

---

## Quality Gates

```python
from pydantic import ValidationError

QUALITY_THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
    "correctness": 0.8
}

def validate_pydanticai_output(result, scores, expected_model):
    """Validate PydanticAI output."""
    if not result.get("success"):
        return False, "Agent execution failed"

    # Validate against Pydantic model
    try:
        if expected_model:
            expected_model(**result["data"])
    except ValidationError as e:
        return False, f"Validation error: {e}"

    # Check quality scores
    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric in scores and scores[metric].score < threshold:
            return False, f"{metric} below threshold"

    return True, "All checks passed"
```

---

## Troubleshooting

### Issue: Validation errors

**Solution**: Improve model field descriptions

```python
# Clear descriptions help the LLM generate valid outputs
class Product(BaseModel):
    id: str = Field(
        description="Product ID in format 'PROD-XXXXX' where X is a digit"
    )
    price: float = Field(
        description="Price in USD, must be positive",
        gt=0
    )
```

### Issue: Tool not being called

**Solution**: Add clear docstrings and type hints

```python
def get_weather(location: str) -> str:
    """Get current weather for a location.

    Args:
        location: City name (e.g., 'San Francisco', 'New York')

    Returns:
        Weather description including temperature and conditions
    """
    return f"Weather in {location}: Sunny, 72°F"
```

### Issue: Async errors

**Solution**: Use proper async context

```python
# Correct async usage
async def main():
    agent = Agent('openai:gpt-4o-mini')
    result = await agent.run('query')  # Use await
    return result

# Run
asyncio.run(main())
```

---

## Comparison with Other Frameworks

| Feature | PydanticAI | Autogen | CrewAI | Swarm |
|---------|-----------|---------|--------|-------|
| Type Safety | ✅✅ | ❌ | ❌ | ❌ |
| Structured Output | ✅✅ | ❌ | ❌ | ❌ |
| Validation | ✅✅ | ❌ | ❌ | ❌ |
| Multi-Agent | Custom | ✅ | ✅ | ✅ |
| Learning Curve | Medium | Medium | Low | Very Low |
| Best For | Production Apps | Research | Workflows | Routing |

---

## Resources

- **Official Docs**: https://ai.pydantic.dev/
- **GitHub**: https://github.com/pydantic/pydantic-ai
- **Pydantic Docs**: https://docs.pydantic.dev/
- **Example File**: `examples/pydanticai_agent_example.py`

---

## Next Steps

1. Install PydanticAI: `pip install pydantic-ai pydantic>=2.0`
2. Run example: `python examples/pydanticai_agent_example.py`
3. Create your first type-safe agent
4. Define Pydantic models for structured outputs
5. Build a production application

**See Also**:
- [OpenAI Assistants](openai-assistants.md) - Official OpenAI SDK
- [OpenAI Swarm](openai-swarm.md) - Multi-agent coordination
- [Autogen](autogen.md) - Multi-agent conversations
