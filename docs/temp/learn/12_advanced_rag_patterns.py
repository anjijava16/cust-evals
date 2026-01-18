"""
Lesson 12: Advanced RAG Evaluation Patterns (Advanced)

Learn to evaluate sophisticated RAG systems with multi-hop reasoning,
iterative retrieval, and hybrid search strategies.

Prerequisites: Lessons 1-11, especially Lesson 4 (RAG Evaluation)
Difficulty: ⭐⭐⭐ Advanced
Time: 50 minutes
"""

print("="*80)
print("LESSON 12: Advanced RAG Evaluation Patterns")
print("="*80)

print("""
🚀 BEYOND BASIC RAG

Basic RAG: Single retrieval → Generate answer
Advanced RAG: Multiple strategies for better results

Advanced Patterns:
1. Multi-hop reasoning (multiple retrieval steps)
2. Iterative retrieval (refine queries)
3. Hybrid search (combine multiple retrievers)
4. Query decomposition (break complex queries)
5. Re-ranking (improve retrieval quality)
6. Context window optimization

This lesson shows how to evaluate these sophisticated patterns.
""")

from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict
import math

# ============================================================================
# PART 1: MULTI-HOP REASONING EVALUATION
# ============================================================================

print("\n" + "="*80)
print("PART 1: Multi-Hop Reasoning Evaluation")
print("="*80)

print("""
🔗 MULTI-HOP REASONING:

Question: "Who was the president when the iPhone was released?"

Single-hop: ❌ Direct answer not in docs
Multi-hop: ✅
  1. When was iPhone released? → 2007
  2. Who was president in 2007? → George W. Bush

Evaluation challenges:
- Track reasoning path
- Verify each hop
- Check final synthesis
""")

class MultiHopEvaluator:
    """Evaluate multi-hop RAG systems."""

    def evaluate_reasoning_path(
        self,
        question: str,
        reasoning_steps: List[Dict],
        expected_steps: List[Dict],
        final_answer: str,
        expected_answer: str
    ) -> Dict[str, Any]:
        """Evaluate a multi-hop reasoning path."""

        # Check number of hops
        num_hops_correct = len(reasoning_steps) == len(expected_steps)

        # Check each step
        step_scores = []
        for i, (actual, expected) in enumerate(zip(reasoning_steps, expected_steps)):
            # Check if step addresses the right sub-question
            subq_match = self._compare_subquestions(
                actual.get('sub_question', ''),
                expected.get('sub_question', '')
            )

            # Check if retrieved info is relevant
            info_relevant = self._check_relevance(
                actual.get('retrieved_info', ''),
                expected.get('expected_info', '')
            )

            step_score = (subq_match + info_relevant) / 2
            step_scores.append(step_score)

        # Check final synthesis
        final_correct = expected_answer.lower() in final_answer.lower()

        # Overall score
        avg_step_score = sum(step_scores) / len(step_scores) if step_scores else 0
        overall_score = (avg_step_score * 0.6) + (float(final_correct) * 0.4)

        return {
            'overall_score': overall_score,
            'num_hops_correct': num_hops_correct,
            'expected_hops': len(expected_steps),
            'actual_hops': len(reasoning_steps),
            'step_scores': step_scores,
            'avg_step_score': avg_step_score,
            'final_answer_correct': final_correct,
            'passed': overall_score >= 0.7
        }

    def _compare_subquestions(self, actual: str, expected: str) -> float:
        """Compare sub-questions for similarity."""
        actual_words = set(actual.lower().split())
        expected_words = set(expected.lower().split())

        if not expected_words:
            return 0.0

        overlap = len(actual_words & expected_words)
        return overlap / len(expected_words)

    def _check_relevance(self, retrieved: str, expected: str) -> float:
        """Check if retrieved info is relevant."""
        # Simplified relevance check
        return 0.8 if expected.lower() in retrieved.lower() else 0.3

# Demo
print("\n🔍 Example: Multi-hop evaluation")

evaluator = MultiHopEvaluator()

question = "Who was the president when the iPhone was released?"

reasoning_steps = [
    {
        'sub_question': 'When was the iPhone released?',
        'retrieved_info': 'The first iPhone was released on June 29, 2007.',
        'answer': '2007'
    },
    {
        'sub_question': 'Who was US president in 2007?',
        'retrieved_info': 'George W. Bush served as the 43rd president from 2001 to 2009.',
        'answer': 'George W. Bush'
    }
]

expected_steps = [
    {
        'sub_question': 'When was iPhone released?',
        'expected_info': '2007'
    },
    {
        'sub_question': 'Who was president in 2007?',
        'expected_info': 'George W. Bush'
    }
]

result = evaluator.evaluate_reasoning_path(
    question=question,
    reasoning_steps=reasoning_steps,
    expected_steps=expected_steps,
    final_answer="George W. Bush was president when the iPhone was released in 2007.",
    expected_answer="George W. Bush"
)

print(f"Question: {question}")
print(f"\nHops: {result['actual_hops']}/{result['expected_hops']}")
print(f"Step scores: {[f'{s:.2f}' for s in result['step_scores']]}")
print(f"Average step score: {result['avg_step_score']:.2f}")
print(f"Final answer correct: {'✓' if result['final_answer_correct'] else '✗'}")
print(f"Overall score: {result['overall_score']:.2f}")
print(f"Status: {'✓ PASS' if result['passed'] else '✗ FAIL'}")

# ============================================================================
# PART 2: ITERATIVE RETRIEVAL EVALUATION
# ============================================================================

print("\n\n" + "="*80)
print("PART 2: Iterative Retrieval Evaluation")
print("="*80)

print("""
🔄 ITERATIVE RETRIEVAL:

Initial query → Retrieve → Analyze → Refine query → Retrieve again

Example:
  Query: "Latest developments in quantum computing"
  1st retrieval: General quantum info
  Refined: "Quantum computing breakthroughs 2025"
  2nd retrieval: Recent specific advances

Evaluation:
- Track query refinements
- Measure improvement per iteration
- Check convergence
""")

class IterativeRetrievalEvaluator:
    """Evaluate iterative retrieval systems."""

    def evaluate_retrieval_iterations(
        self,
        original_query: str,
        iterations: List[Dict],
        ground_truth_docs: List[str]
    ) -> Dict[str, Any]:
        """Evaluate iterative retrieval process."""

        iteration_scores = []
        relevance_progression = []

        for i, iteration in enumerate(iterations):
            query = iteration['query']
            retrieved_docs = iteration['retrieved_docs']

            # Calculate relevance for this iteration
            relevance = self._calculate_relevance(retrieved_docs, ground_truth_docs)
            relevance_progression.append(relevance)

            iteration_scores.append({
                'iteration': i + 1,
                'query': query,
                'relevance': relevance,
                'num_docs': len(retrieved_docs)
            })

        # Check if retrieval improved
        improved = all(
            relevance_progression[i] <= relevance_progression[i+1]
            for i in range(len(relevance_progression)-1)
        ) if len(relevance_progression) > 1 else False

        # Final relevance
        final_relevance = relevance_progression[-1] if relevance_progression else 0

        # Convergence: did it plateau?
        converged = False
        if len(relevance_progression) >= 2:
            last_two = relevance_progression[-2:]
            converged = abs(last_two[1] - last_two[0]) < 0.05

        return {
            'num_iterations': len(iterations),
            'iteration_scores': iteration_scores,
            'relevance_progression': relevance_progression,
            'improved': improved,
            'final_relevance': final_relevance,
            'converged': converged,
            'improvement': relevance_progression[-1] - relevance_progression[0] if len(relevance_progression) > 1 else 0
        }

    def _calculate_relevance(
        self,
        retrieved_docs: List[str],
        ground_truth_docs: List[str]
    ) -> float:
        """Calculate relevance score."""
        if not ground_truth_docs:
            return 0.0

        # Count relevant retrieved docs
        relevant_count = sum(
            1 for doc in retrieved_docs
            if any(gt.lower() in doc.lower() for gt in ground_truth_docs)
        )

        return relevant_count / len(ground_truth_docs)

# Demo
print("\n🔄 Example: Iterative retrieval evaluation")

iter_evaluator = IterativeRetrievalEvaluator()

iterations = [
    {
        'query': 'quantum computing',
        'retrieved_docs': [
            'Quantum computing basics and history',
            'Introduction to qubits and superposition'
        ]
    },
    {
        'query': 'quantum computing recent advances 2025',
        'retrieved_docs': [
            'Google achieves quantum supremacy in 2025',
            'IBM announces 1000-qubit processor',
            'Quantum computing basics and history'
        ]
    },
    {
        'query': 'quantum computing breakthroughs 2025 error correction',
        'retrieved_docs': [
            'Google achieves quantum supremacy in 2025',
            'IBM announces 1000-qubit processor',
            'New error correction breakthrough enables stable qubits'
        ]
    }
]

ground_truth = [
    'Google achieves quantum supremacy',
    'IBM 1000-qubit processor',
    'error correction breakthrough'
]

result = iter_evaluator.evaluate_retrieval_iterations(
    original_query='quantum computing',
    iterations=iterations,
    ground_truth_docs=ground_truth
)

print(f"Iterations: {result['num_iterations']}")
print(f"Relevance progression: {[f'{r:.2f}' for r in result['relevance_progression']]}")
print(f"Improved: {'✓ Yes' if result['improved'] else '✗ No'}")
print(f"Final relevance: {result['final_relevance']:.2f}")
print(f"Improvement: {result['improvement']:+.2f}")
print(f"Converged: {'✓ Yes' if result['converged'] else '✗ No (needs more iterations)'}")

# ============================================================================
# PART 3: HYBRID SEARCH EVALUATION
# ============================================================================

print("\n\n" + "="*80)
print("PART 3: Hybrid Search Evaluation")
print("="*80)

print("""
🔀 HYBRID SEARCH:

Combine multiple retrieval methods:
- Semantic search (embeddings)
- Keyword search (BM25)
- Graph-based (knowledge graphs)

Evaluation questions:
- Does each method contribute?
- Is combination better than single method?
- Optimal weighting?
""")

class HybridSearchEvaluator:
    """Evaluate hybrid search strategies."""

    def evaluate_hybrid_retrieval(
        self,
        query: str,
        semantic_results: List[str],
        keyword_results: List[str],
        hybrid_results: List[str],
        ground_truth: List[str]
    ) -> Dict[str, Any]:
        """Compare individual methods vs hybrid."""

        # Score each method
        semantic_score = self._score_results(semantic_results, ground_truth)
        keyword_score = self._score_results(keyword_results, ground_truth)
        hybrid_score = self._score_results(hybrid_results, ground_truth)

        # Check if hybrid is better
        hybrid_better = hybrid_score > max(semantic_score, keyword_score)

        # Analyze contribution
        semantic_unique = set(semantic_results) - set(keyword_results)
        keyword_unique = set(keyword_results) - set(semantic_results)
        overlap = set(semantic_results) & set(keyword_results)

        return {
            'semantic_score': semantic_score,
            'keyword_score': keyword_score,
            'hybrid_score': hybrid_score,
            'hybrid_better': hybrid_better,
            'improvement': hybrid_score - max(semantic_score, keyword_score),
            'semantic_unique_count': len(semantic_unique),
            'keyword_unique_count': len(keyword_unique),
            'overlap_count': len(overlap),
            'best_method': 'hybrid' if hybrid_better else ('semantic' if semantic_score > keyword_score else 'keyword')
        }

    def _score_results(self, results: List[str], ground_truth: List[str]) -> float:
        """Score retrieval results."""
        if not ground_truth:
            return 0.0

        relevant = sum(
            1 for result in results
            if any(gt.lower() in result.lower() for gt in ground_truth)
        )

        # Precision and recall
        precision = relevant / len(results) if results else 0
        recall = relevant / len(ground_truth) if ground_truth else 0

        # F1 score
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)

# Demo
print("\n🔀 Example: Hybrid search evaluation")

hybrid_evaluator = HybridSearchEvaluator()

semantic_results = [
    "RAG systems retrieve relevant documents",
    "Vector embeddings enable semantic search",
    "Transformers power modern NLP"
]

keyword_results = [
    "RAG: Retrieval-Augmented Generation",
    "How RAG systems work",
    "Benefits of RAG for Q&A"
]

hybrid_results = [
    "RAG: Retrieval-Augmented Generation",
    "Vector embeddings enable semantic search",
    "How RAG systems work",
    "RAG systems retrieve relevant documents"
]

ground_truth = [
    "RAG systems",
    "retrieval",
    "semantic search"
]

result = hybrid_evaluator.evaluate_hybrid_retrieval(
    query="What is RAG?",
    semantic_results=semantic_results,
    keyword_results=keyword_results,
    hybrid_results=hybrid_results,
    ground_truth=ground_truth
)

print(f"Semantic score: {result['semantic_score']:.2f}")
print(f"Keyword score: {result['keyword_score']:.2f}")
print(f"Hybrid score: {result['hybrid_score']:.2f}")
print(f"Best method: {result['best_method']}")
print(f"Hybrid better: {'✓ Yes' if result['hybrid_better'] else '✗ No'}")
print(f"Improvement: {result['improvement']:+.2f}")
print(f"\nContributions:")
print(f"  Semantic unique: {result['semantic_unique_count']}")
print(f"  Keyword unique: {result['keyword_unique_count']}")
print(f"  Overlap: {result['overlap_count']}")

# ============================================================================
# PART 4: QUERY DECOMPOSITION EVALUATION
# ============================================================================

print("\n\n" + "="*80)
print("PART 4: Query Decomposition Evaluation")
print("="*80)

print("""
🧩 QUERY DECOMPOSITION:

Complex query: "Compare Python and JavaScript for web development"

Decomposed:
1. "Python features for web development"
2. "JavaScript features for web development"
3. "Python vs JavaScript comparison"

Evaluation:
- Are sub-queries complete?
- Do they cover the original query?
- Are they independent?
""")

class QueryDecompositionEvaluator:
    """Evaluate query decomposition strategies."""

    def evaluate_decomposition(
        self,
        original_query: str,
        sub_queries: List[str],
        expected_aspects: List[str]
    ) -> Dict[str, Any]:
        """Evaluate if decomposition covers all aspects."""

        # Check coverage of expected aspects
        aspects_covered = []
        for aspect in expected_aspects:
            covered = any(
                aspect.lower() in sub_q.lower()
                for sub_q in sub_queries
            )
            aspects_covered.append(covered)

        coverage_score = sum(aspects_covered) / len(expected_aspects) if expected_aspects else 0

        # Check for redundancy
        redundant_pairs = []
        for i, sq1 in enumerate(sub_queries):
            for j, sq2 in enumerate(sub_queries[i+1:], start=i+1):
                similarity = self._query_similarity(sq1, sq2)
                if similarity > 0.7:
                    redundant_pairs.append((i, j))

        has_redundancy = len(redundant_pairs) > 0

        # Check if queries are atomic (focused)
        atomic_scores = [self._is_atomic(sq) for sq in sub_queries]
        avg_atomic = sum(atomic_scores) / len(atomic_scores) if atomic_scores else 0

        return {
            'num_sub_queries': len(sub_queries),
            'coverage_score': coverage_score,
            'aspects_covered': sum(aspects_covered),
            'total_aspects': len(expected_aspects),
            'has_redundancy': has_redundancy,
            'redundant_pairs': redundant_pairs,
            'avg_atomicity': avg_atomic,
            'passed': coverage_score >= 0.8 and not has_redundancy and avg_atomic >= 0.7
        }

    def _query_similarity(self, q1: str, q2: str) -> float:
        """Calculate similarity between queries."""
        words1 = set(q1.lower().split())
        words2 = set(q2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    def _is_atomic(self, query: str) -> float:
        """Check if query is focused (not too broad)."""
        # Simple heuristic: check for 'and', 'or', multiple questions
        complexity_markers = ['and', 'or', '?.*?']
        word_count = len(query.split())

        # Penalize very long queries or those with multiple markers
        if word_count > 15:
            return 0.5
        if sum(1 for marker in complexity_markers if marker in query.lower()) > 1:
            return 0.6

        return 0.9

# Demo
print("\n🧩 Example: Query decomposition evaluation")

decomp_evaluator = QueryDecompositionEvaluator()

original = "Compare Python and JavaScript for web development"

sub_queries = [
    "Python features for web development",
    "JavaScript features for web development",
    "Comparison of Python and JavaScript"
]

expected_aspects = [
    "Python",
    "JavaScript",
    "web development",
    "comparison"
]

result = decomp_evaluator.evaluate_decomposition(
    original_query=original,
    sub_queries=sub_queries,
    expected_aspects=expected_aspects
)

print(f"Original: {original}")
print(f"Sub-queries: {result['num_sub_queries']}")
for i, sq in enumerate(sub_queries, 1):
    print(f"  {i}. {sq}")

print(f"\nCoverage: {result['aspects_covered']}/{result['total_aspects']} aspects ({result['coverage_score']:.0%})")
print(f"Redundancy: {'⚠️  Yes' if result['has_redundancy'] else '✓ No'}")
print(f"Atomicity: {result['avg_atomicity']:.2f}")
print(f"Status: {'✓ PASS' if result['passed'] else '✗ FAIL'}")

# ============================================================================
# PART 5: RE-RANKING EVALUATION
# ============================================================================

print("\n\n" + "="*80)
print("PART 5: Re-Ranking Evaluation")
print("="*80)

print("""
📊 RE-RANKING:

Initial retrieval: Fast but noisy
Re-ranking: Expensive but accurate

Process:
1. Retrieve top 100 with fast method
2. Re-rank top 20 with expensive model
3. Use top 5 for generation

Evaluation:
- Does re-ranking improve order?
- At what cost (latency)?
- Optimal k for re-ranking?
""")

class ReRankingEvaluator:
    """Evaluate re-ranking effectiveness."""

    def evaluate_reranking(
        self,
        initial_ranking: List[Tuple[str, float]],  # (doc, score)
        reranked_results: List[Tuple[str, float]],
        ground_truth_relevant: List[str],
        k: int = 5
    ) -> Dict[str, Any]:
        """Evaluate re-ranking effectiveness."""

        # Calculate metrics before and after
        initial_metrics = self._calculate_ranking_metrics(
            [doc for doc, _ in initial_ranking[:k]],
            ground_truth_relevant
        )

        reranked_metrics = self._calculate_ranking_metrics(
            [doc for doc, _ in reranked_results[:k]],
            ground_truth_relevant
        )

        # Improvement
        precision_improvement = reranked_metrics['precision'] - initial_metrics['precision']
        ndcg_improvement = reranked_metrics['ndcg'] - initial_metrics['ndcg']

        return {
            'k': k,
            'initial_precision': initial_metrics['precision'],
            'reranked_precision': reranked_metrics['precision'],
            'precision_improvement': precision_improvement,
            'initial_ndcg': initial_metrics['ndcg'],
            'reranked_ndcg': reranked_metrics['ndcg'],
            'ndcg_improvement': ndcg_improvement,
            'improved': precision_improvement > 0 or ndcg_improvement > 0
        }

    def _calculate_ranking_metrics(
        self,
        ranked_docs: List[str],
        relevant_docs: List[str]
    ) -> Dict[str, float]:
        """Calculate precision and NDCG."""

        # Precision@k
        relevant_retrieved = sum(
            1 for doc in ranked_docs
            if any(rel.lower() in doc.lower() for rel in relevant_docs)
        )
        precision = relevant_retrieved / len(ranked_docs) if ranked_docs else 0

        # Simplified NDCG
        dcg = 0
        for i, doc in enumerate(ranked_docs, 1):
            relevance = 1 if any(rel.lower() in doc.lower() for rel in relevant_docs) else 0
            dcg += relevance / math.log2(i + 1)

        # Ideal DCG (all relevant docs at top)
        idcg = sum(1 / math.log2(i + 1) for i in range(1, min(len(relevant_docs), len(ranked_docs)) + 1))

        ndcg = dcg / idcg if idcg > 0 else 0

        return {
            'precision': precision,
            'ndcg': ndcg
        }

# Demo
print("\n📊 Example: Re-ranking evaluation")

rerank_evaluator = ReRankingEvaluator()

initial_ranking = [
    ("Document about cats and pets", 0.75),
    ("General animal information", 0.72),
    ("Dogs are popular pets worldwide", 0.70),
    ("Cat behavior and psychology", 0.68),
    ("Pet care basics", 0.65)
]

reranked_results = [
    ("Cat behavior and psychology", 0.95),
    ("Document about cats and pets", 0.92),
    ("Pet care basics", 0.85),
    ("General animal information", 0.75),
    ("Dogs are popular pets worldwide", 0.60)
]

relevant_docs = ["cat", "feline"]

result = rerank_evaluator.evaluate_reranking(
    initial_ranking=initial_ranking,
    reranked_results=reranked_results,
    ground_truth_relevant=relevant_docs,
    k=5
)

print(f"Evaluating top-{result['k']} results:")
print(f"\nPrecision:")
print(f"  Initial: {result['initial_precision']:.2f}")
print(f"  Re-ranked: {result['reranked_precision']:.2f}")
print(f"  Improvement: {result['precision_improvement']:+.2f}")

print(f"\nNDCG:")
print(f"  Initial: {result['initial_ndcg']:.2f}")
print(f"  Re-ranked: {result['reranked_ndcg']:.2f}")
print(f"  Improvement: {result['ndcg_improvement']:+.2f}")

print(f"\nOverall: {'✓ Improved' if result['improved'] else '✗ No improvement'}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "="*80)
print("KEY TAKEAWAYS")
print("="*80)

print("""
✅ ADVANCED RAG PATTERNS:

1. MULTI-HOP REASONING
   - Evaluate each reasoning step
   - Verify final synthesis
   - Track intermediate results

2. ITERATIVE RETRIEVAL
   - Measure improvement per iteration
   - Check convergence
   - Monitor query refinement

3. HYBRID SEARCH
   - Compare individual methods
   - Verify hybrid adds value
   - Analyze unique contributions

4. QUERY DECOMPOSITION
   - Check aspect coverage
   - Detect redundancy
   - Ensure atomicity

5. RE-RANKING
   - Measure ranking improvement
   - Consider cost/benefit
   - Optimize k parameter

🎯 EVALUATION STRATEGIES:

✓ Test each component separately
✓ Measure end-to-end performance
✓ Track improvements over baseline
✓ Consider latency/cost trade-offs
✓ Use diverse test cases

⚠️  COMMON PITFALLS:

✗ Over-engineering (too complex)
✗ Ignoring latency costs
✗ Not comparing to baseline
✗ Testing only happy paths
✗ Missing edge cases

💡 REMEMBER:

"Advanced RAG patterns should measurably improve results.
 Always compare against simpler baselines to justify complexity."

🔄 WHEN TO USE WHAT:

- Multi-hop: Complex questions requiring multiple facts
- Iterative: Ambiguous queries needing refinement
- Hybrid: When single method insufficient
- Decomposition: Compound questions
- Re-ranking: When recall > precision initially

Next: 13_multi_agent_evaluation.py - Evaluate agent systems!
""")

print("\n" + "="*80)
print("✨ Lesson 12 Complete!")
print("="*80)
print("\nNext: Run 13_multi_agent_evaluation.py")
