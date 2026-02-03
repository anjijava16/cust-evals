"""
Verification script for similarity metrics installation and functionality.

This script tests that all 7 similarity metrics are properly installed
and working correctly.

Run: python verify_similarity_metrics.py
"""

import sys


def test_imports():
    """Test that all metrics can be imported."""
    print("Testing imports...")
    try:
        from custom.evals.metrics import (
            similarity_exact_match,
            case_insensitive_match,
            normalized_match,
            sequence_similarity,
            word_overlap,
            contains_match,
            length_similarity
        )
        print("✓ All metrics imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_exact_match():
    """Test exact match metric."""
    print("\nTesting exact_match...")
    from custom.evals.metrics import similarity_exact_match

    # Test case 1: Should match
    score1 = similarity_exact_match({
        "output": "Hello World",
        "expected": "Hello World"
    })
    assert score1.score == 1.0, f"Expected 1.0, got {score1.score}"
    assert score1.label == "match", f"Expected 'match', got {score1.label}"

    # Test case 2: Should not match
    score2 = similarity_exact_match({
        "output": "Hello World",
        "expected": "hello world"
    })
    assert score2.score == 0.0, f"Expected 0.0, got {score2.score}"
    assert score2.label == "no_match", f"Expected 'no_match', got {score2.label}"

    print("✓ exact_match working correctly")
    return True


def test_case_insensitive_match():
    """Test case insensitive match metric."""
    print("\nTesting case_insensitive_match...")
    from custom.evals.metrics import case_insensitive_match

    score = case_insensitive_match({
        "output": "Hello World",
        "expected": "hello world"
    })
    assert score.score == 1.0, f"Expected 1.0, got {score.score}"
    assert score.label == "match", f"Expected 'match', got {score.label}"

    print("✓ case_insensitive_match working correctly")
    return True


def test_normalized_match():
    """Test normalized match metric."""
    print("\nTesting normalized_match...")
    from custom.evals.metrics import normalized_match

    score = normalized_match({
        "output": "Hello,  World!!!",
        "expected": "hello world"
    })
    assert score.score == 1.0, f"Expected 1.0, got {score.score}"
    assert score.label == "match", f"Expected 'match', got {score.label}"

    print("✓ normalized_match working correctly")
    return True


def test_sequence_similarity():
    """Test sequence similarity metric."""
    print("\nTesting sequence_similarity...")
    from custom.evals.metrics import sequence_similarity

    # Perfect match
    score1 = sequence_similarity({
        "output": "Hello World",
        "expected": "Hello World"
    })
    assert score1.score == 1.0, f"Expected 1.0, got {score1.score}"
    assert score1.label == "excellent", f"Expected 'excellent', got {score1.label}"

    # Partial match
    score2 = sequence_similarity({
        "output": "The quick brown fox",
        "expected": "The quick brown dog"
    })
    assert 0.7 < score2.score < 0.9, f"Expected ~0.85, got {score2.score}"
    assert score2.metadata["similarity_ratio"] > 0, "Missing similarity_ratio in metadata"

    print("✓ sequence_similarity working correctly")
    return True


def test_word_overlap():
    """Test word overlap metric."""
    print("\nTesting word_overlap...")
    from custom.evals.metrics import word_overlap

    score = word_overlap({
        "output": "The quick brown fox",
        "expected": "The quick brown dog"
    })

    # Should have 75% overlap (3 out of 4 words: "the", "quick", "brown")
    assert 0.5 < score.score < 0.8, f"Expected ~0.75, got {score.score}"
    assert "common_words" in score.metadata, "Missing common_words in metadata"
    assert "missing_words" in score.metadata, "Missing missing_words in metadata"
    assert "extra_words" in score.metadata, "Missing extra_words in metadata"

    print("✓ word_overlap working correctly")
    return True


def test_contains_match():
    """Test contains match metric."""
    print("\nTesting contains_match...")
    from custom.evals.metrics import contains_match

    # Test: output contains expected
    score1 = contains_match({
        "output": "The quick brown fox jumps",
        "expected": "quick brown fox"
    })
    assert score1.score == 1.0, f"Expected 1.0, got {score1.score}"
    assert score1.label == "contains", f"Expected 'contains', got {score1.label}"
    assert score1.metadata["output_contains_expected"] == True

    # Test: no containment
    score2 = contains_match({
        "output": "Hello",
        "expected": "World"
    })
    assert score2.score == 0.0, f"Expected 0.0, got {score2.score}"
    assert score2.label == "no_containment", f"Expected 'no_containment', got {score2.label}"

    print("✓ contains_match working correctly")
    return True


def test_length_similarity():
    """Test length similarity metric."""
    print("\nTesting length_similarity...")
    from custom.evals.metrics import length_similarity

    # Same length
    score1 = length_similarity({
        "output": "Hello",
        "expected": "World"
    })
    assert score1.score == 1.0, f"Expected 1.0, got {score1.score}"

    # Different lengths
    score2 = length_similarity({
        "output": "Hello",       # 5 chars
        "expected": "Hello World" # 11 chars
    })
    expected_ratio = 5 / 11  # ~0.45
    assert abs(score2.score - expected_ratio) < 0.01, f"Expected ~{expected_ratio}, got {score2.score}"
    assert "length_difference" in score2.metadata, "Missing length_difference in metadata"

    print("✓ length_similarity working correctly")
    return True


def test_comprehensive_workflow():
    """Test a complete workflow using multiple metrics."""
    print("\nTesting comprehensive workflow...")
    from custom.evals.metrics import (
        sequence_similarity,
        word_overlap,
        normalized_match
    )

    test_data = [
        {
            "output": "Python is a programming language",
            "expected": "Python is a programming language"
        },
        {
            "output": "Machine learning is awesome",
            "expected": "Deep learning is amazing"
        }
    ]

    results = []
    for item in test_data:
        eval_input = {
            "output": item["output"],
            "expected": item["expected"]
        }

        seq_score = sequence_similarity(eval_input)
        word_score = word_overlap(eval_input)
        norm_score = normalized_match(eval_input)

        results.append({
            "sequence_sim": seq_score.score,
            "word_overlap": word_score.score,
            "normalized": norm_score.score
        })

    # First item should have perfect scores
    assert results[0]["sequence_sim"] == 1.0, "First item should have perfect sequence similarity"
    assert results[0]["word_overlap"] == 1.0, "First item should have perfect word overlap"
    assert results[0]["normalized"] == 1.0, "First item should have perfect normalized match"

    # Second item should have lower scores
    assert results[1]["sequence_sim"] < 0.8, "Second item should have lower sequence similarity"
    assert results[1]["word_overlap"] < 0.8, "Second item should have lower word overlap"

    print("✓ Comprehensive workflow working correctly")
    return True


def main():
    """Run all verification tests."""
    print("="*80)
    print("SIMILARITY METRICS VERIFICATION")
    print("="*80)

    tests = [
        ("Import Test", test_imports),
        ("Exact Match", test_exact_match),
        ("Case Insensitive Match", test_case_insensitive_match),
        ("Normalized Match", test_normalized_match),
        ("Sequence Similarity", test_sequence_similarity),
        ("Word Overlap", test_word_overlap),
        ("Contains Match", test_contains_match),
        ("Length Similarity", test_length_similarity),
        ("Comprehensive Workflow", test_comprehensive_workflow)
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name} failed: {e}")
            failed += 1

    print("\n" + "="*80)
    print("VERIFICATION RESULTS")
    print("="*80)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")

    if failed == 0:
        print("\n✓ All similarity metrics are working correctly!")
        print("\nNext steps:")
        print("1. Run examples: python examples/similarity_evaluation_example.py")
        print("2. Read the guide: docs/NON_LLM_EVALUATION_GUIDE.md")
        print("3. Check quick reference: docs/SIMILARITY_METRICS_QUICKSTART.md")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
