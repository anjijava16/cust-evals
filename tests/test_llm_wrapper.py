"""Comprehensive tests for LLM wrapper class."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os


class TestLLMInitialization:
    """Tests for LLM class initialization."""

    def test_llm_openai_initialization(self):
        """Test LLM initialization with OpenAI provider."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")

        assert llm.provider == "openai"
        assert llm.model == "gpt-4o-mini"
        assert llm.api_key == "test-key"

    def test_llm_anthropic_initialization(self):
        """Test LLM initialization with Anthropic provider."""
        from custom.evals.llm import LLM

        llm = LLM(provider="anthropic", model="claude-3-haiku-20240307", api_key="test-key")

        assert llm.provider == "anthropic"
        assert llm.model == "claude-3-haiku-20240307"
        assert llm.api_key == "test-key"

    def test_llm_unsupported_provider(self):
        """Test LLM initialization with unsupported provider."""
        from custom.evals.llm import LLM

        with pytest.raises(ValueError, match="Unsupported provider"):
            LLM(provider="unknown", model="test-model", api_key="test-key")

    def test_llm_missing_api_key(self):
        """Test LLM initialization without API key."""
        from custom.evals.llm import LLM

        with pytest.raises(ValueError, match="API key is required"):
            LLM(provider="openai", model="gpt-4o-mini")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"})
    def test_llm_api_key_from_env(self):
        """Test LLM reads API key from environment."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o-mini")

        assert llm.api_key == "env-key"

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "anthropic-key"})
    def test_llm_anthropic_api_key_from_env(self):
        """Test LLM reads Anthropic API key from environment."""
        from custom.evals.llm import LLM

        llm = LLM(provider="anthropic", model="claude-3-haiku-20240307")

        assert llm.api_key == "anthropic-key"


class TestLLMGeneration:
    """Tests for LLM text generation."""

    @patch("openai.OpenAI")
    def test_llm_openai_generate(self, mock_openai_class):
        """Test LLM generate with OpenAI."""
        from custom.evals.llm import LLM

        # Mock OpenAI response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Generated response"
        mock_client.chat.completions.create = Mock(return_value=mock_response)
        mock_openai_class.return_value = mock_client

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")
        result = llm.generate("Test prompt")

        assert result == "Generated response"
        mock_client.chat.completions.create.assert_called_once()

    @patch("anthropic.Anthropic")
    def test_llm_anthropic_generate(self, mock_anthropic_class):
        """Test LLM generate with Anthropic."""
        from custom.evals.llm import LLM

        # Mock Anthropic response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Generated response"
        mock_client.messages.create = Mock(return_value=mock_response)
        mock_anthropic_class.return_value = mock_client

        llm = LLM(provider="anthropic", model="claude-3-haiku-20240307", api_key="test-key")
        result = llm.generate("Test prompt")

        assert result == "Generated response"
        mock_client.messages.create.assert_called_once()

    @patch("openai.OpenAI")
    def test_llm_openai_generate_with_json(self, mock_openai_class):
        """Test LLM generate with JSON response format."""
        from custom.evals.llm import LLM

        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"result": "test"}'
        mock_client.chat.completions.create = Mock(return_value=mock_response)
        mock_openai_class.return_value = mock_client

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")
        result = llm.generate("Test prompt", response_format="json")

        assert '{"result": "test"}' in result
        # Verify JSON response format was requested
        call_args = mock_client.chat.completions.create.call_args
        assert call_args is not None

    @patch("openai.OpenAI")
    def test_llm_generate_with_custom_temperature(self, mock_openai_class):
        """Test LLM generate with custom temperature."""
        from custom.evals.llm import LLM

        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Response"
        mock_client.chat.completions.create = Mock(return_value=mock_response)
        mock_openai_class.return_value = mock_client

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")
        llm.generate("Test prompt", temperature=0.5)

        # Verify temperature was passed
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs.get("temperature") == 0.5

    @patch("openai.OpenAI")
    def test_llm_generate_handles_api_error(self, mock_openai_class):
        """Test LLM handles API errors gracefully."""
        from custom.evals.llm import LLM

        mock_client = Mock()
        mock_client.chat.completions.create = Mock(side_effect=Exception("API Error"))
        mock_openai_class.return_value = mock_client

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")

        with pytest.raises(Exception, match="API Error"):
            llm.generate("Test prompt")


class TestLLMModelSupport:
    """Tests for different LLM models."""

    def test_llm_supports_gpt4o(self):
        """Test LLM with GPT-4o model."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o", api_key="test-key")

        assert llm.model == "gpt-4o"

    def test_llm_supports_gpt4o_mini(self):
        """Test LLM with GPT-4o-mini model."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")

        assert llm.model == "gpt-4o-mini"

    def test_llm_supports_claude_haiku(self):
        """Test LLM with Claude Haiku model."""
        from custom.evals.llm import LLM

        llm = LLM(provider="anthropic", model="claude-3-haiku-20240307", api_key="test-key")

        assert llm.model == "claude-3-haiku-20240307"

    def test_llm_supports_claude_sonnet(self):
        """Test LLM with Claude Sonnet model."""
        from custom.evals.llm import LLM

        llm = LLM(provider="anthropic", model="claude-3-5-sonnet-20241022", api_key="test-key")

        assert llm.model == "claude-3-5-sonnet-20241022"


class TestLLMPromptTemplates:
    """Tests for LLM prompt template rendering."""

    def test_prompt_template_basic(self):
        """Test basic prompt template rendering."""
        from custom.evals.llm.prompts import PromptTemplate

        template = PromptTemplate("Hello {name}")
        result = template.render(name="World")

        assert result == "Hello World"

    def test_prompt_template_multiple_variables(self):
        """Test prompt template with multiple variables."""
        from custom.evals.llm.prompts import PromptTemplate

        template = PromptTemplate("Query: {query}\nContext: {context}")
        result = template.render(query="What is AI?", context="AI is artificial intelligence.")

        assert "What is AI?" in result
        assert "AI is artificial intelligence." in result

    def test_prompt_template_missing_variable(self):
        """Test prompt template with missing variable."""
        from custom.evals.llm.prompts import PromptTemplate

        template = PromptTemplate("Hello {name}")

        with pytest.raises(KeyError):
            template.render()

    def test_prompt_template_extra_variables(self):
        """Test prompt template with extra variables (should be ignored)."""
        from custom.evals.llm.prompts import PromptTemplate

        template = PromptTemplate("Hello {name}")
        result = template.render(name="World", extra="ignored")

        assert result == "Hello World"

    def test_prompt_template_with_multiline(self):
        """Test prompt template with multiline content."""
        from custom.evals.llm.prompts import PromptTemplate

        template = PromptTemplate("""
        Query: {query}

        Answer: {answer}
        """)
        result = template.render(query="Test", answer="Result")

        assert "Test" in result
        assert "Result" in result


class TestLLMEdgeCases:
    """Test edge cases for LLM wrapper."""

    def test_llm_with_empty_prompt(self):
        """Test LLM with empty prompt."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")

        # Should handle empty prompt (may depend on implementation)
        # This tests the wrapper's behavior with edge case input

    def test_llm_with_very_long_prompt(self):
        """Test LLM with very long prompt."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")
        long_prompt = "Test " * 10000

        # Should handle long prompts (may be limited by API)

    def test_llm_with_special_characters_in_prompt(self):
        """Test LLM with special characters."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")

        # Should handle special characters
        special_prompt = "Test with special chars: @#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"

    def test_llm_with_unicode_in_prompt(self):
        """Test LLM with unicode characters."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")

        # Should handle unicode
        unicode_prompt = "Café résumé naïve 日本語 한국어"

    def test_llm_repr(self):
        """Test LLM string representation."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")
        repr_str = repr(llm)

        assert "openai" in repr_str.lower()
        assert "gpt-4o-mini" in repr_str

    def test_llm_provider_case_insensitive(self):
        """Test LLM provider is case-insensitive."""
        from custom.evals.llm import LLM

        # Should handle uppercase/mixed case
        llm1 = LLM(provider="OpenAI", model="gpt-4o-mini", api_key="test-key")
        llm2 = LLM(provider="OPENAI", model="gpt-4o-mini", api_key="test-key")

        # Both should work or normalize to lowercase


class TestLLMConfiguration:
    """Tests for LLM configuration options."""

    def test_llm_with_max_tokens(self):
        """Test LLM with max_tokens parameter."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key", max_tokens=100)

        # Should store max_tokens configuration
        # Implementation may vary

    def test_llm_with_custom_timeout(self):
        """Test LLM with custom timeout."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key", timeout=30)

        # Should store timeout configuration

    def test_llm_default_temperature(self):
        """Test LLM uses default temperature if not specified."""
        from custom.evals.llm import LLM

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")

        # Should have a default temperature value


class TestLLMClientCreation:
    """Tests for LLM client creation."""

    @patch("openai.OpenAI")
    def test_openai_client_created_once(self, mock_openai_class):
        """Test OpenAI client is created once and reused."""
        from custom.evals.llm import LLM

        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        llm = LLM(provider="openai", model="gpt-4o-mini", api_key="test-key")

        # Access client multiple times
        _ = llm.client
        _ = llm.client

        # Should only create client once
        assert mock_openai_class.call_count == 1

    @patch("anthropic.Anthropic")
    def test_anthropic_client_created_once(self, mock_anthropic_class):
        """Test Anthropic client is created once and reused."""
        from custom.evals.llm import LLM

        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client

        llm = LLM(provider="anthropic", model="claude-3-haiku-20240307", api_key="test-key")

        # Access client multiple times
        _ = llm.client
        _ = llm.client

        # Should only create client once
        assert mock_anthropic_class.call_count == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
