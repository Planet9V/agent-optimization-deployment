# AEON Data Update Procedures

**Version**: 1.0.0
**Last Updated**: 2025-12-02
**Status**: Production

---

## Overview

This document describes the procedures for keeping AEON Cyber Digital Twin data sources current.

---

## 1. Weekly CVE Update Procedure

### Purpose
Update CVE database with new vulnerabilities and refresh EPSS scores.

### Schedule
- **Frequency**: Weekly (Sundays at midnight)
- **Duration**: ~30-60 minutes
- **Data Sources**: NVD API, FIRST.org EPSS API

### Prerequisites
```bash
# Ensure services are running
docker ps | grep neo4j    # Neo4j should be running
curl http://localhost:8000/health  # NER11 API healthy
```

### Execution Steps

```bash
# 1. Navigate to project directory
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model

# 2. Run weekly update
python3 scripts/update_cve_taxonomy.py --days 7

# 3. Verify results
python3 scripts/update_cve_taxonomy.py --report-only
```

### Cron Setup

```bash
# Edit crontab
crontab -e

# Add weekly update job
0 0 * * 0 cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model && python3 scripts/update_cve_taxonomy.py --days 7 >> logs/cve_update.log 2>&1
```

### Expected Output
```
============================================================
CVE Taxonomy Update
Started: 2025-12-02T00:00:00
============================================================
✅ Connected to Neo4j at bolt://localhost:7687
📥 Fetching CVEs from 2025-11-25 to 2025-12-02
   Fetched 247 CVEs (total: 247/247)
📊 Fetching EPSS scores for 247 CVEs
   Got EPSS for 243 CVEs

📝 Updating Neo4j...
✅ UPDATE COMPLETE
   Created: 189
   Updated: 58
   CWE Links: 312
   Errors: 0

📊 CURRENT STATE
   Total CVEs: 316,741
   EPSS Coverage: 95.1%
   CVSS Coverage: 98.2%
============================================================
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| NVD API timeout | Retry with `--days 3` for smaller batch |
| Neo4j connection failed | Check `docker ps`, restart Neo4j |
| EPSS API error | API may be down, retry later |
| Rate limit exceeded | Wait 30 seconds, script auto-retries |

---

## 2. EPSS Daily Update Procedure

### Purpose
Refresh EPSS (Exploit Prediction Scoring System) scores for all CVEs.

### Schedule
- **Frequency**: Daily (optional, for high-priority environments)
- **Duration**: ~10-15 minutes
- **Data Source**: FIRST.org bulk CSV

### Execution Steps

```bash
# 1. Download daily EPSS file
cd /home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/NVS\ Full\ CVE\ CAPEC\ CWE\ EMBED/

# 2. Download compressed CSV
DATE=$(date +%Y-%m-%d)
wget "https://epss.cyentia.com/epss_scores-${DATE}.csv.gz"

# 3. Decompress
gunzip epss_scores-${DATE}.csv.gz

# 4. Update Neo4j
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python3 scripts/load_comprehensive_taxonomy.py --source epss
```

### Python Script for Bulk EPSS Update

```python
#!/usr/bin/env python3
"""Update EPSS scores from daily CSV."""

import csv
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "neo4j@openspg")
)

with open("epss_scores-2025-12-02.csv") as f:
    reader = csv.DictReader(f)
    with driver.session() as session:
        batch = []
        for row in reader:
            batch.append({
                "cve_id": row["cve"],
                "epss": float(row["epss"]),
                "percentile": float(row["percentile"])
            })

            if len(batch) >= 1000:
                session.run("""
                    UNWIND $batch as item
                    MATCH (c:CVE {id: item.cve_id})
                    SET c.epss_score = item.epss,
                        c.epss_percentile = item.percentile
                """, batch=batch)
                batch = []

        # Final batch
        if batch:
            session.run("""
                UNWIND $batch as item
                MATCH (c:CVE {id: item.cve_id})
                SET c.epss_score = item.epss,
                    c.epss_percentile = item.percentile
            """, batch=batch)

driver.close()
print("EPSS update complete!")
```

---

## 3. MITRE ATT&CK Quarterly Update

### Purpose
Update MITRE ATT&CK techniques, tactics, and relationships.

### Schedule
- **Frequency**: Quarterly (check MITRE releases)
- **Duration**: ~15-30 minutes
- **Data Source**: MITRE ATT&CK GitHub

### Execution Steps

```bash
# 1. Download latest ATT&CK data
cd /home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/NVS\ Full\ CVE\ CAPEC\ CWE\ EMBED/

# 2. Download STIX bundles
wget https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json
wget https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack.json
wget https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack.json

# 3. Run loader
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python3 scripts/load_comprehensive_taxonomy.py --source attack
```

### Verification

```cypher
// Check technique counts
MATCH (t:Technique)
RETURN t.domain, count(t) as count
ORDER BY count DESC

// Check tactic counts
MATCH (t:Tactic)
RETURN t.domain, count(t) as count
ORDER BY count DESC

// Check technique-tactic links
MATCH (tech:Technique)-[:BELONGS_TO]->(tac:Tactic)
RETURN count(*) as total_links
```

---

## 4. CWE/CAPEC Annual Update

### Purpose
Update weakness and attack pattern taxonomies when new versions release.

### Schedule
- **Frequency**: Annual (or when MITRE releases new versions)
- **Duration**: ~20-30 minutes
- **Data Sources**: MITRE CWE, MITRE CAPEC

### Execution Steps

```bash
# 1. Download latest CWE
cd /home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/NVS\ Full\ CVE\ CAPEC\ CWE\ EMBED/
wget https://cwe.mitre.org/data/xml/cwec_latest.xml.zip
unzip cwec_latest.xml.zip

# 2. Download latest CAPEC
wget https://capec.mitre.org/data/xml/capec_latest.xml.zip
unzip capec_latest.xml.zip

# 3. Run loaders
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python3 scripts/load_comprehensive_taxonomy.py --source cwe
python3 scripts/load_comprehensive_taxonomy.py --source capec
```

---

## 5. EMB3D Update Procedure

### Purpose
Update EMB3D embedded device threat model.

### Schedule
- **Frequency**: When EMB3D releases updates
- **Duration**: ~5-10 minutes
- **Data Source**: MITRE EMB3D

### Execution Steps

```bash
# 1. Download latest EMB3D STIX
cd /home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/NVS\ Full\ CVE\ CAPEC\ CWE\ EMBED/
wget https://raw.githubusercontent.com/mitre/emb3d/main/stix/emb3d-stix-2.0.1.json

# 2. Run loader
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python3 scripts/load_comprehensive_taxonomy.py --source emb3d
```

### Important Note
EMB3D uses `vulnerability` type in STIX, NOT `attack-pattern`. The loader handles this automatically.

---

## 6. Full Taxonomy Reload

### Purpose
Complete reload of all data sources (use when data integrity issues suspected).

### Schedule
- **Frequency**: As needed
- **Duration**: ~2-4 hours
- **Warning**: This is a heavy operation

### Execution Steps

```bash
# 1. Backup current data (optional)
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
cypher-shell -u neo4j -p 'neo4j@openspg' "CALL apoc.export.json.all('backup.json', {})"

# 2. Run comprehensive loader
python3 scripts/load_comprehensive_taxonomy.py --all --skip-embeddings

# 3. Verify
python3 scripts/load_comprehensive_taxonomy.py --report-only
```

---

## 7. Verification Queries

### Check All Node Counts

```cypher
CALL db.labels() YIELD label
CALL apoc.cypher.run('MATCH (n:`' + label + '`) RETURN count(n) as count', {}) YIELD value
RETURN label, value.count as count
ORDER BY count DESC
```

### Check Relationship Counts

```cypher
CALL db.relationshipTypes() YIELD relationshipType
CALL apoc.cypher.run('MATCH ()-[r:`' + relationshipType + '`]->() RETURN count(r) as count', {}) YIELD value
RETURN relationshipType, value.count as count
ORDER BY count DESC
```

### Check EPSS Coverage

```cypher
MATCH (c:CVE)
WITH count(c) as total
MATCH (c:CVE) WHERE c.epss_score > 0
WITH total, count(c) as with_epss
RETURN total, with_epss,
       round(100.0 * with_epss / total, 1) as coverage_pct
```

### Check Priority Tier Distribution

```cypher
MATCH (c:CVE)
RETURN c.priority_tier as tier, count(c) as count
ORDER BY tier
```

---

## 8. Monitoring and Alerts

### Log File Locations

```
/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/
├── cve_update.log          # Weekly CVE updates
├── taxonomy_load.log       # Full taxonomy loads
├── epss_update.log         # EPSS updates
└── chunked_ingest.log      # Document ingestion
```

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| CVE update failures | > 5% | > 20% |
| EPSS coverage drop | < 90% | < 80% |
| Neo4j connection errors | Any | Consecutive |
| Update duration | > 2x normal | > 5x normal |

### Health Check Script

```bash
#!/bin/bash
# health_check.sh

# Check Neo4j
if ! cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1" > /dev/null 2>&1; then
    echo "CRITICAL: Neo4j not responding"
    exit 1
fi

# Check CVE count
CVE_COUNT=$(cypher-shell -u neo4j -p 'neo4j@openspg' --format plain "MATCH (c:CVE) RETURN count(c)" | tail -1)
if [ "$CVE_COUNT" -lt 300000 ]; then
    echo "WARNING: CVE count low: $CVE_COUNT"
fi

# Check EPSS coverage
EPSS_PCT=$(cypher-shell -u neo4j -p 'neo4j@openspg' --format plain "MATCH (c:CVE) WITH count(c) as t MATCH (c:CVE) WHERE c.epss_score > 0 RETURN round(100.0 * count(c) / t, 1)" | tail -1)
if (( $(echo "$EPSS_PCT < 90" | bc -l) )); then
    echo "WARNING: EPSS coverage low: $EPSS_PCT%"
fi

echo "OK: Neo4j healthy, CVE=$CVE_COUNT, EPSS=$EPSS_PCT%"
```

---

## Appendix: Quick Reference

### Command Cheat Sheet

```bash
# Weekly CVE update
python3 scripts/update_cve_taxonomy.py --days 7

# Specific CVE lookup
python3 scripts/update_cve_taxonomy.py --cve CVE-2024-12345

# Full taxonomy reload
python3 scripts/load_comprehensive_taxonomy.py --all

# Report only (no changes)
python3 scripts/update_cve_taxonomy.py --report-only

# Individual source updates
python3 scripts/load_comprehensive_taxonomy.py --source cve
python3 scripts/load_comprehensive_taxonomy.py --source cwe
python3 scripts/load_comprehensive_taxonomy.py --source capec
python3 scripts/load_comprehensive_taxonomy.py --source attack
python3 scripts/load_comprehensive_taxonomy.py --source emb3d
python3 scripts/load_comprehensive_taxonomy.py --source epss
python3 scripts/load_comprehensive_taxonomy.py --source kev
```

### API Endpoints

| Service | Endpoint | Rate Limit |
|---------|----------|------------|
| NVD | services.nvd.nist.gov/rest/json/cves/2.0 | 5/30s |
| EPSS | api.first.org/data/v1/epss | Reasonable |
| ATT&CK | github.com/mitre-attack/attack-stix-data | None |
| CWE | cwe.mitre.org/data/downloads.html | None |
| CAPEC | capec.mitre.org/data/downloads.html | None |
