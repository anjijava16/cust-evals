"""
Tests for OCR metrics module.

Run with: pytest tests/test_ocr_metrics.py -v
"""

import pytest
from custom.evals.metrics.ocr_metrics import (
    text_extraction_accuracy,
    character_error_rate,
    word_error_rate,
    bounding_box_iou,
    confidence_threshold,
    field_detection_accuracy,
    BoundingBox,
    calculate_iou,
    normalize_text
)


class TestTextExtractionAccuracy:
    """Tests for text_extraction_accuracy metric."""

    def test_perfect_match(self):
        eval_input = {
            "output": "Hello World",
            "expected": "Hello World"
        }
        score = text_extraction_accuracy(eval_input)

        assert score.score == 1.0
        assert score.label == "excellent"
        assert score.name == "text_extraction_accuracy"

    def test_partial_match(self):
        eval_input = {
            "output": "Hello Wrld",  # Missing 'o'
            "expected": "Hello World"
        }
        score = text_extraction_accuracy(eval_input)

        assert 0.8 < score.score < 1.0
        assert score.label in ["good", "excellent"]

    def test_case_insensitive(self):
        eval_input = {
            "output": "HELLO WORLD",
            "expected": "hello world"
        }
        score = text_extraction_accuracy(eval_input, case_sensitive=False)

        assert score.score == 1.0

    def test_normalization(self):
        eval_input = {
            "output": "Hello,  World!",
            "expected": "Hello World"
        }
        score = text_extraction_accuracy(eval_input, normalize=True)

        assert score.score >= 0.95  # Should be very close after normalization


class TestCharacterErrorRate:
    """Tests for character_error_rate metric."""

    def test_perfect_match(self):
        eval_input = {
            "output": "Test",
            "expected": "Test"
        }
        score = character_error_rate(eval_input)

        assert score.score == 1.0
        assert score.metadata["raw_cer"] == 0.0
        assert score.metadata["edit_distance"] == 0

    def test_single_char_difference(self):
        eval_input = {
            "output": "Test",
            "expected": "Text"  # 1 character different
        }
        score = character_error_rate(eval_input)

        expected_cer = 1 / 4  # 1 edit in 4 characters
        assert abs(score.metadata["raw_cer"] - expected_cer) < 0.01
        assert score.metadata["edit_distance"] == 1

    def test_complete_mismatch(self):
        eval_input = {
            "output": "AAAA",
            "expected": "BBBB"
        }
        score = character_error_rate(eval_input)

        assert score.metadata["raw_cer"] == 1.0
        assert score.score == 0.0  # Inverted


class TestWordErrorRate:
    """Tests for word_error_rate metric."""

    def test_perfect_match(self):
        eval_input = {
            "output": "Hello World",
            "expected": "Hello World"
        }
        score = word_error_rate(eval_input)

        assert score.score == 1.0
        assert score.label == "excellent"

    def test_one_word_different(self):
        eval_input = {
            "output": "Hello Universe",
            "expected": "Hello World"
        }
        score = word_error_rate(eval_input)

        assert score.metadata["output_word_count"] == 2
        assert score.metadata["expected_word_count"] == 2
        assert score.score < 1.0


class TestBoundingBoxIoU:
    """Tests for bounding_box_iou metric."""

    def test_perfect_overlap(self):
        bbox = {"Left": 0.1, "Top": 0.2, "Width": 0.3, "Height": 0.1}

        eval_input = {
            "output_bbox": bbox,
            "expected_bbox": bbox
        }
        score = bounding_box_iou(eval_input)

        assert score.score == 1.0
        assert score.label == "excellent"

    def test_no_overlap(self):
        eval_input = {
            "output_bbox": {"Left": 0.0, "Top": 0.0, "Width": 0.1, "Height": 0.1},
            "expected_bbox": {"Left": 0.5, "Top": 0.5, "Width": 0.1, "Height": 0.1}
        }
        score = bounding_box_iou(eval_input)

        assert score.score == 0.0
        assert score.label == "poor"

    def test_partial_overlap(self):
        eval_input = {
            "output_bbox": {"Left": 0.0, "Top": 0.0, "Width": 0.5, "Height": 0.5},
            "expected_bbox": {"Left": 0.25, "Top": 0.25, "Width": 0.5, "Height": 0.5}
        }
        score = bounding_box_iou(eval_input)

        assert 0.0 < score.score < 1.0

    def test_lowercase_fields(self):
        """Test that lowercase field names work."""
        eval_input = {
            "output_bbox": {"left": 0.1, "top": 0.2, "width": 0.3, "height": 0.1},
            "expected_bbox": {"left": 0.1, "top": 0.2, "width": 0.3, "height": 0.1}
        }
        score = bounding_box_iou(eval_input)

        assert score.score == 1.0


class TestBoundingBoxClass:
    """Tests for BoundingBox dataclass."""

    def test_properties(self):
        bbox = BoundingBox(left=0.1, top=0.2, width=0.3, height=0.1)

        assert bbox.right == 0.4
        assert bbox.bottom == 0.3
        assert bbox.area == 0.03

    def test_from_dict_uppercase(self):
        data = {"Left": 0.1, "Top": 0.2, "Width": 0.3, "Height": 0.1}
        bbox = BoundingBox.from_dict(data)

        assert bbox.left == 0.1
        assert bbox.top == 0.2
        assert bbox.width == 0.3
        assert bbox.height == 0.1

    def test_from_dict_lowercase(self):
        data = {"left": 0.1, "top": 0.2, "width": 0.3, "height": 0.1}
        bbox = BoundingBox.from_dict(data)

        assert bbox.left == 0.1


class TestCalculateIoU:
    """Tests for calculate_iou function."""

    def test_identical_boxes(self):
        box1 = BoundingBox(0.1, 0.2, 0.3, 0.1)
        box2 = BoundingBox(0.1, 0.2, 0.3, 0.1)

        iou = calculate_iou(box1, box2)
        assert iou == 1.0

    def test_no_intersection(self):
        box1 = BoundingBox(0.0, 0.0, 0.1, 0.1)
        box2 = BoundingBox(0.5, 0.5, 0.1, 0.1)

        iou = calculate_iou(box1, box2)
        assert iou == 0.0

    def test_half_overlap(self):
        box1 = BoundingBox(0.0, 0.0, 0.2, 0.2)  # Area: 0.04
        box2 = BoundingBox(0.1, 0.0, 0.2, 0.2)  # Area: 0.04

        # Intersection: 0.1 * 0.2 = 0.02
        # Union: 0.04 + 0.04 - 0.02 = 0.06
        # IoU: 0.02 / 0.06 = 0.333...

        iou = calculate_iou(box1, box2)
        assert abs(iou - 0.333) < 0.01


class TestConfidenceThreshold:
    """Tests for confidence_threshold metric."""

    def test_pass_threshold_0_to_1(self):
        eval_input = {
            "confidence": 0.95,
            "threshold": 0.90
        }
        score = confidence_threshold(eval_input)

        assert score.score == 1.0
        assert score.label == "pass"
        assert score.metadata["passes_threshold"] is True

    def test_fail_threshold_0_to_1(self):
        eval_input = {
            "confidence": 0.85,
            "threshold": 0.90
        }
        score = confidence_threshold(eval_input)

        assert score.score == 0.0
        assert score.label == "fail"
        assert score.metadata["passes_threshold"] is False

    def test_pass_threshold_0_to_100(self):
        """Test auto-normalization of 0-100 range."""
        eval_input = {
            "confidence": 95.0,
            "threshold": 0.90
        }
        score = confidence_threshold(eval_input)

        assert score.score == 1.0
        assert score.label == "pass"

    def test_exact_threshold(self):
        eval_input = {
            "confidence": 0.90,
            "threshold": 0.90
        }
        score = confidence_threshold(eval_input)

        assert score.score == 1.0  # Should pass when equal


class TestFieldDetectionAccuracy:
    """Tests for field_detection_accuracy metric."""

    def test_perfect_match(self):
        fields = ["Field1", "Field2", "Field3"]

        eval_input = {
            "detected_fields": fields,
            "expected_fields": fields
        }
        score = field_detection_accuracy(eval_input)

        assert score.score == 1.0
        assert score.label == "excellent"
        assert score.metadata["true_positives"] == 3
        assert score.metadata["false_positives"] == 0
        assert score.metadata["false_negatives"] == 0

    def test_partial_match(self):
        eval_input = {
            "detected_fields": ["Field1", "Field2", "Field3"],
            "expected_fields": ["Field1", "Field2", "Field4"]
        }
        score = field_detection_accuracy(eval_input)

        # TP: 2, FP: 1, FN: 1
        # Precision: 2/3 = 0.667
        # Recall: 2/3 = 0.667
        # F1: 0.667

        assert abs(score.score - 0.667) < 0.01
        assert score.metadata["true_positives"] == 2
        assert score.metadata["false_positives"] == 1
        assert score.metadata["false_negatives"] == 1

    def test_case_insensitive(self):
        eval_input = {
            "detected_fields": ["FIELD1", "FIELD2"],
            "expected_fields": ["field1", "field2"]
        }
        score = field_detection_accuracy(eval_input, case_sensitive=False)

        assert score.score == 1.0

    def test_no_match(self):
        eval_input = {
            "detected_fields": ["Field1", "Field2"],
            "expected_fields": ["Field3", "Field4"]
        }
        score = field_detection_accuracy(eval_input)

        assert score.score == 0.0
        assert score.metadata["true_positives"] == 0


class TestNormalizeText:
    """Tests for normalize_text helper function."""

    def test_lowercase(self):
        result = normalize_text("HELLO WORLD", lowercase=True)
        assert result == "hello world"

    def test_remove_punctuation(self):
        result = normalize_text(
            "Hello, World!",
            lowercase=False,
            remove_punctuation=True
        )
        assert result == "Hello World"

    def test_remove_whitespace(self):
        result = normalize_text(
            "Hello    World",
            lowercase=False,
            remove_punctuation=False,
            remove_whitespace=True
        )
        assert result == "Hello World"

    def test_all_normalizations(self):
        result = normalize_text(
            "  HELLO,   WORLD!  ",
            lowercase=True,
            remove_punctuation=True,
            remove_whitespace=True
        )
        assert result == "hello world"


class TestScoreStructure:
    """Test that all metrics return proper Score objects."""

    def test_score_fields(self):
        eval_input = {
            "output": "test",
            "expected": "test"
        }
        score = text_extraction_accuracy(eval_input)

        # Check all required Score fields
        assert hasattr(score, "score")
        assert hasattr(score, "name")
        assert hasattr(score, "label")
        assert hasattr(score, "explanation")
        assert hasattr(score, "direction")
        assert hasattr(score, "kind")
        assert hasattr(score, "metadata")

        # Check types
        assert isinstance(score.score, float)
        assert isinstance(score.name, str)
        assert isinstance(score.label, str)
        assert isinstance(score.explanation, str)
        assert score.direction in ["maximize", "minimize"]
        assert score.kind == "code"
        assert isinstance(score.metadata, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
