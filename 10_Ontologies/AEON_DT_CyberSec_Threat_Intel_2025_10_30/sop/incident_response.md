# Incident Response Procedures

**File**: incident_response.md
**Purpose**: Emergency incident response procedures for AEON DT CyberSec Threat Intelligence
**Classification**: CRITICAL
**Distribution**: Operations Team Only

---

## Incident Severity Levels

| Level | Description | Response Time | Escalation |
|-------|-------------|---------------|------------|
| **P0 - Critical** | System down, data loss, security breach | Immediate (< 15 min) | Technical Lead + Security |
| **P1 - High** | Major degradation, data corruption | < 1 hour | Technical Lead |
| **P2 - Medium** | Performance issues, partial outage | < 4 hours | On-Call Engineer |
| **P3 - Low** | Minor issues, non-critical failures | Next business day | Standard Support |

---

## P0 - Critical Incident Response

### Incident Types
- Neo4j service completely unavailable
- Data corruption or loss detected
- Security breach or unauthorized access
- Complete system failure (hardware/software)
- Ransomware or malware infection

### Immediate Actions (< 5 minutes)

1. **Declare Incident**: Notify on-call team immediately
   ```bash
   # Send alert
   echo "P0 INCIDENT: [DESCRIPTION]" | mail -s "CRITICAL: AEON DT P0 Incident" oncall@example.com
   ```

2. **Assess Impact**:
   - [ ] Identify affected systems
   - [ ] Determine scope (all users / subset)
   - [ ] Check if data integrity compromised
   - [ ] Verify backup systems operational

3. **Isolate Issue**:
   - [ ] If security breach: Disconnect from network immediately
   - [ ] If data corruption: Stop all write operations
   - [ ] If service failure: Prevent cascading failures

**Isolation Commands**:
```bash
# Stop Neo4j immediately
sudo systemctl stop neo4j

# Block network access (if security breach)
sudo iptables -A INPUT -p tcp --dport 7687 -j DROP
sudo iptables -A INPUT -p tcp --dport 7474 -j DROP

# Kill all active processes
pkill -9 -f "aeon_.*\.py"
```

### Recovery Actions (5-30 minutes)

#### Service Down Recovery
```bash
#!/bin/bash
# p0_service_recovery.sh

echo "=== P0 Service Recovery ==="

# 1. Check service status
systemctl status neo4j

# 2. Check logs for root cause
tail -100 /var/log/neo4j/debug.log | grep "ERROR\|FATAL"

# 3. Attempt service restart
sudo systemctl restart neo4j
sleep 15

# 4. Verify connectivity
if python3 scripts/test_connection.py; then
    echo "✓ Service recovered"
else
    echo "✗ Recovery failed - escalating"
    # Restore from backup
    bash scripts/restore_latest_backup.sh
fi
```

#### Data Corruption Recovery
```bash
#!/bin/bash
# p0_data_recovery.sh

echo "=== P0 Data Recovery ==="

# 1. Stop all operations
sudo systemctl stop neo4j

# 2. Assess corruption extent
neo4j-admin check-consistency --database=neo4j --report-dir=/tmp/consistency_report

# 3. Restore from latest backup
LATEST_BACKUP=$(ls -t /backups/weekly/ | head -1)
neo4j-admin restore --from="/backups/weekly/$LATEST_BACKUP" --database=neo4j --force

# 4. Restart and verify
sudo systemctl start neo4j
sleep 20

python3 scripts/verify_data_integrity.py
```

#### Security Breach Response
```bash
#!/bin/bash
# p0_security_response.sh

echo "=== P0 Security Breach Response ==="

# 1. Isolate system
sudo systemctl stop neo4j
sudo ufw deny 7687
sudo ufw deny 7474

# 2. Collect evidence
mkdir -p /tmp/security_incident_$(date +%Y%m%d_%H%M%S)
cp /var/log/neo4j/*.log /tmp/security_incident_*/
cp /var/log/auth.log /tmp/security_incident_*/

# 3. Reset credentials
neo4j-admin set-initial-password "$(openssl rand -base64 32)"

# 4. Notify security team
echo "Security breach detected on AEON DT system" | mail -s "SECURITY BREACH - P0" security@example.com

# 5. Do NOT restart until security team approval
echo "System isolated. Awaiting security team clearance."
```

### Post-Incident (< 2 hours)

- [ ] Root cause analysis: Document exact cause
- [ ] Impact assessment: Quantify data/service impact
- [ ] Timeline documentation: Record all actions taken
- [ ] Stakeholder notification: Inform affected parties
- [ ] Prevention measures: Implement safeguards
- [ ] Incident report: Complete detailed report

---

## P1 - High Priority Incident Response

### Incident Types
- Major performance degradation (> 50% slower)
- Partial data corruption
- High error rates (> 10% failure)
- NVD API unavailable > 4 hours
- Critical feature failure

### Response Procedure (< 1 hour)

#### Performance Degradation
```bash
#!/bin/bash
# p1_performance_response.sh

echo "=== P1 Performance Response ==="

# 1. Collect performance metrics
python3 - <<EOF
from neo4j import GraphDatabase
import os
import time

driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))

queries = [
    "MATCH (n) RETURN count(n)",
    "MATCH ()-[r]->() RETURN count(r)",
    "MATCH (v:Vulnerability) RETURN count(v)"
]

for query in queries:
    with driver.session() as session:
        start = time.time()
        result = session.run(query)
        _ = list(result)
        duration = time.time() - start
        print(f"Query: {query[:30]}... - Time: {duration:.3f}s")

driver.close()
EOF

# 2. Check system resources
echo -e "\nSystem Resources:"
free -h
df -h

# 3. Identify slow queries
grep "slow query" /var/log/neo4j/query.log | tail -20

# 4. Restart Neo4j if needed
if [[ $(python3 scripts/check_avg_query_time.py) > 3000 ]]; then
    echo "Average query time > 3s, restarting Neo4j..."
    sudo systemctl restart neo4j
fi
```

#### Data Corruption (Partial)
```python
# p1_partial_corruption_fix.py
from neo4j import GraphDatabase
import os

driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))

print("=== P1 Partial Corruption Fix ===")

with driver.session() as session:
    # Find corrupted nodes
    result = session.run("""
        MATCH (n)
        WHERE n.name IS NULL OR n.name = ''
        RETURN labels(n)[0] as type, count(n) as corrupted_count
    """)

    for record in result:
        print(f"Corrupted {record['type']}: {record['corrupted_count']}")

    # Remove corrupted nodes with no relationships
    result = session.run("""
        MATCH (n)
        WHERE (n.name IS NULL OR n.name = '') AND NOT (n)--()
        DELETE n
        RETURN count(n) as deleted
    """)

    deleted = result.single()['deleted']
    print(f"✓ Removed {deleted} corrupted nodes")

    # Flag remaining corrupted nodes for manual review
    session.run("""
        MATCH (n)
        WHERE (n.name IS NULL OR n.name = '') AND (n)--()
        SET n.requires_manual_review = true
        RETURN count(n) as flagged
    """)

driver.close()
```

---

## P2 - Medium Priority Incident Response

### Incident Types
- Moderate performance issues (20-50% slower)
- Ingestion failures (< 10% rate)
- Non-critical service degradation
- Warning threshold exceeded

### Response Procedure (< 4 hours)

```bash
#!/bin/bash
# p2_response.sh

echo "=== P2 Incident Response ==="

# 1. Log incident
echo "$(date -Iseconds) - P2 Incident: $1" >> /var/log/aeon_incidents.log

# 2. Collect diagnostics
python3 scripts/performance_diagnostics.py > /tmp/p2_diagnostics_$(date +%Y%m%d_%H%M%S).log

# 3. Apply standard fixes
bash scripts/optimize_performance.sh

# 4. Monitor for 30 minutes
for i in {1..6}; do
    sleep 300  # 5 minutes
    python3 scripts/check_metrics.py
done

# 5. Document resolution
echo "$(date -Iseconds) - P2 Resolved: $1" >> /var/log/aeon_incidents.log
```

---

## P3 - Low Priority Incident Response

### Incident Types
- Minor performance issues
- Individual document processing failures
- Non-critical warnings
- Cosmetic issues

### Response Procedure (Next Business Day)

```bash
#!/bin/bash
# p3_response.sh

echo "=== P3 Incident Response ==="

# Log incident for batch processing
echo "$(date -Iseconds) - P3 Incident: $1" >> /var/log/aeon_p3_incidents.log

# Add to maintenance queue
echo "$1" >> /var/log/aeon_maintenance_queue.txt

echo "✓ Incident logged for next maintenance window"
```

---

## Communication Templates

### P0 Critical Incident Notification
```
SUBJECT: [P0 CRITICAL] AEON DT System Incident

PRIORITY: CRITICAL
INCIDENT ID: INC-[YYYYMMDD]-[###]
START TIME: [TIMESTAMP]
SEVERITY: P0 - Critical

DESCRIPTION:
[Brief description of the incident]

IMPACT:
[System components affected and user impact]

STATUS:
[Current status and estimated time to resolution]

NEXT UPDATE:
[Time of next status update]

CONTACT:
Incident Commander: [NAME/CONTACT]
```

### P1 High Priority Notification
```
SUBJECT: [P1 HIGH] AEON DT Service Degradation

INCIDENT ID: INC-[YYYYMMDD]-[###]
START TIME: [TIMESTAMP]
SEVERITY: P1 - High

DESCRIPTION:
[Description of the issue]

IMPACT:
[User/system impact]

ESTIMATED RESOLUTION:
[Time estimate]

WORKAROUND:
[Any available workarounds]
```

---

## Escalation Procedures

### When to Escalate

**To Technical Lead**:
- P0 incidents automatically
- P1 incidents not resolved in 2 hours
- Any data loss detected
- Security concerns

**To Security Team**:
- Suspected security breach
- Unauthorized access detected
- Malware/ransomware detected
- Data exfiltration suspected

**To Management**:
- P0 incidents affecting > 4 hours
- Data loss > 1% of database
- Regulatory compliance impact
- Public disclosure required

### Escalation Contacts

```
Technical Lead: [NAME]
- Phone: [NUMBER]
- Email: [EMAIL]
- Backup: [NAME/CONTACT]

Security Team: security@example.com
- On-Call: [NUMBER]
- CISO: [NAME/CONTACT]

Management:
- Director: [NAME/CONTACT]
- VP Engineering: [NAME/CONTACT]
```

---

## Post-Incident Review

### Required Documentation

1. **Incident Timeline**:
   - Detection time
   - Response initiation
   - Key actions taken
   - Resolution time

2. **Root Cause Analysis**:
   - Primary cause
   - Contributing factors
   - Why not detected earlier

3. **Impact Assessment**:
   - Systems affected
   - Data loss (if any)
   - Downtime duration
   - User impact

4. **Corrective Actions**:
   - Immediate fixes applied
   - Long-term prevention measures
   - Monitoring improvements
   - Documentation updates

5. **Lessons Learned**:
   - What went well
   - What could improve
   - Training needs
   - Process improvements

### Post-Incident Meeting Agenda

```markdown
# Post-Incident Review Meeting

**Incident**: [ID and Description]
**Date**: [Date of Incident]
**Attendees**: [Names]

## Agenda

1. Incident Timeline (10 min)
2. Root Cause Analysis (15 min)
3. Impact Assessment (10 min)
4. Response Effectiveness (10 min)
5. Prevention Measures (15 min)
6. Action Items (10 min)

## Action Items
- [ ] [Action 1] - Owner: [Name] - Due: [Date]
- [ ] [Action 2] - Owner: [Name] - Due: [Date]
```

---

## Emergency Contact List

```
=== EMERGENCY CONTACTS ===

On-Call Rotation: Check PagerDuty schedule

Technical Contacts:
- Database Admin: [NAME] - [PHONE/EMAIL]
- Security Lead: [NAME] - [PHONE/EMAIL]
- DevOps Lead: [NAME] - [PHONE/EMAIL]

External Vendors:
- Neo4j Support: support@neo4j.com / +1-xxx-xxx-xxxx
- AWS Support: [ACCOUNT/CONTACT]
- CloudFlare: [CONTACT]

Emergency Services:
- Data Center: [CONTACT]
- Network Operations: [CONTACT]
- Physical Security: [CONTACT]
```

---

**Last Updated**: 2025-10-29
**Review Frequency**: Quarterly (after each P0/P1 incident)
**Version**: 1.0.0
**Classification**: INTERNAL USE ONLY
**Approved By**: AEON DT Security Team & Technical Lead
