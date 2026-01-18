"""
Lesson 20: Efficiency & Performance Metrics (Expert)

Complete coverage of efficiency metrics: Latency, Throughput, Token Usage,
Cost optimization, and Context Window Utilization for production LLM systems.

Prerequisites: Lessons 1-19
Difficulty: ⭐⭐⭐⭐ Expert
Time: 50 minutes
"""

print("="*80)
print("LESSON 20: Efficiency & Performance Metrics")
print("="*80)

print("""
⚡ EFFICIENCY MATTERS

In production, quality isn't enough - you need efficiency:

1. Latency: How fast is the response?
2. Throughput: How many requests/second?
3. Token Usage: How many tokens per request?
4. Cost: What's the $ per request?
5. Context Window Utilization: Using context efficiently?

Poor efficiency = Expensive, slow, bad UX!
""")

from typing import List, Dict, Any
import time
from collections import defaultdict

# ============================================================================
# PART 1: LATENCY METRICS
# ============================================================================

print("\n" + "="*80)
print("PART 1: Latency Metrics - Speed Evaluation")
print("="*80)

print("""
⏱️ LATENCY METRICS:

Types of Latency:
1. Time to First Token (TTFT): Initial response delay
2. Time per Output Token (TPOT): Streaming speed
3. End-to-End Latency: Total request time
4. P50, P95, P99: Latency percentiles

Target Latency:
- Interactive: < 1 second
- Batch: < 30 seconds
- Real-time: < 200ms
""")

class LatencyEvaluator:
    """Evaluate latency and response time metrics."""

    def measure_latency(
        self,
        start_time: float,
        first_token_time: float = None,
        end_time: float = None,
        output_tokens: int = 0
    ) -> Dict[str, Any]:
        """
        Measure comprehensive latency metrics.

        Args:
            start_time: Request start timestamp
            first_token_time: First token received timestamp
            end_time: Request completion timestamp
            output_tokens: Number of tokens generated
        """
        if end_time is None:
            end_time = time.time()

        # Time to First Token (TTFT)
        ttft = (first_token_time - start_time) if first_token_time else None

        # End-to-End Latency
        e2e_latency = end_time - start_time

        # Time Per Output Token (TPOT)
        if first_token_time and output_tokens > 1:
            generation_time = end_time - first_token_time
            tpot = generation_time / (output_tokens - 1)  # Exclude first token
        else:
            tpot = None

        return {
            'ttft_seconds': ttft,
            'ttft_milliseconds': ttft * 1000 if ttft else None,
            'end_to_end_latency_seconds': e2e_latency,
            'end_to_end_latency_ms': e2e_latency * 1000,
            'tpot_seconds': tpot,
            'tpot_milliseconds': tpot * 1000 if tpot else None,
            'output_tokens': output_tokens,
            'tokens_per_second': output_tokens / e2e_latency if e2e_latency > 0 else 0
        }

    def calculate_percentiles(
        self,
        latencies: List[float],
        percentiles: List[int] = [50, 95, 99]
    ) -> Dict[str, float]:
        """
        Calculate latency percentiles.

        Args:
            latencies: List of latency measurements (seconds)
            percentiles: Which percentiles to calculate
        """
        if not latencies:
            return {f'p{p}': 0.0 for p in percentiles}

        sorted_latencies = sorted(latencies)
        n = len(sorted_latencies)

        results = {}
        for p in percentiles:
            idx = int((p / 100.0) * n)
            idx = min(idx, n - 1)  # Ensure within bounds
            results[f'p{p}'] = sorted_latencies[idx]

        # Also include min, max, mean
        results['min'] = min(latencies)
        results['max'] = max(latencies)
        results['mean'] = sum(latencies) / len(latencies)
        results['median'] = results['p50']

        return results

    def evaluate_latency_target(
        self,
        latency_seconds: float,
        target_seconds: float,
        use_case: str = 'interactive'
    ) -> Dict[str, Any]:
        """
        Evaluate if latency meets target.

        Args:
            latency_seconds: Measured latency
            target_seconds: Target latency
            use_case: Type of application
        """
        meets_target = latency_seconds <= target_seconds

        # Calculate margin
        if latency_seconds > 0:
            margin_percentage = ((target_seconds - latency_seconds) / target_seconds) * 100
        else:
            margin_percentage = 100.0

        # Severity based on overage
        if meets_target:
            severity = 'good'
        elif latency_seconds <= target_seconds * 1.5:
            severity = 'acceptable'
        elif latency_seconds <= target_seconds * 2.0:
            severity = 'poor'
        else:
            severity = 'critical'

        return {
            'latency_seconds': latency_seconds,
            'latency_ms': latency_seconds * 1000,
            'target_seconds': target_seconds,
            'target_ms': target_seconds * 1000,
            'meets_target': meets_target,
            'margin_percentage': margin_percentage,
            'severity': severity,
            'use_case': use_case
        }

# Demo
print("\n⏱️ Example: Latency Measurement")

latency_eval = LatencyEvaluator()

# Simulate request timing
start = time.time()
first_token = start + 0.15  # 150ms to first token
end = start + 1.2  # 1.2 seconds total
output_tokens = 100

result = latency_eval.measure_latency(start, first_token, end, output_tokens)

print(f"TTFT: {result['ttft_milliseconds']:.0f}ms")
print(f"End-to-End: {result['end_to_end_latency_ms']:.0f}ms")
print(f"TPOT: {result['tpot_milliseconds']:.2f}ms per token")
print(f"Throughput: {result['tokens_per_second']:.1f} tokens/sec")

# Percentile analysis
latencies = [0.8, 0.9, 1.1, 0.7, 1.5, 2.0, 0.95, 1.2, 1.8, 0.85]
percentiles = latency_eval.calculate_percentiles(latencies)

print(f"\nLatency Distribution:")
print(f"  P50 (median): {percentiles['p50']:.2f}s")
print(f"  P95: {percentiles['p95']:.2f}s")
print(f"  P99: {percentiles['p99']:.2f}s")
print(f"  Mean: {percentiles['mean']:.2f}s")

# Target evaluation
target_result = latency_eval.evaluate_latency_target(1.2, 1.0, 'interactive')
print(f"\nTarget Evaluation:")
print(f"  Latency: {target_result['latency_ms']:.0f}ms")
print(f"  Target: {target_result['target_ms']:.0f}ms")
print(f"  Meets Target: {'✓' if target_result['meets_target'] else '✗'}")
print(f"  Severity: {target_result['severity']}")

# ============================================================================
# PART 2: THROUGHPUT METRICS
# ============================================================================

print("\n\n" + "="*80)
print("PART 2: Throughput Metrics - Request Capacity")
print("="*80)

print("""
🚀 THROUGHPUT METRICS:

Measures system capacity:
1. Requests per Second (RPS)
2. Tokens per Second
3. Concurrent Request Capacity
4. Queue Time

Important for:
- Load testing
- Capacity planning
- Cost estimation
""")

class ThroughputEvaluator:
    """Evaluate system throughput."""

    def calculate_throughput(
        self,
        num_requests: int,
        time_window_seconds: float,
        total_tokens: int = 0
    ) -> Dict[str, Any]:
        """
        Calculate throughput metrics.

        Args:
            num_requests: Number of requests processed
            time_window_seconds: Time window for measurement
            total_tokens: Total tokens processed
        """
        requests_per_second = num_requests / time_window_seconds if time_window_seconds > 0 else 0
        tokens_per_second = total_tokens / time_window_seconds if time_window_seconds > 0 else 0

        # Calculate inverse for latency per request
        avg_latency_per_request = time_window_seconds / num_requests if num_requests > 0 else 0

        return {
            'requests_per_second': requests_per_second,
            'tokens_per_second': tokens_per_second,
            'avg_latency_per_request': avg_latency_per_request,
            'total_requests': num_requests,
            'total_tokens': total_tokens,
            'time_window_seconds': time_window_seconds
        }

    def evaluate_concurrent_capacity(
        self,
        concurrent_requests: List[int],
        successful_requests: List[int],
        failed_requests: List[int]
    ) -> Dict[str, Any]:
        """
        Evaluate system behavior under concurrent load.

        Args:
            concurrent_requests: Concurrency levels tested
            successful_requests: Successful requests at each level
            failed_requests: Failed requests at each level
        """
        results = []

        for i, concurrency in enumerate(concurrent_requests):
            success = successful_requests[i]
            failed = failed_requests[i]
            total = success + failed

            success_rate = success / total if total > 0 else 0.0

            results.append({
                'concurrency': concurrency,
                'success_rate': success_rate,
                'successful': success,
                'failed': failed,
                'total': total
            })

        # Find max stable concurrency (> 95% success)
        max_stable = 0
        for result in results:
            if result['success_rate'] >= 0.95:
                max_stable = max(max_stable, result['concurrency'])

        return {
            'max_stable_concurrency': max_stable,
            'concurrency_results': results
        }

    def calculate_queue_metrics(
        self,
        queue_times: List[float]
    ) -> Dict[str, Any]:
        """
        Calculate queuing metrics.

        Args:
            queue_times: List of time spent in queue (seconds)
        """
        if not queue_times:
            return {
                'avg_queue_time': 0.0,
                'max_queue_time': 0.0,
                'p95_queue_time': 0.0
            }

        avg_queue = sum(queue_times) / len(queue_times)
        max_queue = max(queue_times)

        # P95
        sorted_times = sorted(queue_times)
        p95_idx = int(0.95 * len(sorted_times))
        p95_queue = sorted_times[min(p95_idx, len(sorted_times) - 1)]

        return {
            'avg_queue_time_seconds': avg_queue,
            'max_queue_time_seconds': max_queue,
            'p95_queue_time_seconds': p95_queue,
            'total_queued_requests': len(queue_times)
        }

# Demo
print("\n🚀 Example: Throughput Evaluation")

throughput_eval = ThroughputEvaluator()

# Calculate throughput
result = throughput_eval.calculate_throughput(
    num_requests=1000,
    time_window_seconds=60.0,
    total_tokens=50000
)

print(f"Throughput Metrics:")
print(f"  RPS: {result['requests_per_second']:.1f} requests/sec")
print(f"  Token throughput: {result['tokens_per_second']:.1f} tokens/sec")
print(f"  Avg latency: {result['avg_latency_per_request']:.3f}s per request")

# Concurrent capacity
concurrent_results = throughput_eval.evaluate_concurrent_capacity(
    concurrent_requests=[10, 50, 100, 200],
    successful_requests=[10, 50, 98, 180],
    failed_requests=[0, 0, 2, 20]
)

print(f"\nConcurrent Capacity:")
print(f"  Max stable concurrency: {concurrent_results['max_stable_concurrency']}")
for result in concurrent_results['concurrency_results']:
    print(f"  {result['concurrency']} concurrent: {result['success_rate']:.1%} success rate")

# ============================================================================
# PART 3: TOKEN USAGE & COST METRICS
# ============================================================================

print("\n\n" + "="*80)
print("PART 3: Token Usage & Cost Metrics")
print("="*80)

print("""
💰 TOKEN USAGE & COST:

Track resource consumption:
1. Input Tokens per Request
2. Output Tokens per Request
3. Total Tokens
4. Cost per Request
5. Cost per User/Session

Critical for:
- Budget management
- Cost optimization
- Pricing strategy
""")

class TokenCostEvaluator:
    """Evaluate token usage and costs."""

    def __init__(self, pricing: Dict[str, float] = None):
        """
        Initialize with pricing model.

        Args:
            pricing: Cost per 1000 tokens {'input': X, 'output': Y}
        """
        self.pricing = pricing or {
            'input_per_1k': 0.01,  # $0.01 per 1K input tokens
            'output_per_1k': 0.03   # $0.03 per 1K output tokens
        }

    def calculate_token_usage(
        self,
        input_tokens: int,
        output_tokens: int
    ) -> Dict[str, Any]:
        """
        Calculate token usage metrics.
        """
        total_tokens = input_tokens + output_tokens

        # Calculate costs
        input_cost = (input_tokens / 1000) * self.pricing['input_per_1k']
        output_cost = (output_tokens / 1000) * self.pricing['output_per_1k']
        total_cost = input_cost + output_cost

        # Calculate ratios
        input_ratio = input_tokens / total_tokens if total_tokens > 0 else 0.0
        output_ratio = output_tokens / total_tokens if total_tokens > 0 else 0.0

        return {
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': total_tokens,
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': total_cost,
            'input_ratio': input_ratio,
            'output_ratio': output_ratio,
            'cost_per_token': total_cost / total_tokens if total_tokens > 0 else 0.0
        }

    def analyze_session_costs(
        self,
        session_requests: List[Dict[str, int]]
    ) -> Dict[str, Any]:
        """
        Analyze costs for a user session.

        Args:
            session_requests: List of {input_tokens, output_tokens}
        """
        total_input = sum(r['input_tokens'] for r in session_requests)
        total_output = sum(r['output_tokens'] for r in session_requests)
        num_requests = len(session_requests)

        session_cost = self.calculate_token_usage(total_input, total_output)

        # Per-request averages
        avg_input = total_input / num_requests if num_requests > 0 else 0
        avg_output = total_output / num_requests if num_requests > 0 else 0
        avg_cost = session_cost['total_cost'] / num_requests if num_requests > 0 else 0

        return {
            'total_cost': session_cost['total_cost'],
            'total_tokens': session_cost['total_tokens'],
            'num_requests': num_requests,
            'avg_tokens_per_request': session_cost['total_tokens'] / num_requests if num_requests > 0 else 0,
            'avg_cost_per_request': avg_cost,
            'avg_input_tokens': avg_input,
            'avg_output_tokens': avg_output
        }

    def compare_costs(
        self,
        scenarios: Dict[str, Dict[str, int]]
    ) -> Dict[str, Any]:
        """
        Compare costs across different scenarios.

        Args:
            scenarios: Dict of {scenario_name: {input_tokens, output_tokens}}
        """
        results = {}

        for name, tokens in scenarios.items():
            cost_result = self.calculate_token_usage(
                tokens['input_tokens'],
                tokens['output_tokens']
            )
            results[name] = cost_result

        return results

# Demo
print("\n💰 Example: Token Usage & Cost")

cost_eval = TokenCostEvaluator()

# Single request cost
usage = cost_eval.calculate_token_usage(
    input_tokens=1500,
    output_tokens=500
)

print(f"Single Request:")
print(f"  Input tokens: {usage['input_tokens']}")
print(f"  Output tokens: {usage['output_tokens']}")
print(f"  Total tokens: {usage['total_tokens']}")
print(f"  Input cost: ${usage['input_cost']:.4f}")
print(f"  Output cost: ${usage['output_cost']:.4f}")
print(f"  Total cost: ${usage['total_cost']:.4f}")

# Session analysis
session_requests = [
    {'input_tokens': 1000, 'output_tokens': 300},
    {'input_tokens': 1200, 'output_tokens': 400},
    {'input_tokens': 800, 'output_tokens': 250},
    {'input_tokens': 1500, 'output_tokens': 500}
]

session_result = cost_eval.analyze_session_costs(session_requests)

print(f"\nSession Analysis ({session_result['num_requests']} requests):")
print(f"  Total cost: ${session_result['total_cost']:.4f}")
print(f"  Avg cost/request: ${session_result['avg_cost_per_request']:.4f}")
print(f"  Avg tokens/request: {session_result['avg_tokens_per_request']:.0f}")

# Cost comparison
scenarios = {
    'short_prompt': {'input_tokens': 500, 'output_tokens': 200},
    'medium_prompt': {'input_tokens': 2000, 'output_tokens': 800},
    'long_prompt': {'input_tokens': 5000, 'output_tokens': 2000}
}

comparison = cost_eval.compare_costs(scenarios)

print(f"\nCost Comparison:")
for scenario, result in comparison.items():
    print(f"  {scenario}: ${result['total_cost']:.4f} ({result['total_tokens']} tokens)")

# ============================================================================
# PART 4: CONTEXT WINDOW UTILIZATION
# ============================================================================

print("\n\n" + "="*80)
print("PART 4: Context Window Utilization")
print("="*80)

print("""
📊 CONTEXT WINDOW UTILIZATION:

Efficient use of available context:
1. Utilization Rate: % of window used
2. Efficiency: Are all tokens useful?
3. Truncation Rate: How often truncated?
4. Waste: Unused relevant information

Context window is expensive - use it wisely!
""")

class ContextUtilizationEvaluator:
    """Evaluate context window utilization."""

    def __init__(self, max_context_tokens: int = 4096):
        """
        Initialize with model's max context window.

        Args:
            max_context_tokens: Maximum context window size
        """
        self.max_context_tokens = max_context_tokens

    def calculate_utilization(
        self,
        used_tokens: int,
        useful_tokens: int = None
    ) -> Dict[str, Any]:
        """
        Calculate context window utilization.

        Args:
            used_tokens: Tokens actually used
            useful_tokens: Tokens that contributed to response
        """
        utilization_rate = used_tokens / self.max_context_tokens

        # Efficiency: what % of used tokens were useful
        if useful_tokens is not None:
            efficiency = useful_tokens / used_tokens if used_tokens > 0 else 0.0
            wasted_tokens = used_tokens - useful_tokens
        else:
            efficiency = None
            wasted_tokens = None

        # Headroom
        remaining_tokens = self.max_context_tokens - used_tokens
        headroom_percentage = remaining_tokens / self.max_context_tokens

        # Categorize utilization
        if utilization_rate < 0.5:
            category = 'under-utilized'
        elif utilization_rate < 0.8:
            category = 'optimal'
        elif utilization_rate < 0.95:
            category = 'high'
        else:
            category = 'critical'

        return {
            'used_tokens': used_tokens,
            'max_tokens': self.max_context_tokens,
            'utilization_rate': utilization_rate,
            'utilization_percentage': utilization_rate * 100,
            'remaining_tokens': remaining_tokens,
            'headroom_percentage': headroom_percentage * 100,
            'efficiency': efficiency,
            'wasted_tokens': wasted_tokens,
            'category': category,
            'at_risk': utilization_rate > 0.9
        }

    def analyze_truncation(
        self,
        requests: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze truncation events.

        Args:
            requests: List of {desired_tokens, actual_tokens, truncated}
        """
        total_requests = len(requests)
        truncated_requests = sum(1 for r in requests if r.get('truncated', False))

        truncation_rate = truncated_requests / total_requests if total_requests > 0 else 0.0

        # Calculate token loss from truncation
        total_token_loss = sum(
            r['desired_tokens'] - r['actual_tokens']
            for r in requests if r.get('truncated', False)
        )

        avg_loss_per_truncation = total_token_loss / truncated_requests if truncated_requests > 0 else 0

        return {
            'truncation_rate': truncation_rate,
            'truncated_requests': truncated_requests,
            'total_requests': total_requests,
            'total_token_loss': total_token_loss,
            'avg_token_loss_per_truncation': avg_loss_per_truncation,
            'needs_attention': truncation_rate > 0.1
        }

    def optimize_context_packing(
        self,
        context_elements: List[Dict[str, Any]],
        priorities: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Suggest optimal context packing.

        Args:
            context_elements: List of {name, tokens, priority}
            priorities: Priority levels (higher = more important)
        """
        # Sort by priority
        sorted_elements = sorted(
            context_elements,
            key=lambda x: priorities.get(x['name'], 0),
            reverse=True
        )

        # Pack greedily
        packed = []
        total_tokens = 0

        for element in sorted_elements:
            if total_tokens + element['tokens'] <= self.max_context_tokens:
                packed.append(element['name'])
                total_tokens += element['tokens']

        # Calculate what was left out
        packed_names = set(packed)
        excluded = [e['name'] for e in context_elements if e['name'] not in packed_names]

        return {
            'packed_elements': packed,
            'excluded_elements': excluded,
            'total_tokens_packed': total_tokens,
            'utilization': total_tokens / self.max_context_tokens,
            'optimal': True
        }

# Demo
print("\n📊 Example: Context Utilization")

context_eval = ContextUtilizationEvaluator(max_context_tokens=4096)

# Utilization analysis
utilization = context_eval.calculate_utilization(
    used_tokens=3200,
    useful_tokens=2800
)

print(f"Context Utilization:")
print(f"  Used: {utilization['used_tokens']}/{utilization['max_tokens']} tokens")
print(f"  Utilization: {utilization['utilization_percentage']:.1f}%")
print(f"  Efficiency: {utilization['efficiency']:.1%}")
print(f"  Category: {utilization['category']}")
print(f"  At Risk: {'⚠️  YES' if utilization['at_risk'] else '✓ NO'}")

# Truncation analysis
requests = [
    {'desired_tokens': 3000, 'actual_tokens': 3000, 'truncated': False},
    {'desired_tokens': 5000, 'actual_tokens': 4096, 'truncated': True},
    {'desired_tokens': 3500, 'actual_tokens': 3500, 'truncated': False},
    {'desired_tokens': 4500, 'actual_tokens': 4096, 'truncated': True}
]

truncation = context_eval.analyze_truncation(requests)

print(f"\nTruncation Analysis:")
print(f"  Truncation rate: {truncation['truncation_rate']:.1%}")
print(f"  Truncated: {truncation['truncated_requests']}/{truncation['total_requests']}")
print(f"  Avg token loss: {truncation['avg_token_loss_per_truncation']:.0f} tokens")
print(f"  Needs Attention: {'⚠️  YES' if truncation['needs_attention'] else '✓ NO'}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "="*80)
print("KEY TAKEAWAYS")
print("="*80)

print("""
✅ EFFICIENCY METRICS SUMMARY:

1. LATENCY
   ✓ TTFT: < 500ms for interactive
   ✓ End-to-End: < 2s for most use cases
   ✓ Monitor P95, P99
   ✓ Streaming improves perceived latency

2. THROUGHPUT
   ✓ Target: > 10 RPS per instance
   ✓ Test concurrent capacity
   ✓ Monitor queue times
   ✓ Scale horizontally for capacity

3. TOKEN USAGE
   ✓ Track input/output separately
   ✓ Optimize prompts for efficiency
   ✓ Monitor cost per request
   ✓ Set budget alerts

4. COST
   ✓ Calculate per-request costs
   ✓ Track by user/session
   ✓ Optimize expensive operations
   ✓ Consider caching

5. CONTEXT UTILIZATION
   ✓ Target: 60-80% utilization
   ✓ Avoid >90% (truncation risk)
   ✓ Prioritize important context
   ✓ Monitor efficiency

📊 PRODUCTION EFFICIENCY DASHBOARD:

┌────────────────────────────────────────┐
│ LATENCY:   P50, P95, P99              │
│ THROUGHPUT: RPS, Tokens/sec           │
│ COST:      $/request, $/user          │
│ CONTEXT:   Utilization, Truncation    │
│ QUALITY:   Success rate, Error rate   │
└────────────────────────────────────────┘

🎯 OPTIMIZATION STRATEGIES:

1. Latency Reduction:
   - Use streaming
   - Optimize prompts (shorter)
   - Cache common responses
   - Use faster models when possible
   - Parallel tool calls

2. Cost Reduction:
   - Shorter prompts
   - Smaller models for simple tasks
   - Caching
   - Batch processing
   - Smart context management

3. Throughput Increase:
   - Horizontal scaling
   - Load balancing
   - Request batching
   - Async processing
   - Queue management

4. Context Optimization:
   - Prioritize relevant content
   - Remove redundant information
   - Summarize when appropriate
   - Dynamic context length
   - Smart truncation

⚠️  COMMON ISSUES:

1. High Latency:
   - Large prompts
   - Long outputs
   - Cold starts
   - Network issues

2. Low Throughput:
   - Insufficient capacity
   - Inefficient processing
   - Queue bottlenecks

3. High Costs:
   - Verbose prompts
   - Unnecessary context
   - No caching
   - Wrong model selection

4. Context Issues:
   - Over-utilization
   - Frequent truncation
   - Wasted tokens

💡 BEST PRACTICES:

1. Monitor Continuously:
   - Real-time dashboards
   - Automated alerts
   - Anomaly detection

2. Set SLOs:
   - Latency targets
   - Throughput minimums
   - Cost budgets
   - Error rate thresholds

3. Optimize Iteratively:
   - A/B test changes
   - Measure impact
   - Roll back if worse

4. Plan Capacity:
   - Load testing
   - Growth projections
   - Auto-scaling rules

5. Cost Management:
   - Budget tracking
   - Per-user limits
   - Alert thresholds
   - Regular audits

🔬 ADVANCED TOPICS:

- Model quantization for speed
- Speculative decoding
- Prompt caching
- KV cache optimization
- Continuous batching

CONGRATULATIONS! 🎉

You've completed ALL 20 comprehensive evaluation lessons!

You now have expert-level knowledge of:
✅ ALL text quality metrics
✅ ALL safety & alignment metrics
✅ ALL RAG-specific metrics
✅ ALL agent system metrics
✅ ALL task-specific metrics
✅ ALL efficiency & performance metrics

You're now a COMPLETE LLM Evaluation Expert! 🎓
""")

print("\n" + "="*80)
print("✨ Lesson 20 Complete - ALL LESSONS FINISHED!")
print("="*80)
print("\nReview METRICS_REFERENCE.md for comprehensive metric catalog!")
