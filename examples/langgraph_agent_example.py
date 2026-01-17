"""
LangGraph Agent Example with Custom Evals Testing

This example demonstrates:
1. Creating a LangGraph agent with tools
2. Running the agent on queries
3. Evaluating agent outputs with custom-evals
4. Testing agent quality with multiple metrics
"""

import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool

# Custom Evals imports
from custom.evals import (
    HallucinationEvaluator,
    CoherenceEvaluator,
    RelevanceEvaluator,
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
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # Simulated weather data
    weather_data = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Cloudy, 65°F",
        "London": "Rainy, 58°F",
        "Tokyo": "Clear, 68°F"
    }
    return weather_data.get(city, f"Weather data not available for {city}")


@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    # Simulated Wikipedia search
    wiki_data = {
        "Python": "Python is a high-level programming language known for its simplicity and readability.",
        "Machine Learning": "Machine Learning is a subset of AI that enables systems to learn from data.",
        "LangGraph": "LangGraph is a framework for building stateful, multi-actor applications with LLMs."
    }
    for key, value in wiki_data.items():
        if key.lower() in query.lower():
            return value
    return f"No Wikipedia information found for: {query}"


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"


# ============================================================================
# STEP 2: Define Agent State
# ============================================================================

class AgentState(TypedDict):
    """State of the agent."""
    messages: list
    next_action: str


# ============================================================================
# STEP 3: Create LangGraph Agent
# ============================================================================

class LangGraphAgent:
    """LangGraph agent with tools and evaluation."""

    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Define tools
        self.tools = [get_weather, search_wikipedia, calculate]

        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # Create the graph
        self.graph = self._create_graph()

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow."""
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", ToolNode(self.tools))

        # Set entry point
        workflow.set_entry_point("agent")

        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )

        # Add edge from tools back to agent
        workflow.add_edge("tools", "agent")

        return workflow.compile()

    def _call_model(self, state: AgentState) -> dict:
        """Call the LLM with tools."""
        messages = state["messages"]
        response = self.llm_with_tools.invoke(messages)
        return {"messages": messages + [response]}

    def _should_continue(self, state: AgentState) -> str:
        """Decide whether to continue or end."""
        last_message = state["messages"][-1]

        # If there are tool calls, continue
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"
        return "end"

    def run(self, query: str) -> dict:
        """Run the agent on a query."""
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "next_action": ""
        }

        # Run the graph
        result = self.graph.invoke(initial_state)

        # Extract final response
        final_message = result["messages"][-1]
        response = final_message.content if hasattr(final_message, "content") else str(final_message)

        return {
            "query": query,
            "response": response,
            "messages": result["messages"]
        }

    def evaluate(self, query: str, response: str) -> dict:
        """Evaluate agent response with multiple metrics."""
        eval_input = {
            "input": query,
            "output": response
        }

        scores = {}
        for name, evaluator in self.evaluators.items():
            score = evaluator.evaluate(eval_input)
            scores[name] = score

        return scores


# ============================================================================
# STEP 4: Testing Functions
# ============================================================================

def test_single_query():
    """Test agent on a single query."""
    print("\n" + "="*80)
    print("TEST 1: Single Query - Weather Information")
    print("="*80)

    agent = LangGraphAgent()

    # Test query
    query = "What's the weather like in San Francisco?"
    print(f"\n📝 Query: {query}")

    # Run agent
    result = agent.run(query)
    response = result["response"]
    print(f"\n🤖 Agent Response: {response}")

    # Evaluate response
    print("\n📊 Evaluation Scores:")
    scores = agent.evaluate(query, response)

    for metric, score in scores.items():
        print(f"  • {metric.capitalize()}: {score.label} ({score.score:.2f})")
        if score.explanation:
            print(f"    Explanation: {score.explanation}")

    return scores


def test_multiple_queries():
    """Test agent on multiple queries."""
    print("\n" + "="*80)
    print("TEST 2: Multiple Queries - Comprehensive Testing")
    print("="*80)

    agent = LangGraphAgent()

    test_cases = [
        {
            "query": "Search Wikipedia for information about Python programming",
            "expected_keywords": ["programming", "language"]
        },
        {
            "query": "Calculate 15 * 24 + 100",
            "expected_keywords": ["460"]
        },
        {
            "query": "What's the weather in Tokyo?",
            "expected_keywords": ["Tokyo", "weather"]
        },
        {
            "query": "Tell me about Machine Learning",
            "expected_keywords": ["machine learning", "AI", "data"]
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
        print(f"🤖 Response: {response[:200]}...")

        # Evaluate
        scores = agent.evaluate(query, response)

        # Check for expected keywords
        has_keywords = any(
            keyword.lower() in response.lower()
            for keyword in test_case["expected_keywords"]
        )

        test_result = {
            "query": query,
            "response": response,
            "scores": scores,
            "has_keywords": has_keywords
        }
        results.append(test_result)

        # Print summary
        print(f"  • Coherence: {scores['coherence'].label}")
        print(f"  • Relevance: {scores['relevance'].label}")
        print(f"  • Toxicity: {scores['toxicity'].label}")
        print(f"  • Keywords Found: {'✅' if has_keywords else '❌'}")

    # Overall summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    coherent_count = sum(1 for r in results if r['scores']['coherence'].label == 'coherent')
    relevant_count = sum(1 for r in results if r['scores']['relevance'].label == 'relevant')
    non_toxic_count = sum(1 for r in results if r['scores']['toxicity'].label == 'not_toxic')
    keywords_count = sum(1 for r in results if r['has_keywords'])

    print(f"  • Coherent Responses: {coherent_count}/{len(results)}")
    print(f"  • Relevant Responses: {relevant_count}/{len(results)}")
    print(f"  • Non-Toxic Responses: {non_toxic_count}/{len(results)}")
    print(f"  • Contains Expected Keywords: {keywords_count}/{len(results)}")

    pass_rate = (coherent_count + relevant_count + non_toxic_count) / (len(results) * 3)
    print(f"\n✅ Overall Pass Rate: {pass_rate:.1%}")

    return results


def test_with_context():
    """Test agent with context-aware evaluation."""
    print("\n" + "="*80)
    print("TEST 3: Context-Aware Evaluation")
    print("="*80)

    agent = LangGraphAgent()

    # Query with context
    query = "What's the weather in London and should I bring an umbrella?"
    print(f"\n📝 Query: {query}")

    # Run agent
    result = agent.run(query)
    response = result["response"]
    print(f"\n🤖 Agent Response: {response}")

    # Evaluate with context
    # Get the tool calls context
    context = "The agent has access to weather data showing London is rainy."

    eval_llm = LLM(provider="openai", model="gpt-4o-mini")
    hallucination_eval = HallucinationEvaluator(eval_llm)

    hall_score = hallucination_eval.evaluate({
        "input": query,
        "output": response,
        "context": context
    })

    print(f"\n📊 Hallucination Check:")
    print(f"  • Verdict: {hall_score.label}")
    print(f"  • Score: {hall_score.score:.2f}")
    print(f"  • Explanation: {hall_score.explanation}")

    return hall_score


def test_agent_quality_gates():
    """Test agent with quality gates."""
    print("\n" + "="*80)
    print("TEST 4: Quality Gates - Automated Quality Assurance")
    print("="*80)

    agent = LangGraphAgent()

    # Define quality thresholds
    QUALITY_THRESHOLDS = {
        "coherence": 0.7,      # Minimum 70% coherent
        "relevance": 0.7,      # Minimum 70% relevant
        "toxicity": 0.2,       # Maximum 20% toxic
    }

    query = "Explain what LangGraph is used for"
    print(f"\n📝 Query: {query}")

    # Run agent
    result = agent.run(query)
    response = result["response"]
    print(f"\n🤖 Agent Response: {response}")

    # Evaluate
    scores = agent.evaluate(query, response)

    # Check quality gates
    print("\n🚦 Quality Gate Checks:")
    passed_gates = True

    for metric, threshold in QUALITY_THRESHOLDS.items():
        score_value = scores[metric].score

        if metric == "toxicity":
            # Lower is better for toxicity
            passed = score_value <= threshold
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  • {metric.capitalize()}: {score_value:.2f} <= {threshold} {status}")
        else:
            # Higher is better for coherence and relevance
            passed = score_value >= threshold
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  • {metric.capitalize()}: {score_value:.2f} >= {threshold} {status}")

        if not passed:
            passed_gates = False

    if passed_gates:
        print("\n✅ All quality gates PASSED - Agent ready for production!")
    else:
        print("\n❌ Some quality gates FAILED - Agent needs improvement")

    return passed_gates


def test_batch_evaluation():
    """Test batch evaluation for regression testing."""
    print("\n" + "="*80)
    print("TEST 5: Batch Evaluation - Regression Testing")
    print("="*80)

    agent = LangGraphAgent()

    # Batch test cases
    test_queries = [
        "What's the weather in New York?",
        "Calculate 100 / 5 + 25",
        "Search for information about Python",
        "What's 2 + 2?",
        "Tell me the weather in San Francisco"
    ]

    print(f"\n📋 Running batch evaluation on {len(test_queries)} queries...\n")

    batch_results = []

    for i, query in enumerate(test_queries, 1):
        print(f"[{i}/{len(test_queries)}] Processing: {query[:50]}...")

        # Run agent
        result = agent.run(query)
        response = result["response"]

        # Evaluate
        scores = agent.evaluate(query, response)

        batch_results.append({
            "query": query,
            "response": response,
            "coherence_score": scores["coherence"].score,
            "relevance_score": scores["relevance"].score,
            "toxicity_score": scores["toxicity"].score
        })

    # Calculate statistics
    avg_coherence = sum(r["coherence_score"] for r in batch_results) / len(batch_results)
    avg_relevance = sum(r["relevance_score"] for r in batch_results) / len(batch_results)
    avg_toxicity = sum(r["toxicity_score"] for r in batch_results) / len(batch_results)

    print("\n📊 Batch Evaluation Results:")
    print(f"  • Average Coherence: {avg_coherence:.2f}")
    print(f"  • Average Relevance: {avg_relevance:.2f}")
    print(f"  • Average Toxicity: {avg_toxicity:.2f}")
    print(f"  • Total Queries Tested: {len(batch_results)}")

    return batch_results


# ============================================================================
# STEP 5: Main Execution
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🚀 LangGraph Agent Example with Custom Evals Testing")
    print("="*80)

    try:
        # Test 1: Single query
        test_single_query()

        # Test 2: Multiple queries
        test_multiple_queries()

        # Test 3: Context-aware evaluation
        test_with_context()

        # Test 4: Quality gates
        test_agent_quality_gates()

        # Test 5: Batch evaluation
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
