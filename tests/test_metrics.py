"""Tests for custom evaluation metrics."""

import pytest
from custom.evals import Score, custom_accuracy, exact_match, sentiment_score


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

    def test_negative_sentiment(self):
        """Test negative sentiment detection."""
        eval_input = {"text": "This is terrible and awful."}
        score = sentiment_score(eval_input)

        assert score.score < 0.5
        assert score.label == "negative"

    def test_neutral_sentiment(self):
        """Test neutral sentiment detection."""
        eval_input = {"text": "The package arrived."}
        score = sentiment_score(eval_input)

        assert score.label == "neutral"
        assert 0.4 <= score.score <= 0.6


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


class TestScoreObject:
    """Tests for Score object."""

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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
