"""
Autogen Agent Example with Custom Evals Testing

This example demonstrates:
1. Creating Autogen conversational agents
2. Multi-agent collaboration and conversation
3. Code execution capabilities
4. Tool/function calling
5. Evaluating agent outputs with custom-evals

Autogen is Microsoft's framework for building multi-agent conversational systems.

Requirements:
- pyautogen (pip install pyautogen)
"""

import os
from typing import Dict, Any, List, Optional

try:
    import autogen
    from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
    from autogen.code_utils import extract_code
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    print("⚠️  pyautogen not installed. Install with: pip install pyautogen")

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
# STEP 1: Autogen Configuration
# ============================================================================

def get_autogen_config() -> Dict[str, Any]:
    """Get Autogen LLM configuration."""
    return {
        "config_list": [
            {
                "model": "gpt-4o-mini",
                "api_key": os.getenv("OPENAI_API_KEY"),
            }
        ],
        "temperature": 0,
        "timeout": 120,
    }


# ============================================================================
# STEP 2: Simple Two-Agent System
# ============================================================================

class AutogenTwoAgentSystem:
    """Simple two-agent system with Assistant and User Proxy."""

    def __init__(self):
        if not AUTOGEN_AVAILABLE:
            raise ImportError("pyautogen package required")

        llm_config = get_autogen_config()

        # Create assistant agent
        self.assistant = AssistantAgent(
            name="assistant",
            llm_config=llm_config,
            system_message="""You are a helpful AI assistant.
You help users with questions and tasks.
Be concise and accurate."""
        )

        # Create user proxy (executes code and represents user)
        self.user_proxy = UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",  # No human input needed for testing
            max_consecutive_auto_reply=3,
            code_execution_config={
                "work_dir": "autogen_workspace",
                "use_docker": False,  # Set to True for safer execution
            },
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, message: str) -> Dict[str, Any]:
        """Run conversation between user and assistant."""
        try:
            # Initiate chat
            self.user_proxy.initiate_chat(
                self.assistant,
                message=message,
            )

            # Get conversation history
            conversation = self.user_proxy.chat_messages[self.assistant]

            # Extract assistant's response (last message from assistant)
            response = ""
            for msg in reversed(conversation):
                if msg.get("role") == "assistant" and msg.get("content"):
                    response = msg["content"]
                    break

            return {
                "message": message,
                "response": response,
                "conversation": conversation,
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
# STEP 3: Multi-Agent Group Chat
# ============================================================================

class AutogenGroupChatSystem:
    """Multi-agent system using Autogen's GroupChat."""

    def __init__(self):
        if not AUTOGEN_AVAILABLE:
            raise ImportError("pyautogen package required")

        llm_config = get_autogen_config()

        # Create specialized agents
        self.researcher = AssistantAgent(
            name="researcher",
            llm_config=llm_config,
            system_message="""You are a Research Specialist.
Your role is to gather information and present facts.
Be thorough and cite sources when possible."""
        )

        self.analyst = AssistantAgent(
            name="analyst",
            llm_config=llm_config,
            system_message="""You are a Data Analyst.
Your role is to analyze information and draw insights.
Be analytical and data-driven."""
        )

        self.writer = AssistantAgent(
            name="writer",
            llm_config=llm_config,
            system_message="""You are a Technical Writer.
Your role is to create clear, concise content.
Be professional and well-structured."""
        )

        # Create user proxy to manage the group
        self.user_proxy = UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=2,
            code_execution_config=False,
        )

        # Create group chat
        self.groupchat = GroupChat(
            agents=[self.user_proxy, self.researcher, self.analyst, self.writer],
            messages=[],
            max_round=10
        )

        # Create group chat manager
        self.manager = GroupChatManager(
            groupchat=self.groupchat,
            llm_config=llm_config
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, task: str) -> Dict[str, Any]:
        """Run group chat with task."""
        try:
            # Reset group chat messages
            self.groupchat.messages = []

            # Initiate chat
            self.user_proxy.initiate_chat(
                self.manager,
                message=task,
            )

            # Get all messages
            messages = self.groupchat.messages

            # Extract final response (last assistant message)
            final_response = ""
            for msg in reversed(messages):
                if msg.get("role") == "assistant" and msg.get("content"):
                    final_response = msg["content"]
                    break

            return {
                "task": task,
                "response": final_response,
                "messages": messages,
                "total_messages": len(messages),
                "success": True
            }

        except Exception as e:
            return {
                "task": task,
                "response": str(e),
                "success": False,
                "error": str(e)
            }

    def evaluate(self, task: str, response: str) -> Dict[str, Any]:
        """Evaluate group chat output."""
        eval_input = {
            "input": task,
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
# STEP 4: Function Calling Agent
# ============================================================================

class AutogenFunctionAgent:
    """Autogen agent with function calling capabilities."""

    def __init__(self):
        if not AUTOGEN_AVAILABLE:
            raise ImportError("pyautogen package required")

        llm_config = get_autogen_config()

        # Define functions
        def get_stock_price(symbol: str) -> str:
            """Get stock price for a symbol."""
            # Simulated stock prices
            prices = {
                "AAPL": "$185.50",
                "GOOGL": "$142.30",
                "MSFT": "$410.20",
                "TSLA": "$242.80"
            }
            return prices.get(symbol.upper(), f"Price not available for {symbol}")

        def calculate_portfolio_value(stocks: List[Dict[str, Any]]) -> str:
            """Calculate total portfolio value."""
            # Simulated calculation
            total = 0
            for stock in stocks:
                symbol = stock.get("symbol", "").upper()
                shares = stock.get("shares", 0)

                prices = {"AAPL": 185.50, "GOOGL": 142.30, "MSFT": 410.20, "TSLA": 242.80}
                price = prices.get(symbol, 0)
                total += price * shares

            return f"Portfolio value: ${total:,.2f}"

        # Register functions
        self.get_stock_price = get_stock_price
        self.calculate_portfolio_value = calculate_portfolio_value

        # Create assistant with functions
        self.assistant = AssistantAgent(
            name="financial_assistant",
            llm_config=llm_config,
            system_message="""You are a financial assistant.
You help with stock prices and portfolio calculations.
Use the available functions to provide accurate information."""
        )

        # Register functions with assistant
        self.assistant.register_function(
            function_map={
                "get_stock_price": get_stock_price,
                "calculate_portfolio_value": calculate_portfolio_value,
            }
        )

        # Create user proxy
        self.user_proxy = UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
            code_execution_config=False,
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm)
        }

    def run(self, query: str) -> Dict[str, Any]:
        """Run agent with function calling."""
        try:
            # Initiate chat
            self.user_proxy.initiate_chat(
                self.assistant,
                message=query,
            )

            # Get conversation
            conversation = self.user_proxy.chat_messages[self.assistant]

            # Extract response
            response = ""
            for msg in reversed(conversation):
                if msg.get("role") == "assistant" and msg.get("content"):
                    response = msg["content"]
                    break

            return {
                "query": query,
                "response": response,
                "conversation": conversation,
                "success": True
            }

        except Exception as e:
            return {
                "query": query,
                "response": str(e),
                "success": False,
                "error": str(e)
            }

    def evaluate(self, query: str, response: str, expected: str = None) -> Dict[str, Any]:
        """Evaluate function agent response."""
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
# STEP 5: Testing Functions
# ============================================================================

def test_two_agent_system():
    """Test simple two-agent system."""
    print("\n" + "="*80)
    print("TEST 1: Two-Agent System - Assistant & User Proxy")
    print("="*80)

    system = AutogenTwoAgentSystem()

    test_messages = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms",
        "List three benefits of exercise"
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


def test_group_chat():
    """Test multi-agent group chat."""
    print("\n" + "="*80)
    print("TEST 2: Multi-Agent Group Chat")
    print("="*80)

    system = AutogenGroupChatSystem()

    test_tasks = [
        "Research and write about artificial intelligence trends in 2024",
        "Analyze the benefits of cloud computing and summarize findings"
    ]

    results = []

    for i, task in enumerate(test_tasks, 1):
        print(f"\n--- Test {i}/{len(test_tasks)} ---")
        print(f"📝 Task: {task}")

        # Run group chat
        result = system.run(task)

        if result["success"]:
            response = result["response"]
            print(f"🤖 Final Response: {response[:300]}...")
            print(f"💬 Total Messages: {result['total_messages']}")

            # Evaluate
            scores = system.evaluate(task, response)

            print(f"\n📊 Evaluation:")
            for metric, score in scores.items():
                print(f"  • {metric}: {score.label} ({score.score:.2f})")

            results.append({
                "task": task,
                "response": response,
                "scores": scores,
                "success": True
            })
        else:
            print(f"❌ Error: {result.get('error')}")
            results.append({"task": task, "success": False})

    return results


def test_function_calling():
    """Test agent with function calling."""
    print("\n" + "="*80)
    print("TEST 3: Function Calling Agent")
    print("="*80)

    agent = AutogenFunctionAgent()

    test_queries = [
        {
            "query": "What is the current price of AAPL stock?",
            "expected_keywords": ["185", "AAPL"]
        },
        {
            "query": "Calculate the value of a portfolio with 10 shares of MSFT and 5 shares of GOOGL",
            "expected_keywords": ["portfolio", "value"]
        }
    ]

    results = []

    for i, test_case in enumerate(test_queries, 1):
        query = test_case["query"]
        print(f"\n--- Test {i}/{len(test_queries)} ---")
        print(f"📝 Query: {query}")

        # Run agent
        result = agent.run(query)

        if result["success"]:
            response = result["response"]
            print(f"🤖 Response: {response}")

            # Check for expected keywords
            has_keywords = any(
                kw.lower() in response.lower()
                for kw in test_case["expected_keywords"]
            )
            print(f"Keywords found: {'✅' if has_keywords else '❌'}")

            # Evaluate
            scores = agent.evaluate(query, response)

            print(f"\n📊 Evaluation:")
            for metric, score in scores.items():
                print(f"  • {metric}: {score.label} ({score.score:.2f})")

            results.append({
                "query": query,
                "response": response,
                "has_keywords": has_keywords,
                "scores": scores,
                "success": True
            })
        else:
            print(f"❌ Error: {result.get('error')}")
            results.append({"query": query, "success": False})

    return results


def test_quality_gates():
    """Test with quality gates."""
    print("\n" + "="*80)
    print("TEST 4: Quality Gates")
    print("="*80)

    system = AutogenTwoAgentSystem()

    # Quality thresholds
    QUALITY_THRESHOLDS = {
        "coherence": 0.7,
        "relevance": 0.7,
        "toxicity": 0.2
    }

    test_messages = [
        "What are the main components of a computer?",
        "Explain the water cycle",
        "What is machine learning?"
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


# ============================================================================
# STEP 6: Main Execution
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🚀 Autogen Agent Example with Custom Evals Testing")
    print("="*80)

    if not AUTOGEN_AVAILABLE:
        print("\n❌ pyautogen package not installed")
        print("Install with: pip install pyautogen")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY environment variable not set")
        print("Set with: export OPENAI_API_KEY='your-key'")
        return

    try:
        # Test 1: Two-agent system
        test_two_agent_system()

        # Test 2: Group chat
        test_group_chat()

        # Test 3: Function calling
        test_function_calling()

        # Test 4: Quality gates
        test_quality_gates()

        print("\n" + "="*80)
        print("✅ All tests completed!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
