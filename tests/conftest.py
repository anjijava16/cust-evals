"""Pytest configuration and fixtures for Custom Evals tests."""

import pytest
from unittest.mock import Mock, MagicMock
from typing import Dict, Any


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = '{"verdict": "factual", "explanation": "The response is accurate."}'
    return mock_response


@pytest.fixture
def mock_anthropic_response():
    """Mock Anthropic API response."""
    mock_response = Mock()
    mock_response.content = [Mock()]
    mock_response.content[0].text = '{"verdict": "factual", "explanation": "The response is accurate."}'
    return mock_response


@pytest.fixture
def mock_llm_openai(mock_openai_response):
    """Mock LLM instance with OpenAI provider."""
    from custom.evals.llm import LLM

    llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")

    # Mock the client
    llm.client = Mock()
    llm.client.chat.completions.create = Mock(return_value=mock_openai_response)

    return llm


@pytest.fixture
def mock_llm_anthropic(mock_anthropic_response):
    """Mock LLM instance with Anthropic provider."""
    from custom.evals.llm import LLM

    llm = LLM(provider="anthropic", model="claude-3-haiku-20240307", api_key="test-key")

    # Mock the client
    llm.client = Mock()
    llm.client.messages.create = Mock(return_value=mock_anthropic_response)

    return llm


@pytest.fixture
def sample_eval_input():
    """Sample evaluation input for testing."""
    return {
        "input": "What is the capital of France?",
        "output": "Paris is the capital of France.",
        "context": "Paris is the capital and largest city of France.",
        "expected": "Paris"
    }


@pytest.fixture
def sample_eval_input_no_ground_truth():
    """Sample evaluation input without ground truth."""
    return {
        "input": "What is machine learning?",
        "output": "Machine learning is a subset of AI that enables systems to learn from data.",
        "context": "Machine learning is a branch of artificial intelligence."
    }


@pytest.fixture
def hallucination_eval_input():
    """Hallucination evaluation input."""
    return {
        "input": "What is the capital of France?",
        "output": "Paris is the capital of France with 20 million people.",
        "context": "Paris is the capital of France."
    }


@pytest.fixture
def faithfulness_eval_input():
    """Faithfulness evaluation input."""
    return {
        "input": "What is the capital of France?",
        "output": "Paris is the capital of France. It's located on the Seine River.",
        "context": "Paris is the capital and largest city of France, located on the Seine River."
    }


@pytest.fixture
def relevancy_eval_input():
    """Answer relevancy evaluation input."""
    return {
        "input": "What is machine learning?",
        "output": "Machine learning is a subset of AI that enables systems to learn from data."
    }


@pytest.fixture
def correctness_eval_input():
    """Correctness evaluation input with ground truth."""
    return {
        "input": "What is 2 + 2?",
        "output": "4",
        "expected": "4"
    }


@pytest.fixture
def coherence_eval_input():
    """Coherence evaluation input."""
    return {
        "input": "Explain quantum computing",
        "output": "Quantum computing uses quantum bits or qubits. Unlike classical bits, qubits can exist in superposition."
    }


@pytest.fixture
def relevance_eval_input():
    """Relevance evaluation input."""
    return {
        "input": "What is Python?",
        "context": "Python is a high-level programming language known for its simplicity."
    }


@pytest.fixture
def disable_tracing(monkeypatch):
    """Fixture to disable tracing during tests."""
    import sys
    from custom.evals import tracing

    # Mock tracing as unavailable
    monkeypatch.setattr(tracing, "OTEL_AVAILABLE", False)

    yield

    # Reset after test
    monkeypatch.undo()


@pytest.fixture
def enable_tracing(monkeypatch):
    """Fixture to enable tracing during tests."""
    try:
        import opentelemetry
        from custom.evals import tracing

        # Ensure tracing is available
        monkeypatch.setattr(tracing, "OTEL_AVAILABLE", True)

        yield

        # Reset after test
        monkeypatch.undo()
    except ImportError:
        pytest.skip("OpenTelemetry not available")


@pytest.fixture(autouse=True)
def reset_tracer():
    """Reset tracer singleton between tests."""
    from custom.evals.tracing import _tracer

    # Reset tracer state
    _tracer._initialized = False
    _tracer.tracer = None

    yield

    # Cleanup after test
    _tracer._initialized = False
    _tracer.tracer = None
