"""
Lesson 8: Statistical Evaluation & Significance Testing (Advanced)

Learn to apply statistical rigor to LLM evaluation, ensuring your results
are reliable and not due to chance.

Learning Objectives:
- Statistical significance testing
- Confidence intervals for metrics
- Sample size determination
- Bootstrap methods for evaluation
- Comparing systems with statistical tests
- Detecting and handling variance

Prerequisites: Lessons 1-7, Basic statistics knowledge helpful
Difficulty: ⭐⭐⭐ Advanced
Time: 45 minutes
"""

import random
import math
from typing import List, Dict, Tuple
from collections import defaultdict

print("=" * 80)
print("LESSON 8: Statistical Evaluation & Significance Testing")
print("=" * 80)

print("""
🎲 WHY STATISTICS MATTER IN EVALUATION

Without statistics, you might conclude:
❌ "Model A scores 0.82, Model B scores 0.80, so A is better!"

But with statistics, you ask:
✅ "Is this 2% difference statistically significant?"
✅ "How confident are we in these scores?"
✅ "Did we test on enough examples?"

KEY CONCEPTS:
• Statistical Significance: Is the difference real or due to chance?
• Confidence Intervals: Range where true value likely lies
• Sample Size: How many examples do we need?
• Variance: How much do scores fluctuate?
""")

input("Press Enter to continue...")

# ============================================================================
# PART 1: CONFIDENCE INTERVALS
# ============================================================================

print("\n" + "=" * 80)
print("PART 1: Confidence Intervals - How Certain Are Your Scores?")
print("=" * 80)

def calculate_confidence_interval(
    scores: List[float],
    confidence: float = 0.95
) -> Tuple[float, float, float]:
    """
    Calculate confidence interval for evaluation scores.

    Returns:
        (mean, lower_bound, upper_bound)
    """
    n = len(scores)
    if n < 2:
        return (scores[0] if scores else 0, 0, 0)

    mean = sum(scores) / n

    # Calculate standard error
    variance = sum((x - mean) ** 2 for x in scores) / (n - 1)
    std_error = math.sqrt(variance / n)

    # Z-score for 95% confidence (approximately 1.96)
    z_score = 1.96 if confidence == 0.95 else 2.576  # 99% confidence

    margin_of_error = z_score * std_error

    return (
        mean,
        mean - margin_of_error,
        mean + margin_of_error
    )

# Demo: Why confidence intervals matter
print("\n📊 Example: Two Models with Same Average Score\n")

# Model A: Consistent scores
model_a_scores = [0.80, 0.81, 0.80, 0.79, 0.80, 0.81, 0.80, 0.79, 0.80, 0.81]

# Model B: Inconsistent scores
model_b_scores = [0.95, 0.65, 0.90, 0.70, 0.85, 0.75, 0.82, 0.78, 0.88, 0.72]

mean_a, lower_a, upper_a = calculate_confidence_interval(model_a_scores)
mean_b, lower_b, upper_b = calculate_confidence_interval(model_b_scores)

print(f"Model A: Mean = {mean_a:.3f}, 95% CI = [{lower_a:.3f}, {upper_a:.3f}]")
print(f"Model B: Mean = {mean_b:.3f}, 95% CI = [{lower_b:.3f}, {upper_b:.3f}]")

print(f"\n💡 Insight:")
print(f"Both models have similar means (~0.80), but:")
print(f"  • Model A: Narrow CI (±{(upper_a - lower_a)/2:.3f}) - Consistent!")
print(f"  • Model B: Wide CI (±{(upper_b - lower_b)/2:.3f}) - Unreliable!")
print(f"\nModel A is more trustworthy despite similar average score.")

input("\nPress Enter to continue...")

# ============================================================================
# PART 2: STATISTICAL SIGNIFICANCE TESTING
# ============================================================================

print("\n" + "=" * 80)
print("PART 2: Statistical Significance - Is the Difference Real?")
print("=" * 80)

def t_test(scores_a: List[float], scores_b: List[float]) -> Dict:
    """
    Perform t-test to determine if two models significantly differ.

    Returns:
        dict with t_statistic, p_value, significant
    """
    n_a, n_b = len(scores_a), len(scores_b)
    mean_a = sum(scores_a) / n_a
    mean_b = sum(scores_b) / n_b

    # Calculate pooled standard deviation
    var_a = sum((x - mean_a) ** 2 for x in scores_a) / (n_a - 1)
    var_b = sum((x - mean_b) ** 2 for x in scores_b) / (n_b - 1)

    pooled_std = math.sqrt((var_a / n_a) + (var_b / n_b))

    # Calculate t-statistic
    t_stat = (mean_a - mean_b) / pooled_std if pooled_std > 0 else 0

    # Simplified p-value estimation (for demo purposes)
    # In production, use scipy.stats.ttest_ind
    p_value = 0.05 if abs(t_stat) > 2.0 else 0.20

    return {
        "mean_a": mean_a,
        "mean_b": mean_b,
        "difference": mean_a - mean_b,
        "t_statistic": t_stat,
        "p_value": p_value,
        "significant": p_value < 0.05,
        "conclusion": "Significant difference" if p_value < 0.05 else "No significant difference"
    }

# Demo: Comparing models statistically
print("\n🔬 Example: Is Model Improvement Significant?\n")

baseline_scores = [0.75, 0.74, 0.76, 0.75, 0.77, 0.74, 0.76, 0.75, 0.76, 0.75]
improved_scores = [0.82, 0.81, 0.83, 0.82, 0.84, 0.81, 0.83, 0.82, 0.83, 0.82]

result = t_test(baseline_scores, improved_scores)

print(f"Baseline Model: Mean = {result['mean_a']:.3f}")
print(f"Improved Model: Mean = {result['mean_b']:.3f}")
print(f"Difference: {result['difference']:.3f} ({abs(result['difference'])/result['mean_a']*100:.1f}%)")
print(f"\nT-statistic: {result['t_statistic']:.3f}")
print(f"P-value: {result['p_value']:.3f}")
print(f"\n{'✅' if result['significant'] else '❌'} {result['conclusion']}")

if result['significant']:
    print("\n🎉 The improvement is statistically significant!")
    print("   You can confidently say the new model is better.")
else:
    print("\n⚠️  The improvement is NOT statistically significant.")
    print("   The difference might be due to chance. Need more data!")

input("\nPress Enter to continue...")

# ============================================================================
# PART 3: SAMPLE SIZE DETERMINATION
# ============================================================================

print("\n" + "=" * 80)
print("PART 3: Sample Size - How Many Examples Do You Need?")
print("=" * 80)

def required_sample_size(
    expected_difference: float = 0.05,
    std_dev: float = 0.15,
    confidence: float = 0.95,
    power: float = 0.80
) -> int:
    """
    Calculate required sample size for detecting a difference.

    Args:
        expected_difference: Minimum difference you want to detect
        std_dev: Expected standard deviation
        confidence: Confidence level (typically 0.95)
        power: Statistical power (typically 0.80)

    Returns:
        Required sample size per group
    """
    # Z-scores for confidence and power
    z_alpha = 1.96  # For 95% confidence
    z_beta = 0.84   # For 80% power

    # Calculate sample size
    n = ((z_alpha + z_beta) ** 2 * 2 * (std_dev ** 2)) / (expected_difference ** 2)

    return math.ceil(n)

# Demo: Sample size planning
print("\n📐 Example: Planning Your Evaluation\n")

scenarios = [
    {"diff": 0.10, "std": 0.15, "desc": "Large difference, moderate variance"},
    {"diff": 0.05, "std": 0.15, "desc": "Medium difference, moderate variance"},
    {"diff": 0.02, "std": 0.15, "desc": "Small difference, moderate variance"},
    {"diff": 0.05, "std": 0.25, "desc": "Medium difference, high variance"},
]

print("How many test examples do you need?\n")
for scenario in scenarios:
    n = required_sample_size(scenario["diff"], scenario["std"])
    print(f"{scenario['desc']}:")
    print(f"  Expected difference: {scenario['diff']:.2f}")
    print(f"  Std deviation: {scenario['std']:.2f}")
    print(f"  ➜ Required samples: {n} per model\n")

print("💡 Key Insights:")
print("  • Smaller differences require MORE samples")
print("  • Higher variance requires MORE samples")
print("  • Plan sample size BEFORE evaluation!")
print("  • Underpowered studies waste resources")

input("\nPress Enter to continue...")

# ============================================================================
# PART 4: BOOTSTRAP CONFIDENCE INTERVALS
# ============================================================================

print("\n" + "=" * 80)
print("PART 4: Bootstrap Method - Robust Confidence Estimation")
print("=" * 80)

def bootstrap_confidence_interval(
    scores: List[float],
    n_iterations: int = 1000,
    confidence: float = 0.95
) -> Dict:
    """
    Calculate confidence interval using bootstrap resampling.
    More robust than parametric methods, works with any metric.
    """
    bootstrap_means = []

    for _ in range(n_iterations):
        # Resample with replacement
        sample = [random.choice(scores) for _ in range(len(scores))]
        bootstrap_means.append(sum(sample) / len(sample))

    # Sort bootstrap means
    bootstrap_means.sort()

    # Calculate percentiles for confidence interval
    alpha = 1 - confidence
    lower_idx = int((alpha / 2) * n_iterations)
    upper_idx = int((1 - alpha / 2) * n_iterations)

    return {
        "mean": sum(scores) / len(scores),
        "lower": bootstrap_means[lower_idx],
        "upper": bootstrap_means[upper_idx],
        "std": (bootstrap_means[upper_idx] - bootstrap_means[lower_idx]) / 4
    }

# Demo: Bootstrap for complex metrics
print("\n🔄 Example: Bootstrap Confidence Intervals\n")

test_scores = [0.75, 0.82, 0.78, 0.85, 0.77, 0.80, 0.83, 0.76, 0.81, 0.79]

# Standard CI
mean_std, lower_std, upper_std = calculate_confidence_interval(test_scores)

# Bootstrap CI
bootstrap_result = bootstrap_confidence_interval(test_scores)

print(f"Test Scores: {test_scores}\n")
print(f"Standard CI:  {mean_std:.3f} [{lower_std:.3f}, {upper_std:.3f}]")
print(f"Bootstrap CI: {bootstrap_result['mean']:.3f} [{bootstrap_result['lower']:.3f}, {bootstrap_result['upper']:.3f}]")

print(f"\n💡 Bootstrap Advantages:")
print(f"  • Works with ANY metric (not just mean)")
print(f"  • No distribution assumptions")
print(f"  • Handles outliers better")
print(f"  • More accurate for small samples")

input("\nPress Enter to continue...")

# ============================================================================
# PART 5: DETECTING AND HANDLING VARIANCE
# ============================================================================

print("\n" + "=" * 80)
print("PART 5: Variance Analysis - Understanding Score Fluctuation")
print("=" * 80)

def variance_analysis(scores: List[float]) -> Dict:
    """
    Analyze variance in evaluation scores.
    """
    n = len(scores)
    mean = sum(scores) / n

    # Calculate variance
    variance = sum((x - mean) ** 2 for x in scores) / (n - 1)
    std_dev = math.sqrt(variance)

    # Coefficient of variation (relative variability)
    cv = (std_dev / mean) * 100 if mean > 0 else 0

    # Min and max
    min_score = min(scores)
    max_score = max(scores)
    range_score = max_score - min_score

    return {
        "mean": mean,
        "std_dev": std_dev,
        "variance": variance,
        "cv_percent": cv,
        "min": min_score,
        "max": max_score,
        "range": range_score,
        "consistency": "High" if cv < 10 else "Medium" if cv < 20 else "Low"
    }

# Demo: Comparing variance across models
print("\n📊 Example: Model Consistency Analysis\n")

models = {
    "Stable Model": [0.80, 0.81, 0.80, 0.79, 0.80, 0.81, 0.80, 0.80, 0.81, 0.80],
    "Inconsistent Model": [0.90, 0.70, 0.85, 0.75, 0.88, 0.72, 0.82, 0.78, 0.87, 0.73],
}

for name, scores in models.items():
    analysis = variance_analysis(scores)
    print(f"{name}:")
    print(f"  Mean: {analysis['mean']:.3f} ± {analysis['std_dev']:.3f}")
    print(f"  Range: [{analysis['min']:.3f}, {analysis['max']:.3f}]")
    print(f"  Coefficient of Variation: {analysis['cv_percent']:.1f}%")
    print(f"  Consistency: {analysis['consistency']}")
    print()

print("💡 What This Tells Us:")
print("  • Low CV (<10%) = Reliable model")
print("  • High CV (>20%) = Unpredictable model")
print("  • Consistent models are safer for production")
print("  • Investigate causes of high variance")

input("\nPress Enter to continue...")

# ============================================================================
# PART 6: PRACTICAL WORKFLOW
# ============================================================================

print("\n" + "=" * 80)
print("PART 6: Practical Statistical Evaluation Workflow")
print("=" * 80)

def comprehensive_statistical_evaluation(
    model_a_scores: List[float],
    model_b_scores: List[float],
    model_a_name: str = "Baseline",
    model_b_name: str = "New Model"
) -> Dict:
    """
    Complete statistical comparison of two models.
    """
    # 1. Basic statistics
    mean_a = sum(model_a_scores) / len(model_a_scores)
    mean_b = sum(model_b_scores) / len(model_b_scores)

    # 2. Confidence intervals
    _, lower_a, upper_a = calculate_confidence_interval(model_a_scores)
    _, lower_b, upper_b = calculate_confidence_interval(model_b_scores)

    # 3. Statistical test
    test_result = t_test(model_a_scores, model_b_scores)

    # 4. Variance analysis
    var_a = variance_analysis(model_a_scores)
    var_b = variance_analysis(model_b_scores)

    # 5. Effect size (Cohen's d)
    pooled_std = math.sqrt((var_a['variance'] + var_b['variance']) / 2)
    cohens_d = (mean_b - mean_a) / pooled_std if pooled_std > 0 else 0

    return {
        "summary": {
            f"{model_a_name}_mean": mean_a,
            f"{model_b_name}_mean": mean_b,
            "difference": mean_b - mean_a,
            "percent_change": ((mean_b - mean_a) / mean_a * 100) if mean_a > 0 else 0,
        },
        "significance": test_result,
        "confidence_intervals": {
            model_a_name: (lower_a, upper_a),
            model_b_name: (lower_b, upper_b)
        },
        "consistency": {
            model_a_name: var_a['consistency'],
            model_b_name: var_b['consistency']
        },
        "effect_size": cohens_d,
        "recommendation": generate_recommendation(test_result, cohens_d, var_b['consistency'])
    }

def generate_recommendation(test_result: Dict, cohens_d: float, consistency: str) -> str:
    """Generate actionable recommendation."""
    if not test_result['significant']:
        return "⚠️  No significant improvement detected. Need more data or larger improvements."

    if consistency == "Low":
        return "⚠️  Improvement is significant but model is inconsistent. Investigate variance."

    if abs(cohens_d) > 0.8:
        return "✅ Large, significant improvement with good consistency. Ready to deploy!"
    elif abs(cohens_d) > 0.5:
        return "✅ Medium, significant improvement. Consider deploying with monitoring."
    else:
        return "⚠️  Small but significant improvement. Consider if worth the change."

# Demo: Complete evaluation
print("\n🎯 Complete Statistical Evaluation Example\n")

baseline = [0.72, 0.75, 0.73, 0.74, 0.76, 0.73, 0.75, 0.74, 0.75, 0.73,
            0.74, 0.76, 0.73, 0.75, 0.74, 0.73, 0.75, 0.74, 0.76, 0.73]

new_model = [0.81, 0.83, 0.82, 0.84, 0.85, 0.82, 0.84, 0.83, 0.84, 0.82,
             0.83, 0.85, 0.82, 0.84, 0.83, 0.82, 0.84, 0.83, 0.85, 0.82]

result = comprehensive_statistical_evaluation(baseline, new_model, "Baseline v1.0", "New v2.0")

print("📊 EVALUATION REPORT")
print("=" * 60)
print(f"\nBaseline v1.0: {result['summary']['Baseline v1.0_mean']:.3f} "
      f"CI: [{result['confidence_intervals']['Baseline v1.0'][0]:.3f}, "
      f"{result['confidence_intervals']['Baseline v1.0'][1]:.3f}]")
print(f"New v2.0:      {result['summary']['New v2.0_mean']:.3f} "
      f"CI: [{result['confidence_intervals']['New v2.0'][0]:.3f}, "
      f"{result['confidence_intervals']['New v2.0'][1]:.3f}]")

print(f"\nImprovement: {result['summary']['difference']:.3f} "
      f"({result['summary']['percent_change']:.1f}%)")
print(f"Statistical Significance: {'Yes ✅' if result['significance']['significant'] else 'No ❌'}")
print(f"Effect Size (Cohen's d): {result['effect_size']:.2f}")

print(f"\nConsistency:")
print(f"  Baseline: {result['consistency']['Baseline v1.0']}")
print(f"  New Model: {result['consistency']['New v2.0']}")

print(f"\n🎯 RECOMMENDATION:")
print(f"   {result['recommendation']}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)

print("""
🎓 STATISTICAL EVALUATION ESSENTIALS:

1. CONFIDENCE INTERVALS
   ✓ Always report mean ± confidence interval
   ✓ Narrow CI = reliable estimate
   ✓ Wide CI = need more data

2. SIGNIFICANCE TESTING
   ✓ Use t-tests to compare models
   ✓ p < 0.05 typically means significant
   ✓ Don't confuse statistical with practical significance

3. SAMPLE SIZE
   ✓ Calculate before evaluation
   ✓ More samples for small differences
   ✓ More samples for high variance

4. BOOTSTRAP METHODS
   ✓ Works with any metric
   ✓ No distribution assumptions
   ✓ More robust than parametric methods

5. VARIANCE MATTERS
   ✓ Low variance = consistent model
   ✓ High variance = investigate causes
   ✓ Report both mean and variance

⚠️  COMMON MISTAKES:

❌ Comparing means without significance testing
❌ Ignoring confidence intervals
❌ Using too few test examples
❌ Not checking for variance
❌ Confusing "better score" with "significantly better"
❌ Not planning sample size beforehand

✅ BEST PRACTICES:

1. Plan sample size before evaluation
2. Always use confidence intervals
3. Test for statistical significance
4. Consider effect size (practical significance)
5. Check variance and consistency
6. Use bootstrap for complex metrics
7. Report complete statistics (not just means)
8. Make decisions based on statistics, not intuition

💡 REMEMBER:

"A 2% improvement with p=0.001 is better than
 a 10% improvement with p=0.30"

Statistical rigor prevents costly mistakes in production!
""")

print("\n" + "=" * 80)
print("✨ Lesson 8 Complete!")
print("=" * 80)
print("\nYou've learned statistical evaluation - a critical skill for production ML!")
print("\nNext: 09_adversarial_testing.py - Test your model's robustness!")
