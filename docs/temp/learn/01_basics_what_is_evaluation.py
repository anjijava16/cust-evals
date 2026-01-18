"""
Lesson 1: What is LLM Evaluation? (The Absolute Basics)

This lesson introduces the fundamental concepts of LLM evaluation.
Perfect for someone who has never evaluated an LLM before.

Learning Objectives:
- Understand why we need to evaluate LLMs
- Learn what makes a "good" response
- See simple evaluation in action
- Understand the evaluation process

No prerequisites needed!
"""

# ============================================================================
# PART 1: WHY DO WE NEED TO EVALUATE LLMs?
# ============================================================================

print("=" * 70)
print("LESSON 1: What is LLM Evaluation?")
print("=" * 70)

print("\n📚 WHY EVALUATE LLMs?\n")
print("""
When you ask an LLM a question, how do you know if the answer is good?

Without evaluation, you:
❌ Don't know if your LLM is improving or getting worse
❌ Can't compare different models or prompts
❌ Can't catch problems before users do
❌ Have no metrics to optimize

With evaluation, you:
✅ Measure quality objectively
✅ Compare different approaches
✅ Catch issues early
✅ Track improvements over time
✅ Build confidence in your system
""")

input("Press Enter to continue...")

# ============================================================================
# PART 2: WHAT MAKES A RESPONSE "GOOD"?
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: What Makes a Response 'Good'?")
print("=" * 70)

print("\nLet's look at a simple question and different answers:\n")

question = "What is the capital of France?"

print(f"Question: {question}\n")

# Different quality answers
answers = {
    "Perfect": "Paris",
    "Good": "The capital of France is Paris.",
    "Okay": "Paris is the capital and largest city of France.",
    "Verbose": "Well, if you're asking about France, the country located in Western Europe, its capital city is Paris, which is also its largest city and has been the capital since...",
    "Wrong": "London",
    "Unhelpful": "I don't know.",
}

print("Let's evaluate different answers:\n")
for quality, answer in answers.items():
    print(f"{quality:12} → {answer}")

print("\n💡 Key Point: 'Good' can mean different things:")
print("  • Correct (factually accurate)")
print("  • Complete (answers the question fully)")
print("  • Concise (not too wordy)")
print("  • Relevant (stays on topic)")
print("  • Helpful (useful to the user)")

input("\nPress Enter to continue...")

# ============================================================================
# PART 3: SIMPLE EVALUATION - YOUR FIRST EVALUATOR
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Your First Evaluation")
print("=" * 70)

print("\nLet's build the simplest possible evaluator!")
print("We'll check if the answer contains the right answer.\n")


def simple_evaluator(answer: str, expected: str) -> dict:
    """
    The simplest evaluator: check if expected answer is in the response.

    Args:
        answer: The LLM's response
        expected: What we expect to find

    Returns:
        Dictionary with evaluation results
    """
    # Convert to lowercase for comparison
    answer_lower = answer.lower()
    expected_lower = expected.lower()

    # Check if expected answer is present
    is_correct = expected_lower in answer_lower

    # Return results
    return {
        "correct": is_correct,
        "score": 1.0 if is_correct else 0.0,
        "explanation": f"Expected '{expected}' {'found' if is_correct else 'not found'} in answer"
    }


# Let's test our evaluator!
print("Testing our evaluator:\n")

test_cases = [
    ("Paris", "Paris"),
    ("The capital is Paris", "Paris"),
    ("London", "Paris"),
    ("I don't know", "Paris"),
]

for answer, expected in test_cases:
    result = simple_evaluator(answer, expected)
    status = "✓ PASS" if result["correct"] else "✗ FAIL"
    print(f"{status} | Answer: '{answer[:30]}...' | Score: {result['score']}")

print("\n💡 Congratulations! You just ran your first evaluation!")

input("\nPress Enter to continue...")

# ============================================================================
# PART 4: THE EVALUATION PROCESS
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: The Evaluation Process")
print("=" * 70)

print("""
Every evaluation follows these steps:

1. PREPARE TEST DATA
   ├─ Questions/inputs
   ├─ Expected outputs (if available)
   └─ Test cases

2. GET MODEL RESPONSES
   └─ Run your LLM on the test data

3. EVALUATE RESPONSES
   ├─ Compare with expected output
   ├─ Check quality metrics
   └─ Calculate scores

4. ANALYZE RESULTS
   ├─ Look at scores
   ├─ Find patterns
   └─ Identify problems

5. IMPROVE & ITERATE
   └─ Use insights to make your system better
""")

# Let's see this in action!
print("\nLet's run through the full process:\n")

# Step 1: Prepare test data
print("Step 1: Prepare Test Data")
test_data = [
    {"question": "What is 2+2?", "expected": "4"},
    {"question": "What is the capital of Spain?", "expected": "Madrid"},
    {"question": "Who wrote Romeo and Juliet?", "expected": "Shakespeare"},
]
print(f"  ✓ Prepared {len(test_data)} test cases\n")

# Step 2: Get model responses (simulated)
print("Step 2: Get Model Responses")
model_responses = [
    "2+2 equals 4",
    "The capital of Spain is Madrid",
    "William Shakespeare wrote Romeo and Juliet"
]
print(f"  ✓ Got {len(model_responses)} responses\n")

# Step 3: Evaluate
print("Step 3: Evaluate Responses")
results = []
for i, (test, response) in enumerate(zip(test_data, model_responses)):
    result = simple_evaluator(response, test["expected"])
    results.append(result)
    status = "✓" if result["correct"] else "✗"
    print(f"  {status} Test {i+1}: {result['explanation']}")

# Step 4: Analyze
print("\nStep 4: Analyze Results")
total_tests = len(results)
passed_tests = sum(1 for r in results if r["correct"])
pass_rate = (passed_tests / total_tests) * 100
average_score = sum(r["score"] for r in results) / total_tests

print(f"  📊 Total Tests: {total_tests}")
print(f"  ✓ Passed: {passed_tests}")
print(f"  ✗ Failed: {total_tests - passed_tests}")
print(f"  📈 Pass Rate: {pass_rate:.1f}%")
print(f"  ⭐ Average Score: {average_score:.2f}")

# Step 5: Improve
print("\nStep 5: Improve & Iterate")
if pass_rate == 100:
    print("  🎉 Perfect! All tests passed!")
elif pass_rate >= 70:
    print("  👍 Good performance, but room for improvement")
else:
    print("  ⚠️  Needs work - focus on failed cases")

input("\nPress Enter to continue...")

# ============================================================================
# PART 5: KEY CONCEPTS SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: Key Concepts Summary")
print("=" * 70)

print("""
🎓 What You Learned:

1. EVALUATION = Measuring how good LLM responses are

2. GOOD RESPONSES are:
   • Correct (factually accurate)
   • Complete (fully answers the question)
   • Relevant (stays on topic)
   • Concise (not too wordy)

3. BASIC EVALUATOR checks:
   • Does the answer contain the expected information?
   • Can be as simple as string matching!

4. EVALUATION PROCESS:
   Prepare → Run → Evaluate → Analyze → Improve

5. METRICS matter:
   • Pass Rate: % of correct answers
   • Score: Numerical quality measure
   • Individual results: Find specific problems

💡 Important Insights:

• Start Simple: Even basic evaluation is valuable
• Be Systematic: Follow a process, don't just eyeball it
• Iterate: Use results to improve your system
• Automate: Manual checking doesn't scale

""")

# ============================================================================
# PRACTICE EXERCISE
# ============================================================================

print("=" * 70)
print("PRACTICE EXERCISE: Try It Yourself!")
print("=" * 70)

print("""
Now it's your turn! Try modifying the code above to:

1. Add your own test cases
2. Try different questions
3. See what happens with wrong answers
4. Experiment with the evaluator logic

Next Lesson Preview:
In Lesson 2, we'll learn about different types of metrics:
- Exact match
- Contains check
- Similarity scoring
- And more!

Ready to continue learning? Run the next lesson!
""")

print("=" * 70)
print("✨ Congratulations! You completed Lesson 1!")
print("=" * 70)
print("\nNext: Run 02_simple_metrics.py to learn about evaluation metrics")
