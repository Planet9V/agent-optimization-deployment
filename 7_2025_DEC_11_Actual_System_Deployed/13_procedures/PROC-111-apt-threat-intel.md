# PROCEDURE: [PROC-111] APT Threat Intelligence Ingestion

**Procedure ID**: PROC-111
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
| **Frequency** | WEEKLY |
| **Priority** | HIGH |
| **Estimated Duration** | 2-4 hours |
| **Risk Level** | MEDIUM |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Extract threat intelligence from 31 annotated APT training data files containing 5,000-10,000 indicators of compromise (IoCs), create ThreatActor, Campaign, and Indicator nodes, and establish relationships to existing CVE, CWE, and ATT&CK technique data.

### 2.2 Business Objectives
- [x] Ingest 31 APT training data files with XML-tagged entities
- [x] Create ThreatActor nodes for APT groups (50-80 expected)
- [x] Create Campaign nodes for operations (100-200 expected)
- [x] Create Indicator nodes for IoCs (5,000-10,000 expected)
- [x] Link threat actors to ATT&CK techniques and vulnerabilities

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q3: What do attackers know? | IoCs reveal targeting patterns and infrastructure |
| Q4: Who are the attackers? | ThreatActor nodes profile APT groups, nation-state attribution |
| Q6: What happened before? | Campaign nodes capture historical attack operations |
| Q7: What will happen next? | Threat actor TTP patterns predict future behaviors |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, accessible | `docker ps | grep neo4j` |
| Training Data | Files accessible | `ls -l /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/*.md | wc -l` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query | Expected Result |
|-----------|-------------------|-----------------|
| Technique nodes exist | `MATCH (t:Technique) RETURN count(t)` | >= 600 |
| CVE nodes exist | `MATCH (cve:CVE) RETURN count(cve)` | >= 10,000 |
| Training files present | Shell count | 31 files |

### 3.3 Prior Procedures Required

| Procedure ID | Procedure Name |
|--------------|---------------|
| PROC-001 | Schema Migration |
| PROC-301 | CAPEC-ATT&CK Mapping |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format |
|-------------|------|----------|--------|
| APT Training Files | File Collection | `/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/` | Markdown with XML tags |

### 4.2 Training Data Schema

**Tag Format**:
```xml
<THREAT_ACTOR>APT28</THREAT_ACTOR>
<CAMPAIGN>Ukraine Railway Attacks 2025</CAMPAIGN>
<INDICATOR>87.236.176.122</INDICATOR>
<MALWARE>WhisperGate</MALWARE>
<VULNERABILITY>CVE-2022-38028</VULNERABILITY>
```

### 4.3 File Categories

**APT Group Files (9)**: Volt Typhoon, APT28, Sandworm, APT41, Lazarus, Salt Typhoon, Turla, FIN7, OceanLotus

**Nation-State Files (3)**: China APT Landscape, Russia APT Landscape, Iran/North Korea Landscape

**Malware Files (9)**: LockBit, Emotet, TrickBot, Qakbot, Black Basta, Royal, Cuba ransomware

**Sector Files (8)**: Transportation, Energy, Maritime, Aviation, Healthcare, Financial, Telecommunications, Defense

**Comprehensive (2)**: APT Infrastructure Atlas, STIX Malware/Infrastructure

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
| ThreatActor | name, aliases, attribution, sophistication, motivation | UNIQUE on name |
| Campaign | name, first_seen, last_seen, objective | UNIQUE on name |
| Indicator | value, type, first_seen, confidence | INDEX on value |
| Malware | name, family, type | UNIQUE on name |

**Relationship Types**:
| Type | Source | Target |
|------|--------|--------|
| ATTRIBUTED_TO | (:Campaign) | (:ThreatActor) |
| USES_MALWARE | (:Campaign) | (:Malware) |
| USES_TECHNIQUE | (:ThreatActor) | (:Technique) |
| EXPLOITS | (:Campaign) | (:CVE) |
| OBSERVED_IN | (:Indicator) | (:Campaign) |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Mapping Rules

| Source Field | Target Property | Transformation |
|--------------|-----------------|----------------|
| `<THREAT_ACTOR>` | ThreatActor.name | Direct extract |
| `<CAMPAIGN>` | Campaign.name | Direct extract |
| `<INDICATOR>` | Indicator.value | Direct extract, detect type (IP/domain/hash) |
| `<MALWARE>` | Malware.name | Direct extract |
| `<VULNERABILITY>` | CVE match | Lookup existing CVE node |

### 6.2 Indicator Type Detection

| Pattern | Indicator Type |
|---------|---------------|
| `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}` | IPv4 |
| `[a-f0-9]{32}` | MD5 hash |
| `[a-f0-9]{64}` | SHA256 hash |
| `[a-zA-Z0-9\-\.]+\[?\.\]?[a-z]{2,}` | Domain |

### 6.3 Validation Rules

| Rule | Field | Validation | Action |
|------|-------|------------|--------|
| VAL-001 | THREAT_ACTOR | NOT NULL | SKIP record |
| VAL-002 | INDICATOR | Valid format | WARN, store raw |
| VAL-003 | CAMPAIGN | Min 5 chars | SKIP |

---

## 7. EXECUTION STEPS

### Step 1: Verify Training Data Access
```bash
cd /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training
ls -1 *.md | wc -l  # Should be 31
```

### Step 2: Create Neo4j Constraints
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" << 'EOF'
CREATE CONSTRAINT threat_actor_name_unique IF NOT EXISTS FOR (ta:ThreatActor) REQUIRE ta.name IS UNIQUE;
CREATE CONSTRAINT campaign_name_unique IF NOT EXISTS FOR (c:Campaign) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT malware_name_unique IF NOT EXISTS FOR (m:Malware) REQUIRE m.name IS UNIQUE;
CREATE INDEX indicator_value_idx IF NOT EXISTS FOR (i:Indicator) ON (i.value);
EOF
```

### Step 3: Run Ingestion Script
```bash
python3 << 'SCRIPT'
import re
from neo4j import GraphDatabase
from datetime import datetime
import os

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))
data_path = "/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training"

def extract_tags(content, tag_name):
    pattern = f"<{tag_name}>(.*?)</{tag_name}>"
    return re.findall(pattern, content, re.IGNORECASE)

def detect_indicator_type(value):
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', value):
        return 'ipv4'
    elif re.match(r'^[a-f0-9]{32}$', value, re.IGNORECASE):
        return 'md5'
    elif re.match(r'^[a-f0-9]{64}$', value, re.IGNORECASE):
        return 'sha256'
    elif re.match(r'^[a-zA-Z0-9\-\.]+\[?\.\]?[a-z]{2,}$', value):
        return 'domain'
    else:
        return 'unknown'

def ingest_file(session, filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    threat_actors = extract_tags(content, 'THREAT_ACTOR')
    campaigns = extract_tags(content, 'CAMPAIGN')
    indicators = extract_tags(content, 'INDICATOR')
    malware = extract_tags(content, 'MALWARE')
    vulnerabilities = extract_tags(content, 'VULNERABILITY')

    # Create nodes
    for ta in set(threat_actors):
        session.run("MERGE (ta:ThreatActor {name: $name}) "
                   "ON CREATE SET ta.source_file = $file, ta.created_at = datetime()",
                   name=ta, file=os.path.basename(filepath))

    for camp in set(campaigns):
        session.run("MERGE (c:Campaign {name: $name}) "
                   "ON CREATE SET c.source_file = $file, c.created_at = datetime()",
                   name=camp, file=os.path.basename(filepath))

    for ind in set(indicators):
        ind_type = detect_indicator_type(ind)
        session.run("MERGE (i:Indicator {value: $value}) "
                   "ON CREATE SET i.type = $type, i.first_seen = datetime(), i.source_file = $file",
                   value=ind, type=ind_type, file=os.path.basename(filepath))

    for mal in set(malware):
        session.run("MERGE (m:Malware {name: $name}) "
                   "ON CREATE SET m.source_file = $file, m.created_at = datetime()",
                   name=mal, file=os.path.basename(filepath))

    # Create relationships
    for camp in set(campaigns):
        for ta in set(threat_actors):
            session.run("MATCH (c:Campaign {name: $camp}), (ta:ThreatActor {name: $ta}) "
                       "MERGE (c)-[:ATTRIBUTED_TO]->(ta)", camp=camp, ta=ta)

        for mal in set(malware):
            session.run("MATCH (c:Campaign {name: $camp}), (m:Malware {name: $mal}) "
                       "MERGE (c)-[:USES_MALWARE]->(m)", camp=camp, mal=mal)

        for cve in set(vulnerabilities):
            session.run("MATCH (c:Campaign {name: $camp}), (cve:CVE {cve_id: $cve}) "
                       "MERGE (c)-[:EXPLOITS]->(cve)", camp=camp, cve=cve)

        for ind in set(indicators):
            session.run("MATCH (c:Campaign {name: $camp}), (i:Indicator {value: $ind}) "
                       "MERGE (i)-[:OBSERVED_IN]->(c)", camp=camp, ind=ind)

with driver.session() as session:
    md_files = [f for f in os.listdir(data_path) if f.endswith('.md')]
    for idx, filename in enumerate(md_files, 1):
        print(f"Processing {idx}/{len(md_files)}: {filename}")
        ingest_file(session, os.path.join(data_path, filename))

driver.close()
print("APT threat intelligence ingestion complete")
SCRIPT
```

### Step 4: Verify Results
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" << 'EOF'
MATCH (ta:ThreatActor) RETURN count(ta) AS threat_actors;
MATCH (c:Campaign) RETURN count(c) AS campaigns;
MATCH (i:Indicator) RETURN count(i) AS indicators;
MATCH (m:Malware) RETURN count(m) AS malware;
EOF
```

---

## 8. POST-EXECUTION VERIFICATION

### Verify Node Counts
```cypher
MATCH (ta:ThreatActor)
RETURN count(ta) AS threat_actors;
// Expected: 50-80

MATCH (c:Campaign)
RETURN count(c) AS campaigns;
// Expected: 100-200

MATCH (i:Indicator)
RETURN count(i) AS indicators;
// Expected: 5,000-10,000
```

### Verify Relationships
```cypher
MATCH (c:Campaign)-[r:ATTRIBUTED_TO]->(ta:ThreatActor)
RETURN ta.name, count(c) AS campaign_count
ORDER BY campaign_count DESC
LIMIT 10;
```

### Test Attack Chain
```cypher
MATCH path = (ta:ThreatActor)<-[:ATTRIBUTED_TO]-(c:Campaign)
             -[:EXPLOITS]->(cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
WHERE ta.name =~ '.*APT28.*'
RETURN ta.name, c.name, cve.cve_id, cwe.id
LIMIT 10;
```

### Success Criteria

| Criterion | Threshold | Actual |
|-----------|-----------|--------|
| ThreatActor nodes | >= 50 | ___ |
| Campaign nodes | >= 100 | ___ |
| Indicator nodes | >= 5,000 | ___ |
| ATTRIBUTED_TO rels | >= 100 | ___ |
| Attack chain works | Returns rows | ___ |

---

## 9. ROLLBACK PROCEDURE

### Step 1: Identify Affected Nodes
```cypher
MATCH (n)
WHERE n.source_file IS NOT NULL
  AND n.source_file =~ '.*APT.*|.*Malware.*|.*Sector.*'
RETURN labels(n), count(n);
```

### Step 2: Remove APT Data
```cypher
MATCH (ta:ThreatActor)
WHERE ta.source_file IS NOT NULL
DETACH DELETE ta;

MATCH (c:Campaign)
WHERE c.source_file IS NOT NULL
DETACH DELETE c;

MATCH (i:Indicator)
WHERE i.source_file IS NOT NULL
DETACH DELETE i;

MATCH (m:Malware)
WHERE m.source_file IS NOT NULL
DETACH DELETE m;
```

### Step 3: Verify Rollback
```cypher
MATCH (n)
WHERE n.source_file IS NOT NULL
RETURN count(n);
// Expected: 0
```

---

## 10. SCHEDULING & AUTOMATION

### Cron Schedule
```cron
# Weekly on Sundays at 3 AM
0 3 * * 0 /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_111_apt_threat_intel.sh >> /var/log/aeon/proc_111.log 2>&1
```

### Automation Script
```bash
#!/bin/bash
# /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_111_apt_threat_intel.sh

set -e
LOG_FILE="/var/log/aeon/proc_111_$(date +%Y%m%d_%H%M%S).log"

echo "[$(date)] Starting PROC-111: APT Threat Intelligence Ingestion" | tee -a "$LOG_FILE"

# Execute inline Python script from Step 3
python3 /path/to/proc_111_ingestion_script.py 2>&1 | tee -a "$LOG_FILE"

echo "[$(date)] PROC-111 completed successfully" | tee -a "$LOG_FILE"
```

---

## 11. MONITORING & ALERTING

### Metrics to Monitor

| Metric | Source | Threshold | Alert |
|--------|--------|-----------|-------|
| Execution duration | Log | > 6 hours | ERROR |
| ThreatActor nodes | Neo4j | < 40 | WARN |
| Indicators ingested | Neo4j | < 4,000 | WARN |
| Relationship creation | Neo4j | < 100 | ERROR |

### Log Locations

| Log Type | Location | Retention |
|----------|----------|-----------|
| Execution log | `/var/log/aeon/proc_111.log` | 30 days |
| Error log | `/var/log/aeon/proc_111_error.log` | 90 days |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL System | Initial procedure for E01 APT Threat Intelligence |

---

## 13. APPENDICES

### Appendix A: Sample Training Data
```markdown
# APT28 / Fancy Bear IoCs

<THREAT_ACTOR>APT28</THREAT_ACTOR> (also known as <THREAT_ACTOR>Fancy Bear</THREAT_ACTOR>)
is a Russia-sponsored group targeting <CAMPAIGN>Ukraine Railway Attacks 2025</CAMPAIGN>.

Key indicators include <INDICATOR>87.236.176.122</INDICATOR> (C2 server) and
<MALWARE>WhisperGate</MALWARE> wiper malware exploiting <VULNERABILITY>CVE-2022-38028</VULNERABILITY>.
```

### Appendix B: Related Documentation

| Document | Location |
|----------|----------|
| Enhancement 01 README | `/enhancements/Enhancement_01_APT_Threat_Intel/README.md` |
| DATA_SOURCES.md | `/enhancements/Enhancement_01_APT_Threat_Intel/DATA_SOURCES.md` |
| Training Data Files | `/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/` |

---

**End of Procedure PROC-111**
