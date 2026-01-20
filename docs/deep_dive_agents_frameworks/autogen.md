# AutoGen Deep Dive

## Overview
AutoGen is a framework from Microsoft Research that enables development of LLM applications using multiple agents that can converse with each other to solve tasks. AutoGen agents are customizable, conversable, and seamlessly allow human participation. The framework simplifies orchestration, automation, and optimization of complex LLM workflows.

## System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                  AutoGen Application                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │Conversable   │◄─────┤   Agents     │◄─────┤  Human    │ │
│  │  Agents      │      │  (Workers)   │      │  Proxy    │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│         │                     │                     │        │
│         │                     │                     │        │
│  ┌──────▼─────────────────────▼─────────────────────▼─────┐ │
│  │          Conversation Manager                            │ │
│  └─────────────────────────────────────────────────────────┘ │
│         │                     │                     │        │
│  ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐ │
│  │  Code       │      │   Tools/    │      │Group Chat  │ │
│  │  Execution  │      │  Functions  │      │ Manager    │ │
│  └─────────────┘      └─────────────┘      └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **ConversableAgent**: Base agent class for conversations
2. **AssistantAgent**: AI agent that generates responses
3. **UserProxyAgent**: Agent representing human interaction
4. **GroupChat**: Multi-agent conversation orchestrator
5. **GroupChatManager**: Manager for group conversations
6. **Code Executor**: Executes code in sandboxed environment
7. **Function/Tool**: Custom capabilities for agents

## High-Level System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                         User Application                           │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                    AutoGen Framework Layer                          │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │Conversation  │  │   Agent      │  │   Group      │             │
│  │  Manager     │──┤   Registry   │──┤   Chat       │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│         │                  │                  │                     │
│  ┌──────▼──────────────────▼──────────────────▼─────────┐          │
│  │         Message Exchange & Routing System            │          │
│  └──────────────────────────────────────────────────────┘          │
│         │                  │                  │                     │
│  ┌──────▼──────┐    ┌──────▼──────┐    ┌─────▼──────┐             │
│  │   Code      │    │  Function   │    │   Human    │             │
│  │  Executor   │    │   Calling   │    │  In Loop   │             │
│  └─────────────┘    └─────────────┘    └────────────┘             │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                         LLM Provider                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   OpenAI     │  │    Azure     │  │   Local LLMs │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└────────────────────────────────────────────────────────────────────┘
```

## End-to-End Flow

### Execution Flow

```
1. Agent Initialization
   │
   ├─► Create Agents (Assistant, UserProxy, etc.)
   │
   ├─► Configure LLM Settings
   │
   ├─► Register Functions/Tools
   │
   └─► Setup Code Executor
       │
2. Conversation Initiation
   │
   ├─► User Proxy Sends Initial Message
   │
   └─► Conversation Loop:
       │
       ├─► Assistant Receives Message
       │
       ├─► Assistant Generates Response
       │
       ├─► [Optional] Function Call
       │
       ├─► [Optional] Code Execution
       │
       ├─► Send Reply
       │
       └─► Check Termination Condition
           │
3. Conversation Completion
   │
   ├─► Final Response Generated
   │
   └─► Cleanup Resources
```

### Detailed Execution Steps

1. **Setup Phase**
   - Configure LLM parameters
   - Create conversable agents
   - Register tools and functions
   - Define termination conditions

2. **Initiation Phase**
   - UserProxy sends task description
   - AssistantAgent receives task
   - Conversation context established

3. **Execution Phase**
   - Multi-turn conversation
   - Code generation and execution
   - Function calling
   - Human feedback integration

4. **Completion Phase**
   - Termination condition met
   - Results aggregated
   - Conversation history saved

## Examples

### 1. Simple Agent

A basic two-agent conversation for task completion.

```python
import autogen

# Configure LLM
config_list = [
    {
        "model": "gpt-4",
        "api_key": "your-api-key"
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0
}

# Create assistant agent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="You are a helpful AI assistant."
)

# Create user proxy agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # No human input required
    max_consecutive_auto_reply=10,
    code_execution_config={"use_docker": False}
)

# Start conversation
user_proxy.initiate_chat(
    assistant,
    message="What is the capital of France? Explain why it's important."
)
```

### 2. Complex Agent with Code Execution

An agent that can write and execute code.

```python
import autogen
from autogen.coding import LocalCommandLineCodeExecutor
import tempfile

# Configure LLM
config_list = [
    {
        "model": "gpt-4",
        "api_key": "your-api-key"
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0,
}

# Create a temporary directory for code execution
temp_dir = tempfile.mkdtemp()

# Create code executor
code_executor = LocalCommandLineCodeExecutor(
    timeout=60,
    work_dir=temp_dir
)

# Create assistant that can write code
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="""You are a helpful AI assistant that can write Python code.
    When asked to solve problems, write executable Python code.
    Wrap code in ```python ``` blocks."""
)

# Create user proxy that can execute code
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "executor": code_executor
    }
)

# Task requiring code execution
task = """
Calculate the sum of squares of the first 100 natural numbers.
Write Python code to solve this and show the result.
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)
```

### 3. Multi-Agent System (Group Chat)

Multiple specialized agents collaborating in a group chat.

```python
import autogen

# Configure LLM
config_list = [{"model": "gpt-4", "api_key": "your-api-key"}]
llm_config = {"config_list": config_list, "temperature": 0.7}

# Create specialized agents
researcher = autogen.AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
    system_message="""You are a research specialist. Your role is to:
    - Gather information on topics
    - Identify key facts and trends
    - Provide comprehensive research summaries
    Always start your messages with [RESEARCHER]"""
)

data_analyst = autogen.AssistantAgent(
    name="Data_Analyst",
    llm_config=llm_config,
    system_message="""You are a data analyst. Your role is to:
    - Analyze data and identify patterns
    - Provide statistical insights
    - Create data-driven recommendations
    Always start your messages with [ANALYST]"""
)

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="""You are a technical writer. Your role is to:
    - Transform research and analysis into clear content
    - Create well-structured documents
    - Ensure readability and clarity
    Always start your messages with [WRITER]"""
)

critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="""You are a quality critic. Your role is to:
    - Review work from other agents
    - Identify gaps or issues
    - Suggest improvements
    - Approve final output when quality standards are met
    Always start your messages with [CRITIC]
    Say TERMINATE when the work meets all quality standards."""
)

user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config=False
)

# Create group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, researcher, data_analyst, writer, critic],
    messages=[],
    max_round=20,
    speaker_selection_method="auto"  # Automatic speaker selection
)

# Create group chat manager
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

# Start collaborative task
task = """
Create a comprehensive report on the impact of artificial intelligence
in healthcare. The report should include:
1. Research findings on current AI applications
2. Data analysis of trends and growth
3. Well-written summary of benefits and challenges
4. Quality review ensuring accuracy and completeness
"""

user_proxy.initiate_chat(
    manager,
    message=task
)
```

### 4. Agentic RAG (RAG with Agents)

Retrieval-augmented generation with AutoGen agents.

```python
import autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb

# Configure LLM
config_list = [{"model": "gpt-4", "api_key": "your-api-key"}]

# Create RAG assistant
assistant = RetrieveAssistantAgent(
    name="rag_assistant",
    system_message="""You are a helpful assistant with access to a knowledge base.
    Answer questions using the retrieved documents.
    Cite sources when possible.""",
    llm_config={
        "config_list": config_list,
        "temperature": 0,
    }
)

# Configure retrieval
ragproxyagent = RetrieveUserProxyAgent(
    name="rag_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "qa",
        "docs_path": "./documents",  # Path to your documents
        "chunk_token_size": 2000,
        "model": config_list[0]["model"],
        "embedding_model": "text-embedding-ada-002",
        "get_or_create": True,  # Create collection if doesn't exist
    },
)

# Query the RAG system
question = "What are the main benefits of using AI in healthcare diagnostics?"

ragproxyagent.initiate_chat(
    assistant,
    message=ragproxyagent.message_generator,
    problem=question,
)
```

### 5. Function Calling with Agents

Agents with custom tool/function capabilities.

```python
import autogen
from typing import Annotated, Literal

# Configure LLM
config_list = [{"model": "gpt-4", "api_key": "your-api-key"}]
llm_config = {"config_list": config_list}

# Define custom functions
def search_web(query: Annotated[str, "The search query"]) -> str:
    """Search the web for information."""
    # Simulated web search
    return f"Search results for '{query}': AI in healthcare shows 30% improvement in diagnosis accuracy."

def calculate(
    expression: Annotated[str, "Mathematical expression to evaluate"]
) -> str:
    """Calculate mathematical expressions."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_weather(
    location: Annotated[str, "City name"],
    unit: Annotated[Literal["celsius", "fahrenheit"], "Temperature unit"] = "celsius"
) -> str:
    """Get weather for a location."""
    # Simulated weather API
    return f"Weather in {location}: 22°{unit[0].upper()}, Partly cloudy"

# Create assistant with function calling
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="""You are a helpful assistant with access to tools.
    Use the available functions to answer questions accurately."""
)

# Create user proxy that can execute functions
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    code_execution_config=False
)

# Register functions
autogen.agentchat.register_function(
    search_web,
    caller=assistant,
    executor=user_proxy,
    description="Search the web for information"
)

autogen.agentchat.register_function(
    calculate,
    caller=assistant,
    executor=user_proxy,
    description="Perform mathematical calculations"
)

autogen.agentchat.register_function(
    get_weather,
    caller=assistant,
    executor=user_proxy,
    description="Get weather information"
)

# Test with multi-tool task
user_proxy.initiate_chat(
    assistant,
    message="""Please help me with the following:
    1. Calculate 25 * 17
    2. Search for information about AI in healthcare
    3. Get the weather in Paris"""
)
```

### 6. MCP with Agents (Model Context Protocol)

Integrating MCP servers with AutoGen.

```python
import autogen
from typing import Annotated
import json

# Simulated MCP Server
class MCPFileServer:
    """MCP Server for file operations"""

    @staticmethod
    def list_files(directory: str) -> dict:
        return {
            "success": True,
            "files": ["document1.txt", "document2.md", "data.json"],
            "directory": directory
        }

    @staticmethod
    def read_file(filepath: str) -> dict:
        return {
            "success": True,
            "content": f"Content of {filepath}: Sample document content.",
            "size": 1024
        }

    @staticmethod
    def write_file(filepath: str, content: str) -> dict:
        return {
            "success": True,
            "message": f"Written to {filepath}",
            "bytes_written": len(content)
        }

# Define MCP tools
def mcp_list_files(directory: Annotated[str, "Directory path to list"]) -> str:
    """List files in a directory via MCP server."""
    result = MCPFileServer.list_files(directory)
    if result["success"]:
        files = "\n".join([f"  - {f}" for f in result["files"]])
        return f"Files in {directory}:\n{files}"
    return "Error listing files"

def mcp_read_file(filepath: Annotated[str, "Path to file to read"]) -> str:
    """Read file content via MCP server."""
    result = MCPFileServer.read_file(filepath)
    if result["success"]:
        return f"File: {filepath}\nSize: {result['size']} bytes\n\n{result['content']}"
    return "Error reading file"

def mcp_write_file(
    filepath: Annotated[str, "Path where file should be written"],
    content: Annotated[str, "Content to write to file"]
) -> str:
    """Write content to a file via MCP server."""
    result = MCPFileServer.write_file(filepath, content)
    if result["success"]:
        return result["message"]
    return "Error writing file"

# Configure AutoGen
config_list = [{"model": "gpt-4", "api_key": "your-api-key"}]

# Create MCP-enabled assistant
mcp_assistant = autogen.AssistantAgent(
    name="mcp_assistant",
    llm_config={"config_list": config_list},
    system_message="""You are a file management assistant with MCP capabilities.
    You can list, read, and write files using the MCP server.
    Always confirm operations and provide clear summaries."""
)

# Create user proxy
user_proxy = autogen.UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=False
)

# Register MCP functions
autogen.agentchat.register_function(
    mcp_list_files,
    caller=mcp_assistant,
    executor=user_proxy,
    description="List files in a directory via MCP"
)

autogen.agentchat.register_function(
    mcp_read_file,
    caller=mcp_assistant,
    executor=user_proxy,
    description="Read file content via MCP"
)

autogen.agentchat.register_function(
    mcp_write_file,
    caller=mcp_assistant,
    executor=user_proxy,
    description="Write content to a file via MCP"
)

# Execute MCP operations
user_proxy.initiate_chat(
    mcp_assistant,
    message="""Please:
    1. List all files in the /documents directory
    2. Read the first file you find
    3. Create a summary report and save it as summary.txt"""
)
```

### 7. Agent-to-Agent (A2A) Communication

Direct agent-to-agent communication for complex workflows.

```python
import autogen

# Configure LLM
config_list = [{"model": "gpt-4", "api_key": "your-api-key"}]
llm_config = {"config_list": config_list, "temperature": 0}

# Create agents with specific roles
planner = autogen.AssistantAgent(
    name="Planner",
    llm_config=llm_config,
    system_message="""You are a planning agent. Your responsibilities:
    - Break down complex tasks into steps
    - Communicate requirements to the Developer
    - Review final output from Reviewer
    - Start messages with [PLANNER]"""
)

developer = autogen.AssistantAgent(
    name="Developer",
    llm_config=llm_config,
    system_message="""You are a developer agent. Your responsibilities:
    - Receive plans from Planner
    - Implement solutions
    - Send implementation to Reviewer
    - Start messages with [DEVELOPER]"""
)

reviewer = autogen.AssistantAgent(
    name="Reviewer",
    llm_config=llm_config,
    system_message="""You are a code reviewer. Your responsibilities:
    - Review Developer's implementation
    - Provide feedback
    - Request changes or approve
    - Start messages with [REVIEWER]
    - Say TERMINATE when code is approved"""
)

user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config=False
)

# Setup group chat for A2A communication
groupchat = autogen.GroupChat(
    agents=[user_proxy, planner, developer, reviewer],
    messages=[],
    max_round=15,
    speaker_selection_method="auto",
    allow_repeat_speaker=False
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

# Start A2A workflow
task = """
Design and implement a simple user authentication function in Python.
The Planner should create the plan, the Developer should implement it,
and the Reviewer should review and approve the implementation.
"""

user_proxy.initiate_chat(
    manager,
    message=task
)

print("\n=== A2A Communication Summary ===")
print(f"Total messages: {len(groupchat.messages)}")
print("\nConversation flow:")
for i, msg in enumerate(groupchat.messages, 1):
    sender = msg.get("name", "Unknown")
    content_preview = msg.get("content", "")[:100]
    print(f"{i}. {sender}: {content_preview}...")
```

## Best Practices

1. **Agent Design**
   - Define clear roles and system messages
   - Set appropriate termination conditions
   - Use descriptive agent names

2. **Conversation Management**
   - Monitor max_consecutive_auto_reply to prevent loops
   - Implement proper termination logic
   - Handle edge cases gracefully

3. **Code Execution**
   - Use Docker for isolation when possible
   - Set reasonable timeouts
   - Validate code before execution

4. **Function Calling**
   - Write clear function descriptions
   - Use type annotations
   - Handle errors in functions

5. **Human-in-the-Loop**
   - Use appropriate human_input_mode
   - Provide clear prompts for human input
   - Allow override capabilities

6. **Cost Management**
   - Set budget limits in llm_config
   - Use caching when possible
   - Monitor token usage

## Performance Considerations

1. **Model Selection**: Choose appropriate models for each agent
2. **Caching**: Enable caching for repeated queries
3. **Parallel Execution**: Use concurrent agents when possible
4. **Message History**: Manage conversation history length
5. **Resource Limits**: Set timeouts and retry limits

## Common Patterns

1. **Two-Agent Pattern**: Simple user-assistant interaction
2. **Group Chat**: Multi-agent collaboration
3. **Sequential Workflow**: Step-by-step processing
4. **Hierarchical**: Manager coordinating workers
5. **Human-in-Loop**: Human oversight and intervention
6. **RAG Pattern**: Retrieval-augmented generation

## Advanced Features

### 1. Custom Speaker Selection

```python
def custom_speaker_selection(last_speaker, groupchat):
    """Custom logic to select next speaker"""
    messages = groupchat.messages

    if last_speaker.name == "Planner":
        return "Developer"
    elif last_speaker.name == "Developer":
        return "Reviewer"
    else:
        return "Planner"

# Use in group chat
groupchat = autogen.GroupChat(
    agents=agents,
    messages=[],
    max_round=20,
    speaker_selection_method=custom_speaker_selection
)
```

### 2. State Persistence

```python
# Save conversation history
import json

def save_conversation(groupchat, filename="conversation.json"):
    """Save conversation to file"""
    with open(filename, 'w') as f:
        json.dump(groupchat.messages, f, indent=2)

# Load conversation history
def load_conversation(filename="conversation.json"):
    """Load conversation from file"""
    with open(filename, 'r') as f:
        return json.load(f)
```

### 3. Dynamic Agent Creation

```python
def create_specialist_agent(specialty: str, config_list):
    """Dynamically create specialist agents"""
    return autogen.AssistantAgent(
        name=f"{specialty}_specialist",
        llm_config={"config_list": config_list},
        system_message=f"You are a {specialty} specialist."
    )

# Create agents on demand
agents = [
    create_specialist_agent("database", config_list),
    create_specialist_agent("frontend", config_list),
    create_specialist_agent("backend", config_list)
]
```

## Resources

- GitHub: https://github.com/microsoft/autogen
- Documentation: https://microsoft.github.io/autogen/
- Examples: https://github.com/microsoft/autogen/tree/main/notebook
- Research Paper: https://arxiv.org/abs/2308.08155
- Blog: https://www.microsoft.com/en-us/research/project/autogen/
