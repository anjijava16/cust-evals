"""
CrewAI Agent Example with Custom Evals Testing

This example demonstrates:
1. Creating CrewAI agents with roles and goals
2. Defining tasks for agents
3. Orchestrating crews for complex workflows
4. Sequential and hierarchical processes
5. Evaluating crew outputs with custom-evals

CrewAI is a framework for orchestrating role-based AI agents.

Requirements:
- crewai (pip install crewai)
- crewai-tools (pip install crewai-tools) [optional]
"""

import os
from typing import Dict, Any, List

try:
    from crewai import Agent, Task, Crew, Process
    from crewai_tools import SerperDevTool, WebsiteSearchTool
    CREWAI_AVAILABLE = True
    CREWAI_TOOLS_AVAILABLE = True
except ImportError as e:
    CREWAI_AVAILABLE = False
    CREWAI_TOOLS_AVAILABLE = False
    if "crewai_tools" in str(e):
        try:
            from crewai import Agent, Task, Crew, Process
            CREWAI_AVAILABLE = True
        except:
            pass
    print(f"⚠️  CrewAI not fully installed: {e}")
    print("Install with: pip install crewai crewai-tools")

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
# STEP 1: Simple CrewAI System
# ============================================================================

class SimpleCrewSystem:
    """Simple crew with researcher and writer agents."""

    def __init__(self):
        if not CREWAI_AVAILABLE:
            raise ImportError("crewai package required")

        # Create agents
        self.researcher = Agent(
            role="Research Analyst",
            goal="Gather comprehensive information on given topics",
            backstory="""You are an experienced research analyst with expertise in
            gathering and synthesizing information from various sources. You are
            thorough, accurate, and always cite your sources.""",
            verbose=True,
            allow_delegation=False,
            llm="gpt-4o-mini"
        )

        self.writer = Agent(
            role="Content Writer",
            goal="Create engaging and informative content",
            backstory="""You are a skilled content writer with a talent for making
            complex topics accessible to a general audience. You write in a clear,
            engaging style and always structure your content logically.""",
            verbose=True,
            allow_delegation=False,
            llm="gpt-4o-mini"
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, topic: str) -> Dict[str, Any]:
        """Run crew on a topic."""
        try:
            # Create tasks
            research_task = Task(
                description=f"""Research the topic: {topic}

                Provide:
                1. Key facts and definitions
                2. Main concepts and principles
                3. Current trends or developments
                4. Important statistics or data points

                Be thorough and well-organized.""",
                agent=self.researcher,
                expected_output="Comprehensive research findings with key facts and data"
            )

            writing_task = Task(
                description=f"""Based on the research findings, write an informative article about: {topic}

                Your article should:
                1. Start with a clear introduction
                2. Explain key concepts
                3. Include relevant examples
                4. End with a conclusion

                Make it engaging and accessible.""",
                agent=self.writer,
                expected_output="Well-written article of 300-500 words",
                context=[research_task]  # Depends on research task
            )

            # Create crew
            crew = Crew(
                agents=[self.researcher, self.writer],
                tasks=[research_task, writing_task],
                process=Process.sequential,
                verbose=True
            )

            # Execute
            result = crew.kickoff()

            return {
                "topic": topic,
                "output": str(result),
                "success": True
            }

        except Exception as e:
            return {
                "topic": topic,
                "output": str(e),
                "success": False,
                "error": str(e)
            }

    def evaluate(self, topic: str, output: str) -> Dict[str, Any]:
        """Evaluate crew output."""
        eval_input = {
            "input": f"Write about: {topic}",
            "output": output
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
# STEP 2: Multi-Agent Crew with Specialized Roles
# ============================================================================

class SpecializedCrew:
    """Crew with multiple specialized agents."""

    def __init__(self):
        if not CREWAI_AVAILABLE:
            raise ImportError("crewai package required")

        # Create specialized agents
        self.market_researcher = Agent(
            role="Market Research Specialist",
            goal="Analyze market trends and consumer behavior",
            backstory="""You are a market research specialist with 10 years of experience
            in analyzing market trends, consumer behavior, and competitive landscapes.""",
            verbose=True,
            allow_delegation=False,
            llm="gpt-4o-mini"
        )

        self.data_analyst = Agent(
            role="Data Analyst",
            goal="Extract insights from data and identify patterns",
            backstory="""You are a data analyst expert in statistical analysis and
            data visualization. You excel at finding meaningful patterns in data.""",
            verbose=True,
            allow_delegation=False,
            llm="gpt-4o-mini"
        )

        self.business_strategist = Agent(
            role="Business Strategist",
            goal="Develop actionable business strategies",
            backstory="""You are a business strategist with expertise in corporate
            strategy, business development, and strategic planning.""",
            verbose=True,
            allow_delegation=False,
            llm="gpt-4o-mini"
        )

        self.report_writer = Agent(
            role="Report Writer",
            goal="Create professional business reports",
            backstory="""You are a professional report writer skilled in creating
            clear, concise, and actionable business documents.""",
            verbose=True,
            allow_delegation=False,
            llm="gpt-4o-mini"
        )

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def run(self, business_question: str) -> Dict[str, Any]:
        """Run specialized crew on business question."""
        try:
            # Create tasks
            market_research_task = Task(
                description=f"""Conduct market research on: {business_question}

                Focus on:
                1. Market size and growth trends
                2. Key competitors and market share
                3. Consumer preferences and behavior
                4. Market opportunities and threats""",
                agent=self.market_researcher,
                expected_output="Market research findings with trends and insights"
            )

            data_analysis_task = Task(
                description="""Analyze the market research data and extract key insights.

                Provide:
                1. Statistical trends
                2. Pattern analysis
                3. Key metrics and KPIs
                4. Data-driven observations""",
                agent=self.data_analyst,
                expected_output="Data analysis with statistical insights",
                context=[market_research_task]
            )

            strategy_task = Task(
                description=f"""Based on the market research and data analysis,
                develop a strategic recommendation for: {business_question}

                Include:
                1. Strategic objectives
                2. Recommended actions
                3. Implementation priorities
                4. Expected outcomes""",
                agent=self.business_strategist,
                expected_output="Strategic recommendations with action items",
                context=[market_research_task, data_analysis_task]
            )

            report_task = Task(
                description="""Create a comprehensive business report summarizing
                the market research, data analysis, and strategic recommendations.

                Format:
                1. Executive Summary
                2. Market Research Findings
                3. Data Analysis Insights
                4. Strategic Recommendations
                5. Conclusion""",
                agent=self.report_writer,
                expected_output="Professional business report",
                context=[market_research_task, data_analysis_task, strategy_task]
            )

            # Create crew
            crew = Crew(
                agents=[
                    self.market_researcher,
                    self.data_analyst,
                    self.business_strategist,
                    self.report_writer
                ],
                tasks=[
                    market_research_task,
                    data_analysis_task,
                    strategy_task,
                    report_task
                ],
                process=Process.sequential,
                verbose=True
            )

            # Execute
            result = crew.kickoff()

            return {
                "question": business_question,
                "output": str(result),
                "success": True
            }

        except Exception as e:
            return {
                "question": business_question,
                "output": str(e),
                "success": False,
                "error": str(e)
            }

    def evaluate(self, question: str, output: str) -> Dict[str, Any]:
        """Evaluate specialized crew output."""
        eval_input = {
            "input": question,
            "output": output
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
# STEP 3: Testing Functions
# ============================================================================

def test_simple_crew():
    """Test simple two-agent crew."""
    print("\n" + "="*80)
    print("TEST 1: Simple Crew - Research & Writing")
    print("="*80)

    crew = SimpleCrewSystem()

    test_topics = [
        "Artificial Intelligence in Healthcare",
        "Renewable Energy Technologies"
    ]

    results = []

    for i, topic in enumerate(test_topics, 1):
        print(f"\n--- Test {i}/{len(test_topics)} ---")
        print(f"📝 Topic: {topic}")

        # Run crew
        result = crew.run(topic)

        if result["success"]:
            output = result["output"]
            print(f"\n📄 Output Preview:")
            print(output[:500])
            print("..." if len(output) > 500 else "")

            # Evaluate
            scores = crew.evaluate(topic, output)

            print(f"\n📊 Evaluation:")
            for metric, score in scores.items():
                print(f"  • {metric}: {score.label} ({score.score:.2f})")

            results.append({
                "topic": topic,
                "output": output,
                "scores": scores,
                "success": True
            })
        else:
            print(f"❌ Error: {result.get('error')}")
            results.append({"topic": topic, "success": False})

    # Summary
    success_count = sum(1 for r in results if r["success"])
    print(f"\n📊 Summary: {success_count}/{len(test_topics)} successful")

    return results


def test_specialized_crew():
    """Test specialized multi-agent crew."""
    print("\n" + "="*80)
    print("TEST 2: Specialized Crew - Business Analysis")
    print("="*80)

    crew = SpecializedCrew()

    test_questions = [
        "What are the opportunities in the electric vehicle market?",
        "How can a startup compete in the food delivery space?"
    ]

    results = []

    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Test {i}/{len(test_questions)} ---")
        print(f"📝 Question: {question}")

        # Run crew
        result = crew.run(question)

        if result["success"]:
            output = result["output"]
            print(f"\n📄 Report Preview:")
            print(output[:600])
            print("..." if len(output) > 600 else "")

            # Evaluate
            scores = crew.evaluate(question, output)

            print(f"\n📊 Evaluation:")
            for metric, score in scores.items():
                print(f"  • {metric}: {score.label} ({score.score:.2f})")

            results.append({
                "question": question,
                "output": output,
                "scores": scores,
                "success": True
            })
        else:
            print(f"❌ Error: {result.get('error')}")
            results.append({"question": question, "success": False})

    return results


def test_quality_gates():
    """Test crew with quality gates."""
    print("\n" + "="*80)
    print("TEST 3: Quality Gates for Crew Outputs")
    print("="*80)

    crew = SimpleCrewSystem()

    # Quality thresholds
    QUALITY_THRESHOLDS = {
        "coherence": 0.7,
        "relevance": 0.7,
        "toxicity": 0.2
    }

    test_topics = [
        "Machine Learning Applications",
        "Climate Change Solutions"
    ]

    print(f"\n🚦 Quality Thresholds:")
    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric == "toxicity":
            print(f"  • {metric}: <= {threshold}")
        else:
            print(f"  • {metric}: >= {threshold}")

    all_passed = True
    results = []

    for i, topic in enumerate(test_topics, 1):
        print(f"\n[{i}/{len(test_topics)}] Topic: {topic}")

        # Run crew
        result = crew.run(topic)

        if not result["success"]:
            print(f"❌ Crew failed")
            all_passed = False
            continue

        # Evaluate
        scores = crew.evaluate(topic, result["output"])

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
            "topic": topic,
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


def test_crew_comparison():
    """Compare simple vs specialized crew."""
    print("\n" + "="*80)
    print("TEST 4: Crew Comparison - Simple vs Specialized")
    print("="*80)

    simple_crew = SimpleCrewSystem()
    specialized_crew = SpecializedCrew()

    topic = "E-commerce market trends"

    print(f"\n📝 Topic: {topic}\n")

    # Test simple crew
    print("--- Simple Crew (2 agents) ---")
    simple_result = simple_crew.run(topic)

    if simple_result["success"]:
        simple_output = simple_result["output"]
        simple_scores = simple_crew.evaluate(topic, simple_output)

        print(f"Output length: {len(simple_output)} characters")
        print("Scores:")
        for metric, score in simple_scores.items():
            print(f"  • {metric}: {score.score:.2f}")

    # Test specialized crew
    print("\n--- Specialized Crew (4 agents) ---")
    spec_result = specialized_crew.run(f"Analyze {topic}")

    if spec_result["success"]:
        spec_output = spec_result["output"]
        spec_scores = specialized_crew.evaluate(topic, spec_output)

        print(f"Output length: {len(spec_output)} characters")
        print("Scores:")
        for metric, score in spec_scores.items():
            print(f"  • {metric}: {score.score:.2f}")

    # Comparison
    print(f"\n{'='*80}")
    print("📊 Comparison:")
    if simple_result["success"] and spec_result["success"]:
        print(f"  • Simple crew output: {len(simple_output)} chars")
        print(f"  • Specialized crew output: {len(spec_output)} chars")
        print(f"  • Specialized is {len(spec_output) / len(simple_output):.1f}x longer")


# ============================================================================
# STEP 4: Main Execution
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🚀 CrewAI Agent Example with Custom Evals Testing")
    print("="*80)

    if not CREWAI_AVAILABLE:
        print("\n❌ crewai package not installed")
        print("Install with: pip install crewai")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY environment variable not set")
        print("Set with: export OPENAI_API_KEY='your-key'")
        return

    try:
        # Test 1: Simple crew
        test_simple_crew()

        # Test 2: Specialized crew
        test_specialized_crew()

        # Test 3: Quality gates
        test_quality_gates()

        # Test 4: Crew comparison
        test_crew_comparison()

        print("\n" + "="*80)
        print("✅ All tests completed!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
