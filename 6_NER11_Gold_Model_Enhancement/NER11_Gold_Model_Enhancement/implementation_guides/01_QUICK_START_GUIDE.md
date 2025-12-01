# Quick Start Implementation Guide

**Audience**: Developers & Architects  
**Time to Complete**: 1-2 hours  
**Prerequisites**: Access to Neo4j instance, NER11 model deployed

---

## Step 1: Review Current State (15 minutes)

### Check Neo4j Version
```bash
# Ensure Neo4j 5.x or higher
docker exec neo4j cypher-shell "CALL dbms.components() YIELD versions RETURN versions"
```

### Verify NER11 Model
```bash
cd /home/jim/2_OXOT_Projects_Dev/NER11_Gold_Model
python scripts/test_model.py
```

---

## Step 2: Create Schema v3.1 (30 minutes)

### Run Schema Migration Script

```cypher
// Create new node labels
CREATE CONSTRAINT psych_trait_id IF NOT EXISTS FOR (n:PsychTrait) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT economic_metric_id IF NOT EXISTS FOR (n:EconomicMetric) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT protocol_id IF NOT EXISTS FOR (n:Protocol) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT role_id IF NOT EXISTS FOR (n:Role) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT software_id IF NOT EXISTS FOR (n:Software) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT control_id IF NOT EXISTS FOR (n:Control) REQUIRE n.id IS UNIQUE;

// Create composite indexes
CREATE INDEX asset_class_device IF NOT EXISTS FOR (n:Asset) ON (n.assetClass, n.deviceType);
CREATE INDEX psych_trait_subtype IF NOT EXISTS FOR (n:PsychTrait) ON (n.traitType, n.subtype);
CREATE INDEX malware_family IF NOT EXISTS FOR (n:Malware) ON (n.malwareFamily);
CREATE INDEX economic_metric_type IF NOT EXISTS FOR (n:EconomicMetric) ON (n.metricType, n.category);
```

---

## Step 3: Test Entity Mapping (20 minutes)

### Create Test Nodes

```python
from scripts.neo4j_integration import NER11Neo4jIntegrator

integrator = NER11Neo4jIntegrator(
    model_path="../NER11_Gold_Model/models/model-best",
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)

# Test text with diverse entity types
test_text = """
The CISO exhibited confirmation bias when dismissing the APT29 threat report.
The attack targeted Siemens S7-1500 PLCs using Modbus exploitation,
resulting in $2.5M in breach costs and a 15% stock price drop.
"""

result = integrator.process_and_ingest(test_text, create_relationships=True)
print(f"Entities extracted: {result['entity_count']}")
print(f"Nodes created: {result['nodes_created']}")
```

### Verify in Neo4j Browser

```cypher
// Check PsychTrait nodes
MATCH (p:PsychTrait)
RETURN p.name, p.traitType, p.subtype
LIMIT 10;

// Check Asset nodes with OT classification
MATCH (a:Asset)
WHERE a.assetClass = 'OT'
RETURN a.name, a.deviceType, a.vendor
LIMIT 10;

// Check EconomicMetric nodes
MATCH (em:EconomicMetric)
RETURN em.metricType, em.amount, em.currency
LIMIT 10;
```

---

## Step 4: Run Full Integration Test (15 minutes)

### Process Sample Threat Report

```python
threat_report = """
THREAT INTELLIGENCE BRIEFING - APT29 Energy Sector Campaign

Executive Summary:
APT29, a nation-state threat actor, conducted a sophisticated campaign
targeting critical infrastructure in the energy sector. The operation
exploited CVE-2023-12345 in Siemens S7-1500 PLCs via Modbus protocol.

Psychological Profile:
Analysis of threat actor communications reveals confirmation bias and
narcissistic personality traits, consistent with state-sponsored operations.

Financial Impact:
- Direct breach costs: $2.5M
- Stock price impact: -15% ($200M market cap loss)
- Recovery costs: $1.2M
- Regulatory fines: $500K (GDPR violations)

Technical Details:
- Target: Substations and SCADA systems
- Protocol: Modbus TCP (port 502)
- Malware: Custom ransomware variant
- Persistence: Scheduled tasks and registry modifications
"""

result = integrator.process_and_ingest(
    threat_report,
    source_doc="APT29_Energy_Campaign_2025.txt",
    create_relationships=True
)

print(f"✓ Processed {result['entity_count']} entities")
print(f"✓ Created {result['nodes_created']} nodes")
print(f"✓ Created {result['relationships_created']} relationships")
```

---

## Step 5: Validate Query Performance (10 minutes)

### Run Performance Benchmarks

```cypher
// Query 1: Find all OT assets (should use index)
PROFILE
MATCH (a:Asset)
WHERE a.assetClass = 'OT' AND a.deviceType = 'programmable_logic_controller'
RETURN count(a);
// Expected: <10ms with index

// Query 2: Find insider threats with psychological indicators
PROFILE
MATCH (u:User)-[:EXHIBITS]->(p:PsychTrait)
WHERE p.traitType = 'CognitiveBias'
RETURN u.username, collect(p.subtype) as biases;
// Expected: <50ms

// Query 3: Calculate total breach costs
PROFILE
MATCH (em:EconomicMetric)
WHERE em.metricType = 'Loss'
RETURN sum(em.amount) as total_loss, count(em) as incidents;
// Expected: <20ms
```

---

## Step 6: Monitor & Optimize (Ongoing)

### Check Index Usage

```cypher
CALL db.indexes() YIELD name, state, populationPercent
RETURN name, state, populationPercent
ORDER BY name;
```

### Monitor Query Performance

```cypher
// Enable query logging
CALL dbms.setConfigValue('dbms.logs.query.enabled', 'true');
CALL dbms.setConfigValue('dbms.logs.query.threshold', '100ms');
```

---

## Troubleshooting

### Issue 1: Slow Queries

**Symptom**: Queries taking >500ms  
**Solution**: Check index usage with `PROFILE` or `EXPLAIN`

```cypher
PROFILE
MATCH (a:Asset) WHERE a.deviceType = 'plc' RETURN a;
// Look for "NodeByLabelScan" (bad) vs "NodeIndexSeek" (good)
```

### Issue 2: Missing Entities

**Symptom**: NER11 extracts entities but they don't appear in Neo4j  
**Solution**: Check entity mapping in `neo4j_integration.py`

```python
# Verify LABEL_MAP includes all entity types
print(integrator.LABEL_MAP)
```

### Issue 3: Duplicate Nodes

**Symptom**: Same entity created multiple times  
**Solution**: Ensure `MERGE` is used instead of `CREATE`

```cypher
// Good
MERGE (a:Asset {name: $name})
ON CREATE SET a.created = timestamp()
ON MATCH SET a.updated = timestamp()

// Bad
CREATE (a:Asset {name: $name})
```

---

## Next Steps

1. **Scale Testing**: Process larger datasets (1000+ documents)
2. **Query Optimization**: Create additional indexes based on usage patterns
3. **Monitoring**: Set up Prometheus metrics for Neo4j
4. **Documentation**: Update team wiki with new schema
5. **Training**: Conduct workshop on new query patterns

---

## Success Criteria

✅ All 16 super labels created  
✅ Composite indexes active  
✅ Test entities successfully ingested  
✅ Queries using indexes (<100ms)  
✅ No data loss from NER11 output  

---

**Status**: Ready for Production Deployment  
**Estimated Time**: 1-2 hours for initial setup  
**Support**: See `02_MIGRATION_PLAYBOOK.md` for detailed procedures
