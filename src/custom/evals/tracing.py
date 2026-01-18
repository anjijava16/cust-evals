"""OpenTelemetry tracing and metrics support for Custom Evals.

Integrates with Phoenix (Arize) for distributed tracing and observability.

Features:
- Distributed tracing with span tracking
- Metrics collection (counters, histograms, gauges)
- Phoenix integration for visualization
- Automatic evaluation instrumentation
"""

import os
from contextlib import contextmanager
from typing import Any, Dict, Optional
from functools import wraps

# Check if OpenTelemetry is available
try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME

    # Try to import both HTTP and gRPC exporters
    try:
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as GRPCSpanExporter
        from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter as GRPCMetricExporter
        GRPC_AVAILABLE = True
    except ImportError:
        GRPC_AVAILABLE = False
        GRPCSpanExporter = None
        GRPCMetricExporter = None

    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as HTTPSpanExporter
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter as HTTPMetricExporter
        HTTP_AVAILABLE = True
    except ImportError:
        HTTP_AVAILABLE = False
        HTTPSpanExporter = None
        HTTPMetricExporter = None

    # Metrics imports
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    GRPC_AVAILABLE = False
    HTTP_AVAILABLE = False
    trace = None
    metrics = None


class TracingConfig:
    """Configuration for tracing and metrics."""

    def __init__(
        self,
        enabled: bool = True,
        service_name: str = "custom-evals",
        phoenix_endpoint: Optional[str] = None,
        console_export: bool = False,
        metrics_enabled: bool = True,
        metrics_export_interval: int = 30000,  # 30 seconds in milliseconds
        protocol: str = "grpc"  # "grpc" or "http"
    ):
        """Initialize tracing and metrics configuration.

        Args:
            enabled: Whether tracing is enabled
            service_name: Service name for traces and metrics
            phoenix_endpoint: Phoenix collector endpoint (e.g., "http://localhost:4317" for gRPC or "http://localhost:6006/v1/traces" for HTTP)
            console_export: Whether to export traces/metrics to console (for debugging)
            metrics_enabled: Whether metrics collection is enabled
            metrics_export_interval: Metrics export interval in milliseconds (default: 30s)
            protocol: Protocol to use ("grpc" or "http"). gRPC is recommended for Phoenix. (default: "grpc")
        """
        self.enabled = enabled and OTEL_AVAILABLE
        self.service_name = service_name
        self.phoenix_endpoint = phoenix_endpoint or os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:4317")
        self.console_export = console_export
        self.metrics_enabled = metrics_enabled and OTEL_AVAILABLE
        self.metrics_export_interval = metrics_export_interval
        self.protocol = protocol.lower()

        if self.enabled and not OTEL_AVAILABLE:
            print("Warning: OpenTelemetry not installed. Install with: uv pip install -e '.[tracing]'")


class Tracer:
    """Tracer and Meter for Custom Evals with Phoenix integration."""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize tracer and meter."""
        if not self._initialized:
            self.config = TracingConfig()
            self.tracer = None
            self.meter = None
            self.metrics_instruments = {}  # Cache for metric instruments
            self.tracer_provider = None  # Store provider for shutdown
            self.meter_provider = None  # Store provider for shutdown
            self._initialized = True

    def initialize(self, config: Optional[TracingConfig] = None):
        """Initialize OpenTelemetry tracing and metrics.

        Args:
            config: Tracing configuration
        """
        if config:
            self.config = config

        if not self.config.enabled:
            return

        if not OTEL_AVAILABLE:
            print("OpenTelemetry not available. Tracing disabled.")
            return

        # Create resource with service name
        resource = Resource(attributes={
            SERVICE_NAME: self.config.service_name
        })

        # ========================================
        # Initialize Tracing
        # ========================================
        provider = TracerProvider(resource=resource)

        # Add trace exporters
        if self.config.phoenix_endpoint:
            # Choose exporter based on protocol
            if self.config.protocol == "grpc" and GRPC_AVAILABLE:
                otlp_exporter = GRPCSpanExporter(
                    endpoint=self.config.phoenix_endpoint,
                    insecure=True  # Use insecure connection for localhost
                )
                print(f"✓ Phoenix tracing enabled (gRPC): {self.config.phoenix_endpoint}")
            elif self.config.protocol == "http" and HTTP_AVAILABLE:
                otlp_exporter = HTTPSpanExporter(
                    endpoint=self.config.phoenix_endpoint,
                    headers={}
                )
                print(f"✓ Phoenix tracing enabled (HTTP): {self.config.phoenix_endpoint}")
            else:
                print(f"✗ Warning: {self.config.protocol.upper()} protocol not available")
                otlp_exporter = None

            if otlp_exporter:
                provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

        if self.config.console_export:
            # Export to console (debugging)
            console_exporter = ConsoleSpanExporter()
            provider.add_span_processor(BatchSpanProcessor(console_exporter))

        # Set global tracer provider
        trace.set_tracer_provider(provider)

        # Store provider for shutdown
        self.tracer_provider = provider

        # Get tracer
        self.tracer = trace.get_tracer(__name__)

        # ========================================
        # Initialize Metrics
        # ========================================
        if self.config.metrics_enabled:
            metric_readers = []

            # Add metrics exporters
            if self.config.phoenix_endpoint:
                # Choose exporter based on protocol
                if self.config.protocol == "grpc" and GRPC_AVAILABLE:
                    # gRPC uses same endpoint for traces and metrics
                    otlp_metric_exporter = GRPCMetricExporter(
                        endpoint=self.config.phoenix_endpoint,
                        insecure=True  # Use insecure connection for localhost
                    )
                    metric_reader = PeriodicExportingMetricReader(
                        exporter=otlp_metric_exporter,
                        export_interval_millis=self.config.metrics_export_interval
                    )
                    metric_readers.append(metric_reader)
                    print(f"✓ Phoenix metrics enabled (gRPC): {self.config.phoenix_endpoint}")
                elif self.config.protocol == "http" and HTTP_AVAILABLE:
                    # HTTP needs separate endpoint for metrics
                    metrics_endpoint = self.config.phoenix_endpoint.replace('/v1/traces', '/v1/metrics')
                    print(f"⚠ Warning: Phoenix may not support HTTP metrics endpoint. Consider using gRPC instead.")
                    otlp_metric_exporter = HTTPMetricExporter(
                        endpoint=metrics_endpoint,
                        headers={}
                    )
                    metric_reader = PeriodicExportingMetricReader(
                        exporter=otlp_metric_exporter,
                        export_interval_millis=self.config.metrics_export_interval
                    )
                    metric_readers.append(metric_reader)
                    print(f"✓ Phoenix metrics enabled (HTTP): {metrics_endpoint}")
                else:
                    print(f"✗ Warning: {self.config.protocol.upper()} protocol not available for metrics")

            if self.config.console_export:
                # Export to console (debugging)
                console_metric_exporter = ConsoleMetricExporter()
                console_reader = PeriodicExportingMetricReader(
                    exporter=console_metric_exporter,
                    export_interval_millis=self.config.metrics_export_interval
                )
                metric_readers.append(console_reader)

            # Create meter provider
            meter_provider = MeterProvider(
                resource=resource,
                metric_readers=metric_readers
            )

            # Set global meter provider
            metrics.set_meter_provider(meter_provider)

            # Store provider for shutdown
            self.meter_provider = meter_provider

            # Get meter
            self.meter = metrics.get_meter(__name__)

    def get_tracer(self):
        """Get the tracer instance."""
        if not self.config.enabled or not OTEL_AVAILABLE:
            return None

        if self.tracer is None:
            self.initialize()

        return self.tracer

    def get_meter(self):
        """Get the meter instance for metrics.

        Returns:
            Meter instance or None if metrics disabled
        """
        if not self.config.metrics_enabled or not OTEL_AVAILABLE:
            return None

        if self.meter is None:
            self.initialize()

        return self.meter

    def get_counter(self, name: str, description: str = "", unit: str = ""):
        """Get or create a counter metric.

        Args:
            name: Counter name
            description: Counter description
            unit: Unit of measurement

        Returns:
            Counter instrument or None
        """
        if not self.config.metrics_enabled or self.meter is None:
            return None

        key = f"counter_{name}"
        if key not in self.metrics_instruments:
            self.metrics_instruments[key] = self.meter.create_counter(
                name=name,
                description=description,
                unit=unit
            )
        return self.metrics_instruments[key]

    def get_histogram(self, name: str, description: str = "", unit: str = ""):
        """Get or create a histogram metric.

        Args:
            name: Histogram name
            description: Histogram description
            unit: Unit of measurement

        Returns:
            Histogram instrument or None
        """
        if not self.config.metrics_enabled or self.meter is None:
            return None

        key = f"histogram_{name}"
        if key not in self.metrics_instruments:
            self.metrics_instruments[key] = self.meter.create_histogram(
                name=name,
                description=description,
                unit=unit
            )
        return self.metrics_instruments[key]

    def get_up_down_counter(self, name: str, description: str = "", unit: str = ""):
        """Get or create an up-down counter metric (gauge-like).

        Args:
            name: Counter name
            description: Counter description
            unit: Unit of measurement

        Returns:
            UpDownCounter instrument or None
        """
        if not self.config.metrics_enabled or self.meter is None:
            return None

        key = f"updowncounter_{name}"
        if key not in self.metrics_instruments:
            self.metrics_instruments[key] = self.meter.create_up_down_counter(
                name=name,
                description=description,
                unit=unit
            )
        return self.metrics_instruments[key]

    def record_counter(self, name: str, value: int = 1, attributes: Optional[Dict[str, Any]] = None):
        """Record a counter metric.

        Args:
            name: Counter name
            value: Value to add (default: 1)
            attributes: Metric attributes/labels
        """
        counter = self.get_counter(name)
        if counter:
            counter.add(value, attributes=attributes or {})

    def record_histogram(self, name: str, value: float, attributes: Optional[Dict[str, Any]] = None):
        """Record a histogram metric.

        Args:
            name: Histogram name
            value: Value to record
            attributes: Metric attributes/labels
        """
        histogram = self.get_histogram(name)
        if histogram:
            histogram.record(value, attributes=attributes or {})

    def force_flush(self, timeout_millis: int = 30000):
        """Force flush all pending traces and metrics.

        This should be called before the program exits to ensure all
        telemetry data is sent to the backend.

        Args:
            timeout_millis: Timeout in milliseconds (default: 30s)
        """
        if not self.config.enabled and not self.config.metrics_enabled:
            return

        if not OTEL_AVAILABLE:
            return

        success = True

        # Flush traces
        if self.tracer_provider:
            try:
                result = self.tracer_provider.force_flush(timeout_millis)
                if not result:
                    print("Warning: Trace flush timed out")
                    success = False
            except Exception as e:
                print(f"Warning: Error flushing traces: {e}")
                success = False

        # Flush metrics
        if self.meter_provider:
            try:
                result = self.meter_provider.force_flush(timeout_millis)
                if not result:
                    print("Warning: Metrics flush timed out")
                    success = False
            except Exception as e:
                print(f"Warning: Error flushing metrics: {e}")
                success = False

        return success

    def shutdown(self, timeout_millis: int = 30000):
        """Shutdown the tracer and meter providers.

        This flushes all pending data and releases resources.
        Should be called before program exit.

        Args:
            timeout_millis: Timeout in milliseconds (default: 30s)
        """
        if not self.config.enabled and not self.config.metrics_enabled:
            return

        if not OTEL_AVAILABLE:
            return

        success = True

        # Shutdown traces
        if self.tracer_provider:
            try:
                result = self.tracer_provider.shutdown()
                if not result:
                    print("Warning: Trace shutdown timed out")
                    success = False
            except Exception as e:
                print(f"Warning: Error shutting down traces: {e}")
                success = False

        # Shutdown metrics
        if self.meter_provider:
            try:
                result = self.meter_provider.shutdown()
                if not result:
                    print("Warning: Metrics shutdown timed out")
                    success = False
            except Exception as e:
                print(f"Warning: Error shutting down metrics: {e}")
                success = False

        return success

    @contextmanager
    def span(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """Create a span context.

        Args:
            name: Span name
            attributes: Span attributes

        Yields:
            Span context
        """
        if not self.config.enabled or not OTEL_AVAILABLE or self.tracer is None:
            yield None
            return

        with self.tracer.start_as_current_span(name) as span:
            if attributes:
                for key, value in attributes.items():
                    # Convert value to string if needed
                    if isinstance(value, (dict, list)):
                        value = str(value)
                    span.set_attribute(key, value)

            yield span


# Global tracer instance
_tracer = Tracer()


def initialize_tracing(
    enabled: bool = True,
    service_name: str = "custom-evals",
    phoenix_endpoint: Optional[str] = None,
    console_export: bool = False,
    metrics_enabled: bool = True,
    metrics_export_interval: int = 30000,
    protocol: str = "grpc"
):
    """Initialize tracing and metrics for Custom Evals.

    Args:
        enabled: Whether tracing is enabled
        service_name: Service name for traces and metrics
        phoenix_endpoint: Phoenix collector endpoint (e.g., "http://localhost:4317" for gRPC)
        console_export: Whether to export traces/metrics to console
        metrics_enabled: Whether metrics collection is enabled
        metrics_export_interval: Metrics export interval in milliseconds (default: 30s)
        protocol: Protocol to use - "grpc" (recommended) or "http" (default: "grpc")

    Example:
        >>> from custom.evals.tracing import initialize_tracing, shutdown_tracing
        >>>
        >>> # Initialize with Phoenix (traces + metrics using gRPC - recommended)
        >>> initialize_tracing(
        ...     phoenix_endpoint="http://localhost:4317",
        ...     metrics_enabled=True
        ... )
        >>>
        >>> # Now all evaluations will be traced and metrics collected
        >>> from custom.evals import HallucinationEvaluator
        >>> from custom.evals.llm import LLM
        >>>
        >>> llm = LLM(provider="openai", model="gpt-4o-mini")
        >>> evaluator = HallucinationEvaluator(llm)
        >>> score = evaluator.evaluate({...})  # Traced and metrics recorded!
        >>>
        >>> # Flush data to Phoenix before exit
        >>> shutdown_tracing()
    """
    config = TracingConfig(
        enabled=enabled,
        service_name=service_name,
        phoenix_endpoint=phoenix_endpoint,
        console_export=console_export,
        metrics_enabled=metrics_enabled,
        metrics_export_interval=metrics_export_interval,
        protocol=protocol
    )
    _tracer.initialize(config)


def get_tracer():
    """Get the global tracer instance.

    Returns:
        Tracer instance
    """
    return _tracer


def traced(name: Optional[str] = None):
    """Decorator to trace a function.

    Args:
        name: Span name (defaults to function name)

    Example:
        >>> from custom.evals.tracing import traced
        >>>
        >>> @traced("my_evaluation")
        >>> def my_evaluator(input_data):
        ...     # Your evaluation logic
        ...     return result
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            span_name = name or f"{func.__module__}.{func.__name__}"

            tracer = get_tracer()
            if not tracer.config.enabled or not OTEL_AVAILABLE:
                return func(*args, **kwargs)

            with tracer.span(span_name) as span:
                try:
                    result = func(*args, **kwargs)
                    if span:
                        span.set_attribute("success", True)
                    return result
                except Exception as e:
                    if span:
                        span.set_attribute("success", False)
                        span.set_attribute("error", str(e))
                    raise

        return wrapper
    return decorator


def add_span_attributes(attributes: Dict[str, Any]):
    """Add attributes to the current span.

    Args:
        attributes: Dictionary of attributes to add

    Example:
        >>> from custom.evals.tracing import add_span_attributes
        >>>
        >>> add_span_attributes({
        ...     "model": "gpt-4o-mini",
        ...     "evaluator": "hallucination",
        ...     "score": 0.95
        ... })
    """
    if not OTEL_AVAILABLE:
        return

    current_span = trace.get_current_span()
    if current_span:
        for key, value in attributes.items():
            if isinstance(value, (dict, list)):
                value = str(value)
            current_span.set_attribute(key, value)


# ============================================================================
# Metrics Helper Functions
# ============================================================================

def get_meter():
    """Get the global meter instance for recording metrics.

    Returns:
        Meter instance or None if metrics disabled

    Example:
        >>> from custom.evals.tracing import get_meter
        >>>
        >>> meter = get_meter()
        >>> if meter:
        ...     counter = meter.create_counter("my_counter")
        ...     counter.add(1)
    """
    return _tracer.get_meter()


def record_counter(name: str, value: int = 1, attributes: Optional[Dict[str, Any]] = None):
    """Record a counter metric (monotonically increasing).

    Args:
        name: Counter name
        value: Value to add (default: 1)
        attributes: Metric attributes/labels (e.g., {"evaluator": "hallucination"})

    Example:
        >>> from custom.evals.tracing import record_counter
        >>>
        >>> # Count evaluation runs
        >>> record_counter("evals.evaluations.total", 1, {
        ...     "evaluator": "hallucination",
        ...     "model": "gpt-4o-mini"
        ... })
    """
    _tracer.record_counter(name, value, attributes)


def record_histogram(name: str, value: float, attributes: Optional[Dict[str, Any]] = None):
    """Record a histogram metric (for distributions like latency, scores).

    Args:
        name: Histogram name
        value: Value to record
        attributes: Metric attributes/labels

    Example:
        >>> from custom.evals.tracing import record_histogram
        >>>
        >>> # Record evaluation score
        >>> record_histogram("evals.score", 0.95, {
        ...     "evaluator": "hallucination",
        ...     "label": "factual"
        ... })
        >>>
        >>> # Record evaluation latency
        >>> record_histogram("evals.latency", 1.234, {
        ...     "evaluator": "faithfulness",
        ...     "unit": "seconds"
        ... })
    """
    _tracer.record_histogram(name, value, attributes)


def record_evaluation_metrics(
    evaluator_name: str,
    score: float,
    label: str,
    latency_seconds: float,
    model: Optional[str] = None,
    provider: Optional[str] = None
):
    """Record standard evaluation metrics.

    This is a convenience function that records multiple metrics for an evaluation:
    - Counter: Total evaluations
    - Histogram: Score distribution
    - Histogram: Latency distribution

    Args:
        evaluator_name: Name of the evaluator (e.g., "hallucination")
        score: Evaluation score
        label: Evaluation label (e.g., "factual", "hallucinated")
        latency_seconds: Evaluation latency in seconds
        model: Model name (optional)
        provider: Provider name (optional)

    Example:
        >>> from custom.evals.tracing import record_evaluation_metrics
        >>>
        >>> record_evaluation_metrics(
        ...     evaluator_name="hallucination",
        ...     score=0.0,
        ...     label="factual",
        ...     latency_seconds=1.5,
        ...     model="gpt-4o-mini",
        ...     provider="openai"
        ... )
    """
    attributes = {
        "evaluator": evaluator_name,
        "label": label
    }

    if model:
        attributes["model"] = model
    if provider:
        attributes["provider"] = provider

    # Count total evaluations
    record_counter("evals.evaluations.total", 1, attributes)

    # Record score distribution
    record_histogram("evals.score", score, attributes)

    # Record latency distribution
    record_histogram("evals.latency.seconds", latency_seconds, attributes)


def force_flush_tracing(timeout_millis: int = 30000) -> bool:
    """Force flush all pending traces and metrics.

    Call this before your program exits to ensure all telemetry data
    is sent to Phoenix. This is especially important for short-lived scripts.

    Args:
        timeout_millis: Timeout in milliseconds (default: 30s)

    Returns:
        True if flush succeeded, False otherwise

    Example:
        >>> from custom.evals import initialize_tracing, force_flush_tracing
        >>>
        >>> initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")
        >>>
        >>> # ... run your evaluations ...
        >>>
        >>> # Before exiting, flush all data
        >>> force_flush_tracing()
    """
    return _tracer.force_flush(timeout_millis)


def shutdown_tracing(timeout_millis: int = 30000) -> bool:
    """Shutdown tracing and metrics providers.

    This flushes all pending data and releases resources.
    Call this at the end of your program for clean shutdown.

    Args:
        timeout_millis: Timeout in milliseconds (default: 30s)

    Returns:
        True if shutdown succeeded, False otherwise

    Example:
        >>> from custom.evals import initialize_tracing, shutdown_tracing
        >>>
        >>> initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")
        >>>
        >>> # ... run your evaluations ...
        >>>
        >>> # Clean shutdown
        >>> shutdown_tracing()
    """
    return _tracer.shutdown(timeout_millis)
