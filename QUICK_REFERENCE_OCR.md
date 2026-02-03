# OCR Metrics Quick Reference Card

## 📦 Import

```python
from custom.evals.metrics import (
    text_extraction_accuracy,
    character_error_rate,
    word_error_rate,
    bounding_box_iou,
    confidence_threshold,
    field_detection_accuracy
)
```

---

## 📊 Metrics Overview

| Metric | Input Fields | Output | Use When |
|--------|--------------|--------|----------|
| `text_extraction_accuracy` | `output`, `expected` | 0.0-1.0 ↑ | General OCR quality |
| `character_error_rate` | `output`, `expected` | 0.0-1.0 ↑ | Character precision |
| `word_error_rate` | `output`, `expected` | 0.0-1.0 ↑ | Word accuracy |
| `bounding_box_iou` | `output_bbox`, `expected_bbox` | 0.0-1.0 ↑ | Spatial accuracy |
| `confidence_threshold` | `confidence`, `threshold` | 0.0/1.0 | Quality gating |
| `field_detection_accuracy` | `detected_fields`, `expected_fields` | 0.0-1.0 ↑ | Form field detection |

↑ = Higher is better

---

## 🎯 Usage Patterns

### Pattern 1: Single Document

```python
eval_input = {
    "output": "Textract text...",
    "expected": "Ground truth..."
}

score = text_extraction_accuracy(eval_input)
print(f"{score.score:.2%} ({score.label})")
```

### Pattern 2: Batch Processing

```python
import pandas as pd

df = pd.DataFrame({...})

def eval_row(row):
    return text_extraction_accuracy({
        "output": row["textract_output"],
        "expected": row["ground_truth"]
    }).score

df["accuracy"] = df.apply(eval_row, axis=1)
```

### Pattern 3: Multi-Metric

```python
scores = {
    "accuracy": text_extraction_accuracy(text_eval),
    "cer": character_error_rate(text_eval),
    "wer": word_error_rate(text_eval)
}

overall = sum(s.score for s in scores.values()) / len(scores)
```

---

## 🔧 Common Parameters

### text_extraction_accuracy

```python
text_extraction_accuracy(
    eval_input,
    normalize=True,         # Remove punctuation, whitespace
    case_sensitive=False    # Ignore case
)
```

### confidence_threshold

```python
confidence_threshold({
    "confidence": 92.5,     # 0-100 or 0-1 (auto-normalized)
    "threshold": 0.85       # Minimum acceptable (0-1)
})
```

### field_detection_accuracy

```python
field_detection_accuracy({
    "detected_fields": ["Field1", "Field2"],
    "expected_fields": ["Field1", "Field3"]
}, case_sensitive=False)
```

---

## 📐 Bounding Box Format

### AWS Textract Format (Supported)

```python
bbox = {
    "Left": 0.1,      # X coordinate (0-1)
    "Top": 0.2,       # Y coordinate (0-1)
    "Width": 0.3,     # Width (0-1)
    "Height": 0.1     # Height (0-1)
}
```

Also supports lowercase: `left`, `top`, `width`, `height`

---

## 📊 Score Object

```python
score = text_extraction_accuracy(eval_input)

score.score          # 0.85 (numeric value)
score.name           # "text_extraction_accuracy"
score.label          # "excellent" | "good" | "acceptable" | "poor"
score.explanation    # "Text similarity: 85.00%..."
score.direction      # "maximize" | "minimize"
score.kind           # "code"
score.metadata       # {...} (detailed metrics)
```

---

## 🏷️ Label Thresholds

| Metric | Excellent | Good | Acceptable | Poor |
|--------|-----------|------|------------|------|
| Accuracy | ≥95% | ≥85% | ≥70% | <70% |
| CER/WER | ≤5% | ≤15% | ≤30% | >30% |
| IoU | ≥90% | ≥75% | ≥50% | <50% |
| F1 | ≥95% | ≥85% | ≥70% | <70% |

---

## 🔄 Field Mapping

For different OCR providers:

```python
# Google Cloud Vision
eval_input = {
    "prediction": vision_output,
    "reference": ground_truth
}

field_mapping = {
    "output": "prediction",
    "expected": "reference"
}

score = text_extraction_accuracy(eval_input, field_mapping=field_mapping)
```

---

## 🔍 Metadata Examples

### character_error_rate

```python
score.metadata = {
    "raw_cer": 0.05,
    "edit_distance": 3,
    "output_length": 60,
    "expected_length": 63
}
```

### field_detection_accuracy

```python
score.metadata = {
    "precision": 0.75,
    "recall": 0.80,
    "f1_score": 0.77,
    "true_positives": 3,
    "false_positives": 1,
    "false_negatives": 1,
    "missing_fields": ["Field3"],
    "extra_fields": ["Field4"]
}
```

---

## 🚀 Complete Example

```python
import boto3
from custom.evals.metrics import (
    text_extraction_accuracy,
    character_error_rate,
    confidence_threshold
)

# 1. Call Textract
textract = boto3.client('textract')
response = textract.detect_document_text(
    Document={'S3Object': {'Bucket': 'bucket', 'Name': 'doc.pdf'}}
)

# 2. Extract text
extracted = "\n".join([
    block['Text'] for block in response['Blocks']
    if block['BlockType'] == 'LINE'
])

# 3. Get confidence
avg_conf = sum(
    block.get('Confidence', 0) for block in response['Blocks']
    if 'Confidence' in block
) / len(response['Blocks'])

# 4. Evaluate
text_eval = {"output": extracted, "expected": ground_truth}
conf_eval = {"confidence": avg_conf, "threshold": 0.85}

acc_score = text_extraction_accuracy(text_eval)
cer_score = character_error_rate(text_eval)
conf_score = confidence_threshold(conf_eval)

# 5. Report
print(f"Accuracy: {acc_score.score:.2%} ({acc_score.label})")
print(f"CER: {cer_score.metadata['raw_cer']:.2%}")
print(f"Confidence: {conf_score.label.upper()}")
```

---

## 🐛 Troubleshooting

### ImportError: No module named 'Levenshtein'

```bash
pip install python-Levenshtein
```

### Scores too low

Try normalization:

```python
text_extraction_accuracy(
    eval_input,
    normalize=True,
    case_sensitive=False
)
```

### Different bbox format

Convert to Textract format:

```python
def convert(x1, y1, x2, y2):
    return {
        "Left": x1,
        "Top": y1,
        "Width": x2 - x1,
        "Height": y2 - y1
    }
```

---

## 📚 Resources

- **Full Guide:** `docs/NON_LLM_EVALUATION_GUIDE.md`
- **Quick Start:** `docs/TEXTRACT_QUICKSTART.md`
- **Examples:** `examples/textract_evaluation_example.py`
- **Tests:** `tests/test_ocr_metrics.py`

---

## 💡 Tips

1. **Start simple:** Use `text_extraction_accuracy` first
2. **Batch process:** Use Pandas for multiple documents
3. **Combine metrics:** Calculate weighted average
4. **Check metadata:** Use for debugging
5. **Normalize text:** For OCR error tolerance

---

**Quick Command:**

```bash
python examples/textract_evaluation_example.py
```

Runs 6 examples with detailed output! 🎉
