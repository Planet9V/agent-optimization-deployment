# PROCEDURE: [PROC-102] Kaggle Dataset Enrichment for CVE/CWE/Threat Actor Data

**Procedure ID**: PROC-102
**Version**: 1.0.0
**Created**: 2025-12-11
**Last Modified**: 2025-12-11
**Author**: AEON ETL Agent System
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | ETL |
| **Frequency** | MONTHLY / ON-DEMAND |
| **Priority** | HIGH |
| **Estimated Duration** | 60-120 minutes |
| **Risk Level** | LOW |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Enrich existing CVE, CWE, and ThreatActor nodes with CVSS scores, CWE mappings, and ATT&CK technique data from Kaggle datasets, addressing the critical 0% CVSS coverage gap identified in the E01 corpus assessment.

### 2.2 Business Objectives
- [x] Enrich 316,552 CVEs with CVSS v2/v3/v4 scores (currently 0% coverage)
- [x] Create IS_WEAKNESS_TYPE relationships linking CVEs to CWE weaknesses
- [x] Add ATT&CK technique descriptions and detection methods
- [x] Supplement threat actor profiles with malware family mappings

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q1: What equipment do we have? | N/A |
| Q2: What equipment do customers have? | N/A |
| Q3: What do attackers know? | CVSS exploitability scores reveal attack knowledge |
| Q4: Who are the attackers? | APT group enrichment via ADAPT/APTMalware datasets |
| Q5: How do we defend? | CVSS scores + CWE mappings prioritize defenses |
| Q6: What happened before? | N/A |
| Q7: What will happen next? | Severity scoring enables predictive prioritization |
| Q8: What should we do? | CWE taxonomy enables weakness remediation |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, accessible | `docker ps \| grep neo4j` |
| Network | Internet access for Kaggle API | `curl -I https://www.kaggle.com` |
| Kaggle CLI | Authenticated | `kaggle datasets list --max-size 1` |
| Python 3.9+ | Installed | `python3 --version` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query/Command | Expected Result |
|-----------|---------------------------|-----------------|
| CVE nodes exist | `MATCH (c:CVE) RETURN count(c)` | >= 316,000 |
| CVEs lack CVSS | `MATCH (c:CVE) WHERE c.cvssV31BaseScore IS NULL RETURN count(c)` | ~316,000 (0% coverage) |
| CWE nodes exist (minimal) | `MATCH (c:CWE) RETURN count(c)` | >= 0 (will create) |
| ThreatActor nodes exist | `MATCH (t:ThreatActor) RETURN count(t)` | >= 800 |
| Technique nodes exist | `MATCH (t:Technique) RETURN count(t)` | >= 600 |

### 3.3 Authentication & Credentials

| Service | Credential Source | Environment Variable |
|---------|------------------|---------------------|
| Neo4j | Docker compose | `NEO4J_PASSWORD=neo4j@openspg` |
| Kaggle API | ~/.kaggle/kaggle.json | `KAGGLE_USERNAME`, `KAGGLE_KEY` |

### 3.4 Dependencies

| Dependency | Version Required | Verification |
|------------|-----------------|--------------|
| Python | 3.9+ | `python3 --version` |
| neo4j (Python) | 5.x | `pip show neo4j` |
| pandas | 2.x | `pip show pandas` |
| kaggle | 1.5+ | `pip show kaggle` |
| requests | 2.x | `pip show requests` |

### 3.5 Prior Procedures Required

| Procedure ID | Procedure Name | Must Complete Before |
|--------------|---------------|---------------------|
| PROC-001 | Schema Migration | This procedure (constraints must exist) |
| PROC-111 | APT Threat Intel | Recommended (creates ThreatActor nodes) |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format | Update Frequency |
|-------------|------|----------|--------|------------------|
| CVE & CWE (1999-2025) | Kaggle | stanislavvinokur/cve-and-cwe-dataset-1999-2025 | CSV (ZIP) | Monthly |
| CVE 2024 Database | Kaggle | manavkhambhayata/cve-2024-database-exploits-cvss-os | CSV (ZIP) | Monthly |
| MITRE Tactics & Techniques | Kaggle | tejaswara/cybersec-mitre-tactics-techniques-instruction-data | CSV (ZIP) | Quarterly |
| APTMalware | GitHub | cyber-research/APTMalware | JSON/CSV | On-demand |

### 4.2 Source Details

#### Source 1: CVE & CWE Dataset (1999-2025) ⭐ PRIMARY

**Connection Information**:
```
Type: Kaggle Dataset
Dataset ID: stanislavvinokur/cve-and-cwe-dataset-1999-2025
Authentication: Kaggle API key
File Size: ~22.9 MB (compressed)
Records: ~215,780 CVEs
```

**Data Schema**:
```csv
CVE-ID,CVSS-V4,CVSS-V3,CVSS-V2,SEVERITY,DESCRIPTION,CWE-ID
CVE-2024-21762,9.8,9.8,10.0,CRITICAL,"Out-of-bounds write...",CWE-787
```

**Sample Data**:
```csv
CVE-2024-21762,9.8,9.8,10.0,CRITICAL,"A out-of-bounds write in Fortinet FortiOS versions 7.4.0 through 7.4.2...",CWE-787
CVE-2024-3400,10.0,10.0,10.0,CRITICAL,"A command injection vulnerability in GlobalProtect...",CWE-77
```

**Extraction Command**:
```bash
kaggle datasets download stanislavvinokur/cve-and-cwe-dataset-1999-2025 -p /tmp/kaggle_data
unzip /tmp/kaggle_data/cve-and-cwe-dataset-1999-2025.zip -d /tmp/kaggle_data/
```

#### Source 2: MITRE Tactics & Techniques

**Connection Information**:
```
Type: Kaggle Dataset
Dataset ID: tejaswara/cybersec-mitre-tactics-techniques-instruction-data
Authentication: Kaggle API key
File Size: ~383 KB (compressed)
Format: Q&A instruction data
```

**Data Schema**:
```json
{
  "question": "What is technique T1059.001?",
  "answer": "PowerShell - Adversaries may abuse PowerShell commands and scripts for execution...",
  "detection": "Monitor for loading of PowerShell modules...",
  "platforms": "Windows"
}
```

### 4.3 Data Volume Estimates

| Source | Records Expected | Size Estimate | Processing Time |
|--------|-----------------|---------------|-----------------|
| CVE & CWE (1999-2025) | 215,780 CVEs | ~23MB | 30-45 min |
| MITRE Tactics | ~600 techniques | ~400KB | 5-10 min |
| APTMalware | 3,500 samples | ~5MB | 10-15 min |

---

## 5. DESTINATION

### 5.1 Target System

| Field | Value |
|-------|-------|
| **System** | Neo4j |
| **Container** | openspg-neo4j |
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

#### Node Types ENRICHED (NOT created - existing nodes only)

| Label | Properties Added | Existing Constraint |
|-------|-----------------|---------------------|
| CVE | cvssV31BaseScore, cvssV31BaseSeverity, cvssV2BaseScore, cvssV4BaseScore, kaggle_enriched_timestamp | cve_id_unique |
| CWE | id, name, description (MERGE) | cwe_id_unique |
| Technique | detection_methods, platforms (MERGE) | technique_id_unique |
| ThreatActor | malware_families, nation_state (MERGE) | actor_id_unique |

#### Relationship Types Created/Modified

| Type | Source | Target | Properties |
|------|--------|--------|------------|
| IS_WEAKNESS_TYPE | (:CVE) | (:CWE) | source='kaggle:cve_cwe_2025', created_timestamp |
| USES_MALWARE | (:ThreatActor) | (:Malware) | source='github:aptmalware', samples_count |

### 5.4 Target Data Location

**Exact Storage Path**:
```
Container: openspg-neo4j
Volume: active_neo4j_data
Internal Path: /data/databases/neo4j
Neo4j Import: /var/lib/neo4j/import/
```

---

## 6. TRANSFORMATION LOGIC

### 6.1 Mapping Rules - CVE/CWE Dataset

| Source Field | Target Property | Transformation |
|--------------|-----------------|----------------|
| CVE-ID | CVE.id | Direct match (MUST exist) |
| CVSS-V3 | CVE.cvssV31BaseScore | toFloat(), null if empty |
| CVSS-V2 | CVE.cvssV2BaseScore | toFloat(), null if empty |
| CVSS-V4 | CVE.cvssV4BaseScore | toFloat(), null if empty |
| SEVERITY | CVE.cvssV31BaseSeverity | UPPER(trim(value)) |
| DESCRIPTION | CVE.description | First 2000 chars, null if empty |
| CWE-ID | CWE.id | Extract CWE-XXX pattern |
| [calculated] | CVE.kaggle_enriched_timestamp | datetime() at enrichment |
| [calculated] | *.source | 'kaggle:cve_cwe_2025' |

### 6.2 Data Validation Rules

| Rule ID | Field | Validation | Action on Failure |
|---------|-------|------------|------------------|
| VAL-001 | CVE-ID | REGEX `^CVE-\d{4}-\d{4,}$` | SKIP record |
| VAL-002 | CVSS scores | Range 0.0-10.0 | WARN, set NULL |
| VAL-003 | SEVERITY | IN ['NONE','LOW','MEDIUM','HIGH','CRITICAL'] | DEFAULT to NULL |
| VAL-004 | CWE-ID | REGEX `^CWE-\d+$` OR 'NVD-CWE-Other' | SKIP relationship |
| VAL-005 | CVE exists | MATCH (c:CVE {id: row.CVE-ID}) | SKIP if not exists |

### 6.3 Deduplication Strategy

```
Unique Key: CVE.id (existing), CWE.id
On Duplicate CVE: SET properties (enrich existing)
On Duplicate CWE: MERGE (create if not exists)
On Duplicate Relationship: MERGE (no duplicates)
```

### 6.4 Error Handling

| Error Type | Detection | Action | Logging |
|------------|-----------|--------|---------|
| Kaggle download failure | HTTP error | Retry 3x, abort | ERROR level |
| Missing CVE in graph | No MATCH result | Skip enrichment | DEBUG level |
| Invalid CVSS score | Parse exception | Set NULL | WARN level |
| CWE not in standard format | Regex fail | Skip relationship | WARN level |
| Neo4j connection lost | Driver exception | Retry 3x, checkpoint | ERROR level |

---

## 7. EXECUTION STEPS

### 7.1 Pre-Execution Checklist

- [ ] Kaggle API credentials configured (~/.kaggle/kaggle.json)
- [ ] Neo4j accessible with correct credentials
- [ ] PROC-001 schema migration completed (constraints exist)
- [ ] Sufficient disk space (>500MB for datasets)
- [ ] E30 ingestion NOT actively writing (or coordinate timing)

### 7.2 Step-by-Step Execution

#### Step 1: Verify Neo4j CVE Gap

**Purpose**: Confirm CVSS enrichment is needed

**Command**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (c:CVE)
   WITH count(c) AS total,
        count(c.cvssV31BaseScore) AS has_cvss
   RETURN total, has_cvss, 100.0 * has_cvss / total AS coverage_pct"
```

**Expected Output**:
```
+--------+----------+--------------+
| total  | has_cvss | coverage_pct |
+--------+----------+--------------+
| 316552 | 0        | 0.0          |
+--------+----------+--------------+
```

**Verification**: Coverage < 50% indicates enrichment needed

---

#### Step 2: Download Kaggle CVE/CWE Dataset

**Purpose**: Get primary enrichment data

**Command**:
```bash
mkdir -p /tmp/kaggle_data
kaggle datasets download stanislavvinokur/cve-and-cwe-dataset-1999-2025 \
  -p /tmp/kaggle_data --unzip
ls -la /tmp/kaggle_data/
```

**Expected Output**:
```
total 85000
-rw-r--r-- 1 user user 85123456 Dec 11 12:00 CVE_CWE_2025.csv
```

**Verification**: CSV file exists and is ~80-100MB uncompressed

**Troubleshooting**:
- If auth error: Run `kaggle config set -n username -v YOUR_USERNAME`
- If download fails: Try `wget https://www.kaggle.com/datasets/stanislavvinokur/cve-and-cwe-dataset-1999-2025/download`

---

#### Step 3: Copy CSV to Neo4j Import Directory

**Purpose**: Make data accessible to Neo4j LOAD CSV

**Command**:
```bash
docker cp /tmp/kaggle_data/CVE_CWE_2025.csv openspg-neo4j:/var/lib/neo4j/import/
docker exec openspg-neo4j ls -la /var/lib/neo4j/import/
```

**Expected Output**:
```
-rw-r--r-- 1 neo4j neo4j 85123456 Dec 11 12:05 CVE_CWE_2025.csv
```

---

#### Step 4: Create CWE Constraint if Missing

**Purpose**: Ensure CWE uniqueness before MERGE operations

**Command**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS FOR (c:CWE) REQUIRE c.id IS UNIQUE"
```

**Expected Output**: `0 rows`

---

#### Step 5: Run CVE CVSS Enrichment (Batch 1 - CVSS Scores)

**Purpose**: Enrich existing CVEs with CVSS scores

**Command**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "
CALL apoc.periodic.iterate(
  \"LOAD CSV WITH HEADERS FROM 'file:///CVE_CWE_2025.csv' AS row RETURN row\",
  \"MATCH (cve:CVE {id: row.\\\`CVE-ID\\\`})
   SET cve.cvssV31BaseScore = CASE WHEN row.\\\`CVSS-V3\\\` IS NOT NULL AND row.\\\`CVSS-V3\\\` <> ''
                                   THEN toFloat(row.\\\`CVSS-V3\\\`) ELSE cve.cvssV31BaseScore END,
       cve.cvssV2BaseScore = CASE WHEN row.\\\`CVSS-V2\\\` IS NOT NULL AND row.\\\`CVSS-V2\\\` <> ''
                                  THEN toFloat(row.\\\`CVSS-V2\\\`) ELSE cve.cvssV2BaseScore END,
       cve.cvssV4BaseScore = CASE WHEN row.\\\`CVSS-V4\\\` IS NOT NULL AND row.\\\`CVSS-V4\\\` <> ''
                                  THEN toFloat(row.\\\`CVSS-V4\\\`) ELSE cve.cvssV4BaseScore END,
       cve.cvssV31BaseSeverity = CASE WHEN row.SEVERITY IS NOT NULL AND row.SEVERITY <> ''
                                      THEN toUpper(trim(row.SEVERITY)) ELSE cve.cvssV31BaseSeverity END,
       cve.kaggle_enriched_timestamp = datetime()
   RETURN count(*)\",
  {batchSize: 5000, parallel: false}
) YIELD batches, total, errorMessages
RETURN batches, total, errorMessages
"
```

**Expected Output**:
```
+---------+--------+---------------+
| batches | total  | errorMessages |
+---------+--------+---------------+
| 43      | 215780 | []            |
+---------+--------+---------------+
```

**Verification**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (c:CVE) WHERE c.cvssV31BaseScore IS NOT NULL RETURN count(c)"
```

---

#### Step 6: Run CVE→CWE Relationship Creation (Batch 2 - CWE Links)

**Purpose**: Create IS_WEAKNESS_TYPE relationships

**Command**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "
CALL apoc.periodic.iterate(
  \"LOAD CSV WITH HEADERS FROM 'file:///CVE_CWE_2025.csv' AS row
   WHERE row.\\\`CWE-ID\\\` IS NOT NULL
     AND row.\\\`CWE-ID\\\` <> ''
     AND row.\\\`CWE-ID\\\` <> 'NVD-CWE-Other'
     AND row.\\\`CWE-ID\\\` <> 'NVD-CWE-noinfo'
   RETURN row\",
  \"MATCH (cve:CVE {id: row.\\\`CVE-ID\\\`})
   MERGE (cwe:CWE {id: row.\\\`CWE-ID\\\`})
   ON CREATE SET cwe.source = 'kaggle:cve_cwe_2025',
                 cwe.created_timestamp = datetime()
   MERGE (cve)-[r:IS_WEAKNESS_TYPE]->(cwe)
   ON CREATE SET r.source = 'kaggle:cve_cwe_2025',
                 r.created_timestamp = datetime()
   RETURN count(*)\",
  {batchSize: 5000, parallel: false}
) YIELD batches, total, errorMessages
RETURN batches, total, errorMessages
"
```

**Expected Output**:
```
+---------+--------+---------------+
| batches | total  | errorMessages |
+---------+--------+---------------+
| 30      | 150000 | []            |
+---------+--------+---------------+
```

---

#### Step 7: Verify Enrichment Results

**Purpose**: Confirm successful enrichment

**Command**:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "
MATCH (c:CVE)
WITH count(c) AS total,
     count(c.cvssV31BaseScore) AS has_cvss31,
     count(c.cvssV2BaseScore) AS has_cvss2,
     count(c.kaggle_enriched_timestamp) AS kaggle_enriched
RETURN total, has_cvss31, has_cvss2, kaggle_enriched,
       100.0 * has_cvss31 / total AS cvss31_coverage
"
```

**Expected Output**:
```
+--------+-----------+-----------+------------------+----------------+
| total  | has_cvss31| has_cvss2 | kaggle_enriched  | cvss31_coverage|
+--------+-----------+-----------+------------------+----------------+
| 316552 | 180000+   | 150000+   | 180000+          | 56%+           |
+--------+-----------+-----------+------------------+----------------+
```

---

### 7.3 Complete Execution Script

```bash
#!/bin/bash
# PROCEDURE: PROC-102 - Kaggle Dataset Enrichment
# Version: 1.0.0
# Execute: ./proc_102_kaggle_enrichment.sh

set -e

# Configuration
NEO4J_HOST="localhost"
NEO4J_PORT="7687"
NEO4J_USER="neo4j"
NEO4J_PASS="${NEO4J_PASSWORD:-neo4j@openspg}"
NEO4J_CONTAINER="${NEO4J_CONTAINER:-openspg-neo4j}"
WORK_DIR="/tmp/kaggle_data"
LOG_FILE="/var/log/aeon/proc_102_$(date +%Y%m%d_%H%M%S).log"

# Functions
log_info() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" | tee -a "$LOG_FILE"; }
log_error() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" | tee -a "$LOG_FILE"; }
log_warn() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $1" | tee -a "$LOG_FILE"; }

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

    # Check Kaggle CLI
    if ! command -v kaggle &> /dev/null; then
        log_error "Kaggle CLI not installed. Run: pip install kaggle"
        return 1
    fi

    # Check Kaggle auth
    if [ ! -f ~/.kaggle/kaggle.json ]; then
        log_error "Kaggle credentials not found at ~/.kaggle/kaggle.json"
        return 1
    fi

    # Check CVE gap
    CVE_TOTAL=$(cypher_query "MATCH (c:CVE) RETURN count(c)" | tail -1 | tr -d ' ')
    CVSS_COUNT=$(cypher_query "MATCH (c:CVE) WHERE c.cvssV31BaseScore IS NOT NULL RETURN count(c)" | tail -1 | tr -d ' ')

    log_info "CVE Total: $CVE_TOTAL, With CVSS: $CVSS_COUNT"

    if [ "$CVE_TOTAL" -lt 1000 ]; then
        log_warn "CVE count low ($CVE_TOTAL). Ensure E30 ingestion has run."
    fi
}

download_datasets() {
    log_info "Downloading Kaggle datasets..."
    mkdir -p "$WORK_DIR"

    # Primary CVE/CWE dataset
    kaggle datasets download stanislavvinokur/cve-and-cwe-dataset-1999-2025 \
        -p "$WORK_DIR" --unzip --force

    if [ ! -f "$WORK_DIR"/*.csv ]; then
        log_error "CSV file not found after download"
        return 1
    fi

    # Find and rename to standard name
    CSV_FILE=$(ls "$WORK_DIR"/*.csv | head -1)
    cp "$CSV_FILE" "$WORK_DIR/CVE_CWE_2025.csv"

    log_info "Downloaded: $(ls -lh $WORK_DIR/CVE_CWE_2025.csv)"
}

copy_to_neo4j() {
    log_info "Copying data to Neo4j import directory..."
    docker cp "$WORK_DIR/CVE_CWE_2025.csv" "$NEO4J_CONTAINER:/var/lib/neo4j/import/"
    docker exec "$NEO4J_CONTAINER" chown neo4j:neo4j /var/lib/neo4j/import/CVE_CWE_2025.csv
}

create_constraints() {
    log_info "Creating CWE constraint..."
    cypher_query "CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS FOR (c:CWE) REQUIRE c.id IS UNIQUE"
}

enrich_cvss_scores() {
    log_info "Enriching CVEs with CVSS scores..."

    cypher_query "
    CALL apoc.periodic.iterate(
      \"LOAD CSV WITH HEADERS FROM 'file:///CVE_CWE_2025.csv' AS row RETURN row\",
      \"MATCH (cve:CVE {id: row.\\\`CVE-ID\\\`})
       SET cve.cvssV31BaseScore = CASE WHEN row.\\\`CVSS-V3\\\` IS NOT NULL AND row.\\\`CVSS-V3\\\` <> ''
                                       THEN toFloat(row.\\\`CVSS-V3\\\`) ELSE cve.cvssV31BaseScore END,
           cve.cvssV2BaseScore = CASE WHEN row.\\\`CVSS-V2\\\` IS NOT NULL AND row.\\\`CVSS-V2\\\` <> ''
                                      THEN toFloat(row.\\\`CVSS-V2\\\`) ELSE cve.cvssV2BaseScore END,
           cve.cvssV4BaseScore = CASE WHEN row.\\\`CVSS-V4\\\` IS NOT NULL AND row.\\\`CVSS-V4\\\` <> ''
                                      THEN toFloat(row.\\\`CVSS-V4\\\`) ELSE cve.cvssV4BaseScore END,
           cve.cvssV31BaseSeverity = CASE WHEN row.SEVERITY IS NOT NULL AND row.SEVERITY <> ''
                                          THEN toUpper(trim(row.SEVERITY)) ELSE cve.cvssV31BaseSeverity END,
           cve.kaggle_enriched_timestamp = datetime()
       RETURN count(*)\",
      {batchSize: 5000, parallel: false}
    ) YIELD batches, total, errorMessages
    RETURN batches, total, errorMessages
    " 2>&1 | tee -a "$LOG_FILE"
}

create_cwe_relationships() {
    log_info "Creating CVE→CWE relationships..."

    cypher_query "
    CALL apoc.periodic.iterate(
      \"LOAD CSV WITH HEADERS FROM 'file:///CVE_CWE_2025.csv' AS row
       WHERE row.\\\`CWE-ID\\\` IS NOT NULL
         AND row.\\\`CWE-ID\\\` <> ''
         AND row.\\\`CWE-ID\\\` <> 'NVD-CWE-Other'
         AND row.\\\`CWE-ID\\\` <> 'NVD-CWE-noinfo'
       RETURN row\",
      \"MATCH (cve:CVE {id: row.\\\`CVE-ID\\\`})
       MERGE (cwe:CWE {id: row.\\\`CWE-ID\\\`})
       ON CREATE SET cwe.source = 'kaggle:cve_cwe_2025',
                     cwe.created_timestamp = datetime()
       MERGE (cve)-[r:IS_WEAKNESS_TYPE]->(cwe)
       ON CREATE SET r.source = 'kaggle:cve_cwe_2025',
                     r.created_timestamp = datetime()
       RETURN count(*)\",
      {batchSize: 5000, parallel: false}
    ) YIELD batches, total, errorMessages
    RETURN batches, total, errorMessages
    " 2>&1 | tee -a "$LOG_FILE"
}

verify_results() {
    log_info "Verifying enrichment results..."

    cypher_query "
    MATCH (c:CVE)
    WITH count(c) AS total,
         count(c.cvssV31BaseScore) AS has_cvss31,
         count(c.kaggle_enriched_timestamp) AS kaggle_enriched
    RETURN total, has_cvss31, kaggle_enriched,
           round(100.0 * has_cvss31 / total, 2) AS cvss31_coverage_pct
    " | tee -a "$LOG_FILE"

    cypher_query "
    MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
    RETURN count(r) AS cwe_relationships,
           count(DISTINCT cwe) AS unique_cwes
    " | tee -a "$LOG_FILE"
}

cleanup() {
    log_info "Cleaning up temporary files..."
    rm -rf "$WORK_DIR"
    docker exec "$NEO4J_CONTAINER" rm -f /var/lib/neo4j/import/CVE_CWE_2025.csv
}

main() {
    mkdir -p /var/log/aeon
    log_info "Starting PROC-102: Kaggle Dataset Enrichment"

    check_preconditions || exit 1
    download_datasets || exit 1
    copy_to_neo4j
    create_constraints
    enrich_cvss_scores
    create_cwe_relationships
    verify_results
    cleanup

    log_info "PROC-102 completed successfully"
}

main "$@"
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify CVSS Coverage Improvement

```cypher
// CVSS coverage before and after
MATCH (c:CVE)
WITH count(c) AS total,
     count(c.cvssV31BaseScore) AS has_cvss31,
     count(c.cvssV2BaseScore) AS has_cvss2
RETURN total, has_cvss31, has_cvss2,
       round(100.0 * has_cvss31 / total, 2) AS cvss31_pct,
       round(100.0 * has_cvss2 / total, 2) AS cvss2_pct;
```

**Expected Result**: >= 50% CVSS31 coverage

#### Verify Severity Distribution

```cypher
// Check severity distribution
MATCH (c:CVE)
WHERE c.cvssV31BaseSeverity IS NOT NULL
RETURN c.cvssV31BaseSeverity AS severity, count(c) AS count
ORDER BY count DESC;
```

**Expected Result**:
```
| severity | count   |
|----------|---------|
| MEDIUM   | 80000+  |
| HIGH     | 60000+  |
| CRITICAL | 15000+  |
| LOW      | 10000+  |
```

#### Verify CWE Relationships

```cypher
// Count CVE→CWE relationships
MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
RETURN count(r) AS total_relationships,
       count(DISTINCT cve) AS cves_with_cwe,
       count(DISTINCT cwe) AS unique_cwes;
```

**Expected Result**: >= 100,000 relationships

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| CVEs with CVSS31 | Count | >= 150,000 | [To fill] |
| CVSS coverage % | Percentage | >= 50% | [To fill] |
| CWE relationships | Count | >= 100,000 | [To fill] |
| Unique CWEs | Count | >= 200 | [To fill] |
| Error rate | % failures | < 5% | [To fill] |
| Execution time | Minutes | < 120 | [To fill] |

### 8.3 Cleanup Tasks

- [ ] Remove downloaded Kaggle datasets from /tmp
- [ ] Remove CSV from Neo4j import directory
- [ ] Archive execution log
- [ ] Update procedure execution timestamp in tracking system

---

## 9. ROLLBACK PROCEDURE

### 9.1 Rollback Triggers

- Error rate exceeds 20%
- CVSS scores appear incorrect (values outside 0-10 range)
- CWE relationships to wrong CVEs
- User requests rollback

### 9.2 Rollback Steps

#### Step 1: Identify Affected Data

```cypher
// Find nodes modified by this procedure run
MATCH (c:CVE)
WHERE c.kaggle_enriched_timestamp > datetime('2025-12-11T00:00:00')
RETURN count(c) AS affected_cves;
```

#### Step 2: Remove CVSS Enrichment

```cypher
// Remove CVSS properties added by Kaggle enrichment
MATCH (c:CVE)
WHERE c.kaggle_enriched_timestamp IS NOT NULL
REMOVE c.cvssV31BaseScore, c.cvssV2BaseScore, c.cvssV4BaseScore,
       c.cvssV31BaseSeverity, c.kaggle_enriched_timestamp;
```

#### Step 3: Remove CWE Relationships

```cypher
// Remove CVE→CWE relationships from Kaggle
MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
WHERE r.source = 'kaggle:cve_cwe_2025'
DELETE r;
```

#### Step 4: Remove Orphaned CWE Nodes (Optional)

```cypher
// Remove CWE nodes with no relationships
MATCH (cwe:CWE)
WHERE cwe.source = 'kaggle:cve_cwe_2025'
  AND NOT (cwe)<-[:IS_WEAKNESS_TYPE]-()
DELETE cwe;
```

### 9.3 Rollback Verification

```cypher
// Verify rollback complete
MATCH (c:CVE)
WHERE c.kaggle_enriched_timestamp IS NOT NULL
RETURN count(c);
// Expected: 0
```

---

## 10. SCHEDULING & AUTOMATION

### 10.1 Cron Schedule

```cron
# Monthly Kaggle enrichment on 15th at 4 AM (after E30 completes)
0 4 15 * * /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_102_kaggle_enrichment.sh >> /var/log/aeon/proc_102_cron.log 2>&1
```

### 10.2 Trigger Conditions

| Trigger | Source | Action |
|---------|--------|--------|
| E30 ingestion complete | Pipeline trigger | Execute procedure |
| Monthly schedule | Cron | Execute procedure |
| Manual request | Admin | Execute procedure |
| Kaggle dataset updated | Manual check | Execute procedure |

### 10.3 Dependencies in Pipeline

```
PROC-001 (Schema Setup)
    ↓
E30 (Bulk Graph Ingestion - creates CVE/ThreatActor/Technique nodes)
    ↓
PROC-102 (Kaggle Enrichment) ← YOU ARE HERE
    ↓
PROC-101 (NVD API Enrichment - supplements Kaggle)
    ↓
PROC-201 (CWE-CAPEC Linking)
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
| Execution duration | Log | > 2 hours | WARN |
| CVEs enriched | Neo4j | < 50,000 | ERROR |
| Error rate | Log | > 5% | ERROR |
| CVSS coverage | Neo4j | < 30% | WARN |

### 11.2 Log Locations

| Log Type | Location | Retention |
|----------|----------|-----------|
| Execution log | `/var/log/aeon/proc_102_*.log` | 30 days |
| Cron log | `/var/log/aeon/proc_102_cron.log` | 30 days |

### 11.3 Alert Channels

| Severity | Channel | Recipients |
|----------|---------|------------|
| CRITICAL | Log + Console | Immediate attention |
| ERROR | Log file | Daily review |
| WARN | Log file | Weekly review |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-11 | AEON ETL Agent | Initial version |

---

## 13. APPENDICES

### Appendix A: Kaggle Dataset Field Reference

**CVE & CWE Dataset (1999-2025)**:
```
CVE-ID      - Official CVE identifier (CVE-YYYY-NNNNN)
CVSS-V4     - CVSS v4.0 base score (0.0-10.0)
CVSS-V3     - CVSS v3.1 base score (0.0-10.0)
CVSS-V2     - CVSS v2.0 base score (0.0-10.0)
SEVERITY    - Qualitative severity (NONE/LOW/MEDIUM/HIGH/CRITICAL)
DESCRIPTION - Vulnerability description (English)
CWE-ID      - Associated CWE (CWE-NNN or NVD-CWE-Other)
```

### Appendix B: Alignment with E30 Process

**Critical Integration Points**:
1. **ENRICHES existing nodes** - Does NOT create new CVE nodes
2. **Uses MERGE for relationships** - Safe for re-runs
3. **Timestamps all enrichment** - Enables rollback identification
4. **Sources tagged** - All data tagged with 'kaggle:cve_cwe_2025'
5. **Batch processing** - Uses apoc.periodic.iterate for memory efficiency
6. **Non-destructive** - Only SETs properties, never DELETEs existing data

**E30 Compatibility**:
- Can run DURING E30 if needed (MATCH ensures only existing CVEs enriched)
- Recommended to run AFTER E30 batch completes for efficiency
- Does NOT create new schemas or node types

### Appendix C: Troubleshooting Guide

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| Kaggle download fails | Auth error | Check ~/.kaggle/kaggle.json |
| LOAD CSV fails | File not found | Verify docker cp worked |
| No CVEs enriched | CVE IDs don't match | Check CSV format matches Neo4j |
| CVSS NULL after enrichment | Empty values in CSV | Expected - not all CVEs have CVSS |
| Slow execution | Large dataset | Use batchSize: 10000 |

### Appendix D: Related Documentation

| Document | Location | Relationship |
|----------|----------|--------------|
| KAGGLE_ENRICHMENT_RESEARCH.md | 5_NER11_Gold_Model/docs/ | Dataset research |
| PROC-101 | 13_procedures/ | Complements with NVD API |
| PROC-201 | 13_procedures/ | Next in pipeline |
| E30 Pipeline | 5_NER11_Gold_Model/pipelines/ | Creates nodes for enrichment |

---

**End of Procedure PROC-102**
