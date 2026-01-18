"""
LangSmith Evaluation Framework Example

LangSmith provides comprehensive evaluation and observability for LLM applications.
It integrates well with LangChain and offers both automated and human-in-the-loop evaluation.

Installation:
pip install langsmith langchain-openai

Documentation: https://docs.smith.langchain.com/
"""

import os
from langsmith import Client
from langsmith.evaluation import evaluate, EvaluationResult
from langsmith.schemas import Example, Run
from langchain_openai import ChatOpenAI


def setup_langsmith():
    """Initialize LangSmith client."""
    client = Client(
        api_key=os.getenv("LANGSMITH_API_KEY"),
        api_url=os.getenv("LANGSMITH_API_URL", "https://api.smith.langchain.com")
    )
    return client


def create_dataset():
    """
    Create a dataset for evaluation.
    Datasets are reusable collections of examples for testing.
    """
    print("\n=== Creating Evaluation Dataset ===")

    client = setup_langsmith()

    # Create or get dataset
    dataset_name = "qa-evaluation-dataset"

    try:
        dataset = client.create_dataset(
            dataset_name=dataset_name,
            description="Question-answering evaluation dataset"
        )
        print(f"Created dataset: {dataset_name}")
    except Exception:
        dataset = client.read_dataset(dataset_name=dataset_name)
        print(f"Using existing dataset: {dataset_name}")

    # Add examples to dataset
    examples = [
        {
            "inputs": {"question": "What is the capital of France?"},
            "outputs": {"answer": "Paris"}
        },
        {
            "inputs": {"question": "Who wrote Romeo and Juliet?"},
            "outputs": {"answer": "William Shakespeare"}
        },
        {
            "inputs": {"question": "What is 2+2?"},
            "outputs": {"answer": "4"}
        }
    ]

    for example in examples:
        try:
            client.create_example(
                inputs=example["inputs"],
                outputs=example["outputs"],
                dataset_id=dataset.id
            )
        except Exception:
            pass  # Example might already exist

    print(f"Dataset ready with examples")
    return dataset


def correctness_evaluator(run: Run, example: Example) -> EvaluationResult:
    """
    Custom evaluator for answer correctness.
    Compares predicted answer with expected answer.
    """
    predicted = run.outputs.get("answer", "")
    expected = example.outputs.get("answer", "")

    # Simple exact match (case-insensitive)
    is_correct = predicted.lower().strip() == expected.lower().strip()

    return EvaluationResult(
        key="correctness",
        score=1.0 if is_correct else 0.0,
        comment=f"Expected: {expected}, Got: {predicted}"
    )


def relevance_evaluator(run: Run, example: Example) -> EvaluationResult:
    """
    Evaluate if answer is relevant to the question.
    Uses simple keyword matching (can be enhanced with LLM).
    """
    question = example.inputs.get("question", "").lower()
    answer = run.outputs.get("answer", "").lower()

    # Simple relevance check - answer contains key terms from question
    question_words = set(question.split())
    answer_words = set(answer.split())

    overlap = len(question_words & answer_words)
    relevance_score = min(overlap / max(len(question_words), 1), 1.0)

    return EvaluationResult(
        key="relevance",
        score=relevance_score,
        comment=f"Word overlap: {overlap} words"
    )


def llm_as_judge_evaluator(run: Run, example: Example) -> EvaluationResult:
    """
    Use LLM as a judge to evaluate response quality.
    More sophisticated evaluation using GPT-4.
    """
    llm = ChatOpenAI(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))

    question = example.inputs.get("question", "")
    answer = run.outputs.get("answer", "")
    expected = example.outputs.get("answer", "")

    prompt = f"""
    Evaluate the answer quality on a scale of 0.0 to 1.0.

    Question: {question}
    Expected: {expected}
    Actual: {answer}

    Consider accuracy, completeness, and clarity.
    Respond with just a score between 0.0 and 1.0.
    """

    try:
        response = llm.invoke(prompt)
        score = float(response.content.strip())
        score = max(0.0, min(1.0, score))  # Clamp to [0, 1]
    except Exception:
        score = 0.5  # Default score on error

    return EvaluationResult(
        key="llm_judge_quality",
        score=score,
        comment="Evaluated by GPT-4"
    )


def run_basic_evaluation():
    """
    Run basic evaluation on a dataset.
    Uses predefined evaluators to assess model performance.
    """
    print("\n=== Running Basic Evaluation ===")

    client = setup_langsmith()

    # Create dataset
    dataset = create_dataset()

    # Define the model/function to evaluate
    def qa_model(inputs: dict) -> dict:
        """Simple Q&A model to evaluate."""
        question = inputs["question"]

        # Dummy model - replace with actual model
        answers = {
            "what is the capital of france?": "Paris",
            "who wrote romeo and juliet?": "William Shakespeare",
            "what is 2+2?": "4"
        }

        answer = answers.get(question.lower(), "I don't know")
        return {"answer": answer}

    # Run evaluation
    results = evaluate(
        qa_model,
        data=dataset.name,
        evaluators=[correctness_evaluator, relevance_evaluator],
        experiment_prefix="qa-eval"
    )

    print(f"\nEvaluation completed!")
    print(f"Results: {results}")

    return results


def run_llm_evaluation():
    """
    Evaluate LLM outputs using LangSmith.
    Tests an actual language model's responses.
    """
    print("\n=== Running LLM Evaluation ===")

    client = setup_langsmith()
    llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

    # Create dataset
    dataset = create_dataset()

    # Define model function
    def llm_qa(inputs: dict) -> dict:
        """LLM-based Q&A."""
        question = inputs["question"]
        response = llm.invoke(f"Answer briefly: {question}")
        return {"answer": response.content}

    # Run evaluation with LLM judge
    results = evaluate(
        llm_qa,
        data=dataset.name,
        evaluators=[
            correctness_evaluator,
            relevance_evaluator,
            llm_as_judge_evaluator
        ],
        experiment_prefix="llm-qa-eval"
    )

    print(f"\nLLM Evaluation completed!")
    return results


def run_chain_evaluation():
    """
    Evaluate a LangChain chain.
    Demonstrates evaluation of complex LangChain pipelines.
    """
    print("\n=== Evaluating LangChain Chain ===")

    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain

    client = setup_langsmith()
    llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

    # Create a simple chain
    prompt = PromptTemplate(
        input_variables=["question"],
        template="Please answer this question concisely: {question}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    # Create dataset
    dataset = create_dataset()

    # Evaluation function
    def run_chain(inputs: dict) -> dict:
        result = chain.run(question=inputs["question"])
        return {"answer": result}

    # Run evaluation
    results = evaluate(
        run_chain,
        data=dataset.name,
        evaluators=[correctness_evaluator, llm_as_judge_evaluator],
        experiment_prefix="chain-eval"
    )

    print(f"\nChain evaluation completed!")
    return results


def custom_metric_evaluation():
    """
    Create and use custom evaluation metrics.
    Demonstrates flexibility for domain-specific needs.
    """
    print("\n=== Custom Metric Evaluation ===")

    def length_evaluator(run: Run, example: Example) -> EvaluationResult:
        """Evaluate if answer length is appropriate."""
        answer = run.outputs.get("answer", "")
        length = len(answer)

        # Prefer answers between 10-100 characters
        if 10 <= length <= 100:
            score = 1.0
            comment = "Good length"
        elif length < 10:
            score = 0.5
            comment = "Too short"
        else:
            score = 0.7
            comment = "Too long"

        return EvaluationResult(
            key="answer_length",
            score=score,
            comment=comment
        )

    def completeness_evaluator(run: Run, example: Example) -> EvaluationResult:
        """Evaluate answer completeness."""
        answer = run.outputs.get("answer", "")

        # Check for minimum information
        has_answer = len(answer.strip()) > 0
        has_detail = len(answer.split()) > 3

        score = 0.5 if has_answer else 0.0
        score += 0.5 if has_detail else 0.0

        return EvaluationResult(
            key="completeness",
            score=score,
            comment=f"Answer has {len(answer.split())} words"
        )

    client = setup_langsmith()
    dataset = create_dataset()

    def qa_model(inputs: dict) -> dict:
        return {"answer": "This is a test answer with some detail."}

    # Run with custom evaluators
    results = evaluate(
        qa_model,
        data=dataset.name,
        evaluators=[length_evaluator, completeness_evaluator],
        experiment_prefix="custom-metrics"
    )

    print(f"\nCustom metric evaluation completed!")
    return results


def ab_test_comparison():
    """
    Compare two models/systems using A/B testing.
    Useful for determining which model performs better.
    """
    print("\n=== A/B Test Comparison ===")

    client = setup_langsmith()
    dataset = create_dataset()

    # Model A: Simple responses
    def model_a(inputs: dict) -> dict:
        answers = {
            "what is the capital of france?": "Paris",
            "who wrote romeo and juliet?": "Shakespeare",
            "what is 2+2?": "4"
        }
        return {"answer": answers.get(inputs["question"].lower(), "Unknown")}

    # Model B: Detailed responses
    def model_b(inputs: dict) -> dict:
        answers = {
            "what is the capital of france?": "The capital of France is Paris.",
            "who wrote romeo and juliet?": "Romeo and Juliet was written by William Shakespeare.",
            "what is 2+2?": "2 plus 2 equals 4."
        }
        return {"answer": answers.get(inputs["question"].lower(), "I don't know")}

    # Evaluate both models
    print("\nEvaluating Model A...")
    results_a = evaluate(
        model_a,
        data=dataset.name,
        evaluators=[correctness_evaluator],
        experiment_prefix="model-a"
    )

    print("\nEvaluating Model B...")
    results_b = evaluate(
        model_b,
        data=dataset.name,
        evaluators=[correctness_evaluator],
        experiment_prefix="model-b"
    )

    print("\n=== Comparison Results ===")
    print(f"Model A: {results_a}")
    print(f"Model B: {results_b}")

    return results_a, results_b


def online_evaluation_example():
    """
    Example of setting up online/production evaluation.
    Monitors live system performance.
    """
    print("\n=== Online Evaluation Setup ===")

    from langsmith import traceable

    @traceable(run_type="llm", name="production_qa")
    def production_qa_system(question: str) -> str:
        """Production Q&A system with automatic tracing."""
        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
        response = llm.invoke(question)
        return response.content

    # Use the system - automatically traced
    print("\nRunning traced queries...")
    questions = [
        "What is machine learning?",
        "Explain quantum computing",
        "What is blockchain?"
    ]

    for question in questions:
        answer = production_qa_system(question)
        print(f"Q: {question}")
        print(f"A: {answer[:100]}...")

    print("\n✓ All queries traced to LangSmith")
    print("View traces at: https://smith.langchain.com")

    return True


def main():
    """Run all LangSmith evaluation examples."""
    print("=" * 60)
    print("LangSmith Evaluation Framework Examples")
    print("=" * 60)

    try:
        # Basic evaluations
        run_basic_evaluation()
        run_llm_evaluation()
        run_chain_evaluation()

        # Advanced evaluations
        custom_metric_evaluation()
        ab_test_comparison()
        online_evaluation_example()

        print("\n" + "=" * 60)
        print("All LangSmith evaluations completed successfully!")
        print("=" * 60)

        print("\n📊 LangSmith Evaluation Features:")
        print("  • Dataset Management: Reusable test sets")
        print("  • Custom Evaluators: Domain-specific metrics")
        print("  • LLM-as-Judge: Sophisticated evaluation")
        print("  • A/B Testing: Compare models/systems")
        print("  • Online Monitoring: Production evaluation")
        print("  • Tracing: Full observability")
        print("  • Human Feedback: Manual review integration")

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Setup required:")
        print("  1. Set LANGSMITH_API_KEY environment variable")
        print("  2. Set OPENAI_API_KEY environment variable")
        print("  3. Install: pip install langsmith langchain-openai")


if __name__ == "__main__":
    main()
