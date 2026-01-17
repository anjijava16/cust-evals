"""
LlamaIndex RAG with Qdrant Example - Custom Evals Testing

This example demonstrates:
1. PDF processing with LlamaIndex
2. Creating embeddings and indexes
3. Storing vectors in Qdrant database
4. Building RAG query engine
5. Evaluating RAG outputs with custom-evals (Faithfulness, Answer Relevancy)

Requirements:
- llama-index
- llama-index-vector-stores-qdrant
- llama-index-embeddings-openai
- qdrant-client
- pypdf
"""

import os
import tempfile
from typing import List, Dict, Any
from pathlib import Path

try:
    from llama_index.core import (
        VectorStoreIndex,
        SimpleDirectoryReader,
        StorageContext,
        Settings,
        Document
    )
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.llms.openai import OpenAI
    from llama_index.vector_stores.qdrant import QdrantVectorStore
    from qdrant_client import QdrantClient
    LLAMAINDEX_AVAILABLE = True
except ImportError as e:
    LLAMAINDEX_AVAILABLE = False
    print(f"⚠️  Missing dependencies: {e}")
    print("Install with: pip install llama-index llama-index-vector-stores-qdrant llama-index-embeddings-openai qdrant-client pypdf")

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
# STEP 1: Document Preparation
# ============================================================================

class LlamaIndexDocumentProcessor:
    """Process documents for LlamaIndex RAG."""

    def create_sample_documents(self, temp_dir: str) -> str:
        """Create sample documents about AI/ML topics."""
        documents = {
            "natural_language_processing.txt": """
Natural Language Processing (NLP)

Natural Language Processing is a branch of artificial intelligence that focuses on the
interaction between computers and human language. It enables machines to understand,
interpret, and generate human language in a valuable way.

Key NLP Tasks:
1. Text Classification: Categorizing text into predefined classes
2. Named Entity Recognition (NER): Identifying entities like names, locations, organizations
3. Sentiment Analysis: Determining the emotional tone of text
4. Machine Translation: Translating text between languages
5. Question Answering: Providing answers to natural language questions
6. Text Summarization: Creating concise summaries of longer texts

Popular NLP Models:
- BERT (Bidirectional Encoder Representations from Transformers)
- GPT (Generative Pre-trained Transformer) series
- T5 (Text-to-Text Transfer Transformer)
- RoBERTa (Robustly Optimized BERT)

NLP is widely used in chatbots, virtual assistants, search engines, and content moderation.
""",

            "computer_vision.txt": """
Computer Vision

Computer Vision is a field of artificial intelligence that enables computers to derive
meaningful information from digital images, videos, and other visual inputs. It aims to
automate tasks that the human visual system can perform.

Key Computer Vision Tasks:
1. Image Classification: Categorizing entire images into classes
2. Object Detection: Identifying and locating objects within images
3. Semantic Segmentation: Classifying each pixel in an image
4. Instance Segmentation: Identifying individual object instances
5. Face Recognition: Identifying or verifying faces in images
6. Pose Estimation: Detecting the position and orientation of objects

Popular Architectures:
- ResNet: Deep residual networks for image recognition
- YOLO (You Only Look Once): Real-time object detection
- U-Net: Semantic segmentation architecture
- Vision Transformers (ViT): Transformer-based image models

Applications include autonomous vehicles, medical imaging, surveillance, and augmented reality.
""",

            "vector_databases.txt": """
Vector Databases and Embeddings

Vector databases are specialized databases designed to store and query high-dimensional
vector embeddings efficiently. They are essential for modern AI applications, particularly
in semantic search and retrieval-augmented generation (RAG).

What are Embeddings?
Embeddings are dense vector representations of data (text, images, audio) that capture
semantic meaning. Similar items have similar embeddings in the vector space.

Popular Vector Databases:
1. Qdrant: Open-source vector database with rich filtering
2. Pinecone: Managed vector database service
3. Weaviate: Open-source vector search engine with GraphQL
4. Chroma: Lightweight embedding database
5. Milvus: Highly scalable open-source vector database

Key Features:
- Similarity Search: Finding nearest neighbors using metrics like cosine similarity
- Filtering: Combining vector search with metadata filtering
- Hybrid Search: Combining dense and sparse retrieval
- Scalability: Handling billions of vectors efficiently

Use Cases:
- Semantic Search: Finding relevant documents based on meaning
- Recommendation Systems: Finding similar items
- RAG Systems: Retrieving context for language models
- Anomaly Detection: Identifying outliers in vector space
""",

            "rag_systems.txt": """
Retrieval-Augmented Generation (RAG) Systems

RAG is a technique that enhances large language models by incorporating external knowledge
through a retrieval mechanism. It combines the benefits of retrieval-based and generation-based
approaches to create more accurate and factual responses.

RAG Architecture Components:

1. Document Store:
   - Vector database storing document embeddings
   - Enables efficient semantic search
   - Supports metadata filtering

2. Retriever:
   - Converts queries to embeddings
   - Finds relevant documents using similarity search
   - Can use hybrid retrieval (dense + sparse)

3. Generator:
   - Large language model (LLM)
   - Uses retrieved context to generate responses
   - Grounds answers in source documents

Benefits of RAG:
- Reduced Hallucinations: Responses grounded in actual documents
- Up-to-date Information: No need to retrain models for new data
- Source Attribution: Can cite where information came from
- Domain Adaptation: Easy to add domain-specific knowledge
- Cost Effective: Cheaper than fine-tuning large models

Common RAG Frameworks:
- LangChain: Modular framework for LLM applications
- LlamaIndex: Data framework for LLM applications
- Haystack: End-to-end NLP framework

RAG is widely used in question answering systems, chatbots, customer support, and research assistants.
"""
        }

        # Create temporary directory and files
        Path(temp_dir).mkdir(exist_ok=True)

        for filename, content in documents.items():
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.strip())

        print(f"✅ Created {len(documents)} sample documents in {temp_dir}")
        return temp_dir

    def load_documents(self, directory: str) -> List[Document]:
        """Load documents from directory."""
        reader = SimpleDirectoryReader(directory)
        documents = reader.load_data()

        print(f"📄 Loaded {len(documents)} documents")
        return documents


# ============================================================================
# STEP 2: LlamaIndex RAG with Qdrant
# ============================================================================

class LlamaIndexQdrantRAG:
    """RAG system using LlamaIndex and Qdrant."""

    def __init__(
        self,
        collection_name: str = "llamaindex_docs",
        qdrant_path: str = "./llamaindex_qdrant_data"
    ):
        if not LLAMAINDEX_AVAILABLE:
            raise ImportError("Required packages not installed")

        self.collection_name = collection_name
        self.qdrant_path = qdrant_path

        # Configure LlamaIndex settings
        Settings.embed_model = OpenAIEmbedding(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )

        Settings.llm = OpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        Settings.node_parser = SentenceSplitter(
            chunk_size=1024,
            chunk_overlap=200
        )

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(path=qdrant_path)

        self.index = None
        self.query_engine = None

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "faithfulness": FaithfulnessEvaluator(eval_llm),
            "answer_relevancy": AnswerRelevancyEvaluator(eval_llm),
            "coherence": CoherenceEvaluator(eval_llm),
            "hallucination": HallucinationEvaluator(eval_llm)
        }

    def index_documents(self, documents: List[Document]) -> None:
        """Index documents into Qdrant using LlamaIndex."""
        print(f"\n📥 Indexing {len(documents)} documents...")

        # Create Qdrant vector store
        vector_store = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=self.collection_name
        )

        # Create storage context
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )

        # Create index
        self.index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )

        print(f"✅ Indexed {len(documents)} documents")

    def create_query_engine(self, similarity_top_k: int = 3) -> None:
        """Create query engine."""
        if not self.index:
            raise ValueError("Documents must be indexed first")

        self.query_engine = self.index.as_query_engine(
            similarity_top_k=similarity_top_k,
            response_mode="compact"
        )

        print(f"✅ Query engine created (retrieving top {similarity_top_k} documents)")

    def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system."""
        if not self.query_engine:
            raise ValueError("Query engine must be created first")

        try:
            response = self.query_engine.query(question)

            # Extract source nodes
            source_nodes = response.source_nodes if hasattr(response, 'source_nodes') else []

            # Build context from source nodes
            context_parts = []
            for node in source_nodes:
                if hasattr(node, 'text'):
                    context_parts.append(node.text)
                elif hasattr(node, 'node') and hasattr(node.node, 'text'):
                    context_parts.append(node.node.text)

            context = "\n\n".join(context_parts)

            return {
                "question": question,
                "answer": str(response),
                "source_nodes": source_nodes,
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

        # Faithfulness
        try:
            faithfulness_score = self.evaluators["faithfulness"].evaluate({
                "input": question,
                "output": answer,
                "context": context
            })
            scores["faithfulness"] = faithfulness_score
        except Exception as e:
            print(f"Warning: Faithfulness evaluation failed: {e}")

        # Answer Relevancy
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

        # Hallucination
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

def test_document_loading():
    """Test document loading and processing."""
    print("\n" + "="*80)
    print("TEST 1: Document Loading and Processing")
    print("="*80)

    processor = LlamaIndexDocumentProcessor()

    # Create sample documents
    with tempfile.TemporaryDirectory() as temp_dir:
        doc_dir = processor.create_sample_documents(temp_dir)

        # Load documents
        documents = processor.load_documents(doc_dir)

        print(f"\n📊 Document Summary:")
        for i, doc in enumerate(documents, 1):
            print(f"  {i}. {doc.metadata.get('file_name', 'Unknown')}: {len(doc.text)} characters")

        return doc_dir, documents


def test_rag_setup():
    """Test RAG system setup."""
    print("\n" + "="*80)
    print("TEST 2: LlamaIndex RAG Setup")
    print("="*80)

    processor = LlamaIndexDocumentProcessor()

    # Create and load documents
    with tempfile.TemporaryDirectory() as temp_dir:
        doc_dir = processor.create_sample_documents(temp_dir)
        documents = processor.load_documents(doc_dir)

        # Create RAG system
        rag = LlamaIndexQdrantRAG(collection_name="test_llamaindex")

        # Index documents
        rag.index_documents(documents)

        # Create query engine
        rag.create_query_engine(similarity_top_k=2)

        print("\n✅ RAG system ready")

        return rag


def test_basic_queries():
    """Test basic RAG queries."""
    print("\n" + "="*80)
    print("TEST 3: Basic RAG Queries")
    print("="*80)

    rag = test_rag_setup()

    test_questions = [
        "What is Natural Language Processing?",
        "What are popular computer vision architectures?",
        "What is the purpose of vector databases?",
        "What are the components of a RAG system?"
    ]

    results = []

    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Query {i}/{len(test_questions)} ---")
        print(f"❓ Question: {question}")

        result = rag.query(question)

        if result["success"]:
            answer = result["answer"]
            print(f"💡 Answer: {answer[:300]}...")
            print(f"📚 Retrieved: {len(result['source_nodes'])} source chunks")

            results.append(result)
        else:
            print(f"❌ Error: {result.get('error')}")

    return results


def test_rag_evaluation():
    """Test RAG evaluation with custom metrics."""
    print("\n" + "="*80)
    print("TEST 4: RAG Evaluation - Faithfulness & Relevancy")
    print("="*80)

    rag = test_rag_setup()

    test_cases = [
        {
            "question": "What NLP tasks are mentioned?",
            "description": "Should retrieve NLP tasks from document"
        },
        {
            "question": "What are the benefits of RAG systems?",
            "description": "Should retrieve RAG benefits"
        },
        {
            "question": "Name some vector databases",
            "description": "Should list vector databases"
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


def test_quality_gates():
    """Test RAG with quality gates."""
    print("\n" + "="*80)
    print("TEST 5: RAG Quality Gates")
    print("="*80)

    rag = test_rag_setup()

    # Quality thresholds
    QUALITY_THRESHOLDS = {
        "faithfulness": 0.8,
        "answer_relevancy": 0.7,
        "coherence": 0.7
    }

    test_questions = [
        "What is computer vision?",
        "What are embeddings?",
        "What are common RAG frameworks?"
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
        print(f"\n✅ All quality gates PASSED!")
    else:
        print(f"\n⚠️  Some quality gates FAILED")


def test_multi_document_reasoning():
    """Test RAG with questions requiring multiple documents."""
    print("\n" + "="*80)
    print("TEST 6: Multi-Document Reasoning")
    print("="*80)

    rag = test_rag_setup()

    test_cases = [
        {
            "question": "How do vector databases support RAG systems?",
            "description": "Requires info from both vector DB and RAG documents",
            "expected_topics": ["vector", "rag", "embeddings"]
        },
        {
            "question": "What AI techniques are used in modern applications?",
            "description": "Should synthesize info from NLP and CV documents",
            "expected_topics": ["nlp", "computer vision", "applications"]
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        question = test_case["question"]

        print(f"\n--- Test {i}/{len(test_cases)} ---")
        print(f"❓ Question: {question}")
        print(f"📋 Description: {test_case['description']}")

        # Query
        result = rag.query(question)

        if not result["success"]:
            print(f"❌ Query failed")
            continue

        answer = result["answer"]
        print(f"💡 Answer: {answer[:350]}...")

        # Check if answer covers expected topics
        answer_lower = answer.lower()
        topics_covered = [
            topic for topic in test_case["expected_topics"]
            if topic.lower() in answer_lower
        ]

        print(f"\n📊 Coverage Analysis:")
        print(f"  • Expected topics: {', '.join(test_case['expected_topics'])}")
        print(f"  • Topics covered: {', '.join(topics_covered) if topics_covered else 'None'}")
        print(f"  • Coverage: {len(topics_covered)}/{len(test_case['expected_topics'])}")

        # Evaluate
        scores = rag.evaluate(question, answer, result["context"])
        print(f"\n📊 Quality Scores:")
        for metric, score in scores.items():
            print(f"  • {metric}: {score.label} ({score.score:.2f})")


def test_batch_evaluation():
    """Test batch evaluation for regression testing."""
    print("\n" + "="*80)
    print("TEST 7: Batch Evaluation - Regression Testing")
    print("="*80)

    rag = test_rag_setup()

    test_questions = [
        "What is NLP?",
        "What is semantic segmentation?",
        "What databases are good for embeddings?",
        "What are the benefits of RAG?",
        "What is BERT?",
        "What is YOLO?",
        "What is similarity search?",
        "What frameworks support RAG?"
    ]

    print(f"\n📋 Running batch evaluation on {len(test_questions)} queries...\n")

    batch_results = []

    for i, question in enumerate(test_questions, 1):
        print(f"[{i}/{len(test_questions)}] Processing: {question[:50]}...")

        # Query
        result = rag.query(question)

        if not result["success"]:
            batch_results.append({
                "question": question,
                "success": False
            })
            continue

        # Evaluate
        scores = rag.evaluate(question, result["answer"], result["context"])

        batch_results.append({
            "question": question,
            "answer": result["answer"],
            "success": True,
            "faithfulness": scores.get("faithfulness", {}).score if scores.get("faithfulness") else 0,
            "answer_relevancy": scores.get("answer_relevancy", {}).score if scores.get("answer_relevancy") else 0,
            "coherence": scores.get("coherence", {}).score if scores.get("coherence") else 0
        })

    # Calculate statistics
    successful = [r for r in batch_results if r["success"]]
    success_count = len(successful)

    if success_count > 0:
        avg_faithfulness = sum(r["faithfulness"] for r in successful) / success_count
        avg_relevancy = sum(r["answer_relevancy"] for r in successful) / success_count
        avg_coherence = sum(r["coherence"] for r in successful) / success_count

        print(f"\n{'='*80}")
        print(f"📊 Batch Evaluation Results:")
        print(f"  • Total Queries: {len(test_questions)}")
        print(f"  • Successful: {success_count}/{len(test_questions)}")
        print(f"  • Success Rate: {success_count/len(test_questions):.1%}")
        print(f"  • Average Faithfulness: {avg_faithfulness:.2f}")
        print(f"  • Average Answer Relevancy: {avg_relevancy:.2f}")
        print(f"  • Average Coherence: {avg_coherence:.2f}")


# ============================================================================
# STEP 4: Main Execution
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🚀 LlamaIndex RAG with Qdrant - Custom Evals Testing")
    print("="*80)

    if not LLAMAINDEX_AVAILABLE:
        print("\n❌ Required packages not installed")
        print("Install with: pip install llama-index llama-index-vector-stores-qdrant llama-index-embeddings-openai qdrant-client pypdf")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY environment variable not set")
        print("Set with: export OPENAI_API_KEY='your-key'")
        return

    try:
        # Test 1: Document loading
        test_document_loading()

        # Test 2: RAG setup
        test_rag_setup()

        # Test 3: Basic queries
        test_basic_queries()

        # Test 4: Evaluation
        test_rag_evaluation()

        # Test 5: Quality gates
        test_quality_gates()

        # Test 6: Multi-document reasoning
        test_multi_document_reasoning()

        # Test 7: Batch evaluation
        test_batch_evaluation()

        print("\n" + "="*80)
        print("✅ All tests completed successfully!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
