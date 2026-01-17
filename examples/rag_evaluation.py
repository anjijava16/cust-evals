"""Example usage of RAG-specific evaluators.

This example demonstrates the new RAG evaluation metrics:
- FaithfulnessEvaluator: Checks if response is grounded in retrieval context
- AnswerRelevancyEvaluator: Checks if answer addresses the query

These metrics are inspired by DeepEval and RAGAS frameworks.
"""

import os
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

# Initialize LLM (requires OPENAI_API_KEY or ANTHROPIC_API_KEY)
llm = LLM(provider="openai", model="gpt-4o-mini")

print("=" * 80)
print("RAG Evaluation Examples")
print("=" * 80)

# Example 1: Faithful Response
print("\n1. FAITHFULNESS EVALUATION - Faithful Response")
print("-" * 80)

evaluator = FaithfulnessEvaluator(llm)

eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France. It's located on the Seine River.",
    "context": "Paris is the capital and largest city of France, located on the Seine River in northern France."
}

score = evaluator.evaluate(eval_input)
print(f"Query: {eval_input['input']}")
print(f"Context: {eval_input['context']}")
print(f"Response: {eval_input['output']}")
print(f"\nResult: {score.label} (score: {score.score})")
print(f"Explanation: {score.explanation}")
print(f"Has Ground Truth: {score.metadata.get('has_ground_truth', False)}")

# Example 2: Unfaithful Response (Hallucination)
print("\n2. FAITHFULNESS EVALUATION - Unfaithful Response")
print("-" * 80)

eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France. It has a population of exactly 12 million people and was founded in 250 AD.",
    "context": "Paris is the capital and largest city of France, located on the Seine River."
}

score = evaluator.evaluate(eval_input)
print(f"Query: {eval_input['input']}")
print(f"Context: {eval_input['context']}")
print(f"Response: {eval_input['output']}")
print(f"\nResult: {score.label} (score: {score.score})")
print(f"Explanation: {score.explanation}")

# Example 3: Answer Relevancy - Relevant Answer
print("\n3. ANSWER RELEVANCY EVALUATION - Relevant Answer")
print("-" * 80)

evaluator = AnswerRelevancyEvaluator(llm)

eval_input = {
    "input": "What is the capital of France?",
    "output": "Paris is the capital of France."
}

score = evaluator.evaluate(eval_input)
print(f"Query: {eval_input['input']}")
print(f"Response: {eval_input['output']}")
print(f"\nResult: {score.label} (score: {score.score})")
print(f"Explanation: {score.explanation}")

# Example 4: Answer Relevancy - Irrelevant Answer
print("\n4. ANSWER RELEVANCY EVALUATION - Irrelevant Answer")
print("-" * 80)

eval_input = {
    "input": "What is the capital of France?",
    "output": "The Eiffel Tower is a famous landmark in Europe. It attracts millions of tourists every year."
}

score = evaluator.evaluate(eval_input)
print(f"Query: {eval_input['input']}")
print(f"Response: {eval_input['output']}")
print(f"\nResult: {score.label} (score: {score.score})")
print(f"Explanation: {score.explanation}")

# Example 5: Describe the Evaluators
print("\n5. EVALUATOR DESCRIPTIONS")
print("-" * 80)

print("\nFaithfulness Evaluator:")
faithfulness_desc = FaithfulnessEvaluator(llm).describe()
for key, value in faithfulness_desc.items():
    print(f"  {key}: {value}")

print("\nAnswer Relevancy Evaluator:")
relevancy_desc = AnswerRelevancyEvaluator(llm).describe()
for key, value in relevancy_desc.items():
    print(f"  {key}: {value}")

# Example 6: Batch Evaluation
print("\n6. BATCH RAG EVALUATION")
print("-" * 80)

rag_test_cases = [
    {
        "input": "What is machine learning?",
        "output": "Machine learning is a subset of AI that enables systems to learn from data.",
        "context": "Machine learning is a branch of artificial intelligence that allows computers to learn from data without being explicitly programmed."
    },
    {
        "input": "Who invented the telephone?",
        "output": "Alexander Graham Bell invented the telephone in 1876.",
        "context": "Alexander Graham Bell is credited with inventing and patenting the first practical telephone in 1876."
    },
    {
        "input": "What is photosynthesis?",
        "output": "Photosynthesis is the process by which plants make food using sunlight.",
        "context": "Photosynthesis is the process used by plants to convert light energy into chemical energy stored in glucose."
    }
]

faithfulness_evaluator = FaithfulnessEvaluator(llm)
relevancy_evaluator = AnswerRelevancyEvaluator(llm)

print("\nEvaluating multiple RAG responses...\n")

results = []
for i, test_case in enumerate(rag_test_cases, 1):
    print(f"Test Case {i}: {test_case['input']}")

    # Evaluate faithfulness
    faith_score = faithfulness_evaluator.evaluate(test_case)

    # Evaluate answer relevancy
    rel_score = relevancy_evaluator.evaluate(test_case)

    results.append({
        "query": test_case["input"],
        "faithfulness": faith_score.score,
        "faithfulness_label": faith_score.label,
        "relevancy": rel_score.score,
        "relevancy_label": rel_score.label,
    })

    print(f"  Faithfulness: {faith_score.label} ({faith_score.score})")
    print(f"  Relevancy: {rel_score.label} ({rel_score.score})")
    print()

# Summary
print("\n7. EVALUATION SUMMARY")
print("-" * 80)

avg_faithfulness = sum(r["faithfulness"] for r in results) / len(results)
avg_relevancy = sum(r["relevancy"] for r in results) / len(results)

print(f"Average Faithfulness Score: {avg_faithfulness:.2f}")
print(f"Average Relevancy Score: {avg_relevancy:.2f}")

faithful_count = sum(1 for r in results if r["faithfulness_label"] == "faithful")
relevant_count = sum(1 for r in results if r["relevancy_label"] == "relevant")

print(f"\nFaithful Responses: {faithful_count}/{len(results)}")
print(f"Relevant Responses: {relevant_count}/{len(results)}")

print("\n" + "=" * 80)
print("RAG evaluation complete!")
print("=" * 80)
