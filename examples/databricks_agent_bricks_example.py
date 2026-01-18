"""
Databricks Agent Bricks SDK Example with Custom Evals Testing

This example demonstrates:
1. Building agents with Databricks Agent Bricks SDK
2. MLflow integration for agent tracking
3. Tool integration and function calling
4. Multi-agent workflows with Databricks
5. Evaluating agent outputs with custom-evals

Databricks Agent Bricks provides MLflow-integrated agent capabilities.

Requirements:
- databricks-agents (pip install databricks-agents)
- mlflow (pip install mlflow)
"""

import os
import json
from typing import Dict, Any, List, Optional

try:
    from databricks.agents import Agent, Tool
    from databricks.agents.runtime import AgentRuntime
    import mlflow
    DATABRICKS_AGENTS_AVAILABLE = True
except ImportError:
    DATABRICKS_AGENTS_AVAILABLE = False
    print("⚠️  Databricks Agent Bricks SDK not installed. Install with: pip install databricks-agents mlflow")

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
# STEP 1: Define Tools for Databricks Agents
# ============================================================================

def get_weather(location: str) -> str:
    """Get current weather for a location.

    Args:
        location: City name

    Returns:
        Weather information
    """
    weather_data = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Cloudy, 65°F",
        "London": "Rainy, 55°F",
        "Tokyo": "Clear, 68°F"
    }
    return weather_data.get(location, f"Weather data not available for {location}")


def search_data(query: str) -> str:
    """Search data catalog for information.

    Args:
        query: Search query

    Returns:
        Search results
    """
    data_catalog = {
        "databricks": "Databricks is a unified analytics platform for big data and AI.",
        "mlflow": "MLflow is an open-source platform for the machine learning lifecycle.",
        "spark": "Apache Spark is a unified analytics engine for big data processing.",
        "delta lake": "Delta Lake is an open-source storage layer for data lakes."
    }

    query_lower = query.lower()
    for key, value in data_catalog.items():
        if key in query_lower:
            return value

    return f"No data found for: {query}"


def calculate_metric(expression: str) -> str:
    """Calculate a metric or mathematical expression.

    Args:
        expression: Math expression

    Returns:
        Calculation result
    """
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"


def get_dataset_info(dataset_name: str) -> str:
    """Get information about a dataset.

    Args:
        dataset_name: Name of the dataset

    Returns:
        Dataset information
    """
    datasets = {
        "sales": {"rows": 10000, "columns": 15, "size": "2.5GB"},
        "customers": {"rows": 5000, "columns": 10, "size": "1.2GB"},
        "products": {"rows": 2000, "columns": 8, "size": "500MB"}
    }

    info = datasets.get(dataset_name.lower())
    if info:
        return json.dumps(info)
    return f"Dataset {dataset_name} not found"


# ============================================================================
# STEP 2: Databricks Agent System
# ============================================================================

class DatabricksAgentSystem:
    """Agent system using Databricks Agent Bricks SDK."""

    def __init__(self, model: str = "gpt-4o-mini"):
        if not DATABRICKS_AGENTS_AVAILABLE:
            raise ImportError("Databricks Agent Bricks SDK required")

        # Create tools
        self.tools = [
            Tool.from_function(get_weather),
            Tool.from_function(search_data),
            Tool.from_function(calculate_metric),
            Tool.from_function(get_dataset_info)
        ]

        # Create agent
        self.agent = Agent(
            name="databricks_assistant",
            instructions="You are a helpful assistant with access to data tools. Use them to provide accurate information.",
            tools=self.tools,
            model=model
        )

        # Create runtime
        self.runtime = AgentRuntime()

        # Initialize MLflow
        mlflow.set_experiment("agent_evaluation")

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, message: str) -> Dict[str, Any]:
        """Run agent on a message with MLflow tracking."""
        try:
            with mlflow.start_run():
                # Log input
                mlflow.log_param("input", message)

                # Run agent
                result = self.runtime.run(agent=self.agent, input=message)

                # Log output
                mlflow.log_param("output", result.output)
                mlflow.log_metric("tool_calls", len(result.tool_calls) if hasattr(result, 'tool_calls') else 0)

                return {
                    "success": True,
                    "response": result.output,
                    "tool_calls": result.tool_calls if hasattr(result, 'tool_calls') else [],
                    "agent": "databricks_assistant"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def evaluate(self, query: str, response: str, expected: str = None) -> Dict[str, Any]:
        """Evaluate agent response using custom-evals and log to MLflow."""
        scores = {}

        with mlflow.start_run(nested=True):
            for name, evaluator in self.evaluators.items():
                eval_input = {"input": query, "output": response}

                if name == "correctness" and expected:
                    eval_input["expected"] = expected

                score = evaluator.evaluate(eval_input)
                scores[name] = score

                # Log to MLflow
                mlflow.log_metric(f"{name}_score", score.score)
                mlflow.log_param(f"{name}_label", score.label)

        return scores


# ============================================================================
# STEP 3: Multi-Agent Databricks System
# ============================================================================

class MultiAgentDatabricksSystem:
    """Multi-agent system using Databricks Agent Bricks."""

    def __init__(self):
        if not DATABRICKS_AGENTS_AVAILABLE:
            raise ImportError("Databricks Agent Bricks SDK required")

        # Create specialized agents
        self.data_agent = Agent(
            name="data_analyst",
            instructions="You are a data analyst. Analyze data and provide insights.",
            tools=[Tool.from_function(search_data), Tool.from_function(get_dataset_info)],
            model="gpt-4o-mini"
        )

        self.ml_agent = Agent(
            name="ml_engineer",
            instructions="You are an ML engineer. Explain ML concepts and best practices.",
            model="gpt-4o-mini"
        )

        self.report_agent = Agent(
            name="report_writer",
            instructions="You are a report writer. Create clear, professional reports.",
            model="gpt-4o-mini"
        )

        # Create runtime
        self.runtime = AgentRuntime()

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm)
        }

    def run_workflow(self, topic: str) -> Dict[str, Any]:
        """Run multi-agent workflow."""
        try:
            with mlflow.start_run():
                # Step 1: Data Analysis
                data_result = self.runtime.run(
                    agent=self.data_agent,
                    input=f"Analyze data related to: {topic}"
                )

                # Step 2: ML Engineering
                ml_result = self.runtime.run(
                    agent=self.ml_agent,
                    input=f"Provide ML insights for: {data_result.output}"
                )

                # Step 3: Report Writing
                report_result = self.runtime.run(
                    agent=self.report_agent,
                    input=f"Create a report about {topic} based on: {ml_result.output}"
                )

                # Log workflow
                mlflow.log_param("topic", topic)
                mlflow.log_param("agents_used", "data_analyst,ml_engineer,report_writer")

                return {
                    "success": True,
                    "data_analysis": data_result.output,
                    "ml_insights": ml_result.output,
                    "final_output": report_result.output,
                    "agents_used": ["data_analyst", "ml_engineer", "report_writer"]
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
    print("TEST 1: Simple Databricks Agent")
    print("="*80)

    agent = DatabricksAgentSystem()

    query = "What is artificial intelligence?"
    print(f"\n📝 Query: {query}")

    result = agent.run(query)

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


def test_agent_with_tools():
    """Test 2: Agent with tool usage."""
    print("\n" + "="*80)
    print("TEST 2: Databricks Agent with Tools")
    print("="*80)

    agent = DatabricksAgentSystem()

    query = "Get information about the sales dataset and calculate 1000 * 0.15"
    print(f"\n📝 Query: {query}")

    result = agent.run(query)

    if result["success"]:
        print(f"\n✅ Response: {result['response']}")
        print(f"\n🔧 Tool Calls: {len(result['tool_calls'])}")

        scores = agent.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")
    else:
        print(f"\n❌ Error: {result.get('error')}")

    return result


def test_multi_agent_workflow():
    """Test 3: Multi-agent workflow."""
    print("\n" + "="*80)
    print("TEST 3: Multi-Agent Databricks Workflow")
    print("="*80)

    system = MultiAgentDatabricksSystem()

    topic = "Customer Segmentation Analysis"
    print(f"\n📝 Topic: {topic}")

    result = system.run_workflow(topic)

    if result["success"]:
        print(f"\n✅ Final Output: {result['final_output'][:200]}...")
        print(f"\n🤖 Agents Used: {', '.join(result['agents_used'])}")

        scores = system.evaluate(topic, result["final_output"])

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

    QUALITY_THRESHOLDS = {
        "coherence": 0.7,
        "relevance": 0.7,
        "correctness": 0.7,
        "toxicity": 0.2
    }

    agent = DatabricksAgentSystem()

    test_queries = [
        "Explain MLflow",
        "What is Delta Lake?",
        "Tell me about Apache Spark"
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

    agent = DatabricksAgentSystem()

    test_cases = [
        {"query": "What is Databricks?", "category": "Platform"},
        {"query": "Calculate 200 * 0.25", "category": "Math"},
        {"query": "Get info on customers dataset", "category": "Data"}
    ]

    results = []

    for test_case in test_cases:
        query = test_case["query"]
        print(f"\n📝 Query: {query}")

        result = agent.run(query)

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
    print("Databricks Agent Bricks SDK with Custom Evals - Complete Test Suite")
    print("="*80)

    if not DATABRICKS_AGENTS_AVAILABLE:
        print("\n❌ Databricks Agent Bricks SDK not available.")
        print("Install with: pip install databricks-agents mlflow")
        exit(1)

    # Run all tests
    try:
        test_simple_agent()
        test_agent_with_tools()
        test_multi_agent_workflow()
        test_quality_gates()
        test_batch_evaluation()

        print("\n" + "="*80)
        print("✅ All tests completed successfully!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
