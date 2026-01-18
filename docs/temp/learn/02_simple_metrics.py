"""
Lesson 2: Simple Evaluation Metrics

Learn different ways to measure LLM response quality using simple,
easy-to-understand metrics.

Learning Objectives:
- Understand different types of metrics
- Implement exact match, contains, and similarity metrics
- Know when to use each metric
- Combine multiple metrics

Prerequisites: Complete Lesson 1
"""

from typing import Dict, Any


# ============================================================================
# METRIC 1: EXACT MATCH
# ============================================================================

def exact_match(response: str, expected: str) -> Dict[str, Any]:
    """
    Strictest metric: response must exactly match expected.

    Use when: You need precise, word-for-word accuracy
    Example: Math problems, specific commands, IDs
    """
    # Normalize by stripping whitespace and lowercasing
    response_normalized = response.strip().lower()
    expected_normalized = expected.strip().lower()

    is_match = response_normalized == expected_normalized

    return {
        "score": 1.0 if is_match else 0.0,
        "passed": is_match,
        "metric": "exact_match",
        "explanation": f"Expected exact match with '{expected}'"
    }


# ============================================================================
# METRIC 2: CONTAINS CHECK
# ============================================================================

def contains_answer(response: str, expected: str) -> Dict[str, Any]:
    """
    Flexible metric: check if response contains the expected answer.

    Use when: Answer can be part of a longer response
    Example: Q&A where answer is embedded in explanation
    """
    response_lower = response.lower()
    expected_lower = expected.lower()

    contains = expected_lower in response_lower

    return {
        "score": 1.0 if contains else 0.0,
        "passed": contains,
        "metric": "contains",
        "explanation": f"Checking if response contains '{expected}'"
    }


# ============================================================================
# METRIC 3: WORD OVERLAP / SIMILARITY
# ============================================================================

def word_overlap(response: str, expected: str) -> Dict[str, Any]:
    """
    Similarity metric: measure overlap between words.

    Use when: Paraphrasing is acceptable
    Example: Explanations, descriptions
    """
    response_words = set(response.lower().split())
    expected_words = set(expected.lower().split())

    if not expected_words:
        return {"score": 0.0, "passed": False, "metric": "word_overlap"}

    overlap = len(response_words & expected_words)
    total = len(expected_words)
    score = overlap / total

    return {
        "score": score,
        "passed": score >= 0.5,  # Pass if 50%+ overlap
        "metric": "word_overlap",
        "overlap_words": len(response_words & expected_words),
        "total_expected": total,
        "explanation": f"Word overlap: {overlap}/{total} words"
    }


# ============================================================================
# METRIC 4: LENGTH CHECK
# ============================================================================

def length_check(response: str, min_words: int = 5, max_words: int = 100) -> Dict[str, Any]:
    """
    Quality metric: check if response has appropriate length.

    Use when: You need responses within a certain length range
    Example: Summaries, brief answers
    """
    word_count = len(response.split())

    is_appropriate = min_words <= word_count <= max_words

    if word_count < min_words:
        issue = "too_short"
    elif word_count > max_words:
        issue = "too_long"
    else:
        issue = None

    return {
        "score": 1.0 if is_appropriate else 0.5,
        "passed": is_appropriate,
        "metric": "length_check",
        "word_count": word_count,
        "issue": issue,
        "explanation": f"Length: {word_count} words (target: {min_words}-{max_words})"
    }


# ============================================================================
# METRIC 5: KEYWORD PRESENCE
# ============================================================================

def keyword_presence(response: str, required_keywords: list) -> Dict[str, Any]:
    """
    Coverage metric: check if response includes required keywords.

    Use when: Response must cover specific topics/terms
    Example: Technical documentation, structured answers
    """
    response_lower = response.lower()

    present_keywords = [kw for kw in required_keywords if kw.lower() in response_lower]
    missing_keywords = [kw for kw in required_keywords if kw.lower() not in response_lower]

    coverage = len(present_keywords) / len(required_keywords) if required_keywords else 0

    return {
        "score": coverage,
        "passed": coverage >= 0.7,  # Pass if 70%+ keywords present
        "metric": "keyword_presence",
        "present": present_keywords,
        "missing": missing_keywords,
        "coverage": f"{len(present_keywords)}/{len(required_keywords)}",
        "explanation": f"Found {len(present_keywords)}/{len(required_keywords)} required keywords"
    }


# ============================================================================
# DEMONSTRATION: COMPARING METRICS
# ============================================================================

print("=" * 70)
print("LESSON 2: Simple Evaluation Metrics")
print("=" * 70)

# Test case
question = "What is machine learning?"
expected_short = "ML learns from data"
expected_full = "Machine learning is a type of AI that learns patterns from data"

responses = {
    "Perfect": "Machine learning is a type of AI that learns patterns from data",
    "Paraphrased": "ML is an AI technique that discovers patterns in datasets",
    "Brief": "ML learns from data",
    "Verbose": "Well, machine learning, which is a subset of artificial intelligence, is fundamentally about creating systems that can learn from data and improve their performance over time without being explicitly programmed for every single task",
    "Wrong": "Machine learning is a programming language",
}

print("\n🎯 Testing Different Metrics on Same Responses\n")
print(f"Question: {question}")
print(f"Expected: {expected_full}\n")

for response_type, response in responses.items():
    print(f"\n{response_type} Response:")
    print(f"  '{response[:60]}...'")
    print("\n  Metric Results:")

    # Test exact match
    em = exact_match(response, expected_full)
    print(f"    Exact Match: {'✓' if em['passed'] else '✗'} (score: {em['score']:.2f})")

    # Test contains
    cont = contains_answer(response, "machine learning")
    print(f"    Contains 'ML': {'✓' if cont['passed'] else '✗'} (score: {cont['score']:.2f})")

    # Test word overlap
    overlap = word_overlap(response, expected_full)
    print(f"    Word Overlap: {'✓' if overlap['passed'] else '✗'} (score: {overlap['score']:.2f})")

    # Test length
    length = length_check(response, min_words=5, max_words=30)
    print(f"    Length: {'✓' if length['passed'] else '✗'} ({length['word_count']} words)")

    # Test keywords
    keywords = keyword_presence(response, ["machine learning", "data", "AI"])
    print(f"    Keywords: {'✓' if keywords['passed'] else '✗'} ({keywords['coverage']})")

# ============================================================================
# COMBINING MULTIPLE METRICS
# ============================================================================

print("\n\n" + "=" * 70)
print("COMBINING MULTIPLE METRICS")
print("=" * 70)

def comprehensive_evaluation(response: str, expected: str) -> Dict[str, Any]:
    """Combine multiple metrics for holistic evaluation."""

    # Run all metrics
    metrics = {
        "exact_match": exact_match(response, expected),
        "contains": contains_answer(response, expected.split()[0] if expected else ""),
        "word_overlap": word_overlap(response, expected),
        "length": length_check(response),
        "keywords": keyword_presence(response, ["machine", "learning", "data"])
    }

    # Calculate weighted overall score
    weights = {
        "exact_match": 0.1,      # Less weight - too strict
        "contains": 0.2,         # Moderate weight
        "word_overlap": 0.4,     # High weight - good balance
        "length": 0.1,           # Less weight - secondary concern
        "keywords": 0.2          # Moderate weight
    }

    overall_score = sum(metrics[m]["score"] * weights[m] for m in weights)

    return {
        "overall_score": overall_score,
        "passed": overall_score >= 0.7,
        "individual_metrics": metrics,
        "summary": f"Overall: {overall_score:.2f}/1.00"
    }

# Test comprehensive evaluation
test_response = "ML is an AI technique that discovers patterns in datasets"
result = comprehensive_evaluation(test_response, expected_full)

print(f"\nTest Response: '{test_response}'")
print(f"\nOverall Score: {result['overall_score']:.2f}")
print(f"Status: {'✓ PASS' if result['passed'] else '✗ FAIL'}")
print("\nBreakdown:")
for metric_name, metric_result in result['individual_metrics'].items():
    print(f"  {metric_name:15} → {metric_result['score']:.2f}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "=" * 70)
print("KEY TAKEAWAYS")
print("=" * 70)

print("""
📚 Metrics You Learned:

1. EXACT MATCH (Strictest)
   • Perfect for: Math, codes, specific formats
   • Limitation: No flexibility for paraphrasing

2. CONTAINS CHECK (Flexible)
   • Perfect for: Q&A, key info extraction
   • Limitation: Doesn't catch wrong extra info

3. WORD OVERLAP (Balanced)
   • Perfect for: Paraphrased answers, summaries
   • Limitation: Ignores word order/grammar

4. LENGTH CHECK (Quality control)
   • Perfect for: Ensuring appropriate response length
   • Limitation: Quantity ≠ quality

5. KEYWORD PRESENCE (Coverage)
   • Perfect for: Ensuring key topics covered
   • Limitation: Presence ≠ correct usage

💡 Best Practices:

✓ Use multiple metrics together
✓ Choose metrics appropriate for your task
✓ Exact match for precision tasks
✓ Similarity for flexible tasks
✓ Always consider the context

⚠️ Common Pitfalls:

✗ Using exact match when flexibility needed
✗ Relying on single metric
✗ Ignoring false positives
✗ Not setting appropriate thresholds

🎯 Next Steps:

Ready for more advanced evaluation?
Next lesson: LLM-as-Judge (using LLMs to evaluate LLMs!)
""")

print("=" * 70)
print("✨ Lesson 2 Complete!")
print("=" * 70)
print("\nNext: Run 03_llm_as_judge.py")
