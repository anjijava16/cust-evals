"""
Text Similarity Metrics for comparing outputs against ground truth.

This module provides similarity-based metrics for evaluating text outputs.
Useful for comparing model outputs, search results, or any text comparison tasks.
"""

from typing import Dict, Any, Set
import re
from difflib import SequenceMatcher
from ..evaluators import create_evaluator, Score


@create_evaluator(name="exact_match", kind="code", direction="maximize")
def exact_match(output: str, expected: str) -> Score:
    """
    Exact string matching - character-for-character comparison.

    Args:
        output: Generated/predicted text
        expected: Ground truth text

    Returns:
        Score: 1.0 if exact match, 0.0 otherwise
    """
    match = output == expected
    score_value = 1.0 if match else 0.0

    label = "match" if match else "no_match"

    return Score(
        score=score_value,
        name="exact_match",
        label=label,
        explanation="Exact character-for-character match" if match else "Strings differ",
        direction="maximize",
        kind="code",
        metadata={
            "output_length": len(output),
            "expected_length": len(expected),
            "match": match
        }
    )


@create_evaluator(name="case_insensitive_match", kind="code", direction="maximize")
def case_insensitive_match(output: str, expected: str) -> Score:
    """
    Case-insensitive string matching.

    Args:
        output: Generated/predicted text
        expected: Ground truth text

    Returns:
        Score: 1.0 if match (ignoring case), 0.0 otherwise
    """
    match = output.lower() == expected.lower()
    score_value = 1.0 if match else 0.0

    label = "match" if match else "no_match"

    return Score(
        score=score_value,
        name="case_insensitive_match",
        label=label,
        explanation="Case-insensitive match" if match else "Strings differ (ignoring case)",
        direction="maximize",
        kind="code",
        metadata={
            "output_lowercase": output.lower(),
            "expected_lowercase": expected.lower(),
            "match": match
        }
    )


@create_evaluator(name="normalized_match", kind="code", direction="maximize")
def normalized_match(output: str, expected: str) -> Score:
    """
    Normalized matching after removing punctuation and normalizing whitespace.

    Normalization steps:
    - Convert to lowercase
    - Strip leading/trailing whitespace
    - Normalize multiple spaces to single space
    - Remove all punctuation

    Args:
        output: Generated/predicted text
        expected: Ground truth text

    Returns:
        Score: 1.0 if normalized match, 0.0 otherwise
    """
    def normalize(text: str) -> str:
        """Apply normalization to text."""
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return text

    normalized_output = normalize(output)
    normalized_expected = normalize(expected)
    match = normalized_output == normalized_expected
    score_value = 1.0 if match else 0.0

    label = "match" if match else "no_match"

    return Score(
        score=score_value,
        name="normalized_match",
        label=label,
        explanation=f'Normalized match: "{normalized_output[:50]}" vs "{normalized_expected[:50]}"',
        direction="maximize",
        kind="code",
        metadata={
            "normalized_output": normalized_output,
            "normalized_expected": normalized_expected,
            "match": match,
            "original_output": output,
            "original_expected": expected
        }
    )


@create_evaluator(name="sequence_similarity", kind="code", direction="maximize")
def sequence_similarity(
    output: str,
    expected: str,
    threshold: float = 0.8
) -> Score:
    """
    Calculate sequence similarity ratio using difflib.SequenceMatcher.

    Returns a similarity ratio between 0.0 and 1.0, where 1.0 means the sequences
    are identical and 0.0 means they have nothing in common.

    Args:
        output: Generated/predicted text
        expected: Ground truth text
        threshold: Minimum similarity to be considered a "pass" (default: 0.8)

    Returns:
        Score: Similarity ratio (0.0-1.0)
    """
    ratio = SequenceMatcher(None, output, expected).ratio()
    passes = ratio >= threshold

    label = "excellent" if ratio >= 0.95 else \
            "good" if ratio >= 0.85 else \
            "acceptable" if ratio >= 0.70 else \
            "poor"

    return Score(
        score=ratio,
        name="sequence_similarity",
        label=label,
        explanation=f"Sequence similarity: {ratio:.2%} ({'passes' if passes else 'fails'} {threshold:.0%} threshold)",
        direction="maximize",
        kind="code",
        metadata={
            "similarity_ratio": ratio,
            "threshold": threshold,
            "passes_threshold": passes,
            "output_length": len(output),
            "expected_length": len(expected)
        }
    )


@create_evaluator(name="word_overlap", kind="code", direction="maximize")
def word_overlap(
    output: str,
    expected: str,
    threshold: float = 0.7
) -> Score:
    """
    Calculate word-level overlap using Jaccard similarity.

    Jaccard similarity = |A ∩ B| / |A ∪ B|

    This metric extracts words from both texts (case-insensitive) and calculates
    the ratio of shared words to total unique words.

    Args:
        output: Generated/predicted text
        expected: Ground truth text
        threshold: Minimum overlap to be considered a "pass" (default: 0.7)

    Returns:
        Score: Jaccard similarity (0.0-1.0)
    """
    def get_words(text: str) -> Set[str]:
        """Extract words from text (case-insensitive)."""
        return set(re.findall(r'\w+', text.lower()))

    output_words = get_words(output)
    expected_words = get_words(expected)

    # Handle edge cases
    if not output_words and not expected_words:
        score_value = 1.0
        intersection_count = 0
        union_count = 0
    elif not output_words or not expected_words:
        score_value = 0.0
        intersection_count = 0
        union_count = len(output_words | expected_words)
    else:
        intersection = output_words & expected_words
        union = output_words | expected_words
        intersection_count = len(intersection)
        union_count = len(union)
        score_value = intersection_count / union_count if union_count > 0 else 0.0

    passes = score_value >= threshold

    label = "excellent" if score_value >= 0.90 else \
            "good" if score_value >= 0.75 else \
            "acceptable" if score_value >= 0.60 else \
            "poor"

    return Score(
        score=score_value,
        name="word_overlap",
        label=label,
        explanation=f"Word overlap (Jaccard): {score_value:.2%} "
                   f"({intersection_count}/{union_count} words)",
        direction="maximize",
        kind="code",
        metadata={
            "jaccard_similarity": score_value,
            "intersection_count": intersection_count,
            "union_count": union_count,
            "output_word_count": len(output_words),
            "expected_word_count": len(expected_words),
            "threshold": threshold,
            "passes_threshold": passes,
            "common_words": list(output_words & expected_words) if output_words and expected_words else [],
            "missing_words": list(expected_words - output_words) if expected_words else [],
            "extra_words": list(output_words - expected_words) if output_words else []
        }
    )


@create_evaluator(name="contains_match", kind="code", direction="maximize")
def contains_match(
    output: str,
    expected: str,
    case_sensitive: bool = False
) -> Score:
    """
    Check if one text contains the other (bidirectional containment check).

    Returns 1.0 if either:
    - output contains expected, or
    - expected contains output

    Args:
        output: Generated/predicted text
        expected: Ground truth text
        case_sensitive: Whether to perform case-sensitive matching (default: False)

    Returns:
        Score: 1.0 if containment found, 0.0 otherwise
    """
    if case_sensitive:
        output_cmp = output
        expected_cmp = expected
    else:
        output_cmp = output.lower()
        expected_cmp = expected.lower()

    output_contains_expected = expected_cmp in output_cmp
    expected_contains_output = output_cmp in expected_cmp
    contains = output_contains_expected or expected_contains_output

    score_value = 1.0 if contains else 0.0

    label = "contains" if contains else "no_containment"

    # Determine which direction
    if output_contains_expected and expected_contains_output:
        direction_info = "exact match (both contain each other)"
    elif output_contains_expected:
        direction_info = "output contains expected"
    elif expected_contains_output:
        direction_info = "expected contains output"
    else:
        direction_info = "no containment found"

    return Score(
        score=score_value,
        name="contains_match",
        label=label,
        explanation=f"Containment check: {direction_info}",
        direction="maximize",
        kind="code",
        metadata={
            "contains": contains,
            "output_contains_expected": output_contains_expected,
            "expected_contains_output": expected_contains_output,
            "case_sensitive": case_sensitive,
            "output_length": len(output),
            "expected_length": len(expected)
        }
    )


@create_evaluator(name="length_similarity", kind="code", direction="maximize")
def length_similarity(
    output: str,
    expected: str,
    threshold: float = 0.8
) -> Score:
    """
    Compare text lengths and calculate similarity ratio.

    Ratio = min(len_output, len_expected) / max(len_output, len_expected)

    This metric is useful for detecting if outputs are significantly shorter
    or longer than expected, which might indicate truncation or verbosity issues.

    Args:
        output: Generated/predicted text
        expected: Ground truth text
        threshold: Minimum ratio to be considered a "pass" (default: 0.8)

    Returns:
        Score: Length similarity ratio (0.0-1.0)
    """
    len_output = len(output)
    len_expected = len(expected)

    if len_expected == 0 and len_output == 0:
        score_value = 1.0
    elif len_expected == 0 or len_output == 0:
        score_value = 0.0
    else:
        score_value = min(len_output, len_expected) / max(len_output, len_expected)

    passes = score_value >= threshold

    label = "excellent" if score_value >= 0.95 else \
            "good" if score_value >= 0.85 else \
            "acceptable" if score_value >= 0.70 else \
            "poor"

    # Determine if output is shorter or longer
    if len_output < len_expected:
        length_comparison = f"output is {len_expected - len_output} chars shorter"
    elif len_output > len_expected:
        length_comparison = f"output is {len_output - len_expected} chars longer"
    else:
        length_comparison = "lengths are equal"

    return Score(
        score=score_value,
        name="length_similarity",
        label=label,
        explanation=f"Length similarity: {score_value:.2%} "
                   f"({len_output} vs {len_expected} chars, {length_comparison})",
        direction="maximize",
        kind="code",
        metadata={
            "length_ratio": score_value,
            "output_length": len_output,
            "expected_length": len_expected,
            "length_difference": abs(len_output - len_expected),
            "threshold": threshold,
            "passes_threshold": passes
        }
    )
