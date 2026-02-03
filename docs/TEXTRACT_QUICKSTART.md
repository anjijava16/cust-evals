# AWS Textract Quick Start Guide

**Goal:** Evaluate AWS Textract outputs against ground truth in 5 minutes.

## Installation

```bash
pip install -e .
```

This installs all dependencies including `python-Levenshtein` for OCR metrics.

---

## Minimal Example

```python
from custom.evals.metrics import (
    text_extraction_accuracy,
    character_error_rate,
    confidence_threshold
)

# Your Textract output
textract_result = {
    "text": "Invoice Number: INV-2025-001\nDate: 02/01/2025\nTotal: $1,500.00",
    "confidence": 94.5
}

# Ground truth
ground_truth = {
    "text": "Invoice Number: INV-2025-001\nDate: 02/01/2025\nTotal: $1,500.00"
}

# Evaluate
eval_input = {
    "output": textract_result["text"],
    "expected": ground_truth["text"]
}

accuracy = text_extraction_accuracy(eval_input)
cer = character_error_rate(eval_input)

conf_input = {
    "confidence": textract_result["confidence"],
    "threshold": 0.90
}
conf_score = confidence_threshold(conf_input)

# Print results
print(f"✓ Text Accuracy: {accuracy.score:.2%} ({accuracy.label})")
print(f"✓ Character Error Rate: {cer.metadata['raw_cer']:.2%}")
print(f"✓ Confidence: {conf_score.label.upper()}")
```

**Expected Output:**
```
✓ Text Accuracy: 100.00% (excellent)
✓ Character Error Rate: 0.00%
✓ Confidence: PASS
```

---

## Data Format

### Input Structure

The framework expects a dictionary with these fields:

```python
eval_input = {
    # Required
    "output": str,              # Textract extracted text
    "expected": str,            # Ground truth text

    # Optional (for specific metrics)
    "confidence": float,        # 0-100 or 0-1
    "output_bbox": dict,        # {"Left": 0.1, "Top": 0.2, "Width": 0.3, "Height": 0.1}
    "expected_bbox": dict,      # Ground truth bounding box
    "detected_fields": list,    # ["Field1", "Field2", ...]
    "expected_fields": list     # ["Field1", "Field2", ...]
}
```

### AWS Textract Response Mapping

```python
import boto3

textract = boto3.client('textract')
response = textract.detect_document_text(
    Document={'S3Object': {'Bucket': 'my-bucket', 'Name': 'doc.pdf'}}
)

# Extract text
extracted_text = "\n".join([
    block['Text']
    for block in response['Blocks']
    if block['BlockType'] == 'LINE'
])

# Get average confidence
avg_confidence = sum(
    block.get('Confidence', 0)
    for block in response['Blocks']
    if 'Confidence' in block
) / len(response['Blocks'])

# Get bounding box for first line
first_bbox = next(
    block['Geometry']['BoundingBox']
    for block in response['Blocks']
    if block['BlockType'] == 'LINE'
)

# Format for evaluation
eval_input = {
    "output": extracted_text,
    "expected": ground_truth_text,
    "confidence": avg_confidence,
    "output_bbox": first_bbox  # Already in correct format!
}
```

---

## Available Metrics

| Metric | Purpose | Best For |
|--------|---------|----------|
| `text_extraction_accuracy` | Overall text similarity | General OCR quality |
| `character_error_rate` | Character-level accuracy | Precise text evaluation |
| `word_error_rate` | Word-level accuracy | Documents with clear words |
| `bounding_box_iou` | Spatial accuracy | Text localization |
| `confidence_threshold` | Quality gating | Filtering low-quality results |
| `field_detection_accuracy` | Form field detection | Structured documents (invoices, forms) |

---

## Common Patterns

### Pattern 1: Single Document Evaluation

```python
from custom.evals.metrics import text_extraction_accuracy, character_error_rate

def evaluate_document(textract_output, ground_truth):
    eval_input = {
        "output": textract_output,
        "expected": ground_truth
    }

    acc = text_extraction_accuracy(eval_input)
    cer = character_error_rate(eval_input)

    return {
        "accuracy": acc.score,
        "accuracy_label": acc.label,
        "cer": cer.metadata["raw_cer"],
        "explanation": acc.explanation
    }

result = evaluate_document(
    "INVOICE #12345",
    "INVOICE #12345"
)

print(result)
# {'accuracy': 1.0, 'accuracy_label': 'excellent', 'cer': 0.0, ...}
```

### Pattern 2: Batch Processing

```python
import pandas as pd
from custom.evals.metrics import text_extraction_accuracy

# Load data
df = pd.DataFrame({
    "doc_id": ["doc1", "doc2", "doc3"],
    "textract_output": ["Invoice #001", "Invoice #002", "Invoice #003"],
    "ground_truth": ["Invoice #001", "Invoice #002", "Invoice #003"]
})

# Evaluate
def eval_row(row):
    score = text_extraction_accuracy({
        "output": row["textract_output"],
        "expected": row["ground_truth"]
    })
    return score.score

df["accuracy"] = df.apply(eval_row, axis=1)

print(df)
print(f"\nMean Accuracy: {df['accuracy'].mean():.2%}")
```

### Pattern 3: Multi-Metric Evaluation

```python
from custom.evals.metrics import (
    text_extraction_accuracy,
    character_error_rate,
    word_error_rate,
    confidence_threshold
)

def comprehensive_eval(textract_data, ground_truth, min_confidence=0.85):
    """Run all relevant metrics."""

    # Text metrics
    text_eval = {
        "output": textract_data["text"],
        "expected": ground_truth["text"]
    }

    scores = {
        "accuracy": text_extraction_accuracy(text_eval),
        "cer": character_error_rate(text_eval),
        "wer": word_error_rate(text_eval)
    }

    # Confidence check
    conf_eval = {
        "confidence": textract_data["confidence"],
        "threshold": min_confidence
    }
    scores["confidence"] = confidence_threshold(conf_eval)

    # Calculate weighted overall score
    overall = (
        scores["accuracy"].score * 0.5 +
        scores["cer"].score * 0.3 +
        scores["wer"].score * 0.2
    )

    return {
        "scores": scores,
        "overall": overall,
        "passes_quality": overall >= 0.90 and scores["confidence"].label == "pass"
    }

result = comprehensive_eval(
    textract_data={"text": "INVOICE", "confidence": 95.0},
    ground_truth={"text": "INVOICE"}
)

print(f"Overall Score: {result['overall']:.2%}")
print(f"Passes Quality Gate: {result['passes_quality']}")
```

### Pattern 4: Error Filtering

```python
from custom.evals.metrics import confidence_threshold, character_error_rate

def should_review_manually(textract_data, ground_truth):
    """Determine if document needs manual review."""

    # Check confidence
    conf = confidence_threshold({
        "confidence": textract_data["confidence"],
        "threshold": 0.85
    })

    # Check accuracy
    cer = character_error_rate({
        "output": textract_data["text"],
        "expected": ground_truth["text"]
    })

    # Flag for review if:
    # - Low confidence OR
    # - High character error rate
    return (
        conf.label == "fail" or
        cer.metadata["raw_cer"] > 0.10  # >10% error rate
    )

if should_review_manually(textract_data, ground_truth):
    print("⚠️  Document flagged for manual review")
else:
    print("✓ Document passed automated quality check")
```

---

## Field Mapping for Different Services

If your OCR service uses different field names:

```python
# Google Cloud Vision format
vision_output = {
    "fullTextAnnotation": "Invoice text...",
    "confidence_score": 0.92
}

# Use field mapping
eval_input = {
    "prediction": vision_output["fullTextAnnotation"],
    "reference": ground_truth
}

field_mapping = {
    "output": "prediction",
    "expected": "reference"
}

score = text_extraction_accuracy(eval_input, field_mapping=field_mapping)
```

---

## Interpreting Scores

### Score Object

All metrics return a `Score` object:

```python
score = text_extraction_accuracy(eval_input)

# Access attributes
score.score          # float: 0.0-1.0 numeric value
score.name           # str: "text_extraction_accuracy"
score.label          # str: "excellent" | "good" | "acceptable" | "poor"
score.explanation    # str: Human-readable explanation
score.direction      # str: "maximize" or "minimize"
score.kind           # str: "code" (deterministic)
score.metadata       # dict: Additional metrics and details
```

### Label Thresholds

| Label | Accuracy | CER/WER | IoU |
|-------|----------|---------|-----|
| excellent | ≥95% | ≤5% | ≥90% |
| good | ≥85% | ≤15% | ≥75% |
| acceptable | ≥70% | ≤30% | ≥50% |
| poor | <70% | >30% | <50% |

---

## Troubleshooting

### ImportError: No module named 'Levenshtein'

```bash
pip install python-Levenshtein
```

### Different bounding box format

The framework expects `{Left, Top, Width, Height}`. If your service uses a different format:

```python
# Convert from (x1, y1, x2, y2) format
def convert_bbox(x1, y1, x2, y2):
    return {
        "Left": x1,
        "Top": y1,
        "Width": x2 - x1,
        "Height": y2 - y1
    }

eval_input = {
    "output_bbox": convert_bbox(0.1, 0.2, 0.4, 0.3),
    "expected_bbox": ground_truth_bbox
}
```

### Scores seem too low

Try using normalization:

```python
# More lenient evaluation
score = text_extraction_accuracy(
    eval_input,
    normalize=True,         # Remove punctuation, extra spaces
    case_sensitive=False    # Ignore case
)
```

---

## Next Steps

1. **Run the full example:** `python examples/textract_evaluation_example.py`
2. **Read the complete guide:** `docs/NON_LLM_EVALUATION_GUIDE.md`
3. **Create custom metrics:** See examples in `src/custom/evals/metrics/ocr_metrics.py`
4. **Integrate with your pipeline:** Adapt patterns above to your workflow

---

## Summary

**3 Steps to Evaluate Textract:**

1. **Prepare data:**
   ```python
   eval_input = {"output": textract_text, "expected": ground_truth}
   ```

2. **Run evaluation:**
   ```python
   score = text_extraction_accuracy(eval_input)
   ```

3. **Check results:**
   ```python
   print(f"{score.score:.2%} ({score.label})")
   ```

That's it! 🎉
