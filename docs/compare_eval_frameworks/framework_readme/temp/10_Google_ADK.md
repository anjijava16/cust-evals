# Google ADK (Agent Development Kit): CLI-First Agent Evaluation

**Type**: Python Framework + CLI | **License**: Open Source (Apache 2.0) | **Year**: 2024

---

## Quick Overview

Google ADK (Agent Development Kit) is **Google's official framework for building and evaluating LLM agents**, with a strong focus on agent behavior, tool trajectory analysis, and CLI-driven workflows. It's specifically designed for developers building agentic systems that use tools and follow multi-step reasoning.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | Agent evaluation + tool usage |
| **Setup Time** | ⚡ 10-15 minutes |
| **Learning Curve** | Medium |
| **Dependencies** | Google Cloud (optional), Pytest |
| **Cost** | Free (OSS) + optional Vertex AI |
| **Best For** | Agent developers, Gemini users |

---

## Key Strengths

### ✅ Advantages

1. **Agent-First Design**
   - Built specifically for agentic systems
   - **Tool trajectory tracking** - monitors exact sequence of tool calls
   - Multi-turn conversation evaluation
   - State management across agent steps
   - Action sequence validation

2. **Unique Tool Trajectory Metrics**
   - **tool_trajectory_avg_score**: Exact tool call sequence matching
   - Validates correct tool selection
   - Checks parameter accuracy
   - Evaluates reasoning path quality
   - Detects inefficient tool usage patterns

3. **Three Evaluation Modes**
   - **Test Files** (.test.json): Fast unit tests for active development
   - **Evalset Files**: Complex multi-turn integration tests
   - **Web UI** (`adk web`): Interactive evaluation with trace debugging
   - **Pytest Integration**: Programmatic testing
   - **CLI** (`adk eval`): Automated command-line evaluation

4. **Gemini-Native Integration**
   - Built for Gemini models
   - Seamless Vertex AI integration (optional)
   - Function calling optimized for Gemini
   - Uses Gemini for LLM-as-judge evaluation

5. **Comprehensive Metrics Suite**
   - **Tool Metrics**: trajectory, usage quality, correctness
   - **Response Metrics**: ROUGE-1 similarity, semantic matching
   - **LLM-Judged**: Custom rubrics, hallucination detection
   - **Safety Metrics**: Harmlessness assessment

6. **User Simulation**
   - Dynamic user prompt generation
   - Variable interaction patterns
   - Multi-turn conversation testing
   - Realistic agent testing scenarios

7. **Developer-Friendly**
   - CLI-first workflow
   - Interactive web debugger
   - Pydantic-backed schemas
   - Type-safe evaluation definitions
   - Hot reload for rapid iteration

### ⚠️ Limitations

1. **Agent-Only Focus**
   - Not suitable for simple Q&A systems
   - No RAG-specific metrics
   - Limited for non-agentic use cases
   - Requires tool-using agents

2. **Gemini Ecosystem Bias**
   - Optimized for Gemini models
   - Best with Google's tools
   - Less tested with other LLM providers
   - Vertex AI recommended for full features

3. **Maturity & Documentation**
   - Relatively new framework (2024)
   - Limited community resources
   - Fewer examples than established frameworks
   - Academic-style documentation
   - Smaller ecosystem

4. **Vertex AI Dependency (Optional)**
   - Full features require Vertex AI Evaluation Service
   - Evalset files need GCP API
   - Local-only mode has limitations
   - Internet connectivity for advanced metrics

5. **Learning Curve**
   - More complex than simple eval frameworks
   - Requires understanding of agent architectures
   - Tool trajectory concepts need learning
   - Multiple evaluation modes to master

6. **Limited Non-Agent Metrics**
   - No code evaluation
   - Limited general LLM metrics
   - Focused on tool usage
   - Not comprehensive for all use cases

---

## vs Other Frameworks

### vs Custom-Evals

| Aspect | Google ADK | Custom-Evals |
|--------|------------|--------------|
| **Focus** | Agents + tools | General + RAG + Code |
| **Tool Trajectory** | ✅✅ Core feature | ❌ No |
| **Agent Metrics** | ✅✅ Best | ✅ Good |
| **CLI Tools** | ✅✅ Excellent | ⚠️ Basic |
| **Web UI** | ✅ Interactive | ❌ No |
| **Multi-Framework** | Gemini-focused | 17+ providers |
| **RAG Metrics** | ❌ Limited | ✅ Good |

**Choose ADK if**: You're building Gemini-powered agents with complex tool usage

**Choose Custom-Evals if**: You need flexibility across providers or non-agent evaluation

---

### vs DeepEval

| Aspect | Google ADK | DeepEval |
|--------|------------|----------|
| **Agent Focus** | ✅✅ Core | ⚠️ Basic |
| **Tool Trajectory** | ✅✅ Yes | ❌ No |
| **Pytest Integration** | ✅ Yes | ✅✅ Native |
| **Web UI** | ✅ Built-in | ❌ No |
| **CLI** | ✅✅ Excellent | ⚠️ Basic |
| **Gemini Support** | ✅✅ Native | ⚠️ Manual |
| **General Eval** | ⚠️ Limited | ✅ Comprehensive |

**Choose ADK if**: Building complex agents with tool chains

**Choose DeepEval if**: Need comprehensive pytest-based evaluation framework

---

### vs LangSmith

| Aspect | Google ADK | LangSmith |
|--------|------------|-----------|
| **Agent Tracing** | ✅ Good | ✅✅ Excellent |
| **Tool Analysis** | ✅✅ Deep | ✅ Good |
| **Web UI** | ✅ Local | ✅✅ Cloud |
| **Cost** | Free + optional GCP | Subscription |
| **LangChain** | Manual | ✅✅ Native |
| **Gemini Focus** | ✅✅ Native | ⚠️ Generic |
| **Production Monitoring** | ❌ No | ✅✅ Yes |

**Choose ADK if**: Building Gemini agents, want local-first development

**Choose LangSmith if**: Need production monitoring with LangChain ecosystem

---

## When to Choose Google ADK

### ✅ Perfect For

1. **Agent Development**
   - Building multi-step reasoning agents
   - Agents that use multiple tools
   - Complex decision-making systems
   - Autonomous task execution

2. **Tool Usage Validation**
   - Evaluating tool selection accuracy
   - Validating parameter passing
   - Testing tool call sequences
   - Optimizing agent reasoning paths

3. **Gemini-Based Systems**
   - Using Gemini models (Pro, Flash)
   - Leveraging Gemini function calling
   - GCP-hosted applications
   - Vertex AI deployments

4. **CLI-Driven Workflows**
   - Command-line development
   - CI/CD pipeline integration
   - Automated testing
   - Rapid iteration cycles

5. **Interactive Debugging**
   - Visual trace debugging
   - Step-by-step agent inspection
   - Tool call visualization
   - Multi-turn conversation analysis

### ❌ Not Ideal For

1. **Non-Agent Applications**
   - Simple Q&A systems
   - Basic text generation
   - RAG-only systems without tools
   - Single-response evaluations

2. **Multi-Provider Flexibility**
   - Using multiple LLM providers
   - Need provider-agnostic evaluation
   - Testing across OpenAI, Anthropic, etc.
   - Cloud-agnostic requirements

3. **Production Monitoring**
   - Real-time observability needs
   - Production trace collection
   - Long-term metric storage
   - Alert systems

4. **RAG-Specific Evaluation**
   - Need specialized RAG metrics
   - Retrieval quality focus
   - Faithfulness evaluation
   - Context precision/recall

5. **Established Framework Needs**
   - Want mature, battle-tested tools
   - Need extensive documentation
   - Require large community
   - Want many examples

---

## Pricing

### Cost Breakdown

| Component | Cost |
|-----------|------|
| **ADK Framework** | 💰 **Free** (Apache 2.0) |
| **Test Files Mode** | Free (local execution) |
| **Vertex AI API** (optional) | Pay-per-use for Evalset |
| **Gemini API** | Standard Gemini pricing |
| **Infrastructure** | None (local-first) |

### Detailed Cost Analysis

#### Local Mode (Test Files)
- **Framework**: Free
- **Execution**: Local compute only
- **Storage**: Local filesystem
- **Cost**: $0

#### Vertex AI Mode (Evalset Files)
- **Evaluation API**: Gemini 2.5 Flash throughput
- **Per evaluation**: ~$0.001-0.003
- **Multiple metrics**: ~$0.005-0.015 per sample

#### Monthly Cost Estimates (Vertex AI Mode)

| Evaluations/Month | Local Only | With Vertex AI |
|-------------------|------------|----------------|
| 1,000 | $0 | $5-15 |
| 10,000 | $0 | $50-150 |
| 100,000 | $0 | $500-1,500 |

### Cost Optimization Tips

1. **Use Test Files for development** - Free and fast
2. **Evalset for integration testing** - Only when needed
3. **Local-first workflow** - Minimize API calls
4. **Batch evaluations** - More efficient processing
5. **Sample datasets** - Test on subsets first

---

## Quick Start

### Installation

```bash
# Install Google ADK
pip install google-adk

# Verify installation
adk --version

# Optional: Set up Vertex AI (for Evalset files)
export GOOGLE_CLOUD_PROJECT=your-project-id
gcloud auth application-default login
```

### 5-Minute Example

```python
# my_agent.py - Simple agent definition
from google.adk import Agent, tool

@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"The weather in {location} is sunny, 72°F"

@tool
def convert_temperature(temp_f: float, to_unit: str) -> str:
    """Convert temperature between units."""
    if to_unit == "celsius":
        return f"{(temp_f - 32) * 5/9:.1f}°C"
    return f"{temp_f}°F"

agent = Agent(
    name="weather_agent",
    model="gemini-1.5-flash",
    tools=[get_weather, convert_temperature],
    instructions="Help users with weather information."
)
```

```json
// weather_test.test.json - Test file
{
  "cases": [
    {
      "name": "Weather Query with Conversion",
      "user_prompt": "What's the weather in San Francisco in Celsius?",
      "expected_tools": [
        {
          "name": "get_weather",
          "parameters": {"location": "San Francisco"}
        },
        {
          "name": "convert_temperature",
          "parameters": {"temp_f": 72, "to_unit": "celsius"}
        }
      ],
      "expected_response_contains": ["22", "celsius", "San Francisco"]
    }
  ]
}
```

```bash
# Run evaluation
adk eval my_agent.py weather_test.test.json

# Output:
# ✓ Weather Query with Conversion
#   tool_trajectory_avg_score: 1.000
#   response_match_score: 0.950
#   Status: PASSED
```

---

## Advanced Usage Examples

### 1. Tool Trajectory Evaluation

```python
# complex_agent.py
from google.adk import Agent, tool

@tool
def search_database(query: str) -> str:
    """Search the knowledge database."""
    return f"Found 5 results for: {query}"

@tool
def filter_results(results: str, criteria: str) -> str:
    """Filter search results."""
    return f"Filtered results by {criteria}"

@tool
def summarize(content: str) -> str:
    """Summarize content."""
    return f"Summary: {content[:100]}"

agent = Agent(
    name="research_agent",
    model="gemini-1.5-pro",
    tools=[search_database, filter_results, summarize],
    instructions="Research topics by searching, filtering, and summarizing."
)
```

```json
// trajectory_test.test.json
{
  "cases": [
    {
      "name": "Multi-Step Research",
      "user_prompt": "Find and summarize recent AI papers about transformers",
      "expected_tools": [
        {
          "name": "search_database",
          "parameters": {"query": "AI transformers recent"}
        },
        {
          "name": "filter_results",
          "parameters": {"criteria": "recent"}
        },
        {
          "name": "summarize"
        }
      ],
      "validate_tool_order": true,
      "check_all_tools_used": true
    }
  ]
}
```

```bash
# Evaluate tool trajectory
adk eval complex_agent.py trajectory_test.test.json --print_detailed_results

# Output shows:
# ✓ All expected tools called
# ✓ Correct tool order
# ✓ Valid parameters
# Tool trajectory score: 1.000
```

---

### 2. Interactive Web UI Debugging

```bash
# Start web UI for interactive evaluation
adk web my_agent.py

# Browser opens at http://localhost:8080
# Features:
# - Interactive chat interface
# - Real-time tool call visualization
# - Step-by-step trace debugging
# - Parameter inspection
# - Response analysis
```

**Web UI Features:**
- Chat with your agent in real-time
- See each tool call as it happens
- Inspect tool parameters and results
- Visualize reasoning paths
- Debug agent behavior interactively
- Export traces for analysis

---

### 3. Pytest Integration

```python
# test_agent.py
import pytest
from google.adk.evaluation import evaluate_agent

def test_weather_agent_basic():
    """Test basic weather query."""
    result = evaluate_agent(
        agent_path="my_agent.py",
        test_cases=[{
            "user_prompt": "What's the weather in NYC?",
            "expected_tools": [{"name": "get_weather"}]
        }]
    )

    assert result.tool_trajectory_score > 0.9
    assert "New York" in result.response or "NYC" in result.response


def test_weather_agent_multi_turn():
    """Test multi-turn conversation."""
    result = evaluate_agent(
        agent_path="my_agent.py",
        test_cases=[{
            "turns": [
                {
                    "user": "What's the weather in Boston?",
                    "expected_tools": [{"name": "get_weather"}]
                },
                {
                    "user": "Convert that to Celsius",
                    "expected_tools": [{"name": "convert_temperature"}]
                }
            ]
        }]
    )

    assert result.overall_score > 0.85


@pytest.mark.parametrize("location", ["Seattle", "Austin", "Miami"])
def test_weather_multiple_locations(location):
    """Test weather queries for multiple locations."""
    result = evaluate_agent(
        agent_path="my_agent.py",
        test_cases=[{
            "user_prompt": f"What's the weather in {location}?",
            "expected_tools": [{"name": "get_weather"}]
        }]
    )

    assert result.tool_trajectory_score == 1.0
    assert location in result.response
```

```bash
# Run pytest tests
pytest test_agent.py -v

# Output:
# test_agent.py::test_weather_agent_basic PASSED
# test_agent.py::test_weather_agent_multi_turn PASSED
# test_agent.py::test_weather_multiple_locations[Seattle] PASSED
# test_agent.py::test_weather_multiple_locations[Austin] PASSED
# test_agent.py::test_weather_multiple_locations[Miami] PASSED
```

---

### 4. Evalset with LLM-Judged Metrics (Vertex AI)

```json
// comprehensive_evalset.json
{
  "eval_cases": [
    {
      "name": "Customer Support Agent",
      "scenario": "Handle customer product inquiry",
      "user_prompts": [
        "I need help with my order",
        "Order #12345",
        "Can you check the status?"
      ],
      "evaluation_criteria": {
        "tool_trajectory_avg_score": {
          "expected_tools": [
            {"name": "lookup_order"},
            {"name": "check_status"},
            {"name": "format_response"}
          ]
        },
        "rubric_based_tool_use_quality_v1": {
          "rubric": "Agent should use appropriate tools in logical order"
        },
        "final_response_match_v2": {
          "expected_response": "Order #12345 is currently in transit"
        },
        "hallucinations_v1": {
          "context": "Order database information"
        }
      }
    }
  ]
}
```

```bash
# Run evalset with Vertex AI
adk eval my_agent.py comprehensive_evalset.json \
  --config_file_path=vertex_config.yaml \
  --print_detailed_results

# Outputs comprehensive metrics:
# - Tool trajectory accuracy
# - Tool usage quality (LLM-judged)
# - Response semantic matching
# - Hallucination detection
# - Safety assessment
```

---

### 5. Custom Rubric Evaluation

```python
# rubric_eval.py
from google.adk.evaluation import EvalSet, EvalCase

# Define custom evaluation rubric
custom_rubric = """
Evaluate the agent's performance on:

1. Tool Selection (40%)
   - Did agent choose optimal tools?
   - Were tools used in logical order?
   - Any unnecessary tool calls?

2. Parameter Accuracy (30%)
   - Were parameters correctly extracted?
   - Proper data type usage?
   - No missing required parameters?

3. Response Quality (30%)
   - Complete answer to user query?
   - Information accurately sourced from tools?
   - Professional and clear communication?

Score 1-5 for each category.
Provide overall score and justification.
"""

eval_case = EvalCase(
    name="Rubric-Based Evaluation",
    user_prompt="Find me a good Italian restaurant in Boston",
    evaluation_criteria={
        "rubric_based_final_response_quality_v1": {
            "rubric": custom_rubric
        }
    }
)

# Run evaluation
result = evaluate_agent("my_agent.py", eval_case)

print(f"Overall Score: {result.rubric_score}/5")
print(f"Tool Selection: {result.rubric_breakdown['tool_selection']}/5")
print(f"Parameters: {result.rubric_breakdown['parameters']}/5")
print(f"Response: {result.rubric_breakdown['response']}/5")
print(f"\nJustification:\n{result.rubric_justification}")
```

---

### 6. User Simulation for Variable Testing

```json
// user_simulation_evalset.json
{
  "eval_cases": [
    {
      "name": "Booking Agent - Variable Interactions",
      "scenario": {
        "type": "booking",
        "user_personas": ["impatient", "detail-oriented", "confused"],
        "dynamic_prompts": true
      },
      "conversation_flow": {
        "min_turns": 3,
        "max_turns": 10,
        "user_simulation": {
          "vary_politeness": true,
          "vary_clarity": true,
          "inject_edge_cases": true
        }
      },
      "evaluation_criteria": {
        "tool_trajectory_avg_score": {},
        "rubric_based_tool_use_quality_v1": {
          "rubric": "Agent handles variable user behavior gracefully"
        },
        "safety_v1": {}
      }
    }
  ]
}
```

This enables testing agents against:
- Variable user communication styles
- Different levels of detail in requests
- Edge cases and unexpected inputs
- Realistic conversation patterns

---

### 7. CI/CD Integration

```yaml
# .github/workflows/agent_eval.yml
name: Agent Evaluation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  evaluate:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install google-adk
        pip install -r requirements.txt

    - name: Run agent evaluations
      run: |
        # Fast unit tests
        adk eval agents/customer_support.py tests/basic.test.json

        # Comprehensive integration tests
        adk eval agents/customer_support.py tests/integration.test.json \
          --print_detailed_results

    - name: Run pytest tests
      run: |
        pytest tests/test_agents.py -v --junit-xml=results.xml

    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: evaluation-results
        path: results.xml
```

---

## Architecture Highlights

### Design Principles

1. **Agent-First**: Built for multi-step tool-using agents
2. **CLI-Driven**: Command-line workflow for developers
3. **Local-First**: Fast iteration without cloud dependency
4. **Type-Safe**: Pydantic schemas for evaluation definitions
5. **Interactive**: Web UI for debugging and exploration

### Evaluation Modes Comparison

| Mode | Speed | Features | Use Case |
|------|-------|----------|----------|
| **Test Files** | ⚡ Fast | Basic validation | Active development |
| **Evalset** | Medium | Full metrics | Integration testing |
| **Web UI** | Interactive | Visual debugging | Investigation |
| **Pytest** | Fast | Programmatic | CI/CD pipelines |
| **CLI** | Fast | Automated | Scripts & automation |

### Core Metrics Explained

#### Tool Trajectory Metrics

**tool_trajectory_avg_score**:
- Exact tool call sequence matching
- Validates correct tools are called
- Checks tool order accuracy
- Verifies parameters
- Score: 0-1 (1 = perfect match)

**rubric_based_tool_use_quality_v1**:
- LLM-judged tool usage quality
- Evaluates tool selection logic
- Assesses parameter appropriateness
- Checks for unnecessary calls
- Score: 1-5

#### Response Metrics

**response_match_score**:
- ROUGE-1 similarity to expected response
- Keyword overlap measurement
- Fast statistical comparison
- Score: 0-1

**final_response_match_v2**:
- LLM-judged semantic equivalence
- Understands paraphrasing
- More nuanced than ROUGE
- Score: 0-1

#### Quality Metrics

**rubric_based_final_response_quality_v1**:
- Custom quality criteria evaluation
- Define your own rubrics
- Multi-dimensional scoring
- Detailed justifications
- Score: 1-5

**hallucinations_v1**:
- Groundedness in tool outputs
- Detects fabricated information
- Checks citation accuracy
- Score: 0-1 (higher = less hallucination)

**safety_v1**:
- Harmlessness assessment
- Toxicity detection
- Inappropriate content check
- Score: 0-1 (higher = safer)

---

## Comparison Summary

### Unique Advantages

1. ⭐ **Tool Trajectory Analysis** - Best-in-class for agent tool usage
2. 🛠️ **Agent-First Design** - Purpose-built for agentic systems
3. 💻 **CLI Excellence** - Developer-friendly command-line workflow
4. 🌐 **Interactive Web UI** - Visual debugging and exploration
5. 🔧 **Pytest Integration** - Programmatic testing support
6. 🤖 **Gemini Native** - Optimized for Google's models

### Trade-offs

1. Agent-only focus (limited general eval)
2. Relatively new (smaller community)
3. Gemini ecosystem bias
4. Vertex AI needed for full features
5. Limited RAG-specific metrics
6. Documentation gaps

### Google ADK vs The Competition

| Feature | ADK | Custom-Evals | DeepEval | LangSmith | RAGAS |
|---------|-----|--------------|----------|-----------|-------|
| **Agent Focus** | ✅✅ | ✅ | ⚠️ | ✅ | ❌ |
| **Tool Trajectory** | ✅✅ | ❌ | ❌ | ⚠️ | ❌ |
| **CLI Tools** | ✅✅ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| **Web UI** | ✅ | ❌ | ❌ | ✅✅ | ❌ |
| **Gemini** | ✅✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| **RAG Metrics** | ❌ | ✅ | ✅ | ✅ | ✅✅ |
| **General Eval** | ⚠️ | ✅ | ✅ | ✅ | ❌ |

---

## Real-World Use Cases

### 1. Customer Support Agent Validation

```bash
# Evaluate customer support agent across multiple scenarios
adk eval agents/customer_support.py evalsets/support_scenarios.json \
  --print_detailed_results

# Validates:
# - Order lookup → status check → response formatting
# - Refund processing → approval check → confirmation
# - Product questions → search → answer generation
```

---

### 2. Research Assistant Agent

```python
# research_agent.py - Multi-tool research agent
@tool
def web_search(query: str) -> List[str]:
    """Search the web for information."""
    pass

@tool
def extract_facts(content: str) -> List[str]:
    """Extract key facts from content."""
    pass

@tool
def synthesize_report(facts: List[str]) -> str:
    """Synthesize facts into coherent report."""
    pass

agent = Agent(
    name="research_assistant",
    model="gemini-1.5-pro",
    tools=[web_search, extract_facts, synthesize_report],
    instructions="Research topics and create comprehensive reports"
)
```

Evaluation validates:
- Correct tool ordering (search → extract → synthesize)
- No information fabrication
- Complete coverage of topic
- Clear, well-structured reports

---

## Resources

### Official Documentation
- **Main Docs**: https://google.github.io/adk-docs/
- **Evaluation Guide**: https://google.github.io/adk-docs/evaluate/
- **CLI Reference**: https://google.github.io/adk-docs/cli/
- **API Docs**: https://google.github.io/adk-docs/api/

### Code & Examples
- **GitHub**: https://github.com/google/adk-python
- **Examples**: https://github.com/google/adk-python/tree/main/examples
- **Local Example**: `docs/compare_eval_frameworks/google_adk_eval_example.py`
- **Schemas**: https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/

### Community
- **Issue Tracker**: https://github.com/google/adk-python/issues
- **Discussions**: https://github.com/google/adk-python/discussions

### Related Tools
- **Vertex AI**: https://cloud.google.com/vertex-ai
- **Gemini API**: https://ai.google.dev/
- **Google Cloud SDK**: https://cloud.google.com/sdk

---

## Verdict

**Google ADK is the premier choice for developers building sophisticated agent systems with Gemini, offering unmatched tool trajectory analysis and CLI-driven workflows specifically designed for agentic applications.**

**Rating**: ⭐⭐⭐⭐ (4/5 for agent developers, 2/5 for non-agent use)

### Choose Google ADK if you value:
- ✅ Agent-first evaluation
- ✅ Tool trajectory analysis
- ✅ CLI-driven workflows
- ✅ Interactive debugging UI
- ✅ Gemini integration
- ✅ Local-first development

### Choose alternatives if you need:
- ❌ General LLM evaluation → Custom-Evals, DeepEval
- ❌ RAG-specific metrics → RAGAS
- ❌ Production observability → LangSmith, Phoenix
- ❌ Multi-provider flexibility → Custom-Evals
- ❌ Mature ecosystem → Established frameworks
- ❌ Non-agent applications → General frameworks

---

## Decision Matrix

### Use Google ADK when:
✅ Building agentic systems
✅ Need tool trajectory validation
✅ Using Gemini models
✅ Want CLI-driven workflows
✅ Need interactive debugging
✅ Developing multi-step reasoning agents

### Don't use Google ADK when:
❌ Simple Q&A systems
❌ RAG-only applications
❌ Need multi-provider support
❌ Production monitoring focus
❌ Want mature, established tools
❌ Non-tool-using applications

---

## Quick Reference Card

```bash
# Installation
pip install google-adk

# Create test file
cat > my_test.test.json << EOF
{
  "cases": [{
    "name": "Basic Test",
    "user_prompt": "Hello",
    "expected_response_contains": ["hi", "hello"]
  }]
}
EOF

# Run evaluation
adk eval my_agent.py my_test.test.json

# Interactive debugging
adk web my_agent.py

# Pytest integration
pytest test_agents.py -v

# Core Metrics
tool_trajectory_avg_score          # Tool sequence accuracy
rubric_based_tool_use_quality_v1   # Tool usage quality
final_response_match_v2            # Response semantic match
hallucinations_v1                  # Groundedness check
safety_v1                          # Safety assessment

# Cost: Free (local) + optional Vertex AI ($0.001-0.003/eval)
```

---

**Next Steps**:
1. [Try the Example Code](google_adk_eval_example.py)
2. [Compare All Frameworks](Compare_All_Eval_Frameworks.md)
3. [View Framework Index](FRAMEWORKS_INDEX.md)

**Related**:
- [Custom-Evals Comparison](01_Custom_Evals.md)
- [Vertex AI Comparison](05_Google_Vertex_AI.md)
- [DeepEval Comparison](08_DeepEval.md)

---

*Last Updated: January 2026*
*Google ADK Version: Latest*
*Maintained by: Custom-Evals Team*
