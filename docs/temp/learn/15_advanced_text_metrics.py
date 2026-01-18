"""
Lesson 15: Advanced Text Quality & Similarity Metrics (Expert)

Deep dive into sophisticated text evaluation metrics used in NLP and LLM evaluation:
BLEU, ROUGE, METEOR, BERTScore, BLEURT, and Perplexity.

Prerequisites: Lessons 1-14
Difficulty: ⭐⭐⭐⭐ Expert
Time: 60 minutes
"""

print("="*80)
print("LESSON 15: Advanced Text Quality & Similarity Metrics")
print("="*80)

print("""
📊 BEYOND SIMPLE METRICS

We've covered basic metrics (exact match, word overlap).
Now: Industry-standard metrics used in research and production.

Metric Categories:
1. N-gram Overlap (BLEU, ROUGE, METEOR)
2. Embedding-based (BERTScore)
3. Learned Metrics (BLEURT)
4. Probabilistic (Perplexity)

Each metric has specific use cases, strengths, and limitations.
""")

from typing import List, Dict, Any, Tuple, Set
from collections import Counter
import math
import re

# ============================================================================
# PART 1: BLEU SCORE (Machine Translation)
# ============================================================================

print("\n" + "="*80)
print("PART 1: BLEU Score - Bilingual Evaluation Understudy")
print("="*80)

print("""
📝 BLEU SCORE:

Originally for machine translation, now used for text generation.

Key Concepts:
- N-gram precision (1-gram, 2-gram, 3-gram, 4-gram)
- Brevity penalty (penalizes too-short outputs)
- Geometric mean of precisions

Formula: BLEU = BP × exp(Σ wn × log pn)
  - BP: Brevity penalty
  - pn: n-gram precision
  - wn: weights (usually uniform: 0.25 each for n=1,2,3,4)

Range: 0.0 (worst) to 1.0 (perfect match)

Use Cases:
✓ Machine translation
✓ Text summarization
✓ Paraphrase generation
✗ Creative writing (too strict)
✗ Semantic similarity (surface-level only)
""")

class BLEUScore:
    """Calculate BLEU score for text evaluation."""

    def __init__(self, max_n: int = 4):
        self.max_n = max_n

    def calculate(
        self,
        candidate: str,
        references: List[str],
        weights: Tuple[float, ...] = (0.25, 0.25, 0.25, 0.25)
    ) -> Dict[str, Any]:
        """
        Calculate BLEU score.

        Args:
            candidate: Generated text
            references: List of reference texts
            weights: Weights for n-gram precisions
        """
        candidate_tokens = self._tokenize(candidate)
        references_tokens = [self._tokenize(ref) for ref in references]

        # Calculate n-gram precisions
        precisions = []
        for n in range(1, self.max_n + 1):
            precision = self._modified_precision(candidate_tokens, references_tokens, n)
            precisions.append(precision)

        # Brevity penalty
        bp = self._brevity_penalty(candidate_tokens, references_tokens)

        # Calculate BLEU
        if min(precisions) > 0:
            log_precisions = [w * math.log(p) for w, p in zip(weights, precisions)]
            bleu = bp * math.exp(sum(log_precisions))
        else:
            bleu = 0.0

        return {
            'bleu': bleu,
            'precisions': precisions,
            'brevity_penalty': bp,
            'candidate_length': len(candidate_tokens),
            'reference_length': self._effective_reference_length(references_tokens)
        }

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        return text.lower().split()

    def _get_ngrams(self, tokens: List[str], n: int) -> Counter:
        """Extract n-grams from tokens."""
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngrams.append(tuple(tokens[i:i+n]))
        return Counter(ngrams)

    def _modified_precision(
        self,
        candidate: List[str],
        references: List[List[str]],
        n: int
    ) -> float:
        """Calculate modified n-gram precision."""
        candidate_ngrams = self._get_ngrams(candidate, n)

        if not candidate_ngrams:
            return 0.0

        # Maximum reference count for each n-gram
        max_ref_counts = Counter()
        for ref in references:
            ref_ngrams = self._get_ngrams(ref, n)
            for ngram in ref_ngrams:
                max_ref_counts[ngram] = max(max_ref_counts[ngram], ref_ngrams[ngram])

        # Clipped counts
        clipped_counts = {}
        for ngram, count in candidate_ngrams.items():
            clipped_counts[ngram] = min(count, max_ref_counts.get(ngram, 0))

        numerator = sum(clipped_counts.values())
        denominator = sum(candidate_ngrams.values())

        return numerator / denominator if denominator > 0 else 0.0

    def _brevity_penalty(
        self,
        candidate: List[str],
        references: List[List[str]]
    ) -> float:
        """Calculate brevity penalty."""
        c = len(candidate)
        r = self._effective_reference_length(references)

        if c > r:
            return 1.0
        elif c == 0:
            return 0.0
        else:
            return math.exp(1 - r/c)

    def _effective_reference_length(self, references: List[List[str]]) -> int:
        """Get closest reference length."""
        return min(len(ref) for ref in references) if references else 0

# Demo
print("\n📊 Example: BLEU Score Calculation")

bleu_scorer = BLEUScore()

candidate = "the cat is on the mat"
references = [
    "the cat is sitting on the mat",
    "there is a cat on the mat"
]

result = bleu_scorer.calculate(candidate, references)

print(f"Candidate: '{candidate}'")
print(f"References:")
for i, ref in enumerate(references, 1):
    print(f"  {i}. '{ref}'")

print(f"\nBLEU Score: {result['bleu']:.4f}")
print(f"Precisions:")
for i, p in enumerate(result['precisions'], 1):
    print(f"  {i}-gram: {p:.4f}")
print(f"Brevity penalty: {result['brevity_penalty']:.4f}")

# ============================================================================
# PART 2: ROUGE SCORES (Summarization)
# ============================================================================

print("\n\n" + "="*80)
print("PART 2: ROUGE Scores - Recall-Oriented Understudy for Gisting Evaluation")
print("="*80)

print("""
📝 ROUGE SCORES:

Designed for summarization evaluation (recall-based, not precision).

Variants:
- ROUGE-N: N-gram overlap (ROUGE-1, ROUGE-2, ROUGE-3, etc.)
- ROUGE-L: Longest Common Subsequence
- ROUGE-S: Skip-bigram co-occurrence

Key Difference from BLEU:
- BLEU: Precision-based (how much of candidate is good)
- ROUGE: Recall-based (how much of reference is captured)

Range: 0.0 to 1.0 for each metric

Use Cases:
✓ Summarization (primary use)
✓ Question answering
✓ Caption generation
✗ Translation (BLEU better)
""")

class ROUGEScore:
    """Calculate ROUGE scores for text evaluation."""

    def calculate_rouge_n(
        self,
        candidate: str,
        reference: str,
        n: int = 1
    ) -> Dict[str, float]:
        """
        Calculate ROUGE-N score.

        Returns precision, recall, and F1.
        """
        candidate_tokens = candidate.lower().split()
        reference_tokens = reference.lower().split()

        candidate_ngrams = self._get_ngrams_list(candidate_tokens, n)
        reference_ngrams = self._get_ngrams_list(reference_tokens, n)

        if not reference_ngrams:
            return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0}

        # Count overlaps
        candidate_counter = Counter(candidate_ngrams)
        reference_counter = Counter(reference_ngrams)

        overlap = sum((candidate_counter & reference_counter).values())

        # Calculate metrics
        precision = overlap / len(candidate_ngrams) if candidate_ngrams else 0.0
        recall = overlap / len(reference_ngrams) if reference_ngrams else 0.0

        if precision + recall > 0:
            f1 = 2 * (precision * recall) / (precision + recall)
        else:
            f1 = 0.0

        return {
            'precision': precision,
            'recall': recall,
            'f1': f1
        }

    def calculate_rouge_l(
        self,
        candidate: str,
        reference: str
    ) -> Dict[str, float]:
        """
        Calculate ROUGE-L score (Longest Common Subsequence).

        LCS is order-sensitive but allows gaps.
        """
        candidate_tokens = candidate.lower().split()
        reference_tokens = reference.lower().split()

        lcs_length = self._lcs_length(candidate_tokens, reference_tokens)

        # Calculate metrics
        precision = lcs_length / len(candidate_tokens) if candidate_tokens else 0.0
        recall = lcs_length / len(reference_tokens) if reference_tokens else 0.0

        if precision + recall > 0:
            f1 = 2 * (precision * recall) / (precision + recall)
        else:
            f1 = 0.0

        return {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'lcs_length': lcs_length
        }

    def _get_ngrams_list(self, tokens: List[str], n: int) -> List[Tuple]:
        """Get n-grams as list."""
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngrams.append(tuple(tokens[i:i+n]))
        return ngrams

    def _lcs_length(self, seq1: List[str], seq2: List[str]) -> int:
        """Calculate longest common subsequence length."""
        m, n = len(seq1), len(seq2)

        # DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        return dp[m][n]

# Demo
print("\n📊 Example: ROUGE Scores")

rouge_scorer = ROUGEScore()

candidate = "the cat sat on the mat"
reference = "the cat is sitting on the mat"

rouge1 = rouge_scorer.calculate_rouge_n(candidate, reference, n=1)
rouge2 = rouge_scorer.calculate_rouge_n(candidate, reference, n=2)
rougel = rouge_scorer.calculate_rouge_l(candidate, reference)

print(f"Candidate: '{candidate}'")
print(f"Reference: '{reference}'")

print(f"\nROUGE-1:")
print(f"  Precision: {rouge1['precision']:.4f}")
print(f"  Recall: {rouge1['recall']:.4f}")
print(f"  F1: {rouge1['f1']:.4f}")

print(f"\nROUGE-2:")
print(f"  Precision: {rouge2['precision']:.4f}")
print(f"  Recall: {rouge2['recall']:.4f}")
print(f"  F1: {rouge2['f1']:.4f}")

print(f"\nROUGE-L:")
print(f"  Precision: {rougel['precision']:.4f}")
print(f"  Recall: {rougel['recall']:.4f}")
print(f"  F1: {rougel['f1']:.4f}")
print(f"  LCS Length: {rougel['lcs_length']}")

# ============================================================================
# PART 3: METEOR (MT with Synonyms)
# ============================================================================

print("\n\n" + "="*80)
print("PART 3: METEOR - Metric for Evaluation of Translation with Explicit ORdering")
print("="*80)

print("""
📝 METEOR:

Improvement over BLEU with:
1. Stemming (walk, walked, walking → walk)
2. Synonyms (good, great, excellent)
3. Paraphrases
4. Explicit word ordering

Formula: METEOR = Fmean × (1 - Penalty)
  - Fmean: Harmonic mean of precision and recall
  - Penalty: Based on chunk fragmentation

Better than BLEU for:
✓ Paraphrases
✓ Synonym usage
✓ Correlates better with human judgment

Note: Full implementation requires WordNet for synonyms.
We'll implement a simplified version.
""")

class METEORScore:
    """Simplified METEOR score (without full WordNet integration)."""

    def __init__(self, alpha: float = 0.9, beta: float = 3.0, gamma: float = 0.5):
        """
        Args:
            alpha: Weight for recall vs precision
            beta: Weight for fragmentation penalty
            gamma: Penalty coefficient
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        # Simplified synonym dictionary
        self.synonyms = {
            'good': {'great', 'excellent', 'nice'},
            'great': {'good', 'excellent', 'wonderful'},
            'big': {'large', 'huge', 'enormous'},
            'small': {'tiny', 'little', 'minute'},
            'happy': {'joyful', 'glad', 'pleased'},
            'sad': {'unhappy', 'sorrowful', 'depressed'}
        }

    def calculate(self, candidate: str, reference: str) -> Dict[str, Any]:
        """Calculate METEOR score."""
        candidate_tokens = self._tokenize(candidate)
        reference_tokens = self._tokenize(reference)

        # Find alignments (exact matches and synonyms)
        matches = self._find_matches(candidate_tokens, reference_tokens)

        # Calculate precision and recall
        precision = len(matches) / len(candidate_tokens) if candidate_tokens else 0.0
        recall = len(matches) / len(reference_tokens) if reference_tokens else 0.0

        # F-mean (harmonic mean weighted by alpha)
        if precision + recall > 0:
            fmean = (precision * recall) / (self.alpha * precision + (1 - self.alpha) * recall)
        else:
            fmean = 0.0

        # Fragmentation penalty
        chunks = self._count_chunks(matches)
        penalty = self.gamma * (chunks / len(matches)) ** self.beta if matches else 0.0

        # Final METEOR score
        meteor = fmean * (1 - penalty)

        return {
            'meteor': meteor,
            'precision': precision,
            'recall': recall,
            'fmean': fmean,
            'penalty': penalty,
            'matches': len(matches),
            'chunks': chunks
        }

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize and stem (simplified)."""
        tokens = text.lower().split()
        # Simple stemming: remove common suffixes
        stemmed = []
        for token in tokens:
            if token.endswith('ing'):
                stemmed.append(token[:-3])
            elif token.endswith('ed'):
                stemmed.append(token[:-2])
            elif token.endswith('s') and len(token) > 3:
                stemmed.append(token[:-1])
            else:
                stemmed.append(token)
        return stemmed

    def _find_matches(
        self,
        candidate: List[str],
        reference: List[str]
    ) -> List[Tuple[int, int]]:
        """Find word alignments (exact and synonyms)."""
        matches = []
        used_ref = set()

        # Exact matches first
        for i, c_token in enumerate(candidate):
            for j, r_token in enumerate(reference):
                if j not in used_ref and c_token == r_token:
                    matches.append((i, j))
                    used_ref.add(j)
                    break

        # Synonym matches
        for i, c_token in enumerate(candidate):
            if any(m[0] == i for m in matches):
                continue  # Already matched

            for j, r_token in enumerate(reference):
                if j not in used_ref:
                    if self._are_synonyms(c_token, r_token):
                        matches.append((i, j))
                        used_ref.add(j)
                        break

        return sorted(matches, key=lambda x: x[0])

    def _are_synonyms(self, word1: str, word2: str) -> bool:
        """Check if two words are synonyms (simplified)."""
        if word1 in self.synonyms:
            if word2 in self.synonyms[word1]:
                return True
        if word2 in self.synonyms:
            if word1 in self.synonyms[word2]:
                return True
        return False

    def _count_chunks(self, matches: List[Tuple[int, int]]) -> int:
        """Count number of chunks (contiguous matches)."""
        if not matches:
            return 0

        chunks = 1
        for i in range(1, len(matches)):
            # Check if this match is contiguous with previous
            prev_cand, prev_ref = matches[i-1]
            curr_cand, curr_ref = matches[i]

            if curr_cand != prev_cand + 1 or curr_ref != prev_ref + 1:
                chunks += 1

        return chunks

# Demo
print("\n📊 Example: METEOR Score")

meteor_scorer = METEORScore()

candidate = "the weather is great today"
reference = "the weather is good today"

result = meteor_scorer.calculate(candidate, reference)

print(f"Candidate: '{candidate}'")
print(f"Reference: '{reference}'")
print(f"\nMETEOR Score: {result['meteor']:.4f}")
print(f"Precision: {result['precision']:.4f}")
print(f"Recall: {result['recall']:.4f}")
print(f"F-mean: {result['fmean']:.4f}")
print(f"Penalty: {result['penalty']:.4f}")
print(f"Matches: {result['matches']}")
print(f"Chunks: {result['chunks']}")

# ============================================================================
# PART 4: PERPLEXITY (Language Model Quality)
# ============================================================================

print("\n\n" + "="*80)
print("PART 4: Perplexity - Language Model Evaluation")
print("="*80)

print("""
📝 PERPLEXITY:

Measures how "surprised" a language model is by text.

Formula: PPL = exp(-1/N × Σ log P(wi|context))

Where:
- N: Number of tokens
- P(wi|context): Model's probability for word i

Interpretation:
- Lower = Better (model predicts text well)
- PPL of 10: Model is as confused as choosing from 10 options
- PPL of 100: Very confused

Use Cases:
✓ Language model quality
✓ Model comparison
✓ Domain adaptation validation
✗ Not for generation quality
✗ Doesn't measure factual accuracy

Note: Requires actual LLM to calculate probabilities.
We'll demonstrate with simulated probabilities.
""")

class PerplexityCalculator:
    """Calculate perplexity for text evaluation."""

    def calculate(
        self,
        text: str,
        token_log_probs: List[float]
    ) -> Dict[str, Any]:
        """
        Calculate perplexity from token log probabilities.

        Args:
            text: Input text
            token_log_probs: Log probability for each token
        """
        tokens = text.split()

        if len(tokens) != len(token_log_probs):
            raise ValueError("Number of tokens must match number of log probs")

        if not tokens:
            return {'perplexity': float('inf'), 'avg_log_prob': 0.0}

        # Average log probability
        avg_log_prob = sum(token_log_probs) / len(token_log_probs)

        # Perplexity: exp(-avg_log_prob)
        perplexity = math.exp(-avg_log_prob)

        return {
            'perplexity': perplexity,
            'avg_log_prob': avg_log_prob,
            'num_tokens': len(tokens),
            'min_log_prob': min(token_log_probs),
            'max_log_prob': max(token_log_probs)
        }

    def simulate_probabilities(self, text: str, quality: str = 'high') -> List[float]:
        """
        Simulate token log probabilities for demonstration.

        Args:
            quality: 'high', 'medium', or 'low'
        """
        tokens = text.split()

        if quality == 'high':
            # High quality: confident predictions
            log_probs = [-0.5 + (-0.3 * (i % 3) / 3) for i in range(len(tokens))]
        elif quality == 'medium':
            # Medium quality: moderate confidence
            log_probs = [-1.5 + (-0.5 * (i % 3) / 3) for i in range(len(tokens))]
        else:  # low
            # Low quality: poor predictions
            log_probs = [-3.0 + (-1.0 * (i % 3) / 3) for i in range(len(tokens))]

        return log_probs

# Demo
print("\n📊 Example: Perplexity Calculation")

ppl_calculator = PerplexityCalculator()

text = "the quick brown fox jumps over the lazy dog"

# Simulate different quality scenarios
qualities = ['high', 'medium', 'low']

print(f"Text: '{text}'")
print(f"Tokens: {len(text.split())}\n")

for quality in qualities:
    log_probs = ppl_calculator.simulate_probabilities(text, quality)
    result = ppl_calculator.calculate(text, log_probs)

    print(f"{quality.upper()} Quality Model:")
    print(f"  Perplexity: {result['perplexity']:.2f}")
    print(f"  Avg Log Prob: {result['avg_log_prob']:.4f}")
    print(f"  Interpretation: {'✓ Good' if result['perplexity'] < 10 else '⚠️  Moderate' if result['perplexity'] < 100 else '✗ Poor'}")
    print()

# ============================================================================
# PART 5: COMPARING ALL METRICS
# ============================================================================

print("\n" + "="*80)
print("PART 5: Comprehensive Metric Comparison")
print("="*80)

print("""
Let's compare all metrics on the same examples to understand their differences.
""")

def comprehensive_evaluation(candidate: str, reference: str) -> Dict[str, Any]:
    """Run all metrics on a text pair."""

    # BLEU
    bleu_scorer = BLEUScore()
    bleu_result = bleu_scorer.calculate(candidate, [reference])

    # ROUGE
    rouge_scorer = ROUGEScore()
    rouge1 = rouge_scorer.calculate_rouge_n(candidate, reference, n=1)
    rouge2 = rouge_scorer.calculate_rouge_n(candidate, reference, n=2)
    rougel = rouge_scorer.calculate_rouge_l(candidate, reference)

    # METEOR
    meteor_scorer = METEORScore()
    meteor_result = meteor_scorer.calculate(candidate, reference)

    return {
        'bleu': bleu_result['bleu'],
        'rouge1_f1': rouge1['f1'],
        'rouge2_f1': rouge2['f1'],
        'rougel_f1': rougel['f1'],
        'meteor': meteor_result['meteor']
    }

# Test cases
test_cases = [
    {
        'name': 'Perfect Match',
        'candidate': 'the cat sat on the mat',
        'reference': 'the cat sat on the mat'
    },
    {
        'name': 'Paraphrase (Same Meaning)',
        'candidate': 'the cat was sitting on the mat',
        'reference': 'the cat sat on the mat'
    },
    {
        'name': 'Synonym Usage',
        'candidate': 'the feline sat on the rug',
        'reference': 'the cat sat on the mat'
    },
    {
        'name': 'Partial Match',
        'candidate': 'the cat sat',
        'reference': 'the cat sat on the mat'
    },
    {
        'name': 'Different Content',
        'candidate': 'the dog ran in the park',
        'reference': 'the cat sat on the mat'
    }
]

print("\n📊 Metric Comparison Across Test Cases:\n")
print(f"{'Case':<30} {'BLEU':<8} {'R-1':<8} {'R-2':<8} {'R-L':<8} {'METEOR':<8}")
print("-" * 80)

for test in test_cases:
    results = comprehensive_evaluation(test['candidate'], test['reference'])
    print(f"{test['name']:<30} "
          f"{results['bleu']:<8.3f} "
          f"{results['rouge1_f1']:<8.3f} "
          f"{results['rouge2_f1']:<8.3f} "
          f"{results['rougel_f1']:<8.3f} "
          f"{results['meteor']:<8.3f}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "="*80)
print("KEY TAKEAWAYS")
print("="*80)

print("""
✅ METRIC SELECTION GUIDE:

1. BLEU:
   ✓ Use for: Translation, precise matching
   ✓ Strengths: Standard, easy to understand
   ✗ Weaknesses: Surface-level, no synonyms

2. ROUGE:
   ✓ Use for: Summarization, content coverage
   ✓ Strengths: Recall-focused, multiple variants
   ✗ Weaknesses: Doesn't capture meaning deeply

3. METEOR:
   ✓ Use for: Paraphrases, synonym-aware eval
   ✓ Strengths: Better correlation with humans
   ✗ Weaknesses: More complex, needs resources

4. BERTScore (Not implemented - requires embeddings):
   ✓ Use for: Semantic similarity
   ✓ Strengths: Captures meaning, not just surface
   ✗ Weaknesses: Computationally expensive

5. BLEURT (Not implemented - requires trained model):
   ✓ Use for: High correlation with human judgments
   ✓ Strengths: Learned metric, very accurate
   ✗ Weaknesses: Requires model, complex

6. Perplexity:
   ✓ Use for: Language model evaluation
   ✓ Strengths: Model-intrinsic quality
   ✗ Weaknesses: Not for generation quality

📊 COMPARISON TABLE:

| Metric | Speed | Accuracy | Semantic | Resource Needs |
|--------|-------|----------|----------|----------------|
| BLEU | ⚡⚡⚡ Fast | ⭐⭐ Basic | ❌ Surface | None |
| ROUGE | ⚡⚡⚡ Fast | ⭐⭐ Basic | ❌ Surface | None |
| METEOR | ⚡⚡ Medium | ⭐⭐⭐ Better | ⚠️  Partial | WordNet |
| BERTScore | ⚡ Slow | ⭐⭐⭐⭐ Great | ✅ Yes | BERT model |
| BLEURT | ⚡ Slow | ⭐⭐⭐⭐⭐ Best | ✅ Yes | Trained model |
| Perplexity | ⚡⚡ Medium | ⭐⭐⭐ Good | ⚠️  LM-specific | LM access |

🎯 WHEN TO USE WHAT:

Use Case → Recommended Metrics
- Translation → BLEU, METEOR, BERTScore
- Summarization → ROUGE-1, ROUGE-2, ROUGE-L
- Paraphrasing → METEOR, BERTScore
- Q&A → Exact Match, F1, ROUGE-L
- General Text → BERTScore, BLEURT
- LM Quality → Perplexity
- Research Paper → BLEU + ROUGE + BERTScore (standard combo)

⚠️  IMPORTANT LIMITATIONS:

1. All metrics are PROXIES for quality
2. No single metric captures everything
3. Always use MULTIPLE metrics
4. Correlate with HUMAN evaluation when possible
5. Understand metric BIASES:
   - BLEU favors shorter outputs
   - ROUGE favors longer outputs with keyword overlap
   - All n-gram metrics miss semantic meaning

💡 BEST PRACTICES:

✓ Use metric ensembles (multiple metrics together)
✓ Calibrate on your specific task
✓ Report all metric variants (ROUGE-1, -2, -L)
✓ Include human evaluation for validation
✓ Document which metrics and why
✓ Consider domain-specific metrics

🔬 RESEARCH STANDARD (Papers):

Minimal reporting:
- Translation: BLEU
- Summarization: ROUGE-1, ROUGE-2, ROUGE-L
- General: Add BERTScore or BLEURT

Full evaluation:
- All above + Human evaluation + Task-specific metrics

Next: 16_safety_alignment_evaluation.py - Safety metrics!
""")

print("\n" + "="*80)
print("✨ Lesson 15 Complete!")
print("="*80)
print("\nNext: Run 16_safety_alignment_evaluation.py")
