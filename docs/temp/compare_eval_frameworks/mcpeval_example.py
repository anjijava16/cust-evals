"""
MCPEval (Model Context Protocol Evaluation) Example

MCPEval evaluates models that use the Model Context Protocol (MCP) for tool/context integration.
Focuses on evaluating function calling, tool use, and context utilization.

Installation:
pip install mcp anthropic openai

Documentation: https://modelcontextprotocol.io/
"""

import os
import json
from typing import List, Dict, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class ToolCallStatus(Enum):
    """Status of tool call execution."""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    NOT_CALLED = "not_called"


@dataclass
class Tool:
    """MCP Tool definition."""
    name: str
    description: str
    parameters: Dict[str, Any]

    def to_dict(self):
        return asdict(self)


@dataclass
class ToolCall:
    """Tool call made by the model."""
    tool_name: str
    arguments: Dict[str, Any]
    result: Any = None
    status: ToolCallStatus = ToolCallStatus.SUCCESS


@dataclass
class MCPEvalResult:
    """Evaluation result for MCP interaction."""
    task: str
    expected_tools: List[str]
    actual_tools: List[str]
    tool_calls: List[ToolCall]
    score: float
    passed: bool
    details: Dict[str, Any]


class MCPEvaluator:
    """Evaluator for Model Context Protocol interactions."""

    def __init__(self, tools: List[Tool]):
        self.tools = {tool.name: tool for tool in tools}
        self.results = []

    def evaluate_tool_selection(
        self,
        task: str,
        expected_tools: List[str],
        actual_tool_calls: List[ToolCall]
    ) -> MCPEvalResult:
        """
        Evaluate if model selected correct tools.
        Checks tool selection accuracy.
        """
        actual_tools = [tc.tool_name for tc in actual_tool_calls]

        # Calculate metrics
        expected_set = set(expected_tools)
        actual_set = set(actual_tools)

        correct = len(expected_set & actual_set)
        total_expected = len(expected_set)
        total_actual = len(actual_set)

        precision = correct / total_actual if total_actual > 0 else 0
        recall = correct / total_expected if total_expected > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        passed = f1 >= 0.8

        result = MCPEvalResult(
            task=task,
            expected_tools=expected_tools,
            actual_tools=actual_tools,
            tool_calls=actual_tool_calls,
            score=f1,
            passed=passed,
            details={
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "missing_tools": list(expected_set - actual_set),
                "unexpected_tools": list(actual_set - expected_set)
            }
        )

        return result

    def evaluate_tool_arguments(
        self,
        tool_call: ToolCall,
        expected_arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate if tool arguments are correct.
        Checks argument accuracy and completeness.
        """
        actual_args = tool_call.arguments

        # Check required arguments
        missing_args = []
        incorrect_args = []
        correct_args = []

        for key, expected_value in expected_arguments.items():
            if key not in actual_args:
                missing_args.append(key)
            elif actual_args[key] != expected_value:
                incorrect_args.append({
                    "arg": key,
                    "expected": expected_value,
                    "actual": actual_args[key]
                })
            else:
                correct_args.append(key)

        # Calculate score
        total_args = len(expected_arguments)
        correct_count = len(correct_args)
        score = correct_count / total_args if total_args > 0 else 0

        return {
            "score": score,
            "passed": score >= 0.8,
            "correct_args": correct_args,
            "missing_args": missing_args,
            "incorrect_args": incorrect_args
        }

    def evaluate_tool_sequence(
        self,
        tool_calls: List[ToolCall],
        expected_sequence: List[str]
    ) -> Dict[str, Any]:
        """
        Evaluate if tools were called in correct order.
        Checks sequence adherence for multi-step tasks.
        """
        actual_sequence = [tc.tool_name for tc in tool_calls]

        # Check sequence match
        matches = []
        for i, (expected, actual) in enumerate(zip(expected_sequence, actual_sequence)):
            matches.append(expected == actual)

        # Calculate sequence score
        if len(actual_sequence) == len(expected_sequence):
            score = sum(matches) / len(matches) if matches else 0
        else:
            # Penalize length mismatch
            max_len = max(len(expected_sequence), len(actual_sequence))
            score = sum(matches) / max_len if max_len > 0 else 0

        return {
            "score": score,
            "passed": score >= 0.8,
            "expected_sequence": expected_sequence,
            "actual_sequence": actual_sequence,
            "length_match": len(actual_sequence) == len(expected_sequence)
        }


def define_example_tools() -> List[Tool]:
    """Define example MCP tools for evaluation."""
    tools = [
        Tool(
            name="search_documents",
            description="Search through documents for relevant information",
            parameters={
                "query": {"type": "string", "required": True},
                "max_results": {"type": "integer", "default": 10}
            }
        ),
        Tool(
            name="get_weather",
            description="Get current weather for a location",
            parameters={
                "location": {"type": "string", "required": True},
                "units": {"type": "string", "default": "celsius"}
            }
        ),
        Tool(
            name="calculate",
            description="Perform mathematical calculations",
            parameters={
                "expression": {"type": "string", "required": True}
            }
        ),
        Tool(
            name="send_email",
            description="Send an email",
            parameters={
                "to": {"type": "string", "required": True},
                "subject": {"type": "string", "required": True},
                "body": {"type": "string", "required": True}
            }
        ),
        Tool(
            name="create_calendar_event",
            description="Create a calendar event",
            parameters={
                "title": {"type": "string", "required": True},
                "date": {"type": "string", "required": True},
                "time": {"type": "string", "required": True}
            }
        )
    ]
    return tools


def evaluate_tool_selection_example():
    """
    Evaluate if model selects correct tools for task.
    Tests tool selection accuracy.
    """
    print("\n=== Tool Selection Evaluation ===")

    tools = define_example_tools()
    evaluator = MCPEvaluator(tools)

    # Test case: User wants weather information
    task = "What's the weather like in Tokyo?"
    expected_tools = ["get_weather"]
    actual_tool_calls = [
        ToolCall(
            tool_name="get_weather",
            arguments={"location": "Tokyo", "units": "celsius"}
        )
    ]

    result = evaluator.evaluate_tool_selection(task, expected_tools, actual_tool_calls)

    print(f"Task: {task}")
    print(f"Expected Tools: {expected_tools}")
    print(f"Actual Tools: {result.actual_tools}")
    print(f"Score: {result.score:.2f}")
    print(f"Passed: {result.passed}")
    print(f"Details: {json.dumps(result.details, indent=2)}")

    return result


def evaluate_tool_arguments_example():
    """
    Evaluate if tool arguments are correct.
    Tests argument accuracy.
    """
    print("\n=== Tool Arguments Evaluation ===")

    tools = define_example_tools()
    evaluator = MCPEvaluator(tools)

    # Test case with specific arguments
    tool_call = ToolCall(
        tool_name="send_email",
        arguments={
            "to": "user@example.com",
            "subject": "Meeting Update",
            "body": "The meeting has been rescheduled"
        }
    )

    expected_arguments = {
        "to": "user@example.com",
        "subject": "Meeting Update",
        "body": "The meeting has been rescheduled"
    }

    result = evaluator.evaluate_tool_arguments(tool_call, expected_arguments)

    print(f"Tool: {tool_call.tool_name}")
    print(f"Score: {result['score']:.2f}")
    print(f"Passed: {result['passed']}")
    print(f"Correct Args: {result['correct_args']}")
    print(f"Missing Args: {result['missing_args']}")
    print(f"Incorrect Args: {result['incorrect_args']}")

    return result


def evaluate_multi_step_task():
    """
    Evaluate multi-step task execution.
    Tests tool sequencing and chaining.
    """
    print("\n=== Multi-Step Task Evaluation ===")

    tools = define_example_tools()
    evaluator = MCPEvaluator(tools)

    # Complex task requiring multiple tools
    task = "Search for project info, then email the team"

    expected_sequence = ["search_documents", "send_email"]

    actual_tool_calls = [
        ToolCall(
            tool_name="search_documents",
            arguments={"query": "project info", "max_results": 5}
        ),
        ToolCall(
            tool_name="send_email",
            arguments={
                "to": "team@example.com",
                "subject": "Project Info",
                "body": "Here is the project information"
            }
        )
    ]

    result = evaluator.evaluate_tool_sequence(actual_tool_calls, expected_sequence)

    print(f"Task: {task}")
    print(f"Expected Sequence: {result['expected_sequence']}")
    print(f"Actual Sequence: {result['actual_sequence']}")
    print(f"Score: {result['score']:.2f}")
    print(f"Passed: {result['passed']}")
    print(f"Length Match: {result['length_match']}")

    return result


def evaluate_context_usage():
    """
    Evaluate if model uses provided context correctly.
    Tests context awareness and utilization.
    """
    print("\n=== Context Usage Evaluation ===")

    # Evaluate if model uses context to answer without unnecessary tool calls
    context = {
        "user_location": "New York",
        "user_timezone": "EST",
        "current_time": "14:30"
    }

    # Task that can be answered from context
    task = "What time is it?"

    # Good: Uses context, no tool call needed
    scenario_a = []

    # Bad: Makes unnecessary tool call
    scenario_b = [
        ToolCall(tool_name="get_weather", arguments={"location": "New York"})
    ]

    def score_context_usage(tool_calls, context_keys_needed):
        if len(tool_calls) == 0:
            # No tool calls - good if answer is in context
            return 1.0
        else:
            # Unnecessary tool calls - penalize
            return 0.5

    score_a = score_context_usage(scenario_a, ["current_time"])
    score_b = score_context_usage(scenario_b, ["current_time"])

    print(f"Task: {task}")
    print(f"Available Context: {list(context.keys())}")
    print(f"\nScenario A (No tools): Score = {score_a:.2f} ✓")
    print(f"Scenario B (Unnecessary call): Score = {score_b:.2f} ✗")

    return score_a, score_b


def evaluate_error_handling():
    """
    Evaluate error handling in tool calls.
    Tests robustness and recovery.
    """
    print("\n=== Error Handling Evaluation ===")

    tools = define_example_tools()

    # Scenario: Tool call fails, does model recover?
    task = "Get weather and create reminder"

    tool_calls = [
        ToolCall(
            tool_name="get_weather",
            arguments={"location": "InvalidCity"},
            status=ToolCallStatus.FAILED
        ),
        ToolCall(
            tool_name="get_weather",
            arguments={"location": "London"},
            status=ToolCallStatus.SUCCESS  # Retry with valid input
        ),
        ToolCall(
            tool_name="create_calendar_event",
            arguments={"title": "Check weather", "date": "2024-01-20", "time": "10:00"},
            status=ToolCallStatus.SUCCESS
        )
    ]

    # Evaluate error recovery
    has_failure = any(tc.status == ToolCallStatus.FAILED for tc in tool_calls)
    has_recovery = len([tc for tc in tool_calls if tc.status == ToolCallStatus.SUCCESS]) > 0

    score = 1.0 if has_recovery else 0.0

    print(f"Task: {task}")
    print(f"Tool Calls: {len(tool_calls)}")
    print(f"Failed Calls: {sum(1 for tc in tool_calls if tc.status == ToolCallStatus.FAILED)}")
    print(f"Successful Calls: {sum(1 for tc in tool_calls if tc.status == ToolCallStatus.SUCCESS)}")
    print(f"Error Recovery: {has_recovery}")
    print(f"Score: {score:.2f}")

    return score


def evaluate_tool_call_efficiency():
    """
    Evaluate efficiency of tool usage.
    Tests if model minimizes unnecessary calls.
    """
    print("\n=== Tool Call Efficiency Evaluation ===")

    task = "Find documents about machine learning"

    # Efficient: Single targeted call
    efficient_calls = [
        ToolCall(
            tool_name="search_documents",
            arguments={"query": "machine learning", "max_results": 10}
        )
    ]

    # Inefficient: Multiple redundant calls
    inefficient_calls = [
        ToolCall(
            tool_name="search_documents",
            arguments={"query": "machine", "max_results": 5}
        ),
        ToolCall(
            tool_name="search_documents",
            arguments={"query": "learning", "max_results": 5}
        ),
        ToolCall(
            tool_name="search_documents",
            arguments={"query": "machine learning", "max_results": 10}
        )
    ]

    def efficiency_score(tool_calls, optimal_count=1):
        actual_count = len(tool_calls)
        if actual_count == optimal_count:
            return 1.0
        elif actual_count < optimal_count:
            return 0.5  # Too few calls
        else:
            # Penalize extra calls
            return max(0.0, 1.0 - 0.2 * (actual_count - optimal_count))

    efficient_score = efficiency_score(efficient_calls)
    inefficient_score = efficiency_score(inefficient_calls)

    print(f"Task: {task}")
    print(f"Optimal Tool Calls: 1")
    print(f"\nEfficient Approach:")
    print(f"  Tool Calls: {len(efficient_calls)}")
    print(f"  Score: {efficient_score:.2f} ✓")
    print(f"\nInefficient Approach:")
    print(f"  Tool Calls: {len(inefficient_calls)}")
    print(f"  Score: {inefficient_score:.2f} ✗")

    return efficient_score, inefficient_score


def evaluate_parameter_extraction():
    """
    Evaluate parameter extraction from user input.
    Tests if model correctly parses user intent into tool parameters.
    """
    print("\n=== Parameter Extraction Evaluation ===")

    test_cases = [
        {
            "user_input": "Email john@example.com about the Q4 report",
            "expected_tool": "send_email",
            "expected_params": {
                "to": "john@example.com",
                "subject": "Q4 report",
                "body": "about the Q4 report"
            },
            "actual_params": {
                "to": "john@example.com",
                "subject": "Q4 Report",
                "body": "Information about the Q4 report"
            }
        }
    ]

    for case in test_cases:
        # Score parameter extraction
        expected = case["expected_params"]
        actual = case["actual_params"]

        scores = []
        for key in expected.keys():
            if key in actual:
                # Check if values are semantically similar (simplified)
                exp_val = str(expected[key]).lower()
                act_val = str(actual[key]).lower()
                if exp_val in act_val or act_val in exp_val:
                    scores.append(1.0)
                else:
                    scores.append(0.5)
            else:
                scores.append(0.0)

        avg_score = sum(scores) / len(scores) if scores else 0

        print(f"User Input: {case['user_input']}")
        print(f"Expected Tool: {case['expected_tool']}")
        print(f"Parameter Extraction Score: {avg_score:.2f}")
        print(f"Passed: {avg_score >= 0.8}")


def comprehensive_mcp_evaluation():
    """
    Run comprehensive MCP evaluation across all dimensions.
    Complete end-to-end evaluation suite.
    """
    print("\n=== Comprehensive MCP Evaluation ===")

    tools = define_example_tools()
    evaluator = MCPEvaluator(tools)

    # Test case: Complex multi-step task
    task = "Search for meeting notes, then email the summary to the team and create a follow-up reminder"

    expected_tools = ["search_documents", "send_email", "create_calendar_event"]
    expected_sequence = ["search_documents", "send_email", "create_calendar_event"]

    actual_tool_calls = [
        ToolCall(
            tool_name="search_documents",
            arguments={"query": "meeting notes", "max_results": 5}
        ),
        ToolCall(
            tool_name="send_email",
            arguments={
                "to": "team@example.com",
                "subject": "Meeting Summary",
                "body": "Here's the summary from our meeting"
            }
        ),
        ToolCall(
            tool_name="create_calendar_event",
            arguments={
                "title": "Follow-up on meeting",
                "date": "2024-01-25",
                "time": "14:00"
            }
        )
    ]

    # Evaluate tool selection
    selection_result = evaluator.evaluate_tool_selection(task, expected_tools, actual_tool_calls)

    # Evaluate sequence
    sequence_result = evaluator.evaluate_tool_sequence(actual_tool_calls, expected_sequence)

    # Overall score
    overall_score = (selection_result.score + sequence_result["score"]) / 2

    print(f"Task: {task}")
    print(f"\nTool Selection:")
    print(f"  Score: {selection_result.score:.2f}")
    print(f"  Passed: {selection_result.passed}")
    print(f"\nTool Sequence:")
    print(f"  Score: {sequence_result['score']:.2f}")
    print(f"  Passed: {sequence_result['passed']}")
    print(f"\nOverall Score: {overall_score:.2f}")
    print(f"Overall Passed: {overall_score >= 0.8}")

    return overall_score


def main():
    """Run all MCPEval examples."""
    print("=" * 60)
    print("MCPEval (Model Context Protocol Evaluation) Examples")
    print("=" * 60)

    try:
        # Define tools
        tools = define_example_tools()
        print(f"\n✓ Defined {len(tools)} MCP tools for evaluation")

        # Run evaluations
        evaluate_tool_selection_example()
        evaluate_tool_arguments_example()
        evaluate_multi_step_task()
        evaluate_context_usage()
        evaluate_error_handling()
        evaluate_tool_call_efficiency()
        evaluate_parameter_extraction()
        comprehensive_mcp_evaluation()

        print("\n" + "=" * 60)
        print("All MCPEval evaluations completed successfully!")
        print("=" * 60)

        print("\n📊 MCPEval Evaluation Dimensions:")
        print("  • Tool Selection: Correct tool choice for task")
        print("  • Argument Accuracy: Correct tool parameters")
        print("  • Sequence Adherence: Correct order of operations")
        print("  • Context Usage: Efficient context utilization")
        print("  • Error Handling: Recovery from failures")
        print("  • Efficiency: Minimal unnecessary calls")
        print("  • Parameter Extraction: Parsing user intent")

        print("\n💡 Use Cases:")
        print("  • Agent evaluation")
        print("  • Function calling models")
        print("  • Tool-use systems")
        print("  • MCP-compliant applications")

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Setup required:")
        print("  1. pip install mcp")
        print("  2. Define your MCP tools")
        print("  3. Implement tool calling in your model")


if __name__ == "__main__":
    main()
