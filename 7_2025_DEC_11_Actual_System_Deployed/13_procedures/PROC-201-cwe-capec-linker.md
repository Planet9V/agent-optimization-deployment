# PROCEDURE: [PROC-201] CWE-CAPEC Relationship Linker

**Procedure ID**: PROC-201
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
| **Frequency** | MONTHLY / ON-DEMAND |
| **Priority** | CRITICAL |
| **Estimated Duration** | 30-60 minutes |
| **Risk Level** | LOW |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Create EXPLOITS_WEAKNESS relationships between CAPEC attack patterns and CWE weaknesses by parsing the CAPEC XML database, establishing the critical link in the 8-hop attack chain between vulnerabilities and attack patterns.

### 2.2 Business Objectives
- [x] Create EXPLOITS_WEAKNESS relationships (~3,000+ expected)
- [x] Enable CWE→CAPEC traversal for attack pattern discovery
- [x] Load complete CWE catalog (1,000+ weaknesses)
- [x] Support McKenney Q3 "What do attackers know?" queries

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q1: What equipment do we have? | N/A |
| Q2: What equipment do customers have? | N/A |
| Q3: What do attackers know? | CWE→CAPEC shows how weaknesses enable attacks |
| Q4: Who are the attackers? | CAPEC links to techniques used by threat actors |
| Q5: How do we defend? | Understanding attack patterns guides defense |
| Q6: What happened before? | N/A |
| Q7: What will happen next? | Attack patterns predict exploitation methods |
| Q8: What should we do? | Prioritize CWE remediation by CAPEC severity |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, accessible | `docker ps \| grep neo4j` |
| Network | Access to MITRE downloads | `curl -I https://capec.mitre.org` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query/Command | Expected Result |
|-----------|---------------------------|-----------------|
| CAPEC nodes exist | `MATCH (c:CAPEC) RETURN count(c)` | >= 700 |
| CWE nodes exist | `MATCH (c:CWE) RETURN count(c)` | >= 10 (will expand) |
| CVE→CWE exists | `MATCH ()-[r:IS_WEAKNESS_TYPE]->() RETURN count(r)` | >= 150,000 |

### 3.3 Authentication & Credentials

| Service | Credential Source | Environment Variable |
|---------|------------------|---------------------|
| Neo4j | Docker compose | `NEO4J_PASSWORD=neo4j@openspg` |
| MITRE CAPEC | Public (no auth) | N/A |

### 3.4 Dependencies

| Dependency | Version Required | Verification |
|------------|-----------------|--------------|
| Python | 3.9+ | `python --version` |
| neo4j (Python) | 5.x | `pip show neo4j` |
| lxml | 4.x | `pip show lxml` |
| requests | 2.x | `pip show requests` |

### 3.5 Prior Procedures Required

| Procedure ID | Procedure Name | Must Complete Before |
|--------------|---------------|---------------------|
| PROC-001 | Schema Migration | This procedure |
| PROC-101 | CVE Enrichment | This procedure (creates CWE nodes) |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format | Update Frequency |
|-------------|------|----------|--------|------------------|
| CAPEC XML | File Download | https://capec.mitre.org/data/xml/capec_latest.xml | XML | Quarterly |

### 4.2 Source Details

#### Source 1: CAPEC XML Database

**Connection Information**:
```
Type: File Download
URL: https://capec.mitre.org/data/xml/capec_latest.xml
Authentication: None (public)
Size: ~15MB compressed
```

**Data Schema** (XML):
```xml
<Attack_Pattern ID="242" Name="Code Injection" Status="Draft">
  <Description>...</Description>
  <Likelihood_Of_Attack>High</Likelihood_Of_Attack>
  <Typical_Severity>Very High</Typical_Severity>
  <Related_Weaknesses>
    <Related_Weakness CWE_ID="94"/>
    <Related_Weakness CWE_ID="95"/>
    <Related_Weakness CWE_ID="96"/>
  </Related_Weaknesses>
  <Taxonomy_Mappings>
    <Taxonomy_Mapping Taxonomy_Name="ATTACK">
      <Entry_ID>T1059</Entry_ID>
    </Taxonomy_Mapping>
  </Taxonomy_Mappings>
</Attack_Pattern>
```

**Sample Data**:
```xml
<Attack_Pattern ID="66" Name="SQL Injection">
  <Related_Weaknesses>
    <Related_Weakness CWE_ID="89"/>
    <Related_Weakness CWE_ID="564"/>
    <Related_Weakness CWE_ID="943"/>
  </Related_Weaknesses>
</Attack_Pattern>
```

**Extraction Command**:
```bash
curl -o /tmp/capec_latest.xml https://capec.mitre.org/data/xml/capec_latest.xml
```

### 4.3 Data Volume Estimates

| Source | Records Expected | Size Estimate | Processing Time |
|--------|-----------------|---------------|-----------------|
| CAPEC XML | 706 attack patterns | ~15MB | 10-15 minutes |
| CWE mappings | ~3,000 relationships | N/A | Included above |

---

## 5. DESTINATION

### 5.1 Target System

| Field | Value |
|-------|-------|
| **System** | Neo4j |
| **Container** | openspg-neo4j (or neo4j-explore) |
| **Host** | localhost |
| **Port** | 7687 (Bolt), 7474 (HTTP) |
| **Database** | neo4j (default) |
| **Schema** | AEON 8-Layer Architecture |

### 5.2 Connection Details

```
Protocol: bolt://
Host: localhost
Port: 7687
Database: neo4j
User: neo4j
Password: ${NEO4J_PASSWORD:-neo4j@openspg}
```

### 5.3 Target Schema

#### Node Types Created/Modified

| Label | Properties | Constraints | Indexes |
|-------|-----------|-------------|---------|
| CAPEC | capec_id, name, description, likelihood, severity, abstraction | capec_pattern_id | capec_pattern_name |
| CWE | id, name, description, abstraction, source | cwe_id_unique | cwe_name_idx |

#### Relationship Types Created/Modified

| Type | Source | Target | Properties |
|------|--------|--------|------------|
| EXPLOITS_WEAKNESS | (:CAPEC) | (:CWE) | source, created_timestamp |

### 5.4 Target Data Location

**Exact Storage Path**:
```
Container: openspg-neo4j (or neo4j-explore)
Volume: active_neo4j_data
Internal Path: /data/databases/neo4j
External Mount: /var/lib/docker/volumes/active_neo4j_data/_data
```

---

## 6. TRANSFORMATION LOGIC

### 6.1 Mapping Rules

| Source Field | Target Property | Transformation |
|--------------|-----------------|----------------|
| Attack_Pattern/@ID | CAPEC.capec_id | "CAPEC-" + ID |
| Attack_Pattern/@Name | CAPEC.name | Direct copy |
| Attack_Pattern/Description | CAPEC.description | Extract text, truncate to 4000 chars |
| Attack_Pattern/Likelihood_Of_Attack | CAPEC.likelihood | Direct copy |
| Attack_Pattern/Typical_Severity | CAPEC.severity | Direct copy |
| Related_Weakness/@CWE_ID | CWE.id | "CWE-" + ID |
| [calculated] | *.created_timestamp | datetime() at load time |
| [calculated] | *.source | "capec:mitre" |

### 6.2 Data Validation Rules

| Rule ID | Field | Validation | Action on Failure |
|---------|-------|------------|------------------|
| VAL-001 | Attack_Pattern/@ID | INTEGER > 0 | REJECT pattern |
| VAL-002 | CWE_ID | INTEGER > 0 | SKIP relationship |
| VAL-003 | Name | NOT EMPTY | Use "Unknown CAPEC-{ID}" |
| VAL-004 | Severity | IN valid list | DEFAULT to "Unknown" |

### 6.3 Deduplication Strategy

```
Unique Key: CAPEC.capec_id, CWE.id
On Duplicate: MERGE (preserve existing, update timestamp)
Merge Strategy: Relationship MERGE by endpoints
```

### 6.4 Error Handling

| Error Type | Detection | Action | Logging |
|------------|-----------|--------|---------|
| XML parse error | lxml exception | Abort and report | ERROR level |
| Missing CWE_ID | Empty attribute | Skip relationship | WARN level |
| Neo4j constraint | Duplicate key | MERGE instead of CREATE | DEBUG level |
| Download failure | HTTP error | Retry 3x, then abort | ERROR level |

---

## 7. EXECUTION STEPS

### 7.1 Pre-Execution Checklist

- [ ] PROC-101 completed (CVE→CWE relationships exist)
- [ ] Neo4j accessible with correct credentials
- [ ] Network access to MITRE CAPEC download
- [ ] Sufficient disk space for XML download

### 7.2 Step-by-Step Execution

#### Step 1: Download CAPEC XML

**Purpose**: Get latest CAPEC database from MITRE

**Command**:
```bash
mkdir -p /tmp/aeon_etl
curl -o /tmp/aeon_etl/capec_latest.xml \
  https://capec.mitre.org/data/xml/capec_latest.xml
```

**Expected Output**:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 14.8M  100 14.8M    0     0  5000k      0  0:00:03  0:00:03 --:--:-- 5000k
```

**Verification**:
```bash
ls -la /tmp/aeon_etl/capec_latest.xml
# Should show ~15MB file
```

---

#### Step 2: Verify Existing CAPEC Data

**Purpose**: Check current CAPEC node count

**Command**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (c:CAPEC) RETURN count(c) AS capec_count"
```

**Expected Output**:
```
+-------------+
| capec_count |
+-------------+
| 706         |
+-------------+
```

---

#### Step 3: Create CWE Constraint if Missing

**Purpose**: Ensure CWE nodes can be created with uniqueness

**Command**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS FOR (c:CWE) REQUIRE c.id IS UNIQUE"
```

---

#### Step 4: Run CWE-CAPEC Linker Script

**Purpose**: Parse CAPEC XML and create relationships

**Command**:
```bash
cd /home/jim/2_OXOT_Projects_Dev/scripts/etl
python3 proc_201_cwe_capec_linker.py \
  --capec-xml /tmp/aeon_etl/capec_latest.xml \
  --neo4j-uri bolt://localhost:7687 \
  --neo4j-user neo4j \
  --neo4j-pass "neo4j@openspg"
```

**Expected Output**:
```
[INFO] Starting PROC-201: CWE-CAPEC Linker
[INFO] Parsing CAPEC XML: /tmp/aeon_etl/capec_latest.xml
[INFO] Found 706 attack patterns
[INFO] Processing attack patterns...
[INFO] Creating CWE nodes and relationships...
[INFO] Created/Updated 450 CWE nodes
[INFO] Created 2,847 EXPLOITS_WEAKNESS relationships
[INFO] PROC-201 completed successfully
```

---

#### Step 5: Verify Relationships Created

**Purpose**: Confirm attack chain linkage works

**Command**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (capec:CAPEC)-[r:EXPLOITS_WEAKNESS]->(cwe:CWE)
   RETURN count(r) AS rel_count,
          count(DISTINCT capec) AS capec_with_cwe,
          count(DISTINCT cwe) AS cwe_linked"
```

**Expected Output**:
```
+-----------+---------------+------------+
| rel_count | capec_with_cwe | cwe_linked |
+-----------+---------------+------------+
| 2847      | 520           | 450        |
+-----------+---------------+------------+
```

---

### 7.3 Complete Execution Script

```bash
#!/bin/bash
# PROCEDURE: PROC-201 - CWE-CAPEC Relationship Linker
# Version: 1.0.0
# Execute: ./proc_201_cwe_capec_linker.sh

set -e

# Configuration
NEO4J_HOST="localhost"
NEO4J_PORT="7687"
NEO4J_USER="neo4j"
NEO4J_PASS="${NEO4J_PASSWORD:-neo4j@openspg}"
NEO4J_CONTAINER="${NEO4J_CONTAINER:-openspg-neo4j}"
CAPEC_URL="https://capec.mitre.org/data/xml/capec_latest.xml"

LOG_FILE="/var/log/aeon/proc_201_$(date +%Y%m%d_%H%M%S).log"
WORK_DIR="/tmp/aeon_etl"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Functions
log_info() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" | tee -a "$LOG_FILE"; }
log_error() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" | tee -a "$LOG_FILE"; }

cypher_query() {
    docker exec "$NEO4J_CONTAINER" cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASS" "$1"
}

check_preconditions() {
    log_info "Checking pre-conditions..."

    # Check Neo4j running
    if ! docker ps | grep -q "$NEO4J_CONTAINER"; then
        log_error "Neo4j container not running"
        return 1
    fi

    # Check CAPEC data exists
    CAPEC_COUNT=$(cypher_query "MATCH (c:CAPEC) RETURN count(c)" | tail -1 | tr -d ' ')
    if [ "$CAPEC_COUNT" -lt 100 ]; then
        log_error "Insufficient CAPEC data: $CAPEC_COUNT"
        return 1
    fi

    # Check CVE→CWE relationships exist (PROC-101 completed)
    CWE_REL_COUNT=$(cypher_query "MATCH ()-[r:IS_WEAKNESS_TYPE]->() RETURN count(r)" | tail -1 | tr -d ' ')
    log_info "Pre-conditions verified. CAPEC: $CAPEC_COUNT, CVE→CWE: $CWE_REL_COUNT"
}

download_capec() {
    log_info "Downloading CAPEC XML..."
    mkdir -p "$WORK_DIR"
    curl -s -o "$WORK_DIR/capec_latest.xml" "$CAPEC_URL"

    if [ ! -f "$WORK_DIR/capec_latest.xml" ]; then
        log_error "Failed to download CAPEC XML"
        return 1
    fi

    log_info "CAPEC XML downloaded: $(ls -lh $WORK_DIR/capec_latest.xml | awk '{print $5}')"
}

create_constraints() {
    log_info "Ensuring CWE constraint exists..."
    cypher_query "CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS FOR (c:CWE) REQUIRE c.id IS UNIQUE"
}

run_linker() {
    log_info "Running CWE-CAPEC linker..."

    cd "$SCRIPT_DIR"
    python3 proc_201_cwe_capec_linker.py \
        --capec-xml "$WORK_DIR/capec_latest.xml" \
        --neo4j-uri "bolt://$NEO4J_HOST:$NEO4J_PORT" \
        --neo4j-user "$NEO4J_USER" \
        --neo4j-pass "$NEO4J_PASS" \
        2>&1 | tee -a "$LOG_FILE"
}

verify_results() {
    log_info "Verifying results..."

    RESULTS=$(cypher_query "
        MATCH (capec:CAPEC)-[r:EXPLOITS_WEAKNESS]->(cwe:CWE)
        RETURN count(r) AS relationships,
               count(DISTINCT capec) AS capec_linked,
               count(DISTINCT cwe) AS cwe_linked
    " | tail -1)

    log_info "Results: $RESULTS"
}

cleanup() {
    log_info "Cleaning up temporary files..."
    rm -f "$WORK_DIR/capec_latest.xml"
}

main() {
    mkdir -p /var/log/aeon
    log_info "Starting PROC-201: CWE-CAPEC Relationship Linker"

    check_preconditions || exit 1
    download_capec || exit 1
    create_constraints
    run_linker
    verify_results
    cleanup

    log_info "PROC-201 completed successfully"
}

main "$@"
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify Relationship Count

```cypher
MATCH (capec:CAPEC)-[r:EXPLOITS_WEAKNESS]->(cwe:CWE)
RETURN count(r) AS total_relationships;
```

**Expected Result**: >= 2,500

#### Verify Attack Chain Traversal

```cypher
// Test 3-hop chain: CVE → CWE → CAPEC
MATCH path = (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
              <-[:EXPLOITS_WEAKNESS]-(capec:CAPEC)
WHERE cve.cvssV3Severity = 'CRITICAL'
RETURN cve.cve_id, cwe.id, capec.capec_id, capec.name
LIMIT 10;
```

#### Verify CWE Coverage

```cypher
MATCH (cwe:CWE)
OPTIONAL MATCH (cwe)<-[:EXPLOITS_WEAKNESS]-(capec:CAPEC)
WITH cwe, count(capec) AS capec_count
RETURN
  count(CASE WHEN capec_count > 0 THEN 1 END) AS cwe_with_capec,
  count(CASE WHEN capec_count = 0 THEN 1 END) AS cwe_without_capec;
```

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| Relationships created | Count EXPLOITS_WEAKNESS | >= 2,500 | [To fill] |
| CAPEC linked | Distinct CAPEC with CWE | >= 500 | [To fill] |
| CWE linked | Distinct CWE with CAPEC | >= 400 | [To fill] |
| Error rate | % parse failures | < 1% | [To fill] |

### 8.3 Cleanup Tasks

- [ ] Remove downloaded XML file
- [ ] Update procedure execution log
- [ ] Notify downstream procedures (PROC-301)

---

## 9. ROLLBACK PROCEDURE

### 9.1 Rollback Triggers

- Incorrect relationships created
- Data corruption detected
- User requests rollback

### 9.2 Rollback Steps

#### Step 1: Remove EXPLOITS_WEAKNESS Relationships

```cypher
// Remove relationships from this run
MATCH (capec:CAPEC)-[r:EXPLOITS_WEAKNESS]->(cwe:CWE)
WHERE r.source = 'capec:mitre'
DELETE r;
```

#### Step 2: Remove Orphaned CWE Nodes (Optional)

```cypher
// Remove CWE nodes with no relationships
MATCH (cwe:CWE)
WHERE NOT (cwe)<-[:IS_WEAKNESS_TYPE]-()
  AND NOT (cwe)<-[:EXPLOITS_WEAKNESS]-()
DELETE cwe;
```

### 9.3 Rollback Verification

```cypher
MATCH ()-[r:EXPLOITS_WEAKNESS]->()
RETURN count(r);
// Expected: 0 after full rollback
```

---

## 10. SCHEDULING & AUTOMATION

### 10.1 Cron Schedule

```cron
# Monthly CAPEC refresh on 1st at 4 AM
0 4 1 * * /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_201_cwe_capec_linker.sh >> /var/log/aeon/proc_201_cron.log 2>&1
```

### 10.2 Trigger Conditions

| Trigger | Source | Action |
|---------|--------|--------|
| CAPEC update released | MITRE announcement | Execute procedure |
| PROC-101 completed | Pipeline trigger | Execute procedure |
| Manual request | Admin | Execute procedure |

### 10.3 Dependencies in Pipeline

```
PROC-001 (Schema Setup)
    ↓
PROC-101 (CVE Enrichment)
    ↓
PROC-201 (CWE-CAPEC Linking) ← YOU ARE HERE
    ↓
PROC-301 (CAPEC-ATT&CK Mapping)
    ↓
PROC-901 (Attack Chain Validation)
```

---

## 11. MONITORING & ALERTING

### 11.1 Metrics to Monitor

| Metric | Source | Threshold | Alert |
|--------|--------|-----------|-------|
| Relationships created | Neo4j | < 2000 | ERROR |
| Parse errors | Log | > 10 | WARN |
| Execution time | Log | > 60 min | WARN |

### 11.2 Log Locations

| Log Type | Location | Retention |
|----------|----------|-----------|
| Execution log | `/var/log/aeon/proc_201_*.log` | 30 days |
| Cron log | `/var/log/aeon/proc_201_cron.log` | 30 days |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL Agent | Initial version |

---

## 13. APPENDICES

### Appendix A: CAPEC XML Structure Sample

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Attack_Pattern_Catalog Name="CAPEC" Version="3.9">
  <Attack_Patterns>
    <Attack_Pattern ID="1" Name="Accessing Functionality Not Properly Constrained by ACLs" Abstraction="Standard" Status="Draft">
      <Description>...</Description>
      <Alternate_Terms>
        <Alternate_Term>
          <Term>Authorization Bypass</Term>
        </Alternate_Term>
      </Alternate_Terms>
      <Likelihood_Of_Attack>High</Likelihood_Of_Attack>
      <Typical_Severity>High</Typical_Severity>
      <Related_Attack_Patterns>
        <Related_Attack_Pattern Nature="ChildOf" CAPEC_ID="122"/>
      </Related_Attack_Patterns>
      <Related_Weaknesses>
        <Related_Weakness CWE_ID="276"/>
        <Related_Weakness CWE_ID="285"/>
        <Related_Weakness CWE_ID="732"/>
        <Related_Weakness CWE_ID="1191"/>
      </Related_Weaknesses>
      <Taxonomy_Mappings>
        <Taxonomy_Mapping Taxonomy_Name="ATTACK">
          <Entry_ID>T1574.002</Entry_ID>
          <Entry_Name>DLL Side-Loading</Entry_Name>
        </Taxonomy_Mapping>
      </Taxonomy_Mappings>
    </Attack_Pattern>
  </Attack_Patterns>
</Attack_Pattern_Catalog>
```

### Appendix B: Python Linker Script Structure

```python
#!/usr/bin/env python3
"""
PROC-201: CWE-CAPEC Relationship Linker
Version: 1.0.0
"""

import argparse
from lxml import etree
from neo4j import GraphDatabase

class CWECAPECLinker:
    def __init__(self, neo4j_uri, neo4j_user, neo4j_pass):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))

    def parse_capec_xml(self, xml_path):
        """Parse CAPEC XML and extract CWE relationships"""
        tree = etree.parse(xml_path)
        root = tree.getroot()
        ns = {'capec': 'http://capec.mitre.org/capec-3'}

        patterns = []
        for ap in root.findall('.//Attack_Pattern', ns):
            pattern = {
                'id': f"CAPEC-{ap.get('ID')}",
                'name': ap.get('Name'),
                'cwes': []
            }
            for rw in ap.findall('.//Related_Weakness', ns):
                cwe_id = rw.get('CWE_ID')
                if cwe_id:
                    pattern['cwes'].append(f"CWE-{cwe_id}")
            patterns.append(pattern)
        return patterns

    def create_relationships(self, patterns):
        """Create CWE nodes and EXPLOITS_WEAKNESS relationships"""
        with self.driver.session() as session:
            for pattern in patterns:
                for cwe_id in pattern['cwes']:
                    session.run("""
                        MERGE (cwe:CWE {id: $cwe_id})
                        ON CREATE SET cwe.source = 'capec:mitre',
                                      cwe.created_timestamp = datetime()
                        WITH cwe
                        MATCH (capec:CAPEC {capec_id: $capec_id})
                        MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
                        ON CREATE SET r.source = 'capec:mitre',
                                      r.created_timestamp = datetime()
                    """, cwe_id=cwe_id, capec_id=pattern['id'])

    def run(self, xml_path):
        patterns = self.parse_capec_xml(xml_path)
        print(f"[INFO] Found {len(patterns)} attack patterns")
        self.create_relationships(patterns)
        print("[INFO] Relationships created")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--capec-xml", required=True)
    parser.add_argument("--neo4j-uri", default="bolt://localhost:7687")
    parser.add_argument("--neo4j-user", default="neo4j")
    parser.add_argument("--neo4j-pass", required=True)
    args = parser.parse_args()

    linker = CWECAPECLinker(args.neo4j_uri, args.neo4j_user, args.neo4j_pass)
    linker.run(args.capec_xml)
```

### Appendix C: Related Documentation

| Document | Location | Relationship |
|----------|----------|--------------|
| PROC-101 | procedures/ | Previous in pipeline |
| PROC-301 | procedures/ | Next in pipeline |
| CAPEC Website | https://capec.mitre.org | Source documentation |
| SCHEMA_RECONCILIATION_ANALYSIS.md | technical_specs/ | Gap analysis |

---

**End of Procedure PROC-201**
