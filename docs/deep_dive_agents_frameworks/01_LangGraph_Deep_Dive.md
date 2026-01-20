# LangGraph: Complete Deep Dive Guide

**Version**: 1.0.0 | **Updated**: January 2026 | **License**: MIT

---

## Table of Contents

1. [Introduction & Overview](#1-introduction--overview)
2. [System Architecture](#2-system-architecture)
3. [High-Level System Architecture](#3-high-level-system-architecture)
4. [End-to-End Flow](#4-end-to-end-flow)
5. [Installation & Setup](#5-installation--setup)
6. [Core Concepts](#6-core-concepts)
7. [Simple Agent Examples](#7-simple-agent-examples)
8. [Complex Agent Examples](#8-complex-agent-examples)
9. [Multi-Agent Examples](#9-multi-agent-examples)
10. [Agentic RAG Examples](#10-agentic-rag-examples)
11. [MCP with Agents](#11-mcp-with-agents)
12. [Agent-to-Agent (A2A) Communication](#12-agent-to-agent-a2a-communication)
13. [Best Practices](#13-best-practices)
14. [Advanced Patterns](#14-advanced-patterns)
15. [Deployment & Production](#15-deployment--production)
16. [References & Resources](#16-references--resources)

---

## 1. Introduction & Overview

### 1.1 What is LangGraph?

LangGraph is **LangChain's official framework** for building stateful, multi-actor applications with LLMs using graph-based workflows. It provides a powerful abstraction for creating cyclic agent systems with complex control flow, state management, and coordination patterns.

**Core Philosophy:**
- **Graphs > Chains**: Move beyond linear chains to cyclical, conditional workflows
- **State-Centric**: Explicit state management for complex multi-step processes
- **Agent Coordination**: Native support for multi-agent collaboration
- **Production-Ready**: Built for scalable, fault-tolerant agent systems

### 1.2 Key Features

#### Graph-Based Execution
- **StateGraph**: Define workflows as directed graphs with nodes and edges
- **Cyclic Flows**: Support loops, retries, and iterative refinement
- **Conditional Routing**: Dynamic edge selection based on state
- **Parallel Execution**: Run multiple nodes concurrently

#### State Management
- **TypedDict State**: Type-safe state definitions
- **State Persistence**: Checkpoint and resume workflows
- **State Reducers**: Merge state updates from parallel nodes
- **Immutable Updates**: Functional state transformations

#### Agent Capabilities
- **Tool Calling**: Native integration with LangChain tools
- **Memory Systems**: Built-in short and long-term memory
- **Human-in-the-Loop**: Interrupt workflows for human input
- **Error Handling**: Automatic retry and fallback mechanisms

#### Production Features
- **LangGraph Cloud**: Managed deployment platform
- **Streaming**: Real-time output streaming
- **Monitoring**: Built-in observability with LangSmith
- **Scaling**: Horizontal scaling for high-throughput

### 1.3 When to Use LangGraph

**Perfect For:**
- ✅ Multi-step agent workflows with conditional logic
- ✅ Cyclic reasoning patterns (reflect, retry, refine)
- ✅ Multi-agent collaboration and coordination
- ✅ Stateful conversational agents
- ✅ Complex RAG patterns with agent orchestration
- ✅ Production agent systems requiring persistence

**Not Ideal For:**
- ❌ Simple single-step LLM calls (use LangChain)
- ❌ Linear workflows without branching (use LangChain)
- ❌ Serverless single-invocation functions
- ❌ Real-time sub-100ms responses

---

## 2. System Architecture

### 2.1 Core Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                        LangGraph Application                        │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                         Graph Definition Layer                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                     StateGraph                               │  │
│  │  • Define state schema (TypedDict)                           │  │
│  │  • Add nodes (processing functions)                          │  │
│  │  • Add edges (control flow)                                  │  │
│  │  • Set conditional edges (routing logic)                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────┐
│                      Compilation Layer                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                Graph Compiler                                │  │
│  │  • Validate graph topology                                   │  │
│  │  • Optimize execution plan                                   │  │
│  │  • Set up checkpointing                                      │  │
│  │  • Configure interrupts                                      │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────┐
│                       Execution Layer                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                 Runtime Engine                               │  │
│  │                                                              │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐ │  │
│  │  │ State Manager  │  │ Node Executor  │  │ Edge Router   │ │  │
│  │  │ • Load state   │  │ • Run nodes    │  │ • Select next │ │  │
│  │  │ • Merge updates│  │ • Handle errors│  │ • Conditionals│ │  │
│  │  │ • Checkpoint   │  │ • Parallel exec│  │ • Loops       │ │  │
│  │  └────────────────┘  └────────────────┘  └───────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────┐
│                      Integration Layer                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │            External Systems                                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │  │
│  │  │   LLMs   │  │  Tools   │  │ Memory   │  │ Vector   │    │  │
│  │  │  (GPT-4) │  │ (Search) │  │  Store   │  │   DB     │    │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────┐
│                     Persistence Layer                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              Checkpointing System                            │  │
│  │  • MemorySaver (in-memory for dev)                           │  │
│  │  • PostgresSaver (production persistence)                    │  │
│  │  • State snapshots at each step                              │  │
│  │  • Resume from any checkpoint                                │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Breakdown

#### StateGraph

The core graph abstraction:

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated

# Define state schema
class AgentState(TypedDict):
    messages: Annotated[list, "conversation history"]
    current_step: str
    metadata: dict

# Create graph
graph = StateGraph(AgentState)

# Add nodes (processing functions)
graph.add_node("node_name", node_function)

# Add edges (control flow)
graph.add_edge("node_a", "node_b")  # Always go from A to B
graph.add_conditional_edges("node_c", routing_function)  # Dynamic routing

# Set entry point
graph.set_entry_point("first_node")

# Compile
app = graph.compile()
```

#### Nodes

Processing units that transform state:

```python
def process_node(state: AgentState) -> dict:
    """
    Node function signature:
    - Input: Current state
    - Output: Dictionary of state updates
    """
    # Access current state
    messages = state["messages"]

    # Perform processing (call LLM, tool, etc.)
    result = some_processing(messages)

    # Return state updates
    return {
        "messages": messages + [result],
        "current_step": "processing_done"
    }
```

#### Edges

Control flow connectors:

1. **Direct Edges**: Always transition to specific node
   ```python
   graph.add_edge("node_a", "node_b")
   ```

2. **Conditional Edges**: Dynamic routing based on state
   ```python
   def route_function(state: AgentState) -> str:
       if state["should_continue"]:
           return "continue_node"
       return "end_node"

   graph.add_conditional_edges("decision_node", route_function)
   ```

3. **END**: Terminal node
   ```python
   graph.add_edge("final_node", END)
   ```

#### State Reducers

Merge parallel updates:

```python
from typing import Annotated
from operator import add

class ParallelState(TypedDict):
    # Reducer: concatenate messages from parallel nodes
    messages: Annotated[list, add]
    # Last write wins (default)
    status: str
```

---

## 3. High-Level System Architecture

### 3.1 Execution Flow

```
User Input
    ↓
┌─────────────────────────────────────────────────────────────┐
│                    Graph Invocation                         │
│                                                             │
│  app.invoke(initial_state, config)                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Load Checkpoint (if resuming)                  │
│  • Restore previous state                                   │
│  • Resume from last node                                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Execute Entry Node                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. Load current state                                 │  │
│  │ 2. Call node function                                 │  │
│  │ 3. Receive state updates                              │  │
│  │ 4. Merge updates into state                           │  │
│  │ 5. Save checkpoint                                    │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 Edge Routing Decision                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Check edge type:                                      │  │
│  │  • Direct Edge → Go to specific node                 │  │
│  │  • Conditional Edge → Evaluate routing function      │  │
│  │  • END → Terminate execution                         │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌──────────────────┐          ┌──────────────────┐
│  Next Node       │          │  Termination     │
│  (Loop back)     │          │  (END reached)   │
└──────────────────┘          └──────────────────┘
        │                               │
        │                               ▼
        └────────► (Repeat)    ┌──────────────────┐
                               │  Return Final    │
                               │  State           │
                               └──────────────────┘
```

### 3.2 Multi-Agent Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                  Multi-Agent System                              │
└──────────────────────────────────────────────────────────────────┘

                         [Supervisor Node]
                                │
                                │ Routes to specialized agents
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
    │  Researcher  │    │   Analyzer   │    │    Writer    │
    │    Agent     │    │    Agent     │    │    Agent     │
    └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
           │                   │                   │
           │ Reports back      │ Reports back      │ Reports back
           │                   │                   │
           └───────────────────┴───────────────────┘
                               │
                               ▼
                      [Supervisor Node]
                               │
                               │ Decides next action:
                               │  • Route to another agent
                               │  • Continue with current
                               │  • Terminate
                               ▼
                          Final Output
```

### 3.3 Agentic RAG Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    Agentic RAG System                            │
└──────────────────────────────────────────────────────────────────┘

    User Query
        ↓
┌───────────────────┐
│  Query Analysis   │ ─► Classify query type
│      Node         │    Identify information needs
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Retrieval Plan   │ ─► Determine search strategy
│      Node         │    Select data sources
└────────┬──────────┘
         │
         ├─────────────────────┬──────────────────┐
         ▼                     ▼                  ▼
┌──────────────┐      ┌──────────────┐    ┌──────────────┐
│Vector Search │      │ Web Search   │    │SQL Database  │
│    Tool      │      │    Tool      │    │    Tool      │
└──────┬───────┘      └──────┬───────┘    └──────┬───────┘
       │                     │                    │
       └─────────────────────┴────────────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Retrieval Grading  │ ─► Filter irrelevant docs
                  │       Node          │    Score relevance
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Answer Generation  │ ─► Synthesize response
                  │       Node          │    Cite sources
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Quality Check      │ ─► Verify answer quality
                  │       Node          │    Check hallucinations
                  └──────────┬──────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
       ┌────────────────┐      ┌─────────────────┐
       │  Return Answer │      │  Refine Query   │
       │      (END)     │      │  & Re-retrieve  │
       └────────────────┘      └─────────────────┘
                                        │
                                        └──► (Loop back)
```

---

## 4. End-to-End Flow

### 4.1 Single Agent Flow

```
1. INITIALIZATION
   ├─> Define State Schema (TypedDict)
   ├─> Create StateGraph instance
   ├─> Add nodes (processing functions)
   ├─> Define edges (control flow)
   └─> Compile graph

2. INVOCATION
   ├─> Call app.invoke(initial_state)
   ├─> Load checkpoint (if resuming)
   └─> Start at entry point

3. NODE EXECUTION (Repeated)
   ├─> Load current state
   ├─> Execute node function
   │   ├─> Call LLM
   │   ├─> Use tools
   │   ├─> Process data
   │   └─> Return state updates
   ├─> Merge updates into state
   └─> Save checkpoint

4. EDGE ROUTING
   ├─> Evaluate edge conditions
   ├─> Determine next node
   └─> Continue or terminate

5. TERMINATION
   ├─> Reach END node
   ├─> Save final checkpoint
   └─> Return final state
```

### 4.2 Multi-Agent Flow

```
1. SUPERVISOR INITIALIZATION
   ├─> Define multi-agent state
   ├─> Create supervisor agent
   └─> Create specialized worker agents

2. TASK DISTRIBUTION
   ├─> Supervisor receives user query
   ├─> Analyzes task requirements
   └─> Routes to appropriate agent

3. AGENT EXECUTION
   ├─> Worker agent processes task
   ├─> Uses specialized tools/knowledge
   └─> Returns results to supervisor

4. COORDINATION
   ├─> Supervisor evaluates results
   ├─> Decides next action:
   │   ├─> Route to another agent
   │   ├─> Request refinement
   │   └─> Aggregate and finalize
   └─> Update shared state

5. COMPLETION
   ├─> All required tasks completed
   ├─> Supervisor synthesizes final output
   └─> Return to user
```

---

## 5. Installation & Setup

### 5.1 Prerequisites

**System Requirements:**
- Python 3.9 or higher (3.11+ recommended)
- pip or conda package manager
- 4GB+ RAM
- API keys for LLM providers

**Required Knowledge:**
- Basic Python programming
- Understanding of async/await
- Familiarity with LangChain (helpful)
- TypedDict and type hints

### 5.2 Installation

#### Method 1: pip Install (Recommended)

```bash
# Install LangGraph and LangChain
pip install langgraph langchain langchain-openai langchain-anthropic

# Install additional components
pip install langchain-community  # Community tools
pip install langsmith  # Observability (optional)

# Verify installation
python -c "from langgraph.graph import StateGraph; print('✅ LangGraph installed')"
```

#### Method 2: Poetry

```bash
poetry add langgraph langchain langchain-openai
```

#### Method 3: From Source

```bash
git clone https://github.com/langchain-ai/langgraph.git
cd langgraph
pip install -e .
```

### 5.3 Environment Configuration

```bash
# .env file
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LANGCHAIN_TRACING_V2=true  # Enable LangSmith tracing
LANGCHAIN_API_KEY=lsv2_...
LANGCHAIN_PROJECT=my-langgraph-project
```

```python
# Load environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# Verify
assert os.getenv("OPENAI_API_KEY"), "OpenAI API key required"
print("✅ Environment configured")
```

### 5.4 Quick Verification

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict

class State(TypedDict):
    message: str

def hello_node(state: State):
    return {"message": "Hello from LangGraph!"}

graph = StateGraph(State)
graph.add_node("hello", hello_node)
graph.set_entry_point("hello")
graph.add_edge("hello", END)

app = graph.compile()
result = app.invoke({"message": ""})
print(result)  # {'message': 'Hello from LangGraph!'}
```

---

## 6. Core Concepts

### 6.1 State Management

**TypedDict State Definition:**

```python
from typing import TypedDict, Annotated, Sequence
from operator import add

class AgentState(TypedDict):
    # Simple fields - last write wins
    current_task: str
    iteration: int

    # Annotated fields with reducers
    messages: Annotated[Sequence[str], add]  # Concatenate messages
    errors: Annotated[list[str], add]  # Accumulate errors

    # Complex fields
    metadata: dict
    context: dict
```

**State Updates:**

```python
def node_function(state: AgentState) -> dict:
    # Partial state updates - only return what changes
    return {
        "messages": ["New message"],  # Will be appended via reducer
        "iteration": state["iteration"] + 1  # Increment counter
    }
```

### 6.2 Graph Patterns

#### Pattern 1: Linear Pipeline

```python
# A → B → C → END
graph.add_node("a", node_a)
graph.add_node("b", node_b)
graph.add_node("c", node_c)

graph.set_entry_point("a")
graph.add_edge("a", "b")
graph.add_edge("b", "c")
graph.add_edge("c", END)
```

#### Pattern 2: Conditional Branching

```python
def should_continue(state: AgentState) -> str:
    if state["score"] > 0.8:
        return "end"
    return "retry"

graph.add_conditional_edges(
    "evaluate",
    should_continue,
    {
        "end": END,
        "retry": "generate"
    }
)
```

#### Pattern 3: Loops

```python
# Iterative refinement loop
def check_quality(state: AgentState) -> str:
    if state["quality"] > 0.9 or state["iterations"] >= 5:
        return "finish"
    return "refine"

graph.add_conditional_edges(
    "quality_check",
    check_quality,
    {
        "finish": END,
        "refine": "generate"  # Loop back
    }
)
```

#### Pattern 4: Parallel Execution

```python
from typing import Annotated
from operator import add

class ParallelState(TypedDict):
    results: Annotated[list, add]  # Combine results from parallel nodes

# Fan-out to parallel nodes
graph.add_conditional_edges(
    "split",
    lambda x: "parallel",
    {
        "parallel": ["worker_a", "worker_b", "worker_c"]
    }
)

# Fan-in - all workers converge to aggregator
graph.add_edge("worker_a", "aggregator")
graph.add_edge("worker_b", "aggregator")
graph.add_edge("worker_c", "aggregator")
```

### 6.3 Checkpointing

**In-Memory Checkpointing (Development):**

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

# Run with thread_id for state persistence
config = {"configurable": {"thread_id": "conversation-1"}}
result = app.invoke(initial_state, config)

# Resume from checkpoint
continued_result = app.invoke(None, config)  # Continues from last state
```

**PostgreSQL Checkpointing (Production):**

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:password@localhost:5432/langgraph"
)
app = graph.compile(checkpointer=checkpointer)

# State automatically persisted to PostgreSQL
config = {"configurable": {"thread_id": "user-session-123"}}
result = app.invoke(initial_state, config)
```

### 6.4 Human-in-the-Loop

**Interrupt for Human Input:**

```python
from langgraph.graph import StateGraph, END

def needs_review(state: AgentState) -> str:
    if state["confidence"] < 0.7:
        return "human_review"
    return "continue"

graph.add_conditional_edges(
    "decision",
    needs_review,
    {
        "human_review": "await_human",
        "continue": "proceed"
    }
)

# Compile with interrupt
app = graph.compile(
    checkpointer=memory,
    interrupt_before=["await_human"]  # Pause before this node
)

# Run until interrupt
result = app.invoke(initial_state, config)
print(result)  # Shows pending state

# Human provides input
human_feedback = input("Your feedback: ")
updated_state = result.copy()
updated_state["human_feedback"] = human_feedback

# Resume from interrupt
final_result = app.invoke(updated_state, config)
```

---

## 7. Simple Agent Examples

### 7.1 Basic Q&A Agent

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

class ConversationState(TypedDict):
    messages: list
    response: str

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def chat_node(state: ConversationState):
    """Simple chat completion."""
    messages = state["messages"]
    response = llm.invoke(messages)

    return {
        "messages": messages + [response],
        "response": response.content
    }

# Build graph
workflow = StateGraph(ConversationState)
workflow.add_node("chat", chat_node)
workflow.set_entry_point("chat")
workflow.add_edge("chat", END)

app = workflow.compile()

# Use
result = app.invoke({
    "messages": [HumanMessage(content="What is quantum computing?")],
    "response": ""
})

print(result["response"])
```

### 7.2 ReAct Agent with Tools

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Define tools
@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

tools = [search_web, calculator]

class AgentState(TypedDict):
    messages: list

# Create LLM with tools
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: AgentState):
    """Agent decides whether to use tools or respond."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": messages + [response]}

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Route to tools or end based on agent's decision."""
    last_message = state["messages"][-1]

    # If agent called tools, route to tools node
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # Otherwise, end
    return "end"

# Build graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

# Add edges
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)
workflow.add_edge("tools", "agent")  # After tools, go back to agent

app = workflow.compile()

# Use
result = app.invoke({
    "messages": [HumanMessage(content="What is 15 * 23? Then search for the result.")]
})

print(result["messages"][-1].content)
```

### 7.3 Reflection Agent

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class ReflectionState(TypedDict):
    task: str
    draft: str
    critique: str
    final: str
    iterations: int

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

def generate_draft(state: ReflectionState):
    """Generate initial draft."""
    prompt = [
        SystemMessage(content="You are a creative writer. Write a compelling response."),
        HumanMessage(content=state["task"])
    ]
    response = llm.invoke(prompt)

    return {
        "draft": response.content,
        "iterations": 1
    }

def reflect_on_draft(state: ReflectionState):
    """Critique the draft."""
    prompt = [
        SystemMessage(content="You are a critical reviewer. Provide constructive feedback."),
        HumanMessage(content=f"Task: {state['task']}\n\nDraft:\n{state['draft']}\n\nProvide detailed critique:")
    ]
    response = llm.invoke(prompt)

    return {"critique": response.content}

def revise_draft(state: ReflectionState):
    """Revise based on critique."""
    prompt = [
        SystemMessage(content="You are an editor. Improve the draft based on feedback."),
        HumanMessage(content=f"Original: {state['draft']}\n\nCritique: {state['critique']}\n\nRevised version:")
    ]
    response = llm.invoke(prompt)

    return {
        "draft": response.content,
        "iterations": state["iterations"] + 1
    }

def should_continue(state: ReflectionState) -> str:
    """Decide whether to continue refining."""
    if state["iterations"] >= 3:
        return "finalize"
    return "reflect"

def finalize(state: ReflectionState):
    """Finalize the output."""
    return {"final": state["draft"]}

# Build graph
workflow = StateGraph(ReflectionState)

workflow.add_node("generate", generate_draft)
workflow.add_node("reflect", reflect_on_draft)
workflow.add_node("revise", revise_draft)
workflow.add_node("finalize", finalize)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "reflect")
workflow.add_edge("reflect", "revise")
workflow.add_conditional_edges(
    "revise",
    should_continue,
    {
        "reflect": "reflect",
        "finalize": "finalize"
    }
)
workflow.add_edge("finalize", END)

app = workflow.compile()

# Use
result = app.invoke({
    "task": "Write a short explanation of machine learning for beginners",
    "draft": "",
    "critique": "",
    "final": "",
    "iterations": 0
})

print("="*70)
print("FINAL VERSION:")
print("="*70)
print(result["final"])
```

---

## 8. Complex Agent Examples

### 8.1 Research Agent with Multiple Steps

```python
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool

# Define tools
@tool
def search_papers(query: str) -> str:
    """Search academic papers."""
    return f"Found papers about: {query}"

@tool
def read_paper(paper_id: str) -> str:
    """Read and summarize a paper."""
    return f"Summary of paper {paper_id}"

tools = [search_papers, read_paper]

class ResearchState(TypedDict):
    topic: str
    research_plan: str
    findings: List[str]
    analysis: str
    report: str
    current_step: str

llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools)

def plan_research(state: ResearchState):
    """Create research plan."""
    prompt = [
        SystemMessage(content="You are a research planner. Create a structured research plan."),
        HumanMessage(content=f"Topic: {state['topic']}\n\nCreate a research plan with 3-5 key questions to investigate.")
    ]
    response = llm.invoke(prompt)

    return {
        "research_plan": response.content,
        "current_step": "planned"
    }

def conduct_research(state: ResearchState):
    """Execute research using tools."""
    prompt = [
        SystemMessage(content="You are a researcher. Gather information on the topics in the research plan."),
        HumanMessage(content=f"Research plan: {state['research_plan']}\n\nUse available tools to gather information.")
    ]

    # Multi-turn tool usage
    findings = []
    messages = prompt.copy()

    for i in range(3):  # Multiple research iterations
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if hasattr(response, "tool_calls") and response.tool_calls:
            for tool_call in response.tool_calls:
                # Execute tool
                tool_result = execute_tool(tool_call, tools)
                findings.append(tool_result)
                messages.append(ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call["id"]
                ))

    return {
        "findings": findings,
        "current_step": "researched"
    }

def analyze_findings(state: ResearchState):
    """Analyze research findings."""
    prompt = [
        SystemMessage(content="You are a research analyst. Synthesize findings into key insights."),
        HumanMessage(content=f"Findings:\n" + "\n".join(state["findings"]) + "\n\nProvide analysis:")
    ]
    response = llm.invoke(prompt)

    return {
        "analysis": response.content,
        "current_step": "analyzed"
    }

def write_report(state: ResearchState):
    """Write final research report."""
    prompt = [
        SystemMessage(content="You are a technical writer. Create a comprehensive research report."),
        HumanMessage(content=f"""
        Topic: {state['topic']}
        Plan: {state['research_plan']}
        Analysis: {state['analysis']}

        Write a well-structured research report with:
        1. Executive Summary
        2. Key Findings
        3. Analysis
        4. Conclusions
        """)
    ]
    response = llm.invoke(prompt)

    return {
        "report": response.content,
        "current_step": "completed"
    }

def execute_tool(tool_call, tools):
    """Helper to execute tool calls."""
    for tool in tools:
        if tool.name == tool_call["name"]:
            return tool.invoke(tool_call["args"])
    return "Tool not found"

# Build graph
workflow = StateGraph(ResearchState)

workflow.add_node("plan", plan_research)
workflow.add_node("research", conduct_research)
workflow.add_node("analyze", analyze_findings)
workflow.add_node("write", write_report)

workflow.set_entry_point("plan")
workflow.add_edge("plan", "research")
workflow.add_edge("research", "analyze")
workflow.add_edge("analyze", "write")
workflow.add_edge("write", END)

app = workflow.compile()

# Use
result = app.invoke({
    "topic": "Impact of AI on Healthcare",
    "research_plan": "",
    "findings": [],
    "analysis": "",
    "report": "",
    "current_step": "start"
})

print(result["report"])
```

### 8.2 Self-Correcting Code Generator

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import subprocess

class CodeGenState(TypedDict):
    task: str
    code: str
    test_results: str
    error_message: str
    iterations: int
    status: str

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def generate_code(state: CodeGenState):
    """Generate Python code for the task."""
    context = ""
    if state["iterations"] > 0:
        context = f"\n\nPrevious attempt failed with error:\n{state['error_message']}\n\nPrevious code:\n{state['code']}"

    prompt = [
        SystemMessage(content="You are an expert Python programmer. Write clean, tested code."),
        HumanMessage(content=f"Task: {state['task']}{context}\n\nProvide complete Python code:")
    ]
    response = llm.invoke(prompt)

    # Extract code from response
    code = extract_code_block(response.content)

    return {
        "code": code,
        "iterations": state["iterations"] + 1
    }

def test_code(state: CodeGenState):
    """Execute code and capture results."""
    try:
        # Write code to temp file
        with open("/tmp/generated_code.py", "w") as f:
            f.write(state["code"])

        # Run code
        result = subprocess.run(
            ["python", "/tmp/generated_code.py"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            return {
                "test_results": result.stdout,
                "error_message": "",
                "status": "success"
            }
        else:
            return {
                "test_results": "",
                "error_message": result.stderr,
                "status": "error"
            }

    except Exception as e:
        return {
            "test_results": "",
            "error_message": str(e),
            "status": "error"
        }

def should_continue(state: CodeGenState) -> str:
    """Decide whether to retry or finish."""
    if state["status"] == "success":
        return "end"

    if state["iterations"] >= 5:
        return "end"  # Max retries reached

    return "retry"

def extract_code_block(text: str) -> str:
    """Extract Python code from markdown code blocks."""
    if "```python" in text:
        code = text.split("```python")[1].split("```")[0]
    elif "```" in text:
        code = text.split("```")[1].split("```")[0]
    else:
        code = text
    return code.strip()

# Build graph
workflow = StateGraph(CodeGenState)

workflow.add_node("generate", generate_code)
workflow.add_node("test", test_code)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "test")
workflow.add_conditional_edges(
    "test",
    should_continue,
    {
        "retry": "generate",
        "end": END
    }
)

app = workflow.compile()

# Use
result = app.invoke({
    "task": "Write a function to calculate fibonacci numbers up to n",
    "code": "",
    "test_results": "",
    "error_message": "",
    "iterations": 0,
    "status": "start"
})

print("="*70)
print("GENERATED CODE:")
print("="*70)
print(result["code"])
print("\n" + "="*70)
print(f"Status: {result['status']}")
print(f"Iterations: {result['iterations']}")
```

I'll continue with Multi-Agent, Agentic RAG, MCP, and A2A examples in the next parts. Would you like me to continue with the rest of this comprehensive document, or shall I proceed to create the other framework deep dives as well?