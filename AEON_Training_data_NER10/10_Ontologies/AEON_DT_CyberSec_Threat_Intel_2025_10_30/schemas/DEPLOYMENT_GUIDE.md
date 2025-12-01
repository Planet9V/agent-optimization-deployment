# AEON Digital Twin Cyber Security - Neo4j Deployment Guide

## Quick Deployment

### Prerequisites
- Neo4j 5.x installed and running
- cypher-shell CLI tool
- Python 3.8+ (for validation tools)
- neo4j Python driver: `pip install neo4j`

### Step 1: Deploy Schema (Choose One Method)

#### Method A: Complete Single-Script Deployment
```bash
# Deploy everything in one command
cypher-shell -u neo4j -p YOUR_PASSWORD < cypher/99_complete_schema.cypher
cypher-shell -u neo4j -p YOUR_PASSWORD < cypher/04_sample_data.cypher
```

#### Method B: Step-by-Step Deployment
```bash
# 1. Create constraints and indexes
cypher-shell -u neo4j -p YOUR_PASSWORD < cypher/01_constraints_indexes.cypher

# 2. Load sample data (includes node definitions)
cypher-shell -u neo4j -p YOUR_PASSWORD < cypher/04_sample_data.cypher

# 3. Verify deployment
cypher-shell -u neo4j -p YOUR_PASSWORD -f cypher <<EOF
MATCH (n) RETURN labels(n)[0] AS NodeType, count(*) AS Count ORDER BY Count DESC;
EOF
```

#### Method C: Neo4j Browser (GUI)
1. Open Neo4j Browser: http://localhost:7474
2. Login with credentials
3. Copy and paste each script:
   - `01_constraints_indexes.cypher`
   - `04_sample_data.cypher`
4. Execute each script

### Step 2: Verify Deployment

```bash
# Run schema validator
cd validation/
python3 schema_validator.py bolt://localhost:7687 neo4j YOUR_PASSWORD

# Expected output:
# ✓ CONSTRAINTS: 15/15 valid
# ✓ INDEXES: 60+/60+ valid
# ✓ NODE TYPES: 15/15 valid
# ✓ RELATIONSHIP TYPES: 25/25 valid
# ✓ DATA INTEGRITY: Valid
```

### Step 3: Run Sample Queries

```bash
# Test critical vulnerability query
cypher-shell -u neo4j -p YOUR_PASSWORD -f cypher <<EOF
MATCH (comp:Component)-[:HAS_VULNERABILITY]->(cve:CVE)
WHERE comp.criticalityLevel = 'critical' AND cve.severity = 'critical'
RETURN comp.name, cve.id, cve.cvssScore
ORDER BY cve.cvssScore DESC
LIMIT 5;
EOF
```

Expected Results:
```
+--------------------------------------------------------+
| comp.name              | cve.id          | cvssScore |
+--------------------------------------------------------+
| Train Control System   | CVE-2021-44228  | 10.0      |
| ...                    | ...             | ...       |
+--------------------------------------------------------+
```

## Troubleshooting

### Issue: "Constraint already exists"
**Solution**: Schema is already deployed. Run gap analyzer to check completeness:
```bash
cd validation/
python3 gap_analyzer.py bolt://localhost:7687 neo4j YOUR_PASSWORD
```

### Issue: "Database not empty"
**Solution**: Clear database first:
```bash
cypher-shell -u neo4j -p YOUR_PASSWORD -f cypher <<EOF
MATCH (n) DETACH DELETE n;
EOF
```
**Warning**: This deletes ALL data!

### Issue: Python validation fails
**Solution**: Install dependencies:
```bash
pip install neo4j
```

### Issue: Connection refused
**Solution**: Ensure Neo4j is running:
```bash
# Check status
neo4j status

# Start Neo4j
neo4j start

# Verify connection
cypher-shell -u neo4j -p YOUR_PASSWORD "RETURN 'Connected!' as status;"
```

## Schema Statistics (After Full Deployment)

### Node Counts
```
Organizations: 3
Sites: 10
Trains: 20
Components: 100
Software: 200
Libraries: 50
Network Interfaces: 150
Network Segments: 20
Firewall Rules: 50
Protocols: 10
CVEs: 500
Threat Actors: 10
Campaigns: 5
Attack Techniques: 20
Documents: 10
-------------------
TOTAL: ~1,148 nodes
```

### Relationship Counts
```
~2,000+ relationships across 25 types
```

### Performance Metrics
```
Schema Constraints: 15
Property Indexes: 60+
Full-Text Indexes: 5
Composite Indexes: 3
```

## Customization

### Load Your Own Data

```cypher
// Example: Add your organization
CREATE (org:Organization {
  id: 'ORG-CUSTOM-001',
  name: 'Your Railway Company',
  type: 'operator',
  country: 'Your Country',
  // ... other properties
});

// Connect to existing sites
MATCH (org:Organization {id: 'ORG-CUSTOM-001'}),
      (site:Site {id: 'SITE-001'})
CREATE (org)-[:OPERATES {since: date()}]->(site);
```

### Add Custom CVE Data

```cypher
// Example: Add specific CVE
CREATE (cve:CVE {
  id: 'CVE-2024-12345',
  description: 'Your CVE description',
  severity: 'high',
  cvssScore: 8.5,
  // ... other properties
});

// Link to affected software
MATCH (sw:Software {id: 'SW-001'}),
      (cve:CVE {id: 'CVE-2024-12345'})
CREATE (sw)-[:HAS_VULNERABILITY {
  discoveredDate: date(),
  mitigationStatus: 'active'
}]->(cve);
```

## Maintenance

### Regular Validation
```bash
# Run weekly
cd validation/
python3 schema_validator.py bolt://localhost:7687 neo4j YOUR_PASSWORD > validation_$(date +%Y%m%d).txt
```

### Backup Schedule
```bash
# Daily backups
neo4j-admin dump --database=neo4j --to=/backups/aeon-dt-$(date +%Y%m%d).dump

# Keep 30 days of backups
find /backups -name "aeon-dt-*.dump" -mtime +30 -delete
```

### Performance Monitoring
```cypher
// Check query performance
CALL db.stats.retrieve('QUERIES');

// Monitor index usage
CALL db.indexes() YIELD name, state, populationPercent;

// Check memory usage
CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Memory Pools')
YIELD attributes
RETURN attributes.HeapMemoryUsage.value;
```

## Next Steps

1. **Explore Sample Queries**: See README.md for 10+ sample queries
2. **Customize Schema**: Add organization-specific node types or properties
3. **Integrate Applications**: Use Python/REST API examples in README.md
4. **Set Up Monitoring**: Configure performance dashboards
5. **Plan Updates**: Schedule regular CVE data updates

## Support Resources

- **Documentation**: See README.md for complete reference
- **Sample Queries**: 99_complete_schema.cypher contains verification queries
- **Validation Tools**: Use schema_validator.py and gap_analyzer.py
- **Neo4j Docs**: https://neo4j.com/docs/

## Contact

For issues with this schema deployment:
1. Run validation tools to identify gaps
2. Check Neo4j logs: `logs/neo4j.log`
3. Verify Neo4j version compatibility (5.x required)
