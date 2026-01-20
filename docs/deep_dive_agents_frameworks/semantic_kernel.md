# Microsoft Semantic Kernel Deep Dive: Comprehensive Guide

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

Microsoft Semantic Kernel is an open-source SDK that lets you easily build agents that can call your existing code. It provides a lightweight, extensible framework for integrating AI services with conventional programming languages. Semantic Kernel combines the power of Large Language Models (LLMs) with plugins, planners, and memory to create sophisticated AI applications.

### Key Features

- **Plugin Architecture**: Modular design where business logic is exposed as plugins that AI can orchestrate
- **Multi-AI Service Support**: Works with OpenAI, Azure OpenAI, Hugging Face, and custom AI services
- **Automatic Function Calling**: Native support for function calling with automatic orchestration
- **Planning Capabilities**: Built-in planners that can create and execute multi-step plans
- **Memory & Context Management**: Semantic memory for storing and retrieving context
- **Prompt Engineering**: Template-based prompts with variable substitution
- **Kernel Filters**: Middleware-like filters for pre/post-processing
- **Streaming Support**: Real-time streaming of AI responses
- **Enterprise Ready**: Production-grade with dependency injection, logging, and telemetry

### Core Philosophy

Semantic Kernel follows a **"code-first"** approach where:
1. You write normal functions in your preferred language (Python, C#, Java)
2. You annotate these functions so AI can understand and call them
3. The kernel orchestrates AI services to accomplish complex tasks using your functions
4. Everything is strongly-typed, testable, and maintainable

---

## System Architecture

### Architectural Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Semantic Kernel Application                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     Application Layer                        │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │   User   │  │  Agents  │  │ Business │  │  Custom  │   │   │
│  │  │   Code   │  │  & Chat  │  │  Logic   │  │ Filters  │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     Kernel Core                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │  Kernel  │  │ Function │  │ Prompt   │  │ Context  │   │   │
│  │  │ Instance │  │Invocation│  │ Renderer │  │ Variables│   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Plugin System                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │  Native  │  │ Semantic │  │  Plugin  │  │ Function │   │   │
│  │  │ Functions│  │ Functions│  │ Registry │  │Metadata  │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Planner Layer                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │Stepwise  │  │Sequential│  │ Handlebars│  │  Auto    │   │   │
│  │  │ Planner  │  │  Planner │  │  Planner │  │Invocation│   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Memory & Storage                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │ Semantic │  │  Vector  │  │  Text    │  │ Volatile │   │   │
│  │  │  Memory  │  │  Store   │  │Embeddings│  │  Memory  │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    AI Service Layer                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │  OpenAI  │  │  Azure   │  │ Hugging  │  │  Custom  │   │   │
│  │  │ Connector│  │  OpenAI  │  │   Face   │  │Connectors│   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │               Observability & Diagnostics                    │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │ Logging  │  │Telemetry │  │  Tracing │  │  Metrics │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Core Components

1. **Kernel**: Central orchestration engine that manages plugins, AI services, and execution
2. **Plugins**: Collections of functions (native or semantic) that AI can invoke
3. **Functions**: Individual units of work - either code-based (native) or prompt-based (semantic)
4. **Planners**: Automatic planning engines that create multi-step execution plans
5. **Memory**: Semantic memory for storing and retrieving contextual information
6. **Connectors**: AI service integrations (OpenAI, Azure OpenAI, etc.)
7. **Filters**: Pre/post-processing hooks for function execution

---

## High-Level System Architecture

### Data Flow Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      Client Application                           │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Kernel Initialization                        │
│  ┌────────────────────────────────────────────────────────┐      │
│  │  1. Create Kernel Builder                              │      │
│  │  2. Add AI Services (OpenAI, Azure OpenAI, etc.)      │      │
│  │  3. Register Plugins & Functions                       │      │
│  │  4. Configure Memory & Storage                         │      │
│  │  5. Add Filters & Middleware                           │      │
│  │  6. Build Kernel Instance                              │      │
│  └────────────────────────────────────────────────────────┘      │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Function Invocation Flow                       │
│                                                                    │
│  User Request                                                      │
│       │                                                            │
│       ▼                                                            │
│  ┌─────────────────┐                                              │
│  │ Kernel.Invoke() │                                              │
│  └────────┬────────┘                                              │
│           │                                                        │
│           ▼                                                        │
│  ┌─────────────────────────────────────────────┐                 │
│  │        Pre-Invocation Filters               │                 │
│  │  - Validate Input                           │                 │
│  │  - Add Telemetry                            │                 │
│  │  - Modify Context                           │                 │
│  └────────────────┬────────────────────────────┘                 │
│                   │                                                │
│                   ▼                                                │
│  ┌─────────────────────────────────────────────┐                 │
│  │        Function Type Detection              │                 │
│  └──────┬──────────────────────┬────────────────┘                │
│         │                      │                                  │
│         ▼                      ▼                                  │
│  ┌──────────────┐      ┌──────────────┐                          │
│  │   Native     │      │   Semantic   │                          │
│  │  Function    │      │   Function   │                          │
│  │  (Code)      │      │  (Prompt)    │                          │
│  └──────┬───────┘      └──────┬───────┘                          │
│         │                      │                                  │
│         │                      ▼                                  │
│         │              ┌──────────────┐                           │
│         │              │   Render     │                           │
│         │              │   Prompt     │                           │
│         │              └──────┬───────┘                           │
│         │                      │                                  │
│         │                      ▼                                  │
│         │              ┌──────────────┐                           │
│         │              │   Call AI    │                           │
│         │              │   Service    │                           │
│         │              └──────┬───────┘                           │
│         │                      │                                  │
│         └──────────┬───────────┘                                  │
│                    │                                               │
│                    ▼                                               │
│  ┌─────────────────────────────────────────────┐                 │
│  │     Function Execution & Result             │                 │
│  └────────────────┬────────────────────────────┘                 │
│                   │                                                │
│                   ▼                                                │
│  ┌─────────────────────────────────────────────┐                 │
│  │        Post-Invocation Filters              │                 │
│  │  - Process Output                           │                 │
│  │  - Log Results                              │                 │
│  │  - Update Metrics                           │                 │
│  └────────────────┬────────────────────────────┘                 │
│                   │                                                │
│                   ▼                                                │
│              Return Result                                         │
└──────────────────────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                  Auto Function Calling Flow                       │
│                    (When AI needs tools)                          │
│                                                                    │
│  AI Response with Function Call                                   │
│       │                                                            │
│       ▼                                                            │
│  ┌─────────────────────────────────────────────┐                 │
│  │   Extract Function Call Request            │                 │
│  │   - Function Name                           │                 │
│  │   - Arguments (JSON)                        │                 │
│  └────────────────┬────────────────────────────┘                 │
│                   │                                                │
│                   ▼                                                │
│  ┌─────────────────────────────────────────────┐                 │
│  │   Lookup Function in Plugin Registry       │                 │
│  └────────────────┬────────────────────────────┘                 │
│                   │                                                │
│                   ▼                                                │
│  ┌─────────────────────────────────────────────┐                 │
│  │   Execute Function with Arguments           │                 │
│  └────────────────┬────────────────────────────┘                 │
│                   │                                                │
│                   ▼                                                │
│  ┌─────────────────────────────────────────────┐                 │
│  │   Return Result to AI for Next Iteration   │                 │
│  └────────────────┬────────────────────────────┘                 │
│                   │                                                │
│                   ▼                                                │
│              Loop Until Complete                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Planner Execution Flow

```
User Goal: "Create a report on Q4 sales and email it to the team"
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                     Planner Invocation                       │
└────────────────────────────────┬────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  Step 1: Plan Generation                     │
│  ┌───────────────────────────────────────────────────┐      │
│  │ Planner sends goal + available functions to AI     │      │
│  │ AI returns structured plan:                        │      │
│  │   1. Call SalesPlugin.GetQ4Data()                  │      │
│  │   2. Call AnalysisPlugin.GenerateReport($data)     │      │
│  │   3. Call EmailPlugin.SendEmail($report, $team)    │      │
│  └───────────────────────────────────────────────────┘      │
└────────────────────────────────┬────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  Step 2: Plan Execution                      │
│  ┌───────────────────────────────────────────────────┐      │
│  │ For each step in plan:                             │      │
│  │   ├─ Invoke function                               │      │
│  │   ├─ Capture result                                │      │
│  │   ├─ Pass result as variable to next step          │      │
│  │   └─ Continue to next step                         │      │
│  └───────────────────────────────────────────────────┘      │
└────────────────────────────────┬────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  Step 3: Result Aggregation                  │
│  ┌───────────────────────────────────────────────────┐      │
│  │ - Compile outputs from all steps                   │      │
│  │ - Format final response                            │      │
│  │ - Return to user                                   │      │
│  └───────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components Deep Dive

### 1. Kernel

The Kernel is the central orchestration component that manages all interactions between your code, AI services, and plugins.

#### Creating a Kernel

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
from semantic_kernel.kernel import KernelArguments
import os
from typing import Annotated

# Method 1: Simple kernel creation
kernel = Kernel()

# Add OpenAI chat completion service
kernel.add_service(
    OpenAIChatCompletion(
        service_id="gpt-4",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

# Method 2: Azure OpenAI
azure_kernel = Kernel()
azure_kernel.add_service(
    AzureChatCompletion(
        service_id="azure-gpt-4",
        deployment_name="gpt-4",
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
    )
)

# Method 3: Multiple services with fallback
multi_service_kernel = Kernel()

# Primary service
multi_service_kernel.add_service(
    AzureChatCompletion(
        service_id="primary",
        deployment_name="gpt-4-turbo",
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
    )
)

# Fallback service
multi_service_kernel.add_service(
    OpenAIChatCompletion(
        service_id="fallback",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
)
```

#### Kernel Configuration

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAITextEmbedding
)
from semantic_kernel.connectors.memory import VolatileMemoryStore
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create kernel with comprehensive configuration
kernel = Kernel()

# Add chat completion service
chat_service = OpenAIChatCompletion(
    service_id="chat",
    ai_model_id="gpt-4-turbo-preview",
    api_key=os.getenv("OPENAI_API_KEY")
)
kernel.add_service(chat_service)

# Add embedding service for memory
embedding_service = OpenAITextEmbedding(
    service_id="embeddings",
    ai_model_id="text-embedding-ada-002",
    api_key=os.getenv("OPENAI_API_KEY")
)
kernel.add_service(embedding_service)

# Configure memory
memory_store = VolatileMemoryStore()
memory = SemanticTextMemory(
    storage=memory_store,
    embeddings_generator=embedding_service
)
kernel.memory = memory

logger.info("Kernel configured successfully")
```

### 2. Plugins

Plugins are collections of functions that extend the kernel's capabilities. They can be native (code-based) or semantic (prompt-based).

#### Native Plugin (Python Functions)

```python
from semantic_kernel.functions import kernel_function
from typing import Annotated
import datetime
import json

class MathPlugin:
    """A plugin that provides mathematical operations."""

    @kernel_function(
        name="add",
        description="Adds two numbers together"
    )
    def add(
        self,
        a: Annotated[float, "The first number"],
        b: Annotated[float, "The second number"]
    ) -> Annotated[float, "The sum of the two numbers"]:
        """Add two numbers."""
        return a + b

    @kernel_function(
        name="multiply",
        description="Multiplies two numbers"
    )
    def multiply(
        self,
        a: Annotated[float, "The first number"],
        b: Annotated[float, "The second number"]
    ) -> Annotated[float, "The product of the two numbers"]:
        """Multiply two numbers."""
        return a * b

    @kernel_function(
        name="calculate_percentage",
        description="Calculates percentage of a number"
    )
    def calculate_percentage(
        self,
        number: Annotated[float, "The base number"],
        percentage: Annotated[float, "The percentage to calculate"]
    ) -> Annotated[float, "The calculated percentage"]:
        """Calculate percentage of a number."""
        return (number * percentage) / 100


class TimePlugin:
    """A plugin for time-related operations."""

    @kernel_function(
        name="get_current_time",
        description="Gets the current time in a specified format"
    )
    def get_current_time(
        self,
        format: Annotated[str, "Time format (e.g., '%Y-%m-%d %H:%M:%S')"] = "%Y-%m-%d %H:%M:%S"
    ) -> Annotated[str, "Current time as string"]:
        """Get current time."""
        return datetime.datetime.now().strftime(format)

    @kernel_function(
        name="get_day_of_week",
        description="Gets the current day of the week"
    )
    def get_day_of_week(self) -> Annotated[str, "Day of week"]:
        """Get current day of week."""
        return datetime.datetime.now().strftime("%A")

    @kernel_function(
        name="calculate_date_difference",
        description="Calculates days between two dates"
    )
    def calculate_date_difference(
        self,
        date1: Annotated[str, "First date (YYYY-MM-DD)"],
        date2: Annotated[str, "Second date (YYYY-MM-DD)"]
    ) -> Annotated[int, "Number of days between dates"]:
        """Calculate difference between two dates."""
        d1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
        return abs((d2 - d1).days)


class DataPlugin:
    """A plugin for data operations."""

    @kernel_function(
        name="format_json",
        description="Formats a Python object as pretty JSON"
    )
    def format_json(
        self,
        data: Annotated[str, "Python dict or list as string"]
    ) -> Annotated[str, "Formatted JSON string"]:
        """Format data as JSON."""
        try:
            obj = eval(data)
            return json.dumps(obj, indent=2)
        except Exception as e:
            return f"Error formatting JSON: {str(e)}"

    @kernel_function(
        name="parse_csv_line",
        description="Parses a CSV line into a list"
    )
    def parse_csv_line(
        self,
        csv_line: Annotated[str, "CSV formatted line"],
        delimiter: Annotated[str, "Delimiter character"] = ","
    ) -> Annotated[str, "Parsed values as JSON list"]:
        """Parse CSV line."""
        values = csv_line.split(delimiter)
        return json.dumps([v.strip() for v in values])


# Register plugins with kernel
kernel.add_plugin(MathPlugin(), plugin_name="Math")
kernel.add_plugin(TimePlugin(), plugin_name="Time")
kernel.add_plugin(DataPlugin(), plugin_name="Data")
```

#### Semantic Plugin (Prompt-based)

```python
from semantic_kernel.prompt_template import PromptTemplateConfig
from semantic_kernel.functions import KernelFunctionFromPrompt

# Create semantic functions using prompts
summarize_prompt = """
Summarize the following text in a concise manner:

{{$input}}

Summary:
"""

summarize_config = PromptTemplateConfig(
    name="summarize",
    description="Summarizes input text concisely",
    template=summarize_prompt,
    execution_settings={
        "temperature": 0.3,
        "max_tokens": 200
    }
)

summarize_function = KernelFunctionFromPrompt(
    function_name="summarize",
    plugin_name="TextProcessing",
    prompt=summarize_prompt,
    prompt_template_config=summarize_config
)

# Add to kernel
kernel.add_function(
    plugin_name="TextProcessing",
    function=summarize_function
)


# More complex semantic function with multiple inputs
translate_prompt = """
Translate the following {{$source_language}} text to {{$target_language}}:

Text: {{$input}}

Translation:
"""

translate_config = PromptTemplateConfig(
    name="translate",
    description="Translates text from one language to another",
    template=translate_prompt,
    input_variables=[
        {"name": "input", "description": "Text to translate"},
        {"name": "source_language", "description": "Source language"},
        {"name": "target_language", "description": "Target language"}
    ],
    execution_settings={
        "temperature": 0.3,
        "max_tokens": 500
    }
)

translate_function = KernelFunctionFromPrompt(
    function_name="translate",
    plugin_name="TextProcessing",
    prompt=translate_prompt,
    prompt_template_config=translate_config
)

kernel.add_function(
    plugin_name="TextProcessing",
    function=translate_function
)


# Sentiment analysis semantic function
sentiment_prompt = """
Analyze the sentiment of the following text and respond with one of:
POSITIVE, NEGATIVE, or NEUTRAL

Also provide a confidence score from 0-100.

Text: {{$input}}

Response format:
Sentiment: [POSITIVE/NEGATIVE/NEUTRAL]
Confidence: [0-100]
Reasoning: [brief explanation]
"""

sentiment_function = KernelFunctionFromPrompt(
    function_name="analyze_sentiment",
    plugin_name="TextProcessing",
    prompt=sentiment_prompt
)

kernel.add_function(
    plugin_name="TextProcessing",
    function=sentiment_function
)
```

### 3. Memory

Semantic Kernel provides memory capabilities for storing and retrieving contextual information using embeddings.

#### Semantic Memory Setup

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding
from semantic_kernel.connectors.memory import VolatileMemoryStore
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
import asyncio

# Create kernel
kernel = Kernel()

# Setup embedding service
embedding_service = OpenAITextEmbedding(
    service_id="embeddings",
    ai_model_id="text-embedding-ada-002",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create memory store (volatile - in-memory)
memory_store = VolatileMemoryStore()

# Create semantic memory
semantic_memory = SemanticTextMemory(
    storage=memory_store,
    embeddings_generator=embedding_service
)

# Attach to kernel
kernel.memory = semantic_memory


async def memory_example():
    collection_name = "technical_docs"

    # Save information to memory
    await kernel.memory.save_information(
        collection=collection_name,
        id="doc1",
        text="Semantic Kernel is an SDK that integrates LLMs with conventional programming languages."
    )

    await kernel.memory.save_information(
        collection=collection_name,
        id="doc2",
        text="Plugins in Semantic Kernel are collections of functions that can be native code or semantic prompts."
    )

    await kernel.memory.save_information(
        collection=collection_name,
        id="doc3",
        text="Planners automatically create multi-step plans to accomplish complex goals."
    )

    await kernel.memory.save_information(
        collection=collection_name,
        id="doc4",
        text="Memory in Semantic Kernel uses embeddings to store and retrieve contextual information."
    )

    print("Information saved to memory\n")

    # Search memory
    query = "How does Semantic Kernel handle complex tasks?"

    print(f"Query: {query}\n")

    results = await kernel.memory.search(
        collection=collection_name,
        query=query,
        limit=2,
        min_relevance_score=0.7
    )

    print("Search results:")
    async for result in results:
        print(f"  Relevance: {result.relevance:.2f}")
        print(f"  Text: {result.text}")
        print(f"  ID: {result.id}\n")

asyncio.run(memory_example())
```

---

## End-to-End Flow

### Complete Execution Flow

```
1. Application Initialization
   │
   ├─► Create Kernel instance
   │
   ├─► Register AI Services
   │   ├─► OpenAI / Azure OpenAI
   │   ├─► Embedding Services
   │   └─► Custom Connectors
   │
   ├─► Register Plugins
   │   ├─► Native Functions (Python code)
   │   ├─► Semantic Functions (Prompts)
   │   └─► Plugin Collections
   │
   ├─► Configure Memory
   │   ├─► Setup Vector Store
   │   ├─► Initialize Embeddings
   │   └─► Create Memory Collections
   │
   └─► Add Filters & Middleware
       ├─► Pre-invocation hooks
       ├─► Post-invocation hooks
       └─► Error handlers
       │
2. User Request Processing
   │
   ├─► Receive user input/goal
   │
   ├─► Determine execution strategy
   │   ├─► Direct function invocation
   │   ├─► Auto function calling
   │   └─► Planner-based execution
   │
   └─► Initialize execution context
       │
3. Function Invocation Path
   │
   ├─► Pre-Invocation Filters Execute
   │   ├─► Validate inputs
   │   ├─► Add telemetry
   │   ├─► Modify context
   │   └─► Security checks
   │
   ├─► Function Type Resolution
   │   │
   │   ├─► Native Function Path
   │   │   ├─► Lookup function in registry
   │   │   ├─► Validate parameters
   │   │   ├─► Execute Python code
   │   │   └─► Capture result
   │   │
   │   └─► Semantic Function Path
   │       ├─► Retrieve prompt template
   │       ├─► Render with variables
   │       ├─► Send to AI service
   │       ├─► Parse AI response
   │       └─► Capture result
   │
   ├─► Post-Invocation Filters Execute
   │   ├─► Validate outputs
   │   ├─► Log results
   │   ├─► Update metrics
   │   └─► Transform response
   │
   └─► Return result to caller
       │
4. Auto Function Calling Flow
   │
   ├─► Send initial request to AI
   │
   ├─► Loop: While AI requests functions
   │   │
   │   ├─► Parse function call request
   │   │   ├─► Extract function name
   │   │   ├─► Extract arguments (JSON)
   │   │   └─► Validate signature
   │   │
   │   ├─► Invoke requested function
   │   │   ├─► Execute via kernel
   │   │   └─► Capture result
   │   │
   │   ├─► Send result back to AI
   │   │
   │   └─► Continue until AI returns final answer
   │
   └─► Return final response
       │
5. Memory Integration Flow
   │
   ├─► Save Operation
   │   ├─► Generate embeddings
   │   ├─► Store in vector database
   │   └─► Index with metadata
   │
   └─► Retrieve Operation
       ├─► Generate query embedding
       ├─► Semantic similarity search
       ├─► Rank results by relevance
       └─► Return top matches
       │
6. Response & Cleanup
   │
   ├─► Format final response
   │
   ├─► Update conversation history
   │
   ├─► Persist state (if configured)
   │
   ├─► Emit telemetry events
   │
   └─► Return to application
```

### Detailed Execution Steps

#### Step 1: Kernel Initialization

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import logging

# 1.1: Create kernel
kernel = Kernel()

# 1.2: Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("semantic_kernel")

# 1.3: Add AI service
chat_service = OpenAIChatCompletion(
    service_id="default",
    ai_model_id="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY")
)
kernel.add_service(chat_service)

logger.info("Kernel initialized with AI service")
```

#### Step 2: Plugin Registration

```python
from semantic_kernel.functions import kernel_function
from typing import Annotated

# 2.1: Define plugin class
class BusinessPlugin:
    @kernel_function(
        name="process_order",
        description="Processes a customer order"
    )
    def process_order(
        self,
        order_id: Annotated[str, "Order ID"],
        customer_id: Annotated[str, "Customer ID"]
    ) -> Annotated[str, "Processing result"]:
        # Business logic here
        return f"Order {order_id} processed for customer {customer_id}"

# 2.2: Register plugin
kernel.add_plugin(BusinessPlugin(), plugin_name="Business")

logger.info("Plugin registered successfully")
```

#### Step 3: Function Invocation

```python
from semantic_kernel.kernel import KernelArguments

# 3.1: Prepare arguments
arguments = KernelArguments(
    order_id="ORD-12345",
    customer_id="CUST-67890"
)

# 3.2: Invoke function
result = await kernel.invoke(
    function_name="process_order",
    plugin_name="Business",
    arguments=arguments
)

# 3.3: Process result
print(f"Result: {result}")
```

---

## Simple Agent Examples

### Example 1: Basic Chat Agent

A simple conversational agent with no tools.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import ChatHistory
import asyncio
import os

async def basic_chat_agent():
    """Simple chat agent with conversation history."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Create chat history
    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are a helpful AI assistant. Provide clear, concise answers."
    )

    print("Chat Agent Started (type 'exit' to quit)")
    print("-" * 50)

    while True:
        # Get user input
        user_input = input("\nYou: ")

        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        # Add user message to history
        chat_history.add_user_message(user_input)

        # Get AI response
        response = await chat_service.get_chat_message_content(
            chat_history=chat_history,
            settings=kernel.get_prompt_execution_settings_from_service_id("chat")
        )

        # Add assistant response to history
        chat_history.add_assistant_message(str(response))

        # Display response
        print(f"\nAssistant: {response}")

# Run the agent
if __name__ == "__main__":
    asyncio.run(basic_chat_agent())
```

### Example 2: Agent with Native Functions

An agent that can use Python functions as tools.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.contents import ChatHistory
from typing import Annotated
import asyncio
import os
import datetime

class UtilityPlugin:
    """Plugin with useful utility functions."""

    @kernel_function(
        name="get_current_time",
        description="Gets the current date and time"
    )
    def get_current_time(self) -> Annotated[str, "Current date and time"]:
        """Returns the current time."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @kernel_function(
        name="calculate",
        description="Performs mathematical calculations"
    )
    def calculate(
        self,
        expression: Annotated[str, "Math expression to evaluate (e.g., '2 + 2')"]
    ) -> Annotated[str, "Calculation result"]:
        """Evaluates a mathematical expression."""
        try:
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error calculating: {str(e)}"

    @kernel_function(
        name="count_words",
        description="Counts the number of words in a text"
    )
    def count_words(
        self,
        text: Annotated[str, "Text to count words in"]
    ) -> Annotated[int, "Word count"]:
        """Counts words in text."""
        return len(text.split())

    @kernel_function(
        name="reverse_text",
        description="Reverses the given text"
    )
    def reverse_text(
        self,
        text: Annotated[str, "Text to reverse"]
    ) -> Annotated[str, "Reversed text"]:
        """Reverses text."""
        return text[::-1]


async def agent_with_tools():
    """Agent with native function calling capabilities."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Add utility plugin
    kernel.add_plugin(UtilityPlugin(), plugin_name="Utilities")

    # Create chat history
    chat_history = ChatHistory()
    chat_history.add_system_message(
        """You are a helpful assistant with access to utility tools.
        Use the available functions when needed to help answer questions."""
    )

    print("Agent with Tools Started")
    print("Available tools: get_current_time, calculate, count_words, reverse_text")
    print("-" * 50)

    # Enable auto function calling
    execution_settings = kernel.get_prompt_execution_settings_from_service_id("chat")
    execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(
        auto_invoke=True,
        filters={"included_plugins": ["Utilities"]}
    )

    # Example queries
    queries = [
        "What time is it?",
        "Calculate 25 * 4 + 10",
        "How many words are in this sentence: The quick brown fox jumps",
        "Reverse this text: Hello World"
    ]

    for query in queries:
        print(f"\nUser: {query}")

        # Add user message
        chat_history.add_user_message(query)

        # Get response with auto function calling
        response = await chat_service.get_chat_message_content(
            chat_history=chat_history,
            settings=execution_settings
        )

        # Add assistant response
        chat_history.add_assistant_message(str(response))

        print(f"Assistant: {response}")

        await asyncio.sleep(1)

# Run the agent
if __name__ == "__main__":
    asyncio.run(agent_with_tools())
```

### Example 3: Agent with Semantic Functions

An agent that uses prompt-based semantic functions.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelFunctionFromPrompt
from semantic_kernel.prompt_template import PromptTemplateConfig
import asyncio
import os

async def agent_with_semantic_functions():
    """Agent with prompt-based semantic functions."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Create semantic function for summarization
    summarize_prompt = """
    Provide a concise summary of the following text in 2-3 sentences:

    {{$input}}

    Summary:
    """

    summarize_function = KernelFunctionFromPrompt(
        function_name="summarize",
        plugin_name="TextProcessing",
        prompt=summarize_prompt,
        prompt_template_config=PromptTemplateConfig(
            description="Summarizes text concisely"
        )
    )

    kernel.add_function(
        plugin_name="TextProcessing",
        function=summarize_function
    )

    # Create semantic function for sentiment analysis
    sentiment_prompt = """
    Analyze the sentiment of the following text.
    Respond with: POSITIVE, NEGATIVE, or NEUTRAL

    Text: {{$input}}

    Sentiment:
    """

    sentiment_function = KernelFunctionFromPrompt(
        function_name="analyze_sentiment",
        plugin_name="TextProcessing",
        prompt=sentiment_prompt,
        prompt_template_config=PromptTemplateConfig(
            description="Analyzes sentiment of text"
        )
    )

    kernel.add_function(
        plugin_name="TextProcessing",
        function=sentiment_function
    )

    # Create semantic function for translation
    translate_prompt = """
    Translate the following text to {{$target_language}}:

    {{$input}}

    Translation:
    """

    translate_function = KernelFunctionFromPrompt(
        function_name="translate",
        plugin_name="TextProcessing",
        prompt=translate_prompt,
        prompt_template_config=PromptTemplateConfig(
            description="Translates text to target language"
        )
    )

    kernel.add_function(
        plugin_name="TextProcessing",
        function=translate_function
    )

    print("Agent with Semantic Functions Started")
    print("-" * 50)

    # Example 1: Summarization
    long_text = """
    Artificial Intelligence has revolutionized numerous industries in recent years.
    From healthcare to finance, AI systems are being deployed to automate tasks,
    improve decision-making, and generate insights from vast amounts of data.
    Machine learning algorithms can now detect patterns that humans might miss,
    leading to more accurate diagnoses in medicine and better fraud detection in
    banking. However, the rapid advancement of AI also raises important ethical
    questions about privacy, bias, and the future of work.
    """

    print("\n=== Summarization Example ===")
    print(f"Original text length: {len(long_text)} characters")

    summary = await kernel.invoke(
        function_name="summarize",
        plugin_name="TextProcessing",
        input=long_text
    )

    print(f"\nSummary: {summary}")

    # Example 2: Sentiment Analysis
    print("\n\n=== Sentiment Analysis Example ===")

    texts = [
        "I absolutely love this product! It exceeded all my expectations.",
        "This is the worst experience I've ever had. Very disappointed.",
        "The item arrived on time and works as described."
    ]

    for text in texts:
        sentiment = await kernel.invoke(
            function_name="analyze_sentiment",
            plugin_name="TextProcessing",
            input=text
        )
        print(f"\nText: {text}")
        print(f"Sentiment: {sentiment}")

    # Example 3: Translation
    print("\n\n=== Translation Example ===")

    text_to_translate = "Hello, how are you today?"
    target_langs = ["Spanish", "French", "German"]

    for lang in target_langs:
        translation = await kernel.invoke(
            function_name="translate",
            plugin_name="TextProcessing",
            input=text_to_translate,
            target_language=lang
        )
        print(f"\n{lang}: {translation}")

# Run the agent
if __name__ == "__main__":
    asyncio.run(agent_with_semantic_functions())
```

### Example 4: Streaming Response Agent

An agent that streams responses in real-time.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import ChatHistory
import asyncio
import os

async def streaming_agent():
    """Agent that streams responses as they're generated."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Create chat history
    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are a helpful assistant that provides detailed explanations."
    )

    print("Streaming Agent Started")
    print("-" * 50)

    # Example queries
    queries = [
        "Explain how quantum computing works",
        "What are the benefits of renewable energy?",
        "Describe the process of photosynthesis"
    ]

    for query in queries:
        print(f"\n\nUser: {query}")
        print("\nAssistant: ", end="", flush=True)

        # Add user message
        chat_history.add_user_message(query)

        # Stream response
        full_response = ""

        async for message in chat_service.get_streaming_chat_message_contents(
            chat_history=chat_history,
            settings=kernel.get_prompt_execution_settings_from_service_id("chat")
        ):
            if message:
                chunk = str(message[0])
                full_response += chunk
                print(chunk, end="", flush=True)

        print()  # New line after streaming completes

        # Add full response to history
        chat_history.add_assistant_message(full_response)

        await asyncio.sleep(2)

# Run the agent
if __name__ == "__main__":
    asyncio.run(streaming_agent())
```

---

## Complex Agent Examples

### Example 1: Research Agent with Memory

An advanced agent that uses semantic memory to store and retrieve information.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAITextEmbedding
)
from semantic_kernel.connectors.memory import VolatileMemoryStore
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.contents import ChatHistory
from typing import Annotated
import asyncio
import os

class ResearchPlugin:
    """Plugin for research-related functions."""

    def __init__(self, kernel: Kernel):
        self.kernel = kernel

    @kernel_function(
        name="save_research",
        description="Saves research findings to memory"
    )
    async def save_research(
        self,
        topic: Annotated[str, "Research topic"],
        findings: Annotated[str, "Research findings to save"]
    ) -> Annotated[str, "Confirmation message"]:
        """Save research findings to semantic memory."""
        collection = "research_database"

        # Generate unique ID
        import hashlib
        research_id = hashlib.md5(f"{topic}{findings}".encode()).hexdigest()[:8]

        # Save to memory
        await self.kernel.memory.save_information(
            collection=collection,
            id=research_id,
            text=findings,
            description=f"Research on: {topic}"
        )

        return f"Saved research on '{topic}' with ID: {research_id}"

    @kernel_function(
        name="search_research",
        description="Searches previous research findings"
    )
    async def search_research(
        self,
        query: Annotated[str, "Search query"]
    ) -> Annotated[str, "Research findings"]:
        """Search semantic memory for relevant research."""
        collection = "research_database"

        results = await self.kernel.memory.search(
            collection=collection,
            query=query,
            limit=3,
            min_relevance_score=0.7
        )

        findings = []
        async for result in results:
            findings.append(f"- {result.text} (Relevance: {result.relevance:.2f})")

        if findings:
            return "Found research:\n" + "\n".join(findings)
        else:
            return "No relevant research found in memory."

    @kernel_function(
        name="synthesize_research",
        description="Synthesizes multiple research findings into a summary"
    )
    async def synthesize_research(
        self,
        topic: Annotated[str, "Topic to synthesize research for"]
    ) -> Annotated[str, "Synthesized summary"]:
        """Synthesize research from memory into a cohesive summary."""
        # Search memory
        search_result = await self.search_research(topic)

        if "No relevant research" in search_result:
            return f"No research found on: {topic}"

        return f"Synthesis for '{topic}':\n{search_result}"


async def research_agent_example():
    """Research agent with semantic memory."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Add embedding service
    embedding_service = OpenAITextEmbedding(
        service_id="embeddings",
        ai_model_id="text-embedding-ada-002",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(embedding_service)

    # Setup memory
    memory_store = VolatileMemoryStore()
    semantic_memory = SemanticTextMemory(
        storage=memory_store,
        embeddings_generator=embedding_service
    )
    kernel.memory = semantic_memory

    # Add research plugin
    research_plugin = ResearchPlugin(kernel)
    kernel.add_plugin(research_plugin, plugin_name="Research")

    print("Research Agent with Memory Started")
    print("-" * 50)

    # Enable auto function calling
    execution_settings = kernel.get_prompt_execution_settings_from_service_id("chat")
    execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(
        auto_invoke=True,
        filters={"included_plugins": ["Research"]}
    )

    # Create chat history
    chat_history = ChatHistory()
    chat_history.add_system_message(
        """You are a research assistant with access to a research database.
        You can save research findings and search for previous research.
        Use the available functions to help answer questions."""
    )

    # Scenario: Multi-turn research conversation
    conversation = [
        "Save this research: AI in healthcare improves diagnostic accuracy by 20%",
        "Save this finding: Machine learning models reduce hospital readmission rates",
        "Save this: Deep learning helps detect cancer in early stages with 95% accuracy",
        "What research do we have on AI healthcare applications?",
        "Synthesize our research on medical AI"
    ]

    for user_message in conversation:
        print(f"\nUser: {user_message}")

        chat_history.add_user_message(user_message)

        response = await chat_service.get_chat_message_content(
            chat_history=chat_history,
            settings=execution_settings
        )

        chat_history.add_assistant_message(str(response))

        print(f"Assistant: {response}")

        await asyncio.sleep(1)

# Run the agent
if __name__ == "__main__":
    asyncio.run(research_agent_example())
```

### Example 2: Planning Agent with Multi-Step Tasks

An agent that breaks down complex tasks into steps.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.contents import ChatHistory
from typing import Annotated
import asyncio
import os
import json
import datetime

class DataPlugin:
    """Plugin for data operations."""

    @kernel_function(
        name="fetch_data",
        description="Fetches data from a specified source"
    )
    def fetch_data(
        self,
        source: Annotated[str, "Data source name"]
    ) -> Annotated[str, "Fetched data as JSON"]:
        """Simulates fetching data."""
        # Simulated data sources
        data_sources = {
            "sales": {"revenue": 1000000, "units": 5000, "growth": "15%"},
            "customers": {"total": 10000, "active": 8500, "churn_rate": "5%"},
            "inventory": {"items": 500, "low_stock": 25, "out_of_stock": 3}
        }

        data = data_sources.get(source.lower(), {})
        return json.dumps(data)

    @kernel_function(
        name="transform_data",
        description="Transforms data to a different format"
    )
    def transform_data(
        self,
        data: Annotated[str, "JSON data to transform"],
        format: Annotated[str, "Target format (csv, xml, summary)"]
    ) -> Annotated[str, "Transformed data"]:
        """Transforms data format."""
        try:
            data_obj = json.loads(data)

            if format.lower() == "csv":
                headers = ",".join(data_obj.keys())
                values = ",".join(str(v) for v in data_obj.values())
                return f"{headers}\n{values}"

            elif format.lower() == "summary":
                summary = f"Data Summary:\n"
                for key, value in data_obj.items():
                    summary += f"- {key}: {value}\n"
                return summary

            else:
                return data

        except Exception as e:
            return f"Error transforming data: {str(e)}"

    @kernel_function(
        name="analyze_data",
        description="Performs analysis on data"
    )
    def analyze_data(
        self,
        data: Annotated[str, "JSON data to analyze"]
    ) -> Annotated[str, "Analysis results"]:
        """Analyzes data and provides insights."""
        try:
            data_obj = json.loads(data)

            analysis = "Data Analysis Results:\n"
            analysis += f"- Number of fields: {len(data_obj)}\n"
            analysis += f"- Fields: {', '.join(data_obj.keys())}\n"

            # Simple numeric analysis
            numeric_fields = {k: v for k, v in data_obj.items()
                            if isinstance(v, (int, float))}

            if numeric_fields:
                analysis += f"- Numeric fields: {len(numeric_fields)}\n"
                total = sum(numeric_fields.values())
                analysis += f"- Total of numeric values: {total}\n"

            return analysis

        except Exception as e:
            return f"Error analyzing data: {str(e)}"


class ReportPlugin:
    """Plugin for report generation."""

    @kernel_function(
        name="create_report",
        description="Creates a formatted report from data"
    )
    def create_report(
        self,
        title: Annotated[str, "Report title"],
        content: Annotated[str, "Report content"],
        format: Annotated[str, "Report format (html, markdown, text)"] = "text"
    ) -> Annotated[str, "Formatted report"]:
        """Creates a formatted report."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if format.lower() == "markdown":
            report = f"""# {title}

Generated: {timestamp}

---

{content}

---

*Report generated by Semantic Kernel Agent*
"""
        else:
            report = f"""
{'=' * 60}
{title.center(60)}
{'=' * 60}

Generated: {timestamp}

{content}

{'=' * 60}
"""

        return report


async def planning_agent_example():
    """Planning agent that breaks down complex tasks."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Add plugins
    kernel.add_plugin(DataPlugin(), plugin_name="Data")
    kernel.add_plugin(ReportPlugin(), plugin_name="Report")

    print("Planning Agent Started")
    print("-" * 50)

    # Enable auto function calling
    execution_settings = kernel.get_prompt_execution_settings_from_service_id("chat")
    execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(
        auto_invoke=True
    )

    chat_history = ChatHistory()
    chat_history.add_system_message(
        """You are a planning assistant that can fetch, transform, analyze data
        and create reports. Break down complex requests into steps and use the
        available functions to accomplish the task."""
    )

    # Complex task
    task = """
    Create a comprehensive sales report:
    1. Fetch sales data
    2. Analyze the sales data
    3. Transform it to summary format
    4. Create a markdown report with all the information
    """

    print(f"\nTask: {task}\n")
    print("Executing plan...\n")

    chat_history.add_user_message(task)

    response = await chat_service.get_chat_message_content(
        chat_history=chat_history,
        settings=execution_settings
    )

    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(response)

# Run the agent
if __name__ == "__main__":
    asyncio.run(planning_agent_example())
```

### Example 3: Workflow Agent with State Management

An agent that maintains state across multiple interactions.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.contents import ChatHistory
from typing import Annotated, Dict, Any
import asyncio
import os
import json

class WorkflowState:
    """Manages workflow state."""

    def __init__(self):
        self.current_step = 0
        self.completed_steps = []
        self.data = {}
        self.history = []

    def to_json(self) -> str:
        """Convert state to JSON."""
        return json.dumps({
            "current_step": self.current_step,
            "completed_steps": self.completed_steps,
            "data": self.data,
            "history": self.history
        }, indent=2)

    def from_json(self, json_str: str):
        """Load state from JSON."""
        data = json.loads(json_str)
        self.current_step = data["current_step"]
        self.completed_steps = data["completed_steps"]
        self.data = data["data"]
        self.history = data["history"]


class WorkflowPlugin:
    """Plugin for workflow management."""

    def __init__(self):
        self.state = WorkflowState()

    @kernel_function(
        name="start_workflow",
        description="Starts a new workflow"
    )
    def start_workflow(
        self,
        workflow_name: Annotated[str, "Name of the workflow"]
    ) -> Annotated[str, "Workflow status"]:
        """Start a new workflow."""
        self.state = WorkflowState()
        self.state.data["workflow_name"] = workflow_name
        self.state.history.append(f"Started workflow: {workflow_name}")
        return f"Workflow '{workflow_name}' started. Current step: 0"

    @kernel_function(
        name="complete_step",
        description="Marks current step as complete and moves to next"
    )
    def complete_step(
        self,
        step_name: Annotated[str, "Name of completed step"],
        result: Annotated[str, "Result of the step"]
    ) -> Annotated[str, "Step completion status"]:
        """Complete current step."""
        self.state.completed_steps.append({
            "step": step_name,
            "result": result
        })
        self.state.current_step += 1
        self.state.history.append(f"Completed step: {step_name}")

        return f"Step '{step_name}' completed. Moving to step {self.state.current_step}"

    @kernel_function(
        name="save_data",
        description="Saves data to workflow state"
    )
    def save_data(
        self,
        key: Annotated[str, "Data key"],
        value: Annotated[str, "Data value"]
    ) -> Annotated[str, "Confirmation message"]:
        """Save data to workflow state."""
        self.state.data[key] = value
        self.state.history.append(f"Saved data: {key}")
        return f"Data saved: {key} = {value}"

    @kernel_function(
        name="get_data",
        description="Retrieves data from workflow state"
    )
    def get_data(
        self,
        key: Annotated[str, "Data key"]
    ) -> Annotated[str, "Data value"]:
        """Get data from workflow state."""
        value = self.state.data.get(key, "Not found")
        return f"{key}: {value}"

    @kernel_function(
        name="get_workflow_status",
        description="Gets current workflow status"
    )
    def get_workflow_status(self) -> Annotated[str, "Workflow status"]:
        """Get workflow status."""
        return self.state.to_json()


async def workflow_agent_example():
    """Workflow agent with state management."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Add workflow plugin
    kernel.add_plugin(WorkflowPlugin(), plugin_name="Workflow")

    print("Workflow Agent Started")
    print("-" * 50)

    # Enable auto function calling
    execution_settings = kernel.get_prompt_execution_settings_from_service_id("chat")
    execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(
        auto_invoke=True,
        filters={"included_plugins": ["Workflow"]}
    )

    chat_history = ChatHistory()
    chat_history.add_system_message(
        """You are a workflow assistant that helps manage multi-step processes.
        Use the workflow functions to track progress and maintain state."""
    )

    # Simulate a multi-step workflow
    steps = [
        "Start a workflow called 'Customer Onboarding'",
        "Save customer name as 'John Doe'",
        "Save customer email as 'john@example.com'",
        "Complete step 'Collect Information' with result 'Customer details collected'",
        "Save account_id as 'ACC-12345'",
        "Complete step 'Create Account' with result 'Account created successfully'",
        "What is the workflow status?"
    ]

    for step in steps:
        print(f"\nUser: {step}")

        chat_history.add_user_message(step)

        response = await chat_service.get_chat_message_content(
            chat_history=chat_history,
            settings=execution_settings
        )

        chat_history.add_assistant_message(str(response))

        print(f"Assistant: {response}")

        await asyncio.sleep(1)

# Run the agent
if __name__ == "__main__":
    asyncio.run(workflow_agent_example())
```

---

## Multi-Agent Systems

### Example 1: Coordinator-Worker Pattern

Multiple agents coordinated by a central coordinator.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents import ChatHistory
from typing import Annotated, List, Dict
import asyncio
import os

class AgentRegistry:
    """Registry of specialized agents."""

    def __init__(self):
        self.agents = {}

    def register(self, name: str, kernel: Kernel):
        """Register an agent."""
        self.agents[name] = kernel

    def get(self, name: str) -> Kernel:
        """Get an agent by name."""
        return self.agents.get(name)

    def list_agents(self) -> List[str]:
        """List all registered agents."""
        return list(self.agents.keys())


class ResearcherPlugin:
    """Plugin for research tasks."""

    @kernel_function(
        name="research_topic",
        description="Researches a given topic"
    )
    async def research_topic(
        self,
        topic: Annotated[str, "Topic to research"]
    ) -> Annotated[str, "Research findings"]:
        """Research a topic."""
        # Simulated research
        findings = f"""Research on {topic}:
- Key finding 1: {topic} is an important area of study
- Key finding 2: Recent developments show promise
- Key finding 3: Future applications are extensive"""
        return findings


class AnalystPlugin:
    """Plugin for analysis tasks."""

    @kernel_function(
        name="analyze_data",
        description="Analyzes provided data"
    )
    async def analyze_data(
        self,
        data: Annotated[str, "Data to analyze"]
    ) -> Annotated[str, "Analysis results"]:
        """Analyze data."""
        # Simulated analysis
        analysis = f"""Analysis Results:
- Data complexity: High
- Key patterns identified: 3
- Recommendations: Further investigation recommended
- Confidence: 85%"""
        return analysis


class WriterPlugin:
    """Plugin for writing tasks."""

    @kernel_function(
        name="write_report",
        description="Writes a report from provided information"
    )
    async def write_report(
        self,
        information: Annotated[str, "Information to include in report"],
        title: Annotated[str, "Report title"]
    ) -> Annotated[str, "Written report"]:
        """Write a report."""
        # Simulated writing
        report = f"""
# {title}

## Executive Summary
This report synthesizes the provided information.

## Details
{information}

## Conclusion
The analysis provides valuable insights for decision-making.
"""
        return report


async def multi_agent_coordinator_example():
    """Multi-agent system with coordinator pattern."""

    # Create agent registry
    registry = AgentRegistry()

    # Create specialized agents
    # Researcher Agent
    researcher_kernel = Kernel()
    researcher_kernel.add_service(
        OpenAIChatCompletion(
            service_id="researcher",
            ai_model_id="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
    researcher_kernel.add_plugin(ResearcherPlugin(), plugin_name="Researcher")
    registry.register("researcher", researcher_kernel)

    # Analyst Agent
    analyst_kernel = Kernel()
    analyst_kernel.add_service(
        OpenAIChatCompletion(
            service_id="analyst",
            ai_model_id="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
    analyst_kernel.add_plugin(AnalystPlugin(), plugin_name="Analyst")
    registry.register("analyst", analyst_kernel)

    # Writer Agent
    writer_kernel = Kernel()
    writer_kernel.add_service(
        OpenAIChatCompletion(
            service_id="writer",
            ai_model_id="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
    writer_kernel.add_plugin(WriterPlugin(), plugin_name="Writer")
    registry.register("writer", writer_kernel)

    print("Multi-Agent System Started")
    print(f"Available agents: {', '.join(registry.list_agents())}")
    print("-" * 60)

    # Coordinate multi-agent workflow
    topic = "Artificial Intelligence in Healthcare"

    print(f"\nTask: Create a comprehensive report on '{topic}'\n")

    # Step 1: Research
    print("Step 1: Researcher Agent - Researching topic...")
    researcher = registry.get("researcher")
    research_result = await researcher.invoke(
        plugin_name="Researcher",
        function_name="research_topic",
        topic=topic
    )
    print(f"Research completed:\n{research_result}\n")

    # Step 2: Analyze
    print("Step 2: Analyst Agent - Analyzing research...")
    analyst = registry.get("analyst")
    analysis_result = await analyst.invoke(
        plugin_name="Analyst",
        function_name="analyze_data",
        data=str(research_result)
    )
    print(f"Analysis completed:\n{analysis_result}\n")

    # Step 3: Write Report
    print("Step 3: Writer Agent - Writing report...")
    writer = registry.get("writer")

    combined_info = f"""
Research Findings:
{research_result}

Analysis:
{analysis_result}
"""

    report = await writer.invoke(
        plugin_name="Writer",
        function_name="write_report",
        information=combined_info,
        title=f"Comprehensive Report: {topic}"
    )

    print("=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(report)

# Run the example
if __name__ == "__main__":
    asyncio.run(multi_agent_coordinator_example())
```

### Example 2: Peer-to-Peer Agent Collaboration

Agents that communicate directly with each other.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents import ChatHistory
from typing import Annotated, Dict, List
import asyncio
import os
import json

class MessageBus:
    """Message bus for agent communication."""

    def __init__(self):
        self.messages = []

    def post_message(self, from_agent: str, to_agent: str, content: str):
        """Post a message."""
        message = {
            "from": from_agent,
            "to": to_agent,
            "content": content,
            "timestamp": asyncio.get_event_loop().time()
        }
        self.messages.append(message)

    def get_messages(self, agent_name: str) -> List[Dict]:
        """Get messages for an agent."""
        return [m for m in self.messages if m["to"] == agent_name]

    def clear_messages(self, agent_name: str):
        """Clear messages for an agent."""
        self.messages = [m for m in self.messages if m["to"] != agent_name]


class CommunicationPlugin:
    """Plugin for inter-agent communication."""

    def __init__(self, agent_name: str, message_bus: MessageBus):
        self.agent_name = agent_name
        self.message_bus = message_bus

    @kernel_function(
        name="send_message",
        description="Sends a message to another agent"
    )
    def send_message(
        self,
        to_agent: Annotated[str, "Recipient agent name"],
        message: Annotated[str, "Message content"]
    ) -> Annotated[str, "Confirmation"]:
        """Send message to another agent."""
        self.message_bus.post_message(self.agent_name, to_agent, message)
        return f"Message sent to {to_agent}"

    @kernel_function(
        name="read_messages",
        description="Reads messages sent to this agent"
    )
    def read_messages(self) -> Annotated[str, "Messages"]:
        """Read messages."""
        messages = self.message_bus.get_messages(self.agent_name)

        if not messages:
            return "No messages"

        result = "Messages:\n"
        for msg in messages:
            result += f"From {msg['from']}: {msg['content']}\n"

        self.message_bus.clear_messages(self.agent_name)
        return result


async def peer_to_peer_agents_example():
    """Peer-to-peer agent collaboration."""

    # Create message bus
    message_bus = MessageBus()

    # Create agents
    agents = {}

    for agent_name in ["Alice", "Bob", "Charlie"]:
        kernel = Kernel()
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=agent_name.lower(),
                ai_model_id="gpt-4",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        # Add communication plugin
        comm_plugin = CommunicationPlugin(agent_name, message_bus)
        kernel.add_plugin(comm_plugin, plugin_name="Communication")

        agents[agent_name] = kernel

    print("Peer-to-Peer Agent System Started")
    print(f"Agents: {', '.join(agents.keys())}")
    print("-" * 60)

    # Scenario: Collaborative problem solving
    print("\nScenario: Agents collaborate on a task\n")

    # Alice sends tasks to Bob and Charlie
    print("Alice: Delegating subtasks...")
    await agents["Alice"].invoke(
        plugin_name="Communication",
        function_name="send_message",
        to_agent="Bob",
        message="Please research market trends"
    )

    await agents["Alice"].invoke(
        plugin_name="Communication",
        function_name="send_message",
        to_agent="Charlie",
        message="Please analyze competitor data"
    )

    # Bob reads messages and responds
    print("\nBob: Checking messages...")
    bob_messages = await agents["Bob"].invoke(
        plugin_name="Communication",
        function_name="read_messages"
    )
    print(f"Bob received: {bob_messages}")

    await agents["Bob"].invoke(
        plugin_name="Communication",
        function_name="send_message",
        to_agent="Alice",
        message="Market trends research complete: Growth in AI sector"
    )

    # Charlie reads messages and responds
    print("\nCharlie: Checking messages...")
    charlie_messages = await agents["Charlie"].invoke(
        plugin_name="Communication",
        function_name="read_messages"
    )
    print(f"Charlie received: {charlie_messages}")

    await agents["Charlie"].invoke(
        plugin_name="Communication",
        function_name="send_message",
        to_agent="Alice",
        message="Competitor analysis complete: 3 main competitors identified"
    )

    # Alice reads responses
    print("\nAlice: Checking responses...")
    alice_messages = await agents["Alice"].invoke(
        plugin_name="Communication",
        function_name="read_messages"
    )
    print(f"Alice received: {alice_messages}")

    print("\n" + "=" * 60)
    print("Collaboration complete!")
    print("=" * 60)

# Run the example
if __name__ == "__main__":
    asyncio.run(peer_to_peer_agents_example())
```

### Example 3: Hierarchical Multi-Agent System

A hierarchical system with manager and worker agents.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.contents import ChatHistory
from typing import Annotated, List, Dict
import asyncio
import os

class TaskQueue:
    """Task queue for distributing work."""

    def __init__(self):
        self.pending_tasks = []
        self.completed_tasks = []

    def add_task(self, task: Dict):
        """Add a task to queue."""
        self.pending_tasks.append(task)

    def get_next_task(self) -> Dict:
        """Get next pending task."""
        if self.pending_tasks:
            return self.pending_tasks.pop(0)
        return None

    def mark_complete(self, task_id: str, result: str):
        """Mark task as complete."""
        self.completed_tasks.append({
            "task_id": task_id,
            "result": result
        })

    def get_progress(self) -> str:
        """Get progress summary."""
        total = len(self.pending_tasks) + len(self.completed_tasks)
        completed = len(self.completed_tasks)
        return f"Progress: {completed}/{total} tasks completed"


class ManagerPlugin:
    """Plugin for manager agent."""

    def __init__(self, task_queue: TaskQueue):
        self.task_queue = task_queue

    @kernel_function(
        name="create_tasks",
        description="Creates and distributes tasks"
    )
    def create_tasks(
        self,
        goal: Annotated[str, "Overall goal"],
        num_tasks: Annotated[int, "Number of subtasks"]
    ) -> Annotated[str, "Task creation status"]:
        """Create tasks."""
        for i in range(num_tasks):
            self.task_queue.add_task({
                "task_id": f"TASK-{i+1}",
                "description": f"Subtask {i+1} for: {goal}",
                "status": "pending"
            })

        return f"Created {num_tasks} tasks for: {goal}"

    @kernel_function(
        name="check_progress",
        description="Checks overall progress"
    )
    def check_progress(self) -> Annotated[str, "Progress report"]:
        """Check progress."""
        return self.task_queue.get_progress()


class WorkerPlugin:
    """Plugin for worker agent."""

    def __init__(self, worker_id: str, task_queue: TaskQueue):
        self.worker_id = worker_id
        self.task_queue = task_queue

    @kernel_function(
        name="get_task",
        description="Gets next available task"
    )
    def get_task(self) -> Annotated[str, "Task details"]:
        """Get next task."""
        task = self.task_queue.get_next_task()
        if task:
            return f"Task assigned: {task['task_id']} - {task['description']}"
        return "No tasks available"

    @kernel_function(
        name="complete_task",
        description="Marks task as complete"
    )
    def complete_task(
        self,
        task_id: Annotated[str, "Task ID"],
        result: Annotated[str, "Task result"]
    ) -> Annotated[str, "Completion status"]:
        """Complete a task."""
        self.task_queue.mark_complete(task_id, result)
        return f"Task {task_id} completed by {self.worker_id}"


async def hierarchical_agents_example():
    """Hierarchical multi-agent system."""

    # Create task queue
    task_queue = TaskQueue()

    # Create manager agent
    manager_kernel = Kernel()
    manager_kernel.add_service(
        OpenAIChatCompletion(
            service_id="manager",
            ai_model_id="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
    manager_kernel.add_plugin(
        ManagerPlugin(task_queue),
        plugin_name="Manager"
    )

    # Create worker agents
    worker_agents = {}
    for i in range(3):
        worker_id = f"Worker-{i+1}"
        worker_kernel = Kernel()
        worker_kernel.add_service(
            OpenAIChatCompletion(
                service_id=worker_id.lower(),
                ai_model_id="gpt-4",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )
        worker_kernel.add_plugin(
            WorkerPlugin(worker_id, task_queue),
            plugin_name="Worker"
        )
        worker_agents[worker_id] = worker_kernel

    print("Hierarchical Multi-Agent System Started")
    print(f"Manager: 1")
    print(f"Workers: {len(worker_agents)}")
    print("-" * 60)

    # Manager creates tasks
    print("\nManager: Creating tasks...")
    result = await manager_kernel.invoke(
        plugin_name="Manager",
        function_name="create_tasks",
        goal="Analyze Q4 Performance",
        num_tasks=5
    )
    print(result)

    # Workers execute tasks
    print("\nWorkers: Executing tasks...")
    for worker_id, worker_kernel in worker_agents.items():
        # Get task
        task_info = await worker_kernel.invoke(
            plugin_name="Worker",
            function_name="get_task"
        )
        print(f"\n{worker_id}: {task_info}")

        # Simulate work
        if "Task assigned" in str(task_info):
            task_id = str(task_info).split(":")[1].split("-")[1].strip().split()[0]
            task_id = f"TASK-{task_id}"

            # Complete task
            completion = await worker_kernel.invoke(
                plugin_name="Worker",
                function_name="complete_task",
                task_id=task_id,
                result=f"Completed by {worker_id}"
            )
            print(f"{worker_id}: {completion}")

    # Manager checks progress
    print("\nManager: Checking progress...")
    progress = await manager_kernel.invoke(
        plugin_name="Manager",
        function_name="check_progress"
    )
    print(progress)

    print("\n" + "=" * 60)
    print("Hierarchical workflow complete!")
    print("=" * 60)

# Run the example
if __name__ == "__main__":
    asyncio.run(hierarchical_agents_example())
```

---

## RAG with Agents (Agentic RAG)

### Example 1: Basic RAG Agent

An agent that retrieves documents and uses them to answer questions.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAITextEmbedding
)
from semantic_kernel.connectors.memory import VolatileMemoryStore
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.contents import ChatHistory
from typing import Annotated
import asyncio
import os

class RAGPlugin:
    """Plugin for RAG operations."""

    def __init__(self, kernel: Kernel):
        self.kernel = kernel

    @kernel_function(
        name="add_document",
        description="Adds a document to the knowledge base"
    )
    async def add_document(
        self,
        content: Annotated[str, "Document content"],
        title: Annotated[str, "Document title"],
        metadata: Annotated[str, "Document metadata (optional)"] = ""
    ) -> Annotated[str, "Confirmation message"]:
        """Add document to knowledge base."""
        import hashlib
        doc_id = hashlib.md5(content.encode()).hexdigest()[:8]

        await self.kernel.memory.save_information(
            collection="knowledge_base",
            id=doc_id,
            text=content,
            description=title
        )

        return f"Added document '{title}' with ID: {doc_id}"

    @kernel_function(
        name="search_documents",
        description="Searches the knowledge base for relevant documents"
    )
    async def search_documents(
        self,
        query: Annotated[str, "Search query"],
        limit: Annotated[int, "Maximum number of results"] = 3
    ) -> Annotated[str, "Retrieved documents"]:
        """Search for relevant documents."""
        results = await self.kernel.memory.search(
            collection="knowledge_base",
            query=query,
            limit=limit,
            min_relevance_score=0.6
        )

        documents = []
        async for result in results:
            documents.append(f"Document (Relevance: {result.relevance:.2f}):\n{result.text}")

        if documents:
            return "\n\n---\n\n".join(documents)
        else:
            return "No relevant documents found."


async def rag_agent_example():
    """RAG agent with semantic search."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Add embedding service
    embedding_service = OpenAITextEmbedding(
        service_id="embeddings",
        ai_model_id="text-embedding-ada-002",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(embedding_service)

    # Setup memory
    memory_store = VolatileMemoryStore()
    semantic_memory = SemanticTextMemory(
        storage=memory_store,
        embeddings_generator=embedding_service
    )
    kernel.memory = semantic_memory

    # Add RAG plugin
    rag_plugin = RAGPlugin(kernel)
    kernel.add_plugin(rag_plugin, plugin_name="RAG")

    print("RAG Agent Started")
    print("-" * 60)

    # Populate knowledge base
    documents = [
        {
            "title": "Python Programming",
            "content": "Python is a high-level programming language known for its simplicity and readability. It's widely used in data science, web development, and automation."
        },
        {
            "title": "Machine Learning Basics",
            "content": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without explicit programming. Common algorithms include decision trees, neural networks, and support vector machines."
        },
        {
            "title": "Data Structures",
            "content": "Data structures are ways of organizing and storing data efficiently. Common data structures include arrays, linked lists, stacks, queues, trees, and graphs."
        },
        {
            "title": "Web Development",
            "content": "Web development involves creating websites and web applications. It typically includes frontend development (HTML, CSS, JavaScript) and backend development (server-side languages and databases)."
        }
    ]

    print("\nPopulating knowledge base...")
    for doc in documents:
        result = await kernel.invoke(
            plugin_name="RAG",
            function_name="add_document",
            content=doc["content"],
            title=doc["title"]
        )
        print(f"  {result}")

    # Enable auto function calling
    execution_settings = kernel.get_prompt_execution_settings_from_service_id("chat")
    execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(
        auto_invoke=True,
        filters={"included_plugins": ["RAG"]}
    )

    chat_history = ChatHistory()
    chat_history.add_system_message(
        """You are a helpful assistant with access to a knowledge base.
        When answering questions, search the knowledge base for relevant information
        and use it to provide accurate, well-informed responses."""
    )

    # Test queries
    queries = [
        "What programming language is good for beginners?",
        "Explain what machine learning is",
        "What are some common data structures?"
    ]

    for query in queries:
        print(f"\n\nUser: {query}")

        chat_history.add_user_message(query)

        response = await chat_service.get_chat_message_content(
            chat_history=chat_history,
            settings=execution_settings
        )

        chat_history.add_assistant_message(str(response))

        print(f"Assistant: {response}")

        await asyncio.sleep(1)

# Run the agent
if __name__ == "__main__":
    asyncio.run(rag_agent_example())
```

### Example 2: Advanced RAG with Reranking

RAG agent with document reranking and source attribution.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAITextEmbedding
)
from semantic_kernel.connectors.memory import VolatileMemoryStore
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.functions import kernel_function, KernelFunctionFromPrompt
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.contents import ChatHistory
from typing import Annotated, List, Dict
import asyncio
import os
import json

class AdvancedRAGPlugin:
    """Advanced RAG plugin with reranking."""

    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.retrieval_cache = []

    @kernel_function(
        name="retrieve_and_rerank",
        description="Retrieves documents and reranks them by relevance"
    )
    async def retrieve_and_rerank(
        self,
        query: Annotated[str, "Search query"],
        limit: Annotated[int, "Number of documents to retrieve"] = 5
    ) -> Annotated[str, "Reranked documents with sources"]:
        """Retrieve and rerank documents."""
        # Initial retrieval
        results = await self.kernel.memory.search(
            collection="knowledge_base",
            query=query,
            limit=limit * 2,  # Retrieve more for reranking
            min_relevance_score=0.5
        )

        documents = []
        async for result in results:
            documents.append({
                "id": result.id,
                "text": result.text,
                "description": result.description,
                "relevance": result.relevance
            })

        if not documents:
            return "No documents found."

        # Rerank (simplified - in production use a reranking model)
        reranked = sorted(documents, key=lambda x: x["relevance"], reverse=True)[:limit]

        # Cache for attribution
        self.retrieval_cache = reranked

        # Format response
        response = "Retrieved Documents:\n\n"
        for i, doc in enumerate(reranked, 1):
            response += f"[Source {i}] {doc['description']}\n"
            response += f"Relevance: {doc['relevance']:.2f}\n"
            response += f"{doc['text']}\n\n"

        return response

    @kernel_function(
        name="get_sources",
        description="Gets the sources for the last retrieval"
    )
    def get_sources(self) -> Annotated[str, "Source attributions"]:
        """Get source attributions."""
        if not self.retrieval_cache:
            return "No recent retrievals."

        sources = "Sources:\n"
        for i, doc in enumerate(self.retrieval_cache, 1):
            sources += f"{i}. {doc['description']} (ID: {doc['id']})\n"

        return sources


async def advanced_rag_example():
    """Advanced RAG agent with reranking."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Add embedding service
    embedding_service = OpenAITextEmbedding(
        service_id="embeddings",
        ai_model_id="text-embedding-ada-002",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(embedding_service)

    # Setup memory
    memory_store = VolatileMemoryStore()
    semantic_memory = SemanticTextMemory(
        storage=memory_store,
        embeddings_generator=embedding_service
    )
    kernel.memory = semantic_memory

    # Add advanced RAG plugin
    rag_plugin = AdvancedRAGPlugin(kernel)
    kernel.add_plugin(rag_plugin, plugin_name="RAG")

    print("Advanced RAG Agent Started")
    print("-" * 60)

    # Populate knowledge base
    documents = [
        ("AI History", "Artificial Intelligence research began in the 1950s with pioneers like Alan Turing and John McCarthy. The Dartmouth Conference in 1956 is often considered the birth of AI as a field."),
        ("Neural Networks", "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information through weighted connections."),
        ("Deep Learning", "Deep learning is a subset of machine learning based on artificial neural networks with multiple layers. It has revolutionized computer vision, natural language processing, and speech recognition."),
        ("AI Applications", "Modern AI applications include autonomous vehicles, medical diagnosis, language translation, recommendation systems, and virtual assistants."),
        ("AI Ethics", "AI ethics addresses concerns about bias, privacy, accountability, and the societal impact of AI systems. Responsible AI development requires careful consideration of these issues.")
    ]

    for title, content in documents:
        import hashlib
        doc_id = hashlib.md5(content.encode()).hexdigest()[:8]

        await kernel.memory.save_information(
            collection="knowledge_base",
            id=doc_id,
            text=content,
            description=title
        )

    print("Knowledge base populated.\n")

    # Enable auto function calling
    execution_settings = kernel.get_prompt_execution_settings_from_service_id("chat")
    execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(
        auto_invoke=True,
        filters={"included_plugins": ["RAG"]}
    )

    chat_history = ChatHistory()
    chat_history.add_system_message(
        """You are an AI research assistant. When answering questions:
        1. Use retrieve_and_rerank to find relevant information
        2. Synthesize information from multiple sources
        3. Cite sources using [Source N] notation
        4. Be accurate and acknowledge if information is uncertain"""
    )

    # Complex query requiring multiple sources
    query = "Explain the history and current applications of AI, including ethical considerations"

    print(f"User: {query}\n")

    chat_history.add_user_message(query)

    response = await chat_service.get_chat_message_content(
        chat_history=chat_history,
        settings=execution_settings
    )

    print(f"Assistant: {response}\n")

    # Get sources
    sources = await kernel.invoke(
        plugin_name="RAG",
        function_name="get_sources"
    )

    print("\n" + "="*60)
    print(sources)
    print("="*60)

# Run the agent
if __name__ == "__main__":
    asyncio.run(advanced_rag_example())
```

### Example 3: Multi-Modal RAG Agent

RAG agent that handles both text and structured data.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAITextEmbedding
)
from semantic_kernel.connectors.memory import VolatileMemoryStore
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.functions import kernel_function
from typing import Annotated
import asyncio
import os
import json

class MultiModalRAGPlugin:
    """Multi-modal RAG plugin."""

    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.structured_data = {}

    @kernel_function(
        name="add_text_document",
        description="Adds a text document to the knowledge base"
    )
    async def add_text_document(
        self,
        content: Annotated[str, "Document content"],
        category: Annotated[str, "Document category"]
    ) -> Annotated[str, "Confirmation"]:
        """Add text document."""
        import hashlib
        doc_id = hashlib.md5(content.encode()).hexdigest()[:8]

        await self.kernel.memory.save_information(
            collection="text_documents",
            id=doc_id,
            text=content,
            description=category
        )

        return f"Added text document to category '{category}'"

    @kernel_function(
        name="add_structured_data",
        description="Adds structured data (tables, JSON) to the knowledge base"
    )
    def add_structured_data(
        self,
        data_id: Annotated[str, "Data identifier"],
        data: Annotated[str, "JSON formatted data"]
    ) -> Annotated[str, "Confirmation"]:
        """Add structured data."""
        try:
            parsed_data = json.loads(data)
            self.structured_data[data_id] = parsed_data
            return f"Added structured data with ID '{data_id}'"
        except json.JSONDecodeError:
            return "Error: Invalid JSON format"

    @kernel_function(
        name="search_text",
        description="Searches text documents"
    )
    async def search_text(
        self,
        query: Annotated[str, "Search query"]
    ) -> Annotated[str, "Search results"]:
        """Search text documents."""
        results = await self.kernel.memory.search(
            collection="text_documents",
            query=query,
            limit=3,
            min_relevance_score=0.6
        )

        docs = []
        async for result in results:
            docs.append(f"[{result.description}] {result.text}")

        return "\n\n".join(docs) if docs else "No documents found."

    @kernel_function(
        name="query_structured_data",
        description="Queries structured data by ID"
    )
    def query_structured_data(
        self,
        data_id: Annotated[str, "Data identifier"]
    ) -> Annotated[str, "Structured data"]:
        """Query structured data."""
        data = self.structured_data.get(data_id)
        if data:
            return json.dumps(data, indent=2)
        return f"No data found with ID '{data_id}'"

    @kernel_function(
        name="list_available_data",
        description="Lists all available structured data IDs"
    )
    def list_available_data(self) -> Annotated[str, "Available data IDs"]:
        """List available data."""
        if not self.structured_data:
            return "No structured data available."

        return "Available data IDs:\n" + "\n".join(f"- {id}" for id in self.structured_data.keys())


async def multimodal_rag_example():
    """Multi-modal RAG agent."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Add embedding service
    embedding_service = OpenAITextEmbedding(
        service_id="embeddings",
        ai_model_id="text-embedding-ada-002",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(embedding_service)

    # Setup memory
    memory_store = VolatileMemoryStore()
    semantic_memory = SemanticTextMemory(
        storage=memory_store,
        embeddings_generator=embedding_service
    )
    kernel.memory = semantic_memory

    # Add multi-modal RAG plugin
    rag_plugin = MultiModalRAGPlugin(kernel)
    kernel.add_plugin(rag_plugin, plugin_name="RAG")

    print("Multi-Modal RAG Agent Started")
    print("-" * 60)

    # Add text documents
    await kernel.invoke(
        plugin_name="RAG",
        function_name="add_text_document",
        content="Q1 2024 showed strong revenue growth of 25% year-over-year driven by new product launches and market expansion.",
        category="Financial Report"
    )

    # Add structured data
    sales_data = {
        "Q1_2024": {"revenue": 5000000, "units_sold": 50000, "growth": "25%"},
        "Q2_2024": {"revenue": 5500000, "units_sold": 55000, "growth": "20%"},
        "Q3_2024": {"revenue": 6000000, "units_sold": 60000, "growth": "18%"}
    }

    await kernel.invoke(
        plugin_name="RAG",
        function_name="add_structured_data",
        data_id="sales_2024",
        data=json.dumps(sales_data)
    )

    print("Knowledge base populated.\n")

    # Enable auto function calling
    execution_settings = kernel.get_prompt_execution_settings_from_service_id("chat")
    execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(
        auto_invoke=True,
        filters={"included_plugins": ["RAG"]}
    )

    chat_history = ChatHistory()
    chat_history.add_system_message(
        """You are a business analyst assistant with access to both text documents
        and structured data. Use the appropriate search functions to find information."""
    )

    # Query combining text and structured data
    query = "What was our Q2 2024 performance? Compare it with other quarters and provide insights."

    print(f"User: {query}\n")

    chat_history.add_user_message(query)

    response = await chat_service.get_chat_message_content(
        chat_history=chat_history,
        settings=execution_settings
    )

    print(f"Assistant: {response}")

# Run the agent
if __name__ == "__main__":
    asyncio.run(multimodal_rag_example())
```

---

## FastMCP Servers with Agents

### Example 1: Semantic Kernel Agent with MCP Server

Integrating Semantic Kernel with MCP (Model Context Protocol) servers.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.contents import ChatHistory
from typing import Annotated, Dict, Any
import asyncio
import os
import json
import httpx

class MCPClientPlugin:
    """Plugin for interacting with MCP servers."""

    def __init__(self, mcp_server_url: str):
        self.mcp_server_url = mcp_server_url
        self.client = httpx.AsyncClient()

    @kernel_function(
        name="call_mcp_tool",
        description="Calls a tool on the MCP server"
    )
    async def call_mcp_tool(
        self,
        tool_name: Annotated[str, "Name of the tool to call"],
        arguments: Annotated[str, "JSON string of arguments"]
    ) -> Annotated[str, "Tool execution result"]:
        """Call MCP tool."""
        try:
            args = json.loads(arguments)

            # Simulated MCP call (replace with actual MCP protocol)
            response = await self.client.post(
                f"{self.mcp_server_url}/tools/{tool_name}",
                json={"arguments": args},
                timeout=30.0
            )

            if response.status_code == 200:
                result = response.json()
                return json.dumps(result.get("result", {}))
            else:
                return f"Error calling tool: {response.status_code}"

        except json.JSONDecodeError:
            return "Error: Invalid JSON arguments"
        except Exception as e:
            return f"Error: {str(e)}"

    @kernel_function(
        name="list_mcp_tools",
        description="Lists available tools on the MCP server"
    )
    async def list_mcp_tools(self) -> Annotated[str, "Available tools"]:
        """List available MCP tools."""
        try:
            # Simulated MCP call
            response = await self.client.get(
                f"{self.mcp_server_url}/tools",
                timeout=10.0
            )

            if response.status_code == 200:
                tools = response.json().get("tools", [])
                return "Available MCP tools:\n" + "\n".join(f"- {tool}" for tool in tools)
            else:
                return "Error retrieving tools list"

        except Exception as e:
            return f"Error: {str(e)}"

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


async def mcp_agent_example():
    """Semantic Kernel agent with MCP server integration."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Add MCP client plugin
    # Note: Replace with actual MCP server URL
    mcp_plugin = MCPClientPlugin(mcp_server_url="http://localhost:8000")
    kernel.add_plugin(mcp_plugin, plugin_name="MCP")

    print("Semantic Kernel Agent with MCP Server")
    print("-" * 60)

    try:
        # Enable auto function calling
        execution_settings = kernel.get_prompt_execution_settings_from_service_id("chat")
        execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(
            auto_invoke=True,
            filters={"included_plugins": ["MCP"]}
        )

        chat_history = ChatHistory()
        chat_history.add_system_message(
            """You are an assistant with access to MCP server tools.
            You can list available tools and call them as needed to help users."""
        )

        # Example interactions
        interactions = [
            "What tools are available on the MCP server?",
            "Use the file_search tool to find Python files",
        ]

        for message in interactions:
            print(f"\nUser: {message}")

            chat_history.add_user_message(message)

            response = await chat_service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings
            )

            chat_history.add_assistant_message(str(response))

            print(f"Assistant: {response}")

            await asyncio.sleep(1)

    finally:
        await mcp_plugin.close()

# Run the agent
if __name__ == "__main__":
    asyncio.run(mcp_agent_example())
```

### Example 2: Multi-MCP Server Agent

Agent that coordinates multiple MCP servers.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from typing import Annotated, Dict
import asyncio
import os

class MultiMCPPlugin:
    """Plugin for managing multiple MCP servers."""

    def __init__(self):
        self.servers = {}

    def register_server(self, name: str, url: str):
        """Register an MCP server."""
        self.servers[name] = {
            "url": url,
            "tools": []  # Would be populated from server discovery
        }

    @kernel_function(
        name="call_server_tool",
        description="Calls a tool on a specific MCP server"
    )
    async def call_server_tool(
        self,
        server_name: Annotated[str, "Name of the MCP server"],
        tool_name: Annotated[str, "Name of the tool"],
        arguments: Annotated[str, "Tool arguments as JSON"]
    ) -> Annotated[str, "Tool result"]:
        """Call tool on specific server."""
        if server_name not in self.servers:
            return f"Server '{server_name}' not found"

        # Simulated tool call
        return f"Called {tool_name} on {server_name} with args: {arguments}"

    @kernel_function(
        name="list_servers",
        description="Lists all registered MCP servers"
    )
    def list_servers(self) -> Annotated[str, "Server list"]:
        """List registered servers."""
        if not self.servers:
            return "No MCP servers registered"

        result = "Registered MCP Servers:\n"
        for name, info in self.servers.items():
            result += f"- {name}: {info['url']}\n"

        return result


async def multi_mcp_example():
    """Agent coordinating multiple MCP servers."""

    # Initialize kernel
    kernel = Kernel()

    # Add chat service
    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Add multi-MCP plugin
    mcp_plugin = MultiMCPPlugin()

    # Register multiple MCP servers
    mcp_plugin.register_server("filesystem", "http://localhost:8001")
    mcp_plugin.register_server("database", "http://localhost:8002")
    mcp_plugin.register_server("api", "http://localhost:8003")

    kernel.add_plugin(mcp_plugin, plugin_name="MCP")

    print("Multi-MCP Server Agent Started")
    print("-" * 60)

    # List servers
    servers = await kernel.invoke(
        plugin_name="MCP",
        function_name="list_servers"
    )
    print(f"\n{servers}")

    # Simulate calling tools on different servers
    print("\n\nCalling tools on different servers:")

    result1 = await kernel.invoke(
        plugin_name="MCP",
        function_name="call_server_tool",
        server_name="filesystem",
        tool_name="read_file",
        arguments='{"path": "/data/file.txt"}'
    )
    print(f"\n{result1}")

    result2 = await kernel.invoke(
        plugin_name="MCP",
        function_name="call_server_tool",
        server_name="database",
        tool_name="query",
        arguments='{"sql": "SELECT * FROM users"}'
    )
    print(f"\n{result2}")

# Run the agent
if __name__ == "__main__":
    asyncio.run(multi_mcp_example())
```

---

## A2A (Agent-to-Agent) Examples

### Example 1: A2A Communication with Semantic Kernel

Implementing Agent-to-Agent protocol with Semantic Kernel.

Reference: https://github.com/a2aproject/a2a-samples

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from typing import Annotated, Dict, List
import asyncio
import os
import json
import uuid

class A2AMessage:
    """A2A protocol message."""

    def __init__(
        self,
        from_agent: str,
        to_agent: str,
        content: str,
        message_type: str = "request"
    ):
        self.id = str(uuid.uuid4())
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.content = content
        self.message_type = message_type

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "from": self.from_agent,
            "to": self.to_agent,
            "content": self.content,
            "type": self.message_type
        }


class A2APlugin:
    """Plugin for A2A communication."""

    def __init__(self, agent_id: str, message_queue: List[A2AMessage]):
        self.agent_id = agent_id
        self.message_queue = message_queue

    @kernel_function(
        name="send_a2a_message",
        description="Sends a message to another agent using A2A protocol"
    )
    def send_a2a_message(
        self,
        to_agent: Annotated[str, "Recipient agent ID"],
        content: Annotated[str, "Message content"],
        message_type: Annotated[str, "Message type (request, response, notification)"] = "request"
    ) -> Annotated[str, "Confirmation"]:
        """Send A2A message."""
        message = A2AMessage(
            from_agent=self.agent_id,
            to_agent=to_agent,
            content=content,
            message_type=message_type
        )

        self.message_queue.append(message)

        return f"Sent {message_type} to {to_agent}: {content[:50]}..."

    @kernel_function(
        name="receive_a2a_messages",
        description="Receives messages sent to this agent"
    )
    def receive_a2a_messages(self) -> Annotated[str, "Received messages"]:
        """Receive A2A messages."""
        messages = [msg for msg in self.message_queue if msg.to_agent == self.agent_id]

        if not messages:
            return "No messages"

        result = f"Received {len(messages)} message(s):\n"
        for msg in messages:
            result += f"- From {msg.from_agent} ({msg.message_type}): {msg.content}\n"

        # Remove received messages
        self.message_queue[:] = [msg for msg in self.message_queue if msg.to_agent != self.agent_id]

        return result


async def a2a_example():
    """A2A communication between agents."""

    # Shared message queue
    message_queue = []

    # Create Agent 1
    agent1_kernel = Kernel()
    agent1_kernel.add_service(
        OpenAIChatCompletion(
            service_id="agent1",
            ai_model_id="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
    agent1_kernel.add_plugin(
        A2APlugin("agent-1", message_queue),
        plugin_name="A2A"
    )

    # Create Agent 2
    agent2_kernel = Kernel()
    agent2_kernel.add_service(
        OpenAIChatCompletion(
            service_id="agent2",
            ai_model_id="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
    agent2_kernel.add_plugin(
        A2APlugin("agent-2", message_queue),
        plugin_name="A2A"
    )

    print("A2A Agent Communication System")
    print("-" * 60)

    # Agent 1 sends request to Agent 2
    print("\n### Agent 1 -> Agent 2 (Request) ###")
    result1 = await agent1_kernel.invoke(
        plugin_name="A2A",
        function_name="send_a2a_message",
        to_agent="agent-2",
        content="Please analyze the Q3 sales data and provide insights",
        message_type="request"
    )
    print(result1)

    # Agent 2 receives message
    print("\n### Agent 2: Receiving Messages ###")
    result2 = await agent2_kernel.invoke(
        plugin_name="A2A",
        function_name="receive_a2a_messages"
    )
    print(result2)

    # Agent 2 sends response to Agent 1
    print("\n### Agent 2 -> Agent 1 (Response) ###")
    result3 = await agent2_kernel.invoke(
        plugin_name="A2A",
        function_name="send_a2a_message",
        to_agent="agent-1",
        content="Analysis complete: Q3 sales increased 15% with strong performance in APAC region",
        message_type="response"
    )
    print(result3)

    # Agent 1 receives response
    print("\n### Agent 1: Receiving Messages ###")
    result4 = await agent1_kernel.invoke(
        plugin_name="A2A",
        function_name="receive_a2a_messages"
    )
    print(result4)

    print("\n" + "=" * 60)
    print("A2A communication complete!")
    print("=" * 60)

# Run the example
if __name__ == "__main__":
    asyncio.run(a2a_example())
```

### Example 2: A2A Task Delegation

Agent delegation using A2A protocol.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from typing import Annotated, Dict, List
import asyncio
import os
import json

class A2ATaskPlugin:
    """A2A plugin for task delegation."""

    def __init__(self, agent_id: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.task_results = {}

    @kernel_function(
        name="advertise_capabilities",
        description="Advertises this agent's capabilities"
    )
    def advertise_capabilities(self) -> Annotated[str, "Capabilities"]:
        """Advertise capabilities."""
        return json.dumps({
            "agent_id": self.agent_id,
            "capabilities": self.capabilities
        })

    @kernel_function(
        name="delegate_task",
        description="Delegates a task to another agent"
    )
    def delegate_task(
        self,
        task: Annotated[str, "Task description"],
        required_capability: Annotated[str, "Required capability"]
    ) -> Annotated[str, "Delegation status"]:
        """Delegate task."""
        return f"Task delegated: {task} (requires: {required_capability})"

    @kernel_function(
        name="execute_task",
        description="Executes a delegated task"
    )
    async def execute_task(
        self,
        task_id: Annotated[str, "Task ID"],
        task_description: Annotated[str, "Task description"]
    ) -> Annotated[str, "Task result"]:
        """Execute task."""
        # Simulated task execution
        result = f"Completed task {task_id}: {task_description}"
        self.task_results[task_id] = result
        return result


async def a2a_delegation_example():
    """A2A task delegation example."""

    # Create specialized agents
    # Data Agent
    data_agent = Kernel()
    data_agent.add_service(
        OpenAIChatCompletion(
            service_id="data_agent",
            ai_model_id="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
    data_agent.add_plugin(
        A2ATaskPlugin("data-agent", ["data_processing", "analytics"]),
        plugin_name="A2A"
    )

    # Report Agent
    report_agent = Kernel()
    report_agent.add_service(
        OpenAIChatCompletion(
            service_id="report_agent",
            ai_model_id="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
    report_agent.add_plugin(
        A2ATaskPlugin("report-agent", ["report_generation", "visualization"]),
        plugin_name="A2A"
    )

    print("A2A Task Delegation System")
    print("-" * 60)

    # Advertise capabilities
    print("\n### Agent Capabilities ###")

    data_caps = await data_agent.invoke(
        plugin_name="A2A",
        function_name="advertise_capabilities"
    )
    print(f"Data Agent: {data_caps}")

    report_caps = await report_agent.invoke(
        plugin_name="A2A",
        function_name="advertise_capabilities"
    )
    print(f"Report Agent: {report_caps}")

    # Delegate tasks
    print("\n### Task Delegation ###")

    delegation1 = await report_agent.invoke(
        plugin_name="A2A",
        function_name="delegate_task",
        task="Analyze sales trends for Q4",
        required_capability="analytics"
    )
    print(f"Report Agent: {delegation1}")

    # Execute task
    print("\n### Task Execution ###")

    execution = await data_agent.invoke(
        plugin_name="A2A",
        function_name="execute_task",
        task_id="TASK-001",
        task_description="Analyze sales trends for Q4"
    )
    print(f"Data Agent: {execution}")

    print("\n" + "=" * 60)
    print("Task delegation complete!")
    print("=" * 60)

# Run the example
if __name__ == "__main__":
    asyncio.run(a2a_delegation_example())
```

---

## Advanced Patterns

### 1. Plugin Composition and Chaining

Composing multiple plugins to create complex workflows.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function, KernelFunctionFromPrompt
from typing import Annotated
import asyncio
import os

# Create composable plugins
class ValidationPlugin:
    """Validates data before processing."""

    @kernel_function(
        name="validate_input",
        description="Validates input data"
    )
    def validate_input(
        self,
        data: Annotated[str, "Data to validate"],
        schema: Annotated[str, "Validation schema"]
    ) -> Annotated[str, "Validation result"]:
        """Validate input."""
        # Simplified validation
        if len(data) > 0:
            return f"VALID: Data passes {schema} validation"
        return "INVALID: Empty data"


class TransformationPlugin:
    """Transforms data."""

    @kernel_function(
        name="transform_data",
        description="Transforms data to target format"
    )
    def transform_data(
        self,
        data: Annotated[str, "Data to transform"],
        target_format: Annotated[str, "Target format"]
    ) -> Annotated[str, "Transformed data"]:
        """Transform data."""
        return f"[{target_format}] {data.upper()}"


class StoragePlugin:
    """Stores processed data."""

    def __init__(self):
        self.storage = {}

    @kernel_function(
        name="store_data",
        description="Stores data in persistent storage"
    )
    def store_data(
        self,
        key: Annotated[str, "Storage key"],
        value: Annotated[str, "Data to store"]
    ) -> Annotated[str, "Storage confirmation"]:
        """Store data."""
        self.storage[key] = value
        return f"Stored data with key: {key}"


async def plugin_composition_example():
    """Plugin composition pattern."""

    kernel = Kernel()

    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )

    # Register plugins
    kernel.add_plugin(ValidationPlugin(), plugin_name="Validator")
    kernel.add_plugin(TransformationPlugin(), plugin_name="Transformer")
    storage_plugin = StoragePlugin()
    kernel.add_plugin(storage_plugin, plugin_name="Storage")

    print("Plugin Composition Pattern")
    print("-" * 60)

    # Chain execution: Validate -> Transform -> Store
    input_data = "Important Business Data"

    # Step 1: Validate
    validation = await kernel.invoke(
        plugin_name="Validator",
        function_name="validate_input",
        data=input_data,
        schema="business_data"
    )
    print(f"\n1. Validation: {validation}")

    # Step 2: Transform
    if "VALID" in str(validation):
        transformation = await kernel.invoke(
            plugin_name="Transformer",
            function_name="transform_data",
            data=input_data,
            target_format="JSON"
        )
        print(f"2. Transformation: {transformation}")

        # Step 3: Store
        storage_result = await kernel.invoke(
            plugin_name="Storage",
            function_name="store_data",
            key="processed_data_001",
            value=str(transformation)
        )
        print(f"3. Storage: {storage_result}")

    print("\nPipeline complete!")

if __name__ == "__main__":
    asyncio.run(plugin_composition_example())
```

### 2. Error Handling and Retry Logic

Robust error handling with automatic retries.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from typing import Annotated
import asyncio
import os
from functools import wraps

def with_retry(max_retries: int = 3, delay: float = 1.0):
    """Decorator for automatic retry logic."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                        await asyncio.sleep(delay)
                    else:
                        print(f"All {max_retries} attempts failed.")

            raise last_exception

        return wrapper
    return decorator


class ResilientPlugin:
    """Plugin with error handling."""

    @kernel_function(
        name="risky_operation",
        description="Performs an operation that might fail"
    )
    @with_retry(max_retries=3, delay=0.5)
    async def risky_operation(
        self,
        data: Annotated[str, "Input data"]
    ) -> Annotated[str, "Operation result"]:
        """Perform risky operation."""
        # Simulated operation that might fail
        import random

        if random.random() < 0.3:  # 30% chance of success
            return f"Successfully processed: {data}"
        else:
            raise Exception("Operation failed - network timeout")


async def error_handling_example():
    """Error handling pattern."""

    kernel = Kernel()

    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )

    kernel.add_plugin(ResilientPlugin(), plugin_name="Resilient")

    print("Error Handling & Retry Pattern")
    print("-" * 60)

    try:
        result = await kernel.invoke(
            plugin_name="Resilient",
            function_name="risky_operation",
            data="Critical business data"
        )
        print(f"\nSuccess: {result}")
    except Exception as e:
        print(f"\nFailed after all retries: {str(e)}")

if __name__ == "__main__":
    asyncio.run(error_handling_example())
```

### 3. Dynamic Plugin Loading

Loading plugins dynamically at runtime.

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from typing import Annotated, Type, Any
import asyncio
import os
import importlib
import inspect


class PluginLoader:
    """Dynamically loads and registers plugins."""

    @staticmethod
    def load_plugin_from_class(
        kernel: Kernel,
        plugin_class: Type,
        plugin_name: str,
        **init_kwargs
    ):
        """Load plugin from class."""
        plugin_instance = plugin_class(**init_kwargs)
        kernel.add_plugin(plugin_instance, plugin_name=plugin_name)
        return plugin_instance

    @staticmethod
    def discover_plugins(kernel: Kernel, plugin_directory: str):
        """Discover and load plugins from directory."""
        # This would scan a directory for plugin classes
        # Simplified example
        discovered_plugins = []
        return discovered_plugins


# Example plugin class
class DynamicMathPlugin:
    """Dynamically loaded math plugin."""

    @kernel_function(
        name="power",
        description="Calculates power of a number"
    )
    def power(
        self,
        base: Annotated[float, "Base number"],
        exponent: Annotated[float, "Exponent"]
    ) -> Annotated[float, "Result"]:
        """Calculate power."""
        return base ** exponent


async def dynamic_loading_example():
    """Dynamic plugin loading pattern."""

    kernel = Kernel()

    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )

    print("Dynamic Plugin Loading Pattern")
    print("-" * 60)

    # Load plugin dynamically
    loader = PluginLoader()
    loader.load_plugin_from_class(
        kernel,
        DynamicMathPlugin,
        "DynamicMath"
    )

    print("\nPlugin loaded dynamically!")

    # Use the dynamically loaded plugin
    result = await kernel.invoke(
        plugin_name="DynamicMath",
        function_name="power",
        base=2.0,
        exponent=10.0
    )

    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(dynamic_loading_example())
```

---

## Production Considerations

### 1. Performance Optimization

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from typing import Annotated
import asyncio
import os
import time
from functools import lru_cache

class PerformancePlugin:
    """Plugin with performance optimizations."""

    def __init__(self):
        self.cache = {}

    @kernel_function(
        name="cached_operation",
        description="Performs operation with caching"
    )
    def cached_operation(
        self,
        key: Annotated[str, "Cache key"]
    ) -> Annotated[str, "Cached result"]:
        """Operation with caching."""
        if key in self.cache:
            return f"CACHED: {self.cache[key]}"

        # Expensive operation
        result = f"Computed result for {key}"
        self.cache[key] = result

        return f"COMPUTED: {result}"

    @kernel_function(
        name="batch_process",
        description="Processes items in batch"
    )
    async def batch_process(
        self,
        items: Annotated[str, "Comma-separated items"]
    ) -> Annotated[str, "Batch result"]:
        """Batch processing."""
        item_list = items.split(",")

        # Process in batches
        batch_size = 10
        results = []

        for i in range(0, len(item_list), batch_size):
            batch = item_list[i:i + batch_size]
            # Process batch
            batch_result = f"Processed {len(batch)} items"
            results.append(batch_result)

        return ", ".join(results)
```

### 2. Security Best Practices

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from typing import Annotated
import asyncio
import os
import re
import hashlib

class SecurityPlugin:
    """Plugin with security features."""

    @kernel_function(
        name="sanitize_input",
        description="Sanitizes user input"
    )
    def sanitize_input(
        self,
        user_input: Annotated[str, "User input to sanitize"]
    ) -> Annotated[str, "Sanitized input"]:
        """Sanitize input to prevent injection attacks."""
        # Remove potentially harmful characters
        sanitized = re.sub(r'[<>\"\'%;()&+]', '', user_input)

        # Limit length
        max_length = 1000
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized

    @kernel_function(
        name="validate_permissions",
        description="Validates user permissions"
    )
    def validate_permissions(
        self,
        user_id: Annotated[str, "User ID"],
        resource: Annotated[str, "Resource to access"],
        action: Annotated[str, "Action to perform"]
    ) -> Annotated[str, "Permission check result"]:
        """Validate permissions."""
        # Simplified permission check
        # In production, check against real auth system
        allowed_actions = ["read", "write"]

        if action in allowed_actions:
            return f"ALLOWED: User {user_id} can {action} {resource}"
        else:
            return f"DENIED: User {user_id} cannot {action} {resource}"

    @kernel_function(
        name="hash_sensitive_data",
        description="Hashes sensitive data"
    )
    def hash_sensitive_data(
        self,
        data: Annotated[str, "Sensitive data"]
    ) -> Annotated[str, "Hashed data"]:
        """Hash sensitive data."""
        return hashlib.sha256(data.encode()).hexdigest()
```

### 3. Monitoring and Observability

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from typing import Annotated
import asyncio
import os
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SemanticKernel")


class MonitoringPlugin:
    """Plugin with monitoring capabilities."""

    def __init__(self):
        self.metrics = {
            "function_calls": 0,
            "errors": 0,
            "total_execution_time": 0.0
        }

    @kernel_function(
        name="tracked_operation",
        description="Operation with monitoring"
    )
    async def tracked_operation(
        self,
        operation: Annotated[str, "Operation to perform"]
    ) -> Annotated[str, "Operation result"]:
        """Operation with tracking."""
        start_time = time.time()

        try:
            # Log function call
            logger.info(f"Starting operation: {operation}")

            # Simulate work
            await asyncio.sleep(0.1)

            # Update metrics
            self.metrics["function_calls"] += 1

            result = f"Completed: {operation}"

            logger.info(f"Operation successful: {operation}")

            return result

        except Exception as e:
            self.metrics["errors"] += 1
            logger.error(f"Operation failed: {operation} - {str(e)}")
            raise

        finally:
            execution_time = time.time() - start_time
            self.metrics["total_execution_time"] += execution_time
            logger.info(f"Execution time: {execution_time:.3f}s")

    @kernel_function(
        name="get_metrics",
        description="Retrieves monitoring metrics"
    )
    def get_metrics(self) -> Annotated[str, "Metrics"]:
        """Get metrics."""
        avg_time = (
            self.metrics["total_execution_time"] / self.metrics["function_calls"]
            if self.metrics["function_calls"] > 0
            else 0
        )

        metrics_report = f"""
Monitoring Metrics:
- Total Function Calls: {self.metrics["function_calls"]}
- Total Errors: {self.metrics["errors"]}
- Total Execution Time: {self.metrics["total_execution_time"]:.3f}s
- Average Execution Time: {avg_time:.3f}s
- Error Rate: {(self.metrics["errors"] / max(self.metrics["function_calls"], 1) * 100):.2f}%
"""
        return metrics_report
```

### 4. Configuration Management

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from typing import Dict, Any
import os
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class SemanticKernelConfig:
    """Configuration for Semantic Kernel application."""

    # AI Service Configuration
    ai_service_type: str = "openai"
    ai_model_id: str = "gpt-4"
    api_key: str = ""
    api_endpoint: str = ""

    # Memory Configuration
    memory_type: str = "volatile"
    memory_connection_string: str = ""

    # Performance Configuration
    max_concurrent_requests: int = 10
    request_timeout: int = 30
    retry_attempts: int = 3

    # Security Configuration
    enable_input_validation: bool = True
    enable_output_filtering: bool = True
    max_input_length: int = 10000

    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "semantic_kernel.log"

    @classmethod
    def from_file(cls, config_path: Path) -> "SemanticKernelConfig":
        """Load configuration from file."""
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
        return cls(**config_dict)

    @classmethod
    def from_environment(cls) -> "SemanticKernelConfig":
        """Load configuration from environment variables."""
        return cls(
            ai_service_type=os.getenv("SK_AI_SERVICE", "openai"),
            ai_model_id=os.getenv("SK_MODEL_ID", "gpt-4"),
            api_key=os.getenv("OPENAI_API_KEY", ""),
            api_endpoint=os.getenv("SK_API_ENDPOINT", ""),
            memory_type=os.getenv("SK_MEMORY_TYPE", "volatile"),
            log_level=os.getenv("SK_LOG_LEVEL", "INFO")
        )


def create_configured_kernel(config: SemanticKernelConfig) -> Kernel:
    """Create kernel with configuration."""
    kernel = Kernel()

    # Add AI service based on configuration
    if config.ai_service_type == "openai":
        kernel.add_service(
            OpenAIChatCompletion(
                service_id="configured_service",
                ai_model_id=config.ai_model_id,
                api_key=config.api_key
            )
        )

    # Configure memory, logging, etc. based on config
    # ...

    return kernel
```

### 5. Testing Strategies

```python
import pytest
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from typing import Annotated
import asyncio


class TestablePlugin:
    """Plugin designed for testing."""

    @kernel_function(
        name="add_numbers",
        description="Adds two numbers"
    )
    def add_numbers(
        self,
        a: Annotated[float, "First number"],
        b: Annotated[float, "Second number"]
    ) -> Annotated[float, "Sum"]:
        """Add two numbers."""
        return a + b


# Unit Tests
@pytest.mark.asyncio
async def test_plugin_function():
    """Test plugin function."""
    plugin = TestablePlugin()
    result = plugin.add_numbers(5, 3)
    assert result == 8


@pytest.mark.asyncio
async def test_kernel_invocation():
    """Test kernel invocation."""
    kernel = Kernel()
    kernel.add_plugin(TestablePlugin(), plugin_name="Math")

    result = await kernel.invoke(
        plugin_name="Math",
        function_name="add_numbers",
        a=10.0,
        b=20.0
    )

    assert result == 30.0


# Integration Tests
@pytest.mark.asyncio
async def test_multi_plugin_workflow():
    """Test workflow with multiple plugins."""
    # Test complete workflow
    pass
```

---

## Conclusion

Microsoft Semantic Kernel provides a powerful, flexible framework for building AI-powered applications with a code-first approach. Its plugin architecture, automatic function calling, and enterprise-ready features make it an excellent choice for production AI systems.

### Key Takeaways

1. **Plugin-Based Architecture**: Semantic Kernel's modular plugin system allows for clean separation of concerns and easy extensibility.

2. **Language Agnostic**: Works seamlessly with multiple programming languages (Python, C#, Java), making it accessible to diverse development teams.

3. **AI Service Flexibility**: Supports multiple AI providers (OpenAI, Azure OpenAI, Hugging Face, custom) with easy switching and fallback mechanisms.

4. **Enterprise Ready**: Built-in support for security, monitoring, error handling, and configuration management.

5. **Multi-Agent Capabilities**: Native support for building complex multi-agent systems with coordination patterns.

6. **RAG Support**: Comprehensive semantic memory and vector search capabilities for RAG implementations.

7. **Integration Friendly**: Easy integration with MCP servers, A2A protocols, and other enterprise systems.

### When to Use Semantic Kernel

Semantic Kernel is ideal for:
- Enterprise applications requiring robust AI integration
- Teams preferring code-first approaches over low-code solutions
- Applications needing multi-AI provider support
- Complex multi-agent systems with orchestration requirements
- Production systems requiring strong typing and testability
- Projects integrating with existing codebases

### Getting Started Resources

- **Official Documentation**: https://learn.microsoft.com/semantic-kernel/
- **GitHub Repository**: https://github.com/microsoft/semantic-kernel
- **Python Samples**: https://github.com/microsoft/semantic-kernel/tree/main/python
- **Community Discord**: https://aka.ms/sk/discord
- **Blog**: https://devblogs.microsoft.com/semantic-kernel/

### Best Practices Summary

1. **Design plugins with single responsibility** - Each plugin should focus on one domain
2. **Use type hints extensively** - Leverage Python's type system for better error catching
3. **Implement proper error handling** - Use try-except blocks and retry logic
4. **Add comprehensive logging** - Enable observability in production
5. **Test plugins independently** - Unit test each plugin before integration
6. **Secure sensitive data** - Never hardcode API keys, use environment variables
7. **Monitor performance** - Track metrics and optimize bottlenecks
8. **Document your plugins** - Clear descriptions help AI understand function purposes
9. **Version your plugins** - Maintain backwards compatibility
10. **Use semantic memory wisely** - Implement proper vector store selection for production

### Future Directions

The Semantic Kernel ecosystem continues to evolve with:
- Enhanced planner capabilities
- Improved multi-agent orchestration
- Better streaming support
- Advanced memory management
- Deeper integration with Azure services
- Expanded LLM provider support

### Final Thoughts

Semantic Kernel represents Microsoft's vision for AI application development: bringing together the power of large language models with the structure and reliability of traditional software engineering. By treating AI capabilities as first-class functions within your codebase, Semantic Kernel enables developers to build sophisticated, maintainable, and production-ready AI systems.

Whether you're building simple chatbots or complex multi-agent systems, Semantic Kernel provides the tools, patterns, and abstractions needed to succeed. Its growing ecosystem and enterprise focus make it a compelling choice for organizations serious about AI integration.

---

**Document Version**: 1.0
**Last Updated**: January 2026
**Framework Version**: Semantic Kernel 1.0+
**Author**: AI Agent Documentation System

---

*This comprehensive guide covers Microsoft Semantic Kernel from fundamentals to advanced production patterns. For the latest updates and community contributions, visit the official Semantic Kernel repository and documentation.*
