# Query API Documentation - AEON Cyber Digital Twin

**File:** API_QUERY.md
**Created:** 2025-11-25 10:35:00 UTC
**Modified:** 2025-11-25 10:35:00 UTC
**Version:** v1.0.0
**Author:** API Documentation Specialist
**Purpose:** Comprehensive Query API documentation covering custom Cypher queries, advanced analytics, and graph exploration
**Status:** ACTIVE

---

## Executive Summary

Complete reference for Query API endpoints enabling custom Cypher query execution, sector-level analytics, cross-sector dependency analysis, and 20-hop path discovery. Covers request/response schemas, security validation, injection prevention, frontend integration patterns, business value, and practical example queries for attack path discovery and sector dependency mapping.

**Key Capabilities:**
- Custom Cypher query execution with validation
- Sector and industry analytics
- Cross-sector dependency discovery
- Multi-hop path queries (up to 20 hops)
- Graph explorer integration
- Query builder for frontend applications

---

## Architecture Overview

### API Endpoints

| Endpoint | Method | Purpose | Complexity |
|----------|--------|---------|------------|
| `/api/v1/cypher` | POST | Execute custom Cypher queries | Variable |
| `/api/v1/analytics/sectors` | GET | Sector-level analytics and statistics | Simple |
| `/api/v1/analytics/dependencies` | GET | Cross-sector dependency analysis | Intermediate |
| `/api/v1/query/multi-hop` | POST | 20-hop path discovery queries | Advanced |
| `/api/v1/query/builder` | POST | Query builder for frontend | Variable |
| `/api/v1/query/validate` | POST | Query validation without execution | Simple |

### Technology Stack

- **Query Engine**: Neo4j 5.26.0
- **Protocol**: Bolt 4.4 + HTTP REST API
- **Authentication**: JWT Bearer tokens
- **Rate Limiting**: Token-based quotas
- **Response Format**: JSON with graph metadata

---

## 1. POST /api/v1/cypher - Custom Cypher Execution

### Purpose
Execute custom Cypher queries against the knowledge graph with full validation, parameter binding, and result transformation.

### Request Schema

```json
{
  "query": "string (required)",
  "parameters": "object (optional)",
  "mode": "string (optional: 'row' | 'graph' | 'path')",
  "limit": "integer (optional, default: 1000, max: 100000)",
  "timeout": "integer (optional, milliseconds, default: 30000)",
  "explain": "boolean (optional, return query plan instead of results)"
}
```

### Parameters

**query** (string, required)
- Cypher query to execute
- Parameter placeholders: `$paramName`
- Maximum 100,000 characters
- Must pass validation checks (see Security section)

**parameters** (object, optional)
- Key-value pairs for parameter binding
- Supports: strings, numbers, booleans, arrays, objects
- Example: `{"actorName": "APT28", "minCvss": 7.0}`

**mode** (string, optional)
- `row`: Returns data as rows (default)
- `graph`: Returns nodes and relationships for visualization
- `path`: Returns path structures with nodes and relationships

**limit** (integer, optional)
- Maximum results to return
- Default: 1000
- Maximum: 100,000
- Applied AFTER query execution

**timeout** (integer, optional)
- Query timeout in milliseconds
- Default: 30,000 (30 seconds)
- Maximum: 600,000 (10 minutes)
- Raises timeout error if exceeded

**explain** (boolean, optional)
- Return query plan without execution
- Useful for performance analysis
- Default: false

### Response Schema - Success

```json
{
  "status": "success",
  "data": {
    "records": [
      {
        "columns": ["column1", "column2"],
        "row": [value1, value2]
      }
    ],
    "graph": {
      "nodes": [
        {
          "id": "node_id",
          "labels": ["Label1", "Label2"],
          "properties": {
            "property": "value"
          }
        }
      ],
      "relationships": [
        {
          "id": "rel_id",
          "type": "RELATIONSHIP_TYPE",
          "startNodeId": "node_1",
          "endNodeId": "node_2",
          "properties": {}
        }
      ]
    }
  },
  "metadata": {
    "execution_time_ms": 245,
    "records_returned": 50,
    "query_complexity": "intermediate",
    "cached": false,
    "version": "5.26.0"
  }
}
```

### Response Schema - Error

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "line": 5,
      "offset": 12,
      "suggestion": "Did you mean: ..."
    }
  }
}
```

### Error Codes

| Code | Status | Meaning | Solution |
|------|--------|---------|----------|
| `SYNTAX_ERROR` | 400 | Invalid Cypher syntax | Review query syntax |
| `PARAMETER_ERROR` | 400 | Invalid parameter value | Check parameter types |
| `INJECTION_DETECTED` | 400 | Potential query injection | Use parameterized queries |
| `TIMEOUT` | 504 | Query exceeded timeout | Reduce complexity or increase timeout |
| `UNAUTHORIZED` | 401 | Invalid or missing token | Provide valid JWT |
| `FORBIDDEN` | 403 | Insufficient permissions | Contact administrator |
| `RATE_LIMIT` | 429 | Quota exceeded | Wait and retry |
| `SERVER_ERROR` | 500 | Internal server error | Contact support |

### Example Requests

#### Simple Pattern Match

```bash
curl -X POST http://localhost:8000/api/v1/cypher \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "MATCH (e:Entity {type: $entityType}) RETURN e.name, e.severity LIMIT $limit",
    "parameters": {
      "entityType": "vulnerability",
      "limit": 10
    },
    "mode": "row"
  }'
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "records": [
      {
        "columns": ["e.name", "e.severity"],
        "row": ["SQL Injection", "high"]
      },
      {
        "columns": ["e.name", "e.severity"],
        "row": ["XSS", "medium"]
      }
    ]
  },
  "metadata": {
    "execution_time_ms": 45,
    "records_returned": 2,
    "query_complexity": "simple"
  }
}
```

#### Graph Visualization Query

```bash
curl -X POST http://localhost:8000/api/v1/cypher \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "MATCH (center:Entity {id: $nodeId}) OPTIONAL MATCH (center)-[r]-(connected:Entity) RETURN center, collect(r) AS rels, collect(connected) AS neighbors",
    "parameters": {"nodeId": "entity_123"},
    "mode": "graph"
  }'
```

#### Python Client Example

```python
import requests

class QueryAPIClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def execute_cypher(self, query, parameters=None, mode="row", limit=1000):
        """Execute Cypher query"""
        payload = {
            "query": query,
            "parameters": parameters or {},
            "mode": mode,
            "limit": limit
        }

        response = requests.post(
            f"{self.base_url}/api/v1/cypher",
            headers=self.headers,
            json=payload
        )

        if response.status_code == 200:
            return response.json()["data"]["records"]
        else:
            error = response.json()["error"]
            raise Exception(f"{error['code']}: {error['message']}")

# Usage
client = QueryAPIClient("http://localhost:8000", "YOUR_TOKEN")

# Find vulnerabilities
results = client.execute_cypher(
    "MATCH (e:Entity {type: $type}) RETURN e.name, e.severity",
    {"type": "vulnerability"}
)

for record in results:
    print(f"{record['row'][0]}: {record['row'][1]}")
```

---

## 2. GET /api/v1/analytics/sectors - Sector Analytics

### Purpose
Retrieve sector-level statistics, threat distribution, and entity summaries for dashboard and reporting.

### Query Parameters

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `sector` | string | null | - | Filter by specific sector |
| `metrics` | string | "all" | - | Comma-separated: entities, threats, vulns, relationships, avgRisk |
| `include_distribution` | boolean | true | - | Include entity type distribution |
| `include_timeline` | boolean | false | - | Include creation timeline (slower) |
| `days` | integer | 30 | 365 | Days of historical data |

### Response Schema

```json
{
  "status": "success",
  "data": {
    "sectors": [
      {
        "id": "sector_001",
        "name": "Financial Services",
        "entities": {
          "total": 4521,
          "by_type": {
            "vulnerability": 1240,
            "threat": 856,
            "threat_actor": 45,
            "malware": 234,
            "other": 2146
          }
        },
        "relationships": {
          "total": 8934,
          "by_type": {
            "targets": 2341,
            "exploits": 1892,
            "relates_to": 4701
          }
        },
        "threat_metrics": {
          "critical_vulns": 124,
          "active_threats": 45,
          "affected_orgs": 890,
          "avg_cvss_score": 7.2
        },
        "risk_score": 8.5,
        "last_updated": "2025-11-25T10:30:00Z"
      }
    ]
  },
  "metadata": {
    "query_time_ms": 234,
    "sectors_returned": 16,
    "date_range": "2025-10-26 to 2025-11-25"
  }
}
```

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v1/analytics/sectors?sector=Healthcare&metrics=entities,threats,vulns" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Python Example

```python
import requests

def get_sector_analytics(base_url, token, sector=None):
    """Get sector-level analytics"""
    params = {
        "metrics": "entities,threats,vulns",
        "include_distribution": True
    }

    if sector:
        params["sector"] = sector

    response = requests.get(
        f"{base_url}/api/v1/analytics/sectors",
        headers={"Authorization": f"Bearer {token}"},
        params=params
    )

    return response.json()["data"]["sectors"]

# Get all sectors
sectors = get_sector_analytics("http://localhost:8000", "TOKEN")
for sector in sectors:
    print(f"{sector['name']}: {sector['entities']['total']} entities, Risk: {sector['risk_score']}")
```

---

## 3. GET /api/v1/analytics/dependencies - Cross-Sector Dependencies

### Purpose
Discover dependencies and relationships between sectors, threat actors, and technologies.

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source_sector` | string | null | Source sector to analyze |
| `target_sector` | string | null | Target sector dependency |
| `relationship_type` | string | "all" | targets, exploits, depends_on |
| `min_connections` | integer | 1 | Minimum relationship count |
| `include_paths` | boolean | false | Include attack paths |
| `max_depth` | integer | 3 | Maximum relationship depth |

### Response Schema

```json
{
  "status": "success",
  "data": {
    "dependencies": [
      {
        "id": "dep_001",
        "source": {
          "type": "sector",
          "id": "sector_001",
          "name": "Financial Services"
        },
        "target": {
          "type": "sector",
          "id": "sector_002",
          "name": "Technology"
        },
        "relationship_type": "depends_on",
        "connection_count": 1245,
        "threat_flows": [
          {
            "threat": "ransomware",
            "count": 234,
            "severity": "critical"
          }
        ],
        "vulnerability_chains": 45,
        "risk_score": 8.2
      }
    ],
    "graph": {
      "nodes": [],
      "edges": []
    }
  },
  "metadata": {
    "query_time_ms": 567,
    "dependencies_found": 24,
    "depth_analyzed": 3
  }
}
```

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v1/analytics/dependencies?source_sector=Financial&relationship_type=targets&include_paths=true" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 4. POST /api/v1/query/multi-hop - Multi-Hop Path Discovery

### Purpose
Execute path queries with support for up to 20 hops for complex attack path and supply chain analysis.

### Request Schema

```json
{
  "start_node": {
    "type": "string",
    "id": "string",
    "label": "string"
  },
  "end_node": {
    "type": "string",
    "id": "string",
    "label": "string"
  },
  "max_hops": "integer (1-20, default: 4)",
  "relationship_filters": ["string"],
  "relationship_mode": "string ('any' | 'all' | 'sequence')",
  "exclude_paths": ["string"],
  "weight_property": "string (optional)",
  "limit": "integer (default: 10)",
  "include_intermediate": "boolean (default: true)"
}
```

### Parameters

**start_node, end_node** (object, required)
- Define source and destination nodes
- `type`: Entity type (MitreActor, Vulnerability, etc.)
- `id`: Node ID or `name`: Human-readable name
- `label`: Optional label for filtering

**max_hops** (integer, 1-20)
- Maximum relationship depth to explore
- Default: 4
- Higher values = more complex queries

**relationship_filters** (array, optional)
- Include only specific relationship types
- Example: `["USES_TECHNIQUE", "EXPLOITS_CVE"]`

**relationship_mode** (string, optional)
- `any`: Match any relationship type
- `all`: Must traverse all specified types
- `sequence`: Must follow exact sequence

**weight_property** (string, optional)
- Property to use for shortest weighted path
- Example: `"cvss_score"` for vulnerability paths

### Response Schema

```json
{
  "status": "success",
  "data": {
    "paths": [
      {
        "path_id": "path_001",
        "hops": 4,
        "length": 4,
        "nodes": [
          {
            "id": "G0016",
            "type": "MitreActor",
            "properties": {
              "name": "APT28",
              "country": "Russia"
            }
          }
        ],
        "relationships": [
          {
            "type": "USES_TECHNIQUE",
            "properties": {
              "confidence": 0.95
            }
          }
        ],
        "cumulative_risk": 8.7,
        "attack_likelihood": 0.89
      }
    ]
  },
  "metadata": {
    "query_time_ms": 1245,
    "paths_found": 7,
    "max_depth_reached": 4,
    "result_truncated": false
  }
}
```

### Example Requests

#### Attack Path from Actor to CVE

```bash
curl -X POST http://localhost:8000/api/v1/query/multi-hop \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "start_node": {
      "type": "MitreActor",
      "name": "APT28"
    },
    "end_node": {
      "type": "CVE",
      "properties": {
        "cvss_score": {"$gte": 9.0}
      }
    },
    "max_hops": 5,
    "relationship_filters": ["USES_TECHNIQUE", "EXPLOITS_CVE"],
    "limit": 10
  }'
```

#### Supply Chain Dependency Analysis

```bash
curl -X POST http://localhost:8000/api/v1/query/multi-hop \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "start_node": {
      "type": "Organization",
      "name": "Target Organization"
    },
    "end_node": {
      "type": "Vulnerability",
      "properties": {
        "severity": "critical"
      }
    },
    "max_hops": 8,
    "relationship_filters": ["depends_on", "uses_software", "affected_by"],
    "relationship_mode": "sequence"
  }'
```

#### Python Implementation

```python
def discover_attack_paths(client, actor_name, max_hops=5):
    """Discover attack paths from threat actor to critical CVEs"""
    response = client.execute_post(
        "/api/v1/query/multi-hop",
        {
            "start_node": {
                "type": "MitreActor",
                "name": actor_name
            },
            "end_node": {
                "type": "CVE",
                "properties": {"cvss_score": {"$gte": 9.0}}
            },
            "max_hops": max_hops,
            "relationship_filters": ["USES_TECHNIQUE", "EXPLOITS_CVE"],
            "limit": 20
        }
    )

    paths = response["data"]["paths"]
    for path in paths:
        print(f"Attack path: {path['hops']} hops, Risk: {path['cumulative_risk']}")
        for i, node in enumerate(path["nodes"]):
            print(f"  {i}: {node['properties'].get('name', node['id'])}")

    return paths
```

---

## 5. POST /api/v1/query/builder - Query Builder

### Purpose
Helper endpoint for frontend query builders to generate and validate Cypher queries programmatically.

### Request Schema

```json
{
  "mode": "string ('pattern' | 'aggregation' | 'path')",
  "start_entity": {
    "type": "string",
    "filter": "object"
  },
  "relationships": [
    {
      "type": "string",
      "direction": "string ('out' | 'in' | 'both')",
      "target_entity": {
        "type": "string",
        "filter": "object"
      },
      "properties": "object"
    }
  ],
  "aggregations": ["string"],
  "ordering": [
    {
      "field": "string",
      "direction": "string ('asc' | 'desc')"
    }
  ],
  "limit": "integer"
}
```

### Response Schema

```json
{
  "status": "success",
  "data": {
    "query": "MATCH (start:Entity {type: $type}) RETURN start",
    "parameters": {
      "type": "vulnerability"
    },
    "explanation": "Simple pattern match for vulnerability entities",
    "complexity": "simple",
    "estimated_time_ms": 45
  }
}
```

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/query/builder \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "pattern",
    "start_entity": {
      "type": "Vulnerability",
      "filter": {"severity": "critical"}
    },
    "relationships": [
      {
        "type": "AFFECTS",
        "direction": "out",
        "target_entity": {
          "type": "Organization"
        }
      }
    ],
    "ordering": [
      {"field": "cvss_score", "direction": "desc"}
    ],
    "limit": 100
  }'
```

---

## 6. POST /api/v1/query/validate - Query Validation

### Purpose
Validate Cypher queries for syntax, security issues, and performance without executing them.

### Request Schema

```json
{
  "query": "string (required)",
  "check_injection": "boolean (default: true)",
  "check_performance": "boolean (default: true)",
  "check_syntax": "boolean (default: true)"
}
```

### Response Schema

```json
{
  "status": "success",
  "data": {
    "valid": true,
    "syntax_errors": [],
    "security_issues": [],
    "performance_warnings": [
      {
        "severity": "warning",
        "message": "Query may benefit from index on 'Entity.type'",
        "suggestion": "CREATE INDEX entity_type_idx FOR (n:Entity) ON (n.type)"
      }
    ],
    "estimated_complexity": "intermediate"
  }
}
```

---

## Security - Query Validation & Injection Prevention

### Input Validation Rules

**1. Cypher Injection Prevention**

```python
# VULNERABLE - String concatenation
query = f"MATCH (e:Entity {{name: '{user_input}'}}) RETURN e"

# SAFE - Parameter binding
query = "MATCH (e:Entity {name: $name}) RETURN e"
parameters = {"name": user_input}
```

**2. Restricted Keywords**

Blocked in user queries:
- `CALL` (stored procedures)
- `dbms.*` (database operations)
- `LOAD CSV` (file operations)
- `PLUGIN` (plugin operations)

**3. Query Timeout Protection**

- Default: 30 seconds
- Maximum: 10 minutes
- Prevents resource exhaustion

**4. Result Size Limits**

- Default limit: 1,000 records
- Maximum limit: 100,000 records
- Large results paginated

### Validation Pipeline

```
User Query
    ↓
[Syntax Check] → Returns errors if invalid
    ↓
[Security Scan] → Detects injection attempts
    ↓
[Authorization] → Checks user permissions
    ↓
[Parameter Binding] → Enforces type safety
    ↓
[Execution]
```

### Example: Safe Query Construction

```python
def execute_safe_query(client, search_term, entity_type, min_severity):
    """Execute query with full security validation"""

    # 1. Use parameterized query
    query = """
        MATCH (e:Entity)
        WHERE e.name CONTAINS $searchTerm
          AND e.type = $type
          AND e.severity IN $severities
        RETURN e.id, e.name, e.severity
        LIMIT $limit
    """

    # 2. Define parameters
    parameters = {
        "searchTerm": search_term,  # Never concatenate!
        "type": entity_type,
        "severities": get_severity_levels(min_severity),
        "limit": 1000
    }

    # 3. Validate before execution
    validation = client.validate_query(query, parameters)
    if not validation["valid"]:
        raise Exception(f"Query validation failed: {validation['errors']}")

    # 4. Execute safely
    return client.execute_cypher(query, parameters)
```

---

## Frontend Integration

### Query Builder Component

```javascript
// React example for query builder
import { QueryBuilder } from '@/components/query-builder';

export function AnalyticsPanel() {
  const [query, setQuery] = useState({
    mode: 'pattern',
    start_entity: { type: 'Vulnerability' },
    relationships: [],
    limit: 100
  });

  const handleBuild = async () => {
    const response = await fetch('/api/v1/query/builder', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(query)
    });

    const { data } = await response.json();
    console.log('Generated Cypher:', data.query);

    // Execute generated query
    const results = await executeQuery(data.query, data.parameters);
    setResults(results);
  };

  return (
    <QueryBuilder
      onChange={setQuery}
      onBuild={handleBuild}
    />
  );
}
```

### Graph Explorer Integration

```javascript
// Visualize query results as graph
function GraphExplorer({ queryResult }) {
  const { nodes, relationships } = queryResult.data.graph;

  const graphData = {
    nodes: nodes.map(n => ({
      id: n.id,
      label: n.properties.name || n.id,
      title: JSON.stringify(n.properties),
      color: getLabelColor(n.labels[0])
    })),
    edges: relationships.map(r => ({
      from: r.startNodeId,
      to: r.endNodeId,
      label: r.type,
      title: JSON.stringify(r.properties)
    }))
  };

  return <VisNetwork data={graphData} />;
}
```

---

## Business Value

### 1. Custom Analysis
- **Use Case**: Security teams can write ad-hoc queries
- **Value**: Find custom threat patterns not in predefined reports
- **Example**: "Find all vulnerabilities in financial sector introduced in last 30 days"

### 2. Advanced Analytics
- **Use Case**: Sector-level risk assessment
- **Value**: Understand cross-sector threat distribution
- **Example**: Map which sectors are targets of APT28

### 3. Dependency Discovery
- **Use Case**: Supply chain risk management
- **Value**: Identify vulnerabilities in vendor/supplier ecosystem
- **Example**: Trace technology dependencies through 8 organization layers

### 4. Attack Path Analysis
- **Use Case**: Incident response and threat hunting
- **Value**: Visualize complete attack chains
- **Example**: "What's the fastest attack path from initial access to critical database?"

### 5. Compliance Reporting
- **Use Case**: Demonstrate security control coverage
- **Value**: Show how organization mitigates known threats
- **Example**: "Which MITRE techniques can we detect/mitigate with current controls?"

---

## Example Queries

### 1. Attack Path Discovery

**Business Goal**: Identify complete attack chains from threat actors to critical assets

```cypher
MATCH path = (actor:MitreActor {name: $actorName})
             -[:USES_TECHNIQUE*1..5]->
             (tech:MitreTechnique)
             -[:EXPLOITS_CVE]->
             (cve:CVE)
WHERE cve.cvss_score >= 9.0
RETURN path, length(path) AS hops, cve.cvss_score
ORDER BY cve.cvss_score DESC
LIMIT 10
```

**API Request**:
```bash
curl -X POST http://localhost:8000/api/v1/query/multi-hop \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "start_node": {"type": "MitreActor", "name": "APT28"},
    "end_node": {"type": "CVE", "properties": {"cvss_score": {"$gte": 9.0}}},
    "max_hops": 5,
    "relationship_filters": ["USES_TECHNIQUE", "EXPLOITS_CVE"]
  }'
```

### 2. Sector Vulnerability Distribution

**Business Goal**: Understand which sectors face greatest vulnerability exposure

```cypher
MATCH (s:Sector)-[:CONTAINS]->(org:Organization)
      -[:AFFECTED_BY]->(v:Vulnerability)
WHERE v.severity IN ["critical", "high"]
WITH s.name AS sector,
     COUNT(DISTINCT v) AS vuln_count,
     AVG(v.cvss_score) AS avg_cvss,
     COUNT(DISTINCT org) AS org_count
RETURN sector, vuln_count, avg_cvss, org_count
ORDER BY vuln_count DESC
```

**API Request**:
```bash
curl -X POST http://localhost:8000/api/v1/cypher \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "MATCH (s:Sector)-[:CONTAINS]->(org:Organization) -[:AFFECTED_BY]->(v:Vulnerability) WHERE v.severity IN $severities WITH s.name AS sector, COUNT(DISTINCT v) AS vuln_count RETURN sector, vuln_count ORDER BY vuln_count DESC",
    "parameters": {"severities": ["critical", "high"]},
    "mode": "row"
  }'
```

### 3. Cross-Sector Dependency Chain

**Business Goal**: Trace supply chain risks across multiple sectors

```cypher
MATCH path = (source:Organization {sector: $sourceSector})
             -[:DEPENDS_ON*1..8]->
             (target:Organization)
WHERE target.sector <> source.sector
WITH path, length(path) AS chain_length
MATCH (target)-[:AFFECTED_BY]->(v:Vulnerability)
WHERE v.severity = "critical"
RETURN path, chain_length,
       collect(v.cve_id) AS exploitable_vulns,
       count(v) AS vuln_count
ORDER BY chain_length, vuln_count DESC
LIMIT 20
```

### 4. Threat Actor Toolset Analysis

**Business Goal**: Understand adversary capabilities for defense planning

```cypher
MATCH (actor:MitreActor {name: $actorName})
      -[:USES_TECHNIQUE]->(tech:MitreTechnique),
      (actor)-[:LEVERAGES_SOFTWARE]->(soft:MitreSoftware)
WITH actor,
     collect(DISTINCT tech {.id, .name, .tactic}) AS techniques,
     collect(DISTINCT soft {.id, .name, .type}) AS software,
     COUNT(DISTINCT tech) AS tech_count,
     COUNT(DISTINCT soft) AS soft_count
OPTIONAL MATCH (tech)<-[:MITIGATES]-(mit:MitreMitigation)
WITH actor, techniques, software, tech_count, soft_count,
     collect(DISTINCT mit) AS available_mitigations
RETURN {
  actor: actor.name,
  techniques: techniques,
  software: software,
  technique_count: tech_count,
  software_count: soft_count,
  mitigations_available: size(available_mitigations)
}
```

### 5. Vulnerability Impact Cascade

**Business Goal**: Identify critical vulnerabilities with widest impact

```cypher
MATCH (v:Vulnerability)
      -[:AFFECTS]->(org:Organization)
      -[:CONTAINS]->(system:System)
      -[:RUNS]->(software:Software)
WHERE v.severity = "critical"
WITH v, COUNT(DISTINCT org) AS org_count,
     COUNT(DISTINCT system) AS system_count,
     COUNT(DISTINCT software) AS software_count,
     COLLECT(DISTINCT org.sector) AS sectors_affected
RETURN v.cve_id, v.cvss_score, org_count, system_count,
       software_count, sectors_affected
ORDER BY org_count DESC, system_count DESC
LIMIT 25
```

---

## Performance Guidelines

### Query Complexity Estimation

| Hops | Typical Time | Recommendations |
|------|--------------|-----------------|
| 1-2 | 10-100ms | No optimization needed |
| 3-4 | 100-500ms | Use indexes, limit results |
| 5-7 | 500ms-2s | Reduce scope, add filters |
| 8-10 | 2-10s | Consider caching |
| 11-20 | 10-60s | Plan async, implement pagination |

### Optimization Tips

1. **Use Indexes**: Create indexes on frequently filtered properties
2. **Filter Early**: Apply WHERE clauses close to MATCH
3. **Limit Results**: Use LIMIT to cap result set
4. **Cache Results**: Store frequently accessed queries
5. **Batch Operations**: Group multiple queries when possible

### Query Performance Monitoring

```bash
# Check query execution plan
curl -X POST http://localhost:8000/api/v1/cypher \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "MATCH (e:Entity) WHERE e.severity = $sev RETURN e",
    "parameters": {"sev": "critical"},
    "explain": true
  }'
```

---

## Troubleshooting

### Common Issues

**Timeout Error**
- Reduce `max_hops` in path queries
- Add more specific filters
- Increase timeout parameter if appropriate

**Large Result Set**
- Use LIMIT parameter
- Add WHERE clause filters
- Paginate results

**Slow Query Performance**
- Check EXPLAIN output
- Verify indexes exist
- Reduce relationship depth

---

## Summary

The Query API provides powerful capabilities for:
- Custom threat analysis
- Sector risk assessment
- Attack path discovery
- Supply chain dependency mapping
- Graph visualization and exploration

All queries are validated for security, optimized for performance, and integrated with frontend tools for seamless analysis workflows.

**Best Practices**:
- Always use parameterized queries
- Validate before executing complex queries
- Monitor performance metrics
- Cache frequently used results
- Implement pagination for large result sets

---

**Document Status**: COMPLETE
**Last Updated**: 2025-11-25
**Version**: v1.0.0
