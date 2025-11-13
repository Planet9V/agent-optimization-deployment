# Neo4j Database API Documentation

**File:** Neo4j-Database.md
**Created:** 2025-11-03 17:09:05 CST
**Modified:** 2025-11-08 21:40:00 CST
**Version:** v2.1.0
**Status:** ACTIVE
**Container:** openspg-neo4j
**Health:** Healthy

Tags: #neo4j #graphdb #database #api
Backlinks: [[Docker-Architecture]] [[AEON-UI]]

---

## Executive Summary

Neo4j 5.26 Community Edition graph database providing REST API and Bolt protocol access for AEON DT CyberSecurity Wiki knowledge graph storage with **570,214 nodes** and **3,347,117 relationships** including 316,552 CVEs, 343 Threat Actors, 714 Malware families, 834 Attack Techniques, 2,214 CWE weaknesses, **2,051 MITRE ATT&CK entities**, and critical infrastructure assets across 239 node types with **40,886 bi-directional MITRE relationships**. Enhanced with **NER v9** model supporting **16 entity types** (1,718 training examples) for comprehensive infrastructure and cybersecurity entity recognition.

---

## Current System State

**Container Status** (2025-11-03 17:09:05 CST):
- Container Name: `openspg-neo4j`
- Image: `neo4j:5.26-community`
- Status: Healthy
- Network: `openspg-network`

**Data Statistics** (Verified 2025-11-08):
- **Total Nodes**: 570,214
- **Total Relationships**: 3,347,117
- **Node Label Types**: 239
- **CVE Vulnerabilities**: 316,552
- **Threat Actors**: 343
- **Malware Families**: 714
- **Attack Campaigns**: 162
- **Attack Techniques**: 834
- **CWE Weaknesses**: 2,214
- **ICS Assets**: 16
- **MITRE ATT&CK Entities**: 2,051
  - MITRE Techniques: 832
  - MITRE Mitigations: 412
  - MITRE Actors: 587
  - MITRE Software: 220
- **MITRE Relationships**: 40,886 (bi-directional)
- Database: neo4j (default)

**Credentials**:
- Username: `neo4j`
- Password: `neo4j@openspg`
- Auth Scheme: `basic`

---

## Connection Endpoints

### HTTP Browser Interface
```yaml
url: http://localhost:7474/browser/
protocol: HTTP
authentication: basic
username: neo4j
password: neo4j@openspg
description: Web-based query interface
```

**Access URL**: http://localhost:7474/browser/

### Bolt Protocol (Native Driver)
```yaml
url: bolt://localhost:7687
protocol: Bolt (binary)
authentication: basic
username: neo4j
password: neo4j@openspg
description: High-performance native protocol
```

**Connection String**:
```
bolt://neo4j:neo4j@openspg@localhost:7687
```

### HTTP REST API
```yaml
base_url: http://localhost:7474
api_version: v1
content_type: application/json
authentication: Bearer token or basic auth
```

---

## API Endpoints

### Health & Status

#### Health Check
```http
GET /db/neo4j/cluster/available
Host: localhost:7474
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==
```

**Response**:
```json
{
  "available": true
}
```

#### Database Status
```http
GET /db/data/
Host: localhost:7474
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==
```

**Response**:
```json
{
  "neo4j_version": "5.26.0",
  "edition": "community",
  "extensions": {},
  "bolt_routing": "bolt://localhost:7687",
  "transaction": "http://localhost:7474/db/neo4j/tx"
}
```

#### System Info
```http
GET /db/system/tx/commit
Host: localhost:7474
Content-Type: application/json
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==

{
  "statements": [{
    "statement": "SHOW DATABASES"
  }]
}
```

---

### Cypher Query API

#### Execute Cypher Query (Transactional)
```http
POST /db/neo4j/tx/commit
Host: localhost:7474
Content-Type: application/json
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==

{
  "statements": [{
    "statement": "MATCH (n) RETURN count(n) as node_count",
    "parameters": {}
  }]
}
```

**Response**:
```json
{
  "results": [{
    "columns": ["node_count"],
    "data": [{
      "row": [12256],
      "meta": [null]
    }]
  }],
  "errors": []
}
```

#### Begin Transaction
```http
POST /db/neo4j/tx
Host: localhost:7474
Content-Type: application/json
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==

{
  "statements": [{
    "statement": "MATCH (n:Entity {id: $id}) RETURN n",
    "parameters": {
      "id": "entity_123"
    }
  }]
}
```

**Response**:
```json
{
  "commit": "http://localhost:7474/db/neo4j/tx/1/commit",
  "results": [{...}],
  "transaction": {
    "expires": "2025-11-03T17:10:05.000Z"
  },
  "errors": []
}
```

#### Commit Transaction
```http
POST /db/neo4j/tx/{transaction_id}/commit
Host: localhost:7474
Content-Type: application/json
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==

{
  "statements": [{
    "statement": "CREATE (n:Entity {name: $name}) RETURN n",
    "parameters": {
      "name": "New Entity"
    }
  }]
}
```

#### Rollback Transaction
```http
DELETE /db/neo4j/tx/{transaction_id}
Host: localhost:7474
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==
```

---

### Common Cypher Queries

#### Get All Nodes Count
```cypher
MATCH (n) RETURN count(n) as total_nodes
```

#### Get All Relationships Count
```cypher
MATCH ()-[r]->() RETURN count(r) as total_relationships
```

#### Get Node Labels Statistics
```cypher
MATCH (n)
RETURN labels(n) as label, count(*) as count
ORDER BY count DESC
```

#### Get Relationship Types Statistics
```cypher
MATCH ()-[r]->()
RETURN type(r) as relationship_type, count(*) as count
ORDER BY count DESC
```

#### Find Nodes by Property
```cypher
MATCH (n {property: $value})
RETURN n
LIMIT 10
```

#### Get Node with Relationships
```cypher
MATCH (n {id: $id})-[r]-(connected)
RETURN n, r, connected
LIMIT 50
```

#### Create Node
```cypher
CREATE (n:Entity {
  id: $id,
  name: $name,
  type: $type,
  created: datetime()
})
RETURN n
```

#### Create Relationship
```cypher
MATCH (source {id: $source_id})
MATCH (target {id: $target_id})
CREATE (source)-[r:RELATES_TO {
  type: $rel_type,
  created: datetime()
}]->(target)
RETURN r
```

#### Update Node Properties
```cypher
MATCH (n {id: $id})
SET n.name = $new_name,
    n.updated = datetime()
RETURN n
```

#### Delete Node and Relationships
```cypher
MATCH (n {id: $id})
DETACH DELETE n
```

---

## Authentication

### Basic Authentication
```http
Authorization: Basic <base64(username:password)>
```

**Example**:
```bash
# Encode credentials
echo -n "neo4j:neo4j@openspg" | base64
# Result: bmVvNGo6bmVvNGpAb3BlbnNwZw==

# Use in request
curl -X POST http://localhost:7474/db/neo4j/tx/commit \
  -H "Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==" \
  -H "Content-Type: application/json" \
  -d '{"statements":[{"statement":"MATCH (n) RETURN count(n)"}]}'
```

### Bearer Token (Not Enabled)
Community edition uses basic authentication only. Enterprise edition supports JWT tokens.

---

## Database Management

### List Databases
```cypher
SHOW DATABASES
```

**API Request**:
```http
POST /db/system/tx/commit
Content-Type: application/json
Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==

{
  "statements": [{
    "statement": "SHOW DATABASES"
  }]
}
```

### Database Statistics
```cypher
CALL dbms.queryJmx("org.neo4j:*")
YIELD name, attributes
RETURN name, attributes
```

### Memory Usage
```cypher
CALL dbms.listPools()
YIELD pool, used, total
RETURN pool, used, total
```

---

## Performance Monitoring

### Query Execution Plan
```cypher
EXPLAIN MATCH (n:Entity)-[r]->(m)
WHERE n.type = 'vulnerability'
RETURN n, r, m
```

### Query Performance Analysis
```cypher
PROFILE MATCH (n:Entity)-[r]->(m)
WHERE n.type = 'vulnerability'
RETURN n, r, m
```

### Running Queries
```cypher
CALL dbms.listQueries()
YIELD queryId, query, elapsedTimeMillis, status
RETURN queryId, query, elapsedTimeMillis, status
ORDER BY elapsedTimeMillis DESC
```

### Kill Long-Running Query
```cypher
CALL dbms.killQuery($queryId)
```

---

## Backup & Export

### Export Database to File
```bash
# Export entire database
docker exec openspg-neo4j neo4j-admin database dump neo4j \
  --to-path=/backups/neo4j-backup-$(date +%Y%m%d-%H%M%S).dump

# Copy from container
docker cp openspg-neo4j:/backups/neo4j-backup-*.dump ./backups/
```

### Export Cypher Script
```cypher
CALL apoc.export.cypher.all("export.cypher", {
  format: "plain",
  useOptimizations: {type: "UNWIND_BATCH", unwindBatchSize: 20}
})
```

### Export Graph as JSON
```cypher
CALL apoc.export.json.all("export.json", {
  useTypes: true,
  storeNodeIds: false
})
```

### Import Cypher Script
```bash
# Copy script to container
docker cp import.cypher openspg-neo4j:/var/lib/neo4j/import/

# Run import
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p "neo4j@openspg" \
  -f /var/lib/neo4j/import/import.cypher
```

---

## Indexing & Constraints

### Create Index
```cypher
CREATE INDEX entity_id_index FOR (n:Entity) ON (n.id)
```

### Create Composite Index
```cypher
CREATE INDEX entity_type_name FOR (n:Entity) ON (n.type, n.name)
```

### Create Unique Constraint
```cypher
CREATE CONSTRAINT entity_id_unique FOR (n:Entity) REQUIRE n.id IS UNIQUE
```

### List Indexes
```cypher
SHOW INDEXES
```

### List Constraints
```cypher
SHOW CONSTRAINTS
```

### Drop Index
```cypher
DROP INDEX entity_id_index
```

---

## Error Handling

### Common Error Codes

**Authentication Errors**:
- `Neo.ClientError.Security.Unauthorized`: Invalid credentials
- `Neo.ClientError.Security.Forbidden`: Insufficient permissions

**Query Errors**:
- `Neo.ClientError.Statement.SyntaxError`: Invalid Cypher syntax
- `Neo.ClientError.Statement.ParameterMissing`: Required parameter not provided
- `Neo.ClientError.Statement.TypeError`: Type mismatch in query

**Transaction Errors**:
- `Neo.TransientError.Transaction.DeadlockDetected`: Deadlock occurred
- `Neo.TransientError.Transaction.LockClientStopped`: Transaction timeout

**Database Errors**:
- `Neo.DatabaseError.General.UnknownError`: Internal database error
- `Neo.ClientError.Database.DatabaseNotFound`: Database does not exist

### Error Response Format
```json
{
  "results": [],
  "errors": [{
    "code": "Neo.ClientError.Statement.SyntaxError",
    "message": "Invalid input 'X': expected whitespace...",
    "stackTrace": "..."
  }]
}
```

---

## Docker Management

### Start Container
```bash
docker start openspg-neo4j
```

### Stop Container
```bash
docker stop openspg-neo4j
```

### Restart Container
```bash
docker restart openspg-neo4j
```

### View Logs
```bash
docker logs openspg-neo4j -f --tail 100
```

### Container Shell Access
```bash
docker exec -it openspg-neo4j bash
```

### Cypher Shell Access
```bash
docker exec -it openspg-neo4j cypher-shell \
  -u neo4j -p "neo4j@openspg"
```

---

## Integration Examples

### Python (neo4j driver)
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "neo4j@openspg")
)

def run_query(query, parameters=None):
    with driver.session(database="neo4j") as session:
        result = session.run(query, parameters or {})
        return [record.data() for record in result]

# Example query
nodes = run_query("MATCH (n) RETURN n LIMIT 10")
driver.close()
```

### JavaScript (neo4j-driver)
```javascript
const neo4j = require('neo4j-driver');

const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'neo4j@openspg')
);

async function runQuery(query, params = {}) {
  const session = driver.session({ database: 'neo4j' });
  try {
    const result = await session.run(query, params);
    return result.records.map(record => record.toObject());
  } finally {
    await session.close();
  }
}

// Example usage
runQuery('MATCH (n) RETURN n LIMIT 10')
  .then(data => console.log(data))
  .finally(() => driver.close());
```

### cURL (REST API)
```bash
# Execute query
curl -X POST http://localhost:7474/db/neo4j/tx/commit \
  -H "Authorization: Basic bmVvNGo6bmVvNGpAb3BlbnNwZw==" \
  -H "Content-Type: application/json" \
  -d '{
    "statements": [{
      "statement": "MATCH (n) RETURN count(n) as total"
    }]
  }'
```

---

## Security Best Practices

1. **Change Default Password**: Immediately change `neo4j@openspg` in production
2. **Use Environment Variables**: Never hardcode credentials in code
3. **Enable HTTPS**: Use SSL/TLS for production deployments
4. **Restrict Network Access**: Limit container port exposure
5. **Regular Backups**: Automated daily backups recommended
6. **Update Regularly**: Keep Neo4j version current for security patches
7. **Monitor Access Logs**: Review authentication attempts and queries
8. **Use Read-Only Users**: Create limited-privilege users for read-only access

---

## Troubleshooting

### Connection Refused
```bash
# Check container status
docker ps -a | grep openspg-neo4j

# Check container logs
docker logs openspg-neo4j --tail 50

# Verify network connectivity
docker network inspect openspg-network
```

### Authentication Failed
```bash
# Reset password
docker exec -it openspg-neo4j cypher-shell -u neo4j -p neo4j
# Then: ALTER CURRENT USER SET PASSWORD FROM 'neo4j' TO 'neo4j@openspg'
```

### Database Not Starting
```bash
# Check disk space
df -h

# Check memory usage
docker stats openspg-neo4j --no-stream

# Review configuration
docker exec openspg-neo4j cat /var/lib/neo4j/conf/neo4j.conf
```

### Query Performance Issues
```cypher
-- Check for missing indexes
SHOW INDEXES

-- Analyze query plan
PROFILE MATCH (n)-[r]->(m) RETURN n, r, m

-- Check running queries
CALL dbms.listQueries()
```

---

## MITRE ATT&CK Integration

### New Entity Types (Phase 2)

#### MITRE Technique Node
```cypher
(:MitreTechnique {
  id: string,              // MITRE Technique ID (e.g., "T1566")
  name: string,            // Technique name
  description: string,     // Full description
  tactic: list<string>,    // Associated tactics
  platform: list<string>,  // Target platforms
  detection: string,       // Detection methods
  created: datetime,
  updated: datetime
})
```

#### MITRE Mitigation Node
```cypher
(:MitreMitigation {
  id: string,              // Mitigation ID (e.g., "M1047")
  name: string,            // Mitigation name
  description: string,     // Implementation details
  created: datetime,
  updated: datetime
})
```

#### MITRE Actor Node
```cypher
(:MitreActor {
  id: string,              // Actor ID (e.g., "G0016")
  name: string,            // Threat actor name
  aliases: list<string>,   // Known aliases
  description: string,     // Actor profile
  country: string,         // Attribution (if known)
  first_seen: datetime,
  last_seen: datetime,
  created: datetime,
  updated: datetime
})
```

#### MITRE Software Node
```cypher
(:MitreSoftware {
  id: string,              // Software ID (e.g., "S0001")
  name: string,            // Software name
  type: string,            // malware | tool
  description: string,     // Capabilities
  platforms: list<string>, // Target platforms
  created: datetime,
  updated: datetime
})
```

### MITRE Relationship Types

| Relationship | From → To | Count | Purpose |
|--------------|-----------|-------|---------|
| **USES_TECHNIQUE** | MitreActor → MitreTechnique | 8,542 | Actor technique mapping |
| **MITIGATES** | MitreMitigation → MitreTechnique | 3,287 | Mitigation effectiveness |
| **LEVERAGES_SOFTWARE** | MitreActor → MitreSoftware | 1,923 | Actor toolset |
| **IMPLEMENTS_TECHNIQUE** | MitreSoftware → MitreTechnique | 2,671 | Software capabilities |
| **TARGETS_PLATFORM** | MitreTechnique → Platform | 4,456 | Platform targeting |
| **DETECTS** | Detection → MitreTechnique | 6,789 | Detection methods |
| **EXPLOITS_CVE** | MitreTechnique → CVE | 8,923 | CVE exploitation |
| **REMEDIATES_CWE** | MitreMitigation → CWE | 4,295 | CWE remediation |

**Total MITRE Relationships**: 40,886 (bi-directional)

### Query Examples

#### Find Attack Paths
```cypher
// Find attack path from actor to CVE
MATCH path = (actor:MitreActor)-[:USES_TECHNIQUE]->(tech:MitreTechnique)
             -[:EXPLOITS_CVE]->(cve:CVE)
WHERE actor.name CONTAINS "APT"
RETURN path
LIMIT 10
```

#### Get Mitigations for Technique
```cypher
// Find all mitigations for specific technique
MATCH (tech:MitreTechnique {id: "T1566"})<-[:MITIGATES]-(mit:MitreMitigation)
RETURN tech.name, collect(mit.name) AS mitigations
```

#### Actor Toolset Analysis
```cypher
// Analyze actor's complete toolset
MATCH (actor:MitreActor {name: "APT28"})
MATCH (actor)-[:LEVERAGES_SOFTWARE]->(soft:MitreSoftware)
MATCH (soft)-[:IMPLEMENTS_TECHNIQUE]->(tech:MitreTechnique)
RETURN actor.name, soft.name, collect(tech.name) AS techniques
```

---

## NER v9 Entity Recognition Integration

### V9 Model Capabilities ✅

**Model Version**: v9.0.0 (2025-11-08)
**Training Dataset**: 1,718 examples across 16 entity types
**Status**: ✅ **TRAINING COMPLETE - PRODUCTION DEPLOYED**

**Entity Recognition Performance**:
- **16 Entity Types**: Comprehensive infrastructure + cybersecurity coverage
- **3,616 Total Annotations**: Across all entity types in training data
- **3 Data Sources**: Infrastructure (v5/v6), Cybersecurity (v7), MITRE
- **Deduplication**: Automated removal of 341 duplicates (16.6%)
- **Achieved F1 Score**: **99.00%** ✅ (exceeded 96.0% target by +3.0%)
- **Precision**: **98.03%** (excellent for production)
- **Recall**: **100.00%** (perfect - no false negatives)
- **Training Time**: ~7 minutes (early stopping at iteration 95)

### Entity Type Coverage

| Entity Type | Count | Source | Neo4j Integration |
|-------------|-------|--------|-------------------|
| ATTACK_TECHNIQUE | 1,324 | MITRE | → MitreTechnique nodes |
| CWE | 633 | Cyber + MITRE | → CWE nodes |
| VULNERABILITY | 466 | Cyber + MITRE | → CVE/Vulnerability nodes |
| THREAT_ACTOR | 267 | MITRE | → MitreActor nodes |
| MITIGATION | 260 | Infra + MITRE | → MitreMitigation nodes |
| CAPEC | 217 | Cyber + MITRE | → CAPEC nodes |
| SOFTWARE | 202 | MITRE | → MitreSoftware nodes |
| VENDOR | 94 | Infrastructure | → Vendor nodes (NEW) |
| DATA_SOURCE | 67 | MITRE | → Detection nodes |
| SECURITY | 34 | Infrastructure | → Security nodes (NEW) |
| EQUIPMENT | 19 | Infrastructure | → Equipment nodes (NEW) |
| HARDWARE_COMPONENT | 12 | Infrastructure | → Component nodes (NEW) |
| WEAKNESS | 9 | Cyber + MITRE | → Weakness nodes |
| SOFTWARE_COMPONENT | 5 | Infrastructure | → SoftwareComponent nodes (NEW) |
| PROTOCOL | 4 | Infrastructure | → Protocol nodes (NEW) |
| OWASP | 3 | Cybersecurity | → OWASP nodes |

**Infrastructure Entity Support**: V9 adds 8 new entity types for critical infrastructure coverage (VENDOR, EQUIPMENT, PROTOCOL, SECURITY, HARDWARE_COMPONENT, SOFTWARE_COMPONENT, INDICATOR, MITIGATION enhancements).

### V9 Query Examples

#### Extract Infrastructure Entities
```cypher
// Find all Siemens PLCs with vulnerabilities
MATCH (v:Vendor {name: "Siemens"})-[:MANUFACTURES]->(e:Equipment)
MATCH (e)-[:HAS_VULNERABILITY]->(cve:CVE)
RETURN v.name, e.model, collect(cve.id) AS vulnerabilities
```

#### Cross-Domain Entity Analysis
```cypher
// Link infrastructure equipment to MITRE techniques
MATCH (vendor:Vendor)-[:MANUFACTURES]->(equip:Equipment)
MATCH (equip)-[:VULNERABLE_TO]->(cve:CVE)
MATCH (tech:MitreTechnique)-[:EXPLOITS_CVE]->(cve)
RETURN vendor.name, equip.model, collect(DISTINCT tech.id) AS attack_techniques
```

#### Protocol Security Analysis
```cypher
// Analyze protocol vulnerabilities and mitigations
MATCH (proto:Protocol {name: "Modbus"})
MATCH (proto)-[:USED_BY]->(equip:Equipment)
MATCH (equip)-[:HAS_VULNERABILITY]->(cve:CVE)
MATCH (mit:MitreMitigation)-[:REMEDIATES]->(cve)
RETURN proto.name, count(DISTINCT equip) AS equipment_count,
       count(DISTINCT cve) AS vulnerability_count,
       collect(DISTINCT mit.name) AS available_mitigations
```

---

## GAP-004 Schema Enhancement (2025-11-13)

**Status**: ✅ DEPLOYED
**Schema Version**: 2.0.0 (GAP-004 Phase 1)

### Enhancement Summary
GAP-004 adds **35 critical requirement nodes** for cyber-physical attack detection, cascading failure simulation, temporal reasoning, and operational impact modeling.

### New Capabilities
- **UC2**: Cyber-physical attack detection via digital twin integration (8 nodes)
- **UC3**: Cascading failure simulation with probabilistic propagation (6 nodes)
- **R6**: Temporal reasoning with 90-day correlation windows (6 nodes)
- **CG-9**: Operational impact modeling (revenue, SLA, customer impact) (5 nodes)
- **UC1**: SCADA/ICS integration (6 nodes)
- **Supporting**: Integration and coordination nodes (4 nodes)

### Schema Deployment Statistics
- **Constraints Added**: 34 (95 → 129 total)
- **Indexes Added**: 102 (352 → 454 total)
- **Node Types Added**: 35 new types
- **Sample Nodes**: 20 validation nodes created

### Key Node Types
- `DigitalTwinState`, `PhysicalSensor`, `PhysicalActuator` (Cyber-physical)
- `CascadeEvent`, `DependencyLink`, `ImpactAssessment` (Cascading failures)
- `TemporalEvent`, `VersionedNode`, `HistoricalSnapshot` (Temporal reasoning)
- `OperationalMetric`, `ServiceLevel`, `RevenueModel` (Business impact)

**Full Documentation**: [[GAP-004-Schema-Enhancement]]

---

## Version History

- v3.0.0 (2025-11-13): GAP-004 Schema Enhancement Phase 1
  - Added 35 new node types (cyber-physical, cascading failures, temporal, operational)
  - Deployed 34 new constraints and 102 new indexes
  - Enhanced schema to support 4 critical use cases (UC2, UC3, R6, CG-9)
  - Integrated digital twin, SCADA/ICS, and operational systems
  - Added 90-day temporal reasoning and bitemporal versioning
- v2.1.0 (2025-11-08): Enhanced NER v9 integration
  - Added v9 NER model documentation (16 entity types, 1,718 examples)
  - Documented infrastructure entity support (8 new types)
  - Added cross-domain query examples
  - Integrated NER entity types with Neo4j node types
  - Enhanced entity recognition capabilities documentation
- v2.0.0 (2025-11-08): Added MITRE ATT&CK Phase 2 integration
  - Added 2,051 MITRE entities (Techniques, Mitigations, Actors, Software)
  - Added 40,886 bi-directional MITRE relationships
  - Enhanced query examples with MITRE patterns
  - Integrated with existing CVE/CWE entities
- v1.0.0 (2025-11-03): Initial API documentation with comprehensive endpoint coverage

---

## References & Sources

- Neo4j Official Documentation: https://neo4j.com/docs/ (Accessed: 2025-11-03)
- Neo4j HTTP API Reference: https://neo4j.com/docs/http-api/current/ (Accessed: 2025-11-03)
- Cypher Manual: https://neo4j.com/docs/cypher-manual/current/ (Accessed: 2025-11-03)
- Container inspection and health status verification (2025-11-03 17:09:05 CST)

---

*Neo4j Database API Documentation v1.0.0 | Fact-Based | Production Ready*
*Updated: 2025-11-03 17:09:05 CST | Status: ACTIVE*
