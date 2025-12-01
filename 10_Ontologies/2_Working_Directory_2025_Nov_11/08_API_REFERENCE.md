# API Reference - All API Endpoints

**File**: 08_API_REFERENCE.md
**Created**: 2025-11-11
**Version**: 1.0.0
**Purpose**: Comprehensive API endpoint documentation
**Status**: ACTIVE

## Executive Summary

Complete API reference documentation for AEON platform services including:
- **Pipeline API**: Document processing workflow (Classification → NER → Neo4j Ingestion)
- **NER v9 API**: Entity extraction with 99.00% F1 score across 16 entity types
- **MITRE Query API**: 8 specialized query capabilities for ATT&CK framework analysis
- **Upload API**: Document upload and management
- **Knowledge Graph API**: Neo4j graph queries and exploration

**Performance Metrics**:
- NER v9: 99.00% F1, 98.03% precision, 100% recall (1,718 training examples)
- Pipeline: Serial processing, 5-minute timeout per stage
- MITRE Queries: <100ms (simple) to <2s (advanced)
- Rate Limiting: 100-2000 requests/minute based on tier
- Uptime SLA: 99.9%

**Authentication**: All endpoints require Bearer token authentication (JWT) via Clerk

## API Architecture

### Base URL
```
Production: https://api.yourdomain.com/v1
Development: http://localhost:3000/api
```

### Authentication
```
Authorization: Bearer {jwt_token}
```

### Response Format
```typescript
{
  success: boolean
  data?: any
  error?: {
    code: string
    message: string
    details?: object
  }
  metadata?: {
    timestamp: string
    requestId: string
  }
}
```

## Pipeline Processing API

Base URL: `http://localhost:3000/api/pipeline`

### Overview

The Pipeline API implements a **serial document processing workflow** with three sequential stages:
1. **Classification Stage** (10-40%): Document classification via `classifier_agent.py`
2. **NER Stage** (40-70%): Named Entity Recognition via `ner_agent.py` (NER v9)
3. **Ingestion Stage** (70-100%): Neo4j graph ingestion via `ingestion_agent.py`

**Architecture**: In-memory FIFO queue, serial processing (one job at a time), 5-minute timeout per stage

---

### POST /api/pipeline/process

**Purpose**: Submit document for processing through classification → NER → ingestion pipeline

**Authentication**: Required (Clerk)

**Rate Limiting**: 100 requests per 15 minutes per IP

**Request Body**:
```json
{
  "files": [
    {
      "path": "/uploads/document.pdf",
      "name": "document.pdf",
      "size": 1024000,
      "type": "application/pdf"
    }
  ],
  "customer": "acme-corp",
  "tags": ["critical", "healthcare"],
  "classification": {
    "sector": "healthcare",
    "subsector": "medical-devices"
  }
}
```

**Parameters**:
- `files` (required): Array of file objects
  - `path` (string): File system path to document (validated against UPLOAD_DIR)
  - `name` (string): Human-readable filename
  - `size` (number): File size in bytes (max: 100MB)
  - `type` (string): MIME type (e.g., "application/pdf")
- `customer` (required): Customer identifier
- `tags` (required): Array of classification tags
- `classification` (required): Classification object
  - `sector` (required): Primary sector
  - `subsector` (optional): Secondary sector

**Response (Success - 200)**:
```json
{
  "success": true,
  "jobs": [
    {
      "jobId": "550e8400-e29b-41d4-a716-446655440000",
      "status": "queued",
      "progress": 0,
      "message": "Queued: document.pdf",
      "fileName": "document.pdf"
    }
  ],
  "message": "Started processing 1 file(s)"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:3000/api/pipeline/process \
  -H "Authorization: Bearer YOUR_CLERK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [{
      "path": "/uploads/threat-report.pdf",
      "name": "threat-report.pdf",
      "size": 524288,
      "type": "application/pdf"
    }],
    "customer": "acme-corp",
    "tags": ["threat-intel", "apt28"],
    "classification": {
      "sector": "cybersecurity",
      "subsector": "threat-intelligence"
    }
  }'
```

**Error Responses**:
```json
// 401 Unauthorized
{ "error": "Unauthorized" }

// 400 Bad Request - Missing files
{ "error": "No files provided" }

// 400 Bad Request - Missing required fields
{ "error": "Customer and classification sector are required" }

// 413 Payload Too Large
{
  "error": "File exceeds maximum size of 100MB",
  "details": "threat-report.pdf is 150MB"
}

// 429 Rate Limit Exceeded
{ "error": "Rate limit exceeded. Try again later." }

// 500 Internal Server Error
{
  "error": "Failed to submit for processing",
  "details": "Python environment not configured"
}
```

---

### GET /api/pipeline/status/:jobId

**Purpose**: Get real-time job status and progress

**Authentication**: None (⚠️ Security Issue - should require auth)

**Path Parameters**:
- `jobId` (required): UUID of the job

**Response (Success - 200)**:
```json
{
  "success": true,
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "fileName": "document.pdf",
  "status": "extracting",
  "progress": 45,
  "message": "Classification complete, starting entity extraction",
  "createdAt": "2025-11-11T10:30:00Z",
  "completedAt": null,
  "customer": "acme-corp",
  "tags": ["threat-intel", "apt28"],
  "classification": {
    "sector": "cybersecurity",
    "subsector": "threat-intelligence"
  },
  "steps": {
    "classification": {
      "status": "complete",
      "progress": 100
    },
    "ner": {
      "status": "running",
      "progress": 50
    },
    "ingestion": {
      "status": "pending",
      "progress": 0
    }
  }
}
```

**Job Status Values**:
- `queued`: Waiting in queue (progress: 0%)
- `classifying`: Running classifier_agent.py (progress: 10-40%)
- `extracting`: Running ner_agent.py (progress: 40-70%)
- `ingesting`: Running ingestion_agent.py (progress: 70-100%)
- `complete`: Finished successfully (progress: 100%)
- `failed`: Error during processing (progress: 0%, error field populated)

**Step Status Values**:
- `pending`: Not yet started (progress: 0)
- `running`: Currently processing (progress: 50)
- `complete`: Successfully finished (progress: 100)

**Response (Job Not Found - 404)**:
```json
{ "error": "Job not found" }
```

**cURL Example**:
```bash
curl http://localhost:3000/api/pipeline/status/550e8400-e29b-41d4-a716-446655440000
```

---

### GET /api/pipeline/process

**Purpose**: Get overall queue status and statistics

**Authentication**: Required (Clerk)

**Response (Success - 200)**:
```json
{
  "success": true,
  "jobs": [],
  "queueStatus": {
    "waiting": 5,      // Jobs in queue not yet started
    "active": 1,       // Jobs currently processing
    "completed": 23,   // Successfully completed jobs
    "failed": 2,       // Failed jobs
    "delayed": 0,      // Currently 0 (not implemented)
    "total": 31        // Sum of all jobs
  }
}
```

**cURL Example**:
```bash
curl -H "Authorization: Bearer YOUR_CLERK_TOKEN" \
  http://localhost:3000/api/pipeline/process
```

---

### Pipeline Processing Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   Document Processing Flow                   │
└─────────────────────────────────────────────────────────────┘

CLIENT                    API                         AGENTS
  │                        │                           │
  ├─ POST /process ────────>│                          │
  │                        ├─ Validation              │
  │                        ├─ Create Job              │
  │                        ├─ Add to Queue            │
  │                    <───┤ Response (queued)        │
  │                        │                          │
  │                        ├─ Start processQueue()    │
  │                        ├─ Extract job from queue  │
  │                        │                   ┌──────>│
  │                        │          Stage 1: classifier_agent.py
  │  (polling)             │          (0-5 min, progress: 10→40%)
  ├─ GET /status/jobId ───>│
  │                    <───┤
  │                        │                   <──────┤
  │                        │                          │
  │                        │                   ┌──────>│
  │                        │          Stage 2: ner_agent.py (NER v9)
  ├─ GET /status/jobId ───>│          (0-5 min, progress: 40→70%)
  │                    <───┤          (extracts entities)
  │                        │                   <──────┤
  │                        │                          │
  │                        │                   ┌──────>│
  │                        │          Stage 3: ingestion_agent.py
  ├─ GET /status/jobId ───>│          (0-5 min, progress: 70→100%)
  │                    <───┤          (writes to Neo4j)
  │  Result: 100% complete │                   <──────┤
  │
```

---

### Pipeline Configuration

**Environment Variables**:
```bash
PYTHON_PATH=python3           # Python executable location
AGENTS_PATH=../agents         # Directory containing Python agents
UPLOAD_DIR=/uploads           # Safe directory for uploaded files
```

**Processing Characteristics**:
- **Serial Processing**: Only one job processes at a time (FIFO queue)
- **Stage Timeout**: 5 minutes per stage (classifier, NER, ingestion)
- **Total Timeout**: Maximum 15 minutes per document (3 stages × 5 min)
- **In-Memory Storage**: All state lost on server restart
- **No Persistence**: Jobs cannot be resumed after crash
- **No Cancellation**: Jobs run to completion or timeout

**Known Limitations**:
1. In-memory storage (data lost on restart)
2. Serial processing (only 1 file at a time)
3. No job persistence (cannot resume)
4. Rate limit in-memory (resets per instance)
5. Status route unauthenticated (security risk)
6. Fixed 5-minute timeout (long documents may fail)

---

## NER v9 Entity Extraction API

Base URL: `http://localhost:8000/api/v1/ner`

**Model Version**: v9.0.0 (2025-11-08)
**Status**: ✅ **PRODUCTION DEPLOYED**
**Performance**: 99.00% F1, 98.03% Precision, 100.00% Recall
**Training Dataset**: 1,718 examples across 16 entity types

### Supported Entity Types (16 Total)

**Infrastructure Entities** (6 types):
- `VENDOR`: Equipment manufacturers (e.g., Siemens, Rockwell, ABB)
- `EQUIPMENT`: Industrial equipment (e.g., SIMATIC S7-1200 PLC, Stratix switches)
- `PROTOCOL`: Industrial protocols (e.g., Modbus, DNP3, OPC-UA)
- `SECURITY`: Security mechanisms (e.g., TLS 1.2, AES-256, firewall rules)
- `HARDWARE_COMPONENT`: Physical components (e.g., CPU modules, I/O cards)
- `SOFTWARE_COMPONENT`: Software components (e.g., firmware, HMI software)

**Cybersecurity Entities** (5 types):
- `VULNERABILITY`: CVE identifiers (e.g., CVE-2023-12345)
- `CWE`: Common Weakness Enumeration (e.g., CWE-89)
- `CAPEC`: Attack Pattern Enumeration (e.g., CAPEC-66)
- `WEAKNESS`: Security weaknesses (e.g., SQL injection, buffer overflow)
- `OWASP`: OWASP Top 10 categories

**MITRE Entities** (5 types):
- `ATTACK_TECHNIQUE`: MITRE ATT&CK techniques (e.g., T1566)
- `THREAT_ACTOR`: APT groups (e.g., APT28, Lazarus Group)
- `SOFTWARE`: Malware/tools (e.g., Mimikatz, Cobalt Strike)
- `DATA_SOURCE`: Detection data sources
- `MITIGATION`: Defensive measures (e.g., M1047)

---

### POST /api/v1/ner/extract

**Purpose**: Extract entities from unstructured text using NER v9 model

**Authentication**: Required (Bearer token)

**Request Body**:
```json
{
  "text": "Siemens SIMATIC S7-1200 PLC vulnerable to CVE-2023-12345 using Modbus protocol. APT28 leveraged Mimikatz for T1003 credential dumping.",
  "entity_types": [
    "VENDOR",
    "EQUIPMENT",
    "VULNERABILITY",
    "PROTOCOL",
    "THREAT_ACTOR",
    "SOFTWARE",
    "ATTACK_TECHNIQUE"
  ],
  "confidence_threshold": 0.85
}
```

**Parameters**:
- `text` (required): Text to analyze (max: 10,000 characters)
- `entity_types` (optional): Filter entity types (default: all 16 types)
- `confidence_threshold` (optional): Minimum confidence score (default: 0.85, range: 0.0-1.0)

**Response (Success - 200)**:
```json
{
  "status": "success",
  "entities": [
    {
      "text": "Siemens",
      "label": "VENDOR",
      "start": 0,
      "end": 7,
      "confidence": 0.99,
      "neo4j_id": "vendor_siemens",
      "linked_entity": {
        "id": "vendor_siemens",
        "name": "Siemens",
        "type": "Vendor"
      }
    },
    {
      "text": "SIMATIC S7-1200 PLC",
      "label": "EQUIPMENT",
      "start": 8,
      "end": 27,
      "confidence": 0.98,
      "neo4j_id": "equip_simatic_s7_1200"
    },
    {
      "text": "CVE-2023-12345",
      "label": "VULNERABILITY",
      "start": 42,
      "end": 56,
      "confidence": 1.00,
      "neo4j_id": "CVE-2023-12345"
    },
    {
      "text": "Modbus",
      "label": "PROTOCOL",
      "start": 63,
      "end": 69,
      "confidence": 0.97,
      "neo4j_id": "protocol_modbus"
    },
    {
      "text": "APT28",
      "label": "THREAT_ACTOR",
      "start": 80,
      "end": 85,
      "confidence": 0.98,
      "neo4j_id": "G0016"
    },
    {
      "text": "Mimikatz",
      "label": "SOFTWARE",
      "start": 97,
      "end": 105,
      "confidence": 0.97,
      "neo4j_id": "S0002"
    },
    {
      "text": "T1003",
      "label": "ATTACK_TECHNIQUE",
      "start": 110,
      "end": 115,
      "confidence": 0.99,
      "neo4j_id": "T1003"
    }
  ],
  "metadata": {
    "processing_time_ms": 23,
    "model_version": "v9",
    "total_entities": 7,
    "model_f1_score": 0.99
  }
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/v1/ner/extract \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "APT28 used Mimikatz to dump credentials via T1003.",
    "entity_types": ["THREAT_ACTOR", "SOFTWARE", "ATTACK_TECHNIQUE"],
    "confidence_threshold": 0.85
  }'
```

---

### POST /api/v1/ner/extract-batch

**Purpose**: Extract entities from multiple texts in parallel

**Authentication**: Required (Bearer token)

**Request Body**:
```json
{
  "texts": [
    "APT28 used phishing emails to deliver malware.",
    "Mimikatz dumped LSASS credentials via T1003.",
    "CVE-2021-44228 Log4j vulnerability exploited."
  ],
  "entity_types": ["THREAT_ACTOR", "SOFTWARE", "ATTACK_TECHNIQUE", "VULNERABILITY"],
  "confidence_threshold": 0.80
}
```

**Parameters**:
- `texts` (required): Array of text strings (max: 100 texts)
- `entity_types` (optional): Filter entity types
- `confidence_threshold` (optional): Minimum confidence (default: 0.80)

**Response (Success - 200)**:
```json
{
  "status": "success",
  "results": [
    {
      "text_index": 0,
      "entities": [
        {
          "text": "APT28",
          "label": "THREAT_ACTOR",
          "start": 0,
          "end": 5,
          "confidence": 0.98,
          "neo4j_id": "G0016"
        }
      ]
    },
    {
      "text_index": 1,
      "entities": [
        {
          "text": "Mimikatz",
          "label": "SOFTWARE",
          "confidence": 0.97,
          "neo4j_id": "S0002"
        },
        {
          "text": "T1003",
          "label": "ATTACK_TECHNIQUE",
          "confidence": 0.99,
          "neo4j_id": "T1003"
        }
      ]
    },
    {
      "text_index": 2,
      "entities": [
        {
          "text": "CVE-2021-44228",
          "label": "VULNERABILITY",
          "confidence": 1.0,
          "neo4j_id": "CVE-2021-44228"
        }
      ]
    }
  ],
  "metadata": {
    "processing_time_ms": 67,
    "total_texts": 3,
    "total_entities": 4
  }
}
```

---

### POST /api/v1/ner/link

**Purpose**: Extract entities and create Neo4j relationships

**Authentication**: Required (Bearer token)

**Request Body**:
```json
{
  "text": "APT28 exploited CVE-2021-44228 using Cobalt Strike.",
  "create_relationships": true,
  "relationship_types": ["EXPLOITS_CVE", "LEVERAGES_SOFTWARE"]
}
```

**Response (Success - 200)**:
```json
{
  "status": "success",
  "entities": [
    {
      "text": "APT28",
      "label": "THREAT_ACTOR",
      "neo4j_id": "G0016"
    },
    {
      "text": "CVE-2021-44228",
      "label": "VULNERABILITY",
      "neo4j_id": "CVE-2021-44228"
    },
    {
      "text": "Cobalt Strike",
      "label": "SOFTWARE",
      "neo4j_id": "S0154"
    }
  ],
  "relationships_created": [
    {
      "type": "EXPLOITS_CVE",
      "source": "G0016",
      "target": "CVE-2021-44228",
      "confidence": 0.92
    },
    {
      "type": "LEVERAGES_SOFTWARE",
      "source": "G0016",
      "target": "S0154",
      "confidence": 0.95
    }
  ],
  "metadata": {
    "processing_time_ms": 145,
    "relationships_created": 2
  }
}
```

---

### GET /api/v1/ner/model-info

**Purpose**: Get NER model performance metrics and metadata

**Authentication**: None

**Response (Success - 200)**:
```json
{
  "status": "success",
  "model": {
    "version": "v9",
    "framework": "spaCy 3.7",
    "training_date": "2025-11-08",
    "training_completion": "2025-11-08 22:15:00 UTC",
    "training_examples": 1718,
    "entity_types": 16,
    "dataset_sources": [
      "infrastructure_v5_v6",
      "cybersecurity_v7",
      "mitre"
    ],
    "status": "production_deployed"
  },
  "performance": {
    "achieved": {
      "precision": 98.03,
      "recall": 100.00,
      "f1_score": 99.00
    },
    "target": {
      "precision": 95.0,
      "recall": 94.0,
      "f1_score": 96.0
    },
    "exceeded_target": "+3.0%",
    "improvement_over_v8": "+1.99%",
    "dataset_composition": {
      "infrastructure": {
        "examples": 183,
        "percentage": 10.7
      },
      "cybersecurity": {
        "examples": 755,
        "percentage": 43.9
      },
      "mitre": {
        "examples": 1121,
        "percentage": 65.3
      }
    }
  }
}
```

**cURL Example**:
```bash
curl http://localhost:8000/api/v1/ner/model-info
```

---

## MITRE Query API

Base URL: `http://localhost:8000/api/v1/mitre`

**Data Source**: MITRE ATT&CK Framework v14.1
**Update Frequency**: Daily
**Query Complexity**: Simple (<100ms) to Advanced (<2s)

### Query Complexity Levels

| Complexity | Hops | Response Time | Use Case |
|------------|------|---------------|----------|
| Simple | 1-2 | < 100ms | Single-entity lookups |
| Intermediate | 3-4 | < 500ms | Multi-hop analysis |
| Advanced | 5+ | < 2s | Attack paths, inference |

---

### POST /api/v1/mitre/attack-paths

**Capability**: Attack Path Discovery
**Complexity**: Advanced (3-4 hops)
**Purpose**: Discover multi-hop attack paths from threat actors to critical CVEs

**Request Body**:
```json
{
  "actor_name": "APT28",
  "min_cvss_score": 9.0,
  "max_hops": 4,
  "limit": 10
}
```

**Parameters**:
- `actor_name` (required): Threat actor name (e.g., "APT28", "Lazarus Group")
- `min_cvss_score` (optional): Minimum CVSS score filter (default: 7.0)
- `max_hops` (optional): Maximum path length (default: 4, max: 10)
- `limit` (optional): Results limit (default: 10, max: 50)

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": [
    {
      "path_id": "path_001",
      "actor": "APT28",
      "path_length": 3,
      "nodes": [
        {"type": "MitreActor", "id": "G0016", "name": "APT28"},
        {"type": "MitreTechnique", "id": "T1566", "name": "Phishing"},
        {"type": "CVE", "id": "CVE-2021-34527", "cvss_score": 9.8}
      ],
      "relationships": [
        {"type": "USES_TECHNIQUE", "confidence": 0.95},
        {"type": "EXPLOITS_CVE", "exploit_available": true}
      ]
    }
  ],
  "metadata": {
    "query_time_ms": 245,
    "total_paths": 7,
    "complexity": "advanced"
  }
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/v1/mitre/attack-paths \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "actor_name": "APT28",
    "min_cvss_score": 9.0,
    "max_hops": 4,
    "limit": 10
  }'
```

---

### GET /api/v1/mitre/defensive-gaps

**Capability**: Defensive Gap Analysis
**Complexity**: Intermediate (2-3 hops)
**Purpose**: Identify critical techniques with insufficient mitigations

**Query Parameters**:
- `tactics` (optional): Comma-separated tactics (e.g., "Initial Access,Execution")
- `max_mitigations` (optional): Maximum mitigation threshold (default: 2)
- `limit` (optional): Results limit (default: 20)

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": [
    {
      "technique_id": "T1566",
      "name": "Phishing",
      "tactic": ["Initial Access"],
      "mitigation_count": 1,
      "available_mitigations": [
        {"id": "M1047", "name": "Audit", "effectiveness": "partial"}
      ],
      "gap_severity": "high",
      "recommended_actions": [
        "Implement email filtering",
        "User security awareness training"
      ]
    }
  ],
  "metadata": {
    "query_time_ms": 123,
    "total_gaps": 15
  }
}
```

**cURL Example**:
```bash
curl "http://localhost:8000/api/v1/mitre/defensive-gaps?tactics=Initial%20Access&limit=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### GET /api/v1/mitre/actor-profile/:actor_name

**Capability**: Threat Actor Profiling
**Complexity**: Intermediate (2-3 hops)
**Purpose**: Complete TTP and toolset profile for threat actor

**Path Parameters**:
- `actor_name` (required): Actor name (e.g., "APT28", "Lazarus Group")

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "id": "G0016",
    "name": "APT28",
    "aliases": ["Fancy Bear", "Sofacy", "Sednit"],
    "country": "Russia",
    "sophistication": "advanced",
    "active": true,
    "technique_count": 142,
    "software_count": 18,
    "techniques": [
      {"id": "T1566", "name": "Phishing", "tactic": ["Initial Access"]},
      {"id": "T1003", "name": "Credential Dumping", "tactic": ["Credential Access"]}
    ],
    "software": [
      {"id": "S0002", "name": "Mimikatz", "type": "tool"},
      {"id": "S0363", "name": "Empire", "type": "tool"}
    ]
  },
  "metadata": {
    "query_time_ms": 89
  }
}
```

**cURL Example**:
```bash
curl http://localhost:8000/api/v1/mitre/actor-profile/APT28 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### GET /api/v1/mitre/mitigation-priority

**Capability**: Mitigation Prioritization
**Complexity**: Intermediate (3 hops)
**Purpose**: Find mitigations with broadest coverage against active threats

**Query Parameters**:
- `active_only` (optional): Filter for active actors (default: true)
- `min_actor_coverage` (optional): Minimum actors covered (default: 5)
- `limit` (optional): Results limit (default: 20)

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": [
    {
      "mitigation_id": "M1047",
      "name": "Audit",
      "description": "Perform audits or scans of systems...",
      "actors_covered": 234,
      "techniques_covered": 87,
      "implementation_cost": "medium",
      "effectiveness": "significant",
      "roi_score": 9.2
    }
  ],
  "metadata": {
    "query_time_ms": 156
  }
}
```

---

### GET /api/v1/mitre/software-capabilities/:software_name

**Capability**: Software Capability Analysis
**Complexity**: Simple (2 hops)
**Purpose**: Analyze malware capabilities and available mitigations

**Path Parameters**:
- `software_name` (required): Software name (e.g., "Mimikatz", "Cobalt Strike")

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "software_id": "S0002",
    "name": "Mimikatz",
    "type": "tool",
    "platforms": ["Windows"],
    "technique_count": 12,
    "techniques": [
      {
        "id": "T1003",
        "name": "OS Credential Dumping",
        "tactic": ["Credential Access"],
        "mitigation_count": 3,
        "available_mitigations": [
          {"id": "M1027", "name": "Password Policies"},
          {"id": "M1043", "name": "Credential Access Protection"}
        ]
      }
    ]
  },
  "metadata": {
    "query_time_ms": 45
  }
}
```

---

### GET /api/v1/mitre/cve-exploitation

**Capability**: CVE Exploitation Chains
**Complexity**: Advanced (4 hops)
**Purpose**: Find CVEs exploited by multiple APT groups

**Query Parameters**:
- `min_cvss_score` (optional): Minimum CVSS score (default: 7.0)
- `min_apt_count` (optional): Minimum APT groups (default: 2)
- `sophistication` (optional): Actor sophistication filter (default: "advanced")
- `limit` (optional): Results limit (default: 20)

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": [
    {
      "cve_id": "CVE-2021-44228",
      "cvss_score": 10.0,
      "apt_count": 15,
      "exploiting_actors": ["APT28", "APT29", "Lazarus Group"],
      "techniques_used": ["T1190: Exploit Public-Facing Application"],
      "exploit_available": true,
      "exploited_in_wild": true,
      "threat_level": "critical"
    }
  ],
  "metadata": {
    "query_time_ms": 567
  }
}
```

---

### GET /api/v1/mitre/platform-threats/:platform

**Capability**: Platform-Specific Threats
**Complexity**: Intermediate (3 hops)
**Purpose**: Analyze threats targeting specific platform

**Path Parameters**:
- `platform` (required): Platform name (e.g., "Windows", "Linux", "macOS")

**Query Parameters**:
- `active_only` (optional): Filter for active actors (default: true)
- `limit` (optional): Results limit (default: 25)

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": [
    {
      "technique_id": "T1003",
      "name": "OS Credential Dumping",
      "tactic": ["Credential Access"],
      "actor_count": 89,
      "top_actors": ["APT28", "APT29", "Lazarus Group"]
    }
  ],
  "metadata": {
    "query_time_ms": 198,
    "platform": "Windows"
  }
}
```

---

### POST /api/v1/mitre/threat-inference

**Capability**: Probabilistic Threat Inference
**Complexity**: Advanced (4-5 hops)
**Purpose**: Predict likely next techniques based on observed TTPs

**Request Body**:
```json
{
  "observed_technique_id": "T1566",
  "top_n": 15
}
```

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": [
    {
      "technique_id": "T1059",
      "name": "Command and Scripting Interpreter",
      "tactic": ["Execution"],
      "likelihood_score": 234,
      "probability_percentage": 39.86,
      "confidence": "high",
      "recommended_detections": [
        "PowerShell logging",
        "Command line monitoring"
      ]
    }
  ],
  "metadata": {
    "observed_technique": "T1566: Phishing",
    "query_time_ms": 423
  }
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/v1/mitre/threat-inference \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "observed_technique_id": "T1566",
    "top_n": 15
  }'
```

---

## Authentication Endpoints

### POST /api/v1/auth/token

**Purpose**: Obtain JWT access token for API authentication

**Request**:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "refresh_token_string",
  "user_id": "user_123",
  "tier": "standard"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

---

### POST /api/v1/auth/refresh

**Purpose**: Refresh expired access token

**Request**:
```json
{
  "refresh_token": "refresh_token_string"
}
```

**Response**:
```json
{
  "access_token": "new_access_token",
  "expires_in": 3600
}
```

---

## Legacy Authentication Endpoints

### POST /api/auth/register
**Purpose**: Register new user account (Legacy)

**Request**:
```typescript
{
  email: string
  password: string
  name?: string
}
```

**Response**:
```typescript
{
  success: true,
  data: {
    userId: string
    email: string
    token: string
  }
}
```

### POST /api/auth/login
**Purpose**: Authenticate user and get JWT token

**Request**:
```typescript
{
  email: string
  password: string
}
```

**Response**:
```typescript
{
  success: true,
  data: {
    token: string
    userId: string
    expiresAt: string
  }
}
```

### POST /api/auth/refresh
**Purpose**: Refresh JWT token

**Request**:
```typescript
{
  refreshToken: string
}
```

## Document Management Endpoints

### POST /api/documents/upload
**Purpose**: Upload document for processing

**Request** (multipart/form-data):
```typescript
{
  file: File
  metadata?: {
    title?: string
    description?: string
    tags?: string[]
  }
}
```

**Response**:
```typescript
{
  success: true,
  data: {
    documentId: string
    filename: string
    size: number
    status: 'uploaded'
  }
}
```

### GET /api/documents
**Purpose**: List user's documents

**Query Parameters**:
```typescript
{
  page?: number
  limit?: number
  status?: 'uploaded' | 'processing' | 'completed' | 'failed'
  sortBy?: 'created_at' | 'filename'
  order?: 'asc' | 'desc'
}
```

**Response**:
```typescript
{
  success: true,
  data: {
    documents: Document[]
    total: number
    page: number
    limit: number
  }
}
```

### GET /api/documents/:documentId
**Purpose**: Get document details

**Response**:
```typescript
{
  success: true,
  data: {
    id: string
    filename: string
    fileType: string
    size: number
    status: string
    createdAt: string
    processedAt?: string
    entityCount?: number
    relationshipCount?: number
  }
}
```

### DELETE /api/documents/:documentId
**Purpose**: Delete document and associated data

**Response**:
```typescript
{
  success: true,
  data: {
    deleted: true
  }
}
```

## Entity Endpoints

### POST /api/entities/extract
**Purpose**: Extract entities from document

**Request**:
```typescript
{
  documentId: string
  entityTypes?: string[]
  confidenceThreshold?: number
}
```

**Response**:
```typescript
{
  success: true,
  data: {
    jobId: string
    status: 'queued'
  }
}
```

### GET /api/entities
**Purpose**: Search entities

**Query Parameters**:
```typescript
{
  query?: string
  type?: string
  documentId?: string
  limit?: number
  offset?: number
}
```

**Response**:
```typescript
{
  success: true,
  data: {
    entities: Array<{
      id: string
      name: string
      type: string
      confidence: number
      documentIds: string[]
      attributes: object
    }>
    total: number
  }
}
```

### GET /api/entities/:entityId
**Purpose**: Get entity details

**Response**:
```typescript
{
  success: true,
  data: {
    id: string
    name: string
    type: string
    attributes: object
    relationships: Array<{
      type: string
      targetEntity: Entity
      confidence: number
    }>
    documents: string[]
    createdAt: string
  }
}
```

## Relationship Endpoints

### POST /api/relationships/extract
**Purpose**: Extract relationships from document

**Request**:
```typescript
{
  documentId: string
  relationshipTypes?: string[]
  strategy?: 'pattern' | 'ml' | 'hybrid'
  confidenceThreshold?: number
}
```

**Response**:
```typescript
{
  success: true,
  data: {
    jobId: string
    status: 'queued'
  }
}
```

### GET /api/relationships
**Purpose**: Query relationships

**Query Parameters**:
```typescript
{
  sourceEntityId?: string
  targetEntityId?: string
  type?: string
  documentId?: string
  minConfidence?: number
  limit?: number
}
```

**Response**:
```typescript
{
  success: true,
  data: {
    relationships: Array<{
      id: string
      type: string
      sourceEntity: Entity
      targetEntity: Entity
      confidence: number
      attributes: object
    }>
    total: number
  }
}
```

## Knowledge Graph Endpoints

### GET /api/graph/query
**Purpose**: Execute Cypher query on knowledge graph

**Query Parameters**:
```typescript
{
  query: string
  parameters?: object
  limit?: number
}
```

**Response**:
```typescript
{
  success: true,
  data: {
    results: any[]
    executionTime: number
  }
}
```

### GET /api/graph/explore
**Purpose**: Explore graph from starting entity

**Query Parameters**:
```typescript
{
  entityId: string
  depth?: number
  relationshipTypes?: string[]
  entityTypes?: string[]
}
```

**Response**:
```typescript
{
  success: true,
  data: {
    nodes: Entity[]
    edges: Relationship[]
  }
}
```

### GET /api/graph/path
**Purpose**: Find shortest path between entities

**Query Parameters**:
```typescript
{
  sourceId: string
  targetId: string
  maxDepth?: number
  relationshipTypes?: string[]
}
```

## Semantic Search Endpoints

### POST /api/search/semantic
**Purpose**: Semantic search using embeddings

**Request**:
```typescript
{
  query: string
  type?: 'entity' | 'document'
  filters?: {
    entityType?: string
    documentId?: string
  }
  limit?: number
}
```

**Response**:
```typescript
{
  success: true,
  data: {
    results: Array<{
      id: string
      score: number
      entity?: Entity
      document?: Document
    }>
  }
}
```

## Job Management Endpoints

### GET /api/jobs/:jobId
**Purpose**: Get job status

**Response**:
```typescript
{
  success: true,
  data: {
    id: string
    type: string
    status: 'pending' | 'processing' | 'completed' | 'failed'
    progress?: number
    startedAt?: string
    completedAt?: string
    error?: string
  }
}
```

### GET /api/jobs
**Purpose**: List jobs for document

**Query Parameters**:
```typescript
{
  documentId?: string
  status?: string
  type?: string
  limit?: number
}
```

## Temporal Endpoints

### GET /api/temporal/entity-history/:entityId
**Purpose**: Get entity version history

**Response**:
```typescript
{
  success: true,
  data: {
    versions: Array<{
      version: number
      validFrom: string
      validTo: string
      attributes: object
      changes: object
    }>
  }
}
```

### POST /api/temporal/snapshot
**Purpose**: Create graph snapshot

**Request**:
```typescript
{
  name?: string
  description?: string
}
```

### GET /api/temporal/query
**Purpose**: Point-in-time query

**Query Parameters**:
```typescript
{
  timestamp: string
  query: string
}
```

## Analytics Endpoints

### GET /api/analytics/statistics
**Purpose**: Get system statistics

**Response**:
```typescript
{
  success: true,
  data: {
    documentCount: number
    entityCount: number
    relationshipCount: number
    entityTypeDistribution: object
    relationshipTypeDistribution: object
  }
}
```

### GET /api/analytics/trends
**Purpose**: Get temporal trends

**Query Parameters**:
```typescript
{
  metric: string
  startDate: string
  endDate: string
  interval: 'hour' | 'day' | 'week' | 'month'
}
```

## Webhook Endpoints

### POST /api/webhooks/register
**Purpose**: Register webhook for events

**Request**:
```typescript
{
  url: string
  events: string[]
  secret?: string
}
```

### GET /api/webhooks
**Purpose**: List registered webhooks

### DELETE /api/webhooks/:webhookId
**Purpose**: Delete webhook

## Error Codes

```typescript
enum ErrorCode {
  UNAUTHORIZED = 'UNAUTHORIZED',
  FORBIDDEN = 'FORBIDDEN',
  NOT_FOUND = 'NOT_FOUND',
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  PROCESSING_ERROR = 'PROCESSING_ERROR',
  RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED',
  INTERNAL_ERROR = 'INTERNAL_ERROR'
}
```

## Rate Limiting

```
Rate Limit: 100 requests per minute per user
Headers:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 87
  X-RateLimit-Reset: 1699876543
```

---

*API Reference Documentation | Comprehensive Endpoint Guide*
