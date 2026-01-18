"""
Agno Multi-Agent Framework with Custom-Evals Integration

This example demonstrates:
1. Simple Agno agent with tools
2. Multi-agent systems with Teams
3. Custom-Evals integration (CoherenceEvaluator, RelevanceEvaluator, CorrectnessEvaluator, ToxicityEvaluator)
4. Quality gates validation
5. Batch evaluation

Installation:
    pip install agno anthropic
    export ANTHROPIC_API_KEY="your-api-key"
    export OPENAI_API_KEY="your-openai-key"  # For evaluators

Official Documentation: https://docs.agno.com/
GitHub: https://github.com/agno-agi/agno
"""

import asyncio
import os
from typing import Dict, List

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.openai import OpenAI
from agno.team import Team
from agno.tools import tool

# Custom-Evals imports
from custom.evals import (
    CoherenceEvaluator,
    CorrectnessEvaluator,
    RelevanceEvaluator,
    ToxicityEvaluator,
)
from custom.evals.llm import LLM


# ============================================================================
# Tool Definitions (Python decorators)
# ============================================================================


@tool
def get_weather(location: str) -> str:
    """Get current weather for a location.

    Args:
        location: City name (e.g., "San Francisco", "New York")

    Returns:
        Weather information string
    """
    weather_data = {
        "San Francisco": "Sunny, 72°F with light breeze and clear skies",
        "New York": "Cloudy, 65°F with chance of rain in the evening",
        "London": "Rainy, 58°F with strong winds from the northwest",
        "Tokyo": "Partly cloudy, 68°F with moderate humidity",
    }
    return weather_data.get(
        location, f"Weather data not available for {location}. Try: San Francisco, New York, London, Tokyo"
    )


@tool
def search_web(query: str) -> str:
    """Search the web for information.

    Args:
        query: Search query string

    Returns:
        Search results
    """
    # Simulated search results
    search_results = {
        "machine learning": "Machine learning is a subset of AI focusing on algorithms that learn from data...",
        "python": "Python is a high-level programming language known for simplicity and readability...",
        "climate change": "Climate change refers to long-term shifts in temperatures and weather patterns...",
    }
    for key in search_results:
        if key.lower() in query.lower():
            return search_results[key]
    return f"Search results for '{query}': Found general information about the topic."


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: Mathematical expression (e.g., "2 + 2", "10 * 5")

    Returns:
        Calculation result
    """
    try:
        # Safe eval with limited scope
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


# ============================================================================
# Agno Agent with Custom-Evals Integration
# ============================================================================


class AgnoEvaluatedAgent:
    """Agno agent with integrated Custom-Evals evaluation."""

    def __init__(self, use_openai: bool = False):
        """Initialize Agno agent with evaluators.

        Args:
            use_openai: If True, use OpenAI models. If False, use Anthropic Claude.
        """
        # Create Agno agent
        if use_openai:
            model = OpenAI(id="gpt-4o-mini")
        else:
            model = Claude(id="claude-sonnet-4-5")

        self.agent = Agent(
            name="Research Assistant",
            model=model,
            instructions=[
                "You are a helpful research assistant.",
                "Provide accurate, concise information.",
                "Use tools when needed to gather information.",
                "Be professional and clear in your responses.",
            ],
            tools=[get_weather, search_web, calculate],
            markdown=True,
            show_tool_calls=True,
        )

        # Initialize Custom-Evals evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm),
        }

        # Quality thresholds
        self.quality_thresholds = {
            "coherence": 0.7,
            "relevance": 0.7,
            "correctness": 0.7,
            "toxicity": 0.2,  # Lower is better
        }

    def run(self, query: str) -> str:
        """Run agent and return response.

        Args:
            query: User query

        Returns:
            Agent response
        """
        response = self.agent.run(query)
        # Extract content from response
        if hasattr(response, "content"):
            return response.content
        return str(response)

    def evaluate(self, query: str, response: str) -> Dict:
        """Evaluate agent response using Custom-Evals.

        Args:
            query: User query
            response: Agent response

        Returns:
            Dictionary of evaluation scores
        """
        scores = {}
        for name, evaluator in self.evaluators.items():
            score = evaluator.evaluate({"input": query, "output": response})
            scores[name] = score

        return scores

    def run_and_evaluate(self, query: str) -> Dict:
        """Run agent and evaluate response.

        Args:
            query: User query

        Returns:
            Dictionary with response and evaluation scores
        """
        response = self.run(query)
        scores = self.evaluate(query, response)

        return {"query": query, "response": response, "scores": scores}

    def validate_quality_gates(self, scores: Dict) -> bool:
        """Validate response against quality thresholds.

        Args:
            scores: Evaluation scores

        Returns:
            True if all thresholds passed
        """
        passed = True
        for metric, threshold in self.quality_thresholds.items():
            score_value = scores[metric].score

            if metric == "toxicity":
                # Lower is better for toxicity
                if score_value > threshold:
                    print(f"❌ {metric}: {score_value:.2f} > {threshold} (FAILED)")
                    passed = False
                else:
                    print(f"✅ {metric}: {score_value:.2f} <= {threshold} (PASSED)")
            else:
                # Higher is better for other metrics
                if score_value < threshold:
                    print(f"❌ {metric}: {score_value:.2f} < {threshold} (FAILED)")
                    passed = False
                else:
                    print(f"✅ {metric}: {score_value:.2f} >= {threshold} (PASSED)")

        return passed


# ============================================================================
# Multi-Agent System with Agno Teams
# ============================================================================


class AgnoMultiAgentSystem:
    """Multi-agent system using Agno Teams with Custom-Evals."""

    def __init__(self):
        """Initialize multi-agent system."""
        # Research Agent
        self.researcher = Agent(
            name="Researcher",
            model=Claude(id="claude-sonnet-4-5"),
            instructions=[
                "You are a research specialist.",
                "Gather comprehensive information on topics.",
                "Use search tools to find accurate data.",
                "Provide detailed, factual responses.",
            ],
            tools=[search_web],
            markdown=True,
        )

        # Analyst Agent
        self.analyst = Agent(
            name="Analyst",
            model=Claude(id="claude-sonnet-4-5"),
            instructions=[
                "You are a data analyst.",
                "Analyze information and provide insights.",
                "Use calculations when needed.",
                "Present findings clearly and concisely.",
            ],
            tools=[calculate],
            markdown=True,
        )

        # Weather Agent
        self.weather_agent = Agent(
            name="Weather Specialist",
            model=Claude(id="claude-sonnet-4-5"),
            instructions=[
                "You are a weather information specialist.",
                "Provide weather forecasts and conditions.",
                "Use weather tools to get current data.",
                "Give practical weather advice.",
            ],
            tools=[get_weather],
            markdown=True,
        )

        # Create team
        self.team = Team(
            name="Research Team",
            agents=[self.researcher, self.analyst, self.weather_agent],
            instructions=[
                "Collaborate to provide comprehensive responses.",
                "Each agent contributes their expertise.",
                "Coordinator integrates all inputs into coherent response.",
            ],
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm),
        }

    def run(self, query: str) -> str:
        """Run multi-agent team.

        Args:
            query: User query

        Returns:
            Team response
        """
        response = self.team.run(query)
        if hasattr(response, "content"):
            return response.content
        return str(response)

    def evaluate(self, query: str, response: str) -> Dict:
        """Evaluate team response.

        Args:
            query: User query
            response: Team response

        Returns:
            Evaluation scores
        """
        scores = {}
        for name, evaluator in self.evaluators.items():
            score = evaluator.evaluate({"input": query, "output": response})
            scores[name] = score
        return scores


# ============================================================================
# Test Suite 1: Simple Agent
# ============================================================================


def test_simple_agent():
    """Test simple Agno agent with Custom-Evals."""
    print("\n" + "=" * 80)
    print("TEST SUITE 1: Simple Agno Agent")
    print("=" * 80)

    agent = AgnoEvaluatedAgent()

    test_queries = [
        "What is machine learning?",
        "What's the weather in San Francisco?",
        "Calculate 15 * 24",
    ]

    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 80)

        result = agent.run_and_evaluate(query)

        print(f"🤖 Response: {result['response'][:200]}...")
        print("\n📊 Evaluation Scores:")
        for metric, score in result["scores"].items():
            print(f"  {metric}: {score.score:.2f} - {score.label}")

        print("\n🎯 Quality Gates:")
        passed = agent.validate_quality_gates(result["scores"])
        print(f"Overall: {'✅ PASSED' if passed else '❌ FAILED'}")


# ============================================================================
# Test Suite 2: Tool Usage
# ============================================================================


def test_tool_usage():
    """Test Agno agent tool usage with evaluation."""
    print("\n" + "=" * 80)
    print("TEST SUITE 2: Tool Usage")
    print("=" * 80)

    agent = AgnoEvaluatedAgent()

    tool_queries = [
        ("Weather tool", "What's the weather like in New York and London?"),
        ("Search tool", "Tell me about climate change"),
        ("Calculate tool", "What is 123 multiplied by 456?"),
    ]

    for tool_name, query in tool_queries:
        print(f"\n🔧 Testing: {tool_name}")
        print(f"📝 Query: {query}")
        print("-" * 80)

        result = agent.run_and_evaluate(query)

        print(f"🤖 Response: {result['response'][:200]}...")
        print("\n📊 Evaluation Scores:")
        for metric, score in result["scores"].items():
            print(f"  {metric}: {score.score:.2f} - {score.label}")


# ============================================================================
# Test Suite 3: Multi-Agent System
# ============================================================================


def test_multi_agent_system():
    """Test Agno multi-agent system with Custom-Evals."""
    print("\n" + "=" * 80)
    print("TEST SUITE 3: Multi-Agent System (Agno Teams)")
    print("=" * 80)

    system = AgnoMultiAgentSystem()

    complex_queries = [
        "Research machine learning and provide weather forecast for San Francisco",
        "Search for information about Python and calculate 50 * 100",
    ]

    for query in complex_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 80)

        response = system.run(query)
        scores = system.evaluate(query, response)

        print(f"🤖 Team Response: {response[:300]}...")
        print("\n📊 Evaluation Scores:")
        for metric, score in scores.items():
            print(f"  {metric}: {score.score:.2f} - {score.label}")


# ============================================================================
# Test Suite 4: Quality Gates Validation
# ============================================================================


def test_quality_gates():
    """Test quality gates validation across multiple queries."""
    print("\n" + "=" * 80)
    print("TEST SUITE 4: Quality Gates Validation")
    print("=" * 80)

    agent = AgnoEvaluatedAgent()

    test_scenarios = [
        ("High quality", "Explain artificial intelligence in simple terms"),
        ("Technical", "What is the time complexity of binary search?"),
        ("Creative", "Why is the sky blue?"),
    ]

    results = []
    for scenario_name, query in test_scenarios:
        print(f"\n🧪 Scenario: {scenario_name}")
        print(f"📝 Query: {query}")
        print("-" * 80)

        result = agent.run_and_evaluate(query)
        passed = agent.validate_quality_gates(result["scores"])

        results.append({"scenario": scenario_name, "passed": passed, "scores": result["scores"]})

        print(f"Result: {'✅ PASSED' if passed else '❌ FAILED'}")

    # Summary
    print("\n" + "=" * 80)
    print("QUALITY GATES SUMMARY")
    print("=" * 80)
    passed_count = sum(1 for r in results if r["passed"])
    print(f"Passed: {passed_count}/{len(results)} scenarios")
    print(f"Success Rate: {passed_count/len(results)*100:.1f}%")


# ============================================================================
# Test Suite 5: Batch Evaluation
# ============================================================================


def test_batch_evaluation():
    """Test batch evaluation of multiple queries."""
    print("\n" + "=" * 80)
    print("TEST SUITE 5: Batch Evaluation")
    print("=" * 80)

    agent = AgnoEvaluatedAgent()

    batch_queries = [
        "What is quantum computing?",
        "How does photosynthesis work?",
        "Explain blockchain technology",
        "What causes earthquakes?",
        "How do vaccines work?",
    ]

    all_results = []
    for i, query in enumerate(batch_queries, 1):
        print(f"\n[{i}/{len(batch_queries)}] Processing: {query}")
        result = agent.run_and_evaluate(query)
        all_results.append(result)

    # Aggregate statistics
    print("\n" + "=" * 80)
    print("BATCH EVALUATION RESULTS")
    print("=" * 80)

    metrics = ["coherence", "relevance", "correctness", "toxicity"]
    for metric in metrics:
        scores = [r["scores"][metric].score for r in all_results]
        avg_score = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)

        print(f"\n{metric.upper()}:")
        print(f"  Average: {avg_score:.3f}")
        print(f"  Min: {min_score:.3f}")
        print(f"  Max: {max_score:.3f}")

    # Quality gates summary
    print("\n" + "-" * 80)
    quality_passed = 0
    for result in all_results:
        passed = all(
            result["scores"][m].score >= 0.7 for m in ["coherence", "relevance", "correctness"]
        ) and result["scores"]["toxicity"].score <= 0.2
        if passed:
            quality_passed += 1

    print(f"\nQuality Gates Passed: {quality_passed}/{len(all_results)} queries")
    print(f"Success Rate: {quality_passed/len(all_results)*100:.1f}%")


# ============================================================================
# Main Execution
# ============================================================================


def main():
    """Run all Agno test suites."""
    print("\n" + "=" * 80)
    print("AGNO FRAMEWORK WITH CUSTOM-EVALS INTEGRATION")
    print("=" * 80)
    print("\nOfficial Documentation: https://docs.agno.com/")
    print("This example demonstrates Agno agents with Custom-Evals evaluation")

    # Check API keys
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️  Warning: ANTHROPIC_API_KEY not set. Agno agent will fail.")
        print("Set with: export ANTHROPIC_API_KEY='your-key'")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY not set. Evaluators will fail.")
        print("Set with: export OPENAI_API_KEY='your-key'")
        return

    try:
        # Run all test suites
        test_simple_agent()
        test_tool_usage()
        test_multi_agent_system()
        test_quality_gates()
        test_batch_evaluation()

        print("\n" + "=" * 80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error running tests: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
