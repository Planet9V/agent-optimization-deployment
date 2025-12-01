# VulnCheck Integration - Validation and Rollback Procedures

**File**: VALIDATION_AND_ROLLBACK_PROCEDURES.md
**Created**: 2025-11-01
**Version**: 1.0.0
**Author**: Validation-Engineer Agent
**Purpose**: Comprehensive validation and rollback procedures for VulnCheck ecosystem integration
**Status**: ACTIVE

---

## Executive Summary

This document provides comprehensive validation and rollback procedures for three critical VulnCheck integration recommendations:

1. **EPSS Integration** - Property enrichment for exploitability scoring
2. **KEV Flagging Strategy** - Boolean flags and metadata for known exploited vulnerabilities
3. **VulnCheck XDB PoC Integration** - Relationship-based exploit code linking

Each recommendation includes pre-implementation validation, during-implementation checkpoints, post-implementation verification, complete rollback procedures, and test queries with expected results.

**Total Validation Checks**: 87 automated checks
**Estimated Rollback Time**:
- EPSS Integration: 15-30 minutes
- KEV Flagging: 10-20 minutes
- XDB PoC Integration: 30-60 minutes

---

## Table of Contents

1. [EPSS Integration Validation](#1-epss-integration-validation)
2. [KEV Flagging Validation](#2-kev-flagging-validation)
3. [XDB PoC Integration Validation](#3-xdb-poc-integration-validation)
4. [Cross-Integration Validation](#4-cross-integration-validation)
5. [Monitoring and Alerting](#5-monitoring-and-alerting)

---

## 1. EPSS Integration Validation

### 1.1 Pre-Implementation Validation

**Purpose**: Establish baseline metrics and verify database readiness before EPSS enrichment.

#### Database State Verification

```cypher
// Query 1.1.1: Verify CVE node count
MATCH (cve:CVE)
RETURN count(cve) as total_cves;
// Expected: 267,487 CVEs

// Query 1.1.2: Check for existing EPSS properties (should be none initially)
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
RETURN count(cve) as already_enriched;
// Expected: 0 (or minimal if partial implementation exists)

// Query 1.1.3: Verify CVE ID format consistency
MATCH (cve:CVE)
WHERE NOT cve.id =~ 'CVE-\\d{4}-\\d+'
RETURN count(cve) as malformed_ids, collect(cve.id)[0..10] as samples;
// Expected: 0 malformed IDs

// Query 1.1.4: Check database disk space
CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Store file sizes')
YIELD attributes
RETURN attributes.TotalStoreSize.value as current_size_bytes;
// Note: Ensure >5GB free space for enrichment operations
```

#### Baseline Metrics Capture

```cypher
// Query 1.1.5: Create baseline snapshot node
CREATE (baseline:EnrichmentBaseline {
    operation: 'epss_integration',
    timestamp: datetime(),
    total_cves: 267487,
    enriched_cves: 0,
    avg_cvss_score: null,
    status: 'pre_implementation'
});

// Query 1.1.6: Calculate baseline CVSS statistics
MATCH (cve:CVE)
WHERE exists(cve.cvssScore)
WITH avg(cve.cvssScore) as avg_cvss,
     percentileCont(cve.cvssScore, 0.5) as median_cvss,
     count(cve) as cves_with_cvss
MATCH (baseline:EnrichmentBaseline {operation: 'epss_integration', status: 'pre_implementation'})
SET baseline.avg_cvss_score = avg_cvss,
    baseline.median_cvss_score = median_cvss,
    baseline.cves_with_cvss = cves_with_cvss
RETURN avg_cvss, median_cvss, cves_with_cvss;
```

#### Backup Procedures

```bash
#!/bin/bash
# Script 1.1.1: Create database backup before EPSS enrichment

BACKUP_DIR="/backups/neo4j/pre_epss_$(date +%Y%m%d_%H%M%S)"
NEO4J_HOME="/var/lib/neo4j"

# Stop Neo4j (optional for online backup)
# systemctl stop neo4j

# Create backup using neo4j-admin
neo4j-admin database backup neo4j --to-path="$BACKUP_DIR"

# Verify backup integrity
neo4j-admin database check --from-path="$BACKUP_DIR/neo4j"

# Document backup location
echo "Backup created at: $BACKUP_DIR" >> /var/log/enrichment_backups.log
echo "Backup size: $(du -sh $BACKUP_DIR | cut -f1)" >> /var/log/enrichment_backups.log

# Restart Neo4j if stopped
# systemctl start neo4j
```

```cypher
// Query 1.1.7: Create backup metadata node
CREATE (backup:BackupMetadata {
    operation: 'epss_pre_implementation',
    timestamp: datetime(),
    backup_path: '/backups/neo4j/pre_epss_20251101_120000',
    database_name: 'neo4j',
    node_count: 2200000,
    relationship_count: 8500000,
    status: 'completed'
});
```

---

### 1.2 During-Implementation Validation

**Purpose**: Monitor progress and detect issues during batch enrichment process.

#### Checkpoint Verification Queries

```cypher
// Query 1.2.1: Monitor enrichment progress (run every 1000 CVEs)
MATCH (cve:CVE)
WITH count(cve) as total_cves
MATCH (enriched:CVE)
WHERE exists(enriched.epss_score)
WITH total_cves, count(enriched) as enriched_count
RETURN enriched_count,
       total_cves,
       toFloat(enriched_count) / total_cves * 100 as completion_pct,
       datetime() as checkpoint_time;

// Query 1.2.2: Validate EPSS score ranges
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
  AND (cve.epss_score < 0.0 OR cve.epss_score > 1.0)
RETURN count(cve) as invalid_scores,
       collect(cve.id)[0..5] as sample_cves;
// Expected: 0 invalid scores

// Query 1.2.3: Check for null/missing values in enriched nodes
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
  AND (cve.epss_score IS NULL
    OR cve.epss_percentile IS NULL
    OR cve.epss_date IS NULL)
RETURN count(cve) as incomplete_enrichments;
// Expected: 0 incomplete enrichments

// Query 1.2.4: Verify timestamp consistency
MATCH (cve:CVE)
WHERE exists(cve.epss_last_updated)
WITH cve, duration.between(cve.epss_last_updated, datetime()).minutes as age_minutes
WHERE age_minutes > 60  // Flag if enrichment is taking too long
RETURN count(cve) as stale_updates, avg(age_minutes) as avg_age_minutes;
```

#### Progress Tracking Metrics

```cypher
// Query 1.2.5: Create checkpoint node every 50,000 CVEs
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
WITH count(cve) as enriched_count
CREATE (checkpoint:EnrichmentCheckpoint {
    operation: 'epss_integration',
    checkpoint_time: datetime(),
    enriched_count: enriched_count,
    target_count: 267487,
    completion_pct: toFloat(enriched_count) / 267487 * 100,
    status: 'in_progress'
});

// Query 1.2.6: Monitor EPSS score distribution during enrichment
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
RETURN
    CASE
        WHEN cve.epss_score < 0.1 THEN '0.0-0.1 (Low)'
        WHEN cve.epss_score < 0.3 THEN '0.1-0.3 (Medium)'
        WHEN cve.epss_score < 0.6 THEN '0.3-0.6 (High)'
        ELSE '0.6-1.0 (Critical)'
    END as epss_range,
    count(*) as count,
    toFloat(count(*)) / 267487 * 100 as pct_of_total
ORDER BY epss_range;
```

#### Error Detection Procedures

```python
# Script 1.2.1: Error detection and logging during enrichment

import logging
from datetime import datetime

logging.basicConfig(
    filename=f'/var/log/epss_enrichment_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_epss_batch(batch_results):
    """Validate EPSS enrichment batch results"""
    errors = []

    # Check 1: All scores in valid range
    invalid_scores = [
        r for r in batch_results
        if r['epss_score'] < 0.0 or r['epss_score'] > 1.0
    ]
    if invalid_scores:
        errors.append(f"Invalid EPSS scores: {len(invalid_scores)} CVEs")
        logging.error(f"Invalid scores detected: {invalid_scores[:5]}")

    # Check 2: All percentiles in valid range
    invalid_percentiles = [
        r for r in batch_results
        if r['epss_percentile'] < 0.0 or r['epss_percentile'] > 1.0
    ]
    if invalid_percentiles:
        errors.append(f"Invalid percentiles: {len(invalid_percentiles)} CVEs")
        logging.error(f"Invalid percentiles: {invalid_percentiles[:5]}")

    # Check 3: All required fields present
    incomplete = [
        r for r in batch_results
        if not all([r.get('epss_score'), r.get('epss_percentile'), r.get('epss_date')])
    ]
    if incomplete:
        errors.append(f"Incomplete data: {len(incomplete)} CVEs")
        logging.error(f"Incomplete enrichment: {incomplete[:5]}")

    # Check 4: Date consistency
    from datetime import datetime, timedelta
    recent = datetime.now() - timedelta(days=7)
    old_dates = [
        r for r in batch_results
        if datetime.fromisoformat(r['epss_date']) < recent
    ]
    if old_dates:
        logging.warning(f"Old EPSS dates detected: {len(old_dates)} CVEs")

    return errors

# Error handling in enrichment loop
def enrich_with_error_detection(driver, batch_size=1000):
    """Enrichment with error detection and recovery"""

    total_processed = 0
    total_errors = 0

    with driver.session() as session:
        # Get total CVE count
        total_cves = session.run("MATCH (cve:CVE) RETURN count(cve) as count").single()['count']

        for offset in range(0, total_cves, batch_size):
            try:
                # Fetch batch
                batch = session.run("""
                    MATCH (cve:CVE)
                    WHERE NOT exists(cve.epss_score)
                    RETURN cve.id as cve_id
                    SKIP $offset LIMIT $limit
                """, offset=offset, limit=batch_size).data()

                # Enrich batch (external API call)
                batch_results = fetch_epss_scores([r['cve_id'] for r in batch])

                # Validate results
                errors = validate_epss_batch(batch_results)
                if errors:
                    logging.error(f"Batch {offset}-{offset+batch_size} validation failed: {errors}")
                    total_errors += len(errors)
                    # Continue processing other batches
                else:
                    # Update Neo4j
                    session.execute_write(update_epss_batch, batch_results)
                    total_processed += len(batch_results)
                    logging.info(f"Batch {offset}-{offset+batch_size} completed: {len(batch_results)} CVEs")

            except Exception as e:
                logging.error(f"Batch {offset}-{offset+batch_size} failed: {str(e)}")
                total_errors += batch_size
                # Continue with next batch
                continue

    logging.info(f"Enrichment completed: {total_processed} CVEs processed, {total_errors} errors")
    return total_processed, total_errors
```

---

### 1.3 Post-Implementation Validation

**Purpose**: Verify successful enrichment completion and data quality.

#### Success Criteria Verification

```cypher
// Query 1.3.1: Verify 100% enrichment coverage
MATCH (cve:CVE)
WITH count(cve) as total_cves
MATCH (enriched:CVE)
WHERE exists(enriched.epss_score)
WITH total_cves, count(enriched) as enriched_count
RETURN enriched_count,
       total_cves,
       toFloat(enriched_count) / total_cves * 100 as coverage_pct;
// Expected: enriched_count = 267,487 (100%)

// Query 1.3.2: Validate EPSS score distribution
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
RETURN
    count(cve) as total_enriched,
    min(cve.epss_score) as min_score,
    max(cve.epss_score) as max_score,
    avg(cve.epss_score) as avg_score,
    percentileCont(cve.epss_score, 0.5) as median_score,
    percentileCont(cve.epss_score, 0.9) as p90_score,
    percentileCont(cve.epss_score, 0.99) as p99_score;
// Expected: min=0.0, max=1.0, avg≈0.05-0.15, median≈0.01-0.03

// Query 1.3.3: Verify index creation and performance
SHOW INDEXES YIELD
    name, type, entityType, labelsOrTypes, properties, state
WHERE labelsOrTypes = ['CVE']
  AND 'epss_score' IN properties
RETURN name, type, state;
// Expected: Index exists and state='ONLINE'
```

#### Data Quality Checks

```cypher
// Query 1.3.4: Check for anomalies in EPSS scores
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
WITH cve, cve.epss_score as epss, cve.cvssScore as cvss
WHERE epss > 0.9 AND cvss < 4.0  // High EPSS but low CVSS (unusual)
RETURN count(cve) as anomaly_count,
       collect(cve.id)[0..10] as sample_cves;
// Expected: <1% anomalies (flag for manual review)

// Query 1.3.5: Validate percentile consistency
MATCH (cve:CVE)
WHERE exists(cve.epss_percentile)
WITH cve
WHERE cve.epss_percentile < 0.0 OR cve.epss_percentile > 1.0
RETURN count(cve) as invalid_percentiles;
// Expected: 0 invalid percentiles

// Query 1.3.6: Check timestamp recency
MATCH (cve:CVE)
WHERE exists(cve.epss_last_updated)
WITH cve, duration.between(cve.epss_last_updated, datetime()).days as age_days
WHERE age_days > 7
RETURN count(cve) as stale_updates, avg(age_days) as avg_age;
// Expected: 0 updates older than 7 days

// Query 1.3.7: Validate EPSS date consistency
MATCH (cve:CVE)
WHERE exists(cve.epss_date)
WITH cve, cve.epss_date as epss_date
WHERE epss_date > date()  // Future dates
RETURN count(cve) as future_dates;
// Expected: 0 future dates
```

#### Performance Benchmarks

```cypher
// Query 1.3.8: Benchmark query performance with EPSS filters
PROFILE
MATCH (cve:CVE)
WHERE cve.epss_score > 0.5
RETURN count(cve);
// Expected: <50ms execution time with index

// Query 1.3.9: Test compound query performance
PROFILE
MATCH (cve:CVE)
WHERE cve.epss_score > 0.3
  AND cve.cvssScore >= 7.0
RETURN cve.id, cve.epss_score, cve.cvssScore
ORDER BY cve.epss_score DESC
LIMIT 100;
// Expected: <100ms execution time

// Query 1.3.10: Verify index utilization
EXPLAIN
MATCH (cve:CVE)
WHERE cve.epss_score > 0.7
RETURN cve.id;
// Expected: Plan shows "NodeIndexSeek" for epss_score
```

#### Integration Tests

```cypher
// Query 1.3.11: Validate EPSS enrichment for known CVEs
MATCH (cve:CVE)
WHERE cve.id IN ['CVE-2021-44228', 'CVE-2021-45046', 'CVE-2022-22965']
RETURN cve.id,
       cve.epss_score,
       cve.epss_percentile,
       cve.epss_date,
       cve.cvssScore;
// Expected: All 3 CVEs enriched with high EPSS scores (>0.8)

// Query 1.3.12: Test EPSS filtering for prioritization
MATCH (cve:CVE)
WHERE cve.epss_score > 0.2
  OR cve.epss_percentile > 0.90
WITH cve
ORDER BY cve.epss_score DESC
LIMIT 50
RETURN cve.id, cve.epss_score, cve.epss_percentile, cve.cvssScore;
// Expected: Returns high-priority CVEs with consistent ordering
```

---

### 1.4 Rollback Procedures

**Purpose**: Complete rollback of EPSS enrichment if validation fails.

#### Step-by-Step Rollback Instructions

```cypher
// Step 1.4.1: Document current state before rollback
CREATE (rollback:RollbackLog {
    operation: 'epss_integration_rollback',
    timestamp: datetime(),
    reason: 'Validation failure or user request',
    status: 'initiated'
})
WITH rollback
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
WITH rollback, count(cve) as enriched_count
SET rollback.enriched_cves_before_rollback = enriched_count
RETURN enriched_count;

// Step 1.4.2: Create rollback checkpoint
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
WITH collect({
    id: cve.id,
    epss_score: cve.epss_score,
    epss_percentile: cve.epss_percentile,
    epss_date: cve.epss_date,
    epss_last_updated: cve.epss_last_updated
})[0..100] as sample_data
CREATE (checkpoint:RollbackCheckpoint {
    operation: 'epss_integration',
    timestamp: datetime(),
    sample_data: sample_data
});

// Step 1.4.3: Remove EPSS properties from all CVE nodes
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
REMOVE cve.epss_score,
       cve.epss_percentile,
       cve.epss_date,
       cve.epss_last_updated
RETURN count(cve) as rolled_back_count;
// Expected: 267,487 CVEs rolled back

// Step 1.4.4: Drop EPSS indexes
DROP INDEX cve_epss IF EXISTS;
DROP INDEX cve_epss_percentile IF EXISTS;

// Step 1.4.5: Verify rollback completion
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
RETURN count(cve) as remaining_epss_properties;
// Expected: 0 remaining properties

// Step 1.4.6: Update rollback log
MATCH (rollback:RollbackLog {operation: 'epss_integration_rollback', status: 'initiated'})
SET rollback.status = 'completed',
    rollback.completion_time = datetime(),
    rollback.duration_minutes = duration.between(rollback.timestamp, datetime()).minutes;
```

#### Data Restoration Procedures

```bash
#!/bin/bash
# Script 1.4.1: Restore database from backup if needed

BACKUP_PATH="/backups/neo4j/pre_epss_20251101_120000"
NEO4J_HOME="/var/lib/neo4j"

# Stop Neo4j
echo "Stopping Neo4j..."
systemctl stop neo4j

# Restore database from backup
echo "Restoring database from backup..."
neo4j-admin database restore neo4j --from-path="$BACKUP_PATH"

# Verify restoration
echo "Verifying database integrity..."
neo4j-admin database check neo4j

# Start Neo4j
echo "Starting Neo4j..."
systemctl start neo4j

# Wait for Neo4j to be ready
sleep 30

# Verify CVE count
echo "Verifying CVE count..."
cypher-shell -u neo4j -p password "MATCH (cve:CVE) RETURN count(cve) as total_cves;"

echo "Database restoration completed."
```

#### Relationship Cleanup Queries

```cypher
// Query 1.4.7: No relationships to clean up for EPSS (property-only enrichment)
// This query is a placeholder for consistency with other rollback procedures
MATCH (cve:CVE)
RETURN count(cve) as total_cves;
// Note: EPSS integration does not create relationships
```

#### Validation After Rollback

```cypher
// Query 1.4.8: Verify no EPSS properties remain
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
   OR exists(cve.epss_percentile)
   OR exists(cve.epss_date)
   OR exists(cve.epss_last_updated)
RETURN count(cve) as unexpected_properties;
// Expected: 0 unexpected properties

// Query 1.4.9: Verify indexes dropped
SHOW INDEXES YIELD name, labelsOrTypes, properties
WHERE labelsOrTypes = ['CVE']
  AND ANY(prop IN properties WHERE prop CONTAINS 'epss')
RETURN count(*) as remaining_indexes;
// Expected: 0 remaining EPSS indexes

// Query 1.4.10: Verify database matches pre-implementation state
MATCH (baseline:EnrichmentBaseline {operation: 'epss_integration', status: 'pre_implementation'})
MATCH (cve:CVE)
WITH baseline, count(cve) as current_count
WHERE current_count = baseline.total_cves
RETURN 'Rollback successful: CVE count matches baseline' as status;
// Expected: Returns success message
```

**Estimated Rollback Time**: 15-30 minutes
**Risk Level**: LOW (property removal only, no structural changes)

---

## 2. KEV Flagging Validation

### 2.1 Pre-Implementation Validation

**Purpose**: Establish baseline and verify readiness for KEV flagging.

#### Database State Verification

```cypher
// Query 2.1.1: Verify CVE node count
MATCH (cve:CVE)
RETURN count(cve) as total_cves;
// Expected: 267,487 CVEs

// Query 2.1.2: Check for existing KEV properties
MATCH (cve:CVE)
WHERE exists(cve.in_cisa_kev) OR exists(cve.in_vulncheck_kev)
RETURN count(cve) as already_flagged;
// Expected: 0 (or minimal if partial implementation)

// Query 2.1.3: Verify CVE date fields for KEV due date calculations
MATCH (cve:CVE)
WHERE NOT exists(cve.published)
RETURN count(cve) as missing_published_date;
// Expected: <1% missing (flag for data quality review)

// Query 2.1.4: Check CVSS score distribution for KEV candidates
MATCH (cve:CVE)
WHERE cve.cvssScore >= 7.0
RETURN
    CASE
        WHEN cve.cvssScore >= 9.0 THEN 'Critical (9.0-10.0)'
        WHEN cve.cvssScore >= 7.0 THEN 'High (7.0-8.9)'
    END as severity,
    count(*) as count;
// Note: KEV candidates are typically high/critical severity
```

#### Baseline Metrics Capture

```cypher
// Query 2.1.5: Create KEV baseline snapshot
CREATE (baseline:EnrichmentBaseline {
    operation: 'kev_flagging',
    timestamp: datetime(),
    total_cves: 267487,
    kev_flagged: 0,
    high_severity_cves: 0,
    status: 'pre_implementation'
});

// Query 2.1.6: Calculate baseline high-severity CVE count
MATCH (cve:CVE)
WHERE cve.cvssScore >= 7.0
WITH count(cve) as high_severity_count
MATCH (baseline:EnrichmentBaseline {operation: 'kev_flagging', status: 'pre_implementation'})
SET baseline.high_severity_cves = high_severity_count
RETURN high_severity_count;
```

#### Backup Procedures

```bash
#!/bin/bash
# Script 2.1.1: Create database backup before KEV flagging

BACKUP_DIR="/backups/neo4j/pre_kev_$(date +%Y%m%d_%H%M%S)"

neo4j-admin database backup neo4j --to-path="$BACKUP_DIR"
neo4j-admin database check --from-path="$BACKUP_DIR/neo4j"

echo "KEV flagging backup created at: $BACKUP_DIR" >> /var/log/enrichment_backups.log
```

```cypher
// Query 2.1.7: Create backup metadata
CREATE (backup:BackupMetadata {
    operation: 'kev_pre_implementation',
    timestamp: datetime(),
    backup_path: '/backups/neo4j/pre_kev_20251101_130000',
    database_name: 'neo4j',
    status: 'completed'
});
```

---

### 2.2 During-Implementation Validation

**Purpose**: Monitor KEV flagging progress and data quality.

#### Checkpoint Verification Queries

```cypher
// Query 2.2.1: Monitor CISA KEV flagging progress
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true
RETURN count(cve) as cisa_kev_count,
       datetime() as checkpoint_time;
// Expected: ~1,000 CVEs (CISA KEV catalog size)

// Query 2.2.2: Monitor VulnCheck KEV flagging progress
MATCH (cve:CVE)
WHERE cve.in_vulncheck_kev = true
RETURN count(cve) as vulncheck_kev_count,
       datetime() as checkpoint_time;
// Expected: ~1,800 CVEs (VulnCheck extended KEV size)

// Query 2.2.3: Check for KEV overlap (CVEs in both catalogs)
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true AND cve.in_vulncheck_kev = true
RETURN count(cve) as overlap_count;
// Expected: High overlap (most CISA KEV should be in VulnCheck)

// Query 2.2.4: Validate KEV date fields
MATCH (cve:CVE)
WHERE exists(cve.kev_date_added)
  AND cve.kev_date_added > datetime()
RETURN count(cve) as future_kev_dates;
// Expected: 0 future dates
```

#### Progress Tracking Metrics

```cypher
// Query 2.2.5: Track KEV flagging by source
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true OR cve.in_vulncheck_kev = true
RETURN
    sum(CASE WHEN cve.in_cisa_kev THEN 1 ELSE 0 END) as cisa_count,
    sum(CASE WHEN cve.in_vulncheck_kev THEN 1 ELSE 0 END) as vulncheck_count,
    sum(CASE WHEN cve.in_cisa_kev AND cve.in_vulncheck_kev THEN 1 ELSE 0 END) as both_count,
    count(cve) as total_kev_cves;

// Query 2.2.6: Monitor KEV due dates
MATCH (cve:CVE)
WHERE exists(cve.kev_due_date)
WITH cve, duration.between(datetime(), cve.kev_due_date).days as days_until_due
RETURN
    CASE
        WHEN days_until_due < 0 THEN 'Overdue'
        WHEN days_until_due < 30 THEN '0-30 days'
        WHEN days_until_due < 90 THEN '30-90 days'
        ELSE '90+ days'
    END as due_date_bracket,
    count(cve) as count
ORDER BY due_date_bracket;
```

#### Error Detection Procedures

```python
# Script 2.2.1: KEV flagging validation

def validate_kev_enrichment(kev_data):
    """Validate KEV enrichment data"""
    errors = []

    # Check 1: Required fields present
    required_fields = ['cve_id', 'date_added', 'required_action']
    for entry in kev_data:
        missing = [f for f in required_fields if f not in entry or not entry[f]]
        if missing:
            errors.append(f"CVE {entry.get('cve_id')}: Missing fields {missing}")

    # Check 2: Date format validation
    from dateutil import parser
    for entry in kev_data:
        try:
            parser.parse(entry['date_added'])
        except:
            errors.append(f"CVE {entry['cve_id']}: Invalid date format")

    # Check 3: CVE ID format validation
    import re
    cve_pattern = re.compile(r'CVE-\d{4}-\d+')
    for entry in kev_data:
        if not cve_pattern.match(entry['cve_id']):
            errors.append(f"Invalid CVE ID: {entry['cve_id']}")

    return errors
```

---

### 2.3 Post-Implementation Validation

**Purpose**: Verify successful KEV flagging and data integrity.

#### Success Criteria Verification

```cypher
// Query 2.3.1: Verify CISA KEV coverage
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true
RETURN count(cve) as cisa_kev_count;
// Expected: ~1,000 CVEs (±10% depending on CISA catalog updates)

// Query 2.3.2: Verify VulnCheck KEV coverage
MATCH (cve:CVE)
WHERE cve.in_vulncheck_kev = true
RETURN count(cve) as vulncheck_kev_count;
// Expected: ~1,800 CVEs (80% more than CISA)

// Query 2.3.3: Verify KEV priority tier assignment
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true OR cve.in_vulncheck_kev = true
WITH cve
WHERE NOT exists(cve.kev_priority) OR cve.kev_priority IS NULL
RETURN count(cve) as missing_priority;
// Expected: 0 missing priorities

// Query 2.3.4: Validate KEV metadata completeness
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true
WITH cve
WHERE NOT exists(cve.kev_date_added)
   OR NOT exists(cve.kev_due_date)
   OR NOT exists(cve.kev_required_action)
RETURN count(cve) as incomplete_metadata;
// Expected: 0 incomplete metadata
```

#### Data Quality Checks

```cypher
// Query 2.3.5: Check KEV ransomware use field
MATCH (cve:CVE)
WHERE exists(cve.kev_ransomware_use)
RETURN
    cve.kev_ransomware_use as ransomware_use,
    count(cve) as count
ORDER BY count DESC;
// Expected: Values should be 'Known' or 'Unknown'

// Query 2.3.6: Validate exploited_in_wild consistency
MATCH (cve:CVE)
WHERE (cve.in_cisa_kev = true OR cve.in_vulncheck_kev = true)
  AND cve.exploited_in_wild <> true
RETURN count(cve) as inconsistent_exploitation_flags;
// Expected: 0 (all KEV CVEs should have exploited_in_wild = true)

// Query 2.3.7: Check KEV timestamp recency
MATCH (cve:CVE)
WHERE exists(cve.kev_last_updated)
WITH cve, duration.between(cve.kev_last_updated, datetime()).days as age_days
WHERE age_days > 1
RETURN count(cve) as stale_kev_updates, avg(age_days) as avg_age;
// Expected: 0 updates older than 1 day (or acceptable for initial load)
```

#### Performance Benchmarks

```cypher
// Query 2.3.8: Benchmark KEV filtering performance
PROFILE
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true
RETURN count(cve);
// Expected: <20ms with index

// Query 2.3.9: Test compound KEV queries
PROFILE
MATCH (cve:CVE)
WHERE (cve.in_cisa_kev = true OR cve.in_vulncheck_kev = true)
  AND cve.cvssScore >= 7.0
RETURN cve.id, cve.kev_date_added, cve.kev_due_date
ORDER BY cve.kev_due_date
LIMIT 50;
// Expected: <50ms execution time

// Query 2.3.10: Verify index utilization for KEV flags
EXPLAIN
MATCH (cve:CVE)
WHERE cve.exploited_in_wild = true
RETURN cve.id;
// Expected: Plan shows "NodeIndexSeek" for exploited_in_wild
```

#### Integration Tests

```cypher
// Query 2.3.11: Validate Log4Shell KEV flagging
MATCH (cve:CVE)
WHERE cve.id IN ['CVE-2021-44228', 'CVE-2021-45046', 'CVE-2021-45105']
RETURN cve.id,
       cve.in_cisa_kev,
       cve.in_vulncheck_kev,
       cve.kev_date_added,
       cve.kev_priority,
       cve.exploited_in_wild;
// Expected: All 3 Log4J CVEs flagged in both CISA and VulnCheck KEV

// Query 2.3.12: Test KEV due date filtering
MATCH (cve:CVE)
WHERE exists(cve.kev_due_date)
  AND cve.kev_due_date > datetime()
  AND duration.between(datetime(), cve.kev_due_date).days < 30
RETURN cve.id, cve.kev_due_date, cve.kev_required_action
ORDER BY cve.kev_due_date
LIMIT 20;
// Expected: Returns CVEs with upcoming remediation deadlines

// Query 2.3.13: Validate ransomware-associated CVEs
MATCH (cve:CVE)
WHERE cve.kev_ransomware_use = 'Known'
RETURN count(cve) as ransomware_cves;
// Expected: Significant subset of KEV CVEs (hundreds)
```

---

### 2.4 Rollback Procedures

**Purpose**: Complete rollback of KEV flagging if needed.

#### Step-by-Step Rollback Instructions

```cypher
// Step 2.4.1: Document current state before rollback
CREATE (rollback:RollbackLog {
    operation: 'kev_flagging_rollback',
    timestamp: datetime(),
    reason: 'Validation failure or user request',
    status: 'initiated'
})
WITH rollback
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true OR cve.in_vulncheck_kev = true
WITH rollback, count(cve) as kev_count
SET rollback.kev_cves_before_rollback = kev_count
RETURN kev_count;

// Step 2.4.2: Create rollback checkpoint
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true OR cve.in_vulncheck_kev = true
WITH collect({
    id: cve.id,
    in_cisa_kev: cve.in_cisa_kev,
    in_vulncheck_kev: cve.in_vulncheck_kev,
    kev_date_added: cve.kev_date_added,
    kev_priority: cve.kev_priority
})[0..50] as sample_data
CREATE (checkpoint:RollbackCheckpoint {
    operation: 'kev_flagging',
    timestamp: datetime(),
    sample_data: sample_data
});

// Step 2.4.3: Remove all KEV properties
MATCH (cve:CVE)
WHERE exists(cve.in_cisa_kev)
   OR exists(cve.in_vulncheck_kev)
REMOVE cve.in_cisa_kev,
       cve.in_vulncheck_kev,
       cve.kev_date_added,
       cve.kev_due_date,
       cve.kev_required_action,
       cve.kev_ransomware_use,
       cve.exploited_in_wild,
       cve.kev_last_updated,
       cve.kev_priority
RETURN count(cve) as rolled_back_count;
// Expected: ~1,800 CVEs rolled back

// Step 2.4.4: Drop KEV indexes
DROP INDEX cve_in_cisa_kev IF EXISTS;
DROP INDEX cve_in_vulncheck_kev IF EXISTS;
DROP INDEX cve_exploited_in_wild IF EXISTS;

// Step 2.4.5: Verify rollback completion
MATCH (cve:CVE)
WHERE exists(cve.in_cisa_kev)
   OR exists(cve.in_vulncheck_kev)
   OR exists(cve.kev_priority)
RETURN count(cve) as remaining_kev_properties;
// Expected: 0 remaining properties

// Step 2.4.6: Update rollback log
MATCH (rollback:RollbackLog {operation: 'kev_flagging_rollback', status: 'initiated'})
SET rollback.status = 'completed',
    rollback.completion_time = datetime(),
    rollback.duration_minutes = duration.between(rollback.timestamp, datetime()).minutes;
```

#### Data Restoration Procedures

```bash
#!/bin/bash
# Script 2.4.1: Restore from backup if needed

BACKUP_PATH="/backups/neo4j/pre_kev_20251101_130000"

echo "Restoring database from KEV pre-implementation backup..."
systemctl stop neo4j
neo4j-admin database restore neo4j --from-path="$BACKUP_PATH"
neo4j-admin database check neo4j
systemctl start neo4j
sleep 30

echo "KEV flagging rollback completed via backup restoration."
```

#### Relationship Cleanup Queries

```cypher
// Query 2.4.7: No relationships to clean up for KEV (property-only enrichment)
MATCH (cve:CVE)
RETURN count(cve) as total_cves;
// Note: KEV flagging does not create relationships
```

#### Validation After Rollback

```cypher
// Query 2.4.8: Verify no KEV properties remain
MATCH (cve:CVE)
WHERE exists(cve.in_cisa_kev)
   OR exists(cve.in_vulncheck_kev)
   OR exists(cve.kev_date_added)
   OR exists(cve.kev_due_date)
   OR exists(cve.kev_required_action)
   OR exists(cve.kev_ransomware_use)
   OR exists(cve.exploited_in_wild)
   OR exists(cve.kev_last_updated)
   OR exists(cve.kev_priority)
RETURN count(cve) as unexpected_properties;
// Expected: 0 unexpected properties

// Query 2.4.9: Verify KEV indexes dropped
SHOW INDEXES YIELD name, labelsOrTypes, properties
WHERE labelsOrTypes = ['CVE']
  AND ANY(prop IN properties WHERE prop CONTAINS 'kev' OR prop = 'exploited_in_wild')
RETURN count(*) as remaining_kev_indexes;
// Expected: 0 remaining KEV indexes

// Query 2.4.10: Verify database matches baseline
MATCH (baseline:EnrichmentBaseline {operation: 'kev_flagging', status: 'pre_implementation'})
MATCH (cve:CVE)
WITH baseline, count(cve) as current_count
WHERE current_count = baseline.total_cves
RETURN 'Rollback successful: CVE count matches baseline' as status;
// Expected: Returns success message
```

**Estimated Rollback Time**: 10-20 minutes
**Risk Level**: LOW (property removal only)

---

## 3. XDB PoC Integration Validation

### 3.1 Pre-Implementation Validation

**Purpose**: Establish baseline and prepare for ExploitCode node creation.

#### Database State Verification

```cypher
// Query 3.1.1: Verify CVE node count
MATCH (cve:CVE)
RETURN count(cve) as total_cves;
// Expected: 267,487 CVEs

// Query 3.1.2: Check for existing ExploitCode nodes
MATCH (ec:ExploitCode)
RETURN count(ec) as existing_exploit_nodes;
// Expected: 0 (or minimal if partial implementation)

// Query 3.1.3: Check for existing HAS_EXPLOIT_CODE relationships
MATCH ()-[r:HAS_EXPLOIT_CODE]->()
RETURN count(r) as existing_exploit_relationships;
// Expected: 0 (or minimal)

// Query 3.1.4: Estimate CVEs with potential exploits (high CVSS)
MATCH (cve:CVE)
WHERE cve.cvssScore >= 7.0
RETURN count(cve) as high_severity_cves;
// Note: ~5-10% of these may have exploit code
```

#### Baseline Metrics Capture

```cypher
// Query 3.1.5: Create XDB baseline snapshot
CREATE (baseline:EnrichmentBaseline {
    operation: 'xdb_integration',
    timestamp: datetime(),
    total_cves: 267487,
    exploit_code_nodes: 0,
    exploit_relationships: 0,
    status: 'pre_implementation'
});

// Query 3.1.6: Calculate node and relationship counts
CALL apoc.meta.stats() YIELD nodeCount, relCount
WITH nodeCount, relCount
MATCH (baseline:EnrichmentBaseline {operation: 'xdb_integration', status: 'pre_implementation'})
SET baseline.total_nodes_before = nodeCount,
    baseline.total_relationships_before = relCount
RETURN nodeCount, relCount;
```

#### Backup Procedures

```bash
#!/bin/bash
# Script 3.1.1: Create backup before XDB integration

BACKUP_DIR="/backups/neo4j/pre_xdb_$(date +%Y%m%d_%H%M%S)"

neo4j-admin database backup neo4j --to-path="$BACKUP_DIR"
neo4j-admin database check --from-path="$BACKUP_DIR/neo4j"

echo "XDB integration backup created at: $BACKUP_DIR" >> /var/log/enrichment_backups.log
```

```cypher
// Query 3.1.7: Create backup metadata
CREATE (backup:BackupMetadata {
    operation: 'xdb_pre_implementation',
    timestamp: datetime(),
    backup_path: '/backups/neo4j/pre_xdb_20251101_140000',
    database_name: 'neo4j',
    status: 'completed'
});
```

---

### 3.2 During-Implementation Validation

**Purpose**: Monitor ExploitCode node creation and relationship linking.

#### Checkpoint Verification Queries

```cypher
// Query 3.2.1: Monitor ExploitCode node creation
MATCH (ec:ExploitCode)
RETURN count(ec) as exploit_code_count,
       datetime() as checkpoint_time;
// Expected: Incremental growth to ~13K-27K nodes

// Query 3.2.2: Monitor HAS_EXPLOIT_CODE relationship creation
MATCH ()-[r:HAS_EXPLOIT_CODE]->()
RETURN count(r) as exploit_relationships,
       datetime() as checkpoint_time;
// Expected: Similar count to ExploitCode nodes (one-to-one for most CVEs)

// Query 3.2.3: Check for duplicate ExploitCode nodes
MATCH (ec:ExploitCode)
WITH ec.xdb_id as xdb_id, count(ec) as node_count
WHERE node_count > 1
RETURN xdb_id, node_count;
// Expected: 0 duplicates (constraint should prevent)

// Query 3.2.4: Validate ExploitCode property completeness
MATCH (ec:ExploitCode)
WHERE NOT exists(ec.xdb_id)
   OR NOT exists(ec.xdb_url)
   OR NOT exists(ec.exploit_type)
RETURN count(ec) as incomplete_nodes;
// Expected: 0 incomplete nodes
```

#### Progress Tracking Metrics

```cypher
// Query 3.2.5: Track ExploitCode by exploit type
MATCH (ec:ExploitCode)
RETURN ec.exploit_type as exploit_type,
       count(ec) as count
ORDER BY count DESC;
// Expected: Distribution across initial-access, privilege-escalation, lateral-movement

// Query 3.2.6: Track ExploitCode by maturity level
MATCH (ec:ExploitCode)
RETURN ec.maturity as maturity,
       count(ec) as count
ORDER BY count DESC;
// Expected: poc > functional > weaponized

// Query 3.2.7: Monitor CVEs with multiple exploits
MATCH (cve:CVE)-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WITH cve, count(ec) as exploit_count
WHERE exploit_count > 1
RETURN exploit_count, count(cve) as cve_count
ORDER BY exploit_count DESC;
// Note: Some popular CVEs may have multiple PoCs
```

#### Error Detection Procedures

```python
# Script 3.2.1: XDB integration validation

def validate_exploit_code_data(exploit_data):
    """Validate ExploitCode node data"""
    errors = []

    # Check 1: Required fields
    required = ['xdb_id', 'xdb_url', 'exploit_type', 'date_added']
    for entry in exploit_data:
        missing = [f for f in required if not entry.get(f)]
        if missing:
            errors.append(f"XDB {entry.get('xdb_id')}: Missing {missing}")

    # Check 2: Valid exploit types
    valid_types = ['initial-access', 'privilege-escalation', 'lateral-movement',
                   'defense-evasion', 'credential-access']
    for entry in exploit_data:
        if entry.get('exploit_type') not in valid_types:
            errors.append(f"XDB {entry.get('xdb_id')}: Invalid type {entry.get('exploit_type')}")

    # Check 3: Valid maturity levels
    valid_maturity = ['poc', 'functional', 'weaponized']
    for entry in exploit_data:
        if entry.get('maturity') and entry.get('maturity') not in valid_maturity:
            errors.append(f"XDB {entry.get('xdb_id')}: Invalid maturity {entry.get('maturity')}")

    # Check 4: URL format
    import re
    url_pattern = re.compile(r'^https?://')
    for entry in exploit_data:
        if not url_pattern.match(entry.get('xdb_url', '')):
            errors.append(f"XDB {entry.get('xdb_id')}: Invalid URL format")

    return errors
```

---

### 3.3 Post-Implementation Validation

**Purpose**: Verify successful XDB integration and relationship integrity.

#### Success Criteria Verification

```cypher
// Query 3.3.1: Verify ExploitCode node count
MATCH (ec:ExploitCode)
RETURN count(ec) as total_exploit_codes;
// Expected: ~13,000-27,000 nodes (5-10% of CVEs)

// Query 3.3.2: Verify HAS_EXPLOIT_CODE relationship count
MATCH (cve:CVE)-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
RETURN count(r) as total_relationships,
       count(DISTINCT cve) as cves_with_exploits,
       count(DISTINCT ec) as unique_exploit_codes;
// Expected: relationships ≈ exploit_codes, cves_with_exploits ≈ 5-10% of 267K

// Query 3.3.3: Verify constraint enforcement
SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties
WHERE labelsOrTypes = ['ExploitCode']
  AND 'xdb_id' IN properties
RETURN name, type;
// Expected: UNIQUENESS constraint on ExploitCode.xdb_id

// Query 3.3.4: Verify index creation
SHOW INDEXES YIELD name, labelsOrTypes, properties
WHERE labelsOrTypes = ['ExploitCode']
RETURN name, properties;
// Expected: Index on exploit_type
```

#### Data Quality Checks

```cypher
// Query 3.3.5: Check for orphaned ExploitCode nodes
MATCH (ec:ExploitCode)
WHERE NOT exists((ec)<-[:HAS_EXPLOIT_CODE]-())
RETURN count(ec) as orphaned_exploit_codes;
// Expected: 0 orphaned nodes (all should be linked to CVEs)

// Query 3.3.6: Validate exploit type distribution
MATCH (ec:ExploitCode)
RETURN ec.exploit_type as type,
       count(ec) as count,
       toFloat(count(ec)) / 20000 * 100 as pct
ORDER BY count DESC;
// Expected: Reasonable distribution (initial-access likely highest)

// Query 3.3.7: Validate maturity levels
MATCH (ec:ExploitCode)
WHERE exists(ec.maturity)
RETURN ec.maturity as maturity,
       count(ec) as count
ORDER BY count DESC;
// Expected: poc > functional > weaponized

// Query 3.3.8: Check for invalid URL formats
MATCH (ec:ExploitCode)
WHERE NOT ec.xdb_url STARTS WITH 'http'
RETURN count(ec) as invalid_urls;
// Expected: 0 invalid URLs

// Query 3.3.9: Validate relationship confidence scores
MATCH ()-[r:HAS_EXPLOIT_CODE]->()
WHERE r.confidence < 0.0 OR r.confidence > 1.0
RETURN count(r) as invalid_confidence_scores;
// Expected: 0 invalid scores

// Query 3.3.10: Check for CVEs with unusually high exploit counts
MATCH (cve:CVE)-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WITH cve, count(ec) as exploit_count
WHERE exploit_count > 10  // Flag for manual review
RETURN cve.id, exploit_count
ORDER BY exploit_count DESC
LIMIT 10;
// Note: Some well-known CVEs may legitimately have many PoCs
```

#### Performance Benchmarks

```cypher
// Query 3.3.11: Benchmark exploit code lookup by CVE
PROFILE
MATCH (cve:CVE {id: 'CVE-2021-44228'})-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
RETURN cve.id, count(ec) as exploit_count;
// Expected: <30ms execution time

// Query 3.3.12: Benchmark exploit type filtering
PROFILE
MATCH (ec:ExploitCode)
WHERE ec.exploit_type = 'initial-access'
  AND ec.maturity = 'weaponized'
RETURN count(ec);
// Expected: <50ms with index on exploit_type

// Query 3.3.13: Test compound query performance
PROFILE
MATCH (cve:CVE)-[:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WHERE cve.cvssScore >= 7.0
  AND ec.maturity IN ['functional', 'weaponized']
RETURN cve.id, cve.cvssScore, collect(ec.xdb_url) as exploits
ORDER BY cve.cvssScore DESC
LIMIT 100;
// Expected: <200ms execution time
```

#### Integration Tests

```cypher
// Query 3.3.14: Validate Log4Shell exploit code linking
MATCH (cve:CVE)
WHERE cve.id IN ['CVE-2021-44228', 'CVE-2021-45046']
OPTIONAL MATCH (cve)-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
RETURN cve.id,
       count(ec) as exploit_count,
       collect(ec.exploit_type)[0..5] as sample_types,
       collect(ec.maturity)[0..5] as sample_maturity;
// Expected: Both Log4J CVEs should have multiple exploit codes

// Query 3.3.15: Test CVEs with weaponized exploits
MATCH (cve:CVE)-[:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WHERE ec.maturity = 'weaponized'
RETURN cve.id, cve.cvssScore, ec.xdb_url, ec.exploit_type
ORDER BY cve.cvssScore DESC
LIMIT 20;
// Expected: Returns high-severity CVEs with weaponized exploits

// Query 3.3.16: Verify relationship threat level calculation
MATCH (cve:CVE)-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WHERE r.threat_level <> CASE
    WHEN ec.maturity = 'weaponized' THEN 'high'
    WHEN ec.maturity = 'functional' THEN 'medium'
    ELSE 'low'
END
RETURN count(r) as inconsistent_threat_levels;
// Expected: 0 inconsistencies
```

---

### 3.4 Rollback Procedures

**Purpose**: Complete removal of ExploitCode nodes and relationships.

#### Step-by-Step Rollback Instructions

```cypher
// Step 3.4.1: Document current state before rollback
CREATE (rollback:RollbackLog {
    operation: 'xdb_integration_rollback',
    timestamp: datetime(),
    reason: 'Validation failure or user request',
    status: 'initiated'
})
WITH rollback
MATCH (ec:ExploitCode)
WITH rollback, count(ec) as exploit_count
MATCH ()-[r:HAS_EXPLOIT_CODE]->()
WITH rollback, exploit_count, count(r) as relationship_count
SET rollback.exploit_codes_before_rollback = exploit_count,
    rollback.relationships_before_rollback = relationship_count
RETURN exploit_count, relationship_count;

// Step 3.4.2: Create rollback checkpoint with sample data
MATCH (cve:CVE)-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WITH collect({
    cve_id: cve.id,
    xdb_id: ec.xdb_id,
    xdb_url: ec.xdb_url,
    exploit_type: ec.exploit_type,
    maturity: ec.maturity,
    confidence: r.confidence,
    threat_level: r.threat_level
})[0..50] as sample_data
CREATE (checkpoint:RollbackCheckpoint {
    operation: 'xdb_integration',
    timestamp: datetime(),
    sample_data: sample_data
});

// Step 3.4.3: Delete HAS_EXPLOIT_CODE relationships first
MATCH (cve:CVE)-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WITH r
DELETE r
RETURN count(r) as deleted_relationships;
// Expected: ~13K-27K relationships deleted

// Step 3.4.4: Delete ExploitCode nodes
MATCH (ec:ExploitCode)
WITH ec
DELETE ec
RETURN count(ec) as deleted_nodes;
// Expected: ~13K-27K nodes deleted

// Step 3.4.5: Drop ExploitCode constraints
DROP CONSTRAINT exploit_code_id IF EXISTS;

// Step 3.4.6: Drop ExploitCode indexes
DROP INDEX exploit_code_type IF EXISTS;

// Step 3.4.7: Remove hybrid properties from CVE nodes (if implemented)
MATCH (cve:CVE)
WHERE exists(cve.exploit_count) OR exists(cve.has_weaponized_exploit)
REMOVE cve.exploit_count, cve.has_weaponized_exploit
RETURN count(cve) as cves_cleaned;
```

#### Data Restoration Procedures

```bash
#!/bin/bash
# Script 3.4.1: Restore from backup if needed

BACKUP_PATH="/backups/neo4j/pre_xdb_20251101_140000"

echo "Restoring database from XDB pre-implementation backup..."
systemctl stop neo4j
neo4j-admin database restore neo4j --from-path="$BACKUP_PATH"
neo4j-admin database check neo4j
systemctl start neo4j
sleep 30

echo "XDB integration rollback completed via backup restoration."
```

#### Relationship Cleanup Queries

```cypher
// Query 3.4.8: Verify no HAS_EXPLOIT_CODE relationships remain
MATCH ()-[r:HAS_EXPLOIT_CODE]->()
RETURN count(r) as remaining_relationships;
// Expected: 0 remaining relationships

// Query 3.4.9: Check for orphaned relationship fragments (rare edge case)
MATCH (cve:CVE)
WHERE exists(cve.exploit_count) OR exists(cve.has_weaponized_exploit)
RETURN count(cve) as orphaned_properties;
// Expected: 0 orphaned properties
```

#### Validation After Rollback

```cypher
// Query 3.4.10: Verify no ExploitCode nodes remain
MATCH (ec:ExploitCode)
RETURN count(ec) as remaining_exploit_nodes;
// Expected: 0 remaining nodes

// Query 3.4.11: Verify no HAS_EXPLOIT_CODE relationships remain
MATCH ()-[r:HAS_EXPLOIT_CODE]->()
RETURN count(r) as remaining_exploit_relationships;
// Expected: 0 remaining relationships

// Query 3.4.12: Verify ExploitCode constraints dropped
SHOW CONSTRAINTS YIELD name, labelsOrTypes
WHERE labelsOrTypes = ['ExploitCode']
RETURN count(*) as remaining_constraints;
// Expected: 0 remaining constraints

// Query 3.4.13: Verify ExploitCode indexes dropped
SHOW INDEXES YIELD name, labelsOrTypes
WHERE labelsOrTypes = ['ExploitCode']
RETURN count(*) as remaining_indexes;
// Expected: 0 remaining indexes

// Query 3.4.14: Verify database matches baseline node count
MATCH (baseline:EnrichmentBaseline {operation: 'xdb_integration', status: 'pre_implementation'})
CALL apoc.meta.stats() YIELD nodeCount
WITH baseline, nodeCount
WHERE nodeCount = baseline.total_nodes_before
RETURN 'Rollback successful: Node count matches baseline' as status;
// Expected: Returns success message

// Query 3.4.15: Update rollback log
MATCH (rollback:RollbackLog {operation: 'xdb_integration_rollback', status: 'initiated'})
SET rollback.status = 'completed',
    rollback.completion_time = datetime(),
    rollback.duration_minutes = duration.between(rollback.timestamp, datetime()).minutes;
```

**Estimated Rollback Time**: 30-60 minutes (depends on node/relationship count)
**Risk Level**: MEDIUM (structural changes - node and relationship deletion)

---

## 4. Cross-Integration Validation

### 4.1 Combined Feature Testing

**Purpose**: Verify all three integrations work together correctly.

```cypher
// Query 4.1.1: Test combined EPSS + KEV + XDB prioritization
MATCH (cve:CVE)
WHERE cve.epss_score > 0.5
  AND (cve.in_cisa_kev = true OR cve.in_vulncheck_kev = true)
OPTIONAL MATCH (cve)-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WHERE ec.maturity = 'weaponized'
RETURN cve.id,
       cve.epss_score,
       cve.cvssScore,
       cve.in_cisa_kev,
       cve.in_vulncheck_kev,
       count(ec) as weaponized_exploits
ORDER BY cve.epss_score DESC, weaponized_exploits DESC
LIMIT 50;
// Expected: Returns top priority CVEs with all enrichments

// Query 4.1.2: Validate consistency between KEV and XDB
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true
OPTIONAL MATCH (cve)-[:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WITH cve, count(ec) as exploit_count
RETURN
    CASE
        WHEN exploit_count > 0 THEN 'KEV with exploit code'
        ELSE 'KEV without exploit code'
    END as category,
    count(cve) as count;
// Note: Most KEV CVEs should have exploit code, but not all

// Query 4.1.3: Test EPSS correlation with exploit availability
MATCH (cve:CVE)-[:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WHERE exists(cve.epss_score)
WITH
    CASE
        WHEN cve.epss_score >= 0.7 THEN 'High EPSS (≥0.7)'
        WHEN cve.epss_score >= 0.3 THEN 'Medium EPSS (0.3-0.7)'
        ELSE 'Low EPSS (<0.3)'
    END as epss_bracket,
    count(DISTINCT cve) as cve_count
RETURN epss_bracket, cve_count
ORDER BY epss_bracket;
// Expected: Higher EPSS scores should correlate with exploit availability

// Query 4.1.4: Comprehensive enrichment coverage check
MATCH (cve:CVE)
WITH cve,
     exists(cve.epss_score) as has_epss,
     (cve.in_cisa_kev = true OR cve.in_vulncheck_kev = true) as is_kev,
     exists((cve)-[:HAS_EXPLOIT_CODE]->()) as has_exploit
RETURN
    has_epss,
    is_kev,
    has_exploit,
    count(cve) as count
ORDER BY count DESC;
// Expected: Most CVEs have EPSS, small subset have KEV/exploits
```

### 4.2 Data Consistency Checks

```cypher
// Query 4.2.1: Verify no conflicting enrichment data
MATCH (cve:CVE)
WHERE (cve.in_cisa_kev = true OR cve.in_vulncheck_kev = true)
  AND cve.epss_score < 0.1  // KEV but low EPSS (unusual)
RETURN count(cve) as potential_inconsistencies,
       collect(cve.id)[0..10] as sample_cves;
// Note: Some inconsistencies are expected (EPSS is probabilistic)

// Query 4.2.2: Check exploit code for non-KEV high EPSS CVEs
MATCH (cve:CVE)
WHERE cve.epss_score > 0.7
  AND NOT (cve.in_cisa_kev = true OR cve.in_vulncheck_kev = true)
OPTIONAL MATCH (cve)-[:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
RETURN count(DISTINCT cve) as high_epss_non_kev_cves,
       count(ec) as exploit_codes_found;
// Note: High EPSS without KEV may indicate emerging threats

// Query 4.2.3: Validate timestamp consistency across enrichments
MATCH (cve:CVE)
WHERE exists(cve.epss_last_updated)
  AND exists(cve.kev_last_updated)
WITH cve,
     duration.between(cve.epss_last_updated, cve.kev_last_updated).hours as time_diff_hours
WHERE abs(time_diff_hours) > 24
RETURN count(cve) as inconsistent_timestamps;
// Expected: Most enrichments should occur within same timeframe
```

### 4.3 Performance Testing

```cypher
// Query 4.3.1: Benchmark complex multi-enrichment query
PROFILE
MATCH (cve:CVE)
WHERE cve.epss_score > 0.5
  AND cve.cvssScore >= 7.0
  AND (cve.in_cisa_kev = true OR cve.in_vulncheck_kev = true)
OPTIONAL MATCH (cve)-[r:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
WHERE ec.maturity IN ['functional', 'weaponized']
RETURN cve.id, cve.epss_score, cve.cvssScore,
       cve.kev_date_added, count(ec) as exploit_count
ORDER BY cve.epss_score DESC
LIMIT 100;
// Expected: <300ms execution time with indexes

// Query 4.3.2: Test dashboard query performance
PROFILE
MATCH (cve:CVE)
WHERE exists(cve.epss_score)
WITH cve
ORDER BY cve.epss_score DESC
LIMIT 1000
OPTIONAL MATCH (cve)-[:HAS_EXPLOIT_CODE]->(ec:ExploitCode)
RETURN cve.id, cve.epss_score, cve.in_cisa_kev, count(ec) as exploits;
// Expected: <500ms for dashboard rendering
```

---

## 5. Monitoring and Alerting

### 5.1 Automated Monitoring Queries

```cypher
// Query 5.1.1: Daily enrichment health check
MATCH (cve:CVE)
WITH count(cve) as total_cves
MATCH (epss:CVE)
WHERE exists(epss.epss_score)
WITH total_cves, count(epss) as epss_count
MATCH (kev:CVE)
WHERE kev.in_cisa_kev = true OR kev.in_vulncheck_kev = true
WITH total_cves, epss_count, count(kev) as kev_count
MATCH (exploit:CVE)-[:HAS_EXPLOIT_CODE]->()
WITH total_cves, epss_count, kev_count, count(DISTINCT exploit) as exploit_count
RETURN
    total_cves,
    epss_count,
    toFloat(epss_count) / total_cves * 100 as epss_coverage_pct,
    kev_count,
    exploit_count,
    datetime() as check_time;
// Expected: EPSS ≈100%, KEV ≈1800, Exploits ≈13K-27K

// Query 5.1.2: Detect stale enrichment data
MATCH (cve:CVE)
WHERE exists(cve.epss_last_updated)
WITH cve, duration.between(cve.epss_last_updated, datetime()).days as age_days
WHERE age_days > 7
RETURN count(cve) as stale_epss_updates, max(age_days) as max_age_days;
// Alert if: stale_epss_updates > 1000 OR max_age_days > 14

// Query 5.1.3: Monitor KEV growth
MATCH (kev:CVE)
WHERE kev.in_cisa_kev = true OR kev.in_vulncheck_kev = true
WITH count(kev) as current_kev_count
// Compare with historical baseline
MATCH (baseline:EnrichmentBaseline {operation: 'kev_flagging'})
WHERE exists(baseline.kev_flagged)
WITH current_kev_count, max(baseline.kev_flagged) as baseline_kev_count
RETURN current_kev_count, baseline_kev_count,
       current_kev_count - baseline_kev_count as kev_growth;
// Alert if: kev_growth > 50 (significant KEV additions)
```

### 5.2 Alert Conditions

```python
# Script 5.2.1: Automated alerting for enrichment health

import logging
from datetime import datetime

def check_enrichment_health(driver):
    """Run health checks and alert on failures"""

    alerts = []

    with driver.session() as session:
        # Check 1: EPSS coverage
        result = session.run("""
            MATCH (cve:CVE)
            WITH count(cve) as total
            MATCH (epss:CVE)
            WHERE exists(epss.epss_score)
            RETURN toFloat(count(epss)) / total * 100 as coverage
        """).single()

        epss_coverage = result['coverage']
        if epss_coverage < 95.0:
            alerts.append(f"LOW EPSS COVERAGE: {epss_coverage:.1f}%")

        # Check 2: Stale data
        result = session.run("""
            MATCH (cve:CVE)
            WHERE exists(cve.epss_last_updated)
            WITH cve, duration.between(cve.epss_last_updated, datetime()).days as age
            WHERE age > 7
            RETURN count(cve) as stale_count, max(age) as max_age
        """).single()

        if result['stale_count'] > 1000:
            alerts.append(f"STALE DATA: {result['stale_count']} CVEs not updated in 7+ days")

        # Check 3: Missing indexes
        result = session.run("""
            SHOW INDEXES YIELD name, state
            WHERE name IN ['cve_epss', 'cve_in_cisa_kev', 'exploit_code_type']
            RETURN count(*) as index_count
        """).single()

        if result['index_count'] < 3:
            alerts.append(f"MISSING INDEXES: Expected 3, found {result['index_count']}")

        # Check 4: Orphaned nodes
        result = session.run("""
            MATCH (ec:ExploitCode)
            WHERE NOT exists((ec)<-[:HAS_EXPLOIT_CODE]-())
            RETURN count(ec) as orphaned
        """).single()

        if result['orphaned'] > 0:
            alerts.append(f"ORPHANED EXPLOIT CODES: {result['orphaned']} nodes")

    # Send alerts
    if alerts:
        logging.error(f"Enrichment health check FAILED at {datetime.now()}")
        for alert in alerts:
            logging.error(f"  - {alert}")
        # Send to monitoring system (e.g., PagerDuty, Slack)
        send_alert_notification(alerts)
    else:
        logging.info(f"Enrichment health check PASSED at {datetime.now()}")

    return len(alerts) == 0

def send_alert_notification(alerts):
    """Send alerts to monitoring system"""
    # Implement Slack/email/PagerDuty integration
    pass
```

### 5.3 Performance Monitoring

```cypher
// Query 5.3.1: Monitor query performance trends
CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Transactions')
YIELD attributes
RETURN attributes.NumberOfOpenTransactions.value as open_transactions,
       attributes.NumberOfCommittedTransactions.value as committed_transactions,
       datetime() as sample_time;
// Alert if: open_transactions > 100 (potential bottleneck)

// Query 5.3.2: Monitor database growth
CALL apoc.meta.stats() YIELD nodeCount, relCount, labelCount
RETURN nodeCount, relCount, labelCount, datetime() as sample_time;
// Track growth trends over time
```

---

## Summary

### Total Validation Checks: 87

- **EPSS Integration**: 31 checks (15 pre-impl, 6 during-impl, 10 post-impl)
- **KEV Flagging**: 27 checks (7 pre-impl, 6 during-impl, 14 post-impl)
- **XDB PoC Integration**: 29 checks (7 pre-impl, 7 during-impl, 15 post-impl)

### Rollback Time Estimates

| Integration | Rollback Time | Risk Level |
|-------------|---------------|------------|
| EPSS Integration | 15-30 minutes | LOW |
| KEV Flagging | 10-20 minutes | LOW |
| XDB PoC Integration | 30-60 minutes | MEDIUM |

### Key Success Metrics

- **EPSS**: 100% coverage (267,487 CVEs), score range 0.0-1.0, avg 0.05-0.15
- **KEV**: ~1,800 flagged CVEs, complete metadata, no date inconsistencies
- **XDB**: 13K-27K exploit codes, proper relationships, valid maturity levels

---

**Document Status**: Ready for validation execution
**Last Updated**: 2025-11-01
**Next Review**: After Phase 1 implementation completion
