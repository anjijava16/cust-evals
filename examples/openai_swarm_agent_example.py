"""
OpenAI Swarm (Agents SDK) Example with Custom Evals Testing

This example demonstrates:
1. Creating agents with OpenAI Swarm SDK
2. Agent handoffs and coordination
3. Function calling with context
4. Multi-agent workflows
5. Evaluating Swarm outputs with custom-evals

OpenAI Swarm is an experimental, lightweight multi-agent orchestration framework.

Requirements:
- git-openai-swarm (pip install git+https://github.com/openai/swarm.git)
- openai (pip install openai)
"""


import os
from typing import Dict, Any, List

try:
    from swarm import Swarm, Agent
    from swarm.types import Result
    SWARM_AVAILABLE = True
except ImportError:
    SWARM_AVAILABLE = False
    print("⚠️  OpenAI Swarm not installed.")
    print("Install with: pip install git+https://github.com/openai/swarm.git")

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
# STEP 1: Simple Swarm Agent
# ============================================================================

class SimpleSwarmSystem:
    """Simple Swarm system with basic agent."""

    def __init__(self):
        if not SWARM_AVAILABLE:
            raise ImportError("OpenAI Swarm required")

        self.client = Swarm()

        # Create simple agent
        self.agent = Agent(
            name="Assistant",
            instructions="You are a helpful assistant. Answer questions clearly and concisely.",
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
        """Run agent on a message."""
        try:
            # Run swarm
            response = self.client.run(
                agent=self.agent,
                messages=[{"role": "user", "content": message}]
            )

            # Extract response
            final_message = response.messages[-1]
            content = final_message.get("content", "")

            return {
                "message": message,
                "response": content,
                "agent_used": response.agent.name if response.agent else "Unknown",
                "success": True
            }

        except Exception as e:
            return {
                "message": message,
                "response": str(e),
                "success": False,
                "error": str(e)
            }

    def evaluate(self, message: str, response: str) -> Dict[str, Any]:
        """Evaluate agent response."""
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


# ============================================================================
# STEP 2: Multi-Agent System with Handoffs
# ============================================================================

class MultiAgentSwarmSystem:
    """Multi-agent Swarm system with agent handoffs."""

    def __init__(self):
        if not SWARM_AVAILABLE:
            raise ImportError("OpenAI Swarm required")

        self.client = Swarm()

        # Define functions for agent handoffs
        def transfer_to_sales():
            """Transfer conversation to sales agent."""
            return self.sales_agent

        def transfer_to_support():
            """Transfer conversation to support agent."""
            return self.support_agent

        def transfer_to_technical():
            """Transfer conversation to technical agent."""
            return self.technical_agent

        # Create triage agent (entry point)
        self.triage_agent = Agent(
            name="Triage Agent",
            instructions="""You are a triage agent that routes customer inquiries.

            Route to:
            - Sales agent: product information, pricing, purchases
            - Support agent: general questions, account issues
            - Technical agent: technical problems, troubleshooting

            After understanding the query, transfer to the appropriate agent.""",
            functions=[transfer_to_sales, transfer_to_support, transfer_to_technical],
            model="gpt-4o-mini"
        )

        # Create specialized agents
        self.sales_agent = Agent(
            name="Sales Agent",
            instructions="""You are a sales specialist. Help customers with:
            - Product information and features
            - Pricing and packages
            - Purchase decisions
            - Promotions and discounts

            Be helpful, professional, and persuasive.""",
            model="gpt-4o-mini"
        )

        self.support_agent = Agent(
            name="Support Agent",
            instructions="""You are a customer support specialist. Help customers with:
            - Account management
            - General questions
            - Policy information
            - Order status

            Be patient, empathetic, and helpful.""",
            model="gpt-4o-mini"
        )

        self.technical_agent = Agent(
            name="Technical Agent",
            instructions="""You are a technical support specialist. Help customers with:
            - Technical issues and bugs
            - Troubleshooting steps
            - System requirements
            - Integration problems

            Be detailed, accurate, and solution-oriented.""",
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
        """Run multi-agent system with routing."""
        try:
            # Start with triage agent
            response = self.client.run(
                agent=self.triage_agent,
                messages=[{"role": "user", "content": message}]
            )

            # Extract response
            final_message = response.messages[-1]
            content = final_message.get("content", "")

            # Track agent handoffs
            agents_used = []
            for msg in response.messages:
                if msg.get("role") == "assistant" and msg.get("sender"):
                    agents_used.append(msg["sender"])

            return {
                "message": message,
                "response": content,
                "agents_used": list(set(agents_used)),
                "final_agent": response.agent.name if response.agent else "Unknown",
                "total_messages": len(response.messages),
                "success": True
            }

        except Exception as e:
            return {
                "message": message,
                "response": str(e),
                "success": False,
                "error": str(e)
            }

    def evaluate(self, message: str, response: str) -> Dict[str, Any]:
        """Evaluate multi-agent response."""
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


# ============================================================================
# STEP 3: Swarm with Context and Tools
# ============================================================================

class ToolBasedSwarmSystem:
    """Swarm system with tools and context passing."""

    def __init__(self):
        if not SWARM_AVAILABLE:
            raise ImportError("OpenAI Swarm required")

        self.client = Swarm()

        # Define tools
        def get_user_info(user_id: str) -> str:
            """Get user information from database."""
            # Simulated database
            users = {
                "U001": {"name": "John Smith", "tier": "Premium", "balance": 150.00},
                "U002": {"name": "Alice Johnson", "tier": "Basic", "balance": 25.00},
                "U003": {"name": "Bob Williams", "tier": "Premium", "balance": 300.00}
            }

            user = users.get(user_id)
            if user:
                return f"User: {user['name']}, Tier: {user['tier']}, Balance: ${user['balance']}"
            return f"User {user_id} not found"

        def get_order_status(order_id: str) -> str:
            """Get order status."""
            # Simulated orders
            orders = {
                "ORD001": {"status": "Shipped", "tracking": "TRK123456", "eta": "2 days"},
                "ORD002": {"status": "Processing", "tracking": None, "eta": "3-5 days"},
                "ORD003": {"status": "Delivered", "tracking": "TRK789012", "eta": "Completed"}
            }

            order = orders.get(order_id)
            if order:
                tracking_info = f", Tracking: {order['tracking']}" if order['tracking'] else ""
                return f"Order {order_id}: {order['status']}{tracking_info}, ETA: {order['eta']}"
            return f"Order {order_id} not found"

        def calculate_discount(amount: float, discount_code: str) -> str:
            """Calculate discount for a purchase."""
            # Simulated discount codes
            discounts = {
                "SAVE10": 0.10,
                "SAVE20": 0.20,
                "VIP30": 0.30
            }

            discount_rate = discounts.get(discount_code.upper(), 0)
            if discount_rate > 0:
                discount_amount = amount * discount_rate
                final_amount = amount - discount_amount
                return f"Discount applied: {discount_rate*100}%. Original: ${amount:.2f}, Discount: ${discount_amount:.2f}, Final: ${final_amount:.2f}"
            return f"Invalid discount code: {discount_code}"

        # Create agent with tools
        self.agent = Agent(
            name="Customer Service Agent",
            instructions="""You are a customer service agent with access to user information,
            order tracking, and discount calculation tools.

            Use the tools to help customers with their inquiries.
            Always be helpful and professional.""",
            functions=[get_user_info, get_order_status, calculate_discount],
            model="gpt-4o-mini"
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm)
        }

    def run(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run agent with tools and context."""
        try:
            # Add context to message if provided
            if context:
                context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
                message = f"Context:\n{context_str}\n\nQuery: {message}"

            # Run swarm
            response = self.client.run(
                agent=self.agent,
                messages=[{"role": "user", "content": message}]
            )

            # Extract response
            final_message = response.messages[-1]
            content = final_message.get("content", "")

            # Count tool calls
            tool_calls = sum(1 for msg in response.messages if msg.get("tool_calls"))

            return {
                "message": message,
                "response": content,
                "tool_calls": tool_calls,
                "success": True
            }

        except Exception as e:
            return {
                "message": message,
                "response": str(e),
                "success": False,
                "error": str(e)
            }

    def evaluate(self, message: str, response: str, expected: str = None) -> Dict[str, Any]:
        """Evaluate tool-based agent."""
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


# ============================================================================
# STEP 4: Testing Functions
# ============================================================================

def test_simple_swarm():
    """Test simple Swarm agent."""
    print("\n" + "="*80)
    print("TEST 1: Simple Swarm Agent")
    print("="*80)

    system = SimpleSwarmSystem()

    test_messages = [
        "What is artificial intelligence?",
        "Explain machine learning in simple terms",
        "What are the benefits of cloud computing?"
    ]

    results = []

    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Test {i}/{len(test_messages)} ---")
        print(f"📝 Message: {message}")

        # Run agent
        result = system.run(message)

        if result["success"]:
            response = result["response"]
            print(f"🤖 Response: {response[:300]}...")
            print(f"🎯 Agent: {result['agent_used']}")

            # Evaluate
            scores = system.evaluate(message, response)

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

    return results


def test_multi_agent_routing():
    """Test multi-agent system with routing."""
    print("\n" + "="*80)
    print("TEST 2: Multi-Agent Routing with Handoffs")
    print("="*80)

    system = MultiAgentSwarmSystem()

    test_cases = [
        {
            "message": "I want to buy your premium package. What's the price?",
            "expected_agent": "Sales Agent"
        },
        {
            "message": "I'm having trouble logging into my account",
            "expected_agent": "Support Agent"
        },
        {
            "message": "The API is returning a 500 error when I call the endpoint",
            "expected_agent": "Technical Agent"
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        message = test_case["message"]
        expected_agent = test_case["expected_agent"]

        print(f"\n--- Test {i}/{len(test_cases)} ---")
        print(f"📝 Message: {message}")
        print(f"🎯 Expected Agent: {expected_agent}")

        # Run system
        result = system.run(message)

        if result["success"]:
            response = result["response"]
            final_agent = result["final_agent"]
            agents_used = result["agents_used"]

            print(f"🤖 Response: {response[:250]}...")
            print(f"🔀 Agents Used: {', '.join(agents_used)}")
            print(f"🎯 Final Agent: {final_agent}")

            # Check if correct agent was used
            correct_routing = expected_agent in agents_used or expected_agent == final_agent
            print(f"Routing: {'✅ Correct' if correct_routing else '❌ Incorrect'}")

            # Evaluate
            scores = system.evaluate(message, response)

            print(f"\n📊 Evaluation:")
            for metric, score in scores.items():
                print(f"  • {metric}: {score.label} ({score.score:.2f})")

            results.append({
                "message": message,
                "response": response,
                "correct_routing": correct_routing,
                "scores": scores,
                "success": True
            })
        else:
            print(f"❌ Error: {result.get('error')}")
            results.append({"message": message, "success": False})

    # Summary
    success_count = sum(1 for r in results if r["success"])
    correct_routing_count = sum(1 for r in results if r.get("correct_routing"))

    print(f"\n📊 Summary:")
    print(f"  • Successful: {success_count}/{len(test_cases)}")
    print(f"  • Correct Routing: {correct_routing_count}/{len(test_cases)}")

    return results


def test_tools_and_context():
    """Test Swarm with tools and context."""
    print("\n" + "="*80)
    print("TEST 3: Tools and Context Passing")
    print("="*80)

    system = ToolBasedSwarmSystem()

    test_cases = [
        {
            "message": "Can you look up my account information?",
            "context": {"user_id": "U001"},
            "expected_keywords": ["John Smith", "Premium"]
        },
        {
            "message": "What's the status of my order?",
            "context": {"order_id": "ORD001"},
            "expected_keywords": ["Shipped", "TRK123456"]
        },
        {
            "message": "I have a discount code SAVE20, can you apply it to $100?",
            "context": {},
            "expected_keywords": ["20", "80"]
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        message = test_case["message"]
        context = test_case["context"]

        print(f"\n--- Test {i}/{len(test_cases)} ---")
        print(f"📝 Message: {message}")
        print(f"📋 Context: {context}")

        # Run agent
        result = system.run(message, context)

        if result["success"]:
            response = result["response"]
            tool_calls = result["tool_calls"]

            print(f"🤖 Response: {response}")
            print(f"🔧 Tool Calls: {tool_calls}")

            # Check for expected keywords
            has_keywords = any(
                kw.lower() in response.lower()
                for kw in test_case["expected_keywords"]
            )
            print(f"Keywords Found: {'✅' if has_keywords else '❌'}")

            # Evaluate
            scores = system.evaluate(message, response)

            print(f"\n📊 Evaluation:")
            for metric, score in scores.items():
                print(f"  • {metric}: {score.label} ({score.score:.2f})")

            results.append({
                "message": message,
                "response": response,
                "has_keywords": has_keywords,
                "tool_calls": tool_calls,
                "scores": scores,
                "success": True
            })
        else:
            print(f"❌ Error: {result.get('error')}")
            results.append({"message": message, "success": False})

    return results


def test_quality_gates():
    """Test Swarm with quality gates."""
    print("\n" + "="*80)
    print("TEST 4: Quality Gates")
    print("="*80)

    system = SimpleSwarmSystem()

    # Quality thresholds
    QUALITY_THRESHOLDS = {
        "coherence": 0.7,
        "relevance": 0.7,
        "toxicity": 0.2
    }

    test_messages = [
        "What is blockchain technology?",
        "Explain neural networks",
        "What are the advantages of renewable energy?"
    ]

    print(f"\n🚦 Quality Thresholds:")
    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric == "toxicity":
            print(f"  • {metric}: <= {threshold}")
        else:
            print(f"  • {metric}: >= {threshold}")

    all_passed = True
    results = []

    for i, message in enumerate(test_messages, 1):
        print(f"\n[{i}/{len(test_messages)}] Message: {message[:50]}...")

        # Run agent
        result = system.run(message)

        if not result["success"]:
            print(f"❌ Agent failed")
            all_passed = False
            continue

        # Evaluate
        scores = system.evaluate(message, result["response"])

        # Check quality gates
        passed_gates = True
        for metric, threshold in QUALITY_THRESHOLDS.items():
            if metric not in scores:
                continue

            score_value = scores[metric].score

            if metric == "toxicity":
                passed = score_value <= threshold
                status = "✅" if passed else "❌"
                print(f"  {status} {metric}: {score_value:.2f} <= {threshold}")
            else:
                passed = score_value >= threshold
                status = "✅" if passed else "❌"
                print(f"  {status} {metric}: {score_value:.2f} >= {threshold}")

            if not passed:
                passed_gates = False
                all_passed = False

        results.append({
            "message": message,
            "passed": passed_gates,
            "scores": scores
        })

    # Summary
    passed_count = sum(1 for r in results if r["passed"])
    print(f"\n{'='*80}")
    print(f"🚦 Quality Gate Summary:")
    print(f"  • Passed: {passed_count}/{len(results)}")
    print(f"  • Failed: {len(results) - passed_count}/{len(results)}")

    if all_passed:
        print(f"\n✅ All quality gates PASSED!")
    else:
        print(f"\n⚠️  Some quality gates FAILED")

    return results


def test_end_to_end_workflow():
    """End-to-end workflow test."""
    print("\n" + "="*80)
    print("TEST 5: End-to-End Customer Service Workflow")
    print("="*80)

    # Use multi-agent system
    multi_system = MultiAgentSwarmSystem()

    # Use tool-based system
    tool_system = ToolBasedSwarmSystem()

    # Scenario: Customer inquiry through full workflow
    customer_journey = [
        {
            "system": "multi",
            "message": "I want to check my order status and see if I can get a discount on my next purchase",
            "description": "Initial inquiry (should route to appropriate agent)"
        },
        {
            "system": "tool",
            "message": "Check the status of order ORD002",
            "context": {"order_id": "ORD002"},
            "description": "Order status lookup"
        },
        {
            "system": "tool",
            "message": "Apply discount code VIP30 to a $200 purchase",
            "context": {},
            "description": "Discount calculation"
        }
    ]

    print("\n🎬 Customer Journey Simulation:")

    for i, step in enumerate(customer_journey, 1):
        print(f"\n{'='*60}")
        print(f"Step {i}: {step['description']}")
        print(f"{'='*60}")

        if step["system"] == "multi":
            result = multi_system.run(step["message"])
            if result["success"]:
                print(f"🤖 Response: {result['response'][:300]}...")
                print(f"🔀 Routing: {result.get('final_agent', 'Unknown')}")
        else:
            context = step.get("context", {})
            result = tool_system.run(step["message"], context)
            if result["success"]:
                print(f"🤖 Response: {result['response']}")
                print(f"🔧 Tools Used: {result.get('tool_calls', 0)} calls")

    print(f"\n{'='*80}")
    print("✅ End-to-end workflow completed!")


# ============================================================================
# STEP 5: Main Execution
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🚀 OpenAI Swarm (Agents SDK) Example with Custom Evals Testing")
    print("="*80)

    if not SWARM_AVAILABLE:
        print("\n❌ OpenAI Swarm not installed")
        print("Install with: pip install git+https://github.com/openai/swarm.git")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY environment variable not set")
        print("Set with: export OPENAI_API_KEY='your-key'")
        return

    try:
        # Test 1: Simple Swarm
        test_simple_swarm()

        # Test 2: Multi-agent routing
        test_multi_agent_routing()

        # Test 3: Tools and context
        test_tools_and_context()

        # Test 4: Quality gates
        test_quality_gates()

        # Test 5: End-to-end workflow
        test_end_to_end_workflow()

        print("\n" + "="*80)
        print("✅ All tests completed!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
