# Google Agent Development Kit (ADK): Deep Dive Guide

## Table of Contents

- [Introduction](#introduction)
- [Architecture Overview](#architecture-overview)
- [Installation and Setup](#installation-and-setup)
- [Core Concepts](#core-concepts)
- [Production-Ready Examples](#production-ready-examples)
- [Advanced Usage](#advanced-usage)
- [Best Practices](#best-practices)
- [Integration Guide](#integration-guide)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)
- [Performance](#performance)
- [Security](#security)
- [References](#references)

---

## Introduction

### What is Google ADK?

Google Agent Development Kit (ADK) is Google's comprehensive framework for **building, evaluating, and deploying AI agents**. It provides end-to-end tooling specifically designed for agent-based applications, including specialized evaluation capabilities for agent behavior, tool usage, and multi-step reasoning.

**Key Characteristics:**

- **Agent-First Design**: Built specifically for agent evaluation and development
- **Comprehensive CLI**: Command-line tools for the entire agent lifecycle
- **Built-in Evaluators**: Specialized evaluators for agent-specific metrics
- **Tool Call Evaluation**: Deep analysis of function/tool calling behavior
- **Multi-Turn Assessment**: Evaluate complex, multi-step agent interactions
- **Google Integration**: Native support for Gemini, Vertex AI, and Google Cloud
- **Trajectory Analysis**: Track and analyze complete agent execution paths
- **Production Ready**: Enterprise-grade deployment and monitoring

### Why Use Google ADK?

**Strengths:**

1. **Agent Specialization**: Purpose-built for agent evaluation, not adapted from general LLM eval
2. **Tool/Function Calling**: Best-in-class evaluation of tool usage patterns
3. **CLI Excellence**: Powerful command-line interface for workflows
4. **Google Ecosystem**: Seamless integration with Google Cloud services
5. **Enterprise Features**: Security, scalability, compliance built-in
6. **Trajectory Tracking**: Complete visibility into agent decision-making
7. **Multi-Modal Support**: Evaluate agents using text, images, and more
8. **Automated Testing**: CI/CD integration for agent quality gates

**Ideal Use Cases:**

- AI agent development and testing
- Tool/function calling evaluation
- Multi-step reasoning assessment
- Agent behavior analysis
- Production agent monitoring
- A/B testing agent configurations
- Regression testing for agent updates
- Enterprise agent deployment

### Framework Philosophy

Google ADK design principles:

1. **Agent-Centric**: Everything designed around agent workflows
2. **Tool Excellence**: Deep understanding of tool/function calling patterns
3. **Production Grade**: Built for enterprise deployment from day one
4. **Developer Velocity**: CLI-first approach for rapid iteration
5. **Observable**: Complete visibility into agent behavior
6. **Composable**: Mix and match evaluators and components
7. **Google Scale**: Leverage Google's infrastructure and models

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Google ADK Framework                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    CLI Layer                                 │  │
│  │  - adk init: Initialize projects                            │  │
│  │  - adk eval: Run evaluations                                │  │
│  │  - adk deploy: Deploy agents                                │  │
│  │  - adk monitor: Monitor production                          │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ↓                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  Agent Framework                             │  │
│  │  ┌────────────┬──────────────┬──────────────────────────┐   │  │
│  │  │  Agent     │  Tools       │  Memory                  │   │  │
│  │  │  Core      │  Registry    │  Management              │   │  │
│  │  └────────────┴──────────────┴──────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ↓                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │               Evaluation Engine                              │  │
│  │  ┌────────────┬────────────┬────────────┬──────────────┐    │  │
│  │  │  Task      │  Tool      │  Trajectory│  Human       │    │  │
│  │  │  Success   │  Usage     │  Analysis  │  Alignment   │    │  │
│  │  └────────────┴────────────┴────────────┴──────────────┘    │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ↓                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              Model Abstraction Layer                         │  │
│  │  - Gemini (1.5 Pro, 1.5 Flash, Ultra)                       │  │
│  │  - Vertex AI                                                 │  │
│  │  - Custom models via API                                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ↓                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │            Storage & Analytics                               │  │
│  │  - Eval results                                              │  │
│  │  - Trajectory logs                                           │  │
│  │  - Metrics database                                          │  │
│  │  - BigQuery integration                                      │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ↓                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │          Google Cloud Integration                            │  │
│  │  - Cloud Run (deployment)                                    │  │
│  │  - Cloud Functions                                           │  │
│  │  - Cloud Monitoring                                          │  │
│  │  - Cloud Logging                                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Agent Framework

**Agent Definition:**
```python
from google.adk import Agent, Tool

class CustomerSupportAgent(Agent):
    """Agent for customer support tasks"""

    def __init__(self):
        super().__init__(
            name="customer_support",
            model="gemini-1.5-pro",
            description="Handles customer support queries"
        )

        # Register tools
        self.register_tool(search_knowledge_base)
        self.register_tool(create_ticket)
        self.register_tool(send_email)

    async def plan(self, user_input: str) -> list:
        """Plan agent actions"""
        # Planning logic
        pass

    async def execute(self, plan: list) -> dict:
        """Execute planned actions"""
        # Execution logic
        pass
```

**Tool Definition:**
```python
from google.adk import Tool, Parameter

@Tool(
    name="search_knowledge_base",
    description="Search the customer support knowledge base",
    parameters=[
        Parameter("query", "string", "Search query"),
        Parameter("max_results", "integer", "Max results to return", default=5)
    ]
)
def search_knowledge_base(query: str, max_results: int = 5) -> list:
    """Search implementation"""
    # Search logic
    return results
```

#### 2. Evaluation System

**Built-in Evaluators:**

```python
from google.adk.eval import (
    TaskSuccessEvaluator,
    ToolUsageEvaluator,
    TrajectoryEvaluator,
    HumanAlignmentEvaluator
)

# Task success evaluation
task_eval = TaskSuccessEvaluator(
    expected_outcome="User's question answered accurately"
)

# Tool usage evaluation
tool_eval = ToolUsageEvaluator(
    expected_tools=["search_knowledge_base"],
    check_parameters=True,
    check_sequencing=True
)

# Trajectory evaluation
trajectory_eval = TrajectoryEvaluator(
    max_steps=10,
    efficiency_threshold=0.7
)
```

#### 3. CLI Commands

**Primary Commands:**

```bash
# Initialize new agent project
adk init my-agent --template=basic

# Run evaluations
adk eval --config eval_config.yaml

# Deploy to production
adk deploy --target=cloud-run --region=us-central1

# Monitor production agent
adk monitor --agent=my-agent --metrics=all

# Run tests
adk test --suite=integration

# Benchmark performance
adk benchmark --scenarios=scenarios.json
```

#### 4. Configuration System

**agent_config.yaml:**
```yaml
agent:
  name: customer_support_agent
  model: gemini-1.5-pro
  temperature: 0.3
  max_tokens: 2048

tools:
  - name: search_knowledge_base
    enabled: true
  - name: create_ticket
    enabled: true
  - name: send_email
    enabled: false

evaluation:
  evaluators:
    - task_success
    - tool_usage
    - trajectory_analysis

  datasets:
    - path: ./eval_data/basic_queries.json
    - path: ./eval_data/complex_scenarios.json

deployment:
  platform: cloud-run
  region: us-central1
  min_instances: 1
  max_instances: 10
```

---

## Installation and Setup

### Installation

**Prerequisites:**
```bash
# Python 3.9+
python --version

# Google Cloud SDK (for deployment)
gcloud --version
```

**Install ADK:**
```bash
# Install from PyPI
pip install google-adk

# Or with all extras
pip install google-adk[full]

# Install CLI globally
pip install google-adk-cli
```

**Install from Source:**
```bash
git clone https://github.com/google/adk.git
cd adk
pip install -e ".[dev]"
```

### Google Cloud Setup

**Authentication:**
```bash
# Login to Google Cloud
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable \
  aiplatform.googleapis.com \
  run.googleapis.com \
  cloudfunctions.googleapis.com \
  bigquery.googleapis.com
```

**Application Default Credentials:**
```bash
gcloud auth application-default login
```

### Environment Setup

**.env Configuration:**
```bash
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# Gemini API
GOOGLE_API_KEY=your-api-key

# Vertex AI
VERTEX_AI_LOCATION=us-central1

# Evaluation
ADK_EVAL_DATASET_PATH=./eval_datasets
ADK_EVAL_OUTPUT_PATH=./eval_results

# Deployment
ADK_DEPLOY_REGION=us-central1
ADK_DEPLOY_MIN_INSTANCES=1
ADK_DEPLOY_MAX_INSTANCES=10
```

### Project Initialization

**Create New Agent Project:**
```bash
# Basic template
adk init my-agent --template=basic

# Advanced template with tools
adk init my-agent --template=tools

# Full-featured template
adk init my-agent --template=production

# Interactive setup
adk init my-agent --interactive
```

**Project Structure:**
```
my-agent/
├── agent.py              # Agent implementation
├── tools/                # Tool definitions
│   ├── __init__.py
│   ├── search.py
│   └── actions.py
├── eval/                 # Evaluation configs
│   ├── datasets/
│   │   └── test_cases.json
│   └── config.yaml
├── tests/                # Unit tests
│   └── test_agent.py
├── config.yaml           # Agent configuration
├── requirements.txt
└── README.md
```

### Verification

**Test Installation:**
```bash
# Check version
adk --version

# Run diagnostics
adk diagnose

# Test agent
adk test --agent=./agent.py
```

**Python Test:**
```python
from google.adk import Agent, Tool
from google.adk.eval import TaskSuccessEvaluator

print("Google ADK installed successfully!")

# Test agent creation
agent = Agent(name="test", model="gemini-1.5-flash")
print(f"Created agent: {agent.name}")

# Test evaluator
evaluator = TaskSuccessEvaluator()
print("Evaluator created successfully!")
```

---

## Core Concepts

### 1. Agents

**Agent Lifecycle:**

```python
from google.adk import Agent, AgentConfig

class MyAgent(Agent):
    """Custom agent implementation"""

    def __init__(self, config: AgentConfig):
        super().__init__(config)

    async def initialize(self):
        """Initialize agent resources"""
        await self.load_tools()
        await self.setup_memory()

    async def process(self, input: dict) -> dict:
        """Process user input"""
        # 1. Parse input
        parsed = await self.parse_input(input)

        # 2. Plan actions
        plan = await self.plan(parsed)

        # 3. Execute plan
        result = await self.execute(plan)

        # 4. Format response
        response = await self.format_response(result)

        return response

    async def plan(self, parsed_input: dict) -> list:
        """Create action plan"""
        # Agent planning logic
        return plan

    async def execute(self, plan: list) -> dict:
        """Execute action plan"""
        results = []
        for action in plan:
            if action["type"] == "tool_call":
                result = await self.call_tool(
                    action["tool"],
                    action["parameters"]
                )
                results.append(result)

        return {"results": results}

    async def cleanup(self):
        """Cleanup agent resources"""
        await self.close_connections()
```

### 2. Tools

**Tool Registration and Usage:**

```python
from google.adk import Tool, ToolRegistry, Parameter
from typing import List, Dict

# Define tool
@Tool(
    name="calculator",
    description="Perform mathematical calculations",
    parameters=[
        Parameter("expression", "string", "Mathematical expression to evaluate"),
        Parameter("precision", "integer", "Decimal precision", default=2)
    ]
)
def calculator(expression: str, precision: int = 2) -> float:
    """Calculate result"""
    result = eval(expression)  # Use safe eval in production!
    return round(result, precision)

# Register with agent
registry = ToolRegistry()
registry.register(calculator)

# Tool with async
@Tool(
    name="web_search",
    description="Search the web for information",
    parameters=[
        Parameter("query", "string", "Search query"),
        Parameter("num_results", "integer", "Number of results", default=5)
    ]
)
async def web_search(query: str, num_results: int = 5) -> List[Dict]:
    """Async web search"""
    # Implement search logic
    return results

# Conditional tool execution
@Tool(
    name="send_notification",
    description="Send notification to user",
    parameters=[
        Parameter("message", "string", "Notification message"),
        Parameter("urgency", "string", "Urgency level", enum=["low", "medium", "high"])
    ],
    requires_confirmation=True  # Ask user before executing
)
async def send_notification(message: str, urgency: str = "medium") -> bool:
    """Send notification"""
    # Send logic
    return True
```

**Tool Chains:**

```python
from google.adk import ToolChain

# Create tool chain
search_and_analyze = ToolChain(
    name="search_and_analyze",
    tools=[
        web_search,
        analyze_content,
        summarize_results
    ]
)

# Execute chain
result = await search_and_analyze.execute(
    input={"query": "Latest AI research"}
)
```

### 3. Evaluation

**Evaluation Configuration:**

```python
from google.adk.eval import (
    EvaluationSuite,
    TaskSuccessEvaluator,
    ToolUsageEvaluator,
    EfficiencyEvaluator
)

# Create evaluation suite
eval_suite = EvaluationSuite(
    name="agent_evaluation",
    evaluators=[
        TaskSuccessEvaluator(
            success_criteria={
                "task_completed": True,
                "user_satisfied": True,
                "error_free": True
            }
        ),
        ToolUsageEvaluator(
            check_correct_tools=True,
            check_parameters=True,
            check_sequencing=True,
            allow_extra_calls=False
        ),
        EfficiencyEvaluator(
            max_steps=10,
            min_efficiency=0.7
        )
    ],
    dataset_path="./eval_data/test_cases.json"
)

# Run evaluation
results = await eval_suite.run(agent)

# Analyze results
print(f"Overall Score: {results.overall_score}")
print(f"Task Success Rate: {results.task_success_rate}")
print(f"Tool Usage Score: {results.tool_usage_score}")
print(f"Efficiency Score: {results.efficiency_score}")
```

**Custom Evaluators:**

```python
from google.adk.eval import BaseEvaluator, EvaluationResult

class CustomerSatisfactionEvaluator(BaseEvaluator):
    """Evaluate customer satisfaction"""

    def __init__(self, satisfaction_model=None):
        super().__init__(name="customer_satisfaction")
        self.satisfaction_model = satisfaction_model

    async def evaluate(self, trajectory: dict) -> EvaluationResult:
        """Evaluate trajectory for customer satisfaction"""

        # Extract conversation
        conversation = trajectory["messages"]

        # Analyze sentiment
        sentiment_score = await self.analyze_sentiment(conversation)

        # Check resolution
        resolution_score = await self.check_resolution(trajectory)

        # Calculate overall score
        overall_score = (sentiment_score * 0.6 + resolution_score * 0.4)

        return EvaluationResult(
            evaluator=self.name,
            score=overall_score,
            passed=overall_score >= 0.7,
            details={
                "sentiment_score": sentiment_score,
                "resolution_score": resolution_score
            }
        )

    async def analyze_sentiment(self, conversation: list) -> float:
        """Analyze conversation sentiment"""
        # Sentiment analysis logic
        return score

    async def check_resolution(self, trajectory: dict) -> float:
        """Check if issue was resolved"""
        # Resolution checking logic
        return score
```

### 4. Trajectories

**Trajectory Tracking:**

```python
from google.adk import Trajectory, TrajectoryStep

# Automatic trajectory tracking
trajectory = Trajectory(agent=agent)

async with trajectory.track():
    result = await agent.process(user_input)

# Access trajectory data
print(f"Steps taken: {len(trajectory.steps)}")
print(f"Tools used: {trajectory.tools_used}")
print(f"Total cost: ${trajectory.total_cost}")
print(f"Duration: {trajectory.duration}s")

# Analyze trajectory
for i, step in enumerate(trajectory.steps):
    print(f"\nStep {i+1}:")
    print(f"  Action: {step.action}")
    print(f"  Tool: {step.tool_name}")
    print(f"  Parameters: {step.parameters}")
    print(f"  Result: {step.result}")
    print(f"  Cost: ${step.cost}")
```

**Trajectory Analysis:**

```python
from google.adk.analysis import TrajectoryAnalyzer

analyzer = TrajectoryAnalyzer()

# Analyze trajectory
analysis = analyzer.analyze(trajectory)

print(f"Efficiency: {analysis.efficiency_score}")
print(f"Redundant steps: {analysis.redundant_steps}")
print(f"Optimal path length: {analysis.optimal_steps}")
print(f"Actual path length: {analysis.actual_steps}")

# Identify issues
if analysis.issues:
    print("\nIssues found:")
    for issue in analysis.issues:
        print(f"  - {issue.type}: {issue.description}")

# Get optimization suggestions
suggestions = analyzer.suggest_optimizations(trajectory)
for suggestion in suggestions:
    print(f"Suggestion: {suggestion}")
```

### 5. Memory Management

**Agent Memory:**

```python
from google.adk import Memory, MemoryStore

class AgentWithMemory(Agent):
    """Agent with persistent memory"""

    def __init__(self, config):
        super().__init__(config)

        # Setup memory store
        self.memory = MemoryStore(
            backend="firestore",  # or "redis", "memory"
            project=config.project_id
        )

    async def process(self, input: dict) -> dict:
        """Process with memory"""

        # Retrieve relevant memories
        context = await self.memory.retrieve(
            query=input["text"],
            top_k=5
        )

        # Include context in processing
        input["context"] = context

        result = await super().process(input)

        # Store interaction in memory
        await self.memory.store(
            key=f"interaction_{timestamp}",
            value={
                "input": input,
                "output": result,
                "timestamp": timestamp
            }
        )

        return result

# Memory retrieval strategies
class SemanticMemory(Memory):
    """Semantic memory with embeddings"""

    async def retrieve(self, query: str, top_k: int = 5) -> list:
        """Retrieve semantically similar memories"""
        query_embedding = await self.embed(query)

        similar = await self.vector_search(
            query_embedding,
            top_k=top_k
        )

        return similar
```

---

## Production-Ready Examples

### Example 1: Complete Customer Support Agent

**Scenario:** Production customer support agent with evaluation

```python
"""
Production customer support agent with Google ADK
- Multi-tool integration
- Comprehensive evaluation
- Error handling
- Logging and monitoring
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime

from google.adk import Agent, Tool, Parameter, AgentConfig
from google.adk.eval import (
    EvaluationSuite,
    TaskSuccessEvaluator,
    ToolUsageEvaluator,
    CustomerSatisfactionEvaluator
)
from google.adk.memory import MemoryStore
from google.adk.logging import setup_logging

# Setup logging
logger = setup_logging("customer_support_agent")

# ============================================================================
# TOOLS DEFINITION
# ============================================================================

@Tool(
    name="search_knowledge_base",
    description="Search the knowledge base for support articles",
    parameters=[
        Parameter("query", "string", "Search query"),
        Parameter("category", "string", "Article category", optional=True),
        Parameter("max_results", "integer", "Max results", default=5)
    ]
)
async def search_knowledge_base(
    query: str,
    category: Optional[str] = None,
    max_results: int = 5
) -> List[Dict]:
    """Search knowledge base"""
    logger.info(f"Searching KB: query={query}, category={category}")

    # Simulated KB search
    results = [
        {
            "id": "kb-001",
            "title": "How to reset password",
            "content": "To reset your password...",
            "relevance": 0.95
        },
        {
            "id": "kb-002",
            "title": "Account recovery steps",
            "content": "If you can't access your account...",
            "relevance": 0.87
        }
    ]

    return results[:max_results]

@Tool(
    name="create_support_ticket",
    description="Create a support ticket for issues requiring human review",
    parameters=[
        Parameter("title", "string", "Ticket title"),
        Parameter("description", "string", "Detailed description"),
        Parameter("priority", "string", "Priority level", enum=["low", "medium", "high", "urgent"]),
        Parameter("category", "string", "Issue category")
    ]
)
async def create_support_ticket(
    title: str,
    description: str,
    priority: str,
    category: str
) -> Dict:
    """Create support ticket"""
    logger.info(f"Creating ticket: {title} (Priority: {priority})")

    ticket = {
        "ticket_id": f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "open",
        "created_at": datetime.now().isoformat()
    }

    # Simulated ticket creation
    logger.info(f"Ticket created: {ticket['ticket_id']}")

    return ticket

@Tool(
    name="check_order_status",
    description="Check the status of a customer order",
    parameters=[
        Parameter("order_id", "string", "Order ID")
    ]
)
async def check_order_status(order_id: str) -> Dict:
    """Check order status"""
    logger.info(f"Checking order: {order_id}")

    # Simulated order lookup
    order = {
        "order_id": order_id,
        "status": "shipped",
        "tracking_number": "TRK123456789",
        "estimated_delivery": "2024-01-25",
        "items": [
            {"name": "Product A", "quantity": 1, "status": "shipped"}
        ]
    }

    return order

@Tool(
    name="process_refund",
    description="Process a refund for an order",
    parameters=[
        Parameter("order_id", "string", "Order ID"),
        Parameter("reason", "string", "Refund reason"),
        Parameter("amount", "number", "Refund amount", optional=True)
    ],
    requires_confirmation=True
)
async def process_refund(
    order_id: str,
    reason: str,
    amount: Optional[float] = None
) -> Dict:
    """Process refund"""
    logger.info(f"Processing refund for order: {order_id}")

    refund = {
        "refund_id": f"REF-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "order_id": order_id,
        "amount": amount or 99.99,
        "reason": reason,
        "status": "processing",
        "estimated_completion": "3-5 business days"
    }

    return refund

@Tool(
    name="send_email",
    description="Send email to customer",
    parameters=[
        Parameter("recipient", "string", "Customer email"),
        Parameter("subject", "string", "Email subject"),
        Parameter("body", "string", "Email body"),
        Parameter("template", "string", "Email template name", optional=True)
    ]
)
async def send_email(
    recipient: str,
    subject: str,
    body: str,
    template: Optional[str] = None
) -> Dict:
    """Send email"""
    logger.info(f"Sending email to: {recipient}")

    result = {
        "email_id": f"EMAIL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "recipient": recipient,
        "subject": subject,
        "sent_at": datetime.now().isoformat(),
        "status": "sent"
    }

    return result

# ============================================================================
# AGENT IMPLEMENTATION
# ============================================================================

class CustomerSupportAgent(Agent):
    """Production customer support agent"""

    def __init__(self):
        config = AgentConfig(
            name="customer_support",
            model="gemini-1.5-pro",
            temperature=0.3,
            max_tokens=2048,
            system_prompt="""You are a helpful customer support agent.
Your goal is to assist customers efficiently and professionally.

Guidelines:
1. Always be polite and empathetic
2. Search the knowledge base before creating tickets
3. Only escalate complex issues that require human review
4. Confirm sensitive actions (refunds, etc.) with the user
5. Provide clear, actionable solutions

You have access to tools for:
- Searching the knowledge base
- Checking order status
- Processing refunds
- Creating support tickets
- Sending emails

Use these tools wisely to help customers effectively."""
        )

        super().__init__(config)

        # Register tools
        self.register_tool(search_knowledge_base)
        self.register_tool(create_support_ticket)
        self.register_tool(check_order_status)
        self.register_tool(process_refund)
        self.register_tool(send_email)

        # Setup memory
        self.memory = MemoryStore(backend="memory")

        logger.info("Customer support agent initialized")

    async def process(self, user_input: str, user_id: str) -> Dict:
        """Process customer query"""
        logger.info(f"Processing query from user {user_id}")

        try:
            # Retrieve conversation history
            history = await self.memory.retrieve(f"user:{user_id}")

            # Build context
            context = {
                "user_input": user_input,
                "history": history,
                "user_id": user_id
            }

            # Plan actions
            plan = await self.plan(context)

            # Execute plan
            result = await self.execute(plan)

            # Store interaction
            await self.memory.store(
                f"user:{user_id}:{datetime.now().isoformat()}",
                {
                    "input": user_input,
                    "output": result,
                    "timestamp": datetime.now().isoformat()
                }
            )

            logger.info(f"Query processed successfully for user {user_id}")

            return result

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "error": True,
                "message": "I apologize, but I encountered an error. Let me create a support ticket for you.",
                "ticket": await create_support_ticket(
                    title=f"Agent error: {user_input[:50]}",
                    description=f"Error occurred: {str(e)}",
                    priority="high",
                    category="technical"
                )
            }

    async def plan(self, context: Dict) -> List[Dict]:
        """Plan agent actions"""

        user_input = context["user_input"].lower()
        plan = []

        # Determine actions based on input
        if "order" in user_input and any(word in user_input for word in ["status", "tracking", "where"]):
            plan.append({
                "action": "tool_call",
                "tool": "check_order_status",
                "parameters": self._extract_order_id(user_input)
            })

        elif "refund" in user_input or "return" in user_input:
            plan.append({
                "action": "tool_call",
                "tool": "search_knowledge_base",
                "parameters": {"query": "refund policy", "category": "returns"}
            })

        elif "password" in user_input or "login" in user_input:
            plan.append({
                "action": "tool_call",
                "tool": "search_knowledge_base",
                "parameters": {"query": user_input, "category": "account"}
            })

        else:
            # General query - search KB
            plan.append({
                "action": "tool_call",
                "tool": "search_knowledge_base",
                "parameters": {"query": user_input}
            })

        return plan

    async def execute(self, plan: List[Dict]) -> Dict:
        """Execute action plan"""

        results = []

        for action in plan:
            if action["action"] == "tool_call":
                tool_result = await self.call_tool(
                    action["tool"],
                    action["parameters"]
                )
                results.append({
                    "tool": action["tool"],
                    "result": tool_result
                })

        # Generate response based on results
        response = await self._generate_response(results)

        return {
            "response": response,
            "tool_calls": results,
            "success": True
        }

    def _extract_order_id(self, text: str) -> Dict:
        """Extract order ID from text"""
        import re
        match = re.search(r'ORD-\w+', text)
        if match:
            return {"order_id": match.group()}
        return {"order_id": "ORD-UNKNOWN"}

    async def _generate_response(self, tool_results: List[Dict]) -> str:
        """Generate final response from tool results"""

        if not tool_results:
            return "I apologize, but I couldn't find relevant information. Would you like me to create a support ticket?"

        # Combine tool results into response
        response_parts = []

        for result in tool_results:
            if result["tool"] == "search_knowledge_base":
                kb_results = result["result"]
                if kb_results:
                    response_parts.append(
                        f"I found this information: {kb_results[0]['content']}"
                    )

            elif result["tool"] == "check_order_status":
                order = result["result"]
                response_parts.append(
                    f"Your order {order['order_id']} is {order['status']}. "
                    f"Tracking number: {order['tracking_number']}. "
                    f"Estimated delivery: {order['estimated_delivery']}."
                )

        return " ".join(response_parts)

# ============================================================================
# EVALUATION SETUP
# ============================================================================

def create_evaluation_suite() -> EvaluationSuite:
    """Create comprehensive evaluation suite"""

    return EvaluationSuite(
        name="customer_support_eval",
        evaluators=[
            TaskSuccessEvaluator(
                success_criteria={
                    "provided_solution": True,
                    "used_correct_tools": True,
                    "response_quality": "high"
                }
            ),
            ToolUsageEvaluator(
                check_correct_tools=True,
                check_parameters=True,
                check_sequencing=True
            ),
            CustomerSatisfactionEvaluator()
        ]
    )

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Main execution"""

    # Initialize agent
    agent = CustomerSupportAgent()

    # Test queries
    test_cases = [
        {
            "user_id": "USER001",
            "query": "I need to check the status of my order ORD-123456",
            "expected_tools": ["check_order_status"]
        },
        {
            "user_id": "USER002",
            "query": "How do I reset my password?",
            "expected_tools": ["search_knowledge_base"]
        },
        {
            "user_id": "USER003",
            "query": "I want to return my order ORD-789012",
            "expected_tools": ["search_knowledge_base", "process_refund"]
        }
    ]

    print("="*80)
    print("CUSTOMER SUPPORT AGENT EVALUATION")
    print("="*80 + "\n")

    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i+1}:")
        print(f"Query: {test_case['query']}")

        result = await agent.process(
            test_case["query"],
            test_case["user_id"]
        )

        print(f"Response: {result['response']}")
        print(f"Tools Used: {[r['tool'] for r in result['tool_calls']]}")
        print(f"Expected Tools: {test_case['expected_tools']}")
        print(f"Success: {result['success']}")

    # Run evaluation
    print("\n" + "="*80)
    print("RUNNING EVALUATION")
    print("="*80 + "\n")

    eval_suite = create_evaluation_suite()
    eval_results = await eval_suite.run(agent)

    print(f"Overall Score: {eval_results.overall_score:.2f}")
    print(f"Task Success Rate: {eval_results.task_success_rate:.2%}")
    print(f"Tool Usage Score: {eval_results.tool_usage_score:.2f}")

    print("\n" + "="*80)

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 2: Research Agent with Multi-Step Planning

**Scenario:** Research agent that plans and executes complex research tasks

```python
"""
Research agent with advanced planning and execution
"""

import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass

from google.adk import Agent, Tool, Parameter, AgentConfig
from google.adk.planning import HierarchicalPlanner
from google.adk.eval import TrajectoryEvaluator, EfficiencyEvaluator

# ============================================================================
# RESEARCH TOOLS
# ============================================================================

@Tool(
    name="web_search",
    description="Search the web for information",
    parameters=[
        Parameter("query", "string", "Search query"),
        Parameter("num_results", "integer", "Number of results", default=10)
    ]
)
async def web_search(query: str, num_results: int = 10) -> List[Dict]:
    """Web search"""
    # Simulated search results
    return [
        {
            "title": f"Result {i+1} for {query}",
            "url": f"https://example.com/{i}",
            "snippet": f"Information about {query}..."
        }
        for i in range(num_results)
    ]

@Tool(
    name="scrape_webpage",
    description="Extract content from a webpage",
    parameters=[
        Parameter("url", "string", "Webpage URL")
    ]
)
async def scrape_webpage(url: str) -> Dict:
    """Scrape webpage"""
    return {
        "url": url,
        "title": "Example Page",
        "content": "Detailed content from the page...",
        "extracted_at": "2024-01-20T10:00:00Z"
    }

@Tool(
    name="extract_key_facts",
    description="Extract key facts from text using LLM",
    parameters=[
        Parameter("text", "string", "Text to analyze"),
        Parameter("focus", "string", "Focus area", optional=True)
    ]
)
async def extract_key_facts(text: str, focus: Optional[str] = None) -> List[str]:
    """Extract key facts"""
    # Simulated fact extraction
    return [
        "Key fact 1 from the text",
        "Key fact 2 about the topic",
        "Key fact 3 related to the focus"
    ]

@Tool(
    name="summarize_sources",
    description="Summarize multiple sources into a coherent report",
    parameters=[
        Parameter("sources", "array", "List of source texts"),
        Parameter("format", "string", "Summary format", enum=["brief", "detailed", "academic"])
    ]
)
async def summarize_sources(sources: List[str], format: str = "detailed") -> str:
    """Summarize sources"""
    return f"Comprehensive {format} summary of all provided sources..."

@Tool(
    name="cite_sources",
    description="Generate citations for sources",
    parameters=[
        Parameter("sources", "array", "List of sources to cite"),
        Parameter("style", "string", "Citation style", enum=["APA", "MLA", "Chicago"])
    ]
)
async def cite_sources(sources: List[Dict], style: str = "APA") -> List[str]:
    """Generate citations"""
    return [f"{style} citation for source {i+1}" for i in range(len(sources))]

# ============================================================================
# RESEARCH AGENT
# ============================================================================

@dataclass
class ResearchTask:
    """Research task definition"""
    topic: str
    depth: str  # "shallow", "medium", "deep"
    required_sources: int
    focus_areas: List[str]
    output_format: str

class ResearchAgent(Agent):
    """Advanced research agent with hierarchical planning"""

    def __init__(self):
        config = AgentConfig(
            name="research_agent",
            model="gemini-1.5-pro",
            temperature=0.2,
            max_tokens=4096,
            system_prompt="""You are an advanced research agent.
Your goal is to conduct thorough research on given topics.

Research Process:
1. Break down the research topic into sub-questions
2. Search for relevant information
3. Extract and analyze key facts
4. Synthesize findings into a comprehensive report
5. Cite all sources properly

Always ensure accuracy and provide well-structured outputs."""
        )

        super().__init__(config)

        # Register tools
        self.register_tool(web_search)
        self.register_tool(scrape_webpage)
        self.register_tool(extract_key_facts)
        self.register_tool(summarize_sources)
        self.register_tool(cite_sources)

        # Setup planner
        self.planner = HierarchicalPlanner()

    async def research(self, task: ResearchTask) -> Dict:
        """Execute research task"""

        print(f"\n{'='*80}")
        print(f"RESEARCH TASK: {task.topic}")
        print(f"{'='*80}\n")

        # Phase 1: Planning
        print("Phase 1: Creating research plan...")
        plan = await self.create_research_plan(task)
        print(f"Plan created with {len(plan)} steps\n")

        # Phase 2: Information Gathering
        print("Phase 2: Gathering information...")
        sources = await self.gather_information(task, plan)
        print(f"Gathered {len(sources)} sources\n")

        # Phase 3: Analysis
        print("Phase 3: Analyzing information...")
        facts = await self.analyze_information(sources, task.focus_areas)
        print(f"Extracted {len(facts)} key facts\n")

        # Phase 4: Synthesis
        print("Phase 4: Synthesizing report...")
        report = await self.synthesize_report(facts, sources, task)
        print("Report completed\n")

        # Phase 5: Citation
        print("Phase 5: Generating citations...")
        citations = await cite_sources(sources, "APA")
        print(f"Generated {len(citations)} citations\n")

        return {
            "topic": task.topic,
            "report": report,
            "sources": sources,
            "facts": facts,
            "citations": citations,
            "plan": plan
        }

    async def create_research_plan(self, task: ResearchTask) -> List[Dict]:
        """Create hierarchical research plan"""

        # Decompose topic into sub-questions
        sub_questions = self._decompose_topic(task.topic, task.focus_areas)

        plan = []
        for i, question in enumerate(sub_questions):
            plan.append({
                "step": i + 1,
                "action": "search",
                "query": question,
                "depth": task.depth
            })

        return plan

    async def gather_information(
        self,
        task: ResearchTask,
        plan: List[Dict]
    ) -> List[Dict]:
        """Gather information according to plan"""

        sources = []

        for step in plan:
            # Search for information
            search_results = await web_search(
                step["query"],
                num_results=task.required_sources
            )

            # Scrape top results
            for result in search_results[:3]:
                content = await scrape_webpage(result["url"])
                sources.append({
                    "url": result["url"],
                    "title": result["title"],
                    "content": content["content"],
                    "query": step["query"]
                })

        return sources

    async def analyze_information(
        self,
        sources: List[Dict],
        focus_areas: List[str]
    ) -> List[str]:
        """Analyze gathered information"""

        all_facts = []

        for source in sources:
            facts = await extract_key_facts(
                source["content"],
                focus=", ".join(focus_areas)
            )
            all_facts.extend(facts)

        # Deduplicate and filter
        unique_facts = list(set(all_facts))

        return unique_facts

    async def synthesize_report(
        self,
        facts: List[str],
        sources: List[Dict],
        task: ResearchTask
    ) -> str:
        """Synthesize final report"""

        # Prepare source texts
        source_texts = [s["content"] for s in sources]

        # Generate summary
        summary = await summarize_sources(
            source_texts,
            format=task.output_format
        )

        # Structure report
        report = f"""
# Research Report: {task.topic}

## Executive Summary
{summary}

## Key Findings
{self._format_facts(facts)}

## Detailed Analysis
{self._create_analysis(facts, task.focus_areas)}

## Conclusion
{self._generate_conclusion(facts)}
"""

        return report

    def _decompose_topic(self, topic: str, focus_areas: List[str]) -> List[str]:
        """Decompose topic into sub-questions"""
        sub_questions = [
            f"What is {topic}?",
            f"What are the key aspects of {topic}?",
            f"What are recent developments in {topic}?"
        ]

        for area in focus_areas:
            sub_questions.append(f"How does {topic} relate to {area}?")

        return sub_questions

    def _format_facts(self, facts: List[str]) -> str:
        """Format facts as bullet points"""
        return "\n".join(f"- {fact}" for fact in facts[:10])

    def _create_analysis(self, facts: List[str], focus_areas: List[str]) -> str:
        """Create detailed analysis"""
        analysis = []
        for area in focus_areas:
            relevant_facts = [f for f in facts if area.lower() in f.lower()]
            if relevant_facts:
                analysis.append(f"\n### {area}")
                analysis.append(self._format_facts(relevant_facts))

        return "\n".join(analysis)

    def _generate_conclusion(self, facts: List[str]) -> str:
        """Generate conclusion"""
        return "Based on the research findings, we can conclude that this topic is multi-faceted and requires continued investigation."

# ============================================================================
# EVALUATION
# ============================================================================

async def evaluate_research_agent():
    """Evaluate research agent performance"""

    agent = ResearchAgent()

    # Define research tasks
    tasks = [
        ResearchTask(
            topic="Artificial Intelligence in Healthcare",
            depth="medium",
            required_sources=5,
            focus_areas=["diagnostics", "patient care", "ethics"],
            output_format="detailed"
        ),
        ResearchTask(
            topic="Climate Change Mitigation Strategies",
            depth="deep",
            required_sources=8,
            focus_areas=["renewable energy", "policy", "technology"],
            output_format="academic"
        )
    ]

    # Run research tasks
    results = []
    for task in tasks:
        result = await agent.research(task)
        results.append(result)

    # Evaluate with trajectory analysis
    evaluator = TrajectoryEvaluator(
        max_steps=20,
        efficiency_threshold=0.7
    )

    efficiency_eval = EfficiencyEvaluator(
        optimal_steps={"shallow": 5, "medium": 10, "deep": 15}
    )

    print("\n" + "="*80)
    print("EVALUATION RESULTS")
    print("="*80 + "\n")

    for i, result in enumerate(results):
        print(f"Task {i+1}: {result['topic']}")
        print(f"  Sources gathered: {len(result['sources'])}")
        print(f"  Facts extracted: {len(result['facts'])}")
        print(f"  Plan steps: {len(result['plan'])}")
        print(f"  Report length: {len(result['report'])} characters")
        print()

async def main():
    await evaluate_research_agent()

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 3: Tool Usage Evaluation Deep Dive

**Scenario:** Comprehensive tool usage evaluation

```python
"""
Comprehensive tool usage evaluation with Google ADK
"""

import asyncio
from typing import Dict, List
from dataclasses import dataclass

from google.adk import Agent, Tool, Parameter
from google.adk.eval import ToolUsageEvaluator, EvaluationResult

# ============================================================================
# TOOL USAGE PATTERNS
# ============================================================================

@dataclass
class ToolUsagePattern:
    """Expected tool usage pattern"""
    scenario: str
    expected_tools: List[str]
    expected_sequence: List[str]
    expected_parameters: Dict[str, Dict]
    max_calls: int
    allow_redundant: bool = False

# ============================================================================
# CUSTOM TOOL USAGE EVALUATOR
# ============================================================================

class AdvancedToolUsageEvaluator:
    """Advanced tool usage evaluation"""

    def __init__(self):
        self.patterns = {}

    def register_pattern(self, name: str, pattern: ToolUsagePattern):
        """Register expected usage pattern"""
        self.patterns[name] = pattern

    async def evaluate(self, trajectory: Dict, pattern_name: str) -> EvaluationResult:
        """Evaluate tool usage against expected pattern"""

        pattern = self.patterns.get(pattern_name)
        if not pattern:
            raise ValueError(f"Unknown pattern: {pattern_name}")

        tool_calls = trajectory.get("tool_calls", [])

        # Evaluate different aspects
        scores = {
            "correct_tools": self._evaluate_tool_selection(tool_calls, pattern),
            "correct_sequence": self._evaluate_sequence(tool_calls, pattern),
            "correct_parameters": self._evaluate_parameters(tool_calls, pattern),
            "efficiency": self._evaluate_efficiency(tool_calls, pattern),
            "redundancy": self._evaluate_redundancy(tool_calls, pattern)
        }

        # Calculate overall score
        overall = sum(scores.values()) / len(scores)

        return EvaluationResult(
            evaluator="advanced_tool_usage",
            score=overall,
            passed=overall >= 0.7,
            details=scores
        )

    def _evaluate_tool_selection(
        self,
        tool_calls: List[Dict],
        pattern: ToolUsagePattern
    ) -> float:
        """Evaluate if correct tools were used"""

        called_tools = set(call["tool"] for call in tool_calls)
        expected_tools = set(pattern.expected_tools)

        if not expected_tools:
            return 1.0

        # Check if all expected tools were called
        missing = expected_tools - called_tools
        extra = called_tools - expected_tools

        # Score based on precision and recall
        if not called_tools:
            return 0.0

        precision = len(expected_tools & called_tools) / len(called_tools)
        recall = len(expected_tools & called_tools) / len(expected_tools)

        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        return f1_score

    def _evaluate_sequence(
        self,
        tool_calls: List[Dict],
        pattern: ToolUsagePattern
    ) -> float:
        """Evaluate if tools were called in correct sequence"""

        if not pattern.expected_sequence:
            return 1.0

        actual_sequence = [call["tool"] for call in tool_calls]

        # Find longest common subsequence
        lcs_length = self._lcs_length(pattern.expected_sequence, actual_sequence)

        # Calculate sequence similarity
        max_length = max(len(pattern.expected_sequence), len(actual_sequence))
        if max_length == 0:
            return 1.0

        return lcs_length / max_length

    def _evaluate_parameters(
        self,
        tool_calls: List[Dict],
        pattern: ToolUsagePattern
    ) -> float:
        """Evaluate if correct parameters were used"""

        if not pattern.expected_parameters:
            return 1.0

        scores = []

        for call in tool_calls:
            tool_name = call["tool"]
            if tool_name not in pattern.expected_parameters:
                continue

            expected_params = pattern.expected_parameters[tool_name]
            actual_params = call.get("parameters", {})

            # Check each expected parameter
            param_scores = []
            for param_name, expected_value in expected_params.items():
                if param_name not in actual_params:
                    param_scores.append(0.0)
                elif expected_value == "*":  # Any value acceptable
                    param_scores.append(1.0)
                elif actual_params[param_name] == expected_value:
                    param_scores.append(1.0)
                else:
                    param_scores.append(0.5)  # Wrong value

            if param_scores:
                scores.append(sum(param_scores) / len(param_scores))

        return sum(scores) / len(scores) if scores else 1.0

    def _evaluate_efficiency(
        self,
        tool_calls: List[Dict],
        pattern: ToolUsagePattern
    ) -> float:
        """Evaluate efficiency (not too many calls)"""

        num_calls = len(tool_calls)

        if num_calls == 0:
            return 0.0

        if num_calls <= pattern.max_calls:
            return 1.0

        # Penalize excess calls
        excess = num_calls - pattern.max_calls
        penalty = excess / pattern.max_calls

        return max(0.0, 1.0 - penalty)

    def _evaluate_redundancy(
        self,
        tool_calls: List[Dict],
        pattern: ToolUsagePattern
    ) -> float:
        """Evaluate redundant tool calls"""

        if pattern.allow_redundant:
            return 1.0

        # Check for duplicate calls with same parameters
        seen = set()
        redundant = 0

        for call in tool_calls:
            key = (call["tool"], frozenset(call.get("parameters", {}).items()))
            if key in seen:
                redundant += 1
            seen.add(key)

        if len(tool_calls) == 0:
            return 1.0

        redundancy_ratio = redundant / len(tool_calls)
        return 1.0 - redundancy_ratio

    def _lcs_length(self, seq1: List, seq2: List) -> int:
        """Calculate longest common subsequence length"""
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        return dp[m][n]

# ============================================================================
# EXAMPLE: E-COMMERCE AGENT EVALUATION
# ============================================================================

async def evaluate_ecommerce_agent():
    """Evaluate e-commerce agent tool usage"""

    evaluator = AdvancedToolUsageEvaluator()

    # Register expected patterns
    evaluator.register_pattern(
        "order_inquiry",
        ToolUsagePattern(
            scenario="Customer asks about order status",
            expected_tools=["search_order", "get_order_details"],
            expected_sequence=["search_order", "get_order_details"],
            expected_parameters={
                "search_order": {"query": "*"},
                "get_order_details": {"order_id": "*"}
            },
            max_calls=3,
            allow_redundant=False
        )
    )

    evaluator.register_pattern(
        "product_recommendation",
        ToolUsagePattern(
            scenario="Customer asks for product recommendations",
            expected_tools=["get_user_preferences", "search_products", "filter_products"],
            expected_sequence=["get_user_preferences", "search_products", "filter_products"],
            expected_parameters={
                "search_products": {"category": "*"},
                "filter_products": {"max_results": "*"}
            },
            max_calls=5,
            allow_redundant=False
        )
    )

    evaluator.register_pattern(
        "refund_process",
        ToolUsagePattern(
            scenario="Customer requests refund",
            expected_tools=["verify_order", "check_refund_eligibility", "process_refund"],
            expected_sequence=["verify_order", "check_refund_eligibility", "process_refund"],
            expected_parameters={
                "process_refund": {"order_id": "*", "reason": "*"}
            },
            max_calls=4,
            allow_redundant=False
        )
    )

    # Test trajectories
    test_trajectories = [
        {
            "name": "Order Inquiry - Optimal",
            "pattern": "order_inquiry",
            "tool_calls": [
                {"tool": "search_order", "parameters": {"query": "ORD-123"}},
                {"tool": "get_order_details", "parameters": {"order_id": "ORD-123"}}
            ]
        },
        {
            "name": "Order Inquiry - Redundant",
            "pattern": "order_inquiry",
            "tool_calls": [
                {"tool": "search_order", "parameters": {"query": "ORD-123"}},
                {"tool": "search_order", "parameters": {"query": "ORD-123"}},  # Redundant
                {"tool": "get_order_details", "parameters": {"order_id": "ORD-123"}}
            ]
        },
        {
            "name": "Order Inquiry - Wrong Sequence",
            "pattern": "order_inquiry",
            "tool_calls": [
                {"tool": "get_order_details", "parameters": {"order_id": "ORD-123"}},  # Should be second
                {"tool": "search_order", "parameters": {"query": "ORD-123"}}
            ]
        },
        {
            "name": "Product Recommendation - Optimal",
            "pattern": "product_recommendation",
            "tool_calls": [
                {"tool": "get_user_preferences", "parameters": {}},
                {"tool": "search_products", "parameters": {"category": "electronics"}},
                {"tool": "filter_products", "parameters": {"max_results": 10}}
            ]
        }
    ]

    print("="*80)
    print("TOOL USAGE EVALUATION RESULTS")
    print("="*80 + "\n")

    for trajectory in test_trajectories:
        result = await evaluator.evaluate(trajectory, trajectory["pattern"])

        print(f"Test: {trajectory['name']}")
        print(f"  Overall Score: {result.score:.2f}")
        print(f"  Passed: {result.passed}")
        print(f"  Details:")
        for metric, score in result.details.items():
            print(f"    {metric}: {score:.2f}")
        print()

async def main():
    await evaluate_ecommerce_agent()

if __name__ == "__main__":
    asyncio.run(main())
```

(Continued in next message due to length...)

### Example 4: CLI-Based Evaluation Workflow

**Scenario:** Complete CLI workflow for agent evaluation

```bash
#!/bin/bash
# Google ADK CLI Evaluation Workflow

# ============================================================================
# SETUP
# ============================================================================

# Initialize project
adk init customer-support-agent --template=production

cd customer-support-agent

# Install dependencies
pip install -r requirements.txt

# ============================================================================
# CONFIGURATION
# ============================================================================

# Create evaluation configuration
cat > eval_config.yaml << 'EOF'
evaluation:
  name: customer_support_eval
  agent: ./agent.py

  datasets:
    - name: basic_queries
      path: ./eval/datasets/basic_queries.json
      weight: 0.3

    - name: complex_scenarios
      path: ./eval/datasets/complex_scenarios.json
      weight: 0.5

    - name: edge_cases
      path: ./eval/datasets/edge_cases.json
      weight: 0.2

  evaluators:
    - name: task_success
      type: TaskSuccessEvaluator
      config:
        success_criteria:
          task_completed: true
          user_satisfied: true
          error_free: true

    - name: tool_usage
      type: ToolUsageEvaluator
      config:
        check_correct_tools: true
        check_parameters: true
        check_sequencing: true
        allow_extra_calls: false

    - name: efficiency
      type: EfficiencyEvaluator
      config:
        max_steps: 10
        min_efficiency: 0.7

    - name: customer_satisfaction
      type: CustomEvaluator
      module: ./evaluators/customer_satisfaction.py
      class: CustomerSatisfactionEvaluator

  output:
    format: json
    path: ./eval_results
    include_trajectories: true
    include_details: true

  reporting:
    generate_html: true
    generate_csv: true
    send_email: false
EOF

# ============================================================================
# CREATE EVALUATION DATASETS
# ============================================================================

# Basic queries dataset
cat > eval/datasets/basic_queries.json << 'EOF'
[
  {
    "id": "basic_001",
    "input": "What is your return policy?",
    "expected_tools": ["search_knowledge_base"],
    "expected_outcome": "Clear explanation of return policy"
  },
  {
    "id": "basic_002",
    "input": "How do I track my order?",
    "expected_tools": ["search_knowledge_base"],
    "expected_outcome": "Instructions for order tracking"
  },
  {
    "id": "basic_003",
    "input": "I need to change my shipping address",
    "expected_tools": ["search_knowledge_base", "update_order"],
    "expected_outcome": "Address update confirmation"
  }
]
EOF

# Complex scenarios dataset
cat > eval/datasets/complex_scenarios.json << 'EOF'
[
  {
    "id": "complex_001",
    "input": "I received the wrong item and need a refund",
    "expected_tools": ["verify_order", "check_refund_eligibility", "process_refund"],
    "expected_sequence": ["verify_order", "check_refund_eligibility", "process_refund"],
    "expected_outcome": "Refund processed successfully"
  },
  {
    "id": "complex_002",
    "input": "My order is late and I need it urgently",
    "expected_tools": ["check_order_status", "check_shipping_options", "escalate_ticket"],
    "expected_outcome": "Issue escalated with expedited shipping arranged"
  }
]
EOF

# ============================================================================
# RUN EVALUATIONS
# ============================================================================

echo "Running evaluations..."

# Run full evaluation suite
adk eval --config eval_config.yaml --verbose

# Run specific evaluator
adk eval --config eval_config.yaml --evaluator task_success

# Run on specific dataset
adk eval --config eval_config.yaml --dataset basic_queries

# Run with parallelization
adk eval --config eval_config.yaml --parallel --workers 4

# ============================================================================
# ANALYZE RESULTS
# ============================================================================

# View results summary
adk results summary --path ./eval_results

# View detailed results
adk results detail --path ./eval_results --format table

# View specific test case
adk results show --id basic_001 --path ./eval_results

# Compare with baseline
adk results compare \
  --baseline ./eval_results/baseline \
  --current ./eval_results/latest

# ============================================================================
# GENERATE REPORTS
# ============================================================================

# Generate HTML report
adk report generate \
  --input ./eval_results \
  --output ./reports/eval_report.html \
  --format html

# Generate CSV export
adk report export \
  --input ./eval_results \
  --output ./reports/metrics.csv \
  --format csv

# Generate comparison report
adk report compare \
  --baseline ./eval_results/v1.0 \
  --current ./eval_results/v1.1 \
  --output ./reports/comparison.html

# ============================================================================
# CONTINUOUS EVALUATION
# ============================================================================

# Run evaluation on schedule
adk eval schedule \
  --config eval_config.yaml \
  --cron "0 */6 * * *" \
  --notify team@company.com

# Run evaluation in CI/CD
adk eval ci \
  --config eval_config.yaml \
  --fail-threshold 0.7 \
  --export-metrics ./metrics.json

# ============================================================================
# BENCHMARKING
# ============================================================================

# Benchmark agent performance
adk benchmark \
  --agent ./agent.py \
  --scenarios ./benchmarks/scenarios.json \
  --metrics latency,cost,accuracy

# Compare with other agents
adk benchmark compare \
  --agents ./agent_v1.py,./agent_v2.py \
  --scenarios ./benchmarks/scenarios.json

# ============================================================================
# DEPLOYMENT WITH EVALUATION
# ============================================================================

# Deploy with evaluation gates
adk deploy \
  --agent ./agent.py \
  --target cloud-run \
  --region us-central1 \
  --require-eval \
  --eval-threshold 0.8

# Deploy canary with evaluation
adk deploy canary \
  --agent ./agent.py \
  --traffic-split 10 \
  --eval-duration 1h \
  --auto-rollback

echo "Evaluation workflow completed!"
```

### Example 5: Multi-Modal Agent Evaluation

**Scenario:** Agent that handles text and images

```python
"""
Multi-modal agent evaluation with Google ADK
"""

import asyncio
from typing import Dict, List, Union
import base64

from google.adk import Agent, Tool, Parameter, AgentConfig
from google.adk.multimodal import ImageInput, TextInput
from google.adk.eval import MultiModalEvaluator

# ============================================================================
# MULTI-MODAL TOOLS
# ============================================================================

@Tool(
    name="analyze_image",
    description="Analyze an image and extract information",
    parameters=[
        Parameter("image", "image", "Image to analyze"),
        Parameter("analysis_type", "string", "Type of analysis",
                 enum=["objects", "text", "scene", "faces"])
    ]
)
async def analyze_image(image: bytes, analysis_type: str) -> Dict:
    """Analyze image"""
    # Simulated image analysis
    return {
        "analysis_type": analysis_type,
        "results": {
            "objects": ["person", "desk", "computer"],
            "confidence": 0.95,
            "description": "A person working at a desk with a computer"
        }
    }

@Tool(
    name="extract_text_from_image",
    description="Extract text from an image using OCR",
    parameters=[
        Parameter("image", "image", "Image containing text")
    ]
)
async def extract_text_from_image(image: bytes) -> Dict:
    """OCR extraction"""
    return {
        "text": "Extracted text from the image",
        "confidence": 0.92,
        "language": "en"
    }

@Tool(
    name="compare_images",
    description="Compare two images for similarity",
    parameters=[
        Parameter("image1", "image", "First image"),
        Parameter("image2", "image", "Second image")
    ]
)
async def compare_images(image1: bytes, image2: bytes) -> Dict:
    """Compare images"""
    return {
        "similarity": 0.85,
        "differences": ["lighting", "angle"],
        "same_object": True
    }

@Tool(
    name="generate_image_description",
    description="Generate detailed description of an image",
    parameters=[
        Parameter("image", "image", "Image to describe"),
        Parameter("detail_level", "string", "Level of detail",
                 enum=["brief", "detailed", "comprehensive"])
    ]
)
async def generate_image_description(
    image: bytes,
    detail_level: str = "detailed"
) -> str:
    """Generate description"""
    return f"{detail_level.capitalize()} description: This image shows..."

# ============================================================================
# MULTI-MODAL AGENT
# ============================================================================

class MultiModalAssistant(Agent):
    """Agent that handles both text and images"""

    def __init__(self):
        config = AgentConfig(
            name="multimodal_assistant",
            model="gemini-1.5-pro-vision",  # Vision-capable model
            temperature=0.3,
            max_tokens=2048,
            system_prompt="""You are a multi-modal AI assistant.
You can process both text and images to help users.

For images, you can:
- Analyze content and objects
- Extract text (OCR)
- Compare images
- Generate descriptions

Always provide clear, accurate responses based on the content."""
        )

        super().__init__(config)

        # Register tools
        self.register_tool(analyze_image)
        self.register_tool(extract_text_from_image)
        self.register_tool(compare_images)
        self.register_tool(generate_image_description)

    async def process_multimodal(
        self,
        text: str,
        images: List[bytes] = None
    ) -> Dict:
        """Process multi-modal input"""

        # Determine intent from text
        intent = self._determine_intent(text, images)

        # Execute appropriate tools
        if intent == "analyze":
            results = await self._analyze_images(images)
        elif intent == "extract_text":
            results = await self._extract_text(images)
        elif intent == "compare":
            results = await self._compare_images(images)
        elif intent == "describe":
            results = await self._describe_images(images)
        else:
            results = {"error": "Could not determine intent"}

        # Generate response
        response = await self._generate_response(text, results)

        return {
            "response": response,
            "tool_results": results,
            "intent": intent
        }

    def _determine_intent(self, text: str, images: List[bytes]) -> str:
        """Determine user intent"""
        text_lower = text.lower()

        if "compare" in text_lower:
            return "compare"
        elif "text" in text_lower or "read" in text_lower:
            return "extract_text"
        elif "describe" in text_lower or "what" in text_lower:
            return "describe"
        else:
            return "analyze"

    async def _analyze_images(self, images: List[bytes]) -> List[Dict]:
        """Analyze images"""
        results = []
        for image in images:
            analysis = await analyze_image(image, "objects")
            results.append(analysis)
        return results

    async def _extract_text(self, images: List[bytes]) -> List[Dict]:
        """Extract text from images"""
        results = []
        for image in images:
            text = await extract_text_from_image(image)
            results.append(text)
        return results

    async def _compare_images(self, images: List[bytes]) -> Dict:
        """Compare images"""
        if len(images) < 2:
            return {"error": "Need at least 2 images to compare"}
        return await compare_images(images[0], images[1])

    async def _describe_images(self, images: List[bytes]) -> List[str]:
        """Describe images"""
        results = []
        for image in images:
            description = await generate_image_description(image, "detailed")
            results.append(description)
        return results

    async def _generate_response(self, query: str, results: Dict) -> str:
        """Generate natural language response"""
        # Use LLM to generate natural response
        return f"Based on the analysis: {results}"

# ============================================================================
# MULTI-MODAL EVALUATION
# ============================================================================

class MultiModalEvaluationSuite:
    """Evaluation suite for multi-modal agents"""

    async def evaluate(self, agent: MultiModalAssistant) -> Dict:
        """Run comprehensive evaluation"""

        test_cases = self._create_test_cases()

        results = {
            "total": len(test_cases),
            "passed": 0,
            "failed": 0,
            "details": []
        }

        for test_case in test_cases:
            result = await self._evaluate_case(agent, test_case)
            results["details"].append(result)

            if result["passed"]:
                results["passed"] += 1
            else:
                results["failed"] += 1

        results["pass_rate"] = results["passed"] / results["total"]

        return results

    def _create_test_cases(self) -> List[Dict]:
        """Create test cases"""
        return [
            {
                "id": "mm_001",
                "text": "What objects are in this image?",
                "images": [self._load_test_image("test1.jpg")],
                "expected_tools": ["analyze_image"],
                "expected_intent": "analyze"
            },
            {
                "id": "mm_002",
                "text": "Extract the text from this document",
                "images": [self._load_test_image("document.jpg")],
                "expected_tools": ["extract_text_from_image"],
                "expected_intent": "extract_text"
            },
            {
                "id": "mm_003",
                "text": "Compare these two images",
                "images": [
                    self._load_test_image("image1.jpg"),
                    self._load_test_image("image2.jpg")
                ],
                "expected_tools": ["compare_images"],
                "expected_intent": "compare"
            },
            {
                "id": "mm_004",
                "text": "Describe what's happening in this picture",
                "images": [self._load_test_image("scene.jpg")],
                "expected_tools": ["generate_image_description"],
                "expected_intent": "describe"
            }
        ]

    def _load_test_image(self, filename: str) -> bytes:
        """Load test image"""
        # Simulated image loading
        return b"fake_image_data"

    async def _evaluate_case(
        self,
        agent: MultiModalAssistant,
        test_case: Dict
    ) -> Dict:
        """Evaluate single test case"""

        # Run agent
        result = await agent.process_multimodal(
            test_case["text"],
            test_case["images"]
        )

        # Check results
        correct_intent = result["intent"] == test_case["expected_intent"]

        tools_used = set()
        for tool_result in result.get("tool_results", []):
            if isinstance(tool_result, list):
                tools_used.update(tr.get("tool") for tr in tool_result if "tool" in tr)

        correct_tools = tools_used == set(test_case["expected_tools"])

        passed = correct_intent and correct_tools

        return {
            "test_id": test_case["id"],
            "passed": passed,
            "correct_intent": correct_intent,
            "correct_tools": correct_tools,
            "details": {
                "expected_intent": test_case["expected_intent"],
                "actual_intent": result["intent"],
                "expected_tools": test_case["expected_tools"],
                "actual_tools": list(tools_used)
            }
        }

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Main execution"""

    print("="*80)
    print("MULTI-MODAL AGENT EVALUATION")
    print("="*80 + "\n")

    # Initialize agent
    agent = MultiModalAssistant()

    # Run evaluation
    eval_suite = MultiModalEvaluationSuite()
    results = await eval_suite.evaluate(agent)

    # Print results
    print(f"Total Test Cases: {results['total']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Pass Rate: {results['pass_rate']:.1%}\n")

    print("Detailed Results:")
    for detail in results["details"]:
        status = "PASS" if detail["passed"] else "FAIL"
        print(f"\n[{status}] Test {detail['test_id']}:")
        print(f"  Correct Intent: {detail['correct_intent']}")
        print(f"  Correct Tools: {detail['correct_tools']}")
        print(f"  Expected: {detail['details']['expected_intent']} / {detail['details']['expected_tools']}")
        print(f"  Actual: {detail['details']['actual_intent']} / {detail['details']['actual_tools']}")

if __name__ == "__main__":
    asyncio.run(main())
```

(Continued in next message due to length limit...)

### Example 6: Production Monitoring and Alerting

**Scenario:** Production agent with comprehensive monitoring

```python
"""
Production monitoring for Google ADK agents
"""

import asyncio
from typing import Dict, List
from datetime import datetime, timedelta

from google.adk import Agent
from google.adk.monitoring import Monitor, Alert, MetricCollector
from google.cloud import monitoring_v3
import logging

class ProductionMonitor:
    """Production monitoring for agents"""

    def __init__(self, agent: Agent, project_id: str):
        self.agent = agent
        self.project_id = project_id

        # Setup Cloud Monitoring client
        self.monitoring_client = monitoring_v3.MetricServiceClient()

        # Setup metric collector
        self.metrics = MetricCollector()

        # Setup alerting
        self.alerts = []

        # Logger
        self.logger = logging.getLogger(__name__)

    async def monitor_agent(self, duration_hours: int = 24):
        """Monitor agent for specified duration"""

        end_time = datetime.now() + timedelta(hours=duration_hours)

        while datetime.now() < end_time:
            # Collect metrics
            metrics = await self.collect_metrics()

            # Check thresholds
            await self.check_thresholds(metrics)

            # Log metrics to Cloud Monitoring
            await self.log_metrics(metrics)

            # Wait before next collection
            await asyncio.sleep(60)  # Collect every minute

    async def collect_metrics(self) -> Dict:
        """Collect agent metrics"""

        return {
            "timestamp": datetime.now().isoformat(),
            "request_count": self.metrics.get("request_count"),
            "success_rate": self.metrics.get("success_rate"),
            "avg_latency": self.metrics.get("avg_latency"),
            "error_rate": self.metrics.get("error_rate"),
            "tool_usage": self.metrics.get("tool_usage"),
            "cost": self.metrics.get("cost")
        }

    async def check_thresholds(self, metrics: Dict):
        """Check if metrics exceed thresholds"""

        # Check success rate
        if metrics["success_rate"] < 0.95:
            await self.create_alert(
                "Low Success Rate",
                f"Success rate dropped to {metrics['success_rate']:.2%}",
                "warning"
            )

        # Check latency
        if metrics["avg_latency"] > 5.0:
            await self.create_alert(
                "High Latency",
                f"Average latency is {metrics['avg_latency']:.2f}s",
                "warning"
            )

        # Check error rate
        if metrics["error_rate"] > 0.05:
            await self.create_alert(
                "High Error Rate",
                f"Error rate is {metrics['error_rate']:.2%}",
                "critical"
            )

    async def create_alert(self, title: str, message: str, severity: str):
        """Create and send alert"""

        alert = Alert(
            title=title,
            message=message,
            severity=severity,
            timestamp=datetime.now()
        )

        self.alerts.append(alert)
        self.logger.warning(f"[{severity.upper()}] {title}: {message}")

        # Send to alerting system
        # (Email, Slack, PagerDuty, etc.)

    async def log_metrics(self, metrics: Dict):
        """Log metrics to Cloud Monitoring"""

        project_name = f"projects/{self.project_id}"

        for metric_name, value in metrics.items():
            if metric_name == "timestamp":
                continue

            series = monitoring_v3.TimeSeries()
            series.metric.type = f"custom.googleapis.com/agent/{metric_name}"

            point = monitoring_v3.Point()
            point.value.double_value = float(value)
            point.interval.end_time.seconds = int(datetime.now().timestamp())

            series.points = [point]

            self.monitoring_client.create_time_series(
                name=project_name,
                time_series=[series]
            )
```

### Example 7: Agent Versioning and A/B Testing

**Scenario:** Compare different agent versions

```python
"""
A/B testing framework for agents
"""

import asyncio
from typing import Dict, List
import random

from google.adk import Agent
from google.adk.eval import EvaluationSuite

class ABTestFramework:
    """A/B testing for agent versions"""

    def __init__(self):
        self.agents = {}
        self.traffic_split = {}
        self.results = {}

    def register_agent(self, name: str, agent: Agent, traffic_pct: float):
        """Register agent version"""
        self.agents[name] = agent
        self.traffic_split[name] = traffic_pct
        self.results[name] = {
            "requests": 0,
            "successes": 0,
            "failures": 0,
            "total_latency": 0.0,
            "total_cost": 0.0
        }

    async def route_request(self, input: Dict) -> tuple:
        """Route request to agent based on traffic split"""

        # Randomly select agent based on traffic split
        rand = random.random() * 100
        cumulative = 0

        selected_agent = None
        selected_name = None

        for name, pct in self.traffic_split.items():
            cumulative += pct
            if rand <= cumulative:
                selected_agent = self.agents[name]
                selected_name = name
                break

        if not selected_agent:
            selected_name = list(self.agents.keys())[0]
            selected_agent = self.agents[selected_name]

        # Execute request
        start_time = asyncio.get_event_loop().time()

        try:
            result = await selected_agent.process(input)
            success = True
        except Exception as e:
            result = {"error": str(e)}
            success = False

        end_time = asyncio.get_event_loop().time()
        latency = end_time - start_time

        # Record metrics
        self.results[selected_name]["requests"] += 1
        if success:
            self.results[selected_name]["successes"] += 1
        else:
            self.results[selected_name]["failures"] += 1

        self.results[selected_name]["total_latency"] += latency

        return selected_name, result

    def get_statistics(self) -> Dict:
        """Get A/B test statistics"""

        stats = {}

        for name, results in self.results.items():
            requests = results["requests"]

            if requests == 0:
                continue

            stats[name] = {
                "requests": requests,
                "success_rate": results["successes"] / requests,
                "avg_latency": results["total_latency"] / requests,
                "avg_cost": results["total_cost"] / requests if results["total_cost"] > 0 else 0
            }

        return stats

    def determine_winner(self) -> str:
        """Determine winning agent version"""

        stats = self.get_statistics()

        # Score based on success rate and latency
        scores = {}
        for name, stat in stats.items():
            scores[name] = (
                stat["success_rate"] * 0.6 -
                stat["avg_latency"] * 0.2 -
                stat["avg_cost"] * 0.2
            )

        winner = max(scores.items(), key=lambda x: x[1])
        return winner[0]
```

### Example 8: Comprehensive Agent Testing Suite

**Scenario:** Complete testing framework

```python
"""
Comprehensive testing suite for agents
"""

import asyncio
from typing import Dict, List, Optional
import pytest

from google.adk import Agent
from google.adk.eval import EvaluationSuite

class AgentTestSuite:
    """Comprehensive testing suite"""

    def __init__(self, agent: Agent):
        self.agent = agent

    async def run_all_tests(self) -> Dict:
        """Run all test categories"""

        results = {
            "unit_tests": await self.run_unit_tests(),
            "integration_tests": await self.run_integration_tests(),
            "performance_tests": await self.run_performance_tests(),
            "security_tests": await self.run_security_tests(),
            "edge_case_tests": await self.run_edge_case_tests()
        }

        # Calculate overall pass rate
        total_passed = sum(r["passed"] for r in results.values())
        total_tests = sum(r["total"] for r in results.values())

        results["overall"] = {
            "total": total_tests,
            "passed": total_passed,
            "pass_rate": total_passed / total_tests if total_tests > 0 else 0
        }

        return results

    async def run_unit_tests(self) -> Dict:
        """Unit tests for individual components"""

        tests = [
            self.test_tool_registration(),
            self.test_input_validation(),
            self.test_output_formatting(),
            self.test_error_handling()
        ]

        results = await asyncio.gather(*tests)

        return {
            "total": len(results),
            "passed": sum(1 for r in results if r),
            "failed": sum(1 for r in results if not r)
        }

    async def run_integration_tests(self) -> Dict:
        """Integration tests"""

        tests = [
            self.test_end_to_end_flow(),
            self.test_tool_chaining(),
            self.test_memory_persistence(),
            self.test_external_api_integration()
        ]

        results = await asyncio.gather(*tests)

        return {
            "total": len(results),
            "passed": sum(1 for r in results if r),
            "failed": sum(1 for r in results if not r)
        }

    async def run_performance_tests(self) -> Dict:
        """Performance tests"""

        tests = [
            self.test_latency_under_load(),
            self.test_concurrent_requests(),
            self.test_memory_usage(),
            self.test_cost_efficiency()
        ]

        results = await asyncio.gather(*tests)

        return {
            "total": len(results),
            "passed": sum(1 for r in results if r),
            "failed": sum(1 for r in results if not r)
        }

    async def run_security_tests(self) -> Dict:
        """Security tests"""

        tests = [
            self.test_input_sanitization(),
            self.test_prompt_injection_resistance(),
            self.test_data_privacy(),
            self.test_authentication()
        ]

        results = await asyncio.gather(*tests)

        return {
            "total": len(results),
            "passed": sum(1 for r in results if r),
            "failed": sum(1 for r in results if not r)
        }

    async def run_edge_case_tests(self) -> Dict:
        """Edge case tests"""

        tests = [
            self.test_empty_input(),
            self.test_very_long_input(),
            self.test_malformed_input(),
            self.test_timeout_scenarios()
        ]

        results = await asyncio.gather(*tests)

        return {
            "total": len(results),
            "passed": sum(1 for r in results if r),
            "failed": sum(1 for r in results if not r)
        }

    # Individual test implementations
    async def test_tool_registration(self) -> bool:
        """Test tool registration"""
        try:
            tools = self.agent.get_registered_tools()
            return len(tools) > 0
        except:
            return False

    async def test_input_validation(self) -> bool:
        """Test input validation"""
        try:
            # Test with valid input
            result = await self.agent.process({"input": "test"})
            return "error" not in result
        except:
            return False

    async def test_output_formatting(self) -> bool:
        """Test output formatting"""
        try:
            result = await self.agent.process({"input": "test"})
            return isinstance(result, dict) and "response" in result
        except:
            return False

    async def test_error_handling(self) -> bool:
        """Test error handling"""
        try:
            # Test with problematic input
            result = await self.agent.process(None)
            return "error" in result
        except:
            return True  # Exception caught = good error handling

    async def test_end_to_end_flow(self) -> bool:
        """Test complete flow"""
        try:
            result = await self.agent.process({"input": "full test"})
            return result.get("success", False)
        except:
            return False

    async def test_tool_chaining(self) -> bool:
        """Test tool chaining"""
        # Implementation
        return True

    async def test_memory_persistence(self) -> bool:
        """Test memory persistence"""
        # Implementation
        return True

    async def test_external_api_integration(self) -> bool:
        """Test external API calls"""
        # Implementation
        return True

    async def test_latency_under_load(self) -> bool:
        """Test latency under load"""
        # Implementation
        return True

    async def test_concurrent_requests(self) -> bool:
        """Test concurrent requests"""
        # Implementation
        return True

    async def test_memory_usage(self) -> bool:
        """Test memory usage"""
        # Implementation
        return True

    async def test_cost_efficiency(self) -> bool:
        """Test cost efficiency"""
        # Implementation
        return True

    async def test_input_sanitization(self) -> bool:
        """Test input sanitization"""
        # Implementation
        return True

    async def test_prompt_injection_resistance(self) -> bool:
        """Test prompt injection resistance"""
        # Implementation
        return True

    async def test_data_privacy(self) -> bool:
        """Test data privacy"""
        # Implementation
        return True

    async def test_authentication(self) -> bool:
        """Test authentication"""
        # Implementation
        return True

    async def test_empty_input(self) -> bool:
        """Test empty input"""
        # Implementation
        return True

    async def test_very_long_input(self) -> bool:
        """Test very long input"""
        # Implementation
        return True

    async def test_malformed_input(self) -> bool:
        """Test malformed input"""
        # Implementation
        return True

    async def test_timeout_scenarios(self) -> bool:
        """Test timeout scenarios"""
        # Implementation
        return True
```

---

## Advanced Usage

### Custom Evaluators

Create domain-specific evaluators:

```python
from google.adk.eval import BaseEvaluator, EvaluationResult

class CustomDomainEvaluator(BaseEvaluator):
    def __init__(self, domain_rules: Dict):
        super().__init__(name="custom_domain")
        self.domain_rules = domain_rules

    async def evaluate(self, trajectory: Dict) -> EvaluationResult:
        # Custom evaluation logic
        score = self._calculate_score(trajectory)

        return EvaluationResult(
            evaluator=self.name,
            score=score,
            passed=score >= 0.7,
            details={"custom_metrics": {}}
        )
```

### Distributed Agent Evaluation

Scale evaluation across multiple machines:

```bash
# Run distributed evaluation
adk eval distributed \
  --config eval_config.yaml \
  --workers 10 \
  --coordinator redis://localhost:6379
```

### Continuous Evaluation Pipeline

```yaml
# .github/workflows/eval.yml
name: Agent Evaluation
on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install ADK
        run: pip install google-adk
      - name: Run Evaluation
        run: |
          adk eval --config eval_config.yaml
          adk report generate --output ./report.html
      - name: Check Threshold
        run: |
          adk eval ci --fail-threshold 0.8
```

---

## Best Practices

### 1. Agent Design

- Keep agents focused on specific tasks
- Design clear tool interfaces
- Implement proper error handling
- Use structured outputs
- Document expected behavior

### 2. Tool Development

- Make tools atomic and reusable
- Validate inputs thoroughly
- Provide clear descriptions
- Include examples in docstrings
- Handle edge cases gracefully

### 3. Evaluation Strategy

- Start with basic evaluators
- Add domain-specific evaluators
- Evaluate on diverse datasets
- Include edge cases
- Track metrics over time

### 4. Production Deployment

- Use staging environments
- Implement gradual rollout
- Monitor key metrics
- Set up alerting
- Have rollback procedures

### 5. Cost Management

- Monitor API costs
- Cache expensive operations
- Optimize tool usage
- Use appropriate model sizes
- Set cost budgets

---

## Integration Guide

### Google Cloud Integration

```python
from google.cloud import aiplatform
from google.adk import Agent

# Initialize Vertex AI
aiplatform.init(project="your-project", location="us-central1")

# Deploy agent
agent.deploy(
    platform="vertex-ai",
    endpoint_name="agent-endpoint"
)
```

### BigQuery Integration

```python
from google.cloud import bigquery
from google.adk.storage import BigQueryStorage

# Store evaluation results in BigQuery
storage = BigQueryStorage(
    project="your-project",
    dataset="agent_evals"
)

eval_results = agent.evaluate()
storage.save(eval_results)
```

---

## Troubleshooting

### Common Issues

**Issue: Tool not found**
```python
# Ensure tool is registered
agent.list_tools()  # Check registered tools
agent.register_tool(my_tool)  # Register if missing
```

**Issue: Evaluation timeout**
```yaml
# Increase timeout in config
evaluation:
  timeout: 300  # 5 minutes
```

**Issue: Memory errors**
```python
# Use streaming for large datasets
adk eval --config eval_config.yaml --stream
```

---

## API Reference

### Core Classes

**Agent:**
- `__init__(config: AgentConfig)`
- `register_tool(tool: Tool)`
- `process(input: Dict) -> Dict`
- `evaluate(suite: EvaluationSuite) -> EvaluationResult`

**Tool:**
- `@Tool(name, description, parameters)`
- `execute(*args, **kwargs)`

**EvaluationSuite:**
- `add_evaluator(evaluator: BaseEvaluator)`
- `run(agent: Agent) -> EvaluationResult`

---

## Performance

### Benchmarks

- Agent Initialization: ~100ms
- Tool Registration: ~10ms per tool
- Evaluation Latency: ~2-5s per test case
- Deployment Time: ~30-60s

### Optimization

- Use caching for repeated operations
- Batch similar requests
- Optimize tool implementations
- Use appropriate model sizes

---

## Security

### Best Practices

- Sanitize all inputs
- Validate tool parameters
- Use service accounts
- Implement rate limiting
- Encrypt sensitive data
- Audit tool usage

---

## References

### Official Resources

- **Documentation**: https://cloud.google.com/adk/docs
- **GitHub**: https://github.com/google/adk
- **Examples**: https://github.com/google/adk/examples

### Community

- **Stack Overflow**: [google-adk tag]
- **Discord**: Google Cloud AI Community

---

**Last Updated**: 2024
**Google ADK Version**: 1.0.0+
**Minimum Python**: 3.9+
