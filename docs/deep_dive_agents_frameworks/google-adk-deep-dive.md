# Google ADK Deep Dive: Comprehensive Agent Development Guide

## Table of Contents

1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [High-Level System Architecture](#high-level-system-architecture)
4. [Core Components Deep Dive](#core-components-deep-dive)
5. [End-to-End Flow](#end-to-end-flow)
6. [Simple Agents](#simple-agents)
7. [Complex Agents](#complex-agents)
8. [Multi-Agent Systems](#multi-agent-systems)
9. [RAG with Agents (Agentic RAG)](#rag-with-agents-agentic-rag)
10. [FASTMCP Servers with Agents](#fastmcp-servers-with-agents)
11. [A2A (Agent-to-Agent) Integration](#a2a-agent-to-agent-integration)
12. [Advanced Patterns](#advanced-patterns)
13. [Production Best Practices](#production-best-practices)
14. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is Google ADK?

Google ADK (Agent Development Kit) is Google's official Python framework for building production-grade AI agents powered by Gemini models. Released as part of Google's AI ecosystem, ADK provides a comprehensive toolkit for creating intelligent, tool-enabled agents with state management, multi-agent orchestration, and seamless integration with Google Cloud services.

### Why Google ADK?

**Native Gemini Integration**
- First-class support for Gemini 1.5 Flash, Pro, and Ultra models
- Optimized for Google AI's multimodal capabilities (text, images, audio, video)
- Direct access to Google's latest AI innovations

**Enterprise-Ready Architecture**
- Production-tested components from Google
- Scalable agent orchestration
- Built-in security and compliance considerations
- Integration with Google Cloud Platform (GCP)

**Developer Experience**
- Pythonic API design with decorators and type hints
- Automatic tool schema generation
- Minimal boilerplate code
- Comprehensive error handling

### Key Capabilities

**Function Calling & Tools**
- Decorator-based tool definition (`@function_tool`)
- Automatic JSON schema extraction from Python functions
- Type-safe parameter handling
- Streaming tool calls

**Agent Orchestration**
- AgentRunner for centralized execution
- Multi-agent coordination patterns
- State management across agent interactions
- Conversation history tracking

**Multimodal Support**
- Native image, audio, and video processing
- Cross-modal reasoning
- Document understanding
- Vision-language tasks

**Extensibility**
- Custom tool implementations
- Plugin architecture
- Integration with external systems
- RAG and knowledge base support

---

## System Architecture

### Architectural Overview

Google ADK follows a layered architecture that separates concerns between agent definition, execution, tool management, and state handling.

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Agent 1   │  │   Agent 2   │  │   Agent N   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              AgentRunner                             │   │
│  │  • Execution Management                              │   │
│  │  • State Coordination                                │   │
│  │  • Multi-Agent Routing                               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                      Agent Core Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Agent     │  │    Tools     │  │   Context    │     │
│  │  Definition  │  │   Registry   │  │   Manager    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                    Gemini Integration Layer                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Gemini API Client                         │   │
│  │  • Model Selection                                   │   │
│  │  • Request/Response Handling                         │   │
│  │  • Token Management                                  │   │
│  │  • Streaming Support                                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                      Foundation Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Gemini     │  │   Network    │  │   Security   │     │
│  │   Models     │  │   Transport  │  │   & Auth     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Component Descriptions

**Application Layer**
- **Agents**: Individual agent instances with specific roles and capabilities
- **Configuration**: Agent-specific instructions, tools, and parameters
- **Business Logic**: Domain-specific agent behaviors

**Orchestration Layer**
- **AgentRunner**: Central execution engine managing agent lifecycles
- **State Management**: Conversation history and context tracking
- **Routing**: Multi-agent communication and delegation
- **Error Handling**: Centralized exception management

**Agent Core Layer**
- **Agent Definition**: Agent metadata, instructions, and configuration
- **Tools Registry**: Collection of available function tools
- **Context Manager**: State persistence and retrieval
- **Schema Generation**: Automatic tool schema creation

**Gemini Integration Layer**
- **API Client**: HTTP client for Gemini API communication
- **Model Selection**: Dynamic model choosing (Flash, Pro, Ultra)
- **Token Management**: Rate limiting and quota handling
- **Streaming**: Real-time response streaming

**Foundation Layer**
- **Gemini Models**: Core AI models (Gemini 1.5 Flash, Pro, etc.)
- **Network Transport**: HTTP/HTTPS communication infrastructure
- **Security & Auth**: API key management, authentication, encryption

### Data Flow Architecture

```
User Input → AgentRunner → Agent → Tool Selection → Tool Execution
     ↑                                                      ↓
     └──────────── Response ← Gemini Model ← Tool Results ─┘
```

**Step-by-Step Data Flow**:

1. **Input Reception**: User query enters through AgentRunner
2. **Agent Selection**: Runner routes to appropriate agent
3. **Context Loading**: Agent retrieves conversation history
4. **Tool Analysis**: Agent analyzes available tools
5. **Gemini Request**: Agent sends request to Gemini with tools
6. **Function Calling**: Gemini decides which tools to invoke
7. **Tool Execution**: Selected tools execute with parameters
8. **Result Aggregation**: Tool results collected
9. **Response Generation**: Gemini generates final response
10. **State Update**: Conversation history updated
11. **Output Delivery**: Response returned to user

---

## High-Level System Architecture

### Component Interaction Diagram

```
┌───────────────────────────────────────────────────────────────────┐
│                         User Application                           │
└───────────────┬───────────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────────────┐
│                          AgentRunner                               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  • run(agent, input) → Result                               │ │
│  │  • stream(agent, input) → Iterator[Response]                │ │
│  │  • Manages execution context                                │ │
│  └─────────────────────────────────────────────────────────────┘ │
└───────────────┬───────────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────────────┐
│                            Agent                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Properties:                                                 │ │
│  │  • name: str                                                 │ │
│  │  • model: str (e.g., "gemini-1.5-flash")                    │ │
│  │  • instructions: str                                         │ │
│  │  • tools: List[FunctionTool]                                │ │
│  │  • temperature: float                                        │ │
│  │  • top_p: float                                              │ │
│  │  • max_tokens: int                                           │ │
│  └─────────────────────────────────────────────────────────────┘ │
└───────┬───────────────────────────────────┬───────────────────────┘
        │                                   │
        ▼                                   ▼
┌──────────────────────┐          ┌──────────────────────┐
│   Function Tools     │          │   Gemini API Client  │
│  ┌────────────────┐  │          │  ┌────────────────┐  │
│  │ @function_tool │  │          │  │  API Request   │  │
│  │ def tool(...): │  │          │  │  Handler       │  │
│  │   return ...   │  │          │  └────────────────┘  │
│  └────────────────┘  │          │  ┌────────────────┐  │
│  • Auto Schema Gen  │          │  │  Streaming     │  │
│  • Type Safety      │          │  │  Support       │  │
│  • Error Handling   │          │  └────────────────┘  │
└──────────────────────┘          └──────────────────────┘
```

### Key Architectural Patterns

**1. Decorator Pattern for Tools**
```python
@function_tool
def my_tool(param: str) -> str:
    """Tool description for Gemini."""
    return result
```
- Automatic schema generation from type hints and docstrings
- Reduces boilerplate
- Type-safe parameter handling

**2. Centralized Execution Model**
```python
runner = AgentRunner(api_key=api_key)
result = runner.run(agent=agent, input=query)
```
- Single point of execution control
- Consistent error handling
- Simplified state management

**3. Immutable Agent Configuration**
```python
agent = Agent(
    name="assistant",
    model="gemini-1.5-flash",
    instructions="You are helpful.",
    tools=[tool1, tool2]
)
```
- Agents are configured once, reused many times
- Thread-safe execution
- Clear separation of configuration and runtime

**4. Streaming-First Design**
```python
for chunk in runner.stream(agent=agent, input=query):
    print(chunk.content, end="")
```
- Real-time response delivery
- Better user experience for long responses
- Efficient resource utilization

### State Management Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Conversation History                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Message 1: User → "What is AI?"                  │  │
│  │  Message 2: Agent → "AI is..."                    │  │
│  │  Message 3: User → "Tell me more"                 │  │
│  │  Message 4: Agent → "Additionally..."             │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Context Management                          │
│  • Session ID tracking                                   │
│  • Message ordering                                      │
│  • Tool call history                                     │
│  • State persistence                                     │
└─────────────────────────────────────────────────────────┘
```

### Tool Execution Flow

```
Agent receives query
    ↓
Gemini analyzes available tools
    ↓
Gemini decides: [Tool A, Tool B]
    ↓
┌─────────────────────────────────┐
│  Parallel Tool Execution        │
│  ┌──────────┐    ┌──────────┐  │
│  │ Tool A   │    │ Tool B   │  │
│  │ executes │    │ executes │  │
│  └──────────┘    └──────────┘  │
└─────────────────────────────────┘
    ↓           ↓
Results aggregated
    ↓
Gemini generates response using tool results
    ↓
Final response to user
```

---

## Core Components Deep Dive

### 1. Agent

The `Agent` class is the fundamental building block of Google ADK. It encapsulates the configuration and behavior of an AI agent.

**Agent Class Structure**:

```python
from google_adk import Agent

agent = Agent(
    name: str,                    # Unique identifier for the agent
    model: str,                   # Gemini model ID
    instructions: str,            # System prompt/instructions
    tools: List[FunctionTool] = [],  # Available function tools
    temperature: float = 1.0,     # Sampling temperature (0-2)
    top_p: float = 0.95,         # Nucleus sampling parameter
    top_k: int = 40,             # Top-k sampling parameter
    max_tokens: int = 8192,      # Maximum response length
    response_format: str = None,  # JSON schema for structured output
)
```

**Agent Properties Explained**:

- **name**: Identifier used in multi-agent scenarios and logging
- **model**: One of:
  - `gemini-1.5-flash` - Fast, cost-effective (best for most use cases)
  - `gemini-1.5-pro` - More capable, better reasoning
  - `gemini-1.5-ultra` - Most advanced, complex tasks
- **instructions**: System-level instructions that guide agent behavior
- **tools**: List of function tools the agent can invoke
- **temperature**: Controls randomness (0 = deterministic, 2 = creative)
- **top_p**: Cumulative probability for nucleus sampling
- **max_tokens**: Response length limit

### 2. AgentRunner

The `AgentRunner` manages agent execution and handles communication with Gemini API.

**AgentRunner Interface**:

```python
from google_adk import AgentRunner

runner = AgentRunner(
    api_key: str,              # Google API key
    timeout: int = 60,         # Request timeout in seconds
    max_retries: int = 3,      # Retry attempts on failure
)

# Synchronous execution
result = runner.run(
    agent: Agent,              # Agent to execute
    input: str,               # User input/query
    context: Dict = {},       # Additional context
    session_id: str = None,   # Session ID for stateful conversations
)

# Streaming execution
for chunk in runner.stream(
    agent: Agent,
    input: str,
    context: Dict = {},
    session_id: str = None,
):
    print(chunk.content, end="")
```

**Return Types**:

```python
# RunResult for runner.run()
class RunResult:
    output: str              # Final agent response
    tool_calls: List[ToolCall]  # Tools invoked during execution
    metadata: Dict           # Additional metadata (tokens, timing, etc.)

# StreamChunk for runner.stream()
class StreamChunk:
    content: str             # Chunk of response text
    is_final: bool          # Whether this is the last chunk
    tool_call: ToolCall     # Tool call if present
```

### 3. Function Tools

Function tools are the primary mechanism for extending agent capabilities with custom logic.

**Tool Definition Pattern**:

```python
from google_adk.tools import function_tool

@function_tool
def get_weather(
    location: str,
    units: str = "fahrenheit"
) -> str:
    """Get current weather for a location.

    This function retrieves real-time weather information for a specified
    location. It supports multiple unit systems.

    Args:
        location: City name or location identifier (e.g., "San Francisco", "London")
        units: Temperature units - "fahrenheit", "celsius", or "kelvin" (default: "fahrenheit")

    Returns:
        str: Weather information including temperature, conditions, and forecast
    """
    # Implementation
    weather_data = fetch_weather_api(location, units)
    return f"Weather in {location}: {weather_data['temp']}°{units[0].upper()}, {weather_data['conditions']}"
```

**Schema Generation**:

The `@function_tool` decorator automatically generates a JSON schema that Gemini uses to understand when and how to call the tool:

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location.\n\nThis function retrieves real-time weather information for a specified location. It supports multiple unit systems.",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City name or location identifier (e.g., \"San Francisco\", \"London\")"
      },
      "units": {
        "type": "string",
        "description": "Temperature units - \"fahrenheit\", \"celsius\", or \"kelvin\"",
        "default": "fahrenheit"
      }
    },
    "required": ["location"]
  }
}
```

**Tool Best Practices**:

1. **Clear Descriptions**: Write detailed docstrings explaining what the tool does
2. **Type Hints**: Always use type hints for automatic schema generation
3. **Parameter Documentation**: Document each parameter in Args section
4. **Return Value**: Specify return type and document in Returns section
5. **Error Handling**: Handle errors gracefully and return informative messages
6. **Idempotency**: Tools should be safe to call multiple times with same parameters

### 4. Context and State Management

Google ADK provides built-in context management for stateful conversations.

**Session-Based Conversations**:

```python
import uuid

# Create unique session ID
session_id = str(uuid.uuid4())

# First interaction
result1 = runner.run(
    agent=agent,
    input="My name is Alice",
    session_id=session_id
)

# Second interaction - agent remembers context
result2 = runner.run(
    agent=agent,
    input="What's my name?",
    session_id=session_id
)
# Output: "Your name is Alice"
```

**Context Object**:

```python
context = {
    "user_id": "user_123",
    "preferences": {"language": "en"},
    "metadata": {"source": "web_app"}
}

result = runner.run(
    agent=agent,
    input=query,
    context=context
)
```

### 5. Multi-Agent Coordination

Google ADK supports multiple patterns for multi-agent systems.

**Sequential Agent Pattern**:

```python
# Agent 1: Researcher
researcher = Agent(
    name="researcher",
    model="gemini-1.5-flash",
    instructions="You are a research specialist. Research topics thoroughly.",
    tools=[search_tool, retrieve_tool]
)

# Agent 2: Analyzer
analyzer = Agent(
    name="analyzer",
    model="gemini-1.5-pro",
    instructions="You are an expert analyst. Analyze data and extract insights.",
    tools=[analyze_tool, visualize_tool]
)

# Agent 3: Writer
writer = Agent(
    name="writer",
    model="gemini-1.5-flash",
    instructions="You are a technical writer. Create clear, concise reports.",
    tools=[format_tool, export_tool]
)

# Sequential execution
research_result = runner.run(researcher, "Research AI trends")
analysis_result = runner.run(analyzer, f"Analyze: {research_result.output}")
final_report = runner.run(writer, f"Write report: {analysis_result.output}")
```

**Delegating Agent Pattern**:

```python
@function_tool
def delegate_to_specialist(task: str, specialist: str) -> str:
    """Delegate task to specialist agent."""
    specialists = {
        "research": researcher,
        "analysis": analyzer,
        "writing": writer
    }
    agent = specialists.get(specialist)
    result = runner.run(agent, task)
    return result.output

# Coordinator agent
coordinator = Agent(
    name="coordinator",
    model="gemini-1.5-pro",
    instructions="You coordinate tasks across specialist agents.",
    tools=[delegate_to_specialist]
)

result = runner.run(coordinator, "Create comprehensive AI trends report")
```

---

## End-to-End Flow

### Complete Request Lifecycle

Let's trace a complete request through the Google ADK system with a concrete example.

**Scenario**: User asks "What's the weather in San Francisco and calculate 15% tip on $85?"

**Step 1: Request Initiation**

```python
from google_adk import Agent, AgentRunner
from google_adk.tools import function_tool

# Define tools
@function_tool
def get_weather(location: str) -> str:
    """Get weather for location."""
    return f"San Francisco: Sunny, 72°F"

@function_tool
def calculate(expression: str) -> float:
    """Calculate mathematical expression."""
    return eval(expression)

# Create agent
agent = Agent(
    name="assistant",
    model="gemini-1.5-flash",
    instructions="You are a helpful assistant.",
    tools=[get_weather, calculate]
)

# Create runner
runner = AgentRunner(api_key=os.getenv("GOOGLE_API_KEY"))

# Execute request
result = runner.run(
    agent=agent,
    input="What's the weather in San Francisco and calculate 15% tip on $85?"
)
```

**Step 2: Request Processing in AgentRunner**

```
AgentRunner.run() invoked
    ↓
1. Validate agent configuration
2. Initialize session context
3. Prepare Gemini API request
4. Build message payload with tools
```

**Step 3: Gemini API Request Construction**

```python
# Internal request structure (simplified)
request_payload = {
    "model": "gemini-1.5-flash",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "What's the weather in San Francisco and calculate 15% tip on $85?"
        }
    ],
    "tools": [
        {
            "name": "get_weather",
            "description": "Get weather for location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        },
        {
            "name": "calculate",
            "description": "Calculate mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    ],
    "temperature": 1.0,
    "max_tokens": 8192
}
```

**Step 4: Gemini Model Processing**

```
Gemini 1.5 Flash receives request
    ↓
1. Analyze user query
2. Identify required information:
   - Weather for San Francisco
   - Calculate 15% of $85
3. Determine tool calls needed:
   - Call get_weather("San Francisco")
   - Call calculate("85 * 0.15")
4. Return function calls to ADK
```

**Step 5: Tool Execution**

```python
# ADK executes tools locally
tool_results = []

# Execute get_weather
result1 = get_weather(location="San Francisco")
tool_results.append({
    "tool": "get_weather",
    "result": "San Francisco: Sunny, 72°F"
})

# Execute calculate
result2 = calculate(expression="85 * 0.15")
tool_results.append({
    "tool": "calculate",
    "result": 12.75
})
```

**Step 6: Second Gemini API Call with Tool Results**

```python
# Request with tool results
second_request = {
    "model": "gemini-1.5-flash",
    "messages": [
        # Previous messages...
        {
            "role": "function",
            "name": "get_weather",
            "content": "San Francisco: Sunny, 72°F"
        },
        {
            "role": "function",
            "name": "calculate",
            "content": "12.75"
        }
    ]
}
```

**Step 7: Final Response Generation**

```
Gemini receives tool results
    ↓
Synthesizes information
    ↓
Generates natural language response
    ↓
Returns to ADK
```

**Step 8: Response Delivery**

```python
# Final result returned to application
print(result.output)
# Output: "The weather in San Francisco is sunny and 72°F.
#          A 15% tip on $85 would be $12.75."

# Metadata available
print(result.tool_calls)
# [ToolCall(name='get_weather', args={'location': 'San Francisco'}),
#  ToolCall(name='calculate', args={'expression': '85 * 0.15'})]

print(result.metadata)
# {'tokens_used': 245, 'duration_ms': 1250, 'model': 'gemini-1.5-flash'}
```

### Complete Flow Diagram

```
User Input: "Weather in SF and calculate tip"
    │
    ▼
┌─────────────────────────────────────┐
│        AgentRunner.run()             │
│  • Validate configuration            │
│  • Initialize session                │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│    Build Gemini API Request          │
│  • System instructions               │
│  • User message                      │
│  • Tool schemas                      │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│    Send to Gemini 1.5 Flash          │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│    Gemini Decides Tool Calls         │
│  • get_weather("San Francisco")     │
│  • calculate("85 * 0.15")           │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│    Execute Tools Locally             │
│  • Tool 1: "Sunny, 72°F"            │
│  • Tool 2: "12.75"                  │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Send Tool Results to Gemini         │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Gemini Generates Final Response     │
│  "The weather in San Francisco..."   │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Return Result to Application       │
│  • output: str                       │
│  • tool_calls: List[ToolCall]       │
│  • metadata: Dict                    │
└─────────────────────────────────────┘
```

---

## Simple Agents

### 1. Basic Conversational Agent

The simplest form of agent - pure conversation without tools.

```python
import os
from google_adk import Agent, AgentRunner

def create_simple_conversational_agent():
    """Create a basic conversational agent."""

    # Define agent
    agent = Agent(
        name="conversational_assistant",
        model="gemini-1.5-flash",
        instructions="""You are a friendly and helpful AI assistant.

        Your responsibilities:
        - Answer questions clearly and concisely
        - Be polite and professional
        - Admit when you don't know something
        - Ask clarifying questions when needed
        """,
        temperature=0.7,  # Slightly creative but focused
    )

    # Create runner
    runner = AgentRunner(api_key=os.getenv("GOOGLE_API_KEY"))

    return agent, runner

def run_conversation_example():
    """Run a simple conversation."""
    agent, runner = create_simple_conversational_agent()

    queries = [
        "What is machine learning?",
        "How does it differ from traditional programming?",
        "Can you give me a simple example?",
    ]

    for query in queries:
        print(f"\nUser: {query}")
        result = runner.run(agent=agent, input=query)
        print(f"Agent: {result.output}")

# Example usage
if __name__ == "__main__":
    run_conversation_example()
```

**Output**:
```
User: What is machine learning?
Agent: Machine learning is a subset of artificial intelligence where
       computers learn patterns from data without being explicitly
       programmed for each task...

User: How does it differ from traditional programming?
Agent: The key difference is in how the solution is developed. In
       traditional programming, humans write explicit rules...

User: Can you give me a simple example?
Agent: Sure! A classic example is email spam detection. In traditional
       programming, you'd write rules like "if email contains word X..."
```

### 2. Stateful Conversation Agent

Agent that maintains conversation context across multiple interactions.

```python
import uuid
from typing import Optional

class StatefulConversationAgent:
    """Agent with persistent conversation state."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)
        self.agent = Agent(
            name="stateful_assistant",
            model="gemini-1.5-flash",
            instructions="""You are a helpful assistant with memory.

            Remember:
            - User's name and preferences
            - Previous topics discussed
            - Context from earlier in the conversation
            - Any tasks or commitments mentioned
            """,
        )
        self.sessions = {}

    def start_session(self, user_id: str) -> str:
        """Start a new conversation session."""
        session_id = str(uuid.uuid4())
        self.sessions[user_id] = session_id
        return session_id

    def chat(self, user_id: str, message: str) -> str:
        """Send message in existing session."""
        if user_id not in self.sessions:
            self.start_session(user_id)

        session_id = self.sessions[user_id]
        result = self.runner.run(
            agent=self.agent,
            input=message,
            session_id=session_id
        )
        return result.output

    def end_session(self, user_id: str):
        """End conversation session."""
        if user_id in self.sessions:
            del self.sessions[user_id]

# Usage example
def run_stateful_conversation():
    agent = StatefulConversationAgent(api_key=os.getenv("GOOGLE_API_KEY"))

    user_id = "user_123"

    # Conversation flow
    print(agent.chat(user_id, "Hi, my name is Alice and I love Python"))
    # "Hello Alice! It's great to meet you. Python is an excellent language..."

    print(agent.chat(user_id, "What's my name?"))
    # "Your name is Alice!"

    print(agent.chat(user_id, "What programming language did I mention?"))
    # "You mentioned that you love Python!"

    agent.end_session(user_id)

if __name__ == "__main__":
    run_stateful_conversation()
```

### 3. Simple Tool-Enabled Agent

Agent with basic tool capabilities.

```python
from google_adk.tools import function_tool
from datetime import datetime
import random

# Define simple tools
@function_tool
def get_current_time(timezone: str = "UTC") -> str:
    """Get current time in specified timezone.

    Args:
        timezone: Timezone name (e.g., "UTC", "America/New_York", "Europe/London")

    Returns:
        Current time in the specified timezone
    """
    # Simplified - in production, use pytz
    now = datetime.now()
    return f"Current time in {timezone}: {now.strftime('%Y-%m-%d %H:%M:%S')}"

@function_tool
def roll_dice(sides: int = 6, count: int = 1) -> str:
    """Roll dice and return results.

    Args:
        sides: Number of sides on each die (default: 6)
        count: Number of dice to roll (default: 1)

    Returns:
        Dice roll results
    """
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls)
    return f"Rolled {count}d{sides}: {rolls} (Total: {total})"

@function_tool
def calculate_tip(bill_amount: float, tip_percentage: float = 15.0) -> str:
    """Calculate tip amount and total.

    Args:
        bill_amount: Total bill amount in dollars
        tip_percentage: Tip percentage (default: 15.0)

    Returns:
        Tip amount and total with tip
    """
    tip = bill_amount * (tip_percentage / 100)
    total = bill_amount + tip
    return f"Bill: ${bill_amount:.2f}, Tip ({tip_percentage}%): ${tip:.2f}, Total: ${total:.2f}"

def create_simple_tool_agent():
    """Create agent with simple tools."""

    agent = Agent(
        name="utility_assistant",
        model="gemini-1.5-flash",
        instructions="""You are a helpful utility assistant.

        You can help users with:
        - Checking the current time
        - Rolling dice for games
        - Calculating tips and totals

        Always use the appropriate tool when the user asks for these capabilities.
        """,
        tools=[get_current_time, roll_dice, calculate_tip]
    )

    runner = AgentRunner(api_key=os.getenv("GOOGLE_API_KEY"))

    return agent, runner

# Example usage
def run_simple_tool_examples():
    agent, runner = create_simple_tool_agent()

    # Test queries
    queries = [
        "What time is it?",
        "Roll 2 six-sided dice for me",
        "Calculate a 20% tip on a $125 dinner bill",
        "Roll 3d20 and tell me the time",
    ]

    for query in queries:
        print(f"\n{'='*60}")
        print(f"User: {query}")
        result = runner.run(agent=agent, input=query)
        print(f"Agent: {result.output}")
        if result.tool_calls:
            print(f"Tools used: {[tc.name for tc in result.tool_calls]}")

if __name__ == "__main__":
    run_simple_tool_examples()
```

### 4. Streaming Response Agent

Agent that streams responses for better UX.

```python
def create_streaming_agent():
    """Create agent configured for streaming."""

    agent = Agent(
        name="streaming_assistant",
        model="gemini-1.5-flash",
        instructions="""You are a helpful assistant that provides detailed explanations.

        When explaining concepts:
        - Start with a brief definition
        - Provide examples
        - Explain real-world applications
        - Be thorough but clear
        """,
    )

    runner = AgentRunner(api_key=os.getenv("GOOGLE_API_KEY"))

    return agent, runner

def stream_response_example():
    """Demonstrate streaming responses."""
    agent, runner = create_streaming_agent()

    query = "Explain how neural networks work"

    print(f"User: {query}\n")
    print("Agent: ", end="", flush=True)

    # Stream response chunks
    full_response = ""
    for chunk in runner.stream(agent=agent, input=query):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content

    print("\n")

if __name__ == "__main__":
    stream_response_example()
```

---

## Complex Agents

### 1. Research Agent with Multiple Tools

Advanced agent that performs web research, analyzes data, and generates reports.

```python
from google_adk import Agent, AgentRunner
from google_adk.tools import function_tool
from typing import List, Dict
import json

# Advanced research tools
@function_tool
def web_search(query: str, num_results: int = 5) -> str:
    """Search the web for information.

    Args:
        query: Search query string
        num_results: Number of results to return (default: 5)

    Returns:
        JSON string with search results
    """
    # Simulated search results - in production, integrate with Google Search API
    results = [
        {
            "title": f"Result {i+1} for {query}",
            "url": f"https://example.com/result{i+1}",
            "snippet": f"Information about {query} from source {i+1}..."
        }
        for i in range(num_results)
    ]
    return json.dumps(results, indent=2)

@function_tool
def fetch_webpage(url: str) -> str:
    """Fetch and extract main content from webpage.

    Args:
        url: URL of the webpage to fetch

    Returns:
        Main text content from the webpage
    """
    # Simulated webpage content - in production, use requests + BeautifulSoup
    return f"""
    Content from {url}:

    This is the main article content discussing the topic in detail.
    It contains valuable information extracted from the webpage.
    The content has been cleaned and formatted for analysis.
    """

@function_tool
def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of given text.

    Args:
        text: Text to analyze

    Returns:
        Sentiment analysis results
    """
    # Simulated sentiment analysis - in production, use NLP library
    word_count = len(text.split())
    return json.dumps({
        "sentiment": "positive",
        "confidence": 0.85,
        "word_count": word_count,
        "key_themes": ["technology", "innovation", "growth"]
    }, indent=2)

@function_tool
def extract_key_points(text: str, num_points: int = 5) -> str:
    """Extract key points from text.

    Args:
        text: Text to analyze
        num_points: Number of key points to extract

    Returns:
        List of key points
    """
    # Simulated extraction - in production, use summarization model
    points = [
        f"Key Point {i+1}: Important insight from the text"
        for i in range(num_points)
    ]
    return json.dumps(points, indent=2)

@function_tool
def create_structured_report(title: str, sections: str) -> str:
    """Create structured report from information.

    Args:
        title: Report title
        sections: JSON string with section titles and content

    Returns:
        Formatted markdown report
    """
    try:
        sections_data = json.loads(sections)
        report = f"# {title}\n\n"
        for section_title, content in sections_data.items():
            report += f"## {section_title}\n\n{content}\n\n"
        report += f"\n---\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"
        return report
    except:
        return "Error creating report: Invalid sections format"

class ResearchAgent:
    """Complex agent for comprehensive research tasks."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)

        self.agent = Agent(
            name="research_agent",
            model="gemini-1.5-pro",  # Use Pro for complex reasoning
            instructions="""You are an expert research agent.

            Your research process:
            1. Use web_search to find relevant sources
            2. Use fetch_webpage to get detailed content
            3. Use analyze_sentiment to understand tone
            4. Use extract_key_points to identify important information
            5. Use create_structured_report to compile findings

            Always:
            - Verify information from multiple sources
            - Cite sources in your reports
            - Provide objective analysis
            - Structure information clearly
            - Include both facts and insights
            """,
            tools=[
                web_search,
                fetch_webpage,
                analyze_sentiment,
                extract_key_points,
                create_structured_report
            ],
            temperature=0.3,  # Lower temperature for factual research
        )

    def research_topic(self, topic: str) -> Dict:
        """Conduct comprehensive research on a topic."""
        query = f"""Research the topic: {topic}

        Please:
        1. Search for recent information
        2. Analyze at least 3 sources
        3. Extract key insights
        4. Create a comprehensive report with sections:
           - Executive Summary
           - Key Findings
           - Detailed Analysis
           - Conclusions
           - Sources
        """

        result = self.runner.run(agent=self.agent, input=query)

        return {
            "report": result.output,
            "tools_used": [tc.name for tc in result.tool_calls],
            "metadata": result.metadata
        }

    def comparative_analysis(self, topic1: str, topic2: str) -> Dict:
        """Compare two topics through research."""
        query = f"""Conduct comparative analysis between:
        - Topic A: {topic1}
        - Topic B: {topic2}

        Create a report comparing:
        - Key similarities
        - Important differences
        - Use cases for each
        - Advantages and disadvantages
        - Recommendations
        """

        result = self.runner.run(agent=self.agent, input=query)

        return {
            "analysis": result.output,
            "tools_used": [tc.name for tc in result.tool_calls]
        }

# Usage example
def run_research_agent_example():
    agent = ResearchAgent(api_key=os.getenv("GOOGLE_API_KEY"))

    # Single topic research
    print("="*80)
    print("RESEARCH TASK: Quantum Computing")
    print("="*80)
    result = agent.research_topic("Quantum Computing Applications in 2026")
    print(result["report"])
    print(f"\nTools used: {', '.join(result['tools_used'])}")

    # Comparative analysis
    print("\n" + "="*80)
    print("COMPARATIVE ANALYSIS")
    print("="*80)
    result = agent.comparative_analysis(
        "Machine Learning",
        "Deep Learning"
    )
    print(result["analysis"])

if __name__ == "__main__":
    run_research_agent_example()
```

### 2. Code Analysis Agent

Agent specialized in analyzing and understanding code.

```python
@function_tool
def analyze_code_complexity(code: str, language: str = "python") -> str:
    """Analyze code complexity metrics.

    Args:
        code: Source code to analyze
        language: Programming language (default: "python")

    Returns:
        Complexity analysis including cyclomatic complexity, lines of code, etc.
    """
    lines = code.split('\n')
    loc = len([l for l in lines if l.strip() and not l.strip().startswith('#')])

    return json.dumps({
        "language": language,
        "total_lines": len(lines),
        "lines_of_code": loc,
        "cyclomatic_complexity": "moderate",
        "maintainability_index": 75,
        "suggestions": [
            "Consider breaking down large functions",
            "Add more inline comments",
            "Use type hints consistently"
        ]
    }, indent=2)

@function_tool
def find_security_issues(code: str) -> str:
    """Scan code for potential security vulnerabilities.

    Args:
        code: Source code to scan

    Returns:
        List of potential security issues
    """
    issues = []

    # Simplified checks - in production, use proper security scanning tools
    if "eval(" in code:
        issues.append("CRITICAL: Use of eval() can lead to code injection")
    if "exec(" in code:
        issues.append("CRITICAL: Use of exec() is potentially dangerous")
    if "pickle.loads(" in code:
        issues.append("HIGH: Unpickling untrusted data is unsafe")

    if not issues:
        issues.append("No obvious security issues detected")

    return json.dumps({"issues": issues}, indent=2)

@function_tool
def suggest_refactoring(code: str) -> str:
    """Suggest code refactoring improvements.

    Args:
        code: Source code to analyze

    Returns:
        Refactoring suggestions
    """
    suggestions = [
        {
            "type": "Extract Function",
            "description": "Lines 15-30 could be extracted to a separate function",
            "benefit": "Improves readability and reusability"
        },
        {
            "type": "Use List Comprehension",
            "description": "For loop on lines 35-38 can be replaced with list comprehension",
            "benefit": "More Pythonic and concise"
        }
    ]

    return json.dumps(suggestions, indent=2)

@function_tool
def generate_unit_tests(code: str, framework: str = "pytest") -> str:
    """Generate unit tests for given code.

    Args:
        code: Source code to test
        framework: Testing framework (default: "pytest")

    Returns:
        Generated unit test code
    """
    test_code = f"""
import {framework}
from mymodule import function_name

def test_basic_functionality():
    \"\"\"Test basic function behavior.\"\"\"
    result = function_name("input")
    assert result == "expected_output"

def test_edge_cases():
    \"\"\"Test edge cases.\"\"\"
    assert function_name("") == ""
    assert function_name(None) is None

def test_error_handling():
    \"\"\"Test error conditions.\"\"\"
    with {framework}.raises(ValueError):
        function_name("invalid_input")
"""
    return test_code

class CodeAnalysisAgent:
    """Agent specialized in code analysis and review."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)

        self.agent = Agent(
            name="code_analyst",
            model="gemini-1.5-pro",
            instructions="""You are an expert code analyst and reviewer.

            Your responsibilities:
            - Analyze code quality and complexity
            - Identify security vulnerabilities
            - Suggest refactoring opportunities
            - Generate comprehensive unit tests
            - Provide actionable feedback

            When reviewing code:
            1. Start with security analysis
            2. Check complexity metrics
            3. Suggest refactorings
            4. Generate test cases
            5. Provide summary with prioritized recommendations

            Be specific and constructive in your feedback.
            """,
            tools=[
                analyze_code_complexity,
                find_security_issues,
                suggest_refactoring,
                generate_unit_tests
            ],
            temperature=0.2,  # Low temperature for consistent analysis
        )

    def review_code(self, code: str, language: str = "python") -> Dict:
        """Comprehensive code review."""
        query = f"""Please review this {language} code:

```{language}
{code}
```

Provide:
1. Security analysis
2. Complexity assessment
3. Refactoring suggestions
4. Generated unit tests
5. Overall code quality score (1-10)
6. Prioritized action items
"""

        result = self.runner.run(agent=self.agent, input=query)

        return {
            "review": result.output,
            "tools_used": [tc.name for tc in result.tool_calls],
            "metadata": result.metadata
        }

# Example usage
def run_code_analysis_example():
    code_sample = """
def process_user_input(user_input):
    # Process user input
    result = eval(user_input)
    data = []
    for i in range(len(result)):
        if result[i] > 0:
            data.append(result[i] * 2)
    return data
"""

    analyst = CodeAnalysisAgent(api_key=os.getenv("GOOGLE_API_KEY"))
    review = analyst.review_code(code_sample)

    print("CODE REVIEW RESULTS")
    print("="*80)
    print(review["review"])
    print(f"\nAnalysis tools used: {', '.join(review['tools_used'])}")

if __name__ == "__main__":
    run_code_analysis_example()
```

### 3. Customer Support Agent

Complex agent handling customer inquiries with knowledge base access.

```python
@function_tool
def search_knowledge_base(query: str, category: str = "all") -> str:
    """Search internal knowledge base.

    Args:
        query: Search query
        category: Category to search in (all, technical, billing, account)

    Returns:
        Relevant knowledge base articles
    """
    # Simulated KB search - in production, integrate with real KB
    articles = [
        {
            "id": "KB001",
            "title": "How to reset your password",
            "category": "account",
            "content": "To reset your password, click on 'Forgot Password'...",
            "relevance": 0.95
        },
        {
            "id": "KB002",
            "title": "Billing cycle information",
            "category": "billing",
            "content": "Your billing cycle starts on the first day...",
            "relevance": 0.88
        }
    ]

    if category != "all":
        articles = [a for a in articles if a["category"] == category]

    return json.dumps(articles, indent=2)

@function_tool
def get_user_account_info(user_id: str) -> str:
    """Retrieve user account information.

    Args:
        user_id: User identifier

    Returns:
        Account information (sanitized)
    """
    # Simulated account lookup
    account = {
        "user_id": user_id,
        "account_status": "active",
        "subscription_tier": "premium",
        "member_since": "2024-01-15",
        "last_login": "2026-01-18",
        "support_tickets": 2
    }
    return json.dumps(account, indent=2)

@function_tool
def create_support_ticket(
    user_id: str,
    category: str,
    priority: str,
    description: str
) -> str:
    """Create a support ticket.

    Args:
        user_id: User identifier
        category: Issue category (technical, billing, account, other)
        priority: Priority level (low, medium, high, urgent)
        description: Detailed issue description

    Returns:
        Ticket confirmation with ticket ID
    """
    ticket_id = f"TKT-{random.randint(10000, 99999)}"
    return json.dumps({
        "ticket_id": ticket_id,
        "status": "created",
        "estimated_response": "2-4 hours",
        "message": f"Ticket {ticket_id} created successfully. Our team will respond shortly."
    }, indent=2)

@function_tool
def escalate_to_human(reason: str) -> str:
    """Escalate conversation to human agent.

    Args:
        reason: Reason for escalation

    Returns:
        Escalation confirmation
    """
    return json.dumps({
        "escalated": True,
        "reason": reason,
        "wait_time": "5-10 minutes",
        "message": "Connecting you with a human agent..."
    }, indent=2)

class CustomerSupportAgent:
    """Complex customer support agent."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)

        self.agent = Agent(
            name="support_agent",
            model="gemini-1.5-flash",
            instructions="""You are a helpful customer support agent.

            Your guidelines:
            1. Always be polite, empathetic, and professional
            2. Search the knowledge base before providing answers
            3. Verify user account information when relevant
            4. Create support tickets for issues you cannot resolve
            5. Escalate to human agents when:
               - User is frustrated or upset
               - Issue is complex and requires human judgment
               - User explicitly requests human agent
               - Issue involves sensitive account matters

            Response structure:
            - Acknowledge the user's issue
            - Provide solution or next steps
            - Ask if there's anything else you can help with

            Be concise but thorough. Prioritize user satisfaction.
            """,
            tools=[
                search_knowledge_base,
                get_user_account_info,
                create_support_ticket,
                escalate_to_human
            ],
            temperature=0.7,  # Balanced for friendly but consistent responses
        )

    def handle_inquiry(self, user_id: str, message: str) -> Dict:
        """Handle customer support inquiry."""
        context = {
            "user_id": user_id,
            "channel": "chat",
            "timestamp": datetime.now().isoformat()
        }

        result = self.runner.run(
            agent=self.agent,
            input=message,
            context=context
        )

        return {
            "response": result.output,
            "actions_taken": [tc.name for tc in result.tool_calls],
            "metadata": result.metadata
        }

# Example usage
def run_support_agent_example():
    support = CustomerSupportAgent(api_key=os.getenv("GOOGLE_API_KEY"))

    # Test scenarios
    scenarios = [
        {
            "user_id": "user_12345",
            "message": "I forgot my password and can't log in"
        },
        {
            "user_id": "user_67890",
            "message": "Why was I charged twice this month?"
        },
        {
            "user_id": "user_11111",
            "message": "This is ridiculous! I've been waiting for 2 days and no one has helped me!"
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*80}")
        print(f"SCENARIO {i}")
        print(f"{'='*80}")
        print(f"User: {scenario['message']}\n")

        response = support.handle_inquiry(
            user_id=scenario["user_id"],
            message=scenario["message"]
        )

        print(f"Agent: {response['response']}")
        print(f"\nActions taken: {', '.join(response['actions_taken']) if response['actions_taken'] else 'None'}")

if __name__ == "__main__":
    run_support_agent_example()
```

---

## Multi-Agent Systems

### 1. Sequential Multi-Agent Pipeline

Multiple agents working in sequence, each handling a specific stage.

```python
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class AgentResult:
    """Result from an agent execution."""
    agent_name: str
    output: str
    tool_calls: List[str]
    metadata: Dict[str, Any]

class MultiAgentPipeline:
    """Sequential multi-agent system."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)
        self.agents = self._create_agents()

    def _create_agents(self) -> Dict[str, Agent]:
        """Create specialized agents for pipeline."""

        # Agent 1: Data Collector
        collector = Agent(
            name="data_collector",
            model="gemini-1.5-flash",
            instructions="""You are a data collection specialist.

            Your task:
            - Gather relevant information from available sources
            - Use web_search to find recent data
            - Extract factual information
            - Organize data in structured format

            Output format:
            Provide data in clear, organized sections.
            """,
            tools=[web_search, fetch_webpage]
        )

        # Agent 2: Analyzer
        analyzer = Agent(
            name="analyzer",
            model="gemini-1.5-pro",
            instructions="""You are a data analyst.

            Your task:
            - Analyze data provided by the data collector
            - Identify patterns and trends
            - Extract insights
            - Perform sentiment analysis when relevant

            Output format:
            Provide analysis with:
            - Key findings
            - Trends identified
            - Insights and implications
            """,
            tools=[analyze_sentiment, extract_key_points]
        )

        # Agent 3: Reporter
        reporter = Agent(
            name="reporter",
            model="gemini-1.5-flash",
            instructions="""You are a report writer.

            Your task:
            - Transform analysis into clear, professional reports
            - Create structured documents
            - Use appropriate formatting
            - Include executive summaries

            Output format:
            Well-structured markdown report with:
            - Executive Summary
            - Detailed Findings
            - Recommendations
            """,
            tools=[create_structured_report]
        )

        return {
            "collector": collector,
            "analyzer": analyzer,
            "reporter": reporter
        }

    def execute_pipeline(self, task: str) -> List[AgentResult]:
        """Execute multi-agent pipeline."""
        results = []

        # Stage 1: Collection
        print("Stage 1: Data Collection")
        print("-" * 60)
        collection_result = self.runner.run(
            agent=self.agents["collector"],
            input=f"Collect information about: {task}"
        )
        results.append(AgentResult(
            agent_name="data_collector",
            output=collection_result.output,
            tool_calls=[tc.name for tc in collection_result.tool_calls],
            metadata=collection_result.metadata
        ))
        print(f"Collected data ({len(collection_result.output)} chars)")

        # Stage 2: Analysis
        print("\nStage 2: Analysis")
        print("-" * 60)
        analysis_result = self.runner.run(
            agent=self.agents["analyzer"],
            input=f"Analyze this data:\n\n{collection_result.output}"
        )
        results.append(AgentResult(
            agent_name="analyzer",
            output=analysis_result.output,
            tool_calls=[tc.name for tc in analysis_result.tool_calls],
            metadata=analysis_result.metadata
        ))
        print(f"Analysis complete ({len(analysis_result.output)} chars)")

        # Stage 3: Reporting
        print("\nStage 3: Report Generation")
        print("-" * 60)
        report_result = self.runner.run(
            agent=self.agents["reporter"],
            input=f"Create a comprehensive report from this analysis:\n\n{analysis_result.output}"
        )
        results.append(AgentResult(
            agent_name="reporter",
            output=report_result.output,
            tool_calls=[tc.name for tc in report_result.tool_calls],
            metadata=report_result.metadata
        ))
        print(f"Report generated ({len(report_result.output)} chars)")

        return results

    def get_final_output(self, results: List[AgentResult]) -> str:
        """Get final output from pipeline."""
        return results[-1].output if results else ""

    def get_pipeline_summary(self, results: List[AgentResult]) -> Dict:
        """Get summary of pipeline execution."""
        return {
            "stages": len(results),
            "agents_used": [r.agent_name for r in results],
            "total_tool_calls": sum(len(r.tool_calls) for r in results),
            "total_tokens": sum(r.metadata.get("tokens_used", 0) for r in results)
        }

# Usage example
def run_multi_agent_pipeline():
    pipeline = MultiAgentPipeline(api_key=os.getenv("GOOGLE_API_KEY"))

    task = "AI advancements in healthcare 2026"

    print("="*80)
    print(f"MULTI-AGENT PIPELINE EXECUTION")
    print(f"Task: {task}")
    print("="*80)
    print()

    results = pipeline.execute_pipeline(task)

    print("\n" + "="*80)
    print("FINAL REPORT")
    print("="*80)
    print(pipeline.get_final_output(results))

    print("\n" + "="*80)
    print("PIPELINE SUMMARY")
    print("="*80)
    summary = pipeline.get_pipeline_summary(results)
    for key, value in summary.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    run_multi_agent_pipeline()
```

### 2. Collaborative Multi-Agent System

Agents working together with shared context and dynamic collaboration.

```python
class CollaborativeAgentSystem:
    """Multi-agent system with collaboration."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)
        self.shared_context = {}
        self.agents = self._create_collaborative_agents()

    def _create_collaborative_agents(self) -> Dict[str, Agent]:
        """Create agents that can collaborate."""

        # Research Specialist
        researcher = Agent(
            name="researcher",
            model="gemini-1.5-flash",
            instructions="""You are a research specialist in a collaborative team.

            Your role:
            - Find and verify information
            - Provide factual data to team
            - Flag uncertainties for expert review

            Collaboration:
            - Share your findings with the team
            - Indicate confidence level in your research
            - Suggest when expert consultation is needed
            """,
            tools=[web_search, fetch_webpage]
        )

        # Domain Expert
        expert = Agent(
            name="expert",
            model="gemini-1.5-pro",
            instructions="""You are a domain expert in a collaborative team.

            Your role:
            - Provide expert analysis and insights
            - Validate research findings
            - Clarify complex concepts

            Collaboration:
            - Review researcher's findings
            - Add expert context and nuance
            - Identify gaps in understanding
            """,
            tools=[analyze_sentiment, extract_key_points]
        )

        # Quality Checker
        checker = Agent(
            name="quality_checker",
            model="gemini-1.5-flash",
            instructions="""You are a quality assurance specialist in a collaborative team.

            Your role:
            - Verify accuracy of information
            - Check for logical consistency
            - Ensure completeness

            Collaboration:
            - Review all team outputs
            - Flag issues or gaps
            - Suggest improvements
            """,
            tools=[]
        )

        return {
            "researcher": researcher,
            "expert": expert,
            "checker": checker
        }

    def collaborate(self, task: str) -> Dict:
        """Execute collaborative workflow."""
        session_id = str(uuid.uuid4())

        # Round 1: Research
        print("Round 1: Research Phase")
        research_result = self.runner.run(
            agent=self.agents["researcher"],
            input=task,
            session_id=session_id
        )
        self.shared_context["research"] = research_result.output

        # Round 2: Expert Analysis
        print("Round 2: Expert Analysis")
        expert_prompt = f"""Review and enhance this research:

Research findings:
{research_result.output}

Provide expert analysis and additional insights."""

        expert_result = self.runner.run(
            agent=self.agents["expert"],
            input=expert_prompt,
            session_id=session_id
        )
        self.shared_context["expert_analysis"] = expert_result.output

        # Round 3: Quality Check
        print("Round 3: Quality Assurance")
        checker_prompt = f"""Review this research and analysis for quality:

Research:
{research_result.output}

Expert Analysis:
{expert_result.output}

Verify accuracy, check for gaps, and provide a quality assessment."""

        checker_result = self.runner.run(
            agent=self.agents["checker"],
            input=checker_prompt,
            session_id=session_id
        )
        self.shared_context["quality_check"] = checker_result.output

        # Compile final output
        final_output = f"""# Collaborative Analysis Results

## Research Findings
{research_result.output}

## Expert Analysis
{expert_result.output}

## Quality Assessment
{checker_result.output}
"""

        return {
            "final_output": final_output,
            "shared_context": self.shared_context,
            "collaboration_summary": {
                "rounds": 3,
                "agents_participated": ["researcher", "expert", "quality_checker"],
                "session_id": session_id
            }
        }

# Usage example
def run_collaborative_system():
    system = CollaborativeAgentSystem(api_key=os.getenv("GOOGLE_API_KEY"))

    task = "Analyze the impact of quantum computing on cybersecurity"

    print("="*80)
    print("COLLABORATIVE MULTI-AGENT SYSTEM")
    print("="*80)
    print(f"Task: {task}\n")

    result = system.collaborate(task)

    print("\n" + "="*80)
    print("COLLABORATIVE RESULTS")
    print("="*80)
    print(result["final_output"])

    print("\n" + "="*80)
    print("COLLABORATION SUMMARY")
    print("="*80)
    for key, value in result["collaboration_summary"].items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    run_collaborative_system()
```

### 3. Supervisor-Worker Multi-Agent Pattern

Supervisor agent coordinates multiple worker agents.

```python
class SupervisorWorkerSystem:
    """Supervisor-worker multi-agent architecture."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)
        self.workers = self._create_workers()
        self.supervisor = self._create_supervisor()

    def _create_workers(self) -> Dict[str, Agent]:
        """Create specialized worker agents."""

        # Worker 1: Web Research Worker
        web_worker = Agent(
            name="web_research_worker",
            model="gemini-1.5-flash",
            instructions="You search the web and gather information. Be thorough and cite sources.",
            tools=[web_search, fetch_webpage]
        )

        # Worker 2: Data Analysis Worker
        analysis_worker = Agent(
            name="analysis_worker",
            model="gemini-1.5-flash",
            instructions="You analyze data and extract insights. Focus on patterns and trends.",
            tools=[analyze_sentiment, extract_key_points]
        )

        # Worker 3: Document Worker
        doc_worker = Agent(
            name="documentation_worker",
            model="gemini-1.5-flash",
            instructions="You create structured documents and reports. Ensure clarity and organization.",
            tools=[create_structured_report]
        )

        return {
            "web_research": web_worker,
            "analysis": analysis_worker,
            "documentation": doc_worker
        }

    def _create_supervisor_tools(self):
        """Create tools for supervisor to delegate tasks."""

        @function_tool
        def assign_web_research(task: str) -> str:
            """Assign web research task to worker.

            Args:
                task: Research task description

            Returns:
                Research results
            """
            result = self.runner.run(
                agent=self.workers["web_research"],
                input=task
            )
            return result.output

        @function_tool
        def assign_analysis(data: str) -> str:
            """Assign analysis task to worker.

            Args:
                data: Data to analyze

            Returns:
                Analysis results
            """
            result = self.runner.run(
                agent=self.workers["analysis"],
                input=f"Analyze this data:\n{data}"
            )
            return result.output

        @function_tool
        def assign_documentation(content: str) -> str:
            """Assign documentation task to worker.

            Args:
                content: Content to document

            Returns:
                Formatted document
            """
            result = self.runner.run(
                agent=self.workers["documentation"],
                input=f"Create documentation for:\n{content}"
            )
            return result.output

        return [assign_web_research, assign_analysis, assign_documentation]

    def _create_supervisor(self) -> Agent:
        """Create supervisor agent."""

        supervisor_tools = self._create_supervisor_tools()

        return Agent(
            name="supervisor",
            model="gemini-1.5-pro",
            instructions="""You are a supervisor coordinating worker agents.

            Your responsibilities:
            1. Break down complex tasks into subtasks
            2. Assign subtasks to appropriate workers:
               - assign_web_research: For gathering information
               - assign_analysis: For analyzing data
               - assign_documentation: For creating reports
            3. Coordinate worker outputs
            4. Synthesize final results

            Workflow:
            1. Analyze the main task
            2. Create subtasks
            3. Assign to workers in logical order
            4. Integrate results
            5. Provide comprehensive final output
            """,
            tools=supervisor_tools,
            temperature=0.3
        )

    def execute(self, task: str) -> Dict:
        """Execute task using supervisor-worker pattern."""
        print("Supervisor analyzing task and coordinating workers...")

        result = self.runner.run(
            agent=self.supervisor,
            input=task
        )

        return {
            "final_output": result.output,
            "worker_assignments": [tc.name for tc in result.tool_calls],
            "metadata": result.metadata
        }

# Usage example
def run_supervisor_worker_example():
    system = SupervisorWorkerSystem(api_key=os.getenv("GOOGLE_API_KEY"))

    task = """Create a comprehensive report on the state of artificial
    intelligence in education, including recent developments, key players,
    and future trends."""

    print("="*80)
    print("SUPERVISOR-WORKER MULTI-AGENT SYSTEM")
    print("="*80)
    print(f"Task: {task}\n")

    result = system.execute(task)

    print("\n" + "="*80)
    print("FINAL OUTPUT")
    print("="*80)
    print(result["final_output"])

    print("\n" + "="*80)
    print("WORKER ASSIGNMENTS")
    print("="*80)
    print(f"Workers used: {', '.join(result['worker_assignments'])}")

if __name__ == "__main__":
    run_supervisor_worker_example()
```

---

## RAG with Agents (Agentic RAG)

### 1. Basic RAG Agent

Agent with retrieval-augmented generation capabilities.

```python
from typing import List, Tuple
import numpy as np

# Simple vector store simulation
class SimpleVectorStore:
    """Simplified vector store for RAG."""

    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add_documents(self, documents: List[str]):
        """Add documents to vector store."""
        self.documents.extend(documents)
        # Simulated embeddings - in production, use real embedding model
        for doc in documents:
            # Simple hash-based embedding simulation
            embedding = [hash(word) % 1000 / 1000.0 for word in doc.split()[:10]]
            self.embeddings.append(embedding)

    def similarity_search(self, query: str, k: int = 3) -> List[str]:
        """Search for similar documents."""
        # Simulated search - in production, use cosine similarity
        query_words = set(query.lower().split())

        scores = []
        for i, doc in enumerate(self.documents):
            doc_words = set(doc.lower().split())
            overlap = len(query_words & doc_words)
            scores.append((overlap, i))

        # Get top k
        scores.sort(reverse=True)
        top_k = scores[:k]

        return [self.documents[idx] for _, idx in top_k]

# RAG tools
@function_tool
def retrieve_documents(query: str, num_docs: int = 3) -> str:
    """Retrieve relevant documents from knowledge base.

    Args:
        query: Search query
        num_docs: Number of documents to retrieve

    Returns:
        Retrieved documents as JSON
    """
    # Access global vector store (in production, use proper dependency injection)
    docs = vector_store.similarity_search(query, k=num_docs)

    results = [
        {"id": i+1, "content": doc, "relevance_score": 0.9 - (i * 0.1)}
        for i, doc in enumerate(docs)
    ]

    return json.dumps(results, indent=2)

@function_tool
def add_to_knowledge_base(document: str, metadata: str = "{}") -> str:
    """Add new document to knowledge base.

    Args:
        document: Document content to add
        metadata: JSON string with document metadata

    Returns:
        Confirmation message
    """
    vector_store.add_documents([document])
    return f"Document added to knowledge base. Total documents: {len(vector_store.documents)}"

@function_tool
def get_knowledge_stats() -> str:
    """Get statistics about the knowledge base.

    Returns:
        Knowledge base statistics
    """
    return json.dumps({
        "total_documents": len(vector_store.documents),
        "total_embeddings": len(vector_store.embeddings),
        "avg_doc_length": np.mean([len(doc.split()) for doc in vector_store.documents])
    }, indent=2)

# Initialize global vector store with sample data
vector_store = SimpleVectorStore()
vector_store.add_documents([
    "Machine learning is a subset of artificial intelligence that enables computers to learn from data without explicit programming.",
    "Deep learning uses neural networks with multiple layers to learn hierarchical representations of data.",
    "Natural language processing (NLP) is a field of AI focused on enabling computers to understand and generate human language.",
    "Computer vision enables machines to derive meaningful information from digital images and videos.",
    "Reinforcement learning is a type of machine learning where agents learn to make decisions by interacting with an environment.",
    "Transfer learning allows models trained on one task to be adapted for related tasks, reducing training time and data requirements.",
    "Transformers are a neural network architecture that has revolutionized NLP, enabling models like GPT and BERT.",
    "Supervised learning involves training models on labeled data, where the correct output is known for each input.",
    "Unsupervised learning finds patterns in unlabeled data through techniques like clustering and dimensionality reduction.",
    "Generative AI creates new content, including text, images, and code, by learning patterns from training data.",
])

class RAGAgent:
    """Agent with retrieval-augmented generation."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)

        self.agent = Agent(
            name="rag_agent",
            model="gemini-1.5-flash",
            instructions="""You are a knowledge assistant with RAG capabilities.

            Your process:
            1. When asked a question, ALWAYS retrieve relevant documents first
            2. Use retrieved documents to inform your answer
            3. Cite specific information from retrieved documents
            4. If documents don't contain relevant information, say so
            5. You can add new information to the knowledge base when provided

            Response structure:
            - Start with retrieved context
            - Provide answer based on retrieved documents
            - Include citations (e.g., "According to document 1...")
            - Indicate confidence level
            """,
            tools=[retrieve_documents, add_to_knowledge_base, get_knowledge_stats],
            temperature=0.3,  # Lower temperature for factual responses
        )

    def ask(self, question: str) -> Dict:
        """Ask question with RAG."""
        result = self.runner.run(agent=self.agent, input=question)

        return {
            "answer": result.output,
            "tools_used": [tc.name for tc in result.tool_calls],
            "metadata": result.metadata
        }

    def add_knowledge(self, document: str, metadata: Dict = None) -> Dict:
        """Add document to knowledge base."""
        metadata_str = json.dumps(metadata) if metadata else "{}"

        prompt = f"Add this document to the knowledge base: {document}"
        if metadata:
            prompt += f"\nMetadata: {metadata_str}"

        result = self.runner.run(agent=self.agent, input=prompt)

        return {
            "response": result.output,
            "success": "added to knowledge base" in result.output.lower()
        }

# Usage example
def run_rag_agent_example():
    agent = RAGAgent(api_key=os.getenv("GOOGLE_API_KEY"))

    print("="*80)
    print("RAG AGENT EXAMPLE")
    print("="*80)

    # Test questions
    questions = [
        "What is machine learning?",
        "Explain the difference between supervised and unsupervised learning",
        "What are transformers in AI?",
        "How does transfer learning work?",
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{'='*80}")
        print(f"Question {i}: {question}")
        print(f"{'='*80}")

        response = agent.ask(question)
        print(f"\nAnswer:\n{response['answer']}")
        print(f"\nTools used: {', '.join(response['tools_used']) if response['tools_used'] else 'None'}")

    # Add new knowledge
    print(f"\n{'='*80}")
    print("ADDING NEW KNOWLEDGE")
    print(f"{'='*80}")

    new_doc = "Quantum machine learning combines quantum computing with machine learning algorithms to potentially achieve exponential speedups for certain tasks."
    result = agent.add_knowledge(
        new_doc,
        metadata={"source": "research_paper", "date": "2026-01-15"}
    )
    print(f"Result: {result['response']}")

    # Test with new knowledge
    print(f"\n{'='*80}")
    print("Testing with new knowledge")
    print(f"{'='*80}")

    response = agent.ask("What is quantum machine learning?")
    print(f"\nAnswer:\n{response['answer']}")

if __name__ == "__main__":
    run_rag_agent_example()
```

### 2. Advanced Agentic RAG

Multi-step RAG with query decomposition and iterative retrieval.

```python
@function_tool
def decompose_query(query: str) -> str:
    """Decompose complex query into sub-queries.

    Args:
        query: Complex query to decompose

    Returns:
        List of sub-queries as JSON
    """
    # Simplified decomposition - in production, use LLM
    sub_queries = [
        f"What is {query.split()[0]}?",
        f"How does {query} work?",
        f"What are examples of {query}?"
    ]
    return json.dumps({"sub_queries": sub_queries}, indent=2)

@function_tool
def rerank_documents(query: str, documents: str) -> str:
    """Rerank retrieved documents by relevance.

    Args:
        query: Original query
        documents: JSON string with documents to rerank

    Returns:
        Reranked documents
    """
    try:
        docs = json.loads(documents)
        # Simplified reranking - in production, use cross-encoder
        # For now, just reverse order as simulation
        docs.reverse()
        return json.dumps(docs, indent=2)
    except:
        return documents

@function_tool
def synthesize_answer(query: str, context_documents: str) -> str:
    """Synthesize answer from multiple context documents.

    Args:
        query: Original query
        context_documents: JSON string with context documents

    Returns:
        Synthesized answer with citations
    """
    try:
        docs = json.loads(context_documents)

        synthesis = f"Based on {len(docs)} documents:\n\n"
        for i, doc in enumerate(docs, 1):
            content = doc.get("content", "")
            synthesis += f"[{i}] {content[:100]}...\n"

        synthesis += f"\nSynthesized answer for: {query}"
        return synthesis
    except:
        return "Error synthesizing answer"

class AdvancedAgenticRAG:
    """Advanced RAG with multi-step reasoning."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)

        # Query Planner Agent
        self.planner = Agent(
            name="query_planner",
            model="gemini-1.5-pro",
            instructions="""You are a query planning specialist.

            Your role:
            - Analyze complex queries
            - Decompose into sub-queries when needed
            - Determine retrieval strategy
            - Plan multi-step retrieval if necessary
            """,
            tools=[decompose_query],
        )

        # Retrieval Agent
        self.retriever = Agent(
            name="retriever",
            model="gemini-1.5-flash",
            instructions="""You are a retrieval specialist.

            Your role:
            - Retrieve relevant documents
            - Rerank for relevance
            - Filter low-quality results
            - Ensure comprehensive coverage
            """,
            tools=[retrieve_documents, rerank_documents],
        )

        # Synthesis Agent
        self.synthesizer = Agent(
            name="synthesizer",
            model="gemini-1.5-pro",
            instructions="""You are an answer synthesis specialist.

            Your role:
            - Combine information from multiple sources
            - Generate coherent answers
            - Include proper citations
            - Indicate confidence and limitations
            """,
            tools=[synthesize_answer],
        )

    def answer_query(self, query: str) -> Dict:
        """Answer query using multi-step agentic RAG."""

        # Step 1: Query Planning
        print("Step 1: Query Planning")
        plan_result = self.runner.run(
            agent=self.planner,
            input=f"Analyze and plan retrieval for: {query}"
        )
        print(f"Plan: {plan_result.output[:200]}...")

        # Step 2: Retrieval
        print("\nStep 2: Document Retrieval")
        retrieval_result = self.runner.run(
            agent=self.retriever,
            input=f"Retrieve and rank documents for: {query}"
        )
        print(f"Retrieved {len(retrieval_result.tool_calls)} document sets")

        # Step 3: Synthesis
        print("\nStep 3: Answer Synthesis")
        synthesis_input = f"""Synthesize answer for query: {query}

Retrieved context:
{retrieval_result.output}

Provide comprehensive answer with citations."""

        synthesis_result = self.runner.run(
            agent=self.synthesizer,
            input=synthesis_input
        )

        return {
            "query": query,
            "plan": plan_result.output,
            "retrieved_docs": retrieval_result.output,
            "final_answer": synthesis_result.output,
            "steps": {
                "planning": [tc.name for tc in plan_result.tool_calls],
                "retrieval": [tc.name for tc in retrieval_result.tool_calls],
                "synthesis": [tc.name for tc in synthesis_result.tool_calls],
            }
        }

# Usage example
def run_advanced_rag_example():
    rag = AdvancedAgenticRAG(api_key=os.getenv("GOOGLE_API_KEY"))

    query = "How do transformers and transfer learning work together in modern NLP?"

    print("="*80)
    print("ADVANCED AGENTIC RAG")
    print("="*80)
    print(f"Query: {query}\n")

    result = rag.answer_query(query)

    print("\n" + "="*80)
    print("FINAL ANSWER")
    print("="*80)
    print(result["final_answer"])

    print("\n" + "="*80)
    print("PROCESS SUMMARY")
    print("="*80)
    for step, tools in result["steps"].items():
        print(f"{step.capitalize()}: {', '.join(tools) if tools else 'No tools'}")

if __name__ == "__main__":
    run_advanced_rag_example()
```

---

## FASTMCP Servers with Agents

### What is MCP?

Model Context Protocol (MCP) is a standardized protocol for connecting AI models to external tools and data sources. FASTMCP is a Python implementation that makes it easy to create MCP servers.

### Integrating MCP with Google ADK

```python
# Install FASTMCP
# pip install fastmcp

from fastmcp import FastMCP
from google_adk import Agent, AgentRunner
from google_adk.tools import function_tool
import asyncio

# Create MCP Server
mcp_server = FastMCP("Google ADK MCP Server")

# Define MCP tools
@mcp_server.tool()
def mcp_get_user_data(user_id: str) -> dict:
    """Retrieve user data via MCP.

    Args:
        user_id: User identifier

    Returns:
        User data dictionary
    """
    # Simulated user data retrieval
    return {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john@example.com",
        "preferences": {"theme": "dark", "language": "en"}
    }

@mcp_server.tool()
def mcp_update_user_settings(user_id: str, settings: dict) -> dict:
    """Update user settings via MCP.

    Args:
        user_id: User identifier
        settings: Settings to update

    Returns:
        Update confirmation
    """
    return {
        "success": True,
        "user_id": user_id,
        "updated_settings": settings,
        "timestamp": datetime.now().isoformat()
    }

@mcp_server.tool()
def mcp_query_database(query: str) -> list:
    """Query database via MCP.

    Args:
        query: SQL-like query string

    Returns:
        Query results
    """
    # Simulated database query
    return [
        {"id": 1, "name": "Record 1", "value": 100},
        {"id": 2, "name": "Record 2", "value": 200},
    ]

# Wrap MCP tools for Google ADK
@function_tool
def get_user_via_mcp(user_id: str) -> str:
    """Get user data through MCP server.

    Args:
        user_id: User identifier

    Returns:
        User data as JSON string
    """
    result = mcp_get_user_data(user_id)
    return json.dumps(result, indent=2)

@function_tool
def update_settings_via_mcp(user_id: str, settings_json: str) -> str:
    """Update user settings through MCP server.

    Args:
        user_id: User identifier
        settings_json: Settings as JSON string

    Returns:
        Update confirmation
    """
    settings = json.loads(settings_json)
    result = mcp_update_user_settings(user_id, settings)
    return json.dumps(result, indent=2)

@function_tool
def query_db_via_mcp(query: str) -> str:
    """Query database through MCP server.

    Args:
        query: Query string

    Returns:
        Query results as JSON
    """
    result = mcp_query_database(query)
    return json.dumps(result, indent=2)

class MCPEnabledAgent:
    """Google ADK agent with MCP server integration."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)

        self.agent = Agent(
            name="mcp_agent",
            model="gemini-1.5-flash",
            instructions="""You are an assistant with access to MCP server tools.

            Available capabilities through MCP:
            - Retrieve user data
            - Update user settings
            - Query database

            Always use MCP tools to access external data and services.
            Provide clear feedback about operations performed.
            """,
            tools=[
                get_user_via_mcp,
                update_settings_via_mcp,
                query_db_via_mcp
            ]
        )

    def execute(self, query: str) -> dict:
        """Execute query with MCP integration."""
        result = self.runner.run(agent=self.agent, input=query)

        return {
            "response": result.output,
            "mcp_calls": [tc.name for tc in result.tool_calls],
            "metadata": result.metadata
        }

# Advanced MCP Server with Multiple Agents
class MultiAgentMCPSystem:
    """Multi-agent system with centralized MCP server."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)
        self.mcp_server = FastMCP("Multi-Agent MCP Hub")
        self._setup_mcp_resources()
        self.agents = self._create_agents()

    def _setup_mcp_resources(self):
        """Setup MCP resources for shared access."""

        @self.mcp_server.resource("user://profile/{user_id}")
        def get_user_profile(user_id: str) -> str:
            """MCP resource: User profile."""
            return json.dumps({
                "user_id": user_id,
                "profile": {"name": "User", "role": "customer"}
            })

        @self.mcp_server.resource("db://records")
        def get_database_records() -> str:
            """MCP resource: Database records."""
            return json.dumps([
                {"id": 1, "data": "Record 1"},
                {"id": 2, "data": "Record 2"}
            ])

    def _create_mcp_tools(self):
        """Create ADK tools that use MCP server."""

        @function_tool
        def access_mcp_resource(resource_uri: str) -> str:
            """Access MCP resource.

            Args:
                resource_uri: MCP resource URI (e.g., "user://profile/123")

            Returns:
                Resource data
            """
            # In production, this would call actual MCP server
            if "user://profile" in resource_uri:
                user_id = resource_uri.split("/")[-1]
                return json.dumps({"user_id": user_id, "data": "User profile"})
            elif "db://records" in resource_uri:
                return json.dumps([{"id": 1, "data": "Record"}])
            return json.dumps({"error": "Resource not found"})

        @function_tool
        def mcp_tool_call(tool_name: str, parameters: str) -> str:
            """Call MCP server tool.

            Args:
                tool_name: Name of MCP tool
                parameters: JSON string with parameters

            Returns:
                Tool execution result
            """
            params = json.loads(parameters)
            # Route to appropriate MCP tool
            if tool_name == "get_user_data":
                return json.dumps(mcp_get_user_data(**params))
            elif tool_name == "query_database":
                return json.dumps(mcp_query_database(**params))
            return json.dumps({"error": "Tool not found"})

        return [access_mcp_resource, mcp_tool_call]

    def _create_agents(self) -> dict:
        """Create agents with MCP access."""
        mcp_tools = self._create_mcp_tools()

        # Agent 1: Data Access Agent
        data_agent = Agent(
            name="data_agent",
            model="gemini-1.5-flash",
            instructions="You access data through MCP resources and tools. Use MCP for all data operations.",
            tools=mcp_tools
        )

        # Agent 2: Processing Agent
        process_agent = Agent(
            name="process_agent",
            model="gemini-1.5-flash",
            instructions="You process data obtained from MCP. Focus on analysis and transformation.",
            tools=mcp_tools
        )

        return {
            "data": data_agent,
            "process": process_agent
        }

    def workflow(self, task: str) -> dict:
        """Execute multi-agent workflow with MCP."""

        # Step 1: Data Access
        data_result = self.runner.run(
            agent=self.agents["data"],
            input=f"Access required data for: {task}"
        )

        # Step 2: Processing
        process_result = self.runner.run(
            agent=self.agents["process"],
            input=f"Process this data: {data_result.output}"
        )

        return {
            "task": task,
            "data_accessed": data_result.output,
            "processed_result": process_result.output,
            "mcp_interactions": {
                "data_agent": [tc.name for tc in data_result.tool_calls],
                "process_agent": [tc.name for tc in process_result.tool_calls]
            }
        }

# Usage Examples
def run_mcp_examples():
    """Run MCP integration examples."""
    api_key = os.getenv("GOOGLE_API_KEY")

    # Example 1: Basic MCP Agent
    print("="*80)
    print("EXAMPLE 1: Basic MCP-Enabled Agent")
    print("="*80)

    mcp_agent = MCPEnabledAgent(api_key=api_key)

    result = mcp_agent.execute("Get user data for user ID 12345 and show their settings")
    print(f"Response: {result['response']}")
    print(f"MCP calls: {result['mcp_calls']}")

    # Example 2: Multi-Agent MCP System
    print("\n" + "="*80)
    print("EXAMPLE 2: Multi-Agent MCP System")
    print("="*80)

    mcp_system = MultiAgentMCPSystem(api_key=api_key)

    result = mcp_system.workflow("Analyze user engagement data")
    print(f"Processed Result: {result['processed_result']}")
    print(f"MCP Interactions: {result['mcp_interactions']}")

if __name__ == "__main__":
    run_mcp_examples()
```

### MCP Server Benefits

**Standardization**
- Consistent interface across different tools and data sources
- Easy integration with multiple agent frameworks
- Interoperability between systems

**Scalability**
- Centralized tool management
- Share resources across multiple agents
- Efficient resource utilization

**Security**
- Controlled access to external systems
- Audit logging of all interactions
- Permission management

---

## A2A (Agent-to-Agent) Integration

### A2A Protocol Overview

Agent-to-Agent (A2A) protocol enables agents to discover and communicate with each other as standalone services. Each agent exposes its capabilities through an AgentCard and can interact with other agents via standardized messaging.

### A2A Architecture with Google ADK

```python
from typing import Optional, Dict, List
from dataclasses import dataclass
from enum import Enum

# A2A Protocol Types
class MessageType(Enum):
    """A2A message types."""
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    AGENT_CARD = "agent_card"
    ERROR = "error"

@dataclass
class AgentCard:
    """Agent capability description for A2A."""
    agent_id: str
    name: str
    description: str
    capabilities: List[str]
    version: str
    endpoint: str

@dataclass
class A2AMessage:
    """A2A protocol message."""
    message_type: MessageType
    sender_id: str
    receiver_id: str
    payload: Dict
    conversation_id: Optional[str] = None

class A2AAgent:
    """Google ADK agent with A2A capabilities."""

    def __init__(
        self,
        agent_id: str,
        name: str,
        description: str,
        capabilities: List[str],
        api_key: str,
        endpoint: str = "http://localhost:8000"
    ):
        self.agent_id = agent_id
        self.endpoint = endpoint

        # Create agent card
        self.card = AgentCard(
            agent_id=agent_id,
            name=name,
            description=description,
            capabilities=capabilities,
            version="1.0.0",
            endpoint=endpoint
        )

        # Create Google ADK agent
        self.runner = AgentRunner(api_key=api_key)
        self.agent = self._create_agent(name, description)

        # Track known agents
        self.known_agents: Dict[str, AgentCard] = {}

    def _create_agent(self, name: str, description: str) -> Agent:
        """Create underlying Google ADK agent."""

        # Create A2A communication tools
        @function_tool
        def discover_agents() -> str:
            """Discover available A2A agents.

            Returns:
                List of available agents with their capabilities
            """
            agents_info = [
                {
                    "agent_id": card.agent_id,
                    "name": card.name,
                    "capabilities": card.capabilities,
                    "endpoint": card.endpoint
                }
                for card in self.known_agents.values()
            ]
            return json.dumps(agents_info, indent=2)

        @function_tool
        def send_task_to_agent(target_agent_id: str, task: str) -> str:
            """Send task to another A2A agent.

            Args:
                target_agent_id: ID of target agent
                task: Task description

            Returns:
                Response from target agent
            """
            if target_agent_id not in self.known_agents:
                return json.dumps({"error": f"Agent {target_agent_id} not found"})

            # Simulate A2A communication
            message = A2AMessage(
                message_type=MessageType.TASK_REQUEST,
                sender_id=self.agent_id,
                receiver_id=target_agent_id,
                payload={"task": task},
                conversation_id=str(uuid.uuid4())
            )

            # In production, this would send actual HTTP request to target agent
            response = self._simulate_a2a_request(message)
            return json.dumps(response, indent=2)

        @function_tool
        def request_agent_capability(agent_id: str, capability: str, parameters: str) -> str:
            """Request specific capability from another agent.

            Args:
                agent_id: Target agent ID
                capability: Capability name
                parameters: JSON string with parameters

            Returns:
                Capability execution result
            """
            if agent_id not in self.known_agents:
                return json.dumps({"error": "Agent not found"})

            agent_card = self.known_agents[agent_id]
            if capability not in agent_card.capabilities:
                return json.dumps({"error": f"Capability {capability} not available"})

            params = json.loads(parameters)

            message = A2AMessage(
                message_type=MessageType.TASK_REQUEST,
                sender_id=self.agent_id,
                receiver_id=agent_id,
                payload={
                    "capability": capability,
                    "parameters": params
                }
            )

            response = self._simulate_a2a_request(message)
            return json.dumps(response, indent=2)

        return Agent(
            name=name,
            model="gemini-1.5-flash",
            instructions=f"""{description}

            You are an A2A-enabled agent. You can:
            - Discover other agents using discover_agents()
            - Send tasks to other agents using send_task_to_agent()
            - Request specific capabilities using request_agent_capability()

            When you need help with tasks outside your expertise, discover and
            delegate to appropriate agents.
            """,
            tools=[discover_agents, send_task_to_agent, request_agent_capability]
        )

    def _simulate_a2a_request(self, message: A2AMessage) -> Dict:
        """Simulate A2A request (in production, this would be actual HTTP call)."""
        return {
            "status": "success",
            "result": f"Response from {message.receiver_id}",
            "conversation_id": message.conversation_id
        }

    def register_agent(self, agent_card: AgentCard):
        """Register another A2A agent."""
        self.known_agents[agent_card.agent_id] = agent_card

    def get_card(self) -> AgentCard:
        """Get this agent's card."""
        return self.card

    def handle_request(self, message: A2AMessage) -> A2AMessage:
        """Handle incoming A2A request."""
        if message.message_type == MessageType.TASK_REQUEST:
            # Process task with Google ADK agent
            task = message.payload.get("task", "")
            result = self.runner.run(agent=self.agent, input=task)

            return A2AMessage(
                message_type=MessageType.TASK_RESPONSE,
                sender_id=self.agent_id,
                receiver_id=message.sender_id,
                payload={"result": result.output},
                conversation_id=message.conversation_id
            )

        elif message.message_type == MessageType.AGENT_CARD:
            return A2AMessage(
                message_type=MessageType.AGENT_CARD,
                sender_id=self.agent_id,
                receiver_id=message.sender_id,
                payload={
                    "card": {
                        "agent_id": self.card.agent_id,
                        "name": self.card.name,
                        "description": self.card.description,
                        "capabilities": self.card.capabilities,
                        "version": self.card.version
                    }
                }
            )

        return A2AMessage(
            message_type=MessageType.ERROR,
            sender_id=self.agent_id,
            receiver_id=message.sender_id,
            payload={"error": "Unsupported message type"}
        )

    def execute(self, task: str) -> Dict:
        """Execute task (may delegate to other A2A agents)."""
        result = self.runner.run(agent=self.agent, input=task)

        return {
            "result": result.output,
            "a2a_interactions": [tc.name for tc in result.tool_calls],
            "metadata": result.metadata
        }

# Multi-Agent A2A System Example
class A2AMultiAgentSystem:
    """Complete A2A multi-agent system."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.agents: Dict[str, A2AAgent] = {}
        self._setup_agents()

    def _setup_agents(self):
        """Setup multiple A2A agents."""

        # Research Agent
        research_agent = A2AAgent(
            agent_id="research_001",
            name="Research Specialist",
            description="Expert at finding and analyzing information",
            capabilities=["web_search", "data_analysis", "fact_checking"],
            api_key=self.api_key,
            endpoint="http://localhost:8001"
        )
        self.agents["research"] = research_agent

        # Code Agent
        code_agent = A2AAgent(
            agent_id="code_001",
            name="Code Specialist",
            description="Expert at code analysis and generation",
            capabilities=["code_review", "code_generation", "debugging"],
            api_key=self.api_key,
            endpoint="http://localhost:8002"
        )
        self.agents["code"] = code_agent

        # Writing Agent
        writing_agent = A2AAgent(
            agent_id="writing_001",
            name="Writing Specialist",
            description="Expert at creating documentation and reports",
            capabilities=["technical_writing", "documentation", "reporting"],
            api_key=self.api_key,
            endpoint="http://localhost:8003"
        )
        self.agents["writing"] = writing_agent

        # Coordinator Agent
        coordinator = A2AAgent(
            agent_id="coordinator_001",
            name="Coordinator",
            description="Coordinates tasks across specialist agents",
            capabilities=["task_delegation", "workflow_management", "coordination"],
            api_key=self.api_key,
            endpoint="http://localhost:8000"
        )
        self.agents["coordinator"] = coordinator

        # Register all agents with each other
        for agent_id, agent in self.agents.items():
            for other_id, other_agent in self.agents.items():
                if agent_id != other_id:
                    agent.register_agent(other_agent.get_card())

    def execute_collaborative_task(self, task: str) -> Dict:
        """Execute task using agent collaboration."""

        print(f"Coordinator processing task: {task}")

        # Coordinator decides which agents to involve
        coordinator = self.agents["coordinator"]
        result = coordinator.execute(
            f"""Coordinate this task: {task}

            Available specialist agents:
            - Research Specialist: web_search, data_analysis, fact_checking
            - Code Specialist: code_review, code_generation, debugging
            - Writing Specialist: technical_writing, documentation, reporting

            Determine which specialists to involve and delegate appropriately.
            """
        )

        return {
            "task": task,
            "coordinator_response": result["result"],
            "a2a_interactions": result["a2a_interactions"],
            "agents_involved": list(self.agents.keys())
        }

# Usage Example
def run_a2a_examples():
    """Run A2A integration examples."""
    api_key = os.getenv("GOOGLE_API_KEY")

    print("="*80)
    print("A2A MULTI-AGENT SYSTEM")
    print("="*80)

    # Create A2A system
    system = A2AMultiAgentSystem(api_key=api_key)

    # Example tasks
    tasks = [
        "Research latest AI frameworks and create a comparison document",
        "Review this Python code and write documentation for it",
        "Analyze market trends and generate executive summary"
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n{'='*80}")
        print(f"TASK {i}: {task}")
        print(f"{'='*80}\n")

        result = system.execute_collaborative_task(task)

        print(f"Result: {result['coordinator_response']}")
        print(f"\nA2A Interactions: {result['a2a_interactions']}")
        print(f"Agents in System: {', '.join(result['agents_involved'])}")

if __name__ == "__main__":
    run_a2a_examples()
```

### A2A Best Practices

**1. Agent Discovery**
- Implement robust agent discovery mechanisms
- Maintain updated registry of available agents
- Handle agent unavailability gracefully

**2. Message Validation**
- Validate all incoming A2A messages
- Implement request/response timeouts
- Handle malformed messages properly

**3. Security**
- Treat external agents as untrusted
- Validate and sanitize all external inputs
- Implement authentication and authorization
- Prevent prompt injection attacks

**4. Error Handling**
- Implement retry logic for failed communications
- Provide meaningful error messages
- Log all A2A interactions

**5. Performance**
- Use async communication when possible
- Implement caching for frequent requests
- Monitor agent response times

---

## Advanced Patterns

### 1. Hierarchical Agent Systems

```python
class HierarchicalAgentSystem:
    """Hierarchical multi-level agent organization."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)
        self.hierarchy = self._build_hierarchy()

    def _build_hierarchy(self) -> Dict:
        """Build three-level hierarchy."""

        # Level 3: Worker Agents (lowest level)
        workers = {
            "data_fetcher": Agent(
                name="data_fetcher",
                model="gemini-1.5-flash",
                instructions="Fetch data from sources",
                tools=[web_search]
            ),
            "data_processor": Agent(
                name="data_processor",
                model="gemini-1.5-flash",
                instructions="Process and clean data",
                tools=[analyze_sentiment]
            ),
            "report_generator": Agent(
                name="report_generator",
                model="gemini-1.5-flash",
                instructions="Generate formatted reports",
                tools=[create_structured_report]
            )
        }

        # Level 2: Team Leads (middle management)
        # These agents coordinate workers
        team_leads = {
            "data_team_lead": Agent(
                name="data_team_lead",
                model="gemini-1.5-flash",
                instructions="Coordinate data fetching and processing",
                tools=[]  # Delegates to workers
            ),
            "reporting_lead": Agent(
                name="reporting_lead",
                model="gemini-1.5-flash",
                instructions="Coordinate report generation",
                tools=[]
            )
        }

        # Level 1: Executive (top level)
        executive = Agent(
            name="executive",
            model="gemini-1.5-pro",
            instructions="""You are the executive coordinator.

            Responsibilities:
            - Understand high-level goals
            - Break down into team-level objectives
            - Coordinate team leads
            - Synthesize final results
            """,
            tools=[]
        )

        return {
            "level_1": {"executive": executive},
            "level_2": team_leads,
            "level_3": workers
        }

    def execute_hierarchical(self, goal: str) -> Dict:
        """Execute goal through hierarchy."""

        # Level 1: Executive planning
        exec_agent = self.hierarchy["level_1"]["executive"]
        exec_result = self.runner.run(
            agent=exec_agent,
            input=f"Break down this goal into team objectives: {goal}"
        )

        # Level 2: Team leads coordinate
        # (Simplified - in production, parse exec_result for specific tasks)
        data_lead = self.hierarchy["level_2"]["data_team_lead"]
        data_result = self.runner.run(
            agent=data_lead,
            input="Coordinate data collection and processing"
        )

        # Level 3: Workers execute
        fetcher = self.hierarchy["level_3"]["data_fetcher"]
        fetch_result = self.runner.run(
            agent=fetcher,
            input="Fetch required data"
        )

        return {
            "goal": goal,
            "executive_plan": exec_result.output,
            "team_execution": data_result.output,
            "worker_results": fetch_result.output
        }

# Usage
def run_hierarchical_example():
    system = HierarchicalAgentSystem(api_key=os.getenv("GOOGLE_API_KEY"))
    result = system.execute_hierarchical(
        "Create comprehensive market analysis report"
    )
    print(json.dumps(result, indent=2))
```

### 2. Event-Driven Agent System

```python
from queue import Queue
from threading import Thread

class Event:
    """System event."""
    def __init__(self, event_type: str, data: Dict):
        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.now()

class EventDrivenAgentSystem:
    """Event-driven multi-agent system."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)
        self.event_queue = Queue()
        self.agents = self._create_agents()
        self.event_handlers = self._setup_handlers()

    def _create_agents(self) -> Dict[str, Agent]:
        """Create event-responsive agents."""
        return {
            "monitor": Agent(
                name="monitor",
                model="gemini-1.5-flash",
                instructions="Monitor events and trigger responses"
            ),
            "responder": Agent(
                name="responder",
                model="gemini-1.5-flash",
                instructions="Respond to triggered events"
            )
        }

    def _setup_handlers(self) -> Dict:
        """Setup event handlers."""
        return {
            "data_received": self._handle_data_event,
            "error_occurred": self._handle_error_event,
            "task_completed": self._handle_completion_event
        }

    def _handle_data_event(self, event: Event):
        """Handle data received event."""
        agent = self.agents["responder"]
        result = self.runner.run(
            agent=agent,
            input=f"Process new data: {event.data}"
        )
        print(f"Data processed: {result.output[:100]}...")

    def _handle_error_event(self, event: Event):
        """Handle error event."""
        agent = self.agents["responder"]
        result = self.runner.run(
            agent=agent,
            input=f"Handle error: {event.data}"
        )
        print(f"Error handled: {result.output[:100]}...")

    def _handle_completion_event(self, event: Event):
        """Handle task completion event."""
        print(f"Task completed: {event.data}")

    def emit_event(self, event_type: str, data: Dict):
        """Emit event to system."""
        event = Event(event_type, data)
        self.event_queue.put(event)

    def process_events(self):
        """Process events from queue."""
        while not self.event_queue.empty():
            event = self.event_queue.get()
            handler = self.event_handlers.get(event.event_type)
            if handler:
                handler(event)
            self.event_queue.task_done()

# Usage
def run_event_driven_example():
    system = EventDrivenAgentSystem(api_key=os.getenv("GOOGLE_API_KEY"))

    # Emit events
    system.emit_event("data_received", {"source": "API", "records": 100})
    system.emit_event("task_completed", {"task_id": "123", "status": "success"})

    # Process
    system.process_events()
```

### 3. Self-Improving Agent

```python
class SelfImprovingAgent:
    """Agent that learns from interactions."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)
        self.feedback_history = []
        self.performance_metrics = {
            "successful_tasks": 0,
            "failed_tasks": 0,
            "average_quality": 0.0
        }
        self.agent = self._create_adaptive_agent()

    def _create_adaptive_agent(self) -> Agent:
        """Create agent that adapts based on feedback."""

        instructions = self._generate_instructions()

        return Agent(
            name="self_improving",
            model="gemini-1.5-pro",
            instructions=instructions,
            tools=[web_search, analyze_sentiment]
        )

    def _generate_instructions(self) -> str:
        """Generate instructions based on performance history."""

        base_instructions = "You are a helpful assistant that learns from feedback."

        if self.feedback_history:
            recent_feedback = self.feedback_history[-5:]
            feedback_summary = "\n".join([
                f"- {fb['task']}: {fb['feedback']}"
                for fb in recent_feedback
            ])

            adaptive_instructions = f"""

Recent Performance Feedback:
{feedback_summary}

Adjust your approach based on this feedback to improve performance.
"""
            return base_instructions + adaptive_instructions

        return base_instructions

    def execute_with_learning(self, task: str) -> Dict:
        """Execute task and prepare for feedback."""
        result = self.runner.run(agent=self.agent, input=task)

        return {
            "task_id": str(uuid.uuid4()),
            "task": task,
            "result": result.output,
            "metadata": result.metadata
        }

    def provide_feedback(self, task_id: str, task: str, feedback: str, quality_score: float):
        """Provide feedback to improve agent."""

        self.feedback_history.append({
            "task_id": task_id,
            "task": task,
            "feedback": feedback,
            "quality_score": quality_score,
            "timestamp": datetime.now()
        })

        # Update metrics
        if quality_score >= 0.7:
            self.performance_metrics["successful_tasks"] += 1
        else:
            self.performance_metrics["failed_tasks"] += 1

        # Update average quality
        scores = [fb["quality_score"] for fb in self.feedback_history]
        self.performance_metrics["average_quality"] = np.mean(scores)

        # Recreate agent with updated instructions
        self.agent = self._create_adaptive_agent()

    def get_performance_report(self) -> Dict:
        """Get agent performance report."""
        return {
            "metrics": self.performance_metrics,
            "total_interactions": len(self.feedback_history),
            "recent_feedback": self.feedback_history[-5:]
        }

# Usage
def run_self_improving_example():
    agent = SelfImprovingAgent(api_key=os.getenv("GOOGLE_API_KEY"))

    # Task 1
    result1 = agent.execute_with_learning("Explain quantum computing")
    agent.provide_feedback(
        result1["task_id"],
        result1["task"],
        "Good explanation but could be more concise",
        quality_score=0.75
    )

    # Task 2 - agent adapts based on feedback
    result2 = agent.execute_with_learning("Explain machine learning")
    agent.provide_feedback(
        result2["task_id"],
        result2["task"],
        "Excellent concise explanation",
        quality_score=0.95
    )

    # Check performance
    report = agent.get_performance_report()
    print(json.dumps(report, indent=2, default=str))
```

---

## Production Best Practices

### 1. Error Handling

```python
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustAgent:
    """Production-ready agent with comprehensive error handling."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(
            api_key=api_key,
            timeout=30,
            max_retries=3
        )
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Create agent with error handling."""
        return Agent(
            name="production_agent",
            model="gemini-1.5-flash",
            instructions="You are a production assistant with robust error handling.",
            tools=[web_search]
        )

    def execute_safe(self, task: str) -> Optional[Dict]:
        """Execute task with comprehensive error handling."""
        try:
            logger.info(f"Executing task: {task[:50]}...")

            result = self.runner.run(
                agent=self.agent,
                input=task
            )

            logger.info("Task completed successfully")

            return {
                "status": "success",
                "result": result.output,
                "metadata": result.metadata
            }

        except TimeoutError:
            logger.error("Task timed out")
            return {
                "status": "error",
                "error_type": "timeout",
                "message": "Task execution timed out"
            }

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return {
                "status": "error",
                "error_type": "validation",
                "message": str(e)
            }

        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return {
                "status": "error",
                "error_type": "unexpected",
                "message": "An unexpected error occurred"
            }
```

### 2. Rate Limiting

```python
from time import time, sleep

class RateLimitedAgent:
    """Agent with rate limiting."""

    def __init__(self, api_key: str, max_requests_per_minute: int = 60):
        self.runner = AgentRunner(api_key=api_key)
        self.agent = Agent(
            name="rate_limited",
            model="gemini-1.5-flash",
            instructions="You are a rate-limited assistant."
        )

        self.max_requests = max_requests_per_minute
        self.request_times = []

    def execute_with_rate_limit(self, task: str) -> Dict:
        """Execute with rate limiting."""

        # Clean old requests (older than 1 minute)
        current_time = time()
        self.request_times = [
            t for t in self.request_times
            if current_time - t < 60
        ]

        # Check rate limit
        if len(self.request_times) >= self.max_requests:
            oldest_request = min(self.request_times)
            wait_time = 60 - (current_time - oldest_request)

            if wait_time > 0:
                logger.info(f"Rate limit reached, waiting {wait_time:.2f}s")
                sleep(wait_time)

        # Execute request
        self.request_times.append(time())
        result = self.runner.run(agent=self.agent, input=task)

        return {
            "result": result.output,
            "requests_in_window": len(self.request_times)
        }
```

### 3. Monitoring and Logging

```python
import json
from datetime import datetime

class MonitoredAgent:
    """Agent with comprehensive monitoring."""

    def __init__(self, api_key: str):
        self.runner = AgentRunner(api_key=api_key)
        self.agent = Agent(
            name="monitored",
            model="gemini-1.5-flash",
            instructions="You are a monitored assistant."
        )

        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens": 0,
            "total_duration_ms": 0
        }

    def execute_monitored(self, task: str) -> Dict:
        """Execute with monitoring."""

        start_time = time()
        self.metrics["total_requests"] += 1

        try:
            result = self.runner.run(agent=self.agent, input=task)

            # Update metrics
            self.metrics["successful_requests"] += 1
            self.metrics["total_tokens"] += result.metadata.get("tokens_used", 0)
            duration = (time() - start_time) * 1000
            self.metrics["total_duration_ms"] += duration

            # Log
            self._log_request(task, result, duration, "success")

            return {
                "status": "success",
                "result": result.output
            }

        except Exception as e:
            self.metrics["failed_requests"] += 1
            duration = (time() - start_time) * 1000

            # Log error
            self._log_request(task, None, duration, "error", str(e))

            raise

    def _log_request(
        self,
        task: str,
        result: Optional[Any],
        duration: float,
        status: str,
        error: Optional[str] = None
    ):
        """Log request details."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task[:100],
            "status": status,
            "duration_ms": duration,
            "error": error
        }

        if result:
            log_entry["tokens"] = result.metadata.get("tokens_used", 0)

        logger.info(json.dumps(log_entry))

    def get_metrics(self) -> Dict:
        """Get performance metrics."""
        total = self.metrics["total_requests"]

        return {
            **self.metrics,
            "success_rate": (
                self.metrics["successful_requests"] / total
                if total > 0 else 0
            ),
            "avg_duration_ms": (
                self.metrics["total_duration_ms"] / total
                if total > 0 else 0
            ),
            "avg_tokens_per_request": (
                self.metrics["total_tokens"] / total
                if total > 0 else 0
            )
        }
```

---

## Troubleshooting

### Common Issues and Solutions

**1. API Key Issues**

*Problem*: "Invalid API key" or authentication errors

*Solution*:
```python
# Verify API key is set
import os
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set")

# Test API key
try:
    runner = AgentRunner(api_key=api_key)
    test_agent = Agent(name="test", model="gemini-1.5-flash", instructions="Test")
    runner.run(agent=test_agent, input="Hello")
    print("✓ API key valid")
except Exception as e:
    print(f"✗ API key invalid: {e}")
```

**2. Tool Call Failures**

*Problem*: Agent doesn't call tools or calls wrong tools

*Solution*:
```python
# Ensure clear tool descriptions
@function_tool
def my_tool(param: str) -> str:
    """CLEAR DESCRIPTION: What this tool does, when to use it.

    Args:
        param: CLEAR parameter description

    Returns:
        CLEAR return value description
    """
    return result

# Test tool independently
result = my_tool("test_input")
print(f"Tool works: {result}")
```

**3. Timeout Issues**

*Problem*: Requests timing out

*Solution*:
```python
# Increase timeout
runner = AgentRunner(
    api_key=api_key,
    timeout=120  # 2 minutes
)

# Or handle timeouts gracefully
try:
    result = runner.run(agent=agent, input=task)
except TimeoutError:
    print("Request timed out, retrying with simpler task...")
    result = runner.run(agent=agent, input=simplified_task)
```

**4. Memory/Context Issues**

*Problem*: Agent forgets context or context too large

*Solution*:
```python
# Use session IDs for stateful conversations
session_id = str(uuid.uuid4())

# Split long conversations
if message_count > 10:
    # Summarize and start new session
    summary = runner.run(agent=agent, input="Summarize our conversation")
    session_id = str(uuid.uuid4())  # New session
    runner.run(
        agent=agent,
        input=f"Previous context: {summary.output}\n\nNew query: {query}",
        session_id=session_id
    )
```

**5. Rate Limiting**

*Problem*: "Rate limit exceeded" errors

*Solution*:
```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RateLimitError:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        print(f"Rate limited, waiting {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def execute_task(agent, runner, task):
    return runner.run(agent=agent, input=task)
```

---

## Conclusion

Google ADK provides a powerful, production-ready framework for building sophisticated AI agents. This deep dive covered:

- **System Architecture**: Understanding the layered architecture and component interactions
- **Core Components**: Agents, AgentRunner, tools, and state management
- **End-to-End Flow**: Complete request lifecycle from input to output
- **Simple to Complex Agents**: Progressive examples from basic to advanced
- **Multi-Agent Systems**: Sequential, collaborative, and supervisor-worker patterns
- **Agentic RAG**: Retrieval-augmented generation with intelligent agents
- **MCP Integration**: Connecting agents to standardized tool servers
- **A2A Protocol**: Agent-to-agent communication and collaboration
- **Advanced Patterns**: Hierarchical systems, event-driven architectures, self-improvement
- **Production Practices**: Error handling, rate limiting, monitoring
- **Troubleshooting**: Common issues and solutions

### Next Steps

1. **Start Simple**: Begin with basic agents and tools
2. **Add Complexity**: Gradually introduce multi-agent patterns
3. **Integrate External Systems**: Connect to databases, APIs, MCP servers
4. **Implement Production Features**: Add monitoring, error handling, rate limiting
5. **Optimize**: Profile and optimize for your specific use cases

### Resources

- **Google ADK GitHub**: https://github.com/google/adk-python
- **Gemini API Docs**: https://ai.google.dev/docs
- **MCP Protocol**: https://modelcontextprotocol.io
- **A2A Samples**: https://github.com/a2aproject/a2a-samples

---

**Document Version**: 1.0
**Last Updated**: 2026-01-19
**Total Lines**: 2400+
**Status**: Production Ready
