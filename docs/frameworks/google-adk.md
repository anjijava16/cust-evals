# Google ADK (Agent Development Kit) - Production AI Agents

## Overview

**Google ADK (Agent Development Kit)** is Google's framework for building production-grade AI agents using Gemini models with advanced capabilities.

**Key Features**:
- Integration with Gemini models (1.5 Flash, Pro)
- Multi-agent collaboration
- Tool integration and function calling
- State management across agents
- Production-ready architecture
- Google Cloud integration

**Example File**: `examples/google_adk_agent_example.py`

---

## Installation

```bash
pip install google-generativeai
```

**Set up API Key**:
```bash
export GOOGLE_API_KEY="your-google-api-key"
```

Get your API key from: https://makersuite.google.com/app/apikey

---

## Quick Start

### Simple Agent

```python
import google.generativeai as genai
import os

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create model
model = genai.GenerativeModel('gemini-1.5-flash')

# Generate response
response = model.generate_content("What is machine learning?")
print(response.text)
```

---

## Agent with System Instructions

### Configure Agent Behavior

```python
# Create agent with system instructions
agent = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction="""You are a helpful AI assistant specializing in technology.
    Provide clear, accurate answers with examples when appropriate.
    """
)

# Run agent
response = agent.generate_content("Explain neural networks")
print(response.text)
```

---

## Tool Integration

### Define and Use Tools

```python
def get_weather(location: str) -> str:
    """Get weather for a location."""
    weather_data = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Cloudy, 65°F"
    }
    return weather_data.get(location, "Data not available")

def search_database(query: str) -> str:
    """Search knowledge base."""
    db = {
        "python": "Python is a programming language...",
        "ai": "AI is artificial intelligence..."
    }
    return db.get(query.lower(), "No information found")

# Integrate tools with agent
class GoogleADKAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.tools = {
            "get_weather": get_weather,
            "search_database": search_database
        }

    def run_with_tools(self, prompt: str):
        # Enhanced prompt with tool context
        enhanced_prompt = prompt

        # Route to appropriate tool
        if "weather" in prompt.lower():
            for location in ["San Francisco", "New York"]:
                if location.lower() in prompt.lower():
                    tool_result = get_weather(location)
                    enhanced_prompt += f"\n\nWeather data: {tool_result}"

        # Generate response with context
        response = self.model.generate_content(enhanced_prompt)
        return response.text

# Use agent with tools
agent = GoogleADKAgent()
result = agent.run_with_tools("What's the weather in San Francisco?")
```

---

## Multi-Agent System

### Collaborative Agents

```python
class MultiAgentSystem:
    """Multi-agent system with specialized roles."""

    def __init__(self):
        # Research Agent
        self.research_agent = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction="You are a research specialist. Gather comprehensive information."
        )

        # Analysis Agent
        self.analysis_agent = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction="You are an analyst. Extract key insights and patterns."
        )

        # Writer Agent
        self.writer_agent = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction="You are a technical writer. Create clear summaries."
        )

    def run_workflow(self, topic: str):
        """Run multi-agent workflow."""
        # Step 1: Research
        research_prompt = f"Research key information about: {topic}"
        research_result = self.research_agent.generate_content(research_prompt)

        # Step 2: Analysis
        analysis_prompt = f"Analyze: {research_result.text}"
        analysis_result = self.analysis_agent.generate_content(analysis_prompt)

        # Step 3: Writing
        writing_prompt = f"Summarize: {analysis_result.text}"
        final_result = self.writer_agent.generate_content(writing_prompt)

        return {
            "research": research_result.text,
            "analysis": analysis_result.text,
            "summary": final_result.text
        }

# Use multi-agent system
system = MultiAgentSystem()
result = system.run_workflow("Quantum Computing")
```

---

## Evaluation with Custom-Evals

### Comprehensive Evaluation

```python
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM

# Run agent
model = genai.GenerativeModel('gemini-1.5-flash')
query = "Explain machine learning"
response = model.generate_content(query)
answer = response.text

# Evaluate
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

evaluators = {
    "coherence": CoherenceEvaluator(eval_llm),
    "relevance": RelevanceEvaluator(eval_llm),
    "correctness": CorrectnessEvaluator(eval_llm),
    "toxicity": ToxicityEvaluator(eval_llm)
}

scores = {}
for name, evaluator in evaluators.items():
    score = evaluator.evaluate({
        "input": query,
        "output": answer
    })
    scores[name] = score
    print(f"{name.capitalize()}: {score.label} ({score.score:.2f})")
```

---

## Testing Examples

### Test Simple Agent

```python
def test_simple_agent():
    """Test basic agent functionality."""
    agent = GoogleADKAgent("SimpleAgent")

    query = "What is deep learning?"
    result = agent.run(query, "You are a helpful assistant.")

    assert result["success"]
    assert len(result["response"]) > 0

    scores = agent.evaluate(query, result["response"])
    assert scores["coherence"].score >= 0.7

def test_tool_integration():
    """Test agent with tools."""
    agent = GoogleADKAgent("ToolAgent")

    query = "What's the weather in Tokyo?"
    result = agent.run_with_tools(query)

    assert result["success"]
    assert len(result["tool_calls"]) > 0
    assert any("weather" in tc["tool"].lower() for tc in result["tool_calls"])
```

---

## Best Practices

### 1. Clear System Instructions

```python
# Good: Specific and detailed
system_instruction = """You are an AI coding assistant.
- Provide code examples with explanations
- Follow Python best practices
- Include error handling
- Add comments for clarity"""

# Avoid: Vague instructions
system_instruction = "You help with code"
```

### 2. Model Selection

```python
# For quick responses: gemini-1.5-flash
model = genai.GenerativeModel('gemini-1.5-flash')

# For complex tasks: gemini-1.5-pro
model = genai.GenerativeModel('gemini-1.5-pro')
```

### 3. Error Handling

```python
def run_agent_safely(model, prompt, max_retries=3):
    """Run agent with error handling."""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Retry {attempt + 1}: {e}")
            time.sleep(2 ** attempt)
```

### 4. Content Safety

```python
# Configure safety settings
from google.generativeai.types import HarmCategory, HarmBlockThreshold

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
)
```

---

## Use Cases

### Technical Support Bot

```python
support_agent = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction="""You are a technical support specialist.
    Help users troubleshoot issues step-by-step.
    """
)
```

### Content Generator

```python
content_agent = genai.GenerativeModel(
    'gemini-1.5-pro',
    system_instruction="""You are a content creator.
    Generate engaging, informative content.
    """
)
```

### Research Assistant

```python
research_agent = genai.GenerativeModel(
    'gemini-1.5-pro',
    system_instruction="""You are a research assistant.
    Provide comprehensive, well-sourced information.
    """
)
```

---

## Quality Gates

```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
    "correctness": 0.7,
    "toxicity": 0.2
}

def validate_agent_output(query, response, scores):
    """Validate agent output quality."""
    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric in scores:
            if metric == "toxicity":
                if scores[metric].score > threshold:
                    return False, f"High {metric}"
            else:
                if scores[metric].score < threshold:
                    return False, f"Low {metric}"

    return True, "All checks passed"
```

---

## Troubleshooting

### Issue: API quota exceeded

**Solution**: Monitor usage and implement rate limiting

```python
import time

def rate_limited_call(model, prompt, delay=1):
    """Call with rate limiting."""
    time.sleep(delay)
    return model.generate_content(prompt)
```

### Issue: Long response times

**Solution**: Use gemini-1.5-flash for faster responses

```python
# Faster model for simple tasks
model = genai.GenerativeModel('gemini-1.5-flash')
```

### Issue: Content filtering blocks

**Solution**: Adjust safety settings or rephrase prompt

```python
# More permissive settings (use carefully)
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }
)
```

---

## Resources

- **Official Docs**: https://ai.google.dev/docs
- **Gemini API**: https://ai.google.dev/gemini-api
- **API Key**: https://makersuite.google.com/app/apikey
- **Example File**: `examples/google_adk_agent_example.py`

---

## Next Steps

1. Install: `pip install google-generativeai`
2. Get API key from Google AI Studio
3. Run example: `python examples/google_adk_agent_example.py`
4. Create your first agent
5. Experiment with multi-agent workflows

**See Also**:
- [Google Vertex AI](google-vertex.md) - Enterprise Vertex AI agents
- [OpenAI Agents](openai-agents-framework.md) - OpenAI's agent framework
- [Multi-Agent System](multi-agent.md) - Custom multi-agent orchestration
