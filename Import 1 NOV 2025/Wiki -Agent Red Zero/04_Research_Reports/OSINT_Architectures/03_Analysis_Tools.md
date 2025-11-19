# Part 3 of 4: Analysis & Tools

**Series**: OSINT Architectures
**Navigation**: [← Part 2](./02_Data_Collection.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 4 →](./04_Integration_Cases.md)

---

collection = client.create_collection("osint_docs")

# Add documents with embeddings
collection.add(
    documents=["Email from suspect...", "Social media post..."],
    metadatas=[{"type": "email", "date": "2025-10-16"},
               {"type": "social", "date": "2025-10-15"}],
    ids=["doc1", "doc2"]
)

# Semantic search
results = collection.query(
    query_texts=["communication from target"],
    n_results=5,
    where={"type": "email"}  # Metadata filtering
)
```

### 6.4 SQL Databases for Structured Data

**Purpose:**
- Structured OSINT data storage
- Transaction management
- Reporting and analytics
- Metadata and audit trails

**Data Types:**
- Entity records (people, organizations, locations)
- Collection metadata (source, date, method)
- Relationship metadata (type, strength, date)
- Confidence scores and validation status
- User queries and search history

**Popular Choices:**
- **PostgreSQL**: Most versatile, JSON support, full-text search
- **SQLite**: Lightweight, embedded, perfect for Agent Zero
- **MySQL**: Mature, wide adoption
- **DuckDB**: Embedded analytics, very fast aggregations

**Schema Example:**
```sql
-- Entities table
CREATE TABLE entities (
    id INTEGER PRIMARY KEY,
    entity_type VARCHAR(50),  -- email, ip, domain, person, org
    value TEXT,
    confidence FLOAT,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    source_count INTEGER,
    metadata JSON
);

-- Relationships table
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    entity1_id INTEGER,
    entity2_id INTEGER,
    relationship_type VARCHAR(50),
    strength FLOAT,
    first_observed TIMESTAMP,
    last_observed TIMESTAMP,
    FOREIGN KEY (entity1_id) REFERENCES entities(id),
    FOREIGN KEY (entity2_id) REFERENCES entities(id)
);

-- Sources table
CREATE TABLE sources (
    id INTEGER PRIMARY KEY,
    entity_id INTEGER,
    source_url TEXT,
    source_type VARCHAR(50),
    collection_date TIMESTAMP,
    credibility_tier INTEGER,
    raw_data JSON,
    FOREIGN KEY (entity_id) REFERENCES entities(id)
);

-- Indexes for performance
CREATE INDEX idx_entity_type ON entities(entity_type);
CREATE INDEX idx_entity_value ON entities(value);
CREATE INDEX idx_confidence ON entities(confidence);
CREATE INDEX idx_relationship_entities ON relationships(entity1_id, entity2_id);
```

### 6.5 Hybrid Storage Strategy (Recommended)

**Decision Matrix:**

| Data Type | Storage | Reason |
|-----------|---------|--------|
| Entity records | SQL | Structured, transactional |
| Entity relationships | Graph | Traversal performance |
| Document embeddings | Vector | Semantic search |
| Relationship metadata | SQL | Structured queries |
| Raw collected data | SQL (JSON) | Flexibility |
| Social network analysis | Graph | Network algorithms |
| Similar content search | Vector | Similarity matching |
| Reports and exports | SQL | Reporting, aggregation |

**Integration Pattern:**
```python
class HybridOSINTStore:
    def __init__(self):
        self.sql_db = sqlite3.connect('osint.db')
        self.graph_db = GraphClient('neo4j://localhost')
        self.vector_db = chromadb.Client()

    def store_entity(self, entity):
        # Store structured data in SQL
        entity_id = self.sql_db.execute(
            "INSERT INTO entities VALUES (?, ?, ?, ?)",
            (entity.type, entity.value, entity.confidence, entity.metadata)
        )

        # Store relationships in graph
        self.graph_db.execute(
            "CREATE (e:Entity {id: $id, type: $type, value: $value})",
            id=entity_id, type=entity.type, value=entity.value
        )

        # Store content embedding in vector DB
        if entity.has_content:
            self.vector_db.add(
                documents=[entity.content],
                ids=[str(entity_id)],
                metadatas=[{"type": entity.type}]
            )

    def find_related(self, entity_id, max_hops=3):
        # Use graph for relationship traversal
        return self.graph_db.execute(
            "MATCH (e:Entity {id: $id})-[*..{hops}]-(related) RETURN related",
            id=entity_id, hops=max_hops
        )

    def find_similar(self, content, limit=10):
        # Use vector DB for semantic similarity
        return self.vector_db.query(
            query_texts=[content],
            n_results=limit
        )
```

### 6.6 Indexing Best Practices

**SQL Indexing:**
- Index frequently queried columns (entity_type, value, confidence)
- Composite indexes for common filter combinations
- Full-text indexes for text search
- Avoid over-indexing (impacts write performance)
- Regular ANALYZE/VACUUM for query optimizer

**Graph Indexing:**
- Index node properties used in lookups
- Index relationship types for filtering
- Consider property indexes for common traversals
- Use schema indexes for type constraints

**Vector Indexing:**
- Choose index based on use case (HNSW for reads, IVFFlat for writes)
- Tune index parameters (M, ef_construction for HNSW)
- Consider quantization for memory efficiency
- Rebuild indexes periodically for optimal performance

**Performance Monitoring:**
- Track query latency (p50, p95, p99)
- Monitor index hit rates
- Measure storage growth
- Alert on slow queries (>100ms for critical paths)

---

## 7. Lightweight Implementation Strategies

### 7.1 Resource Constraints for Agent Zero

**Target Profile:**
- Memory: <500MB for OSINT subsystem
- CPU: Single core, non-blocking operations
- Storage: Embedded databases (no external services)
- Dependencies: Minimal, pure Python where possible
- Startup: <2 seconds for OSINT capabilities

### 7.2 Lightweight Technology Stack

**Recommended Components:**

| Component | Technology | Memory | Rationale |
|-----------|-----------|--------|-----------|
| Entity Extraction | GLiNER | 150MB | Zero-shot, no retraining |
| Regex Patterns | re (stdlib) | <1MB | Structured patterns |
| Rule-based NER | Custom EntityRuler | <10MB | Known entities |
| SQL Database | SQLite | 10-50MB | Embedded, transactional |
| Vector Database | ChromaDB | 50-100MB | Embedded, lightweight |
| Graph Database | NetworkX (in-memory) | 50-200MB | Pure Python, flexible |
| Web Scraping | httpx + beautifulsoup4 | 20MB | Async, efficient |
| Rate Limiting | aiolimiter | <1MB | Async, token bucket |

**Total Footprint: ~290-530MB (within constraints)**

### 7.3 Lightweight Architecture

```
┌─────────────────────────────────────────────────────┐
│              Agent Zero OSINT Module                │
├─────────────────────────────────────────────────────┤
│  Collection Layer (Async)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ HTTP     │  │ Social   │  │ Search   │          │
│  │ Scraper  │  │ Media    │  │ APIs     │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│         ↓ Rate Limited ↓                            │
├─────────────────────────────────────────────────────┤
│  Processing Layer                                   │
│  ┌──────────────┐  ┌──────────────┐                │
│  │ Regex        │→ │ GLiNER       │                │
│  │ (structured) │  │ (contextual) │                │
│  └──────────────┘  └──────────────┘                │
│         ↓ Extracted Entities ↓                      │
├─────────────────────────────────────────────────────┤
│  Validation Layer                                   │
│  • Confidence Scoring                               │
│  • Deduplication                                    │
│  • Cross-validation                                 │
│         ↓ Validated Entities ↓                      │
├─────────────────────────────────────────────────────┤
│  Storage Layer                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ SQLite   │  │ ChromaDB │  │ NetworkX │          │
│  │(entities)│  │(semantic)│  │(relations)│         │
│  └──────────┘  └──────────┘  └──────────┘          │
└─────────────────────────────────────────────────────┘
```

### 7.4 Implementation Patterns

**1. Lazy Loading**
```python
class LazyOSINTEngine:
    def __init__(self):
        self._gliner = None
        self._chromadb = None

    @property
    def gliner(self):
        if self._gliner is None:
            from gliner import GLiNER
            self._gliner = GLiNER.from_pretrained("urchade/gliner_base")
        return self._gliner

    @property
    def vector_db(self):
        if self._chromadb is None:
            import chromadb
            self._chromadb = chromadb.Client()
        return self._chromadb
```

**2. Streaming Processing**
```python
async def process_documents_streaming(documents):
    """Process documents in stream to minimize memory"""
    async for doc in documents:
        entities = extract_entities(doc)  # Process one at a time
        validated = validate_entities(entities)
        await store_entities(validated)
        # Document garbage collected after processing
```

**3. Caching Strategy**
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def extract_entities_cached(text_hash, entity_types):
    """Cache extraction results for repeated queries"""
    text = get_text_from_hash(text_hash)
    return gliner.extract(text, entity_types)

def hash_text(text):
    return hashlib.md5(text.encode()).hexdigest()
```

**4. Batch Processing**
```python
async def batch_extraction(texts, batch_size=32):
    """Process in batches for efficiency"""
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        results = await extract_batch(batch)  # GPU utilization
        await store_batch(results)
```

### 7.5 Performance Optimization

**Memory Management:**
- Use generators instead of lists where possible
- Implement document streaming for large collections
- Clear caches periodically (LRU with max size)
- Use weak references for graph nodes
- Garbage collect after batch processing

**CPU Optimization:**
- Regex pre-compilation for repeated patterns
- Async I/O for network operations (httpx, aiohttp)
- Multi-processing for CPU-bound tasks (entity extraction)
- Use numpy/vectorized operations where possible

**Storage Optimization:**
- SQLite WAL mode for concurrent reads
- Vacuum database periodically
- Use appropriate data types (INTEGER vs TEXT)
- Index pruning for unused indexes
- Compress stored raw data (gzip, zstd)

**Network Optimization:**
- Connection pooling (reuse HTTP connections)
- Concurrent requests with limits (10-20 max)
- Request compression (gzip, deflate)
- Response streaming for large payloads
- DNS caching

### 7.6 Minimal Dependency Set

```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.10"

# Core
httpx = "^0.27"           # Async HTTP client (lighter than requests)
beautifulsoup4 = "^4.12"  # HTML parsing
gliner = "^0.2"           # Lightweight NER

# Storage (all embedded)
sqlite3 = "*"             # Stdlib, no install needed
chromadb = "^0.4"         # Vector DB
networkx = "^3.2"         # Graph analysis

# Utilities
aiolimiter = "^1.1"       # Rate limiting
python-dateutil = "^2.8"  # Date parsing
pydantic = "^2.5"         # Data validation

# Optional (for specific use cases)
pillow = { version = "^10.0", optional = true }  # Image processing
playwright = { version = "^1.40", optional = true }  # JS rendering

# Total: ~8 core dependencies, <300MB installed
```

### 7.7 Fallback Strategies

**When Resource Constrained:**

1. **Disable Vector Search**: Use only SQL full-text search
   - Saves 50-100MB memory
   - 70-80% effectiveness of semantic search

2. **Use Regex Only**: Skip NLP entity extraction
   - Saves 150MB memory
   - 60-70% recall on structured entities

3. **In-Memory Only**: Skip persistent storage
   - Session-based intelligence gathering
   - Reset on restart

4. **Simplified Confidence Scoring**: Basic 3-tier system
   - VERIFIED: 2+ sources (0.8)
   - PROBABLE: 1 source (0.5)
   - UNVERIFIED: No validation (0.3)

**Progressive Enhancement:**
```python
class AdaptiveOSINT:
    def __init__(self, memory_limit_mb=500):
        self.memory_limit = memory_limit_mb
        self.capabilities = self._detect_capabilities()

    def _detect_capabilities(self):
        available = psutil.virtual_memory().available / 1024 / 1024

        if available > 1000:
            return {'nlp': True, 'vector': True, 'graph': True}
        elif available > 500:
            return {'nlp': True, 'vector': True, 'graph': False}
        elif available > 300:
            return {'nlp': True, 'vector': False, 'graph': False}
        else:
            return {'nlp': False, 'vector': False, 'graph': False}

    def extract_entities(self, text):
        if self.capabilities['nlp']:
            return self.gliner_extract(text)
        else:
            return self.regex_extract(text)  # Fallback
```

---

## 8. Integration Recommendations for Agent Zero

### 8.1 Recommended Architecture

```
Agent Zero Core
    ↓
┌─────────────────────────────────────┐
│     OSINT Intelligence Module       │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │  Collection Manager (Async)   │  │
│  │  • Rate-limited scraping      │  │
│  │  • Multi-source aggregation   │  │
│  │  • Ethical compliance         │  │
│  └───────────────────────────────┘  │
│              ↓                      │
│  ┌───────────────────────────────┐  │
│  │  Hybrid Entity Extractor      │  │
│  │  • Regex (structured)         │  │
│  │  • GLiNER (contextual)        │  │
│  │  • Entity Ruler (known)       │  │
│  └───────────────────────────────┘  │
│              ↓                      │
│  ┌───────────────────────────────┐  │
│  │  Intelligence Processor       │  │
│  │  • Deduplication              │  │
│  │  • Confidence scoring         │  │
│  │  • Cross-validation           │  │
│  └───────────────────────────────┘  │
│              ↓                      │
│  ┌───────────────────────────────┐  │
│  │  Lightweight Storage          │  │
│  │  • SQLite (structured)        │  │
│  │  • ChromaDB (semantic)        │  │
│  │  • NetworkX (relationships)   │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
         ↓ Intelligence Output
    Agent Zero Memory System
```

### 8.2 API Design

```python
from typing import List, Dict, Optional
from enum import Enum
from pydantic import BaseModel

class EntityType(str, Enum):
    EMAIL = "email"
    DOMAIN = "domain"
    IP = "ip_address"
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    PHONE = "phone"
    URL = "url"


---

**Navigation**: [← Part 2](./02_Data_Collection.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 4 →](./04_Integration_Cases.md)
**Part 3 of 4** | Lines 921-1380 of original document
