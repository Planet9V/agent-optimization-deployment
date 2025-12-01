# Database Architecture - Multi-Database System

**File**: 07_DATABASE_ARCHITECTURE.md
**Created**: 2025-11-11 11:00:00 UTC
**Modified**: 2025-11-11 11:00:00 UTC
**Version**: 1.0.0
**Purpose**: Neo4j, Qdrant, MySQL, and MinIO architecture documentation for AEON DT
**Status**: ACTIVE

## Executive Summary

The AEON DT system uses a multi-database architecture optimized for different data access patterns. Neo4j 5.25.0 stores the knowledge graph (2,051 MITRE entities, 40,886 relationships), Qdrant provides vector search with 768-dimensional embeddings for semantic queries, MySQL manages structured metadata across 33 tables, and MinIO handles S3-compatible object storage for uploaded documents. This polyglot persistence pattern enables graph traversal, semantic search, relational queries, and file storage within a single platform.

**Database Summary**:
- **Neo4j**: Knowledge graph with entity deduplication (text, label) and temporal tracking
- **Qdrant**: Vector database with 12 collections, cosine similarity search
- **MySQL**: 33 tables for user management, document metadata, job tracking
- **MinIO**: S3-compatible object storage (aeon-documents bucket)

**Current Data**: 115 ingested documents, 12,256 entities in Neo4j, 14,645 relationships in Neo4j, 12 Qdrant collections

## Database Architecture Overview

### System Architecture
```
┌─────────────┐
│   Frontend  │
└──────┬──────┘
       │
┌──────▼──────────────────────────────────────┐
│           API Gateway / Backend             │
└──┬────┬────┬────┬────────────────────────┬──┘
   │    │    │    │                        │
   ▼    ▼    ▼    ▼                        ▼
┌─────┬──────┬────────┬─────────────┬────────┐
│Neo4j│Qdrant│ MySQL  │   MinIO     │ Redis  │
└─────┴──────┴────────┴─────────────┴────────┘
```

## 1. Neo4j - Knowledge Graph Database

### Connection Details
- **URI**: bolt://localhost:7687
- **Browser**: http://localhost:7474
- **User**: neo4j (⚠️ default credentials)
- **Password**: neo4j@openspg (⚠️ change for production)
- **Database**: neo4j
- **Version**: 5.25.0

### Current Data (2025-11-11)
- **MITRE Entities**: 2,051 nodes
- **Relationships**: 40,886 edges
- **Ingested Documents**: 115 total
- **Total Entities**: 12,256 (including non-MITRE)
- **Unique Entity Types**: 18 (8 industrial + 10 cybersecurity)

### Purpose
- Store entities and relationships in a knowledge graph
- Graph-based querying with Cypher language
- Relationship traversal (1-hop to N-hop paths)
- Pattern matching for complex queries
- Entity deduplication using (text, label) composite key
- Temporal tracking with validFrom/validTo timestamps

### Schema Design

#### Document and Metadata Nodes

**Document Node**:
```cypher
CREATE (d:Document {
  id: randomUUID(),
  content: $content,
  char_count: $char_count,
  line_count: $line_count,
  created_at: datetime()
})
```

**Metadata Node** (SHA256 deduplication):
```cypher
MERGE (m:Metadata {sha256: $sha256})
ON CREATE SET
  m.file_path = $file_path,
  m.file_name = $file_name,
  m.file_ext = $file_ext,
  m.file_size = $file_size,
  m.processed_at = $processed_at
CREATE (m)-[:METADATA_FOR]->(d)
```

#### Entity Nodes

**Entity Node Structure** (from ner_agent.py ingestion):
```cypher
MERGE (e:Entity {text: $text, label: $label})
ON CREATE SET
  e.created_at = datetime(),
  e.count = 1
ON MATCH SET
  e.count = coalesce(e.count, 0) + 1
```

**Entity Properties**:
```typescript
interface EntityNode {
  text: string;           // Entity text (e.g., "Siemens S7-1500")
  label: string;          // Entity type (VENDOR, PROTOCOL, CVE, etc.)
  count: number;          // Occurrence counter across all documents
  created_at: DateTime;   // First occurrence timestamp
  validFrom?: DateTime;   // Temporal tracking (optional)
  validTo?: DateTime;     // Temporal tracking (null = current)
  version?: number;       // Version control (optional)
}
```

**18 Entity Labels**:
- **Industrial** (8): VENDOR, PROTOCOL, STANDARD, COMPONENT, MEASUREMENT, ORGANIZATION, SAFETY_CLASS, SYSTEM_LAYER
- **Cybersecurity** (10): CVE, CWE, CAPEC, THREAT_ACTOR, CAMPAIGN, ATTACK_TECHNIQUE, MALWARE, IOC, APT_GROUP

#### Relationship Types

**CONTAINS_ENTITY** (Document → Entity):
```cypher
CREATE (d)-[r:CONTAINS_ENTITY {
  start: $start_position,
  end: $end_position,
  type: $entity_type,
  confidence: $confidence_score,
  source: $extraction_source  // 'pattern' or 'neural'
}]->(e)
```

**METADATA_FOR** (Metadata → Document):
```cypher
CREATE (m:Metadata)-[:METADATA_FOR]->(d:Document)
```

**HAS_TAG** (Document → Tag):
```cypher
CREATE (d:Document)-[:HAS_TAG]->(t:Tag {id: $tag_id, name: $tag_name})
```

**Example Temporal Relationships** (future feature):
```cypher
CREATE (source:Entity)-[r:WORKS_FOR {
  validFrom: datetime('2024-01-01T00:00:00Z'),
  validTo: null,  // Current relationship
  confidence: 0.85,
  source: 'document-123'
}]->(target:Entity)
```

#### Relationship Edges
```cypher
CREATE (source:Entity)-[r:RELATIONSHIP_TYPE {
  type: string,
  confidence: number,
  validFrom: datetime(),
  validTo: null,
  sources: [],
  attributes: {}
}]->(target:Entity)
```

### Query Patterns

#### Entity Retrieval
```cypher
MATCH (e:Entity {type: $entityType})
WHERE e.validTo IS NULL
RETURN e
LIMIT $limit
```

#### Relationship Traversal
```cypher
MATCH path = (source:Entity)-[r*1..3]-(target:Entity)
WHERE source.id = $sourceId
RETURN path
```

#### Pattern Matching
```cypher
MATCH (person:Entity {type: 'PERSON'})
      -[:WORKS_FOR]->(org:Entity {type: 'ORGANIZATION'})
      -[:LOCATED_IN]->(loc:Entity {type: 'LOCATION'})
RETURN person, org, loc
```

### Performance Optimization
- Index strategy
- Query caching
- Batch operations
- Connection pooling

## 2. Qdrant - Vector Database

### Purpose
- Store entity embeddings
- Semantic search
- Similarity queries
- Recommendation engine

### Collection Schema

#### Entity Embeddings Collection
```typescript
{
  collection_name: "entity_embeddings",
  vectors: {
    size: 768,  // Embedding dimension
    distance: "Cosine"
  },
  payload_schema: {
    entityId: "keyword",
    entityType: "keyword",
    entityName: "text",
    documentId: "keyword",
    timestamp: "datetime"
  }
}
```

#### Document Embeddings Collection
```typescript
{
  collection_name: "document_embeddings",
  vectors: {
    size: 768,
    distance: "Cosine"
  },
  payload_schema: {
    documentId: "keyword",
    chunkId: "keyword",
    text: "text",
    metadata: "object"
  }
}
```

### Vector Operations

#### Insert Embeddings
```typescript
await qdrantClient.upsert("entity_embeddings", {
  points: [{
    id: entityId,
    vector: embedding,
    payload: {
      entityId,
      entityType,
      entityName,
      documentId
    }
  }]
});
```

#### Semantic Search
```typescript
const results = await qdrantClient.search("entity_embeddings", {
  vector: queryEmbedding,
  limit: 10,
  filter: {
    must: [
      { key: "entityType", match: { value: "PERSON" } }
    ]
  }
});
```

### Performance Optimization
- HNSW index configuration
- Quantization settings
- Batch insertion
- Shard distribution

## 3. MySQL - Structured Data Storage

### Purpose
- User management
- Document metadata
- Job tracking
- System configuration

### Schema Design

#### Users Table
```sql
CREATE TABLE users (
  id VARCHAR(36) PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin', 'user', 'viewer') DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_email (email)
);
```

#### Documents Table
```sql
CREATE TABLE documents (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  filename VARCHAR(255) NOT NULL,
  file_type VARCHAR(50) NOT NULL,
  file_size BIGINT NOT NULL,
  minio_path VARCHAR(500) NOT NULL,
  status ENUM('uploaded', 'processing', 'completed', 'failed') DEFAULT 'uploaded',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  processed_at TIMESTAMP NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
);
```

#### Jobs Table
```sql
CREATE TABLE jobs (
  id VARCHAR(36) PRIMARY KEY,
  document_id VARCHAR(36) NOT NULL,
  job_type ENUM('parse', 'ner', 'relationship', 'graph', 'embedding', 'temporal'),
  status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
  priority INT DEFAULT 0,
  attempts INT DEFAULT 0,
  max_attempts INT DEFAULT 3,
  error_message TEXT NULL,
  started_at TIMESTAMP NULL,
  completed_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (document_id) REFERENCES documents(id),
  INDEX idx_document_id (document_id),
  INDEX idx_status (status),
  INDEX idx_job_type (job_type)
);
```

### Query Optimization
- Index strategy
- Query caching
- Connection pooling
- Partitioning strategy

## 4. MinIO - Object Storage

### Purpose
- Store uploaded documents
- Store processed files
- Backup and archival
- Binary data storage

### Bucket Structure

#### Documents Bucket
```
documents/
├── raw/
│   ├── {userId}/
│   │   ├── {documentId}.pdf
│   │   └── {documentId}.docx
├── processed/
│   ├── {documentId}/
│   │   ├── text.txt
│   │   ├── metadata.json
│   │   └── entities.json
└── archives/
    └── {year}/{month}/
```

### Operations

#### Upload Document
```typescript
await minioClient.putObject(
  'documents',
  `raw/${userId}/${documentId}.pdf`,
  fileBuffer,
  fileSize,
  { 'Content-Type': 'application/pdf' }
);
```

#### Retrieve Document
```typescript
const stream = await minioClient.getObject(
  'documents',
  `raw/${userId}/${documentId}.pdf`
);
```

### Lifecycle Policies
- Automatic archival
- Retention policies
- Versioning
- Backup strategy

## 5. Redis - Caching and Queue Management

### Purpose
- BullMQ job queues
- Session storage
- API response caching
- Rate limiting

### Key Patterns

#### Job Queue Keys
```
bull:{queueName}:id
bull:{queueName}:wait
bull:{queueName}:active
bull:{queueName}:completed
bull:{queueName}:failed
```

#### Cache Keys
```
cache:entity:{entityId}
cache:document:{documentId}
cache:search:{query_hash}
```

## Database Integration Strategy

### Data Flow
1. **Document Upload** → MinIO storage + MySQL metadata
2. **ETL Processing** → Redis job queues → BullMQ workers
3. **Entity Extraction** → Neo4j nodes + Qdrant embeddings
4. **Relationship Extraction** → Neo4j edges
5. **Query Processing** → Neo4j graph queries + Qdrant semantic search

### Transaction Management
- Distributed transaction patterns
- Eventual consistency
- Rollback strategies
- Data synchronization

### Backup and Recovery
- Neo4j: Automatic backups
- MySQL: Daily backups
- MinIO: Versioning and replication
- Qdrant: Snapshot backups
- Redis: Persistence configuration

## Monitoring and Performance

### Metrics Tracking
- Query performance
- Storage utilization
- Connection pool status
- Cache hit rates

### Performance Optimization
- Query optimization
- Index management
- Connection pooling
- Caching strategies

---

*Database Architecture Documentation | Multi-Database System*

### Indexes and Constraints

**Implemented Indexes**:
```cypher
-- Entity indexes (actual implementation)
CREATE INDEX entity_text IF NOT EXISTS
  FOR (e:Entity) ON (e.text);

CREATE INDEX entity_label IF NOT EXISTS
  FOR (e:Entity) ON (e.label);

CREATE INDEX entity_composite IF NOT EXISTS
  FOR (e:Entity) ON (e.text, e.label);

-- Metadata constraint (SHA256 deduplication)
CREATE CONSTRAINT metadata_sha256 IF NOT EXISTS
  FOR (m:Metadata) REQUIRE m.sha256 IS UNIQUE;

-- Document constraint
CREATE CONSTRAINT document_id IF NOT EXISTS
  FOR (d:Document) REQUIRE d.id IS UNIQUE;

-- Full-text search index
CREATE FULLTEXT INDEX document_fulltext IF NOT EXISTS
  FOR (d:Document) ON EACH [d.content];
```

### Query Patterns

#### Entity Retrieval (Find all VENDOR entities)
```cypher
MATCH (e:Entity {label: 'VENDOR'})
RETURN e.text, e.count, e.created_at
ORDER BY e.count DESC
LIMIT 50
```

#### Document-Entity Relationships
```cypher
// Find all entities in a document
MATCH (m:Metadata {file_name: 'technical_spec.pdf'})-[:METADATA_FOR]->(d:Document)
MATCH (d)-[r:CONTAINS_ENTITY]->(e:Entity)
RETURN e.text, e.label, r.confidence, r.source
ORDER BY r.confidence DESC
```

#### Relationship Traversal (1-3 hops)
```cypher
// Find entities connected to a specific entity within 3 hops
MATCH path = (source:Entity {text: 'Siemens'})-[*1..3]-(target:Entity)
RETURN path
LIMIT 100
```

#### Pattern Matching (Find all documents with CVEs and vendors)
```cypher
MATCH (d:Document)-[:CONTAINS_ENTITY]->(cve:Entity {label: 'CVE'})
MATCH (d)-[:CONTAINS_ENTITY]->(vendor:Entity {label: 'VENDOR'})
RETURN d.id, cve.text, vendor.text
```

#### Entity Co-occurrence Analysis
```cypher
// Find entities that frequently appear together
MATCH (d:Document)-[:CONTAINS_ENTITY]->(e1:Entity {label: 'VENDOR'})
MATCH (d)-[:CONTAINS_ENTITY]->(e2:Entity {label: 'PROTOCOL'})
WHERE e1 <> e2
RETURN e1.text, e2.text, count(d) as co_occurrences
ORDER BY co_occurrences DESC
LIMIT 20
```

### Performance Optimization
- **Index Strategy**: Composite index on (text, label) for fast entity lookups
- **Batch Insertion**: 100 entities per transaction (ingestion_agent.py)
- **Query Caching**: Frequently-used queries cached by Neo4j
- **Connection Pooling**: Node.js driver manages connection pool

---

## 2. Qdrant - Vector Database

### Connection Details
- **URL**: http://localhost:6333
- **API Key**: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ= (⚠️ default)
- **Admin UI**: http://localhost:6334
- **Container Status**: Unhealthy (needs investigation)

### Current Data (2025-11-11)
- **Collections**: 12 active collections
- **Embedding Model**: spaCy en_core_web_lg (768 dimensions)
- **Distance Metric**: Cosine similarity
- **Vector Dimension**: 768

### Purpose
- Store entity embeddings for semantic search
- Semantic similarity queries (find similar entities)
- Document chunk embeddings for retrieval
- Recommendation engine (similar documents)
- Clustering and classification

### Collection Schema

#### Entity Embeddings Collection
```typescript
{
  collection_name: "entity_embeddings",
  vectors: {
    size: 768,  // spaCy en_core_web_lg dimension
    distance: "Cosine"
  },
  payload_schema: {
    entityId: "keyword",      // Neo4j entity ID
    entityText: "text",       // Entity text content
    entityType: "keyword",    // Entity label (VENDOR, CVE, etc.)
    documentId: "keyword",    // Source document ID
    confidence: "float",      // Extraction confidence
    source: "keyword",        // 'pattern' or 'neural'
    timestamp: "datetime"     // Embedding creation time
  }
}
```

#### Document Embeddings Collection
```typescript
{
  collection_name: "document_embeddings",
  vectors: {
    size: 768,
    distance: "Cosine"
  },
  payload_schema: {
    documentId: "keyword",
    chunkId: "keyword",
    chunkText: "text",
    chunkIndex: "integer",
    fileName: "text",
    sector: "keyword",
    subsector: "keyword",
    tags: "text[]"
  }
}
```

### Vector Operations

#### Insert Embeddings
```typescript
import { QdrantClient } from '@qdrant/js-client-rest';

const qdrantClient = new QdrantClient({
  url: 'http://localhost:6333',
  apiKey: process.env.QDRANT_API_KEY
});

// Upsert entity embedding
await qdrantClient.upsert("entity_embeddings", {
  points: [{
    id: entityId,
    vector: embedding,  // 768-dim array from spaCy
    payload: {
      entityId,
      entityText,
      entityType,
      documentId,
      confidence,
      source,
      timestamp: new Date().toISOString()
    }
  }]
});
```

#### Semantic Search (Find similar entities)
```typescript
const results = await qdrantClient.search("entity_embeddings", {
  vector: queryEmbedding,  // 768-dim query vector
  limit: 10,
  filter: {
    must: [
      { key: "entityType", match: { value: "VENDOR" } }
    ]
  },
  with_payload: true,
  score_threshold: 0.7  // Cosine similarity threshold
});

// Results format:
// [
//   {
//     id: "entity-123",
//     score: 0.95,  // Cosine similarity
//     payload: { entityText: "Siemens S7-1500", entityType: "VENDOR", ... }
//   }
// ]
```

#### Recommendation (Find similar documents)
```typescript
const similarDocs = await qdrantClient.search("document_embeddings", {
  vector: documentEmbedding,
  limit: 5,
  filter: {
    must: [
      { key: "sector", match: { value: "Infrastructure" } }
    ]
  }
});
```

### Performance Optimization
- **HNSW Index**: Hierarchical Navigable Small World for fast approximate search
- **Quantization**: Optional quantization to reduce memory usage
- **Batch Insertion**: Insert embeddings in batches of 100
- **Shard Distribution**: Distribu

te collections across shards for scalability

---

## 3. MySQL - Structured Data Storage

### Connection Details
- **Host**: localhost:3306
- **User**: root (⚠️ default credentials)
- **Password**: openspg (⚠️ change for production)
- **Database**: openspg
- **Container Status**: Healthy

### Current Data (2025-11-11)
- **Tables**: 33 total tables
- **Purpose**: User management, document metadata, job tracking, system configuration

### Schema Design

#### Users Table
```sql
CREATE TABLE users (
  id VARCHAR(36) PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin', 'user', 'viewer') DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_email (email),
  INDEX idx_role (role)
);
```

#### Documents Table
```sql
CREATE TABLE documents (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  filename VARCHAR(255) NOT NULL,
  file_type VARCHAR(50) NOT NULL,
  file_size BIGINT NOT NULL,
  minio_path VARCHAR(500) NOT NULL,
  sha256_hash VARCHAR(64) NOT NULL,
  status ENUM('uploaded', 'processing', 'completed', 'failed') DEFAULT 'uploaded',
  sector VARCHAR(100),
  subsector VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  processed_at TIMESTAMP NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at),
  INDEX idx_sha256 (sha256_hash)
);
```

#### Jobs Table (Pipeline tracking)
```sql
CREATE TABLE jobs (
  id VARCHAR(36) PRIMARY KEY,
  document_id VARCHAR(36) NOT NULL,
  job_type ENUM('parse', 'classification', 'ner', 'ingestion', 'embedding') NOT NULL,
  status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
  priority INT DEFAULT 0,
  progress INT DEFAULT 0,  -- 0-100
  attempts INT DEFAULT 0,
  max_attempts INT DEFAULT 3,
  error_message TEXT NULL,
  started_at TIMESTAMP NULL,
  completed_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
  INDEX idx_document_id (document_id),
  INDEX idx_status (status),
  INDEX idx_job_type (job_type),
  INDEX idx_priority (priority)
);
```

### Query Optimization
- **Indexes**: All foreign keys, status fields, and timestamp fields indexed
- **Connection Pooling**: MySQL driver manages connection pool (max 10 connections)
- **Query Caching**: Frequently-used queries cached
- **Partitioning**: Consider partitioning documents table by created_at (future optimization)

---

## 4. MinIO - Object Storage

### Connection Details
- **Console**: http://localhost:9001
- **Endpoint**: http://localhost:9000
- **Access Key**: minio (⚠️ default credentials)
- **Secret Key**: minio@openspg (⚠️ change for production)
- **Bucket**: aeon-documents
- **Container Status**: Healthy

### Purpose
- Store uploaded documents (PDF, DOCX, TXT, MD)
- Store processed files (extracted text, entities, metadata)
- Backup and archival storage
- Binary data storage for large files

### Bucket Structure

```
aeon-documents/
├── uploads/                     # Raw uploaded files
│   ├── 2025-11-11_10-30-00_technical_spec.pdf
│   ├── 2025-11-11_10-35-15_manual.docx
│   └── ...
├── processed/                   # Processed outputs
│   ├── {documentId}/
│   │   ├── text.txt             # Extracted text
│   │   ├── entities.json        # NER results
│   │   └── metadata.json        # Document metadata
└── archives/                    # Archived files (by date)
    ├── 2025-11/
    │   ├── 2025-11-01/
    │   └── 2025-11-02/
```

### Operations

#### Upload Document
```typescript
import { Client as MinioClient } from 'minio';

const minioClient = new MinioClient({
  endPoint: 'localhost',
  port: 9000,
  useSSL: false,
  accessKey: 'minio',
  secretKey: 'minio@openspg'
});

// Upload file
const filename = `uploads/${new Date().toISOString()}_${file.name}`;
await minioClient.putObject(
  'aeon-documents',
  filename,
  fileBuffer,
  fileSize,
  { 'Content-Type': file.type }
);
```

#### Retrieve Document
```typescript
// Get file stream
const stream = await minioClient.getObject('aeon-documents', filename);

// Get file metadata
const stat = await minioClient.statObject('aeon-documents', filename);
// { size: 1024000, etag: "...", lastModified: Date }
```

#### List Files
```typescript
const objectsStream = minioClient.listObjects('aeon-documents', 'uploads/', true);

objectsStream.on('data', (obj) => {
  console.log(obj.name, obj.size, obj.lastModified);
});
```

### Lifecycle Policies
- **Automatic Archival**: Move files older than 90 days to archives/
- **Retention**: Keep archives for 365 days
- **Versioning**: Enabled for accidental deletion recovery
- **Backup**: Daily backup to external storage (recommended for production)

---

## Database Integration Strategy

### Data Flow (Complete Pipeline)

```
1. Document Upload
   ↓
   MinIO (raw file storage)
   MySQL (document metadata insert)

2. Queue Job
   ↓
   BullMQ (in-memory queue, production: Redis)

3. Classification (classifier_agent.py)
   ↓
   MySQL (update job status to 'classifying', progress 10-40%)

4. NER Extraction (ner_agent.py)
   ↓
   Extract 18 entity types (pattern + neural)
   MySQL (update job status to 'extracting', progress 40-70%)

5. Graph Ingestion (ingestion_agent.py)
   ↓
   Neo4j (create Document, merge Entities, create relationships)
   MySQL (update job status to 'ingesting', progress 70-100%)

6. Embedding Generation (future: embedding_agent.py)
   ↓
   Generate embeddings with spaCy en_core_web_lg
   Qdrant (upsert entity/document embeddings)
   MySQL (update job status to 'completed', progress 100%)

7. Query & Visualization
   ↓
   Neo4j (graph traversal, pattern matching)
   Qdrant (semantic search, similarity)
   MySQL (document metadata, job status)
   MinIO (retrieve original files)
```

### Transaction Management
- **Distributed Transactions**: Not implemented (eventual consistency model)
- **Rollback Strategy**: If ingestion fails, Neo4j entities may remain (manual cleanup required)
- **Data Synchronization**: Document ID is the common key across all databases
- **Idempotency**: Entity deduplication ensures re-processing same document doesn't create duplicates

### Backup and Recovery

**Neo4j**:
- Automatic backups configured in container
- Manual backup: `neo4j-admin database backup neo4j --to-path=/backups`

**MySQL**:
- Daily backups recommended: `mysqldump -u root -p openspg > backup.sql`
- Point-in-time recovery with binary logs

**MinIO**:
- Versioning enabled for accidental deletion recovery
- Mirror to external S3 bucket for disaster recovery

**Qdrant**:
- Snapshot backups: `qdrant-cli snapshot create`
- Restore from snapshot: `qdrant-cli snapshot restore`

---

## Monitoring and Performance

### Metrics Tracking

**Neo4j Metrics**:
- Query performance: PROFILE/EXPLAIN for slow queries
- Storage utilization: Disk space usage for graph.db
- Connection pool: Active connections, wait time
- Index performance: Index hit rates

**Qdrant Metrics**:
- Search latency: <50ms for semantic queries
- Memory usage: Vector index size
- Cache hit rates: Query result caching

**MySQL Metrics**:
- Query performance: Slow query log
- Connection pool: Max connections, wait time
- Storage: Table sizes, index sizes

**MinIO Metrics**:
- Storage capacity: Bucket size, object count
- Transfer rates: Upload/download bandwidth
- API requests: Request rate, error rate

### Performance Optimization

**Neo4j**:
- Use MERGE instead of CREATE for deduplication
- Batch inserts (100 entities per transaction)
- Index all frequently-queried properties
- Use PROFILE to identify slow queries

**Qdrant**:
- HNSW index configuration for fast search
- Batch upsert operations
- Use filters to reduce search space
- Quantization for memory optimization

**MySQL**:
- Index all foreign keys and status fields
- Connection pooling (max 10 connections)
- Query caching for frequent queries
- Partition large tables by date

**MinIO**:
- Use parallel uploads for large files
- Enable versioning for recovery
- Lifecycle policies for automatic archival
- Compression for text files

---

*Database Architecture Documentation | AEON DT v1.0.0 | 2025-11-11*
*Multi-Database System: Neo4j (graph) + Qdrant (vector) + MySQL (metadata) + MinIO (storage)*
