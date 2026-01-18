"""
Lesson 4: RAG Evaluation - Evaluating Retrieval-Augmented Generation

Learn how to evaluate RAG systems that combine retrieval and generation.

Learning Objectives:
- Understand RAG systems
- Evaluate retrieval quality
- Evaluate generation quality
- End-to-end RAG metrics

Prerequisites: Lessons 1-3
"""

print("=" * 70)
print("LESSON 4: RAG Evaluation")
print("=" * 70)

print("""
🔍 WHAT IS RAG?

RAG = Retrieval-Augmented Generation

Instead of just generating answers, RAG systems:
1. RETRIEVE relevant documents/context
2. GENERATE answers using that context

Example:
  User asks: "What's our refund policy?"
  
  System:
  1. Retrieves: [policy_doc.txt, faq.txt]
  2. Generates: "Our refund policy allows returns within 30 days..."

Why evaluate RAG differently?
✓ Need to check BOTH retrieval AND generation
✓ Retrieval quality affects generation quality
✓ Can have retrieval failures OR generation failures
""")

# ============================================================================
# COMPONENT 1: RETRIEVAL EVALUATION
# ============================================================================

print("\n" + "=" * 70)
print("COMPONENT 1: Evaluating Retrieval")
print("=" * 70)

def evaluate_retrieval(
    retrieved_docs: list,
    relevant_docs: list
) -> dict:
    """
    Evaluate retrieval quality using precision and recall.
    
    Precision: Of what was retrieved, how much was relevant?
    Recall: Of what was relevant, how much was retrieved?
    """
    
    retrieved_set = set(retrieved_docs)
    relevant_set = set(relevant_docs)
    
    # True positives: relevant docs that were retrieved
    true_positives = retrieved_set & relevant_set
    
    # Calculate metrics
    precision = len(true_positives) / len(retrieved_set) if retrieved_set else 0
    recall = len(true_positives) / len(relevant_set) if relevant_set else 0
    
    # F1 score: harmonic mean of precision and recall
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "retrieved_count": len(retrieved_set),
        "relevant_count": len(relevant_set),
        "correct_count": len(true_positives)
    }

# Demo
print("\nExample: Document Retrieval")
print("-" * 40)

relevant_docs = ["doc1", "doc2", "doc5"]
retrieved_docs = ["doc1", "doc2", "doc3", "doc4"]

result = evaluate_retrieval(retrieved_docs, relevant_docs)

print(f"Relevant docs:  {relevant_docs}")
print(f"Retrieved docs: {retrieved_docs}")
print(f"\nMetrics:")
print(f"  Precision: {result['precision']:.2%} (2/4 retrieved were relevant)")
print(f"  Recall:    {result['recall']:.2%} (2/3 relevant were retrieved)")
print(f"  F1 Score:  {result['f1_score']:.2%} (harmonic mean)")

# ============================================================================
# COMPONENT 2: GENERATION EVALUATION
# ============================================================================

print("\n\n" + "=" * 70)
print("COMPONENT 2: Evaluating Generation")
print("=" * 70)

def evaluate_faithfulness(answer: str, context: str) -> dict:
    """
    Check if answer is faithful to (grounded in) the context.
    Detects hallucination.
    """
    
    # Simple faithfulness check: word overlap
    answer_words = set(answer.lower().split())
    context_words = set(context.lower().split())
    
    grounded_words = answer_words & context_words
    faithfulness = len(grounded_words) / len(answer_words) if answer_words else 0
    
    return {
        "faithfulness_score": faithfulness,
        "grounded_words": len(grounded_words),
        "total_words": len(answer_words),
        "passed": faithfulness >= 0.5
    }

def evaluate_relevance(question: str, answer: str) -> dict:
    """Check if answer is relevant to the question."""
    
    question_words = set(question.lower().split())
    answer_words = set(answer.lower().split())
    
    overlap = len(question_words & answer_words)
    relevance = min(overlap / len(question_words), 1.0) if question_words else 0
    
    return {
        "relevance_score": relevance,
        "passed": relevance >= 0.3
    }

# Demo
print("\nExample: Generation Quality")
print("-" * 40)

context = "Our company offers free shipping on orders over $50. Standard delivery takes 3-5 business days."
question = "What is your shipping policy?"
answer = "We offer free shipping on orders over $50, with delivery in 3-5 days."

faith_result = evaluate_faithfulness(answer, context)
rel_result = evaluate_relevance(question, answer)

print(f"Context:  {context}")
print(f"Question: {question}")
print(f"Answer:   {answer}")
print(f"\nFaithfulness: {faith_result['faithfulness_score']:.2%} ({'✓ PASS' if faith_result['passed'] else '✗ FAIL'})")
print(f"Relevance:    {rel_result['relevance_score']:.2%} ({'✓ PASS' if rel_result['passed'] else '✗ FAIL'})")

# ============================================================================
# END-TO-END RAG EVALUATION
# ============================================================================

print("\n\n" + "=" * 70)
print("END-TO-END RAG EVALUATION")
print("=" * 70)

def evaluate_rag_system(
    question: str,
    retrieved_docs: list,
    relevant_docs: list,
    generated_answer: str,
    ground_truth: str,
    context: str
) -> dict:
    """Comprehensive RAG evaluation."""
    
    # Evaluate retrieval
    retrieval_metrics = evaluate_retrieval(retrieved_docs, relevant_docs)
    
    # Evaluate generation
    faithfulness_metrics = evaluate_faithfulness(generated_answer, context)
    relevance_metrics = evaluate_relevance(question, generated_answer)
    
    # Overall score (weighted average)
    overall_score = (
        retrieval_metrics['f1_score'] * 0.3 +
        faithfulness_metrics['faithfulness_score'] * 0.4 +
        relevance_metrics['relevance_score'] * 0.3
    )
    
    return {
        "overall_score": overall_score,
        "retrieval": retrieval_metrics,
        "faithfulness": faithfulness_metrics,
        "relevance": relevance_metrics,
        "passed": overall_score >= 0.7
    }

# Full demo
print("\nComplete RAG Evaluation Example")
print("-" * 40)

# Simulated RAG system output
question = "How do I return a product?"
retrieved_docs = ["return_policy.txt", "faq.txt", "shipping.txt"]
relevant_docs = ["return_policy.txt", "faq.txt"]
context = "Returns are accepted within 30 days. Items must be unused. Contact support to initiate return."
generated_answer = "You can return products within 30 days if unused. Contact our support team to start the return process."
ground_truth = "Returns within 30 days, items must be unused, contact support"

result = evaluate_rag_system(
    question=question,
    retrieved_docs=retrieved_docs,
    relevant_docs=relevant_docs,
    generated_answer=generated_answer,
    ground_truth=ground_truth,
    context=context
)

print(f"Question: {question}\n")
print(f"Overall Score: {result['overall_score']:.2%}")
print(f"Status: {'✓ PASS' if result['passed'] else '✗ FAIL'}\n")

print("Component Scores:")
print(f"  Retrieval F1:   {result['retrieval']['f1_score']:.2%}")
print(f"  Faithfulness:   {result['faithfulness']['faithfulness_score']:.2%}")
print(f"  Relevance:      {result['relevance']['relevance_score']:.2%}")

# ============================================================================
# KEY RAG METRICS SUMMARY
# ============================================================================

print("\n\n" + "=" * 70)
print("KEY RAG METRICS SUMMARY")
print("=" * 70)

print("""
📊 RETRIEVAL METRICS:

• Precision: Accuracy of retrieved docs
  → High precision = few irrelevant docs retrieved
  
• Recall: Coverage of relevant docs
  → High recall = most relevant docs retrieved
  
• F1 Score: Balance of precision and recall
  → Best overall retrieval metric

📝 GENERATION METRICS:

• Faithfulness (Groundedness): Answer based on context?
  → Prevents hallucination
  → Critical for trust
  
• Relevance: Answer addresses question?
  → Ensures usefulness
  
• Completeness: All required info included?
  → Measures thoroughness

🎯 END-TO-END METRICS:

• Answer Quality: Overall goodness
• Context Utilization: How well context was used
• Correctness: Match with ground truth

💡 PRO TIPS:

✓ Evaluate retrieval AND generation separately
✓ Poor retrieval → poor generation (usually)
✓ Good retrieval doesn't guarantee good generation
✓ Track which component is failing
✓ Optimize the weak component first

⚠️ COMMON ISSUES:

❌ Retrieving irrelevant docs (low precision)
❌ Missing relevant docs (low recall)
❌ Hallucinating beyond context (low faithfulness)
❌ Ignoring retrieved context (low utilization)
""")

print("\n" + "=" * 70)
print("✨ Lesson 4 Complete!")
print("=" * 70)
print("\nNext: 05_custom_metrics.py - Build your own evaluators!")
