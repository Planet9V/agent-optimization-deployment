# Neo4j Hierarchical Schema - Maintenance Guide

**Document:** MAINTENANCE_GUIDE.md
**Created:** 2025-12-12
**Version:** 1.0.0
**Status:** PRODUCTION-READY
**For:** Database Administrators & DevOps Engineers

---

## Table of Contents

1. [Schema Health Monitoring](#schema-health-monitoring)
2. [Fixing Schema Drift](#fixing-schema-drift)
3. [Adding New Entities Correctly](#adding-new-entities-correctly)
4. [Monthly Validation Procedure](#monthly-validation-procedure)
5. [Troubleshooting Common Issues](#troubleshooting-common-issues)
6. [Performance Optimization](#performance-optimization)
7. [Backup & Recovery](#backup--recovery)

---

## Schema Health Monitoring

### Daily Health Checks (5 minutes)

**Run Neo4j Browser:**
```cypher
// Quick schema health summary
CALL {
    MATCH (n) RETURN count(n) as total_nodes
} CALL {
    MATCH ()-[r]->() RETURN count(r) as total_relationships
} CALL {
    MATCH (n) WHERE n.super_label IS NOT NULL RETURN count(n) as super_labeled
} CALL {
    MATCH (n) WHERE n.tier IS NOT NULL RETURN count(n) as tiered_nodes
}
RETURN
    total_nodes,
    total_relationships,
    super_labeled,
    toFloat(super_labeled) / total_nodes * 100 as super_label_coverage_pct,
    tiered_nodes,
    toFloat(tiered_nodes) / total_nodes * 100 as tier_coverage_pct;
```

**Expected Results:**
- `total_nodes`: >= 1,207,032 (should only increase)
- `super_label_coverage_pct`: >= 16% (target: >90%)
- `tier_coverage_pct`: >= 16% (target: >90%)

**Alert Conditions:**
- Node count decrease (data loss!)
- Super label coverage < 15% (schema drift)
- Tier coverage < 15% (enrichment failure)

### Weekly Trend Analysis (15 minutes)

**Create tracking table in separate database or CSV:**

```csv
date,total_nodes,super_labeled,tier_coverage,new_nodes_week
2025-12-12,1207032,193078,16.0,102966
2025-12-19,TBD,TBD,TBD,TBD
2025-12-26,TBD,TBD,TBD,TBD
```

**Query for weekly delta:**
```cypher
// Track growth (run weekly, compare to last week)
MATCH (n)
WHERE n.created_at > datetime() - duration('P7D')
RETURN
    labels(n)[0] as label,
    count(n) as new_nodes_last_7days
ORDER BY new_nodes_last_7days DESC
LIMIT 20;
```

**What to Look For:**
- Steady growth in super_labeled nodes
- New nodes have super_label property (check label distribution)
- No sudden spikes in unlabeled nodes (indicates legacy pipeline usage)

---

## Fixing Schema Drift

### Detecting Drift

**Schema drift** = New nodes added without hierarchical properties (super_label, tier, etc.)

**Detection Query:**
```cypher
// Find nodes added recently without hierarchical enrichment
MATCH (n)
WHERE n.created_at > datetime() - duration('P7D')
  AND n.super_label IS NULL
RETURN
    labels(n)[0] as label,
    count(n) as unenriched_nodes
ORDER BY unenriched_nodes DESC
LIMIT 20;
```

**Root Causes:**
1. Legacy pipeline used instead of `05_ner11_to_neo4j_hierarchical.py`
2. Direct Cypher writes bypassing enrichment
3. External data import without transformation
4. Bulk loader (`06_bulk_graph_ingestion.py`) still active

### Fixing Drift (Retroactive Enrichment)

**Step 1: Identify Source**
```bash
# Check recent ingestion logs
grep -r "bulk_graph_ingestion" /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/*.log
grep -r "hierarchical" /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/*.log

# Identify which pipeline was used
tail -100 /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json
```

**Step 2: Stop Drift Source**
```bash
# If legacy pipeline found, disable it
mv /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/06_bulk_graph_ingestion.py \
   /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/DEPRECATED_06_bulk_graph_ingestion.py.bak

# Add warning to deprecated scripts
echo "# DEPRECATED: Use 05_ner11_to_neo4j_hierarchical.py instead" | \
   cat - /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/DEPRECATED_*.py > temp && mv temp /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/DEPRECATED_*.py
```

**Step 3: Enrich Drifted Nodes**

For nodes that can be re-processed:
```python
# Run enrichment script for drifted nodes
from pipelines.ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline
from neo4j import GraphDatabase

# Connect to Neo4j
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "neo4j@openspg")
)

# Get nodes needing enrichment
with driver.session() as session:
    result = session.run("""
        MATCH (n)
        WHERE n.created_at > datetime() - duration('P7D')
          AND n.super_label IS NULL
          AND n.ner_label IS NOT NULL
        RETURN n.ner_label as ner_label, n.name as name, id(n) as node_id
        LIMIT 1000
    """)

    nodes_to_enrich = [record.data() for record in result]

print(f"Found {len(nodes_to_enrich)} nodes needing enrichment")

# TODO: Implement enrichment logic based on ner_label
# Reference: HierarchicalEntityProcessor.get_taxonomy(ner_label)
```

For bulk enrichment of existing nodes:
```cypher
// Manual enrichment for common patterns
// Example: Enrich CVE nodes with Vulnerability super label
MATCH (n:CVE)
WHERE n.super_label IS NULL
SET
    n.super_label = 'Vulnerability',
    n.tier1 = 'TECHNICAL',
    n.tier2 = 'Vulnerability',
    n.tier = 2,
    n.fine_grained_type = 'vulnerability',
    n.vulnType = 'cve',
    n.hierarchy_path = 'TECHNICAL/Vulnerability/' + n.name,
    n.updated_at = datetime()
RETURN count(n) as enriched_cve_nodes;
```

### Preventing Future Drift

**Configuration Changes:**

1. **Disable Legacy Pipelines:**
```bash
# Create pipeline whitelist
cat > /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/config/pipeline_whitelist.txt <<EOF
05_ner11_to_neo4j_hierarchical.py
EOF

# Update ingestion scripts to check whitelist
# Add to beginning of any ingestion script:
# if [ "$(basename $0)" != "05_ner11_to_neo4j_hierarchical.py" ]; then
#     echo "ERROR: Only 05_ner11_to_neo4j_hierarchical.py is allowed for ingestion"
#     exit 1
# fi
```

2. **Add Pre-Commit Validation:**
```bash
# Add to Neo4j pre-commit hook (requires APOC)
# /var/lib/neo4j/scripts/pre_commit_validation.cypher
MATCH (n)
WHERE n.created_at > datetime() - duration('PT1M')
  AND n.super_label IS NULL
WITH count(n) as drift_count
WHERE drift_count > 0
RETURN 'DRIFT DETECTED: ' + drift_count + ' nodes without super_label' as warning;
```

3. **Automated Drift Alerts:**
```bash
# Create cron job for daily drift detection
cat > /home/jim/2_OXOT_Projects_Dev/scripts/detect_schema_drift.sh <<'EOF'
#!/bin/bash
DRIFT_COUNT=$(cypher-shell -u neo4j -p neo4j@openspg \
  "MATCH (n) WHERE n.created_at > datetime() - duration('P1D') AND n.super_label IS NULL RETURN count(n) as drift" \
  | grep -o '[0-9]\+' | head -1)

if [ "$DRIFT_COUNT" -gt 100 ]; then
    echo "ALERT: $DRIFT_COUNT nodes added without hierarchical enrichment in last 24 hours"
    # TODO: Send email/Slack alert
fi
EOF

chmod +x /home/jim/2_OXOT_Projects_Dev/scripts/detect_schema_drift.sh

# Add to crontab (run daily at 8am)
# 0 8 * * * /home/jim/2_OXOT_Projects_Dev/scripts/detect_schema_drift.sh
```

---

## Adding New Entities Correctly

### Using the Hierarchical Pipeline

**ALWAYS use this pattern for new data ingestion:**

```python
#!/usr/bin/env python3
"""
Correct Entity Ingestion Example
Uses hierarchical enrichment pipeline
"""
from pathlib import Path
import sys

# Add pipeline directory to path
pipeline_dir = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines")
sys.path.insert(0, str(pipeline_dir))

from ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

def ingest_new_document(document_text: str, document_id: str):
    """
    Correctly ingest a new document with hierarchical enrichment.

    Args:
        document_text: Full text of document
        document_id: Unique document identifier
    """
    # Initialize pipeline with hierarchical enrichment
    with NER11ToNeo4jPipeline(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="neo4j@openspg",
        ner11_api_url="http://localhost:8000"
    ) as pipeline:

        # Process document (includes hierarchical enrichment)
        stats = pipeline.process_document(document_text, document_id)

        # Validate enrichment
        validation = pipeline.validate_ingestion()

        # Check for successful enrichment
        if not validation['validation_passed']:
            print(f"WARNING: Validation failed for {document_id}")
            print(f"  Node count preserved: {validation['node_count_preserved']}")
            print(f"  Tier2 > Tier1: {validation['tier2_greater_than_tier1']}")

        return stats

# Example usage
if __name__ == "__main__":
    text = """
    APT29 exploited CVE-2024-12345 using WellMess malware to target
    government organizations in the United States.
    """

    stats = ingest_new_document(text, "sample_doc_001")

    print(f"Entities extracted: {stats['entities_extracted']}")
    print(f"Nodes created: {stats['nodes_created']}")
    print(f"Relationships created: {stats['relationships_created']}")
```

### Manual Entity Creation (When Pipeline Not Applicable)

**Use this template for direct Cypher writes:**

```cypher
// Template: Create entity with full hierarchical enrichment
// Replace ALL CAPS placeholders with actual values

MERGE (n:SUPER_LABEL {name: 'ENTITY_NAME'})
ON CREATE SET
    // Required hierarchical properties
    n.super_label = 'SUPER_LABEL',
    n.tier1 = 'TIER1_CATEGORY',  // TECHNICAL, OPERATIONAL, ASSET, ORGANIZATIONAL, CONTEXTUAL
    n.tier2 = 'SUPER_LABEL',
    n.tier = 2,  // 1, 2, or 3
    n.hierarchy_path = 'TIER1_CATEGORY/SUPER_LABEL/ENTITY_NAME',
    n.fine_grained_type = 'FINE_GRAINED_TYPE',

    // Required metadata
    n.created_at = datetime(),
    n.ner_label = 'ORIGINAL_NER_LABEL',
    n.specific_instance = 'ENTITY_NAME',

    // Optional: Property discriminator (if applicable)
    n.DISCRIMINATOR_PROPERTY = 'DISCRIMINATOR_VALUE',

    // Domain-specific properties
    n.description = 'DESCRIPTION',
    n.source = 'DATA_SOURCE'

ON MATCH SET
    n.updated_at = datetime()

RETURN n;
```

**Example: Create new APT group**

```cypher
MERGE (n:ThreatActor {name: 'APT99'})
ON CREATE SET
    // Hierarchical properties
    n.super_label = 'ThreatActor',
    n.tier1 = 'TECHNICAL',
    n.tier2 = 'ThreatActor',
    n.tier = 2,
    n.hierarchy_path = 'TECHNICAL/ThreatActor/APT99',
    n.fine_grained_type = 'threatactor',

    // Metadata
    n.created_at = datetime(),
    n.ner_label = 'APT',
    n.specific_instance = 'APT99',

    // Property discriminator
    n.actorType = 'apt_group',

    // Domain properties
    n.description = 'Advanced persistent threat group 99',
    n.source = 'threat_intelligence_feed',
    n.first_seen = date('2025-01-01'),
    n.attribution = 'Unknown'

ON MATCH SET
    n.updated_at = datetime()

RETURN n;
```

### Validation After Manual Creation

**Always validate manually created entities:**

```cypher
// Validate last 10 manually created nodes
MATCH (n)
WHERE n.created_at > datetime() - duration('PT1H')
RETURN
    labels(n)[0] as label,
    n.name as name,
    n.super_label as super_label,
    n.tier1 as tier1,
    n.tier as tier,
    CASE
        WHEN n.super_label IS NULL THEN 'MISSING super_label'
        WHEN n.tier1 IS NULL THEN 'MISSING tier1'
        WHEN n.tier IS NULL THEN 'MISSING tier'
        WHEN n.hierarchy_path IS NULL THEN 'MISSING hierarchy_path'
        ELSE 'OK'
    END as validation_status
ORDER BY n.created_at DESC
LIMIT 10;
```

---

## Monthly Validation Procedure

**Frequency:** First Monday of each month
**Duration:** 30-45 minutes
**Who:** Database Administrator

### Step 1: Run Comprehensive Validation (15 min)

```bash
# Navigate to validation directory
cd /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts

# Run validation queries and save report
cypher-shell -u neo4j -p neo4j@openspg < VALIDATION_QUERIES.cypher > ../reports/validation_$(date +%Y%m%d).txt 2>&1

# Review report
cat ../reports/validation_$(date +%Y%m%d).txt
```

### Step 2: Analyze Trends (10 min)

**Compare to last month:**

```cypher
// Get current stats
CALL {
    MATCH (n) RETURN count(n) as total_nodes
} CALL {
    MATCH (n) WHERE n.super_label IS NOT NULL RETURN count(n) as super_labeled
} CALL {
    MATCH (n) WHERE n.tier IS NOT NULL RETURN count(n) as tiered
} CALL {
    MATCH (n) WHERE n.tier = 1 RETURN count(n) as tier1
} CALL {
    MATCH (n) WHERE n.tier = 2 RETURN count(n) as tier2
} CALL {
    MATCH (n) WHERE n.tier = 3 RETURN count(n) as tier3
}
RETURN
    total_nodes,
    super_labeled,
    toFloat(super_labeled) / total_nodes * 100 as super_label_pct,
    tiered,
    toFloat(tiered) / total_nodes * 100 as tier_pct,
    tier1,
    tier2,
    tier3,
    tier2 + tier3 as tier2_plus_tier3,
    CASE WHEN (tier2 + tier3) > tier1 THEN 'PASS' ELSE 'FAIL' END as tier_distribution_status;
```

**Record in tracking spreadsheet:**

| Date | Total Nodes | Super Labeled | Coverage % | Tier1 | Tier2+3 | Distribution | Notes |
|:-----|------------:|--------------:|-----------:|------:|--------:|:-------------|:------|
| 2025-12-12 | 1,207,032 | 193,078 | 16.0% | 7,907 | 43 | FAIL | Partial migration complete |
| 2026-01-06 | TBD | TBD | TBD | TBD | TBD | TBD | Monthly validation |

### Step 3: Check for Anomalies (10 min)

**Orphan Node Growth:**
```cypher
// Track orphan nodes over time
MATCH (n)
WHERE NOT (n)--()  // Node with no relationships
RETURN
    labels(n)[0] as label,
    count(n) as orphan_count
ORDER BY orphan_count DESC
LIMIT 20;
```

**Duplicate Detection:**
```cypher
// Find potential duplicates (same name, same label)
MATCH (n)
WITH labels(n)[0] as label, n.name as name, collect(n) as nodes
WHERE size(nodes) > 1
RETURN
    label,
    name,
    size(nodes) as duplicate_count
ORDER BY duplicate_count DESC
LIMIT 20;
```

**Property Completeness:**
```cypher
// Check property completeness for super-labeled nodes
MATCH (n)
WHERE n.super_label IS NOT NULL
RETURN
    n.super_label as super_label,
    count(n) as total,
    sum(CASE WHEN n.tier1 IS NOT NULL THEN 1 ELSE 0 END) as has_tier1,
    sum(CASE WHEN n.tier IS NOT NULL THEN 1 ELSE 0 END) as has_tier,
    sum(CASE WHEN n.hierarchy_path IS NOT NULL THEN 1 ELSE 0 END) as has_hierarchy_path,
    sum(CASE WHEN n.fine_grained_type IS NOT NULL THEN 1 ELSE 0 END) as has_fine_grained_type,
    toFloat(sum(CASE WHEN n.tier1 IS NOT NULL THEN 1 ELSE 0 END)) / count(n) * 100 as completeness_pct
ORDER BY completeness_pct ASC
LIMIT 10;
```

### Step 4: Report Findings (5 min)

**Template:**

```markdown
# Neo4j Schema Health - Monthly Report
**Date:** YYYY-MM-DD
**Validator:** [Name]

## Overall Health: [EXCELLENT / GOOD / FAIR / POOR]

### Key Metrics
- Total Nodes: XXX,XXX (Δ +X,XXX from last month)
- Super Label Coverage: XX.X% (Δ +X.X% from last month)
- Tier Property Coverage: XX.X% (Δ +X.X% from last month)
- Tier Distribution: [PASS/FAIL] (tier2+tier3 [>/≤] tier1)

### Achievements
- [List positive findings]

### Issues Identified
- [List problems found]

### Actions Required
- [ ] [Action item 1]
- [ ] [Action item 2]

### Next Review Date
YYYY-MM-DD
```

---

## Troubleshooting Common Issues

### Issue 1: New Nodes Missing super_label

**Symptom:**
```cypher
MATCH (n) WHERE n.created_at > datetime() - duration('P1D') AND n.super_label IS NULL
RETURN count(n);
// Returns > 0
```

**Diagnosis:**
1. Check which pipeline was used
2. Verify `05_ner11_to_neo4j_hierarchical.py` active
3. Check NER11 API connectivity
4. Review HierarchicalEntityProcessor logs

**Fix:**
```bash
# 1. Identify source
grep "pipeline" /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json

# 2. If legacy pipeline, disable it
# See "Fixing Schema Drift" section above

# 3. Re-process with correct pipeline
# See "Adding New Entities Correctly" section
```

### Issue 2: Tier Distribution Imbalance (tier1 > tier2+tier3)

**Symptom:**
```cypher
MATCH (n) WHERE n.tier IS NOT NULL
RETURN n.tier as tier, count(n) as count;
// tier1 count > tier2 + tier3 count
```

**Diagnosis:**
- Most entities assigned to top-level categories
- Taxonomy lacks depth in fine_grained_type mappings

**Fix:**
```python
# Expand HierarchicalEntityProcessor taxonomy
# File: /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/00_hierarchical_entity_processor.py

# Add more tier2 and tier3 mappings
# Example: Expand ThreatActor subtypes
self.taxonomy["APT_GROUP"] = {
    "super_label": Neo4jSuperLabel.THREAT_ACTOR,
    "tier": 2,  # Changed from 1 to 2
    "subtype": "apt_group",
    "actorType": "advanced_persistent_threat",
    # Add tier3 specific types
    "sophistication": "high",
    "resources": "nation_state"
}
```

### Issue 3: CVE Nodes Not Classified

**Symptom:**
```cypher
MATCH (n:CVE) WHERE n.super_label IS NULL RETURN count(n);
// Returns 316,552
```

**Diagnosis:**
- CVE data imported from external source
- Bulk import bypassed hierarchical enrichment

**Fix:**
```cypher
// Batch enrichment for all CVE nodes
MATCH (n:CVE)
WHERE n.super_label IS NULL
CALL apoc.periodic.iterate(
    'MATCH (n:CVE) WHERE n.super_label IS NULL RETURN n',
    'SET n.super_label = "Vulnerability",
         n.tier1 = "TECHNICAL",
         n.tier2 = "Vulnerability",
         n.tier = 2,
         n.fine_grained_type = "vulnerability",
         n.vulnType = "cve",
         n.hierarchy_path = "TECHNICAL/Vulnerability/" + n.name,
         n.updated_at = datetime()',
    {batchSize:1000, parallel:true}
)
YIELD batches, total
RETURN batches, total;
```

### Issue 4: Property Discriminator Missing

**Symptom:**
```cypher
MATCH (n:ThreatActor) WHERE n.actorType IS NULL RETURN count(n);
// Returns > 0 (should be 0 for all ThreatActors)
```

**Diagnosis:**
- Nodes created before discriminator implementation
- Or enrichment failed for some entities

**Fix:**
```cypher
// Infer actorType from ner_label or name patterns
MATCH (n:ThreatActor)
WHERE n.actorType IS NULL
SET n.actorType =
    CASE
        WHEN n.ner_label = 'APT' OR n.name STARTS WITH 'APT' THEN 'apt_group'
        WHEN n.ner_label = 'ADVERSARY' THEN 'adversary'
        WHEN n.attribution = 'nation_state' THEN 'nation_state'
        ELSE 'unknown'
    END,
    n.updated_at = datetime()
RETURN count(n) as updated_threat_actors;
```

### Issue 5: Performance Degradation

**Symptom:**
- Queries taking >10 seconds for hierarchical traversals
- Neo4j Browser slow to load

**Diagnosis:**
```cypher
// Check if indexes exist on hierarchical properties
SHOW INDEXES;
// Look for indexes on: super_label, tier1, tier, hierarchy_path
```

**Fix:**
```cypher
// Create indexes on hierarchical properties
CREATE INDEX super_label_index FOR (n) ON (n.super_label);
CREATE INDEX tier1_index FOR (n) ON (n.tier1);
CREATE INDEX tier_index FOR (n) ON (n.tier);
CREATE INDEX hierarchy_path_index FOR (n) ON (n.hierarchy_path);

// For property discriminators
CREATE INDEX actorType_index FOR (n:ThreatActor) ON (n.actorType);
CREATE INDEX malwareFamily_index FOR (n:Malware) ON (n.malwareFamily);
CREATE INDEX vulnType_index FOR (n:Vulnerability) ON (n.vulnType);

// Wait for indexes to come online
SHOW INDEXES;
```

---

## Performance Optimization

### Index Strategy

**Core Hierarchical Indexes (Required):**
```cypher
// Property indexes for all nodes
CREATE INDEX super_label_index IF NOT EXISTS FOR (n) ON (n.super_label);
CREATE INDEX tier1_index IF NOT EXISTS FOR (n) ON (n.tier1);
CREATE INDEX tier_index IF NOT EXISTS FOR (n) ON (n.tier);
CREATE INDEX hierarchy_path_index IF NOT EXISTS FOR (n) ON (n.hierarchy_path);
CREATE INDEX fine_grained_type_index IF NOT EXISTS FOR (n) ON (n.fine_grained_type);

// Temporal indexes
CREATE INDEX created_at_index IF NOT EXISTS FOR (n) ON (n.created_at);
CREATE INDEX updated_at_index IF NOT EXISTS FOR (n) ON (n.updated_at);
```

**Super Label Specific Indexes:**
```cypher
// ThreatActor indexes
CREATE INDEX threatactor_name IF NOT EXISTS FOR (n:ThreatActor) ON (n.name);
CREATE INDEX threatactor_actorType IF NOT EXISTS FOR (n:ThreatActor) ON (n.actorType);

// Malware indexes
CREATE INDEX malware_name IF NOT EXISTS FOR (n:Malware) ON (n.name);
CREATE INDEX malware_family IF NOT EXISTS FOR (n:Malware) ON (n.malwareFamily);

// Vulnerability indexes
CREATE INDEX vulnerability_name IF NOT EXISTS FOR (n:Vulnerability) ON (n.name);
CREATE INDEX vulnerability_vulnType IF NOT EXISTS FOR (n:Vulnerability) ON (n.vulnType);

// CVE indexes (if not already created)
CREATE INDEX cve_name IF NOT EXISTS FOR (n:CVE) ON (n.name);

// Control indexes
CREATE INDEX control_name IF NOT EXISTS FOR (n:Control) ON (n.name);
CREATE INDEX control_controlType IF NOT EXISTS FOR (n:Control) ON (n.controlType);
```

### Query Optimization

**Before Optimization:**
```cypher
// Slow: Full graph scan
MATCH (n)
WHERE n.tier1 = 'TECHNICAL'
RETURN n;
// Execution time: ~30 seconds
```

**After Optimization:**
```cypher
// Fast: Uses tier1_index
CREATE INDEX tier1_index IF NOT EXISTS FOR (n) ON (n.tier1);

MATCH (n)
WHERE n.tier1 = 'TECHNICAL'
RETURN n;
// Execution time: <1 second
```

### Memory Tuning

**Neo4j Configuration (`/etc/neo4j/neo4j.conf`):**
```properties
# Heap size (set to 50% of available RAM, max 31GB)
dbms.memory.heap.initial_size=8g
dbms.memory.heap.max_size=8g

# Page cache (remaining RAM after heap)
dbms.memory.pagecache.size=8g

# Query cache
dbms.query_cache_size=200

# Bolt connection pool
dbms.connector.bolt.thread_pool_min_size=10
dbms.connector.bolt.thread_pool_max_size=100
```

---

## Backup & Recovery

### Daily Backup Procedure

**Automated Daily Backup:**
```bash
#!/bin/bash
# File: /home/jim/2_OXOT_Projects_Dev/scripts/neo4j_daily_backup.sh

BACKUP_DIR="/var/lib/neo4j/backups"
DATE=$(date +%Y%m%d)
NEO4J_HOME="/var/lib/neo4j"

# Stop Neo4j (offline backup for consistency)
sudo systemctl stop neo4j

# Backup database
sudo cp -r $NEO4J_HOME/data/databases/neo4j $BACKUP_DIR/neo4j_$DATE

# Backup configuration
sudo cp -r $NEO4J_HOME/conf $BACKUP_DIR/conf_$DATE

# Restart Neo4j
sudo systemctl start neo4j

# Wait for startup
sleep 10

# Compress backup (async)
tar -czf $BACKUP_DIR/neo4j_backup_$DATE.tar.gz -C $BACKUP_DIR neo4j_$DATE conf_$DATE &

# Remove uncompressed backup after compression
wait
rm -rf $BACKUP_DIR/neo4j_$DATE $BACKUP_DIR/conf_$DATE

# Retention: Keep last 7 daily backups
find $BACKUP_DIR -name "neo4j_backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: neo4j_backup_$DATE.tar.gz"
```

**Add to crontab:**
```bash
# Run daily at 2am
0 2 * * * /home/jim/2_OXOT_Projects_Dev/scripts/neo4j_daily_backup.sh
```

### Weekly Schema Validation Backup

**Export schema validation results:**
```bash
#!/bin/bash
# File: /home/jim/2_OXOT_Projects_Dev/scripts/export_schema_validation.sh

REPORT_DIR="/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/reports"
DATE=$(date +%Y%m%d)

# Run validation queries
cypher-shell -u neo4j -p neo4j@openspg < \
  /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/VALIDATION_QUERIES.cypher \
  > $REPORT_DIR/schema_validation_$DATE.txt 2>&1

# Compress old reports (>30 days)
find $REPORT_DIR -name "schema_validation_*.txt" -mtime +30 -exec gzip {} \;

echo "Schema validation exported: schema_validation_$DATE.txt"
```

### Recovery Procedure

**Restore from Backup:**
```bash
#!/bin/bash
# CRITICAL: Only run when recovering from data loss

BACKUP_DATE="20251212"  # Change to backup date
BACKUP_DIR="/var/lib/neo4j/backups"
NEO4J_HOME="/var/lib/neo4j"

# 1. Stop Neo4j
sudo systemctl stop neo4j

# 2. Backup current database (just in case)
sudo mv $NEO4J_HOME/data/databases/neo4j $NEO4J_HOME/data/databases/neo4j.before_restore

# 3. Extract backup
tar -xzf $BACKUP_DIR/neo4j_backup_$BACKUP_DATE.tar.gz -C $BACKUP_DIR

# 4. Restore database
sudo cp -r $BACKUP_DIR/neo4j_$BACKUP_DATE $NEO4J_HOME/data/databases/neo4j

# 5. Restore configuration (optional)
sudo cp -r $BACKUP_DIR/conf_$BACKUP_DATE/* $NEO4J_HOME/conf/

# 6. Fix permissions
sudo chown -R neo4j:neo4j $NEO4J_HOME/data/databases/neo4j

# 7. Restart Neo4j
sudo systemctl start neo4j

# 8. Wait for startup
sleep 30

# 9. Validate restoration
cypher-shell -u neo4j -p neo4j@openspg "MATCH (n) RETURN count(n) as total_nodes;"

echo "Recovery complete from backup: $BACKUP_DATE"
```

---

## Emergency Contacts

**Database Administrator:** [Your Name]
**Email:** [Your Email]
**Phone:** [Your Phone]

**Escalation:** AEON Architecture Team
**Slack:** #aeon-database-ops

---

**Guide Prepared By:** AEON Documentation Specialist
**Last Updated:** 2025-12-12
**Next Review:** 2026-03-12 (quarterly)

**END OF MAINTENANCE GUIDE**
