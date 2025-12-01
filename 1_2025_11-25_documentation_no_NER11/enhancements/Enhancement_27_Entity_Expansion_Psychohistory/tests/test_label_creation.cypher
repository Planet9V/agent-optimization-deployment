// ============================================================
// Enhancement 27: Label Creation Tests
// File: tests/test_label_creation.cypher
// Created: 2025-11-26 23:30:00 UTC
// Purpose: Verify all 16 Super Labels are correctly created
// ============================================================

// ============================================================
// TEST SUITE 1: LABEL COUNT VERIFICATION
// ============================================================

// T1.1: Verify exactly 16 Super Labels exist (after migration)
// Expected: 16 labels
CALL db.labels() YIELD label
WITH collect(label) as all_labels
WHERE NOT label STARTS WITH '_'  // Exclude internal labels
RETURN
  size(all_labels) as label_count,
  all_labels as labels,
  CASE
    WHEN size(all_labels) = 16 THEN 'PASS'
    WHEN size(all_labels) < 16 THEN 'FAIL - Missing labels'
    ELSE 'FAIL - Extra labels remain'
  END as test_result,
  '16 Super Labels should exist' as test_description;

// T1.2: Verify required Super Labels present
WITH ['ThreatActor', 'AttackPattern', 'Vulnerability', 'Malware', 'Indicator',
      'Asset', 'Organization', 'Location', 'Software', 'Protocol',
      'PsychTrait', 'EconomicMetric', 'Role', 'Campaign', 'Event', 'Control'] as required_labels
CALL db.labels() YIELD label
WITH required_labels, collect(label) as existing_labels
WITH required_labels, existing_labels,
     [l IN required_labels WHERE NOT l IN existing_labels] as missing_labels
RETURN
  size(missing_labels) as missing_count,
  missing_labels,
  CASE WHEN size(missing_labels) = 0 THEN 'PASS' ELSE 'FAIL' END as test_result,
  'All required Super Labels should exist' as test_description;

// ============================================================
// TEST SUITE 2: DEPRECATED LABEL VERIFICATION
// ============================================================

// T2.1: Verify no deprecated labels remain
WITH ['AttackTechnique', 'CVE', 'Exploit', 'VulnerabilityReport', 'MalwareVariant',
      'Mitigation', 'ComplianceFramework', 'NERCCIPStandard', 'IncidentReport', 'Sector',
      'Substation', 'TransmissionLine', 'EnergyDevice', 'EnergyManagementSystem',
      'DistributedEnergyResource', 'WaterSystem', 'Measurement', 'EnergyProperty',
      'WaterProperty'] as deprecated_labels
CALL db.labels() YIELD label
WITH deprecated_labels, collect(label) as existing_labels
WITH [l IN deprecated_labels WHERE l IN existing_labels] as remaining_deprecated
RETURN
  size(remaining_deprecated) as deprecated_count,
  remaining_deprecated,
  CASE WHEN size(remaining_deprecated) = 0 THEN 'PASS' ELSE 'FAIL' END as test_result,
  'No deprecated labels should remain' as test_description;

// T2.2: Verify no nodes with deprecated labels
MATCH (n)
WHERE any(l IN labels(n) WHERE l IN [
  'AttackTechnique', 'CVE', 'Exploit', 'VulnerabilityReport', 'MalwareVariant',
  'Mitigation', 'ComplianceFramework', 'NERCCIPStandard', 'IncidentReport', 'Sector',
  'Substation', 'TransmissionLine', 'EnergyDevice', 'EnergyManagementSystem',
  'DistributedEnergyResource', 'WaterSystem', 'Measurement', 'EnergyProperty', 'WaterProperty'
])
WITH labels(n)[0] as deprecated_label, count(*) as node_count
RETURN
  deprecated_label,
  node_count,
  'FAIL' as test_result,
  'Nodes with deprecated labels found' as test_description
UNION ALL
MATCH (n)
WHERE NOT any(l IN labels(n) WHERE l IN [
  'AttackTechnique', 'CVE', 'Exploit', 'VulnerabilityReport', 'MalwareVariant',
  'Mitigation', 'ComplianceFramework', 'NERCCIPStandard', 'IncidentReport', 'Sector',
  'Substation', 'TransmissionLine', 'EnergyDevice', 'EnergyManagementSystem',
  'DistributedEnergyResource', 'WaterSystem', 'Measurement', 'EnergyProperty', 'WaterProperty'
])
WITH count(*) as clean_count
WHERE clean_count > 0
RETURN
  'None' as deprecated_label,
  0 as node_count,
  'PASS' as test_result,
  'No nodes with deprecated labels' as test_description
LIMIT 1;

// ============================================================
// TEST SUITE 3: DISCRIMINATOR PROPERTY VERIFICATION
// ============================================================

// T3.1: Verify Asset nodes have assetClass property
MATCH (n:Asset)
WHERE n.assetClass IS NULL
WITH count(*) as missing_assetClass
RETURN
  missing_assetClass,
  CASE WHEN missing_assetClass = 0 THEN 'PASS' ELSE 'FAIL' END as test_result,
  'All Asset nodes should have assetClass property' as test_description;

// T3.2: Verify Asset nodes have deviceType property
MATCH (n:Asset)
WHERE n.deviceType IS NULL
WITH count(*) as missing_deviceType
RETURN
  missing_deviceType,
  CASE WHEN missing_deviceType = 0 THEN 'PASS' ELSE 'FAIL' END as test_result,
  'All Asset nodes should have deviceType property' as test_description;

// T3.3: Verify Vulnerability nodes have vulnType property
MATCH (n:Vulnerability)
WHERE n.vulnType IS NULL
WITH count(*) as missing_vulnType
RETURN
  missing_vulnType,
  CASE WHEN missing_vulnType = 0 THEN 'PASS' ELSE 'FAIL' END as test_result,
  'All Vulnerability nodes should have vulnType property' as test_description;

// T3.4: Verify AttackPattern nodes have patternType property
MATCH (n:AttackPattern)
WHERE n.patternType IS NULL
WITH count(*) as missing_patternType
RETURN
  missing_patternType,
  CASE WHEN missing_patternType = 0 THEN 'PASS' ELSE 'FAIL' END as test_result,
  'All AttackPattern nodes should have patternType property' as test_description;

// T3.5: Verify Control nodes have controlType property
MATCH (n:Control)
WHERE n.controlType IS NULL
WITH count(*) as missing_controlType
RETURN
  missing_controlType,
  CASE WHEN missing_controlType = 0 THEN 'PASS' ELSE 'FAIL' END as test_result,
  'All Control nodes should have controlType property' as test_description;

// ============================================================
// TEST SUITE 4: MIGRATION TRACKING VERIFICATION
// ============================================================

// T4.1: Verify migration tracking properties exist
MATCH (n)
WHERE n.migrated_from IS NOT NULL
WITH n.migrated_from as source_label, count(*) as migrated_count
RETURN
  source_label,
  migrated_count,
  'INFO' as test_result,
  'Migration tracking - nodes migrated from each source' as test_description
ORDER BY source_label;

// T4.2: Verify migration dates are recorded
MATCH (n)
WHERE n.migrated_from IS NOT NULL AND n.migration_date IS NULL
WITH count(*) as missing_date
RETURN
  missing_date,
  CASE WHEN missing_date = 0 THEN 'PASS' ELSE 'FAIL' END as test_result,
  'All migrated nodes should have migration_date' as test_description;

// ============================================================
// TEST SUITE 5: NODE DISTRIBUTION VERIFICATION
// ============================================================

// T5.1: Count nodes per Super Label
CALL db.labels() YIELD label
WHERE NOT label STARTS WITH '_'
CALL {
  WITH label
  MATCH (n) WHERE label IN labels(n)
  RETURN count(n) as node_count
}
RETURN
  label,
  node_count,
  'INFO' as test_result,
  'Node distribution across Super Labels' as test_description
ORDER BY node_count DESC;

// T5.2: Verify no orphan nodes (nodes without any label)
MATCH (n)
WHERE size(labels(n)) = 0
WITH count(*) as orphan_count
RETURN
  orphan_count,
  CASE WHEN orphan_count = 0 THEN 'PASS' ELSE 'FAIL' END as test_result,
  'No orphan nodes (without labels) should exist' as test_description;

// ============================================================
// AGGREGATE TEST SUMMARY
// ============================================================

// Run all tests and generate summary
// Note: This requires APOC for aggregate collection
// CALL {
//   // Run each test and collect results
//   ...
// }
// RETURN test_suite, passed_count, failed_count, total_tests;
