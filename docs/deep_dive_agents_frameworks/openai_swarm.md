# OpenAI Swarm Deep Dive: Comprehensive Guide

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

OpenAI Swarm is an experimental, educational framework for exploring ergonomic, lightweight multi-agent orchestration. Managed by the OpenAI Solution team, Swarm focuses on making agent coordination and execution highly controllable, easily testable, and simple to understand.

**Important Note**: As of 2026, Swarm has been superseded by the OpenAI Agents SDK for production use cases. However, Swarm remains an excellent educational resource for learning multi-agent orchestration patterns and is perfect for experimentation and prototyping.

### Key Features

- **Lightweight Design**: Minimal abstractions focused on two core primitives: Agents and Handoffs
- **Stateless Architecture**: No state management between calls (similar to Chat Completions API)
- **Client-Side Execution**: All orchestration logic runs on the client
- **Explicit Control**: Developers have complete control over agent behavior and routing
- **Easy Testing**: Simple, predictable execution model makes testing straightforward
- **Ergonomic API**: Pythonic, intuitive interface for building multi-agent systems
- **Function Calling**: Native support for tool use and function execution
- **Context Variables**: Built-in mechanism for passing state between agents
- **Dynamic Instructions**: Support for both static and dynamic agent instructions
- **Streaming Support**: Real-time streaming of agent responses

### When to Use Swarm

**Good Use Cases:**
- Learning multi-agent orchestration patterns
- Rapid prototyping of agent workflows
- Educational projects and experiments
- Simple agent handoff scenarios
- Customer service bots with specialized agents
- Triage and routing systems

**Not Recommended For:**
- Production applications (use OpenAI Agents SDK instead)
- Applications requiring state persistence across sessions
- Complex memory management needs
- Long-running agent processes
- Enterprise-scale deployments

### Installation

**Requirements**: Python 3.10+

```bash
# Install from GitHub via SSH
pip install git+ssh://git@github.com/openai/swarm.git

# Or via HTTPS
pip install git+https://github.com/openai/swarm.git

# Install OpenAI SDK (required)
pip install openai
```

**Environment Setup:**

```python
import os
from swarm import Swarm, Agent

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Initialize Swarm client
client = Swarm()
```

---

## System Architecture

### Architectural Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      OpenAI Swarm System                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Application Layer                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  Agent   │  │ Handoff  │  │ Context  │  │ Function │  │  │
│  │  │Definition│  │  Logic   │  │Variables │  │  Tools   │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  Orchestration Layer                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  Agent   │  │ Function │  │ Handoff  │  │ Response │  │  │
│  │  │ Executor │  │ Executor │  │ Manager  │  │ Builder  │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Execution Engine                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  Run     │  │ Message  │  │ Context  │  │  Stream  │  │  │
│  │  │  Loop    │  │ Handler  │  │ Manager  │  │ Handler  │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    OpenAI API Layer                        │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │   Chat   │  │ Function │  │ Streaming│  │  Model   │  │  │
│  │  │Completion│  │ Calling  │  │   API    │  │ Router   │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   LLM Models (GPT-4, etc.)                 │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Agent
The fundamental building block representing an AI agent with:
- **Name**: Unique identifier for the agent
- **Model**: LLM model to use (e.g., "gpt-4o", "gpt-4-turbo")
- **Instructions**: System prompt or callable returning instructions
- **Functions**: List of tools/functions the agent can call
- **Tool Choice**: Optional control over function selection
- **Parallel Tool Calls**: Whether to execute tools in parallel

```python
from swarm import Agent
from typing import Dict, Any

# Basic agent
simple_agent = Agent(
    name="SimpleAgent",
    instructions="You are a helpful assistant.",
    model="gpt-4o"
)

# Agent with dynamic instructions
def get_instructions(context_variables: Dict[str, Any]) -> str:
    user_name = context_variables.get("user_name", "User")
    return f"You are helping {user_name}. Be friendly and professional."

dynamic_agent = Agent(
    name="DynamicAgent",
    instructions=get_instructions,
    model="gpt-4o"
)
```

#### 2. Swarm Client
The main execution engine that:
- Manages agent execution flow
- Handles function calling
- Processes agent handoffs
- Updates context variables
- Returns responses

```python
from swarm import Swarm

client = Swarm()

# Run agent
response = client.run(
    agent=my_agent,
    messages=[{"role": "user", "content": "Hello!"}],
    context_variables={"user_id": "123"},
    max_turns=10,
    debug=False
)
```

#### 3. Functions
Python callables that agents can invoke:
- Must have type hints for parameters
- Can return strings, Result objects, or Agent objects
- Access context variables via parameter
- Automatically converted to OpenAI function schemas

```python
from swarm import Agent
from typing import Optional

def search_database(query: str, context_variables: dict) -> str:
    """Search the customer database.

    Args:
        query: The search query
        context_variables: Shared context

    Returns:
        Search results as a string
    """
    user_id = context_variables.get("user_id")
    # Perform search logic
    return f"Found results for: {query}"

agent = Agent(
    name="SearchAgent",
    functions=[search_database]
)
```

#### 4. Handoffs
Mechanism for transferring control between agents:
- Return an Agent object from a function
- Use Result object for complex handoffs
- Update context variables during transfer
- Support multi-step agent chains

```python
from swarm import Agent, Result

# Define agents
sales_agent = Agent(name="Sales", instructions="Handle sales inquiries")
support_agent = Agent(name="Support", instructions="Handle support issues")

def transfer_to_sales() -> Agent:
    """Transfer to sales department"""
    return sales_agent

def transfer_to_support(issue_type: str) -> Result:
    """Transfer to support with context"""
    return Result(
        value=f"Transferring for {issue_type} issue",
        agent=support_agent,
        context_variables={"issue_type": issue_type}
    )

triage_agent = Agent(
    name="Triage",
    instructions="Route users to the right department",
    functions=[transfer_to_sales, transfer_to_support]
)
```

#### 5. Context Variables
Shared state passed between agents and functions:
- Dictionary of key-value pairs
- Updated via Result objects
- Accessible in functions and dynamic instructions
- Not persisted between client.run() calls

```python
from swarm import Result

def update_context(new_data: str, context_variables: dict) -> Result:
    """Update shared context"""
    return Result(
        value="Context updated",
        context_variables={
            "last_update": new_data,
            "update_count": context_variables.get("update_count", 0) + 1
        }
    )
```

---

## High-Level System Architecture

### Data Flow Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Client Application                         │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 │ client.run(agent, messages, context)
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                         Swarm Client                              │
│                                                                    │
│  ┌────────────────────────────────────────────────────────┐      │
│  │                  Execution Loop                         │      │
│  │                                                          │      │
│  │  1. Get Completion from Current Agent                   │      │
│  │          │                                               │      │
│  │          ▼                                               │      │
│  │  2. Execute Function Calls (if any)                     │      │
│  │          │                                               │      │
│  │          ▼                                               │      │
│  │  3. Check for Agent Handoff                             │      │
│  │          │                                               │      │
│  │          ▼                                               │      │
│  │  4. Update Context Variables                            │      │
│  │          │                                               │      │
│  │          ▼                                               │      │
│  │  5. Continue or Return Response                         │      │
│  └────────────────────────────────────────────────────────┘      │
│                            │                                       │
└────────────────────────────┼───────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    OpenAI Chat Completions API                    │
│                                                                    │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐     │
│  │   GPT-4/4o     │  │ Function Call  │  │   Streaming    │     │
│  │   Models       │  │   Processing   │  │   Responses    │     │
│  └────────────────┘  └────────────────┘  └────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

### Agent Handoff Flow

```
User Request
     │
     ▼
┌─────────────────┐
│  Triage Agent   │ ─────► Analyzes request type
└────────┬────────┘
         │
         │ (determines routing)
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│ Sales   │ │ Support  │
│ Agent   │ │  Agent   │
└────┬────┘ └─────┬────┘
     │            │
     │            │ (if needs escalation)
     │            ▼
     │      ┌──────────────┐
     │      │ Senior Agent │
     │      └──────────────┘
     │
     │ (if needs technical info)
     ▼
┌─────────────────┐
│ Technical Agent │
└─────────────────┘
```

### Function Execution Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     Agent Message                             │
│          "I need to search the database"                      │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                  LLM Function Call                            │
│     {                                                         │
│       "name": "search_database",                              │
│       "arguments": {"query": "customer 123"}                  │
│     }                                                         │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│              Swarm Function Executor                          │
│                                                               │
│  1. Extract function name and arguments                       │
│  2. Inject context_variables if needed                        │
│  3. Call Python function                                      │
│  4. Process return value:                                     │
│     - String → tool result                                    │
│     - Agent → trigger handoff                                 │
│     - Result → update context + optional handoff              │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                   Function Result                             │
│          Returned to LLM as tool call result                  │
└──────────────────────────────────────────────────────────────┘
```

### Context Variable Flow

```
Initial Context
    │
    ▼
┌─────────────────────────┐
│ {"user_id": "123",      │
│  "department": null}    │
└───────────┬─────────────┘
            │
            │ (Agent A processes)
            ▼
┌─────────────────────────┐
│ Function returns Result │
│ with context updates    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ {"user_id": "123",      │
│  "department": "sales", │
│  "priority": "high"}    │
└───────────┬─────────────┘
            │
            │ (Handoff to Agent B)
            ▼
┌─────────────────────────┐
│ Agent B accesses        │
│ updated context         │
└─────────────────────────┘
```

---

## Core Components Deep Dive

### 1. Agent Configuration

#### Basic Agent Structure

```python
from swarm import Agent
from typing import List, Callable, Optional, Dict, Any

def create_agent(
    name: str,
    instructions: str | Callable,
    functions: Optional[List[Callable]] = None,
    model: str = "gpt-4o",
    tool_choice: Optional[str] = None,
    parallel_tool_calls: bool = True
) -> Agent:
    """
    Create a configured agent.

    Args:
        name: Agent identifier
        instructions: System prompt or callable returning prompt
        functions: List of callable functions
        model: OpenAI model to use
        tool_choice: Force specific tool ("auto", "required", or function name)
        parallel_tool_calls: Allow parallel function execution

    Returns:
        Configured Agent instance
    """
    return Agent(
        name=name,
        instructions=instructions,
        functions=functions or [],
        model=model,
        tool_choice=tool_choice,
        parallel_tool_calls=parallel_tool_calls
    )

# Usage
agent = create_agent(
    name="CustomerService",
    instructions="You are a helpful customer service agent.",
    model="gpt-4o"
)
```

#### Dynamic Instructions

```python
from typing import Dict, Any
from datetime import datetime

def get_time_aware_instructions(context_variables: Dict[str, Any]) -> str:
    """
    Generate instructions based on time and context.

    Args:
        context_variables: Shared context including user info

    Returns:
        Customized instruction string
    """
    user_name = context_variables.get("user_name", "valued customer")
    user_tier = context_variables.get("tier", "standard")
    hour = datetime.now().hour

    # Time-based greeting
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    # Tier-based treatment
    if user_tier == "premium":
        service_level = "our premium service team. Provide exceptional, personalized assistance."
    else:
        service_level = "our service team. Provide helpful and professional assistance."

    return f"""{greeting}, {user_name}! You are speaking with {service_level}

Current context:
- User tier: {user_tier}
- Time: {hour}:00

Guidelines:
1. Be warm and professional
2. Prioritize user satisfaction
3. Offer proactive solutions
4. {'Emphasize premium benefits' if user_tier == 'premium' else 'Mention upgrade options when relevant'}
"""

# Create agent with dynamic instructions
dynamic_agent = Agent(
    name="DynamicServiceAgent",
    instructions=get_time_aware_instructions,
    model="gpt-4o"
)
```

#### Agent with Multiple Functions

```python
from swarm import Agent, Result
from typing import Optional, Dict, Any
import json

def get_user_info(user_id: str, context_variables: Dict[str, Any]) -> str:
    """
    Retrieve user information from database.

    Args:
        user_id: User identifier
        context_variables: Shared context

    Returns:
        User information as JSON string
    """
    # Simulate database lookup
    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "tier": "premium",
        "account_status": "active"
    }
    return json.dumps(user_data, indent=2)

def create_ticket(
    issue_description: str,
    priority: str,
    context_variables: Dict[str, Any]
) -> Result:
    """
    Create support ticket.

    Args:
        issue_description: Description of the issue
        priority: Ticket priority (low, medium, high)
        context_variables: Shared context

    Returns:
        Result with ticket ID and updated context
    """
    user_id = context_variables.get("user_id", "unknown")
    ticket_id = f"TKT-{hash(issue_description) % 10000:04d}"

    return Result(
        value=f"Created ticket {ticket_id} with {priority} priority",
        context_variables={
            "last_ticket_id": ticket_id,
            "ticket_priority": priority
        }
    )

def escalate_to_supervisor(reason: str, context_variables: Dict[str, Any]) -> Agent:
    """
    Escalate to supervisor agent.

    Args:
        reason: Reason for escalation
        context_variables: Shared context

    Returns:
        Supervisor agent
    """
    supervisor = Agent(
        name="Supervisor",
        instructions=f"""You are a supervisor handling an escalated case.

Escalation reason: {reason}
Review the conversation history and provide expert assistance.""",
        functions=[create_ticket, get_user_info]
    )
    return supervisor

# Create full-featured agent
service_agent = Agent(
    name="ServiceAgent",
    instructions="You are a customer service agent. Help users with their issues.",
    functions=[get_user_info, create_ticket, escalate_to_supervisor],
    model="gpt-4o",
    parallel_tool_calls=True
)
```

### 2. Function Calling Patterns

#### Simple Function Return

```python
def get_weather(location: str) -> str:
    """
    Get weather information for a location.

    Args:
        location: City name or coordinates

    Returns:
        Weather information
    """
    # Simulate API call
    return f"Weather in {location}: 72°F, Sunny"

weather_agent = Agent(
    name="WeatherAgent",
    instructions="Provide weather information to users.",
    functions=[get_weather]
)
```

#### Function with Context Access

```python
from typing import Dict, Any

def get_personalized_recommendations(
    category: str,
    context_variables: Dict[str, Any]
) -> str:
    """
    Get personalized recommendations based on user context.

    Args:
        category: Product category
        context_variables: User preferences and history

    Returns:
        Personalized recommendations
    """
    user_id = context_variables.get("user_id")
    preferences = context_variables.get("preferences", {})

    # Use context for personalization
    recommendations = f"Recommendations for {category} based on your preferences: "
    recommendations += ", ".join(preferences.get(category, ["Item 1", "Item 2"]))

    return recommendations

recommendation_agent = Agent(
    name="RecommendationAgent",
    instructions="Provide personalized product recommendations.",
    functions=[get_personalized_recommendations]
)
```

#### Function Returning Result Object

```python
from swarm import Result
from typing import Dict, Any, Optional

def process_payment(
    amount: float,
    payment_method: str,
    context_variables: Dict[str, Any]
) -> Result:
    """
    Process payment and update context.

    Args:
        amount: Payment amount
        payment_method: Payment method (card, bank, etc.)
        context_variables: User and transaction context

    Returns:
        Result with payment confirmation and updated context
    """
    user_id = context_variables.get("user_id")

    # Simulate payment processing
    transaction_id = f"TXN-{hash(f'{user_id}{amount}') % 100000:05d}"

    return Result(
        value=f"Payment of ${amount:.2f} processed successfully. Transaction ID: {transaction_id}",
        context_variables={
            "last_transaction_id": transaction_id,
            "last_payment_amount": amount,
            "payment_method": payment_method,
            "transaction_count": context_variables.get("transaction_count", 0) + 1
        }
    )

payment_agent = Agent(
    name="PaymentAgent",
    instructions="Process payments securely.",
    functions=[process_payment]
)
```

#### Function with Error Handling

```python
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_database_query(
    query: str,
    context_variables: Dict[str, Any]
) -> str:
    """
    Execute database query with error handling.

    Args:
        query: SQL query to execute
        context_variables: Database connection info

    Returns:
        Query results or error message
    """
    try:
        # Validate query
        if "DROP" in query.upper() or "DELETE" in query.upper():
            logger.warning(f"Dangerous query blocked: {query}")
            return "Error: Destructive queries are not allowed."

        # Simulate query execution
        logger.info(f"Executing query: {query}")
        results = "Sample results: [Row 1, Row 2, Row 3]"

        return results

    except Exception as e:
        logger.error(f"Query error: {e}")
        return f"Error executing query: {str(e)}"

database_agent = Agent(
    name="DatabaseAgent",
    instructions="Execute safe database queries for users.",
    functions=[safe_database_query]
)
```

### 3. Handoff Mechanisms

#### Simple Agent Handoff

```python
from swarm import Agent

# Define specialized agents
sales_agent = Agent(
    name="SalesAgent",
    instructions="You are a sales specialist. Help customers make purchases.",
    model="gpt-4o"
)

support_agent = Agent(
    name="SupportAgent",
    instructions="You are a technical support specialist. Help with technical issues.",
    model="gpt-4o"
)

# Handoff functions
def transfer_to_sales() -> Agent:
    """Transfer customer to sales department."""
    return sales_agent

def transfer_to_support() -> Agent:
    """Transfer customer to technical support."""
    return support_agent

# Triage agent with handoff functions
triage_agent = Agent(
    name="TriageAgent",
    instructions="""You are a triage agent. Analyze customer requests and route them:
    - Sales inquiries → transfer_to_sales()
    - Technical issues → transfer_to_support()

Ask clarifying questions if the request type is unclear.""",
    functions=[transfer_to_sales, transfer_to_support],
    model="gpt-4o"
)
```

#### Conditional Handoff with Context

```python
from swarm import Agent, Result
from typing import Dict, Any

# Define agents
basic_support = Agent(
    name="BasicSupport",
    instructions="Handle basic support questions.",
    model="gpt-4o"
)

advanced_support = Agent(
    name="AdvancedSupport",
    instructions="Handle complex technical issues.",
    model="gpt-4o"
)

billing_agent = Agent(
    name="BillingAgent",
    instructions="Handle billing and payment issues.",
    model="gpt-4o"
)

def route_by_issue_type(
    issue_type: str,
    complexity: str,
    context_variables: Dict[str, Any]
) -> Result:
    """
    Route to appropriate agent based on issue type and complexity.

    Args:
        issue_type: Type of issue (technical, billing, general)
        complexity: Issue complexity (basic, advanced)
        context_variables: Current context

    Returns:
        Result with handoff and updated context
    """
    # Determine target agent
    if issue_type == "billing":
        target_agent = billing_agent
        message = "Transferring to billing specialist"
    elif issue_type == "technical":
        if complexity == "advanced":
            target_agent = advanced_support
            message = "Transferring to advanced technical support"
        else:
            target_agent = basic_support
            message = "Transferring to basic technical support"
    else:
        target_agent = basic_support
        message = "Transferring to support agent"

    return Result(
        value=message,
        agent=target_agent,
        context_variables={
            "issue_type": issue_type,
            "complexity": complexity,
            "routing_timestamp": "2024-01-15T10:30:00"
        }
    )

router_agent = Agent(
    name="RouterAgent",
    instructions="Analyze customer issues and route to appropriate specialist.",
    functions=[route_by_issue_type],
    model="gpt-4o"
)
```

#### Multi-Step Handoff Chain

```python
from swarm import Agent, Result
from typing import Dict, Any

# Step 1: Initial contact
def transfer_to_verification() -> Agent:
    """Transfer to verification agent."""
    verification_agent = Agent(
        name="VerificationAgent",
        instructions="Verify customer identity before proceeding.",
        functions=[transfer_to_service]
    )
    return verification_agent

# Step 2: After verification
def transfer_to_service(verified: bool, context_variables: Dict[str, Any]) -> Result:
    """
    Transfer to service agent after verification.

    Args:
        verified: Whether customer is verified
        context_variables: Current context

    Returns:
        Result with appropriate handoff
    """
    if verified:
        service_agent = Agent(
            name="ServiceAgent",
            instructions="Provide full service access to verified customers.",
            functions=[escalate_to_manager]
        )
        return Result(
            value="Verification successful. Connecting to service agent.",
            agent=service_agent,
            context_variables={"verified": True, "verification_time": "2024-01-15T10:30:00"}
        )
    else:
        return Result(
            value="Verification failed. Please try again or contact support.",
            context_variables={"verified": False}
        )

# Step 3: Escalation option
def escalate_to_manager(reason: str) -> Agent:
    """Escalate to manager."""
    manager_agent = Agent(
        name="ManagerAgent",
        instructions=f"You are a manager handling an escalation. Reason: {reason}"
    )
    return manager_agent

# Initial agent
intake_agent = Agent(
    name="IntakeAgent",
    instructions="Welcome customers and initiate verification process.",
    functions=[transfer_to_verification],
    model="gpt-4o"
)
```

### 4. Context Variable Management

#### Context Variable Patterns

```python
from swarm import Result, Agent
from typing import Dict, Any
from datetime import datetime

def initialize_session(user_id: str, context_variables: Dict[str, Any]) -> Result:
    """
    Initialize user session with default context.

    Args:
        user_id: User identifier
        context_variables: Current context

    Returns:
        Result with initialized context
    """
    session_context = {
        "user_id": user_id,
        "session_start": datetime.now().isoformat(),
        "interaction_count": 0,
        "user_tier": "standard",
        "preferences": {},
        "conversation_history": []
    }

    return Result(
        value=f"Session initialized for user {user_id}",
        context_variables=session_context
    )

def update_preferences(
    preference_key: str,
    preference_value: str,
    context_variables: Dict[str, Any]
) -> Result:
    """
    Update user preferences in context.

    Args:
        preference_key: Preference name
        preference_value: Preference value
        context_variables: Current context

    Returns:
        Result with updated preferences
    """
    current_prefs = context_variables.get("preferences", {})
    current_prefs[preference_key] = preference_value

    return Result(
        value=f"Updated {preference_key} preference",
        context_variables={"preferences": current_prefs}
    )

def increment_interaction_count(context_variables: Dict[str, Any]) -> Result:
    """
    Track interaction count.

    Args:
        context_variables: Current context

    Returns:
        Result with updated interaction count
    """
    count = context_variables.get("interaction_count", 0) + 1

    return Result(
        value=f"Interaction #{count}",
        context_variables={"interaction_count": count}
    )

session_agent = Agent(
    name="SessionAgent",
    instructions="Manage user sessions and preferences.",
    functions=[initialize_session, update_preferences, increment_interaction_count]
)
```

#### Context-Aware Agent Instructions

```python
from typing import Dict, Any

def get_context_aware_instructions(context_variables: Dict[str, Any]) -> str:
    """
    Generate instructions based on current context.

    Args:
        context_variables: Current context including user state

    Returns:
        Customized instructions
    """
    user_tier = context_variables.get("user_tier", "standard")
    interaction_count = context_variables.get("interaction_count", 0)
    verified = context_variables.get("verified", False)

    base_instructions = "You are a customer service agent."

    # Add tier-specific instructions
    if user_tier == "premium":
        base_instructions += "\n\nThis is a PREMIUM user. Provide white-glove service."
    elif user_tier == "enterprise":
        base_instructions += "\n\nThis is an ENTERPRISE user. Prioritize their requests."

    # Add interaction-based instructions
    if interaction_count > 5:
        base_instructions += "\n\nThis user has had multiple interactions. They may be frustrated - be extra patient."

    # Add verification-based instructions
    if not verified:
        base_instructions += "\n\nUser is NOT verified. Do not provide sensitive information."
    else:
        base_instructions += "\n\nUser is verified. You can provide full account access."

    return base_instructions

context_aware_agent = Agent(
    name="ContextAwareAgent",
    instructions=get_context_aware_instructions,
    model="gpt-4o"
)
```

### 5. Response Handling

#### Basic Response Processing

```python
from swarm import Swarm, Agent
from typing import List, Dict, Any

client = Swarm()

def process_response(
    agent: Agent,
    messages: List[Dict[str, str]],
    context_variables: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Process agent response and extract key information.

    Args:
        agent: Agent to run
        messages: Conversation messages
        context_variables: Optional context

    Returns:
        Processed response data
    """
    response = client.run(
        agent=agent,
        messages=messages,
        context_variables=context_variables or {}
    )

    # Extract information
    final_message = response.messages[-1]["content"] if response.messages else ""
    current_agent = response.agent.name if response.agent else "Unknown"
    updated_context = response.context_variables

    return {
        "message": final_message,
        "agent": current_agent,
        "context": updated_context,
        "message_count": len(response.messages)
    }

# Usage
agent = Agent(name="Assistant", instructions="You are helpful.")
result = process_response(
    agent=agent,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(f"Agent: {result['agent']}, Message: {result['message']}")
```

#### Streaming Response Handling

```python
from swarm import Swarm, Agent
from typing import Generator, Dict, Any

client = Swarm()

def stream_agent_response(
    agent: Agent,
    messages: List[Dict[str, str]],
    context_variables: Dict[str, Any] = None
) -> Generator[str, None, None]:
    """
    Stream agent response in real-time.

    Args:
        agent: Agent to run
        messages: Conversation messages
        context_variables: Optional context

    Yields:
        Response chunks as they arrive
    """
    stream = client.run(
        agent=agent,
        messages=messages,
        context_variables=context_variables or {},
        stream=True
    )

    for chunk in stream:
        # Check chunk type
        if isinstance(chunk, dict):
            if "delim" in chunk:
                if chunk["delim"] == "start":
                    yield f"\n[Agent {chunk.get('agent', 'Unknown')} speaking]\n"
                elif chunk["delim"] == "end":
                    yield "\n[Agent finished]\n"
            elif "content" in chunk:
                yield chunk["content"]
            elif "response" in chunk:
                # Final aggregated response
                final_response = chunk["response"]
                yield f"\n\n[Final Agent: {final_response.agent.name}]"

# Usage
agent = Agent(name="Assistant", instructions="You are helpful.")
for chunk in stream_agent_response(
    agent=agent,
    messages=[{"role": "user", "content": "Tell me a story"}]
):
    print(chunk, end="", flush=True)
```

---

## End-to-End Flow

### Complete Execution Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                    1. Initialize Request                     │
│                                                               │
│  client.run(                                                  │
│      agent=triage_agent,                                      │
│      messages=[{"role": "user", "content": "Need help"}],    │
│      context_variables={"user_id": "123"}                    │
│  )                                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              2. First Agent Processes Request                │
│                                                               │
│  - Triage Agent receives message                             │
│  - Analyzes: "Need help" + context                           │
│  - Decides to call function: route_to_department()           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                3. Function Execution                         │
│                                                               │
│  route_to_department(issue="general", user_id="123")         │
│  Returns: Result(                                             │
│      value="Routing to support",                             │
│      agent=support_agent,                                    │
│      context_variables={"department": "support"}             │
│  )                                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  4. Agent Handoff                            │
│                                                               │
│  - Active agent changes: triage_agent → support_agent        │
│  - Context updated: {"user_id": "123", "department": "..."}  │
│  - Messages updated with function results                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              5. Second Agent Processes                       │
│                                                               │
│  - Support Agent takes over                                  │
│  - Has access to full conversation history                   │
│  - Uses updated context variables                            │
│  - Generates response based on its instructions              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  6. Response Return                          │
│                                                               │
│  Response(                                                    │
│      messages=[...conversation history...],                  │
│      agent=support_agent,                                    │
│      context_variables={...updated context...}               │
│  )                                                            │
└─────────────────────────────────────────────────────────────┘
```

### Detailed Step-by-Step Example

```python
from swarm import Swarm, Agent, Result
from typing import Dict, Any, List
import json

# Initialize client
client = Swarm()

# Define specialized agents
support_agent = Agent(
    name="SupportAgent",
    instructions="You are a technical support specialist. Help users resolve technical issues.",
    model="gpt-4o"
)

billing_agent = Agent(
    name="BillingAgent",
    instructions="You are a billing specialist. Help users with payment and billing questions.",
    model="gpt-4o"
)

# Define routing function
def route_to_department(
    department: str,
    context_variables: Dict[str, Any]
) -> Result:
    """
    Route user to appropriate department.

    Args:
        department: Target department (support, billing)
        context_variables: Current context

    Returns:
        Result with appropriate agent handoff
    """
    user_id = context_variables.get("user_id", "unknown")

    if department.lower() == "billing":
        target_agent = billing_agent
        message = f"Routing user {user_id} to billing department"
    else:
        target_agent = support_agent
        message = f"Routing user {user_id} to support department"

    return Result(
        value=message,
        agent=target_agent,
        context_variables={
            "department": department,
            "routed_at": "2024-01-15T10:30:00"
        }
    )

# Create triage agent
triage_agent = Agent(
    name="TriageAgent",
    instructions="""You are a triage agent. Analyze user requests and determine the appropriate department:

- Technical issues, bugs, errors → route to 'support'
- Payment issues, billing questions, invoices → route to 'billing'

Call route_to_department() with the appropriate department name.""",
    functions=[route_to_department],
    model="gpt-4o"
)

# Execute complete flow
def execute_complete_flow():
    """Demonstrate complete execution flow."""

    print("="*60)
    print("SWARM EXECUTION FLOW DEMONSTRATION")
    print("="*60)

    # Step 1: Initialize
    print("\n[Step 1: Initialize Request]")
    messages = [
        {"role": "user", "content": "I'm having trouble with my last invoice"}
    ]
    context = {"user_id": "USER-123", "tier": "premium"}
    print(f"Messages: {json.dumps(messages, indent=2)}")
    print(f"Context: {json.dumps(context, indent=2)}")

    # Step 2: Execute
    print("\n[Step 2: Execute Swarm]")
    response = client.run(
        agent=triage_agent,
        messages=messages,
        context_variables=context,
        debug=True  # Enable debug output
    )

    # Step 3: Process response
    print("\n[Step 3: Process Response]")
    print(f"Final Agent: {response.agent.name}")
    print(f"Message Count: {len(response.messages)}")
    print(f"Updated Context: {json.dumps(response.context_variables, indent=2)}")

    # Step 4: Display conversation
    print("\n[Step 4: Conversation History]")
    for i, msg in enumerate(response.messages, 1):
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        sender = msg.get("sender", "N/A")

        print(f"\nMessage {i}:")
        print(f"  Role: {role}")
        print(f"  Sender: {sender}")
        if content:
            print(f"  Content: {content[:100]}..." if len(content) > 100 else f"  Content: {content}")

        # Show function calls if present
        if msg.get("tool_calls"):
            print(f"  Function Calls: {len(msg['tool_calls'])}")
            for call in msg["tool_calls"]:
                func_name = call.get("function", {}).get("name", "unknown")
                print(f"    - {func_name}()")

    print("\n" + "="*60)
    print("EXECUTION COMPLETE")
    print("="*60)

# Run demonstration
if __name__ == "__main__":
    execute_complete_flow()
```

### Message Flow Visualization

```python
from swarm import Swarm, Agent
from typing import List, Dict

def visualize_message_flow(messages: List[Dict[str, str]]) -> None:
    """
    Visualize message flow in conversation.

    Args:
        messages: List of conversation messages
    """
    print("\n┌─── MESSAGE FLOW ───┐")

    for i, msg in enumerate(messages, 1):
        role = msg.get("role", "unknown")
        sender = msg.get("sender", "N/A")
        content = msg.get("content", "")

        # Visual indicator based on role
        if role == "user":
            icon = "👤"
            arrow = "  →  "
        elif role == "assistant":
            icon = "🤖"
            arrow = "  ←  "
        elif role == "tool":
            icon = "🔧"
            arrow = "  ↔  "
        else:
            icon = "  "
            arrow = "     "

        print(f"\n{i}. {icon} {role.upper()} ({sender})")
        print(f"{arrow}{content[:80]}..." if len(content) > 80 else f"{arrow}{content}")

    print("\n└────────────────────┘\n")

# Usage example
def demo_message_flow():
    client = Swarm()
    agent = Agent(
        name="DemoAgent",
        instructions="You are a helpful assistant."
    )

    response = client.run(
        agent=agent,
        messages=[
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi! How can I help?"},
            {"role": "user", "content": "What's the weather?"}
        ]
    )

    visualize_message_flow(response.messages)

if __name__ == "__main__":
    demo_message_flow()
```

---

## Simple Agent Examples

### Example 1: Basic Question-Answering Agent

```python
from swarm import Swarm, Agent
from typing import List, Dict
import os

# Set API key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def create_qa_agent() -> Agent:
    """
    Create a simple question-answering agent.

    Returns:
        Configured QA agent
    """
    return Agent(
        name="QAAgent",
        instructions="""You are a knowledgeable assistant that answers questions accurately and concisely.

Guidelines:
1. Provide clear, factual answers
2. If unsure, admit it rather than guessing
3. Keep responses focused and relevant
4. Use examples when helpful""",
        model="gpt-4o"
    )

def run_qa_session():
    """Run an interactive QA session."""
    client = Swarm()
    agent = create_qa_agent()

    # Example questions
    questions = [
        "What is Python?",
        "How do I create a list in Python?",
        "What's the difference between a list and a tuple?"
    ]

    print("="*60)
    print("QUESTION-ANSWERING AGENT")
    print("="*60)

    messages = []
    for question in questions:
        print(f"\n📝 Question: {question}")

        # Add user message
        messages.append({"role": "user", "content": question})

        # Get response
        response = client.run(
            agent=agent,
            messages=messages
        )

        # Update messages with full history
        messages = response.messages

        # Display answer
        answer = response.messages[-1]["content"]
        print(f"💡 Answer: {answer}\n")
        print("-"*60)

if __name__ == "__main__":
    run_qa_session()
```

### Example 2: Calculator Agent with Tool Use

```python
from swarm import Swarm, Agent
from typing import Union
import math
import os

os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def calculate(expression: str) -> str:
    """
    Safely evaluate mathematical expressions.

    Args:
        expression: Mathematical expression to evaluate

    Returns:
        Result of calculation or error message
    """
    try:
        # Safe evaluation (restricted to math operations)
        allowed_names = {
            'sqrt': math.sqrt,
            'pow': math.pow,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'pi': math.pi,
            'e': math.e
        }

        # Evaluate expression
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Result: {result}"

    except Exception as e:
        return f"Error: {str(e)}"

def get_formula(operation: str) -> str:
    """
    Get mathematical formula for common operations.

    Args:
        operation: Name of mathematical operation

    Returns:
        Formula description
    """
    formulas = {
        "pythagorean": "a² + b² = c² (for right triangles)",
        "quadratic": "x = (-b ± √(b² - 4ac)) / 2a",
        "circle_area": "A = πr²",
        "circle_circumference": "C = 2πr",
        "sphere_volume": "V = (4/3)πr³"
    }

    return formulas.get(operation.lower(), "Formula not found")

def create_calculator_agent() -> Agent:
    """
    Create calculator agent with mathematical tools.

    Returns:
        Configured calculator agent
    """
    return Agent(
        name="CalculatorAgent",
        instructions="""You are a mathematical assistant that helps with calculations and formulas.

Capabilities:
1. Perform calculations using calculate() function
2. Provide mathematical formulas using get_formula() function
3. Explain mathematical concepts
4. Help solve math problems step-by-step

When asked to calculate something, use the calculate() function with the expression.
For formulas, use get_formula() with the operation name.""",
        functions=[calculate, get_formula],
        model="gpt-4o"
    )

def run_calculator_demo():
    """Demonstrate calculator agent capabilities."""
    client = Swarm()
    agent = create_calculator_agent()

    print("="*60)
    print("CALCULATOR AGENT DEMO")
    print("="*60)

    # Test cases
    test_queries = [
        "Calculate 15 * 23 + 45",
        "What is the square root of 144?",
        "Show me the formula for the area of a circle",
        "Calculate sin(pi/2)",
        "What's 2 to the power of 10?"
    ]

    messages = []
    for query in test_queries:
        print(f"\n🔢 Query: {query}")

        messages.append({"role": "user", "content": query})

        response = client.run(
            agent=agent,
            messages=messages
        )

        messages = response.messages
        answer = response.messages[-1]["content"]

        print(f"✅ Response: {answer}\n")
        print("-"*60)

if __name__ == "__main__":
    run_calculator_demo()
```

### Example 3: Weather Information Agent

```python
from swarm import Swarm, Agent
from typing import Dict, Any
import os
from datetime import datetime

os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def get_weather(location: str, units: str = "fahrenheit") -> str:
    """
    Get current weather for a location.

    Args:
        location: City name or coordinates
        units: Temperature units (fahrenheit or celsius)

    Returns:
        Weather information
    """
    # Simulate weather API response
    weather_data = {
        "new york": {"temp": 72, "condition": "Partly Cloudy", "humidity": 65},
        "london": {"temp": 15, "condition": "Rainy", "humidity": 80},
        "tokyo": {"temp": 25, "condition": "Clear", "humidity": 55},
        "sydney": {"temp": 28, "condition": "Sunny", "humidity": 45}
    }

    location_lower = location.lower()
    data = weather_data.get(location_lower, {
        "temp": 20,
        "condition": "Unknown",
        "humidity": 50
    })

    temp = data["temp"]
    if units == "celsius":
        temp = (temp - 32) * 5/9
        unit_symbol = "°C"
    else:
        unit_symbol = "°F"

    return f"""Weather in {location.title()}:
    Temperature: {temp:.1f}{unit_symbol}
    Condition: {data['condition']}
    Humidity: {data['humidity']}%
    Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""

def get_forecast(location: str, days: int = 3) -> str:
    """
    Get weather forecast for upcoming days.

    Args:
        location: City name
        days: Number of days to forecast (1-7)

    Returns:
        Forecast information
    """
    days = min(max(days, 1), 7)  # Limit to 1-7 days

    forecast = f"📅 {days}-Day Forecast for {location.title()}:\n\n"

    for i in range(days):
        date = datetime.now().day + i
        temp_high = 75 + i * 2
        temp_low = 60 + i
        condition = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy"][i % 4]

        forecast += f"Day {i+1} (Day {date}):\n"
        forecast += f"  High: {temp_high}°F, Low: {temp_low}°F\n"
        forecast += f"  Condition: {condition}\n\n"

    return forecast

def get_weather_alerts(location: str) -> str:
    """
    Get weather alerts for a location.

    Args:
        location: City name

    Returns:
        Alert information
    """
    # Simulate alerts
    return f"⚠️ Weather Alerts for {location.title()}:\n\nNo active alerts at this time."

def create_weather_agent() -> Agent:
    """
    Create weather information agent.

    Returns:
        Configured weather agent
    """
    return Agent(
        name="WeatherAgent",
        instructions="""You are a friendly weather assistant. Help users with weather information.

Available tools:
- get_weather(location, units): Current weather conditions
- get_forecast(location, days): Multi-day forecast
- get_weather_alerts(location): Weather warnings and alerts

When users ask about weather:
1. Get their location if not provided
2. Ask about unit preference if relevant
3. Provide detailed, helpful information
4. Offer additional relevant information (forecast, alerts)""",
        functions=[get_weather, get_forecast, get_weather_alerts],
        model="gpt-4o"
    )

def run_weather_demo():
    """Demonstrate weather agent."""
    client = Swarm()
    agent = create_weather_agent()

    print("="*60)
    print("WEATHER AGENT DEMO")
    print("="*60)

    queries = [
        "What's the weather in New York?",
        "Give me a 5-day forecast for London",
        "Are there any weather alerts for Tokyo?",
        "What's the temperature in Sydney in Celsius?"
    ]

    messages = []
    for query in queries:
        print(f"\n🌤️  Query: {query}")

        messages.append({"role": "user", "content": query})

        response = client.run(
            agent=agent,
            messages=messages
        )

        messages = response.messages
        answer = response.messages[-1]["content"]

        print(f"📍 Response:\n{answer}\n")
        print("-"*60)

if __name__ == "__main__":
    run_weather_demo()
```

### Example 4: Task Management Agent

```python
from swarm import Swarm, Agent, Result
from typing import Dict, Any, List
import os
from datetime import datetime
import json

os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def add_task(
    task_name: str,
    priority: str,
    context_variables: Dict[str, Any]
) -> Result:
    """
    Add a new task to the task list.

    Args:
        task_name: Name/description of the task
        priority: Task priority (low, medium, high)
        context_variables: Current context with task list

    Returns:
        Result with updated task list
    """
    tasks = context_variables.get("tasks", [])

    new_task = {
        "id": len(tasks) + 1,
        "name": task_name,
        "priority": priority.lower(),
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }

    tasks.append(new_task)

    return Result(
        value=f"✅ Added task: '{task_name}' with {priority} priority (ID: {new_task['id']})",
        context_variables={"tasks": tasks}
    )

def list_tasks(
    filter_by: str = "all",
    context_variables: Dict[str, Any] = None
) -> str:
    """
    List all tasks with optional filtering.

    Args:
        filter_by: Filter by status (all, pending, completed) or priority
        context_variables: Current context with task list

    Returns:
        Formatted task list
    """
    tasks = context_variables.get("tasks", [])

    if not tasks:
        return "📝 No tasks found."

    # Filter tasks
    if filter_by != "all":
        if filter_by in ["pending", "completed"]:
            filtered_tasks = [t for t in tasks if t["status"] == filter_by]
        else:
            filtered_tasks = [t for t in tasks if t["priority"] == filter_by.lower()]
    else:
        filtered_tasks = tasks

    if not filtered_tasks:
        return f"📝 No {filter_by} tasks found."

    # Format output
    output = f"📋 Task List ({len(filtered_tasks)} tasks):\n\n"

    for task in filtered_tasks:
        status_icon = "✅" if task["status"] == "completed" else "⏳"
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")

        output += f"{status_icon} [{task['id']}] {priority_icon} {task['name']}\n"
        output += f"   Status: {task['status']}, Priority: {task['priority']}\n\n"

    return output

def complete_task(task_id: int, context_variables: Dict[str, Any]) -> Result:
    """
    Mark a task as completed.

    Args:
        task_id: ID of task to complete
        context_variables: Current context with task list

    Returns:
        Result with updated task list
    """
    tasks = context_variables.get("tasks", [])

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "completed"
            task["completed_at"] = datetime.now().isoformat()
            return Result(
                value=f"✅ Completed task: '{task['name']}'",
                context_variables={"tasks": tasks}
            )

    return Result(
        value=f"❌ Task {task_id} not found",
        context_variables={"tasks": tasks}
    )

def delete_task(task_id: int, context_variables: Dict[str, Any]) -> Result:
    """
    Delete a task from the list.

    Args:
        task_id: ID of task to delete
        context_variables: Current context with task list

    Returns:
        Result with updated task list
    """
    tasks = context_variables.get("tasks", [])

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(i)
            return Result(
                value=f"🗑️  Deleted task: '{deleted_task['name']}'",
                context_variables={"tasks": tasks}
            )

    return Result(
        value=f"❌ Task {task_id} not found",
        context_variables={"tasks": tasks}
    )

def create_task_agent() -> Agent:
    """
    Create task management agent.

    Returns:
        Configured task agent
    """
    return Agent(
        name="TaskAgent",
        instructions="""You are a helpful task management assistant.

Available commands:
- add_task(task_name, priority): Add a new task
- list_tasks(filter_by): Show tasks (filter: all, pending, completed, high, medium, low)
- complete_task(task_id): Mark task as done
- delete_task(task_id): Remove a task

Help users:
1. Add tasks with appropriate priorities
2. View and organize their tasks
3. Track task completion
4. Manage their task list efficiently

Be proactive in suggesting task organization and prioritization.""",
        functions=[add_task, list_tasks, complete_task, delete_task],
        model="gpt-4o"
    )

def run_task_manager_demo():
    """Demonstrate task management agent."""
    client = Swarm()
    agent = create_task_agent()

    print("="*60)
    print("TASK MANAGEMENT AGENT DEMO")
    print("="*60)

    commands = [
        "Add a task: Write documentation with high priority",
        "Add another task: Review pull requests with medium priority",
        "Show me all my tasks",
        "Complete task 1",
        "Show me pending tasks only"
    ]

    messages = []
    context = {"tasks": []}

    for command in commands:
        print(f"\n📝 Command: {command}")

        messages.append({"role": "user", "content": command})

        response = client.run(
            agent=agent,
            messages=messages,
            context_variables=context
        )

        messages = response.messages
        context = response.context_variables
        answer = response.messages[-1]["content"]

        print(f"🤖 Response:\n{answer}\n")
        print("-"*60)

    # Show final state
    print("\n📊 Final Task State:")
    print(json.dumps(context.get("tasks", []), indent=2))

if __name__ == "__main__":
    run_task_manager_demo()
```

### Example 5: Translation Agent

```python
from swarm import Swarm, Agent
from typing import Dict
import os

os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def translate_text(text: str, target_language: str) -> str:
    """
    Translate text to target language.

    Args:
        text: Text to translate
        target_language: Target language name

    Returns:
        Translation note (actual translation done by LLM)
    """
    return f"Translating to {target_language}: {text}"

def detect_language(text: str) -> str:
    """
    Detect the language of the input text.

    Args:
        text: Text to analyze

    Returns:
        Detection note (actual detection done by LLM)
    """
    return f"Detecting language for: {text}"

def get_language_info(language: str) -> str:
    """
    Get information about a language.

    Args:
        language: Language name

    Returns:
        Language information
    """
    language_data = {
        "spanish": {
            "native_name": "Español",
            "speakers": "500+ million",
            "family": "Romance",
            "writing": "Latin alphabet"
        },
        "french": {
            "native_name": "Français",
            "speakers": "280+ million",
            "family": "Romance",
            "writing": "Latin alphabet"
        },
        "japanese": {
            "native_name": "日本語 (Nihongo)",
            "speakers": "125+ million",
            "family": "Japonic",
            "writing": "Kanji, Hiragana, Katakana"
        },
        "mandarin": {
            "native_name": "中文 (Zhōngwén)",
            "speakers": "1.1+ billion",
            "family": "Sino-Tibetan",
            "writing": "Chinese characters"
        }
    }

    info = language_data.get(language.lower(), {
        "native_name": "Unknown",
        "speakers": "Unknown",
        "family": "Unknown",
        "writing": "Unknown"
    })

    return f"""Language: {language.title()}
    Native Name: {info['native_name']}
    Speakers: {info['speakers']}
    Language Family: {info['family']}
    Writing System: {info['writing']}"""

def create_translation_agent() -> Agent:
    """
    Create translation agent.

    Returns:
        Configured translation agent
    """
    return Agent(
        name="TranslationAgent",
        instructions="""You are a multilingual translation assistant.

Capabilities:
1. Translate text between languages
2. Detect input language
3. Provide language information and facts
4. Explain cultural context and nuances

When translating:
- Preserve tone and meaning
- Note any cultural context
- Provide alternative translations when relevant
- Explain idioms and expressions

Languages you support: Spanish, French, German, Italian, Portuguese, Japanese, Mandarin, Korean, Russian, Arabic, and many more.""",
        functions=[translate_text, detect_language, get_language_info],
        model="gpt-4o"
    )

def run_translation_demo():
    """Demonstrate translation agent."""
    client = Swarm()
    agent = create_translation_agent()

    print("="*60)
    print("TRANSLATION AGENT DEMO")
    print("="*60)

    queries = [
        "Translate 'Hello, how are you?' to Spanish",
        "What language is this: 'Bonjour, comment allez-vous?'",
        "Tell me about the Japanese language",
        "Translate 'Thank you very much' to French and German"
    ]

    messages = []
    for query in queries:
        print(f"\n🌍 Query: {query}")

        messages.append({"role": "user", "content": query})

        response = client.run(
            agent=agent,
            messages=messages
        )

        messages = response.messages
        answer = response.messages[-1]["content"]

        print(f"💬 Response:\n{answer}\n")
        print("-"*60)

if __name__ == "__main__":
    run_translation_demo()
```

---

## Complex Agent Examples

### Example 1: Customer Service Bot with Multiple Departments

```python
from swarm import Swarm, Agent, Result
from typing import Dict, Any, Optional
import os
from datetime import datetime
import json

os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_customer_info(customer_id: str, context_variables: Dict[str, Any]) -> str:
    """
    Retrieve customer information from database.

    Args:
        customer_id: Customer identifier
        context_variables: Current context

    Returns:
        Customer information as JSON string
    """
    # Simulate database lookup
    customers = {
        "CUST001": {
            "name": "Alice Johnson",
            "tier": "premium",
            "account_since": "2022-01-15",
            "total_orders": 45,
            "lifetime_value": 5420.50
        },
        "CUST002": {
            "name": "Bob Smith",
            "tier": "standard",
            "account_since": "2023-06-20",
            "total_orders": 12,
            "lifetime_value": 845.25
        }
    }

    customer = customers.get(customer_id, {
        "name": "Unknown Customer",
        "tier": "standard",
        "account_since": "Unknown",
        "total_orders": 0,
        "lifetime_value": 0.0
    })

    return json.dumps(customer, indent=2)

def create_support_ticket(
    issue_type: str,
    description: str,
    priority: str,
    context_variables: Dict[str, Any]
) -> Result:
    """
    Create a support ticket.

    Args:
        issue_type: Type of issue (technical, billing, general)
        description: Issue description
        priority: Ticket priority (low, medium, high, critical)
        context_variables: Current context

    Returns:
        Result with ticket information
    """
    customer_id = context_variables.get("customer_id", "UNKNOWN")
    ticket_id = f"TKT-{hash(description) % 100000:05d}"

    ticket = {
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "issue_type": issue_type,
        "description": description,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now().isoformat()
    }

    return Result(
        value=f"Created support ticket {ticket_id} with {priority} priority",
        context_variables={
            "last_ticket_id": ticket_id,
            "last_ticket_status": "open"
        }
    )

def check_order_status(order_id: str, context_variables: Dict[str, Any]) -> str:
    """
    Check order status.

    Args:
        order_id: Order identifier
        context_variables: Current context

    Returns:
        Order status information
    """
    # Simulate order lookup
    orders = {
        "ORD001": {
            "status": "shipped",
            "tracking": "1Z999AA10123456784",
            "eta": "2024-01-20",
            "items": ["Product A", "Product B"]
        },
        "ORD002": {
            "status": "processing",
            "tracking": None,
            "eta": "2024-01-22",
            "items": ["Product C"]
        }
    }

    order = orders.get(order_id, None)

    if not order:
        return f"Order {order_id} not found"

    status_msg = f"""Order {order_id} Status:
    Status: {order['status'].upper()}
    Items: {', '.join(order['items'])}
    Expected Delivery: {order['eta']}"""

    if order['tracking']:
        status_msg += f"\n    Tracking Number: {order['tracking']}"

    return status_msg

def process_refund(
    order_id: str,
    reason: str,
    context_variables: Dict[str, Any]
) -> Result:
    """
    Process refund request.

    Args:
        order_id: Order to refund
        reason: Refund reason
        context_variables: Current context

    Returns:
        Result with refund information
    """
    customer_id = context_variables.get("customer_id", "UNKNOWN")
    refund_id = f"REF-{hash(order_id) % 10000:04d}"

    return Result(
        value=f"Refund {refund_id} initiated for order {order_id}. Processing time: 5-7 business days.",
        context_variables={
            "last_refund_id": refund_id,
            "refund_order_id": order_id,
            "refund_reason": reason
        }
    )

def get_billing_info(customer_id: str, context_variables: Dict[str, Any]) -> str:
    """
    Get customer billing information.

    Args:
        customer_id: Customer identifier
        context_variables: Current context

    Returns:
        Billing information
    """
    # Simulate billing lookup
    billing = {
        "payment_method": "Visa ending in 1234",
        "billing_address": "123 Main St, City, ST 12345",
        "next_billing_date": "2024-02-01",
        "current_balance": 0.00
    }

    return json.dumps(billing, indent=2)

# ============================================================================
# SPECIALIZED AGENTS
# ============================================================================

def create_sales_agent() -> Agent:
    """Create sales specialist agent."""
    return Agent(
        name="SalesAgent",
        instructions="""You are a sales specialist helping customers make purchases.

Your role:
1. Understand customer needs
2. Recommend appropriate products
3. Answer product questions
4. Help with order placement
5. Offer promotions and upsells when relevant

Be friendly, knowledgeable, and focused on customer satisfaction.""",
        functions=[get_customer_info, check_order_status],
        model="gpt-4o"
    )

def create_support_agent() -> Agent:
    """Create technical support agent."""
    return Agent(
        name="SupportAgent",
        instructions="""You are a technical support specialist.

Your role:
1. Diagnose technical issues
2. Provide step-by-step solutions
3. Create support tickets for complex issues
4. Escalate critical problems
5. Follow up on existing tickets

Be patient, methodical, and thorough in your assistance.""",
        functions=[get_customer_info, create_support_ticket, check_order_status],
        model="gpt-4o"
    )

def create_billing_agent() -> Agent:
    """Create billing specialist agent."""
    return Agent(
        name="BillingAgent",
        instructions="""You are a billing and payments specialist.

Your role:
1. Handle billing inquiries
2. Process refunds and credits
3. Update payment information
4. Explain charges and invoices
5. Resolve payment disputes

Be accurate, transparent, and helpful with financial matters.""",
        functions=[get_customer_info, get_billing_info, process_refund, check_order_status],
        model="gpt-4o"
    )

# ============================================================================
# ROUTING LOGIC
# ============================================================================

def transfer_to_sales() -> Agent:
    """Transfer to sales department."""
    return create_sales_agent()

def transfer_to_support() -> Agent:
    """Transfer to technical support."""
    return create_support_agent()

def transfer_to_billing() -> Agent:
    """Transfer to billing department."""
    return create_billing_agent()

def escalate_to_manager(reason: str, context_variables: Dict[str, Any]) -> Agent:
    """
    Escalate to manager.

    Args:
        reason: Escalation reason
        context_variables: Current context

    Returns:
        Manager agent
    """
    customer_tier = context_variables.get("customer_tier", "standard")

    return Agent(
        name="ManagerAgent",
        instructions=f"""You are a customer service manager handling an escalated case.

Customer Tier: {customer_tier}
Escalation Reason: {reason}

Your role:
1. Review the situation thoroughly
2. Provide expert-level assistance
3. Make decisions on exceptions and special cases
4. Ensure customer satisfaction
5. Resolve complex issues

You have authority to:
- Approve refunds and credits
- Offer compensation
- Bypass standard procedures when appropriate
- Make final decisions

Prioritize customer retention and satisfaction.""",
        functions=[
            get_customer_info,
            create_support_ticket,
            process_refund,
            check_order_status,
            get_billing_info
        ],
        model="gpt-4o"
    )

# ============================================================================
# TRIAGE AGENT
# ============================================================================

def create_triage_agent() -> Agent:
    """Create main triage agent."""
    return Agent(
        name="TriageAgent",
        instructions="""You are the initial customer service contact point.

Your role:
1. Greet customers warmly
2. Understand their needs
3. Route to the appropriate department:
   - SALES: Product inquiries, purchases, recommendations
   - SUPPORT: Technical issues, troubleshooting, how-to questions
   - BILLING: Payment issues, refunds, billing questions
4. Collect necessary information before transfer
5. Escalate to manager for complex or sensitive issues

Routing guidelines:
- Ask clarifying questions if the issue category is unclear
- Get customer ID before transferring
- Set context for the next agent
- Use escalate_to_manager() for angry customers or complex problems

Available functions:
- transfer_to_sales(): Route to sales department
- transfer_to_support(): Route to technical support
- transfer_to_billing(): Route to billing department
- escalate_to_manager(reason): Escalate to management
- get_customer_info(customer_id): Look up customer details""",
        functions=[
            transfer_to_sales,
            transfer_to_support,
            transfer_to_billing,
            escalate_to_manager,
            get_customer_info
        ],
        model="gpt-4o"
    )

# ============================================================================
# DEMO
# ============================================================================

def run_customer_service_demo():
    """Demonstrate customer service bot."""
    client = Swarm()
    agent = create_triage_agent()

    print("="*70)
    print("CUSTOMER SERVICE BOT - MULTI-DEPARTMENT DEMO")
    print("="*70)

    # Simulate different customer scenarios
    scenarios = [
        {
            "context": {"customer_id": "CUST001", "customer_tier": "premium"},
            "queries": [
                "Hi, I need help with my recent order",
                "My order number is ORD001, I want to know when it will arrive"
            ]
        },
        {
            "context": {"customer_id": "CUST002", "customer_tier": "standard"},
            "queries": [
                "I'm having trouble logging into my account",
                "I keep getting an error message"
            ]
        },
        {
            "context": {"customer_id": "CUST001", "customer_tier": "premium"},
            "queries": [
                "I need to request a refund for order ORD001",
                "The product was damaged when it arrived"
            ]
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*70}")
        print(f"SCENARIO {i}")
        print(f"Customer: {scenario['context']['customer_id']} ({scenario['context']['customer_tier']})")
        print(f"{'='*70}\n")

        messages = []
        context = scenario["context"]

        for query in scenario["queries"]:
            print(f"👤 Customer: {query}\n")

            messages.append({"role": "user", "content": query})

            response = client.run(
                agent=agent,
                messages=messages,
                context_variables=context
            )

            messages = response.messages
            context = response.context_variables
            current_agent = response.agent.name
            answer = response.messages[-1]["content"]

            print(f"🤖 {current_agent}: {answer}\n")
            print(f"📊 Context: {json.dumps({k: v for k, v in context.items() if k not in ['customer_id', 'customer_tier']}, indent=2)}\n")
            print("-"*70)

        print("\n")

if __name__ == "__main__":
    run_customer_service_demo()
```

This completes the first part of the documentation. I'll continue with the remaining sections in the next response.