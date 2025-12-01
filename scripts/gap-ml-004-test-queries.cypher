// ============================================================================
// GAP-ML-004: Temporal Versioning Test Queries
// File: gap-ml-004-test-queries.cypher
// Created: 2025-11-30
// Purpose: Test temporal versioning functionality
// ============================================================================

// ============================================================================
// TEST 1: Point-in-time Query
// ============================================================================
// Get Actor state at specific timestamp
// Expected: Should return the version valid at that time

MATCH (a:Actor {id: $actor_id})
WHERE a.valid_from <= $timestamp
  AND a.valid_to > $timestamp
RETURN
    'Point-in-time Query' AS test,
    a.id AS actor_id,
    a.version AS version,
    a.name AS name,
    a.spin AS spin,
    a.threshold AS threshold,
    a.change_source AS change_source,
    a.change_actor AS change_actor,
    a.valid_from AS valid_from,
    a.valid_to AS valid_to;

// Example usage with parameters:
// :param actor_id => 'ACTOR-001'
// :param timestamp => datetime('2025-11-30T12:00:00Z')

// ============================================================================
// TEST 2: Version History Query
// ============================================================================
// Get all versions of an Actor ordered by version number

MATCH (a:Actor {id: $actor_id})
RETURN
    'Version History' AS test,
    a.id AS actor_id,
    a.version AS version,
    a.valid_from AS valid_from,
    a.valid_to AS valid_to,
    a.change_source AS change_source,
    a.change_actor AS change_actor
ORDER BY a.version DESC;

// Example usage:
// :param actor_id => 'ACTOR-001'

// ============================================================================
// TEST 3: Current Version Query
// ============================================================================
// Get only the current (active) version of an Actor

MATCH (a:Actor {id: $actor_id})
WHERE a.valid_to > datetime()
RETURN
    'Current Version' AS test,
    a.id AS actor_id,
    a.version AS current_version,
    a.name AS name,
    a.spin AS current_spin,
    a.threshold AS current_threshold,
    a.valid_from AS became_active,
    a.change_source AS last_change;

// ============================================================================
// TEST 4: Version Chain Query
// ============================================================================
// Follow SUPERSEDED_BY relationships to see version chain

MATCH path = (a1:Actor {id: $actor_id})-[:SUPERSEDED_BY*0..10]->(a2:Actor)
WHERE a1.version = 1
RETURN
    'Version Chain' AS test,
    [node IN nodes(path) | {
        version: node.version,
        valid_from: node.valid_from,
        valid_to: node.valid_to,
        change_source: node.change_source
    }] AS version_history,
    length(path) AS versions_count;

// ============================================================================
// TEST 5: Temporal Range Query
// ============================================================================
// Find all Actors that were active during a specific time range

MATCH (a:Actor)
WHERE a.valid_from < $end_time
  AND a.valid_to > $start_time
RETURN
    'Temporal Range Query' AS test,
    a.id AS actor_id,
    a.version AS version,
    a.valid_from AS valid_from,
    a.valid_to AS valid_to
ORDER BY a.id, a.version;

// Example usage:
// :param start_time => datetime('2025-11-01T00:00:00Z')
// :param end_time => datetime('2025-11-30T23:59:59Z')

// ============================================================================
// TEST 6: Change Audit Query
// ============================================================================
// Find all changes made by a specific actor or source

MATCH (a:Actor)
WHERE a.change_actor = $change_actor
  OR a.change_source = $change_source
RETURN
    'Change Audit' AS test,
    a.id AS actor_id,
    a.version AS version,
    a.change_source AS source,
    a.change_actor AS actor,
    a.valid_from AS change_timestamp
ORDER BY a.valid_from DESC;

// Example usage:
// :param change_actor => 'granovetter_cascade_engine'
// :param change_source => 'CASCADE_ACTIVATION'

// ============================================================================
// TEST 7: Compare Versions Query
// ============================================================================
// Compare two versions of the same Actor to see what changed

MATCH (old:Actor {id: $actor_id, version: $old_version})
MATCH (new:Actor {id: $actor_id, version: $new_version})
RETURN
    'Version Comparison' AS test,
    old.id AS actor_id,
    {
        version: old.version,
        spin: old.spin,
        threshold: old.threshold,
        valid_from: old.valid_from,
        valid_to: old.valid_to
    } AS old_version,
    {
        version: new.version,
        spin: new.spin,
        threshold: new.threshold,
        valid_from: new.valid_from,
        valid_to: new.valid_to
    } AS new_version,
    {
        spin_changed: old.spin <> new.spin,
        threshold_changed: old.threshold <> new.threshold,
        change_source: new.change_source,
        change_actor: new.change_actor
    } AS changes;

// Example usage:
// :param actor_id => 'ACTOR-001'
// :param old_version => 1
// :param new_version => 2

// ============================================================================
// TEST 8: Active Versions Count
// ============================================================================
// Count how many Actors have multiple versions

MATCH (a:Actor)
WITH a.id AS actor_id, count(*) AS version_count
WHERE version_count > 1
RETURN
    'Multiple Versions Analysis' AS test,
    count(actor_id) AS actors_with_multiple_versions,
    avg(version_count) AS avg_versions_per_actor,
    max(version_count) AS max_versions;

// ============================================================================
// TEST 9: Performance Test - Temporal Query
// ============================================================================
// Test query performance with EXPLAIN

EXPLAIN MATCH (a:Actor {id: $actor_id})
WHERE a.valid_from <= datetime()
  AND a.valid_to > datetime()
RETURN a.id, a.version, a.spin;

// ============================================================================
// TEST 10: Consistency Check
// ============================================================================
// Verify temporal data consistency
// - No gaps in time coverage
// - No overlapping valid ranges
// - Version numbers are sequential

MATCH (a:Actor)
WITH a.id AS actor_id, collect(a) AS versions
UNWIND range(0, size(versions)-2) AS i
WITH
    actor_id,
    versions[i] AS current_version,
    versions[i+1] AS next_version
WHERE current_version.valid_to <> next_version.valid_from
RETURN
    'Consistency Check' AS test,
    actor_id,
    'Temporal gap or overlap detected' AS issue,
    current_version.version AS version1,
    current_version.valid_to AS version1_end,
    next_version.version AS version2,
    next_version.valid_from AS version2_start;
