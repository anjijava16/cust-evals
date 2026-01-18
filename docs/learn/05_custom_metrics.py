"""
Lesson 5: Building Custom Metrics

Learn to create your own evaluation metrics for specific use cases.

Learning Objectives:
- Design custom metrics
- Implement evaluators from scratch
- Combine metrics effectively
- Handle edge cases

Prerequisites: Lessons 1-4
"""

from typing import Dict, Any, Callable


# ============================================================================
# CUSTOM METRIC TEMPLATE
# ============================================================================

class CustomMetric:
    """Base class for custom metrics."""
    
    def __init__(self, name: str, threshold: float = 0.7):
        self.name = name
        self.threshold = threshold
    
    def evaluate(self, **kwargs) -> Dict[str, Any]:
        """
        Override this method with your evaluation logic.
        
        Returns:
            dict with 'score', 'passed', and any additional info
        """
        raise NotImplementedError
    
    def __call__(self, **kwargs):
        return self.evaluate(**kwargs)


# ============================================================================
# EXAMPLE 1: SENTIMENT APPROPRIATENESS
# ============================================================================

class SentimentAppropriatenessMetric(CustomMetric):
    """Check if response has appropriate sentiment for context."""
    
    def __init__(self):
        super().__init__("sentiment_appropriateness")
        # Positive words and negative words (simplified)
        self.positive_words = {'good', 'great', 'excellent', 'happy', 'wonderful'}
        self.negative_words = {'bad', 'poor', 'terrible', 'sad', 'awful'}
    
    def evaluate(self, response: str, expected_sentiment: str) -> Dict[str, Any]:
        """
        Evaluate if response matches expected sentiment.
        
        Args:
            response: The text to evaluate
            expected_sentiment: 'positive', 'negative', or 'neutral'
        """
        words = set(response.lower().split())
        
        positive_count = len(words & self.positive_words)
        negative_count = len(words & self.negative_words)
        
        # Determine actual sentiment
        if positive_count > negative_count:
            actual_sentiment = 'positive'
        elif negative_count > positive_count:
            actual_sentiment = 'negative'
        else:
            actual_sentiment = 'neutral'
        
        matches = actual_sentiment == expected_sentiment
        
        return {
            "score": 1.0 if matches else 0.0,
            "passed": matches,
            "expected": expected_sentiment,
            "actual": actual_sentiment,
            "metric": self.name
        }


# ============================================================================
# EXAMPLE 2: CODE QUALITY METRIC
# ============================================================================

class CodeQualityMetric(CustomMetric):
    """Evaluate generated code quality."""
    
    def __init__(self):
        super().__init__("code_quality")
    
    def evaluate(self, code: str) -> Dict[str, Any]:
        """
        Evaluate code quality based on basic criteria.
        """
        issues = []
        score = 1.0
        
        # Check 1: Has docstring?
        if '"""' not in code and "'''" not in code:
            issues.append("Missing docstring")
            score -= 0.2
        
        # Check 2: Has function definition?
        if 'def ' not in code:
            issues.append("No function definition")
            score -= 0.3
        
        # Check 3: Reasonable length?
        lines = code.split('\n')
        if len(lines) > 50:
            issues.append("Too long (>50 lines)")
            score -= 0.1
        
        # Check 4: Has comments?
        has_comments = any(line.strip().startswith('#') for line in lines)
        if not has_comments and len(lines) > 10:
            issues.append("No comments for complex code")
            score -= 0.1
        
        score = max(0.0, score)
        
        return {
            "score": score,
            "passed": score >= self.threshold,
            "issues": issues,
            "metric": self.name
        }


# ============================================================================
# EXAMPLE 3: DOMAIN-SPECIFIC METRIC
# ============================================================================

class MedicalSafetyMetric(CustomMetric):
    """Ensure medical responses include appropriate disclaimers."""
    
    def __init__(self):
        super().__init__("medical_safety")
        self.required_phrases = [
            'consult',
            'doctor',
            'professional',
            'medical advice'
        ]
    
    def evaluate(self, response: str, is_medical_topic: bool) -> Dict[str, Any]:
        """
        Check if medical response has appropriate safety language.
        """
        if not is_medical_topic:
            return {
                "score": 1.0,
                "passed": True,
                "metric": self.name,
                "note": "Not a medical topic"
            }
        
        response_lower = response.lower()
        
        # Check for disclaimer phrases
        has_disclaimer = any(
            phrase in response_lower 
            for phrase in self.required_phrases
        )
        
        return {
            "score": 1.0 if has_disclaimer else 0.0,
            "passed": has_disclaimer,
            "metric": self.name,
            "has_safety_language": has_disclaimer,
            "warning": "Medical response lacks safety disclaimer" if not has_disclaimer else None
        }


# ============================================================================
# EXAMPLE 4: RESPONSE TIME METRIC
# ============================================================================

import time

class LatencyMetric(CustomMetric):
    """Measure response generation time."""
    
    def __init__(self, max_seconds: float = 2.0):
        super().__init__("latency")
        self.max_seconds = max_seconds
    
    def evaluate(self, start_time: float, end_time: float) -> Dict[str, Any]:
        """
        Evaluate if response was generated within time limit.
        """
        latency = end_time - start_time
        
        return {
            "score": 1.0 if latency <= self.max_seconds else 0.0,
            "passed": latency <= self.max_seconds,
            "latency_seconds": latency,
            "max_allowed": self.max_seconds,
            "metric": self.name
        }


# ============================================================================
# DEMONSTRATIONS
# ============================================================================

print("=" * 70)
print("LESSON 5: Building Custom Metrics")
print("=" * 70)

print("""
🛠️  WHY BUILD CUSTOM METRICS?

Pre-built metrics don't cover everything. You need custom metrics for:

✓ Domain-specific requirements (medical, legal, finance)
✓ Business rules (tone, length, format)
✓ Safety constraints (disclaimers, warnings)
✓ Performance requirements (latency, cost)
✓ Unique quality criteria

Let's build some!
""")

# Demo 1: Sentiment
print("\n" + "=" * 70)
print("EXAMPLE 1: Sentiment Appropriateness")
print("=" * 70)

sentiment_metric = SentimentAppropriatenessMetric()

test_cases = [
    ("Great job on the project!", "positive"),
    ("This is terrible and disappointing.", "negative"),
    ("The meeting is scheduled for 3pm.", "neutral"),
]

for response, expected in test_cases:
    result = sentiment_metric.evaluate(response, expected)
    status = "✓" if result['passed'] else "✗"
    print(f"\n{status} Response: '{response}'")
    print(f"   Expected: {expected}, Got: {result['actual']}")

# Demo 2: Code Quality
print("\n\n" + "=" * 70)
print("EXAMPLE 2: Code Quality Metric")
print("=" * 70)

code_metric = CodeQualityMetric()

code_examples = [
    '''
def add(a, b):
    """Add two numbers."""
    return a + b
''',
    '''
x = 5
y = 10
print(x + y)
'''
]

for i, code in enumerate(code_examples, 1):
    result = code_metric.evaluate(code)
    print(f"\nCode Example {i}:")
    print(f"  Score: {result['score']:.2f}")
    print(f"  Status: {'✓ PASS' if result['passed'] else '✗ FAIL'}")
    if result['issues']:
        print(f"  Issues: {', '.join(result['issues'])}")

# Demo 3: Medical Safety
print("\n\n" + "=" * 70)
print("EXAMPLE 3: Domain-Specific Safety")
print("=" * 70)

safety_metric = MedicalSafetyMetric()

medical_responses = [
    ("Try stretching exercises for back pain. But consult your doctor if pain persists.", True),
    ("Headaches can be caused by stress or dehydration.", True),
    ("The weather today is sunny.", False),
]

for response, is_medical in medical_responses:
    result = safety_metric.evaluate(response, is_medical)
    status = "✓" if result['passed'] else "✗"
    print(f"\n{status} Response: '{response[:50]}...'")
    print(f"   Medical topic: {is_medical}")
    if result.get('warning'):
        print(f"   ⚠️  {result['warning']}")

# ============================================================================
# COMBINING CUSTOM METRICS
# ============================================================================

print("\n\n" + "=" * 70)
print("COMBINING CUSTOM METRICS")
print("=" * 70)

def comprehensive_evaluation(response: str, **kwargs) -> Dict[str, Any]:
    """Run multiple custom metrics together."""
    
    metrics = {
        "sentiment": SentimentAppropriatenessMetric(),
        "medical_safety": MedicalSafetyMetric(),
    }
    
    results = {}
    for name, metric in metrics.items():
        if name == "sentiment" and "expected_sentiment" in kwargs:
            results[name] = metric.evaluate(response, kwargs["expected_sentiment"])
        elif name == "medical_safety" and "is_medical" in kwargs:
            results[name] = metric.evaluate(response, kwargs["is_medical"])
    
    # Calculate overall score
    scores = [r["score"] for r in results.values() if "score" in r]
    overall = sum(scores) / len(scores) if scores else 0
    
    return {
        "overall_score": overall,
        "passed": overall >= 0.8,
        "individual_results": results
    }

# Test
response = "Drink more water for headaches. Consult a doctor if severe."
result = comprehensive_evaluation(
    response,
    expected_sentiment="neutral",
    is_medical=True
)

print(f"\nResponse: {response}")
print(f"Overall Score: {result['overall_score']:.2f}")
print(f"Status: {'✓ PASS' if result['passed'] else '✗ FAIL'}")

# ============================================================================
# BEST PRACTICES
# ============================================================================

print("\n\n" + "=" * 70)
print("BEST PRACTICES")
print("=" * 70)

print("""
✅ DESIGN PRINCIPLES:

1. Clear Purpose
   • Know exactly what you're measuring
   • Document why this metric matters

2. Measurable Criteria
   • Define concrete checks
   • Avoid subjective judgments

3. Appropriate Thresholds
   • Set realistic pass/fail boundaries
   • Consider business requirements

4. Actionable Results
   • Provide clear feedback
   • Explain failures with details

5. Edge Case Handling
   • Test with unusual inputs
   • Handle missing/invalid data

🎯 IMPLEMENTATION CHECKLIST:

□ Name clearly describes what's measured
□ Has configurable threshold
□ Returns consistent dict structure
□ Includes explanatory information
□ Handles edge cases gracefully
□ Is testable and tested
□ Has documentation

⚠️ COMMON PITFALLS:

❌ Too complex (hard to debug)
❌ Too strict (fails too often)
❌ Too lenient (passes everything)
❌ Unclear failure messages
❌ Not validated with real data

💡 TESTING YOUR METRICS:

1. Test with known good examples (should pass)
2. Test with known bad examples (should fail)
3. Test edge cases (empty, very long, special chars)
4. Validate against human judgment
5. Monitor in production
""")

print("\n" + "=" * 70)
print("✨ Lesson 5 Complete!")
print("=" * 70)
print("\nNext: 06_production_evaluation.py - Production considerations!")
