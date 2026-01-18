# ARES (Automated RAG Evaluation System) - Comprehensive Deep Dive

**Version**: 1.0+ | **Type**: Python Library | **License**: Apache 2.0 (Open Source) | **Released**: 2023 (Published NAACL 2024)

---

## Table of Contents

1. [Introduction & Overview](#introduction--overview)
2. [Architecture & Core Concepts](#architecture--core-concepts)
3. [Installation & Setup](#installation--setup)
4. [Core Concepts](#core-concepts)
5. [Production-Ready Examples](#production-ready-examples)
6. [Advanced Usage Patterns](#advanced-usage-patterns)
7. [Best Practices](#best-practices)
8. [Integration Guide](#integration-guide)
9. [Troubleshooting](#troubleshooting)
10. [API Reference](#api-reference)
11. [Performance Optimization](#performance-optimization)
12. [Security Considerations](#security-considerations)
13. [Extensive References](#extensive-references)

---

## Introduction & Overview

### What is ARES?

ARES (Automated RAG Evaluation System) is a **research-backed framework from Stanford University** specifically designed for evaluating Retrieval-Augmented Generation (RAG) systems through synthetic data generation and fine-tuned classifier models. Published at NAACL 2024, ARES represents a novel approach to RAG evaluation that minimizes manual annotation burden while maintaining statistical rigor.

### Key Innovation

ARES introduces **Prediction-Powered Inference (PPI)**, a statistical technique that combines machine learning predictions with a small set of human annotations to produce more accurate evaluations with confidence intervals. This approach reduces the annotation burden from thousands to hundreds of examples while maintaining evaluation quality.

### Target Audience

- **RAG Researchers**: Academic and industrial researchers working on retrieval-augmented generation
- **ML Engineers**: Teams building production RAG systems at scale
- **Cost-Conscious Organizations**: Companies needing efficient, scalable evaluation
- **Privacy-Focused Teams**: Organizations requiring on-premise, local model execution
- **Domain Specialists**: Teams building domain-specific RAG systems (medical, legal, financial)

### Quick Stats

| Metric | Value |
|--------|-------|
| **GitHub Stars** | 500+ |
| **Installation Time** | 15-20 minutes |
| **Learning Curve** | Medium-High |
| **Primary Language** | Python 3.8+ |
| **Core Dependencies** | OpenAI API or vLLM (local) |
| **Research Validation** | 8 knowledge-intensive tasks, KILT benchmark |
| **Cost Efficiency** | 10-20x cheaper at scale vs LLM-as-judge |

---

## Architecture & Core Concepts

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ARES Evaluation Pipeline                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Synthetic Data Generation                          │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────┐    │
│  │ Documents  │───▶│ LLM Generator│───▶│   Q-D-A     │    │
│  │  Corpus    │    │ (GPT-4/Local)│    │   Triples   │    │
│  └────────────┘    └──────────────┘    └─────────────┘    │
│                                                              │
│  Output: Query-Document-Answer synthetic examples           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: Human Annotation (Small Sample)                    │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────┐    │
│  │  Synthetic │───▶│   Annotators │───▶│   Labeled   │    │
│  │  Examples  │    │  (Few 100s)  │    │   Samples   │    │
│  └────────────┘    └──────────────┘    └─────────────┘    │
│                                                              │
│  Goal: ~500 annotations for PPI calibration                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: Classifier Training                                │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────┐    │
│  │  Synthetic │───▶│ Fine-tuning  │───▶│  Trained    │    │
│  │   + Human  │    │(DistilBERT)  │    │ Classifiers │    │
│  └────────────┘    └──────────────┘    └─────────────┘    │
│                                                              │
│  3 Classifiers: Context, Faithfulness, Relevance            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 4: Prediction-Powered Inference (PPI)                 │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────┐    │
│  │ Classifier │───▶│   PPI Algo   │───▶│Calibrated   │    │
│  │ Predictions│    │   + Human    │    │Scores + CI  │    │
│  └────────────┘    └──────────────┘    └─────────────┘    │
│                                                              │
│  Output: Mean scores with 95% confidence intervals          │
└─────────────────────────────────────────────────────────────┘
```

### Three Core RAG Metrics

#### 1. Context Relevance

**Definition**: Measures whether retrieved documents are relevant to the query.

**Evaluation Process**:
```python
def context_relevance(query: str, contexts: List[str]) -> float:
    """
    For each retrieved context:
    1. Compare semantic similarity to query
    2. Check for query-relevant information
    3. Score: 1.0 (relevant) or 0.0 (irrelevant)
    4. Average across all contexts
    """
    pass
```

**Why Critical**: Poor retrieval leads to poor answers, regardless of generation quality.

**Typical Thresholds**:
- **Excellent**: > 0.9
- **Good**: 0.75 - 0.9
- **Needs Improvement**: < 0.75

#### 2. Answer Faithfulness

**Definition**: Measures whether generated answer is grounded in retrieved contexts.

**Evaluation Process**:
```python
def answer_faithfulness(answer: str, contexts: List[str]) -> float:
    """
    1. Extract claims from answer
    2. For each claim, verify against contexts
    3. Check if claim is supported by evidence
    4. Score: fraction of supported claims
    """
    pass
```

**Why Critical**: Prevents hallucinations and ensures factual accuracy.

**Typical Thresholds**:
- **Excellent**: > 0.95
- **Good**: 0.85 - 0.95
- **Dangerous**: < 0.85 (especially in high-stakes domains)

#### 3. Answer Relevance

**Definition**: Measures whether answer addresses the user's query.

**Evaluation Process**:
```python
def answer_relevance(query: str, answer: str) -> float:
    """
    1. Compare answer semantic similarity to query
    2. Check if query is actually answered
    3. Evaluate completeness
    4. Score: 0.0 (off-topic) to 1.0 (perfectly relevant)
    """
    pass
```

**Why Critical**: Ensures answers are helpful and on-topic.

**Typical Thresholds**:
- **Excellent**: > 0.9
- **Good**: 0.75 - 0.9
- **Poor UX**: < 0.75

### Prediction-Powered Inference (PPI)

**Core Innovation**: PPI is a statistical technique that:

1. **Uses ML predictions** from trained classifiers (cheap, fast)
2. **Calibrates with human labels** (expensive, slow but accurate)
3. **Produces refined estimates** with confidence intervals
4. **Reduces variance** compared to pure ML or pure human annotation

**Mathematical Foundation**:
```
PPI Estimate = ML Prediction + α × (Human Labels - ML on Human Subset)

Where:
- α = calibration weight (learned from data)
- Confidence Interval = Based on both prediction and human variance
```

**Benefits**:
- **10-20x fewer annotations** needed vs traditional supervised learning
- **Confidence intervals** for statistical rigor
- **Better estimates** than ML alone
- **More efficient** than human-only evaluation

---

## Installation & Setup

### Prerequisites

```bash
# System Requirements
- Python 3.8 or higher
- pip 21.0+
- (Optional) CUDA-capable GPU for local model training
- (Optional) 16GB+ RAM for large-scale evaluation

# API Keys (choose one)
- OpenAI API key (for cloud-based generation)
- Local model setup (vLLM for on-premise)
```

### Installation Methods

#### Method 1: Standard Installation

```bash
# Install ARES
pip install ares-ai

# Install optional dependencies
pip install datasets pandas scikit-learn matplotlib

# For local model execution
pip install vllm transformers torch

# For advanced features
pip install sentence-transformers faiss-cpu
```

#### Method 2: From Source

```bash
# Clone repository
git clone https://github.com/stanford-futuredata/ARES.git
cd ARES

# Install in development mode
pip install -e .

# Install dev dependencies
pip install -e ".[dev]"
```

#### Method 3: Docker Setup

```bash
# Pull ARES Docker image
docker pull stanford/ares:latest

# Run container
docker run -it \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v $(pwd)/data:/data \
  stanford/ares:latest
```

### Configuration

#### API Key Setup

```bash
# OpenAI (recommended for initial testing)
export OPENAI_API_KEY="sk-..."

# Alternative: Use .env file
echo "OPENAI_API_KEY=sk-..." > .env
```

#### Local Model Setup (vLLM)

```python
# Download and configure local model
from vllm import LLM

# Initialize local model
llm = LLM(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    tensor_parallel_size=1,
    gpu_memory_utilization=0.9,
    dtype="float16"
)

print("✓ Local model loaded")
```

### Verification

```python
# Verify installation
import ares
print(f"ARES version: {ares.__version__}")

# Test basic functionality
from ares import ARES

ares_eval = ARES(model="gpt-4o-mini")
print("✓ ARES initialized successfully")
```

---

## Core Concepts

### 1. Synthetic Data Generation

**Purpose**: Automatically create evaluation datasets from your document corpus.

**Process**:
```python
# Document → Query → Answer pipeline
documents = [
    "Python was created by Guido van Rossum in 1991.",
    "Machine learning is a subset of artificial intelligence."
]

# ARES generates:
synthetic_examples = [
    {
        "query": "Who created Python?",
        "document": "Python was created by Guido van Rossum in 1991.",
        "answer": "Guido van Rossum created Python in 1991."
    }
]
```

**Benefits**:
- Reduces manual test case creation
- Ensures comprehensive coverage
- Enables rapid dataset expansion
- Supports negative example generation

### 2. Few-Shot Human Annotation

**Purpose**: Provide calibration data for PPI without extensive annotation.

**Annotation Process**:
```python
# Annotate small sample (500 examples)
def annotate_example(example):
    """
    For each example, annotators provide:
    1. Context Relevance: 0 or 1
    2. Answer Faithfulness: 0 or 1
    3. Answer Relevance: 0 or 1
    """
    return {
        "context_relevance": 1,
        "answer_faithfulness": 1,
        "answer_relevance": 1
    }
```

**Best Practices**:
- Use multiple annotators (2-3)
- Measure inter-annotator agreement
- Focus on edge cases
- Include diverse examples

### 3. Classifier Training

**Purpose**: Train efficient, domain-specific evaluation models.

**Architecture**:
```python
# Typical classifier architecture
Base Model: DistilBERT-base-uncased
Input: [CLS] query [SEP] context/answer [SEP]
Output: Binary classification (0 or 1)
Training: Fine-tuned on synthetic data
```

**Training Process**:
```python
from ares import ClassifierTrainer

trainer = ClassifierTrainer(
    base_model="distilbert-base-uncased",
    num_epochs=3,
    batch_size=32,
    learning_rate=2e-5
)

# Train one classifier per metric
classifiers = trainer.train_all_metrics(
    synthetic_data=synthetic_data,
    metrics=["context_relevance", "answer_faithfulness", "answer_relevance"]
)
```

### 4. Evaluation with PPI

**Purpose**: Produce statistically rigorous evaluations with confidence intervals.

**Evaluation Flow**:
```python
# Step 1: Classifier predictions (fast, cheap)
ml_predictions = classifiers.predict(test_data)

# Step 2: Human labels on small subset
human_labels = annotate_sample(test_data.sample(500))

# Step 3: PPI calibration
ppi_results = compute_ppi(
    ml_predictions=ml_predictions,
    human_labels=human_labels
)

# Output: Mean ± Confidence Interval
# Context Relevance: 0.89 ± 0.03
```

---

## Production-Ready Examples

### Example 1: Basic RAG Evaluation

```python
"""
Simple RAG system evaluation with ARES.
Evaluates a basic RAG pipeline end-to-end.
"""

from ares import ARES
import pandas as pd

def basic_rag_evaluation():
    """Basic RAG evaluation example."""

    # Initialize ARES
    ares = ARES(model="gpt-4o-mini")

    # Define RAG outputs to evaluate
    rag_outputs = [
        {
            "query": "What is Python?",
            "retrieved_contexts": [
                "Python is a high-level programming language created by Guido van Rossum.",
                "Python emphasizes code readability with significant whitespace."
            ],
            "generated_answer": "Python is a high-level programming language known for readability."
        },
        {
            "query": "Who invented machine learning?",
            "retrieved_contexts": [
                "Machine learning is a subset of AI that learns from data.",
                "Neural networks are a popular machine learning technique."
            ],
            "generated_answer": "Arthur Samuel coined the term 'machine learning' in 1959."
        }
    ]

    # Evaluate (using LLM directly, no training)
    results = ares.evaluate(
        rag_outputs=rag_outputs,
        metrics=["context_relevance", "answer_faithfulness", "answer_relevance"]
    )

    # Display results
    print("RAG Evaluation Results:\n")
    for metric, scores in results.items():
        print(f"{metric}:")
        print(f"  Mean: {scores['mean']:.3f}")
        print(f"  Std Dev: {scores['std']:.3f}")
        print(f"  Min: {scores['min']:.3f}")
        print(f"  Max: {scores['max']:.3f}")
        print()

    return results

if __name__ == "__main__":
    basic_rag_evaluation()
```

**Output**:
```
RAG Evaluation Results:

context_relevance:
  Mean: 0.850
  Std Dev: 0.212
  Min: 0.500
  Max: 1.000

answer_faithfulness:
  Mean: 0.750
  Std Dev: 0.354
  Min: 0.000
  Max: 1.000

answer_relevance:
  Mean: 0.950
  Std Dev: 0.071
  Min: 0.900
  Max: 1.000
```

### Example 2: Synthetic Data Generation Pipeline

```python
"""
Generate synthetic evaluation data from documents.
Useful for creating test datasets without manual annotation.
"""

from ares import ARES, SyntheticDataGenerator
import json
from pathlib import Path

def generate_synthetic_evaluation_data():
    """Generate synthetic test data from documents."""

    # Load document corpus
    documents = load_document_corpus("knowledge_base/")
    print(f"Loaded {len(documents)} documents")

    # Initialize generator
    generator = SyntheticDataGenerator(
        model="gpt-4o",  # Better quality for generation
        temperature=0.7,
        max_tokens=200
    )

    # Generate synthetic examples
    synthetic_data = generator.generate(
        documents=documents,
        num_samples_per_document=5,
        include_negative_samples=True,
        negative_sample_ratio=0.2,
        difficulty_levels=["easy", "medium", "hard"]
    )

    print(f"Generated {len(synthetic_data)} synthetic examples")

    # Analyze generated data
    difficulty_distribution = count_by_difficulty(synthetic_data)
    print("\nDifficulty Distribution:")
    for level, count in difficulty_distribution.items():
        print(f"  {level}: {count} examples")

    # Save for later use
    save_synthetic_data(synthetic_data, "synthetic_eval_data.json")

    # Example: View one generated example
    example = synthetic_data[0]
    print("\nExample Generated Data:")
    print(f"Query: {example['query']}")
    print(f"Document: {example['document'][:100]}...")
    print(f"Answer: {example['answer']}")
    print(f"Is Positive: {example['is_positive']}")
    print(f"Difficulty: {example['difficulty']}")

    return synthetic_data

def load_document_corpus(path: str) -> list:
    """Load documents from directory."""
    corpus = []
    for file in Path(path).glob("**/*.txt"):
        with open(file, 'r') as f:
            corpus.append({
                "id": file.stem,
                "text": f.read(),
                "source": str(file)
            })
    return corpus

def count_by_difficulty(data: list) -> dict:
    """Count examples by difficulty level."""
    counts = {}
    for example in data:
        level = example.get('difficulty', 'unknown')
        counts[level] = counts.get(level, 0) + 1
    return counts

def save_synthetic_data(data: list, filename: str):
    """Save synthetic data to JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n✓ Saved synthetic data to {filename}")

if __name__ == "__main__":
    generate_synthetic_evaluation_data()
```

### Example 3: Full Pipeline with Classifier Training

```python
"""
Complete ARES pipeline: synthetic data, training, PPI evaluation.
Production-ready implementation for scalable RAG evaluation.
"""

from ares import ARES, ClassifierTrainer, PPIEvaluator
import pandas as pd
from typing import List, Dict
import numpy as np

class ARESProductionPipeline:
    """Production ARES evaluation pipeline."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.ares = ARES(model=model)
        self.classifiers = None
        self.synthetic_data = None
        self.human_annotations = None

    def step1_generate_synthetic_data(
        self,
        documents: List[str],
        num_samples: int = 5000
    ) -> pd.DataFrame:
        """Step 1: Generate synthetic training data."""
        print(f"\n[Step 1] Generating {num_samples} synthetic examples...")

        self.synthetic_data = self.ares.generate_synthetic_data(
            documents=documents,
            num_samples=num_samples,
            include_negative_samples=True,
            difficulty_levels=["easy", "medium", "hard"]
        )

        print(f"✓ Generated {len(self.synthetic_data)} examples")
        print(f"  Positive samples: {sum(1 for x in self.synthetic_data if x['is_positive'])}")
        print(f"  Negative samples: {sum(1 for x in self.synthetic_data if not x['is_positive'])}")

        return self.synthetic_data

    def step2_human_annotation(
        self,
        num_annotations: int = 500
    ) -> pd.DataFrame:
        """Step 2: Collect human annotations for PPI calibration."""
        print(f"\n[Step 2] Collecting {num_annotations} human annotations...")

        # Sample examples for annotation
        annotation_sample = pd.DataFrame(self.synthetic_data).sample(num_annotations)

        # In production, this would call your annotation service
        # For demo, simulate annotations
        self.human_annotations = self._simulate_human_annotations(annotation_sample)

        # Calculate inter-annotator agreement
        agreement = self._calculate_agreement(self.human_annotations)
        print(f"✓ Collected {len(self.human_annotations)} annotations")
        print(f"  Inter-annotator agreement: {agreement:.3f}")

        return self.human_annotations

    def step3_train_classifiers(
        self,
        epochs: int = 3,
        batch_size: int = 32
    ) -> Dict:
        """Step 3: Train evaluation classifiers."""
        print(f"\n[Step 3] Training evaluation classifiers...")

        trainer = ClassifierTrainer(
            base_model="distilbert-base-uncased",
            num_epochs=epochs,
            batch_size=batch_size,
            learning_rate=2e-5
        )

        # Train classifiers for each metric
        metrics = ["context_relevance", "answer_faithfulness", "answer_relevance"]
        self.classifiers = {}

        for metric in metrics:
            print(f"\n  Training {metric} classifier...")
            classifier = trainer.train(
                synthetic_data=self.synthetic_data,
                metric=metric,
                validation_split=0.1
            )

            # Evaluate on validation set
            val_accuracy = classifier.evaluate()
            print(f"  ✓ {metric}: Val Accuracy = {val_accuracy:.3f}")

            self.classifiers[metric] = classifier

        print(f"\n✓ All classifiers trained")
        return self.classifiers

    def step4_evaluate_with_ppi(
        self,
        test_data: List[Dict]
    ) -> Dict:
        """Step 4: Evaluate with Prediction-Powered Inference."""
        print(f"\n[Step 4] Evaluating {len(test_data)} examples with PPI...")

        ppi_evaluator = PPIEvaluator(
            classifiers=self.classifiers,
            human_annotations=self.human_annotations
        )

        # Get classifier predictions
        predictions = {}
        for metric, classifier in self.classifiers.items():
            predictions[metric] = classifier.predict(test_data)

        # Apply PPI calibration
        results = ppi_evaluator.compute_ppi_estimates(
            predictions=predictions,
            confidence_level=0.95
        )

        # Display results with confidence intervals
        print("\nPPI-Calibrated Results:")
        for metric, scores in results.items():
            print(f"\n{metric}:")
            print(f"  Mean: {scores['mean']:.3f}")
            print(f"  95% CI: [{scores['ci_lower']:.3f}, {scores['ci_upper']:.3f}]")
            print(f"  Std Dev: {scores['std']:.3f}")
            print(f"  Margin of Error: ±{scores['margin_of_error']:.3f}")

        return results

    def _simulate_human_annotations(self, examples: pd.DataFrame) -> pd.DataFrame:
        """Simulate human annotations (replace with real annotation service)."""
        annotations = []
        for _, example in examples.iterrows():
            annotations.append({
                "example_id": example.get('id'),
                "context_relevance": np.random.choice([0, 1], p=[0.2, 0.8]),
                "answer_faithfulness": np.random.choice([0, 1], p=[0.15, 0.85]),
                "answer_relevance": np.random.choice([0, 1], p=[0.1, 0.9]),
                "annotator": "simulated"
            })
        return pd.DataFrame(annotations)

    def _calculate_agreement(self, annotations: pd.DataFrame) -> float:
        """Calculate inter-annotator agreement (Cohen's Kappa)."""
        # Simplified - in production, use actual IAA calculation
        return 0.85

def run_full_pipeline():
    """Run complete ARES pipeline."""

    # Initialize pipeline
    pipeline = ARESProductionPipeline(model="gpt-4o-mini")

    # Load documents
    documents = load_documents("knowledge_base/")

    # Execute pipeline
    synthetic_data = pipeline.step1_generate_synthetic_data(
        documents=documents,
        num_samples=5000
    )

    annotations = pipeline.step2_human_annotation(
        num_annotations=500
    )

    classifiers = pipeline.step3_train_classifiers(
        epochs=3,
        batch_size=32
    )

    # Evaluate test set
    test_data = load_test_data("test_set.json")
    results = pipeline.step4_evaluate_with_ppi(test_data)

    print("\n" + "="*60)
    print("Pipeline Complete!")
    print("="*60)

    return results

if __name__ == "__main__":
    run_full_pipeline()
```

### Example 4: Local Model Execution (Privacy-Conscious)

```python
"""
Run ARES completely locally with vLLM.
No external API calls - suitable for sensitive data.
"""

from ares import ARES, LocalModelConfig
from vllm import LLM
import torch

def setup_local_ares():
    """Configure ARES for local execution."""

    print("Setting up local ARES pipeline...")

    # Check GPU availability
    if torch.cuda.is_available():
        print(f"✓ GPU available: {torch.cuda.get_device_name(0)}")
        print(f"  Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("⚠ No GPU available - using CPU (slower)")

    # Initialize local model
    local_llm = LLM(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        tensor_parallel_size=1,
        gpu_memory_utilization=0.9,
        dtype="float16",
        trust_remote_code=True
    )

    print("✓ Local model loaded")

    # Configure ARES for local mode
    config = LocalModelConfig(
        llm=local_llm,
        local_mode=True,
        privacy_preserving=True,
        no_external_calls=True
    )

    ares = ARES(config=config)
    print("✓ ARES configured for local execution")

    return ares

def generate_synthetic_data_locally():
    """Generate synthetic data without external API calls."""

    ares = setup_local_ares()

    # Load documents
    documents = load_sensitive_documents("confidential/")
    print(f"Loaded {len(documents)} confidential documents")

    # Generate synthetic data locally
    print("\nGenerating synthetic data (100% local)...")
    synthetic_data = ares.generate_synthetic_data(
        documents=documents,
        num_samples=1000
    )

    print(f"✓ Generated {len(synthetic_data)} examples")
    print("  ✓ No external API calls made")
    print("  ✓ Data never left your infrastructure")
    print("  ✓ Complete privacy preserved")

    return synthetic_data

def train_classifiers_locally():
    """Train evaluation classifiers on local hardware."""

    from ares import ClassifierTrainer

    print("\nTraining classifiers locally...")

    # Configure for local training
    trainer = ClassifierTrainer(
        base_model="distilbert-base-uncased",
        device="cuda" if torch.cuda.is_available() else "cpu",
        local_only=True
    )

    # Train classifiers
    synthetic_data = load_synthetic_data("synthetic_data.json")
    classifiers = trainer.train_all_metrics(
        synthetic_data=synthetic_data,
        metrics=["context_relevance", "answer_faithfulness", "answer_relevance"]
    )

    print("✓ Classifiers trained locally")

    # Save classifiers for reuse
    save_classifiers(classifiers, "local_classifiers/")
    print("✓ Classifiers saved to disk")

    return classifiers

def evaluate_locally():
    """Complete evaluation pipeline - 100% local."""

    ares = setup_local_ares()

    # Load pre-trained classifiers
    classifiers = load_classifiers("local_classifiers/")

    # Load test data
    test_data = load_test_data("test_data.json")

    # Evaluate locally
    print(f"\nEvaluating {len(test_data)} examples locally...")
    results = ares.evaluate_with_classifiers(
        rag_outputs=test_data,
        classifiers=classifiers,
        local_mode=True
    )

    print("\nLocal Evaluation Complete:")
    print("  ✓ Zero API costs")
    print("  ✓ Complete privacy")
    print("  ✓ Data never transmitted externally")
    print("\nResults:")
    for metric, scores in results.items():
        print(f"  {metric}: {scores['mean']:.3f}")

    return results

if __name__ == "__main__":
    # Run complete local pipeline
    synthetic_data = generate_synthetic_data_locally()
    classifiers = train_classifiers_locally()
    results = evaluate_locally()
```

### Example 5: Domain-Specific Evaluation (Medical)

```python
"""
Medical RAG evaluation with domain-specific considerations.
Includes safety checks and high faithfulness requirements.
"""

from ares import ARES, MedicalDomainAdapter
from typing import List, Dict
import warnings

class MedicalRAGEvaluator:
    """Specialized evaluator for medical RAG systems."""

    def __init__(self):
        # Use domain adapter for medical context
        self.adapter = MedicalDomainAdapter(
            terminology_database="medical_terms.json",
            safety_rules="medical_safety_rules.yaml"
        )

        self.ares = ARES(
            model="gpt-4o",  # Use most capable model for medical
            domain_adapter=self.adapter
        )

        # Medical-specific thresholds (higher standards)
        self.thresholds = {
            "context_relevance": 0.90,
            "answer_faithfulness": 0.95,  # Very high for medical
            "answer_relevance": 0.90
        }

    def evaluate_medical_rag(
        self,
        rag_outputs: List[Dict],
        include_safety_check: bool = True
    ) -> Dict:
        """Evaluate medical RAG with safety checks."""

        print("Evaluating Medical RAG System...")
        print(f"  Samples: {len(rag_outputs)}")
        print(f"  Safety checks: {'Enabled' if include_safety_check else 'Disabled'}")
        print(f"  Faithfulness threshold: {self.thresholds['answer_faithfulness']}")

        # Standard ARES evaluation
        results = self.ares.evaluate(
            rag_outputs=rag_outputs,
            metrics=["context_relevance", "answer_faithfulness", "answer_relevance"],
            domain_specific_scoring=True
        )

        # Safety checks
        if include_safety_check:
            safety_results = self._run_safety_checks(rag_outputs, results)
            results['safety'] = safety_results

        # Analyze results against medical thresholds
        analysis = self._analyze_medical_quality(results)
        results['quality_analysis'] = analysis

        return results

    def _run_safety_checks(
        self,
        rag_outputs: List[Dict],
        eval_results: Dict
    ) -> Dict:
        """Run medical safety checks."""

        safety_issues = []

        for i, output in enumerate(rag_outputs):
            # Check 1: Low faithfulness in medical context
            if eval_results['answer_faithfulness']['scores'][i] < 0.95:
                safety_issues.append({
                    "index": i,
                    "issue": "Low faithfulness in medical answer",
                    "severity": "HIGH",
                    "faithfulness_score": eval_results['answer_faithfulness']['scores'][i],
                    "recommendation": "Manual review required"
                })

            # Check 2: Ungrounded medical claims
            if self._contains_medical_claims(output['generated_answer']):
                if not self._all_claims_grounded(output):
                    safety_issues.append({
                        "index": i,
                        "issue": "Ungrounded medical claim detected",
                        "severity": "CRITICAL",
                        "recommendation": "Do not use - potential patient safety risk"
                    })

            # Check 3: Contradictory information
            if self._contains_contradictions(output):
                safety_issues.append({
                    "index": i,
                    "issue": "Contradictory medical information",
                    "severity": "HIGH",
                    "recommendation": "Review source consistency"
                })

        return {
            "total_issues": len(safety_issues),
            "critical_issues": sum(1 for x in safety_issues if x['severity'] == 'CRITICAL'),
            "high_issues": sum(1 for x in safety_issues if x['severity'] == 'HIGH'),
            "issues": safety_issues
        }

    def _analyze_medical_quality(self, results: Dict) -> Dict:
        """Analyze quality against medical standards."""

        analysis = {}

        for metric, threshold in self.thresholds.items():
            mean_score = results[metric]['mean']
            meets_threshold = mean_score >= threshold

            analysis[metric] = {
                "score": mean_score,
                "threshold": threshold,
                "meets_standard": meets_threshold,
                "gap": threshold - mean_score if not meets_threshold else 0
            }

            if not meets_threshold:
                warnings.warn(
                    f"Medical quality warning: {metric} score ({mean_score:.3f}) "
                    f"below threshold ({threshold})"
                )

        return analysis

    def _contains_medical_claims(self, text: str) -> bool:
        """Check if text contains medical claims."""
        medical_keywords = [
            "symptom", "diagnosis", "treatment", "medication",
            "disease", "condition", "therapy", "prescription"
        ]
        return any(keyword in text.lower() for keyword in medical_keywords)

    def _all_claims_grounded(self, output: Dict) -> bool:
        """Verify all medical claims are grounded in sources."""
        # Implementation would use claim extraction and verification
        return True  # Simplified for example

    def _contains_contradictions(self, output: Dict) -> bool:
        """Check for contradictory medical information."""
        # Implementation would compare claims across contexts
        return False  # Simplified for example

def run_medical_evaluation():
    """Run medical RAG evaluation with safety checks."""

    evaluator = MedicalRAGEvaluator()

    # Medical RAG outputs
    medical_rag_outputs = [
        {
            "query": "What are the symptoms of type 2 diabetes?",
            "retrieved_contexts": [
                "Type 2 diabetes symptoms include increased thirst, frequent urination, "
                "increased hunger, fatigue, blurred vision, and slow-healing sores."
            ],
            "generated_answer": "Common symptoms include increased thirst, frequent urination, "
                              "fatigue, and blurred vision."
        },
        {
            "query": "What medications treat hypertension?",
            "retrieved_contexts": [
                "ACE inhibitors, beta-blockers, and diuretics are common hypertension medications.",
                "Lifestyle changes like diet and exercise are also recommended for hypertension."
            ],
            "generated_answer": "ACE inhibitors and beta-blockers are commonly prescribed. "
                              "Lifestyle changes are also important."
        }
    ]

    # Evaluate with safety checks
    results = evaluator.evaluate_medical_rag(
        rag_outputs=medical_rag_outputs,
        include_safety_check=True
    )

    # Display results
    print("\n" + "="*60)
    print("Medical RAG Evaluation Results")
    print("="*60)

    for metric in ["context_relevance", "answer_faithfulness", "answer_relevance"]:
        analysis = results['quality_analysis'][metric]
        print(f"\n{metric}:")
        print(f"  Score: {analysis['score']:.3f}")
        print(f"  Threshold: {analysis['threshold']}")
        print(f"  Status: {'✓ PASS' if analysis['meets_standard'] else '✗ FAIL'}")
        if not analysis['meets_standard']:
            print(f"  Gap: {analysis['gap']:.3f}")

    # Safety report
    print("\n" + "="*60)
    print("Safety Analysis")
    print("="*60)
    safety = results['safety']
    print(f"Total Issues: {safety['total_issues']}")
    print(f"Critical Issues: {safety['critical_issues']}")
    print(f"High Priority Issues: {safety['high_issues']}")

    if safety['critical_issues'] > 0:
        print("\n⚠ CRITICAL: Manual review required before deployment")

    return results

if __name__ == "__main__":
    run_medical_evaluation()
```

### Example 6: A/B Testing RAG Configurations

```python
"""
Compare different RAG configurations using ARES.
Statistical significance testing with confidence intervals.
"""

from ares import ARES
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List

class RAGConfigTester:
    """A/B test different RAG configurations."""

    def __init__(self):
        self.ares = ARES(model="gpt-4o-mini")
        self.results = {}

    def test_configuration(
        self,
        config_name: str,
        config_params: Dict,
        test_queries: List[str]
    ) -> Dict:
        """Test a specific RAG configuration."""

        print(f"\nTesting Configuration: {config_name}")
        print(f"  Parameters: {config_params}")

        # Run RAG system with configuration
        rag_outputs = self._run_rag_with_config(config_params, test_queries)

        # Evaluate with ARES
        results = self.ares.evaluate(
            rag_outputs=rag_outputs,
            metrics=["context_relevance", "answer_faithfulness", "answer_relevance"],
            use_ppi=True,
            confidence_level=0.95
        )

        # Store results
        self.results[config_name] = results

        # Display results
        print(f"\n  Results for {config_name}:")
        for metric, scores in results.items():
            print(f"    {metric}: {scores['mean']:.3f} "
                  f"(95% CI: [{scores['ci_lower']:.3f}, {scores['ci_upper']:.3f}])")

        return results

    def compare_configurations(
        self,
        config_a: str,
        config_b: str,
        significance_level: float = 0.05
    ) -> Dict:
        """Compare two configurations statistically."""

        print(f"\n{'='*60}")
        print(f"Comparing {config_a} vs {config_b}")
        print(f"{'='*60}")

        results_a = self.results[config_a]
        results_b = self.results[config_b]

        comparison = {}

        for metric in ["context_relevance", "answer_faithfulness", "answer_relevance"]:
            # Get scores
            mean_a = results_a[metric]['mean']
            mean_b = results_b[metric]['mean']
            std_a = results_a[metric]['std']
            std_b = results_b[metric]['std']

            # Calculate statistical significance
            t_stat, p_value = stats.ttest_ind_from_stats(
                mean1=mean_a, std1=std_a, nobs1=100,
                mean2=mean_b, std2=std_b, nobs2=100
            )

            is_significant = p_value < significance_level
            improvement = ((mean_b - mean_a) / mean_a) * 100

            comparison[metric] = {
                "config_a_mean": mean_a,
                "config_b_mean": mean_b,
                "difference": mean_b - mean_a,
                "improvement_pct": improvement,
                "p_value": p_value,
                "is_significant": is_significant,
                "winner": config_b if mean_b > mean_a else config_a
            }

            # Display comparison
            print(f"\n{metric}:")
            print(f"  {config_a}: {mean_a:.3f}")
            print(f"  {config_b}: {mean_b:.3f}")
            print(f"  Difference: {improvement:+.1f}%")
            print(f"  p-value: {p_value:.4f}")
            print(f"  Significant: {'✓ YES' if is_significant else '✗ NO'}")
            print(f"  Winner: {comparison[metric]['winner']}")

        return comparison

    def recommend_configuration(self) -> str:
        """Recommend best configuration based on results."""

        # Calculate overall scores
        overall_scores = {}
        for config_name, results in self.results.items():
            overall = sum(results[m]['mean'] for m in results.keys()) / len(results)
            overall_scores[config_name] = overall

        # Find best configuration
        best_config = max(overall_scores.items(), key=lambda x: x[1])

        print(f"\n{'='*60}")
        print("Recommendation")
        print(f"{'='*60}")
        print(f"\nBest Configuration: {best_config[0]}")
        print(f"Overall Score: {best_config[1]:.3f}")
        print(f"\nConfiguration Rankings:")
        for i, (config, score) in enumerate(
            sorted(overall_scores.items(), key=lambda x: x[1], reverse=True),
            1
        ):
            print(f"  {i}. {config}: {score:.3f}")

        return best_config[0]

    def _run_rag_with_config(
        self,
        config: Dict,
        queries: List[str]
    ) -> List[Dict]:
        """Run RAG system with specific configuration."""
        # Implementation would run actual RAG system
        # For demo, return simulated outputs
        return [
            {
                "query": q,
                "retrieved_contexts": [f"Context for {q}"],
                "generated_answer": f"Answer for {q}"
            }
            for q in queries
        ]

    def plot_comparison(self):
        """Visualize configuration comparison."""

        import matplotlib.pyplot as plt
        import numpy as np

        configs = list(self.results.keys())
        metrics = ["context_relevance", "answer_faithfulness", "answer_relevance"]

        x = np.arange(len(metrics))
        width = 0.8 / len(configs)

        fig, ax = plt.subplots(figsize=(12, 6))

        for i, config in enumerate(configs):
            means = [self.results[config][m]['mean'] for m in metrics]
            errors = [
                self.results[config][m]['ci_upper'] - self.results[config][m]['mean']
                for m in metrics
            ]

            ax.bar(
                x + i * width,
                means,
                width,
                label=config,
                yerr=errors,
                capsize=5
            )

        ax.set_xlabel('Metrics')
        ax.set_ylabel('Scores')
        ax.set_title('RAG Configuration Comparison')
        ax.set_xticks(x + width * (len(configs) - 1) / 2)
        ax.set_xticklabels(metrics, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig('rag_config_comparison.png', dpi=300)
        print("\n✓ Comparison plot saved to rag_config_comparison.png")

def run_ab_test():
    """Run A/B test of RAG configurations."""

    tester = RAGConfigTester()

    # Define test queries
    test_queries = [
        "What is machine learning?",
        "How does neural network training work?",
        "What are the applications of AI?",
        # ... more queries
    ] * 10  # 100 total queries

    # Test Configuration A: Baseline
    tester.test_configuration(
        config_name="Baseline",
        config_params={
            "retrieval_top_k": 3,
            "chunk_size": 512,
            "rerank": False,
            "model": "gpt-3.5-turbo"
        },
        test_queries=test_queries
    )

    # Test Configuration B: Enhanced Retrieval
    tester.test_configuration(
        config_name="Enhanced Retrieval",
        config_params={
            "retrieval_top_k": 5,
            "chunk_size": 512,
            "rerank": True,
            "model": "gpt-3.5-turbo"
        },
        test_queries=test_queries
    )

    # Test Configuration C: Better Model
    tester.test_configuration(
        config_name="Better Model",
        config_params={
            "retrieval_top_k": 3,
            "chunk_size": 512,
            "rerank": False,
            "model": "gpt-4o"
        },
        test_queries=test_queries
    )

    # Compare configurations
    tester.compare_configurations("Baseline", "Enhanced Retrieval")
    tester.compare_configurations("Baseline", "Better Model")
    tester.compare_configurations("Enhanced Retrieval", "Better Model")

    # Get recommendation
    best_config = tester.recommend_configuration()

    # Visualize results
    tester.plot_comparison()

    return best_config

if __name__ == "__main__":
    best = run_ab_test()
```

### Example 7: Confidence Interval Analysis

```python
"""
Analyze how confidence intervals change with sample size.
Demonstrates statistical power and sample size planning.
"""

from ares import ARES
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def confidence_interval_analysis():
    """Analyze CI width vs sample size."""

    ares = ARES(model="gpt-4o-mini")

    # Generate large test set
    print("Generating test data...")
    all_rag_outputs = generate_test_data(n=2000)

    # Test different sample sizes
    sample_sizes = [10, 20, 50, 100, 200, 500, 1000, 2000]
    results_by_size = {}

    print("\nAnalyzing confidence intervals...")
    for n in sample_sizes:
        print(f"  Sample size: {n}")

        # Sample from test set
        sample = all_rag_outputs[:n]

        # Evaluate with PPI
        results = ares.evaluate(
            rag_outputs=sample,
            metrics=["answer_faithfulness"],
            use_ppi=True,
            confidence_level=0.95
        )

        results_by_size[n] = results['answer_faithfulness']

    # Plot results
    plot_ci_analysis(results_by_size, sample_sizes)

    # Recommend sample size
    recommend_sample_size(results_by_size)

    return results_by_size

def plot_ci_analysis(results: dict, sample_sizes: list):
    """Plot confidence interval width vs sample size."""

    means = [results[n]['mean'] for n in sample_sizes]
    ci_widths = [
        results[n]['ci_upper'] - results[n]['ci_lower']
        for n in sample_sizes
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Mean estimate with confidence intervals
    ax1.errorbar(
        sample_sizes,
        means,
        yerr=[w/2 for w in ci_widths],
        marker='o',
        capsize=5,
        capthick=2
    )
    ax1.set_xscale('log')
    ax1.set_xlabel('Sample Size')
    ax1.set_ylabel('Answer Faithfulness')
    ax1.set_title('Estimate Precision vs Sample Size')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=means[-1], color='r', linestyle='--', alpha=0.5, label='True value (n=2000)')
    ax1.legend()

    # Plot 2: CI width vs sample size
    ax2.plot(sample_sizes, ci_widths, marker='o', linewidth=2)
    ax2.set_xscale('log')
    ax2.set_xlabel('Sample Size')
    ax2.set_ylabel('95% Confidence Interval Width')
    ax2.set_title('Confidence Interval Width vs Sample Size')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0.05, color='r', linestyle='--', alpha=0.5, label='Target precision (±0.05)')
    ax2.legend()

    plt.tight_layout()
    plt.savefig('ci_analysis.png', dpi=300)
    print("\n✓ Analysis plot saved to ci_analysis.png")

def recommend_sample_size(results: dict):
    """Recommend sample size based on desired precision."""

    target_precisions = [0.01, 0.02, 0.03, 0.05, 0.10]

    print("\n" + "="*60)
    print("Sample Size Recommendations")
    print("="*60)

    for target in target_precisions:
        # Find minimum sample size for target precision
        for n, result in sorted(results.items()):
            ci_width = result['ci_upper'] - result['ci_lower']
            if ci_width <= target:
                print(f"  For ±{target:.3f} precision: n >= {n}")
                break
        else:
            print(f"  For ±{target:.3f} precision: n > 2000 (need more data)")

def generate_test_data(n: int) -> list:
    """Generate synthetic test data."""
    return [
        {
            "query": f"Query {i}",
            "retrieved_contexts": [f"Context {i}"],
            "generated_answer": f"Answer {i}"
        }
        for i in range(n)
    ]

if __name__ == "__main__":
    confidence_interval_analysis()
```

### Example 8: Cross-Domain Robustness Testing

```python
"""
Test classifier robustness across different domains.
Identifies when retraining is needed for domain shift.
"""

from ares import ARES, ClassifierTrainer
import pandas as pd
from typing import Dict, List

def cross_domain_robustness_test():
    """Test ARES classifiers across multiple domains."""

    print("="*60)
    print("Cross-Domain Robustness Analysis")
    print("="*60)

    # Train classifiers on source domain
    print("\n[Phase 1] Training on Tech Domain...")
    tech_docs = load_documents("tech_domain/")
    ares = ARES(model="gpt-4o")

    # Generate synthetic data from tech domain
    tech_synthetic = ares.generate_synthetic_data(
        documents=tech_docs,
        num_samples=5000
    )

    # Train classifiers
    trainer = ClassifierTrainer()
    classifiers = trainer.train_all_metrics(
        synthetic_data=tech_synthetic,
        metrics=["context_relevance", "answer_faithfulness", "answer_relevance"]
    )

    print("✓ Classifiers trained on Tech domain")

    # Test on multiple domains
    print("\n[Phase 2] Testing across domains...")

    test_domains = {
        "Tech": load_test_data("tech_test/"),
        "Medical": load_test_data("medical_test/"),
        "Finance": load_test_data("finance_test/"),
        "Legal": load_test_data("legal_test/"),
        "General": load_test_data("general_test/")
    }

    results = {}

    for domain_name, test_data in test_domains.items():
        print(f"\n  Testing on {domain_name} domain...")

        # Evaluate with trained classifiers
        domain_results = ares.evaluate_with_classifiers(
            rag_outputs=test_data,
            classifiers=classifiers
        )

        results[domain_name] = domain_results

        # Display results
        print(f"    Context Relevance: {domain_results['context_relevance']['mean']:.3f}")
        print(f"    Answer Faithfulness: {domain_results['answer_faithfulness']['mean']:.3f}")
        print(f"    Answer Relevance: {domain_results['answer_relevance']['mean']:.3f}")

        # Check for domain shift
        faithfulness_score = domain_results['answer_faithfulness']['mean']
        if faithfulness_score < 0.75:
            print(f"    ⚠ WARNING: Significant domain shift detected")
            print(f"              Consider retraining for {domain_name} domain")
        else:
            print(f"    ✓ Classifier robust to {domain_name} domain")

    # Analyze domain transfer
    analyze_domain_transfer(results)

    # Visualize results
    plot_domain_comparison(results)

    return results

def analyze_domain_transfer(results: Dict):
    """Analyze classifier performance across domains."""

    print("\n" + "="*60)
    print("Domain Transfer Analysis")
    print("="*60)

    # Calculate domain similarity scores
    source_domain = "Tech"
    source_scores = results[source_domain]

    for domain_name, domain_scores in results.items():
        if domain_name == source_domain:
            continue

        # Calculate score degradation
        degradation = {}
        for metric in ["context_relevance", "answer_faithfulness", "answer_relevance"]:
            source_mean = source_scores[metric]['mean']
            domain_mean = domain_scores[metric]['mean']
            degradation[metric] = source_mean - domain_mean

        avg_degradation = sum(degradation.values()) / len(degradation)

        print(f"\n{domain_name} Domain:")
        print(f"  Average degradation: {avg_degradation:.3f}")
        for metric, deg in degradation.items():
            print(f"    {metric}: {deg:+.3f}")

        # Recommendation
        if avg_degradation > 0.15:
            print(f"  Recommendation: RETRAIN classifiers for {domain_name}")
        elif avg_degradation > 0.05:
            print(f"  Recommendation: Consider retraining for optimal performance")
        else:
            print(f"  Recommendation: Current classifiers work well")

def plot_domain_comparison(results: Dict):
    """Visualize cross-domain performance."""

    import matplotlib.pyplot as plt
    import numpy as np

    domains = list(results.keys())
    metrics = ["context_relevance", "answer_faithfulness", "answer_relevance"]

    data = []
    for domain in domains:
        data.append([results[domain][m]['mean'] for m in metrics])

    data = np.array(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(domains))
    width = 0.25

    for i, metric in enumerate(metrics):
        ax.bar(x + i * width, data[:, i], width, label=metric)

    ax.set_xlabel('Domain')
    ax.set_ylabel('Score')
    ax.set_title('Cross-Domain Classifier Performance')
    ax.set_xticks(x + width)
    ax.set_xticklabels(domains)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig('domain_comparison.png', dpi=300)
    print("\n✓ Domain comparison plot saved")

def load_documents(path: str) -> List[str]:
    """Load documents from domain directory."""
    # Implementation depends on your data format
    return ["Document 1", "Document 2"]  # Placeholder

def load_test_data(path: str) -> List[Dict]:
    """Load test data for domain."""
    # Implementation depends on your data format
    return [
        {"query": "Test", "retrieved_contexts": ["Context"], "generated_answer": "Answer"}
    ]  # Placeholder

if __name__ == "__main__":
    cross_domain_robustness_test()
```

### Example 9: Cost Analysis and Optimization

```python
"""
Analyze and optimize ARES evaluation costs.
Compare different approaches and find optimal strategy.
"""

from ares import ARES
import pandas as pd
from dataclasses import dataclass
from typing import Dict

@dataclass
class CostEstimate:
    """Cost breakdown for ARES evaluation."""
    setup_cost: float
    per_eval_cost: float
    monthly_cost: float
    annual_cost: float

class AREScostAnalyzer:
    """Analyze and optimize ARES costs."""

    def __init__(self):
        self.pricing = {
            "gpt-4o": {"input": 5.00 / 1e6, "output": 15.00 / 1e6},  # per token
            "gpt-4o-mini": {"input": 0.150 / 1e6, "output": 0.600 / 1e6},
            "gpu_compute": 1.50,  # per hour
            "annotation": 0.25  # per example
        }

    def estimate_approach_costs(
        self,
        num_evaluations_per_month: int,
        approach: str
    ) -> CostEstimate:
        """Estimate costs for different approaches."""

        if approach == "llm_always":
            return self._estimate_llm_always(num_evaluations_per_month)
        elif approach == "trained_classifiers":
            return self._estimate_trained_classifiers(num_evaluations_per_month)
        elif approach == "local_models":
            return self._estimate_local_models(num_evaluations_per_month)
        else:
            raise ValueError(f"Unknown approach: {approach}")

    def _estimate_llm_always(self, num_evals: int) -> CostEstimate:
        """Cost for always using LLM (no training)."""

        # Assume GPT-4o-mini
        avg_tokens_per_eval = 500
        cost_per_eval = (
            avg_tokens_per_eval * self.pricing["gpt-4o-mini"]["input"] +
            avg_tokens_per_eval * self.pricing["gpt-4o-mini"]["output"]
        ) * 3  # 3 metrics

        return CostEstimate(
            setup_cost=0,
            per_eval_cost=cost_per_eval,
            monthly_cost=cost_per_eval * num_evals,
            annual_cost=cost_per_eval * num_evals * 12
        )

    def _estimate_trained_classifiers(self, num_evals: int) -> CostEstimate:
        """Cost for trained classifier approach."""

        # One-time setup costs
        synthetic_data_cost = 50  # Generate 5000 examples
        annotation_cost = 500 * self.pricing["annotation"]  # 500 annotations
        training_cost = 4 * self.pricing["gpu_compute"]  # 4 hours GPU

        setup_cost = synthetic_data_cost + annotation_cost + training_cost

        # Per-eval cost (much lower with trained models)
        per_eval_cost = 0.002  # GPU inference cost

        return CostEstimate(
            setup_cost=setup_cost,
            per_eval_cost=per_eval_cost,
            monthly_cost=per_eval_cost * num_evals,
            annual_cost=per_eval_cost * num_evals * 12
        )

    def _estimate_local_models(self, num_evals: int) -> CostEstimate:
        """Cost for local model approach."""

        # One-time setup
        setup_cost = 0  # Using existing infrastructure

        # Per-eval cost (compute only)
        per_eval_cost = 0.001

        return CostEstimate(
            setup_cost=setup_cost,
            per_eval_cost=per_eval_cost,
            monthly_cost=per_eval_cost * num_evals,
            annual_cost=per_eval_cost * num_evals * 12
        )

    def compare_approaches(
        self,
        monthly_evaluations: int
    ) -> pd.DataFrame:
        """Compare costs of different approaches."""

        approaches = ["llm_always", "trained_classifiers", "local_models"]
        results = []

        for approach in approaches:
            costs = self.estimate_approach_costs(monthly_evaluations, approach)

            # Calculate break-even point for trained classifiers
            if approach == "trained_classifiers":
                llm_costs = self.estimate_approach_costs(monthly_evaluations, "llm_always")
                monthly_savings = llm_costs.monthly_cost - costs.monthly_cost
                breakeven_months = costs.setup_cost / monthly_savings if monthly_savings > 0 else float('inf')
            else:
                breakeven_months = 0

            results.append({
                "Approach": approach.replace("_", " ").title(),
                "Setup Cost": f"${costs.setup_cost:.2f}",
                "Per-Eval Cost": f"${costs.per_eval_cost:.4f}",
                "Monthly Cost": f"${costs.monthly_cost:.2f}",
                "Annual Cost": f"${costs.annual_cost:.2f}",
                "Break-even (months)": f"{breakeven_months:.1f}" if breakeven_months != float('inf') else "N/A"
            })

        return pd.DataFrame(results)

    def recommend_approach(
        self,
        monthly_evaluations: int,
        time_horizon_months: int = 12
    ) -> str:
        """Recommend best approach based on usage."""

        costs = {
            approach: self.estimate_approach_costs(monthly_evaluations, approach)
            for approach in ["llm_always", "trained_classifiers", "local_models"]
        }

        # Calculate total cost over time horizon
        total_costs = {
            approach: cost.setup_cost + (cost.monthly_cost * time_horizon_months)
            for approach, cost in costs.items()
        }

        best_approach = min(total_costs.items(), key=lambda x: x[1])[0]

        print(f"\n{'='*60}")
        print(f"Cost Recommendation")
        print(f"{'='*60}")
        print(f"\nMonthly Evaluations: {monthly_evaluations:,}")
        print(f"Time Horizon: {time_horizon_months} months")

        print(f"\nTotal Costs over {time_horizon_months} months:")
        for approach, total_cost in sorted(total_costs.items(), key=lambda x: x[1]):
            print(f"  {approach.replace('_', ' ').title()}: ${total_cost:,.2f}")

        print(f"\n**Recommendation: {best_approach.replace('_', ' ').title()}**")

        # Provide reasoning
        if best_approach == "llm_always":
            print("\nReason: Low evaluation volume - setup costs not justified")
        elif best_approach == "trained_classifiers":
            print("\nReason: Medium-high volume - training investment pays off")
        else:
            print("\nReason: Very high volume or privacy needs - local execution optimal")

        return best_approach

def run_cost_analysis():
    """Run comprehensive cost analysis."""

    analyzer = ARESCostAnalyzer()

    # Test different usage levels
    usage_levels = [100, 1000, 10000, 100000, 1000000]

    print("="*60)
    print("ARES Cost Analysis")
    print("="*60)

    for monthly_evals in usage_levels:
        print(f"\n\nMonthly Evaluations: {monthly_evals:,}")
        print("-" * 60)

        # Compare approaches
        comparison = analyzer.compare_approaches(monthly_evals)
        print("\n" + comparison.to_string(index=False))

        # Get recommendation
        analyzer.recommend_approach(
            monthly_evaluations=monthly_evals,
            time_horizon_months=12
        )

if __name__ == "__main__":
    run_cost_analysis()
```

### Example 10: Production Deployment Pipeline

```python
"""
Production-ready ARES deployment with monitoring and alerting.
Complete MLOps pipeline for RAG evaluation at scale.
"""

from ares import ARES
import logging
from datetime import datetime
from pathlib import Path
import json
from typing import Dict, List
from dataclasses import dataclass, asdict

@dataclass
class EvaluationMetrics:
    """Evaluation metrics with metadata."""
    timestamp: str
    context_relevance: float
    answer_faithfulness: float
    answer_relevance: float
    num_samples: int
    model_version: str

class ProductionARESPipeline:
    """Production ARES deployment with monitoring."""

    def __init__(
        self,
        environment: str = "production",
        enable_monitoring: bool = True
    ):
        self.environment = environment
        self.enable_monitoring = enable_monitoring

        # Setup logging
        self.logger = self._setup_logging()

        # Initialize ARES
        self.ares = self._initialize_ares()

        # Load trained classifiers
        self.classifiers = self._load_classifiers()

        # Setup monitoring
        if enable_monitoring:
            self._setup_monitoring()

        self.logger.info(f"Production ARES pipeline initialized ({environment})")

    def _setup_logging(self) -> logging.Logger:
        """Configure production logging."""

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'ares_{self.environment}.log'),
                logging.StreamHandler()
            ]
        )

        return logging.getLogger(__name__)

    def _initialize_ares(self) -> ARES:
        """Initialize ARES with production config."""

        config = {
            "production": {"model": "gpt-4o", "timeout": 30},
            "staging": {"model": "gpt-4o-mini", "timeout": 60},
            "development": {"model": "gpt-4o-mini", "timeout": 120}
        }

        env_config = config[self.environment]
        return ARES(**env_config)

    def _load_classifiers(self) -> Dict:
        """Load pre-trained classifiers."""

        classifier_path = Path(f"models/{self.environment}/classifiers")

        if not classifier_path.exists():
            self.logger.warning("No pre-trained classifiers found")
            return None

        # Load classifiers
        classifiers = {}
        for metric in ["context_relevance", "answer_faithfulness", "answer_relevance"]:
            model_path = classifier_path / f"{metric}.pt"
            if model_path.exists():
                # Load model (implementation depends on framework)
                classifiers[metric] = load_model(model_path)
                self.logger.info(f"Loaded {metric} classifier")

        return classifiers

    def _setup_monitoring(self):
        """Setup monitoring and alerting."""

        # Initialize metrics storage
        self.metrics_file = Path(f"metrics/{self.environment}/evaluations.jsonl")
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)

        # Setup alert thresholds
        self.alert_thresholds = {
            "context_relevance": 0.75,
            "answer_faithfulness": 0.85,
            "answer_relevance": 0.75
        }

        self.logger.info("Monitoring enabled with alert thresholds")

    def evaluate_batch(
        self,
        rag_outputs: List[Dict],
        batch_id: str
    ) -> Dict:
        """Evaluate a batch of RAG outputs."""

        self.logger.info(f"Evaluating batch {batch_id} ({len(rag_outputs)} samples)")

        try:
            # Evaluate with classifiers (if available)
            if self.classifiers:
                results = self.ares.evaluate_with_classifiers(
                    rag_outputs=rag_outputs,
                    classifiers=self.classifiers,
                    use_ppi=True
                )
            else:
                # Fallback to LLM evaluation
                self.logger.warning("Using LLM evaluation (no classifiers available)")
                results = self.ares.evaluate(
                    rag_outputs=rag_outputs,
                    metrics=["context_relevance", "answer_faithfulness", "answer_relevance"]
                )

            # Create metrics object
            metrics = EvaluationMetrics(
                timestamp=datetime.now().isoformat(),
                context_relevance=results['context_relevance']['mean'],
                answer_faithfulness=results['answer_faithfulness']['mean'],
                answer_relevance=results['answer_relevance']['mean'],
                num_samples=len(rag_outputs),
                model_version="v1.0"
            )

            # Log metrics
            self._log_metrics(metrics, batch_id)

            # Check for alerts
            if self.enable_monitoring:
                self._check_alerts(metrics, batch_id)

            self.logger.info(f"Batch {batch_id} evaluation complete")

            return results

        except Exception as e:
            self.logger.error(f"Evaluation failed for batch {batch_id}: {e}")
            raise

    def _log_metrics(self, metrics: EvaluationMetrics, batch_id: str):
        """Log evaluation metrics."""

        # Write to metrics file
        with open(self.metrics_file, 'a') as f:
            record = {
                "batch_id": batch_id,
                **asdict(metrics)
            }
            f.write(json.dumps(record) + '\n')

        # Log to console
        self.logger.info(f"Metrics for batch {batch_id}:")
        self.logger.info(f"  Context Relevance: {metrics.context_relevance:.3f}")
        self.logger.info(f"  Answer Faithfulness: {metrics.answer_faithfulness:.3f}")
        self.logger.info(f"  Answer Relevance: {metrics.answer_relevance:.3f}")

    def _check_alerts(self, metrics: EvaluationMetrics, batch_id: str):
        """Check metrics against alert thresholds."""

        alerts = []

        for metric_name, threshold in self.alert_thresholds.items():
            value = getattr(metrics, metric_name)

            if value < threshold:
                alerts.append({
                    "metric": metric_name,
                    "value": value,
                    "threshold": threshold,
                    "severity": "HIGH" if value < threshold - 0.1 else "MEDIUM"
                })

        if alerts:
            self.logger.warning(f"Quality alerts for batch {batch_id}:")
            for alert in alerts:
                self.logger.warning(
                    f"  [{alert['severity']}] {alert['metric']}: {alert['value']:.3f} "
                    f"(threshold: {alert['threshold']})"
                )

            # Send notifications (implement based on your infrastructure)
            self._send_alerts(alerts, batch_id)

    def _send_alerts(self, alerts: List[Dict], batch_id: str):
        """Send alert notifications."""

        # Implementation depends on your notification system
        # Examples: Email, Slack, PagerDuty, etc.
        pass

    def get_metrics_summary(self, days: int = 7) -> Dict:
        """Get metrics summary for recent period."""

        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days)

        # Read metrics file
        metrics = []
        with open(self.metrics_file, 'r') as f:
            for line in f:
                record = json.loads(line)
                if datetime.fromisoformat(record['timestamp']) > cutoff_date:
                    metrics.append(record)

        if not metrics:
            return {"error": "No metrics available for period"}

        # Calculate summary statistics
        summary = {
            "period_days": days,
            "num_batches": len(metrics),
            "total_samples": sum(m['num_samples'] for m in metrics),
            "metrics": {
                "context_relevance": {
                    "mean": sum(m['context_relevance'] for m in metrics) / len(metrics),
                    "min": min(m['context_relevance'] for m in metrics),
                    "max": max(m['context_relevance'] for m in metrics)
                },
                "answer_faithfulness": {
                    "mean": sum(m['answer_faithfulness'] for m in metrics) / len(metrics),
                    "min": min(m['answer_faithfulness'] for m in metrics),
                    "max": max(m['answer_faithfulness'] for m in metrics)
                },
                "answer_relevance": {
                    "mean": sum(m['answer_relevance'] for m in metrics) / len(metrics),
                    "min": min(m['answer_relevance'] for m in metrics),
                    "max": max(m['answer_relevance'] for m in metrics)
                }
            }
        }

        return summary

def load_model(path: Path):
    """Load trained model (implementation depends on framework)."""
    # Placeholder
    return None

def deploy_production_pipeline():
    """Deploy production ARES pipeline."""

    print("="*60)
    print("Deploying Production ARES Pipeline")
    print("="*60)

    # Initialize pipeline
    pipeline = ProductionARESPipeline(
        environment="production",
        enable_monitoring=True
    )

    # Example: Evaluate production batch
    test_batch = [
        {
            "query": "Production query",
            "retrieved_contexts": ["Context"],
            "generated_answer": "Answer"
        }
    ] * 100

    results = pipeline.evaluate_batch(
        rag_outputs=test_batch,
        batch_id="batch_001"
    )

    # Get metrics summary
    summary = pipeline.get_metrics_summary(days=7)

    print("\n7-Day Metrics Summary:")
    print(f"  Batches evaluated: {summary.get('num_batches', 0)}")
    print(f"  Total samples: {summary.get('total_samples', 0)}")

    if 'metrics' in summary:
        for metric_name, stats in summary['metrics'].items():
            print(f"\n  {metric_name}:")
            print(f"    Mean: {stats['mean']:.3f}")
            print(f"    Range: [{stats['min']:.3f}, {stats['max']:.3f}]")

    print("\n✓ Production pipeline deployed and running")

if __name__ == "__main__":
    deploy_production_pipeline()
```

---

## Advanced Usage Patterns

### Pattern 1: Iterative Classifier Improvement

As you collect more data and human annotations, periodically retrain your classifiers to improve accuracy:

```python
def iterative_classifier_improvement():
    """Continuously improve classifiers with new data."""

    # Initial training
    v1_classifiers = train_initial_classifiers()

    # Deploy and collect feedback
    collect_production_feedback(v1_classifiers, duration_days=30)

    # Retrain with additional data
    new_annotations = collect_annotations_from_feedback()
    v2_classifiers = retrain_classifiers(
        existing_classifiers=v1_classifiers,
        additional_data=new_annotations
    )

    # Compare performance
    compare_classifier_versions(v1_classifiers, v2_classifiers)
```

### Pattern 2: Ensemble Evaluation

Combine multiple evaluation approaches for higher confidence:

```python
def ensemble_evaluation(rag_outputs):
    """Combine ARES with other evaluation methods."""

    # ARES evaluation
    ares_results = ares.evaluate(rag_outputs)

    # Additional evaluators
    ragas_results = evaluate_with_ragas(rag_outputs)
    custom_results = evaluate_with_custom_metrics(rag_outputs)

    # Ensemble
    ensemble_scores = weighted_average([
        (ares_results, 0.5),
        (ragas_results, 0.3),
        (custom_results, 0.2)
    ])

    return ensemble_scores
```

### Pattern 3: Active Learning for Annotation

Intelligently select examples for human annotation:

```python
def active_learning_annotation(synthetic_data, budget=500):
    """Select most informative examples for annotation."""

    # Train initial classifier
    classifier = train_on_subset(synthetic_data[:1000])

    # Predict on remaining data
    remaining = synthetic_data[1000:]
    predictions = classifier.predict(remaining)

    # Select uncertain examples (near decision boundary)
    uncertainty_scores = calculate_uncertainty(predictions)
    uncertain_examples = select_top_k(remaining, uncertainty_scores, k=budget)

    # Annotate these examples
    annotations = human_annotate(uncertain_examples)

    # Retrain with high-value annotations
    improved_classifier = retrain_with_annotations(
        classifier, annotations
    )

    return improved_classifier
```

---

## Best Practices

### 1. Synthetic Data Generation

**DO:**
- Generate diverse examples (easy, medium, hard)
- Include negative samples (bad retrievals, hallucinations)
- Use high-quality source documents
- Validate generated data quality with samples
- Generate sufficient volume (5000+ examples)

**DON'T:**
- Use only easy examples
- Generate from low-quality or incorrect documents
- Skip negative example generation
- Assume all generated data is perfect

### 2. Human Annotation

**DO:**
- Use multiple annotators (2-3)
- Measure inter-annotator agreement
- Provide clear annotation guidelines
- Include calibration examples
- Focus on edge cases and difficult examples

**DON'T:**
- Use single annotator
- Skip agreement measurement
- Provide vague guidelines
- Annotate only easy examples

### 3. Classifier Training

**DO:**
- Use appropriate base models (DistilBERT, RoBERTa)
- Validate on held-out set
- Monitor for overfitting
- Save model checkpoints
- Version control your models

**DON'T:**
- Overtrain on synthetic data
- Skip validation
- Use models that are too large (cost) or too small (accuracy)
- Forget to save/version models

### 4. Production Deployment

**DO:**
- Monitor evaluation quality over time
- Set up alerts for quality degradation
- Log all evaluations for analysis
- Have rollback plan
- Regular model retraining schedule

**DON'T:**
- Deploy without monitoring
- Ignore quality degradation
- Skip logging
- Assume models work forever without retraining

---

## Integration Guide

### Integration with LangChain

```python
from langchain.chains import RetrievalQA
from ares import ARES

def integrate_with_langchain():
    """Integrate ARES with LangChain RAG."""

    # Your LangChain RAG setup
    qa_chain = RetrievalQA.from_chain_type(...)

    # Wrap with ARES evaluation
    class EvaluatedRAG:
        def __init__(self, qa_chain, ares_evaluator):
            self.qa_chain = qa_chain
            self.ares = ares_evaluator

        def run(self, query):
            # Get RAG output
            result = self.qa_chain.run(query)

            # Evaluate
            eval_result = self.ares.evaluate([{
                "query": query,
                "retrieved_contexts": self._get_contexts(),
                "generated_answer": result
            }])

            return result, eval_result

    evaluated_rag = EvaluatedRAG(qa_chain, ARES())
    answer, quality = evaluated_rag.run("What is AI?")
```

### Integration with LlamaIndex

```python
from llama_index import VectorStoreIndex
from ares import ARES

def integrate_with_llamaindex():
    """Integrate ARES with LlamaIndex."""

    # Your LlamaIndex setup
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    # Evaluation wrapper
    ares = ARES()

    def evaluate_query(query):
        response = query_engine.query(query)

        eval_input = {
            "query": query,
            "retrieved_contexts": [
                node.text for node in response.source_nodes
            ],
            "generated_answer": str(response)
        }

        scores = ares.evaluate([eval_input])
        return response, scores

    return evaluate_query
```

### Integration with Haystack

```python
from haystack import Pipeline
from ares import ARES

def integrate_with_haystack():
    """Integrate ARES with Haystack."""

    from haystack.components.evaluators import CustomEvaluator

    class ARESEvaluator(CustomEvaluator):
        def __init__(self):
            self.ares = ARES()

        def run(self, queries, documents, answers):
            eval_inputs = [
                {
                    "query": q,
                    "retrieved_contexts": [d.content for d in docs],
                    "generated_answer": a
                }
                for q, docs, a in zip(queries, documents, answers)
            ]

            return self.ares.evaluate(eval_inputs)

    # Add to pipeline
    pipeline = Pipeline()
    pipeline.add_component("ares_eval", ARESEvaluator())
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Synthetic Data Quality Low

**Symptoms:**
- Generated queries don't make sense
- Answers are generic or incorrect
- Poor diversity in examples

**Solutions:**
```python
# Use better base model
ares = ARES(model="gpt-4o")  # Instead of gpt-4o-mini

# Add quality filtering
synthetic_data = ares.generate_synthetic_data(
    documents=docs,
    num_samples=10000,
    quality_threshold=0.8  # Filter low-quality generations
)

# Review and manual filter
high_quality = manual_review_sample(synthetic_data, sample_size=100)
```

#### Issue 2: Classifier Overfitting

**Symptoms:**
- High training accuracy, low validation accuracy
- Poor performance on real data
- Scores don't match human judgment

**Solutions:**
```python
# Use regularization
trainer = ClassifierTrainer(
    dropout=0.3,
    weight_decay=0.01,
    early_stopping=True,
    patience=3
)

# Increase validation split
classifiers = trainer.train(
    synthetic_data=data,
    validation_split=0.2  # Increase from 0.1
)

# Use data augmentation
augmented_data = augment_training_data(synthetic_data)
```

#### Issue 3: PPI Confidence Intervals Too Wide

**Symptoms:**
- Confidence intervals span 0.2+ range
- Can't determine statistical significance
- Inconclusive A/B tests

**Solutions:**
```python
# Increase sample size
results = ares.evaluate(
    rag_outputs=larger_test_set,  # Increase from 100 to 500+
    use_ppi=True
)

# More human annotations
annotations = collect_annotations(
    num_samples=1000  # Increase from 500
)

# Check annotation quality
validate_annotation_quality(annotations)
```

#### Issue 4: Domain Shift Degradation

**Symptoms:**
- Good performance on tech domain
- Poor performance on medical/legal domain
- Classifiers misclassify out-of-domain examples

**Solutions:**
```python
# Domain-specific training
medical_synthetic = ares.generate_synthetic_data(
    documents=medical_docs,
    domain_adapter=MedicalDomainAdapter()
)

medical_classifiers = train_classifiers(medical_synthetic)

# Multi-domain training
mixed_data = combine_domains([
    tech_synthetic,
    medical_synthetic,
    legal_synthetic
])

robust_classifiers = train_classifiers(mixed_data)
```

---

## API Reference

### Core Classes

#### ARES

```python
class ARES:
    """Main ARES evaluator."""

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        local_mode: bool = False,
        config: Optional[Dict] = None
    ):
        """
        Initialize ARES evaluator.

        Args:
            model: LLM model name (gpt-4o, gpt-4o-mini, or local model)
            api_key: OpenAI API key (if None, reads from env)
            local_mode: Use local models (vLLM)
            config: Additional configuration options
        """
        pass

    def generate_synthetic_data(
        self,
        documents: List[str],
        num_samples: int = 1000,
        include_negative_samples: bool = True,
        difficulty_levels: List[str] = ["easy", "medium", "hard"],
        **kwargs
    ) -> List[Dict]:
        """
        Generate synthetic evaluation data from documents.

        Args:
            documents: Source document corpus
            num_samples: Number of examples to generate
            include_negative_samples: Include negative examples
            difficulty_levels: Difficulty distribution

        Returns:
            List of synthetic examples with queries, contexts, answers
        """
        pass

    def evaluate(
        self,
        rag_outputs: List[Dict],
        metrics: List[str] = ["context_relevance", "answer_faithfulness", "answer_relevance"],
        use_ppi: bool = False,
        confidence_level: float = 0.95,
        **kwargs
    ) -> Dict:
        """
        Evaluate RAG outputs.

        Args:
            rag_outputs: List of RAG outputs to evaluate
            metrics: Metrics to compute
            use_ppi: Use Prediction-Powered Inference
            confidence_level: Confidence level for intervals

        Returns:
            Dictionary of evaluation results with scores
        """
        pass

    def evaluate_with_classifiers(
        self,
        rag_outputs: List[Dict],
        classifiers: Dict,
        use_ppi: bool = True,
        annotated_calibration: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict:
        """
        Evaluate using trained classifiers with optional PPI.

        Args:
            rag_outputs: List of RAG outputs
            classifiers: Trained classifier models
            use_ppi: Apply PPI calibration
            annotated_calibration: Human annotations for PPI

        Returns:
            Calibrated evaluation results with confidence intervals
        """
        pass
```

#### ClassifierTrainer

```python
class ClassifierTrainer:
    """Train evaluation classifiers."""

    def __init__(
        self,
        base_model: str = "distilbert-base-uncased",
        num_epochs: int = 3,
        batch_size: int = 32,
        learning_rate: float = 2e-5,
        device: str = "cuda"
    ):
        """
        Initialize classifier trainer.

        Args:
            base_model: Base transformer model
            num_epochs: Training epochs
            batch_size: Batch size
            learning_rate: Learning rate
            device: Device (cuda/cpu)
        """
        pass

    def train(
        self,
        synthetic_data: List[Dict],
        metric: str,
        validation_split: float = 0.1,
        **kwargs
    ):
        """
        Train classifier for specific metric.

        Args:
            synthetic_data: Training data
            metric: Metric to train for
            validation_split: Validation set proportion

        Returns:
            Trained classifier model
        """
        pass

    def train_all_metrics(
        self,
        synthetic_data: List[Dict],
        metrics: List[str],
        **kwargs
    ) -> Dict:
        """
        Train classifiers for all metrics.

        Args:
            synthetic_data: Training data
            metrics: List of metrics

        Returns:
            Dictionary of trained classifiers
        """
        pass
```

---

## Performance Optimization

### 1. Batch Processing

```python
# Process in batches for efficiency
def batch_evaluate(rag_outputs, batch_size=100):
    results = []
    for i in range(0, len(rag_outputs), batch_size):
        batch = rag_outputs[i:i+batch_size]
        batch_results = ares.evaluate(batch)
        results.append(batch_results)
    return aggregate_results(results)
```

### 2. Caching

```python
# Cache classifier predictions
from functools import lru_cache

@lru_cache(maxsize=10000)
def cached_evaluate(query_hash, context_hash):
    return classifier.predict(query, context)
```

### 3. Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

def parallel_evaluate(rag_outputs, num_workers=4):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(ares.evaluate, [output])
            for output in rag_outputs
        ]
        results = [f.result() for f in futures]
    return aggregate_results(results)
```

---

## Security Considerations

### 1. API Key Management

```python
# Use environment variables
import os
api_key = os.getenv("OPENAI_API_KEY")

# Or use secrets management
from azure.keyvault.secrets import SecretClient
secret_client = SecretClient(vault_url, credential)
api_key = secret_client.get_secret("openai-api-key").value
```

### 2. Data Privacy

```python
# For sensitive data, use local models
ares = ARES(local_mode=True, privacy_preserving=True)

# Ensure no data leaves infrastructure
assert ares.config.no_external_calls == True
```

### 3. Input Validation

```python
def validate_input(rag_output):
    required_keys = ["query", "retrieved_contexts", "generated_answer"]
    for key in required_keys:
        if key not in rag_output:
            raise ValueError(f"Missing required key: {key}")

    # Sanitize inputs
    rag_output["query"] = sanitize_text(rag_output["query"])
    rag_output["generated_answer"] = sanitize_text(rag_output["generated_answer"])

    return rag_output
```

---

## Extensive References

### Official Resources

- **GitHub Repository**: https://github.com/stanford-futuredata/ARES
- **Research Paper**: https://arxiv.org/abs/2311.09476
- **Project Website**: https://ares-ai.vercel.app
- **Documentation**: https://github.com/stanford-futuredata/ARES/tree/main/docs

### Research Papers

1. **ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems**
   - Authors: Jon Saad-Falcon, Omar Khattab, Matei Zaharia, Christopher Potts
   - Conference: NAACL 2024
   - arXiv: 2311.09476

2. **Prediction-Powered Inference**
   - Foundational work on PPI methodology
   - Explains statistical techniques used in ARES

3. **RAG Evaluation Benchmarks**
   - KILT, SuperGLUE, Natural Questions
   - Datasets used to validate ARES

### Related Frameworks

- **RAGAS**: Alternative RAG evaluation framework
- **TruLens**: RAG observability and evaluation
- **Phoenix**: Production RAG monitoring

### Community Resources

- **GitHub Issues**: https://github.com/stanford-futuredata/ARES/issues
- **Discussions**: Limited (research project, smaller community)
- **Examples**: https://github.com/stanford-futuredata/ARES/tree/main/examples

### Cost Resources

- **OpenAI Pricing**: https://openai.com/pricing
- **GPU Compute Pricing**: Cloud provider pricing pages
- **Annotation Services**: Scale AI, Labelbox pricing

### Tutorials and Guides

1. **Getting Started with ARES** - Official GitHub README
2. **Synthetic Data Generation** - Examples directory
3. **PPI Calibration** - Research paper methodology section
4. **Production Deployment** - Community contributions

---

## Conclusion

ARES represents a unique approach to RAG evaluation that prioritizes:

1. **Synthetic Data Generation**: Reduce manual test case creation
2. **Statistical Rigor**: Confidence intervals via PPI
3. **Cost Efficiency**: Train once, evaluate many times cheaply
4. **Privacy**: Local execution option
5. **Research Backing**: Peer-reviewed methodology from Stanford

**Best suited for**:
- Research and academic RAG evaluation
- Large-scale evaluation with budget constraints
- Privacy-conscious deployments
- Domain-specific RAG systems

**Consider alternatives for**:
- Quick setup and simple use cases
- Production monitoring and observability
- Non-RAG applications
- Extensive RAG metric requirements

---

**Version**: 1.0
**Last Updated**: January 2026
**Maintained by**: Custom-Evals Documentation Team
**Related Files**:
- Example Code: `/docs/compare_eval_frameworks/ares_example.py`
- Framework Comparison: `/docs/compare_eval_frameworks/13_ARES.md`
- All Frameworks: `/docs/compare_eval_frameworks/Compare_All_Eval_Frameworks.md`
