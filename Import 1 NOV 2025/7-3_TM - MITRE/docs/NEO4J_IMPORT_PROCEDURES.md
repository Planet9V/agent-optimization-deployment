# Neo4j MITRE ATT&CK Import Procedures

**Document Version:** 1.0
**Last Updated:** 2025-11-08
**Status:** ACTIVE

## Executive Summary

This document provides comprehensive procedures for importing MITRE ATT&CK data into Neo4j graph database. The import includes 2,051 entities and 40,886 bi-directional relationships representing the complete MITRE ATT&CK framework.

**Import Specifications:**
- **Source File:** `scripts/neo4j_mitre_import.cypher` (7.6 MB, 119,335 lines)
- **Entity Types:** 7 (Techniques, Mitigations, Threat Actors, Software, Campaigns, Data Sources, Data Components)
- **Total Nodes:** ~2,051
- **Total Relationships:** ~40,886 (bi-directional)
- **Estimated Import Time:** 5-15 minutes (depending on hardware)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Pre-Import Preparation](#pre-import-preparation)
3. [Execution Steps](#execution-steps)
4. [Validation](#validation)
5. [Troubleshooting](#troubleshooting)
6. [Rollback Procedures](#rollback-procedures)
7. [Performance Tuning](#performance-tuning)
8. [Post-Import Operations](#post-import-operations)
9. [Appendix](#appendix)

---

## Prerequisites

### System Requirements

**Minimum Requirements:**
- **Neo4j Version:** 4.4+ (Recommended: 5.0+)
- **RAM:** 4 GB minimum (8 GB recommended for optimal performance)
- **Disk Space:** 2 GB free space (for database + backups)
- **CPU:** 2+ cores recommended

**Optimal Configuration:**
- **Neo4j Version:** 5.x (latest stable)
- **RAM:** 16 GB+ (allows larger heap and page cache)
- **Disk Space:** 10 GB+ (for multiple backups and logs)
- **CPU:** 4+ cores (enables parallel query execution)
- **Storage:** SSD strongly recommended

### Software Prerequisites

1. **Neo4j Database:**
   ```bash
   # Verify Neo4j installation
   neo4j version

   # Should output something like:
   # neo4j 5.x.x
   ```

2. **Cypher Shell:**
   ```bash
   # Verify cypher-shell is available
   cypher-shell --version

   # Should output version information
   ```

3. **Python 3.8+ (for validation script):**
   ```bash
   # Check Python version
   python3 --version

   # Install Neo4j Python driver
   pip install neo4j
   ```

### Neo4j Configuration

**Recommended `neo4j.conf` settings for import:**

```properties
# Memory Settings (adjust based on available RAM)
dbms.memory.heap.initial_size=2g
dbms.memory.heap.max_size=4g
dbms.memory.pagecache.size=2g

# Transaction Settings (for large imports)
dbms.transaction.timeout=30m
db.transaction.concurrent.maximum=1000

# Query Settings
dbms.memory.transaction.global_max_size=1g
dbms.memory.transaction.max_size=512m

# Performance
dbms.jvm.additional=-XX:+UseG1GC
dbms.jvm.additional=-XX:+UnlockExperimentalVMOptions
dbms.jvm.additional=-XX:+UseJVMCICompiler
```

**Apply configuration changes:**
```bash
# Stop Neo4j
neo4j stop

# Edit configuration
sudo nano /etc/neo4j/neo4j.conf
# (or wherever your neo4j.conf is located)

# Start Neo4j
neo4j start

# Verify Neo4j is running
neo4j status
```

### Network Configuration

**Default Neo4j Ports:**
- **Bolt:** 7687 (binary protocol for queries)
- **HTTP:** 7474 (web interface)
- **HTTPS:** 7473 (secure web interface)

**Firewall Configuration (if needed):**
```bash
# Allow Neo4j ports
sudo ufw allow 7687/tcp
sudo ufw allow 7474/tcp
```

### Environment Setup

**Set environment variables:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_secure_password"

# Reload shell configuration
source ~/.bashrc
```

**Security Note:** Never commit passwords to version control. Use environment variables or secure credential management.

---

## Pre-Import Preparation

### 1. Database Health Check

**Verify Neo4j is running and accessible:**
```bash
# Check Neo4j status
neo4j status

# Test connection with cypher-shell
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" "RETURN 'Connected' AS status;"

# Should output: "Connected"
```

**Check current database state:**
```bash
# Count existing nodes
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" "MATCH (n) RETURN count(n) AS node_count;"

# Count existing relationships
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" "MATCH ()-[r]->() RETURN count(r) AS rel_count;"
```

### 2. Backup Existing Data

**Important:** Always backup before import, especially if database is not empty.

**Manual Backup (if using Community Edition):**
```bash
# Create backup directory
mkdir -p backups

# Export existing data
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" \
  "CALL apoc.export.cypher.all('backups/pre_import_backup.cypher', {})" \
  2>&1 | tee backups/backup.log

# Note: Requires APOC plugin installed
```

**Built-in Backup (Enterprise Edition only):**
```bash
# Stop Neo4j
neo4j stop

# Create backup
neo4j-admin database backup neo4j --to-path=backups/

# Start Neo4j
neo4j start
```

**Automated Backup (recommended):**
The import script `execute_neo4j_import.sh` includes automatic backup functionality:
```bash
# Backup is created automatically unless --skip-backup is specified
./scripts/execute_neo4j_import.sh
```

### 3. Verify Import Files

**Check Cypher script integrity:**
```bash
# Verify file exists and check size
ls -lh scripts/neo4j_mitre_import.cypher

# Should show approximately 7.6 MB

# Count lines
wc -l scripts/neo4j_mitre_import.cypher

# Should show 119,335 lines

# Validate syntax (check for obvious errors)
grep -n "syntax error\|ERROR" scripts/neo4j_mitre_import.cypher
# Should return no results
```

### 4. Resource Monitoring Setup

**Install monitoring tools (optional but recommended):**
```bash
# Install htop for system monitoring
sudo apt install htop

# Install neo4j-admin for database monitoring
# (usually included with Neo4j installation)
```

**Monitor during import:**
```bash
# Terminal 1: Monitor system resources
htop

# Terminal 2: Monitor Neo4j logs
tail -f /var/log/neo4j/neo4j.log

# Terminal 3: Run import script
./scripts/execute_neo4j_import.sh
```

---

## Execution Steps

### Method 1: Automated Execution (Recommended)

The automated script handles backup, import, monitoring, validation, and rollback.

**Basic execution:**
```bash
# Make script executable
chmod +x scripts/execute_neo4j_import.sh

# Set Neo4j password
export NEO4J_PASSWORD="your_password"

# Run import with automatic backup
./scripts/execute_neo4j_import.sh
```

**Execution with options:**
```bash
# Dry run (validate setup without importing)
./scripts/execute_neo4j_import.sh --dry-run

# Skip backup (faster, but no rollback capability)
./scripts/execute_neo4j_import.sh --skip-backup

# Custom batch size
./scripts/execute_neo4j_import.sh --batch-size 2000
```

**Expected output:**
```
==========================================
Neo4j MITRE ATT&CK Import Execution
==========================================
Timestamp: 20251108_143022
Neo4j URI: bolt://localhost:7687
Batch Size: 1000
Skip Backup: false
Dry Run: false
==========================================
[2025-11-08 14:30:22] Running pre-flight checks...
[2025-11-08 14:30:22] ✓ cypher-shell found
[2025-11-08 14:30:22] ✓ Cypher file found: 7.6M
[2025-11-08 14:30:22] ✓ Neo4j credentials configured
[2025-11-08 14:30:23] ✓ Neo4j connection established
[2025-11-08 14:30:23]   Neo4j version: 5.15.0
[2025-11-08 14:30:23]   Current database: 0 nodes, 0 relationships
[2025-11-08 14:30:24] ✓ Backup created: backups/neo4j_backup_20251108_143022.cypher
[2025-11-08 14:30:24] Starting MITRE ATT&CK import...
[2025-11-08 14:35:12] ✓ Import completed successfully in 288s
[2025-11-08 14:35:15] ✓ Validation complete
==========================================
Import completed successfully!
==========================================
```

### Method 2: Manual Execution

**Direct execution with cypher-shell:**
```bash
# Set environment variables
export NEO4J_PASSWORD="your_password"

# Execute import
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" -a bolt://localhost:7687 \
  --file scripts/neo4j_mitre_import.cypher \
  2>&1 | tee logs/import_manual_$(date +%Y%m%d_%H%M%S).log
```

**Manual batch execution (for very large databases or limited memory):**
```bash
# Split Cypher file by sections
csplit -f section_ scripts/neo4j_mitre_import.cypher '/^\/\/ MITRE ATT&CK/' '{*}'

# Execute each section separately
for section in section_*; do
  echo "Executing $section..."
  cypher-shell -u neo4j -p "$NEO4J_PASSWORD" --file "$section"
  sleep 5  # Brief pause between sections
done

# Clean up section files
rm section_*
```

### Method 3: Browser-Based Execution (Not Recommended)

**For small imports or testing only:**

1. Open Neo4j Browser: http://localhost:7474
2. Login with credentials
3. Upload Cypher file or paste content
4. Execute query

**Warning:** Browser execution may timeout on large imports. Use cypher-shell instead.

---

## Validation

### Automated Validation

**Run validation script:**
```bash
# Make script executable
chmod +x scripts/validate_neo4j_mitre_import.py

# Basic validation
python3 scripts/validate_neo4j_mitre_import.py

# Detailed validation with sample queries
python3 scripts/validate_neo4j_mitre_import.py --detailed

# Export validation report
python3 scripts/validate_neo4j_mitre_import.py \
  --detailed \
  --export-report reports/validation_$(date +%Y%m%d_%H%M%S).json
```

**Expected validation output:**
```
============================================================
ENTITY COUNT VALIDATION
============================================================
✓ AttackTechnique    :  823 (expected:  823, variance: 0)
✓ Mitigation        :   46 (expected:   46, variance: 0)
✓ ThreatActor       :  152 (expected:  152, variance: 0)
✓ Software          :  747 (expected:  747, variance: 0)
✓ Campaign          :   36 (expected:   36, variance: 0)
✓ DataSource        :   39 (expected:   39, variance: 0)
✓ DataComponent     :  208 (expected:  208, variance: 0)
------------------------------------------------------------
✓ TOTAL NODES: 2051 (expected: ~2051)

============================================================
RELATIONSHIP COUNT VALIDATION
============================================================
  USES                     :  19234
  USED_BY                  :  19234
  MITIGATES                :   1485
  MITIGATED_BY             :   1485
  ...
------------------------------------------------------------
✓ TOTAL RELATIONSHIPS: 40886 (expected: ~40886, variance: 0)

============================================================
BI-DIRECTIONAL RELATIONSHIP INTEGRITY
============================================================
✓ USES                ↔ USED_BY
   Forward:  19234 | Reverse:  19234
✓ MITIGATES           ↔ MITIGATED_BY
   Forward:   1485 | Reverse:   1485
...

============================================================
VALIDATION SUMMARY
============================================================
Total Checks: 8
Passed: 8
Failed: 0

OVERALL STATUS: PASSED
============================================================
```

### Manual Validation Queries

**Quick validation queries:**
```cypher
// Count nodes by type
MATCH (n)
RETURN labels(n)[0] AS type, count(n) AS count
ORDER BY count DESC;

// Count relationships by type
CALL db.relationshipTypes()
YIELD relationshipType
CALL {
  WITH relationshipType
  MATCH ()-[r]->()
  WHERE type(r) = relationshipType
  RETURN count(r) AS count
}
RETURN relationshipType, count
ORDER BY count DESC;

// Verify bi-directional integrity
MATCH ()-[r:USES]->()
WITH count(r) AS uses_count
MATCH ()-[r:USED_BY]->()
WITH uses_count, count(r) AS used_by_count
RETURN uses_count, used_by_count,
       uses_count = used_by_count AS is_valid;

// Sample data check: Top techniques used by threat actors
MATCH (actor:ThreatActor)-[:USES]->(tech:AttackTechnique)
RETURN tech.id, tech.name, count(actor) AS threat_actor_count
ORDER BY threat_actor_count DESC
LIMIT 10;
```

---

## Troubleshooting

### Common Issues

#### 1. Connection Refused Error

**Symptom:**
```
ServiceUnavailable: Unable to connect to bolt://localhost:7687
```

**Solutions:**
```bash
# Check if Neo4j is running
neo4j status

# If not running, start it
neo4j start

# Check if correct port is being used
netstat -tulpn | grep 7687

# Verify Neo4j configuration
cat /etc/neo4j/neo4j.conf | grep bolt

# Check logs for startup errors
tail -100 /var/log/neo4j/neo4j.log
```

#### 2. Authentication Failed

**Symptom:**
```
ClientError: The client is unauthorized due to authentication failure.
```

**Solutions:**
```bash
# Reset Neo4j password
neo4j-admin dbms set-initial-password new_password

# Restart Neo4j
neo4j restart

# Try connection again
cypher-shell -u neo4j -p new_password "RETURN 'Connected';"
```

#### 3. Out of Memory Error

**Symptom:**
```
OutOfMemoryError: Java heap space
```

**Solutions:**
```bash
# Stop Neo4j
neo4j stop

# Edit neo4j.conf to increase heap
sudo nano /etc/neo4j/neo4j.conf

# Increase these values:
# dbms.memory.heap.initial_size=4g
# dbms.memory.heap.max_size=8g

# Start Neo4j
neo4j start

# Retry import with smaller batch size
./scripts/execute_neo4j_import.sh --batch-size 500
```

#### 4. Transaction Timeout

**Symptom:**
```
TransientError: Transaction timeout after 300s
```

**Solutions:**
```bash
# Increase transaction timeout in neo4j.conf
dbms.transaction.timeout=30m

# Restart Neo4j
neo4j restart

# Or execute in smaller batches manually
```

#### 5. Import Hangs or Freezes

**Symptom:**
Import appears to hang with no progress.

**Solutions:**
```bash
# Check system resources
htop  # Look for high CPU/memory usage

# Check Neo4j logs in another terminal
tail -f /var/log/neo4j/neo4j.log

# Monitor database activity
watch -n 5 "cypher-shell -u neo4j -p \$NEO4J_PASSWORD \
  'MATCH (n) RETURN count(n) AS nodes;'"

# If truly hung, stop and restart:
# 1. Kill cypher-shell process
pkill -f cypher-shell

# 2. Check database integrity
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" "CALL db.ping();"

# 3. Retry import
```

#### 6. Partial Import (Some Data Missing)

**Symptom:**
Validation shows some entities missing.

**Solutions:**
```cypher
// Check which batches succeeded
MATCH (t:AttackTechnique)
WITH substring(t.id, 0, 5) AS prefix, count(t) AS count
RETURN prefix, count
ORDER BY prefix;

// Re-run specific failed sections from Cypher file
// Extract and execute only failed batches
```

### Performance Issues

**Slow import (>30 minutes):**

1. **Increase memory allocation:**
   ```properties
   dbms.memory.heap.max_size=8g
   dbms.memory.pagecache.size=4g
   ```

2. **Disable unnecessary features during import:**
   ```cypher
   // Run before import
   CALL db.index.fulltext.stop();

   // Run after import
   CALL db.index.fulltext.start();
   ```

3. **Use batch import mode (if available):**
   ```bash
   neo4j-admin database import full \
     --nodes=nodes.csv \
     --relationships=relationships.csv \
     neo4j
   ```

### Disk Space Issues

**Check disk usage:**
```bash
# Check available disk space
df -h /var/lib/neo4j

# Check database size
du -sh /var/lib/neo4j/data

# Clean up old backups if needed
rm backups/neo4j_backup_*.cypher
```

---

## Rollback Procedures

### Automatic Rollback

The import script automatically rolls back on failure (if backup was created):

```bash
# Import with automatic rollback on failure
./scripts/execute_neo4j_import.sh

# On failure, database is automatically cleared
# and can be restored from backup
```

### Manual Rollback

**If import script is not used:**

```bash
# 1. Stop any running imports
pkill -f cypher-shell

# 2. Clear database
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" <<EOF
MATCH (n) DETACH DELETE n;
EOF

# 3. Verify database is empty
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" \
  "MATCH (n) RETURN count(n) AS count;"

# Should return: count: 0
```

### Restore from Backup

**Restore from Cypher export:**
```bash
# If you have a Cypher backup file
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" \
  --file backups/neo4j_backup_TIMESTAMP.cypher
```

**Restore from Neo4j backup (Enterprise):**
```bash
# Stop Neo4j
neo4j stop

# Restore from backup
neo4j-admin database restore neo4j \
  --from-path=backups/backup_TIMESTAMP/

# Start Neo4j
neo4j start

# Verify restoration
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" \
  "MATCH (n) RETURN count(n) AS count;"
```

---

## Performance Tuning

### Pre-Import Optimization

**Disable unnecessary features:**
```cypher
// Disable monitoring during import
CALL dbms.setConfigValue('metrics.enabled', 'false');

// Increase write buffer
CALL dbms.setConfigValue('dbms.memory.transaction.max_size', '1g');
```

### Memory Configuration

**Optimal settings for 16GB RAM system:**
```properties
# Heap (40-50% of RAM for Neo4j process)
dbms.memory.heap.initial_size=4g
dbms.memory.heap.max_size=6g

# Page cache (remaining available RAM)
dbms.memory.pagecache.size=6g

# Transaction memory
dbms.memory.transaction.global_max_size=2g
dbms.memory.transaction.max_size=1g
```

**For 8GB RAM system:**
```properties
dbms.memory.heap.initial_size=2g
dbms.memory.heap.max_size=3g
dbms.memory.pagecache.size=3g
dbms.memory.transaction.max_size=512m
```

### Post-Import Optimization

**Create additional indexes for performance:**
```cypher
// Create indexes on commonly queried properties
CREATE INDEX technique_tactic IF NOT EXISTS
FOR (t:AttackTechnique) ON (t.tactics);

CREATE INDEX threat_actor_alias IF NOT EXISTS
FOR (a:ThreatActor) ON (a.aliases);

CREATE INDEX software_type IF NOT EXISTS
FOR (s:Software) ON (s.type);

// Full-text search indexes
CREATE FULLTEXT INDEX technique_description IF NOT EXISTS
FOR (t:AttackTechnique) ON EACH [t.name, t.description];

CREATE FULLTEXT INDEX threat_actor_name IF NOT EXISTS
FOR (a:ThreatActor) ON EACH [a.name, a.description];
```

**Warm up caches:**
```cypher
// Load frequently accessed data into page cache
MATCH (t:AttackTechnique) RETURN count(t);
MATCH (a:ThreatActor) RETURN count(a);
MATCH ()-[r:USES]->() RETURN count(r);
```

---

## Post-Import Operations

### Verify Import Completeness

```bash
# Run comprehensive validation
python3 scripts/validate_neo4j_mitre_import.py --detailed

# Export validation report
python3 scripts/validate_neo4j_mitre_import.py \
  --export-report reports/post_import_validation.json
```

### Create Derived Data

**Add computed properties:**
```cypher
// Add technique complexity score (based on relationship count)
MATCH (t:AttackTechnique)
OPTIONAL MATCH (t)-[r]-()
WITH t, count(r) AS rel_count
SET t.complexity_score = rel_count;

// Add threat actor activity score
MATCH (a:ThreatActor)
OPTIONAL MATCH (a)-[:USES]->(tech:AttackTechnique)
WITH a, count(tech) AS tech_count
SET a.activity_score = tech_count;
```

### Setup Monitoring

**Create monitoring queries:**
```cypher
// Database health check
CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Store sizes')
YIELD attributes
RETURN attributes.TotalStoreSize.value AS store_size;

// Monitor query performance
CALL dbms.listQueries()
YIELD query, elapsedTimeMillis, allocatedBytes
WHERE elapsedTimeMillis > 1000
RETURN query, elapsedTimeMillis, allocatedBytes
ORDER BY elapsedTimeMillis DESC;
```

### Schedule Regular Backups

**Cron job for daily backups:**
```bash
# Add to crontab (crontab -e)
0 2 * * * /opt/neo4j/bin/neo4j-admin database backup neo4j --to-path=/backups/$(date +\%Y\%m\%d) 2>&1 | logger -t neo4j-backup
```

---

## Appendix

### A. Expected Entity Counts

| Entity Type | Count |
|------------|-------|
| AttackTechnique | 823 |
| Mitigation | 46 |
| ThreatActor | 152 |
| Software | 747 |
| Campaign | 36 |
| DataSource | 39 |
| DataComponent | 208 |
| **TOTAL** | **2,051** |

### B. Expected Relationship Counts

| Relationship Type | Count (each direction) |
|------------------|----------------------|
| USES / USED_BY | ~19,234 |
| MITIGATES / MITIGATED_BY | ~1,485 |
| DETECTS / DETECTED_BY | ~1,800 |
| SUBTECHNIQUE_OF / HAS_SUBTECHNIQUE | ~570 |
| Others | ~17,797 |
| **TOTAL** | **~40,886** |

### C. File Structure

```
project/
├── scripts/
│   ├── neo4j_mitre_import.cypher      # Main import file (7.6 MB)
│   ├── execute_neo4j_import.sh        # Automated import script
│   └── validate_neo4j_mitre_import.py # Validation script
├── docs/
│   └── NEO4J_IMPORT_PROCEDURES.md     # This document
├── backups/
│   └── [auto-generated backups]
├── logs/
│   └── [import logs]
└── reports/
    └── [validation reports]
```

### D. Environment Variables Reference

```bash
# Required
NEO4J_PASSWORD="your_secure_password"

# Optional (with defaults)
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
BATCH_SIZE="1000"
```

### E. Quick Reference Commands

```bash
# Check Neo4j status
neo4j status

# Start/stop Neo4j
neo4j start
neo4j stop
neo4j restart

# Connect to database
cypher-shell -u neo4j -p "$NEO4J_PASSWORD"

# Run import
./scripts/execute_neo4j_import.sh

# Validate import
python3 scripts/validate_neo4j_mitre_import.py --detailed

# Clear database
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" "MATCH (n) DETACH DELETE n;"

# Count nodes
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" "MATCH (n) RETURN count(n);"

# View logs
tail -f /var/log/neo4j/neo4j.log
```

### F. Support and Resources

**Neo4j Documentation:**
- Official Docs: https://neo4j.com/docs/
- Cypher Manual: https://neo4j.com/docs/cypher-manual/
- Operations Manual: https://neo4j.com/docs/operations-manual/

**MITRE ATT&CK:**
- Official Website: https://attack.mitre.org/
- Matrix Navigator: https://mitre-attack.github.io/attack-navigator/

**Community Resources:**
- Neo4j Community Forum: https://community.neo4j.com/
- Stack Overflow: https://stackoverflow.com/questions/tagged/neo4j

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-08 | Initial release with complete import procedures |

---

**End of Document**
