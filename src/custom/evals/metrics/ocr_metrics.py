"""
OCR and Document Extraction Metrics for AWS Textract and similar services.

This module provides deterministic metrics for evaluating OCR outputs against ground truth.
Designed for non-LLM document extraction evaluation.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from ..evaluators import create_evaluator, Score
import difflib


@dataclass
class BoundingBox:
    """Represents a bounding box in normalized coordinates (0-1)."""
    left: float
    top: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top + self.height

    @property
    def area(self) -> float:
        return self.width * self.height

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BoundingBox':
        """Create from Textract-style dict with Left, Top, Width, Height."""
        return cls(
            left=data.get('Left', data.get('left', 0)),
            top=data.get('Top', data.get('top', 0)),
            width=data.get('Width', data.get('width', 0)),
            height=data.get('Height', data.get('height', 0))
        )


def calculate_iou(box1: BoundingBox, box2: BoundingBox) -> float:
    """Calculate Intersection over Union (IoU) for two bounding boxes."""
    # Calculate intersection
    x_left = max(box1.left, box2.left)
    y_top = max(box1.top, box2.top)
    x_right = min(box1.right, box2.right)
    y_bottom = min(box1.bottom, box2.bottom)

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # Calculate union
    union_area = box1.area + box2.area - intersection_area

    if union_area == 0:
        return 0.0

    return intersection_area / union_area


def normalize_text(text: str, lowercase: bool = True,
                   remove_punctuation: bool = True,
                   remove_whitespace: bool = True) -> str:
    """Normalize text for comparison (OCR-tolerant)."""
    import re

    if lowercase:
        text = text.lower()

    if remove_punctuation:
        text = re.sub(r'[^\w\s]', '', text)

    if remove_whitespace:
        text = re.sub(r'\s+', ' ', text).strip()

    return text


@create_evaluator(name="text_extraction_accuracy", kind="code", direction="maximize")
def text_extraction_accuracy(
    output: str,
    expected: str,
    normalize: bool = True,
    case_sensitive: bool = False
) -> Score:
    """
    Calculate text extraction accuracy using sequence matching.

    Args:
        output: Extracted text from Textract
        expected: Ground truth text
        normalize: Apply normalization (punctuation, whitespace)
        case_sensitive: Whether to consider case

    Returns:
        Score with similarity ratio (0.0-1.0)
    """
    if normalize:
        output_normalized = normalize_text(
            output,
            lowercase=not case_sensitive,
            remove_punctuation=True,
            remove_whitespace=True
        )
        expected_normalized = normalize_text(
            expected,
            lowercase=not case_sensitive,
            remove_punctuation=True,
            remove_whitespace=True
        )
    else:
        output_normalized = output if case_sensitive else output.lower()
        expected_normalized = expected if case_sensitive else expected.lower()

    # Use SequenceMatcher for fuzzy matching
    similarity = difflib.SequenceMatcher(
        None,
        output_normalized,
        expected_normalized
    ).ratio()

    label = "excellent" if similarity >= 0.95 else \
            "good" if similarity >= 0.85 else \
            "acceptable" if similarity >= 0.70 else \
            "poor"

    return Score(
        score=similarity,
        name="text_extraction_accuracy",
        label=label,
        explanation=f"Text similarity: {similarity:.2%}. "
                   f"Output length: {len(output_normalized)}, "
                   f"Expected length: {len(expected_normalized)}",
        direction="maximize",
        kind="code",
        metadata={
            "output_length": len(output),
            "expected_length": len(expected),
            "normalized": normalize,
            "case_sensitive": case_sensitive
        }
    )


@create_evaluator(name="character_error_rate", kind="code", direction="minimize")
def character_error_rate(output: str, expected: str) -> Score:
    """
    Calculate Character Error Rate (CER) - Levenshtein distance normalized.

    CER = (substitutions + deletions + insertions) / total_characters_in_reference

    Args:
        output: Extracted text from Textract
        expected: Ground truth text

    Returns:
        Score with CER (0.0 = perfect, higher = worse)
    """
    import Levenshtein

    distance = Levenshtein.distance(output, expected)
    cer = distance / max(len(expected), 1)  # Avoid division by zero

    # Invert for score (0.0-1.0 where 1.0 is best)
    score = max(0.0, 1.0 - cer)

    label = "excellent" if cer <= 0.05 else \
            "good" if cer <= 0.15 else \
            "acceptable" if cer <= 0.30 else \
            "poor"

    return Score(
        score=score,
        name="character_error_rate",
        label=label,
        explanation=f"CER: {cer:.2%} ({distance} character edits needed). "
                   f"Lower is better.",
        direction="minimize",
        kind="code",
        metadata={
            "raw_cer": cer,
            "edit_distance": distance,
            "output_length": len(output),
            "expected_length": len(expected)
        }
    )


@create_evaluator(name="word_error_rate", kind="code", direction="minimize")
def word_error_rate(output: str, expected: str) -> Score:
    """
    Calculate Word Error Rate (WER).

    WER = (substitutions + deletions + insertions) / total_words_in_reference

    Args:
        output: Extracted text from Textract
        expected: Ground truth text

    Returns:
        Score with WER (0.0 = perfect, higher = worse)
    """
    import Levenshtein

    output_words = output.split()
    expected_words = expected.split()

    distance = Levenshtein.distance(
        ' '.join(output_words),
        ' '.join(expected_words)
    )
    wer = distance / max(len(expected_words), 1)

    # Invert for score
    score = max(0.0, 1.0 - wer)

    label = "excellent" if wer <= 0.05 else \
            "good" if wer <= 0.15 else \
            "acceptable" if wer <= 0.30 else \
            "poor"

    return Score(
        score=score,
        name="word_error_rate",
        label=label,
        explanation=f"WER: {wer:.2%} ({distance} word edits needed). "
                   f"Lower is better.",
        direction="minimize",
        kind="code",
        metadata={
            "raw_wer": wer,
            "edit_distance": distance,
            "output_word_count": len(output_words),
            "expected_word_count": len(expected_words)
        }
    )


@create_evaluator(name="bounding_box_iou", kind="code", direction="maximize")
def bounding_box_iou(
    output_bbox: Dict[str, float],
    expected_bbox: Dict[str, float]
) -> Score:
    """
    Calculate Intersection over Union (IoU) for bounding boxes.

    Args:
        output_bbox: Predicted bounding box (Left, Top, Width, Height)
        expected_bbox: Ground truth bounding box

    Returns:
        Score with IoU (0.0-1.0 where 1.0 is perfect overlap)
    """
    box1 = BoundingBox.from_dict(output_bbox)
    box2 = BoundingBox.from_dict(expected_bbox)

    iou = calculate_iou(box1, box2)

    label = "excellent" if iou >= 0.90 else \
            "good" if iou >= 0.75 else \
            "acceptable" if iou >= 0.50 else \
            "poor"

    return Score(
        score=iou,
        name="bounding_box_iou",
        label=label,
        explanation=f"IoU: {iou:.2%}. Measures spatial overlap accuracy.",
        direction="maximize",
        kind="code",
        metadata={
            "output_bbox": output_bbox,
            "expected_bbox": expected_bbox,
            "output_area": box1.area,
            "expected_area": box2.area
        }
    )


@create_evaluator(name="confidence_threshold", kind="code", direction="maximize")
def confidence_threshold(
    confidence: float,
    threshold: float = 0.8
) -> Score:
    """
    Validate if confidence score meets minimum threshold.

    Args:
        confidence: Textract confidence score (0-100 or 0-1)
        threshold: Minimum acceptable confidence (0-1)

    Returns:
        Score (1.0 if above threshold, 0.0 otherwise)
    """
    # Normalize to 0-1 if confidence is 0-100
    if confidence > 1.0:
        confidence = confidence / 100.0

    passes = confidence >= threshold
    score_value = 1.0 if passes else 0.0

    label = "pass" if passes else "fail"

    return Score(
        score=score_value,
        name="confidence_threshold",
        label=label,
        explanation=f"Confidence: {confidence:.2%} "
                   f"({'above' if passes else 'below'} threshold {threshold:.2%})",
        direction="maximize",
        kind="code",
        metadata={
            "raw_confidence": confidence,
            "threshold": threshold,
            "passes_threshold": passes
        }
    )


@create_evaluator(name="field_detection_accuracy", kind="code", direction="maximize")
def field_detection_accuracy(
    detected_fields: List[str],
    expected_fields: List[str],
    case_sensitive: bool = False
) -> Score:
    """
    Calculate accuracy of form field detection.

    Precision = TP / (TP + FP)
    Recall = TP / (TP + FN)
    F1 = 2 * (Precision * Recall) / (Precision + Recall)

    Args:
        detected_fields: List of field names detected by Textract
        expected_fields: List of expected field names
        case_sensitive: Whether field names are case-sensitive

    Returns:
        Score with F1 score
    """
    if not case_sensitive:
        detected_set = set(f.lower() for f in detected_fields)
        expected_set = set(f.lower() for f in expected_fields)
    else:
        detected_set = set(detected_fields)
        expected_set = set(expected_fields)

    true_positives = len(detected_set & expected_set)
    false_positives = len(detected_set - expected_set)
    false_negatives = len(expected_set - detected_set)

    precision = true_positives / max(true_positives + false_positives, 1)
    recall = true_positives / max(true_positives + false_negatives, 1)

    f1_score = (2 * precision * recall / max(precision + recall, 1)) \
               if (precision + recall) > 0 else 0.0

    label = "excellent" if f1_score >= 0.95 else \
            "good" if f1_score >= 0.85 else \
            "acceptable" if f1_score >= 0.70 else \
            "poor"

    return Score(
        score=f1_score,
        name="field_detection_accuracy",
        label=label,
        explanation=f"F1: {f1_score:.2%}, Precision: {precision:.2%}, "
                   f"Recall: {recall:.2%}. "
                   f"Detected {len(detected_fields)}/{len(expected_fields)} fields.",
        direction="maximize",
        kind="code",
        metadata={
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "missing_fields": list(expected_set - detected_set),
            "extra_fields": list(detected_set - expected_set)
        }
    )
