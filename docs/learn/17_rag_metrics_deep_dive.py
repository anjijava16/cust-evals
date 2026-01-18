"""
Lesson 17: RAG Metrics Deep Dive (Expert)

Comprehensive coverage of all RAG-specific evaluation metrics including
retrieval metrics, grounding/faithfulness, answer quality, context quality,
and latency/cost considerations.

Prerequisites: Lessons 1-16, especially Lesson 4 and 12
Difficulty: ⭐⭐⭐⭐ Expert
Time: 70 minutes
"""

print("="*80)
print("LESSON 17: RAG Metrics Deep Dive")
print("="*80)

print("""
🔍 COMPREHENSIVE RAG EVALUATION

RAG systems have multiple components to evaluate:
1. Retrieval Quality (are the right documents retrieved?)
2. Grounding & Faithfulness (is the answer based on retrieved docs?)
3. Answer Quality (is the final answer good?)
4. Context Quality (are retrieved docs relevant and useful?)
5. Latency & Cost (is the system efficient?)

This lesson provides comprehensive metrics for each dimension.
""")

from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict
import math

# ============================================================================
# PART 1: RETRIEVAL METRICS
# ============================================================================

print("\n" + "="*80)
print("PART 1: Retrieval Metrics - Measuring Retrieval Quality")
print("="*80)

print("""
📊 RETRIEVAL METRICS:

Key metrics for evaluating retrieval:
1. Recall@K: Of relevant docs, how many in top K?
2. Precision@K: Of top K docs, how many relevant?
3. Mean Reciprocal Rank (MRR): Position of first relevant doc
4. NDCG: Discounted cumulative gain (considers ranking)
5. Hit Rate: % of queries with ≥1 relevant doc in top K
6. Coverage: % of corpus that can be retrieved

Each metric tells a different story about retrieval quality.
""")

class RetrievalMetrics:
    """Comprehensive retrieval evaluation metrics."""

    def recall_at_k(
        self,
        retrieved_ids: List[str],
        relevant_ids: List[str],
        k: int
    ) -> float:
        """
        Recall@K: What fraction of relevant docs are in top K?

        Formula: |relevant ∩ top_k| / |relevant|
        """
        top_k = set(retrieved_ids[:k])
        relevant = set(relevant_ids)

        if not relevant:
            return 0.0

        return len(top_k & relevant) / len(relevant)

    def precision_at_k(
        self,
        retrieved_ids: List[str],
        relevant_ids: List[str],
        k: int
    ) -> float:
        """
        Precision@K: What fraction of top K docs are relevant?

        Formula: |relevant ∩ top_k| / K
        """
        top_k = set(retrieved_ids[:k])
        relevant = set(relevant_ids)

        if k == 0:
            return 0.0

        return len(top_k & relevant) / k

    def f1_at_k(
        self,
        retrieved_ids: List[str],
        relevant_ids: List[str],
        k: int
    ) -> float:
        """F1@K: Harmonic mean of Precision@K and Recall@K."""
        precision = self.precision_at_k(retrieved_ids, relevant_ids, k)
        recall = self.recall_at_k(retrieved_ids, relevant_ids, k)

        if precision + recall == 0:
            return 0.0

        return 2 * (precision * recall) / (precision + recall)

    def mean_reciprocal_rank(
        self,
        retrieved_ids: List[str],
        relevant_ids: List[str]
    ) -> float:
        """
        MRR: Reciprocal of rank of first relevant document.

        Example: First relevant at position 3 → MRR = 1/3 = 0.333
        """
        relevant = set(relevant_ids)

        for rank, doc_id in enumerate(retrieved_ids, start=1):
            if doc_id in relevant:
                return 1.0 / rank

        return 0.0  # No relevant doc found

    def ndcg_at_k(
        self,
        retrieved_ids: List[str],
        relevant_ids: List[str],
        relevance_scores: Dict[str, float],
        k: int
    ) -> float:
        """
        NDCG@K: Normalized Discounted Cumulative Gain.

        Considers both:
        - Relevance scores (not just binary)
        - Position (earlier = better)

        Formula: DCG / IDCG
        DCG = Σ (relevance / log2(position + 1))
        """
        # Calculate DCG
        dcg = 0.0
        for i, doc_id in enumerate(retrieved_ids[:k], start=1):
            relevance = relevance_scores.get(doc_id, 0.0)
            dcg += relevance / math.log2(i + 1)

        # Calculate IDCG (ideal DCG with perfect ranking)
        ideal_relevances = sorted(
            [relevance_scores.get(doc_id, 0.0) for doc_id in relevant_ids],
            reverse=True
        )[:k]

        idcg = 0.0
        for i, relevance in enumerate(ideal_relevances, start=1):
            idcg += relevance / math.log2(i + 1)

        if idcg == 0:
            return 0.0

        return dcg / idcg

    def hit_rate_at_k(
        self,
        queries: List[Dict[str, Any]],
        k: int
    ) -> float:
        """
        Hit Rate@K: % of queries with at least one relevant doc in top K.

        Args:
            queries: List of {retrieved_ids, relevant_ids}
        """
        hits = 0

        for query in queries:
            top_k = set(query['retrieved_ids'][:k])
            relevant = set(query['relevant_ids'])

            if len(top_k & relevant) > 0:
                hits += 1

        return hits / len(queries) if queries else 0.0

    def coverage(
        self,
        retrieved_docs: List[List[str]],
        corpus_size: int
    ) -> float:
        """
        Coverage: What fraction of corpus can be retrieved?

        Measures retrieval system's breadth.
        """
        all_retrieved = set()
        for docs in retrieved_docs:
            all_retrieved.update(docs)

        return len(all_retrieved) / corpus_size if corpus_size > 0 else 0.0

# Demo
print("\n📊 Example: Retrieval Metrics")

retrieval_metrics = RetrievalMetrics()

# Simulated retrieval results
retrieved_ids = ["doc3", "doc1", "doc5", "doc2", "doc7"]
relevant_ids = ["doc1", "doc2", "doc4"]
relevance_scores = {
    "doc1": 0.9,
    "doc2": 0.7,
    "doc3": 0.0,
    "doc4": 0.8,
    "doc5": 0.1,
    "doc7": 0.0
}

k = 3

print(f"Retrieved (top {k}): {retrieved_ids[:k]}")
print(f"Relevant docs: {relevant_ids}\n")

recall = retrieval_metrics.recall_at_k(retrieved_ids, relevant_ids, k)
precision = retrieval_metrics.precision_at_k(retrieved_ids, relevant_ids, k)
f1 = retrieval_metrics.f1_at_k(retrieved_ids, relevant_ids, k)
mrr = retrieval_metrics.mean_reciprocal_rank(retrieved_ids, relevant_ids)
ndcg = retrieval_metrics.ndcg_at_k(retrieved_ids, relevant_ids, relevance_scores, k)

print(f"Recall@{k}: {recall:.3f} (found {recall*len(relevant_ids):.0f}/{len(relevant_ids)} relevant docs)")
print(f"Precision@{k}: {precision:.3f} ({precision*k:.0f}/{k} retrieved are relevant)")
print(f"F1@{k}: {f1:.3f}")
print(f"MRR: {mrr:.3f} (first relevant at position {1/mrr if mrr > 0 else 'N/A'})")
print(f"NDCG@{k}: {ndcg:.3f}")

# ============================================================================
# PART 2: GROUNDING & FAITHFULNESS
# ============================================================================

print("\n\n" + "="*80)
print("PART 2: Grounding & Faithfulness - Answer Attribution")
print("="*80)

print("""
🔗 GROUNDING & FAITHFULNESS:

Critical for RAG: Is the answer based on retrieved documents?

Metrics:
1. Faithfulness Score: Answer supported by context
2. Groundedness: No hallucinated information
3. Attribution Accuracy: Correct citation/sourcing
4. Citation Precision/Recall: Citation quality

Hallucination in RAG is especially problematic!
""")

class GroundingMetrics:
    """Evaluate grounding and faithfulness of RAG answers."""

    def faithfulness_score(
        self,
        answer: str,
        context: str,
        granularity: str = 'sentence'
    ) -> Dict[str, Any]:
        """
        Faithfulness: All claims in answer supported by context.

        Args:
            answer: Generated answer
            context: Retrieved documents
            granularity: 'sentence' or 'claim'
        """
        # Extract claims from answer
        if granularity == 'sentence':
            claims = self._extract_sentences(answer)
        else:
            claims = self._extract_claims(answer)

        # Check each claim against context
        supported_claims = []
        unsupported_claims = []

        for claim in claims:
            if self._is_supported(claim, context):
                supported_claims.append(claim)
            else:
                unsupported_claims.append(claim)

        total_claims = len(claims)
        faithfulness = len(supported_claims) / total_claims if total_claims > 0 else 0.0

        return {
            'faithfulness_score': faithfulness,
            'total_claims': total_claims,
            'supported': len(supported_claims),
            'unsupported': len(unsupported_claims),
            'is_faithful': faithfulness >= 0.9,  # 90% threshold
            'unsupported_claims': unsupported_claims[:3]  # Show first 3
        }

    def groundedness_check(
        self,
        answer: str,
        context: str
    ) -> Dict[str, Any]:
        """
        Groundedness: Check for hallucinated information.

        Stricter than faithfulness - checks for any invented content.
        """
        # Extract entities and facts from answer
        answer_entities = self._extract_entities(answer)
        context_entities = self._extract_entities(context)

        # Check if answer entities are in context
        grounded_entities = answer_entities & context_entities
        hallucinated_entities = answer_entities - context_entities

        groundedness = len(grounded_entities) / len(answer_entities) if answer_entities else 1.0

        return {
            'groundedness_score': groundedness,
            'grounded_entities': list(grounded_entities),
            'hallucinated_entities': list(hallucinated_entities),
            'is_grounded': len(hallucinated_entities) == 0
        }

    def attribution_accuracy(
        self,
        answer: str,
        citations: List[Dict[str, Any]],
        context_docs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Attribution Accuracy: Are citations correct?

        Args:
            answer: Generated answer
            citations: List of {claim, cited_doc_id}
            context_docs: List of {doc_id, content}
        """
        correct_citations = 0
        incorrect_citations = 0

        doc_map = {doc['doc_id']: doc['content'] for doc in context_docs}

        for citation in citations:
            claim = citation['claim']
            cited_doc_id = citation['cited_doc_id']

            if cited_doc_id in doc_map:
                doc_content = doc_map[cited_doc_id]
                if self._is_supported(claim, doc_content):
                    correct_citations += 1
                else:
                    incorrect_citations += 1
            else:
                incorrect_citations += 1  # Cited non-existent doc

        total = len(citations)
        accuracy = correct_citations / total if total > 0 else 0.0

        return {
            'attribution_accuracy': accuracy,
            'correct_citations': correct_citations,
            'incorrect_citations': incorrect_citations,
            'total_citations': total
        }

    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text."""
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]

    def _extract_claims(self, text: str) -> List[str]:
        """Extract factual claims (simplified)."""
        # For simplicity, use sentences as claims
        return self._extract_sentences(text)

    def _is_supported(self, claim: str, context: str) -> bool:
        """Check if claim is supported by context (simplified)."""
        claim_words = set(claim.lower().split())
        context_words = set(context.lower().split())

        # Simple word overlap check (real system would use NLI model)
        overlap = len(claim_words & context_words)
        return overlap >= len(claim_words) * 0.6  # 60% overlap

    def _extract_entities(self, text: str) -> Set[str]:
        """Extract entities (simplified - uses capitalized words)."""
        import re
        # Find capitalized words (simplified entity extraction)
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        return set(entities)

# Demo
print("\n🔗 Example: Grounding & Faithfulness")

grounding_metrics = GroundingMetrics()

context = """
Paris is the capital and largest city of France.
It is located on the River Seine. The city has an estimated population
of 2.2 million residents. The Eiffel Tower is located in Paris.
"""

answer1 = "Paris is the capital of France with 2.2 million residents."
answer2 = "Paris is the capital of Germany with 5 million residents."

print(f"Context: {context[:100]}...\n")

for i, answer in enumerate([answer1, answer2], 1):
    result = grounding_metrics.faithfulness_score(answer, context)

    print(f"Answer {i}: '{answer}'")
    print(f"  Faithfulness: {result['faithfulness_score']:.1%}")
    print(f"  Supported claims: {result['supported']}/{result['total_claims']}")
    print(f"  Is Faithful: {'✓ YES' if result['is_faithful'] else '✗ NO'}")
    if result['unsupported_claims']:
        print(f"  Unsupported: {result['unsupported_claims']}")
    print()

# ============================================================================
# PART 3: ANSWER QUALITY METRICS
# ============================================================================

print("\n" + "="*80)
print("PART 3: Answer Quality - End-to-End Evaluation")
print("="*80)

print("""
✅ ANSWER QUALITY METRICS:

Beyond retrieval, evaluate the final answer:
1. Answer Correctness: Is it factually correct?
2. Answer Relevance: Does it address the question?
3. Answer Completeness: Is it comprehensive?
4. Answer Consistency: No self-contradictions?

These capture end-to-end RAG quality.
""")

class AnswerQualityMetrics:
    """Evaluate RAG answer quality."""

    def answer_correctness(
        self,
        answer: str,
        ground_truth: str,
        semantic_similarity_fn: callable = None
    ) -> Dict[str, Any]:
        """
        Answer Correctness: Match with ground truth.

        Combines exact match and semantic similarity.
        """
        # Exact match component
        answer_lower = answer.lower().strip()
        truth_lower = ground_truth.lower().strip()

        exact_match = answer_lower == truth_lower

        # Word overlap component
        answer_words = set(answer_lower.split())
        truth_words = set(truth_lower.split())

        if truth_words:
            word_overlap = len(answer_words & truth_words) / len(truth_words)
        else:
            word_overlap = 0.0

        # Semantic similarity (if function provided)
        if semantic_similarity_fn:
            semantic_sim = semantic_similarity_fn(answer, ground_truth)
        else:
            semantic_sim = word_overlap  # Fallback

        # Combined score
        correctness = (word_overlap * 0.5) + (semantic_sim * 0.5)

        return {
            'correctness_score': correctness,
            'exact_match': exact_match,
            'word_overlap': word_overlap,
            'semantic_similarity': semantic_sim,
            'is_correct': correctness >= 0.7
        }

    def answer_relevance(
        self,
        question: str,
        answer: str
    ) -> Dict[str, Any]:
        """
        Answer Relevance: Does answer address the question?
        """
        # Extract key terms from question
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())

        # Remove stop words (simplified)
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of'}
        question_keywords = question_words - stop_words
        answer_keywords = answer_words - stop_words

        if not question_keywords:
            return {'relevance_score': 0.0, 'is_relevant': False}

        # Calculate overlap
        overlap = len(question_keywords & answer_keywords)
        relevance = overlap / len(question_keywords)

        return {
            'relevance_score': relevance,
            'question_keywords_covered': overlap,
            'total_question_keywords': len(question_keywords),
            'is_relevant': relevance >= 0.5
        }

    def answer_completeness(
        self,
        answer: str,
        expected_aspects: List[str]
    ) -> Dict[str, Any]:
        """
        Answer Completeness: Covers all required aspects?

        Args:
            expected_aspects: List of aspects that should be covered
        """
        answer_lower = answer.lower()

        covered_aspects = []
        missing_aspects = []

        for aspect in expected_aspects:
            if aspect.lower() in answer_lower:
                covered_aspects.append(aspect)
            else:
                missing_aspects.append(aspect)

        completeness = len(covered_aspects) / len(expected_aspects) if expected_aspects else 0.0

        return {
            'completeness_score': completeness,
            'covered_aspects': covered_aspects,
            'missing_aspects': missing_aspects,
            'is_complete': completeness >= 0.8
        }

    def answer_consistency(
        self,
        answer: str
    ) -> Dict[str, Any]:
        """
        Answer Consistency: No self-contradictions?

        Simplified check for obvious contradictions.
        """
        sentences = self._split_sentences(answer)

        # Check for negation patterns that might contradict
        contradictions_found = 0

        for i, sent1 in enumerate(sentences):
            for sent2 in sentences[i+1:]:
                if self._check_contradiction(sent1, sent2):
                    contradictions_found += 1

        consistency = 1.0 - min(1.0, contradictions_found * 0.3)

        return {
            'consistency_score': consistency,
            'contradictions_found': contradictions_found,
            'is_consistent': contradictions_found == 0
        }

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re
        return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]

    def _check_contradiction(self, sent1: str, sent2: str) -> bool:
        """Check if two sentences contradict (very simplified)."""
        # Look for opposite assertions
        sent1_lower = sent1.lower()
        sent2_lower = sent2.lower()

        # If one has "not" and shares words, might be contradiction
        if ('not' in sent1_lower) != ('not' in sent2_lower):
            words1 = set(sent1_lower.split())
            words2 = set(sent2_lower.split())
            overlap = len(words1 & words2)

            if overlap > 3:  # Significant overlap
                return True

        return False

# Demo
print("\n✅ Example: Answer Quality Metrics")

answer_metrics = AnswerQualityMetrics()

question = "What is the capital of France and what is its population?"
answer = "Paris is the capital of France. The city has approximately 2.2 million residents."
ground_truth = "The capital of France is Paris, with a population of about 2.2 million."

expected_aspects = ["capital", "Paris", "population", "2.2 million"]

correctness = answer_metrics.answer_correctness(answer, ground_truth)
relevance = answer_metrics.answer_relevance(question, answer)
completeness = answer_metrics.answer_completeness(answer, expected_aspects)
consistency = answer_metrics.answer_consistency(answer)

print(f"Question: {question}")
print(f"Answer: {answer}\n")

print(f"Correctness: {correctness['correctness_score']:.1%} ({'✓' if correctness['is_correct'] else '✗'})")
print(f"Relevance: {relevance['relevance_score']:.1%} ({'✓' if relevance['is_relevant'] else '✗'})")
print(f"Completeness: {completeness['completeness_score']:.1%} ({'✓' if completeness['is_complete'] else '✗'})")
print(f"Consistency: {consistency['consistency_score']:.1%} ({'✓' if consistency['is_consistent'] else '✗'})")

# ============================================================================
# PART 4: CONTEXT QUALITY METRICS
# ============================================================================

print("\n\n" + "="*80)
print("PART 4: Context Quality - Retrieved Document Evaluation")
print("="*80)

print("""
📄 CONTEXT QUALITY:

Evaluate retrieved documents themselves:
1. Context Relevance: Are docs relevant to query?
2. Context Utilization: Is retrieved context used?
3. Context Redundancy: How much overlap between docs?
4. Noise Sensitivity: Does irrelevant context hurt?

Good retrieval ≠ good context quality!
""")

class ContextQualityMetrics:
    """Evaluate quality of retrieved context."""

    def context_relevance(
        self,
        query: str,
        retrieved_docs: List[str]
    ) -> Dict[str, Any]:
        """
        Context Relevance: Are retrieved documents relevant to query?
        """
        query_words = set(query.lower().split())

        relevance_scores = []
        for doc in retrieved_docs:
            doc_words = set(doc.lower().split())
            overlap = len(query_words & doc_words)
            doc_relevance = overlap / len(query_words) if query_words else 0.0
            relevance_scores.append(doc_relevance)

        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0

        return {
            'average_relevance': avg_relevance,
            'relevance_scores': relevance_scores,
            'highly_relevant_docs': sum(1 for r in relevance_scores if r >= 0.5),
            'total_docs': len(retrieved_docs)
        }

    def context_utilization_ratio(
        self,
        answer: str,
        retrieved_docs: List[str]
    ) -> Dict[str, Any]:
        """
        Context Utilization: How much of retrieved context is used in answer?
        """
        answer_words = set(answer.lower().split())

        utilized_docs = 0
        for doc in retrieved_docs:
            doc_words = set(doc.lower().split())
            overlap = len(answer_words & doc_words)

            # If significant overlap, doc was utilized
            if overlap >= len(doc_words) * 0.3:  # 30% threshold
                utilized_docs += 1

        utilization = utilized_docs / len(retrieved_docs) if retrieved_docs else 0.0

        return {
            'utilization_ratio': utilization,
            'utilized_docs': utilized_docs,
            'total_docs': len(retrieved_docs),
            'unused_docs': len(retrieved_docs) - utilized_docs
        }

    def context_redundancy(
        self,
        retrieved_docs: List[str]
    ) -> Dict[str, Any]:
        """
        Context Redundancy: How much overlap between documents?

        High redundancy = wasted context window
        """
        if len(retrieved_docs) < 2:
            return {'redundancy_score': 0.0, 'unique_info_ratio': 1.0}

        # Calculate pairwise similarity
        similarities = []
        for i, doc1 in enumerate(retrieved_docs):
            for doc2 in retrieved_docs[i+1:]:
                sim = self._jaccard_similarity(doc1, doc2)
                similarities.append(sim)

        avg_redundancy = sum(similarities) / len(similarities) if similarities else 0.0
        unique_info = 1.0 - avg_redundancy

        return {
            'redundancy_score': avg_redundancy,
            'unique_info_ratio': unique_info,
            'is_redundant': avg_redundancy > 0.7,
            'pairwise_similarities': similarities
        }

    def noise_sensitivity(
        self,
        answer_with_noise: str,
        answer_without_noise: str,
        noise_ratio: float
    ) -> Dict[str, Any]:
        """
        Noise Sensitivity: Does irrelevant context degrade quality?

        Compare answers with/without noisy documents.
        """
        # Calculate similarity between answers
        similarity = self._text_similarity(answer_with_noise, answer_without_noise)

        # Inverse of similarity shows sensitivity to noise
        sensitivity = 1.0 - similarity

        return {
            'noise_sensitivity': sensitivity,
            'answer_similarity': similarity,
            'noise_ratio': noise_ratio,
            'is_robust': sensitivity < 0.3  # Less than 30% degradation
        }

    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between texts."""
        return self._jaccard_similarity(text1, text2)

# Demo
print("\n📄 Example: Context Quality Metrics")

context_metrics = ContextQualityMetrics()

query = "What is machine learning?"
retrieved_docs = [
    "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
    "Machine learning algorithms can identify patterns in large datasets automatically.",
    "AI and machine learning are transforming how we process information."  # Somewhat redundant
]
answer = "Machine learning is a subset of AI that learns from data and identifies patterns."

relevance = context_metrics.context_relevance(query, retrieved_docs)
utilization = context_metrics.context_utilization_ratio(answer, retrieved_docs)
redundancy = context_metrics.context_redundancy(retrieved_docs)

print(f"Query: {query}")
print(f"Retrieved {len(retrieved_docs)} documents\n")

print(f"Context Relevance: {relevance['average_relevance']:.1%}")
print(f"  Highly relevant: {relevance['highly_relevant_docs']}/{relevance['total_docs']}")

print(f"\nContext Utilization: {utilization['utilization_ratio']:.1%}")
print(f"  Utilized: {utilization['utilized_docs']}/{utilization['total_docs']}")
print(f"  Unused: {utilization['unused_docs']}")

print(f"\nContext Redundancy: {redundancy['redundancy_score']:.1%}")
print(f"  Unique info: {redundancy['unique_info_ratio']:.1%}")
print(f"  Is Redundant: {'⚠️  YES' if redundancy['is_redundant'] else '✓ NO'}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "="*80)
print("KEY TAKEAWAYS")
print("="*80)

print("""
✅ COMPREHENSIVE RAG EVALUATION:

1. RETRIEVAL METRICS
   ✓ Recall@K: Coverage of relevant docs
   ✓ Precision@K: Quality of top-K results
   ✓ MRR: Ranking quality
   ✓ NDCG: Graded relevance + ranking
   ✓ Target: Recall@5 > 0.8, NDCG@5 > 0.7

2. GROUNDING & FAITHFULNESS
   ✓ Faithfulness: Answer supported by context
   ✓ Groundedness: No hallucinations
   ✓ Attribution: Correct citations
   ✓ Target: Faithfulness > 0.95

3. ANSWER QUALITY
   ✓ Correctness: Factually accurate
   ✓ Relevance: Addresses question
   ✓ Completeness: Comprehensive
   ✓ Consistency: No contradictions
   ✓ Target: All > 0.8

4. CONTEXT QUALITY
   ✓ Relevance: Docs match query
   ✓ Utilization: Context actually used
   ✓ Redundancy: Minimal overlap
   ✓ Noise sensitivity: Robust to irrelevant docs
   ✓ Target: Relevance > 0.7, Redundancy < 0.5

5. EFFICIENCY
   ✓ Retrieval latency: < 100ms
   ✓ End-to-end latency: < 2s
   ✓ Cost per query: Track tokens
   ✓ Context window usage: < 80%

📊 RAG EVALUATION DASHBOARD:

Essential Metrics to Monitor:
┌─────────────────────────────────────────┐
│ Retrieval: Recall@5, NDCG@5            │
│ Grounding: Faithfulness                 │
│ Answer: Correctness, Relevance          │
│ Context: Relevance, Utilization         │
│ Efficiency: Latency, Cost               │
└─────────────────────────────────────────┘

🎯 RECOMMENDED TESTING STRATEGY:

1. Offline Evaluation:
   - Build test set with ground truth
   - Measure all retrieval metrics
   - Check faithfulness on samples
   - Track answer quality

2. Online Monitoring:
   - Track latency percentiles
   - Monitor retrieval hit rates
   - Sample faithfulness checks
   - User feedback collection

3. Continuous Improvement:
   - A/B test retrieval changes
   - Optimize context window usage
   - Fine-tune ranking
   - Improve grounding

⚠️  COMMON RAG ISSUES & DIAGNOSTICS:

Low Answer Quality?
├─ Check Retrieval: Recall@5 low?
├─ Check Grounding: Faithfulness low?
├─ Check Context: Relevance low?
└─ Check Generation: Model capability

High Hallucination?
├─ Improve retrieval recall
├─ Add faithfulness constraints
├─ Better context filtering
└─ Stronger grounding prompts

Slow Response Time?
├─ Optimize retrieval (HNSW, quantization)
├─ Reduce context length
├─ Use smaller models
└─ Implement caching

💡 BEST PRACTICES:

1. Start Simple:
   - Get retrieval right first
   - Measure end-to-end before optimizing parts
   - Use standard metrics initially

2. Comprehensive Testing:
   - Test all components separately
   - Measure end-to-end quality
   - Include edge cases

3. Balance Trade-offs:
   - Recall vs Precision
   - Quality vs Latency
   - Coverage vs Relevance
   - Context length vs Cost

4. Continuous Monitoring:
   - Track metrics over time
   - Detect degradation early
   - Regular human evaluation
   - User feedback loops

Next: 18_agent_systems_evaluation.py - Agent metrics!
""")

print("\n" + "="*80)
print("✨ Lesson 17 Complete!")
print("="*80)
print("\nNext: Run 18_agent_systems_evaluation.py")
