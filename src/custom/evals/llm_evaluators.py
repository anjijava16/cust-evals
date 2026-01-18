"""LLM-based evaluators for classification tasks."""

import asyncio
import time
from typing import Any, Dict, List, Optional

from .evaluators import Score
from .llm import LLM, PromptTemplate
from .tracing import get_tracer, add_span_attributes, record_evaluation_metrics


class LLMEvaluator:
    """Base class for LLM-based evaluators.

    Provides both synchronous and asynchronous evaluation methods,
    along with utility methods for introspection and description.

    This class follows Phoenix Evals' architecture with evaluate/_evaluate patterns.
    """

    NAME = "llm_evaluator"
    PROMPT_TEMPLATE: str = ""
    PROMPT_TEMPLATE_NO_GROUND_TRUTH: Optional[str] = None  # For reference-free evaluation
    CHOICES: Dict[str, float] = {}
    DIRECTION = "maximize"
    REQUIRES_GROUND_TRUTH = False  # Whether ground truth is required

    def __init__(self, llm: LLM):
        """Initialize LLM evaluator.

        Args:
            llm: LLM instance to use for evaluation
        """
        self.llm = llm
        self.name = self.NAME
        self.kind = "llm"
        self.direction = self.DIRECTION

    # Public API Methods

    def evaluate(self, eval_input: Dict[str, Any]) -> Score:
        """Main evaluation method (synchronous).

        This is the primary public API. It validates input and calls _evaluate.

        Args:
            eval_input: Dictionary with evaluation inputs

        Returns:
            Score with LLM judgment
        """
        return self._evaluate(eval_input)

    async def async_evaluate(self, eval_input: Dict[str, Any]) -> Score:
        """Main evaluation method (asynchronous).

        This is the async variant of evaluate().

        Args:
            eval_input: Dictionary with evaluation inputs

        Returns:
            Score with LLM judgment
        """
        return await self._async_evaluate(eval_input)

    def describe(self) -> Dict[str, Any]:
        """Return a description of this evaluator.

        Returns:
            Dictionary with evaluator metadata including name, kind, direction,
            required fields, and whether ground truth is required.

        Example:
            >>> evaluator.describe()
            {
                'name': 'hallucination',
                'kind': 'llm',
                'direction': 'minimize',
                'requires_ground_truth': False,
                'choices': {'factual': 0.0, 'hallucinated': 1.0},
                'model': 'gpt-4o-mini'
            }
        """
        return {
            "name": self.name,
            "kind": self.kind,
            "direction": self.direction,
            "requires_ground_truth": self.REQUIRES_GROUND_TRUTH,
            "choices": self.CHOICES,
            "model": self.llm.model,
            "provider": self.llm.provider,
        }

    # Internal Implementation Methods

    def _evaluate(self, eval_input: Dict[str, Any]) -> Score:
        """Internal evaluation logic (synchronous).

        Subclasses can override this for custom behavior, but the default
        implementation should work for most cases.

        Args:
            eval_input: Dictionary with evaluation inputs

        Returns:
            Score with LLM judgment
        """
        # Start timing for metrics
        start_time = time.time()

        # Create tracing span
        tracer = get_tracer()
        with tracer.span(f"evaluate.{self.name}", attributes={
            "evaluator.name": self.name,
            "evaluator.kind": "llm",
            "evaluator.direction": self.DIRECTION,
            "llm.model": self.llm.model,
            "llm.provider": self.llm.provider,
        }):
            # Check if ground truth is available
            has_ground_truth = self._check_ground_truth(eval_input)
            add_span_attributes({"has_ground_truth": has_ground_truth})

            # If ground truth is required but not available, return error score
            if self.REQUIRES_GROUND_TRUTH and not has_ground_truth:
                add_span_attributes({"result": "no_ground_truth"})
                latency = time.time() - start_time
                score_result = Score(
                    score=0.0,
                    name=self.name,
                    label="no_ground_truth",
                    explanation=f"{self.NAME} requires ground truth data (expected value)",
                    kind="llm",
                    direction=self.DIRECTION,  # type: ignore
                    metadata={"model": self.llm.model, "has_ground_truth": False}
                )
                # Record metrics for error case
                record_evaluation_metrics(
                    evaluator_name=self.name,
                    score=0.0,
                    label="no_ground_truth",
                    latency_seconds=latency,
                    model=self.llm.model,
                    provider=self.llm.provider
                )
                return score_result

            # Select appropriate prompt template
            if has_ground_truth or not self.PROMPT_TEMPLATE_NO_GROUND_TRUTH:
                prompt_template = self.PROMPT_TEMPLATE
            else:
                prompt_template = self.PROMPT_TEMPLATE_NO_GROUND_TRUTH

            # Render prompt with input variables
            try:
                prompt = prompt_template.format(**eval_input)
            except KeyError as e:
                add_span_attributes({"result": "error", "error": str(e)})
                latency = time.time() - start_time
                score_result = Score(
                    score=0.0,
                    name=self.name,
                    label="error",
                    explanation=f"Missing required input field: {e}",
                    kind="llm",
                    direction=self.DIRECTION,  # type: ignore
                    metadata={"model": self.llm.model, "error": str(e)}
                )
                # Record metrics for error case
                record_evaluation_metrics(
                    evaluator_name=self.name,
                    score=0.0,
                    label="error",
                    latency_seconds=latency,
                    model=self.llm.model,
                    provider=self.llm.provider
                )
                return score_result

            # Create schema for structured output
            schema = self._create_output_schema()

            # Get LLM response
            response = self.llm.generate_object(prompt, schema)

            # Extract label and explanation
            label = response.get("label", "")
            explanation = response.get("explanation", "")
            score_value = self.CHOICES.get(label, 0.0)

            # Calculate latency
            latency = time.time() - start_time

            # Add result to span
            add_span_attributes({
                "result.label": label,
                "result.score": score_value,
                "latency.seconds": latency,
            })

            # Record metrics
            record_evaluation_metrics(
                evaluator_name=self.name,
                score=score_value,
                label=label,
                latency_seconds=latency,
                model=self.llm.model,
                provider=self.llm.provider
            )

            return Score(
                score=score_value,
                name=self.name,
                label=label,
                explanation=explanation,
                kind="llm",
                direction=self.DIRECTION,  # type: ignore
                metadata={"model": self.llm.model, "has_ground_truth": has_ground_truth}
            )

    async def _async_evaluate(self, eval_input: Dict[str, Any]) -> Score:
        """Internal async evaluation logic.

        By default, runs the sync _evaluate in a thread pool.
        Subclasses can override for true async implementation.

        Args:
            eval_input: Dictionary with evaluation inputs

        Returns:
            Score with LLM judgment
        """
        # Run sync evaluation in thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._evaluate, eval_input)

    # Helper Methods

    def _check_ground_truth(self, eval_input: Dict[str, Any]) -> bool:
        """Check if ground truth data is available.

        Override this method in subclasses if different ground truth fields are used.

        Args:
            eval_input: Evaluation input dictionary

        Returns:
            True if ground truth is available, False otherwise
        """
        # Common ground truth field names
        ground_truth_fields = ["expected", "reference", "ground_truth", "target", "label"]
        return any(field in eval_input and eval_input[field] is not None
                   for field in ground_truth_fields)

    def _create_output_schema(self) -> Dict[str, Any]:
        """Create JSON schema for structured LLM output.

        Returns:
            JSON schema dict
        """
        return {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "enum": list(self.CHOICES.keys()),
                    "description": "The classification label"
                },
                "explanation": {
                    "type": "string",
                    "description": "Brief explanation of the reasoning"
                }
            },
            "required": ["label", "explanation"],
            "additionalProperties": False
        }

    def __repr__(self) -> str:
        """Return string representation of evaluator."""
        return f"{self.__class__.__name__}(name='{self.name}', model='{self.llm.model}')"


class HallucinationEvaluator(LLMEvaluator):
    """Evaluator for detecting hallucinations in LLM responses.

    This evaluator does NOT require ground truth - it evaluates whether
    the output is factual based on the provided context.

    Example:
        >>> from custom.evals import HallucinationEvaluator
        >>> from custom.evals.llm import LLM
        >>>
        >>> llm = LLM(provider="openai", model="gpt-4o-mini")
        >>> evaluator = HallucinationEvaluator(llm)
        >>>
        >>> # Describe the evaluator
        >>> print(evaluator.describe())
        >>>
        >>> # Synchronous evaluation
        >>> eval_input = {
        ...     "input": "What is the capital of France?",
        ...     "output": "Paris is the capital of France.",
        ...     "context": "Paris is the capital and largest city of France."
        ... }
        >>> score = evaluator.evaluate(eval_input)
        >>> print(f"Score: {score.score}, Label: {score.label}")
        >>>
        >>> # Async evaluation
        >>> score = await evaluator.async_evaluate(eval_input)
    """

    NAME = "hallucination"
    DIRECTION = "minimize"  # Lower is better (0 = factual, 1 = hallucinated)
    REQUIRES_GROUND_TRUTH = False  # Does NOT require ground truth
    CHOICES = {
        "factual": 0.0,
        "hallucinated": 1.0,
    }
    PROMPT_TEMPLATE = """You are an expert evaluator. Your task is to determine if a response contains hallucinations.

A 'hallucination' is a response that is not based on the provided context or assumes information not available in the context.

<query>
{input}
</query>

<context>
{context}
</context>

<response>
{output}
</response>

Analyze the response carefully. Is it factual based on the context, or does it contain hallucinated information?

Respond with:
- label: "factual" if the response is accurate based on the context
- label: "hallucinated" if the response contains false or unsupported information
- explanation: Brief reasoning for your judgment"""

    def _check_ground_truth(self, eval_input: Dict[str, Any]) -> bool:
        """Hallucination evaluator doesn't use ground truth."""
        return False  # Always reference-free


class CorrectnessEvaluator(LLMEvaluator):
    """Evaluator for assessing correctness of responses.

    This evaluator REQUIRES ground truth (expected answer) to compare against.

    Example:
        >>> from custom.evals import CorrectnessEvaluator
        >>> from custom.evals.llm import LLM
        >>>
        >>> llm = LLM(provider="openai", model="gpt-4o-mini")
        >>> evaluator = CorrectnessEvaluator(llm)
        >>>
        >>> # With ground truth
        >>> eval_input = {
        ...     "input": "What is 2+2?",
        ...     "output": "4",
        ...     "expected": "4"
        ... }
        >>> score = evaluator.evaluate(eval_input)
        >>> print(f"Score: {score.score}, Label: {score.label}")
    """

    NAME = "correctness"
    DIRECTION = "maximize"  # Higher is better (1 = correct, 0 = incorrect)
    REQUIRES_GROUND_TRUTH = True  # REQUIRES ground truth
    CHOICES = {
        "correct": 1.0,
        "incorrect": 0.0,
    }
    PROMPT_TEMPLATE = """You are an expert evaluator. Your task is to assess if the output correctly answers the input question.

<input>
{input}
</input>

<output>
{output}
</output>

<expected_answer>
{expected}
</expected_answer>

Compare the output with the expected answer. Does the output correctly answer the question?

Respond with:
- label: "correct" if the output matches or is equivalent to the expected answer
- label: "incorrect" if the output is wrong or doesn't match
- explanation: Brief reasoning for your judgment"""


class RelevanceEvaluator(LLMEvaluator):
    """Evaluator for assessing relevance of retrieved documents.

    This evaluator does NOT require ground truth - it evaluates whether
    the context is relevant to the input question.

    Example:
        >>> from custom.evals import RelevanceEvaluator
        >>> from custom.evals.llm import LLM
        >>>
        >>> llm = LLM(provider="openai", model="gpt-4o-mini")
        >>> evaluator = RelevanceEvaluator(llm)
        >>>
        >>> eval_input = {
        ...     "input": "What is the capital of France?",
        ...     "context": "Paris is the capital and largest city of France."
        ... }
        >>> score = evaluator.evaluate(eval_input)
    """

    NAME = "relevance"
    DIRECTION = "maximize"  # Higher is better (1 = relevant, 0 = irrelevant)
    REQUIRES_GROUND_TRUTH = False  # Does NOT require ground truth
    CHOICES = {
        "relevant": 1.0,
        "irrelevant": 0.0,
    }
    PROMPT_TEMPLATE = """You are an expert evaluator. Your task is to assess if the context is relevant to the question.

<question>
{input}
</question>

<context>
{context}
</context>

Does the context contain information that helps answer the question?

Respond with:
- label: "relevant" if the context is useful for answering the question
- label: "irrelevant" if the context doesn't help answer the question
- explanation: Brief reasoning for your judgment"""

    def _check_ground_truth(self, eval_input: Dict[str, Any]) -> bool:
        """Relevance evaluator doesn't use ground truth."""
        return False  # Always reference-free


class CoherenceEvaluator(LLMEvaluator):
    """Evaluator for assessing coherence and consistency of text.

    This evaluator does NOT require ground truth - it evaluates the
    internal coherence and logical flow of the output.

    Example:
        >>> from custom.evals import CoherenceEvaluator
        >>> from custom.evals.llm import LLM
        >>>
        >>> llm = LLM(provider="openai", model="gpt-4o-mini")
        >>> evaluator = CoherenceEvaluator(llm)
        >>>
        >>> eval_input = {
        ...     "output": "Paris is the capital of France. It is known for the Eiffel Tower."
        ... }
        >>> score = evaluator.evaluate(eval_input)
    """

    NAME = "coherence"
    DIRECTION = "maximize"  # Higher is better (1 = coherent, 0 = incoherent)
    REQUIRES_GROUND_TRUTH = False  # Does NOT require ground truth
    CHOICES = {
        "coherent": 1.0,
        "incoherent": 0.0,
    }
    PROMPT_TEMPLATE = """You are an expert evaluator. Your task is to assess if the text is coherent and logically consistent.

<text>
{output}
</text>

Evaluate whether the text:
1. Has logical flow and structure
2. Is internally consistent
3. Makes sense and is easy to understand

Respond with:
- label: "coherent" if the text is well-structured and logical
- label: "incoherent" if the text is confusing, contradictory, or poorly structured
- explanation: Brief reasoning for your judgment"""

    def _check_ground_truth(self, eval_input: Dict[str, Any]) -> bool:
        """Coherence evaluator doesn't use ground truth."""
        return False  # Always reference-free


class FaithfulnessEvaluator(LLMEvaluator):
    """Evaluator for assessing faithfulness of responses to retrieval context.

    This evaluator checks whether the generated response is grounded in the
    provided retrieval context and doesn't contain hallucinations. It's
    specifically designed for RAG (Retrieval-Augmented Generation) systems.

    This is similar to HallucinationEvaluator but focuses on statement-level
    verification for RAG applications.

    Example:
        >>> from custom.evals import FaithfulnessEvaluator
        >>> from custom.evals.llm import LLM
        >>>
        >>> llm = LLM(provider="openai", model="gpt-4o-mini")
        >>> evaluator = FaithfulnessEvaluator(llm)
        >>>
        >>> eval_input = {
        ...     "input": "What is the capital of France?",
        ...     "output": "Paris is the capital of France. It's located on the Seine River.",
        ...     "context": "Paris is the capital and largest city of France, located on the Seine River."
        ... }
        >>> score = evaluator.evaluate(eval_input)
        >>> print(f"Faithfulness: {score.label} ({score.score})")
    """

    NAME = "faithfulness"
    DIRECTION = "maximize"  # Higher is better (1 = faithful, 0 = unfaithful)
    REQUIRES_GROUND_TRUTH = False  # Does NOT require ground truth
    CHOICES = {
        "faithful": 1.0,
        "unfaithful": 0.0,
    }
    PROMPT_TEMPLATE = """You are an expert evaluator for RAG (Retrieval-Augmented Generation) systems. Your task is to assess the faithfulness of a generated response to the provided retrieval context.

Faithfulness means the response is fully grounded in the context and contains no hallucinated information.

<query>
{input}
</query>

<retrieval_context>
{context}
</retrieval_context>

<generated_response>
{output}
</generated_response>

Analyze the generated response:
1. Break down the response into key statements/claims
2. Verify each statement is supported by the retrieval context
3. Check if any information goes beyond what's in the context

The response is FAITHFUL if:
- All statements can be verified from the context
- No information is added beyond the context
- No facts are misrepresented or distorted

The response is UNFAITHFUL if:
- Contains claims not found in the context
- Misrepresents information from the context
- Adds assumptions or external knowledge

Respond with:
- label: "faithful" if the response is fully grounded in the context
- label: "unfaithful" if the response contains any information not supported by the context
- explanation: Brief reasoning with specific examples of faithful or unfaithful statements"""

    def _check_ground_truth(self, eval_input: Dict[str, Any]) -> bool:
        """Faithfulness evaluator doesn't use ground truth."""
        return False  # Always reference-free


class AnswerRelevancyEvaluator(LLMEvaluator):
    """Evaluator for assessing how relevant the answer is to the input query.

    This evaluator checks whether the generated response directly addresses
    the input question and provides relevant information. Unlike RelevanceEvaluator
    which checks context relevance, this checks answer-to-query relevance.

    Example:
        >>> from custom.evals import AnswerRelevancyEvaluator
        >>> from custom.evals.llm import LLM
        >>>
        >>> llm = LLM(provider="openai", model="gpt-4o-mini")
        >>> evaluator = AnswerRelevancyEvaluator(llm)
        >>>
        >>> eval_input = {
        ...     "input": "What is the capital of France?",
        ...     "output": "Paris is the capital of France."
        ... }
        >>> score = evaluator.evaluate(eval_input)
        >>> print(f"Answer Relevancy: {score.label} ({score.score})")
    """

    NAME = "answer_relevancy"
    DIRECTION = "maximize"  # Higher is better (1 = relevant, 0 = irrelevant)
    REQUIRES_GROUND_TRUTH = False  # Does NOT require ground truth
    CHOICES = {
        "relevant": 1.0,
        "irrelevant": 0.0,
    }
    PROMPT_TEMPLATE = """You are an expert evaluator for LLM systems. Your task is to assess how relevant the generated answer is to the input query.

Answer relevancy measures whether the response directly addresses the question and provides useful information.

<query>
{input}
</query>

<generated_answer>
{output}
</generated_answer>

Evaluate the answer:
1. Does it directly address the query?
2. Does it provide information that helps answer the question?
3. Is it focused and on-topic (not rambling or off-topic)?
4. Does it include the key information requested?

The answer is RELEVANT if:
- Directly answers the specific question asked
- Provides useful and appropriate information
- Stays focused on the query topic
- Includes the core information requested

The answer is IRRELEVANT if:
- Doesn't address the query
- Provides unrelated information
- Is too vague or generic
- Completely misses the point of the question

Respond with:
- label: "relevant" if the answer appropriately addresses the query
- label: "irrelevant" if the answer doesn't address the query
- explanation: Brief reasoning about why the answer is relevant or irrelevant"""

    def _check_ground_truth(self, eval_input: Dict[str, Any]) -> bool:
        """Answer relevancy evaluator doesn't use ground truth."""
        return False  # Always reference-free
