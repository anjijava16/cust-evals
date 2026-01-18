"""
Lesson 18: Agent Systems Comprehensive Evaluation (Expert)

Complete evaluation framework for LLM agent systems including task success,
reasoning quality, tool usage, autonomy, robustness, and human-in-the-loop metrics.

Prerequisites: Lessons 1-17, especially Lesson 13
Difficulty: ⭐⭐⭐⭐ Expert
Time: 70 minutes
"""

print("="*80)
print("LESSON 18: Agent Systems Comprehensive Evaluation")
print("="*80)

print("""
🤖 AGENT EVALUATION FRAMEWORK

LLM Agents are autonomous systems that:
- Break down complex tasks
- Use tools and APIs
- Reason about actions
- Execute multi-step plans
- Recover from failures
- Interact with environments

Evaluation Dimensions:
1. Task Success Metrics
2. Reasoning & Planning Quality
3. Tool & Environment Interaction
4. Autonomy & Efficiency
5. Robustness & Reliability
6. Human-in-the-Loop Metrics

This lesson provides comprehensive metrics for each dimension.
""")

from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict
import time

# ============================================================================
# PART 1: TASK SUCCESS METRICS
# ============================================================================

print("\n" + "="*80)
print("PART 1: Task Success Metrics - Did the Agent Succeed?")
print("="*80)

print("""
✅ TASK SUCCESS METRICS:

Core metrics for agent evaluation:
1. Task Success Rate: % of tasks completed successfully
2. Goal Completion Rate: % of goals achieved
3. Subtask Completion Rate: Granular progress tracking
4. Plan Accuracy: How accurate was the initial plan?

These are the most important agent metrics!
""")

class TaskSuccessEvaluator:
    """Evaluate agent task success."""

    def evaluate_task_success(
        self,
        task: str,
        agent_output: Dict[str, Any],
        expected_outcome: Dict[str, Any],
        evaluation_criteria: List[str]
    ) -> Dict[str, Any]:
        """
        Evaluate if agent successfully completed a task.

        Args:
            task: Task description
            agent_output: Agent's result
            expected_outcome: Expected result
            evaluation_criteria: List of success criteria
        """
        # Check each criterion
        criteria_results = {}
        for criterion in evaluation_criteria:
            met = self._check_criterion(agent_output, expected_outcome, criterion)
            criteria_results[criterion] = met

        # Calculate success
        success_rate = sum(criteria_results.values()) / len(criteria_results) if criteria_results else 0.0
        fully_successful = all(criteria_results.values())

        return {
            'task_success_rate': success_rate,
            'fully_successful': fully_successful,
            'criteria_met': sum(criteria_results.values()),
            'total_criteria': len(criteria_results),
            'criteria_results': criteria_results
        }

    def evaluate_goal_completion(
        self,
        goals: List[Dict[str, Any]],
        agent_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate goal completion across multiple goals.

        Args:
            goals: List of {goal_id, description, success_criteria}
            agent_results: List of {goal_id, completed, result}
        """
        results_map = {r['goal_id']: r for r in agent_results}

        completed_goals = 0
        partially_completed = 0
        failed_goals = 0

        goal_details = []

        for goal in goals:
            goal_id = goal['goal_id']
            result = results_map.get(goal_id, {})

            if result.get('completed', False):
                # Check if meets success criteria
                criteria_met = self._verify_success_criteria(
                    result.get('result', {}),
                    goal.get('success_criteria', [])
                )

                if criteria_met >= 0.8:  # 80% threshold
                    completed_goals += 1
                    status = 'completed'
                else:
                    partially_completed += 1
                    status = 'partial'
            else:
                failed_goals += 1
                status = 'failed'

            goal_details.append({
                'goal_id': goal_id,
                'status': status,
                'criteria_met': criteria_met if result.get('completed') else 0.0
            })

        total_goals = len(goals)
        completion_rate = completed_goals / total_goals if total_goals > 0 else 0.0

        return {
            'goal_completion_rate': completion_rate,
            'completed_goals': completed_goals,
            'partially_completed_goals': partially_completed,
            'failed_goals': failed_goals,
            'total_goals': total_goals,
            'goal_details': goal_details
        }

    def evaluate_subtask_completion(
        self,
        planned_subtasks: List[Dict[str, Any]],
        executed_subtasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate subtask-level completion.

        Provides granular progress tracking.
        """
        total_subtasks = len(planned_subtasks)
        executed_ids = {s['subtask_id'] for s in executed_subtasks if s.get('completed', False)}

        completed_subtasks = len(executed_ids)
        completion_rate = completed_subtasks / total_subtasks if total_subtasks > 0 else 0.0

        # Track which subtasks were skipped
        planned_ids = {s['subtask_id'] for s in planned_subtasks}
        skipped_ids = planned_ids - executed_ids

        return {
            'subtask_completion_rate': completion_rate,
            'completed_subtasks': completed_subtasks,
            'total_planned_subtasks': total_subtasks,
            'skipped_subtasks': len(skipped_ids),
            'skipped_ids': list(skipped_ids)
        }

    def evaluate_plan_accuracy(
        self,
        initial_plan: List[str],
        actual_execution: List[str]
    ) -> Dict[str, Any]:
        """
        Evaluate how accurate the initial plan was.

        Measures planning quality vs execution reality.
        """
        # Calculate edit distance between plan and execution
        # Simplified: just compare steps
        plan_set = set(initial_plan)
        execution_set = set(actual_execution)

        correct_steps = len(plan_set & execution_set)
        extra_steps = len(execution_set - plan_set)
        missing_steps = len(plan_set - execution_set)

        accuracy = correct_steps / len(plan_set) if plan_set else 0.0

        # Check if order was preserved
        common_steps = [s for s in initial_plan if s in execution_set]
        order_preserved = self._check_order_preservation(common_steps, actual_execution)

        return {
            'plan_accuracy': accuracy,
            'correct_steps': correct_steps,
            'extra_steps': extra_steps,
            'missing_steps': missing_steps,
            'order_preserved': order_preserved,
            'deviation_rate': (extra_steps + missing_steps) / len(plan_set) if plan_set else 0.0
        }

    def _check_criterion(self, output: Dict, expected: Dict, criterion: str) -> bool:
        """Check if a success criterion is met."""
        if criterion == 'output_format':
            return output.get('format') == expected.get('format')
        elif criterion == 'contains_result':
            return 'result' in output
        elif criterion == 'no_errors':
            return output.get('errors', 0) == 0
        else:
            # Custom criterion check
            return output.get(criterion) == expected.get(criterion)

    def _verify_success_criteria(self, result: Dict, criteria: List[str]) -> float:
        """Verify what percentage of success criteria are met."""
        if not criteria:
            return 1.0

        met = sum(1 for c in criteria if result.get(c, False))
        return met / len(criteria)

    def _check_order_preservation(self, planned: List[str], executed: List[str]) -> bool:
        """Check if order of steps was preserved."""
        planned_indices = {step: i for i, step in enumerate(planned)}

        prev_idx = -1
        for step in executed:
            if step in planned_indices:
                curr_idx = planned_indices[step]
                if curr_idx < prev_idx:
                    return False  # Order violated
                prev_idx = curr_idx

        return True

# Demo
print("\n✅ Example: Task Success Evaluation")

task_evaluator = TaskSuccessEvaluator()

# Example 1: Single task evaluation
task = "Book a restaurant reservation for 2 people at 7pm"
agent_output = {
    'format': 'json',
    'result': {'restaurant': 'Italian Place', 'time': '7pm', 'party_size': 2, 'confirmed': True},
    'errors': 0
}
expected_outcome = {'format': 'json', 'confirmed': True}
criteria = ['output_format', 'contains_result', 'no_errors']

result = task_evaluator.evaluate_task_success(task, agent_output, expected_outcome, criteria)

print(f"Task: {task}")
print(f"Success Rate: {result['task_success_rate']:.1%}")
print(f"Criteria Met: {result['criteria_met']}/{result['total_criteria']}")
print(f"Fully Successful: {'✓ YES' if result['fully_successful'] else '✗ NO'}")

# Example 2: Goal completion across multiple goals
goals = [
    {'goal_id': 'G1', 'description': 'Research topic', 'success_criteria': ['sources_found', 'summary_created']},
    {'goal_id': 'G2', 'description': 'Write report', 'success_criteria': ['report_written', 'formatted']},
    {'goal_id': 'G3', 'description': 'Send email', 'success_criteria': ['email_sent']}
]

agent_results = [
    {'goal_id': 'G1', 'completed': True, 'result': {'sources_found': True, 'summary_created': True}},
    {'goal_id': 'G2', 'completed': True, 'result': {'report_written': True, 'formatted': False}},
    {'goal_id': 'G3', 'completed': False, 'result': {}}
]

goal_result = task_evaluator.evaluate_goal_completion(goals, agent_results)

print(f"\n\nGoal Completion:")
print(f"Completion Rate: {goal_result['goal_completion_rate']:.1%}")
print(f"Completed: {goal_result['completed_goals']}/{goal_result['total_goals']}")
print(f"Partially: {goal_result['partially_completed_goals']}")
print(f"Failed: {goal_result['failed_goals']}")

# ============================================================================
# PART 2: REASONING & PLANNING QUALITY
# ============================================================================

print("\n\n" + "="*80)
print("PART 2: Reasoning & Planning Quality")
print("="*80)

print("""
🧠 REASONING & PLANNING METRICS:

Evaluate agent's thinking process:
1. Reasoning Correctness: Is the reasoning sound?
2. Step Accuracy: Are individual steps correct?
3. Logical Consistency: No contradictions?
4. Tool Selection Accuracy: Right tools chosen?
""")

class ReasoningEvaluator:
    """Evaluate agent reasoning and planning quality."""

    def evaluate_reasoning_correctness(
        self,
        reasoning_trace: List[Dict[str, Any]],
        ground_truth_reasoning: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate correctness of reasoning steps.

        Args:
            reasoning_trace: Agent's reasoning steps
            ground_truth_reasoning: Expected reasoning
        """
        if not ground_truth_reasoning:
            # No ground truth - can only check for obvious errors
            return {'reasoning_correctness': 0.5, 'verified': False}

        correct_steps = 0
        total_steps = len(ground_truth_reasoning)

        # Match reasoning steps
        trace_map = {r['step_id']: r for r in reasoning_trace}

        for gt_step in ground_truth_reasoning:
            step_id = gt_step['step_id']
            if step_id in trace_map:
                agent_step = trace_map[step_id]
                if self._steps_match(agent_step, gt_step):
                    correct_steps += 1

        correctness = correct_steps / total_steps if total_steps > 0 else 0.0

        return {
            'reasoning_correctness': correctness,
            'correct_steps': correct_steps,
            'total_steps': total_steps,
            'verified': True
        }

    def evaluate_step_accuracy(
        self,
        execution_steps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate accuracy of each execution step.

        Checks if steps succeeded and produced expected outputs.
        """
        total_steps = len(execution_steps)
        successful_steps = 0
        failed_steps = 0
        step_details = []

        for step in execution_steps:
            step_success = step.get('success', False)
            expected_output = step.get('expected_output')
            actual_output = step.get('actual_output')

            if step_success:
                if expected_output is not None:
                    # Verify output matches expectation
                    output_matches = self._outputs_match(actual_output, expected_output)
                    if output_matches:
                        successful_steps += 1
                        accuracy = 1.0
                    else:
                        accuracy = 0.5  # Completed but wrong output
                else:
                    successful_steps += 1
                    accuracy = 1.0
            else:
                failed_steps += 1
                accuracy = 0.0

            step_details.append({
                'step_id': step.get('step_id'),
                'accuracy': accuracy,
                'success': step_success
            })

        overall_accuracy = successful_steps / total_steps if total_steps > 0 else 0.0

        return {
            'step_accuracy': overall_accuracy,
            'successful_steps': successful_steps,
            'failed_steps': failed_steps,
            'total_steps': total_steps,
            'step_details': step_details
        }

    def evaluate_logical_consistency(
        self,
        reasoning_trace: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Check for logical contradictions in reasoning.
        """
        contradictions = []

        # Check for contradictory statements
        for i, step1 in enumerate(reasoning_trace):
            for step2 in reasoning_trace[i+1:]:
                if self._check_contradiction(step1, step2):
                    contradictions.append({
                        'step1': step1['step_id'],
                        'step2': step2['step_id'],
                        'reason': 'contradictory statements'
                    })

        consistency_score = 1.0 - min(1.0, len(contradictions) * 0.2)

        return {
            'logical_consistency': consistency_score,
            'contradictions_found': len(contradictions),
            'is_consistent': len(contradictions) == 0,
            'contradictions': contradictions[:5]  # Show first 5
        }

    def evaluate_tool_selection_accuracy(
        self,
        planned_tools: List[str],
        available_tools: List[str],
        task_requirements: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Evaluate if agent selected appropriate tools.

        Args:
            planned_tools: Tools agent plans to use
            available_tools: All available tools
            task_requirements: Required capabilities for task
        """
        # Check if selected tools are available
        valid_tools = [t for t in planned_tools if t in available_tools]
        invalid_tools = [t for t in planned_tools if t not in available_tools]

        # Check if selected tools cover requirements
        tool_capabilities = self._get_tool_capabilities(valid_tools)
        required_capabilities = set()
        for caps in task_requirements.values():
            required_capabilities.update(caps)

        covered_capabilities = tool_capabilities & required_capabilities
        missing_capabilities = required_capabilities - tool_capabilities

        coverage = len(covered_capabilities) / len(required_capabilities) if required_capabilities else 1.0

        return {
            'tool_selection_accuracy': coverage,
            'valid_tools': len(valid_tools),
            'invalid_tools': len(invalid_tools),
            'capability_coverage': coverage,
            'missing_capabilities': list(missing_capabilities),
            'all_requirements_met': len(missing_capabilities) == 0
        }

    def _steps_match(self, step1: Dict, step2: Dict) -> bool:
        """Check if two reasoning steps match."""
        # Simplified comparison
        return step1.get('action') == step2.get('action')

    def _outputs_match(self, actual: Any, expected: Any) -> bool:
        """Check if outputs match."""
        return str(actual).lower() == str(expected).lower()

    def _check_contradiction(self, step1: Dict, step2: Dict) -> bool:
        """Check if two steps contradict each other."""
        # Simplified contradiction detection
        text1 = str(step1.get('reasoning', '')).lower()
        text2 = str(step2.get('reasoning', '')).lower()

        # Check for negation patterns
        if ('not' in text1 and 'is' in text2) or ('not' in text2 and 'is' in text1):
            # Check for shared concepts
            words1 = set(text1.split())
            words2 = set(text2.split())
            if len(words1 & words2) > 3:
                return True

        return False

    def _get_tool_capabilities(self, tools: List[str]) -> Set[str]:
        """Get capabilities provided by tools (simplified)."""
        # Mock tool capabilities
        tool_caps = {
            'web_search': {'search', 'information_retrieval'},
            'calculator': {'math', 'computation'},
            'file_reader': {'read', 'file_access'},
            'email_sender': {'send', 'communication'},
            'database': {'query', 'data_access'}
        }

        capabilities = set()
        for tool in tools:
            capabilities.update(tool_caps.get(tool, set()))

        return capabilities

# Demo
print("\n🧠 Example: Reasoning Quality Evaluation")

reasoning_eval = ReasoningEvaluator()

execution_steps = [
    {'step_id': 'S1', 'success': True, 'expected_output': 'data', 'actual_output': 'data'},
    {'step_id': 'S2', 'success': True, 'expected_output': 'processed', 'actual_output': 'processed'},
    {'step_id': 'S3', 'success': False, 'expected_output': 'result', 'actual_output': None}
]

step_result = reasoning_eval.evaluate_step_accuracy(execution_steps)

print(f"Step Accuracy: {step_result['step_accuracy']:.1%}")
print(f"Successful: {step_result['successful_steps']}/{step_result['total_steps']}")
print(f"Failed: {step_result['failed_steps']}")

# Tool selection example
planned_tools = ['web_search', 'calculator', 'nonexistent_tool']
available_tools = ['web_search', 'calculator', 'database', 'file_reader']
task_requirements = {'research': ['search', 'information_retrieval'], 'analysis': ['math']}

tool_result = reasoning_eval.evaluate_tool_selection_accuracy(
    planned_tools, available_tools, task_requirements
)

print(f"\nTool Selection Accuracy: {tool_result['tool_selection_accuracy']:.1%}")
print(f"Valid tools: {tool_result['valid_tools']}")
print(f"Invalid tools: {tool_result['invalid_tools']}")
print(f"All requirements met: {'✓ YES' if tool_result['all_requirements_met'] else '✗ NO'}")

# ============================================================================
# PART 3: TOOL & ENVIRONMENT INTERACTION
# ============================================================================

print("\n\n" + "="*80)
print("PART 3: Tool & Environment Interaction")
print("="*80)

print("""
🔧 TOOL USAGE METRICS:

Evaluate how agent uses tools and interacts with environment:
1. Tool Invocation Precision/Recall: Right tools called?
2. API Call Success Rate: Calls succeed?
3. Error Recovery Rate: Can agent recover?
4. Environment Constraint Violations: Rules followed?
""")

class ToolInteractionEvaluator:
    """Evaluate agent's tool and environment interaction."""

    def evaluate_tool_invocation(
        self,
        expected_tool_calls: List[Dict[str, Any]],
        actual_tool_calls: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate tool invocation precision and recall.

        Args:
            expected_tool_calls: Tools that should have been called
            actual_tool_calls: Tools that were actually called
        """
        expected_set = {(call['tool'], call.get('purpose', '')) for call in expected_tool_calls}
        actual_set = {(call['tool'], call.get('purpose', '')) for call in actual_tool_calls}

        true_positives = len(expected_set & actual_set)
        false_positives = len(actual_set - expected_set)
        false_negatives = len(expected_set - actual_set)

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {
            'tool_invocation_precision': precision,
            'tool_invocation_recall': recall,
            'tool_invocation_f1': f1,
            'correct_calls': true_positives,
            'unnecessary_calls': false_positives,
            'missed_calls': false_negatives
        }

    def evaluate_api_call_success(
        self,
        api_calls: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate success rate of API/tool calls.
        """
        total_calls = len(api_calls)
        successful_calls = sum(1 for call in api_calls if call.get('success', False))
        failed_calls = total_calls - successful_calls

        # Categorize failures
        failure_reasons = defaultdict(int)
        for call in api_calls:
            if not call.get('success', False):
                reason = call.get('failure_reason', 'unknown')
                failure_reasons[reason] += 1

        success_rate = successful_calls / total_calls if total_calls > 0 else 0.0

        return {
            'api_call_success_rate': success_rate,
            'successful_calls': successful_calls,
            'failed_calls': failed_calls,
            'total_calls': total_calls,
            'failure_reasons': dict(failure_reasons)
        }

    def evaluate_error_recovery(
        self,
        error_events: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate agent's ability to recover from errors.

        Args:
            error_events: List of {error_type, recovered, recovery_steps}
        """
        total_errors = len(error_events)
        recovered_errors = sum(1 for event in error_events if event.get('recovered', False))

        recovery_rate = recovered_errors / total_errors if total_errors > 0 else 0.0

        # Average recovery steps
        recovery_steps = [event.get('recovery_steps', 0) for event in error_events if event.get('recovered', False)]
        avg_recovery_steps = sum(recovery_steps) / len(recovery_steps) if recovery_steps else 0

        return {
            'error_recovery_rate': recovery_rate,
            'recovered_errors': recovered_errors,
            'unrecovered_errors': total_errors - recovered_errors,
            'total_errors': total_errors,
            'avg_recovery_steps': avg_recovery_steps,
            'resilient': recovery_rate >= 0.7
        }

    def evaluate_constraint_violations(
        self,
        agent_actions: List[Dict[str, Any]],
        environment_constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate if agent violated environment constraints.

        Args:
            agent_actions: Actions taken by agent
            environment_constraints: Rules/constraints to follow
        """
        violations = []

        for action in agent_actions:
            # Check each constraint
            for constraint_name, constraint_rule in environment_constraints.items():
                if self._violates_constraint(action, constraint_rule):
                    violations.append({
                        'action': action.get('action_id'),
                        'constraint': constraint_name,
                        'details': action.get('details')
                    })

        total_actions = len(agent_actions)
        violation_count = len(violations)
        compliance_rate = 1.0 - (violation_count / total_actions) if total_actions > 0 else 1.0

        return {
            'compliance_rate': compliance_rate,
            'violations': violation_count,
            'total_actions': total_actions,
            'is_compliant': violation_count == 0,
            'violation_details': violations[:5]  # Show first 5
        }

    def _violates_constraint(self, action: Dict, constraint: Any) -> bool:
        """Check if action violates constraint (simplified)."""
        # Simplified constraint checking
        if isinstance(constraint, dict):
            constraint_type = constraint.get('type')

            if constraint_type == 'max_calls':
                return action.get('call_count', 0) > constraint.get('limit', float('inf'))
            elif constraint_type == 'allowed_tools':
                tool = action.get('tool')
                return tool not in constraint.get('tools', [])

        return False

# Demo
print("\n🔧 Example: Tool & Environment Interaction")

tool_eval = ToolInteractionEvaluator()

# API call success rate
api_calls = [
    {'api': 'weather', 'success': True},
    {'api': 'database', 'success': True},
    {'api': 'search', 'success': False, 'failure_reason': 'timeout'},
    {'api': 'email', 'success': False, 'failure_reason': 'auth_error'},
    {'api': 'calculator', 'success': True}
]

api_result = tool_eval.evaluate_api_call_success(api_calls)

print(f"API Call Success Rate: {api_result['api_call_success_rate']:.1%}")
print(f"Successful: {api_result['successful_calls']}/{api_result['total_calls']}")
print(f"Failed: {api_result['failed_calls']}")
print(f"Failure reasons: {api_result['failure_reasons']}")

# Error recovery
error_events = [
    {'error_type': 'api_timeout', 'recovered': True, 'recovery_steps': 2},
    {'error_type': 'invalid_input', 'recovered': True, 'recovery_steps': 1},
    {'error_type': 'system_error', 'recovered': False, 'recovery_steps': 0}
]

recovery_result = tool_eval.evaluate_error_recovery(error_events)

print(f"\nError Recovery Rate: {recovery_result['error_recovery_rate']:.1%}")
print(f"Recovered: {recovery_result['recovered_errors']}/{recovery_result['total_errors']}")
print(f"Avg recovery steps: {recovery_result['avg_recovery_steps']:.1f}")
print(f"Resilient: {'✓ YES' if recovery_result['resilient'] else '✗ NO'}")

# ============================================================================
# PART 4: AUTONOMY & EFFICIENCY
# ============================================================================

print("\n\n" + "="*80)
print("PART 4: Autonomy & Efficiency")
print("="*80)

print("""
⚡ EFFICIENCY METRICS:

Measure agent efficiency and autonomy:
1. Steps to Completion: How many steps taken?
2. Time to Completion: How long did it take?
3. Cost per Task: Token/API costs
4. Redundant Action Rate: Wasted effort

Lower is better for all these metrics!
""")

class EfficiencyEvaluator:
    """Evaluate agent autonomy and efficiency."""

    def evaluate_steps_to_completion(
        self,
        actual_steps: int,
        optimal_steps: int,
        task_complexity: str = 'medium'
    ) -> Dict[str, Any]:
        """
        Evaluate if agent took reasonable number of steps.

        Args:
            actual_steps: Steps agent actually took
            optimal_steps: Minimum steps needed
            task_complexity: Task difficulty level
        """
        # Allow some overhead based on complexity
        complexity_factors = {'low': 1.2, 'medium': 1.5, 'high': 2.0}
        max_reasonable = optimal_steps * complexity_factors.get(task_complexity, 1.5)

        efficiency = optimal_steps / actual_steps if actual_steps > 0 else 0.0
        overhead = ((actual_steps - optimal_steps) / optimal_steps * 100) if optimal_steps > 0 else 0

        return {
            'step_efficiency': efficiency,
            'actual_steps': actual_steps,
            'optimal_steps': optimal_steps,
            'overhead_percentage': overhead,
            'within_reasonable_range': actual_steps <= max_reasonable,
            'excessive_steps': actual_steps > max_reasonable
        }

    def evaluate_time_to_completion(
        self,
        start_time: float,
        end_time: float,
        expected_duration: float
    ) -> Dict[str, Any]:
        """
        Evaluate task completion time.

        Args:
            start_time: Task start timestamp
            end_time: Task end timestamp
            expected_duration: Expected time in seconds
        """
        actual_duration = end_time - start_time
        time_efficiency = expected_duration / actual_duration if actual_duration > 0 else 0.0

        return {
            'time_efficiency': time_efficiency,
            'actual_duration_seconds': actual_duration,
            'expected_duration_seconds': expected_duration,
            'time_overhead': actual_duration - expected_duration,
            'within_expected': actual_duration <= expected_duration * 1.5
        }

    def evaluate_cost_per_task(
        self,
        token_usage: Dict[str, int],
        api_calls: List[Dict[str, Any]],
        pricing: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calculate and evaluate cost efficiency.

        Args:
            token_usage: {input_tokens, output_tokens}
            api_calls: List of API calls with costs
            pricing: Cost per unit for various resources
        """
        # Token costs
        input_tokens = token_usage.get('input_tokens', 0)
        output_tokens = token_usage.get('output_tokens', 0)

        token_cost = (
            input_tokens * pricing.get('input_token_per_1k', 0.0) / 1000 +
            output_tokens * pricing.get('output_token_per_1k', 0.0) / 1000
        )

        # API call costs
        api_cost = sum(call.get('cost', 0.0) for call in api_calls)

        total_cost = token_cost + api_cost

        return {
            'total_cost': total_cost,
            'token_cost': token_cost,
            'api_cost': api_cost,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens,
            'cost_breakdown': {
                'tokens': token_cost,
                'apis': api_cost
            }
        }

    def evaluate_redundant_actions(
        self,
        action_sequence: List[str]
    ) -> Dict[str, Any]:
        """
        Detect redundant or repeated actions.
        """
        total_actions = len(action_sequence)

        # Find repeated consecutive actions
        consecutive_repeats = 0
        for i in range(1, len(action_sequence)):
            if action_sequence[i] == action_sequence[i-1]:
                consecutive_repeats += 1

        # Find any duplicated actions
        unique_actions = len(set(action_sequence))
        total_duplicates = total_actions - unique_actions

        redundancy_rate = (consecutive_repeats + total_duplicates) / (total_actions * 2) if total_actions > 0 else 0.0

        return {
            'redundant_action_rate': redundancy_rate,
            'consecutive_repeats': consecutive_repeats,
            'total_duplicates': total_duplicates,
            'unique_actions': unique_actions,
            'total_actions': total_actions,
            'is_efficient': redundancy_rate < 0.2
        }

# Demo
print("\n⚡ Example: Efficiency Evaluation")

efficiency_eval = EfficiencyEvaluator()

# Steps to completion
step_result = efficiency_eval.evaluate_steps_to_completion(
    actual_steps=12,
    optimal_steps=8,
    task_complexity='medium'
)

print(f"Step Efficiency: {step_result['step_efficiency']:.1%}")
print(f"Steps: {step_result['actual_steps']} (optimal: {step_result['optimal_steps']})")
print(f"Overhead: {step_result['overhead_percentage']:.1f}%")
print(f"Reasonable: {'✓ YES' if step_result['within_reasonable_range'] else '✗ NO'}")

# Cost evaluation
token_usage = {'input_tokens': 1500, 'output_tokens': 800}
api_calls = [{'api': 'search', 'cost': 0.01}, {'api': 'db', 'cost': 0.005}]
pricing = {'input_token_per_1k': 0.01, 'output_token_per_1k': 0.03}

cost_result = efficiency_eval.evaluate_cost_per_task(token_usage, api_calls, pricing)

print(f"\nTotal Cost: ${cost_result['total_cost']:.4f}")
print(f"  Token cost: ${cost_result['token_cost']:.4f}")
print(f"  API cost: ${cost_result['api_cost']:.4f}")
print(f"Total tokens: {cost_result['total_tokens']}")

# ============================================================================
# PART 5: ROBUSTNESS & RELIABILITY
# ============================================================================

print("\n\n" + "="*80)
print("PART 5: Robustness & Reliability")
print("="*80)

print("""
🛡️ ROBUSTNESS METRICS:

1. Failure Rate: How often does agent fail?
2. Recovery Time: How long to recover?
3. Sensitivity to Prompt Variations: Stable outputs?
4. Long-Horizon Stability: Performance over long tasks?
""")

class RobustnessEvaluator:
    """Evaluate agent robustness and reliability."""

    def evaluate_failure_rate(
        self,
        task_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate failure rate across tasks."""
        total_tasks = len(task_results)
        failed_tasks = sum(1 for result in task_results if not result.get('success', False))

        failure_rate = failed_tasks / total_tasks if total_tasks > 0 else 0.0

        # Categorize failures
        failure_types = defaultdict(int)
        for result in task_results:
            if not result.get('success', False):
                failure_type = result.get('failure_type', 'unknown')
                failure_types[failure_type] += 1

        return {
            'failure_rate': failure_rate,
            'failed_tasks': failed_tasks,
            'successful_tasks': total_tasks - failed_tasks,
            'total_tasks': total_tasks,
            'reliability': 1.0 - failure_rate,
            'failure_types': dict(failure_types)
        }

    def evaluate_recovery_time(
        self,
        failure_events: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate time to recover from failures.

        Args:
            failure_events: List of {failure_time, recovery_time, recovered}
        """
        recovery_times = []

        for event in failure_events:
            if event.get('recovered', False):
                recovery_time = event['recovery_time'] - event['failure_time']
                recovery_times.append(recovery_time)

        if recovery_times:
            avg_recovery = sum(recovery_times) / len(recovery_times)
            max_recovery = max(recovery_times)
            min_recovery = min(recovery_times)
        else:
            avg_recovery = max_recovery = min_recovery = 0.0

        return {
            'avg_recovery_time_seconds': avg_recovery,
            'max_recovery_time': max_recovery,
            'min_recovery_time': min_recovery,
            'total_recoveries': len(recovery_times),
            'fast_recovery': avg_recovery < 30.0  # Under 30 seconds
        }

    def evaluate_prompt_sensitivity(
        self,
        base_prompt: str,
        prompt_variations: List[str],
        results_for_each: List[Any]
    ) -> Dict[str, Any]:
        """
        Evaluate sensitivity to prompt variations.

        Robust agents should give similar results for similar prompts.
        """
        base_result = results_for_each[0] if results_for_each else None

        consistent_results = 0
        for result in results_for_each[1:]:
            if self._results_similar(base_result, result):
                consistent_results += 1

        total_variations = len(prompt_variations)
        consistency = consistent_results / (total_variations - 1) if total_variations > 1 else 1.0

        return {
            'prompt_consistency': consistency,
            'consistent_variations': consistent_results,
            'total_variations': total_variations - 1,
            'is_robust': consistency >= 0.8
        }

    def evaluate_long_horizon_stability(
        self,
        performance_over_steps: List[float]
    ) -> Dict[str, Any]:
        """
        Evaluate if performance degrades over long tasks.

        Args:
            performance_over_steps: Performance score at each step
        """
        if len(performance_over_steps) < 2:
            return {'stability': 1.0, 'degradation': 0.0}

        # Calculate trend
        initial_performance = sum(performance_over_steps[:3]) / min(3, len(performance_over_steps))
        final_performance = sum(performance_over_steps[-3:]) / min(3, len(performance_over_steps))

        degradation = (initial_performance - final_performance) / initial_performance if initial_performance > 0 else 0.0

        # Calculate variance
        mean_performance = sum(performance_over_steps) / len(performance_over_steps)
        variance = sum((p - mean_performance) ** 2 for p in performance_over_steps) / len(performance_over_steps)

        stability = 1.0 - min(1.0, abs(degradation) + variance)

        return {
            'long_horizon_stability': stability,
            'initial_performance': initial_performance,
            'final_performance': final_performance,
            'degradation': degradation,
            'variance': variance,
            'is_stable': abs(degradation) < 0.2
        }

    def _results_similar(self, result1: Any, result2: Any) -> bool:
        """Check if two results are similar."""
        # Simplified similarity check
        return str(result1).lower() == str(result2).lower()

# Demo
print("\n🛡️ Example: Robustness Evaluation")

robustness_eval = RobustnessEvaluator()

# Failure rate
task_results = [
    {'success': True},
    {'success': True},
    {'success': False, 'failure_type': 'timeout'},
    {'success': True},
    {'success': False, 'failure_type': 'error'},
    {'success': True}
]

failure_result = robustness_eval.evaluate_failure_rate(task_results)

print(f"Failure Rate: {failure_result['failure_rate']:.1%}")
print(f"Reliability: {failure_result['reliability']:.1%}")
print(f"Failed: {failure_result['failed_tasks']}/{failure_result['total_tasks']}")

# Long-horizon stability
performance_over_steps = [0.9, 0.85, 0.88, 0.82, 0.80, 0.78, 0.75, 0.72]

stability_result = robustness_eval.evaluate_long_horizon_stability(performance_over_steps)

print(f"\nLong-Horizon Stability: {stability_result['long_horizon_stability']:.1%}")
print(f"Initial performance: {stability_result['initial_performance']:.2f}")
print(f"Final performance: {stability_result['final_performance']:.2f}")
print(f"Degradation: {stability_result['degradation']:.1%}")
print(f"Stable: {'✓ YES' if stability_result['is_stable'] else '⚠️  NO'}")

# ============================================================================
# PART 6: HUMAN-IN-THE-LOOP METRICS
# ============================================================================

print("\n\n" + "="*80)
print("PART 6: Human-in-the-Loop Metrics")
print("="*80)

print("""
👤 HUMAN-IN-THE-LOOP METRICS:

When humans supervise agents:
1. Human Intervention Rate: How often is human needed?
2. Override Frequency: How often are agent decisions overridden?
3. User Satisfaction: Are users happy with agent?

Goal: Minimize intervention while maximizing satisfaction.
""")

class HumanLoopEvaluator:
    """Evaluate human-in-the-loop metrics."""

    def evaluate_intervention_rate(
        self,
        total_actions: int,
        human_interventions: int,
        intervention_details: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate how often human intervention was needed.

        Args:
            total_actions: Total actions agent could take
            human_interventions: Number of times human intervened
            intervention_details: Details about each intervention
        """
        intervention_rate = human_interventions / total_actions if total_actions > 0 else 0.0
        autonomy = 1.0 - intervention_rate

        # Categorize interventions
        intervention_reasons = defaultdict(int)
        for intervention in intervention_details:
            reason = intervention.get('reason', 'unknown')
            intervention_reasons[reason] += 1

        return {
            'human_intervention_rate': intervention_rate,
            'autonomy_rate': autonomy,
            'total_interventions': human_interventions,
            'total_actions': total_actions,
            'intervention_reasons': dict(intervention_reasons),
            'highly_autonomous': intervention_rate < 0.1
        }

    def evaluate_override_frequency(
        self,
        agent_decisions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate how often agent decisions are overridden.

        Args:
            agent_decisions: List of {decision, overridden, override_reason}
        """
        total_decisions = len(agent_decisions)
        overridden_decisions = sum(1 for d in agent_decisions if d.get('overridden', False))

        override_rate = overridden_decisions / total_decisions if total_decisions > 0 else 0.0
        decision_quality = 1.0 - override_rate

        # Categorize overrides
        override_reasons = defaultdict(int)
        for decision in agent_decisions:
            if decision.get('overridden', False):
                reason = decision.get('override_reason', 'unknown')
                override_reasons[reason] += 1

        return {
            'override_frequency': override_rate,
            'decision_quality': decision_quality,
            'overridden_decisions': overridden_decisions,
            'accepted_decisions': total_decisions - overridden_decisions,
            'total_decisions': total_decisions,
            'override_reasons': dict(override_reasons),
            'trustworthy': override_rate < 0.15
        }

    def evaluate_user_satisfaction(
        self,
        satisfaction_scores: List[int],
        feedback_comments: List[str]
    ) -> Dict[str, Any]:
        """
        Evaluate user satisfaction with agent.

        Args:
            satisfaction_scores: List of scores (1-5 scale)
            feedback_comments: User feedback text
        """
        if not satisfaction_scores:
            return {'avg_satisfaction': 0.0, 'total_responses': 0}

        avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores)

        # Categorize satisfaction levels
        very_satisfied = sum(1 for s in satisfaction_scores if s >= 4)
        neutral = sum(1 for s in satisfaction_scores if s == 3)
        dissatisfied = sum(1 for s in satisfaction_scores if s <= 2)

        # Analyze sentiment in comments (simplified)
        positive_comments = sum(1 for c in feedback_comments if self._is_positive(c))
        negative_comments = sum(1 for c in feedback_comments if self._is_negative(c))

        return {
            'avg_satisfaction_score': avg_satisfaction,
            'satisfaction_out_of_5': avg_satisfaction,
            'very_satisfied': very_satisfied,
            'neutral': neutral,
            'dissatisfied': dissatisfied,
            'total_responses': len(satisfaction_scores),
            'positive_feedback': positive_comments,
            'negative_feedback': negative_comments,
            'highly_rated': avg_satisfaction >= 4.0
        }

    def _is_positive(self, comment: str) -> bool:
        """Check if comment is positive (simplified)."""
        positive_words = ['good', 'great', 'excellent', 'helpful', 'amazing', 'love', 'perfect']
        return any(word in comment.lower() for word in positive_words)

    def _is_negative(self, comment: str) -> bool:
        """Check if comment is negative (simplified)."""
        negative_words = ['bad', 'poor', 'terrible', 'useless', 'hate', 'awful', 'worst']
        return any(word in comment.lower() for word in negative_words)

# Demo
print("\n👤 Example: Human-in-the-Loop Evaluation")

human_loop_eval = HumanLoopEvaluator()

# Intervention rate
intervention_details = [
    {'reason': 'uncertain_decision'},
    {'reason': 'safety_concern'},
    {'reason': 'verification_needed'}
]

intervention_result = human_loop_eval.evaluate_intervention_rate(
    total_actions=50,
    human_interventions=3,
    intervention_details=intervention_details
)

print(f"Human Intervention Rate: {intervention_result['human_intervention_rate']:.1%}")
print(f"Autonomy Rate: {intervention_result['autonomy_rate']:.1%}")
print(f"Interventions: {intervention_result['total_interventions']}/{intervention_result['total_actions']}")
print(f"Highly Autonomous: {'✓ YES' if intervention_result['highly_autonomous'] else '✗ NO'}")

# User satisfaction
satisfaction_scores = [5, 4, 5, 4, 3, 5, 4, 5]
feedback_comments = [
    'Great job!',
    'Very helpful agent',
    'Could be better',
    'Excellent performance'
]

satisfaction_result = human_loop_eval.evaluate_user_satisfaction(
    satisfaction_scores, feedback_comments
)

print(f"\nUser Satisfaction: {satisfaction_result['avg_satisfaction_score']:.1f}/5.0")
print(f"Very Satisfied: {satisfaction_result['very_satisfied']}/{satisfaction_result['total_responses']}")
print(f"Positive Feedback: {satisfaction_result['positive_feedback']}/{len(feedback_comments)}")
print(f"Highly Rated: {'✓ YES' if satisfaction_result['highly_rated'] else '✗ NO'}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "="*80)
print("KEY TAKEAWAYS")
print("="*80)

print("""
✅ COMPREHENSIVE AGENT EVALUATION:

1. TASK SUCCESS (Most Important)
   ✓ Task Success Rate: > 85%
   ✓ Goal Completion: > 90%
   ✓ Subtask Tracking: Granular monitoring
   ✓ Plan Accuracy: > 70%

2. REASONING & PLANNING
   ✓ Reasoning Correctness: > 80%
   ✓ Step Accuracy: > 90%
   ✓ Logical Consistency: No contradictions
   ✓ Tool Selection: > 85% appropriate

3. TOOL INTERACTION
   ✓ Tool Invocation F1: > 0.8
   ✓ API Success Rate: > 95%
   ✓ Error Recovery: > 70%
   ✓ Compliance: 100% (no violations)

4. EFFICIENCY
   ✓ Step Overhead: < 50%
   ✓ Time Efficiency: < 2x expected
   ✓ Cost per Task: Track and optimize
   ✓ Redundancy: < 20%

5. ROBUSTNESS
   ✓ Failure Rate: < 10%
   ✓ Recovery Time: < 30 seconds
   ✓ Prompt Stability: > 80%
   ✓ Long-horizon: Minimal degradation

6. HUMAN-IN-THE-LOOP
   ✓ Intervention Rate: < 10%
   ✓ Override Frequency: < 15%
   ✓ User Satisfaction: > 4.0/5.0

📊 AGENT EVALUATION DASHBOARD:

┌──────────────────────────────────────────┐
│ SUCCESS:   Task Success, Goal Complete   │
│ QUALITY:   Reasoning, Step Accuracy      │
│ TOOLS:     API Success, Error Recovery   │
│ EFFICIENCY: Steps, Time, Cost            │
│ RELIABILITY: Failure Rate, Stability     │
│ UX:        Interventions, Satisfaction   │
└──────────────────────────────────────────┘

🎯 TESTING STRATEGY:

Phase 1: Unit Testing
- Test individual capabilities
- Tool usage correctness
- Reasoning on simple tasks

Phase 2: Integration Testing
- Multi-step task execution
- Tool chains
- Error recovery

Phase 3: End-to-End Testing
- Full tasks with real tools
- Long-horizon scenarios
- Edge cases

Phase 4: Production Monitoring
- Continuous metrics tracking
- Failure alerts
- User feedback

⚠️  AGENT-SPECIFIC CHALLENGES:

1. Non-determinism:
   - Agents can take different paths
   - Solution: Measure outcome, not path

2. Long Tasks:
   - Hard to define success for complex tasks
   - Solution: Break into subtasks

3. Tool Dependencies:
   - External API failures
   - Solution: Mock tools for testing

4. Context Window:
   - Long tasks exceed context
   - Solution: Test context management

💡 BEST PRACTICES:

1. Start with Task Success:
   - Most important metric
   - Everything else is secondary

2. Monitor Tool Usage:
   - Critical failure point
   - Track API success rates

3. Test Edge Cases:
   - Ambiguous instructions
   - Tool failures
   - Long task sequences

4. Human Baselines:
   - Compare to human performance
   - Set realistic targets

5. Continuous Improvement:
   - A/B test changes
   - Track regressions
   - User feedback loops

🔬 RESEARCH FRONTIERS:

- Better long-horizon evaluation
- Tool selection optimization
- Multi-agent coordination
- Safety guarantees
- Interpretable reasoning

Next: 19_task_specific_metrics.py - Task-specific evaluation!
""")

print("\n" + "="*80)
print("✨ Lesson 18 Complete!")
print("="*80)
print("\nNext: Run 19_task_specific_metrics.py")
