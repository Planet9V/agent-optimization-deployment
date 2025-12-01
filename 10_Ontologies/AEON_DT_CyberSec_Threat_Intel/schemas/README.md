# AEON Digital Twin Cyber Security Threat Intelligence - Neo4j Graph Schema

Complete Neo4j graph database schema for railway digital twin cybersecurity analysis.

## Version: 1.0.0
## Created: 2025-10-29

## Overview

This schema provides a comprehensive graph model for:
- Railway infrastructure digital twins (organizations, sites, trains, components)
- Operational Technology (OT) and Industrial Control Systems (ICS)
- Network topology and security controls
- Cybersecurity threat intelligence (CVEs, threat actors, campaigns)
- Attack path analysis and risk assessment

## Schema Statistics

- **Node Types**: 15
- **Relationship Types**: 25
- **Unique Constraints**: 15
- **Property Indexes**: 60+
- **Full-Text Indexes**: 5

### Sample Data (04_sample_data.cypher)
- Organizations: 3
- Sites: 10
- Trains: 20
- Components: 100
- Software: 200
- Libraries: 50
- Network Interfaces: 150
- Network Segments: 20
- Firewall Rules: 50
- Protocols: 10
- CVEs: 500
- Threat Actors: 10
- Campaigns: 5
- Attack Techniques: 20
- Documents: 10
- **Total Nodes**: ~1,148
- **Total Relationships**: ~2,000+

## Directory Structure

```
schemas/
├── cypher/                          # Cypher scripts for Neo4j
│   ├── 01_constraints_indexes.cypher   # Constraints and indexes
│   ├── 02_node_definitions.cypher      # Node type definitions
│   ├── 03_relationship_definitions.cypher  # Relationship definitions
│   ├── 04_sample_data.cypher           # Sample dataset
│   └── 99_complete_schema.cypher       # Complete deployment script
│
├── json/                            # JSON schema exports
│   ├── schema_complete.json            # Complete schema definition
│   ├── node_types.json                 # Node type catalog
│   └── relationship_types.json         # Relationship catalog
│
├── validation/                      # Validation tools
│   ├── schema_validator.py             # Schema validation script
│   └── gap_analyzer.py                 # Gap analysis tool
│
└── README.md                        # This file
```

## Quick Start

### Option 1: Deploy Complete Schema with Sample Data

```bash
# Deploy all schema components in sequence
cypher-shell -u neo4j -p password < cypher/01_constraints_indexes.cypher
cypher-shell -u neo4j -p password < cypher/04_sample_data.cypher
```

### Option 2: Deploy via Single Script

```bash
# Use the complete deployment script
cypher-shell -u neo4j -p password < cypher/99_complete_schema.cypher
```

### Option 3: Deploy via Neo4j Browser

1. Open Neo4j Browser
2. Copy contents of each script
3. Execute in order:
   - 01_constraints_indexes.cypher
   - 04_sample_data.cypher

## Node Types

### Infrastructure & Assets
1. **Organization** - Railway operators, manufacturers, regulators
2. **Site** - Physical locations (stations, depots, control centers)
3. **Train** - Train sets and rolling stock
4. **Component** - Hardware/software components (PLC, SCADA, sensors)
5. **Software** - Operating systems, applications, firmware
6. **Library** - Software libraries and dependencies

### Network & Security
7. **NetworkInterface** - Network interfaces on components
8. **NetworkSegment** - Network zones and segments
9. **FirewallRule** - Firewall rules protecting segments
10. **Protocol** - Industrial and network protocols

### Threat Intelligence
11. **CVE** - Common Vulnerabilities and Exposures
12. **ThreatActor** - Adversary groups and threat actors
13. **Campaign** - Coordinated threat campaigns
14. **AttackTechnique** - MITRE ATT&CK techniques
15. **Document** - Security documents and reports

## Key Relationship Types

### Infrastructure Relationships
- **OPERATES**: Organization → Site
- **HOSTS**: Site → Train
- **HAS_COMPONENT**: Train/Site → Component
- **RUNS_SOFTWARE**: Component → Software
- **DEPENDS_ON**: Software → Library

### Network Relationships
- **HAS_INTERFACE**: Component → NetworkInterface
- **BELONGS_TO**: NetworkInterface → NetworkSegment
- **CONNECTS_TO**: NetworkSegment → NetworkSegment
- **PROTECTED_BY**: NetworkSegment → FirewallRule
- **USES_PROTOCOL**: Component → Protocol

### Security Relationships
- **HAS_VULNERABILITY**: Software/Component/Library → CVE
- **EXPLOITS**: ThreatActor → CVE
- **TARGETS**: ThreatActor → Organization
- **CONDUCTS**: ThreatActor → Campaign
- **USES**: ThreatActor/Campaign → AttackTechnique

### Analysis Relationships
- **ATTACK_PATH_STEP**: NetworkSegment/Component → NetworkSegment/Component
- **MITIGATES**: FirewallRule/Component → CVE/ThreatActor
- **MONITORS**: Component → Component/NetworkSegment
- **REQUIRES_UPDATE**: Component/Software → CVE

## Validation

### Schema Validator

Validates schema completeness and consistency:

```bash
cd validation/
python3 schema_validator.py bolt://localhost:7687 neo4j password
```

Checks:
- All constraints exist
- All indexes created
- All node types present
- All relationship types exist
- Data integrity (IDs, formats, orphaned nodes)

### Gap Analyzer

Identifies missing schema elements and generates remediation:

```bash
cd validation/
python3 gap_analyzer.py bolt://localhost:7687 neo4j password
```

Outputs:
- Gap analysis report
- Remediation Cypher script
- JSON results file

## Sample Queries

### Find Critical Components with Vulnerabilities
```cypher
MATCH (comp:Component)-[:HAS_VULNERABILITY]->(cve:CVE)
WHERE comp.criticalityLevel = 'critical' AND cve.severity = 'critical'
RETURN comp.name, comp.riskScore, cve.id, cve.cvssScore
ORDER BY comp.riskScore DESC, cve.cvssScore DESC;
```

### Trace Attack Paths to Critical Components
```cypher
MATCH path = (start:NetworkSegment)-[:ATTACK_PATH_STEP*]->(target:Component)
WHERE start.securityZone = 'public' AND target.criticalityLevel = 'critical'
RETURN path, length(path) AS PathLength
ORDER BY PathLength
LIMIT 10;
```

### Identify Active Threat Actors Targeting Organization
```cypher
MATCH (ta:ThreatActor)-[t:TARGETS]->(org:Organization)
WHERE org.id = 'ORG-001' AND t.isActive = true
RETURN ta.name, ta.sophisticationLevel, ta.primaryMotivation, t.lastActivity
ORDER BY ta.sophisticationLevel DESC;
```

### Find Unpatched Critical Vulnerabilities
```cypher
MATCH (sw:Software)-[hv:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.severity = 'critical' AND hv.mitigationStatus <> 'patched'
RETURN sw.name, sw.version, cve.id, cve.cvssScore, cve.description
ORDER BY cve.cvssScore DESC;
```

### Network Segmentation Analysis
```cypher
MATCH (ns:NetworkSegment)-[:CONNECTS_TO]->(ns2:NetworkSegment)
WHERE ns.securityZone <> ns2.securityZone
RETURN ns.name AS From, ns.securityZone AS FromZone,
       ns2.name AS To, ns2.securityZone AS ToZone
ORDER BY ns.securityZone, ns2.securityZone;
```

## Performance Tuning

### Recommended Neo4j Settings

```properties
# Memory settings
dbms.memory.heap.initial_size=2G
dbms.memory.heap.max_size=4G
dbms.memory.pagecache.size=4G

# Query logging
dbms.logs.query.enabled=true
dbms.logs.query.threshold=1s

# Transaction settings
dbms.transaction.timeout=60s
```

### Monitoring

```cypher
// Check database statistics
CALL db.stats.retrieve('QUERIES');

// Monitor index usage
CALL db.indexes() YIELD name, state, populationPercent;

// Check constraint status
SHOW CONSTRAINTS;
```

## Backup and Restore

### Create Backup
```bash
neo4j-admin dump --database=neo4j --to=/backups/aeon-dt-$(date +%Y%m%d).dump
```

### Restore Backup
```bash
neo4j-admin load --from=/backups/aeon-dt-20251029.dump --database=neo4j --force
```

## Integration

### Python Integration

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

with driver.session() as session:
    result = session.run("""
        MATCH (comp:Component)-[:HAS_VULNERABILITY]->(cve:CVE)
        WHERE cve.severity = 'critical'
        RETURN comp.name, cve.id, cve.cvssScore
        ORDER BY cve.cvssScore DESC
        LIMIT 10
    """)

    for record in result:
        print(f"{record['comp.name']}: {record['cve.id']} (Score: {record['cve.cvssScore']})")

driver.close()
```

### REST API Integration

```bash
# Query via HTTP API
curl -X POST http://localhost:7474/db/neo4j/tx/commit \
  -H "Content-Type: application/json" \
  -u neo4j:password \
  -d '{
    "statements": [{
      "statement": "MATCH (n:CVE) WHERE n.severity = $severity RETURN n LIMIT 10",
      "parameters": {"severity": "critical"}
    }]
  }'
```

## Support

For issues or questions:
- Review sample queries in `99_complete_schema.cypher`
- Run validation: `python3 validation/schema_validator.py`
- Check Neo4j logs: `logs/neo4j.log`

## Version History

- **1.0.0** (2025-10-29): Initial complete schema release
  - 15 node types
  - 25 relationship types
  - Complete sample data
  - Validation tooling

## License

AEON Digital Twin Cyber Security Threat Intelligence Schema
Copyright 2025
