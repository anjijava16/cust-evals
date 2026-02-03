"""
Example: Evaluating AWS Textract outputs using cust-evals framework.

This example demonstrates how to use the custom evaluation framework
for non-LLM use cases, specifically AWS Textract document extraction.
"""

import pandas as pd
from typing import Dict, Any, List
from custom.evals.metrics.ocr_metrics import (
    text_extraction_accuracy,
    character_error_rate,
    word_error_rate,
    bounding_box_iou,
    confidence_threshold,
    field_detection_accuracy
)


# ============================================================================
# Example 1: Single Text Extraction Evaluation
# ============================================================================

def example_text_extraction():
    """Evaluate a single text extraction result."""
    print("\n" + "="*60)
    print("Example 1: Single Text Extraction Evaluation")
    print("="*60)

    # Simulated Textract output
    textract_output = "Invoice Date: 12/31/2025\nTotal Amount: $1,234.56"
    ground_truth = "Invoice Date: 12/31/2025\nTotal Amount: $1,234.56"

    # Prepare evaluation input
    eval_input = {
        "output": textract_output,
        "expected": ground_truth
    }

    # Run evaluations
    accuracy_score = text_extraction_accuracy(eval_input)
    cer_score = character_error_rate(eval_input)
    wer_score = word_error_rate(eval_input)

    print(f"\n✓ Text Extraction Accuracy: {accuracy_score.score:.2%}")
    print(f"  Label: {accuracy_score.label}")
    print(f"  {accuracy_score.explanation}")

    print(f"\n✓ Character Error Rate: {cer_score.score:.2%}")
    print(f"  Label: {cer_score.label}")
    print(f"  {cer_score.explanation}")

    print(f"\n✓ Word Error Rate: {wer_score.score:.2%}")
    print(f"  Label: {wer_score.label}")
    print(f"  {wer_score.explanation}")


# ============================================================================
# Example 2: Bounding Box Evaluation
# ============================================================================

def example_bounding_box():
    """Evaluate bounding box detection accuracy."""
    print("\n" + "="*60)
    print("Example 2: Bounding Box IoU Evaluation")
    print("="*60)

    # Textract-style bounding box (normalized coordinates)
    predicted_bbox = {
        "Left": 0.1,
        "Top": 0.2,
        "Width": 0.3,
        "Height": 0.1
    }

    ground_truth_bbox = {
        "Left": 0.12,
        "Top": 0.19,
        "Width": 0.28,
        "Height": 0.11
    }

    eval_input = {
        "output_bbox": predicted_bbox,
        "expected_bbox": ground_truth_bbox
    }

    iou_score = bounding_box_iou(eval_input)

    print(f"\n✓ Bounding Box IoU: {iou_score.score:.2%}")
    print(f"  Label: {iou_score.label}")
    print(f"  {iou_score.explanation}")
    print(f"  Metadata: {iou_score.metadata}")


# ============================================================================
# Example 3: Confidence Score Validation
# ============================================================================

def example_confidence():
    """Validate Textract confidence scores."""
    print("\n" + "="*60)
    print("Example 3: Confidence Score Validation")
    print("="*60)

    # Textract returns confidence as 0-100
    textract_confidence = 92.5

    eval_input = {
        "confidence": textract_confidence,
        "threshold": 0.85  # 85% minimum confidence
    }

    conf_score = confidence_threshold(eval_input)

    print(f"\n✓ Confidence Check: {conf_score.label.upper()}")
    print(f"  Score: {conf_score.score}")
    print(f"  {conf_score.explanation}")


# ============================================================================
# Example 4: Form Field Detection Evaluation
# ============================================================================

def example_field_detection():
    """Evaluate form field detection accuracy."""
    print("\n" + "="*60)
    print("Example 4: Form Field Detection Accuracy")
    print("="*60)

    detected_fields = [
        "Invoice Number",
        "Invoice Date",
        "Total Amount",
        "Customer Name",
        "Payment Terms"  # Extra field detected
    ]

    expected_fields = [
        "Invoice Number",
        "Invoice Date",
        "Total Amount",
        "Customer Name",
        "Due Date"  # This was missed
    ]

    eval_input = {
        "detected_fields": detected_fields,
        "expected_fields": expected_fields
    }

    field_score = field_detection_accuracy(eval_input)

    print(f"\n✓ Field Detection F1 Score: {field_score.score:.2%}")
    print(f"  Label: {field_score.label}")
    print(f"  {field_score.explanation}")
    print(f"\n  Missing Fields: {field_score.metadata['missing_fields']}")
    print(f"  Extra Fields: {field_score.metadata['extra_fields']}")


# ============================================================================
# Example 5: Batch Evaluation with Pandas
# ============================================================================

def example_batch_evaluation():
    """Evaluate multiple Textract outputs in batch."""
    print("\n" + "="*60)
    print("Example 5: Batch Evaluation with Pandas")
    print("="*60)

    # Sample dataset
    data = {
        "document_id": ["doc_001", "doc_002", "doc_003"],
        "textract_output": [
            "Invoice #12345",
            "Invoice #67890",
            "Invoice #11223"
        ],
        "ground_truth": [
            "Invoice #12345",
            "Invoice #67890",
            "Invoice #11223"  # Exact match
        ],
        "confidence": [95.2, 87.3, 72.1]
    }

    df = pd.DataFrame(data)

    # Apply evaluations
    def evaluate_row(row):
        eval_input = {
            "output": row["textract_output"],
            "expected": row["ground_truth"]
        }

        acc_score = text_extraction_accuracy(eval_input)
        cer_score = character_error_rate(eval_input)

        conf_input = {
            "confidence": row["confidence"],
            "threshold": 0.80
        }
        conf_score = confidence_threshold(conf_input)

        return pd.Series({
            "accuracy": acc_score.score,
            "accuracy_label": acc_score.label,
            "cer": cer_score.metadata["raw_cer"],
            "confidence_pass": conf_score.label
        })

    results = df.apply(evaluate_row, axis=1)
    df_results = pd.concat([df, results], axis=1)

    print("\nBatch Evaluation Results:")
    print(df_results.to_string(index=False))

    print(f"\nAggregate Statistics:")
    print(f"  Mean Accuracy: {df_results['accuracy'].mean():.2%}")
    print(f"  Mean CER: {df_results['cer'].mean():.2%}")
    print(f"  Confidence Pass Rate: "
          f"{(df_results['confidence_pass'] == 'pass').sum()}/{len(df_results)}")


# ============================================================================
# Example 6: Complete Textract Pipeline Evaluation
# ============================================================================

def example_complete_pipeline():
    """Simulate a complete Textract evaluation pipeline."""
    print("\n" + "="*60)
    print("Example 6: Complete Textract Pipeline Evaluation")
    print("="*60)

    # Simulated Textract API response
    textract_response = {
        "document_id": "invoice_001.pdf",
        "extracted_text": "INVOICE\nDate: 2025-02-01\nAmount: $500.00",
        "confidence": 94.5,
        "bounding_boxes": {
            "date_field": {"Left": 0.1, "Top": 0.2, "Width": 0.2, "Height": 0.05}
        },
        "detected_fields": ["Date", "Amount", "Total"]
    }

    # Ground truth
    ground_truth = {
        "expected_text": "INVOICE\nDate: 2025-02-01\nAmount: $500.00",
        "expected_bbox": {
            "date_field": {"Left": 0.11, "Top": 0.19, "Width": 0.19, "Height": 0.06}
        },
        "expected_fields": ["Date", "Amount", "Invoice Number"]
    }

    # Run all evaluations
    scores = []

    # Text accuracy
    text_eval = {
        "output": textract_response["extracted_text"],
        "expected": ground_truth["expected_text"]
    }
    scores.append(text_extraction_accuracy(text_eval))
    scores.append(word_error_rate(text_eval))

    # Bounding box
    bbox_eval = {
        "output_bbox": textract_response["bounding_boxes"]["date_field"],
        "expected_bbox": ground_truth["expected_bbox"]["date_field"]
    }
    scores.append(bounding_box_iou(bbox_eval))

    # Confidence
    conf_eval = {
        "confidence": textract_response["confidence"],
        "threshold": 0.90
    }
    scores.append(confidence_threshold(conf_eval))

    # Field detection
    field_eval = {
        "detected_fields": textract_response["detected_fields"],
        "expected_fields": ground_truth["expected_fields"]
    }
    scores.append(field_detection_accuracy(field_eval))

    # Display results
    print(f"\nDocument: {textract_response['document_id']}")
    print("\nEvaluation Results:")
    print("-" * 60)

    for score in scores:
        print(f"\n{score.name}:")
        print(f"  Score: {score.score:.2%}")
        print(f"  Label: {score.label}")
        print(f"  {score.explanation}")

    # Calculate overall score (weighted average)
    overall_score = sum(s.score for s in scores) / len(scores)
    print(f"\n{'='*60}")
    print(f"Overall Document Quality Score: {overall_score:.2%}")
    print(f"{'='*60}")


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("AWS TEXTRACT EVALUATION EXAMPLES")
    print("Using cust-evals framework for non-LLM evaluation")
    print("="*60)

    # Run all examples
    example_text_extraction()
    example_bounding_box()
    example_confidence()
    example_field_detection()
    example_batch_evaluation()
    example_complete_pipeline()

    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60 + "\n")
