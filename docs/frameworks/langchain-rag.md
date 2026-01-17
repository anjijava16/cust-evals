# LangChain RAG with Qdrant - Document Q&A System

## Overview

**LangChain RAG** demonstrates building a Retrieval-Augmented Generation (RAG) system using LangChain for orchestration and Qdrant as the vector database for semantic search.

**Key Features**:
- PDF document processing
- OpenAI embeddings integration
- Qdrant vector database
- RetrievalQA chains
- RAG-specific evaluation (Faithfulness, Answer Relevancy)
- Production-ready architecture

**Example File**: `examples/rag_langchain_qdrant.py`

---

## Installation

```bash
pip install langchain langchain-openai qdrant-client pypdf reportlab
```

---

## Quick Start

### Simple RAG System

```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA

# 1. Load documents
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# 3. Create embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 4. Create vector store
vectorstore = Qdrant.from_documents(
    documents=chunks,
    embedding=embeddings,
    path="./qdrant_data",
    collection_name="documents"
)

# 5. Create QA chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# 6. Ask questions
response = qa_chain.invoke({"query": "What is machine learning?"})
print(response["result"])
```

---

## PDF Processing

### Create and Process PDFs

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create sample PDF
def create_sample_pdf(filepath: str):
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Machine Learning Overview")

    c.setFont("Helvetica", 12)
    c.drawString(50, 720, "Machine Learning is a subset of AI...")
    c.drawString(50, 700, "Key concepts include supervised learning,")
    c.drawString(50, 680, "unsupervised learning, and reinforcement learning.")

    c.save()

create_sample_pdf("ml_guide.pdf")

# Load and process
from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("ml_guide.pdf")
documents = loader.load()

print(f"Loaded {len(documents)} pages")
for i, doc in enumerate(documents):
    print(f"Page {i+1}: {len(doc.page_content)} characters")
```

---

## Text Chunking

### Optimal Chunking Strategy

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configure chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,          # Characters per chunk
    chunk_overlap=200,        # Overlap between chunks
    length_function=len,
    separators=["\n\n", "\n", " ", ""]  # Split hierarchy
)

# Split documents
chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")
for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i+1}:")
    print(f"Content: {chunk.page_content[:100]}...")
    print(f"Metadata: {chunk.metadata}")
```

---

## Vector Store Setup

### Qdrant Configuration

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings

# Initialize embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536  # Default for text-embedding-3-small
)

# Option 1: In-memory Qdrant
vectorstore = Qdrant.from_documents(
    documents=chunks,
    embedding=embeddings,
    location=":memory:",
    collection_name="documents"
)

# Option 2: Persistent local storage
vectorstore = Qdrant.from_documents(
    documents=chunks,
    embedding=embeddings,
    path="./qdrant_data",
    collection_name="documents"
)

# Option 3: Remote Qdrant server
client = QdrantClient(url="http://localhost:6333")
vectorstore = Qdrant(
    client=client,
    collection_name="documents",
    embeddings=embeddings
)
```

---

## Retrieval Strategies

### Configure Retrieval

```python
# Basic retrieval (top-k)
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Return top 3 chunks
)

# Maximum Marginal Relevance (MMR) - diverse results
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 10,  # Fetch 10, return diverse 3
        "lambda_mult": 0.5  # Diversity vs relevance balance
    }
)

# Similarity with score threshold
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.7,  # Minimum similarity score
        "k": 5
    }
)

# Use retriever
docs = retriever.get_relevant_documents("What is deep learning?")
for doc in docs:
    print(f"Content: {doc.page_content[:200]}")
```

---

## QA Chain Types

### Different Chain Strategies

```python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 1. Stuff Chain (default) - all docs in one prompt
qa_stuff = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

# 2. Map-Reduce - process docs separately, then combine
qa_map_reduce = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="map_reduce",
    retriever=retriever
)

# 3. Refine - iteratively refine answer with each doc
qa_refine = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="refine",
    retriever=retriever
)

# Use chain
response = qa_stuff.invoke({"query": "What are neural networks?"})
print(response["result"])
```

---

## Custom Prompts

### Customize RAG Prompts

```python
from langchain.prompts import PromptTemplate

# Custom QA prompt
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer concise.

Context: {context}

Question: {question}

Helpful Answer:"""

QA_PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

# Use custom prompt
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": QA_PROMPT}
)
```

---

## RAG Evaluation with Custom-Evals

### Faithfulness and Answer Relevancy

```python
from custom.evals import (
    FaithfulnessEvaluator,
    AnswerRelevancyEvaluator,
    CoherenceEvaluator,
    HallucinationEvaluator
)
from custom.evals.llm import LLM

# Query RAG system
query = "What is machine learning?"
response = qa_chain.invoke({"query": query})
answer = response["result"]

# Get retrieved context
docs = retriever.get_relevant_documents(query)
context = "\n".join([doc.page_content for doc in docs])

# Initialize evaluators
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

# RAG-specific metrics
faithfulness = FaithfulnessEvaluator(eval_llm)
faith_score = faithfulness.evaluate({
    "input": query,
    "output": answer,
    "context": context
})

answer_rel = AnswerRelevancyEvaluator(eval_llm)
rel_score = answer_rel.evaluate({
    "input": query,
    "output": answer
})

# General metrics
coherence = CoherenceEvaluator(eval_llm)
coh_score = coherence.evaluate({
    "input": query,
    "output": answer
})

hallucination = HallucinationEvaluator(eval_llm)
hall_score = hallucination.evaluate({
    "input": query,
    "output": answer,
    "context": context
})

print(f"Faithfulness: {faith_score.label} ({faith_score.score:.2f})")
print(f"Answer Relevancy: {rel_score.label} ({rel_score.score:.2f})")
print(f"Coherence: {coh_score.label} ({coh_score.score:.2f})")
print(f"Hallucination: {hall_score.label} ({hall_score.score:.2f})")
```

---

## Testing Examples

### Test RAG Setup

```python
def test_rag_setup():
    rag_system = LangChainRAGSystem()

    # Setup
    result = rag_system.setup()
    assert result["success"]
    assert result["num_chunks"] > 0
    assert result["collection_name"] is not None

def test_basic_query():
    rag_system = LangChainRAGSystem()
    rag_system.setup()

    query = "What is supervised learning?"
    result = rag_system.query(query)

    assert result["success"]
    assert len(result["answer"]) > 0
    assert "retrieved_docs" in result
    assert len(result["retrieved_docs"]) > 0

def test_rag_evaluation():
    rag_system = LangChainRAGSystem()
    rag_system.setup()

    query = "Explain neural networks"
    result = rag_system.query(query)

    scores = rag_system.evaluate(query, result["answer"], result["context"])

    # RAG-specific thresholds
    assert scores["faithfulness"].score >= 0.7
    assert scores["answer_relevancy"].score >= 0.7
    assert scores["coherence"].score >= 0.7
```

---

## Best Practices

### 1. Optimal Chunk Size

```python
# Good: Balanced chunk size
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    # Not too small, not too large
    chunk_overlap=200   # 20% overlap
)

# Too small: Loss of context
chunk_size=200

# Too large: Irrelevant information
chunk_size=5000
```

### 2. Embedding Model Selection

```python
# Good: Use latest embedding models
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"  # Cost-effective
)

# For higher quality
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"  # Better accuracy
)
```

### 3. Retrieval Configuration

```python
# Good: Retrieve enough context
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}  # Top 3 chunks
)

# Consider: Use MMR for diversity
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 10}
)
```

### 4. Prompt Engineering

```python
# Good: Clear instructions for RAG
template = """Use ONLY the context below. If the answer isn't in the context, say "I don't know".

Context: {context}

Question: {question}

Answer:"""
```

---

## Use Cases

### Document Q&A

```python
# Answer questions from documents
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)
```

### Knowledge Base

```python
# Company knowledge base
# Load all company docs → chunk → embed → query
```

### Research Assistant

```python
# Research paper analysis
# Load papers → extract key info → answer questions
```

### Customer Support

```python
# Product documentation Q&A
# Load manuals → help customers find answers
```

---

## Quality Gates

```python
RAG_QUALITY_THRESHOLDS = {
    "faithfulness": 0.7,      # Answer grounded in context
    "answer_relevancy": 0.7,   # Answer relevant to question
    "coherence": 0.7,          # Answer is coherent
    "hallucination": 0.3       # Low hallucination (inverted)
}

def validate_rag_output(query, answer, context, scores):
    """Validate RAG output meets quality standards."""
    # Check faithfulness
    if scores["faithfulness"].score < RAG_QUALITY_THRESHOLDS["faithfulness"]:
        return False, "Answer not faithful to context"

    # Check answer relevancy
    if scores["answer_relevancy"].score < RAG_QUALITY_THRESHOLDS["answer_relevancy"]:
        return False, "Answer not relevant to query"

    # Check hallucination
    if scores["hallucination"].score > RAG_QUALITY_THRESHOLDS["hallucination"]:
        return False, "High hallucination detected"

    return True, "All quality checks passed"
```

---

## Troubleshooting

### Issue: Poor retrieval quality

**Solution**: Adjust chunk size and overlap

```python
# Experiment with different sizes
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,   # Try smaller chunks
    chunk_overlap=100
)
```

### Issue: Answers not grounded in context

**Solution**: Improve prompt to enforce context usage

```python
template = """IMPORTANT: Answer using ONLY the context below.
If the answer is not in the context, say "I don't know based on the provided context."

Context: {context}

Question: {question}

Answer (based solely on context):"""
```

### Issue: High hallucination scores

**Solution**: Use lower temperature and enforce context

```python
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0  # More deterministic, less creative
)
```

### Issue: Slow queries

**Solution**: Optimize retrieval and use caching

```python
# Reduce k
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# Use faster embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
```

---

## Resources

- **LangChain Docs**: https://python.langchain.com/
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **Example File**: `examples/rag_langchain_qdrant.py`
- **RAG Guide**: https://python.langchain.com/docs/use_cases/question_answering/

---

## Next Steps

1. Install dependencies: `pip install langchain langchain-openai qdrant-client pypdf`
2. Run example: `python examples/rag_langchain_qdrant.py`
3. Create your first RAG system
4. Experiment with chunk sizes
5. Evaluate with custom-evals

**See Also**:
- [LlamaIndex RAG](llamaindex-rag.md) - Alternative RAG framework
- [LangChain Agent](langchain-agent.md) - Agent capabilities
