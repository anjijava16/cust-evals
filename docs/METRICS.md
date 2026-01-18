# Metrics Guide

This guide explains how to use OpenTelemetry metrics with Custom Evals and Phoenix for comprehensive observability of your evaluation pipeline.

## Table of Contents

- [Overview](#overview)
- [What's Missing vs What You Have](#whats-missing-vs-what-you-have)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Metrics Types](#metrics-types)
- [Automatic Metrics](#automatic-metrics)
- [Custom Metrics](#custom-metrics)
- [Viewing Metrics in Phoenix](#viewing-metrics-in-phoenix)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

### What are Metrics?

**Metrics** are aggregated numerical measurements collected over time. Unlike traces (which show individual operations), metrics provide statistical views of your system's behavior.

**Common use cases:**
- Track evaluation counts over time
- Monitor score distributions
- Measure latency percentiles (P50, P95, P99)
- Set up alerts for anomalies
- Analyze trends and patterns

### Traces vs Metrics

| Feature | Traces | Metrics |
|---------|--------|---------|
| **Granularity** | Individual operations | Aggregated data |
| **Storage** | High volume | Low volume |
| **Use case** | Debug specific requests | Monitor trends |
| **Example** | "This evaluation took 1.5s" | "P95 latency is 2.1s" |

**Best practice:** Use both together for full observability!

---

## What's Missing vs What You Have

### Before (Traces Only)

Your original implementation only exported **traces** to Phoenix:

```python
# Only traces were sent
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces"
)
```

**What you could see:**
- ✅ Individual evaluation spans
- ✅ Timing for each evaluation
- ✅ Attributes and labels

**What was missing:**
- ❌ Aggregated statistics (avg, p95, p99)
- ❌ Time-series data (trends over time)
- ❌ Counters (total evaluations)
- ❌ Distributions (score histograms)
- ❌ Rate calculations (evals/second)

### Now (Traces + Metrics)

The enhanced implementation exports **both traces and metrics**:

```python
# Both traces and metrics are sent
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces",
    metrics_enabled=True,  # NEW!
    metrics_export_interval=30000  # Export every 30s
)
```

**What you have now:**
- ✅ Everything from before (traces)
- ✅ Aggregated statistics
- ✅ Time-series dashboards
- ✅ Evaluation counters
- ✅ Score and latency distributions
- ✅ Automatic metric collection

---

## Installation

Install OpenTelemetry dependencies:

```bash
pip install -e ".[tracing]"
```

This installs:
- `opentelemetry-api` - Core API
- `opentelemetry-sdk` - SDK for metrics and traces
- `opentelemetry-exporter-otlp` - Phoenix exporter

---

## Quick Start

### Basic Setup

```python
from custom.evals import initialize_tracing

# Initialize with metrics enabled
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces",
    metrics_enabled=True,
    metrics_export_interval=30000  # Export every 30 seconds
)
```

### Full Example

```python
from custom.evals import (
    initialize_tracing,
    HallucinationEvaluator
)
from custom.evals.llm import LLM

# 1. Initialize tracing + metrics
initialize_tracing(
    service_name="my-eval-service",
    phoenix_endpoint="http://localhost:6006/v1/traces",
    metrics_enabled=True
)

# 2. Run evaluations (metrics automatically collected)
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

score = evaluator.evaluate({
    "input": "What is AI?",
    "output": "AI is artificial intelligence.",
    "context": "AI stands for artificial intelligence."
})

# Metrics automatically recorded:
# - evals.evaluations.total += 1
# - evals.score histogram += 0.0
# - evals.latency.seconds histogram += <latency>
```

See [`examples/metrics_example.py`](../examples/metrics_example.py) for a complete example.

---

## Metrics Types

OpenTelemetry supports several metric types:

### 1. Counter

**Description:** Monotonically increasing value (never decreases)

**Use cases:**
- Total evaluations
- Error counts
- Request counts

**Example:**
```python
from custom.evals.tracing import record_counter

record_counter(
    "evals.evaluations.total",
    value=1,
    attributes={"evaluator": "hallucination"}
)
```

### 2. Histogram

**Description:** Distribution of values (with buckets/percentiles)

**Use cases:**
- Latency distributions
- Score distributions
- Request sizes

**Example:**
```python
from custom.evals.tracing import record_histogram

# Record latency
record_histogram(
    "evals.latency.seconds",
    value=1.234,
    attributes={"evaluator": "faithfulness"}
)

# Record score
record_histogram(
    "evals.score",
    value=0.95,
    attributes={"evaluator": "hallucination", "label": "factual"}
)
```

### 3. UpDownCounter (Gauge-like)

**Description:** Value that can increase or decrease

**Use cases:**
- Active connections
- Queue sizes
- Current load

**Example:**
```python
from custom.evals.tracing import get_tracer

tracer = get_tracer()
gauge = tracer.get_up_down_counter("app.active_evaluations")
gauge.add(1)  # Increment
# ... later ...
gauge.add(-1)  # Decrement
```

---

## Automatic Metrics

All LLM-based evaluators automatically record metrics when evaluations run.

### Collected Metrics

#### 1. `evals.evaluations.total`

**Type:** Counter
**Description:** Total number of evaluations
**Labels:**
- `evaluator` - Evaluator name (e.g., "hallucination")
- `label` - Result label (e.g., "factual", "hallucinated")
- `model` - Model name (e.g., "gpt-4o-mini")
- `provider` - Provider name (e.g., "openai")

**Example queries:**
- Total evaluations: `sum(evals.evaluations.total)`
- By evaluator: `sum by (evaluator) (evals.evaluations.total)`
- By label: `sum by (label) (evals.evaluations.total)`

#### 2. `evals.score`

**Type:** Histogram
**Description:** Distribution of evaluation scores
**Labels:** Same as above

**Example queries:**
- Average score: `avg(evals.score)`
- P95 score: `histogram_quantile(0.95, evals.score)`
- By evaluator: `avg by (evaluator) (evals.score)`

#### 3. `evals.latency.seconds`

**Type:** Histogram
**Description:** Evaluation latency in seconds
**Labels:** Same as above

**Example queries:**
- P50 latency: `histogram_quantile(0.50, evals.latency.seconds)`
- P95 latency: `histogram_quantile(0.95, evals.latency.seconds)`
- P99 latency: `histogram_quantile(0.99, evals.latency.seconds)`
- By model: `avg by (model) (evals.latency.seconds)`

### How It Works

Metrics are automatically recorded in the `_evaluate` method of `LLMEvaluator`:

```python
# Inside llm_evaluators.py
def _evaluate(self, eval_input):
    start_time = time.time()

    # ... evaluation logic ...

    # Automatic metrics recording
    record_evaluation_metrics(
        evaluator_name=self.name,
        score=score_value,
        label=label,
        latency_seconds=time.time() - start_time,
        model=self.llm.model,
        provider=self.llm.provider
    )
```

---

## Custom Metrics

You can record custom metrics for application-specific monitoring.

### Basic Recording

```python
from custom.evals.tracing import record_counter, record_histogram

# Record a counter
record_counter(
    "app.batch_jobs.completed",
    value=1,
    attributes={"job_type": "evaluation"}
)

# Record a histogram
record_histogram(
    "app.batch_size",
    value=100,
    attributes={"batch_type": "daily"}
)
```

### Using the Meter Directly

For advanced use cases, get the meter instance:

```python
from custom.evals.tracing import get_meter

meter = get_meter()
if meter:
    # Create instruments
    counter = meter.create_counter(
        name="app.custom_counter",
        description="My custom counter",
        unit="1"
    )

    histogram = meter.create_histogram(
        name="app.processing_time",
        description="Processing time",
        unit="ms"
    )

    # Record values
    counter.add(1, {"key": "value"})
    histogram.record(250.5, {"operation": "process"})
```

### Convenience Function

Use `record_evaluation_metrics` for standard evaluation metrics:

```python
from custom.evals.tracing import record_evaluation_metrics

record_evaluation_metrics(
    evaluator_name="custom_evaluator",
    score=0.85,
    label="positive",
    latency_seconds=1.2,
    model="gpt-4o-mini",
    provider="openai"
)
```

This records all three metrics (counter, score histogram, latency histogram) at once.

---

## Viewing Metrics in Phoenix

### Starting Phoenix

```bash
python -m phoenix.server.main serve
```

Phoenix runs at: http://localhost:6006

### Accessing Metrics

1. **Open Phoenix UI:** Navigate to http://localhost:6006
2. **Go to Metrics tab:** Look for "Metrics" or "Monitoring" section
3. **Filter by service:** Select your service name (e.g., "custom-evals")
4. **Explore metrics:**
   - View time-series graphs
   - Filter by labels/attributes
   - Calculate percentiles
   - Set up alerts

### Example Visualizations

**Evaluation Rate:**
```
rate(evals.evaluations.total[5m])
```
Shows evaluations per second over 5-minute windows.

**Average Score by Evaluator:**
```
avg by (evaluator) (evals.score)
```

**P95 Latency:**
```
histogram_quantile(0.95, evals.latency.seconds)
```

**Error Rate:**
```
sum by (label) (evals.evaluations.total{label="error"})
/ sum(evals.evaluations.total)
```

### Understanding Phoenix Metrics UI

Phoenix provides:
- **Time series graphs:** Metrics over time
- **Heatmaps:** Distribution visualizations
- **Aggregations:** Sum, avg, min, max, percentiles
- **Filtering:** By service, evaluator, model, label
- **Alerting:** Set thresholds for notifications

---

## Best Practices

### 1. Use Descriptive Metric Names

**Good:**
```python
record_counter("evals.hallucination.detected")
```

**Bad:**
```python
record_counter("count")  # Too vague
```

### 2. Add Meaningful Labels

Labels enable filtering and grouping:

```python
record_histogram(
    "evals.score",
    value=score,
    attributes={
        "evaluator": "hallucination",
        "model": "gpt-4o-mini",
        "dataset": "production",
        "environment": "staging"
    }
)
```

### 3. Choose Appropriate Metric Types

- **Counter:** For things that only increase (totals, counts)
- **Histogram:** For distributions (latency, sizes, scores)
- **UpDownCounter:** For values that fluctuate (queue depth)

### 4. Set Reasonable Export Intervals

```python
# Fast (for demos/debugging)
metrics_export_interval=5000  # 5 seconds

# Normal (production)
metrics_export_interval=30000  # 30 seconds

# Slow (high-volume systems)
metrics_export_interval=60000  # 60 seconds
```

### 5. Monitor Key Metrics

Essential metrics to track:
- Evaluation throughput (evals/second)
- P95 and P99 latency
- Error rate
- Score distributions
- Model usage

### 6. Combine with Traces

Use traces for debugging specific issues, metrics for monitoring trends:

```python
# Both enabled for full observability
initialize_tracing(
    enabled=True,           # Traces
    metrics_enabled=True    # Metrics
)
```

### 7. Set Up Alerts

Configure Phoenix alerts for:
- High error rates
- Elevated latency (P95 > threshold)
- Low evaluation throughput
- Unusual score distributions

---

## Troubleshooting

### Metrics Not Showing Up

**Problem:** Metrics aren't visible in Phoenix.

**Solutions:**

1. **Check metrics are enabled:**
   ```python
   initialize_tracing(metrics_enabled=True)
   ```

2. **Wait for export interval:**
   Metrics export periodically (default: 30s). Wait at least one interval.

3. **Verify Phoenix endpoint:**
   ```python
   initialize_tracing(
       phoenix_endpoint="http://localhost:6006/v1/traces"
   )
   # Metrics endpoint derived automatically: /v1/metrics
   ```

4. **Check Phoenix is running:**
   ```bash
   curl http://localhost:6006/healthz
   ```

5. **Enable console export for debugging:**
   ```python
   initialize_tracing(
       metrics_enabled=True,
       console_export=True  # Print metrics to console
   )
   ```

### Dependencies Not Installed

**Problem:** `ImportError` for OpenTelemetry modules.

**Solution:**
```bash
pip install -e ".[tracing]"
```

### Metrics Export Failing

**Problem:** Errors in Phoenix logs.

**Solutions:**

1. **Check endpoint format:**
   - Correct: `http://localhost:6006/v1/traces`
   - Incorrect: `http://localhost:6006` (missing path)

2. **Verify network connectivity:**
   ```bash
   curl -X POST http://localhost:6006/v1/metrics
   ```

3. **Check Phoenix version:**
   Ensure Phoenix version supports OTLP metrics (v3.0+).

### High Memory Usage

**Problem:** Metrics consuming too much memory.

**Solutions:**

1. **Reduce export frequency:**
   ```python
   metrics_export_interval=60000  # Export less often
   ```

2. **Limit metric labels:**
   Too many unique label combinations create many time series.

   **Bad:**
   ```python
   attributes={"user_id": user_id}  # High cardinality!
   ```

   **Good:**
   ```python
   attributes={"user_tier": "premium"}  # Low cardinality
   ```

### Metrics vs Traces Confusion

**Problem:** Not sure when to use metrics vs traces.

**Rule of thumb:**
- **Traces:** "What happened in this specific request?"
- **Metrics:** "What's the overall trend?"

**Use traces when:**
- Debugging a specific issue
- Understanding execution flow
- Finding bottlenecks in one request

**Use metrics when:**
- Monitoring system health
- Detecting trends
- Setting up alerts
- Analyzing aggregated data

---

## Advanced Topics

### Custom Metric Exporters

Export to multiple backends:

```python
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader

# Add Prometheus exporter
prometheus_reader = PrometheusMetricReader()

# Modify tracing.py to support multiple exporters
# (Advanced - requires code changes)
```

### Metric Aggregation

Control how metrics are aggregated:

```python
from opentelemetry.sdk.metrics import Aggregation

# Configure histogram buckets
histogram = meter.create_histogram(
    name="custom.latency",
    description="Custom latency",
    unit="s"
)
# Default buckets: [0, 5, 10, 25, 50, 75, 100, 250, 500, 1000]
```

### Delta vs Cumulative

OpenTelemetry supports two aggregation temporalities:
- **Cumulative:** Total since start (default)
- **Delta:** Change since last export

Phoenix typically uses cumulative for easier querying.

---

## What's Next?

### Related Documentation

- [Tracing Guide](./TRACING.md) - Learn about distributed tracing
- [API Reference](./API.md) - Full API documentation
- [Examples](../examples/) - More code examples

### Learn More

- [OpenTelemetry Metrics Spec](https://opentelemetry.io/docs/specs/otel/metrics/)
- [Phoenix Documentation](https://docs.arize.com/phoenix/)
- [Observability Best Practices](https://opentelemetry.io/docs/concepts/observability-primer/)

---

## Summary

### Key Takeaways

1. **Metrics ≠ Traces:**
   - Traces show individual operations
   - Metrics show aggregated statistics

2. **Automatic Collection:**
   - All evaluators automatically record metrics
   - No code changes needed for basic monitoring

3. **Three Core Metrics:**
   - `evals.evaluations.total` - Counter
   - `evals.score` - Histogram
   - `evals.latency.seconds` - Histogram

4. **Custom Metrics:**
   - Use `record_counter()` and `record_histogram()`
   - Add labels for filtering and grouping

5. **Phoenix Integration:**
   - Metrics export to Phoenix automatically
   - View in Phoenix UI for monitoring and alerting

### Getting Started Checklist

- [ ] Install dependencies: `pip install -e ".[tracing]"`
- [ ] Start Phoenix: `python -m phoenix.server.main serve`
- [ ] Enable metrics: `initialize_tracing(metrics_enabled=True)`
- [ ] Run evaluations
- [ ] Open Phoenix UI: http://localhost:6006
- [ ] View metrics in Metrics tab
- [ ] Set up alerts for key metrics

---

**Questions or issues?** See [Troubleshooting](#troubleshooting) or open an issue on GitHub.
