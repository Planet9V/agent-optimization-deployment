// ============================================================
// Migration Test Script
// File: test_migration.cypher
// Created: 2025-11-28
// Purpose: Test each phase of 03_migration_24_to_16.cypher
// ============================================================

// ============================================================
// PRE-MIGRATION DIAGNOSTICS
// ============================================================

// Test 1: Count existing deprecated labels
CALL db.labels() YIELD label
WHERE label IN [
  'AttackTechnique', 'CVE', 'Exploit', 'VulnerabilityReport',
  'MalwareVariant', 'Mitigation', 'ComplianceFramework', 'NERCCIPStandard',
  'IncidentReport', 'Sector', 'Substation', 'TransmissionLine',
  'EnergyDevice', 'EnergyManagementSystem', 'DistributedEnergyResource',
  'WaterSystem', 'Measurement', 'EnergyProperty', 'WaterProperty'
]
WITH label
MATCH (n) WHERE label IN labels(n)
RETURN label, count(n) as pre_migration_count
ORDER BY label;

// ============================================================
// PHASE 2 TESTS: DISCRIMINATOR PROPERTY ADDITION
// ============================================================

// Test 2.1: ThreatActor actorType assignment
MATCH (n:ThreatActor)
WHERE n.actorType IS NULL
RETURN
  'ThreatActor' as label,
  count(*) as missing_discriminator,
  collect(DISTINCT n.name)[0..5] as sample_names;

// Test 2.2: AttackPattern patternType assignment
MATCH (n:AttackPattern)
WHERE n.patternType IS NULL
RETURN
  'AttackPattern' as label,
  count(*) as missing_discriminator,
  collect(DISTINCT n.external_id)[0..5] as sample_ids;

// Test 2.3: Organization orgType assignment
MATCH (n:Organization)
WHERE n.orgType IS NULL
RETURN
  'Organization' as label,
  count(*) as missing_discriminator,
  collect(DISTINCT n.name)[0..5] as sample_names;

// Test 2.4: Location locationType assignment
MATCH (n:Location)
WHERE n.locationType IS NULL
RETURN
  'Location' as label,
  count(*) as missing_discriminator,
  collect(DISTINCT n.name)[0..5] as sample_names;

// Test 2.5: Software softwareType assignment
MATCH (n:Software)
WHERE n.softwareType IS NULL
RETURN
  'Software' as label,
  count(*) as missing_discriminator,
  collect(DISTINCT n.name)[0..5] as sample_names;

// ============================================================
// INDIVIDUAL CASE STATEMENT TESTS
// ============================================================

// Test CASE 2.1: ThreatActor actorType logic
MATCH (n:ThreatActor)
WHERE n.actorType IS NULL
WITH n,
  CASE
    WHEN n.type IS NOT NULL THEN n.type
    WHEN n.name CONTAINS 'APT' THEN 'apt'
    WHEN n.name CONTAINS 'State' THEN 'nation_state'
    ELSE 'unknown'
  END as computed_actorType
RETURN
  n.name,
  n.type,
  computed_actorType,
  CASE
    WHEN computed_actorType IS NULL THEN 'ERROR: NULL result'
    ELSE 'OK'
  END as validation
LIMIT 10;

// Test CASE 2.2: AttackPattern patternType logic
MATCH (n:AttackPattern)
WHERE n.patternType IS NULL
WITH n,
  CASE
    WHEN n.external_id STARTS WITH 'T' THEN 'technique'
    WHEN n.external_id STARTS WITH 'TA' THEN 'tactic'
    WHEN n.external_id STARTS WITH 'CAPEC' THEN 'capec'
    ELSE 'technique'
  END as computed_patternType
RETURN
  n.name,
  n.external_id,
  computed_patternType,
  CASE
    WHEN computed_patternType IS NULL THEN 'ERROR: NULL result'
    ELSE 'OK'
  END as validation
LIMIT 10;

// Test CASE 2.3: Organization orgType logic
MATCH (n:Organization)
WHERE n.orgType IS NULL
WITH n,
  CASE
    WHEN n.sector IS NOT NULL THEN 'company'
    WHEN n.name CONTAINS 'Agency' THEN 'government'
    WHEN n.name CONTAINS 'University' THEN 'academic'
    ELSE 'company'
  END as computed_orgType
RETURN
  n.name,
  n.sector,
  computed_orgType,
  CASE
    WHEN computed_orgType IS NULL THEN 'ERROR: NULL result'
    ELSE 'OK'
  END as validation
LIMIT 10;

// Test CASE 2.4: Location locationType logic
MATCH (n:Location)
WHERE n.locationType IS NULL
WITH n,
  CASE
    WHEN n.type IS NOT NULL THEN n.type
    WHEN n.coordinates IS NOT NULL THEN 'geo'
    ELSE 'facility'
  END as computed_locationType
RETURN
  n.name,
  n.type,
  n.coordinates,
  computed_locationType,
  CASE
    WHEN computed_locationType IS NULL THEN 'ERROR: NULL result'
    ELSE 'OK'
  END as validation
LIMIT 10;

// Test CASE 2.5: Software softwareType logic
MATCH (n:Software)
WHERE n.softwareType IS NULL
WITH n,
  CASE
    WHEN n.is_malware = true THEN 'malware_tool'
    WHEN n.type IS NOT NULL THEN n.type
    ELSE 'application'
  END as computed_softwareType
RETURN
  n.name,
  n.is_malware,
  n.type,
  computed_softwareType,
  CASE
    WHEN computed_softwareType IS NULL THEN 'ERROR: NULL result'
    ELSE 'OK'
  END as validation
LIMIT 10;

// ============================================================
// POST-MIGRATION VERIFICATION
// ============================================================

// Verify 1: Count nodes per final label (should show 16 Super Labels)
CALL db.labels() YIELD label
WHERE NOT label STARTS WITH '_'
WITH label
MATCH (n) WHERE label IN labels(n)
RETURN label, count(n) as node_count
ORDER BY node_count DESC, label;

// Verify 2: Check for any remaining deprecated labels
MATCH (n)
WHERE any(l IN labels(n) WHERE l IN [
  'AttackTechnique', 'CVE', 'Exploit', 'VulnerabilityReport',
  'MalwareVariant', 'Mitigation', 'ComplianceFramework', 'NERCCIPStandard',
  'IncidentReport', 'Sector', 'Substation', 'TransmissionLine',
  'EnergyDevice', 'EnergyManagementSystem', 'DistributedEnergyResource',
  'WaterSystem', 'Measurement', 'EnergyProperty', 'WaterProperty'
])
RETURN labels(n) as deprecated_labels, count(*) as remaining_count
ORDER BY deprecated_labels;

// Verify 3: Migration tracking completeness
MATCH (n)
WHERE n.migrated_from IS NOT NULL
RETURN
  n.migrated_from as source_label,
  labels(n) as current_labels,
  count(*) as migrated_count,
  min(n.migration_date) as earliest_migration,
  max(n.migration_date) as latest_migration
ORDER BY source_label;

// Verify 4: Discriminator property coverage
MATCH (n:ThreatActor)
RETURN 'ThreatActor' as label,
  count(*) as total,
  sum(CASE WHEN n.actorType IS NULL THEN 1 ELSE 0 END) as missing_discriminator
UNION ALL
MATCH (n:AttackPattern)
RETURN 'AttackPattern' as label,
  count(*) as total,
  sum(CASE WHEN n.patternType IS NULL THEN 1 ELSE 0 END) as missing_discriminator
UNION ALL
MATCH (n:Organization)
RETURN 'Organization' as label,
  count(*) as total,
  sum(CASE WHEN n.orgType IS NULL THEN 1 ELSE 0 END) as missing_discriminator
UNION ALL
MATCH (n:Location)
RETURN 'Location' as label,
  count(*) as total,
  sum(CASE WHEN n.locationType IS NULL THEN 1 ELSE 0 END) as missing_discriminator
UNION ALL
MATCH (n:Software)
RETURN 'Software' as label,
  count(*) as total,
  sum(CASE WHEN n.softwareType IS NULL THEN 1 ELSE 0 END) as missing_discriminator;

// Verify 5: Sample migrated nodes by phase
MATCH (n:Vulnerability)
WHERE n.migrated_from IN ['CVE', 'Exploit', 'VulnerabilityReport']
RETURN
  'Vulnerability consolidation' as phase,
  n.migrated_from as original_label,
  n.vulnType as discriminator,
  count(*) as count
ORDER BY original_label;

// Verify 6: Sample Asset migrations
MATCH (n:Asset)
WHERE n.migrated_from IN [
  'Substation', 'TransmissionLine', 'EnergyDevice',
  'EnergyManagementSystem', 'DistributedEnergyResource', 'WaterSystem'
]
RETURN
  'Asset consolidation' as phase,
  n.migrated_from as original_label,
  n.deviceType as discriminator,
  n.purdue_level as purdue_level,
  count(*) as count
ORDER BY original_label;
