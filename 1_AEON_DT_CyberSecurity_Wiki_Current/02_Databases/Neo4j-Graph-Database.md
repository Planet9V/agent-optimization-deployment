# Neo4j Graph Database API Documentation

**File:** Neo4j-Graph-Database.md
**Created:** 2025-11-29
**Version:** v1.0.0
**Purpose:** Primary graph database API reference for AEON Digital Twin
**Status:** ACTIVE - CRITICAL INFRASTRUCTURE

---

## Executive Summary

Neo4j is the **PRIMARY database** for the AEON Cyber Digital Twin, storing all 7-level architecture data including CVEs, equipment, attack patterns, sectors, predictions, and psychohistory entities.

**Container Configuration:**
- **Container Name:** release-openspg-neo4j
- **Image:** neo4j:5.x (via OpenSPG)
- **Network:** openspg-network

**Service Endpoints:**
- **Bolt Protocol:** bolt://localhost:7687
- **HTTP API:** http://localhost:7474
- **Browser:** http://localhost:7474/browser

**Credentials:**
- **Username:** neo4j
- **Password:** neo4j@openspg

---

## Database Statistics (Verified 2025-11-29)

```cypher
// Node Counts
MATCH (n) RETURN count(n); // 1,104,066 nodes

// Relationship Counts
MATCH ()-[r]->() RETURN count(r); // 11,998,401 relationships

// Key Entity Counts
MATCH (n:CVE) RETURN count(n);           // 316,552
MATCH (n:Equipment) RETURN count(n);      // 48,288
MATCH (n:ATT_CK_Technique) RETURN count(n); // 691
MATCH (n:InformationEvent) RETURN count(n); // 5,001
MATCH (n:HistoricalPattern) RETURN count(n); // 14,985
MATCH (n:FutureThreat) RETURN count(n);   // 8,900
MATCH (n:WhatIfScenario) RETURN count(n); // 524
```

---

## Connection Methods

### 1. Bolt Protocol (Primary - Recommended)

**Python (neo4j-driver):**
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "neo4j@openspg")
)

def run_query(query, params=None):
    with driver.session() as session:
        result = session.run(query, params or {})
        return [record.data() for record in result]

# Example: Get CVE details
cves = run_query("""
    MATCH (c:CVE {id: $cve_id})
    RETURN c.id, c.cvss_score, c.description
""", {"cve_id": "CVE-2024-1234"})
```

**JavaScript (neo4j-driver):**
```javascript
const neo4j = require('neo4j-driver');

const driver = neo4j.driver(
    'bolt://localhost:7687',
    neo4j.auth.basic('neo4j', 'neo4j@openspg')
);

async function runQuery(query, params = {}) {
    const session = driver.session();
    try {
        const result = await session.run(query, params);
        return result.records.map(r => r.toObject());
    } finally {
        await session.close();
    }
}

// Example: Get sector equipment
const equipment = await runQuery(`
    MATCH (s:Sector {id: $sector_id})-[:CONTAINS]->(e:Equipment)
    RETURN e.id, e.name, e.criticality
`, { sector_id: 'energy' });
```

### 2. HTTP API

**Transaction Endpoint:**
```bash
# Execute Cypher via HTTP
curl -X POST http://localhost:7474/db/neo4j/tx/commit \
  -u neo4j:neo4j@openspg \
  -H "Content-Type: application/json" \
  -d '{
    "statements": [{
      "statement": "MATCH (c:CVE) RETURN count(c) as total"
    }]
  }'
```

**Response:**
```json
{
  "results": [{
    "columns": ["total"],
    "data": [{"row": [316552]}]
  }],
  "errors": []
}
```

### 3. Neo4j Browser

**URL:** http://localhost:7474/browser

**Features:**
- Interactive Cypher queries
- Graph visualization
- Query history
- Schema exploration

---

## Schema Overview (7-Level Architecture)

### Level 0: Foundation Layer

| Label | Count | Description |
|-------|-------|-------------|
| `Sector` | 16 | CISA critical infrastructure sectors |
| `Equipment` | 48,288 | Physical/virtual equipment |
| `Vendor` | 500+ | Equipment manufacturers |

**Cypher:**
```cypher
// Get all sectors with equipment counts
MATCH (s:Sector)
OPTIONAL MATCH (s)-[:CONTAINS]->(e:Equipment)
RETURN s.name, s.id, count(e) as equipment_count
ORDER BY equipment_count DESC
```

### Level 1: Vulnerability Layer

| Label | Count | Description |
|-------|-------|-------------|
| `CVE` | 316,552 | Common Vulnerabilities and Exposures |
| `CWE` | 1,426 | Common Weakness Enumeration |
| `CVSS` | 315,000+ | Scoring vectors |

**Cypher:**
```cypher
// Get CVEs affecting equipment
MATCH (e:Equipment {id: $equipment_id})-[:HAS_VULNERABILITY]->(c:CVE)
RETURN c.id, c.cvss_score, c.description, c.epss_score
ORDER BY c.cvss_score DESC
LIMIT 20
```

### Level 2: Attack Pattern Layer

| Label | Count | Description |
|-------|-------|-------------|
| `ATT_CK_Technique` | 691 | MITRE ATT&CK techniques |
| `ATT_CK_Tactic` | 14 | MITRE ATT&CK tactics |
| `CAPEC` | 559 | Attack patterns |

**Cypher:**
```cypher
// Get attack chain from CVE to Tactic
MATCH path = (c:CVE {id: $cve_id})-[:EXPLOITED_BY]->(w:CWE)
              -[:ENABLES]->(capec:CAPEC)-[:USES]->(t:ATT_CK_Technique)
              -[:PART_OF]->(tactic:ATT_CK_Tactic)
RETURN path
```

### Level 3: Threat Actor Layer

| Label | Count | Description |
|-------|-------|-------------|
| `ThreatActor` | 200+ | APT groups, cybercriminals |
| `Campaign` | 500+ | Attack campaigns |
| `Indicator` | 10,000+ | IoCs |

**Cypher:**
```cypher
// Get threat actors targeting sector
MATCH (ta:ThreatActor)-[:TARGETS]->(s:Sector {id: $sector_id})
RETURN ta.name, ta.aliases, ta.motivation
```

### Level 4: Cognitive Layer

| Label | Count | Description |
|-------|-------|-------------|
| `CognitiveBias` | 30 | Human cognitive biases |
| `PersonalityTrait` | 50+ | Big Five, DISC, MBTI |
| `RiskTolerance` | 5 | Risk tolerance levels |

**Cypher:**
```cypher
// Get biases affecting vulnerability response
MATCH (cb:CognitiveBias)-[:AFFECTS_PERCEPTION]->(c:CVE {id: $cve_id})
RETURN cb.name, cb.description, cb.mitigation
```

### Level 5: Temporal Layer

| Label | Count | Description |
|-------|-------|-------------|
| `InformationEvent` | 5,001 | Historical events |
| `HistoricalPattern` | 14,985 | Pattern recognition |
| `FutureThreat` | 8,900 | Predicted threats |

**Cypher:**
```cypher
// Get historical patterns for prediction
MATCH (hp:HistoricalPattern)-[:PREDICTS]->(ft:FutureThreat)
WHERE hp.sector = $sector_id
RETURN hp.pattern_type, ft.threat_type, ft.probability
ORDER BY ft.probability DESC
```

### Level 6: Psychohistory Layer (E27)

| Label | Count | Description |
|-------|-------|-------------|
| `WhatIfScenario` | 524 | Scenario analysis |
| `SeldonCrisis` | 3 | SC001-SC003 crisis types |
| `PsychohistoryPrediction` | 1,000+ | Population-level forecasts |

**Cypher:**
```cypher
// Seldon Crisis analysis
MATCH (sc:SeldonCrisis {id: $crisis_id})
OPTIONAL MATCH (sc)-[:TRIGGERED_BY]->(trigger)
OPTIONAL MATCH (sc)-[:MITIGATED_BY]->(mit)
RETURN sc, collect(trigger) as triggers, collect(mit) as mitigations
```

---

## Common Query Patterns

### NOW/NEXT/NEVER Triage

```cypher
// Get CVEs prioritized by NOW/NEXT/NEVER
MATCH (c:CVE)
WHERE c.triage_category IS NOT NULL
RETURN c.triage_category, count(c) as count
// NOW: 1.4%, NEXT: 18%, NEVER: 80.6%
```

### Attack Path Enumeration

```cypher
// Find attack paths from CVE to sector impact
MATCH path = (c:CVE)-[*1..5]-(s:Sector {id: $sector_id})
RETURN path, length(path) as hops
ORDER BY hops ASC
LIMIT 10
```

### Equipment Vulnerability Analysis

```cypher
// Equipment with critical vulnerabilities
MATCH (e:Equipment)-[:HAS_VULNERABILITY]->(c:CVE)
WHERE c.cvss_score >= 9.0
RETURN e.id, e.name, e.sector, count(c) as critical_vulns
ORDER BY critical_vulns DESC
LIMIT 20
```

### Psychohistory Prediction Query

```cypher
// Get epidemic spread prediction
MATCH (ep:EpidemicPrediction)-[:AFFECTS]->(s:Sector)
WHERE ep.r0 > 1.0
RETURN ep.malware_family, ep.r0, ep.peak_infection_day, s.name
ORDER BY ep.r0 DESC
```

---

## Index Configuration

### Existing Indexes

```cypher
// Show all indexes
SHOW INDEXES

// Key indexes for performance
CREATE INDEX cve_id IF NOT EXISTS FOR (c:CVE) ON (c.id);
CREATE INDEX equipment_id IF NOT EXISTS FOR (e:Equipment) ON (e.id);
CREATE INDEX sector_id IF NOT EXISTS FOR (s:Sector) ON (s.id);
CREATE INDEX technique_id IF NOT EXISTS FOR (t:ATT_CK_Technique) ON (t.id);
CREATE INDEX cve_cvss IF NOT EXISTS FOR (c:CVE) ON (c.cvss_score);
CREATE INDEX cve_epss IF NOT EXISTS FOR (c:CVE) ON (c.epss_score);
```

---

## Performance Guidelines

### Query Optimization

1. **Use LIMIT** for large result sets
2. **Use indexes** for WHERE clauses
3. **Profile queries** with `PROFILE` prefix
4. **Avoid Cartesian products** (missing relationships)

### Connection Pooling

```python
# Python: Configure connection pool
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "neo4j@openspg"),
    max_connection_pool_size=50,
    connection_acquisition_timeout=60
)
```

### Batch Operations

```cypher
// Batch update with UNWIND
UNWIND $cve_updates as update
MATCH (c:CVE {id: update.id})
SET c.epss_score = update.epss
RETURN count(c)
```

---

## Frontend Integration

### API Layer Access

Frontend developers should use the REST API layer (`/api/v1/query/cypher`) rather than direct Bolt connections:

```javascript
// Frontend: Use Query API
const response = await fetch('/api/v1/query/cypher', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        query: 'MATCH (c:CVE) WHERE c.cvss_score >= $min RETURN c LIMIT 100',
        params: { min: 9.0 }
    })
});
const data = await response.json();
```

### GraphQL Alternative

Use GraphQL API for typed queries with automatic pagination:

```graphql
query GetCriticalCVEs($minScore: Float!) {
    cves(filter: { cvss_gte: $minScore }, limit: 100) {
        id
        cvssScore
        description
        affectedEquipment {
            id
            name
        }
    }
}
```

---

## Troubleshooting

### Connection Issues

```bash
# Test connection
cypher-shell -a bolt://localhost:7687 -u neo4j -p 'neo4j@openspg' \
  "RETURN 1 as test"

# Check container status
docker ps | grep neo4j
docker logs release-openspg-neo4j --tail 50
```

### Query Timeout

```cypher
// Add timeout to long-running queries
CALL dbms.setConfigValue('dbms.transaction.timeout', '300s')
```

### Memory Issues

```bash
# Check Neo4j memory allocation
docker exec release-openspg-neo4j cat /var/lib/neo4j/conf/neo4j.conf | grep heap
```

---

## Security Notes

1. **Change default password** in production
2. **Use TLS/SSL** for external connections
3. **Restrict network access** to Docker network
4. **Audit queries** for injection vulnerabilities
5. **Use parameterized queries** always

---

## Related Documentation

- `04_APIs/API_QUERY.md` - Cypher query execution API
- `04_APIs/API_GRAPHQL.md` - GraphQL interface
- `03_Applications/OpenSPG-Server.md` - OpenSPG integration
- `01_ARCHITECTURE/02_LEVELS_OVERVIEW.md` - 7-level architecture

---

**CRITICAL:** Neo4j is the authoritative data source for all AEON queries. All other APIs ultimately query Neo4j.
