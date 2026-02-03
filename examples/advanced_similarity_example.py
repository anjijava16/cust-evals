"""
Advanced Similarity Metrics Examples

Demonstrates industry-standard NLP metrics:
- BLEU (machine translation)
- ROUGE (summarization)
- Jaro-Winkler (string matching)
- Dice Coefficient
- Token F1 Score
- Cosine Similarity (TF-IDF)

Run: python examples/advanced_similarity_example.py
"""

from custom.evals.metrics import (
    bleu_score,
    rouge_n,
    rouge_l,
    jaro_winkler_similarity,
    dice_coefficient,
    token_f1_score,
    cosine_similarity_tfidf
)


def example_1_bleu():
    """Example 1: BLEU score for translation/generation evaluation."""
    print("="*80)
    print("Example 1: BLEU Score (Machine Translation)")
    print("="*80)

    test_cases = [
        {
            "name": "Perfect translation",
            "output": "The cat is on the mat",
            "reference": "The cat is on the mat"
        },
        {
            "name": "Good translation",
            "output": "The cat sits on the mat",
            "reference": "The cat is on the mat"
        },
        {
            "name": "Poor translation",
            "output": "A feline animal on floor covering",
            "reference": "The cat is on the mat"
        }
    ]

    for case in test_cases:
        print(f"\n{case['name']}:")
        print(f"  Output:    {case['output']}")
        print(f"  Reference: {case['reference']}")

        eval_input = {
            "output": case["output"],
            "expected": case["reference"]
        }

        score = bleu_score(eval_input)
        print(f"  BLEU Score: {score.score:.2%} ({score.label})")
        print(f"  Brevity Penalty: {score.metadata['brevity_penalty']:.3f}")
        print(f"  1-gram precision: {score.metadata['precisions']['1-gram']:.2%}")
        print(f"  2-gram precision: {score.metadata['precisions']['2-gram']:.2%}")


def example_2_rouge():
    """Example 2: ROUGE scores for summarization evaluation."""
    print("\n" + "="*80)
    print("Example 2: ROUGE Scores (Summarization)")
    print("="*80)

    reference_summary = "Machine learning is a subset of artificial intelligence that enables computers to learn from data"
    test_summaries = [
        "Machine learning is a subset of AI that allows computers to learn from data",
        "ML is part of AI and helps computers learn",
        "Artificial intelligence includes machine learning capabilities"
    ]

    print(f"\nReference Summary:")
    print(f"  {reference_summary}")

    for i, summary in enumerate(test_summaries, 1):
        print(f"\nCandidate {i}: {summary}")

        eval_input = {
            "output": summary,
            "expected": reference_summary
        }

        # ROUGE-1 (unigram)
        eval_input_r1 = {**eval_input, "n": 1}
        rouge1 = rouge_n(eval_input_r1)
        print(f"  ROUGE-1: {rouge1.score:.2%} (P: {rouge1.metadata['precision']:.2%}, "
              f"R: {rouge1.metadata['recall']:.2%})")

        # ROUGE-2 (bigram)
        eval_input_r2 = {**eval_input, "n": 2}
        rouge2 = rouge_n(eval_input_r2)
        print(f"  ROUGE-2: {rouge2.score:.2%} (P: {rouge2.metadata['precision']:.2%}, "
              f"R: {rouge2.metadata['recall']:.2%})")

        # ROUGE-L (LCS)
        rougel = rouge_l(eval_input)
        print(f"  ROUGE-L: {rougel.score:.2%} (LCS length: {rougel.metadata['lcs_length']})")


def example_3_jaro_winkler():
    """Example 3: Jaro-Winkler for name/short string matching."""
    print("\n" + "="*80)
    print("Example 3: Jaro-Winkler Similarity (Name Matching)")
    print("="*80)

    test_cases = [
        ("Martha", "Marhta"),      # Transposition
        ("John Smith", "Jon Smith"),  # Missing character
        ("Microsoft", "Microsft"),    # Missing character
        ("Apple Inc", "Apple Incorporated"),  # Abbreviation
        ("OpenAI", "Open AI"),        # Space variation
    ]

    print("\nComparing similar strings (good for names, identifiers):\n")

    for output, expected in test_cases:
        eval_input = {
            "output": output,
            "expected": expected
        }

        score = jaro_winkler_similarity(eval_input)
        print(f"  '{output}' vs '{expected}'")
        print(f"    Jaro-Winkler: {score.score:.2%} ({score.label})")
        print(f"    Jaro: {score.metadata['jaro']:.2%}, "
              f"Common prefix: {score.metadata['common_prefix_length']} chars")
        print()


def example_4_dice_coefficient():
    """Example 4: Dice coefficient for n-gram similarity."""
    print("="*80)
    print("Example 4: Dice Coefficient (N-gram Similarity)")
    print("="*80)

    test_cases = [
        {
            "output": "The quick brown fox",
            "expected": "The quick brown dog",
            "n": 1  # Word-level
        },
        {
            "output": "Hello World",
            "expected": "Hello Word",
            "n": 2  # Character bigrams
        },
        {
            "output": "Machine Learning",
            "expected": "Deep Learning",
            "n": 1  # Word-level
        }
    ]

    for case in test_cases:
        print(f"\nComparing: '{case['output']}' vs '{case['expected']}'")
        print(f"  N-gram size: {case['n']} ({'word-level' if case['n'] == 1 else f'{case['n']}-gram'})")

        eval_input = {
            "output": case["output"],
            "expected": case["expected"],
            "n": case["n"]
        }

        score = dice_coefficient(eval_input)
        print(f"  Dice Coefficient: {score.score:.2%} ({score.label})")
        print(f"  Common: {score.metadata['intersection_count']}, "
              f"Total: {score.metadata['output_ngram_count'] + score.metadata['expected_ngram_count']}")


def example_5_token_f1():
    """Example 5: Token-level F1 score."""
    print("\n" + "="*80)
    print("Example 5: Token F1 Score (Precision/Recall)")
    print("="*80)

    test_cases = [
        {
            "name": "NER evaluation",
            "output": "John Smith works at Microsoft in Seattle",
            "expected": "John Smith works at Microsoft"
        },
        {
            "name": "Keyword extraction",
            "output": "machine learning artificial intelligence",
            "expected": "machine learning deep learning AI"
        },
        {
            "name": "Classification labels",
            "output": "positive neutral",
            "expected": "positive negative neutral"
        }
    ]

    for case in test_cases:
        print(f"\n{case['name']}:")
        print(f"  Output:   {case['output']}")
        print(f"  Expected: {case['expected']}")

        eval_input = {
            "output": case["output"],
            "expected": case["expected"]
        }

        score = token_f1_score(eval_input)
        print(f"  F1 Score: {score.score:.2%} ({score.label})")
        print(f"  Precision: {score.metadata['precision']:.2%}, "
              f"Recall: {score.metadata['recall']:.2%}")
        print(f"  Common tokens: {score.metadata['common_tokens']}")
        if score.metadata['missing_tokens']:
            print(f"  Missing: {score.metadata['missing_tokens']}")
        if score.metadata['extra_tokens']:
            print(f"  Extra: {score.metadata['extra_tokens']}")


def example_6_cosine_similarity():
    """Example 6: Cosine similarity with TF-IDF."""
    print("\n" + "="*80)
    print("Example 6: Cosine Similarity with TF-IDF (Document Comparison)")
    print("="*80)

    reference_doc = "Machine learning is a method of data analysis that automates analytical model building"

    test_docs = [
        "Machine learning automates the process of analytical model building using data analysis methods",
        "Deep learning is a subset of machine learning based on neural networks",
        "Data science involves statistics, programming, and domain knowledge"
    ]

    print(f"\nReference Document:")
    print(f"  {reference_doc}")

    for i, doc in enumerate(test_docs, 1):
        print(f"\nDocument {i}:")
        print(f"  {doc}")

        eval_input = {
            "output": doc,
            "expected": reference_doc
        }

        score = cosine_similarity_tfidf(eval_input)
        print(f"  Cosine Similarity: {score.score:.2%} ({score.label})")
        print(f"  Vocabulary size: {score.metadata['vocabulary_size']} terms")


def example_7_comprehensive_comparison():
    """Example 7: Run all advanced metrics on the same text pair."""
    print("\n" + "="*80)
    print("Example 7: Comprehensive Comparison (All Advanced Metrics)")
    print("="*80)

    output = "The quick brown fox jumps over the lazy dog"
    expected = "The quick brown fox jumped over a lazy dog"

    print(f"\nOutput:   {output}")
    print(f"Expected: {expected}")
    print("\n" + "-"*80)

    eval_input = {
        "output": output,
        "expected": expected
    }

    # Run all metrics
    metrics = [
        ("BLEU", bleu_score(eval_input)),
        ("ROUGE-1", rouge_n({**eval_input, "n": 1})),
        ("ROUGE-2", rouge_n({**eval_input, "n": 2})),
        ("ROUGE-L", rouge_l(eval_input)),
        ("Jaro-Winkler", jaro_winkler_similarity(eval_input)),
        ("Dice Coef", dice_coefficient({**eval_input, "n": 1})),
        ("Token F1", token_f1_score(eval_input)),
        ("Cosine (TF-IDF)", cosine_similarity_tfidf(eval_input))
    ]

    for name, score in metrics:
        status = "✓" if score.score >= 0.7 else "~" if score.score >= 0.5 else "✗"
        print(f"{status} {name:20s}: {score.score:.2%} ({score.label})")

    # Calculate overall score
    avg_score = sum(score.score for _, score in metrics) / len(metrics)
    print("-"*80)
    print(f"Average Score: {avg_score:.2%}")


def example_8_use_case_scenarios():
    """Example 8: Real-world use case scenarios."""
    print("\n" + "="*80)
    print("Example 8: Real-World Use Case Scenarios")
    print("="*80)

    # Use Case 1: Translation Quality
    print("\nUse Case 1: Machine Translation Quality")
    print("-" * 40)
    translation_eval = {
        "output": "El gato está en la alfombra",
        "expected": "El gato esta sobre la alfombra"
    }
    bleu = bleu_score(translation_eval)
    print(f"Translation: {translation_eval['output']}")
    print(f"Reference:   {translation_eval['expected']}")
    print(f"BLEU Score:  {bleu.score:.2%} - Translation quality is {bleu.label}")

    # Use Case 2: Summary Quality
    print("\nUse Case 2: Text Summarization Quality")
    print("-" * 40)
    summary_eval = {
        "output": "AI and ML are transforming industries",
        "expected": "Artificial intelligence and machine learning technologies are transforming various industries"
    }
    r1 = rouge_n({**summary_eval, "n": 1})
    rl = rouge_l(summary_eval)
    print(f"Summary:   {summary_eval['output']}")
    print(f"Reference: {summary_eval['expected']}")
    print(f"ROUGE-1:   {r1.score:.2%}")
    print(f"ROUGE-L:   {rl.score:.2%}")
    print(f"Summary captures {r1.metadata['recall']:.0%} of reference content")

    # Use Case 3: Name Matching
    print("\nUse Case 3: Entity Name Matching")
    print("-" * 40)
    name_eval = {
        "output": "Steven Johnson",
        "expected": "Stephen Jonson"
    }
    jw = jaro_winkler_similarity(name_eval)
    print(f"Detected: {name_eval['output']}")
    print(f"Expected: {name_eval['expected']}")
    print(f"Similarity: {jw.score:.2%} - Names are {jw.label} match")

    # Use Case 4: Keyword Extraction
    print("\nUse Case 4: Keyword Extraction Quality")
    print("-" * 40)
    keyword_eval = {
        "output": "machine learning deep learning AI neural networks",
        "expected": "machine learning AI data science neural networks"
    }
    f1 = token_f1_score(keyword_eval)
    print(f"Extracted: {keyword_eval['output']}")
    print(f"Expected:  {keyword_eval['expected']}")
    print(f"F1 Score:  {f1.score:.2%}")
    print(f"Precision: {f1.metadata['precision']:.2%}, Recall: {f1.metadata['recall']:.2%}")
    print(f"Missing keywords: {f1.metadata['missing_tokens']}")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("ADVANCED SIMILARITY METRICS - COMPREHENSIVE EXAMPLES")
    print("="*80)
    print("\nIndustry-standard NLP metrics for NON-LLM evaluation")
    print()

    example_1_bleu()
    example_2_rouge()
    example_3_jaro_winkler()
    example_4_dice_coefficient()
    example_5_token_f1()
    example_6_cosine_similarity()
    example_7_comprehensive_comparison()
    example_8_use_case_scenarios()

    print("\n" + "="*80)
    print("All examples completed successfully!")
    print("="*80)
    print("\nThese metrics are perfect for:")
    print("  • Machine translation evaluation (BLEU)")
    print("  • Text summarization (ROUGE)")
    print("  • Name/entity matching (Jaro-Winkler)")
    print("  • Document similarity (Cosine, Dice)")
    print("  • Classification quality (Token F1)")
    print()


if __name__ == "__main__":
    main()
