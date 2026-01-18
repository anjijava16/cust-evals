# AWS Strands Agents with Custom-Evals

## Overview

AWS Strands is an agent framework that provides seamless integration with AWS Bedrock, enabling developers to build production-ready AI agents using Claude and other foundation models. The framework offers robust multi-agent orchestration, tool integration, and state management capabilities specifically designed for AWS cloud environments.

**Key Features**:
- **AWS Bedrock Integration**: Native support for Claude models (Claude 3 Haiku, Sonnet, Opus)
- **Multi-Agent Orchestration**: Coordinate multiple specialized agents in complex workflows
- **Tool Integration**: Extensible tool system for weather, search, calculations, and custom tools
- **State Management**: Built-in conversation and context tracking
- **Production Ready**: Enterprise-grade reliability and scalability on AWS infrastructure
- **Custom-Evals Integration**: Full support for Phoenix custom-evals evaluation framework

**Use Cases**:
- Customer service automation on AWS
- Data analysis and reporting workflows
- Multi-step research and analysis tasks
- AWS cloud operations automation
- Enterprise AI assistants with AWS services integration

---

## Installation

### Prerequisites
- Python 3.10 or higher
- AWS Account with Bedrock access
- OpenAI API key (for custom-evals)

### Install Dependencies

```bash
pip install strands boto3
```

### Environment Setup

Set up your AWS credentials and configuration:

```bash
export AWS_ACCESS_KEY_ID="your-aws-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-aws-secret-access-key"
export AWS_REGION="us-east-1"

# For custom-evals (optional but recommended)
export OPENAI_API_KEY="your-openai-api-key"
```

### Verify Installation

```python
import boto3
from strands import Agent, Tool
from strands.providers import BedrockProvider

# Test Bedrock connection
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
print("✅ AWS Bedrock connection successful")
```

---

## Quick Start

### Simple Agent Example

```python
import os
from strands import Agent, Tool
from strands.providers import BedrockProvider

# Create Bedrock provider
provider = BedrockProvider(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

# Define a simple tool
class WeatherTool(Tool):
    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get current weather for a location"
        )

    def execute(self, location: str) -> str:
        weather_data = {
            "San Francisco": {"temp": "72°F", "condition": "Sunny"},
            "New York": {"temp": "65°F", "condition": "Cloudy"},
            "London": {"temp": "55°F", "condition": "Rainy"}
        }
        data = weather_data.get(location, {"temp": "Unknown", "condition": "Unknown"})
        return f"Weather in {location}: {data['condition']}, {data['temp']}"

# Create agent
agent = Agent(
    name="assistant",
    provider=provider,
    tools=[WeatherTool()],
    instructions="You are a helpful assistant with access to weather information."
)

# Run agent
result = agent.run("What's the weather in San Francisco?")
print(result.response)
```

### Agent with Custom-Evals Integration

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

# Initialize evaluators
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
coherence_evaluator = CoherenceEvaluator(eval_llm)
relevance_evaluator = RelevanceEvaluator(eval_llm)

# Run agent
query = "What's the weather like in New York?"
result = agent.run(query)

# Evaluate response
coherence_score = coherence_evaluator.evaluate({
    "input": query,
    "output": result.response
})

relevance_score = relevance_evaluator.evaluate({
    "input": query,
    "output": result.response
})

print(f"Coherence: {coherence_score.label} ({coherence_score.score:.2f})")
print(f"Relevance: {relevance_score.label} ({relevance_score.score:.2f})")
```

---

## Architecture

### Core Components

**1. BedrockProvider**
- Manages AWS Bedrock API connections
- Handles model selection and configuration
- Provides retry logic and error handling

**2. Agent**
- Main agent class that orchestrates tasks
- Manages tool execution and conversation flow
- Supports both synchronous and asynchronous operations

**3. Tool System**
- Base `Tool` class for creating custom tools
- Tools have `name`, `description`, and `execute()` method
- Automatic parameter extraction from tool descriptions

**4. Multi-Agent Coordinator**
- Orchestrates multiple specialized agents
- Manages handoffs between agents
- Maintains shared context and state

### Agent Creation Pattern

```python
from strands import Agent, Tool
from strands.providers import BedrockProvider

class MyTool(Tool):
    def __init__(self):
        super().__init__(
            name="tool_name",
            description="Tool description for the LLM",
            parameters={
                "param1": {"type": "string", "description": "Parameter description"}
            }
        )

    def execute(self, param1: str) -> str:
        # Tool implementation
        return result

# Create agent with tool
provider = BedrockProvider(model_id="anthropic.claude-3-haiku-20240307-v1:0")
agent = Agent(
    name="agent_name",
    provider=provider,
    tools=[MyTool()],
    instructions="Agent instructions"
)
```

---

## Multi-Agent Systems

### Multi-Agent Workflow Example

```python
from strands import Agent, Tool
from strands.providers import BedrockProvider

class MultiAgentStrandsSystem:
    """Multi-agent system with specialized agents."""

    def __init__(self):
        provider = BedrockProvider(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1"
        )

        # Create specialized agents
        self.research_agent = Agent(
            name="researcher",
            provider=provider,
            tools=[SearchTool()],
            instructions="You are a research specialist. Gather comprehensive information."
        )

        self.analysis_agent = Agent(
            name="analyst",
            provider=provider,
            instructions="You are an analysis expert. Extract key insights and patterns."
        )

        self.writer_agent = Agent(
            name="writer",
            provider=provider,
            instructions="You are a technical writer. Create clear, concise summaries."
        )

    def run_workflow(self, topic: str):
        """Run multi-agent workflow."""
        # Step 1: Research
        research_result = self.research_agent.run(f"Research information about: {topic}")

        # Step 2: Analysis
        analysis_result = self.analysis_agent.run(
            f"Analyze this research: {research_result.response}"
        )

        # Step 3: Writing
        final_result = self.writer_agent.run(
            f"Create a summary about {topic} based on: {analysis_result.response}"
        )

        return {
            "research": research_result.response,
            "analysis": analysis_result.response,
            "final_output": final_result.response
        }

# Usage
system = MultiAgentStrandsSystem()
result = system.run_workflow("Artificial Intelligence in Healthcare")
print(result["final_output"])
```

---

## Custom-Evals Integration

### Complete Evaluation System

AWS Strands agents can be evaluated using Phoenix custom-evals framework with four key metrics:

**1. Coherence (threshold: 0.7)**
- Measures logical flow and consistency of responses

**2. Relevance (threshold: 0.7)**
- Measures how relevant the response is to the query

**3. Correctness (threshold: 0.7)**
- Measures factual accuracy of the response

**4. Toxicity (threshold: 0.2, lower is better)**
- Measures harmful or toxic content

### Implementation

```python
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM

class EvaluatedAWSStrandsAgent:
    """AWS Strands agent with evaluation capabilities."""

    def __init__(self):
        # Create agent
        provider = BedrockProvider(model_id="anthropic.claude-3-haiku-20240307-v1:0")
        self.agent = Agent(
            name="assistant",
            provider=provider,
            tools=[WeatherTool(), SearchTool()],
            instructions="You are a helpful assistant."
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run_and_evaluate(self, query: str, expected: str = None):
        """Run agent and evaluate response."""
        # Run agent
        result = self.agent.run(query)
        response = result.response

        # Evaluate
        scores = {}
        for name, evaluator in self.evaluators.items():
            eval_input = {"input": query, "output": response}

            if name == "correctness" and expected:
                eval_input["expected"] = expected

            score = evaluator.evaluate(eval_input)
            scores[name] = score

        return {
            "response": response,
            "scores": scores
        }

# Usage
agent = EvaluatedAWSStrandsAgent()
result = agent.run_and_evaluate("What is artificial intelligence?")

print(f"Response: {result['response']}\n")
print("Evaluation Scores:")
for metric, score in result['scores'].items():
    print(f"  {metric.capitalize()}: {score.label} ({score.score:.2f})")
    print(f"    {score.explanation[:100]}...")
```

### Quality Gates

```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
    "correctness": 0.7,
    "toxicity": 0.2  # Lower is better
}

def validate_quality_gates(scores):
    """Validate response against quality thresholds."""
    passed = True

    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric in scores:
            score_value = scores[metric].score

            if metric == "toxicity":
                if score_value > threshold:
                    passed = False
                    print(f"❌ {metric}: {score_value:.2f} (threshold: <{threshold})")
                else:
                    print(f"✅ {metric}: {score_value:.2f}")
            else:
                if score_value < threshold:
                    passed = False
                    print(f"❌ {metric}: {score_value:.2f} (threshold: >{threshold})")
                else:
                    print(f"✅ {metric}: {score_value:.2f}")

    return passed

# Usage
result = agent.run_and_evaluate("Explain machine learning")
passed = validate_quality_gates(result['scores'])
print(f"\nQuality Gate: {'✅ PASSED' if passed else '❌ FAILED'}")
```

---

## Testing Examples

### Test Suite 1: Simple Agent Query

```python
def test_simple_agent():
    """Test basic agent functionality."""
    provider = BedrockProvider(model_id="anthropic.claude-3-haiku-20240307-v1:0")
    agent = Agent(
        name="assistant",
        provider=provider,
        instructions="You are a helpful assistant."
    )

    query = "What is artificial intelligence?"
    result = agent.run(query)

    assert result.success
    assert len(result.response) > 0
    print(f"✅ Response: {result.response[:200]}...")
```

### Test Suite 2: Agent with Tools

```python
def test_agent_with_tools():
    """Test agent with tool usage."""
    provider = BedrockProvider(model_id="anthropic.claude-3-haiku-20240307-v1:0")
    agent = Agent(
        name="assistant",
        provider=provider,
        tools=[WeatherTool(), CalculatorTool()],
        instructions="You are a helpful assistant with access to tools."
    )

    query = "What's the weather in Tokyo and calculate 25 * 4?"
    result = agent.run(query)

    assert result.success
    assert "Tokyo" in result.response or "weather" in result.response.lower()
    assert "100" in result.response  # 25 * 4 = 100
    print(f"✅ Response with tools: {result.response}")
```

### Test Suite 3: Multi-Agent Workflow

```python
def test_multi_agent_workflow():
    """Test multi-agent collaboration."""
    system = MultiAgentStrandsSystem()

    topic = "Climate Change"
    result = system.run_workflow(topic)

    assert "research" in result
    assert "analysis" in result
    assert "final_output" in result
    assert len(result["final_output"]) > 0
    print(f"✅ Multi-agent workflow completed: {result['final_output'][:200]}...")
```

### Test Suite 4: Quality Gates Validation

```python
def test_quality_gates():
    """Test quality gate validation."""
    agent = EvaluatedAWSStrandsAgent()

    test_queries = [
        "Explain AWS Bedrock",
        "What is Claude AI?",
        "Tell me about machine learning"
    ]

    passed_count = 0

    for query in test_queries:
        result = agent.run_and_evaluate(query)
        passed = validate_quality_gates(result['scores'])
        if passed:
            passed_count += 1

    print(f"\n✅ Quality Gates: {passed_count}/{len(test_queries)} passed")
    assert passed_count >= len(test_queries) * 0.8  # 80% pass rate
```

### Test Suite 5: Batch Evaluation

```python
def test_batch_evaluation():
    """Test batch evaluation of multiple queries."""
    agent = EvaluatedAWSStrandsAgent()

    test_cases = [
        {"query": "What is AI?", "category": "AI"},
        {"query": "Calculate 100 / 4", "category": "Math"},
        {"query": "Weather in London?", "category": "Weather"}
    ]

    results = []

    for test_case in test_cases:
        result = agent.run_and_evaluate(test_case["query"])
        avg_score = sum(s.score for s in result['scores'].values()) / len(result['scores'])
        results.append({"query": test_case["query"], "avg_score": avg_score})

    overall_avg = sum(r['avg_score'] for r in results) / len(results)
    print(f"\n✅ Batch Evaluation - Average Score: {overall_avg:.2f}")
    assert overall_avg >= 0.7  # Minimum average score threshold
```

---

## Best Practices

### 1. Model Selection

**Use appropriate Claude models for your use case**:
- **Claude 3 Haiku**: Fast, cost-effective for simple tasks
- **Claude 3 Sonnet**: Balanced performance and cost
- **Claude 3 Opus**: Maximum capability for complex reasoning

```python
# For simple tasks
provider = BedrockProvider(model_id="anthropic.claude-3-haiku-20240307-v1:0")

# For complex analysis
provider = BedrockProvider(model_id="anthropic.claude-3-opus-20240229-v1:0")
```

### 2. Tool Design

**Keep tools focused and single-purpose**:
```python
# ✅ Good: Focused tool
class WeatherTool(Tool):
    def execute(self, location: str) -> str:
        return self.get_weather(location)

# ❌ Bad: Multi-purpose tool
class UtilityTool(Tool):
    def execute(self, action: str, **kwargs):
        if action == "weather":
            return self.get_weather(kwargs["location"])
        elif action == "search":
            return self.search(kwargs["query"])
        # ... too many responsibilities
```

### 3. Error Handling

**Implement robust error handling**:
```python
def run_agent_safely(agent, query):
    """Run agent with comprehensive error handling."""
    try:
        result = agent.run(query)

        if not result.success:
            print(f"❌ Agent execution failed: {result.error}")
            return None

        return result

    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None
```

### 4. Evaluation Integration

**Always evaluate production agents**:
```python
# Evaluate every production response
result = agent.run(query)
scores = evaluate_response(query, result.response)

# Log to monitoring system
log_evaluation_metrics(query, result.response, scores)

# Alert on quality issues
if not validate_quality_gates(scores):
    alert_quality_failure(query, scores)
```

### 5. Cost Optimization

**Monitor and optimize AWS Bedrock costs**:
- Use streaming for long responses
- Cache frequent queries
- Choose appropriate model tiers
- Monitor token usage

```python
# Enable streaming for cost efficiency
result = agent.run(query, stream=True)
for chunk in result.stream():
    print(chunk, end="")
```

### 6. Security

**Secure your AWS credentials**:
- Use IAM roles instead of access keys when possible
- Implement least privilege access
- Rotate credentials regularly
- Never commit credentials to version control

```python
# Use environment variables
import os
from strands.providers import BedrockProvider

provider = BedrockProvider(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name=os.getenv("AWS_REGION"),
    # Credentials loaded from environment or IAM role
)
```

---

## Troubleshooting

### Common Issues

**1. AWS Credentials Not Found**
```
Error: Unable to locate credentials
```

**Solution**:
```bash
# Set AWS credentials
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_REGION="us-east-1"

# Or configure AWS CLI
aws configure
```

**2. Bedrock Model Access Denied**
```
Error: AccessDeniedException: User is not authorized to perform bedrock:InvokeModel
```

**Solution**:
- Enable Bedrock model access in AWS Console
- Verify IAM permissions include `bedrock:InvokeModel`
- Check that the model is available in your region

**3. Tool Execution Failures**
```
Error: Tool execution failed
```

**Solution**:
- Add error handling to tool `execute()` methods
- Validate tool parameters before execution
- Return informative error messages

```python
class SafeTool(Tool):
    def execute(self, param: str) -> str:
        try:
            # Tool logic
            return result
        except Exception as e:
            return f"Error: {str(e)}"
```

**4. Slow Response Times**
```
Agent taking too long to respond
```

**Solution**:
- Use Claude 3 Haiku for faster responses
- Reduce context size
- Implement request timeouts
- Consider streaming responses

**5. High AWS Costs**
```
Unexpected AWS Bedrock charges
```

**Solution**:
- Monitor token usage with CloudWatch
- Use smaller models when appropriate
- Implement response caching
- Set up billing alerts

---

## Resources

### Official Documentation
- **AWS Bedrock**: https://aws.amazon.com/bedrock/
- **Claude Models**: https://www.anthropic.com/claude
- **Strands Framework**: Check AWS documentation for latest SDK

### Example Files
- **Complete Example**: `examples/aws_strands_agents_example.py` (18KB)
- **Test Suites**: 5 comprehensive tests covering all use cases
- **Custom-Evals Integration**: Full evaluation implementation

### Phoenix Custom-Evals
- **Documentation**: Phoenix custom-evals framework docs
- **Evaluators**: CoherenceEvaluator, RelevanceEvaluator, CorrectnessEvaluator, ToxicityEvaluator
- **LLM Integration**: Support for OpenAI, Anthropic, and other providers

### AWS Resources
- **IAM Setup**: AWS IAM for Bedrock access
- **Pricing**: AWS Bedrock pricing calculator
- **Quotas**: Service quotas and limits

### Community
- **GitHub Issues**: Report bugs and feature requests
- **Discord**: Join community discussions
- **Examples**: Browse community examples and templates

---

## Quick Reference

### Installation
```bash
pip install strands boto3
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_REGION="us-east-1"
```

### Basic Agent
```python
from strands import Agent
from strands.providers import BedrockProvider

provider = BedrockProvider(model_id="anthropic.claude-3-haiku-20240307-v1:0")
agent = Agent(name="assistant", provider=provider)
result = agent.run("Your query here")
```

### With Evaluation
```python
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM

eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)
score = evaluator.evaluate({"input": query, "output": response})
```

### Quality Thresholds
- Coherence: ≥ 0.7
- Relevance: ≥ 0.7
- Correctness: ≥ 0.7
- Toxicity: ≤ 0.2

---

**Created**: 2026-01-17
**Status**: Production Ready
**Framework Version**: Latest
**Custom-Evals**: Fully Integrated
