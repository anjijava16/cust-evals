"""Test OpenTelemetry availability and configuration."""
import sys

print("=" * 80)
print("OpenTelemetry Availability Test")
print("=" * 80)

# Check if OpenTelemetry is installed
try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

    print("✓ All OpenTelemetry packages are available")
    OTEL_AVAILABLE = True
except ImportError as e:
    print(f"✗ OpenTelemetry import error: {e}")
    OTEL_AVAILABLE = False
    sys.exit(1)

# Test creating an OTLP exporter
try:
    endpoint = "http://localhost:6006/v1/traces"
    print(f"\nTesting OTLP exporter with endpoint: {endpoint}")

    exporter = OTLPSpanExporter(
        endpoint=endpoint,
        headers={}
    )
    print(f"✓ OTLP exporter created successfully")
    print(f"  - Endpoint: {exporter._endpoint}")
    print(f"  - Timeout: {exporter._timeout}")

except Exception as e:
    print(f"✗ Error creating OTLP exporter: {e}")
    sys.exit(1)

# Test tracer initialization
try:
    print("\nInitializing tracer provider...")
    resource = Resource(attributes={SERVICE_NAME: "test-service"})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer(__name__)
    print("✓ Tracer provider initialized")

    # Create a test span
    print("\nCreating test span...")
    with tracer.start_as_current_span("test-span") as span:
        span.set_attribute("test.attribute", "test-value")
        print("✓ Test span created")

    # Force flush
    print("\nFlushing spans...")
    result = provider.force_flush()
    print(f"✓ Flush result: {result}")

    # Shutdown
    print("\nShutting down...")
    result = provider.shutdown()
    print(f"✓ Shutdown result: {result}")

except Exception as e:
    print(f"✗ Error during tracing test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("✓ All tests passed!")
print("OpenTelemetry is properly configured and working.")
print("=" * 80)
