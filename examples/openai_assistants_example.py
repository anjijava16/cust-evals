"""
OpenAI Assistants API Example with Custom Evals Testing

This example demonstrates:
1. Creating OpenAI Assistants with specific instructions
2. Using function calling with assistants
3. Managing threads and messages
4. Code interpreter integration
5. Evaluating assistant outputs with custom-evals

The Assistants API allows you to build AI assistants with tools and persistent threads.

Requirements:
- openai (pip install openai>=1.0.0)
"""

import os
import time
from typing import Dict, Any, List, Optional

try:
    from openai import OpenAI
    OPENAI_SDK_AVAILABLE = True
except ImportError:
    OPENAI_SDK_AVAILABLE = False
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
# STEP 1: Simple Assistant
# ============================================================================

class SimpleAssistant:
    """Simple OpenAI Assistant for Q&A."""

    def __init__(self):
        if not OPENAI_SDK_AVAILABLE:
            raise ImportError("OpenAI SDK required")

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Create assistant
        self.assistant = self.client.beta.assistants.create(
            name="General Assistant",
            instructions="""You are a helpful assistant that answers questions clearly and concisely.
            Provide accurate information and cite sources when possible.""",
            model="gpt-4o-mini"
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, message: str) -> Dict[str, Any]:
        """Run assistant on a message."""
        try:
            # Create thread
            thread = self.client.beta.threads.create()

            # Add message
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=message
            )

            # Run assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant.id
            )

            # Wait for completion
            while run.status in ["queued", "in_progress"]:
                time.sleep(1)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )

            if run.status == "completed":
                # Get messages
                messages = self.client.beta.threads.messages.list(
                    thread_id=thread.id
                )

                # Extract assistant's response
                response = messages.data[0].content[0].text.value

                return {
                    "message": message,
                    "response": response,
                    "thread_id": thread.id,
                    "success": True
                }
            else:
                return {
                    "message": message,
                    "response": f"Run failed with status: {run.status}",
                    "success": False,
                    "error": f"Status: {run.status}"
                }

        except Exception as e:
            return {
                "message": message,
                "response": str(e),
                "success": False,
                "error": str(e)
            }
        finally:
            # Clean up
            try:
                self.client.beta.threads.delete(thread.id)
            except:
                pass

    def evaluate(self, message: str, response: str) -> Dict[str, Any]:
        """Evaluate assistant response."""
        eval_input = {
            "input": message,
            "output": response
        }

        scores = {}
        for name, evaluator in self.evaluators.items():
            try:
                score = evaluator.evaluate(eval_input)
                scores[name] = score
            except Exception as e:
                print(f"Warning: {name} evaluation failed: {str(e)}")

        return scores

    def cleanup(self):
        """Delete assistant."""
        try:
            self.client.beta.assistants.delete(self.assistant.id)
        except:
            pass


# ============================================================================
# STEP 2: Function Calling Assistant
# ============================================================================

class FunctionCallingAssistant:
    """Assistant with function calling capabilities."""

    def __init__(self):
        if not OPENAI_SDK_AVAILABLE:
            raise ImportError("OpenAI SDK required")

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Define functions
        self.functions = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The city name"
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "Temperature unit"
                            }
                        },
                        "required": ["city"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_database",
                    "description": "Search for information in the database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "category": {
                                "type": "string",
                                "enum": ["users", "products", "orders"],
                                "description": "Database category"
                            }
                        },
                        "required": ["query", "category"]
                    }
                }
            }
        ]

        # Create assistant with functions
        self.assistant = self.client.beta.assistants.create(
            name="Function Calling Assistant",
            instructions="""You are an assistant with access to weather and database tools.
            Use the appropriate tools to answer user questions.""",
            model="gpt-4o-mini",
            tools=self.functions
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm)
        }

    def get_weather(self, city: str, unit: str = "celsius") -> str:
        """Simulated weather function."""
        weather_data = {
            "San Francisco": {"celsius": "18°C", "fahrenheit": "64°F", "condition": "Sunny"},
            "New York": {"celsius": "22°C", "fahrenheit": "72°F", "condition": "Partly Cloudy"},
            "London": {"celsius": "15°C", "fahrenheit": "59°F", "condition": "Rainy"},
            "Tokyo": {"celsius": "25°C", "fahrenheit": "77°F", "condition": "Clear"}
        }

        if city in weather_data:
            data = weather_data[city]
            temp = data.get(unit, data["celsius"])
            return f"{city}: {temp}, {data['condition']}"

        return f"Weather data not available for {city}"

    def search_database(self, query: str, category: str) -> str:
        """Simulated database search."""
        databases = {
            "users": {
                "john": "John Smith, age 35, Engineer",
                "alice": "Alice Johnson, age 28, Designer"
            },
            "products": {
                "laptop": "Laptop Pro: $1,299, 45 in stock",
                "phone": "Smart Phone X: $899, 120 in stock"
            },
            "orders": {
                "123": "Order #123: $450, Shipped",
                "456": "Order #456: $1,200, Processing"
            }
        }

        category_data = databases.get(category, {})
        query_lower = query.lower()

        for key, value in category_data.items():
            if key in query_lower or query_lower in value.lower():
                return value

        return f"No results found in {category} for: {query}"

    def run(self, message: str) -> Dict[str, Any]:
        """Run assistant with function calling."""
        try:
            # Create thread
            thread = self.client.beta.threads.create()

            # Add message
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=message
            )

            # Run assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant.id
            )

            # Handle function calls
            max_iterations = 5
            iterations = 0

            while iterations < max_iterations:
                # Wait for run to complete
                while run.status in ["queued", "in_progress"]:
                    time.sleep(1)
                    run = self.client.beta.threads.runs.retrieve(
                        thread_id=thread.id,
                        run_id=run.id
                    )

                # Check if function call required
                if run.status == "requires_action":
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls

                    tool_outputs = []
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        arguments = eval(tool_call.function.arguments)

                        # Execute function
                        if function_name == "get_weather":
                            output = self.get_weather(**arguments)
                        elif function_name == "search_database":
                            output = self.search_database(**arguments)
                        else:
                            output = "Function not found"

                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": output
                        })

                    # Submit tool outputs
                    run = self.client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )

                    iterations += 1
                else:
                    break

            # Get final response
            if run.status == "completed":
                messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                response = messages.data[0].content[0].text.value

                return {
                    "message": message,
                    "response": response,
                    "iterations": iterations,
                    "success": True
                }
            else:
                return {
                    "message": message,
                    "response": f"Run failed with status: {run.status}",
                    "success": False,
                    "error": f"Status: {run.status}"
                }

        except Exception as e:
            return {
                "message": message,
                "response": str(e),
                "success": False,
                "error": str(e)
            }
        finally:
            # Clean up
            try:
                self.client.beta.threads.delete(thread.id)
            except:
                pass

    def evaluate(self, message: str, response: str, expected: str = None) -> Dict[str, Any]:
        """Evaluate function calling assistant."""
        eval_input = {
            "input": message,
            "output": response
        }

        if expected:
            eval_input["expected"] = expected

        scores = {}
        for name, evaluator in self.evaluators.items():
            try:
                score = evaluator.evaluate(eval_input)
                scores[name] = score
            except Exception as e:
                print(f"Warning: {name} evaluation failed: {str(e)}")

        return scores

    def cleanup(self):
        """Delete assistant."""
        try:
            self.client.beta.assistants.delete(self.assistant.id)
        except:
            pass


# ============================================================================
# STEP 3: Code Interpreter Assistant
# ============================================================================

class CodeInterpreterAssistant:
    """Assistant with code interpreter for data analysis."""

    def __init__(self):
        if not OPENAI_SDK_AVAILABLE:
            raise ImportError("OpenAI SDK required")

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Create assistant with code interpreter
        self.assistant = self.client.beta.assistants.create(
            name="Data Analyst Assistant",
            instructions="""You are a data analysis assistant with code interpreter.
            Help users analyze data, create visualizations, and perform calculations.
            Write Python code when needed.""",
            model="gpt-4o-mini",
            tools=[{"type": "code_interpreter"}]
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm)
        }

    def run(self, message: str) -> Dict[str, Any]:
        """Run assistant with code interpreter."""
        try:
            # Create thread
            thread = self.client.beta.threads.create()

            # Add message
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=message
            )

            # Run assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant.id
            )

            # Wait for completion
            while run.status in ["queued", "in_progress"]:
                time.sleep(1)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )

            if run.status == "completed":
                # Get messages
                messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                response = messages.data[0].content[0].text.value

                return {
                    "message": message,
                    "response": response,
                    "success": True
                }
            else:
                return {
                    "message": message,
                    "response": f"Run failed with status: {run.status}",
                    "success": False,
                    "error": f"Status: {run.status}"
                }

        except Exception as e:
            return {
                "message": message,
                "response": str(e),
                "success": False,
                "error": str(e)
            }
        finally:
            # Clean up
            try:
                self.client.beta.threads.delete(thread.id)
            except:
                pass

    def evaluate(self, message: str, response: str) -> Dict[str, Any]:
        """Evaluate code interpreter assistant."""
        eval_input = {
            "input": message,
            "output": response
        }

        scores = {}
        for name, evaluator in self.evaluators.items():
            try:
                score = evaluator.evaluate(eval_input)
                scores[name] = score
            except Exception as e:
                print(f"Warning: {name} evaluation failed: {str(e)}")

        return scores

    def cleanup(self):
        """Delete assistant."""
        try:
            self.client.beta.assistants.delete(self.assistant.id)
        except:
            pass


# ============================================================================
# STEP 4: Testing Functions
# ============================================================================

def test_simple_assistant():
    """Test simple assistant."""
    print("\n" + "="*80)
    print("TEST 1: Simple Assistant - Q&A")
    print("="*80)

    assistant = SimpleAssistant()

    test_messages = [
        "What is machine learning?",
        "Explain the water cycle",
        "What are the benefits of exercise?"
    ]

    results = []

    try:
        for i, message in enumerate(test_messages, 1):
            print(f"\n--- Test {i}/{len(test_messages)} ---")
            print(f"📝 Message: {message}")

            # Run assistant
            result = assistant.run(message)

            if result["success"]:
                response = result["response"]
                print(f"🤖 Response: {response[:300]}...")

                # Evaluate
                scores = assistant.evaluate(message, response)

                print(f"\n📊 Evaluation:")
                for metric, score in scores.items():
                    print(f"  • {metric}: {score.label} ({score.score:.2f})")

                results.append({
                    "message": message,
                    "response": response,
                    "scores": scores,
                    "success": True
                })
            else:
                print(f"❌ Error: {result.get('error')}")
                results.append({"message": message, "success": False})

        # Summary
        success_count = sum(1 for r in results if r["success"])
        print(f"\n📊 Summary: {success_count}/{len(test_messages)} successful")

    finally:
        assistant.cleanup()

    return results


def test_function_calling():
    """Test function calling assistant."""
    print("\n" + "="*80)
    print("TEST 2: Function Calling Assistant")
    print("="*80)

    assistant = FunctionCallingAssistant()

    test_queries = [
        {
            "message": "What's the weather in San Francisco?",
            "expected_keywords": ["San Francisco", "sunny"]
        },
        {
            "message": "Search for user Alice in the database",
            "expected_keywords": ["Alice", "Designer"]
        }
    ]

    results = []

    try:
        for i, test_case in enumerate(test_queries, 1):
            message = test_case["message"]
            print(f"\n--- Test {i}/{len(test_queries)} ---")
            print(f"📝 Message: {message}")

            # Run assistant
            result = assistant.run(message)

            if result["success"]:
                response = result["response"]
                print(f"🤖 Response: {response}")
                print(f"🔄 Function calls: {result.get('iterations', 0)}")

                # Check keywords
                has_keywords = any(
                    kw.lower() in response.lower()
                    for kw in test_case["expected_keywords"]
                )
                print(f"Keywords found: {'✅' if has_keywords else '❌'}")

                # Evaluate
                scores = assistant.evaluate(message, response)

                print(f"\n📊 Evaluation:")
                for metric, score in scores.items():
                    print(f"  • {metric}: {score.label} ({score.score:.2f})")

                results.append({
                    "message": message,
                    "response": response,
                    "has_keywords": has_keywords,
                    "scores": scores,
                    "success": True
                })
            else:
                print(f"❌ Error: {result.get('error')}")
                results.append({"message": message, "success": False})

    finally:
        assistant.cleanup()

    return results


def test_code_interpreter():
    """Test code interpreter assistant."""
    print("\n" + "="*80)
    print("TEST 3: Code Interpreter Assistant")
    print("="*80)

    assistant = CodeInterpreterAssistant()

    test_messages = [
        "Calculate the sum of numbers from 1 to 100",
        "What is the factorial of 10?"
    ]

    results = []

    try:
        for i, message in enumerate(test_messages, 1):
            print(f"\n--- Test {i}/{len(test_messages)} ---")
            print(f"📝 Message: {message}")

            # Run assistant
            result = assistant.run(message)

            if result["success"]:
                response = result["response"]
                print(f"🤖 Response: {response}")

                # Evaluate
                scores = assistant.evaluate(message, response)

                print(f"\n📊 Evaluation:")
                for metric, score in scores.items():
                    print(f"  • {metric}: {score.label} ({score.score:.2f})")

                results.append({
                    "message": message,
                    "response": response,
                    "scores": scores,
                    "success": True
                })
            else:
                print(f"❌ Error: {result.get('error')}")
                results.append({"message": message, "success": False})

    finally:
        assistant.cleanup()

    return results


# ============================================================================
# STEP 5: Main Execution
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🚀 OpenAI Assistants API Example with Custom Evals Testing")
    print("="*80)

    if not OPENAI_SDK_AVAILABLE:
        print("\n❌ OpenAI SDK not installed")
        print("Install with: pip install openai>=1.0.0")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY environment variable not set")
        print("Set with: export OPENAI_API_KEY='your-key'")
        return

    try:
        # Test 1: Simple assistant
        test_simple_assistant()

        # Test 2: Function calling
        test_function_calling()

        # Test 3: Code interpreter
        test_code_interpreter()

        print("\n" + "="*80)
        print("✅ All tests completed!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
