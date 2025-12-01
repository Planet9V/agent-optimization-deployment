# Weekly Maintenance Procedures

**File**: weekly_maintenance.md
**Purpose**: Weekly maintenance tasks for AEON DT CyberSec Threat Intelligence
**Frequency**: Weekly (Sunday 2:00 AM)
**Estimated Time**: 2-3 hours
**Maintenance Window**: Sunday 2:00 AM - 5:00 AM

---

## Pre-Maintenance Checklist

### Preparation (Saturday Evening)
- [ ] Notify users of maintenance window (if applicable)
- [ ] Review change log for any pending updates
- [ ] Verify backup systems operational
- [ ] Check disk space (minimum 30% free required)
- [ ] Document current system state
- [ ] Prepare rollback plan

### Pre-Maintenance Snapshot
- [ ] Create database snapshot: `scripts/create_snapshot.sh`
- [ ] Export current metrics: `scripts/export_metrics.sh`
- [ ] Backup configuration files
- [ ] Record current performance baseline
- [ ] Save current node/relationship counts

---

## Database Maintenance (2:00 AM - 3:30 AM)

### Backup & Archive
- [ ] Create full Neo4j backup: `neo4j-admin backup --to=/backups/$(date +%Y%m%d)`
- [ ] Verify backup integrity: Test random restore
- [ ] Archive old backups (> 30 days): Move to long-term storage
- [ ] Clean backup directory: Remove temporary files
- [ ] Update backup rotation log

**Backup Script**:
```bash
#!/bin/bash
# weekly_backup.sh

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/weekly/$BACKUP_DATE"

echo "=== Weekly Backup: $BACKUP_DATE ==="

# Stop Neo4j for consistent backup
sudo systemctl stop neo4j
sleep 10

# Create backup
neo4j-admin backup --backup-dir="$BACKUP_DIR" --database=neo4j

# Restart Neo4j
sudo systemctl start neo4j
sleep 15

# Verify backup
if [ -d "$BACKUP_DIR" ]; then
    SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
    echo "✓ Backup created: $BACKUP_DIR ($SIZE)"
else
    echo "✗ Backup failed"
    exit 1
fi

# Archive old backups
find /backups/weekly -maxdepth 1 -type d -mtime +30 -exec mv {} /backups/archive/ \;

echo "✓ Backup complete"
```

### Database Optimization
- [ ] Rebuild all indexes: Execute index rebuild script
- [ ] Update statistics: `CALL db.stats.retrieve()`
- [ ] Compact database: Run compaction if fragmentation > 20%
- [ ] Optimize query cache: Clear and warm cache
- [ ] Review execution plans: Analyze slow queries

**Index Rebuild**:
```cypher
// Rebuild all indexes for optimal performance
CALL db.indexes() YIELD name
WITH name WHERE name STARTS WITH 'vuln_' OR name STARTS WITH 'threat_'
CALL {
    WITH name
    CALL apoc.cypher.run('DROP INDEX ' + name, {}) YIELD value
    RETURN value
}
// Recreate indexes
CREATE INDEX vuln_cve_idx IF NOT EXISTS FOR (v:Vulnerability) ON (v.cve_id);
CREATE INDEX vuln_cvss_idx IF NOT EXISTS FOR (v:Vulnerability) ON (v.cvss_score);
CREATE INDEX threat_actor_name_idx IF NOT EXISTS FOR (t:ThreatActor) ON (t.name);
CREATE INDEX malware_name_idx IF NOT EXISTS FOR (m:Malware) ON (m.name);
```

### Data Quality Maintenance
- [ ] Run deduplication across all entity types
- [ ] Remove orphaned nodes (< 100 expected)
- [ ] Validate relationship integrity
- [ ] Update entity classifications
- [ ] Standardize naming conventions

**Deduplication Script**:
```bash
#!/bin/bash
# weekly_deduplication.sh

echo "=== Weekly Deduplication ==="

for entity_type in ThreatActor Malware Vulnerability Tool Campaign Organization; do
    echo "Processing $entity_type..."
    python3 - <<EOF
from neo4j import GraphDatabase
import os

driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))

with driver.session() as session:
    result = session.run(f"""
        MATCH (e:$entity_type)
        WITH toLower(e.name) as norm_name, collect(e) as entities
        WHERE size(entities) > 1
        WITH entities
        UNWIND tail(entities) as duplicate
        MATCH (duplicate)-[r]-()
        DELETE r, duplicate
        RETURN count(*) as deleted
    """)
    deleted = result.single()['deleted']
    print(f"  Removed {deleted} {entity_type} duplicates")

driver.close()
EOF
done
```

---

## Performance Tuning (3:30 AM - 4:15 AM)

### Query Performance Analysis
- [ ] Identify slow queries (> 3 seconds): Review slow query log
- [ ] Analyze execution plans: Run EXPLAIN on slow queries
- [ ] Optimize query patterns: Refactor inefficient queries
- [ ] Update query cache settings
- [ ] Document performance improvements

**Performance Analysis**:
```python
# weekly_performance_analysis.py
from neo4j import GraphDatabase
import os
import time

driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))

test_queries = [
    ("Count all nodes", "MATCH (n) RETURN count(n)"),
    ("High CVSS vulnerabilities", "MATCH (v:Vulnerability) WHERE v.cvss_score > 9.0 RETURN v LIMIT 100"),
    ("Threat actor relationships", "MATCH (t:ThreatActor)-[r]->(m:Malware) RETURN t, r, m LIMIT 50"),
    ("Recent CVEs", "MATCH (v:Vulnerability) WHERE v.published > date() - duration('P7D') RETURN v"),
]

print("=== Weekly Performance Analysis ===\n")

for description, query in test_queries:
    with driver.session() as session:
        start = time.time()
        result = session.run(query)
        _ = list(result)
        duration = time.time() - start

        status = "✓" if duration < 1.0 else "⚠" if duration < 3.0 else "✗"
        print(f"{status} {description}: {duration:.3f}s")

driver.close()
```

### Resource Optimization
- [ ] Analyze memory usage patterns
- [ ] Review connection pool configuration
- [ ] Optimize JVM heap settings (if needed)
- [ ] Clean transaction logs
- [ ] Review and adjust cache sizes

### Index Maintenance
- [ ] Verify all required indexes exist
- [ ] Check index usage statistics
- [ ] Remove unused indexes
- [ ] Update index provider settings
- [ ] Rebuild fragmented indexes

---

## Security & Compliance (4:15 AM - 4:45 AM)

### Security Audit
- [ ] Review access logs: Check for unusual activity
- [ ] Validate user permissions: Ensure least privilege
- [ ] Update passwords (quarterly rotation): Check rotation schedule
- [ ] Review API key usage: Check NVD API key status
- [ ] Scan for security vulnerabilities: Run security scanner

**Security Audit Script**:
```bash
#!/bin/bash
# weekly_security_audit.sh

echo "=== Weekly Security Audit ==="

# Check Neo4j access logs
echo "[1/5] Analyzing access logs..."
grep "authentication\|unauthorized" /var/log/neo4j/*.log | tail -20

# Check file permissions
echo "[2/5] Verifying file permissions..."
find /home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel -type f -perm /o+w | head -10

# Validate API keys
echo "[3/5] Checking API keys..."
if [ -n "$NVD_API_KEY" ]; then
    echo "  ✓ NVD_API_KEY is set"
else
    echo "  ✗ NVD_API_KEY is missing"
fi

# Check for exposed secrets
echo "[4/5] Scanning for exposed secrets..."
grep -r "password\|api_key\|secret" --include="*.py" --include="*.sh" scripts/ | grep -v "getenv\|#" || echo "  ✓ No exposed secrets found"

# Review user access
echo "[5/5] Reviewing database users..."
python3 - <<EOF
from neo4j import GraphDatabase
import os

driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))

with driver.session() as session:
    result = session.run("SHOW USERS")
    for user in result:
        print(f"  User: {user['user']} - Roles: {user['roles']}")

driver.close()
EOF
```

### Compliance Validation
- [ ] Verify data retention policies: Archive old data
- [ ] Validate audit trail completeness
- [ ] Generate compliance report
- [ ] Review data privacy controls
- [ ] Document compliance status

---

## System Updates (4:45 AM - 5:00 AM)

### Software Updates
- [ ] Check for Neo4j updates: Review release notes
- [ ] Update Python packages: `pip list --outdated`
- [ ] Update Claude-Flow: `npm update -g claude-flow@alpha`
- [ ] Update spaCy models: Check for model updates
- [ ] Review and install security patches

**Update Check Script**:
```bash
#!/bin/bash
# check_updates.sh

echo "=== Weekly Update Check ==="

# Neo4j version
echo "Neo4j version:"
neo4j version

# Python packages
echo -e "\nOutdated Python packages:"
pip list --outdated | head -10

# Claude-Flow version
echo -e "\nClaude-Flow version:"
npx claude-flow@alpha --version

# System updates
echo -e "\nSystem updates available:"
apt list --upgradable 2>/dev/null | head -10
```

### Configuration Review
- [ ] Review neo4j.conf settings
- [ ] Validate environment variables
- [ ] Check log rotation configuration
- [ ] Review backup schedules
- [ ] Update documentation if needed

---

## Post-Maintenance Validation

### System Verification
- [ ] Verify Neo4j service running: `systemctl status neo4j`
- [ ] Test database connectivity: Run connection test
- [ ] Validate query performance: Run performance tests
- [ ] Check all indexes operational: `SHOW INDEXES`
- [ ] Verify data integrity: Run quality checks

**Post-Maintenance Validation**:
```bash
#!/bin/bash
# post_maintenance_validation.sh

echo "=== Post-Maintenance Validation ==="

# Service status
systemctl is-active --quiet neo4j && echo "✓ Neo4j is running" || echo "✗ Neo4j is NOT running"

# Connection test
python3 -c "from neo4j import GraphDatabase; import os; GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))).verify_connectivity(); print('✓ Connection successful')"

# Performance test
python3 scripts/weekly_performance_analysis.py

# Data integrity
python3 scripts/data_quality_diagnostics.py

echo -e "\n✓ Post-maintenance validation complete"
```

### Metrics Comparison
- [ ] Compare pre/post node counts: Should match
- [ ] Verify performance improvements: Document gains
- [ ] Check backup completion: Confirm backup exists
- [ ] Review any errors: Document issues
- [ ] Generate weekly report

---

## Maintenance Report Template

```markdown
# Weekly Maintenance Report - [DATE]

## Maintenance Summary
- Start Time: [TIME]
- End Time: [TIME]
- Duration: [DURATION]
- Status: [SUCCESS/PARTIAL/FAILED]

## Activities Completed
- [x] Database backup
- [x] Index rebuild
- [x] Deduplication
- [x] Performance tuning
- [x] Security audit
- [x] Software updates

## Metrics
- Nodes before: [COUNT]
- Nodes after: [COUNT]
- Duplicates removed: [COUNT]
- Backup size: [SIZE]
- Performance improvement: [PERCENTAGE]

## Issues Encountered
[List any issues and resolutions]

## Recommendations
[List any recommendations for next maintenance]

## Next Maintenance
- Scheduled: [NEXT SUNDAY DATE]
- Special tasks: [ANY SPECIAL TASKS]
```

---

## Emergency Rollback Procedure

If issues occur during maintenance:

1. **Stop current operations**: Kill running processes
2. **Restore from snapshot**: `scripts/restore_snapshot.sh [SNAPSHOT_ID]`
3. **Verify restoration**: Run validation tests
4. **Document issues**: Record what went wrong
5. **Escalate if needed**: Contact technical lead

**Rollback Command**:
```bash
#!/bin/bash
# rollback_maintenance.sh

SNAPSHOT_ID=$1

if [ -z "$SNAPSHOT_ID" ]; then
    echo "Usage: $0 <snapshot_id>"
    exit 1
fi

echo "Rolling back to snapshot: $SNAPSHOT_ID"

# Stop Neo4j
sudo systemctl stop neo4j

# Restore from snapshot
neo4j-admin restore --from="/backups/snapshots/$SNAPSHOT_ID" --database=neo4j

# Start Neo4j
sudo systemctl start neo4j
sleep 15

# Verify
python3 scripts/test_connection.py && echo "✓ Rollback successful" || echo "✗ Rollback failed"
```

---

**Last Updated**: 2025-10-29
**Review Frequency**: Quarterly
**Version**: 1.0.0
**Approved By**: AEON DT Technical Lead
