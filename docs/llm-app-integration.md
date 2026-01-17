# LLM Application Integration Guide

This guide shows you how to integrate Custom Evals with simple LLM applications like chatbots, Q&A systems, summarization tools, and classification tasks.

## Table of Contents

- [Why Evaluate LLM Applications?](#why-evaluate-llm-applications)
- [Yes, Works with ALL LLM Applications!](#yes-works-with-all-llm-applications)
- [Quick Start](#quick-start)
- [LLM Application Types](#llm-application-types)
- [Integration Patterns](#integration-patterns)
- [Conversational Applications](#conversational-applications)
- [Production Monitoring](#production-monitoring)
- [Batch Testing](#batch-testing)
- [Best Practices](#best-practices)
- [Quick Reference](#quick-reference)

---

## Why Evaluate LLM Applications?

LLM applications face several quality challenges:

1. **Response Quality**: Ensuring outputs are coherent, relevant, and accurate
2. **Hallucinations**: Detecting when the model generates false information
3. **Tone & Style**: Maintaining consistent tone across responses
4. **User Satisfaction**: Measuring if responses meet user expectations
5. **Cost vs Quality**: Balancing API costs with output quality

**Custom Evals helps you:**
- ✅ Automatically evaluate every LLM response
- ✅ Detect quality issues in real-time
- ✅ Compare different models and prompts
- ✅ Monitor production quality
- ✅ Build confidence in your LLM application

---

## Yes, Works with ALL LLM Applications!

**Custom Evals is framework-agnostic.** It works with:

- ✅ **Direct OpenAI API calls** (openai library)
- ✅ **Direct Anthropic API calls** (anthropic library)
- ✅ **LangChain applications** (chains, prompts, etc.)
- ✅ **LlamaIndex applications** (query engines, chat engines)
- ✅ **Custom LLM wrappers** (your own implementation)
- ✅ **Any framework** that produces text output

**Why?** Because Custom Evals evaluates **text outputs**, not specific frameworks.

---

## Quick Start

### Installation

```bash
# Install Custom Evals
pip install -e .

# Optional: Install tracing for observability
pip install -e ".[dev,tracing]"
```

### Basic Evaluation (4 Steps)

```python
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM

# 1. Initialize evaluator
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(llm)

# 2. Run your LLM application
user_input = "Explain quantum computing"
llm_output = your_llm_app(user_input)

# 3. Evaluate output
score = evaluator.evaluate({
    "input": user_input,
    "output": llm_output
})

# 4. Check quality
print(f"Coherence: {score.label} ({score.score})")
print(f"Explanation: {score.explanation}")
```

That's it! The same pattern works for **ANY** LLM application.

---

## LLM Application Types

### 1. Question Answering Systems

**Use Case**: Answer user questions with LLM-generated responses

```python
from custom.evals import CorrectnessEvaluator, CoherenceEvaluator
from custom.evals.llm import LLM
import openai

# Your Q&A system
def qa_system(question: str) -> str:
    """Simple Q&A using OpenAI."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

# Setup evaluators
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
coherence = CoherenceEvaluator(eval_llm)
correctness = CorrectnessEvaluator(eval_llm)

# Run and evaluate
question = "What is the capital of France?"
answer = qa_system(question)

# Evaluate coherence
coh_score = coherence.evaluate({
    "input": question,
    "output": answer
})

# Evaluate correctness (with ground truth)
corr_score = correctness.evaluate({
    "input": question,
    "output": answer,
    "expected": "Paris is the capital of France."
})

print(f"Coherence: {coh_score.label} ({coh_score.score})")
print(f"Correctness: {corr_score.label} ({corr_score.score})")
```

### 2. Text Summarization

**Use Case**: Summarize long documents or articles

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

def summarize_text(text: str) -> str:
    """Summarize text using LLM."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Summarize the following text concisely:\n\n{text}"
        }]
    )
    return response.choices[0].message.content

# Setup evaluators
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
coherence = CoherenceEvaluator(eval_llm)
relevance = RelevanceEvaluator(eval_llm)

# Original text
original_text = """
[Your long document here...]
"""

# Generate summary
summary = summarize_text(original_text)

# Evaluate coherence
coh_score = coherence.evaluate({
    "input": "Summarize this text",
    "output": summary
})

# Evaluate relevance (summary should be relevant to original)
rel_score = relevance.evaluate({
    "input": "Summarize this text",
    "context": original_text,
    "output": summary
})

print(f"Summary Coherence: {coh_score.label}")
print(f"Summary Relevance: {rel_score.label}")
```

### 3. Chatbots & Conversational AI

**Use Case**: Multi-turn conversations with context

```python
from custom.evals import CoherenceEvaluator, ToxicityEvaluator
from custom.evals.llm import LLM

class SimpleChatbot:
    """Simple chatbot with conversation history."""

    def __init__(self):
        self.history = []

    def chat(self, user_message: str) -> str:
        """Send message and get response."""
        self.history.append({"role": "user", "content": user_message})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a friendly assistant."}
            ] + self.history
        )

        bot_message = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": bot_message})
        return bot_message

# Setup chatbot and evaluators
chatbot = SimpleChatbot()
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
coherence = CoherenceEvaluator(eval_llm)
toxicity = ToxicityEvaluator(eval_llm)

# Chat and evaluate each response
user_message = "Tell me about artificial intelligence"
bot_response = chatbot.chat(user_message)

# Evaluate response quality
coh_score = coherence.evaluate({
    "input": user_message,
    "output": bot_response
})

tox_score = toxicity.evaluate({
    "input": user_message,
    "output": bot_response
})

print(f"Coherence: {coh_score.label}")
print(f"Toxicity: {tox_score.label}")

# Continue conversation
next_message = "Can you explain it more simply?"
next_response = chatbot.chat(next_message)

# Evaluate with conversation context
next_coh_score = coherence.evaluate({
    "input": next_message,
    "output": next_response
})
```

### 4. Text Classification

**Use Case**: Classify text into categories using LLM

```python
from custom.evals import custom_accuracy
from custom.evals.llm import LLM

def classify_sentiment(text: str) -> str:
    """Classify sentiment using LLM."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Classify the sentiment of this text as positive, negative, or neutral:\n\n{text}\n\nRespond with only one word: positive, negative, or neutral."
        }]
    )
    return response.choices[0].message.content.strip().lower()

# Test classification
test_cases = [
    {"text": "This product is amazing!", "expected": "positive"},
    {"text": "Terrible experience, very disappointed.", "expected": "negative"},
    {"text": "The package arrived on time.", "expected": "neutral"}
]

# Evaluate classification accuracy
correct = 0
total = len(test_cases)

for case in test_cases:
    prediction = classify_sentiment(case["text"])

    # Use custom_accuracy to evaluate
    score = custom_accuracy(
        {"output": prediction, "expected": case["expected"]},
        normalize=True
    )

    if score.label == "correct":
        correct += 1

    print(f"Text: {case['text']}")
    print(f"Expected: {case['expected']}, Got: {prediction}")
    print(f"Score: {score.label}\n")

accuracy = correct / total
print(f"Overall Accuracy: {accuracy:.2%}")
```

### 5. Content Generation

**Use Case**: Generate blog posts, emails, or creative content

```python
from custom.evals import CoherenceEvaluator, CreativityEvaluator
from custom.evals.llm import LLM

def generate_blog_post(topic: str, tone: str = "professional") -> str:
    """Generate blog post content."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Write a {tone} blog post about: {topic}\n\nLength: ~300 words"
        }]
    )
    return response.choices[0].message.content

# Setup evaluators
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
coherence = CoherenceEvaluator(eval_llm)

# Generate content
topic = "The Future of Artificial Intelligence"
blog_post = generate_blog_post(topic)

# Evaluate coherence
coh_score = coherence.evaluate({
    "input": f"Write a blog post about: {topic}",
    "output": blog_post
})

print(f"Coherence: {coh_score.label} ({coh_score.score})")
print(f"Explanation: {coh_score.explanation}")
```

---

## Integration Patterns

### Pattern 1: Direct OpenAI Integration

```python
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM
import openai

# Configure OpenAI
openai.api_key = "your-api-key"

# Setup evaluator
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)

# Your LLM call
def call_llm(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Evaluate
prompt = "Explain photosynthesis"
output = call_llm(prompt)

score = evaluator.evaluate({
    "input": prompt,
    "output": output
})
```

### Pattern 2: LangChain Integration

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM

# Setup LangChain
llm_langchain = OpenAI(temperature=0.7)
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple terms."
)
chain = LLMChain(llm=llm_langchain, prompt=prompt)

# Setup evaluator
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)

# Run chain and evaluate
topic = "blockchain"
output = chain.run(topic=topic)

score = evaluator.evaluate({
    "input": f"Explain {topic} in simple terms.",
    "output": output
})
```

### Pattern 3: LlamaIndex Integration

```python
from llama_index import GPTSimpleVectorIndex, Document
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM

# Setup LlamaIndex
documents = [Document(text="Your document text...")]
index = GPTSimpleVectorIndex.from_documents(documents)

# Setup evaluator
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)

# Query and evaluate
query = "What is the main topic?"
response = index.query(query)

score = evaluator.evaluate({
    "input": query,
    "output": str(response)
})
```

### Pattern 4: Anthropic Claude Integration

```python
from anthropic import Anthropic
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM

# Setup Anthropic
client = Anthropic(api_key="your-api-key")

# Setup evaluator (using OpenAI for evaluation)
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)

# Your Claude call
def call_claude(prompt: str) -> str:
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

# Evaluate
prompt = "What is quantum computing?"
output = call_claude(prompt)

score = evaluator.evaluate({
    "input": prompt,
    "output": output
})
```

---

## Conversational Applications

### Multi-Turn Conversation Evaluation

```python
from custom.evals import CoherenceEvaluator, RelevanceEvaluator
from custom.evals.llm import LLM

class EvaluatedChatbot:
    """Chatbot with automatic evaluation."""

    def __init__(self):
        self.history = []

        # Setup evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.coherence_eval = CoherenceEvaluator(eval_llm)
        self.relevance_eval = RelevanceEvaluator(eval_llm)

        self.quality_scores = []

    def chat(self, user_message: str) -> dict:
        """Chat and return response with quality scores."""

        # Generate response
        self.history.append({"role": "user", "content": user_message})
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."}
            ] + self.history
        )
        bot_response = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": bot_response})

        # Evaluate response
        coh_score = self.coherence_eval.evaluate({
            "input": user_message,
            "output": bot_response
        })

        # Get conversation context (last 3 messages)
        context = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.history[-3:]
        ])

        rel_score = self.relevance_eval.evaluate({
            "input": user_message,
            "context": context,
            "output": bot_response
        })

        # Store scores
        quality = {
            "coherence": coh_score,
            "relevance": rel_score
        }
        self.quality_scores.append(quality)

        return {
            "response": bot_response,
            "quality": quality
        }

    def get_average_quality(self) -> dict:
        """Get average quality scores across conversation."""
        if not self.quality_scores:
            return {}

        avg_coherence = sum(
            s["coherence"].score for s in self.quality_scores
        ) / len(self.quality_scores)

        avg_relevance = sum(
            s["relevance"].score for s in self.quality_scores
        ) / len(self.quality_scores)

        return {
            "avg_coherence": avg_coherence,
            "avg_relevance": avg_relevance
        }

# Usage
chatbot = EvaluatedChatbot()

# Turn 1
result1 = chatbot.chat("What is machine learning?")
print(f"Response: {result1['response']}")
print(f"Coherence: {result1['quality']['coherence'].label}")

# Turn 2
result2 = chatbot.chat("Can you give me an example?")
print(f"Response: {result2['response']}")
print(f"Coherence: {result2['quality']['coherence'].label}")

# Overall quality
avg_quality = chatbot.get_average_quality()
print(f"\nAverage Coherence: {avg_quality['avg_coherence']:.2f}")
print(f"Average Relevance: {avg_quality['avg_relevance']:.2f}")
```

### Context-Aware Evaluation

```python
def evaluate_with_context(user_input: str, bot_response: str, history: list) -> dict:
    """Evaluate response considering conversation history."""

    eval_llm = LLM(provider="openai", model="gpt-4o-mini")
    coherence = CoherenceEvaluator(eval_llm)
    relevance = RelevanceEvaluator(eval_llm)

    # Format history as context
    context = "\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in history[-5:]  # Last 5 messages
    ])

    # Evaluate coherence
    coh_score = coherence.evaluate({
        "input": user_input,
        "output": bot_response
    })

    # Evaluate relevance to conversation
    rel_score = relevance.evaluate({
        "input": user_input,
        "context": context,
        "output": bot_response
    })

    return {
        "coherence": coh_score,
        "relevance": rel_score
    }
```

---

## Production Monitoring

### Real-Time Quality Monitoring

```python
from custom.evals import CoherenceEvaluator, HallucinationEvaluator
from custom.evals.llm import LLM
import logging

class MonitoredLLMApp:
    """LLM application with production monitoring."""

    def __init__(self):
        # Setup evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.coherence_eval = CoherenceEvaluator(eval_llm)
        self.hallucination_eval = HallucinationEvaluator(eval_llm)

        # Quality thresholds
        self.coherence_threshold = 0.7
        self.hallucination_threshold = 0.3

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_response(self, user_input: str, context: str = None) -> dict:
        """Generate response with quality monitoring."""

        # Generate response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        output = response.choices[0].message.content

        # Evaluate quality
        coh_score = self.coherence_eval.evaluate({
            "input": user_input,
            "output": output
        })

        # Check for hallucinations if context provided
        hall_score = None
        if context:
            hall_score = self.hallucination_eval.evaluate({
                "input": user_input,
                "output": output,
                "context": context
            })

        # Log quality metrics
        self.logger.info(f"Coherence: {coh_score.score:.2f}")
        if hall_score:
            self.logger.info(f"Hallucination: {hall_score.score:.2f}")

        # Alert on quality issues
        if coh_score.score < self.coherence_threshold:
            self.logger.warning(f"Low coherence detected: {coh_score.score:.2f}")

        if hall_score and hall_score.score > self.hallucination_threshold:
            self.logger.warning(f"Potential hallucination: {hall_score.score:.2f}")

        return {
            "response": output,
            "quality": {
                "coherence": coh_score,
                "hallucination": hall_score
            }
        }

# Usage
app = MonitoredLLMApp()

result = app.generate_response(
    user_input="What is the weather?",
    context="I don't have access to real-time weather data."
)

print(f"Response: {result['response']}")
print(f"Coherence: {result['quality']['coherence'].label}")
```

### Quality Metrics Dashboard

```python
from collections import defaultdict
from datetime import datetime

class QualityDashboard:
    """Track and report quality metrics over time."""

    def __init__(self):
        self.metrics = defaultdict(list)

    def log_evaluation(self, eval_type: str, score: float):
        """Log an evaluation score."""
        self.metrics[eval_type].append({
            "score": score,
            "timestamp": datetime.now()
        })

    def get_stats(self, eval_type: str, hours: int = 24) -> dict:
        """Get statistics for last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)

        recent_scores = [
            m["score"] for m in self.metrics[eval_type]
            if m["timestamp"] > cutoff
        ]

        if not recent_scores:
            return {}

        return {
            "count": len(recent_scores),
            "avg": sum(recent_scores) / len(recent_scores),
            "min": min(recent_scores),
            "max": max(recent_scores)
        }

    def print_summary(self):
        """Print summary of all metrics."""
        print("\n=== Quality Metrics Summary ===")
        for eval_type in self.metrics:
            stats = self.get_stats(eval_type)
            if stats:
                print(f"\n{eval_type}:")
                print(f"  Count: {stats['count']}")
                print(f"  Average: {stats['avg']:.2f}")
                print(f"  Min: {stats['min']:.2f}, Max: {stats['max']:.2f}")

# Usage
dashboard = QualityDashboard()

# Log evaluations
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)

for _ in range(10):
    output = your_llm_app("test query")
    score = evaluator.evaluate({
        "input": "test query",
        "output": output
    })
    dashboard.log_evaluation("coherence", score.score)

# View summary
dashboard.print_summary()
```

---

## Batch Testing

### Test Suite for LLM Application

```python
from custom.evals import CoherenceEvaluator, CorrectnessEvaluator
from custom.evals.llm import LLM

def batch_test_llm_app(test_cases: list) -> dict:
    """Run batch evaluation on test cases."""

    # Setup evaluators
    eval_llm = LLM(provider="openai", model="gpt-4o-mini")
    coherence = CoherenceEvaluator(eval_llm)
    correctness = CorrectnessEvaluator(eval_llm)

    results = []

    for case in test_cases:
        # Generate response
        output = your_llm_app(case["input"])

        # Evaluate
        coh_score = coherence.evaluate({
            "input": case["input"],
            "output": output
        })

        corr_score = None
        if "expected" in case:
            corr_score = correctness.evaluate({
                "input": case["input"],
                "output": output,
                "expected": case["expected"]
            })

        results.append({
            "input": case["input"],
            "output": output,
            "coherence": coh_score,
            "correctness": corr_score
        })

    # Calculate pass rate
    coherent = sum(1 for r in results if r["coherence"].label == "coherent")
    pass_rate = coherent / len(results)

    return {
        "results": results,
        "pass_rate": pass_rate,
        "total": len(results)
    }

# Test cases
test_cases = [
    {"input": "What is Python?", "expected": "Python is a programming language"},
    {"input": "Explain AI", "expected": "AI stands for Artificial Intelligence"},
    {"input": "What is 2+2?", "expected": "4"}
]

# Run batch test
batch_results = batch_test_llm_app(test_cases)

print(f"Pass Rate: {batch_results['pass_rate']:.1%}")
print(f"Total Tests: {batch_results['total']}")

# Print details
for i, result in enumerate(batch_results['results'], 1):
    print(f"\nTest {i}:")
    print(f"  Input: {result['input']}")
    print(f"  Coherence: {result['coherence'].label}")
    if result['correctness']:
        print(f"  Correctness: {result['correctness'].label}")
```

### Regression Testing

```python
def regression_test(baseline_results: dict, current_results: dict) -> dict:
    """Compare current results against baseline."""

    comparison = {
        "baseline_pass_rate": baseline_results["pass_rate"],
        "current_pass_rate": current_results["pass_rate"],
        "change": current_results["pass_rate"] - baseline_results["pass_rate"]
    }

    # Detailed comparison
    regressions = []
    improvements = []

    for baseline, current in zip(
        baseline_results["results"],
        current_results["results"]
    ):
        if baseline["coherence"].label == "coherent" and current["coherence"].label != "coherent":
            regressions.append(baseline["input"])
        elif baseline["coherence"].label != "coherent" and current["coherence"].label == "coherent":
            improvements.append(baseline["input"])

    comparison["regressions"] = regressions
    comparison["improvements"] = improvements

    return comparison

# Run baseline
baseline = batch_test_llm_app(test_cases)

# Make changes to your app
# ...

# Run current
current = batch_test_llm_app(test_cases)

# Compare
comparison = regression_test(baseline, current)

print(f"Pass Rate Change: {comparison['change']:+.1%}")
if comparison["regressions"]:
    print(f"Regressions: {len(comparison['regressions'])}")
```

---

## Best Practices

### 1. Choose Appropriate Evaluators

```python
# For Q&A systems
evaluators = [
    CoherenceEvaluator(llm),      # Response makes sense
    CorrectnessEvaluator(llm),    # Response is correct
    RelevanceEvaluator(llm)       # Response is relevant
]

# For chatbots
evaluators = [
    CoherenceEvaluator(llm),      # Response is coherent
    ToxicityEvaluator(llm),       # Response is not toxic
    RelevanceEvaluator(llm)       # Response is contextual
]

# For summarization
evaluators = [
    CoherenceEvaluator(llm),      # Summary is coherent
    RelevanceEvaluator(llm)       # Summary captures key points
]

# For content generation
evaluators = [
    CoherenceEvaluator(llm),      # Content is coherent
    HallucinationEvaluator(llm)   # Content is factual
]
```

### 2. Multi-Metric Evaluation

```python
def comprehensive_evaluation(input_text: str, output: str, context: str = None) -> dict:
    """Evaluate using multiple metrics."""

    eval_llm = LLM(provider="openai", model="gpt-4o-mini")

    evaluators = {
        "coherence": CoherenceEvaluator(eval_llm),
        "relevance": RelevanceEvaluator(eval_llm),
        "toxicity": ToxicityEvaluator(eval_llm)
    }

    if context:
        evaluators["hallucination"] = HallucinationEvaluator(eval_llm)

    results = {}
    for name, evaluator in evaluators.items():
        eval_input = {"input": input_text, "output": output}
        if name in ["relevance", "hallucination"] and context:
            eval_input["context"] = context

        results[name] = evaluator.evaluate(eval_input)

    # Calculate overall score
    avg_score = sum(r.score for r in results.values()) / len(results)

    return {
        "scores": results,
        "overall": avg_score
    }
```

### 3. Set Quality Thresholds

```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,      # Minimum 70% coherent
    "correctness": 0.8,    # Minimum 80% correct
    "toxicity": 0.1,       # Maximum 10% toxic
    "hallucination": 0.2   # Maximum 20% hallucination
}

def check_quality_gates(scores: dict) -> bool:
    """Check if response meets quality thresholds."""

    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric not in scores:
            continue

        score = scores[metric].score

        # Lower is better for toxicity and hallucination
        if metric in ["toxicity", "hallucination"]:
            if score > threshold:
                return False
        else:
            if score < threshold:
                return False

    return True

# Usage
scores = comprehensive_evaluation(user_input, llm_output, context)
passes = check_quality_gates(scores["scores"])

if not passes:
    # Handle quality failure (retry, use fallback, alert, etc.)
    pass
```

### 4. Cache Evaluation Results

```python
from functools import lru_cache
import hashlib

def hash_input(input_text: str, output: str) -> str:
    """Create hash of input/output pair."""
    combined = f"{input_text}|{output}"
    return hashlib.md5(combined.encode()).hexdigest()

@lru_cache(maxsize=1000)
def cached_evaluate(input_hash: str, evaluator_name: str) -> dict:
    """Cached evaluation (in-memory)."""
    # This would be called with the actual evaluation
    pass

# For persistent caching, use a database or file
class EvaluationCache:
    """Persistent evaluation cache."""

    def __init__(self, cache_file: str = "eval_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()

    def _load_cache(self) -> dict:
        """Load cache from file."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """Save cache to file."""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def get(self, input_text: str, output: str, evaluator: str):
        """Get cached evaluation."""
        key = hash_input(input_text, output)
        return self.cache.get(f"{key}_{evaluator}")

    def set(self, input_text: str, output: str, evaluator: str, result: dict):
        """Cache evaluation result."""
        key = hash_input(input_text, output)
        self.cache[f"{key}_{evaluator}"] = result
        self._save_cache()
```

### 5. Use Phoenix Tracing (Optional)

```python
from custom.evals import initialize_tracing

# Initialize tracing (optional)
initialize_tracing(
    phoenix_endpoint="http://localhost:6006/v1/traces",
    project_name="my-llm-app"
)

# All evaluations now automatically traced in Phoenix UI!
```

---

## Quick Reference

### Universal 4-Step Pattern

```python
from custom.evals import [Evaluator]
from custom.evals.llm import LLM

# 1. Initialize evaluator
llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = [Evaluator](llm)

# 2. Run your LLM application
output = your_llm_app(input)

# 3. Evaluate output
score = evaluator.evaluate({
    "input": input,
    "output": output
})

# 4. Check quality
print(f"Quality: {score.label} ({score.score})")
```

### Available Evaluators

**Code-Based Metrics:**
- `exact_match()` - Exact string matching
- `sentiment_score()` - Sentiment analysis
- `custom_accuracy()` - Accuracy with normalization

**LLM-Based Evaluators:**
- `HallucinationEvaluator` - Detect false information
- `ToxicityEvaluator` - Detect toxic content
- `CorrectnessEvaluator` - Evaluate correctness
- `CoherenceEvaluator` - Evaluate coherence
- `RelevanceEvaluator` - Evaluate relevance
- `BiasEvaluator` - Detect bias

**RAG-Specific Evaluators:**
- `FaithfulnessEvaluator` - Check faithfulness to context
- `AnswerRelevancyEvaluator` - Check answer relevancy

### Common Patterns

**Single Evaluation:**
```python
score = evaluator.evaluate({"input": input, "output": output})
```

**Multi-Metric:**
```python
scores = {
    "coherence": coherence_eval.evaluate({...}),
    "toxicity": toxicity_eval.evaluate({...})
}
```

**Batch Testing:**
```python
results = [
    evaluator.evaluate({"input": case["input"], "output": output})
    for case in test_cases
]
```

**Production Monitoring:**
```python
score = evaluator.evaluate({...})
if score.score < threshold:
    logger.warning(f"Low quality: {score.score}")
```

---

## Summary

Custom Evals makes it easy to evaluate **ANY** LLM application:

✅ **Works with ALL frameworks** - OpenAI, Anthropic, LangChain, LlamaIndex, custom
✅ **Simple 4-step pattern** - Initialize, Run, Evaluate, Check
✅ **Multiple evaluators** - 9 evaluators for different quality aspects
✅ **Production ready** - Real-time monitoring and alerting
✅ **Batch testing** - Test multiple cases simultaneously
✅ **Optional tracing** - Phoenix integration for observability

**Get Started:**

1. Install: `pip install -e .`
2. Choose evaluator for your use case
3. Wrap your LLM application with evaluation
4. Monitor quality in production

**Next Steps:**
- See [Agents Integration](agents-integration.md) for agent projects
- See [RAG Integration](rag-integration.md) for RAG applications
- See [Getting Started](getting-started.md) for basic usage
- See [Examples](../examples/) for more code samples

---

Your LLM application now has production-grade quality monitoring! 🎉
