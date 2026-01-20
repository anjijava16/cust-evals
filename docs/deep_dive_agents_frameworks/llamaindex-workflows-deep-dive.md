# LlamaIndex Workflows Deep Dive: Comprehensive Event-Driven Agent Guide

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

### What is LlamaIndex Workflows?

LlamaIndex Workflows is an event-driven orchestration framework for building sophisticated multi-step AI agent systems. Unlike traditional linear agent frameworks, Workflows provides a powerful abstraction for managing complex, branching agent workflows using events, steps, and shared context. It's part of the broader LlamaIndex ecosystem but focuses specifically on orchestration patterns rather than just RAG (Retrieval-Augmented Generation).

### Why LlamaIndex Workflows?

**Event-Driven Architecture**
- Build reactive, asynchronous agent systems
- Handle complex, non-linear workflows naturally
- Enable parallel execution of independent steps
- Create dynamic, adaptive agent behaviors

**Flexible Orchestration**
- Define custom events for inter-step communication
- Share state across workflow steps via Context
- Support both sequential and parallel execution patterns
- Enable conditional routing and branching logic

**Production-Ready**
- Native async/await support for scalability
- Built-in error handling and recovery
- Comprehensive logging and observability
- Integration with LlamaIndex RAG components

**Developer Experience**
- Intuitive @step decorator for defining workflow steps
- Type-safe event handling with Pydantic models
- Clear separation of concerns
- Extensive documentation and examples

### Key Capabilities

**Step-Based Workflow Definition**
- Decorator-based step creation (`@step`)
- Automatic event routing
- Type-checked event handling
- Conditional step execution

**Event System**
- Custom event types inheriting from `Event`
- Built-in `StartEvent` and `StopEvent`
- Event payloads for data transfer
- Event-driven step triggering

**Context Management**
- Shared context across all workflow steps
- Async get/set operations
- Type-safe context storage
- Persistent state during workflow execution

**Integration Capabilities**
- LlamaIndex query engines and retrievers
- External LLMs (OpenAI, Anthropic, etc.)
- Vector databases
- Custom tools and services

---

## System Architecture

### Architectural Overview

LlamaIndex Workflows follows an event-driven architecture where steps react to events and produce new events, creating a flow of execution through the workflow graph.

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Workflow 1  │  │ Workflow 2  │  │ Workflow N  │         │
│  │  (Custom)   │  │  (Custom)   │  │  (Custom)   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                    Workflow Engine Layer                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Workflow Runtime                           │   │
│  │  • Event Queue Management                            │   │
│  │  • Step Execution Orchestration                      │   │
│  │  • Context Lifecycle Management                      │   │
│  │  • Error Handling & Recovery                         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                      Event System Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Event     │  │   Event      │  │   Event      │     │
│  │    Queue     │  │   Router     │  │   Handler    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                        Step Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Step 1     │  │   Step 2     │  │   Step N     │     │
│  │  (Async)     │  │  (Async)     │  │  (Async)     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                    Integration Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     LLM      │  │    Vector    │  │   External   │     │
│  │  Providers   │  │      DB      │  │    Tools     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Component Descriptions

**Application Layer**
- **Workflows**: Custom workflow implementations inheriting from `Workflow`
- **Business Logic**: Domain-specific workflow orchestration
- **Configuration**: Workflow-specific parameters and settings

**Workflow Engine Layer**
- **Runtime**: Manages workflow lifecycle and execution
- **Event Queue**: Queues events for processing
- **Context Manager**: Handles shared state across steps
- **Error Handler**: Manages exceptions and recovery

**Event System Layer**
- **Event Queue**: FIFO queue for event processing
- **Event Router**: Routes events to appropriate step handlers
- **Event Handler**: Processes events and triggers steps
- **Type System**: Pydantic-based event validation

**Step Layer**
- **Step Functions**: Async functions decorated with `@step`
- **Event Listeners**: Steps listening for specific event types
- **Event Emitters**: Steps producing events
- **Business Logic**: Core processing within steps

**Integration Layer**
- **LLM Providers**: OpenAI, Anthropic, Google, etc.
- **Vector Databases**: Pinecone, Chroma, Weaviate, etc.
- **External Tools**: APIs, databases, file systems
- **LlamaIndex Components**: Query engines, retrievers, indices

### Execution Flow Architecture

```
StartEvent → Event Queue → Event Router → Matching Step(s)
                              ↓
                    Context (Shared State)
                              ↓
        Step Execution → Process Logic → Emit New Event(s)
                              ↓
        New Event(s) → Event Queue → ... (cycle continues)
                              ↓
                          StopEvent
```

**Detailed Execution Flow**:

1. **Initialization**: Workflow instance created with configuration
2. **Start Event**: User triggers workflow with `StartEvent`
3. **Event Queue**: Event added to processing queue
4. **Event Routing**: Router matches event type to step handlers
5. **Step Execution**: Matching step(s) execute asynchronously
6. **Context Access**: Step reads/writes shared context
7. **Event Emission**: Step emits one or more new events
8. **Queue Update**: New events added to queue
9. **Cycle Repeat**: Process continues until `StopEvent`
10. **Result Return**: Workflow returns final result

---

## High-Level System Architecture

### Workflow Execution Model

```
┌───────────────────────────────────────────────────────────┐
│                    User Application                        │
│  workflow = MyWorkflow()                                   │
│  result = await workflow.run(query="...")                  │
└───────────────┬───────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────┐
│                    Workflow Instance                       │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  • __init__(): Initialize resources (LLM, etc.)     │ │
│  │  • run(): Execute workflow                          │ │
│  │  • @step decorated methods                          │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────┬───────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────┐
│                   Event Processing                         │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Event Queue: [StartEvent, CustomEvent1, ...]       │ │
│  │               ↓                                      │ │
│  │  Event Router: Match event type → step handlers     │ │
│  │               ↓                                      │ │
│  │  Step Execution: await step_function(ctx, event)    │ │
│  │               ↓                                      │ │
│  │  Return: New Event(s) or StopEvent                  │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────┬───────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────┐
│                   Shared Context                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  context: Context                                    │ │
│  │  • await ctx.set("key", value)                      │ │
│  │  • value = await ctx.get("key")                     │ │
│  │  • Persistent across all steps                      │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

### Step Definition Pattern

```python
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Event, Context

class MyEvent(Event):
    """Custom event for workflow."""
    data: str
    metadata: Dict[str, Any] = {}

class MyWorkflow(Workflow):
    """Custom workflow implementation."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def process_start(self, ctx: Context, ev: StartEvent) -> MyEvent:
        """Step triggered by StartEvent."""
        query = ev.get("query")

        # Process with LLM
        response = await self.llm.achat([
            ChatMessage(role="user", content=query)
        ])

        # Save to context
        await ctx.set("processed_query", response.message.content)

        # Emit custom event
        return MyEvent(data=response.message.content)

    @step
    async def finalize(self, ctx: Context, ev: MyEvent) -> StopEvent:
        """Step triggered by MyEvent."""
        # Get from context
        processed = await ctx.get("processed_query")

        # Return final result
        return StopEvent(result={"output": processed})
```

### Event Flow Patterns

**1. Linear Flow**
```
StartEvent → Step1 → Event1 → Step2 → Event2 → Step3 → StopEvent
```

**2. Branching Flow**
```
                    ┌→ Step2a → Event2a ┐
StartEvent → Step1 →│                    ├→ Step4 → StopEvent
                    └→ Step2b → Event2b ┘
```

**3. Parallel Flow**
```
             ┌→ Step2 → Event2 ┐
StartEvent →│  Step3 → Event3  │→ Aggregator → StopEvent
             └→ Step4 → Event4 ┘
```

**4. Loop Flow**
```
StartEvent → Step1 → Event1 → Step2 → Event2 ─┐
                 ↑                             │
                 └─────────────────────────────┘
                          (conditional loop)
```

---

## Core Components Deep Dive

### 1. Workflow Base Class

The `Workflow` class is the foundation for all workflow implementations.

**Class Structure**:

```python
from llama_index.core.workflow import Workflow

class MyWorkflow(Workflow):
    """
    Custom workflow inheriting from Workflow base class.

    The Workflow base class provides:
    - Event queue management
    - Step registration and routing
    - Context lifecycle management
    - Async execution support
    """

    def __init__(self, **kwargs):
        """
        Initialize workflow with custom resources.

        Common initialization tasks:
        - Create LLM instances
        - Initialize vector stores
        - Setup external connections
        - Configure parameters
        """
        super().__init__(**kwargs)

        # Initialize resources
        self.llm = OpenAI(model="gpt-4o-mini")
        self.embedding_model = OpenAIEmbedding()

    # Define steps using @step decorator
    @step
    async def my_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Step implementation."""
        pass
```

**Key Methods**:

- `run(**kwargs)`: Execute workflow asynchronously
- `_dispatch_event(event)`: Internal event dispatching
- `_create_context()`: Initialize workflow context

**Usage**:

```python
# Create workflow instance
workflow = MyWorkflow()

# Execute workflow
result = await workflow.run(query="What is AI?")

# Access result
print(result)  # Output from StopEvent
```

### 2. Events

Events are Pydantic models that carry data between workflow steps.

**Built-in Events**:

```python
from llama_index.core.workflow import StartEvent, StopEvent

# StartEvent: Initiates workflow
start = StartEvent(query="User question", user_id="123")
# Access via ev.get("query")

# StopEvent: Terminates workflow
stop = StopEvent(result={"answer": "Response"})
# Final result returned from workflow.run()
```

**Custom Events**:

```python
from llama_index.core.workflow import Event
from typing import List, Dict, Any
from pydantic import Field

class ResearchEvent(Event):
    """Event carrying research results."""
    query: str
    findings: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    sources: List[Dict[str, str]] = []

class AnalysisEvent(Event):
    """Event carrying analysis results."""
    research_data: str
    insights: List[str]
    recommendations: List[str] = []

class ErrorEvent(Event):
    """Event for error handling."""
    error_type: str
    error_message: str
    original_event: Optional[Event] = None
```

**Event Best Practices**:

1. **Specific Event Types**: Create event types for specific purposes
2. **Type Hints**: Always use type hints for event fields
3. **Validation**: Use Pydantic validators for data validation
4. **Documentation**: Add docstrings to event classes
5. **Default Values**: Provide sensible defaults where appropriate

### 3. Steps

Steps are async functions decorated with `@step` that process events.

**Step Signature**:

```python
from llama_index.core.workflow import step, Context

@step
async def my_step(
    self,
    ctx: Context,
    ev: EventType  # The event that triggers this step
) -> OutputEventType:  # The event this step produces
    """
    Step implementation.

    Args:
        ctx: Shared context for state management
        ev: Input event triggering this step

    Returns:
        Output event(s) for next step(s)
    """
    # 1. Extract data from event
    data = ev.field_name

    # 2. Access shared context
    previous_result = await ctx.get("key", default=None)

    # 3. Perform processing
    result = process_data(data)

    # 4. Update context
    await ctx.set("new_key", result)

    # 5. Return new event
    return NextEvent(data=result)
```

**Multiple Event Handlers**:

```python
class MyWorkflow(Workflow):
    """Workflow with multiple steps handling different events."""

    @step
    async def handle_start(self, ctx: Context, ev: StartEvent) -> ResearchEvent:
        """Handle initial query."""
        return ResearchEvent(query=ev.get("query"), findings=[])

    @step
    async def handle_research(self, ctx: Context, ev: ResearchEvent) -> AnalysisEvent:
        """Handle research results."""
        return AnalysisEvent(research_data=str(ev.findings))

    @step
    async def handle_analysis(self, ctx: Context, ev: AnalysisEvent) -> StopEvent:
        """Handle analysis completion."""
        return StopEvent(result=ev.insights)
```

**Conditional Returns**:

```python
@step
async def conditional_step(
    self,
    ctx: Context,
    ev: InputEvent
) -> ResearchEvent | ErrorEvent:
    """Step with conditional event emission."""

    try:
        # Processing
        result = await process(ev.data)

        if result.is_valid:
            return ResearchEvent(findings=result.data)
        else:
            return ErrorEvent(
                error_type="validation",
                error_message="Invalid result"
            )

    except Exception as e:
        return ErrorEvent(
            error_type="exception",
            error_message=str(e),
            original_event=ev
        )
```

### 4. Context

The `Context` object provides shared state across all workflow steps.

**Context Operations**:

```python
from llama_index.core.workflow import Context

# In a step function
@step
async def my_step(self, ctx: Context, ev: Event) -> Event:
    """Step with context operations."""

    # Set value
    await ctx.set("user_data", {"name": "Alice", "role": "admin"})

    # Get value
    user_data = await ctx.get("user_data")

    # Get with default
    counter = await ctx.get("counter", default=0)

    # Update existing value
    counter += 1
    await ctx.set("counter", counter)

    # Store complex objects
    await ctx.set("results_list", [1, 2, 3])
    await ctx.set("config", {"temperature": 0.7, "max_tokens": 1000})

    return NextEvent()
```

**Context Patterns**:

```python
# Pattern 1: Accumulating Results
@step
async def accumulate(self, ctx: Context, ev: DataEvent) -> StopEvent:
    """Accumulate results from multiple steps."""
    results = await ctx.get("results", default=[])
    results.append(ev.data)
    await ctx.set("results", results)

    if len(results) >= 5:
        return StopEvent(result=results)
    else:
        return ProcessMoreEvent()

# Pattern 2: Configuration Sharing
@step
async def setup(self, ctx: Context, ev: StartEvent) -> ProcessEvent:
    """Setup shared configuration."""
    config = {
        "temperature": 0.7,
        "model": "gpt-4o-mini",
        "max_tokens": 2000
    }
    await ctx.set("config", config)
    return ProcessEvent()

@step
async def use_config(self, ctx: Context, ev: ProcessEvent) -> StopEvent:
    """Use shared configuration."""
    config = await ctx.get("config")
    # Use config settings
    response = await self.llm.achat(
        messages,
        temperature=config["temperature"]
    )
    return StopEvent(result=response.message.content)

# Pattern 3: State Machine
@step
async def state_transition(self, ctx: Context, ev: StateEvent) -> Event:
    """Implement state machine with context."""
    current_state = await ctx.get("state", default="initial")

    if current_state == "initial":
        await ctx.set("state", "processing")
        return ProcessEvent()
    elif current_state == "processing":
        await ctx.set("state", "complete")
        return StopEvent(result="Done")
```

### 5. Async/Await Pattern

LlamaIndex Workflows is built on async/await for concurrent execution.

**Async Best Practices**:

```python
import asyncio
from llama_index.llms.openai import OpenAI

class AsyncWorkflow(Workflow):
    """Workflow with async operations."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def parallel_processing(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> ResultEvent:
        """Execute multiple async operations in parallel."""

        # Define async tasks
        async def task1():
            return await self.llm.achat([
                ChatMessage(role="user", content="Task 1")
            ])

        async def task2():
            return await self.llm.achat([
                ChatMessage(role="user", content="Task 2")
            ])

        async def task3():
            return await self.llm.achat([
                ChatMessage(role="user", content="Task 3")
            ])

        # Execute in parallel
        results = await asyncio.gather(task1(), task2(), task3())

        # Process results
        combined = "\n".join([r.message.content for r in results])

        return ResultEvent(data=combined)

    @step
    async def sequential_processing(
        self,
        ctx: Context,
        ev: ResultEvent
    ) -> StopEvent:
        """Execute operations sequentially."""

        # Step 1
        result1 = await self.process_step1(ev.data)

        # Step 2 depends on step 1
        result2 = await self.process_step2(result1)

        # Step 3 depends on step 2
        final = await self.process_step3(result2)

        return StopEvent(result=final)

# Usage
async def main():
    workflow = AsyncWorkflow()
    result = await workflow.run(query="Process this")
    print(result)

# Run
asyncio.run(main())
```

---

## End-to-End Flow

### Complete Request Lifecycle

Let's trace a complete request through LlamaIndex Workflows with a multi-step research workflow.

**Scenario**: User asks "Research AI trends and create a summary report"

**Step 1: Workflow Setup**

```python
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Event, Context
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
import asyncio

# Define custom events
class ResearchEvent(Event):
    """Event with research results."""
    query: str
    research_data: str

class AnalysisEvent(Event):
    """Event with analysis results."""
    analysis: str
    key_points: List[str]

class ReportEvent(Event):
    """Event with final report."""
    report: str

# Define workflow
class ResearchWorkflow(Workflow):
    """Multi-step research workflow."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def research(self, ctx: Context, ev: StartEvent) -> ResearchEvent:
        """Step 1: Research the topic."""
        query = ev.get("query")

        # Simulate research
        messages = [
            ChatMessage(
                role="system",
                content="You are a research specialist."
            ),
            ChatMessage(
                role="user",
                content=f"Research: {query}"
            )
        ]

        response = await self.llm.achat(messages)

        # Save to context
        await ctx.set("original_query", query)
        await ctx.set("research_result", response.message.content)

        # Emit research event
        return ResearchEvent(
            query=query,
            research_data=response.message.content
        )

    @step
    async def analyze(self, ctx: Context, ev: ResearchEvent) -> AnalysisEvent:
        """Step 2: Analyze research data."""
        messages = [
            ChatMessage(
                role="system",
                content="You are an analyst."
            ),
            ChatMessage(
                role="user",
                content=f"Analyze this research:\\n\\n{ev.research_data}"
            )
        ]

        response = await self.llm.achat(messages)

        # Extract key points (simplified)
        key_points = response.message.content.split("\\n")[:5]

        # Save to context
        await ctx.set("analysis_result", response.message.content)

        return AnalysisEvent(
            analysis=response.message.content,
            key_points=key_points
        )

    @step
    async def create_report(self, ctx: Context, ev: AnalysisEvent) -> StopEvent:
        """Step 3: Create final report."""
        # Get previous results from context
        original_query = await ctx.get("original_query")
        research = await ctx.get("research_result")

        # Generate report
        messages = [
            ChatMessage(
                role="system",
                content="You are a report writer."
            ),
            ChatMessage(
                role="user",
                content=f"""Create a summary report:

Query: {original_query}

Research: {research}

Analysis: {ev.analysis}

Create a well-structured markdown report."""
            )
        ]

        response = await self.llm.achat(messages)

        # Return final result
        return StopEvent(result={
            "report": response.message.content,
            "key_points": ev.key_points
        })
```

**Step 2: Execution**

```python
async def run_research_workflow():
    """Execute the research workflow."""

    # Create workflow instance
    workflow = ResearchWorkflow()

    # Execute with query
    result = await workflow.run(
        query="Research AI trends and create a summary report"
    )

    # Access results
    print("FINAL REPORT")
    print("=" * 80)
    print(result["report"])
    print("\\nKEY POINTS")
    print("=" * 80)
    for point in result["key_points"]:
        print(f"- {point}")

# Run
asyncio.run(run_research_workflow())
```

**Step 3: Event Flow Trace**

```
1. User calls workflow.run(query="...")
   ↓
2. Workflow creates StartEvent(query="...")
   ↓
3. Event Router: StartEvent → research() step
   ↓
4. research() step executes:
   - Extracts query from StartEvent
   - Calls LLM for research
   - Saves to context
   - Returns ResearchEvent(research_data="...")
   ↓
5. Event Queue receives ResearchEvent
   ↓
6. Event Router: ResearchEvent → analyze() step
   ↓
7. analyze() step executes:
   - Processes research_data
   - Calls LLM for analysis
   - Saves to context
   - Returns AnalysisEvent(analysis="...", key_points=[...])
   ↓
8. Event Queue receives AnalysisEvent
   ↓
9. Event Router: AnalysisEvent → create_report() step
   ↓
10. create_report() step executes:
    - Retrieves previous results from context
    - Calls LLM to generate report
    - Returns StopEvent(result={...})
    ↓
11. Workflow receives StopEvent
    ↓
12. Workflow.run() returns result to user
```

**Step 4: Context State Timeline**

```
Time 0 (Initialization):
  Context = {}

Time 1 (After research step):
  Context = {
    "original_query": "Research AI trends...",
    "research_result": "AI trends include..."
  }

Time 2 (After analyze step):
  Context = {
    "original_query": "Research AI trends...",
    "research_result": "AI trends include...",
    "analysis_result": "Analysis shows..."
  }

Time 3 (After create_report step):
  Context = {
    "original_query": "Research AI trends...",
    "research_result": "AI trends include...",
    "analysis_result": "Analysis shows..."
  }
  (No changes, just reads from context)
```

**Step 5: Complete Execution Diagram**

```
User Application
    │
    ▼
workflow.run(query="...")
    │
    ▼
┌──────────────────────────────┐
│   Workflow Initialization     │
│  • Create Context             │
│  • Create Event Queue         │
│  • Register Steps             │
└────────────┬─────────────────┘
             │
             ▼
      StartEvent Created
             │
             ▼
┌──────────────────────────────┐
│    Event Queue Processin      │
│  Queue: [StartEvent]          │
└────────────┬─────────────────┘
             │
             ▼
      Event Router
             │
             ▼
┌──────────────────────────────┐
│  research() Step Execution    │
│  • Get query from StartEvent  │
│  • Call LLM                   │
│  • ctx.set("research_result") │
│  • Return ResearchEvent       │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────────┐
│    Event Queue Processing     │
│  Queue: [ResearchEvent]       │
└────────────┬─────────────────┘
             │
             ▼
      Event Router
             │
             ▼
┌──────────────────────────────┐
│  analyze() Step Execution     │
│  • Get data from ResearchEv.  │
│  • Call LLM                   │
│  • ctx.set("analysis_result") │
│  • Return AnalysisEvent       │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────────┐
│    Event Queue Processing     │
│  Queue: [AnalysisEvent]       │
└────────────┬─────────────────┘
             │
             ▼
      Event Router
             │
             ▼
┌──────────────────────────────┐
│ create_report() Step Exec.    │
│  • ctx.get("original_query")  │
│  • ctx.get("research_result") │
│  • Call LLM                   │
│  • Return StopEvent           │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────────┐
│   Workflow Completion         │
│  • Extract result from Stop   │
│  • Return to user             │
└───────────────────────────────┘
```

---

## Simple Agents

### 1. Basic Question-Answer Agent

The simplest workflow - single step processing.

```python
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Context
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage

class SimpleQAAgent(Workflow):
    """Simple question-answering agent."""

    def __init__(self, model: str = "gpt-4o-mini"):
        super().__init__()
        self.llm = OpenAI(model=model)

    @step
    async def answer(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Answer the question."""
        query = ev.get("query")

        messages = [
            ChatMessage(
                role="system",
                content="You are a helpful assistant."
            ),
            ChatMessage(
                role="user",
                content=query
            )
        ]

        response = await self.llm.achat(messages)

        return StopEvent(result=response.message.content)

# Usage
async def main():
    agent = SimpleQAAgent()
    result = await agent.run(query="What is machine learning?")
    print(result)

asyncio.run(main())
```

### 2. Stateful Conversation Agent

Agent that maintains conversation history.

```python
class ConversationAgent(Workflow):
    """Agent with conversation memory."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def process_message(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> StopEvent:
        """Process message with conversation history."""
        message = ev.get("message")

        # Get conversation history from context
        history = await ctx.get("history", default=[])

        # Add user message
        history.append(
            ChatMessage(role="user", content=message)
        )

        # Generate response
        response = await self.llm.achat(history)

        # Add assistant response to history
        history.append(response.message)

        # Update context
        await ctx.set("history", history)

        return StopEvent(result=response.message.content)

# Usage
async def conversation_example():
    agent = ConversationAgent()

    # Message 1
    result1 = await agent.run(message="Hi, my name is Alice")
    print(f"Agent: {result1}")

    # Message 2 - agent remembers context
    result2 = await agent.run(message="What's my name?")
    print(f"Agent: {result2}")
    # Output: "Your name is Alice"

asyncio.run(conversation_example())
```

### 3. Tool-Using Agent

Agent that uses external tools.

```python
class ToolEvent(Event):
    """Event indicating tool should be used."""
    tool_name: str
    tool_input: str

class ToolAgent(Workflow):
    """Agent with tool usage."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    def calculate(self, expression: str) -> str:
        """Calculator tool."""
        try:
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error: {str(e)}"

    def get_weather(self, location: str) -> str:
        """Weather tool (simulated)."""
        return f"Weather in {location}: Sunny, 72°F"

    @step
    async def decide_tool(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> ToolEvent | StopEvent:
        """Decide if tool is needed."""
        query = ev.get("query")

        # Simple rule-based tool selection
        if "calculate" in query.lower() or any(op in query for op in ["+", "-", "*", "/"]):
            # Extract expression
            import re
            match = re.search(r'[0-9+\-*/\s().]+', query)
            if match:
                return ToolEvent(
                    tool_name="calculate",
                    tool_input=match.group().strip()
                )

        if "weather" in query.lower():
            # Extract location
            words = query.split()
            if "in" in words:
                idx = words.index("in")
                if idx + 1 < len(words):
                    return ToolEvent(
                        tool_name="get_weather",
                        tool_input=words[idx + 1]
                    )

        # No tool needed, answer directly
        messages = [
            ChatMessage(role="user", content=query)
        ]
        response = await self.llm.achat(messages)
        return StopEvent(result=response.message.content)

    @step
    async def use_tool(
        self,
        ctx: Context,
        ev: ToolEvent
    ) -> StopEvent:
        """Execute tool and return result."""
        # Execute tool
        if ev.tool_name == "calculate":
            tool_result = self.calculate(ev.tool_input)
        elif ev.tool_name == "get_weather":
            tool_result = self.get_weather(ev.tool_input)
        else:
            tool_result = "Unknown tool"

        # Format response
        return StopEvent(result=f"Tool result: {tool_result}")

# Usage
async def tool_agent_example():
    agent = ToolAgent()

    queries = [
        "What is 25 * 4?",
        "What's the weather in Tokyo?",
        "What is artificial intelligence?"
    ]

    for query in queries:
        print(f"\\nQuery: {query}")
        result = await agent.run(query=query)
        print(f"Result: {result}")

asyncio.run(tool_agent_example())
```

---

## Complex Agents

### 1. Multi-Step Processing Agent

Agent with multiple processing stages.

```python
class ProcessingEvent(Event):
    """Event for data processing stage."""
    data: str
    stage: str

class ValidationEvent(Event):
    """Event for validation stage."""
    processed_data: str
    is_valid: bool

class ComplexProcessingAgent(Workflow):
    """Multi-stage processing agent."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def extract(self, ctx: Context, ev: StartEvent) -> ProcessingEvent:
        """Stage 1: Extract information."""
        raw_data = ev.get("data")

        messages = [
            ChatMessage(
                role="system",
                content="Extract key information from the following text."
            ),
            ChatMessage(role="user", content=raw_data)
        ]

        response = await self.llm.achat(messages)

        await ctx.set("extracted", response.message.content)

        return ProcessingEvent(
            data=response.message.content,
            stage="extraction"
        )

    @step
    async def transform(
        self,
        ctx: Context,
        ev: ProcessingEvent
    ) -> ValidationEvent:
        """Stage 2: Transform data."""
        if ev.stage != "extraction":
            # Only process extraction events
            return

        messages = [
            ChatMessage(
                role="system",
                content="Transform this data into structured format."
            ),
            ChatMessage(role="user", content=ev.data)
        ]

        response = await self.llm.achat(messages)

        await ctx.set("transformed", response.message.content)

        # Simple validation check
        is_valid = len(response.message.content) > 50

        return ValidationEvent(
            processed_data=response.message.content,
            is_valid=is_valid
        )

    @step
    async def finalize(
        self,
        ctx: Context,
        ev: ValidationEvent
    ) -> StopEvent:
        """Stage 3: Finalize results."""
        if not ev.is_valid:
            return StopEvent(result={
                "status": "error",
                "message": "Validation failed"
            })

        # Get all processing stages
        extracted = await ctx.get("extracted")
        transformed = await ctx.get("transformed")

        return StopEvent(result={
            "status": "success",
            "extracted": extracted,
            "transformed": transformed,
            "final": ev.processed_data
        })

# Usage
async def complex_agent_example():
    agent = ComplexProcessingAgent()
    result = await agent.run(
        data="AI is transforming healthcare through diagnostic tools and personalized medicine."
    )
    print(json.dumps(result, indent=2))

asyncio.run(complex_agent_example())
```

### 2. Decision-Making Agent

Agent with branching logic based on conditions.

```python
class AnalyzeEvent(Event):
    """Event for analysis."""
    content: str
    complexity: str  # "simple" or "complex"

class SimpleResponseEvent(Event):
    """Event for simple responses."""
    response: str

class ComplexResponseEvent(Event):
    """Event for complex responses."""
    detailed_response: str
    sub_topics: List[str]

class DecisionAgent(Workflow):
    """Agent with decision-making logic."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def analyze_complexity(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> AnalyzeEvent:
        """Analyze query complexity."""
        query = ev.get("query")

        # Determine complexity
        word_count = len(query.split())
        has_multiple_questions = "?" in query[:-1]  # Multiple question marks
        technical_terms = sum(1 for word in ["algorithm", "neural", "quantum", "blockchain"] if word in query.lower())

        if word_count > 20 or has_multiple_questions or technical_terms > 1:
            complexity = "complex"
        else:
            complexity = "simple"

        await ctx.set("original_query", query)
        await ctx.set("complexity", complexity)

        return AnalyzeEvent(content=query, complexity=complexity)

    @step
    async def handle_simple(
        self,
        ctx: Context,
        ev: AnalyzeEvent
    ) -> SimpleResponseEvent | None:
        """Handle simple queries."""
        if ev.complexity != "simple":
            return None

        messages = [
            ChatMessage(
                role="system",
                content="Provide a concise, clear answer."
            ),
            ChatMessage(role="user", content=ev.content)
        ]

        response = await self.llm.achat(messages)

        return SimpleResponseEvent(response=response.message.content)

    @step
    async def handle_complex(
        self,
        ctx: Context,
        ev: AnalyzeEvent
    ) -> ComplexResponseEvent | None:
        """Handle complex queries."""
        if ev.complexity != "complex":
            return None

        messages = [
            ChatMessage(
                role="system",
                content="Provide a detailed, structured answer with sub-topics."
            ),
            ChatMessage(role="user", content=ev.content)
        ]

        response = await self.llm.achat(messages)

        # Extract sub-topics (simplified)
        sub_topics = ["Topic 1", "Topic 2", "Topic 3"]

        return ComplexResponseEvent(
            detailed_response=response.message.content,
            sub_topics=sub_topics
        )

    @step
    async def finalize_simple(
        self,
        ctx: Context,
        ev: SimpleResponseEvent
    ) -> StopEvent:
        """Finalize simple response."""
        return StopEvent(result={
            "type": "simple",
            "response": ev.response
        })

    @step
    async def finalize_complex(
        self,
        ctx: Context,
        ev: ComplexResponseEvent
    ) -> StopEvent:
        """Finalize complex response."""
        return StopEvent(result={
            "type": "complex",
            "response": ev.detailed_response,
            "sub_topics": ev.sub_topics
        })

# Usage
async def decision_agent_example():
    agent = DecisionAgent()

    queries = [
        "What is Python?",
        "Explain the differences between supervised, unsupervised, and reinforcement learning, and how do neural networks, decision trees, and ensemble methods compare in each context?"
    ]

    for query in queries:
        print(f"\\nQuery: {query[:80]}...")
        result = await agent.run(query=query)
        print(f"Type: {result['type']}")
        print(f"Response: {result['response'][:200]}...")

asyncio.run(decision_agent_example())
```

### 3. Error-Handling Agent

Agent with robust error recovery.

```python
class RetryEvent(Event):
    """Event for retry logic."""
    original_query: str
    attempt: int
    error: str

class ErrorHandlingAgent(Workflow):
    """Agent with error handling and retry logic."""

    def __init__(self, max_retries: int = 3):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")
        self.max_retries = max_retries

    @step
    async def process_query(
        self,
        ctx: Context,
        ev: StartEvent | RetryEvent
    ) -> StopEvent | RetryEvent:
        """Process query with error handling."""
        if isinstance(ev, StartEvent):
            query = ev.get("query")
            attempt = 1
        else:
            query = ev.original_query
            attempt = ev.attempt + 1

        await ctx.set("query", query)
        await ctx.set("attempt", attempt)

        try:
            # Simulate potential failure
            import random
            if random.random() < 0.3 and attempt < 2:  # 30% chance of failure
                raise ValueError("Simulated processing error")

            messages = [
                ChatMessage(role="user", content=query)
            ]

            response = await self.llm.achat(messages)

            # Success
            return StopEvent(result={
                "status": "success",
                "response": response.message.content,
                "attempts": attempt
            })

        except Exception as e:
            error_msg = str(e)
            print(f"Attempt {attempt} failed: {error_msg}")

            if attempt >= self.max_retries:
                # Max retries reached
                return StopEvent(result={
                    "status": "error",
                    "error": error_msg,
                    "attempts": attempt,
                    "message": "Max retries exceeded"
                })

            # Retry
            await asyncio.sleep(1 * attempt)  # Exponential backoff
            return RetryEvent(
                original_query=query,
                attempt=attempt,
                error=error_msg
            )

# Usage
async def error_handling_example():
    agent = ErrorHandlingAgent(max_retries=3)
    result = await agent.run(query="Process this query")
    print(json.dumps(result, indent=2))

asyncio.run(error_handling_example())
```

---

## Multi-Agent Systems

### 1. Sequential Multi-Workflow System

Multiple workflows executing in sequence.

```python
class ResearchWorkflow(Workflow):
    """Workflow for research."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def research(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Research a topic."""
        topic = ev.get("topic")

        messages = [
            ChatMessage(
                role="system",
                content="You are a research specialist."
            ),
            ChatMessage(role="user", content=f"Research: {topic}")
        ]

        response = await self.llm.achat(messages)

        return StopEvent(result=response.message.content)


class AnalysisWorkflow(Workflow):
    """Workflow for analysis."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def analyze(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Analyze data."""
        data = ev.get("data")

        messages = [
            ChatMessage(
                role="system",
                content="You are a data analyst."
            ),
            ChatMessage(role="user", content=f"Analyze: {data}")
        ]

        response = await self.llm.achat(messages)

        return StopEvent(result=response.message.content)


class ReportWorkflow(Workflow):
    """Workflow for report generation."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def generate_report(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Generate report."""
        analysis = ev.get("analysis")

        messages = [
            ChatMessage(
                role="system",
                content="You are a report writer."
            ),
            ChatMessage(role="user", content=f"Create report from: {analysis}")
        ]

        response = await self.llm.achat(messages)

        return StopEvent(result=response.message.content)


class SequentialSystem:
    """Sequential multi-workflow system."""

    def __init__(self):
        self.research_workflow = ResearchWorkflow()
        self.analysis_workflow = AnalysisWorkflow()
        self.report_workflow = ReportWorkflow()

    async def execute(self, topic: str) -> Dict:
        """Execute workflows sequentially."""

        # Step 1: Research
        research_result = await self.research_workflow.run(topic=topic)
        print(f"Research completed: {len(research_result)} chars")

        # Step 2: Analysis
        analysis_result = await self.analysis_workflow.run(data=research_result)
        print(f"Analysis completed: {len(analysis_result)} chars")

        # Step 3: Report
        report_result = await self.report_workflow.run(analysis=analysis_result)
        print(f"Report completed: {len(report_result)} chars")

        return {
            "research": research_result,
            "analysis": analysis_result,
            "report": report_result
        }

# Usage
async def sequential_system_example():
    system = SequentialSystem()
    result = await system.execute("Quantum computing applications")
    print("\\nFINAL REPORT:")
    print(result["report"])

asyncio.run(sequential_system_example())
```

### 2. Parallel Multi-Workflow System

Multiple workflows executing in parallel.

```python
class ParallelSystem:
    """Parallel multi-workflow system."""

    def __init__(self):
        self.workflow1 = ResearchWorkflow()
        self.workflow2 = ResearchWorkflow()
        self.workflow3 = ResearchWorkflow()

    async def execute_parallel(self, topics: List[str]) -> List[str]:
        """Execute multiple workflows in parallel."""

        # Create tasks
        tasks = [
            self.workflow1.run(topic=topics[0]),
            self.workflow2.run(topic=topics[1]),
            self.workflow3.run(topic=topics[2])
        ]

        # Execute in parallel
        results = await asyncio.gather(*tasks)

        return results

# Usage
async def parallel_system_example():
    system = ParallelSystem()

    topics = [
        "Machine Learning",
        "Quantum Computing",
        "Blockchain Technology"
    ]

    print("Executing research in parallel...")
    results = await system.execute_parallel(topics)

    for topic, result in zip(topics, results):
        print(f"\\n{topic}:")
        print(result[:200] + "...")

asyncio.run(parallel_system_example())
```

### 3. Hierarchical Multi-Agent System

Coordinator workflow delegating to specialist workflows.

```python
class DelegateEvent(Event):
    """Event for delegation."""
    task_type: str
    task_data: str

class CoordinatorWorkflow(Workflow):
    """Coordinator workflow."""

    def __init__(self, specialists: Dict[str, Workflow]):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")
        self.specialists = specialists

    @step
    async def analyze_task(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> DelegateEvent:
        """Analyze task and determine delegation."""
        task = ev.get("task")

        # Determine task type (simplified)
        if "research" in task.lower():
            task_type = "research"
        elif "analyze" in task.lower() or "analysis" in task.lower():
            task_type = "analysis"
        elif "report" in task.lower() or "document" in task.lower():
            task_type = "report"
        else:
            task_type = "research"  # Default

        await ctx.set("task", task)
        await ctx.set("task_type", task_type)

        return DelegateEvent(task_type=task_type, task_data=task)

    @step
    async def delegate_and_aggregate(
        self,
        ctx: Context,
        ev: DelegateEvent
    ) -> StopEvent:
        """Delegate to specialist and return result."""
        specialist = self.specialists.get(ev.task_type)

        if not specialist:
            return StopEvent(result={"error": "No specialist found"})

        # Delegate to specialist
        if ev.task_type == "research":
            result = await specialist.run(topic=ev.task_data)
        elif ev.task_type == "analysis":
            result = await specialist.run(data=ev.task_data)
        elif ev.task_type == "report":
            result = await specialist.run(analysis=ev.task_data)
        else:
            result = "Unknown task type"

        return StopEvent(result={
            "task_type": ev.task_type,
            "result": result,
            "delegated_to": ev.task_type + "_specialist"
        })

# Usage
async def hierarchical_system_example():
    # Create specialists
    specialists = {
        "research": ResearchWorkflow(),
        "analysis": AnalysisWorkflow(),
        "report": ReportWorkflow()
    }

    # Create coordinator
    coordinator = CoordinatorWorkflow(specialists)

    # Execute tasks
    tasks = [
        "Research AI trends",
        "Analyze this data: [sample data]",
        "Create a report about findings"
    ]

    for task in tasks:
        print(f"\\nTask: {task}")
        result = await coordinator.run(task=task)
        print(f"Delegated to: {result['delegated_to']}")
        print(f"Result: {result['result'][:100]}...")

asyncio.run(hierarchical_system_example())
```

---

## RAG with Agents (Agentic RAG)

### 1. Basic RAG Workflow

Workflow with retrieval and generation.

```python
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

class RetrievalEvent(Event):
    """Event with retrieved documents."""
    query: str
    documents: List[str]

class RAGWorkflow(Workflow):
    """Basic RAG workflow."""

    def __init__(self, documents: List[str]):
        super().__init__()

        # Setup LlamaIndex
        Settings.llm = OpenAI(model="gpt-4o-mini")
        Settings.embed_model = OpenAIEmbedding()

        # Create index from documents
        docs = [Document(text=doc) for doc in documents]
        self.index = VectorStoreIndex.from_documents(docs)
        self.retriever = self.index.as_retriever(similarity_top_k=3)

    @step
    async def retrieve(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> RetrievalEvent:
        """Retrieve relevant documents."""
        query = ev.get("query")

        # Retrieve documents
        nodes = await self.retriever.aretrieve(query)
        documents = [node.text for node in nodes]

        await ctx.set("query", query)
        await ctx.set("retrieved_docs", documents)

        return RetrievalEvent(query=query, documents=documents)

    @step
    async def generate(
        self,
        ctx: Context,
        ev: RetrievalEvent
    ) -> StopEvent:
        """Generate answer from retrieved documents."""
        context = "\\n\\n".join(ev.documents)

        messages = [
            ChatMessage(
                role="system",
                content="Answer the question based on the provided context."
            ),
            ChatMessage(
                role="user",
                content=f"""Context:\\n{context}\\n\\nQuestion: {ev.query}"""
            )
        ]

        response = await Settings.llm.achat(messages)

        return StopEvent(result={
            "answer": response.message.content,
            "sources": ev.documents,
            "num_sources": len(ev.documents)
        })

# Usage
async def rag_workflow_example():
    documents = [
        "Machine learning is a subset of AI that enables systems to learn from data.",
        "Deep learning uses neural networks with multiple layers.",
        "Natural language processing helps computers understand human language.",
        "Computer vision enables machines to interpret images and videos.",
        "Reinforcement learning involves learning through trial and error."
    ]

    workflow = RAGWorkflow(documents)

    result = await workflow.run(query="What is machine learning?")

    print("Answer:", result["answer"])
    print(f"\\nBased on {result['num_sources']} sources")

asyncio.run(rag_workflow_example())
```

### 2. Advanced Agentic RAG

Multi-step RAG with query refinement and re-ranking.

```python
class QueryRefinementEvent(Event):
    """Event with refined query."""
    original_query: str
    refined_query: str

class RerankEvent(Event):
    """Event with re-ranked documents."""
    query: str
    ranked_documents: List[tuple[str, float]]  # (doc, score)

class AdvancedRAGWorkflow(Workflow):
    """Advanced agentic RAG workflow."""

    def __init__(self, documents: List[str]):
        super().__init__()

        Settings.llm = OpenAI(model="gpt-4o-mini")
        Settings.embed_model = OpenAIEmbedding()

        docs = [Document(text=doc) for doc in documents]
        self.index = VectorStoreIndex.from_documents(docs)
        self.retriever = self.index.as_retriever(similarity_top_k=5)

    @step
    async def refine_query(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> QueryRefinementEvent:
        """Refine user query for better retrieval."""
        query = ev.get("query")

        messages = [
            ChatMessage(
                role="system",
                content="Refine this query to be more specific and searchable."
            ),
            ChatMessage(role="user", content=query)
        ]

        response = await Settings.llm.achat(messages)
        refined_query = response.message.content

        await ctx.set("original_query", query)
        await ctx.set("refined_query", refined_query)

        return QueryRefinementEvent(
            original_query=query,
            refined_query=refined_query
        )

    @step
    async def retrieve_and_rerank(
        self,
        ctx: Context,
        ev: QueryRefinementEvent
    ) -> RerankEvent:
        """Retrieve documents and re-rank."""
        # Retrieve with refined query
        nodes = await self.retriever.aretrieve(ev.refined_query)
        documents = [node.text for node in nodes]

        # Simple re-ranking based on query similarity
        # In production, use a proper re-ranking model
        scores = [0.9, 0.8, 0.75, 0.6, 0.5][:len(documents)]
        ranked_docs = list(zip(documents, scores))
        ranked_docs.sort(key=lambda x: x[1], reverse=True)

        await ctx.set("retrieved_docs", ranked_docs)

        return RerankEvent(
            query=ev.refined_query,
            ranked_documents=ranked_docs
        )

    @step
    async def generate_with_citations(
        self,
        ctx: Context,
        ev: RerankEvent
    ) -> StopEvent:
        """Generate answer with citations."""
        # Use top 3 re-ranked documents
        top_docs = ev.ranked_documents[:3]

        context = "\\n\\n".join([
            f"[Source {i+1}] {doc}"
            for i, (doc, score) in enumerate(top_docs)
        ])

        messages = [
            ChatMessage(
                role="system",
                content="Answer using the context and cite sources with [Source N]."
            ),
            ChatMessage(
                role="user",
                content=f"""Context:\\n{context}\\n\\nQuestion: {ev.query}"""
            )
        ]

        response = await Settings.llm.achat(messages)

        return StopEvent(result={
            "answer": response.message.content,
            "sources": [doc for doc, _ in top_docs],
            "source_scores": [score for _, score in top_docs],
            "original_query": await ctx.get("original_query"),
            "refined_query": await ctx.get("refined_query")
        })

# Usage
async def advanced_rag_example():
    documents = [
        "Machine learning algorithms learn patterns from data without explicit programming.",
        "Deep learning is a subset of machine learning using multi-layer neural networks.",
        "Supervised learning requires labeled training data.",
        "Unsupervised learning finds patterns in unlabeled data.",
        "Transfer learning applies pre-trained models to new tasks.",
        "Neural networks consist of interconnected nodes organized in layers.",
        "Convolutional neural networks excel at image processing tasks.",
        "Recurrent neural networks handle sequential data like text.",
        "Transformers revolutionized natural language processing.",
        "Attention mechanisms help models focus on relevant information."
    ]

    workflow = AdvancedRAGWorkflow(documents)

    result = await workflow.run(query="How do ML algorithms learn?")

    print("Answer:", result["answer"])
    print(f"\\nOriginal query: {result['original_query']}")
    print(f"Refined query: {result['refined_query']}")
    print(f"\\nTop sources:")
    for i, (source, score) in enumerate(zip(result['sources'], result['source_scores'])):
        print(f"  {i+1}. (score: {score:.2f}) {source[:60]}...")

asyncio.run(advanced_rag_example())
```

---

## FASTMCP Servers with Agents

FASTMCP integrates with LlamaIndex Workflows to provide standardized tool access.

```python
from fastmcp import FastMCP

# Create MCP Server
mcp = FastMCP("LlamaIndex MCP Server")

@mcp.tool()
def query_database(query_text: str) -> str:
    """Query database via MCP."""
    # Simulated database query
    return json.dumps([{"id": 1, "data": "Result"}])

class MCPWorkflow(Workflow):
    """Workflow using MCP tools."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def use_mcp_tool(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Use MCP tool in workflow."""
        query = ev.get("query")

        # Call MCP tool
        result = query_database(query)

        # Process with LLM
        messages = [ChatMessage(role="user", content=f"Analyze: {result}")]
        response = await self.llm.achat(messages)

        return StopEvent(result=response.message.content)
```

---

## A2A (Agent-to-Agent) Integration

LlamaIndex Workflows can implement A2A protocol for agent communication.

```python
from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"

@dataclass
class A2AMessage:
    message_type: MessageType
    sender_id: str
    receiver_id: str
    payload: Dict

class A2AWorkflow(Workflow):
    """Workflow with A2A capabilities."""

    def __init__(self, agent_id: str):
        super().__init__()
        self.agent_id = agent_id
        self.llm = OpenAI(model="gpt-4o-mini")
        self.known_agents = {}

    @step
    async def handle_a2a_request(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Handle A2A message."""
        message = A2AMessage(
            message_type=MessageType.TASK_REQUEST,
            sender_id=self.agent_id,
            receiver_id="target_agent",
            payload={"task": ev.get("task")}
        )

        # Process message
        response = await self.llm.achat([
            ChatMessage(role="user", content=message.payload["task"])
        ])

        return StopEvent(result=response.message.content)
```

---

## Advanced Patterns

### 1. Dynamic Step Registration

```python
class DynamicWorkflow(Workflow):
    """Workflow with dynamic step creation."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    def create_processing_step(self, step_name: str):
        """Dynamically create processing step."""
        @step
        async def dynamic_step(ctx: Context, ev: Event) -> StopEvent:
            result = await self.llm.achat([
                ChatMessage(role="user", content=f"Process with {step_name}")
            ])
            return StopEvent(result=result.message.content)

        return dynamic_step
```

### 2. Workflow Composition

```python
class ComposedWorkflow(Workflow):
    """Compose multiple workflows."""

    def __init__(self):
        super().__init__()
        self.sub_workflow1 = ResearchWorkflow()
        self.sub_workflow2 = AnalysisWorkflow()

    @step
    async def orchestrate(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Orchestrate sub-workflows."""
        # Execute sub-workflows
        result1 = await self.sub_workflow1.run(topic=ev.get("topic"))
        result2 = await self.sub_workflow2.run(data=result1)

        return StopEvent(result=result2)
```

---

## Production Best Practices

### 1. Error Handling

```python
class ProductionWorkflow(Workflow):
    """Production-ready workflow with error handling."""

    @step
    async def safe_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Step with comprehensive error handling."""
        try:
            result = await self.llm.achat([
                ChatMessage(role="user", content=ev.get("query"))
            ])
            return StopEvent(result=result.message.content)

        except asyncio.TimeoutError:
            return StopEvent(result={"error": "Timeout"})

        except Exception as e:
            logger.error(f"Error: {e}")
            return StopEvent(result={"error": str(e)})
```

### 2. Logging and Monitoring

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoredWorkflow(Workflow):
    """Workflow with logging."""

    @step
    async def monitored_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Step with logging."""
        logger.info(f"Processing: {ev.get('query')}")

        start = time.time()
        result = await self.llm.achat([
            ChatMessage(role="user", content=ev.get("query"))
        ])
        duration = time.time() - start

        logger.info(f"Completed in {duration:.2f}s")

        return StopEvent(result=result.message.content)
```

---

## Troubleshooting

### Common Issues

**1. Event Not Triggering Step**
- Ensure event type matches step signature
- Check event import statements
- Verify step decorator is applied

**2. Context Not Persisting**
- Always use `await ctx.set()` and `await ctx.get()`
- Check context key names for typos
- Ensure context operations are awaited

**3. Workflow Hangs**
- Check for missing StopEvent
- Verify all async operations are awaited
- Look for infinite event loops

**4. Import Errors**
```python
# Correct imports
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Event, Context
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
```

---

## Conclusion

LlamaIndex Workflows provides a powerful event-driven framework for building sophisticated AI agent systems. Key takeaways:

- **Event-Driven**: Natural modeling of complex, branching workflows
- **Async/Await**: Built for scalability and performance
- **Context Management**: Shared state across workflow steps
- **Flexible**: Sequential, parallel, and conditional execution
- **Production-Ready**: Error handling, logging, monitoring

### Resources

- **LlamaIndex Docs**: https://docs.llamaindex.ai/
- **Workflows Guide**: https://docs.llamaindex.ai/en/stable/module_guides/workflows/
- **GitHub**: https://github.com/run-llama/llama_index

---

**Document Version**: 1.0
**Last Updated**: 2026-01-19
**Total Lines**: 2400+
**Status**: Production Ready