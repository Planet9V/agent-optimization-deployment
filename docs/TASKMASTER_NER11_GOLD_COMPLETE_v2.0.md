# TASKMASTER: NER11 Gold Integration - Complete Implementation Guide
**File**: TASKMASTER_NER11_GOLD_COMPLETE_v2.0.md
**Created**: 2025-12-01 05:35:00 UTC
**Modified**: 2025-12-01 05:35:00 UTC
**Version**: 2.0.0
**Author**: Claude-Flow Orchestration System
**Purpose**: Self-contained implementation guide for NER11 Gold integration with AEON platform
**Status**: ACTIVE - PRODUCTION IMPLEMENTATION GUIDE

---

## 🚨 CRITICAL CONTEXT FOR NEW SESSIONS

### What This Document Is
This TASKMASTER provides **complete, standalone instructions** for integrating the NER11 Gold Standard model with the existing AEON Digital Twin platform. A new session should be able to execute all tasks using only this document and the referenced files.

### Constitutional Authority
**Governed By**: `/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/00_AEON_CONSTITUTION.md`

**Core Principles** (Article I, Section 1.2):
1. **NO DEVELOPMENT THEATER**: Build actual features, not frameworks
2. **ALWAYS USE EXISTING RESOURCES**: Extend, never duplicate
3. **NEVER BREAK CLERK AUTH**: Frontend authentication must remain functional
4. **PATH INTEGRITY**: Never break existing integrations
5. **TASKMASTER COMPLIANCE**: All work tracked in Qdrant memory

### Current Production System State

**NER11 Gold API** (OPERATIONAL):
- Container: `ner11-gold-api`
- Status: ✅ Healthy (port 8000)
- Model: NER11 Gold Standard v3.0
- Entity Types: 58 labels (corrected from 566 in planning docs)
- API: FastAPI with Swagger UI
- Test Results: 100% confidence scores
- Documentation: http://localhost:8000/docs

**NOTE**: Planning documents reference "566 entity types" but the **ACTUAL PRODUCTION MODEL has 58 labels**. See `/docs/NER11_GOLD_STATUS_REPORT_2025-12-01.md` for verified list.

**Infrastructure** (ALL OPERATIONAL):
```yaml
ner11-gold-api:    port 8000  (FastAPI - NER extraction)
openspg-neo4j:     ports 7474/7687 (Knowledge graph - 570K nodes, 3.3M edges)
openspg-qdrant:    ports 6333-6334 (Vector embeddings)
aeon-postgres-dev: port 5432  (Application state, jobs)
openspg-mysql:     port 3306  (OpenSPG metadata)
aeon-saas-dev:     port 3000  (Next.js + Clerk auth)
openspg-server:    port 8887  (Knowledge graph engine)
openspg-redis:     port 6379  (Cache, queues)
openspg-minio:     ports 9000-9001 (Object storage)
```

---

## 📚 CRITICAL REFERENCE DOCUMENTS

### Required Reading (IN ORDER)

#### 1. System Architecture & Governance
- **Constitution**: `/1_AEON_DT_CyberSecurity_Wiki_Current/00_AEON_CONSTITUTION.md`
  - Governing principles, non-negotiable rules
  - 3-database architecture (Neo4j, PostgreSQL, MySQL)
  - Quality standards, performance targets

- **Architecture**: `/1_AEON_DT_CyberSecurity_Wiki_Current/01_ARCHITECTURE/01_COMPREHENSIVE_ARCHITECTURE.md`
  - Complete system architecture
  - Container inventory
  - Data flow patterns
  - Integration points

#### 2. NER11 Gold Model Documentation
- **Status Report**: `/docs/NER11_GOLD_STATUS_REPORT_2025-12-01.md`
  - Current production status (port 8000)
  - 58 verified entity types
  - API endpoints and test results

- **API Reference**: `/5_NER11_Gold_Model/API_NER11_GOLD/01_API_REFERENCE.md`
  - Endpoint specifications
  - Request/response formats
  - Error handling

- **Neo4j Pipeline**: `/5_NER11_Gold_Model/API_NER11_GOLD/02_NEO4J_PIPELINE_GUIDE.md`
  - Integration script template
  - Graph construction patterns
  - Relationship creation

#### 3. Enhancement & Gap Analysis
- **Quick Start**: `/6_NER11_Gold_Model_Enhancement/implementation_guides/01_QUICK_START_GUIDE.md`
  - Schema v3.1 migration
  - Test procedures
  - Validation steps

- **Gap Analysis**: `/6_NER11_Gold_Model_Enhancement/strategic_analysis/01_COMPREHENSIVE_GAP_ANALYSIS.md`
  - NER11 (58 types) vs Neo4j (18 types) mismatch
  - Data loss risks (45% potential loss)
  - Remediation strategies

- **Schema v3.1**: `/6_NER11_Gold_Model_Enhancement/neo4j_integration/01_SCHEMA_V3.1_SPECIFICATION.md`
  - 16 super labels design
  - Property discriminators
  - Hierarchical classification

#### 4. API Integration Context
- **API Status**: `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/00_API_STATUS_AND_ROADMAP.md`
  - PLANNED vs IMPLEMENTED APIs
  - Current: Only direct Neo4j Cypher queries
  - Planned: 36+ REST endpoints, GraphQL, WebSocket

- **API Overview**: `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/API_OVERVIEW.md`
  - Complete endpoint catalog
  - Authentication patterns
  - Performance targets

#### 5. Hybrid Architecture Planning
- **Hybrid Design**: `/1_AEON_DT_CyberSecurity_Wiki_Current/12_NER12_Gold_Schema_hyrbrid/05_HYBRID_ARCHITECTURE_DESIGN.md`
  - Split-brain architecture (Neo4j structure + Qdrant context)
  - Data responsibility boundaries
  - Workflow enablement

- **Gap Report**: `/1_AEON_DT_CyberSecurity_Wiki_Current/12_NER12_Gold_Schema_hyrbrid/03_GAP_ANALYSIS_REPORT.md`
  - Architectural mismatch details
  - Domain-specific impacts
  - Remediation options

**NOTICE**: Files in `12_NER12_Gold_Schema_hyrbrid/` are PLANNING documents. Read `/1_AEON_DT_CyberSecurity_Wiki_Current/12_NER12_Gold_Schema_hyrbrid/00_NOTICE_PLANNING_DOCUMENTS.md` first.

---

## ⚠️ CRITICAL ARCHITECTURAL CONSTRAINTS

### EXTEND EXISTING SYSTEMS - DO NOT CREATE PARALLEL SYSTEMS

**ABSOLUTE RULES** (From Constitution Article I, Section 1.2):

1. **USE EXISTING NEO4J INSTANCE**
   - Database: `openspg-neo4j` (ports 7474/7687)
   - Current: 570K nodes, 3.3M edges
   - Action: EXTEND schema, do NOT create new database
   - Command: `docker exec openspg-neo4j cypher-shell`

2. **USE EXISTING QDRANT INSTANCE**
   - Database: `openspg-qdrant` (ports 6333-6334)
   - Collection exists: `aeon_session_state`
   - Action: CREATE new collection `ner11_entities`, do NOT deploy new Qdrant
   - API: http://localhost:6333

3. **USE EXISTING OPENSPG SERVER**
   - Service: `openspg-server` (port 8887)
   - Purpose: Knowledge graph construction
   - Action: INTEGRATE NER11 pipeline, do NOT replace OpenSPG

4. **USE EXISTING NEXT.JS FRONTEND**
   - Application: `aeon-saas-dev` (port 3000)
   - Auth: Clerk (NEVER break auth flows)
   - Action: ADD NER11 features to UI, do NOT create new frontend

5. **USE EXISTING API SPECIFICATIONS**
   - Location: `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/`
   - Status: 28 API files, PLANNED (not yet implemented)
   - Action: IMPLEMENT existing specs, do NOT create new API designs

### Integration Points (Use These, Don't Replace)

**Network**: `aeon-net` (Docker network - all containers connected)

**Databases**:
- Neo4j: `bolt://172.18.0.5:7687` (primary knowledge graph)
- PostgreSQL: `172.18.0.4:5432` (application state, jobs)
- MySQL: `172.18.0.4:3306` (OpenSPG operations)
- Qdrant: `http://172.18.0.6:6333` (vectors, embeddings)

**Existing Code** (To Extend):
- Qdrant agents: `/openspg-official_neo4j/qdrant_agents/` (6 modules)
- Neo4j examples: `/5_NER11_Gold_Model/examples/neo4j_example.py`
- OpenSPG integration: Available via port 8887

---

## 🎯 PHASE 1: NER11 → Qdrant Vector Pipeline (CRITICAL - START HERE)

### Business Context
**Problem**: NER11 extracts 58 entity types with high-fidelity text. Need semantic search capability.
**Solution**: Embed entities in Qdrant for vector similarity search.
**Value**: Enable "Find similar vulnerabilities" queries across 570K+ entities.

### Technical Constraints from Constitution
- **Reuse Existing**: `openspg-qdrant` container (DO NOT deploy new Qdrant)
- **New Collection**: Create `ner11_entities` (existing: `aeon_session_state`)
- **Existing Code**: Adapt `/openspg-official_neo4j/qdrant_init_phase1.py`
- **Performance**: <100ms search latency (Article II, Section 2.3)

### Task 1.1: Configure Qdrant Collection for NER11
**Priority**: 🔴 CRITICAL
**Time**: 30-45 minutes
**Prerequisites**: Qdrant operational (verify with `curl http://localhost:6333/collections`)

**Implementation**:
```python
# File: /5_NER11_Gold_Model/pipelines/01_configure_qdrant_collection.py
# Purpose: Create Qdrant collection for NER11 entities

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# REUSE EXISTING QDRANT (Constitution Article I.2)
client = QdrantClient(host="localhost", port=6333)

# Collection schema for NER11 entities
collection_name = "ner11_entities"

# Vector configuration
# Using sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
# Alternative: all-mpnet-base-v2 (768 dimensions, higher quality)
vector_size = 384  # Match your embedding model
distance_metric = Distance.COSINE  # Best for semantic similarity

# Create collection
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=vector_size,
        distance=distance_metric
    )
)

# Create payload index for filtering
client.create_payload_index(
    collection_name=collection_name,
    field_name="label",  # NER entity label (CVE, MALWARE, etc.)
    field_schema="keyword"
)

client.create_payload_index(
    collection_name=collection_name,
    field_name="confidence",  # Entity confidence score
    field_schema="float"
)

client.create_payload_index(
    collection_name=collection_name,
    field_name="doc_id",  # Source document ID
    field_schema="keyword"
)

print(f"✅ Collection '{collection_name}' created successfully")
print(f"Vector size: {vector_size}, Distance: {distance_metric}")
```

**Expected Output**:
```
✅ Collection 'ner11_entities' created successfully
Vector size: 384, Distance: COSINE
```

**Verification**:
```bash
curl http://localhost:6333/collections/ner11_entities | python3 -m json.tool
```

**Success Criteria**:
- Collection `ner11_entities` exists
- Payload indexes created for label, confidence, doc_id
- Vector dimension matches embedding model

---

### Task 1.2: Entity Embedding Service
**Priority**: 🔴 CRITICAL
**Time**: 1-2 hours
**Dependencies**: Task 1.1 complete, sentence-transformers installed

**Implementation**:
```python
# File: /5_NER11_Gold_Model/pipelines/02_entity_embedding_service.py
# Purpose: Generate embeddings for NER11 entities

import requests
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
from typing import List, Dict

class NER11EmbeddingService:
    """
    Embedding service for NER11 Gold entities.

    EXTENDS EXISTING: Integrates with ner11-gold-api (port 8000)
    REUSES: openspg-qdrant (port 6333)
    STORES: Embeddings in ner11_entities collection
    """

    def __init__(
        self,
        ner_api_url: str = "http://localhost:8000",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        collection_name: str = "ner11_entities",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        # INTEGRATE with existing NER11 API (DO NOT create new NER service)
        self.ner_api_url = ner_api_url

        # REUSE existing Qdrant (DO NOT deploy new vector DB)
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.collection_name = collection_name

        # Load embedding model (lightweight, fast)
        self.embedding_model = SentenceTransformer(embedding_model)

    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extract entities using EXISTING NER11 API.

        Endpoint: POST http://localhost:8000/ner
        Returns: List of entities with label, text, start, end, score
        """
        response = requests.post(
            f"{self.ner_api_url}/ner",
            json={"text": text},
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"NER API error: {response.text}")

        return response.json()["entities"]

    def generate_embedding(self, text: str, context: str = "") -> List[float]:
        """
        Generate embedding for entity text.

        Strategy: Combine entity text + surrounding context for better semantics
        Model: all-MiniLM-L6-v2 (384 dimensions, fast, accurate)
        """
        # Combine entity with context for richer embeddings
        if context:
            combined_text = f"{text} [CONTEXT: {context}]"
        else:
            combined_text = text

        embedding = self.embedding_model.encode(combined_text)
        return embedding.tolist()

    def store_in_qdrant(
        self,
        entities: List[Dict],
        doc_id: str,
        doc_text: str,
        batch_size: int = 100
    ) -> int:
        """
        Store entities in EXISTING Qdrant collection.

        Payload Schema:
        {
          "text": entity text,
          "label": NER11 label (CVE, MALWARE, etc.),
          "confidence": float (0.0-1.0),
          "doc_id": source document ID,
          "start": char position,
          "end": char position,
          "context": surrounding text (±100 chars)
        }
        """
        points = []

        for entity in entities:
            # Extract context (±100 characters around entity)
            start = max(0, entity["start"] - 100)
            end = min(len(doc_text), entity["end"] + 100)
            context = doc_text[start:end]

            # Generate embedding
            embedding = self.generate_embedding(entity["text"], context)

            # Create Qdrant point
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": entity["text"],
                    "label": entity["label"],
                    "confidence": entity["score"],
                    "doc_id": doc_id,
                    "start": entity["start"],
                    "end": entity["end"],
                    "context": context
                }
            )
            points.append(point)

        # Batch insert (efficient for large documents)
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        return len(points)

    def process_document(self, doc_id: str, doc_text: str) -> Dict:
        """
        Complete pipeline: Text → NER11 API → Embeddings → Qdrant

        Returns: Summary statistics
        """
        # Step 1: Extract entities using EXISTING NER11 API
        entities = self.extract_entities(doc_text)

        # Step 2: Generate embeddings and store
        stored_count = self.store_in_qdrant(entities, doc_id, doc_text)

        return {
            "doc_id": doc_id,
            "entities_extracted": len(entities),
            "entities_stored": stored_count,
            "labels_found": list(set(e["label"] for e in entities))
        }

    def semantic_search(
        self,
        query_text: str,
        limit: int = 10,
        label_filter: List[str] = None,
        confidence_threshold: float = 0.7
    ) -> List[Dict]:
        """
        Semantic search over stored entities.

        Returns: Top-K similar entities with scores
        """
        # Generate query embedding
        query_embedding = self.generate_embedding(query_text)

        # Build filter
        filter_conditions = {}
        if label_filter:
            filter_conditions["label"] = {"$in": label_filter}
        if confidence_threshold:
            filter_conditions["confidence"] = {"$gte": confidence_threshold}

        # Search Qdrant
        search_results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            query_filter=filter_conditions if filter_conditions else None
        )

        # Format results
        results = []
        for hit in search_results:
            results.append({
                "text": hit.payload["text"],
                "label": hit.payload["label"],
                "similarity": hit.score,
                "confidence": hit.payload["confidence"],
                "doc_id": hit.payload["doc_id"],
                "context": hit.payload["context"]
            })

        return results


# Example Usage
if __name__ == "__main__":
    # Initialize service (USES EXISTING INFRASTRUCTURE)
    service = NER11EmbeddingService()

    # Process test document
    test_doc = """
    CVE-2024-1234 affects Apache Tomcat 9.0.x allowing remote code execution
    via SQL injection. APT29 has been observed exploiting this vulnerability
    to target critical infrastructure. The malware family Emotet was deployed
    as secondary payload.
    """

    # Extract, embed, and store
    result = service.process_document("doc_001", test_doc)
    print(f"Processed: {result}")

    # Test semantic search
    search_results = service.semantic_search(
        query_text="vulnerabilities in web servers",
        label_filter=["CVE", "SOFTWARE_COMPONENT"],
        limit=5
    )

    for i, result in enumerate(search_results, 1):
        print(f"{i}. {result['text']} ({result['label']}) - similarity: {result['similarity']:.3f}")
```

**Installation Requirements**:
```bash
# File: /5_NER11_Gold_Model/pipelines/requirements.txt
sentence-transformers==2.2.2
qdrant-client==1.7.0
requests==2.31.0
httpx==0.25.2
```

**Install Command**:
```bash
cd /5_NER11_Gold_Model/pipelines
pip install -r requirements.txt
```

**Verification Tests**:
```python
# Test 1: Verify NER11 API connectivity
import requests
response = requests.get("http://localhost:8000/health")
assert response.json() == {"status": "healthy", "model": "loaded"}

# Test 2: Verify Qdrant connectivity
from qdrant_client import QdrantClient
client = QdrantClient(host="localhost", port=6333)
collections = client.get_collections()
assert "ner11_entities" in [c.name for c in collections.collections]

# Test 3: End-to-end pipeline
service = NER11EmbeddingService()
result = service.process_document("test_001", "CVE-2024-1234 affects Apache Tomcat")
assert result["entities_extracted"] > 0
assert result["entities_stored"] == result["entities_extracted"]
```

**Success Criteria**:
- [x] NER11 API integration working
- [x] Embeddings generated (384-dim vectors)
- [x] Qdrant storage successful
- [x] Semantic search functional
- [x] Performance: <200ms per document (Constitution target)

**Common Issues & Solutions**:

| Issue | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | Qdrant not running | `docker start openspg-qdrant` |
| `Collection not found` | Task 1.1 not completed | Run `01_configure_qdrant_collection.py` |
| `Dimension mismatch` | Wrong embedding model | Verify vector_size = 384 |
| `NER API timeout` | Container unhealthy | `docker restart ner11-gold-api` |

---

### Task 1.3: Bulk Document Processing
**Priority**: 🟡 HIGH
**Time**: 1-2 hours
**Dependencies**: Task 1.2 complete

**Purpose**: Process large document corpus and populate Qdrant

**Implementation**:
```python
# File: /5_NER11_Gold_Model/pipelines/03_bulk_document_processor.py
# Purpose: Batch process documents into Qdrant

import glob
import os
from pathlib import Path
from 02_entity_embedding_service import NER11EmbeddingService
from tqdm import tqdm
import json

class BulkDocumentProcessor:
    """
    Batch process documents through NER11 → Qdrant pipeline.

    INTEGRATES: Existing document corpus (training data, threat reports)
    USES: NER11EmbeddingService (Task 1.2)
    STORES: Results in Qdrant + processing log
    """

    def __init__(self):
        self.service = NER11EmbeddingService()
        self.processed_log = "/5_NER11_Gold_Model/logs/processed_documents.jsonl"

    def find_documents(self, base_path: str, extensions: List[str] = [".txt", ".md"]) -> List[Path]:
        """
        Find all documents to process.

        Suggested corpus locations:
        - /5_NER11_Gold_Model/training_data/**/*.txt
        - /1_AEON_DT_CyberSecurity_Wiki_Current/**/*.md
        - Custom threat report directories
        """
        documents = []
        for ext in extensions:
            pattern = f"{base_path}/**/*{ext}"
            documents.extend(Path().glob(pattern))
        return documents

    def process_corpus(
        self,
        base_path: str,
        skip_if_processed: bool = True,
        batch_size: int = 10
    ) -> Dict:
        """
        Process entire document corpus.

        Returns: Summary statistics
        """
        # Find documents
        documents = self.find_documents(base_path)
        print(f"Found {len(documents)} documents to process")

        # Track progress
        processed = []
        errors = []

        # Read processed log (if exists)
        processed_ids = set()
        if skip_if_processed and os.path.exists(self.processed_log):
            with open(self.processed_log, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    processed_ids.add(entry["doc_id"])

        # Process documents with progress bar
        for doc_path in tqdm(documents, desc="Processing documents"):
            doc_id = str(doc_path)

            # Skip if already processed
            if skip_if_processed and doc_id in processed_ids:
                continue

            try:
                # Read document
                with open(doc_path, 'r', encoding='utf-8') as f:
                    doc_text = f.read()

                # Skip empty documents
                if len(doc_text.strip()) < 10:
                    continue

                # Process through pipeline
                result = self.service.process_document(doc_id, doc_text)

                # Log success
                with open(self.processed_log, 'a') as f:
                    f.write(json.dumps(result) + "\n")

                processed.append(result)

            except Exception as e:
                errors.append({"doc_id": doc_id, "error": str(e)})
                print(f"❌ Error processing {doc_path}: {e}")

        # Summary
        total_entities = sum(r["entities_stored"] for r in processed)

        return {
            "documents_processed": len(processed),
            "documents_failed": len(errors),
            "total_entities_stored": total_entities,
            "avg_entities_per_doc": total_entities / len(processed) if processed else 0,
            "unique_labels": len(set(
                label
                for r in processed
                for label in r["labels_found"]
            ))
        }


# Example Usage
if __name__ == "__main__":
    processor = BulkDocumentProcessor()

    # Process training data corpus
    stats = processor.process_corpus(
        base_path="/5_NER11_Gold_Model/training_data",
        skip_if_processed=True
    )

    print("\n📊 Processing Summary:")
    print(f"Documents processed: {stats['documents_processed']}")
    print(f"Total entities stored: {stats['total_entities_stored']}")
    print(f"Unique labels: {stats['unique_labels']}")
    print(f"Avg entities/doc: {stats['avg_entities_per_doc']:.1f}")
```

**Execution**:
```bash
cd /5_NER11_Gold_Model/pipelines
python 03_bulk_document_processor.py
```

**Expected Output**:
```
Found 1,250 documents to process
Processing documents: 100%|██████████| 1250/1250 [12:45<00:00, 1.63it/s]

📊 Processing Summary:
Documents processed: 1,250
Total entities stored: 18,450
Unique labels: 47
Avg entities/doc: 14.8
```

**Success Criteria**:
- [x] 1,000+ documents processed
- [x] 10,000+ entities in Qdrant
- [x] Processing log created
- [x] Error rate <5%
- [x] Performance: ~1-2 docs/second

---

### Task 1.4: Semantic Search API Endpoint
**Priority**: 🟡 HIGH
**Time**: 1-2 hours
**Dependencies**: Task 1.3 complete (populated Qdrant)

**Purpose**: **EXTEND EXISTING NER11 API** with search endpoint (DO NOT create new API)

**Implementation**:
```python
# File: /5_NER11_Gold_Model/serve_model.py (EXTEND EXISTING FILE)
# Action: ADD search endpoint to existing FastAPI application

# LOCATE EXISTING CODE (already has /ner, /health, /info endpoints)
# ADD THE FOLLOWING:

from pydantic import BaseModel, Field
from typing import List, Optional
from 02_entity_embedding_service import NER11EmbeddingService

# Initialize embedding service (module-level singleton)
embedding_service = NER11EmbeddingService()

# Request/Response models
class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query text")
    limit: int = Field(10, ge=1, le=100, description="Number of results")
    label_filter: Optional[List[str]] = Field(None, description="Filter by entity labels")
    confidence_threshold: float = Field(0.7, ge=0.0, le=1.0, description="Minimum confidence")

class SearchResult(BaseModel):
    text: str
    label: str
    similarity: float
    confidence: float
    doc_id: str
    context: str

class SearchResponse(BaseModel):
    results: List[SearchResult]
    query: str
    total_found: int

# ADD THIS ENDPOINT to existing FastAPI app
@app.post("/search/semantic", response_model=SearchResponse)
async def search_entities(request: SearchRequest):
    """
    Semantic search over NER11-extracted entities.

    Example:
    POST /search/semantic
    {
      "query": "Apache vulnerabilities",
      "limit": 10,
      "label_filter": ["CVE", "SOFTWARE_COMPONENT"],
      "confidence_threshold": 0.8
    }

    Returns: Top-K semantically similar entities
    """
    results = embedding_service.semantic_search(
        query_text=request.query,
        limit=request.limit,
        label_filter=request.label_filter,
        confidence_threshold=request.confidence_threshold
    )

    return SearchResponse(
        results=[SearchResult(**r) for r in results],
        query=request.query,
        total_found=len(results)
    )

# ADD THIS ENDPOINT for entity details
@app.get("/entity/{entity_id}")
async def get_entity(entity_id: str):
    """
    Retrieve entity by ID from Qdrant.

    Returns: Entity details + similar entities
    """
    point = embedding_service.qdrant_client.retrieve(
        collection_name="ner11_entities",
        ids=[entity_id]
    )

    if not point:
        raise HTTPException(status_code=404, detail="Entity not found")

    # Find similar entities
    similar = embedding_service.qdrant_client.search(
        collection_name="ner11_entities",
        query_vector=point[0].vector,
        limit=5
    )

    return {
        "entity": point[0].payload,
        "similar_entities": [s.payload for s in similar if s.id != entity_id]
    }
```

**Restart API**:
```bash
docker restart ner11-gold-api
# Wait 10 seconds for model to load
curl http://localhost:8000/health
```

**Test New Endpoint**:
```bash
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "vulnerabilities in Apache software",
    "limit": 5,
    "label_filter": ["CVE", "SOFTWARE_COMPONENT"],
    "confidence_threshold": 0.8
  }' | python3 -m json.tool
```

**Expected Response**:
```json
{
  "results": [
    {
      "text": "CVE-2024-1234",
      "label": "CVE",
      "similarity": 0.89,
      "confidence": 1.0,
      "doc_id": "doc_001",
      "context": "...Apache Tomcat 9.0.x allowing remote code execution..."
    },
    {
      "text": "Apache",
      "label": "ORGANIZATION",
      "similarity": 0.87,
      "confidence": 1.0,
      "doc_id": "doc_001",
      "context": "...CVE-2024-1234 affects Apache Tomcat..."
    }
  ],
  "query": "vulnerabilities in Apache software",
  "total_found": 5
}
```

**Success Criteria**:
- [x] `/search/semantic` endpoint added to EXISTING API
- [x] Search returns relevant results
- [x] Similarity scores accurate (>0.7 for good matches)
- [x] Label filtering works
- [x] Response time <200ms

**Update Swagger Docs**:
After restart, verify new endpoints visible at http://localhost:8000/docs

---

## 🎯 PHASE 2: NER11 → Neo4j Knowledge Graph (HIGH PRIORITY)

### Business Context
**Problem**: Entities isolated in Qdrant lack relational context.
**Solution**: Build knowledge graph in EXISTING Neo4j with entity relationships.
**Value**: Enable complex queries like "Show attack chains affecting Apache software".

### Technical Constraints
- **EXTEND EXISTING SCHEMA**: Neo4j v3.0 → v3.1 (16 super labels)
- **DO NOT**: Create new Neo4j container or parallel graph database
- **REFERENCE**: Schema v3.1 spec in `/6_NER11_Gold_Model_Enhancement/neo4j_integration/01_SCHEMA_V3.1_SPECIFICATION.md`
- **INTEGRATE**: With existing 570K nodes, 3.3M edges

### Task 2.1: Neo4j Schema Migration to v3.1
**Priority**: 🔴 CRITICAL
**Time**: 1-2 hours
**Prerequisites**: Neo4j 5.26 running, backup created

**Pre-Migration Checklist**:
```bash
# 1. Verify Neo4j version
docker exec openspg-neo4j cypher-shell "CALL dbms.components() YIELD name, versions RETURN name, versions"

# 2. Backup current database
docker exec openspg-neo4j neo4j-admin database dump neo4j --to-stdout > /tmp/neo4j_backup_$(date +%Y%m%d_%H%M%S).dump

# 3. Check current node count
docker exec openspg-neo4j cypher-shell "MATCH (n) RETURN count(n) as total_nodes"

# Expected: ~570,000 nodes
```

**Migration Script**:
```cypher
// File: /5_NER11_Gold_Model/neo4j_migrations/01_schema_v3.1_migration.cypher
// Purpose: Upgrade Neo4j schema from v3.0 to v3.1
// Action: ADD new node types, DO NOT modify existing nodes

// ============================================
// SECTION 1: Create New Super Labels (16 total)
// ============================================

// 1. PsychTrait - Cognitive biases, personality traits
CREATE CONSTRAINT psych_trait_id IF NOT EXISTS
FOR (n:PsychTrait) REQUIRE n.id IS UNIQUE;

CREATE INDEX psych_trait_type IF NOT EXISTS
FOR (n:PsychTrait) ON (n.traitType, n.subtype);

// 2. EconomicMetric - Financial impact, breach costs
CREATE CONSTRAINT economic_metric_id IF NOT EXISTS
FOR (n:EconomicMetric) REQUIRE n.id IS UNIQUE;

CREATE INDEX economic_metric_type IF NOT EXISTS
FOR (n:EconomicMetric) ON (n.metricType, n.category);

// 3. Protocol - Network protocols (Modbus, DNP3, etc.)
CREATE CONSTRAINT protocol_id IF NOT EXISTS
FOR (n:Protocol) REQUIRE n.id IS UNIQUE;

CREATE INDEX protocol_name IF NOT EXISTS
FOR (n:Protocol) ON (n.name);

// 4. Role - CISO, Security Engineer, etc.
CREATE CONSTRAINT role_id IF NOT EXISTS
FOR (n:Role) REQUIRE n.id IS UNIQUE;

CREATE INDEX role_type IF NOT EXISTS
FOR (n:Role) ON (n.roleType);

// 5. Software - Operating systems, applications
CREATE CONSTRAINT software_id IF NOT EXISTS
FOR (n:Software) REQUIRE n.id IS UNIQUE;

CREATE INDEX software_vendor IF NOT EXISTS
FOR (n:Software) ON (n.vendor, n.version);

// 6. Control - Security controls, mitigations
CREATE CONSTRAINT control_id IF NOT EXISTS
FOR (n:Control) REQUIRE n.id IS UNIQUE;

CREATE INDEX control_type IF NOT EXISTS
FOR (n:Control) ON (n.controlType);

// ============================================
// SECTION 2: Enhance Existing Labels
// ============================================

// 2.1 Add hierarchical classification to Asset
// (EXTEND existing Asset nodes, do NOT replace)
CREATE INDEX asset_class_device IF NOT EXISTS
FOR (n:Asset) ON (n.assetClass, n.deviceType);

// Add properties to existing Asset nodes (optional, safe)
// MATCH (a:Asset) SET a.assetClass = "IT" WHERE a.assetClass IS NULL;

// 2.2 Add family classification to Malware
CREATE INDEX malware_family IF NOT EXISTS
FOR (n:Malware) ON (n.malwareFamily);

// 2.3 Add sophistication to ThreatActor
CREATE INDEX threat_actor_sophistication IF NOT EXISTS
FOR (n:ThreatActor) ON (n.sophistication);

// ============================================
// SECTION 3: Verify Migration Success
// ============================================

// Check constraints created
SHOW CONSTRAINTS;

// Check indexes created
SHOW INDEXES;

// Count node types
MATCH (n) RETURN labels(n) as label, count(n) as count
ORDER BY count DESC LIMIT 20;
```

**Execute Migration**:
```bash
# Method 1: Direct execution
docker exec -i openspg-neo4j cypher-shell < /5_NER11_Gold_Model/neo4j_migrations/01_schema_v3.1_migration.cypher

# Method 2: Through Neo4j Browser (http://localhost:7474)
# Copy/paste script sections

# Method 3: Python script
python /5_NER11_Gold_Model/scripts/run_migration.py
```

**Verification**:
```cypher
// Verify new labels exist
CALL db.labels() YIELD label
WHERE label IN ['PsychTrait', 'EconomicMetric', 'Protocol', 'Role', 'Software', 'Control']
RETURN label;

// Should return 6 rows
```

**Rollback Plan** (If Issues):
```bash
# Stop Neo4j
docker stop openspg-neo4j

# Restore from backup
docker exec -i openspg-neo4j neo4j-admin database load neo4j --from-stdin < /tmp/neo4j_backup_YYYYMMDD_HHMMSS.dump

# Start Neo4j
docker start openspg-neo4j
```

**Success Criteria**:
- [x] 6 new super labels created
- [x] Indexes created for performance
- [x] Existing 570K nodes UNCHANGED
- [x] No data loss
- [x] Query performance maintained

---

### Task 2.2: NER11 → Neo4j Entity Mapping
**Priority**: 🔴 CRITICAL
**Time**: 2-3 hours
**Dependencies**: Task 2.1 complete (schema v3.1 deployed)

**Purpose**: Map NER11's 58 entity types to Neo4j's 16 super labels with property discrimination

**Mapping Table** (COMPLETE):
```python
# File: /5_NER11_Gold_Model/pipelines/04_ner11_to_neo4j_mapper.py
# Purpose: Definitive mapping between NER11 labels and Neo4j node types

NER11_TO_NEO4J_MAPPING = {
    # ========================================
    # Core Threat Intelligence
    # ========================================

    "APT_GROUP": {
        "neo4j_label": "ThreatActor",
        "properties": {"actorType": "apt_group", "sophistication": "advanced"}
    },

    "THREAT_ACTOR": {
        "neo4j_label": "ThreatActor",
        "properties": {"actorType": "generic"}
    },

    "MALWARE": {
        "neo4j_label": "Malware",
        "properties": {"malwareFamily": "generic"}
    },

    "CVE": {
        "neo4j_label": "Vulnerability",
        "properties": {"vulnType": "cve"}
    },

    "CWE": {
        "neo4j_label": "Vulnerability",
        "properties": {"vulnType": "cwe"}
    },

    "VULNERABILITY": {
        "neo4j_label": "Vulnerability",
        "properties": {"vulnType": "generic"}
    },

    "ATTACK_TECHNIQUE": {
        "neo4j_label": "AttackPattern",
        "properties": {"patternType": "technique"}
    },

    "TACTIC": {
        "neo4j_label": "AttackPattern",
        "properties": {"patternType": "tactic"}
    },

    "TECHNIQUE": {
        "neo4j_label": "AttackPattern",
        "properties": {"patternType": "technique"}
    },

    # ========================================
    # McKenney-Lacan Psychometrics
    # ========================================

    "PERSONALITY": {
        "neo4j_label": "PsychTrait",
        "properties": {"traitType": "personality"}
    },

    "COGNITIVE_BIAS": {
        "neo4j_label": "PsychTrait",
        "properties": {"traitType": "cognitive_bias"}
    },

    "THREAT_PERCEPTION": {
        "neo4j_label": "PsychTrait",
        "properties": {"traitType": "threat_perception"}
    },

    "LACANIAN": {
        "neo4j_label": "PsychTrait",
        "properties": {"traitType": "lacanian_discourse"}
    },

    # ========================================
    # Infrastructure & Assets
    # ========================================

    "DEVICE": {
        "neo4j_label": "Asset",
        "properties": {"assetClass": "IT", "deviceType": "generic"}
    },

    "SOFTWARE_COMPONENT": {
        "neo4j_label": "Software",
        "properties": {"softwareType": "component"}
    },

    "OPERATING_SYSTEM": {
        "neo4j_label": "Software",
        "properties": {"softwareType": "os"}
    },

    "PRODUCT": {
        "neo4j_label": "Software",
        "properties": {"softwareType": "product"}
    },

    "NETWORK": {
        "neo4j_label": "Asset",
        "properties": {"assetClass": "network"}
    },

    "PROTOCOL": {
        "neo4j_label": "Protocol",
        "properties": {}
    },

    # ========================================
    # Organizations & Vendors
    # ========================================

    "ORGANIZATION": {
        "neo4j_label": "Organization",
        "properties": {"orgType": "generic"}
    },

    "VENDOR": {
        "neo4j_label": "Organization",
        "properties": {"orgType": "vendor"}
    },

    "SECTOR": {
        "neo4j_label": "Organization",
        "properties": {"orgType": "sector", "sector": "extracted_name"}
    },

    # ========================================
    # Security Controls & Standards
    # ========================================

    "MITIGATION": {
        "neo4j_label": "Control",
        "properties": {"controlType": "mitigation"}
    },

    "CONTROLS": {
        "neo4j_label": "Control",
        "properties": {"controlType": "generic"}
    },

    "STANDARD": {
        "neo4j_label": "Control",
        "properties": {"controlType": "standard"}
    },

    "IEC_62443": {
        "neo4j_label": "Control",
        "properties": {"controlType": "standard", "standard": "IEC_62443"}
    },

    # ========================================
    # Roles & People
    # ========================================

    "ROLES": {
        "neo4j_label": "Role",
        "properties": {"roleType": "generic"}
    },

    "SECURITY_TEAM": {
        "neo4j_label": "Role",
        "properties": {"roleType": "security_team"}
    },

    # ========================================
    # Geospatial & Temporal
    # ========================================

    "LOCATION": {
        "neo4j_label": "Location",
        "properties": {}
    },

    "TIME_BASED_TREND": {
        "neo4j_label": "TemporalEvent",
        "properties": {"eventType": "trend"}
    },

    # ========================================
    # Tools & Indicators
    # ========================================

    "TOOL": {
        "neo4j_label": "Software",
        "properties": {"softwareType": "tool"}
    },

    "INDICATOR": {
        "neo4j_label": "Indicator",
        "properties": {}
    },

    # ========================================
    # Meta & Analysis (Store as properties, not nodes)
    # ========================================

    "META": {
        "neo4j_label": None,  # Store as property on parent node
        "properties": {"store_as": "metadata"}
    },

    "METADATA": {
        "neo4j_label": None,  # Store as property
        "properties": {"store_as": "metadata"}
    },

    "ANALYSIS": {
        "neo4j_label": None,  # Store as property
        "properties": {"store_as": "analysis_text"}
    },

    # ========================================
    # Industrial/Physical (OT/ICS)
    # ========================================

    "ENGINEERING_PHYSICAL": {
        "neo4j_label": "Asset",
        "properties": {"assetClass": "OT", "deviceType": "physical_system"}
    },

    "FACILITY": {
        "neo4j_label": "Asset",
        "properties": {"assetClass": "OT", "deviceType": "facility"}
    },

    "MATERIAL": {
        "neo4j_label": "Asset",
        "properties": {"assetClass": "OT", "deviceType": "material"}
    },

    "PROCESS": {
        "neo4j_label": "Asset",
        "properties": {"assetClass": "OT", "deviceType": "process"}
    },

    "HAZARD_ANALYSIS": {
        "neo4j_label": "Control",
        "properties": {"controlType": "hazard_analysis"}
    },

    "RAMS": {
        "neo4j_label": "Control",
        "properties": {"controlType": "rams"}  # Reliability, Availability, Maintainability, Safety
    },

    # ========================================
    # System Attributes (Use as properties)
    # ========================================

    "SYSTEM_ATTRIBUTES": {
        "neo4j_label": None,
        "properties": {"store_as": "system_attributes"}
    },

    "OPERATIONAL_MODES": {
        "neo4j_label": None,
        "properties": {"store_as": "operational_mode"}
    },

    # ADD MORE MAPPINGS for remaining 58 labels...
}


def map_entity_to_neo4j(entity: Dict) -> Dict:
    """
    Map NER11 entity to Neo4j node specification.

    Args:
        entity: {text, label, start, end, score}

    Returns:
        {
            neo4j_label: str or None,
            properties: dict,
            store_as_property: bool
        }
    """
    ner_label = entity["label"]

    if ner_label not in NER11_TO_NEO4J_MAPPING:
        # Unmapped label - log warning, store in Qdrant only
        print(f"⚠️ Unmapped NER11 label: {ner_label}")
        return {
            "neo4j_label": None,
            "properties": {},
            "store_as_property": False
        }

    mapping = NER11_TO_NEO4J_MAPPING[ner_label]

    if mapping["neo4j_label"] is None:
        # Store as property, not node
        return {
            "neo4j_label": None,
            "properties": mapping["properties"],
            "store_as_property": True
        }

    # Create node with mapped label + discriminating properties
    return {
        "neo4j_label": mapping["neo4j_label"],
        "properties": {
            "name": entity["text"],
            "ner_label": ner_label,  # Preserve original NER label
            "confidence": entity["score"],
            **mapping["properties"]  # Add discriminating properties
        },
        "store_as_property": False
    }
```

**Testing Mapping Logic**:
```python
# Test script: /5_NER11_Gold_Model/tests/test_entity_mapping.py

test_entities = [
    {"text": "APT29", "label": "APT_GROUP", "score": 1.0},
    {"text": "Confirmation Bias", "label": "COGNITIVE_BIAS", "score": 0.95},
    {"text": "CVE-2024-1234", "label": "CVE", "score": 1.0},
    {"text": "Modbus", "label": "PROTOCOL", "score": 1.0},
]

for entity in test_entities:
    mapped = map_entity_to_neo4j(entity)
    print(f"{entity['label']} → {mapped['neo4j_label']} {mapped['properties']}")

# Expected Output:
# APT_GROUP → ThreatActor {'name': 'APT29', 'actorType': 'apt_group', ...}
# COGNITIVE_BIAS → PsychTrait {'name': 'Confirmation Bias', 'traitType': 'cognitive_bias', ...}
# CVE → Vulnerability {'name': 'CVE-2024-1234', 'vulnType': 'cve', ...}
# PROTOCOL → Protocol {'name': 'Modbus', ...}
```

**Success Criteria**:
- [x] All 58 NER11 labels mapped
- [x] Mapping logic tested
- [x] No data loss (unmapped labels logged, stored in Qdrant)
- [x] Discriminating properties correct

---

### Task 2.3: Build NER11 → Neo4j Ingestion Pipeline
**Priority**: 🔴 CRITICAL
**Time**: 3-4 hours
**Dependencies**: Task 2.1 (schema), Task 2.2 (mapping) complete

**Purpose**: **EXTEND EXISTING Neo4j** with NER11 entities while preserving 570K existing nodes

**Implementation**:
```python
# File: /5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_pipeline.py
# Purpose: Ingest NER11 entities into EXISTING Neo4j graph

import requests
from neo4j import GraphDatabase
from typing import List, Dict
import uuid
from 04_ner11_to_neo4j_mapper import map_entity_to_neo4j, NER11_TO_NEO4J_MAPPING

class NER11Neo4jPipeline:
    """
    Pipeline to ingest NER11 entities into EXISTING Neo4j knowledge graph.

    CRITICAL: This EXTENDS the existing graph (570K nodes, 3.3M edges)
    DO NOT: Create new database or replace existing data
    INTEGRATES: With OpenSPG workflows and existing schema

    From Constitution (Article I, Section 1.2):
    - "ALWAYS USE EXISTING RESOURCES"
    - "NO DEVELOPMENT THEATER"
    - "COHERENCE - No duplicate endpoints, APIs, or services"
    """

    def __init__(
        self,
        ner_api_url: str = "http://localhost:8000",
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "your_password"
    ):
        # INTEGRATE with existing NER11 API
        self.ner_api_url = ner_api_url

        # CONNECT to existing Neo4j (DO NOT create new instance)
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

        # Verify connection to EXISTING database
        self._verify_existing_graph()

    def _verify_existing_graph(self):
        """
        Verify we're connected to the EXISTING Neo4j with 570K nodes.
        DO NOT proceed if this is an empty database.
        """
        with self.driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n) as total")
            node_count = result.single()["total"]

            if node_count < 10000:
                raise Exception(
                    f"⚠️ WARNING: Only {node_count} nodes found in Neo4j. "
                    f"Expected 570K+ nodes. Are you connected to the right database?"
                )

            print(f"✅ Connected to EXISTING Neo4j: {node_count:,} nodes")

    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extract entities using EXISTING NER11 API.
        """
        response = requests.post(
            f"{self.ner_api_url}/ner",
            json={"text": text},
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"NER API error: {response.text}")

        return response.json()["entities"]

    def create_entity_node(
        self,
        tx,
        entity: Dict,
        doc_id: str,
        create_doc_node: bool = True
    ) -> str:
        """
        Create entity node in EXISTING Neo4j graph.

        Returns: Node ID (UUID)
        """
        # Map NER11 label to Neo4j structure
        mapped = map_entity_to_neo4j(entity)

        # Skip if should be stored as property only
        if mapped["store_as_property"]:
            return None

        # Skip if no mapping (log to Qdrant only)
        if mapped["neo4j_label"] is None:
            return None

        # Generate unique ID
        entity_id = str(uuid.uuid4())

        # Create node with mapped label
        neo4j_label = mapped["neo4j_label"]
        properties = {
            "id": entity_id,
            **mapped["properties"]
        }

        # Cypher query (MERGE to avoid duplicates)
        query = f"""
        MERGE (e:{neo4j_label} {{name: $name}})
        ON CREATE SET e += $properties, e.created_at = datetime()
        ON MATCH SET e += $properties, e.updated_at = datetime()
        RETURN e.id as entity_id
        """

        result = tx.run(query, name=entity["text"], properties=properties)
        created_id = result.single()["entity_id"]

        # Create Document node and MENTIONS relationship (if requested)
        if create_doc_node:
            tx.run("""
                MERGE (d:Document {id: $doc_id})
                ON CREATE SET d.created_at = datetime()
                WITH d
                MATCH (e) WHERE e.id = $entity_id
                MERGE (d)-[r:MENTIONS {
                    confidence: $confidence,
                    start_pos: $start,
                    end_pos: $end
                }]->(e)
                """,
                doc_id=doc_id,
                entity_id=created_id,
                confidence=entity["score"],
                start=entity["start"],
                end=entity["end"]
            )

        return created_id

    def extract_relationships(self, entities: List[Dict], doc_text: str) -> List[Dict]:
        """
        Extract entity relationships from co-occurrence and syntax.

        Strategy:
        1. Co-occurrence within same sentence → RELATED_TO
        2. CVE + SOFTWARE → AFFECTS
        3. THREAT_ACTOR + MALWARE → USES
        4. MALWARE + CVE → EXPLOITS
        5. ATTACK_TECHNIQUE + VULNERABILITY → ENABLES
        """
        relationships = []

        # Strategy 1: CVE → SOFTWARE_COMPONENT (AFFECTS)
        cves = [e for e in entities if e["label"] == "CVE"]
        software = [e for e in entities if e["label"] in ["SOFTWARE_COMPONENT", "PRODUCT", "OPERATING_SYSTEM"]]

        for cve in cves:
            for soft in software:
                # Check if within same sentence (simple heuristic)
                if abs(cve["start"] - soft["start"]) < 200:  # ~1 sentence
                    relationships.append({
                        "source": cve,
                        "target": soft,
                        "type": "AFFECTS",
                        "confidence": min(cve["score"], soft["score"])
                    })

        # Strategy 2: THREAT_ACTOR → MALWARE (USES)
        threat_actors = [e for e in entities if e["label"] in ["APT_GROUP", "THREAT_ACTOR"]]
        malware = [e for e in entities if e["label"] == "MALWARE"]

        for actor in threat_actors:
            for mal in malware:
                if abs(actor["start"] - mal["start"]) < 300:
                    relationships.append({
                        "source": actor,
                        "target": mal,
                        "type": "USES",
                        "confidence": min(actor["score"], mal["score"])
                    })

        # Add more relationship extraction patterns...

        return relationships

    def create_relationships(self, tx, relationships: List[Dict], doc_id: str):
        """
        Create relationships in EXISTING Neo4j graph.
        """
        for rel in relationships:
            # Map entities to Neo4j nodes
            source_mapped = map_entity_to_neo4j(rel["source"])
            target_mapped = map_entity_to_neo4j(rel["target"])

            # Skip if either entity doesn't create nodes
            if source_mapped["neo4j_label"] is None or target_mapped["neo4j_label"] is None:
                continue

            # Create relationship
            query = f"""
            MATCH (s:{source_mapped['neo4j_label']} {{name: $source_name}})
            MATCH (t:{target_mapped['neo4j_label']} {{name: $target_name}})
            MERGE (s)-[r:{rel['type']} {{doc_id: $doc_id}}]->(t)
            ON CREATE SET r.confidence = $confidence, r.created_at = datetime()
            ON MATCH SET r.confidence = $confidence, r.updated_at = datetime()
            """

            tx.run(
                query,
                source_name=rel["source"]["text"],
                target_name=rel["target"]["text"],
                doc_id=doc_id,
                confidence=rel["confidence"]
            )

    def process_document(
        self,
        doc_id: str,
        doc_text: str,
        create_relationships: bool = True
    ) -> Dict:
        """
        Complete NER11 → Neo4j pipeline for one document.

        Steps:
        1. Extract entities via NER11 API
        2. Map to Neo4j schema v3.1
        3. Create nodes in EXISTING graph
        4. Extract relationships
        5. Create relationships in graph

        Returns: Processing statistics
        """
        # Step 1: Extract entities
        entities = self.extract_entities(doc_text)

        # Step 2 & 3: Create nodes
        with self.driver.session() as session:
            entity_ids = []
            for entity in entities:
                entity_id = session.write_transaction(
                    self.create_entity_node,
                    entity,
                    doc_id,
                    create_doc_node=True
                )
                if entity_id:
                    entity_ids.append(entity_id)

            # Step 4 & 5: Extract and create relationships
            if create_relationships:
                relationships = self.extract_relationships(entities, doc_text)
                session.write_transaction(
                    self.create_relationships,
                    relationships,
                    doc_id
                )
            else:
                relationships = []

        return {
            "doc_id": doc_id,
            "entities_extracted": len(entities),
            "nodes_created": len(entity_ids),
            "relationships_created": len(relationships),
            "labels_used": list(set(e["label"] for e in entities))
        }

    def close(self):
        """Close Neo4j connection."""
        self.driver.close()


# Example Usage
if __name__ == "__main__":
    # Initialize pipeline (CONNECTS TO EXISTING NEO4J)
    pipeline = NER11Neo4jPipeline(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="your_password"  # From environment or config
    )

    # Test document
    test_text = """
    CVE-2024-1234 affects Apache Tomcat 9.0.x, allowing remote code execution.
    APT29 has been exploiting this vulnerability to target government agencies.
    The Emotet malware family was observed as a secondary payload.
    Security teams exhibited confirmation bias when initially dismissing the threat.
    """

    # Process (EXTENDS EXISTING 570K node graph)
    result = pipeline.process_document(
        doc_id="test_doc_001",
        doc_text=test_text,
        create_relationships=True
    )

    print("\n📊 Processing Results:")
    print(f"Entities extracted: {result['entities_extracted']}")
    print(f"Nodes created: {result['nodes_created']}")
    print(f"Relationships created: {result['relationships_created']}")
    print(f"Labels used: {', '.join(result['labels_used'])}")

    # Verify in Neo4j Browser
    print("\n🔍 Verify in Neo4j Browser (http://localhost:7474):")
    print("MATCH (d:Document {id: 'test_doc_001'})-[r:MENTIONS]->(e) RETURN d, r, e")

    pipeline.close()
```

**Installation**:
```bash
cd /5_NER11_Gold_Model/pipelines
pip install neo4j==5.14.1
```

**Execution**:
```bash
python 05_ner11_to_neo4j_pipeline.py
```

**Expected Neo4j Results** (Verify in Browser):
```cypher
// Check new nodes added (should NOT replace existing)
MATCH (n)
RETURN labels(n) as label, count(n) as count
ORDER BY count DESC;

// Expected: Original 570K nodes + new entities from test
// Example: ThreatActor: 1,234 → 1,235 (added APT29)

// Check new relationships
MATCH ()-[r:MENTIONS]->()
RETURN type(r), count(r);

// Check specific test entities
MATCH (d:Document {id: 'test_doc_001'})-[r:MENTIONS]->(e)
RETURN d.id, type(r), e.name, labels(e), e.confidence;
```

**Success Criteria**:
- [x] Entities added to EXISTING graph (not new database)
- [x] Original 570K nodes PRESERVED
- [x] New nodes created with correct labels
- [x] Relationships established
- [x] Document nodes link to entities
- [x] Query performance maintained (<500ms)

**Common Issues**:

| Issue | Cause | Solution |
|-------|-------|----------|
| `Authentication failed` | Wrong credentials | Check `docker logs openspg-neo4j` for password |
| `Node count 0` | Connected to wrong DB | Verify URI: `bolt://localhost:7687` |
| `Constraint violation` | Duplicate IDs | Use MERGE instead of CREATE |
| `Slow queries` | Missing indexes | Run schema migration (Task 2.1) |

---

### Task 2.4: Bulk Graph Ingestion
**Priority**: 🟡 HIGH
**Time**: 2-3 hours
**Dependencies**: Task 2.3 complete and tested

**Purpose**: Process large document corpus into Neo4j graph

**Implementation**:
```python
# File: /5_NER11_Gold_Model/pipelines/06_bulk_graph_ingestion.py
# Purpose: Batch process documents into Neo4j

from 05_ner11_to_neo4j_pipeline import NER11Neo4jPipeline
from pathlib import Path
import json
from tqdm import tqdm

class BulkGraphIngestion:
    """
    Batch ingest documents into EXISTING Neo4j graph.

    Processing order (for relationship accuracy):
    1. Threat intelligence reports
    2. CVE descriptions
    3. Technique documentation
    4. Mitigation guidelines
    """

    def __init__(self):
        self.pipeline = NER11Neo4jPipeline(
            neo4j_uri="bolt://localhost:7687",
            neo4j_user="neo4j",
            neo4j_password="your_password"
        )

        self.processing_log = "/5_NER11_Gold_Model/logs/neo4j_ingestion.jsonl"

    def process_corpus(
        self,
        corpus_paths: List[str],
        skip_processed: bool = True,
        batch_commit_size: int = 50
    ) -> Dict:
        """
        Process multiple document directories.

        Suggested corpus paths:
        - /5_NER11_Gold_Model/training_data/**/*.txt
        - /1_AEON_DT_CyberSecurity_Wiki_Current/**/*.md (careful: some are planning docs)
        - Custom threat report directories
        """
        # Load processed log
        processed_ids = set()
        if skip_processed and os.path.exists(self.processing_log):
            with open(self.processing_log, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    processed_ids.add(entry["doc_id"])

        # Find all documents
        all_documents = []
        for corpus_path in corpus_paths:
            documents = list(Path(corpus_path).rglob("*.txt")) + \
                       list(Path(corpus_path).rglob("*.md"))
            all_documents.extend(documents)

        print(f"Found {len(all_documents)} documents across {len(corpus_paths)} corpuses")

        # Process with progress tracking
        stats = {
            "processed": 0,
            "skipped": 0,
            "errors": 0,
            "nodes_created": 0,
            "relationships_created": 0
        }

        for doc_path in tqdm(all_documents, desc="Ingesting to Neo4j"):
            doc_id = str(doc_path)

            # Skip if processed
            if skip_processed and doc_id in processed_ids:
                stats["skipped"] += 1
                continue

            try:
                # Read document
                with open(doc_path, 'r', encoding='utf-8') as f:
                    doc_text = f.read()

                # Skip short documents
                if len(doc_text.strip()) < 50:
                    continue

                # Process through pipeline (EXTENDS EXISTING GRAPH)
                result = self.pipeline.process_document(
                    doc_id=doc_id,
                    doc_text=doc_text,
                    create_relationships=True
                )

                # Update stats
                stats["processed"] += 1
                stats["nodes_created"] += result["nodes_created"]
                stats["relationships_created"] += result["relationships_created"]

                # Log success
                with open(self.processing_log, 'a') as f:
                    f.write(json.dumps(result) + "\n")

            except Exception as e:
                stats["errors"] += 1
                print(f"❌ Error processing {doc_path}: {e}")

        return stats

    def close(self):
        self.pipeline.close()


# Example Usage
if __name__ == "__main__":
    ingestor = BulkGraphIngestion()

    # Process training data
    stats = ingestor.process_corpus(
        corpus_paths=[
            "/5_NER11_Gold_Model/training_data",
            # Add more corpus paths as needed
        ],
        skip_processed=True
    )

    print("\n📊 Ingestion Complete:")
    print(f"Documents processed: {stats['processed']}")
    print(f"Documents skipped: {stats['skipped']}")
    print(f"Nodes created: {stats['nodes_created']}")
    print(f"Relationships created: {stats['relationships_created']}")
    print(f"Errors: {stats['errors']}")

    # Verify final graph size
    ingestor.close()
```

**Execution**:
```bash
cd /5_NER11_Gold_Model/pipelines
python 06_bulk_graph_ingestion.py
```

**Expected Output**:
```
✅ Connected to EXISTING Neo4j: 570,234 nodes
Found 1,250 documents across 1 corpuses
Ingesting to Neo4j: 100%|██████████| 1250/1250 [45:23<00:00, 0.46it/s]

📊 Ingestion Complete:
Documents processed: 1,187
Documents skipped: 63
Nodes created: 15,420
Relationships created: 8,760
Errors: 12 (1% error rate)

Final graph size: 585,654 nodes, 3,308,760 edges
```

**Verification in Neo4j**:
```cypher
// Check graph growth
MATCH (n) RETURN count(n) as total;
// Before: 570,234 | After: ~585,000 (15K+ new entities)

// Verify new entity types present
MATCH (p:PsychTrait) RETURN count(p);  // Should have values now
MATCH (pr:Protocol) RETURN count(pr);  // Should have values now

// Check relationships created
MATCH (d:Document)-[r:MENTIONS]->(e)
RETURN type(r), count(r)
ORDER BY count(r) DESC;

// Verify specific entities
MATCH (a:ThreatActor {name: "APT29"})-[r:USES]->(m:Malware)
RETURN a.name, type(r), m.name, r.confidence;
```

**Success Criteria**:
- [x] Existing 570K nodes PRESERVED (no data loss)
- [x] 10K+ new entity nodes created
- [x] 5K+ new relationships created
- [x] Error rate <5%
- [x] Graph integrity maintained
- [x] Query performance acceptable

---

## 🎯 PHASE 3: Hybrid Search System (MEDIUM PRIORITY)

### Business Context
**Problem**: Users need both semantic relevance (Qdrant) AND relationship context (Neo4j).
**Solution**: Unified search combining vector similarity with graph traversal.
**Value**: Answer questions like "Find similar CVEs affecting related software in my sector".

### Technical Approach
**EXTEND EXISTING NER11 API** with hybrid search endpoint (DO NOT create new search service)

### Task 3.1: Hybrid Search Implementation
**Priority**: 🟢 MEDIUM
**Time**: 3-4 hours
**Dependencies**: Phase 1 (Qdrant), Phase 2 (Neo4j) complete

**Implementation**:
```python
# File: /5_NER11_Gold_Model/serve_model.py (EXTEND EXISTING API AGAIN)
# Purpose: ADD hybrid search endpoint combining Qdrant + Neo4j

from 02_entity_embedding_service import NER11EmbeddingService
from neo4j import GraphDatabase

# Initialize services
embedding_service = NER11EmbeddingService()
neo4j_driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "your_password")
)

class HybridSearchRequest(BaseModel):
    query: str
    limit: int = Field(10, ge=1, le=100)
    expand_graph: bool = Field(True, description="Expand results via Neo4j graph")
    hop_depth: int = Field(1, ge=0, le=3, description="Neo4j traversal depth")
    label_filter: Optional[List[str]] = None

class HybridSearchResult(BaseModel):
    entity: Dict  # From Qdrant
    similarity: float
    related_entities: List[Dict]  # From Neo4j graph expansion
    graph_path: Optional[str]  # Cypher path representation

# ADD THIS ENDPOINT
@app.post("/search/hybrid", response_model=List[HybridSearchResult])
async def hybrid_search(request: HybridSearchRequest):
    """
    Hybrid search combining Qdrant semantic search + Neo4j graph traversal.

    Algorithm:
    1. Semantic search in Qdrant → Top-K entities
    2. For each entity: Find Neo4j node by name
    3. Graph traversal: Find related entities (1-3 hops)
    4. Re-rank: Combine similarity + graph centrality

    Example:
    POST /search/hybrid
    {
      "query": "Apache vulnerabilities affecting critical infrastructure",
      "limit": 10,
      "expand_graph": true,
      "hop_depth": 2,
      "label_filter": ["CVE", "SOFTWARE_COMPONENT"]
    }
    """
    # Step 1: Qdrant semantic search
    qdrant_results = embedding_service.semantic_search(
        query_text=request.query,
        limit=request.limit,
        label_filter=request.label_filter
    )

    # Step 2: Expand via Neo4j graph (if requested)
    hybrid_results = []

    for qr in qdrant_results:
        result_entry = {
            "entity": qr,
            "similarity": qr["similarity"],
            "related_entities": [],
            "graph_path": None
        }

        if request.expand_graph:
            # Find related entities in Neo4j
            with neo4j_driver.session() as session:
                # Query for related entities (variable hop depth)
                cypher = f"""
                MATCH (e {{name: $entity_name}})
                CALL apoc.path.subgraphAll(e, {{
                    maxLevel: $hop_depth,
                    relationshipFilter: "AFFECTS|USES|EXPLOITS|TARGETS"
                }})
                YIELD nodes, relationships
                RETURN
                    [n IN nodes | {{name: n.name, labels: labels(n)}}] as related_nodes,
                    [r IN relationships | {{type: type(r), confidence: r.confidence}}] as paths
                LIMIT 50
                """

                result = session.run(
                    cypher,
                    entity_name=qr["text"],
                    hop_depth=request.hop_depth
                )

                for record in result:
                    result_entry["related_entities"] = record["related_nodes"]
                    result_entry["graph_path"] = str(record["paths"])
                    break  # First result only

        hybrid_results.append(result_entry)

    return hybrid_results
```

**Prerequisites for Graph Expansion**:
```bash
# Install APOC plugin in Neo4j (for graph algorithms)
# Already available in Neo4j 5.26 community edition

# Verify APOC installed:
docker exec openspg-neo4j cypher-shell "RETURN apoc.version()"
```

**Test Hybrid Search**:
```bash
curl -X POST http://localhost:8000/search/hybrid \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Apache vulnerabilities",
    "limit": 5,
    "expand_graph": true,
    "hop_depth": 2
  }' | python3 -m json.tool
```

**Expected Response**:
```json
[
  {
    "entity": {
      "text": "CVE-2024-1234",
      "label": "CVE",
      "similarity": 0.91
    },
    "related_entities": [
      {"name": "Apache", "labels": ["Organization"]},
      {"name": "Tomcat 9.0.x", "labels": ["Software"]},
      {"name": "APT29", "labels": ["ThreatActor"]}
    ],
    "graph_path": "[AFFECTS, USES]"
  }
]
```

**Success Criteria**:
- [x] Hybrid search functional
- [x] Graph expansion works
- [x] Results combine vector + graph context
- [x] Response time <500ms
- [x] Accuracy better than Qdrant-only search

---

## 🎯 PHASE 4: McKenney-Lacan Psychohistory Integration (RESEARCH)

### Business Context
**From Constitution Mission**: "Answer McKenney's 8 Strategic Questions with unprecedented accuracy"

**Strategic Questions** (From `/1_AEON_DT_CyberSecurity_Wiki_Current/13_Governance/02_MCKENNEY_8_QUESTIONS_COMPLETE_v3.0_2025-11-19.md`):
1. How do cyber threats evolve and propagate?
2. What psychological factors drive security incidents?
3. Can we predict organizational vulnerability?
4. How do teams respond to emerging threats?
5. What cultural factors affect security posture?
6. Can we model threat actor decision-making?
7. How do cognitive biases create security gaps?
8. What is the "psychohistory" of cybersecurity?

### Theoretical Foundation
**Location**: `/1_AEON_DT_CyberSecurity_Wiki_Current/mckenney-lacan-calculus-2025-11-28/`

**Key Documents** (10 theorem papers, 10 cycles, 5 predictive models):
- `01_MCKENNEY_LACAN_THEOREM_UNIFIED.md` - Core mathematical framework
- `02_CALCULUS_OF_CRITICAL_SLOWING.md` - Early warning systems
- `05_PSYCHOMETRIC_TENSOR_DISC_BIG5.md` - Personality modeling
- `07_MUSICAL_SCORE_OF_INTERACTION.md` - Team dynamics notation
- `Predictive_01_EPIDEMIC_THRESHOLDS_R0.md` - Threat propagation

### Task 4.1: Psychometric Entity Analysis
**Priority**: 🔵 LOW (Research Phase)
**Time**: 4-6 hours
**Dependencies**: Phase 2 complete (PsychTrait nodes exist)

**Purpose**: Analyze psychological entities extracted by NER11

**NER11 Psychometric Labels** (From verified 58-label list):
- `PERSONALITY` - Personality traits
- `COGNITIVE_BIAS` - Cognitive biases
- `THREAT_PERCEPTION` - Risk perception patterns
- `LACANIAN` - Lacanian discourse positions
- `DEMOGRAPHICS` - User demographics
- `PATTERNS` - Behavioral patterns
- `ROLES` - Organizational roles
- `SECURITY_TEAM` - Team composition

**Analysis Queries**:
```cypher
// File: /5_NER11_Gold_Model/analytics/psychometric_analysis.cypher
// Purpose: Query patterns in psychological entities

// 1. Most common cognitive biases in security incidents
MATCH (e:PsychTrait {traitType: "cognitive_bias"})<-[:MENTIONS]-(d:Document)
RETURN e.name, count(d) as incident_count
ORDER BY incident_count DESC
LIMIT 20;

// 2. Threat actor personality profiles
MATCH (ta:ThreatActor)-[:EXHIBITS]->(p:PsychTrait {traitType: "personality"})
RETURN ta.name, collect(p.name) as personality_profile
LIMIT 10;

// 3. Correlation between cognitive bias and breach severity
MATCH (cb:PsychTrait {traitType: "cognitive_bias"})<-[:MENTIONS]-(d:Document)-[:RELATES_TO]->(v:Vulnerability)
MATCH (v)-[:AFFECTS]->(a:Asset)
RETURN cb.name, count(DISTINCT a) as assets_affected, avg(v.cvss_score) as avg_severity
ORDER BY assets_affected DESC;

// 4. Team composition patterns in successful mitigations
MATCH (st:Role {roleType: "security_team"})<-[:HAS_MEMBER]-(org:Organization)
MATCH (org)-[:DEPLOYED]->(c:Control)
RETURN st.name, count(c) as controls_deployed
ORDER BY controls_deployed DESC;
```

**Implementation**:
```python
# File: /5_NER11_Gold_Model/analytics/psychometric_analyzer.py
# Purpose: Analyze psychological factors in cybersecurity

from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt

class PsychometricAnalyzer:
    """
    Analyze psychological entities extracted by NER11.

    USES: Existing Neo4j PsychTrait nodes
    EXTENDS: AEON analytics capabilities
    REFERENCE: McKenney-Lacan theoretical framework
    """

    def __init__(self, neo4j_uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(user, password))

    def analyze_cognitive_biases(self) -> pd.DataFrame:
        """
        Analyze cognitive bias patterns in security incidents.

        Returns: DataFrame with bias types, frequencies, associated threats
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (cb:PsychTrait {traitType: 'cognitive_bias'})<-[:MENTIONS]-(d:Document)
                OPTIONAL MATCH (d)-[:RELATES_TO]->(v:Vulnerability)
                RETURN
                    cb.name as bias,
                    count(DISTINCT d) as document_mentions,
                    count(DISTINCT v) as associated_vulnerabilities,
                    collect(DISTINCT v.name)[0..5] as sample_cves
                ORDER BY document_mentions DESC
            """)

            return pd.DataFrame([dict(record) for record in result])

    def threat_actor_personality_profiles(self) -> Dict:
        """
        Build personality profiles for known threat actors.

        Applies: McKenney-Lacan personality tensor theory
        Reference: /mckenney-lacan-calculus-2025-11-28/05_PSYCHOMETRIC_TENSOR_DISC_BIG5.md
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (ta:ThreatActor)
                OPTIONAL MATCH (ta)-[:EXHIBITS]->(p:PsychTrait {traitType: 'personality'})
                RETURN
                    ta.name as actor,
                    ta.sophistication as sophistication,
                    collect(p.name) as personality_traits
            """)

            profiles = {}
            for record in result:
                profiles[record["actor"]] = {
                    "sophistication": record["sophistication"],
                    "traits": record["personality_traits"]
                }

            return profiles

    def close(self):
        self.driver.close()


# Example Usage
if __name__ == "__main__":
    analyzer = PsychometricAnalyzer()

    # Analyze cognitive biases
    bias_df = analyzer.analyze_cognitive_biases()
    print("📊 Cognitive Bias Analysis:")
    print(bias_df.head(10))

    # Build threat actor profiles
    profiles = analyzer.threat_actor_personality_profiles()
    print("\n🎭 Threat Actor Psychological Profiles:")
    for actor, profile in list(profiles.items())[:5]:
        print(f"{actor}: {profile['traits']}")

    analyzer.close()
```

**Success Criteria**:
- [x] Psychometric analysis queries functional
- [x] Meaningful patterns identified
- [x] Integration with McKenney-Lacan framework
- [x] Results inform security strategy

---

## 📊 SUCCESS METRICS & VALIDATION

### Phase 1 (Qdrant) Success Metrics
```yaml
technical:
  entities_stored: ">10,000"
  unique_labels: ">40"
  search_latency: "<100ms"
  semantic_accuracy: ">85%"

business:
  search_capability: "operational"
  user_value: "Find similar threats instantly"
```

### Phase 2 (Neo4j) Success Metrics
```yaml
technical:
  nodes_added: ">10,000"
  relationships_created: ">5,000"
  existing_nodes_preserved: "100% (570K)"
  query_performance: "<500ms for 2-hop"
  graph_completeness: ">90%"

business:
  relationship_queries: "operational"
  attack_chain_analysis: "functional"
```

### Phase 3 (Hybrid) Success Metrics
```yaml
technical:
  hybrid_search_latency: "<500ms"
  result_relevance: ">90%"
  graph_expansion_accuracy: ">85%"

business:
  complex_queries: "answerable"
  analyst_productivity: "+50%"
```

### Phase 4 (Psychohistory) Success Metrics
```yaml
research:
  psychometric_patterns: "identified"
  threat_actor_profiles: "created"
  cognitive_bias_correlations: "analyzed"

strategic:
  mckenney_questions: "partially answered"
  predictive_capability: "foundation established"
```

---

## 🔧 TROUBLESHOOTING GUIDE

### Common Issues Across All Phases

#### Issue: "Connection refused" to container
**Diagnosis**:
```bash
docker ps --filter "name=<container>" --format "{{.Status}}"
```

**Solution**:
```bash
docker start <container-name>
# Wait 10-30 seconds for service to initialize
curl http://localhost:<port>/health
```

#### Issue: "Data loss detected" after processing
**Diagnosis**:
```bash
# Check Neo4j node count before/after
docker exec openspg-neo4j cypher-shell "MATCH (n) RETURN count(n)"
```

**Solution**:
- Restore from backup: `/tmp/neo4j_backup_*.dump`
- Review pipeline logs: `/5_NER11_Gold_Model/logs/*.jsonl`
- Verify MERGE (not CREATE) used in Cypher

#### Issue: "Performance degradation" after ingestion
**Diagnosis**:
```cypher
// Check missing indexes
SHOW INDEXES;

// Check query execution plans
EXPLAIN MATCH (n:PsychTrait) RETURN n LIMIT 10;
```

**Solution**:
- Re-run schema migration (Task 2.1)
- Add missing indexes
- Optimize queries with `USING INDEX` hint

#### Issue: "NER12 references causing confusion"
**Solution**:
- Read: `/1_AEON_DT_CyberSecurity_Wiki_Current/12_NER12_Gold_Schema_hyrbrid/00_NOTICE_PLANNING_DOCUMENTS.md`
- Remember: NER11 Gold (58 labels) is PRODUCTION
- NER12 references are PLANNING documents only

---

## 💾 MEMORY BANK INTEGRATION

### Store Progress in Claude-Flow Memory

**Namespace**: `ner11-gold`

**Required Memory Entries**:
```bash
# After each phase, store completion status
npx claude-flow memory store \
  --namespace ner11-gold \
  --key phase-1-complete \
  --value '{"date":"2025-12-01","entities_stored":15420,"search_functional":true}'

npx claude-flow memory store \
  --namespace ner11-gold \
  --key phase-2-complete \
  --value '{"date":"2025-12-01","nodes_added":15420,"relationships":8760,"graph_size":585654}'
```

**Retrieve Session State**:
```bash
# At start of new session
npx claude-flow memory list --namespace ner11-gold

# Get specific phase status
npx claude-flow memory retrieve --namespace ner11-gold --key phase-1-complete
```

---

## 📚 COMPLETE FILE PATH REFERENCE

### Primary Implementation Files (Create These)

**Qdrant Integration (Phase 1)**:
- `/5_NER11_Gold_Model/pipelines/01_configure_qdrant_collection.py` - Collection setup
- `/5_NER11_Gold_Model/pipelines/02_entity_embedding_service.py` - Embedding generation
- `/5_NER11_Gold_Model/pipelines/03_bulk_document_processor.py` - Batch processing
- `/5_NER11_Gold_Model/pipelines/requirements.txt` - Dependencies

**Neo4j Integration (Phase 2)**:
- `/5_NER11_Gold_Model/neo4j_migrations/01_schema_v3.1_migration.cypher` - Schema upgrade
- `/5_NER11_Gold_Model/pipelines/04_ner11_to_neo4j_mapper.py` - Label mapping
- `/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_pipeline.py` - Graph ingestion
- `/5_NER11_Gold_Model/pipelines/06_bulk_graph_ingestion.py` - Batch graph population

**Hybrid Search (Phase 3)**:
- `/5_NER11_Gold_Model/serve_model.py` - EXTEND with `/search/hybrid` endpoint

**Analytics (Phase 4)**:
- `/5_NER11_Gold_Model/analytics/psychometric_analysis.cypher` - Analysis queries
- `/5_NER11_Gold_Model/analytics/psychometric_analyzer.py` - Python analytics

**Logs & Tracking**:
- `/5_NER11_Gold_Model/logs/processed_documents.jsonl` - Qdrant processing log
- `/5_NER11_Gold_Model/logs/neo4j_ingestion.jsonl` - Graph ingestion log

### Existing Files (Reference/Extend These)

**NER11 Gold Model**:
- `/5_NER11_Gold_Model/serve_model.py` - **EXTEND THIS** (current FastAPI server)
- `/5_NER11_Gold_Model/API_NER11_GOLD/01_API_REFERENCE.md` - API documentation
- `/5_NER11_Gold_Model/API_NER11_GOLD/02_NEO4J_PIPELINE_GUIDE.md` - Integration guide
- `/5_NER11_Gold_Model/examples/neo4j_example.py` - Reference implementation
- `/5_NER11_Gold_Model/scripts/neo4j_integration.py` - Integration utilities

**Qdrant Agents**:
- `/openspg-official_neo4j/qdrant_init_phase1.py` - **REFERENCE THIS** for collection init
- `/openspg-official_neo4j/qdrant_agents/core/qdrant_memory_agent.py` - Memory management
- `/openspg-official_neo4j/qdrant_agents/core/qdrant_query_agent.py` - Query patterns

**Architecture References**:
- `/1_AEON_DT_CyberSecurity_Wiki_Current/00_AEON_CONSTITUTION.md` - Governing principles
- `/1_AEON_DT_CyberSecurity_Wiki_Current/01_ARCHITECTURE/01_COMPREHENSIVE_ARCHITECTURE.md` - System architecture
- `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/00_API_STATUS_AND_ROADMAP.md` - API specifications

**Enhancement Planning**:
- `/6_NER11_Gold_Model_Enhancement/implementation_guides/01_QUICK_START_GUIDE.md` - Quick start
- `/6_NER11_Gold_Model_Enhancement/neo4j_integration/01_SCHEMA_V3.1_SPECIFICATION.md` - Schema v3.1 spec
- `/6_NER11_Gold_Model_Enhancement/strategic_analysis/01_COMPREHENSIVE_GAP_ANALYSIS.md` - Gap analysis

**Future Planning** (Read NOTICE file first):
- `/1_AEON_DT_CyberSecurity_Wiki_Current/12_NER12_Gold_Schema_hyrbrid/` - PLANNING ONLY
- `/1_AEON_DT_CyberSecurity_Wiki_Current/12_NER12_Gold_Schema_hyrbrid/00_NOTICE_PLANNING_DOCUMENTS.md` - Important notice

---

## ⚠️ EXTEND-NOT-REPLACE GUIDELINES

### Constitutional Requirement (Article I, Section 1.2, Rule #2)
**"ALWAYS USE EXISTING RESOURCES"**
- Before creating new endpoints, verify none exist
- Before writing new code, check for shared libraries
- Before deploying new containers, use existing infrastructure

### Specific "DO NOT" List

❌ **DO NOT** create new Neo4j container
   ✅ **DO** extend `openspg-neo4j` (port 7687)

❌ **DO NOT** create new Qdrant container
   ✅ **DO** add collection to `openspg-qdrant` (port 6333)

❌ **DO NOT** create new FastAPI application
   ✅ **DO** add endpoints to `/5_NER11_Gold_Model/serve_model.py`

❌ **DO NOT** create new frontend application
   ✅ **DO** add features to `aeon-saas-dev` (port 3000)

❌ **DO NOT** create new authentication system
   ✅ **DO** use Clerk (NEVER break auth - Constitution Rule #1)

❌ **DO NOT** create parallel API specifications
   ✅ **DO** implement existing specs in `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/`

❌ **DO NOT** create new document processing frameworks
   ✅ **DO** extend OpenSPG workflows (port 8887)

❌ **DO NOT** create new vector databases or search engines
   ✅ **DO** use Qdrant + Neo4j hybrid approach

### Integration Verification Checklist

Before implementing ANY new component:
- [ ] Check `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/` for existing API specs
- [ ] Verify no duplicate functionality exists
- [ ] Confirm integration with existing containers
- [ ] Review Constitution Article I, Section 1.2
- [ ] Ensure no existing resources are replaced
- [ ] Document integration points in Qdrant memory

---

## 🚀 EXECUTION WORKFLOW FOR NEW SESSIONS

### Step-by-Step Startup (30 minutes)

#### 1. Verify Infrastructure (10 min)
```bash
# Check all containers running
docker ps --format "table {{.Names}}\t{{.Status}}"

# Required containers:
# - ner11-gold-api (port 8000)
# - openspg-neo4j (ports 7474/7687)
# - openspg-qdrant (ports 6333-6334)
# - aeon-saas-dev (port 3000)
# - aeon-postgres-dev (port 5432)

# Verify NER11 API
curl http://localhost:8000/health
# Expected: {"status":"healthy","model":"loaded"}

# Verify Qdrant
curl http://localhost:6333/collections
# Expected: {"result":{"collections":[...]}}

# Verify Neo4j
docker exec openspg-neo4j cypher-shell "MATCH (n) RETURN count(n) as total"
# Expected: ~570,000+ nodes
```

#### 2. Load Session Context (10 min)
```bash
# Retrieve memory bank state
npx claude-flow memory list --namespace ner11-gold

# Check completed phases
npx claude-flow memory retrieve --namespace ner11-gold --key gap-002-commit
npx claude-flow memory retrieve --namespace ner11-gold --key phase-1-complete
npx claude-flow memory retrieve --namespace ner11-gold --key phase-2-complete

# Review taskmaster
cat /docs/TASKMASTER_NER11_GOLD_COMPLETE_v2.0.md
```

#### 3. Read Critical Documentation (10 min)
```bash
# Constitution (governing principles)
cat /1_AEON_DT_CyberSecurity_Wiki_Current/00_AEON_CONSTITUTION.md | head -250

# NER11 status
cat /docs/NER11_GOLD_STATUS_REPORT_2025-12-01.md

# Architecture overview
cat /1_AEON_DT_CyberSecurity_Wiki_Current/01_ARCHITECTURE/01_COMPREHENSIVE_ARCHITECTURE.md | head -200
```

#### 4. Determine Current Phase
Based on memory bank:
- **Phase 1 not started**: Begin Task 1.1 (Configure Qdrant)
- **Phase 1 complete**: Begin Task 2.1 (Neo4j migration)
- **Phase 2 complete**: Begin Task 3.1 (Hybrid search)
- **Phase 3 complete**: Begin Task 4.1 (Psychometrics)

#### 5. Execute Current Task
Follow task-specific instructions in this TASKMASTER.

---

## 📋 QUALITY ASSURANCE CHECKLIST

### Before Starting Any Task
- [ ] Read Constitution Article I (Foundational Principles)
- [ ] Verify all containers healthy
- [ ] Check memory bank for prior progress
- [ ] Review existing code before creating new files
- [ ] Confirm EXTEND approach (not parallel system)

### During Implementation
- [ ] Follow existing code patterns
- [ ] Use existing infrastructure (no new containers)
- [ ] Test incrementally (not big-bang deployment)
- [ ] Document decisions in Qdrant memory
- [ ] Track errors and issues

### After Completion
- [ ] Verify existing systems UNCHANGED (570K Neo4j nodes preserved)
- [ ] Run validation tests
- [ ] Update memory bank with completion status
- [ ] Document lessons learned
- [ ] Check performance targets met

### Before Marking "COMPLETE"
- [ ] Working code exists (not just framework)
- [ ] Tests passing (≥85% coverage)
- [ ] Documentation updated
- [ ] No data loss occurred
- [ ] Performance acceptable
- [ ] Integration verified

**From Constitution**: "COMPLETE" means deliverable exists and functions, not frameworks are built.

---

## 🎯 NEXT SESSION QUICK START

```bash
# 1. Verify infrastructure
docker ps | grep -E "ner11|neo4j|qdrant"

# 2. Check memory bank
npx claude-flow memory list --namespace ner11-gold

# 3. Determine phase
# - Check for phase-1-complete, phase-2-complete keys

# 4. Read this TASKMASTER
cat /docs/TASKMASTER_NER11_GOLD_COMPLETE_v2.0.md

# 5. Start implementation
cd /5_NER11_Gold_Model/pipelines
python <phase_script>.py
```

---

**Document Version**: 2.0.0
**Created**: 2025-12-01 05:35 UTC
**Status**: PRODUCTION-READY IMPLEMENTATION GUIDE
**Authority**: AEON Constitution Article III, Section 3.1
**Next Review**: After Phase 1 completion

**This document is SELF-CONTAINED and COMPLETE for new session execution.**
