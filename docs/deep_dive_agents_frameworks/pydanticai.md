# PydanticAI: Type-Safe Agent Framework

## Table of Contents

1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [System Architecture](#system-architecture)
4. [High-Level System Architecture](#high-level-system-architecture)
5. [Core Components Deep Dive](#core-components-deep-dive)
   - [Agent Class](#agent-class)
   - [Models and Model Adapters](#models-and-model-adapters)
   - [Tools and Function Calling](#tools-and-function-calling)
   - [Dependencies and Dependency Injection](#dependencies-and-dependency-injection)
   - [Result and Structured Outputs](#result-and-structured-outputs)
   - [Streaming](#streaming)
   - [Message History](#message-history)
6. [End-to-End Flow](#end-to-end-flow)
7. [Simple Agent Examples](#simple-agent-examples)
8. [Complex Agent Examples](#complex-agent-examples)
9. [Multi-Agent Systems](#multi-agent-systems)
10. [RAG with Agents / Agentic RAG](#rag-with-agents--agentic-rag)
11. [FastMCP Servers with Agents](#fastmcp-servers-with-agents)
12. [A2A (Agent-to-Agent) Examples](#a2a-agent-to-agent-examples)
13. [Advanced Patterns](#advanced-patterns)
14. [Production Considerations](#production-considerations)
15. [Conclusion](#conclusion)

---

## Introduction

**PydanticAI** is a modern Python agent framework designed from the ground up with type safety, validation, and developer experience as core principles. Built on top of Pydantic, PydanticAI leverages Python's type system to provide compile-time safety, runtime validation, and excellent IDE support for building AI agents.

Unlike traditional agent frameworks that evolved from LLM wrapper libraries, PydanticAI was purpose-built for agent development. It provides a clean, intuitive API that embraces modern Python features like type hints, async/await, and dataclasses while offering powerful abstractions for common agent patterns.

PydanticAI is model-agnostic, supporting OpenAI, Anthropic, Google Gemini, Groq, and other providers through a unified interface. This allows developers to build agents that can seamlessly switch between different LLM providers without changing application code.

### Why PydanticAI?

- **Type Safety**: Full type hints throughout the codebase with MyPy strict mode support
- **Validation**: Automatic validation of inputs, outputs, and tool parameters using Pydantic
- **Model Agnostic**: Support for multiple LLM providers with a unified interface
- **Developer Experience**: Excellent IDE support, clear error messages, and intuitive APIs
- **Production Ready**: Built-in retry logic, error handling, and observability hooks
- **Dependency Injection**: Clean separation of concerns with type-safe dependency injection
- **Streaming Support**: First-class support for streaming responses and structured outputs

---

## Key Features

### 1. Type-Safe Agent Development

PydanticAI uses Python's type system to ensure correctness at both compile-time and runtime:

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class UserQuery(BaseModel):
    question: str
    user_id: int

class Response(BaseModel):
    answer: str
    confidence: float
    sources: list[str]

# Agent with typed inputs and outputs
agent = Agent[UserQuery, Response](
    'openai:gpt-4',
    result_type=Response
)
```

### 2. Powerful Tool System

Define tools with automatic parameter validation:

```python
from pydantic_ai import RunContext

@agent.tool
async def search_database(
    ctx: RunContext[UserQuery],
    query: str,
    limit: int = 10
) -> list[dict]:
    """Search the database for relevant documents."""
    # Access dependency through context
    db = ctx.deps
    return await db.search(query, limit)
```

### 3. Dependency Injection

Clean separation of concerns with type-safe dependencies:

```python
from dataclasses import dataclass

@dataclass
class Dependencies:
    db: DatabaseClient
    cache: CacheClient
    user_id: int

result = await agent.run(
    "What are my recent orders?",
    deps=Dependencies(db=db, cache=cache, user_id=123)
)
```

### 4. Structured Outputs

Guaranteed structured responses with Pydantic validation:

```python
class Analysis(BaseModel):
    sentiment: Literal['positive', 'negative', 'neutral']
    key_points: list[str]
    action_items: list[str]
    confidence: float = Field(ge=0.0, le=1.0)

agent = Agent('openai:gpt-4', result_type=Analysis)
result = await agent.run("Analyze this customer feedback...")
# result.data is a validated Analysis instance
```

### 5. Streaming Support

Stream both text and structured outputs:

```python
async with agent.run_stream("Generate a report...") as response:
    async for text in response.stream_text():
        print(text, end='', flush=True)

    final_result = await response.get_data()
```

### 6. Multi-Model Support

Switch between models without changing code:

```python
# OpenAI
agent = Agent('openai:gpt-4')

# Anthropic
agent = Agent('anthropic:claude-3-opus-20240229')

# Google Gemini
agent = Agent('gemini:gemini-1.5-pro')

# Groq
agent = Agent('groq:llama-3.1-70b-versatile')
```

### 7. Message History

Fine-grained control over conversation history:

```python
result1 = await agent.run("What's 2+2?")
result2 = await agent.run(
    "What about multiplied by 3?",
    message_history=result1.message_history()
)
```

### 8. Retry Logic and Error Handling

Built-in retry mechanisms with validation:

```python
agent = Agent(
    'openai:gpt-4',
    result_type=Response,
    retries=3  # Automatic retries on failure
)

try:
    result = await agent.run("Process this request")
except ModelRetry as e:
    print(f"Retry needed: {e}")
except UnexpectedModelBehavior as e:
    print(f"Model error: {e}")
```

---

## System Architecture

PydanticAI's architecture is built around clean separation of concerns and type safety:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Application Layer                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │   Agent    │  │   Tools    │  │Dependencies│  │  Results  │ │
│  │  Instance  │  │ Functions  │  │  Context   │  │   Data    │ │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬─────┘ │
└────────┼───────────────┼───────────────┼───────────────┼───────┘
         │               │               │               │
         └───────────────┼───────────────┼───────────────┘
                         │               │
┌────────────────────────┼───────────────┼─────────────────────────┐
│                   Core Agent Runtime                              │
│  ┌─────────────────────▼───────────────▼─────────────┐           │
│  │           Agent Execution Engine                   │           │
│  │  • Message Processing                              │           │
│  │  • Tool Dispatch                                   │           │
│  │  • Dependency Injection                            │           │
│  │  • Retry Logic                                     │           │
│  │  • Validation Pipeline                             │           │
│  └────────────────┬────────────────────┬──────────────┘           │
└───────────────────┼────────────────────┼──────────────────────────┘
                    │                    │
┌───────────────────▼────────────────────▼──────────────────────────┐
│                     Model Adapter Layer                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│  │   OpenAI     │ │  Anthropic   │ │    Gemini    │             │
│  │   Adapter    │ │   Adapter    │ │   Adapter    │             │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘             │
└─────────┼────────────────┼────────────────┼─────────────────────┘
          │                │                │
┌─────────▼────────────────▼────────────────▼─────────────────────┐
│                   External LLM APIs                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│  │   OpenAI     │ │  Anthropic   │ │   Google     │             │
│  │     API      │ │     API      │ │     API      │             │
│  └──────────────┘ └──────────────┘ └──────────────┘             │
└───────────────────────────────────────────────────────────────────┘
```

### Architecture Layers

1. **Application Layer**: User-defined agents, tools, and dependencies
2. **Core Runtime**: Message processing, tool dispatch, and validation
3. **Model Adapter Layer**: Unified interface to different LLM providers
4. **External APIs**: Communication with actual LLM services

---

## High-Level System Architecture

```
┌───────────────────────────────────────────────────────────────────────┐
│                         PydanticAI System                             │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                    Agent Configuration                          │ │
│  │                                                                 │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │ │
│  │  │  Model   │  │  System  │  │  Tools   │  │  Result  │      │ │
│  │  │  String  │  │  Prompt  │  │  List    │  │  Type    │      │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │ │
│  └───────────────────────┬─────────────────────────────────────────┘ │
│                          │                                           │
│  ┌───────────────────────▼─────────────────────────────────────────┐ │
│  │                    Execution Pipeline                           │ │
│  │                                                                 │ │
│  │  Input → Validation → Model Call → Tool Execution → Validation │ │
│  │    ↓         ↓            ↓             ↓              ↓       │ │
│  │  [Pydantic] [Types]  [Adapter]    [Functions]    [Pydantic]   │ │
│  └───────────────────────┬─────────────────────────────────────────┘ │
│                          │                                           │
│  ┌───────────────────────▼─────────────────────────────────────────┐ │
│  │                    Result Processing                            │ │
│  │                                                                 │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │ │
│  │  │  Data    │  │ Message  │  │  Usage   │  │  Retry   │      │ │
│  │  │ (Typed)  │  │ History  │  │  Stats   │  │  Info    │      │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────┐
│                        Data Flow Diagram                              │
│                                                                       │
│  User Input (str/Pydantic)                                           │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────┐                                                    │
│  │ Validation  │                                                    │
│  └──────┬──────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────┐     ┌──────────────┐                              │
│  │   Agent     │────▶│ Dependencies │                              │
│  │  run/stream │     └──────────────┘                              │
│  └──────┬──────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────┐                                                    │
│  │   Format    │                                                    │
│  │  Messages   │                                                    │
│  └──────┬──────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────┐     ┌──────────────┐                              │
│  │   Model     │────▶│ Tool Schema  │                              │
│  │   Adapter   │     │  Generation  │                              │
│  └──────┬──────┘     └──────────────┘                              │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────┐                                                    │
│  │  LLM API    │                                                    │
│  │    Call     │                                                    │
│  └──────┬──────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────┐                                                    │
│  │  Response   │                                                    │
│  │  Parsing    │                                                    │
│  └──────┬──────┘                                                    │
│         │                                                            │
│    ┌────┴────┐                                                      │
│    │         │                                                      │
│    ▼         ▼                                                      │
│  Tool      Text                                                     │
│  Call     Response                                                  │
│    │         │                                                      │
│    ▼         │                                                      │
│  Execute     │                                                      │
│  Function    │                                                      │
│    │         │                                                      │
│    └────┬────┘                                                      │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────┐                                                    │
│  │  Validate   │                                                    │
│  │   Output    │                                                    │
│  └──────┬──────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  Result Object (RunResult)                                          │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Core Components Deep Dive

### Agent Class

The `Agent` class is the central component in PydanticAI. It encapsulates the model, system prompt, tools, and execution logic.

#### Agent Definition

```python
from typing import TypeVar
from pydantic import BaseModel
from pydantic_ai import Agent

# Define dependency type
DepsT = TypeVar('DepsT')

# Define result type
class ResultType(BaseModel):
    value: str
    confidence: float

# Create agent with full type safety
agent: Agent[DepsT, ResultType] = Agent(
    model='openai:gpt-4',
    result_type=ResultType,
    system_prompt="You are a helpful assistant.",
    retries=3
)
```

#### Agent Parameters

- **model**: Model identifier (e.g., 'openai:gpt-4', 'anthropic:claude-3-opus-20240229')
- **result_type**: Pydantic model or Python type for structured output
- **system_prompt**: Static or dynamic system prompt
- **retries**: Number of retry attempts on failure
- **tools**: List of tools available to the agent
- **deps_type**: Type hint for dependencies

#### Dynamic System Prompts

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

@dataclass
class UserContext:
    user_id: int
    role: str
    preferences: dict

agent = Agent[UserContext, str]('openai:gpt-4')

@agent.system_prompt
def dynamic_prompt(ctx: RunContext[UserContext]) -> str:
    """Generate system prompt based on user context."""
    role = ctx.deps.role
    user_id = ctx.deps.user_id

    return f"""You are an AI assistant for user {user_id}.
User role: {role}
Adapt your responses to their role and preferences.
"""

# Use with dependency injection
result = await agent.run(
    "Help me with a task",
    deps=UserContext(user_id=123, role='admin', preferences={})
)
```

### Models and Model Adapters

PydanticAI provides a unified interface for different LLM providers through model adapters.

#### Supported Models

```python
from pydantic_ai import Agent

# OpenAI Models
agent_gpt4 = Agent('openai:gpt-4')
agent_gpt4_turbo = Agent('openai:gpt-4-turbo-preview')
agent_gpt35 = Agent('openai:gpt-3.5-turbo')

# Anthropic Models
agent_opus = Agent('anthropic:claude-3-opus-20240229')
agent_sonnet = Agent('anthropic:claude-3-sonnet-20240229')
agent_haiku = Agent('anthropic:claude-3-haiku-20240307')

# Google Gemini Models
agent_gemini_pro = Agent('gemini:gemini-1.5-pro')
agent_gemini_flash = Agent('gemini:gemini-1.5-flash')

# Groq Models
agent_llama = Agent('groq:llama-3.1-70b-versatile')
agent_mixtral = Agent('groq:mixtral-8x7b-32768')
```

#### Custom Model Settings

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Create custom model with specific settings
custom_model = OpenAIModel(
    'gpt-4',
    api_key='your-api-key',
    base_url='https://api.openai.com/v1',
    timeout=30.0,
    max_retries=3
)

agent = Agent(model=custom_model)
```

#### Model Request Settings

```python
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

agent = Agent('openai:gpt-4')

result = await agent.run(
    "Generate a creative story",
    model_settings=ModelSettings(
        temperature=0.8,
        max_tokens=1000,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )
)
```

### Tools and Function Calling

Tools are Python functions that agents can call to interact with external systems or perform computations.

#### Basic Tool Definition

```python
from pydantic_ai import Agent, RunContext
from datetime import datetime

agent = Agent('openai:gpt-4')

@agent.tool
def get_current_time(ctx: RunContext[None]) -> str:
    """Get the current time in ISO format."""
    return datetime.now().isoformat()

@agent.tool
async def fetch_weather(
    ctx: RunContext[None],
    city: str,
    units: str = 'metric'
) -> dict:
    """Fetch weather data for a city.

    Args:
        city: Name of the city
        units: Temperature units (metric/imperial)
    """
    # Simulated API call
    return {
        'city': city,
        'temperature': 22.5,
        'conditions': 'sunny',
        'units': units
    }
```

#### Tool with Dependencies

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import Any

@dataclass
class DatabaseDeps:
    db_client: Any
    cache: Any

agent = Agent[DatabaseDeps, str]('openai:gpt-4')

@agent.tool
async def query_database(
    ctx: RunContext[DatabaseDeps],
    query: str,
    limit: int = 10
) -> list[dict]:
    """Query the database with access to dependencies.

    Args:
        query: SQL query or search term
        limit: Maximum number of results
    """
    # Access dependencies through context
    db = ctx.deps.db_client
    cache = ctx.deps.cache

    # Check cache first
    cache_key = f"query:{query}:{limit}"
    cached = await cache.get(cache_key)
    if cached:
        return cached

    # Execute query
    results = await db.execute(query, limit=limit)

    # Cache results
    await cache.set(cache_key, results, ttl=300)

    return results

@agent.tool
def validate_user_access(
    ctx: RunContext[DatabaseDeps],
    resource_id: str
) -> bool:
    """Check if user has access to a resource."""
    db = ctx.deps.db_client
    # Perform access check
    return True
```

#### Tool with Validation

```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field, validator
from typing import Literal

class SearchParams(BaseModel):
    query: str = Field(..., min_length=1, max_length=200)
    category: Literal['products', 'articles', 'users']
    limit: int = Field(default=10, ge=1, le=100)

    @validator('query')
    def validate_query(cls, v):
        if len(v.split()) < 2:
            raise ValueError('Query must contain at least 2 words')
        return v

agent = Agent('openai:gpt-4')

@agent.tool
async def search(
    ctx: RunContext[None],
    params: SearchParams
) -> list[dict]:
    """Search with validated parameters.

    Args:
        params: Validated search parameters
    """
    # Parameters are already validated by Pydantic
    return [
        {'id': 1, 'title': f'Result for {params.query}'},
        {'id': 2, 'title': f'Another result'}
    ][:params.limit]
```

#### Tool Error Handling

```python
from pydantic_ai import Agent, RunContext, ModelRetry
from typing import Optional, Any

agent = Agent('openai:gpt-4')

@agent.tool
async def risky_operation(
    ctx: RunContext[None],
    operation: str
) -> dict:
    """Perform an operation that might fail.

    Args:
        operation: The operation to perform
    """
    try:
        # Attempt operation
        result = await perform_operation(operation)
        return {'success': True, 'data': result}
    except ValueError as e:
        # Validation error - let agent retry with different params
        raise ModelRetry(f"Invalid operation: {e}") from e
    except ConnectionError as e:
        # Transient error - agent should retry
        raise ModelRetry(f"Connection failed: {e}") from e
    except Exception as e:
        # Critical error - return error info to agent
        return {
            'success': False,
            'error': str(e),
            'message': 'Operation failed, please try a different approach'
        }

async def perform_operation(operation: str) -> Any:
    """Simulated operation that might fail."""
    if operation == 'invalid':
        raise ValueError('Invalid operation')
    return {'result': 'success'}
```

### Dependencies and Dependency Injection

PydanticAI uses dependency injection to provide clean separation between agent logic and runtime dependencies.

#### Basic Dependency Pattern

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import Protocol, Any

# Define dependency interface
class DatabaseProtocol(Protocol):
    async def query(self, sql: str) -> list[dict]: ...
    async def execute(self, sql: str) -> int: ...

@dataclass
class AppDependencies:
    db: DatabaseProtocol
    api_key: str
    user_id: int

# Create agent with dependency type
agent = Agent[AppDependencies, str]('openai:gpt-4')

@agent.tool
async def get_user_data(ctx: RunContext[AppDependencies]) -> dict:
    """Fetch user data from database."""
    deps = ctx.deps
    results = await deps.db.query(
        f"SELECT * FROM users WHERE id = {deps.user_id}"
    )
    return results[0] if results else {}

# Use agent with dependencies
class DatabaseClient:
    async def query(self, sql: str) -> list[dict]:
        return [{'id': 123, 'name': 'John'}]
    async def execute(self, sql: str) -> int:
        return 1

db_client = DatabaseClient()
deps = AppDependencies(
    db=db_client,
    api_key='secret-key',
    user_id=123
)

result = await agent.run(
    "Get my profile information",
    deps=deps
)
```

### Result and Structured Outputs

PydanticAI ensures type-safe, validated outputs through Pydantic models.

#### Basic Structured Output

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import Literal

class SentimentAnalysis(BaseModel):
    """Structured sentiment analysis result."""
    sentiment: Literal['positive', 'negative', 'neutral']
    confidence: float = Field(ge=0.0, le=1.0)
    key_phrases: list[str]
    language: str = Field(default='en')

agent = Agent[None, SentimentAnalysis](
    'openai:gpt-4',
    result_type=SentimentAnalysis,
    system_prompt='Analyze sentiment and extract key phrases from text.'
)

result = await agent.run("I absolutely love this product! Best purchase ever!")

# result.data is a validated SentimentAnalysis instance
print(f"Sentiment: {result.data.sentiment}")
print(f"Confidence: {result.data.confidence}")
print(f"Key phrases: {', '.join(result.data.key_phrases)}")
```

### Streaming

PydanticAI supports streaming both text and structured outputs.

#### Text Streaming

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4')

async def stream_response(prompt: str):
    """Stream text response in real-time."""
    async with agent.run_stream(prompt) as response:
        print("Streaming response: ", end='')
        async for text_chunk in response.stream_text():
            print(text_chunk, end='', flush=True)
        print()  # New line after streaming

        # Get final result
        result = await response.get_data()
        return result

# Usage
await stream_response("Write a short story about a robot learning to paint")
```

### Message History

PydanticAI provides fine-grained control over conversation context.

#### Basic Message History

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4')

async def conversation_example():
    """Example of maintaining conversation context."""
    # First message
    result1 = await agent.run("What's the capital of France?")
    print(f"Answer 1: {result1.data}")

    # Follow-up with history
    result2 = await agent.run(
        "What's the population?",
        message_history=result1.message_history()
    )
    print(f"Answer 2: {result2.data}")

    # Another follow-up
    result3 = await agent.run(
        "What are the top attractions?",
        message_history=result2.message_history()
    )
    print(f"Answer 3: {result3.data}")

    return result3

await conversation_example()
```

---

## End-to-End Flow

Let's trace a complete request through PydanticAI's execution pipeline.

### Execution Steps

```
1. User initiates request
   ↓
2. Input validation (Pydantic)
   ↓
3. Dependencies injected into context
   ↓
4. System prompt generation (static or dynamic)
   ↓
5. Message formatting (user message + history)
   ↓
6. Tool schemas generated from registered tools
   ↓
7. Model adapter formats request for specific LLM API
   ↓
8. API call to LLM provider
   ↓
9. Response parsing and interpretation
   ↓
10. Tool call detection
    ↓
    ├─ If tool calls present:
    │  ├─ Validate tool parameters
    │  ├─ Execute tool functions with dependencies
    │  ├─ Collect tool results
    │  └─ Return to step 7 with tool results
    │
    └─ If text/structured response:
       ↓
11. Output validation (if result_type specified)
    ↓
12. Retry logic (if validation fails)
    ↓
13. Result object creation
    ↓
14. Return to user
```

### Detailed Example with Tracing

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import Optional
import logging
import asyncio

# Configure logging to trace execution
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Step 1: Define structured types
class WeatherQuery(BaseModel):
    """Validated input model."""
    location: str = Field(..., min_length=2)
    units: str = Field(default='celsius')

class WeatherResult(BaseModel):
    """Validated output model."""
    location: str
    temperature: float
    conditions: str
    humidity: int = Field(ge=0, le=100)
    forecast: list[str]

# Step 2: Define dependencies
@dataclass
class WeatherDeps:
    api_key: str
    cache_enabled: bool = True

# Step 3: Create agent with configuration
agent = Agent[WeatherDeps, WeatherResult](
    model='openai:gpt-4',
    result_type=WeatherResult,
    system_prompt="""You are a weather assistant.
    Use the weather API tool to fetch real-time data.
    Always provide comprehensive forecasts.""",
    retries=2
)

# Step 4: Register tools
@agent.tool
async def fetch_weather_data(
    ctx: RunContext[WeatherDeps],
    location: str,
    units: str = 'celsius'
) -> dict:
    """Fetch weather from external API.

    Args:
        location: City name or coordinates
        units: Temperature units (celsius/fahrenheit)
    """
    logger.info(f"Tool called: fetch_weather_data({location}, {units})")
    logger.info(f"Using API key: {ctx.deps.api_key[:8]}...")

    # Simulate API call
    return {
        'location': location,
        'temperature': 22.5,
        'conditions': 'Partly cloudy',
        'humidity': 65,
        'forecast': ['Sunny tomorrow', 'Rain on Tuesday']
    }

# Step 5: Execute request with full tracing
async def trace_execution():
    """Execute request and trace through all steps."""

    logger.info("=" * 60)
    logger.info("STEP 1: User initiates request")
    user_input = "What's the weather in London?"
    logger.info(f"Input: {user_input}")

    logger.info("\nSTEP 2: Create dependencies")
    deps = WeatherDeps(api_key='secret-api-key-12345', cache_enabled=True)
    logger.info(f"Dependencies: {deps}")

    logger.info("\nSTEP 3: Execute agent.run()")
    try:
        result = await agent.run(
            user_input,
            deps=deps
        )

        logger.info("\nSTEP 4: Execution successful")
        logger.info(f"Result type: {type(result.data)}")
        logger.info(f"Data: {result.data}")

        logger.info("\nSTEP 5: Access result attributes")
        weather = result.data
        logger.info(f"Location: {weather.location}")
        logger.info(f"Temperature: {weather.temperature}°C")
        logger.info(f"Conditions: {weather.conditions}")
        logger.info(f"Humidity: {weather.humidity}%")
        logger.info(f"Forecast: {weather.forecast}")

        logger.info("\nSTEP 6: Access metadata")
        logger.info(f"Message history length: {len(result.message_history())}")

        logger.info("=" * 60)

        return result

    except Exception as e:
        logger.error(f"Execution failed: {e}", exc_info=True)
        raise

# Run the traced execution
if __name__ == "__main__":
    asyncio.run(trace_execution())
```

---

## Simple Agent Examples

### Example 1: Basic Question Answering Agent

```python
"""
Simple Q&A agent with no tools or dependencies.
Demonstrates basic agent setup and usage.
"""

from pydantic_ai import Agent
import asyncio

# Create basic agent
qa_agent = Agent(
    model='openai:gpt-4',
    system_prompt='You are a helpful assistant that provides clear, concise answers.'
)

async def simple_qa_example():
    """Basic question answering."""

    # Single question
    result = await qa_agent.run("What is the capital of Japan?")
    print(f"Answer: {result.data}")

    # Follow-up question with history
    result2 = await qa_agent.run(
        "What is its population?",
        message_history=result.message_history()
    )
    print(f"Follow-up answer: {result2.data}")

    # Another question without history (fresh context)
    result3 = await qa_agent.run("Explain photosynthesis in simple terms.")
    print(f"New question: {result3.data}")

if __name__ == "__main__":
    asyncio.run(simple_qa_example())
```

### Example 2: Structured Data Extraction Agent

```python
"""
Agent that extracts structured data from unstructured text.
Demonstrates Pydantic models for output validation.
"""

from pydantic import BaseModel, Field, EmailStr
from pydantic_ai import Agent
from typing import Optional, List
import asyncio

class Person(BaseModel):
    """Extracted person information."""
    name: str
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    occupation: Optional[str] = None

class ContactInfo(BaseModel):
    """Structured contact information extraction."""
    people: List[Person]
    organization: Optional[str] = None
    location: Optional[str] = None
    summary: str

# Create extraction agent with structured output
extraction_agent = Agent[None, ContactInfo](
    model='openai:gpt-4',
    result_type=ContactInfo,
    system_prompt="""Extract structured information from text.
    Identify all people mentioned with their details.
    Return valid, complete data."""
)

async def extraction_example():
    """Extract structured data from unstructured text."""

    text = """
    John Smith (john.smith@techcorp.com) is the 35-year-old CTO of TechCorp,
    located in San Francisco. He works closely with Sarah Johnson, the
    28-year-old Lead Developer (sarah.j@techcorp.com, 555-1234).
    They are currently hiring senior engineers for their AI team.
    """

    result = await extraction_agent.run(text)
    info = result.data

    print("Extracted Information:")
    print(f"Organization: {info.organization}")
    print(f"Location: {info.location}")
    print(f"\nPeople ({len(info.people)}):")

    for person in info.people:
        print(f"\n  Name: {person.name}")
        if person.age:
            print(f"  Age: {person.age}")
        if person.email:
            print(f"  Email: {person.email}")
        if person.phone:
            print(f"  Phone: {person.phone}")
        if person.occupation:
            print(f"  Occupation: {person.occupation}")

    print(f"\nSummary: {info.summary}")

    return info

if __name__ == "__main__":
    asyncio.run(extraction_example())
```

### Example 3: Calculator Agent with Tools

```python
"""
Simple calculator agent with mathematical tools.
Demonstrates basic tool usage and function calling.
"""

from pydantic_ai import Agent, RunContext
import asyncio
import math

# Create calculator agent
calc_agent = Agent(
    model='openai:gpt-4',
    system_prompt="""You are a calculator assistant.
    Use the provided tools to perform calculations.
    Always show your work and explain the steps."""
)

@calc_agent.tool
def add(ctx: RunContext[None], a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@calc_agent.tool
def subtract(ctx: RunContext[None], a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

@calc_agent.tool
def multiply(ctx: RunContext[None], a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@calc_agent.tool
def divide(ctx: RunContext[None], a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@calc_agent.tool
def power(ctx: RunContext[None], base: float, exponent: float) -> float:
    """Raise base to the power of exponent."""
    return base ** exponent

@calc_agent.tool
def square_root(ctx: RunContext[None], n: float) -> float:
    """Calculate square root of n."""
    if n < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(n)

async def calculator_example():
    """Demonstrate calculator agent with various operations."""

    queries = [
        "What is 15 + 27?",
        "Calculate 144 divided by 12",
        "What is the square root of 225?",
        "Calculate 2 to the power of 8",
        "If I have $150 and spend $47.50, how much is left?"
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        result = await calc_agent.run(query)
        print(f"Answer: {result.data}\n")

if __name__ == "__main__":
    asyncio.run(calculator_example())
```

### Example 4: Customer Support Agent with Dependencies

```python
"""
Customer support agent with database access.
Demonstrates dependency injection and context usage.
"""

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import asyncio

class SupportTicket(BaseModel):
    """Customer support ticket."""
    ticket_id: str
    summary: str
    priority: str
    suggested_actions: List[str]

@dataclass
class SupportDeps:
    """Dependencies for support agent."""
    customer_id: str
    db: 'CustomerDatabase'

class CustomerDatabase:
    """Mock customer database."""

    def __init__(self):
        self.customers = {
            'C001': {
                'name': 'Alice Johnson',
                'email': 'alice@example.com',
                'orders': ['ORD-123', 'ORD-456'],
                'account_status': 'active'
            },
            'C002': {
                'name': 'Bob Smith',
                'email': 'bob@example.com',
                'orders': ['ORD-789'],
                'account_status': 'active'
            }
        }

        self.orders = {
            'ORD-123': {'product': 'Laptop', 'status': 'delivered', 'date': '2024-01-15'},
            'ORD-456': {'product': 'Mouse', 'status': 'shipped', 'date': '2024-02-01'},
            'ORD-789': {'product': 'Keyboard', 'status': 'processing', 'date': '2024-02-10'}
        }

    async def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get customer information."""
        return self.customers.get(customer_id)

    async def get_orders(self, customer_id: str) -> List[Dict[str, Any]]:
        """Get customer orders."""
        customer = await self.get_customer(customer_id)
        if not customer:
            return []

        order_ids = customer.get('orders', [])
        return [
            {**self.orders[oid], 'order_id': oid}
            for oid in order_ids
            if oid in self.orders
        ]

# Create support agent
support_agent = Agent[SupportDeps, SupportTicket](
    model='openai:gpt-4',
    result_type=SupportTicket,
    system_prompt="""You are a customer support agent.
    Help customers with their inquiries using the available tools.
    Always be polite and provide accurate information."""
)

@support_agent.tool
async def get_customer_info(ctx: RunContext[SupportDeps]) -> dict:
    """Get information about the current customer."""
    customer = await ctx.deps.db.get_customer(ctx.deps.customer_id)
    if not customer:
        return {'error': 'Customer not found'}
    return customer

@support_agent.tool
async def get_order_history(ctx: RunContext[SupportDeps]) -> List[dict]:
    """Get customer's order history."""
    orders = await ctx.deps.db.get_orders(ctx.deps.customer_id)
    return orders

@support_agent.tool
async def check_order_status(
    ctx: RunContext[SupportDeps],
    order_id: str
) -> dict:
    """Check the status of a specific order."""
    orders = await ctx.deps.db.get_orders(ctx.deps.customer_id)
    for order in orders:
        if order['order_id'] == order_id:
            return order
    return {'error': 'Order not found'}

async def support_example():
    """Demonstrate customer support agent."""

    # Initialize database
    db = CustomerDatabase()

    # Create dependencies for customer C001
    deps = SupportDeps(customer_id='C001', db=db)

    # Customer inquiry
    inquiry = """
    Hi, I'd like to check the status of my recent orders.
    Also, when was my laptop delivered?
    """

    print("Customer Inquiry:")
    print(inquiry)
    print("\nProcessing...\n")

    result = await support_agent.run(inquiry, deps=deps)
    ticket = result.data

    print("Support Ticket Created:")
    print(f"Ticket ID: {ticket.ticket_id}")
    print(f"Summary: {ticket.summary}")
    print(f"Priority: {ticket.priority}")
    print(f"\nSuggested Actions:")
    for action in ticket.suggested_actions:
        print(f"  - {action}")

if __name__ == "__main__":
    asyncio.run(support_example())
```

### Example 5: Content Moderation Agent

```python
"""
Content moderation agent with structured analysis.
Demonstrates multi-faceted content analysis.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Literal
import asyncio

class ModerationFlag(BaseModel):
    """Individual moderation flag."""
    category: str
    severity: Literal['low', 'medium', 'high']
    description: str
    confidence: float = Field(ge=0.0, le=1.0)

class ModerationResult(BaseModel):
    """Complete moderation analysis."""
    is_safe: bool
    overall_score: float = Field(ge=0.0, le=1.0, description="0=unsafe, 1=safe")
    flags: List[ModerationFlag]
    summary: str
    recommended_action: Literal['approve', 'review', 'reject']
    explanation: str

# Create moderation agent
moderation_agent = Agent[None, ModerationResult](
    model='openai:gpt-4',
    result_type=ModerationResult,
    system_prompt="""You are a content moderation assistant.
    Analyze content for:
    - Harmful or offensive language
    - Spam or promotional content
    - Personal information exposure
    - Misinformation or false claims
    - Copyright violations

    Provide detailed, fair analysis with confidence scores."""
)

async def moderate_content(content: str) -> ModerationResult:
    """Moderate user-generated content."""
    result = await moderation_agent.run(f"Analyze this content:\n\n{content}")
    return result.data

async def moderation_example():
    """Demonstrate content moderation."""

    test_contents = [
        "This is a great product! I've been using it for months and love it.",

        "BUY NOW!!! CLICK HERE FOR AMAZING DEALS!!! LIMITED TIME OFFER!!!",

        "I disagree with your opinion, but I respect your perspective.",

        "You can contact me at john.doe@email.com or call 555-1234.",
    ]

    for i, content in enumerate(test_contents, 1):
        print(f"\n{'='*60}")
        print(f"Content {i}:")
        print(f"{'='*60}")
        print(content)
        print(f"\n{'─'*60}")

        result = await moderate_content(content)

        print(f"Safe: {result.is_safe}")
        print(f"Overall Score: {result.overall_score:.2f}")
        print(f"Recommended Action: {result.recommended_action.upper()}")
        print(f"\nSummary: {result.summary}")

        if result.flags:
            print(f"\nFlags ({len(result.flags)}):")
            for flag in result.flags:
                print(f"  - {flag.category} ({flag.severity}): {flag.description}")
                print(f"    Confidence: {flag.confidence:.2%}")

        print(f"\nExplanation: {result.explanation}")

if __name__ == "__main__":
    asyncio.run(moderation_example())
```

---

## Complex Agent Examples

### Example 1: E-Commerce Recommendation Engine

```python
"""
Complex e-commerce recommendation agent with multiple tools and data sources.
Demonstrates advanced tool coordination and dependency management.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Literal
import asyncio
from datetime import datetime, timedelta

class ProductRecommendation(BaseModel):
    """Individual product recommendation."""
    product_id: str
    name: str
    category: str
    price: float
    relevance_score: float = Field(ge=0.0, le=1.0)
    reason: str

class RecommendationResult(BaseModel):
    """Complete recommendation response."""
    recommendations: List[ProductRecommendation]
    user_profile_summary: str
    search_strategy: str
    total_products_analyzed: int
    personalization_factors: List[str]

@dataclass
class EcommerceDeps:
    """E-commerce system dependencies."""
    user_id: str
    product_db: 'ProductDatabase'
    user_profile_service: 'UserProfileService'
    analytics_service: 'AnalyticsService'

class ProductDatabase:
    """Mock product database."""

    def __init__(self):
        self.products = [
            {'id': 'P001', 'name': 'Laptop Pro 15"', 'category': 'electronics', 'price': 1299.99, 'tags': ['work', 'productivity', 'premium']},
            {'id': 'P002', 'name': 'Wireless Mouse', 'category': 'electronics', 'price': 29.99, 'tags': ['accessories', 'ergonomic']},
            {'id': 'P003', 'name': 'USB-C Hub', 'category': 'electronics', 'price': 49.99, 'tags': ['accessories', 'connectivity']},
            {'id': 'P004', 'name': 'Mechanical Keyboard', 'category': 'electronics', 'price': 149.99, 'tags': ['peripherals', 'gaming', 'premium']},
            {'id': 'P005', 'name': 'Monitor 27" 4K', 'category': 'electronics', 'price': 499.99, 'tags': ['display', 'premium', 'productivity']},
            {'id': 'P006', 'name': 'Webcam HD', 'category': 'electronics', 'price': 79.99, 'tags': ['video', 'work', 'streaming']},
            {'id': 'P007', 'name': 'Desk Lamp LED', 'category': 'office', 'price': 39.99, 'tags': ['lighting', 'productivity']},
            {'id': 'P008', 'name': 'Office Chair', 'category': 'office', 'price': 299.99, 'tags': ['furniture', 'ergonomic', 'comfort']},
        ]

    async def search_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        max_price: Optional[float] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search products with filters."""
        results = self.products.copy()

        if category:
            results = [p for p in results if p['category'] == category]

        if max_price:
            results = [p for p in results if p['price'] <= max_price]

        if tags:
            results = [p for p in results if any(t in p['tags'] for t in tags)]

        if query:
            query_lower = query.lower()
            results = [p for p in results if query_lower in p['name'].lower() or query_lower in ' '.join(p['tags']).lower()]

        return results[:limit]

    async def get_product_details(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed product information."""
        for product in self.products:
            if product['id'] == product_id:
                return product
        return None

class UserProfileService:
    """User profile and preference service."""

    def __init__(self):
        self.profiles = {
            'U001': {
                'preferences': ['electronics', 'premium', 'productivity'],
                'budget_range': (0, 2000),
                'purchase_history': ['P001', 'P002'],
                'browsing_history': ['P004', 'P005', 'P006'],
                'interests': ['work from home', 'gaming', 'content creation']
            },
            'U002': {
                'preferences': ['budget-friendly', 'office', 'ergonomic'],
                'budget_range': (0, 500),
                'purchase_history': ['P007'],
                'browsing_history': ['P008', 'P003'],
                'interests': ['home office', 'comfort', 'productivity']
            }
        }

    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile data."""
        return self.profiles.get(user_id, {
            'preferences': [],
            'budget_range': (0, 10000),
            'purchase_history': [],
            'browsing_history': [],
            'interests': []
        })

    async def get_user_purchase_history(self, user_id: str) -> List[str]:
        """Get user's previous purchases."""
        profile = await self.get_user_profile(user_id)
        return profile.get('purchase_history', [])

    async def get_user_preferences(self, user_id: str) -> List[str]:
        """Get user preferences."""
        profile = await self.get_user_profile(user_id)
        return profile.get('preferences', [])

class AnalyticsService:
    """Analytics and trending data service."""

    async def get_trending_products(self, category: Optional[str] = None, limit: int = 5) -> List[str]:
        """Get trending product IDs."""
        # Mock trending products
        trending = ['P001', 'P004', 'P005', 'P008', 'P006']
        return trending[:limit]

    async def get_similar_users_purchased(self, user_id: str, limit: int = 5) -> List[str]:
        """Get products purchased by similar users."""
        # Mock collaborative filtering
        similar_purchases = ['P003', 'P004', 'P006']
        return similar_purchases[:limit]

    async def get_frequently_bought_together(self, product_id: str) -> List[str]:
        """Get products frequently bought with given product."""
        # Mock association rules
        bundles = {
            'P001': ['P002', 'P003', 'P006'],
            'P004': ['P002', 'P001'],
            'P008': ['P007']
        }
        return bundles.get(product_id, [])

# Create recommendation agent
recommendation_agent = Agent[EcommerceDeps, RecommendationResult](
    model='openai:gpt-4',
    result_type=RecommendationResult,
    system_prompt="""You are an intelligent e-commerce recommendation engine.
    Analyze user preferences, purchase history, and browsing behavior to provide personalized recommendations.
    Use all available tools to gather data and make informed recommendations.
    Consider price range, user interests, trending items, and complementary products."""
)

@recommendation_agent.tool
async def get_user_preferences(ctx: RunContext[EcommerceDeps]) -> Dict[str, Any]:
    """Get user's preferences and profile information."""
    profile = await ctx.deps.user_profile_service.get_user_profile(ctx.deps.user_id)
    return profile

@recommendation_agent.tool
async def search_products_by_criteria(
    ctx: RunContext[EcommerceDeps],
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    tags: Optional[List[str]] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Search products based on criteria."""
    return await ctx.deps.product_db.search_products(
        category=category,
        max_price=max_price,
        tags=tags,
        limit=limit
    )

@recommendation_agent.tool
async def get_trending_items(
    ctx: RunContext[EcommerceDeps],
    category: Optional[str] = None,
    limit: int = 5
) -> List[str]:
    """Get currently trending product IDs."""
    return await ctx.deps.analytics_service.get_trending_products(category, limit)

@recommendation_agent.tool
async def get_product_info(
    ctx: RunContext[EcommerceDeps],
    product_id: str
) -> Optional[Dict[str, Any]]:
    """Get detailed information about a product."""
    return await ctx.deps.product_db.get_product_details(product_id)

@recommendation_agent.tool
async def find_complementary_products(
    ctx: RunContext[EcommerceDeps],
    product_id: str
) -> List[str]:
    """Find products that are frequently bought together."""
    return await ctx.deps.analytics_service.get_frequently_bought_together(product_id)

@recommendation_agent.tool
async def get_collaborative_recommendations(
    ctx: RunContext[EcommerceDeps],
    limit: int = 5
) -> List[str]:
    """Get recommendations based on similar users' purchases."""
    return await ctx.deps.analytics_service.get_similar_users_purchased(
        ctx.deps.user_id, limit
    )

async def ecommerce_recommendation_example():
    """Demonstrate complex e-commerce recommendation engine."""

    # Initialize services
    product_db = ProductDatabase()
    user_service = UserProfileService()
    analytics = AnalyticsService()

    # Create dependencies
    deps = EcommerceDeps(
        user_id='U001',
        product_db=product_db,
        user_profile_service=user_service,
        analytics_service=analytics
    )

    # User query
    query = "I'm setting up my home office and need recommendations for a complete workstation setup"

    print(f"User Query: {query}\n")
    print("Analyzing preferences and generating recommendations...\n")

    result = await recommendation_agent.run(query, deps=deps)
    recommendations = result.data

    print("=" * 70)
    print("PERSONALIZED RECOMMENDATIONS")
    print("=" * 70)

    print(f"\nUser Profile Summary:\n{recommendations.user_profile_summary}")
    print(f"\nSearch Strategy: {recommendations.search_strategy}")
    print(f"Products Analyzed: {recommendations.total_products_analyzed}")

    print(f"\nPersonalization Factors:")
    for factor in recommendations.personalization_factors:
        print(f"  - {factor}")

    print(f"\n{'─' * 70}")
    print(f"TOP RECOMMENDATIONS ({len(recommendations.recommendations)})")
    print(f"{'─' * 70}\n")

    for i, rec in enumerate(recommendations.recommendations, 1):
        print(f"{i}. {rec.name} (${rec.price})")
        print(f"   Category: {rec.category}")
        print(f"   Relevance: {rec.relevance_score:.1%}")
        print(f"   Reason: {rec.reason}\n")

if __name__ == "__main__":
    asyncio.run(ecommerce_recommendation_example())
```

### Example 2: Research Assistant with Web Search

```python
"""
Research assistant that searches, analyzes, and synthesizes information.
Demonstrates complex information gathering and analysis workflows.
"""

from pydantic import BaseModel, Field, HttpUrl
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import asyncio
from datetime import datetime

class Citation(BaseModel):
    """Source citation."""
    title: str
    url: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[str] = None
    relevance_score: float = Field(ge=0.0, le=1.0)

class ResearchSection(BaseModel):
    """Section of research report."""
    heading: str
    content: str
    key_points: List[str]
    citations: List[Citation]

class ResearchReport(BaseModel):
    """Complete research report."""
    title: str
    executive_summary: str
    sections: List[ResearchSection]
    conclusions: List[str]
    further_research: List[str]
    total_sources: int
    confidence_level: Literal['low', 'medium', 'high']

@dataclass
class ResearchDeps:
    """Research assistant dependencies."""
    search_engine: 'SearchEngine'
    knowledge_base: 'KnowledgeBase'
    citation_formatter: 'CitationFormatter'

class SearchEngine:
    """Mock search engine."""

    async def search(
        self,
        query: str,
        num_results: int = 10,
        search_type: str = 'general'
    ) -> List[Dict[str, Any]]:
        """Perform web search."""
        # Mock search results
        results = [
            {
                'title': f'Article about {query} - Part 1',
                'url': f'https://example.com/article-1',
                'snippet': f'This article discusses {query} in detail with recent findings...',
                'author': 'Dr. Jane Smith',
                'published': '2024-01-15'
            },
            {
                'title': f'Research paper on {query}',
                'url': f'https://example.com/research-paper',
                'snippet': f'A comprehensive study of {query} covering methodology and results...',
                'author': 'John Doe et al.',
                'published': '2023-12-20'
            },
            {
                'title': f'{query}: A Complete Guide',
                'url': f'https://example.com/guide',
                'snippet': f'Everything you need to know about {query} including best practices...',
                'author': 'Tech Blog',
                'published': '2024-02-01'
            }
        ]
        return results[:num_results]

    async def get_page_content(self, url: str) -> str:
        """Fetch content from URL."""
        # Mock page content
        return f"Detailed content from {url} discussing the topic in depth with analysis and examples."

class KnowledgeBase:
    """Internal knowledge base."""

    async def query(
        self,
        topic: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Query internal knowledge base."""
        return {
            'topic': topic,
            'summary': f'Knowledge base information about {topic}',
            'related_topics': ['topic1', 'topic2', 'topic3'],
            'last_updated': '2024-01-01'
        }

    async def find_related_topics(self, topic: str) -> List[str]:
        """Find related topics."""
        return [f'{topic} applications', f'{topic} history', f'{topic} future trends']

class CitationFormatter:
    """Format citations."""

    def format_citation(
        self,
        title: str,
        author: Optional[str],
        url: Optional[str],
        date: Optional[str],
        style: str = 'APA'
    ) -> str:
        """Format citation in specified style."""
        if style == 'APA':
            citation = f"{author or 'Unknown'}. ({date or 'n.d.'}). {title}."
            if url:
                citation += f" Retrieved from {url}"
            return citation
        return f"{title} by {author or 'Unknown'}"

# Create research agent
research_agent = Agent[ResearchDeps, ResearchReport](
    model='openai:gpt-4',
    result_type=ResearchReport,
    system_prompt="""You are an expert research assistant.
    Conduct thorough research using web search and knowledge base.
    Synthesize information from multiple sources.
    Provide well-structured reports with proper citations.
    Evaluate source credibility and information quality."""
)

@research_agent.tool
async def web_search(
    ctx: RunContext[ResearchDeps],
    query: str,
    num_results: int = 10
) -> List[Dict[str, Any]]:
    """Search the web for information.

    Args:
        query: Search query
        num_results: Number of results to return
    """
    return await ctx.deps.search_engine.search(query, num_results)

@research_agent.tool
async def fetch_article_content(
    ctx: RunContext[ResearchDeps],
    url: str
) -> str:
    """Fetch full content from a URL.

    Args:
        url: URL to fetch
    """
    return await ctx.deps.search_engine.get_page_content(url)

@research_agent.tool
async def query_knowledge_base(
    ctx: RunContext[ResearchDeps],
    topic: str
) -> Dict[str, Any]:
    """Query internal knowledge base for information.

    Args:
        topic: Topic to search for
    """
    return await ctx.deps.knowledge_base.query(topic)

@research_agent.tool
async def find_related_topics(
    ctx: RunContext[ResearchDeps],
    topic: str
) -> List[str]:
    """Find topics related to the given topic.

    Args:
        topic: Base topic
    """
    return await ctx.deps.knowledge_base.find_related_topics(topic)

async def research_assistant_example():
    """Demonstrate research assistant."""

    # Initialize dependencies
    search = SearchEngine()
    kb = KnowledgeBase()
    citation_fmt = CitationFormatter()

    deps = ResearchDeps(
        search_engine=search,
        knowledge_base=kb,
        citation_formatter=citation_fmt
    )

    # Research topic
    topic = "The impact of artificial intelligence on software development practices"

    print(f"Research Topic: {topic}\n")
    print("Conducting research...\n")

    result = await research_agent.run(
        f"Research this topic comprehensively: {topic}",
        deps=deps
    )

    report = result.data

    print("=" * 80)
    print(f"RESEARCH REPORT: {report.title}")
    print("=" * 80)

    print(f"\nEXECUTIVE SUMMARY")
    print(f"{'─' * 80}")
    print(f"{report.executive_summary}\n")

    print(f"MAIN FINDINGS")
    print(f"{'─' * 80}")
    for i, section in enumerate(report.sections, 1):
        print(f"\n{i}. {section.heading}")
        print(f"{section.content}\n")

        if section.key_points:
            print("Key Points:")
            for point in section.key_points:
                print(f"  • {point}")

        if section.citations:
            print(f"\nSources ({len(section.citations)}):")
            for cite in section.citations[:3]:  # Show first 3
                print(f"  - {cite.title}")
                if cite.url:
                    print(f"    {cite.url}")
        print()

    print(f"CONCLUSIONS")
    print(f"{'─' * 80}")
    for i, conclusion in enumerate(report.conclusions, 1):
        print(f"{i}. {conclusion}")

    print(f"\nFURTHER RESEARCH")
    print(f"{'─' * 80}")
    for area in report.further_research:
        print(f"  • {area}")

    print(f"\nREPORT METADATA")
    print(f"{'─' * 80}")
    print(f"Total Sources: {report.total_sources}")
    print(f"Confidence Level: {report.confidence_level.upper()}")

if __name__ == "__main__":
    asyncio.run(research_assistant_example())
```

### Example 3: Financial Analysis Agent

```python
"""
Financial analysis agent with data processing and risk assessment.
Demonstrates complex numerical analysis and decision support.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Literal
import asyncio
from datetime import datetime, timedelta
import statistics

class StockData(BaseModel):
    """Stock price data."""
    symbol: str
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class FinancialMetrics(BaseModel):
    """Key financial metrics."""
    metric_name: str
    value: float
    unit: str
    interpretation: Literal['positive', 'negative', 'neutral']
    explanation: str

class RiskAssessment(BaseModel):
    """Risk assessment."""
    risk_level: Literal['low', 'medium', 'high', 'critical']
    risk_factors: List[str]
    mitigation_strategies: List[str]
    confidence: float = Field(ge=0.0, le=1.0)

class FinancialAnalysis(BaseModel):
    """Complete financial analysis."""
    asset_symbol: str
    analysis_date: str
    price_summary: Dict[str, float]
    key_metrics: List[FinancialMetrics]
    trend_analysis: str
    risk_assessment: RiskAssessment
    recommendation: Literal['strong_buy', 'buy', 'hold', 'sell', 'strong_sell']
    recommendation_rationale: str
    target_price: Optional[float] = None

@dataclass
class FinancialDeps:
    """Financial analysis dependencies."""
    market_data: 'MarketDataService'
    analytics: 'FinancialAnalyticsService'
    risk_engine: 'RiskEngine'

class MarketDataService:
    """Market data service."""

    async def get_stock_price(self, symbol: str) -> float:
        """Get current stock price."""
        # Mock price
        prices = {'AAPL': 175.50, 'GOOGL': 142.30, 'MSFT': 378.90}
        return prices.get(symbol, 100.0)

    async def get_historical_prices(
        self,
        symbol: str,
        days: int = 30
    ) -> List[StockData]:
        """Get historical price data."""
        # Mock historical data
        base_price = await self.get_stock_price(symbol)
        data = []

        for i in range(days):
            date = (datetime.now() - timedelta(days=days-i)).strftime('%Y-%m-%d')
            variance = (i % 5 - 2) * 2
            data.append(StockData(
                symbol=symbol,
                date=date,
                open=base_price + variance,
                high=base_price + variance + 2,
                low=base_price + variance - 2,
                close=base_price + variance + 1,
                volume=1000000 + (i * 10000)
            ))

        return data

    async def get_market_indicators(self) -> Dict[str, Any]:
        """Get overall market indicators."""
        return {
            'vix': 18.5,  # Volatility index
            'market_sentiment': 'bullish',
            'sector_performance': {'tech': 2.3, 'finance': 1.1, 'healthcare': 0.8}
        }

class FinancialAnalyticsService:
    """Financial analytics service."""

    async def calculate_moving_average(
        self,
        prices: List[float],
        period: int = 20
    ) -> float:
        """Calculate moving average."""
        if len(prices) < period:
            period = len(prices)
        return sum(prices[-period:]) / period

    async def calculate_volatility(self, prices: List[float]) -> float:
        """Calculate price volatility."""
        if len(prices) < 2:
            return 0.0
        returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
        return statistics.stdev(returns) if len(returns) > 1 else 0.0

    async def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index."""
        if len(prices) < period + 1:
            return 50.0  # Neutral

        gains = []
        losses = []

        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    async def detect_trend(self, prices: List[float]) -> str:
        """Detect price trend."""
        if len(prices) < 5:
            return 'insufficient_data'

        recent = prices[-5:]
        if all(recent[i] > recent[i-1] for i in range(1, len(recent))):
            return 'strong_uptrend'
        elif all(recent[i] < recent[i-1] for i in range(1, len(recent))):
            return 'strong_downtrend'
        elif recent[-1] > recent[0]:
            return 'uptrend'
        elif recent[-1] < recent[0]:
            return 'downtrend'
        else:
            return 'sideways'

class RiskEngine:
    """Risk assessment engine."""

    async def assess_volatility_risk(self, volatility: float) -> str:
        """Assess risk based on volatility."""
        if volatility < 0.02:
            return 'low'
        elif volatility < 0.05:
            return 'medium'
        else:
            return 'high'

    async def assess_market_risk(self, vix: float) -> str:
        """Assess market risk based on VIX."""
        if vix < 15:
            return 'low'
        elif vix < 25:
            return 'medium'
        else:
            return 'high'

# Create financial analysis agent
financial_agent = Agent[FinancialDeps, FinancialAnalysis](
    model='openai:gpt-4',
    result_type=FinancialAnalysis,
    system_prompt="""You are an expert financial analyst.
    Analyze stocks using technical indicators, market data, and risk assessment.
    Provide comprehensive analysis with clear recommendations.
    Consider both quantitative metrics and qualitative factors.
    Always include risk assessment and rationale for recommendations."""
)

@financial_agent.tool
async def get_current_price(
    ctx: RunContext[FinancialDeps],
    symbol: str
) -> float:
    """Get current stock price.

    Args:
        symbol: Stock ticker symbol
    """
    return await ctx.deps.market_data.get_stock_price(symbol)

@financial_agent.tool
async def get_price_history(
    ctx: RunContext[FinancialDeps],
    symbol: str,
    days: int = 30
) -> List[Dict[str, Any]]:
    """Get historical price data.

    Args:
        symbol: Stock ticker symbol
        days: Number of days of history
    """
    data = await ctx.deps.market_data.get_historical_prices(symbol, days)
    return [d.dict() for d in data]

@financial_agent.tool
async def calculate_technical_indicators(
    ctx: RunContext[FinancialDeps],
    symbol: str
) -> Dict[str, float]:
    """Calculate technical indicators for a stock.

    Args:
        symbol: Stock ticker symbol
    """
    history = await ctx.deps.market_data.get_historical_prices(symbol, 30)
    prices = [h.close for h in history]

    ma20 = await ctx.deps.analytics.calculate_moving_average(prices, 20)
    volatility = await ctx.deps.analytics.calculate_volatility(prices)
    rsi = await ctx.deps.analytics.calculate_rsi(prices)

    return {
        'moving_average_20': ma20,
        'volatility': volatility,
        'rsi': rsi,
        'current_price': prices[-1] if prices else 0
    }

@financial_agent.tool
async def analyze_trend(
    ctx: RunContext[FinancialDeps],
    symbol: str
) -> str:
    """Analyze price trend for a stock.

    Args:
        symbol: Stock ticker symbol
    """
    history = await ctx.deps.market_data.get_historical_prices(symbol, 30)
    prices = [h.close for h in history]
    return await ctx.deps.analytics.detect_trend(prices)

@financial_agent.tool
async def assess_risk(
    ctx: RunContext[FinancialDeps],
    symbol: str
) -> Dict[str, str]:
    """Assess investment risk.

    Args:
        symbol: Stock ticker symbol
    """
    history = await ctx.deps.market_data.get_historical_prices(symbol, 30)
    prices = [h.close for h in history]

    volatility = await ctx.deps.analytics.calculate_volatility(prices)
    market_indicators = await ctx.deps.market_data.get_market_indicators()

    vol_risk = await ctx.deps.risk_engine.assess_volatility_risk(volatility)
    market_risk = await ctx.deps.risk_engine.assess_market_risk(market_indicators['vix'])

    return {
        'volatility_risk': vol_risk,
        'market_risk': market_risk,
        'market_sentiment': market_indicators['market_sentiment']
    }

@financial_agent.tool
async def get_market_context(ctx: RunContext[FinancialDeps]) -> Dict[str, Any]:
    """Get overall market context and indicators."""
    return await ctx.deps.market_data.get_market_indicators()

async def financial_analysis_example():
    """Demonstrate financial analysis agent."""

    # Initialize services
    market_data = MarketDataService()
    analytics = FinancialAnalyticsService()
    risk_engine = RiskEngine()

    deps = FinancialDeps(
        market_data=market_data,
        analytics=analytics,
        risk_engine=risk_engine
    )

    # Analyze stock
    symbol = "AAPL"

    print(f"Analyzing {symbol}...\n")

    result = await financial_agent.run(
        f"Provide a comprehensive financial analysis for {symbol} including technical indicators, trend analysis, and investment recommendation",
        deps=deps
    )

    analysis = result.data

    print("=" * 80)
    print(f"FINANCIAL ANALYSIS: {analysis.asset_symbol}")
    print("=" * 80)

    print(f"\nAnalysis Date: {analysis.analysis_date}")

    print(f"\nPRICE SUMMARY")
    print(f"{'─' * 80}")
    for key, value in analysis.price_summary.items():
        print(f"{key}: ${value:.2f}")

    print(f"\nKEY METRICS")
    print(f"{'─' * 80}")
    for metric in analysis.key_metrics:
        print(f"\n{metric.metric_name}: {metric.value:.2f} {metric.unit}")
        print(f"Interpretation: {metric.interpretation.upper()}")
        print(f"Explanation: {metric.explanation}")

    print(f"\nTREND ANALYSIS")
    print(f"{'─' * 80}")
    print(analysis.trend_analysis)

    print(f"\nRISK ASSESSMENT")
    print(f"{'─' * 80}")
    risk = analysis.risk_assessment
    print(f"Risk Level: {risk.risk_level.upper()}")
    print(f"Confidence: {risk.confidence:.1%}")

    print(f"\nRisk Factors:")
    for factor in risk.risk_factors:
        print(f"  • {factor}")

    print(f"\nMitigation Strategies:")
    for strategy in risk.mitigation_strategies:
        print(f"  • {strategy}")

    print(f"\nRECOMMENDATION")
    print(f"{'─' * 80}")
    print(f"Action: {analysis.recommendation.upper().replace('_', ' ')}")
    if analysis.target_price:
        print(f"Target Price: ${analysis.target_price:.2f}")
    print(f"\nRationale:")
    print(analysis.recommendation_rationale)

if __name__ == "__main__":
    asyncio.run(financial_analysis_example())
```

---

## Multi-Agent Systems

### Example 1: Content Creation Pipeline

```python
"""
Multi-agent content creation system with specialized agents.
Demonstrates agent collaboration and workflow orchestration.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Optional, Literal
import asyncio

# Output models for each agent
class ContentOutline(BaseModel):
    """Content outline from researcher."""
    title: str
    sections: List[str]
    key_points: List[str]
    target_audience: str
    tone: Literal['formal', 'casual', 'technical', 'friendly']

class DraftContent(BaseModel):
    """Draft content from writer."""
    title: str
    introduction: str
    body_sections: List[Dict[str, str]]  # {heading: content}
    conclusion: str
    word_count: int

class EditedContent(BaseModel):
    """Edited content from editor."""
    title: str
    content: str
    improvements_made: List[str]
    quality_score: float = Field(ge=0.0, le=10.0)
    seo_keywords: List[str]

class FinalArticle(BaseModel):
    """Final published article."""
    title: str
    content: str
    meta_description: str
    tags: List[str]
    estimated_read_time: int
    quality_metrics: Dict[str, Any]

@dataclass
class ContentDeps:
    """Shared dependencies for content pipeline."""
    topic: str
    target_length: int
    style_guide: Dict[str, str]

# Agent 1: Research Agent
research_agent = Agent[ContentDeps, ContentOutline](
    model='openai:gpt-4',
    result_type=ContentOutline,
    system_prompt="""You are a content researcher.
    Create detailed outlines for articles.
    Identify key points and structure content logically.
    Consider audience and appropriate tone."""
)

# Agent 2: Writer Agent
writer_agent = Agent[ContentDeps, DraftContent](
    model='openai:gpt-4',
    result_type=DraftContent,
    system_prompt="""You are a content writer.
    Write engaging, informative content based on outlines.
    Maintain consistent tone and style.
    Create clear, well-structured prose."""
)

# Agent 3: Editor Agent
editor_agent = Agent[ContentDeps, EditedContent](
    model='openai:gpt-4',
    result_type=EditedContent,
    system_prompt="""You are a content editor.
    Improve clarity, grammar, and flow.
    Optimize for SEO and readability.
    Ensure consistency and quality."""
)

# Agent 4: Publishing Agent
publishing_agent = Agent[ContentDeps, FinalArticle](
    model='openai:gpt-4',
    result_type=FinalArticle,
    system_prompt="""You are a publishing specialist.
    Prepare content for publication.
    Add metadata, tags, and descriptions.
    Calculate quality metrics."""
)

class ContentPipeline:
    """Orchestrate multi-agent content creation."""

    def __init__(self, deps: ContentDeps):
        self.deps = deps

    async def create_content(self) -> FinalArticle:
        """Run complete content creation pipeline."""

        print("=" * 80)
        print("CONTENT CREATION PIPELINE")
        print("=" * 80)

        # Step 1: Research and outline
        print("\n[1/4] Research Agent: Creating outline...")
        outline_result = await research_agent.run(
            f"Create a detailed outline for an article about: {self.deps.topic}",
            deps=self.deps
        )
        outline = outline_result.data
        print(f"✓ Outline created: {outline.title}")
        print(f"  Sections: {len(outline.sections)}")
        print(f"  Target audience: {outline.target_audience}")
        print(f"  Tone: {outline.tone}")

        # Step 2: Write draft
        print("\n[2/4] Writer Agent: Writing draft...")
        outline_text = f"""
        Title: {outline.title}
        Sections: {', '.join(outline.sections)}
        Key points: {', '.join(outline.key_points)}
        Tone: {outline.tone}
        Target length: {self.deps.target_length} words
        """

        draft_result = await writer_agent.run(
            f"Write an article based on this outline:\n{outline_text}",
            deps=self.deps
        )
        draft = draft_result.data
        print(f"✓ Draft completed: {draft.word_count} words")
        print(f"  Sections written: {len(draft.body_sections)}")

        # Step 3: Edit and improve
        print("\n[3/4] Editor Agent: Editing and optimizing...")
        draft_text = f"""
        Title: {draft.title}
        Introduction: {draft.introduction}
        Body: {draft.body_sections}
        Conclusion: {draft.conclusion}
        """

        edited_result = await editor_agent.run(
            f"Edit and improve this draft:\n{draft_text}",
            deps=self.deps
        )
        edited = edited_result.data
        print(f"✓ Editing completed")
        print(f"  Quality score: {edited.quality_score}/10")
        print(f"  Improvements: {len(edited.improvements_made)}")
        print(f"  SEO keywords: {', '.join(edited.seo_keywords[:5])}")

        # Step 4: Prepare for publishing
        print("\n[4/4] Publishing Agent: Preparing for publication...")
        final_result = await publishing_agent.run(
            f"""Prepare this content for publication:
            Title: {edited.title}
            Content: {edited.content}
            Keywords: {', '.join(edited.seo_keywords)}
            """,
            deps=self.deps
        )
        final = final_result.data
        print(f"✓ Ready for publication")
        print(f"  Meta description: {final.meta_description[:60]}...")
        print(f"  Tags: {', '.join(final.tags)}")
        print(f"  Read time: {final.estimated_read_time} minutes")

        return final

async def multi_agent_content_example():
    """Demonstrate multi-agent content creation."""

    deps = ContentDeps(
        topic="The Future of Artificial Intelligence in Healthcare",
        target_length=1500,
        style_guide={
            'voice': 'professional but accessible',
            'perspective': 'third person',
            'formatting': 'use headings and bullet points'
        }
    )

    pipeline = ContentPipeline(deps)
    final_article = await pipeline.create_content()

    print("\n" + "=" * 80)
    print("FINAL ARTICLE")
    print("=" * 80)
    print(f"\nTitle: {final_article.title}")
    print(f"\nMeta Description:\n{final_article.meta_description}")
    print(f"\nContent Preview:")
    print(final_article.content[:500] + "...")
    print(f"\nTags: {', '.join(final_article.tags)}")
    print(f"Estimated Read Time: {final_article.estimated_read_time} minutes")

    print(f"\nQuality Metrics:")
    for metric, value in final_article.quality_metrics.items():
        print(f"  {metric}: {value}")

if __name__ == "__main__":
    asyncio.run(multi_agent_content_example())
```

### Example 2: Customer Service Multi-Agent System

```python
"""
Multi-agent customer service system with specialized agents.
Demonstrates agent delegation and escalation patterns.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Optional, Literal, Dict, Any
import asyncio

class TicketClassification(BaseModel):
    """Ticket classification result."""
    category: Literal['technical', 'billing', 'general', 'complaint']
    priority: Literal['low', 'medium', 'high', 'urgent']
    requires_escalation: bool
    suggested_agent: str
    confidence: float = Field(ge=0.0, le=1.0)

class TechnicalSolution(BaseModel):
    """Technical support solution."""
    issue_identified: str
    solution_steps: List[str]
    estimated_resolution_time: str
    requires_followup: bool
    knowledge_base_articles: List[str]

class BillingResolution(BaseModel):
    """Billing issue resolution."""
    issue_type: str
    resolution: str
    refund_amount: Optional[float] = None
    account_adjustments: List[str]
    requires_manager_approval: bool

class CustomerResponse(BaseModel):
    """Final response to customer."""
    response_text: str
    resolution_status: Literal['resolved', 'pending', 'escalated']
    followup_required: bool
    followup_date: Optional[str] = None
    satisfaction_survey_sent: bool

@dataclass
class ServiceDeps:
    """Customer service dependencies."""
    ticket_id: str
    customer_id: str
    customer_history: List[Dict[str, Any]]

# Triage Agent
triage_agent = Agent[ServiceDeps, TicketClassification](
    model='openai:gpt-4',
    result_type=TicketClassification,
    system_prompt="""You are a customer service triage specialist.
    Classify tickets by category and priority.
    Determine if escalation is needed.
    Route to appropriate specialized agent."""
)

# Technical Support Agent
technical_agent = Agent[ServiceDeps, TechnicalSolution](
    model='openai:gpt-4',
    result_type=TechnicalSolution,
    system_prompt="""You are a technical support specialist.
    Diagnose technical issues systematically.
    Provide clear, step-by-step solutions.
    Reference knowledge base articles."""
)

# Billing Support Agent
billing_agent = Agent[ServiceDeps, BillingResolution](
    model='openai:gpt-4',
    result_type=BillingResolution,
    system_prompt="""You are a billing specialist.
    Resolve billing inquiries and disputes.
    Calculate refunds and adjustments accurately.
    Follow company refund policies."""
)

# Response Agent
response_agent = Agent[ServiceDeps, CustomerResponse](
    model='openai:gpt-4',
    result_type=CustomerResponse,
    system_prompt="""You are a customer service response specialist.
    Create professional, empathetic responses.
    Ensure customer satisfaction.
    Schedule appropriate followups."""
)

class CustomerServiceSystem:
    """Multi-agent customer service orchestrator."""

    def __init__(self, deps: ServiceDeps):
        self.deps = deps

    async def handle_ticket(self, customer_message: str) -> CustomerResponse:
        """Handle customer ticket through multi-agent system."""

        print(f"\n{'='*80}")
        print(f"TICKET #{self.deps.ticket_id}")
        print(f"{'='*80}")
        print(f"Customer: {self.deps.customer_id}")
        print(f"Message: {customer_message}\n")

        # Step 1: Triage
        print("[1] Triage Agent: Classifying ticket...")
        classification_result = await triage_agent.run(
            f"Classify this customer ticket:\n{customer_message}",
            deps=self.deps
        )
        classification = classification_result.data

        print(f"✓ Classification:")
        print(f"  Category: {classification.category}")
        print(f"  Priority: {classification.priority}")
        print(f"  Suggested Agent: {classification.suggested_agent}")
        print(f"  Escalation needed: {classification.requires_escalation}")

        # Step 2: Route to specialized agent
        solution_text = ""

        if classification.category == 'technical':
            print("\n[2] Technical Support Agent: Analyzing issue...")
            tech_result = await technical_agent.run(
                f"Provide technical support for:\n{customer_message}",
                deps=self.deps
            )
            tech_solution = tech_result.data

            print(f"✓ Technical Solution:")
            print(f"  Issue: {tech_solution.issue_identified}")
            print(f"  Steps: {len(tech_solution.solution_steps)}")
            print(f"  Resolution time: {tech_solution.estimated_resolution_time}")

            solution_text = f"""
            Issue: {tech_solution.issue_identified}
            Solution Steps:
            {chr(10).join(f"{i+1}. {step}" for i, step in enumerate(tech_solution.solution_steps))}
            Estimated time: {tech_solution.estimated_resolution_time}
            """

        elif classification.category == 'billing':
            print("\n[2] Billing Support Agent: Processing request...")
            billing_result = await billing_agent.run(
                f"Resolve billing issue:\n{customer_message}",
                deps=self.deps
            )
            billing_solution = billing_result.data

            print(f"✓ Billing Resolution:")
            print(f"  Issue type: {billing_solution.issue_type}")
            print(f"  Refund: ${billing_solution.refund_amount or 0}")
            print(f"  Manager approval: {billing_solution.requires_manager_approval}")

            solution_text = f"""
            Issue: {billing_solution.issue_type}
            Resolution: {billing_solution.resolution}
            """
            if billing_solution.refund_amount:
                solution_text += f"\nRefund amount: ${billing_solution.refund_amount}"

        else:
            # General inquiry
            solution_text = "General inquiry processed by standard procedures."

        # Step 3: Generate customer response
        print("\n[3] Response Agent: Crafting response...")
        response_result = await response_agent.run(
            f"""Create a customer response based on:
            Original message: {customer_message}
            Classification: {classification.category} - {classification.priority}
            Solution: {solution_text}
            """,
            deps=self.deps
        )
        final_response = response_result.data

        print(f"✓ Response prepared:")
        print(f"  Status: {final_response.resolution_status}")
        print(f"  Followup: {final_response.followup_required}")
        print(f"  Survey sent: {final_response.satisfaction_survey_sent}")

        return final_response

async def multi_agent_service_example():
    """Demonstrate multi-agent customer service."""

    # Example tickets
    tickets = [
        {
            'id': 'T001',
            'customer': 'C12345',
            'message': "My application keeps crashing when I try to upload files larger than 10MB. This is very urgent as I need to submit a project today.",
            'history': []
        },
        {
            'id': 'T002',
            'customer': 'C67890',
            'message': "I was charged twice for my subscription this month. Can you please refund the duplicate charge?",
            'history': [{'type': 'purchase', 'date': '2024-01-15'}]
        }
    ]

    for ticket in tickets:
        deps = ServiceDeps(
            ticket_id=ticket['id'],
            customer_id=ticket['customer'],
            customer_history=ticket['history']
        )

        system = CustomerServiceSystem(deps)
        response = await system.handle_ticket(ticket['message'])

        print(f"\n{'─'*80}")
        print("FINAL CUSTOMER RESPONSE:")
        print(f"{'─'*80}")
        print(response.response_text)
        print(f"\nStatus: {response.resolution_status.upper()}")

        if response.followup_required and response.followup_date:
            print(f"Followup scheduled: {response.followup_date}")

        print("\n")

if __name__ == "__main__":
    asyncio.run(multi_agent_service_example())
```

### Example 3: Code Review Multi-Agent System

```python
"""
Multi-agent code review system with specialized reviewers.
Demonstrates parallel agent execution and consensus building.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Literal, Dict, Any
import asyncio

class CodeIssue(BaseModel):
    """Individual code issue."""
    severity: Literal['critical', 'major', 'minor', 'suggestion']
    category: str
    line_number: Optional[int] = None
    description: str
    suggestion: str

class ReviewResult(BaseModel):
    """Review result from a single agent."""
    reviewer_type: str
    overall_rating: float = Field(ge=0.0, le=10.0)
    issues_found: List[CodeIssue]
    strengths: List[str]
    summary: str

class ConsolidatedReview(BaseModel):
    """Final consolidated review."""
    overall_score: float = Field(ge=0.0, le=10.0)
    all_issues: List[CodeIssue]
    consensus_strengths: List[str]
    recommended_actions: List[str]
    approval_status: Literal['approved', 'approved_with_comments', 'changes_requested', 'rejected']
    reviewer_summaries: Dict[str, str]

# Security Reviewer Agent
security_agent = Agent[None, ReviewResult](
    model='openai:gpt-4',
    result_type=ReviewResult,
    system_prompt="""You are a security code reviewer.
    Focus on security vulnerabilities:
    - Input validation
    - Authentication/authorization
    - Data exposure
    - Injection attacks
    - Cryptography issues"""
)

# Performance Reviewer Agent
performance_agent = Agent[None, ReviewResult](
    model='openai:gpt-4',
    result_type=ReviewResult,
    system_prompt="""You are a performance code reviewer.
    Focus on performance issues:
    - Algorithm efficiency
    - Memory usage
    - Database queries
    - Caching opportunities
    - Scalability concerns"""
)

# Code Quality Reviewer Agent
quality_agent = Agent[None, ReviewResult](
    model='openai:gpt-4',
    result_type=ReviewResult,
    system_prompt="""You are a code quality reviewer.
    Focus on code quality:
    - Readability
    - Maintainability
    - Design patterns
    - Code organization
    - Documentation"""
)

# Consolidation Agent
consolidation_agent = Agent[None, ConsolidatedReview](
    model='openai:gpt-4',
    result_type=ConsolidatedReview,
    system_prompt="""You are a senior code reviewer.
    Consolidate reviews from multiple specialists.
    Prioritize issues and create final recommendation.
    Build consensus and provide clear guidance."""
)

class CodeReviewSystem:
    """Multi-agent code review orchestrator."""

    async def review_code(self, code: str, context: str = "") -> ConsolidatedReview:
        """Perform comprehensive code review."""

        print("=" * 80)
        print("CODE REVIEW SYSTEM")
        print("=" * 80)

        prompt = f"""Review this code:

```python
{code}
```

Context: {context}
"""

        # Run all specialized reviews in parallel
        print("\nRunning parallel reviews...")
        print("  - Security review")
        print("  - Performance review")
        print("  - Code quality review")

        security_task = security_agent.run(prompt)
        performance_task = performance_agent.run(prompt)
        quality_task = quality_agent.run(prompt)

        # Wait for all reviews
        security_result, performance_result, quality_result = await asyncio.gather(
            security_task,
            performance_task,
            quality_task
        )

        security_review = security_result.data
        performance_review = performance_result.data
        quality_review = quality_result.data

        print("\n✓ All reviews completed")
        print(f"  Security score: {security_review.overall_rating}/10")
        print(f"  Performance score: {performance_review.overall_rating}/10")
        print(f"  Quality score: {quality_review.overall_rating}/10")

        # Consolidate reviews
        print("\nConsolidating reviews...")

        consolidation_prompt = f"""
        Consolidate these code reviews:

        SECURITY REVIEW (Rating: {security_review.overall_rating}/10):
        {security_review.summary}
        Issues: {len(security_review.issues_found)}

        PERFORMANCE REVIEW (Rating: {performance_review.overall_rating}/10):
        {performance_review.summary}
        Issues: {len(performance_review.issues_found)}

        QUALITY REVIEW (Rating: {quality_review.overall_rating}/10):
        {quality_review.summary}
        Issues: {len(quality_review.issues_found)}

        All issues:
        {[issue.dict() for issue in security_review.issues_found + performance_review.issues_found + quality_review.issues_found]}
        """

        consolidated_result = await consolidation_agent.run(consolidation_prompt)
        consolidated = consolidated_result.data

        print("✓ Consolidation complete")
        print(f"  Overall score: {consolidated.overall_score}/10")
        print(f"  Total issues: {len(consolidated.all_issues)}")
        print(f"  Status: {consolidated.approval_status}")

        return consolidated

async def code_review_example():
    """Demonstrate multi-agent code review."""

    # Sample code to review
    code = '''
def process_user_data(user_input):
    # Process user data
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    results = database.execute(query)

    data = []
    for row in results:
        data.append(row)

    return data

def calculate_total(items):
    total = 0
    for item in items:
        for i in range(len(items)):
            total += item['price']
    return total
'''

    context = "This code is part of a user management system that handles customer data."

    system = CodeReviewSystem()
    review = await system.review_code(code, context)

    print("\n" + "=" * 80)
    print("CONSOLIDATED CODE REVIEW")
    print("=" * 80)

    print(f"\nOverall Score: {review.overall_score}/10")
    print(f"Status: {review.approval_status.upper().replace('_', ' ')}")

    print(f"\nISSUES FOUND ({len(review.all_issues)}):")
    print("─" * 80)

    # Group by severity
    critical = [i for i in review.all_issues if i.severity == 'critical']
    major = [i for i in review.all_issues if i.severity == 'major']
    minor = [i for i in review.all_issues if i.severity == 'minor']

    for severity, issues in [('CRITICAL', critical), ('MAJOR', major), ('MINOR', minor)]:
        if issues:
            print(f"\n{severity} ({len(issues)}):")
            for issue in issues:
                print(f"\n  Category: {issue.category}")
                if issue.line_number:
                    print(f"  Line: {issue.line_number}")
                print(f"  Description: {issue.description}")
                print(f"  Suggestion: {issue.suggestion}")

    if review.consensus_strengths:
        print(f"\nSTRENGTHS:")
        print("─" * 80)
        for strength in review.consensus_strengths:
            print(f"  • {strength}")

    print(f"\nRECOMMENDED ACTIONS:")
    print("─" * 80)
    for i, action in enumerate(review.recommended_actions, 1):
        print(f"  {i}. {action}")

    print(f"\nREVIEWER SUMMARIES:")
    print("─" * 80)
    for reviewer, summary in review.reviewer_summaries.items():
        print(f"\n{reviewer}:")
        print(f"  {summary}")

if __name__ == "__main__":
    asyncio.run(code_review_example())
```

---

## RAG with Agents / Agentic RAG

### Example 1: Basic RAG Agent with Vector Database

```python
"""
RAG agent with vector database for document retrieval.
Demonstrates retrieval-augmented generation with PydanticAI.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import asyncio
import numpy as np
from datetime import datetime

class Document(BaseModel):
    """Document model."""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None

class RetrievalResult(BaseModel):
    """Retrieved document with relevance score."""
    document: Document
    relevance_score: float = Field(ge=0.0, le=1.0)
    snippet: str

class RAGResponse(BaseModel):
    """RAG-enhanced response."""
    answer: str
    sources: List[RetrievalResult]
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str

@dataclass
class RAGDeps:
    """RAG system dependencies."""
    vector_store: 'VectorStore'
    embedding_service: 'EmbeddingService'

class EmbeddingService:
    """Mock embedding service."""

    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text."""
        # Mock embedding (in production, use actual embedding model)
        np.random.seed(hash(text) % 2**32)
        return np.random.rand(384).tolist()

    async def embed_query(self, query: str) -> List[float]:
        """Generate embedding for search query."""
        return await self.embed_text(query)

class VectorStore:
    """Mock vector database."""

    def __init__(self):
        self.documents: List[Document] = []
        self._initialized = False

    async def initialize(self):
        """Initialize with sample documents."""
        if self._initialized:
            return

        sample_docs = [
            {
                'id': 'doc1',
                'content': 'PydanticAI is a Python framework for building type-safe AI agents. It provides excellent developer experience with full type hints and validation.',
                'metadata': {'source': 'documentation', 'date': '2024-01-15'}
            },
            {
                'id': 'doc2',
                'content': 'Agents in PydanticAI can use tools to interact with external systems. Tools are defined as Python functions with type hints.',
                'metadata': {'source': 'guide', 'date': '2024-01-20'}
            },
            {
                'id': 'doc3',
                'content': 'Dependency injection in PydanticAI allows clean separation of concerns. Dependencies are passed through RunContext.',
                'metadata': {'source': 'tutorial', 'date': '2024-02-01'}
            },
            {
                'id': 'doc4',
                'content': 'Structured outputs in PydanticAI use Pydantic models for validation. This ensures type-safe responses from LLMs.',
                'metadata': {'source': 'documentation', 'date': '2024-02-10'}
            },
            {
                'id': 'doc5',
                'content': 'PydanticAI supports multiple LLM providers including OpenAI, Anthropic, and Google Gemini through a unified interface.',
                'metadata': {'source': 'guide', 'date': '2024-02-15'}
            }
        ]

        embedding_service = EmbeddingService()
        for doc_data in sample_docs:
            embedding = await embedding_service.embed_text(doc_data['content'])
            doc = Document(
                id=doc_data['id'],
                content=doc_data['content'],
                metadata=doc_data['metadata'],
                embedding=embedding
            )
            self.documents.append(doc)

        self._initialized = True

    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 3,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """Search for similar documents."""
        if not self._initialized:
            await self.initialize()

        # Calculate cosine similarity
        query_vec = np.array(query_embedding)
        results = []

        for doc in self.documents:
            if filter_metadata:
                # Apply metadata filters
                if not all(doc.metadata.get(k) == v for k, v in filter_metadata.items()):
                    continue

            doc_vec = np.array(doc.embedding)
            similarity = np.dot(query_vec, doc_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
            )
            results.append((doc, float(similarity)))

        # Sort by similarity and return top_k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

# Create RAG agent
rag_agent = Agent[RAGDeps, RAGResponse](
    model='openai:gpt-4',
    result_type=RAGResponse,
    system_prompt="""You are a knowledgeable assistant with access to a document database.
    Use the search tool to find relevant information before answering questions.
    Always cite your sources and provide accurate, well-supported answers.
    If information is not found, clearly state that."""
)

@rag_agent.tool
async def search_documents(
    ctx: RunContext[RAGDeps],
    query: str,
    num_results: int = 3
) -> List[Dict[str, Any]]:
    """Search the document database for relevant information.

    Args:
        query: Search query
        num_results: Number of results to return
    """
    # Generate query embedding
    query_embedding = await ctx.deps.embedding_service.embed_query(query)

    # Search vector store
    results = await ctx.deps.vector_store.search(
        query_embedding,
        top_k=num_results
    )

    # Format results
    formatted_results = []
    for doc, score in results:
        formatted_results.append({
            'id': doc.id,
            'content': doc.content,
            'metadata': doc.metadata,
            'relevance_score': score,
            'snippet': doc.content[:200] + '...' if len(doc.content) > 200 else doc.content
        })

    return formatted_results

async def rag_example():
    """Demonstrate RAG agent."""

    # Initialize dependencies
    vector_store = VectorStore()
    await vector_store.initialize()
    embedding_service = EmbeddingService()

    deps = RAGDeps(
        vector_store=vector_store,
        embedding_service=embedding_service
    )

    # Ask questions
    questions = [
        "What is PydanticAI and what are its main features?",
        "How do I use tools in PydanticAI?",
        "Which LLM providers does PydanticAI support?",
        "How does dependency injection work?"
    ]

    for question in questions:
        print(f"\n{'='*80}")
        print(f"Question: {question}")
        print(f"{'='*80}\n")

        result = await rag_agent.run(question, deps=deps)
        response = result.data

        print(f"Answer:\n{response.answer}\n")
        print(f"Confidence: {response.confidence:.1%}")
        print(f"Reasoning: {response.reasoning}\n")

        if response.sources:
            print(f"Sources ({len(response.sources)}):")
            for i, source in enumerate(response.sources, 1):
                print(f"\n{i}. Document {source.document.id}")
                print(f"   Relevance: {source.relevance_score:.1%}")
                print(f"   Snippet: {source.snippet}")
                print(f"   Metadata: {source.document.metadata}")

if __name__ == "__main__":
    asyncio.run(rag_example())
```

### Example 2: Agentic RAG with Query Rewriting

```python
"""
Advanced RAG agent with query rewriting and multi-step retrieval.
Demonstrates agentic RAG patterns.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import asyncio

class QueryPlan(BaseModel):
    """Query decomposition and planning."""
    original_query: str
    sub_queries: List[str]
    search_strategy: str
    expected_document_types: List[str]

class EnhancedRAGResponse(BaseModel):
    """Enhanced RAG response with reasoning."""
    answer: str
    sources: List[Dict[str, Any]]
    query_plan: QueryPlan
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning_steps: List[str]

@dataclass
class AgenticRAGDeps:
    """Agentic RAG dependencies."""
    vector_store: 'VectorStore'
    embedding_service: 'EmbeddingService'
    query_history: List[str]

# Query Planning Agent
query_planner = Agent[AgenticRAGDeps, QueryPlan](
    model='openai:gpt-4',
    result_type=QueryPlan,
    system_prompt="""You are a query planning specialist.
    Analyze user queries and break them down into sub-queries.
    Plan an effective search strategy.
    Consider what types of documents would be most relevant."""
)

# RAG Agent with advanced retrieval
agentic_rag_agent = Agent[AgenticRAGDeps, EnhancedRAGResponse](
    model='openai:gpt-4',
    result_type=EnhancedRAGResponse,
    system_prompt="""You are an advanced RAG assistant.
    Use query planning to break down complex questions.
    Perform multiple searches if needed.
    Synthesize information from multiple sources.
    Show your reasoning process."""
)

@agentic_rag_agent.tool
async def plan_query(
    ctx: RunContext[AgenticRAGDeps],
    query: str
) -> QueryPlan:
    """Plan how to search for information.

    Args:
        query: User's question
    """
    result = await query_planner.run(
        f"Create a search plan for: {query}",
        deps=ctx.deps
    )
    return result.data

@agentic_rag_agent.tool
async def search_with_plan(
    ctx: RunContext[AgenticRAGDeps],
    sub_query: str,
    document_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search documents using a sub-query.

    Args:
        sub_query: Specific search query
        document_type: Optional document type filter
    """
    query_embedding = await ctx.deps.embedding_service.embed_query(sub_query)

    filter_metadata = {'source': document_type} if document_type else None

    results = await ctx.deps.vector_store.search(
        query_embedding,
        top_k=3,
        filter_metadata=filter_metadata
    )

    return [
        {
            'id': doc.id,
            'content': doc.content,
            'metadata': doc.metadata,
            'relevance_score': score
        }
        for doc, score in results
    ]

@agentic_rag_agent.tool
async def synthesize_information(
    ctx: RunContext[AgenticRAGDeps],
    documents: List[Dict[str, Any]],
    original_query: str
) -> str:
    """Synthesize information from multiple documents.

    Args:
        documents: Retrieved documents
        original_query: Original user query
    """
    # Combine document contents
    combined = "\n\n".join([
        f"Document {doc['id']}: {doc['content']}"
        for doc in documents
    ])

    return f"Synthesized from {len(documents)} documents addressing: {original_query}\n\n{combined}"

async def agentic_rag_example():
    """Demonstrate agentic RAG."""

    # Initialize dependencies
    vector_store = VectorStore()
    await vector_store.initialize()
    embedding_service = EmbeddingService()

    deps = AgenticRAGDeps(
        vector_store=vector_store,
        embedding_service=embedding_service,
        query_history=[]
    )

    # Complex question requiring multi-step retrieval
    question = "Compare how tools and dependency injection work in PydanticAI, and explain their relationship"

    print(f"{'='*80}")
    print(f"Question: {question}")
    print(f"{'='*80}\n")

    result = await agentic_rag_agent.run(question, deps=deps)
    response = result.data

    print(f"QUERY PLAN")
    print(f"{'─'*80}")
    print(f"Strategy: {response.query_plan.search_strategy}")
    print(f"Sub-queries: {len(response.query_plan.sub_queries)}")
    for i, sq in enumerate(response.query_plan.sub_queries, 1):
        print(f"  {i}. {sq}")
    print(f"Expected document types: {', '.join(response.query_plan.expected_document_types)}")

    print(f"\nREASONING STEPS")
    print(f"{'─'*80}")
    for i, step in enumerate(response.reasoning_steps, 1):
        print(f"{i}. {step}")

    print(f"\nANSWER")
    print(f"{'─'*80}")
    print(response.answer)

    print(f"\nSOURCES ({len(response.sources)})")
    print(f"{'─'*80}")
    for i, source in enumerate(response.sources, 1):
        print(f"\n{i}. {source.get('id', 'Unknown')}")
        print(f"   Content: {source.get('content', '')[:100]}...")

    print(f"\nConfidence: {response.confidence:.1%}")

if __name__ == "__main__":
    asyncio.run(agentic_rag_example())
```

### Example 3: RAG with Hybrid Search

```python
"""
RAG agent with hybrid search (vector + keyword).
Demonstrates combining multiple retrieval strategies.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Dict, Any, Literal
import asyncio

class SearchResult(BaseModel):
    """Search result with multiple scores."""
    document_id: str
    content: str
    vector_score: float = Field(ge=0.0, le=1.0)
    keyword_score: float = Field(ge=0.0, le=1.0)
    hybrid_score: float = Field(ge=0.0, le=1.0)
    rank: int

class HybridRAGResponse(BaseModel):
    """Hybrid RAG response."""
    answer: str
    search_results: List[SearchResult]
    search_method: Literal['vector', 'keyword', 'hybrid']
    total_documents_searched: int
    confidence: float = Field(ge=0.0, le=1.0)

@dataclass
class HybridRAGDeps:
    """Hybrid RAG dependencies."""
    vector_store: 'VectorStore'
    keyword_index: 'KeywordIndex'
    embedding_service: 'EmbeddingService'

class KeywordIndex:
    """Simple keyword search index."""

    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.inverted_index: Dict[str, List[str]] = {}
        self._build_index()

    def _build_index(self):
        """Build inverted index."""
        for doc in self.documents:
            words = doc.content.lower().split()
            for word in set(words):  # Unique words
                if word not in self.inverted_index:
                    self.inverted_index[word] = []
                self.inverted_index[word].append(doc.id)

    async def search(self, query: str, top_k: int = 5) -> List[tuple[Document, float]]:
        """Keyword-based search."""
        query_words = set(query.lower().split())
        doc_scores: Dict[str, float] = {}

        # Calculate TF-IDF-like scores
        for word in query_words:
            if word in self.inverted_index:
                doc_ids = self.inverted_index[word]
                idf = 1.0 / len(doc_ids)  # Simple IDF
                for doc_id in doc_ids:
                    doc_scores[doc_id] = doc_scores.get(doc_id, 0) + idf

        # Get top documents
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []

        for doc_id, score in sorted_docs[:top_k]:
            doc = next((d for d in self.documents if d.id == doc_id), None)
            if doc:
                # Normalize score
                normalized_score = score / max(doc_scores.values()) if doc_scores else 0
                results.append((doc, normalized_score))

        return results

# Hybrid RAG Agent
hybrid_rag_agent = Agent[HybridRAGDeps, HybridRAGResponse](
    model='openai:gpt-4',
    result_type=HybridRAGResponse,
    system_prompt="""You are a hybrid search RAG assistant.
    Use both vector and keyword search to find relevant information.
    Combine results using reciprocal rank fusion.
    Provide comprehensive answers with proper citations."""
)

@hybrid_rag_agent.tool
async def vector_search(
    ctx: RunContext[HybridRAGDeps],
    query: str,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """Perform vector similarity search.

    Args:
        query: Search query
        top_k: Number of results
    """
    query_embedding = await ctx.deps.embedding_service.embed_query(query)
    results = await ctx.deps.vector_store.search(query_embedding, top_k=top_k)

    return [
        {
            'doc_id': doc.id,
            'content': doc.content,
            'score': score,
            'method': 'vector'
        }
        for doc, score in results
    ]

@hybrid_rag_agent.tool
async def keyword_search(
    ctx: RunContext[HybridRAGDeps],
    query: str,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """Perform keyword-based search.

    Args:
        query: Search query
        top_k: Number of results
    """
    results = await ctx.deps.keyword_index.search(query, top_k=top_k)

    return [
        {
            'doc_id': doc.id,
            'content': doc.content,
            'score': score,
            'method': 'keyword'
        }
        for doc, score in results
    ]

@hybrid_rag_agent.tool
async def hybrid_search(
    ctx: RunContext[HybridRAGDeps],
    query: str,
    top_k: int = 5,
    alpha: float = 0.5
) -> List[Dict[str, Any]]:
    """Perform hybrid search combining vector and keyword methods.

    Args:
        query: Search query
        top_k: Number of results
        alpha: Weight for vector search (1-alpha for keyword)
    """
    # Get results from both methods
    vector_results = await vector_search(ctx, query, top_k=top_k)
    keyword_results = await keyword_search(ctx, query, top_k=top_k)

    # Combine using reciprocal rank fusion
    combined_scores: Dict[str, Dict[str, Any]] = {}

    for rank, result in enumerate(vector_results, 1):
        doc_id = result['doc_id']
        combined_scores[doc_id] = {
            'content': result['content'],
            'vector_score': result['score'],
            'vector_rank': rank,
            'keyword_score': 0,
            'keyword_rank': 0
        }

    for rank, result in enumerate(keyword_results, 1):
        doc_id = result['doc_id']
        if doc_id not in combined_scores:
            combined_scores[doc_id] = {
                'content': result['content'],
                'vector_score': 0,
                'vector_rank': 0,
                'keyword_score': result['score'],
                'keyword_rank': rank
            }
        else:
            combined_scores[doc_id]['keyword_score'] = result['score']
            combined_scores[doc_id]['keyword_rank'] = rank

    # Calculate hybrid scores using RRF
    k = 60  # RRF constant
    for doc_id, scores in combined_scores.items():
        rrf_score = 0
        if scores['vector_rank'] > 0:
            rrf_score += alpha / (k + scores['vector_rank'])
        if scores['keyword_rank'] > 0:
            rrf_score += (1 - alpha) / (k + scores['keyword_rank'])

        scores['hybrid_score'] = rrf_score

    # Sort by hybrid score
    sorted_results = sorted(
        combined_scores.items(),
        key=lambda x: x[1]['hybrid_score'],
        reverse=True
    )

    return [
        {
            'doc_id': doc_id,
            'content': scores['content'],
            'vector_score': scores['vector_score'],
            'keyword_score': scores['keyword_score'],
            'hybrid_score': scores['hybrid_score'],
            'method': 'hybrid'
        }
        for doc_id, scores in sorted_results[:top_k]
    ]

async def hybrid_rag_example():
    """Demonstrate hybrid RAG."""

    # Initialize dependencies
    vector_store = VectorStore()
    await vector_store.initialize()
    keyword_index = KeywordIndex(vector_store.documents)
    embedding_service = EmbeddingService()

    deps = HybridRAGDeps(
        vector_store=vector_store,
        keyword_index=keyword_index,
        embedding_service=embedding_service
    )

    # Test different search strategies
    query = "type-safe validation with Pydantic models"

    print(f"{'='*80}")
    print(f"Query: {query}")
    print(f"{'='*80}\n")

    result = await hybrid_rag_agent.run(
        f"Search for information about: {query}\nUse hybrid search for best results.",
        deps=deps
    )
    response = result.data

    print(f"Search Method: {response.search_method.upper()}")
    print(f"Documents Searched: {response.total_documents_searched}")
    print(f"Confidence: {response.confidence:.1%}\n")

    print(f"SEARCH RESULTS ({len(response.search_results)})")
    print(f"{'─'*80}")
    for result in response.search_results:
        print(f"\nRank {result.rank}: Document {result.document_id}")
        print(f"  Vector Score: {result.vector_score:.3f}")
        print(f"  Keyword Score: {result.keyword_score:.3f}")
        print(f"  Hybrid Score: {result.hybrid_score:.3f}")
        print(f"  Content: {result.content[:100]}...")

    print(f"\nANSWER")
    print(f"{'─'*80}")
    print(response.answer)

if __name__ == "__main__":
    asyncio.run(hybrid_rag_example())
```

---

## FastMCP Servers with Agents

### Example 1: PydanticAI Agent with FastMCP Tools

```python
"""
PydanticAI agent using FastMCP server tools.
Demonstrates MCP protocol integration with agents.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import asyncio

class MCPToolResult(BaseModel):
    """Result from MCP tool invocation."""
    tool_name: str
    result: Any
    execution_time: float
    success: bool
    error_message: Optional[str] = None

class AgentWithMCPResponse(BaseModel):
    """Response from agent using MCP tools."""
    answer: str
    tools_used: List[MCPToolResult]
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)

@dataclass
class MCPDeps:
    """MCP integration dependencies."""
    mcp_client: 'MCPClient'
    tool_registry: 'MCPToolRegistry'

class MCPToolRegistry:
    """Registry of available MCP tools."""

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {
            'filesystem_read': {
                'description': 'Read file contents',
                'parameters': {'path': 'string'},
                'server': 'filesystem'
            },
            'filesystem_write': {
                'description': 'Write to file',
                'parameters': {'path': 'string', 'content': 'string'},
                'server': 'filesystem'
            },
            'database_query': {
                'description': 'Query database',
                'parameters': {'query': 'string'},
                'server': 'database'
            },
            'web_fetch': {
                'description': 'Fetch web page',
                'parameters': {'url': 'string'},
                'server': 'web'
            }
        }

    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all available MCP tools."""
        return [
            {
                'name': name,
                **details
            }
            for name, details in self.tools.items()
        ]

    async def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool."""
        return self.tools.get(tool_name)

class MCPClient:
    """Mock MCP client for tool invocation."""

    async def invoke_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> MCPToolResult:
        """Invoke an MCP tool."""
        import time
        start_time = time.time()

        try:
            # Mock tool execution
            if tool_name == 'filesystem_read':
                result = f"Contents of {parameters.get('path')}: Sample file content"
                success = True
                error = None
            elif tool_name == 'database_query':
                result = [
                    {'id': 1, 'name': 'Record 1'},
                    {'id': 2, 'name': 'Record 2'}
                ]
                success = True
                error = None
            elif tool_name == 'web_fetch':
                result = f"<html>Content from {parameters.get('url')}</html>"
                success = True
                error = None
            else:
                result = None
                success = False
                error = f"Unknown tool: {tool_name}"

            execution_time = time.time() - start_time

            return MCPToolResult(
                tool_name=tool_name,
                result=result,
                execution_time=execution_time,
                success=success,
                error_message=error
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return MCPToolResult(
                tool_name=tool_name,
                result=None,
                execution_time=execution_time,
                success=False,
                error_message=str(e)
            )

# Agent with MCP integration
mcp_agent = Agent[MCPDeps, AgentWithMCPResponse](
    model='openai:gpt-4',
    result_type=AgentWithMCPResponse,
    system_prompt="""You are an agent with access to MCP server tools.
    Use available tools to accomplish tasks.
    Check tool registry to see what tools are available.
    Handle tool errors gracefully."""
)

@mcp_agent.tool
async def list_available_tools(ctx: RunContext[MCPDeps]) -> List[Dict[str, Any]]:
    """List all available MCP tools."""
    return await ctx.deps.tool_registry.list_tools()

@mcp_agent.tool
async def call_mcp_tool(
    ctx: RunContext[MCPDeps],
    tool_name: str,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """Call an MCP tool with parameters.

    Args:
        tool_name: Name of the MCP tool
        parameters: Tool parameters
    """
    # Validate tool exists
    tool_info = await ctx.deps.tool_registry.get_tool_info(tool_name)
    if not tool_info:
        return {
            'success': False,
            'error': f'Tool {tool_name} not found'
        }

    # Invoke tool through MCP client
    result = await ctx.deps.mcp_client.invoke_tool(tool_name, parameters)

    return {
        'success': result.success,
        'result': result.result,
        'execution_time': result.execution_time,
        'error': result.error_message
    }

async def mcp_agent_example():
    """Demonstrate agent with MCP tools."""

    # Initialize dependencies
    mcp_client = MCPClient()
    tool_registry = MCPToolRegistry()

    deps = MCPDeps(
        mcp_client=mcp_client,
        tool_registry=tool_registry
    )

    # Task requiring MCP tools
    task = "Read the config file at /etc/config.json and then query the database for user records"

    print(f"{'='*80}")
    print(f"Task: {task}")
    print(f"{'='*80}\n")

    result = await mcp_agent.run(task, deps=deps)
    response = result.data

    print(f"TOOLS USED ({len(response.tools_used)})")
    print(f"{'─'*80}")
    for tool_result in response.tools_used:
        print(f"\nTool: {tool_result.tool_name}")
        print(f"  Success: {tool_result.success}")
        print(f"  Execution Time: {tool_result.execution_time:.3f}s")
        if tool_result.error_message:
            print(f"  Error: {tool_result.error_message}")
        else:
            print(f"  Result: {str(tool_result.result)[:100]}...")

    print(f"\nREASONING")
    print(f"{'─'*80}")
    print(response.reasoning)

    print(f"\nANSWER")
    print(f"{'─'*80}")
    print(response.answer)

    print(f"\nConfidence: {response.confidence:.1%}")

if __name__ == "__main__":
    asyncio.run(mcp_agent_example())
```

### Example 2: Multi-Server MCP Integration

```python
"""
Agent coordinating multiple MCP servers.
Demonstrates complex MCP orchestration.
"""

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Dict, Any
import asyncio

class ServerStatus(BaseModel):
    """MCP server status."""
    server_name: str
    is_connected: bool
    available_tools: List[str]
    latency_ms: float

class MultiServerResponse(BaseModel):
    """Response from multi-server orchestration."""
    answer: str
    servers_used: List[ServerStatus]
    total_tools_invoked: int
    workflow_steps: List[str]

@dataclass
class MultiServerDeps:
    """Multi-server MCP dependencies."""
    mcp_servers: Dict[str, 'MCPServer']
    orchestrator: 'MCPOrchestrator'

class MCPServer:
    """Mock MCP server."""

    def __init__(self, name: str, tools: List[str]):
        self.name = name
        self.tools = tools
        self.is_connected = True

    async def get_status(self) -> ServerStatus:
        """Get server status."""
        return ServerStatus(
            server_name=self.name,
            is_connected=self.is_connected,
            available_tools=self.tools,
            latency_ms=10.0 + (len(self.tools) * 2)
        )

    async def invoke_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Invoke a tool on this server."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not available on {self.name}")

        # Mock implementation
        await asyncio.sleep(0.1)  # Simulate network delay
        return {
            'server': self.name,
            'tool': tool_name,
            'result': f'Result from {self.name}.{tool_name}',
            'params': params
        }

class MCPOrchestrator:
    """Orchestrate multiple MCP servers."""

    def __init__(self, servers: Dict[str, MCPServer]):
        self.servers = servers

    async def find_tool(self, tool_name: str) -> Optional[str]:
        """Find which server provides a tool."""
        for server_name, server in self.servers.items():
            if tool_name in server.tools:
                return server_name
        return None

    async def execute_workflow(
        self,
        workflow: List[Dict[str, Any]]
    ) -> List[Any]:
        """Execute a workflow across multiple servers."""
        results = []
        for step in workflow:
            server_name = step['server']
            tool_name = step['tool']
            params = step.get('params', {})

            if server_name in self.servers:
                result = await self.servers[server_name].invoke_tool(
                    tool_name,
                    params
                )
                results.append(result)

        return results

# Multi-server agent
multi_server_agent = Agent[MultiServerDeps, MultiServerResponse](
    model='openai:gpt-4',
    result_type=MultiServerResponse,
    system_prompt="""You are an orchestrator agent managing multiple MCP servers.
    Coordinate tasks across different servers.
    Plan efficient workflows utilizing appropriate servers.
    Handle server failures gracefully."""
)

@multi_server_agent.tool
async def check_server_status(
    ctx: RunContext[MultiServerDeps],
    server_name: str
) -> Dict[str, Any]:
    """Check status of an MCP server.

    Args:
        server_name: Name of the server
    """
    if server_name not in ctx.deps.mcp_servers:
        return {'error': f'Server {server_name} not found'}

    server = ctx.deps.mcp_servers[server_name]
    status = await server.get_status()

    return status.dict()

@multi_server_agent.tool
async def find_tool_server(
    ctx: RunContext[MultiServerDeps],
    tool_name: str
) -> Optional[str]:
    """Find which server provides a specific tool.

    Args:
        tool_name: Name of the tool
    """
    return await ctx.deps.orchestrator.find_tool(tool_name)

@multi_server_agent.tool
async def execute_cross_server_workflow(
    ctx: RunContext[MultiServerDeps],
    workflow_steps: List[Dict[str, Any]]
) -> List[Any]:
    """Execute a workflow across multiple servers.

    Args:
        workflow_steps: List of workflow steps with server and tool info
    """
    return await ctx.deps.orchestrator.execute_workflow(workflow_steps)

async def multi_server_example():
    """Demonstrate multi-server MCP orchestration."""

    # Initialize MCP servers
    servers = {
        'filesystem': MCPServer('filesystem', ['read_file', 'write_file', 'list_dir']),
        'database': MCPServer('database', ['query', 'insert', 'update']),
        'api': MCPServer('api', ['http_get', 'http_post', 'websocket']),
        'compute': MCPServer('compute', ['run_job', 'get_metrics', 'cancel_job'])
    }

    orchestrator = MCPOrchestrator(servers)

    deps = MultiServerDeps(
        mcp_servers=servers,
        orchestrator=orchestrator
    )

    # Complex task requiring multiple servers
    task = """
    1. Read configuration from filesystem
    2. Query database for processing jobs
    3. Submit jobs to compute server
    4. Post results to API endpoint
    """

    print(f"{'='*80}")
    print("Multi-Server MCP Orchestration")
    print(f"{'='*80}")
    print(f"\nTask:{task}\n")

    result = await multi_server_agent.run(
        f"Execute this multi-step task: {task}",
        deps=deps
    )
    response = result.data

    print(f"SERVERS USED ({len(response.servers_used)})")
    print(f"{'─'*80}")
    for server in response.servers_used:
        print(f"\n{server.server_name}:")
        print(f"  Connected: {server.is_connected}")
        print(f"  Tools: {', '.join(server.available_tools)}")
        print(f"  Latency: {server.latency_ms:.1f}ms")

    print(f"\nWORKFLOW STEPS ({len(response.workflow_steps)})")
    print(f"{'─'*80}")
    for i, step in enumerate(response.workflow_steps, 1):
        print(f"{i}. {step}")

    print(f"\nRESULT")
    print(f"{'─'*80}")
    print(response.answer)
    print(f"\nTotal Tools Invoked: {response.total_tools_invoked}")

if __name__ == "__main__":
    asyncio.run(multi_server_example())
```

---

## A2A (Agent-to-Agent) Examples

### Example 1: Basic A2A Communication

```python
"""
Agent-to-Agent communication using A2A protocol.
Demonstrates basic A2A message exchange patterns.
Reference: https://github.com/a2aproject/a2a-samples
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Literal
import asyncio
import uuid
from datetime import datetime

class A2AMessage(BaseModel):
    """A2A protocol message."""
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_agent_id: str
    recipient_agent_id: str
    message_type: Literal['request', 'response', 'notification', 'error']
    content: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    correlation_id: Optional[str] = None

class A2AAgent(BaseModel):
    """A2A Agent descriptor."""
    agent_id: str
    agent_name: str
    capabilities: List[str]
    endpoint: str
    status: Literal['active', 'busy', 'inactive']

class A2AResponse(BaseModel):
    """Response from A2A interaction."""
    result: Any
    messages_exchanged: List[A2AMessage]
    participating_agents: List[A2AAgent]
    success: bool
    error_message: Optional[str] = None

@dataclass
class A2ADeps:
    """A2A communication dependencies."""
    agent_registry: 'A2AAgentRegistry'
    message_broker: 'A2AMessageBroker'
    current_agent_id: str

class A2AAgentRegistry:
    """Registry of available A2A agents."""

    def __init__(self):
        self.agents: Dict[str, A2AAgent] = {}

    async def register_agent(self, agent: A2AAgent) -> bool:
        """Register an agent."""
        self.agents[agent.agent_id] = agent
        return True

    async def discover_agents(
        self,
        capability: Optional[str] = None
    ) -> List[A2AAgent]:
        """Discover agents by capability."""
        if capability:
            return [
                agent for agent in self.agents.values()
                if capability in agent.capabilities
            ]
        return list(self.agents.values())

    async def get_agent(self, agent_id: str) -> Optional[A2AAgent]:
        """Get agent by ID."""
        return self.agents.get(agent_id)

class A2AMessageBroker:
    """Message broker for A2A communication."""

    def __init__(self):
        self.message_history: List[A2AMessage] = []

    async def send_message(
        self,
        sender_id: str,
        recipient_id: str,
        message_type: str,
        content: Dict[str, Any],
        correlation_id: Optional[str] = None
    ) -> A2AMessage:
        """Send a message between agents."""
        message = A2AMessage(
            sender_agent_id=sender_id,
            recipient_agent_id=recipient_id,
            message_type=message_type,
            content=content,
            correlation_id=correlation_id
        )

        self.message_history.append(message)
        return message

    async def get_messages(
        self,
        agent_id: str,
        correlation_id: Optional[str] = None
    ) -> List[A2AMessage]:
        """Get messages for an agent."""
        messages = [
            msg for msg in self.message_history
            if msg.recipient_agent_id == agent_id
        ]

        if correlation_id:
            messages = [
                msg for msg in messages
                if msg.correlation_id == correlation_id
            ]

        return messages

# Coordinator Agent
coordinator_agent = Agent[A2ADeps, A2AResponse](
    model='openai:gpt-4',
    result_type=A2AResponse,
    system_prompt="""You are a coordinator agent using A2A protocol.
    Discover available agents and delegate tasks.
    Coordinate multi-agent workflows.
    Handle agent communication using A2A messages."""
)

@coordinator_agent.tool
async def discover_agents_by_capability(
    ctx: RunContext[A2ADeps],
    capability: str
) -> List[Dict[str, Any]]:
    """Discover agents with specific capability.

    Args:
        capability: Required capability
    """
    agents = await ctx.deps.agent_registry.discover_agents(capability)
    return [agent.dict() for agent in agents]

@coordinator_agent.tool
async def send_task_to_agent(
    ctx: RunContext[A2ADeps],
    target_agent_id: str,
    task_description: str,
    task_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Send a task to another agent using A2A protocol.

    Args:
        target_agent_id: ID of the target agent
        task_description: Description of the task
        task_data: Task data
    """
    message = await ctx.deps.message_broker.send_message(
        sender_id=ctx.deps.current_agent_id,
        recipient_id=target_agent_id,
        message_type='request',
        content={
            'task': task_description,
            'data': task_data
        }
    )

    # Simulate agent processing and response
    response_message = await ctx.deps.message_broker.send_message(
        sender_id=target_agent_id,
        recipient_id=ctx.deps.current_agent_id,
        message_type='response',
        content={
            'status': 'completed',
            'result': f'Task "{task_description}" completed successfully'
        },
        correlation_id=message.message_id
    )

    return {
        'request_id': message.message_id,
        'response_id': response_message.message_id,
        'result': response_message.content
    }

async def a2a_basic_example():
    """Demonstrate basic A2A communication."""

    # Initialize A2A infrastructure
    registry = A2AAgentRegistry()
    broker = A2AMessageBroker()

    # Register agents
    await registry.register_agent(A2AAgent(
        agent_id='agent-001',
        agent_name='DataProcessor',
        capabilities=['data_processing', 'etl', 'validation'],
        endpoint='http://localhost:8001',
        status='active'
    ))

    await registry.register_agent(A2AAgent(
        agent_id='agent-002',
        agent_name='Analyzer',
        capabilities=['analysis', 'statistics', 'reporting'],
        endpoint='http://localhost:8002',
        status='active'
    ))

    await registry.register_agent(A2AAgent(
        agent_id='agent-003',
        agent_name='Notifier',
        capabilities=['notifications', 'alerts', 'messaging'],
        endpoint='http://localhost:8003',
        status='active'
    ))

    # Coordinator agent dependencies
    deps = A2ADeps(
        agent_registry=registry,
        message_broker=broker,
        current_agent_id='coordinator-001'
    )

    # Task requiring multiple agents
    task = "Process user data, analyze results, and send notifications"

    print(f"{'='*80}")
    print("A2A Agent Coordination")
    print(f"{'='*80}")
    print(f"\nTask: {task}\n")

    result = await coordinator_agent.run(
        f"Coordinate this multi-agent task: {task}",
        deps=deps
    )
    response = result.data

    print(f"SUCCESS: {response.success}")

    if response.error_message:
        print(f"Error: {response.error_message}")

    print(f"\nPARTICIPATING AGENTS ({len(response.participating_agents)})")
    print(f"{'─'*80}")
    for agent in response.participating_agents:
        print(f"\n{agent.agent_name} ({agent.agent_id})")
        print(f"  Capabilities: {', '.join(agent.capabilities)}")
        print(f"  Status: {agent.status}")

    print(f"\nMESSAGE EXCHANGE ({len(response.messages_exchanged)})")
    print(f"{'─'*80}")
    for msg in response.messages_exchanged:
        print(f"\n{msg.message_type.upper()}: {msg.sender_agent_id} → {msg.recipient_agent_id}")
        print(f"  Message ID: {msg.message_id}")
        print(f"  Content: {msg.content}")

    print(f"\nRESULT")
    print(f"{'─'*80}")
    print(response.result)

if __name__ == "__main__":
    asyncio.run(a2a_basic_example())
```

### Example 2: A2A Workflow Orchestration

```python
"""
Complex A2A workflow with agent choreography.
Based on patterns from https://github.com/a2aproject/a2a-samples
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Dict, Any, Literal
import asyncio

class WorkflowStep(BaseModel):
    """Single step in A2A workflow."""
    step_id: str
    agent_capability: str
    task_description: str
    input_data: Dict[str, Any]
    depends_on: List[str] = Field(default_factory=list)

class WorkflowExecution(BaseModel):
    """A2A workflow execution result."""
    workflow_id: str
    steps_completed: List[str]
    step_results: Dict[str, Any]
    total_execution_time: float
    status: Literal['completed', 'failed', 'partial']

@dataclass
class WorkflowDeps:
    """Workflow orchestration dependencies."""
    agent_registry: A2AAgentRegistry
    message_broker: A2AMessageBroker
    workflow_engine: 'A2AWorkflowEngine'

class A2AWorkflowEngine:
    """Engine for executing A2A workflows."""

    def __init__(
        self,
        registry: A2AAgentRegistry,
        broker: A2AMessageBroker
    ):
        self.registry = registry
        self.broker = broker

    async def execute_workflow(
        self,
        steps: List[WorkflowStep],
        coordinator_id: str
    ) -> WorkflowExecution:
        """Execute a multi-step workflow."""
        import time
        start_time = time.time()

        workflow_id = str(uuid.uuid4())
        completed_steps = []
        step_results = {}
        execution_order = self._topological_sort(steps)

        for step in execution_order:
            # Find agent with required capability
            agents = await self.registry.discover_agents(step.agent_capability)
            if not agents:
                return WorkflowExecution(
                    workflow_id=workflow_id,
                    steps_completed=completed_steps,
                    step_results=step_results,
                    total_execution_time=time.time() - start_time,
                    status='failed'
                )

            # Select first available agent
            target_agent = agents[0]

            # Send task
            await self.broker.send_message(
                sender_id=coordinator_id,
                recipient_id=target_agent.agent_id,
                message_type='request',
                content={
                    'workflow_id': workflow_id,
                    'step_id': step.step_id,
                    'task': step.task_description,
                    'input': step.input_data
                }
            )

            # Mock response
            await asyncio.sleep(0.1)
            step_results[step.step_id] = {
                'agent': target_agent.agent_name,
                'result': f'Completed: {step.task_description}',
                'output': {'status': 'success'}
            }
            completed_steps.append(step.step_id)

        return WorkflowExecution(
            workflow_id=workflow_id,
            steps_completed=completed_steps,
            step_results=step_results,
            total_execution_time=time.time() - start_time,
            status='completed'
        )

    def _topological_sort(self, steps: List[WorkflowStep]) -> List[WorkflowStep]:
        """Sort steps by dependencies."""
        # Simple implementation - in production use proper topological sort
        sorted_steps = []
        remaining = steps.copy()

        while remaining:
            for step in remaining[:]:
                if all(dep in [s.step_id for s in sorted_steps] for dep in step.depends_on):
                    sorted_steps.append(step)
                    remaining.remove(step)

        return sorted_steps

# Workflow orchestration agent
workflow_agent = Agent[WorkflowDeps, WorkflowExecution](
    model='openai:gpt-4',
    result_type=WorkflowExecution,
    system_prompt="""You are a workflow orchestration agent using A2A protocol.
    Create and execute complex multi-agent workflows.
    Handle dependencies between workflow steps.
    Coordinate parallel and sequential execution."""
)

@workflow_agent.tool
async def create_workflow_step(
    ctx: RunContext[WorkflowDeps],
    step_id: str,
    capability: str,
    task: str,
    input_data: Dict[str, Any],
    dependencies: List[str] = []
) -> Dict[str, Any]:
    """Create a workflow step.

    Args:
        step_id: Unique step identifier
        capability: Required agent capability
        task: Task description
        input_data: Input data for the step
        dependencies: List of step IDs this depends on
    """
    step = WorkflowStep(
        step_id=step_id,
        agent_capability=capability,
        task_description=task,
        input_data=input_data,
        depends_on=dependencies
    )

    return step.dict()

@workflow_agent.tool
async def execute_workflow(
    ctx: RunContext[WorkflowDeps],
    workflow_steps: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Execute a complete workflow.

    Args:
        workflow_steps: List of workflow steps
    """
    steps = [WorkflowStep(**step_dict) for step_dict in workflow_steps]

    execution = await ctx.deps.workflow_engine.execute_workflow(
        steps,
        coordinator_id='workflow-coordinator'
    )

    return execution.dict()

async def a2a_workflow_example():
    """Demonstrate A2A workflow orchestration."""

    # Setup
    registry = A2AAgentRegistry()
    broker = A2AMessageBroker()
    workflow_engine = A2AWorkflowEngine(registry, broker)

    # Register specialized agents
    agents_to_register = [
        ('ingest-agent', 'DataIngestor', ['data_ingestion', 'validation']),
        ('transform-agent', 'DataTransformer', ['data_transformation', 'etl']),
        ('analyze-agent', 'DataAnalyzer', ['analysis', 'statistics']),
        ('report-agent', 'ReportGenerator', ['reporting', 'visualization']),
    ]

    for agent_id, name, caps in agents_to_register:
        await registry.register_agent(A2AAgent(
            agent_id=agent_id,
            agent_name=name,
            capabilities=caps,
            endpoint=f'http://localhost:800{len(caps)}',
            status='active'
        ))

    deps = WorkflowDeps(
        agent_registry=registry,
        message_broker=broker,
        workflow_engine=workflow_engine
    )

    # Complex workflow
    workflow_description = """
    Create a data processing pipeline:
    1. Ingest data from multiple sources
    2. Transform and clean the data
    3. Perform statistical analysis
    4. Generate comprehensive report
    """

    print(f"{'='*80}")
    print("A2A Workflow Orchestration")
    print(f"{'='*80}")
    print(f"\nWorkflow:{workflow_description}\n")

    result = await workflow_agent.run(
        f"Execute this workflow: {workflow_description}",
        deps=deps
    )
    execution = result.data

    print(f"WORKFLOW EXECUTION")
    print(f"{'─'*80}")
    print(f"Workflow ID: {execution.workflow_id}")
    print(f"Status: {execution.status.upper()}")
    print(f"Execution Time: {execution.total_execution_time:.2f}s")
    print(f"Steps Completed: {len(execution.steps_completed)}/{len(execution.steps_completed)}")

    print(f"\nSTEP RESULTS")
    print(f"{'─'*80}")
    for step_id, result in execution.step_results.items():
        print(f"\n{step_id}:")
        print(f"  Agent: {result['agent']}")
        print(f"  Result: {result['result']}")
        print(f"  Output: {result['output']}")

if __name__ == "__main__":
    asyncio.run(a2a_workflow_example())
```

---

## Advanced Patterns

### Pattern 1: Agent Composition

```python
"""
Compose multiple agents into a higher-level agent.
Demonstrates agent composition and delegation patterns.
"""

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import Optional
import asyncio

class CompositeResult(BaseModel):
    """Result from composite agent."""
    analysis: str
    summary: str
    recommendations: list[str]
    confidence: float

@dataclass
class CompositeDeps:
    """Dependencies for composite agent."""
    data: str

# Specialized sub-agents
analyzer_agent = Agent[CompositeDeps, str](
    'openai:gpt-4',
    system_prompt="Analyze data and provide insights."
)

summarizer_agent = Agent[CompositeDeps, str](
    'openai:gpt-4',
    system_prompt="Create concise summaries."
)

recommender_agent = Agent[CompositeDeps, list[str]](
    'openai:gpt-4',
    result_type=list[str],
    system_prompt="Generate actionable recommendations."
)

# Composite agent that orchestrates sub-agents
composite_agent = Agent[CompositeDeps, CompositeResult](
    'openai:gpt-4',
    result_type=CompositeResult,
    system_prompt="Orchestrate analysis, summarization, and recommendations."
)

@composite_agent.tool
async def analyze_data(ctx: RunContext[CompositeDeps]) -> str:
    """Analyze data using specialized agent."""
    result = await analyzer_agent.run(
        f"Analyze: {ctx.deps.data}",
        deps=ctx.deps
    )
    return result.data

@composite_agent.tool
async def summarize_data(ctx: RunContext[CompositeDeps]) -> str:
    """Summarize data using specialized agent."""
    result = await summarizer_agent.run(
        f"Summarize: {ctx.deps.data}",
        deps=ctx.deps
    )
    return result.data

@composite_agent.tool
async def get_recommendations(ctx: RunContext[CompositeDeps]) -> list[str]:
    """Get recommendations using specialized agent."""
    result = await recommender_agent.run(
        f"Recommend actions for: {ctx.deps.data}",
        deps=ctx.deps
    )
    return result.data

async def composition_example():
    """Demonstrate agent composition."""
    deps = CompositeDeps(data="Sales data showing 20% growth in Q3")

    result = await composite_agent.run(
        "Provide complete analysis with recommendations",
        deps=deps
    )

    print("Composite Result:")
    print(f"Analysis: {result.data.analysis}")
    print(f"Summary: {result.data.summary}")
    print(f"Recommendations: {result.data.recommendations}")

if __name__ == "__main__":
    asyncio.run(composition_example())
```

### Pattern 2: Circuit Breaker

```python
"""
Implement circuit breaker pattern for resilient agents.
Handles failures gracefully with fallback mechanisms.
"""

from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

@dataclass
class CircuitBreaker:
    """Circuit breaker for agent calls."""
    failure_threshold: int = 5
    timeout: int = 60
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: Optional[datetime] = None

    def record_success(self):
        """Record successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self):
        """Record failed call."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def can_attempt(self) -> bool:
        """Check if call should be attempted."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            if self.last_failure_time:
                if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                    self.state = CircuitState.HALF_OPEN
                    return True
            return False

        return True  # HALF_OPEN state

@dataclass
class ResilientDeps:
    """Dependencies with circuit breaker."""
    circuit_breaker: CircuitBreaker
    fallback_response: str = "Service temporarily unavailable"

agent = Agent[ResilientDeps, str]('openai:gpt-4')

@agent.tool
async def resilient_operation(
    ctx: RunContext[ResilientDeps],
    operation: str
) -> str:
    """Perform operation with circuit breaker."""
    cb = ctx.deps.circuit_breaker

    if not cb.can_attempt():
        return f"Circuit breaker OPEN: {ctx.deps.fallback_response}"

    try:
        # Simulate operation
        await asyncio.sleep(0.1)
        # result = await perform_operation(operation)

        cb.record_success()
        return f"Operation '{operation}' succeeded"

    except Exception as e:
        cb.record_failure()
        if cb.state == CircuitState.OPEN:
            return f"Circuit breaker opened after failures: {ctx.deps.fallback_response}"
        raise

async def circuit_breaker_example():
    """Demonstrate circuit breaker pattern."""
    cb = CircuitBreaker(failure_threshold=3, timeout=5)
    deps = ResilientDeps(circuit_breaker=cb)

    for i in range(10):
        result = await agent.run(f"Operation {i}", deps=deps)
        print(f"Attempt {i}: {result.data}")
        print(f"  Circuit state: {cb.state.value}, Failures: {cb.failure_count}")

if __name__ == "__main__":
    asyncio.run(circuit_breaker_example())
```

### Pattern 3: Caching Layer

```python
"""
Implement caching for agent responses.
Reduces costs and improves performance.
"""

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import Optional, Any
import asyncio
import hashlib
import json
from datetime import datetime, timedelta

class CacheEntry(BaseModel):
    """Cache entry with TTL."""
    key: str
    value: Any
    timestamp: datetime
    ttl_seconds: int

    def is_expired(self) -> bool:
        """Check if entry is expired."""
        age = datetime.now() - self.timestamp
        return age.total_seconds() > self.ttl_seconds

class AgentCache:
    """Simple in-memory cache for agent responses."""

    def __init__(self):
        self.cache: dict[str, CacheEntry] = {}

    def _make_key(self, prompt: str, deps: Any) -> str:
        """Generate cache key from prompt and dependencies."""
        content = json.dumps({
            'prompt': prompt,
            'deps': str(deps)
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, prompt: str, deps: Any) -> Optional[Any]:
        """Get cached response."""
        key = self._make_key(prompt, deps)
        entry = self.cache.get(key)

        if entry and not entry.is_expired():
            return entry.value

        if entry:
            del self.cache[key]  # Remove expired entry

        return None

    def set(self, prompt: str, deps: Any, value: Any, ttl_seconds: int = 300):
        """Cache response."""
        key = self._make_key(prompt, deps)
        self.cache[key] = CacheEntry(
            key=key,
            value=value,
            timestamp=datetime.now(),
            ttl_seconds=ttl_seconds
        )

    def clear(self):
        """Clear all cache entries."""
        self.cache.clear()

@dataclass
class CachedDeps:
    """Dependencies with cache."""
    cache: AgentCache
    data: str

agent = Agent[CachedDeps, str]('openai:gpt-4')

@agent.tool
async def cached_operation(
    ctx: RunContext[CachedDeps],
    query: str
) -> str:
    """Perform operation with caching."""
    cache = ctx.deps.cache

    # Check cache
    cached_result = cache.get(query, ctx.deps)
    if cached_result:
        return f"[CACHE HIT] {cached_result}"

    # Perform actual operation
    result = f"Processed: {query} with {ctx.deps.data}"

    # Cache result
    cache.set(query, ctx.deps, result, ttl_seconds=60)

    return f"[CACHE MISS] {result}"

async def caching_example():
    """Demonstrate caching pattern."""
    cache = AgentCache()
    deps = CachedDeps(cache=cache, data="test-data")

    queries = [
        "What is AI?",
        "What is AI?",  # Cache hit
        "What is ML?",
        "What is AI?",  # Cache hit
    ]

    for query in queries:
        result = await agent.run(f"Process: {query}", deps=deps)
        print(f"Query: {query}")
        print(f"Result: {result.data}\n")

if __name__ == "__main__":
    asyncio.run(caching_example())
```

### Pattern 4: Observability and Tracing

```python
"""
Add comprehensive observability to agents.
Track execution, performance, and errors.
"""

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass, field
from typing import List, Any
from datetime import datetime
import asyncio
import uuid

class TraceSpan(BaseModel):
    """Individual trace span."""
    span_id: str
    parent_id: Optional[str]
    operation: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    status: str = "pending"
    metadata: dict = {}

class AgentTrace(BaseModel):
    """Complete trace for agent execution."""
    trace_id: str
    agent_name: str
    spans: List[TraceSpan]
    total_duration_ms: Optional[float] = None
    error: Optional[str] = None

@dataclass
class TracingDeps:
    """Dependencies with tracing."""
    tracer: 'AgentTracer'
    operation_name: str

class AgentTracer:
    """Tracer for agent execution."""

    def __init__(self):
        self.traces: dict[str, AgentTrace] = {}
        self.current_trace_id: Optional[str] = None

    def start_trace(self, agent_name: str) -> str:
        """Start new trace."""
        trace_id = str(uuid.uuid4())
        self.current_trace_id = trace_id
        self.traces[trace_id] = AgentTrace(
            trace_id=trace_id,
            agent_name=agent_name,
            spans=[]
        )
        return trace_id

    def start_span(
        self,
        operation: str,
        parent_id: Optional[str] = None
    ) -> str:
        """Start new span."""
        if not self.current_trace_id:
            raise ValueError("No active trace")

        span_id = str(uuid.uuid4())
        span = TraceSpan(
            span_id=span_id,
            parent_id=parent_id,
            operation=operation,
            start_time=datetime.now()
        )

        self.traces[self.current_trace_id].spans.append(span)
        return span_id

    def end_span(self, span_id: str, status: str = "success", metadata: dict = {}):
        """End span."""
        if not self.current_trace_id:
            return

        trace = self.traces[self.current_trace_id]
        for span in trace.spans:
            if span.span_id == span_id:
                span.end_time = datetime.now()
                span.duration_ms = (span.end_time - span.start_time).total_seconds() * 1000
                span.status = status
                span.metadata = metadata
                break

    def end_trace(self):
        """End current trace."""
        if not self.current_trace_id:
            return

        trace = self.traces[self.current_trace_id]
        if trace.spans:
            total_duration = sum(
                span.duration_ms for span in trace.spans
                if span.duration_ms is not None
            )
            trace.total_duration_ms = total_duration

        self.current_trace_id = None

    def get_trace(self, trace_id: str) -> Optional[AgentTrace]:
        """Get trace by ID."""
        return self.traces.get(trace_id)

agent = Agent[TracingDeps, str]('openai:gpt-4')

@agent.tool
async def traced_operation(
    ctx: RunContext[TracingDeps],
    operation: str
) -> str:
    """Perform operation with tracing."""
    tracer = ctx.deps.tracer
    span_id = tracer.start_span(f"tool:{operation}")

    try:
        # Simulate operation
        await asyncio.sleep(0.1)
        result = f"Completed: {operation}"

        tracer.end_span(span_id, status="success", metadata={'result': result})
        return result

    except Exception as e:
        tracer.end_span(span_id, status="error", metadata={'error': str(e)})
        raise

async def tracing_example():
    """Demonstrate observability pattern."""
    tracer = AgentTracer()

    # Start trace
    trace_id = tracer.start_trace("example-agent")

    try:
        deps = TracingDeps(tracer=tracer, operation_name="main")

        result = await agent.run("Execute traced operation", deps=deps)
        print(f"Result: {result.data}")

    finally:
        tracer.end_trace()

    # Print trace
    trace = tracer.get_trace(trace_id)
    if trace:
        print(f"\nTrace ID: {trace.trace_id}")
        print(f"Agent: {trace.agent_name}")
        print(f"Total Duration: {trace.total_duration_ms:.2f}ms")
        print(f"\nSpans ({len(trace.spans)}):")
        for span in trace.spans:
            print(f"  {span.operation}")
            print(f"    Duration: {span.duration_ms:.2f}ms")
            print(f"    Status: {span.status}")

if __name__ == "__main__":
    asyncio.run(tracing_example())
```

---

## Production Considerations

### Error Handling and Retries

```python
"""
Production-ready error handling with exponential backoff.
"""

from pydantic_ai import Agent, ModelRetry
import asyncio
from typing import Optional

async def robust_agent_call(
    agent: Agent,
    prompt: str,
    max_retries: int = 3,
    base_delay: float = 1.0
) -> Optional[Any]:
    """Call agent with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            result = await agent.run(prompt)
            return result.data

        except ModelRetry as e:
            if attempt == max_retries - 1:
                raise

            delay = base_delay * (2 ** attempt)
            print(f"Retry {attempt + 1}/{max_retries} after {delay}s: {e}")
            await asyncio.sleep(delay)

        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    return None
```

### Rate Limiting

```python
"""
Implement rate limiting for API calls.
"""

import asyncio
from datetime import datetime, timedelta
from collections import deque

class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()

    async def acquire(self):
        """Acquire permission to make request."""
        now = datetime.now()

        # Remove old requests outside time window
        while self.requests and now - self.requests[0] > timedelta(seconds=self.time_window):
            self.requests.popleft()

        # Wait if at limit
        if len(self.requests) >= self.max_requests:
            sleep_time = (self.requests[0] + timedelta(seconds=self.time_window) - now).total_seconds()
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            await self.acquire()
        else:
            self.requests.append(now)

# Usage
rate_limiter = RateLimiter(max_requests=10, time_window=60)

async def rate_limited_call(agent: Agent, prompt: str):
    """Make rate-limited agent call."""
    await rate_limiter.acquire()
    return await agent.run(prompt)
```

### Cost Tracking

```python
"""
Track and monitor LLM API costs.
"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class CostTracker:
    """Track agent execution costs."""
    model_costs: Dict[str, float] = None  # Cost per 1K tokens

    def __post_init__(self):
        if self.model_costs is None:
            self.model_costs = {
                'gpt-4': 0.03,
                'gpt-3.5-turbo': 0.002,
                'claude-3-opus': 0.015,
            }

        self.total_cost = 0.0
        self.calls_count = 0

    def record_call(self, model: str, input_tokens: int, output_tokens: int):
        """Record API call cost."""
        cost_per_k = self.model_costs.get(model, 0.01)
        total_tokens = input_tokens + output_tokens
        cost = (total_tokens / 1000) * cost_per_k

        self.total_cost += cost
        self.calls_count += 1

    def get_stats(self) -> dict:
        """Get cost statistics."""
        return {
            'total_cost': f"${self.total_cost:.4f}",
            'calls': self.calls_count,
            'avg_cost_per_call': f"${self.total_cost / max(self.calls_count, 1):.4f}"
        }
```

### Logging and Monitoring

```python
"""
Production logging setup.
"""

import logging
from pythonjsonlogger import jsonlogger

def setup_production_logging():
    """Configure structured JSON logging."""
    logger = logging.getLogger()
    handler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger

# Usage
logger = setup_production_logging()

async def logged_agent_call(agent: Agent, prompt: str):
    """Agent call with structured logging."""
    logger.info("Starting agent call", extra={
        'agent': agent.__class__.__name__,
        'prompt_length': len(prompt)
    })

    try:
        result = await agent.run(prompt)
        logger.info("Agent call successful", extra={
            'result_length': len(str(result.data))
        })
        return result

    except Exception as e:
        logger.error("Agent call failed", extra={
            'error': str(e),
            'error_type': type(e).__name__
        })
        raise
```

### Health Checks

```python
"""
Health check endpoint for agent services.
"""

from pydantic import BaseModel
from datetime import datetime

class HealthStatus(BaseModel):
    """Service health status."""
    status: str
    timestamp: datetime
    agent_available: bool
    model_accessible: bool
    dependencies_ok: bool

async def check_agent_health(agent: Agent) -> HealthStatus:
    """Check agent health."""
    try:
        # Test agent with simple query
        result = await agent.run("health check", timeout=5.0)

        return HealthStatus(
            status="healthy",
            timestamp=datetime.now(),
            agent_available=True,
            model_accessible=True,
            dependencies_ok=True
        )

    except Exception as e:
        return HealthStatus(
            status="unhealthy",
            timestamp=datetime.now(),
            agent_available=False,
            model_accessible=False,
            dependencies_ok=False
        )
```

### Security Best Practices

```python
"""
Security considerations for production agents.
"""

from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
import re

@dataclass
class SecureDepspython:
    """Dependencies with security controls."""
    user_id: str
    api_key: str
    allowed_operations: set[str]

def sanitize_input(text: str) -> str:
    """Sanitize user input."""
    # Remove potentially dangerous characters
    text = re.sub(r'[<>{}]', '', text)
    # Limit length
    return text[:1000]

def validate_permissions(
    user_id: str,
    operation: str,
    allowed_operations: set[str]
) -> bool:
    """Validate user has permission."""
    return operation in allowed_operations

agent = Agent[SecureDeps, str]('openai:gpt-4')

@agent.tool
async def secure_operation(
    ctx: RunContext[SecureDeps],
    operation: str,
    data: str
) -> str:
    """Perform operation with security checks."""
    # Validate permissions
    if not validate_permissions(ctx.deps.user_id, operation, ctx.deps.allowed_operations):
        raise PermissionError(f"User {ctx.deps.user_id} not allowed to perform {operation}")

    # Sanitize input
    clean_data = sanitize_input(data)

    # Perform operation
    return f"Securely executed {operation} with data: {clean_data[:50]}..."
```

---

## Conclusion

PydanticAI represents a modern approach to building AI agents in Python, with a strong focus on type safety, developer experience, and production readiness. Throughout this guide, we've explored:

### Key Takeaways

1. **Type Safety First**: PydanticAI's foundation on Pydantic ensures compile-time and runtime validation, catching errors early and improving code quality.

2. **Clean Architecture**: The framework promotes clean separation of concerns through dependency injection, making code more testable and maintainable.

3. **Model Agnostic**: Support for multiple LLM providers allows flexibility in choosing the right model for your use case without vendor lock-in.

4. **Production Ready**: Built-in features like retry logic, error handling, and streaming support make it suitable for production deployments.

5. **Extensible**: The tool system and dependency injection make it easy to extend agents with custom functionality.

### When to Use PydanticAI

PydanticAI is particularly well-suited for:

- **Type-Safe Applications**: Projects where type safety and validation are priorities
- **Complex Agent Systems**: Multi-agent systems with specialized agents
- **Production Services**: Applications requiring reliability and observability
- **API Integration**: Agents that need to interact with external APIs and services
- **RAG Applications**: Retrieval-augmented generation with structured outputs

### Best Practices Summary

1. **Always define Pydantic models** for inputs and outputs
2. **Use dependency injection** for external resources
3. **Implement proper error handling** with retries and fallbacks
4. **Add observability** through logging and tracing
5. **Test agents** with unit and integration tests
6. **Monitor costs** and performance in production
7. **Implement rate limiting** to avoid API throttling
8. **Use caching** to reduce costs and improve latency

### Getting Started

```bash
# Install PydanticAI
pip install pydantic-ai

# Install with specific model support
pip install pydantic-ai[openai]
pip install pydantic-ai[anthropic]
pip install pydantic-ai[google]
```

### Resources

- **Official Documentation**: https://ai.pydantic.dev/
- **GitHub Repository**: https://github.com/pydantic/pydantic-ai
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Community**: Pydantic Discord and GitHub Discussions

### Next Steps

1. **Start Simple**: Begin with a basic agent and gradually add complexity
2. **Experiment**: Try different models and compare results
3. **Build Tools**: Create custom tools for your specific domain
4. **Test Thoroughly**: Write tests for agents and tools
5. **Monitor Production**: Implement observability from the start
6. **Optimize Costs**: Use caching and rate limiting effectively
7. **Join Community**: Engage with the PydanticAI community for support

### Future Developments

PydanticAI is actively developed with ongoing improvements in:

- Enhanced model support and integrations
- Advanced agent patterns and best practices
- Performance optimizations
- Extended tooling and utilities
- Better observability and debugging tools

### Final Thoughts

PydanticAI brings the rigor of Pydantic's validation and type safety to the world of AI agents. Whether you're building a simple chatbot or a complex multi-agent system, PydanticAI provides the tools and patterns needed for success. Its emphasis on developer experience, combined with production-ready features, makes it an excellent choice for Python developers building AI-powered applications.

The framework's design philosophy of "type safety without compromise" ensures that as your agents grow in complexity, your codebase remains maintainable, testable, and reliable. Start small, iterate quickly, and leverage the powerful patterns demonstrated in this guide to build robust, production-ready AI agents.

---

**Happy Building with PydanticAI!**

