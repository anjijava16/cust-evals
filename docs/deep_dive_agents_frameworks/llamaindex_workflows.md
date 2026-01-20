# LlamaIndex Workflows Deep Dive: Comprehensive Guide

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
14. [Conclusion](#conclusion)

---

## Introduction

LlamaIndex Workflows is an event-driven orchestration framework for building agentic applications. It provides a powerful, flexible way to coordinate complex multi-step processes with LLMs, tools, and data operations. Unlike traditional sequential pipelines, Workflows uses an event-based architecture that enables reactive, parallel, and conditional execution patterns.

### Key Features

- **Event-Driven Architecture**: Build reactive systems using events and handlers
- **Type-Safe Events**: Leverage Pydantic models for event validation
- **Async-First Design**: Native support for asynchronous execution
- **Flexible Orchestration**: Support for parallel, sequential, and conditional flows
- **Context Management**: Shared context accessible across all steps
- **Built-in Observability**: Integration with LlamaIndex's observability tools
- **Streaming Support**: Real-time streaming of intermediate results
- **Human-in-the-Loop**: Easy integration of human feedback and approval
- **RAG Integration**: Seamless integration with LlamaIndex's retrieval capabilities
- **Tool Calling**: Native support for function calling and tool execution

### Why Use Workflows?

Traditional agentic frameworks often rely on rigid control flow or complex state machines. LlamaIndex Workflows provides:

1. **Simplicity**: Define steps as simple async functions
2. **Flexibility**: Event-driven model adapts to changing requirements
3. **Composability**: Combine workflows into larger systems
4. **Observability**: Built-in tracking and debugging
5. **Production-Ready**: Designed for real-world applications

---

## System Architecture

### Architectural Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    LlamaIndex Workflows System                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Application Layer                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │ Workflow │  │   Step   │  │  Event   │  │  Context │  │  │
│  │  │Definition│  │ Functions│  │ Handlers │  │  Manager │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Event Processing Layer                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  Event   │  │  Event   │  │  Event   │  │  Step    │  │  │
│  │  │  Queue   │  │  Router  │  │ Validator│  │ Executor │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Execution Layer                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  Async   │  │ Parallel │  │Sequential│  │Conditional│ │  │
│  │  │Execution │  │ Executor │  │ Executor │  │  Router  │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Context & State Layer                   │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │ Workflow │  │  Global  │  │  Step    │  │ Memory   │  │  │
│  │  │ Context  │  │  State   │  │  State   │  │  Store   │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Integration Layer                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │   LLM    │  │  Vector  │  │   MCP    │  │   A2A    │  │  │
│  │  │   APIs   │  │  Stores  │  │ Servers  │  │ Protocol │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Observability Layer                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  Tracing │  │  Logging │  │ Metrics  │  │  Debug   │  │  │
│  │  │  System  │  │  Handler │  │Collector │  │   Mode   │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Core Architecture Principles

1. **Event-Driven**: All communication happens through typed events
2. **Step-Based**: Work is organized into discrete, reusable steps
3. **Context-Aware**: Shared context flows through all steps
4. **Async-Native**: Built on asyncio for efficient execution
5. **Type-Safe**: Pydantic validation ensures correctness

---

## High-Level System Architecture

### Workflow Execution Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                        Client Application                         │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Workflow Interface                           │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐     │
│  │  run()         │  │  stream()      │  │  run_step()    │     │
│  │  Execute full  │  │  Stream events │  │  Run single    │     │
│  │  workflow      │  │  in real-time  │  │  step          │     │
│  └────────────────┘  └────────────────┘  └────────────────┘     │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Workflow Runtime Engine                        │
│                                                                    │
│  ┌────────────────────────────────────────────────────────┐      │
│  │              Event Processing Pipeline                  │      │
│  │                                                          │      │
│  │  Input Event → [Queue] → [Router] → [Handler] → Output │      │
│  │                   ↓          ↓           ↓              │      │
│  │              [Validate]  [Select]   [Execute]          │      │
│  └────────────────────────────────────────────────────────┘      │
│                            │                                       │
│  ┌─────────────────────────┴───────────────────────┐             │
│  │                                                   │             │
│  ▼                                                   ▼             │
│  ┌────────────────┐                      ┌────────────────┐      │
│  │  Step Executor │                      │ Context Store  │      │
│  ├────────────────┤                      ├────────────────┤      │
│  │ - Async Steps  │◄────────────────────►│ - Global Data  │      │
│  │ - Parallel     │    Context Access    │ - Step Data    │      │
│  │ - Sequential   │                      │ - Memory       │      │
│  │ - Conditional  │                      │ - State        │      │
│  └────────────────┘                      └────────────────┘      │
│         │                                        │                │
└─────────┼────────────────────────────────────────┼────────────────┘
          │                                        │
          ▼                                        ▼
┌──────────────────────┐              ┌─────────────────────────┐
│   LlamaIndex Core    │              │   External Services     │
├──────────────────────┤              ├─────────────────────────┤
│ - LLM Engines        │              │ - Vector Databases      │
│ - Indices            │              │ - MCP Servers           │
│ - Query Engines      │              │ - API Services          │
│ - Tools/Functions    │              │ - Data Sources          │
│ - Retrievers         │              │ - A2A Endpoints         │
└──────────────────────┘              └─────────────────────────┘
          │                                        │
          └────────────┬───────────────────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │   Observability Stack   │
          ├─────────────────────────┤
          │ - Event Traces          │
          │ - Performance Metrics   │
          │ - Error Logging         │
          │ - Debug Inspector       │
          └─────────────────────────┘
```

### Component Interaction Details

1. **Input Processing**: Client initiates workflow with initial event
2. **Event Routing**: Events are queued and routed to appropriate handlers
3. **Step Execution**: Handlers execute async step functions
4. **Context Management**: Steps read/write to shared context
5. **Event Emission**: Steps emit new events to trigger subsequent steps
6. **Parallel Processing**: Multiple steps can execute concurrently
7. **Result Aggregation**: Final results collected and returned
8. **Streaming**: Intermediate events streamed to client in real-time

---

## Core Components Deep Dive

### 1. Workflows

The `Workflow` class is the foundation of the framework. It orchestrates event processing and step execution.

#### Basic Workflow Structure

```python
from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    step,
    Event,
    Context
)
from typing import Optional, List
import asyncio

class MyWorkflow(Workflow):
    """A basic workflow example"""

    @step
    async def start(self, ctx: Context, ev: StartEvent) -> ProcessEvent:
        """Initial step that processes input"""
        # Access input from StartEvent
        user_input = ev.input

        # Store in context
        await ctx.set("user_query", user_input)

        # Emit next event
        return ProcessEvent(data=user_input)

    @step
    async def process(self, ctx: Context, ev: ProcessEvent) -> StopEvent:
        """Processing step that returns final result"""
        # Get from context
        query = await ctx.get("user_query")

        # Process
        result = f"Processed: {ev.data}"

        # Return final event
        return StopEvent(result=result)

# Define custom event
class ProcessEvent(Event):
    data: str

# Execute workflow
async def main():
    workflow = MyWorkflow(timeout=60, verbose=True)
    result = await workflow.run(input="Hello World")
    print(result)

# Run
asyncio.run(main())
```

#### Workflow Configuration

```python
from llama_index.core.workflow import Workflow
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

class ConfiguredWorkflow(Workflow):
    def __init__(
        self,
        llm: Optional[OpenAI] = None,
        embed_model: Optional[OpenAIEmbedding] = None,
        timeout: float = 60.0,
        verbose: bool = False,
        **kwargs
    ):
        super().__init__(timeout=timeout, verbose=verbose, **kwargs)
        self.llm = llm or OpenAI(model="gpt-4")
        self.embed_model = embed_model or OpenAIEmbedding()

    @step
    async def generate(self, ctx: Context, ev: StartEvent) -> StopEvent:
        # Use configured LLM
        response = await self.llm.acomplete(ev.input)
        return StopEvent(result=str(response))

# Usage
workflow = ConfiguredWorkflow(
    llm=OpenAI(model="gpt-4-turbo", temperature=0.7),
    timeout=120,
    verbose=True
)
```

### 2. Events

Events are the communication mechanism between steps. They must inherit from the `Event` base class.

#### Event Definition

```python
from llama_index.core.workflow import Event
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# Simple event
class MessageEvent(Event):
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

# Complex event with validation
class DataProcessedEvent(Event):
    """Event emitted when data processing completes"""

    data: List[Dict[str, Any]]
    source: str
    processed_count: int = Field(ge=0)
    errors: Optional[List[str]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        frozen = False  # Allow modification

# Hierarchical events
class BaseAgentEvent(Event):
    agent_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

class AgentThinkingEvent(BaseAgentEvent):
    thought: str
    reasoning: str

class AgentActionEvent(BaseAgentEvent):
    action: str
    action_input: Dict[str, Any]

class AgentResponseEvent(BaseAgentEvent):
    response: str
    confidence: float = Field(ge=0.0, le=1.0)
```

#### Built-in Events

```python
from llama_index.core.workflow import StartEvent, StopEvent, Event

# StartEvent - initiates workflow
start_ev = StartEvent(input="User query here")

# StopEvent - terminates workflow
stop_ev = StopEvent(result={"answer": "42", "metadata": {}})

# Custom intermediate events
class QueryEvent(Event):
    query: str

class RetrievalEvent(Event):
    documents: List[str]
    query: str
```

### 3. Steps

Steps are async functions decorated with `@step` that handle events.

#### Step Basics

```python
from llama_index.core.workflow import step, Context, Event, StopEvent
from typing import Union

class MyWorkflow(Workflow):

    @step
    async def simple_step(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> StopEvent:
        """Simple step that processes and returns"""
        result = ev.input.upper()
        return StopEvent(result=result)

    @step
    async def multi_output_step(
        self,
        ctx: Context,
        ev: InputEvent
    ) -> Union[ProcessEvent, ErrorEvent]:
        """Step that can emit different event types"""
        try:
            data = process_data(ev.data)
            return ProcessEvent(data=data)
        except Exception as e:
            return ErrorEvent(error=str(e))

    @step
    async def conditional_step(
        self,
        ctx: Context,
        ev: ProcessEvent
    ) -> Union[ContinueEvent, StopEvent]:
        """Step with conditional logic"""
        if ev.data.get("complete"):
            return StopEvent(result=ev.data)
        else:
            return ContinueEvent(data=ev.data)
```

#### Step Patterns

```python
from llama_index.core.workflow import step
import asyncio

class AdvancedWorkflow(Workflow):

    @step
    async def parallel_operations(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> AggregateEvent:
        """Execute multiple operations in parallel"""
        # Run operations concurrently
        results = await asyncio.gather(
            self._fetch_data(ev.query),
            self._search_index(ev.query),
            self._call_api(ev.query)
        )

        # Combine results
        return AggregateEvent(
            data_result=results[0],
            search_result=results[1],
            api_result=results[2]
        )

    @step
    async def stateful_step(
        self,
        ctx: Context,
        ev: ProcessEvent
    ) -> Union[ContinueEvent, StopEvent]:
        """Step that maintains state across invocations"""
        # Get counter from context
        counter = await ctx.get("counter", default=0)
        counter += 1
        await ctx.set("counter", counter)

        # Store intermediate results
        results = await ctx.get("results", default=[])
        results.append(ev.data)
        await ctx.set("results", results)

        # Continue or stop based on state
        if counter >= 5:
            return StopEvent(result=results)
        else:
            return ContinueEvent(iteration=counter)

    @step
    async def error_handling_step(
        self,
        ctx: Context,
        ev: RiskyEvent
    ) -> Union[SuccessEvent, ErrorEvent]:
        """Step with comprehensive error handling"""
        try:
            # Attempt risky operation
            result = await self._risky_operation(ev.data)
            return SuccessEvent(result=result)
        except ValueError as e:
            # Handle specific error
            await ctx.set("last_error", str(e))
            return ErrorEvent(error=str(e), retryable=True)
        except Exception as e:
            # Handle unexpected error
            await ctx.set("fatal_error", str(e))
            return ErrorEvent(error=str(e), retryable=False)

    async def _fetch_data(self, query: str) -> dict:
        """Helper method for data fetching"""
        await asyncio.sleep(0.1)
        return {"data": query}

    async def _search_index(self, query: str) -> List[str]:
        """Helper method for index search"""
        await asyncio.sleep(0.1)
        return [f"doc_{i}" for i in range(3)]

    async def _call_api(self, query: str) -> str:
        """Helper method for API calls"""
        await asyncio.sleep(0.1)
        return f"API result for {query}"

    async def _risky_operation(self, data: dict) -> dict:
        """Simulated risky operation"""
        if not data:
            raise ValueError("Empty data")
        return {"processed": data}
```

### 4. Context

Context provides shared state across workflow steps.

#### Context Operations

```python
from llama_index.core.workflow import Context
from typing import Any, Optional, List, Dict

class ContextWorkflow(Workflow):

    @step
    async def demonstrate_context(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> StopEvent:
        """Demonstrate context operations"""

        # Set simple values
        await ctx.set("user_id", "user_123")
        await ctx.set("timestamp", datetime.now())

        # Set complex values
        await ctx.set("config", {
            "temperature": 0.7,
            "max_tokens": 1000
        })

        # Get values
        user_id = await ctx.get("user_id")
        config = await ctx.get("config")

        # Get with default
        retry_count = await ctx.get("retry_count", default=0)

        # Update existing value
        retry_count += 1
        await ctx.set("retry_count", retry_count)

        # Store lists
        results = await ctx.get("results", default=[])
        results.append("new result")
        await ctx.set("results", results)

        return StopEvent(result={"processed": True})

    @step
    async def context_patterns(
        self,
        ctx: Context,
        ev: ProcessEvent
    ) -> StopEvent:
        """Common context patterns"""

        # Accumulator pattern
        accumulated = await ctx.get("accumulated", default=[])
        accumulated.append(ev.data)
        await ctx.set("accumulated", accumulated)

        # Counter pattern
        count = await ctx.get("count", default=0)
        await ctx.set("count", count + 1)

        # Flag pattern
        is_complete = await ctx.get("is_complete", default=False)
        if len(accumulated) >= 10:
            await ctx.set("is_complete", True)

        # Cache pattern
        cache_key = f"cache_{ev.query}"
        cached = await ctx.get(cache_key)
        if cached is None:
            result = await self._expensive_operation(ev.query)
            await ctx.set(cache_key, result)
        else:
            result = cached

        return StopEvent(result=result)

    async def _expensive_operation(self, query: str) -> dict:
        """Simulated expensive operation"""
        await asyncio.sleep(1)
        return {"result": f"Processed {query}"}
```

#### Context Best Practices

```python
class BestPracticesWorkflow(Workflow):

    @step
    async def namespace_context(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> ProcessEvent:
        """Use namespacing to avoid collisions"""

        # Good: namespaced keys
        await ctx.set("agent_1:state", "thinking")
        await ctx.set("agent_2:state", "acting")
        await ctx.set("workflow:iteration", 1)

        # Bad: generic keys (can collide)
        # await ctx.set("state", "thinking")  # Which agent?
        # await ctx.set("iteration", 1)  # Which component?

        return ProcessEvent(data="processed")

    @step
    async def typed_context(
        self,
        ctx: Context,
        ev: ProcessEvent
    ) -> StopEvent:
        """Use type hints and validation"""

        # Define expected structure
        class WorkflowState(BaseModel):
            current_step: str
            iteration: int
            results: List[str]
            config: Dict[str, Any]

        # Get and validate
        state_dict = await ctx.get("state", default={
            "current_step": "init",
            "iteration": 0,
            "results": [],
            "config": {}
        })
        state = WorkflowState(**state_dict)

        # Modify
        state.current_step = "processing"
        state.iteration += 1
        state.results.append("new result")

        # Store back
        await ctx.set("state", state.dict())

        return StopEvent(result=state.dict())
```

---

## End-to-End Flow

### Complete Workflow Execution

Let's trace a complete workflow execution from start to finish.

```python
from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    Event,
    step,
    Context
)
from llama_index.llms.openai import OpenAI
from typing import List, Optional, Union
import asyncio

# Step 1: Define Events
class QueryEvent(Event):
    """User query to process"""
    query: str
    user_id: str

class RetrievalEvent(Event):
    """Documents retrieved from index"""
    query: str
    documents: List[str]
    scores: List[float]

class GenerationEvent(Event):
    """Generated response"""
    query: str
    context: str
    response: str

class ValidationEvent(Event):
    """Validated final response"""
    response: str
    is_valid: bool
    confidence: float

# Step 2: Define Workflow
class RAGWorkflow(Workflow):
    """Complete RAG workflow with all steps"""

    def __init__(self, llm: Optional[OpenAI] = None, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm or OpenAI(model="gpt-4")

    @step
    async def parse_query(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> QueryEvent:
        """
        Step 1: Parse and validate user query
        Flow: StartEvent -> QueryEvent
        """
        print("Step 1: Parsing query...")

        # Extract query from input
        query = ev.input

        # Store initial state
        await ctx.set("original_query", query)
        await ctx.set("start_time", datetime.now())

        # Emit query event
        return QueryEvent(
            query=query,
            user_id="user_123"
        )

    @step
    async def retrieve_documents(
        self,
        ctx: Context,
        ev: QueryEvent
    ) -> RetrievalEvent:
        """
        Step 2: Retrieve relevant documents
        Flow: QueryEvent -> RetrievalEvent
        """
        print(f"Step 2: Retrieving documents for: {ev.query}")

        # Simulate retrieval
        documents = [
            "Document 1: LlamaIndex is a data framework for LLM applications.",
            "Document 2: Workflows enable event-driven orchestration.",
            "Document 3: RAG combines retrieval with generation."
        ]
        scores = [0.95, 0.87, 0.82]

        # Store retrieval results
        await ctx.set("retrieved_docs", documents)
        await ctx.set("retrieval_scores", scores)

        return RetrievalEvent(
            query=ev.query,
            documents=documents,
            scores=scores
        )

    @step
    async def generate_response(
        self,
        ctx: Context,
        ev: RetrievalEvent
    ) -> GenerationEvent:
        """
        Step 3: Generate response using LLM
        Flow: RetrievalEvent -> GenerationEvent
        """
        print("Step 3: Generating response...")

        # Prepare context
        context = "\n\n".join(ev.documents)

        # Create prompt
        prompt = f"""Given the following context, answer the query.

Context:
{context}

Query: {ev.query}

Answer:"""

        # Generate response
        response = await self.llm.acomplete(prompt)
        response_text = str(response)

        # Store generation info
        await ctx.set("context_used", context)
        await ctx.set("raw_response", response_text)

        return GenerationEvent(
            query=ev.query,
            context=context,
            response=response_text
        )

    @step
    async def validate_response(
        self,
        ctx: Context,
        ev: GenerationEvent
    ) -> StopEvent:
        """
        Step 4: Validate and finalize response
        Flow: GenerationEvent -> StopEvent
        """
        print("Step 4: Validating response...")

        # Simple validation
        is_valid = len(ev.response) > 10 and ev.response.strip() != ""
        confidence = 0.9 if is_valid else 0.3

        # Get metadata from context
        original_query = await ctx.get("original_query")
        start_time = await ctx.get("start_time")
        duration = (datetime.now() - start_time).total_seconds()

        # Prepare final result
        result = {
            "query": original_query,
            "response": ev.response,
            "is_valid": is_valid,
            "confidence": confidence,
            "duration_seconds": duration,
            "documents_used": len(await ctx.get("retrieved_docs")),
            "metadata": {
                "retrieval_scores": await ctx.get("retrieval_scores"),
                "context_length": len(ev.context)
            }
        }

        return StopEvent(result=result)

# Step 3: Execute Workflow
async def main():
    """Execute the complete workflow"""

    # Create workflow instance
    workflow = RAGWorkflow(
        llm=OpenAI(model="gpt-4", temperature=0.7),
        timeout=120,
        verbose=True
    )

    # Run workflow
    print("Starting RAG workflow execution...\n")
    result = await workflow.run(
        input="What is LlamaIndex Workflows?"
    )

    print("\n=== Final Result ===")
    print(f"Query: {result['query']}")
    print(f"Response: {result['response']}")
    print(f"Valid: {result['is_valid']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Duration: {result['duration_seconds']:.2f}s")
    print(f"Documents Used: {result['documents_used']}")

    return result

# Run
if __name__ == "__main__":
    result = asyncio.run(main())
```

### Execution Trace

```
Starting RAG workflow execution...

Step 1: Parsing query...
  ├─ Input: "What is LlamaIndex Workflows?"
  ├─ Storing: original_query, start_time
  └─ Emit: QueryEvent(query="What is LlamaIndex Workflows?", user_id="user_123")

Step 2: Retrieving documents for: What is LlamaIndex Workflows?
  ├─ Retrieved: 3 documents
  ├─ Scores: [0.95, 0.87, 0.82]
  ├─ Storing: retrieved_docs, retrieval_scores
  └─ Emit: RetrievalEvent(query=..., documents=[...], scores=[...])

Step 3: Generating response...
  ├─ Context length: 156 chars
  ├─ LLM call: OpenAI GPT-4
  ├─ Storing: context_used, raw_response
  └─ Emit: GenerationEvent(query=..., context=..., response=...)

Step 4: Validating response...
  ├─ Validation: PASS
  ├─ Confidence: 0.9
  ├─ Duration: 2.34s
  └─ Emit: StopEvent(result={...})

=== Final Result ===
Query: What is LlamaIndex Workflows?
Response: LlamaIndex Workflows is an event-driven orchestration framework...
Valid: True
Confidence: 0.9
Duration: 2.34s
Documents Used: 3
```

---

## Simple Agent Examples

### Example 1: Basic Q&A Agent

```python
from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    Event,
    step,
    Context
)
from llama_index.llms.openai import OpenAI
from typing import Optional

class QuestionEvent(Event):
    """Question to answer"""
    question: str

class AnswerEvent(Event):
    """Generated answer"""
    question: str
    answer: str

class QAAgent(Workflow):
    """Simple question-answering agent"""

    def __init__(
        self,
        llm: Optional[OpenAI] = None,
        temperature: float = 0.7,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.llm = llm or OpenAI(
            model="gpt-4",
            temperature=temperature
        )

    @step
    async def process_question(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> QuestionEvent:
        """Process incoming question"""
        question = ev.input
        await ctx.set("question", question)
        return QuestionEvent(question=question)

    @step
    async def generate_answer(
        self,
        ctx: Context,
        ev: QuestionEvent
    ) -> AnswerEvent:
        """Generate answer using LLM"""
        prompt = f"Answer the following question concisely:\n\n{ev.question}"
        response = await self.llm.acomplete(prompt)

        return AnswerEvent(
            question=ev.question,
            answer=str(response)
        )

    @step
    async def format_response(
        self,
        ctx: Context,
        ev: AnswerEvent
    ) -> StopEvent:
        """Format final response"""
        result = {
            "question": ev.question,
            "answer": ev.answer,
            "model": self.llm.model
        }
        return StopEvent(result=result)

# Usage
async def example_qa():
    agent = QAAgent(temperature=0.5, verbose=True)
    result = await agent.run(input="What is the capital of France?")
    print(f"Q: {result['question']}")
    print(f"A: {result['answer']}")

# Run
import asyncio
asyncio.run(example_qa())
```

### Example 2: Task Decomposition Agent

```python
from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    Event,
    step,
    Context
)
from llama_index.llms.openai import OpenAI
from typing import List, Optional
import json

class TaskEvent(Event):
    """Complex task to decompose"""
    task: str

class SubtasksEvent(Event):
    """Decomposed subtasks"""
    original_task: str
    subtasks: List[str]

class ExecutionEvent(Event):
    """Subtask execution results"""
    subtasks: List[str]
    results: List[str]

class TaskDecompositionAgent(Workflow):
    """Agent that breaks down complex tasks"""

    def __init__(self, llm: Optional[OpenAI] = None, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm or OpenAI(model="gpt-4")

    @step
    async def receive_task(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> TaskEvent:
        """Receive and validate task"""
        task = ev.input
        await ctx.set("original_task", task)
        return TaskEvent(task=task)

    @step
    async def decompose_task(
        self,
        ctx: Context,
        ev: TaskEvent
    ) -> SubtasksEvent:
        """Decompose task into subtasks"""
        prompt = f"""Break down this complex task into 3-5 simple subtasks.
Return as JSON array of strings.

Task: {ev.task}

Subtasks (JSON array):"""

        response = await self.llm.acomplete(prompt)
        subtasks = json.loads(str(response))

        await ctx.set("subtasks", subtasks)

        return SubtasksEvent(
            original_task=ev.task,
            subtasks=subtasks
        )

    @step
    async def execute_subtasks(
        self,
        ctx: Context,
        ev: SubtasksEvent
    ) -> ExecutionEvent:
        """Execute each subtask"""
        results = []

        for subtask in ev.subtasks:
            prompt = f"Complete this subtask: {subtask}"
            response = await self.llm.acomplete(prompt)
            results.append(str(response))

        return ExecutionEvent(
            subtasks=ev.subtasks,
            results=results
        )

    @step
    async def aggregate_results(
        self,
        ctx: Context,
        ev: ExecutionEvent
    ) -> StopEvent:
        """Aggregate subtask results"""
        original_task = await ctx.get("original_task")

        # Format results
        formatted_results = []
        for subtask, result in zip(ev.subtasks, ev.results):
            formatted_results.append({
                "subtask": subtask,
                "result": result
            })

        return StopEvent(result={
            "original_task": original_task,
            "subtasks": formatted_results,
            "summary": f"Completed {len(ev.subtasks)} subtasks"
        })

# Usage
async def example_decomposition():
    agent = TaskDecompositionAgent(verbose=True)
    result = await agent.run(
        input="Plan a week-long trip to Japan"
    )

    print(f"Task: {result['original_task']}")
    print(f"\nSubtasks and Results:")
    for item in result['subtasks']:
        print(f"\n- {item['subtask']}")
        print(f"  Result: {item['result'][:100]}...")

asyncio.run(example_decomposition())
```

### Example 3: Conversational Agent with Memory

```python
from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    Event,
    step,
    Context
)
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from typing import Optional, List
from datetime import datetime

class MessageEvent(Event):
    """User message"""
    message: str
    timestamp: datetime

class ResponseEvent(Event):
    """Agent response"""
    message: str
    history_context: str

class ConversationalAgent(Workflow):
    """Agent with conversation memory"""

    def __init__(
        self,
        llm: Optional[OpenAI] = None,
        memory_size: int = 10,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.llm = llm or OpenAI(model="gpt-4")
        self.memory = ChatMemoryBuffer.from_defaults(
            token_limit=memory_size * 100
        )

    @step
    async def receive_message(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> MessageEvent:
        """Receive user message"""
        message = ev.input
        timestamp = datetime.now()

        # Store in context
        await ctx.set("current_message", message)
        await ctx.set("timestamp", timestamp)

        return MessageEvent(
            message=message,
            timestamp=timestamp
        )

    @step
    async def retrieve_history(
        self,
        ctx: Context,
        ev: MessageEvent
    ) -> ResponseEvent:
        """Retrieve conversation history and generate response"""
        # Get conversation history
        history = self.memory.get()

        # Build context from history
        history_text = "\n".join([
            f"{msg.role}: {msg.content}"
            for msg in history
        ])

        # Generate response with context
        prompt = f"""Previous conversation:
{history_text}

User: {ev.message}