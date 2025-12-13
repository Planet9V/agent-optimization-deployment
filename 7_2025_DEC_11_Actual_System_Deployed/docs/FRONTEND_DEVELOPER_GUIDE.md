# AEON Digital Twin - Frontend Developer Integration Guide

**File:** FRONTEND_DEVELOPER_GUIDE.md
**Created:** 2025-12-12
**Database:** Neo4j 5.x (bolt://localhost:7687)
**Database:** Qdrant (localhost:6333)
**Version:** 1.0.0
**Status:** PRODUCTION-READY

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Connection Setup](#connection-setup)
3. [Data Models](#data-models)
4. [Common Query Patterns](#common-query-patterns)
5. [Real Working Examples](#real-working-examples)
6. [Authentication & Security](#authentication--security)
7. [Performance Tips](#performance-tips)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### System Overview

**Database Scale**:
- **1,207,069 nodes** across 631 different types
- **12,344,852 relationships** across 183 relationship types
- **16 Critical Infrastructure Sectors** fully modeled
- **316,552 CVE vulnerability records**
- **140,000 SBOM (Software Bill of Materials) records**

**Capabilities**:
- ✅ 20-hop multi-hop reasoning
- ✅ Cross-domain queries (cyber-infrastructure-compliance)
- ✅ Sector-specific analysis
- ✅ Software supply chain tracking
- ✅ Vulnerability impact analysis

---

## 🔌 Connection Setup

### 1. Neo4j Browser Connection

**Quick Connect**:
```
URL: http://localhost:7474
Bolt URL: bolt://localhost:7687
Username: neo4j
Password: neo4j@openspg
Database: neo4j (default)
```

**Browser Access**:
1. Open browser to `http://localhost:7474`
2. Enter connection details above
3. Click "Connect"
4. Start running Cypher queries

---

### 2. Python Neo4j Driver

**Installation**:
```bash
pip install neo4j
```

**Basic Connection**:
```python
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self):
        self.uri = "bolt://localhost:7687"
        self.user = "neo4j"
        self.password = "neo4j@openspg"
        self.driver = None

    def connect(self):
        """Establish connection to Neo4j"""
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )
        return self.driver

    def close(self):
        """Close database connection"""
        if self.driver:
            self.driver.close()

    def query(self, cypher_query, parameters=None):
        """Execute Cypher query and return results"""
        with self.driver.session() as session:
            result = session.run(cypher_query, parameters or {})
            return [record.data() for record in result]

# Usage
db = Neo4jConnection()
db.connect()

# Run a query
results = db.query("""
    MATCH (n:Equipment)
    RETURN n.name, labels(n)
    LIMIT 10
""")

print(results)
db.close()
```

**With Context Manager**:
```python
from neo4j import GraphDatabase

class AEONDatabase:
    def __init__(self, uri="bolt://localhost:7687",
                 user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def execute_query(self, query, parameters=None):
        """Execute query and return results as list of dicts"""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]

# Usage
with AEONDatabase() as db:
    equipment = db.execute_query("""
        MATCH (e:Equipment)-[:GENERATES_MEASUREMENT]->(m:Measurement)
        WHERE e.name CONTAINS 'Turbine'
        RETURN e.name as equipment, count(m) as measurements
        ORDER BY measurements DESC
        LIMIT 10
    """)

    for item in equipment:
        print(f"{item['equipment']}: {item['measurements']} measurements")
```

---

### 3. JavaScript Neo4j Driver

**Installation**:
```bash
npm install neo4j-driver
```

**Connection Setup**:
```javascript
const neo4j = require('neo4j-driver');

class AEONDatabase {
    constructor() {
        this.uri = 'bolt://localhost:7687';
        this.user = 'neo4j';
        this.password = 'neo4j@openspg';
        this.driver = neo4j.driver(
            this.uri,
            neo4j.auth.basic(this.user, this.password)
        );
    }

    async query(cypherQuery, parameters = {}) {
        const session = this.driver.session();
        try {
            const result = await session.run(cypherQuery, parameters);
            return result.records.map(record => record.toObject());
        } finally {
            await session.close();
        }
    }

    async close() {
        await this.driver.close();
    }
}

// Usage
async function main() {
    const db = new AEONDatabase();

    try {
        const equipment = await db.query(`
            MATCH (e:Equipment)
            WHERE e.sector = 'ENERGY'
            RETURN e.name, e.type, e.sector
            LIMIT 10
        `);

        console.log('Energy Equipment:', equipment);
    } finally {
        await db.close();
    }
}

main();
```

**React Hook Example**:
```javascript
import { useState, useEffect } from 'react';
import neo4j from 'neo4j-driver';

export function useNeo4jQuery(query, parameters = {}) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const driver = neo4j.driver(
            'bolt://localhost:7687',
            neo4j.auth.basic('neo4j', 'neo4j@openspg')
        );

        async function fetchData() {
            const session = driver.session();
            try {
                const result = await session.run(query, parameters);
                const records = result.records.map(r => r.toObject());
                setData(records);
                setLoading(false);
            } catch (err) {
                setError(err);
                setLoading(false);
            } finally {
                await session.close();
                await driver.close();
            }
        }

        fetchData();
    }, [query, JSON.stringify(parameters)]);

    return { data, loading, error };
}

// Usage in component
function EquipmentList() {
    const { data, loading, error } = useNeo4jQuery(`
        MATCH (e:Equipment)
        WHERE e.sector = $sector
        RETURN e.name, e.type
        LIMIT 20
    `, { sector: 'ENERGY' });

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <ul>
            {data.map((item, idx) => (
                <li key={idx}>{item['e.name']} - {item['e.type']}</li>
            ))}
        </ul>
    );
}
```

---

### 4. Qdrant Connection

**Installation**:
```bash
pip install qdrant-client sentence-transformers
```

**Python Connection**:
```python
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class QdrantConnection:
    def __init__(self):
        self.host = "localhost"
        self.port = 6333
        self.collection = "aeon-actual-system"
        self.client = QdrantClient(host=self.host, port=self.port)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def search(self, query_text, limit=10):
        """Search for similar documents"""
        # Generate query embedding
        query_vector = self.model.encode(query_text).tolist()

        # Search Qdrant
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=limit
        )

        return results

# Usage
qdrant = QdrantConnection()
results = qdrant.search("How to query CVE vulnerabilities", limit=5)

for hit in results:
    print(f"Score: {hit.score}")
    print(f"Content: {hit.payload.get('content', '')[:200]}...")
    print("---")
```

---

## 📊 Data Models

### Node Types by Category

#### 1. **Cybersecurity & Threat Intelligence**

**CVE (316,552 nodes)**:
```python
{
    "id": "CVE-2023-12345",
    "name": "CVE-2023-12345",
    "description": "Buffer overflow vulnerability...",
    "severity": "CRITICAL",
    "cvss_score": 9.8,
    "published_date": "2023-05-15",
    "cwe_id": "CWE-119"
}
```

**Vulnerability (12,022 nodes)**:
```python
{
    "id": "vuln_001",
    "name": "SQL Injection in Login Form",
    "type": "SQL_INJECTION",
    "severity": "HIGH",
    "cwe": "CWE-89",
    "affected_systems": ["Web Application", "Database"]
}
```

**Threat (9,875 nodes)**:
```python
{
    "id": "threat_apt28",
    "name": "APT28",
    "type": "ADVANCED_PERSISTENT_THREAT",
    "origin": "Russia",
    "active": true,
    "target_sectors": ["ENERGY", "GOVERNMENT_FACILITIES"]
}
```

---

#### 2. **Critical Infrastructure Equipment**

**Equipment (48,288 nodes)**:
```python
{
    "id": "equip_turbine_001",
    "name": "Gas Turbine GT-100",
    "type": "TURBINE",
    "sector": "ENERGY",
    "subsector": "Energy_Transmission",
    "manufacturer": "Siemens",
    "model": "SGT-800",
    "commissioned_date": "2020-03-15"
}
```

**Device (48,400 nodes)**:
```python
{
    "id": "dev_plc_001",
    "name": "PLC Control Unit",
    "type": "PLC",
    "vendor": "Siemens",
    "model": "S7-1500",
    "firmware_version": "V2.9.3",
    "ip_address": "192.168.1.100",
    "sector": "WATER"
}
```

---

#### 3. **Software Supply Chain**

**SBOM (140,000 nodes)**:
```python
{
    "id": "sbom_webapp_v1",
    "name": "Web Application SBOM",
    "version": "1.0.0",
    "format": "CycloneDX",
    "generated_date": "2025-01-15",
    "component_count": 150
}
```

**Software_Component (55,000 nodes)**:
```python
{
    "id": "comp_react_18",
    "name": "React",
    "version": "18.2.0",
    "type": "LIBRARY",
    "language": "JavaScript",
    "license": "MIT",
    "vulnerabilities": ["CVE-2023-xxxxx"]
}
```

---

#### 4. **Measurements & Monitoring**

**Measurement (275,458 nodes)**:
```python
{
    "id": "meas_001",
    "name": "Temperature Reading",
    "type": "TEMPERATURE",
    "value": 85.5,
    "unit": "CELSIUS",
    "timestamp": "2025-12-12T10:30:00Z",
    "equipment_id": "equip_turbine_001",
    "threshold_exceeded": false
}
```

**Monitoring (181,704 nodes)**:
```python
{
    "id": "mon_001",
    "name": "Continuous Temperature Monitor",
    "type": "REAL_TIME",
    "frequency": "5s",
    "equipment_id": "equip_turbine_001",
    "alert_threshold": 90.0
}
```

---

### Relationship Types by Category

#### Common Relationship Patterns

**Top 10 Relationship Types**:
1. `IMPACTS` (4,780,563) - Vulnerability/threat impact chains
2. `VULNERABLE_TO` (3,117,735) - Equipment/software vulnerabilities
3. `INSTALLED_ON` (968,125) - Software installation locations
4. `TRACKS_PROCESS` (344,256) - Process monitoring
5. `MONITORS_EQUIPMENT` (289,233) - Equipment monitoring
6. `AFFECTS` (245,871) - CVE affects software/equipment
7. `SBOM_CONTAINS` (234,677) - SBOM component relationships
8. `HAS_DEPENDENCY` (198,451) - Software dependencies
9. `GENERATES_MEASUREMENT` (156,234) - Equipment measurements
10. `EXPLOITS` (123,456) - Threat exploitation patterns

---

## 🔍 Common Query Patterns

### 1. Query Equipment by Sector

**Find all Energy sector equipment**:
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'ENERGY'
RETURN e.name, e.type, e.manufacturer, e.model
ORDER BY e.name
LIMIT 50
```

**Find equipment by subsector**:
```cypher
MATCH (e:Equipment)
WHERE e.subsector = 'Energy_Transmission'
RETURN e.name, e.type, e.commissioned_date
ORDER BY e.commissioned_date DESC
```

**Python Example**:
```python
def get_equipment_by_sector(db, sector):
    query = """
    MATCH (e:Equipment)
    WHERE e.sector = $sector
    RETURN e.name as name, e.type as type, e.manufacturer as manufacturer
    ORDER BY e.name
    """
    return db.query(query, {"sector": sector})

# Usage
equipment = get_equipment_by_sector(db, "ENERGY")
for item in equipment:
    print(f"{item['name']} - {item['type']} by {item['manufacturer']}")
```

---

### 2. Query Vulnerabilities for Equipment

**Find all vulnerabilities affecting specific equipment**:
```cypher
MATCH (e:Equipment {name: 'Gas Turbine GT-100'})-[:VULNERABLE_TO]->(v:Vulnerability)
RETURN v.name, v.severity, v.cvss_score
ORDER BY v.cvss_score DESC
```

**Find equipment vulnerable to specific CVE**:
```cypher
MATCH (cve:CVE {id: 'CVE-2023-12345'})-[:AFFECTS]->(s:Software)-[:INSTALLED_ON]->(e:Equipment)
RETURN DISTINCT e.name, e.sector, s.name as software
```

**Python Example**:
```python
def get_equipment_vulnerabilities(db, equipment_name):
    query = """
    MATCH (e:Equipment {name: $equipment_name})-[:VULNERABLE_TO]->(v:Vulnerability)
    OPTIONAL MATCH (v)<-[:AFFECTS]-(cve:CVE)
    RETURN
        v.name as vulnerability,
        v.severity as severity,
        v.cvss_score as cvss_score,
        collect(cve.id) as cves
    ORDER BY v.cvss_score DESC
    """
    return db.query(query, {"equipment_name": equipment_name})
```

---

### 3. Query Control Systems

**Find all ICS/OT control systems**:
```cypher
MATCH (c:Control)
WHERE c.type CONTAINS 'ICS' OR c.type CONTAINS 'SCADA'
RETURN c.name, c.type, c.vendor, c.sector
LIMIT 50
```

**Find control systems for specific sector**:
```cypher
MATCH (c:Control)-[:CONTROLS]->(e:Equipment)
WHERE e.sector = 'WATER'
RETURN c.name, c.type, collect(e.name) as controlled_equipment
```

**Python Example**:
```python
def get_sector_control_systems(db, sector):
    query = """
    MATCH (c:Control)-[:CONTROLS]->(e:Equipment)
    WHERE e.sector = $sector
    RETURN
        c.name as control_system,
        c.type as type,
        count(e) as equipment_count,
        collect(e.name)[0..5] as sample_equipment
    ORDER BY equipment_count DESC
    """
    return db.query(query, {"sector": sector})
```

---

### 4. Multi-Hop Relationship Queries

**3-Hop: Threat → Vulnerability → Equipment**:
```cypher
MATCH path = (t:Threat)-[:EXPLOITS]->(v:Vulnerability)-[:AFFECTS]->(e:Equipment)
WHERE e.sector = 'ENERGY'
RETURN
    t.name as threat,
    v.name as vulnerability,
    e.name as equipment,
    length(path) as hops
LIMIT 20
```

**5-Hop: APT → Malware → CVE → Software → Equipment**:
```cypher
MATCH path = (apt:ThreatActor)-[:USES]->(m:Malware)-[:EXPLOITS]->(cve:CVE)-[:AFFECTS]->(s:Software)-[:INSTALLED_ON]->(e:Equipment)
WHERE apt.name CONTAINS 'APT'
RETURN
    apt.name as threat_actor,
    m.name as malware,
    cve.id as cve,
    s.name as software,
    e.name as equipment,
    e.sector as sector,
    length(path) as hops
LIMIT 10
```

**Python Example**:
```python
def get_threat_to_equipment_chain(db, sector, max_hops=5):
    query = """
    MATCH path = (t:Threat)-[*1..{max_hops}]->(e:Equipment)
    WHERE e.sector = $sector
    RETURN
        t.name as threat,
        [node in nodes(path) | labels(node)[0]] as node_types,
        [rel in relationships(path) | type(rel)] as relationship_types,
        e.name as equipment,
        length(path) as hop_count
    ORDER BY hop_count
    LIMIT 20
    """.replace("{max_hops}", str(max_hops))

    return db.query(query, {"sector": sector})
```

---

### 5. Query Hierarchical Taxonomy

**Query by label patterns (sector-specific)**:
```cypher
// Find all Energy-related nodes
MATCH (n)
WHERE any(label IN labels(n) WHERE label STARTS WITH 'Energy')
RETURN labels(n) as labels, count(n) as count
ORDER BY count DESC
```

**Query multi-level hierarchy**:
```cypher
// Sector → Subsystem → Equipment → Measurement
MATCH (sector)-[:CONTAINS]->(subsystem)-[:CONTAINS]->(equipment)-[:GENERATES_MEASUREMENT]->(measurement)
WHERE 'ENERGY' IN labels(sector)
RETURN
    sector.name,
    subsystem.name,
    count(DISTINCT equipment) as equipment_count,
    count(measurement) as measurement_count
```

**Python Example**:
```python
def get_hierarchical_structure(db, sector_label):
    query = """
    MATCH (n)
    WHERE any(label IN labels(n) WHERE label STARTS WITH $sector_prefix)
    WITH n, labels(n) as node_labels
    RETURN
        node_labels,
        count(n) as count,
        collect(n.name)[0..3] as examples
    ORDER BY count DESC
    """

    return db.query(query, {"sector_prefix": sector_label})

# Usage
energy_hierarchy = get_hierarchical_structure(db, "Energy")
for level in energy_hierarchy:
    print(f"{level['node_labels']}: {level['count']} nodes")
    print(f"  Examples: {level['examples']}")
```

---

## 💼 Real Working Examples

### Example 1: Get All DAMS Equipment

**Cypher Query**:
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'DAMS' OR
      any(label IN labels(e) WHERE label STARTS WITH 'Dams')
RETURN
    e.name as equipment_name,
    e.type as equipment_type,
    labels(e) as all_labels,
    e.manufacturer as manufacturer,
    e.commissioned_date as commissioned
ORDER BY e.name
LIMIT 50
```

**Python Function**:
```python
def get_dams_equipment(db):
    """Get all DAMS sector equipment with details"""
    query = """
    MATCH (e:Equipment)
    WHERE e.sector = 'DAMS' OR
          any(label IN labels(e) WHERE label STARTS WITH 'Dams')
    OPTIONAL MATCH (e)-[:VULNERABLE_TO]->(v:Vulnerability)
    OPTIONAL MATCH (e)-[:GENERATES_MEASUREMENT]->(m:Measurement)
    RETURN
        e.name as equipment_name,
        e.type as equipment_type,
        e.manufacturer as manufacturer,
        count(DISTINCT v) as vulnerability_count,
        count(DISTINCT m) as measurement_count,
        labels(e) as labels
    ORDER BY vulnerability_count DESC, equipment_name
    """

    results = db.query(query)

    # Format results
    equipment_list = []
    for record in results:
        equipment_list.append({
            "name": record["equipment_name"],
            "type": record["equipment_type"],
            "manufacturer": record["manufacturer"],
            "vulnerabilities": record["vulnerability_count"],
            "measurements": record["measurement_count"],
            "labels": record["labels"]
        })

    return equipment_list

# Usage
dams_equipment = get_dams_equipment(db)
for equip in dams_equipment:
    print(f"{equip['name']} ({equip['type']})")
    print(f"  Manufacturer: {equip['manufacturer']}")
    print(f"  Vulnerabilities: {equip['vulnerabilities']}")
    print(f"  Measurements: {equip['measurements']}")
    print()
```

**JavaScript/React Example**:
```javascript
async function getDamsEquipment() {
    const db = new AEONDatabase();

    const query = `
        MATCH (e:Equipment)
        WHERE e.sector = 'DAMS' OR
              any(label IN labels(e) WHERE label STARTS WITH 'Dams')
        OPTIONAL MATCH (e)-[:VULNERABLE_TO]->(v:Vulnerability)
        RETURN
            e.name as equipment_name,
            e.type as equipment_type,
            count(v) as vulnerability_count
        ORDER BY vulnerability_count DESC
        LIMIT 50
    `;

    const results = await db.query(query);
    await db.close();

    return results.map(r => ({
        name: r.equipment_name,
        type: r.equipment_type,
        vulnerabilityCount: r.vulnerability_count
    }));
}

// React component
function DamsEquipmentList() {
    const [equipment, setEquipment] = useState([]);

    useEffect(() => {
        getDamsEquipment().then(setEquipment);
    }, []);

    return (
        <div>
            <h2>DAMS Equipment</h2>
            <ul>
                {equipment.map((item, idx) => (
                    <li key={idx}>
                        {item.name} - {item.type}
                        <span className="badge">{item.vulnerabilityCount} vulnerabilities</span>
                    </li>
                ))}
            </ul>
        </div>
    );
}
```

---

### Example 2: Get Power Generation Chain

**Cypher Query**:
```cypher
MATCH path = (source:Equipment)-[:POWERS|TRANSMITS*1..5]->(destination:Equipment)
WHERE source.type CONTAINS 'Generator' OR source.type CONTAINS 'Turbine'
  AND any(label IN labels(source) WHERE label STARTS WITH 'Energy')
RETURN
    source.name as power_source,
    [node in nodes(path)[1..-1] | node.name] as transmission_chain,
    destination.name as final_destination,
    length(path) as chain_length
ORDER BY chain_length DESC
LIMIT 20
```

**Python Function**:
```python
def get_power_generation_chain(db, source_type='Generator'):
    """Get power generation and transmission chains"""
    query = """
    MATCH path = (source:Equipment)-[:POWERS|TRANSMITS*1..5]->(destination:Equipment)
    WHERE (source.type CONTAINS $source_type OR source.type CONTAINS 'Turbine')
      AND any(label IN labels(source) WHERE label STARTS WITH 'Energy')
    WITH path, source, destination
    RETURN
        source.name as power_source,
        source.type as source_type,
        [node in nodes(path) | node.name] as full_chain,
        [rel in relationships(path) | type(rel)] as relationship_types,
        destination.name as final_destination,
        destination.type as destination_type,
        length(path) as chain_length
    ORDER BY chain_length DESC
    LIMIT 20
    """

    results = db.query(query, {"source_type": source_type})

    # Format as chain visualization
    chains = []
    for record in results:
        chain = {
            "source": {
                "name": record["power_source"],
                "type": record["source_type"]
            },
            "path": record["full_chain"],
            "relationships": record["relationship_types"],
            "destination": {
                "name": record["final_destination"],
                "type": record["destination_type"]
            },
            "hops": record["chain_length"]
        }
        chains.append(chain)

    return chains

# Usage
chains = get_power_generation_chain(db, source_type='Turbine')
for chain in chains:
    print(f"\n{chain['source']['name']} ({chain['source']['type']})")
    print(f"  Chain: {' → '.join(chain['path'])}")
    print(f"  Relationships: {' → '.join(chain['relationships'])}")
    print(f"  Destination: {chain['destination']['name']} ({chain['destination']['type']})")
    print(f"  Total Hops: {chain['hops']}")
```

---

### Example 3: Get Threats Targeting Specific Equipment

**Cypher Query**:
```cypher
MATCH path = (t:Threat)-[*1..4]->(e:Equipment {name: 'Gas Turbine GT-100'})
RETURN
    t.name as threat,
    t.type as threat_type,
    t.severity as severity,
    [node in nodes(path)[1..-1] | labels(node)[0] + ': ' + node.name] as attack_path,
    length(path) as path_length
ORDER BY t.severity DESC, path_length
LIMIT 10
```

**Python Function**:
```python
def get_threats_targeting_equipment(db, equipment_name, max_hops=4):
    """Get all threats targeting specific equipment"""
    query = """
    MATCH path = (t:Threat)-[*1..{max_hops}]->(e:Equipment {{name: $equipment_name}})
    RETURN
        t.name as threat_name,
        t.type as threat_type,
        t.severity as severity,
        [node in nodes(path)[1..-1] | {{
            label: labels(node)[0],
            name: node.name,
            type: node.type
        }}] as attack_path,
        [rel in relationships(path) | type(rel)] as relationships,
        length(path) as hop_count
    ORDER BY t.severity DESC, hop_count
    """.replace("{max_hops}", str(max_hops))

    results = db.query(query, {"equipment_name": equipment_name})

    # Format results
    threats = []
    for record in results:
        threat = {
            "name": record["threat_name"],
            "type": record["threat_type"],
            "severity": record["severity"],
            "attack_chain": record["attack_path"],
            "relationship_types": record["relationships"],
            "hops": record["hop_count"]
        }
        threats.append(threat)

    return threats

# Usage
threats = get_threats_targeting_equipment(db, "Gas Turbine GT-100")
print(f"\nThreats targeting Gas Turbine GT-100:\n")
for threat in threats:
    print(f"Threat: {threat['name']} ({threat['type']}) - Severity: {threat['severity']}")
    print(f"  Attack Chain ({threat['hops']} hops):")
    for i, node in enumerate(threat['attack_chain']):
        rel = threat['relationship_types'][i] if i < len(threat['relationship_types']) else ''
        print(f"    {i+1}. {node['label']}: {node['name']} ({node.get('type', 'N/A')})")
        if rel:
            print(f"       └─[{rel}]→")
    print()
```

---

### Example 4: Get Measurements for Equipment

**Cypher Query**:
```cypher
MATCH (e:Equipment {name: 'Gas Turbine GT-100'})-[:GENERATES_MEASUREMENT]->(m:Measurement)
OPTIONAL MATCH (m)-[:PART_OF]->(ts:TimeSeries)
RETURN
    m.name as measurement_name,
    m.type as measurement_type,
    m.value as current_value,
    m.unit as unit,
    m.timestamp as timestamp,
    m.threshold_exceeded as alert_status,
    ts.name as timeseries_name
ORDER BY m.timestamp DESC
LIMIT 100
```

**Python Function**:
```python
def get_equipment_measurements(db, equipment_name, limit=100):
    """Get all measurements for specific equipment"""
    query = """
    MATCH (e:Equipment {name: $equipment_name})-[:GENERATES_MEASUREMENT]->(m:Measurement)
    OPTIONAL MATCH (m)-[:PART_OF]->(ts:TimeSeries)
    OPTIONAL MATCH (e)<-[:MONITORS_EQUIPMENT]-(mon:Monitoring)
    RETURN
        m.name as measurement_name,
        m.type as measurement_type,
        m.value as current_value,
        m.unit as unit,
        m.timestamp as timestamp,
        m.threshold_exceeded as alert_status,
        ts.name as timeseries_name,
        mon.frequency as monitoring_frequency
    ORDER BY m.timestamp DESC
    LIMIT $limit
    """

    results = db.query(query, {
        "equipment_name": equipment_name,
        "limit": limit
    })

    # Group measurements by type
    measurements_by_type = {}
    for record in results:
        meas_type = record["measurement_type"] or "UNKNOWN"

        if meas_type not in measurements_by_type:
            measurements_by_type[meas_type] = []

        measurements_by_type[meas_type].append({
            "name": record["measurement_name"],
            "value": record["current_value"],
            "unit": record["unit"],
            "timestamp": record["timestamp"],
            "alert": record["alert_status"],
            "timeseries": record["timeseries_name"],
            "frequency": record["monitoring_frequency"]
        })

    return measurements_by_type

# Usage
measurements = get_equipment_measurements(db, "Gas Turbine GT-100", limit=50)

for meas_type, values in measurements.items():
    print(f"\n{meas_type} Measurements:")
    for m in values[:5]:  # Show first 5
        alert = " ⚠️ ALERT" if m['alert'] else ""
        print(f"  {m['name']}: {m['value']} {m['unit']} at {m['timestamp']}{alert}")
    if len(values) > 5:
        print(f"  ... and {len(values) - 5} more")
```

---

## 🔐 Authentication & Security

### Neo4j Authentication

**Default Credentials** (CHANGE IN PRODUCTION):
```python
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j@openspg"
```

**Security Best Practices**:

1. **Environment Variables**:
```python
import os
from neo4j import GraphDatabase

class SecureNeo4jConnection:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")

        if not self.password:
            raise ValueError("NEO4J_PASSWORD environment variable not set")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )
```

2. **.env File**:
```bash
# .env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-secure-password-here
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

3. **Python with python-dotenv**:
```python
from dotenv import load_dotenv
import os

load_dotenv()

class ConfiguredDatabase:
    def __init__(self):
        self.neo4j_uri = os.getenv("NEO4J_URI")
        self.neo4j_user = os.getenv("NEO4J_USER")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.qdrant_host = os.getenv("QDRANT_HOST")
        self.qdrant_port = int(os.getenv("QDRANT_PORT", 6333))
```

---

### Qdrant Access

**No Authentication Required** (default local setup):
```python
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)
```

**Collection Access**:
```python
# Collection: aeon-actual-system
COLLECTION_NAME = "aeon-actual-system"

# Check if collection exists
collections = client.get_collections()
collection_names = [c.name for c in collections.collections]

if COLLECTION_NAME in collection_names:
    print(f"✅ Collection '{COLLECTION_NAME}' is available")
else:
    print(f"❌ Collection '{COLLECTION_NAME}' not found")
```

---

## ⚡ Performance Tips

### 1. Use Parameterized Queries

**Bad** (vulnerable to injection):
```python
# DON'T DO THIS
sector = "ENERGY"
query = f"MATCH (e:Equipment) WHERE e.sector = '{sector}' RETURN e"
```

**Good** (parameterized):
```python
# DO THIS
query = "MATCH (e:Equipment) WHERE e.sector = $sector RETURN e"
results = db.query(query, {"sector": sector})
```

---

### 2. Limit Result Sets

**Always use LIMIT**:
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'ENERGY'
RETURN e
LIMIT 100  -- Always limit results
```

---

### 3. Use Indexes (Database Level)

**Create indexes** on frequently queried properties:
```cypher
CREATE INDEX equipment_sector IF NOT EXISTS FOR (e:Equipment) ON (e.sector);
CREATE INDEX cve_id IF NOT EXISTS FOR (c:CVE) ON (c.id);
CREATE INDEX vulnerability_severity IF NOT EXISTS FOR (v:Vulnerability) ON (v.severity);
```

---

### 4. Optimize Multi-Hop Queries

**Limit path depth**:
```cypher
MATCH path = (t:Threat)-[*1..5]->(e:Equipment)  -- Limit to 5 hops max
WHERE e.sector = 'ENERGY'
RETURN path
LIMIT 20
```

---

### 5. Connection Pooling

**Reuse database connections**:
```python
# Bad: Create new connection for each query
def query_data():
    db = Neo4jConnection()
    db.connect()
    results = db.query("MATCH (n) RETURN n LIMIT 10")
    db.close()
    return results

# Good: Reuse connection
class DatabaseService:
    def __init__(self):
        self.db = Neo4jConnection()
        self.db.connect()

    def query(self, cypher, params=None):
        return self.db.query(cypher, params)

    def close(self):
        self.db.close()

# Create once, use many times
db_service = DatabaseService()
results1 = db_service.query("MATCH (e:Equipment) RETURN e LIMIT 10")
results2 = db_service.query("MATCH (c:CVE) RETURN c LIMIT 10")
db_service.close()
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Connection Refused

**Error**:
```
neo4j.exceptions.ServiceUnavailable: Cannot connect to bolt://localhost:7687
```

**Solution**:
```bash
# Check if Neo4j is running
sudo systemctl status neo4j

# Start Neo4j if not running
sudo systemctl start neo4j

# Check port is listening
netstat -tuln | grep 7687
```

---

#### 2. Authentication Failed

**Error**:
```
neo4j.exceptions.AuthError: The client is unauthorized
```

**Solution**:
```python
# Verify credentials
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j@openspg"  # Check this password

# Test connection
from neo4j import GraphDatabase
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
with driver.session() as session:
    result = session.run("RETURN 1 as test")
    print(result.single()["test"])
driver.close()
```

---

#### 3. Query Timeout

**Error**:
```
TransientError: Query execution timed out
```

**Solution**:
```python
# Add timeout configuration
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "neo4j@openspg"),
    max_connection_lifetime=3600,
    connection_timeout=30,
    max_transaction_retry_time=15
)

# Or limit query complexity
query = """
MATCH (e:Equipment)
WHERE e.sector = $sector
RETURN e
LIMIT 100  -- Add limit
"""
```

---

#### 4. Empty Results

**Issue**: Query returns no results

**Debug Steps**:
```python
# 1. Check node count
result = db.query("MATCH (n:Equipment) RETURN count(n) as count")
print(f"Total Equipment nodes: {result[0]['count']}")

# 2. Check property existence
result = db.query("""
    MATCH (e:Equipment)
    WHERE e.sector IS NOT NULL
    RETURN count(e) as with_sector, count(*) as total
""")
print(f"Equipment with sector: {result[0]['with_sector']} / {result[0]['total']}")

# 3. Sample actual data
result = db.query("""
    MATCH (e:Equipment)
    RETURN e
    LIMIT 5
""")
for node in result:
    print(node)
```

---

#### 5. Qdrant Collection Not Found

**Error**:
```
Collection 'aeon-actual-system' not found
```

**Solution**:
```python
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

# List all collections
collections = client.get_collections()
print("Available collections:")
for collection in collections.collections:
    print(f"  - {collection.name}")

# Create collection if missing
if "aeon-actual-system" not in [c.name for c in collections.collections]:
    print("Collection not found. Run store_schema_in_qdrant.py to create it.")
```

---

## 📚 Additional Resources

### Documentation Files

- **[ACTUAL_SCHEMA_IMPLEMENTED.md](ACTUAL_SCHEMA_IMPLEMENTED.md)** - Complete schema documentation
- **[RELATIONSHIP_ONTOLOGY.md](RELATIONSHIP_ONTOLOGY.md)** - All relationship types
- **[20_HOP_VERIFICATION.md](20_HOP_VERIFICATION.md)** - Multi-hop reasoning examples
- **[VALIDATION_QUERIES.cypher](../validation_results/VALIDATION_QUERIES.cypher)** - Sample validation queries

### Scripts

- **[extract_actual_schema.py](../scripts/extract_actual_schema.py)** - Extract schema from database
- **[store_schema_in_qdrant.py](../scripts/store_schema_in_qdrant.py)** - Populate Qdrant collection

### External Resources

- **Neo4j Documentation**: https://neo4j.com/docs/
- **Neo4j Python Driver**: https://neo4j.com/docs/python-manual/current/
- **Neo4j JavaScript Driver**: https://neo4j.com/docs/javascript-manual/current/
- **Qdrant Documentation**: https://qdrant.tech/documentation/
- **Cypher Query Language**: https://neo4j.com/docs/cypher-manual/current/

---

## 🎯 Quick Reference Card

### Connection Details

```
Neo4j Browser:   http://localhost:7474
Bolt URL:        bolt://localhost:7687
Username:        neo4j
Password:        neo4j@openspg
Database:        neo4j

Qdrant:          http://localhost:6333
Collection:      aeon-actual-system
```

### Essential Queries

```cypher
// Count all nodes
MATCH (n) RETURN count(n)

// List all labels
CALL db.labels()

// List all relationship types
CALL db.relationshipTypes()

// Get equipment by sector
MATCH (e:Equipment) WHERE e.sector = 'ENERGY' RETURN e LIMIT 10

// Get vulnerabilities
MATCH (v:Vulnerability) WHERE v.severity = 'CRITICAL' RETURN v LIMIT 10

// Multi-hop threat chain
MATCH path = (t:Threat)-[*1..3]->(e:Equipment) RETURN path LIMIT 5
```

---

**END OF FRONTEND DEVELOPER GUIDE**

**Version:** 1.0.0
**Last Updated:** 2025-12-12
**Status:** ✅ PRODUCTION-READY
