# CrewAI Deep Dive

## Overview
CrewAI is a framework for orchestrating role-playing, autonomous AI agents. It enables agents to work together collaboratively on complex tasks by defining roles, goals, and backstories. CrewAI emphasizes human-like collaboration patterns and delegation among agents.

## System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    CrewAI Application                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │    Crew      │◄─────┤    Agents    │◄─────┤   Tasks   │ │
│  │ (Orchestrator)│      │  (Workers)   │      │  (Work)   │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│         │                     │                     │        │
│         │                     │                     │        │
│  ┌──────▼─────────────────────▼─────────────────────▼─────┐ │
│  │              Process Manager                             │ │
│  │     (Sequential / Hierarchical / Consensus)              │ │
│  └─────────────────────────────────────────────────────────┘ │
│         │                     │                     │        │
│  ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐ │
│  │   Tools     │      │   Memory    │      │ Delegation  │ │
│  └─────────────┘      └─────────────┘      └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Crew**: The orchestrator that manages agents and tasks
2. **Agent**: Individual AI worker with role, goal, and backstory
3. **Task**: Unit of work with description and expected output
4. **Process**: Execution strategy (Sequential, Hierarchical, Consensus)
5. **Tools**: Functions agents can use to accomplish tasks
6. **Memory**: Short-term and long-term memory systems
7. **Delegation**: Agent-to-agent task delegation mechanism

## High-Level System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                         User Application                           │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                       CrewAI Framework Layer                        │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │    Crew      │  │   Process    │  │   Manager    │             │
│  │   Builder    │──┤   Engine     │──┤   System     │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│         │                  │                  │                     │
│  ┌──────▼──────────────────▼──────────────────▼─────────┐          │
│  │             Agent Execution Layer                     │          │
│  │  • Role Management  • Task Assignment  • Delegation   │          │
│  └───────────────────────────────────────────────────────┘          │
│         │                  │                  │                     │
│  ┌──────▼──────┐    ┌──────▼──────┐    ┌─────▼──────┐             │
│  │   Memory    │    │    Tools    │    │Collaboration│             │
│  │   System    │    │   Registry  │    │   Manager  │             │
│  └─────────────┘    └─────────────┘    └────────────┘             │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                         LLM Layer                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   OpenAI     │  │   Anthropic  │  │   Local LLMs │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└────────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│              External Services (APIs, Databases, etc.)              │
└────────────────────────────────────────────────────────────────────┘
```

## End-to-End Flow

### Execution Flow

```
1. Define Crew
   │
   ├─► Create Agents (with roles, goals, backstories)
   │
   ├─► Create Tasks (with descriptions, expected outputs)
   │
   ├─► Assign Tasks to Agents
   │
   └─► Set Process Type (Sequential/Hierarchical/Consensus)
       │
2. Kickoff Execution
   │
   ├─► Process Manager Initializes
   │
   ├─► Distribute Tasks Based on Process
   │
   └─► For Each Task:
       │
       ├─► Agent Receives Task
       │
       ├─► Agent Plans Approach
       │
       ├─► Agent Uses Tools (if needed)
       │
       ├─► Agent Delegates (if needed)
       │
       ├─► Agent Produces Output
       │
       └─► Move to Next Task
           │
3. Aggregate Results
   │
   └─► Return Final Output
```

### Detailed Execution Steps

1. **Initialization Phase**
   - Define agents with personas
   - Create tasks with acceptance criteria
   - Link agents to tasks
   - Configure process type

2. **Planning Phase**
   - Manager agent (if hierarchical) creates plan
   - Tasks are ordered by dependencies
   - Resource allocation determined

3. **Execution Phase**
   - Tasks executed per process strategy
   - Agents collaborate via delegation
   - Tools invoked as needed
   - Memory updated continuously

4. **Completion Phase**
   - Outputs validated against criteria
   - Results aggregated
   - Final report generated

## Examples

### 1. Simple Agent

A basic single-agent crew for content generation.

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4")

# Create agent
writer_agent = Agent(
    role="Content Writer",
    goal="Write engaging and informative content",
    backstory="""You are an experienced content writer with a talent for
    creating clear, engaging articles. You understand SEO best practices
    and know how to write for different audiences.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Create task
writing_task = Task(
    description="""Write a 300-word article about the benefits of
    artificial intelligence in healthcare. Include specific examples
    and maintain a professional tone.""",
    expected_output="A well-structured 300-word article with introduction, body, and conclusion",
    agent=writer_agent
)

# Create crew
crew = Crew(
    agents=[writer_agent],
    tasks=[writing_task],
    process=Process.sequential,
    verbose=True
)

# Execute
result = crew.kickoff()
print(result)
```

### 2. Complex Agent with Tools

An agent equipped with custom tools for research and analysis.

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_openai import ChatOpenAI
import requests

# Define custom tools
@tool("Search Tool")
def search_web(query: str) -> str:
    """Search the web for information about a topic."""
    # Simulated search
    return f"Search results for: {query}\n- Result 1: AI is transforming healthcare\n- Result 2: Benefits include diagnosis and treatment"

@tool("Analysis Tool")
def analyze_data(data: str) -> str:
    """Analyze text data and extract key insights."""
    # Simulated analysis
    return f"Analysis of data:\n- Key theme: Technology advancement\n- Sentiment: Positive\n- Main topics: AI, Healthcare, Innovation"

@tool("Calculator Tool")
def calculate(expression: str) -> str:
    """Perform mathematical calculations."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create researcher agent with tools
researcher_agent = Agent(
    role="Research Analyst",
    goal="Conduct thorough research and provide data-driven insights",
    backstory="""You are a meticulous research analyst with expertise in
    gathering, analyzing, and synthesizing information from multiple sources.
    You excel at finding patterns and drawing meaningful conclusions.""",
    tools=[search_web, analyze_data, calculate],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Create research task
research_task = Task(
    description="""Research the impact of AI in healthcare.
    Use the search tool to find information, analyze the data,
    and calculate any relevant statistics. Provide a comprehensive
    summary with key findings.""",
    expected_output="""A detailed research report including:
    1. Key findings from search
    2. Data analysis results
    3. Statistical insights
    4. Conclusions and recommendations""",
    agent=researcher_agent
)

# Create crew
crew = Crew(
    agents=[researcher_agent],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)

# Execute
result = crew.kickoff()
print("\n=== Research Report ===")
print(result)
```

### 3. Multi-Agent System

Multiple specialized agents working together on a complex project.

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Create specialized agents
researcher = Agent(
    role="Senior Researcher",
    goal="Discover groundbreaking insights and trends",
    backstory="""You are a world-class researcher with a PhD in your field.
    You have access to vast knowledge and can synthesize complex information
    into actionable insights.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze data and provide statistical insights",
    backstory="""You are an expert data analyst with strong statistical
    background. You can identify patterns, trends, and anomalies in data,
    and present findings clearly.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

writer = Agent(
    role="Technical Writer",
    goal="Create clear, engaging technical documentation",
    backstory="""You are a skilled technical writer who can translate
    complex technical concepts into accessible content. You have a gift
    for making difficult topics easy to understand.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Ensure highest quality standards in all outputs",
    backstory="""You are a meticulous reviewer with an eye for detail.
    You ensure accuracy, clarity, and consistency in all work products.
    You provide constructive feedback for improvements.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Create tasks
research_task = Task(
    description="""Research the current state of quantum computing.
    Focus on recent breakthroughs, key players, and future trends.
    Gather comprehensive information from multiple perspectives.""",
    expected_output="Detailed research findings on quantum computing with sources and key insights",
    agent=researcher
)

analysis_task = Task(
    description="""Analyze the research findings on quantum computing.
    Identify key trends, growth patterns, and potential impact areas.
    Provide statistical context where applicable.""",
    expected_output="Analytical report with trends, patterns, and statistical insights",
    agent=analyst,
    context=[research_task]  # Depends on research task
)

writing_task = Task(
    description="""Using the research and analysis, write a comprehensive
    article about quantum computing. Make it accessible to a technical
    audience while maintaining accuracy. Include an executive summary.""",
    expected_output="Well-structured article (800-1000 words) with executive summary",
    agent=writer,
    context=[research_task, analysis_task]  # Depends on both
)

review_task = Task(
    description="""Review the article for accuracy, clarity, and quality.
    Check for technical accuracy, readability, and completeness.
    Provide a quality assessment and final recommendations.""",
    expected_output="Quality review report with approval or recommendations for improvements",
    agent=reviewer,
    context=[writing_task]  # Depends on writing task
)

# Create crew with sequential process
crew = Crew(
    agents=[researcher, analyst, writer, reviewer],
    tasks=[research_task, analysis_task, writing_task, review_task],
    process=Process.sequential,
    verbose=True
)

# Execute
result = crew.kickoff()
print("\n=== Final Output ===")
print(result)
```

### 4. Hierarchical Process (Manager Agent)

A crew with a manager agent coordinating specialized workers.

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4")

# Create worker agents
planner = Agent(
    role="Project Planner",
    goal="Create detailed project plans and timelines",
    backstory="""You are an experienced project planner who excels at
    breaking down complex projects into manageable tasks and realistic
    timelines.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

developer = Agent(
    role="Software Developer",
    goal="Implement technical solutions efficiently",
    backstory="""You are a senior software developer with expertise in
    multiple programming languages and frameworks. You write clean,
    maintainable code.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

tester = Agent(
    role="QA Tester",
    goal="Ensure software quality through comprehensive testing",
    backstory="""You are a detail-oriented QA engineer who creates
    thorough test plans and finds edge cases that others miss.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Manager agent (automatically created in hierarchical process)
manager = Agent(
    role="Project Manager",
    goal="Coordinate team efforts and ensure project success",
    backstory="""You are an experienced project manager who excels at
    coordinating teams, managing resources, and ensuring timely delivery
    of high-quality products.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

# Create tasks (manager will delegate)
project_task = Task(
    description="""Develop a user authentication system with the following requirements:
    1. User registration and login
    2. Password hashing and security
    3. Session management
    4. Password reset functionality

    Coordinate planning, development, and testing phases.""",
    expected_output="""Complete authentication system including:
    - Project plan with timeline
    - Implementation details
    - Test results and quality report""",
    agent=manager  # Manager will delegate to others
)

# Create hierarchical crew
crew = Crew(
    agents=[manager, planner, developer, tester],
    tasks=[project_task],
    process=Process.hierarchical,  # Manager coordinates
    manager_llm=llm,
    verbose=True
)

# Execute
result = crew.kickoff()
print("\n=== Project Completion Report ===")
print(result)
```

### 5. Agentic RAG (RAG with Agents)

Combining retrieval-augmented generation with CrewAI agents.

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Setup vector store
documents = [
    Document(page_content="Artificial Intelligence is transforming healthcare through improved diagnostics.", metadata={"source": "article1"}),
    Document(page_content="Machine learning algorithms can detect diseases earlier than traditional methods.", metadata={"source": "article2"}),
    Document(page_content="AI-powered robotic surgery offers greater precision and faster recovery times.", metadata={"source": "article3"}),
    Document(page_content="Natural language processing helps analyze patient records efficiently.", metadata={"source": "article4"}),
]

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

# Create RAG tools
@tool("Retrieve Documents")
def retrieve_documents(query: str) -> str:
    """Retrieve relevant documents from the knowledge base."""
    docs = vectorstore.similarity_search(query, k=3)
    results = "\n\n".join([
        f"Document {i+1} (from {doc.metadata['source']}):\n{doc.page_content}"
        for i, doc in enumerate(docs)
    ])
    return results

@tool("Grade Document Relevance")
def grade_relevance(query: str, document: str) -> str:
    """Grade if a document is relevant to the query."""
    # Simplified grading logic
    query_lower = query.lower()
    doc_lower = document.lower()

    # Check for keyword overlap
    query_words = set(query_lower.split())
    doc_words = set(doc_lower.split())
    overlap = len(query_words.intersection(doc_words))

    if overlap >= 2:
        return "RELEVANT"
    else:
        return "NOT_RELEVANT"

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create RAG agents
retriever_agent = Agent(
    role="Document Retriever",
    goal="Find the most relevant documents for user queries",
    backstory="""You are an expert at searching through document collections
    and finding the most relevant information. You understand semantic
    similarity and can identify key documents quickly.""",
    tools=[retrieve_documents],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

grader_agent = Agent(
    role="Relevance Grader",
    goal="Assess the relevance of retrieved documents",
    backstory="""You are a critical evaluator who determines whether
    documents are truly relevant to a query. You have high standards
    and only approve documents that directly address the question.""",
    tools=[grade_relevance],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

answer_agent = Agent(
    role="Answer Synthesizer",
    goal="Generate accurate answers based on retrieved documents",
    backstory="""You are an expert at synthesizing information from
    multiple sources into coherent, accurate answers. You cite sources
    and acknowledge when information is not available.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Create RAG tasks
query = "How is AI being used in healthcare?"

retrieval_task = Task(
    description=f"""Retrieve documents relevant to this query: '{query}'
    Use the retrieve_documents tool to find the most relevant information.""",
    expected_output="List of relevant documents with their content",
    agent=retriever_agent
)

grading_task = Task(
    description=f"""Grade the relevance of retrieved documents for the query: '{query}'
    Use the grade_relevance tool to assess each document.
    Keep only RELEVANT documents.""",
    expected_output="Assessment of document relevance with reasoning",
    agent=grader_agent,
    context=[retrieval_task]
)

answer_task = Task(
    description=f"""Using the relevant documents, answer this query: '{query}'
    Synthesize the information into a comprehensive answer.
    Cite specific sources where appropriate.
    If information is insufficient, acknowledge it.""",
    expected_output="A well-structured answer with source citations",
    agent=answer_agent,
    context=[retrieval_task, grading_task]
)

# Create RAG crew
rag_crew = Crew(
    agents=[retriever_agent, grader_agent, answer_agent],
    tasks=[retrieval_task, grading_task, answer_task],
    process=Process.sequential,
    verbose=True
)

# Execute
result = rag_crew.kickoff()
print("\n=== Agentic RAG Answer ===")
print(result)
```

### 6. MCP with Agents (Model Context Protocol)

Integrating MCP servers with CrewAI agents for enhanced capabilities.

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_openai import ChatOpenAI
import json

# Simulated MCP Server
class MCPFileSystem:
    """MCP Server for file system operations"""

    @staticmethod
    def list_directory(path: str) -> dict:
        return {
            "success": True,
            "files": ["document1.txt", "document2.pdf", "data.csv"],
            "path": path
        }

    @staticmethod
    def read_file(filepath: str) -> dict:
        return {
            "success": True,
            "content": f"Content of {filepath}: This is sample file content.",
            "size": 1024
        }

    @staticmethod
    def create_file(filepath: str, content: str) -> dict:
        return {
            "success": True,
            "message": f"File created: {filepath}",
            "path": filepath
        }

# Create MCP tools
@tool("MCP List Directory")
def mcp_list_dir(path: str) -> str:
    """List files in a directory via MCP server."""
    result = MCPFileSystem.list_directory(path)
    if result["success"]:
        files = "\n".join([f"  - {f}" for f in result["files"]])
        return f"Files in {path}:\n{files}"
    return "Error listing directory"

@tool("MCP Read File")
def mcp_read_file(filepath: str) -> str:
    """Read file content via MCP server."""
    result = MCPFileSystem.read_file(filepath)
    if result["success"]:
        return f"Content ({result['size']} bytes):\n{result['content']}"
    return "Error reading file"

@tool("MCP Create File")
def mcp_create_file(filepath: str, content: str) -> str:
    """Create a new file via MCP server."""
    result = MCPFileSystem.create_file(filepath, content)
    if result["success"]:
        return result["message"]
    return "Error creating file"

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create MCP-enabled agents
file_manager = Agent(
    role="File System Manager",
    goal="Manage files and directories efficiently using MCP",
    backstory="""You are an expert system administrator who manages
    files and directories. You use the Model Context Protocol to
    interact with the file system safely and efficiently.""",
    tools=[mcp_list_dir, mcp_read_file, mcp_create_file],
    verbose=True,
    allow_delegation=True,
    llm=llm
)

content_processor = Agent(
    role="Content Processor",
    goal="Process and analyze file content",
    backstory="""You are a content processing specialist who analyzes
    documents and extracts valuable information. You work with the
    file manager to access and process content.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

report_generator = Agent(
    role="Report Generator",
    goal="Generate comprehensive reports from processed data",
    backstory="""You are a report generation expert who creates
    well-structured, informative reports. You compile information
    from various sources into cohesive documents.""",
    tools=[mcp_create_file],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Create tasks
list_task = Task(
    description="""Use MCP to list all files in the /documents directory.
    Provide a clear summary of what files are available.""",
    expected_output="List of files in /documents directory",
    agent=file_manager
)

process_task = Task(
    description="""Based on the file list, identify which files should be
    processed. Analyze the content and extract key information.""",
    expected_output="Summary of file contents and key findings",
    agent=content_processor,
    context=[list_task]
)

report_task = Task(
    description="""Create a comprehensive report of all processed files.
    Use MCP to save the report as 'summary_report.txt'.
    Include file names, key findings, and recommendations.""",
    expected_output="Completion confirmation of report creation",
    agent=report_generator,
    context=[list_task, process_task]
)

# Create MCP crew
mcp_crew = Crew(
    agents=[file_manager, content_processor, report_generator],
    tasks=[list_task, process_task, report_task],
    process=Process.sequential,
    verbose=True
)

# Execute
result = mcp_crew.kickoff()
print("\n=== MCP Integration Result ===")
print(result)
```

### 7. Agent-to-Agent (A2A) Communication

Direct agent-to-agent communication for complex problem solving.

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Create agents that communicate with each other
architect = Agent(
    role="Solution Architect",
    goal="Design system architecture and communicate requirements to developers",
    backstory="""You are a senior solution architect with deep expertise in
    system design. You excel at breaking down complex systems and communicating
    technical requirements clearly. You actively delegate and coordinate with
    other team members.""",
    verbose=True,
    allow_delegation=True,  # Can delegate to other agents
    llm=llm
)

backend_dev = Agent(
    role="Backend Developer",
    goal="Implement backend services and APIs",
    backstory="""You are an experienced backend developer. You communicate
    with the architect to clarify requirements and with the frontend developer
    to define API contracts. You ask questions when requirements are unclear.""",
    verbose=True,
    allow_delegation=True,  # Can communicate with other agents
    llm=llm
)

frontend_dev = Agent(
    role="Frontend Developer",
    goal="Build user interfaces and integrate with backend",
    backstory="""You are a skilled frontend developer. You coordinate with
    the backend developer to understand API specifications and with the
    architect to align on user experience decisions.""",
    verbose=True,
    allow_delegation=True,  # Can communicate with other agents
    llm=llm
)

devops = Agent(
    role="DevOps Engineer",
    goal="Setup infrastructure and deployment pipelines",
    backstory="""You are a DevOps expert who ensures smooth deployment and
    operations. You work with all team members to understand infrastructure
    needs and provide deployment solutions.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Create interconnected tasks
architecture_task = Task(
    description="""Design the architecture for an e-commerce platform with:
    1. User authentication
    2. Product catalog
    3. Shopping cart
    4. Payment processing

    Create a high-level design and communicate specific requirements to
    backend and frontend developers.""",
    expected_output="System architecture document with component specifications",
    agent=architect
)

backend_task = Task(
    description="""Based on the architecture design, implement the backend:
    1. Review architecture decisions with the architect
    2. Define API endpoints
    3. Communicate API contracts with frontend developer
    4. Specify database requirements
    5. Coordinate with DevOps on infrastructure needs

    Ensure clear communication about technical decisions.""",
    expected_output="Backend implementation plan with API specifications",
    agent=backend_dev,
    context=[architecture_task]
)

frontend_task = Task(
    description="""Develop the frontend based on backend APIs:
    1. Coordinate with backend developer on API integration
    2. Discuss with architect about UX decisions
    3. Identify any architecture adjustments needed
    4. Specify deployment requirements to DevOps

    Maintain open communication about technical challenges.""",
    expected_output="Frontend implementation plan with integration details",
    agent=frontend_dev,
    context=[architecture_task, backend_task]
)

devops_task = Task(
    description="""Setup deployment infrastructure:
    1. Review requirements from all developers
    2. Design CI/CD pipeline
    3. Configure hosting and databases
    4. Provide deployment documentation to team

    Ensure all team needs are addressed.""",
    expected_output="Infrastructure and deployment plan",
    agent=devops,
    context=[architecture_task, backend_task, frontend_task]
)

# Create A2A crew with hierarchical process for coordination
a2a_crew = Crew(
    agents=[architect, backend_dev, frontend_dev, devops],
    tasks=[architecture_task, backend_task, frontend_task, devops_task],
    process=Process.sequential,  # Or hierarchical for more delegation
    verbose=True
)

# Execute
result = a2a_crew.kickoff()
print("\n=== A2A Collaboration Result ===")
print(result)
```

## Best Practices

1. **Agent Design**
   - Write detailed backstories for better role-playing
   - Set clear, specific goals
   - Use appropriate temperature settings
   - Enable delegation only when needed

2. **Task Definition**
   - Write clear, detailed descriptions
   - Specify expected outputs
   - Use task context for dependencies
   - Break complex tasks into smaller ones

3. **Tool Integration**
   - Create focused, single-purpose tools
   - Provide clear tool descriptions
   - Handle errors gracefully
   - Test tools independently

4. **Process Selection**
   - Sequential: Simple, linear workflows
   - Hierarchical: Complex projects needing coordination
   - Consensus: When multiple perspectives are valuable

5. **Memory Management**
   - Enable memory for context retention
   - Use short-term memory for task execution
   - Implement long-term memory for learning

6. **Error Handling**
   - Set verbose=True during development
   - Implement tool error handling
   - Monitor agent interactions
   - Log decisions and outputs

## Performance Considerations

1. **LLM Selection**: Choose appropriate models for each agent
2. **Tool Optimization**: Keep tools fast and efficient
3. **Memory Usage**: Monitor memory consumption
4. **Parallel Execution**: Use concurrent tasks when possible
5. **Cost Management**: Track API usage and costs

## Common Patterns

1. **Research-Analysis-Writing**: Information pipeline
2. **Manager-Worker**: Hierarchical delegation
3. **Expert Panel**: Multiple specialists collaborating
4. **Review-Feedback Loop**: Quality assurance
5. **Specialist Consultation**: Agent-to-agent advice

### 8. Self-Reflective RAG with Corrective Mechanism

Advanced RAG with self-reflection and correction capabilities.

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import Literal

# Setup knowledge base
documents = [
    Document(page_content="Python is a high-level programming language known for simplicity.", metadata={"source": "python_intro"}),
    Document(page_content="Python supports multiple programming paradigms including OOP.", metadata={"source": "python_paradigms"}),
    Document(page_content="JavaScript is primarily used for web development.", metadata={"source": "javascript_intro"}),
    Document(page_content="TypeScript is a typed superset of JavaScript.", metadata={"source": "typescript_intro"}),
]

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

# RAG Tools
@tool("Vector Search")
def vector_search(query: str) -> str:
    """Search the vector database for relevant documents."""
    docs = vectorstore.similarity_search(query, k=3)
    results = []
    for i, doc in enumerate(docs):
        results.append(f"[{i+1}] {doc.page_content} (source: {doc.metadata['source']})")
    return "\n".join(results)

@tool("Grade Document")
def grade_document(question: str, document: str) -> str:
    """Grade if document is relevant to the question."""
    # Simple keyword-based grading
    question_words = set(question.lower().split())
    doc_words = set(document.lower().split())
    overlap = len(question_words.intersection(doc_words))

    if overlap >= 2:
        return "RELEVANT"
    return "NOT_RELEVANT"

@tool("Web Search Fallback")
def web_search(query: str) -> str:
    """Fallback web search when documents are not relevant."""
    # Simulated web search
    return f"Web search results for '{query}':\n- Python is widely used in data science and AI\n- Python has excellent library support"

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create specialized RAG agents
retriever = Agent(
    role="Document Retriever",
    goal="Retrieve the most relevant documents from the vector database",
    backstory="""You are an expert at semantic search and information retrieval.
    You understand how to formulate queries and find relevant documents.""",
    tools=[vector_search],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

grader = Agent(
    role="Relevance Evaluator",
    goal="Critically evaluate document relevance to questions",
    backstory="""You are a strict evaluator who ensures only truly relevant
    documents are used. You prevent hallucinations by filtering irrelevant content.""",
    tools=[grade_document],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

web_searcher = Agent(
    role="Web Search Specialist",
    goal="Find information from the web when local documents are insufficient",
    backstory="""You are a web search expert who can find additional information
    when the knowledge base lacks relevant documents.""",
    tools=[web_search],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

answer_generator = Agent(
    role="Answer Generator",
    goal="Generate accurate, well-sourced answers",
    backstory="""You are an expert at synthesizing information into clear answers.
    You always cite sources and acknowledge limitations.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Create CRAG tasks
user_question = "What are the main features of Python programming language?"

retrieve_task = Task(
    description=f"""Retrieve documents for: '{user_question}'
    Use vector search to find the most relevant documents.""",
    expected_output="Retrieved documents with content and sources",
    agent=retriever
)

grade_task = Task(
    description=f"""Grade each retrieved document for relevance to: '{user_question}'
    Mark each as RELEVANT or NOT_RELEVANT.
    If most documents are NOT_RELEVANT, trigger web search.""",
    expected_output="Document relevance grades with decision on web search need",
    agent=grader,
    context=[retrieve_task]
)

search_task = Task(
    description=f"""If documents were graded as NOT_RELEVANT, perform web search for: '{user_question}'
    Otherwise, skip this step.""",
    expected_output="Web search results or indication that search was skipped",
    agent=web_searcher,
    context=[grade_task]
)

generate_task = Task(
    description=f"""Generate a comprehensive answer to: '{user_question}'
    Use RELEVANT documents and web search results if available.
    Cite all sources used. If information is insufficient, state that clearly.""",
    expected_output="Complete answer with source citations",
    agent=answer_generator,
    context=[retrieve_task, grade_task, search_task]
)

# Create CRAG crew
crag_crew = Crew(
    agents=[retriever, grader, web_searcher, answer_generator],
    tasks=[retrieve_task, grade_task, search_task, generate_task],
    process=Process.sequential,
    verbose=True
)

# Execute
result = crag_crew.kickoff()
print("\n=== Corrective RAG Answer ===")
print(result)
```

### 9. Multi-MCP Server Orchestration

Coordinating multiple MCP servers for complex workflows.

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_openai import ChatOpenAI
from typing import Dict, List
import json

# Simulated MCP Servers
class DatabaseMCP:
    """MCP Server for database operations"""

    @staticmethod
    def query(sql: str) -> dict:
        return {
            "success": True,
            "rows": [
                {"id": 1, "name": "Product A", "price": 29.99},
                {"id": 2, "name": "Product B", "price": 49.99}
            ],
            "count": 2
        }

    @staticmethod
    def insert(table: str, data: dict) -> dict:
        return {
            "success": True,
            "id": 3,
            "message": f"Inserted into {table}"
        }

class EmailMCP:
    """MCP Server for email operations"""

    @staticmethod
    def send_email(to: str, subject: str, body: str) -> dict:
        return {
            "success": True,
            "message": f"Email sent to {to}",
            "message_id": "msg_12345"
        }

    @staticmethod
    def list_emails(folder: str = "inbox") -> dict:
        return {
            "success": True,
            "emails": [
                {"id": 1, "from": "user@example.com", "subject": "Test"},
                {"id": 2, "from": "admin@example.com", "subject": "Report"}
            ]
        }

class AnalyticsMCP:
    """MCP Server for analytics operations"""

    @staticmethod
    def track_event(event_name: str, properties: dict) -> dict:
        return {
            "success": True,
            "event_id": "evt_67890",
            "tracked": event_name
        }

    @staticmethod
    def get_metrics(metric_name: str) -> dict:
        return {
            "success": True,
            "metric": metric_name,
            "value": 1250,
            "change": "+15%"
        }

# Create MCP tools
@tool("Database Query")
def db_query(sql: str) -> str:
    """Query database via MCP."""
    result = DatabaseMCP.query(sql)
    if result["success"]:
        return json.dumps(result["rows"], indent=2)
    return "Query failed"

@tool("Database Insert")
def db_insert(table: str, data: str) -> str:
    """Insert data into database via MCP."""
    data_dict = json.loads(data)
    result = DatabaseMCP.insert(table, data_dict)
    return json.dumps(result)

@tool("Send Email")
def send_email(to: str, subject: str, body: str) -> str:
    """Send email via MCP."""
    result = EmailMCP.send_email(to, subject, body)
    if result["success"]:
        return f"Email sent: {result['message_id']}"
    return "Email failed"

@tool("Track Analytics Event")
def track_event(event_name: str, properties: str) -> str:
    """Track analytics event via MCP."""
    props = json.loads(properties)
    result = AnalyticsMCP.track_event(event_name, props)
    return f"Tracked: {result['event_id']}"

@tool("Get Analytics")
def get_analytics(metric: str) -> str:
    """Get analytics metrics via MCP."""
    result = AnalyticsMCP.get_metrics(metric)
    return f"{result['metric']}: {result['value']} ({result['change']})"

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create MCP-coordinating agents
database_agent = Agent(
    role="Database Administrator",
    goal="Manage database operations efficiently",
    backstory="""You are a database expert who handles all data storage
    and retrieval operations through the database MCP server.""",
    tools=[db_query, db_insert],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

email_agent = Agent(
    role="Email Manager",
    goal="Handle all email communications",
    backstory="""You are an email management specialist who sends
    notifications and manages email communications via MCP.""",
    tools=[send_email],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

analytics_agent = Agent(
    role="Analytics Specialist",
    goal="Track events and monitor metrics",
    backstory="""You are an analytics expert who tracks important events
    and monitors system metrics through the analytics MCP server.""",
    tools=[track_event, get_analytics],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

coordinator = Agent(
    role="Workflow Coordinator",
    goal="Orchestrate complex workflows across multiple MCP servers",
    backstory="""You are a workflow orchestration expert who coordinates
    activities across database, email, and analytics systems.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

# Create orchestrated tasks
fetch_data_task = Task(
    description="""Query the database for all products with price > 25.
    Use SQL: SELECT * FROM products WHERE price > 25""",
    expected_output="List of products matching criteria",
    agent=database_agent
)

track_task = Task(
    description="""Track an analytics event for 'product_query_completed'
    with properties: {\"query_type\": \"price_filter\", \"threshold\": 25}""",
    expected_output="Confirmation of event tracking",
    agent=analytics_agent,
    context=[fetch_data_task]
)

email_task = Task(
    description="""Send an email to admin@company.com with subject
    'Product Query Report' summarizing the query results.""",
    expected_output="Email sent confirmation",
    agent=email_agent,
    context=[fetch_data_task]
)

metrics_task = Task(
    description="""Retrieve the 'product_queries' analytics metric
    to monitor query trends.""",
    expected_output="Analytics metrics report",
    agent=analytics_agent,
    context=[track_task]
)

# Create multi-MCP crew
multi_mcp_crew = Crew(
    agents=[coordinator, database_agent, email_agent, analytics_agent],
    tasks=[fetch_data_task, track_task, email_task, metrics_task],
    process=Process.sequential,
    verbose=True
)

# Execute
result = multi_mcp_crew.kickoff()
print("\n=== Multi-MCP Orchestration Result ===")
print(result)
```

### 10. A2A Travel Planning System

Complex A2A system for collaborative travel planning.

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from typing import Dict, List
import json

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Create specialized travel agents
flight_specialist = Agent(
    role="Flight Booking Specialist",
    goal="Find and recommend optimal flight options",
    backstory="""You are an expert in flight bookings with access to airline
    schedules and pricing. You communicate with the hotel specialist to coordinate
    arrival times and with the budget manager for price constraints.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

hotel_specialist = Agent(
    role="Hotel Booking Specialist",
    goal="Find suitable accommodation options",
    backstory="""You are a hotel booking expert who finds the best accommodations.
    You coordinate with the flight specialist for check-in timing and with the
    activities planner for location preferences.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

activities_planner = Agent(
    role="Activities Coordinator",
    goal="Plan engaging activities and experiences",
    backstory="""You are an activities planning expert who designs itineraries.
    You work with the hotel specialist for proximity to attractions and with
    the budget manager to stay within spending limits.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

budget_manager = Agent(
    role="Budget Manager",
    goal="Ensure trip stays within budget constraints",
    backstory="""You are a financial planning expert who ensures the trip
    is affordable. You communicate with all other agents to optimize costs
    while maintaining quality.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

travel_coordinator = Agent(
    role="Travel Coordinator",
    goal="Orchestrate all aspects of trip planning",
    backstory="""You are the main coordinator who ensures all travel components
    work together seamlessly. You facilitate communication between all specialists
    and make final decisions.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

# Create A2A communication tasks
trip_requirements = {
    "destination": "Tokyo, Japan",
    "duration": "7 days",
    "travelers": 2,
    "budget": "$4000",
    "dates": "April 15-22, 2024"
}

coordinate_task = Task(
    description=f"""Coordinate a trip to {trip_requirements['destination']}:
    - Duration: {trip_requirements['duration']}
    - Travelers: {trip_requirements['travelers']}
    - Budget: {trip_requirements['budget']}
    - Dates: {trip_requirements['dates']}

    Facilitate communication between all specialists to create a cohesive plan.""",
    expected_output="Initial coordination plan with specialist assignments",
    agent=travel_coordinator
)

flight_task = Task(
    description=f"""Find flight options for {trip_requirements['travelers']} travelers
    to {trip_requirements['destination']} for {trip_requirements['dates']}.

    Communicate with:
    - Budget Manager: Confirm price constraints
    - Hotel Specialist: Coordinate arrival/departure times
    - Travel Coordinator: Report options and get approval""",
    expected_output="Flight recommendations with pricing and schedules",
    agent=flight_specialist,
    context=[coordinate_task]
)

hotel_task = Task(
    description=f"""Find hotel accommodations for {trip_requirements['duration']}
    in {trip_requirements['destination']}.

    Communicate with:
    - Flight Specialist: Align with arrival/departure times
    - Activities Planner: Ensure good location for planned activities
    - Budget Manager: Stay within allocated hotel budget
    - Travel Coordinator: Present options for approval""",
    expected_output="Hotel recommendations with pricing and locations",
    agent=hotel_specialist,
    context=[coordinate_task, flight_task]
)

activities_task = Task(
    description=f"""Plan activities and experiences for {trip_requirements['duration']}
    in {trip_requirements['destination']}.

    Communicate with:
    - Hotel Specialist: Consider proximity to accommodation
    - Budget Manager: Ensure activities fit budget
    - Travel Coordinator: Create daily itinerary

    Include mix of cultural experiences, dining, and sightseeing.""",
    expected_output="Daily activity itinerary with costs",
    agent=activities_planner,
    context=[coordinate_task, hotel_task]
)

budget_task = Task(
    description=f"""Review all proposed expenses against {trip_requirements['budget']}:

    Communicate with:
    - Flight Specialist: Negotiate or find alternative flights if needed
    - Hotel Specialist: Adjust accommodation level if necessary
    - Activities Planner: Prioritize activities within budget
    - Travel Coordinator: Provide final budget breakdown

    Ensure total cost doesn't exceed budget while maximizing value.""",
    expected_output="Complete budget breakdown with all expenses",
    agent=budget_manager,
    context=[flight_task, hotel_task, activities_task]
)

final_plan_task = Task(
    description="""Compile all specialist inputs into a comprehensive travel plan:

    - Finalize flight bookings based on budget approval
    - Confirm hotel reservations
    - Lock in activity schedule
    - Verify budget alignment
    - Create final itinerary with all details

    Ensure all agents are aligned on the final plan.""",
    expected_output="Complete travel itinerary with all bookings and budget",
    agent=travel_coordinator,
    context=[flight_task, hotel_task, activities_task, budget_task]
)

# Create A2A travel crew
travel_crew = Crew(
    agents=[travel_coordinator, flight_specialist, hotel_specialist,
            activities_planner, budget_manager],
    tasks=[coordinate_task, flight_task, hotel_task, activities_task,
           budget_task, final_plan_task],
    process=Process.sequential,  # Can also use hierarchical for more coordination
    verbose=True
)

# Execute
result = travel_crew.kickoff()
print("\n=== Travel Planning Result ===")
print(result)
```

## Advanced Patterns

### 1. Human-in-the-Loop

Integrating human feedback into agent workflows.

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

# Agent that produces initial output
draft_writer = Agent(
    role="Draft Writer",
    goal="Create initial content drafts",
    backstory="You create high-quality content drafts for human review.",
    verbose=True,
    llm=llm
)

# Agent that incorporates human feedback
editor = Agent(
    role="Editor",
    goal="Refine content based on feedback",
    backstory="You excel at incorporating feedback to improve content.",
    verbose=True,
    llm=llm
)

# Create tasks with human feedback points
draft_task = Task(
    description="Write a blog post about AI in healthcare (300 words)",
    expected_output="Initial draft blog post",
    agent=draft_writer
)

# Simulated human feedback
def get_human_feedback(draft: str) -> str:
    """Simulate human providing feedback"""
    return "Add more specific examples and make the tone more conversational."

review_task = Task(
    description="""Review the draft and incorporate this feedback:
    'Add more specific examples and make the tone more conversational.'

    Revise the content accordingly.""",
    expected_output="Revised blog post incorporating feedback",
    agent=editor,
    context=[draft_task]
)

# Create crew
hitl_crew = Crew(
    agents=[draft_writer, editor],
    tasks=[draft_task, review_task],
    process=Process.sequential,
    verbose=True
)

result = hitl_crew.kickoff()
print(result)
```

### 2. Dynamic Task Generation

Agents that create new tasks based on discoveries.

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

analyzer = Agent(
    role="Code Analyzer",
    goal="Analyze codebases and identify issues",
    backstory="You analyze code and identify potential problems or improvements.",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

fixer = Agent(
    role="Code Fixer",
    goal="Fix identified code issues",
    backstory="You fix code problems efficiently.",
    verbose=True,
    llm=llm
)

# Initial analysis task
analysis_task = Task(
    description="""Analyze this Python function and identify any issues:

    def calculate_total(prices):
        total = 0
        for price in prices:
            total += price
        return total

    Check for: error handling, type hints, documentation, edge cases.""",
    expected_output="List of identified issues with severity levels",
    agent=analyzer
)

# Dynamic fix task (created based on analysis)
fix_task = Task(
    description="""Based on the analysis, fix all identified issues.
    Provide the improved code with proper error handling, type hints, and documentation.""",
    expected_output="Refactored code addressing all issues",
    agent=fixer,
    context=[analysis_task]
)

# Create crew
dynamic_crew = Crew(
    agents=[analyzer, fixer],
    tasks=[analysis_task, fix_task],
    process=Process.sequential,
    verbose=True
)

result = dynamic_crew.kickoff()
print(result)
```

### 3. Consensus-Based Decision Making

Multiple agents voting on decisions.

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Create expert panel
security_expert = Agent(
    role="Security Expert",
    goal="Evaluate from security perspective",
    backstory="You are a cybersecurity expert who prioritizes system security.",
    verbose=True,
    llm=llm
)

performance_expert = Agent(
    role="Performance Expert",
    goal="Evaluate from performance perspective",
    backstory="You are a performance optimization expert.",
    verbose=True,
    llm=llm
)

cost_expert = Agent(
    role="Cost Expert",
    goal="Evaluate from cost perspective",
    backstory="You are a financial analyst who optimizes for cost-effectiveness.",
    verbose=True,
    llm=llm
)

decision_maker = Agent(
    role="Decision Synthesizer",
    goal="Synthesize expert opinions into final decision",
    backstory="You weigh different perspectives to make balanced decisions.",
    verbose=True,
    llm=llm
)

# Decision scenario
scenario = "Should we migrate our application to a microservices architecture?"

security_eval = Task(
    description=f"Evaluate this decision from a security perspective: {scenario}",
    expected_output="Security analysis with recommendation and concerns",
    agent=security_expert
)

performance_eval = Task(
    description=f"Evaluate this decision from a performance perspective: {scenario}",
    expected_output="Performance analysis with recommendation and concerns",
    agent=performance_expert
)

cost_eval = Task(
    description=f"Evaluate this decision from a cost perspective: {scenario}",
    expected_output="Cost analysis with recommendation and concerns",
    agent=cost_expert
)

final_decision = Task(
    description=f"""Synthesize all expert evaluations to make a final decision: {scenario}

    Consider all perspectives and provide:
    1. Final recommendation (Yes/No/Conditional)
    2. Key factors supporting the decision
    3. Risks and mitigation strategies
    4. Implementation considerations""",
    expected_output="Comprehensive decision with rationale",
    agent=decision_maker,
    context=[security_eval, performance_eval, cost_eval]
)

# Create consensus crew
consensus_crew = Crew(
    agents=[security_expert, performance_expert, cost_expert, decision_maker],
    tasks=[security_eval, performance_eval, cost_eval, final_decision],
    process=Process.sequential,
    verbose=True
)

result = consensus_crew.kickoff()
print(result)
```

## Production Considerations

### 1. Error Handling and Resilience

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    llm = ChatOpenAI(model="gpt-4", temperature=0, max_retries=3)

    agent = Agent(
        role="Resilient Agent",
        goal="Perform tasks with error handling",
        backstory="You handle errors gracefully and retry when appropriate.",
        verbose=True,
        llm=llm,
        max_iter=10  # Maximum iterations to prevent infinite loops
    )

    task = Task(
        description="Process data with error handling",
        expected_output="Processed results or error report",
        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    logger.info(f"Success: {result}")

except Exception as e:
    logger.error(f"Crew execution failed: {str(e)}")
    # Implement fallback logic or alerts
```

### 2. Monitoring and Observability

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.callbacks import OpenAICallbackHandler
import time

class MetricsCallback(OpenAICallbackHandler):
    """Custom callback for monitoring"""

    def __init__(self):
        super().__init__()
        self.start_time = None
        self.task_metrics = []

    def on_llm_start(self, *args, **kwargs):
        self.start_time = time.time()
        super().on_llm_start(*args, **kwargs)

    def on_llm_end(self, *args, **kwargs):
        duration = time.time() - self.start_time
        self.task_metrics.append({
            "duration": duration,
            "tokens": self.total_tokens,
            "cost": self.total_cost
        })
        print(f"LLM call: {duration:.2f}s, {self.total_tokens} tokens, ${self.total_cost:.4f}")
        super().on_llm_end(*args, **kwargs)

# Use callback for monitoring
callback = MetricsCallback()

llm = ChatOpenAI(
    model="gpt-4",
    callbacks=[callback],
    streaming=True
)

agent = Agent(
    role="Monitored Agent",
    goal="Perform tasks with full monitoring",
    backstory="Your actions are monitored for performance optimization.",
    verbose=True,
    llm=llm
)

task = Task(
    description="Analyze system performance metrics",
    expected_output="Performance analysis report",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()

# Print monitoring results
print("\n=== Metrics Summary ===")
for i, metrics in enumerate(callback.task_metrics):
    print(f"Call {i+1}: {metrics['duration']:.2f}s, {metrics['tokens']} tokens, ${metrics['cost']:.4f}")
```

### 3. Deployment Patterns

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from typing import Dict, Any
import os

class ProductionCrew:
    """Production-ready crew wrapper"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm = ChatOpenAI(
            model=config.get("model", "gpt-4"),
            temperature=config.get("temperature", 0),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.crew = None

    def build_crew(self):
        """Build the crew with configuration"""
        agents = self._create_agents()
        tasks = self._create_tasks(agents)

        self.crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process(self.config.get("process", "sequential")),
            verbose=self.config.get("verbose", False),
            max_rpm=self.config.get("max_rpm", 10)  # Rate limiting
        )

    def _create_agents(self):
        """Create agents from configuration"""
        return [
            Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                verbose=self.config.get("verbose", False),
                llm=self.llm
            )
            for agent_config in self.config.get("agents", [])
        ]

    def _create_tasks(self, agents):
        """Create tasks from configuration"""
        tasks = []
        task_configs = self.config.get("tasks", [])

        for i, task_config in enumerate(task_configs):
            task = Task(
                description=task_config["description"],
                expected_output=task_config["expected_output"],
                agent=agents[task_config.get("agent_index", i)]
            )
            tasks.append(task)

        return tasks

    def run(self) -> str:
        """Execute the crew"""
        if not self.crew:
            self.build_crew()

        return self.crew.kickoff()

# Production configuration
production_config = {
    "model": "gpt-4",
    "temperature": 0,
    "process": "sequential",
    "verbose": False,
    "max_rpm": 10,
    "agents": [
        {
            "role": "Analyst",
            "goal": "Analyze data",
            "backstory": "Expert analyst"
        }
    ],
    "tasks": [
        {
            "description": "Analyze user behavior",
            "expected_output": "Behavior analysis report",
            "agent_index": 0
        }
    ]
}

# Deploy
prod_crew = ProductionCrew(production_config)
result = prod_crew.run()
print(result)
```

### 4. Cost Optimization

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.callbacks import get_openai_callback

# Use cost tracking
with get_openai_callback() as cb:
    # Use cheaper model for simple tasks
    cheap_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    expensive_llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Simple agent with cheaper model
    researcher = Agent(
        role="Researcher",
        goal="Gather information",
        backstory="You research topics efficiently.",
        llm=cheap_llm,
        verbose=True
    )

    # Complex agent with expensive model
    analyzer = Agent(
        role="Analyst",
        goal="Perform deep analysis",
        backstory="You provide expert analysis.",
        llm=expensive_llm,
        verbose=True
    )

    research_task = Task(
        description="Research AI trends in 2024",
        expected_output="Research findings",
        agent=researcher
    )

    analysis_task = Task(
        description="Analyze research findings and provide insights",
        expected_output="Analysis report",
        agent=analyzer,
        context=[research_task]
    )

    crew = Crew(
        agents=[researcher, analyzer],
        tasks=[research_task, analysis_task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()

    # Print cost analysis
    print(f"\n=== Cost Analysis ===")
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost: ${cb.total_cost:.4f}")
```

### 5. Security Considerations

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from typing import Optional

class SecureCrewBuilder:
    """Secure crew builder with validation"""

    def __init__(self):
        # Use environment variables for sensitive data
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set")

        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model="gpt-4",
            temperature=0
        )

    def sanitize_input(self, user_input: str) -> str:
        """Sanitize user input to prevent injection"""
        # Remove potentially harmful content
        forbidden_patterns = ["<script>", "javascript:", "eval("]
        sanitized = user_input

        for pattern in forbidden_patterns:
            sanitized = sanitized.replace(pattern, "")

        return sanitized.strip()

    def create_secure_task(self, description: str, agent: Agent) -> Task:
        """Create task with sanitized input"""
        safe_description = self.sanitize_input(description)

        return Task(
            description=safe_description,
            expected_output="Processed output",
            agent=agent
        )

# Usage
builder = SecureCrewBuilder()

secure_agent = Agent(
    role="Secure Agent",
    goal="Process data securely",
    backstory="You process data with security in mind.",
    llm=builder.llm,
    verbose=True
)

user_input = "Analyze this data <script>alert('xss')</script>"
safe_task = builder.create_secure_task(user_input, secure_agent)

crew = Crew(
    agents=[secure_agent],
    tasks=[safe_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
print(result)
```

## Conclusion

CrewAI provides a powerful framework for building collaborative multi-agent systems with role-playing capabilities. Its key strengths include:

**Core Strengths:**
- Intuitive agent role-playing model with personas
- Flexible process types (Sequential, Hierarchical, Consensus)
- Built-in delegation and collaboration mechanisms
- Easy integration with LangChain tools and components
- Strong support for memory and context retention

**Best Use Cases:**
- Multi-agent collaboration scenarios
- Role-based task delegation systems
- Complex workflows requiring specialist agents
- Projects benefiting from hierarchical coordination
- Systems requiring consensus-based decisions

**When to Choose CrewAI:**
- Need clear role separation among agents
- Benefit from agent backstories and personas
- Require hierarchical task management
- Want built-in delegation capabilities
- Need human-like collaboration patterns

**Integration Capabilities:**
- Seamless LangChain tool integration
- MCP server support for extended capabilities
- A2A communication for agent coordination
- RAG integration for knowledge-based agents
- Custom tool development support

## Resources

- **GitHub**: https://github.com/joaomdmoura/crewAI
- **Documentation**: https://docs.crewai.com/
- **Examples**: https://github.com/joaomdmoura/crewAI-examples
- **Community**: https://discord.gg/X4JWnZnxPb
- **Tutorials**: https://docs.crewai.com/getting-started/
- **API Reference**: https://docs.crewai.com/core-concepts/

**Related Frameworks:**
- LangGraph: For graph-based agent orchestration
- LangChain: For general LLM application development
- AutoGen: For conversational multi-agent systems
- A2A Protocol: For standardized agent communication
