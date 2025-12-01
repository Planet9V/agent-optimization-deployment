# Part 5 of 5: Integration & Deployment

**Series**: RAG Best Practices
**Navigation**: [← Part 4](./04_Pitfalls_Scaling.md) | [📚 Series Overview](./00_Series_Overview.md)

---

            return json.loads(cached)

        # Retrieve
        results = self.retrieve(query)

        # Cache
        self.redis_client.setex(
            key,
            self.retrieval_ttl,
            json.dumps(results)
        )

        return results
```

### Scaling Benchmarks

| Scale | Documents | Index Size | Query Latency | Infrastructure | Monthly Cost |
|-------|-----------|------------|---------------|----------------|--------------|
| Small | 10K-100K | 100MB-1GB | 15-50ms | Single server | $50-200 |
| Medium | 100K-1M | 1GB-10GB | 25-100ms | 2-4 servers | $200-1000 |
| Large | 1M-10M | 10GB-100GB | 50-200ms | 10-20 servers | $1000-5000 |
| Enterprise | 10M+ | 100GB+ | 100-500ms | 50+ servers, distributed | $5000+ |

---

## 8. LangChain-FAISS Integration Patterns

### Basic Integration

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

class LangChainFAISSRAG:
    """
    Production-ready LangChain + FAISS integration
    """
    def __init__(self, openai_api_key):
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            openai_api_key=openai_api_key
        )

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        # Vector store
        self.vectorstore = None

        # LLM for generation
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            openai_api_key=openai_api_key
        )

    def index_documents(self, documents):
        """
        Index documents into FAISS
        """
        # Split documents
        texts = self.text_splitter.split_documents(documents)

        # Create FAISS index
        self.vectorstore = FAISS.from_documents(
            documents=texts,
            embedding=self.embeddings
        )

        print(f"Indexed {len(texts)} chunks from {len(documents)} documents")

    def index_from_texts(self, texts, metadatas=None):
        """
        Index from raw texts
        """
        self.vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas
        )

    def save_index(self, path):
        """
        Save FAISS index to disk
        """
        self.vectorstore.save_local(path)

    def load_index(self, path):
        """
        Load FAISS index from disk
        """
        self.vectorstore = FAISS.load_local(
            path,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True  # Only if you trust the source
        )

    def create_qa_chain(self):
        """
        Create QA chain with retrieval
        """
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # or "map_reduce", "refine", "map_rerank"
            retriever=self.vectorstore.as_retriever(
                search_type="mmr",  # Maximal Marginal Relevance
                search_kwargs={"k": 5, "fetch_k": 20}
            ),
            return_source_documents=True
        )

        return qa_chain

    def query(self, question, k=5):
        """
        Query the RAG system
        """
        # Create QA chain
        qa_chain = self.create_qa_chain()

        # Run query
        result = qa_chain({"query": question})

        return {
            "answer": result["result"],
            "sources": result["source_documents"]
        }

    def similarity_search(self, query, k=5, filter=None):
        """
        Direct similarity search
        """
        results = self.vectorstore.similarity_search(
            query=query,
            k=k,
            filter=filter
        )
        return results

    def similarity_search_with_score(self, query, k=5):
        """
        Similarity search with relevance scores
        """
        results = self.vectorstore.similarity_search_with_score(
            query=query,
            k=k
        )
        return results
```

### Advanced Retrieval Strategies

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

class AdvancedLangChainRetriever:
    """
    Advanced retrieval patterns with LangChain
    """
    def __init__(self, vectorstore, llm):
        self.vectorstore = vectorstore
        self.llm = llm

    def create_mmr_retriever(self, k=5, fetch_k=20, lambda_mult=0.5):
        """
        Maximal Marginal Relevance for diversity
        """
        return self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": fetch_k,
                "lambda_mult": lambda_mult  # 0=diversity, 1=relevance
            }
        )

    def create_similarity_score_threshold_retriever(self, score_threshold=0.7):
        """
        Only return documents above relevance threshold
        """
        return self.vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": score_threshold}
        )

    def create_contextual_compression_retriever(self, base_retriever):
        """
        Compress retrieved documents to only relevant parts
        """
        compressor = LLMChainExtractor.from_llm(self.llm)

        return ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )

    def create_ensemble_retriever(self, retrievers, weights=None):
        """
        Combine multiple retrievers with ensemble
        """
        from langchain.retrievers import EnsembleRetriever

        return EnsembleRetriever(
            retrievers=retrievers,
            weights=weights or [1.0 / len(retrievers)] * len(retrievers)
        )
```

### Async Support

```python
class AsyncLangChainFAISS:
    """
    Async LangChain + FAISS for high throughput
    """
    def __init__(self, vectorstore, llm):
        self.vectorstore = vectorstore
        self.llm = llm

    async def asimilarity_search(self, query, k=5):
        """
        Async similarity search
        """
        # LangChain FAISS doesn't have native async yet
        # Use run_in_executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.vectorstore.similarity_search,
            query,
            k
        )

    async def aquery(self, question):
        """
        Async full RAG query
        """
        # Parallel retrieval and any other async operations
        docs = await self.asimilarity_search(question, k=5)

        # Generate response
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""Answer the question based on the context below.

Context:
{context}

Question: {question}

Answer:"""

        # Use async LLM call
        response = await self.llm.agenerate([[prompt]])

        return response.generations[0][0].text
```

### Custom Embedding Function

```python
from langchain.embeddings.base import Embeddings

class CustomEmbeddings(Embeddings):
    """
    Custom embedding function for LangChain
    """
    def __init__(self, model_name="BAAI/bge-large-en-v1.5"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        """Embed list of documents"""
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text):
        """Embed single query"""
        return self.model.encode(text, normalize_embeddings=True).tolist()

# Use custom embeddings
custom_embeddings = CustomEmbeddings()
vectorstore = FAISS.from_texts(
    texts=["text1", "text2"],
    embedding=custom_embeddings
)
```

---

## 9. Production Deployment Checklist

### Pre-Deployment

- [ ] **Data Preparation**
  - [ ] Document cleaning and normalization
  - [ ] Optimal chunk size determined (250-400 tokens)
  - [ ] 15% chunk overlap implemented
  - [ ] Metadata extraction and enrichment
  - [ ] Document deduplication

- [ ] **Embedding Strategy**
  - [ ] Embedding model selected and benchmarked
  - [ ] Fallback embedding provider configured
  - [ ] Embedding cache implemented
  - [ ] Version tracking enabled

- [ ] **Index Optimization**
  - [ ] Index type selected based on scale
  - [ ] Training completed on representative sample
  - [ ] Search parameters tuned (nprobe, efSearch)
  - [ ] GPU acceleration enabled (if applicable)
  - [ ] Index persistence configured

- [ ] **Retrieval Pipeline**
  - [ ] Two-stage retrieval implemented (if needed)
  - [ ] Reranking model integrated
  - [ ] Metadata filtering enabled
  - [ ] Context window expansion configured
  - [ ] Hybrid search tested (dense + sparse)

### Testing

- [ ] **Unit Tests**
  - [ ] Embedding generation
  - [ ] Index creation and search
  - [ ] Chunking logic
  - [ ] Metadata handling

- [ ] **Integration Tests**
  - [ ] End-to-end RAG pipeline
  - [ ] Fallback mechanisms
  - [ ] Cache hit/miss scenarios
  - [ ] Error handling

- [ ] **Performance Tests**
  - [ ] Load testing (concurrent users)
  - [ ] Latency benchmarks (p50, p95, p99)
  - [ ] Throughput testing (queries/second)
  - [ ] Memory usage profiling

- [ ] **Quality Tests**
  - [ ] Retrieval accuracy (Recall@10, Precision@10)
  - [ ] Generation quality (ROUGE, BLEU)
  - [ ] End-to-end accuracy on test set
  - [ ] Comparison with baseline

### Monitoring

- [ ] **Metrics Collection**
  - [ ] Query latency (p50, p95, p99)
  - [ ] Retrieval quality scores
  - [ ] Generation success rate
  - [ ] Cache hit rates
  - [ ] Error rates by type

- [ ] **Logging**
  - [ ] All queries logged
  - [ ] Retrieved documents logged
  - [ ] Generation outputs logged
  - [ ] Errors and exceptions logged

- [ ] **Alerting**
  - [ ] High latency alerts
  - [ ] Low quality alerts
  - [ ] High error rate alerts
  - [ ] API provider outage alerts

### Operations

- [ ] **Scaling**
  - [ ] Horizontal scaling configured
  - [ ] Load balancing enabled
  - [ ] Auto-scaling policies defined
  - [ ] Resource limits set

- [ ] **Resilience**
  - [ ] Multi-provider fallback tested
  - [ ] Circuit breakers implemented
  - [ ] Retry logic with backoff
  - [ ] Graceful degradation

- [ ] **Maintenance**
  - [ ] Index update strategy defined
  - [ ] Embedding model upgrade path
  - [ ] Document refresh schedule
  - [ ] Backup and recovery procedures

### Cost Optimization

- [ ] **Cost Tracking**
  - [ ] Embedding API costs monitored
  - [ ] LLM API costs monitored
  - [ ] Infrastructure costs tracked
  - [ ] Cost per query calculated

- [ ] **Optimization**
  - [ ] Caching strategy implemented
  - [ ] Batch processing enabled
  - [ ] Cost-effective models used where appropriate
  - [ ] Tiered storage for historical data

---

## Conclusion

This comprehensive guide synthesizes best practices for implementing hierarchical RAG systems at production scale. Key takeaways:

1. **Two-round retrieval** (RAPTOR, HM-RAG) significantly improves complex query performance
2. **FAISS optimization** requires careful index selection and parameter tuning
3. **Chunk size** of 250-400 tokens with 15% overlap is optimal for most use cases
4. **Embedding model selection** depends on accuracy requirements, budget, and data privacy
5. **Scaling beyond 100K documents** requires distributed architecture and caching
6. **Common pitfalls** can be avoided through proper chunking, reranking, and monitoring
7. **LangChain-FAISS integration** simplifies implementation but requires understanding of underlying components

### Next Steps

1. **Start small:** Build MVP with 10K documents using IndexIVFPQ
2. **Measure baseline:** Establish retrieval and generation quality metrics
3. **Iterate:** Test different chunking strategies, embedding models, and retrieval methods
4. **Scale gradually:** Move to distributed architecture only when necessary
5. **Monitor continuously:** Track performance and costs in production

### Additional Resources

**Academic Papers:**
- RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval
- HM-RAG: Hierarchical Multi-Agent Multimodal RAG
- LevelRAG: Multi-hop Logic Planning

**Official Documentation:**
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [LangChain FAISS Integration](https://python.langchain.com/docs/integrations/vectorstores/faiss/)
- [Sentence Transformers](https://www.sbert.net/)

**Production Examples:**
- [RAPTOR Implementation](https://github.com/parthsarthi03/raptor)
- [RAG Techniques Repository](https://github.com/NirDiamant/RAG_Techniques)

---

**Report Confidence:** High
**Last Updated:** October 16, 2025
**Research Methodology:** Web search synthesis from academic papers, production case studies, and official documentation


---

**Navigation**: [← Part 4](./04_Pitfalls_Scaling.md) | [📚 Series Overview](./00_Series_Overview.md)
**Part 5 of 5** | Lines 1801-2254 of original document
