"""
RAGAS (Retrieval-Augmented Generation Assessment) Framework Example

RAGAS is specifically designed for evaluating RAG (Retrieval-Augmented Generation) pipelines.
It provides metrics for both retrieval and generation quality.

Installation:
pip install ragas langchain openai datasets

Documentation: https://docs.ragas.io/
"""

import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
    answer_similarity,
    answer_correctness
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def setup_ragas_models():
    """Initialize models for RAGAS evaluation."""
    llm = ChatOpenAI(
        model="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    embeddings = OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return llm, embeddings


def basic_rag_evaluation():
    """
    Basic RAG evaluation with core metrics.
    Evaluates both retrieval quality and generation quality.
    """
    print("\n=== Basic RAG Evaluation ===")

    # Sample RAG outputs
    data = {
        "question": [
            "What is the capital of France?",
            "Who invented the telephone?",
            "What is photosynthesis?"
        ],
        "answer": [
            "The capital of France is Paris.",
            "Alexander Graham Bell invented the telephone in 1876.",
            "Photosynthesis is the process by which plants use sunlight to convert CO2 and water into glucose and oxygen."
        ],
        "contexts": [
            ["Paris is the capital and largest city of France."],
            ["The telephone was invented by Alexander Graham Bell in 1876."],
            ["Photosynthesis is a process used by plants to convert light energy into chemical energy."]
        ],
        "ground_truth": [
            "Paris",
            "Alexander Graham Bell",
            "Photosynthesis is the process where plants convert sunlight, water, and CO2 into glucose and oxygen."
        ]
    }

    # Convert to RAGAS dataset format
    dataset = Dataset.from_dict(data)

    # Define metrics to evaluate
    metrics = [
        faithfulness,           # Measures factual consistency with context
        answer_relevancy,       # Measures relevance to the question
        context_recall,         # Measures retrieval quality
        context_precision,      # Measures ranking quality
        answer_correctness      # Measures correctness vs ground truth
    ]

    # Run evaluation
    results = evaluate(
        dataset,
        metrics=metrics
    )

    print(f"\nEvaluation Results:")
    print(f"Faithfulness: {results['faithfulness']:.3f}")
    print(f"Answer Relevancy: {results['answer_relevancy']:.3f}")
    print(f"Context Recall: {results['context_recall']:.3f}")
    print(f"Context Precision: {results['context_precision']:.3f}")
    print(f"Answer Correctness: {results['answer_correctness']:.3f}")

    return results


def faithfulness_evaluation():
    """
    Evaluate faithfulness - whether answers are grounded in retrieved context.
    This is crucial for preventing hallucinations in RAG systems.
    """
    print("\n=== Faithfulness Evaluation ===")

    data = {
        "question": ["What are the benefits of regular exercise?"],
        "answer": [
            "Regular exercise improves cardiovascular health, strengthens muscles, "
            "boosts mental well-being, and helps maintain a healthy weight."
        ],
        "contexts": [[
            "Exercise has numerous health benefits including improved heart health, "
            "stronger muscles, better mood, and weight management."
        ]]
    }

    dataset = Dataset.from_dict(data)

    # Evaluate only faithfulness
    results = evaluate(
        dataset,
        metrics=[faithfulness]
    )

    print(f"Faithfulness Score: {results['faithfulness']:.3f}")
    print("(Score closer to 1.0 means answer is well-grounded in context)")

    return results


def context_quality_evaluation():
    """
    Evaluate retrieval quality using context precision and recall.
    - Precision: Are retrieved contexts relevant?
    - Recall: Are all necessary contexts retrieved?
    """
    print("\n=== Context Quality Evaluation ===")

    data = {
        "question": [
            "What are the main features of Python programming language?"
        ],
        "answer": [
            "Python is known for its simple syntax, dynamic typing, extensive libraries, "
            "and strong community support."
        ],
        "contexts": [
            [
                "Python is a high-level programming language with simple, readable syntax.",
                "Python features dynamic typing and automatic memory management.",
                "Python has a vast ecosystem of libraries and frameworks.",
                "Python has a large and active developer community."
            ]
        ],
        "ground_truth": [
            "Python features include simple syntax, dynamic typing, extensive libraries, and strong community."
        ]
    }

    dataset = Dataset.from_dict(data)

    # Evaluate context quality
    results = evaluate(
        dataset,
        metrics=[context_precision, context_recall]
    )

    print(f"Context Precision: {results['context_precision']:.3f}")
    print(f"Context Recall: {results['context_recall']:.3f}")

    return results


def answer_quality_evaluation():
    """
    Evaluate answer quality using relevancy and correctness metrics.
    - Relevancy: Does the answer address the question?
    - Correctness: Is the answer factually correct?
    """
    print("\n=== Answer Quality Evaluation ===")

    data = {
        "question": [
            "How does machine learning differ from traditional programming?"
        ],
        "answer": [
            "Machine learning allows systems to learn patterns from data automatically, "
            "while traditional programming requires explicit rule-based instructions."
        ],
        "contexts": [
            [
                "Traditional programming uses explicit rules coded by developers.",
                "Machine learning systems learn patterns from training data.",
                "ML models can improve performance with more data."
            ]
        ],
        "ground_truth": [
            "Machine learning learns from data, traditional programming uses explicit rules."
        ]
    }

    dataset = Dataset.from_dict(data)

    # Evaluate answer quality
    results = evaluate(
        dataset,
        metrics=[answer_relevancy, answer_correctness, answer_similarity]
    )

    print(f"Answer Relevancy: {results['answer_relevancy']:.3f}")
    print(f"Answer Correctness: {results['answer_correctness']:.3f}")
    print(f"Answer Similarity: {results['answer_similarity']:.3f}")

    return results


def multi_context_evaluation():
    """
    Evaluate RAG with multiple retrieved contexts.
    Tests how well the system handles multiple sources.
    """
    print("\n=== Multi-Context RAG Evaluation ===")

    data = {
        "question": [
            "What are the environmental and economic benefits of renewable energy?"
        ],
        "answer": [
            "Renewable energy reduces greenhouse gas emissions and air pollution, "
            "while also creating jobs and reducing energy costs over time."
        ],
        "contexts": [
            [
                "Renewable energy sources like solar and wind produce no greenhouse gases.",
                "Air pollution from fossil fuels causes respiratory diseases.",
                "The renewable energy sector has created millions of jobs globally.",
                "Solar and wind energy costs have decreased significantly.",
                "Long-term renewable energy is cheaper than fossil fuels."
            ]
        ],
        "ground_truth": [
            "Renewable energy reduces emissions, creates jobs, and lowers long-term costs."
        ]
    }

    dataset = Dataset.from_dict(data)

    # Full evaluation with all metrics
    results = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
            answer_correctness
        ]
    )

    print("\nComprehensive Results:")
    for metric, score in results.items():
        print(f"  {metric}: {score:.3f}")

    return results


def comparative_rag_evaluation():
    """
    Compare multiple RAG systems or configurations.
    Useful for A/B testing different retrieval strategies.
    """
    print("\n=== Comparative RAG Evaluation ===")

    # System A: Simple retrieval
    system_a = {
        "question": ["What causes climate change?"],
        "answer": ["Climate change is caused by greenhouse gas emissions."],
        "contexts": [["Greenhouse gases trap heat in the atmosphere."]],
        "ground_truth": ["Climate change is primarily caused by human greenhouse gas emissions."]
    }

    # System B: Enhanced retrieval with more context
    system_b = {
        "question": ["What causes climate change?"],
        "answer": [
            "Climate change is primarily caused by human activities that release greenhouse gases, "
            "particularly burning fossil fuels and deforestation."
        ],
        "contexts": [[
            "Human activities release greenhouse gases into the atmosphere.",
            "Burning fossil fuels is the main source of CO2 emissions.",
            "Deforestation reduces CO2 absorption by trees."
        ]],
        "ground_truth": ["Climate change is primarily caused by human greenhouse gas emissions."]
    }

    # Evaluate both systems
    dataset_a = Dataset.from_dict(system_a)
    dataset_b = Dataset.from_dict(system_b)

    results_a = evaluate(dataset_a, metrics=[faithfulness, answer_correctness])
    results_b = evaluate(dataset_b, metrics=[faithfulness, answer_correctness])

    print("\nSystem A Results:")
    print(f"  Faithfulness: {results_a['faithfulness']:.3f}")
    print(f"  Correctness: {results_a['answer_correctness']:.3f}")

    print("\nSystem B Results:")
    print(f"  Faithfulness: {results_b['faithfulness']:.3f}")
    print(f"  Correctness: {results_b['answer_correctness']:.3f}")

    return results_a, results_b


def batch_evaluation_from_file():
    """
    Example of batch evaluation from a larger dataset.
    Useful for evaluating production RAG systems at scale.
    """
    print("\n=== Batch Evaluation Example ===")

    # Simulate larger dataset
    questions = [
        "What is quantum computing?",
        "How do neural networks work?",
        "What is blockchain technology?",
        "Explain natural language processing",
        "What is cloud computing?"
    ]

    answers = [
        "Quantum computing uses quantum bits to perform complex calculations.",
        "Neural networks are computing systems inspired by biological neural networks.",
        "Blockchain is a distributed ledger technology for secure transactions.",
        "NLP enables computers to understand and generate human language.",
        "Cloud computing delivers computing services over the internet."
    ]

    contexts = [
        ["Quantum computers use qubits which can exist in multiple states."],
        ["Neural networks consist of interconnected nodes that process information."],
        ["Blockchain uses cryptography to create immutable transaction records."],
        ["NLP combines linguistics and machine learning to process language."],
        ["Cloud services include storage, computing power, and applications."]
    ]

    ground_truths = [
        "Quantum computing uses quantum mechanics for computation.",
        "Neural networks are inspired by the brain and learn from data.",
        "Blockchain is a decentralized, secure ledger system.",
        "NLP helps computers understand and generate human language.",
        "Cloud computing provides on-demand computing resources via internet."
    ]

    data = {
        "question": questions,
        "answer": answers,
        "contexts": [[ctx] for ctx in contexts],
        "ground_truth": ground_truths
    }

    dataset = Dataset.from_dict(data)

    # Run comprehensive evaluation
    results = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, answer_correctness]
    )

    print(f"\nBatch Evaluation Results ({len(questions)} samples):")
    print(f"  Average Faithfulness: {results['faithfulness']:.3f}")
    print(f"  Average Answer Relevancy: {results['answer_relevancy']:.3f}")
    print(f"  Average Answer Correctness: {results['answer_correctness']:.3f}")

    return results


def main():
    """Run all RAGAS evaluation examples."""
    print("=" * 60)
    print("RAGAS RAG Evaluation Framework Examples")
    print("=" * 60)

    try:
        # Basic evaluations
        basic_rag_evaluation()
        faithfulness_evaluation()
        context_quality_evaluation()
        answer_quality_evaluation()

        # Advanced evaluations
        multi_context_evaluation()
        comparative_rag_evaluation()
        batch_evaluation_from_file()

        print("\n" + "=" * 60)
        print("All RAGAS evaluations completed successfully!")
        print("=" * 60)

        print("\n📊 RAGAS Metrics Summary:")
        print("  • Faithfulness: Factual consistency with retrieved context")
        print("  • Answer Relevancy: How well answer addresses the question")
        print("  • Context Precision: Relevance of retrieved contexts")
        print("  • Context Recall: Coverage of necessary information")
        print("  • Answer Correctness: Accuracy vs ground truth")

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Make sure you have set OPENAI_API_KEY environment variable")
        print("Install requirements: pip install ragas langchain-openai datasets")


if __name__ == "__main__":
    main()
