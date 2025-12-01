# Part 3 of 5: Embeddings & Performance

**Series**: RAG Best Practices
**Navigation**: [← Part 2](./02_FAISS_Optimization.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 4 →](./04_Pitfalls_Scaling.md)

---

        for query, relevant_docs in zip(self.test_queries, self.ground_truth):
            start = time.time()
            retrieved = self.rag_system.retrieve(query, k=k)
            latency = time.time() - start

            retrieved_ids = [doc['id'] for doc in retrieved]

            # Calculate metrics
            precision = self.calculate_precision(retrieved_ids, relevant_docs)
            recall = self.calculate_recall(retrieved_ids, relevant_docs)
            f1 = self.calculate_f1(precision, recall)
            ndcg = self.calculate_ndcg(retrieved_ids, relevant_docs)
            mrr = self.calculate_mrr(retrieved_ids, relevant_docs)

            metrics["precision"].append(precision)
            metrics["recall"].append(recall)
            metrics["f1"].append(f1)
            metrics["ndcg"].append(ndcg)
            metrics["mrr"].append(mrr)
            metrics["latency"].append(latency)

        # Return average metrics
        return {k: np.mean(v) for k, v in metrics.items()}

    def calculate_precision(self, retrieved, relevant):
        """Precision@K"""
        if not retrieved:
            return 0.0
        relevant_retrieved = set(retrieved) & set(relevant)
        return len(relevant_retrieved) / len(retrieved)

    def calculate_recall(self, retrieved, relevant):
        """Recall@K"""
        if not relevant:
            return 0.0
        relevant_retrieved = set(retrieved) & set(relevant)
        return len(relevant_retrieved) / len(relevant)

    def calculate_f1(self, precision, recall):
        """F1 Score"""
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)

    def calculate_ndcg(self, retrieved, relevant, k=10):
        """Normalized Discounted Cumulative Gain"""
        dcg = 0.0
        for i, doc_id in enumerate(retrieved[:k]):
            if doc_id in relevant:
                dcg += 1.0 / np.log2(i + 2)  # i+2 because i starts at 0

        # Ideal DCG
        idcg = sum(1.0 / np.log2(i + 2) for i in range(min(len(relevant), k)))

        return dcg / idcg if idcg > 0 else 0.0

    def calculate_mrr(self, retrieved, relevant):
        """Mean Reciprocal Rank"""
        for i, doc_id in enumerate(retrieved):
            if doc_id in relevant:
                return 1.0 / (i + 1)
        return 0.0

    def benchmark_generation(self, llm):
        """
        Measure generation quality
        """
        from rouge import Rouge

        rouge = Rouge()
        metrics = {
            "rouge1": [],
            "rouge2": [],
            "rougeL": [],
            "generation_time": []
        }

        for query, reference in zip(self.test_queries, self.ground_truth):
            start = time.time()
            generated = self.rag_system.generate(query, llm)
            gen_time = time.time() - start

            # Calculate ROUGE scores
            scores = rouge.get_scores(generated, reference)[0]

            metrics["rouge1"].append(scores["rouge-1"]["f"])
            metrics["rouge2"].append(scores["rouge-2"]["f"])
            metrics["rougeL"].append(scores["rouge-l"]["f"])
            metrics["generation_time"].append(gen_time)

        return {k: np.mean(v) for k, v in metrics.items()}

    def benchmark_end_to_end(self, llm):
        """
        Full RAG pipeline benchmark
        """
        retrieval_metrics = self.benchmark_retrieval()
        generation_metrics = self.benchmark_generation(llm)

        return {
            "retrieval": retrieval_metrics,
            "generation": generation_metrics,
            "total_latency": retrieval_metrics["latency"] + generation_metrics["generation_time"]
        }
```

### Real-World Performance Benchmarks

Based on production systems and published research:

#### Small Scale (10K-100K Documents)

| Metric | Value | Configuration |
|--------|-------|---------------|
| Retrieval Latency | 15-50ms | IndexIVFPQ, nprobe=10 |
| Recall@10 | 95-98% | BGE-large embeddings |
| Precision@10 | 88-92% | With reranking |
| Generation Latency | 500-2000ms | GPT-3.5/GPT-4 |
| Total Query Time | 515-2050ms | End-to-end |
| Index Size | 50-500MB | Depending on compression |

#### Medium Scale (100K-1M Documents)

| Metric | Value | Configuration |
|--------|-------|---------------|
| Retrieval Latency | 25-100ms | IndexIVFPQ or HNSW |
| Recall@10 | 92-96% | Optimized nprobe |
| Precision@10 | 85-90% | Hybrid search + reranking |
| Generation Latency | 500-2000ms | GPT-3.5/GPT-4 |
| Total Query Time | 525-2100ms | End-to-end |
| Index Size | 500MB-5GB | IVF+PQ compression |

#### Large Scale (1M-10M Documents)

| Metric | Value | Configuration |
|--------|-------|---------------|
| Retrieval Latency | 50-200ms | GPU-accelerated IVFPQ |
| Recall@10 | 90-95% | Hierarchical retrieval |
| Precision@10 | 82-88% | Multi-stage reranking |
| Generation Latency | 500-2000ms | GPT-3.5/GPT-4 |
| Total Query Time | 550-2200ms | End-to-end |
| Index Size | 5GB-50GB | Optimized compression |

#### Cost Benchmarks (Production)

**Processing 10M input tokens + 3M output tokens daily:**
- GPT-4: ~$480/day ($14,400/month)
- GPT-3.5-turbo: ~$60/day ($1,800/month)
- Open-source LLM (self-hosted): ~$200/month (infrastructure)

**Embedding Costs:**
- OpenAI text-embedding-3-large: ~$130/month (1B tokens)
- OpenAI text-embedding-3-small: ~$20/month (1B tokens)
- Self-hosted (Sentence Transformers): ~$50/month (GPU instance)

---

## 6. Common Pitfalls and Failure Modes

### Critical Failure Modes

#### 1. Chunking Problems

**Issue:** Ineffective document chunking leads to information loss and poor retrieval.

**Common Mistakes:**
- Chunks too large (>1000 tokens): Loss of specificity, noisy context
- Chunks too small (<100 tokens): Loss of context, fragmented information
- Arbitrary splitting: Breaking sentences/paragraphs mid-thought

**Solution:**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

class SmartChunker:
    """
    Context-aware document chunking
    """
    def __init__(self, chunk_size=400, chunk_overlap=60):
        # Optimal: 250-400 tokens (~1000-1600 chars)
        # Overlap: 15% (recommended by NVIDIA research)
        self.chunk_size = chunk_size * 4  # ~4 chars per token
        self.chunk_overlap = chunk_overlap * 4

        # Hierarchical separators
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n\n",  # Multiple blank lines
                "\n\n",    # Paragraphs
                "\n",      # Lines
                ". ",      # Sentences
                ", ",      # Clauses
                " ",       # Words
                ""         # Characters (last resort)
            ]
        )

    def chunk_document(self, text, metadata=None):
        """
        Split document into semantically coherent chunks
        """
        chunks = self.splitter.create_documents(
            texts=[text],
            metadatas=[metadata] if metadata else None
        )

        # Post-process: add context to each chunk
        enhanced_chunks = []
        for i, chunk in enumerate(chunks):
            # Add position info
            chunk.metadata['chunk_index'] = i
            chunk.metadata['total_chunks'] = len(chunks)

            # Add surrounding context if available
            if i > 0:
                chunk.metadata['previous_chunk_preview'] = chunks[i-1].page_content[:100]
            if i < len(chunks) - 1:
                chunk.metadata['next_chunk_preview'] = chunks[i+1].page_content[:100]

            enhanced_chunks.append(chunk)

        return enhanced_chunks

    def chunk_with_semantic_boundaries(self, text, document_type="general"):
        """
        Type-aware chunking for different document types
        """
        if document_type == "code":
            # Split by functions/classes
            return self.chunk_code(text)
        elif document_type == "legal":
            # Split by sections/clauses
            return self.chunk_legal(text)
        elif document_type == "academic":
            # Split by sections/subsections
            return self.chunk_academic(text)
        else:
            return self.splitter.split_text(text)
```

**Best Practices:**
- Start with 250-400 tokens (1000-1600 characters)
- Use 15% overlap between chunks
- Respect document structure (paragraphs, sections)
- Include metadata (chunk position, document context)
- Test on your specific document types

#### 2. Embedding Model Drift

**Issue:** Embedding models change over time (updates, fine-tuning), causing misalignment with existing indexes.

**Solution:**
```python
class VersionedEmbeddingService:
    """
    Track embedding model versions and handle migrations
    """
    def __init__(self, model_name, version):
        self.model_name = model_name
        self.version = version
        self.model = self.load_model(model_name, version)

    def embed(self, text):
        """Embed with version tracking"""
        embedding = self.model.encode(text)
        return {
            "embedding": embedding,
            "model": self.model_name,
            "version": self.version,
            "timestamp": time.time()
        }

    def migrate_index(self, old_index, old_version, new_version):
        """
        Re-embed documents when model changes
        """
        print(f"Migrating from {old_version} to {new_version}")

        # Load old documents
        documents = self.load_documents_from_index(old_index)

        # Re-embed with new model
        new_embeddings = []
        for doc in documents:
            new_emb = self.embed(doc['text'])
            new_embeddings.append(new_emb['embedding'])

        # Create new index
        new_index = self.create_index()
        new_index.add(np.array(new_embeddings))

        return new_index
```

#### 3. Insufficient Context in Retrieved Chunks

**Issue:** Retrieved chunks don't contain enough context for accurate generation.

**Solution: Context Window Expansion**
```python
class ContextAwareRetriever:
    """
    Retrieve chunks with expanded context
    """
    def __init__(self, index, chunk_store):
        self.index = index
        self.chunk_store = chunk_store  # Maps chunk_id -> chunk data

    def retrieve_with_context(self, query, k=5, context_window=1):
        """
        Retrieve chunks and include neighboring chunks for context
        """
        # Standard retrieval
        distances, indices = self.index.search(query, k)

        # Expand context
        expanded_results = []
        for idx in indices[0]:
            chunk = self.chunk_store[idx]

            # Get neighboring chunks
            context_chunks = []
            for offset in range(-context_window, context_window + 1):
                neighbor_idx = chunk['chunk_index'] + offset
                if 0 <= neighbor_idx < chunk['total_chunks']:
                    neighbor = self.chunk_store.get(neighbor_idx)
                    if neighbor and neighbor['document_id'] == chunk['document_id']:
                        context_chunks.append(neighbor)

            # Combine chunks
            expanded_text = "\n\n".join([c['text'] for c in context_chunks])
            expanded_results.append({
                "text": expanded_text,
                "main_chunk": chunk,
                "context_chunks": context_chunks
            })

        return expanded_results
```

#### 4. Poor Reranking or No Reranking

**Issue:** Initial retrieval returns relevant documents, but they're poorly ranked.

**Solution: Two-Stage Retrieval with Reranking**
```python
from sentence_transformers import CrossEncoder

class TwoStageRetriever:
    """
    Fast retrieval + slow reranking for optimal accuracy
    """
    def __init__(self, retriever, reranker_model="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.retriever = retriever
        self.reranker = CrossEncoder(reranker_model)

    def retrieve_and_rerank(self, query, k=10, rerank_top_n=50):
        """
        1. Fast retrieval: Get top 50 candidates
        2. Slow reranking: Rerank to get top 10
        """
        # Stage 1: Fast approximate retrieval
        candidates = self.retriever.retrieve(query, k=rerank_top_n)

        # Stage 2: Accurate reranking
        query_doc_pairs = [[query, doc['text']] for doc in candidates]
        rerank_scores = self.reranker.predict(query_doc_pairs)

        # Sort by reranked scores
        for doc, score in zip(candidates, rerank_scores):
            doc['rerank_score'] = score

        candidates.sort(key=lambda x: x['rerank_score'], reverse=True)

        return candidates[:k]
```

#### 5. Single Point of Failure (Single LLM/Embedding Model)

**Issue:** Production outages when API provider has issues.

**Solution: Multi-Model Fallback**
```python
class ResilientRAGSystem:
    """
    RAG system with fallback models
    """
    def __init__(self):
        self.embedding_providers = [
            {"name": "openai", "model": "text-embedding-3-large", "priority": 1},
            {"name": "cohere", "model": "embed-english-v3.0", "priority": 2},
            {"name": "local", "model": "BAAI/bge-large-en-v1.5", "priority": 3}
        ]

        self.llm_providers = [
            {"name": "openai", "model": "gpt-4", "priority": 1},
            {"name": "anthropic", "model": "claude-3-opus", "priority": 2},
            {"name": "local", "model": "llama-3-70b", "priority": 3}
        ]

    def get_embedding(self, text, max_retries=3):
        """
        Try embedding providers in priority order
        """
        for provider in sorted(self.embedding_providers, key=lambda x: x['priority']):
            try:
                return self._embed_with_provider(text, provider)
            except Exception as e:
                print(f"Provider {provider['name']} failed: {e}")
                continue

        raise Exception("All embedding providers failed")

    def generate(self, query, context, max_retries=3):
        """
        Try LLM providers in priority order
        """
        for provider in sorted(self.llm_providers, key=lambda x: x['priority']):
            try:
                return self._generate_with_provider(query, context, provider)
            except Exception as e:
                print(f"Provider {provider['name']} failed: {e}")
                continue

        raise Exception("All LLM providers failed")
```

#### 6. Metadata Ignored in Retrieval

**Issue:** Pure vector search treats all documents equally, ignoring valuable metadata.

**Solution: Metadata-Enhanced Retrieval**
```python
class MetadataAwareRetriever:
    """
    Combine vector search with metadata filtering
    """
    def __init__(self, vector_index, metadata_db):
        self.vector_index = vector_index
        self.metadata_db = metadata_db  # SQL/NoSQL database

    def retrieve_with_filters(
        self,
        query,
        k=10,
        filters=None,
        boost_metadata=None
    ):


---

**Navigation**: [← Part 2](./02_FAISS_Optimization.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 4 →](./04_Pitfalls_Scaling.md)
**Part 3 of 5** | Lines 901-1350 of original document
