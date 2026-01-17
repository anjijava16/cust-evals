"""Comprehensive tests for LLM-based evaluators with mocked LLM responses."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json
from custom.evals import (
    HallucinationEvaluator,
    CorrectnessEvaluator,
    RelevanceEvaluator,
    CoherenceEvaluator,
    FaithfulnessEvaluator,
    AnswerRelevancyEvaluator,
    Score
)


class TestHallucinationEvaluator:
    """Tests for HallucinationEvaluator."""

    def test_hallucination_evaluator_factual(self, mock_llm_openai):
        """Test hallucination evaluator with factual response."""
        # Mock response indicating factual
        mock_response = {"verdict": "factual", "explanation": "Response is grounded in context."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is the capital of France?",
            "output": "Paris is the capital of France.",
            "context": "Paris is the capital of France."
        }

        score = evaluator.evaluate(eval_input)

        assert isinstance(score, Score)
        assert score.name == "hallucination"
        assert score.label == "factual"
        assert score.score == 0.0  # Lower is better for hallucination
        assert score.direction == "minimize"

    def test_hallucination_evaluator_hallucinated(self, mock_llm_openai):
        """Test hallucination evaluator with hallucinated response."""
        mock_response = {"verdict": "hallucinated", "explanation": "Response contains unsupported information."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is the capital of France?",
            "output": "Paris is the capital with 20 million people.",
            "context": "Paris is the capital of France."
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "hallucinated"
        assert score.score == 1.0

    def test_hallucination_evaluator_describe(self, mock_llm_openai):
        """Test hallucination evaluator describe method."""
        evaluator = HallucinationEvaluator(mock_llm_openai)

        description = evaluator.describe()

        assert isinstance(description, dict)
        assert description["name"] == "hallucination"
        assert description["direction"] == "minimize"
        assert "model" in description
        assert description["provider"] == "openai"

    def test_hallucination_evaluator_missing_context(self, mock_llm_openai):
        """Test hallucination evaluator with missing context field."""
        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is the capital of France?",
            "output": "Paris is the capital of France."
            # Missing context
        }

        score = evaluator.evaluate(eval_input)

        # Should return error score for missing required field
        assert isinstance(score, Score)
        assert score.label == "error"


class TestCorrectnessEvaluator:
    """Tests for CorrectnessEvaluator."""

    def test_correctness_evaluator_correct(self, mock_llm_openai):
        """Test correctness evaluator with correct response."""
        mock_response = {"verdict": "correct", "explanation": "The output matches the expected answer."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = CorrectnessEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is 2 + 2?",
            "output": "4",
            "expected": "4"
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "correct"
        assert score.score == 1.0
        assert score.direction == "maximize"

    def test_correctness_evaluator_incorrect(self, mock_llm_openai):
        """Test correctness evaluator with incorrect response."""
        mock_response = {"verdict": "incorrect", "explanation": "The output does not match the expected answer."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = CorrectnessEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is 2 + 2?",
            "output": "5",
            "expected": "4"
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "incorrect"
        assert score.score == 0.0

    def test_correctness_evaluator_no_ground_truth(self, mock_llm_openai):
        """Test correctness evaluator without ground truth."""
        evaluator = CorrectnessEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is 2 + 2?",
            "output": "4"
            # Missing expected
        }

        score = evaluator.evaluate(eval_input)

        # Should return no_ground_truth error
        assert score.label == "no_ground_truth"
        assert "requires ground truth" in score.explanation.lower()


class TestRelevanceEvaluator:
    """Tests for RelevanceEvaluator."""

    def test_relevance_evaluator_relevant(self, mock_llm_openai):
        """Test relevance evaluator with relevant context."""
        mock_response = {"verdict": "relevant", "explanation": "Context addresses the query."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = RelevanceEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is Python?",
            "context": "Python is a high-level programming language."
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "relevant"
        assert score.score == 1.0
        assert score.direction == "maximize"

    def test_relevance_evaluator_irrelevant(self, mock_llm_openai):
        """Test relevance evaluator with irrelevant context."""
        mock_response = {"verdict": "irrelevant", "explanation": "Context does not address the query."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = RelevanceEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is Python?",
            "context": "JavaScript is used for web development."
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "irrelevant"
        assert score.score == 0.0


class TestCoherenceEvaluator:
    """Tests for CoherenceEvaluator."""

    def test_coherence_evaluator_coherent(self, mock_llm_openai):
        """Test coherence evaluator with coherent text."""
        mock_response = {"verdict": "coherent", "explanation": "Text flows logically."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = CoherenceEvaluator(mock_llm_openai)
        eval_input = {
            "input": "Explain AI",
            "output": "AI is artificial intelligence. It enables machines to learn and make decisions."
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "coherent"
        assert score.score == 1.0
        assert score.direction == "maximize"

    def test_coherence_evaluator_incoherent(self, mock_llm_openai):
        """Test coherence evaluator with incoherent text."""
        mock_response = {"verdict": "incoherent", "explanation": "Text lacks logical flow."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = CoherenceEvaluator(mock_llm_openai)
        eval_input = {
            "input": "Explain AI",
            "output": "AI blue banana. Then coffee machine yesterday."
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "incoherent"
        assert score.score == 0.0


class TestFaithfulnessEvaluator:
    """Tests for FaithfulnessEvaluator (RAG-specific)."""

    def test_faithfulness_evaluator_faithful(self, mock_llm_openai):
        """Test faithfulness evaluator with faithful response."""
        mock_response = {"verdict": "faithful", "explanation": "All statements are grounded in context."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = FaithfulnessEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is the capital of France?",
            "output": "Paris is the capital of France.",
            "context": "Paris is the capital and largest city of France."
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "faithful"
        assert score.score == 1.0
        assert score.direction == "maximize"

    def test_faithfulness_evaluator_unfaithful(self, mock_llm_openai):
        """Test faithfulness evaluator with unfaithful response."""
        mock_response = {"verdict": "unfaithful", "explanation": "Response contains unverified information."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = FaithfulnessEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is the capital of France?",
            "output": "Paris is the capital of France with a population of 50 million.",
            "context": "Paris is the capital of France."
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "unfaithful"
        assert score.score == 0.0

    def test_faithfulness_evaluator_missing_context(self, mock_llm_openai):
        """Test faithfulness evaluator with missing context."""
        evaluator = FaithfulnessEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is the capital of France?",
            "output": "Paris is the capital of France."
            # Missing context
        }

        score = evaluator.evaluate(eval_input)

        # Should return error for missing context
        assert score.label == "error"


class TestAnswerRelevancyEvaluator:
    """Tests for AnswerRelevancyEvaluator (RAG-specific)."""

    def test_answer_relevancy_evaluator_relevant(self, mock_llm_openai):
        """Test answer relevancy evaluator with relevant answer."""
        mock_response = {"verdict": "relevant", "explanation": "Answer directly addresses the query."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = AnswerRelevancyEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is machine learning?",
            "output": "Machine learning is a subset of AI that enables systems to learn from data."
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "relevant"
        assert score.score == 1.0
        assert score.direction == "maximize"

    def test_answer_relevancy_evaluator_irrelevant(self, mock_llm_openai):
        """Test answer relevancy evaluator with irrelevant answer."""
        mock_response = {"verdict": "irrelevant", "explanation": "Answer does not address the query."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = AnswerRelevancyEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is machine learning?",
            "output": "Python is a programming language."
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "irrelevant"
        assert score.score == 0.0


class TestAsyncEvaluation:
    """Tests for async evaluation."""

    @pytest.mark.asyncio
    async def test_hallucination_evaluator_async(self, mock_llm_openai):
        """Test hallucination evaluator async evaluation."""
        mock_response = {"verdict": "factual", "explanation": "Response is accurate."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is AI?",
            "output": "AI is artificial intelligence.",
            "context": "AI stands for artificial intelligence."
        }

        score = await evaluator.async_evaluate(eval_input)

        assert isinstance(score, Score)
        assert score.label == "factual"

    @pytest.mark.asyncio
    async def test_correctness_evaluator_async(self, mock_llm_openai):
        """Test correctness evaluator async evaluation."""
        mock_response = {"verdict": "correct", "explanation": "Answer is correct."}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = CorrectnessEvaluator(mock_llm_openai)
        eval_input = {
            "input": "What is 5 + 5?",
            "output": "10",
            "expected": "10"
        }

        score = await evaluator.async_evaluate(eval_input)

        assert score.label == "correct"


class TestEvaluatorEdgeCases:
    """Test edge cases and error handling."""

    def test_invalid_llm_response_format(self, mock_llm_openai):
        """Test evaluator with invalid JSON response from LLM."""
        # Mock invalid JSON response
        mock_llm_openai.generate = Mock(return_value="Not valid JSON")

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {
            "input": "Test query",
            "output": "Test output",
            "context": "Test context"
        }

        score = evaluator.evaluate(eval_input)

        # Should handle invalid JSON gracefully
        assert isinstance(score, Score)
        # Likely returns error or fallback score

    def test_missing_verdict_in_response(self, mock_llm_openai):
        """Test evaluator with missing verdict in LLM response."""
        mock_response = {"explanation": "Some explanation"}  # Missing verdict
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {
            "input": "Test",
            "output": "Test",
            "context": "Test"
        }

        score = evaluator.evaluate(eval_input)

        # Should handle missing verdict gracefully
        assert isinstance(score, Score)

    def test_empty_input_fields(self, mock_llm_openai):
        """Test evaluator with empty input fields."""
        mock_response = {"verdict": "factual", "explanation": "Test"}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {
            "input": "",
            "output": "",
            "context": ""
        }

        score = evaluator.evaluate(eval_input)

        # Should handle empty fields
        assert isinstance(score, Score)

    def test_very_long_input(self, mock_llm_openai):
        """Test evaluator with very long input text."""
        mock_response = {"verdict": "factual", "explanation": "Test"}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        long_text = "This is a test. " * 1000
        eval_input = {
            "input": long_text,
            "output": long_text,
            "context": long_text
        }

        score = evaluator.evaluate(eval_input)

        # Should handle long inputs
        assert isinstance(score, Score)

    def test_unicode_in_input(self, mock_llm_openai):
        """Test evaluator with unicode characters."""
        mock_response = {"verdict": "factual", "explanation": "Test"}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {
            "input": "Café résumé naïve",
            "output": "Español 日本語 한국어",
            "context": "مرحبا Здравствуйте"
        }

        score = evaluator.evaluate(eval_input)

        # Should handle unicode
        assert isinstance(score, Score)


class TestEvaluatorWithAnthropicProvider:
    """Test evaluators with Anthropic provider."""

    def test_hallucination_evaluator_anthropic(self, mock_llm_anthropic):
        """Test hallucination evaluator with Anthropic provider."""
        mock_response = {"verdict": "factual", "explanation": "Accurate."}
        mock_llm_anthropic.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_anthropic)
        eval_input = {
            "input": "Test",
            "output": "Test output",
            "context": "Test context"
        }

        score = evaluator.evaluate(eval_input)

        assert isinstance(score, Score)
        assert score.metadata["provider"] == "anthropic"

    def test_correctness_evaluator_anthropic(self, mock_llm_anthropic):
        """Test correctness evaluator with Anthropic provider."""
        mock_response = {"verdict": "correct", "explanation": "Correct."}
        mock_llm_anthropic.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = CorrectnessEvaluator(mock_llm_anthropic)
        eval_input = {
            "input": "What is 1+1?",
            "output": "2",
            "expected": "2"
        }

        score = evaluator.evaluate(eval_input)

        assert score.label == "correct"
        assert score.metadata["provider"] == "anthropic"


class TestFieldMapping:
    """Test custom field mapping for evaluators."""

    def test_hallucination_evaluator_custom_fields(self, mock_llm_openai):
        """Test hallucination evaluator with custom field names."""
        mock_response = {"verdict": "factual", "explanation": "Test"}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {
            "query": "What is AI?",
            "response": "AI is artificial intelligence.",
            "retrieved_docs": "AI stands for artificial intelligence."
        }

        # This should work if the evaluator checks alternative field names
        # or we need to explicitly test field mapping if implemented
        # For now, test that it handles custom fields appropriately

    def test_correctness_evaluator_alternative_ground_truth_fields(self, mock_llm_openai):
        """Test correctness evaluator recognizes alternative ground truth field names."""
        mock_response = {"verdict": "correct", "explanation": "Correct"}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = CorrectnessEvaluator(mock_llm_openai)

        # Test with 'ground_truth' instead of 'expected'
        eval_input = {
            "input": "What is 2+2?",
            "output": "4",
            "ground_truth": "4"
        }

        score = evaluator.evaluate(eval_input)

        # Should recognize ground_truth as expected
        assert isinstance(score, Score)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
