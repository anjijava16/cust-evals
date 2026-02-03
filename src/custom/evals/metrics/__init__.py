"""Evaluation metrics."""

from .accuracy import custom_accuracy
from .exact_match import exact_match
from .sentiment import sentiment_score
from .ocr_metrics import (
    text_extraction_accuracy,
    character_error_rate,
    word_error_rate,
    bounding_box_iou,
    confidence_threshold,
    field_detection_accuracy,
)
from .similarity_metrics import (
    exact_match as similarity_exact_match,
    case_insensitive_match,
    normalized_match,
    sequence_similarity,
    word_overlap,
    contains_match,
    length_similarity,
)
from .advanced_similarity_metrics import (
    bleu_score,
    rouge_n,
    rouge_l,
    jaro_winkler_similarity,
    dice_coefficient,
    token_f1_score,
    cosine_similarity_tfidf,
)

__all__ = [
    "exact_match",
    "sentiment_score",
    "custom_accuracy",
    # OCR/Document Extraction Metrics
    "text_extraction_accuracy",
    "character_error_rate",
    "word_error_rate",
    "bounding_box_iou",
    "confidence_threshold",
    "field_detection_accuracy",
    # Text Similarity Metrics (Basic)
    "similarity_exact_match",
    "case_insensitive_match",
    "normalized_match",
    "sequence_similarity",
    "word_overlap",
    "contains_match",
    "length_similarity",
    # Advanced Similarity Metrics (Industry Standard)
    "bleu_score",
    "rouge_n",
    "rouge_l",
    "jaro_winkler_similarity",
    "dice_coefficient",
    "token_f1_score",
    "cosine_similarity_tfidf",
]
