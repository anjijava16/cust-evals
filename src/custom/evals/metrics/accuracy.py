"""Custom accuracy evaluation metric with normalization options."""

from typing import Optional

from ..evaluators import Score, create_evaluator


def _normalize_text(text: str, lowercase: bool = True, strip: bool = True) -> str:
    """Normalize text for comparison.

    Args:
        text: Text to normalize
        lowercase: Convert to lowercase
        strip: Remove leading/trailing whitespace

    Returns:
        Normalized text
    """
    if strip:
        text = text.strip()
    if lowercase:
        text = text.lower()
    return text


@create_evaluator(name="accuracy", kind="code", direction="maximize")
def custom_accuracy(
    output: str,
    expected: str,
    normalize: bool = True,
    lowercase: bool = True,
) -> Score:
    """Calculate accuracy with optional text normalization.

    This metric is similar to exact_match but supports text normalization
    options for more flexible matching.

    Args:
        output: The output to evaluate
        expected: The expected output
        normalize: Whether to normalize text (strip whitespace, lowercase)
        lowercase: Whether to convert to lowercase (when normalize=True)

    Returns:
        Score: A Score object with accuracy score (1.0 or 0.0)

    Examples:
        >>> # Basic usage - exact match with normalization
        >>> eval_input = {"output": " Paris ", "expected": "paris"}
        >>> score = custom_accuracy(eval_input)
        >>> print(score)
        Score(score=1.0, name='accuracy', label='correct', ...)

        >>> # Without normalization - strict matching
        >>> eval_input = {"output": " Paris ", "expected": "paris"}
        >>> score = custom_accuracy(eval_input, normalize=False)
        >>> print(score)
        Score(score=0.0, name='accuracy', label='incorrect', ...)

        >>> # With field mapping
        >>> eval_input = {"prediction": "42", "target": "42"}
        >>> field_mapping = {"output": "prediction", "expected": "target"}
        >>> score = custom_accuracy(eval_input, field_mapping=field_mapping)
        >>> print(score)
        Score(score=1.0, name='accuracy', label='correct', ...)
    """
    # Apply normalization if requested
    if normalize:
        output_normalized = _normalize_text(output, lowercase=lowercase)
        expected_normalized = _normalize_text(expected, lowercase=lowercase)
        correct = output_normalized == expected_normalized
    else:
        correct = output == expected

    label = "correct" if correct else "incorrect"

    metadata = {
        "normalization": "enabled" if normalize else "disabled",
    }
    if normalize:
        metadata["lowercase"] = lowercase

    return Score(
        score=float(correct),
        label=label,
        explanation=f"Output is {label}",
        metadata=metadata
    )
