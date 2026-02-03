"""
Quick Start: Using Similarity Metrics for Non-LLM Evaluation

This is the simplest example to get started with similarity metrics.
Perfect for: similarity search, text comparison, fuzzy matching

Run: python examples/quick_start_similarity.py
"""

from custom.evals.metrics import (
    sequence_similarity,
    word_overlap,
    normalized_match
)


def evaluate_single_comparison():
    """Example 1: Compare a single output against ground truth."""
    print("="*80)
    print("Example 1: Single Comparison")
    print("="*80)

    # Your data: output from your system and expected ground truth
    output = "The Python programming language is great for data science"
    ground_truth = "Python is an excellent language for data science tasks"

    # Prepare evaluation input
    eval_input = {
        "output": output,
        "expected": ground_truth
    }

    # Run similarity metrics
    seq_score = sequence_similarity(eval_input)
    word_score = word_overlap(eval_input)

    # Print results
    print(f"\nOutput:   {output}")
    print(f"Expected: {ground_truth}")
    print(f"\nResults:")
    print(f"  Sequence Similarity: {seq_score.score:.2%} ({seq_score.label})")
    print(f"  Word Overlap:        {word_score.score:.2%} ({word_score.label})")

    # Combined assessment
    combined = (seq_score.score * 0.6) + (word_score.score * 0.4)
    print(f"  Combined Score:      {combined:.2%}")

    if combined >= 0.8:
        print("  ✓ High similarity - Good match!")
    elif combined >= 0.6:
        print("  ~ Moderate similarity")
    else:
        print("  ✗ Low similarity - May not match")


def evaluate_batch():
    """Example 2: Batch evaluation of multiple items."""
    print("\n" + "="*80)
    print("Example 2: Batch Evaluation")
    print("="*80)

    # Your dataset
    data = [
        {
            "id": 1,
            "output": "Machine learning algorithms learn from data",
            "ground_truth": "ML algorithms learn from data"
        },
        {
            "id": 2,
            "output": "Python is a programming language",
            "ground_truth": "Python is a programming language"
        },
        {
            "id": 3,
            "output": "Deep neural networks are powerful",
            "ground_truth": "Shallow decision trees are simple"
        }
    ]

    print(f"\nEvaluating {len(data)} items...\n")

    results = []

    for item in data:
        eval_input = {
            "output": item["output"],
            "expected": item["ground_truth"]
        }

        # Run metrics
        seq_score = sequence_similarity(eval_input)
        word_score = word_overlap(eval_input)

        # Store results
        result = {
            "id": item["id"],
            "sequence_sim": seq_score.score,
            "word_overlap": word_score.score,
            "avg_score": (seq_score.score + word_score.score) / 2
        }
        results.append(result)

        # Print individual result
        print(f"Item {item['id']}:")
        print(f"  Sequence Similarity: {seq_score.score:.2%}")
        print(f"  Word Overlap:        {word_score.score:.2%}")
        print(f"  Average:             {result['avg_score']:.2%}")
        print()

    # Summary statistics
    avg_seq = sum(r["sequence_sim"] for r in results) / len(results)
    avg_word = sum(r["word_overlap"] for r in results) / len(results)
    avg_overall = sum(r["avg_score"] for r in results) / len(results)

    print("-"*80)
    print("Summary:")
    print(f"  Avg Sequence Similarity: {avg_seq:.2%}")
    print(f"  Avg Word Overlap:        {avg_word:.2%}")
    print(f"  Avg Overall Score:       {avg_overall:.2%}")


def evaluate_search_results():
    """Example 3: Evaluate similarity search results."""
    print("\n" + "="*80)
    print("Example 3: Search Result Evaluation")
    print("="*80)

    # Scenario: You have a search query and want to rank results
    query = "What is machine learning?"
    ground_truth = "Machine learning is a subset of artificial intelligence"

    # Retrieved results from your search system
    search_results = [
        "Machine learning is a subset of artificial intelligence",
        "ML is a branch of AI that enables systems to learn",
        "Python is a programming language used for ML",
        "Database systems store structured data"
    ]

    print(f"\nQuery: {query}")
    print(f"Ground Truth: {ground_truth}\n")

    ranked_results = []

    for i, result in enumerate(search_results, 1):
        eval_input = {
            "output": result,
            "expected": ground_truth
        }

        # Calculate similarity
        seq_score = sequence_similarity(eval_input)
        word_score = word_overlap(eval_input)
        combined = (seq_score.score * 0.6) + (word_score.score * 0.4)

        ranked_results.append({
            "rank": i,
            "text": result,
            "score": combined
        })

    # Sort by score (descending)
    ranked_results.sort(key=lambda x: x["score"], reverse=True)

    print("Ranked Results:")
    for item in ranked_results:
        relevance = "✓ Relevant" if item["score"] >= 0.7 else "✗ Not relevant"
        print(f"  [{item['score']:.2%}] {relevance}")
        print(f"           {item['text'][:60]}...")
        print()


def simple_workflow():
    """Example 4: Simple workflow for your use case."""
    print("\n" + "="*80)
    print("Example 4: Simple Workflow Template")
    print("="*80)

    print("\nStep 1: Prepare your data")
    print("  - You have: input, output, and ground_truth")
    print("  - Create eval_input = {'output': ..., 'expected': ...}")

    print("\nStep 2: Choose metrics")
    print("  - sequence_similarity: Overall text similarity")
    print("  - word_overlap: Shared vocabulary")
    print("  - normalized_match: Exact match after normalization")

    print("\nStep 3: Run evaluation")
    print("  - Call metric functions with eval_input")
    print("  - Get Score object with .score, .label, .metadata")

    print("\nStep 4: Analyze results")
    print("  - Check score.score for numeric value (0.0-1.0)")
    print("  - Check score.label for quality ('excellent', 'good', etc.)")
    print("  - Use score.metadata for debugging")

    print("\nStep 5: Aggregate (optional)")
    print("  - Combine multiple metrics with weighted average")
    print("  - Calculate statistics across batches")

    print("\n" + "-"*80)
    print("Template Code:")
    print("-"*80)
    print("""
from custom.evals.metrics import sequence_similarity, word_overlap

# Your data
eval_input = {
    "output": your_system_output,
    "expected": ground_truth_data
}

# Evaluate
score1 = sequence_similarity(eval_input)
score2 = word_overlap(eval_input)

# Combine
overall = (score1.score * 0.6) + (score2.score * 0.4)

# Decide
if overall >= 0.8:
    print("High quality match")
elif overall >= 0.6:
    print("Acceptable match")
else:
    print("Low quality match")
""")


def main():
    """Run all quick start examples."""
    print("\n" + "="*80)
    print("QUICK START: Similarity Metrics for Non-LLM Evaluation")
    print("="*80)
    print("\nThese metrics help you compare outputs against ground truth")
    print("Perfect for: search, text comparison, similarity detection")
    print()

    evaluate_single_comparison()
    evaluate_batch()
    evaluate_search_results()
    simple_workflow()

    print("\n" + "="*80)
    print("Next Steps:")
    print("="*80)
    print("1. Run full examples: python examples/similarity_evaluation_example.py")
    print("2. Read quick reference: docs/SIMILARITY_METRICS_QUICKSTART.md")
    print("3. Read full guide: docs/NON_LLM_EVALUATION_GUIDE.md")
    print("4. Adapt to your use case!")
    print()


if __name__ == "__main__":
    main()
