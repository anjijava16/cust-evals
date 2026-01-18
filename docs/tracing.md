# Phoenix Tracing & Metrics (Optional)

**Tracing and metrics are completely optional.** Custom Evals works perfectly end-to-end without observability. This guide is only for users who want comprehensive monitoring with Phoenix (Arize).

## Why Tracing & Metrics?

Tracing and metrics provide full observability into your evaluations:

### Tracing (Individual Operations)
- 📊 **Visualize** evaluation flows in Phoenix UI
- 🔍 **Debug** specific requests and issues
- ⏱️ **Monitor** individual operation timing
- 🎯 **Track** execution paths

### Metrics (Aggregated Statistics)
- 📈 **Analyze** trends over time
- 📊 **Monitor** score distributions
- ⚡ **Track** latency percentiles (P50, P95, P99)
- 🚨 **Set alerts** for anomalies
- 📉 **Calculate** error rates

**When to use tracing & metrics:**
- Production deployments
- Performance monitoring
- A/B testing models
- Trend analysis and alerting

**When to skip:**
- Quick local testing
- Development and prototyping
- When Phoenix is not available
- Simple evaluation scripts

---

## Quick Start

### Option 1: Without Tracing (Default)

```python
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

# Just use evaluators normally
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

score = evaluator.evaluate({
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France.",
    "context": "Paris is the capital of France."
})

print(f"Result: {score.label}")  # Works perfectly without tracing!
```

### Option 2: With Tracing (Optional)

If you want observability, enable tracing:

```python
from custom.evals import initialize_tracing, HallucinationEvaluator
from custom.evals.llm import LLM

# Step 1: Initialize tracing (one-time setup)
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces"  # Your Phoenix endpoint
)

# Step 2: Use evaluators normally (now automatically traced!)
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

score = evaluator.evaluate({
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France.",
    "context": "Paris is the capital of France."
})

print(f"Result: {score.label}")  # Same code, now traced in Phoenix!
```

### Option 3: With Tracing + Metrics (Full Observability)

For complete monitoring with aggregated statistics:

```python
from custom.evals import initialize_tracing, HallucinationEvaluator
from custom.evals.llm import LLM

# Step 1: Initialize tracing AND metrics
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces",
    metrics_enabled=True  # Enable metrics collection!
)

# Step 2: Use evaluators normally (now traced + metrics collected!)
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

score = evaluator.evaluate({
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France.",
    "context": "Paris is the capital of France."
})

print(f"Result: {score.label}")
# Automatic metrics: evaluation count, score distribution, latency!
```

**📊 See [METRICS.md](./METRICS.md) for complete metrics documentation.**

---

## Setup (Only if You Want Tracing)

### 1. Install Tracing Dependencies

```bash
# Install with tracing support
pip install -e ".[dev,tracing]"
```

This adds OpenTelemetry packages for Phoenix integration.

### 2. Start Phoenix Server

```bash
# Install Phoenix
pip install arize-phoenix

# Start Phoenix server
python -m phoenix.server.main serve

# Opens at: http://localhost:6006
```

### 3. Initialize Tracing in Your Code

```python
from custom.evals import initialize_tracing

# Initialize once at the start of your script
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces"
)

# Now all evaluations are automatically traced!
```

---

## Configuration Options

### Basic Configuration

```python
from custom.evals import initialize_tracing

initialize_tracing(
    enabled=True,  # Enable/disable tracing
    service_name="my-app",  # Service name in Phoenix UI
    phoenix_endpoint="http://localhost:6006/v1/traces",  # Phoenix endpoint
    metrics_enabled=True,  # Enable metrics collection
    metrics_export_interval=30000  # Export metrics every 30 seconds
)
```

### Using Environment Variables

```bash
# Set Phoenix endpoint via environment variable
export PHOENIX_COLLECTOR_ENDPOINT="http://localhost:6006/v1/traces"
```

```python
# Will use environment variable automatically
initialize_tracing()
```

### Console Export (Debugging)

```python
# Print traces to console for debugging
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces",
    console_export=True  # Enable console logging
)
```

### Disable Tracing

```python
# Tracing disabled (no overhead)
initialize_tracing(enabled=False)

# Or simply don't call initialize_tracing() at all
# Evaluations work normally without tracing
```

---

## What Gets Traced & Measured

### Traces (Individual Operations)

When tracing is enabled, every evaluation creates a span with:

**Span Attributes:**
- `evaluator.name` - Evaluator name (e.g., "hallucination")
- `evaluator.kind` - Type ("llm", "code", etc.)
- `evaluator.direction` - Optimization direction ("maximize", "minimize")
- `llm.model` - Model name (e.g., "gpt-4o-mini")
- `llm.provider` - Provider ("openai", "anthropic")
- `has_ground_truth` - Whether ground truth was provided
- `result.label` - Evaluation label (e.g., "factual", "hallucinated")
- `result.score` - Numerical score (0.0 to 1.0)
- `latency.seconds` - Evaluation latency

### Metrics (Aggregated Statistics)

When metrics are enabled (`metrics_enabled=True`), these metrics are automatically collected:

**1. `evals.evaluations.total` (Counter)**
- Total number of evaluations
- Labels: evaluator, label, model, provider

**2. `evals.score` (Histogram)**
- Distribution of evaluation scores
- Enables: P50, P95, P99, avg calculations
- Labels: evaluator, label, model, provider

**3. `evals.latency.seconds` (Histogram)**
- Distribution of evaluation latencies
- Enables: P50, P95, P99 latency calculations
- Labels: evaluator, label, model, provider

**📊 See [METRICS.md](./METRICS.md) for detailed metrics documentation.**

---

## Advanced Usage

### Custom Traced Functions

Trace your own functions:

```python
from custom.evals import traced

@traced("my_evaluation_pipeline")
def evaluate_batch(inputs):
    """Custom pipeline with tracing."""
    results = []
    for inp in inputs:
        score = evaluator.evaluate(inp)
        results.append(score)
    return results

# This function call will create a span in Phoenix
scores = evaluate_batch(my_inputs)
```

### Adding Custom Attributes

Add custom attributes to the current span:

```python
from custom.evals import add_span_attributes

# In your evaluation code
add_span_attributes({
    "dataset_name": "test_set_v2",
    "experiment_id": "exp_123",
    "batch_size": 32
})
```

---

## Using Phoenix UI

### View Traces

1. **Open Phoenix**: http://localhost:6006
2. **Navigate to Traces** tab
3. **Filter by**:
   - Service name: "custom-evals" (or your service name)
   - Time range
   - Evaluator name

### Analyze Performance

Phoenix shows:
- **Latency** - How long each evaluation took
- **Throughput** - Evaluations per second
- **Error rates** - Failed evaluations
- **Model usage** - Which models are used most

### Debug Issues

Click on any trace to see:
- Full span hierarchy
- All attributes
- Timing breakdown
- Error messages (if any)

---

## Example Scenarios

### Scenario 1: Quick Local Testing (No Tracing)

```python
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

# No tracing setup needed - just use evaluators
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

for test_input in test_cases:
    score = evaluator.evaluate(test_input)
    print(f"Result: {score.label}")
```

### Scenario 2: Production Monitoring (With Tracing)

```python
from custom.evals import initialize_tracing, HallucinationEvaluator
from custom.evals.llm import LLM

# Enable tracing for production monitoring
initialize_tracing(
    service_name="production-evals",
    phoenix_endpoint="http://phoenix-prod:6006/v1/traces"
)

# All evaluations now monitored in Phoenix
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

for test_input in test_cases:
    score = evaluator.evaluate(test_input)
    # Automatically traced!
```

### Scenario 3: A/B Testing Models

```python
from custom.evals import initialize_tracing, add_span_attributes

initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")

# Test with GPT-4o-mini
llm_mini = LLM(provider="openai", model="gpt-4o-mini")
evaluator_mini = HallucinationEvaluator(llm_mini)

add_span_attributes({"experiment": "model_comparison", "model_group": "mini"})
score_mini = evaluator_mini.evaluate(test_input)

# Test with GPT-4o
llm_4o = LLM(provider="openai", model="gpt-4o")
evaluator_4o = HallucinationEvaluator(llm_4o)

add_span_attributes({"experiment": "model_comparison", "model_group": "4o"})
score_4o = evaluator_4o.evaluate(test_input)

# Compare in Phoenix UI: Filter by experiment="model_comparison"
```

---

## Troubleshooting

### Tracing Not Working

**Check 1: Dependencies installed?**
```bash
pip install -e ".[tracing]"
```

**Check 2: Phoenix running?**
```bash
# Should return 200 OK
curl http://localhost:6006
```

**Check 3: Tracing initialized?**
```python
from custom.evals import initialize_tracing

initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces"
)
```

**Check 4: Enable console export for debugging**
```python
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces",
    console_export=True  # See traces in console
)
```

### No Traces in Phoenix UI

1. **Wait 2-3 seconds** - Traces are batched
2. **Refresh Phoenix UI** - Click refresh button
3. **Check service name filter** - Make sure it matches
4. **Check time range** - Adjust to "Last 15 minutes"

### Performance Impact

**Overhead:**
- Minimal: ~5-10ms per evaluation
- Async: Traces exported in background
- Production: Safe to use

**Disable if needed:**
```python
# No tracing overhead
initialize_tracing(enabled=False)

# Or don't call initialize_tracing() at all
```

---

## Complete Examples

### Tracing Example

See **[examples/tracing_example.py](../examples/tracing_example.py)** for a complete tracing example.

```bash
# Run the tracing example
python examples/tracing_example.py

# Open Phoenix UI
# http://localhost:6006
```

### Metrics Example (NEW!)

See **[examples/metrics_example.py](../examples/metrics_example.py)** for a complete metrics example.

```bash
# Run the metrics example
python examples/metrics_example.py

# Open Phoenix UI to see metrics
# http://localhost:6006
```

This example demonstrates:
- Automatic metric collection
- Custom metrics recording
- Viewing metrics in Phoenix
- Understanding metric types

---

## Key Takeaways

✅ **Tracing & metrics are completely optional** - Framework works perfectly without them

✅ **Easy to enable** - Just call `initialize_tracing()` with your Phoenix endpoint

✅ **Zero code changes** - Same evaluator code works with or without observability

✅ **Production-ready** - Minimal overhead (~5-10ms per evaluation)

✅ **Powerful observability** - Full visibility with traces + aggregated metrics

✅ **Automatic metrics** - Evaluators automatically record counts, scores, and latencies

✅ **Custom metrics** - Add your own counters and histograms as needed

---

## Learn More

- **[METRICS.md](./METRICS.md)** - Complete metrics guide (NEW!)
- **[examples/metrics_example.py](../examples/metrics_example.py)** - Metrics example code
- **[examples/tracing_example.py](../examples/tracing_example.py)** - Tracing example code
- **[Phoenix Documentation](https://docs.arize.com/phoenix)** - Official Phoenix docs
- **[OpenTelemetry](https://opentelemetry.io/)** - OpenTelemetry documentation

---

**Remember:** Tracing is optional. Use it when you need observability, skip it when you don't!
