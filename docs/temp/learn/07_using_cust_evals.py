"""
Lesson 7: Using the Custom Evaluation Framework (cust-evals)

Learn to use the custom evaluation framework provided in this repository.
Brings together everything you've learned!

Learning Objectives:
- Use cust-evals library
- Create custom evaluators
- Integrate with your code
- Leverage advanced features

Prerequisites: Lessons 1-6
"""

# Import from the custom framework
# Note: Adjust path based on your setup
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

try:
    from custom.evals.llm_evaluators import LLMEvaluator
    FRAMEWORK_AVAILABLE = True
except ImportError:
    FRAMEWORK_AVAILABLE = False
    print("Note: cust-evals not in path. This lesson shows usage patterns.")

print("=" * 70)
print("LESSON 7: Using the Custom Evaluation Framework")
print("=" * 70)

print("""
🎓 WHAT IS CUST-EVALS?

This repository's custom evaluation framework provides:
✓ Pre-built evaluators
✓ LLM-as-judge integrations
✓ Tracing and observability
✓ Metrics collection
✓ Production-ready patterns

Let's explore how to use it!
""")

# ============================================================================
# PATTERN 1: BASIC USAGE
# ============================================================================

print("\n" + "=" * 70)
print("PATTERN 1: Basic Evaluator Usage")
print("=" * 70)

print("""
# Standard usage pattern:

from custom.evals.llm_evaluators import LLMEvaluator

# Create evaluator
evaluator = LLMEvaluator(
    model="gpt-4",
    criteria="accuracy and completeness"
)

# Evaluate a response
result = evaluator.evaluate(
    input="What is machine learning?",
    output="ML is a subset of AI that learns from data.",
    context="Machine learning uses algorithms to learn patterns."
)

# Check results
print(f"Score: {result.score}")
print(f"Passed: {result.passed}")
print(f"Reasoning: {result.reasoning}")
""")

# ============================================================================
# PATTERN 2: CUSTOM EVALUATORS
# ============================================================================

print("\n" + "=" * 70)
print("PATTERN 2: Creating Custom Evaluators")
print("=" * 70)

print("""
# Extend the base evaluator:

from custom.evals.llm_evaluators import BaseEvaluator

class MyCustomEvaluator(BaseEvaluator):
    def evaluate(self, input, output, **kwargs):
        # Your evaluation logic
        score = self.calculate_score(output)
        
        return {
            'score': score,
            'passed': score >= self.threshold,
            'details': {'custom_metric': score}
        }
    
    def calculate_score(self, text):
        # Custom scoring logic
        return 0.85

# Use it:
evaluator = MyCustomEvaluator(threshold=0.7)
result = evaluator.evaluate(input="test", output="response")
""")

# ============================================================================
# PATTERN 3: BATCH EVALUATION
# ============================================================================

print("\n" + "=" * 70)
print("PATTERN 3: Batch Evaluation")
print("=" * 70)

print("""
# Evaluate multiple examples:

from custom.evals import BatchEvaluator

# Prepare test data
test_cases = [
    {
        'input': 'Question 1',
        'output': 'Answer 1',
        'expected': 'Expected 1'
    },
    # ... more cases
]

# Run batch evaluation
batch_evaluator = BatchEvaluator(
    evaluator=my_evaluator,
    test_cases=test_cases
)

results = batch_evaluator.run()

# Analyze results
print(f"Pass rate: {results.pass_rate}")
print(f"Avg score: {results.avg_score}")
print(f"Failed cases: {results.failures}")
""")

# ============================================================================
# PATTERN 4: TRACING & OBSERVABILITY
# ============================================================================

print("\n" + "=" * 70)
print("PATTERN 4: Tracing & Observability")
print("=" * 70)

print("""
# Enable tracing for debugging:

from custom.evals.tracing import trace_evaluation

@trace_evaluation(service_name="my-llm-app")
def my_llm_function(input_text):
    # Your LLM code
    response = generate_response(input_text)
    return response

# Tracing automatically captures:
# - Input/output
# - Latency
# - Evaluation scores
# - Errors

# View traces in Phoenix or other observability tools
""")

# ============================================================================
# PATTERN 5: METRICS COLLECTION
# ============================================================================

print("\n" + "=" * 70)
print("PATTERN 5: Metrics Collection")
print("=" * 70)

print("""
# Collect and export metrics:

from custom.evals.metrics import MetricsCollector

collector = MetricsCollector()

# Log evaluation metrics
collector.log_evaluation(
    score=0.85,
    passed=True,
    latency_ms=150,
    model="gpt-4",
    tags={'env': 'production'}
)

# Export to monitoring systems
collector.export_prometheus()  # Prometheus format
collector.export_datadog()     # Datadog format
collector.get_summary()        # Summary stats
""")

# ============================================================================
# COMPLETE EXAMPLE
# ============================================================================

print("\n" + "=" * 70)
print("COMPLETE EXAMPLE: RAG System Evaluation")
print("=" * 70)

print("""
# Full example combining everything:

from custom.evals.llm_evaluators import LLMEvaluator
from custom.evals.rag_evaluators import RAGEvaluator
from custom.evals.tracing import trace_evaluation
from custom.evals.metrics import MetricsCollector

# Setup
metrics = MetricsCollector()

# Create specialized evaluators
faithfulness_eval = RAGEvaluator(
    criteria="faithfulness",
    threshold=0.8
)

relevance_eval = LLMEvaluator(
    model="gpt-4",
    criteria="answer relevance to question"
)

# Trace your RAG function
@trace_evaluation(service_name="rag-qa-system")
def rag_qa_system(question):
    # 1. Retrieve context
    contexts = retrieve_documents(question)
    
    # 2. Generate answer
    answer = generate_answer(question, contexts)
    
    # 3. Evaluate
    faith_result = faithfulness_eval.evaluate(
        output=answer,
        context=contexts
    )
    
    rel_result = relevance_eval.evaluate(
        input=question,
        output=answer
    )
    
    # 4. Log metrics
    metrics.log_evaluation(
        score=(faith_result.score + rel_result.score) / 2,
        passed=faith_result.passed and rel_result.passed,
        tags={'component': 'rag'}
    )
    
    return answer

# Use it
answer = rag_qa_system("What is quantum computing?")
print(f"Answer: {answer}")

# View metrics
print(metrics.get_summary())
""")

# ============================================================================
# INTEGRATION PATTERNS
# ============================================================================

print("\n" + "=" * 70)
print("INTEGRATION PATTERNS")
print("=" * 70)

print("""
🔌 COMMON INTEGRATIONS:

1. LangChain Integration:
   
   from custom.evals.integrations.langchain import LangChainEvaluator
   
   evaluator = LangChainEvaluator()
   evaluator.evaluate_chain(my_chain, test_cases)

2. LlamaIndex Integration:
   
   from custom.evals.integrations.llamaindex import LlamaIndexEvaluator
   
   evaluator = LlamaIndexEvaluator()
   evaluator.evaluate_query_engine(engine, questions)

3. FastAPI Integration:
   
   from custom.evals.integrations.fastapi import evaluation_middleware
   
   app.add_middleware(evaluation_middleware, 
                       evaluator=my_evaluator)

4. Pytest Integration:
   
   from custom.evals.testing import llm_test
   
   @llm_test(evaluator=my_evaluator, threshold=0.8)
   def test_my_llm():
       response = my_llm("test input")
       return response
""")

# ============================================================================
# CONFIGURATION
# ============================================================================

print("\n" + "=" * 70)
print("CONFIGURATION")
print("=" * 70)

print("""
# Configure via environment variables or config file:

# .env file:
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
EVAL_THRESHOLD=0.7
TRACING_ENABLED=true
PHOENIX_ENDPOINT=http://localhost:6006

# Or config.yaml:
evaluation:
  default_threshold: 0.7
  llm_model: gpt-4
  enable_tracing: true
  
tracing:
  service_name: my-app
  endpoint: http://localhost:6006
  
metrics:
  export_format: prometheus
  export_interval: 60

# Load in code:
from custom.evals.config import load_config

config = load_config()
evaluator = LLMEvaluator(**config.evaluation)
""")

# ============================================================================
# BEST PRACTICES
# ============================================================================

print("\n" + "=" * 70)
print("BEST PRACTICES")
print("=" * 70)

print("""
✅ DO:

1. Start with pre-built evaluators
2. Add tracing early
3. Monitor metrics in production
4. Version your test datasets
5. Use appropriate thresholds
6. Combine multiple evaluators
7. Log all evaluation results
8. Review failures manually

❌ DON'T:

1. Over-evaluate (adds latency)
2. Ignore evaluation results
3. Use single evaluator only
4. Skip validation
5. Forget edge cases
6. Hardcode thresholds
7. Miss tracking changes

🎯 WORKFLOW:

1. Development:
   • Use batch evaluation
   • Iterate on test cases
   • Tune thresholds
   
2. Staging:
   • Enable tracing
   • Run full test suite
   • Validate metrics
   
3. Production:
   • Online evaluation
   • Continuous monitoring
   • Alert on anomalies
   • A/B test changes
""")

# ============================================================================
# FURTHER LEARNING
# ============================================================================

print("\n" + "=" * 70)
print("FURTHER LEARNING")
print("=" * 70)

print("""
📚 NEXT STEPS:

1. Read the framework documentation:
   → See /docs for detailed guides

2. Explore example implementations:
   → See /examples for working code

3. Check out integrations:
   → See /src/custom/evals/integrations

4. Review test suite:
   → See /tests for testing patterns

5. Compare with other frameworks:
   → See /docs/compare_eval_frameworks

🔗 USEFUL RESOURCES:

• Framework docs: ./docs/
• Examples: ./examples/
• Source code: ./src/custom/evals/
• Tests: ./tests/
• Configuration: ./configs/

💡 TIP: Start small!

Begin with one evaluator on one task, then expand:
1. Single eval metric → Multiple metrics
2. Manual testing → Automated testing
3. Development only → Production monitoring
4. Basic logging → Full observability
""")

# ============================================================================
# CONCLUSION
# ============================================================================

print("\n\n" + "=" * 70)
print("CONGRATULATIONS!")
print("=" * 70)

print("""
🎉 You've completed the evaluation learning path!

You now know:
✅ What LLM evaluation is and why it matters
✅ Different types of metrics (exact match, similarity, etc.)
✅ How to use LLMs as judges
✅ RAG-specific evaluation patterns
✅ Building custom metrics
✅ Production evaluation patterns
✅ Using the cust-evals framework

🚀 YOU'RE READY TO:

• Evaluate your LLM applications
• Build custom evaluators
• Monitor production systems
• Improve model quality
• Make data-driven decisions

Keep learning, keep evaluating, keep improving!

📖 Resources:
• Framework comparison: ../compare_eval_frameworks/
• Official docs: ../
• Examples: ../../examples/
• Source code: ../../src/

Happy evaluating! 🎯
""")

print("=" * 70)
print("✨ Learning Path Complete!")
print("=" * 70)
