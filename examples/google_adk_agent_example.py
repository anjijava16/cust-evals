"""
Google ADK (Agent Development Kit) Example with Custom Evals Testing

This example demonstrates:
1. Building agents with Google ADK framework
2. Multi-agent collaboration with ADK
3. Tool integration and function calling
4. State management across agents
5. Evaluating agent outputs with custom-evals

Google ADK is Google's framework for building production-grade AI agents.

Requirements:
- google-adk (pip install google-adk)
- google-generativeai (pip install google-generativeai)
"""

import os
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

try:
    import google.generativeai as genai
    GOOGLE_ADK_AVAILABLE = True
except ImportError:
    GOOGLE_ADK_AVAILABLE = False
    print("⚠️  Google ADK not installed. Install with: pip install google-generativeai")

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
# STEP 1: Define Tools for Agents
# ============================================================================

def get_weather_info(location: str) -> str:
    """Get weather information for a location."""
    weather_database = {
        "San Francisco": {"temp": "72°F", "condition": "Sunny", "humidity": "65%"},
        "New York": {"temp": "65°F", "condition": "Cloudy", "humidity": "70%"},
        "London": {"temp": "55°F", "condition": "Rainy", "humidity": "85%"},
        "Tokyo": {"temp": "68°F", "condition": "Clear", "humidity": "60%"}
    }

    data = weather_database.get(location)
    if data:
        return f"Weather in {location}: {data['condition']}, {data['temp']}, Humidity: {data['humidity']}"
    return f"Weather data not available for {location}"


def search_knowledge_base(query: str) -> str:
    """Search knowledge base for information."""
    knowledge_base = {
        "machine learning": "Machine learning is a method of data analysis that automates analytical model building.",
        "neural networks": "Neural networks are computing systems inspired by biological neural networks.",
        "deep learning": "Deep learning is part of machine learning based on artificial neural networks.",
        "ai ethics": "AI ethics involves moral principles and techniques for developing ethical AI systems.",
        "nlp": "Natural Language Processing enables computers to understand and generate human language."
    }

    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value

    return f"No information found in knowledge base for: {query}"


def calculate_metrics(data: str) -> str:
    """Calculate basic metrics from data."""
    try:
        # Parse simple calculations
        if "average" in data.lower():
            numbers = [int(s) for s in data.split() if s.isdigit()]
            if numbers:
                avg = sum(numbers) / len(numbers)
                return f"Average of {numbers}: {avg}"

        if "sum" in data.lower():
            numbers = [int(s) for s in data.split() if s.isdigit()]
            if numbers:
                total = sum(numbers)
                return f"Sum of {numbers}: {total}"

        return "Calculation completed"
    except Exception as e:
        return f"Error calculating: {str(e)}"


def get_user_preferences(user_id: str) -> str:
    """Get user preferences and settings."""
    users = {
        "user001": {"name": "Alice", "interests": ["AI", "ML"], "role": "Data Scientist"},
        "user002": {"name": "Bob", "interests": ["Cloud", "DevOps"], "role": "Engineer"},
        "user003": {"name": "Carol", "interests": ["NLP", "Research"], "role": "Researcher"}
    }

    user = users.get(user_id)
    if user:
        return json.dumps(user)
    return f"User {user_id} not found"


# ============================================================================
# STEP 2: Google ADK Agent
# ============================================================================

class GoogleADKAgent:
    """Agent using Google ADK with Gemini models."""

    def __init__(self, name: str = "GoogleADKAgent", model: str = "gemini-1.5-flash"):
        if not GOOGLE_ADK_AVAILABLE:
            raise ImportError("Google Generative AI SDK required")

        # Configure API
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")

        genai.configure(api_key=api_key)

        self.name = name
        self.model_name = model
        self.model = genai.GenerativeModel(model)

        # Define available tools
        self.tools = {
            "get_weather_info": get_weather_info,
            "search_knowledge_base": search_knowledge_base,
            "calculate_metrics": calculate_metrics,
            "get_user_preferences": get_user_preferences
        }

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, prompt: str, system_instruction: str = None) -> Dict[str, Any]:
        """Run agent on a prompt."""
        try:
            # Configure with system instruction if provided
            if system_instruction:
                model = genai.GenerativeModel(
                    self.model_name,
                    system_instruction=system_instruction
                )
            else:
                model = self.model

            # Generate response
            response = model.generate_content(prompt)

            return {
                "success": True,
                "response": response.text,
                "agent": self.name
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def run_with_tools(self, prompt: str, tool_names: List[str] = None) -> Dict[str, Any]:
        """Run agent with tool integration (simulated)."""
        try:
            # Check if tools are needed based on prompt
            tool_calls = []
            enhanced_prompt = prompt

            # Simple tool routing based on keywords
            if "weather" in prompt.lower():
                for location in ["San Francisco", "New York", "London", "Tokyo"]:
                    if location.lower() in prompt.lower():
                        result = get_weather_info(location)
                        tool_calls.append({"tool": "get_weather_info", "args": {"location": location}, "result": result})
                        enhanced_prompt += f"\n\nWeather data: {result}"

            if "knowledge" in prompt.lower() or "tell me about" in prompt.lower():
                topics = ["machine learning", "neural networks", "deep learning", "nlp"]
                for topic in topics:
                    if topic in prompt.lower():
                        result = search_knowledge_base(topic)
                        tool_calls.append({"tool": "search_knowledge_base", "args": {"query": topic}, "result": result})
                        enhanced_prompt += f"\n\nKnowledge base info: {result}"

            # Generate response with tool context
            response = self.model.generate_content(enhanced_prompt)

            return {
                "success": True,
                "response": response.text,
                "tool_calls": tool_calls,
                "agent": self.name
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
# STEP 3: Multi-Agent ADK System
# ============================================================================

class MultiAgentADKSystem:
    """Multi-agent system using Google ADK."""

    def __init__(self):
        if not GOOGLE_ADK_AVAILABLE:
            raise ImportError("Google Generative AI SDK required")

        # Create specialized agents
        self.research_agent = GoogleADKAgent("ResearchAgent", "gemini-1.5-flash")
        self.analysis_agent = GoogleADKAgent("AnalysisAgent", "gemini-1.5-flash")
        self.writer_agent = GoogleADKAgent("WriterAgent", "gemini-1.5-flash")

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm)
        }

    def run_workflow(self, topic: str) -> Dict[str, Any]:
        """Run multi-agent workflow."""
        try:
            # Step 1: Research
            research_prompt = f"Research and gather key information about: {topic}"
            research_system = "You are a research specialist. Provide comprehensive, factual information."
            research_result = self.research_agent.run(research_prompt, research_system)

            if not research_result["success"]:
                return research_result

            # Step 2: Analysis
            analysis_prompt = f"Analyze this research about {topic}:\n\n{research_result['response']}\n\nProvide key insights."
            analysis_system = "You are an analysis expert. Extract key insights and patterns."
            analysis_result = self.analysis_agent.run(analysis_prompt, analysis_system)

            if not analysis_result["success"]:
                return analysis_result

            # Step 3: Writing
            writing_prompt = f"Create a clear summary about {topic} based on:\n\nResearch: {research_result['response']}\n\nAnalysis: {analysis_result['response']}"
            writing_system = "You are a technical writer. Create clear, concise summaries."
            writing_result = self.writer_agent.run(writing_prompt, writing_system)

            if not writing_result["success"]:
                return writing_result

            return {
                "success": True,
                "research": research_result["response"],
                "analysis": analysis_result["response"],
                "final_output": writing_result["response"],
                "agents_used": ["ResearchAgent", "AnalysisAgent", "WriterAgent"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def evaluate(self, query: str, response: str) -> Dict[str, Any]:
        """Evaluate multi-agent output."""
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
    print("TEST 1: Simple Google ADK Agent")
    print("="*80)

    agent = GoogleADKAgent("SimpleAgent")

    query = "What is artificial intelligence?"
    print(f"\n📝 Query: {query}")

    result = agent.run(query, "You are a helpful AI assistant.")

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
    """Test 2: Agent with tool integration."""
    print("\n" + "="*80)
    print("TEST 2: Google ADK Agent with Tools")
    print("="*80)

    agent = GoogleADKAgent("ToolAgent")

    query = "What's the weather like in Tokyo?"
    print(f"\n📝 Query: {query}")

    result = agent.run_with_tools(query)

    if result["success"]:
        print(f"\n✅ Response: {result['response'][:200]}...")
        print(f"\n🔧 Tool Calls: {len(result['tool_calls'])}")
        for tc in result["tool_calls"]:
            print(f"  - {tc['tool']}: {tc['result'][:100]}...")

        scores = agent.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")

    return result


def test_multi_agent_workflow():
    """Test 3: Multi-agent collaboration."""
    print("\n" + "="*80)
    print("TEST 3: Multi-Agent ADK Workflow")
    print("="*80)

    system = MultiAgentADKSystem()

    topic = "Machine Learning in Healthcare"
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

    agent = GoogleADKAgent("QualityAgent")

    test_queries = [
        "Explain neural networks",
        "What is deep learning?",
        "Tell me about natural language processing"
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

    agent = GoogleADKAgent("BatchAgent")

    test_cases = [
        {"query": "What is machine learning?", "category": "ML"},
        {"query": "Explain neural networks", "category": "DL"},
        {"query": "What is NLP?", "category": "NLP"}
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
    print("Google ADK with Custom Evals - Complete Test Suite")
    print("="*80)

    if not GOOGLE_ADK_AVAILABLE:
        print("\n❌ Google Generative AI SDK not available.")
        print("Install with: pip install google-generativeai")
        exit(1)

    if not os.getenv("GOOGLE_API_KEY"):
        print("\n❌ GOOGLE_API_KEY not set. Please set your API key.")
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
