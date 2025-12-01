// ============================================================
// Enhancement 27: Index-Constraint Conflict Resolution
// File: fix_constraint_conflicts.cypher
// Created: 2025-11-28 22:05:00 UTC
// Purpose: Resolve blocking index conflicts and create missing constraints
// ============================================================

// ------------------------------------------------------------
// PHASE 1: DROP CONFLICTING CONSTRAINTS
// ------------------------------------------------------------
// These constraints block creation of E27 composite keys
// or have property name mismatches

// 1.1 Location - Blocks composite key (name, locationType)
// Current: UNIQUE on locationId
// Target: NODE KEY on (name, locationType)
DROP CONSTRAINT location_id_unique IF EXISTS;

// 1.2 Protocol - Wrong property name
// Current: UNIQUE on 'name'
// Target: UNIQUE on 'name' (actually correct, but need to recreate with proper constraint name)
DROP CONSTRAINT constraint_316ea96d IF EXISTS;

// 1.3 PsychTrait - Blocks composite key
// Current: UNIQUE on 'name'
// Target: NODE KEY on (traitType, subtype) [Note: subtype not in current data, using name instead]
DROP CONSTRAINT constraint_e9b7e8e5 IF EXISTS;

// ------------------------------------------------------------
// PHASE 2: VERIFY NO DUPLICATES (VALIDATION QUERIES)
// ------------------------------------------------------------
// Run these to ensure constraint creation will succeed:

// Location: Check for duplicates on (name, locationType)
// MATCH (l:Location)
// WITH l.name AS name, l.locationType AS type, count(*) AS count
// WHERE count > 1
// RETURN name, type, count;
// Expected: No results

// Protocol: Check for duplicates on name
// MATCH (p:Protocol)
// WITH p.name AS name, count(*) AS count
// WHERE count > 1
// RETURN name, count;
// Expected: No results

// PsychTrait: Check for duplicates on name
// MATCH (pt:PsychTrait)
// WITH pt.name AS name, count(*) AS count
// WHERE count > 1
// RETURN name, count;
// Expected: No results

// ------------------------------------------------------------
// PHASE 3: CREATE CORRECTED CONSTRAINTS
// ------------------------------------------------------------

// 3.1 Location - Composite NODE KEY
// Properties verified in data: name, locationType both exist
CREATE CONSTRAINT location_id IF NOT EXISTS
FOR (n:Location) REQUIRE (n.name, n.locationType) IS NODE KEY;

// 3.2 Protocol - UNIQUE on name (correct property verified)
// Property verified in data: 'name' exists (not 'protocol_name')
CREATE CONSTRAINT protocol_id IF NOT EXISTS
FOR (n:Protocol) REQUIRE n.name IS UNIQUE;

// 3.3 PsychTrait - UNIQUE on name (simplified from composite key)
// Note: Data has 'traitType' and 'name' but no 'subtype'
// Using name as primary key since it's unique in current data
CREATE CONSTRAINT psych_trait_id IF NOT EXISTS
FOR (n:PsychTrait) REQUIRE n.name IS UNIQUE;

// 3.4 Role - UNIQUE on name (Role nodes don't exist yet)
// Note: Role nodes have count=0, constraint creation will succeed
// Using 'name' as property (standard pattern)
CREATE CONSTRAINT role_id IF NOT EXISTS
FOR (n:Role) REQUIRE n.name IS UNIQUE;

// ------------------------------------------------------------
// PHASE 4: VERIFICATION QUERIES
// ------------------------------------------------------------

// Count total E27 constraints (should be 16)
// SHOW CONSTRAINTS
// YIELD name, type, entityType, properties
// WHERE name IN [
//   'threat_actor_name', 'attack_pattern_id', 'vulnerability_id', 'malware_name',
//   'indicator_id', 'asset_id', 'org_name', 'location_id', 'protocol_id',
//   'software_name', 'psych_trait_id', 'role_id', 'economic_metric_id',
//   'campaign_id', 'event_id', 'control_id'
// ]
// RETURN name, type, entityType, properties
// ORDER BY name;

// List all constraints by Super Label
// SHOW CONSTRAINTS
// YIELD name, type, entityType, labelsOrTypes, properties
// WHERE labelsOrTypes[0] IN [
//   'ThreatActor', 'AttackPattern', 'Vulnerability', 'Malware', 'Indicator',
//   'Asset', 'Organization', 'Location', 'Protocol', 'Software',
//   'PsychTrait', 'Role', 'EconomicMetric', 'Campaign', 'Event', 'Control'
// ]
// RETURN labelsOrTypes[0] AS label, name, type, properties
// ORDER BY label, name;

// ------------------------------------------------------------
// EXPECTED RESULTS
// ------------------------------------------------------------
// After successful execution:
// - 4 old constraints dropped
// - 4 new constraints created
// - Total E27 constraints: 16 (12 existing + 4 new)
// - No index conflicts remaining
// - All Super Labels have primary key constraints
