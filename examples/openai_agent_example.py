"""
OpenAI Agents SDK Example with Custom Evals Testing

This example demonstrates:
1. Building agents with OpenAI ChatCompletion API and function calling
2. Multi-turn conversations with tool execution
3. Stateless agent pattern (vs Assistants' threads)
4. Function/tool calling and execution
5. Evaluating agent outputs with custom-evals

This is the core OpenAI SDK approach, simpler than Assistants API or Swarm.

Requirements:
- openai (pip install openai>=1.0.0)
"""

import os
import json
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI SDK not installed. Install with: pip install openai>=1.0.0")

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
# STEP 1: Define Tools/Functions
# ============================================================================

def get_weather(location: str) -> str:
    """Get current weather for a location."""
    weather_data = {
        "San Francisco": "Sunny, 72°F with light breeze",
        "New York": "Cloudy, 65°F with chance of rain",
        "London": "Foggy, 55°F",
        "Tokyo": "Clear, 68°F",
        "Sydney": "Partly cloudy, 75°F"
    }
    return weather_data.get(location, f"Weather data not available for {location}")


def calculate(expression: str) -> str:
    """Safely calculate a mathematical expression."""
    try:
        # Only allow basic math operations for safety
        allowed_chars = set("0123456789+-*/()., ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"


def search_database(query: str) -> str:
    """Search a mock database for information."""
    database = {
        "python": "Python is a high-level programming language known for readability and versatility.",
        "machine learning": "Machine learning is a subset of AI that enables systems to learn from data.",
        "neural network": "A neural network is a computational model inspired by biological neural networks.",
        "api": "An API (Application Programming Interface) allows different software to communicate.",
        "docker": "Docker is a platform for developing, shipping, and running applications in containers."
    }

    query_lower = query.lower()
    for key, value in database.items():
        if key in query_lower:
            return value

    return f"No information found for: {query}"


def get_user_info(user_id: str) -> str:
    """Get user information by ID."""
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
# STEP 2: OpenAI Function Agent
# ============================================================================

class OpenAIFunctionAgent:
    """Agent using OpenAI ChatCompletion API with function calling."""

    def __init__(self, model: str = "gpt-4o-mini"):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI SDK required")

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

        # Define available functions
        self.available_functions = {
            "get_weather": get_weather,
            "calculate": calculate,
            "search_database": search_database,
            "get_user_info": get_user_info
        }

        # Define function schemas for OpenAI
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get the current weather for a specific location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city name (e.g., 'San Francisco', 'New York')"
                            }
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "Calculate a mathematical expression",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression to evaluate (e.g., '25 * 4')"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_database",
                    "description": "Search the database for information on a topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_user_info",
                    "description": "Get information about a user by their ID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The user ID (e.g., 'user123')"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            }
        ]

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, user_message: str, system_prompt: str = None) -> Dict[str, Any]:
        """Run agent on a message with function calling support."""
        try:
            messages = []

            # Add system message
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({
                    "role": "system",
                    "content": "You are a helpful assistant with access to various tools. Use them when needed to provide accurate information."
                })

            # Add user message
            messages.append({"role": "user", "content": user_message})

            function_calls = []
            max_iterations = 5
            iteration = 0

            # Multi-turn function calling loop
            while iteration < max_iterations:
                # Call OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto",
                    temperature=0
                )

                assistant_message = response.choices[0].message

                # Check if function calling is requested
                if assistant_message.tool_calls:
                    # Add assistant message to conversation
                    messages.append(assistant_message)

                    # Execute each function call
                    for tool_call in assistant_message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)

                        # Execute function
                        function_to_call = self.available_functions[function_name]
                        function_result = function_to_call(**function_args)

                        # Track function call
                        function_calls.append({
                            "function": function_name,
                            "arguments": function_args,
                            "result": function_result
                        })

                        # Add function result to conversation
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": function_result
                        })

                    iteration += 1
                else:
                    # No more function calls, return final response
                    final_response = assistant_message.content

                    return {
                        "success": True,
                        "response": final_response,
                        "function_calls": function_calls,
                        "iterations": iteration,
                        "total_messages": len(messages)
                    }

            # Max iterations reached
            return {
                "success": False,
                "error": "Max iterations reached",
                "function_calls": function_calls
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

            # Add expected output for correctness evaluation
            if name == "correctness" and expected:
                eval_input["expected"] = expected

            score = evaluator.evaluate(eval_input)
            scores[name] = score

        return scores


# ============================================================================
# STEP 3: Multi-Tool Agent
# ============================================================================

class MultiToolAgent:
    """Agent that uses multiple tools in a single query."""

    def __init__(self):
        self.agent = OpenAIFunctionAgent(model="gpt-4o-mini")

    def run(self, query: str) -> Dict[str, Any]:
        """Run agent with multi-tool support."""
        system_prompt = """You are a helpful assistant with access to multiple tools.
        When answering questions, use the appropriate tools to gather information.
        You can use multiple tools in sequence if needed."""

        return self.agent.run(query, system_prompt)

    def evaluate(self, query: str, response: str) -> Dict[str, Any]:
        """Evaluate multi-tool agent response."""
        return self.agent.evaluate(query, response)


# ============================================================================
# STEP 4: Conversational Agent
# ============================================================================

class ConversationalAgent:
    """Agent that maintains conversation context."""

    def __init__(self):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI SDK required")

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"
        self.messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Maintain context across the conversation."
            }
        ]

        # Tools setup
        self.agent = OpenAIFunctionAgent()

    def chat(self, user_message: str) -> Dict[str, Any]:
        """Continue conversation with context."""
        result = self.agent.run(user_message)
        return result

    def reset(self):
        """Reset conversation history."""
        self.messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ]


# ============================================================================
# TESTING FUNCTIONS
# ============================================================================

def test_simple_query():
    """Test 1: Simple query without function calling."""
    print("\n" + "="*80)
    print("TEST 1: Simple Query (No Function Calling)")
    print("="*80)

    agent = OpenAIFunctionAgent()

    query = "What is artificial intelligence?"
    print(f"\n📝 Query: {query}")

    result = agent.run(query)

    if result["success"]:
        print(f"\n✅ Response: {result['response']}")
        print(f"📊 Function calls: {len(result['function_calls'])}")
        print(f"🔄 Iterations: {result['iterations']}")

        # Evaluate
        scores = agent.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")
            print(f"    Explanation: {score.explanation[:100]}...")
    else:
        print(f"\n❌ Error: {result.get('error')}")

    return result


def test_weather_function():
    """Test 2: Function calling with weather tool."""
    print("\n" + "="*80)
    print("TEST 2: Weather Function Calling")
    print("="*80)

    agent = OpenAIFunctionAgent()

    query = "What's the weather like in San Francisco?"
    print(f"\n📝 Query: {query}")

    result = agent.run(query)

    if result["success"]:
        print(f"\n✅ Response: {result['response']}")
        print(f"\n🔧 Function Calls:")
        for i, fc in enumerate(result["function_calls"], 1):
            print(f"  {i}. {fc['function']}({fc['arguments']})")
            print(f"     Result: {fc['result']}")

        # Evaluate
        scores = agent.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")

    return result


def test_multi_step_reasoning():
    """Test 3: Multi-step reasoning with multiple function calls."""
    print("\n" + "="*80)
    print("TEST 3: Multi-Step Reasoning")
    print("="*80)

    agent = MultiToolAgent()

    query = "What's the weather in Tokyo and calculate what 15 * 8 equals?"
    print(f"\n📝 Query: {query}")

    result = agent.run(query)

    if result["success"]:
        print(f"\n✅ Response: {result['response']}")
        print(f"\n🔧 Function Calls ({len(result['function_calls'])}):")
        for i, fc in enumerate(result["function_calls"], 1):
            print(f"  {i}. {fc['function']}({fc['arguments']})")
            print(f"     Result: {fc['result']}")

        # Evaluate
        scores = agent.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")

    return result


def test_database_search():
    """Test 4: Database search function."""
    print("\n" + "="*80)
    print("TEST 4: Database Search")
    print("="*80)

    agent = OpenAIFunctionAgent()

    query = "Tell me about machine learning"
    print(f"\n📝 Query: {query}")

    result = agent.run(query)

    if result["success"]:
        print(f"\n✅ Response: {result['response']}")
        print(f"\n🔧 Function Calls:")
        for fc in result["function_calls"]:
            print(f"  - {fc['function']}: {fc['result']}")

        scores = agent.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")

    return result


def test_quality_gates():
    """Test 5: Quality gates validation."""
    print("\n" + "="*80)
    print("TEST 5: Quality Gates")
    print("="*80)

    QUALITY_THRESHOLDS = {
        "coherence": 0.7,
        "relevance": 0.7,
        "correctness": 0.7,
        "toxicity": 0.2  # Lower is better
    }

    agent = OpenAIFunctionAgent()

    test_queries = [
        "What's the weather in New York?",
        "Calculate 100 / 4",
        "Tell me about neural networks"
    ]

    results = []

    for query in test_queries:
        print(f"\n📝 Query: {query}")
        result = agent.run(query)

        if result["success"]:
            scores = agent.evaluate(query, result["response"])

            # Check quality gates
            passed = True
            for metric, threshold in QUALITY_THRESHOLDS.items():
                if metric in scores:
                    score_value = scores[metric].score
                    if metric == "toxicity":
                        if score_value > threshold:
                            passed = False
                            print(f"  ❌ {metric}: {score_value:.2f} (threshold: <{threshold})")
                        else:
                            print(f"  ✅ {metric}: {score_value:.2f}")
                    else:
                        if score_value < threshold:
                            passed = False
                            print(f"  ❌ {metric}: {score_value:.2f} (threshold: >{threshold})")
                        else:
                            print(f"  ✅ {metric}: {score_value:.2f}")

            results.append({
                "query": query,
                "passed": passed,
                "scores": scores
            })

    print(f"\n📊 Quality Gate Summary: {sum(r['passed'] for r in results)}/{len(results)} passed")
    return results


def test_batch_evaluation():
    """Test 6: Batch evaluation for regression testing."""
    print("\n" + "="*80)
    print("TEST 6: Batch Evaluation")
    print("="*80)

    agent = OpenAIFunctionAgent()

    test_cases = [
        {"query": "What's the weather in London?", "expected_function": "get_weather"},
        {"query": "Calculate 50 * 20", "expected_function": "calculate"},
        {"query": "Search for information about Python", "expected_function": "search_database"},
    ]

    results = []

    for test_case in test_cases:
        query = test_case["query"]
        expected_function = test_case["expected_function"]

        print(f"\n📝 Query: {query}")
        print(f"🎯 Expected function: {expected_function}")

        result = agent.run(query)

        if result["success"]:
            # Check if expected function was called
            function_names = [fc["function"] for fc in result["function_calls"]]
            function_used = expected_function in function_names

            print(f"  ✅ Function called: {function_used}")
            print(f"  📊 Functions used: {', '.join(function_names)}")

            scores = agent.evaluate(query, result["response"])

            avg_score = sum(s.score for s in scores.values() if s.score is not None) / len(scores)
            print(f"  📈 Average score: {avg_score:.2f}")

            results.append({
                "query": query,
                "function_used": function_used,
                "avg_score": avg_score
            })

    print(f"\n📊 Batch Summary:")
    print(f"  - Tests: {len(results)}")
    print(f"  - Correct function usage: {sum(r['function_used'] for r in results)}/{len(results)}")
    print(f"  - Average score: {sum(r['avg_score'] for r in results) / len(results):.2f}")

    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("OpenAI Agents SDK with Custom Evals - Complete Test Suite")
    print("="*80)

    if not OPENAI_AVAILABLE:
        print("\n❌ OpenAI SDK not available. Please install: pip install openai>=1.0.0")
        exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY not set. Please set your API key.")
        exit(1)

    # Run all tests
    try:
        test_simple_query()
        test_weather_function()
        test_multi_step_reasoning()
        test_database_search()
        test_quality_gates()
        test_batch_evaluation()

        print("\n" + "="*80)
        print("✅ All tests completed successfully!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
