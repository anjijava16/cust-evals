"""
LlamaIndex Workflows Agent Example with Custom Evals Testing

This example demonstrates:
1. Building agentic workflows with LlamaIndex Workflows
2. Event-driven agent orchestration
3. Multi-step workflows with state management
4. Tool integration and function calling
5. Evaluating workflow outputs with custom-evals

LlamaIndex Workflows provides event-driven agent orchestration.

Requirements:
- llama-index (pip install llama-index)
- llama-index-llms-openai (pip install llama-index-llms-openai)
"""

import os
import asyncio
from typing import Dict, Any, List, Optional

try:
    from llama_index.core.workflow import (
        Workflow,
        StartEvent,
        StopEvent,
        step,
        Event,
        Context
    )
    from llama_index.core.llms import ChatMessage
    from llama_index.llms.openai import OpenAI
    from llama_index.core.tools import FunctionTool
    LLAMAINDEX_AVAILABLE = True
except ImportError:
    LLAMAINDEX_AVAILABLE = False
    print("⚠️  LlamaIndex not installed. Install with: pip install llama-index llama-index-llms-openai")

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
# STEP 1: Define Tools for Workflows
# ============================================================================

def get_weather(location: str) -> str:
    """Get current weather for a location."""
    weather_data = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Cloudy, 65°F",
        "London": "Foggy, 55°F",
        "Tokyo": "Clear, 68°F"
    }
    return weather_data.get(location, f"Weather data not available for {location}")


def search_knowledge_base(query: str) -> str:
    """Search knowledge base for information."""
    knowledge = {
        "python": "Python is a high-level programming language.",
        "machine learning": "Machine learning is a method of data analysis.",
        "neural networks": "Neural networks are computing systems inspired by biological neural networks.",
        "ai": "Artificial intelligence is the simulation of human intelligence."
    }

    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return value

    return f"No information found for: {query}"


def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# STEP 2: Define Custom Events
# ============================================================================

class ResearchEvent(Event):
    """Event for research phase."""
    query: str


class AnalysisEvent(Event):
    """Event for analysis phase."""
    research_result: str


class SummaryEvent(Event):
    """Event for summary phase."""
    analysis_result: str


# ============================================================================
# STEP 3: Simple LlamaIndex Workflow Agent
# ============================================================================

class SimpleWorkflowAgent(Workflow):
    """Simple workflow agent using LlamaIndex Workflows."""

    def __init__(self):
        if not LLAMAINDEX_AVAILABLE:
            raise ImportError("LlamaIndex required")

        super().__init__()

        self.llm = OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

        # Create tools
        self.weather_tool = FunctionTool.from_defaults(fn=get_weather)
        self.search_tool = FunctionTool.from_defaults(fn=search_knowledge_base)
        self.calc_tool = FunctionTool.from_defaults(fn=calculate)

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    @step
    async def process_query(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Process user query."""
        query = ev.get("query")

        # Generate response
        messages = [
            ChatMessage(role="system", content="You are a helpful assistant."),
            ChatMessage(role="user", content=query)
        ]

        response = await self.llm.achat(messages)

        return StopEvent(result={"response": response.message.content, "query": query})

    def evaluate(self, query: str, response: str, expected: str = None) -> Dict[str, Any]:
        """Evaluate workflow response."""
        scores = {}

        for name, evaluator in self.evaluators.items():
            eval_input = {"input": query, "output": response}

            if name == "correctness" and expected:
                eval_input["expected"] = expected

            score = evaluator.evaluate(eval_input)
            scores[name] = score

        return scores


# ============================================================================
# STEP 4: Multi-Step Research Workflow
# ============================================================================

class ResearchWorkflow(Workflow):
    """Multi-step research workflow with event-driven orchestration."""

    def __init__(self):
        if not LLAMAINDEX_AVAILABLE:
            raise ImportError("LlamaIndex required")

        super().__init__()

        self.llm = OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm)
        }

    @step
    async def research_step(self, ctx: Context, ev: StartEvent) -> ResearchEvent:
        """Step 1: Research the topic."""
        query = ev.get("query")

        # Research using search tool
        search_result = search_knowledge_base(query)

        # Generate research summary
        prompt = f"Research the following topic: {query}\n\nKnowledge base info: {search_result}"
        messages = [
            ChatMessage(role="system", content="You are a research specialist."),
            ChatMessage(role="user", content=prompt)
        ]

        response = await self.llm.achat(messages)

        # Store in context
        await ctx.set("research", response.message.content)

        return ResearchEvent(query=query)

    @step
    async def analysis_step(self, ctx: Context, ev: ResearchEvent) -> AnalysisEvent:
        """Step 2: Analyze the research."""
        research = await ctx.get("research")

        # Analyze the research
        prompt = f"Analyze this research and extract key insights:\n\n{research}"
        messages = [
            ChatMessage(role="system", content="You are an analysis expert."),
            ChatMessage(role="user", content=prompt)
        ]

        response = await self.llm.achat(messages)

        # Store in context
        await ctx.set("analysis", response.message.content)

        return AnalysisEvent(research_result=research)

    @step
    async def summary_step(self, ctx: Context, ev: AnalysisEvent) -> StopEvent:
        """Step 3: Create final summary."""
        research = await ctx.get("research")
        analysis = await ctx.get("analysis")

        # Create summary
        prompt = f"Create a concise summary based on:\n\nResearch: {research}\n\nAnalysis: {analysis}"
        messages = [
            ChatMessage(role="system", content="You are a technical writer."),
            ChatMessage(role="user", content=prompt)
        ]

        response = await self.llm.achat(messages)

        return StopEvent(result={
            "research": research,
            "analysis": analysis,
            "summary": response.message.content
        })

    def evaluate(self, query: str, response: str) -> Dict[str, Any]:
        """Evaluate workflow output."""
        scores = {}

        for name, evaluator in self.evaluators.items():
            score = evaluator.evaluate({"input": query, "output": response})
            scores[name] = score

        return scores


# ============================================================================
# STEP 5: Tool-Based Workflow Agent
# ============================================================================

class ToolWorkflowAgent(Workflow):
    """Workflow agent with tool integration."""

    def __init__(self):
        if not LLAMAINDEX_AVAILABLE:
            raise ImportError("LlamaIndex required")

        super().__init__()

        self.llm = OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm)
        }

    @step
    async def process_with_tools(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Process query with tools."""
        query = ev.get("query")

        # Determine which tools to use
        tool_results = []

        if "weather" in query.lower():
            for location in ["San Francisco", "New York", "London", "Tokyo"]:
                if location.lower() in query.lower():
                    result = get_weather(location)
                    tool_results.append(f"Weather: {result}")

        if "calculate" in query.lower() or any(op in query for op in ['+', '-', '*', '/']):
            # Extract expression
            import re
            match = re.search(r'(\d+\s*[+\-*/]\s*\d+)', query)
            if match:
                expr = match.group(1)
                result = calculate(expr)
                tool_results.append(f"Calculation: {result}")

        if "search" in query.lower() or "information" in query.lower():
            result = search_knowledge_base(query)
            tool_results.append(f"Search: {result}")

        # Generate response with tool context
        context = "\n".join(tool_results) if tool_results else "No tools used"
        prompt = f"User query: {query}\n\nTool results:\n{context}\n\nProvide a helpful response."

        messages = [
            ChatMessage(role="system", content="You are a helpful assistant."),
            ChatMessage(role="user", content=prompt)
        ]

        response = await self.llm.achat(messages)

        return StopEvent(result={
            "response": response.message.content,
            "tools_used": tool_results
        })

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

def test_simple_workflow():
    """Test 1: Simple workflow agent."""
    print("\n" + "="*80)
    print("TEST 1: Simple LlamaIndex Workflow Agent")
    print("="*80)

    workflow = SimpleWorkflowAgent()

    query = "What is artificial intelligence?"
    print(f"\n📝 Query: {query}")

    # Run workflow
    result = asyncio.run(workflow.run(query=query))

    if result and "response" in result:
        print(f"\n✅ Response: {result['response'][:200]}...")

        # Evaluate
        scores = workflow.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")
            print(f"    Explanation: {score.explanation[:100]}...")
    else:
        print(f"\n❌ No result")

    return result


def test_research_workflow():
    """Test 2: Multi-step research workflow."""
    print("\n" + "="*80)
    print("TEST 2: Multi-Step Research Workflow")
    print("="*80)

    workflow = ResearchWorkflow()

    query = "machine learning"
    print(f"\n📝 Query: {query}")

    # Run workflow
    result = asyncio.run(workflow.run(query=query))

    if result:
        print(f"\n✅ Summary: {result['summary'][:200]}...")
        print(f"\n📊 Workflow Steps:")
        print(f"  1. Research: {len(result['research'])} chars")
        print(f"  2. Analysis: {len(result['analysis'])} chars")
        print(f"  3. Summary: {len(result['summary'])} chars")

        # Evaluate
        scores = workflow.evaluate(query, result["summary"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")
    else:
        print(f"\n❌ No result")

    return result


def test_tool_workflow():
    """Test 3: Tool-based workflow."""
    print("\n" + "="*80)
    print("TEST 3: Tool-Based Workflow")
    print("="*80)

    workflow = ToolWorkflowAgent()

    query = "What's the weather in Tokyo?"
    print(f"\n📝 Query: {query}")

    # Run workflow
    result = asyncio.run(workflow.run(query=query))

    if result and "response" in result:
        print(f"\n✅ Response: {result['response']}")
        print(f"\n🔧 Tools Used: {len(result['tools_used'])}")
        for tool_result in result['tools_used']:
            print(f"  - {tool_result}")

        # Evaluate
        scores = workflow.evaluate(query, result["response"])

        print("\n📈 Evaluation Scores:")
        for name, score in scores.items():
            print(f"  - {name.capitalize()}: {score.label} ({score.score:.2f})")
    else:
        print(f"\n❌ No result")

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

    workflow = SimpleWorkflowAgent()

    test_queries = [
        "Explain neural networks",
        "What is deep learning?",
        "Tell me about Python programming"
    ]

    results = []

    for query in test_queries:
        print(f"\n📝 Query: {query}")
        result = asyncio.run(workflow.run(query=query))

        if result and "response" in result:
            scores = workflow.evaluate(query, result["response"])

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

    workflow = SimpleWorkflowAgent()

    test_cases = [
        {"query": "What is AI?", "category": "AI"},
        {"query": "Explain machine learning", "category": "ML"},
        {"query": "What are neural networks?", "category": "NN"}
    ]

    results = []

    for test_case in test_cases:
        query = test_case["query"]
        print(f"\n📝 Query: {query}")

        result = asyncio.run(workflow.run(query=query))

        if result and "response" in result:
            scores = workflow.evaluate(query, result["response"])
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
    print("LlamaIndex Workflows with Custom Evals - Complete Test Suite")
    print("="*80)

    if not LLAMAINDEX_AVAILABLE:
        print("\n❌ LlamaIndex not available.")
        print("Install with: pip install llama-index llama-index-llms-openai")
        exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY not set. Please set your API key.")
        exit(1)

    # Run all tests
    try:
        test_simple_workflow()
        test_research_workflow()
        test_tool_workflow()
        test_quality_gates()
        test_batch_evaluation()

        print("\n" + "="*80)
        print("✅ All tests completed successfully!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
