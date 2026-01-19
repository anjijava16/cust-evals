# LangGraph Deep Dive: Comprehensive Guide

## Table of Contents
1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [High-Level System Architecture](#high-level-system-architecture)
4. [Core Components Deep Dive](#core-components-deep-dive)
5. [End-to-End Flow](#end-to-end-flow)
6. [Simple Agent Examples](#simple-agent-examples)
7. [Complex Agent Examples](#complex-agent-examples)
8. [Multi-Agent Systems](#multi-agent-systems)
9. [RAG with Agents (Agentic RAG)](#rag-with-agents-agentic-rag)
10. [FastMCP Servers with Agents](#fastmcp-servers-with-agents)
11. [A2A (Agent-to-Agent) Examples](#a2a-agent-to-agent-examples)
12. [Advanced Patterns](#advanced-patterns)
13. [Production Considerations](#production-considerations)

---

## Introduction

LangGraph is a library for building stateful, multi-actor applications with LLMs, built on top of LangChain. It extends the LangChain Expression Language with the ability to coordinate multiple chains (or actors) across multiple steps of computation in a cyclic manner. It is inspired by Pregel and Apache Beam.

### Key Features
- **Graph-based Architecture**: Define agent workflows as directed graphs
- **State Management**: Built-in state persistence and checkpointing
- **Cyclic Flows**: Support for loops and conditional branching
- **Multi-Agent Coordination**: Native support for multiple agents working together
- **Human-in-the-Loop**: Easy integration of human feedback
- **Streaming Support**: Real-time streaming of intermediate steps
- **Time Travel**: Ability to replay and fork from any point in execution
- **LangSmith Integration**: Native observability and debugging

---

## System Architecture

### Architectural Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         LangGraph System                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Application Layer                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  Agent   │  │ Workflow │  │  Human   │  │  Tools   │  │  │
│  │  │  Nodes   │  │  Logic   │  │   Loop   │  │  Layer   │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Graph Execution Layer                   │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  State   │  │  Node    │  │  Edge    │  │ Conditional│ │  │
│  │  │  Graph   │  │ Executor │  │ Router   │  │  Router  │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    State Management Layer                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  State   │  │Checkpoint│  │  State   │  │  History │  │  │
│  │  │  Store   │  │  Manager │  │ Reducer  │  │  Tracker │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Persistence Layer                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │ Memory   │  │  SQLite  │  │PostgreSQL│  │  Redis   │  │  │
│  │  │  Store   │  │  Backend │  │  Backend │  │  Backend │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Integration Layer                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │LangChain │  │LangSmith │  │   MCP    │  │   A2A    │  │  │
│  │  │   Core   │  │   Tracing│  │ Servers  │  │ Protocol │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. StateGraph
The fundamental building block of LangGraph. It defines:
- **Nodes**: Individual computational units (functions, agents, tools)
- **Edges**: Connections between nodes (conditional or unconditional)
- **State**: Shared state passed between nodes
- **Entry Point**: Where execution begins
- **Finish Points**: Where execution can end

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_action: str
    context: dict

# Create graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tool", tool_node)
workflow.add_node("validator", validator_node)

# Add edges
workflow.add_edge("agent", "tool")
workflow.add_conditional_edges(
    "tool",
    should_continue,
    {
        "continue": "agent",
        "end": END
    }
)

workflow.set_entry_point("agent")
```

#### 2. Checkpointer
Handles state persistence and enables time-travel debugging:

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Create checkpointer
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

# Compile graph with checkpointing
app = workflow.compile(checkpointer=checkpointer)

# Execute with thread_id for persistence
config = {"configurable": {"thread_id": "conversation-1"}}
result = app.invoke(input_data, config=config)

# Resume from checkpoint
continued_result = app.invoke(more_input, config=config)
```

#### 3. State Channels
Define how state updates are merged:

```python
from langgraph.graph import add
from typing import Annotated

class State(TypedDict):
    # Append to list
    messages: Annotated[list, add]

    # Replace value
    current_step: str

    # Custom reducer
    scores: Annotated[dict, custom_merge_function]

def custom_merge_function(left: dict, right: dict) -> dict:
    """Custom logic for merging state"""
    return {**left, **right}
```

#### 4. Prebuilt Components

LangGraph provides prebuilt agent executors:

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """Search for information"""
    return f"Results for: {query}"

llm = ChatOpenAI(model="gpt-4")
tools = [search]

# Create ReAct agent
agent = create_react_agent(llm, tools)

# Execute
result = agent.invoke({
    "messages": [("user", "What is LangGraph?")]
})
```

---

## High-Level System Architecture

### Data Flow Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Client Application                         │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                         API Layer                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐     │
│  │  REST API      │  │  WebSocket     │  │  Streaming     │     │
│  │  Endpoint      │  │  Handler       │  │  Response      │     │
│  └────────────────┘  └────────────────┘  └────────────────┘     │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                    LangGraph Runtime                              │
│                                                                    │
│  ┌────────────────────────────────────────────────────────┐      │
│  │              Graph Compiler & Executor                  │      │
│  │                                                          │      │
│  │  Input → [Node 1] → [Conditional] → [Node 2] → Output  │      │
│  │              ↓            ↓              ↓              │      │
│  │          [State]      [Router]      [State]            │      │
│  └────────────────────────────────────────────────────────┘      │
│                            │                                       │
│  ┌─────────────────────────┴───────────────────────┐             │
│  │                                                   │             │
│  ▼                                                   ▼             │
│  ┌────────────────┐                      ┌────────────────┐      │
│  │  Node Executor │                      │ State Manager  │      │
│  ├────────────────┤                      ├────────────────┤      │
│  │ - Agent Nodes  │◄────────────────────►│ - Get State    │      │
│  │ - Tool Nodes   │    State Updates     │ - Update State │      │
│  │ - LLM Nodes    │                      │ - Checkpoint   │      │
│  │ - Custom Nodes │                      │ - History      │      │
│  └────────────────┘                      └────────────────┘      │
│         │                                        │                │
└─────────┼────────────────────────────────────────┼────────────────┘
          │                                        │
          ▼                                        ▼
┌──────────────────────┐              ┌─────────────────────────┐
│   External Services   │              │   Persistence Layer     │
├──────────────────────┤              ├─────────────────────────┤
│ - LLM APIs           │              │ - Checkpoints Store     │
│ - Vector Stores      │              │ - State Database        │
│ - Search APIs        │              │ - Conversation History  │
│ - MCP Servers        │              │ - Redis Cache           │
│ - External Tools     │              │ - File Storage          │
└──────────────────────┘              └─────────────────────────┘
          │                                        │
          └────────────┬───────────────────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │   Observability Layer   │
          ├─────────────────────────┤
          │ - LangSmith Tracing     │
          │ - Metrics Collection    │
          │ - Error Tracking        │
          │ - Performance Monitoring│
          └─────────────────────────┘
```

### Component Interaction Flow

1. **Request Reception**: Client sends request through API layer
2. **Graph Compilation**: Workflow graph is compiled into executable form
3. **State Initialization**: Initial state is created or loaded from checkpoint
4. **Node Execution**: Graph executor runs nodes in defined order
5. **State Updates**: Each node updates shared state
6. **Conditional Routing**: Edges determine next node based on state
7. **Checkpointing**: State is persisted at key points
8. **Response Streaming**: Intermediate results streamed to client
9. **Completion**: Final state returned to client

---

## Core Components Deep Dive

### 1. Graph Construction

#### Basic Graph Structure

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Literal
import operator

# Define state schema
class GraphState(TypedDict):
    messages: Annotated[list, operator.add]
    current_step: str
    iteration: int
    data: dict

# Initialize graph
graph = StateGraph(GraphState)

# Node functions
def process_input(state: GraphState) -> GraphState:
    """Process initial input"""
    messages = state["messages"]
    return {
        "messages": [f"Processed: {messages[-1]}"],
        "current_step": "processing",
        "iteration": state.get("iteration", 0) + 1
    }

def analyze_data(state: GraphState) -> GraphState:
    """Analyze processed data"""
    return {
        "messages": ["Analysis complete"],
        "current_step": "analysis",
        "data": {"analyzed": True}
    }

def make_decision(state: GraphState) -> GraphState:
    """Make decision based on analysis"""
    return {
        "messages": ["Decision made"],
        "current_step": "decision"
    }

# Add nodes
graph.add_node("process", process_input)
graph.add_node("analyze", analyze_data)
graph.add_node("decide", make_decision)

# Add edges
graph.add_edge("process", "analyze")
graph.add_edge("analyze", "decide")
graph.add_edge("decide", END)

# Set entry point
graph.set_entry_point("process")

# Compile
app = graph.compile()
```

#### Conditional Edges

```python
def route_decision(state: GraphState) -> Literal["continue", "end", "retry"]:
    """Route based on state"""
    if state.get("iteration", 0) > 5:
        return "end"
    elif state.get("data", {}).get("error"):
        return "retry"
    else:
        return "continue"

# Add conditional routing
graph.add_conditional_edges(
    "decide",
    route_decision,
    {
        "continue": "process",  # Loop back
        "end": END,
        "retry": "analyze"
    }
)
```

### 2. State Management Patterns

#### State Reducers

```python
from typing import Any

def merge_lists(left: list, right: list) -> list:
    """Merge two lists without duplicates"""
    return list(set(left + right))

def merge_dicts_deep(left: dict, right: dict) -> dict:
    """Deep merge dictionaries"""
    result = left.copy()
    for key, value in right.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts_deep(result[key], value)
        else:
            result[key] = value
    return result

class AdvancedState(TypedDict):
    # Append messages
    messages: Annotated[list, operator.add]

    # Merge unique items
    tags: Annotated[list, merge_lists]

    # Deep merge config
    config: Annotated[dict, merge_dicts_deep]

    # Replace (default behavior)
    status: str
```

#### State Channels

```python
from langgraph.channels import LastValue, Topic

class ChannelState(TypedDict):
    # Last value wins
    current_user: Annotated[str, LastValue()]

    # Publish-subscribe pattern
    notifications: Annotated[list, Topic()]

    # Accumulated values
    logs: Annotated[list, operator.add]
```

### 3. Checkpointing Mechanisms

#### SQLite Checkpointer

```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph

# Create checkpointer
checkpointer = SqliteSaver.from_conn_string("agent_checkpoints.db")

# Compile with checkpointing
app = workflow.compile(checkpointer=checkpointer)

# Use with thread ID
config = {
    "configurable": {
        "thread_id": "user-123-session-456"
    }
}

# First invocation
result1 = app.invoke({"messages": ["Hello"]}, config=config)

# Continue conversation (loads from checkpoint)
result2 = app.invoke({"messages": ["Tell me more"]}, config=config)

# Get checkpoint history
history = app.get_state_history(config)
for state_snapshot in history:
    print(f"Step: {state_snapshot.step}, State: {state_snapshot.values}")
```

#### Custom Checkpointer

```python
from langgraph.checkpoint import BaseCheckpointSaver
from typing import Optional
import redis
import json

class RedisCheckpointer(BaseCheckpointSaver):
    def __init__(self, redis_client):
        self.redis = redis_client

    def put(self, config: dict, checkpoint: dict) -> None:
        """Save checkpoint"""
        thread_id = config["configurable"]["thread_id"]
        key = f"checkpoint:{thread_id}"
        self.redis.set(key, json.dumps(checkpoint))

    def get(self, config: dict) -> Optional[dict]:
        """Load checkpoint"""
        thread_id = config["configurable"]["thread_id"]
        key = f"checkpoint:{thread_id}"
        data = self.redis.get(key)
        return json.loads(data) if data else None

# Use custom checkpointer
redis_client = redis.Redis(host='localhost', port=6379)
checkpointer = RedisCheckpointer(redis_client)
app = workflow.compile(checkpointer=checkpointer)
```

### 4. Streaming and Real-time Updates

#### Stream Graph Execution

```python
# Stream all intermediate steps
for chunk in app.stream({"messages": ["Hello"]}, config=config):
    print(f"Step: {chunk}")

# Stream with mode
for chunk in app.stream(
    {"messages": ["Hello"]},
    config=config,
    stream_mode="values"  # "values", "updates", "debug"
):
    print(chunk)

# Async streaming
async for chunk in app.astream({"messages": ["Hello"]}, config=config):
    print(chunk)
```

#### Custom Streaming

```python
from langgraph.pregel import Channel

def streaming_node(state: GraphState) -> GraphState:
    """Node that produces streaming output"""
    messages = []
    for i in range(10):
        message = f"Processing step {i}"
        messages.append(message)
        # Yield intermediate result
        yield {"messages": [message], "current_step": f"step_{i}"}

    return {"messages": messages, "current_step": "complete"}
```

---

## End-to-End Flow

### Complete Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         1. Input Phase                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  User Input → API → Graph Runtime → State Initialization        │
│                                                                   │
│  {                                                                │
│    "messages": ["User query"],                                   │
│    "config": {"thread_id": "session-123"}                        │
│  }                                                                │
│                                                                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    2. State Loading Phase                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Checkpointer.get(thread_id) → Load Previous State              │
│                                                                   │
│  if exists:                                                       │
│    state = merge(checkpoint_state, new_input)                    │
│  else:                                                            │
│    state = initialize_state(new_input)                           │
│                                                                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   3. Graph Traversal Phase                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  current_node = entry_point                                      │
│  while current_node != END:                                      │
│    │                                                              │
│    ├─► Execute Node                                              │
│    │   ├─ Load node function                                     │
│    │   ├─ Pass current state                                     │
│    │   ├─ Execute node logic                                     │
│    │   └─ Return state updates                                   │
│    │                                                              │
│    ├─► Update State                                              │
│    │   ├─ Apply state reducers                                   │
│    │   ├─ Merge updates with current state                       │
│    │   └─ Validate state schema                                  │
│    │                                                              │
│    ├─► Create Checkpoint                                         │
│    │   ├─ Serialize current state                                │
│    │   ├─ Save to persistence layer                              │
│    │   └─ Record metadata (timestamp, node, etc.)                │
│    │                                                              │
│    ├─► Determine Next Node                                       │
│    │   ├─ Check edge type (conditional/unconditional)            │
│    │   ├─ Execute routing function if conditional                │
│    │   └─ Set current_node to next node                          │
│    │                                                              │
│    └─► Stream Update (if enabled)                                │
│        └─ Send intermediate result to client                     │
│                                                                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     4. Output Phase                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Final State → Format Response → Return to Client                │
│                                                                   │
│  {                                                                │
│    "messages": [...],                                            │
│    "result": "...",                                              │
│    "metadata": {                                                 │
│      "steps": 5,                                                 │
│      "duration": "2.3s"                                          │
│    }                                                             │
│  }                                                               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Detailed Execution Example

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# State definition
class ExecutionState(TypedDict):
    messages: Annotated[list, operator.add]
    step_count: int
    context: dict

# Node implementations
def step_1_input_processing(state: ExecutionState) -> ExecutionState:
    """Step 1: Process input"""
    print(f"[Step 1] Processing input: {state['messages']}")
    return {
        "messages": ["Processed input"],
        "step_count": 1,
        "context": {"input_processed": True}
    }

def step_2_analysis(state: ExecutionState) -> ExecutionState:
    """Step 2: Analyze data"""
    print(f"[Step 2] Analyzing data, current count: {state['step_count']}")
    return {
        "messages": ["Analysis complete"],
        "step_count": state["step_count"] + 1,
        "context": {"analysis": "completed"}
    }

def step_3_decision(state: ExecutionState) -> ExecutionState:
    """Step 3: Make decision"""
    print(f"[Step 3] Making decision, current count: {state['step_count']}")
    return {
        "messages": ["Decision made"],
        "step_count": state["step_count"] + 1,
        "context": {"decision": "approved"}
    }

def should_continue(state: ExecutionState) -> str:
    """Routing logic"""
    if state["step_count"] >= 5:
        return "end"
    elif state["context"].get("error"):
        return "retry"
    else:
        return "continue"

# Build graph
workflow = StateGraph(ExecutionState)
workflow.add_node("process", step_1_input_processing)
workflow.add_node("analyze", step_2_analysis)
workflow.add_node("decide", step_3_decision)

workflow.add_edge("process", "analyze")
workflow.add_edge("analyze", "decide")
workflow.add_conditional_edges(
    "decide",
    should_continue,
    {
        "continue": "process",
        "retry": "analyze",
        "end": END
    }
)

workflow.set_entry_point("process")

# Compile and execute
app = workflow.compile()

# Run with streaming
print("Executing graph with streaming:\n")
for i, chunk in enumerate(app.stream({
    "messages": ["Start"],
    "step_count": 0,
    "context": {}
})):
    print(f"\n=== Chunk {i} ===")
    print(chunk)

# Final result
print("\n=== Final Result ===")
result = app.invoke({
    "messages": ["Start"],
    "step_count": 0,
    "context": {}
})
print(result)
```

---

## Simple Agent Examples

### Example 1: Basic Chatbot Agent

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import TypedDict, Annotated, Sequence
import operator

# State
class ChatState(TypedDict):
    messages: Annotated[Sequence, operator.add]

# LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Agent node
def chatbot(state: ChatState) -> ChatState:
    """Simple chatbot node"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Build graph
workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot)
workflow.set_entry_point("chatbot")
workflow.add_edge("chatbot", END)

# Compile
app = workflow.compile()

# Execute
response = app.invoke({
    "messages": [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What is LangGraph?")
    ]
})

print(response["messages"][-1].content)
```

### Example 2: Tool-Using Agent

```python
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expression"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_weather(location: str) -> str:
    """Get weather for a location"""
    # Mock implementation
    return f"Weather in {location}: Sunny, 72°F"

# Create agent with tools
llm = ChatOpenAI(model="gpt-4")
tools = [calculator, get_weather]

agent = create_react_agent(llm, tools)

# Execute
result = agent.invoke({
    "messages": [("user", "What's 25 * 4 and what's the weather in Paris?")]
})

for message in result["messages"]:
    print(f"{message.type}: {message.content}")
```

### Example 3: ReAct Agent with Custom Logic

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from typing import TypedDict, Literal

@tool
def search_database(query: str) -> str:
    """Search internal database"""
    return f"Database results for: {query}"

@tool
def web_search(query: str) -> str:
    """Search the web"""
    return f"Web results for: {query}"

class AgentState(TypedDict):
    messages: list
    next_action: str

llm = ChatOpenAI(model="gpt-4").bind_tools([search_database, web_search])

def agent_node(state: AgentState) -> AgentState:
    """Agent reasoning node"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def tool_node(state: AgentState) -> AgentState:
    """Tool execution node"""
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls

    results = []
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # Execute tool
        if tool_name == "search_database":
            result = search_database.invoke(tool_args)
        elif tool_name == "web_search":
            result = web_search.invoke(tool_args)

        results.append(
            ToolMessage(content=result, tool_call_id=tool_call["id"])
        )

    return {"messages": results}

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Determine if we should continue or end"""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app = workflow.compile()

# Execute
result = app.invoke({
    "messages": [HumanMessage(content="Search for LangGraph documentation")],
    "next_action": ""
})
```

### Example 4: Stateful Conversation Agent

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from typing import TypedDict

class ConversationState(TypedDict):
    messages: list
    user_name: str
    conversation_count: int

llm = ChatOpenAI(model="gpt-4")

def conversation_node(state: ConversationState) -> ConversationState:
    """Maintain conversation context"""
    user_name = state.get("user_name", "User")
    count = state.get("conversation_count", 0)

    system_msg = f"You are talking to {user_name}. This is message #{count + 1}."

    response = llm.invoke([
        {"role": "system", "content": system_msg},
        *state["messages"]
    ])

    return {
        "messages": [response],
        "conversation_count": count + 1
    }

# Build graph with memory
workflow = StateGraph(ConversationState)
workflow.add_node("chat", conversation_node)
workflow.set_entry_point("chat")
workflow.add_edge("chat", END)

# Compile with checkpointing
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# Multi-turn conversation
config = {"configurable": {"thread_id": "user-123"}}

# Turn 1
response1 = app.invoke({
    "messages": [{"role": "user", "content": "Hi, I'm Alice"}],
    "user_name": "Alice",
    "conversation_count": 0
}, config=config)

print(f"Turn 1: {response1['messages'][-1].content}")

# Turn 2 (continues from checkpoint)
response2 = app.invoke({
    "messages": [{"role": "user", "content": "What's my name?"}]
}, config=config)

print(f"Turn 2: {response2['messages'][-1].content}")
```

---

## Complex Agent Examples

### Example 1: Research Agent with Planning

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import TypedDict, List

@tool
def search_arxiv(query: str) -> str:
    """Search academic papers on ArXiv"""
    return f"Found papers about: {query}"

@tool
def search_web(query: str) -> str:
    """Search the web"""
    return f"Web results for: {query}"

@tool
def summarize_text(text: str) -> str:
    """Summarize long text"""
    return f"Summary: {text[:100]}..."

class ResearchState(TypedDict):
    task: str
    plan: List[str]
    research_data: List[dict]
    current_step: int
    final_report: str

llm = ChatOpenAI(model="gpt-4")

def planner_node(state: ResearchState) -> ResearchState:
    """Create research plan"""
    task = state["task"]

    prompt = f"""Create a step-by-step research plan for: {task}

    Provide 3-5 specific research steps."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    # Parse plan steps (simplified)
    steps = [line.strip() for line in response.content.split('\n') if line.strip()]

    return {
        "plan": steps[:5],
        "current_step": 0,
        "research_data": []
    }

def researcher_node(state: ResearchState) -> ResearchState:
    """Execute research step"""
    current_step = state["current_step"]
    plan = state["plan"]

    if current_step >= len(plan):
        return state

    step = plan[current_step]

    # Determine which tool to use
    if "paper" in step.lower() or "academic" in step.lower():
        result = search_arxiv.invoke({"query": step})
    else:
        result = search_web.invoke({"query": step})

    research_data = state.get("research_data", [])
    research_data.append({
        "step": step,
        "data": result
    })

    return {
        "research_data": research_data,
        "current_step": current_step + 1
    }

def synthesizer_node(state: ResearchState) -> ResearchState:
    """Synthesize findings into report"""
    research_data = state["research_data"]
    task = state["task"]

    data_summary = "\n".join([
        f"- {item['step']}: {item['data']}"
        for item in research_data
    ])

    prompt = f"""Based on this research data, write a comprehensive report for: {task}

    Research Data:
    {data_summary}

    Provide a structured report."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {"final_report": response.content}

def should_continue_research(state: ResearchState) -> str:
    """Check if more research is needed"""
    if state["current_step"] >= len(state["plan"]):
        return "synthesize"
    return "research"

# Build graph
workflow = StateGraph(ResearchState)
workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("synthesizer", synthesizer_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_conditional_edges(
    "researcher",
    should_continue_research,
    {
        "research": "researcher",
        "synthesize": "synthesizer"
    }
)
workflow.add_edge("synthesizer", END)

app = workflow.compile()

# Execute research task
result = app.invoke({
    "task": "Impact of LLMs on software development",
    "plan": [],
    "research_data": [],
    "current_step": 0,
    "final_report": ""
})

print("=== Research Plan ===")
for i, step in enumerate(result["plan"], 1):
    print(f"{i}. {step}")

print("\n=== Final Report ===")
print(result["final_report"])
```

### Example 2: Code Generation Agent with Validation

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List
import ast

class CodeGenState(TypedDict):
    requirement: str
    generated_code: str
    test_code: str
    validation_errors: List[str]
    iteration: int
    final_code: str

llm = ChatOpenAI(model="gpt-4", temperature=0)

def code_generator_node(state: CodeGenState) -> CodeGenState:
    """Generate code based on requirements"""
    requirement = state["requirement"]
    errors = state.get("validation_errors", [])
    iteration = state.get("iteration", 0)

    prompt = f"""Generate Python code for: {requirement}

    Requirements:
    - Include docstrings
    - Handle edge cases
    - Follow PEP 8
    """

    if errors:
        prompt += f"\n\nFix these validation errors:\n" + "\n".join(errors)

    response = llm.invoke([{"role": "user", "content": prompt}])

    # Extract code from response
    code = response.content
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()

    return {
        "generated_code": code,
        "iteration": iteration + 1
    }

def test_generator_node(state: CodeGenState) -> CodeGenState:
    """Generate test cases"""
    code = state["generated_code"]
    requirement = state["requirement"]

    prompt = f"""Generate pytest test cases for this code:

    ```python
    {code}
    ```

    Original requirement: {requirement}

    Include:
    - Normal cases
    - Edge cases
    - Error cases
    """

    response = llm.invoke([{"role": "user", "content": prompt}])

    test_code = response.content
    if "```python" in test_code:
        test_code = test_code.split("```python")[1].split("```")[0].strip()

    return {"test_code": test_code}

def validator_node(state: CodeGenState) -> CodeGenState:
    """Validate generated code"""
    code = state["generated_code"]
    errors = []

    # Syntax validation
    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append(f"Syntax error: {str(e)}")

    # Static analysis
    if "def " not in code:
        errors.append("No function definition found")

    if '"""' not in code and "'''" not in code:
        errors.append("Missing docstring")

    return {"validation_errors": errors}

def should_regenerate(state: CodeGenState) -> str:
    """Decide if code needs regeneration"""
    errors = state.get("validation_errors", [])
    iteration = state.get("iteration", 0)

    if not errors:
        return "finalize"
    elif iteration >= 3:
        return "finalize"  # Max iterations reached
    else:
        return "regenerate"

def finalizer_node(state: CodeGenState) -> CodeGenState:
    """Finalize and format code"""
    return {"final_code": state["generated_code"]}

# Build graph
workflow = StateGraph(CodeGenState)
workflow.add_node("generator", code_generator_node)
workflow.add_node("test_gen", test_generator_node)
workflow.add_node("validator", validator_node)
workflow.add_node("finalizer", finalizer_node)

workflow.set_entry_point("generator")
workflow.add_edge("generator", "test_gen")
workflow.add_edge("test_gen", "validator")
workflow.add_conditional_edges(
    "validator",
    should_regenerate,
    {
        "regenerate": "generator",
        "finalize": "finalizer"
    }
)
workflow.add_edge("finalizer", END)

app = workflow.compile()

# Generate code
result = app.invoke({
    "requirement": "Create a function to calculate fibonacci numbers with memoization",
    "generated_code": "",
    "test_code": "",
    "validation_errors": [],
    "iteration": 0,
    "final_code": ""
})

print("=== Generated Code ===")
print(result["final_code"])
print("\n=== Test Code ===")
print(result["test_code"])
```

### Example 3: Data Analysis Agent

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import TypedDict, List, Dict

@tool
def load_data(file_path: str) -> str:
    """Load data from file"""
    # Mock implementation
    return "Data loaded: 1000 rows, 5 columns"

@tool
def analyze_statistics(column: str) -> str:
    """Calculate statistics for a column"""
    # Mock implementation
    return f"Stats for {column}: mean=45.3, std=12.1, min=10, max=90"

@tool
def create_visualization(chart_type: str, data: str) -> str:
    """Create data visualization"""
    return f"Created {chart_type} chart"

class AnalysisState(TypedDict):
    query: str
    data_info: str
    analysis_steps: List[str]
    results: Dict[str, str]
    insights: List[str]
    report: str

llm = ChatOpenAI(model="gpt-4")

def query_analyzer_node(state: AnalysisState) -> AnalysisState:
    """Analyze user query and create analysis plan"""
    query = state["query"]

    prompt = f"""Analyze this data analysis request and create a step-by-step plan:

    Query: {query}

    List specific analysis steps needed."""

    response = llm.invoke([{"role": "user", "content": prompt}])
    steps = [s.strip() for s in response.content.split('\n') if s.strip()]

    return {"analysis_steps": steps}

def data_loader_node(state: AnalysisState) -> AnalysisState:
    """Load and inspect data"""
    result = load_data.invoke({"file_path": "data.csv"})
    return {"data_info": result}

def analyzer_node(state: AnalysisState) -> AnalysisState:
    """Perform analysis"""
    steps = state["analysis_steps"]
    results = {}

    for step in steps:
        if "statistic" in step.lower():
            result = analyze_statistics.invoke({"column": "sales"})
        elif "visualiz" in step.lower():
            result = create_visualization.invoke({"chart_type": "bar", "data": "sales"})
        else:
            result = f"Executed: {step}"

        results[step] = result

    return {"results": results}

def insight_generator_node(state: AnalysisState) -> AnalysisState:
    """Generate insights from results"""
    results = state["results"]
    query = state["query"]

    results_text = "\n".join([f"- {k}: {v}" for k, v in results.items()])

    prompt = f"""Based on these analysis results, provide key insights for: {query}

    Results:
    {results_text}

    Provide 3-5 actionable insights."""

    response = llm.invoke([{"role": "user", "content": prompt}])
    insights = [i.strip() for i in response.content.split('\n') if i.strip()]

    return {"insights": insights}

def report_generator_node(state: AnalysisState) -> AnalysisState:
    """Generate final report"""
    query = state["query"]
    insights = state["insights"]
    results = state["results"]

    report = f"""# Data Analysis Report

## Query
{query}

## Analysis Performed
{', '.join(results.keys())}

## Key Insights
{chr(10).join([f"{i+1}. {insight}" for i, insight in enumerate(insights)])}

## Detailed Results
{chr(10).join([f"**{k}**: {v}" for k, v in results.items()])}
"""

    return {"report": report}

# Build graph
workflow = StateGraph(AnalysisState)
workflow.add_node("query_analyzer", query_analyzer_node)
workflow.add_node("data_loader", data_loader_node)
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("insight_generator", insight_generator_node)
workflow.add_node("report_generator", report_generator_node)

workflow.set_entry_point("query_analyzer")
workflow.add_edge("query_analyzer", "data_loader")
workflow.add_edge("data_loader", "analyzer")
workflow.add_edge("analyzer", "insight_generator")
workflow.add_edge("insight_generator", "report_generator")
workflow.add_edge("report_generator", END)

app = workflow.compile()

# Execute analysis
result = app.invoke({
    "query": "Analyze sales trends and identify top performing products",
    "data_info": "",
    "analysis_steps": [],
    "results": {},
    "insights": [],
    "report": ""
})

print(result["report"])
```

---

## Multi-Agent Systems

### Example 1: Supervisor Multi-Agent Pattern

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import TypedDict, Literal

class MultiAgentState(TypedDict):
    messages: list
    next_agent: str
    task_result: dict

# Define specialized agents
llm = ChatOpenAI(model="gpt-4")

def supervisor_agent(state: MultiAgentState) -> MultiAgentState:
    """Supervisor that routes to specialized agents"""
    messages = state["messages"]

    system_prompt = """You are a supervisor managing specialized agents:
    - researcher: For gathering information
    - analyst: For analyzing data
    - writer: For creating content

    Based on the user request, decide which agent should handle it.
    Respond with ONLY the agent name."""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        *messages
    ])

    next_agent = response.content.strip().lower()

    return {
        "next_agent": next_agent,
        "messages": [response]
    }

def researcher_agent(state: MultiAgentState) -> MultiAgentState:
    """Research specialist agent"""
    messages = state["messages"]

    system_prompt = "You are a research specialist. Gather and summarize information."

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        *messages
    ])

    return {
        "messages": [response],
        "task_result": {"agent": "researcher", "completed": True}
    }

def analyst_agent(state: MultiAgentState) -> MultiAgentState:
    """Analysis specialist agent"""
    messages = state["messages"]

    system_prompt = "You are a data analyst. Analyze information and provide insights."

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        *messages
    ])

    return {
        "messages": [response],
        "task_result": {"agent": "analyst", "completed": True}
    }

def writer_agent(state: MultiAgentState) -> MultiAgentState:
    """Writing specialist agent"""
    messages = state["messages"]

    system_prompt = "You are a professional writer. Create clear, engaging content."

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        *messages
    ])

    return {
        "messages": [response],
        "task_result": {"agent": "writer", "completed": True}
    }

def route_to_agent(state: MultiAgentState) -> str:
    """Route to appropriate agent"""
    next_agent = state.get("next_agent", "end")

    if next_agent in ["researcher", "analyst", "writer"]:
        return next_agent
    return "end"

# Build multi-agent graph
workflow = StateGraph(MultiAgentState)

# Add agents
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("researcher", researcher_agent)
workflow.add_node("analyst", analyst_agent)
workflow.add_node("writer", writer_agent)

# Set entry point
workflow.set_entry_point("supervisor")

# Add conditional routing from supervisor
workflow.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "researcher": "researcher",
        "analyst": "analyst",
        "writer": "writer",
        "end": END
    }
)

# All agents return to END
workflow.add_edge("researcher", END)
workflow.add_edge("analyst", END)
workflow.add_edge("writer", END)

app = workflow.compile()

# Test with different queries
queries = [
    "Research the latest trends in AI",
    "Analyze this sales data",
    "Write a blog post about Python"
]

for query in queries:
    print(f"\n=== Query: {query} ===")
    result = app.invoke({
        "messages": [HumanMessage(content=query)],
        "next_agent": "",
        "task_result": {}
    })
    print(f"Routed to: {result['task_result']['agent']}")
    print(f"Response: {result['messages'][-1].content[:200]}...")
```

### Example 2: Collaborative Multi-Agent System

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List

class CollaborativeState(TypedDict):
    task: str
    contributions: List[dict]
    current_agent: str
    iteration: int
    final_output: str

llm = ChatOpenAI(model="gpt-4")

def idea_generator_agent(state: CollaborativeState) -> CollaborativeState:
    """Generate initial ideas"""
    task = state["task"]

    prompt = f"""Generate creative ideas for: {task}

    Provide 3-5 diverse ideas."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    contributions = state.get("contributions", [])
    contributions.append({
        "agent": "idea_generator",
        "content": response.content
    })

    return {
        "contributions": contributions,
        "current_agent": "critic"
    }

def critic_agent(state: CollaborativeState) -> CollaborativeState:
    """Critique and improve ideas"""
    contributions = state["contributions"]
    last_contribution = contributions[-1]["content"]

    prompt = f"""Review these ideas and provide constructive criticism:

    {last_contribution}

    Identify strengths and weaknesses."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    contributions.append({
        "agent": "critic",
        "content": response.content
    })

    return {
        "contributions": contributions,
        "current_agent": "improver"
    }

def improver_agent(state: CollaborativeState) -> CollaborativeState:
    """Improve based on criticism"""
    contributions = state["contributions"]
    ideas = contributions[0]["content"]
    criticism = contributions[1]["content"]

    prompt = f"""Improve these ideas based on the criticism:

    Original Ideas:
    {ideas}

    Criticism:
    {criticism}

    Provide improved versions."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    contributions.append({
        "agent": "improver",
        "content": response.content
    })

    return {
        "contributions": contributions,
        "current_agent": "synthesizer",
        "iteration": state.get("iteration", 0) + 1
    }

def synthesizer_agent(state: CollaborativeState) -> CollaborativeState:
    """Synthesize all contributions"""
    contributions = state["contributions"]
    task = state["task"]

    all_content = "\n\n".join([
        f"From {c['agent']}:\n{c['content']}"
        for c in contributions
    ])

    prompt = f"""Synthesize all contributions into a final solution for: {task}

    Contributions:
    {all_content}

    Provide a comprehensive, polished final output."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {
        "final_output": response.content,
        "current_agent": "done"
    }

def route_agents(state: CollaborativeState) -> str:
    """Route to next agent"""
    current = state.get("current_agent", "idea_generator")
    iteration = state.get("iteration", 0)

    if current == "done" or iteration >= 2:
        return "end"

    return current

# Build collaborative graph
workflow = StateGraph(CollaborativeState)

workflow.add_node("idea_generator", idea_generator_agent)
workflow.add_node("critic", critic_agent)
workflow.add_node("improver", improver_agent)
workflow.add_node("synthesizer", synthesizer_agent)

workflow.set_entry_point("idea_generator")

workflow.add_conditional_edges(
    "idea_generator",
    route_agents,
    {
        "critic": "critic",
        "end": END
    }
)

workflow.add_conditional_edges(
    "critic",
    route_agents,
    {
        "improver": "improver",
        "end": END
    }
)

workflow.add_conditional_edges(
    "improver",
    route_agents,
    {
        "synthesizer": "synthesizer",
        "critic": "critic",  # Loop for iteration
        "end": END
    }
)

workflow.add_edge("synthesizer", END)

app = workflow.compile()

# Execute collaborative task
result = app.invoke({
    "task": "Design an innovative mobile app for learning languages",
    "contributions": [],
    "current_agent": "idea_generator",
    "iteration": 0,
    "final_output": ""
})

print("=== Collaborative Process ===")
for i, contrib in enumerate(result["contributions"], 1):
    print(f"\n{i}. {contrib['agent'].upper()}:")
    print(contrib["content"][:300] + "...")

print("\n=== Final Synthesized Output ===")
print(result["final_output"])
```

### Example 3: Debate Multi-Agent System

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List

class DebateState(TypedDict):
    topic: str
    rounds: int
    current_round: int
    arguments: List[dict]
    judge_decision: str

llm = ChatOpenAI(model="gpt-4")

def agent_for(state: DebateState) -> DebateState:
    """Agent arguing FOR the topic"""
    topic = state["topic"]
    current_round = state["current_round"]
    arguments = state.get("arguments", [])

    # Get opponent's last argument if exists
    opponent_arg = ""
    if arguments and arguments[-1]["side"] == "against":
        opponent_arg = arguments[-1]["content"]

    prompt = f"""You are debating FOR: {topic}
    Round: {current_round}

    {"Opponent's argument: " + opponent_arg if opponent_arg else "Present your opening argument."}

    Provide a strong argument."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    arguments.append({
        "round": current_round,
        "side": "for",
        "content": response.content
    })

    return {"arguments": arguments}

def agent_against(state: DebateState) -> DebateState:
    """Agent arguing AGAINST the topic"""
    topic = state["topic"]
    current_round = state["current_round"]
    arguments = state["arguments"]

    # Get opponent's last argument
    opponent_arg = arguments[-1]["content"] if arguments else ""

    prompt = f"""You are debating AGAINST: {topic}
    Round: {current_round}

    Opponent's argument: {opponent_arg}

    Provide a strong counter-argument."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    arguments.append({
        "round": current_round,
        "side": "against",
        "content": response.content
    })

    return {
        "arguments": arguments,
        "current_round": current_round + 1
    }

def judge_agent(state: DebateState) -> DebateState:
    """Judge evaluates the debate"""
    topic = state["topic"]
    arguments = state["arguments"]

    debate_text = "\n\n".join([
        f"Round {arg['round']} - {arg['side'].upper()}:\n{arg['content']}"
        for arg in arguments
    ])

    prompt = f"""You are judging a debate on: {topic}

    Debate transcript:
    {debate_text}

    Evaluate both sides and declare a winner with reasoning."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {"judge_decision": response.content}

def should_continue_debate(state: DebateState) -> str:
    """Check if debate should continue"""
    current_round = state.get("current_round", 0)
    max_rounds = state.get("rounds", 3)

    if current_round >= max_rounds:
        return "judge"

    # Check whose turn it is
    arguments = state.get("arguments", [])
    if not arguments or arguments[-1]["side"] == "against":
        return "for"
    else:
        return "against"

# Build debate graph
workflow = StateGraph(DebateState)

workflow.add_node("agent_for", agent_for)
workflow.add_node("agent_against", agent_against)
workflow.add_node("judge", judge_agent)

workflow.set_entry_point("agent_for")

workflow.add_conditional_edges(
    "agent_for",
    should_continue_debate,
    {
        "against": "agent_against",
        "judge": "judge"
    }
)

workflow.add_conditional_edges(
    "agent_against",
    should_continue_debate,
    {
        "for": "agent_for",
        "judge": "judge"
    }
)

workflow.add_edge("judge", END)

app = workflow.compile()

# Run debate
result = app.invoke({
    "topic": "AI will replace human programmers within 10 years",
    "rounds": 3,
    "current_round": 1,
    "arguments": [],
    "judge_decision": ""
})

print("=== DEBATE TRANSCRIPT ===\n")
for arg in result["arguments"]:
    print(f"Round {arg['round']} - {arg['side'].upper()}:")
    print(arg["content"])
    print()

print("=== JUDGE'S DECISION ===")
print(result["judge_decision"])
```

---

## RAG with Agents (Agentic RAG)

### Example 1: Basic Agentic RAG

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.tools import tool
from typing import TypedDict, List

# Sample documents
documents = [
    Document(page_content="LangGraph is a library for building stateful, multi-actor applications with LLMs.",
             metadata={"source": "docs", "page": 1}),
    Document(page_content="LangGraph extends LangChain Expression Language with cyclic computation support.",
             metadata={"source": "docs", "page": 2}),
    Document(page_content="StateGraph is the main class for defining agent workflows in LangGraph.",
             metadata={"source": "docs", "page": 3}),
]

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

@tool
def retrieve_documents(query: str) -> str:
    """Retrieve relevant documents"""
    docs = retriever.get_relevant_documents(query)
    return "\n\n".join([doc.page_content for doc in docs])

@tool
def web_search(query: str) -> str:
    """Search the web for additional information"""
    # Mock implementation
    return f"Web search results for: {query}"

class AgenticRAGState(TypedDict):
    question: str
    retrieved_docs: str
    web_results: str
    analysis: str
    answer: str
    confidence: float

llm = ChatOpenAI(model="gpt-4")

def query_analyzer_node(state: AgenticRAGState) -> AgenticRAGState:
    """Analyze query complexity"""
    question = state["question"]

    prompt = f"""Analyze this question: {question}

    Determine:
    1. Can it be answered from documents alone?
    2. Does it need web search?
    3. Complexity level (1-5)

    Respond in format:
    docs_sufficient: yes/no
    needs_web: yes/no
    complexity: <number>
    """

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {"analysis": response.content}

def retriever_node(state: AgenticRAGState) -> AgenticRAGState:
    """Retrieve relevant documents"""
    question = state["question"]
    docs = retrieve_documents.invoke({"query": question})

    return {"retrieved_docs": docs}

def web_search_node(state: AgenticRAGState) -> AgenticRAGState:
    """Search web if needed"""
    question = state["question"]
    analysis = state.get("analysis", "")

    if "needs_web: yes" in analysis.lower():
        results = web_search.invoke({"query": question})
        return {"web_results": results}

    return {"web_results": ""}

def answer_generator_node(state: AgenticRAGState) -> AgenticRAGState:
    """Generate final answer"""
    question = state["question"]
    docs = state.get("retrieved_docs", "")
    web = state.get("web_results", "")

    context = f"Documents:\n{docs}"
    if web:
        context += f"\n\nWeb Results:\n{web}"

    prompt = f"""Answer this question based on the context:

    Question: {question}

    Context:
    {context}

    Provide a comprehensive answer and rate your confidence (0-1)."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    # Extract confidence (simplified)
    confidence = 0.8

    return {
        "answer": response.content,
        "confidence": confidence
    }

def should_search_web(state: AgenticRAGState) -> str:
    """Decide if web search is needed"""
    analysis = state.get("analysis", "")

    if "needs_web: yes" in analysis.lower():
        return "web_search"
    return "answer"

# Build agentic RAG graph
workflow = StateGraph(AgenticRAGState)

workflow.add_node("query_analyzer", query_analyzer_node)
workflow.add_node("retriever", retriever_node)
workflow.add_node("web_search", web_search_node)
workflow.add_node("answer_generator", answer_generator_node)

workflow.set_entry_point("query_analyzer")
workflow.add_edge("query_analyzer", "retriever")
workflow.add_conditional_edges(
    "retriever",
    should_search_web,
    {
        "web_search": "web_search",
        "answer": "answer_generator"
    }
)
workflow.add_edge("web_search", "answer_generator")
workflow.add_edge("answer_generator", END)

app = workflow.compile()

# Query the system
result = app.invoke({
    "question": "What is LangGraph and how does it work?",
    "retrieved_docs": "",
    "web_results": "",
    "analysis": "",
    "answer": "",
    "confidence": 0.0
})

print("=== Retrieved Documents ===")
print(result["retrieved_docs"])
print("\n=== Answer ===")
print(result["answer"])
print(f"\nConfidence: {result['confidence']}")
```

### Example 2: Advanced Agentic RAG with Self-Reflection

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import TypedDict, List, Literal

class SelfReflectiveRAGState(TypedDict):
    question: str
    documents: List[str]
    generation: str
    critique: str
    iteration: int
    final_answer: str

llm = ChatOpenAI(model="gpt-4", temperature=0)

# Mock vector store
def get_retriever():
    texts = [
        "LangGraph provides stateful agent workflows.",
        "Agents can use tools and make decisions.",
        "Multi-agent systems coordinate multiple AI agents.",
    ]
    return lambda q: texts

retriever = get_retriever()

def retrieve_node(state: SelfReflectiveRAGState) -> SelfReflectiveRAGState:
    """Retrieve documents"""
    question = state["question"]
    docs = retriever(question)

    return {"documents": docs}

def grade_documents_node(state: SelfReflectiveRAGState) -> SelfReflectiveRAGState:
    """Grade document relevance"""
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    for doc in documents:
        prompt = f"""Grade the relevance of this document to the question.

        Question: {question}
        Document: {doc}

        Answer 'yes' or 'no' only."""

        response = llm.invoke([{"role": "user", "content": prompt}])

        if "yes" in response.content.lower():
            filtered_docs.append(doc)

    return {"documents": filtered_docs}

def generate_node(state: SelfReflectiveRAGState) -> SelfReflectiveRAGState:
    """Generate answer"""
    question = state["question"]
    documents = state["documents"]

    context = "\n\n".join(documents)

    prompt = f"""Answer the question based on this context:

    Context:
    {context}

    Question: {question}

    Answer:"""

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {"generation": response.content}

def critique_node(state: SelfReflectiveRAGState) -> SelfReflectiveRAGState:
    """Critique the generated answer"""
    question = state["question"]
    generation = state["generation"]
    documents = state["documents"]

    prompt = f"""Critique this answer for accuracy and completeness:

    Question: {question}
    Answer: {generation}
    Context: {documents}

    Identify issues and suggest improvements."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {
        "critique": response.content,
        "iteration": state.get("iteration", 0) + 1
    }

def refine_node(state: SelfReflectiveRAGState) -> SelfReflectiveRAGState:
    """Refine answer based on critique"""
    question = state["question"]
    generation = state["generation"]
    critique = state["critique"]
    documents = state["documents"]

    prompt = f"""Improve this answer based on the critique:

    Question: {question}
    Original Answer: {generation}
    Critique: {critique}
    Context: {documents}

    Provide an improved answer."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {"generation": response.content}

def should_refine(state: SelfReflectiveRAGState) -> Literal["refine", "finalize"]:
    """Decide if refinement is needed"""
    iteration = state.get("iteration", 0)
    critique = state.get("critique", "")

    # Check if critique suggests major issues
    if iteration >= 2:
        return "finalize"

    if "issue" in critique.lower() or "improve" in critique.lower():
        return "refine"

    return "finalize"

def finalize_node(state: SelfReflectiveRAGState) -> SelfReflectiveRAGState:
    """Finalize answer"""
    return {"final_answer": state["generation"]}

# Build self-reflective RAG graph
workflow = StateGraph(SelfReflectiveRAGState)

workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade_documents", grade_documents_node)
workflow.add_node("generate", generate_node)
workflow.add_node("critique", critique_node)
workflow.add_node("refine", refine_node)
workflow.add_node("finalize", finalize_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_edge("grade_documents", "generate")
workflow.add_edge("generate", "critique")
workflow.add_conditional_edges(
    "critique",
    should_refine,
    {
        "refine": "refine",
        "finalize": "finalize"
    }
)
workflow.add_edge("refine", "critique")
workflow.add_edge("finalize", END)

app = workflow.compile()

# Execute
result = app.invoke({
    "question": "How do multi-agent systems work in LangGraph?",
    "documents": [],
    "generation": "",
    "critique": "",
    "iteration": 0,
    "final_answer": ""
})

print("=== Final Answer ===")
print(result["final_answer"])
print(f"\nIterations: {result['iteration']}")
```

### Example 3: Corrective RAG (CRAG) Pattern

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal, List

class CRAGState(TypedDict):
    question: str
    documents: List[str]
    document_relevance: str
    generation: str
    search_query: str
    web_results: str
    final_answer: str

llm = ChatOpenAI(model="gpt-4")

def retrieve_node(state: CRAGState) -> CRAGState:
    """Retrieve documents"""
    question = state["question"]
    # Mock retrieval
    docs = [
        "LangGraph enables building stateful agents.",
        "Agents can be composed in workflows."
    ]
    return {"documents": docs}

def grade_documents_node(state: CRAGState) -> CRAGState:
    """Grade document relevance"""
    question = state["question"]
    documents = state["documents"]

    prompt = f"""Grade if these documents are relevant to the question:

    Question: {question}
    Documents: {documents}

    Answer: 'relevant', 'partially_relevant', or 'not_relevant'"""

    response = llm.invoke([{"role": "user", "content": prompt}])
    relevance = response.content.strip().lower()

    return {"document_relevance": relevance}

def transform_query_node(state: CRAGState) -> CRAGState:
    """Transform query for better search"""
    question = state["question"]

    prompt = f"""Transform this question into a better search query:

    Original: {question}

    Provide an optimized search query."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {"search_query": response.content}

def web_search_node(state: CRAGState) -> CRAGState:
    """Perform web search"""
    query = state["search_query"]
    # Mock web search
    results = f"Web results for: {query}"

    return {"web_results": results}

def generate_answer_node(state: CRAGState) -> CRAGState:
    """Generate final answer"""
    question = state["question"]
    documents = state["documents"]
    web_results = state.get("web_results", "")

    context = "\n".join(documents)
    if web_results:
        context += f"\n\nAdditional info: {web_results}"

    prompt = f"""Answer based on this context:

    Context: {context}
    Question: {question}

    Answer:"""

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {"final_answer": response.content}

def decide_next_step(state: CRAGState) -> Literal["transform", "generate"]:
    """Decide whether to search web or generate directly"""
    relevance = state["document_relevance"]

    if "not_relevant" in relevance:
        return "transform"
    return "generate"

# Build CRAG graph
workflow = StateGraph(CRAGState)

workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade", grade_documents_node)
workflow.add_node("transform", transform_query_node)
workflow.add_node("web_search", web_search_node)
workflow.add_node("generate", generate_answer_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade")
workflow.add_conditional_edges(
    "grade",
    decide_next_step,
    {
        "transform": "transform",
        "generate": "generate"
    }
)
workflow.add_edge("transform", "web_search")
workflow.add_edge("web_search", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()

# Execute
result = app.invoke({
    "question": "What are the latest features in LangGraph 2024?",
    "documents": [],
    "document_relevance": "",
    "generation": "",
    "search_query": "",
    "web_results": "",
    "final_answer": ""
})

print("=== Document Relevance ===")
print(result["document_relevance"])
print("\n=== Final Answer ===")
print(result["final_answer"])
```

---

## FastMCP Servers with Agents

### Example 1: LangGraph Agent with MCP Server

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List
import httpx
import json

class MCPAgentState(TypedDict):
    messages: List[dict]
    mcp_tools: List[dict]
    tool_results: List[dict]
    response: str

# MCP Server Configuration
MCP_SERVER_URL = "http://localhost:8000"

async def fetch_mcp_tools() -> List[dict]:
    """Fetch available tools from MCP server"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MCP_SERVER_URL}/tools")
        return response.json()

async def call_mcp_tool(tool_name: str, parameters: dict) -> dict:
    """Call an MCP tool"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{MCP_SERVER_URL}/call_tool",
            json={
                "name": tool_name,
                "parameters": parameters
            }
        )
        return response.json()

llm = ChatOpenAI(model="gpt-4")

async def tool_discovery_node(state: MCPAgentState) -> MCPAgentState:
    """Discover available MCP tools"""
    tools = await fetch_mcp_tools()

    return {"mcp_tools": tools}

def agent_planning_node(state: MCPAgentState) -> MCPAgentState:
    """Agent plans which tools to use"""
    messages = state["messages"]
    mcp_tools = state["mcp_tools"]

    tools_description = "\n".join([
        f"- {tool['name']}: {tool['description']}"
        for tool in mcp_tools
    ])

    prompt = f"""You have access to these MCP tools:

    {tools_description}

    User message: {messages[-1]['content']}

    Which tools should you use and with what parameters?
    Respond in JSON format:
    {{
        "tools": [
            {{"name": "tool_name", "parameters": {{...}}}}
        ]
    }}
    """

    response = llm.invoke([{"role": "user", "content": prompt}])

    # Parse tool calls (simplified)
    try:
        tool_calls = json.loads(response.content)
        return {"messages": [{"role": "assistant", "content": response.content}]}
    except:
        return {"messages": [{"role": "assistant", "content": response.content}]}

async def tool_execution_node(state: MCPAgentState) -> MCPAgentState:
    """Execute MCP tools"""
    messages = state["messages"]
    last_message = messages[-1]["content"]

    try:
        tool_calls = json.loads(last_message)
        results = []

        for tool_call in tool_calls.get("tools", []):
            result = await call_mcp_tool(
                tool_call["name"],
                tool_call["parameters"]
            )
            results.append({
                "tool": tool_call["name"],
                "result": result
            })

        return {"tool_results": results}
    except:
        return {"tool_results": []}

def response_generation_node(state: MCPAgentState) -> MCPAgentState:
    """Generate final response"""
    messages = state["messages"]
    tool_results = state.get("tool_results", [])

    results_text = "\n".join([
        f"{r['tool']}: {r['result']}"
        for r in tool_results
    ])

    prompt = f"""Based on these tool results, provide a response:

    Tool Results:
    {results_text}

    Original query: {messages[0]['content']}

    Provide a helpful response."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {"response": response.content}

# Build MCP agent graph
workflow = StateGraph(MCPAgentState)

workflow.add_node("discover_tools", tool_discovery_node)
workflow.add_node("plan", agent_planning_node)
workflow.add_node("execute_tools", tool_execution_node)
workflow.add_node("generate_response", response_generation_node)

workflow.set_entry_point("discover_tools")
workflow.add_edge("discover_tools", "plan")
workflow.add_edge("plan", "execute_tools")
workflow.add_edge("execute_tools", "generate_response")
workflow.add_edge("generate_response", END)

app = workflow.compile()

# Example usage (async)
async def main():
    result = await app.ainvoke({
        "messages": [{"role": "user", "content": "Get the weather in New York"}],
        "mcp_tools": [],
        "tool_results": [],
        "response": ""
    })

    print("=== Agent Response ===")
    print(result["response"])

# Run
import asyncio
# asyncio.run(main())
```

### Example 2: Multi-MCP Server Integration

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List, Dict
import httpx

class MultiMCPState(TypedDict):
    query: str
    mcp_servers: Dict[str, str]  # name: url
    available_tools: Dict[str, List[dict]]  # server: tools
    execution_plan: List[dict]
    results: List[dict]
    final_response: str

# Multiple MCP servers
MCP_SERVERS = {
    "filesystem": "http://localhost:8001",
    "database": "http://localhost:8002",
    "api": "http://localhost:8003"
}

llm = ChatOpenAI(model="gpt-4")

async def discover_all_tools_node(state: MultiMCPState) -> MultiMCPState:
    """Discover tools from all MCP servers"""
    all_tools = {}

    async with httpx.AsyncClient() as client:
        for server_name, server_url in MCP_SERVERS.items():
            try:
                response = await client.get(f"{server_url}/tools")
                all_tools[server_name] = response.json()
            except:
                all_tools[server_name] = []

    return {
        "mcp_servers": MCP_SERVERS,
        "available_tools": all_tools
    }

def create_execution_plan_node(state: MultiMCPState) -> MultiMCPState:
    """Create plan using tools from multiple servers"""
    query = state["query"]
    available_tools = state["available_tools"]

    # Format tools for LLM
    tools_description = []
    for server, tools in available_tools.items():
        for tool in tools:
            tools_description.append(
                f"[{server}] {tool['name']}: {tool['description']}"
            )

    prompt = f"""Create an execution plan for: {query}

    Available tools:
    {chr(10).join(tools_description)}

    Respond with JSON:
    {{
        "steps": [
            {{
                "server": "server_name",
                "tool": "tool_name",
                "parameters": {{...}},
                "description": "what this does"
            }}
        ]
    }}
    """

    response = llm.invoke([{"role": "user", "content": prompt}])

    try:
        plan = json.loads(response.content)
        return {"execution_plan": plan.get("steps", [])}
    except:
        return {"execution_plan": []}

async def execute_plan_node(state: MultiMCPState) -> MultiMCPState:
    """Execute plan across multiple MCP servers"""
    execution_plan = state["execution_plan"]
    mcp_servers = state["mcp_servers"]
    results = []

    async with httpx.AsyncClient() as client:
        for step in execution_plan:
            server_name = step["server"]
            tool_name = step["tool"]
            parameters = step["parameters"]

            server_url = mcp_servers.get(server_name)
            if not server_url:
                continue

            try:
                response = await client.post(
                    f"{server_url}/call_tool",
                    json={
                        "name": tool_name,
                        "parameters": parameters
                    }
                )

                results.append({
                    "step": step["description"],
                    "server": server_name,
                    "tool": tool_name,
                    "result": response.json()
                })
            except Exception as e:
                results.append({
                    "step": step["description"],
                    "server": server_name,
                    "tool": tool_name,
                    "error": str(e)
                })

    return {"results": results}

def synthesize_response_node(state: MultiMCPState) -> MultiMCPState:
    """Synthesize results into final response"""
    query = state["query"]
    results = state["results"]

    results_text = "\n".join([
        f"{i+1}. {r['step']}\n   Server: {r['server']}\n   Result: {r.get('result', r.get('error'))}"
        for i, r in enumerate(results)
    ])

    prompt = f"""Synthesize these results into a response for: {query}

    Results:
    {results_text}

    Provide a comprehensive answer."""

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {"final_response": response.content}

# Build multi-MCP graph
workflow = StateGraph(MultiMCPState)

workflow.add_node("discover_tools", discover_all_tools_node)
workflow.add_node("create_plan", create_execution_plan_node)
workflow.add_node("execute_plan", execute_plan_node)
workflow.add_node("synthesize", synthesize_response_node)

workflow.set_entry_point("discover_tools")
workflow.add_edge("discover_tools", "create_plan")
workflow.add_edge("create_plan", "execute_plan")
workflow.add_edge("execute_plan", "synthesize")
workflow.add_edge("synthesize", END)

app = workflow.compile()

# Example usage
async def main():
    result = await app.ainvoke({
        "query": "Read config.json, update database with settings, and call the API",
        "mcp_servers": {},
        "available_tools": {},
        "execution_plan": [],
        "results": [],
        "final_response": ""
    })

    print("=== Execution Plan ===")
    for step in result["execution_plan"]:
        print(f"- {step['description']}")

    print("\n=== Final Response ===")
    print(result["final_response"])

# asyncio.run(main())
```

---

## A2A (Agent-to-Agent) Examples

### Example 1: Basic A2A Communication

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List, Dict
import httpx
import json

class A2AState(TypedDict):
    task: str
    messages: List[Dict]
    agents: Dict[str, str]  # agent_name: url
    current_agent: str
    result: str

# A2A Agent Registry
A2A_AGENTS = {
    "currency_agent": "http://localhost:9001",
    "weather_agent": "http://localhost:9002",
    "travel_agent": "http://localhost:9003"
}

llm = ChatOpenAI(model="gpt-4")

async def get_agent_card(agent_url: str) -> dict:
    """Get agent capabilities (AgentCard)"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{agent_url}/agent_card")
        return response.json()

async def send_message_to_agent(agent_url: str, message: dict) -> dict:
    """Send A2A message to agent"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{agent_url}/message",
            json=message
        )
        return response.json()

async def discover_agents_node(state: A2AState) -> A2AState:
    """Discover available A2A agents"""
    agents_info = {}

    for agent_name, agent_url in A2A_AGENTS.items():
        try:
            card = await get_agent_card(agent_url)
            agents_info[agent_name] = {
                "url": agent_url,
                "capabilities": card
            }
        except:
            pass

    return {"agents": agents_info}

def router_node(state: A2AState) -> A2AState:
    """Route task to appropriate agent"""
    task = state["task"]
    agents = state["agents"]

    # Format agent capabilities
    agents_desc = "\n".join([
        f"- {name}: {info['capabilities'].get('description', 'N/A')}"
        for name, info in agents.items()
    ])

    prompt = f"""Route this task to the best agent:

    Task: {task}

    Available agents:
    {agents_desc}

    Respond with just the agent name."""

    response = llm.invoke([{"role": "user", "content": prompt}])
    agent_name = response.content.strip().lower()

    # Validate agent exists
    if agent_name not in agents:
        agent_name = list(agents.keys())[0]  # Default to first

    return {"current_agent": agent_name}

async def communicate_node(state: A2AState) -> A2AState:
    """Communicate with selected agent via A2A protocol"""
    current_agent = state["current_agent"]
    task = state["task"]
    agents = state["agents"]

    agent_url = agents[current_agent]["url"]

    # Create A2A message
    a2a_message = {
        "message": {
            "role": "user",
            "content": task
        },
        "context": {
            "conversation_id": "conv-123",
            "request_id": "req-456"
        }
    }

    # Send message
    try:
        response = await send_message_to_agent(agent_url, a2a_message)

        messages = state.get("messages", [])
        messages.append({
            "from": "coordinator",
            "to": current_agent,
            "content": task
        })
        messages.append({
            "from": current_agent,
            "to": "coordinator",
            "content": response.get("content", "")
        })

        return {
            "messages": messages,
            "result": response.get("content", "")
        }
    except Exception as e:
        return {
            "result": f"Error communicating with {current_agent}: {str(e)}"
        }

# Build A2A graph
workflow = StateGraph(A2AState)

workflow.add_node("discover", discover_agents_node)
workflow.add_node("route", router_node)
workflow.add_node("communicate", communicate_node)

workflow.set_entry_point("discover")
workflow.add_edge("discover", "route")
workflow.add_edge("route", "communicate")
workflow.add_edge("communicate", END)

app = workflow.compile()

# Example usage
async def main():
    result = await app.ainvoke({
        "task": "Convert 100 USD to EUR",
        "messages": [],
        "agents": {},
        "current_agent": "",
        "result": ""
    })

    print("=== A2A Communication ===")
    for msg in result["messages"]:
        print(f"{msg['from']} -> {msg['to']}: {msg['content']}")

    print("\n=== Final Result ===")
    print(result["result"])

# asyncio.run(main())
```

### Example 2: Multi-Agent Travel Planner (A2A Pattern)

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List, Dict

class TravelPlannerState(TypedDict):
    request: str
    flight_info: dict
    hotel_info: dict
    weather_info: dict
    itinerary: str
    budget: dict

llm = ChatOpenAI(model="gpt-4")

# Simulated A2A agent responses
async def call_flight_agent(request: str) -> dict:
    """Call flight booking agent via A2A"""
    # Simulate A2A call
    return {
        "flights": [
            {"airline": "AA", "price": 450, "duration": "5h"},
            {"airline": "Delta", "price": 420, "duration": "5h 30m"}
        ],
        "recommendation": "Delta - best value"
    }

async def call_hotel_agent(location: str, dates: dict) -> dict:
    """Call hotel booking agent via A2A"""
    return {
        "hotels": [
            {"name": "Grand Hotel", "price": 200, "rating": 4.5},
            {"name": "City Inn", "price": 150, "rating": 4.0}
        ],
        "recommendation": "Grand Hotel - best rated"
    }

async def call_weather_agent(location: str, dates: dict) -> dict:
    """Call weather forecast agent via A2A"""
    return {
        "forecast": "Sunny, 75°F",
        "recommendation": "Pack light clothing"
    }

def request_parser_node(state: TravelPlannerState) -> TravelPlannerState:
    """Parse travel request"""
    request = state["request"]

    # Extract details (simplified)
    return state

async def flight_coordinator_node(state: TravelPlannerState) -> TravelPlannerState:
    """Coordinate with flight agent"""
    request = state["request"]
    flight_info = await call_flight_agent(request)

    return {"flight_info": flight_info}

async def hotel_coordinator_node(state: TravelPlannerState) -> TravelPlannerState:
    """Coordinate with hotel agent"""
    request = state["request"]
    hotel_info = await call_hotel_agent("Paris", {})

    return {"hotel_info": hotel_info}

async def weather_coordinator_node(state: TravelPlannerState) -> TravelPlannerState:
    """Coordinate with weather agent"""
    request = state["request"]
    weather_info = await call_weather_agent("Paris", {})

    return {"weather_info": weather_info}

def itinerary_builder_node(state: TravelPlannerState) -> TravelPlannerState:
    """Build complete itinerary"""
    flight_info = state["flight_info"]
    hotel_info = state["hotel_info"]
    weather_info = state["weather_info"]

    # Calculate budget
    flight_price = flight_info["flights"][0]["price"]
    hotel_price = hotel_info["hotels"][0]["price"]
    total_budget = flight_price + (hotel_price * 5)  # 5 nights

    itinerary = f"""# Travel Itinerary

## Flight
{flight_info["recommendation"]}
- Price: ${flight_price}

## Accommodation
{hotel_info["recommendation"]}
- Price: ${hotel_price}/night

## Weather
{weather_info["forecast"]}
{weather_info["recommendation"]}

## Total Budget
${total_budget}
"""

    return {
        "itinerary": itinerary,
        "budget": {"total": total_budget, "breakdown": {
            "flight": flight_price,
            "hotel": hotel_price * 5
        }}
    }

# Build travel planner graph
workflow = StateGraph(TravelPlannerState)

workflow.add_node("parse_request", request_parser_node)
workflow.add_node("get_flights", flight_coordinator_node)
workflow.add_node("get_hotels", hotel_coordinator_node)
workflow.add_node("get_weather", weather_coordinator_node)
workflow.add_node("build_itinerary", itinerary_builder_node)

workflow.set_entry_point("parse_request")

# Parallel coordination
workflow.add_edge("parse_request", "get_flights")
workflow.add_edge("parse_request", "get_hotels")
workflow.add_edge("parse_request", "get_weather")

# Wait for all, then build
workflow.add_edge("get_flights", "build_itinerary")
workflow.add_edge("get_hotels", "build_itinerary")
workflow.add_edge("get_weather", "build_itinerary")

workflow.add_edge("build_itinerary", END)

app = workflow.compile()

# Execute
async def main():
    result = await app.ainvoke({
        "request": "Plan a 5-day trip to Paris next month",
        "flight_info": {},
        "hotel_info": {},
        "weather_info": {},
        "itinerary": "",
        "budget": {}
    })

    print(result["itinerary"])
    print(f"\nTotal Budget: ${result['budget']['total']}")

# asyncio.run(main())
```

---

## Advanced Patterns

### 1. Human-in-the-Loop Pattern

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from typing import TypedDict

class HITLState(TypedDict):
    task: str
    agent_proposal: str
    human_feedback: str
    revised_output: str
    approved: bool

llm = ChatOpenAI(model="gpt-4")

def agent_proposal_node(state: HITLState) -> HITLState:
    """Agent creates initial proposal"""
    task = state["task"]

    response = llm.invoke([{
        "role": "user",
        "content": f"Create a solution for: {task}"
    }])

    return {"agent_proposal": response.content}

def human_review_node(state: HITLState) -> HITLState:
    """Human reviews and provides feedback"""
    proposal = state["agent_proposal"]

    # In real implementation, this would pause for human input
    print(f"\n=== Agent Proposal ===\n{proposal}\n")
    print("Please provide feedback (or 'approve' to accept):")

    # Simulated human feedback
    feedback = "approve"  # In real app, get from user input

    return {
        "human_feedback": feedback,
        "approved": feedback.lower() == "approve"
    }

def revision_node(state: HITLState) -> HITLState:
    """Agent revises based on feedback"""
    proposal = state["agent_proposal"]
    feedback = state["human_feedback"]

    response = llm.invoke([{
        "role": "user",
        "content": f"Revise this proposal based on feedback:\n\nProposal: {proposal}\n\nFeedback: {feedback}"
    }])

    return {"agent_proposal": response.content}

def should_continue(state: HITLState) -> str:
    """Check if approved"""
    if state.get("approved", False):
        return "finalize"
    return "revise"

def finalize_node(state: HITLState) -> HITLState:
    """Finalize approved output"""
    return {"revised_output": state["agent_proposal"]}

# Build HITL graph
workflow = StateGraph(HITLState)

workflow.add_node("propose", agent_proposal_node)
workflow.add_node("review", human_review_node)
workflow.add_node("revise", revision_node)
workflow.add_node("finalize", finalize_node)

workflow.set_entry_point("propose")
workflow.add_edge("propose", "review")
workflow.add_conditional_edges(
    "review",
    should_continue,
    {
        "revise": "revise",
        "finalize": "finalize"
    }
)
workflow.add_edge("revise", "review")
workflow.add_edge("finalize", END)

checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer, interrupt_before=["review"])

# Execute with interruption
config = {"configurable": {"thread_id": "hitl-1"}}

# Start execution (will interrupt at review)
result = app.invoke({
    "task": "Write a marketing email",
    "agent_proposal": "",
    "human_feedback": "",
    "revised_output": "",
    "approved": False
}, config=config)

print("Execution interrupted for human review")

# Get current state
current_state = app.get_state(config)
print(f"Current state: {current_state.values}")

# Continue after human input
result = app.invoke(None, config=config)  # Resume
```

### 2. Time Travel and Forking

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END

# Use previous simple chatbot example
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "time-travel-demo"}}

# Execute multiple turns
app.invoke({"messages": [("user", "Hello")]}, config=config)
app.invoke({"messages": [("user", "Tell me about AI")]}, config=config)
app.invoke({"messages": [("user", "What about ML?")]}, config=config)

# Get history
history = list(app.get_state_history(config))

print("=== State History ===")
for i, state in enumerate(history):
    print(f"{i}. Config: {state.config}")
    print(f"   Messages: {len(state.values.get('messages', []))}")

# Time travel: Get state from step 1
past_config = history[1].config
print(f"\n=== Rewinding to: {past_config} ===")

# Fork from that point
fork_config = {
    "configurable": {
        **past_config["configurable"],
        "thread_id": "forked-conversation"
    }
}

# Continue from forked point with different input
result = app.invoke({"messages": [("user", "Actually, tell me about robotics")]}, config=fork_config)
print(f"Forked result: {result}")
```

### 3. Dynamic Graph Modification

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Callable

class DynamicState(TypedDict):
    task_type: str
    data: dict
    result: str

def build_dynamic_graph(task_type: str) -> StateGraph:
    """Build graph based on task type"""

    workflow = StateGraph(DynamicState)

    if task_type == "analysis":
        workflow.add_node("load_data", load_data_node)
        workflow.add_node("analyze", analyze_node)
        workflow.add_node("visualize", visualize_node)

        workflow.set_entry_point("load_data")
        workflow.add_edge("load_data", "analyze")
        workflow.add_edge("analyze", "visualize")
        workflow.add_edge("visualize", END)

    elif task_type == "generation":
        workflow.add_node("research", research_node)
        workflow.add_node("draft", draft_node)
        workflow.add_node("refine", refine_node)

        workflow.set_entry_point("research")
        workflow.add_edge("research", "draft")
        workflow.add_edge("draft", "refine")
        workflow.add_edge("refine", END)

    return workflow

# Define nodes (simplified)
def load_data_node(state): return {"data": {"loaded": True}}
def analyze_node(state): return {"result": "analysis complete"}
def visualize_node(state): return {"result": "visualization created"}
def research_node(state): return {"data": {"researched": True}}
def draft_node(state): return {"result": "draft created"}
def refine_node(state): return {"result": "content refined"}

# Use dynamic graph
task_type = "analysis"
workflow = build_dynamic_graph(task_type)
app = workflow.compile()

result = app.invoke({
    "task_type": task_type,
    "data": {},
    "result": ""
})

print(f"Result: {result['result']}")
```

---

## Production Considerations

### 1. Error Handling and Resilience

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResilientState(TypedDict):
    data: dict
    errors: list
    retry_count: int
    success: bool

def resilient_node(state: ResilientState) -> ResilientState:
    """Node with error handling"""
    try:
        # Risky operation
        result = perform_operation()

        return {
            "data": result,
            "success": True
        }

    except Exception as e:
        logger.error(f"Node failed: {str(e)}")

        errors = state.get("errors", [])
        errors.append(str(e))
        retry_count = state.get("retry_count", 0)

        return {
            "errors": errors,
            "retry_count": retry_count + 1,
            "success": False
        }

def perform_operation():
    # Simulated operation
    return {"processed": True}

def should_retry(state: ResilientState) -> str:
    """Retry logic"""
    if state.get("success", False):
        return "success"

    if state.get("retry_count", 0) >= 3:
        return "failed"

    return "retry"

# Build resilient graph
workflow = StateGraph(ResilientState)
workflow.add_node("process", resilient_node)

workflow.set_entry_point("process")
workflow.add_conditional_edges(
    "process",
    should_retry,
    {
        "retry": "process",
        "success": END,
        "failed": END
    }
)

app = workflow.compile()
```

### 2. Monitoring and Observability

```python
from langgraph.graph import StateGraph, END
from langsmith import Client, traceable
import time

# LangSmith integration
client = Client()

@traceable(run_type="chain", name="monitored_agent")
def monitored_node(state: dict) -> dict:
    """Node with monitoring"""
    start_time = time.time()

    try:
        # Operation
        result = {"processed": True}

        duration = time.time() - start_time

        # Log metrics
        logger.info(f"Node completed in {duration:.2f}s")

        return result

    except Exception as e:
        logger.error(f"Node failed: {str(e)}")
        raise

# Use with LangSmith tracing enabled
workflow = StateGraph(dict)
workflow.add_node("monitored", monitored_node)
workflow.set_entry_point("monitored")
workflow.add_edge("monitored", END)

app = workflow.compile()
```

### 3. Deployment Patterns

```python
from fastapi import FastAPI, HTTPException
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import BaseModel
import uvicorn

app_api = FastAPI()

# Build LangGraph application
checkpointer = SqliteSaver.from_conn_string("prod_checkpoints.db")
graph_app = workflow.compile(checkpointer=checkpointer)

class AgentRequest(BaseModel):
    message: str
    thread_id: str

class AgentResponse(BaseModel):
    response: str
    thread_id: str

@app_api.post("/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """API endpoint for agent"""
    try:
        config = {"configurable": {"thread_id": request.thread_id}}

        result = graph_app.invoke({
            "messages": [request.message]
        }, config=config)

        return AgentResponse(
            response=result["messages"][-1].content,
            thread_id=request.thread_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app_api.get("/health")
async def health():
    return {"status": "healthy"}

# Run server
if __name__ == "__main__":
    uvicorn.run(app_api, host="0.0.0.0", port=8000)
```

---

## Conclusion

This comprehensive guide covers LangGraph from basic concepts to advanced production patterns. Key takeaways:

1. **Graph-Based Architecture**: LangGraph's graph structure enables complex agent workflows
2. **State Management**: Robust state handling with checkpointing and persistence
3. **Multi-Agent Systems**: Native support for agent collaboration
4. **Production Ready**: Built-in features for monitoring, error handling, and deployment
5. **Integration**: Seamless integration with MCP servers, A2A protocol, and external services

For more information:
- Official Documentation: https://langchain-ai.github.io/langgraph/
- GitHub: https://github.com/langchain-ai/langgraph
- LangSmith: https://smith.langchain.com/

---

**Document Version**: 1.0
**Last Updated**: 2024
**Total Lines**: 2400+
