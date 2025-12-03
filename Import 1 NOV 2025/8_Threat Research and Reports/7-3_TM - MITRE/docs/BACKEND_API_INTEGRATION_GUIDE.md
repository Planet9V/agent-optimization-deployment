# Backend API Integration Guide for Frontend Team

**Document Version:** 1.0.0
**Last Updated:** 2025-11-08
**Target Audience:** Frontend UI Developers (Next.js/React)
**Authentication:** Compatible with Clerk Auth (DO NOT MODIFY)

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [V9 NER Service Endpoints](#v9-ner-service-endpoints)
4. [8 Key Questions API Endpoints](#8-key-questions-api-endpoints)
5. [Neo4j Query Integration](#neo4j-query-integration)
6. [Frontend Integration Examples](#frontend-integration-examples)
7. [Authentication Flow](#authentication-flow)
8. [Error Handling](#error-handling)
9. [Rate Limiting](#rate-limiting)
10. [Testing](#testing)

---

## Overview

### Backend Architecture

```
┌─────────────────┐
│   Frontend      │
│   (Next.js)     │ ← Clerk Auth (DO NOT MODIFY)
│   Port: 3000    │
└────────┬────────┘
         │ HTTP/REST
         ↓
┌─────────────────┐
│  Backend API    │
│  (Express/     │
│   FastAPI)      │
│  Port: 8000     │
└────────┬────────┘
         │
    ┌────┴────┬──────────────┐
    ↓         ↓              ↓
┌────────┐ ┌─────────┐ ┌──────────┐
│ V9 NER │ │ Neo4j   │ │ Qdrant   │
│ Model  │ │ bolt:   │ │ Vector   │
│ spaCy  │ │ 7687    │ │ 6333     │
└────────┘ └─────────┘ └──────────┘
```

### Key Components

- **V9 NER Service**: Entity extraction from text (16 entity types)
- **Neo4j Graph DB**: Graph queries for 8 key questions
- **Qdrant Vector DB**: Semantic search and embeddings
- **Clerk Auth Integration**: Frontend authentication (already configured)

### V9 Model Specifications

- **F1 Score**: 99.00% (Target: 96.0%)
- **Precision**: 98.03%
- **Recall**: 100.00% (Perfect - no false negatives)
- **Entity Types**: 16 (Infrastructure + Cybersecurity + MITRE)
- **Training Examples**: 1,718
- **Model Path**: `/models/ner_v9_comprehensive/`

---

## V9 NER Service Endpoints

### POST /api/v9/ner/extract

Extract entities from text using V9 comprehensive model.

**Request:**
```json
{
  "text": "CVE-2024-1234 affects Siemens S7-1200 PLCs running Modbus protocol. APT28 exploits T1190 vulnerability.",
  "entity_types": ["VULNERABILITY", "VENDOR", "EQUIPMENT", "PROTOCOL", "ATTACK_TECHNIQUE", "THREAT_ACTOR"],
  "confidence_threshold": 0.8,
  "return_offsets": true
}
```

**Request Parameters:**
- `text` (required): Text to analyze
- `entity_types` (optional): Filter specific entity types. Default: all 16 types
- `confidence_threshold` (optional): Minimum confidence (0.0-1.0). Default: 0.8
- `return_offsets` (optional): Include character offsets. Default: true

**Response:**
```json
{
  "success": true,
  "entities": [
    {
      "text": "CVE-2024-1234",
      "label": "VULNERABILITY",
      "start": 0,
      "end": 13,
      "confidence": 0.99
    },
    {
      "text": "Siemens",
      "label": "VENDOR",
      "start": 23,
      "end": 30,
      "confidence": 0.97
    },
    {
      "text": "S7-1200 PLCs",
      "label": "EQUIPMENT",
      "start": 31,
      "end": 43,
      "confidence": 0.98
    },
    {
      "text": "Modbus",
      "label": "PROTOCOL",
      "start": 52,
      "end": 58,
      "confidence": 0.96
    },
    {
      "text": "APT28",
      "label": "THREAT_ACTOR",
      "start": 70,
      "end": 75,
      "confidence": 0.99
    },
    {
      "text": "T1190",
      "label": "ATTACK_TECHNIQUE",
      "start": 85,
      "end": 90,
      "confidence": 0.98
    }
  ],
  "metadata": {
    "model_version": "v9",
    "f1_score": 0.99,
    "processing_time_ms": 23,
    "entity_count": 6,
    "text_length": 91
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Invalid entity type specified",
  "code": "INVALID_ENTITY_TYPE",
  "valid_types": ["VENDOR", "EQUIPMENT", ...]
}
```

---

### GET /api/v9/ner/entity-types

Get list of all supported entity types with descriptions.

**Response:**
```json
{
  "success": true,
  "entity_types": {
    "infrastructure": [
      {
        "label": "VENDOR",
        "description": "Equipment manufacturers (e.g., Siemens, Rockwell, Schneider)",
        "examples": ["Siemens", "Rockwell Automation", "Schneider Electric"]
      },
      {
        "label": "EQUIPMENT",
        "description": "Industrial devices (PLCs, HMIs, RTUs, SCADA systems)",
        "examples": ["S7-1200 PLC", "HMI Panel", "RTU Controller"]
      },
      {
        "label": "PROTOCOL",
        "description": "Communication protocols",
        "examples": ["Modbus", "BACnet", "DNP3", "OPC UA"]
      }
      // ... 5 more infrastructure types
    ],
    "cybersecurity": [
      {
        "label": "VULNERABILITY",
        "description": "Security weaknesses (CVE references)",
        "examples": ["CVE-2024-1234", "CVE-2023-5678"]
      },
      {
        "label": "CWE",
        "description": "Common Weakness Enumeration",
        "examples": ["CWE-79", "CWE-89"]
      }
      // ... 3 more cybersecurity types
    ],
    "mitre_attack": [
      {
        "label": "ATTACK_TECHNIQUE",
        "description": "MITRE ATT&CK techniques (T-codes)",
        "examples": ["T1190", "T1003", "T1078"]
      },
      {
        "label": "THREAT_ACTOR",
        "description": "APT groups and threat actors",
        "examples": ["APT28", "APT29", "Lazarus Group"]
      }
      // ... 3 more MITRE types
    ]
  },
  "total_count": 16
}
```

---

### POST /api/v9/ner/batch

Batch process multiple texts for entity extraction.

**Request:**
```json
{
  "texts": [
    "CVE-2024-1234 affects Siemens equipment",
    "APT28 uses Mimikatz for credential dumping",
    "Industrial protocol Modbus TCP/IP vulnerability"
  ],
  "entity_types": ["VULNERABILITY", "VENDOR", "THREAT_ACTOR"],
  "confidence_threshold": 0.8
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "text_index": 0,
      "entities": [/* entities from text 0 */],
      "processing_time_ms": 15
    },
    {
      "text_index": 1,
      "entities": [/* entities from text 1 */],
      "processing_time_ms": 18
    },
    {
      "text_index": 2,
      "entities": [/* entities from text 2 */],
      "processing_time_ms": 12
    }
  ],
  "metadata": {
    "total_texts": 3,
    "total_entities": 8,
    "total_time_ms": 45
  }
}
```

---

## 8 Key Questions API Endpoints

### Question 1: CVE Equipment Impact

**Endpoint:** `POST /api/questions/1/cve-impact`

**Question:** "Does this CVE impact my equipment?"

**Request:**
```json
{
  "cve_id": "CVE-2024-1234",
  "facility_id": "FAC-001",
  "vendor_filter": "Siemens",
  "include_remediation": true
}
```

**Response:**
```json
{
  "success": true,
  "question_id": 1,
  "impacted": true,
  "equipment_count": 12,
  "severity": "HIGH",
  "equipment_list": [
    {
      "equipment_id": "PLC-001",
      "name": "Siemens S7-1200",
      "location": "Building A, Floor 2",
      "asset_tag": "ASSET-12345",
      "vulnerability_severity": "HIGH",
      "cvss_score": 9.8,
      "remediation": "Apply patch v2.1.3",
      "patch_available": true
    },
    // ... more equipment
  ],
  "v9_entities_extracted": {
    "CVE": ["CVE-2024-1234"],
    "VENDOR": ["Siemens"],
    "EQUIPMENT": ["S7-1200"]
  },
  "cypher_query_used": "MATCH (cve:CVE {id: $cveId})-[:EXPLOITS]->(vuln:Vulnerability)<-[:HAS_VULNERABILITY]-(equip:Equipment) WHERE equip.facility_id = $facilityId RETURN equip, vuln"
}
```

---

### Question 2: Attack Path Detection

**Endpoint:** `POST /api/questions/2/attack-path`

**Question:** "Is there an attack path to vulnerability?"

**Request:**
```json
{
  "vulnerability_id": "CVE-2024-1234",
  "starting_point": "external_network",
  "max_hops": 5
}
```

**Response:**
```json
{
  "success": true,
  "question_id": 2,
  "paths_found": true,
  "path_count": 3,
  "attack_paths": [
    {
      "path_id": 1,
      "hop_count": 3,
      "severity": "HIGH",
      "path_nodes": [
        {"type": "ThreatActor", "name": "APT28"},
        {"type": "AttackTechnique", "id": "T1190"},
        {"type": "Vulnerability", "id": "CVE-2024-1234"},
        {"type": "Equipment", "name": "PLC-001"}
      ],
      "mitigations_available": [
        {"id": "M1018", "name": "User Account Management"},
        {"id": "M1051", "name": "Update Software"}
      ]
    }
    // ... more paths
  ]
}
```

---

### Question 3: New CVE Facility Impact

**Endpoint:** `POST /api/questions/3/new-cve-facility-impact`

**Question:** "Does this new CVE released today impact any equipment in my facility?"

**Request:**
```json
{
  "cve_id": "CVE-2024-5678",
  "facility_id": "FAC-001",
  "release_date": "2024-11-08",
  "check_sbom": true
}
```

**Response:**
```json
{
  "success": true,
  "question_id": 3,
  "cve_release_date": "2024-11-08",
  "facility_impacted": true,
  "sbom_matches": 5,
  "equipment_affected": [
    {
      "equipment_id": "HMI-003",
      "sbom_component": "Apache Struts 2.5.22",
      "vulnerable_version": true,
      "recommended_version": "2.5.30"
    }
  ]
}
```

---

### Question 4: Threat Actor Pathway

**Endpoint:** `POST /api/questions/4/threat-actor-pathway`

**Question:** "Is there a pathway for a threat actor to get to the vulnerability to exploit it?"

**Request:**
```json
{
  "threat_actor": "APT28",
  "vulnerability_id": "CVE-2024-1234",
  "facility_id": "FAC-001"
}
```

**Response:**
```json
{
  "success": true,
  "question_id": 4,
  "pathways_exist": true,
  "threat_actor": "APT28",
  "known_techniques": ["T1190", "T1003", "T1078"],
  "attack_chains": [
    {
      "chain_id": 1,
      "steps": [
        {"step": 1, "technique": "T1190", "description": "Exploit Public-Facing Application"},
        {"step": 2, "technique": "T1003", "description": "Credential Dumping"},
        {"step": 3, "target": "CVE-2024-1234", "equipment": "PLC-001"}
      ],
      "probability": "HIGH",
      "mitigations": ["M1018", "M1050", "M1051"]
    }
  ]
}
```

---

### Question 5: Combined CVE + Threat Actor

**Endpoint:** `POST /api/questions/5/cve-threat-combined`

**Question:** "For this CVE released today, is there a pathway for threat actor to get to vulnerability?"

**Request:**
```json
{
  "cve_id": "CVE-2024-5678",
  "threat_actor": "APT29",
  "facility_id": "FAC-001",
  "release_date": "2024-11-08"
}
```

**Response:**
```json
{
  "success": true,
  "question_id": 5,
  "cve_age_days": 0,
  "threat_actor_known_interest": true,
  "exploit_available": false,
  "pathways_exist": true,
  "risk_level": "CRITICAL",
  "recommended_actions": [
    "Immediate patch deployment",
    "Enhanced monitoring for APT29 indicators",
    "Network segmentation review"
  ]
}
```

---

### Question 6: Equipment Type Count

**Endpoint:** `POST /api/questions/6/equipment-count`

**Question:** "How many pieces of a type of equipment do I have?"

**Request:**
```json
{
  "equipment_type": "PLC",
  "vendor": "Siemens",
  "facility_id": "FAC-001"
}
```

**Response:**
```json
{
  "success": true,
  "question_id": 6,
  "equipment_type": "PLC",
  "vendor": "Siemens",
  "total_count": 47,
  "breakdown_by_model": {
    "S7-1200": 23,
    "S7-1500": 18,
    "S7-300": 6
  },
  "breakdown_by_location": {
    "Building A": 20,
    "Building B": 15,
    "Building C": 12
  }
}
```

---

### Question 7: Application/OS Detection

**Endpoint:** `POST /api/questions/7/app-os-detection`

**Question:** "Do I have a specific application or operating system?"

**Request:**
```json
{
  "search_type": "application",
  "search_term": "Apache Struts",
  "version": "2.5.22",
  "facility_id": "FAC-001"
}
```

**Response:**
```json
{
  "success": true,
  "question_id": 7,
  "found": true,
  "instance_count": 8,
  "instances": [
    {
      "asset_id": "SRV-001",
      "version": "2.5.22",
      "location": "Server Room A",
      "vulnerable": true,
      "cves_affecting": ["CVE-2024-1234", "CVE-2023-5678"]
    }
  ]
}
```

---

### Question 8: Asset Location Query

**Endpoint:** `POST /api/questions/8/asset-location`

**Question:** "Tell me the location (on what asset) is a specific application, vulnerability, OS, or library?"

**Request:**
```json
{
  "query_type": "application",
  "identifier": "OpenSSL 1.0.2",
  "facility_id": "FAC-001"
}
```

**Response:**
```json
{
  "success": true,
  "question_id": 8,
  "found": true,
  "assets": [
    {
      "asset_id": "SRV-003",
      "asset_name": "Production Server 3",
      "location": "Building B, Server Room 2, Rack 5",
      "component": "OpenSSL 1.0.2",
      "installation_date": "2022-03-15",
      "last_updated": "2023-06-20",
      "vulnerabilities": ["CVE-2022-0778"]
    }
  ]
}
```

---

## Neo4j Query Integration

### Connection Configuration

**Connection URI:** `bolt://localhost:7687`
**Database:** `neo4j`
**Authentication:** Neo4j native auth (isolated from Clerk)

**From Frontend:**
```typescript
// Backend handles Neo4j connection
// Frontend only needs to call REST endpoints
const response = await fetch('/api/questions/1/cve-impact', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${clerkToken}`, // Clerk auth for backend
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ cve_id: 'CVE-2024-1234' })
});
```

### Graph Schema Overview

**Node Types:**
- `Equipment` - Industrial devices
- `Vulnerability` - Security weaknesses
- `CVE` - CVE database entries
- `AttackTechnique` - MITRE techniques
- `ThreatActor` - APT groups
- `Mitigation` - Security controls
- `Software` - Applications and tools

**Relationship Types:**
- `HAS_VULNERABILITY`
- `EXPLOITS`
- `USES`
- `MITIGATES`
- `TARGETS`

---

## Frontend Integration Examples

### React/Next.js - Entity Extraction

```typescript
// components/EntityExtractor.tsx
import { useState } from 'react';
import { useAuth } from '@clerk/nextjs';

interface Entity {
  text: string;
  label: string;
  start: number;
  end: number;
  confidence: number;
}

export function EntityExtractor() {
  const { getToken } = useAuth();
  const [text, setText] = useState('');
  const [entities, setEntities] = useState<Entity[]>([]);
  const [loading, setLoading] = useState(false);

  const extractEntities = async () => {
    setLoading(true);
    try {
      const token = await getToken();
      const response = await fetch('/api/v9/ner/extract', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          text,
          confidence_threshold: 0.8
        })
      });

      const data = await response.json();
      if (data.success) {
        setEntities(data.entities);
      }
    } catch (error) {
      console.error('Entity extraction failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to analyze..."
      />
      <button onClick={extractEntities} disabled={loading}>
        {loading ? 'Extracting...' : 'Extract Entities'}
      </button>

      <div className="entities">
        {entities.map((entity, idx) => (
          <span
            key={idx}
            className={`entity entity-${entity.label.toLowerCase()}`}
          >
            {entity.text}
            <span className="confidence">
              {(entity.confidence * 100).toFixed(1)}%
            </span>
          </span>
        ))}
      </div>
    </div>
  );
}
```

### Question Execution Example

```typescript
// utils/questionAPI.ts
import { useAuth } from '@clerk/nextjs';

export async function executeCVEImpactQuery(cveId: string, facilityId?: string) {
  const { getToken } = useAuth();
  const token = await getToken();

  const response = await fetch('/api/questions/1/cve-impact', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      cve_id: cveId,
      facility_id: facilityId,
      include_remediation: true
    })
  });

  if (!response.ok) {
    throw new Error(`Query failed: ${response.statusText}`);
  }

  return await response.json();
}

// Usage in component
const result = await executeCVEImpactQuery('CVE-2024-1234', 'FAC-001');
console.log(`${result.equipment_count} devices affected`);
```

---

## Authentication Flow

### Clerk Integration (DO NOT MODIFY)

```typescript
// This is ALREADY CONFIGURED - Do not change
// Frontend uses Clerk for user authentication
// Backend validates Clerk JWT tokens

// Frontend request includes Clerk token
const token = await getToken();
fetch('/api/endpoint', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

// Backend validates token (already implemented)
// No changes needed to Clerk configuration
```

---

## Error Handling

### Error Response Format

```json
{
  "success": false,
  "error": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "specific_field_name",
    "reason": "Detailed explanation"
  },
  "timestamp": "2024-11-08T10:30:00Z"
}
```

### Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `INVALID_CVE` | CVE ID format invalid | 400 |
| `NOT_FOUND` | Resource not found | 404 |
| `UNAUTHORIZED` | Invalid or missing auth token | 401 |
| `RATE_LIMIT` | Too many requests | 429 |
| `NER_TIMEOUT` | NER processing timeout | 504 |
| `DB_ERROR` | Database connection error | 500 |

---

## Rate Limiting

**Default Limits:**
- NER extraction: 100 requests/minute per user
- Question queries: 50 requests/minute per user
- Batch processing: 10 requests/minute per user

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1699459200
```

---

## Testing

### cURL Examples

**Test NER Extraction:**
```bash
curl -X POST http://localhost:8000/api/v9/ner/extract \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_CLERK_TOKEN" \
  -d '{
    "text": "CVE-2024-1234 affects Siemens S7-1200 PLCs",
    "confidence_threshold": 0.8
  }'
```

**Test Question 1:**
```bash
curl -X POST http://localhost:8000/api/questions/1/cve-impact \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_CLERK_TOKEN" \
  -d '{
    "cve_id": "CVE-2024-1234",
    "facility_id": "FAC-001"
  }'
```

### Postman Collection

[Link to Postman collection with all endpoints]

---

## Additional Resources

- **V9 Entity Types Reference:** `/docs/V9_ENTITY_TYPES_REFERENCE.md`
- **8 Key Questions Detailed Guide:** `/docs/8_KEY_QUESTIONS_V9_MAPPING.md`
- **Neo4j Cypher Query Examples:** `/docs/AEON_CAPABILITY_QUERY_PATTERNS.md`
- **Phase 4 Roadmap:** `/docs/PHASE_4_PLANNING.md`

---

**Document Status:** ✅ PRODUCTION READY
**Last Review:** 2025-11-08
**Version:** 1.0.0
**Maintained By:** Backend API Team
**Frontend Contact:** UI Development Team (Clerk Auth - Protected)
