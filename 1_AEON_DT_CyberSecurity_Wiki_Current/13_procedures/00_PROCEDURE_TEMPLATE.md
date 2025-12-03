# AEON CYBER DIGITAL TWIN - PROCEDURE TEMPLATE

**Template Version**: 1.0.0
**Created**: 2025-11-26
**Purpose**: Standard template for all ETL, data loading, maintenance, and update procedures

---

## TEMPLATE STRUCTURE

All procedures in the AEON system MUST follow this template structure for consistency, repeatability, and maintainability.

---

```markdown
# PROCEDURE: [PROC-XXX] [Procedure Name]

**Procedure ID**: PROC-XXX (unique identifier)
**Version**: X.Y.Z
**Created**: YYYY-MM-DD
**Last Modified**: YYYY-MM-DD
**Author**: [Name/Agent]
**Status**: DRAFT | REVIEW | APPROVED | DEPRECATED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | ETL | MAINTENANCE | UPDATE | MIGRATION | BACKUP | VALIDATION |
| **Frequency** | ONE-TIME | DAILY | WEEKLY | MONTHLY | ON-DEMAND | TRIGGERED |
| **Priority** | CRITICAL | HIGH | MEDIUM | LOW |
| **Estimated Duration** | X hours/days |
| **Risk Level** | HIGH | MEDIUM | LOW |
| **Rollback Available** | YES | PARTIAL | NO |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
[Clear 1-2 sentence description of what this procedure accomplishes]

### 2.2 Business Objectives
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q1: What equipment do we have? | [Description or N/A] |
| Q2: What equipment do customers have? | [Description or N/A] |
| Q3: What do attackers know? | [Description or N/A] |
| Q4: Who are the attackers? | [Description or N/A] |
| Q5: How do we defend? | [Description or N/A] |
| Q6: What happened before? | [Description or N/A] |
| Q7: What will happen next? | [Description or N/A] |
| Q8: What should we do? | [Description or N/A] |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, accessible | `docker ps \| grep neo4j` |
| OpenSPG Server | Healthy | `curl http://localhost:8887/health` |
| MySQL | Running | `docker ps \| grep mysql` |
| MinIO | Running | `curl http://localhost:9000/minio/health/live` |
| Redis | Running | `docker exec openspg-redis redis-cli ping` |
| Qdrant | Running | `curl http://localhost:6333/health` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query/Command | Expected Result |
|-----------|---------------------------|-----------------|
| [Condition 1] | [Query/Command] | [Expected value] |
| [Condition 2] | [Query/Command] | [Expected value] |

### 3.3 Authentication & Credentials

| Service | Credential Source | Environment Variable |
|---------|------------------|---------------------|
| Neo4j | [Location] | `NEO4J_PASSWORD` |
| MySQL | [Location] | `MYSQL_ROOT_PASSWORD` |
| MinIO | [Location] | `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY` |
| External API | [Location] | `[API_KEY_NAME]` |

### 3.4 Dependencies

| Dependency | Version Required | Verification |
|------------|-----------------|--------------|
| Python | 3.9+ | `python --version` |
| neo4j (Python) | 5.x | `pip show neo4j` |
| requests | 2.x | `pip show requests` |
| [Other libs] | [Version] | [Command] |

### 3.5 Prior Procedures Required

| Procedure ID | Procedure Name | Must Complete Before |
|--------------|---------------|---------------------|
| PROC-XXX | [Name] | This procedure |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format | Update Frequency |
|-------------|------|----------|--------|------------------|
| [Source 1] | API / File / Database | [URL/Path] | JSON / XML / CSV | [Frequency] |

### 4.2 Source Details

#### Source 1: [Name]

**Connection Information**:
```
Type: [API | File | Database | Stream]
URL/Path: [Full URL or file path]
Authentication: [None | API Key | OAuth | Basic Auth]
Rate Limits: [X requests per Y time period]
```

**Data Schema**:
```json
{
  "field1": "type (string/int/array)",
  "field2": "type",
  "nested": {
    "subfield": "type"
  }
}
```

**Sample Data**:
```json
{
  "example": "actual sample from source"
}
```

**Extraction Query/Command**:
```bash
# Command to extract data from source
curl -X GET "https://api.example.com/data" -H "Authorization: Bearer $API_KEY"
```

### 4.3 Data Volume Estimates

| Source | Records Expected | Size Estimate | Processing Time |
|--------|-----------------|---------------|-----------------|
| [Source 1] | [Count] | [MB/GB] | [Time] |

---

## 5. DESTINATION

### 5.1 Target System

| Field | Value |
|-------|-------|
| **System** | Neo4j / MySQL / MinIO / Redis / Qdrant / OpenSPG |
| **Container** | [Container name] |
| **Host** | localhost / [hostname] |
| **Port** | [Port number] |
| **Database/Bucket** | [Database name or bucket] |
| **Schema/Collection** | [Schema or collection name] |

### 5.2 Connection Details

```
Protocol: bolt:// | http:// | mysql:// | s3://
Host: localhost
Port: [port]
Database: [database]
User: [username]
Password: [env var reference]
```

### 5.3 Target Schema

#### Node Types Created/Modified

| Label | Properties | Constraints | Indexes |
|-------|-----------|-------------|---------|
| [NodeLabel] | prop1, prop2, prop3 | UNIQUE on [prop] | INDEX on [prop] |

#### Relationship Types Created/Modified

| Type | Source | Target | Properties |
|------|--------|--------|-----------|
| [REL_TYPE] | (:SourceLabel) | (:TargetLabel) | prop1, prop2 |

### 5.4 Target Data Location

**Exact Storage Path**:
```
Container: [container_name]
Volume: [volume_name]
Internal Path: /data/[path]
External Mount: /home/jim/[path]
```

---

## 6. TRANSFORMATION LOGIC

### 6.1 Mapping Rules

| Source Field | Target Property | Transformation |
|--------------|-----------------|----------------|
| source.field1 | target.property1 | Direct copy |
| source.field2 | target.property2 | `UPPER(value)` |
| source.nested.field | target.flat_property | Extract from nested |
| [calculated] | target.derived | `field1 + field2` |

### 6.2 Data Validation Rules

| Rule ID | Field | Validation | Action on Failure |
|---------|-------|------------|------------------|
| VAL-001 | [field] | NOT NULL | REJECT record |
| VAL-002 | [field] | REGEX pattern | WARN and continue |
| VAL-003 | [field] | Range [min-max] | DEFAULT value |

### 6.3 Deduplication Strategy

```
Unique Key: [field1, field2]
On Duplicate: MERGE | UPDATE | SKIP | ERROR
Merge Strategy: [Description of merge logic]
```

### 6.4 Error Handling

| Error Type | Detection | Action | Logging |
|------------|-----------|--------|---------|
| Connection failure | Exception | Retry 3x with backoff | ERROR level |
| Data validation | Rule check | Skip record | WARN level |
| Rate limit | HTTP 429 | Wait and retry | INFO level |
| Partial failure | Transaction | Rollback batch | ERROR level |

---

## 7. EXECUTION STEPS

### 7.1 Pre-Execution Checklist

- [ ] All pre-conditions verified
- [ ] Credentials available and valid
- [ ] Backup created (if required)
- [ ] Notification sent to stakeholders (if required)
- [ ] Maintenance window confirmed (if required)

### 7.2 Step-by-Step Execution

#### Step 1: [Step Name]

**Purpose**: [What this step accomplishes]

**Command**:
```bash
# Actual command to execute
[command]
```

**Expected Output**:
```
[What you should see]
```

**Verification**:
```bash
# Command to verify step completed correctly
[verification command]
```

**Troubleshooting**:
- If [error]: [solution]
- If [error]: [solution]

---

#### Step 2: [Step Name]

**Purpose**: [What this step accomplishes]

**Command**:
```bash
[command]
```

**Expected Output**:
```
[What you should see]
```

**Verification**:
```bash
[verification command]
```

---

### 7.3 Complete Execution Script

```bash
#!/bin/bash
# PROCEDURE: PROC-XXX - [Name]
# Version: X.Y.Z
# Execute: ./proc_xxx_name.sh

set -e  # Exit on error

# Configuration
NEO4J_HOST="localhost"
NEO4J_PORT="7687"
NEO4J_USER="neo4j"
NEO4J_PASS="${NEO4J_PASSWORD:-neo4j@openspg}"

LOG_FILE="/var/log/aeon/proc_xxx_$(date +%Y%m%d_%H%M%S).log"

# Functions
log_info() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" | tee -a "$LOG_FILE"; }
log_error() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" | tee -a "$LOG_FILE"; }
log_warn() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $1" | tee -a "$LOG_FILE"; }

# Pre-condition checks
check_preconditions() {
    log_info "Checking pre-conditions..."
    # Add checks here
}

# Main execution
main() {
    log_info "Starting PROC-XXX: [Name]"
    check_preconditions

    # Step 1
    log_info "Step 1: [Name]"
    # commands

    # Step 2
    log_info "Step 2: [Name]"
    # commands

    log_info "PROC-XXX completed successfully"
}

# Execute
main "$@"
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify Node Counts

```cypher
// Count new/modified nodes
MATCH (n:[Label])
WHERE n.loaded_timestamp > datetime('YYYY-MM-DDTHH:MM:SS')
RETURN count(n) AS new_nodes;
```

**Expected Result**: [count]

#### Verify Relationship Counts

```cypher
// Count new relationships
MATCH ()-[r:[TYPE]]->()
WHERE r.created_at > datetime('YYYY-MM-DDTHH:MM:SS')
RETURN count(r) AS new_relationships;
```

**Expected Result**: [count]

#### Data Quality Check

```cypher
// Check for expected properties
MATCH (n:[Label])
WHERE n.[property] IS NULL
RETURN count(n) AS missing_property_count;
```

**Expected Result**: 0

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| Records processed | Count | >= [X] | [To fill] |
| Error rate | % | < 1% | [To fill] |
| Execution time | Minutes | < [X] | [To fill] |
| Data quality | % valid | >= 99% | [To fill] |

### 8.3 Cleanup Tasks

- [ ] Remove temporary files
- [ ] Clear staging tables (if any)
- [ ] Archive source files (if required)
- [ ] Update procedure log

---

## 9. ROLLBACK PROCEDURE

### 9.1 Rollback Triggers

- Execution time exceeds [X] hours
- Error rate exceeds [X]%
- Critical validation failures
- System instability detected

### 9.2 Rollback Steps

#### Step 1: Stop Current Execution

```bash
# Kill running process
pkill -f proc_xxx
```

#### Step 2: Identify Affected Data

```cypher
// Find nodes created by this procedure run
MATCH (n)
WHERE n.procedure_id = 'PROC-XXX'
  AND n.run_timestamp = datetime('YYYY-MM-DDTHH:MM:SS')
RETURN labels(n), count(n);
```

#### Step 3: Remove Affected Data

```cypher
// Delete nodes created by this run
MATCH (n)
WHERE n.procedure_id = 'PROC-XXX'
  AND n.run_timestamp = datetime('YYYY-MM-DDTHH:MM:SS')
DETACH DELETE n;
```

#### Step 4: Restore from Backup (if needed)

```bash
# Restore Neo4j from backup
neo4j-admin database restore --from-path=/backup/[backup_name] neo4j
```

### 9.3 Rollback Verification

```cypher
// Verify rollback complete
MATCH (n)
WHERE n.procedure_id = 'PROC-XXX'
  AND n.run_timestamp = datetime('YYYY-MM-DDTHH:MM:SS')
RETURN count(n);
// Expected: 0
```

---

## 10. SCHEDULING & AUTOMATION

### 10.1 Cron Schedule (if recurring)

```cron
# Example: Run daily at 2 AM
0 2 * * * /path/to/proc_xxx.sh >> /var/log/aeon/proc_xxx_cron.log 2>&1
```

### 10.2 Trigger Conditions (if event-driven)

| Trigger | Source | Action |
|---------|--------|--------|
| New CVE published | NVD API webhook | Execute procedure |
| File uploaded | MinIO notification | Execute procedure |

### 10.3 Dependencies in Pipeline

```
PROC-001 (Schema Setup)
    ↓
PROC-002 (CVE Load)
    ↓
PROC-003 (CWE Load) ──────┐
    ↓                      ↓
PROC-004 (CAPEC Load) ← PROC-005 (Linking)
    ↓
PROC-006 (Validation)
```

---

## 11. MONITORING & ALERTING

### 11.1 Metrics to Monitor

| Metric | Source | Threshold | Alert |
|--------|--------|-----------|-------|
| Execution duration | Log | > [X] min | WARN |
| Records processed | Log | < [X] | ERROR |
| Error count | Log | > [X] | ERROR |
| Database connections | Neo4j | > 80% | WARN |

### 11.2 Log Locations

| Log Type | Location | Retention |
|----------|----------|-----------|
| Execution log | `/var/log/aeon/proc_xxx.log` | 30 days |
| Error log | `/var/log/aeon/proc_xxx_error.log` | 90 days |
| Audit log | `/var/log/aeon/audit.log` | 1 year |

### 11.3 Alert Channels

| Severity | Channel | Recipients |
|----------|---------|------------|
| CRITICAL | [Slack/Email] | [Team/Individual] |
| ERROR | [Slack/Email] | [Team/Individual] |
| WARN | [Log only] | - |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Name] | Initial version |
| 1.0.1 | YYYY-MM-DD | [Name] | [Description of changes] |

---

## 13. APPENDICES

### Appendix A: Sample Data Files

[Include or reference sample input files]

### Appendix B: Full Cypher Scripts

[Include complete Cypher scripts]

### Appendix C: Troubleshooting Guide

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| [Symptom] | [Cause] | [Solution] |

### Appendix D: Related Documentation

| Document | Location | Relationship |
|----------|----------|--------------|
| [Doc name] | [Path] | [How related] |

---

**End of Procedure Template**
```

---

## PROCEDURE NAMING CONVENTION

| Category | ID Range | Example |
|----------|----------|---------|
| Schema Setup | PROC-001 to PROC-099 | PROC-001-schema-init |
| CVE Operations | PROC-100 to PROC-199 | PROC-101-cve-enrichment |
| CWE Operations | PROC-200 to PROC-299 | PROC-201-cwe-load |
| CAPEC Operations | PROC-300 to PROC-399 | PROC-301-capec-load |
| ATT&CK Operations | PROC-400 to PROC-499 | PROC-401-attack-mapping |
| Threat Actor Ops | PROC-500 to PROC-599 | PROC-501-ta-enrichment |
| Equipment/Asset | PROC-600 to PROC-699 | PROC-601-equipment-load |
| Validation/QA | PROC-900 to PROC-999 | PROC-901-data-validation |

---

## USAGE INSTRUCTIONS

1. **Copy this template** to create new procedures
2. **Fill in ALL sections** - do not skip any
3. **Test thoroughly** before marking APPROVED
4. **Version control** all procedure changes
5. **Review annually** even if procedure unchanged

---

**Template Version**: 1.0.0
**Last Updated**: 2025-11-26
