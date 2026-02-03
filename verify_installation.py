#!/usr/bin/env python3
"""
Verification script for OCR metrics installation.

Run this to verify that all OCR metrics are properly installed and working.
"""

import sys


def verify_imports():
    """Verify all OCR metrics can be imported."""
    print("=" * 60)
    print("Step 1: Verifying imports...")
    print("=" * 60)

    try:
        from custom.evals.metrics import (
            text_extraction_accuracy,
            character_error_rate,
            word_error_rate,
            bounding_box_iou,
            confidence_threshold,
            field_detection_accuracy
        )
        print("✓ All OCR metrics imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        print("\nTry running: pip install -e .")
        return False


def verify_dependencies():
    """Verify required dependencies are installed."""
    print("\n" + "=" * 60)
    print("Step 2: Verifying dependencies...")
    print("=" * 60)

    required = {
        "pandas": "pandas",
        "pydantic": "pydantic",
        "Levenshtein": "python-Levenshtein"
    }

    all_ok = True
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            print(f"  Install with: pip install {package}")
            all_ok = False

    return all_ok


def verify_basic_functionality():
    """Verify basic functionality works."""
    print("\n" + "=" * 60)
    print("Step 3: Verifying basic functionality...")
    print("=" * 60)

    try:
        from custom.evals.metrics import (
            text_extraction_accuracy,
            character_error_rate,
            bounding_box_iou
        )

        # Test 1: Text extraction accuracy
        eval_input = {
            "output": "Hello World",
            "expected": "Hello World"
        }
        score = text_extraction_accuracy(eval_input)
        assert score.score == 1.0, "Expected perfect score"
        print("✓ text_extraction_accuracy works correctly")

        # Test 2: Character error rate
        score = character_error_rate(eval_input)
        assert score.score == 1.0, "Expected perfect score"
        assert score.metadata["raw_cer"] == 0.0, "Expected 0% error rate"
        print("✓ character_error_rate works correctly")

        # Test 3: Bounding box IoU
        bbox = {"Left": 0.1, "Top": 0.2, "Width": 0.3, "Height": 0.1}
        bbox_input = {
            "output_bbox": bbox,
            "expected_bbox": bbox
        }
        score = bounding_box_iou(bbox_input)
        assert score.score == 1.0, "Expected perfect IoU"
        print("✓ bounding_box_iou works correctly")

        return True

    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_score_structure():
    """Verify Score object structure is correct."""
    print("\n" + "=" * 60)
    print("Step 4: Verifying Score object structure...")
    print("=" * 60)

    try:
        from custom.evals.metrics import text_extraction_accuracy

        eval_input = {
            "output": "test",
            "expected": "test"
        }
        score = text_extraction_accuracy(eval_input)

        # Check required attributes
        required_attrs = [
            "score", "name", "label", "explanation",
            "direction", "kind", "metadata"
        ]

        for attr in required_attrs:
            assert hasattr(score, attr), f"Missing attribute: {attr}"

        print(f"✓ Score object has all required attributes: {required_attrs}")

        # Check types
        assert isinstance(score.score, float), "score should be float"
        assert isinstance(score.name, str), "name should be str"
        assert isinstance(score.label, str), "label should be str"
        assert isinstance(score.metadata, dict), "metadata should be dict"

        print("✓ Score object attributes have correct types")

        # Check values
        assert score.direction in ["maximize", "minimize"], "Invalid direction"
        assert score.kind == "code", "Should be code-based metric"

        print("✓ Score object has correct values")

        return True

    except Exception as e:
        print(f"✗ Score structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_example():
    """Run a complete example."""
    print("\n" + "=" * 60)
    print("Step 5: Running complete example...")
    print("=" * 60)

    try:
        from custom.evals.metrics import (
            text_extraction_accuracy,
            character_error_rate,
            word_error_rate,
            confidence_threshold
        )

        # Simulated Textract output
        textract_output = "Invoice Date: 12/31/2025\nTotal Amount: $1,234.56"
        ground_truth = "Invoice Date: 12/31/2025\nTotal Amount: $1,234.56"

        # Text evaluations
        text_eval = {
            "output": textract_output,
            "expected": ground_truth
        }

        acc = text_extraction_accuracy(text_eval)
        cer = character_error_rate(text_eval)
        wer = word_error_rate(text_eval)

        # Confidence check
        conf_eval = {
            "confidence": 94.5,
            "threshold": 0.90
        }
        conf = confidence_threshold(conf_eval)

        # Display results
        print("\nResults:")
        print(f"  Text Accuracy: {acc.score:.2%} ({acc.label})")
        print(f"  CER: {cer.metadata['raw_cer']:.2%}")
        print(f"  WER: {wer.metadata['raw_wer']:.2%}")
        print(f"  Confidence: {conf.label.upper()}")

        print("\n✓ Complete example ran successfully")
        return True

    except Exception as e:
        print(f"✗ Example failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verification steps."""
    print("\n" + "=" * 60)
    print("OCR METRICS INSTALLATION VERIFICATION")
    print("=" * 60 + "\n")

    results = {
        "imports": verify_imports(),
        "dependencies": verify_dependencies(),
        "functionality": verify_basic_functionality(),
        "score_structure": verify_score_structure(),
        "example": run_example()
    }

    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    for test, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test}")

    all_passed = all(results.values())

    print("\n" + "=" * 60)
    if all_passed:
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("=" * 60)
        print("\nYour OCR metrics installation is working correctly!")
        print("\nNext steps:")
        print("  1. Run examples: python examples/textract_evaluation_example.py")
        print("  2. Run tests: pytest tests/test_ocr_metrics.py -v")
        print("  3. Read the guide: docs/NON_LLM_EVALUATION_GUIDE.md")
    else:
        print("✗✗✗ SOME TESTS FAILED ✗✗✗")
        print("=" * 60)
        print("\nPlease fix the issues above and try again.")
        print("\nCommon fixes:")
        print("  1. Install package: pip install -e .")
        print("  2. Install dependencies: pip install python-Levenshtein")
        print("  3. Check Python version: python --version (need >=3.8)")

    print("\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
