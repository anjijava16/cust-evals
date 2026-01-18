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

# Tracing support (optional)
try:
    from .tracing import (
        initialize_tracing,
        get_tracer,
        traced,
        add_span_attributes,
        force_flush_tracing,
        shutdown_tracing,
    )
    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False
    initialize_tracing = None
    get_tracer = None
    traced = None
    add_span_attributes = None
    force_flush_tracing = None
    shutdown_tracing = None

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
    # Tracing (optional)
    "initialize_tracing",
    "get_tracer",
    "traced",
    "add_span_attributes",
    "force_flush_tracing",
    "shutdown_tracing",
]
