"""
LangChain RAG with Qdrant Example - Custom Evals Testing

This example demonstrates:
1. PDF processing and text extraction
2. Creating embeddings with LangChain
3. Storing vectors in Qdrant database
4. Building RAG (Retrieval-Augmented Generation) system
5. Evaluating RAG outputs with custom-evals (Faithfulness, Answer Relevancy)

Requirements:
- langchain
- langchain-openai
- qdrant-client
- pypdf or pypdf2
- sentence-transformers (optional for local embeddings)
"""

import os
import tempfile
from typing import List, Dict, Any
from pathlib import Path

try:
    from langchain.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain.vectorstores import Qdrant
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    print(f"⚠️  Missing dependencies: {e}")
    print("Install with: pip install langchain langchain-openai qdrant-client pypdf")

# Custom Evals imports
from custom.evals import (
    FaithfulnessEvaluator,
    AnswerRelevancyEvaluator,
    CoherenceEvaluator,
    RelevanceEvaluator,
    HallucinationEvaluator
)
from custom.evals.llm import LLM

# Optional: Initialize Phoenix tracing
try:
    from custom.evals import initialize_tracing
    initialize_tracing(phoenix_endpoint="http://localhost:6006/v1/traces")
    print("✅ Phoenix tracing enabled")
except:
    print("ℹ️  Phoenix tracing not available (optional)")


# ============================================================================
# STEP 1: PDF Processing and Document Loading
# ============================================================================

class PDFProcessor:
    """Process PDF documents for RAG."""

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def create_sample_pdf(self, filepath: str) -> str:
        """Create a sample PDF with AI/ML content."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            c = canvas.Canvas(filepath, pagesize=letter)
            width, height = letter

            # Page 1: Machine Learning
            y_position = height - 50
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y_position, "Machine Learning Overview")

            y_position -= 30
            c.setFont("Helvetica", 12)
            text = [
                "Machine Learning (ML) is a subset of artificial intelligence that enables",
                "systems to learn and improve from experience without being explicitly programmed.",
                "",
                "Key Concepts:",
                "- Supervised Learning: Training with labeled data",
                "- Unsupervised Learning: Finding patterns in unlabeled data",
                "- Reinforcement Learning: Learning through rewards and penalties",
                "",
                "Common Algorithms:",
                "- Linear Regression: For continuous predictions",
                "- Decision Trees: For classification and regression",
                "- Neural Networks: For complex pattern recognition",
                "- Support Vector Machines: For classification tasks",
            ]

            for line in text:
                c.drawString(50, y_position, line)
                y_position -= 20
                if y_position < 50:
                    c.showPage()
                    y_position = height - 50

            # Page 2: Deep Learning
            c.showPage()
            y_position = height - 50
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y_position, "Deep Learning")

            y_position -= 30
            c.setFont("Helvetica", 12)
            text = [
                "Deep Learning is a specialized subset of machine learning using neural networks",
                "with multiple layers. It excels at processing unstructured data like images,",
                "text, and audio.",
                "",
                "Architecture Types:",
                "- Convolutional Neural Networks (CNNs): For image processing",
                "- Recurrent Neural Networks (RNNs): For sequential data",
                "- Transformers: For natural language processing",
                "- Generative Adversarial Networks (GANs): For content generation",
                "",
                "Applications:",
                "- Computer Vision: Object detection, image classification",
                "- Natural Language Processing: Translation, sentiment analysis",
                "- Speech Recognition: Voice assistants, transcription",
                "- Autonomous Systems: Self-driving cars, robotics",
            ]

            for line in text:
                c.drawString(50, y_position, line)
                y_position -= 20

            # Page 3: RAG Systems
            c.showPage()
            y_position = height - 50
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y_position, "Retrieval-Augmented Generation")

            y_position -= 30
            c.setFont("Helvetica", 12)
            text = [
                "RAG (Retrieval-Augmented Generation) combines information retrieval with",
                "text generation to create more accurate and contextual responses.",
                "",
                "Components:",
                "- Document Store: Vector database for efficient retrieval",
                "- Retriever: Finds relevant documents based on query",
                "- Generator: LLM that creates responses using retrieved context",
                "",
                "Benefits:",
                "- Reduces hallucinations by grounding responses in source documents",
                "- Enables up-to-date information without retraining models",
                "- Provides source attribution for generated content",
                "- Improves accuracy for domain-specific questions",
                "",
                "Common Vector Databases: Qdrant, Pinecone, Weaviate, Chroma",
            ]

            for line in text:
                c.drawString(50, y_position, line)
                y_position -= 20

            c.save()
            return filepath

        except ImportError:
            # Fallback: Create text file if reportlab not available
            print("⚠️  reportlab not available, creating text file instead")
            text_content = """Machine Learning Overview

Machine Learning (ML) is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.

Key Concepts:
- Supervised Learning: Training with labeled data
- Unsupervised Learning: Finding patterns in unlabeled data
- Reinforcement Learning: Learning through rewards and penalties

Common Algorithms:
- Linear Regression: For continuous predictions
- Decision Trees: For classification and regression
- Neural Networks: For complex pattern recognition
- Support Vector Machines: For classification tasks

Deep Learning

Deep Learning is a specialized subset of machine learning using neural networks with multiple layers. It excels at processing unstructured data like images, text, and audio.

Architecture Types:
- Convolutional Neural Networks (CNNs): For image processing
- Recurrent Neural Networks (RNNs): For sequential data
- Transformers: For natural language processing
- Generative Adversarial Networks (GANs): For content generation

Applications:
- Computer Vision: Object detection, image classification
- Natural Language Processing: Translation, sentiment analysis
- Speech Recognition: Voice assistants, transcription
- Autonomous Systems: Self-driving cars, robotics

Retrieval-Augmented Generation

RAG (Retrieval-Augmented Generation) combines information retrieval with text generation to create more accurate and contextual responses.

Components:
- Document Store: Vector database for efficient retrieval
- Retriever: Finds relevant documents based on query
- Generator: LLM that creates responses using retrieved context

Benefits:
- Reduces hallucinations by grounding responses in source documents
- Enables up-to-date information without retraining models
- Provides source attribution for generated content
- Improves accuracy for domain-specific questions

Common Vector Databases: Qdrant, Pinecone, Weaviate, Chroma
"""
            # Save as .txt instead of .pdf
            txt_filepath = filepath.replace('.pdf', '.txt')
            with open(txt_filepath, 'w') as f:
                f.write(text_content)
            return txt_filepath

    def load_and_split_pdf(self, pdf_path: str) -> List[Any]:
        """Load PDF and split into chunks."""
        # Check if it's a text file (fallback)
        if pdf_path.endswith('.txt'):
            with open(pdf_path, 'r') as f:
                content = f.read()

            # Create a simple document object
            from langchain.schema import Document
            doc = Document(page_content=content, metadata={"source": pdf_path})
            chunks = self.text_splitter.split_documents([doc])
            return chunks

        # Load PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        # Split into chunks
        chunks = self.text_splitter.split_documents(documents)

        print(f"📄 Loaded {len(documents)} pages, split into {len(chunks)} chunks")
        return chunks


# ============================================================================
# STEP 2: LangChain RAG with Qdrant
# ============================================================================

class LangChainQdrantRAG:
    """RAG system using LangChain and Qdrant."""

    def __init__(
        self,
        collection_name: str = "ml_documents",
        qdrant_path: str = "./qdrant_data",
        use_local: bool = True
    ):
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("Required packages not installed")

        self.collection_name = collection_name

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Initialize Qdrant client
        if use_local:
            self.qdrant_client = QdrantClient(path=qdrant_path)
        else:
            # For Qdrant Cloud
            self.qdrant_client = QdrantClient(
                url=os.getenv("QDRANT_URL"),
                api_key=os.getenv("QDRANT_API_KEY")
            )

        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.vectorstore = None
        self.qa_chain = None

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "faithfulness": FaithfulnessEvaluator(eval_llm),
            "answer_relevancy": AnswerRelevancyEvaluator(eval_llm),
            "coherence": CoherenceEvaluator(eval_llm),
            "hallucination": HallucinationEvaluator(eval_llm)
        }

    def index_documents(self, documents: List[Any]) -> None:
        """Index documents into Qdrant."""
        print(f"\n📥 Indexing {len(documents)} documents into Qdrant...")

        # Create or recreate collection
        try:
            self.qdrant_client.delete_collection(self.collection_name)
        except:
            pass

        # Create Qdrant vectorstore
        self.vectorstore = Qdrant.from_documents(
            documents,
            self.embeddings,
            path="./qdrant_data",
            collection_name=self.collection_name,
        )

        print(f"✅ Indexed {len(documents)} documents")

    def create_qa_chain(self) -> None:
        """Create QA chain with custom prompt."""
        if not self.vectorstore:
            raise ValueError("Documents must be indexed first")

        # Custom prompt template
        prompt_template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Always cite the source of your information when possible.

Context:
{context}

Question: {question}

Answer: """

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

        print("✅ QA chain created")

    def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system."""
        if not self.qa_chain:
            raise ValueError("QA chain must be created first")

        try:
            result = self.qa_chain({"query": question})

            # Extract source documents
            source_docs = result.get("source_documents", [])
            context = "\n\n".join([doc.page_content for doc in source_docs])

            return {
                "question": question,
                "answer": result["result"],
                "source_documents": source_docs,
                "context": context,
                "success": True
            }

        except Exception as e:
            return {
                "question": question,
                "answer": str(e),
                "success": False,
                "error": str(e)
            }

    def evaluate(self, question: str, answer: str, context: str) -> Dict[str, Any]:
        """Evaluate RAG response with multiple metrics."""
        scores = {}

        # Faithfulness: Is the answer grounded in the context?
        try:
            faithfulness_score = self.evaluators["faithfulness"].evaluate({
                "input": question,
                "output": answer,
                "context": context
            })
            scores["faithfulness"] = faithfulness_score
        except Exception as e:
            print(f"Warning: Faithfulness evaluation failed: {e}")

        # Answer Relevancy: Does the answer address the question?
        try:
            relevancy_score = self.evaluators["answer_relevancy"].evaluate({
                "input": question,
                "output": answer
            })
            scores["answer_relevancy"] = relevancy_score
        except Exception as e:
            print(f"Warning: Answer relevancy evaluation failed: {e}")

        # Coherence
        try:
            coherence_score = self.evaluators["coherence"].evaluate({
                "input": question,
                "output": answer
            })
            scores["coherence"] = coherence_score
        except Exception as e:
            print(f"Warning: Coherence evaluation failed: {e}")

        # Hallucination check
        try:
            hallucination_score = self.evaluators["hallucination"].evaluate({
                "input": question,
                "output": answer,
                "context": context
            })
            scores["hallucination"] = hallucination_score
        except Exception as e:
            print(f"Warning: Hallucination evaluation failed: {e}")

        return scores


# ============================================================================
# STEP 3: Testing Functions
# ============================================================================

def test_pdf_processing():
    """Test PDF processing and chunking."""
    print("\n" + "="*80)
    print("TEST 1: PDF Processing and Chunking")
    print("="*80)

    processor = PDFProcessor()

    # Create sample PDF
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        pdf_path = tmp.name

    print(f"\n📝 Creating sample PDF...")
    pdf_path = processor.create_sample_pdf(pdf_path)

    print(f"✅ Sample document created: {pdf_path}")

    # Load and split
    chunks = processor.load_and_split_pdf(pdf_path)

    print(f"\n📊 Chunking Results:")
    print(f"  • Total chunks: {len(chunks)}")
    print(f"  • First chunk preview: {chunks[0].page_content[:200]}...")

    return pdf_path, chunks


def test_rag_system_setup():
    """Test RAG system setup and indexing."""
    print("\n" + "="*80)
    print("TEST 2: RAG System Setup and Indexing")
    print("="*80)

    # Process PDF
    processor = PDFProcessor()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        pdf_path = tmp.name
    pdf_path = processor.create_sample_pdf(pdf_path)
    chunks = processor.load_and_split_pdf(pdf_path)

    # Create RAG system
    rag = LangChainQdrantRAG(collection_name="test_ml_docs")

    # Index documents
    rag.index_documents(chunks)

    # Create QA chain
    rag.create_qa_chain()

    print("\n✅ RAG system ready")

    return rag


def test_basic_queries():
    """Test basic RAG queries."""
    print("\n" + "="*80)
    print("TEST 3: Basic RAG Queries")
    print("="*80)

    rag = test_rag_system_setup()

    test_questions = [
        "What is machine learning?",
        "What are the different types of neural networks?",
        "What is RAG and what are its benefits?",
        "What are common vector databases mentioned?"
    ]

    results = []

    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Query {i}/{len(test_questions)} ---")
        print(f"❓ Question: {question}")

        result = rag.query(question)

        if result["success"]:
            answer = result["answer"]
            print(f"💡 Answer: {answer[:300]}...")
            print(f"📚 Sources: {len(result['source_documents'])} documents")

            results.append(result)
        else:
            print(f"❌ Error: {result.get('error')}")

    return results


def test_rag_evaluation():
    """Test RAG evaluation with custom metrics."""
    print("\n" + "="*80)
    print("TEST 4: RAG Evaluation - Faithfulness & Relevancy")
    print("="*80)

    rag = test_rag_system_setup()

    test_cases = [
        {
            "question": "What is supervised learning?",
            "description": "Should retrieve definition from ML section"
        },
        {
            "question": "What are CNNs used for?",
            "description": "Should retrieve info about convolutional neural networks"
        },
        {
            "question": "How does RAG reduce hallucinations?",
            "description": "Should retrieve RAG benefits section"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        question = test_case["question"]

        print(f"\n--- Evaluation {i}/{len(test_cases)} ---")
        print(f"❓ Question: {question}")
        print(f"📋 Description: {test_case['description']}")

        # Query RAG
        result = rag.query(question)

        if not result["success"]:
            print(f"❌ Query failed: {result.get('error')}")
            continue

        answer = result["answer"]
        context = result["context"]

        print(f"💡 Answer: {answer[:250]}...")

        # Evaluate
        scores = rag.evaluate(question, answer, context)

        print(f"\n📊 Evaluation Scores:")
        for metric, score in scores.items():
            print(f"  • {metric.replace('_', ' ').title()}: {score.label} ({score.score:.2f})")
            if score.explanation:
                print(f"    {score.explanation[:150]}...")


def test_rag_quality_gates():
    """Test RAG with quality gates."""
    print("\n" + "="*80)
    print("TEST 5: RAG Quality Gates")
    print("="*80)

    rag = test_rag_system_setup()

    # Quality thresholds
    QUALITY_THRESHOLDS = {
        "faithfulness": 0.8,      # High bar for factual accuracy
        "answer_relevancy": 0.7,  # Answer should be relevant
        "coherence": 0.7,          # Answer should be coherent
    }

    test_questions = [
        "What is deep learning?",
        "What types of learning are mentioned in machine learning?",
        "What are the components of a RAG system?"
    ]

    print(f"\n🚦 Quality Thresholds:")
    for metric, threshold in QUALITY_THRESHOLDS.items():
        print(f"  • {metric.replace('_', ' ').title()}: >= {threshold}")

    all_passed = True
    results = []

    for i, question in enumerate(test_questions, 1):
        print(f"\n[{i}/{len(test_questions)}] Question: {question}")

        # Query
        result = rag.query(question)

        if not result["success"]:
            print(f"❌ Query failed")
            all_passed = False
            continue

        # Evaluate
        scores = rag.evaluate(question, result["answer"], result["context"])

        # Check quality gates
        passed_gates = True
        for metric, threshold in QUALITY_THRESHOLDS.items():
            if metric not in scores:
                continue

            score_value = scores[metric].score
            passed = score_value >= threshold
            status = "✅" if passed else "❌"

            print(f"  {status} {metric}: {score_value:.2f} >= {threshold}")

            if not passed:
                passed_gates = False
                all_passed = False

        results.append({
            "question": question,
            "passed": passed_gates,
            "scores": scores
        })

    # Summary
    passed_count = sum(1 for r in results if r["passed"])
    print(f"\n{'='*80}")
    print(f"🚦 Quality Gate Summary:")
    print(f"  • Passed: {passed_count}/{len(results)}")
    print(f"  • Failed: {len(results) - passed_count}/{len(results)}")

    if all_passed:
        print(f"\n✅ All quality gates PASSED - RAG system ready!")
    else:
        print(f"\n⚠️  Some quality gates FAILED")


def test_rag_with_ground_truth():
    """Test RAG with expected answers."""
    print("\n" + "="*80)
    print("TEST 6: RAG with Ground Truth Evaluation")
    print("="*80)

    rag = test_rag_system_setup()

    test_cases = [
        {
            "question": "What does RAG stand for?",
            "expected_keywords": ["retrieval", "augmented", "generation"],
            "description": "Should contain RAG acronym expansion"
        },
        {
            "question": "Name a common vector database",
            "expected_keywords": ["qdrant", "pinecone", "weaviate", "chroma"],
            "description": "Should mention at least one vector database"
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        question = test_case["question"]
        expected_keywords = test_case["expected_keywords"]

        print(f"\n--- Test {i}/{len(test_cases)} ---")
        print(f"❓ Question: {question}")
        print(f"✅ Expected Keywords: {', '.join(expected_keywords)}")

        # Query
        result = rag.query(question)

        if not result["success"]:
            print(f"❌ Query failed")
            continue

        answer = result["answer"]
        print(f"💡 Answer: {answer}")

        # Check for expected keywords
        found_keywords = [
            kw for kw in expected_keywords
            if kw.lower() in answer.lower()
        ]

        has_expected = len(found_keywords) > 0
        print(f"\n📊 Ground Truth Check:")
        print(f"  • Keywords found: {', '.join(found_keywords) if found_keywords else 'None'}")
        print(f"  • Status: {'✅ PASS' if has_expected else '❌ FAIL'}")

        results.append({
            "question": question,
            "answer": answer,
            "expected_keywords": expected_keywords,
            "found_keywords": found_keywords,
            "passed": has_expected
        })

    # Summary
    passed_count = sum(1 for r in results if r["passed"])
    print(f"\n📊 Summary:")
    print(f"  • Ground Truth Checks Passed: {passed_count}/{len(results)}")


# ============================================================================
# STEP 4: Main Execution
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🚀 LangChain RAG with Qdrant - Custom Evals Testing")
    print("="*80)

    if not LANGCHAIN_AVAILABLE:
        print("\n❌ Required packages not installed")
        print("Install with: pip install langchain langchain-openai qdrant-client pypdf reportlab")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY environment variable not set")
        print("Set with: export OPENAI_API_KEY='your-key'")
        return

    try:
        # Test 1: PDF processing
        test_pdf_processing()

        # Test 2: RAG setup
        test_rag_system_setup()

        # Test 3: Basic queries
        test_basic_queries()

        # Test 4: RAG evaluation
        test_rag_evaluation()

        # Test 5: Quality gates
        test_rag_quality_gates()

        # Test 6: Ground truth
        test_rag_with_ground_truth()

        print("\n" + "="*80)
        print("✅ All tests completed successfully!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
