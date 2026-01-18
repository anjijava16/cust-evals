"""
Microsoft Agent Framework Example with Custom Evals Testing

This example demonstrates:
1. Building agents with Microsoft's Agent Framework
2. Multi-agent orchestration and collaboration
3. Tool integration and state management
4. Conversation management and context
5. Evaluating agent outputs with custom-evals

Microsoft Agent Framework provides production-ready agent capabilities.

Requirements:
- microsoft-agents (pip install microsoft-agents)
- azure-ai-agents (pip install azure-ai-agents)
"""

import os
import json
from typing import Dict, Any, List, Optional

try:
    from microsoft_agents import Agent, AgentConfig, Tool
    from microsoft_agents.runtime import AgentRuntime
    MICROSOFT_AGENTS_AVAILABLE = True
except ImportError:
    MICROSOFT_AGENTS_AVAILABLE = False
    print("⚠️  Microsoft Agent Framework not installed. Install with: pip install microsoft-agents")

# Custom Evals imports
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator,
    HallucinationEvaluator
)
from custom.evals.llm import LLM

# Optional: Initialize Phoenix tracing
try:
    from custom.evals import initialize_tracing
    initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")
    print("✅ Phoenix tracing enabled")
except:
    print("ℹ️  Phoenix tracing not available (optional)")


# ============================================================================
# STEP 1: Define Tools for Microsoft Agents
# ============================================================================

class WeatherTool(Tool):
    """Tool for weather information."""

    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get current weather for a location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name (e.g., 'San Francisco')"
                    }
                },
                "required": ["location"]
            }
        )

    def execute(self, location: str) -> str:
        """Execute weather lookup."""
        weather_data = {
            "San Francisco": "Sunny, 72°F",
            "New York": "Cloudy, 65°F",
            "London": "Rainy, 55°F",
            "Tokyo": "Clear, 68°F"
        }
        return weather_data.get(location, f"Weather data not available for {location}")


class SearchTool(Tool):
    """Tool for knowledge base search."""

    def __init__(self):
        super().__init__(
            name="search_knowledge",
            description="Search knowledge base for information",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        )

    def execute(self, query: str) -> str:
        """Execute search."""
        knowledge = {
            "microsoft": "Microsoft is a technology company known for Windows, Azure, and AI services.",
            "azure": "Azure is Microsoft's cloud computing platform.",
            "ai": "Artificial intelligence enables machines to perform tasks that typically require human intelligence.",
            "dotnet": ".NET is a free, open-source developer platform for building applications."
        }

        query_lower = query.lower()
        for key, value in knowledge.items():
            if key in query_lower:
                return value

        return f"No information found for: {query}"


class CalculatorTool(Tool):
    """Tool for calculations."""

    def __init__(self):
        super().__init__(
            name="calculate",
            description="Calculate mathematical expressions",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression (e.g., '25 * 4')"
                    }
                },
                "required": ["expression"]
            }
        )

    def execute(self, expression: str) -> str:
        """Execute calculation."""
        try:
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error: {str(e)}"


# ============================================================================
# STEP 2: Microsoft Agent System
# ============================================================================

class MicrosoftAgentSystem:
    """Agent system using Microsoft Agent Framework."""

    def __init__(self, model: str = "gpt-4o-mini"):
        if not MICROSOFT_AGENTS_AVAILABLE:
            raise ImportError("Microsoft Agent Framework required")

        # Create agent config
        config = AgentConfig(
            name="assistant",
            instructions="You are a helpful assistant with access to tools. Use them to provide accurate information.",
            model=model,
            tools=[
                WeatherTool(),
                SearchTool(),
                CalculatorTool()
            ]
        )

        # Create agent
        self.agent = Agent(config=config)

        # Create runtime
        self.runtime = AgentRuntime(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, message: str) -> Dict[str, Any]:
        """Run agent on a message."""
        try:
            # Run agent
            result = self.runtime.run(agent=self.agent, input=message)

            return {
                "success": True,
                "response": result.output,
                "tool_calls": result.tool_calls if hasattr(result, 'tool_calls') else [],
                "agent": "assistant"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def evaluate(self, query: str, response: str, expected: str = None) -> Dict[str, Any]:
        """Evaluate agent response using custom-evals."""
        scores = {}

        for name, evaluator in self.evaluators.items():
            eval_input = {"input": query, "output": response}

            if name == "correctness" and expected:
                eval_input["expected"] = expected

            score = evaluator.evaluate(eval_input)
            scores[name] = score

        return scores


# ============================================================================
# STEP 3: Multi-Agent Collaboration System
# ============================================================================

class MultiAgentMicrosoftSystem:
    """Multi-agent collaboration using Microsoft Agent Framework."""

    def __init__(self):
        if not MICROSOFT_AGENTS_AVAILABLE:
            raise ImportError("Microsoft Agent Framework required")

        # Create specialized agents
        research_config = AgentConfig(
            name="researcher",
            instructions="You are a research specialist. Gather comprehensive information.",
            model="gpt-4o-mini",
            tools=[SearchTool()]
        )
        self.research_agent = Agent(config=research_config)

        analysis_config = AgentConfig(
            name="analyst",
            instructions="You are an analysis expert. Extract key insights and patterns.",
            model="gpt-4o-mini"
        )
        self.analysis_agent = Agent(config=analysis_config)

        writer_config = AgentConfig(
            name="writer",
            instructions="You are a technical writer. Create clear, concise summaries.",
            model="gpt-4o-mini"
        )
        self.writer_agent = Agent(config=writer_config)

        # Create runtime
        self.runtime = AgentRuntime(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm)
        }

    def run_workflow(self, topic: str) -> Dict[str, Any]:
        """Run multi-agent workflow."""
        try:
            # Step 1: Research
            research_result = self.runtime.run(
                agent=self.research_agent,
                input=f"Research information about: {topic}"
            )

            # Step 2: Analysis
            analysis_result = self.runtime.run(
                agent=self.analysis_agent,
                input=f"Analyze this research: {research_result.output}"
            )

            # Step 3: Writing
            writing_result = self.runtime.run(
                agent=self.writer_agent,
                input=f"Create a summary about {topic} based on: {analysis_result.output}"
            )

            return {
                "success": True,
                "research": research_result.output,
                "analysis": analysis_result.output,
                "final_output": writing_result.output,
                "agents_used": ["researcher", "analyst", "writer"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def evaluate(self, query: str, response: str) -> Dict[str, Any]:
        """Evaluate workflow output."""
        scores = {}

        for name, evaluator in self.evaluators.items():
            score = evaluator.evaluate({"input": query, "output": response})
            scores[name] = score

        return scores


# ============================================================================
# TESTING FUNCTIONS
# ============================================================================

def test_simple_agent():
    """Test 1: Simple agent query."""
    print("\n" + "="*80)
    print("TEST 1: Simple Microsoft Agent")
    print("="*80)

    agent = MicrosoftAgentSystem()

    query = "What is artificial intelligence?"
    print(f"\n📝 Query: {query}")

    result = agent.run(query)

    if result["success"]:
        print(f"\n✅ Response: {result['response'][:200]}...")
        print(f"🤖 Agent: {result['agent']}")

        # Evaluate
        scores = agent.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")
            print(f"    Explanation: {score.explanation[:100]}...")
    else:
        print(f"\n❌ Error: {result.get('error')}")

    return result


def test_agent_with_tools():
    """Test 2: Agent with tool usage."""
    print("\n" + "="*80)
    print("TEST 2: Microsoft Agent with Tools")
    print("="*80)

    agent = MicrosoftAgentSystem()

    query = "What's the weather in New York and calculate 50 * 20?"
    print(f"\n📝 Query: {query}")

    result = agent.run(query)

    if result["success"]:
        print(f"\n✅ Response: {result['response']}")
        print(f"\n🔧 Tool Calls: {len(result['tool_calls'])}")

        scores = agent.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")
    else:
        print(f"\n❌ Error: {result.get('error')}")

    return result


def test_multi_agent_workflow():
    """Test 3: Multi-agent workflow."""
    print("\n" + "="*80)
    print("TEST 3: Multi-Agent Microsoft Workflow")
    print("="*80)

    system = MultiAgentMicrosoftSystem()

    topic = "Azure Cloud Services"
    print(f"\n📝 Topic: {topic}")

    result = system.run_workflow(topic)

    if result["success"]:
        print(f"\n✅ Final Output: {result['final_output'][:200]}...")
        print(f"\n🤖 Agents Used: {', '.join(result['agents_used'])}")

        scores = system.evaluate(topic, result["final_output"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")
    else:
        print(f"\n❌ Error: {result.get('error')}")

    return result


def test_quality_gates():
    """Test 4: Quality gates validation."""
    print("\n" + "="*80)
    print("TEST 4: Quality Gates")
    print("="*80)

    QUALITY_THRESHOLDS = {
        "coherence": 0.7,
        "relevance": 0.7,
        "correctness": 0.7,
        "toxicity": 0.2
    }

    agent = MicrosoftAgentSystem()

    test_queries = [
        "Explain machine learning",
        "What is Microsoft Azure?",
        "Tell me about .NET"
    ]

    results = []

    for query in test_queries:
        print(f"\n📝 Query: {query}")
        result = agent.run(query)

        if result["success"]:
            scores = agent.evaluate(query, result["response"])

            passed = True
            for metric, threshold in QUALITY_THRESHOLDS.items():
                if metric in scores:
                    score_value = scores[metric].score
                    if metric == "toxicity":
                        if score_value > threshold:
                            passed = False
                            print(f"  ❌ {metric}: {score_value:.2f}")
                        else:
                            print(f"  ✅ {metric}: {score_value:.2f}")
                    else:
                        if score_value < threshold:
                            passed = False
                            print(f"  ❌ {metric}: {score_value:.2f}")
                        else:
                            print(f"  ✅ {metric}: {score_value:.2f}")

            results.append({"query": query, "passed": passed})

    print(f"\n📊 Quality Gate Summary: {sum(r['passed'] for r in results)}/{len(results)} passed")
    return results


def test_batch_evaluation():
    """Test 5: Batch evaluation."""
    print("\n" + "="*80)
    print("TEST 5: Batch Evaluation")
    print("="*80)

    agent = MicrosoftAgentSystem()

    test_cases = [
        {"query": "What is AI?", "category": "AI"},
        {"query": "Calculate 100 / 4", "category": "Math"},
        {"query": "Weather in Tokyo?", "category": "Weather"}
    ]

    results = []

    for test_case in test_cases:
        query = test_case["query"]
        print(f"\n📝 Query: {query}")

        result = agent.run(query)

        if result["success"]:
            scores = agent.evaluate(query, result["response"])
            avg_score = sum(s.score for s in scores.values()) / len(scores)

            print(f"  📈 Average score: {avg_score:.2f}")
            results.append({"query": query, "avg_score": avg_score})

    print(f"\n📊 Batch Summary:")
    print(f"  - Tests: {len(results)}")
    print(f"  - Average score: {sum(r['avg_score'] for r in results) / len(results):.2f}")

    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("Microsoft Agent Framework with Custom Evals - Complete Test Suite")
    print("="*80)

    if not MICROSOFT_AGENTS_AVAILABLE:
        print("\n❌ Microsoft Agent Framework not available.")
        print("Install with: pip install microsoft-agents")
        exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY not set. Please set your API key.")
        exit(1)

    # Run all tests
    try:
        test_simple_agent()
        test_agent_with_tools()
        test_multi_agent_workflow()
        test_quality_gates()
        test_batch_evaluation()

        print("\n" + "="*80)
        print("✅ All tests completed successfully!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
