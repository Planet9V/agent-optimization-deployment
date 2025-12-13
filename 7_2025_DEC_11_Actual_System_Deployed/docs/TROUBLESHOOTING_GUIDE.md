# Neo4j Hierarchical Schema - Troubleshooting Guide

**Document:** TROUBLESHOOTING_GUIDE.md
**Created:** 2025-12-12
**Version:** 1.0.0
**Status:** PRODUCTION-READY
**For:** Support Engineers & Database Administrators

---

## Table of Contents

1. [Quick Diagnostic Checklist](#quick-diagnostic-checklist)
2. [Schema Drift Issues](#schema-drift-issues)
3. [Ingestion Pipeline Failures](#ingestion-pipeline-failures)
4. [Performance Problems](#performance-problems)
5. [Data Quality Issues](#data-quality-issues)
6. [Neo4j Database Issues](#neo4j-database-issues)
7. [NER11 API Issues](#ner11-api-issues)
8. [Emergency Procedures](#emergency-procedures)

---

## Quick Diagnostic Checklist

**Run this 5-minute diagnostic when any issue is reported:**

### System Health Check

```bash
#!/bin/bash
# Quick system diagnostic
# File: /home/jim/2_OXOT_Projects_Dev/scripts/quick_diagnostic.sh

echo "=== AEON Neo4j System Diagnostic ==="
echo "Timestamp: $(date)"
echo ""

# 1. Neo4j Status
echo "1. NEO4J STATUS"
sudo systemctl status neo4j | grep -E "Active:|Main PID:" || echo "  ❌ Neo4j not running"
echo ""

# 2. Neo4j Connection Test
echo "2. NEO4J CONNECTION"
cypher-shell -u neo4j -p neo4j@openspg "RETURN 1 as test;" 2>&1 | grep -q "test" \
    && echo "  ✅ Connection successful" \
    || echo "  ❌ Connection failed"
echo ""

# 3. NER11 API Status
echo "3. NER11 API STATUS"
curl -s http://localhost:8000/health | grep -q "healthy" \
    && echo "  ✅ API healthy" \
    || echo "  ❌ API not responding"
echo ""

# 4. Database Node Count
echo "4. DATABASE NODE COUNT"
NODE_COUNT=$(cypher-shell -u neo4j -p neo4j@openspg \
    "MATCH (n) RETURN count(n) as count;" 2>/dev/null | grep -o '[0-9]\+' | head -1)
echo "  Current nodes: $NODE_COUNT"
echo "  Baseline: 1,207,032"
if [ "$NODE_COUNT" -lt 1200000 ]; then
    echo "  ⚠️ WARNING: Node count below baseline (potential data loss)"
else
    echo "  ✅ Node count healthy"
fi
echo ""

# 5. Schema Enrichment Coverage
echo "5. HIERARCHICAL ENRICHMENT"
ENRICHED=$(cypher-shell -u neo4j -p neo4j@openspg \
    "MATCH (n) WHERE n.super_label IS NOT NULL RETURN count(n) as count;" \
    2>/dev/null | grep -o '[0-9]\+' | head -1)
COVERAGE=$(echo "scale=1; $ENRICHED * 100 / $NODE_COUNT" | bc)
echo "  Enriched nodes: $ENRICHED ($COVERAGE%)"
if (( $(echo "$COVERAGE < 15" | bc -l) )); then
    echo "  ⚠️ WARNING: Enrichment coverage below 15%"
else
    echo "  ✅ Enrichment coverage healthy"
fi
echo ""

# 6. Recent Errors
echo "6. RECENT INGESTION ERRORS"
if [ -f "/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json" ]; then
    ERROR_COUNT=$(grep -o '"errors"' /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json | wc -l)
    echo "  Recent error log entries: $ERROR_COUNT"
else
    echo "  No error log found"
fi
echo ""

echo "=== DIAGNOSTIC COMPLETE ==="
```

**Make it executable:**
```bash
chmod +x /home/jim/2_OXOT_Projects_Dev/scripts/quick_diagnostic.sh
```

**Run it:**
```bash
/home/jim/2_OXOT_Projects_Dev/scripts/quick_diagnostic.sh
```

---

## Schema Drift Issues

### Issue 1: New Nodes Without super_label Property

**Symptom:**
```cypher
MATCH (n)
WHERE n.created_at > datetime() - duration('P1D')
  AND n.super_label IS NULL
RETURN count(n) as drift_count;
// Returns > 100
```

**Diagnosis Steps:**

1. **Check which pipeline was used:**
```bash
# Review recent ingestion logs
tail -100 /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json | grep "pipeline"
```

2. **Check for direct Cypher writes:**
```bash
# Search for direct CREATE statements in logs
grep -r "CREATE (" /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/*.log
```

3. **Identify source:**
```cypher
// Find recent unenriched nodes by label
MATCH (n)
WHERE n.created_at > datetime() - duration('P1D')
  AND n.super_label IS NULL
RETURN labels(n)[0] as label, count(n) as count
ORDER BY count DESC;
```

**Root Causes:**
- Legacy pipeline (`06_bulk_graph_ingestion.py`) still being used
- Direct Cypher writes bypassing enrichment
- External data import without transformation
- Script error causing HierarchicalEntityProcessor to be skipped

**Solution:**

**Step 1: Stop the drift source**
```bash
# Disable legacy pipelines
mv /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/06_bulk_graph_ingestion.py \
   /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/DEPRECATED_06_bulk_graph_ingestion.py.bak

# Add deprecation warning
echo "# DEPRECATED: Use 05_ner11_to_neo4j_hierarchical.py instead" | \
   cat - /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/DEPRECATED_*.py > temp && \
   mv temp /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/DEPRECATED_*.py
```

**Step 2: Fix drifted nodes retroactively**

For common patterns (CVE example):
```cypher
// Enrich CVE nodes that lack super_label
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
RETURN count(n) as enriched_cves;
```

For nodes with `ner_label` property:
```cypher
// Re-enrich based on ner_label
MATCH (n)
WHERE n.super_label IS NULL AND n.ner_label IS NOT NULL
WITH n, n.ner_label as ner_label
// Map NER labels to super labels
SET n.super_label =
    CASE ner_label
        WHEN 'APT' THEN 'ThreatActor'
        WHEN 'MALWARE' THEN 'Malware'
        WHEN 'VULNERABILITY' THEN 'Vulnerability'
        WHEN 'INDICATOR' THEN 'Indicator'
        WHEN 'CAMPAIGN' THEN 'Campaign'
        WHEN 'ASSET' THEN 'Asset'
        WHEN 'ORGANIZATION' THEN 'Organization'
        WHEN 'LOCATION' THEN 'Location'
        ELSE 'Entity'
    END,
    n.tier1 = 'TECHNICAL',  // Default, adjust as needed
    n.tier = 2,
    n.updated_at = datetime()
RETURN count(n) as enriched_nodes;
```

**Step 3: Monitor for recurrence**
```bash
# Add to cron (daily check at 9am)
cat >> /etc/crontab <<'EOF'
0 9 * * * root /home/jim/2_OXOT_Projects_Dev/scripts/detect_schema_drift.sh
EOF
```

---

### Issue 2: Tier Distribution Imbalance (tier1 >> tier2+tier3)

**Symptom:**
```cypher
MATCH (n) WHERE n.tier IS NOT NULL
RETURN n.tier, count(n) as count
ORDER BY n.tier;
// tier1: 71,775
// tier2: 1,384
// tier3: 0
// Imbalance: tier1 >> (tier2 + tier3)
```

**Diagnosis:**
- Taxonomy configured with too many tier1 classifications
- Most entities assigned to top-level categories
- Insufficient fine-grained type mappings

**Root Cause:**
This is a taxonomy configuration issue, not a pipeline failure.

**Solution:**

**Option 1: Accept as expected for now**
- This is normal during partial migration
- Will improve as more documents processed with deeper taxonomy
- Monitor coverage growth over time

**Option 2: Expand taxonomy (advanced)**
```python
# Edit HierarchicalEntityProcessor taxonomy
# File: /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/00_hierarchical_entity_processor.py

# Change tier levels for specific types
self.taxonomy["APT_GROUP"] = {
    "super_label": Neo4jSuperLabel.THREAT_ACTOR,
    "tier": 2,  # Changed from 1 to 2
    "subtype": "apt_group",
    "actorType": "advanced_persistent_threat"
}

# Add more tier3 specific types
self.taxonomy["APT29"] = {
    "super_label": Neo4jSuperLabel.THREAT_ACTOR,
    "tier": 3,  # Specific instance
    "parent_type": "APT_GROUP",
    "actorType": "nation_state_apt",
    "attribution": "Russia"
}
```

**Option 3: Re-classify existing tier1 nodes**
```cypher
// Move specific entity types from tier1 to tier2
MATCH (n:ThreatActor)
WHERE n.tier = 1 AND n.actorType = 'apt_group'
SET
    n.tier = 2,
    n.updated_at = datetime()
RETURN count(n) as reclassified;
```

---

## Ingestion Pipeline Failures

### Issue 3: Pipeline Fails with "NER11 API Not Responding"

**Error Message:**
```
requests.exceptions.ConnectionError: Failed to establish a new connection:
[Errno 111] Connection refused
```

**Diagnosis:**

1. **Check NER11 API status:**
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","service":"ner11"}
```

2. **Check API process:**
```bash
ps aux | grep ner11_api
# Should show running process
```

3. **Check API logs:**
```bash
tail -50 /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ner11_api.log
```

**Solution:**

**Step 1: Start NER11 API**
```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
nohup python3 api/ner11_api.py > logs/ner11_api.log 2>&1 &

# Verify startup
sleep 5
curl http://localhost:8000/health
```

**Step 2: Configure API auto-start**
```bash
# Create systemd service
sudo tee /etc/systemd/system/ner11-api.service > /dev/null <<'EOF'
[Unit]
Description=NER11 Entity Extraction API
After=network.target

[Service]
Type=simple
User=jim
WorkingDirectory=/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
ExecStart=/usr/bin/python3 /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/api/ner11_api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ner11-api
sudo systemctl start ner11-api
sudo systemctl status ner11-api
```

**Step 3: Retry failed ingestion**
```python
# Re-run pipeline for failed documents
from pipelines.ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

with NER11ToNeo4jPipeline() as pipeline:
    # Re-process failed documents
    stats = pipeline.process_document(text, doc_id)
```

---

### Issue 4: No Entities Extracted from Documents

**Symptom:**
```python
stats = pipeline.process_document(text, doc_id)
# stats['entities_extracted'] = 0
# stats['nodes_created'] = 0
```

**Diagnosis:**

1. **Check document length:**
```python
print(f"Document length: {len(text)} characters")
# Minimum: ~50 characters for meaningful extraction
```

2. **Check document language:**
```python
# NER11 expects English text
# Non-English text will not produce entities
```

3. **Test NER11 API directly:**
```bash
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text":"APT29 exploited CVE-2024-12345 using malware."}' | jq .

# Expected: {"entities": [{...}, {...}]}
```

**Root Causes:**
- Document too short (<50 characters)
- Document language not English
- Document contains no cybersecurity entities
- NER11 model not loaded properly

**Solution:**

**For short documents:**
```python
# Add length check before processing
MIN_LENGTH = 50

if len(text.strip()) < MIN_LENGTH:
    print(f"Skipping document {doc_id}: too short ({len(text)} chars)")
    continue
```

**For non-English documents:**
```python
# Add language detection (optional)
from langdetect import detect

try:
    lang = detect(text)
    if lang != 'en':
        print(f"Skipping document {doc_id}: language {lang} not supported")
        continue
except:
    pass  # Continue if detection fails
```

**For documents with no cybersecurity content:**
```python
# This is expected behavior
# Not every document will contain cybersecurity entities
# Log for review:
if stats['entities_extracted'] == 0:
    with open('/home/jim/2_OXOT_Projects_Dev/logs/no_entities.log', 'a') as f:
        f.write(f"{doc_id}: {text[:200]}...\n")
```

---

## Performance Problems

### Issue 5: Slow Query Performance on Hierarchical Queries

**Symptom:**
```cypher
// This query takes >10 seconds
MATCH (n) WHERE n.tier1 = 'TECHNICAL' RETURN count(n);
// Execution time: 12.3 seconds
```

**Diagnosis:**

1. **Check for indexes:**
```cypher
SHOW INDEXES;
// Look for indexes on: super_label, tier1, tier, hierarchy_path
```

2. **Explain query plan:**
```cypher
EXPLAIN MATCH (n) WHERE n.tier1 = 'TECHNICAL' RETURN count(n);
// Look for "NodeByLabelScan" (bad) vs "NodeIndexSeek" (good)
```

**Root Cause:**
- Missing indexes on hierarchical properties
- Neo4j doing full graph scans

**Solution:**

**Create indexes:**
```cypher
// Core hierarchical indexes
CREATE INDEX super_label_index IF NOT EXISTS FOR (n) ON (n.super_label);
CREATE INDEX tier1_index IF NOT EXISTS FOR (n) ON (n.tier1);
CREATE INDEX tier_index IF NOT EXISTS FOR (n) ON (n.tier);
CREATE INDEX hierarchy_path_index IF NOT EXISTS FOR (n) ON (n.hierarchy_path);

// Wait for indexes to build
SHOW INDEXES;
// Check "state" column - should be "ONLINE"
```

**Verify improvement:**
```cypher
// Re-run slow query
MATCH (n) WHERE n.tier1 = 'TECHNICAL' RETURN count(n);
// Expected execution time: <1 second
```

---

### Issue 6: Neo4j Running Out of Memory

**Symptom:**
```
Neo4j error: java.lang.OutOfMemoryError: GC overhead limit exceeded
```

**Diagnosis:**

1. **Check Neo4j heap usage:**
```cypher
CALL dbms.queryJmx("java.lang:type=Memory")
YIELD attributes
RETURN attributes.HeapMemoryUsage.value as heap;
```

2. **Check page cache usage:**
```cypher
CALL dbms.queryJmx("org.neo4j:*")
YIELD name, attributes
WHERE name CONTAINS "PageCache"
RETURN name, attributes;
```

**Root Cause:**
- Neo4j heap size too small for database size
- Too many concurrent queries
- Large batch operations

**Solution:**

**Step 1: Increase heap size**
```bash
# Edit Neo4j configuration
sudo nano /etc/neo4j/neo4j.conf

# Set heap size (50% of available RAM, max 31GB)
dbms.memory.heap.initial_size=8g
dbms.memory.heap.max_size=8g

# Set page cache (remaining RAM)
dbms.memory.pagecache.size=8g

# Restart Neo4j
sudo systemctl restart neo4j
```

**Step 2: Optimize batch operations**
```cypher
// Use APOC periodic commit for large updates
CALL apoc.periodic.iterate(
    'MATCH (n:CVE) WHERE n.super_label IS NULL RETURN n',
    'SET n.super_label = "Vulnerability", n.tier1 = "TECHNICAL"',
    {batchSize:1000, parallel:false}
)
YIELD batches, total
RETURN batches, total;
```

---

## Data Quality Issues

### Issue 7: Duplicate Nodes Created

**Symptom:**
```cypher
MATCH (n)
WITH labels(n)[0] as label, n.name as name, collect(n) as nodes
WHERE size(nodes) > 1
RETURN label, name, size(nodes) as duplicate_count
ORDER BY duplicate_count DESC
LIMIT 10;
// Returns duplicates
```

**Diagnosis:**

1. **Check if MERGE was used:**
```bash
# Search ingestion logs for CREATE vs MERGE
grep -r "CREATE (" /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/*.py
# Should only find MERGE statements in 05_ner11_to_neo4j_hierarchical.py
```

2. **Identify duplicate patterns:**
```cypher
// Detailed duplicate analysis
MATCH (n)
WITH labels(n)[0] as label, n.name as name, collect(n) as nodes
WHERE size(nodes) > 1
RETURN
    label,
    name,
    size(nodes) as count,
    [node in nodes | id(node)] as node_ids,
    [node in nodes | node.created_at][0] as first_created,
    [node in nodes | node.created_at][-1] as last_created;
```

**Root Cause:**
- Legacy pipeline used CREATE instead of MERGE
- Multiple ingestion runs without deduplication
- Different property values causing MERGE to fail (e.g., different `name` capitalization)

**Solution:**

**Step 1: Deduplicate existing data**
```cypher
// Deduplicate nodes by merging duplicates
MATCH (n)
WITH labels(n)[0] as label, n.name as name, collect(n) as nodes
WHERE size(nodes) > 1
CALL {
    WITH nodes
    // Keep first node, merge properties from others
    WITH nodes[0] as keep, tail(nodes) as duplicates
    UNWIND duplicates as dup
    // Merge relationships to kept node
    MATCH (dup)-[r]->(target)
    MERGE (keep)-[r2:type(r)]->(target)
    SET r2 += properties(r)
    DELETE r
    WITH keep, dup
    MATCH (source)-[r]->(dup)
    MERGE (source)-[r2:type(r)]->(keep)
    SET r2 += properties(r)
    DELETE r
    // Delete duplicate node
    DETACH DELETE dup
}
RETURN count(*) as deduplicated_groups;
```

**Step 2: Prevent future duplicates**
```cypher
// Create uniqueness constraints (prevents duplicates)
CREATE CONSTRAINT threatactor_name_unique IF NOT EXISTS
    FOR (n:ThreatActor) REQUIRE n.name IS UNIQUE;

CREATE CONSTRAINT malware_name_unique IF NOT EXISTS
    FOR (n:Malware) REQUIRE n.name IS UNIQUE;

CREATE CONSTRAINT vulnerability_name_unique IF NOT EXISTS
    FOR (n:Vulnerability) REQUIRE n.name IS UNIQUE;

// For CVE specifically
CREATE CONSTRAINT cve_name_unique IF NOT EXISTS
    FOR (n:CVE) REQUIRE n.name IS UNIQUE;
```

---

### Issue 8: Orphan Nodes (No Relationships)

**Symptom:**
```cypher
MATCH (n)
WHERE NOT (n)--()
RETURN labels(n)[0] as label, count(n) as orphan_count
ORDER BY orphan_count DESC;
// High orphan counts (>50% for some labels)
```

**Diagnosis:**

1. **Check which labels have orphans:**
```cypher
MATCH (n)
WHERE NOT (n)--()
RETURN labels(n)[0] as label, count(n) as count
ORDER BY count DESC
LIMIT 20;
```

2. **Check if relationships failed to create:**
```bash
# Review relationship creation logs
grep "relationship" /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/*.log | grep -i error
```

**Root Cause:**
- Entities imported without context (no related entities in same document)
- Relationship extraction failed due to distance threshold
- Source data lacks relationship information

**Solution:**

**For CVE orphans:**
```cypher
// Create relationships from CVE to Software (example)
MATCH (cve:CVE), (sw:Software)
WHERE cve.description CONTAINS sw.name
  AND NOT (cve)-[:AFFECTS]->(sw)
MERGE (cve)-[r:AFFECTS]->(sw)
SET r.confidence = 0.7, r.created_at = datetime()
RETURN count(r) as relationships_created;
```

**For entity proximity-based relationships:**
```cypher
// Create relationships based on co-occurrence patterns
MATCH (ta:ThreatActor), (m:Malware)
WHERE ta.description CONTAINS m.name OR m.description CONTAINS ta.name
  AND NOT (ta)-[:USES]->(m)
MERGE (ta)-[r:USES]->(m)
SET r.confidence = 0.8, r.created_at = datetime()
RETURN count(r) as relationships_created;
```

---

## Neo4j Database Issues

### Issue 9: Neo4j Won't Start

**Symptom:**
```bash
sudo systemctl start neo4j
# Fails to start
```

**Diagnosis:**

1. **Check Neo4j logs:**
```bash
sudo tail -100 /var/log/neo4j/neo4j.log
# Look for error messages
```

2. **Check disk space:**
```bash
df -h /var/lib/neo4j
# Need at least 10GB free space
```

3. **Check Java version:**
```bash
java -version
# Neo4j 5.x requires Java 17
```

**Common Root Causes:**

**A) Disk full:**
```bash
# Check disk usage
df -h

# Solution: Clear logs or old backups
sudo find /var/lib/neo4j/logs -name "*.log" -mtime +7 -delete
sudo find /var/lib/neo4j/backups -name "*.tar.gz" -mtime +30 -delete
```

**B) Corrupt database files:**
```bash
# Check for corruption
sudo neo4j-admin check-consistency --database=neo4j

# If corrupted, restore from backup
# See MAINTENANCE_GUIDE.md "Recovery Procedure"
```

**C) Port conflict:**
```bash
# Check if port 7687 already in use
sudo lsof -i :7687

# Solution: Kill conflicting process or change Neo4j port
```

---

### Issue 10: Neo4j Queries Timing Out

**Symptom:**
```cypher
MATCH (n) RETURN count(n);
// Error: Query timed out after 60 seconds
```

**Diagnosis:**

1. **Check active queries:**
```cypher
SHOW TRANSACTIONS;
// Look for long-running queries
```

2. **Check database size:**
```cypher
CALL apoc.meta.stats() YIELD nodeCount, relCount
RETURN nodeCount, relCount;
```

**Solution:**

**Step 1: Kill long-running queries**
```cypher
// Find long-running queries
SHOW TRANSACTIONS
WHERE elapsedTime.milliseconds > 60000;

// Kill specific transaction
TERMINATE TRANSACTIONS "transaction-id";
```

**Step 2: Increase query timeout**
```bash
# Edit Neo4j configuration
sudo nano /etc/neo4j/neo4j.conf

# Add/modify timeout setting
dbms.transaction.timeout=300s

# Restart Neo4j
sudo systemctl restart neo4j
```

---

## NER11 API Issues

### Issue 11: NER11 API Slow Response Times

**Symptom:**
```python
# Entity extraction taking >30 seconds per document
```

**Diagnosis:**

1. **Check API resource usage:**
```bash
# Monitor CPU and memory while API running
top -p $(pgrep -f ner11_api)
```

2. **Test API response time:**
```bash
time curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text":"Test document with APT29 malware."}' | jq .
```

**Root Cause:**
- Model not fully loaded into memory
- Insufficient CPU/GPU resources
- Too many concurrent requests

**Solution:**

**Optimize API performance:**
```python
# Edit NER11 API configuration
# File: /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/api/ner11_api.py

# Increase worker processes (if using gunicorn)
workers = 4  # Number of CPU cores

# Add model caching
from functools import lru_cache

@lru_cache(maxsize=1)
def load_model():
    # Model loaded once and cached
    return NER11Model()
```

---

## Emergency Procedures

### Emergency 1: Catastrophic Data Loss

**Symptom:**
```cypher
MATCH (n) RETURN count(n);
// Returns << 1,000,000 (significant loss)
```

**IMMEDIATE ACTIONS:**

1. **STOP all ingestion immediately:**
```bash
# Kill all ingestion processes
pkill -f "ner11_to_neo4j"
pkill -f "batch_ingest"

# Stop Neo4j
sudo systemctl stop neo4j
```

2. **Assess damage:**
```bash
# Check backup availability
ls -lh /var/lib/neo4j/backups/

# Check most recent backup
ls -lt /var/lib/neo4j/backups/ | head -5
```

3. **Restore from backup:**
```bash
# See MAINTENANCE_GUIDE.md "Recovery Procedure"
# Use most recent backup before data loss
```

4. **Contact escalation:**
```
Email: aeon-emergency@[domain]
Subject: CRITICAL: Neo4j Data Loss Detected
Body: [Include diagnostic output]
```

---

### Emergency 2: Schema Completely Broken

**Symptom:**
```cypher
// All hierarchical properties missing
MATCH (n) WHERE n.super_label IS NOT NULL RETURN count(n);
// Returns 0 or very low number
```

**IMMEDIATE ACTIONS:**

1. **Stop ingestion:**
```bash
pkill -f "ner11_to_neo4j"
```

2. **Backup current state (even if broken):**
```bash
sudo systemctl stop neo4j
sudo cp -r /var/lib/neo4j/data/databases/neo4j \
   /var/lib/neo4j/data/databases/neo4j.broken.$(date +%Y%m%d_%H%M%S)
sudo systemctl start neo4j
```

3. **Run schema fix:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts
python3 FIX_HIERARCHICAL_SCHEMA.py
```

4. **Validate fix:**
```bash
cypher-shell -u neo4j -p neo4j@openspg < VALIDATION_QUERIES.cypher
```

---

## Support Escalation

**Level 1: Self-Service**
- Check this troubleshooting guide
- Run quick diagnostic script
- Check known issues in documentation

**Level 2: Database Administrator**
- Email: dba@[domain]
- Slack: #aeon-database-ops
- Response time: 2 hours (business hours)

**Level 3: Architecture Team**
- Email: architecture@[domain]
- Slack: #aeon-architecture
- Response time: 4 hours (business hours)

**Level 4: Emergency Escalation**
- Email: aeon-emergency@[domain]
- Phone: [Emergency number]
- Response time: 30 minutes (24/7)

---

**Guide Prepared By:** AEON Documentation Specialist
**Last Updated:** 2025-12-12
**Next Review:** 2026-03-12 (quarterly)

**END OF TROUBLESHOOTING GUIDE**
