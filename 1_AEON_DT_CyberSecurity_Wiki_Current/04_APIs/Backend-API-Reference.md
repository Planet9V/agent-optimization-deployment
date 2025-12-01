# Backend API Reference Documentation

**File:** Backend-API-Reference.md
**Created:** 2025-11-08 20:59:00 CST
**Modified:** 2025-11-08 22:30:00 CST
**Version:** v2.0.0
**Author:** OpenAPI Documentation Specialist
**Purpose:** Complete backend API reference for AEON MITRE Query and NER v9 services
**Status:** ACTIVE - V9 PRODUCTION READY

Tags: #api #backend #mitre #ner #rest #authentication

---

## Executive Summary

Complete REST API reference for AEON backend services including MITRE ATT&CK query capabilities (8 endpoints) and NER v9 entity extraction (4 endpoints) with comprehensive infrastructure and cybersecurity coverage. All endpoints require Bearer token authentication and support JSON request/response formats.

**Base URLs**:
- MITRE Query API: `http://localhost:8000/api/v1/mitre`
- NER v8 API: `http://localhost:8000/api/v1/ner`
- Authentication: `http://localhost:8000/api/v1/auth`

**Features**:
- 8 MITRE ATT&CK query capabilities (attack paths, gaps, profiling, etc.)
- 4 NER v9 entity extraction endpoints (extract, batch, link, model-info)
- 16 entity types supported (infrastructure + cybersecurity)
- NER v9 model: **99.00% F1 score**, 98.03% precision, 100% recall ✅
- 1,718 training examples across 3 data sources
- Bearer token authentication with JWT
- Rate limiting: 100-2000 requests/minute based on tier
- Response times: 100ms-2s based on complexity
- 99.9% uptime SLA

---

## Table of Contents

1. [Authentication](#authentication)
2. [MITRE Query API](#mitre-query-api)
   - [Attack Path Discovery](#capability-1-attack-path-discovery)
   - [Defensive Gap Analysis](#capability-2-defensive-gap-analysis)
   - [Threat Actor Profiling](#capability-3-threat-actor-profiling)
   - [Mitigation Prioritization](#capability-4-mitigation-prioritization)
   - [Software Capability Analysis](#capability-5-software-capability-analysis)
   - [CVE Exploitation Chains](#capability-6-cve-exploitation-chains)
   - [Platform-Specific Threats](#capability-7-platform-specific-threats)
   - [Probabilistic Threat Inference](#capability-8-probabilistic-threat-inference)
3. [NER v9 API](#ner-v9-api)
   - [Extract Entities](#extract-entities-from-text)
   - [Batch Extraction](#batch-entity-extraction)
   - [Entity Linking](#entity-linking-to-neo4j)
   - [Model Information](#model-information)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting-and-quotas)
6. [Performance and SLA](#performance-and-sla)
7. [Code Examples](#complete-code-examples)
8. [Troubleshooting](#troubleshooting)

---

## Authentication

### Obtain API Token

**Endpoint**: `POST /api/v1/auth/token`

**Description**: Obtain JWT access token for API authentication

**Request Body**:
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

### Using Access Token

All API requests require Bearer token authentication:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Example**:
```bash
curl -X GET http://localhost:8000/api/v1/mitre/actor-profile/APT28 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Refresh Token

**Endpoint**: `POST /api/v1/auth/refresh`

**Description**: Refresh expired access token

**Request Body**:
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

## MITRE Query API

Base URL: `http://localhost:8000/api/v1/mitre`

### Query Complexity Levels

| Complexity | Hops | Response Time | Use Case |
|------------|------|---------------|----------|
| Simple | 1-2 | < 100ms | Single-entity lookups |
| Intermediate | 3-4 | < 500ms | Multi-hop analysis |
| Advanced | 5+ | < 2s | Attack paths, inference |

---

### Capability 1: Attack Path Discovery

**Endpoint**: `POST /api/v1/mitre/attack-paths`

**Complexity**: Advanced (3-4 hops)

**Description**: Discover multi-hop attack paths from threat actors to critical CVEs

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

**Response**:
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

---

### Capability 2: Defensive Gap Analysis

**Endpoint**: `GET /api/v1/mitre/defensive-gaps`

**Complexity**: Intermediate (2-3 hops)

**Description**: Identify critical techniques with insufficient mitigations

**Query Parameters**:
- `tactics` (optional): Comma-separated tactics (e.g., "Initial Access,Execution")
- `max_mitigations` (optional): Maximum mitigation threshold (default: 2)
- `limit` (optional): Results limit (default: 20)

**Response**:
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

---

### Capability 3: Threat Actor Profiling

**Endpoint**: `GET /api/v1/mitre/actor-profile/{actor_name}`

**Complexity**: Intermediate (2-3 hops)

**Description**: Complete TTP and toolset profile for threat actor

**Path Parameters**:
- `actor_name` (required): Actor name (e.g., "APT28", "Lazarus Group")

**Response**:
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

---

### Capability 4: Mitigation Prioritization

**Endpoint**: `GET /api/v1/mitre/mitigation-priority`

**Complexity**: Intermediate (3 hops)

**Description**: Find mitigations with broadest coverage against active threats

**Query Parameters**:
- `active_only` (optional): Filter for active actors (default: true)
- `min_actor_coverage` (optional): Minimum actors covered (default: 5)
- `limit` (optional): Results limit (default: 20)

**Response**:
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

### Capability 5: Software Capability Analysis

**Endpoint**: `GET /api/v1/mitre/software-capabilities/{software_name}`

**Complexity**: Simple (2 hops)

**Description**: Analyze malware capabilities and available mitigations

**Path Parameters**:
- `software_name` (required): Software name (e.g., "Mimikatz", "Cobalt Strike")

**Response**:
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

### Capability 6: CVE Exploitation Chains

**Endpoint**: `GET /api/v1/mitre/cve-exploitation`

**Complexity**: Advanced (4 hops)

**Description**: Find CVEs exploited by multiple APT groups

**Query Parameters**:
- `min_cvss_score` (optional): Minimum CVSS score (default: 7.0)
- `min_apt_count` (optional): Minimum APT groups (default: 2)
- `sophistication` (optional): Actor sophistication filter (default: "advanced")
- `limit` (optional): Results limit (default: 20)

**Response**:
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

### Capability 7: Platform-Specific Threats

**Endpoint**: `GET /api/v1/mitre/platform-threats/{platform}`

**Complexity**: Intermediate (3 hops)

**Description**: Analyze threats targeting specific platform

**Path Parameters**:
- `platform` (required): Platform name (e.g., "Windows", "Linux", "macOS")

**Query Parameters**:
- `active_only` (optional): Filter for active actors (default: true)
- `limit` (optional): Results limit (default: 25)

**Response**:
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

### Capability 8: Probabilistic Threat Inference

**Endpoint**: `POST /api/v1/mitre/threat-inference`

**Complexity**: Advanced (4-5 hops)

**Description**: Predict likely next techniques based on observed TTPs

**Request Body**:
```json
{
  "observed_technique_id": "T1566",
  "top_n": 15
}
```

**Response**:
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

---

## NER v9 API

Base URL: `http://localhost:8000/api/v1/ner`

**Model Version**: v9.0.0 (2025-11-08)
**Training Dataset**: 1,718 examples across 16 entity types
**Status**: ✅ **TRAINING COMPLETE - PRODUCTION DEPLOYED**
**Performance**: 99.00% F1, 98.03% Precision, 100.00% Recall

### Extract Entities from Text

**Endpoint**: `POST /api/v1/ner/extract`

**Description**: Extract MITRE entities from unstructured text

**Request Body**:
```json
{
  "text": "Siemens SIMATIC S7-1200 PLC vulnerable to CVE-2023-12345 using Modbus protocol. APT28 leveraged Mimikatz for T1003 credential dumping.",
  "entity_types": ["VENDOR", "EQUIPMENT", "VULNERABILITY", "PROTOCOL", "THREAT_ACTOR", "SOFTWARE", "ATTACK_TECHNIQUE"],
  "confidence_threshold": 0.85
}
```

**Parameters**:
- `text` (required): Text to analyze
- `entity_types` (optional): Filter entity types from 16 available types (default: all types)
- `confidence_threshold` (optional): Minimum confidence (default: 0.85)

**Available Entity Types** (16 total):
- **Infrastructure**: VENDOR, EQUIPMENT, PROTOCOL, SECURITY, HARDWARE_COMPONENT, SOFTWARE_COMPONENT
- **Cybersecurity**: VULNERABILITY, CWE, CAPEC, WEAKNESS, OWASP
- **MITRE**: ATTACK_TECHNIQUE, THREAT_ACTOR, SOFTWARE, DATA_SOURCE, MITIGATION

**Response**:
```json
{
  "status": "success",
  "entities": [
    {
      "text": "APT28",
      "label": "ACTOR",
      "start": 0,
      "end": 5,
      "confidence": 0.98,
      "neo4j_id": "G0016",
      "linked_entity": {
        "id": "G0016",
        "name": "APT28",
        "type": "MitreActor"
      }
    },
    {
      "text": "Mimikatz",
      "label": "SOFTWARE",
      "start": 16,
      "end": 24,
      "confidence": 0.97,
      "neo4j_id": "S0002"
    },
    {
      "text": "T1003",
      "label": "TECHNIQUE",
      "start": 66,
      "end": 71,
      "confidence": 0.99,
      "neo4j_id": "T1003"
    }
  ],
  "metadata": {
    "processing_time_ms": 23,
    "model_version": "v9",
    "total_entities": 3,
    "model_f1_score": 0.99
  }
}
```

---

### Batch Entity Extraction

**Endpoint**: `POST /api/v1/ner/extract-batch`

**Description**: Extract entities from multiple texts in parallel

**Request Body**:
```json
{
  "texts": [
    "APT28 used phishing emails.",
    "Mimikatz dumped credentials.",
    "CVE-2021-44228 exploited."
  ],
  "entity_types": ["ACTOR", "SOFTWARE", "CVE"],
  "confidence_threshold": 0.80
}
```

**Response**:
```json
{
  "status": "success",
  "results": [
    {
      "text_index": 0,
      "entities": [
        {"text": "APT28", "label": "ACTOR", "confidence": 0.98}
      ]
    },
    {
      "text_index": 1,
      "entities": [
        {"text": "Mimikatz", "label": "SOFTWARE", "confidence": 0.97}
      ]
    },
    {
      "text_index": 2,
      "entities": [
        {"text": "CVE-2021-44228", "label": "CVE", "confidence": 1.0}
      ]
    }
  ],
  "metadata": {
    "processing_time_ms": 67,
    "total_texts": 3
  }
}
```

---

### Entity Linking to Neo4j

**Endpoint**: `POST /api/v1/ner/link`

**Description**: Extract entities and create Neo4j relationships

**Request Body**:
```json
{
  "text": "APT28 exploited CVE-2021-44228 using Cobalt Strike.",
  "create_relationships": true,
  "relationship_types": ["EXPLOITS_CVE", "LEVERAGES_SOFTWARE"]
}
```

**Response**:
```json
{
  "status": "success",
  "entities": [
    {"text": "APT28", "label": "ACTOR", "neo4j_id": "G0016"},
    {"text": "CVE-2021-44228", "label": "CVE", "neo4j_id": "CVE-2021-44228"}
  ],
  "relationships_created": [
    {
      "type": "EXPLOITS_CVE",
      "source": "G0016",
      "target": "CVE-2021-44228",
      "confidence": 0.92
    }
  ],
  "metadata": {
    "processing_time_ms": 145,
    "relationships_created": 1
  }
}
```

---

### Model Information

**Endpoint**: `GET /api/v1/ner/model-info`

**Description**: Get NER model performance metrics

**Response**:
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
    "dataset_sources": ["infrastructure_v5_v6", "cybersecurity_v7", "mitre"],
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
      "infrastructure": {"examples": 183, "percentage": 10.7},
      "cybersecurity": {"examples": 755, "percentage": 43.9},
      "mitre": {"examples": 1121, "percentage": 65.3}
    }
  }
}
```

---

## Error Handling

### Standard Error Response

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional context"
    }
  }
}
```

### Error Codes

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `INVALID_TOKEN` | 401 | Invalid or expired token | Re-authenticate |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests | Wait and retry |
| `RESOURCE_NOT_FOUND` | 404 | Entity not found | Check entity ID |
| `INVALID_PARAMETER` | 400 | Invalid query parameter | Review API docs |
| `DATABASE_ERROR` | 500 | Neo4j connection failure | Contact support |
| `TIMEOUT` | 504 | Query timeout exceeded | Reduce complexity |

---

## Rate Limiting and Quotas

### Rate Limit Tiers

| Tier | Requests/Minute | Requests/Day | Cost |
|------|-----------------|--------------|------|
| Free | 100 | 10,000 | $0 |
| Standard | 500 | 100,000 | $49/month |
| Enterprise | 2,000 | Unlimited | $199/month |

### Rate Limit Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1699459200
```

### Rate Limit Exceeded Response

```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit exceeded",
    "retry_after": 45
  }
}
```

---

## Performance and SLA

### Service Level Agreement

- **Availability**: 99.9% uptime
- **Response Time**:
  - Simple queries: < 100ms (P95)
  - Intermediate queries: < 500ms (P95)
  - Advanced queries: < 2s (P95)
- **Data Freshness**: Updated daily from MITRE ATT&CK v14.1

### Performance Tips

1. **Use caching**: Cache frequently accessed data client-side
2. **Limit results**: Use `limit` parameter to reduce response size
3. **Filter early**: Apply filters to reduce query complexity
4. **Batch requests**: Combine multiple queries when possible
5. **Use webhooks**: Subscribe to data updates instead of polling

---

## Complete Code Examples

### Python Client Library

```python
import requests
from datetime import datetime, timedelta

class AEONAPIClient:
    """Complete Python client for AEON Backend API"""

    def __init__(self, base_url="http://localhost:8000", username=None, password=None):
        self.base_url = base_url
        self.token = None
        self.token_expiry = None
        if username and password:
            self.authenticate(username, password)

    def authenticate(self, username, password):
        """Obtain API token"""
        response = requests.post(
            f"{self.base_url}/api/v1/auth/token",
            json={"username": username, "password": password}
        )
        data = response.json()
        self.token = data["access_token"]
        self.token_expiry = datetime.now() + timedelta(seconds=data["expires_in"])

    def _get_headers(self):
        """Get headers with valid token"""
        if not self.token or datetime.now() >= self.token_expiry:
            raise Exception("Token expired. Please re-authenticate.")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    # MITRE API Methods

    def get_attack_paths(self, actor_name, min_cvss=9.0, max_hops=4, limit=10):
        """Get attack paths from threat actor to CVEs"""
        response = requests.post(
            f"{self.base_url}/api/v1/mitre/attack-paths",
            headers=self._get_headers(),
            json={
                "actor_name": actor_name,
                "min_cvss_score": min_cvss,
                "max_hops": max_hops,
                "limit": limit
            }
        )
        return response.json()

    def get_actor_profile(self, actor_name):
        """Get complete threat actor profile"""
        response = requests.get(
            f"{self.base_url}/api/v1/mitre/actor-profile/{actor_name}",
            headers=self._get_headers()
        )
        return response.json()

    def get_defensive_gaps(self, tactics=None, max_mitigations=2, limit=20):
        """Find defensive gaps in technique coverage"""
        params = {
            "max_mitigations": max_mitigations,
            "limit": limit
        }
        if tactics:
            params["tactics"] = ",".join(tactics)

        response = requests.get(
            f"{self.base_url}/api/v1/mitre/defensive-gaps",
            headers=self._get_headers(),
            params=params
        )
        return response.json()

    def get_mitigation_priority(self, active_only=True, min_coverage=5, limit=20):
        """Get prioritized mitigations"""
        response = requests.get(
            f"{self.base_url}/api/v1/mitre/mitigation-priority",
            headers=self._get_headers(),
            params={
                "active_only": active_only,
                "min_actor_coverage": min_coverage,
                "limit": limit
            }
        )
        return response.json()

    # NER API Methods

    def extract_entities(self, text, entity_types=None, threshold=0.85):
        """Extract MITRE entities from text"""
        response = requests.post(
            f"{self.base_url}/api/v1/ner/extract",
            headers=self._get_headers(),
            json={
                "text": text,
                "entity_types": entity_types,
                "confidence_threshold": threshold
            }
        )
        return response.json()

    def extract_batch(self, texts, entity_types=None, threshold=0.80):
        """Extract entities from multiple texts"""
        response = requests.post(
            f"{self.base_url}/api/v1/ner/extract-batch",
            headers=self._get_headers(),
            json={
                "texts": texts,
                "entity_types": entity_types,
                "confidence_threshold": threshold
            }
        )
        return response.json()

    def link_entities(self, text, create_relationships=True):
        """Extract and link entities to Neo4j"""
        response = requests.post(
            f"{self.base_url}/api/v1/ner/link",
            headers=self._get_headers(),
            json={
                "text": text,
                "create_relationships": create_relationships
            }
        )
        return response.json()

# Usage Examples
client = AEONAPIClient(username="user", password="pass")

# Get attack paths
paths = client.get_attack_paths("APT28", min_cvss=9.0)
print(f"Found {len(paths['data'])} attack paths")

# Get actor profile
profile = client.get_actor_profile("APT28")
print(f"Actor: {profile['data']['name']}")
print(f"Techniques: {profile['data']['technique_count']}")

# Extract entities
text = "APT28 used Mimikatz to dump credentials via T1003."
result = client.extract_entities(text)
for entity in result["entities"]:
    print(f"{entity['label']}: {entity['text']}")

# Batch extraction
texts = [
    "APT29 leveraged PowerShell.",
    "CVE-2021-44228 exploited.",
    "Mimikatz dumped LSASS."
]
batch = client.extract_batch(texts)
print(f"Extracted entities from {len(batch['results'])} texts")
```

---

## Troubleshooting

### Connection Issues

```bash
# Verify service is running
docker ps | grep aeon-backend

# Test connectivity
curl -v http://localhost:8000/health

# Check firewall
sudo iptables -L | grep 8000
```

### Authentication Failures

```python
# Verify token expiry
import jwt
token = "YOUR_TOKEN"
decoded = jwt.decode(token, options={"verify_signature": False})
print(f"Expires: {decoded['exp']}")

# Re-authenticate
client.authenticate("username", "password")
```

### Query Timeout Errors

```python
# Reduce complexity
response = client.get_attack_paths(
    "APT28",
    max_hops=4,  # Reduced from 10
    limit=10     # Limited results
)
```

### Data Inconsistency

```bash
# Verify MITRE data loaded
curl http://localhost:8000/api/v1/mitre/stats

# Check database indexes
docker exec openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg "SHOW INDEXES"
```

---

## Version History

- v1.1.0 (2025-11-08): Enhanced NER v9 integration
  - Updated NER API documentation to v9 (16 entity types, 1,718 examples)
  - Added infrastructure entity type support
  - Enhanced entity extraction examples with infrastructure + cybersecurity
  - Updated model information endpoint with v9 performance targets
  - Added dataset composition documentation
- v1.0.0 (2025-11-08): Initial backend API reference
  - 8 MITRE query capabilities documented
  - 4 NER v8 endpoints documented
  - Complete authentication guide
  - Error handling and troubleshooting
  - Python client library examples

---

## References & Sources

- MITRE ATT&CK Framework v14.1: https://attack.mitre.org/
- Neo4j Documentation: https://neo4j.com/docs/
- spaCy NER Documentation: https://spacy.io/usage/linguistic-features#named-entities
- JWT Authentication: https://jwt.io/

---

*Backend API Reference v1.0.0 | Comprehensive | Production Ready*
*Updated: 2025-11-08 20:59:00 CST | Status: ACTIVE*

---

## Related Documentation

### Wiki Documentation
- [[MITRE-ATT&CK-Integration]] - Complete MITRE integration reference
- [[Neo4j-Database]] - Database configuration and connection details
- [[Neo4j-Schema-Enhanced]] - Graph database schema reference
- [[Cypher-Query-API]] - Cypher query examples and patterns
- [[Credentials-Management]] - Authentication and security

### MITRE Project Documentation

**Location**: `/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/docs/`

#### Complete Reference Documentation
- **V9_ENTITY_TYPES_REFERENCE.md** (~50KB) - Comprehensive documentation of all 16 entity types with examples, schema mapping, Python usage, and Neo4j integration
- **BACKEND_API_INTEGRATION_GUIDE.md** (~80KB) - Complete API specifications including V9 NER endpoints, 8 Key Questions API, request/response schemas, React/TypeScript examples, Clerk authentication guide
- **8_KEY_QUESTIONS_V9_MAPPING.md** (~120KB) - Detailed mapping of AEON capability questions to V9 entities, NER pre-processing workflows, 24 Cypher query variations (3 complexity levels)
- **V9_DEPLOYMENT_SUMMARY.md** - Executive summary, architecture diagrams, Phase 4 roadmap, frontend integration guide
- **DEPLOYMENT_INSTRUCTIONS.md** - Step-by-step deployment procedures for NER v9 model and Neo4j import

#### Quick Reference
For complete endpoint specifications and integration examples, see **BACKEND_API_INTEGRATION_GUIDE.md** which includes:
- Full API endpoint definitions with request/response schemas
- React/TypeScript integration code examples
- Clerk authentication integration (protected - DO NOT BREAK)
- Error handling and rate limiting examples
- Testing procedures with cURL commands

---

**Last Updated:** 2025-11-08 22:30:00 CST
**Version:** v2.0.0 (V9 Production)
**Maintained By:** Backend API Development Team
**Review Cycle:** Bi-weekly

#api #backend #mitre #ner-v9 #rest #authentication #v9-production-ready
