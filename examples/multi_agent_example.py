"""
Multi-Agent System Example with Custom Evals Testing

This example demonstrates:
1. Creating a multi-agent system with specialized agents
2. Orchestrating agent collaboration
3. Running complex workflows
4. Evaluating multi-agent outputs with custom-evals
5. Testing coordination and quality

Architecture:
- ResearchAgent: Gathers information
- AnalysisAgent: Analyzes data
- WriterAgent: Creates content
- ReviewerAgent: Quality checks
- Orchestrator: Coordinates all agents
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

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
# STEP 1: Define Agent Types and Data Structures
# ============================================================================

class AgentRole(Enum):
    """Agent roles in the multi-agent system."""
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"
    REVIEWER = "reviewer"
    ORCHESTRATOR = "orchestrator"


@dataclass
class AgentMessage:
    """Message passed between agents."""
    sender: AgentRole
    recipient: AgentRole
    content: str
    metadata: Dict[str, Any] = None


@dataclass
class TaskResult:
    """Result from an agent task."""
    agent: AgentRole
    content: str
    success: bool
    metadata: Dict[str, Any] = None


# ============================================================================
# STEP 2: Define Specialized Agents
# ============================================================================

class BaseAgent:
    """Base class for all agents."""

    def __init__(self, role: AgentRole, system_prompt: str):
        self.role = role
        self.system_prompt = system_prompt
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.conversation_history: List[AgentMessage] = []

    def process(self, task: str, context: str = "") -> TaskResult:
        """Process a task with optional context."""
        try:
            # Build prompt
            prompt = f"{self.system_prompt}\n\nTask: {task}"
            if context:
                prompt += f"\n\nContext:\n{context}"

            # Call LLM
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=f"Task: {task}\n\nContext:\n{context}" if context else task)
            ]

            response = self.llm.invoke(messages)
            content = response.content

            return TaskResult(
                agent=self.role,
                content=content,
                success=True,
                metadata={"task": task, "has_context": bool(context)}
            )

        except Exception as e:
            return TaskResult(
                agent=self.role,
                content=f"Error: {str(e)}",
                success=False,
                metadata={"error": str(e)}
            )


class ResearchAgent(BaseAgent):
    """Agent specialized in gathering and organizing information."""

    def __init__(self):
        system_prompt = """You are a Research Agent specialized in gathering information.
Your role is to:
- Identify key information needs
- Organize facts and data
- Provide comprehensive research summaries
- Cite sources when available

Be thorough, accurate, and well-organized."""

        super().__init__(AgentRole.RESEARCHER, system_prompt)

    def research(self, topic: str) -> TaskResult:
        """Research a specific topic."""
        # Simulated knowledge base
        knowledge_base = {
            "machine learning": """Machine Learning is a subset of AI that enables systems to learn from data.
Key concepts: supervised learning, unsupervised learning, neural networks, deep learning.
Applications: computer vision, NLP, recommendation systems, autonomous vehicles.
Popular frameworks: TensorFlow, PyTorch, scikit-learn.""",

            "quantum computing": """Quantum Computing uses quantum mechanics principles for computation.
Key concepts: qubits, superposition, entanglement, quantum gates.
Advantages: exponential speedup for certain problems like factorization and optimization.
Challenges: decoherence, error correction, scalability.
Current state: NISQ (Noisy Intermediate-Scale Quantum) era.""",

            "blockchain": """Blockchain is a distributed ledger technology.
Key concepts: decentralization, immutability, consensus mechanisms, smart contracts.
Applications: cryptocurrencies, supply chain, identity management, voting systems.
Popular platforms: Bitcoin, Ethereum, Hyperledger, Solana.""",

            "climate change": """Climate change refers to long-term shifts in global temperatures and weather patterns.
Causes: greenhouse gas emissions, deforestation, industrial activities.
Effects: rising temperatures, sea level rise, extreme weather events, ecosystem disruption.
Solutions: renewable energy, carbon capture, sustainable practices, policy changes."""
        }

        # Find relevant information
        topic_lower = topic.lower()
        research_data = ""

        for key, info in knowledge_base.items():
            if key in topic_lower:
                research_data = info
                break

        if not research_data:
            research_data = f"Limited information available on {topic}. General context: This is an emerging or specialized topic requiring further investigation."

        task = f"Provide comprehensive research on: {topic}"
        context = f"Available data:\n{research_data}"

        return self.process(task, context)


class AnalysisAgent(BaseAgent):
    """Agent specialized in analyzing data and drawing insights."""

    def __init__(self):
        system_prompt = """You are an Analysis Agent specialized in data analysis.
Your role is to:
- Analyze information critically
- Identify patterns and trends
- Draw meaningful insights
- Make data-driven recommendations

Be analytical, objective, and insightful."""

        super().__init__(AgentRole.ANALYST, system_prompt)

    def analyze(self, data: str, focus: str = "") -> TaskResult:
        """Analyze data with optional focus area."""
        task = f"Analyze the following information"
        if focus:
            task += f" with focus on: {focus}"

        return self.process(task, data)


class WriterAgent(BaseAgent):
    """Agent specialized in content creation."""

    def __init__(self):
        system_prompt = """You are a Writer Agent specialized in content creation.
Your role is to:
- Create clear, engaging content
- Structure information logically
- Adapt tone for the audience
- Ensure proper grammar and style

Be creative, clear, and professional."""

        super().__init__(AgentRole.WRITER, system_prompt)

    def write(self, topic: str, source_material: str, format_type: str = "article") -> TaskResult:
        """Write content based on source material."""
        task = f"Write a {format_type} about: {topic}"
        return self.process(task, source_material)


class ReviewerAgent(BaseAgent):
    """Agent specialized in quality review."""

    def __init__(self):
        system_prompt = """You are a Reviewer Agent specialized in quality assurance.
Your role is to:
- Review content for accuracy
- Check for clarity and coherence
- Identify improvements
- Provide constructive feedback

Be thorough, fair, and constructive."""

        super().__init__(AgentRole.REVIEWER, system_prompt)

    def review(self, content: str, criteria: List[str] = None) -> TaskResult:
        """Review content against criteria."""
        task = "Review the following content for quality"
        if criteria:
            task += f"\n\nCriteria: {', '.join(criteria)}"

        return self.process(task, content)


# ============================================================================
# STEP 3: Multi-Agent Orchestrator
# ============================================================================

class MultiAgentOrchestrator:
    """Orchestrates multiple agents to complete complex tasks."""

    def __init__(self):
        # Initialize all agents
        self.agents = {
            AgentRole.RESEARCHER: ResearchAgent(),
            AgentRole.ANALYST: AnalysisAgent(),
            AgentRole.WRITER: WriterAgent(),
            AgentRole.REVIEWER: ReviewerAgent()
        }

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

        self.workflow_history: List[TaskResult] = []

    def run_research_workflow(self, topic: str) -> Dict[str, Any]:
        """Run complete research workflow: Research -> Analyze -> Write -> Review."""
        print(f"\n{'='*80}")
        print(f"🔄 Starting Research Workflow for: {topic}")
        print(f"{'='*80}")

        workflow_results = {}

        # Step 1: Research
        print("\n📚 Step 1: Research Agent - Gathering information...")
        research_result = self.agents[AgentRole.RESEARCHER].research(topic)
        workflow_results["research"] = research_result
        self.workflow_history.append(research_result)

        if not research_result.success:
            return {"success": False, "error": "Research phase failed", "results": workflow_results}

        print(f"✅ Research completed: {len(research_result.content)} characters")

        # Step 2: Analysis
        print("\n🔍 Step 2: Analysis Agent - Analyzing research data...")
        analysis_result = self.agents[AgentRole.ANALYST].analyze(
            data=research_result.content,
            focus="key insights and implications"
        )
        workflow_results["analysis"] = analysis_result
        self.workflow_history.append(analysis_result)

        if not analysis_result.success:
            return {"success": False, "error": "Analysis phase failed", "results": workflow_results}

        print(f"✅ Analysis completed: {len(analysis_result.content)} characters")

        # Step 3: Writing
        print("\n✍️  Step 3: Writer Agent - Creating content...")
        write_result = self.agents[AgentRole.WRITER].write(
            topic=topic,
            source_material=f"Research:\n{research_result.content}\n\nAnalysis:\n{analysis_result.content}",
            format_type="comprehensive article"
        )
        workflow_results["writing"] = write_result
        self.workflow_history.append(write_result)

        if not write_result.success:
            return {"success": False, "error": "Writing phase failed", "results": workflow_results}

        print(f"✅ Writing completed: {len(write_result.content)} characters")

        # Step 4: Review
        print("\n🔎 Step 4: Reviewer Agent - Quality assurance...")
        review_result = self.agents[AgentRole.REVIEWER].review(
            content=write_result.content,
            criteria=["accuracy", "clarity", "completeness", "coherence"]
        )
        workflow_results["review"] = review_result
        self.workflow_history.append(review_result)

        print(f"✅ Review completed: {len(review_result.content)} characters")

        return {
            "success": True,
            "topic": topic,
            "results": workflow_results,
            "final_content": write_result.content
        }

    def evaluate_workflow(self, topic: str, final_content: str) -> Dict[str, Any]:
        """Evaluate the final output of the workflow."""
        eval_input = {
            "input": f"Create comprehensive content about: {topic}",
            "output": final_content
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

def test_individual_agents():
    """Test each agent individually."""
    print("\n" + "="*80)
    print("TEST 1: Individual Agent Testing")
    print("="*80)

    # Test Research Agent
    print("\n--- Testing Research Agent ---")
    researcher = ResearchAgent()
    result = researcher.research("machine learning")
    print(f"Research Result: {result.content[:200]}...")
    print(f"Success: {result.success}")

    # Test Analysis Agent
    print("\n--- Testing Analysis Agent ---")
    analyst = AnalysisAgent()
    result = analyst.analyze(
        data="Machine learning is growing rapidly. Applications include computer vision and NLP.",
        focus="future trends"
    )
    print(f"Analysis Result: {result.content[:200]}...")
    print(f"Success: {result.success}")

    # Test Writer Agent
    print("\n--- Testing Writer Agent ---")
    writer = WriterAgent()
    result = writer.write(
        topic="AI in Healthcare",
        source_material="AI is revolutionizing healthcare through diagnosis, treatment planning, and drug discovery.",
        format_type="blog post"
    )
    print(f"Writing Result: {result.content[:200]}...")
    print(f"Success: {result.success}")

    # Test Reviewer Agent
    print("\n--- Testing Reviewer Agent ---")
    reviewer = ReviewerAgent()
    result = reviewer.review(
        content="AI is changing healthcare. It helps doctors. It's very good.",
        criteria=["clarity", "depth", "professionalism"]
    )
    print(f"Review Result: {result.content[:200]}...")
    print(f"Success: {result.success}")


def test_complete_workflow():
    """Test complete multi-agent workflow."""
    print("\n" + "="*80)
    print("TEST 2: Complete Workflow - Research to Publication")
    print("="*80)

    orchestrator = MultiAgentOrchestrator()

    # Run workflow
    result = orchestrator.run_research_workflow("quantum computing")

    if result["success"]:
        print("\n" + "="*80)
        print("📄 Final Content Preview:")
        print("="*80)
        print(result["final_content"][:500])
        print("...")

        # Evaluate
        print("\n📊 Evaluating final output...")
        scores = orchestrator.evaluate_workflow(
            result["topic"],
            result["final_content"]
        )

        print("\n📊 Evaluation Results:")
        for metric, score in scores.items():
            print(f"  • {metric.capitalize()}: {score.label} ({score.score:.2f})")
            if score.explanation:
                print(f"    {score.explanation[:100]}...")

    return result


def test_multiple_workflows():
    """Test multiple workflows on different topics."""
    print("\n" + "="*80)
    print("TEST 3: Multiple Workflows - Different Topics")
    print("="*80)

    orchestrator = MultiAgentOrchestrator()

    topics = [
        "blockchain technology",
        "climate change",
        "machine learning"
    ]

    workflow_results = []

    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*80}")
        print(f"Workflow {i}/{len(topics)}: {topic}")
        print(f"{'='*80}")

        result = orchestrator.run_research_workflow(topic)

        if result["success"]:
            scores = orchestrator.evaluate_workflow(topic, result["final_content"])
            workflow_results.append({
                "topic": topic,
                "result": result,
                "scores": scores,
                "success": True
            })
        else:
            workflow_results.append({
                "topic": topic,
                "result": result,
                "success": False
            })

    # Summary
    print("\n" + "="*80)
    print("SUMMARY - Multiple Workflows")
    print("="*80)

    success_count = sum(1 for r in workflow_results if r["success"])
    print(f"  • Successful Workflows: {success_count}/{len(topics)}")

    if success_count > 0:
        avg_coherence = sum(
            r["scores"]["coherence"].score for r in workflow_results if r["success"]
        ) / success_count

        avg_relevance = sum(
            r["scores"]["relevance"].score for r in workflow_results if r["success"]
        ) / success_count

        print(f"  • Average Coherence: {avg_coherence:.2f}")
        print(f"  • Average Relevance: {avg_relevance:.2f}")

    return workflow_results


def test_workflow_quality_gates():
    """Test workflows with quality gates."""
    print("\n" + "="*80)
    print("TEST 4: Workflow Quality Gates")
    print("="*80)

    orchestrator = MultiAgentOrchestrator()

    # Quality thresholds
    QUALITY_THRESHOLDS = {
        "coherence": 0.7,
        "relevance": 0.8,
        "toxicity": 0.2
    }

    topic = "machine learning applications"

    print(f"\n🧪 Testing workflow with quality gates...")
    print(f"Topic: {topic}")
    print(f"\n🚦 Quality Thresholds:")
    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric == "toxicity":
            print(f"  • {metric.capitalize()}: <= {threshold}")
        else:
            print(f"  • {metric.capitalize()}: >= {threshold}")

    # Run workflow
    result = orchestrator.run_research_workflow(topic)

    if not result["success"]:
        print("\n❌ Workflow failed")
        return False

    # Evaluate
    scores = orchestrator.evaluate_workflow(topic, result["final_content"])

    # Check quality gates
    print("\n🚦 Quality Gate Results:")
    all_passed = True

    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric not in scores:
            continue

        score_value = scores[metric].score

        if metric == "toxicity":
            passed = score_value <= threshold
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  • {metric.capitalize()}: {score_value:.2f} <= {threshold} {status}")
        else:
            passed = score_value >= threshold
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  • {metric.capitalize()}: {score_value:.2f} >= {threshold} {status}")

        if not passed:
            all_passed = False

    if all_passed:
        print("\n✅ All quality gates PASSED - Workflow ready for production!")
    else:
        print("\n⚠️  Some quality gates FAILED - Workflow needs improvement")

    return all_passed


def test_agent_collaboration():
    """Test agent collaboration and handoffs."""
    print("\n" + "="*80)
    print("TEST 5: Agent Collaboration - Information Flow")
    print("="*80)

    orchestrator = MultiAgentOrchestrator()

    topic = "blockchain technology"

    print(f"\n🔄 Testing agent collaboration for: {topic}")
    print("\nTracking information flow through agents...\n")

    # Run workflow and track
    result = orchestrator.run_research_workflow(topic)

    if result["success"]:
        print("\n📊 Collaboration Analysis:")

        # Check information flow
        workflow_results = result["results"]

        research_len = len(workflow_results["research"].content)
        analysis_len = len(workflow_results["analysis"].content)
        writing_len = len(workflow_results["writing"].content)
        review_len = len(workflow_results["review"].content)

        print(f"  • Research output: {research_len} characters")
        print(f"  • Analysis output: {analysis_len} characters")
        print(f"  • Writing output: {writing_len} characters")
        print(f"  • Review output: {review_len} characters")

        # Verify each agent built upon previous work
        final_content = workflow_results["writing"].content.lower()
        research_keywords = ["machine", "learning", "data"] if "machine" in topic.lower() else ["blockchain", "technology"]

        has_research_info = any(keyword in final_content for keyword in research_keywords)
        print(f"\n  • Final content incorporates research: {'✅' if has_research_info else '❌'}")

        # Check review quality
        review_content = workflow_results["review"].content
        has_feedback = any(word in review_content.lower() for word in ["good", "improve", "strength", "weakness", "clear"])
        print(f"  • Review provides feedback: {'✅' if has_feedback else '❌'}")

    return result


# ============================================================================
# STEP 5: Main Execution
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🚀 Multi-Agent System Example with Custom Evals Testing")
    print("="*80)

    try:
        # Test 1: Individual agents
        test_individual_agents()

        # Test 2: Complete workflow
        test_complete_workflow()

        # Test 3: Multiple workflows
        test_multiple_workflows()

        # Test 4: Quality gates
        test_workflow_quality_gates()

        # Test 5: Agent collaboration
        test_agent_collaboration()

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
