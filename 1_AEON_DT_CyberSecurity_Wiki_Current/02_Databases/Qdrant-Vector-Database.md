# Qdrant Vector Database API Documentation

**File:** Qdrant-Vector-Database.md
**Created:** 2025-11-03 17:09:18 CST
**Modified:** 2025-11-03 17:09:18 CST
**Version:** v1.0.0
**Author:** SuperClaude API Documentation Specialist
**Purpose:** Professional API documentation for Qdrant vector database deployment
**Status:** ACTIVE

**Tags:** #qdrant #vectordb #memory #swarm #api-documentation #docker

**Related Documentation:**
- [[Docker-Architecture]] - Container deployment architecture
- [[Swarm-Coordination]] - Multi-agent coordination patterns

---

## Executive Summary

Qdrant is a high-performance vector similarity search engine deployed as Docker container `openspg-qdrant` for AI agent memory storage, swarm coordination, and knowledge graph operations. This deployment uses the latest Qdrant image with API key authentication, exposing REST (6333) and gRPC (6334) endpoints.

**System Status:** Running (Health: Unhealthy - requires investigation)
**Current State:** 12 active collections, 3072-dimensional vectors, Cosine distance metric

---

## Container Configuration

### Deployment Details

```yaml
Container Information:
  Name: openspg-qdrant
  Image: qdrant/qdrant:latest
  Status: running
  Health: unhealthy
  Created: 2025-10-31T05:38:16Z
  Timezone: Asia/Shanghai

Network Configuration:
  HTTP API Port: 6333 (0.0.0.0:6333 → 6333/tcp)
  gRPC Port: 6334 (0.0.0.0:6334 → 6334/tcp)
  Dashboard URL: http://localhost:6333/dashboard

Authentication:
  API Key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=
  Header: api-key: [API_KEY]
  Enforcement: Required for all operations
```

### Environment Variables

```bash
# Timezone Configuration
TZ=Asia/Shanghai
LANG=C.UTF-8

# Authentication
QDRANT__SERVICE__API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=

# Performance Tuning
QDRANT__STORAGE__PERFORMANCE__MAX_SEARCH_THREADS=4
QDRANT__COLLECTION__DEFAULT_HNSW_M=16
QDRANT__COLLECTION__DEFAULT_HNSW_EF_CONSTRUCT=100
QDRANT__STORAGE__OPTIMIZERS__DEFAULT_SEGMENT_NUMBER=2

# Logging
QDRANT__LOG_LEVEL=INFO

# Runtime Mode
RUN_MODE=production
```

---

## REST API Reference

### Base URL

```
http://localhost:6333
```

### Authentication

All requests require API key authentication:

```bash
# Header-based authentication
curl -H "api-key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=" \
     http://localhost:6333/collections
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized (missing or invalid API key)
- `404` - Resource not found
- `500` - Internal server error

---

### Collection Management

#### List All Collections

```http
GET /collections
```

**Response:**
```json
{
  "result": {
    "collections": [
      {"name": "implementation_decisions"},
      {"name": "schema_knowledge"},
      {"name": "agent_shared_memory"}
    ]
  },
  "status": "ok",
  "time": 0.000011713
}
```

#### Get Collection Info

```http
GET /collections/{collection_name}
```

**Response:**
```json
{
  "result": {
    "status": "green",
    "optimizer_status": "ok",
    "indexed_vectors_count": 0,
    "points_count": 4,
    "segments_count": 2,
    "config": {
      "params": {
        "vectors": {
          "size": 3072,
          "distance": "Cosine"
        },
        "shard_number": 1,
        "replication_factor": 1,
        "on_disk_payload": true
      },
      "hnsw_config": {
        "m": 16,
        "ef_construct": 100,
        "full_scan_threshold": 10000
      }
    }
  }
}
```

#### Create Collection

```http
PUT /collections/{collection_name}
```

**Request Body:**
```json
{
  "vectors": {
    "size": 3072,
    "distance": "Cosine"
  }
}
```

#### Delete Collection

```http
DELETE /collections/{collection_name}
```

---

### Point Operations

#### Insert/Update Points

```http
PUT /collections/{collection_name}/points
```

**Request Body:**
```json
{
  "points": [
    {
      "id": "uuid-or-integer",
      "vector": [0.1, 0.2, ..., 0.3],
      "payload": {
        "agent_id": "researcher-001",
        "timestamp": "2025-11-03T17:00:00Z",
        "content": "Memory content"
      }
    }
  ]
}
```

#### Search Points

```http
POST /collections/{collection_name}/points/search
```

**Request Body:**
```json
{
  "vector": [0.1, 0.2, ..., 0.3],
  "limit": 10,
  "with_payload": true,
  "with_vector": false,
  "filter": {
    "must": [
      {
        "key": "agent_id",
        "match": {"value": "researcher-001"}
      }
    ]
  }
}
```

**Response:**
```json
{
  "result": [
    {
      "id": "point-id",
      "version": 1,
      "score": 0.95,
      "payload": {
        "agent_id": "researcher-001",
        "content": "Relevant memory"
      }
    }
  ],
  "status": "ok",
  "time": 0.004496
}
```

#### Scroll Points (Pagination)

```http
POST /collections/{collection_name}/points/scroll
```

**Request Body:**
```json
{
  "limit": 100,
  "with_payload": true,
  "with_vector": false
}
```

#### Get Point by ID

```http
GET /collections/{collection_name}/points/{point_id}
```

#### Delete Points

```http
POST /collections/{collection_name}/points/delete
```

**Request Body:**
```json
{
  "points": ["id1", "id2", "id3"]
}
```

---

## Collection Catalog

### Current Collections (12 Total)

#### 1. implementation_decisions
**Purpose:** Store architectural and implementation decisions
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Points:** 4
**Usage:** Tracks project design choices, rationale, and trade-offs

#### 2. schema_knowledge
**Purpose:** Knowledge graph schema definitions and ontology mappings
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Usage:** Stores OpenSPG schema structures, entity relationships

#### 3. agent_shared_memory
**Purpose:** Cross-agent memory sharing and coordination
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Points:** 4
**Usage:** Swarm coordination, agent communication, shared context

#### 4. operation_logs
**Purpose:** System operation and activity logging
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Usage:** Audit trail, debugging, performance monitoring

#### 5. query_patterns
**Purpose:** Store successful query patterns and optimizations
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Usage:** Query optimization, pattern reuse, performance tuning

#### 6. ontology_checkpoints
**Purpose:** Versioned ontology snapshots and checkpoints
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Usage:** Schema versioning, rollback capability, migration tracking

#### 7. RedAgent_Org_Spectrum_Safety
**Purpose:** Red team agent organizational safety analysis
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Usage:** Security assessment, threat modeling, vulnerability patterns

#### 8. redagent_decision_patterns
**Purpose:** Red team agent decision-making patterns
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Usage:** Attack strategy patterns, decision trees, threat intelligence

#### 9. redagent_threat_intelligence
**Purpose:** Threat intelligence and vulnerability data
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Usage:** CVE tracking, exploit patterns, security advisories

#### 10. redagent_analysis_memories
**Purpose:** Historical security analysis and findings
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Usage:** Past assessments, learned patterns, remediation tracking

#### 11. redagent_validation_cache
**Purpose:** Validation results and test outcomes
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Usage:** Test result caching, validation patterns, quality gates

#### 12. redagent_core_knowledge
**Purpose:** Core security knowledge base
**Vector Dimensions:** 3072
**Distance Metric:** Cosine
**Usage:** Security fundamentals, best practices, compliance requirements

---

## Vector Configuration

### Standard Configuration

```yaml
Vector Settings:
  Dimensions: 3072
  Distance Metric: Cosine
  Reason: Compatible with OpenAI text-embedding-3-large model

HNSW Index (Hierarchical Navigable Small World):
  M: 16 (number of bi-directional links)
  ef_construct: 100 (construction time search depth)
  full_scan_threshold: 10000 (switch to exact search below this)
  on_disk: false (keep index in memory)

Sharding:
  Shard Number: 1
  Replication Factor: 1
  Write Consistency Factor: 1

Storage:
  On-Disk Payload: true
  Payload storage on disk to reduce memory usage
```

### Distance Metrics

**Cosine Distance** (Used by all collections)
- Range: 0.0 to 2.0 (smaller is more similar)
- Measures angle between vectors
- Preferred for text embeddings
- Normalized vectors: independent of magnitude

**Alternative Metrics** (Available but not used):
- **Euclidean:** Straight-line distance
- **Dot Product:** Raw similarity score

---

## Swarm Coordination Usage

### Agent Memory Patterns

```python
# Store agent decision
{
  "id": "decision_123",
  "vector": embedding_vector,  # 3072-dim
  "payload": {
    "agent_id": "researcher-001",
    "agent_type": "researcher",
    "decision": "Selected GPT-4 for analysis",
    "rationale": "Higher accuracy needed",
    "timestamp": "2025-11-03T17:00:00Z",
    "context": {
      "task": "vulnerability-analysis",
      "complexity": "high"
    }
  }
}

# Query similar decisions
{
  "vector": current_task_embedding,
  "limit": 5,
  "filter": {
    "must": [
      {"key": "agent_type", "match": {"value": "researcher"}},
      {"key": "context.complexity", "match": {"value": "high"}}
    ]
  }
}
```

### Cross-Agent Communication

```python
# Share knowledge between agents
{
  "id": "shared_knowledge_456",
  "vector": knowledge_embedding,
  "payload": {
    "source_agent": "coder-001",
    "target_agents": ["reviewer-001", "tester-001"],
    "knowledge_type": "implementation_pattern",
    "content": "Authentication middleware pattern",
    "relevance": 0.95,
    "timestamp": "2025-11-03T17:05:00Z"
  }
}
```

### Coordination State

```python
# Store coordination state
{
  "id": "coord_state_789",
  "vector": state_embedding,
  "payload": {
    "swarm_id": "swarm-001",
    "topology": "hierarchical",
    "active_agents": ["coordinator-001", "researcher-001", "coder-001"],
    "current_phase": "implementation",
    "bottlenecks": ["code_review_pending"],
    "timestamp": "2025-11-03T17:10:00Z"
  }
}
```

---

## Python Client Examples

### Basic Operations

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Initialize client
client = QdrantClient(
    host="localhost",
    port=6333,
    api_key="deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ="
)

# Create collection
client.create_collection(
    collection_name="my_collection",
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
)

# Insert points
client.upsert(
    collection_name="my_collection",
    points=[
        PointStruct(
            id=1,
            vector=[0.1] * 3072,
            payload={"agent_id": "agent-001", "content": "Memory content"}
        )
    ]
)

# Search
results = client.search(
    collection_name="my_collection",
    query_vector=[0.1] * 3072,
    limit=10,
    with_payload=True
)

# Get collection info
info = client.get_collection(collection_name="my_collection")
print(f"Points: {info.points_count}")
print(f"Status: {info.status}")
```

### Advanced Filtering

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Complex search with filters
results = client.search(
    collection_name="agent_shared_memory",
    query_vector=embedding_vector,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="agent_type",
                match=MatchValue(value="researcher")
            ),
            FieldCondition(
                key="timestamp",
                range={
                    "gte": "2025-11-01T00:00:00Z",
                    "lte": "2025-11-03T23:59:59Z"
                }
            )
        ]
    ),
    limit=20,
    with_payload=True,
    with_vector=False
)
```

---

## Performance Optimization

### HNSW Index Tuning

```yaml
Performance Parameters:
  max_search_threads: 4
    - Controls parallel search operations
    - Increase for higher throughput

  m: 16
    - Number of bi-directional links per node
    - Higher values: better recall, more memory
    - Lower values: faster indexing, less memory

  ef_construct: 100
    - Search depth during index construction
    - Higher values: better quality, slower indexing
    - Recommended: 100-200 for most use cases

Optimizer Settings:
  default_segment_number: 2
    - Number of segments per collection
    - More segments: better parallel performance

  flush_interval_sec: 5
    - Write-ahead log flush frequency
    - Lower values: more durability, less throughput

  indexing_threshold: 10000
    - Points count to trigger indexing
    - Adjust based on collection size
```

### Query Optimization

```python
# Optimize search performance
results = client.search(
    collection_name="implementation_decisions",
    query_vector=query_embedding,
    limit=10,

    # Performance tuning
    search_params={
        "hnsw_ef": 128,  # Higher for better recall
        "exact": False    # Use approximate search
    },

    # Reduce payload transfer
    with_payload=["agent_id", "timestamp"],  # Only specific fields
    with_vector=False  # Exclude vectors from response
)
```

---

## Monitoring and Health

### Health Check Endpoint

```bash
curl -H "api-key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=" \
     http://localhost:6333/
```

**Expected Response:**
```json
{
  "title": "qdrant - vector search engine",
  "version": "latest"
}
```

### Collection Health Status

**Status Values:**
- `green` - All shards operational
- `yellow` - Some degradation
- `red` - Critical issues

**Optimizer Status:**
- `ok` - Optimizer running normally
- `error` - Optimization issues detected

### Docker Health Investigation

**Current Issue:** Container health check failing

```bash
# Check container logs
docker logs openspg-qdrant --tail 100

# Inspect health check configuration
docker inspect openspg-qdrant | jq '.[] | .Config.Healthcheck'

# Test API accessibility
curl -H "api-key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=" \
     http://localhost:6333/collections

# Verify authentication
curl -v http://localhost:6333/collections  # Should return 401

# Check resource usage
docker stats openspg-qdrant --no-stream
```

**Common Issues:**
- Missing health check configuration in Docker
- Health check endpoint requires authentication
- Network connectivity issues
- Resource constraints (CPU/Memory)

---

## Backup and Recovery

### Collection Snapshot

```bash
# Create snapshot
curl -X POST \
  -H "api-key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=" \
  http://localhost:6333/collections/{collection_name}/snapshots

# List snapshots
curl -H "api-key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=" \
  http://localhost:6333/collections/{collection_name}/snapshots

# Download snapshot
curl -H "api-key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=" \
  -o snapshot.tar \
  http://localhost:6333/collections/{collection_name}/snapshots/{snapshot_name}

# Restore from snapshot
curl -X PUT \
  -H "api-key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=" \
  -H "Content-Type: multipart/form-data" \
  -F "snapshot=@snapshot.tar" \
  http://localhost:6333/collections/{collection_name}/snapshots/recover
```

### Data Persistence

**Volume Configuration:**
```bash
# Check mounted volumes
docker inspect openspg-qdrant | jq '.[].Mounts'

# Recommended volume mount
docker run -d \
  -p 6333:6333 -p 6334:6334 \
  -v /path/to/storage:/qdrant/storage \
  -e QDRANT__SERVICE__API_KEY="your-api-key" \
  qdrant/qdrant:latest
```

---

## Security Best Practices

### API Key Management

```bash
# Rotate API key
# 1. Generate new key
NEW_KEY=$(openssl rand -base64 32)

# 2. Update environment variable
docker stop openspg-qdrant
docker rm openspg-qdrant

docker run -d \
  --name openspg-qdrant \
  -p 6333:6333 -p 6334:6334 \
  -e QDRANT__SERVICE__API_KEY="$NEW_KEY" \
  qdrant/qdrant:latest

# 3. Update client configurations
```

### Access Control

```yaml
Network Security:
  - Bind to localhost only: -p 127.0.0.1:6333:6333
  - Use reverse proxy (nginx/traefik) with TLS
  - Implement rate limiting
  - Enable HTTPS for production

Authentication:
  - Never commit API keys to version control
  - Use environment variables or secrets management
  - Rotate keys regularly (quarterly minimum)
  - Monitor unauthorized access attempts

Collection Security:
  - Implement payload field encryption for sensitive data
  - Use separate collections for different security levels
  - Audit collection access patterns
  - Implement backup encryption
```

---

## Integration Patterns

### With Claude-Flow Swarm

```python
# Claude-Flow integration hook
def store_agent_decision(agent_id, decision, embedding):
    """Store agent decision in Qdrant for swarm coordination"""
    client = QdrantClient(
        host="localhost",
        port=6333,
        api_key=os.environ["QDRANT_API_KEY"]
    )

    client.upsert(
        collection_name="agent_shared_memory",
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "agent_id": agent_id,
                    "decision": decision,
                    "timestamp": datetime.utcnow().isoformat(),
                    "swarm_context": get_swarm_context()
                }
            )
        ]
    )

# Query relevant past decisions
def get_relevant_decisions(current_task_embedding, agent_type):
    """Retrieve similar past decisions for context"""
    results = client.search(
        collection_name="agent_shared_memory",
        query_vector=current_task_embedding,
        query_filter=Filter(
            must=[
                FieldCondition(key="agent_type", match=MatchValue(value=agent_type))
            ]
        ),
        limit=5,
        with_payload=True
    )
    return results
```

### With OpenSPG Knowledge Graph

```python
# Store schema knowledge
def store_spg_schema(schema_name, schema_data, embedding):
    """Store OpenSPG schema in Qdrant"""
    client.upsert(
        collection_name="schema_knowledge",
        points=[
            PointStruct(
                id=schema_name,
                vector=embedding,
                payload={
                    "schema_name": schema_name,
                    "schema_type": schema_data["type"],
                    "entities": schema_data["entities"],
                    "relations": schema_data["relations"],
                    "version": schema_data["version"],
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        ]
    )
```

---

## Troubleshooting

### Common Issues

**Issue:** 401 Unauthorized
```bash
# Solution: Verify API key in request header
curl -H "api-key: YOUR_API_KEY" http://localhost:6333/collections
```

**Issue:** Connection refused
```bash
# Solution: Check container status
docker ps | grep qdrant
docker logs openspg-qdrant

# Verify port binding
netstat -tulpn | grep 6333
```

**Issue:** Slow search performance
```python
# Solution: Tune HNSW parameters
# Increase ef parameter for better recall
results = client.search(
    collection_name="my_collection",
    query_vector=vector,
    search_params={"hnsw_ef": 256},  # Increase from default
    limit=10
)
```

**Issue:** High memory usage
```yaml
# Solution: Enable on-disk payload storage
params:
  on_disk_payload: true  # Store payloads on disk

# Enable quantization for large collections
quantization_config:
  scalar:
    type: "int8"
    quantile: 0.99
```

---

## API Rate Limits

**Current Configuration:** No explicit rate limits configured

**Recommended Production Limits:**
```yaml
Rate Limiting:
  Per IP: 100 requests/second
  Per API Key: 1000 requests/second
  Search Operations: 50/second
  Bulk Operations: 10/second

Implementation:
  - Use nginx/traefik reverse proxy
  - Configure rate limiting middleware
  - Monitor via prometheus/grafana
```

---

## References

**Official Documentation:**
- Qdrant Official Docs: https://qdrant.tech/documentation/
- REST API Reference: https://qdrant.github.io/qdrant/redoc/index.html
- Python Client: https://github.com/qdrant/qdrant-client

**Related Systems:**
- [[Docker-Architecture]] - Container orchestration and deployment
- [[Swarm-Coordination]] - Multi-agent coordination patterns
- [[OpenSPG-Integration]] - Knowledge graph integration

**Version History:**
- v1.0.0 (2025-11-03): Initial comprehensive API documentation

---

**Document Status:** ✅ Complete
**Review Required:** Health check investigation needed
**Next Update:** After health check resolution
**Maintained By:** System Architecture Team
