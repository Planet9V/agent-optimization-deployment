// ============================================================
// Enhancement 27: Constraint Verification
// File: verify_constraints.cypher
// Created: 2025-11-28 22:10:00 UTC
// Purpose: Verify all E27 constraints are properly created
// ============================================================

// ------------------------------------------------------------
// VERIFICATION 1: Count E27 Constraints
// ------------------------------------------------------------
// Should return exactly 16 constraints

SHOW CONSTRAINTS
YIELD name, type, entityType, properties
WHERE entityType = 'NODE'
  AND type IN ['UNIQUENESS', 'NODE_KEY']
  AND name IN [
    'constraint_338f9f7b',  // ThreatActor.name
    'attack_pattern_id',     // AttackPattern.external_id
    'vulnerability_id',      // Vulnerability.external_id
    'constraint_ce8e6a06',  // Malware.name
    'indicator_id',          // Indicator.indicator_value
    'asset_id',              // Asset.asset_id
    'org_name',              // Organization.name
    'location_id',           // Location (name, locationType)
    'protocol_id',           // Protocol.name
    'constraint_2172d887',  // Software.name
    'psych_trait_id',        // PsychTrait.name
    'role_id',               // Role.name
    'constraint_60b2f84c',  // EconomicMetric.name
    'constraint_9b04054f',  // Campaign.name
    'constraint_f16c28c9',  // Event.name
    'constraint_2c4108aa'   // Control.name
  ]
RETURN count(*) AS e27_constraint_count;
// Expected: 16

// ------------------------------------------------------------
// VERIFICATION 2: List All E27 Constraints by Super Label
// ------------------------------------------------------------

SHOW CONSTRAINTS
YIELD name, type, entityType, labelsOrTypes, properties
WHERE entityType = 'NODE'
  AND labelsOrTypes[0] IN [
    'ThreatActor', 'AttackPattern', 'Vulnerability', 'Malware', 'Indicator',
    'Asset', 'Organization', 'Location', 'Protocol', 'Software',
    'PsychTrait', 'Role', 'EconomicMetric', 'Campaign', 'Event', 'Control'
  ]
  AND type IN ['UNIQUENESS', 'NODE_KEY']
RETURN
  labelsOrTypes[0] AS super_label,
  name AS constraint_name,
  type AS constraint_type,
  properties AS key_properties
ORDER BY super_label, constraint_name;

// ------------------------------------------------------------
// VERIFICATION 3: Identify Missing Constraints
// ------------------------------------------------------------
// Compare expected vs actual constraints

WITH [
  {label: 'ThreatActor', expected_property: 'name'},
  {label: 'AttackPattern', expected_property: 'external_id'},
  {label: 'Vulnerability', expected_property: 'external_id'},
  {label: 'Malware', expected_property: 'name'},
  {label: 'Indicator', expected_property: 'indicator_value'},
  {label: 'Asset', expected_property: 'asset_id'},
  {label: 'Organization', expected_property: 'name'},
  {label: 'Location', expected_property: '(name, locationType)'},
  {label: 'Protocol', expected_property: 'name'},
  {label: 'Software', expected_property: 'name'},
  {label: 'PsychTrait', expected_property: 'name'},
  {label: 'Role', expected_property: 'name'},
  {label: 'EconomicMetric', expected_property: 'name'},
  {label: 'Campaign', expected_property: 'name'},
  {label: 'Event', expected_property: 'name'},
  {label: 'Control', expected_property: 'name'}
] AS expected_constraints
UNWIND expected_constraints AS expected
CALL {
  WITH expected
  SHOW CONSTRAINTS
  YIELD labelsOrTypes, properties
  WHERE labelsOrTypes[0] = expected.label
  RETURN count(*) > 0 AS has_constraint
}
RETURN
  expected.label AS super_label,
  expected.expected_property AS expected_key,
  has_constraint,
  CASE WHEN has_constraint THEN '✅' ELSE '❌' END AS status
ORDER BY super_label;

// ------------------------------------------------------------
// VERIFICATION 4: Check for Index Conflicts
// ------------------------------------------------------------
// List any indexes that might conflict with future constraint operations

SHOW INDEXES
YIELD name, labelsOrTypes, properties, owningConstraint
WHERE owningConstraint IS NULL
  AND labelsOrTypes[0] IN [
    'ThreatActor', 'AttackPattern', 'Vulnerability', 'Malware', 'Indicator',
    'Asset', 'Organization', 'Location', 'Protocol', 'Software',
    'PsychTrait', 'Role', 'EconomicMetric', 'Campaign', 'Event', 'Control'
  ]
RETURN
  labelsOrTypes[0] AS super_label,
  name AS index_name,
  properties AS indexed_properties,
  'Independent (no conflict)' AS status
ORDER BY super_label, index_name;

// ------------------------------------------------------------
// VERIFICATION 5: Constraint Coverage Summary
// ------------------------------------------------------------

MATCH (n)
WHERE n:ThreatActor OR n:AttackPattern OR n:Vulnerability OR n:Malware
   OR n:Indicator OR n:Asset OR n:Organization OR n:Location
   OR n:Protocol OR n:Software OR n:PsychTrait OR n:Role
   OR n:EconomicMetric OR n:Campaign OR n:Event OR n:Control
WITH labels(n)[0] AS super_label
RETURN
  super_label,
  count(*) AS node_count,
  EXISTS {
    SHOW CONSTRAINTS
    YIELD labelsOrTypes
    WHERE labelsOrTypes[0] = super_label
  } AS has_constraint
ORDER BY super_label;
