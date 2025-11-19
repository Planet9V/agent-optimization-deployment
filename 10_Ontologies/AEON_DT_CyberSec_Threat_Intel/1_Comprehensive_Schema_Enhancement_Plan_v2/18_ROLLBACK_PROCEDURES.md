# Rollback Procedures
**File:** 18_ROLLBACK_PROCEDURES.md
**Created:** 2025-10-30 00:00:00 UTC
**Modified:** 2025-10-30 00:00:00 UTC
**Version:** v1.0.0
**Author:** AEON FORGE Implementation Team
**Purpose:** Comprehensive rollback procedures for safe schema enhancement wave reversal
**Status:** ACTIVE

## Executive Summary

This document provides detailed rollback procedures for safely reversing AEON Digital Twin schema enhancements at wave-level or individual component level. Each procedure includes detection triggers, decision criteria, execution steps, and validation protocols to ensure complete restoration to pre-wave state with zero data loss.

### Rollback Strategy Overview

**Three-Tier Rollback Approach:**
1. **Surgical Rollback**: Remove only new enhancements, preserve all original data (fastest, lowest risk)
2. **Incremental Restoration**: Restore specific components from differential backups (moderate speed, moderate risk)
3. **Full Database Restore**: Complete restoration from full backup (slowest, highest confidence)

**Rollback Decision Matrix:**
- **Surgical**: Validation failures in new data only, CVE count intact
- **Incremental**: Property corruption or partial relationship loss
- **Full Restore**: CVE node loss, database corruption, or multiple critical failures

## 1. Rollback Triggers and Detection

### 1.1 Automatic Rollback Triggers

**CRITICAL Triggers (Automatic Rollback Initiation):**

```cypher
// ===============================================
// TRIGGER 1: CVE Node Count Discrepancy
// ===============================================
// Run continuously during wave execution (every 5 minutes)
MATCH (c:CVE)
WITH count(c) AS current_cve_count
WHERE current_cve_count <> 147923
RETURN
  current_cve_count,
  147923 AS expected_count,
  'CRITICAL: CVE NODE LOSS DETECTED - INITIATING AUTOMATIC ROLLBACK' AS alert_message,
  datetime() AS trigger_time;
// Trigger Action: Halt wave execution, initiate full database restore

// ===============================================
// TRIGGER 2: Existing Relationship Deletion
// ===============================================
// Run after each major wave operation
MATCH (c:CVE)-[r]->()
WHERE type(r) IN [
  'HAS_WEAKNESS', 'AFFECTS', 'IMPACTS_VENDOR', 'EXPLOITED_BY',
  'ENABLES_TECHNIQUE', 'MITIGATED_BY', 'EXPLOITED_BY_ACTOR',
  'USED_IN_CAMPAIGN', 'RELATED_TO', 'FIXED_BY'
]
WITH type(r) AS rel_type, count(r) AS current_count
WITH rel_type, current_count,
  CASE rel_type
    WHEN 'HAS_WEAKNESS' THEN 128456
    WHEN 'AFFECTS' THEN 843291
    WHEN 'IMPACTS_VENDOR' THEN 287634
    WHEN 'EXPLOITED_BY' THEN 64219
    WHEN 'ENABLES_TECHNIQUE' THEN 89347
    WHEN 'MITIGATED_BY' THEN 112568
    WHEN 'EXPLOITED_BY_ACTOR' THEN 12847
    WHEN 'USED_IN_CAMPAIGN' THEN 8456
    WHEN 'RELATED_TO' THEN 45782
    WHEN 'FIXED_BY' THEN 98234
  END AS baseline_count
WHERE current_count < baseline_count
RETURN
  rel_type,
  current_count,
  baseline_count,
  (baseline_count - current_count) AS missing_relationships,
  'CRITICAL: RELATIONSHIP LOSS DETECTED - INITIATING AUTOMATIC ROLLBACK' AS alert_message,
  datetime() AS trigger_time;
// Trigger Action: Halt wave execution, initiate incremental restoration

// ===============================================
// TRIGGER 3: Property Nullification
// ===============================================
// Run after each property enhancement operation
MATCH (c:CVE)
WHERE c.id IS NULL OR c.description IS NULL OR c.cvss_score IS NULL
WITH count(c) AS nullified_count
WHERE nullified_count > 0
RETURN
  nullified_count,
  'CRITICAL: PROPERTY NULLIFICATION DETECTED - INITIATING AUTOMATIC ROLLBACK' AS alert_message,
  datetime() AS trigger_time;
// Trigger Action: Halt wave execution, initiate incremental restoration
```

**Automatic Rollback Script:**

```bash
#!/bin/bash
# File: /home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/scripts/automatic_rollback_trigger.sh

WAVE_NUMBER=$1
BACKUP_DIR="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/backups"
LOG_FILE="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/logs/rollback.log"

echo "=== AUTOMATIC ROLLBACK TRIGGER: Wave $WAVE_NUMBER ===" | tee -a "$LOG_FILE"
echo "Trigger Time: $(date)" | tee -a "$LOG_FILE"

# 1. Check CVE node count
CVE_COUNT=$(cypher-shell -u neo4j -p password \
  "MATCH (c:CVE) RETURN count(c) AS count" --format plain | tail -n 1)

if [ "$CVE_COUNT" -ne "147923" ]; then
  echo "CRITICAL: CVE count mismatch! Expected: 147923, Found: $CVE_COUNT" | tee -a "$LOG_FILE"
  echo "Initiating FULL DATABASE RESTORE..." | tee -a "$LOG_FILE"
  ./rollback_wave_full.sh $WAVE_NUMBER
  exit 1
fi

# 2. Check for property nullification
NULL_PROPERTIES=$(cypher-shell -u neo4j -p password \
  "MATCH (c:CVE) WHERE c.id IS NULL OR c.description IS NULL RETURN count(c)" \
  --format plain | tail -n 1)

if [ "$NULL_PROPERTIES" -ne "0" ]; then
  echo "CRITICAL: Property nullification detected! Count: $NULL_PROPERTIES" | tee -a "$LOG_FILE"
  echo "Initiating INCREMENTAL RESTORATION..." | tee -a "$LOG_FILE"
  ./rollback_wave_incremental.sh $WAVE_NUMBER
  exit 1
fi

echo "✓ No critical triggers detected" | tee -a "$LOG_FILE"
```

### 1.2 Manual Rollback Triggers

**High-Priority Triggers (Manual Decision Required):**

- **Performance Degradation**: Query response times > 200% of baseline
- **Semantic Inconsistencies**: Validation failures in domain logic
- **Integration Failures**: Cross-domain relationship errors
- **User-Reported Issues**: Critical functionality broken

**Rollback Decision Flowchart:**

```
Validation Failure Detected
  ├─ CVE Node Loss? ─ YES ─> FULL RESTORE (Automatic)
  ├─ Property Nullification? ─ YES ─> INCREMENTAL RESTORE (Automatic)
  ├─ Relationship Loss? ─ YES ─> INCREMENTAL RESTORE (Automatic)
  ├─ Performance > 200% Baseline? ─ YES ─> Manual Review ─> SURGICAL or FULL
  ├─ Semantic Errors? ─ YES ─> Manual Review ─> SURGICAL or No Action
  └─ Other Issues? ─ YES ─> Manual Review ─> Context-Dependent
```

## 2. Surgical Rollback Procedures

### 2.1 Wave-Specific Surgical Rollback

**Use Case:** Remove only new enhancements added during specific wave, preserve all original data.

**Wave 1: SAREF IoT Integration Rollback**

```cypher
// ===============================================
// SURGICAL ROLLBACK: Wave 1 (SAREF)
// ===============================================

// Step 1: Log rollback initiation
CREATE (rollback:RollbackEvent {
  wave: 1,
  wave_name: 'SAREF IoT Integration',
  rollback_type: 'surgical',
  initiated_by: 'validation_failure',
  timestamp: datetime(),
  status: 'in_progress'
});

// Step 2: Remove SAREF relationships from CVEs
MATCH (c:CVE)-[r:AFFECTS_SAREF_DEVICE]->()
WITH count(r) AS saref_device_rels
DELETE r
RETURN saref_device_rels AS deleted_saref_device_relationships;

MATCH (c:CVE)-[r:IMPACTS_SAREF_FUNCTION]->()
WITH count(r) AS saref_function_rels
DELETE r
RETURN saref_function_rels AS deleted_saref_function_relationships;

MATCH (c:CVE)-[r:CORRUPTS_MEASUREMENT]->()
WITH count(r) AS measurement_rels
DELETE r
RETURN measurement_rels AS deleted_measurement_relationships;

// Step 3: Remove SAREF-specific properties from CVE nodes
MATCH (c:CVE)
WHERE c.saref_device_types IS NOT NULL
  OR c.saref_function_impact IS NOT NULL
  OR c.saref_measurement_risk IS NOT NULL
  OR c.iot_exploitation_vector IS NOT NULL
  OR c.saref_severity_modifier IS NOT NULL
WITH count(c) AS cves_to_update
SET
  c.saref_device_types = null,
  c.saref_function_impact = null,
  c.saref_measurement_risk = null,
  c.iot_exploitation_vector = null,
  c.saref_severity_modifier = null
RETURN cves_to_update AS cves_cleaned;

// Step 4: Drop SAREF-specific indexes
DROP INDEX cve_saref_device_types_index IF EXISTS;
DROP INDEX cve_iot_exploitation_vector_index IF EXISTS;

// Step 5: Update rollback event status
MATCH (rollback:RollbackEvent)
WHERE rollback.wave = 1 AND rollback.status = 'in_progress'
SET rollback.status = 'completed',
    rollback.completion_time = datetime();

// Step 6: Verification
MATCH (c:CVE)
RETURN
  count(c) AS total_cves,
  count(c.saref_device_types) AS cves_with_saref_props,
  CASE
    WHEN count(c) = 147923 AND count(c.saref_device_types) = 0 THEN 'SUCCESS'
    ELSE 'VERIFICATION FAILED'
  END AS rollback_verification;
// Expected: total_cves = 147923, cves_with_saref_props = 0, verification = 'SUCCESS'
```

**Wave 2: ICS/OT Integration Rollback**

```cypher
// ===============================================
// SURGICAL ROLLBACK: Wave 2 (ICS)
// ===============================================

// Step 1: Log rollback initiation
CREATE (rollback:RollbackEvent {
  wave: 2,
  wave_name: 'ICS/OT Integration',
  rollback_type: 'surgical',
  timestamp: datetime(),
  status: 'in_progress'
});

// Step 2: Remove ICS relationships
MATCH (c:CVE)-[r:AFFECTS_ICS_COMPONENT]->()
DELETE r;

MATCH (c:CVE)-[r:EXPLOITS_PROTOCOL]->()
DELETE r;

MATCH (c:CVE)-[r:ENABLES_ICS_TECHNIQUE]->()
DELETE r;

// Step 3: Remove ICS-specific properties from CVE nodes
MATCH (c:CVE)
WHERE c.ics_applicable IS NOT NULL
SET
  c.ics_applicable = null,
  c.ics_component_types = null,
  c.purdue_levels = null,
  c.safety_impact = null,
  c.process_impact = null,
  c.ics_mitre_techniques = null,
  c.industrial_protocols = null;

// Step 4: Drop ICS-specific indexes
DROP INDEX cve_ics_applicable_index IF EXISTS;
DROP INDEX cve_safety_impact_index IF EXISTS;
DROP INDEX cve_purdue_levels_index IF EXISTS;
DROP INDEX cve_ics_severity_composite IF EXISTS;

// Step 5: Update rollback event status
MATCH (rollback:RollbackEvent)
WHERE rollback.wave = 2 AND rollback.status = 'in_progress'
SET rollback.status = 'completed',
    rollback.completion_time = datetime();

// Step 6: Verification
MATCH (c:CVE)
RETURN
  count(c) AS total_cves,
  count(c.ics_applicable) AS cves_with_ics_props,
  CASE
    WHEN count(c) = 147923 AND count(c.ics_applicable) = 0 THEN 'SUCCESS'
    ELSE 'VERIFICATION FAILED'
  END AS rollback_verification;
```

**Wave 3: SBOM Integration Rollback**

```cypher
// ===============================================
// SURGICAL ROLLBACK: Wave 3 (SBOM)
// ===============================================

// Step 1: Log rollback initiation
CREATE (rollback:RollbackEvent {
  wave: 3,
  wave_name: 'SBOM Integration',
  rollback_type: 'surgical',
  timestamp: datetime(),
  status: 'in_progress'
});

// Step 2: Remove SBOM relationships
MATCH (c:CVE)-[r:AFFECTS_SBOM_COMPONENT]->()
DELETE r;

MATCH (c:CVE)-[r:IMPACTS_PACKAGE]->()
DELETE r;

MATCH (c:CVE)-[r:PROPAGATES_THROUGH]->()
DELETE r;

// Step 3: Remove SBOM-specific properties
MATCH (c:CVE)
WHERE c.sbom_component_count IS NOT NULL
SET
  c.sbom_component_count = null,
  c.package_ecosystems = null,
  c.dependency_depth = null,
  c.license_implications = null,
  c.supply_chain_risk = null,
  c.purl_identifiers = null;

// Step 4: Drop SBOM-specific indexes
DROP INDEX cve_package_ecosystems_index IF EXISTS;
DROP INDEX cve_supply_chain_risk_index IF EXISTS;
DROP INDEX cve_sbom_risk_composite IF EXISTS;

// Step 5: Update rollback event status
MATCH (rollback:RollbackEvent)
WHERE rollback.wave = 3 AND rollback.status = 'in_progress'
SET rollback.status = 'completed',
    rollback.completion_time = datetime();

// Step 6: Verification
MATCH (c:CVE)
RETURN
  count(c) AS total_cves,
  count(c.sbom_component_count) AS cves_with_sbom_props,
  CASE
    WHEN count(c) = 147923 AND count(c.sbom_component_count) = 0 THEN 'SUCCESS'
    ELSE 'VERIFICATION FAILED'
  END AS rollback_verification;
```

**Wave 4: UCO Integration Rollback**

```cypher
// ===============================================
// SURGICAL ROLLBACK: Wave 4 (UCO)
// ===============================================

// Step 1: Log rollback initiation
CREATE (rollback:RollbackEvent {
  wave: 4,
  wave_name: 'UCO Integration',
  rollback_type: 'surgical',
  timestamp: datetime(),
  status: 'in_progress'
});

// Step 2: Remove UCO relationships
MATCH (c:CVE)-[r:CREATES_OBSERVABLE]->()
DELETE r;

MATCH (c:CVE)-[r:TRIGGERS_ACTION]->()
DELETE r;

// Step 3: Remove UCO-specific properties
MATCH (c:CVE)
WHERE c.uco_observable_types IS NOT NULL
SET
  c.uco_observable_types = null,
  c.forensic_artifacts = null,
  c.exploitation_signatures = null,
  c.investigation_priority = null;

// Step 4: Drop UCO-specific indexes
DROP INDEX cve_uco_observable_types_index IF EXISTS;
DROP INDEX cve_investigation_priority_index IF EXISTS;

// Step 5: Update rollback event status
MATCH (rollback:RollbackEvent)
WHERE rollback.wave = 4 AND rollback.status = 'in_progress'
SET rollback.status = 'completed',
    rollback.completion_time = datetime();

// Step 6: Verification
MATCH (c:CVE)
RETURN
  count(c) AS total_cves,
  count(c.uco_observable_types) AS cves_with_uco_props,
  CASE
    WHEN count(c) = 147923 AND count(c.uco_observable_types) = 0 THEN 'SUCCESS'
    ELSE 'VERIFICATION FAILED'
  END AS rollback_verification;
```

**Wave 5: Threat Intelligence Integration Rollback**

```cypher
// ===============================================
// SURGICAL ROLLBACK: Wave 5 (Threat Intelligence)
// ===============================================

// Step 1: Log rollback initiation
CREATE (rollback:RollbackEvent {
  wave: 5,
  wave_name: 'Threat Intelligence Integration',
  rollback_type: 'surgical',
  timestamp: datetime(),
  status: 'in_progress'
});

// Step 2: Remove Threat Intelligence relationships
MATCH (c:CVE)-[r:HAS_STIX_INDICATOR]->()
DELETE r;

MATCH (ta:ThreatActor)-[r:TARGETS_ICS_COMPONENT]->()
DELETE r;

MATCH (ta:ThreatActor)-[r:USES_ICS_TECHNIQUE]->()
DELETE r;

MATCH (ta:ThreatActor)-[r:ASSOCIATED_WITH_STIX]->()
DELETE r;

// Step 3: Remove enhanced ThreatActor properties
MATCH (ta:ThreatActor)
WHERE ta.psychometric_profile IS NOT NULL
SET
  ta.psychometric_profile = null,
  ta.risk_tolerance = null,
  ta.operational_tempo = null,
  ta.target_selection = null,
  ta.technical_capability = null,
  ta.ttp_diversity_score = null,
  ta.ics_focused = null,
  ta.ics_target_count = null,
  ta.ics_threat_level = null;

// Step 4: Remove Threat Intelligence properties from CVEs
MATCH (c:CVE)
WHERE c.threat_actor_associations IS NOT NULL
SET
  c.threat_actor_associations = null,
  c.campaign_usage_count = null,
  c.exploit_kit_usage = null,
  c.dark_web_mentions = null,
  c.weaponization_timeline = null,
  c.stix_indicator_count = null,
  c.threat_intel_confidence = null;

// Step 5: Drop Threat Intelligence indexes
DROP INDEX cve_threat_actor_associations_index IF EXISTS;
DROP INDEX cve_weaponization_timeline_index IF EXISTS;

// Step 6: Update rollback event status
MATCH (rollback:RollbackEvent)
WHERE rollback.wave = 5 AND rollback.status = 'in_progress'
SET rollback.status = 'completed',
    rollback.completion_time = datetime();

// Step 7: Verification
MATCH (c:CVE)
WITH count(c) AS total_cves,
     count(c.threat_actor_associations) AS cves_with_ti_props
MATCH (ta:ThreatActor)
RETURN
  total_cves,
  cves_with_ti_props,
  count(ta.psychometric_profile) AS tas_with_profiles,
  CASE
    WHEN total_cves = 147923
      AND cves_with_ti_props = 0
      AND count(ta.psychometric_profile) = 0
    THEN 'SUCCESS'
    ELSE 'VERIFICATION FAILED'
  END AS rollback_verification;
```

### 2.2 Surgical Rollback Automation Script

```bash
#!/bin/bash
# File: /home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/scripts/surgical_rollback.sh

WAVE_NUMBER=$1
LOG_FILE="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/logs/surgical_rollback_wave_${WAVE_NUMBER}.log"

echo "=== SURGICAL ROLLBACK: Wave $WAVE_NUMBER ===" | tee -a "$LOG_FILE"
echo "Start Time: $(date)" | tee -a "$LOG_FILE"

# Load wave-specific Cypher rollback script
ROLLBACK_SCRIPT="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/cypher/rollback_wave_${WAVE_NUMBER}.cypher"

if [ ! -f "$ROLLBACK_SCRIPT" ]; then
  echo "ERROR: Rollback script not found: $ROLLBACK_SCRIPT" | tee -a "$LOG_FILE"
  exit 1
fi

# Execute surgical rollback
echo "Executing surgical rollback for Wave $WAVE_NUMBER..." | tee -a "$LOG_FILE"
cypher-shell -u neo4j -p password < "$ROLLBACK_SCRIPT" 2>&1 | tee -a "$LOG_FILE"

# Verify CVE count
CVE_COUNT=$(cypher-shell -u neo4j -p password \
  "MATCH (c:CVE) RETURN count(c)" --format plain | tail -n 1)

echo "Post-Rollback CVE Count: $CVE_COUNT" | tee -a "$LOG_FILE"

if [ "$CVE_COUNT" -eq "147923" ]; then
  echo "✓ SUCCESS: CVE count verified (147,923)" | tee -a "$LOG_FILE"
else
  echo "✗ FAILURE: CVE count mismatch! Expected: 147923, Found: $CVE_COUNT" | tee -a "$LOG_FILE"
  exit 1
fi

# Verify relationship preservation
echo "Verifying existing relationship preservation..." | tee -a "$LOG_FILE"
cypher-shell -u neo4j -p password <<CYPHER | tee -a "$LOG_FILE"
MATCH (c:CVE)-[r]->()
WHERE type(r) IN [
  'HAS_WEAKNESS', 'AFFECTS', 'IMPACTS_VENDOR', 'EXPLOITED_BY',
  'ENABLES_TECHNIQUE', 'MITIGATED_BY', 'EXPLOITED_BY_ACTOR',
  'USED_IN_CAMPAIGN', 'RELATED_TO', 'FIXED_BY'
]
RETURN
  type(r) AS relationship_type,
  count(r) AS current_count
ORDER BY relationship_type;
CYPHER

echo "=== Surgical Rollback Complete ===" | tee -a "$LOG_FILE"
echo "End Time: $(date)" | tee -a "$LOG_FILE"
```

## 3. Incremental Restoration Procedures

### 3.1 Property-Level Restoration

**Use Case:** Restore corrupted or nullified CVE properties from differential backups.

```bash
#!/bin/bash
# File: /home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/scripts/restore_cve_properties.sh

WAVE_NUMBER=$1
BACKUP_DIR="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/backups/wave_${WAVE_NUMBER}"
LOG_FILE="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/logs/property_restoration_wave_${WAVE_NUMBER}.log"

echo "=== CVE PROPERTY RESTORATION: Wave $WAVE_NUMBER ===" | tee -a "$LOG_FILE"
echo "Start Time: $(date)" | tee -a "$LOG_FILE"

# 1. Identify corrupted CVEs
echo "Identifying corrupted CVE properties..." | tee -a "$LOG_FILE"
CORRUPTED_CVES=$(cypher-shell -u neo4j -p password <<CYPHER
MATCH (c:CVE)
WHERE c.id IS NULL OR c.description IS NULL OR c.cvss_score IS NULL
RETURN collect(id(c)) AS corrupted_ids;
CYPHER
)

if [ "$CORRUPTED_CVES" == "[]" ]; then
  echo "✓ No corrupted CVE properties detected" | tee -a "$LOG_FILE"
  exit 0
fi

# 2. Load backup CVE data
BACKUP_FILE="$BACKUP_DIR/cve_nodes_*.json"
echo "Loading backup CVE data from: $BACKUP_FILE" | tee -a "$LOG_FILE"

# 3. Restore properties for corrupted CVEs
cypher-shell -u neo4j -p password <<CYPHER | tee -a "$LOG_FILE"
CALL apoc.load.json('file:///$BACKUP_FILE') YIELD value
WITH value
WHERE value.id IN $CORRUPTED_CVES
MATCH (c:CVE)
WHERE id(c) IN $CORRUPTED_CVES AND c.id = value.id
SET c = value.properties
RETURN count(c) AS restored_cves;
CYPHER

# 4. Verification
echo "Verifying property restoration..." | tee -a "$LOG_FILE"
NULL_COUNT=$(cypher-shell -u neo4j -p password \
  "MATCH (c:CVE) WHERE c.id IS NULL OR c.description IS NULL RETURN count(c)" \
  --format plain | tail -n 1)

if [ "$NULL_COUNT" -eq "0" ]; then
  echo "✓ SUCCESS: All CVE properties restored" | tee -a "$LOG_FILE"
else
  echo "✗ FAILURE: $NULL_COUNT CVEs still have null properties" | tee -a "$LOG_FILE"
  exit 1
fi

echo "=== Property Restoration Complete ===" | tee -a "$LOG_FILE"
echo "End Time: $(date)" | tee -a "$LOG_FILE"
```

### 3.2 Relationship-Level Restoration

**Use Case:** Restore deleted or corrupted CVE relationships from differential backups.

```bash
#!/bin/bash
# File: /home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/scripts/restore_cve_relationships.sh

WAVE_NUMBER=$1
BACKUP_DIR="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/backups/wave_${WAVE_NUMBER}"
LOG_FILE="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/logs/relationship_restoration_wave_${WAVE_NUMBER}.log"

echo "=== CVE RELATIONSHIP RESTORATION: Wave $WAVE_NUMBER ===" | tee -a "$LOG_FILE"
echo "Start Time: $(date)" | tee -a "$LOG_FILE"

# 1. Identify missing relationships
echo "Checking for missing relationships..." | tee -a "$LOG_FILE"
cypher-shell -u neo4j -p password <<CYPHER | tee -a "$LOG_FILE"
MATCH (c:CVE)-[r]->()
WHERE type(r) IN [
  'HAS_WEAKNESS', 'AFFECTS', 'IMPACTS_VENDOR', 'EXPLOITED_BY',
  'ENABLES_TECHNIQUE', 'MITIGATED_BY', 'EXPLOITED_BY_ACTOR',
  'USED_IN_CAMPAIGN', 'RELATED_TO', 'FIXED_BY'
]
WITH type(r) AS rel_type, count(r) AS current_count
WITH rel_type, current_count,
  CASE rel_type
    WHEN 'HAS_WEAKNESS' THEN 128456
    WHEN 'AFFECTS' THEN 843291
    WHEN 'IMPACTS_VENDOR' THEN 287634
    WHEN 'EXPLOITED_BY' THEN 64219
    WHEN 'ENABLES_TECHNIQUE' THEN 89347
    WHEN 'MITIGATED_BY' THEN 112568
    WHEN 'EXPLOITED_BY_ACTOR' THEN 12847
    WHEN 'USED_IN_CAMPAIGN' THEN 8456
    WHEN 'RELATED_TO' THEN 45782
    WHEN 'FIXED_BY' THEN 98234
  END AS baseline_count
WHERE current_count < baseline_count
RETURN
  rel_type,
  baseline_count - current_count AS missing_count;
CYPHER

# 2. Load backup relationship data
BACKUP_FILE="$BACKUP_DIR/cve_relationships_*.json"
echo "Loading backup relationship data from: $BACKUP_FILE" | tee -a "$LOG_FILE"

# 3. Restore missing relationships
cypher-shell -u neo4j -p password <<CYPHER | tee -a "$LOG_FILE"
CALL apoc.load.json('file:///$BACKUP_FILE') YIELD value
MATCH (c:CVE {id: value.source_id})
MATCH (target) WHERE id(target) = value.target_id
MERGE (c)-[r:\`\${value.rel_type}\`]->(target)
SET r = value.rel_properties
RETURN count(r) AS restored_relationships;
CYPHER

# 4. Verification
echo "Verifying relationship restoration..." | tee -a "$LOG_FILE"
cypher-shell -u neo4j -p password <<CYPHER | tee -a "$LOG_FILE"
MATCH (c:CVE)-[r]->()
WHERE type(r) IN [
  'HAS_WEAKNESS', 'AFFECTS', 'IMPACTS_VENDOR', 'EXPLOITED_BY',
  'ENABLES_TECHNIQUE', 'MITIGATED_BY', 'EXPLOITED_BY_ACTOR',
  'USED_IN_CAMPAIGN', 'RELATED_TO', 'FIXED_BY'
]
RETURN
  type(r) AS relationship_type,
  count(r) AS current_count,
  CASE
    WHEN count(r) >= CASE type(r)
      WHEN 'HAS_WEAKNESS' THEN 128456
      WHEN 'AFFECTS' THEN 843291
      WHEN 'IMPACTS_VENDOR' THEN 287634
      WHEN 'EXPLOITED_BY' THEN 64219
      WHEN 'ENABLES_TECHNIQUE' THEN 89347
      WHEN 'MITIGATED_BY' THEN 112568
      WHEN 'EXPLOITED_BY_ACTOR' THEN 12847
      WHEN 'USED_IN_CAMPAIGN' THEN 8456
      WHEN 'RELATED_TO' THEN 45782
      WHEN 'FIXED_BY' THEN 98234
    END THEN 'PASS'
    ELSE 'FAIL'
  END AS validation_status
ORDER BY relationship_type;
CYPHER

echo "=== Relationship Restoration Complete ===" | tee -a "$LOG_FILE"
echo "End Time: $(date)" | tee -a "$LOG_FILE"
```

## 4. Full Database Restore Procedures

### 4.1 Complete Database Restoration

**Use Case:** Catastrophic failure requiring complete database restoration from full backup.

```bash
#!/bin/bash
# File: /home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/scripts/full_database_restore.sh

WAVE_NUMBER=$1
BACKUP_DIR="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/backups/wave_${WAVE_NUMBER}"
MANIFEST="$BACKUP_DIR/backup_manifest_*.json"
LOG_FILE="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/logs/full_restore_wave_${WAVE_NUMBER}.log"

echo "=== FULL DATABASE RESTORE: Wave $WAVE_NUMBER ===" | tee -a "$LOG_FILE"
echo "WARNING: This will completely restore database to pre-wave state" | tee -a "$LOG_FILE"
echo "Start Time: $(date)" | tee -a "$LOG_FILE"

# 1. Confirm restoration
read -p "Are you sure you want to perform FULL DATABASE RESTORE? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
  echo "Restoration cancelled by user" | tee -a "$LOG_FILE"
  exit 0
fi

# 2. Stop Neo4j database
echo "Stopping Neo4j database..." | tee -a "$LOG_FILE"
neo4j stop

# Wait for clean shutdown
sleep 10

# 3. Identify backup path from manifest
if [ ! -f "$MANIFEST" ]; then
  echo "ERROR: Backup manifest not found: $MANIFEST" | tee -a "$LOG_FILE"
  exit 1
fi

BACKUP_PATH=$(jq -r '.files.full_database' "$MANIFEST")
FULL_BACKUP_PATH="$BACKUP_DIR/$BACKUP_PATH"

if [ ! -d "$FULL_BACKUP_PATH" ]; then
  echo "ERROR: Backup not found: $FULL_BACKUP_PATH" | tee -a "$LOG_FILE"
  exit 1
fi

echo "Restoring from: $FULL_BACKUP_PATH" | tee -a "$LOG_FILE"

# 4. Perform database restore
neo4j-admin database restore \
  --from-path="$FULL_BACKUP_PATH" \
  --database=aeon-cyber-threat \
  --overwrite-destination=true \
  2>&1 | tee -a "$LOG_FILE"

if [ $? -ne 0 ]; then
  echo "ERROR: Database restore failed!" | tee -a "$LOG_FILE"
  exit 1
fi

# 5. Start Neo4j database
echo "Starting Neo4j database..." | tee -a "$LOG_FILE"
neo4j start

# Wait for database to be ready
sleep 30

# 6. Verify restoration
echo "Verifying database restoration..." | tee -a "$LOG_FILE"

CVE_COUNT=$(cypher-shell -u neo4j -p password \
  "MATCH (c:CVE) RETURN count(c)" --format plain | tail -n 1)

EXPECTED_COUNT=$(jq -r '.baseline_cve_count' "$MANIFEST")

echo "CVE Count: $CVE_COUNT (Expected: $EXPECTED_COUNT)" | tee -a "$LOG_FILE"

if [ "$CVE_COUNT" -ne "$EXPECTED_COUNT" ]; then
  echo "ERROR: Restoration verification failed! CVE count mismatch" | tee -a "$LOG_FILE"
  exit 1
fi

# 7. Verify property completeness
cypher-shell -u neo4j -p password <<CYPHER | tee -a "$LOG_FILE"
MATCH (c:CVE)
RETURN
  count(c) AS total_cves,
  count(c.id) AS id_count,
  count(c.description) AS description_count,
  count(c.cvss_score) AS cvss_count,
  CASE
    WHEN count(c.id) = count(c) AND count(c.cvss_score) >= 142847
    THEN 'SUCCESS'
    ELSE 'VERIFICATION FAILED'
  END AS validation_status;
CYPHER

# 8. Verify relationship counts
cypher-shell -u neo4j -p password <<CYPHER | tee -a "$LOG_FILE"
MATCH (c:CVE)-[r]->()
WHERE type(r) IN [
  'HAS_WEAKNESS', 'AFFECTS', 'IMPACTS_VENDOR', 'EXPLOITED_BY',
  'ENABLES_TECHNIQUE', 'MITIGATED_BY', 'EXPLOITED_BY_ACTOR',
  'USED_IN_CAMPAIGN', 'RELATED_TO', 'FIXED_BY'
]
RETURN
  type(r) AS relationship_type,
  count(r) AS current_count
ORDER BY relationship_type;
CYPHER

echo "✓ FULL DATABASE RESTORE COMPLETE" | tee -a "$LOG_FILE"
echo "Database restored to pre-Wave $WAVE_NUMBER state" | tee -a "$LOG_FILE"
echo "End Time: $(date)" | tee -a "$LOG_FILE"
```

## 5. Post-Rollback Validation

### 5.1 Comprehensive Post-Rollback Validation

```cypher
// ===============================================
// POST-ROLLBACK VALIDATION SUITE
// ===============================================

// Validation 1: CVE Node Count
MATCH (c:CVE)
WITH count(c) AS cve_count
RETURN
  cve_count,
  147923 AS expected_count,
  CASE WHEN cve_count = 147923 THEN 'PASS' ELSE 'FAIL' END AS status;

// Validation 2: Core Property Integrity
MATCH (c:CVE)
RETURN
  count(c.id) / count(c) * 100.0 AS id_completeness,
  count(c.description) / count(c) * 100.0 AS description_completeness,
  count(c.cvss_score) / count(c) * 100.0 AS cvss_completeness,
  CASE
    WHEN count(c.id) = count(c) AND count(c.cvss_score) >= 142847
    THEN 'PASS'
    ELSE 'FAIL'
  END AS status;

// Validation 3: Relationship Preservation
MATCH (c:CVE)-[r]->()
WHERE type(r) IN ['HAS_WEAKNESS', 'AFFECTS', 'IMPACTS_VENDOR']
RETURN
  type(r) AS rel_type,
  count(r) AS count,
  CASE
    WHEN type(r) = 'HAS_WEAKNESS' AND count(r) >= 128456 THEN 'PASS'
    WHEN type(r) = 'AFFECTS' AND count(r) >= 843291 THEN 'PASS'
    WHEN type(r) = 'IMPACTS_VENDOR' AND count(r) >= 287634 THEN 'PASS'
    ELSE 'FAIL'
  END AS status;

// Validation 4: Enhanced Properties Removed
MATCH (c:CVE)
RETURN
  count(c.saref_device_types) AS saref_props,
  count(c.ics_applicable) AS ics_props,
  count(c.sbom_component_count) AS sbom_props,
  count(c.uco_observable_types) AS uco_props,
  count(c.threat_actor_associations) AS ti_props,
  CASE
    WHEN count(c.saref_device_types) = 0
      AND count(c.ics_applicable) = 0
      AND count(c.sbom_component_count) = 0
      AND count(c.uco_observable_types) = 0
      AND count(c.threat_actor_associations) = 0
    THEN 'PASS: All Enhanced Properties Removed'
    ELSE 'WARN: Some Enhanced Properties Remain'
  END AS status;

// Validation 5: Query Performance Check
// Run baseline queries and verify performance
PROFILE MATCH (c:CVE {id: 'CVE-2023-12345'}) RETURN c;
// Expected: < 10ms execution time
```

## 6. Rollback Documentation and Reporting

### 6.1 Rollback Report Template

```markdown
# Rollback Report: Wave [N]

**Date:** [YYYY-MM-DD HH:MM:SS]
**Wave:** [N] - [Wave Name]
**Rollback Type:** [Surgical / Incremental / Full]
**Initiated By:** [Automatic Trigger / Manual Decision / User Request]
**Duration:** [HH:MM:SS]

## 1. Rollback Trigger
**Trigger Type:** [CVE Loss / Property Corruption / Relationship Loss / Performance / Other]
**Detection Time:** [YYYY-MM-DD HH:MM:SS]
**Severity:** [CRITICAL / HIGH / MEDIUM]
**Description:** [Detailed description of failure that triggered rollback]

## 2. Rollback Execution
**Start Time:** [YYYY-MM-DD HH:MM:SS]
**End Time:** [YYYY-MM-DD HH:MM:SS]
**Backup Used:** [Path to backup]
**Operations Performed:**
- [List of rollback operations]

## 3. Verification Results
**CVE Node Count:** [PASS/FAIL] (147,923 expected, [ACTUAL] found)
**Property Integrity:** [PASS/FAIL]
**Relationship Preservation:** [PASS/FAIL]
**Query Performance:** [PASS/FAIL]

## 4. Data Recovery
**CVE Nodes Recovered:** [count]
**Properties Restored:** [count]
**Relationships Restored:** [count]
**Data Loss:** [NONE / description]

## 5. Root Cause Analysis
**Primary Cause:** [Description]
**Contributing Factors:** [List]
**Preventable:** [YES / NO]

## 6. Recommendations
**Immediate Actions:** [List]
**Process Improvements:** [List]
**Prevention Measures:** [List]

## 7. Approval
**Rollback Verified By:** [Name]
**Verification Date:** [YYYY-MM-DD]
**Database Status:** [RESTORED / PARTIALLY RESTORED / FAILED]
**Approved for Retry:** [YES / NO / CONDITIONAL]

---
**Log File:** [Path to detailed log]
**Backup Location:** [Path to backup used]
```

---

**Document Version:** v1.0.0
**Last Updated:** 2025-10-30
**Next Review:** After Each Rollback Event
**Owner:** AEON FORGE Implementation Team
