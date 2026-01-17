"""Basic usage examples for custom-evals."""

from custom.evals import custom_accuracy, exact_match, sentiment_score


def example_exact_match():
    """Example: Exact Match metric."""
    print("=" * 60)
    print("Example 1: Exact Match")
    print("=" * 60)

    # Test case 1: Match
    eval_input = {"output": "Paris", "expected": "Paris"}
    score = exact_match(eval_input)
    print(f"\nInput: {eval_input}")
    print(f"Result: {score}")

    # Test case 2: No match
    eval_input = {"output": "London", "expected": "Paris"}
    score = exact_match(eval_input)
    print(f"\nInput: {eval_input}")
    print(f"Result: {score}")

    # Test case 3: With field mapping
    eval_input = {"prediction": "Tokyo", "ground_truth": "Tokyo"}
    field_mapping = {"output": "prediction", "expected": "ground_truth"}
    score = exact_match(eval_input, field_mapping=field_mapping)
    print(f"\nInput: {eval_input}")
    print(f"Field mapping: {field_mapping}")
    print(f"Result: {score}")


def example_sentiment():
    """Example: Sentiment analysis metric."""
    print("\n" + "=" * 60)
    print("Example 2: Sentiment Analysis")
    print("=" * 60)

    test_cases = [
        {"text": "I love this product! It's amazing and wonderful!"},
        {"text": "This is terrible and awful. I hate it."},
        {"text": "The package arrived on time."},
        {"text": "Great quality but bad customer service."},
    ]

    for eval_input in test_cases:
        score = sentiment_score(eval_input)
        print(f"\nText: '{eval_input['text']}'")
        print(f"Result: score={score.score:.2f}, label={score.label}")


def example_custom_accuracy():
    """Example: Custom accuracy with normalization."""
    print("\n" + "=" * 60)
    print("Example 3: Custom Accuracy")
    print("=" * 60)

    # Test case 1: With normalization (default)
    eval_input = {"output": " Paris ", "expected": "paris"}
    score = custom_accuracy(eval_input)
    print(f"\nInput: {eval_input}")
    print(f"Normalization: ON")
    print(f"Result: {score}")

    # Test case 2: Without normalization
    eval_input = {"output": " Paris ", "expected": "paris"}
    score = custom_accuracy(eval_input, normalize=False)
    print(f"\nInput: {eval_input}")
    print(f"Normalization: OFF")
    print(f"Result: {score}")

    # Test case 3: Numbers
    eval_input = {"output": "42", "expected": "42"}
    score = custom_accuracy(eval_input)
    print(f"\nInput: {eval_input}")
    print(f"Result: {score}")


def example_batch_evaluation():
    """Example: Batch evaluation with pandas."""
    print("\n" + "=" * 60)
    print("Example 4: Batch Evaluation")
    print("=" * 60)

    try:
        import pandas as pd

        # Sample dataset
        data = {
            "prediction": ["Paris", "London", "Tokyo", "Berlin"],
            "ground_truth": ["Paris", "Paris", "Tokyo", "Berlin"],
        }
        df = pd.DataFrame(data)

        print("\nDataset:")
        print(df)

        # Evaluate each row
        scores = []
        for _, row in df.iterrows():
            eval_input = {
                "output": row["prediction"],
                "expected": row["ground_truth"],
            }
            score = exact_match(eval_input)
            scores.append(score.score)

        df["exact_match_score"] = scores

        print("\nResults:")
        print(df)
        print(f"\nAccuracy: {df['exact_match_score'].mean():.2%}")

    except ImportError:
        print("\n[pandas not installed - skipping batch evaluation example]")


if __name__ == "__main__":
    example_exact_match()
    example_sentiment()
    example_custom_accuracy()
    example_batch_evaluation()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
