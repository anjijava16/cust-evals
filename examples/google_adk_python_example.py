"""
Google ADK (adk-python) Example with Custom Evals Testing

This example demonstrates:
1. Building agents with Google's official ADK (adk-python)
2. Multi-agent orchestration and workflows
3. Tool integration and state management
4. Agent routing and handoffs
5. Evaluating agent outputs with custom-evals

Google ADK from: https://github.com/google/adk-python

Requirements:
- adk (pip install adk)
- google-generativeai (pip install google-generativeai)
"""

import os
import json
from typing import Dict, Any, List, Optional

try:
    from adk import Agent, Tool, Workflow
    from adk.runners import LocalRunner
    ADK_AVAILABLE = True
except ImportError:
    ADK_AVAILABLE = False
    print("⚠️  Google ADK (adk-python) not installed. Install with: pip install adk")

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("⚠️  google-generativeai not installed. Install with: pip install google-generativeai")

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
# STEP 1: Define Tools for ADK Agents
# ============================================================================

class WeatherTool(Tool):
    """Tool to get weather information."""

    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get current weather for a location"
        )

    def execute(self, location: str) -> str:
        """Get weather for location."""
        weather_data = {
            "San Francisco": "Sunny, 72°F with light breeze",
            "New York": "Cloudy, 65°F with chance of rain",
            "London": "Foggy, 55°F",
            "Tokyo": "Clear, 68°F",
            "Sydney": "Partly cloudy, 75°F"
        }
        return weather_data.get(location, f"Weather data not available for {location}")


class SearchTool(Tool):
    """Tool to search knowledge base."""

    def __init__(self):
        super().__init__(
            name="search_database",
            description="Search knowledge database for information"
        )

    def execute(self, query: str) -> str:
        """Search database."""
        database = {
            "python": "Python is a high-level programming language known for readability.",
            "machine learning": "Machine learning is a method of data analysis that automates analytical model building.",
            "neural network": "A neural network is a computational model inspired by biological neural networks.",
            "ai": "Artificial intelligence is the simulation of human intelligence by machines.",
            "cloud computing": "Cloud computing delivers computing services over the internet."
        }

        query_lower = query.lower()
        for key, value in database.items():
            if key in query_lower:
                return value

        return f"No information found for: {query}"


class CalculatorTool(Tool):
    """Tool for calculations."""

    def __init__(self):
        super().__init__(
            name="calculate",
            description="Calculate mathematical expressions"
        )

    def execute(self, expression: str) -> str:
        """Calculate expression."""
        try:
            allowed_chars = set("0123456789+-*/()., ")
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters"
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error: {str(e)}"


# ============================================================================
# STEP 2: Google ADK Agent System
# ============================================================================

class GoogleADKAgent:
    """Agent using Google ADK (adk-python)."""

    def __init__(self, model: str = "gemini-1.5-flash"):
        if not ADK_AVAILABLE:
            raise ImportError("Google ADK (adk-python) required")

        if not GENAI_AVAILABLE:
            raise ImportError("google-generativeai required")

        # Configure Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")

        genai.configure(api_key=api_key)
        self.model = model

        # Create tools
        self.tools = [
            WeatherTool(),
            SearchTool(),
            CalculatorTool()
        ]

        # Create agent
        self.agent = Agent(
            name="assistant",
            model=self.model,
            instructions="You are a helpful assistant with access to tools. Use them to provide accurate information.",
            tools=self.tools
        )

        # Create runner
        self.runner = LocalRunner()

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
            result = self.runner.run(
                agent=self.agent,
                input=message
            )

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
# STEP 3: Multi-Agent Workflow with ADK
# ============================================================================

class MultiAgentADKWorkflow:
    """Multi-agent workflow using Google ADK."""

    def __init__(self):
        if not ADK_AVAILABLE or not GENAI_AVAILABLE:
            raise ImportError("Google ADK and generativeai required")

        # Configure API
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        # Create specialized agents
        self.research_agent = Agent(
            name="researcher",
            model="gemini-1.5-flash",
            instructions="You are a research specialist. Gather comprehensive information.",
            tools=[SearchTool()]
        )

        self.analysis_agent = Agent(
            name="analyst",
            model="gemini-1.5-flash",
            instructions="You are an analysis expert. Extract insights and patterns."
        )

        self.writer_agent = Agent(
            name="writer",
            model="gemini-1.5-flash",
            instructions="You are a technical writer. Create clear, concise summaries."
        )

        # Create workflow
        self.workflow = Workflow(
            name="research_workflow",
            agents=[self.research_agent, self.analysis_agent, self.writer_agent]
        )

        self.runner = LocalRunner()

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
            research_result = self.runner.run(
                agent=self.research_agent,
                input=f"Research information about: {topic}"
            )

            # Step 2: Analysis
            analysis_result = self.runner.run(
                agent=self.analysis_agent,
                input=f"Analyze this research: {research_result.output}"
            )

            # Step 3: Writing
            writing_result = self.runner.run(
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
    print("TEST 1: Simple Google ADK Agent")
    print("="*80)

    agent = GoogleADKAgent()

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
    print("TEST 2: Google ADK Agent with Tools")
    print("="*80)

    agent = GoogleADKAgent()

    query = "What's the weather in Tokyo and calculate 25 * 8?"
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
    print("TEST 3: Multi-Agent ADK Workflow")
    print("="*80)

    workflow = MultiAgentADKWorkflow()

    topic = "Quantum Computing"
    print(f"\n📝 Topic: {topic}")

    result = workflow.run_workflow(topic)

    if result["success"]:
        print(f"\n✅ Final Output: {result['final_output'][:200]}...")
        print(f"\n🤖 Agents Used: {', '.join(result['agents_used'])}")

        scores = workflow.evaluate(topic, result["final_output"])

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

    agent = GoogleADKAgent()

    test_queries = [
        "Explain machine learning",
        "What is deep learning?",
        "Tell me about neural networks"
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

    agent = GoogleADKAgent()

    test_cases = [
        {"query": "What is AI?", "category": "AI"},
        {"query": "Calculate 100 / 4", "category": "Math"},
        {"query": "Weather in London?", "category": "Weather"}
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
    print("Google ADK (adk-python) with Custom Evals - Complete Test Suite")
    print("="*80)

    if not ADK_AVAILABLE:
        print("\n❌ Google ADK (adk-python) not available.")
        print("Install with: pip install adk")
        exit(1)

    if not GENAI_AVAILABLE:
        print("\n❌ google-generativeai not available.")
        print("Install with: pip install google-generativeai")
        exit(1)

    if not os.getenv("GOOGLE_API_KEY"):
        print("\n❌ GOOGLE_API_KEY not set. Please set your API key.")
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
