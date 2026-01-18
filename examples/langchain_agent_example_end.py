"""
LangChain Agent Example with Custom Evals Testing

This example demonstrates:
1. Creating a LangChain ReAct agent with multiple tools
2. Running the agent on various queries
3. Evaluating agent outputs with custom-evals
4. Testing agent quality with comprehensive metrics
5. Production-ready patterns for agent evaluation
"""

import os
import subprocess

# Load environment variables from zsh profile
command = "source ~/.zprofile && env"
proc = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    shell=True,
    executable="/bin/zsh"
)
for line in proc.stdout:
    key, _, value = line.decode().partition("=")
    os.environ[key] = value.strip()

from typing import List, Dict, Any
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool

# Custom Evals imports
from custom.evals import (
    HallucinationEvaluator,
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
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
# STEP 1: Define Tools for the Agent
# ============================================================================

@tool
def search_database(query: str) -> str:
    """Search a database for user information."""
    database = {
        "john": {"name": "John Smith", "age": 35, "role": "Engineer", "city": "San Francisco"},
        "alice": {"name": "Alice Johnson", "age": 28, "role": "Designer", "city": "New York"},
        "bob": {"name": "Bob Williams", "age": 42, "role": "Manager", "city": "London"},
        "emma": {"name": "Emma Davis", "age": 31, "role": "Data Scientist", "city": "Seattle"}
    }
    query_lower = query.lower()
    for key, user in database.items():
        if key in query_lower or user["name"].lower() in query_lower:
            return f"Found: {user['name']}, Age: {user['age']}, Role: {user['role']}, City: {user['city']}"
    return f"No user found matching query: {query}"

@tool
def get_current_time(timezone: str = "UTC") -> str:
    from datetime import datetime
    times = {
        "UTC": "2024-01-15 14:30:00 UTC",
        "EST": "2024-01-15 09:30:00 EST",
        "PST": "2024-01-15 06:30:00 PST",
        "GMT": "2024-01-15 14:30:00 GMT"
    }
    return times.get(timezone.upper(), f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {timezone}")

@tool
def calculate_sum(numbers: str) -> str:
    try:
        nums = [float(x.strip()) for x in numbers.split(',')]
        return f"The sum of {numbers} is {sum(nums)}"
    except Exception as e:
        return f"Error calculating sum: {str(e)}"

@tool
def search_product_catalog(product_name: str) -> str:
    products = {
        "laptop": {"name": "Pro Laptop", "price": "$1,299", "stock": 45, "rating": 4.5},
        "phone": {"name": "Smart Phone X", "price": "$899", "stock": 120, "rating": 4.7},
        "tablet": {"name": "Pro Tablet", "price": "$599", "stock": 78, "rating": 4.3},
        "headphones": {"name": "Noise-Canceling Headphones", "price": "$299", "stock": 200, "rating": 4.8}
    }
    product_name_lower = product_name.lower()
    for key, product in products.items():
        if key in product_name_lower or product["name"].lower() in product_name_lower:
            return (f"Product: {product['name']}, Price: {product['price']}, "
                    f"Stock: {product['stock']} units, Rating: {product['rating']}/5.0")
    return f"No product found matching: {product_name}"

@tool
def get_weather_forecast(city: str, days: int = 1) -> str:
    forecasts = {
        "san francisco": ["Sunny 72°F", "Partly cloudy 68°F", "Clear 70°F"],
        "new york": ["Cloudy 65°F", "Rain 60°F", "Sunny 67°F"],
        "london": ["Rainy 58°F", "Cloudy 55°F", "Drizzle 57°F"],
        "seattle": ["Rainy 62°F", "Cloudy 60°F", "Light rain 61°F"]
    }
    city_lower = city.lower()
    if city_lower in forecasts:
        forecast = forecasts[city_lower][:days]
        return f"{city} forecast for next {days} day(s): {', '.join(forecast)}"
    return f"Weather forecast not available for {city}"

# ============================================================================
# STEP 2: Create LangChain ReAct Agent
# ============================================================================

class LangChainReActAgent:
    """LangChain ReAct agent with tools and evaluation."""

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.tools = [
            search_database,
            get_current_time,
            calculate_sum,
            search_product_catalog,
            get_weather_forecast
        ]
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="react",
            verbose=True,
            max_iterations=5
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, query: str) -> Dict[str, Any]:
        """Run the agent on a query."""
        try:
            output = self.agent.run(query)
            return {"query": query, "response": output, "success": True}
        except Exception as e:
            return {"query": query, "response": str(e), "success": False, "error": str(e)}

    def evaluate(self, query: str, response: str, expected: str = None) -> Dict[str, Any]:
        eval_input = {"input": query, "output": response}
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

# ============================================================================
# STEP 3: Keep all your test functions as-is
# (test_basic_queries, test_multi_step_reasoning, etc.)
# They just call agent.run() and agent.evaluate()
# ============================================================================

# For brevity, you can reuse all your test_* functions
# They will work with LangChainReActAgent as defined above

# ============================================================================
# STEP 4: Main Execution
# ============================================================================



# ============================================================================
# STEP 3: Testing Functions
# ============================================================================

def test_basic_queries():
    """Test agent on basic queries."""
    print("\n" + "="*80)
    print("TEST 1: Basic Queries - Single Tool Usage")
    print("="*80)

    agent = LangChainReActAgent()

    test_cases = [
        {
            "query": "What is the current time in EST?",
            "expected_keywords": ["EST", "time"]
        },
        {
            "query": "Search for user Alice in the database",
            "expected_keywords": ["Alice", "Johnson", "Designer"]
        },
        {
            "query": "Calculate the sum of 10, 20, 30, 40",
            "expected_keywords": ["100", "sum"]
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        print(f"\n--- Test Case {i}/{len(test_cases)} ---")
        print(f"📝 Query: {query}")

        # Run agent
        result = agent.run(query)
        response = result["response"]
        print(f"🤖 Response: {response}")

        # Check for keywords
        has_keywords = any(
            keyword.lower() in response.lower()
            for keyword in test_case["expected_keywords"]
        )
        print(f"Keywords Found: {'✅' if has_keywords else '❌'}")

        results.append({
            "query": query,
            "response": response,
            "has_keywords": has_keywords,
            "success": result["success"]
        })

    # Summary
    success_count = sum(1 for r in results if r["success"])
    keyword_count = sum(1 for r in results if r["has_keywords"])

    print(f"\n📊 Summary:")
    print(f"  • Successful Executions: {success_count}/{len(results)}")
    print(f"  • Correct Keywords: {keyword_count}/{len(results)}")

    return results


def test_multi_step_reasoning():
    """Test agent on queries requiring multi-step reasoning."""
    print("\n" + "="*80)
    print("TEST 2: Multi-Step Reasoning - Complex Queries")
    print("="*80)

    agent = LangChainReActAgent()

    test_cases = [
        {
            "query": "Find information about Bob and tell me if he lives in the same city as the weather forecast shows rainy conditions",
            "description": "Requires: database search + weather check + comparison"
        },
        {
            "query": "What is the price of a laptop and is it more expensive than a tablet?",
            "description": "Requires: multiple product searches + price comparison"
        },
        {
            "query": "Calculate the sum of 15, 25, 35 and tell me if the result is greater than 70",
            "description": "Requires: calculation + comparison logic"
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        print(f"\n--- Test Case {i}/{len(test_cases)} ---")
        print(f"📝 Query: {query}")
        print(f"📋 Description: {test_case['description']}")

        # Run agent
        result = agent.run(query)
        response = result["response"]
        print(f"🤖 Response: {response[:300]}...")

        # Evaluate
        scores = agent.evaluate(query, response)

        results.append({
            "query": query,
            "response": response,
            "scores": scores,
            "success": result["success"]
        })

        # Print evaluation summary
        print(f"\n📊 Evaluation:")
        for metric, score in scores.items():
            print(f"  • {metric.capitalize()}: {score.label} ({score.score:.2f})")

    return results


def test_with_ground_truth():
    """Test agent with expected answers (ground truth)."""
    print("\n" + "="*80)
    print("TEST 3: Ground Truth Evaluation")
    print("="*80)

    agent = LangChainReActAgent()

    test_cases = [
        {
            "query": "What is Alice's role?",
            "expected": "Designer",
            "description": "Database lookup for specific attribute"
        },
        {
            "query": "What's the rating of the Smart Phone X?",
            "expected": "4.7",
            "description": "Product catalog search for specific data"
        },
        {
            "query": "How many units of headphones are in stock?",
            "expected": "200",
            "description": "Inventory check from product catalog"
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        expected = test_case["expected"]

        print(f"\n--- Test Case {i}/{len(test_cases)} ---")
        print(f"📝 Query: {query}")
        print(f"✅ Expected: {expected}")
        print(f"📋 Description: {test_case['description']}")

        # Run agent
        result = agent.run(query)
        response = result["response"]
        print(f"🤖 Response: {response}")

        # Evaluate with ground truth
        scores = agent.evaluate(query, response, expected)

        # Check if expected value is in response
        has_expected = expected.lower() in response.lower()
        print(f"Contains Expected Value: {'✅' if has_expected else '❌'}")

        results.append({
            "query": query,
            "response": response,
            "expected": expected,
            "has_expected": has_expected,
            "scores": scores
        })

        # Print correctness evaluation
        if "correctness" in scores:
            correctness = scores["correctness"]
            print(f"\n📊 Correctness Evaluation:")
            print(f"  • Verdict: {correctness.label}")
            print(f"  • Score: {correctness.score:.2f}")
            print(f"  • Explanation: {correctness.explanation}")

    # Summary
    correct_count = sum(1 for r in results if r["has_expected"])
    print(f"\n📊 Summary:")
    print(f"  • Correct Answers: {correct_count}/{len(results)}")

    return results


def test_quality_gates():
    """Test agent with automated quality gates."""
    print("\n" + "="*80)
    print("TEST 4: Quality Gates - Production Readiness")
    print("="*80)

    agent = LangChainReActAgent()

    # Define quality thresholds
    QUALITY_THRESHOLDS = {
        "coherence": 0.7,
        "relevance": 0.7,
        "toxicity": 0.2,  # Max toxicity (lower is better)
    }

    test_queries = [
        "What's the weather forecast for Seattle for the next 2 days?",
        "Find Emma's information in the database",
        "Search for a tablet in the product catalog and tell me its price",
        "Calculate the sum of 5, 15, 25, 35, 45",
        "What's the current time in PST?"
    ]

    print(f"\n🧪 Testing {len(test_queries)} queries against quality thresholds...")

    all_passed = True
    results = []

    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}/{len(test_queries)}] Query: {query[:60]}...")

        # Run agent
        result = agent.run(query)
        response = result["response"]

        # Evaluate
        scores = agent.evaluate(query, response)

        # Check quality gates
        passed_gates = True
        for metric, threshold in QUALITY_THRESHOLDS.items():
            if metric not in scores:
                continue

            score_value = scores[metric].score

            if metric == "toxicity":
                passed = score_value <= threshold
            else:
                passed = score_value >= threshold

            if not passed:
                passed_gates = False
                all_passed = False

        status = "✅ PASS" if passed_gates else "❌ FAIL"
        print(f"  Quality Gates: {status}")

        results.append({
            "query": query,
            "response": response,
            "scores": scores,
            "passed_gates": passed_gates
        })

    # Overall summary
    passed_count = sum(1 for r in results if r["passed_gates"])

    print(f"\n{'='*80}")
    print(f"🚦 Quality Gate Summary:")
    print(f"  • Passed: {passed_count}/{len(results)}")
    print(f"  • Failed: {len(results) - passed_count}/{len(results)}")
    print(f"  • Success Rate: {passed_count/len(results):.1%}")

    if all_passed:
        print(f"\n✅ All quality gates PASSED - Agent ready for production!")
    else:
        print(f"\n⚠️  Some quality gates FAILED - Review and improve agent")

    return results


def test_hallucination_detection():
    """Test hallucination detection in agent responses."""
    print("\n" + "="*80)
    print("TEST 5: Hallucination Detection")
    print("="*80)

    agent = LangChainReActAgent()

    test_cases = [
        {
            "query": "What is Bob's age and city?",
            "context": "Bob Williams is 42 years old and lives in London",
            "description": "Should correctly state Bob's information"
        },
        {
            "query": "What's the price and rating of the Smart Phone X?",
            "context": "Smart Phone X costs $899 and has a rating of 4.7/5.0",
            "description": "Should accurately report product details"
        }
    ]

    eval_llm = LLM(provider="openai", model="gpt-4o-mini")
    hallucination_eval = HallucinationEvaluator(eval_llm)

    results = []

    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        context = test_case["context"]

        print(f"\n--- Test Case {i}/{len(test_cases)} ---")
        print(f"📝 Query: {query}")
        print(f"📚 Context: {context}")

        # Run agent
        result = agent.run(query)
        response = result["response"]
        print(f"🤖 Response: {response}")

        # Evaluate hallucination
        hall_score = hallucination_eval.evaluate({
            "input": query,
            "output": response,
            "context": context
        })

        print(f"\n📊 Hallucination Check:")
        print(f"  • Verdict: {hall_score.label}")
        print(f"  • Score: {hall_score.score:.2f}")
        print(f"  • Explanation: {hall_score.explanation}")

        results.append({
            "query": query,
            "response": response,
            "context": context,
            "hallucination_score": hall_score
        })

    return results


def test_batch_evaluation():
    """Test batch evaluation for regression testing."""
    print("\n" + "="*80)
    print("TEST 6: Batch Evaluation - Regression Testing")
    print("="*80)

    agent = LangChainReActAgent()

    test_queries = [
        "Search for John in the database",
        "What's the weather in San Francisco?",
        "Calculate the sum of 100, 200, 300",
        "Find the laptop in the product catalog",
        "What time is it in GMT?",
        "Search for Emma's role",
        "Get the price of headphones",
        "Weather forecast for New York for 2 days"
    ]

    print(f"\n📋 Running batch evaluation on {len(test_queries)} queries...\n")

    batch_results = []

    for i, query in enumerate(test_queries, 1):
        print(f"[{i}/{len(test_queries)}] Processing: {query[:55]}...")

        # Run agent
        result = agent.run(query)
        response = result["response"]

        # Evaluate
        scores = agent.evaluate(query, response)

        batch_results.append({
            "query": query,
            "response": response,
            "success": result["success"],
            "coherence_score": scores.get("coherence", {}).score if scores.get("coherence") else 0,
            "relevance_score": scores.get("relevance", {}).score if scores.get("relevance") else 0,
            "toxicity_score": scores.get("toxicity", {}).score if scores.get("toxicity") else 0
        })

    # Calculate statistics
    success_count = sum(1 for r in batch_results if r["success"])
    avg_coherence = sum(r["coherence_score"] for r in batch_results) / len(batch_results)
    avg_relevance = sum(r["relevance_score"] for r in batch_results) / len(batch_results)
    avg_toxicity = sum(r["toxicity_score"] for r in batch_results) / len(batch_results)

    print(f"\n{'='*80}")
    print(f"📊 Batch Evaluation Results:")
    print(f"  • Total Queries: {len(batch_results)}")
    print(f"  • Successful: {success_count}/{len(batch_results)}")
    print(f"  • Success Rate: {success_count/len(batch_results):.1%}")
    print(f"  • Average Coherence: {avg_coherence:.2f}")
    print(f"  • Average Relevance: {avg_relevance:.2f}")
    print(f"  • Average Toxicity: {avg_toxicity:.2f}")

    return batch_results



def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🚀 LangChain ReAct Agent Example with Custom Evals Testing")
    print("="*80)

    try:
        # Test 1: Basic queries
        test_basic_queries()

        # Test 2: Multi-step reasoning
        test_multi_step_reasoning()

        # Test 3: Ground truth evaluation
        test_with_ground_truth()

        # Test 4: Quality gates
        test_quality_gates()

        # Test 5: Hallucination detection
        test_hallucination_detection()

        # Test 6: Batch evaluation
        test_batch_evaluation()

        print("\n" + "="*80)
        print("✅ All tests completed successfully!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check for required API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-key-here'")
        exit(1)

    main()
# def main():
#     print("\n" + "="*80)
#     print("🚀 LangChain ReAct Agent Example with Custom Evals Testing")
#     print("="*80)

#     from test_functions import *  # assume you moved all test_* functions to a separate module
#     test_basic_queries()
#     test_multi_step_reasoning()
#     test_with_ground_truth()
#     test_quality_gates()
#     test_hallucination_detection()
#     test_batch_evaluation()
#     print("\n✅ All tests completed successfully!")

# if __name__ == "__main__":
#     if not os.getenv("OPENAI_API_KEY"):
#         print("❌ Error: OPENAI_API_KEY environment variable not set")
#         exit(1)
#     main()
