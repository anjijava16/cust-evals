"""
Lesson 13: Multi-Agent System Evaluation (Advanced)

Learn to evaluate systems where multiple AI agents collaborate,
communicate, and coordinate to solve complex tasks.

Prerequisites: Lessons 1-12
Difficulty: ⭐⭐⭐ Advanced
Time: 50 minutes
"""

print("="*80)
print("LESSON 13: Multi-Agent System Evaluation")
print("="*80)

print("""
🤖🤖🤖 MULTI-AGENT SYSTEMS

Single agent: One LLM handles everything
Multi-agent: Multiple specialized agents collaborate

Example system:
- Researcher agent: Gathers information
- Analyst agent: Analyzes data
- Writer agent: Produces report
- Critic agent: Reviews and provides feedback

Evaluation challenges:
• Individual agent performance
• Inter-agent communication
• Task coordination
• System-level outcomes
• Emergent behaviors

This lesson shows how to evaluate multi-agent systems comprehensively.
""")

from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
import json

# ============================================================================
# PART 1: AGENT COMMUNICATION EVALUATION
# ============================================================================

print("\n" + "="*80)
print("PART 1: Agent Communication Evaluation")
print("="*80)

print("""
💬 AGENT COMMUNICATION:

Agents need to exchange information effectively.

Communication quality metrics:
1. Clarity: Is the message understandable?
2. Relevance: Is information pertinent?
3. Completeness: Is all needed info included?
4. Timeliness: Is it sent at the right time?
5. Format: Is structure appropriate?
""")

class CommunicationEvaluator:
    """Evaluate inter-agent communication."""

    def evaluate_message(
        self,
        sender: str,
        receiver: str,
        message: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate a single agent-to-agent message."""

        # Check clarity (message has required fields)
        required_fields = ['content', 'type', 'metadata']
        clarity_score = sum(1 for field in required_fields if field in message) / len(required_fields)

        # Check relevance (content matches receiver's needs)
        receiver_needs = context.get('receiver_needs', [])
        content_lower = str(message.get('content', '')).lower()
        relevance_score = sum(
            1 for need in receiver_needs
            if need.lower() in content_lower
        ) / len(receiver_needs) if receiver_needs else 0.5

        # Check completeness (has sufficient detail)
        content_length = len(str(message.get('content', '')).split())
        completeness_score = min(1.0, content_length / 20)  # At least 20 words

        # Overall score
        overall = (clarity_score + relevance_score + completeness_score) / 3

        return {
            'sender': sender,
            'receiver': receiver,
            'clarity': clarity_score,
            'relevance': relevance_score,
            'completeness': completeness_score,
            'overall_score': overall,
            'passed': overall >= 0.7
        }

    def evaluate_conversation(
        self,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Evaluate a full conversation between agents."""

        if not messages:
            return {'error': 'No messages to evaluate'}

        # Analyze message flow
        senders = [msg.get('sender') for msg in messages]
        unique_agents = set(senders)

        # Check turn-taking (not dominated by one agent)
        sender_counts = defaultdict(int)
        for sender in senders:
            sender_counts[sender] += 1

        max_messages = max(sender_counts.values())
        min_messages = min(sender_counts.values())
        balance_ratio = min_messages / max_messages if max_messages > 0 else 0

        # Check for deadlocks (repeated messages)
        repeated_patterns = self._detect_repetition(messages)

        # Check convergence (agents reaching conclusion)
        converged = self._check_convergence(messages)

        return {
            'total_messages': len(messages),
            'unique_agents': len(unique_agents),
            'balance_ratio': balance_ratio,
            'balanced_participation': balance_ratio > 0.5,
            'has_repetition': repeated_patterns > 0,
            'repetition_count': repeated_patterns,
            'converged': converged,
            'avg_message_length': sum(len(str(m.get('content', '')).split()) for m in messages) / len(messages)
        }

    def _detect_repetition(self, messages: List[Dict]) -> int:
        """Detect repeated message patterns."""
        if len(messages) < 2:
            return 0

        repetitions = 0
        for i in range(len(messages) - 1):
            msg1 = str(messages[i].get('content', ''))
            msg2 = str(messages[i + 1].get('content', ''))

            # Check for very similar consecutive messages
            words1 = set(msg1.lower().split())
            words2 = set(msg2.lower().split())

            if words1 and words2:
                similarity = len(words1 & words2) / len(words1 | words2)
                if similarity > 0.8:
                    repetitions += 1

        return repetitions

    def _check_convergence(self, messages: List[Dict]) -> bool:
        """Check if conversation reached a conclusion."""
        if not messages:
            return False

        last_message = messages[-1]
        content = str(last_message.get('content', '')).lower()

        convergence_indicators = [
            'conclusion', 'decided', 'agreed', 'final',
            'complete', 'done', 'resolved'
        ]

        return any(indicator in content for indicator in convergence_indicators)

# Demo
print("\n💬 Example: Agent communication evaluation")

comm_evaluator = CommunicationEvaluator()

# Evaluate single message
message = {
    'sender': 'researcher',
    'receiver': 'analyst',
    'type': 'data_delivery',
    'content': 'Here is the market data from Q1 2025: revenue $10M, growth 25%, new customers 1500',
    'metadata': {'timestamp': '2025-01-15'}
}

context = {
    'receiver_needs': ['revenue', 'growth', 'customers']
}

result = comm_evaluator.evaluate_message(
    sender='researcher',
    receiver='analyst',
    message=message,
    context=context
)

print(f"Message from {result['sender']} to {result['receiver']}:")
print(f"  Clarity: {result['clarity']:.2f}")
print(f"  Relevance: {result['relevance']:.2f}")
print(f"  Completeness: {result['completeness']:.2f}")
print(f"  Overall: {result['overall_score']:.2f}")
print(f"  Status: {'✓ PASS' if result['passed'] else '✗ FAIL'}")

# Evaluate conversation
conversation = [
    {'sender': 'user', 'content': 'Analyze competitor pricing'},
    {'sender': 'researcher', 'content': 'Gathering competitor data...'},
    {'sender': 'researcher', 'content': 'Found 5 competitors with avg price $49'},
    {'sender': 'analyst', 'content': 'Our price $59 is 20% higher than average'},
    {'sender': 'strategist', 'content': 'Recommendation: reduce to $52 or add features'},
    {'sender': 'critic', 'content': 'Analysis complete, conclusion reached'}
]

conv_result = comm_evaluator.evaluate_conversation(conversation)
print(f"\nConversation analysis:")
print(f"  Total messages: {conv_result['total_messages']}")
print(f"  Agents involved: {conv_result['unique_agents']}")
print(f"  Balanced participation: {'✓ Yes' if conv_result['balanced_participation'] else '✗ No'} ({conv_result['balance_ratio']:.2f})")
print(f"  Repetition detected: {'⚠️  Yes' if conv_result['has_repetition'] else '✓ No'}")
print(f"  Converged: {'✓ Yes' if conv_result['converged'] else '✗ No'}")

# ============================================================================
# PART 2: TASK COORDINATION EVALUATION
# ============================================================================

print("\n\n" + "="*80)
print("PART 2: Task Coordination Evaluation")
print("="*80)

print("""
🎯 TASK COORDINATION:

Complex task → Break into subtasks → Assign to agents → Coordinate

Example: "Write a market analysis report"
- Agent A: Research market data
- Agent B: Analyze trends
- Agent C: Write report
- Agent D: Review quality

Evaluation:
• Proper task decomposition
• Efficient assignment
• Handling dependencies
• Parallel execution where possible
""")

class CoordinationEvaluator:
    """Evaluate task coordination in multi-agent systems."""

    def evaluate_task_distribution(
        self,
        task: str,
        subtasks: List[Dict[str, Any]],
        agent_capabilities: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """Evaluate how well task was decomposed and distributed."""

        # Check if task is fully decomposed
        total_coverage = self._estimate_task_coverage(task, subtasks)

        # Check if agents are matched to capabilities
        assignments = []
        mismatches = 0

        for subtask in subtasks:
            assigned_agent = subtask.get('assigned_to')
            required_skill = subtask.get('requires_skill')

            if assigned_agent and required_skill:
                agent_skills = agent_capabilities.get(assigned_agent, [])
                matched = required_skill in agent_skills
                assignments.append({
                    'subtask': subtask.get('description', ''),
                    'agent': assigned_agent,
                    'matched': matched
                })
                if not matched:
                    mismatches += 1

        # Check for load balancing
        agent_loads = defaultdict(int)
        for subtask in subtasks:
            agent = subtask.get('assigned_to')
            if agent:
                agent_loads[agent] += 1

        if agent_loads:
            max_load = max(agent_loads.values())
            min_load = min(agent_loads.values())
            load_balance = min_load / max_load if max_load > 0 else 0
        else:
            load_balance = 0

        # Check for parallelization opportunities
        can_parallelize = self._count_parallel_tasks(subtasks)

        return {
            'num_subtasks': len(subtasks),
            'task_coverage': total_coverage,
            'skill_matches': len(assignments) - mismatches,
            'skill_mismatches': mismatches,
            'match_rate': (len(assignments) - mismatches) / len(assignments) if assignments else 0,
            'load_balance': load_balance,
            'parallelizable_tasks': can_parallelize,
            'efficient': total_coverage > 0.8 and mismatches == 0 and load_balance > 0.6
        }

    def _estimate_task_coverage(self, task: str, subtasks: List[Dict]) -> float:
        """Estimate what % of task is covered by subtasks."""
        task_words = set(task.lower().split())

        if not task_words:
            return 0.0

        covered_words = set()
        for subtask in subtasks:
            desc = subtask.get('description', '')
            covered_words.update(desc.lower().split())

        coverage = len(task_words & covered_words) / len(task_words)
        return min(1.0, coverage * 1.5)  # Scale up a bit

    def _count_parallel_tasks(self, subtasks: List[Dict]) -> int:
        """Count tasks that can run in parallel."""
        # Tasks without dependencies can run in parallel
        parallel_count = sum(
            1 for subtask in subtasks
            if not subtask.get('depends_on')
        )
        return parallel_count

# Demo
print("\n🎯 Example: Task coordination evaluation")

coord_evaluator = CoordinationEvaluator()

task = "Create comprehensive market analysis report with trends and recommendations"

subtasks = [
    {
        'description': 'Research market data and statistics',
        'assigned_to': 'researcher',
        'requires_skill': 'research',
        'depends_on': None
    },
    {
        'description': 'Analyze trends and patterns',
        'assigned_to': 'analyst',
        'requires_skill': 'analysis',
        'depends_on': 'research'
    },
    {
        'description': 'Write report document',
        'assigned_to': 'writer',
        'requires_skill': 'writing',
        'depends_on': 'analysis'
    },
    {
        'description': 'Review report quality',
        'assigned_to': 'critic',
        'requires_skill': 'review',
        'depends_on': 'writing'
    }
]

agent_capabilities = {
    'researcher': ['research', 'data_collection'],
    'analyst': ['analysis', 'statistics'],
    'writer': ['writing', 'documentation'],
    'critic': ['review', 'quality_assurance']
}

result = coord_evaluator.evaluate_task_distribution(
    task=task,
    subtasks=subtasks,
    agent_capabilities=agent_capabilities
)

print(f"Task: {task}")
print(f"\nCoordination analysis:")
print(f"  Subtasks: {result['num_subtasks']}")
print(f"  Task coverage: {result['task_coverage']:.1%}")
print(f"  Skill matches: {result['skill_matches']}/{result['skill_matches'] + result['skill_mismatches']}")
print(f"  Match rate: {result['match_rate']:.1%}")
print(f"  Load balance: {result['load_balance']:.2f}")
print(f"  Parallel tasks: {result['parallelizable_tasks']}")
print(f"  Efficient: {'✓ Yes' if result['efficient'] else '✗ No'}")

# ============================================================================
# PART 3: CONSENSUS BUILDING EVALUATION
# ============================================================================

print("\n\n" + "="*80)
print("PART 3: Consensus Building Evaluation")
print("="*80)

print("""
🤝 CONSENSUS BUILDING:

When agents disagree, they need to reach consensus.

Patterns:
- Voting
- Weighted opinions
- Iterative refinement
- Mediator agent

Evaluation:
• Time to consensus
• Quality of final decision
• All perspectives considered
• No domination by single agent
""")

class ConsensusEvaluator:
    """Evaluate consensus building processes."""

    def evaluate_consensus_process(
        self,
        initial_positions: Dict[str, Any],
        discussion_rounds: List[Dict],
        final_decision: Any,
        ground_truth: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Evaluate how agents reached consensus."""

        num_agents = len(initial_positions)
        num_rounds = len(discussion_rounds)

        # Check if consensus was reached
        final_positions = discussion_rounds[-1] if discussion_rounds else initial_positions
        consensus_reached = self._check_consensus(final_positions)

        # Check if process was efficient
        efficiency = 1.0 / (num_rounds + 1)  # Fewer rounds = more efficient

        # Check if all agents participated
        participants = set()
        for round_data in discussion_rounds:
            participants.update(round_data.keys())

        participation_rate = len(participants) / num_agents if num_agents > 0 else 0

        # Check decision quality if ground truth available
        decision_quality = None
        if ground_truth is not None:
            decision_quality = self._compare_to_truth(final_decision, ground_truth)

        return {
            'num_agents': num_agents,
            'num_rounds': num_rounds,
            'consensus_reached': consensus_reached,
            'efficiency_score': efficiency,
            'participation_rate': participation_rate,
            'decision_quality': decision_quality,
            'converged_quickly': num_rounds <= 3,
            'inclusive': participation_rate >= 0.8
        }

    def _check_consensus(self, positions: Dict) -> bool:
        """Check if agents have reached consensus."""
        values = list(positions.values())

        if not values:
            return False

        # For simplicity, check if all values are similar
        # In real systems, this would be more sophisticated
        first_val = str(values[0]).lower()

        return all(
            str(val).lower() == first_val
            for val in values
        )

    def _compare_to_truth(self, decision: Any, truth: Any) -> float:
        """Compare final decision to ground truth."""
        decision_str = str(decision).lower()
        truth_str = str(truth).lower()

        if decision_str == truth_str:
            return 1.0

        # Partial credit for similar answers
        decision_words = set(decision_str.split())
        truth_words = set(truth_str.split())

        if not truth_words:
            return 0.0

        overlap = len(decision_words & truth_words)
        return overlap / len(truth_words)

# Demo
print("\n🤝 Example: Consensus building evaluation")

consensus_evaluator = ConsensusEvaluator()

initial_positions = {
    'agent_a': 'Increase price to $59',
    'agent_b': 'Keep price at $49',
    'agent_c': 'Reduce price to $45'
}

discussion_rounds = [
    {
        'agent_a': 'Maybe $54 is reasonable',
        'agent_b': 'I can accept $54',
        'agent_c': 'Okay, $54 works'
    },
    {
        'agent_a': '$54 agreed',
        'agent_b': '$54 agreed',
        'agent_c': '$54 agreed'
    }
]

final_decision = '$54'
ground_truth = '$52'  # Optimal price from data

result = consensus_evaluator.evaluate_consensus_process(
    initial_positions=initial_positions,
    discussion_rounds=discussion_rounds,
    final_decision=final_decision,
    ground_truth=ground_truth
)

print(f"Consensus process:")
print(f"  Agents: {result['num_agents']}")
print(f"  Rounds: {result['num_rounds']}")
print(f"  Consensus reached: {'✓ Yes' if result['consensus_reached'] else '✗ No'}")
print(f"  Efficiency: {result['efficiency_score']:.2f}")
print(f"  Participation: {result['participation_rate']:.1%}")
print(f"  Decision quality: {result['decision_quality']:.2f}")
print(f"  Converged quickly: {'✓ Yes' if result['converged_quickly'] else '✗ No'}")
print(f"  Inclusive: {'✓ Yes' if result['inclusive'] else '✗ No'}")

# ============================================================================
# PART 4: SYSTEM-LEVEL EVALUATION
# ============================================================================

print("\n\n" + "="*80)
print("PART 4: System-Level Evaluation")
print("="*80)

print("""
📊 SYSTEM-LEVEL METRICS:

Beyond individual agents, evaluate the system as a whole:

1. Task completion success rate
2. Overall latency
3. Resource utilization
4. Fault tolerance
5. Scalability
6. Output quality

These metrics capture emergent system properties.
""")

class SystemLevelEvaluator:
    """Evaluate multi-agent system as a whole."""

    def evaluate_system_performance(
        self,
        tasks_completed: int,
        tasks_attempted: int,
        total_latency: float,
        agent_costs: Dict[str, float],
        output_quality_scores: List[float],
        failures: List[Dict]
    ) -> Dict[str, Any]:
        """Comprehensive system evaluation."""

        # Success rate
        success_rate = tasks_completed / tasks_attempted if tasks_attempted > 0 else 0

        # Average latency
        avg_latency = total_latency / tasks_completed if tasks_completed > 0 else float('inf')

        # Total cost
        total_cost = sum(agent_costs.values())

        # Average quality
        avg_quality = sum(output_quality_scores) / len(output_quality_scores) if output_quality_scores else 0

        # Fault tolerance (how system handles failures)
        failure_rate = len(failures) / tasks_attempted if tasks_attempted > 0 else 0
        fault_tolerant = failure_rate < 0.1

        # Efficiency (quality per unit cost)
        efficiency = avg_quality / total_cost if total_cost > 0 else 0

        return {
            'success_rate': success_rate,
            'avg_latency_seconds': avg_latency,
            'total_cost': total_cost,
            'avg_output_quality': avg_quality,
            'failure_rate': failure_rate,
            'fault_tolerant': fault_tolerant,
            'efficiency': efficiency,
            'system_healthy': success_rate >= 0.9 and avg_quality >= 0.7 and fault_tolerant
        }

# Demo
print("\n📊 Example: System-level evaluation")

sys_evaluator = SystemLevelEvaluator()

result = sys_evaluator.evaluate_system_performance(
    tasks_completed=95,
    tasks_attempted=100,
    total_latency=475.0,  # seconds
    agent_costs={'researcher': 2.5, 'analyst': 3.0, 'writer': 2.0, 'critic': 1.5},
    output_quality_scores=[0.85, 0.90, 0.88, 0.92, 0.87] * 19,  # 95 scores
    failures=[
        {'task_id': 23, 'reason': 'timeout'},
        {'task_id': 67, 'reason': 'agent_unavailable'}
    ]
)

print(f"System performance:")
print(f"  Success rate: {result['success_rate']:.1%}")
print(f"  Avg latency: {result['avg_latency_seconds']:.1f}s")
print(f"  Total cost: ${result['total_cost']:.2f}")
print(f"  Avg quality: {result['avg_output_quality']:.2f}")
print(f"  Failure rate: {result['failure_rate']:.1%}")
print(f"  Fault tolerant: {'✓ Yes' if result['fault_tolerant'] else '✗ No'}")
print(f"  Efficiency: {result['efficiency']:.3f} quality/$")
print(f"  System healthy: {'✓ Yes' if result['system_healthy'] else '⚠️  Issues detected'}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "="*80)
print("KEY TAKEAWAYS")
print("="*80)

print("""
✅ MULTI-AGENT EVALUATION DIMENSIONS:

1. COMMUNICATION
   - Message clarity and relevance
   - Conversation flow
   - Information exchange quality

2. COORDINATION
   - Task distribution
   - Dependency management
   - Load balancing

3. CONSENSUS
   - Time to agreement
   - Inclusivity
   - Decision quality

4. SYSTEM-LEVEL
   - Success rate
   - Latency
   - Cost efficiency
   - Fault tolerance

🎯 EVALUATION STRATEGIES:

✓ Evaluate at multiple levels (agent, interaction, system)
✓ Track emergent behaviors
✓ Monitor communication patterns
✓ Measure coordination efficiency
✓ Assess fault tolerance
✓ Compare to single-agent baseline

⚠️  COMMON CHALLENGES:

✗ Over-reliance on single agent
✗ Communication bottlenecks
✗ Coordination overhead
✗ Consensus deadlocks
✗ Cascading failures
✗ Unnecessary complexity

💡 REMEMBER:

"Multi-agent systems should provide clear benefits over single agents.
 Always measure overhead costs and emergent system properties."

🔍 DEBUG CHECKLIST:

When multi-agent system underperforms:
1. Check individual agent quality
2. Analyze communication patterns
3. Review task distribution
4. Monitor resource usage
5. Identify bottlenecks
6. Compare to single-agent baseline

Next: 14_prompt_optimization.py - Optimize prompts via evaluation!
""")

print("\n" + "="*80)
print("✨ Lesson 13 Complete!")
print("="*80)
print("\nNext: Run 14_prompt_optimization.py")
