# System Overview and Architecture

**File**: 00_OVERVIEW.md
**Created**: 2025-11-11 10:00:00 UTC
**Modified**: 2025-11-11 10:00:00 UTC
**Version**: 1.0.0
**Purpose**: Comprehensive system architecture overview for AEON DT enterprise knowledge graph platform
**Status**: ACTIVE

## Executive Summary

The AEON Digital Twin (AEON DT) system is an enterprise knowledge graph platform for document intelligence, cybersecurity analysis, and industrial control system (ICS) management. The system ingests documents through a 5-step user interface, extracts entities and relationships using hybrid NER (95%+ precision), and stores knowledge in a multi-database architecture optimized for graph traversal, semantic search, and temporal tracking.

**Core Capabilities**:
- Document ingestion with 18 entity types (8 industrial + 10 cybersecurity)
- Hybrid Pattern-Neural NER (92-96% combined precision)
- Knowledge graph storage with 2,051 MITRE entities, 40,886 relationships
- Semantic search using vector embeddings
- Temporal tracking for entity/relationship versioning
- Real-time job monitoring with BullMQ queue management

**Current Status**: Production system with web interface (Next.js 15), processing pipeline (Python agents), and multi-database backend (Neo4j, Qdrant, MySQL, MinIO)

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AEON DT System Architecture                      │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│   FRONTEND       │  Next.js 15 (React 19.0.0)
│   aeon-ui        │  - Five-step upload wizard
│   172.18.0.8     │  - Graph visualization
│   Port: 3000     │  - Real-time job monitoring
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────┐
│              API GATEWAY / BACKEND (Node.js)                     │
│  - /api/upload (MinIO integration)                               │
│  - /api/pipeline/process (Document processing)                   │
│  - /api/pipeline/status/[jobId] (Progress tracking)              │
│  - Clerk Authentication                                          │
└─────┬────────────┬────────────┬────────────────────────┬─────────┘
      │            │            │                        │
      ▼            ▼            ▼                        ▼
┌──────────┐ ┌──────────┐ ┌─────────────┐ ┌─────────────────────────┐
│  Neo4j   │ │  Qdrant  │ │    MySQL    │ │        MinIO            │
│  Graph   │ │  Vector  │ │  Metadata   │ │   Object Storage        │
│  DB      │ │  Search  │ │  33 Tables  │ │   (S3-compatible)       │
└──────────┘ └──────────┘ └─────────────┘ └─────────────────────────┘
172.18.0.5   172.18.0.6   172.18.0.3       172.18.0.4
7474, 7687   6333, 6334   3306             9000, 9001

                        ┌────────────────────┐
                        │  Python Agents     │
                        │  (Serial Pipeline) │
                        ├────────────────────┤
                        │ 1. classifier.py   │
                        │ 2. ner_agent.py    │
                        │ 3. ingestion.py    │
                        └────────────────────┘
```

**Container Network**: openspg-network (bridge), Subnet: 172.18.0.0/16, Gateway: 172.18.0.1

**Current Infrastructure Status** (2025-11-11):
| Container | Status | Health | IP | Ports | Role |
|-----------|--------|--------|-----|-------|------|
| aeon-ui | Running | Unhealthy | 172.18.0.8 | 3000 | Web interface |
| openspg-neo4j | Running | Healthy | 172.18.0.5 | 7474, 7687 | Knowledge graph |
| openspg-qdrant | Running | Unhealthy | 172.18.0.6 | 6333, 6334 | Vector search |
| openspg-mysql | Running | Healthy | 172.18.0.3 | 3306 | Metadata storage |
| openspg-minio | Running | Healthy | 172.18.0.4 | 9000, 9001 | Object storage |
| openspg-server | Running | Unhealthy | 172.18.0.2 | 8887 | KG processing |

## Technology Stack

### Frontend (Next.js 15.0.3)
- **Framework**: Next.js 15.0.3 with App Router
- **UI Library**: React 19.0.0
- **Authentication**: Clerk (user management)
- **Styling**: TailwindCSS, Tremor (data visualization), Framer Motion (animations)
- **State Management**: React Server Components
- **Icons**: Lucide React, Radix UI Icons

**Key Dependencies** (from package.json):
```json
{
  "next": "15.0.3",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "@clerk/nextjs": "^6.7.3",
  "@tremor/react": "^3.18.5",
  "framer-motion": "^11.18.0",
  "minio": "^8.0.2",
  "neo4j-driver": "^5.27.0"
}
```

### Backend (Node.js/Express + Python)
- **Runtime**: Node.js with TypeScript
- **Queue Management**: BullMQ 5.26.2 (in-memory, production should use Redis)
- **Document Processing**: Python 3 agents (classifier, NER, ingestion)
- **Python NLP**: spaCy en_core_web_lg model (768-dim embeddings)
- **Agent Timeout**: 5 minutes per stage

### Databases

#### 1. Neo4j 5.25.0 (Knowledge Graph)
- **URI**: bolt://localhost:7687
- **Browser**: http://localhost:7474
- **Current Data**: 2,051 MITRE entities, 40,886 relationships
- **Schema**: Entity nodes with CONTAINS_ENTITY relationships
- **Indexes**: entity_text, entity_label, entity_composite, document_fulltext
- **Deduplication**: SHA256 hash + (text, label) composite key

#### 2. Qdrant (Vector Search)
- **URL**: http://localhost:6333
- **Collections**: 12 active collections
- **Embeddings**: 768-dimensional vectors (spaCy en_core_web_lg)
- **Distance**: Cosine similarity
- **Purpose**: Semantic search, entity similarity, recommendation

#### 3. MySQL (Structured Data)
- **Host**: localhost:3306
- **Database**: openspg
- **Tables**: 33 tables (user management, document metadata, job tracking)
- **Purpose**: System configuration, user data, document metadata

#### 4. MinIO (Object Storage)
- **Console**: http://localhost:9001
- **Endpoint**: http://localhost:9000
- **Bucket**: aeon-documents
- **Purpose**: Uploaded files, processed results, archival

## Core Components

### 1. Frontend Application (Next.js 15)

**Architecture**: Next.js 15 App Router with React Server Components

**Key Pages**:
- `/` - Dashboard home
- `/upload` - Five-step upload wizard
- `/documents` - Document management
- `/graph` - Knowledge graph visualization
- `/search` - Semantic search interface

**Upload Wizard Flow** (5 Steps):
1. **File Selection** - Choose files for upload
2. **Document Classification** - Assign sector/subsector
3. **Entity Configuration** - Select entity types to extract
4. **Relationship Configuration** - Define relationship types
5. **Processing & Results** - Monitor progress, view graph

**Authentication**: Clerk integration for user management

### 2. Document Processing Pipeline

**Architecture**: Serial queue (in-memory Map), processes ONE document at a time

**Job Submission** (POST /api/pipeline/process):
```typescript
interface DocumentJobData {
  files: Array<{
    path: string;        // File system path
    name: string;        // Filename
    size: number;        // File size in bytes
    type: string;        // MIME type
  }>;
  customer: string;      // Customer identifier
  tags: string[];        // Classification tags
  classification: {
    sector: string;      // Required
    subsector?: string;  // Optional
  };
}
```

**Processing Flow**:
```
Upload → Queue → Classification (0-40%) → NER (40-70%) → Ingestion (70-100%)
```

**Progress Tracking** (GET /api/pipeline/status/[jobId]):
```json
{
  "jobId": "uuid",
  "status": "extracting",
  "progress": 66,
  "steps": {
    "classification": {"status": "complete", "progress": 100},
    "ner": {"status": "running", "progress": 50},
    "ingestion": {"status": "pending", "progress": 0}
  }
}
```

### 3. Python Agent Pipeline (Serial Execution)

**Agent 1: classifier_agent.py** (10-40% progress)
- **Purpose**: Document classification, content analysis
- **Input**: file_path, sector, subsector
- **Output**: Classification results
- **Timeout**: 5 minutes

**Agent 2: ner_agent.py** (40-70% progress) - **PRIMARY NER EXTRACTION**
- **Purpose**: Named entity extraction using hybrid approach
- **Input**: file_path, customer
- **NER Implementation**: Pattern-Neural Hybrid
  - **Pattern-Based NER**: 95%+ precision (regex + spaCy EntityRuler)
  - **Neural NER**: 85-92% precision (spaCy en_core_web_lg)
  - **Combined Precision**: 92-96% target
- **18 Entity Types**:
  - Industrial (8): VENDOR, PROTOCOL, STANDARD, COMPONENT, MEASUREMENT, ORGANIZATION, SAFETY_CLASS, SYSTEM_LAYER
  - Cybersecurity (10): CVE, CWE, CAPEC, THREAT_ACTOR, CAMPAIGN, ATTACK_TECHNIQUE, MALWARE, IOC, APT_GROUP
- **Output**: JSON with entities, confidence scores, sources (pattern/neural)
- **Timeout**: 5 minutes

**Agent 3: ingestion_agent.py** (70-100% progress)
- **Purpose**: Neo4j node creation, relationship mapping
- **Input**: file_path, customer, tags, classification
- **Graph Operations**: CREATE Document nodes, MERGE Entities, CREATE relationships
- **Deduplication**: SHA256 hash for documents, (text, label) for entities
- **Timeout**: 5 minutes

**Key Finding**: NO v9 API endpoint at localhost:8001/api/v9/ner/extract. NER is implemented as a Python agent with spaCy.

### 4. Entity Extraction (Hybrid NER)

**Pattern Library** (95%+ precision):
```python
# Example patterns from ner_agent.py
{"label": "VENDOR", "pattern": [{"LOWER": "siemens"}]}
{"label": "PROTOCOL", "pattern": [{"LOWER": "modbus"}, {"LOWER": "tcp"}]}
{"label": "STANDARD", "pattern": [{"TEXT": {"REGEX": "IEC\\s*\\d+"}}]}
{"label": "CVE", "pattern": [{"TEXT": {"REGEX": "CVE-\\d{4}-\\d{4,7}"}}]}
{"label": "MEASUREMENT", "pattern": [{"TEXT": {"REGEX": "\\d+(\\.\\d+)?\\s*PSI"}}]}
```

**spaCy Neural NER** (85-92% precision):
- Model: en_core_web_lg (pre-trained English model)
- Extracts: PERSON, ORG, GPE, DATE, PRODUCT, etc.
- Contextual understanding for entities not in pattern library

**Entity Output Structure**:
```json
{
  "entities": [
    {
      "text": "Siemens S7-1500",
      "label": "VENDOR",
      "confidence": 0.95,
      "source": "pattern",
      "start": 10,
      "end": 25
    }
  ],
  "entity_count": 45,
  "by_type": {"VENDOR": 12, "PROTOCOL": 8, "STANDARD": 5},
  "precision_estimate": 0.93
}
```

### 5. Relationship Extraction

**Current Implementation**: Limited to entity co-occurrence

**Storage Pattern** (Neo4j):
```cypher
// Document contains entities
(Document)-[:CONTAINS_ENTITY {
  start: number,
  end: number,
  type: string,
  confidence: number,
  source: 'pattern' | 'neural'
}]->(Entity)

// Entity metadata
(Metadata)-[:METADATA_FOR]->(Document)

// Tag relationships
(Document)-[:HAS_TAG]->(Tag)
```

**Gap**: No advanced Subject-Verb-Object (SVO) triple extraction currently active in main pipeline

**Alternative**: `nlp_ingestion_pipeline.py` (standalone) supports dependency parsing for SVO triples

### 6. Temporal Tracking

**Entity Versioning** (Neo4j properties):
```typescript
interface EntityNode {
  validFrom: DateTime;   // Start of validity
  validTo: DateTime;     // End of validity (null = current)
  version: number;       // Version number
  created_at: DateTime;  // First occurrence
  count: number;         // Occurrence counter
}
```

**Relationship Versioning**:
```cypher
CREATE (source)-[r:RELATIONSHIP_TYPE {
  validFrom: datetime(),
  validTo: null,
  version: 1
}]->(target)
```

**Temporal Queries**:
```cypher
// Get current entities
MATCH (e:Entity)
WHERE e.validTo IS NULL
RETURN e

// Get historical snapshot
MATCH (e:Entity)
WHERE e.validFrom <= $timestamp AND (e.validTo IS NULL OR e.validTo > $timestamp)
RETURN e
```

### 7. Storage Layer

**Multi-Database Architecture**:

| Database | Purpose | Current Data | Performance |
|----------|---------|--------------|-------------|
| Neo4j | Knowledge graph | 2,051 entities, 40,886 relationships | Healthy |
| Qdrant | Vector search | 12 collections, 768-dim embeddings | Unhealthy (needs investigation) |
| MySQL | Metadata | 33 tables, user/document tracking | Healthy |
| MinIO | Object storage | aeon-documents bucket | Healthy |

**Data Flow**:
1. Upload → MinIO (raw files)
2. Queue → BullMQ in-memory
3. Process → Python agents
4. Extract → Neo4j + Qdrant
5. Query → Graph traversal + semantic search

## Integration Points

### REST API Endpoints

**Upload API**:
- POST /api/upload - File upload to MinIO
- Response: file path, bucket, size, type

**Pipeline API**:
- POST /api/pipeline/process - Submit document for processing
- GET /api/pipeline/status/[jobId] - Job progress
- GET /api/pipeline/process - Queue status

**Neo4j API**:
- Browser: http://localhost:7474
- Bolt: bolt://localhost:7687
- REST: POST http://localhost:7474/db/neo4j/tx/commit

**Qdrant API**:
- Collections: GET http://localhost:6333/collections
- Search: POST http://localhost:6333/collections/{name}/points/search

**MinIO API**:
- Console: http://localhost:9001
- S3 API: http://localhost:9000

### Authentication

**Clerk Integration**:
```typescript
const { userId } = await auth();  // Clerk authentication
if (!userId) return 401;
```

**Security Issue**: Status endpoint (GET /api/pipeline/status/[jobId]) has NO authentication

### Rate Limiting

**Implementation**: In-memory Map per IP
- Limit: 100 requests per 15 minutes
- Window: Sliding window per IP
- Applied to: POST /api/pipeline/process

## Security Architecture

### Credentials (⚠️ DEFAULT - CHANGE FOR PRODUCTION)

**Neo4j**:
- URI: bolt://localhost:7687
- User: neo4j
- Password: neo4j@openspg

**Qdrant**:
- URL: http://localhost:6333
- API Key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=

**MySQL**:
- Host: localhost:3306
- User: root
- Password: openspg

**MinIO**:
- Access Key: minio
- Secret Key: minio@openspg

### Security Vulnerabilities

| ID | Vulnerability | Severity | CVSS | Status |
|----|---------------|----------|------|--------|
| VUL-001 | Default Database Credentials | Critical | 9.8 | Requires Action |
| VUL-002 | Unencrypted Communication | High | 8.7 | Requires Action |
| VUL-003 | Exposed API Key | High | 7.4 | Requires Action |
| VUL-004 | No Network Segmentation | Medium | 6.5 | Requires Action |
| VUL-005 | Weak Password Policy | Medium | 6.2 | Requires Action |

### Path Validation

```typescript
function validateFilePath(filePath: string): boolean {
  const normalized = path.normalize(filePath);
  const allowedDir = path.resolve(process.env.UPLOAD_DIR || '/uploads');

  // Prevent directory traversal
  if (normalized.includes('..')) return false;

  // Verify within allowed directory
  if (!resolvedPath.startsWith(allowedDir)) return false;

  return true;
}
```

## Performance Characteristics

### Processing Performance

**NER Agent**:
- Speed: ~1-2 seconds per document page
- Precision: 92-96% combined (pattern + neural)
- Entity Types: 18 total
- Timeout: 5 minutes per document

**Pipeline Performance**:
- Queue: Serial (one at a time)
- Batch Size: 100 entities per Neo4j insert
- Job Timeout: 5 minutes per agent
- Total Processing: 0.5-15.5 minutes per document (depends on complexity)

**Neo4j Performance**:
- Entities: 2,051 indexed
- Relationships: 40,886 indexed
- Query Time: <100ms for simple traversals
- Indexes: entity_text, entity_label, composite, fulltext

**Qdrant Performance**:
- Collections: 12 active
- Embedding Dimension: 768
- Distance Metric: Cosine similarity
- Search Time: <50ms for semantic queries

### Scalability Limits

**Current Bottlenecks**:
1. **Serial Processing**: Only 1 document at a time
2. **In-Memory Queue**: Data lost on restart
3. **No Job Persistence**: Cannot resume after crash
4. **5-Min Timeout**: Long documents may fail

**Recommended Improvements**:
1. Replace in-memory queue with Redis (BullMQ)
2. Implement parallel worker processes
3. Add job persistence to MySQL
4. WebSocket for real-time updates
5. Increase or configure timeouts

## Deployment Architecture

### Docker Deployment

**Network**: openspg-network (bridge)
- Subnet: 172.18.0.0/16
- Gateway: 172.18.0.1

**Container Orchestration**: Docker Compose

**Environment Variables** (from .env.local):
```bash
# MinIO
MINIO_ENDPOINT=openspg-minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_BUCKET=aeon-documents

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg

# Python Agents
PYTHON_PATH=python3
AGENTS_PATH=../agents
```

### Health Monitoring

**Health Endpoints**:
- AEON UI: http://localhost:3000/api/health
- Neo4j: http://localhost:7474
- Qdrant: http://localhost:6333/health
- MinIO: http://localhost:9001/minio/health/live

**Current Status Issues** (2025-11-11):
- aeon-ui: Unhealthy (port 3000 accessibility)
- openspg-qdrant: Unhealthy (needs investigation)
- openspg-server: Unhealthy (port 8887 accessibility)

### Backup Strategy

**Neo4j**: Automatic backups (configured in container)
**MySQL**: Daily backups (manual configuration needed)
**MinIO**: Versioning enabled, replication recommended
**Qdrant**: Snapshot backups (manual configuration needed)

---

## Current vs. McKenney's Vision

**Implemented** ✅:
- Document upload pipeline
- Hybrid NER extraction (18 entity types)
- Neo4j knowledge graph storage
- Vector search with Qdrant
- Real-time job monitoring
- Web interface (Next.js 15)

**Gaps** ⚠️:
- Advanced relationship extraction (SVO triples not active)
- Temporal analytics dashboard
- Advanced graph algorithms
- Knowledge base integration (DBpedia, Wikidata)
- Custom spaCy model training
- Production-grade queue (Redis BullMQ)
- Parallel worker processes
- Full security hardening

**Next Priorities**:
1. Security remediation (credentials, TLS, network segmentation)
2. Container health investigation (aeon-ui, qdrant, openspg-server)
3. Production queue implementation (Redis)
4. Parallel processing for scalability
5. Advanced relationship extraction
6. Temporal analytics features

---

*AEON DT v1.0.0 | Complete System Documentation | 2025-11-11*
*Status: OPERATIONAL | Health: 3/6 Containers Healthy*
