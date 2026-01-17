"""
PydanticAI Agent Example with Custom Evals Testing

This example demonstrates:
1. Creating type-safe agents with PydanticAI
2. Using Pydantic models for structured outputs
3. Tool/function calling with type validation
4. Multi-agent workflows
5. Evaluating agent outputs with custom-evals

PydanticAI is Pydantic's framework for building production-grade AI agents.

Requirements:
- pydantic-ai (pip install pydantic-ai)
- pydantic (pip install pydantic>=2.0)
"""

import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

try:
    from pydantic import BaseModel, Field
    from pydantic_ai import Agent, RunContext
    from pydantic_ai.models.openai import OpenAIModel
    PYDANTIC_AI_AVAILABLE = True
except ImportError as e:
    PYDANTIC_AI_AVAILABLE = False
    print(f"⚠️  PydanticAI not installed: {e}")
    print("Install with: pip install pydantic-ai pydantic>=2.0")

# Custom Evals imports
from custom.evals import (
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
# STEP 1: Structured Output Models
# ============================================================================

class ProductInfo(BaseModel):
    """Product information model."""
    name: str = Field(description="Product name")
    price: float = Field(description="Product price")
    category: str = Field(description="Product category")
    in_stock: bool = Field(description="Whether product is in stock")


class WeatherInfo(BaseModel):
    """Weather information model."""
    city: str = Field(description="City name")
    temperature: str = Field(description="Temperature")
    condition: str = Field(description="Weather condition")
    humidity: Optional[int] = Field(None, description="Humidity percentage")


class AnalysisResult(BaseModel):
    """Analysis result model."""
    summary: str = Field(description="Summary of analysis")
    key_points: List[str] = Field(description="Key points identified")
    recommendations: List[str] = Field(description="Recommendations")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")


# ============================================================================
# STEP 2: Simple PydanticAI Agent
# ============================================================================

class SimplePydanticAgent:
    """Simple PydanticAI agent with structured outputs."""

    def __init__(self):
        if not PYDANTIC_AI_AVAILABLE:
            raise ImportError("PydanticAI required")

        # Create agent with structured output
        self.agent = Agent(
            'openai:gpt-4o-mini',
            system_prompt="""You are a helpful assistant that provides
            clear and accurate information."""
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    async def run_async(self, message: str) -> Dict[str, Any]:
        """Run agent asynchronously."""
        try:
            result = await self.agent.run(message)
            response = result.data

            return {
                "message": message,
                "response": response,
                "success": True
            }

        except Exception as e:
            return {
                "message": message,
                "response": str(e),
                "success": False,
                "error": str(e)
            }

    def run(self, message: str) -> Dict[str, Any]:
        """Run agent synchronously."""
        import asyncio
        return asyncio.run(self.run_async(message))

    def evaluate(self, message: str, response: str) -> Dict[str, Any]:
        """Evaluate agent response."""
        eval_input = {
            "input": message,
            "output": str(response)
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
# STEP 3: Agent with Tools
# ============================================================================

class ToolBasedAgent:
    """PydanticAI agent with tool/function calling."""

    def __init__(self):
        if not PYDANTIC_AI_AVAILABLE:
            raise ImportError("PydanticAI required")

        # Create agent
        self.agent = Agent(
            'openai:gpt-4o-mini',
            system_prompt="""You are an assistant with access to weather and
            product information tools. Use the tools to answer user questions."""
        )

        # Register tools
        @self.agent.tool
        async def get_weather(ctx: RunContext[None], city: str) -> WeatherInfo:
            """Get weather information for a city."""
            # Simulated weather data
            weather_db = {
                "san francisco": WeatherInfo(
                    city="San Francisco",
                    temperature="72°F",
                    condition="Sunny",
                    humidity=65
                ),
                "new york": WeatherInfo(
                    city="New York",
                    temperature="68°F",
                    condition="Partly Cloudy",
                    humidity=70
                ),
                "london": WeatherInfo(
                    city="London",
                    temperature="58°F",
                    condition="Rainy",
                    humidity=85
                )
            }

            city_lower = city.lower()
            if city_lower in weather_db:
                return weather_db[city_lower]

            return WeatherInfo(
                city=city,
                temperature="N/A",
                condition="Data not available",
                humidity=None
            )

        @self.agent.tool
        async def get_product_info(ctx: RunContext[None], product_name: str) -> ProductInfo:
            """Get product information."""
            # Simulated product database
            products_db = {
                "laptop": ProductInfo(
                    name="Pro Laptop",
                    price=1299.99,
                    category="Electronics",
                    in_stock=True
                ),
                "phone": ProductInfo(
                    name="Smart Phone X",
                    price=899.99,
                    category="Electronics",
                    in_stock=True
                ),
                "headphones": ProductInfo(
                    name="Wireless Headphones",
                    price=199.99,
                    category="Audio",
                    in_stock=False
                )
            }

            product_lower = product_name.lower()
            for key, product in products_db.items():
                if key in product_lower:
                    return product

            return ProductInfo(
                name=product_name,
                price=0.0,
                category="Unknown",
                in_stock=False
            )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm)
        }

    async def run_async(self, query: str) -> Dict[str, Any]:
        """Run agent with tools asynchronously."""
        try:
            result = await self.agent.run(query)
            response = result.data

            return {
                "query": query,
                "response": response,
                "success": True
            }

        except Exception as e:
            return {
                "query": query,
                "response": str(e),
                "success": False,
                "error": str(e)
            }

    def run(self, query: str) -> Dict[str, Any]:
        """Run agent with tools synchronously."""
        import asyncio
        return asyncio.run(self.run_async(query))

    def evaluate(self, query: str, response: str) -> Dict[str, Any]:
        """Evaluate tool-based agent."""
        eval_input = {
            "input": query,
            "output": str(response)
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
# STEP 4: Structured Output Agent
# ============================================================================

class StructuredOutputAgent:
    """Agent that returns structured analysis results."""

    def __init__(self):
        if not PYDANTIC_AI_AVAILABLE:
            raise ImportError("PydanticAI required")

        # Create agent with structured output
        self.agent = Agent(
            'openai:gpt-4o-mini',
            result_type=AnalysisResult,
            system_prompt="""You are an analyst that provides structured analysis.
            Analyze the given topic and provide a summary, key points,
            recommendations, and confidence score."""
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm)
        }

    async def analyze_async(self, topic: str) -> Dict[str, Any]:
        """Analyze topic asynchronously."""
        try:
            result = await self.agent.run(f"Analyze the following topic: {topic}")
            analysis: AnalysisResult = result.data

            return {
                "topic": topic,
                "analysis": analysis,
                "success": True
            }

        except Exception as e:
            return {
                "topic": topic,
                "analysis": None,
                "success": False,
                "error": str(e)
            }

    def analyze(self, topic: str) -> Dict[str, Any]:
        """Analyze topic synchronously."""
        import asyncio
        return asyncio.run(self.analyze_async(topic))

    def evaluate(self, topic: str, analysis: AnalysisResult) -> Dict[str, Any]:
        """Evaluate structured analysis."""
        # Convert analysis to text for evaluation
        response = f"""Summary: {analysis.summary}

Key Points:
{chr(10).join('- ' + point for point in analysis.key_points)}

Recommendations:
{chr(10).join('- ' + rec for rec in analysis.recommendations)}

Confidence: {analysis.confidence}"""

        eval_input = {
            "input": f"Analyze: {topic}",
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
# STEP 5: Testing Functions
# ============================================================================

def test_simple_agent():
    """Test simple PydanticAI agent."""
    print("\n" + "="*80)
    print("TEST 1: Simple PydanticAI Agent")
    print("="*80)

    agent = SimplePydanticAgent()

    test_messages = [
        "What is artificial intelligence?",
        "Explain quantum computing",
        "What are the benefits of renewable energy?"
    ]

    results = []

    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Test {i}/{len(test_messages)} ---")
        print(f"📝 Message: {message}")

        # Run agent
        result = agent.run(message)

        if result["success"]:
            response = result["response"]
            print(f"🤖 Response: {response[:300]}...")

            # Evaluate
            scores = agent.evaluate(message, response)

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


def test_tool_based_agent():
    """Test agent with tools."""
    print("\n" + "="*80)
    print("TEST 2: Tool-Based Agent")
    print("="*80)

    agent = ToolBasedAgent()

    test_queries = [
        {
            "query": "What's the weather in San Francisco?",
            "expected_keywords": ["San Francisco", "sunny", "72"]
        },
        {
            "query": "Tell me about the laptop product",
            "expected_keywords": ["laptop", "1299", "electronics"]
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
            response = str(result["response"])
            print(f"🤖 Response: {response}")

            # Check keywords
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


def test_structured_output():
    """Test structured output agent."""
    print("\n" + "="*80)
    print("TEST 3: Structured Output Agent")
    print("="*80)

    agent = StructuredOutputAgent()

    test_topics = [
        "Impact of AI on healthcare",
        "Future of electric vehicles"
    ]

    results = []

    for i, topic in enumerate(test_topics, 1):
        print(f"\n--- Test {i}/{len(test_topics)} ---")
        print(f"📝 Topic: {topic}")

        # Run analysis
        result = agent.analyze(topic)

        if result["success"]:
            analysis: AnalysisResult = result["analysis"]

            print(f"\n📊 Structured Analysis:")
            print(f"  • Summary: {analysis.summary[:150]}...")
            print(f"  • Key Points: {len(analysis.key_points)} identified")
            print(f"  • Recommendations: {len(analysis.recommendations)} provided")
            print(f"  • Confidence: {analysis.confidence:.2f}")

            # Evaluate
            scores = agent.evaluate(topic, analysis)

            print(f"\n📊 Evaluation:")
            for metric, score in scores.items():
                print(f"  • {metric}: {score.label} ({score.score:.2f})")

            results.append({
                "topic": topic,
                "analysis": analysis,
                "scores": scores,
                "success": True
            })
        else:
            print(f"❌ Error: {result.get('error')}")
            results.append({"topic": topic, "success": False})

    return results


def test_quality_gates():
    """Test with quality gates."""
    print("\n" + "="*80)
    print("TEST 4: Quality Gates")
    print("="*80)

    agent = SimplePydanticAgent()

    # Quality thresholds
    QUALITY_THRESHOLDS = {
        "coherence": 0.7,
        "relevance": 0.7,
        "toxicity": 0.2
    }

    test_messages = [
        "Explain blockchain technology",
        "What is machine learning?",
        "Describe the solar system"
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
        result = agent.run(message)

        if not result["success"]:
            print(f"❌ Agent failed")
            all_passed = False
            continue

        # Evaluate
        scores = agent.evaluate(message, result["response"])

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
    print("🚀 PydanticAI Agent Example with Custom Evals Testing")
    print("="*80)

    if not PYDANTIC_AI_AVAILABLE:
        print("\n❌ PydanticAI not installed")
        print("Install with: pip install pydantic-ai pydantic>=2.0")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY environment variable not set")
        print("Set with: export OPENAI_API_KEY='your-key'")
        return

    try:
        # Test 1: Simple agent
        test_simple_agent()

        # Test 2: Tool-based agent
        test_tool_based_agent()

        # Test 3: Structured output
        test_structured_output()

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
