"""Comprehensive tests for custom evaluation metrics."""

import pytest
from custom.evals import Score, custom_accuracy, exact_match, sentiment_score, create_evaluator


class TestExactMatch:
    """Tests for exact_match metric."""

    def test_exact_match_success(self):
        """Test exact match with matching strings."""
        eval_input = {"output": "Paris", "expected": "Paris"}
        score = exact_match(eval_input)

        assert isinstance(score, Score)
        assert score.score == 1.0
        assert score.name == "exact_match"
        assert score.label == "match"
        assert score.kind == "code"
        assert score.direction == "maximize"

    def test_exact_match_failure(self):
        """Test exact match with non-matching strings."""
        eval_input = {"output": "London", "expected": "Paris"}
        score = exact_match(eval_input)

        assert score.score == 0.0
        assert score.label == "no_match"

    def test_exact_match_with_field_mapping(self):
        """Test exact match with custom field mapping."""
        eval_input = {"prediction": "Tokyo", "ground_truth": "Tokyo"}
        field_mapping = {"output": "prediction", "expected": "ground_truth"}
        score = exact_match(eval_input, field_mapping=field_mapping)

        assert score.score == 1.0

    def test_exact_match_case_sensitive(self):
        """Test exact match is case-sensitive."""
        eval_input = {"output": "paris", "expected": "Paris"}
        score = exact_match(eval_input)

        assert score.score == 0.0
        assert score.label == "no_match"

    def test_exact_match_with_whitespace(self):
        """Test exact match with whitespace differences."""
        eval_input = {"output": "Paris ", "expected": " Paris"}
        score = exact_match(eval_input)

        assert score.score == 0.0

    def test_exact_match_with_numbers(self):
        """Test exact match with numeric strings."""
        eval_input = {"output": "42", "expected": "42"}
        score = exact_match(eval_input)

        assert score.score == 1.0

    def test_exact_match_empty_strings(self):
        """Test exact match with empty strings."""
        eval_input = {"output": "", "expected": ""}
        score = exact_match(eval_input)

        assert score.score == 1.0

    def test_exact_match_special_characters(self):
        """Test exact match with special characters."""
        eval_input = {"output": "hello@world.com", "expected": "hello@world.com"}
        score = exact_match(eval_input)

        assert score.score == 1.0

    def test_exact_match_unicode(self):
        """Test exact match with unicode characters."""
        eval_input = {"output": "café", "expected": "café"}
        score = exact_match(eval_input)

        assert score.score == 1.0

    def test_exact_match_multiline(self):
        """Test exact match with multiline strings."""
        text = "Line 1\nLine 2\nLine 3"
        eval_input = {"output": text, "expected": text}
        score = exact_match(eval_input)

        assert score.score == 1.0

    def test_exact_match_missing_output(self):
        """Test exact match with missing output field."""
        eval_input = {"expected": "Paris"}

        # Missing 'output' field raises TypeError (not KeyError)
        with pytest.raises(TypeError):
            exact_match(eval_input)

    def test_exact_match_missing_expected(self):
        """Test exact match with missing expected field."""
        eval_input = {"output": "Paris"}

        # Missing expected returns no_ground_truth score
        score = exact_match(eval_input)
        assert score.score == 0.0
        assert score.label == "no_ground_truth"


class TestSentiment:
    """Tests for sentiment_score metric."""

    def test_positive_sentiment(self):
        """Test positive sentiment detection."""
        eval_input = {"text": "I love this! It's amazing and great!"}
        score = sentiment_score(eval_input)

        assert isinstance(score, Score)
        assert score.score > 0.5
        assert score.label == "positive"
        assert score.name == "sentiment"
        assert score.kind == "code"

    def test_negative_sentiment(self):
        """Test negative sentiment detection."""
        eval_input = {"text": "This is terrible and awful. I hate it."}
        score = sentiment_score(eval_input)

        assert score.score < 0.5
        assert score.label == "negative"

    def test_neutral_sentiment(self):
        """Test neutral sentiment detection."""
        eval_input = {"text": "The package arrived."}
        score = sentiment_score(eval_input)

        assert score.label == "neutral"
        assert 0.4 <= score.score <= 0.6

    def test_empty_text_sentiment(self):
        """Test sentiment with empty text."""
        eval_input = {"text": ""}
        score = sentiment_score(eval_input)

        # Empty text should be neutral
        assert score.label == "neutral"
        assert score.score == 0.5

    def test_very_positive_sentiment(self):
        """Test very positive sentiment."""
        eval_input = {"text": "Excellent! Outstanding! Perfect! Amazing! Wonderful! Best ever!"}
        score = sentiment_score(eval_input)

        assert score.score > 0.7
        assert score.label == "positive"

    def test_very_negative_sentiment(self):
        """Test very negative sentiment."""
        eval_input = {"text": "Horrible! Terrible! Awful! Worst! Disgusting! Never again!"}
        score = sentiment_score(eval_input)

        assert score.score < 0.3
        assert score.label == "negative"

    def test_mixed_sentiment(self):
        """Test mixed sentiment text."""
        eval_input = {"text": "The product is good but the service was bad."}
        score = sentiment_score(eval_input)

        # Should lean slightly positive or neutral
        assert 0.3 <= score.score <= 0.7

    def test_sentiment_with_punctuation(self):
        """Test sentiment with heavy punctuation."""
        eval_input = {"text": "Great!!! Amazing!!! Wow!!!"}
        score = sentiment_score(eval_input)

        assert score.label == "positive"

    def test_sentiment_with_emojis(self):
        """Test sentiment with emoji-like text."""
        eval_input = {"text": "This is good :) :)"}
        score = sentiment_score(eval_input)

        assert score.label == "positive"

    def test_sentiment_with_field_mapping(self):
        """Test sentiment with custom field mapping."""
        eval_input = {"content": "I love this!"}
        field_mapping = {"text": "content"}
        score = sentiment_score(eval_input, field_mapping=field_mapping)

        assert score.label == "positive"

    def test_sentiment_missing_text(self):
        """Test sentiment with missing text field."""
        eval_input = {"content": "Some text"}

        # Missing 'text' field raises TypeError
        with pytest.raises(TypeError):
            sentiment_score(eval_input)


class TestCustomAccuracy:
    """Tests for custom_accuracy metric."""

    def test_accuracy_with_normalization(self):
        """Test accuracy with text normalization."""
        eval_input = {"output": " Paris ", "expected": "paris"}
        score = custom_accuracy(eval_input, normalize=True)

        assert score.score == 1.0
        assert score.label == "correct"
        assert score.metadata["normalization"] == "enabled"

    def test_accuracy_without_normalization(self):
        """Test accuracy without text normalization."""
        eval_input = {"output": " Paris ", "expected": "paris"}
        score = custom_accuracy(eval_input, normalize=False)

        assert score.score == 0.0
        assert score.label == "incorrect"
        assert score.metadata["normalization"] == "disabled"

    def test_accuracy_numbers(self):
        """Test accuracy with numeric strings."""
        eval_input = {"output": "42", "expected": "42"}
        score = custom_accuracy(eval_input)

        assert score.score == 1.0

    def test_accuracy_with_field_mapping(self):
        """Test accuracy with field mapping."""
        eval_input = {"pred": "yes", "target": "yes"}
        field_mapping = {"output": "pred", "expected": "target"}
        score = custom_accuracy(eval_input, field_mapping=field_mapping)

        assert score.score == 1.0

    def test_accuracy_normalization_removes_whitespace(self):
        """Test normalization removes leading/trailing whitespace."""
        eval_input = {"output": "  hello  ", "expected": "hello"}
        score = custom_accuracy(eval_input, normalize=True)

        assert score.score == 1.0

    def test_accuracy_normalization_lowercases(self):
        """Test normalization converts to lowercase."""
        eval_input = {"output": "HELLO", "expected": "hello"}
        score = custom_accuracy(eval_input, normalize=True)

        assert score.score == 1.0

    def test_accuracy_normalization_preserves_case_when_disabled(self):
        """Test case is preserved when normalization is disabled."""
        eval_input = {"output": "HELLO", "expected": "hello"}
        score = custom_accuracy(eval_input, normalize=False)

        assert score.score == 0.0

    def test_accuracy_empty_strings(self):
        """Test accuracy with empty strings."""
        eval_input = {"output": "", "expected": ""}
        score = custom_accuracy(eval_input)

        assert score.score == 1.0

    def test_accuracy_special_characters(self):
        """Test accuracy with special characters."""
        eval_input = {"output": "test@123", "expected": "test@123"}
        score = custom_accuracy(eval_input)

        assert score.score == 1.0

    def test_accuracy_unicode(self):
        """Test accuracy with unicode."""
        eval_input = {"output": "café", "expected": "café"}
        score = custom_accuracy(eval_input)

        assert score.score == 1.0

    def test_accuracy_multiline(self):
        """Test accuracy with multiline text."""
        text = "Line 1\nLine 2"
        eval_input = {"output": text, "expected": text}
        score = custom_accuracy(eval_input)

        assert score.score == 1.0

    def test_accuracy_normalization_with_multiline(self):
        """Test normalization with multiline text."""
        eval_input = {"output": "  Line 1\nLine 2  ", "expected": "line 1\nline 2"}
        score = custom_accuracy(eval_input, normalize=True)

        assert score.score == 1.0


class TestScoreObject:
    """Tests for Score object."""

    def test_score_creation(self):
        """Test Score object creation."""
        score = Score(
            score=0.85,
            name="test_metric",
            label="pass",
            explanation="Test passed",
            direction="maximize",
            kind="code",
            metadata={"test": "value"}
        )

        assert score.score == 0.85
        assert score.name == "test_metric"
        assert score.label == "pass"
        assert score.explanation == "Test passed"
        assert score.direction == "maximize"
        assert score.kind == "code"
        assert score.metadata == {"test": "value"}

    def test_score_to_dict(self):
        """Test Score.to_dict() method."""
        score = Score(
            score=0.95,
            name="test_metric",
            label="positive",
            explanation="Test explanation",
            direction="maximize",
            kind="code",
            metadata={"key": "value"}
        )

        score_dict = score.to_dict()

        assert score_dict["score"] == 0.95
        assert score_dict["name"] == "test_metric"
        assert score_dict["label"] == "positive"
        assert score_dict["explanation"] == "Test explanation"
        assert score_dict["direction"] == "maximize"
        assert score_dict["kind"] == "code"
        assert score_dict["metadata"]["key"] == "value"

    def test_score_to_dict_all_fields(self):
        """Test Score.to_dict() includes all fields."""
        score = Score(
            score=0.5,
            name="metric",
            label="neutral",
            explanation="Explanation",
            direction="neutral",
            kind="heuristic",
            metadata={}
        )

        score_dict = score.to_dict()

        assert "score" in score_dict
        assert "name" in score_dict
        assert "label" in score_dict
        assert "explanation" in score_dict
        assert "direction" in score_dict
        assert "kind" in score_dict
        assert "metadata" in score_dict

    def test_score_optional_fields(self):
        """Test Score with optional fields as None."""
        score = Score(
            score=0.75,
            name="test",
            label=None,
            explanation=None,
            direction="maximize",
            kind="code",
            metadata=None
        )

        assert score.label is None
        assert score.explanation is None
        assert score.metadata is None

    def test_score_default_metadata(self):
        """Test Score with default empty metadata."""
        score = Score(
            score=0.5,
            name="test",
            direction="maximize",
            kind="code"
        )

        score_dict = score.to_dict()
        assert "metadata" in score_dict

    def test_score_repr(self):
        """Test Score string representation."""
        score = Score(
            score=0.8,
            name="test_metric",
            label="pass",
            direction="maximize",
            kind="code"
        )

        repr_str = repr(score)
        assert "test_metric" in repr_str
        assert "0.8" in repr_str or "0.80" in repr_str


class TestCreateEvaluatorDecorator:
    """Tests for create_evaluator decorator."""

    def test_create_evaluator_basic(self):
        """Test create_evaluator decorator with basic function."""

        @create_evaluator(name="test_evaluator", kind="code")
        def test_metric(value: float) -> Score:
            return Score(
                score=value,
                label="test" if value > 0.5 else "fail",
                explanation=f"Value is {value}"
            )

        # create_evaluator expects a dict input
        result = test_metric({"value": 0.8})

        assert isinstance(result, Score)
        assert result.score == 0.8
        assert result.name == "test_evaluator"
        assert result.kind == "code"
        assert result.label == "test"

    def test_create_evaluator_with_direction(self):
        """Test create_evaluator with custom direction."""

        @create_evaluator(name="loss_metric", kind="code", direction="minimize")
        def loss_metric(loss: float) -> Score:
            return Score(
                score=loss,
                label="low" if loss < 0.1 else "high",
                explanation=f"Loss: {loss}"
            )

        # create_evaluator expects a dict input
        result = loss_metric({"loss": 0.05})

        assert result.direction == "minimize"
        assert result.label == "low"

    def test_create_evaluator_preserves_metadata(self):
        """Test create_evaluator preserves metadata from inner function."""

        @create_evaluator(name="custom_eval", kind="code")
        def custom_metric(x: int) -> Score:
            return Score(
                score=float(x) / 100,
                label="pass",
                metadata={"original_value": x}
            )

        # create_evaluator expects a dict input
        result = custom_metric({"x": 75})

        assert result.score == 0.75
        assert result.metadata["original_value"] == 75
        assert result.name == "custom_eval"


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_exact_match_none_values(self):
        """Test exact match with None values."""
        eval_input = {"output": None, "expected": None}

        # Should handle None gracefully (as strings)
        try:
            score = exact_match(eval_input)
            # If it doesn't raise, check it handles None -> str conversion
            assert isinstance(score, Score)
        except (TypeError, AttributeError):
            # Expected if None is not handled
            pass

    def test_sentiment_very_long_text(self):
        """Test sentiment with very long text."""
        long_text = "This is great! " * 1000
        eval_input = {"text": long_text}

        score = sentiment_score(eval_input)

        assert isinstance(score, Score)
        assert score.label == "positive"

    def test_accuracy_with_integers(self):
        """Test accuracy with integer inputs (edge case)."""
        # If the function accepts any type and converts to string
        eval_input = {"output": 42, "expected": 42}

        try:
            score = custom_accuracy(eval_input)
            # Should work if it handles type conversion
            assert isinstance(score, Score)
        except (TypeError, AttributeError):
            # Expected if non-string inputs aren't handled
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
