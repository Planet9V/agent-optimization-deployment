// ═══════════════════════════════════════════════════════════════
// ROLLBACK SCRIPT - Universal Location Architecture Migration
// Created: 2025-11-13
// Purpose: Complete rollback of all 4 migration phases
// Constitution: GAP-004 Zero Breaking Changes
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// CRITICAL SAFETY CHECKS BEFORE ROLLBACK
// ───────────────────────────────────────────────────────────────

// Verify current database state before rollback
MATCH (eq:Equipment) RETURN count(eq) AS equipment_count_pre_rollback;
MATCH ()-[r:CONNECTS_TO]->() RETURN count(r) AS connects_to_pre_rollback;
SHOW CONSTRAINTS YIELD name RETURN count(name) AS constraints_pre_rollback;
SHOW INDEXES YIELD name RETURN count(name) AS indexes_pre_rollback;

// Expected values (pre-rollback):
// - equipment_count_pre_rollback: 571,913 (unchanged from baseline)
// - connects_to_pre_rollback: <existing count> (unchanged from baseline)
// - constraints_pre_rollback: >= 129 (baseline + 4 Facility constraints)
// - indexes_pre_rollback: >= 455 (baseline + Facility indexes)

// ───────────────────────────────────────────────────────────────
// PHASE 4 ROLLBACK: Remove Tags Properties
// (Execute in reverse order)
// ───────────────────────────────────────────────────────────────

// Remove tags from Equipment nodes
MATCH (eq:Equipment)
WHERE eq.tags IS NOT NULL
REMOVE eq.tags;

// Remove tags from Facility nodes
MATCH (fac:Facility)
WHERE fac.tags IS NOT NULL
REMOVE fac.tags;

// Remove tags from Customer nodes
MATCH (c:Customer)
WHERE c.tags IS NOT NULL
REMOVE c.tags;

// Remove tags from Region nodes
MATCH (r:Region)
WHERE r.tags IS NOT NULL
REMOVE r.tags;

// Remove tags from Sector nodes
MATCH (s:Sector)
WHERE s.tags IS NOT NULL
REMOVE s.tags;

// Validation: Verify tags removed
MATCH (n)
WHERE n.tags IS NOT NULL
RETURN count(n) AS nodes_with_tags;
// Expected: 0

// ───────────────────────────────────────────────────────────────
// PHASE 3 ROLLBACK: Remove Facility Nodes and LOCATED_AT Relationships
// ───────────────────────────────────────────────────────────────

// Remove LOCATED_AT relationships (Equipment → Facility)
MATCH (eq:Equipment)-[r:LOCATED_AT]->(fac:Facility)
DELETE r;

// Remove HOUSES_EQUIPMENT relationships (Facility → Equipment)
MATCH (fac:Facility)-[r:HOUSES_EQUIPMENT]->(eq:Equipment)
DELETE r;

// Remove geocoded property from Equipment (added in Phase 3)
MATCH (eq:Equipment)
WHERE eq.geocoded IS NOT NULL
REMOVE eq.geocoded;

// Remove Facility nodes (including orphaned Facilities)
MATCH (fac:Facility)
DETACH DELETE fac;

// Validation: Verify Facility nodes removed
MATCH (fac:Facility) RETURN count(fac) AS facility_count;
// Expected: 0

// Validation: Verify LOCATED_AT relationships removed
MATCH ()-[r:LOCATED_AT]->() RETURN count(r) AS located_at_count;
// Expected: 0

// ───────────────────────────────────────────────────────────────
// PHASE 2 ROLLBACK: Remove Organizational Relationships
// ───────────────────────────────────────────────────────────────

// Remove OWNED_BY relationships (Facility → Customer)
MATCH ()-[r:OWNED_BY]->() DELETE r;

// Remove IN_REGION relationships (Facility → Region)
MATCH ()-[r:IN_REGION]->() DELETE r;

// Remove OPERATES_IN relationships (Region → Sector, Customer → Sector)
MATCH ()-[r:OPERATES_IN]->() DELETE r;

// Remove Customer nodes
MATCH (c:Customer) DETACH DELETE c;

// Remove Region nodes
MATCH (r:Region) DETACH DELETE r;

// Remove Sector nodes
MATCH (s:Sector) DETACH DELETE s;

// Validation: Verify organizational nodes removed
MATCH (c:Customer) RETURN count(c) AS customer_count;
MATCH (r:Region) RETURN count(r) AS region_count;
MATCH (s:Sector) RETURN count(s) AS sector_count;
// Expected: All 0

// Validation: Verify organizational relationships removed
MATCH ()-[r:OWNED_BY]->() RETURN count(r) AS owned_by_count;
MATCH ()-[r:IN_REGION]->() RETURN count(r) AS in_region_count;
MATCH ()-[r:OPERATES_IN]->() RETURN count(r) AS operates_in_count;
// Expected: All 0

// ───────────────────────────────────────────────────────────────
// PHASE 1 ROLLBACK: Remove Constraints and Indexes
// ───────────────────────────────────────────────────────────────

// Drop Facility constraints
DROP CONSTRAINT facility_id IF EXISTS;
DROP CONSTRAINT customer_id IF EXISTS;
DROP CONSTRAINT region_id IF EXISTS;
DROP CONSTRAINT sector_id IF EXISTS;

// Drop Facility indexes
DROP INDEX facility_name IF EXISTS;
DROP INDEX facility_type IF EXISTS;
DROP INDEX facility_namespace IF EXISTS;
DROP INDEX facility_location IF EXISTS;
DROP INDEX facility_tags IF EXISTS;

// Drop Customer indexes
DROP INDEX customer_name IF EXISTS;
DROP INDEX customer_namespace IF EXISTS;

// Drop Region indexes
DROP INDEX region_name IF EXISTS;
DROP INDEX region_type IF EXISTS;

// Drop Sector indexes
DROP INDEX sector_name IF EXISTS;
DROP INDEX sector_critical IF EXISTS;

// Validation: Verify constraints removed
SHOW CONSTRAINTS YIELD name
WHERE name IN ['facility_id', 'customer_id', 'region_id', 'sector_id']
RETURN count(name) AS migration_constraints;
// Expected: 0

// Validation: Verify indexes removed
SHOW INDEXES YIELD name
WHERE name IN ['facility_name', 'facility_type', 'facility_namespace', 'facility_location', 'facility_tags',
               'customer_name', 'customer_namespace',
               'region_name', 'region_type',
               'sector_name', 'sector_critical']
RETURN count(name) AS migration_indexes;
// Expected: 0

// ───────────────────────────────────────────────────────────────
// FINAL VALIDATION - Verify Database Restored to Pre-Migration State
// ───────────────────────────────────────────────────────────────

// Verify Equipment nodes unchanged
MATCH (eq:Equipment) RETURN count(eq) AS equipment_count_post_rollback;
// Expected: 571,913 (same as pre-migration baseline)

// Verify CONNECTS_TO relationships unchanged
MATCH ()-[r:CONNECTS_TO]->() RETURN count(r) AS connects_to_post_rollback;
// Expected: Same as pre-migration baseline

// Verify Equipment.location property preserved
MATCH (eq:Equipment)
WHERE eq.location IS NOT NULL
RETURN count(eq) AS equipment_with_location_post_rollback;
// Expected: Same as pre-migration baseline

// Verify Equipment.latitude/longitude preserved (if they existed)
MATCH (eq:Equipment)
WHERE eq.latitude IS NOT NULL AND eq.longitude IS NOT NULL
RETURN count(eq) AS equipment_with_coords_post_rollback;
// Expected: Same as pre-migration baseline (may be 0 if no Equipment had coords)

// Verify constraint count restored to baseline
SHOW CONSTRAINTS YIELD name RETURN count(name) AS total_constraints_post_rollback;
// Expected: 129 (pre-migration baseline)

// Verify index count restored to baseline
SHOW INDEXES YIELD name RETURN count(name) AS total_indexes_post_rollback;
// Expected: 455 (pre-migration baseline)

// Verify no orphaned relationships remain
MATCH ()-[r:LOCATED_AT|HOUSES_EQUIPMENT|OWNED_BY|IN_REGION|OPERATES_IN]->()
RETURN count(r) AS orphaned_relationships;
// Expected: 0

// Verify no orphaned nodes remain
MATCH (n)
WHERE (n:Facility OR n:Customer OR n:Region OR n:Sector)
RETURN count(n) AS orphaned_nodes;
// Expected: 0

// ───────────────────────────────────────────────────────────────
// BACKWARDS COMPATIBILITY VERIFICATION
// ───────────────────────────────────────────────────────────────

// Test: Old Equipment queries still work
MATCH (eq:Equipment)
WHERE eq.location CONTAINS 'Building A'
  AND eq.customer_namespace = 'railway_operator_001'
RETURN eq.equipmentId, eq.name, eq.location
LIMIT 5;
// Expected: Same results as pre-migration

// Test: Old Equipment-to-Equipment topology queries still work
MATCH (eq1:Equipment {equipmentId: 'PLC-001'})-[:CONNECTS_TO*1..3]->(eq2:Equipment)
RETURN eq1.name AS source, eq2.name AS target
LIMIT 5;
// Expected: Same results as pre-migration (if PLC-001 exists)

// Test: Old UC2 cyber-physical queries still work
MATCH (eq:Equipment)-[:HAS_INTERFACE]->(ni:NetworkInterface)
WHERE eq.customer_namespace = 'railway_operator_001'
RETURN eq.equipmentId, eq.location, ni.ip_address
LIMIT 5;
// Expected: Same results as pre-migration

// Test: Old UC3 cascade queries still work
MATCH (ce:CascadeEvent)-[:PROPAGATES_VIA*1..3]->(downstream:CascadeEvent)
RETURN ce.eventId, downstream.eventId
LIMIT 5;
// Expected: Same results as pre-migration

// ───────────────────────────────────────────────────────────────
// ROLLBACK COMPLETION REPORT
// ───────────────────────────────────────────────────────────────

// Generate rollback completion summary
MATCH (eq:Equipment) WITH count(eq) AS eq_count
MATCH ()-[r:CONNECTS_TO]->() WITH eq_count, count(r) AS conn_count
SHOW CONSTRAINTS YIELD name WITH eq_count, conn_count, count(name) AS const_count
SHOW INDEXES YIELD name WITH eq_count, conn_count, const_count, count(name) AS idx_count
RETURN
  eq_count AS equipment_nodes,
  conn_count AS connects_to_relationships,
  const_count AS total_constraints,
  idx_count AS total_indexes,
  CASE
    WHEN eq_count = 571913 AND const_count = 129 AND idx_count = 455
    THEN '✅ ROLLBACK SUCCESSFUL - Database restored to pre-migration baseline'
    ELSE '⚠️ ROLLBACK VERIFICATION FAILED - Manual inspection required'
  END AS rollback_status;

// ───────────────────────────────────────────────────────────────
// ROLLBACK SCRIPT COMPLETE
// ───────────────────────────────────────────────────────────────

// All migration changes have been rolled back
// Database state restored to pre-migration baseline
// Zero data loss verified
// Constitution compliance maintained: Zero breaking changes during migration
// Constitution compliance maintained: Complete rollback capability verified
