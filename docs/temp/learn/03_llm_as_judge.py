"""
Lesson 3: LLM-as-Judge - Using LLMs to Evaluate LLMs

Learn how to use powerful LLMs to evaluate other LLM outputs.
This is one of the most powerful evaluation techniques!

Learning Objectives:
- Understand LLM-as-judge concept
- Write effective evaluation prompts
- Implement basic LLM judges
- Handle edge cases

Prerequisites: Lessons 1-2
"""

# Simulated LLM judge (in practice, use OpenAI, Anthropic, etc.)
def call_judge_llm(prompt: str) -> str:
    """
    Simulates calling an LLM judge.
    In production, replace with actual API calls.
    """
    # This is a simulation - in real code, call OpenAI/Anthropic/etc
    # For demo purposes, we'll return simulated judgments
    
    if "evaluate quality" in prompt.lower():
        return "Score: 8/10\nReasoning: The response is accurate and clear but could be more concise."
    elif "check accuracy" in prompt.lower():
        return "Score: 10/10\nReasoning: The information is factually correct."
    else:
        return "Score: 7/10\nReasoning: Adequate response."


# ============================================================================
# PATTERN 1: BASIC QUALITY JUDGMENT
# ============================================================================

def llm_judge_quality(question: str, response: str) -> dict:
    """
    Use LLM to judge overall response quality.
    """
    
    prompt = f"""
    Evaluate the following Q&A pair on a scale of 1-10.
    
    Question: {question}
    Response: {response}
    
    Evaluate the quality considering:
    - Accuracy: Is it factually correct?
    - Completeness: Does it fully answer the question?
    - Clarity: Is it easy to understand?
    
    Provide your evaluation in this format:
    Score: X/10
    Reasoning: <your explanation>
    """
    
    judgment = call_judge_llm(prompt)
    
    # Parse score (simplified)
    score_line = [line for line in judgment.split('\n') if 'Score:' in line][0]
    score = int(score_line.split('/')[0].split(':')[1].strip())
    
    return {
        "score": score / 10,  # Normalize to 0-1
        "raw_judgment": judgment,
        "passed": score >= 7
    }


# ============================================================================
# PATTERN 2: SPECIFIC CRITERIA EVALUATION
# ============================================================================

def llm_judge_criteria(response: str, criteria: str) -> dict:
    """
    Judge response against specific criteria.
    """
    
    prompt = f"""
    Evaluate this response for: {criteria}
    
    Response: {response}
    
    Rate from 1-10 and explain your reasoning.
    
    Format:
    Score: X/10
    Reasoning: <explanation>
    """
    
    judgment = call_judge_llm(prompt)
    
    return {
        "criteria": criteria,
        "judgment": judgment,
        "metric": "llm_judge"
    }


# ============================================================================
# PATTERN 3: COMPARATIVE JUDGMENT
# ============================================================================

def llm_judge_compare(question: str, response_a: str, response_b: str) -> dict:
    """
    Have LLM compare two responses and pick the better one.
    """
    
    prompt = f"""
    Compare these two responses to the question and determine which is better.
    
    Question: {question}
    
    Response A: {response_a}
    Response B: {response_b}
    
    Which response is better and why?
    
    Format:
    Better Response: [A or B]
    Reasoning: <detailed explanation>
    """
    
    # Simulated judgment
    judgment = "Better Response: B\nReasoning: Response B is more detailed and comprehensive."
    
    winner = 'B' if 'B' in judgment.split('\n')[0] else 'A'
    
    return {
        "winner": winner,
        "judgment": judgment,
        "preference": winner
    }


# ============================================================================
# PATTERN 4: HALLUCINATION DETECTION
# ============================================================================

def llm_judge_hallucination(response: str, context: str) -> dict:
    """
    Check if response contains information not in context (hallucination).
    """
    
    prompt = f"""
    Check if the response contains any information NOT supported by the context.
    
    Context: {context}
    Response: {response}
    
    Identify any hallucinated claims (information not in context).
    
    Format:
    Hallucinated: [Yes/No]
    Claims: <list any unsupported claims>
    """
    
    # Simulated
    judgment = "Hallucinated: No\nClaims: All information is supported by context."
    
    has_hallucination = 'Yes' in judgment.split('\n')[0]
    
    return {
        "has_hallucination": has_hallucination,
        "judgment": judgment,
        "passed": not has_hallucination
    }


# ============================================================================
# DEMONSTRATION
# ============================================================================

print("=" * 70)
print("LESSON 3: LLM-as-Judge Evaluation")
print("=" * 70)

print("\n📚 What is LLM-as-Judge?\n")
print("""
LLM-as-Judge uses a powerful LLM (like GPT-4 or Claude) to evaluate
other LLM outputs. Why?

✅ Understands nuance (paraphrasing, tone, style)
✅ Can evaluate complex criteria (helpfulness, politeness)
✅ Flexible - works for any task
✅ Mimics human judgment

⚠️  But be aware:
- Costs money (API calls)
- Can be biased
- Need good prompts
- Not deterministic
""")

# Example 1: Quality Judgment
print("\n" + "=" * 70)
print("EXAMPLE 1: Quality Judgment")
print("=" * 70)

question = "Explain photosynthesis"
response = "Photosynthesis is how plants make food using sunlight, water, and CO2."

result = llm_judge_quality(question, response)
print(f"\nQuestion: {question}")
print(f"Response: {response}")
print(f"\nLLM Judge Result:")
print(f"  Score: {result['score']:.2f}")
print(f"  Status: {'✓ PASS' if result['passed'] else '✗ FAIL'}")
print(f"  Judgment:\n{result['raw_judgment']}")

# Example 2: Specific Criteria
print("\n" + "=" * 70)
print("EXAMPLE 2: Specific Criteria Evaluation")
print("=" * 70)

response = "Hey! Quantum physics is super complex but basically particles can be in multiple states at once!"

criteria_tests = [
    "professional tone",
    "technical accuracy",
    "clarity for beginners"
]

print(f"\nResponse: {response}\n")
print("Evaluating against different criteria:")

for criteria in criteria_tests:
    result = llm_judge_criteria(response, criteria)
    print(f"\n  Criteria: {criteria}")
    print(f"  {result['judgment']}")

# Example 3: Comparative Judgment
print("\n" + "=" * 70)
print("EXAMPLE 3: Comparing Two Responses")
print("=" * 70)

question = "What is recursion?"
response_a = "Recursion is when a function calls itself."
response_b = "Recursion is a programming technique where a function calls itself to solve a problem by breaking it into smaller instances."

result = llm_judge_compare(question, response_a, response_b)
print(f"\nQuestion: {question}")
print(f"Response A: {response_a}")
print(f"Response B: {response_b}")
print(f"\nLLM Judge says: Response {result['winner']} is better")
print(f"Reasoning:\n{result['judgment']}")

# ============================================================================
# BEST PRACTICES
# ============================================================================

print("\n\n" + "=" * 70)
print("BEST PRACTICES FOR LLM-AS-JUDGE")
print("=" * 70)

print("""
✅ DO:
  • Use specific, clear criteria
  • Provide examples of good/bad responses
  • Ask for reasoning (improves accuracy)
  • Use structured output formats
  • Test your prompts thoroughly
  • Use stronger models as judges (GPT-4, Claude Opus)

❌ DON'T:
  • Use vague criteria like "good" or "bad"
  • Forget to handle edge cases
  • Blindly trust scores without reasoning
  • Use as only evaluation method
  • Ignore cost implications

🎯 EFFECTIVE PROMPT STRUCTURE:

  1. Clear task description
  2. Specific criteria
  3. Input data (question, response, context)
  4. Scoring scale with examples
  5. Required output format
  6. Request for reasoning

💡 PRO TIPS:

  • Combine with automated metrics
  • Use for complex, subjective criteria
  • Validate with human evaluation samples
  • Monitor for judge bias
  • Consider using multiple judges
""")

# ============================================================================
# PRACTICE EXERCISE
# ============================================================================

print("\n" + "=" * 70)
print("PRACTICE EXERCISE")
print("=" * 70)

print("""
Try creating your own LLM judge prompts for:

1. Evaluating code quality
2. Checking if explanation is age-appropriate
3. Detecting sarcasm or inappropriate tone
4. Measuring helpfulness of customer support response

Remember the prompt structure:
- Clear task
- Specific criteria
- Input data
- Scoring instructions
- Output format
""")

print("\n" + "=" * 70)
print("✨ Lesson 3 Complete!")
print("=" * 70)
print("\nNext: 04_rag_evaluation.py - Learn RAG-specific evaluation!")
