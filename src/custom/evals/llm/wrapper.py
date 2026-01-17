"""LLM wrapper for various providers."""

import json
from typing import Any, Dict, List, Literal, Optional, Union


class LLM:
    """Simplified LLM wrapper supporting OpenAI and Anthropic.

    This is a POC implementation. In production, you'd want:
    - Async support
    - Rate limiting
    - Better error handling
    - More providers

    Example:
        >>> llm = LLM(provider="openai", model="gpt-4o-mini")
        >>> response = llm.generate_text("Hello, world!")
        >>> print(response)
        'Hello! How can I help you today?'
    """

    def __init__(
        self,
        provider: Literal["openai", "anthropic"],
        model: str,
        api_key: Optional[str] = None,
        **kwargs: Any,
    ):
        """Initialize LLM wrapper.

        Args:
            provider: Provider name ('openai' or 'anthropic')
            model: Model name
            api_key: Optional API key (defaults to environment variable)
            **kwargs: Additional provider-specific arguments
        """
        self.provider = provider
        self.model = model
        self._kwargs = kwargs

        # Initialize the appropriate client
        if provider == "openai":
            try:
                import openai
                self.client = openai.OpenAI(api_key=api_key, **kwargs)
            except ImportError:
                raise ImportError(
                    "OpenAI SDK not installed. Install with: pip install openai"
                )
        elif provider == "anthropic":
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=api_key, **kwargs)
            except ImportError:
                raise ImportError(
                    "Anthropic SDK not installed. Install with: pip install anthropic"
                )
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def generate_text(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        **kwargs: Any,
    ) -> str:
        """Generate text from prompt.

        Args:
            prompt: String prompt or list of message dicts
            **kwargs: Additional generation parameters

        Returns:
            Generated text
        """
        if self.provider == "openai":
            return self._openai_generate_text(prompt, **kwargs)
        elif self.provider == "anthropic":
            return self._anthropic_generate_text(prompt, **kwargs)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def generate_object(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        schema: Dict[str, Any],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate structured object from prompt.

        Args:
            prompt: String prompt or list of message dicts
            schema: JSON schema for the output
            **kwargs: Additional generation parameters

        Returns:
            Generated object matching schema
        """
        if self.provider == "openai":
            return self._openai_generate_object(prompt, schema, **kwargs)
        elif self.provider == "anthropic":
            return self._anthropic_generate_object(prompt, schema, **kwargs)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _openai_generate_text(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        **kwargs: Any,
    ) -> str:
        """Generate text using OpenAI."""
        messages = self._normalize_messages(prompt)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore
            **kwargs,
        )

        return response.choices[0].message.content or ""

    def _openai_generate_object(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        schema: Dict[str, Any],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate structured object using OpenAI."""
        messages = self._normalize_messages(prompt)

        # Use structured outputs (response_format) if available
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "response",
                    "schema": schema,
                    "strict": True,
                },
            },
            **kwargs,
        )

        content = response.choices[0].message.content or "{}"
        return json.loads(content)

    def _anthropic_generate_text(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        **kwargs: Any,
    ) -> str:
        """Generate text using Anthropic."""
        messages = self._normalize_messages(prompt)

        # Extract system message if present
        system = None
        if messages and messages[0]["role"] == "system":
            system = messages[0]["content"]
            messages = messages[1:]

        response = self.client.messages.create(
            model=self.model,
            messages=messages,  # type: ignore
            system=system,
            max_tokens=kwargs.pop("max_tokens", 1024),
            **kwargs,
        )

        return response.content[0].text

    def _anthropic_generate_object(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        schema: Dict[str, Any],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate structured object using Anthropic."""
        messages = self._normalize_messages(prompt)

        # Extract system message if present
        system = None
        if messages and messages[0]["role"] == "system":
            system = messages[0]["content"]
            messages = messages[1:]

        # Add schema to system message or append instruction
        schema_instruction = f"\n\nRespond with valid JSON matching this schema:\n{json.dumps(schema, indent=2)}"
        if system:
            system += schema_instruction
        else:
            system = f"You are a helpful assistant.{schema_instruction}"

        response = self.client.messages.create(
            model=self.model,
            messages=messages,  # type: ignore
            system=system,
            max_tokens=kwargs.pop("max_tokens", 1024),
            **kwargs,
        )

        content = response.content[0].text
        # Extract JSON from response (might be wrapped in markdown code blocks)
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        return json.loads(content)

    def _normalize_messages(
        self, prompt: Union[str, List[Dict[str, str]]]
    ) -> List[Dict[str, str]]:
        """Normalize prompt to message format.

        Args:
            prompt: String or message list

        Returns:
            List of message dicts
        """
        if isinstance(prompt, str):
            return [{"role": "user", "content": prompt}]
        return prompt
