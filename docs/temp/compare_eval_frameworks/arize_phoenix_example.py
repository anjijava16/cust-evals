"""
Arize Phoenix Evaluation Framework Example

This example demonstrates how to use Phoenix evals for LLM evaluation.
Phoenix provides pre-built evaluators for relevance, hallucination, toxicity, and more.

Installation:
pip install arize-phoenix-evals openai

Documentation: https://docs.arize.com/phoenix/
"""

import os
from phoenix.evals import (
    HallucinationEvaluator,
    RelevanceEvaluator,
    QAEvaluator,
    ToxicityEvaluator,
    OpenAIModel
)
import pandas as pd


def setup_phoenix_model():
    """Initialize the Phoenix OpenAI model for evaluations."""
    # Phoenix uses OpenAI models for evaluations
    model = OpenAIModel(
        model="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return model


def evaluate_hallucination():
    """
    Evaluate whether responses contain hallucinations.
    Checks if the output is grounded in the provided context.
    """
    print("\n=== Hallucination Evaluation ===")

    model = setup_phoenix_model()
    evaluator = HallucinationEvaluator(model)

    # Sample data
    data = pd.DataFrame({
        "input": ["What is the capital of France?"],
        "output": ["The capital of France is Paris, which is located on the Seine River."],
        "context": ["France is a country in Western Europe. Paris is its capital and largest city."]
    })

    # Run evaluation
    results = evaluator.evaluate(data)

    print(f"Results:\n{results}")
    return results


def evaluate_relevance():
    """
    Evaluate the relevance of responses to queries.
    Measures how well the response addresses the question.
    """
    print("\n=== Relevance Evaluation ===")

    model = setup_phoenix_model()
    evaluator = RelevanceEvaluator(model)

    # Sample data
    data = pd.DataFrame({
        "input": ["What are the health benefits of exercise?"],
        "output": ["Regular exercise improves cardiovascular health, strengthens muscles, and enhances mental well-being."],
        "context": ["Exercise has numerous health benefits including improved heart health, weight management, and better mood."]
    })

    # Run evaluation
    results = evaluator.evaluate(data)

    print(f"Results:\n{results}")
    return results


def evaluate_qa_correctness():
    """
    Evaluate question-answering correctness.
    Compares model output against reference answers.
    """
    print("\n=== QA Correctness Evaluation ===")

    model = setup_phoenix_model()
    evaluator = QAEvaluator(model)

    # Sample data with expected answers
    data = pd.DataFrame({
        "input": ["What is 2+2?", "Who wrote Romeo and Juliet?"],
        "output": ["2+2 equals 4", "William Shakespeare wrote Romeo and Juliet"],
        "expected": ["4", "William Shakespeare"]
    })

    # Run evaluation
    results = evaluator.evaluate(data)

    print(f"Results:\n{results}")
    return results


def evaluate_toxicity():
    """
    Evaluate content for toxicity and harmful language.
    Useful for content moderation and safety checks.
    """
    print("\n=== Toxicity Evaluation ===")

    model = setup_phoenix_model()
    evaluator = ToxicityEvaluator(model)

    # Sample data
    data = pd.DataFrame({
        "input": ["Tell me about the weather", "What do you think about technology?"],
        "output": [
            "The weather today is sunny and pleasant.",
            "Technology has revolutionized how we communicate and work."
        ]
    })

    # Run evaluation
    results = evaluator.evaluate(data)

    print(f"Results:\n{results}")
    return results


def batch_evaluation_example():
    """
    Demonstrate batch evaluation with multiple metrics.
    Evaluate a dataset across multiple dimensions simultaneously.
    """
    print("\n=== Batch Multi-Metric Evaluation ===")

    model = setup_phoenix_model()

    # Create sample dataset
    data = pd.DataFrame({
        "query": [
            "What causes rain?",
            "Explain photosynthesis",
            "How do vaccines work?"
        ],
        "response": [
            "Rain is caused by water vapor condensing in clouds and falling as precipitation.",
            "Photosynthesis is the process where plants convert sunlight into energy using chlorophyll.",
            "Vaccines train the immune system to recognize and fight specific pathogens."
        ],
        "reference_context": [
            "The water cycle involves evaporation, condensation, and precipitation.",
            "Plants use sunlight, water, and CO2 to produce glucose and oxygen.",
            "Vaccines contain weakened or inactive pathogens that trigger immune response."
        ]
    })

    # Initialize multiple evaluators
    hallucination_eval = HallucinationEvaluator(model)
    relevance_eval = RelevanceEvaluator(model)

    # Prepare data for each evaluator
    hallucination_data = data.rename(columns={
        "query": "input",
        "response": "output",
        "reference_context": "context"
    })

    # Run evaluations
    hallucination_results = hallucination_eval.evaluate(hallucination_data)
    relevance_results = relevance_eval.evaluate(hallucination_data)

    # Combine results
    combined = pd.concat([
        data,
        hallucination_results.add_prefix("hallucination_"),
        relevance_results.add_prefix("relevance_")
    ], axis=1)

    print(f"\nCombined Results:\n{combined}")
    return combined


def custom_evaluation_criteria():
    """
    Example of using Phoenix with custom evaluation criteria.
    You can define custom prompts for domain-specific evaluations.
    """
    print("\n=== Custom Evaluation Criteria ===")

    from phoenix.evals import LLMEvaluator

    model = setup_phoenix_model()

    # Define custom evaluation template
    custom_template = """
    Evaluate if the response demonstrates professional tone and clarity.

    Query: {input}
    Response: {output}

    Score from 1-5 where:
    1 = Unprofessional or unclear
    5 = Highly professional and clear

    Provide your score and brief explanation.
    """

    evaluator = LLMEvaluator(
        model=model,
        template=custom_template
    )

    data = pd.DataFrame({
        "input": ["How do I reset my password?"],
        "output": ["You can reset your password by clicking the 'Forgot Password' link on the login page."]
    })

    results = evaluator.evaluate(data)
    print(f"Custom Evaluation Results:\n{results}")
    return results


def main():
    """Run all Phoenix evaluation examples."""
    print("=" * 60)
    print("Arize Phoenix Evaluation Framework Examples")
    print("=" * 60)

    try:
        # Run individual evaluations
        evaluate_hallucination()
        evaluate_relevance()
        evaluate_qa_correctness()
        evaluate_toxicity()

        # Run batch evaluation
        batch_evaluation_example()

        # Run custom evaluation
        custom_evaluation_criteria()

        print("\n" + "=" * 60)
        print("All evaluations completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Make sure you have set OPENAI_API_KEY environment variable")
        print("Install requirements: pip install arize-phoenix-evals openai pandas")


if __name__ == "__main__":
    main()
