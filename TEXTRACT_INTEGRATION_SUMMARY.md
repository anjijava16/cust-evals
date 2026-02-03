# AWS Textract Integration Summary

## Overview

Your `cust-evals` framework has been successfully extended to support **non-LLM evaluation**, specifically for AWS Textract and other OCR/document extraction services. The framework maintains its original LLM evaluation capabilities while adding a complete suite of deterministic metrics for document extraction.

---

## What Was Added

### 1. New OCR Metrics Module

**File:** `src/custom/evals/metrics/ocr_metrics.py` (500+ lines)

Six production-ready metrics for evaluating document extraction:

| Metric | Purpose | Returns | Best For |
|--------|---------|---------|----------|
| `text_extraction_accuracy` | Fuzzy string matching | 0.0-1.0 (higher=better) | Overall text quality |
| `character_error_rate` | Levenshtein distance (char-level) | 0.0-1.0 (inverted) | Character-level precision |
| `word_error_rate` | Levenshtein distance (word-level) | 0.0-1.0 (inverted) | Word-level accuracy |
| `bounding_box_iou` | Intersection over Union | 0.0-1.0 | Spatial accuracy |
| `confidence_threshold` | Quality gating | 1.0 (pass) or 0.0 (fail) | Filtering low-quality results |
| `field_detection_accuracy` | F1 score for form fields | 0.0-1.0 | Structured forms |

**Key Features:**
- Uses existing `@create_evaluator` decorator for consistency
- Returns standard `Score` objects for easy composition
- Supports field mapping for different OCR providers
- Includes helper classes (`BoundingBox`) and utilities

---

### 2. Comprehensive Examples

**File:** `examples/textract_evaluation_example.py` (400+ lines)

Six practical examples:
1. **Single text extraction** - Basic usage
2. **Bounding box evaluation** - Spatial accuracy
3. **Confidence validation** - Quality gating
4. **Form field detection** - Structured documents
5. **Batch processing** - Pandas integration
6. **Complete pipeline** - End-to-end workflow

**Run it:**
```bash
python examples/textract_evaluation_example.py
```

---

### 3. Documentation

#### Complete Guide
**File:** `docs/NON_LLM_EVALUATION_GUIDE.md` (800+ lines)

Comprehensive documentation including:
- Overview and architecture
- Detailed metric descriptions with examples
- AWS Textract integration patterns
- Batch evaluation with Pandas
- Custom metric creation guide
- Best practices and troubleshooting

#### Quick Start Guide
**File:** `docs/TEXTRACT_QUICKSTART.md` (400+ lines)

Get started in 5 minutes:
- Minimal working example
- Data format specifications
- Common usage patterns
- Field mapping examples
- Troubleshooting tips

---

### 4. Test Suite

**File:** `tests/test_ocr_metrics.py` (400+ lines)

Comprehensive test coverage:
- 10 test classes
- 40+ test cases
- Tests for all metrics
- Helper function tests
- Score structure validation

**Run tests:**
```bash
pytest tests/test_ocr_metrics.py -v
```

---

### 5. Updated Dependencies

**File:** `pyproject.toml`

Added dependency:
```toml
dependencies = [
  "pandas",
  "typing-extensions>=4.5, <5",
  "pydantic>=2.0.0",
  "python-Levenshtein>=0.21.0",  # NEW - For OCR metrics
]
```

---

### 6. Updated Exports

**File:** `src/custom/evals/metrics/__init__.py`

All OCR metrics are now importable:
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

### 7. Updated README

**File:** `README.md`

Added sections:
- OCR/Document Extraction Metrics in features list
- Non-LLM Evaluation Guide in documentation links
- Textract Quick Start in user guides
- Textract example in quick examples

---

## How to Use

### Installation

```bash
# Navigate to your project
cd /path/to/cust-evals

# Install dependencies
pip install -e .
```

This installs all dependencies including `python-Levenshtein`.

---

### Minimal Example

```python
from custom.evals.metrics import (
    text_extraction_accuracy,
    character_error_rate,
    confidence_threshold
)

# Your Textract output
textract_output = "Invoice Number: INV-2025-001"
ground_truth = "Invoice Number: INV-2025-001"

# Evaluate
eval_input = {
    "output": textract_output,
    "expected": ground_truth
}

accuracy = text_extraction_accuracy(eval_input)
cer = character_error_rate(eval_input)

print(f"Accuracy: {accuracy.score:.2%} ({accuracy.label})")
print(f"CER: {cer.metadata['raw_cer']:.2%}")
```

---

### AWS Textract Integration

```python
import boto3
from custom.evals.metrics import text_extraction_accuracy, bounding_box_iou

# Call Textract
textract = boto3.client('textract', region_name='us-east-1')
response = textract.detect_document_text(
    Document={'S3Object': {'Bucket': 'my-bucket', 'Name': 'doc.pdf'}}
)

# Extract text
extracted_text = "\n".join([
    block['Text']
    for block in response['Blocks']
    if block['BlockType'] == 'LINE'
])

# Evaluate
eval_input = {
    "output": extracted_text,
    "expected": ground_truth_text
}

score = text_extraction_accuracy(eval_input)
print(f"Text Accuracy: {score.score:.2%} ({score.label})")
```

---

### Batch Processing

```python
import pandas as pd
from custom.evals.metrics import text_extraction_accuracy

# Load dataset
df = pd.DataFrame({
    "doc_id": ["doc1", "doc2", "doc3"],
    "textract_output": ["...", "...", "..."],
    "ground_truth": ["...", "...", "..."]
})

# Evaluate
def eval_row(row):
    score = text_extraction_accuracy({
        "output": row["textract_output"],
        "expected": row["ground_truth"]
    })
    return score.score

df["accuracy"] = df.apply(eval_row, axis=1)

print(f"Mean Accuracy: {df['accuracy'].mean():.2%}")
```

---

## Architecture Integration

### Before (LLM-Centric)

```
cust-evals/
├── src/custom/evals/
│   ├── evaluators.py           # Core Score, @create_evaluator
│   ├── llm_evaluators.py       # LLM-based evaluators
│   └── metrics/
│       ├── exact_match.py
│       ├── accuracy.py
│       └── sentiment.py
```

### After (LLM + Non-LLM)

```
cust-evals/
├── src/custom/evals/
│   ├── evaluators.py           # Core Score, @create_evaluator
│   ├── llm_evaluators.py       # LLM-based evaluators
│   └── metrics/
│       ├── exact_match.py
│       ├── accuracy.py
│       ├── sentiment.py
│       └── ocr_metrics.py      # NEW - OCR/Textract metrics
│
├── examples/
│   └── textract_evaluation_example.py  # NEW
│
├── tests/
│   └── test_ocr_metrics.py     # NEW
│
└── docs/
    ├── NON_LLM_EVALUATION_GUIDE.md     # NEW
    └── TEXTRACT_QUICKSTART.md          # NEW
```

---

## Key Design Decisions

### 1. Reused Existing Framework

✅ **Leveraged `@create_evaluator` decorator**
- All metrics return standard `Score` objects
- Consistent API across LLM and non-LLM metrics
- Easy to compose multiple metrics

### 2. Zero LLM Dependency

✅ **Code-based metrics path**
- No API keys required
- Fast, deterministic evaluation
- Works offline

### 3. Flexible Field Mapping

✅ **Supports different OCR providers**
```python
# Works with any field names
field_mapping = {
    "output": "prediction",
    "expected": "reference"
}
```

### 4. Rich Metadata

✅ **Detailed debugging information**
```python
score.metadata = {
    "raw_cer": 0.05,
    "edit_distance": 3,
    "output_length": 60,
    "expected_length": 63,
    "missing_fields": ["Field3"],
    "extra_fields": ["Field4"]
}
```

### 5. Normalization Options

✅ **OCR-tolerant matching**
```python
text_extraction_accuracy(
    eval_input,
    normalize=True,        # Remove punctuation, whitespace
    case_sensitive=False   # Ignore case
)
```

---

## What's NOT Changed

✅ **Existing LLM functionality unchanged**
- All LLM-based evaluators work as before
- No breaking changes
- Backward compatible

✅ **Code-based metrics unchanged**
- `exact_match`, `custom_accuracy`, `sentiment_score` work as before

✅ **Project structure unchanged**
- Only added new files
- No modifications to core architecture

---

## Missing Features (Future Enhancements)

If needed in the future, you could add:

1. **Table Structure Evaluation**
   - Row/column detection accuracy
   - Cell boundary accuracy

2. **Multi-Page Document Metrics**
   - Page-level accuracy
   - Cross-page consistency

3. **Language-Specific Metrics**
   - Right-to-left text support
   - Unicode normalization

4. **Image Quality Metrics**
   - Blur detection
   - Skew correction validation

5. **OCR Provider Adapters**
   - Google Cloud Vision adapter
   - Azure Form Recognizer adapter
   - Tesseract adapter

---

## File Manifest

**New Files Created:**

1. `src/custom/evals/metrics/ocr_metrics.py` - 500+ lines
2. `examples/textract_evaluation_example.py` - 400+ lines
3. `docs/NON_LLM_EVALUATION_GUIDE.md` - 800+ lines
4. `docs/TEXTRACT_QUICKSTART.md` - 400+ lines
5. `tests/test_ocr_metrics.py` - 400+ lines
6. `TEXTRACT_INTEGRATION_SUMMARY.md` - This file

**Modified Files:**

1. `src/custom/evals/metrics/__init__.py` - Added OCR metric exports
2. `pyproject.toml` - Added `python-Levenshtein` dependency
3. `README.md` - Added non-LLM evaluation documentation links

**Total:** 6 new files, 3 modified files, ~2,900+ lines of code and documentation

---

## Next Steps

### 1. Install Dependencies

```bash
cd /path/to/cust-evals
pip install -e .
```

### 2. Run Examples

```bash
# Run all Textract examples
python examples/textract_evaluation_example.py

# Expected output: 6 examples with detailed metrics
```

### 3. Run Tests

```bash
# Run OCR metrics tests
pytest tests/test_ocr_metrics.py -v

# Run all tests
pytest tests/ -v
```

### 4. Try with Your Data

```python
from custom.evals.metrics import text_extraction_accuracy

# Replace with your Textract output
your_textract_output = "..."
your_ground_truth = "..."

eval_input = {
    "output": your_textract_output,
    "expected": your_ground_truth
}

score = text_extraction_accuracy(eval_input)
print(f"Score: {score.score:.2%} ({score.label})")
print(f"Explanation: {score.explanation}")
```

### 5. Create Custom Metrics (Optional)

See `docs/NON_LLM_EVALUATION_GUIDE.md` section "Custom Metrics" for examples.

---

## Support for Other OCR Services

While designed for AWS Textract, the metrics work with **any OCR service**:

### Google Cloud Vision

```python
from google.cloud import vision

client = vision.ImageAnnotatorClient()
response = client.text_detection(image=image)

eval_input = {
    "output": response.text_annotations[0].description,
    "expected": ground_truth
}

score = text_extraction_accuracy(eval_input)
```

### Azure Form Recognizer

```python
from azure.ai.formrecognizer import DocumentAnalysisClient

client = DocumentAnalysisClient(endpoint=endpoint, credential=credential)
poller = client.begin_analyze_document("prebuilt-document", document)
result = poller.result()

eval_input = {
    "output": result.content,
    "expected": ground_truth
}

score = text_extraction_accuracy(eval_input)
```

### Tesseract OCR

```python
import pytesseract

text = pytesseract.image_to_string(image)

eval_input = {
    "output": text,
    "expected": ground_truth
}

score = text_extraction_accuracy(eval_input)
```

---

## Summary

Your `cust-evals` framework now supports:

✅ **LLM Evaluation** (Original)
- OpenAI, Anthropic
- Coherence, Relevance, Correctness, etc.
- RAG-specific metrics

✅ **Non-LLM Evaluation** (NEW)
- AWS Textract, Google Vision, Azure, Tesseract
- 6 OCR-specific metrics
- Deterministic, no API keys needed

✅ **Production Ready**
- Comprehensive tests
- Full documentation
- Working examples
- Backward compatible

**The framework is now truly generic and can evaluate ANY output (LLM or non-LLM) against ground truth.**

---

## Questions or Issues?

- **Read the guide:** `docs/NON_LLM_EVALUATION_GUIDE.md`
- **Quick start:** `docs/TEXTRACT_QUICKSTART.md`
- **Run examples:** `python examples/textract_evaluation_example.py`
- **Run tests:** `pytest tests/test_ocr_metrics.py -v`

Enjoy evaluating your AWS Textract outputs! 🎉
