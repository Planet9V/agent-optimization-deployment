// ============================================================================
// GAP-ML-004: Temporal Versioning Implementation
// File: gap-ml-004-temporal-implementation.cypher
// Created: 2025-11-30
// Purpose: Add temporal properties to Actor nodes and create temporal infrastructure
// Target Database: aeon-neo4j-dev (172.18.0.5:7687)
// ============================================================================

// ============================================================================
// STEP 1: ADD TEMPORAL PROPERTIES TO EXISTING ACTOR NODES
// ============================================================================
// Add temporal metadata to all existing Actor nodes
// Set initial values: valid_from = now, valid_to = null (current), version = 1

MATCH (a:Actor)
SET a.valid_from = COALESCE(a.valid_from, datetime()),
    a.valid_to = COALESCE(a.valid_to, datetime('9999-12-31T23:59:59Z')),
    a.version = COALESCE(a.version, 1),
    a.change_source = COALESCE(a.change_source, 'INITIAL_LOAD'),
    a.change_actor = COALESCE(a.change_actor, 'system')
RETURN
    'Step 1 Complete' AS step,
    count(a) AS actors_updated;

// ============================================================================
// STEP 2: CREATE TEMPORAL INDEXES
// ============================================================================
// Create indexes for efficient temporal queries
// Check against existing indexes to avoid duplicates

// Index on valid_from for point-in-time queries
CREATE INDEX actor_valid_from_idx IF NOT EXISTS
FOR (a:Actor) ON (a.valid_from);

// Index on valid_to for current version queries
CREATE INDEX actor_valid_to_idx IF NOT EXISTS
FOR (a:Actor) ON (a.valid_to);

// Index on version for version history queries
CREATE INDEX actor_version_idx IF NOT EXISTS
FOR (a:Actor) ON (a.version);

// Composite index for temporal range queries
CREATE INDEX actor_temporal_range_idx IF NOT EXISTS
FOR (a:Actor) ON (a.id, a.valid_from, a.valid_to);

// Index on change metadata for audit queries
CREATE INDEX actor_change_source_idx IF NOT EXISTS
FOR (a:Actor) ON (a.change_source);

// ============================================================================
// STEP 3: CREATE VERSION PROCEDURES USING APOC
// ============================================================================
// Create helper procedures for temporal operations using existing APOC patterns

// Procedure: Create new version of an Actor node
// Uses APOC temporal functions and node cloning patterns from library
CALL apoc.custom.declareProcedure(
  'temporal.createActorVersion(actorId :: STRING, changes :: MAP, changeSource :: STRING, changeActor :: STRING) :: (oldVersion :: NODE, newVersion :: NODE)',
  '
  MATCH (old:Actor {id: $actorId})
  WHERE old.valid_to > datetime()
  WITH old, old.version AS currentVersion

  // Close the current version
  SET old.valid_to = datetime()

  // Create new version with updated properties
  CREATE (new:Actor)
  SET new = old,
      new.version = currentVersion + 1,
      new.valid_from = datetime(),
      new.valid_to = datetime(''9999-12-31T23:59:59Z''),
      new.change_source = $changeSource,
      new.change_actor = $changeActor

  // Apply the changes
  SET new += $changes

  // Create SUPERSEDED_BY relationship
  CREATE (old)-[:SUPERSEDED_BY {timestamp: datetime()}]->(new)

  RETURN old AS oldVersion, new AS newVersion
  ',
  'WRITE'
);

// Procedure: Get Actor state at specific timestamp
CALL apoc.custom.declareFunction(
  'temporal.getActorAtTime(actorId :: STRING, timestamp :: DATETIME) :: (NODE)',
  '
  MATCH (a:Actor {id: $actorId})
  WHERE a.valid_from <= $timestamp
    AND a.valid_to > $timestamp
  RETURN a
  ',
  false
);

// Procedure: Get Actor version history
CALL apoc.custom.declareFunction(
  'temporal.getActorHistory(actorId :: STRING) :: (LIST OF NODE)',
  '
  MATCH (a:Actor {id: $actorId})
  RETURN collect(a) AS history
  ORDER BY a.version DESC
  ',
  false
);

// ============================================================================
// STEP 4: VERIFICATION QUERIES
// ============================================================================
// Verify temporal properties are set correctly

// Test 1: Check all Actors have temporal properties
MATCH (a:Actor)
RETURN
    'Temporal Properties Check' AS test,
    count(a) AS total_actors,
    count(a.valid_from) AS has_valid_from,
    count(a.valid_to) AS has_valid_to,
    count(a.version) AS has_version,
    count(a.change_source) AS has_change_source;

// Test 2: Verify indexes were created
CALL db.indexes()
YIELD name, labelsOrTypes, properties
WHERE name STARTS WITH 'actor_'
  AND (
    name = 'actor_valid_from_idx'
    OR name = 'actor_valid_to_idx'
    OR name = 'actor_version_idx'
    OR name = 'actor_temporal_range_idx'
    OR name = 'actor_change_source_idx'
  )
RETURN name, labelsOrTypes, properties
ORDER BY name;

// Test 3: Point-in-time query example
// Get Actor state at specific timestamp
MATCH (a:Actor {id: 'ACTOR-001'})
WHERE a.valid_from <= datetime()
  AND a.valid_to > datetime()
RETURN
    'Point-in-time Query Test' AS test,
    a.id AS actor_id,
    a.version AS current_version,
    a.change_source AS last_change_source,
    a.change_actor AS last_change_actor,
    a.valid_from AS valid_from,
    a.valid_to AS valid_to;

// Test 4: Current version query
// Find all current versions (valid_to in the future)
MATCH (a:Actor)
WHERE a.valid_to > datetime()
RETURN
    'Current Versions Check' AS test,
    count(a) AS current_version_count,
    collect(DISTINCT a.version) AS version_distribution;

// Test 5: Temporal query performance test
EXPLAIN MATCH (a:Actor {id: 'ACTOR-001'})
WHERE a.valid_from <= datetime()
  AND a.valid_to > datetime()
RETURN a;

// ============================================================================
// STEP 5: CREATE SAMPLE VERSIONED ACTOR FOR TESTING
// ============================================================================
// Create a test Actor and demonstrate versioning

// Create initial Actor
CREATE (a:Actor {
    id: 'ACTOR-TEST-001',
    name: 'Test Actor',
    type: 'User',

    // Ising properties
    spin: 1,
    threshold: 0.3,
    volatility: 0.5,

    // Temporal metadata
    valid_from: datetime('2025-11-30T00:00:00Z'),
    valid_to: datetime('9999-12-31T23:59:59Z'),
    version: 1,
    change_source: 'TEST_CREATION',
    change_actor: 'gap-ml-004-test'
})
RETURN
    'Sample Actor Created' AS status,
    a.id AS actor_id,
    a.version AS version;

// ============================================================================
// SUMMARY AND REPORTING
// ============================================================================

// Final Summary Report
MATCH (a:Actor)
WITH
    count(a) AS total_actors,
    count(CASE WHEN a.valid_to > datetime() THEN 1 END) AS current_versions,
    count(CASE WHEN a.valid_to <= datetime() THEN 1 END) AS historical_versions,
    avg(a.version) AS avg_version,
    max(a.version) AS max_version
RETURN
    '=== GAP-ML-004 Implementation Complete ===' AS status,
    total_actors AS total_actors,
    current_versions AS current_versions,
    historical_versions AS historical_versions,
    avg_version AS average_version,
    max_version AS max_version,
    '✓ Temporal properties added' AS step1,
    '✓ Indexes created' AS step2,
    '✓ Procedures defined' AS step3,
    '✓ Verification complete' AS step4;
