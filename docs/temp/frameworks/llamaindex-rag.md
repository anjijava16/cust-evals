# LlamaIndex RAG with Qdrant - Advanced Document Intelligence

## Overview

**LlamaIndex RAG** demonstrates building an advanced Retrieval-Augmented Generation (RAG) system using LlamaIndex for document intelligence and Qdrant for vector storage.

**Key Features**:
- Multi-format document loading
- Advanced indexing strategies
- Query engines with response synthesis
- Qdrant vector store integration
- Multi-document reasoning
- RAG-specific evaluation (Faithfulness, Answer Relevancy)

**Example File**: `examples/rag_llamaindex_qdrant.py`

---

## Installation

```bash
pip install llama-index llama-index-vector-stores-qdrant llama-index-embeddings-openai qdrant-client pypdf
```

---

## Quick Start

### Simple RAG System

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Configure settings
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# 1. Load documents
documents = SimpleDirectoryReader("./docs").load_data()

# 2. Create Qdrant client
client = QdrantClient(path="./qdrant_data")

# 3. Create vector store
vector_store = QdrantVectorStore(
    client=client,
    collection_name="documents"
)

# 4. Create index
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# 5. Create query engine
query_engine = index.as_query_engine()

# 6. Query
response = query_engine.query("What is machine learning?")
print(response.response)
```

---

## Document Loading

### Multi-Format Support

```python
from llama_index.core import SimpleDirectoryReader, Document
from pathlib import Path

# Load all files in directory
documents = SimpleDirectoryReader(
    "./docs",
    recursive=True,  # Include subdirectories
    required_exts=[".pdf", ".txt", ".md"]  # File types
).load_data()

# Load single file
documents = SimpleDirectoryReader(
    input_files=["document.pdf"]
).load_data()

# Create documents manually
documents = [
    Document(
        text="Machine Learning is a subset of AI...",
        metadata={"source": "ml_basics.txt", "category": "intro"}
    ),
    Document(
        text="Deep Learning uses neural networks...",
        metadata={"source": "dl_guide.txt", "category": "advanced"}
    )
]

print(f"Loaded {len(documents)} documents")
```

---

## Text Chunking with Node Parser

### Configure Chunking

```python
from llama_index.core.node_parser import SentenceSplitter

# Create node parser (chunker)
node_parser = SentenceSplitter(
    chunk_size=1024,           # Characters per chunk
    chunk_overlap=200,         # Overlap between chunks
    separator=" ",
    paragraph_separator="\n\n"
)

# Parse documents into nodes
from llama_index.core import Settings
Settings.node_parser = node_parser

# Nodes are created automatically during indexing
# Or create manually
nodes = node_parser.get_nodes_from_documents(documents)

print(f"Created {len(nodes)} nodes")
for i, node in enumerate(nodes[:3]):
    print(f"\nNode {i+1}:")
    print(f"Text: {node.text[:100]}...")
    print(f"Metadata: {node.metadata}")
```

---

## Vector Store Configuration

### Qdrant Setup

```python
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext
from qdrant_client import QdrantClient

# Option 1: In-memory
client = QdrantClient(location=":memory:")

# Option 2: Local persistent storage
client = QdrantClient(path="./qdrant_data")

# Option 3: Remote Qdrant server
client = QdrantClient(
    url="http://localhost:6333",
    api_key="your-api-key"  # Optional
)

# Create vector store
vector_store = QdrantVectorStore(
    client=client,
    collection_name="my_documents"
)

# Create storage context
storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

# Build index with vector store
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)
```

---

## Query Engines

### Different Query Strategies

```python
# 1. Basic Vector Query Engine
query_engine = index.as_query_engine(
    similarity_top_k=3  # Retrieve top 3 chunks
)

# 2. Detailed response
query_engine = index.as_query_engine(
    response_mode="compact",  # Compact context
    similarity_top_k=5
)

# 3. Tree Summarize - hierarchical summarization
query_engine = index.as_query_engine(
    response_mode="tree_summarize"
)

# 4. Refine - iteratively refine answer
query_engine = index.as_query_engine(
    response_mode="refine"
)

# 5. Custom retriever
from llama_index.core.retrievers import VectorIndexRetriever

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=3
)

query_engine = index.as_query_engine(
    retriever=retriever
)

# Query
response = query_engine.query("Explain neural networks")
print(response.response)
```

---

## Advanced Retrieval

### Metadata Filtering

```python
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

# Create documents with metadata
documents = [
    Document(
        text="Content about Python...",
        metadata={"language": "python", "level": "beginner"}
    ),
    Document(
        text="Content about Java...",
        metadata={"language": "java", "level": "intermediate"}
    )
]

# Build index
index = VectorStoreIndex.from_documents(documents)

# Query with metadata filter
filters = MetadataFilters(
    filters=[
        ExactMatchFilter(key="language", value="python")
    ]
)

query_engine = index.as_query_engine(
    filters=filters,
    similarity_top_k=3
)

response = query_engine.query("Tell me about functions")
```

---

## Response Synthesis

### Custom Response Modes

```python
# Compact (default) - fit chunks in single prompt
query_engine = index.as_query_engine(response_mode="compact")

# Refine - iteratively refine with each chunk
query_engine = index.as_query_engine(response_mode="refine")

# Tree Summarize - hierarchical summarization
query_engine = index.as_query_engine(response_mode="tree_summarize")

# Simple Summarize - truncate to fit context
query_engine = index.as_query_engine(response_mode="simple_summarize")

# No text - just return chunks
query_engine = index.as_query_engine(response_mode="no_text")

# Compare responses
for mode in ["compact", "tree_summarize", "refine"]:
    qe = index.as_query_engine(response_mode=mode)
    response = qe.query("What is AI?")
    print(f"\n{mode}: {response.response[:100]}...")
```

---

## Multi-Document Reasoning

### Cross-Document Queries

```python
from llama_index.core import SimpleDirectoryReader

# Load multiple documents
documents = SimpleDirectoryReader("./docs").load_data()

# Build index
index = VectorStoreIndex.from_documents(documents)

# Query engine with increased retrieval
query_engine = index.as_query_engine(
    similarity_top_k=10,  # Retrieve from multiple docs
    response_mode="tree_summarize"  # Synthesize across docs
)

# Ask cross-document questions
response = query_engine.query(
    "Compare machine learning and deep learning approaches"
)

print(response.response)

# Get source nodes
print("\nSources:")
for node in response.source_nodes:
    print(f"- {node.metadata.get('file_name', 'Unknown')}")
```

---

## RAG Evaluation with Custom-Evals

### Comprehensive RAG Evaluation

```python
from custom.evals import (
    FaithfulnessEvaluator,
    AnswerRelevancyEvaluator,
    CoherenceEvaluator,
    HallucinationEvaluator
)
from custom.evals.llm import LLM

# Query system
query = "What is deep learning?"
response = query_engine.query(query)
answer = response.response

# Get retrieved context
retriever = index.as_retriever(similarity_top_k=3)
nodes = retriever.retrieve(query)
context = "\n".join([node.text for node in nodes])

# Initialize evaluators
eval_llm = LLM(provider="openai", model="gpt-4o-mini")

# RAG-specific evaluations
faithfulness = FaithfulnessEvaluator(eval_llm)
faith_score = faithfulness.evaluate({
    "input": query,
    "output": answer,
    "context": context
})

answer_relevancy = AnswerRelevancyEvaluator(eval_llm)
rel_score = answer_relevancy.evaluate({
    "input": query,
    "output": answer
})

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

### Test Document Loading

```python
def test_document_loading():
    system = LlamaIndexRAGSystem()

    result = system.load_documents()

    assert result["success"]
    assert result["num_documents"] > 0
    assert len(result["documents"]) > 0

def test_rag_query():
    system = LlamaIndexRAGSystem()
    system.setup()

    query = "What is supervised learning?"
    result = system.query(query)

    assert result["success"]
    assert len(result["response"]) > 0
    assert "source_nodes" in result

def test_multi_document_reasoning():
    system = LlamaIndexRAGSystem()
    system.setup()

    # Query across multiple documents
    query = "Compare supervised and unsupervised learning"
    result = system.query(query)

    assert result["success"]
    assert len(result["source_nodes"]) > 1  # Multiple sources

    scores = system.evaluate(query, result["response"], result["context"])
    assert scores["faithfulness"].score >= 0.7
```

---

## Best Practices

### 1. Configure Settings Globally

```python
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Set once, use everywhere
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.chunk_size = 1024
Settings.chunk_overlap = 200
```

### 2. Use Appropriate Response Modes

```python
# Simple queries: compact
query_engine = index.as_query_engine(response_mode="compact")

# Complex queries: tree_summarize
query_engine = index.as_query_engine(response_mode="tree_summarize")

# Detailed analysis: refine
query_engine = index.as_query_engine(response_mode="refine")
```

### 3. Optimize Retrieval

```python
# Balance quality vs cost
query_engine = index.as_query_engine(
    similarity_top_k=3,  # Start with 3, adjust as needed
    response_mode="compact"
)
```

### 4. Add Metadata

```python
# Rich metadata helps retrieval
documents = [
    Document(
        text="Content...",
        metadata={
            "title": "Document Title",
            "author": "Author Name",
            "date": "2024-01-01",
            "category": "tutorial",
            "tags": ["python", "ml"]
        }
    )
]
```

---

## Use Cases

### Technical Documentation

```python
# Index company docs
docs = SimpleDirectoryReader("./tech_docs").load_data()
index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()
```

### Research Papers

```python
# Multi-paper reasoning
papers = SimpleDirectoryReader("./papers").load_data()
index = VectorStoreIndex.from_documents(papers)
query_engine = index.as_query_engine(
    similarity_top_k=10,
    response_mode="tree_summarize"
)
```

### Knowledge Base

```python
# Cross-reference multiple sources
kb_docs = SimpleDirectoryReader("./knowledge_base").load_data()
index = VectorStoreIndex.from_documents(kb_docs)
```

---

## Quality Gates

```python
RAG_QUALITY_THRESHOLDS = {
    "faithfulness": 0.75,       # Higher for LlamaIndex
    "answer_relevancy": 0.7,
    "coherence": 0.7,
    "hallucination": 0.25
}

def validate_llamaindex_output(query, response, scores):
    """Validate LlamaIndex RAG output."""
    if not response:
        return False, "Empty response"

    for metric, threshold in RAG_QUALITY_THRESHOLDS.items():
        if metric in scores:
            if metric == "hallucination":
                if scores[metric].score > threshold:
                    return False, f"High {metric}"
            else:
                if scores[metric].score < threshold:
                    return False, f"Low {metric}"

    return True, "Quality checks passed"
```

---

## Troubleshooting

### Issue: Slow indexing

**Solution**: Adjust chunk size and use caching

```python
Settings.chunk_size = 512  # Smaller chunks
Settings.chunk_overlap = 50

# Enable caching
from llama_index.core import set_global_handler
set_global_handler("simple")
```

### Issue: Poor retrieval

**Solution**: Tune similarity_top_k and response mode

```python
query_engine = index.as_query_engine(
    similarity_top_k=5,  # Increase retrieval
    response_mode="tree_summarize"  # Better synthesis
)
```

### Issue: Context too large

**Solution**: Use compact or simple_summarize

```python
query_engine = index.as_query_engine(
    response_mode="simple_summarize",
    similarity_top_k=2  # Reduce chunks
)
```

---

## Comparison with LangChain RAG

| Feature | LlamaIndex | LangChain |
|---------|-----------|-----------|
| Document Loading | ✅✅ SimpleDirectoryReader | ✅ Various loaders |
| Query Engines | ✅✅ Advanced | ✅ RetrievalQA |
| Response Modes | ✅✅ Multiple | ✅ Chain types |
| Metadata | ✅✅ Rich support | ✅ Basic |
| Learning Curve | Medium | Medium |
| Best For | Multi-doc reasoning | Simple RAG |

---

## Resources

- **Official Docs**: https://docs.llamaindex.ai/
- **GitHub**: https://github.com/run-llama/llama_index
- **Qdrant Integration**: https://docs.llamaindex.ai/en/stable/examples/vector_stores/QdrantIndexDemo/
- **Example File**: `examples/rag_llamaindex_qdrant.py`

---

## Next Steps

1. Install: `pip install llama-index llama-index-vector-stores-qdrant`
2. Run example: `python examples/rag_llamaindex_qdrant.py`
3. Build your first index
4. Experiment with query engines
5. Try multi-document reasoning

**See Also**:
- [LangChain RAG](langchain-rag.md) - Alternative RAG framework
- [Qdrant Docs](https://qdrant.tech/documentation/) - Vector database
