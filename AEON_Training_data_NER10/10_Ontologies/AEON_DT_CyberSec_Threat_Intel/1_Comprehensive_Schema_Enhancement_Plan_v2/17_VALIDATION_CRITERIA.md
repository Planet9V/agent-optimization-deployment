# Validation Criteria
**File:** 17_VALIDATION_CRITERIA.md
**Created:** 2025-10-30 00:00:00 UTC
**Modified:** 2025-10-30 00:00:00 UTC
**Version:** v1.0.0
**Author:** AEON FORGE Implementation Team
**Purpose:** Comprehensive validation test suites and acceptance criteria for schema enhancement
**Status:** ACTIVE

## Executive Summary

This document defines comprehensive validation criteria, test suites, and acceptance standards for the AEON Digital Twin Cybersecurity Threat Intelligence schema enhancement. Validation covers data integrity, relationship correctness, query performance, semantic consistency, and cross-domain integration quality across all five enhancement waves.

### Validation Architecture

**Multi-Layer Validation Approach:**
1. **Structural Validation**: Schema structure, node/relationship existence, property types
2. **Data Integrity Validation**: Node counts, property completeness, relationship cardinality
3. **Semantic Validation**: Relationship correctness, property value validity, domain logic
4. **Performance Validation**: Query response times, index effectiveness, scalability
5. **Integration Validation**: Cross-domain consistency, chain completeness, attribution accuracy

## 1. Structural Validation Criteria

### 1.1 Schema Structure Validation

**Objective:** Verify all expected node labels, relationship types, and property schemas exist.

**Validation Query Suite:**

```cypher
// ===============================================
// VALIDATION 1.1.1: Node Label Existence
// ===============================================
CALL db.labels() YIELD label
WITH collect(label) AS existing_labels
WITH existing_labels,
  ['CVE', 'CWE', 'CAPEC', 'ThreatActor', 'Campaign', 'AttackTechnique',
   'ICSAttackTechnique', 'Mitigation', 'Product', 'Vendor',
   'SAREFDevice', 'SAREFFunction', 'SAREFMeasurement',
   'ICSComponent', 'IndustrialProtocol',
   'SBOMComponent', 'SoftwarePackage', 'DependencyChain',
   'UCOObservable', 'UCOAction',
   'STIXIndicator'] AS required_labels
WITH existing_labels, required_labels,
  [label IN required_labels WHERE NOT label IN existing_labels] AS missing_labels
RETURN
  required_labels,
  existing_labels,
  missing_labels,
  CASE
    WHEN size(missing_labels) = 0 THEN 'PASS'
    ELSE 'FAIL: Missing Labels'
  END AS validation_status;
// Expected: validation_status = 'PASS', missing_labels = []

// ===============================================
// VALIDATION 1.1.2: Relationship Type Existence
// ===============================================
CALL db.relationshipTypes() YIELD relationshipType
WITH collect(relationshipType) AS existing_rels
WITH existing_rels,
  // Core CVE relationships
  ['HAS_WEAKNESS', 'AFFECTS', 'IMPACTS_VENDOR', 'EXPLOITED_BY',
   'ENABLES_TECHNIQUE', 'MITIGATED_BY', 'EXPLOITED_BY_ACTOR',
   'USED_IN_CAMPAIGN', 'RELATED_TO', 'FIXED_BY',
   // Wave 1: SAREF
   'AFFECTS_SAREF_DEVICE', 'IMPACTS_SAREF_FUNCTION', 'CORRUPTS_MEASUREMENT',
   // Wave 2: ICS
   'AFFECTS_ICS_COMPONENT', 'EXPLOITS_PROTOCOL', 'ENABLES_ICS_TECHNIQUE',
   // Wave 3: SBOM
   'AFFECTS_SBOM_COMPONENT', 'IMPACTS_PACKAGE', 'PROPAGATES_THROUGH',
   // Wave 4: UCO
   'CREATES_OBSERVABLE', 'TRIGGERS_ACTION',
   // Wave 5: Threat Intelligence
   'EXPLOITED_BY_ACTOR_ENHANCED', 'HAS_STIX_INDICATOR', 'TARGETS_ICS_COMPONENT',
   'USES_ICS_TECHNIQUE', 'ASSOCIATED_WITH_STIX'] AS required_rels
WITH existing_rels, required_rels,
  [rel IN required_rels WHERE NOT rel IN existing_rels] AS missing_rels
RETURN
  required_rels,
  existing_rels,
  missing_rels,
  CASE
    WHEN size(missing_rels) = 0 THEN 'PASS'
    ELSE 'FAIL: Missing Relationships'
  END AS validation_status;
// Expected: validation_status = 'PASS', missing_rels = []

// ===============================================
// VALIDATION 1.1.3: Property Schema Validation
// ===============================================
// CVE node property schema
MATCH (c:CVE)
WITH c LIMIT 1
WITH keys(c) AS cve_properties
WITH cve_properties,
  ['id', 'cve_id', 'description', 'published_date', 'last_modified_date',
   'cvss_score', 'cvss_vector', 'severity', 'cwe_id', 'vulnerability_type',
   'references', 'advisory_links', 'impact_score', 'exploitability_score',
   'status', 'source', 'data_version', '_created_at', '_last_synced',
   // Wave 1: SAREF properties
   'saref_device_types', 'saref_function_impact', 'saref_measurement_risk',
   'iot_exploitation_vector', 'saref_severity_modifier',
   // Wave 2: ICS properties
   'ics_applicable', 'ics_component_types', 'purdue_levels', 'safety_impact',
   'process_impact', 'ics_mitre_techniques', 'industrial_protocols',
   // Wave 3: SBOM properties
   'sbom_component_count', 'package_ecosystems', 'dependency_depth',
   'license_implications', 'supply_chain_risk', 'purl_identifiers',
   // Wave 4: UCO properties
   'uco_observable_types', 'forensic_artifacts', 'exploitation_signatures',
   'investigation_priority',
   // Wave 5: Threat Intelligence properties
   'threat_actor_associations', 'campaign_usage_count', 'exploit_kit_usage',
   'dark_web_mentions', 'weaponization_timeline', 'stix_indicator_count',
   'threat_intel_confidence'] AS expected_properties
WITH cve_properties, expected_properties,
  [prop IN expected_properties WHERE NOT prop IN cve_properties] AS missing_props
RETURN
  expected_properties,
  cve_properties,
  missing_props,
  CASE
    WHEN size(missing_props) = 0 THEN 'PASS'
    WHEN size(missing_props) <= 5 THEN 'PASS (with warnings)'
    ELSE 'FAIL: Missing Properties'
  END AS validation_status;
// Expected: validation_status = 'PASS' or 'PASS (with warnings)'
// Note: Some properties may not be populated yet depending on wave completion
```

**Acceptance Criteria:**
- ✅ All required node labels exist in database
- ✅ All required relationship types exist in database
- ✅ CVE nodes have all core properties (original + enhanced)
- ✅ No unexpected schema changes to existing entities

### 1.2 Index Existence Validation

**Objective:** Verify all performance-critical indexes are created and online.

**Validation Query Suite:**

```cypher
// ===============================================
// VALIDATION 1.2.1: CVE Index Validation
// ===============================================
CALL db.indexes() YIELD name, state, labelsOrTypes, properties
WHERE 'CVE' IN labelsOrTypes
WITH collect({
  name: name,
  state: state,
  properties: properties
}) AS cve_indexes
WITH cve_indexes,
  ['id', 'cve_id', 'published_date', 'severity', 'cvss_score',
   'cwe_id', 'vulnerability_type', 'status', '_last_synced',
   // Enhanced property indexes
   'saref_device_types', 'iot_exploitation_vector',
   'ics_applicable', 'safety_impact', 'purdue_levels',
   'package_ecosystems', 'supply_chain_risk',
   'uco_observable_types', 'investigation_priority',
   'threat_actor_associations', 'weaponization_timeline'] AS expected_indexed_props
WITH cve_indexes,
  [prop IN expected_indexed_props
   WHERE NOT ANY(idx IN cve_indexes WHERE prop IN idx.properties)] AS missing_indexes,
  [idx IN cve_indexes WHERE idx.state <> 'ONLINE'] AS offline_indexes
RETURN
  size(cve_indexes) AS total_cve_indexes,
  missing_indexes,
  offline_indexes,
  CASE
    WHEN size(missing_indexes) = 0 AND size(offline_indexes) = 0 THEN 'PASS'
    WHEN size(offline_indexes) > 0 THEN 'FAIL: Offline Indexes'
    ELSE 'WARN: Missing Indexes'
  END AS validation_status;
// Expected: validation_status = 'PASS'

// ===============================================
// VALIDATION 1.2.2: Full-Text Index Validation
// ===============================================
CALL db.index.fulltext.queryNodes('cveFullTextSearch', 'test') YIELD node
RETURN 'PASS' AS validation_status
UNION ALL
CALL db.index.fulltext.queryNodes('cveEnhancedFullTextSearch', 'test') YIELD node
RETURN 'PASS' AS validation_status;
// Expected: Both queries return results without errors

// ===============================================
// VALIDATION 1.2.3: Composite Index Validation
// ===============================================
CALL db.indexes() YIELD name, state, properties
WHERE size(properties) > 1  // Composite indexes
  AND state = 'ONLINE'
WITH collect({name: name, properties: properties}) AS composite_indexes
RETURN
  composite_indexes,
  size(composite_indexes) AS count,
  CASE
    WHEN size(composite_indexes) >= 3 THEN 'PASS'
    ELSE 'WARN: Insufficient Composite Indexes'
  END AS validation_status;
// Expected: At least 3 composite indexes (severity+date, cvss+date, ics+severity)
```

**Acceptance Criteria:**
- ✅ All core CVE property indexes exist and are ONLINE
- ✅ Enhanced property indexes created for new properties
- ✅ Full-text search indexes functional
- ✅ Composite indexes created for common query patterns
- ✅ No index population failures (100% populated)

## 2. Data Integrity Validation Criteria

### 2.1 Node Count Validation

**Objective:** Verify no data loss occurred during enhancement waves.

**Validation Query Suite:**

```cypher
// ===============================================
// VALIDATION 2.1.1: CVE Node Count Preservation
// ===============================================
MATCH (c:CVE)
WITH count(c) AS current_cve_count
RETURN
  current_cve_count,
  147923 AS expected_cve_count,
  current_cve_count = 147923 AS count_preserved,
  CASE
    WHEN current_cve_count = 147923 THEN 'PASS'
    WHEN current_cve_count > 147923 THEN 'WARN: Additional CVEs Added'
    ELSE 'FAIL: CVE DATA LOSS'
  END AS validation_status;
// Expected: validation_status = 'PASS', count_preserved = true

// ===============================================
// VALIDATION 2.1.2: Property Completeness Check
// ===============================================
MATCH (c:CVE)
RETURN
  count(c) AS total_cves,
  count(c.id) AS cves_with_id,
  count(c.description) AS cves_with_description,
  count(c.cvss_score) AS cves_with_cvss,
  count(c.severity) AS cves_with_severity,
  count(c.published_date) AS cves_with_date,
  // Validate critical properties have high completeness
  (count(c.id) * 100.0 / count(c)) AS id_completeness_percent,
  (count(c.cvss_score) * 100.0 / count(c)) AS cvss_completeness_percent,
  CASE
    WHEN count(c.id) = count(c) AND count(c.cvss_score) >= 142847 THEN 'PASS'
    ELSE 'FAIL: Property Completeness Issue'
  END AS validation_status;
// Expected: id_completeness_percent = 100.0, cvss_completeness_percent >= 96.6

// ===============================================
// VALIDATION 2.1.3: Enhanced Property Population
// ===============================================
// Wave 1: SAREF property population
MATCH (c:CVE)
WHERE c.saref_device_types IS NOT NULL
WITH count(c) AS cves_with_saref
MATCH (c:CVE)
WITH cves_with_saref, count(c) AS total_cves
RETURN
  cves_with_saref,
  total_cves,
  (cves_with_saref * 100.0 / total_cves) AS saref_population_percent,
  CASE
    WHEN cves_with_saref > 0 THEN 'PASS: SAREF Enhancement Applied'
    ELSE 'FAIL: No SAREF Enhancement'
  END AS validation_status;
// Expected: saref_population_percent > 0.0 (at least some CVEs enhanced)

// Wave 2: ICS property population
MATCH (c:CVE)
WHERE c.ics_applicable = true
WITH count(c) AS ics_applicable_cves
MATCH (c:CVE)
WITH ics_applicable_cves, count(c) AS total_cves
RETURN
  ics_applicable_cves,
  total_cves,
  (ics_applicable_cves * 100.0 / total_cves) AS ics_population_percent,
  CASE
    WHEN ics_applicable_cves > 0 THEN 'PASS: ICS Enhancement Applied'
    ELSE 'FAIL: No ICS Enhancement'
  END AS validation_status;
// Expected: ics_population_percent > 0.0

// Wave 3: SBOM property population
MATCH (c:CVE)
WHERE c.sbom_component_count > 0
WITH count(c) AS cves_with_sbom
MATCH (c:CVE)
WITH cves_with_sbom, count(c) AS total_cves
RETURN
  cves_with_sbom,
  total_cves,
  (cves_with_sbom * 100.0 / total_cves) AS sbom_population_percent,
  CASE
    WHEN cves_with_sbom > 0 THEN 'PASS: SBOM Enhancement Applied'
    ELSE 'FAIL: No SBOM Enhancement'
  END AS validation_status;
// Expected: sbom_population_percent > 0.0
```

**Acceptance Criteria:**
- ✅ **CRITICAL**: CVE node count = 147,923 (zero tolerance for loss)
- ✅ Core property completeness matches baseline (id: 100%, cvss_score: ≥96.6%)
- ✅ Enhanced properties populated for applicable CVEs (>0% for each wave)
- ✅ No property values overwritten to NULL
- ✅ Property data types correct (Float for scores, DateTime for dates, etc.)

### 2.2 Relationship Integrity Validation

**Objective:** Verify existing relationships preserved and new relationships created correctly.

**Validation Query Suite:**

```cypher
// ===============================================
// VALIDATION 2.2.1: Existing Relationship Preservation
// ===============================================
MATCH (c:CVE)-[r]->()
WHERE type(r) IN [
  'HAS_WEAKNESS', 'AFFECTS', 'IMPACTS_VENDOR', 'EXPLOITED_BY',
  'ENABLES_TECHNIQUE', 'MITIGATED_BY', 'EXPLOITED_BY_ACTOR',
  'USED_IN_CAMPAIGN', 'RELATED_TO', 'FIXED_BY'
]
RETURN
  type(r) AS relationship_type,
  count(r) AS current_count,
  // Expected baseline counts
  CASE type(r)
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
  END AS expected_baseline,
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
    ELSE 'FAIL: Relationship Loss'
  END AS validation_status
ORDER BY relationship_type;
// Expected: All validation_status = 'PASS' (current_count >= expected_baseline)

// ===============================================
// VALIDATION 2.2.2: New Relationship Creation
// ===============================================
// Wave 1: SAREF relationships
MATCH (c:CVE)-[r:AFFECTS_SAREF_DEVICE]->()
WITH 'AFFECTS_SAREF_DEVICE' AS rel_type, count(r) AS count
RETURN rel_type, count,
  CASE WHEN count > 0 THEN 'PASS' ELSE 'FAIL' END AS status
UNION ALL
MATCH (c:CVE)-[r:IMPACTS_SAREF_FUNCTION]->()
WITH 'IMPACTS_SAREF_FUNCTION' AS rel_type, count(r) AS count
RETURN rel_type, count,
  CASE WHEN count > 0 THEN 'PASS' ELSE 'FAIL' END AS status
UNION ALL
MATCH (c:CVE)-[r:CORRUPTS_MEASUREMENT]->()
WITH 'CORRUPTS_MEASUREMENT' AS rel_type, count(r) AS count
RETURN rel_type, count,
  CASE WHEN count > 0 THEN 'PASS' ELSE 'FAIL' END AS status

UNION ALL
// Wave 2: ICS relationships
MATCH (c:CVE)-[r:AFFECTS_ICS_COMPONENT]->()
WITH 'AFFECTS_ICS_COMPONENT' AS rel_type, count(r) AS count
RETURN rel_type, count,
  CASE WHEN count > 0 THEN 'PASS' ELSE 'FAIL' END AS status
UNION ALL
MATCH (c:CVE)-[r:EXPLOITS_PROTOCOL]->()
WITH 'EXPLOITS_PROTOCOL' AS rel_type, count(r) AS count
RETURN rel_type, count,
  CASE WHEN count > 0 THEN 'PASS' ELSE 'FAIL' END AS status

UNION ALL
// Wave 3: SBOM relationships
MATCH (c:CVE)-[r:AFFECTS_SBOM_COMPONENT]->()
WITH 'AFFECTS_SBOM_COMPONENT' AS rel_type, count(r) AS count
RETURN rel_type, count,
  CASE WHEN count > 0 THEN 'PASS' ELSE 'FAIL' END AS status
UNION ALL
MATCH (c:CVE)-[r:PROPAGATES_THROUGH]->()
WITH 'PROPAGATES_THROUGH' AS rel_type, count(r) AS count
RETURN rel_type, count,
  CASE WHEN count > 0 THEN 'PASS' ELSE 'FAIL' END AS status

UNION ALL
// Wave 4: UCO relationships
MATCH (c:CVE)-[r:CREATES_OBSERVABLE]->()
WITH 'CREATES_OBSERVABLE' AS rel_type, count(r) AS count
RETURN rel_type, count,
  CASE WHEN count > 0 THEN 'PASS' ELSE 'FAIL' END AS status
UNION ALL
MATCH (c:CVE)-[r:TRIGGERS_ACTION]->()
WITH 'TRIGGERS_ACTION' AS rel_type, count(r) AS count
RETURN rel_type, count,
  CASE WHEN count > 0 THEN 'PASS' ELSE 'FAIL' END AS status

UNION ALL
// Wave 5: Threat Intelligence relationships
MATCH (c:CVE)-[r:HAS_STIX_INDICATOR]->()
WITH 'HAS_STIX_INDICATOR' AS rel_type, count(r) AS count
RETURN rel_type, count,
  CASE WHEN count > 0 THEN 'PASS' ELSE 'FAIL' END AS status;
// Expected: All status = 'PASS' (count > 0)

// ===============================================
// VALIDATION 2.2.3: Relationship Property Validation
// ===============================================
// Validate SAREF relationship properties
MATCH (c:CVE)-[r:AFFECTS_SAREF_DEVICE]->()
WITH r LIMIT 100
RETURN
  count(r.device_category) AS has_device_category,
  count(r.vulnerability_context) AS has_vuln_context,
  count(r.exposure_level) AS has_exposure_level,
  count(r.remediation_priority) AS has_priority,
  count(r.confidence_score) AS has_confidence,
  CASE
    WHEN count(r.device_category) = 100
      AND count(r.confidence_score) = 100
    THEN 'PASS'
    ELSE 'WARN: Incomplete Relationship Properties'
  END AS validation_status;
// Expected: All properties present in relationships

// Validate ICS relationship properties
MATCH (c:CVE)-[r:AFFECTS_ICS_COMPONENT]->()
WITH r LIMIT 100
RETURN
  count(r.component_type) AS has_component_type,
  count(r.criticality_level) AS has_criticality,
  count(r.ics_impact) AS has_impact,
  count(r.purdue_level) AS has_purdue_level,
  CASE
    WHEN count(r.component_type) = 100
      AND count(r.purdue_level) = 100
    THEN 'PASS'
    ELSE 'WARN: Incomplete Relationship Properties'
  END AS validation_status;
// Expected: Critical relationship properties populated
```

**Acceptance Criteria:**
- ✅ **CRITICAL**: All existing relationship counts ≥ baseline (no relationship loss)
- ✅ New relationships created for each wave (count > 0)
- ✅ Relationship properties populated with valid values
- ✅ No orphaned relationships (source or target nodes missing)
- ✅ Relationship cardinality correct (e.g., CVE can have multiple SAREFDevice targets)

## 3. Semantic Validation Criteria

### 3.1 Domain Logic Validation

**Objective:** Verify relationships and properties make semantic sense.

**Validation Query Suite:**

```cypher
// ===============================================
// VALIDATION 3.1.1: SAREF Device Type Consistency
// ===============================================
// Validate that CVEs affecting sensors have sensing-related descriptions
MATCH (c:CVE)-[r:AFFECTS_SAREF_DEVICE]->(saref:SAREFDevice)
WHERE r.device_category = 'sensor'
  AND NOT (c.description =~ '(?i).*(sensor|sensing|measurement|detect|monitor).*')
RETURN
  c.id AS potentially_incorrect_cve,
  c.description AS description,
  r.device_category AS claimed_device_category,
  r.confidence_score AS confidence;
// Expected: Empty result set (all sensor CVEs mention sensors)
// If results exist, review confidence scores and descriptions

// ===============================================
// VALIDATION 3.1.2: ICS Criticality Logic
// ===============================================
// Validate that safety_critical ICS vulnerabilities have high CVSS scores
MATCH (c:CVE)-[r:AFFECTS_ICS_COMPONENT]->()
WHERE r.criticality_level = 'safety_critical'
  AND c.cvss_score < 7.0
RETURN
  c.id AS low_severity_safety_critical,
  c.cvss_score AS cvss,
  r.criticality_level AS criticality,
  r.ics_impact AS impact;
// Expected: Empty or very small result set (safety critical should be high severity)

// ===============================================
// VALIDATION 3.1.3: Purdue Model Level Logic
// ===============================================
// Validate Purdue levels are in valid range (0-5)
MATCH (c:CVE)-[r:AFFECTS_ICS_COMPONENT]->()
WHERE ANY(level IN r.purdue_level WHERE level < 0 OR level > 5)
RETURN
  c.id AS invalid_purdue_level_cve,
  r.purdue_level AS invalid_levels;
// Expected: Empty result set (all Purdue levels between 0-5)

// ===============================================
// VALIDATION 3.1.4: SBOM Supply Chain Risk Logic
// ===============================================
// Validate high supply chain risk correlates with high component count or severity
MATCH (c:CVE)
WHERE c.supply_chain_risk = 'high'
  AND c.sbom_component_count < 5
  AND c.cvss_score < 7.0
RETURN
  c.id AS questionable_high_risk_cve,
  c.sbom_component_count AS component_count,
  c.cvss_score AS severity,
  c.supply_chain_risk AS risk_level;
// Expected: Empty or small result set (high risk should have justification)

// ===============================================
// VALIDATION 3.1.5: UCO Observable Artifact Consistency
// ===============================================
// Validate process observables have execution-related CVEs
MATCH (c:CVE)-[r:CREATES_OBSERVABLE]->(obs:UCOObservable {observable_type: 'process'})
WHERE NOT (c.description =~ '(?i).*(execution|command|process|inject|run|execute).*')
RETURN
  c.id AS potentially_incorrect_process_observable,
  c.description AS description,
  obs.observable_type AS observable_type;
// Expected: Empty or very small result set

// ===============================================
// VALIDATION 3.1.6: Threat Actor Motivation Consistency
// ===============================================
// Validate threat actor exploitation motivation matches actor profile
MATCH (ta:ThreatActor)-[r:EXPLOITED_BY_ACTOR]->(c:CVE)
WHERE r.exploitation_motivation <> ta.motivation
RETURN
  ta.name AS threat_actor,
  ta.motivation AS actor_motivation,
  r.exploitation_motivation AS relationship_motivation,
  c.id AS cve;
// Expected: Empty result set (motivations should match)
```

**Acceptance Criteria:**
- ✅ SAREF device categorization logically consistent with CVE descriptions
- ✅ ICS criticality levels correlate with severity and impact
- ✅ Purdue Model levels within valid range (0-5)
- ✅ Supply chain risk ratings justified by component count or severity
- ✅ UCO observable types match exploitation artifacts described in CVE
- ✅ Threat actor exploitation motivations consistent with actor profiles
- ✅ No semantic contradictions in relationship properties

### 3.2 Cross-Domain Integration Validation

**Objective:** Verify cross-domain relationships are logically correct.

**Validation Query Suite:**

```cypher
// ===============================================
// VALIDATION 3.2.1: SAREF → CVE → Mitigation Chain Completeness
// ===============================================
// Validate critical SAREF device vulnerabilities have mitigations
MATCH (saref:SAREFDevice)<-[:AFFECTS_SAREF_DEVICE]-(c:CVE)
WHERE c.severity = 'CRITICAL' AND c.cvss_score >= 9.0
OPTIONAL MATCH (c)-[:MITIGATED_BY]->(m:Mitigation)
WITH saref, c, m
WHERE m IS NULL
RETURN
  saref.device_category AS device,
  count(c) AS unmitigated_critical_cves,
  collect(c.id)[0..5] AS sample_cves;
// Expected: Low count or empty (critical CVEs should have mitigations)

// ===============================================
// VALIDATION 3.2.2: ICS → ATT&CK → CVE Chain Validation
// ===============================================
// Validate ICS CVEs enabling ATT&CK techniques actually affect ICS components
MATCH (c:CVE)-[:ENABLES_ICS_TECHNIQUE]->(tech:ICSAttackTechnique)
WHERE NOT EXISTS((c)-[:AFFECTS_ICS_COMPONENT]->())
RETURN
  c.id AS orphaned_ics_technique_cve,
  tech.technique_id AS technique;
// Expected: Empty result set (CVEs with ICS techniques should affect ICS components)

// ===============================================
// VALIDATION 3.2.3: SBOM → CVE → Dependency Propagation
// ===============================================
// Validate dependency chains have valid depth and impact assessment
MATCH (c:CVE)-[r:PROPAGATES_THROUGH]->(chain:DependencyChain)
WHERE r.chain_depth < 1 OR r.chain_depth IS NULL
RETURN
  c.id AS invalid_chain_depth_cve,
  r.chain_depth AS depth,
  chain.id AS chain_id;
// Expected: Empty result set (all chains should have valid depth ≥ 1)

// ===============================================
// VALIDATION 3.2.4: ThreatActor → CVE → UCO Observable Chain
// ===============================================
// Validate threat actors exploiting CVEs have observable artifacts
MATCH (ta:ThreatActor)-[:EXPLOITED_BY_ACTOR]->(c:CVE)
WHERE c.cvss_score >= 9.0  // Critical CVEs
OPTIONAL MATCH (c)-[:CREATES_OBSERVABLE]->(obs:UCOObservable)
WITH ta, c, collect(obs) AS observables
WHERE size(observables) = 0
RETURN
  ta.name AS threat_actor,
  count(c) AS critical_cves_without_observables,
  collect(c.id)[0..3] AS sample_cves;
// Expected: Low count (critical exploited CVEs should have forensic artifacts)

// ===============================================
// VALIDATION 3.2.5: Multi-Domain CVE Coverage
// ===============================================
// Validate high-severity CVEs are enhanced across multiple domains
MATCH (c:CVE)
WHERE c.severity = 'CRITICAL' AND c.cvss_score >= 9.0
OPTIONAL MATCH (c)-[:AFFECTS_SAREF_DEVICE]->(saref)
OPTIONAL MATCH (c)-[:AFFECTS_ICS_COMPONENT]->(ics)
OPTIONAL MATCH (c)-[:AFFECTS_SBOM_COMPONENT]->(sbom)
OPTIONAL MATCH (c)-[:CREATES_OBSERVABLE]->(uco)
WITH c,
  (saref IS NOT NULL) AS has_saref,
  (ics IS NOT NULL) AS has_ics,
  (sbom IS NOT NULL) AS has_sbom,
  (uco IS NOT NULL) AS has_uco
WITH c, has_saref, has_ics, has_sbom, has_uco,
  size([x IN [has_saref, has_ics, has_sbom, has_uco] WHERE x = true]) AS domain_coverage
WHERE domain_coverage = 0
RETURN
  c.id AS unenhanced_critical_cve,
  c.description AS description,
  domain_coverage;
// Expected: Empty or small result set (critical CVEs should have some enhancement)
```

**Acceptance Criteria:**
- ✅ Critical SAREF device vulnerabilities have mitigation paths
- ✅ CVEs enabling ICS ATT&CK techniques actually affect ICS components
- ✅ SBOM dependency chains have valid depth and impact assessments
- ✅ High-severity exploited CVEs have UCO forensic observables
- ✅ Critical CVEs enhanced across at least one domain (SAREF, ICS, SBOM, or UCO)
- ✅ No orphaned cross-domain relationships

## 4. Performance Validation Criteria

### 4.1 Query Performance Validation

**Objective:** Ensure query performance meets or exceeds baseline after enhancement.

**Validation Query Suite:**

```cypher
// ===============================================
// VALIDATION 4.1.1: CVE Lookup Performance (Baseline: <5ms)
// ===============================================
PROFILE
MATCH (c:CVE {id: 'CVE-2023-12345'})
RETURN c;
// Expected: Execution time < 10ms (allowing 2x baseline tolerance)

// ===============================================
// VALIDATION 4.1.2: Severity Filter Performance (Baseline: <50ms)
// ===============================================
PROFILE
MATCH (c:CVE)
WHERE c.severity = 'CRITICAL'
  AND c.published_date >= date('2023-01-01')
RETURN c
ORDER BY c.cvss_score DESC
LIMIT 100;
// Expected: Execution time < 100ms

// ===============================================
// VALIDATION 4.1.3: Multi-hop Relationship Performance (Baseline: <200ms)
// ===============================================
PROFILE
MATCH path = (c:CVE {id: 'CVE-2023-12345'})-[*1..2]-(related)
RETURN path
LIMIT 50;
// Expected: Execution time < 400ms

// ===============================================
// VALIDATION 4.1.4: Full-Text Search Performance (Baseline: <100ms)
// ===============================================
PROFILE
CALL db.index.fulltext.queryNodes(
  'cveFullTextSearch',
  'sql injection'
) YIELD node, score
RETURN node, score
ORDER BY score DESC
LIMIT 20;
// Expected: Execution time < 200ms

// ===============================================
// VALIDATION 4.1.5: Complex Analytics Performance (Baseline: <500ms)
// ===============================================
PROFILE
MATCH (c:CVE)
WHERE c.published_date >= date('2023-01-01')
  AND c.published_date < date('2024-01-01')
RETURN
  c.severity AS severity,
  count(c) AS count,
  avg(c.cvss_score) AS avg_cvss,
  collect(c.id)[0..5] AS sample_cves
ORDER BY severity;
// Expected: Execution time < 1000ms

// ===============================================
// VALIDATION 4.1.6: Enhanced Cross-Domain Query Performance
// ===============================================
PROFILE
MATCH (c:CVE)-[:AFFECTS_SAREF_DEVICE]->(saref:SAREFDevice)
MATCH (c)-[:AFFECTS_ICS_COMPONENT]->(ics:ICSComponent)
WHERE c.cvss_score >= 9.0
RETURN
  c.id AS cve,
  saref.device_category AS iot_device,
  ics.component_type AS ics_component,
  c.cvss_score AS severity
LIMIT 50;
// Expected: Execution time < 500ms

// ===============================================
// VALIDATION 4.1.7: Threat Actor Exploitation Chain Performance
// ===============================================
PROFILE
MATCH (ta:ThreatActor)-[:EXPLOITED_BY_ACTOR]->(c:CVE)-[:CREATES_OBSERVABLE]->(obs:UCOObservable)
WHERE ta.name = 'APT28'
RETURN
  ta.name AS actor,
  collect(DISTINCT c.id) AS exploited_cves,
  collect(DISTINCT obs.observable_type) AS observables
LIMIT 100;
// Expected: Execution time < 300ms
```

**Performance Measurement Script:**

```bash
#!/bin/bash
# File: /home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/scripts/measure_query_performance.sh

echo "=== Query Performance Validation ==="
echo "Measuring query execution times..."

# Function to measure query time
measure_query() {
  local query_name=$1
  local query=$2
  local baseline_ms=$3

  echo "Testing: $query_name"
  start_time=$(date +%s%3N)

  cypher-shell -u neo4j -p password "$query" > /dev/null 2>&1

  end_time=$(date +%s%3N)
  execution_time=$((end_time - start_time))

  if [ "$execution_time" -le "$((baseline_ms * 2))" ]; then
    echo "✓ PASS: ${execution_time}ms (baseline: ${baseline_ms}ms, tolerance: $((baseline_ms * 2))ms)"
  else
    echo "✗ FAIL: ${execution_time}ms exceeds tolerance"
  fi
}

# Test queries
measure_query "CVE Lookup" "MATCH (c:CVE {id: 'CVE-2023-12345'}) RETURN c;" 5
measure_query "Severity Filter" "MATCH (c:CVE) WHERE c.severity = 'CRITICAL' RETURN c LIMIT 100;" 50
measure_query "Full-Text Search" "CALL db.index.fulltext.queryNodes('cveFullTextSearch', 'sql injection') YIELD node RETURN node LIMIT 20;" 100

echo "=== Performance Validation Complete ==="
```

**Acceptance Criteria:**
- ✅ Simple CVE lookup < 10ms (2x baseline tolerance)
- ✅ Severity filtering < 100ms
- ✅ Multi-hop relationships < 400ms
- ✅ Full-text search < 200ms
- ✅ Complex analytics < 1000ms
- ✅ Enhanced cross-domain queries < 500ms
- ✅ No query performance regression > 100% (2x slowdown)
- ✅ Index hints used appropriately in PROFILE output

### 4.2 Scalability Validation

**Objective:** Verify system handles enhanced data volume efficiently.

**Validation Query Suite:**

```cypher
// ===============================================
// VALIDATION 4.2.1: Total Relationship Count
// ===============================================
MATCH ()-[r]->()
WITH count(r) AS total_rels
RETURN
  total_rels,
  total_rels / 1000000.0 AS total_rels_millions,
  CASE
    WHEN total_rels > 0 AND total_rels < 10000000 THEN 'PASS: Manageable Scale'
    WHEN total_rels >= 10000000 THEN 'WARN: Large Scale (Monitor Performance)'
    ELSE 'FAIL: Zero Relationships'
  END AS validation_status;
// Expected: total_rels > 1,670,834 (baseline), validation_status = 'PASS'

// ===============================================
// VALIDATION 4.2.2: Average Relationship Degree
// ===============================================
MATCH (c:CVE)
OPTIONAL MATCH (c)-[r]->()
WITH c, count(r) AS degree
RETURN
  min(degree) AS min_degree,
  max(degree) AS max_degree,
  avg(degree) AS avg_degree,
  percentileCont(degree, 0.95) AS p95_degree,
  CASE
    WHEN avg(degree) > 0 AND avg(degree) < 100 THEN 'PASS: Healthy Connectivity'
    ELSE 'WARN: Review Connectivity'
  END AS validation_status;
// Expected: avg_degree between 5-50, p95_degree < 100

// ===============================================
// VALIDATION 4.2.3: Memory Usage Estimate
// ===============================================
CALL apoc.meta.stats() YIELD nodeCount, relCount, labelCount, relTypeCount, propertyKeyCount
RETURN
  nodeCount,
  relCount,
  labelCount,
  relTypeCount,
  propertyKeyCount,
  (nodeCount * 500 + relCount * 200) / 1024 / 1024 AS estimated_heap_mb,
  CASE
    WHEN (nodeCount * 500 + relCount * 200) / 1024 / 1024 < 16000 THEN 'PASS: Manageable Memory'
    ELSE 'WARN: High Memory Usage'
  END AS validation_status;
// Expected: estimated_heap_mb < 16,000 MB (16GB) for production systems
```

**Acceptance Criteria:**
- ✅ Total relationships > baseline (1.67M) and < 10M for manageable scale
- ✅ Average CVE relationship degree between 5-50 (healthy connectivity)
- ✅ 95th percentile relationship degree < 100 (no super-nodes)
- ✅ Estimated heap memory < 16GB for production deployment
- ✅ Query response times linear with data growth (not exponential)

## 5. Wave-Specific Validation

### 5.1 Wave 1: SAREF IoT Integration Validation

```cypher
// Wave 1 Validation Suite
MATCH (c:CVE)-[:AFFECTS_SAREF_DEVICE]->(saref:SAREFDevice)
WITH count(DISTINCT c) AS saref_cves,
     count(DISTINCT saref) AS saref_devices
MATCH (c:CVE)-[:IMPACTS_SAREF_FUNCTION]->()
WITH saref_cves, saref_devices, count(DISTINCT c) AS function_impact_cves
MATCH (c:CVE)-[:CORRUPTS_MEASUREMENT]->()
WITH saref_cves, saref_devices, function_impact_cves, count(DISTINCT c) AS measurement_cves
RETURN
  saref_cves,
  saref_devices,
  function_impact_cves,
  measurement_cves,
  CASE
    WHEN saref_cves > 0 AND saref_devices >= 3 THEN 'PASS: Wave 1 Complete'
    ELSE 'FAIL: Wave 1 Incomplete'
  END AS validation_status;
// Expected: saref_cves > 0, saref_devices >= 3 (sensor, actuator, appliance)
```

### 5.2 Wave 2: ICS/OT Integration Validation

```cypher
// Wave 2 Validation Suite
MATCH (c:CVE)-[:AFFECTS_ICS_COMPONENT]->(ics:ICSComponent)
WITH count(DISTINCT c) AS ics_cves,
     count(DISTINCT ics) AS ics_components
MATCH (c:CVE)-[:EXPLOITS_PROTOCOL]->()
WITH ics_cves, ics_components, count(DISTINCT c) AS protocol_cves
MATCH (c:CVE)
WHERE c.ics_applicable = true
WITH ics_cves, ics_components, protocol_cves, count(c) AS ics_applicable_cves
RETURN
  ics_cves,
  ics_components,
  protocol_cves,
  ics_applicable_cves,
  CASE
    WHEN ics_cves > 0 AND ics_components >= 5 THEN 'PASS: Wave 2 Complete'
    ELSE 'FAIL: Wave 2 Incomplete'
  END AS validation_status;
// Expected: ics_cves > 0, ics_components >= 5 (PLC, HMI, SCADA, DCS, RTU)
```

### 5.3 Wave 3: SBOM Integration Validation

```cypher
// Wave 3 Validation Suite
MATCH (c:CVE)-[:AFFECTS_SBOM_COMPONENT]->(sbom:SBOMComponent)
WITH count(DISTINCT c) AS sbom_cves,
     count(DISTINCT sbom) AS sbom_components
MATCH (c:CVE)-[:PROPAGATES_THROUGH]->()
WITH sbom_cves, sbom_components, count(DISTINCT c) AS chain_cves
MATCH (c:CVE)
WHERE c.sbom_component_count > 0
WITH sbom_cves, sbom_components, chain_cves, count(c) AS tracked_cves
RETURN
  sbom_cves,
  sbom_components,
  chain_cves,
  tracked_cves,
  CASE
    WHEN sbom_cves > 0 AND sbom_components > 0 THEN 'PASS: Wave 3 Complete'
    ELSE 'FAIL: Wave 3 Incomplete'
  END AS validation_status;
// Expected: sbom_cves > 0, sbom_components > 0
```

### 5.4 Wave 4: UCO Integration Validation

```cypher
// Wave 4 Validation Suite
MATCH (c:CVE)-[:CREATES_OBSERVABLE]->(obs:UCOObservable)
WITH count(DISTINCT c) AS observable_cves,
     count(DISTINCT obs) AS observable_types
MATCH (c:CVE)-[:TRIGGERS_ACTION]->()
WITH observable_cves, observable_types, count(DISTINCT c) AS action_cves
MATCH (c:CVE)
WHERE c.uco_observable_types IS NOT NULL
WITH observable_cves, observable_types, action_cves, count(c) AS tracked_cves
RETURN
  observable_cves,
  observable_types,
  action_cves,
  tracked_cves,
  CASE
    WHEN observable_cves > 0 AND observable_types >= 4 THEN 'PASS: Wave 4 Complete'
    ELSE 'FAIL: Wave 4 Incomplete'
  END AS validation_status;
// Expected: observable_cves > 0, observable_types >= 4 (file, process, network, registry)
```

### 5.5 Wave 5: Threat Intelligence Integration Validation

```cypher
// Wave 5 Validation Suite
MATCH (c:CVE)-[:HAS_STIX_INDICATOR]->()
WITH count(DISTINCT c) AS stix_cves
MATCH (ta:ThreatActor)
WHERE ta.psychometric_profile IS NOT NULL
WITH stix_cves, count(ta) AS profiled_actors
MATCH (ta:ThreatActor)-[:TARGETS_ICS_COMPONENT]->()
WITH stix_cves, profiled_actors, count(DISTINCT ta) AS ics_targeting_actors
RETURN
  stix_cves,
  profiled_actors,
  ics_targeting_actors,
  CASE
    WHEN stix_cves > 0 AND profiled_actors > 0 THEN 'PASS: Wave 5 Complete'
    ELSE 'FAIL: Wave 5 Incomplete'
  END AS validation_status;
// Expected: stix_cves > 0, profiled_actors > 0
```

## 6. Final Acceptance Criteria

### 6.1 Go/No-Go Decision Criteria

**CRITICAL (Must Pass All):**
- ✅ CVE node count = 147,923 (zero data loss)
- ✅ All existing relationship types preserved with counts ≥ baseline
- ✅ All core CVE properties intact (id, description, cvss_score, etc.)
- ✅ All required indexes created and ONLINE
- ✅ No query performance regression > 100% (2x slowdown)

**HIGH PRIORITY (Must Pass ≥80%):**
- ✅ Enhanced properties populated for applicable CVEs (>0% per wave)
- ✅ New relationships created for each completed wave
- ✅ Semantic consistency checks pass (no logical contradictions)
- ✅ Cross-domain integration chains complete
- ✅ Wave-specific validation criteria met

**MEDIUM PRIORITY (Must Pass ≥60%):**
- ✅ Relationship property completeness ≥90%
- ✅ Complex query performance within 2x tolerance
- ✅ Scalability metrics within acceptable ranges
- ✅ Multi-domain CVE coverage for critical vulnerabilities

### 6.2 Validation Report Template

```markdown
# Schema Enhancement Validation Report

**Date:** [YYYY-MM-DD]
**Waves Validated:** [1, 2, 3, 4, 5]
**Overall Status:** [PASS / CONDITIONAL PASS / FAIL]

## 1. Structural Validation
- Node Labels: [PASS/FAIL]
- Relationship Types: [PASS/FAIL]
- Property Schemas: [PASS/FAIL]
- Index Existence: [PASS/FAIL]

## 2. Data Integrity
- CVE Node Count: [PASS/FAIL] (147,923 expected)
- Property Completeness: [PASS/FAIL]
- Relationship Preservation: [PASS/FAIL]
- New Relationships: [PASS/FAIL]

## 3. Semantic Validation
- Domain Logic: [PASS/FAIL]
- Cross-Domain Integration: [PASS/FAIL]
- Attribute Consistency: [PASS/FAIL]

## 4. Performance Validation
- Query Performance: [PASS/FAIL]
- Scalability: [PASS/FAIL]

## 5. Wave-Specific Validation
- Wave 1 (SAREF): [PASS/FAIL]
- Wave 2 (ICS): [PASS/FAIL]
- Wave 3 (SBOM): [PASS/FAIL]
- Wave 4 (UCO): [PASS/FAIL]
- Wave 5 (Threat Intel): [PASS/FAIL]

## 6. Critical Failures
[List any critical failures that require immediate remediation]

## 7. Warnings and Recommendations
[List warnings and improvement recommendations]

## 8. Approval Decision
**Approved for Production:** [YES / NO / CONDITIONAL]
**Conditions (if applicable):** [List conditions]

**Validated By:** [Name]
**Date:** [YYYY-MM-DD]
```

---

**Document Version:** v1.0.0
**Last Updated:** 2025-10-30
**Next Review:** After Each Wave Completion
**Owner:** AEON FORGE Implementation Team
