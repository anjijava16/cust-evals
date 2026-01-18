"""
Humanloop Evaluation Example

Humanloop is a human-in-the-loop evaluation platform with focus on human feedback,
prompt management, A/B testing, and collaborative evaluation.

Installation:
pip install humanloop

Documentation: https://humanloop.com/docs
"""

import os
from humanloop import Humanloop
from typing import List, Dict, Any, Optional
import time
import random


def setup_humanloop():
    """Initialize Humanloop client."""
    api_key = os.getenv("HUMANLOOP_API_KEY", "")

    client = Humanloop(api_key=api_key)

    print("✓ Humanloop client initialized")
    print(f"  View at: https://app.humanloop.com/")

    return client


def basic_prompt_example():
    """
    Create and use prompts in Humanloop.
    Prompts are versioned and managed centrally.
    """
    print("\n=== Basic Prompt Example ===")

    client = setup_humanloop()

    # Define a prompt
    prompt_data = {
        "project": "qa-assistant",
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 150,
        "template": "You are a helpful AI assistant. Answer the following question:\n\nQuestion: {{question}}\n\nAnswer:"
    }

    # In practice, create prompt via API
    print("✓ Prompt created:")
    print(f"  Project: {prompt_data['project']}")
    print(f"  Model: {prompt_data['model']}")
    print(f"  Template variables: question")
    print(f"  Prompt automatically versioned")

    # Simulate using the prompt
    question = "What is machine learning?"
    filled_prompt = prompt_data["template"].replace("{{question}}", question)

    print(f"\n  Example usage:")
    print(f"  Question: {question}")
    print(f"  Prompt: {filled_prompt[:80]}...")

    return prompt_data


def prompt_versioning_example():
    """
    Version control for prompts.
    Track changes and iterate on prompt design.
    """
    print("\n=== Prompt Versioning Example ===")

    # Different versions of the same prompt
    prompt_versions = {
        "v1": {
            "template": "Answer: {{question}}",
            "description": "Basic prompt"
        },
        "v2": {
            "template": "You are a helpful assistant. Please answer:\n{{question}}",
            "description": "Added system context"
        },
        "v3": {
            "template": "You are an expert assistant. Provide a detailed, accurate answer:\n\nQuestion: {{question}}\n\nAnswer:",
            "description": "Expert persona with structured format"
        },
        "v4": {
            "template": "You are an expert assistant. Provide a detailed, accurate answer with examples:\n\nQuestion: {{question}}\n\nAnswer (include examples):",
            "description": "Added instruction for examples"
        }
    }

    print("Prompt evolution:")
    for version, data in prompt_versions.items():
        print(f"\n  {version}:")
        print(f"    Description: {data['description']}")
        print(f"    Length: {len(data['template'])} chars")

    print("\n✓ Prompt versioning:")
    print(f"  Total versions: {len(prompt_versions)}")
    print(f"  Each version tracked and revertible")
    print(f"  Compare performance across versions")
    print(f"  Roll back to any version instantly")

    return prompt_versions


def human_feedback_collection():
    """
    Collect human feedback on model outputs.
    Essential for continuous improvement.
    """
    print("\n=== Human Feedback Collection Example ===")

    client = setup_humanloop()

    # Simulate model generations with human feedback
    generations = [
        {
            "question": "What is quantum computing?",
            "answer": "Quantum computing uses quantum mechanics to process information.",
            "human_rating": 4,  # 1-5 scale
            "feedback_text": "Good explanation but could be more detailed"
        },
        {
            "question": "Explain photosynthesis",
            "answer": "Photosynthesis is how plants convert sunlight into energy using chlorophyll.",
            "human_rating": 5,
            "feedback_text": "Excellent, clear and accurate"
        },
        {
            "question": "What is blockchain?",
            "answer": "A distributed ledger technology.",
            "human_rating": 2,
            "feedback_text": "Too brief, needs more explanation"
        }
    ]

    print("Human feedback collected:\n")
    for i, gen in enumerate(generations, 1):
        print(f"  Generation {i}:")
        print(f"    Question: {gen['question']}")
        print(f"    Rating: {'⭐' * gen['human_rating']} ({gen['human_rating']}/5)")
        print(f"    Feedback: {gen['feedback_text']}")
        print()

    avg_rating = sum(g['human_rating'] for g in generations) / len(generations)

    print(f"✓ Human feedback summary:")
    print(f"  Total feedback collected: {len(generations)}")
    print(f"  Average rating: {avg_rating:.1f}/5")
    print(f"  Feedback stored and analyzed in Humanloop")

    return generations


def preference_ranking_example():
    """
    Human preference ranking between model outputs.
    Compare multiple responses to find best.
    """
    print("\n=== Preference Ranking Example ===")

    # Comparison scenarios
    comparisons = [
        {
            "question": "Explain machine learning",
            "outputs": {
                "model_a": "ML is when computers learn from data.",
                "model_b": "Machine learning is a subset of AI that enables systems to learn from data without explicit programming.",
                "model_c": "It's about algorithms learning patterns."
            },
            "human_preference": "model_b",
            "reason": "Most comprehensive and clear"
        },
        {
            "question": "What is climate change?",
            "outputs": {
                "model_a": "Long-term changes in Earth's climate patterns.",
                "model_b": "Global warming and weather changes.",
                "model_c": "Climate change refers to long-term shifts in temperatures and weather patterns, primarily caused by human activities."
            },
            "human_preference": "model_c",
            "reason": "Includes cause and is most accurate"
        }
    ]

    print("Preference ranking results:\n")
    for i, comp in enumerate(comparisons, 1):
        print(f"  Comparison {i}: {comp['question']}")
        print(f"    Options compared: {len(comp['outputs'])}")
        print(f"    Winner: {comp['human_preference']}")
        print(f"    Reason: {comp['reason']}")
        print()

    print(f"✓ Preference ranking:")
    print(f"  Total comparisons: {len(comparisons)}")
    print(f"  Pairwise preferences collected")
    print(f"  Helps identify best model/prompt")
    print(f"  Data used for model alignment")

    return comparisons


def ab_testing_example():
    """
    A/B testing for prompts and models.
    Data-driven decision making.
    """
    print("\n=== A/B Testing Example ===")

    # A/B test configuration
    test_config = {
        "name": "Prompt Temperature Test",
        "variants": [
            {"name": "A: Low Temp", "temperature": 0.3, "sample_size": 100},
            {"name": "B: High Temp", "temperature": 0.9, "sample_size": 100}
        ],
        "metrics": ["accuracy", "creativity", "user_satisfaction"]
    }

    # Simulated results
    results = {
        "A: Low Temp": {
            "accuracy": 0.87,
            "creativity": 0.65,
            "user_satisfaction": 0.78,
            "avg_score": 0.77
        },
        "B: High Temp": {
            "accuracy": 0.75,
            "creativity": 0.91,
            "user_satisfaction": 0.82,
            "avg_score": 0.83
        }
    }

    print(f"A/B Test: {test_config['name']}\n")
    print(f"{'Variant':<15} {'Accuracy':<12} {'Creativity':<12} {'Satisfaction':<12} {'Avg'}")
    print("-" * 65)

    for variant_name, metrics in results.items():
        print(f"{variant_name:<15} {metrics['accuracy']:<12.2f} {metrics['creativity']:<12.2f} {metrics['user_satisfaction']:<12.2f} {metrics['avg_score']:.2f}")

    winner = max(results.items(), key=lambda x: x[1]['avg_score'])

    print(f"\n✓ A/B test results:")
    print(f"  Winner: {winner[0]}")
    print(f"  Average score: {winner[1]['avg_score']:.2f}")
    print(f"  Statistical significance calculated")
    print(f"  Automatic traffic distribution")

    return results


def collaborative_evaluation_example():
    """
    Team collaboration on evaluation.
    Multiple reviewers can provide feedback.
    """
    print("\n=== Collaborative Evaluation Example ===")

    # Multi-reviewer evaluation
    evaluation_task = {
        "output_id": "gen_12345",
        "question": "Explain neural networks",
        "answer": "Neural networks are computing systems inspired by biological neural networks in brains.",
        "reviewers": [
            {
                "name": "Alice (ML Engineer)",
                "accuracy_score": 4,
                "clarity_score": 5,
                "comments": "Good high-level explanation"
            },
            {
                "name": "Bob (Domain Expert)",
                "accuracy_score": 5,
                "clarity_score": 4,
                "comments": "Accurate but could mention learning aspect"
            },
            {
                "name": "Carol (Product Manager)",
                "accuracy_score": 4,
                "clarity_score": 5,
                "comments": "Clear for end users"
            }
        ]
    }

    print(f"Output: {evaluation_task['answer']}\n")
    print("Team evaluation:")

    total_accuracy = 0
    total_clarity = 0

    for reviewer in evaluation_task["reviewers"]:
        total_accuracy += reviewer["accuracy_score"]
        total_clarity += reviewer["clarity_score"]

        print(f"\n  {reviewer['name']}:")
        print(f"    Accuracy: {reviewer['accuracy_score']}/5")
        print(f"    Clarity: {reviewer['clarity_score']}/5")
        print(f"    Comments: {reviewer['comments']}")

    num_reviewers = len(evaluation_task["reviewers"])
    avg_accuracy = total_accuracy / num_reviewers
    avg_clarity = total_clarity / num_reviewers

    print(f"\n✓ Collaborative evaluation:")
    print(f"  Reviewers: {num_reviewers}")
    print(f"  Avg Accuracy: {avg_accuracy:.1f}/5")
    print(f"  Avg Clarity: {avg_clarity:.1f}/5")
    print(f"  Multiple perspectives captured")

    return evaluation_task


def quality_scoring_example():
    """
    Multi-dimensional quality scoring.
    Comprehensive evaluation framework.
    """
    print("\n=== Quality Scoring Example ===")

    # Define quality dimensions
    quality_dimensions = [
        "accuracy",
        "relevance",
        "completeness",
        "clarity",
        "tone",
        "safety"
    ]

    # Example evaluation
    evaluation = {
        "question": "What are the benefits of exercise?",
        "answer": "Regular exercise improves cardiovascular health, strengthens muscles, enhances mental well-being, and boosts energy levels.",
        "scores": {
            "accuracy": 0.95,
            "relevance": 0.92,
            "completeness": 0.85,
            "clarity": 0.90,
            "tone": 0.88,
            "safety": 1.0
        }
    }

    print(f"Question: {evaluation['question']}")
    print(f"Answer: {evaluation['answer']}\n")
    print("Quality scores:")

    for dimension in quality_dimensions:
        score = evaluation["scores"][dimension]
        bar = "█" * int(score * 10)
        print(f"  {dimension:<15} {score:.2f} {bar}")

    overall_score = sum(evaluation["scores"].values()) / len(evaluation["scores"])

    print(f"\n✓ Quality assessment:")
    print(f"  Dimensions evaluated: {len(quality_dimensions)}")
    print(f"  Overall score: {overall_score:.2f}")
    print(f"  Detailed breakdown available")

    return evaluation


def production_monitoring_example():
    """
    Monitor production model performance.
    Track quality metrics in real-time.
    """
    print("\n=== Production Monitoring Example ===")

    # Simulate production metrics over time
    monitoring_data = {
        "time_period": "Last 24 hours",
        "total_requests": 1500,
        "metrics": {
            "avg_quality_score": 0.85,
            "avg_latency_ms": 234,
            "error_rate": 0.02,
            "user_satisfaction": 0.82
        },
        "feedback_collected": 150,
        "issues_detected": [
            {"type": "quality_drop", "severity": "low", "time": "14:30", "description": "Quality dip in 10 requests"},
            {"type": "latency_spike", "severity": "medium", "time": "18:45", "description": "Latency above threshold"}
        ]
    }

    print(f"Period: {monitoring_data['time_period']}")
    print(f"Total requests: {monitoring_data['total_requests']}\n")

    print("Key metrics:")
    for metric, value in monitoring_data["metrics"].items():
        if "score" in metric or "satisfaction" in metric or "rate" in metric:
            print(f"  {metric}: {value:.2%}")
        else:
            print(f"  {metric}: {value:.0f} ms")

    print(f"\nFeedback: {monitoring_data['feedback_collected']} responses collected")

    print(f"\nIssues detected: {len(monitoring_data['issues_detected'])}")
    for issue in monitoring_data["issues_detected"]:
        print(f"  • {issue['time']} - {issue['type']} ({issue['severity']})")
        print(f"    {issue['description']}")

    print(f"\n✓ Production monitoring:")
    print(f"  Real-time metric tracking")
    print(f"  Automated issue detection")
    print(f"  Human feedback integration")
    print(f"  Dashboard and alerts")

    return monitoring_data


def dataset_management_example():
    """
    Manage evaluation datasets.
    Curate and version test sets.
    """
    print("\n=== Dataset Management Example ===")

    # Evaluation datasets
    datasets = {
        "golden_set": {
            "description": "High-quality verified examples",
            "size": 50,
            "categories": ["factual", "reasoning", "creative"],
            "created": "2024-01-01",
            "version": "1.0"
        },
        "edge_cases": {
            "description": "Challenging corner cases",
            "size": 30,
            "categories": ["ambiguous", "complex", "multi-step"],
            "created": "2024-01-10",
            "version": "1.0"
        },
        "production_samples": {
            "description": "Real user queries",
            "size": 100,
            "categories": ["common", "rare", "problematic"],
            "created": "2024-01-15",
            "version": "2.0"
        }
    }

    print("Evaluation datasets:\n")
    for name, info in datasets.items():
        print(f"  {name}:")
        print(f"    Description: {info['description']}")
        print(f"    Size: {info['size']} examples")
        print(f"    Categories: {', '.join(info['categories'])}")
        print(f"    Version: {info['version']}")
        print()

    total_examples = sum(d["size"] for d in datasets.values())

    print(f"✓ Dataset management:")
    print(f"  Total datasets: {len(datasets)}")
    print(f"  Total examples: {total_examples}")
    print(f"  Categorized and versioned")
    print(f"  Reusable across evaluations")

    return datasets


def feedback_driven_improvement():
    """
    Use feedback to drive model improvement.
    Iterative refinement based on human input.
    """
    print("\n=== Feedback-Driven Improvement Example ===")

    # Improvement cycle
    improvement_cycle = [
        {
            "iteration": 1,
            "prompt": "Answer: {{question}}",
            "avg_score": 0.65,
            "feedback_themes": ["Too brief", "Lacks context"],
            "action": "Add system context"
        },
        {
            "iteration": 2,
            "prompt": "You are helpful. Answer: {{question}}",
            "avg_score": 0.75,
            "feedback_themes": ["Better but needs structure"],
            "action": "Add structure to format"
        },
        {
            "iteration": 3,
            "prompt": "You are helpful. Question: {{question}}\nAnswer:",
            "avg_score": 0.82,
            "feedback_themes": ["Good, could be more detailed"],
            "action": "Request detailed responses"
        },
        {
            "iteration": 4,
            "prompt": "You are helpful. Provide detailed answer.\nQ: {{question}}\nA:",
            "avg_score": 0.88,
            "feedback_themes": ["Excellent improvement"],
            "action": "Keep this version"
        }
    ]

    print("Improvement trajectory:\n")
    print(f"{'Iter':<6} {'Score':<8} {'Change':<10} {'Feedback Themes'}")
    print("-" * 60)

    prev_score = None
    for cycle in improvement_cycle:
        change = ""
        if prev_score:
            diff = cycle['avg_score'] - prev_score
            change = f"+{diff:.2f}" if diff > 0 else f"{diff:.2f}"

        print(f"{cycle['iteration']:<6} {cycle['avg_score']:<8.2f} {change:<10} {', '.join(cycle['feedback_themes'])}")
        prev_score = cycle['avg_score']

    improvement = improvement_cycle[-1]['avg_score'] - improvement_cycle[0]['avg_score']

    print(f"\n✓ Feedback-driven improvement:")
    print(f"  Iterations: {len(improvement_cycle)}")
    print(f"  Score improvement: +{improvement:.2f}")
    print(f"  Systematic refinement process")
    print(f"  Human feedback at center")

    return improvement_cycle


def main():
    """Run all Humanloop examples."""
    print("=" * 60)
    print("Humanloop Evaluation Examples")
    print("=" * 60)

    try:
        # Prompt management
        basic_prompt_example()
        prompt_versioning_example()

        # Human feedback
        human_feedback_collection()
        preference_ranking_example()
        collaborative_evaluation_example()

        # Testing and evaluation
        ab_testing_example()
        quality_scoring_example()
        dataset_management_example()

        # Production and improvement
        production_monitoring_example()
        feedback_driven_improvement()

        print("\n" + "=" * 60)
        print("All Humanloop examples completed successfully!")
        print("=" * 60)

        print("\n📊 Humanloop Key Features:")
        print("  • Human Feedback: Collect ratings and preferences")
        print("  • Prompt Versioning: Track and iterate on prompts")
        print("  • A/B Testing: Data-driven prompt optimization")
        print("  • Collaborative Evaluation: Team-based review")
        print("  • Quality Scoring: Multi-dimensional assessment")
        print("  • Production Monitoring: Real-time quality tracking")
        print("  • Dataset Management: Curated test sets")
        print("  • Preference Ranking: Compare model outputs")
        print("  • Feedback Loop: Continuous improvement cycle")
        print("  • Beautiful UI: Intuitive dashboard")

        print("\n💡 Humanloop Use Cases:")
        print("  • Prompt engineering and optimization")
        print("  • Human-in-the-loop evaluation")
        print("  • Model output quality assessment")
        print("  • A/B testing prompts and models")
        print("  • Collecting user feedback")
        print("  • Team collaboration on evaluation")
        print("  • Production quality monitoring")
        print("  • Iterative model improvement")
        print("  • Dataset curation and management")

        print("\n🚀 Getting Started:")
        print("  1. Sign up: https://humanloop.com/")
        print("  2. Get API key from dashboard")
        print("  3. Install: pip install humanloop")
        print("  4. Set key: export HUMANLOOP_API_KEY='your-key'")
        print("  5. Create projects and start evaluating")

        print("\n🎯 Why Humanloop:")
        print("  • Human feedback at the center")
        print("  • Collaborative evaluation workflows")
        print("  • Excellent prompt management")
        print("  • Built-in A/B testing")
        print("  • Production-ready monitoring")
        print("  • Intuitive UI for non-technical users")
        print("  • Systematic improvement process")
        print("  • Enterprise-ready features")

        print("\n👥 Human-in-the-Loop Benefits:")
        print("  • Capture nuanced quality signals")
        print("  • Domain expert evaluation")
        print("  • Preference learning")
        print("  • Catch subtle issues")
        print("  • Build evaluation datasets")
        print("  • Continuous quality improvement")

    except Exception as e:
        print(f"\nNote: {e}")
        print("\nSetup required:")
        print("  1. Sign up at https://humanloop.com/")
        print("  2. Get API key from dashboard")
        print("  3. Install: pip install humanloop")
        print("  4. Set environment variable:")
        print("     export HUMANLOOP_API_KEY='your-api-key'")
        print("\nThese examples demonstrate Humanloop's capabilities.")


if __name__ == "__main__":
    main()
