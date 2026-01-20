# Semantic Kernel Deep Dive: Comprehensive Microsoft AI Agent Guide

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

### What is Semantic Kernel?

Semantic Kernel is Microsoft's open-source SDK for integrating Large Language Models (LLMs) into applications with enterprise-grade features. It provides a kernel-based architecture that orchestrates AI capabilities through plugins, planners, and memory systems. Think of it as the "operating system" for AI - it manages resources, coordinates execution, and provides a consistent interface for AI operations.

### Why Semantic Kernel?

**Enterprise-Ready Architecture**
- Built by Microsoft for production workloads
- Comprehensive plugin system for extensibility
- Automatic planning and orchestration
- Strong typing and error handling
- Native Azure integration

**Plugin-Based Extensibility**
- Decorator-based plugin creation (`@kernel_function`)
- Automatic parameter binding and validation
- Plugin composition and reusability
- Support for both semantic and native plugins

**Intelligent Planning**
- Automatic multi-step workflow generation
- Sequential and action planners
- Goal-oriented task decomposition
- Dynamic plan adaptation

**Memory and State**
- Semantic memory with vector embeddings
- Context-aware conversations
- Persistent and volatile memory options
- Integration with vector databases

**Cross-Platform Support**
- Python and .NET SDKs
- Consistent API across languages
- Cloud and edge deployment
- Integration with Microsoft ecosystem

### Key Capabilities

**Kernel-Centric Design**
- Central orchestration of AI services
- Plugin registry and management
- Service registration and dependency injection
- Unified configuration management

**Plugin Functions**
- Native functions (Python code)
- Semantic functions (LLM-powered)
- Function chaining and composition
- Parameter validation and type safety

**AI Service Integration**
- OpenAI, Azure OpenAI, Google, Anthropic
- Multiple concurrent services
- Model selection and routing
- Fallback and retry strategies

**Planning and Orchestration**
- SequentialPlanner for step-by-step execution
- ActionPlanner for single-step optimization
- FunctionCallingStepwisePlanner for iterative planning
- Custom planner development

---

## System Architecture

### Architectural Overview

Semantic Kernel follows a kernel-centric architecture where the Kernel acts as the central orchestrator managing plugins, services, and execution flow.

```
┌────────────────────────────────────────────────────────────────┐
│                      Application Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   User App   │  │   Service    │  │   API        │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────────────────────┬────────────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────────────┐
│                         Kernel Layer                            │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                 Semantic Kernel                          │  │
│  │  ┌───────────┐  ┌───────────┐  ┌────────────┐          │  │
│  │  │  Plugin   │  │  Service  │  │   Memory   │          │  │
│  │  │ Registry  │  │ Registry  │  │  Manager   │          │  │
│  │  └───────────┘  └───────────┘  └────────────┘          │  │
│  │  ┌───────────┐  ┌───────────┐  ┌────────────┐          │  │
│  │  │ Function  │  │  Planner  │  │  Context   │          │  │
│  │  │ Invoker   │  │  Engine   │  │  Variables │          │  │
│  │  └───────────┘  └───────────┘  └────────────┘          │  │
│  └─────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────────────┐
│                        Plugin Layer                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐│
│  │  Plugin 1  │  │  Plugin 2  │  │  Plugin N  │  │  Built-in││
│  │  (Custom)  │  │  (Custom)  │  │  (Custom)  │  │  Plugins ││
│  └────────────┘  └────────────┘  └────────────┘  └──────────┘│
└────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────────────┐
│                      Service Layer                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐│
│  │  OpenAI    │  │   Azure    │  │  Anthropic │  │  Custom  ││
│  │  Service   │  │   OpenAI   │  │  Service   │  │ Services ││
│  └────────────┘  └────────────┘  └────────────┘  └──────────┘│
└────────────────────────────────────────────────────────────────┘
```

### Component Descriptions

**Application Layer**
- User applications and services
- Web apps, APIs, CLI tools
- Integration points

**Kernel Layer**
- **Kernel**: Central orchestrator managing all components
- **Plugin Registry**: Manages registered plugins
- **Service Registry**: Manages AI service connections
- **Memory Manager**: Handles semantic memory and context
- **Function Invoker**: Executes plugin functions
- **Planner Engine**: Generates and executes plans
- **Context Variables**: Manages execution context

**Plugin Layer**
- **Custom Plugins**: User-defined functionality
- **Built-in Plugins**: Core capabilities (HTTP, Time, etc.)
- **Plugin Functions**: Individual executable functions
- **Function Metadata**: Schemas, parameters, descriptions

**Service Layer**
- **AI Services**: LLM providers (OpenAI, Azure, etc.)
- **Embedding Services**: Vector embedding generation
- **Custom Services**: User-defined service integrations

### Data Flow Architecture

```
User Request
    │
    ▼
Kernel.invoke_function()
    │
    ├─→ Plugin Registry (lookup function)
    │
    ├─→ Service Registry (get AI service)
    │
    ├─→ Context Variables (load context)
    │
    ▼
Function Execution
    │
    ├─→ Parameter Binding
    │
    ├─→ AI Service Call (if semantic function)
    │
    ├─→ Native Code Execution (if native function)
    │
    ▼
Result Processing
    │
    ├─→ Memory Update (store results)
    │
    ├─→ Context Update (update variables)
    │
    ▼
Return Result to User
```

---

## High-Level System Architecture

### Kernel Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                         Kernel                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                    Configuration                        │  │
│  │  • Services: List[AIService]                           │  │
│  │  • Plugins: Dict[str, Plugin]                          │  │
│  │  • Memory: SemanticMemory                              │  │
│  │  • Settings: KernelSettings                            │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                     Operations                          │  │
│  │  • add_service(service)                                │  │
│  │  • add_plugin(plugin, name)                            │  │
│  │  • invoke(function, **kwargs)                          │  │
│  │  • invoke_prompt(prompt, **settings)                   │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Plugin Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                          Plugin                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Plugin Class Definition                    │  │
│  │                                                         │  │
│  │  class MyPlugin:                                        │  │
│  │      @kernel_function(                                  │  │
│  │          name="function_name",                          │  │
│  │          description="Function description"             │  │
│  │      )                                                  │  │
│  │      def my_function(self, param: str) -> str:          │  │
│  │          # Implementation                               │  │
│  │          return result                                  │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Function Metadata                          │  │
│  │  • Name: "function_name"                                │  │
│  │  • Description: "Function description"                  │  │
│  │  • Parameters: [{"name": "param", "type": "str"}]       │  │
│  │  • Return Type: "str"                                   │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Execution Flow

```
1. Initialize Kernel
   kernel = Kernel()

2. Add AI Service
   kernel.add_service(OpenAIChatCompletion(...))

3. Add Plugins
   kernel.add_plugin(MyPlugin(), "MyPlugin")

4. Invoke Function
   result = await kernel.invoke(
       plugin_name="MyPlugin",
       function_name="my_function",
       param="value"
   )

5. Process Result
   print(result)
```

---

## Core Components Deep Dive

### 1. Kernel

The Kernel is the central component managing all AI operations.

**Kernel Creation and Configuration**:

```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

# Create kernel
kernel = sk.Kernel()

# Add AI service
chat_service = OpenAIChatCompletion(
    service_id="chat",
    ai_model_id="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)
kernel.add_service(chat_service)

# Configure kernel settings (optional)
kernel.retry_mechanism.max_retry_count = 3
kernel.retry_mechanism.use_exponential_backoff = True
```

**Key Methods**:

```python
# Add service
kernel.add_service(ai_service)

# Add plugin
kernel.add_plugin(plugin_instance, plugin_name="PluginName")

# Invoke function
result = await kernel.invoke(
    plugin_name="PluginName",
    function_name="function_name",
    **parameters
)

# Invoke prompt (quick LLM call)
result = await kernel.invoke_prompt(
    "What is {{$topic}}?",
    topic="machine learning"
)

# Get plugin
plugin = kernel.get_plugin("PluginName")

# Get function
function = kernel.get_function("PluginName", "function_name")
```

### 2. Plugins

Plugins are collections of related functions.

**Plugin Definition**:

```python
import semantic_kernel as sk
from typing import Annotated

class WeatherPlugin:
    """Plugin for weather operations."""

    @sk.kernel_function(
        name="get_weather",
        description="Get current weather for a location"
    )
    def get_weather(
        self,
        location: Annotated[str, "City name or location"]
    ) -> Annotated[str, "Weather information"]:
        """
        Get weather for a location.

        Args:
            location: The city name or location to get weather for

        Returns:
            Weather information including temperature and conditions
        """
        # Implementation
        weather_data = {
            "San Francisco": "Sunny, 72°F, light breeze",
            "New York": "Cloudy, 65°F, chance of rain",
            "London": "Rainy, 55°F, windy"
        }
        return weather_data.get(
            location,
            f"Weather data not available for {location}"
        )

    @sk.kernel_function(
        name="get_forecast",
        description="Get weather forecast for upcoming days"
    )
    def get_forecast(
        self,
        location: Annotated[str, "City name"],
        days: Annotated[int, "Number of days (1-7)"] = 3
    ) -> Annotated[str, "Weather forecast"]:
        """Get multi-day weather forecast."""
        return f"{days}-day forecast for {location}: Partly cloudy with temperatures ranging 60-75°F"

# Register plugin with kernel
kernel.add_plugin(WeatherPlugin(), "Weather")
```

**Plugin Best Practices**:

1. **Focused Responsibility**: Each plugin should handle a specific domain
2. **Clear Descriptions**: Essential for AI to choose correct functions
3. **Type Annotations**: Use Annotated for parameter descriptions
4. **Error Handling**: Handle errors gracefully within functions
5. **Stateless Design**: Avoid state unless necessary

### 3. Functions

Functions are the executable units within plugins.

**Function Types**:

**Native Functions** (Python code):
```python
@sk.kernel_function(name="calculate", description="Perform calculations")
def calculate(self, expression: str) -> str:
    """Execute mathematical calculations."""
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"
```

**Semantic Functions** (LLM-powered):
```python
# Created directly in kernel
semantic_function = kernel.add_function(
    prompt="""You are a helpful assistant.

User question: {{$input}}

Provide a clear and concise answer.""",
    function_name="answer_question",
    plugin_name="QA"
)

# Invoke semantic function
result = await kernel.invoke(
    plugin_name="QA",
    function_name="answer_question",
    input="What is Python?"
)
```

**Function Parameters**:

```python
from typing import Annotated, Optional

@sk.kernel_function(
    name="advanced_search",
    description="Perform advanced search with filters"
)
def advanced_search(
    self,
    query: Annotated[str, "Search query"],
    max_results: Annotated[int, "Maximum number of results"] = 10,
    include_archived: Annotated[bool, "Include archived items"] = False,
    category: Annotated[Optional[str], "Filter by category"] = None
) -> Annotated[str, "Search results"]:
    """Advanced search with multiple parameters."""
    results = f"Searching for '{query}' (max: {max_results})"
    if include_archived:
        results += " including archived items"
    if category:
        results += f" in category '{category}'"
    return results
```

### 4. Services

AI services provide LLM capabilities to the kernel.

**Adding Services**:

```python
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    AzureChatCompletion,
    OpenAITextEmbedding
)

# OpenAI Service
openai_service = OpenAIChatCompletion(
    service_id="openai-gpt4",
    ai_model_id="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)
kernel.add_service(openai_service)

# Azure OpenAI Service
azure_service = AzureChatCompletion(
    service_id="azure-gpt4",
    deployment_name="gpt-4",
    endpoint="https://your-resource.openai.azure.com",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)
kernel.add_service(azure_service)

# Embedding Service
embedding_service = OpenAITextEmbedding(
    service_id="embeddings",
    ai_model_id="text-embedding-ada-002",
    api_key=os.getenv("OPENAI_API_KEY")
)
kernel.add_service(embedding_service)

# Use specific service
result = await kernel.invoke(
    plugin_name="MyPlugin",
    function_name="my_function",
    service_id="azure-gpt4"  # Use specific service
)
```

### 5. Memory

Semantic Memory provides context-aware storage and retrieval.

**Memory Configuration**:

```python
from semantic_kernel.memory import SemanticTextMemory
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding

# Create memory with embedding service
embedding_service = OpenAITextEmbedding(
    service_id="embeddings",
    ai_model_id="text-embedding-ada-002",
    api_key=os.getenv("OPENAI_API_KEY")
)

memory = SemanticTextMemory(
    storage=MemoryStore(),  # In-memory storage
    embedding_generator=embedding_service
)

# Add memory to kernel
kernel.import_plugin_from_object(memory, "memory")

# Save to memory
await memory.save_information(
    collection="facts",
    text="Machine learning is a subset of artificial intelligence.",
    id="fact_1"
)

# Search memory
results = await memory.search(
    collection="facts",
    query="What is ML?",
    limit=3
)

for result in results:
    print(f"Score: {result.relevance}, Text: {result.text}")
```

### 6. Planners

Planners automatically generate execution plans for complex goals.

**Sequential Planner**:

```python
from semantic_kernel.planning import SequentialPlanner

# Create planner
planner = SequentialPlanner(kernel)

# Create plan from goal
goal = "Research AI trends, analyze the findings, and create a summary report"
plan = await planner.create_plan(goal)

# Inspect plan
print(f"Plan has {len(plan._steps)} steps:")
for i, step in enumerate(plan._steps):
    print(f"  Step {i+1}: {step.description}")

# Execute plan
result = await plan.invoke(kernel)
print(f"\\nResult: {result}")
```

**Action Planner**:

```python
from semantic_kernel.planning import ActionPlanner

# Create action planner (single-step)
action_planner = ActionPlanner(kernel)

# Get best action for goal
goal = "Get the current weather in San Francisco"
plan = await action_planner.create_plan(goal)

# Execute
result = await plan.invoke(kernel)
print(result)
```

---

## End-to-End Flow

### Complete Request Lifecycle

**Scenario**: User asks "What's the weather in London and calculate 15% of 200?"

**Step 1: Setup**

```python
import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

# Create kernel
kernel = sk.Kernel()

# Add AI service
kernel.add_service(
    OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

# Define plugins
class WeatherPlugin:
    @sk.kernel_function(name="get_weather", description="Get weather")
    def get_weather(self, location: str) -> str:
        return f"Weather in {location}: Sunny, 72°F"

class MathPlugin:
    @sk.kernel_function(name="calculate", description="Calculate percentage")
    def calculate(self, number: float, percentage: float) -> str:
        result = number * (percentage / 100)
        return f"{percentage}% of {number} is {result}"

# Add plugins
kernel.add_plugin(WeatherPlugin(), "Weather")
kernel.add_plugin(MathPlugin(), "Math")
```

**Step 2: Create Agent Function**

```python
# Create semantic function that can use plugins
agent_function = kernel.add_function(
    prompt="""You are a helpful assistant with access to tools.

Available tools:
- Weather.get_weather: Get weather for a location
- Math.calculate: Calculate percentage of a number

User request: {{$input}}

Use the appropriate tools to answer the request. Format your response clearly.""",
    function_name="agent",
    plugin_name="Agent"
)
```

**Step 3: Execute Request**

```python
import asyncio

async def main():
    result = await kernel.invoke(
        plugin_name="Agent",
        function_name="agent",
        input="What's the weather in London and calculate 15% of 200?"
    )
    print(result)

asyncio.run(main())
```

**Step 4: Execution Flow Trace**

```
1. User calls kernel.invoke()
   ↓
2. Kernel looks up function: Agent.agent
   ↓
3. Function is semantic function (prompt-based)
   ↓
4. Kernel prepares prompt with input variable
   ↓
5. Kernel sends prompt to AI service (GPT-4o-mini)
   ↓
6. AI analyzes request and decides to use tools
   ↓
7. AI generates tool calls:
   - Weather.get_weather(location="London")
   - Math.calculate(number=200, percentage=15)
   ↓
8. Kernel executes tool calls:
   a. kernel.invoke("Weather", "get_weather", location="London")
      → "Weather in London: Sunny, 72°F"
   b. kernel.invoke("Math", "calculate", number=200, percentage=15)
      → "15% of 200 is 30.0"
   ↓
9. Tool results returned to AI
   ↓
10. AI synthesizes final response:
    "The weather in London is sunny and 72°F. 15% of 200 is 30."
    ↓
11. Result returned to user
```

**Step 5: Complete Execution Diagram**

```
User Query
    │
    ▼
Kernel.invoke("Agent", "agent", input="...")
    │
    ├──→ Lookup Function: Agent.agent
    │
    ├──→ Function Type: Semantic
    │
    ├──→ Prepare Prompt
    │         │
    │         ├──→ Template: "You are a helpful assistant..."
    │         │
    │         └──→ Variables: {input: "What's the weather..."}
    │
    ▼
Send to AI Service (GPT-4o-mini)
    │
    ▼
AI Decision: Use Tools
    │
    ├──→ Tool Call 1: Weather.get_weather("London")
    │         │
    │         ├──→ Kernel.invoke("Weather", "get_weather", ...)
    │         │
    │         └──→ Result: "Weather in London: Sunny, 72°F"
    │
    ├──→ Tool Call 2: Math.calculate(200, 15)
    │         │
    │         ├──→ Kernel.invoke("Math", "calculate", ...)
    │         │
    │         └──→ Result: "15% of 200 is 30.0"
    │
    ▼
AI Synthesizes Response
    │
    └──→ "The weather in London is sunny and 72°F. 15% of 200 is 30."
    │
    ▼
Return to User
```

---

## Simple Agents

### 1. Basic Chat Agent

```python
import os
import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

class SimpleChatAgent:
    """Basic conversational agent."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id=model,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        # Create chat function
        self.chat_function = self.kernel.add_function(
            prompt="""You are a friendly and helpful AI assistant.

User message: {{$message}}

Respond in a helpful and conversational tone.""",
            function_name="chat",
            plugin_name="ChatAgent"
        )

    async def chat(self, message: str) -> str:
        """Send message and get response."""
        result = await self.kernel.invoke(
            plugin_name="ChatAgent",
            function_name="chat",
            message=message
        )
        return str(result)

# Usage
async def main():
    agent = SimpleChatAgent()

    messages = [
        "Hello, how are you?",
        "What can you help me with?",
        "Tell me about Python programming"
    ]

    for msg in messages:
        print(f"\\nUser: {msg}")
        response = await agent.chat(msg)
        print(f"Agent: {response}")

asyncio.run(main())
```

### 2. Stateful Conversation Agent

```python
class StatefulChatAgent:
    """Agent with conversation history."""

    def __init__(self):
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        self.conversation_history = []

    async def chat(self, message: str) -> str:
        """Chat with history tracking."""
        # Add user message to history
        self.conversation_history.append(f"User: {message}")

        # Create context with history
        history_text = "\\n".join(self.conversation_history[-10:])  # Last 10 messages

        # Create dynamic function with history
        chat_function = self.kernel.add_function(
            prompt=f"""Conversation history:
{history_text}

You are a helpful assistant. Continue the conversation naturally.""",
            function_name="chat_with_history",
            plugin_name="Chat"
        )

        result = await self.kernel.invoke(
            plugin_name="Chat",
            function_name="chat_with_history"
        )

        response = str(result)

        # Add assistant response to history
        self.conversation_history.append(f"Assistant: {response}")

        return response

# Usage
async def stateful_example():
    agent = StatefulChatAgent()

    print("User: My name is Alice")
    response1 = await agent.chat("My name is Alice")
    print(f"Agent: {response1}")

    print("\\nUser: What's my name?")
    response2 = await agent.chat("What's my name?")
    print(f"Agent: {response2}")
    # Should remember "Alice"

asyncio.run(stateful_example())
```

### 3. Tool-Enabled Agent

```python
class ToolAgent:
    """Agent with multiple tools."""

    def __init__(self):
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        # Add tool plugins
        self.kernel.add_plugin(WeatherPlugin(), "Weather")
        self.kernel.add_plugin(MathPlugin(), "Math")
        self.kernel.add_plugin(TimePlugin(), "Time")

    async def execute(self, query: str) -> str:
        """Execute query using available tools."""
        # Create agent function
        agent_function = self.kernel.add_function(
            prompt="""You are an assistant with access to these tools:
- Weather.get_weather(location): Get weather
- Math.calculate(expression): Calculate math
- Time.get_current_time(): Get current time

User query: {{$query}}

Use the appropriate tools to answer the query.""",
            function_name="agent",
            plugin_name="ToolAgent"
        )

        result = await self.kernel.invoke(
            plugin_name="ToolAgent",
            function_name="agent",
            query=query
        )

        return str(result)

# Usage
async def tool_agent_example():
    agent = ToolAgent()

    queries = [
        "What's the weather in Tokyo?",
        "What is 25 * 16?",
        "What time is it now?"
    ]

    for query in queries:
        print(f"\\nQuery: {query}")
        response = await agent.execute(query)
        print(f"Response: {response}")

asyncio.run(tool_agent_example())
```

---

## Complex Agents

### 1. Multi-Step Research Agent

Complex agent performing research, analysis, and reporting.

```python
class ResearchPlugin:
    """Plugin for research operations."""

    @sk.kernel_function(name="search_web", description="Search the web")
    def search_web(self, query: str) -> str:
        """Simulated web search."""
        return f"Search results for '{query}': [Multiple relevant articles and sources...]"

    @sk.kernel_function(name="analyze_data", description="Analyze data")
    def analyze_data(self, data: str) -> str:
        """Analyze research data."""
        return f"Analysis of data: Key insights and patterns identified..."

class ResearchAgent:
    """Complex research agent."""

    def __init__(self):
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        self.kernel.add_plugin(ResearchPlugin(), "Research")

    async def conduct_research(self, topic: str) -> dict:
        """Conduct comprehensive research."""
        # Step 1: Research
        research_func = self.kernel.add_function(
            prompt="""Research the topic: {{$topic}}

Use the Research.search_web tool to gather information.
Provide a comprehensive summary of findings.""",
            function_name="do_research",
            plugin_name="ResearchAgent"
        )

        research_result = await self.kernel.invoke(
            plugin_name="ResearchAgent",
            function_name="do_research",
            topic=topic
        )

        # Step 2: Analysis
        analysis_func = self.kernel.add_function(
            prompt="""Analyze this research:

{{$research}}

Use the Research.analyze_data tool if needed.
Provide key insights and conclusions.""",
            function_name="analyze",
            plugin_name="AnalysisAgent"
        )

        analysis_result = await self.kernel.invoke(
            plugin_name="AnalysisAgent",
            function_name="analyze",
            research=str(research_result)
        )

        # Step 3: Report
        report_func = self.kernel.add_function(
            prompt="""Create a research report:

Topic: {{$topic}}
Research: {{$research}}
Analysis: {{$analysis}}

Create a well-structured markdown report with:
- Executive Summary
- Key Findings
- Detailed Analysis
- Conclusions""",
            function_name="create_report",
            plugin_name="ReportAgent"
        )

        report_result = await self.kernel.invoke(
            plugin_name="ReportAgent",
            function_name="create_report",
            topic=topic,
            research=str(research_result),
            analysis=str(analysis_result)
        )

        return {
            "topic": topic,
            "research": str(research_result),
            "analysis": str(analysis_result),
            "report": str(report_result)
        }

# Usage
async def research_agent_example():
    agent = ResearchAgent()
    result = await agent.conduct_research("Quantum Computing Applications")
    print(result["report"])

asyncio.run(research_agent_example())
```

### 2. Decision-Making Agent

Agent with conditional logic and routing.

```python
class DecisionAgent:
    """Agent with decision-making capabilities."""

    def __init__(self):
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

    async def process_request(self, request: str) -> dict:
        """Process request with decision-making."""

        # Step 1: Classify request
        classifier = self.kernel.add_function(
            prompt="""Classify this request into one of these categories:
- technical: Technical questions or problems
- general: General information queries
- creative: Creative writing or ideation
- other: Everything else

Request: {{$request}}

Respond with only the category name.""",
            function_name="classify",
            plugin_name="Classifier"
        )

        category = await self.kernel.invoke(
            plugin_name="Classifier",
            function_name="classify",
            request=request
        )
        category = str(category).strip().lower()

        # Step 2: Route based on category
        if category == "technical":
            handler = self.kernel.add_function(
                prompt="""You are a technical expert. Provide detailed technical answer:

{{$request}}""",
                function_name="technical_handler",
                plugin_name="Handlers"
            )
        elif category == "creative":
            handler = self.kernel.add_function(
                prompt="""You are a creative writing assistant. Provide creative response:

{{$request}}""",
                function_name="creative_handler",
                plugin_name="Handlers"
            )
        else:
            handler = self.kernel.add_function(
                prompt="""You are a general assistant. Provide helpful response:

{{$request}}""",
                function_name="general_handler",
                plugin_name="Handlers"
            )

        response = await self.kernel.invoke(
            plugin_name="Handlers",
            function_name=handler.metadata.name,
            request=request
        )

        return {
            "category": category,
            "response": str(response)
        }

# Usage
async def decision_agent_example():
    agent = DecisionAgent()

    requests = [
        "Explain how neural networks work",
        "Write a short story about a robot",
        "What is the capital of France?"
    ]

    for req in requests:
        print(f"\\nRequest: {req}")
        result = await agent.process_request(req)
        print(f"Category: {result['category']}")
        print(f"Response: {result['response'][:100]}...")

asyncio.run(decision_agent_example())
```

### 3. Error-Handling Agent

Agent with comprehensive error recovery.

```python
class RobustAgent:
    """Agent with error handling and retries."""

    def __init__(self, max_retries: int = 3):
        self.kernel = sk.Kernel()
        self.max_retries = max_retries

        # Configure retry mechanism
        self.kernel.retry_mechanism.max_retry_count = max_retries
        self.kernel.retry_mechanism.use_exponential_backoff = True

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

    async def safe_execute(self, query: str) -> dict:
        """Execute with error handling."""
        attempts = 0

        while attempts < self.max_retries:
            try:
                attempts += 1

                result = await self.kernel.invoke_prompt(
                    "Answer this question: {{$query}}",
                    query=query
                )

                return {
                    "status": "success",
                    "response": str(result),
                    "attempts": attempts
                }

            except Exception as e:
                logger.error(f"Attempt {attempts} failed: {e}")

                if attempts >= self.max_retries:
                    return {
                        "status": "error",
                        "error": str(e),
                        "attempts": attempts
                    }

                await asyncio.sleep(2 ** attempts)  # Exponential backoff

        return {
            "status": "error",
            "error": "Max retries exceeded",
            "attempts": attempts
        }

# Usage
async def robust_agent_example():
    agent = RobustAgent(max_retries=3)
    result = await agent.safe_execute("What is machine learning?")
    print(result)

asyncio.run(robust_agent_example())
```

---

## Multi-Agent Systems

### 1. Sequential Multi-Agent System

Multiple specialized agents working in sequence.

```python
class SpecialistAgent:
    """Base class for specialist agents."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        self.role_function = self.kernel.add_function(
            prompt=f"""You are {role}.

{{{{$task}}}}

Provide expert-level response in your domain.""",
            function_name=f"{name}_process",
            plugin_name=name
        )

    async def process(self, task: str) -> str:
        """Process task in specialist role."""
        result = await self.kernel.invoke(
            plugin_name=self.name,
            function_name=f"{self.name}_process",
            task=task
        )
        return str(result)


class MultiAgentPipeline:
    """Sequential multi-agent system."""

    def __init__(self):
        self.researcher = SpecialistAgent(
            "Researcher",
            "a research specialist who gathers and verifies information"
        )

        self.analyzer = SpecialistAgent(
            "Analyzer",
            "a data analyst who identifies patterns and insights"
        )

        self.writer = SpecialistAgent(
            "Writer",
            "a technical writer who creates clear documentation"
        )

    async def execute(self, topic: str) -> dict:
        """Execute multi-agent pipeline."""

        # Stage 1: Research
        print("Stage 1: Research")
        research = await self.researcher.process(f"Research: {topic}")

        # Stage 2: Analysis
        print("Stage 2: Analysis")
        analysis = await self.analyzer.process(f"Analyze: {research}")

        # Stage 3: Writing
        print("Stage 3: Report Writing")
        report = await self.writer.process(f"Create report from: {analysis}")

        return {
            "topic": topic,
            "research": research,
            "analysis": analysis,
            "report": report
        }

# Usage
async def multi_agent_example():
    pipeline = MultiAgentPipeline()
    result = await pipeline.execute("AI in Healthcare")
    print("\\nFINAL REPORT:")
    print(result["report"])

asyncio.run(multi_agent_example())
```

### 2. Collaborative Multi-Agent System

Agents collaborating with shared context.

```python
class CollaborativeSystem:
    """Agents working together with shared memory."""

    def __init__(self):
        # Shared kernel and memory
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        # Shared context
        self.shared_context = {}

    async def agent_contribution(
        self,
        agent_name: str,
        role: str,
        task: str
    ) -> str:
        """Agent makes contribution to shared context."""

        # Create agent function with access to shared context
        context_str = "\\n".join([
            f"{k}: {v}" for k, v in self.shared_context.items()
        ])

        agent_func = self.kernel.add_function(
            prompt=f"""You are {role}.

Shared Context:
{context_str}

Your task: {{{{$task}}}}

Provide your contribution based on the shared context.""",
            function_name=f"{agent_name}_contribute",
            plugin_name=agent_name
        )

        result = await self.kernel.invoke(
            plugin_name=agent_name,
            function_name=f"{agent_name}_contribute",
            task=task
        )

        # Add to shared context
        self.shared_context[agent_name] = str(result)

        return str(result)

    async def collaborate(self, goal: str) -> dict:
        """Multiple agents collaborate."""

        # Agent 1: Research
        await self.agent_contribution(
            "ResearchAgent",
            "a research specialist",
            f"Research: {goal}"
        )

        # Agent 2: Analysis (uses research)
        await self.agent_contribution(
            "AnalysisAgent",
            "a data analyst",
            "Analyze the research findings"
        )

        # Agent 3: Quality Check (reviews all)
        quality_result = await self.agent_contribution(
            "QualityAgent",
            "a quality assurance specialist",
            "Review and verify the research and analysis"
        )

        return {
            "goal": goal,
            "shared_context": self.shared_context,
            "final_review": quality_result
        }

# Usage
async def collaborative_example():
    system = CollaborativeSystem()
    result = await system.collaborate("Impact of AI on education")

    print("Collaboration Results:")
    for agent, contribution in result["shared_context"].items():
        print(f"\\n{agent}:")
        print(contribution[:200] + "...")

asyncio.run(collaborative_example())
```

### 3. Planner-Based Multi-Agent System

Using planners to coordinate multiple agents.

```python
from semantic_kernel.planning import SequentialPlanner

class PlannerMultiAgentSystem:
    """Planner-coordinated multi-agent system."""

    def __init__(self):
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        # Add specialist plugins
        self.kernel.add_plugin(ResearchPlugin(), "Research")
        self.kernel.add_plugin(AnalysisPlugin(), "Analysis")
        self.kernel.add_plugin(ReportPlugin(), "Report")

        # Create planner
        self.planner = SequentialPlanner(self.kernel)

    async def execute_with_planner(self, goal: str) -> dict:
        """Use planner to coordinate agents."""

        # Create plan
        plan = await self.planner.create_plan(goal)

        print(f"Plan created with {len(plan._steps)} steps:")
        for i, step in enumerate(plan._steps):
            print(f"  {i+1}. {step.description}")

        # Execute plan
        result = await plan.invoke(self.kernel)

        return {
            "goal": goal,
            "steps_executed": len(plan._steps),
            "result": str(result)
        }

# Usage
async def planner_multi_agent_example():
    system = PlannerMultiAgentSystem()
    result = await system.execute_with_planner(
        "Research quantum computing, analyze applications, and create report"
    )
    print(f"\\nResult: {result['result']}")

asyncio.run(planner_multi_agent_example())
```

---

## RAG with Agents (Agentic RAG)

### 1. Basic RAG Agent

```python
from semantic_kernel.memory import SemanticTextMemory, MemoryStore
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding

class RAGAgent:
    """Agent with RAG capabilities."""

    def __init__(self, documents: list[str]):
        self.kernel = sk.Kernel()

        # Add chat service
        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        # Add embedding service
        embedding_service = OpenAITextEmbedding(
            service_id="embeddings",
            ai_model_id="text-embedding-ada-002",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.kernel.add_service(embedding_service)

        # Create memory
        self.memory = SemanticTextMemory(
            storage=MemoryStore(),
            embedding_generator=embedding_service
        )

        # Load documents
        asyncio.run(self._load_documents(documents))

    async def _load_documents(self, documents: list[str]):
        """Load documents into memory."""
        for i, doc in enumerate(documents):
            await self.memory.save_information(
                collection="knowledge",
                text=doc,
                id=f"doc_{i}"
            )

    async def query(self, question: str) -> dict:
        """Query with RAG."""

        # Retrieve relevant documents
        search_results = await self.memory.search(
            collection="knowledge",
            query=question,
            limit=3
        )

        # Build context from results
        context = "\\n\\n".join([
            f"[Source {i+1}] {result.text}"
            for i, result in enumerate(search_results)
        ])

        # Generate answer with context
        answer_func = self.kernel.add_function(
            prompt="""Answer the question based on the provided context.

Context:
{{$context}}

Question: {{$question}}

Provide a clear answer with citations [Source N].""",
            function_name="answer",
            plugin_name="RAG"
        )

        answer = await self.kernel.invoke(
            plugin_name="RAG",
            function_name="answer",
            context=context,
            question=question
        )

        return {
            "question": question,
            "answer": str(answer),
            "sources": [result.text for result in search_results],
            "relevance_scores": [result.relevance for result in search_results]
        }

# Usage
async def rag_agent_example():
    documents = [
        "Machine learning enables systems to learn from data without explicit programming.",
        "Deep learning uses multi-layer neural networks for complex pattern recognition.",
        "Natural language processing helps computers understand and generate human language.",
        "Computer vision allows machines to interpret and understand visual information.",
        "Reinforcement learning trains agents through trial and error with rewards."
    ]

    agent = RAGAgent(documents)
    result = await agent.query("What is machine learning?")

    print(f"Question: {result['question']}")
    print(f"\\nAnswer: {result['answer']}")
    print(f"\\nSources used:")
    for i, (source, score) in enumerate(zip(result['sources'], result['relevance_scores'])):
        print(f"  {i+1}. (relevance: {score:.2f}) {source[:60]}...")

asyncio.run(rag_agent_example())
```

### 2. Advanced Agentic RAG

Multi-step RAG with query refinement and synthesis.

```python
class AdvancedRAGAgent:
    """Advanced RAG with query refinement."""

    def __init__(self, documents: list[str]):
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        embedding_service = OpenAITextEmbedding(
            service_id="embeddings",
            ai_model_id="text-embedding-ada-002",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.kernel.add_service(embedding_service)

        self.memory = SemanticTextMemory(
            storage=MemoryStore(),
            embedding_generator=embedding_service
        )

        asyncio.run(self._load_documents(documents))

    async def _load_documents(self, documents: list[str]):
        for i, doc in enumerate(documents):
            await self.memory.save_information(
                collection="knowledge",
                text=doc,
                id=f"doc_{i}"
            )

    async def agentic_query(self, question: str) -> dict:
        """Agentic RAG workflow."""

        # Step 1: Refine query
        refine_func = self.kernel.add_function(
            prompt="""Refine this question to be more specific and searchable:

{{$question}}

Provide only the refined question.""",
            function_name="refine",
            plugin_name="QueryRefiner"
        )

        refined_question = await self.kernel.invoke(
            plugin_name="QueryRefiner",
            function_name="refine",
            question=question
        )
        refined_question = str(refined_question)

        # Step 2: Retrieve with refined query
        search_results = await self.memory.search(
            collection="knowledge",
            query=refined_question,
            limit=5
        )

        # Step 3: Re-rank results
        rerank_func = self.kernel.add_function(
            prompt="""Rank these sources by relevance to the question.

Question: {{$question}}

Sources:
{{$sources}}

Return the top 3 source IDs (comma-separated).""",
            function_name="rerank",
            plugin_name="Reranker"
        )

        sources_text = "\\n".join([
            f"ID {i}: {result.text}"
            for i, result in enumerate(search_results)
        ])

        reranked_ids = await self.kernel.invoke(
            plugin_name="Reranker",
            function_name="rerank",
            question=question,
            sources=sources_text
        )

        # Step 4: Generate answer
        top_sources = search_results[:3]  # Simplified
        context = "\\n\\n".join([
            f"[Source {i+1}] {result.text}"
            for i, result in enumerate(top_sources)
        ])

        answer_func = self.kernel.add_function(
            prompt="""Answer with citations:

Context:
{{$context}}

Question: {{$question}}

Provide comprehensive answer citing sources.""",
            function_name="answer",
            plugin_name="Answerer"
        )

        answer = await self.kernel.invoke(
            plugin_name="Answerer",
            function_name="answer",
            context=context,
            question=question
        )

        return {
            "original_question": question,
            "refined_question": refined_question,
            "answer": str(answer),
            "sources": [r.text for r in top_sources]
        }

# Usage
async def advanced_rag_example():
    documents = [
        "Machine learning algorithms learn patterns from training data.",
        "Supervised learning requires labeled datasets for training.",
        "Unsupervised learning discovers patterns in unlabeled data.",
        "Deep learning employs neural networks with many layers.",
        "Transfer learning applies pre-trained models to new tasks.",
        "Reinforcement learning optimizes actions through rewards.",
        "Natural language processing enables text understanding.",
        "Computer vision processes and analyzes images.",
        "Generative AI creates new content like text and images.",
        "Transformers revolutionized NLP with attention mechanisms."
    ]

    agent = AdvancedRAGAgent(documents)
    result = await agent.agentic_query("How do ML models learn?")

    print(f"Original: {result['original_question']}")
    print(f"Refined: {result['refined_question']}")
    print(f"\\nAnswer: {result['answer']}")

asyncio.run(advanced_rag_example())
```

---

## FASTMCP Servers with Agents

Integrating FASTMCP with Semantic Kernel for standardized tool access.

```python
from fastmcp import FastMCP

# Create MCP Server
mcp = FastMCP("Semantic Kernel MCP")

@mcp.tool()
def database_query(query: str) -> str:
    """Query database via MCP."""
    return json.dumps({"results": [{"id": 1, "data": "Sample"}]})

@mcp.tool()
def external_api_call(endpoint: str, params: dict) -> str:
    """Call external API via MCP."""
    return json.dumps({"status": "success", "data": params})

# Semantic Kernel plugin wrapping MCP tools
class MCPPlugin:
    """Plugin wrapping MCP tools."""

    @sk.kernel_function(name="query_db", description="Query database")
    def query_db(self, query: str) -> str:
        """Query database through MCP."""
        return database_query(query)

    @sk.kernel_function(name="call_api", description="Call external API")
    def call_api(self, endpoint: str, params_json: str) -> str:
        """Call API through MCP."""
        params = json.loads(params_json)
        return external_api_call(endpoint, params)

class MCPAgent:
    """Agent with MCP integration."""

    def __init__(self):
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        # Add MCP plugin
        self.kernel.add_plugin(MCPPlugin(), "MCP")

    async def execute(self, task: str) -> str:
        """Execute task using MCP tools."""
        agent_func = self.kernel.add_function(
            prompt="""You have access to MCP tools:
- MCP.query_db: Query database
- MCP.call_api: Call external APIs

Task: {{$task}}

Use appropriate MCP tools to complete the task.""",
            function_name="mcp_agent",
            plugin_name="Agent"
        )

        result = await self.kernel.invoke(
            plugin_name="Agent",
            function_name="mcp_agent",
            task=task
        )

        return str(result)

# Usage
async def mcp_example():
    agent = MCPAgent()
    result = await agent.execute("Query the database for user records")
    print(result)

asyncio.run(mcp_example())
```

---

## A2A (Agent-to-Agent) Integration

Implementing A2A protocol with Semantic Kernel.

```python
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class MessageType(Enum):
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"

@dataclass
class A2AMessage:
    message_type: MessageType
    sender_id: str
    receiver_id: str
    payload: Dict

class A2AAgent:
    """Semantic Kernel agent with A2A capabilities."""

    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id
        self.role = role
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        self.known_agents = {}

    def register_agent(self, agent_id: str, capabilities: List[str]):
        """Register another A2A agent."""
        self.known_agents[agent_id] = capabilities

    async def send_task(self, target_id: str, task: str) -> str:
        """Send task to another agent."""
        message = A2AMessage(
            message_type=MessageType.TASK_REQUEST,
            sender_id=self.agent_id,
            receiver_id=target_id,
            payload={"task": task}
        )

        # Simulate A2A communication
        return f"Task sent to {target_id}: {task}"

    async def handle_request(self, message: A2AMessage) -> str:
        """Handle incoming A2A request."""
        task = message.payload.get("task")

        # Process with Semantic Kernel
        handler_func = self.kernel.add_function(
            prompt=f"""You are {self.role}.

Task from {message.sender_id}: {{{{$task}}}}

Complete the task using your expertise.""",
            function_name="handle_task",
            plugin_name=self.agent_id
        )

        result = await self.kernel.invoke(
            plugin_name=self.agent_id,
            function_name="handle_task",
            task=task
        )

        return str(result)

# Multi-Agent A2A System
class A2ASystem:
    """System of A2A agents."""

    def __init__(self):
        self.research_agent = A2AAgent(
            "research_001",
            "a research specialist"
        )

        self.analysis_agent = A2AAgent(
            "analysis_001",
            "a data analyst"
        )

        self.writing_agent = A2AAgent(
            "writing_001",
            "a technical writer"
        )

        # Register agents with each other
        for agent in [self.research_agent, self.analysis_agent, self.writing_agent]:
            for other in [self.research_agent, self.analysis_agent, self.writing_agent]:
                if agent != other:
                    agent.register_agent(other.agent_id, ["process_task"])

    async def collaborative_task(self, task: str) -> dict:
        """Execute collaborative task."""

        # Research phase
        research_msg = A2AMessage(
            message_type=MessageType.TASK_REQUEST,
            sender_id="system",
            receiver_id="research_001",
            payload={"task": f"Research: {task}"}
        )
        research_result = await self.research_agent.handle_request(research_msg)

        # Analysis phase
        analysis_msg = A2AMessage(
            message_type=MessageType.TASK_REQUEST,
            sender_id="research_001",
            receiver_id="analysis_001",
            payload={"task": f"Analyze: {research_result}"}
        )
        analysis_result = await self.analysis_agent.handle_request(analysis_msg)

        # Writing phase
        writing_msg = A2AMessage(
            message_type=MessageType.TASK_REQUEST,
            sender_id="analysis_001",
            receiver_id="writing_001",
            payload={"task": f"Write report: {analysis_result}"}
        )
        writing_result = await self.writing_agent.handle_request(writing_msg)

        return {
            "task": task,
            "research": research_result,
            "analysis": analysis_result,
            "report": writing_result
        }

# Usage
async def a2a_example():
    system = A2ASystem()
    result = await system.collaborative_task("AI impact on education")
    print(result["report"])

asyncio.run(a2a_example())
```

---

## Advanced Patterns

### 1. Plugin Composition

```python
class CompositePlugin:
    """Plugin that composes multiple plugins."""

    def __init__(self, kernel: sk.Kernel):
        self.kernel = kernel

    @sk.kernel_function(name="complex_operation", description="Complex multi-step operation")
    async def complex_operation(self, input_data: str) -> str:
        """Compose multiple plugin functions."""

        # Step 1: Use plugin A
        result1 = await self.kernel.invoke(
            plugin_name="PluginA",
            function_name="process",
            data=input_data
        )

        # Step 2: Use plugin B with result from A
        result2 = await self.kernel.invoke(
            plugin_name="PluginB",
            function_name="transform",
            data=str(result1)
        )

        # Step 3: Use plugin C with combined results
        final_result = await self.kernel.invoke(
            plugin_name="PluginC",
            function_name="finalize",
            data=str(result2)
        )

        return str(final_result)
```

### 2. Dynamic Plugin Loading

```python
class DynamicPluginSystem:
    """System with dynamic plugin loading."""

    def __init__(self):
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        self.available_plugins = {}

    def register_plugin_class(self, name: str, plugin_class):
        """Register plugin class for later instantiation."""
        self.available_plugins[name] = plugin_class

    async def load_plugin(self, name: str):
        """Dynamically load and add plugin."""
        if name in self.available_plugins:
            plugin_instance = self.available_plugins[name]()
            self.kernel.add_plugin(plugin_instance, name)
            return True
        return False

    async def execute_with_plugins(self, task: str, required_plugins: List[str]):
        """Load required plugins and execute task."""

        # Load required plugins
        for plugin_name in required_plugins:
            await self.load_plugin(plugin_name)

        # Execute task
        result = await self.kernel.invoke_prompt(
            "Complete this task: {{$task}}",
            task=task
        )

        return str(result)
```

---

## Production Best Practices

### 1. Configuration Management

```python
from dataclasses import dataclass

@dataclass
class AgentConfig:
    """Agent configuration."""
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2000
    max_retries: int = 3
    timeout: int = 30

class ConfigurableAgent:
    """Agent with externalized configuration."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.kernel = sk.Kernel()

        # Configure service with settings
        service = OpenAIChatCompletion(
            service_id="chat",
            ai_model_id=config.model,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.kernel.add_service(service)

        # Configure retry mechanism
        self.kernel.retry_mechanism.max_retry_count = config.max_retries
```

### 2. Logging and Monitoring

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoredAgent:
    """Agent with comprehensive logging."""

    def __init__(self):
        self.kernel = sk.Kernel()

        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0
        }

    async def execute(self, query: str) -> dict:
        """Execute with logging."""
        self.metrics["total_requests"] += 1
        logger.info(f"Processing query: {query[:50]}...")

        start_time = time.time()

        try:
            result = await self.kernel.invoke_prompt(
                "Answer: {{$query}}",
                query=query
            )

            duration = time.time() - start_time
            self.metrics["successful_requests"] += 1

            logger.info(f"Success in {duration:.2f}s")

            return {
                "status": "success",
                "result": str(result),
                "duration": duration
            }

        except Exception as e:
            duration = time.time() - start_time
            self.metrics["failed_requests"] += 1

            logger.error(f"Failed in {duration:.2f}s: {e}")

            return {
                "status": "error",
                "error": str(e),
                "duration": duration
            }

    def get_metrics(self) -> dict:
        """Get performance metrics."""
        return self.metrics
```

### 3. Error Handling

```python
class RobustProductionAgent:
    """Production-ready agent with comprehensive error handling."""

    async def safe_invoke(self, query: str) -> dict:
        """Invoke with full error handling."""
        try:
            result = await self.kernel.invoke_prompt(
                "Answer: {{$query}}",
                query=query
            )

            return {
                "status": "success",
                "result": str(result)
            }

        except TimeoutError:
            logger.error("Request timed out")
            return {
                "status": "error",
                "error_type": "timeout",
                "message": "Request exceeded timeout limit"
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

---

## Troubleshooting

### Common Issues

**1. Plugin Not Found**
```python
# Problem: Plugin not registered
# Solution: Ensure plugin is added to kernel
kernel.add_plugin(MyPlugin(), "MyPlugin")

# Verify plugin exists
plugin = kernel.get_plugin("MyPlugin")
print(f"Plugin registered: {plugin is not None}")
```

**2. Function Description Issues**
```python
# Problem: AI doesn't call function correctly
# Solution: Improve description

# ❌ Bad
@sk.kernel_function(name="calc", description="Does math")
def calc(self, x: str) -> str:
    pass

# ✓ Good
@sk.kernel_function(
    name="calculate",
    description="Calculates mathematical expressions like '5 + 3' or '10 * 2'. Returns the result as a string."
)
def calculate(self, expression: Annotated[str, "Mathematical expression to evaluate"]) -> str:
    pass
```

**3. Service Configuration**
```python
# Problem: Service not available
# Solution: Verify service registration

services = kernel.services
print(f"Registered services: {[s.service_id for s in services]}")

# Add missing service
if "chat" not in [s.service_id for s in services]:
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
```

**4. Async/Await Issues**
```python
# Problem: Forgetting await
# Solution: Always await async functions

# ❌ Wrong
result = kernel.invoke(...)  # Missing await

# ✓ Correct
result = await kernel.invoke(...)
```

**5. Memory Issues**
```python
# Problem: Memory not working
# Solution: Ensure embedding service is configured

embedding_service = OpenAITextEmbedding(
    service_id="embeddings",
    ai_model_id="text-embedding-ada-002",
    api_key=os.getenv("OPENAI_API_KEY")
)
kernel.add_service(embedding_service)
```

---

## Conclusion

Semantic Kernel provides a robust, enterprise-grade framework for building AI agents with Microsoft's backing. Key strengths:

- **Kernel-Centric Architecture**: Centralized orchestration and management
- **Plugin Extensibility**: Easy to add custom functionality
- **Intelligent Planning**: Automatic workflow generation
- **Memory Integration**: Semantic memory with vector search
- **Cross-Platform**: Python and .NET support
- **Production-Ready**: Error handling, retries, monitoring

### Resources

- **Official Docs**: https://learn.microsoft.com/en-us/semantic-kernel/
- **GitHub**: https://github.com/microsoft/semantic-kernel
- **Python SDK**: https://github.com/microsoft/semantic-kernel/tree/main/python

---

**Document Version**: 1.0
**Last Updated**: 2026-01-19
**Total Lines**: 2600+
**Status**: Production Ready