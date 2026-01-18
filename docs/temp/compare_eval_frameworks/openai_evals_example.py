"""
OpenAI Evals Framework Example

OpenAI Evals is an open-source framework for evaluating LLMs.
It provides a standardized way to create and run evaluations.

Installation:
pip install evals openai

Documentation: https://github.com/openai/evals
"""

import os
import json
from typing import Any, Dict, List
from dataclasses import dataclass


# Note: OpenAI Evals typically uses a CLI, but we'll demonstrate the core concepts


@dataclass
class EvalResult:
    """Result of an evaluation."""
    score: float
    passed: bool
    metadata: Dict[str, Any]


class BaseEval:
    """Base class for evaluations."""

    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.results: List[EvalResult] = []

    def run_eval(self) -> Dict[str, Any]:
        """Run the evaluation and return results."""
        raise NotImplementedError


class MatchEval(BaseEval):
    """
    Exact match evaluation.
    Tests if model output exactly matches expected output.
    """

    def __init__(self, test_cases: List[Dict[str, str]], **kwargs):
        super().__init__(**kwargs)
        self.test_cases = test_cases

    def run_eval(self) -> Dict[str, Any]:
        """Run exact match evaluation."""
        print("\n=== Exact Match Evaluation ===")

        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        results = []
        for i, case in enumerate(self.test_cases, 1):
            prompt = case["prompt"]
            expected = case["expected"].lower().strip()

            # Get model response
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            actual = response.choices[0].message.content.lower().strip()

            # Check match
            passed = expected in actual or actual in expected
            score = 1.0 if passed else 0.0

            result = EvalResult(
                score=score,
                passed=passed,
                metadata={
                    "prompt": prompt,
                    "expected": expected,
                    "actual": actual
                }
            )
            results.append(result)

            print(f"Test {i}: {'✓ PASS' if passed else '✗ FAIL'}")
            print(f"  Expected: {expected}")
            print(f"  Got: {actual}")

        # Calculate statistics
        total_score = sum(r.score for r in results)
        avg_score = total_score / len(results) if results else 0

        print(f"\nOverall Score: {avg_score:.2%} ({int(total_score)}/{len(results)})")

        return {
            "average_score": avg_score,
            "total_passed": int(total_score),
            "total_cases": len(results),
            "results": results
        }


class IncludesEval(BaseEval):
    """
    Inclusion evaluation.
    Tests if model output includes specific required content.
    """

    def __init__(self, test_cases: List[Dict[str, Any]], **kwargs):
        super().__init__(**kwargs)
        self.test_cases = test_cases

    def run_eval(self) -> Dict[str, Any]:
        """Run inclusion evaluation."""
        print("\n=== Includes Evaluation ===")

        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        results = []
        for i, case in enumerate(self.test_cases, 1):
            prompt = case["prompt"]
            required_terms = case["required_terms"]

            # Get model response
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            actual = response.choices[0].message.content.lower()

            # Check if all required terms are included
            included = [term for term in required_terms if term.lower() in actual]
            missing = [term for term in required_terms if term.lower() not in actual]

            score = len(included) / len(required_terms) if required_terms else 1.0
            passed = len(missing) == 0

            result = EvalResult(
                score=score,
                passed=passed,
                metadata={
                    "prompt": prompt,
                    "required_terms": required_terms,
                    "included": included,
                    "missing": missing,
                    "response": actual[:200]
                }
            )
            results.append(result)

            print(f"Test {i}: {'✓ PASS' if passed else '✗ FAIL'} ({score:.0%})")
            print(f"  Included: {included}")
            if missing:
                print(f"  Missing: {missing}")

        avg_score = sum(r.score for r in results) / len(results) if results else 0
        print(f"\nOverall Score: {avg_score:.2%}")

        return {
            "average_score": avg_score,
            "results": results
        }


class ModelGradedEval(BaseEval):
    """
    Model-graded evaluation.
    Uses another LLM to grade the outputs.
    """

    def __init__(self, test_cases: List[Dict[str, str]], grading_model: str = "gpt-4", **kwargs):
        super().__init__(**kwargs)
        self.test_cases = test_cases
        self.grading_model = grading_model

    def run_eval(self) -> Dict[str, Any]:
        """Run model-graded evaluation."""
        print("\n=== Model-Graded Evaluation ===")

        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        results = []
        for i, case in enumerate(self.test_cases, 1):
            prompt = case["prompt"]
            grading_criteria = case.get("criteria", "accuracy and helpfulness")

            # Get model response
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            actual = response.choices[0].message.content

            # Grade the response
            grading_prompt = f"""
            Grade the following response on a scale of 1-5 for {grading_criteria}.

            Prompt: {prompt}
            Response: {actual}

            Provide your grade as a single number (1-5) followed by a brief explanation.
            Format: GRADE: <number>
            EXPLANATION: <explanation>
            """

            grading_response = client.chat.completions.create(
                model=self.grading_model,
                messages=[{"role": "user", "content": grading_prompt}],
                temperature=0
            )
            grading_text = grading_response.choices[0].message.content

            # Parse grade
            try:
                grade_line = [line for line in grading_text.split('\n') if 'GRADE:' in line][0]
                grade = float(grade_line.split(':')[1].strip().split()[0])
                score = grade / 5.0  # Normalize to 0-1
                passed = grade >= 3.0
            except Exception:
                score = 0.5
                passed = False
                grading_text = "Failed to parse grade"

            result = EvalResult(
                score=score,
                passed=passed,
                metadata={
                    "prompt": prompt,
                    "response": actual,
                    "grading": grading_text
                }
            )
            results.append(result)

            print(f"Test {i}: {'✓ PASS' if passed else '✗ FAIL'} (Score: {score:.2f})")
            print(f"  {grading_text[:100]}...")

        avg_score = sum(r.score for r in results) / len(results) if results else 0
        print(f"\nOverall Score: {avg_score:.2%}")

        return {
            "average_score": avg_score,
            "results": results
        }


class ClosedQAEval(BaseEval):
    """
    Closed Q&A evaluation with multiple choice.
    Tests factual knowledge with specific correct answers.
    """

    def __init__(self, test_cases: List[Dict[str, Any]], **kwargs):
        super().__init__(**kwargs)
        self.test_cases = test_cases

    def run_eval(self) -> Dict[str, Any]:
        """Run closed Q&A evaluation."""
        print("\n=== Closed Q&A Evaluation ===")

        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        results = []
        for i, case in enumerate(self.test_cases, 1):
            question = case["question"]
            choices = case["choices"]
            correct_answer = case["correct_answer"]

            # Format prompt with choices
            choices_text = "\n".join([f"{chr(65+i)}. {choice}" for i, choice in enumerate(choices)])
            prompt = f"{question}\n\n{choices_text}\n\nAnswer with just the letter (A, B, C, or D)."

            # Get model response
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=10
            )
            actual = response.choices[0].message.content.strip().upper()

            # Check if correct
            passed = correct_answer.upper() in actual
            score = 1.0 if passed else 0.0

            result = EvalResult(
                score=score,
                passed=passed,
                metadata={
                    "question": question,
                    "correct": correct_answer,
                    "actual": actual,
                    "choices": choices
                }
            )
            results.append(result)

            print(f"Test {i}: {'✓ PASS' if passed else '✗ FAIL'}")
            print(f"  Question: {question}")
            print(f"  Expected: {correct_answer}, Got: {actual}")

        total_score = sum(r.score for r in results)
        avg_score = total_score / len(results) if results else 0

        print(f"\nOverall Score: {avg_score:.2%} ({int(total_score)}/{len(results)})")

        return {
            "average_score": avg_score,
            "total_correct": int(total_score),
            "total_questions": len(results),
            "results": results
        }


class FuzzyMatchEval(BaseEval):
    """
    Fuzzy matching evaluation.
    Allows for minor variations in responses.
    """

    def __init__(self, test_cases: List[Dict[str, Any]], threshold: float = 0.8, **kwargs):
        super().__init__(**kwargs)
        self.test_cases = test_cases
        self.threshold = threshold

    def run_eval(self) -> Dict[str, Any]:
        """Run fuzzy match evaluation."""
        print("\n=== Fuzzy Match Evaluation ===")

        from openai import OpenAI
        from difflib import SequenceMatcher

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        results = []
        for i, case in enumerate(self.test_cases, 1):
            prompt = case["prompt"]
            expected = case["expected"]

            # Get model response
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            actual = response.choices[0].message.content

            # Calculate similarity
            similarity = SequenceMatcher(None, expected.lower(), actual.lower()).ratio()
            passed = similarity >= self.threshold
            score = similarity

            result = EvalResult(
                score=score,
                passed=passed,
                metadata={
                    "prompt": prompt,
                    "expected": expected,
                    "actual": actual,
                    "similarity": similarity
                }
            )
            results.append(result)

            print(f"Test {i}: {'✓ PASS' if passed else '✗ FAIL'} (Similarity: {similarity:.2%})")

        avg_score = sum(r.score for r in results) / len(results) if results else 0
        print(f"\nOverall Score: {avg_score:.2%}")

        return {
            "average_score": avg_score,
            "threshold": self.threshold,
            "results": results
        }


def run_match_eval_example():
    """Example of exact match evaluation."""
    test_cases = [
        {
            "prompt": "What is 2+2? Answer with just the number.",
            "expected": "4"
        },
        {
            "prompt": "What is the capital of France? Answer with just the city name.",
            "expected": "Paris"
        },
        {
            "prompt": "Who wrote Romeo and Juliet? Answer with just the name.",
            "expected": "William Shakespeare"
        }
    ]

    eval_runner = MatchEval(test_cases=test_cases, model="gpt-3.5-turbo")
    return eval_runner.run_eval()


def run_includes_eval_example():
    """Example of includes evaluation."""
    test_cases = [
        {
            "prompt": "Explain the benefits of exercise.",
            "required_terms": ["health", "cardiovascular", "strength"]
        },
        {
            "prompt": "What is machine learning?",
            "required_terms": ["data", "algorithms", "predictions"]
        }
    ]

    eval_runner = IncludesEval(test_cases=test_cases)
    return eval_runner.run_eval()


def run_model_graded_example():
    """Example of model-graded evaluation."""
    test_cases = [
        {
            "prompt": "Explain quantum computing to a 10-year-old.",
            "criteria": "clarity and age-appropriateness"
        },
        {
            "prompt": "Write a professional email requesting a meeting.",
            "criteria": "professionalism and clarity"
        }
    ]

    eval_runner = ModelGradedEval(test_cases=test_cases)
    return eval_runner.run_eval()


def run_closed_qa_example():
    """Example of closed Q&A evaluation."""
    test_cases = [
        {
            "question": "What is the capital of Japan?",
            "choices": ["Beijing", "Tokyo", "Seoul", "Bangkok"],
            "correct_answer": "B"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "choices": ["Venus", "Jupiter", "Mars", "Saturn"],
            "correct_answer": "C"
        }
    ]

    eval_runner = ClosedQAEval(test_cases=test_cases)
    return eval_runner.run_eval()


def run_fuzzy_match_example():
    """Example of fuzzy matching evaluation."""
    test_cases = [
        {
            "prompt": "Summarize: The quick brown fox jumps over the lazy dog.",
            "expected": "A fox jumps over a dog"
        }
    ]

    eval_runner = FuzzyMatchEval(test_cases=test_cases, threshold=0.6)
    return eval_runner.run_eval()


def main():
    """Run all OpenAI Evals examples."""
    print("=" * 60)
    print("OpenAI Evals Framework Examples")
    print("=" * 60)

    try:
        # Run different evaluation types
        run_match_eval_example()
        run_includes_eval_example()
        run_model_graded_example()
        run_closed_qa_example()
        run_fuzzy_match_example()

        print("\n" + "=" * 60)
        print("All OpenAI Evals completed successfully!")
        print("=" * 60)

        print("\n📊 OpenAI Evals Evaluation Types:")
        print("  • Match: Exact string matching")
        print("  • Includes: Required content presence")
        print("  • Model-Graded: LLM-based evaluation")
        print("  • Closed Q&A: Multiple choice questions")
        print("  • Fuzzy Match: Similarity-based matching")
        print("  • Custom: Build your own evaluators")

        print("\n💡 Note: OpenAI Evals typically uses CLI commands:")
        print("  oaievals <eval_name> --model <model_name>")
        print("  This example demonstrates core concepts programmatically.")

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Make sure you have set OPENAI_API_KEY environment variable")
        print("Install requirements: pip install evals openai")


if __name__ == "__main__":
    main()
