"""Exact match evaluation metric."""

from typing import Optional

from ..evaluators import Score, create_evaluator


@create_evaluator(name="exact_match", kind="code", direction="maximize")
def exact_match(output: str, expected: Optional[str] = None) -> Score:
    """Return exact_match score: 1.0 if output == expected else 0.0.

    Note: No text normalization is performed.

    Args:
        output: The output to evaluate
        expected: The expected output (optional - if not provided, returns score of 0.0)

    Returns:
        Score: A Score object with score 1.0 if output matches expected, 0.0 otherwise

    Examples:
        >>> # With ground truth
        >>> eval_input = {"output": "Paris", "expected": "Paris"}
        >>> score = exact_match(eval_input)
        >>> print(score)
        Score(score=1.0, name='exact_match', label='match', ...)

        >>> # Without ground truth (can't evaluate)
        >>> eval_input = {"output": "Paris"}
        >>> score = exact_match(eval_input)
        >>> print(score)
        Score(score=0.0, name='exact_match', label='no_ground_truth', ...)

        >>> # With field mapping
        >>> eval_input = {"prediction": "Paris", "ground_truth": "Paris"}
        >>> field_mapping = {"output": "prediction", "expected": "ground_truth"}
        >>> score = exact_match(eval_input, field_mapping=field_mapping)
        >>> print(score)
        Score(score=1.0, name='exact_match', label='match', ...)
    """
    if expected is None:
        return Score(
            score=0.0,
            label="no_ground_truth",
            explanation="Cannot evaluate without expected value",
            metadata={"has_ground_truth": False}
        )

    correct = output == expected
    label = "match" if correct else "no_match"

    return Score(
        score=float(correct),
        label=label,
        explanation=f"Output {'matches' if correct else 'does not match'} expected value",
        metadata={"has_ground_truth": True}
    )
