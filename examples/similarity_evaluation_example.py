"""
Comprehensive examples for using text similarity metrics.

This script demonstrates how to use all 7 similarity metrics for:
1. Exact and fuzzy text matching
2. Similarity search evaluation
3. Text comparison workflows
4. Batch processing

Run: python examples/similarity_evaluation_example.py
"""

from custom.evals.metrics import (
    similarity_exact_match,
    case_insensitive_match,
    normalized_match,
    sequence_similarity,
    word_overlap,
    contains_match,
    length_similarity
)


def example_1_basic_matching():
    """Example 1: Basic text matching with different strictness levels."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Text Matching")
    print("="*80)

    output = "Hello, World!"
    expected = "hello world"

    eval_input = {
        "output": output,
        "expected": expected
    }

    print(f"\nComparing:")
    print(f"  Output:   '{output}'")
    print(f"  Expected: '{expected}'")
    print("\nResults:")

    # Exact match (strict)
    score1 = similarity_exact_match(eval_input)
    print(f"  Exact Match:          {score1.score:.0f} ({score1.label})")

    # Case insensitive
    score2 = case_insensitive_match(eval_input)
    print(f"  Case Insensitive:     {score2.score:.0f} ({score2.label})")

    # Normalized (most lenient)
    score3 = normalized_match(eval_input)
    print(f"  Normalized Match:     {score3.score:.0f} ({score3.label})")


def example_2_fuzzy_matching():
    """Example 2: Fuzzy matching with similarity scores."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Fuzzy Matching")
    print("="*80)

    test_cases = [
        {
            "output": "The quick brown fox jumps over the lazy dog",
            "expected": "The quick brown fox jumped over the lazy dog"
        },
        {
            "output": "Machine learning is awesome",
            "expected": "Deep learning is amazing"
        },
        {
            "output": "Python programming",
            "expected": "Python coding"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Output:   '{test_case['output']}'")
        print(f"Expected: '{test_case['expected']}'")

        # Sequence similarity
        seq_score = sequence_similarity(test_case)
        print(f"  Sequence Similarity: {seq_score.score:.2%} ({seq_score.label})")

        # Word overlap
        word_score = word_overlap(test_case)
        print(f"  Word Overlap:        {word_score.score:.2%} ({word_score.label})")
        print(f"    Common words: {word_score.metadata['common_words']}")


def example_3_partial_matching():
    """Example 3: Partial matching and containment."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Partial Matching & Containment")
    print("="*80)

    test_cases = [
        {
            "name": "Output contains expected",
            "output": "The Python programming language is widely used for data science",
            "expected": "Python programming"
        },
        {
            "name": "Expected contains output",
            "output": "ML",
            "expected": "Machine Learning and Deep Learning"
        },
        {
            "name": "No containment",
            "output": "Database systems",
            "expected": "Web development"
        }
    ]

    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        print(f"Output:   '{test_case['output']}'")
        print(f"Expected: '{test_case['expected']}'")

        eval_input = {
            "output": test_case["output"],
            "expected": test_case["expected"]
        }

        score = contains_match(eval_input)
        print(f"  Contains Match: {score.score:.0f} ({score.label})")
        print(f"  {score.explanation}")


def example_4_length_validation():
    """Example 4: Length similarity for detecting truncation."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Length Similarity")
    print("="*80)

    test_cases = [
        {
            "name": "Similar lengths",
            "output": "Hello World",
            "expected": "Hello Earth"
        },
        {
            "name": "Truncated output",
            "output": "Hello",
            "expected": "Hello World, this is a long message"
        },
        {
            "name": "Verbose output",
            "output": "This is a very long and detailed explanation",
            "expected": "Short answer"
        }
    ]

    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        print(f"Output:   '{test_case['output']}' ({len(test_case['output'])} chars)")
        print(f"Expected: '{test_case['expected']}' ({len(test_case['expected'])} chars)")

        eval_input = {
            "output": test_case["output"],
            "expected": test_case["expected"]
        }

        score = length_similarity(eval_input)
        print(f"  Length Similarity: {score.score:.2%} ({score.label})")
        print(f"  Difference: {score.metadata['length_difference']} chars")


def example_5_search_evaluation():
    """Example 5: Evaluating similarity search results."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Similarity Search Evaluation")
    print("="*80)

    # Simulated search scenario
    query = "What is machine learning?"
    ground_truth = "Machine learning is a subset of artificial intelligence"

    # Different retrieval results
    retrieved_results = [
        "Machine learning is a subset of artificial intelligence",  # Perfect match
        "ML is a subset of AI that enables computers to learn",     # Good match
        "Deep learning is a type of neural network",                # Partial match
        "Python is a programming language"                          # Poor match
    ]

    print(f"\nQuery: '{query}'")
    print(f"Ground Truth: '{ground_truth}'")
    print("\n" + "-"*80)

    for i, result in enumerate(retrieved_results, 1):
        print(f"\nResult {i}: '{result}'")

        eval_input = {
            "output": result,
            "expected": ground_truth
        }

        # Use multiple metrics for comprehensive evaluation
        seq_score = sequence_similarity(eval_input)
        word_score = word_overlap(eval_input)

        # Combined score (weighted average)
        combined_score = (seq_score.score * 0.6 + word_score.score * 0.4)

        print(f"  Sequence Similarity: {seq_score.score:.2%}")
        print(f"  Word Overlap:        {word_score.score:.2%}")
        print(f"  Combined Score:      {combined_score:.2%}")

        # Relevance assessment
        if combined_score >= 0.8:
            print(f"  Assessment: ✓ Highly relevant")
        elif combined_score >= 0.5:
            print(f"  Assessment: ~ Moderately relevant")
        else:
            print(f"  Assessment: ✗ Not relevant")


def example_6_batch_evaluation():
    """Example 6: Batch evaluation with multiple metrics."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Batch Evaluation")
    print("="*80)

    # Sample dataset
    dataset = [
        {
            "id": "doc_001",
            "output": "Python is a programming language",
            "expected": "Python is a programming language"
        },
        {
            "id": "doc_002",
            "output": "Machine learning is a subset of AI",
            "expected": "Machine Learning is a subset of Artificial Intelligence"
        },
        {
            "id": "doc_003",
            "output": "Data science uses statistical methods",
            "expected": "Data scientists use statistics"
        },
        {
            "id": "doc_004",
            "output": "Neural networks are inspired by the brain",
            "expected": "Deep neural networks mimic human brain structure"
        }
    ]

    print(f"\nEvaluating {len(dataset)} documents...")
    print("\n" + "-"*80)

    results = []

    for item in dataset:
        eval_input = {
            "output": item["output"],
            "expected": item["expected"]
        }

        # Run all metrics
        exact = similarity_exact_match(eval_input)
        case_ins = case_insensitive_match(eval_input)
        normalized = normalized_match(eval_input)
        seq_sim = sequence_similarity(eval_input)
        word_ov = word_overlap(eval_input)
        contains = contains_match(eval_input)
        len_sim = length_similarity(eval_input)

        # Calculate overall score (weighted average)
        overall_score = (
            exact.score * 0.05 +
            case_ins.score * 0.05 +
            normalized.score * 0.10 +
            seq_sim.score * 0.35 +
            word_ov.score * 0.25 +
            contains.score * 0.10 +
            len_sim.score * 0.10
        )

        result = {
            "id": item["id"],
            "exact_match": exact.score,
            "sequence_similarity": seq_sim.score,
            "word_overlap": word_ov.score,
            "overall_score": overall_score
        }

        results.append(result)

        print(f"\n{item['id']}:")
        print(f"  Exact Match:         {exact.score:.0f}")
        print(f"  Sequence Similarity: {seq_sim.score:.2%}")
        print(f"  Word Overlap:        {word_ov.score:.2%}")
        print(f"  Overall Score:       {overall_score:.2%}")

    # Summary statistics
    print("\n" + "-"*80)
    print("SUMMARY STATISTICS")
    print("-"*80)

    avg_seq_sim = sum(r["sequence_similarity"] for r in results) / len(results)
    avg_word_ov = sum(r["word_overlap"] for r in results) / len(results)
    avg_overall = sum(r["overall_score"] for r in results) / len(results)
    exact_matches = sum(1 for r in results if r["exact_match"] == 1.0)

    print(f"Total documents:             {len(results)}")
    print(f"Exact matches:               {exact_matches}/{len(results)}")
    print(f"Avg. sequence similarity:    {avg_seq_sim:.2%}")
    print(f"Avg. word overlap:           {avg_word_ov:.2%}")
    print(f"Avg. overall score:          {avg_overall:.2%}")


def example_7_comprehensive_comparison():
    """Example 7: Comprehensive text comparison with all metrics."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Comprehensive Text Comparison")
    print("="*80)

    output = "The Quick Brown Fox Jumps Over the Lazy Dog!"
    expected = "the quick brown fox jumped over the lazy dog"

    print(f"\nOutput:   '{output}'")
    print(f"Expected: '{expected}'")
    print("\n" + "-"*80)

    eval_input = {
        "output": output,
        "expected": expected
    }

    # Run all 7 metrics
    metrics = [
        ("Exact Match", similarity_exact_match(eval_input)),
        ("Case Insensitive", case_insensitive_match(eval_input)),
        ("Normalized Match", normalized_match(eval_input)),
        ("Sequence Similarity", sequence_similarity(eval_input)),
        ("Word Overlap", word_overlap(eval_input)),
        ("Contains Match", contains_match(eval_input)),
        ("Length Similarity", length_similarity(eval_input))
    ]

    for metric_name, score in metrics:
        status = "✓" if score.score >= 0.7 else "✗"
        print(f"{status} {metric_name:20s}: {score.score:.2%} ({score.label})")

    # Calculate weighted overall score
    weights = [0.05, 0.05, 0.10, 0.35, 0.25, 0.10, 0.10]
    overall = sum(score.score * weight for (_, score), weight in zip(metrics, weights))

    print("-"*80)
    print(f"Overall Weighted Score: {overall:.2%}")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("TEXT SIMILARITY METRICS - COMPREHENSIVE EXAMPLES")
    print("="*80)

    example_1_basic_matching()
    example_2_fuzzy_matching()
    example_3_partial_matching()
    example_4_length_validation()
    example_5_search_evaluation()
    example_6_batch_evaluation()
    example_7_comprehensive_comparison()

    print("\n" + "="*80)
    print("All examples completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
