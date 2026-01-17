"""Simple prompt template system."""

from typing import Any, Dict, List, Union


class PromptTemplate:
    """Simple template for rendering prompts with variable substitution.

    Uses Python string formatting with {variable} syntax.

    Example:
        >>> template = PromptTemplate(
        ...     template="Evaluate: {input}\nExpected: {expected}"
        ... )
        >>> prompt = template.render({"input": "2+2", "expected": "4"})
        >>> print(prompt)
        Evaluate: 2+2
        Expected: 4
    """

    def __init__(self, template: Union[str, List[Dict[str, Any]]]):
        """Initialize prompt template.

        Args:
            template: Either a string template or list of message dicts
                     with 'role' and 'content' fields (OpenAI format)
        """
        self.template = template
        self._is_messages = isinstance(template, list)

    def render(self, variables: Dict[str, Any]) -> Union[str, List[Dict[str, Any]]]:
        """Render template with variables.

        Args:
            variables: Dictionary of variables to substitute

        Returns:
            Rendered template (string or message list)
        """
        if self._is_messages:
            # Render message list
            rendered = []
            for msg in self.template:  # type: ignore
                rendered_msg = {
                    "role": msg["role"],
                    "content": msg["content"].format(**variables)
                }
                rendered.append(rendered_msg)
            return rendered
        else:
            # Render string template
            return self.template.format(**variables)  # type: ignore
