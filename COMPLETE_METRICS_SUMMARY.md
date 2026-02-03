# Complete Metrics Summary - NON-LLM Evaluation Framework

## 🎯 Total: 20 Metrics Available

The `cust-evals` framework now provides **20 comprehensive metrics** for NON-LLM evaluation, covering all major use cases for comparing output against ground truth.

---

## 📊 Metric Categories

### 1. OCR/Document Extraction Metrics (6 metrics)

Perfect for evaluating AWS Textract, Google Cloud Vision, Azure Form Recognizer, etc.

| # | Metric | Purpose | Returns |
|---|--------|---------|---------|
| 1 | `text_extraction_accuracy` | Overall text quality | 0.0-1.0 |
| 2 | `character_error_rate` | Character-level precision | 0.0-1.0 |
| 3 | `word_error_rate` | Word-level accuracy | 0.0-1.0 |
| 4 | `bounding_box_iou` | Spatial accuracy (IoU) | 0.0-1.0 |
| 5 | `confidence_threshold` | Quality filtering | 1.0 or 0.0 |
| 6 | `field_detection_accuracy` | Form field detection (F1) | 0.0-1.0 |

**Documentation:** `/docs/NON_LLM_EVALUATION_GUIDE.md` (lines 88-252)

---

### 2. Basic Text Similarity Metrics (7 metrics)

General-purpose text comparison for any use case.

| # | Metric | Purpose | Returns |
|---|--------|---------|---------|
| 7 | `similarity_exact_match` | Exact string matching | 1.0 or 0.0 |
| 8 | `case_insensitive_match` | Case-insensitive matching | 1.0 or 0.0 |
| 9 | `normalized_match` | Normalized matching | 1.0 or 0.0 |
| 10 | `sequence_similarity` | Fuzzy similarity (SequenceMatcher) | 0.0-1.0 |
| 11 | `word_overlap` | Jaccard word similarity | 0.0-1.0 |
| 12 | `contains_match` | Substring/containment check | 1.0 or 0.0 |
| 13 | `length_similarity` | Text length comparison | 0.0-1.0 |

**Documentation:** `/docs/NON_LLM_EVALUATION_GUIDE.md` (lines 254-436)
**Quick Reference:** `/docs/SIMILARITY_METRICS_QUICKSTART.md`

---

### 3. Advanced Industry-Standard Metrics (7 metrics)

Professional NLP metrics used in research and production.

| # | Metric | Purpose | Returns |
|---|--------|---------|---------|
| 14 | `bleu_score` | Machine translation (n-gram precision) | 0.0-1.0 |
| 15 | `rouge_n` | Summarization (n-gram recall) | 0.0-1.0 |
| 16 | `rouge_l` | Summarization (LCS-based) | 0.0-1.0 |
| 17 | `jaro_winkler_similarity` | Name/entity matching | 0.0-1.0 |
| 18 | `dice_coefficient` | N-gram similarity | 0.0-1.0 |
| 19 | `token_f1_score` | Token precision/recall | 0.0-1.0 |
| 20 | `cosine_similarity_tfidf` | Document similarity | 0.0-1.0 |

**Documentation:** `/docs/ADVANCED_METRICS_GUIDE.md`

---

## 🚀 Quick Start

### Installation

```bash
pip install -e .
```

### Basic Usage

```python
from custom.evals.metrics import sequence_similarity, word_overlap

# Your data
eval_input = {
    "output": "Your system's output",
    "expected": "Ground truth data"
}

# Evaluate
score = sequence_similarity(eval_input)
print(f"Similarity: {score.score:.2%} ({score.label})")
```

### Import All Metrics

```python
# OCR Metrics
from custom.evals.metrics import (
    text_extraction_accuracy,
    character_error_rate,
    word_error_rate,
    bounding_box_iou,
    confidence_threshold,
    field_detection_accuracy
)

# Basic Similarity Metrics
from custom.evals.metrics import (
    similarity_exact_match,
    case_insensitive_match,
    normalized_match,
    sequence_similarity,
    word_overlap,
    contains_match,
    length_similarity
)

# Advanced Metrics
from custom.evals.metrics import (
    bleu_score,
    rouge_n,
    rouge_l,
    jaro_winkler_similarity,
    dice_coefficient,
    token_f1_score,
    cosine_similarity_tfidf
)
```

---

## 📚 Use Case Guide

### Use Case 1: OCR/Document Extraction

```python
# Evaluate AWS Textract output
from custom.evals.metrics import (
    text_extraction_accuracy,
    character_error_rate,
    bounding_box_iou
)

eval_input = {
    "output": textract_output_text,
    "expected": ground_truth_text
}

text_acc = text_extraction_accuracy(eval_input)
cer = character_error_rate(eval_input)

print(f"Text Accuracy: {text_acc.score:.2%}")
print(f"CER: {cer.metadata['raw_cer']:.2%}")
```

**Documentation:** `/docs/NON_LLM_EVALUATION_GUIDE.md` - Section "AWS Textract Integration"

---

### Use Case 2: Similarity Search Evaluation

```python
# Rank search results by relevance
from custom.evals.metrics import sequence_similarity, word_overlap

def rank_search_results(query, ground_truth, search_results):
    ranked = []
    for result in search_results:
        eval_input = {"output": result, "expected": ground_truth}

        seq_score = sequence_similarity(eval_input)
        word_score = word_overlap(eval_input)

        # Weighted combination
        combined = (seq_score.score * 0.6) + (word_score.score * 0.4)
        ranked.append({"text": result, "score": combined})

    return sorted(ranked, key=lambda x: x["score"], reverse=True)
```

**Examples:** `/examples/similarity_evaluation_example.py` - Example 5

---

### Use Case 3: Machine Translation Evaluation

```python
# Evaluate translation quality
from custom.evals.metrics import bleu_score, rouge_l

eval_input = {
    "output": translated_text,
    "expected": reference_translation
}

bleu = bleu_score(eval_input)
rougel = rouge_l(eval_input)

print(f"BLEU: {bleu.score:.2%} ({bleu.label})")
print(f"ROUGE-L: {rougel.score:.2%}")

# BLEU ≥ 0.5 is good quality
# BLEU ≥ 0.7 is excellent quality
```

**Examples:** `/examples/advanced_similarity_example.py` - Example 1

---

### Use Case 4: Text Summarization Evaluation

```python
# Evaluate summary quality
from custom.evals.metrics import rouge_n, rouge_l

eval_input = {
    "output": generated_summary,
    "expected": reference_summary
}

rouge1 = rouge_n({**eval_input, "n": 1})
rouge2 = rouge_n({**eval_input, "n": 2})
rougel = rouge_l(eval_input)

print(f"ROUGE-1: {rouge1.score:.2%} (content coverage)")
print(f"ROUGE-2: {rouge2.score:.2%} (fluency)")
print(f"ROUGE-L: {rougel.score:.2%} (structure)")
```

**Examples:** `/examples/advanced_similarity_example.py` - Example 2

---

### Use Case 5: Name/Entity Matching

```python
# Match similar names or entities
from custom.evals.metrics import jaro_winkler_similarity

eval_input = {
    "output": "Steven Johnson",
    "expected": "Stephen Jonson"
}

score = jaro_winkler_similarity(eval_input)
print(f"Match: {score.score:.2%} ({score.label})")

# Jaro-Winkler ≥ 0.85 is typically a good match for names
if score.score >= 0.85:
    print("✓ Likely the same entity")
```

**Examples:** `/examples/advanced_similarity_example.py` - Example 3

---

### Use Case 6: Keyword/Entity Extraction

```python
# Evaluate extracted keywords or entities
from custom.evals.metrics import token_f1_score

eval_input = {
    "output": "machine learning deep learning AI",
    "expected": "machine learning AI data science"
}

score = token_f1_score(eval_input)
print(f"F1: {score.score:.2%}")
print(f"Precision: {score.metadata['precision']:.2%}")
print(f"Recall: {score.metadata['recall']:.2%}")
print(f"Missing: {score.metadata['missing_tokens']}")
print(f"Extra: {score.metadata['extra_tokens']}")
```

**Examples:** `/examples/advanced_similarity_example.py` - Example 5

---

### Use Case 7: Batch Processing

```python
import pandas as pd
from custom.evals.metrics import sequence_similarity

# Load your dataset
df = pd.read_csv("data.csv")  # columns: output, ground_truth

# Apply metric
df["similarity"] = df.apply(
    lambda row: sequence_similarity({
        "output": row["output"],
        "expected": row["ground_truth"]
    }).score,
    axis=1
)

# Analyze
print(f"Average similarity: {df['similarity'].mean():.2%}")
print(f"High quality (≥80%): {(df['similarity'] >= 0.8).sum()}/{len(df)}")

# Filter low-quality outputs
low_quality = df[df["similarity"] < 0.5]
print(f"Need review: {len(low_quality)} items")
```

**Examples:** `/docs/NON_LLM_EVALUATION_GUIDE.md` - Section "Batch Evaluation"

---

## 📁 File Structure

```
cust-evals/
├── src/custom/evals/metrics/
│   ├── __init__.py (exports all 20 metrics)
│   ├── ocr_metrics.py (6 OCR metrics)
│   ├── similarity_metrics.py (7 basic similarity metrics)
│   └── advanced_similarity_metrics.py (7 advanced metrics)
│
├── docs/
│   ├── NON_LLM_EVALUATION_GUIDE.md (Main guide - OCR + Basic Similarity)
│   ├── SIMILARITY_METRICS_QUICKSTART.md (Quick reference for basic metrics)
│   ├── ADVANCED_METRICS_GUIDE.md (Advanced metrics deep dive)
│   └── TEXTRACT_QUICKSTART.md (OCR-specific quickstart)
│
├── examples/
│   ├── textract_evaluation_example.py (6 OCR examples)
│   ├── similarity_evaluation_example.py (7 basic similarity examples)
│   ├── advanced_similarity_example.py (8 advanced metric examples)
│   └── quick_start_similarity.py (Simple getting started guide)
│
└── verification scripts/
    ├── verify_similarity_metrics.py (Test basic metrics)
    └── verify_installation.py (Test all components)
```

---

## 🎓 Learning Path

### Beginner

1. **Read:** `/docs/NON_LLM_EVALUATION_GUIDE.md` - Overview section
2. **Run:** `python verify_similarity_metrics.py`
3. **Try:** `python examples/quick_start_similarity.py`
4. **Practice:** Use 2-3 basic metrics on your data

### Intermediate

1. **Read:** `/docs/SIMILARITY_METRICS_QUICKSTART.md`
2. **Run:** `python examples/similarity_evaluation_example.py`
3. **Experiment:** Try all 7 basic similarity metrics
4. **Implement:** Batch processing with Pandas

### Advanced

1. **Read:** `/docs/ADVANCED_METRICS_GUIDE.md`
2. **Run:** `python examples/advanced_similarity_example.py`
3. **Learn:** BLEU, ROUGE, Jaro-Winkler, Token F1
4. **Deploy:** Choose metrics for your specific use case

---

## 🔍 Metric Selection Matrix

| Your Task | Recommended Metrics | Priority |
|-----------|-------------------|----------|
| **OCR Text Extraction** | `text_extraction_accuracy`, `character_error_rate` | High |
| **OCR Bounding Boxes** | `bounding_box_iou` | High |
| **OCR Form Fields** | `field_detection_accuracy` | High |
| **General Text Comparison** | `sequence_similarity`, `word_overlap` | High |
| **Exact String Matching** | `similarity_exact_match` → `case_insensitive_match` → `normalized_match` | High |
| **Fuzzy String Matching** | `jaro_winkler_similarity`, `dice_coefficient` | High |
| **Machine Translation** | `bleu_score`, `rouge_l` | High |
| **Text Summarization** | `rouge_n` (n=1,2), `rouge_l` | High |
| **Name Matching** | `jaro_winkler_similarity` | High |
| **Entity Extraction** | `token_f1_score` | High |
| **Keyword Extraction** | `token_f1_score`, `word_overlap` | High |
| **Document Similarity** | `cosine_similarity_tfidf`, `rouge_l` | Medium |
| **Search Result Ranking** | `sequence_similarity` (60%) + `word_overlap` (40%) | High |
| **Truncation Detection** | `length_similarity` | Medium |
| **Partial Matching** | `contains_match` | Medium |

---

## ✅ Verification

Test that all metrics work correctly:

```bash
# Test basic similarity metrics
python verify_similarity_metrics.py

# Test advanced metrics (manual verification via examples)
python examples/advanced_similarity_example.py

# Test OCR metrics
python examples/textract_evaluation_example.py
```

All tests should pass with output showing ✓ for each metric.

---

## 🎯 Key Features

### 1. Standardized Output

All metrics return a `Score` object:

```python
score = sequence_similarity(eval_input)

# Access attributes
score.score          # Float 0.0-1.0
score.name           # Metric name
score.label          # Human-readable label
score.explanation    # Detailed description
score.direction      # "maximize" or "minimize"
score.kind           # "code" (deterministic)
score.metadata       # Dict with additional details
```

### 2. Rich Metadata

Every metric includes debugging information:

```python
score = word_overlap(eval_input)

# Metadata examples
score.metadata['common_words']      # Shared words
score.metadata['missing_words']     # In expected, not in output
score.metadata['extra_words']       # In output, not in expected
score.metadata['jaccard_similarity'] # Raw score
```

### 3. No External Dependencies

All metrics are:
- ✅ **Deterministic** - Same input always gives same output
- ✅ **Code-based** - No ML models or APIs required
- ✅ **Fast** - Optimized algorithms
- ✅ **Portable** - Works anywhere Python runs

### 4. Pandas Integration

Works seamlessly with DataFrames:

```python
df["metric_score"] = df.apply(
    lambda row: metric_function({
        "output": row["output"],
        "expected": row["expected"]
    }).score,
    axis=1
)
```

---

## 🔗 Quick Links

### Documentation
- Main Guide: [`/docs/NON_LLM_EVALUATION_GUIDE.md`](docs/NON_LLM_EVALUATION_GUIDE.md)
- Quick Reference: [`/docs/SIMILARITY_METRICS_QUICKSTART.md`](docs/SIMILARITY_METRICS_QUICKSTART.md)
- Advanced Guide: [`/docs/ADVANCED_METRICS_GUIDE.md`](docs/ADVANCED_METRICS_GUIDE.md)
- OCR Quickstart: [`/docs/TEXTRACT_QUICKSTART.md`](docs/TEXTRACT_QUICKSTART.md)

### Examples
- Basic Similarity: [`/examples/similarity_evaluation_example.py`](examples/similarity_evaluation_example.py)
- Advanced Metrics: [`/examples/advanced_similarity_example.py`](examples/advanced_similarity_example.py)
- Quick Start: [`/examples/quick_start_similarity.py`](examples/quick_start_similarity.py)
- OCR/Textract: [`/examples/textract_evaluation_example.py`](examples/textract_evaluation_example.py)

### API Reference
- OCR Metrics: [`/src/custom/evals/metrics/ocr_metrics.py`](src/custom/evals/metrics/ocr_metrics.py)
- Basic Similarity: [`/src/custom/evals/metrics/similarity_metrics.py`](src/custom/evals/metrics/similarity_metrics.py)
- Advanced Metrics: [`/src/custom/evals/metrics/advanced_similarity_metrics.py`](src/custom/evals/metrics/advanced_similarity_metrics.py)

---

## 🎉 Summary

The `cust-evals` framework now provides **20 comprehensive metrics** covering:

- ✅ **OCR/Document Extraction** (6 metrics)
- ✅ **Basic Text Similarity** (7 metrics)
- ✅ **Advanced Industry Standards** (7 metrics)

All metrics are:
- Production-ready
- Well-documented
- Thoroughly tested
- Easy to use
- Fully deterministic

**Perfect for evaluating NON-LLM outputs against ground truth!**

---

## 💡 Next Steps

1. **Install:** `pip install -e .`
2. **Verify:** `python verify_similarity_metrics.py`
3. **Learn:** Read `/docs/NON_LLM_EVALUATION_GUIDE.md`
4. **Try:** Run `/examples/quick_start_similarity.py`
5. **Implement:** Choose metrics for your use case
6. **Deploy:** Integrate into your evaluation pipeline

---

## 📞 Support

- **Issues:** Open an issue in the repository
- **Documentation:** See `/docs/` directory
- **Examples:** See `/examples/` directory

---

**Version:** 2.0 - Complete NON-LLM Evaluation Framework
**Last Updated:** 2026-02-02
