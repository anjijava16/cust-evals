# Phoenix (Arize) Tracing Integration

Custom Evals integrates with **Phoenix (Arize)** using **OpenTelemetry** for distributed tracing and observability.

## 🎯 Why Tracing?

**Benefits:**
- 📊 **Visualize** evaluation flows in Phoenix UI
- 🔍 **Debug** evaluation issues
- ⏱️ **Monitor** performance and latency
- 📈 **Analyze** patterns across evaluations
- 🎯 **Track** model usage and costs

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install tracing support
pip install -e ".[tracing]"

# Or install manually
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

### 2. Start Phoenix

```bash
# Install Phoenix
pip install arize-phoenix

# Start Phoenix server
python -m phoenix.server.main serve

# Opens at: http://localhost:6006
```

### 3. Initialize Tracing

```python
from custom.evals import initialize_tracing

# Initialize with Phoenix endpoint
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces"
)

print("✓ Tracing enabled!")
```

### 4. Run Evaluations (Automatically Traced!)

```python
from custom.evals import HallucinationEvaluator
from custom.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

# This evaluation is automatically traced!
score = evaluator.evaluate({
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France.",
    "context": "Paris is the capital of France."
})

print(f"Result: {score.label}")
# Check Phoenix UI at http://localhost:6006
```

That's it! All evaluations are now traced in Phoenix.

---

## 📊 What Gets Traced

Every evaluation creates a span in Phoenix with:

**Span Attributes:**
- `evaluator.name` - Evaluator name (e.g., "hallucination")
- `evaluator.kind` - Type ("llm", "code", etc.)
- `evaluator.direction` - Optimization direction ("maximize", "minimize")
- `llm.model` - Model name (e.g., "gpt-4o-mini")
- `llm.provider` - Provider ("openai", "anthropic")
- `has_ground_truth` - Whether ground truth was provided
- `result.label` - Evaluation label (e.g., "factual", "hallucinated")
- `result.score` - Numerical score (0.0 to 1.0)

**Example Trace:**
```
custom-evals-demo
└── evaluate.hallucination (2.3s)
    ├── evaluator.name: hallucination
    ├── evaluator.kind: llm
    ├── llm.model: gpt-4o-mini
    ├── llm.provider: openai
    ├── result.label: factual
    └── result.score: 0.0
```

---

## 🎨 Configuration Options

### Basic Configuration

```python
from custom.evals import initialize_tracing

initialize_tracing(
    enabled=True,  # Enable/disable tracing
    service_name="my-app",  # Service name in Phoenix
    phoenix_endpoint="http://localhost:6006/v1/traces"  # Phoenix endpoint
)
```

### Console Export (Debugging)

```python
# Print traces to console for debugging
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces",
    console_export=True  # Enable console logging
)
```

### Environment Variables

```bash
# Set Phoenix endpoint via environment variable
export PHOENIX_COLLECTOR_ENDPOINT="http://localhost:6006/v1/traces"
```

```python
# Will use environment variable automatically
initialize_tracing()
```

### Disable Tracing

```python
# Tracing disabled (no overhead)
initialize_tracing(enabled=False)

# Or don't call initialize_tracing() at all
# Evaluations work normally without tracing
```

---

## 🔧 Advanced Usage

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

# This function call will create a span
scores = evaluate_batch(my_inputs)
```

### Adding Custom Attributes

Add custom attributes to current span:

```python
from custom.evals import add_span_attributes

# In your evaluation code
add_span_attributes({
    "dataset_name": "test_set_v2",
    "experiment_id": "exp_123",
    "batch_size": 32
})
```

### Manual Spans

Create spans manually:

```python
from custom.evals import get_tracer

tracer = get_tracer()

with tracer.span("preprocessing", attributes={"step": "tokenization"}):
    # Your preprocessing code
    tokens = tokenize(text)

with tracer.span("evaluation"):
    score = evaluator.evaluate(input)
```

---

## 🖥️ Using Phoenix UI

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

## 📊 Example Scenarios

### Scenario 1: Debug Slow Evaluations

```python
from custom.evals import initialize_tracing, HallucinationEvaluator
from custom.evals.llm import LLM

# Enable tracing
initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")

llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

# Run evaluations
for i in range(100):
    score = evaluator.evaluate(test_inputs[i])

# Check Phoenix UI:
# - Sort by duration to find slow evaluations
# - Look for patterns in slow cases
# - Identify bottlenecks
```

### Scenario 2: A/B Test Models

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

# Phoenix UI: Filter by experiment="model_comparison"
# Compare: latency, cost, accuracy between models
```

### Scenario 3: Monitor Production

```python
from custom.evals import initialize_tracing

# In production
initialize_tracing(
    service_name="production-evals",
    phoenix_endpoint="http://phoenix-prod:6006/v1/traces"
)

# All evaluations traced automatically
# Monitor in Phoenix:
# - Evaluation volumes
# - Error rates
# - Performance trends
```

---

## 🛠️ Troubleshooting

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
```

---

## 📚 Complete Example

See [`examples/tracing_example.py`](examples/tracing_example.py) for a complete working example.

```bash
# Run the example
python examples/tracing_example.py

# Open Phoenix UI
# http://localhost:6006
```

---

## 🔗 Integration with Phoenix Features

### Datasets

Upload evaluation results to Phoenix:

```python
# After running evaluations
import phoenix as px

# Log evaluations as a dataset
px.Client().log_evaluations(
    evaluations=your_evaluations,
    dataset_name="my_eval_results"
)
```

### Experiments

Track experiments in Phoenix:

```python
from custom.evals import add_span_attributes

add_span_attributes({
    "experiment.name": "prompt_optimization",
    "experiment.version": "v2",
    "experiment.config": "temperature_0.7"
})
```

---

## 🎯 Best Practices

### 1. Use Descriptive Service Names

```python
# Good
initialize_tracing(service_name="rag-eval-prod")

# Bad
initialize_tracing(service_name="app")
```

### 2. Add Context with Attributes

```python
from custom.evals import add_span_attributes

add_span_attributes({
    "user_id": user.id,
    "dataset": "test_set_v3",
    "environment": "production"
})
```

### 3. Trace Custom Pipelines

```python
from custom.evals import traced

@traced("evaluation_pipeline")
def full_pipeline(inputs):
    # Preprocessing
    processed = preprocess(inputs)

    # Evaluation
    scores = [evaluator.evaluate(inp) for inp in processed]

    # Post-processing
    return aggregate(scores)
```

### 4. Monitor in Production

- Set up Phoenix in production environment
- Track evaluation volumes and latency
- Set up alerts for anomalies
- Review traces regularly

---

## 📖 Resources

- **Phoenix Documentation**: https://docs.arize.com/phoenix
- **OpenTelemetry**: https://opentelemetry.io/
- **Example**: [`examples/tracing_example.py`](examples/tracing_example.py)

---

## ✅ Summary

**Setup (5 minutes):**
1. Install: `pip install -e ".[tracing]"`
2. Start Phoenix: `python -m phoenix.server.main serve`
3. Initialize: `initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")`

**Benefits:**
- ✅ Automatic tracing of all evaluations
- ✅ Visualize in Phoenix UI
- ✅ Debug performance issues
- ✅ Monitor production usage
- ✅ Track experiments

**Optional:**
- Tracing is optional (framework works without it)
- No overhead if not initialized
- Easy to enable/disable

**Phoenix Integration:**
- ✅ Uses OpenTelemetry (standard)
- ✅ Compatible with Phoenix (Arize)
- ✅ Same tracing as Phoenix Evals

Your evaluations are now observable with Phoenix! 🎉
