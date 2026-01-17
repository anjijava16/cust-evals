"""Custom Evals - LLM Evaluation Framework."""

from .evaluators import Score, create_evaluator
from .llm_evaluators import (
    AnswerRelevancyEvaluator,
    CoherenceEvaluator,
    CorrectnessEvaluator,
    FaithfulnessEvaluator,
    HallucinationEvaluator,
    RelevanceEvaluator,
)
from .metrics import custom_accuracy, exact_match, sentiment_score

__version__ = "0.1.0"

__all__ = [
    # Core
    "Score",
    "create_evaluator",
    # Code-based metrics
    "exact_match",
    "sentiment_score",
    "custom_accuracy",
    # LLM-based evaluators
    "HallucinationEvaluator",
    "CorrectnessEvaluator",
    "RelevanceEvaluator",
    "CoherenceEvaluator",
    "FaithfulnessEvaluator",
    "AnswerRelevancyEvaluator",
]
