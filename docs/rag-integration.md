# RAG-Based Application Integration Guide

This guide shows how to use Custom Evals to evaluate Retrieval-Augmented Generation (RAG) applications.

## 🎯 Why Evaluate RAG Systems?

RAG systems need evaluation for:
- **Faithfulness**: Is the answer grounded in retrieved context?
- **Answer Relevancy**: Does the answer address the question?
- **Context Quality**: Is the retrieved context relevant?
- **Hallucination Detection**: Is the model making things up?
- **Performance Monitoring**: Track RAG quality over time

---

## ✅ Custom Evals is Perfect for RAG!

Custom Evals provides **RAG-specific evaluators** inspired by RAGAS and DeepEval:

- ✅ **FaithfulnessEvaluator** - Checks if response is grounded in context
- ✅ **AnswerRelevancyEvaluator** - Checks if answer addresses the query
- ✅ **HallucinationEvaluator** - Detects hallucinations
- ✅ **RelevanceEvaluator** - Evaluates context relevance
- ✅ **CorrectnessEvaluator** - Compares against ground truth (if available)

---

## 🔧 Basic RAG Evaluation Pattern

```python
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

# 1. Initialize evaluators
llm = LLM(provider="openai", model="gpt-4o-mini")
faithfulness = FaithfulnessEvaluator(llm)
relevancy = AnswerRelevancyEvaluator(llm)

# 2. Run your RAG pipeline
query = "What is the capital of France?"
retrieved_context = rag_system.retrieve(query)  # Retrieved documents
generated_answer = rag_system.generate(query, retrieved_context)  # LLM response

# 3. Evaluate RAG output
faith_score = faithfulness.evaluate({
    "input": query,
    "output": generated_answer,
    "context": retrieved_context
})

rel_score = relevancy.evaluate({
    "input": query,
    "output": generated_answer
})

# 4. Check results
print(f"Faithfulness: {faith_score.label} ({faith_score.score})")
print(f"Relevancy: {rel_score.label} ({rel_score.score})")

if faith_score.label == "unfaithful":
    print(f"⚠️ Warning: {faith_score.explanation}")
```

---

## 📊 Complete RAG Evaluation Pipeline

### Comprehensive RAG Evaluation

```python
from custom.evals import (
    FaithfulnessEvaluator,
    AnswerRelevancyEvaluator,
    HallucinationEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator
)
from custom.evals.llm import LLM

class RAGEvaluator:
    """Comprehensive RAG evaluation."""

    def __init__(self):
        self.llm = LLM(provider="openai", model="gpt-4o-mini")

        # RAG-specific evaluators
        self.faithfulness = FaithfulnessEvaluator(self.llm)
        self.answer_relevancy = AnswerRelevancyEvaluator(self.llm)
        self.hallucination = HallucinationEvaluator(self.llm)
        self.context_relevance = RelevanceEvaluator(self.llm)
        self.correctness = CorrectnessEvaluator(self.llm)

    def evaluate_rag_response(self, query, answer, context, expected=None):
        """Evaluate a single RAG response."""
        results = {}

        # 1. Faithfulness: Is answer grounded in context?
        results["faithfulness"] = self.faithfulness.evaluate({
            "input": query,
            "output": answer,
            "context": context
        })

        # 2. Answer Relevancy: Does answer address the query?
        results["answer_relevancy"] = self.answer_relevancy.evaluate({
            "input": query,
            "output": answer
        })

        # 3. Hallucination: Any hallucinations?
        results["hallucination"] = self.hallucination.evaluate({
            "input": query,
            "output": answer,
            "context": context
        })

        # 4. Context Relevance: Is retrieved context relevant?
        results["context_relevance"] = self.context_relevance.evaluate({
            "input": query,
            "context": context
        })

        # 5. Correctness: If ground truth available
        if expected:
            results["correctness"] = self.correctness.evaluate({
                "input": query,
                "output": answer,
                "expected": expected
            })

        return results

    def print_report(self, results):
        """Print evaluation report."""
        print("\n" + "="*60)
        print("RAG Evaluation Report")
        print("="*60)

        for metric, score in results.items():
            print(f"\n{metric.upper()}:")
            print(f"  Label: {score.label}")
            print(f"  Score: {score.score:.2f}")
            print(f"  Explanation: {score.explanation}")

        print("\n" + "="*60)

# Example usage
evaluator = RAGEvaluator()

# Your RAG system
query = "What is machine learning?"
context = rag.retrieve(query)  # Retrieved documents
answer = rag.generate(query, context)  # Generated answer

# Evaluate
results = evaluator.evaluate_rag_response(query, answer, context)
evaluator.print_report(results)
```

---

## 🔄 RAG Framework Integration

### LangChain RAG

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

# 1. Setup LangChain RAG
vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 2. Setup evaluators
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
faithfulness = FaithfulnessEvaluator(eval_llm)
relevancy = AnswerRelevancyEvaluator(eval_llm)

# 3. Run and evaluate
query = "What is Python?"
result = qa_chain({"query": query})

answer = result["result"]
context = "\n".join([doc.page_content for doc in vectorstore.similarity_search(query)])

# Evaluate
faith_score = faithfulness.evaluate({
    "input": query,
    "output": answer,
    "context": context
})

rel_score = relevancy.evaluate({
    "input": query,
    "output": answer
})

print(f"Faithfulness: {faith_score.label} ({faith_score.score})")
print(f"Relevancy: {rel_score.label} ({rel_score.score})")
```

### LlamaIndex RAG

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

# 1. Setup LlamaIndex RAG
documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# 2. Setup evaluators
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
faithfulness = FaithfulnessEvaluator(eval_llm)
relevancy = AnswerRelevancyEvaluator(eval_llm)

# 3. Run and evaluate
query = "Summarize the document"
response = query_engine.query(query)

answer = str(response)
context = "\n".join([node.get_text() for node in response.source_nodes])

# Evaluate
faith_score = faithfulness.evaluate({
    "input": query,
    "output": answer,
    "context": context
})

rel_score = relevancy.evaluate({
    "input": query,
    "output": answer
})

print(f"Faithfulness: {faith_score.label}")
print(f"Relevancy: {rel_score.label}")
```

### Custom RAG Implementation

```python
class CustomRAG:
    def __init__(self, vectorstore, llm):
        self.vectorstore = vectorstore
        self.llm = llm

    def retrieve(self, query, k=3):
        """Retrieve relevant documents."""
        docs = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in docs])

    def generate(self, query, context):
        """Generate answer from context."""
        prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        answer = self.llm(prompt)
        return answer

    def answer(self, query):
        """Complete RAG pipeline."""
        context = self.retrieve(query)
        answer = self.generate(query, context)
        return answer, context

# Evaluate custom RAG
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

rag = CustomRAG(vectorstore, llm)
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

faithfulness = FaithfulnessEvaluator(eval_llm)
relevancy = AnswerRelevancyEvaluator(eval_llm)

query = "What is quantum computing?"
answer, context = rag.answer(query)

faith_score = faithfulness.evaluate({
    "input": query,
    "output": answer,
    "context": context
})

rel_score = relevancy.evaluate({
    "input": query,
    "output": answer
})

print(f"RAG Quality:")
print(f"  Faithfulness: {faith_score.label} ({faith_score.score})")
print(f"  Relevancy: {rel_score.label} ({rel_score.score})")
```

---

## 📊 Batch RAG Evaluation

### Evaluate RAG on Test Dataset

```python
import pandas as pd
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM

def batch_evaluate_rag(rag_system, test_cases, evaluators):
    """Evaluate RAG system on multiple queries."""
    results = []

    for test in test_cases:
        query = test["query"]

        # Run RAG pipeline
        context = rag_system.retrieve(query)
        answer = rag_system.generate(query, context)

        # Evaluate
        eval_results = {
            "query": query,
            "answer": answer,
            "expected": test.get("expected"),
        }

        for name, evaluator in evaluators.items():
            eval_input = {
                "input": query,
                "output": answer
            }

            if name == "faithfulness":
                eval_input["context"] = context

            if name == "correctness" and test.get("expected"):
                eval_input["expected"] = test["expected"]

            score = evaluator.evaluate(eval_input)

            eval_results[f"{name}_score"] = score.score
            eval_results[f"{name}_label"] = score.label

        results.append(eval_results)

    return pd.DataFrame(results)

# Example usage
llm = LLM(provider="openai", model="gpt-4o-mini")

evaluators = {
    "faithfulness": FaithfulnessEvaluator(llm),
    "answer_relevancy": AnswerRelevancyEvaluator(llm)
}

test_cases = [
    {"query": "What is Python?", "expected": "A programming language"},
    {"query": "Who created Python?", "expected": "Guido van Rossum"},
    # ... more test cases
]

df = batch_evaluate_rag(my_rag_system, test_cases, evaluators)

print("\nRAG System Performance:")
print(f"Average Faithfulness: {df['faithfulness_score'].mean():.2f}")
print(f"Average Relevancy: {df['answer_relevancy_score'].mean():.2f}")
print(f"Faithful Responses: {(df['faithfulness_label'] == 'faithful').sum()}/{len(df)}")
```

---

## 🎯 RAG-Specific Evaluation Strategies

### Strategy 1: Retrieval Quality

Evaluate the quality of retrieved context before generation.

```python
from custom.evals import RelevanceEvaluator
from custom.evals.llm import LLM

def evaluate_retrieval(query, retrieved_docs):
    """Evaluate retrieval quality."""
    llm = LLM(provider="openai", model="gpt-4o-mini")
    evaluator = RelevanceEvaluator(llm)

    context = "\n\n".join(retrieved_docs)

    score = evaluator.evaluate({
        "input": query,
        "context": context
    })

    return score

# Use it
query = "What is machine learning?"
docs = rag.retrieve(query)

retrieval_quality = evaluate_retrieval(query, docs)

if retrieval_quality.label == "irrelevant":
    print("⚠️ Poor retrieval quality - consider adjusting retrieval parameters")
else:
    print("✓ Good retrieval quality - proceeding with generation")
```

### Strategy 2: Generation Quality

Evaluate the quality of generated answer.

```python
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator, CoherenceEvaluator
from custom.evals.llm import LLM

def evaluate_generation(query, answer, context):
    """Evaluate generation quality."""
    llm = LLM(provider="openai", model="gpt-4o-mini")

    faithfulness = FaithfulnessEvaluator(llm)
    relevancy = AnswerRelevancyEvaluator(llm)
    coherence = CoherenceEvaluator(llm)

    results = {
        "faithfulness": faithfulness.evaluate({
            "input": query,
            "output": answer,
            "context": context
        }),
        "relevancy": relevancy.evaluate({
            "input": query,
            "output": answer
        }),
        "coherence": coherence.evaluate({
            "input": query,
            "output": answer
        })
    }

    return results

# Use it
generation_quality = evaluate_generation(query, answer, context)

for metric, score in generation_quality.items():
    print(f"{metric}: {score.label} ({score.score})")
```

### Strategy 3: End-to-End RAG Evaluation

Evaluate complete RAG pipeline.

```python
def evaluate_complete_rag_pipeline(query, rag_system, expected=None):
    """Complete RAG evaluation."""
    from custom.evals import (
        RelevanceEvaluator,
        FaithfulnessEvaluator,
        AnswerRelevancyEvaluator,
        CorrectnessEvaluator
    )
    from custom.evals.llm import LLM

    llm = LLM(provider="openai", model="gpt-4o-mini")

    # Phase 1: Retrieval
    docs = rag_system.retrieve(query)
    context = "\n\n".join(docs)

    retrieval_eval = RelevanceEvaluator(llm).evaluate({
        "input": query,
        "context": context
    })

    print(f"Phase 1 - Retrieval: {retrieval_eval.label}")

    # Phase 2: Generation
    answer = rag_system.generate(query, context)

    generation_evals = {
        "faithfulness": FaithfulnessEvaluator(llm).evaluate({
            "input": query,
            "output": answer,
            "context": context
        }),
        "relevancy": AnswerRelevancyEvaluator(llm).evaluate({
            "input": query,
            "output": answer
        })
    }

    print(f"Phase 2 - Generation:")
    print(f"  Faithfulness: {generation_evals['faithfulness'].label}")
    print(f"  Relevancy: {generation_evals['relevancy'].label}")

    # Phase 3: Correctness (if ground truth available)
    if expected:
        correctness = CorrectnessEvaluator(llm).evaluate({
            "input": query,
            "output": answer,
            "expected": expected
        })
        print(f"Phase 3 - Correctness: {correctness.label}")

        return retrieval_eval, generation_evals, correctness

    return retrieval_eval, generation_evals, None

# Use it
results = evaluate_complete_rag_pipeline(
    query="What is Python?",
    rag_system=my_rag,
    expected="Python is a high-level programming language"
)
```

---

## 📈 Production RAG Monitoring

### Monitor RAG Quality in Production

```python
from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
from custom.evals.llm import LLM
import logging
from datetime import datetime

class ProductionRAGMonitor:
    """Monitor RAG quality in production."""

    def __init__(self, log_file="rag_metrics.jsonl"):
        self.llm = LLM(provider="openai", model="gpt-4o-mini")
        self.faithfulness = FaithfulnessEvaluator(self.llm)
        self.relevancy = AnswerRelevancyEvaluator(self.llm)
        self.log_file = log_file

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def monitor_rag_request(self, query, answer, context):
        """Monitor a single RAG request."""
        # Evaluate
        faith_score = self.faithfulness.evaluate({
            "input": query,
            "output": answer,
            "context": context
        })

        rel_score = self.relevancy.evaluate({
            "input": query,
            "output": answer
        })

        # Log metrics
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "faithfulness": faith_score.to_dict(),
            "relevancy": rel_score.to_dict()
        }

        with open(self.log_file, "a") as f:
            f.write(json.dumps(metrics) + "\n")

        # Alert on issues
        if faith_score.label == "unfaithful":
            self.logger.warning(f"⚠️ Unfaithful response detected: {faith_score.explanation}")

        if rel_score.label == "irrelevant":
            self.logger.warning(f"⚠️ Irrelevant response detected: {rel_score.explanation}")

        return faith_score, rel_score

# Use in production
monitor = ProductionRAGMonitor()

def rag_endpoint(query):
    """RAG endpoint with monitoring."""
    context = rag.retrieve(query)
    answer = rag.generate(query, context)

    # Monitor quality
    faith_score, rel_score = monitor.monitor_rag_request(query, answer, context)

    return {
        "answer": answer,
        "quality": {
            "faithfulness": faith_score.label,
            "relevancy": rel_score.label
        }
    }
```

---

## 🎯 RAG Optimization with Evaluations

### A/B Test RAG Configurations

```python
def compare_rag_configurations(query, config_a, config_b):
    """Compare two RAG configurations."""
    from custom.evals import FaithfulnessEvaluator, AnswerRelevancyEvaluator
    from custom.evals.llm import LLM

    llm = LLM(provider="openai", model="gpt-4o-mini")
    faithfulness = FaithfulnessEvaluator(llm)
    relevancy = AnswerRelevancyEvaluator(llm)

    results = {}

    for name, rag_config in [("Config A", config_a), ("Config B", config_b)]:
        # Run RAG with this config
        context = rag_config.retrieve(query)
        answer = rag_config.generate(query, context)

        # Evaluate
        faith_score = faithfulness.evaluate({
            "input": query,
            "output": answer,
            "context": context
        })

        rel_score = relevancy.evaluate({
            "input": query,
            "output": answer
        })

        results[name] = {
            "faithfulness": faith_score.score,
            "relevancy": rel_score.score,
            "avg_score": (faith_score.score + rel_score.score) / 2
        }

    # Compare
    winner = max(results.items(), key=lambda x: x[1]["avg_score"])
    print(f"\nWinner: {winner[0]}")
    print(f"  Avg Score: {winner[1]['avg_score']:.2f}")

    return results

# Example
results = compare_rag_configurations(
    query="What is AI?",
    config_a=rag_with_3_chunks,
    config_b=rag_with_5_chunks
)
```

---

## ✅ Best Practices for RAG Evaluation

1. **Always Evaluate Faithfulness** - Critical for RAG systems
2. **Check Both Retrieval and Generation** - Evaluate each stage
3. **Use Multiple Metrics** - Combine faithfulness, relevancy, coherence
4. **Batch Test Regularly** - Regression testing on test set
5. **Monitor Production** - Track quality metrics in real-time
6. **Compare Configurations** - A/B test different RAG setups
7. **Log Evaluations** - Track metrics over time

---

## 📚 See Also

- [Agents Integration](agents-integration.md) - For RAG-based agents
- [Test Case Documentation](testing.md) - Test your RAG system
- [Phoenix Tracing](tracing.md) - Enable observability
- [Examples](../examples/rag_integration.py) - Complete examples

---

**Your RAG system is now ready for comprehensive evaluation! 🎉**
