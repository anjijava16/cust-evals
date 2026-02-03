# Similarity Metrics Quick Reference

Quick reference for using the 7 text similarity metrics for non-LLM evaluation.

## Import

```python
from custom.evals.metrics import (
    similarity_exact_match,
    case_insensitive_match,
    normalized_match,
    sequence_similarity,
    word_overlap,
    contains_match,
    length_similarity
)
```

## Basic Usage

All metrics accept an evaluation input dictionary with `output` and `expected` fields:

```python
eval_input = {
    "output": "Your generated text",
    "expected": "Ground truth text"
}

score = similarity_exact_match(eval_input)
print(f"Score: {score.score:.2%} ({score.label})")
```

---

## Metrics Cheat Sheet

### 1. `similarity_exact_match`
**Purpose:** Exact character-for-character matching
**Returns:** 1.0 or 0.0
**Use when:** You need perfect string matching

```python
similarity_exact_match({"output": "Hello", "expected": "Hello"})
# → 1.0 (match)

similarity_exact_match({"output": "Hello", "expected": "hello"})
# → 0.0 (no_match)
```

---

### 2. `case_insensitive_match`
**Purpose:** Matching ignoring case
**Returns:** 1.0 or 0.0
**Use when:** Case differences don't matter

```python
case_insensitive_match({"output": "Hello", "expected": "hello"})
# → 1.0 (match)

case_insensitive_match({"output": "Hello World", "expected": "hello world"})
# → 1.0 (match)
```

---

### 3. `normalized_match`
**Purpose:** Matching after removing punctuation and normalizing whitespace
**Returns:** 1.0 or 0.0
**Use when:** You want to ignore formatting differences

```python
normalized_match({"output": "Hello,  World!!!", "expected": "hello world"})
# → 1.0 (match)

# Normalization: lowercase, strip, remove punctuation, normalize whitespace
normalized_match({"output": "A-B-C", "expected": "a b c"})
# → 1.0 (match, both normalize to "a b c")
```

---

### 4. `sequence_similarity`
**Purpose:** Fuzzy matching with similarity ratio
**Returns:** 0.0 - 1.0
**Use when:** You need a similarity score for near-matches

```python
sequence_similarity({
    "output": "The quick brown fox",
    "expected": "The quick brown dog",
    "threshold": 0.8  # Optional
})
# → ~0.85 (good)

# Uses difflib.SequenceMatcher under the hood
```

**Parameters:**
- `threshold` (default: 0.8) - Minimum similarity to pass

**Labels:** excellent (≥95%), good (≥85%), acceptable (≥70%), poor (<70%)

---

### 5. `word_overlap`
**Purpose:** Jaccard similarity at word level
**Returns:** 0.0 - 1.0
**Use when:** You want to measure shared vocabulary

```python
word_overlap({
    "output": "Python is great for data science",
    "expected": "Python is used for machine learning",
    "threshold": 0.7  # Optional
})
# → ~0.43 (poor)
# Common words: ["python", "is", "for"]

# Access metadata for details
score = word_overlap(eval_input)
print(score.metadata['common_words'])     # Shared words
print(score.metadata['missing_words'])    # In expected, not in output
print(score.metadata['extra_words'])      # In output, not in expected
```

**Parameters:**
- `threshold` (default: 0.7) - Minimum overlap to pass

**Formula:** `|A ∩ B| / |A ∪ B|`

---

### 6. `contains_match`
**Purpose:** Check if one text contains the other
**Returns:** 1.0 or 0.0
**Use when:** You need partial/substring matching

```python
contains_match({
    "output": "Python is a programming language",
    "expected": "programming language",
    "case_sensitive": False  # Optional
})
# → 1.0 (contains)
# Direction: "output contains expected"

# Bidirectional check
contains_match({
    "output": "Python",
    "expected": "Python is great"
})
# → 1.0 (contains)
# Direction: "expected contains output"
```

**Parameters:**
- `case_sensitive` (default: False) - Whether to match case

---

### 7. `length_similarity`
**Purpose:** Compare text lengths
**Returns:** 0.0 - 1.0
**Use when:** You want to detect truncation/verbosity

```python
length_similarity({
    "output": "Hello World",  # 11 chars
    "expected": "Hello",       # 5 chars
    "threshold": 0.8  # Optional
})
# → ~0.45 (poor)
# Difference: 6 chars

# Use metadata for details
score = length_similarity(eval_input)
print(score.metadata['length_difference'])  # Absolute difference
print(score.metadata['output_length'])      # Output length
print(score.metadata['expected_length'])    # Expected length
```

**Parameters:**
- `threshold` (default: 0.8) - Minimum ratio to pass

**Formula:** `min(len_output, len_expected) / max(len_output, len_expected)`

---

## Common Usage Patterns

### Pattern 1: Strict Matching

```python
# Try increasingly lenient matching
score1 = similarity_exact_match(eval_input)
if score1.score == 1.0:
    print("Perfect match")
else:
    score2 = case_insensitive_match(eval_input)
    if score2.score == 1.0:
        print("Match (ignoring case)")
    else:
        score3 = normalized_match(eval_input)
        if score3.score == 1.0:
            print("Match (after normalization)")
        else:
            print("No match")
```

### Pattern 2: Fuzzy Similarity Search

```python
# Evaluate similarity for search/retrieval
eval_input = {
    "output": retrieved_document,
    "expected": query_text
}

seq_score = sequence_similarity(eval_input)
word_score = word_overlap(eval_input)

# Combined score (weighted average)
combined = (seq_score.score * 0.6) + (word_score.score * 0.4)

if combined >= 0.8:
    print("Highly relevant")
elif combined >= 0.5:
    print("Moderately relevant")
else:
    print("Not relevant")
```

### Pattern 3: Comprehensive Evaluation

```python
# Run all 7 metrics for complete assessment
def comprehensive_eval(output, expected):
    eval_input = {"output": output, "expected": expected}

    scores = {
        "exact": similarity_exact_match(eval_input),
        "case_ins": case_insensitive_match(eval_input),
        "normalized": normalized_match(eval_input),
        "sequence": sequence_similarity(eval_input),
        "word_overlap": word_overlap(eval_input),
        "contains": contains_match(eval_input),
        "length": length_similarity(eval_input)
    }

    # Weighted overall score
    weights = {
        "exact": 0.05,
        "case_ins": 0.05,
        "normalized": 0.10,
        "sequence": 0.35,
        "word_overlap": 0.25,
        "contains": 0.10,
        "length": 0.10
    }

    overall = sum(scores[k].score * weights[k] for k in weights)

    return scores, overall
```

### Pattern 4: Batch Processing

```python
import pandas as pd

data = [
    {"id": 1, "output": "text1", "expected": "ref1"},
    {"id": 2, "output": "text2", "expected": "ref2"},
    # ... more data
]

results = []

for item in data:
    eval_input = {
        "output": item["output"],
        "expected": item["expected"]
    }

    results.append({
        "id": item["id"],
        "sequence_sim": sequence_similarity(eval_input).score,
        "word_overlap": word_overlap(eval_input).score,
        "length_sim": length_similarity(eval_input).score
    })

df = pd.DataFrame(results)
print(f"Average sequence similarity: {df['sequence_sim'].mean():.2%}")
```

---

## Metric Selection Guide

| Scenario | Recommended Metrics |
|----------|---------------------|
| **Exact matching required** | `similarity_exact_match` → `case_insensitive_match` → `normalized_match` |
| **Fuzzy similarity** | `sequence_similarity` + `word_overlap` |
| **Partial/substring matching** | `contains_match` |
| **Detect truncation/verbosity** | `length_similarity` |
| **Search result ranking** | `sequence_similarity` (0.6) + `word_overlap` (0.4) |
| **General text comparison** | All 7 metrics with weighted average |

---

## Return Value Structure

All metrics return a `Score` object with:

```python
score = sequence_similarity(eval_input)

# Attributes
score.score          # Float 0.0-1.0 (main score)
score.name           # Metric name
score.label          # Human-readable label (e.g., "excellent", "good")
score.explanation    # Detailed explanation
score.direction      # "maximize" or "minimize"
score.kind           # "code"
score.metadata       # Dict with additional details
```

Example metadata access:

```python
# Word overlap metadata
score = word_overlap(eval_input)
print(score.metadata['common_words'])      # ['word1', 'word2']
print(score.metadata['missing_words'])     # ['word3']
print(score.metadata['jaccard_similarity']) # 0.75

# Sequence similarity metadata
score = sequence_similarity(eval_input)
print(score.metadata['similarity_ratio'])  # 0.85
print(score.metadata['passes_threshold'])  # True
```

---

## Performance Tips

1. **Use exact matching first** - Cheapest computation
2. **Skip unnecessary metrics** - Don't run all 7 if you only need 1-2
3. **Batch processing** - Process multiple items together
4. **Cache normalization** - If comparing same text multiple times

---

## Complete Example

```python
from custom.evals.metrics import (
    sequence_similarity,
    word_overlap,
    normalized_match
)

# Evaluate a model output
output = "The Python programming language is great for data science"
expected = "Python is a great language for data science tasks"

eval_input = {
    "output": output,
    "expected": expected
}

# Quick check: normalized match
norm_score = normalized_match(eval_input)
if norm_score.score == 1.0:
    print("✓ Exact match (after normalization)")
else:
    # Fuzzy evaluation
    seq_score = sequence_similarity(eval_input)
    word_score = word_overlap(eval_input)

    print(f"Sequence Similarity: {seq_score.score:.2%} ({seq_score.label})")
    print(f"Word Overlap:        {word_score.score:.2%} ({word_score.label})")

    # Combined assessment
    combined = (seq_score.score + word_score.score) / 2
    if combined >= 0.7:
        print(f"✓ Good match (combined: {combined:.2%})")
    else:
        print(f"✗ Poor match (combined: {combined:.2%})")
```

---

## See Also

- **Full Guide:** `/docs/NON_LLM_EVALUATION_GUIDE.md`
- **Examples:** `/examples/similarity_evaluation_example.py`
- **API Reference:** `/src/custom/evals/metrics/similarity_metrics.py`

---

## Quick Help

```bash
# Run comprehensive examples
python examples/similarity_evaluation_example.py

# Install dependencies
pip install -e .

# Import in your code
from custom.evals.metrics import sequence_similarity, word_overlap
```
