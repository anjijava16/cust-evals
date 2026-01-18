"""
RAGalyst Evaluation Framework Example

RAGalyst provides comprehensive RAG pipeline analysis and evaluation.
Focuses on component-level analysis and bottleneck identification.

Installation:
pip install ragalyst pandas

Documentation: https://github.com/ragalyst/ragalyst
"""

import os
import time
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
import pandas as pd


@dataclass
class RetrievalMetrics:
    """Metrics for retrieval component."""
    precision: float
    recall: float
    f1_score: float
    mrr: float  # Mean Reciprocal Rank
    latency_ms: float
    num_retrieved: int


@dataclass
class GenerationMetrics:
    """Metrics for generation component."""
    relevance: float
    faithfulness: float
    coherence: float
    latency_ms: float
    token_count: int


@dataclass
class EndToEndMetrics:
    """End-to-end RAG pipeline metrics."""
    total_latency_ms: float
    answer_quality: float
    context_utilization: float
    success_rate: float


@dataclass
class RAGalystReport:
    """Comprehensive RAG analysis report."""
    retrieval: RetrievalMetrics
    generation: GenerationMetrics
    end_to_end: EndToEndMetrics
    bottlenecks: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class RAGalystEvaluator:
    """RAGalyst evaluator for RAG pipeline analysis."""

    def __init__(self):
        self.traces = []

    def evaluate_retrieval(
        self,
        query: str,
        retrieved_docs: List[str],
        relevant_docs: List[str],
        latency_ms: float
    ) -> RetrievalMetrics:
        """
        Evaluate retrieval component.
        Measures precision, recall, and performance.
        """
        retrieved_set = set(retrieved_docs)
        relevant_set = set(relevant_docs)

        true_positives = len(retrieved_set & relevant_set)
        retrieved_count = len(retrieved_set)
        relevant_count = len(relevant_set)

        precision = true_positives / retrieved_count if retrieved_count > 0 else 0
        recall = true_positives / relevant_count if relevant_count > 0 else 0
        f1 = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0 else 0
        )

        # Calculate MRR (Mean Reciprocal Rank)
        mrr = 0.0
        for i, doc in enumerate(retrieved_docs, 1):
            if doc in relevant_set:
                mrr = 1.0 / i
                break

        return RetrievalMetrics(
            precision=precision,
            recall=recall,
            f1_score=f1,
            mrr=mrr,
            latency_ms=latency_ms,
            num_retrieved=retrieved_count
        )

    def evaluate_generation(
        self,
        query: str,
        contexts: List[str],
        generated_answer: str,
        latency_ms: float
    ) -> GenerationMetrics:
        """
        Evaluate generation component.
        Measures answer quality and performance.
        """
        # Relevance: Does answer address query?
        query_words = set(query.lower().split())
        answer_words = set(generated_answer.lower().split())
        relevance = len(query_words & answer_words) / len(query_words) if query_words else 0

        # Faithfulness: Is answer grounded in contexts?
        context_words = set()
        for ctx in contexts:
            context_words.update(ctx.lower().split())
        faithfulness = len(answer_words & context_words) / len(answer_words) if answer_words else 0

        # Coherence: Simple length-based heuristic
        coherence = min(len(generated_answer.split()) / 50, 1.0)

        token_count = len(generated_answer.split())

        return GenerationMetrics(
            relevance=relevance,
            faithfulness=faithfulness,
            coherence=coherence,
            latency_ms=latency_ms,
            token_count=token_count
        )

    def analyze_pipeline(
        self,
        retrieval_metrics: RetrievalMetrics,
        generation_metrics: GenerationMetrics
    ) -> RAGalystReport:
        """
        Comprehensive pipeline analysis.
        Identifies bottlenecks and provides recommendations.
        """
        total_latency = retrieval_metrics.latency_ms + generation_metrics.latency_ms

        # Calculate end-to-end metrics
        answer_quality = (
            generation_metrics.relevance * 0.4 +
            generation_metrics.faithfulness * 0.4 +
            generation_metrics.coherence * 0.2
        )

        context_utilization = (
            retrieval_metrics.f1_score * 0.5 +
            generation_metrics.faithfulness * 0.5
        )

        success_rate = 1.0 if answer_quality > 0.7 else 0.0

        end_to_end = EndToEndMetrics(
            total_latency_ms=total_latency,
            answer_quality=answer_quality,
            context_utilization=context_utilization,
            success_rate=success_rate
        )

        # Identify bottlenecks
        bottlenecks = []
        recommendations = []

        if retrieval_metrics.precision < 0.7:
            bottlenecks.append("Low retrieval precision")
            recommendations.append("Improve document ranking or filtering")

        if retrieval_metrics.recall < 0.7:
            bottlenecks.append("Low retrieval recall")
            recommendations.append("Increase number of retrieved documents or improve indexing")

        if retrieval_metrics.latency_ms > 1000:
            bottlenecks.append("High retrieval latency")
            recommendations.append("Optimize vector search or add caching")

        if generation_metrics.faithfulness < 0.7:
            bottlenecks.append("Low generation faithfulness")
            recommendations.append("Improve prompt engineering or use stronger grounding instructions")

        if generation_metrics.latency_ms > 2000:
            bottlenecks.append("High generation latency")
            recommendations.append("Use faster model or reduce context length")

        return RAGalystReport(
            retrieval=retrieval_metrics,
            generation=generation_metrics,
            end_to_end=end_to_end,
            bottlenecks=bottlenecks,
            recommendations=recommendations
        )


def basic_pipeline_analysis():
    """
    Basic RAG pipeline analysis.
    Demonstrates core evaluation workflow.
    """
    print("\n=== Basic Pipeline Analysis ===")

    evaluator = RAGalystEvaluator()

    query = "What are the benefits of renewable energy?"

    # Simulate retrieval
    retrieved_docs = [
        "Renewable energy reduces carbon emissions",
        "Solar and wind power are renewable sources",
        "Renewable energy creates jobs"
    ]
    relevant_docs = [
        "Renewable energy reduces carbon emissions",
        "Renewable energy creates jobs"
    ]
    retrieval_latency = 150  # ms

    # Simulate generation
    contexts = retrieved_docs
    generated_answer = "Renewable energy offers benefits like reduced carbon emissions and job creation."
    generation_latency = 800  # ms

    # Evaluate components
    retrieval_metrics = evaluator.evaluate_retrieval(
        query, retrieved_docs, relevant_docs, retrieval_latency
    )

    generation_metrics = evaluator.evaluate_generation(
        query, contexts, generated_answer, generation_latency
    )

    # Analyze pipeline
    report = evaluator.analyze_pipeline(retrieval_metrics, generation_metrics)

    print(f"Query: {query}\n")
    print("Retrieval Metrics:")
    print(f"  Precision: {retrieval_metrics.precision:.3f}")
    print(f"  Recall: {retrieval_metrics.recall:.3f}")
    print(f"  F1 Score: {retrieval_metrics.f1_score:.3f}")
    print(f"  Latency: {retrieval_metrics.latency_ms}ms")

    print("\nGeneration Metrics:")
    print(f"  Relevance: {generation_metrics.relevance:.3f}")
    print(f"  Faithfulness: {generation_metrics.faithfulness:.3f}")
    print(f"  Latency: {generation_metrics.latency_ms}ms")

    print("\nEnd-to-End:")
    print(f"  Total Latency: {report.end_to_end.total_latency_ms}ms")
    print(f"  Answer Quality: {report.end_to_end.answer_quality:.3f}")

    if report.bottlenecks:
        print("\n⚠️  Bottlenecks:")
        for bottleneck in report.bottlenecks:
            print(f"  • {bottleneck}")

    if report.recommendations:
        print("\n💡 Recommendations:")
        for rec in report.recommendations:
            print(f"  • {rec}")

    return report


def component_comparison():
    """
    Compare different retrieval or generation strategies.
    Helps identify best configurations.
    """
    print("\n=== Component Comparison ===")

    evaluator = RAGalystEvaluator()

    query = "How does machine learning work?"
    relevant_docs = ["ML learns from data", "ML uses algorithms"]

    # Strategy A: Retrieve few documents
    docs_a = ["ML learns from data"]
    metrics_a = evaluator.evaluate_retrieval(query, docs_a, relevant_docs, 100)

    # Strategy B: Retrieve many documents
    docs_b = ["ML learns from data", "ML uses algorithms", "ML improves with more data"]
    metrics_b = evaluator.evaluate_retrieval(query, docs_b, relevant_docs, 200)

    print("Retrieval Strategy Comparison:")
    print("\nStrategy A (Few docs):")
    print(f"  Precision: {metrics_a.precision:.3f}")
    print(f"  Recall: {metrics_a.recall:.3f}")
    print(f"  F1: {metrics_a.f1_score:.3f}")
    print(f"  Latency: {metrics_a.latency_ms}ms")

    print("\nStrategy B (More docs):")
    print(f"  Precision: {metrics_b.precision:.3f}")
    print(f"  Recall: {metrics_b.recall:.3f}")
    print(f"  F1: {metrics_b.f1_score:.3f}")
    print(f"  Latency: {metrics_b.latency_ms}ms")

    better = "B" if metrics_b.f1_score > metrics_a.f1_score else "A"
    print(f"\n✓ Better Strategy: {better}")

    return metrics_a, metrics_b


def latency_profiling():
    """
    Profile latency across pipeline stages.
    Identifies performance bottlenecks.
    """
    print("\n=== Latency Profiling ===")

    # Simulate different latency profiles
    profiles = [
        {
            "name": "Fast Pipeline",
            "retrieval_ms": 50,
            "generation_ms": 300
        },
        {
            "name": "Slow Retrieval",
            "retrieval_ms": 2000,
            "generation_ms": 300
        },
        {
            "name": "Slow Generation",
            "retrieval_ms": 50,
            "generation_ms": 5000
        }
    ]

    for profile in profiles:
        total = profile["retrieval_ms"] + profile["generation_ms"]
        retrieval_pct = (profile["retrieval_ms"] / total) * 100
        generation_pct = (profile["generation_ms"] / total) * 100

        print(f"\n{profile['name']}:")
        print(f"  Retrieval: {profile['retrieval_ms']}ms ({retrieval_pct:.1f}%)")
        print(f"  Generation: {profile['generation_ms']}ms ({generation_pct:.1f}%)")
        print(f"  Total: {total}ms")

        if profile["retrieval_ms"] > 1000:
            print(f"  ⚠️  Retrieval bottleneck detected")
        if profile["generation_ms"] > 3000:
            print(f"  ⚠️  Generation bottleneck detected")


def quality_score_breakdown():
    """
    Break down quality scores by component.
    Helps understand what impacts overall quality.
    """
    print("\n=== Quality Score Breakdown ===")

    evaluator = RAGalystEvaluator()

    test_cases = [
        {
            "name": "High Quality",
            "relevance": 0.9,
            "faithfulness": 0.95,
            "coherence": 0.85
        },
        {
            "name": "Low Faithfulness",
            "relevance": 0.9,
            "faithfulness": 0.4,
            "coherence": 0.85
        },
        {
            "name": "Low Relevance",
            "relevance": 0.3,
            "faithfulness": 0.9,
            "coherence": 0.85
        }
    ]

    for case in test_cases:
        overall = (
            case["relevance"] * 0.4 +
            case["faithfulness"] * 0.4 +
            case["coherence"] * 0.2
        )

        print(f"\n{case['name']}:")
        print(f"  Relevance: {case['relevance']:.2f} (40% weight)")
        print(f"  Faithfulness: {case['faithfulness']:.2f} (40% weight)")
        print(f"  Coherence: {case['coherence']:.2f} (20% weight)")
        print(f"  Overall Quality: {overall:.2f}")

        if overall < 0.7:
            print(f"  ⚠️  Below quality threshold")


def batch_pipeline_evaluation():
    """
    Evaluate multiple queries through the pipeline.
    Aggregates metrics across dataset.
    """
    print("\n=== Batch Pipeline Evaluation ===")

    evaluator = RAGalystEvaluator()

    # Simulate batch evaluation
    results = []

    for i in range(10):
        query = f"Query {i}"
        retrieved = [f"Doc {i}.{j}" for j in range(3)]
        relevant = [f"Doc {i}.0", f"Doc {i}.1"]

        metrics = evaluator.evaluate_retrieval(
            query, retrieved, relevant, 100 + i * 10
        )
        results.append(metrics)

    # Calculate aggregates
    avg_precision = sum(m.precision for m in results) / len(results)
    avg_recall = sum(m.recall for m in results) / len(results)
    avg_f1 = sum(m.f1_score for m in results) / len(results)
    avg_latency = sum(m.latency_ms for m in results) / len(results)

    print(f"Batch Results ({len(results)} queries):")
    print(f"  Average Precision: {avg_precision:.3f}")
    print(f"  Average Recall: {avg_recall:.3f}")
    print(f"  Average F1: {avg_f1:.3f}")
    print(f"  Average Latency: {avg_latency:.1f}ms")

    return results


def context_length_analysis():
    """
    Analyze impact of context length on generation.
    Tests optimal context size.
    """
    print("\n=== Context Length Analysis ===")

    evaluator = RAGalystEvaluator()

    query = "What is AI?"

    # Different context lengths
    scenarios = [
        {
            "name": "Short Context",
            "contexts": ["AI is artificial intelligence"],
            "latency": 500
        },
        {
            "name": "Medium Context",
            "contexts": [
                "AI is artificial intelligence",
                "AI systems can learn from data",
                "AI is used in many applications"
            ],
            "latency": 1000
        },
        {
            "name": "Long Context",
            "contexts": [f"Context {i}" for i in range(10)],
            "latency": 2500
        }
    ]

    for scenario in scenarios:
        answer = "AI is a system that can learn and make decisions"

        metrics = evaluator.evaluate_generation(
            query, scenario["contexts"], answer, scenario["latency"]
        )

        context_len = sum(len(c) for c in scenario["contexts"])

        print(f"\n{scenario['name']}:")
        print(f"  Contexts: {len(scenario['contexts'])}")
        print(f"  Total Length: {context_len} chars")
        print(f"  Faithfulness: {metrics.faithfulness:.3f}")
        print(f"  Latency: {metrics.latency_ms}ms")
        print(f"  Latency/Context: {metrics.latency_ms/len(scenario['contexts']):.1f}ms")


def main():
    """Run all RAGalyst evaluation examples."""
    print("=" * 60)
    print("RAGalyst RAG Pipeline Analysis Examples")
    print("=" * 60)

    try:
        # Component-level analysis
        basic_pipeline_analysis()
        component_comparison()

        # Performance analysis
        latency_profiling()
        quality_score_breakdown()

        # Batch and advanced
        batch_pipeline_evaluation()
        context_length_analysis()

        print("\n" + "=" * 60)
        print("All RAGalyst evaluations completed successfully!")
        print("=" * 60)

        print("\n📊 RAGalyst Key Features:")
        print("  • Component Analysis: Separate retrieval & generation eval")
        print("  • Bottleneck Detection: Identify performance issues")
        print("  • Latency Profiling: Track time spent in each stage")
        print("  • Quality Breakdown: Understand score composition")
        print("  • Recommendations: Actionable improvement suggestions")
        print("  • Batch Evaluation: Aggregate metrics across datasets")
        print("  • Configuration Testing: Compare strategies")

        print("\n💡 RAGalyst Use Cases:")
        print("  • RAG pipeline optimization")
        print("  • Performance bottleneck identification")
        print("  • Component-level debugging")
        print("  • Configuration comparison")
        print("  • Production monitoring")

    except Exception as e:
        print(f"\nError running evaluations: {e}")
        print("Setup required:")
        print("  1. pip install ragalyst")
        print("  2. Instrument your RAG pipeline")
        print("  3. Collect evaluation data")


if __name__ == "__main__":
    main()
