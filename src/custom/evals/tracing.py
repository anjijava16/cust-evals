"""OpenTelemetry tracing support for Custom Evals.

Integrates with Phoenix (Arize) for distributed tracing and observability.
"""

import os
from contextlib import contextmanager
from typing import Any, Dict, Optional
from functools import wraps

# Check if OpenTelemetry is available
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    trace = None


class TracingConfig:
    """Configuration for tracing."""

    def __init__(
        self,
        enabled: bool = True,
        service_name: str = "custom-evals",
        phoenix_endpoint: Optional[str] = None,
        console_export: bool = False
    ):
        """Initialize tracing configuration.

        Args:
            enabled: Whether tracing is enabled
            service_name: Service name for traces
            phoenix_endpoint: Phoenix collector endpoint (e.g., "http://localhost:6006/v1/traces")
            console_export: Whether to export traces to console (for debugging)
        """
        self.enabled = enabled and OTEL_AVAILABLE
        self.service_name = service_name
        self.phoenix_endpoint = phoenix_endpoint or os.getenv("PHOENIX_COLLECTOR_ENDPOINT")
        self.console_export = console_export

        if self.enabled and not OTEL_AVAILABLE:
            print("Warning: OpenTelemetry not installed. Install with: pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp")


class Tracer:
    """Tracer for Custom Evals with Phoenix integration."""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize tracer."""
        if not self._initialized:
            self.config = TracingConfig()
            self.tracer = None
            self._initialized = True

    def initialize(self, config: Optional[TracingConfig] = None):
        """Initialize OpenTelemetry tracing.

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

        # Create tracer provider
        provider = TracerProvider(resource=resource)

        # Add exporters
        if self.config.phoenix_endpoint:
            # Export to Phoenix
            otlp_exporter = OTLPSpanExporter(
                endpoint=self.config.phoenix_endpoint,
                headers={}
            )
            provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
            print(f"✓ Phoenix tracing enabled: {self.config.phoenix_endpoint}")

        if self.config.console_export:
            # Export to console (debugging)
            console_exporter = ConsoleSpanExporter()
            provider.add_span_processor(BatchSpanProcessor(console_exporter))

        # Set global tracer provider
        trace.set_tracer_provider(provider)

        # Get tracer
        self.tracer = trace.get_tracer(__name__)

    def get_tracer(self):
        """Get the tracer instance."""
        if not self.config.enabled or not OTEL_AVAILABLE:
            return None

        if self.tracer is None:
            self.initialize()

        return self.tracer

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
    console_export: bool = False
):
    """Initialize tracing for Custom Evals.

    Args:
        enabled: Whether tracing is enabled
        service_name: Service name for traces
        phoenix_endpoint: Phoenix collector endpoint (e.g., "http://localhost:6006/v1/traces")
        console_export: Whether to export traces to console

    Example:
        >>> from custom.evals.tracing import initialize_tracing
        >>>
        >>> # Initialize with Phoenix
        >>> initialize_tracing(
        ...     phoenix_endpoint="http://localhost:6006/v1/traces"
        ... )
        >>>
        >>> # Now all evaluations will be traced
        >>> from custom.evals import HallucinationEvaluator
        >>> from custom.evals.llm import LLM
        >>>
        >>> llm = LLM(provider="openai", model="gpt-4o-mini")
        >>> evaluator = HallucinationEvaluator(llm)
        >>> score = evaluator.evaluate({...})  # Traced!
    """
    config = TracingConfig(
        enabled=enabled,
        service_name=service_name,
        phoenix_endpoint=phoenix_endpoint,
        console_export=console_export
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
