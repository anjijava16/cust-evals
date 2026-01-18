"""
Lesson 6: Production Evaluation Patterns

Learn how to implement evaluation in production systems.

Learning Objectives:
- Batch vs real-time evaluation
- Monitoring and alerting
- A/B testing evaluation
- Human-in-the-loop patterns

Prerequisites: Lessons 1-5
"""

import time
from datetime import datetime

print("=" * 70)
print("LESSON 6: Production Evaluation Patterns")
print("=" * 70)

print("""
🏭 PRODUCTION VS DEVELOPMENT EVALUATION

Development:
• Batch evaluation on test sets
• Focus on accuracy
• Iterate quickly
• Manual inspection OK

Production:
• Real-time + batch evaluation
• Focus on reliability
• Monitor continuously
• Automated alerts needed
""")

# ============================================================================
# PATTERN 1: BATCH EVALUATION
# ============================================================================

print("\n" + "=" * 70)
print("PATTERN 1: Batch Evaluation")
print("=" * 70)

def batch_evaluate(test_cases: list, model_fn, eval_fn) -> dict:
    """
    Evaluate model on a batch of examples.
    Use for: Regression testing, model comparison
    """
    results = []
    start_time = time.time()
    
    for case in test_cases:
        # Get model response
        response = model_fn(case['input'])
        
        # Evaluate
        eval_result = eval_fn(response, case['expected'])
        
        results.append({
            'input': case['input'],
            'response': response,
            'expected': case['expected'],
            'score': eval_result['score'],
            'passed': eval_result['passed']
        })
    
    elapsed = time.time() - start_time
    
    # Aggregate metrics
    scores = [r['score'] for r in results]
    passed_count = sum(1 for r in results if r['passed'])
    
    return {
        'total_cases': len(results),
        'passed': passed_count,
        'failed': len(results) - passed_count,
        'pass_rate': passed_count / len(results) if results else 0,
        'avg_score': sum(scores) / len(scores) if scores else 0,
        'elapsed_seconds': elapsed,
        'results': results
    }

# Demo
def simple_model(input_text):
    # Simulated model
    return f"Response to: {input_text}"

def simple_eval(response, expected):
    return {'score': 0.8, 'passed': True}

test_data = [
    {'input': 'Test 1', 'expected': 'Expected 1'},
    {'input': 'Test 2', 'expected': 'Expected 2'},
]

result = batch_evaluate(test_data, simple_model, simple_eval)
print(f"\nBatch Evaluation Results:")
print(f"  Total: {result['total_cases']}")
print(f"  Passed: {result['passed']}")
print(f"  Pass Rate: {result['pass_rate']:.1%}")
print(f"  Avg Score: {result['avg_score']:.2f}")
print(f"  Time: {result['elapsed_seconds']:.2f}s")

# ============================================================================
# PATTERN 2: ONLINE EVALUATION
# ============================================================================

print("\n\n" + "=" * 70)
print("PATTERN 2: Online/Real-time Evaluation")
print("=" * 70)

class OnlineEvaluator:
    """
    Evaluate responses in real-time as they're generated.
    Use for: Production monitoring, immediate feedback
    """
    
    def __init__(self):
        self.metrics = {
            'total_requests': 0,
            'passed': 0,
            'failed': 0,
            'scores': []
        }
    
    def evaluate_response(self, response: str, expected: str = None) -> dict:
        """Evaluate single response in real-time."""
        self.metrics['total_requests'] += 1
        
        # Quick evaluation (must be fast!)
        score = 0.8  # Simplified
        passed = score >= 0.7
        
        if passed:
            self.metrics['passed'] += 1
        else:
            self.metrics['failed'] += 1
        
        self.metrics['scores'].append(score)
        
        # Keep only recent scores
        if len(self.metrics['scores']) > 100:
            self.metrics['scores'] = self.metrics['scores'][-100:]
        
        return {
            'score': score,
            'passed': passed,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_stats(self) -> dict:
        """Get current statistics."""
        scores = self.metrics['scores']
        return {
            'total': self.metrics['total_requests'],
            'pass_rate': self.metrics['passed'] / max(self.metrics['total_requests'], 1),
            'recent_avg_score': sum(scores) / len(scores) if scores else 0,
            'recent_min_score': min(scores) if scores else 0
        }

# Demo
evaluator = OnlineEvaluator()

print("\nSimulating real-time evaluation:")
for i in range(5):
    result = evaluator.evaluate_response(f"Response {i}")
    print(f"  Request {i+1}: Score={result['score']:.2f}, {'✓ PASS' if result['passed'] else '✗ FAIL'}")

stats = evaluator.get_stats()
print(f"\nCurrent Stats:")
print(f"  Total Requests: {stats['total']}")
print(f"  Pass Rate: {stats['pass_rate']:.1%}")
print(f"  Avg Score: {stats['recent_avg_score']:.2f}")

# ============================================================================
# PATTERN 3: MONITORING & ALERTING
# ============================================================================

print("\n\n" + "=" * 70)
print("PATTERN 3: Monitoring & Alerting")
print("=" * 70)

class EvaluationMonitor:
    """
    Monitor evaluation metrics and trigger alerts.
    """
    
    def __init__(self, alert_threshold: float = 0.7):
        self.alert_threshold = alert_threshold
        self.alerts = []
    
    def check_metrics(self, metrics: dict) -> list:
        """
        Check if metrics are within acceptable ranges.
        Return list of alerts if any.
        """
        alerts = []
        
        # Check pass rate
        if metrics.get('pass_rate', 1.0) < self.alert_threshold:
            alerts.append({
                'severity': 'HIGH',
                'metric': 'pass_rate',
                'value': metrics['pass_rate'],
                'threshold': self.alert_threshold,
                'message': f"Pass rate ({metrics['pass_rate']:.1%}) below threshold ({self.alert_threshold:.1%})"
            })
        
        # Check average score
        if metrics.get('avg_score', 1.0) < self.alert_threshold:
            alerts.append({
                'severity': 'MEDIUM',
                'metric': 'avg_score',
                'value': metrics['avg_score'],
                'threshold': self.alert_threshold,
                'message': f"Average score ({metrics['avg_score']:.2f}) below threshold ({self.alert_threshold:.2f})"
            })
        
        # Check for sudden drops
        recent_scores = metrics.get('recent_scores', [])
        if len(recent_scores) >= 2:
            recent_avg = sum(recent_scores[-10:]) / min(len(recent_scores), 10)
            prev_avg = sum(recent_scores[-20:-10]) / min(len(recent_scores[-20:-10]), 10) if len(recent_scores) >= 20 else recent_avg
            
            if recent_avg < prev_avg * 0.8:  # 20% drop
                alerts.append({
                    'severity': 'HIGH',
                    'metric': 'score_drop',
                    'message': f"Significant score drop detected: {prev_avg:.2f} → {recent_avg:.2f}"
                })
        
        self.alerts.extend(alerts)
        return alerts

# Demo
monitor = EvaluationMonitor(alert_threshold=0.75)

# Simulate declining metrics
scenarios = [
    {'pass_rate': 0.95, 'avg_score': 0.9, 'name': 'Good'},
    {'pass_rate': 0.7, 'avg_score': 0.75, 'name': 'Declining'},
    {'pass_rate': 0.6, 'avg_score': 0.65, 'name': 'Alert!'},
]

print("\nMonitoring simulation:")
for scenario in scenarios:
    alerts = monitor.check_metrics(scenario)
    print(f"\n{scenario['name']} metrics:")
    print(f"  Pass rate: {scenario['pass_rate']:.1%}")
    print(f"  Avg score: {scenario['avg_score']:.2f}")
    
    if alerts:
        print(f"  🚨 ALERTS:")
        for alert in alerts:
            print(f"    [{alert['severity']}] {alert['message']}")
    else:
        print(f"  ✓ All metrics OK")

# ============================================================================
# PATTERN 4: A/B TESTING
# ============================================================================

print("\n\n" + "=" * 70)
print("PATTERN 4: A/B Testing for Model Comparison")
print("=" * 70)

def ab_test(test_cases: list, model_a, model_b, eval_fn) -> dict:
    """
    Compare two models on same test cases.
    """
    results_a = []
    results_b = []
    
    for case in test_cases:
        # Test both models
        response_a = model_a(case['input'])
        response_b = model_b(case['input'])
        
        # Evaluate both
        eval_a = eval_fn(response_a, case['expected'])
        eval_b = eval_fn(response_b, case['expected'])
        
        results_a.append(eval_a['score'])
        results_b.append(eval_b['score'])
    
    # Compare
    avg_a = sum(results_a) / len(results_a) if results_a else 0
    avg_b = sum(results_b) / len(results_b) if results_b else 0
    
    winner = 'Model A' if avg_a > avg_b else 'Model B' if avg_b > avg_a else 'Tie'
    improvement = ((max(avg_a, avg_b) - min(avg_a, avg_b)) / min(avg_a, avg_b) * 100) if min(avg_a, avg_b) > 0 else 0
    
    return {
        'model_a_avg': avg_a,
        'model_b_avg': avg_b,
        'winner': winner,
        'improvement_pct': improvement,
        'significant': improvement > 5  # >5% difference
    }

# Demo
def model_a(input_text):
    return "Simple response"

def model_b(input_text):
    return "Detailed comprehensive response"

test_data = [{'input': f'Test {i}', 'expected': 'Good'} for i in range(10)]
ab_result = ab_test(test_data, model_a, model_b, simple_eval)

print("\nA/B Test Results:")
print(f"  Model A avg: {ab_result['model_a_avg']:.2f}")
print(f"  Model B avg: {ab_result['model_b_avg']:.2f}")
print(f"  Winner: {ab_result['winner']}")
print(f"  Improvement: {ab_result['improvement_pct']:.1f}%")
print(f"  Significant: {'Yes' if ab_result['significant'] else 'No'}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "=" * 70)
print("KEY TAKEAWAYS")
print("=" * 70)

print("""
🎯 PRODUCTION EVALUATION STRATEGIES:

1. BATCH EVALUATION
   ✓ Run regularly (daily/weekly)
   ✓ Use for regression testing
   ✓ Can be comprehensive (slow OK)
   
2. ONLINE EVALUATION
   ✓ Real-time monitoring
   ✓ Must be fast (<100ms)
   ✓ Use simple metrics
   
3. MONITORING & ALERTS
   ✓ Track key metrics continuously
   ✓ Alert on anomalies
   ✓ Set appropriate thresholds
   
4. A/B TESTING
   ✓ Compare changes scientifically
   ✓ Need statistical significance
   ✓ Run on representative data

💡 BEST PRACTICES:

✅ Automate everything
✅ Monitor metrics dashboards
✅ Set up alerts early
✅ Keep evaluation fast
✅ Version test datasets
✅ Log all evaluations
✅ Review failures manually
✅ Iterate based on data

⚠️ PRODUCTION PITFALLS:

❌ Eval too slow (blocks production)
❌ No alerting (miss issues)
❌ Stale test data (not representative)
❌ No logging (can't debug)
❌ Alert fatigue (too many false alarms)
""")

print("\n" + "=" * 70)
print("✨ Lesson 6 Complete!")
print("=" * 70)
print("\nNext: 07_using_cust_evals.py - Use the custom framework!")
