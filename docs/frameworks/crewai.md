# CrewAI - Role-Based Agent Orchestration

## Overview

**CrewAI** is a framework for orchestrating role-based AI agents to work together on complex tasks through sequential or hierarchical processes.

**Key Features**:
- Role-based agent design
- Task delegation and dependencies
- Sequential/hierarchical processes
- Specialized agent roles
- Team collaboration

**Example File**: `examples/crewai_agent_example.py`

---

## Installation

```bash
pip install crewai
pip install crewai-tools  # Optional for additional tools
```

---

## Quick Start

### Simple Two-Agent Crew

```python
from crewai import Agent, Task, Crew, Process

# Create agents with roles
researcher = Agent(
    role="Research Analyst",
    goal="Gather comprehensive information on topics",
    backstory="""You are an experienced research analyst with expertise
    in gathering and synthesizing information.""",
    verbose=True,
    llm="gpt-4o-mini"
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging and informative content",
    backstory="""You are a skilled content writer who makes complex
    topics accessible to general audiences.""",
    verbose=True,
    llm="gpt-4o-mini"
)

# Create tasks
research_task = Task(
    description="Research artificial intelligence trends in 2024",
    agent=researcher,
    expected_output="Comprehensive research findings"
)

writing_task = Task(
    description="Write an article based on the research",
    agent=writer,
    expected_output="Well-written 500-word article",
    context=[research_task]  # Depends on research task
)

# Create crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True
)

# Execute
result = crew.kickoff()
print(result)
```

---

## Specialized Multi-Agent Crew

```python
from crewai import Agent, Task, Crew, Process

# Create specialized business agents
market_researcher = Agent(
    role="Market Research Specialist",
    goal="Analyze market trends and consumer behavior",
    backstory="""You are a market research specialist with 10 years
    of experience in market analysis.""",
    verbose=True,
    llm="gpt-4o-mini"
)

data_analyst = Agent(
    role="Data Analyst",
    goal="Extract insights from data",
    backstory="""You are a data analyst expert in statistical
    analysis and data visualization.""",
    verbose=True,
    llm="gpt-4o-mini"
)

strategist = Agent(
    role="Business Strategist",
    goal="Develop actionable strategies",
    backstory="""You are a business strategist with expertise
    in corporate strategy and planning.""",
    verbose=True,
    llm="gpt-4o-mini"
)

report_writer = Agent(
    role="Report Writer",
    goal="Create professional business reports",
    backstory="""You are a professional report writer skilled
    in creating clear business documents.""",
    verbose=True,
    llm="gpt-4o-mini"
)

# Create dependent tasks
market_task = Task(
    description="Conduct market research on electric vehicles",
    agent=market_researcher,
    expected_output="Market research findings"
)

analysis_task = Task(
    description="Analyze the market research data",
    agent=data_analyst,
    expected_output="Data analysis with insights",
    context=[market_task]
)

strategy_task = Task(
    description="Develop strategic recommendations",
    agent=strategist,
    expected_output="Strategic recommendations",
    context=[market_task, analysis_task]
)

report_task = Task(
    description="Create comprehensive business report",
    agent=report_writer,
    expected_output="Professional business report",
    context=[market_task, analysis_task, strategy_task]
)

# Create crew
crew = Crew(
    agents=[market_researcher, data_analyst, strategist, report_writer],
    tasks=[market_task, analysis_task, strategy_task, report_task],
    process=Process.sequential,
    verbose=True
)

# Execute workflow
result = crew.kickoff()
```

---

## Hierarchical Process

```python
# Create manager agent
manager = Agent(
    role="Project Manager",
    goal="Coordinate the team and ensure quality",
    backstory="You are an experienced project manager",
    llm="gpt-4o-mini"
)

# Create crew with hierarchical process
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,
    manager_llm="gpt-4o-mini",
    verbose=True
)
```

---

## Tools Integration

```python
from crewai_tools import SerperDevTool, WebsiteSearchTool

# Create tools
search_tool = SerperDevTool()
web_tool = WebsiteSearchTool()

# Create agent with tools
researcher = Agent(
    role="Research Analyst",
    goal="Find information online",
    tools=[search_tool, web_tool],
    verbose=True,
    llm="gpt-4o-mini"
)
```

---

## Evaluation with Custom-Evals

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

# Run crew
result = crew.kickoff()

# Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

coherence = CoherenceEvaluator(eval_llm)
score = coherence.evaluate({
    "input": "Write about AI trends",
    "output": str(result)
})

relevance = RelevanceEvaluator(eval_llm)
rel_score = relevance.evaluate({
    "input": "Write about AI trends",
    "output": str(result)
})

print(f"Coherence: {score.label} ({score.score:.2f})")
print(f"Relevance: {rel_score.label} ({rel_score.score:.2f})")
```

---

## Testing Examples

### Test Simple Crew

```python
def test_simple_crew():
    crew = SimpleCrewSystem()

    result = crew.run("Artificial Intelligence in Healthcare")

    assert result["success"]
    assert len(result["output"]) > 100

    scores = crew.evaluate(
        "Artificial Intelligence in Healthcare",
        result["output"]
    )

    assert scores["coherence"].score >= 0.7
```

### Test Specialized Crew

```python
def test_specialized_crew():
    crew = SpecializedCrew()

    result = crew.run("Market opportunities in e-commerce")

    assert result["success"]
    assert "market" in result["output"].lower()

    scores = crew.evaluate(
        "Market opportunities in e-commerce",
        result["output"]
    )

    assert all(s.score >= 0.7 for s in scores.values())
```

---

## Best Practices

### 1. Clear Role Definitions

```python
# Good: Clear, specific role
agent = Agent(
    role="Senior Data Analyst",
    goal="Analyze sales data and identify trends",
    backstory="""You are a senior data analyst with 8 years of experience
    specializing in retail analytics and trend forecasting."""
)

# Avoid: Vague role
agent = Agent(
    role="Analyst",
    goal="Analyze stuff",
    backstory="You analyze things"
)
```

### 2. Task Dependencies

```python
# Define clear dependencies
task1 = Task(description="Research", agent=researcher)
task2 = Task(description="Analyze", agent=analyst, context=[task1])
task3 = Task(description="Write", agent=writer, context=[task1, task2])

# Task3 can access outputs from task1 and task2
```

### 3. Expected Outputs

```python
task = Task(
    description="Research AI trends",
    agent=researcher,
    expected_output="Bulleted list of top 5 AI trends with explanations"
)
```

### 4. Process Selection

```python
# Sequential: Tasks run in order
crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.sequential  # task1 → task2 → task3
)

# Hierarchical: Manager coordinates
crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.hierarchical,  # Manager delegates
    manager_llm="gpt-4o-mini"
)
```

---

## Use Cases

### Content Creation

```python
# Blog post creation workflow
researcher = Agent(role="Researcher", ...)
seo_specialist = Agent(role="SEO Specialist", ...)
writer = Agent(role="Content Writer", ...)
editor = Agent(role="Editor", ...)

# Research → SEO → Write → Edit
```

### Business Analysis

```python
# Market analysis workflow
market_researcher = Agent(role="Market Researcher", ...)
data_analyst = Agent(role="Data Analyst", ...)
strategist = Agent(role="Strategist", ...)
report_writer = Agent(role="Report Writer", ...)

# Research → Analyze → Strategy → Report
```

### Product Development

```python
# Product planning workflow
user_researcher = Agent(role="User Researcher", ...)
product_manager = Agent(role="Product Manager", ...)
designer = Agent(role="Designer", ...)
tech_lead = Agent(role="Tech Lead", ...)

# User Research → Requirements → Design → Tech Spec
```

---

## Quality Gates

```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
    "completeness": 0.8
}

def validate_crew_output(result, scores):
    if not result["success"]:
        return False, "Crew execution failed"

    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric in scores:
            if scores[metric].score < threshold:
                return False, f"{metric} below threshold"

    return True, "All checks passed"
```

---

## Performance Tips

### 1. Optimize Agent Count

```python
# Good: 2-4 agents for most tasks
crew = Crew(agents=[researcher, writer], ...)

# Avoid: Too many agents (slow and expensive)
crew = Crew(agents=[agent1, agent2, ..., agent10], ...)
```

### 2. Limit Task Complexity

```python
# Break complex tasks into smaller ones
task1 = Task(description="Research topic X")
task2 = Task(description="Analyze findings")
task3 = Task(description="Write summary")

# Better than one huge task
```

### 3. Use Caching

```python
# CrewAI caches LLM responses automatically
# Ensure deterministic tasks for cache hits
```

---

## Troubleshooting

### Issue: Tasks taking too long

**Solution**: Simplify task descriptions and reduce agent count

```python
# Use clear, concise task descriptions
task = Task(
    description="Research top 3 AI trends in healthcare",  # Specific
    agent=researcher
)
```

### Issue: Low-quality outputs

**Solution**: Improve agent backstories and task expectations

```python
agent = Agent(
    role="Expert Researcher",
    goal="Provide accurate, well-sourced information",
    backstory="Detailed expertise description...",
    verbose=True  # Enable to see agent reasoning
)
```

### Issue: Agents not collaborating well

**Solution**: Use task context to share information

```python
task2 = Task(
    description="Analyze the research",
    agent=analyst,
    context=[research_task]  # Access research_task output
)
```

---

## Resources

- **Official Docs**: https://docs.crewai.com/
- **GitHub**: https://github.com/joaomdmoura/crewAI
- **Example File**: `examples/crewai_agent_example.py`
- **Tools**: https://github.com/joaomdmoura/crewAI-tools

---

## Next Steps

1. Install CrewAI: `pip install crewai`
2. Run example: `python examples/crewai_agent_example.py`
3. Create your first crew with 2 agents
4. Experiment with task dependencies
5. Build a complete workflow

**See Also**:
- [Autogen](autogen.md) - Multi-agent conversations
- [OpenAI Swarm](openai-swarm.md) - Lightweight coordination
- [Multi-Agent System](multi-agent.md) - Custom orchestration
