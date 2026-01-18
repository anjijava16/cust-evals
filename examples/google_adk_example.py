"""
Google ADK (google-adk) Example with Custom Evals Testing

This example demonstrates:
1. Building agents with Google ADK (google-adk package)
2. Multi-agent orchestration with Google's framework
3. Tool integration and state management
4. Workflow execution and routing
5. Evaluating agent outputs with custom-evals

Google ADK from: https://github.com/google/adk-python
Install: pip install google-adk

Requirements:
- google-adk (pip install google-adk)
"""

import os
import json
from typing import Dict, Any, List, Optional

try:
    from google_adk import Agent, Tool, AgentRunner
    from google_adk.tools import function_tool
    GOOGLE_ADK_AVAILABLE = True
except ImportError:
    GOOGLE_ADK_AVAILABLE = False
    print("⚠️  Google ADK not installed. Install with: pip install google-adk")

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
# STEP 1: Define Tools for Google ADK Agents
# ============================================================================

@function_tool
def get_weather(location: str) -> str:
    """Get current weather for a location.

    Args:
        location: City name (e.g., 'San Francisco', 'New York')

    Returns:
        Weather information including temperature and conditions
    """
    weather_data = {
        "San Francisco": "Sunny, 72°F with light breeze",
        "New York": "Cloudy, 65°F with chance of rain",
        "London": "Foggy, 55°F",
        "Tokyo": "Clear, 68°F",
        "Sydney": "Partly cloudy, 75°F"
    }
    return weather_data.get(location, f"Weather data not available for {location}")


@function_tool
def search_knowledge_base(query: str) -> str:
    """Search knowledge base for information.

    Args:
        query: Search query

    Returns:
        Relevant information from knowledge base
    """
    database = {
        "python": "Python is a high-level programming language known for readability.",
        "machine learning": "Machine learning is a method of data analysis that automates analytical model building.",
        "neural network": "A neural network is a computational model inspired by biological neural networks.",
        "google cloud": "Google Cloud Platform is a suite of cloud computing services.",
        "ai": "Artificial intelligence is the simulation of human intelligence by machines."
    }

    query_lower = query.lower()
    for key, value in database.items():
        if key in query_lower:
            return value

    return f"No information found for: {query}"


@function_tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression.

    Args:
        expression: Mathematical expression (e.g., '25 * 4')

    Returns:
        Calculation result
    """
    try:
        allowed_chars = set("0123456789+-*/()., ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters"
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@function_tool
def get_user_info(user_id: str) -> str:
    """Get user information by ID.

    Args:
        user_id: User ID to look up

    Returns:
        User information as JSON string
    """
    users = {
        "user123": {"name": "Alice", "role": "Engineer", "department": "AI"},
        "user456": {"name": "Bob", "role": "Manager", "department": "Product"},
        "user789": {"name": "Carol", "role": "Researcher", "department": "ML"}
    }

    user = users.get(user_id)
    if user:
        return json.dumps(user)
    return f"User {user_id} not found"


# ============================================================================
# STEP 2: Google ADK Agent System
# ============================================================================

class GoogleADKAgentSystem:
    """Agent system using Google ADK."""

    def __init__(self, model: str = "gemini-1.5-flash"):
        if not GOOGLE_ADK_AVAILABLE:
            raise ImportError("Google ADK required")

        self.model = model

        # Create agent with tools
        self.agent = Agent(
            name="assistant",
            model=model,
            instructions="You are a helpful assistant with access to tools. Use them to provide accurate information.",
            tools=[get_weather, search_knowledge_base, calculate, get_user_info]
        )

        # Create runner
        self.runner = AgentRunner(api_key=os.getenv("GOOGLE_API_KEY"))

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
            result = self.runner.run(agent=self.agent, input=message)

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
# STEP 3: Multi-Agent System with Google ADK
# ============================================================================

class MultiAgentADKSystem:
    """Multi-agent system using Google ADK."""

    def __init__(self):
        if not GOOGLE_ADK_AVAILABLE:
            raise ImportError("Google ADK required")

        model = "gemini-1.5-flash"
        api_key = os.getenv("GOOGLE_API_KEY")

        # Create specialized agents
        self.research_agent = Agent(
            name="researcher",
            model=model,
            instructions="You are a research specialist. Gather comprehensive, factual information.",
            tools=[search_knowledge_base]
        )

        self.analysis_agent = Agent(
            name="analyst",
            model=model,
            instructions="You are an analysis expert. Extract key insights and patterns."
        )

        self.writer_agent = Agent(
            name="writer",
            model=model,
            instructions="You are a technical writer. Create clear, concise summaries."
        )

        # Create runner
        self.runner = AgentRunner(api_key=api_key)

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

    agent = GoogleADKAgentSystem()

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

    agent = GoogleADKAgentSystem()

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
    print("TEST 3: Multi-Agent Google ADK Workflow")
    print("="*80)

    system = MultiAgentADKSystem()

    topic = "Machine Learning"
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

    agent = GoogleADKAgentSystem()

    test_queries = [
        "Explain neural networks",
        "What is Google Cloud?",
        "Tell me about Python"
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

    agent = GoogleADKAgentSystem()

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
    print("Google ADK (google-adk) with Custom Evals - Complete Test Suite")
    print("="*80)

    if not GOOGLE_ADK_AVAILABLE:
        print("\n❌ Google ADK not available.")
        print("Install with: pip install google-adk")
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
