"""
Lesson 19: Task-Specific & Human-Centered Metrics (Expert)

Complete coverage of task-specific metrics (Exact Match, Pass@K, Execution Accuracy)
and human-centered metrics (Helpfulness, Coherence, Fluency, Relevance).

Prerequisites: Lessons 1-18
Difficulty: ⭐⭐⭐⭐ Expert
Time: 60 minutes
"""

print("="*80)
print("LESSON 19: Task-Specific & Human-Centered Metrics")
print("="*80)

print("""
🎯 TASK-SPECIFIC & HUMAN METRICS

Two categories of specialized metrics:

A. Task-Specific Metrics (Objective):
   - Exact Match (EM)
   - Token-level F1
   - Pass@K (code generation)
   - Execution Accuracy
   - Semantic Accuracy

B. Human-Centered Metrics (Subjective):
   - Helpfulness
   - Correctness/Factual Accuracy
   - Coherence
   - Fluency
   - Relevance
   - Completeness

These metrics are critical for specific use cases!
""")

from typing import List, Dict, Any, Set, Tuple
import re
from collections import Counter

# ============================================================================
# PART 1: EXACT MATCH & TOKEN-LEVEL F1
# ============================================================================

print("\n" + "="*80)
print("PART 1: Exact Match & Token-level F1")
print("="*80)

print("""
📊 EXACT MATCH (EM):

Strictest metric - answer must exactly match reference.

Use Cases:
✓ Question Answering (SQuAD, Natural Questions)
✓ Extractive tasks
✓ Named Entity Recognition
✗ Open-ended generation
✗ Summarization

TOKEN-LEVEL F1:

More flexible - measures token overlap between prediction and reference.

Formula:
- Precision = |common_tokens| / |predicted_tokens|
- Recall = |common_tokens| / |reference_tokens|
- F1 = 2 * (Precision * Recall) / (Precision + Recall)
""")

class ExactMatchF1Evaluator:
    """Evaluate Exact Match and Token-level F1."""

    def exact_match(
        self,
        prediction: str,
        reference: str,
        normalize: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate Exact Match score.

        Args:
            prediction: Model's answer
            reference: Ground truth answer
            normalize: Whether to normalize (lowercase, remove punct)
        """
        if normalize:
            pred_norm = self._normalize_text(prediction)
            ref_norm = self._normalize_text(reference)
        else:
            pred_norm = prediction
            ref_norm = reference

        exact_match = pred_norm == ref_norm

        return {
            'exact_match': 1.0 if exact_match else 0.0,
            'matches': exact_match,
            'prediction': prediction,
            'reference': reference
        }

    def token_level_f1(
        self,
        prediction: str,
        reference: str
    ) -> Dict[str, Any]:
        """
        Calculate token-level F1 score.

        Commonly used in SQuAD and other QA benchmarks.
        """
        pred_tokens = self._tokenize(prediction)
        ref_tokens = self._tokenize(reference)

        # Count common tokens
        common = Counter(pred_tokens) & Counter(ref_tokens)
        num_common = sum(common.values())

        if num_common == 0:
            return {
                'f1': 0.0,
                'precision': 0.0,
                'recall': 0.0
            }

        # Calculate metrics
        precision = num_common / len(pred_tokens) if pred_tokens else 0.0
        recall = num_common / len(ref_tokens) if ref_tokens else 0.0

        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {
            'f1': f1,
            'precision': precision,
            'recall': recall,
            'common_tokens': num_common,
            'pred_tokens': len(pred_tokens),
            'ref_tokens': len(ref_tokens)
        }

    def evaluate_dataset(
        self,
        predictions: List[str],
        references: List[str]
    ) -> Dict[str, Any]:
        """
        Evaluate dataset with both EM and F1.

        Standard for QA benchmarks.
        """
        em_scores = []
        f1_scores = []

        for pred, ref in zip(predictions, references):
            em_result = self.exact_match(pred, ref)
            f1_result = self.token_level_f1(pred, ref)

            em_scores.append(em_result['exact_match'])
            f1_scores.append(f1_result['f1'])

        avg_em = sum(em_scores) / len(em_scores) if em_scores else 0.0
        avg_f1 = sum(f1_scores) / len(f1_scores) if f1_scores else 0.0

        return {
            'exact_match': avg_em,
            'f1': avg_f1,
            'num_examples': len(predictions)
        }

    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        # Lowercase
        text = text.lower()
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text."""
        return self._normalize_text(text).split()

# Demo
print("\n📊 Example: Exact Match & F1")

em_f1_eval = ExactMatchF1Evaluator()

test_cases = [
    ("Paris", "Paris"),  # Perfect match
    ("The capital is Paris", "Paris"),  # Partial match
    ("Paris, France", "Paris"),  # Extra information
    ("London", "Paris")  # Wrong answer
]

print("\nIndividual Examples:")
for i, (pred, ref) in enumerate(test_cases, 1):
    em = em_f1_eval.exact_match(pred, ref)
    f1 = em_f1_eval.token_level_f1(pred, ref)

    print(f"\n{i}. Pred: '{pred}' | Ref: '{ref}'")
    print(f"   EM: {em['exact_match']:.0f} | F1: {f1['f1']:.3f}")

# Dataset evaluation
predictions = ["Paris", "The capital is Paris", "London", "Paris France"]
references = ["Paris", "Paris", "Paris", "Paris"]

dataset_result = em_f1_eval.evaluate_dataset(predictions, references)

print(f"\nDataset Results ({dataset_result['num_examples']} examples):")
print(f"  Average EM: {dataset_result['exact_match']:.1%}")
print(f"  Average F1: {dataset_result['f1']:.1%}")

# ============================================================================
# PART 2: PASS@K FOR CODE GENERATION
# ============================================================================

print("\n\n" + "="*80)
print("PART 2: Pass@K for Code Generation")
print("="*80)

print("""
💻 PASS@K METRIC:

Used for evaluating code generation models.

Definition:
- Generate K code samples for each problem
- Pass@K = % of problems with ≥1 correct solution in K samples

Common values: Pass@1, Pass@10, Pass@100

Example:
- Generate 10 solutions per problem
- If ANY of the 10 solutions passes tests → success
- Pass@10 = (problems with ≥1 passing solution) / (total problems)

Higher K allows model multiple attempts.
""")

class PassAtKEvaluator:
    """Evaluate Pass@K for code generation."""

    def pass_at_k(
        self,
        problems: List[Dict[str, Any]],
        k: int = 1
    ) -> Dict[str, Any]:
        """
        Calculate Pass@K metric.

        Args:
            problems: List of {problem_id, samples: [{code, passed}]}
            k: Number of samples to consider
        """
        total_problems = len(problems)
        solved_problems = 0

        problem_details = []

        for problem in problems:
            samples = problem.get('samples', [])[:k]  # Take first k samples

            # Check if any sample passed
            any_passed = any(sample.get('passed', False) for sample in samples)

            if any_passed:
                solved_problems += 1

            problem_details.append({
                'problem_id': problem.get('problem_id'),
                'solved': any_passed,
                'samples_checked': len(samples),
                'passing_samples': sum(1 for s in samples if s.get('passed', False))
            })

        pass_at_k_score = solved_problems / total_problems if total_problems > 0 else 0.0

        return {
            'pass_at_k': pass_at_k_score,
            'k': k,
            'solved_problems': solved_problems,
            'total_problems': total_problems,
            'problem_details': problem_details
        }

    def compare_pass_at_k(
        self,
        problems: List[Dict[str, Any]],
        k_values: List[int]
    ) -> Dict[str, Any]:
        """
        Compare Pass@K for different K values.

        Shows improvement as K increases.
        """
        results = {}

        for k in k_values:
            result = self.pass_at_k(problems, k)
            results[f'pass@{k}'] = result['pass_at_k']

        return results

# Demo
print("\n💻 Example: Pass@K Evaluation")

pass_k_eval = PassAtKEvaluator()

# Simulated code generation results
problems = [
    {
        'problem_id': 'P1',
        'samples': [
            {'code': 'def add(a,b): return a+b', 'passed': True},
            {'code': 'def add(a,b): return a-b', 'passed': False},
            {'code': 'def add(a,b): return a*b', 'passed': False},
        ]
    },
    {
        'problem_id': 'P2',
        'samples': [
            {'code': 'def mul(a,b): return a+b', 'passed': False},
            {'code': 'def mul(a,b): return a*b', 'passed': True},
            {'code': 'def mul(a,b): return a/b', 'passed': False},
        ]
    },
    {
        'problem_id': 'P3',
        'samples': [
            {'code': 'def sub(a,b): return a+b', 'passed': False},
            {'code': 'def sub(a,b): return a*b', 'passed': False},
            {'code': 'def sub(a,b): return a/b', 'passed': False},
        ]
    }
]

# Calculate Pass@1, Pass@2, Pass@3
for k in [1, 2, 3]:
    result = pass_k_eval.pass_at_k(problems, k)
    print(f"Pass@{k}: {result['pass_at_k']:.1%} ({result['solved_problems']}/{result['total_problems']} problems)")

# ============================================================================
# PART 3: EXECUTION ACCURACY
# ============================================================================

print("\n\n" + "="*80)
print("PART 3: Execution Accuracy for Code")
print("="*80)

print("""
⚙️ EXECUTION ACCURACY:

Don't just check syntax - run the code!

Metrics:
1. Syntax Correctness: Does it parse?
2. Runtime Success: Does it execute without errors?
3. Test Pass Rate: Does it pass test cases?
4. Output Correctness: Is output correct?

Most rigorous: Execute with test cases.
""")

class ExecutionAccuracyEvaluator:
    """Evaluate code execution accuracy."""

    def evaluate_code_execution(
        self,
        code: str,
        test_cases: List[Dict[str, Any]],
        timeout_seconds: float = 5.0
    ) -> Dict[str, Any]:
        """
        Evaluate code by running test cases.

        Args:
            code: Generated code
            test_cases: List of {input, expected_output}
            timeout_seconds: Max execution time
        """
        # Check syntax
        syntax_valid = self._check_syntax(code)

        if not syntax_valid:
            return {
                'execution_accuracy': 0.0,
                'syntax_valid': False,
                'tests_passed': 0,
                'total_tests': len(test_cases),
                'runtime_success': False
            }

        # Run test cases (simplified - in real system, use sandbox)
        passed_tests = 0
        runtime_errors = []

        for i, test in enumerate(test_cases):
            try:
                # In real system: execute in sandbox with timeout
                result = self._execute_code_with_input(code, test['input'])

                if result == test['expected_output']:
                    passed_tests += 1
            except Exception as e:
                runtime_errors.append({
                    'test_case': i,
                    'error': str(e)
                })

        total_tests = len(test_cases)
        test_pass_rate = passed_tests / total_tests if total_tests > 0 else 0.0
        runtime_success = len(runtime_errors) == 0

        return {
            'execution_accuracy': test_pass_rate,
            'syntax_valid': syntax_valid,
            'runtime_success': runtime_success,
            'tests_passed': passed_tests,
            'total_tests': total_tests,
            'test_pass_rate': test_pass_rate,
            'runtime_errors': runtime_errors
        }

    def _check_syntax(self, code: str) -> bool:
        """Check if code has valid syntax (simplified)."""
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False

    def _execute_code_with_input(self, code: str, input_data: Any) -> Any:
        """
        Execute code with input (highly simplified).

        WARNING: In production, NEVER execute untrusted code!
        Use sandboxes (Docker, etc.)
        """
        # This is a simplified example - DO NOT use in production!
        # Real system needs proper sandboxing

        # For demo, just return mock result
        return "mock_output"

# Demo
print("\n⚙️ Example: Execution Accuracy")

exec_eval = ExecutionAccuracyEvaluator()

# Example code
code_samples = [
    {
        'code': 'def add(a, b):\n    return a + b',
        'test_cases': [
            {'input': (2, 3), 'expected_output': 5},
            {'input': (10, 20), 'expected_output': 30}
        ]
    },
    {
        'code': 'def add(a, b\n    return a + b',  # Syntax error
        'test_cases': [
            {'input': (2, 3), 'expected_output': 5}
        ]
    }
]

for i, sample in enumerate(code_samples, 1):
    result = exec_eval.evaluate_code_execution(
        sample['code'],
        sample['test_cases']
    )

    print(f"\nSample {i}:")
    print(f"  Syntax Valid: {'✓' if result['syntax_valid'] else '✗'}")
    print(f"  Execution Accuracy: {result['execution_accuracy']:.1%}")
    if result['syntax_valid']:
        print(f"  Tests Passed: {result['tests_passed']}/{result['total_tests']}")

# ============================================================================
# PART 4: SEMANTIC ACCURACY
# ============================================================================

print("\n\n" + "="*80)
print("PART 4: Semantic Accuracy")
print("="*80)

print("""
🎯 SEMANTIC ACCURACY:

Beyond exact match - does the answer have the correct meaning?

Use Cases:
- Paraphrased answers
- Different phrasings, same meaning
- Semantic equivalence

Methods:
1. Semantic similarity (embeddings)
2. Entailment checking (NLI models)
3. LLM-as-judge
""")

class SemanticAccuracyEvaluator:
    """Evaluate semantic accuracy."""

    def semantic_accuracy_simple(
        self,
        prediction: str,
        reference: str,
        threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Simple semantic accuracy using word overlap.

        For production, use embeddings or NLI models.
        """
        pred_words = set(prediction.lower().split())
        ref_words = set(reference.lower().split())

        if not ref_words:
            return {'semantic_accuracy': 0.0, 'semantically_correct': False}

        # Jaccard similarity
        intersection = len(pred_words & ref_words)
        union = len(pred_words | ref_words)

        similarity = intersection / union if union > 0 else 0.0

        semantically_correct = similarity >= threshold

        return {
            'semantic_accuracy': similarity,
            'semantically_correct': semantically_correct,
            'threshold': threshold,
            'similarity_score': similarity
        }

# Demo
print("\n🎯 Example: Semantic Accuracy")

semantic_eval = SemanticAccuracyEvaluator()

test_pairs = [
    ("The cat sat on the mat", "A cat was sitting on a mat"),
    ("Paris is the capital of France", "France's capital city is Paris"),
    ("2 + 2 = 4", "The sum of two and two equals four"),
    ("The sky is blue", "Grass is green")
]

for pred, ref in test_pairs:
    result = semantic_eval.semantic_accuracy_simple(pred, ref)

    print(f"\nPred: '{pred}'")
    print(f"Ref:  '{ref}'")
    print(f"  Semantic Accuracy: {result['semantic_accuracy']:.2f}")
    print(f"  Semantically Correct: {'✓' if result['semantically_correct'] else '✗'}")

# ============================================================================
# PART 5: HUMAN-CENTERED METRICS
# ============================================================================

print("\n\n" + "="*80)
print("PART 5: Human-Centered Metrics")
print("="*80)

print("""
👤 HUMAN-CENTERED EVALUATION:

Subjective quality metrics that require human judgment:

1. Helpfulness: Is the response useful?
2. Correctness: Is it factually accurate?
3. Coherence: Does it make logical sense?
4. Fluency: Is it well-written?
5. Relevance: Does it address the question?
6. Completeness: Is it comprehensive?

Can be evaluated by:
- Human annotators
- LLM-as-judge (approximation)
- User feedback
""")

class HumanCenteredEvaluator:
    """Evaluate human-centered quality metrics."""

    def helpfulness_score(
        self,
        question: str,
        answer: str,
        context: str = None
    ) -> Dict[str, Any]:
        """
        Evaluate helpfulness (simulated).

        In production: Use human raters or LLM-as-judge.
        """
        # Simplified heuristics
        score = 0.5  # Start neutral

        # Check if answer addresses question
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        overlap = len(question_words & answer_words)

        if overlap >= len(question_words) * 0.3:
            score += 0.2

        # Check answer length (not too short, not too long)
        word_count = len(answer.split())
        if 20 <= word_count <= 200:
            score += 0.2
        elif word_count < 10:
            score -= 0.2

        # Check for actionable information
        actionable_markers = ['how to', 'you can', 'steps', 'first', 'follow']
        if any(marker in answer.lower() for marker in actionable_markers):
            score += 0.1

        score = max(0.0, min(1.0, score))  # Clamp to [0, 1]

        return {
            'helpfulness': score,
            'is_helpful': score >= 0.6,
            'factors': {
                'addresses_question': overlap >= len(question_words) * 0.3,
                'appropriate_length': 20 <= word_count <= 200,
                'actionable': any(marker in answer.lower() for marker in actionable_markers)
            }
        }

    def coherence_score(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Evaluate coherence - logical flow and consistency.
        """
        sentences = self._split_sentences(text)

        if len(sentences) < 2:
            return {'coherence': 1.0, 'is_coherent': True}

        # Check for discourse markers
        discourse_markers = ['however', 'therefore', 'moreover', 'furthermore',
                           'additionally', 'consequently', 'thus', 'hence']

        has_markers = any(marker in text.lower() for marker in discourse_markers)

        # Check for pronouns (indicates continuation)
        pronouns = ['it', 'this', 'that', 'these', 'those', 'they']
        has_pronouns = any(pronoun in text.lower() for pronoun in pronouns)

        # Simple coherence score
        score = 0.5
        if has_markers:
            score += 0.25
        if has_pronouns:
            score += 0.25

        return {
            'coherence': score,
            'is_coherent': score >= 0.6,
            'has_discourse_markers': has_markers,
            'has_referential_pronouns': has_pronouns
        }

    def fluency_score(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Evaluate fluency - grammatical correctness and naturalness.
        """
        # Simplified fluency checks
        score = 1.0

        # Check for repeated words
        words = text.lower().split()
        if len(words) != len(set(words)):
            repeated_ratio = 1 - (len(set(words)) / len(words))
            if repeated_ratio > 0.3:  # More than 30% repetition
                score -= 0.3

        # Check for sentence fragments
        sentences = self._split_sentences(text)
        fragments = sum(1 for s in sentences if len(s.split()) < 3)
        if fragments > len(sentences) * 0.3:
            score -= 0.2

        # Check for basic grammar (simplified)
        has_capitals = any(c.isupper() for c in text)
        has_punctuation = any(p in text for p in '.!?')

        if not (has_capitals and has_punctuation):
            score -= 0.2

        score = max(0.0, min(1.0, score))

        return {
            'fluency': score,
            'is_fluent': score >= 0.7,
            'factors': {
                'minimal_repetition': repeated_ratio < 0.3 if 'repeated_ratio' in locals() else True,
                'complete_sentences': fragments < len(sentences) * 0.3 if sentences else True,
                'proper_formatting': has_capitals and has_punctuation
            }
        }

    def relevance_score(
        self,
        question: str,
        answer: str
    ) -> Dict[str, Any]:
        """
        Evaluate relevance - does answer address the question?
        """
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())

        # Remove stop words
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are', 'was', 'were', 'in', 'to', 'for', 'of', 'with'}
        question_keywords = question_words - stop_words
        answer_keywords = answer_words - stop_words

        if not question_keywords:
            return {'relevance': 0.5, 'is_relevant': True}

        # Calculate keyword coverage
        overlap = len(question_keywords & answer_keywords)
        coverage = overlap / len(question_keywords)

        return {
            'relevance': coverage,
            'is_relevant': coverage >= 0.5,
            'question_keywords_covered': overlap,
            'total_question_keywords': len(question_keywords)
        }

    def completeness_score(
        self,
        question: str,
        answer: str,
        expected_aspects: List[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate completeness - comprehensive coverage?
        """
        if expected_aspects:
            answer_lower = answer.lower()
            covered = [asp for asp in expected_aspects if asp.lower() in answer_lower]
            score = len(covered) / len(expected_aspects)

            return {
                'completeness': score,
                'is_complete': score >= 0.8,
                'covered_aspects': covered,
                'missing_aspects': [asp for asp in expected_aspects if asp not in covered]
            }
        else:
            # Use length as proxy for completeness
            word_count = len(answer.split())

            if word_count < 20:
                score = 0.3
            elif word_count < 50:
                score = 0.6
            elif word_count < 100:
                score = 0.8
            else:
                score = 1.0

            return {
                'completeness': score,
                'is_complete': score >= 0.7,
                'word_count': word_count
            }

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

# Demo
print("\n👤 Example: Human-Centered Metrics")

human_eval = HumanCenteredEvaluator()

question = "How do I train a machine learning model?"
answer = """To train a machine learning model, follow these steps:
First, prepare your data by cleaning and splitting it.
Then, choose an appropriate algorithm. Finally, train the model
and evaluate its performance."""

print(f"Question: {question}")
print(f"Answer: {answer}\n")

helpfulness = human_eval.helpfulness_score(question, answer)
coherence = human_eval.coherence_score(answer)
fluency = human_eval.fluency_score(answer)
relevance = human_eval.relevance_score(question, answer)
completeness = human_eval.completeness_score(question, answer,
    expected_aspects=['data', 'algorithm', 'training', 'evaluation'])

print(f"Helpfulness: {helpfulness['helpfulness']:.2f} ({'✓' if helpfulness['is_helpful'] else '✗'})")
print(f"Coherence: {coherence['coherence']:.2f} ({'✓' if coherence['is_coherent'] else '✗'})")
print(f"Fluency: {fluency['fluency']:.2f} ({'✓' if fluency['is_fluent'] else '✗'})")
print(f"Relevance: {relevance['relevance']:.2f} ({'✓' if relevance['is_relevant'] else '✗'})")
print(f"Completeness: {completeness['completeness']:.2f} ({'✓' if completeness['is_complete'] else '✗'})")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "="*80)
print("KEY TAKEAWAYS")
print("="*80)

print("""
✅ TASK-SPECIFIC METRICS:

1. EXACT MATCH (EM)
   ✓ Use for: QA, extraction tasks
   ✓ Strict but clear
   ✓ Target: > 80% for extractive QA

2. TOKEN-LEVEL F1
   ✓ More flexible than EM
   ✓ Standard for SQuAD
   ✓ Target: > 85% for good models

3. PASS@K (Code)
   ✓ Multiple attempts allowed
   ✓ Pass@1 < Pass@10 < Pass@100
   ✓ Target: Pass@1 > 40% (difficult tasks)

4. EXECUTION ACCURACY
   ✓ Run the code!
   ✓ Most rigorous for code generation
   ✓ Target: > 70% test pass rate

5. SEMANTIC ACCURACY
   ✓ Meaning over exact match
   ✓ Use embeddings/NLI
   ✓ Target: > 0.8 similarity

👤 HUMAN-CENTERED METRICS:

1. HELPFULNESS
   - Is it useful to the user?
   - Addresses question + actionable
   - Target: > 0.7/1.0

2. CORRECTNESS/FACTUAL ACCURACY
   - Factually accurate information
   - No hallucinations
   - Target: > 0.9/1.0

3. COHERENCE
   - Logical flow
   - Consistent throughout
   - Target: > 0.8/1.0

4. FLUENCY
   - Natural language
   - Grammatically correct
   - Target: > 0.8/1.0

5. RELEVANCE
   - Addresses the question
   - On-topic
   - Target: > 0.8/1.0

6. COMPLETENESS
   - Comprehensive answer
   - Covers all aspects
   - Target: > 0.8/1.0

📊 METRIC SELECTION GUIDE:

| Task Type | Recommended Metrics |
|-----------|-------------------|
| **Extractive QA** | EM, Token F1 |
| **Code Generation** | Pass@K, Execution Accuracy |
| **Open-ended QA** | Semantic Accuracy, Helpfulness |
| **Summarization** | ROUGE, Coherence, Completeness |
| **Translation** | BLEU, Fluency |
| **Dialogue** | Coherence, Helpfulness, Relevance |

💡 BEST PRACTICES:

1. Combine Objective & Subjective:
   - Use EM/F1 for factual parts
   - Use human metrics for quality

2. Task-Appropriate Metrics:
   - Don't use EM for creative writing
   - Don't use fluency alone for QA

3. Human Evaluation:
   - Gold standard for human metrics
   - Sample regularly
   - Use LLM-as-judge for scale

4. Multiple Annotators:
   - Inter-annotator agreement
   - Resolve disagreements
   - Clear guidelines

⚠️  LIMITATIONS:

1. Exact Match: Too strict
2. Token F1: Ignores meaning
3. Pass@K: Doesn't check code quality
4. Human metrics: Subjective, expensive

Next: 20_efficiency_performance.py - Efficiency metrics!
""")

print("\n" + "="*80)
print("✨ Lesson 19 Complete!")
print("="*80)
print("\nNext: Run 20_efficiency_performance.py")
