# Advanced Similarity Metrics Guide

## Overview

This guide covers 7 industry-standard NLP metrics for comprehensive NON-LLM evaluation:

1. **BLEU** - Machine translation standard
2. **ROUGE-N** - Summarization (n-gram recall)
3. **ROUGE-L** - Summarization (LCS-based)
4. **Jaro-Winkler** - Name/entity matching
5. **Dice Coefficient** - N-gram similarity
6. **Token F1 Score** - Precision/recall balance
7. **Cosine Similarity (TF-IDF)** - Document comparison

All metrics are deterministic (no ML models required) and return standardized `Score` objects.

---

## 1. BLEU Score

**Purpose:** Evaluate machine translation and text generation quality
**Metric:** N-gram precision with brevity penalty
**Range:** 0.0-1.0 (higher is better)
**Best for:** Translation, paraphrasing, generation tasks

### Usage

```python
from custom.evals.metrics import bleu_score

eval_input = {
    "output": "The cat sits on the mat",
    "expected": "The cat is on the mat",
    "max_n": 4,  # Optional: max n-gram size (default: 4)
    "weights": [0.25, 0.25, 0.25, 0.25]  # Optional: n-gram weights
}

score = bleu_score(eval_input)
print(f"BLEU: {score.score:.2%} ({score.label})")
print(f"Brevity Penalty: {score.metadata['brevity_penalty']}")
print(f"1-gram precision: {score.metadata['precisions']['1-gram']:.2%}")
```

### How It Works

1. **Tokenizes** text into words
2. **Calculates n-gram precision** for 1-gram through 4-gram (default)
3. **Applies clipping** to prevent over-counting repeated n-grams
4. **Computes geometric mean** of precisions
5. **Applies brevity penalty** if output is shorter than reference

**Formula:**
```
BLEU = BP × exp(Σ wₙ log pₙ)

BP = 1 if len(output) > len(reference)
BP = exp(1 - len(reference)/len(output)) otherwise
```

### Interpretation

| Score | Label | Meaning |
|-------|-------|---------|
| ≥ 0.7 | excellent | Very high quality translation |
| ≥ 0.5 | good | Adequate translation |
| ≥ 0.3 | acceptable | Partially correct |
| < 0.3 | poor | Low quality |

---

## 2. ROUGE-N (N-gram Recall)

**Purpose:** Evaluate summarization quality with n-gram recall
**Metric:** N-gram overlap (F1 score)
**Range:** 0.0-1.0 (higher is better)
**Best for:** Summarization, content coverage

### Usage

```python
from custom.evals.metrics import rouge_n

# ROUGE-1 (unigrams)
eval_input_1 = {
    "output": "Machine learning is a subset of AI",
    "expected": "Machine learning is a subset of artificial intelligence",
    "n": 1
}
score1 = rouge_n(eval_input_1)

# ROUGE-2 (bigrams)
eval_input_2 = {**eval_input_1, "n": 2}
score2 = rouge_n(eval_input_2)

print(f"ROUGE-1: {score1.score:.2%} (P: {score1.metadata['precision']:.2%}, "
      f"R: {score1.metadata['recall']:.2%})")
print(f"ROUGE-2: {score2.score:.2%}")
```

### How It Works

1. **Tokenizes** text into words
2. **Generates n-grams** (size = n)
3. **Counts overlapping n-grams** between output and reference
4. **Calculates precision, recall, and F1**

**Formula:**
```
Recall = overlap_count / reference_ngram_count
Precision = overlap_count / candidate_ngram_count
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

### Interpretation

- **ROUGE-1**: Measures word-level content coverage
- **ROUGE-2**: Measures bigram fluency and coherence
- Higher recall = better content coverage
- Higher precision = less redundancy

---

## 3. ROUGE-L (Longest Common Subsequence)

**Purpose:** Evaluate sentence-level structure similarity
**Metric:** LCS-based F1 score
**Range:** 0.0-1.0 (higher is better)
**Best for:** Capturing sentence structure, word order

### Usage

```python
from custom.evals.metrics import rouge_l

eval_input = {
    "output": "Machine learning is a subset of AI",
    "expected": "Machine learning is a subset of artificial intelligence"
}

score = rouge_l(eval_input)
print(f"ROUGE-L: {score.score:.2%}")
print(f"LCS length: {score.metadata['lcs_length']} tokens")
```

### How It Works

1. **Tokenizes** text into words
2. **Finds longest common subsequence** (LCS) between texts
3. **Calculates precision and recall** based on LCS length
4. **Computes F1 score**

**Advantages over ROUGE-N:**
- Captures word order without requiring consecutive matches
- More flexible than fixed n-grams
- Better for longer texts

---

## 4. Jaro-Winkler Similarity

**Purpose:** Match short strings (names, identifiers, addresses)
**Metric:** String similarity with prefix bonus
**Range:** 0.0-1.0 (higher is better)
**Best for:** Entity matching, name deduplication, record linkage

### Usage

```python
from custom.evals.metrics import jaro_winkler_similarity

eval_input = {
    "output": "Steven Johnson",
    "expected": "Stephen Jonson",
    "prefix_scale": 0.1,  # Optional (default: 0.1)
    "max_prefix_length": 4  # Optional (default: 4)
}

score = jaro_winkler_similarity(eval_input)
print(f"Similarity: {score.score:.2%} ({score.label})")
print(f"Common prefix: {score.metadata['common_prefix_length']} chars")
```

### How It Works

1. **Calculates Jaro similarity** (accounts for character matches and transpositions)
2. **Identifies common prefix** (up to max_prefix_length)
3. **Applies prefix bonus** (gives extra weight to matching prefixes)

**Formula:**
```
Jaro-Winkler = Jaro + (prefix_length × prefix_scale × (1 - Jaro))
```

### When to Use

✓ **Perfect for:**
- Name matching (first names, last names)
- Address matching
- Short identifiers (product codes, IDs)
- Record deduplication

✗ **Not ideal for:**
- Long texts or documents
- Word order matters
- Semantic similarity

---

## 5. Dice Coefficient

**Purpose:** Measure n-gram similarity (alternative to Jaccard)
**Metric:** 2|A ∩ B| / (|A| + |B|)
**Range:** 0.0-1.0 (higher is better)
**Best for:** Fuzzy string matching, typo tolerance

### Usage

```python
from custom.evals.metrics import dice_coefficient

# Word-level Dice
eval_input_words = {
    "output": "The quick brown fox",
    "expected": "The quick brown dog",
    "n": 1  # 1 = word-level, 2+ = character n-grams
}
score1 = dice_coefficient(eval_input_words)

# Character bigram Dice
eval_input_bigrams = {
    "output": "Hello World",
    "expected": "Hello Word",
    "n": 2
}
score2 = dice_coefficient(eval_input_bigrams)

print(f"Word Dice: {score1.score:.2%}")
print(f"Bigram Dice: {score2.score:.2%}")
```

### How It Works

1. **Extracts n-grams** (words if n=1, character n-grams otherwise)
2. **Counts intersection** and total n-grams
3. **Applies Dice formula** (more lenient than Jaccard)

**Dice vs Jaccard:**
- Dice: 2|A∩B| / (|A|+|B|) - weights common elements more
- Jaccard: |A∩B| / |A∪B| - stricter similarity measure
- Dice typically gives higher scores for same inputs

---

## 6. Token F1 Score

**Purpose:** Measure token-level precision and recall
**Metric:** Harmonic mean of precision and recall
**Range:** 0.0-1.0 (higher is better)
**Best for:** Classification, NER, keyword extraction, entity detection

### Usage

```python
from custom.evals.metrics import token_f1_score

eval_input = {
    "output": "machine learning deep learning AI",
    "expected": "machine learning AI data science",
    "case_sensitive": False  # Optional (default: False)
}

score = token_f1_score(eval_input)
print(f"F1: {score.score:.2%} (P: {score.metadata['precision']:.2%}, "
      f"R: {score.metadata['recall']:.2%})")
print(f"Common tokens: {score.metadata['common_tokens']}")
print(f"Missing tokens: {score.metadata['missing_tokens']}")
print(f"Extra tokens: {score.metadata['extra_tokens']}")
```

### How It Works

1. **Tokenizes** text into words
2. **Computes token sets**
3. **Calculates true positives, false positives, false negatives**
4. **Computes precision, recall, and F1**

**Formula:**
```
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

### Use Cases

- **NER evaluation**: Did the model extract the right entities?
- **Keyword extraction**: Are the right keywords identified?
- **Classification labels**: Are the correct labels predicted?
- **Diagnostic analysis**: See exactly which tokens are missing or extra

---

## 7. Cosine Similarity (TF-IDF)

**Purpose:** Document-level semantic similarity
**Metric:** Cosine of angle between TF-IDF vectors
**Range:** 0.0-1.0 (higher is better)
**Best for:** Document similarity, topic matching

### Usage

```python
from custom.evals.metrics import cosine_similarity_tfidf

eval_input = {
    "output": "Machine learning automates analytical model building",
    "expected": "Machine learning is a method of data analysis"
}

score = cosine_similarity_tfidf(eval_input)
print(f"Cosine Similarity: {score.score:.2%}")
print(f"Vocabulary: {score.metadata['vocabulary_size']} terms")
```

### How It Works

1. **Tokenizes** text into words
2. **Calculates term frequencies** (TF)
3. **Computes inverse document frequency** (IDF)
4. **Creates TF-IDF vectors**
5. **Calculates cosine similarity**

**Formula:**
```
Cosine = (A · B) / (||A|| × ||B||)
```

**Note:** With only 2 documents, IDF calculation is limited. For more robust results, use with multiple documents or consider simpler metrics.

---

## Metric Selection Guide

| Task | Primary Metric | Secondary Metrics |
|------|---------------|-------------------|
| **Machine Translation** | BLEU | ROUGE-1, Token F1 |
| **Summarization** | ROUGE-1, ROUGE-2, ROUGE-L | BLEU |
| **Name Matching** | Jaro-Winkler | Dice (bigrams) |
| **Entity Extraction** | Token F1 | ROUGE-1 |
| **Keyword Extraction** | Token F1 | Dice (words) |
| **Document Similarity** | Cosine (TF-IDF) | ROUGE-L |
| **Paraphrasing** | BLEU | ROUGE-L, Dice |
| **Fuzzy String Match** | Jaro-Winkler, Dice | - |

---

## Complete Example

```python
from custom.evals.metrics import (
    bleu_score,
    rouge_n,
    rouge_l,
    jaro_winkler_similarity,
    dice_coefficient,
    token_f1_score,
    cosine_similarity_tfidf
)

# Your data
output = "Machine learning is a subset of AI"
expected = "Machine learning is a subset of artificial intelligence"

eval_input = {"output": output, "expected": expected}

# Run comprehensive evaluation
results = {
    "BLEU": bleu_score(eval_input),
    "ROUGE-1": rouge_n({**eval_input, "n": 1}),
    "ROUGE-2": rouge_n({**eval_input, "n": 2}),
    "ROUGE-L": rouge_l(eval_input),
    "Jaro-Winkler": jaro_winkler_similarity(eval_input),
    "Dice": dice_coefficient({**eval_input, "n": 1}),
    "Token F1": token_f1_score(eval_input),
    "Cosine": cosine_similarity_tfidf(eval_input)
}

# Print results
for metric_name, score in results.items():
    print(f"{metric_name}: {score.score:.2%} ({score.label})")

# Calculate weighted average
weights = {"BLEU": 0.2, "ROUGE-1": 0.2, "ROUGE-L": 0.2,
           "Token F1": 0.2, "Dice": 0.2}
overall = sum(results[k].score * weights[k] for k in weights)
print(f"\nOverall Score: {overall:.2%}")
```

---

## Metric Comparison

| Metric | Focus | Granularity | Word Order | Speed |
|--------|-------|-------------|------------|-------|
| BLEU | Precision | N-grams | Yes | Fast |
| ROUGE-N | Recall | N-grams | Yes | Fast |
| ROUGE-L | Structure | Sequence | Yes | Medium |
| Jaro-Winkler | Characters | Chars | Partial | Fast |
| Dice | Similarity | N-grams | No | Fast |
| Token F1 | Balance | Tokens | No | Fast |
| Cosine (TF-IDF) | Semantics | Terms | No | Medium |

---

## Best Practices

### 1. Choose Multiple Metrics

Don't rely on a single metric - combine several for comprehensive evaluation:

```python
# Translation evaluation
translation_metrics = [bleu_score, rouge_l, token_f1_score]

# Summarization evaluation
summary_metrics = [rouge_n (n=1), rouge_n (n=2), rouge_l]

# Entity matching
entity_metrics = [jaro_winkler_similarity, dice_coefficient]
```

### 2. Understand Metric Biases

- **BLEU**: Favors shorter outputs (brevity penalty)
- **ROUGE**: Favors longer outputs (recall-oriented)
- **Token F1**: Balanced but ignores order
- **Jaro-Winkler**: Best for short strings only

### 3. Set Appropriate Thresholds

```python
# Different tasks need different thresholds
if use_case == "translation":
    threshold = 0.5  # BLEU ≥ 0.5 is good
elif use_case == "summarization":
    threshold = 0.3  # ROUGE ≥ 0.3 is acceptable
elif use_case == "name_matching":
    threshold = 0.85  # Jaro-Winkler ≥ 0.85 is good match
```

### 4. Use Metadata for Debugging

```python
score = token_f1_score(eval_input)

if score.score < 0.7:
    print(f"Missing tokens: {score.metadata['missing_tokens']}")
    print(f"Extra tokens: {score.metadata['extra_tokens']}")
    # Analyze what went wrong
```

---

## Examples

See `/examples/advanced_similarity_example.py` for 8 comprehensive examples:

1. BLEU score for translation
2. ROUGE scores for summarization
3. Jaro-Winkler for name matching
4. Dice coefficient for n-gram similarity
5. Token F1 for precision/recall
6. Cosine similarity for documents
7. Comprehensive comparison
8. Real-world use case scenarios

Run: `python examples/advanced_similarity_example.py`

---

## Summary

**20 Total Metrics Available:**

- 6 OCR/Document Extraction metrics
- 7 Basic Similarity metrics
- 7 Advanced Industry-Standard metrics

All metrics are:
- ✅ Deterministic (no randomness)
- ✅ Code-based (no ML models)
- ✅ Fast and efficient
- ✅ Standardized Score output
- ✅ Rich metadata for debugging

Perfect for NON-LLM evaluation tasks!
