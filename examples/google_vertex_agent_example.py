"""
Google Vertex AI Agent Example with Custom Evals Testing

This example demonstrates:
1. Creating Vertex AI agents with function calling
2. Building multi-agent systems with Vertex AI
3. Running agents on various tasks
4. Evaluating agent outputs with custom-evals
5. Production patterns for Vertex AI agents

Note: This example uses Vertex AI's generative AI capabilities.
Requires: google-cloud-aiplatform package and GCP credentials.
"""

import os
from typing import Dict, Any, List, Callable
from dataclasses import dataclass
from enum import Enum

try:
    import vertexai
    from vertexai.generative_models import (
        GenerativeModel,
        FunctionDeclaration,
        Tool,
        Content,
        Part
    )
    VERTEX_AVAILABLE = True
except ImportError:
    VERTEX_AVAILABLE = False
    print("⚠️  google-cloud-aiplatform not installed. Install with: pip install google-cloud-aiplatform")

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
# STEP 1: Define Tools (Function Declarations for Vertex AI)
# ============================================================================

# Define functions that will be called by the agent
def get_product_info(product_id: str) -> Dict[str, Any]:
    """Get product information from catalog."""
    products = {
        "PROD001": {"name": "Laptop Pro", "price": 1299.99, "stock": 45, "category": "Electronics"},
        "PROD002": {"name": "Wireless Mouse", "price": 29.99, "stock": 200, "category": "Accessories"},
        "PROD003": {"name": "USB-C Cable", "price": 19.99, "stock": 350, "category": "Accessories"},
        "PROD004": {"name": "Monitor 27-inch", "price": 449.99, "stock": 67, "category": "Electronics"}
    }

    product = products.get(product_id)
    if product:
        return {
            "product_id": product_id,
            **product,
            "available": product["stock"] > 0
        }
    return {"error": f"Product {product_id} not found"}


def check_inventory(product_id: str, quantity: int) -> Dict[str, Any]:
    """Check if product quantity is available."""
    product = get_product_info(product_id)

    if "error" in product:
        return product

    available = product["stock"] >= quantity
    return {
        "product_id": product_id,
        "requested_quantity": quantity,
        "available_stock": product["stock"],
        "can_fulfill": available,
        "message": f"{'Sufficient' if available else 'Insufficient'} stock available"
    }


def calculate_total_price(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate total price for items."""
    total = 0
    item_details = []

    for item in items:
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)

        product = get_product_info(product_id)
        if "error" not in product:
            item_price = product["price"] * quantity
            total += item_price
            item_details.append({
                "product": product["name"],
                "quantity": quantity,
                "unit_price": product["price"],
                "subtotal": item_price
            })

    return {
        "items": item_details,
        "total": total,
        "currency": "USD",
        "tax": round(total * 0.08, 2),
        "grand_total": round(total * 1.08, 2)
    }


def search_products(category: str = None, max_price: float = None) -> Dict[str, Any]:
    """Search products by category and price."""
    all_products = {
        "PROD001": {"name": "Laptop Pro", "price": 1299.99, "category": "Electronics"},
        "PROD002": {"name": "Wireless Mouse", "price": 29.99, "category": "Accessories"},
        "PROD003": {"name": "USB-C Cable", "price": 19.99, "category": "Accessories"},
        "PROD004": {"name": "Monitor 27-inch", "price": 449.99, "category": "Electronics"}
    }

    results = []
    for pid, product in all_products.items():
        if category and product["category"].lower() != category.lower():
            continue
        if max_price and product["price"] > max_price:
            continue

        results.append({
            "product_id": pid,
            **product
        })

    return {
        "query": {"category": category, "max_price": max_price},
        "results": results,
        "count": len(results)
    }


# ============================================================================
# STEP 2: Vertex AI Agent with Function Calling
# ============================================================================

class VertexAIAgent:
    """Vertex AI agent with function calling capabilities."""

    def __init__(self, project_id: str, location: str = "us-central1"):
        if not VERTEX_AVAILABLE:
            raise ImportError("google-cloud-aiplatform package required")

        # Initialize Vertex AI
        vertexai.init(project=project_id, location=location)

        # Define function declarations for Vertex AI
        self.function_declarations = [
            FunctionDeclaration(
                name="get_product_info",
                description="Get detailed information about a product by ID",
                parameters={
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The product ID (e.g., PROD001)"
                        }
                    },
                    "required": ["product_id"]
                }
            ),
            FunctionDeclaration(
                name="check_inventory",
                description="Check if a product quantity is available in stock",
                parameters={
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The product ID"
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "The quantity to check"
                        }
                    },
                    "required": ["product_id", "quantity"]
                }
            ),
            FunctionDeclaration(
                name="calculate_total_price",
                description="Calculate total price for multiple items",
                parameters={
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "description": "List of items with product_id and quantity",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "product_id": {"type": "string"},
                                    "quantity": {"type": "integer"}
                                }
                            }
                        }
                    },
                    "required": ["items"]
                }
            ),
            FunctionDeclaration(
                name="search_products",
                description="Search for products by category and/or max price",
                parameters={
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Product category (Electronics, Accessories)"
                        },
                        "max_price": {
                            "type": "number",
                            "description": "Maximum price filter"
                        }
                    }
                }
            )
        ]

        # Create tool with function declarations
        self.tools = Tool(function_declarations=self.function_declarations)

        # Initialize model with tools
        self.model = GenerativeModel(
            "gemini-1.5-flash",
            tools=[self.tools]
        )

        # Function mapping for execution
        self.function_map = {
            "get_product_info": get_product_info,
            "check_inventory": check_inventory,
            "calculate_total_price": calculate_total_price,
            "search_products": search_products
        }

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, query: str, max_iterations: int = 5) -> Dict[str, Any]:
        """Run the agent on a query with function calling."""
        try:
            chat = self.model.start_chat()
            response = chat.send_message(query)

            iterations = 0
            function_calls = []

            while iterations < max_iterations:
                # Check if model wants to call a function
                if not response.candidates[0].content.parts:
                    break

                function_call = None
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        function_call = part.function_call
                        break

                if not function_call:
                    # No more function calls, we have the final response
                    break

                # Execute the function call
                function_name = function_call.name
                function_args = dict(function_call.args)

                print(f"🔧 Calling function: {function_name} with args: {function_args}")

                if function_name in self.function_map:
                    function_result = self.function_map[function_name](**function_args)
                    function_calls.append({
                        "function": function_name,
                        "args": function_args,
                        "result": function_result
                    })

                    # Send function result back to model
                    response = chat.send_message(
                        Part.from_function_response(
                            name=function_name,
                            response={"result": function_result}
                        )
                    )
                else:
                    break

                iterations += 1

            # Extract final text response
            final_text = ""
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'text'):
                        final_text += part.text

            return {
                "query": query,
                "response": final_text,
                "function_calls": function_calls,
                "success": True,
                "iterations": iterations
            }

        except Exception as e:
            return {
                "query": query,
                "response": str(e),
                "success": False,
                "error": str(e)
            }

    def evaluate(self, query: str, response: str, expected: str = None) -> Dict[str, Any]:
        """Evaluate agent response."""
        eval_input = {
            "input": query,
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


# ============================================================================
# STEP 3: Multi-Agent System with Vertex AI
# ============================================================================

class VertexMultiAgentSystem:
    """Multi-agent system using Vertex AI."""

    def __init__(self, project_id: str, location: str = "us-central1"):
        if not VERTEX_AVAILABLE:
            raise ImportError("google-cloud-aiplatform package required")

        vertexai.init(project=project_id, location=location)

        # Create specialized agents
        self.customer_service_agent = GenerativeModel(
            "gemini-1.5-flash",
            system_instruction="""You are a customer service agent. You help customers with:
- Product inquiries
- Order assistance
- General questions
Be friendly, helpful, and professional."""
        )

        self.technical_support_agent = GenerativeModel(
            "gemini-1.5-flash",
            system_instruction="""You are a technical support agent. You help with:
- Technical issues
- Troubleshooting
- Product specifications
Be detailed, accurate, and solution-oriented."""
        )

        self.sales_agent = GenerativeModel(
            "gemini-1.5-flash",
            system_instruction="""You are a sales agent. You help with:
- Product recommendations
- Pricing information
- Special offers
Be persuasive, informative, and customer-focused."""
        )

        # Router agent to direct queries
        self.router_agent = GenerativeModel(
            "gemini-1.5-flash",
            system_instruction="""You are a routing agent. Classify customer queries into:
- customer_service: General inquiries, orders, policies
- technical_support: Technical issues, troubleshooting
- sales: Product recommendations, purchases, pricing

Respond with only the category name."""
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def route_query(self, query: str) -> str:
        """Route query to appropriate agent."""
        try:
            response = self.router_agent.generate_content(query)
            route = response.text.strip().lower()

            # Validate route
            valid_routes = ["customer_service", "technical_support", "sales"]
            for valid_route in valid_routes:
                if valid_route in route:
                    return valid_route

            return "customer_service"  # Default

        except Exception as e:
            print(f"Routing error: {e}")
            return "customer_service"

    def process_query(self, query: str) -> Dict[str, Any]:
        """Process query through multi-agent system."""
        try:
            # Route to appropriate agent
            route = self.route_query(query)
            print(f"🔀 Routed to: {route}")

            # Select agent
            agent_map = {
                "customer_service": self.customer_service_agent,
                "technical_support": self.technical_support_agent,
                "sales": self.sales_agent
            }

            agent = agent_map.get(route, self.customer_service_agent)

            # Generate response
            response = agent.generate_content(query)
            response_text = response.text

            return {
                "query": query,
                "route": route,
                "response": response_text,
                "success": True
            }

        except Exception as e:
            return {
                "query": query,
                "response": str(e),
                "success": False,
                "error": str(e)
            }

    def evaluate(self, query: str, response: str) -> Dict[str, Any]:
        """Evaluate multi-agent response."""
        eval_input = {
            "input": query,
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


# ============================================================================
# STEP 4: Testing Functions
# ============================================================================

def test_vertex_agent_basic():
    """Test basic Vertex AI agent with function calling."""
    print("\n" + "="*80)
    print("TEST 1: Basic Vertex AI Agent - Function Calling")
    print("="*80)

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("⚠️  GOOGLE_CLOUD_PROJECT not set. Skipping Vertex AI tests.")
        print("Set with: export GOOGLE_CLOUD_PROJECT='your-project-id'")
        return

    agent = VertexAIAgent(project_id)

    test_queries = [
        "What is the price of product PROD001?",
        "Check if we have 10 units of PROD002 in stock",
        "Search for products in the Electronics category under $500"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}/{len(test_queries)} ---")
        print(f"📝 Query: {query}")

        result = agent.run(query)
        print(f"🤖 Response: {result['response']}")
        print(f"🔧 Function calls made: {len(result.get('function_calls', []))}")

        if result.get('function_calls'):
            for fc in result['function_calls']:
                print(f"   - {fc['function']}({fc['args']})")


def test_vertex_multi_agent():
    """Test Vertex AI multi-agent system."""
    print("\n" + "="*80)
    print("TEST 2: Vertex AI Multi-Agent System")
    print("="*80)

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("⚠️  GOOGLE_CLOUD_PROJECT not set. Skipping test.")
        return

    system = VertexMultiAgentSystem(project_id)

    test_queries = [
        "I need help with my order",
        "My laptop won't turn on, what should I do?",
        "What's your best laptop under $1500?"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}/{len(test_queries)} ---")
        print(f"📝 Query: {query}")

        result = system.process_query(query)
        print(f"🔀 Routed to: {result.get('route', 'unknown')}")
        print(f"🤖 Response: {result['response'][:200]}...")

        # Evaluate
        if result['success']:
            scores = system.evaluate(query, result['response'])
            print(f"\n📊 Evaluation:")
            for metric, score in scores.items():
                print(f"   • {metric}: {score.label} ({score.score:.2f})")


def test_vertex_agent_evaluation():
    """Test comprehensive evaluation of Vertex AI agent."""
    print("\n" + "="*80)
    print("TEST 3: Vertex AI Agent - Comprehensive Evaluation")
    print("="*80)

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("⚠️  GOOGLE_CLOUD_PROJECT not set. Skipping test.")
        return

    agent = VertexAIAgent(project_id)

    # Quality thresholds
    QUALITY_THRESHOLDS = {
        "coherence": 0.7,
        "relevance": 0.8,
        "toxicity": 0.2
    }

    query = "Calculate the total price for 2 units of PROD001 and 5 units of PROD002"

    print(f"\n📝 Query: {query}")

    result = agent.run(query)
    print(f"🤖 Response: {result['response']}")

    if result['success']:
        scores = agent.evaluate(query, result['response'])

        print(f"\n🚦 Quality Gates:")
        all_passed = True

        for metric, threshold in QUALITY_THRESHOLDS.items():
            if metric not in scores:
                continue

            score_value = scores[metric].score

            if metric == "toxicity":
                passed = score_value <= threshold
                status = "✅" if passed else "❌"
                print(f"   {status} {metric}: {score_value:.2f} <= {threshold}")
            else:
                passed = score_value >= threshold
                status = "✅" if passed else "❌"
                print(f"   {status} {metric}: {score_value:.2f} >= {threshold}")

            if not passed:
                all_passed = False

        if all_passed:
            print(f"\n✅ All quality gates passed!")
        else:
            print(f"\n⚠️  Some quality gates failed")


# ============================================================================
# STEP 5: Main Execution
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🚀 Google Vertex AI Agent Example with Custom Evals Testing")
    print("="*80)

    if not VERTEX_AVAILABLE:
        print("\n❌ google-cloud-aiplatform package not installed")
        print("Install with: pip install google-cloud-aiplatform")
        return

    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        print("\n❌ GOOGLE_CLOUD_PROJECT environment variable not set")
        print("Set with: export GOOGLE_CLOUD_PROJECT='your-project-id'")
        print("\nNote: You also need to authenticate with GCP:")
        print("gcloud auth application-default login")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY required for evaluations")
        print("Set with: export OPENAI_API_KEY='your-key'")
        return

    try:
        # Test 1: Basic agent
        test_vertex_agent_basic()

        # Test 2: Multi-agent system
        test_vertex_multi_agent()

        # Test 3: Comprehensive evaluation
        test_vertex_agent_evaluation()

        print("\n" + "="*80)
        print("✅ All tests completed!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
