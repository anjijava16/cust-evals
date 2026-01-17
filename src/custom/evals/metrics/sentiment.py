"""Sentiment analysis evaluation metric."""

from typing import Literal

from ..evaluators import Score, create_evaluator


def _simple_sentiment_analyzer(text: str) -> tuple[float, Literal["positive", "negative", "neutral"]]:
    """Simple sentiment analyzer based on keyword matching.

    This is a basic POC implementation. In production, you'd use a proper
    sentiment analysis library like TextBlob, VADER, or an LLM.

    Args:
        text: Text to analyze

    Returns:
        Tuple of (score, label) where score is 0.0-1.0 and label is sentiment category
    """
    text_lower = text.lower()

    # Simple keyword-based sentiment
    positive_words = ["good", "great", "excellent", "amazing", "love", "wonderful", "fantastic"]
    negative_words = ["bad", "terrible", "awful", "hate", "horrible", "poor", "worst"]

    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    if positive_count > negative_count:
        # Normalize score between 0.6 and 1.0 for positive sentiment
        score = 0.6 + (0.4 * min(positive_count / 3, 1.0))
        label = "positive"
    elif negative_count > positive_count:
        # Normalize score between 0.0 and 0.4 for negative sentiment
        score = 0.4 - (0.4 * min(negative_count / 3, 1.0))
        label = "negative"
    else:
        # Neutral sentiment
        score = 0.5
        label = "neutral"

    return score, label


@create_evaluator(name="sentiment", kind="code", direction="maximize")
def sentiment_score(text: str) -> Score:
    """Evaluate the sentiment of text.

    Returns a score between 0.0 (very negative) and 1.0 (very positive).

    Note: This is a simple POC implementation using keyword matching.
    In production, you'd use a proper sentiment analysis model.

    Args:
        text: The text to analyze

    Returns:
        Score: A Score object with sentiment score and label

    Examples:
        >>> eval_input = {"text": "I love this product! It's amazing!"}
        >>> score = sentiment_score(eval_input)
        >>> print(score)
        Score(score=0.8, name='sentiment', label='positive', ...)

        >>> eval_input = {"text": "This is terrible and awful."}
        >>> score = sentiment_score(eval_input)
        >>> print(score)
        Score(score=0.13, name='sentiment', label='negative', ...)

        >>> eval_input = {"text": "The product arrived on time."}
        >>> score = sentiment_score(eval_input)
        >>> print(score)
        Score(score=0.5, name='sentiment', label='neutral', ...)
    """
    score_value, sentiment_label = _simple_sentiment_analyzer(text)

    return Score(
        score=score_value,
        label=sentiment_label,
        explanation=f"Text has {sentiment_label} sentiment",
        metadata={"method": "keyword_matching"}
    )
