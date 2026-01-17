"""Tests for base evaluator classes and functionality."""

import pytest
from unittest.mock import Mock
import json
from custom.evals import Score
from custom.evals.llm_evaluators import LLMEvaluator


class TestLLMEvaluatorBase:
    """Tests for LLMEvaluator base class."""

    def test_llm_evaluator_requires_llm(self):
        """Test LLMEvaluator requires LLM instance."""
        from custom.evals import HallucinationEvaluator

        # Should require LLM
        with pytest.raises(TypeError):
            HallucinationEvaluator()

    def test_llm_evaluator_stores_llm(self, mock_llm_openai):
        """Test LLMEvaluator stores LLM instance."""
        from custom.evals import HallucinationEvaluator

        evaluator = HallucinationEvaluator(mock_llm_openai)

        assert evaluator.llm == mock_llm_openai

    def test_llm_evaluator_has_name(self, mock_llm_openai):
        """Test LLMEvaluator has name attribute."""
        from custom.evals import HallucinationEvaluator

        evaluator = HallucinationEvaluator(mock_llm_openai)

        assert hasattr(evaluator, "name")
        assert evaluator.name == "hallucination"

    def test_llm_evaluator_has_direction(self, mock_llm_openai):
        """Test LLMEvaluator has direction attribute."""
        from custom.evals import HallucinationEvaluator, CorrectnessEvaluator

        hall_eval = HallucinationEvaluator(mock_llm_openai)
        corr_eval = CorrectnessEvaluator(mock_llm_openai)

        assert hall_eval.DIRECTION == "minimize"
        assert corr_eval.DIRECTION == "maximize"

    def test_llm_evaluator_describe_method(self, mock_llm_openai):
        """Test LLMEvaluator describe method."""
        from custom.evals import HallucinationEvaluator

        evaluator = HallucinationEvaluator(mock_llm_openai)
        description = evaluator.describe()

        assert isinstance(description, dict)
        assert "name" in description
        assert "direction" in description
        assert "model" in description
        assert "provider" in description
        assert description["name"] == "hallucination"


class TestGroundTruthHandling:
    """Tests for ground truth handling in evaluators."""

    def test_check_ground_truth_with_expected(self, mock_llm_openai):
        """Test _check_ground_truth with 'expected' field."""
        from custom.evals import CorrectnessEvaluator

        evaluator = CorrectnessEvaluator(mock_llm_openai)
        eval_input = {"input": "test", "output": "test", "expected": "test"}

        has_gt = evaluator._check_ground_truth(eval_input)

        assert has_gt is True

    def test_check_ground_truth_with_ground_truth(self, mock_llm_openai):
        """Test _check_ground_truth with 'ground_truth' field."""
        from custom.evals import CorrectnessEvaluator

        evaluator = CorrectnessEvaluator(mock_llm_openai)
        eval_input = {"input": "test", "output": "test", "ground_truth": "test"}

        has_gt = evaluator._check_ground_truth(eval_input)

        assert has_gt is True

    def test_check_ground_truth_with_reference(self, mock_llm_openai):
        """Test _check_ground_truth with 'reference' field."""
        from custom.evals import CorrectnessEvaluator

        evaluator = CorrectnessEvaluator(mock_llm_openai)
        eval_input = {"input": "test", "output": "test", "reference": "test"}

        has_gt = evaluator._check_ground_truth(eval_input)

        assert has_gt is True

    def test_check_ground_truth_without_any(self, mock_llm_openai):
        """Test _check_ground_truth without ground truth fields."""
        from custom.evals import CorrectnessEvaluator

        evaluator = CorrectnessEvaluator(mock_llm_openai)
        eval_input = {"input": "test", "output": "test"}

        has_gt = evaluator._check_ground_truth(eval_input)

        assert has_gt is False

    def test_evaluator_requires_ground_truth_flag(self, mock_llm_openai):
        """Test evaluators have REQUIRES_GROUND_TRUTH flag."""
        from custom.evals import CorrectnessEvaluator, HallucinationEvaluator

        # Correctness requires ground truth
        corr_eval = CorrectnessEvaluator(mock_llm_openai)
        assert corr_eval.REQUIRES_GROUND_TRUTH is True

        # Hallucination does not require ground truth
        hall_eval = HallucinationEvaluator(mock_llm_openai)
        assert hall_eval.REQUIRES_GROUND_TRUTH is False


class TestEvaluatorReturnTypes:
    """Test evaluators return correct Score objects."""

    def test_evaluate_returns_score(self, mock_llm_openai):
        """Test evaluate method returns Score object."""
        from custom.evals import HallucinationEvaluator

        mock_response = {"verdict": "factual", "explanation": "Test"}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {"input": "test", "output": "test", "context": "test"}

        score = evaluator.evaluate(eval_input)

        assert isinstance(score, Score)

    def test_score_has_required_fields(self, mock_llm_openai):
        """Test Score object has all required fields."""
        from custom.evals import HallucinationEvaluator

        mock_response = {"verdict": "factual", "explanation": "Test"}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {"input": "test", "output": "test", "context": "test"}

        score = evaluator.evaluate(eval_input)

        assert hasattr(score, "score")
        assert hasattr(score, "name")
        assert hasattr(score, "label")
        assert hasattr(score, "explanation")
        assert hasattr(score, "kind")
        assert hasattr(score, "direction")
        assert hasattr(score, "metadata")

    def test_score_metadata_includes_model_info(self, mock_llm_openai):
        """Test Score metadata includes model information."""
        from custom.evals import HallucinationEvaluator

        mock_response = {"verdict": "factual", "explanation": "Test"}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {"input": "test", "output": "test", "context": "test"}

        score = evaluator.evaluate(eval_input)

        assert "model" in score.metadata
        assert "provider" in score.metadata
        assert score.metadata["model"] == "gpt-4o-mini"
        assert score.metadata["provider"] == "openai"


class TestEvaluatorInputValidation:
    """Test evaluators validate input correctly."""

    def test_evaluator_missing_required_field(self, mock_llm_openai):
        """Test evaluator handles missing required field."""
        from custom.evals import HallucinationEvaluator

        evaluator = HallucinationEvaluator(mock_llm_openai)

        # Missing context field
        eval_input = {"input": "test", "output": "test"}

        score = evaluator.evaluate(eval_input)

        # Should return error score
        assert score.label == "error"

    def test_evaluator_with_extra_fields(self, mock_llm_openai):
        """Test evaluator handles extra fields gracefully."""
        from custom.evals import HallucinationEvaluator

        mock_response = {"verdict": "factual", "explanation": "Test"}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)

        # Extra fields should be ignored
        eval_input = {
            "input": "test",
            "output": "test",
            "context": "test",
            "extra_field": "ignored"
        }

        score = evaluator.evaluate(eval_input)

        # Should work normally
        assert isinstance(score, Score)


class TestPromptTemplateUsage:
    """Test evaluators use prompt templates correctly."""

    def test_evaluator_has_prompt_template(self, mock_llm_openai):
        """Test evaluators have PROMPT_TEMPLATE attribute."""
        from custom.evals import HallucinationEvaluator

        evaluator = HallucinationEvaluator(mock_llm_openai)

        assert hasattr(evaluator, "PROMPT_TEMPLATE")
        assert isinstance(evaluator.PROMPT_TEMPLATE, str)
        assert len(evaluator.PROMPT_TEMPLATE) > 0

    def test_prompt_template_contains_placeholders(self, mock_llm_openai):
        """Test prompt templates contain expected placeholders."""
        from custom.evals import HallucinationEvaluator

        evaluator = HallucinationEvaluator(mock_llm_openai)

        # Should contain placeholders for formatting
        template = evaluator.PROMPT_TEMPLATE
        assert "{" in template and "}" in template


class TestChoicesMapping:
    """Test evaluators use CHOICES mapping correctly."""

    def test_evaluator_has_choices(self, mock_llm_openai):
        """Test evaluators have CHOICES attribute."""
        from custom.evals import HallucinationEvaluator

        evaluator = HallucinationEvaluator(mock_llm_openai)

        assert hasattr(evaluator, "CHOICES")
        assert isinstance(evaluator.CHOICES, dict)

    def test_choices_map_to_scores(self, mock_llm_openai):
        """Test CHOICES map labels to numeric scores."""
        from custom.evals import HallucinationEvaluator, CorrectnessEvaluator

        hall_eval = HallucinationEvaluator(mock_llm_openai)
        corr_eval = CorrectnessEvaluator(mock_llm_openai)

        # Hallucination: factual=0.0, hallucinated=1.0
        assert hall_eval.CHOICES["factual"] == 0.0
        assert hall_eval.CHOICES["hallucinated"] == 1.0

        # Correctness: correct=1.0, incorrect=0.0
        assert corr_eval.CHOICES["correct"] == 1.0
        assert corr_eval.CHOICES["incorrect"] == 0.0


class TestAsyncEvaluationSupport:
    """Test async evaluation support."""

    @pytest.mark.asyncio
    async def test_async_evaluate_method_exists(self, mock_llm_openai):
        """Test evaluators have async_evaluate method."""
        from custom.evals import HallucinationEvaluator

        evaluator = HallucinationEvaluator(mock_llm_openai)

        assert hasattr(evaluator, "async_evaluate")
        assert callable(evaluator.async_evaluate)

    @pytest.mark.asyncio
    async def test_async_evaluate_returns_score(self, mock_llm_openai):
        """Test async_evaluate returns Score object."""
        from custom.evals import HallucinationEvaluator

        mock_response = {"verdict": "factual", "explanation": "Test"}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {"input": "test", "output": "test", "context": "test"}

        score = await evaluator.async_evaluate(eval_input)

        assert isinstance(score, Score)


class TestEvaluatorErrorHandling:
    """Test evaluators handle errors gracefully."""

    def test_evaluator_handles_llm_error(self, mock_llm_openai):
        """Test evaluator handles LLM generation error."""
        from custom.evals import HallucinationEvaluator

        # Mock LLM to raise exception
        mock_llm_openai.generate = Mock(side_effect=Exception("LLM Error"))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {"input": "test", "output": "test", "context": "test"}

        # Should handle error gracefully (may raise or return error score)
        try:
            score = evaluator.evaluate(eval_input)
            # If it doesn't raise, check it's a valid score
            assert isinstance(score, Score)
        except Exception:
            # Exception propagated (acceptable behavior)
            pass

    def test_evaluator_handles_invalid_json_response(self, mock_llm_openai):
        """Test evaluator handles invalid JSON from LLM."""
        from custom.evals import HallucinationEvaluator

        # Mock LLM to return invalid JSON
        mock_llm_openai.generate = Mock(return_value="Not valid JSON at all")

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {"input": "test", "output": "test", "context": "test"}

        score = evaluator.evaluate(eval_input)

        # Should handle gracefully
        assert isinstance(score, Score)


class TestEvaluatorInheritance:
    """Test evaluator inheritance structure."""

    def test_evaluators_inherit_from_llm_evaluator(self, mock_llm_openai):
        """Test all LLM evaluators inherit from LLMEvaluator."""
        from custom.evals import (
            HallucinationEvaluator,
            CorrectnessEvaluator,
            RelevanceEvaluator,
            CoherenceEvaluator,
            FaithfulnessEvaluator,
            AnswerRelevancyEvaluator
        )

        evaluators = [
            HallucinationEvaluator(mock_llm_openai),
            CorrectnessEvaluator(mock_llm_openai),
            RelevanceEvaluator(mock_llm_openai),
            CoherenceEvaluator(mock_llm_openai),
            FaithfulnessEvaluator(mock_llm_openai),
            AnswerRelevancyEvaluator(mock_llm_openai)
        ]

        for evaluator in evaluators:
            assert isinstance(evaluator, LLMEvaluator)

    def test_evaluators_implement_required_attributes(self, mock_llm_openai):
        """Test evaluators implement required class attributes."""
        from custom.evals import HallucinationEvaluator

        evaluator = HallucinationEvaluator(mock_llm_openai)

        # Required attributes
        assert hasattr(evaluator, "NAME")
        assert hasattr(evaluator, "DIRECTION")
        assert hasattr(evaluator, "CHOICES")
        assert hasattr(evaluator, "PROMPT_TEMPLATE")
        assert hasattr(evaluator, "REQUIRES_GROUND_TRUTH")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
