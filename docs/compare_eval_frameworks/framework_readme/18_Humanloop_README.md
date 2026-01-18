# Humanloop: The Complete Deep-Dive Guide

**Version**: 1.0.0 | **Updated**: January 2026 | **License**: Proprietary

---

## Table of Contents

1. [Introduction & Overview](#1-introduction--overview)
2. [Complete Architecture](#2-complete-architecture)
3. [Installation & Setup](#3-installation--setup)
4. [Core Concepts](#4-core-concepts)
5. [Complete Examples Section](#5-complete-examples-section)
6. [Advanced Usage](#6-advanced-usage)
7. [Best Practices](#7-best-practices)
8. [Integration Guide](#8-integration-guide)
9. [Troubleshooting](#9-troubleshooting)
10. [API Reference](#10-api-reference)
11. [Performance & Optimization](#11-performance--optimization)
12. [Security Considerations](#12-security-considerations)
13. [References & Resources](#13-references--resources)

---

## 1. Introduction & Overview

### 1.1 What is Humanloop?

Humanloop is the human-in-the-loop platform for LLM applications. Unlike purely automated evaluation tools, Humanloop recognizes that human judgment is essential for building production-quality AI. It combines powerful prompt engineering tools, human feedback collection, and collaborative workflows to help teams ship better AI products faster.

**Core Philosophy:**
- **Human-in-the-Loop**: Combine automated metrics with human expertise
- **Collaborative**: Built for cross-functional teams (engineers, product, domain experts)
- **Production-First**: From prompt playground to production monitoring
- **Feedback-Driven**: Continuous improvement through user and expert feedback

### 1.2 Key Features

#### Prompt Management
- **Visual Editor**: Build prompts with intuitive UI
- **Version Control**: Git-like versioning for all prompts
- **A/B Testing**: Run experiments with automatic user assignment
- **Template Variables**: Dynamic prompts with type safety
- **Multi-Model**: Deploy same prompt across GPT-4, Claude, Gemini

#### Human Feedback Platform
- **In-App Feedback**: Embed feedback widgets in your application
- **Annotation Interface**: Label and rate generations
- **Expert Review**: Subject matter experts review outputs
- **Feedback Analytics**: Aggregate and analyze feedback trends
- **Active Learning**: Prioritize examples for review

#### Collaborative Workflows
- **Team Prompts**: Share and iterate on prompts
- **Comments & Reviews**: Discuss changes before deployment
- **Role-Based Access**: Engineers, reviewers, admins
- **Approval Workflows**: Require sign-off before production

#### Evaluation & Testing
- **Human Evaluations**: Distributed evaluation tasks
- **Automated Metrics**: Standard and custom scorers
- **Comparison Mode**: Side-by-side prompt comparison
- **Regression Testing**: Catch regressions automatically

#### Production Features
- **Logging & Monitoring**: Stream production traces
- **Cost Tracking**: Per-user, per-feature cost analytics
- **Performance Monitoring**: Latency, error rates, throughput
- **User Segmentation**: Analyze by cohorts

### 1.3 When to Use Humanloop

**Perfect For:**
- Products requiring high-quality outputs (customer-facing)
- Teams needing cross-functional collaboration
- Applications where human feedback is essential
- Domain-specific use cases requiring expert review
- Companies wanting prompt management + monitoring
- Regulated industries requiring human oversight

**Not Ideal For:**
- Pure research projects (use Weave or W&B)
- Small scripts or prototypes (overhead too high)
- Teams only wanting automated evaluation
- Budget-conscious startups (pricing can be steep)

### 1.4 Comparison Matrix

| Feature | Humanloop | LangSmith | Braintrust | Langfuse | Phoenix |
|---------|-----------|-----------|------------|----------|---------|
| **Human Feedback UI** | ✅✅ Best | ⚠️ Basic | ⚠️ Basic | ⚠️ Basic | ❌ No |
| **Prompt Playground** | ✅✅ Excellent | ✅ Good | ✅ Good | ⚠️ Basic | ❌ No |
| **Collaboration** | ✅✅ Core Feature | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | ❌ No |
| **Expert Review** | ✅✅ Built-in | ❌ No | ❌ No | ❌ No | ❌ No |
| **Annotation Tools** | ✅✅ Advanced | ⚠️ Basic | ⚠️ Basic | ⚠️ Basic | ❌ No |
| **A/B Testing** | ✅ Built-in | ✅ Built-in | ✅ Built-in | ⚠️ Manual | ❌ No |
| **Production Monitoring** | ✅ Yes | ✅✅ Excellent | ✅ Yes | ✅✅ Excellent | ✅✅ Excellent |
| **Self-Hosting** | ❌ No | ❌ No | ⚠️ Enterprise | ✅ Yes | ✅ Yes |
| **Pricing** | $$$ High | $$ Medium | $ Low | $ Low | Free |
| **Developer UX** | ✅ Good | ✅ Good | ✅✅ Excellent | ✅ Good | ⚠️ Basic |

---

## 2. Complete Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Your Application                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Humanloop SDK Integration                             │ │
│  │  - hl.prompts.call() for managed prompts               │ │
│  │  - hl.log() for production logging                     │ │
│  │  - hl.feedback() for user feedback                     │ │
│  └──────────────┬─────────────────────────────────────────┘ │
└─────────────────┼──────────────────────────────────────────┘
                  │ HTTPS API
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Humanloop Platform (Cloud)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Prompt      │  │  Feedback    │  │  Logging     │      │
│  │  Registry    │  │  Pipeline    │  │  Pipeline    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                           │                                  │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │  Analytics & Aggregation Engine                        │ │
│  │  - Aggregate feedback by prompt version                │ │
│  │  - Compute evaluation metrics                          │ │
│  │  - Detect anomalies and regressions                    │ │
│  └────────────────────────┬───────────────────────────────┘ │
│                           │                                  │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │  Web UI (React)                                        │ │
│  │  - Prompt editor                                       │ │
│  │  - Feedback dashboard                                  │ │
│  │  - Annotation interface                                │ │
│  │  - Team collaboration                                  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Human Feedback Loop

```
1. User Interaction
   ├── User submits query
   └── App calls Humanloop prompt

2. Generation
   ├── Humanloop routes to configured model
   ├── Logs input/output
   └── Returns response to user

3. Feedback Collection
   ├── User provides thumbs up/down
   ├── Optional: detailed rating (1-5)
   └── Optional: text comment

4. Feedback Storage
   ├── Linked to generation log
   ├── Tagged with prompt version
   └── Associated with user cohort

5. Analysis
   ├── Aggregate metrics by version
   ├── Identify patterns in negative feedback
   └── Surface examples for expert review

6. Expert Review (Optional)
   ├── Review flagged examples
   ├── Provide structured annotations
   └── Approve/reject prompt versions

7. Iteration
   ├── Create new prompt version
   ├── A/B test against current version
   └── Promote winner to production
```

### 2.3 Prompt Lifecycle

```
Development
├── Create prompt in editor
├── Test with sample inputs
└── Iterate based on results

Testing
├── Create evaluation dataset
├── Run bulk evaluation
└── Review results

Staging
├── Deploy to staging environment
├── A/B test with small % of traffic
└── Collect feedback

Production
├── Promote to 100% traffic
├── Monitor performance
└── Collect user feedback

Monitoring
├── Track metrics over time
├── Detect regressions
└── Plan next iteration

Improvement
└── Analyze feedback → back to Development
```

---

## 3. Installation & Setup

### 3.1 Installation

```bash
# Python
pip install humanloop

# Node.js
npm install humanloop

# TypeScript
npm install humanloop
npm install --save-dev @types/humanloop

# Verify
python -c "import humanloop; print(humanloop.__version__)"
```

### 3.2 Quick Start (Python)

```python
import os
from humanloop import Humanloop

# Initialize (get API key from https://app.humanloop.com)
hl = Humanloop(api_key=os.environ.get("HUMANLOOP_API_KEY"))

# Call a managed prompt
response = hl.prompts.call(
    project="my-project",
    prompt="customer-support-v1",
    inputs={
        "customer_name": "Alice",
        "question": "How do I reset my password?"
    }
)

print(f"Response: {response.data[0].output}")
print(f"Log ID: {response.data[0].id}")

# Add user feedback
hl.feedback(
    log_id=response.data[0].id,
    rating="good",  # or "bad"
    comment="Very helpful response!"
)
```

### 3.3 Quick Start (TypeScript)

```typescript
import { Humanloop } from "humanloop";

const hl = new Humanloop({
  apiKey: process.env.HUMANLOOP_API_KEY,
});

// Call prompt
const response = await hl.prompts.call({
  project: "my-project",
  prompt: "customer-support-v1",
  inputs: {
    customer_name: "Alice",
    question: "How do I reset my password?",
  },
});

console.log(`Response: ${response.data[0].output}`);

// Add feedback
await hl.feedback({
  logId: response.data[0].id,
  rating: "good",
  comment: "Helpful!",
});
```

### 3.4 Web Dashboard Setup

1. Sign up at https://app.humanloop.com
2. Create a project
3. Create a prompt in the editor
4. Configure model and parameters
5. Test with sample inputs
6. Deploy and get prompt ID
7. Use prompt ID in your application

---

## 4. Core Concepts

### 4.1 Projects

Projects are top-level containers for prompts, logs, and datasets.

```python
from humanloop import Humanloop

hl = Humanloop(api_key="...")

# Projects are created via UI
# Use project name in API calls

hl.prompts.call(
    project="customer-support",  # Project name
    prompt="greeting-v1",
    inputs={...}
)
```

### 4.2 Prompts

Prompts are versioned templates managed in Humanloop.

```python
# Prompts are created in the UI with:
# - Template text with {{variables}}
# - Model selection (GPT-4, Claude, etc.)
# - Parameters (temperature, max_tokens)
# - System message
# - Few-shot examples

# Call from code
response = hl.prompts.call(
    project="my-project",
    prompt="prompt-name",
    inputs={"variable1": "value1"},

    # Optional overrides
    model="gpt-4-turbo-preview",
    temperature=0.8
)

# Humanloop handles:
# - Template rendering
# - API calls to LLM
# - Logging
# - Version tracking
```

### 4.3 Logs

Every generation is automatically logged.

```python
# Automatic logging
response = hl.prompts.call(...)

# Log has:
log_id = response.data[0].id  # Unique ID
log_output = response.data[0].output  # Model output
log_metadata = response.data[0].metadata  # Custom metadata

# Query logs via API or UI
logs = hl.logs.list(
    project="my-project",
    prompt="prompt-name"
)
```

### 4.4 Feedback

Feedback connects user ratings to specific generations.

```python
# Simple thumbs up/down
hl.feedback(
    log_id=log_id,
    rating="good"  # or "bad"
)

# Detailed rating
hl.feedback(
    log_id=log_id,
    rating=4,  # 1-5 scale
    comment="Accurate but could be more concise"
)

# Custom feedback
hl.feedback(
    log_id=log_id,
    rating="good",
    metadata={
        "correctness": True,
        "helpful": True,
        "clarity": 4,
        "user_segment": "premium"
    }
)
```

### 4.5 Evaluations

Evaluations run prompts against test datasets.

```python
# Create evaluation dataset in UI
# Then run evaluation

evaluation = hl.evaluations.create(
    project="my-project",
    prompt="prompt-v2",
    dataset="eval-set-v1",

    # Optional: custom evaluators
    evaluators=["accuracy", "helpfulness"]
)

# View results in UI or fetch via API
results = hl.evaluations.get(evaluation_id=evaluation.id)

print(f"Accuracy: {results.metrics['accuracy']}")
print(f"Helpfulness: {results.metrics['helpfulness']}")
```

---

## 5. Complete Examples Section

### Example 1: Basic Prompt Management

**Use Case**: Manage a customer support prompt with versioning

```python
import os
from humanloop import Humanloop

# Initialize
hl = Humanloop(api_key=os.environ.get("HUMANLOOP_API_KEY"))

# Step 1: Create prompt in Humanloop UI
# Project: "support-bot"
# Prompt: "answer-question"
# Template:
"""
You are a helpful customer support agent for {{company_name}}.

Customer Question: {{question}}

Provide a clear, helpful answer.
"""

# Step 2: Call prompt from application
def answer_customer_question(question: str, customer_name: str) -> dict:
    """Answer customer question using managed prompt"""

    response = hl.prompts.call(
        project="support-bot",
        prompt="answer-question",
        inputs={
            "company_name": "Acme Corp",
            "question": question
        },
        metadata={
            "customer_name": customer_name,
            "channel": "web"
        }
    )

    return {
        "answer": response.data[0].output,
        "log_id": response.data[0].id
    }

# Step 3: Collect user feedback
def submit_feedback(log_id: str, helpful: bool, comment: str = None):
    """Submit user feedback"""

    hl.feedback(
        log_id=log_id,
        rating="good" if helpful else "bad",
        comment=comment
    )

if __name__ == "__main__":
    # Example usage
    result = answer_customer_question(
        question="How do I reset my password?",
        customer_name="Alice"
    )

    print(f"Answer: {result['answer']}")

    # Simulate user feedback
    submit_feedback(
        log_id=result["log_id"],
        helpful=True,
        comment="Very clear instructions!"
    )

    print("✅ View feedback in Humanloop dashboard")

# In Humanloop UI:
# - View all generations
# - See feedback rate (% thumbs up)
# - Read user comments
# - Identify problematic queries
# - Iterate on prompt based on feedback
```

**Humanloop Dashboard View:**
```
Prompt: answer-question (v3)
Feedback Rate: 87% positive (152/175)

Recent Feedback:
├── ✅ "Very clear instructions!" (Alice)
├── ❌ "Too technical" (Bob)
├── ✅ "Helpful!" (Charlie)
└── ✅ "Perfect" (Diana)

Insights:
- 13% negative feedback mentions "too technical"
- Recommendation: Simplify language
```

### Example 2: A/B Testing Prompts

**Use Case**: Test two prompt versions with real users

```python
import os
from humanloop import Humanloop
import random

hl = Humanloop(api_key=os.environ.get("HUMANLOOP_API_KEY"))

# Create two prompt versions in Humanloop UI:
# Prompt A: "answer-concise" - Short, direct answers
# Prompt B: "answer-detailed" - Comprehensive answers

def answer_with_ab_test(question: str, user_id: str) -> dict:
    """Answer question with A/B test"""

    # Assign user to variant (50/50 split)
    # In production: use Humanloop's built-in A/B testing
    variant = "A" if hash(user_id) % 2 == 0 else "B"

    prompt_name = "answer-concise" if variant == "A" else "answer-detailed"

    response = hl.prompts.call(
        project="support-bot",
        prompt=prompt_name,
        inputs={"question": question},
        metadata={
            "user_id": user_id,
            "variant": variant,
            "experiment": "concise_vs_detailed"
        }
    )

    return {
        "answer": response.data[0].output,
        "log_id": response.data[0].id,
        "variant": variant
    }

def submit_feedback(log_id: str, rating: int, variant: str):
    """Submit feedback with variant info"""

    hl.feedback(
        log_id=log_id,
        rating=rating,  # 1-5
        metadata={"variant": variant}
    )

if __name__ == "__main__":
    # Simulate A/B test with multiple users
    questions = [
        "How do I reset my password?",
        "What are your business hours?",
        "How do I track my order?",
        "Do you ship internationally?"
    ]

    for i, question in enumerate(questions):
        user_id = f"user-{i}"

        print(f"\n--- User {user_id} ---")
        print(f"Question: {question}")

        result = answer_with_ab_test(question, user_id)

        print(f"Variant: {result['variant']}")
        print(f"Answer: {result['answer'][:100]}...")

        # Simulate feedback (variant A gets slightly better ratings)
        if result["variant"] == "A":
            rating = random.choice([4, 4, 5, 5, 5])  # Avg 4.6
        else:
            rating = random.choice([3, 4, 4, 4, 5])  # Avg 4.0

        submit_feedback(result["log_id"], rating, result["variant"])

        print(f"User rating: {rating}/5")

    print("\n✅ View A/B test results in Humanloop")
    print("Compare: feedback rates, ratings, comments")

# Humanloop A/B Test Results:
# Experiment: concise_vs_detailed
#
#                  │ Variant A │ Variant B │ Difference │
# ─────────────────┼───────────┼───────────┼────────────┤
# Avg Rating       │ 4.6       │ 4.0       │ +0.6 ✅    │
# Positive Rate    │ 92%       │ 78%       │ +14% ✅    │
# Samples          │ 523       │ 512       │            │
#
# Statistical Significance: p < 0.01 ✅
#
# Winner: Variant A (concise)
# Action: Promote to 100% traffic
```

### Example 3: Expert Review Workflow

**Use Case**: Route generations to domain experts for review

```python
import os
from humanloop import Humanloop

hl = Humanloop(api_key=os.environ.get("HUMANLOOP_API_KEY"))

# Medical chatbot requiring expert review
def answer_medical_question(question: str, patient_id: str) -> dict:
    """Answer medical question"""

    response = hl.prompts.call(
        project="medical-assistant",
        prompt="medical-qa-v1",
        inputs={
            "question": question,
            "disclaimer": "This is not medical advice. Consult a doctor."
        },
        metadata={
            "patient_id": patient_id,
            "requires_review": True,  # Flag for expert review
            "category": "medical",
            "urgency": "normal"
        }
    )

    log_id = response.data[0].id

    # Create review task (via Humanloop UI or API)
    hl.reviews.create(
        log_id=log_id,
        reviewers=["dr.smith@hospital.com"],
        instructions="Review medical accuracy and safety",
        required_fields=["accurate", "safe", "appropriate"]
    )

    return {
        "answer": response.data[0].output,
        "log_id": log_id,
        "status": "pending_review"
    }

# Expert reviews in Humanloop UI:
# 1. Reviewer sees generation
# 2. Rates on custom dimensions
# 3. Provides feedback/corrections
# 4. Approves or rejects

def check_review_status(log_id: str) -> dict:
    """Check if expert has reviewed"""

    review = hl.reviews.get(log_id=log_id)

    return {
        "reviewed": review.completed,
        "approved": review.approved if review.completed else None,
        "feedback": review.feedback if review.completed else None
    }

if __name__ == "__main__":
    # Patient asks question
    result = answer_medical_question(
        question="What are the symptoms of diabetes?",
        patient_id="patient-123"
    )

    print(f"Answer: {result['answer'][:100]}...")
    print(f"Status: {result['status']}")

    # Later: Check review status
    status = check_review_status(result["log_id"])

    if status["reviewed"]:
        print(f"\n✅ Expert review completed")
        print(f"Approved: {status['approved']}")
        print(f"Feedback: {status['feedback']}")
    else:
        print(f"\n⏳ Awaiting expert review")

# Humanloop Expert Review Interface:
# ┌─────────────────────────────────────────────┐
# │ Review: Medical Q&A Generation              │
# ├─────────────────────────────────────────────┤
# │ Question: What are symptoms of diabetes?    │
# │                                             │
# │ Generated Answer:                           │
# │ "Common symptoms include increased thirst..."│
# │                                             │
# │ Rate this response:                         │
# │ ☐ Medically Accurate                        │
# │ ☐ Safe                                      │
# │ ☐ Appropriate Language                      │
# │                                             │
# │ Feedback: ____________________________      │
# │                                             │
# │ [Approve] [Request Changes] [Reject]        │
# └─────────────────────────────────────────────┘
```

### Example 4: Custom Feedback UI in Your App

**Use Case**: Embed feedback collection directly in your application

```python
import os
from humanloop import Humanloop
from flask import Flask, request, jsonify

hl = Humanloop(api_key=os.environ.get("HUMANLOOP_API_KEY"))
app = Flask(__name__)

@app.route("/api/chat", methods=["POST"])
def chat():
    """Chat endpoint with feedback"""

    data = request.json
    question = data.get("question")
    user_id = data.get("user_id")

    # Generate response
    response = hl.prompts.call(
        project="chatbot",
        prompt="chat-v1",
        inputs={"question": question},
        metadata={"user_id": user_id}
    )

    answer = response.data[0].output
    log_id = response.data[0].id

    return jsonify({
        "answer": answer,
        "log_id": log_id  # Return to client for feedback
    })

@app.route("/api/feedback", methods=["POST"])
def feedback():
    """Feedback endpoint"""

    data = request.json
    log_id = data.get("log_id")
    rating = data.get("rating")  # "good" or "bad"
    comment = data.get("comment", "")

    # Submit to Humanloop
    hl.feedback(
        log_id=log_id,
        rating=rating,
        comment=comment
    )

    return jsonify({"success": True})

# Frontend (React example):
"""
import React, { useState } from 'react';

function Chat() {
  const [answer, setAnswer] = useState("");
  const [logId, setLogId] = useState(null);

  const askQuestion = async (question) => {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question, user_id: "user-123"})
    });

    const data = await response.json();
    setAnswer(data.answer);
    setLogId(data.log_id);
  };

  const submitFeedback = async (rating) => {
    await fetch("/api/feedback", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        log_id: logId,
        rating: rating
      })
    });

    alert("Thanks for your feedback!");
  };

  return (
    <div>
      <div>{answer}</div>

      {logId && (
        <div className="feedback">
          <button onClick={() => submitFeedback("good")}>
            👍 Helpful
          </button>
          <button onClick={() => submitFeedback("bad")}>
            👎 Not Helpful
          </button>
        </div>
      )}
    </div>
  );
}
"""

if __name__ == "__main__":
    app.run(port=5000)

# Humanloop collects all feedback
# View aggregated metrics in dashboard
```

### Example 5: Bulk Evaluation with Human Judges

**Use Case**: Evaluate prompt on dataset with human annotation

```python
import os
from humanloop import Humanloop

hl = Humanloop(api_key=os.environ.get("HUMANLOOP_API_KEY"))

# Step 1: Create evaluation dataset in Humanloop UI
# Dataset: "customer-support-eval"
# Examples:
# - Input: "How do I reset password?"
#   Expected: "You can reset your password by..."
# - Input: "What are shipping costs?"
#   Expected: "Shipping costs vary by location..."

# Step 2: Run evaluation
def run_evaluation(prompt_name: str, dataset_name: str) -> str:
    """Run evaluation on dataset"""

    evaluation = hl.evaluations.create(
        project="support-bot",
        prompt=prompt_name,
        dataset=dataset_name,

        # Automatic evaluators
        evaluators=["exact_match", "semantic_similarity"],

        # Human evaluation
        human_evaluation=True,
        reviewers=["reviewer1@company.com", "reviewer2@company.com"],
        review_instructions="""
        Rate each response on:
        1. Accuracy (correct information)
        2. Helpfulness (addresses question)
        3. Tone (professional and friendly)

        Use scale: 1 (poor) to 5 (excellent)
        """
    )

    return evaluation.id

# Step 3: Reviewers see evaluation tasks in Humanloop UI
# They rate each generation individually

# Step 4: View aggregated results
def get_evaluation_results(evaluation_id: str) -> dict:
    """Get evaluation results"""

    results = hl.evaluations.get(evaluation_id=evaluation_id)

    return {
        "automated_metrics": {
            "exact_match": results.metrics["exact_match"],
            "semantic_similarity": results.metrics["semantic_similarity"]
        },
        "human_ratings": {
            "accuracy": results.human_metrics["accuracy"],
            "helpfulness": results.human_metrics["helpfulness"],
            "tone": results.human_metrics["tone"],
            "avg_score": results.human_metrics["average"]
        },
        "inter_rater_agreement": results.inter_rater_reliability
    }

if __name__ == "__main__":
    # Run evaluation
    print("Running evaluation...")
    eval_id = run_evaluation(
        prompt_name="answer-question-v2",
        dataset_name="customer-support-eval"
    )

    print(f"Evaluation created: {eval_id}")
    print("Waiting for human reviewers...")

    # In real scenario: poll or use webhooks
    # For demo, assume completed

    print("\n✅ View evaluation progress in Humanloop")
    print("Human reviewers rate each example")

# Humanloop Evaluation Results:
# ┌────────────────────────────────────────────┐
# │ Evaluation: answer-question-v2             │
# ├────────────────────────────────────────────┤
# │ Dataset: customer-support-eval (50 items)  │
# │ Reviewers: 2                               │
# │                                            │
# │ Automated Metrics:                         │
# │ ├── Exact Match: 0.34                      │
# │ └── Semantic Similarity: 0.78              │
# │                                            │
# │ Human Ratings:                             │
# │ ├── Accuracy: 4.2 / 5                      │
# │ ├── Helpfulness: 4.5 / 5                   │
# │ ├── Tone: 4.7 / 5                          │
# │ └── Average: 4.5 / 5 ✅                    │
# │                                            │
# │ Inter-Rater Agreement: 0.82 (Good)         │
# │                                            │
# │ Top Issues:                                │
# │ ├── 3 examples: too brief                  │
# │ └── 2 examples: missing key info           │
# └────────────────────────────────────────────┘
```

### Example 6: Multi-Model Deployment

**Use Case**: Deploy same prompt across multiple models

```python
import os
from humanloop import Humanloop

hl = Humanloop(api_key=os.environ.get("HUMANLOOP_API_KEY"))

# Create prompt versions in Humanloop UI with different models:
# - customer-support-gpt4: GPT-4 Turbo
# - customer-support-claude: Claude 3 Sonnet
# - customer-support-gpt35: GPT-3.5 Turbo (fallback)

def answer_with_fallback(question: str, user_id: str) -> dict:
    """Answer with automatic fallback"""

    # Try primary model (GPT-4)
    try:
        response = hl.prompts.call(
            project="support-bot",
            prompt="customer-support-gpt4",
            inputs={"question": question},
            metadata={"user_id": user_id},
            timeout=5  # 5 second timeout
        )

        return {
            "answer": response.data[0].output,
            "model": "gpt-4-turbo",
            "fallback": False
        }

    except Exception as e:
        print(f"Primary model failed: {e}")

        # Fallback to Claude
        try:
            response = hl.prompts.call(
                project="support-bot",
                prompt="customer-support-claude",
                inputs={"question": question},
                metadata={"user_id": user_id, "fallback": "claude"}
            )

            return {
                "answer": response.data[0].output,
                "model": "claude-3-sonnet",
                "fallback": True
            }

        except Exception as e:
            print(f"Secondary model failed: {e}")

            # Final fallback to GPT-3.5
            response = hl.prompts.call(
                project="support-bot",
                prompt="customer-support-gpt35",
                inputs={"question": question},
                metadata={"user_id": user_id, "fallback": "gpt-3.5"}
            )

            return {
                "answer": response.data[0].output,
                "model": "gpt-3.5-turbo",
                "fallback": True
            }

def route_by_user_tier(question: str, user_tier: str) -> dict:
    """Route to model based on user tier"""

    model_routing = {
        "enterprise": "customer-support-gpt4",
        "pro": "customer-support-claude",
        "free": "customer-support-gpt35"
    }

    prompt = model_routing.get(user_tier, "customer-support-gpt35")

    response = hl.prompts.call(
        project="support-bot",
        prompt=prompt,
        inputs={"question": question},
        metadata={"user_tier": user_tier}
    )

    return {
        "answer": response.data[0].output,
        "model_used": prompt
    }

if __name__ == "__main__":
    # Test fallback
    print("=== Testing Fallback ===")
    result = answer_with_fallback(
        question="How do I reset my password?",
        user_id="user-123"
    )
    print(f"Model: {result['model']}")
    print(f"Fallback: {result['fallback']}")
    print(f"Answer: {result['answer'][:100]}...")

    # Test tier-based routing
    print("\n=== Testing Tier-Based Routing ===")
    tiers = ["enterprise", "pro", "free"]

    for tier in tiers:
        result = route_by_user_tier(
            question="What are your business hours?",
            user_tier=tier
        )
        print(f"\n{tier.title()} User:")
        print(f"Model: {result['model_used']}")
        print(f"Answer: {result['answer'][:100]}...")

    print("\n✅ View model usage in Humanloop dashboard")
    print("Compare: costs, latency, feedback by model")

# Humanloop Model Comparison Dashboard:
# ┌──────────────────┬──────────┬─────────┬──────────┬─────────┐
# │ Model            │ Requests │ Avg Cost│ Avg Time │ Feedback│
# ├──────────────────┼──────────┼─────────┼──────────┼─────────┤
# │ gpt-4-turbo      │ 1,234    │ $0.012  │ 1.8s     │ 92% ✅  │
# │ claude-3-sonnet  │ 856      │ $0.008  │ 1.5s     │ 88% ✅  │
# │ gpt-3.5-turbo    │ 3,421    │ $0.002  │ 0.9s     │ 78%     │
# └──────────────────┴──────────┴─────────┴──────────┴─────────┘
```

### Example 7: Active Learning Loop

**Use Case**: Automatically identify examples needing review

```python
import os
from humanloop import Humanloop

hl = Humanloop(api_key=os.environ.get("HUMANLOOP_API_KEY"))

def detect_low_confidence(log_id: str, output: str, metadata: dict) -> bool:
    """Detect if generation needs human review"""

    # Criteria for review:
    # 1. Model confidence is low
    # 2. Output is very short or very long
    # 3. Contains uncertainty phrases

    confidence = metadata.get("confidence", 1.0)
    length = len(output.split())

    uncertainty_phrases = [
        "i'm not sure",
        "i don't know",
        "might be",
        "possibly",
        "unclear"
    ]

    has_uncertainty = any(
        phrase in output.lower()
        for phrase in uncertainty_phrases
    )

    needs_review = (
        confidence < 0.7 or
        length < 10 or
        length > 200 or
        has_uncertainty
    )

    if needs_review:
        # Flag for human review
        hl.reviews.create(
            log_id=log_id,
            reason="low_confidence",
            priority="medium",
            reviewers=["expert@company.com"]
        )

    return needs_review

def answer_with_confidence_check(question: str) -> dict:
    """Answer with automatic confidence checking"""

    response = hl.prompts.call(
        project="qa-system",
        prompt="qa-v1",
        inputs={"question": question}
    )

    log_id = response.data[0].id
    output = response.data[0].output
    metadata = response.data[0].metadata

    # Check if needs review
    needs_review = detect_low_confidence(log_id, output, metadata)

    return {
        "answer": output,
        "needs_review": needs_review,
        "log_id": log_id
    }

# Batch processing: identify problematic examples
def review_recent_logs(hours: int = 24):
    """Review recent logs and flag for expert review"""

    # Get recent logs
    logs = hl.logs.list(
        project="qa-system",
        hours=hours,
        has_feedback=False  # No feedback yet
    )

    flagged_count = 0

    for log in logs:
        needs_review = detect_low_confidence(
            log.id,
            log.output,
            log.metadata
        )

        if needs_review:
            flagged_count += 1

    print(f"Flagged {flagged_count} logs for review")

if __name__ == "__main__":
    # Test individual question
    result = answer_with_confidence_check(
        question="What is the capital of Mars?"  # Tricky question
    )

    print(f"Answer: {result['answer']}")
    print(f"Needs Review: {result['needs_review']}")

    if result["needs_review"]:
        print("⚠️ Flagged for expert review")

    # Batch review
    print("\n=== Reviewing Recent Logs ===")
    review_recent_logs(hours=24)

    print("\n✅ View flagged examples in Humanloop")
    print("Experts can review and provide corrections")

# Humanloop Active Learning Dashboard:
# ┌────────────────────────────────────────────┐
# │ Flagged for Review (Last 24h)              │
# ├────────────────────────────────────────────┤
# │ Total Flagged: 23                          │
# │                                            │
# │ By Reason:                                 │
# │ ├── Low Confidence: 12                     │
# │ ├── Uncertainty: 7                         │
# │ ├── Length Issues: 4                       │
# │                                            │
# │ Priority Distribution:                     │
# │ ├── High: 3 ⚠️                             │
# │ ├── Medium: 15                             │
# │ └── Low: 5                                 │
# │                                            │
# │ Pending Reviews: 18                        │
# │ Completed: 5                               │
# └────────────────────────────────────────────┘
```

### Example 8: Cost Optimization by User Cohort

**Use Case**: Track and optimize costs per user segment

```python
import os
from humanloop import Humanloop

hl = Humanloop(api_key=os.environ.get("HUMANLOOP_API_KEY"))

def answer_with_cost_tracking(
    question: str,
    user_id: str,
    user_tier: str,
    user_region: str
) -> dict:
    """Answer with detailed cost tracking"""

    response = hl.prompts.call(
        project="chatbot",
        prompt="chat-v1",
        inputs={"question": question},
        metadata={
            "user_id": user_id,
            "user_tier": user_tier,
            "user_region": user_region,
            "timestamp": datetime.now().isoformat()
        }
    )

    # Humanloop automatically tracks costs
    # Associated with metadata for segmentation

    return {
        "answer": response.data[0].output,
        "cost": response.data[0].cost,  # Estimated cost
        "log_id": response.data[0].id
    }

# Query cost analytics via Humanloop API
def get_cost_by_cohort(days: int = 30) -> dict:
    """Get cost breakdown by user cohorts"""

    # Query Humanloop analytics API
    analytics = hl.analytics.costs(
        project="chatbot",
        days=days,
        group_by=["user_tier", "user_region"]
    )

    return analytics

if __name__ == "__main__":
    # Example: Track costs for different users
    users = [
        {"id": "user-1", "tier": "enterprise", "region": "us"},
        {"id": "user-2", "tier": "pro", "region": "eu"},
        {"id": "user-3", "tier": "free", "region": "asia"},
    ]

    for user in users:
        result = answer_with_cost_tracking(
            question="Tell me about your product",
            user_id=user["id"],
            user_tier=user["tier"],
            user_region=user["region"]
        )

        print(f"\n{user['tier'].title()} User ({user['region'].upper()}):")
        print(f"Cost: ${result['cost']:.6f}")
        print(f"Answer: {result['answer'][:100]}...")

    # View cost analytics
    print("\n=== Cost Analytics ===")
    print("✅ View detailed cost breakdown in Humanloop")

# Humanloop Cost Analytics Dashboard:
# ┌────────────────────────────────────────────┐
# │ Cost Breakdown (Last 30 Days)              │
# ├────────────────────────────────────────────┤
# │ Total Spent: $1,234.56                     │
# │                                            │
# │ By User Tier:                              │
# │ ├── Enterprise: $678.90 (55%)              │
# │ ├── Pro: $432.10 (35%)                     │
# │ └── Free: $123.56 (10%)                    │
# │                                            │
# │ By Region:                                 │
# │ ├── US: $567.89 (46%)                      │
# │ ├── EU: $445.67 (36%)                      │
# │ └── Asia: $221.00 (18%)                    │
# │                                            │
# │ Cost per User:                             │
# │ ├── Enterprise: $12.34                     │
# │ ├── Pro: $4.56                             │
# │ └── Free: $0.89                            │
# │                                            │
# │ Trends:                                    │
# │ ├── Enterprise costs ↑ 15%                 │
# │ └── Free tier costs ↓ 5%                   │
# └────────────────────────────────────────────┘
```

### Example 9: Monitoring and Alerts

**Use Case**: Set up monitoring and get alerted on issues

```python
import os
from humanloop import Humanloop

hl = Humanloop(api_key=os.environ.get("HUMANLOOP_API_KEY"))

# Configure alerts in Humanloop UI:
# 1. Feedback rate drops below 80%
# 2. Error rate exceeds 5%
# 3. P95 latency > 3 seconds
# 4. Daily cost exceeds budget

# Monitor in code
def check_health_metrics() -> dict:
    """Check system health"""

    # Get metrics from Humanloop API
    metrics = hl.analytics.metrics(
        project="chatbot",
        hours=1  # Last hour
    )

    health = {
        "feedback_rate": metrics.feedback_rate,
        "error_rate": metrics.error_rate,
        "p95_latency": metrics.latency_p95,
        "requests_per_minute": metrics.rpm
    }

    # Check thresholds
    issues = []

    if health["feedback_rate"] < 0.8:
        issues.append("Low feedback rate")

    if health["error_rate"] > 0.05:
        issues.append("High error rate")

    if health["p95_latency"] > 3.0:
        issues.append("High latency")

    health["issues"] = issues
    health["healthy"] = len(issues) == 0

    return health

if __name__ == "__main__":
    health = check_health_metrics()

    print("=== System Health ===")
    print(f"Feedback Rate: {health['feedback_rate']:.1%}")
    print(f"Error Rate: {health['error_rate']:.1%}")
    print(f"P95 Latency: {health['p95_latency']:.2f}s")
    print(f"Requests/min: {health['requests_per_minute']}")

    if health["healthy"]:
        print("\n✅ All systems healthy")
    else:
        print(f"\n⚠️ Issues detected:")
        for issue in health["issues"]:
            print(f"  - {issue}")

# Humanloop sends alerts via:
# - Email
# - Slack
# - Webhook
# - PagerDuty (enterprise)
```

### Example 10: Compliance and Audit Trail

**Use Case**: Maintain audit trail for regulated industries

```python
import os
from humanloop import Humanloop
from datetime import datetime

hl = Humanloop(api_key=os.environ.get("HUMANLOOP_API_KEY"))

def compliant_generation(
    question: str,
    user_id: str,
    operator_id: str,
    purpose: str
) -> dict:
    """Generate with full audit trail"""

    response = hl.prompts.call(
        project="regulated-assistant",
        prompt="compliant-response-v1",
        inputs={"question": question},
        metadata={
            # User info
            "user_id": user_id,
            "user_consent": True,

            # Operator info
            "operator_id": operator_id,
            "operator_role": "agent",

            # Purpose
            "purpose": purpose,
            "data_classification": "confidential",

            # Audit fields
            "timestamp": datetime.now().isoformat(),
            "environment": "production",
            "compliance_version": "v2.1",
            "retention_days": 2555  # 7 years
        }
    )

    log_id = response.data[0].id

    # Log access
    hl.audit.log_access(
        log_id=log_id,
        accessor=operator_id,
        action="generate",
        justification=purpose
    )

    return {
        "answer": response.data[0].output,
        "log_id": log_id,
        "audit_trail": True
    }

def review_audit_trail(log_id: str) -> dict:
    """Get complete audit trail"""

    audit = hl.audit.get(log_id=log_id)

    return {
        "created_at": audit.created_at,
        "user_id": audit.metadata["user_id"],
        "operator_id": audit.metadata["operator_id"],
        "purpose": audit.metadata["purpose"],
        "accesses": audit.access_log,
        "modifications": audit.modification_log,
        "retention_until": audit.retention_until
    }

if __name__ == "__main__":
    # Example: Healthcare use case
    result = compliant_generation(
        question="What are treatment options for condition X?",
        user_id="patient-12345",
        operator_id="dr-smith",
        purpose="clinical_decision_support"
    )

    print(f"Answer: {result['answer'][:100]}...")
    print(f"Log ID: {result['log_id']}")

    # Retrieve audit trail
    print("\n=== Audit Trail ===")
    audit = review_audit_trail(result["log_id"])
    print(f"Created: {audit['created_at']}")
    print(f"User: {audit['user_id']}")
    print(f"Operator: {audit['operator_id']}")
    print(f"Purpose: {audit['purpose']}")
    print(f"Retention: {audit['retention_until']}")

    print("\n✅ Full audit trail maintained for compliance")

# Humanloop Compliance Features:
# - Complete audit logs
# - Data retention policies
# - Access controls
# - Encryption at rest
# - GDPR/HIPAA compliance tools
# - Export for regulators
```

---

## 6. Advanced Usage

### 6.1 Custom Feedback Schemas

```python
# Define custom feedback structure
hl.feedback_schema.create(
    project="my-project",
    schema={
        "rating": {"type": "number", "min": 1, "max": 5},
        "categories": {
            "type": "array",
            "items": ["accuracy", "helpfulness", "tone"]
        },
        "comment": {"type": "string", "optional": True}
    }
)
```

### 6.2 Webhooks

```python
# Configure webhook in UI to receive:
# - New feedback
# - Evaluation completion
# - Alert triggers

# Example webhook payload:
{
    "event": "feedback.created",
    "log_id": "log-123",
    "rating": "good",
    "project": "my-project"
}
```

### 6.3 Advanced Analytics

```python
# Query via API
analytics = hl.analytics.query(
    project="my-project",
    metric="feedback_rate",
    group_by=["prompt_version", "user_segment"],
    filters={"created_at": {"gte": "2026-01-01"}},
    aggregation="average"
)
```

---

## 7. Best Practices

### 7.1 Feedback Collection

```python
# DO: Make feedback easy and quick
# DO: Collect context (why helpful/not helpful)
# DO: Offer multiple feedback methods (thumbs, ratings, comments)

# DON'T: Interrupt user flow
# DON'T: Force feedback
# DON'T: Ignore negative feedback
```

### 7.2 Expert Reviews

```python
# DO: Provide clear review guidelines
# DO: Use structured rating dimensions
# DO: Track inter-rater agreement

# DON'T: Overload reviewers
# DON'T: Skip calibration sessions
```

### 7.3 Prompt Management

```python
# DO: Version every change
# DO: Add descriptions to versions
# DO: Test before production deployment

# DON'T: Edit production prompts directly
# DON'T: Skip A/B testing
```

---

## 8. Integration Guide

### 8.1 Frameworks

Humanloop works with any LLM framework:

```python
# Direct API calls (OpenAI, Anthropic, etc.)
# LangChain
# LlamaIndex
# Custom implementations
```

### 8.2 Frontend Integration

```javascript
// React example
import { HumanloopFeedback } from '@humanloop/react';

<HumanloopFeedback
  logId={logId}
  onSubmit={(feedback) => console.log(feedback)}
/>
```

---

## 9. Troubleshooting

### 9.1 Common Issues

**Prompts not updating:**
```python
# Check prompt version deployed
# Verify cache settings
# Clear prompt cache if needed
```

**Feedback not appearing:**
```python
# Verify log_id is correct
# Check API key permissions
# View logs in Humanloop UI
```

---

## 10. API Reference

### 10.1 Core Methods

```python
# Prompts
hl.prompts.call(project, prompt, inputs, metadata)
hl.prompts.get(project, prompt)
hl.prompts.list(project)

# Feedback
hl.feedback(log_id, rating, comment, metadata)

# Logs
hl.logs.list(project, filters)
hl.logs.get(log_id)

# Evaluations
hl.evaluations.create(project, prompt, dataset)
hl.evaluations.get(evaluation_id)

# Analytics
hl.analytics.metrics(project, hours)
hl.analytics.costs(project, days)
```

---

## 11. Performance & Optimization

### 11.1 Latency

- Prompt calls: ~100ms overhead
- Feedback submission: <50ms
- Async recommended for high throughput

### 11.2 Costs

- Track by project, prompt, user
- Set budgets and alerts
- Optimize via model selection

---

## 12. Security Considerations

### 12.1 Data Privacy

```python
# Redact PII before logging
# Use Humanloop's PII detection
# Configure retention policies
# Enable encryption
```

### 12.2 Access Control

- Role-based permissions
- SSO (enterprise)
- API key scoping
- Audit logs

---

## 13. References & Resources

### 13.1 Official Links

- Website: https://humanloop.com
- Documentation: https://humanloop.com/docs
- Blog: https://humanloop.com/blog
- Support: support@humanloop.com

### 13.2 Pricing

- Starter: Free (1k generations/month)
- Growth: $99/month (10k generations)
- Pro: $499/month (100k generations)
- Enterprise: Custom pricing

### 13.3 Comparison

**vs LangSmith:**
- Humanloop: Better human feedback tools
- LangSmith: Better LangChain integration

**vs Braintrust:**
- Humanloop: Human-in-the-loop focus
- Braintrust: Evaluation-first focus

**vs Langfuse:**
- Humanloop: Better collaboration features
- Langfuse: Better production monitoring

---

## Conclusion

Humanloop is the platform for teams that understand AI quality requires human judgment. Its combination of prompt management, human feedback collection, and collaborative workflows makes it ideal for customer-facing AI applications where quality is paramount. The platform shines when domain experts and end users are integral to your evaluation process.

**Key Strengths:**
- Best human feedback infrastructure
- Collaborative prompt management
- Expert review workflows
- Production monitoring
- Compliance features

**Best For:**
- Customer-facing AI products
- Domain-specific applications
- Teams with domain experts
- Regulated industries
- Quality-critical use cases

Build better AI with humans in the loop: https://humanloop.com
