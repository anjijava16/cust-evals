"""Base evaluator classes and score definitions."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Literal, Optional


@dataclass
class Score:
    """Represents an evaluation score with metadata.

    Args:
        score: Numeric score value (typically 0.0 to 1.0)
        name: Name of the metric
        label: Optional categorical label
        explanation: Optional explanation of the score
        direction: Whether higher or lower is better
        kind: Type of evaluator (code, llm, human, heuristic)
        metadata: Additional metadata
    """

    score: float
    name: str = "score"
    label: Optional[str] = None
    explanation: Optional[str] = None
    direction: Literal["maximize", "minimize", "neutral"] = "maximize"
    kind: Literal["code", "llm", "human", "heuristic"] = "code"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert score to dictionary."""
        return {
            "score": self.score,
            "name": self.name,
            "label": self.label,
            "explanation": self.explanation,
            "direction": self.direction,
            "kind": self.kind,
            "metadata": self.metadata,
        }


def create_evaluator(
    name: str,
    kind: Literal["code", "llm", "human", "heuristic"] = "code",
    direction: Literal["maximize", "minimize", "neutral"] = "maximize",
) -> Callable:
    """Decorator to create an evaluator function.

    Args:
        name: Name of the evaluator
        kind: Type of evaluator
        direction: Whether to maximize or minimize the score

    Returns:
        Decorator function that wraps evaluation logic

    Example:
        @create_evaluator(name="exact_match", kind="code")
        def exact_match(output: str, expected: str) -> Score:
            return Score(score=1.0 if output == expected else 0.0)
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(
            eval_input: Dict[str, Any],
            field_mapping: Optional[Dict[str, str]] = None,
            **extra_kwargs: Any,
        ) -> Score:
            """
            Evaluate input and return score.

            Args:
                eval_input: Dictionary with evaluation inputs
                field_mapping: Optional mapping from evaluator params to input keys
                **extra_kwargs: Additional keyword arguments passed to the evaluator

            Returns:
                Score object with evaluation results
            """
            # Apply field mapping if provided
            if field_mapping:
                mapped_input = {}
                for eval_param, input_key in field_mapping.items():
                    if input_key in eval_input:
                        mapped_input[eval_param] = eval_input[input_key]
                kwargs = mapped_input
            else:
                kwargs = eval_input

            # Merge with extra kwargs (extra_kwargs take precedence)
            kwargs.update(extra_kwargs)

            # Call the evaluation function
            result = func(**kwargs)

            # Ensure result is a Score object
            if not isinstance(result, Score):
                result = Score(score=float(result))

            # Override score metadata with evaluator config
            result.name = name
            result.kind = kind
            result.direction = direction

            return result

        # Preserve original function metadata
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__

        return wrapper

    return decorator
