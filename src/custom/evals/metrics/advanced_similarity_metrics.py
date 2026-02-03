"""
Advanced Text Similarity Metrics for NON-LLM Evaluation.

This module provides industry-standard NLP metrics including:
- BLEU (machine translation)
- ROUGE (summarization)
- Jaro-Winkler (string matching)
- Dice Coefficient (n-gram similarity)
- F1/Precision/Recall (token-level)
- Cosine Similarity with TF-IDF
- Longest Common Subsequence
"""

from typing import Dict, Any, List, Set, Tuple
import re
from collections import Counter
import math
from ..evaluators import create_evaluator, Score


# ============================================================================
# BLEU Score (Bilingual Evaluation Understudy)
# ============================================================================

def compute_ngrams(tokens: List[str], n: int) -> Counter:
    """Compute n-grams from a list of tokens."""
    return Counter(tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1))


def compute_bleu_precision(candidate_ngrams: Counter, reference_ngrams: Counter) -> float:
    """Compute clipped precision for n-grams."""
    clipped_count = sum(min(candidate_ngrams[ng], reference_ngrams[ng])
                       for ng in candidate_ngrams)
    total_count = sum(candidate_ngrams.values())
    return clipped_count / total_count if total_count > 0 else 0.0


@create_evaluator(name="bleu_score", kind="code", direction="maximize")
def bleu_score(
    output: str,
    expected: str,
    max_n: int = 4,
    weights: List[float] = None
) -> Score:
    """
    Calculate BLEU score (Bilingual Evaluation Understudy).

    Industry-standard metric for machine translation and text generation.
    Measures n-gram precision with brevity penalty.

    Args:
        output: Generated/predicted text
        expected: Ground truth reference text
        max_n: Maximum n-gram size (default: 4)
        weights: Weights for each n-gram size (default: uniform)

    Returns:
        Score: BLEU score (0.0-1.0, higher is better)
    """
    if weights is None:
        weights = [1.0 / max_n] * max_n

    # Tokenize
    candidate_tokens = output.split()
    reference_tokens = expected.split()

    if not candidate_tokens or not reference_tokens:
        return Score(
            score=0.0,
            name="bleu_score",
            label="empty",
            explanation="Empty output or reference",
            direction="maximize",
            kind="code",
            metadata={"error": "empty_input"}
        )

    # Calculate n-gram precisions
    precisions = []
    for n in range(1, max_n + 1):
        cand_ngrams = compute_ngrams(candidate_tokens, n)
        ref_ngrams = compute_ngrams(reference_tokens, n)

        if sum(cand_ngrams.values()) == 0:
            precisions.append(0.0)
        else:
            precisions.append(compute_bleu_precision(cand_ngrams, ref_ngrams))

    # Calculate geometric mean of precisions
    if all(p > 0 for p in precisions):
        log_precision_sum = sum(w * math.log(p) for w, p in zip(weights, precisions))
        geometric_mean = math.exp(log_precision_sum)
    else:
        geometric_mean = 0.0

    # Apply brevity penalty
    candidate_length = len(candidate_tokens)
    reference_length = len(reference_tokens)

    if candidate_length > reference_length:
        brevity_penalty = 1.0
    else:
        brevity_penalty = math.exp(1 - reference_length / candidate_length) if candidate_length > 0 else 0.0

    bleu = brevity_penalty * geometric_mean

    label = "excellent" if bleu >= 0.7 else \
            "good" if bleu >= 0.5 else \
            "acceptable" if bleu >= 0.3 else \
            "poor"

    return Score(
        score=bleu,
        name="bleu_score",
        label=label,
        explanation=f"BLEU-{max_n}: {bleu:.2%} (BP: {brevity_penalty:.3f}). "
                   f"Candidate length: {candidate_length}, Reference: {reference_length}",
        direction="maximize",
        kind="code",
        metadata={
            "bleu_score": bleu,
            "brevity_penalty": brevity_penalty,
            "geometric_mean": geometric_mean,
            "precisions": {f"{n}-gram": p for n, p in enumerate(precisions, 1)},
            "candidate_length": candidate_length,
            "reference_length": reference_length
        }
    )


# ============================================================================
# ROUGE Scores (Recall-Oriented Understudy for Gisting Evaluation)
# ============================================================================

@create_evaluator(name="rouge_n", kind="code", direction="maximize")
def rouge_n(
    output: str,
    expected: str,
    n: int = 1
) -> Score:
    """
    Calculate ROUGE-N score (n-gram recall).

    Standard metric for summarization evaluation.
    Measures n-gram overlap with focus on recall.

    Args:
        output: Generated/predicted text
        expected: Ground truth reference text
        n: N-gram size (1 for unigrams, 2 for bigrams, etc.)

    Returns:
        Score: ROUGE-N F1 score (0.0-1.0)
    """
    # Tokenize
    candidate_tokens = output.split()
    reference_tokens = expected.split()

    if not reference_tokens:
        return Score(
            score=0.0,
            name=f"rouge_{n}",
            label="empty",
            explanation="Empty reference",
            direction="maximize",
            kind="code",
            metadata={"error": "empty_reference"}
        )

    # Compute n-grams
    cand_ngrams = compute_ngrams(candidate_tokens, n)
    ref_ngrams = compute_ngrams(reference_tokens, n)

    # Calculate overlap
    overlap = sum(min(cand_ngrams[ng], ref_ngrams[ng]) for ng in ref_ngrams)

    # Calculate precision, recall, F1
    precision = overlap / sum(cand_ngrams.values()) if cand_ngrams else 0.0
    recall = overlap / sum(ref_ngrams.values()) if ref_ngrams else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    label = "excellent" if f1 >= 0.7 else \
            "good" if f1 >= 0.5 else \
            "acceptable" if f1 >= 0.3 else \
            "poor"

    return Score(
        score=f1,
        name=f"rouge_{n}",
        label=label,
        explanation=f"ROUGE-{n} F1: {f1:.2%} (P: {precision:.2%}, R: {recall:.2%})",
        direction="maximize",
        kind="code",
        metadata={
            "f1": f1,
            "precision": precision,
            "recall": recall,
            "overlap_count": overlap,
            "candidate_ngram_count": sum(cand_ngrams.values()),
            "reference_ngram_count": sum(ref_ngrams.values())
        }
    )


def lcs_length(x: List[str], y: List[str]) -> int:
    """Calculate length of longest common subsequence."""
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i-1] == y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]


@create_evaluator(name="rouge_l", kind="code", direction="maximize")
def rouge_l(
    output: str,
    expected: str
) -> Score:
    """
    Calculate ROUGE-L score (Longest Common Subsequence).

    Measures longest common subsequence between texts.
    Captures sentence-level structure similarity.

    Args:
        output: Generated/predicted text
        expected: Ground truth reference text

    Returns:
        Score: ROUGE-L F1 score (0.0-1.0)
    """
    # Tokenize
    candidate_tokens = output.split()
    reference_tokens = expected.split()

    if not reference_tokens or not candidate_tokens:
        return Score(
            score=0.0,
            name="rouge_l",
            label="empty",
            explanation="Empty output or reference",
            direction="maximize",
            kind="code",
            metadata={"error": "empty_input"}
        )

    # Calculate LCS length
    lcs_len = lcs_length(candidate_tokens, reference_tokens)

    # Calculate precision, recall, F1
    precision = lcs_len / len(candidate_tokens)
    recall = lcs_len / len(reference_tokens)
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    label = "excellent" if f1 >= 0.7 else \
            "good" if f1 >= 0.5 else \
            "acceptable" if f1 >= 0.3 else \
            "poor"

    return Score(
        score=f1,
        name="rouge_l",
        label=label,
        explanation=f"ROUGE-L F1: {f1:.2%} (LCS length: {lcs_len}/{len(reference_tokens)} tokens)",
        direction="maximize",
        kind="code",
        metadata={
            "f1": f1,
            "precision": precision,
            "recall": recall,
            "lcs_length": lcs_len,
            "candidate_length": len(candidate_tokens),
            "reference_length": len(reference_tokens)
        }
    )


# ============================================================================
# Jaro-Winkler Distance
# ============================================================================

def jaro_similarity(s1: str, s2: str) -> float:
    """Calculate Jaro similarity between two strings."""
    if s1 == s2:
        return 1.0

    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0.0

    # Maximum distance for matches
    max_dist = max(len1, len2) // 2 - 1
    if max_dist < 1:
        max_dist = 1

    # Arrays to track matches
    s1_matches = [False] * len1
    s2_matches = [False] * len2

    matches = 0
    transpositions = 0

    # Find matches
    for i in range(len1):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len2)

        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = s2_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    # Count transpositions
    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    jaro = (matches / len1 + matches / len2 +
            (matches - transpositions / 2) / matches) / 3

    return jaro


@create_evaluator(name="jaro_winkler_similarity", kind="code", direction="maximize")
def jaro_winkler_similarity(
    output: str,
    expected: str,
    prefix_scale: float = 0.1,
    max_prefix_length: int = 4
) -> Score:
    """
    Calculate Jaro-Winkler similarity.

    Best for short strings (names, addresses, identifiers).
    Gives extra weight to matching prefixes.

    Args:
        output: Generated/predicted text
        expected: Ground truth text
        prefix_scale: Scaling factor for prefix bonus (default: 0.1)
        max_prefix_length: Maximum prefix length to consider (default: 4)

    Returns:
        Score: Jaro-Winkler similarity (0.0-1.0)
    """
    jaro = jaro_similarity(output, expected)

    # Calculate common prefix length (up to max_prefix_length)
    prefix_len = 0
    for i in range(min(len(output), len(expected), max_prefix_length)):
        if output[i] == expected[i]:
            prefix_len += 1
        else:
            break

    # Apply Winkler adjustment
    jw = jaro + (prefix_len * prefix_scale * (1 - jaro))

    label = "excellent" if jw >= 0.95 else \
            "good" if jw >= 0.85 else \
            "acceptable" if jw >= 0.70 else \
            "poor"

    return Score(
        score=jw,
        name="jaro_winkler_similarity",
        label=label,
        explanation=f"Jaro-Winkler: {jw:.2%} (Jaro: {jaro:.2%}, Prefix: {prefix_len} chars)",
        direction="maximize",
        kind="code",
        metadata={
            "jaro_winkler": jw,
            "jaro": jaro,
            "common_prefix_length": prefix_len,
            "prefix_scale": prefix_scale
        }
    )


# ============================================================================
# Dice Coefficient
# ============================================================================

@create_evaluator(name="dice_coefficient", kind="code", direction="maximize")
def dice_coefficient(
    output: str,
    expected: str,
    n: int = 2
) -> Score:
    """
    Calculate Dice coefficient (Sørensen-Dice) for n-grams.

    Alternative to Jaccard similarity, more lenient with partial matches.
    Formula: 2|A ∩ B| / (|A| + |B|)

    Args:
        output: Generated/predicted text
        expected: Ground truth text
        n: N-gram size (2 for bigrams, 1 for words)

    Returns:
        Score: Dice coefficient (0.0-1.0)
    """
    def get_ngrams(text: str, n: int) -> Set[str]:
        """Extract character n-grams."""
        if n == 1:
            # Word-level
            return set(text.lower().split())
        else:
            # Character n-grams
            text = text.lower()
            return set(text[i:i+n] for i in range(len(text) - n + 1))

    output_ngrams = get_ngrams(output, n)
    expected_ngrams = get_ngrams(expected, n)

    if not output_ngrams and not expected_ngrams:
        dice = 1.0
    elif not output_ngrams or not expected_ngrams:
        dice = 0.0
    else:
        intersection = len(output_ngrams & expected_ngrams)
        dice = (2 * intersection) / (len(output_ngrams) + len(expected_ngrams))

    label = "excellent" if dice >= 0.9 else \
            "good" if dice >= 0.75 else \
            "acceptable" if dice >= 0.6 else \
            "poor"

    ngram_type = "word" if n == 1 else f"{n}-gram"

    return Score(
        score=dice,
        name="dice_coefficient",
        label=label,
        explanation=f"Dice ({ngram_type}): {dice:.2%} "
                   f"({len(output_ngrams & expected_ngrams)} common / "
                   f"{len(output_ngrams) + len(expected_ngrams)} total)",
        direction="maximize",
        kind="code",
        metadata={
            "dice_coefficient": dice,
            "n": n,
            "intersection_count": len(output_ngrams & expected_ngrams) if output_ngrams and expected_ngrams else 0,
            "output_ngram_count": len(output_ngrams),
            "expected_ngram_count": len(expected_ngrams)
        }
    )


# ============================================================================
# Token-Level Metrics (Precision, Recall, F1)
# ============================================================================

@create_evaluator(name="token_f1_score", kind="code", direction="maximize")
def token_f1_score(
    output: str,
    expected: str,
    case_sensitive: bool = False
) -> Score:
    """
    Calculate token-level F1 score (harmonic mean of precision and recall).

    Measures how well output tokens match expected tokens.
    Useful for classification, NER, and extraction tasks.

    Args:
        output: Generated/predicted text
        expected: Ground truth text
        case_sensitive: Whether to consider case (default: False)

    Returns:
        Score: F1 score (0.0-1.0)
    """
    def tokenize(text: str) -> Set[str]:
        tokens = text.split()
        if not case_sensitive:
            tokens = [t.lower() for t in tokens]
        return set(tokens)

    output_tokens = tokenize(output)
    expected_tokens = tokenize(expected)

    if not expected_tokens and not output_tokens:
        precision = recall = f1 = 1.0
    elif not expected_tokens or not output_tokens:
        precision = recall = f1 = 0.0
    else:
        true_positives = len(output_tokens & expected_tokens)
        false_positives = len(output_tokens - expected_tokens)
        false_negatives = len(expected_tokens - output_tokens)

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    label = "excellent" if f1 >= 0.9 else \
            "good" if f1 >= 0.75 else \
            "acceptable" if f1 >= 0.6 else \
            "poor"

    return Score(
        score=f1,
        name="token_f1_score",
        label=label,
        explanation=f"Token F1: {f1:.2%} (P: {precision:.2%}, R: {recall:.2%})",
        direction="maximize",
        kind="code",
        metadata={
            "f1_score": f1,
            "precision": precision,
            "recall": recall,
            "true_positives": len(output_tokens & expected_tokens) if output_tokens and expected_tokens else 0,
            "false_positives": len(output_tokens - expected_tokens) if output_tokens and expected_tokens else 0,
            "false_negatives": len(expected_tokens - output_tokens) if output_tokens and expected_tokens else 0,
            "common_tokens": list(output_tokens & expected_tokens) if output_tokens and expected_tokens else [],
            "missing_tokens": list(expected_tokens - output_tokens) if expected_tokens and output_tokens else [],
            "extra_tokens": list(output_tokens - expected_tokens) if output_tokens and expected_tokens else []
        }
    )


# ============================================================================
# Cosine Similarity with TF-IDF
# ============================================================================

@create_evaluator(name="cosine_similarity_tfidf", kind="code", direction="maximize")
def cosine_similarity_tfidf(
    output: str,
    expected: str
) -> Score:
    """
    Calculate cosine similarity using TF-IDF vectors.

    Document-level semantic similarity without requiring ML models.
    Useful for longer texts and document comparison.

    Args:
        output: Generated/predicted text
        expected: Ground truth text

    Returns:
        Score: Cosine similarity (0.0-1.0)
    """
    def tokenize(text: str) -> List[str]:
        return text.lower().split()

    output_tokens = tokenize(output)
    expected_tokens = tokenize(expected)

    if not output_tokens or not expected_tokens:
        return Score(
            score=0.0,
            name="cosine_similarity_tfidf",
            label="empty",
            explanation="Empty output or reference",
            direction="maximize",
            kind="code",
            metadata={"error": "empty_input"}
        )

    # Build vocabulary
    vocab = set(output_tokens + expected_tokens)

    # Calculate term frequencies
    output_tf = Counter(output_tokens)
    expected_tf = Counter(expected_tokens)

    # Calculate IDF (simple version with just these two documents)
    doc_count = 2
    idf = {}
    for term in vocab:
        docs_with_term = (1 if term in output_tf else 0) + (1 if term in expected_tf else 0)
        idf[term] = math.log(doc_count / docs_with_term)

    # Calculate TF-IDF vectors
    output_tfidf = {term: output_tf.get(term, 0) * idf[term] for term in vocab}
    expected_tfidf = {term: expected_tf.get(term, 0) * idf[term] for term in vocab}

    # Calculate cosine similarity
    dot_product = sum(output_tfidf[term] * expected_tfidf[term] for term in vocab)
    output_magnitude = math.sqrt(sum(val ** 2 for val in output_tfidf.values()))
    expected_magnitude = math.sqrt(sum(val ** 2 for val in expected_tfidf.values()))

    if output_magnitude == 0 or expected_magnitude == 0:
        cosine_sim = 0.0
    else:
        cosine_sim = dot_product / (output_magnitude * expected_magnitude)

    label = "excellent" if cosine_sim >= 0.9 else \
            "good" if cosine_sim >= 0.75 else \
            "acceptable" if cosine_sim >= 0.6 else \
            "poor"

    return Score(
        score=cosine_sim,
        name="cosine_similarity_tfidf",
        label=label,
        explanation=f"Cosine similarity (TF-IDF): {cosine_sim:.2%}. "
                   f"Vocabulary: {len(vocab)} terms",
        direction="maximize",
        kind="code",
        metadata={
            "cosine_similarity": cosine_sim,
            "vocabulary_size": len(vocab),
            "output_unique_terms": len(set(output_tokens)),
            "expected_unique_terms": len(set(expected_tokens))
        }
    )
