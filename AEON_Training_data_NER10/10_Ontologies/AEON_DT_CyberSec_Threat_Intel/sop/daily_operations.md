# Daily Operations Checklist

**File**: daily_operations.md
**Purpose**: Daily operational tasks and monitoring for AEON DT CyberSec Threat Intelligence
**Frequency**: Daily
**Estimated Time**: 30-45 minutes

---

## Morning Operations (8:00 AM)

### System Health Check
- [ ] Verify Neo4j service is running: `systemctl status neo4j`
- [ ] Check disk space: `df -h` (minimum 20% free)
- [ ] Monitor memory usage: `free -h` (ensure < 80% used)
- [ ] Review overnight processing logs: `tail -100 /var/log/aeon_ingestion.log`
- [ ] Check for failed jobs: `grep "ERROR\|FAILED" /var/log/aeon_*.log`

### Database Status
- [ ] Connect to Neo4j: `python3 scripts/test_connection.py`
- [ ] Verify node counts: Query total nodes and compare to yesterday
- [ ] Check recent updates: Count nodes updated in last 24 hours
- [ ] Review orphaned nodes: Run orphan detection query
- [ ] Validate index health: `SHOW INDEXES` in Neo4j Browser

**Neo4j Health Query**:
```cypher
MATCH (n)
WHERE n.updated_at > datetime() - duration('P1D')
RETURN labels(n)[0] as type, count(n) as updates_last_24h
ORDER BY updates_last_24h DESC
```

### NVD API Update
- [ ] Check last NVD sync timestamp in Neo4j
- [ ] Verify NVD_API_KEY is set: `echo $NVD_API_KEY | wc -c` (should be > 36)
- [ ] Review NVD update logs: `tail -50 /var/log/aeon_nvd_updates.log`
- [ ] Verify CVE freshness (< 2 hours old): Run freshness report
- [ ] Check for API errors: `grep "NVD-\|ERROR" /var/log/aeon_nvd_updates.log`

---

## Midday Operations (12:00 PM)

### Document Ingestion
- [ ] Count documents in incoming: `ls -1 data/staging/incoming | wc -l`
- [ ] Review documents in processing: Check for stuck documents
- [ ] Count successful ingestions today: Check completed directory
- [ ] Review failed ingestions: Analyze failed directory
- [ ] Check ingestion error log: `tail -50 data/logs/errors/ingestion_*.log`

**Ingestion Status Command**:
```bash
echo "Incoming: $(ls -1 data/staging/incoming | wc -l)"
echo "Processing: $(ls -1 data/staging/processing | wc -l)"
echo "Completed today: $(find data/staging/completed -name "*.meta.json" -mtime -1 | wc -l)"
echo "Failed today: $(find data/staging/failed -name "*.meta.json" -mtime -1 | wc -l)"
```

### Performance Monitoring
- [ ] Check query response times: Run performance test suite
- [ ] Monitor database size growth: Compare to last week
- [ ] Review slow query log: Identify queries > 3 seconds
- [ ] Check connection pool usage: Monitor active connections
- [ ] Verify batch import performance: Review import metrics

---

## Afternoon Operations (4:00 PM)

### Quality Assurance
- [ ] Run duplicate detection: Execute deduplication script
- [ ] Validate data integrity: Run data quality diagnostics
- [ ] Check relationship consistency: Verify bidirectional relationships
- [ ] Review entity classification confidence: Check low-confidence entities
- [ ] Validate CVSS scores: Ensure all in range 0.0-10.0

**Quality Check Commands**:
```bash
# Run data quality diagnostics
python3 scripts/data_quality_diagnostics.py

# Check for duplicates
python3 scripts/detect_duplicates.py --report

# Validate relationships
python3 scripts/validate_relationships.py
```

### Backup Verification
- [ ] Verify last backup timestamp: Check backup log
- [ ] Confirm backup size: Compare to database size
- [ ] Test backup integrity: Random restore test (weekly)
- [ ] Check backup storage space: Ensure adequate space
- [ ] Review backup rotation: Verify old backups archived

---

## End-of-Day Operations (6:00 PM)

### Audit & Reporting
- [ ] Generate daily statistics report: Run metrics script
- [ ] Review ingestion success rate: Calculate % successful
- [ ] Document any incidents: Update incident log
- [ ] Prepare summary for stakeholders: Key metrics
- [ ] Archive daily logs: Rotate logs to archive directory

**Daily Metrics Script**:
```bash
#!/bin/bash
# daily_metrics.sh

DATE=$(date '+%Y-%m-%d')

echo "=== AEON DT Daily Metrics: $DATE ==="

# Node counts
python3 - <<EOF
from neo4j import GraphDatabase
import os

driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))

with driver.session() as session:
    result = session.run("MATCH (n) RETURN count(n) as total")
    print(f"Total nodes: {result.single()['total']:,}")

    result = session.run("MATCH ()-[r]->() RETURN count(r) as total")
    print(f"Total relationships: {result.single()['total']:,}")

    result = session.run("""
        MATCH (v:Vulnerability)
        WHERE date(v.published) = date()
        RETURN count(v) as new_cves
    """)
    print(f"New CVEs today: {result.single()['new_cves']}")

driver.close()
EOF

# Ingestion stats
COMPLETED=$(find data/staging/completed -name "*.meta.json" -mtime -1 | wc -l)
FAILED=$(find data/staging/failed -name "*.meta.json" -mtime -1 | wc -l)
SUCCESS_RATE=$(awk "BEGIN {printf \"%.1f\", ($COMPLETED/($COMPLETED+$FAILED))*100}")

echo "Documents ingested: $COMPLETED"
echo "Documents failed: $FAILED"
echo "Success rate: $SUCCESS_RATE%"
```

### System Cleanup
- [ ] Clean temporary files: `find /tmp/aeon_* -mtime +1 -delete`
- [ ] Rotate logs: Execute logrotate
- [ ] Archive completed documents: Move to long-term storage
- [ ] Clean failed documents: Review and re-attempt or archive
- [ ] Update operations log: Record day's activities

### Preparation for Next Day
- [ ] Review scheduled maintenance: Check weekly/monthly tasks
- [ ] Prepare document queue: Stage documents for tomorrow
- [ ] Check system updates: Review pending updates
- [ ] Document any issues: Update issue tracker
- [ ] Set up monitoring alerts: Ensure alerts active overnight

---

## Emergency Contacts

**On-Call Rotation**: Check current on-call schedule
**Technical Lead**: [Contact Info]
**Database Administrator**: [Contact Info]
**Security Team**: [Contact Info]

---

## Escalation Criteria

**Immediate Escalation Required**:
- Neo4j service down > 15 minutes
- Data corruption detected
- Security breach indicators
- Disk space < 10% free
- NVD API unavailable > 4 hours

**Next Business Day Escalation**:
- Performance degradation > 20%
- Ingestion failure rate > 10%
- Duplicate entity increase > 5%
- Slow query count increase > 15%

---

## Daily Metrics Targets

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| System Uptime | 99.9% | < 99.5% |
| Ingestion Success Rate | > 95% | < 90% |
| Average Query Time | < 500ms | > 1000ms |
| NVD Sync Latency | < 2 hours | > 4 hours |
| Disk Space Free | > 20% | < 15% |
| Memory Usage | < 80% | > 90% |
| Duplicate Entities | < 0.1% | > 0.5% |
| Orphaned Nodes | < 100 | > 500 |

---

**Last Updated**: 2025-10-29
**Review Frequency**: Monthly
**Version**: 1.0.0
