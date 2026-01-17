"""
OpenAI Agents Framework Example with Custom Evals Testing

This example demonstrates:
1. Building agents with the official OpenAI Agents framework (openai-agents-python)
2. Agent handoffs and routing
3. Tool integration and function calling
4. Multi-agent collaboration
5. Evaluating agent outputs with custom-evals

This is the official OpenAI Agents framework from: https://openai.github.io/openai-agents-python/

Requirements:
- openai-agents (pip install openai-agents)
- openai (pip install openai>=1.0.0)
"""

import os
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

try:
    from agents import Agent, Runner, function_tool
    from agents.extensions.handoff import Handoff
    OPENAI_AGENTS_AVAILABLE = True
except ImportError:
    OPENAI_AGENTS_AVAILABLE = False
    print("⚠️  OpenAI Agents framework not installed. Install with: pip install openai-agents")

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
# STEP 1: Define Tools with @function_tool decorator
# ============================================================================

@function_tool
def get_weather(location: str) -> str:
    """Get current weather for a location.

    Args:
        location: The city name (e.g., 'San Francisco', 'New York')

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
def search_database(query: str) -> str:
    """Search knowledge database for information.

    Args:
        query: The search query

    Returns:
        Relevant information from the database
    """
    database = {
        "python": "Python is a high-level programming language known for readability.",
        "machine learning": "Machine learning is a method of data analysis that automates analytical model building.",
        "neural network": "A neural network is a computational model inspired by biological neural networks.",
        "ai": "Artificial intelligence is the simulation of human intelligence by machines.",
        "api": "An API allows different software applications to communicate with each other."
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
        expression: Mathematical expression to evaluate (e.g., '25 * 4')

    Returns:
        The calculation result
    """
    try:
        allowed_chars = set("0123456789+-*/()., ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"


@function_tool
def get_user_info(user_id: str) -> str:
    """Get user information by ID.

    Args:
        user_id: The user ID to look up

    Returns:
        User information as JSON string
    """
    users = {
        "user123": {"name": "Alice Smith", "role": "Engineer", "department": "AI Research"},
        "user456": {"name": "Bob Johnson", "role": "Manager", "department": "Product"},
        "user789": {"name": "Carol Davis", "role": "Designer", "department": "UX"}
    }

    user = users.get(user_id)
    if user:
        return json.dumps(user)
    return f"User {user_id} not found"


# ============================================================================
# STEP 2: Simple OpenAI Agents Framework Agent
# ============================================================================

class OpenAIAgentsFrameworkAgent:
    """Agent using official OpenAI Agents framework."""

    def __init__(self, model: str = "gpt-4o-mini"):
        if not OPENAI_AGENTS_AVAILABLE:
            raise ImportError("OpenAI Agents framework required")

        self.model = model

        # Create agent with tools
        self.agent = Agent(
            name="assistant",
            instructions="You are a helpful assistant with access to various tools. Use them to provide accurate information.",
            tools=[get_weather, search_database, calculate, get_user_info],
            model=model
        )

        # Initialize runner
        self.runner = Runner(api_key=os.getenv("OPENAI_API_KEY"))

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
                messages=[{"role": "user", "content": message}]
            )

            # Extract response
            response_text = ""
            tool_calls = []

            for msg in result.messages:
                if msg.role == "assistant":
                    if msg.content:
                        response_text = msg.content
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for tc in msg.tool_calls:
                            tool_calls.append({
                                "function": tc.function.name,
                                "arguments": json.loads(tc.function.arguments) if tc.function.arguments else {}
                            })

            return {
                "success": True,
                "response": response_text,
                "tool_calls": tool_calls,
                "total_messages": len(result.messages)
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
# STEP 3: Multi-Agent System with Handoffs
# ============================================================================

class MultiAgentSystem:
    """Multi-agent system with handoffs using OpenAI Agents framework."""

    def __init__(self):
        if not OPENAI_AGENTS_AVAILABLE:
            raise ImportError("OpenAI Agents framework required")

        # Create specialized agents
        self.sales_agent = Agent(
            name="sales_agent",
            instructions="You are a sales specialist. Help customers with purchases, pricing, and product information.",
            tools=[search_database],
            model="gpt-4o-mini"
        )

        self.support_agent = Agent(
            name="support_agent",
            instructions="You are a technical support specialist. Help customers with technical issues and troubleshooting.",
            tools=[get_user_info, search_database],
            model="gpt-4o-mini"
        )

        self.info_agent = Agent(
            name="info_agent",
            instructions="You are an information specialist. Provide general information and answer questions.",
            tools=[search_database, get_weather],
            model="gpt-4o-mini"
        )

        # Create triage agent with handoffs
        self.triage_agent = Agent(
            name="triage_agent",
            instructions="""You are a triage agent that routes customers to the right specialist.
            - For purchases, pricing, products → Transfer to sales_agent
            - For technical issues, support → Transfer to support_agent
            - For general information, weather → Transfer to info_agent
            Analyze the customer's request and transfer to the appropriate agent.""",
            handoffs=[
                Handoff(agent=self.sales_agent),
                Handoff(agent=self.support_agent),
                Handoff(agent=self.info_agent)
            ],
            model="gpt-4o-mini"
        )

        # Initialize runner
        self.runner = Runner(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm)
        }

    def run(self, message: str) -> Dict[str, Any]:
        """Run multi-agent system with routing."""
        try:
            # Start with triage agent
            result = self.runner.run(
                agent=self.triage_agent,
                messages=[{"role": "user", "content": message}]
            )

            # Extract response and track agents used
            response_text = ""
            agents_used = []

            for msg in result.messages:
                if msg.role == "assistant":
                    if msg.content:
                        response_text = msg.content
                    # Track which agent responded
                    if hasattr(msg, 'agent_name'):
                        agents_used.append(msg.agent_name)

            return {
                "success": True,
                "response": response_text,
                "agents_used": list(set(agents_used)) if agents_used else ["triage_agent"],
                "total_messages": len(result.messages)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def evaluate(self, query: str, response: str) -> Dict[str, Any]:
        """Evaluate multi-agent system response."""
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
    print("TEST 1: Simple OpenAI Agents Framework Agent")
    print("="*80)

    agent = OpenAIAgentsFrameworkAgent()

    query = "What is artificial intelligence?"
    print(f"\n📝 Query: {query}")

    result = agent.run(query)

    if result["success"]:
        print(f"\n✅ Response: {result['response'][:200]}...")
        print(f"📊 Total messages: {result['total_messages']}")

        # Evaluate
        scores = agent.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")
            print(f"    Explanation: {score.explanation[:100]}...")
    else:
        print(f"\n❌ Error: {result.get('error')}")

    return result


def test_tool_calling():
    """Test 2: Agent with tool calling."""
    print("\n" + "="*80)
    print("TEST 2: Tool Calling")
    print("="*80)

    agent = OpenAIAgentsFrameworkAgent()

    query = "What's the weather in Tokyo and calculate 15 * 8?"
    print(f"\n📝 Query: {query}")

    result = agent.run(query)

    if result["success"]:
        print(f"\n✅ Response: {result['response']}")
        print(f"\n🔧 Tool Calls: {len(result['tool_calls'])}")
        for tc in result["tool_calls"]:
            print(f"  - {tc['function']}: {tc['arguments']}")

        scores = agent.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")

    return result


def test_multi_agent_handoffs():
    """Test 3: Multi-agent system with handoffs."""
    print("\n" + "="*80)
    print("TEST 3: Multi-Agent System with Handoffs")
    print("="*80)

    system = MultiAgentSystem()

    test_queries = [
        "I want to buy a product",
        "I need technical support",
        "What's the weather in San Francisco?"
    ]

    results = []

    for query in test_queries:
        print(f"\n📝 Query: {query}")

        result = system.run(query)

        if result["success"]:
            print(f"✅ Response: {result['response'][:150]}...")
            print(f"🤖 Agents used: {', '.join(result['agents_used'])}")

            scores = system.evaluate(query, result["response"])
            print(f"📈 Coherence: {scores['coherence'].score:.2f}, Relevance: {scores['relevance'].score:.2f}")

            results.append(result)

    return results


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

    agent = OpenAIAgentsFrameworkAgent()

    test_queries = [
        "Tell me about machine learning",
        "What's the weather in London?",
        "Calculate 100 / 4"
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

    agent = OpenAIAgentsFrameworkAgent()

    test_cases = [
        {"query": "What's 50 * 20?", "expected_tool": "calculate"},
        {"query": "Search for information about Python", "expected_tool": "search_database"},
        {"query": "What's the weather in New York?", "expected_tool": "get_weather"}
    ]

    results = []

    for test_case in test_cases:
        query = test_case["query"]
        expected_tool = test_case["expected_tool"]

        print(f"\n📝 Query: {query}")
        print(f"🎯 Expected tool: {expected_tool}")

        result = agent.run(query)

        if result["success"]:
            tool_names = [tc["function"] for tc in result["tool_calls"]]
            tool_used = expected_tool in tool_names

            print(f"  ✅ Correct tool used: {tool_used}")
            print(f"  🔧 Tools: {', '.join(tool_names)}")

            scores = agent.evaluate(query, result["response"])
            avg_score = sum(s.score for s in scores.values()) / len(scores)
            print(f"  📈 Average score: {avg_score:.2f}")

            results.append({"query": query, "tool_used": tool_used, "avg_score": avg_score})

    print(f"\n📊 Batch Summary:")
    print(f"  - Tests: {len(results)}")
    print(f"  - Correct tool usage: {sum(r['tool_used'] for r in results)}/{len(results)}")
    print(f"  - Average score: {sum(r['avg_score'] for r in results) / len(results):.2f}")

    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("OpenAI Agents Framework with Custom Evals - Complete Test Suite")
    print("="*80)

    if not OPENAI_AGENTS_AVAILABLE:
        print("\n❌ OpenAI Agents framework not available.")
        print("Install with: pip install openai-agents")
        exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY not set. Please set your API key.")
        exit(1)

    # Run all tests
    try:
        test_simple_agent()
        test_tool_calling()
        test_multi_agent_handoffs()
        test_quality_gates()
        test_batch_evaluation()

        print("\n" + "="*80)
        print("✅ All tests completed successfully!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
