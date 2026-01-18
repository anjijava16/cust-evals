"""
Weights & Biases Weave Evaluation Example

Weave is W&B's toolkit for tracking, evaluating, and versioning LLM applications.
It provides experiment tracking, evaluation pipelines, artifact logging, and comparison tools.

Installation:
pip install weave

Documentation: https://wandb.me/weave
"""

import os
import weave
from typing import List, Dict, Any
import json


def setup_weave():
    """Initialize Weave with W&B project."""
    # Initialize Weave - this will prompt for W&B login if not authenticated
    project_name = os.getenv("WANDB_PROJECT", "llm-evaluation-examples")

    # Initialize weave tracking
    weave.init(project_name)
    print(f"✓ Weave initialized with project: {project_name}")
    print(f"  View at: https://wandb.ai/{os.getenv('WANDB_ENTITY', 'your-entity')}/{project_name}")


def basic_trace_example():
    """
    Basic tracing with Weave.
    Automatically tracks function calls and their inputs/outputs.
    """
    print("\n=== Basic Trace Example ===")

    # Use @weave.op decorator to automatically track operations
    @weave.op()
    def simple_qa(question: str) -> str:
        """Simple Q&A function that gets traced."""
        answers = {
            "What is AI?": "Artificial Intelligence is the simulation of human intelligence by machines.",
            "What is ML?": "Machine Learning is a subset of AI that learns from data.",
        }
        return answers.get(question, "I don't know the answer to that question.")

    # Call the function - Weave automatically tracks it
    question = "What is AI?"
    answer = simple_qa(question)

    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print("✓ Function call automatically traced by Weave")

    return answer


def model_class_example():
    """
    Create a Model class for structured LLM application tracking.
    Weave Models allow version control of your application logic.
    """
    print("\n=== Model Class Example ===")

    class RAGModel(weave.Model):
        """RAG system as a Weave Model for automatic versioning."""

        model_name: str
        temperature: float

        @weave.op()
        def retrieve(self, query: str) -> List[str]:
            """Simulate document retrieval."""
            # In production, this would query a vector database
            documents = [
                "Machine learning is a method of data analysis that automates analytical model building.",
                "Deep learning is a subset of machine learning using neural networks.",
                "AI systems can learn from experience and improve over time."
            ]
            print(f"  Retrieved {len(documents)} documents")
            return documents

        @weave.op()
        def generate(self, query: str, context: List[str]) -> str:
            """Simulate answer generation."""
            # In production, this would call an LLM API
            answer = f"Based on the context, {query.lower()} refers to techniques in artificial intelligence."
            print(f"  Generated answer: {answer[:50]}...")
            return answer

        @weave.op()
        def predict(self, query: str) -> Dict[str, Any]:
            """Full RAG pipeline."""
            documents = self.retrieve(query)
            answer = self.generate(query, documents)

            return {
                "query": query,
                "answer": answer,
                "context": documents,
                "model": self.model_name,
                "temperature": self.temperature
            }

    # Create model instance
    model = RAGModel(model_name="gpt-4", temperature=0.7)

    # Run prediction - all steps are automatically tracked
    result = model.predict("What is machine learning?")

    print("\n✓ RAG Model prediction tracked:")
    print(f"  Query: {result['query']}")
    print(f"  Answer: {result['answer'][:80]}...")
    print(f"  Context docs: {len(result['context'])}")
    print(f"  Model version automatically saved in Weave")

    return model


def dataset_example():
    """
    Create and manage evaluation datasets in Weave.
    Datasets are versioned and can be reused across evaluations.
    """
    print("\n=== Dataset Management Example ===")

    # Create evaluation dataset
    dataset = weave.Dataset(
        name="qa_evaluation_set",
        rows=[
            {
                "question": "What is artificial intelligence?",
                "expected_answer": "AI is the simulation of human intelligence by machines",
                "category": "definition"
            },
            {
                "question": "What is machine learning?",
                "expected_answer": "ML is a subset of AI that learns from data",
                "category": "definition"
            },
            {
                "question": "What is deep learning?",
                "expected_answer": "Deep learning uses neural networks with multiple layers",
                "category": "definition"
            }
        ]
    )

    # Publish dataset to Weave
    weave.publish(dataset)

    print(f"✓ Dataset created and published:")
    print(f"  Name: {dataset.name}")
    print(f"  Rows: {len(dataset.rows)}")
    print(f"  Categories: {set(row['category'] for row in dataset.rows)}")
    print(f"  Dataset is versioned and reusable")

    return dataset


def custom_evaluator_example():
    """
    Create custom evaluators for your specific needs.
    Evaluators can score predictions on various dimensions.
    """
    print("\n=== Custom Evaluator Example ===")

    @weave.op()
    def accuracy_evaluator(expected: str, actual: str) -> Dict[str, Any]:
        """
        Simple accuracy evaluator.
        Checks if key terms from expected answer appear in actual answer.
        """
        expected_terms = set(expected.lower().split())
        actual_terms = set(actual.lower().split())

        # Calculate overlap
        overlap = expected_terms.intersection(actual_terms)
        score = len(overlap) / len(expected_terms) if expected_terms else 0.0

        return {
            "score": score,
            "passed": score > 0.5,
            "matched_terms": list(overlap),
            "missing_terms": list(expected_terms - actual_terms)
        }

    @weave.op()
    def relevance_evaluator(question: str, answer: str) -> Dict[str, Any]:
        """
        Evaluate answer relevance to question.
        Simple keyword-based approach (in production, use LLM).
        """
        question_keywords = set(question.lower().split())
        answer_keywords = set(answer.lower().split())

        # Check if question keywords appear in answer
        relevant_keywords = question_keywords.intersection(answer_keywords)
        score = len(relevant_keywords) / len(question_keywords) if question_keywords else 0.0

        return {
            "score": score,
            "passed": score > 0.3,
            "relevant_keywords": list(relevant_keywords)
        }

    @weave.op()
    def completeness_evaluator(answer: str, min_length: int = 20) -> Dict[str, Any]:
        """
        Evaluate answer completeness based on length and structure.
        """
        score = min(len(answer) / 100, 1.0)  # Normalize to max length of 100
        has_sufficient_length = len(answer) >= min_length

        return {
            "score": score,
            "passed": has_sufficient_length,
            "length": len(answer),
            "sufficient": has_sufficient_length
        }

    # Test evaluators
    question = "What is artificial intelligence?"
    expected = "AI is the simulation of human intelligence by machines"
    actual = "Artificial intelligence simulates human intelligence using computer systems"

    print(f"Question: {question}")
    print(f"Expected: {expected}")
    print(f"Actual: {actual}\n")

    # Run evaluators
    accuracy_result = accuracy_evaluator(expected, actual)
    relevance_result = relevance_evaluator(question, actual)
    completeness_result = completeness_evaluator(actual)

    print("✓ Evaluation Results:")
    print(f"  Accuracy: {accuracy_result['score']:.2f} - {'PASS' if accuracy_result['passed'] else 'FAIL'}")
    print(f"    Matched terms: {accuracy_result['matched_terms']}")
    print(f"  Relevance: {relevance_result['score']:.2f} - {'PASS' if relevance_result['passed'] else 'FAIL'}")
    print(f"  Completeness: {completeness_result['score']:.2f} - {'PASS' if completeness_result['passed'] else 'FAIL'}")

    return {
        "accuracy": accuracy_result,
        "relevance": relevance_result,
        "completeness": completeness_result
    }


def evaluation_pipeline_example():
    """
    Create a full evaluation pipeline with Weave.
    Combines model, dataset, and evaluators.
    """
    print("\n=== Evaluation Pipeline Example ===")

    # Define a simple model
    @weave.op()
    def qa_model(question: str) -> str:
        """Simple Q&A model."""
        responses = {
            "what is ai": "AI is the simulation of human intelligence by computer systems",
            "what is ml": "Machine learning is a subset of AI that learns from data",
            "what is dl": "Deep learning is a subset of ML using neural networks"
        }

        # Simple keyword matching
        q_lower = question.lower()
        for key, value in responses.items():
            if key in q_lower:
                return value

        return "I don't have enough information to answer that question."

    # Define evaluator
    @weave.op()
    def semantic_similarity_evaluator(expected: str, actual: str) -> Dict[str, float]:
        """
        Simulate semantic similarity evaluation.
        In production, use embeddings or LLM-as-judge.
        """
        # Simple word overlap as proxy for semantic similarity
        expected_words = set(expected.lower().split())
        actual_words = set(actual.lower().split())

        if not expected_words:
            return {"similarity": 0.0}

        overlap = expected_words.intersection(actual_words)
        similarity = len(overlap) / len(expected_words.union(actual_words))

        return {"similarity": similarity}

    # Create evaluation
    evaluation = weave.Evaluation(
        dataset=[
            {"question": "What is AI?", "expected": "AI is machine intelligence"},
            {"question": "What is ML?", "expected": "ML learns from data"},
            {"question": "What is DL?", "expected": "DL uses neural networks"}
        ],
        scorers=[semantic_similarity_evaluator]
    )

    # Run evaluation
    print("Running evaluation pipeline...")
    results = evaluation.evaluate(qa_model)

    print("\n✓ Evaluation completed:")
    print(f"  Test cases: 3")
    print(f"  Evaluator: semantic_similarity_evaluator")
    print(f"  Results tracked in Weave dashboard")

    return results


def experiment_tracking_example():
    """
    Track experiments with different configurations.
    Compare model performance across variations.
    """
    print("\n=== Experiment Tracking Example ===")

    class QAExperiment(weave.Model):
        """Q&A model with configurable parameters."""

        temperature: float
        max_tokens: int
        model_name: str

        @weave.op()
        def predict(self, question: str) -> Dict[str, Any]:
            """Generate answer with tracking."""
            # Simulate LLM call with different parameters
            answer_quality = 0.7 + (self.temperature * 0.2)  # Simulated quality

            return {
                "question": question,
                "answer": f"Answer generated with {self.model_name} at temp {self.temperature}",
                "simulated_quality": answer_quality,
                "config": {
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "model_name": self.model_name
                }
            }

    # Run experiments with different configurations
    experiments = [
        {"temp": 0.3, "tokens": 100, "model": "gpt-4"},
        {"temp": 0.7, "tokens": 100, "model": "gpt-4"},
        {"temp": 0.9, "tokens": 150, "model": "gpt-4"},
    ]

    results = []
    for i, exp in enumerate(experiments, 1):
        print(f"\nExperiment {i}:")
        print(f"  Config: temp={exp['temp']}, tokens={exp['tokens']}, model={exp['model']}")

        model = QAExperiment(
            temperature=exp['temp'],
            max_tokens=exp['tokens'],
            model_name=exp['model']
        )

        result = model.predict("What is the best approach to machine learning?")
        results.append(result)

        print(f"  Quality: {result['simulated_quality']:.2f}")

    print("\n✓ All experiments tracked:")
    print(f"  Total runs: {len(experiments)}")
    print(f"  Parameters automatically logged")
    print(f"  Compare results in Weave UI")

    return results


def prompt_versioning_example():
    """
    Version control for prompts using Weave.
    Track prompt evolution and performance.
    """
    print("\n=== Prompt Versioning Example ===")

    # Define prompt versions
    prompts = {
        "v1": "Answer the question: {question}",
        "v2": "You are a helpful AI assistant. Answer this question accurately: {question}",
        "v3": "You are an expert AI assistant. Provide a clear, concise answer to: {question}\n\nAnswer:"
    }

    @weave.op()
    def generate_with_prompt(question: str, prompt_template: str, version: str) -> Dict[str, Any]:
        """Generate answer using specific prompt version."""
        prompt = prompt_template.format(question=question)

        # Simulate LLM call
        answer = f"This is a response using prompt {version}"

        return {
            "prompt": prompt,
            "answer": answer,
            "prompt_version": version,
            "prompt_length": len(prompt)
        }

    # Test all prompt versions
    question = "What is quantum computing?"
    results = {}

    for version, template in prompts.items():
        result = generate_with_prompt(question, template, version)
        results[version] = result
        print(f"\n{version.upper()}:")
        print(f"  Prompt: {template[:60]}...")
        print(f"  Length: {result['prompt_length']} chars")

    print("\n✓ Prompt versions tracked:")
    print(f"  Versions: {len(prompts)}")
    print(f"  All prompts and outputs logged")
    print(f"  Compare performance in Weave")

    return results


def artifact_logging_example():
    """
    Log artifacts like model outputs, evaluations, and metadata.
    Keep track of important results.
    """
    print("\n=== Artifact Logging Example ===")

    # Create evaluation results
    evaluation_results = {
        "model": "gpt-4-turbo",
        "dataset": "qa_benchmark_v1",
        "metrics": {
            "accuracy": 0.87,
            "f1_score": 0.85,
            "precision": 0.89,
            "recall": 0.83
        },
        "timestamp": "2024-01-18T10:00:00Z",
        "examples": [
            {
                "input": "What is AI?",
                "expected": "Artificial Intelligence",
                "predicted": "AI is artificial intelligence",
                "correct": True
            },
            {
                "input": "What is ML?",
                "expected": "Machine Learning",
                "predicted": "ML is machine learning",
                "correct": True
            }
        ]
    }

    # Publish results as artifact
    artifact = weave.publish(evaluation_results, name="qa_evaluation_results")

    print("✓ Artifacts logged:")
    print(f"  Model: {evaluation_results['model']}")
    print(f"  Metrics:")
    for metric, value in evaluation_results['metrics'].items():
        print(f"    {metric}: {value:.2f}")
    print(f"  Examples: {len(evaluation_results['examples'])}")
    print(f"  Artifact saved and versioned")

    return evaluation_results


def comparison_tools_example():
    """
    Compare different models or configurations.
    Side-by-side comparison of performance.
    """
    print("\n=== Model Comparison Example ===")

    @weave.op()
    def evaluate_model(model_name: str, test_cases: List[Dict]) -> Dict[str, Any]:
        """Evaluate a model on test cases."""
        # Simulate model performance (different scores for different models)
        model_scores = {
            "gpt-4": 0.90,
            "gpt-3.5-turbo": 0.75,
            "claude-2": 0.88
        }

        base_score = model_scores.get(model_name, 0.70)

        results = {
            "model": model_name,
            "total_cases": len(test_cases),
            "scores": {
                "accuracy": base_score,
                "relevance": base_score + 0.02,
                "completeness": base_score - 0.05
            },
            "avg_score": base_score
        }

        return results

    # Compare multiple models
    models_to_compare = ["gpt-4", "gpt-3.5-turbo", "claude-2"]
    test_cases = [
        {"question": "What is AI?", "expected": "Artificial Intelligence"},
        {"question": "What is ML?", "expected": "Machine Learning"},
    ]

    comparison_results = []

    print("Comparing models:")
    for model in models_to_compare:
        result = evaluate_model(model, test_cases)
        comparison_results.append(result)

        print(f"\n  {model}:")
        print(f"    Accuracy: {result['scores']['accuracy']:.2f}")
        print(f"    Relevance: {result['scores']['relevance']:.2f}")
        print(f"    Completeness: {result['scores']['completeness']:.2f}")
        print(f"    Average: {result['avg_score']:.2f}")

    # Find best model
    best_model = max(comparison_results, key=lambda x: x['avg_score'])

    print(f"\n✓ Comparison completed:")
    print(f"  Models compared: {len(models_to_compare)}")
    print(f"  Best performer: {best_model['model']} ({best_model['avg_score']:.2f})")
    print(f"  Detailed comparison in Weave UI")

    return comparison_results


def main():
    """Run all Weave examples."""
    print("=" * 60)
    print("Weights & Biases Weave Evaluation Examples")
    print("=" * 60)

    try:
        # Initialize Weave
        setup_weave()

        # Basic features
        basic_trace_example()
        model_class_example()
        dataset_example()

        # Evaluation
        custom_evaluator_example()
        evaluation_pipeline_example()

        # Advanced features
        experiment_tracking_example()
        prompt_versioning_example()
        artifact_logging_example()
        comparison_tools_example()

        print("\n" + "=" * 60)
        print("All Weave examples completed successfully!")
        print("=" * 60)

        print("\n📊 Weave Key Features:")
        print("  • Automatic Tracing: Track all operations with @weave.op()")
        print("  • Model Versioning: Version control for model logic")
        print("  • Dataset Management: Versioned evaluation datasets")
        print("  • Custom Evaluators: Build your own scoring functions")
        print("  • Evaluation Pipelines: Systematic model evaluation")
        print("  • Experiment Tracking: Compare configurations")
        print("  • Prompt Versioning: Track prompt evolution")
        print("  • Artifact Logging: Store and version results")
        print("  • Comparison Tools: Side-by-side model comparison")
        print("  • Rich UI: Visualize all tracked data")

        print("\n💡 Weave Use Cases:")
        print("  • LLM application development")
        print("  • Model evaluation and comparison")
        print("  • Prompt engineering and testing")
        print("  • RAG system evaluation")
        print("  • A/B testing different configurations")
        print("  • Tracking model performance over time")
        print("  • Debugging LLM applications")
        print("  • Dataset versioning and management")

        print("\n🚀 Getting Started:")
        print("  1. Install: pip install weave")
        print("  2. Login to W&B: wandb login")
        print("  3. Initialize: weave.init('project-name')")
        print("  4. Decorate functions: @weave.op()")
        print("  5. View traces at: https://wandb.ai/")

        print("\n🔗 Integration Benefits:")
        print("  • Seamless W&B integration")
        print("  • Works with any LLM provider")
        print("  • Python-first API")
        print("  • Automatic versioning")
        print("  • Collaborative evaluation")
        print("  • Production-ready tracking")

    except Exception as e:
        print(f"\nNote: {e}")
        print("\nSetup required:")
        print("  1. Install Weave: pip install weave")
        print("  2. Sign up at https://wandb.ai/")
        print("  3. Login: wandb login")
        print("  4. Set project: export WANDB_PROJECT='your-project'")
        print("\nThese examples demonstrate Weave's capabilities.")


if __name__ == "__main__":
    main()
