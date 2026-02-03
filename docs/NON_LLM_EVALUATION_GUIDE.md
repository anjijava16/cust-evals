# Non-LLM Evaluation Guide: AWS Textract & OCR Use Cases

This guide shows how to use the `cust-evals` framework for evaluating **non-LLM services** like AWS Textract, Google Cloud Vision, Azure Form Recognizer, and other document extraction tools.

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Available OCR Metrics](#available-ocr-metrics)
4. [AWS Textract Integration](#aws-textract-integration)
5. [Batch Evaluation](#batch-evaluation)
6. [Custom Metrics](#custom-metrics)
7. [Best Practices](#best-practices)

---

## Overview

While the `cust-evals` framework was initially designed for LLM evaluation, its **code-based metrics** path is completely generic and works for any evaluation task. This guide focuses on evaluating document extraction services.

### What You Need

**Input Data Structure:**
```python
{
    "output": str,              # Extracted text from OCR service
    "expected": str,            # Ground truth text
    "confidence": float,        # (Optional) OCR confidence score
    "output_bbox": dict,        # (Optional) Predicted bounding box
    "expected_bbox": dict,      # (Optional) Ground truth bounding box
    "detected_fields": list,    # (Optional) Detected form fields
    "expected_fields": list     # (Optional) Expected form fields
}
```

**Dependencies:**
```bash
pip install custom-evals
# or
pip install -e .
```

This includes `python-Levenshtein` for edit distance calculations.

---

## Quick Start

### Example 1: Basic Text Extraction Evaluation

```python
from custom.evals.metrics import (
    text_extraction_accuracy,
    character_error_rate,
    word_error_rate
)

# Your OCR output
textract_output = "Invoice Date: 12/31/2025\nTotal: $1,234.56"
ground_truth = "Invoice Date: 12/31/2025\nTotal: $1,234.56"

# Prepare evaluation input
eval_input = {
    "output": textract_output,
    "expected": ground_truth
}

# Run evaluations
accuracy = text_extraction_accuracy(eval_input)
cer = character_error_rate(eval_input)
wer = word_error_rate(eval_input)

# Print results
print(f"Accuracy: {accuracy.score:.2%} ({accuracy.label})")
print(f"CER: {cer.metadata['raw_cer']:.2%}")
print(f"WER: {wer.metadata['raw_wer']:.2%}")
```

**Output:**
```
Accuracy: 100.00% (excellent)
CER: 0.00%
WER: 0.00%
```

---

## Available OCR Metrics

### 1. `text_extraction_accuracy`

Fuzzy string matching using sequence similarity.

**Use Case:** Overall text extraction quality
**Returns:** Score 0.0-1.0 (higher is better)

```python
from custom.evals.metrics import text_extraction_accuracy

eval_input = {
    "output": "Invoise Date: 01/15/2025",  # OCR error: "Invoise"
    "expected": "Invoice Date: 01/15/2025"
}

score = text_extraction_accuracy(eval_input, normalize=True, case_sensitive=False)
print(f"Score: {score.score:.2%}")  # ~95% (tolerates minor errors)
```

**Parameters:**
- `normalize` (bool): Remove punctuation/whitespace
- `case_sensitive` (bool): Consider case differences

---

### 2. `character_error_rate` (CER)

Levenshtein distance normalized by reference length.

**Use Case:** Fine-grained character-level accuracy
**Formula:** `(substitutions + deletions + insertions) / total_characters`
**Returns:** Score 0.0-1.0 (inverted: 1.0 = perfect, 0.0 = worst)

```python
from custom.evals.metrics import character_error_rate

eval_input = {
    "output": "HELLO WORLD",
    "expected": "HELLO WRLD"  # Missing 'O'
}

score = character_error_rate(eval_input)
print(f"CER: {score.metadata['raw_cer']:.2%}")  # ~9% error rate
print(f"Edit distance: {score.metadata['edit_distance']}")  # 1 character
```

---

### 3. `word_error_rate` (WER)

Levenshtein distance at word level.

**Use Case:** Word-level accuracy (better for text with spaces)
**Formula:** `(word substitutions + deletions + insertions) / total_words`
**Returns:** Score 0.0-1.0 (inverted)

```python
from custom.evals.metrics import word_error_rate

eval_input = {
    "output": "Invoice Number 12345",
    "expected": "Invoice Number 67890"  # Different number
}

score = word_error_rate(eval_input)
print(f"WER: {score.metadata['raw_wer']:.2%}")
```

---

### 4. `bounding_box_iou`

Intersection over Union for spatial accuracy.

**Use Case:** Evaluate if OCR correctly locates text regions
**Returns:** Score 0.0-1.0 (1.0 = perfect overlap)

```python
from custom.evals.metrics import bounding_box_iou

# AWS Textract format (normalized coordinates 0-1)
predicted = {
    "Left": 0.1,
    "Top": 0.2,
    "Width": 0.3,
    "Height": 0.1
}

ground_truth = {
    "Left": 0.12,
    "Top": 0.19,
    "Width": 0.28,
    "Height": 0.11
}

eval_input = {
    "output_bbox": predicted,
    "expected_bbox": ground_truth
}

score = bounding_box_iou(eval_input)
print(f"IoU: {score.score:.2%}")  # ~85% overlap
```

**Supported formats:**
- AWS Textract: `{Left, Top, Width, Height}`
- Alternative: `{left, top, width, height}` (lowercase)

---

### 5. `confidence_threshold`

Validate if OCR confidence meets minimum quality bar.

**Use Case:** Filter low-quality extractions
**Returns:** 1.0 (pass) or 0.0 (fail)

```python
from custom.evals.metrics import confidence_threshold

# Textract returns confidence as 0-100
eval_input = {
    "confidence": 92.5,
    "threshold": 0.90  # 90% minimum
}

score = confidence_threshold(eval_input)
print(f"Status: {score.label}")  # "pass" or "fail"
```

**Auto-normalization:** Handles both 0-100 and 0-1 ranges.

---

### 6. `field_detection_accuracy`

Evaluate form field detection using F1 score.

**Use Case:** Structured forms (invoices, receipts, contracts)
**Returns:** F1 score (harmonic mean of precision and recall)

```python
from custom.evals.metrics import field_detection_accuracy

detected = ["Invoice Number", "Date", "Total", "Tax"]
expected = ["Invoice Number", "Date", "Total", "Subtotal"]

eval_input = {
    "detected_fields": detected,
    "expected_fields": expected
}

score = field_detection_accuracy(eval_input)
print(f"F1: {score.score:.2%}")
print(f"Missing: {score.metadata['missing_fields']}")  # ['Subtotal']
print(f"Extra: {score.metadata['extra_fields']}")      # ['Tax']
```

**Metrics breakdown:**
- `precision`: TP / (TP + FP)
- `recall`: TP / (TP + FN)
- `f1_score`: 2 × (precision × recall) / (precision + recall)

---

## Text Similarity Metrics

The framework also includes generic text similarity metrics for comparing any text outputs against ground truth. These are perfect for:
- Similarity search evaluation
- Text comparison tasks
- Fuzzy matching scenarios
- General text quality assessment

### 7. `similarity_exact_match`

Exact character-for-character string matching.

**Use Case:** When you need perfect string matching
**Returns:** 1.0 (match) or 0.0 (no match)

```python
from custom.evals.metrics import similarity_exact_match

eval_input = {
    "output": "Hello World",
    "expected": "Hello World"
}

score = similarity_exact_match(eval_input)
print(f"Match: {score.label}")  # "match" or "no_match"
```

---

### 8. `case_insensitive_match`

Case-insensitive string matching.

**Use Case:** When case differences should be ignored
**Returns:** 1.0 (match) or 0.0 (no match)

```python
from custom.evals.metrics import case_insensitive_match

eval_input = {
    "output": "Hello World",
    "expected": "hello world"
}

score = case_insensitive_match(eval_input)
print(f"Match: {score.label}")  # "match"
```

---

### 9. `normalized_match`

Normalized matching after removing punctuation and normalizing whitespace.

**Use Case:** Tolerant matching for text with formatting differences
**Normalization:** Lowercase, strip, normalize whitespace, remove punctuation
**Returns:** 1.0 (match) or 0.0 (no match)

```python
from custom.evals.metrics import normalized_match

eval_input = {
    "output": "Hello,  World!!!",
    "expected": "hello world"
}

score = normalized_match(eval_input)
print(f"Match: {score.label}")  # "match"
print(f"Normalized: {score.metadata['normalized_output']}")  # "hello world"
```

---

### 10. `sequence_similarity`

Calculate sequence similarity ratio using difflib.SequenceMatcher.

**Use Case:** Fuzzy matching with similarity score
**Returns:** Score 0.0-1.0 (ratio of matching characters)

```python
from custom.evals.metrics import sequence_similarity

eval_input = {
    "output": "The quick brown fox",
    "expected": "The quick brown dog",
    "threshold": 0.8  # Optional: minimum similarity to pass
}

score = sequence_similarity(eval_input)
print(f"Similarity: {score.score:.2%}")  # ~85%
print(f"Quality: {score.label}")  # "good"
```

**Parameters:**
- `threshold` (float): Minimum similarity to be considered a "pass" (default: 0.8)

---

### 11. `word_overlap`

Calculate word-level overlap using Jaccard similarity.

**Use Case:** Measure shared vocabulary between texts
**Formula:** Jaccard = |words_in_common| / |total_unique_words|
**Returns:** Score 0.0-1.0

```python
from custom.evals.metrics import word_overlap

eval_input = {
    "output": "The quick brown fox jumps",
    "expected": "The lazy brown dog sleeps",
    "threshold": 0.7  # Optional
}

score = word_overlap(eval_input)
print(f"Word overlap: {score.score:.2%}")  # 40% (2 common words: "the", "brown")
print(f"Common words: {score.metadata['common_words']}")  # ['the', 'brown']
print(f"Missing words: {score.metadata['missing_words']}")  # ['lazy', 'dog', 'sleeps']
```

**Metadata includes:**
- `common_words`: List of shared words
- `missing_words`: Words in expected but not in output
- `extra_words`: Words in output but not in expected

---

### 12. `contains_match`

Check if one text contains the other (bidirectional).

**Use Case:** Partial matching, substring detection
**Returns:** 1.0 if containment found, 0.0 otherwise

```python
from custom.evals.metrics import contains_match

eval_input = {
    "output": "The quick brown fox jumps over the lazy dog",
    "expected": "quick brown fox",
    "case_sensitive": False  # Optional
}

score = contains_match(eval_input)
print(f"Contains: {score.label}")  # "contains"
print(f"Direction: {score.explanation}")  # "output contains expected"
```

**Parameters:**
- `case_sensitive` (bool): Whether to perform case-sensitive matching (default: False)

---

### 13. `length_similarity`

Compare text lengths and calculate similarity ratio.

**Use Case:** Detect truncation or verbosity issues
**Formula:** min(len_output, len_expected) / max(len_output, len_expected)
**Returns:** Score 0.0-1.0

```python
from custom.evals.metrics import length_similarity

eval_input = {
    "output": "Hello World",  # 11 chars
    "expected": "Hello",      # 5 chars
    "threshold": 0.8  # Optional
}

score = length_similarity(eval_input)
print(f"Length similarity: {score.score:.2%}")  # 45%
print(f"Difference: {score.metadata['length_difference']} chars")  # 6
```

**Use this to detect:**
- Truncated outputs
- Overly verbose responses
- Significant length mismatches

---

## AWS Textract Integration

### Full Pipeline Example

```python
import boto3
from custom.evals.metrics import (
    text_extraction_accuracy,
    bounding_box_iou,
    confidence_threshold,
    field_detection_accuracy
)

# Initialize Textract client
textract = boto3.client('textract', region_name='us-east-1')

def evaluate_textract_document(s3_bucket, s3_key, ground_truth):
    """Complete Textract evaluation pipeline."""

    # 1. Call Textract
    response = textract.detect_document_text(
        Document={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}}
    )

    # 2. Extract text and metadata
    extracted_text = "\n".join([
        block['Text']
        for block in response['Blocks']
        if block['BlockType'] == 'LINE'
    ])

    avg_confidence = sum(
        block['Confidence']
        for block in response['Blocks']
        if 'Confidence' in block
    ) / len(response['Blocks'])

    # 3. Run evaluations
    scores = {}

    # Text accuracy
    scores['text_accuracy'] = text_extraction_accuracy({
        "output": extracted_text,
        "expected": ground_truth['text']
    })

    # Confidence check
    scores['confidence'] = confidence_threshold({
        "confidence": avg_confidence,
        "threshold": 0.85
    })

    # Bounding box (example for first line)
    if ground_truth.get('bounding_boxes'):
        first_line_bbox = next(
            block['Geometry']['BoundingBox']
            for block in response['Blocks']
            if block['BlockType'] == 'LINE'
        )

        scores['bbox_accuracy'] = bounding_box_iou({
            "output_bbox": first_line_bbox,
            "expected_bbox": ground_truth['bounding_boxes'][0]
        })

    return scores

# Usage
ground_truth = {
    "text": "INVOICE\nDate: 2025-02-01\nAmount: $500.00",
    "bounding_boxes": [
        {"Left": 0.1, "Top": 0.05, "Width": 0.3, "Height": 0.05}
    ]
}

scores = evaluate_textract_document(
    s3_bucket="my-documents",
    s3_key="invoices/invoice_001.pdf",
    ground_truth=ground_truth
)

for name, score in scores.items():
    print(f"{name}: {score.score:.2%} ({score.label})")
```

---

## Similarity Search & Text Comparison Examples

### Example: Evaluating Search Results

```python
from custom.evals.metrics import (
    sequence_similarity,
    word_overlap,
    contains_match,
    normalized_match
)

# Scenario: You have a search system that finds similar documents
# You want to evaluate if the retrieved text matches the expected result

def evaluate_search_result(retrieved_text, expected_text):
    """Evaluate a single search result against expected text."""

    eval_input = {
        "output": retrieved_text,
        "expected": expected_text
    }

    # Run multiple similarity metrics
    scores = {
        "sequence_sim": sequence_similarity(eval_input),
        "word_overlap": word_overlap(eval_input),
        "normalized": normalized_match(eval_input),
        "contains": contains_match(eval_input)
    }

    # Print results
    print("Search Result Evaluation:")
    for metric_name, score in scores.items():
        print(f"  {metric_name}: {score.score:.2%} ({score.label})")

    # Overall pass/fail based on sequence similarity
    if scores["sequence_sim"].score >= 0.8:
        print("✓ Search result is relevant")
    else:
        print("✗ Search result may not be relevant")

    return scores

# Example usage
retrieved = "The Python programming language is widely used for data science and machine learning"
expected = "Python is a popular language for data science and ML applications"

evaluate_search_result(retrieved, expected)
```

**Output:**
```
Search Result Evaluation:
  sequence_sim: 67.21% (acceptable)
  word_overlap: 52.94% (poor)
  normalized: 0.00% (no_match)
  contains: 0.00% (no_containment)
✗ Search result may not be relevant
```

---

### Example: Batch Similarity Evaluation

```python
import pandas as pd
from custom.evals.metrics import (
    sequence_similarity,
    word_overlap,
    case_insensitive_match,
    length_similarity
)

# Dataset: search queries and retrieved results
data = [
    {
        "query": "What is Python?",
        "output": "Python is a programming language",
        "expected": "Python is a programming language"
    },
    {
        "query": "Who created Python?",
        "output": "Guido van Rossum created Python in 1991",
        "expected": "Python was created by Guido van Rossum"
    },
    {
        "query": "What is machine learning?",
        "output": "ML is a subset of AI",
        "expected": "Machine learning is a subset of artificial intelligence"
    }
]

def evaluate_batch_similarity(data):
    """Evaluate multiple outputs against ground truth."""

    results = []

    for item in data:
        eval_input = {
            "output": item["output"],
            "expected": item["expected"]
        }

        # Run all similarity metrics
        seq_sim = sequence_similarity(eval_input)
        word_ov = word_overlap(eval_input)
        case_ins = case_insensitive_match(eval_input)
        len_sim = length_similarity(eval_input)

        results.append({
            "query": item["query"],
            "output": item["output"],
            "expected": item["expected"],
            "sequence_similarity": seq_sim.score,
            "word_overlap": word_ov.score,
            "case_insensitive_match": case_ins.score,
            "length_similarity": len_sim.score,
            "avg_score": (seq_sim.score + word_ov.score + len_sim.score) / 3
        })

    # Convert to DataFrame
    df = pd.DataFrame(results)

    print("\nBatch Evaluation Results:")
    print(f"Average sequence similarity: {df['sequence_similarity'].mean():.2%}")
    print(f"Average word overlap: {df['word_overlap'].mean():.2%}")
    print(f"Average length similarity: {df['length_similarity'].mean():.2%}")
    print(f"Exact matches (case-insensitive): {df['case_insensitive_match'].sum()}/{len(df)}")

    return df

# Run evaluation
results_df = evaluate_batch_similarity(data)
results_df.to_csv("similarity_evaluation_results.csv", index=False)
```

---

### Example: Comprehensive Text Comparison

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

def comprehensive_text_comparison(output, expected):
    """Run all 7 similarity metrics on a single comparison."""

    eval_input = {
        "output": output,
        "expected": expected
    }

    metrics = {
        "Exact Match": similarity_exact_match(eval_input),
        "Case Insensitive": case_insensitive_match(eval_input),
        "Normalized Match": normalized_match(eval_input),
        "Sequence Similarity": sequence_similarity(eval_input),
        "Word Overlap": word_overlap(eval_input),
        "Contains Match": contains_match(eval_input),
        "Length Similarity": length_similarity(eval_input)
    }

    print("\n" + "="*80)
    print("COMPREHENSIVE TEXT COMPARISON")
    print("="*80)
    print(f"\nOutput:   {output[:60]}{'...' if len(output) > 60 else ''}")
    print(f"Expected: {expected[:60]}{'...' if len(expected) > 60 else ''}")
    print("\n" + "-"*80)

    for metric_name, score in metrics.items():
        status = "✓" if score.score >= 0.7 else "✗"
        print(f"{status} {metric_name:20s}: {score.score:.2%} ({score.label})")

    # Calculate weighted overall score
    weights = {
        "Exact Match": 0.05,
        "Case Insensitive": 0.05,
        "Normalized Match": 0.10,
        "Sequence Similarity": 0.35,
        "Word Overlap": 0.25,
        "Contains Match": 0.10,
        "Length Similarity": 0.10
    }

    overall = sum(metrics[k].score * weights[k] for k in weights)

    print("-"*80)
    print(f"Overall Weighted Score: {overall:.2%}")
    print("="*80)

    return metrics, overall

# Example 1: Very similar texts
print("\nExample 1: High Similarity")
comprehensive_text_comparison(
    "The quick brown fox jumps over the lazy dog",
    "The quick brown fox jumped over the lazy dog"
)

# Example 2: Different texts with some overlap
print("\nExample 2: Moderate Similarity")
comprehensive_text_comparison(
    "Python is a programming language",
    "Python is used for data science"
)

# Example 3: Very different texts
print("\nExample 3: Low Similarity")
comprehensive_text_comparison(
    "Machine learning algorithms",
    "Database management systems"
)
```

---

## Batch Evaluation

### Using Pandas for Large Datasets

```python
import pandas as pd
from custom.evals.metrics import text_extraction_accuracy, character_error_rate

# Load dataset
df = pd.read_csv("textract_results.csv")
# Columns: document_id, textract_output, ground_truth, confidence

def evaluate_row(row):
    """Apply evaluations to each row."""
    eval_input = {
        "output": row["textract_output"],
        "expected": row["ground_truth"]
    }

    acc = text_extraction_accuracy(eval_input)
    cer = character_error_rate(eval_input)

    return pd.Series({
        "accuracy": acc.score,
        "accuracy_label": acc.label,
        "cer": cer.metadata["raw_cer"],
        "edit_distance": cer.metadata["edit_distance"]
    })

# Apply to all rows
results = df.apply(evaluate_row, axis=1)
df_results = pd.concat([df, results], axis=1)

# Aggregate statistics
print(f"Mean Accuracy: {df_results['accuracy'].mean():.2%}")
print(f"Mean CER: {df_results['cer'].mean():.2%}")
print(f"Documents with >95% accuracy: {(df_results['accuracy'] > 0.95).sum()}")

# Save results
df_results.to_csv("evaluation_results.csv", index=False)
```

---

## Custom Metrics

### Creating Your Own OCR Metrics

Use the `@create_evaluator` decorator to add custom metrics:

```python
from custom.evals import create_evaluator, Score

@create_evaluator(name="table_structure_accuracy", kind="code", direction="maximize")
def table_structure_accuracy(
    detected_rows: int,
    expected_rows: int,
    detected_cols: int,
    expected_cols: int
) -> Score:
    """Evaluate if table structure was correctly detected."""

    row_accuracy = 1.0 - abs(detected_rows - expected_rows) / max(expected_rows, 1)
    col_accuracy = 1.0 - abs(detected_cols - expected_cols) / max(expected_cols, 1)

    # Weighted average (rows are more important)
    score = 0.7 * row_accuracy + 0.3 * col_accuracy

    label = "excellent" if score >= 0.95 else \
            "good" if score >= 0.85 else \
            "acceptable" if score >= 0.70 else \
            "poor"

    return Score(
        score=score,
        name="table_structure_accuracy",
        label=label,
        explanation=f"Detected {detected_rows}×{detected_cols} table, "
                   f"expected {expected_rows}×{expected_cols}",
        direction="maximize",
        kind="code",
        metadata={
            "detected_rows": detected_rows,
            "detected_cols": detected_cols,
            "row_accuracy": row_accuracy,
            "col_accuracy": col_accuracy
        }
    )

# Usage
eval_input = {
    "detected_rows": 12,
    "expected_rows": 10,
    "detected_cols": 5,
    "expected_cols": 5
}

score = table_structure_accuracy(eval_input)
print(f"Table Structure: {score.score:.2%} ({score.label})")
```

---

## Best Practices

### 1. Choose the Right Metric

| Use Case | Recommended Metrics |
|----------|---------------------|
| **OCR/Document Extraction** | |
| Overall text quality | `text_extraction_accuracy`, `word_error_rate` |
| Character-level precision | `character_error_rate` |
| Spatial accuracy | `bounding_box_iou` |
| Quality filtering | `confidence_threshold` |
| Structured forms | `field_detection_accuracy` |
| **Text Similarity & Comparison** | |
| Exact matching | `similarity_exact_match`, `case_insensitive_match` |
| Fuzzy matching | `sequence_similarity`, `word_overlap` |
| Partial matching | `contains_match`, `normalized_match` |
| Length validation | `length_similarity` |
| Similarity search evaluation | `sequence_similarity` + `word_overlap` |
| General text comparison | Combine all 7 similarity metrics |
| **Multi-metric Approach** | |
| Comprehensive evaluation | Combine all relevant scores with weights |

### 2. Normalization Strategy

For noisy OCR outputs, use normalization:

```python
# Tolerant to OCR errors (punctuation, spacing)
score = text_extraction_accuracy(
    eval_input,
    normalize=True,        # Remove punctuation, extra spaces
    case_sensitive=False   # Ignore case differences
)
```

For exact matching:
```python
# Strict evaluation
score = text_extraction_accuracy(
    eval_input,
    normalize=False,
    case_sensitive=True
)
```

### 3. Multi-Metric Evaluation

Combine multiple metrics for comprehensive assessment:

```python
def comprehensive_evaluation(textract_output, ground_truth):
    """Run all relevant metrics."""
    eval_input = {
        "output": textract_output["text"],
        "expected": ground_truth["text"]
    }

    scores = {
        "accuracy": text_extraction_accuracy(eval_input),
        "cer": character_error_rate(eval_input),
        "wer": word_error_rate(eval_input)
    }

    # Weighted overall score
    weights = {"accuracy": 0.5, "cer": 0.3, "wer": 0.2}
    overall = sum(scores[k].score * weights[k] for k in weights)

    return {
        "scores": scores,
        "overall": overall
    }
```

### 4. Field Mapping for Different OCR Providers

Adapt to different column names:

```python
# Google Cloud Vision format
eval_input = {
    "prediction": vision_output,    # Different field name
    "reference": ground_truth       # Different field name
}

field_mapping = {
    "output": "prediction",
    "expected": "reference"
}

score = text_extraction_accuracy(eval_input, field_mapping=field_mapping)
```

### 5. Error Analysis

Use metadata for debugging:

```python
score = character_error_rate(eval_input)

if score.metadata["raw_cer"] > 0.15:  # High error rate
    print(f"High CER detected: {score.metadata['raw_cer']:.2%}")
    print(f"Edit distance: {score.metadata['edit_distance']}")
    print(f"Output length: {score.metadata['output_length']}")
    print(f"Expected length: {score.metadata['expected_length']}")

    # Investigate specific errors
    print(f"\nOutput: {eval_input['output'][:100]}")
    print(f"Expected: {eval_input['expected'][:100]}")
```

---

## Complete Examples

### OCR/Textract Examples

See `examples/textract_evaluation_example.py` for 6 comprehensive examples:

1. Single text extraction
2. Bounding box evaluation
3. Confidence validation
4. Form field detection
5. Batch processing with Pandas
6. Complete pipeline

Run the examples:

```bash
cd examples
python textract_evaluation_example.py
```

### Similarity Metrics Examples

See `examples/similarity_evaluation_example.py` for 7 comprehensive examples:

1. Basic text matching (exact, case-insensitive, normalized)
2. Fuzzy matching (sequence similarity, word overlap)
3. Partial matching and containment
4. Length validation
5. Similarity search evaluation
6. Batch evaluation with multiple metrics
7. Comprehensive text comparison

Run the examples:

```bash
cd examples
python similarity_evaluation_example.py
```

---

## Summary

The `cust-evals` framework provides:

✅ **13 ready-to-use metrics:**
   - 6 OCR/document extraction metrics
   - 7 text similarity/comparison metrics
✅ **Code-based path** - no LLM dependency
✅ **Standardized `Score` objects** for easy aggregation
✅ **Flexible field mapping** for different OCR providers and data sources
✅ **Pandas integration** for batch evaluation
✅ **Extensible** - create custom metrics easily

### Metric Categories

**OCR/Document Extraction (6 metrics):**
1. `text_extraction_accuracy` - Overall text quality
2. `character_error_rate` - Character-level precision
3. `word_error_rate` - Word-level accuracy
4. `bounding_box_iou` - Spatial accuracy
5. `confidence_threshold` - Quality filtering
6. `field_detection_accuracy` - Form field detection

**Text Similarity/Comparison (7 metrics):**
1. `similarity_exact_match` - Exact string matching
2. `case_insensitive_match` - Case-insensitive matching
3. `normalized_match` - Normalized text matching
4. `sequence_similarity` - Fuzzy sequence matching
5. `word_overlap` - Jaccard word similarity
6. `contains_match` - Substring/containment detection
7. `length_similarity` - Text length comparison

**Next Steps:**
1. Install dependencies: `pip install -e .`
2. Run OCR examples: `python examples/textract_evaluation_example.py`
3. Run similarity examples: `python examples/similarity_evaluation_example.py`
4. Adapt to your use case (OCR services, search systems, text comparison, etc.)
5. Create custom metrics for your specific needs

---

## Additional Resources

- **Framework Documentation:** `/docs/README.md`
- **API Reference:** See docstrings in `/src/custom/evals/metrics/ocr_metrics.py`
- **Custom Metrics Guide:** `/docs/CUSTOM_METRICS.md`

For questions or issues, please open an issue in the repository.
