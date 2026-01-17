"""LLM wrappers and adapters for evaluation."""

from .prompts import PromptTemplate
from .wrapper import LLM

__all__ = [
    "LLM",
    "PromptTemplate",
]
