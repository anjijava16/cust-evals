"""
MLflow LLM Evaluation Example

MLflow provides comprehensive LLM evaluation capabilities with tracking,
model comparison, and integration with the MLflow ecosystem.

Installation:
pip install mlflow openai

Documentation: https://mlflow.org/docs/latest/llms/llm-evaluate/index.html
"""

import os
import mlflow
import pandas as pd
from mlflow.metrics.genai import (
    answer_relevance,
    answer_correctness,
    faithfulness,
    answer_similarity
)


def setup_mlflow():
    """Setup MLflow tracking."""
    # Set tracking URI (can be local or remote)
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("llm_evaluation_examples")
    print("✓ MLflow tracking setup complete")


def basic_qa_evaluation():
    """
    Basic Q&A evaluation using MLflow.
    Demonstrates core evaluation workflow.
    """
    print("\n=== Basic Q&A Evaluation ===")

    # Create evaluation dataset
    eval_data = pd.DataFrame({
        "question": [
            "What is machine learning?",
            "What is Python?",
            "What is the capital of France?"
        ],
        "answer": [
            "Machine learning is a subset of AI that learns from data.",
            "Python is a high-level programming language.",
            "The capital of France is Paris."
        ],
        "ground_truth": [
            "Machine learning is a branch of AI focused on learning from data.",
            "Python is a programming language known for its simplicity.",
            "Paris"
        ]
    })

    # Define model to evaluate (simple function)
    def qa_model(question):
        # In practice, this would call your actual model
        answers = {
            "What is machine learning?": "Machine learning is a subset of AI that learns from data.",
            "What is Python?": "Python is a high-level programming language.",
            "What is the capital of France?": "The capital of France is Paris."
        }
        return answers.get(question, "I don't know")

    # Run evaluation
    with mlflow.start_run(run_name="basic_qa_eval"):
        results = mlflow.evaluate(
            model=qa_model,
            data=eval_data,
            targets="ground_truth",
            model_type="question-answering",
            evaluators="default"
        )

        print(f"\nEvaluation Metrics:")
        print(f"  Toxicity: {results.metrics.get('toxicity/v1/mean', 'N/A')}")
        print(f"  Flesch Kincaid: {results.metrics.get('flesch_kincaid_grade_level/v1/mean', 'N/A')}")

    return results


def rag_evaluation_with_context():
    """
    Evaluate RAG system with context.
    Includes faithfulness and groundedness metrics.
    """
    print("\n=== RAG Evaluation with Context ===")

    # RAG evaluation data
    eval_data = pd.DataFrame({
        "question": [
            "What are the health benefits of exercise?",
            "How does photosynthesis work?",
        ],
        "answer": [
            "Regular exercise improves cardiovascular health, strengthens muscles, and enhances mental well-being.",
            "Photosynthesis is the process by which plants use sunlight to convert CO2 and water into glucose and oxygen.",
        ],
        "context": [
            "Exercise has numerous health benefits including improved heart health, stronger muscles, better mood, and weight management.",
            "During photosynthesis, plants absorb sunlight through chlorophyll and use it to transform carbon dioxide and water into glucose (sugar) and oxygen.",
        ],
        "ground_truth": [
            "Exercise benefits include cardiovascular health, muscle strength, and mental health.",
            "Photosynthesis converts light energy into chemical energy, producing glucose and oxygen from CO2 and water.",
        ]
    })

    # Define RAG model
    def rag_model(question, context):
        # Simulated RAG model that uses context
        responses = {
            "What are the health benefits of exercise?":
                "Regular exercise improves cardiovascular health, strengthens muscles, and enhances mental well-being.",
            "How does photosynthesis work?":
                "Photosynthesis is the process by which plants use sunlight to convert CO2 and water into glucose and oxygen.",
        }
        return responses.get(question, "Information not found")

    # Wrap model for MLflow
    class RAGModel(mlflow.pyfunc.PythonModel):
        def predict(self, context, model_input):
            if isinstance(model_input, pd.DataFrame):
                results = []
                for _, row in model_input.iterrows():
                    answer = rag_model(row['question'], row.get('context', ''))
                    results.append(answer)
                return results
            return rag_model(model_input['question'], model_input.get('context', ''))

    with mlflow.start_run(run_name="rag_evaluation"):
        # Create custom metrics for RAG
        faithfulness_metric = faithfulness(model="openai:/gpt-4")
        answer_relevance_metric = answer_relevance(model="openai:/gpt-4")

        # Log model
        model = RAGModel()

        results = mlflow.evaluate(
            model=lambda x: [rag_model(row['question'], row['context']) for _, row in x.iterrows()],
            data=eval_data,
            targets="ground_truth",
            model_type="text",
            extra_metrics=[faithfulness_metric, answer_relevance_metric],
            evaluators="default"
        )

        print(f"\nRAG Evaluation Metrics:")
        for key, value in results.metrics.items():
            if isinstance(value, (int, float)):
                print(f"  {key}: {value:.3f}")

    return results


def custom_metric_evaluation():
    """
    Define and use custom evaluation metrics.
    Demonstrates MLflow metric extensibility.
    """
    print("\n=== Custom Metric Evaluation ===")

    from mlflow.metrics import make_metric

    # Define custom metric: word count
    def word_count_metric(predictions, targets, metrics):
        """Custom metric to check response length."""
        word_counts = [len(pred.split()) for pred in predictions]
        avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
        return avg_words

    word_count = make_metric(
        eval_fn=word_count_metric,
        greater_is_better=False,
        name="word_count"
    )

    # Define custom metric: keyword presence
    def keyword_presence_metric(predictions, targets, metrics):
        """Check if key terms from targets appear in predictions."""
        scores = []
        for pred, target in zip(predictions, targets):
            target_words = set(target.lower().split())
            pred_words = set(pred.lower().split())
            overlap = len(target_words & pred_words)
            score = overlap / len(target_words) if target_words else 0
            scores.append(score)
        return sum(scores) / len(scores) if scores else 0

    keyword_metric = make_metric(
        eval_fn=keyword_presence_metric,
        greater_is_better=True,
        name="keyword_presence"
    )

    # Evaluation data
    eval_data = pd.DataFrame({
        "input": ["What is AI?", "Explain cloud computing"],
        "prediction": [
            "AI is artificial intelligence",
            "Cloud computing delivers services over the internet"
        ],
        "target": [
            "artificial intelligence",
            "cloud computing internet services"
        ]
    })

    with mlflow.start_run(run_name="custom_metrics"):
        results = mlflow.evaluate(
            data=eval_data,
            predictions="prediction",
            targets="target",
            model_type="text",
            extra_metrics=[word_count, keyword_metric]
        )

        print(f"\nCustom Metric Results:")
        print(f"  Word Count: {results.metrics.get('word_count', 'N/A')}")
        print(f"  Keyword Presence: {results.metrics.get('keyword_presence', 'N/A'):.3f}")

    return results


def model_comparison():
    """
    Compare multiple models using MLflow.
    Useful for A/B testing and model selection.
    """
    print("\n=== Model Comparison ===")

    eval_data = pd.DataFrame({
        "question": [
            "What is machine learning?",
            "What is deep learning?",
            "What is neural network?"
        ],
        "ground_truth": [
            "Machine learning is AI that learns from data",
            "Deep learning uses neural networks with many layers",
            "Neural networks are computing systems inspired by biological neural networks"
        ]
    })

    # Model A: Simple responses
    def model_a(question):
        responses = {
            "What is machine learning?": "ML is AI",
            "What is deep learning?": "DL uses neural nets",
            "What is neural network?": "NN processes data"
        }
        return responses.get(question, "Unknown")

    # Model B: Detailed responses
    def model_b(question):
        responses = {
            "What is machine learning?": "Machine learning is a subset of artificial intelligence that learns from data",
            "What is deep learning?": "Deep learning is a type of machine learning using neural networks with multiple layers",
            "What is neural network?": "Neural networks are computational models inspired by biological neural networks"
        }
        return responses.get(question, "Unknown")

    # Evaluate Model A
    print("\nEvaluating Model A...")
    with mlflow.start_run(run_name="model_a"):
        mlflow.log_param("model_type", "simple")
        results_a = mlflow.evaluate(
            model=model_a,
            data=eval_data,
            targets="ground_truth",
            model_type="text",
            evaluators="default"
        )
        score_a = results_a.metrics.get('token_count/mean', 0)
        mlflow.log_metric("avg_response_length", score_a)

    # Evaluate Model B
    print("Evaluating Model B...")
    with mlflow.start_run(run_name="model_b"):
        mlflow.log_param("model_type", "detailed")
        results_b = mlflow.evaluate(
            model=model_b,
            data=eval_data,
            targets="ground_truth",
            model_type="text",
            evaluators="default"
        )
        score_b = results_b.metrics.get('token_count/mean', 0)
        mlflow.log_metric("avg_response_length", score_b)

    print(f"\n✓ Model comparison complete")
    print(f"  View results: mlflow ui")
    print(f"  Compare runs in MLflow UI")

    return results_a, results_b


def llm_judge_evaluation():
    """
    Use LLM as a judge with MLflow.
    Leverages GPT-4 for sophisticated evaluation.
    """
    print("\n=== LLM Judge Evaluation ===")

    eval_data = pd.DataFrame({
        "question": [
            "Explain quantum computing to a 10-year-old",
            "What is the theory of relativity?"
        ],
        "answer": [
            "Quantum computing is like a super-fast computer that can look at many answers at once, like checking all paths in a maze simultaneously.",
            "Einstein's theory of relativity describes how space and time are connected and how gravity works."
        ],
        "ground_truth": [
            "Age-appropriate explanation of quantum computing",
            "Accurate explanation of relativity"
        ]
    })

    def qa_model(question):
        responses = {
            "Explain quantum computing to a 10-year-old":
                "Quantum computing is like a super-fast computer that can look at many answers at once.",
            "What is the theory of relativity?":
                "Einstein's theory of relativity describes how space and time are connected."
        }
        return responses.get(question, "Unknown")

    with mlflow.start_run(run_name="llm_judge"):
        # Use GPT-4 as judge
        relevance = answer_relevance(model="openai:/gpt-4")
        correctness = answer_correctness(model="openai:/gpt-4")

        results = mlflow.evaluate(
            model=qa_model,
            data=eval_data,
            targets="ground_truth",
            model_type="text",
            extra_metrics=[relevance, correctness]
        )

        print(f"\nLLM Judge Results:")
        for key, value in results.metrics.items():
            if 'relevance' in key or 'correctness' in key:
                print(f"  {key}: {value}")

    return results


def batch_evaluation():
    """
    Run batch evaluation on large dataset.
    Demonstrates scalability.
    """
    print("\n=== Batch Evaluation ===")

    # Create larger dataset
    questions = [f"Question {i}?" for i in range(50)]
    answers = [f"Answer to question {i}" for i in range(50)]
    ground_truths = [f"Ground truth {i}" for i in range(50)]

    eval_data = pd.DataFrame({
        "question": questions,
        "answer": answers,
        "ground_truth": ground_truths
    })

    def batch_model(question):
        # Simple model for demo
        return f"Response to {question}"

    with mlflow.start_run(run_name="batch_evaluation"):
        mlflow.log_param("dataset_size", len(eval_data))

        results = mlflow.evaluate(
            model=batch_model,
            data=eval_data,
            targets="ground_truth",
            model_type="text",
            evaluators="default"
        )

        print(f"\nBatch Evaluation Results:")
        print(f"  Dataset Size: {len(eval_data)}")
        print(f"  Metrics Computed: {len(results.metrics)}")
        print(f"  ✓ Results logged to MLflow")

    return results


def evaluate_with_artifacts():
    """
    Evaluate and log artifacts (charts, tables, etc.).
    Demonstrates MLflow's artifact logging.
    """
    print("\n=== Evaluation with Artifacts ===")

    eval_data = pd.DataFrame({
        "input": ["Query 1", "Query 2", "Query 3"],
        "prediction": ["Response 1", "Response 2", "Response 3"],
        "target": ["Expected 1", "Expected 2", "Expected 3"]
    })

    with mlflow.start_run(run_name="eval_with_artifacts"):
        results = mlflow.evaluate(
            data=eval_data,
            predictions="prediction",
            targets="target",
            model_type="text"
        )

        # Log additional artifacts
        eval_data.to_csv("evaluation_data.csv", index=False)
        mlflow.log_artifact("evaluation_data.csv")

        # Log parameters
        mlflow.log_param("eval_type", "text_comparison")
        mlflow.log_param("num_samples", len(eval_data))

        # Log custom metrics
        mlflow.log_metric("custom_score", 0.85)

        print(f"\n✓ Artifacts logged:")
        print(f"  • evaluation_data.csv")
        print(f"  • Evaluation metrics")
        print(f"  • Run parameters")

    return results


def prompt_template_evaluation():
    """
    Evaluate different prompt templates.
    Useful for prompt engineering.
    """
    print("\n=== Prompt Template Evaluation ===")

    eval_data = pd.DataFrame({
        "question": ["What is AI?", "Explain ML"],
    })

    # Template A: Simple
    def template_a_model(question):
        prompt = f"Answer: {question}"
        return f"Simple answer about {question}"

    # Template B: Detailed
    def template_b_model(question):
        prompt = f"Provide a detailed explanation: {question}"
        return f"Detailed comprehensive answer about {question}"

    print("\nEvaluating Template A...")
    with mlflow.start_run(run_name="template_a"):
        mlflow.log_param("template", "simple")
        results_a = mlflow.evaluate(
            model=template_a_model,
            data=eval_data,
            model_type="text",
            evaluators="default"
        )

    print("Evaluating Template B...")
    with mlflow.start_run(run_name="template_b"):
        mlflow.log_param("template", "detailed")
        results_b = mlflow.evaluate(
            model=template_b_model,
            data=eval_data,
            model_type="text",
            evaluators="default"
        )

    print(f"\n✓ Template comparison complete")
    print(f"  Compare in MLflow UI: mlflow ui")

    return results_a, results_b


def main():
    """Run all MLflow LLM evaluation examples."""
    print("=" * 60)
    print("MLflow LLM Evaluation Examples")
    print("=" * 60)

    try:
        # Setup
        setup_mlflow()

        # Basic evaluations
        basic_qa_evaluation()
        rag_evaluation_with_context()

        # Custom metrics
        custom_metric_evaluation()

        # Advanced features
        model_comparison()
        llm_judge_evaluation()
        batch_evaluation()
        evaluate_with_artifacts()
        prompt_template_evaluation()

        print("\n" + "=" * 60)
        print("All MLflow evaluations completed successfully!")
        print("=" * 60)

        print("\n📊 MLflow LLM Evaluation Features:")
        print("  • Model Tracking: Version and track all models")
        print("  • Experiment Comparison: Compare multiple runs")
        print("  • Built-in Metrics: Toxicity, relevance, correctness")
        print("  • Custom Metrics: Define your own evaluators")
        print("  • LLM Judge: Use GPT-4 or other LLMs as judges")
        print("  • Artifact Logging: Store datasets, charts, reports")
        print("  • UI Dashboard: Visual exploration of results")
        print("  • Integration: Works with any Python model")

        print("\n💡 Next Steps:")
        print("  1. View results: mlflow ui")
        print("  2. Open browser: http://localhost:5000")
        print("  3. Compare runs, view metrics, download artifacts")
        print("  4. Docs: https://mlflow.org/docs/latest/llms/llm-evaluate/")

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Setup required:")
        print("  1. pip install mlflow openai")
        print("  2. Set OPENAI_API_KEY for LLM judge features")
        print("  3. Run: mlflow ui (to view results)")


if __name__ == "__main__":
    main()
