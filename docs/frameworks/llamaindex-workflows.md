# LlamaIndex Workflows with Custom-Evals

## Overview

LlamaIndex Workflows is an event-driven orchestration framework for building sophisticated multi-step AI agents. It provides a powerful abstraction for managing complex agent workflows with state management, event routing, and step-by-step execution control.

**Key Features**:
- **Event-Driven Architecture**: Build workflows using custom events and event handlers
- **Step Decorators**: Define workflow steps with `@step` decorator
- **Context Management**: Shared context across workflow steps
- **Async/Await Support**: Native asynchronous execution
- **Multi-Step Orchestration**: Complex multi-agent research and analysis workflows
- **Custom-Evals Integration**: Full support for Phoenix custom-evals evaluation framework

**Use Cases**:
- Multi-step research workflows
- Complex data processing pipelines
- Automated analysis and reporting
- Knowledge extraction and summarization
- Event-driven agent orchestration

---

## Installation

### Prerequisites
- Python 3.10 or higher
- OpenAI API key
- LlamaIndex library

### Install Dependencies

```bash
pip install llama-index llama-index-llms-openai
```

### Environment Setup

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### Verify Installation

```python
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4o-mini")
print("✅ LlamaIndex Workflows installed successfully")
```

---

## Quick Start

### Simple Workflow Example

```python
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Context
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage

class SimpleWorkflow(Workflow):
    """Basic workflow with single step."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def process_query(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Process the query."""
        query = ev.get("query")

        messages = [
            ChatMessage(role="system", content="You are a helpful assistant."),
            ChatMessage(role="user", content=query)
        ]

        response = await self.llm.achat(messages)
        return StopEvent(result=response.message.content)

# Usage
import asyncio

workflow = SimpleWorkflow()
result = asyncio.run(workflow.run(query="What is artificial intelligence?"))
print(result)
```

### Multi-Step Research Workflow

```python
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Event, Context

class ResearchEvent(Event):
    """Event for research phase."""
    query: str

class AnalysisEvent(Event):
    """Event for analysis phase."""
    research_result: str

class ResearchWorkflow(Workflow):
    """Multi-step research workflow."""

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def research_step(self, ctx: Context, ev: StartEvent) -> ResearchEvent:
        """Step 1: Research the topic."""
        query = ev.get("query")

        messages = [
            ChatMessage(role="system", content="You are a research specialist."),
            ChatMessage(role="user", content=f"Research: {query}")
        ]

        response = await self.llm.achat(messages)
        await ctx.set("research", response.message.content)
        return ResearchEvent(query=query)

    @step
    async def analysis_step(self, ctx: Context, ev: ResearchEvent) -> AnalysisEvent:
        """Step 2: Analyze the research."""
        research = await ctx.get("research")

        messages = [
            ChatMessage(role="system", content="You are an analysis expert."),
            ChatMessage(role="user", content=f"Analyze: {research}")
        ]

        response = await self.llm.achat(messages)
        await ctx.set("analysis", response.message.content)
        return AnalysisEvent(research_result=research)

    @step
    async def summary_step(self, ctx: Context, ev: AnalysisEvent) -> StopEvent:
        """Step 3: Create summary."""
        analysis = await ctx.get("analysis")

        messages = [
            ChatMessage(role="system", content="You are a technical writer."),
            ChatMessage(role="user", content=f"Summarize: {analysis}")
        ]

        response = await self.llm.achat(messages)
        return StopEvent(result=response.message.content)

# Usage
workflow = ResearchWorkflow()
result = asyncio.run(workflow.run(query="Machine Learning Applications"))
print(result)
```

---

## Architecture

### Core Components

**1. Workflow**
- Base class for all workflows
- Manages event routing and step execution
- Handles context and state management

**2. Events**
- Custom event classes inheriting from `Event`
- Carry data between workflow steps
- `StartEvent`: Initiates workflow
- `StopEvent`: Terminates workflow with result

**3. Steps**
- Functions decorated with `@step`
- Process events and return new events
- Access shared context via `Context` object

**4. Context**
- Shared state across workflow steps
- Async get/set operations: `await ctx.get()`, `await ctx.set()`
- Persists data throughout workflow execution

### Event Flow Pattern

```
StartEvent → Step 1 → CustomEvent1 → Step 2 → CustomEvent2 → Step 3 → StopEvent
              ↓                        ↓                        ↓
           Context                  Context                  Context
```

---

## Custom-Evals Integration

### Complete Evaluation System

```python
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM

class EvaluatedWorkflowAgent:
    """Workflow agent with evaluation capabilities."""

    def __init__(self):
        self.workflow = ResearchWorkflow()

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    async def run_and_evaluate(self, query: str):
        """Run workflow and evaluate response."""
        # Run workflow
        result = await self.workflow.run(query=query)

        # Evaluate
        scores = {}
        for name, evaluator in self.evaluators.items():
            score = evaluator.evaluate({"input": query, "output": result})
            scores[name] = score

        return {"response": result, "scores": scores}

# Usage
agent = EvaluatedWorkflowAgent()
result = asyncio.run(agent.run_and_evaluate("Explain neural networks"))

print(f"Response: {result['response'][:200]}...\n")
print("Evaluation Scores:")
for metric, score in result['scores'].items():
    print(f"  {metric.capitalize()}: {score.label} ({score.score:.2f})")
```

### Quality Thresholds
- Coherence: ≥ 0.7
- Relevance: ≥ 0.7
- Correctness: ≥ 0.7
- Toxicity: ≤ 0.2

---

## Best Practices

### 1. Event Design
**Create specific, focused events**:
```python
# ✅ Good: Specific event
class ResearchEvent(Event):
    query: str
    sources: List[str]

# ❌ Bad: Generic event
class GenericEvent(Event):
    data: Dict[str, Any]
```

### 2. Context Management
**Use context for state sharing**:
```python
@step
async def step1(self, ctx: Context, ev: StartEvent):
    result = process(ev.get("query"))
    await ctx.set("step1_result", result)  # Save to context
    return NextEvent()

@step
async def step2(self, ctx: Context, ev: NextEvent):
    previous_result = await ctx.get("step1_result")  # Retrieve from context
    return StopEvent(result=process(previous_result))
```

### 3. Error Handling
**Implement robust error handling in steps**:
```python
@step
async def safe_step(self, ctx: Context, ev: Event) -> Event:
    try:
        result = await process(ev.data)
        return SuccessEvent(result=result)
    except Exception as e:
        return ErrorEvent(error=str(e))
```

### 4. Async Operations
**Always use async/await for workflows**:
```python
# ✅ Good: Async execution
result = await workflow.run(query="...")

# ❌ Bad: Sync execution
# result = workflow.run(query="...")  # Won't work correctly
```

---

## Resources

### Official Documentation
- **LlamaIndex**: https://docs.llamaindex.ai/
- **Workflows Guide**: https://docs.llamaindex.ai/en/stable/module_guides/workflows/

### Example Files
- **Complete Example**: `examples/llamaindex_workflows_example.py` (17KB)
- **Test Suites**: 5 comprehensive tests covering all use cases
- **Custom-Evals Integration**: Full evaluation implementation

### Phoenix Custom-Evals
- **Evaluators**: CoherenceEvaluator, RelevanceEvaluator, CorrectnessEvaluator, ToxicityEvaluator
- **LLM Integration**: Support for OpenAI, Anthropic, and other providers

---

**Created**: 2026-01-17
**Status**: Production Ready
**Framework Version**: Latest
**Custom-Evals**: Fully Integrated
