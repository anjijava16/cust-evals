"""
Google Vertex AI Gen AI Evaluation Example

This example demonstrates using Google's Vertex AI Gen AI Evaluation service
for LLM evaluation with various built-in metrics.

Installation:
pip install google-cloud-aiplatform

Documentation: https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/evaluation
"""

import os
from google.cloud import aiplatform
from vertexai.preview.evaluation import EvalTask, MetricPromptTemplateExamples
import vertexai


def setup_vertex_ai():
    """Initialize Vertex AI with project settings."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")

    vertexai.init(project=project_id, location=location)
    return project_id, location


def evaluate_summarization():
    """
    Evaluate text summarization quality.
    Uses metrics like ROUGE, coherence, and fluency.
    """
    print("\n=== Summarization Evaluation ===")

    project_id, location = setup_vertex_ai()

    # Sample data
    eval_dataset = [
        {
            "reference": "The quick brown fox jumps over the lazy dog. This is a common English pangram.",
            "prediction": "A brown fox jumps over a dog.",
            "context": "The quick brown fox jumps over the lazy dog. This is a common English pangram used to test fonts."
        }
    ]

    # Create evaluation task
    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[
            "rouge_1",
            "rouge_2",
            "rouge_l",
            "bleu",
            "coherence",
            "fluency"
        ],
        experiment="summarization-eval"
    )

    # Run evaluation
    result = eval_task.evaluate(
        model="gemini-1.5-pro",
        prompt_template="Summarize the following: {context}"
    )

    print(f"Evaluation Results:")
    print(f"  ROUGE-1: {result.summary_metrics.get('rouge_1', 'N/A')}")
    print(f"  ROUGE-L: {result.summary_metrics.get('rouge_l', 'N/A')}")
    print(f"  BLEU: {result.summary_metrics.get('bleu', 'N/A')}")
    print(f"  Coherence: {result.summary_metrics.get('coherence', 'N/A')}")
    print(f"  Fluency: {result.summary_metrics.get('fluency', 'N/A')}")

    return result


def evaluate_question_answering():
    """
    Evaluate question-answering tasks.
    Measures accuracy, relevance, and completeness.
    """
    print("\n=== Question Answering Evaluation ===")

    project_id, location = setup_vertex_ai()

    # Sample Q&A data
    eval_dataset = [
        {
            "question": "What is the capital of France?",
            "prediction": "The capital of France is Paris.",
            "reference": "Paris",
            "context": "France is a country in Western Europe. Its capital city is Paris."
        },
        {
            "question": "Who wrote Romeo and Juliet?",
            "prediction": "William Shakespeare wrote Romeo and Juliet.",
            "reference": "William Shakespeare",
            "context": "Romeo and Juliet is a tragedy written by William Shakespeare."
        }
    ]

    # Create evaluation task
    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[
            "exact_match",
            "f1_score",
            "question_answering_quality",
            "question_answering_relevance",
            "question_answering_helpfulness"
        ],
        experiment="qa-eval"
    )

    # Run evaluation
    result = eval_task.evaluate()

    print(f"Evaluation Results:")
    print(f"  Exact Match: {result.summary_metrics.get('exact_match', 'N/A')}")
    print(f"  F1 Score: {result.summary_metrics.get('f1_score', 'N/A')}")
    print(f"  QA Quality: {result.summary_metrics.get('question_answering_quality', 'N/A')}")

    return result


def evaluate_groundedness():
    """
    Evaluate if responses are grounded in provided context.
    Critical for preventing hallucinations in RAG systems.
    """
    print("\n=== Groundedness Evaluation ===")

    project_id, location = setup_vertex_ai()

    eval_dataset = [
        {
            "context": "Python is a high-level programming language. It was created by Guido van Rossum in 1991.",
            "prediction": "Python is a programming language created by Guido van Rossum in 1991."
        },
        {
            "context": "The Earth orbits the Sun once every 365.25 days.",
            "prediction": "The Earth takes approximately one year to orbit the Sun, which is about 365.25 days."
        }
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=["groundedness"],
        experiment="groundedness-eval"
    )

    result = eval_task.evaluate(model="gemini-1.5-pro")

    print(f"Groundedness Score: {result.summary_metrics.get('groundedness', 'N/A')}")
    print("(Higher score means response is well-grounded in context)")

    return result


def evaluate_safety():
    """
    Evaluate content for safety issues.
    Checks for harmful, toxic, or inappropriate content.
    """
    print("\n=== Safety Evaluation ===")

    project_id, location = setup_vertex_ai()

    eval_dataset = [
        {
            "prediction": "I'd be happy to help you with your programming question."
        },
        {
            "prediction": "Thank you for reaching out. Let me provide some information."
        }
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[
            "safety"
        ],
        experiment="safety-eval"
    )

    result = eval_task.evaluate()

    print(f"Safety Evaluation Results:")
    print(f"  Safety Score: {result.summary_metrics.get('safety', 'N/A')}")

    return result


def evaluate_instruction_following():
    """
    Evaluate how well model follows given instructions.
    Important for task-oriented applications.
    """
    print("\n=== Instruction Following Evaluation ===")

    project_id, location = setup_vertex_ai()

    eval_dataset = [
        {
            "instruction": "List three benefits of exercise in bullet points.",
            "prediction": "• Improves cardiovascular health\n• Strengthens muscles\n• Enhances mental well-being"
        }
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=["instruction_following"],
        experiment="instruction-eval"
    )

    result = eval_task.evaluate(model="gemini-1.5-pro")

    print(f"Instruction Following Score: {result.summary_metrics.get('instruction_following', 'N/A')}")

    return result


def evaluate_pairwise_comparison():
    """
    Compare two model outputs and determine which is better.
    Useful for A/B testing and model comparison.
    """
    print("\n=== Pairwise Comparison Evaluation ===")

    project_id, location = setup_vertex_ai()

    eval_dataset = [
        {
            "prompt": "Explain machine learning",
            "baseline_prediction": "Machine learning is AI.",
            "candidate_prediction": "Machine learning is a subset of AI that enables systems to learn from data and improve performance without explicit programming."
        }
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=["pairwise_question_answering_quality"],
        experiment="pairwise-eval"
    )

    result = eval_task.evaluate()

    print(f"Pairwise Comparison Results:")
    print(f"  Preferred: {result.summary_metrics.get('pairwise_winner', 'N/A')}")
    print(f"  Quality Score: {result.summary_metrics.get('pairwise_question_answering_quality', 'N/A')}")

    return result


def evaluate_rag_system():
    """
    Comprehensive RAG (Retrieval-Augmented Generation) evaluation.
    Evaluates both retrieval and generation components.
    """
    print("\n=== RAG System Evaluation ===")

    project_id, location = setup_vertex_ai()

    eval_dataset = [
        {
            "question": "What are the health benefits of regular exercise?",
            "context": "Regular exercise provides numerous health benefits including improved cardiovascular health, stronger muscles, better mood, and weight management.",
            "prediction": "Exercise improves heart health, builds muscle strength, enhances mental well-being, and helps maintain healthy weight.",
            "reference": "Exercise benefits include cardiovascular health, muscle strength, mental health, and weight management."
        }
    ]

    # Evaluate multiple RAG-specific metrics
    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[
            "groundedness",                     # Is answer grounded in context?
            "question_answering_quality",       # Overall quality
            "question_answering_relevance",     # Relevance to question
            "question_answering_helpfulness",   # Helpfulness of answer
            "coherence",                        # Internal consistency
            "fluency"                           # Language quality
        ],
        experiment="rag-eval"
    )

    result = eval_task.evaluate(model="gemini-1.5-pro")

    print(f"\nRAG Evaluation Results:")
    for metric, score in result.summary_metrics.items():
        print(f"  {metric}: {score}")

    return result


def evaluate_with_custom_metric():
    """
    Create and use custom evaluation metrics.
    Demonstrates flexibility for domain-specific needs.
    """
    print("\n=== Custom Metric Evaluation ===")

    project_id, location = setup_vertex_ai()

    # Define custom metric using prompt template
    custom_metric_prompt = """
    Evaluate if the response demonstrates professional communication.

    Response: {prediction}

    Rate from 1-5 where:
    1 = Very unprofessional
    5 = Highly professional

    Consider: tone, clarity, courtesy, and appropriateness.
    Provide score and brief explanation.
    """

    eval_dataset = [
        {
            "prediction": "Thank you for contacting us. I'll be happy to assist you with your inquiry."
        }
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[
            {
                "metric_name": "professionalism",
                "metric_prompt_template": custom_metric_prompt
            }
        ],
        experiment="custom-metric-eval"
    )

    result = eval_task.evaluate(model="gemini-1.5-pro")

    print(f"Custom Metric Results:")
    print(f"  Professionalism Score: {result.summary_metrics.get('professionalism', 'N/A')}")

    return result


def batch_evaluation():
    """
    Evaluate multiple examples in batch.
    Demonstrates scalable evaluation approach.
    """
    print("\n=== Batch Evaluation ===")

    project_id, location = setup_vertex_ai()

    # Larger dataset
    eval_dataset = [
        {
            "question": f"What is example {i}?",
            "prediction": f"This is example number {i}.",
            "reference": f"Example {i}"
        }
        for i in range(1, 11)
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[
            "question_answering_quality",
            "question_answering_relevance"
        ],
        experiment="batch-eval"
    )

    result = eval_task.evaluate(model="gemini-1.5-pro")

    print(f"\nBatch Evaluation Results ({len(eval_dataset)} examples):")
    print(f"  Average QA Quality: {result.summary_metrics.get('question_answering_quality', 'N/A')}")
    print(f"  Average Relevance: {result.summary_metrics.get('question_answering_relevance', 'N/A')}")

    # Show per-example results
    print(f"\n  Evaluated {result.metrics_table.shape[0]} examples")

    return result


def evaluate_with_gemini():
    """
    Direct evaluation using Gemini models.
    Alternative approach without EvalTask framework.
    """
    print("\n=== Direct Gemini Evaluation ===")

    from vertexai.generative_models import GenerativeModel

    project_id, location = setup_vertex_ai()

    model = GenerativeModel("gemini-1.5-pro")

    # Evaluation prompt
    response_to_evaluate = "Machine learning is a subset of AI that learns from data."

    prompt = f"""
    Evaluate the following response for accuracy and completeness on a scale of 1-5.

    Response: {response_to_evaluate}

    Provide:
    - Accuracy score (1-5)
    - Completeness score (1-5)
    - Brief explanation
    """

    response = model.generate_content(prompt)
    print(f"\nGemini Evaluation:\n{response.text}")

    return response


def main():
    """Run all Google Vertex AI evaluation examples."""
    print("=" * 60)
    print("Google Vertex AI Gen AI Evaluation Examples")
    print("=" * 60)

    try:
        # Basic evaluations
        evaluate_summarization()
        evaluate_question_answering()
        evaluate_groundedness()
        evaluate_safety()
        evaluate_instruction_following()

        # Advanced evaluations
        evaluate_pairwise_comparison()
        evaluate_rag_system()
        evaluate_with_custom_metric()
        batch_evaluation()
        evaluate_with_gemini()

        print("\n" + "=" * 60)
        print("All Vertex AI evaluations completed successfully!")
        print("=" * 60)

        print("\n📊 Vertex AI Evaluation Capabilities:")
        print("  • Summarization: ROUGE, BLEU, coherence, fluency")
        print("  • Q&A: Exact match, F1, quality, relevance, helpfulness")
        print("  • RAG: Groundedness, context relevance")
        print("  • Safety: Toxicity, harm detection")
        print("  • Task Compliance: Instruction following")
        print("  • Comparison: Pairwise evaluation, A/B testing")
        print("  • Custom: Domain-specific metrics")

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Setup required:")
        print("  1. Set GOOGLE_CLOUD_PROJECT environment variable")
        print("  2. Set GOOGLE_CLOUD_REGION (optional, defaults to us-central1)")
        print("  3. Authenticate: gcloud auth application-default login")
        print("  4. Install: pip install google-cloud-aiplatform")


if __name__ == "__main__":
    main()
