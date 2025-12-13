# AEON Hierarchical Schema Fix - Test Procedure

**Document:** HIERARCHICAL_SCHEMA_FIX_PROCEDURE.md
**Created:** 2025-12-12
**Version:** 1.0.0
**Status:** READY FOR EXECUTION
**Author:** AEON Solution Architect

---

## Executive Summary

This procedure fixes the critical gap where 1.4M Neo4j nodes exist without hierarchical schema properties from v3.1 specification. The fix adds super labels, tier properties, and property discriminators to enable the 6-level architecture with 16 super labels and 560 hierarchical types.

### Problem Statement

**Current State:**
- 1,426,989 total nodes in Neo4j database
- Only 83,052 (5.8%) have super labels
- 0 nodes have `tier1`, `tier2` hierarchical properties
- 0 nodes have property discriminators (`actorType`, `malwareFamily`, etc.)
- 316,552 CVE nodes missing `Vulnerability` super label

**Impact:**
- 6-level architecture NOT FUNCTIONAL
- 566-type taxonomy NOT ACCESSIBLE
- Hierarchical queries IMPOSSIBLE
- Fine-grained entity typing UNAVAILABLE

**Root Cause:**
- v3.1 schema designed after bulk data ingestion
- Migration scripts never executed
- Multiple ingestion pipelines with different schemas
- Legacy data not migrated to new schema

---

## Solution Overview

### Fix Components

1. **Migration Script:** `FIX_HIERARCHICAL_SCHEMA.py`
   - Adds super labels to all nodes based on existing label patterns
   - Adds hierarchical properties (tier1, tier2, tier)
   - Adds property discriminators for fine-grained typing
   - Validates all requirements met

2. **Validation Queries:** `VALIDATION_QUERIES.cypher`
   - 11 comprehensive validation checks
   - Verifies node count preservation
   - Confirms tier distribution
   - Validates property coverage

3. **Pipeline Fix:** Future ingestions use hierarchical enrichment
   - Route through `05_ner11_to_neo4j_hierarchical.py`
   - Ensure `HierarchicalEntityProcessor` is active
   - Deprecate legacy loaders

---

## Pre-Execution Checklist

### Environment Verification

```bash
# 1. Verify Neo4j is running
curl http://localhost:7474

# 2. Verify connection credentials
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="neo4j@openspg"

# 3. Verify Python dependencies
python3 -c "import neo4j; print('neo4j:', neo4j.__version__)"

# 4. Verify APOC plugin installed (required for validation)
# Run in Neo4j Browser:
# CALL dbms.procedures() YIELD name WHERE name STARTS WITH 'apoc' RETURN count(name);
# Expected: > 0
```

### Backup Database (CRITICAL)

```bash
# Stop Neo4j
sudo systemctl stop neo4j

# Backup database
sudo cp -r /var/lib/neo4j/data/databases/neo4j /var/lib/neo4j/data/databases/neo4j.backup.$(date +%Y%m%d_%H%M%S)

# Backup logs
sudo cp -r /var/lib/neo4j/logs /var/lib/neo4j/logs.backup.$(date +%Y%m%d_%H%M%S)

# Restart Neo4j
sudo systemctl start neo4j

# Wait for startup
sleep 10
```

### Baseline Measurements

```bash
# Record current state in Neo4j Browser
MATCH (n) RETURN count(n) as total_nodes;
# Expected: 1,426,989

CALL db.labels() YIELD label
RETURN count(label) as total_labels;
# Expected: ~580
```

---

## Execution Procedure

### Phase 1: Analysis (Read-Only)

```bash
# Run analysis phase only (no modifications)
cd /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts

# Execute with dry-run (recommended first time)
python3 -c "
from FIX_HIERARCHICAL_SCHEMA import HierarchicalSchemaFix
with HierarchicalSchemaFix() as fixer:
    analysis = fixer.analyze_current_state()
    print('Analysis complete. Review logs before proceeding.')
"
```

**Expected Output:**
```
Total nodes: 1,426,989
Nodes with super labels: 83,052 (5.8%)
Nodes with tier properties: 12
Nodes with discriminators: ~30,000

Gaps identified: 3
  - CRITICAL: Less than 50% of nodes have super labels
  - CRITICAL: Less than 10% of nodes have tier properties
  - CRITICAL: Less than 10% of nodes have discriminators
```

**Decision Point:** If gaps match expectations, proceed to Phase 2.

---

### Phase 2: Super Label Addition

```bash
# Add super labels to existing nodes
python3 -c "
from FIX_HIERARCHICAL_SCHEMA import HierarchicalSchemaFix
with HierarchicalSchemaFix() as fixer:
    results = fixer.add_super_labels()
    print('Super labels added:', sum(results.values()))
"
```

**Expected Output:**
```
ThreatActor: Added to 1,067 nodes
Malware: Added to 1,016 nodes
Technique: Added to 1,023 nodes
Vulnerability: Added to 304,530 nodes  # ← Critical: CVE nodes
Indicator: Added to 6,601 nodes
Campaign: Added to 163 nodes
Asset: Added to 140,000 nodes  # ← SBOM nodes
... (other super labels)

Total super labels added: ~500,000
```

**Validation:**
```cypher
// Run in Neo4j Browser
MATCH (n:CVE)
WHERE n:Vulnerability
RETURN count(n) as cve_nodes_with_vulnerability_label;
// Expected: 316,552 (all CVEs now have Vulnerability super label)
```

---

### Phase 3: Hierarchical Properties

```bash
# Add tier1, tier2, tier properties
python3 -c "
from FIX_HIERARCHICAL_SCHEMA import HierarchicalSchemaFix
with HierarchicalSchemaFix() as fixer:
    results = fixer.add_hierarchical_properties()
    print('Tier properties added:', sum(results.values()))
"
```

**Expected Output:**
```
ThreatActor (TECHNICAL): Added tier properties to 1,067 nodes
Malware (TECHNICAL): Added tier properties to 1,016 nodes
Technique (TECHNICAL): Added tier properties to 1,023 nodes
Vulnerability (TECHNICAL): Added tier properties to 316,552 nodes
... (other super labels)

Total tier properties added: ~1,400,000
```

**Validation:**
```cypher
// Verify tier distribution
MATCH (n)
WHERE n.tier IS NOT NULL
RETURN n.tier as tier, count(n) as count
ORDER BY tier;

// Expected:
// tier 1 (TECHNICAL): ~500,000
// tier 2 (OPERATIONAL/ASSET/ORGANIZATIONAL): ~600,000
// tier 3 (CONTEXTUAL): ~300,000
```

---

### Phase 4: Property Discriminators

```bash
# Add property discriminators for fine-grained typing
python3 -c "
from FIX_HIERARCHICAL_SCHEMA import HierarchicalSchemaFix
with HierarchicalSchemaFix() as fixer:
    results = fixer.add_property_discriminators()
    print('Discriminators added:', sum(results.values()))
"
```

**Expected Output:**
```
ThreatActor.actorType: Added to 1,067 nodes
Malware.malwareFamily: Added to 1,016 nodes
Technique.patternType: Added to 1,023 nodes
Vulnerability.vulnType: Added to 316,552 nodes
... (other discriminators)

Total discriminators added: ~500,000
```

**Validation:**
```cypher
// Verify discriminators exist
MATCH (n:Vulnerability)
RETURN n.vulnType as vulnType, count(n) as count;

// Expected:
// vulnType='cve': 316,552
// vulnType='cwe': (if CWE nodes exist)
```

---

### Phase 5: Complete Validation

```bash
# Run complete migration with validation
cd /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts

python3 FIX_HIERARCHICAL_SCHEMA.py
# Will prompt: "Proceed with migration? (yes/no): "
# Type: yes
```

**Expected Output:**
```
PHASE 1: ANALYZING CURRENT DATABASE STATE
Total nodes: 1,426,989
Nodes with super labels: 83,052 (5.8%)
...

PHASE 2: ADDING SUPER LABELS TO EXISTING NODES
ThreatActor: Added to 1,067 nodes
...
Total super labels added: 500,000

PHASE 3: ADDING HIERARCHICAL PROPERTIES
ThreatActor (TECHNICAL): Added tier properties to 1,067 nodes
...
Total tier properties added: 1,400,000

PHASE 4: ADDING PROPERTY DISCRIMINATORS
ThreatActor.actorType: Added to 1,067 nodes
...
Total discriminators added: 500,000

PHASE 5: VALIDATION
Total nodes: 1,426,989
Node count preserved: ✅ PASS
Super label coverage: 95.0% ✅ PASS
Tier property coverage: 98.5% ✅ PASS
Discriminator coverage: 35.0% ✅ PASS

Tier distribution:
  tier_1: 500,000
  tier_2: 600,000
  tier_3: 326,989

Overall validation: ✅ PASS

MIGRATION COMPLETE
Total nodes: 1,426,989
Super labels added: 500,000
Tier properties added: 1,400,000
Discriminators added: 500,000
Validation: ✅ PASSED
```

---

## Post-Execution Validation

### Run Comprehensive Validation Queries

```bash
# Load validation queries in Neo4j Browser
# File: /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/VALIDATION_QUERIES.cypher

# Or run via cypher-shell
cat VALIDATION_QUERIES.cypher | cypher-shell -u neo4j -p neo4j@openspg > validation_results.txt
```

### Critical Validation Checks

**Check 1: Node Count Preservation**
```cypher
MATCH (n) RETURN count(n) as total_nodes;
// Expected: >= 1,426,989
// Status: PASS
```

**Check 2: Super Label Coverage**
```cypher
MATCH (n)
WHERE n:ThreatActor OR n:Malware OR n:Technique OR n:Vulnerability OR
      n:Indicator OR n:Campaign OR n:Asset OR n:Organization OR
      n:Location OR n:PsychTrait OR n:EconomicMetric OR n:Protocol OR
      n:Role OR n:Software OR n:Control OR n:Event
RETURN count(n) as nodes_with_super_labels;
// Expected: > 1,300,000 (>90% coverage)
// Status: PASS if > 1,000,000
```

**Check 3: Tier Distribution**
```cypher
MATCH (n)
WHERE n.tier IS NOT NULL
WITH n.tier as tier, count(n) as count
WITH collect({tier: tier, count: count}) as tier_counts
WITH [x IN tier_counts WHERE x.tier = 1 | x.count][0] as tier1_count,
     [x IN tier_counts WHERE x.tier = 2 | x.count][0] as tier2_count,
     [x IN tier_counts WHERE x.tier = 3 | x.count][0] as tier3_count
RETURN
  tier1_count,
  tier2_count,
  tier3_count,
  (tier2_count + tier3_count) > tier1_count as validation_passed;
// Expected: validation_passed = true
// Status: PASS
```

**Check 4: CVE Classification**
```cypher
MATCH (n:CVE)
WHERE NOT n:Vulnerability
RETURN count(n) as unclassified_cves;
// Expected: 0
// Status: PASS if = 0
```

**Check 5: Sample Node Structure**
```cypher
MATCH (n:ThreatActor)
RETURN n.name, n.super_label, n.tier1, n.tier2, n.tier, n.actorType, labels(n)
LIMIT 5;
// Expected: All properties populated
// Status: PASS if all non-null
```

---

## Rollback Procedure (If Needed)

### Option 1: Restore from Backup

```bash
# Stop Neo4j
sudo systemctl stop neo4j

# Remove current database
sudo rm -rf /var/lib/neo4j/data/databases/neo4j

# Restore backup
sudo cp -r /var/lib/neo4j/data/databases/neo4j.backup.YYYYMMDD_HHMMSS /var/lib/neo4j/data/databases/neo4j

# Fix permissions
sudo chown -R neo4j:neo4j /var/lib/neo4j/data/databases/neo4j

# Restart Neo4j
sudo systemctl start neo4j
```

### Option 2: Remove Added Properties

```cypher
// Remove super labels (careful - only remove if they were added by script)
MATCH (n)
WHERE n.super_label IS NOT NULL
REMOVE n:ThreatActor, n:Malware, n:Technique, n:Vulnerability,
       n:Indicator, n:Campaign, n:Asset, n:Organization,
       n:Location, n:PsychTrait, n:EconomicMetric, n:Protocol,
       n:Role, n:Software, n:Control, n:Event
REMOVE n.super_label, n.tier1, n.tier2, n.tier, n.hierarchy_path
RETURN count(n) as reverted_nodes;

// Remove discriminators
MATCH (n)
WHERE n.actorType IS NOT NULL OR n.malwareFamily IS NOT NULL OR n.patternType IS NOT NULL
REMOVE n.actorType, n.malwareFamily, n.patternType, n.vulnType,
       n.indicatorType, n.campaignType, n.assetClass, n.protocolType,
       n.roleType, n.softwareType, n.controlType, n.eventType, n.fine_grained_type
RETURN count(n) as reverted_discriminators;
```

---

## Future Ingestion Pipeline Fix

### Ensure Future Data Uses v3.1 Schema

**Update Pipeline Configuration:**
```python
# File: /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/config.py

# PRIMARY PIPELINE (use this for all ingestions)
PRIMARY_PIPELINE = "05_ner11_to_neo4j_hierarchical.py"

# Enable hierarchical processor
USE_HIERARCHICAL_ENRICHMENT = True

# Deprecate legacy pipelines
DEPRECATED_PIPELINES = [
    "06_bulk_graph_ingestion.py",  # Does not use v3.1 schema
]
```

**Route All Ingestions Through Hierarchical Pipeline:**
```python
# Example ingestion code
from pipelines.ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

with NER11ToNeo4jPipeline() as pipeline:
    # This automatically applies:
    # - HierarchicalEntityProcessor (566 types)
    # - NER11ToNeo4jMapper (60 NER → 16 super labels)
    # - Tier properties (tier1, tier2, tier)
    # - Property discriminators

    doc_stats = pipeline.process_document(text, "doc_id")
```

---

## Success Criteria

### Migration Success

- ✅ Node count preserved (>= 1,426,989)
- ✅ Super label coverage > 90%
- ✅ Tier property coverage > 90%
- ✅ Property discriminator coverage > 30%
- ✅ Tier distribution: (tier2 + tier3) > tier1
- ✅ All 16 super labels in use
- ✅ CVE nodes have Vulnerability super label (100%)
- ✅ All validation queries PASS

### Functional Verification

**Test Query 1: Hierarchical Navigation**
```cypher
// Find all TECHNICAL tier entities with APT actorType
MATCH (n)
WHERE n.tier1 = 'TECHNICAL' AND n.actorType = 'apt_group'
RETURN n.name, n.tier2, n.actorType
LIMIT 10;
// Expected: 10 results (APT groups)
```

**Test Query 2: Fine-Grained Type Filtering**
```cypher
// Find all CVE vulnerabilities
MATCH (n:Vulnerability)
WHERE n.vulnType = 'cve'
RETURN count(n) as cve_count;
// Expected: 316,552
```

**Test Query 3: Tier-Based Aggregation**
```cypher
// Count entities by tier1 category
MATCH (n)
WHERE n.tier1 IS NOT NULL
RETURN n.tier1, count(n) as count
ORDER BY count DESC;
// Expected: 5 categories with counts
```

---

## Troubleshooting

### Issue 1: APOC Plugin Not Found

**Symptom:**
```
Neo4jError: There is no procedure with the name `apoc.cypher.run`
```

**Solution:**
```bash
# Install APOC plugin
sudo cp /path/to/apoc-5.x.x-core.jar /var/lib/neo4j/plugins/
sudo systemctl restart neo4j

# Verify
# In Neo4j Browser:
CALL dbms.procedures() YIELD name WHERE name STARTS WITH 'apoc' RETURN count(name);
```

### Issue 2: Out of Memory During Migration

**Symptom:**
```
Neo4jError: Java heap space
```

**Solution:**
```bash
# Increase Neo4j memory
sudo nano /etc/neo4j/neo4j.conf

# Modify:
server.memory.heap.initial_size=4g
server.memory.heap.max_size=8g
server.memory.pagecache.size=4g

# Restart
sudo systemctl restart neo4j
```

### Issue 3: Migration Takes Too Long

**Symptom:**
Migration runs for > 2 hours

**Solution:**
Run in batches:
```python
# Modify FIX_HIERARCHICAL_SCHEMA.py to process in batches
BATCH_SIZE = 10000  # Process 10K nodes at a time

# Add batching to queries:
MATCH (n:ThreatActor)
WHERE n.tier1 IS NULL
WITH n LIMIT $batch_size
SET n.tier1 = $tier1, ...
```

---

## Performance Metrics

**Expected Execution Time:**
- Phase 1 (Analysis): 30 seconds - 2 minutes
- Phase 2 (Super Labels): 5-15 minutes
- Phase 3 (Tier Properties): 10-30 minutes
- Phase 4 (Discriminators): 10-30 minutes
- Phase 5 (Validation): 2-5 minutes

**Total:** 30-90 minutes (depends on hardware)

**Disk Space:**
- Backup: ~5-10 GB
- Logs: ~100 MB
- No significant database size increase (only properties added)

---

## Appendix: File Locations

**Scripts:**
- `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/FIX_HIERARCHICAL_SCHEMA.py`
- `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/VALIDATION_QUERIES.cypher`

**Documentation:**
- `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/HIERARCHICAL_SCHEMA_FIX_PROCEDURE.md`
- `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/docs/AEON_SCHEMA_COMPLIANCE_REPORT.md`

**Logs:**
- `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/logs/schema_fix.log`

**Pipelines:**
- `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_hierarchical.py`
- `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/00_hierarchical_entity_processor.py`
- `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/04_ner11_to_neo4j_mapper.py`

---

**END OF PROCEDURE**

**Prepared By:** AEON Solution Architect
**Review Status:** READY FOR EXECUTION
**Risk Level:** MEDIUM (backup required)
**Estimated Duration:** 30-90 minutes
**Prerequisites:** Neo4j backup, APOC plugin, Python neo4j library
