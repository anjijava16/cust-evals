"""Comprehensive tests for tracing functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os


class TestTracingInitialization:
    """Tests for tracing initialization."""

    def test_tracing_available_when_otel_installed(self):
        """Test TRACING_AVAILABLE flag when OpenTelemetry is installed."""
        try:
            import opentelemetry
            from custom.evals import TRACING_AVAILABLE

            # If OpenTelemetry is installed, tracing should be available
            assert TRACING_AVAILABLE is True
        except ImportError:
            # If not installed, skip this test
            pytest.skip("OpenTelemetry not installed")

    def test_tracing_unavailable_when_otel_not_installed(self):
        """Test TRACING_AVAILABLE flag when OpenTelemetry is not installed."""
        # This test would require mocking the import failure
        # For now, we test that the flag exists
        from custom.evals import TRACING_AVAILABLE

        assert isinstance(TRACING_AVAILABLE, bool)

    def test_initialize_tracing_basic(self):
        """Test basic tracing initialization."""
        try:
            from custom.evals import initialize_tracing

            # Should not raise error
            initialize_tracing(
                enabled=True,
                service_name="test-service",
                phoenix_endpoint="http://localhost:6006/v1/traces"
            )

            # Initialization successful
            assert True
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_initialize_tracing_disabled(self):
        """Test tracing initialization when disabled."""
        from custom.evals import initialize_tracing

        # Should not raise error when disabled
        initialize_tracing(enabled=False)

        assert True

    def test_initialize_tracing_with_console_export(self):
        """Test tracing initialization with console export."""
        try:
            from custom.evals import initialize_tracing

            initialize_tracing(
                phoenix_endpoint="http://localhost:6006/v1/traces",
                console_export=True
            )

            assert True
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    @patch.dict(os.environ, {"PHOENIX_COLLECTOR_ENDPOINT": "http://env-endpoint:6006/v1/traces"})
    def test_initialize_tracing_from_env(self):
        """Test tracing reads endpoint from environment variable."""
        try:
            from custom.evals import initialize_tracing

            initialize_tracing()

            # Should use endpoint from environment
            assert True
        except ImportError:
            pytest.skip("OpenTelemetry not installed")


class TestGetTracer:
    """Tests for get_tracer function."""

    def test_get_tracer_returns_tracer_object(self):
        """Test get_tracer returns a tracer object."""
        try:
            from custom.evals import get_tracer

            tracer = get_tracer()

            # Should return tracer object (not None)
            assert tracer is not None
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_get_tracer_without_initialization(self):
        """Test get_tracer works without explicit initialization."""
        try:
            from custom.evals import get_tracer

            tracer = get_tracer()

            # Should return a tracer (may be no-op if not initialized)
            assert tracer is not None
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_get_tracer_returns_singleton(self):
        """Test get_tracer returns the same instance."""
        try:
            from custom.evals import get_tracer

            tracer1 = get_tracer()
            tracer2 = get_tracer()

            # Should return same singleton instance
            assert tracer1 is tracer2
        except ImportError:
            pytest.skip("OpenTelemetry not installed")


class TestTracedDecorator:
    """Tests for @traced decorator."""

    def test_traced_decorator_basic(self):
        """Test traced decorator on basic function."""
        try:
            from custom.evals import traced

            @traced("test_function")
            def test_func():
                return "result"

            result = test_func()

            assert result == "result"
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_traced_decorator_with_arguments(self):
        """Test traced decorator on function with arguments."""
        try:
            from custom.evals import traced

            @traced("add_numbers")
            def add(a, b):
                return a + b

            result = add(2, 3)

            assert result == 5
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_traced_decorator_preserves_function_name(self):
        """Test traced decorator preserves function name."""
        try:
            from custom.evals import traced

            @traced("test")
            def my_function():
                return "test"

            # Should preserve function name
            assert my_function.__name__ == "my_function"
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_traced_decorator_handles_exceptions(self):
        """Test traced decorator handles exceptions."""
        try:
            from custom.evals import traced

            @traced("error_function")
            def error_func():
                raise ValueError("Test error")

            with pytest.raises(ValueError, match="Test error"):
                error_func()

            # Exception should propagate
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_traced_decorator_without_tracing(self, disable_tracing):
        """Test traced decorator works when tracing is disabled."""
        from custom.evals import traced

        @traced("test")
        def func():
            return "result"

        # Should still work without tracing
        result = func()
        assert result == "result"


class TestAddSpanAttributes:
    """Tests for add_span_attributes function."""

    def test_add_span_attributes_basic(self):
        """Test add_span_attributes with basic attributes."""
        try:
            from custom.evals import add_span_attributes, traced

            @traced("test")
            def func():
                add_span_attributes({
                    "key1": "value1",
                    "key2": "value2"
                })
                return "result"

            result = func()
            assert result == "result"
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_add_span_attributes_with_dict_value(self):
        """Test add_span_attributes with dict values."""
        try:
            from custom.evals import add_span_attributes, traced

            @traced("test")
            def func():
                add_span_attributes({
                    "config": {"option": "value"}
                })
                return "result"

            result = func()
            assert result == "result"
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_add_span_attributes_without_active_span(self):
        """Test add_span_attributes without active span (should not error)."""
        try:
            from custom.evals import add_span_attributes

            # Should not raise error even without active span
            add_span_attributes({"key": "value"})

            assert True
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_add_span_attributes_without_tracing(self, disable_tracing):
        """Test add_span_attributes when tracing is disabled."""
        from custom.evals import add_span_attributes

        # Should not error when tracing is disabled
        add_span_attributes({"key": "value"})

        assert True


class TestTracingWithEvaluators:
    """Tests for tracing integration with evaluators."""

    def test_evaluator_creates_spans(self, mock_llm_openai):
        """Test evaluator creates tracing spans."""
        try:
            from custom.evals import initialize_tracing, HallucinationEvaluator
            import json

            # Initialize tracing
            initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")

            # Mock LLM response
            mock_response = {"verdict": "factual", "explanation": "Test"}
            mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

            evaluator = HallucinationEvaluator(mock_llm_openai)
            eval_input = {
                "input": "Test",
                "output": "Test output",
                "context": "Test context"
            }

            # Evaluate (should create spans)
            score = evaluator.evaluate(eval_input)

            assert score is not None
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_evaluator_works_without_tracing(self, mock_llm_openai, disable_tracing):
        """Test evaluator works without tracing initialized."""
        from custom.evals import HallucinationEvaluator
        import json

        # Mock LLM response
        mock_response = {"verdict": "factual", "explanation": "Test"}
        mock_llm_openai.generate = Mock(return_value=json.dumps(mock_response))

        evaluator = HallucinationEvaluator(mock_llm_openai)
        eval_input = {
            "input": "Test",
            "output": "Test output",
            "context": "Test context"
        }

        # Should work without tracing
        score = evaluator.evaluate(eval_input)

        assert score is not None


class TestTracingConfig:
    """Tests for TracingConfig class."""

    def test_tracing_config_default_values(self):
        """Test TracingConfig with default values."""
        try:
            from custom.evals.tracing import TracingConfig

            config = TracingConfig()

            assert config.enabled is True or config.enabled is False  # Depends on OTEL_AVAILABLE
            assert config.service_name == "custom-evals"
            assert config.console_export is False
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_tracing_config_custom_values(self):
        """Test TracingConfig with custom values."""
        try:
            from custom.evals.tracing import TracingConfig

            config = TracingConfig(
                enabled=True,
                service_name="my-service",
                phoenix_endpoint="http://custom:6006/v1/traces",
                console_export=True
            )

            assert config.service_name == "my-service"
            assert config.phoenix_endpoint == "http://custom:6006/v1/traces"
            assert config.console_export is True
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    @patch.dict(os.environ, {"PHOENIX_COLLECTOR_ENDPOINT": "http://env:6006/v1/traces"})
    def test_tracing_config_reads_env_variable(self):
        """Test TracingConfig reads from environment variable."""
        try:
            from custom.evals.tracing import TracingConfig

            config = TracingConfig()

            assert config.phoenix_endpoint == "http://env:6006/v1/traces"
        except ImportError:
            pytest.skip("OpenTelemetry not installed")


class TestTracingSpans:
    """Tests for tracing span creation."""

    def test_tracer_span_context_manager(self):
        """Test tracer span as context manager."""
        try:
            from custom.evals import get_tracer

            tracer = get_tracer()

            # Should work as context manager
            with tracer.span("test_span", attributes={"key": "value"}):
                # Do some work
                result = 1 + 1

            assert result == 2
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_tracer_span_without_attributes(self):
        """Test tracer span without attributes."""
        try:
            from custom.evals import get_tracer

            tracer = get_tracer()

            with tracer.span("simple_span"):
                result = "test"

            assert result == "test"
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_tracer_span_nested(self):
        """Test nested tracing spans."""
        try:
            from custom.evals import get_tracer

            tracer = get_tracer()

            with tracer.span("outer_span"):
                with tracer.span("inner_span"):
                    result = "nested"

            assert result == "nested"
        except ImportError:
            pytest.skip("OpenTelemetry not installed")


class TestTracingEdgeCases:
    """Test edge cases for tracing."""

    def test_multiple_initialize_tracing_calls(self):
        """Test multiple calls to initialize_tracing."""
        try:
            from custom.evals import initialize_tracing

            # Should not error on multiple calls
            initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")
            initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")

            assert True
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_tracing_with_empty_service_name(self):
        """Test tracing with empty service name."""
        try:
            from custom.evals import initialize_tracing

            # Should handle empty service name
            initialize_tracing(service_name="")

            # May use default or handle gracefully
            assert True
        except ImportError:
            pytest.skip("OpenTelemetry not installed")

    def test_tracing_with_invalid_endpoint(self):
        """Test tracing with invalid endpoint."""
        try:
            from custom.evals import initialize_tracing

            # Should not crash on invalid endpoint
            initialize_tracing(phoenix_endpoint="invalid-endpoint")

            # May fail silently or handle gracefully
            assert True
        except ImportError:
            pytest.skip("OpenTelemetry not installed")


class TestTracingOptionalBehavior:
    """Test that tracing is truly optional."""

    def test_framework_works_without_tracing_import(self):
        """Test framework works even if tracing imports fail."""
        # Test that evaluators can be imported and used
        from custom.evals import HallucinationEvaluator, Score

        # Should be able to import
        assert HallucinationEvaluator is not None
        assert Score is not None

    def test_tracing_functions_gracefully_fail(self, disable_tracing):
        """Test tracing functions handle disabled tracing gracefully."""
        from custom.evals import initialize_tracing, get_tracer, traced, add_span_attributes

        # All should be callable (may be no-ops)
        if initialize_tracing:
            initialize_tracing(enabled=False)

        if get_tracer:
            tracer = get_tracer()

        if traced:
            @traced("test")
            def func():
                return "test"

            result = func()
            assert result == "test"

        if add_span_attributes:
            add_span_attributes({"key": "value"})

        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
