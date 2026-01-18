# Tracing Issue - FIXED

## Problem
Traces and metrics were not showing up in Phoenix because:
1. **OpenTelemetry was not installed** in the virtual environment
2. **Wrong endpoint** - was using HTTP endpoint instead of gRPC
3. **Missing shutdown logic** - spans weren't being flushed before program exit
4. **Metrics not supported** - Phoenix OTLP endpoint only supports traces, not metrics

## Solution

### 1. Install OpenTelemetry
```bash
cd /path/to/cust-evals
uv pip install -e ".[tracing]"
```

### 2. Update Your Script
Use gRPC protocol and call `shutdown_tracing()` before exit:

```python
from custom.evals import initialize_tracing, shutdown_tracing, HallucinationEvaluator
from custom.evals.llm import LLM

# Initialize with gRPC endpoint (port 4317, not 6006)
initialize_tracing(
    phoenix_endpoint="http://localhost:4317",  # gRPC endpoint
    metrics_enabled=False,  # Phoenix doesn't support metrics via OTLP
    protocol="grpc"
)

# Run your evaluations
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = HallucinationEvaluator(llm)

score = evaluator.evaluate({
    "input": "What is AI?",
    "output": "AI is artificial intelligence.",
    "context": "AI stands for artificial intelligence."
})

print(f"Score: {score.score}, Label: {score.label}")

# IMPORTANT: Flush traces to Phoenix before exit
shutdown_tracing()
```

### 3. Check Phoenix UI
Open http://localhost:6006/projects to see your traces.

## Key Changes Made

1. **Added `force_flush()` and `shutdown()` methods** to the Tracer class
2. **Added public API functions**: `force_flush_tracing()` and `shutdown_tracing()`
3. **Added gRPC protocol support** - Phoenix prefers gRPC over HTTP
4. **Set correct default endpoint**: `http://localhost:4317` for gRPC
5. **Exported new functions** from `__init__.py`

## Phoenix Endpoints

- **gRPC (recommended)**: `http://localhost:4317` - supports traces
- **HTTP**: `http://localhost:6006/v1/traces` - traces only, metrics not supported
- **UI**: `http://localhost:6006` - web interface

## Metrics Note

Phoenix's OTLP endpoint **does not support metrics**. Metrics will show "UNIMPLEMENTED" error.

For metrics, you have two options:
1. Disable metrics: `metrics_enabled=False`
2. Use console export for debugging: `console_export=True`

Phoenix uses its own metrics system - traces automatically include timing and attributes that can be used for analysis.
