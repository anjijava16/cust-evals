"""
Lesson 14: Prompt Optimization via Evaluation (Advanced)

Learn to systematically improve prompts using evaluation-driven optimization.
Use data and metrics to refine prompts instead of guessing.

Prerequisites: Lessons 1-13
Difficulty: ⭐⭐⭐ Advanced
Time: 50 minutes
"""

print("="*80)
print("LESSON 14: Prompt Optimization via Evaluation")
print("="*80)

print("""
🎯 EVALUATION-DRIVEN PROMPT ENGINEERING

Traditional approach: ❌
- Write prompt
- Test manually
- Guess what's wrong
- Try random changes
- Hope it works

Evaluation-driven approach: ✅
- Define metrics
- Test systematically
- Measure improvements
- Iterate with data
- Optimize confidently

This lesson shows how to use evaluation to optimize prompts scientifically.
""")

from typing import List, Dict, Any, Tuple, Optional, Callable
from collections import defaultdict
import random

# ============================================================================
# PART 1: PROMPT TESTING FRAMEWORK
# ============================================================================

print("\n" + "="*80)
print("PART 1: Systematic Prompt Testing")
print("="*80)

print("""
🧪 PROMPT TESTING FRAMEWORK:

1. Define test cases
2. Run prompt variations
3. Collect metrics
4. Compare results
5. Select winner
6. Iterate

Key principle: Change one thing at a time to isolate effects.
""")

class PromptTester:
    """Framework for systematic prompt testing."""

    def __init__(self, test_cases: List[Dict]):
        self.test_cases = test_cases
        self.results = {}

    def test_prompt(
        self,
        prompt_template: str,
        prompt_name: str,
        model_fn: Callable,
        evaluator_fn: Callable
    ) -> Dict[str, Any]:
        """Test a prompt on all test cases."""

        test_results = []
        scores = []

        for i, test_case in enumerate(self.test_cases):
            # Format prompt with test case input
            prompt = prompt_template.format(**test_case)

            # Get model response (simulated here)
            response = model_fn(prompt, test_case)

            # Evaluate response
            eval_result = evaluator_fn(response, test_case.get('expected', ''))
            scores.append(eval_result['score'])

            test_results.append({
                'test_case_id': i,
                'input': test_case.get('input', ''),
                'response': response,
                'score': eval_result['score'],
                'passed': eval_result.get('passed', eval_result['score'] >= 0.7)
            })

        # Aggregate metrics
        avg_score = sum(scores) / len(scores) if scores else 0
        pass_rate = sum(1 for r in test_results if r['passed']) / len(test_results) if test_results else 0

        result = {
            'prompt_name': prompt_name,
            'prompt_template': prompt_template,
            'num_tests': len(test_results),
            'avg_score': avg_score,
            'pass_rate': pass_rate,
            'test_results': test_results
        }

        self.results[prompt_name] = result
        return result

    def compare_prompts(self, prompt_names: List[str]) -> Dict[str, Any]:
        """Compare multiple tested prompts."""

        comparisons = []

        for name in prompt_names:
            if name in self.results:
                result = self.results[name]
                comparisons.append({
                    'name': name,
                    'avg_score': result['avg_score'],
                    'pass_rate': result['pass_rate']
                })

        # Find best
        best = max(comparisons, key=lambda x: x['avg_score']) if comparisons else None

        return {
            'comparisons': comparisons,
            'best_prompt': best['name'] if best else None,
            'best_score': best['avg_score'] if best else 0
        }

# Demo
print("\n🧪 Example: Testing prompt variations")

# Test cases
test_cases = [
    {'input': 'What is 2+2?', 'expected': '4'},
    {'input': 'What is 5*3?', 'expected': '15'},
    {'input': 'What is 10-7?', 'expected': '3'}
]

# Simulated model function
def simple_model(prompt: str, test_case: Dict) -> str:
    """Simulate LLM response."""
    input_text = test_case['input']

    if 'step by step' in prompt.lower():
        # Better performance with step-by-step
        if '+' in input_text:
            return "Step 1: Identify operation (addition). Step 2: 2+2=4. Answer: 4"
        elif '*' in input_text:
            return "Step 1: Identify operation (multiplication). Step 2: 5*3=15. Answer: 15"
        elif '-' in input_text:
            return "Step 1: Identify operation (subtraction). Step 2: 10-7=3. Answer: 3"

    # Basic response
    if '+' in input_text:
        return "4"
    elif '*' in input_text:
        return "15"
    elif '-' in input_text:
        return "3"

    return "I don't know"

# Evaluator function
def math_evaluator(response: str, expected: str) -> Dict:
    """Evaluate math response."""
    # Extract number from response
    import re
    numbers = re.findall(r'\d+', response)

    if numbers and numbers[-1] == expected:
        return {'score': 1.0, 'passed': True}
    return {'score': 0.0, 'passed': False}

# Test different prompts
tester = PromptTester(test_cases)

# Prompt 1: Basic
prompt1 = "Solve: {input}"
result1 = tester.test_prompt(
    prompt_template=prompt1,
    prompt_name="basic",
    model_fn=simple_model,
    evaluator_fn=math_evaluator
)

# Prompt 2: With instruction
prompt2 = "Solve this math problem step by step: {input}"
result2 = tester.test_prompt(
    prompt_template=prompt2,
    prompt_name="step_by_step",
    model_fn=simple_model,
    evaluator_fn=math_evaluator
)

# Prompt 3: With format instruction
prompt3 = "Solve: {input}\nProvide only the numeric answer."
result3 = tester.test_prompt(
    prompt_template=prompt3,
    prompt_name="format_specified",
    model_fn=simple_model,
    evaluator_fn=math_evaluator
)

# Compare
comparison = tester.compare_prompts(['basic', 'step_by_step', 'format_specified'])

print("\n📊 Prompt comparison:")
for comp in comparison['comparisons']:
    print(f"  {comp['name']:20} → Score: {comp['avg_score']:.2f}, Pass rate: {comp['pass_rate']:.1%}")

print(f"\n🏆 Best prompt: {comparison['best_prompt']} (score: {comparison['best_score']:.2f})")

# ============================================================================
# PART 2: A/B TESTING FOR PROMPTS
# ============================================================================

print("\n\n" + "="*80)
print("PART 2: A/B Testing for Prompts")
print("="*80)

print("""
🔬 A/B TESTING METHODOLOGY:

Compare two prompt variants on same test set:
- Prompt A (baseline)
- Prompt B (variation)

Statistical comparison:
1. Run both on identical test set
2. Measure performance metrics
3. Calculate significance
4. Choose winner

Critical: Use statistical tests to ensure difference is real.
""")

class PromptABTester:
    """A/B testing for prompt optimization."""

    def ab_test(
        self,
        prompt_a: str,
        prompt_b: str,
        test_cases: List[Dict],
        model_fn: Callable,
        evaluator_fn: Callable
    ) -> Dict[str, Any]:
        """Run A/B test between two prompts."""

        scores_a = []
        scores_b = []

        for test_case in test_cases:
            # Test prompt A
            prompt_a_formatted = prompt_a.format(**test_case)
            response_a = model_fn(prompt_a_formatted, test_case)
            eval_a = evaluator_fn(response_a, test_case.get('expected', ''))
            scores_a.append(eval_a['score'])

            # Test prompt B
            prompt_b_formatted = prompt_b.format(**test_case)
            response_b = model_fn(prompt_b_formatted, test_case)
            eval_b = evaluator_fn(response_b, test_case.get('expected', ''))
            scores_b.append(eval_b['score'])

        # Calculate metrics
        avg_a = sum(scores_a) / len(scores_a) if scores_a else 0
        avg_b = sum(scores_b) / len(scores_b) if scores_b else 0

        improvement = ((avg_b - avg_a) / avg_a * 100) if avg_a > 0 else 0

        # Simple statistical test (t-test approximation)
        is_significant = abs(avg_b - avg_a) > 0.1  # Simplified

        return {
            'prompt_a_score': avg_a,
            'prompt_b_score': avg_b,
            'improvement_percent': improvement,
            'significant': is_significant,
            'winner': 'B' if avg_b > avg_a and is_significant else 'A' if avg_a > avg_b and is_significant else 'Tie',
            'recommendation': 'Use prompt B' if avg_b > avg_a and is_significant else 'Keep prompt A'
        }

# Demo
print("\n🔬 Example: A/B testing prompts")

ab_tester = PromptABTester()

prompt_a = "Answer this question: {input}"
prompt_b = "Answer this question accurately and concisely: {input}"

result = ab_tester.ab_test(
    prompt_a=prompt_a,
    prompt_b=prompt_b,
    test_cases=test_cases,
    model_fn=simple_model,
    evaluator_fn=math_evaluator
)

print(f"Prompt A score: {result['prompt_a_score']:.2f}")
print(f"Prompt B score: {result['prompt_b_score']:.2f}")
print(f"Improvement: {result['improvement_percent']:+.1f}%")
print(f"Significant: {'✓ Yes' if result['significant'] else '✗ No'}")
print(f"Winner: {result['winner']}")
print(f"Recommendation: {result['recommendation']}")

# ============================================================================
# PART 3: ITERATIVE REFINEMENT
# ============================================================================

print("\n\n" + "="*80)
print("PART 3: Iterative Prompt Refinement")
print("="*80)

print("""
🔄 ITERATIVE OPTIMIZATION:

Start with baseline → Test → Analyze → Refine → Repeat

Refinement strategies:
1. Add specificity
2. Include examples
3. Clarify format
4. Add constraints
5. Simplify language
6. Add structure

Track improvements across iterations.
""")

class PromptOptimizer:
    """Iteratively optimize prompts using evaluation feedback."""

    def __init__(self, test_cases: List[Dict], evaluator_fn: Callable):
        self.test_cases = test_cases
        self.evaluator_fn = evaluator_fn
        self.history = []

    def optimize_iteratively(
        self,
        initial_prompt: str,
        model_fn: Callable,
        refinements: List[Dict],
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """Iteratively refine prompt."""

        current_prompt = initial_prompt
        best_score = 0

        for iteration in range(max_iterations):
            # Test current prompt
            scores = []
            for test_case in self.test_cases:
                prompt = current_prompt.format(**test_case)
                response = model_fn(prompt, test_case)
                eval_result = self.evaluator_fn(response, test_case.get('expected', ''))
                scores.append(eval_result['score'])

            avg_score = sum(scores) / len(scores) if scores else 0

            # Record iteration
            self.history.append({
                'iteration': iteration + 1,
                'prompt': current_prompt,
                'score': avg_score
            })

            # Check if improved
            if avg_score > best_score:
                best_score = avg_score
                best_prompt = current_prompt

            # Apply next refinement if available
            if iteration < len(refinements):
                refinement = refinements[iteration]
                current_prompt = refinement.get('prompt', current_prompt)

        return {
            'iterations': len(self.history),
            'history': self.history,
            'best_score': best_score,
            'best_prompt': best_prompt,
            'improvement': best_score - self.history[0]['score'] if self.history else 0
        }

# Demo
print("\n🔄 Example: Iterative refinement")

optimizer = PromptOptimizer(test_cases, math_evaluator)

refinements = [
    {'prompt': "Solve: {input}"},
    {'prompt': "Solve this math problem: {input}"},
    {'prompt': "Solve this math problem carefully: {input}\nShow your work."},
    {'prompt': "Solve this math problem step by step: {input}\nProvide the final answer clearly."}
]

result = optimizer.optimize_iteratively(
    initial_prompt=refinements[0]['prompt'],
    model_fn=simple_model,
    refinements=refinements,
    max_iterations=len(refinements)
)

print(f"Optimization process:")
for entry in result['history']:
    print(f"  Iteration {entry['iteration']}: Score {entry['score']:.2f}")

print(f"\nBest score: {result['best_score']:.2f}")
print(f"Total improvement: {result['improvement']:+.2f}")

# ============================================================================
# PART 4: FEW-SHOT EXAMPLE OPTIMIZATION
# ============================================================================

print("\n\n" + "="*80)
print("PART 4: Few-Shot Example Selection")
print("="*80)

print("""
💡 OPTIMIZING FEW-SHOT EXAMPLES:

Few-shot prompting: Include examples in prompt

Questions:
- How many examples?
- Which examples?
- What order?

Use evaluation to find optimal few-shot configuration.
""")

class FewShotOptimizer:
    """Optimize few-shot example selection."""

    def evaluate_few_shot_config(
        self,
        base_prompt: str,
        examples: List[Dict],
        num_examples: int,
        test_cases: List[Dict],
        model_fn: Callable,
        evaluator_fn: Callable
    ) -> Dict[str, Any]:
        """Evaluate a few-shot configuration."""

        # Select examples
        selected_examples = examples[:num_examples]

        # Build few-shot prompt
        few_shot_text = "\n".join([
            f"Q: {ex['input']}\nA: {ex['output']}"
            for ex in selected_examples
        ])

        scores = []
        for test_case in test_cases:
            # Format prompt with examples
            prompt = f"{few_shot_text}\n\nQ: {test_case['input']}\nA:"

            response = model_fn(prompt, test_case)
            eval_result = evaluator_fn(response, test_case.get('expected', ''))
            scores.append(eval_result['score'])

        avg_score = sum(scores) / len(scores) if scores else 0

        return {
            'num_examples': num_examples,
            'score': avg_score,
            'examples_used': selected_examples
        }

    def find_optimal_num_examples(
        self,
        base_prompt: str,
        available_examples: List[Dict],
        test_cases: List[Dict],
        model_fn: Callable,
        evaluator_fn: Callable,
        max_examples: int = 5
    ) -> Dict[str, Any]:
        """Find optimal number of few-shot examples."""

        results = []

        for n in range(1, min(max_examples + 1, len(available_examples) + 1)):
            result = self.evaluate_few_shot_config(
                base_prompt=base_prompt,
                examples=available_examples,
                num_examples=n,
                test_cases=test_cases,
                model_fn=model_fn,
                evaluator_fn=evaluator_fn
            )
            results.append(result)

        # Find best
        best = max(results, key=lambda x: x['score'])

        return {
            'results': results,
            'optimal_num_examples': best['num_examples'],
            'best_score': best['score']
        }

# Demo
print("\n💡 Example: Few-shot optimization")

few_shot_optimizer = FewShotOptimizer()

available_examples = [
    {'input': '2+2', 'output': '4'},
    {'input': '5*3', 'output': '15'},
    {'input': '10-7', 'output': '3'},
    {'input': '12/4', 'output': '3'}
]

result = few_shot_optimizer.find_optimal_num_examples(
    base_prompt="",
    available_examples=available_examples,
    test_cases=test_cases,
    model_fn=simple_model,
    evaluator_fn=math_evaluator,
    max_examples=3
)

print("Few-shot example optimization:")
for r in result['results']:
    print(f"  {r['num_examples']} examples → Score: {r['score']:.2f}")

print(f"\n🏆 Optimal: {result['optimal_num_examples']} examples (score: {result['best_score']:.2f})")

# ============================================================================
# PART 5: PROMPT VERSION MANAGEMENT
# ============================================================================

print("\n\n" + "="*80)
print("PART 5: Prompt Version Management")
print("="*80)

print("""
📝 VERSIONING PROMPTS:

Like code, prompts need version control:
- Track changes
- Compare versions
- Rollback if needed
- Document why changes were made

Best practices:
1. Semantic versioning (1.0.0)
2. Changelog
3. Performance metrics per version
4. A/B test before promoting
""")

class PromptVersionManager:
    """Manage prompt versions with metrics."""

    def __init__(self):
        self.versions = {}
        self.current_version = None

    def register_version(
        self,
        version_id: str,
        prompt: str,
        performance_metrics: Dict[str, float],
        notes: str = ""
    ):
        """Register a new prompt version."""
        self.versions[version_id] = {
            'prompt': prompt,
            'metrics': performance_metrics,
            'notes': notes,
            'timestamp': '2026-01-18'
        }
        print(f"✓ Registered version {version_id}")

    def compare_versions(self, v1: str, v2: str) -> Dict:
        """Compare two versions."""
        if v1 not in self.versions or v2 not in self.versions:
            return {'error': 'Version not found'}

        metrics_v1 = self.versions[v1]['metrics']
        metrics_v2 = self.versions[v2]['metrics']

        improvements = {}
        for metric in metrics_v1:
            if metric in metrics_v2:
                change = metrics_v2[metric] - metrics_v1[metric]
                improvements[metric] = {
                    'v1': metrics_v1[metric],
                    'v2': metrics_v2[metric],
                    'change': change,
                    'improved': change > 0
                }

        return {
            'version_1': v1,
            'version_2': v2,
            'improvements': improvements
        }

    def get_best_version(self, metric: str = 'avg_score') -> Optional[str]:
        """Get best version by metric."""
        if not self.versions:
            return None

        best_version = max(
            self.versions.items(),
            key=lambda x: x[1]['metrics'].get(metric, 0)
        )

        return best_version[0]

# Demo
print("\n📝 Example: Prompt version management")

version_manager = PromptVersionManager()

# Register versions
version_manager.register_version(
    version_id="1.0.0",
    prompt="Solve: {input}",
    performance_metrics={'avg_score': 0.67, 'pass_rate': 0.67},
    notes="Initial version"
)

version_manager.register_version(
    version_id="1.1.0",
    prompt="Solve this math problem: {input}",
    performance_metrics={'avg_score': 0.75, 'pass_rate': 0.75},
    notes="Added context 'math problem'"
)

version_manager.register_version(
    version_id="2.0.0",
    prompt="Solve this math problem step by step: {input}",
    performance_metrics={'avg_score': 1.0, 'pass_rate': 1.0},
    notes="Added step-by-step instruction"
)

# Compare versions
comparison = version_manager.compare_versions("1.0.0", "2.0.0")
print(f"\nComparing {comparison['version_1']} vs {comparison['version_2']}:")
for metric, data in comparison['improvements'].items():
    print(f"  {metric}: {data['v1']:.2f} → {data['v2']:.2f} ({data['change']:+.2f}) {'✓' if data['improved'] else '✗'}")

# Get best version
best = version_manager.get_best_version('avg_score')
print(f"\n🏆 Best version: {best} (avg_score: {version_manager.versions[best]['metrics']['avg_score']:.2f})")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "="*80)
print("KEY TAKEAWAYS")
print("="*80)

print("""
✅ PROMPT OPTIMIZATION PRINCIPLES:

1. MEASURE FIRST
   - Define metrics before optimizing
   - Establish baseline
   - Track all changes

2. TEST SYSTEMATICALLY
   - Use consistent test set
   - Change one variable at a time
   - Run statistical comparisons

3. ITERATE WITH DATA
   - Let metrics guide refinements
   - Don't guess, measure
   - Track improvement trajectory

4. VERSION EVERYTHING
   - Keep history of changes
   - Document rationale
   - Enable rollbacks

5. A/B TEST BEFORE DEPLOYING
   - Validate improvements
   - Check statistical significance
   - Consider all metrics

🎯 OPTIMIZATION WORKFLOW:

1. Define success metrics
2. Create test set
3. Establish baseline
4. Generate variations
5. Test systematically
6. Measure improvements
7. Select winner
8. Version and deploy
9. Monitor in production
10. Iterate continuously

⚠️  COMMON MISTAKES:

✗ Optimizing without metrics
✗ Testing on single example
✗ Ignoring statistical significance
✗ Over-fitting to test set
✗ Not versioning prompts
✗ Deploying without A/B test
✗ Optimizing for wrong metric

💡 REMEMBER:

"Prompt engineering is an empirical science. Use data and evaluation
 to guide optimization, not intuition alone."

🔧 OPTIMIZATION TECHNIQUES:

1. Specificity: Add clear instructions
2. Examples: Include few-shot examples
3. Structure: Format output clearly
4. Constraints: Add guardrails
5. Context: Provide background
6. Chain-of-thought: Request reasoning
7. Simplification: Remove unnecessary parts

📊 METRICS TO TRACK:

- Accuracy/correctness
- Response quality
- Format compliance
- Latency
- Token usage
- User satisfaction
- Edge case handling

🎓 CONGRATULATIONS!

You've completed all 14 advanced lessons! You now have:
✓ Statistical evaluation skills
✓ Adversarial testing knowledge
✓ Bias detection capabilities
✓ Benchmark creation expertise
✓ Advanced RAG evaluation
✓ Multi-agent evaluation skills
✓ Prompt optimization mastery

You're now an LLM evaluation expert! 🎉
""")

print("\n" + "="*80)
print("✨ Lesson 14 Complete - Advanced Track Finished!")
print("="*80)
print("\nReview ADVANCED_TOPICS.md for synthesis and next steps!")
