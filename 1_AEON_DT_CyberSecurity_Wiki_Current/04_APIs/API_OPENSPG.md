# AEON Digital Twin - OpenSPG API Specification

**File:** API_OPENSPG.md
**Created:** 2025-11-29 04:50:00 UTC
**Version:** 1.0.0
**Author:** AEON API Architecture Team
**Purpose:** OpenSPG Semantic Property Graph REST API specification for knowledge graph construction, reasoning, and entity management
**Status:** PLANNED - Ready for Implementation

---

## EXECUTIVE SUMMARY

OpenSPG (Semantic Property Graph) provides the knowledge graph construction and reasoning engine for the AEON Cyber Digital Twin. This API specification documents the REST endpoints for interacting with the OpenSPG server running on port 8887.

**Current Implementation Status:**
- Container: `release-openspg-server` running on port 8887
- Database Backend: Neo4j (bolt://localhost:7687)
- Metadata Storage: MySQL (port 3306)
- Object Storage: MinIO (ports 9000/9001)

**Key Capabilities:**
- Schema management (entity types, relationships, constraints)
- Entity extraction and linking
- Relationship inference
- Rule-based reasoning
- Causal inference
- Knowledge graph construction

---

## TABLE OF CONTENTS

1. [API Architecture](#api-architecture)
2. [Authentication](#authentication)
3. [Schema Management APIs](#schema-management-apis)
4. [Entity Management APIs](#entity-management-apis)
5. [Relationship APIs](#relationship-apis)
6. [Reasoning APIs](#reasoning-apis)
7. [Job Management APIs](#job-management-apis)
8. [Query APIs](#query-apis)
9. [Error Handling](#error-handling)
10. [Integration Patterns](#integration-patterns)

---

## API ARCHITECTURE

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenSPG Server (Port 8887)                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Schema Manager │  │ Entity Manager  │  │ Reasoner    │ │
│  │  - Type defs    │  │ - Extraction    │  │ - Rules     │ │
│  │  - Constraints  │  │ - Linking       │  │ - Inference │ │
│  └────────┬────────┘  └────────┬────────┘  └──────┬──────┘ │
│           │                    │                   │         │
│  ┌────────▼────────────────────▼───────────────────▼──────┐ │
│  │                    Knowledge Graph Core                 │ │
│  │  - Graph Construction  - Pattern Matching              │ │
│  │  - Semantic Reasoning  - Entity Resolution             │ │
│  └────────┬────────────────────┬───────────────────┬──────┘ │
│           │                    │                   │         │
│  ┌────────▼────┐      ┌───────▼────┐      ┌───────▼─────┐  │
│  │   Neo4j     │      │   MySQL    │      │   MinIO     │  │
│  │   Graph     │      │  Metadata  │      │  Objects    │  │
│  │   Storage   │      │  Storage   │      │  Storage    │  │
│  └─────────────┘      └────────────┘      └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Base URL

| Environment | URL |
|-------------|-----|
| Development | `http://localhost:8887/api/v1` |
| Docker Network | `http://release-openspg-server:8887/api/v1` |

### Connection Parameters
```yaml
openspg_server:
  host: localhost
  port: 8887
  protocol: http

neo4j_backend:
  host: release-openspg-neo4j
  port: 7687
  user: neo4j
  password: neo4j@openspg
  database: neo4j

mysql_metadata:
  host: release-openspg-mysql
  port: 3306
  user: root
  password: openspg
  database: openspg

minio_storage:
  host: release-openspg-minio
  api_port: 9000
  console_port: 9001
  access_key: minio
  secret_key: minio@openspg
```

---

## AUTHENTICATION

### Current State
OpenSPG currently runs without authentication in development mode. Production deployment requires API key or OAuth integration.

### Planned Authentication
```http
Authorization: Bearer <api_key>
X-OpenSPG-Project: aeon-cyber-dt
```

---

## SCHEMA MANAGEMENT APIs

### Create Schema

**Endpoint:** `POST /api/v1/schema`

**Description:** Define entity types, relationship types, and constraints for the knowledge graph.

**Request:**
```json
{
  "projectId": "aeon-cyber-dt",
  "schemaName": "CyberSecurityOntology",
  "version": "1.0.0",
  "entityTypes": [
    {
      "name": "Asset",
      "description": "Physical or virtual equipment",
      "properties": [
        {"name": "assetClass", "type": "STRING", "required": true, "enum": ["OT", "IT", "IoT"]},
        {"name": "deviceType", "type": "STRING", "required": true},
        {"name": "manufacturer", "type": "STRING"},
        {"name": "model", "type": "STRING"},
        {"name": "sector", "type": "STRING"}
      ],
      "constraints": [
        {"type": "UNIQUE", "properties": ["id"]}
      ]
    },
    {
      "name": "Vulnerability",
      "description": "Security vulnerability",
      "properties": [
        {"name": "vulnType", "type": "STRING", "required": true, "enum": ["cve", "cwe", "exploit"]},
        {"name": "cveID", "type": "STRING"},
        {"name": "cvssScore", "type": "FLOAT"},
        {"name": "epssScore", "type": "FLOAT"},
        {"name": "severity", "type": "STRING"}
      ]
    }
  ],
  "relationshipTypes": [
    {
      "name": "HAS_VULNERABILITY",
      "sourceType": "Asset",
      "targetType": "Vulnerability",
      "properties": [
        {"name": "discoveredDate", "type": "DATE"},
        {"name": "status", "type": "STRING", "enum": ["active", "patched", "mitigated"]}
      ]
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "schemaId": "schema_aeon_cyber_dt_v1",
  "version": "1.0.0",
  "entityTypes": 2,
  "relationshipTypes": 1,
  "createdAt": "2025-11-29T04:50:00Z"
}
```

### Get Schema

**Endpoint:** `GET /api/v1/schema/{schemaId}`

**Response:**
```json
{
  "schemaId": "schema_aeon_cyber_dt_v1",
  "projectId": "aeon-cyber-dt",
  "schemaName": "CyberSecurityOntology",
  "version": "1.0.0",
  "entityTypes": [...],
  "relationshipTypes": [...],
  "createdAt": "2025-11-29T04:50:00Z",
  "modifiedAt": "2025-11-29T04:50:00Z"
}
```

### List Schemas

**Endpoint:** `GET /api/v1/schemas`

**Query Parameters:**
- `projectId` (optional): Filter by project
- `page` (default: 1)
- `limit` (default: 20)

---

## ENTITY MANAGEMENT APIs

### Create Entity

**Endpoint:** `POST /api/v1/entities`

**Request:**
```json
{
  "schemaId": "schema_aeon_cyber_dt_v1",
  "entityType": "Asset",
  "properties": {
    "id": "FW-LAW-001",
    "assetClass": "IT",
    "deviceType": "firewall",
    "manufacturer": "Cisco Systems",
    "model": "ASA5525-K9",
    "sector": "WATER"
  },
  "metadata": {
    "source": "customer_upload",
    "confidence": 0.95
  }
}
```

**Response:**
```json
{
  "success": true,
  "entityId": "ent_fw_law_001",
  "entityType": "Asset",
  "neo4jNodeId": 12345,
  "createdAt": "2025-11-29T04:55:00Z"
}
```

### Batch Create Entities

**Endpoint:** `POST /api/v1/entities/batch`

**Request:**
```json
{
  "schemaId": "schema_aeon_cyber_dt_v1",
  "entities": [
    {
      "entityType": "Asset",
      "properties": {"id": "PLC-001", "assetClass": "OT", "deviceType": "plc"}
    },
    {
      "entityType": "Asset",
      "properties": {"id": "RTU-001", "assetClass": "OT", "deviceType": "rtu"}
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "created": 2,
  "failed": 0,
  "entities": [
    {"entityId": "ent_plc_001", "status": "created"},
    {"entityId": "ent_rtu_001", "status": "created"}
  ]
}
```

### Get Entity

**Endpoint:** `GET /api/v1/entities/{entityId}`

### Search Entities

**Endpoint:** `POST /api/v1/entities/search`

**Request:**
```json
{
  "schemaId": "schema_aeon_cyber_dt_v1",
  "entityType": "Asset",
  "filters": [
    {"property": "assetClass", "operator": "eq", "value": "OT"},
    {"property": "sector", "operator": "in", "value": ["WATER", "ENERGY"]}
  ],
  "pagination": {
    "page": 1,
    "limit": 50
  }
}
```

---

## RELATIONSHIP APIs

### Create Relationship

**Endpoint:** `POST /api/v1/relationships`

**Request:**
```json
{
  "schemaId": "schema_aeon_cyber_dt_v1",
  "relationshipType": "HAS_VULNERABILITY",
  "sourceEntityId": "ent_fw_law_001",
  "targetEntityId": "ent_cve_2021_44228",
  "properties": {
    "discoveredDate": "2025-11-15",
    "status": "active"
  },
  "metadata": {
    "confidence": 0.92,
    "source": "vulnerability_scan"
  }
}
```

**Response:**
```json
{
  "success": true,
  "relationshipId": "rel_fw_cve_001",
  "neo4jRelId": 67890,
  "createdAt": "2025-11-29T05:00:00Z"
}
```

### Infer Relationships

**Endpoint:** `POST /api/v1/relationships/infer`

**Description:** Apply relationship inference rules to discover implicit relationships.

**Request:**
```json
{
  "schemaId": "schema_aeon_cyber_dt_v1",
  "inferenceRules": [
    {
      "name": "transitive_vulnerability",
      "pattern": "(Asset)-[:RUNS_SOFTWARE]->(Software)-[:HAS_VULNERABILITY]->(Vulnerability)",
      "inference": "(Asset)-[:POTENTIALLY_AFFECTED_BY]->(Vulnerability)"
    }
  ],
  "scope": {
    "entityTypes": ["Asset"],
    "maxDepth": 3
  }
}
```

**Response:**
```json
{
  "success": true,
  "inferredRelationships": 1247,
  "rulesApplied": 1,
  "executionTime": "2.3s"
}
```

---

## REASONING APIs

### Apply Reasoning Rules

**Endpoint:** `POST /api/v1/reasoning/apply`

**Description:** Execute rule-based reasoning on the knowledge graph.

**Request:**
```json
{
  "schemaId": "schema_aeon_cyber_dt_v1",
  "rules": [
    {
      "name": "vulnerability_severity_propagation",
      "condition": "Vulnerability.cvssScore >= 9.0",
      "action": "SET Asset.criticalRisk = true WHERE (Asset)-[:HAS_VULNERABILITY]->(Vulnerability)"
    },
    {
      "name": "epss_priority_classification",
      "condition": "Vulnerability.epssScore >= 0.5",
      "action": "SET Vulnerability.priority = 'NOW'"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "rulesExecuted": 2,
  "nodesModified": 4423,
  "executionTime": "5.7s",
  "results": [
    {"rule": "vulnerability_severity_propagation", "affected": 1247},
    {"rule": "epss_priority_classification", "affected": 3176}
  ]
}
```

### Causal Inference

**Endpoint:** `POST /api/v1/reasoning/causal`

**Description:** Perform causal inference to identify cause-effect relationships.

**Request:**
```json
{
  "schemaId": "schema_aeon_cyber_dt_v1",
  "query": {
    "effect": "SecurityBreach",
    "potentialCauses": ["UnpatchedVulnerability", "MisconfiguredFirewall", "PhishingAttack"],
    "confidenceThreshold": 0.7
  }
}
```

**Response:**
```json
{
  "success": true,
  "causalChains": [
    {
      "cause": "UnpatchedVulnerability",
      "effect": "SecurityBreach",
      "confidence": 0.87,
      "intermediateSteps": [
        "UnpatchedVulnerability -> ExploitAvailable -> AttackAttempt -> SecurityBreach"
      ]
    }
  ]
}
```

### Entity Linking

**Endpoint:** `POST /api/v1/reasoning/entity-linking`

**Description:** Link entities across different sources and resolve duplicates.

**Request:**
```json
{
  "schemaId": "schema_aeon_cyber_dt_v1",
  "entities": [
    {"type": "ThreatActor", "name": "APT29", "aliases": ["CozyBear", "The Dukes"]},
    {"type": "ThreatActor", "name": "Cozy Bear", "source": "threat_feed_2"}
  ],
  "linkingStrategy": "semantic_similarity",
  "threshold": 0.85
}
```

**Response:**
```json
{
  "success": true,
  "linkedEntities": [
    {
      "canonicalId": "ent_apt29",
      "linkedIds": ["ent_cozy_bear_feed2"],
      "confidence": 0.94,
      "linkType": "SAME_AS"
    }
  ]
}
```

---

## JOB MANAGEMENT APIs

### Create Job

**Endpoint:** `POST /api/v1/jobs`

**Description:** Create asynchronous jobs for large-scale operations.

**Request:**
```json
{
  "jobType": "entity_extraction",
  "config": {
    "schemaId": "schema_aeon_cyber_dt_v1",
    "source": "document_batch",
    "documentIds": ["doc_001", "doc_002"],
    "extractors": ["ner", "relationship"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "jobId": "job_extract_001",
  "status": "pending",
  "createdAt": "2025-11-29T05:10:00Z"
}
```

### Get Job Status

**Endpoint:** `GET /api/v1/jobs/{jobId}`

**Response:**
```json
{
  "jobId": "job_extract_001",
  "jobType": "entity_extraction",
  "status": "running",
  "progress": 0.65,
  "entitiesExtracted": 1247,
  "relationshipsExtracted": 892,
  "errors": 0,
  "startedAt": "2025-11-29T05:10:05Z",
  "estimatedCompletion": "2025-11-29T05:15:00Z"
}
```

### List Jobs

**Endpoint:** `GET /api/v1/jobs`

**Query Parameters:**
- `status`: pending, running, completed, failed
- `jobType`: entity_extraction, relationship_inference, reasoning
- `page`, `limit`

---

## QUERY APIs

### Execute Cypher Query

**Endpoint:** `POST /api/v1/query/cypher`

**Description:** Execute Cypher queries against the Neo4j backend through OpenSPG.

**Request:**
```json
{
  "query": "MATCH (a:Asset {assetClass: 'OT'})-[:HAS_VULNERABILITY]->(v:Vulnerability) WHERE v.cvssScore >= 9.0 RETURN a.id, v.cveID, v.cvssScore LIMIT 100",
  "parameters": {}
}
```

**Response:**
```json
{
  "success": true,
  "columns": ["a.id", "v.cveID", "v.cvssScore"],
  "rows": [
    {"a.id": "PLC-001", "v.cveID": "CVE-2021-44228", "v.cvssScore": 10.0},
    {"a.id": "RTU-002", "v.cveID": "CVE-2022-0778", "v.cvssScore": 9.8}
  ],
  "rowCount": 2,
  "executionTime": "0.045s"
}
```

### Graph Traversal Query

**Endpoint:** `POST /api/v1/query/traverse`

**Description:** Semantic graph traversal with reasoning.

**Request:**
```json
{
  "startEntity": "ent_apt29",
  "traversalPattern": "ThreatActor-[:USES]->AttackPattern-[:EXPLOITS]->Vulnerability<-[:HAS_VULNERABILITY]-Asset",
  "maxDepth": 4,
  "filters": {
    "Asset.sector": "ENERGY"
  }
}
```

**Response:**
```json
{
  "success": true,
  "paths": [
    {
      "nodes": ["APT29", "T1190", "CVE-2021-44228", "SCADA-001"],
      "relationships": ["USES", "EXPLOITS", "HAS_VULNERABILITY"],
      "pathLength": 3
    }
  ],
  "pathCount": 47,
  "executionTime": "0.234s"
}
```

---

## ERROR HANDLING

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "ENTITY_NOT_FOUND",
    "message": "Entity with ID 'ent_invalid_001' not found",
    "details": {
      "entityId": "ent_invalid_001",
      "schemaId": "schema_aeon_cyber_dt_v1"
    }
  },
  "timestamp": "2025-11-29T05:20:00Z",
  "requestId": "req_abc123"
}
```

### Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| SCHEMA_NOT_FOUND | 404 | Schema does not exist |
| ENTITY_NOT_FOUND | 404 | Entity does not exist |
| VALIDATION_ERROR | 400 | Request validation failed |
| CONSTRAINT_VIOLATION | 409 | Unique constraint violated |
| INFERENCE_ERROR | 500 | Reasoning rule execution failed |
| CONNECTION_ERROR | 503 | Backend database unavailable |

---

## INTEGRATION PATTERNS

### AEON Pipeline Integration

OpenSPG is Step 3 in the AEON data ingestion pipeline:

```
Step 1: Document Ingestion (Upload/Fetch)
         ↓
Step 2: NER Extraction (spaCy NER v9)
         ↓
Step 3: OpenSPG Reasoning (This API)    ← Current Specification
         ↓
Step 4: Neo4j Storage (Knowledge Graph)
         ↓
Step 5: Intelligence Generation (Predictions)
```

### Example Integration Flow

```python
# Python client example
import requests

OPENSPG_URL = "http://localhost:8887/api/v1"

# 1. Create entities from NER extraction
entities = [
    {"entityType": "Asset", "properties": {"id": "PLC-001", "assetClass": "OT"}},
    {"entityType": "Vulnerability", "properties": {"vulnType": "cve", "cveID": "CVE-2021-44228"}}
]

response = requests.post(f"{OPENSPG_URL}/entities/batch", json={
    "schemaId": "schema_aeon_cyber_dt_v1",
    "entities": entities
})

# 2. Infer relationships
response = requests.post(f"{OPENSPG_URL}/relationships/infer", json={
    "schemaId": "schema_aeon_cyber_dt_v1",
    "inferenceRules": [...]
})

# 3. Apply reasoning rules
response = requests.post(f"{OPENSPG_URL}/reasoning/apply", json={
    "schemaId": "schema_aeon_cyber_dt_v1",
    "rules": [...]
})
```

---

## IMPLEMENTATION STATUS

| Endpoint | Status | Priority |
|----------|--------|----------|
| Schema Management | 📋 PLANNED | P1 |
| Entity CRUD | 📋 PLANNED | P1 |
| Relationship Management | 📋 PLANNED | P1 |
| Reasoning Rules | 📋 PLANNED | P2 |
| Causal Inference | 📋 PLANNED | P2 |
| Entity Linking | 📋 PLANNED | P2 |
| Job Management | 📋 PLANNED | P1 |
| Query APIs | 📋 PLANNED | P1 |

**Estimated Implementation Effort:** 8-10 weeks

---

## RELATED DOCUMENTATION

- **OpenSPG Reasoning Process**: [../../1_2025_11-25_documentation_no_NER11/ingestion_process/INGESTION_STEP3_OPENSPG_REASONING.md]
- **Architecture Overview**: [../01_ARCHITECTURE/02_LEVELS_OVERVIEW.md]
- **API Status Roadmap**: [00_API_STATUS_AND_ROADMAP.md]
- **Docker Compose**: [../../openspg-official_neo4j/docker-compose.yml]

---

*Last Updated: 2025-11-29 | Status: SPECIFICATION COMPLETE*
