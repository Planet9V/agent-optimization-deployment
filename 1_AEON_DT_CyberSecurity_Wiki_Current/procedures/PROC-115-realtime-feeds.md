# PROCEDURE: [PROC-115] Real-Time Threat Intelligence Feeds

**Procedure ID**: PROC-115
**Version**: 1.0.0
**Created**: 2025-11-26
**Last Modified**: 2025-11-26
**Author**: AEON ETL Agent System
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | ETL |
| **Frequency** | REAL-TIME / HOURLY |
| **Priority** | CRITICAL |
| **Estimated Duration** | 10-20 minutes per run |
| **Risk Level** | MEDIUM |
| **Rollback Available** | PARTIAL |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Establish automated real-time ingestion from multiple threat intelligence feeds (NVD, CISA KEV, VulnCheck, MITRE ATT&CK) via polling and webhook mechanisms, create ThreatFeed and ThreatEvent nodes with temporal tracking, and enable continuous threat landscape monitoring with automated alerting for critical vulnerabilities.

### 2.2 Business Objectives
- [x] Ingest NVD CVE updates (hourly polling)
- [x] Ingest CISA KEV catalog (weekly polling)
- [x] Integrate VulnCheck API (real-time webhooks)
- [x] Sync MITRE ATT&CK updates (quarterly)
- [x] Enable automated alerting for CRITICAL/HIGH vulnerabilities

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q3: What do attackers know? | Real-time exploit intelligence from VulnCheck |
| Q6: What happened before? | Temporal tracking of vulnerability disclosures |
| Q7: What will happen next? | Predictive alerts based on emerging threats |
| Q8: What should we do? | Automated remediation recommendations |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, accessible | `docker ps | grep neo4j` |
| Internet Access | Available | `curl -I https://nvd.nist.gov` |
| API Keys | Configured | `echo $NVD_API_KEY $VULNCHECK_API_KEY` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query | Expected Result |
|-----------|-------------------|-----------------|
| CVE schema exists | `MATCH (cve:CVE) RETURN count(cve) LIMIT 1` | >= 1 |
| Technique nodes exist | `MATCH (t:Technique) RETURN count(t)` | >= 600 |

### 3.3 API Keys Required

| Service | Environment Variable | Acquisition |
|---------|---------------------|------------|
| NVD | `NVD_API_KEY` | https://nvd.nist.gov/developers/ |
| VulnCheck | `VULNCHECK_API_KEY` | https://vulncheck.com/api |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Update Frequency |
|-------------|------|----------|------------------|
| NVD API 2.0 | REST API | https://services.nvd.nist.gov/rest/json/cves/2.0 | Hourly |
| CISA KEV | CSV | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv | Weekly |
| VulnCheck API | REST + Webhooks | https://api.vulncheck.com/v3/ | Real-time |
| MITRE ATT&CK | GitHub STIX | https://github.com/mitre-attack/attack-stix-data | Quarterly |

### 4.2 NVD API 2.0 Schema
```json
{
  "vulnerabilities": [
    {
      "cve": {
        "id": "CVE-2025-00001",
        "published": "2025-01-15T00:00:00Z",
        "lastModified": "2025-01-20T12:34:56Z"
      },
      "metrics": {
        "cvssV31": {
          "cvssData": {
            "baseScore": 9.8,
            "baseSeverity": "CRITICAL"
          }
        }
      }
    }
  ]
}
```

### 4.3 CISA KEV CSV Schema
```csv
cveID,vendor,product,vulnerabilityName,dateAdded,shortDescription,requiredAction,dueDate,knownRansomwareCampaignUse
CVE-2021-44228,Apache,Log4j,Apache Log4j2 Remote Code Execution,2021-12-10,RCE via JNDI,Patch,2022-01-10,Yes
```

### 4.4 VulnCheck Webhook Payload
```json
{
  "event": "vulnerability.published",
  "cveId": "CVE-2025-00001",
  "severity": "CRITICAL",
  "exploitAvailable": true,
  "exploitDate": "2025-01-16T12:34:56Z"
}
```

---

## 5. DESTINATION

### 5.1 Target System

| Field | Value |
|-------|-------|
| **System** | Neo4j |
| **Container** | openspg-neo4j |
| **Port** | 7687 (Bolt) |
| **Volume** | active_neo4j_data |

### 5.2 Target Schema

**Node Types**:
| Label | Properties | Constraints |
|-------|-----------|-------------|
| ThreatFeed | name, source_url, last_poll | UNIQUE on name |
| ThreatEvent | event_id, event_type, timestamp, severity | UNIQUE on event_id |
| KEVEntry | cve_id, date_added, due_date, ransomware_use | UNIQUE on cve_id |

**Relationships**:
| Type | Source | Target |
|------|--------|--------|
| PUBLISHED_BY | (:ThreatEvent) | (:ThreatFeed) |
| RELATES_TO | (:ThreatEvent) | (:CVE) |
| EXPLOITED_IN_WILD | (:CVE) | (:KEVEntry) |
| REQUIRES_ACTION | (:KEVEntry) | (:Remediation) |

---

## 6. TRANSFORMATION LOGIC

### 6.1 NVD Incremental Polling

**Last Modified Strategy**:
```python
last_poll = get_last_poll_timestamp()  # From ThreatFeed.last_poll
api_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?lastModStartDate={last_poll}"
```

### 6.2 CISA KEV Differential Update

**Comparison Logic**:
```python
current_kev = download_kev_csv()
previous_kev = load_from_database()
new_entries = current_kev - previous_kev
```

### 6.3 Validation Rules

| Rule | Field | Validation | Action |
|------|-------|------------|--------|
| VAL-001 | CVE ID | REGEX `^CVE-\d{4}-\d{4,}$` | REJECT |
| VAL-002 | Severity | In [LOW, MEDIUM, HIGH, CRITICAL] | WARN |
| VAL-003 | Timestamp | Valid ISO 8601 | REJECT |

---

## 7. EXECUTION STEPS

### Step 1: Create ThreatFeed Tracking Nodes
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" << 'EOF'
MERGE (tf:ThreatFeed {name: 'NVD API 2.0'})
SET tf.source_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0',
    tf.poll_frequency = 'HOURLY',
    tf.last_poll = datetime('2025-01-01T00:00:00Z');

MERGE (tf:ThreatFeed {name: 'CISA KEV'})
SET tf.source_url = 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv',
    tf.poll_frequency = 'WEEKLY',
    tf.last_poll = datetime('2025-01-01T00:00:00Z');

MERGE (tf:ThreatFeed {name: 'VulnCheck API'})
SET tf.source_url = 'https://api.vulncheck.com/v3/',
    tf.poll_frequency = 'REAL-TIME',
    tf.last_poll = datetime();
EOF
```

### Step 2: NVD Hourly Polling Script
```bash
python3 << 'SCRIPT'
import requests
from neo4j import GraphDatabase
from datetime import datetime
import os

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))
NVD_API_KEY = os.getenv('NVD_API_KEY', '')

def get_last_poll(session):
    result = session.run("MATCH (tf:ThreatFeed {name: 'NVD API 2.0'}) RETURN tf.last_poll AS last_poll")
    record = result.single()
    return record['last_poll'].isoformat() if record and record['last_poll'] else '2025-01-01T00:00:00Z'

def poll_nvd(session):
    last_poll = get_last_poll(session)
    headers = {'apiKey': NVD_API_KEY} if NVD_API_KEY else {}

    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?lastModStartDate={last_poll}"

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            vulnerabilities = data.get('vulnerabilities', [])

            for vuln in vulnerabilities:
                cve_data = vuln.get('cve', {})
                cve_id = cve_data.get('id')
                published = cve_data.get('published')
                modified = cve_data.get('lastModified')

                metrics = vuln.get('metrics', {})
                cvss_v31 = metrics.get('cvssV31', [{}])[0] if 'cvssV31' in metrics else {}
                cvss_data = cvss_v31.get('cvssData', {})
                base_score = cvss_data.get('baseScore')
                severity = cvss_data.get('baseSeverity')

                # Update CVE node
                session.run("""
                    MERGE (cve:CVE {cve_id: $cve_id})
                    SET cve.published = datetime($published),
                        cve.lastModified = datetime($modified),
                        cve.cvssV3BaseScore = $base_score,
                        cve.cvssV3Severity = $severity,
                        cve.updated_by_feed = 'NVD API 2.0',
                        cve.feed_update_timestamp = datetime()
                """, cve_id=cve_id, published=published, modified=modified,
                    base_score=base_score, severity=severity)

                # Create ThreatEvent
                session.run("""
                    CREATE (te:ThreatEvent {
                        event_id: randomUUID(),
                        event_type: 'CVE_UPDATED',
                        timestamp: datetime($modified),
                        severity: $severity
                    })
                    WITH te
                    MATCH (cve:CVE {cve_id: $cve_id})
                    MATCH (tf:ThreatFeed {name: 'NVD API 2.0'})
                    CREATE (te)-[:RELATES_TO]->(cve)
                    CREATE (te)-[:PUBLISHED_BY]->(tf)
                """, cve_id=cve_id, modified=modified, severity=severity)

            # Update last poll timestamp
            session.run("""
                MATCH (tf:ThreatFeed {name: 'NVD API 2.0'})
                SET tf.last_poll = datetime()
            """)

            print(f"NVD poll complete: {len(vulnerabilities)} CVEs processed")

    except Exception as e:
        print(f"NVD polling failed: {e}")

with driver.session() as session:
    poll_nvd(session)

driver.close()
SCRIPT
```

### Step 3: CISA KEV Weekly Polling Script
```bash
python3 << 'SCRIPT'
import csv
import requests
from neo4j import GraphDatabase
from datetime import datetime

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv"

def poll_cisa_kev(session):
    response = requests.get(KEV_URL, timeout=30)
    if response.status_code == 200:
        lines = response.text.strip().split('\n')
        reader = csv.DictReader(lines)

        for row in reader:
            cve_id = row.get('cveID')
            date_added = row.get('dateAdded')
            due_date = row.get('dueDate')
            ransomware_use = row.get('knownRansomwareCampaignUse', 'Unknown')

            # Create KEVEntry and link to CVE
            session.run("""
                MERGE (kev:KEVEntry {cve_id: $cve_id})
                SET kev.date_added = date($date_added),
                    kev.due_date = date($due_date),
                    kev.ransomware_use = $ransomware_use,
                    kev.vendor = $vendor,
                    kev.product = $product,
                    kev.vulnerability_name = $vuln_name
                WITH kev
                MATCH (cve:CVE {cve_id: $cve_id})
                MERGE (cve)-[:EXPLOITED_IN_WILD]->(kev)
            """, cve_id=cve_id, date_added=date_added, due_date=due_date,
                ransomware_use=ransomware_use, vendor=row.get('vendor'),
                product=row.get('product'), vuln_name=row.get('vulnerabilityName'))

        session.run("MATCH (tf:ThreatFeed {name: 'CISA KEV'}) SET tf.last_poll = datetime()")
        print(f"CISA KEV poll complete: {reader.line_num - 1} entries processed")

with driver.session() as session:
    poll_cisa_kev(session)

driver.close()
SCRIPT
```

### Step 4: Setup Cron Jobs
```bash
# Create cron jobs for automated polling
(crontab -l 2>/dev/null; echo "0 * * * * /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_115_nvd_poll.sh >> /var/log/aeon/proc_115_nvd.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "0 2 * * 0 /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_115_cisa_kev_poll.sh >> /var/log/aeon/proc_115_kev.log 2>&1") | crontab -
```

---

## 8. POST-EXECUTION VERIFICATION

### Verify ThreatFeed Status
```cypher
MATCH (tf:ThreatFeed)
RETURN tf.name, tf.poll_frequency, tf.last_poll
ORDER BY tf.last_poll DESC;
```

### Verify Recent Threat Events
```cypher
MATCH (te:ThreatEvent)-[:RELATES_TO]->(cve:CVE)
WHERE te.timestamp > datetime() - duration('P1D')
RETURN te.event_type, cve.cve_id, cve.cvssV3Severity, te.timestamp
ORDER BY te.timestamp DESC
LIMIT 20;
```

### Verify CISA KEV Critical Items
```cypher
MATCH (cve:CVE)-[:EXPLOITED_IN_WILD]->(kev:KEVEntry)
WHERE cve.cvssV3Severity = 'CRITICAL'
RETURN cve.cve_id, kev.date_added, kev.due_date, kev.ransomware_use
ORDER BY kev.date_added DESC
LIMIT 10;
```

### Success Criteria

| Criterion | Threshold | Actual |
|-----------|-----------|--------|
| NVD polling functional | Returns data | ___ |
| CISA KEV updates | New entries detected | ___ |
| ThreatEvent creation | Events created | ___ |
| Last poll < 2 hours ago | For NVD feed | ___ |

---

## 9. ROLLBACK PROCEDURE

### Disable Automated Polling
```bash
# Remove cron jobs
crontab -l | grep -v 'proc_115' | crontab -
```

### Remove Recent Threat Events
```cypher
MATCH (te:ThreatEvent)
WHERE te.timestamp > datetime() - duration('P7D')
DETACH DELETE te;
```

---

## 10. SCHEDULING & AUTOMATION

### Cron Schedule Summary

| Feed | Frequency | Cron Expression |
|------|-----------|-----------------|
| NVD API 2.0 | Hourly | `0 * * * *` |
| CISA KEV | Weekly (Sunday 2 AM) | `0 2 * * 0` |
| VulnCheck | Webhook (real-time) | N/A (event-driven) |
| MITRE ATT&CK | Quarterly (1st of quarter) | `0 3 1 1,4,7,10 *` |

---

## 11. MONITORING & ALERTING

### Metrics to Monitor

| Metric | Source | Threshold | Alert |
|--------|--------|-----------|-------|
| Last poll age | ThreatFeed.last_poll | > 2 hours (NVD) | ERROR |
| Critical CVEs | ThreatEvent | > 0 new CRITICAL | ALERT |
| API failures | Log | > 3 consecutive | ERROR |
| KEV updates | KEVEntry count | No change in 8 days | WARN |

### Alert Rules
```cypher
// Find new CRITICAL CVEs from last hour
MATCH (te:ThreatEvent)-[:RELATES_TO]->(cve:CVE)
WHERE te.timestamp > datetime() - duration('PT1H')
  AND cve.cvssV3Severity = 'CRITICAL'
RETURN cve.cve_id, cve.cvssV3BaseScore
ORDER BY cve.cvssV3BaseScore DESC;
```

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL System | Initial procedure for E05 Real-Time Feeds |

---

## 13. APPENDICES

### Appendix A: API Rate Limits

| Service | Free Tier | Authenticated | Enterprise |
|---------|-----------|---------------|------------|
| NVD | 5 req/30s | 30 req/30s | Custom |
| CISA KEV | Unlimited (CSV) | N/A | N/A |
| VulnCheck | 300 req/min | 1,000+ req/min | Custom |

### Appendix B: Data Sources
- NVD API Documentation: https://nvd.nist.gov/developers/
- CISA KEV Catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- VulnCheck API: https://vulncheck.com/api

---

**End of Procedure PROC-115**
