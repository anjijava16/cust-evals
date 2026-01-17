# Agents & Multi-Agent Integration Guide

This guide shows how to use Custom Evals to evaluate AI agents and multi-agent systems.

## 🎯 Why Evaluate Agents?

AI agents and multi-agent systems need evaluation for:
- **Quality Assurance**: Ensure agent outputs meet standards
- **Performance Monitoring**: Track agent behavior over time
- **Debugging**: Identify issues in agent reasoning
- **A/B Testing**: Compare different agent configurations
- **Production Monitoring**: Monitor agent behavior in real-time

---

## ✅ Yes, Custom Evals Works with ALL Agent Projects!

Custom Evals is **framework-agnostic** and works with:

- ✅ **LangChain Agents**
- ✅ **LlamaIndex Agents**
- ✅ **AutoGPT / BabyAGI**
- ✅ **CrewAI Agents**
- ✅ **Custom Agent Implementations**
- ✅ **Multi-Agent Systems**
- ✅ **Tool-Using Agents**
- ✅ **ReAct Agents**
- ✅ **Conversational Agents**

**Why?** Because Custom Evals evaluates **text outputs**, not specific frameworks.

---

## 🔧 Integration Pattern

### Basic Pattern

```python
from custom.evals import HallucinationEvaluator, CorrectnessEvaluator
from custom.evals.llm import LLM

# 1. Initialize evaluator
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

# 2. Run your agent
agent_output = your_agent.run(query)

# 3. Evaluate agent output
score = evaluator.evaluate({
    "input": query,
    "output": agent_output,
    "context": retrieved_context  # if applicable
})

# 4. Use the score
print(f"Agent quality: {score.label} ({score.score})")
if score.label == "hallucinated":
    print(f"⚠️ Warning: {score.explanation}")
```

---

## 📊 Agent Evaluation Strategies

### Strategy 1: Single Output Evaluation

Evaluate each agent response individually.

```python
from custom.evals import HallucinationEvaluator, CoherenceEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")

# Create evaluators
hallucination_eval = HallucinationEvaluator(llm)
coherence_eval = CoherenceEvaluator(llm)

def evaluate_agent_response(query, agent_output, context=None):
    """Evaluate a single agent response."""
    results = {}

    # Check for hallucinations (if context available)
    if context:
        hall_score = hallucination_eval.evaluate({
            "input": query,
            "output": agent_output,
            "context": context
        })
        results["hallucination"] = hall_score

    # Check coherence
    coh_score = coherence_eval.evaluate({
        "input": query,
        "output": agent_output
    })
    results["coherence"] = coh_score

    return results

# Use with your agent
query = "What are the latest market trends?"
agent_output = my_agent.run(query)
context = my_agent.get_retrieved_context()

scores = evaluate_agent_response(query, agent_output, context)
print(f"Hallucination: {scores['hallucination'].label}")
print(f"Coherence: {scores['coherence'].label}")
```

### Strategy 2: Batch Evaluation

Evaluate multiple agent runs together.

```python
import pandas as pd
from custom.evals import CorrectnessEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CorrectnessEvaluator(llm)

# Test queries with expected outputs
test_cases = [
    {"query": "What is 2+2?", "expected": "4"},
    {"query": "Capital of France?", "expected": "Paris"},
    {"query": "Who wrote Hamlet?", "expected": "Shakespeare"}
]

# Run agent on all queries
results = []
for test in test_cases:
    agent_output = my_agent.run(test["query"])

    score = evaluator.evaluate({
        "input": test["query"],
        "output": agent_output,
        "expected": test["expected"]
    })

    results.append({
        "query": test["query"],
        "output": agent_output,
        "expected": test["expected"],
        "score": score.score,
        "label": score.label
    })

# Analyze results
df = pd.DataFrame(results)
print(f"Agent Accuracy: {df['score'].mean():.2%}")
print(f"Correct: {(df['label'] == 'correct').sum()}/{len(df)}")
```

### Strategy 3: Multi-Metric Evaluation

Use multiple evaluators for comprehensive assessment.

```python
from custom.evals import (
    HallucinationEvaluator,
    CorrectnessEvaluator,
    RelevanceEvaluator,
    CoherenceEvaluator
)

def comprehensive_agent_evaluation(query, agent_output, context=None, expected=None):
    """Comprehensive multi-metric evaluation."""
    llm = LLM(provider="openai", model="gpt-4o-mini")

    evaluators = {
        "hallucination": HallucinationEvaluator(llm),
        "relevance": RelevanceEvaluator(llm),
        "coherence": CoherenceEvaluator(llm)
    }

    if expected:
        evaluators["correctness"] = CorrectnessEvaluator(llm)

    results = {}

    for name, evaluator in evaluators.items():
        eval_input = {"input": query, "output": agent_output}

        if name == "hallucination" and context:
            eval_input["context"] = context
        elif name == "relevance" and context:
            eval_input["context"] = context
        elif name == "correctness" and expected:
            eval_input["expected"] = expected

        try:
            score = evaluator.evaluate(eval_input)
            results[name] = {
                "score": score.score,
                "label": score.label,
                "explanation": score.explanation
            }
        except Exception as e:
            results[name] = {"error": str(e)}

    return results
```

---

## 🤖 Framework-Specific Examples

### LangChain Agents

```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

# 1. Create LangChain agent
tools = [...]  # Your tools
llm_langchain = OpenAI(temperature=0)
agent = initialize_agent(tools, llm_langchain, agent="zero-shot-react-description")

# 2. Create evaluator
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(eval_llm)

# 3. Run and evaluate
query = "What is the weather in San Francisco?"
agent_output = agent.run(query)

# Get context from agent's intermediate steps
context = agent.agent.llm_chain.memory.buffer if hasattr(agent.agent, 'llm_chain') else None

score = evaluator.evaluate({
    "input": query,
    "output": agent_output,
    "context": context or "No context available"
})

print(f"Agent Quality: {score.label}")
```

### LlamaIndex Agents

```python
from llama_index.core.agent import ReActAgent
from custom.evals import CorrectnessEvaluator, CoherenceEvaluator
from custom.evals.llm import LLM

# 1. Create LlamaIndex agent
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True)

# 2. Create evaluators
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
correctness = CorrectnessEvaluator(eval_llm)
coherence = CoherenceEvaluator(eval_llm)

# 3. Run and evaluate
response = agent.chat("Analyze the latest sales data")

# Evaluate correctness (if you have expected answer)
if expected_answer:
    corr_score = correctness.evaluate({
        "input": "Analyze the latest sales data",
        "output": str(response),
        "expected": expected_answer
    })

# Evaluate coherence
coh_score = coherence.evaluate({
    "input": "Analyze the latest sales data",
    "output": str(response)
})

print(f"Coherence: {coh_score.label} ({coh_score.score})")
```

### CrewAI Agents

```python
from crewai import Agent, Task, Crew
from custom.evals import HallucinationEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

# 1. Create CrewAI agents
researcher = Agent(
    role='Researcher',
    goal='Research accurate information',
    backstory='Expert researcher',
    verbose=True
)

# 2. Create task
task = Task(
    description='Research AI trends',
    agent=researcher
)

crew = Crew(agents=[researcher], tasks=[task])

# 3. Run crew
result = crew.kickoff()

# 4. Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = RelevanceEvaluator(eval_llm)

score = evaluator.evaluate({
    "input": "Research AI trends",
    "context": result.output
})

print(f"Agent Output Relevance: {score.label}")
```

### Custom Agent Implementation

```python
class MyCustomAgent:
    def __init__(self):
        self.llm = OpenAI()

    def run(self, query):
        # Your custom agent logic
        response = self.llm(query)
        return response

# Evaluate your custom agent
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM

agent = MyCustomAgent()
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)

# Run and evaluate
query = "Explain quantum computing"
output = agent.run(query)

score = evaluator.evaluate({
    "input": query,
    "output": output
})

print(f"Agent coherence: {score.label}")
```

---

## 🔄 Multi-Agent System Evaluation

### Evaluating Agent Collaboration

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

def evaluate_multi_agent_output(task, agent_outputs):
    """Evaluate outputs from multiple agents."""
    llm = LLM(provider="openai", model="gpt-4o-mini")
    coherence_eval = CoherenceEvaluator(llm)
    relevance_eval = RelevanceEvaluator(llm)

    results = {}

    for agent_name, output in agent_outputs.items():
        # Evaluate each agent's contribution
        coh_score = coherence_eval.evaluate({
            "input": task,
            "output": output
        })

        rel_score = relevance_eval.evaluate({
            "input": task,
            "context": output
        })

        results[agent_name] = {
            "coherence": coh_score,
            "relevance": rel_score
        }

    return results

# Example usage
task = "Create a marketing strategy"
agent_outputs = {
    "research_agent": "Market analysis shows...",
    "strategy_agent": "Proposed strategy: ...",
    "writer_agent": "Campaign content: ..."
}

scores = evaluate_multi_agent_output(task, agent_outputs)

for agent, metrics in scores.items():
    print(f"{agent}:")
    print(f"  Coherence: {metrics['coherence'].label}")
    print(f"  Relevance: {metrics['relevance'].label}")
```

### Evaluating Agent Handoffs

```python
def evaluate_agent_handoff(previous_output, current_output, context):
    """Evaluate if agent properly continued from previous agent."""
    from custom.evals import CoherenceEvaluator, RelevanceEvaluator
    from custom.evals.llm import LLM

    llm = LLM(provider="openai", model="gpt-4o-mini")

    # Check if current output is coherent with previous
    combined_output = f"{previous_output}\n\n{current_output}"
    coherence_eval = CoherenceEvaluator(llm)

    score = coherence_eval.evaluate({
        "input": context,
        "output": combined_output
    })

    return score

# Example
prev = "Agent 1 found 3 solutions..."
curr = "Agent 2 analyzed those solutions and recommends..."
context = "Find and analyze solutions for problem X"

handoff_score = evaluate_agent_handoff(prev, curr, context)
print(f"Handoff quality: {handoff_score.label}")
```

---

## 📈 Production Monitoring for Agents

### Real-Time Agent Monitoring

```python
from custom.evals import HallucinationEvaluator, initialize_tracing
from custom.evals.llm import LLM
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Optional: Enable Phoenix tracing for observability
initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")

class MonitoredAgent:
    def __init__(self, agent):
        self.agent = agent
        self.llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluator = HallucinationEvaluator(self.llm)

    def run_with_evaluation(self, query, context=None):
        """Run agent and evaluate output."""
        # Run agent
        output = self.agent.run(query)

        # Evaluate
        score = self.evaluator.evaluate({
            "input": query,
            "output": output,
            "context": context or "No context"
        })

        # Log results
        logger.info(f"Query: {query}")
        logger.info(f"Quality: {score.label} ({score.score})")

        # Alert on issues
        if score.label == "hallucinated":
            logger.warning(f"⚠️ Hallucination detected: {score.explanation}")
            # Send alert, save to DB, etc.

        return output, score

# Use monitored agent
monitored_agent = MonitoredAgent(my_agent)
output, score = monitored_agent.run_with_evaluation("What are the Q3 results?")
```

### Batch Agent Performance Testing

```python
import pandas as pd
from datetime import datetime

def batch_test_agent(agent, test_cases, evaluator):
    """Run comprehensive batch testing on agent."""
    results = []

    for test in test_cases:
        start_time = datetime.now()

        # Run agent
        try:
            output = agent.run(test["query"])
            success = True
            error = None
        except Exception as e:
            output = ""
            success = False
            error = str(e)

        end_time = datetime.now()
        latency = (end_time - start_time).total_seconds()

        # Evaluate if successful
        if success:
            score = evaluator.evaluate({
                "input": test["query"],
                "output": output,
                "expected": test.get("expected"),
                "context": test.get("context")
            })

            results.append({
                "query": test["query"],
                "output": output,
                "expected": test.get("expected"),
                "score": score.score,
                "label": score.label,
                "latency_s": latency,
                "success": True,
                "error": None
            })
        else:
            results.append({
                "query": test["query"],
                "output": None,
                "expected": test.get("expected"),
                "score": 0.0,
                "label": "error",
                "latency_s": latency,
                "success": False,
                "error": error
            })

    # Create report
    df = pd.DataFrame(results)

    report = {
        "total_tests": len(df),
        "successful": df["success"].sum(),
        "failed": (~df["success"]).sum(),
        "avg_score": df[df["success"]]["score"].mean(),
        "avg_latency": df["latency_s"].mean(),
        "pass_rate": (df["label"] == "correct").sum() / len(df)
    }

    return df, report

# Example usage
test_cases = [
    {"query": "What is 2+2?", "expected": "4"},
    {"query": "Capital of Japan?", "expected": "Tokyo"},
    # ... more tests
]

from custom.evals.llm import LLM
from custom.evals import CorrectnessEvaluator

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CorrectnessEvaluator(llm)

df, report = batch_test_agent(my_agent, test_cases, evaluator)

print("Agent Performance Report:")
print(f"  Total Tests: {report['total_tests']}")
print(f"  Success Rate: {report['successful']/report['total_tests']:.2%}")
print(f"  Average Score: {report['avg_score']:.2f}")
print(f"  Average Latency: {report['avg_latency']:.2f}s")
print(f"  Pass Rate: {report['pass_rate']:.2%}")
```

---

## 🎯 Best Practices for Agent Evaluation

### 1. Choose Appropriate Evaluators

```python
# For agents with context/RAG
use_evaluators = [HallucinationEvaluator, FaithfulnessEvaluator, RelevanceEvaluator]

# For agents with known expected outputs
use_evaluators = [CorrectnessEvaluator]

# For conversational agents
use_evaluators = [CoherenceEvaluator, RelevanceEvaluator]

# For tool-using agents
use_evaluators = [CorrectnessEvaluator, HallucinationEvaluator]
```

### 2. Evaluate at Multiple Stages

```python
# Evaluate intermediate steps
for step in agent.intermediate_steps:
    evaluate_step(step)

# Evaluate final output
evaluate_final_output(agent.output)

# Evaluate tool calls
for tool_call in agent.tool_calls:
    evaluate_tool_usage(tool_call)
```

### 3. Create Custom Metrics for Your Agent

```python
from custom.evals import create_evaluator, Score

@create_evaluator(name="tool_accuracy", kind="code")
def evaluate_tool_selection(tool_used: str, expected_tool: str) -> Score:
    """Evaluate if agent selected correct tool."""
    correct = tool_used == expected_tool
    return Score(
        score=float(correct),
        label="correct_tool" if correct else "wrong_tool",
        explanation=f"Agent used {tool_used}, expected {expected_tool}"
    )

# Use it
score = evaluate_tool_selection({
    "tool_used": agent.last_tool,
    "expected_tool": "calculator"
})
```

### 4. Track Metrics Over Time

```python
import json
from datetime import datetime

class AgentMetricsTracker:
    def __init__(self, log_file="agent_metrics.jsonl"):
        self.log_file = log_file

    def log_evaluation(self, query, output, scores):
        """Log evaluation metrics."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "output": output,
            "scores": {name: score.to_dict() for name, score in scores.items()}
        }

        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_trends(self):
        """Analyze trends in agent performance."""
        # Load and analyze metrics
        pass

# Use it
tracker = AgentMetricsTracker()

output = agent.run(query)
scores = evaluate_agent(query, output)
tracker.log_evaluation(query, output, scores)
```

---

## ✅ Quick Start Checklist

- [ ] Choose evaluators appropriate for your agent type
- [ ] Integrate evaluation into agent workflow
- [ ] Test with sample queries
- [ ] Set up batch testing
- [ ] Configure production monitoring (optional)
- [ ] Enable Phoenix tracing for observability (optional)
- [ ] Create custom metrics if needed
- [ ] Set up metrics tracking

---

## 📚 See Also

- [RAG Integration Guide](rag-integration.md) - For RAG-based agents
- [LLM App Integration](llm-app-integration.md) - For simple LLM apps
- [Test Case Documentation](testing.md) - Test your integrations
- [Phoenix Tracing Guide](tracing.md) - Enable observability

---

## 💡 Example Projects

Check `examples/` for complete working examples:
- `examples/agent_evaluation.py` - Complete agent evaluation example
- `examples/multi_agent_evaluation.py` - Multi-agent system example
- `examples/agent_monitoring.py` - Production monitoring example

---

**Your agents can now be evaluated with Custom Evals! 🎉**
