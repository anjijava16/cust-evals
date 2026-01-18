"""
Semantic Kernel (Microsoft) Example with Custom Evals Testing

This example demonstrates:
1. Building agents with Semantic Kernel from Microsoft
2. Plugin system and function calling
3. Multi-agent orchestration with planners
4. Memory and context management
5. Evaluating agent outputs with custom-evals

Semantic Kernel is Microsoft's SDK for integrating AI into applications.

Requirements:
- semantic-kernel (pip install semantic-kernel)
"""

import os
import json
from typing import Dict, Any, List, Optional

try:
    import semantic_kernel as sk
    from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
    from semantic_kernel.core_plugins import TextPlugin
    from semantic_kernel.planning import SequentialPlanner
    SEMANTIC_KERNEL_AVAILABLE = True
except ImportError:
    SEMANTIC_KERNEL_AVAILABLE = False
    print("⚠️  Semantic Kernel not installed. Install with: pip install semantic-kernel")

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
# STEP 1: Define Plugins (Tools) for Semantic Kernel
# ============================================================================

class WeatherPlugin:
    """Plugin for weather information."""

    @sk.kernel_function(
        name="get_weather",
        description="Get current weather for a location"
    )
    def get_weather(self, location: str) -> str:
        """Get weather for a location."""
        weather_data = {
            "San Francisco": "Sunny, 72°F",
            "New York": "Cloudy, 65°F",
            "London": "Rainy, 55°F",
            "Tokyo": "Clear, 68°F"
        }
        return weather_data.get(location, f"Weather data not available for {location}")


class KnowledgePlugin:
    """Plugin for knowledge base access."""

    @sk.kernel_function(
        name="search_knowledge",
        description="Search knowledge base for information"
    )
    def search_knowledge(self, query: str) -> str:
        """Search knowledge base."""
        knowledge = {
            "semantic kernel": "Semantic Kernel is Microsoft's SDK for integrating AI into applications.",
            "azure": "Azure is Microsoft's cloud computing platform.",
            "copilot": "Microsoft Copilot is an AI assistant integrated into Microsoft products.",
            "ai": "Artificial intelligence enables machines to perform cognitive tasks."
        }

        query_lower = query.lower()
        for key, value in knowledge.items():
            if key in query_lower:
                return value

        return f"No information found for: {query}"


class MathPlugin:
    """Plugin for mathematical operations."""

    @sk.kernel_function(
        name="calculate",
        description="Calculate mathematical expressions"
    )
    def calculate(self, expression: str) -> str:
        """Calculate expression."""
        try:
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error: {str(e)}"


class DataPlugin:
    """Plugin for data operations."""

    @sk.kernel_function(
        name="get_data_info",
        description="Get information about datasets"
    )
    def get_data_info(self, dataset_name: str) -> str:
        """Get dataset information."""
        datasets = {
            "sales": "Sales dataset: 10000 rows, updated daily",
            "customers": "Customer dataset: 5000 rows, updated weekly",
            "products": "Product dataset: 2000 rows, updated monthly"
        }
        return datasets.get(dataset_name.lower(), f"Dataset {dataset_name} not found")


# ============================================================================
# STEP 2: Semantic Kernel Agent System
# ============================================================================

class SemanticKernelAgent:
    """Agent using Semantic Kernel."""

    def __init__(self, model: str = "gpt-4o-mini"):
        if not SEMANTIC_KERNEL_AVAILABLE:
            raise ImportError("Semantic Kernel required")

        # Create kernel
        self.kernel = sk.Kernel()

        # Add AI service
        api_key = os.getenv("OPENAI_API_KEY")
        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id=model,
                api_key=api_key
            )
        )

        # Add plugins
        self.kernel.add_plugin(WeatherPlugin(), "Weather")
        self.kernel.add_plugin(KnowledgePlugin(), "Knowledge")
        self.kernel.add_plugin(MathPlugin(), "Math")
        self.kernel.add_plugin(DataPlugin(), "Data")

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    async def run(self, message: str) -> Dict[str, Any]:
        """Run agent on a message."""
        try:
            # Create chat function
            chat_function = self.kernel.add_function(
                prompt=f"{{{{$input}}}}\n\nYou are a helpful assistant with access to tools. Use them when needed.",
                function_name="chat",
                plugin_name="ChatPlugin"
            )

            # Invoke
            result = await self.kernel.invoke(chat_function, input=message)

            return {
                "success": True,
                "response": str(result),
                "agent": "semantic_kernel"
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
# STEP 3: Multi-Agent System with Planner
# ============================================================================

class SemanticKernelMultiAgent:
    """Multi-agent system using Semantic Kernel with planner."""

    def __init__(self):
        if not SEMANTIC_KERNEL_AVAILABLE:
            raise ImportError("Semantic Kernel required")

        # Create kernel
        self.kernel = sk.Kernel()

        # Add AI service
        api_key = os.getenv("OPENAI_API_KEY")
        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="chat",
                ai_model_id="gpt-4o-mini",
                api_key=api_key
            )
        )

        # Add plugins
        self.kernel.add_plugin(WeatherPlugin(), "Weather")
        self.kernel.add_plugin(KnowledgePlugin(), "Knowledge")
        self.kernel.add_plugin(MathPlugin(), "Math")

        # Create planner
        self.planner = SequentialPlanner(self.kernel)

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm)
        }

    async def run_workflow(self, goal: str) -> Dict[str, Any]:
        """Run multi-step workflow with planner."""
        try:
            # Create plan
            plan = await self.planner.create_plan(goal)

            # Execute plan
            result = await plan.invoke(self.kernel)

            return {
                "success": True,
                "goal": goal,
                "plan_steps": len(plan._steps) if hasattr(plan, '_steps') else 0,
                "final_output": str(result),
                "planner": "SequentialPlanner"
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
    print("TEST 1: Simple Semantic Kernel Agent")
    print("="*80)

    import asyncio

    agent = SemanticKernelAgent()

    query = "What is artificial intelligence?"
    print(f"\n📝 Query: {query}")

    result = asyncio.run(agent.run(query))

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


def test_agent_with_plugins():
    """Test 2: Agent with plugin usage."""
    print("\n" + "="*80)
    print("TEST 2: Semantic Kernel Agent with Plugins")
    print("="*80)

    import asyncio

    agent = SemanticKernelAgent()

    query = "What's the weather in Tokyo?"
    print(f"\n📝 Query: {query}")

    result = asyncio.run(agent.run(query))

    if result["success"]:
        print(f"\n✅ Response: {result['response']}")

        scores = agent.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")
    else:
        print(f"\n❌ Error: {result.get('error')}")

    return result


def test_multi_agent_planner():
    """Test 3: Multi-agent with planner."""
    print("\n" + "="*80)
    print("TEST 3: Semantic Kernel Multi-Agent with Planner")
    print("="*80)

    import asyncio

    system = SemanticKernelMultiAgent()

    goal = "Get the weather in San Francisco and explain Semantic Kernel"
    print(f"\n📝 Goal: {goal}")

    result = asyncio.run(system.run_workflow(goal))

    if result["success"]:
        print(f"\n✅ Final Output: {result['final_output'][:200]}...")
        print(f"\n📊 Plan Steps: {result['plan_steps']}")
        print(f"🤖 Planner: {result['planner']}")

        scores = system.evaluate(goal, result["final_output"])

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

    import asyncio

    QUALITY_THRESHOLDS = {
        "coherence": 0.7,
        "relevance": 0.7,
        "correctness": 0.7,
        "toxicity": 0.2
    }

    agent = SemanticKernelAgent()

    test_queries = [
        "Explain Semantic Kernel",
        "What is Azure?",
        "Tell me about Microsoft Copilot"
    ]

    results = []

    for query in test_queries:
        print(f"\n📝 Query: {query}")
        result = asyncio.run(agent.run(query))

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

    import asyncio

    agent = SemanticKernelAgent()

    test_cases = [
        {"query": "What is AI?", "category": "AI"},
        {"query": "Calculate 100 / 4", "category": "Math"},
        {"query": "Weather in London?", "category": "Weather"}
    ]

    results = []

    for test_case in test_cases:
        query = test_case["query"]
        print(f"\n📝 Query: {query}")

        result = asyncio.run(agent.run(query))

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
    print("Semantic Kernel (Microsoft) with Custom Evals - Complete Test Suite")
    print("="*80)

    if not SEMANTIC_KERNEL_AVAILABLE:
        print("\n❌ Semantic Kernel not available.")
        print("Install with: pip install semantic-kernel")
        exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY not set. Please set your API key.")
        exit(1)

    # Run all tests
    try:
        test_simple_agent()
        test_agent_with_plugins()
        test_multi_agent_planner()
        test_quality_gates()
        test_batch_evaluation()

        print("\n" + "="*80)
        print("✅ All tests completed successfully!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
