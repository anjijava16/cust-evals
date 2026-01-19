# OpenAI Agents Framework: Comprehensive Deep Dive

**Version:** 2.0
**Last Updated:** January 2026
**Framework Type:** Official OpenAI Agentic AI Framework

---

## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 [Overview](#11-overview)
   - 1.2 [Key Features](#12-key-features)
   - 1.3 [Evolution: From Assistants API to Agents SDK](#13-evolution-from-assistants-api-to-agents-sdk)
   - 1.4 [When to Use OpenAI Agents](#14-when-to-use-openai-agents)

2. [System Architecture](#2-system-architecture)
   - 2.1 [High-Level Architecture](#21-high-level-architecture)
   - 2.2 [Component Interaction Diagrams](#22-component-interaction-diagrams)
   - 2.3 [Request/Response Flow](#23-requestresponse-flow)
   - 2.4 [Multi-Agent Architecture](#24-multi-agent-architecture)

3. [Core Components Deep Dive](#3-core-components-deep-dive)
   - 3.1 [Agents](#31-agents)
   - 3.2 [Tools](#32-tools)
   - 3.3 [Handoffs](#33-handoffs)
   - 3.4 [Guardrails](#34-guardrails)
   - 3.5 [Tracing](#35-tracing)
   - 3.6 [Responses API](#36-responses-api)

4. [End-to-End Flow](#4-end-to-end-flow)
   - 4.1 [Agent Initialization](#41-agent-initialization)
   - 4.2 [Message Processing](#42-message-processing)
   - 4.3 [Tool Execution](#43-tool-execution)
   - 4.4 [Response Generation](#44-response-generation)

5. [Simple Agent Examples](#5-simple-agent-examples)
   - 5.1 [Basic Chat Agent](#51-basic-chat-agent)
   - 5.2 [Weather Information Agent](#52-weather-information-agent)
   - 5.3 [Calculator Agent](#53-calculator-agent)
   - 5.4 [Data Analysis Agent](#54-data-analysis-agent)
   - 5.5 [Task Management Agent](#55-task-management-agent)

6. [Complex Agent Examples](#6-complex-agent-examples)
   - 6.1 [Customer Support Agent with Context](#61-customer-support-agent-with-context)
   - 6.2 [Research Assistant with Web Search](#62-research-assistant-with-web-search)
   - 6.3 [Code Review Agent](#63-code-review-agent)
   - 6.4 [Financial Analysis Agent](#64-financial-analysis-agent)

7. [Multi-Agent Systems](#7-multi-agent-systems)
   - 7.1 [Triage and Routing System](#71-triage-and-routing-system)
   - 7.2 [Software Development Team](#72-software-development-team)
   - 7.3 [Customer Service Hierarchy](#73-customer-service-hierarchy)
   - 7.4 [Research and Analysis Pipeline](#74-research-and-analysis-pipeline)

8. [RAG with Agents / Agentic RAG](#8-rag-with-agents--agentic-rag)
   - 8.1 [File Search Basics](#81-file-search-basics)
   - 8.2 [Vector Store RAG Agent](#82-vector-store-rag-agent)
   - 8.3 [Multi-Document RAG Agent](#83-multi-document-rag-agent)
   - 8.4 [Hybrid Search Agent](#84-hybrid-search-agent)

9. [FastMCP Servers with Agents](#9-fastmcp-servers-with-agents)
   - 9.1 [Building a FastMCP Server](#91-building-a-fastmcp-server)
   - 9.2 [Integrating FastMCP with OpenAI Agents](#92-integrating-fastmcp-with-openai-agents)
   - 9.3 [Custom Tools via MCP](#93-custom-tools-via-mcp)

10. [A2A Agent-to-Agent Examples](#10-a2a-agent-to-agent-examples)
    - 10.1 [Agent Card Protocol](#101-agent-card-protocol)
    - 10.2 [Peer-to-Peer Agent Communication](#102-peer-to-peer-agent-communication)
    - 10.3 [Cross-Organization Agent Collaboration](#103-cross-organization-agent-collaboration)

11. [Advanced Patterns](#11-advanced-patterns)
    - 11.1 [Streaming Responses](#111-streaming-responses)
    - 11.2 [Polling and Status Monitoring](#112-polling-and-status-monitoring)
    - 11.3 [Error Handling and Retries](#113-error-handling-and-retries)
    - 11.4 [Context Management](#114-context-management)
    - 11.5 [Parallel Tool Execution](#115-parallel-tool-execution)

12. [Production Considerations](#12-production-considerations)
    - 12.1 [Rate Limits and Quotas](#121-rate-limits-and-quotas)
    - 12.2 [Cost Optimization](#122-cost-optimization)
    - 12.3 [Security Best Practices](#123-security-best-practices)
    - 12.4 [Monitoring and Observability](#124-monitoring-and-observability)
    - 12.5 [Deployment Strategies](#125-deployment-strategies)

13. [Conclusion](#13-conclusion)
    - 13.1 [Summary](#131-summary)
    - 13.2 [Best Practices](#132-best-practices)
    - 13.3 [Resources](#133-resources)

---

## 1. Introduction

### 1.1 Overview

The **OpenAI Agents Framework** represents the evolution of OpenAI's approach to building agentic AI applications. As of January 2026, OpenAI has transitioned from the Assistants API (which will sunset on August 26, 2026) to a more powerful and flexible ecosystem consisting of:

- **Responses API**: A new API primitive combining the simplicity of Chat Completions with advanced tool-use capabilities
- **Agents SDK**: A lightweight, production-ready framework for building multi-agent workflows
- **AgentKit**: Visual tools including Agent Builder, Connector Registry, and ChatKit for simplified agent development

The framework enables developers to build sophisticated AI agents that can:
- Use external tools and APIs
- Access knowledge bases through RAG (Retrieval-Augmented Generation)
- Collaborate in multi-agent systems
- Handle complex workflows with handoffs between specialized agents
- Execute code, search the web, and generate images
- Connect to enterprise systems via Model Context Protocol (MCP)

### 1.2 Key Features

#### **1. Agents SDK Core Features**

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenAI Agents SDK                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Agents     │  │    Tools     │  │  Handoffs    │     │
│  │              │  │              │  │              │     │
│  │ - LLMs with  │  │ - Function   │  │ - Agent      │     │
│  │   instructions│  │   calling    │  │   delegation │     │
│  │ - Context    │  │ - Built-in   │  │ - Context    │     │
│  │ - Memory     │  │   tools      │  │   transfer   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Guardrails   │  │   Tracing    │  │ Multi-Model  │     │
│  │              │  │              │  │              │     │
│  │ - Input      │  │ - Debugging  │  │ - OpenAI     │     │
│  │   validation │  │ - Monitoring │  │ - 100+ LLMs  │     │
│  │ - Output     │  │ - Logging    │  │ - Provider   │     │
│  │   validation │  │              │  │   agnostic   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

**Key Capabilities:**

1. **Function Calling**: Wrap any Python function as a tool with automatic schema generation
2. **Built-in Tools**:
   - `WebSearchTool`: Search the web
   - `FileSearchTool`: Retrieve from vector stores
   - `CodeInterpreterTool`: Execute code in sandboxed environments
   - `ImageGenerationTool`: Generate images from prompts
   - `HostedMCPTool`: Expose remote MCP server tools

3. **Agents as Tools**: Expose agents as callable tools for hierarchical agent systems
4. **Guardrails**: Validate inputs and outputs to ensure safe, reliable behavior
5. **Tracing**: Built-in observability for debugging and monitoring agent flows
6. **Provider Agnostic**: Support for OpenAI and 100+ other LLM providers

#### **2. Responses API Features**

The Responses API is OpenAI's successor to the Assistants API, offering:

- **Hosted Tools**: Tools that run on OpenAI's infrastructure (web search, file search, computer use)
- **Streaming Support**: Real-time streaming of responses and tool calls
- **Built-in RAG**: Native vector store integration for knowledge retrieval
- **MCP Integration**: Connect to Model Context Protocol servers
- **Simplified API**: Single endpoint for complex agentic workflows

#### **3. AgentKit Features**

- **Agent Builder**: Visual canvas for creating multi-agent workflows
- **Connector Registry**: Manage data sources and tool integrations
- **ChatKit**: Embed agent experiences into applications
- **Pre-built Templates**: Accelerate development with tested patterns

### 1.3 Evolution: From Assistants API to Agents SDK

```
Timeline: OpenAI Agents Evolution
════════════════════════════════════════════════════════════════

2023                2024                2025                2026
  │                   │                   │                   │
  │                   │                   │                   │
  ▼                   ▼                   ▼                   ▼
┌─────────┐      ┌─────────┐      ┌─────────────┐     ┌─────────────┐
│ Chat    │      │Assistants│      │  Responses  │     │  AgentKit   │
│Completions─────▶   API    │──────▶     API      │─────▶   Launch    │
│   API   │      │  Beta   │      │             │     │             │
└─────────┘      └─────────┘      │  Agents SDK │     │ Production  │
                                  │   Release   │     │   Ready     │
                 ┌─────────┐      └─────────────┘     └─────────────┘
                 │ Swarm   │             │                   │
                 │Experiment───────────────────────────▶ Deprecated  │
                 └─────────┘                           │ Aug 26, 2026│
                                                       └─────────────┘

Key Changes:
───────────
✓ Function Calling → Tool Use (enhanced)
✓ Simple Threads → Multi-Agent Workflows
✓ Basic RAG → Advanced Vector Store Integration
✓ Manual Orchestration → Built-in Handoffs
✓ Limited Observability → Full Tracing
✓ OpenAI Only → Provider Agnostic (100+ LLMs)
```

**Migration Path:**

The Assistants API is being deprecated on August 26, 2026. Developers must migrate to:
1. **Responses API** for hosted tools and RAG capabilities
2. **Agents SDK** for multi-agent orchestration and custom workflows
3. **Chat Completions API** for simple, stateless interactions

### 1.4 When to Use OpenAI Agents

**Use OpenAI Agents When:**

✅ Building conversational AI with tool use
✅ Creating RAG applications with vector stores
✅ Orchestrating multi-agent workflows
✅ Requiring hosted tools (web search, code execution)
✅ Building customer support, research, or analysis systems
✅ Need observability and tracing
✅ Want visual workflow building (AgentKit)

**Consider Alternatives When:**

❌ Simple prompt-response patterns (use Chat Completions)
❌ Need complete control over LLM interactions
❌ Extremely latency-sensitive applications
❌ Very high-volume, low-complexity tasks
❌ Budget constraints (agents can be more expensive)

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌───────────────────────────────────────────────────────────────────────────┐
│                         OpenAI Agents Ecosystem                           │
└───────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌────────────────┐         ┌────────────────┐
│  Responses    │          │   Agents SDK   │         │   AgentKit     │
│     API       │          │                │         │                │
│               │          │  - Orchestration│         │  - Visual      │
│  - Hosted     │◄────────▶│  - Multi-Agent │◄───────▶│    Builder     │
│    Tools      │          │  - Handoffs    │         │  - Templates   │
│  - Streaming  │          │  - Guardrails  │         │  - Connectors  │
│  - RAG        │          │  - Tracing     │         │                │
└───────┬───────┘          └────────┬───────┘         └────────────────┘
        │                           │
        │                           │
        └───────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────────────────────┐
    │           Core Infrastructure                 │
    ├───────────────────────────────────────────────┤
    │                                               │
    │  ┌──────────────┐  ┌──────────────┐         │
    │  │   Language   │  │    Vector    │         │
    │  │    Models    │  │    Stores    │         │
    │  │              │  │              │         │
    │  │ - GPT-4      │  │ - Embeddings │         │
    │  │ - GPT-4o     │  │ - Search     │         │
    │  │ - o1         │  │ - Storage    │         │
    │  └──────────────┘  └──────────────┘         │
    │                                               │
    │  ┌──────────────┐  ┌──────────────┐         │
    │  │  Built-in    │  │     MCP      │         │
    │  │    Tools     │  │  Servers     │         │
    │  │              │  │              │         │
    │  │ - Web Search │  │ - FastMCP    │         │
    │  │ - Code Exec  │  │ - Custom     │         │
    │  │ - File Search│  │ - Enterprise │         │
    │  └──────────────┘  └──────────────┘         │
    └───────────────────────────────────────────────┘
```

### 2.2 Component Interaction Diagrams

#### **Agent Execution Flow**

```
┌──────────┐                                           ┌──────────┐
│  Client  │                                           │ OpenAI   │
│Application│                                          │  API     │
└─────┬────┘                                           └────┬─────┘
      │                                                     │
      │  1. Initialize Agent                               │
      │────────────────────────────────────────────────────▶│
      │                                                     │
      │  2. Agent Configuration Stored                     │
      │◄────────────────────────────────────────────────────│
      │                                                     │
      │  3. Send Message                                   │
      │────────────────────────────────────────────────────▶│
      │                                                     │
      │              ┌──────────────────┐                  │
      │              │  LLM Processing  │                  │
      │              │                  │                  │
      │              │  - Analyze Query │                  │
      │              │  - Select Tools  │                  │
      │              │  - Generate Args │                  │
      │              └──────────────────┘                  │
      │                                                     │
      │  4. Tool Call Request                              │
      │◄────────────────────────────────────────────────────│
      │                                                     │
      │  5. Execute Tool Locally                           │
      ├─────────────────┐                                  │
      │                 │                                  │
      │  ┌──────────────▼───────────┐                     │
      │  │   Tool Execution         │                     │
      │  │                          │                     │
      │  │  - API Calls             │                     │
      │  │  - Database Queries      │                     │
      │  │  - Computations          │                     │
      │  └──────────────┬───────────┘                     │
      │                 │                                  │
      │◄────────────────┘                                  │
      │                                                     │
      │  6. Return Tool Results                            │
      │────────────────────────────────────────────────────▶│
      │                                                     │
      │              ┌──────────────────┐                  │
      │              │  LLM Synthesis   │                  │
      │              │                  │                  │
      │              │  - Process Results│                 │
      │              │  - Generate Response│               │
      │              └──────────────────┘                  │
      │                                                     │
      │  7. Final Response                                 │
      │◄────────────────────────────────────────────────────│
      │                                                     │
```

#### **Multi-Agent Handoff Flow**

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│   Triage   │     │  Research  │     │  Analysis  │     │  Response  │
│   Agent    │     │   Agent    │     │   Agent    │     │   Agent    │
└──────┬─────┘     └──────┬─────┘     └──────┬─────┘     └──────┬─────┘
       │                  │                  │                  │
       │ 1. User Query    │                  │                  │
       │◄─────────        │                  │                  │
       │                  │                  │                  │
       │ 2. Analyze &     │                  │                  │
       │    Route         │                  │                  │
       ├──────────────────▶                  │                  │
       │ Handoff Context  │                  │                  │
       │                  │                  │                  │
       │                  │ 3. Gather Data   │                  │
       │                  │   (Web Search,   │                  │
       │                  │    APIs, etc.)   │                  │
       │                  │                  │                  │
       │                  │ 4. Handoff to    │                  │
       │                  │    Analysis      │                  │
       │                  ├──────────────────▶                  │
       │                  │ Context + Data   │                  │
       │                  │                  │                  │
       │                  │                  │ 5. Process &     │
       │                  │                  │    Synthesize    │
       │                  │                  │                  │
       │                  │                  │ 6. Handoff to    │
       │                  │                  │    Response      │
       │                  │                  ├──────────────────▶
       │                  │                  │ Findings         │
       │                  │                  │                  │
       │                  │                  │                  │ 7. Format &
       │                  │                  │                  │    Deliver
       │                  │                  │                  │
       │◄─────────────────────────────────────────────────────────
       │                  Final Response                        │
       │                  │                  │                  │
```

### 2.3 Request/Response Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Detailed Request/Response Cycle                  │
└─────────────────────────────────────────────────────────────────────┘

Phase 1: Initialization
━━━━━━━━━━━━━━━━━━━━━━
┌─────────────┐
│   Client    │
│ Creates     │──────┐
│   Agent     │      │
└─────────────┘      │
                     ▼
              ┌──────────────┐
              │  Agent Config│
              │              │
              │ - Name       │
              │ - Model      │
              │ - Instructions│
              │ - Tools      │
              │ - Handoffs   │
              └──────────────┘

Phase 2: Message Processing
━━━━━━━━━━━━━━━━━━━━━━━━━━━
User Message
     │
     ▼
┌─────────────────┐
│ Message Context │
│                 │
│ - History       │
│ - System Prompt │
│ - Available Tools│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Analysis   │
│                 │
│ Input: Context  │
│ Output: Plan    │
└────────┬────────┘
         │
         ▼
    Decision Point
         │
    ┌────┴────┐
    │         │
    ▼         ▼
Direct     Tool Call
Response   Required
    │         │
    │         ▼
    │    ┌─────────────┐
    │    │Tool Selection│
    │    │             │
    │    │ - Tool Name │
    │    │ - Arguments │
    │    └──────┬──────┘
    │           │
    │           ▼
    │    ┌─────────────┐
    │    │  Execute    │
    │    │   Tool      │
    │    └──────┬──────┘
    │           │
    │           ▼
    │    ┌─────────────┐
    │    │Tool Results │
    │    └──────┬──────┘
    │           │
    └───────────┴──────▶ Synthesis
                         │
                         ▼
                  ┌──────────────┐
                  │Final Response│
                  └──────────────┘

Phase 3: Streaming (Optional)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────┐
│Response │
│Chunks   │──▶ Chunk 1 ──▶ Client
└─────────┘
     │
     ├────▶ Chunk 2 ──▶ Client
     │
     ├────▶ Chunk 3 ──▶ Client
     │
     └────▶ [done] ───▶ Client
```

### 2.4 Multi-Agent Architecture

```
┌───────────────────────────────────────────────────────────────────────┐
│                    Multi-Agent System Patterns                        │
└───────────────────────────────────────────────────────────────────────┘

Pattern 1: Sequential Handoff
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent A ──▶ Agent B ──▶ Agent C ──▶ Final Output

Pattern 2: Hierarchical
━━━━━━━━━━━━━━━━━━━━━━
         ┌─────────────┐
         │   Manager   │
         │    Agent    │
         └──────┬──────┘
                │
       ┌────────┼────────┐
       │        │        │
       ▼        ▼        ▼
   ┌──────┐ ┌──────┐ ┌──────┐
   │Agent │ │Agent │ │Agent │
   │  1   │ │  2   │ │  3   │
   └──────┘ └──────┘ └──────┘

Pattern 3: Collaborative
━━━━━━━━━━━━━━━━━━━━━━━━
   ┌──────┐         ┌──────┐
   │Agent │◄───────▶│Agent │
   │  A   │         │  B   │
   └───┬──┘         └───┬──┘
       │      ┌──────┐  │
       └─────▶│Agent │◄─┘
              │  C   │
              └──────┘

Pattern 4: Pipeline
━━━━━━━━━━━━━━━━━━
Input ──▶ [Agent A] ──▶ [Agent B] ──▶ [Agent C] ──▶ Output
           │              │              │
           ▼              ▼              ▼
       Transform      Enrich         Format
```

---

## 3. Core Components Deep Dive

### 3.1 Agents

An **Agent** is the fundamental building block of the OpenAI Agents framework. It combines:
- A language model (LLM)
- Instructions (system prompt)
- Tools (functions the agent can call)
- Context (conversation history and state)

#### **Agent Structure**

```python
from typing import Optional, List, Dict, Any
from openai import OpenAI
from dataclasses import dataclass
import os

@dataclass
class Agent:
    """
    Core Agent representation in OpenAI Agents SDK
    """
    name: str
    model: str = "gpt-4o"
    instructions: str = ""
    tools: List[Dict[str, Any]] = None
    temperature: float = 1.0
    max_tokens: Optional[int] = None

    def __post_init__(self):
        if self.tools is None:
            self.tools = []
```

#### **Agent Lifecycle**

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Lifecycle                          │
└─────────────────────────────────────────────────────────────┘

1. CREATION
   │
   ├─▶ Define Instructions
   ├─▶ Specify Model
   ├─▶ Register Tools
   └─▶ Set Parameters

2. INITIALIZATION
   │
   ├─▶ Load Configuration
   ├─▶ Initialize Tools
   └─▶ Prepare Context

3. EXECUTION
   │
   ├─▶ Receive Message
   ├─▶ Process Context
   ├─▶ Call LLM
   ├─▶ Execute Tools (if needed)
   ├─▶ Synthesize Response
   └─▶ Update State

4. HANDOFF (Optional)
   │
   ├─▶ Transfer Context
   ├─▶ Invoke Target Agent
   └─▶ Return Control

5. TERMINATION
   │
   ├─▶ Cleanup Resources
   ├─▶ Store State
   └─▶ Generate Trace
```

### 3.2 Tools

Tools are functions that agents can call to interact with external systems, perform computations, or access data.

#### **Tool Categories**

```
┌───────────────────────────────────────────────────────────────┐
│                        Tool Types                             │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  1. HOSTED TOOLS (Run on OpenAI infrastructure)              │
│     ┌────────────────────────────────────────────┐           │
│     │ • WebSearchTool      - Web search          │           │
│     │ • FileSearchTool     - Vector store RAG    │           │
│     │ • CodeInterpreterTool - Code execution     │           │
│     │ • ImageGenerationTool - DALL-E integration │           │
│     │ • ComputerUseTool    - GUI interaction     │           │
│     └────────────────────────────────────────────┘           │
│                                                               │
│  2. LOCAL TOOLS (Run in your environment)                    │
│     ┌────────────────────────────────────────────┐           │
│     │ • Function Calling   - Custom Python funcs │           │
│     │ • API Integrations   - External APIs       │           │
│     │ • Database Access    - Query databases     │           │
│     │ • File Operations    - File I/O            │           │
│     └────────────────────────────────────────────┘           │
│                                                               │
│  3. MCP TOOLS (Model Context Protocol)                       │
│     ┌────────────────────────────────────────────┐           │
│     │ • HostedMCPTool      - Remote MCP servers  │           │
│     │ • FastMCP            - FastMCP integration │           │
│     │ • Custom MCP         - Enterprise tools    │           │
│     └────────────────────────────────────────────┘           │
│                                                               │
│  4. AGENT TOOLS (Agents as callable tools)                   │
│     ┌────────────────────────────────────────────┐           │
│     │ • Handoff Agent      - Delegate to agent   │           │
│     │ • Specialized Agent  - Domain expert       │           │
│     └────────────────────────────────────────────┘           │
└───────────────────────────────────────────────────────────────┘
```

#### **Tool Definition Schema**

```python
from typing import Callable, Dict, Any, List
from pydantic import BaseModel, Field
import inspect

class ToolParameter(BaseModel):
    """Parameter definition for a tool"""
    type: str
    description: str
    enum: List[str] = None

class ToolDefinition(BaseModel):
    """
    Complete tool definition following OpenAI function calling schema
    """
    type: str = "function"
    function: Dict[str, Any]

    @classmethod
    def from_function(cls, func: Callable, description: str) -> "ToolDefinition":
        """
        Create tool definition from Python function

        Args:
            func: Python function to wrap
            description: Description of what the tool does

        Returns:
            ToolDefinition object
        """
        # Extract function signature
        sig = inspect.signature(func)
        parameters = {}
        required = []

        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue

            param_type = "string"  # Default
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"

            parameters[param_name] = {
                "type": param_type,
                "description": f"Parameter {param_name}"
            }

            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        return cls(
            type="function",
            function={
                "name": func.__name__,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": required
                }
            }
        )
```

### 3.3 Handoffs

**Handoffs** enable agents to delegate tasks to other specialized agents, transferring context and control.

#### **Handoff Mechanism**

```
┌─────────────────────────────────────────────────────────────┐
│                    Handoff Process                          │
└─────────────────────────────────────────────────────────────┘

Agent A (Source)                    Agent B (Target)
     │                                    │
     │ 1. Determine Handoff Needed        │
     │    (Based on task complexity)      │
     │                                    │
     │ 2. Prepare Context                 │
     ├────────────────────────────────────┤
     │    Context Package:                │
     │    - Conversation history          │
     │    - Current state                 │
     │    - Task parameters               │
     │    - Constraints                   │
     ├────────────────────────────────────┤
     │                                    │
     │ 3. Invoke Target Agent             │
     │────────────────────────────────────▶
     │                                    │
     │                                    │ 4. Receive Context
     │                                    │
     │                                    │ 5. Execute Task
     │                                    │    - Process request
     │                                    │    - Use tools
     │                                    │    - Generate result
     │                                    │
     │ 6. Return Result                   │
     │◄────────────────────────────────────
     │                                    │
     │ 7. Continue or Return to User      │
     │                                    │
```

#### **Handoff Implementation**

```python
from enum import Enum
from typing import Optional, Dict, Any, Callable

class HandoffType(Enum):
    """Types of agent handoffs"""
    SEQUENTIAL = "sequential"      # A → B → C (linear chain)
    CONDITIONAL = "conditional"    # A → B or C (based on condition)
    RETURN = "return"             # A → B → A (return to original)
    ESCALATION = "escalation"     # Junior → Senior agent
    SPECIALIZATION = "specialization"  # General → Domain expert

class Handoff:
    """
    Represents a handoff configuration
    """
    def __init__(
        self,
        target_agent: str,
        handoff_type: HandoffType = HandoffType.SEQUENTIAL,
        condition: Optional[Callable] = None,
        context_filter: Optional[Callable] = None
    ):
        self.target_agent = target_agent
        self.handoff_type = handoff_type
        self.condition = condition
        self.context_filter = context_filter

    def should_handoff(self, context: Dict[str, Any]) -> bool:
        """Determine if handoff should occur"""
        if self.condition is None:
            return True
        return self.condition(context)

    def prepare_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Filter and prepare context for target agent"""
        if self.context_filter is None:
            return context
        return self.context_filter(context)
```

### 3.4 Guardrails

**Guardrails** validate agent inputs and outputs to ensure safe, reliable, and compliant behavior.

#### **Guardrail Architecture**

```
┌───────────────────────────────────────────────────────────────┐
│                    Guardrail System                           │
└───────────────────────────────────────────────────────────────┘

INPUT VALIDATION                OUTPUT VALIDATION
       │                               │
       ▼                               ▼
┌──────────────┐              ┌──────────────┐
│ Pre-Process  │              │ Post-Process │
│  Guardrails  │              │  Guardrails  │
├──────────────┤              ├──────────────┤
│              │              │              │
│ • Content    │              │ • Content    │
│   Safety     │              │   Safety     │
│ • Input      │              │ • Output     │
│   Validation │              │   Validation │
│ • Rate       │              │ • PII        │
│   Limiting   │              │   Detection  │
│ • Auth       │              │ • Fact       │
│   Check      │              │   Checking   │
│              │              │ • Toxicity   │
│              │              │   Filter     │
└──────┬───────┘              └──────┬───────┘
       │                             │
       ▼                             ▼
   ┌────────┐                    ┌────────┐
   │ Allow  │                    │ Allow  │
   │  or    │                    │  or    │
   │ Reject │                    │ Reject │
   └────────┘                    └────────┘
```

#### **Guardrail Implementation**

```python
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
import re

class Guardrail(ABC):
    """Base class for all guardrails"""

    @abstractmethod
    def validate(self, data: Any) -> tuple[bool, Optional[str]]:
        """
        Validate data against guardrail rules

        Returns:
            (is_valid, error_message)
        """
        pass

class InputGuardrail(Guardrail):
    """Validates input before agent processing"""
    pass

class OutputGuardrail(Guardrail):
    """Validates output before returning to user"""
    pass

class ContentSafetyGuardrail(Guardrail):
    """Check for unsafe content"""

    def __init__(self, blocked_terms: List[str]):
        self.blocked_terms = blocked_terms

    def validate(self, data: str) -> tuple[bool, Optional[str]]:
        """Check if content contains blocked terms"""
        data_lower = data.lower()
        for term in self.blocked_terms:
            if term.lower() in data_lower:
                return False, f"Content contains blocked term: {term}"
        return True, None

class PIIDetectionGuardrail(OutputGuardrail):
    """Detect and prevent PII in responses"""

    def validate(self, data: str) -> tuple[bool, Optional[str]]:
        """Detect common PII patterns"""
        # Email pattern
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data):
            return False, "Response contains email address"

        # SSN pattern (US)
        if re.search(r'\b\d{3}-\d{2}-\d{4}\b', data):
            return False, "Response contains SSN"

        # Credit card pattern
        if re.search(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', data):
            return False, "Response contains credit card number"

        return True, None

class GuardrailManager:
    """Manages and executes guardrails"""

    def __init__(self):
        self.input_guardrails: List[InputGuardrail] = []
        self.output_guardrails: List[OutputGuardrail] = []

    def add_input_guardrail(self, guardrail: InputGuardrail):
        """Add input validation guardrail"""
        self.input_guardrails.append(guardrail)

    def add_output_guardrail(self, guardrail: OutputGuardrail):
        """Add output validation guardrail"""
        self.output_guardrails.append(guardrail)

    def validate_input(self, data: Any) -> tuple[bool, List[str]]:
        """Validate input against all input guardrails"""
        errors = []
        for guardrail in self.input_guardrails:
            is_valid, error_msg = guardrail.validate(data)
            if not is_valid:
                errors.append(error_msg)
        return len(errors) == 0, errors

    def validate_output(self, data: Any) -> tuple[bool, List[str]]:
        """Validate output against all output guardrails"""
        errors = []
        for guardrail in self.output_guardrails:
            is_valid, error_msg = guardrail.validate(data)
            if not is_valid:
                errors.append(error_msg)
        return len(errors) == 0, errors
```

### 3.5 Tracing

**Tracing** provides observability into agent execution, enabling debugging, monitoring, and optimization.

#### **Trace Structure**

```
┌───────────────────────────────────────────────────────────────┐
│                    Agent Execution Trace                      │
└───────────────────────────────────────────────────────────────┘

Trace ID: trace_abc123
Timestamp: 2026-01-19T10:30:00Z
Duration: 2.3s

┌─ Agent: CustomerSupportAgent ────────────────────────────────┐
│  Model: gpt-4o                                                │
│  Instructions: "You are a helpful customer support agent..."  │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─ Step 1: Message Received ─────────────────────┐          │
│  │  Timestamp: 10:30:00.000                        │          │
│  │  Content: "I need help with my order #12345"   │          │
│  └─────────────────────────────────────────────────┘          │
│                                                               │
│  ┌─ Step 2: LLM Call ──────────────────────────────┐         │
│  │  Timestamp: 10:30:00.100                        │          │
│  │  Tokens: 150 input, 0 output                    │          │
│  │  Decision: Call tool "get_order_details"        │          │
│  └─────────────────────────────────────────────────┘          │
│                                                               │
│  ┌─ Step 3: Tool Execution ─────────────────────────┐        │
│  │  Tool: get_order_details                        │          │
│  │  Arguments: {"order_id": "12345"}               │          │
│  │  Duration: 0.5s                                 │          │
│  │  Result: {order details...}                     │          │
│  └─────────────────────────────────────────────────┘          │
│                                                               │
│  ┌─ Step 4: LLM Synthesis ──────────────────────────┐        │
│  │  Timestamp: 10:30:00.700                        │          │
│  │  Tokens: 300 input, 150 output                  │          │
│  │  Response generated                             │          │
│  └─────────────────────────────────────────────────┘          │
│                                                               │
│  ┌─ Step 5: Response Delivered ────────────────────┐         │
│  │  Timestamp: 10:30:02.300                        │          │
│  │  Content: "Your order #12345 is..."            │          │
│  └─────────────────────────────────────────────────┘          │
│                                                               │
└───────────────────────────────────────────────────────────────┘

Metrics:
  Total Duration: 2.3s
  LLM Calls: 2
  Tool Calls: 1
  Tokens: 450 input, 150 output
  Cost: $0.0045
```

#### **Tracing Implementation**

```python
from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class TraceStep:
    """Individual step in agent execution"""
    step_type: str  # "message", "llm_call", "tool_call", "response"
    timestamp: str
    content: Dict[str, Any]
    duration: float = 0.0

@dataclass
class AgentTrace:
    """Complete trace of agent execution"""
    trace_id: str
    agent_name: str
    model: str
    start_time: str
    end_time: Optional[str] = None
    steps: List[TraceStep] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def add_step(self, step: TraceStep):
        """Add a step to the trace"""
        self.steps.append(step)

    def finalize(self):
        """Finalize the trace with metrics"""
        self.end_time = datetime.now().isoformat()

        # Calculate metrics
        start = datetime.fromisoformat(self.start_time)
        end = datetime.fromisoformat(self.end_time)
        total_duration = (end - start).total_seconds()

        llm_calls = sum(1 for s in self.steps if s.step_type == "llm_call")
        tool_calls = sum(1 for s in self.steps if s.step_type == "tool_call")

        self.metrics = {
            "total_duration": total_duration,
            "llm_calls": llm_calls,
            "tool_calls": tool_calls,
            "total_steps": len(self.steps)
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary"""
        return {
            "trace_id": self.trace_id,
            "agent_name": self.agent_name,
            "model": self.model,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "steps": [
                {
                    "step_type": s.step_type,
                    "timestamp": s.timestamp,
                    "content": s.content,
                    "duration": s.duration
                }
                for s in self.steps
            ],
            "metrics": self.metrics
        }

class TracingManager:
    """Manages tracing for agents"""

    def __init__(self):
        self.traces: Dict[str, AgentTrace] = {}

    def create_trace(self, trace_id: str, agent_name: str, model: str) -> AgentTrace:
        """Create a new trace"""
        trace = AgentTrace(
            trace_id=trace_id,
            agent_name=agent_name,
            model=model,
            start_time=datetime.now().isoformat()
        )
        self.traces[trace_id] = trace
        return trace

    def get_trace(self, trace_id: str) -> Optional[AgentTrace]:
        """Get a trace by ID"""
        return self.traces.get(trace_id)

    def export_trace(self, trace_id: str, format: str = "json") -> str:
        """Export trace in specified format"""
        trace = self.get_trace(trace_id)
        if not trace:
            return None

        if format == "json":
            return json.dumps(trace.to_dict(), indent=2)
        else:
            return str(trace.to_dict())
```

### 3.6 Responses API

The **Responses API** is OpenAI's new primitive for building agents, replacing the Assistants API.

#### **Key Differences from Chat Completions**

```
┌───────────────────────────────────────────────────────────────┐
│          Chat Completions vs Responses API                    │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  CHAT COMPLETIONS API                                         │
│  ┌────────────────────────────────────────────────┐           │
│  │ • Stateless                                    │           │
│  │ • Manual tool orchestration                    │           │
│  │ • Client manages context                       │           │
│  │ • Lower latency                                │           │
│  │ • Full control over flow                       │           │
│  └────────────────────────────────────────────────┘           │
│                                                               │
│  RESPONSES API                                                │
│  ┌────────────────────────────────────────────────┐           │
│  │ • Stateful (threads)                           │           │
│  │ • Automatic tool orchestration                 │           │
│  │ • Server manages context                       │           │
│  │ • Built-in hosted tools                        │           │
│  │ • RAG with vector stores                       │           │
│  │ • Simplified multi-turn conversations          │           │
│  └────────────────────────────────────────────────┘           │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## 4. End-to-End Flow

### 4.1 Agent Initialization

```python
from openai import OpenAI
from typing import List, Dict, Any, Optional, Callable
import os

class AgentFramework:
    """
    Complete agent initialization and management
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the agent framework

        Args:
            api_key: OpenAI API key (defaults to env variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required")

        self.client = OpenAI(api_key=self.api_key)
        self.agents = {}
        self.tools = {}

    def register_tool(self, name: str, tool_def: Dict[str, Any], func: Callable):
        """
        Register a tool for use by agents

        Args:
            name: Tool name
            tool_def: OpenAI tool definition
            func: Python function to execute
        """
        self.tools[name] = {
            "definition": tool_def,
            "function": func
        }

    def create_agent(
        self,
        name: str,
        model: str = "gpt-4o",
        instructions: str = "",
        tools: List[str] = None
    ) -> str:
        """
        Create and register an agent

        Args:
            name: Agent name
            model: Model to use
            instructions: System instructions
            tools: List of tool names to attach

        Returns:
            Agent ID
        """
        agent_tools = []
        if tools:
            for tool_name in tools:
                if tool_name in self.tools:
                    agent_tools.append(self.tools[tool_name]["definition"])

        agent_config = {
            "name": name,
            "model": model,
            "instructions": instructions,
            "tools": agent_tools,
            "tool_functions": {
                t: self.tools[t]["function"]
                for t in tools if t in self.tools
            } if tools else {}
        }

        self.agents[name] = agent_config
        return name

    def get_agent(self, name: str) -> Dict[str, Any]:
        """Get agent configuration"""
        return self.agents.get(name)
```

### 4.2 Message Processing

```python
import json
from typing import List, Dict, Any, Optional, Generator

class MessageProcessor:
    """
    Handles message processing for agents
    """

    def __init__(self, client: OpenAI, agent_config: Dict[str, Any]):
        self.client = client
        self.agent_config = agent_config
        self.conversation_history: List[Dict[str, str]] = []

    def process_message(
        self,
        user_message: str,
        stream: bool = False
    ) -> str:
        """
        Process a user message through the agent

        Args:
            user_message: User's input message
            stream: Whether to stream the response

        Returns:
            Agent's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Prepare messages with system instructions
        messages = [
            {"role": "system", "content": self.agent_config["instructions"]}
        ] + self.conversation_history

        # Make initial LLM call
        response = self.client.chat.completions.create(
            model=self.agent_config["model"],
            messages=messages,
            tools=self.agent_config["tools"] if self.agent_config["tools"] else None,
            tool_choice="auto" if self.agent_config["tools"] else None,
            stream=stream
        )

        if stream:
            return self._handle_streaming_response(response, messages)
        else:
            return self._handle_response(response, messages)

    def _handle_response(
        self,
        response: Any,
        messages: List[Dict[str, str]]
    ) -> str:
        """
        Handle non-streaming response with potential tool calls

        Args:
            response: OpenAI API response
            messages: Current message history

        Returns:
            Final response text
        """
        message = response.choices[0].message

        # Check if tool calls are requested
        if message.tool_calls:
            # Add assistant message with tool calls to history
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            # Execute tool calls
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Execute the tool
                tool_result = self._execute_tool(function_name, function_args)

                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })

            # Make follow-up LLM call with tool results
            follow_up_response = self.client.chat.completions.create(
                model=self.agent_config["model"],
                messages=messages,
                tools=self.agent_config["tools"] if self.agent_config["tools"] else None
            )

            final_message = follow_up_response.choices[0].message.content
        else:
            final_message = message.content

        # Add assistant response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": final_message
        })

        return final_message

    def _execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function

        Args:
            function_name: Name of the function to call
            arguments: Function arguments

        Returns:
            Tool execution result
        """
        if function_name in self.agent_config["tool_functions"]:
            func = self.agent_config["tool_functions"][function_name]
            try:
                result = func(**arguments)
                return {"success": True, "result": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {"success": False, "error": f"Tool {function_name} not found"}
```

### 4.3 Tool Execution

```python
from typing import Callable, Dict, Any, List
import inspect

class ToolExecutor:
    """
    Manages tool registration and execution
    """

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        func: Callable,
        description: str,
        parameters_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Register a function as a tool

        Args:
            func: Python function to register
            description: Description of what the function does
            parameters_schema: Optional custom parameter schema

        Returns:
            OpenAI tool definition
        """
        # Auto-generate schema if not provided
        if parameters_schema is None:
            parameters_schema = self._generate_schema(func)

        tool_def = {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": description,
                "parameters": parameters_schema
            }
        }

        self.tools[func.__name__] = {
            "definition": tool_def,
            "function": func
        }

        return tool_def

    def _generate_schema(self, func: Callable) -> Dict[str, Any]:
        """
        Auto-generate JSON schema from function signature

        Args:
            func: Function to analyze

        Returns:
            JSON schema for function parameters
        """
        sig = inspect.signature(func)
        properties = {}
        required = []

        for param_name, param in sig.parameters.items():
            # Determine type
            param_type = "string"
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == list or param.annotation == List:
                    param_type = "array"
                elif param.annotation == dict or param.annotation == Dict:
                    param_type = "object"

            properties[param_name] = {
                "type": param_type,
                "description": f"Parameter {param_name}"
            }

            # Check if required
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

    def execute(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a registered tool

        Args:
            function_name: Name of the tool to execute
            arguments: Arguments to pass to the tool

        Returns:
            Tool execution result
        """
        if function_name not in self.tools:
            raise ValueError(f"Tool '{function_name}' not registered")

        func = self.tools[function_name]["function"]

        try:
            result = func(**arguments)
            return result
        except Exception as e:
            raise RuntimeError(f"Tool execution failed: {str(e)}")

    def get_definitions(self, tool_names: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Get tool definitions for specified tools or all tools

        Args:
            tool_names: Optional list of specific tools to get

        Returns:
            List of tool definitions
        """
        if tool_names is None:
            return [tool["definition"] for tool in self.tools.values()]
        else:
            return [
                self.tools[name]["definition"]
                for name in tool_names
                if name in self.tools
            ]
```

### 4.4 Response Generation

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentResponse:
    """
    Structured agent response
    """
    content: str
    role: str = "assistant"
    timestamp: datetime = None
    tool_calls: List[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.tool_calls is None:
            self.tool_calls = []
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "content": self.content,
            "role": self.role,
            "timestamp": self.timestamp.isoformat(),
            "tool_calls": self.tool_calls,
            "metadata": self.metadata
        }

class ResponseGenerator:
    """
    Handles response generation and formatting
    """

    def __init__(self, client: OpenAI, agent_config: Dict[str, Any]):
        self.client = client
        self.agent_config = agent_config

    def generate(
        self,
        messages: List[Dict[str, str]],
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Generate a response from the agent

        Args:
            messages: Conversation messages
            context: Additional context for generation

        Returns:
            AgentResponse object
        """
        # Add system message if not present
        if not messages or messages[0].get("role") != "system":
            messages = [
                {"role": "system", "content": self.agent_config["instructions"]}
            ] + messages

        # Make LLM call
        response = self.client.chat.completions.create(
            model=self.agent_config["model"],
            messages=messages,
            tools=self.agent_config.get("tools"),
            temperature=self.agent_config.get("temperature", 1.0),
            max_tokens=self.agent_config.get("max_tokens")
        )

        message = response.choices[0].message

        # Extract tool calls if present
        tool_calls = []
        if message.tool_calls:
            tool_calls = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]

        # Create response object
        agent_response = AgentResponse(
            content=message.content or "",
            tool_calls=tool_calls,
            metadata={
                "model": self.agent_config["model"],
                "finish_reason": response.choices[0].finish_reason,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        )

        return agent_response
```

---

## 5. Simple Agent Examples

### 5.1 Basic Chat Agent

```python
"""
Basic Chat Agent
================
A simple conversational agent without tools.
"""

from openai import OpenAI
from typing import List, Dict
import os

class BasicChatAgent:
    """
    Simple chat agent for general conversation
    """

    def __init__(self, api_key: str = None, model: str = "gpt-4o"):
        """
        Initialize chat agent

        Args:
            api_key: OpenAI API key
            model: Model to use
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = "You are a helpful, friendly AI assistant."

    def chat(self, user_message: str) -> str:
        """
        Send a message and get a response

        Args:
            user_message: User's input

        Returns:
            Agent's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Prepare messages with system prompt
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history

        # Get response from LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )

        assistant_message = response.choices[0].message.content

        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def reset(self):
        """Clear conversation history"""
        self.conversation_history = []

    def set_system_prompt(self, prompt: str):
        """Update system prompt"""
        self.system_prompt = prompt


def main():
    """Example usage"""
    # Initialize agent
    agent = BasicChatAgent()

    print("Basic Chat Agent")
    print("=" * 50)
    print("Type 'quit' to exit, 'reset' to clear history\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'reset':
            agent.reset()
            print("Conversation history cleared.\n")
            continue

        response = agent.chat(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
```

### 5.2 Weather Information Agent

```python
"""
Weather Information Agent
=========================
Agent with function calling for weather queries.
"""

from openai import OpenAI
from typing import Dict, Any, List
import os
import json

class WeatherAgent:
    """
    Agent that can fetch weather information using tools
    """

    def __init__(self, api_key: str = None):
        """Initialize weather agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
        self.conversation_history: List[Dict[str, Any]] = []

        # Define tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g., San Francisco, CA"
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "Temperature unit"
                            }
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_forecast",
                    "description": "Get weather forecast for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state"
                            },
                            "days": {
                                "type": "integer",
                                "description": "Number of days for forecast (1-7)"
                            }
                        },
                        "required": ["location", "days"]
                    }
                }
            }
        ]

    def get_current_weather(self, location: str, unit: str = "fahrenheit") -> Dict[str, Any]:
        """
        Simulate getting current weather
        (In production, this would call a real weather API)
        """
        # Simulated data
        weather_data = {
            "location": location,
            "temperature": 72 if unit == "fahrenheit" else 22,
            "unit": unit,
            "conditions": "Partly cloudy",
            "humidity": 65,
            "wind_speed": 10
        }
        return weather_data

    def get_forecast(self, location: str, days: int) -> Dict[str, Any]:
        """
        Simulate getting weather forecast
        """
        forecast = {
            "location": location,
            "days": days,
            "forecast": [
                {
                    "day": i + 1,
                    "high": 75 - i,
                    "low": 60 - i,
                    "conditions": "Sunny" if i % 2 == 0 else "Cloudy"
                }
                for i in range(days)
            ]
        }
        return forecast

    def execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool function"""
        if function_name == "get_current_weather":
            return self.get_current_weather(**arguments)
        elif function_name == "get_forecast":
            return self.get_forecast(**arguments)
        else:
            return {"error": f"Unknown function: {function_name}"}

    def chat(self, user_message: str) -> str:
        """
        Process user message with tool support

        Args:
            user_message: User's query

        Returns:
            Agent's response
        """
        # Add user message
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        messages = [
            {
                "role": "system",
                "content": "You are a helpful weather assistant. Use the provided tools to answer weather questions."
            }
        ] + self.conversation_history

        # Initial LLM call
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Handle tool calls
        if message.tool_calls:
            # Add assistant message with tool calls
            self.conversation_history.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            # Execute tools
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                tool_result = self.execute_tool(function_name, function_args)

                # Add tool result
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })

            # Get final response with tool results
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful weather assistant."
                }
            ] + self.conversation_history

            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            final_message = final_response.choices[0].message.content
        else:
            final_message = message.content

        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": final_message
        })

        return final_message


def main():
    """Example usage"""
    agent = WeatherAgent()

    print("Weather Information Agent")
    print("=" * 50)

    # Example queries
    queries = [
        "What's the weather in San Francisco?",
        "Can you give me a 5-day forecast for New York City?",
        "How's the weather in London in celsius?"
    ]

    for query in queries:
        print(f"\nUser: {query}")
        response = agent.chat(query)
        print(f"Agent: {response}")


if __name__ == "__main__":
    main()
```

### 5.3 Calculator Agent

```python
"""
Calculator Agent
================
Agent with mathematical calculation capabilities.
"""

from openai import OpenAI
from typing import Dict, Any, List
import os
import json
import math

class CalculatorAgent:
    """
    Agent that can perform mathematical calculations
    """

    def __init__(self, api_key: str = None):
        """Initialize calculator agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"

        # Define calculation tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "Perform basic arithmetic calculations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "scientific_calc",
                    "description": "Perform scientific calculations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "operation": {
                                "type": "string",
                                "enum": ["sqrt", "pow", "log", "sin", "cos", "tan"],
                                "description": "Scientific operation"
                            },
                            "value": {
                                "type": "number",
                                "description": "Input value"
                            },
                            "exponent": {
                                "type": "number",
                                "description": "Exponent (for pow operation)"
                            }
                        },
                        "required": ["operation", "value"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "unit_conversion",
                    "description": "Convert between units",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "value": {
                                "type": "number",
                                "description": "Value to convert"
                            },
                            "from_unit": {
                                "type": "string",
                                "description": "Source unit (e.g., 'meters', 'feet', 'celsius')"
                            },
                            "to_unit": {
                                "type": "string",
                                "description": "Target unit"
                            }
                        },
                        "required": ["value", "from_unit", "to_unit"]
                    }
                }
            }
        ]

    def calculate(self, expression: str) -> Dict[str, Any]:
        """
        Safely evaluate a mathematical expression

        Args:
            expression: Math expression as string

        Returns:
            Calculation result
        """
        try:
            # Use eval with restricted namespace for safety
            allowed_names = {
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
                "sum": sum
            }
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return {
                "expression": expression,
                "result": result,
                "success": True
            }
        except Exception as e:
            return {
                "expression": expression,
                "error": str(e),
                "success": False
            }

    def scientific_calc(
        self,
        operation: str,
        value: float,
        exponent: float = None
    ) -> Dict[str, Any]:
        """
        Perform scientific calculations
        """
        try:
            if operation == "sqrt":
                result = math.sqrt(value)
            elif operation == "pow":
                if exponent is None:
                    raise ValueError("Exponent required for pow operation")
                result = math.pow(value, exponent)
            elif operation == "log":
                result = math.log(value)
            elif operation == "sin":
                result = math.sin(value)
            elif operation == "cos":
                result = math.cos(value)
            elif operation == "tan":
                result = math.tan(value)
            else:
                raise ValueError(f"Unknown operation: {operation}")

            return {
                "operation": operation,
                "value": value,
                "result": result,
                "success": True
            }
        except Exception as e:
            return {
                "operation": operation,
                "value": value,
                "error": str(e),
                "success": False
            }

    def unit_conversion(
        self,
        value: float,
        from_unit: str,
        to_unit: str
    ) -> Dict[str, Any]:
        """
        Convert between common units
        """
        # Simplified conversion table
        conversions = {
            ("meters", "feet"): 3.28084,
            ("feet", "meters"): 0.3048,
            ("celsius", "fahrenheit"): lambda x: x * 9/5 + 32,
            ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
            ("kilometers", "miles"): 0.621371,
            ("miles", "kilometers"): 1.60934,
        }

        try:
            key = (from_unit.lower(), to_unit.lower())
            if key in conversions:
                converter = conversions[key]
                if callable(converter):
                    result = converter(value)
                else:
                    result = value * converter

                return {
                    "value": value,
                    "from_unit": from_unit,
                    "to_unit": to_unit,
                    "result": result,
                    "success": True
                }
            else:
                return {
                    "error": f"Conversion from {from_unit} to {to_unit} not supported",
                    "success": False
                }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    def execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool"""
        if function_name == "calculate":
            return self.calculate(**arguments)
        elif function_name == "scientific_calc":
            return self.scientific_calc(**arguments)
        elif function_name == "unit_conversion":
            return self.unit_conversion(**arguments)
        else:
            return {"error": f"Unknown function: {function_name}", "success": False}

    def process(self, user_message: str) -> str:
        """
        Process calculation request

        Args:
            user_message: User's calculation query

        Returns:
            Calculation result
        """
        messages = [
            {
                "role": "system",
                "content": "You are a helpful calculator assistant. Use the provided tools to perform calculations and unit conversions."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        # Initial LLM call
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Handle tool calls
        if message.tool_calls:
            # Execute all tool calls
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                tool_result = self.execute_tool(function_name, function_args)

                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": function_name,
                            "arguments": tool_call.function.arguments
                        }
                    }]
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })

            # Get final response
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            return final_response.choices[0].message.content
        else:
            return message.content


def main():
    """Example usage"""
    agent = CalculatorAgent()

    print("Calculator Agent")
    print("=" * 50)

    # Example calculations
    queries = [
        "What is 125 * 47?",
        "Calculate the square root of 144",
        "Convert 100 degrees Fahrenheit to Celsius",
        "What's the sine of 45 degrees?",
        "How many meters is 10 feet?"
    ]

    for query in queries:
        print(f"\nUser: {query}")
        response = agent.process(query)
        print(f"Agent: {response}")


if __name__ == "__main__":
    main()
```

### 5.4 Data Analysis Agent

```python
"""
Data Analysis Agent
===================
Agent for analyzing datasets and generating insights.
"""

from openai import OpenAI
from typing import Dict, Any, List, Optional
import os
import json
import statistics

class DataAnalysisAgent:
    """
    Agent that can analyze data and generate statistical insights
    """

    def __init__(self, api_key: str = None):
        """Initialize data analysis agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
        self.datasets: Dict[str, List[float]] = {}

        # Define analysis tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "create_dataset",
                    "description": "Create a named dataset from a list of numbers",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name for the dataset"
                            },
                            "data": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "List of numeric values"
                            }
                        },
                        "required": ["name", "data"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_statistics",
                    "description": "Calculate statistical measures for a dataset",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "dataset_name": {
                                "type": "string",
                                "description": "Name of the dataset to analyze"
                            }
                        },
                        "required": ["dataset_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "compare_datasets",
                    "description": "Compare two datasets",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "dataset1": {
                                "type": "string",
                                "description": "First dataset name"
                            },
                            "dataset2": {
                                "type": "string",
                                "description": "Second dataset name"
                            }
                        },
                        "required": ["dataset1", "dataset2"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_outliers",
                    "description": "Find outliers in a dataset using IQR method",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "dataset_name": {
                                "type": "string",
                                "description": "Name of the dataset"
                            }
                        },
                        "required": ["dataset_name"]
                    }
                }
            }
        ]

    def create_dataset(self, name: str, data: List[float]) -> Dict[str, Any]:
        """Create a named dataset"""
        self.datasets[name] = data
        return {
            "name": name,
            "size": len(data),
            "success": True,
            "message": f"Dataset '{name}' created with {len(data)} values"
        }

    def calculate_statistics(self, dataset_name: str) -> Dict[str, Any]:
        """Calculate comprehensive statistics for a dataset"""
        if dataset_name not in self.datasets:
            return {"error": f"Dataset '{dataset_name}' not found", "success": False}

        data = self.datasets[dataset_name]

        try:
            stats = {
                "dataset_name": dataset_name,
                "count": len(data),
                "mean": statistics.mean(data),
                "median": statistics.median(data),
                "mode": statistics.mode(data) if len(data) > 1 else data[0],
                "stdev": statistics.stdev(data) if len(data) > 1 else 0,
                "variance": statistics.variance(data) if len(data) > 1 else 0,
                "min": min(data),
                "max": max(data),
                "range": max(data) - min(data),
                "sum": sum(data),
                "success": True
            }

            # Calculate quartiles
            sorted_data = sorted(data)
            n = len(sorted_data)
            stats["q1"] = sorted_data[n // 4]
            stats["q2"] = statistics.median(sorted_data)
            stats["q3"] = sorted_data[3 * n // 4]
            stats["iqr"] = stats["q3"] - stats["q1"]

            return stats
        except Exception as e:
            return {"error": str(e), "success": False}

    def compare_datasets(self, dataset1: str, dataset2: str) -> Dict[str, Any]:
        """Compare two datasets"""
        if dataset1 not in self.datasets:
            return {"error": f"Dataset '{dataset1}' not found", "success": False}
        if dataset2 not in self.datasets:
            return {"error": f"Dataset '{dataset2}' not found", "success": False}

        stats1 = self.calculate_statistics(dataset1)
        stats2 = self.calculate_statistics(dataset2)

        if not stats1["success"] or not stats2["success"]:
            return {"error": "Failed to calculate statistics", "success": False}

        comparison = {
            "dataset1": dataset1,
            "dataset2": dataset2,
            "mean_difference": stats2["mean"] - stats1["mean"],
            "median_difference": stats2["median"] - stats1["median"],
            "stdev_difference": stats2["stdev"] - stats1["stdev"],
            "larger_mean": dataset1 if stats1["mean"] > stats2["mean"] else dataset2,
            "larger_variance": dataset1 if stats1["variance"] > stats2["variance"] else dataset2,
            "stats1": stats1,
            "stats2": stats2,
            "success": True
        }

        return comparison

    def find_outliers(self, dataset_name: str) -> Dict[str, Any]:
        """Find outliers using IQR method"""
        if dataset_name not in self.datasets:
            return {"error": f"Dataset '{dataset_name}' not found", "success": False}

        data = self.datasets[dataset_name]
        stats = self.calculate_statistics(dataset_name)

        if not stats["success"]:
            return stats

        q1 = stats["q1"]
        q3 = stats["q3"]
        iqr = stats["iqr"]

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = [x for x in data if x < lower_bound or x > upper_bound]

        return {
            "dataset_name": dataset_name,
            "outliers": outliers,
            "count": len(outliers),
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "success": True
        }

    def execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool"""
        if function_name == "create_dataset":
            return self.create_dataset(**arguments)
        elif function_name == "calculate_statistics":
            return self.calculate_statistics(**arguments)
        elif function_name == "compare_datasets":
            return self.compare_datasets(**arguments)
        elif function_name == "find_outliers":
            return self.find_outliers(**arguments)
        else:
            return {"error": f"Unknown function: {function_name}", "success": False}

    def analyze(self, user_message: str) -> str:
        """
        Process data analysis request

        Args:
            user_message: User's analysis query

        Returns:
            Analysis result
        """
        messages = [
            {
                "role": "system",
                "content": "You are a data analysis assistant. Help users analyze datasets by creating datasets, calculating statistics, comparing data, and finding outliers."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        # Allow multiple rounds of tool calls
        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if not message.tool_calls:
                # No more tool calls, return response
                return message.content

            # Add assistant message with tool calls
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            # Execute tool calls
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                tool_result = self.execute_tool(function_name, function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })

            iteration += 1

        return "Analysis completed (max iterations reached)"


def main():
    """Example usage"""
    agent = DataAnalysisAgent()

    print("Data Analysis Agent")
    print("=" * 50)

    # Example analysis
    query = """
    I have two datasets:
    - Sales Q1: [120, 135, 142, 138, 145, 150, 148, 152, 155, 160]
    - Sales Q2: [155, 160, 165, 170, 162, 158, 175, 180, 178, 185]

    Please create these datasets, calculate statistics for each,
    and compare them to tell me which quarter performed better.
    """

    print(f"User: {query}\n")
    response = agent.analyze(query)
    print(f"Agent: {response}")


if __name__ == "__main__":
    main()
```

### 5.5 Task Management Agent

```python
"""
Task Management Agent
=====================
Agent for managing tasks and to-do lists.
"""

from openai import OpenAI
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import os
import json

@dataclass
class Task:
    """Task data structure"""
    id: str
    title: str
    description: str
    priority: str  # "low", "medium", "high"
    status: str  # "todo", "in_progress", "completed"
    due_date: Optional[str] = None
    created_at: str = None
    completed_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

class TaskManagementAgent:
    """
    Agent for managing tasks and to-do lists
    """

    def __init__(self, api_key: str = None):
        """Initialize task management agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
        self.tasks: Dict[str, Task] = {}
        self.task_counter = 0

        # Define task management tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "create_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Task title"
                            },
                            "description": {
                                "type": "string",
                                "description": "Task description"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Task priority"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "Due date in YYYY-MM-DD format"
                            }
                        },
                        "required": ["title", "description"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks with optional filters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["todo", "in_progress", "completed", "all"],
                                "description": "Filter by status"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "all"],
                                "description": "Filter by priority"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "Task ID"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["todo", "in_progress", "completed"],
                                "description": "New status"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "New priority"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "Task ID to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_task_summary",
                    "description": "Get a summary of all tasks",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]

    def create_task(
        self,
        title: str,
        description: str,
        priority: str = "medium",
        due_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new task"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"

        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            status="todo",
            due_date=due_date
        )

        self.tasks[task_id] = task

        return {
            "success": True,
            "task_id": task_id,
            "task": asdict(task),
            "message": f"Task '{title}' created successfully"
        }

    def list_tasks(
        self,
        status: str = "all",
        priority: str = "all"
    ) -> Dict[str, Any]:
        """List tasks with optional filters"""
        filtered_tasks = []

        for task in self.tasks.values():
            if status != "all" and task.status != status:
                continue
            if priority != "all" and task.priority != priority:
                continue
            filtered_tasks.append(asdict(task))

        return {
            "success": True,
            "count": len(filtered_tasks),
            "tasks": filtered_tasks
        }

    def update_task(
        self,
        task_id: str,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update a task"""
        if task_id not in self.tasks:
            return {
                "success": False,
                "error": f"Task '{task_id}' not found"
            }

        task = self.tasks[task_id]

        if status:
            task.status = status
            if status == "completed" and task.completed_at is None:
                task.completed_at = datetime.now().isoformat()

        if priority:
            task.priority = priority

        return {
            "success": True,
            "task_id": task_id,
            "task": asdict(task),
            "message": f"Task '{task.title}' updated successfully"
        }

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete a task"""
        if task_id not in self.tasks:
            return {
                "success": False,
                "error": f"Task '{task_id}' not found"
            }

        task = self.tasks.pop(task_id)

        return {
            "success": True,
            "message": f"Task '{task.title}' deleted successfully"
        }

    def get_task_summary(self) -> Dict[str, Any]:
        """Get summary of all tasks"""
        total = len(self.tasks)
        todo = sum(1 for t in self.tasks.values() if t.status == "todo")
        in_progress = sum(1 for t in self.tasks.values() if t.status == "in_progress")
        completed = sum(1 for t in self.tasks.values() if t.status == "completed")

        high_priority = sum(1 for t in self.tasks.values() if t.priority == "high")

        # Find overdue tasks
        today = datetime.now().date()
        overdue = []
        for task in self.tasks.values():
            if task.due_date and task.status != "completed":
                due = datetime.fromisoformat(task.due_date).date()
                if due < today:
                    overdue.append(asdict(task))

        return {
            "success": True,
            "total_tasks": total,
            "by_status": {
                "todo": todo,
                "in_progress": in_progress,
                "completed": completed
            },
            "high_priority_count": high_priority,
            "overdue_count": len(overdue),
            "overdue_tasks": overdue
        }

    def execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool"""
        if function_name == "create_task":
            return self.create_task(**arguments)
        elif function_name == "list_tasks":
            return self.list_tasks(**arguments)
        elif function_name == "update_task":
            return self.update_task(**arguments)
        elif function_name == "delete_task":
            return self.delete_task(**arguments)
        elif function_name == "get_task_summary":
            return self.get_task_summary()
        else:
            return {"error": f"Unknown function: {function_name}", "success": False}

    def process(self, user_message: str) -> str:
        """
        Process task management request

        Args:
            user_message: User's request

        Returns:
            Response
        """
        messages = [
            {
                "role": "system",
                "content": "You are a helpful task management assistant. Help users create, update, list, and manage their tasks effectively."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        # Allow multiple rounds of tool calls
        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return message.content

            # Add assistant message
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            # Execute tools
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                tool_result = self.execute_tool(function_name, function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })

            iteration += 1

        return "Request completed (max iterations reached)"


def main():
    """Example usage"""
    agent = TaskManagementAgent()

    print("Task Management Agent")
    print("=" * 50)

    # Example requests
    requests = [
        "Create a high-priority task to finish the project report by 2026-01-25",
        "Create a task to review code with medium priority",
        "Show me all my tasks",
        "Mark task_1 as in progress",
        "Give me a summary of all tasks"
    ]

    for request in requests:
        print(f"\nUser: {request}")
        response = agent.process(request)
        print(f"Agent: {response}")


if __name__ == "__main__":
    main()
```

---

## 6. Complex Agent Examples

### 6.1 Customer Support Agent with Context

```python
"""
Customer Support Agent with Context
====================================
Advanced customer support agent with customer database and ticket management.
"""

from openai import OpenAI
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import os
import json

@dataclass
class Customer:
    """Customer information"""
    customer_id: str
    name: str
    email: str
    phone: str
    subscription_tier: str  # "free", "basic", "premium"
    account_status: str  # "active", "suspended", "cancelled"
    join_date: str
    lifetime_value: float

@dataclass
class Ticket:
    """Support ticket"""
    ticket_id: str
    customer_id: str
    subject: str
    description: str
    category: str  # "technical", "billing", "general"
    priority: str  # "low", "medium", "high", "urgent"
    status: str  # "open", "in_progress", "resolved", "closed"
    created_at: str
    updated_at: str
    resolution: Optional[str] = None

class CustomerSupportAgent:
    """
    Advanced customer support agent with full context awareness
    """

    def __init__(self, api_key: str = None):
        """Initialize customer support agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"

        # Simulated databases
        self.customers: Dict[str, Customer] = self._init_customers()
        self.tickets: Dict[str, Ticket] = {}
        self.ticket_counter = 0

        # Define support tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "lookup_customer",
                    "description": "Look up customer information by email or customer ID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "identifier": {
                                "type": "string",
                                "description": "Customer email or ID"
                            }
                        },
                        "required": ["identifier"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_ticket",
                    "description": "Create a support ticket for a customer",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_id": {"type": "string"},
                            "subject": {"type": "string"},
                            "description": {"type": "string"},
                            "category": {
                                "type": "string",
                                "enum": ["technical", "billing", "general"]
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "urgent"]
                            }
                        },
                        "required": ["customer_id", "subject", "description", "category"]
                    }
                }
            }
        ]

    def _init_customers(self) -> Dict[str, Customer]:
        """Initialize sample customer database"""
        customers = [
            Customer(
                customer_id="C001",
                name="John Doe",
                email="john@example.com",
                phone="+1-555-0100",
                subscription_tier="premium",
                account_status="active",
                join_date="2024-01-15",
                lifetime_value=1200.00
            ),
            Customer(
                customer_id="C002",
                name="Jane Smith",
                email="jane@example.com",
                phone="+1-555-0101",
                subscription_tier="basic",
                account_status="active",
                join_date="2024-06-20",
                lifetime_value=240.00
            )
        ]
        return {c.customer_id: c for c in customers}

    def lookup_customer(self, identifier: str) -> Dict[str, Any]:
        """Look up customer by email or ID"""
        for customer in self.customers.values():
            if customer.email.lower() == identifier.lower() or customer.customer_id == identifier:
                return {"success": True, "customer": asdict(customer)}
        return {"success": False, "error": f"Customer not found: {identifier}"}

    def create_ticket(
        self,
        customer_id: str,
        subject: str,
        description: str,
        category: str,
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """Create a support ticket"""
        if customer_id not in self.customers:
            return {"success": False, "error": f"Customer not found: {customer_id}"}

        self.ticket_counter += 1
        ticket_id = f"T{self.ticket_counter:05d}"

        now = datetime.now().isoformat()
        ticket = Ticket(
            ticket_id=ticket_id,
            customer_id=customer_id,
            subject=subject,
            description=description,
            category=category,
            priority=priority,
            status="open",
            created_at=now,
            updated_at=now
        )

        self.tickets[ticket_id] = ticket

        return {
            "success": True,
            "ticket": asdict(ticket),
            "message": f"Ticket {ticket_id} created successfully"
        }

    def execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool"""
        if function_name == "lookup_customer":
            return self.lookup_customer(**arguments)
        elif function_name == "create_ticket":
            return self.create_ticket(**arguments)
        else:
            return {"error": f"Unknown function: {function_name}", "success": False}

    def handle_request(self, user_message: str) -> str:
        """Handle customer support request"""
        messages = [
            {
                "role": "system",
                "content": "You are a helpful customer support agent. Look up customers and create tickets as needed."
            },
            {"role": "user", "content": user_message}
        ]

        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return message.content

            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                tool_result = self.execute_tool(function_name, function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })

            iteration += 1

        return "Support request completed"
```

### 6.2 Research Assistant with Web Search

```python
"""
Research Assistant with Web Search
===================================
Agent that performs web research and synthesizes findings.
"""

from openai import OpenAI
from typing import Dict, Any, List
import os
import json

class ResearchAssistant:
    """
    Research assistant with web search capabilities
    """

    def __init__(self, api_key: str = None):
        """Initialize research assistant"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
        self.research_history: List[Dict[str, Any]] = []

        # Define research tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the web for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "num_results": {
                                "type": "integer",
                                "description": "Number of results to return (1-10)"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "save_research_finding",
                    "description": "Save an important research finding",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "content": {"type": "string"},
                            "source": {"type": "string"}
                        },
                        "required": ["title", "content"]
                    }
                }
            }
        ]

    def web_search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Simulated web search
        (In production, integrate with real search API)
        """
        # Simulated search results
        results = [
            {
                "title": f"Result {i+1} for: {query}",
                "snippet": f"This is a summary of search result {i+1} about {query}",
                "url": f"https://example.com/result{i+1}"
            }
            for i in range(min(num_results, 5))
        ]

        return {
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        }

    def save_research_finding(
        self,
        title: str,
        content: str,
        source: str = ""
    ) -> Dict[str, Any]:
        """Save a research finding"""
        finding = {
            "title": title,
            "content": content,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }

        self.research_history.append(finding)

        return {
            "success": True,
            "message": f"Finding '{title}' saved",
            "finding_id": len(self.research_history) - 1
        }

    def execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a research tool"""
        if function_name == "web_search":
            return self.web_search(**arguments)
        elif function_name == "save_research_finding":
            return self.save_research_finding(**arguments)
        else:
            return {"error": f"Unknown function: {function_name}", "success": False}

    def research(self, topic: str) -> str:
        """
        Conduct research on a topic

        Args:
            topic: Research topic

        Returns:
            Research summary
        """
        messages = [
            {
                "role": "system",
                "content": "You are a research assistant. Search for information, analyze it, and save important findings."
            },
            {
                "role": "user",
                "content": f"Research this topic and provide a comprehensive summary: {topic}"
            }
        ]

        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return message.content

            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                tool_result = self.execute_tool(function_name, function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })

            iteration += 1

        return "Research completed"
```

### 6.3 Code Review Agent

```python
"""
Code Review Agent
=================
Agent that reviews code and provides feedback.
"""

from openai import OpenAI
from typing import Dict, Any, List
import os
import json

class CodeReviewAgent:
    """
    Agent for reviewing code and providing suggestions
    """

    def __init__(self, api_key: str = None):
        """Initialize code review agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "analyze_code_complexity",
                    "description": "Analyze code complexity metrics",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string"}
                        },
                        "required": ["code"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_security_issues",
                    "description": "Check for common security vulnerabilities",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string"}
                        },
                        "required": ["code"]
                    }
                }
            }
        ]

    def analyze_code_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity (simplified)"""
        lines = code.split('\n')
        functions = code.count('def ')
        classes = code.count('class ')

        return {
            "success": True,
            "metrics": {
                "lines_of_code": len(lines),
                "functions": functions,
                "classes": classes,
                "complexity_score": len(lines) + functions * 5
            }
        }

    def check_security_issues(self, code: str) -> Dict[str, Any]:
        """Check for security issues (simplified)"""
        issues = []

        if 'eval(' in code:
            issues.append("Use of eval() detected - security risk")
        if 'exec(' in code:
            issues.append("Use of exec() detected - security risk")
        if 'os.system(' in code:
            issues.append("Direct os.system() call - consider using subprocess")

        return {
            "success": True,
            "issues": issues,
            "severity": "high" if len(issues) > 0 else "low"
        }

    def execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool"""
        if function_name == "analyze_code_complexity":
            return self.analyze_code_complexity(**arguments)
        elif function_name == "check_security_issues":
            return self.check_security_issues(**arguments)
        else:
            return {"error": f"Unknown function: {function_name}", "success": False}

    def review(self, code: str) -> str:
        """Review code and provide feedback"""
        messages = [
            {
                "role": "system",
                "content": "You are a code review assistant. Analyze code for quality, security, and best practices."
            },
            {
                "role": "user",
                "content": f"Please review this code:\n\n```python\n{code}\n```"
            }
        ]

        max_iterations = 3
        iteration = 0

        while iteration < max_iterations:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return message.content

            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                tool_result = self.execute_tool(function_name, function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })

            iteration += 1

        return "Review completed"
```

### 6.4 Financial Analysis Agent

```python
"""
Financial Analysis Agent
========================
Agent for analyzing financial data and generating reports.
"""

from openai import OpenAI
from typing import Dict, Any, List
import os
import json

class FinancialAnalysisAgent:
    """
    Agent for financial analysis and reporting
    """

    def __init__(self, api_key: str = None):
        """Initialize financial analysis agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "calculate_financial_ratios",
                    "description": "Calculate key financial ratios",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "revenue": {"type": "number"},
                            "expenses": {"type": "number"},
                            "assets": {"type": "number"},
                            "liabilities": {"type": "number"}
                        },
                        "required": ["revenue", "expenses", "assets", "liabilities"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "forecast_revenue",
                    "description": "Forecast future revenue based on historical data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "historical_data": {
                                "type": "array",
                                "items": {"type": "number"}
                            },
                            "periods": {"type": "integer"}
                        },
                        "required": ["historical_data", "periods"]
                    }
                }
            }
        ]

    def calculate_financial_ratios(
        self,
        revenue: float,
        expenses: float,
        assets: float,
        liabilities: float
    ) -> Dict[str, Any]:
        """Calculate financial ratios"""
        profit = revenue - expenses
        equity = assets - liabilities

        ratios = {
            "profit_margin": (profit / revenue * 100) if revenue > 0 else 0,
            "return_on_assets": (profit / assets * 100) if assets > 0 else 0,
            "debt_to_equity": (liabilities / equity) if equity > 0 else 0,
            "current_ratio": (assets / liabilities) if liabilities > 0 else 0
        }

        return {
            "success": True,
            "ratios": ratios,
            "profit": profit,
            "equity": equity
        }

    def forecast_revenue(
        self,
        historical_data: List[float],
        periods: int
    ) -> Dict[str, Any]:
        """Simple linear forecast"""
        if len(historical_data) < 2:
            return {"error": "Need at least 2 data points", "success": False}

        # Simple linear trend
        avg_growth = sum(
            historical_data[i] - historical_data[i-1]
            for i in range(1, len(historical_data))
        ) / (len(historical_data) - 1)

        forecast = []
        last_value = historical_data[-1]
        for i in range(periods):
            last_value += avg_growth
            forecast.append(round(last_value, 2))

        return {
            "success": True,
            "forecast": forecast,
            "avg_growth": round(avg_growth, 2)
        }

    def execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool"""
        if function_name == "calculate_financial_ratios":
            return self.calculate_financial_ratios(**arguments)
        elif function_name == "forecast_revenue":
            return self.forecast_revenue(**arguments)
        else:
            return {"error": f"Unknown function: {function_name}", "success": False}

    def analyze(self, query: str) -> str:
        """Analyze financial data"""
        messages = [
            {
                "role": "system",
                "content": "You are a financial analysis assistant. Calculate ratios, forecast revenue, and provide insights."
            },
            {"role": "user", "content": query}
        ]

        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return message.content

            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                tool_result = self.execute_tool(function_name, function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })

            iteration += 1

        return "Analysis completed"
```

---

## 7. Multi-Agent Systems

### 7.1 Triage and Routing System

```python
"""
Triage and Routing System
==========================
Multi-agent system that routes requests to specialized agents.
"""

from openai import OpenAI
from typing import Dict, Any, List
import os
import json

class TriageAgent:
    """Main triage agent that routes to specialists"""

    def __init__(self, api_key: str = None):
        """Initialize triage agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"

        # Initialize specialist agents
        self.specialists = {
            "technical": TechnicalSupportAgent(api_key),
            "billing": BillingAgent(api_key),
            "general": GeneralInquiryAgent(api_key)
        }

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "route_to_specialist",
                    "description": "Route request to appropriate specialist",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "specialist": {
                                "type": "string",
                                "enum": ["technical", "billing", "general"]
                            },
                            "request": {"type": "string"}
                        },
                        "required": ["specialist", "request"]
                    }
                }
            }
        ]

    def route_to_specialist(self, specialist: str, request: str) -> Dict[str, Any]:
        """Route to specialist agent"""
        if specialist not in self.specialists:
            return {"error": f"Unknown specialist: {specialist}", "success": False}

        result = self.specialists[specialist].handle(request)
        return {
            "success": True,
            "specialist": specialist,
            "response": result
        }

    def execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute routing tool"""
        if function_name == "route_to_specialist":
            return self.route_to_specialist(**arguments)
        return {"error": "Unknown function", "success": False}

    def handle(self, request: str) -> str:
        """Handle incoming request"""
        messages = [
            {
                "role": "system",
                "content": "You are a triage agent. Analyze requests and route to the appropriate specialist: technical, billing, or general."
            },
            {"role": "user", "content": request}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments)
                result = self.execute_tool(tool_call.function.name, function_args)

                messages.append({
                    "role": "assistant",
                    "tool_calls": [{
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }]
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": json.dumps(result)
                })

                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )

                return final_response.choices[0].message.content

        return message.content


class TechnicalSupportAgent:
    """Specialist for technical issues"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def handle(self, request: str) -> str:
        """Handle technical request"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical support specialist. Help with technical issues."
                },
                {"role": "user", "content": request}
            ]
        )
        return response.choices[0].message.content


class BillingAgent:
    """Specialist for billing inquiries"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def handle(self, request: str) -> str:
        """Handle billing request"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a billing specialist. Help with billing and payment issues."
                },
                {"role": "user", "content": request}
            ]
        )
        return response.choices[0].message.content


class GeneralInquiryAgent:
    """Specialist for general inquiries"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def handle(self, request: str) -> str:
        """Handle general request"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a general inquiry specialist. Help with general questions."
                },
                {"role": "user", "content": request}
            ]
        )
        return response.choices[0].message.content
```

### 7.2 Software Development Team

```python
"""
Software Development Team
=========================
Multi-agent system simulating a software development team.
"""

from openai import OpenAI
from typing import Dict, Any
import os

class SoftwareDevTeam:
    """
    Simulates a software development team with multiple specialized agents
    """

    def __init__(self, api_key: str = None):
        """Initialize the dev team"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

        # Initialize team members
        self.product_manager = ProductManagerAgent(self.api_key)
        self.developer = DeveloperAgent(self.api_key)
        self.qa_engineer = QAEngineerAgent(self.api_key)
        self.tech_writer = TechWriterAgent(self.api_key)

    def develop_feature(self, feature_request: str) -> Dict[str, str]:
        """
        Complete feature development workflow

        Args:
            feature_request: Description of the feature to build

        Returns:
            Dictionary with outputs from each team member
        """
        print(f"New Feature Request: {feature_request}\n")

        # Step 1: Product Manager creates requirements
        print("Step 1: Product Manager defining requirements...")
        requirements = self.product_manager.create_requirements(feature_request)
        print(f"Requirements: {requirements}\n")

        # Step 2: Developer implements
        print("Step 2: Developer implementing...")
        code = self.developer.implement(requirements)
        print(f"Code: {code}\n")

        # Step 3: QA tests
        print("Step 3: QA testing...")
        test_results = self.qa_engineer.test(code)
        print(f"Test Results: {test_results}\n")

        # Step 4: Tech Writer documents
        print("Step 4: Tech Writer documenting...")
        documentation = self.tech_writer.document(code, requirements)
        print(f"Documentation: {documentation}\n")

        return {
            "requirements": requirements,
            "code": code,
            "test_results": test_results,
            "documentation": documentation
        }


class ProductManagerAgent:
    """Product Manager agent"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def create_requirements(self, feature_request: str) -> str:
        """Create detailed requirements"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a product manager. Create detailed technical requirements."
                },
                {"role": "user", "content": f"Create requirements for: {feature_request}"}
            ]
        )
        return response.choices[0].message.content


class DeveloperAgent:
    """Developer agent"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def implement(self, requirements: str) -> str:
        """Implement code based on requirements"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a software developer. Write clean, efficient code."
                },
                {"role": "user", "content": f"Implement these requirements:\n{requirements}"}
            ]
        )
        return response.choices[0].message.content


class QAEngineerAgent:
    """QA Engineer agent"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def test(self, code: str) -> str:
        """Test the code"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a QA engineer. Create test cases and identify issues."
                },
                {"role": "user", "content": f"Test this code:\n{code}"}
            ]
        )
        return response.choices[0].message.content


class TechWriterAgent:
    """Technical Writer agent"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def document(self, code: str, requirements: str) -> str:
        """Create documentation"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical writer. Create clear documentation."
                },
                {
                    "role": "user",
                    "content": f"Document this code:\n{code}\n\nRequirements:\n{requirements}"
                }
            ]
        )
        return response.choices[0].message.content
```

### 7.3 Customer Service Hierarchy

```python
"""
Customer Service Hierarchy
===========================
Hierarchical multi-agent system for customer service with escalation.
"""

from openai import OpenAI
from typing import Dict, Any
import os
import json

class CustomerServiceHierarchy:
    """
    Hierarchical customer service system
    """

    def __init__(self, api_key: str = None):
        """Initialize the hierarchy"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

        # Initialize agents at different levels
        self.tier1_agent = Tier1SupportAgent(self.api_key)
        self.tier2_agent = Tier2SupportAgent(self.api_key)
        self.manager_agent = ManagerAgent(self.api_key)

    def handle_request(self, request: str) -> Dict[str, Any]:
        """
        Handle customer request with potential escalation

        Args:
            request: Customer request

        Returns:
            Response with resolution path
        """
        resolution_path = []

        # Start with Tier 1
        print("Tier 1 Support handling request...")
        tier1_response = self.tier1_agent.handle(request)
        resolution_path.append({"level": "Tier 1", "response": tier1_response})

        # Check if escalation needed
        if "escalate" in tier1_response.lower():
            print("Escalating to Tier 2...")
            tier2_response = self.tier2_agent.handle(request)
            resolution_path.append({"level": "Tier 2", "response": tier2_response})

            # Check if further escalation needed
            if "escalate" in tier2_response.lower():
                print("Escalating to Manager...")
                manager_response = self.manager_agent.handle(request)
                resolution_path.append({"level": "Manager", "response": manager_response})

                return {
                    "resolution_level": "Manager",
                    "final_response": manager_response,
                    "path": resolution_path
                }

            return {
                "resolution_level": "Tier 2",
                "final_response": tier2_response,
                "path": resolution_path
            }

        return {
            "resolution_level": "Tier 1",
            "final_response": tier1_response,
            "path": resolution_path
        }


class Tier1SupportAgent:
    """First-line support agent"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def handle(self, request: str) -> str:
        """Handle tier 1 request"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a Tier 1 support agent. Handle basic requests.
                    If the request is complex or requires escalation, include 'ESCALATE' in your response."""
                },
                {"role": "user", "content": request}
            ]
        )
        return response.choices[0].message.content


class Tier2SupportAgent:
    """Second-line support agent"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def handle(self, request: str) -> str:
        """Handle tier 2 request"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a Tier 2 support agent. Handle complex technical issues.
                    If the issue requires manager approval or is a critical issue, include 'ESCALATE' in your response."""
                },
                {"role": "user", "content": request}
            ]
        )
        return response.choices[0].message.content


class ManagerAgent:
    """Manager-level agent"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def handle(self, request: str) -> str:
        """Handle manager-level request"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a customer service manager. Make final decisions on complex issues,
                    authorize special requests, and ensure customer satisfaction."""
                },
                {"role": "user", "content": request}
            ]
        )
        return response.choices[0].message.content
```

### 7.4 Research and Analysis Pipeline

```python
"""
Research and Analysis Pipeline
===============================
Sequential multi-agent pipeline for research and analysis.
"""

from openai import OpenAI
from typing import Dict, Any, List
import os

class ResearchAnalysisPipeline:
    """
    Sequential pipeline: Research → Analysis → Synthesis → Report
    """

    def __init__(self, api_key: str = None):
        """Initialize the pipeline"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        # Initialize pipeline agents
        self.researcher = ResearcherAgent(self.api_key)
        self.analyst = AnalystAgent(self.api_key)
        self.synthesizer = SynthesizerAgent(self.api_key)
        self.reporter = ReporterAgent(self.api_key)

    def process(self, topic: str) -> Dict[str, str]:
        """
        Process topic through the pipeline

        Args:
            topic: Research topic

        Returns:
            Dictionary with outputs from each stage
        """
        print(f"Processing topic: {topic}\n")

        # Stage 1: Research
        print("Stage 1: Research...")
        research_findings = self.researcher.research(topic)
        print(f"Research completed.\n")

        # Stage 2: Analysis
        print("Stage 2: Analysis...")
        analysis = self.analyst.analyze(research_findings)
        print(f"Analysis completed.\n")

        # Stage 3: Synthesis
        print("Stage 3: Synthesis...")
        synthesis = self.synthesizer.synthesize(research_findings, analysis)
        print(f"Synthesis completed.\n")

        # Stage 4: Report
        print("Stage 4: Report generation...")
        report = self.reporter.generate_report(research_findings, analysis, synthesis)
        print(f"Report generated.\n")

        return {
            "research_findings": research_findings,
            "analysis": analysis,
            "synthesis": synthesis,
            "final_report": report
        }


class ResearcherAgent:
    """Agent that conducts research"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def research(self, topic: str) -> str:
        """Conduct research on topic"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a researcher. Gather comprehensive information on topics."
                },
                {"role": "user", "content": f"Research this topic: {topic}"}
            ]
        )
        return response.choices[0].message.content


class AnalystAgent:
    """Agent that analyzes research"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def analyze(self, research_findings: str) -> str:
        """Analyze research findings"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an analyst. Analyze data and identify patterns, insights, and implications."
                },
                {"role": "user", "content": f"Analyze these findings:\n{research_findings}"}
            ]
        )
        return response.choices[0].message.content


class SynthesizerAgent:
    """Agent that synthesizes information"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def synthesize(self, research: str, analysis: str) -> str:
        """Synthesize research and analysis"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a synthesizer. Combine research and analysis into cohesive insights."
                },
                {
                    "role": "user",
                    "content": f"Synthesize:\n\nResearch:\n{research}\n\nAnalysis:\n{analysis}"
                }
            ]
        )
        return response.choices[0].message.content


class ReporterAgent:
    """Agent that generates reports"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def generate_report(self, research: str, analysis: str, synthesis: str) -> str:
        """Generate final report"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a report writer. Create comprehensive, well-structured reports."
                },
                {
                    "role": "user",
                    "content": f"Generate a report from:\n\nResearch:\n{research}\n\nAnalysis:\n{analysis}\n\nSynthesis:\n{synthesis}"
                }
            ]
        )
        return response.choices[0].message.content
```

---

## 8. RAG with Agents / Agentic RAG

### 8.1 File Search Basics

```python
"""
File Search Basics with OpenAI Agents
======================================
Basic RAG implementation using OpenAI's file search capabilities.
"""

from openai import OpenAI
from typing import Dict, Any, List
import os

class BasicFileSearchAgent:
    """
    Basic agent with file search for RAG
    """

    def __init__(self, api_key: str = None):
        """Initialize file search agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
        self.vector_store_id = None

    def create_vector_store(self, name: str, file_paths: List[str]) -> str:
        """
        Create a vector store and upload files

        Args:
            name: Name for the vector store
            file_paths: List of file paths to upload

        Returns:
            Vector store ID
        """
        # Note: This is a simplified version
        # In production, use the actual Responses API with file_search tool

        print(f"Creating vector store '{name}'...")
        print(f"Uploading {len(file_paths)} files...")

        # Simulated vector store creation
        # In actual implementation, use:
        # vector_store = client.beta.vector_stores.create(name=name)
        # for file_path in file_paths:
        #     file = client.files.create(file=open(file_path, "rb"), purpose="assistants")
        #     client.beta.vector_stores.files.create(vector_store_id=vector_store.id, file_id=file.id)

        self.vector_store_id = "vs_simulated_123"
        return self.vector_store_id

    def query(self, question: str) -> str:
        """
        Query the vector store

        Args:
            question: User's question

        Returns:
            Answer based on retrieved documents
        """
        if not self.vector_store_id:
            return "No vector store configured. Please create one first."

        # In production, this would use the file_search tool
        # with the Responses API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant with access to a knowledge base. Answer questions based on the provided context."
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nNote: In production, this would search the vector store."
                }
            ]
        )

        return response.choices[0].message.content
```

### 8.2 Vector Store RAG Agent

```python
"""
Vector Store RAG Agent
======================
Advanced RAG agent with vector store management.
"""

from openai import OpenAI
from typing import Dict, Any, List, Optional
import os
import json

class VectorStoreRAGAgent:
    """
    Advanced RAG agent with vector store capabilities
    """

    def __init__(self, api_key: str = None):
        """Initialize vector store RAG agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
        self.vector_stores: Dict[str, str] = {}  # name -> ID mapping

    def create_knowledge_base(
        self,
        name: str,
        documents: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Create a knowledge base from documents

        Args:
            name: Knowledge base name
            documents: List of documents with 'title' and 'content'

        Returns:
            Creation result
        """
        # In production implementation:
        # 1. Create vector store
        # 2. Upload documents as files
        # 3. Process and index

        print(f"Creating knowledge base: {name}")
        print(f"Processing {len(documents)} documents...")

        # Simulated processing
        vector_store_id = f"vs_{name}_{len(self.vector_stores)}"
        self.vector_stores[name] = vector_store_id

        return {
            "success": True,
            "knowledge_base": name,
            "vector_store_id": vector_store_id,
            "document_count": len(documents)
        }

    def query_knowledge_base(
        self,
        knowledge_base: str,
        query: str,
        num_results: int = 5
    ) -> Dict[str, Any]:
        """
        Query a knowledge base

        Args:
            knowledge_base: Knowledge base name
            query: Search query
            num_results: Number of results to retrieve

        Returns:
            Query results with retrieved documents
        """
        if knowledge_base not in self.vector_stores:
            return {
                "success": False,
                "error": f"Knowledge base '{knowledge_base}' not found"
            }

        print(f"Querying knowledge base: {knowledge_base}")
        print(f"Query: {query}")

        # Simulated semantic search
        # In production, this would use the file_search tool
        retrieved_docs = [
            {
                "title": f"Document {i+1}",
                "content": f"Relevant content for query: {query}",
                "score": 0.95 - (i * 0.1)
            }
            for i in range(min(num_results, 3))
        ]

        return {
            "success": True,
            "query": query,
            "knowledge_base": knowledge_base,
            "results": retrieved_docs,
            "count": len(retrieved_docs)
        }

    def answer_with_context(
        self,
        knowledge_base: str,
        question: str
    ) -> str:
        """
        Answer question using knowledge base context

        Args:
            knowledge_base: Knowledge base to query
            question: User's question

        Returns:
            Answer with citations
        """
        # Retrieve relevant documents
        search_results = self.query_knowledge_base(knowledge_base, question)

        if not search_results["success"]:
            return f"Error: {search_results['error']}"

        # Build context from retrieved documents
        context = "\n\n".join([
            f"Document: {doc['title']}\n{doc['content']}"
            for doc in search_results["results"]
        ])

        # Generate answer with context
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful assistant. Answer questions based on the provided context.
                    If the context doesn't contain relevant information, say so.
                    Always cite which documents you used."""
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}"
                }
            ]
        )

        return response.choices[0].message.content


# Example usage
def main():
    """Example usage of Vector Store RAG Agent"""
    agent = VectorStoreRAGAgent()

    # Create a knowledge base
    documents = [
        {"title": "Python Basics", "content": "Python is a high-level programming language..."},
        {"title": "Data Structures", "content": "Lists, tuples, and dictionaries are core data structures..."},
        {"title": "Object-Oriented Programming", "content": "Classes and objects enable OOP in Python..."}
    ]

    result = agent.create_knowledge_base("python_docs", documents)
    print(f"Knowledge base created: {result}\n")

    # Query the knowledge base
    answer = agent.answer_with_context(
        "python_docs",
        "What are the core data structures in Python?"
    )
    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
```

### 8.3 Multi-Document RAG Agent

```python
"""
Multi-Document RAG Agent
=========================
RAG agent that handles multiple document collections.
"""

from openai import OpenAI
from typing import Dict, Any, List
import os

class MultiDocumentRAGAgent:
    """
    RAG agent supporting multiple document collections
    """

    def __init__(self, api_key: str = None):
        """Initialize multi-document RAG agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
        self.collections: Dict[str, List[Dict[str, str]]] = {}

    def add_collection(
        self,
        collection_name: str,
        documents: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Add a document collection

        Args:
            collection_name: Name of the collection
            documents: List of documents

        Returns:
            Status
        """
        self.collections[collection_name] = documents
        return {
            "success": True,
            "collection": collection_name,
            "document_count": len(documents)
        }

    def search_all_collections(
        self,
        query: str,
        collections: List[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search across multiple collections

        Args:
            query: Search query
            collections: List of collections to search (None = all)

        Returns:
            Results grouped by collection
        """
        if collections is None:
            collections = list(self.collections.keys())

        results = {}

        for collection in collections:
            if collection in self.collections:
                # Simulate search in collection
                collection_results = [
                    {
                        "title": doc["title"],
                        "content": doc["content"][:200],
                        "score": 0.9
                    }
                    for doc in self.collections[collection][:2]
                ]
                results[collection] = collection_results

        return results

    def answer_with_multi_source(
        self,
        question: str,
        collections: List[str] = None
    ) -> str:
        """
        Answer question using multiple document collections

        Args:
            question: User's question
            collections: Collections to search

        Returns:
            Answer with multi-source citations
        """
        # Search across collections
        search_results = self.search_all_collections(question, collections)

        # Build context from all sources
        context_parts = []
        for collection, docs in search_results.items():
            context_parts.append(f"=== From {collection} ===")
            for doc in docs:
                context_parts.append(f"{doc['title']}: {doc['content']}")

        context = "\n\n".join(context_parts)

        # Generate answer
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a research assistant. Answer questions by synthesizing information
                    from multiple sources. Cite the specific sources you use."""
                },
                {
                    "role": "user",
                    "content": f"Sources:\n{context}\n\nQuestion: {question}"
                }
            ]
        )

        return response.choices[0].message.content
```

### 8.4 Hybrid Search Agent

```python
"""
Hybrid Search Agent
===================
RAG agent combining keyword and semantic search.
"""

from openai import OpenAI
from typing import Dict, Any, List
import os

class HybridSearchAgent:
    """
    Agent using both keyword and semantic search for RAG
    """

    def __init__(self, api_key: str = None):
        """Initialize hybrid search agent"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
        self.documents: List[Dict[str, str]] = []

    def index_documents(self, documents: List[Dict[str, str]]):
        """
        Index documents for both keyword and semantic search

        Args:
            documents: Documents to index
        """
        self.documents = documents
        print(f"Indexed {len(documents)} documents")

    def keyword_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform keyword-based search

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            Search results
        """
        # Simplified keyword matching
        query_terms = set(query.lower().split())
        results = []

        for doc in self.documents:
            content_lower = doc["content"].lower()
            matches = sum(1 for term in query_terms if term in content_lower)

            if matches > 0:
                results.append({
                    "document": doc,
                    "score": matches / len(query_terms),
                    "method": "keyword"
                })

        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic search

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            Search results
        """
        # In production, this would use embeddings
        # For now, simulate semantic search
        results = [
            {
                "document": doc,
                "score": 0.85,
                "method": "semantic"
            }
            for doc in self.documents[:top_k]
        ]

        return results

    def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
        keyword_weight: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining keyword and semantic

        Args:
            query: Search query
            top_k: Number of results
            keyword_weight: Weight for keyword search (0-1)

        Returns:
            Combined search results
        """
        # Get results from both methods
        keyword_results = self.keyword_search(query, top_k)
        semantic_results = self.semantic_search(query, top_k)

        # Combine and re-rank
        combined = {}

        for result in keyword_results:
            doc_id = result["document"]["title"]
            combined[doc_id] = {
                "document": result["document"],
                "score": result["score"] * keyword_weight,
                "methods": ["keyword"]
            }

        for result in semantic_results:
            doc_id = result["document"]["title"]
            if doc_id in combined:
                combined[doc_id]["score"] += result["score"] * (1 - keyword_weight)
                combined[doc_id]["methods"].append("semantic")
            else:
                combined[doc_id] = {
                    "document": result["document"],
                    "score": result["score"] * (1 - keyword_weight),
                    "methods": ["semantic"]
                }

        # Convert to list and sort
        results = list(combined.values())
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_k]

    def answer_with_hybrid_search(
        self,
        question: str,
        top_k: int = 5
    ) -> str:
        """
        Answer question using hybrid search

        Args:
            question: User's question
            top_k: Number of documents to retrieve

        Returns:
            Answer based on retrieved documents
        """
        # Perform hybrid search
        results = self.hybrid_search(question, top_k)

        # Build context
        context = "\n\n".join([
            f"Document: {r['document']['title']}\n{r['document']['content']}\n(Retrieved via: {', '.join(r['methods'])})"
            for r in results
        ])

        # Generate answer
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer based on the provided context."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}"
                }
            ]
        )

        return response.choices[0].message.content
```

---

## 9. FastMCP Servers with Agents

### 9.1 Building a FastMCP Server

```python
"""
Building a FastMCP Server
==========================
Create a Model Context Protocol server using FastMCP.
"""

from typing import Dict, Any, List
import json

# Note: This is a conceptual example
# In production, install fastmcp: pip install fastmcp

class FastMCPServer:
    """
    Example FastMCP server implementation
    """

    def __init__(self, name: str):
        """
        Initialize FastMCP server

        Args:
            name: Server name
        """
        self.name = name
        self.tools: Dict[str, callable] = {}

    def tool(self, description: str):
        """
        Decorator to register a tool

        Args:
            description: Tool description

        Returns:
            Decorator function
        """
        def decorator(func):
            self.tools[func.__name__] = {
                "function": func,
                "description": description
            }
            return func
        return decorator

    def get_tools_manifest(self) -> List[Dict[str, Any]]:
        """
        Get list of available tools

        Returns:
            Tool manifest
        """
        manifest = []
        for name, tool in self.tools.items():
            manifest.append({
                "name": name,
                "description": tool["description"],
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            })
        return manifest

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool

        Args:
            tool_name: Name of tool to execute
            arguments: Tool arguments

        Returns:
            Tool result
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")

        func = self.tools[tool_name]["function"]
        return func(**arguments)


# Example: Create a database MCP server
class DatabaseMCPServer(FastMCPServer):
    """
    MCP server for database operations
    """

    def __init__(self):
        super().__init__("database_server")
        self.db = {}  # Simulated database

        # Register tools
        @self.tool("Query database records")
        def query_records(table: str, filter: Dict[str, Any] = None):
            """Query records from a table"""
            if table not in self.db:
                return {"error": f"Table '{table}' not found", "records": []}

            records = self.db[table]

            if filter:
                # Simple filtering
                filtered = [r for r in records if all(r.get(k) == v for k, v in filter.items())]
                return {"records": filtered}

            return {"records": records}

        @self.tool("Insert database record")
        def insert_record(table: str, record: Dict[str, Any]):
            """Insert a record into a table"""
            if table not in self.db:
                self.db[table] = []

            self.db[table].append(record)
            return {"success": True, "record_id": len(self.db[table]) - 1}

        @self.tool("Update database record")
        def update_record(table: str, record_id: int, updates: Dict[str, Any]):
            """Update a record"""
            if table not in self.db or record_id >= len(self.db[table]):
                return {"success": False, "error": "Record not found"}

            self.db[table][record_id].update(updates)
            return {"success": True}


def main():
    """Example usage"""
    # Create server
    server = DatabaseMCPServer()

    # Insert some data
    server.execute_tool("insert_record", {
        "table": "users",
        "record": {"name": "Alice", "email": "alice@example.com"}
    })

    # Query data
    result = server.execute_tool("query_records", {
        "table": "users",
        "filter": {"name": "Alice"}
    })

    print(f"Query result: {result}")

    # Get tools manifest
    manifest = server.get_tools_manifest()
    print(f"\nAvailable tools:")
    for tool in manifest:
        print(f"- {tool['name']}: {tool['description']}")


if __name__ == "__main__":
    main()
```

### 9.2 Integrating FastMCP with OpenAI Agents

```python
"""
Integrating FastMCP with OpenAI Agents
=======================================
Connect FastMCP servers to OpenAI agents.
"""

from openai import OpenAI
from typing import Dict, Any, List
import os
import json

class MCPIntegratedAgent:
    """
    OpenAI agent integrated with FastMCP server
    """

    def __init__(self, api_key: str = None):
        """Initialize agent with MCP integration"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
        self.mcp_server = DatabaseMCPServer()  # From previous example

        # Convert MCP tools to OpenAI function format
        self.tools = self._convert_mcp_tools()

    def _convert_mcp_tools(self) -> List[Dict[str, Any]]:
        """
        Convert MCP tools to OpenAI function calling format

        Returns:
            OpenAI-compatible tool definitions
        """
        mcp_manifest = self.mcp_server.get_tools_manifest()
        openai_tools = []

        for mcp_tool in mcp_manifest:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": mcp_tool["name"],
                    "description": mcp_tool["description"],
                    "parameters": mcp_tool["input_schema"]
                }
            })

        return openai_tools

    def execute_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute MCP tool

        Args:
            tool_name: Tool name
            arguments: Tool arguments

        Returns:
            Tool result
        """
        return self.mcp_server.execute_tool(tool_name, arguments)

    def chat(self, user_message: str) -> str:
        """
        Chat with agent that can use MCP tools

        Args:
            user_message: User's message

        Returns:
            Agent's response
        """
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant with access to a database via MCP tools. Use the tools to answer questions."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return message.content

            # Add assistant message
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            # Execute tools
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Execute via MCP
                tool_result = self.execute_mcp_tool(function_name, function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })

            iteration += 1

        return "Request completed"


def main():
    """Example usage"""
    agent = MCPIntegratedAgent()

    # Add some data first
    agent.mcp_server.execute_tool("insert_record", {
        "table": "products",
        "record": {"name": "Laptop", "price": 999}
    })

    # Query via agent
    response = agent.chat("Show me all products in the database")
    print(f"Agent: {response}")


if __name__ == "__main__":
    main()
```

### 9.3 Custom Tools via MCP

```python
"""
Custom Tools via MCP
====================
Create custom business logic tools via MCP.
"""

from typing import Dict, Any, List
import datetime

class BusinessLogicMCPServer(FastMCPServer):
    """
    MCP server with custom business logic tools
    """

    def __init__(self):
        super().__init__("business_logic_server")

        @self.tool("Calculate order total with tax and discounts")
        def calculate_order_total(
            items: List[Dict[str, float]],
            tax_rate: float = 0.08,
            discount_code: str = None
        ) -> Dict[str, Any]:
            """Calculate order total"""
            subtotal = sum(item["price"] * item.get("quantity", 1) for item in items)

            # Apply discount
            discount = 0
            if discount_code:
                discount_rates = {"SAVE10": 0.10, "SAVE20": 0.20}
                discount = subtotal * discount_rates.get(discount_code, 0)

            # Calculate tax
            taxable_amount = subtotal - discount
            tax = taxable_amount * tax_rate

            total = taxable_amount + tax

            return {
                "subtotal": round(subtotal, 2),
                "discount": round(discount, 2),
                "tax": round(tax, 2),
                "total": round(total, 2),
                "discount_code": discount_code
            }

        @self.tool("Check inventory availability")
        def check_inventory(product_id: str, quantity: int) -> Dict[str, Any]:
            """Check if product is in stock"""
            # Simulated inventory check
            inventory = {
                "PROD001": 50,
                "PROD002": 30,
                "PROD003": 0
            }

            available = inventory.get(product_id, 0)

            return {
                "product_id": product_id,
                "requested_quantity": quantity,
                "available_quantity": available,
                "in_stock": available >= quantity,
                "can_fulfill": available >= quantity
            }

        @self.tool("Generate shipping estimate")
        def estimate_shipping(
            destination_zip: str,
            weight_lbs: float,
            shipping_method: str = "standard"
        ) -> Dict[str, Any]:
            """Estimate shipping cost and time"""
            # Simulated shipping calculation
            base_rates = {
                "standard": 5.99,
                "express": 12.99,
                "overnight": 24.99
            }

            rate = base_rates.get(shipping_method, 5.99)
            weight_surcharge = max(0, weight_lbs - 5) * 0.50

            delivery_days = {
                "standard": 7,
                "express": 3,
                "overnight": 1
            }

            estimated_delivery = datetime.datetime.now() + datetime.timedelta(
                days=delivery_days.get(shipping_method, 7)
            )

            return {
                "shipping_method": shipping_method,
                "cost": round(rate + weight_surcharge, 2),
                "estimated_delivery": estimated_delivery.strftime("%Y-%m-%d"),
                "destination_zip": destination_zip
            }
```

---

## 13. Conclusion

### 13.1 Summary

The OpenAI Agents Framework represents a significant evolution in building production-ready agentic AI applications. Key takeaways:

1. **Responses API** provides simplified access to hosted tools and RAG capabilities
2. **Agents SDK** enables multi-agent orchestration with handoffs, guardrails, and tracing
3. **AgentKit** offers visual tools for rapid agent development
4. **MCP integration** connects agents to enterprise systems
5. **A2A protocol** enables cross-organization agent collaboration

### 13.2 Best Practices

1. **Design**:
   - Start simple, add complexity as needed
   - Use handoffs for specialized tasks
   - Implement guardrails for safety
   - Enable tracing for debugging

2. **Development**:
   - Test tools independently
   - Use type hints and validation
   - Handle errors gracefully
   - Document agent instructions clearly

3. **Production**:
   - Monitor costs and usage
   - Implement rate limiting
   - Secure API keys and credentials
   - Log agent interactions
   - Plan for scaling

### 13.3 Resources

**Official Documentation:**
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Responses API Guide](https://platform.openai.com/docs/guides/agents-sdk)
- [Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [File Search & RAG](https://platform.openai.com/docs/assistants/tools/file-search)

**Community Resources:**
- [OpenAI Cookbook](https://cookbook.openai.com/topic/agents)
- [OpenAI Community Forum](https://community.openai.com/)
- [GitHub - openai-agents-python](https://github.com/openai/openai-agents-python)

**Model Context Protocol:**
- [MCP Documentation](https://platform.openai.com/docs/mcp)
- [FastMCP](https://gofastmcp.com/)
- [Building MCP Servers](https://developers.openai.com/apps-sdk/build/mcp-server/)

**Related Frameworks:**
- LangChain, LangGraph, CrewAI, AutoGen, Semantic Kernel

---

**End of OpenAI Agents Framework Deep Dive**

---

## Sources

- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/guides/agents-sdk)
- [OpenAI Agents SDK Python](https://openai.github.io/openai-agents-python/)
- [Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Assistants API File Search](https://platform.openai.com/docs/assistants/tools/file-search)
- [OpenAI Cookbook - Agents](https://cookbook.openai.com/topic/agents)
- [FastMCP OpenAI Integration](https://gofastmcp.com/integrations/openai)
- [MCP Documentation](https://platform.openai.com/docs/mcp)
- [Assistants API Deprecation Notice](https://community.openai.com/t/assistants-api-beta-deprecation-august-26-2026-sunset/1354666)
- [OpenAI for Developers 2025](https://developers.openai.com/blog/openai-for-developers-2025/)
- [Multi-Agent Portfolio Collaboration](https://cookbook.openai.com/examples/agents_sdk/multi-agent-portfolio-collaboration/multi_agent_portfolio_collaboration)
