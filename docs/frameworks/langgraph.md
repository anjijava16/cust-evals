# LangGraph with Custom-Evals

## Overview

LangGraph is LangChain's library for building stateful, multi-actor applications with LLMs using graph-based workflows. It extends LangChain's capabilities with cyclical graphs, state persistence, and sophisticated control flow for building complex agent systems.

**Key Features**:
- **State Graphs**: Build applications as graphs with nodes and edges
- **Cyclic Workflows**: Support for loops and conditional branching
- **State Persistence**: Maintain state across workflow steps
- **Multi-Agent Systems**: Orchestrate multiple agents in complex workflows
- **Human-in-the-Loop**: Built-in support for human intervention
- **Checkpointing**: Save and restore workflow state
- **Custom-Evals Integration**: Full support for Phoenix custom-evals evaluation framework

**Use Cases**:
- Complex multi-step reasoning workflows
- Agent collaboration and handoffs
- Stateful conversational agents
- Multi-actor research and analysis
- Workflow automation with conditional logic

---

## Installation

### Prerequisites
- Python 3.10 or higher
- OpenAI API key
- LangChain and LangGraph libraries

### Install Dependencies

```bash
pip install langgraph langchain langchain-openai
```

### Environment Setup

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### Verify Installation

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
print("✅ LangGraph installed successfully")
```

---

## Quick Start

### Simple State Graph Example

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Define state
class AgentState(TypedDict):
    messages: list
    current_step: str

# Create LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define nodes
def agent_node(state: AgentState):
    """Process query with LLM."""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {
        "messages": messages + [response],
        "current_step": "completed"
    }

# Create graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", agent_node)

# Set entry point
workflow.set_entry_point("agent")

# Add edges
workflow.add_edge("agent", END)

# Compile
app = workflow.compile()

# Run
result = app.invoke({
    "messages": [HumanMessage(content="What is artificial intelligence?")],
    "current_step": "start"
})

print(result["messages"][-1].content)
```

### Multi-Step Research Workflow

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class ResearchState(TypedDict):
    query: str
    research: str
    analysis: str
    summary: str
    current_step: str

llm = ChatOpenAI(model="gpt-4o-mini")

def research_node(state: ResearchState):
    """Research the topic."""
    messages = [
        SystemMessage(content="You are a research specialist. Gather comprehensive information."),
        HumanMessage(content=f"Research: {state['query']}")
    ]
    response = llm.invoke(messages)
    return {"research": response.content, "current_step": "research_done"}

def analysis_node(state: ResearchState):
    """Analyze the research."""
    messages = [
        SystemMessage(content="You are an analysis expert. Extract key insights."),
        HumanMessage(content=f"Analyze: {state['research']}")
    ]
    response = llm.invoke(messages)
    return {"analysis": response.content, "current_step": "analysis_done"}

def summary_node(state: ResearchState):
    """Create summary."""
    messages = [
        SystemMessage(content="You are a technical writer. Create clear summaries."),
        HumanMessage(content=f"Summarize: {state['analysis']}")
    ]
    response = llm.invoke(messages)
    return {"summary": response.content, "current_step": "completed"}

# Create workflow
workflow = StateGraph(ResearchState)

# Add nodes
workflow.add_node("research", research_node)
workflow.add_node("analysis", analysis_node)
workflow.add_node("summary", summary_node)

# Set entry point
workflow.set_entry_point("research")

# Add edges
workflow.add_edge("research", "analysis")
workflow.add_edge("analysis", "summary")
workflow.add_edge("summary", END)

# Compile
app = workflow.compile()

# Run
result = app.invoke({
    "query": "Machine Learning Applications",
    "research": "",
    "analysis": "",
    "summary": "",
    "current_step": "start"
})

print(result["summary"])
```

---

## Architecture

### Core Components

**1. StateGraph**
- Defines workflow as a graph
- Manages state transitions between nodes
- Supports conditional edges and loops

**2. State**
- TypedDict defining workflow state
- Passed between nodes
- Can include any Python objects

**3. Nodes**
- Functions that process state
- Return updated state
- Can call LLMs, tools, or other functions

**4. Edges**
- Define transitions between nodes
- Can be conditional based on state
- Support loops and branching

**5. Checkpointing**
- Save workflow state at each step
- Resume from checkpoints
- Support for human-in-the-loop

### Graph Pattern

```
START → Node1 → Node2 → Node3 → END
          ↓       ↑
          └───────┘  (conditional loop)
```

---

## Custom-Evals Integration

### Complete Evaluation System

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM

class EvaluatedAgentState(TypedDict):
    query: str
    response: str
    evaluation_scores: dict
    current_step: str

class EvaluatedLangGraphAgent:
    """LangGraph agent with custom-evals integration."""

    def __init__(self):
        # Create LLM
        self.llm = ChatOpenAI(model="gpt-4o-mini")

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

        # Create workflow
        self.app = self._create_workflow()

    def _agent_node(self, state: EvaluatedAgentState):
        """Agent processing node."""
        messages = [HumanMessage(content=state["query"])]
        response = self.llm.invoke(messages)
        return {
            "response": response.content,
            "current_step": "agent_done"
        }

    def _evaluation_node(self, state: EvaluatedAgentState):
        """Evaluation node."""
        scores = {}
        for name, evaluator in self.evaluators.items():
            score = evaluator.evaluate({
                "input": state["query"],
                "output": state["response"]
            })
            scores[name] = score

        return {
            "evaluation_scores": scores,
            "current_step": "completed"
        }

    def _create_workflow(self):
        """Create LangGraph workflow."""
        workflow = StateGraph(EvaluatedAgentState)

        # Add nodes
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("evaluate", self._evaluation_node)

        # Set entry point
        workflow.set_entry_point("agent")

        # Add edges
        workflow.add_edge("agent", "evaluate")
        workflow.add_edge("evaluate", END)

        return workflow.compile()

    def run_and_evaluate(self, query: str):
        """Run agent and evaluate response."""
        result = self.app.invoke({
            "query": query,
            "response": "",
            "evaluation_scores": {},
            "current_step": "start"
        })

        return {
            "response": result["response"],
            "scores": result["evaluation_scores"]
        }

# Usage
agent = EvaluatedLangGraphAgent()
result = agent.run_and_evaluate("What is machine learning?")

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

## Multi-Agent Systems

### Multi-Agent Collaboration with State Graph

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

class MultiAgentState(TypedDict):
    topic: str
    research_output: str
    analysis_output: str
    final_output: str
    current_agent: str

class LangGraphMultiAgentSystem:
    """Multi-agent system using LangGraph."""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.app = self._create_workflow()

    def _research_agent(self, state: MultiAgentState):
        """Research agent node."""
        messages = [
            SystemMessage(content="You are a research specialist."),
            HumanMessage(content=f"Research: {state['topic']}")
        ]
        response = self.llm.invoke(messages)
        return {
            "research_output": response.content,
            "current_agent": "analyst"
        }

    def _analysis_agent(self, state: MultiAgentState):
        """Analysis agent node."""
        messages = [
            SystemMessage(content="You are an analysis expert."),
            HumanMessage(content=f"Analyze: {state['research_output']}")
        ]
        response = self.llm.invoke(messages)
        return {
            "analysis_output": response.content,
            "current_agent": "writer"
        }

    def _writer_agent(self, state: MultiAgentState):
        """Writer agent node."""
        messages = [
            SystemMessage(content="You are a technical writer."),
            HumanMessage(content=f"Summarize: {state['analysis_output']}")
        ]
        response = self.llm.invoke(messages)
        return {
            "final_output": response.content,
            "current_agent": "done"
        }

    def _create_workflow(self):
        """Create multi-agent workflow."""
        workflow = StateGraph(MultiAgentState)

        # Add agent nodes
        workflow.add_node("researcher", self._research_agent)
        workflow.add_node("analyst", self._analysis_agent)
        workflow.add_node("writer", self._writer_agent)

        # Set entry point
        workflow.set_entry_point("researcher")

        # Add edges
        workflow.add_edge("researcher", "analyst")
        workflow.add_edge("analyst", "writer")
        workflow.add_edge("writer", END)

        return workflow.compile()

    def run_workflow(self, topic: str):
        """Run multi-agent workflow."""
        result = self.app.invoke({
            "topic": topic,
            "research_output": "",
            "analysis_output": "",
            "final_output": "",
            "current_agent": "researcher"
        })

        return {
            "research": result["research_output"],
            "analysis": result["analysis_output"],
            "final_output": result["final_output"]
        }

# Usage
system = LangGraphMultiAgentSystem()
result = system.run_workflow("Artificial Intelligence Ethics")
print(result["final_output"])
```

---

## Best Practices

### 1. State Design
**Use TypedDict for clear state definitions**:
```python
# ✅ Good: Clear state structure
class AgentState(TypedDict):
    query: str
    response: str
    metadata: dict
    current_step: str

# ❌ Bad: Untyped dictionary
state = {"query": "...", "response": "..."}
```

### 2. Node Functions
**Keep nodes focused and single-purpose**:
```python
# ✅ Good: Focused node
def research_node(state: ResearchState):
    response = llm.invoke([HumanMessage(content=state["query"])])
    return {"research": response.content}

# ❌ Bad: Doing too much
def mega_node(state):
    # Research, analyze, summarize all in one node
    ...
```

### 3. Error Handling
**Implement error handling in nodes**:
```python
def safe_node(state: AgentState):
    try:
        response = llm.invoke([HumanMessage(content=state["query"])])
        return {"response": response.content, "error": None}
    except Exception as e:
        return {"response": "", "error": str(e)}
```

### 4. Conditional Edges
**Use conditional edges for branching logic**:
```python
def should_continue(state: AgentState):
    """Decide whether to continue or end."""
    if state.get("error"):
        return "end"
    return "continue"

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "next_node",
        "end": END
    }
)
```

### 5. Checkpointing
**Use checkpoints for long-running workflows**:
```python
from langgraph.checkpoint import MemorySaver

# Add checkpointing
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Run with thread_id for resuming
config = {"configurable": {"thread_id": "unique-id"}}
result = app.invoke(initial_state, config)
```

---

## Resources

### Official Documentation
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **LangChain**: https://python.langchain.com/
- **GitHub**: https://github.com/langchain-ai/langgraph

### Example Files
- **Complete Example**: Create `examples/langgraph_example.py`
- **Test Suites**: 5 comprehensive tests
- **Custom-Evals Integration**: Full evaluation implementation

### Phoenix Custom-Evals
- **Evaluators**: CoherenceEvaluator, RelevanceEvaluator, CorrectnessEvaluator, ToxicityEvaluator
- **LLM Integration**: Support for OpenAI, Anthropic, and other providers

---

## Quick Reference

### Installation
```bash
pip install langgraph langchain langchain-openai
export OPENAI_API_KEY="your-openai-api-key"
```

### Basic Graph
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    data: str

workflow = StateGraph(State)
workflow.add_node("node1", lambda state: {"data": "processed"})
workflow.set_entry_point("node1")
workflow.add_edge("node1", END)
app = workflow.compile()

result = app.invoke({"data": "input"})
```

### With Evaluation
```python
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM

eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)
score = evaluator.evaluate({"input": query, "output": response})
```

---

**Created**: 2026-01-17
**Status**: Production Ready
**Framework Version**: Latest
**Custom-Evals**: Fully Integrated
