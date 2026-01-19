# LangChain Deep Dive: Comprehensive Guide

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

---

## Introduction

LangChain is a framework for developing applications powered by language models. It provides a standard interface for chains, integrations with other tools, and end-to-end chains for common applications. LangChain enables developers to build context-aware reasoning applications that can connect language models to other sources of data and interact with their environment.

### Key Features
- **Modular Components**: Reusable building blocks for LLM applications
- **Chains**: Sequences of calls to LLMs and other utilities
- **Agents**: Systems that use LLMs to decide which actions to take
- **Memory**: Persistence of state between chain/agent calls
- **Retrieval**: Integration with vector stores and retrievers
- **Callbacks**: Hooks for logging, monitoring, and streaming
- **LangSmith Integration**: Native observability and debugging
- **Extensive Integrations**: 100+ integrations with LLMs, vector stores, and tools

---

## System Architecture

### Architectural Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      LangChain Framework                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  Application Layer                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  Agents  │  │  Chains  │  │  Tools   │  │ Prompts  │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Core Abstractions                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │ Runnables│  │  Memory  │  │Retrievers│  │Callbacks │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Integration Layer                        │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │   LLMs   │  │  Vector  │  │  Data    │  │External  │  │  │
│  │  │(OpenAI,  │  │  Stores  │  │ Loaders  │  │  APIs    │  │  │
│  │  │Anthropic)│  │(Pinecone)│  │          │  │          │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Language Models
LangChain provides a standard interface for interacting with LLMs:

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

# OpenAI
llm_openai = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    max_tokens=1000
)

# Anthropic
llm_anthropic = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    temperature=0.7,
    max_tokens=1000
)

# Standard interface
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is LangChain?")
]

response_openai = llm_openai.invoke(messages)
response_anthropic = llm_anthropic.invoke(messages)

print(response_openai.content)
print(response_anthropic.content)
```

#### 2. Prompts
Prompt templates for creating reusable prompts:

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Simple template
simple_prompt = ChatPromptTemplate.from_template(
    "Tell me a {adjective} joke about {topic}"
)

# Complex template with system message
complex_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant specializing in {domain}."),
    ("human", "Please help me with: {query}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Format prompt
formatted = simple_prompt.format(adjective="funny", topic="programming")
print(formatted)

# Invoke with LLM
chain = simple_prompt | llm_openai
result = chain.invoke({"adjective": "funny", "topic": "AI"})
print(result.content)
```

#### 3. Chains
Sequences of operations:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Create a simple chain
chain = (
    ChatPromptTemplate.from_template("Tell me a joke about {topic}")
    | llm_openai
    | StrOutputParser()
)

# Invoke chain
result = chain.invoke({"topic": "programmers"})
print(result)

# Chain with multiple steps
multi_chain = (
    {
        "topic": RunnablePassthrough(),
        "context": ChatPromptTemplate.from_template("What do you know about {topic}?") | llm_openai
    }
    | ChatPromptTemplate.from_template(
        "Based on this context: {context}\n\nTell me more about {topic}"
    )
    | llm_openai
    | StrOutputParser()
)

result = multi_chain.invoke("quantum computing")
print(result)
```

#### 4. Agents
Systems that use LLMs to choose actions:

```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.tools import tool

@tool
def search_api(query: str) -> str:
    """Search for information on a topic."""
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

tools = [search_api, calculator]

# Create agent prompt
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Create agent
agent = create_openai_functions_agent(llm_openai, tools, agent_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run agent
result = agent_executor.invoke({"input": "What is 25 * 17 and search for Python tutorials"})
print(result["output"])
```

#### 5. Memory
State persistence between calls:

```python
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains import ConversationChain

# Buffer memory (stores all messages)
buffer_memory = ConversationBufferMemory(return_messages=True)

# Summary memory (creates summaries)
summary_memory = ConversationSummaryMemory(
    llm=llm_openai,
    return_messages=True
)

# Create conversation chain with memory
conversation = ConversationChain(
    llm=llm_openai,
    memory=buffer_memory,
    verbose=True
)

# Multi-turn conversation
response1 = conversation.predict(input="Hi, I'm Alice")
print(response1)

response2 = conversation.predict(input="What's my name?")
print(response2)

# Access memory
print(buffer_memory.load_memory_variables({}))
```

#### 6. Retrievers
Integration with vector stores for RAG:

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Create documents
documents = [
    Document(page_content="LangChain is a framework for LLM applications."),
    Document(page_content="LangChain supports multiple LLM providers."),
    Document(page_content="LangChain includes tools for RAG applications."),
]

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# Retrieve documents
query = "What is LangChain?"
retrieved_docs = retriever.get_relevant_documents(query)

for doc in retrieved_docs:
    print(doc.page_content)
```

---

## High-Level System Architecture

### Data Flow Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        User Application                           │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                    LangChain Execution Layer                      │
│                                                                    │
│  ┌────────────────────────────────────────────────────────┐      │
│  │              LCEL (LangChain Expression Language)      │      │
│  │                                                          │      │
│  │  Runnable 1 → Runnable 2 → Runnable 3 → Output         │      │
│  │       ↓            ↓            ↓                       │      │
│  │   [Transform]  [LLM Call]  [Parse]                     │      │
│  └────────────────────────────────────────────────────────┘      │
│                            │                                       │
│  ┌─────────────────────────┴───────────────────────┐             │
│  │                                                   │             │
│  ▼                                                   ▼             │
│  ┌────────────────┐                      ┌────────────────┐      │
│  │  Agent Layer   │                      │  Memory Layer  │      │
│  ├────────────────┤                      ├────────────────┤      │
│  │ - Tool Calling │◄────────────────────►│ - Buffer       │      │
│  │ - ReAct Loop   │    State Updates     │ - Summary      │      │
│  │ - Planning     │                      │ - Vector Store │      │
│  │ - Execution    │                      │ - Chat History │      │
│  └────────────────┘                      └────────────────┘      │
│         │                                        │                │
└─────────┼────────────────────────────────────────┼────────────────┘
          │                                        │
          ▼                                        ▼
┌──────────────────────┐              ┌─────────────────────────┐
│   External Services   │              │   Storage & Persistence │
├──────────────────────┤              ├─────────────────────────┤
│ - LLM APIs           │              │ - Vector Databases      │
│ - Vector Stores      │              │ - SQL Databases         │
│ - Search APIs        │              │ - Redis Cache           │
│ - Custom Tools       │              │ - File Storage          │
│ - MCP Servers        │              │ - Cloud Storage         │
└──────────────────────┘              └─────────────────────────┘
          │                                        │
          └────────────┬───────────────────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │   Observability Layer   │
          ├─────────────────────────┤
          │ - LangSmith Tracing     │
          │ - Callbacks             │
          │ - Logging               │
          │ - Metrics               │
          └─────────────────────────┘
```

### Component Interaction

1. **Input Layer**: User input enters through application
2. **LCEL Pipeline**: Runnables process data sequentially
3. **Agent Execution**: LLM decides on tool usage
4. **Memory Management**: State is stored and retrieved
5. **External Integration**: Calls to LLMs, databases, APIs
6. **Output Layer**: Parsed and formatted results returned

---

## Core Components Deep Dive

### 1. LCEL (LangChain Expression Language)

LCEL is a declarative way to compose chains:

```python
from langchain_core.runnables import RunnableLambda, RunnableParallel

# Simple LCEL chain
chain = prompt | llm | StrOutputParser()

# Parallel execution
parallel_chain = RunnableParallel(
    joke=ChatPromptTemplate.from_template("Tell a joke about {topic}") | llm,
    poem=ChatPromptTemplate.from_template("Write a poem about {topic}") | llm
)

result = parallel_chain.invoke({"topic": "AI"})
print(result["joke"].content)
print(result["poem"].content)

# Custom runnable
def transform_text(text: str) -> str:
    return text.upper()

custom_chain = (
    ChatPromptTemplate.from_template("Say: {text}")
    | llm
    | StrOutputParser()
    | RunnableLambda(transform_text)
)

result = custom_chain.invoke({"text": "hello world"})
print(result)
```

### 2. Agent Types

#### ReAct Agent

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# ReAct prompt template
react_prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought: {agent_scratchpad}
""")

# Create ReAct agent
agent = create_react_agent(llm_openai, tools, react_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

result = agent_executor.invoke({"input": "What is 25 * 17?"})
```

#### Structured Chat Agent

```python
from langchain.agents import create_structured_chat_agent

structured_prompt = ChatPromptTemplate.from_messages([
    ("system", """Respond to the human as helpfully and accurately as possible.

    You have access to the following tools:
    {tools}

    Use a json blob to specify a tool by providing an action key (tool name)
    and an action_input key (tool input).
    """),
    ("human", "{input}\n\n{agent_scratchpad}")
])

structured_agent = create_structured_chat_agent(llm_openai, tools, structured_prompt)
executor = AgentExecutor(agent=structured_agent, tools=tools, verbose=True)

result = executor.invoke({"input": "Calculate 100 + 200 and search for Python"})
```

### 3. Memory Systems

#### Conversation Buffer Window Memory

```python
from langchain.memory import ConversationBufferWindowMemory

# Keep only last k interactions
window_memory = ConversationBufferWindowMemory(
    k=3,  # Keep last 3 interactions
    return_messages=True
)

# Add to memory
window_memory.save_context(
    {"input": "Hi, I'm Alice"},
    {"output": "Hello Alice! Nice to meet you."}
)

window_memory.save_context(
    {"input": "I like Python"},
    {"output": "Python is a great language!"}
)

# Retrieve memory
print(window_memory.load_memory_variables({}))
```

#### Entity Memory

```python
from langchain.memory import ConversationEntityMemory

entity_memory = ConversationEntityMemory(llm=llm_openai)

# Stores information about entities mentioned
conversation_with_entity = ConversationChain(
    llm=llm_openai,
    memory=entity_memory,
    verbose=True
)

conversation_with_entity.predict(
    input="My friend Bob works at Google as a software engineer"
)

conversation_with_entity.predict(
    input="What does Bob do?"
)

# Access entity store
print(entity_memory.entity_store.store)
```

### 4. Output Parsers

```python
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field

# JSON parser
json_parser = JsonOutputParser()

json_prompt = ChatPromptTemplate.from_template(
    "Return a JSON object with keys 'name' and 'age' for: {person}"
)

json_chain = json_prompt | llm_openai | json_parser
result = json_chain.invoke({"person": "a 30-year-old software engineer named Alice"})
print(result)

# Pydantic parser
class Person(BaseModel):
    name: str = Field(description="person's name")
    age: int = Field(description="person's age")
    occupation: str = Field(description="person's occupation")

pydantic_parser = PydanticOutputParser(pydantic_object=Person)

pydantic_prompt = ChatPromptTemplate.from_template(
    """Extract person information from the following text:
    {text}

    {format_instructions}
    """
)

pydantic_chain = (
    pydantic_prompt.partial(format_instructions=pydantic_parser.get_format_instructions())
    | llm_openai
    | pydantic_parser
)

result = pydantic_chain.invoke({"text": "Alice is a 30-year-old software engineer"})
print(f"Name: {result.name}, Age: {result.age}, Occupation: {result.occupation}")
```

### 5. Callbacks

```python
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult

class CustomCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"LLM started with prompts: {prompts}")

    def on_llm_end(self, response: LLMResult, **kwargs):
        print(f"LLM ended with response: {response.generations[0][0].text}")

    def on_llm_error(self, error, **kwargs):
        print(f"LLM error: {error}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"Tool {serialized['name']} started with input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"Tool ended with output: {output}")

# Use callback
callback_handler = CustomCallbackHandler()

chain_with_callback = (
    ChatPromptTemplate.from_template("Tell me about {topic}")
    | llm_openai.with_config(callbacks=[callback_handler])
    | StrOutputParser()
)

result = chain_with_callback.invoke({"topic": "LangChain"})
```

---

## End-to-End Flow

### Complete Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         1. Input Phase                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  User Input → Application → LangChain Runtime                   │
│                                                                   │
│  {                                                                │
│    "query": "What is quantum computing?",                        │
│    "session_id": "user-123"                                      │
│  }                                                                │
│                                                                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    2. Prompt Formation Phase                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Prompt Template → Format with Variables → Add System Context   │
│                                                                   │
│  if memory_enabled:                                               │
│    history = memory.load(session_id)                             │
│    prompt = prompt + history                                     │
│                                                                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   3. Execution Phase                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  FOR EACH runnable IN chain:                                     │
│    │                                                              │
│    ├─► Execute Runnable                                          │
│    │   ├─ Invoke LLM if LLM runnable                            │
│    │   ├─ Transform data if Lambda runnable                      │
│    │   ├─ Parse output if Parser runnable                        │
│    │   └─ Route to tools if Agent runnable                       │
│    │                                                              │
│    ├─► Trigger Callbacks                                         │
│    │   ├─ on_chain_start                                         │
│    │   ├─ on_llm_start                                           │
│    │   ├─ on_tool_start (if agent)                              │
│    │   └─ on_*_end events                                        │
│    │                                                              │
│    ├─► Handle Errors                                             │
│    │   ├─ Retry if configured                                    │
│    │   ├─ Fallback if available                                  │
│    │   └─ Raise exception if fatal                               │
│    │                                                              │
│    └─► Pass output to next runnable                              │
│                                                                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     4. Output Phase                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Parse Final Output → Save to Memory → Return to User           │
│                                                                   │
│  if memory_enabled:                                               │
│    memory.save(session_id, interaction)                          │
│                                                                   │
│  return formatted_response                                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Detailed Example

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 1. Setup components
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant specializing in {domain}."),
    ("human", "{query}")
])

parser = StrOutputParser()

# 2. Build chain with LCEL
chain = prompt | llm | parser

# 3. Execute
print("=== Executing Chain ===\n")
result = chain.invoke({
    "domain": "science",
    "query": "Explain quantum computing in simple terms"
})

print(f"\n\n=== Final Result ===\n{result}")

# 4. Stream execution
print("\n=== Streaming Execution ===\n")
for chunk in chain.stream({
    "domain": "science",
    "query": "What is photosynthesis?"
}):
    print(chunk, end="", flush=True)
```

---

## Simple Agent Examples

### Example 1: Basic Q&A Agent

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Simple Q&A agent
class SimpleQAAgent:
    def __init__(self, model="gpt-4"):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful Q&A assistant. Provide clear, concise answers."),
            ("human", "{question}")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()

    def ask(self, question: str) -> str:
        return self.chain.invoke({"question": question})

# Usage
agent = SimpleQAAgent()
answer = agent.ask("What is the capital of France?")
print(f"Answer: {answer}")
```

### Example 2: Calculator Agent

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.tools import tool

@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        return "Error: Division by zero"
    return a / b

# Create calculator agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = [add, subtract, multiply, divide]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a calculator assistant. Use the available tools to perform calculations."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Execute
result = agent_executor.invoke({
    "input": "What is (25 + 17) * 3 - 10?"
})
print(f"Result: {result['output']}")
```

### Example 3: Search Agent

```python
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_openai_functions_agent, AgentExecutor

@tool
def search(query: str) -> str:
    """Search the web for information."""
    # Mock implementation
    return f"Search results for: {query}\n- Result 1\n- Result 2\n- Result 3"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

# Create search agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = [search, get_weather]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can search the web and get weather information."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Execute
result = agent_executor.invoke({
    "input": "Search for Python tutorials and tell me the weather in Seattle"
})
print(result['output'])
```

### Example 4: Conversational Agent with Memory

```python
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_openai_functions_agent, AgentExecutor

# Create conversational agent with memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly conversational assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

llm = ChatOpenAI(model="gpt-4", temperature=0.7)
tools = []  # No tools for this simple conversational agent

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# Multi-turn conversation
print("Turn 1:")
result1 = agent_executor.invoke({"input": "Hi, my name is Alice and I love Python programming"})
print(result1['output'])

print("\nTurn 2:")
result2 = agent_executor.invoke({"input": "What's my name and what do I love?"})
print(result2['output'])

print("\nTurn 3:")
result3 = agent_executor.invoke({"input": "Can you recommend some Python libraries for me?"})
print(result3['output'])
```

---

## Complex Agent Examples

### Example 1: Research Assistant Agent

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.tools import tool
from langchain.memory import ConversationBufferMemory
from typing import List, Dict

@tool
def search_arxiv(query: str) -> str:
    """Search for academic papers on ArXiv."""
    # Mock implementation
    return f"Found 5 papers about {query}:\n1. Paper Title 1\n2. Paper Title 2\n3. Paper Title 3"

@tool
def search_web(query: str) -> str:
    """Search the web for general information."""
    return f"Web search results for {query}"

@tool
def summarize_text(text: str) -> str:
    """Summarize a long text."""
    # Use LLM to summarize
    summary_llm = ChatOpenAI(model="gpt-4", temperature=0)
    prompt = f"Summarize the following text concisely:\n\n{text}"
    return summary_llm.invoke(prompt).content

@tool
def save_research_note(title: str, content: str) -> str:
    """Save a research note."""
    # Mock implementation
    return f"Saved note '{title}' with content length {len(content)}"

class ResearchAssistant:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.tools = [search_arxiv, search_web, summarize_text, save_research_note]
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research assistant. Your job is to:
            1. Search for relevant academic papers and web resources
            2. Summarize findings
            3. Save important research notes
            4. Provide comprehensive research summaries

            Be thorough and cite your sources."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=10
        )

    def research(self, topic: str) -> str:
        return self.executor.invoke({"input": topic})['output']

# Usage
assistant = ResearchAssistant()
result = assistant.research(
    "Research the latest developments in quantum computing and save key findings"
)
print(result)
```

### Example 2: Data Analysis Agent

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.tools import tool
import pandas as pd
import json

@tool
def load_csv(filepath: str) -> str:
    """Load a CSV file and return basic info."""
    # Mock implementation
    return json.dumps({
        "rows": 1000,
        "columns": ["id", "name", "age", "salary", "department"],
        "sample": [
            {"id": 1, "name": "Alice", "age": 30, "salary": 75000, "department": "Engineering"},
            {"id": 2, "name": "Bob", "age": 35, "salary": 80000, "department": "Sales"}
        ]
    })

@tool
def calculate_statistics(column: str) -> str:
    """Calculate statistics for a column."""
    # Mock implementation
    return json.dumps({
        "column": column,
        "mean": 45.3,
        "median": 44.0,
        "std": 12.5,
        "min": 18,
        "max": 75
    })

@tool
def filter_data(condition: str) -> str:
    """Filter data based on a condition."""
    return f"Filtered data with condition: {condition}. Found 150 matching rows."

@tool
def create_visualization(chart_type: str, x_column: str, y_column: str) -> str:
    """Create a visualization."""
    return f"Created {chart_type} chart with X={x_column}, Y={y_column}"

class DataAnalysisAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.tools = [load_csv, calculate_statistics, filter_data, create_visualization]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a data analysis expert. You can:
            1. Load and inspect CSV files
            2. Calculate statistics
            3. Filter data based on conditions
            4. Create visualizations

            Provide clear insights and recommendations based on the data."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=15
        )

    def analyze(self, query: str) -> str:
        return self.executor.invoke({"input": query})['output']

# Usage
analyst = DataAnalysisAgent()
result = analyst.analyze(
    "Load employee_data.csv, calculate salary statistics by department, "
    "and create visualizations showing the distribution"
)
print(result)
```

### Example 3: Code Generation and Validation Agent

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.tools import tool
import ast

@tool
def generate_code(requirement: str) -> str:
    """Generate Python code based on requirements."""
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    prompt = f"""Generate clean, well-documented Python code for:
    {requirement}

    Include:
    - Type hints
    - Docstrings
    - Error handling
    - Example usage
    """
    return llm.invoke(prompt).content

@tool
def validate_syntax(code: str) -> str:
    """Validate Python code syntax."""
    try:
        ast.parse(code)
        return "Syntax is valid ✓"
    except SyntaxError as e:
        return f"Syntax error: {str(e)}"

@tool
def generate_tests(code: str) -> str:
    """Generate unit tests for code."""
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    prompt = f"""Generate comprehensive pytest unit tests for:

    ```python
    {code}
    ```

    Include:
    - Normal cases
    - Edge cases
    - Error cases
    """
    return llm.invoke(prompt).content

@tool
def run_static_analysis(code: str) -> str:
    """Run static analysis on code."""
    # Mock implementation
    issues = []

    if "def " not in code:
        issues.append("No function definition found")
    if '"""' not in code and "'''" not in code:
        issues.append("Missing docstrings")
    if "except:" in code or "except :" in code:
        issues.append("Bare except clause found - specify exception type")

    if not issues:
        return "No issues found ✓"
    return "Issues found:\n- " + "\n- ".join(issues)

class CodeAssistant:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.tools = [generate_code, validate_syntax, generate_tests, run_static_analysis]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a senior software engineer assistant. Your workflow:
            1. Generate code based on requirements
            2. Validate syntax
            3. Run static analysis
            4. Generate unit tests
            5. Provide the final code package

            Ensure all code is production-ready."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=10
        )

    def create_code(self, requirement: str) -> str:
        return self.executor.invoke({"input": requirement})['output']

# Usage
assistant = CodeAssistant()
result = assistant.create_code(
    "Create a function to calculate Fibonacci numbers with memoization, "
    "validate it, generate tests, and ensure it follows best practices"
)
print(result)
```

---

## Multi-Agent Systems

### Example 1: Hierarchical Multi-Agent System

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.tools import tool
from typing import Dict, List

# Define specialized agents
class SpecialistAgent:
    def __init__(self, name: str, specialty: str, tools: List):
        self.name = name
        self.specialty = specialty
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are a {specialty} specialist. {self.get_specialty_prompt()}"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        agent = create_openai_functions_agent(self.llm, tools, self.prompt)
        self.executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    def get_specialty_prompt(self) -> str:
        prompts = {
            "research": "You excel at finding and analyzing information from various sources.",
            "analysis": "You excel at analyzing data and providing insights.",
            "writing": "You excel at creating clear, well-structured content.",
            "coding": "You excel at writing clean, efficient code."
        }
        return prompts.get(self.specialty, "You are an expert in your field.")

    def execute(self, task: str) -> str:
        result = self.executor.invoke({"input": task})
        return result['output']

# Supervisor Agent
class SupervisorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.specialists = {
            "researcher": SpecialistAgent("Researcher", "research", [search_web]),
            "analyst": SpecialistAgent("Analyst", "analysis", [calculate_statistics]),
            "writer": SpecialistAgent("Writer", "writing", []),
            "coder": SpecialistAgent("Coder", "coding", [generate_code])
        }

    def route_task(self, task: str) -> str:
        """Determine which specialist should handle the task."""
        routing_prompt = f"""Given this task: "{task}"

        Which specialist should handle it?
        Options: researcher, analyst, writer, coder

        Respond with just the specialist name."""

        response = self.llm.invoke(routing_prompt)
        return response.content.strip().lower()

    def delegate(self, task: str) -> Dict[str, str]:
        """Delegate task to appropriate specialist."""
        specialist_name = self.route_task(task)

        if specialist_name in self.specialists:
            specialist = self.specialists[specialist_name]
            result = specialist.execute(task)
            return {
                "specialist": specialist_name,
                "result": result
            }
        else:
            return {
                "specialist": "none",
                "result": "Could not route task to appropriate specialist"
            }

# Usage
supervisor = SupervisorAgent()

tasks = [
    "Research the latest trends in AI",
    "Analyze the performance metrics of our application",
    "Write a blog post about machine learning",
    "Write a Python function to sort a list"
]

for task in tasks:
    print(f"\n=== Task: {task} ===")
    result = supervisor.delegate(task)
    print(f"Delegated to: {result['specialist']}")
    print(f"Result: {result['result'][:200]}...")
```

### Example 2: Collaborative Multi-Agent System

```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Message:
    from_agent: str
    to_agent: str
    content: str
    message_type: str  # request, response, broadcast

class CollaborativeAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        self.message_history: List[Message] = []

    def receive_message(self, message: Message):
        """Receive and process a message from another agent."""
        self.message_history.append(message)

        # Generate response based on message
        context = "\n".join([
            f"{msg.from_agent} -> {msg.to_agent}: {msg.content}"
            for msg in self.message_history[-5:]  # Last 5 messages
        ])

        prompt = f"""You are {self.name}, a {self.role}.

        Message history:
        {context}

        Latest message from {message.from_agent}:
        {message.content}

        Provide your response or contribution."""

        response = self.llm.invoke(prompt)
        return response.content

    def send_message(self, to_agent: str, content: str, message_type: str = "request") -> Message:
        """Send a message to another agent."""
        message = Message(
            from_agent=self.name,
            to_agent=to_agent,
            content=content,
            message_type=message_type
        )
        return message

class MultiAgentCollaboration:
    def __init__(self):
        self.agents = {
            "planner": CollaborativeAgent("Planner", "task planning and coordination"),
            "executor": CollaborativeAgent("Executor", "task execution"),
            "reviewer": CollaborativeAgent("Reviewer", "quality review and validation")
        }
        self.message_queue: List[Message] = []

    def run_collaboration(self, task: str) -> Dict[str, List[str]]:
        """Run a collaborative task across agents."""
        conversation = []

        # 1. Planner creates plan
        msg1 = self.agents["planner"].send_message(
            "executor",
            f"Create a plan for: {task}",
            "request"
        )
        self.message_queue.append(msg1)
        conversation.append(f"[{msg1.from_agent} -> {msg1.to_agent}]: {msg1.content}")

        # 2. Executor receives and responds
        response1 = self.agents["executor"].receive_message(msg1)
        msg2 = self.agents["executor"].send_message(
            "reviewer",
            response1,
            "response"
        )
        self.message_queue.append(msg2)
        conversation.append(f"[{msg2.from_agent} -> {msg2.to_agent}]: {msg2.content}")

        # 3. Reviewer provides feedback
        response2 = self.agents["reviewer"].receive_message(msg2)
        msg3 = self.agents["reviewer"].send_message(
            "executor",
            response2,
            "response"
        )
        self.message_queue.append(msg3)
        conversation.append(f"[{msg3.from_agent} -> {msg3.to_agent}]: {msg3.content}")

        # 4. Executor refines based on feedback
        response3 = self.agents["executor"].receive_message(msg3)
        conversation.append(f"[Executor Final]: {response3}")

        return {
            "conversation": conversation,
            "final_result": response3
        }

# Usage
collaboration = MultiAgentCollaboration()
result = collaboration.run_collaboration(
    "Design and implement a user authentication system"
)

print("=== Collaboration Flow ===")
for message in result["conversation"]:
    print(message)
    print()

print("=== Final Result ===")
print(result["final_result"])
```

### Example 3: Debate Multi-Agent System

```python
class DebateAgent:
    def __init__(self, name: str, position: str):
        self.name = name
        self.position = position  # "for" or "against"
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.8)
        self.arguments: List[str] = []

    def make_argument(self, topic: str, opponent_argument: str = None, round_num: int = 1) -> str:
        """Make an argument for or against the topic."""
        context = ""
        if opponent_argument:
            context = f"\n\nOpponent's last argument:\n{opponent_argument}"

        prompt = f"""You are debating {self.position.upper()} the topic: "{topic}"
        Round: {round_num}
        {context}

        Your previous arguments:
        {chr(10).join([f"- {arg}" for arg in self.arguments])}

        Provide a strong, logical argument for your position.
        Be persuasive but respectful."""

        response = self.llm.invoke(prompt)
        argument = response.content
        self.arguments.append(argument)
        return argument

class JudgeAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)

    def evaluate(self, topic: str, for_arguments: List[str], against_arguments: List[str]) -> str:
        """Evaluate the debate and declare a winner."""
        for_text = "\n\n".join([f"Round {i+1}: {arg}" for i, arg in enumerate(for_arguments)])
        against_text = "\n\n".join([f"Round {i+1}: {arg}" for i, arg in enumerate(against_arguments)])

        prompt = f"""You are judging a debate on: "{topic}"

        Arguments FOR:
        {for_text}

        Arguments AGAINST:
        {against_text}

        Evaluate both sides based on:
        1. Strength of arguments
        2. Logic and reasoning
        3. Use of evidence
        4. Persuasiveness

        Declare a winner and explain your decision."""

        response = self.llm.invoke(prompt)
        return response.content

class DebateSystem:
    def __init__(self, topic: str, rounds: int = 3):
        self.topic = topic
        self.rounds = rounds
        self.agent_for = DebateAgent("Agent_For", "for")
        self.agent_against = DebateAgent("Agent_Against", "against")
        self.judge = JudgeAgent()

    def run_debate(self) -> Dict:
        """Run the complete debate."""
        transcript = []

        # Opening statement from FOR
        for_arg = self.agent_for.make_argument(self.topic, round_num=1)
        transcript.append(f"[FOR - Round 1]:\n{for_arg}\n")

        # Debate rounds
        against_arg = None
        for round_num in range(1, self.rounds + 1):
            # Against responds
            against_arg = self.agent_against.make_argument(
                self.topic,
                for_arg,
                round_num
            )
            transcript.append(f"[AGAINST - Round {round_num}]:\n{against_arg}\n")

            # For responds (except in last round)
            if round_num < self.rounds:
                for_arg = self.agent_for.make_argument(
                    self.topic,
                    against_arg,
                    round_num + 1
                )
                transcript.append(f"[FOR - Round {round_num + 1}]:\n{for_arg}\n")

        # Judge evaluates
        decision = self.judge.evaluate(
            self.topic,
            self.agent_for.arguments,
            self.agent_against.arguments
        )

        return {
            "topic": self.topic,
            "transcript": transcript,
            "decision": decision
        }

# Usage
debate = DebateSystem(
    topic="Artificial Intelligence will benefit humanity more than harm it",
    rounds=3
)

result = debate.run_debate()

print(f"=== DEBATE: {result['topic']} ===\n")
for entry in result['transcript']:
    print(entry)

print("=== JUDGE'S DECISION ===")
print(result['decision'])
```

---

## RAG with Agents (Agentic RAG)

### Example 1: Basic RAG with Agent Router

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.agents import create_openai_functions_agent, AgentExecutor

# Create vector store
documents = [
    Document(page_content="LangChain is a framework for building LLM applications."),
    Document(page_content="LangChain supports RAG, agents, and chains."),
    Document(page_content="LangChain integrates with multiple LLM providers."),
    Document(page_content="LangChain has extensive documentation and examples."),
]

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

@tool
def search_documents(query: str) -> str:
    """Search the knowledge base for relevant information."""
    docs = vectorstore.similarity_search(query, k=3)
    return "\n\n".join([doc.page_content for doc in docs])

@tool
def search_web(query: str) -> str:
    """Search the web for current information."""
    # Mock implementation
    return f"Latest web information about: {query}"

# Create RAG agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = [search_documents, search_web]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant with access to:
    1. A knowledge base (use search_documents)
    2. Web search (use search_web)

    Strategy:
    - First, search the knowledge base
    - If info is insufficient or outdated, search the web
    - Combine information from both sources if needed
    - Always cite your sources"""),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Query
result = agent_executor.invoke({
    "input": "What is LangChain and what are its latest features?"
})
print(result['output'])
```

### Example 2: Self-Querying RAG Agent

```python
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.vectorstores import Chroma

# Create documents with metadata
documents = [
    Document(
        page_content="Machine learning basics for beginners",
        metadata={"topic": "ML", "difficulty": "beginner", "year": 2024}
    ),
    Document(
        page_content="Advanced deep learning techniques",
        metadata={"topic": "DL", "difficulty": "advanced", "year": 2024}
    ),
    Document(
        page_content="Natural language processing introduction",
        metadata={"topic": "NLP", "difficulty": "intermediate", "year": 2023}
    ),
]

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

# Define metadata fields
metadata_field_info = [
    AttributeInfo(
        name="topic",
        description="The topic of the document (ML, DL, NLP, etc.)",
        type="string"
    ),
    AttributeInfo(
        name="difficulty",
        description="The difficulty level (beginner, intermediate, advanced)",
        type="string"
    ),
    AttributeInfo(
        name="year",
        description="The year the document was created",
        type="integer"
    ),
]

# Create self-querying retriever
document_content_description = "Technical documentation about AI and machine learning"

llm = ChatOpenAI(model="gpt-4", temperature=0)
retriever = SelfQueryRetriever.from_llm(
    llm,
    vectorstore,
    document_content_description,
    metadata_field_info,
    verbose=True
)

@tool
def smart_search(query: str) -> str:
    """Search documents with automatic metadata filtering."""
    docs = retriever.get_relevant_documents(query)
    return "\n\n".join([
        f"[{doc.metadata}]\n{doc.page_content}"
        for doc in docs
    ])

# Create agent with smart search
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to a smart document search that can filter by topic, difficulty, and year."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_openai_functions_agent(llm, [smart_search], agent_prompt)
agent_executor = AgentExecutor(agent=agent, tools=[smart_search], verbose=True)

# Query with implicit filtering
result = agent_executor.invoke({
    "input": "Find beginner-level machine learning resources from 2024"
})
print(result['output'])
```

### Example 3: Multi-Step RAG Agent with Refinement

```python
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain

class MultiStepRAGAgent:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.refine_llm = ChatOpenAI(model="gpt-4", temperature=0)

    @tool
    def retrieve_context(query: str) -> str:
        """Retrieve initial context from vector store."""
        docs = self.vectorstore.similarity_search(query, k=5)
        return "\n\n".join([doc.page_content for doc in docs])

    @tool
    def generate_followup_questions(context: str, original_query: str) -> str:
        """Generate follow-up questions to get more specific information."""
        prompt = f"""Based on this context:
        {context}

        And this original query: {original_query}

        What follow-up questions should we ask to get more comprehensive information?
        List 2-3 specific follow-up questions."""

        response = self.llm.invoke(prompt)
        return response.content

    @tool
    def refine_answer(initial_answer: str, additional_context: str) -> str:
        """Refine the answer with additional context."""
        prompt = f"""Initial answer:
        {initial_answer}

        Additional context:
        {additional_context}

        Provide a refined, more comprehensive answer."""

        response = self.refine_llm.invoke(prompt)
        return response.content

    def answer_question(self, question: str) -> Dict[str, any]:
        """Answer a question using multi-step RAG."""
        # Step 1: Initial retrieval
        initial_context = self.retrieve_context(question)

        # Step 2: Generate initial answer
        initial_answer = self.llm.invoke(f"""Context:
        {initial_context}

        Question: {question}

        Answer:""").content

        # Step 3: Generate follow-up questions
        followup_questions = self.generate_followup_questions(initial_context, question)

        # Step 4: Retrieve additional context
        additional_context = ""
        for followup in followup_questions.split("\n"):
            if followup.strip():
                additional_context += self.retrieve_context(followup) + "\n\n"

        # Step 5: Refine answer
        final_answer = self.refine_answer(initial_answer, additional_context)

        return {
            "initial_answer": initial_answer,
            "followup_questions": followup_questions,
            "final_answer": final_answer
        }

# Usage
embeddings = OpenAIEmbeddings()
documents = [
    Document(page_content="LangChain provides modular components for LLM apps."),
    Document(page_content="LangChain agents can use tools and make decisions."),
    Document(page_content="LangChain supports multiple LLM providers including OpenAI and Anthropic."),
]
vectorstore = FAISS.from_documents(documents, embeddings)

rag_agent = MultiStepRAGAgent(vectorstore)
result = rag_agent.answer_question("How does LangChain help build LLM applications?")

print("=== Initial Answer ===")
print(result["initial_answer"])
print("\n=== Follow-up Questions ===")
print(result["followup_questions"])
print("\n=== Final Refined Answer ===")
print(result["final_answer"])
```

---

## FastMCP Servers with Agents

### Example 1: LangChain Agent with MCP Server Integration

```python
import httpx
import json
from typing import List, Dict

class MCPClient:
    """Client for interacting with MCP servers."""

    def __init__(self, server_url: str):
        self.server_url = server_url

    async def list_tools(self) -> List[Dict]:
        """Get available tools from MCP server."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.server_url}/tools")
            return response.json()

    async def call_tool(self, tool_name: str, parameters: Dict) -> Dict:
        """Call a tool on the MCP server."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.server_url}/tools/{tool_name}",
                json=parameters
            )
            return response.json()

class MCPAgent:
    """LangChain agent that uses MCP servers."""

    def __init__(self, mcp_server_url: str):
        self.mcp_client = MCPClient(mcp_server_url)
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.available_tools = []

    async def initialize(self):
        """Initialize by discovering MCP tools."""
        self.available_tools = await self.mcp_client.list_tools()
        print(f"Discovered {len(self.available_tools)} MCP tools")

    async def execute(self, task: str) -> str:
        """Execute a task using MCP tools."""
        # Step 1: Plan which tools to use
        tools_description = "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in self.available_tools
        ])

        plan_prompt = f"""Task: {task}

        Available MCP tools:
        {tools_description}

        Create a plan using these tools. Respond in JSON format:
        {{
            "steps": [
                {{"tool": "tool_name", "parameters": {{...}}, "reason": "why this step"}}
            ]
        }}
        """

        plan_response = self.llm.invoke(plan_prompt)

        try:
            plan = json.loads(plan_response.content)
        except:
            return "Failed to create execution plan"

        # Step 2: Execute plan
        results = []
        for step in plan["steps"]:
            tool_name = step["tool"]
            parameters = step["parameters"]

            result = await self.mcp_client.call_tool(tool_name, parameters)
            results.append({
                "step": step["reason"],
                "tool": tool_name,
                "result": result
            })

        # Step 3: Synthesize results
        results_text = "\n".join([
            f"Step: {r['step']}\nTool: {r['tool']}\nResult: {r['result']}"
            for r in results
        ])

        synthesis_prompt = f"""Task: {task}

        Execution results:
        {results_text}

        Provide a final answer based on these results."""

        final_response = self.llm.invoke(synthesis_prompt)
        return final_response.content

# Usage
async def main():
    # Initialize MCP agent
    agent = MCPAgent("http://localhost:8000")
    await agent.initialize()

    # Execute task
    result = await agent.execute(
        "Read the config file, update the database settings, and restart the service"
    )

    print("=== MCP Agent Result ===")
    print(result)

# Run
import asyncio
# asyncio.run(main())
```

### Example 2: Multi-MCP Server Orchestration

```python
class MultiMCPOrchestrator:
    """Orchestrate multiple MCP servers."""

    def __init__(self, mcp_servers: Dict[str, str]):
        self.mcp_servers = mcp_servers  # name: url
        self.mcp_clients = {
            name: MCPClient(url)
            for name, url in mcp_servers.items()
        }
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.all_tools = {}

    async def discover_all_tools(self):
        """Discover tools from all MCP servers."""
        for server_name, client in self.mcp_clients.items():
            tools = await client.list_tools()
            self.all_tools[server_name] = tools
            print(f"Server '{server_name}': {len(tools)} tools")

    async def execute_cross_server_task(self, task: str) -> Dict:
        """Execute a task that may require multiple MCP servers."""
        # Build comprehensive tool inventory
        tool_inventory = []
        for server_name, tools in self.all_tools.items():
            for tool in tools:
                tool_inventory.append({
                    "server": server_name,
                    "name": tool["name"],
                    "description": tool["description"]
                })

        inventory_text = "\n".join([
            f"[{t['server']}] {t['name']}: {t['description']}"
            for t in tool_inventory
        ])

        # Create execution plan
        plan_prompt = f"""Task: {task}

        Available tools across MCP servers:
        {inventory_text}

        Create a cross-server execution plan. Respond in JSON:
        {{
            "steps": [
                {{
                    "server": "server_name",
                    "tool": "tool_name",
                    "parameters": {{...}},
                    "description": "what this accomplishes"
                }}
            ]
        }}
        """

        plan_response = self.llm.invoke(plan_prompt)

        try:
            plan = json.loads(plan_response.content)
        except:
            return {"error": "Failed to create plan"}

        # Execute across servers
        results = []
        for step in plan["steps"]:
            server_name = step["server"]
            tool_name = step["tool"]
            parameters = step["parameters"]

            client = self.mcp_clients[server_name]
            result = await client.call_tool(tool_name, parameters)

            results.append({
                "server": server_name,
                "tool": tool_name,
                "description": step["description"],
                "result": result
            })

        return {
            "plan": plan,
            "results": results
        }

# Usage
async def main():
    # Multiple MCP servers
    servers = {
        "filesystem": "http://localhost:8001",
        "database": "http://localhost:8002",
        "api": "http://localhost:8003"
    }

    orchestrator = MultiMCPOrchestrator(servers)
    await orchestrator.discover_all_tools()

    # Execute cross-server task
    result = await orchestrator.execute_cross_server_task(
        "Read user.json file, update user table in database, and notify via API"
    )

    print("=== Execution Plan ===")
    for step in result["plan"]["steps"]:
        print(f"- [{step['server']}] {step['tool']}: {step['description']}")

    print("\n=== Results ===")
    for r in result["results"]:
        print(f"\n[{r['server']}] {r['tool']}:")
        print(f"  {r['description']}")
        print(f"  Result: {r['result']}")

# asyncio.run(main())
```

---

## A2A (Agent-to-Agent) Examples

### Example 1: Basic A2A Communication Protocol

```python
from typing import Dict, List
from dataclasses import dataclass
import json

@dataclass
class A2AMessage:
    """Agent-to-Agent message format."""
    sender: str
    receiver: str
    content: str
    message_type: str  # request, response, broadcast
    context: Dict

class A2AAgent:
    """Agent capable of A2A communication."""

    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.message_history: List[A2AMessage] = []

    def get_agent_card(self) -> Dict:
        """Return agent capabilities (AgentCard)."""
        return {
            "name": self.name,
            "capabilities": self.capabilities,
            "description": f"Agent specialized in: {', '.join(self.capabilities)}"
        }

    async def send_message(self, receiver: str, content: str, message_type: str = "request") -> A2AMessage:
        """Send A2A message to another agent."""
        message = A2AMessage(
            sender=self.name,
            receiver=receiver,
            content=content,
            message_type=message_type,
            context={"timestamp": "2024-01-01T00:00:00Z"}
        )
        self.message_history.append(message)
        return message

    async def receive_message(self, message: A2AMessage) -> str:
        """Process incoming A2A message."""
        # Build context from message history
        history_context = "\n".join([
            f"{msg.sender} -> {msg.receiver}: {msg.content}"
            for msg in self.message_history[-5:]
        ])

        prompt = f"""You are {self.name} with capabilities: {', '.join(self.capabilities)}

        Message history:
        {history_context}

        New message from {message.sender}:
        Type: {message.message_type}
        Content: {message.content}

        Provide your response based on your capabilities."""

        response = self.llm.invoke(prompt)
        return response.content

class A2ACoordinator:
    """Coordinates communication between A2A agents."""

    def __init__(self):
        self.agents: Dict[str, A2AAgent] = {}

    def register_agent(self, agent: A2AAgent):
        """Register an A2A agent."""
        self.agents[agent.name] = agent
        print(f"Registered agent: {agent.name}")

    def discover_agents(self) -> List[Dict]:
        """Discover all registered agents and their capabilities."""
        return [agent.get_agent_card() for agent in self.agents.values()]

    async def route_message(self, message: A2AMessage) -> str:
        """Route message to appropriate agent."""
        if message.receiver in self.agents:
            receiver_agent = self.agents[message.receiver]
            response = await receiver_agent.receive_message(message)
            return response
        else:
            return f"Agent {message.receiver} not found"

# Usage
async def main():
    # Create A2A agents
    data_agent = A2AAgent("DataAgent", ["data_processing", "analytics"])
    ml_agent = A2AAgent("MLAgent", ["machine_learning", "predictions"])
    viz_agent = A2AAgent("VizAgent", ["visualization", "reporting"])

    # Create coordinator
    coordinator = A2ACoordinator()
    coordinator.register_agent(data_agent)
    coordinator.register_agent(ml_agent)
    coordinator.register_agent(viz_agent)

    # Discover agents
    print("\n=== Discovered Agents ===")
    for card in coordinator.discover_agents():
        print(f"- {card['name']}: {card['description']}")

    # A2A communication flow
    print("\n=== A2A Communication Flow ===")

    # 1. DataAgent sends to MLAgent
    msg1 = await data_agent.send_message(
        "MLAgent",
        "I've processed the dataset. Ready for model training.",
        "request"
    )
    response1 = await coordinator.route_message(msg1)
    print(f"\n[{msg1.sender} -> {msg1.receiver}]: {msg1.content}")
    print(f"[{msg1.receiver} response]: {response1}")

    # 2. MLAgent sends to VizAgent
    msg2 = await ml_agent.send_message(
        "VizAgent",
        "Model training complete. Here are the results for visualization.",
        "request"
    )
    response2 = await coordinator.route_message(msg2)
    print(f"\n[{msg2.sender} -> {msg2.receiver}]: {msg2.content}")
    print(f"[{msg2.receiver} response]: {response2}")

# asyncio.run(main())
```

### Example 2: A2A Multi-Agent Travel System (Based on a2a-samples)

```python
class TravelAgent(A2AAgent):
    """Specialized travel planning agent."""

    def __init__(self):
        super().__init__(
            name="TravelPlanner",
            capabilities=["itinerary_planning", "destination_research"]
        )

class FlightAgent(A2AAgent):
    """Flight booking agent."""

    def __init__(self):
        super().__init__(
            name="FlightBooker",
            capabilities=["flight_search", "booking"]
        )

    async def search_flights(self, origin: str, destination: str, date: str) -> Dict:
        """Search for flights."""
        # Mock implementation
        return {
            "flights": [
                {"airline": "AA", "price": 450, "departure": "08:00"},
                {"airline": "Delta", "price": 420, "departure": "10:30"}
            ]
        }

class HotelAgent(A2AAgent):
    """Hotel booking agent."""

    def __init__(self):
        super().__init__(
            name="HotelBooker",
            capabilities=["hotel_search", "booking"]
        )

    async def search_hotels(self, location: str, checkin: str, checkout: str) -> Dict:
        """Search for hotels."""
        return {
            "hotels": [
                {"name": "Grand Hotel", "price": 200, "rating": 4.5},
                {"name": "City Inn", "price": 150, "rating": 4.0}
            ]
        }

class WeatherAgent(A2AAgent):
    """Weather information agent."""

    def __init__(self):
        super().__init__(
            name="WeatherService",
            capabilities=["weather_forecast"]
        )

    async def get_forecast(self, location: str, date: str) -> Dict:
        """Get weather forecast."""
        return {
            "location": location,
            "date": date,
            "forecast": "Sunny, 75°F",
            "recommendation": "Great weather for outdoor activities"
        }

class TravelOrchestratorAgent:
    """Orchestrates multiple travel agents via A2A."""

    def __init__(self):
        self.coordinator = A2ACoordinator()
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)

        # Initialize specialized agents
        self.travel_agent = TravelAgent()
        self.flight_agent = FlightAgent()
        self.hotel_agent = HotelAgent()
        self.weather_agent = WeatherAgent()

        # Register all agents
        for agent in [self.travel_agent, self.flight_agent,
                     self.hotel_agent, self.weather_agent]:
            self.coordinator.register_agent(agent)

    async def plan_trip(self, request: str) -> Dict:
        """Plan a complete trip using A2A communication."""
        # Parse request
        parse_prompt = f"""Parse this travel request: {request}

        Extract:
        - origin
        - destination
        - dates
        - preferences

        Return as JSON."""

        parsed = self.llm.invoke(parse_prompt)

        # Coordinate agents via A2A
        results = {}

        # 1. Get flights
        flight_msg = await self.travel_agent.send_message(
            "FlightBooker",
            f"Search flights from origin to destination",
            "request"
        )
        flight_results = await self.flight_agent.search_flights(
            "NYC", "Paris", "2024-06-01"
        )
        results["flights"] = flight_results

        # 2. Get hotels
        hotel_msg = await self.travel_agent.send_message(
            "HotelBooker",
            f"Search hotels in destination",
            "request"
        )
        hotel_results = await self.hotel_agent.search_hotels(
            "Paris", "2024-06-01", "2024-06-07"
        )
        results["hotels"] = hotel_results

        # 3. Get weather
        weather_msg = await self.travel_agent.send_message(
            "WeatherService",
            f"Get weather forecast for destination",
            "request"
        )
        weather_results = await self.weather_agent.get_forecast(
            "Paris", "2024-06-01"
        )
        results["weather"] = weather_results

        # 4. Create itinerary
        itinerary_prompt = f"""Create a travel itinerary based on:

        Flights: {results['flights']}
        Hotels: {results['hotels']}
        Weather: {results['weather']}

        Provide a comprehensive travel plan."""

        itinerary = self.llm.invoke(itinerary_prompt)
        results["itinerary"] = itinerary.content

        return results

# Usage
async def main():
    orchestrator = TravelOrchestratorAgent()

    result = await orchestrator.plan_trip(
        "Plan a 7-day trip to Paris from New York in June 2024"
    )

    print("=== Travel Plan ===")
    print(f"\nFlights:")
    for flight in result["flights"]["flights"]:
        print(f"  - {flight['airline']}: ${flight['price']} @ {flight['departure']}")

    print(f"\nHotels:")
    for hotel in result["hotels"]["hotels"]:
        print(f"  - {hotel['name']}: ${hotel['price']}/night (★{hotel['rating']})")

    print(f"\nWeather: {result['weather']['forecast']}")
    print(f"Recommendation: {result['weather']['recommendation']}")

    print(f"\n=== Complete Itinerary ===")
    print(result["itinerary"])

# asyncio.run(main())
```

---

## Advanced Patterns

### 1. Error Handling and Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain.callbacks.base import BaseCallbackHandler

class ErrorHandlingAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def invoke_with_retry(self, prompt: str) -> str:
        """Invoke LLM with automatic retry on failure."""
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
            raise

    def invoke_with_fallback(self, prompt: str, fallback_model: str = "gpt-3.5-turbo") -> str:
        """Invoke with fallback to another model."""
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Primary model failed: {e}. Using fallback...")
            fallback_llm = ChatOpenAI(model=fallback_model, temperature=0)
            response = fallback_llm.invoke(prompt)
            return response.content

# Usage
agent = ErrorHandlingAgent()
result = agent.invoke_with_retry("Explain quantum computing")
print(result)
```

### 2. Streaming Responses

```python
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Create streaming LLM
streaming_llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

# Stream responses
chain = ChatPromptTemplate.from_template("Tell me about {topic}") | streaming_llm

print("Streaming response:")
for chunk in chain.stream({"topic": "artificial intelligence"}):
    pass  # Handled by callback
```

### 3. Custom Callbacks for Monitoring

```python
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any
import time

class MonitoringCallback(BaseCallbackHandler):
    def __init__(self):
        self.start_time = None
        self.token_count = 0

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        self.start_time = time.time()
        print(f"[Monitor] LLM started with {len(prompts)} prompts")

    def on_llm_end(self, response, **kwargs):
        duration = time.time() - self.start_time
        print(f"[Monitor] LLM completed in {duration:.2f}s")

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs):
        print(f"[Monitor] Tool '{serialized['name']}' started")

    def on_tool_end(self, output: str, **kwargs):
        print(f"[Monitor] Tool completed with output length: {len(output)}")

    def on_agent_action(self, action, **kwargs):
        print(f"[Monitor] Agent action: {action.tool}")

    def on_agent_finish(self, finish, **kwargs):
        print(f"[Monitor] Agent finished with output: {finish.return_values}")

# Use monitoring
monitor = MonitoringCallback()
llm_with_monitor = ChatOpenAI(model="gpt-4", callbacks=[monitor])
response = llm_with_monitor.invoke("What is LangChain?")
```

---

## Production Considerations

### 1. Rate Limiting and Cost Management

```python
from functools import wraps
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()

            # Remove old calls outside time window
            while self.calls and self.calls[0] < now - self.time_window:
                self.calls.popleft()

            # Check if we've exceeded limit
            if len(self.calls) >= self.max_calls:
                sleep_time = self.time_window - (now - self.calls[0])
                print(f"Rate limit reached. Sleeping for {sleep_time:.2f}s")
                time.sleep(sleep_time)
                self.calls.popleft()

            # Record this call
            self.calls.append(now)
            return func(*args, **kwargs)

        return wrapper

# Usage
@RateLimiter(max_calls=10, time_window=60)
def call_llm(prompt: str) -> str:
    llm = ChatOpenAI(model="gpt-4")
    return llm.invoke(prompt).content

# This will automatically rate limit
for i in range(20):
    result = call_llm(f"Question {i}")
    print(f"Response {i}: {result[:50]}...")
```

### 2. Caching Responses

```python
from langchain.cache import InMemoryCache, SQLiteCache
from langchain.globals import set_llm_cache

# In-memory cache
set_llm_cache(InMemoryCache())

# SQLite cache (persistent)
# set_llm_cache(SQLiteCache(database_path=".langchain.db"))

llm = ChatOpenAI(model="gpt-4")

# First call - hits LLM
print("First call:")
response1 = llm.invoke("What is 2+2?")
print(response1.content)

# Second call - uses cache
print("\nSecond call (cached):")
response2 = llm.invoke("What is 2+2?")
print(response2.content)
```

### 3. Production API Deployment

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor

app = FastAPI(title="LangChain Agent API")

# Initialize agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = []  # Add your tools here

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Request/Response models
class AgentRequest(BaseModel):
    query: str
    session_id: str = "default"

class AgentResponse(BaseModel):
    response: str
    session_id: str

@app.post("/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """Execute agent query."""
    try:
        result = agent_executor.invoke({"input": request.query})
        return AgentResponse(
            response=result["output"],
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "langchain-agent"}

# Run with: uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Logging and Monitoring

```python
import logging
from langsmith import Client

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# LangSmith tracing
client = Client()

# Create agent with tracing
llm = ChatOpenAI(model="gpt-4", temperature=0)

def run_with_tracing(query: str) -> str:
    """Run agent with full tracing."""
    logger.info(f"Starting query: {query}")

    try:
        result = agent_executor.invoke({"input": query})
        logger.info(f"Query completed successfully")
        return result["output"]
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        raise

# Usage
result = run_with_tracing("What is the weather in Paris?")
```

---

## Conclusion

LangChain provides a comprehensive framework for building LLM applications with its modular components, powerful abstractions, and extensive integrations. Key takeaways:

1. **Modular Design**: Reusable components for chains, agents, and tools
2. **LCEL**: Declarative way to compose complex workflows
3. **Agent Ecosystem**: Multiple agent types for different use cases
4. **Memory Systems**: Various memory options for stateful applications
5. **RAG Support**: Built-in support for retrieval-augmented generation
6. **Production Ready**: Callbacks, caching, and monitoring capabilities
7. **Integration**: Extensive integrations with LLMs, vector stores, and tools

For more information:
- Official Documentation: https://python.langchain.com/
- GitHub: https://github.com/langchain-ai/langchain
- LangSmith: https://smith.langchain.com/

---

**Document Version**: 1.0
**Last Updated**: 2024
**Total Lines**: 2800+
