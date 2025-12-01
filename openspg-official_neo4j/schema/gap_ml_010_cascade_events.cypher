// ============================================
// GAP-ML-010: Cascade Event Tracking Schema
// ============================================
// Purpose: Track cascade event genealogy and propagation dynamics
// Integration: Works with existing Granovetter threshold queries (03_granovetter_threshold.cypher)
// Created: 2025-11-30
// Status: ACTIVE

// ============================================
// STEP 1: Create CascadeEvent Node Type
// ============================================

// Create unique constraint for CascadeEvent ID
CREATE CONSTRAINT cascade_event_id_unique IF NOT EXISTS
FOR (ce:CascadeEvent) REQUIRE ce.id IS UNIQUE;

// Create index for generation tracking (critical for genealogy queries)
CREATE INDEX cascade_event_generation_idx IF NOT EXISTS
FOR (ce:CascadeEvent) ON (ce.generation);

// Create index for timestamp-based queries
CREATE INDEX cascade_event_timestamp_idx IF NOT EXISTS
FOR (ce:CascadeEvent) ON (ce.timestamp);

// Create index for cascade_id grouping
CREATE INDEX cascade_event_cascade_id_idx IF NOT EXISTS
FOR (ce:CascadeEvent) ON (ce.cascade_id);

// Create composite index for velocity calculations
CREATE INDEX cascade_event_cascade_gen_idx IF NOT EXISTS
FOR (ce:CascadeEvent) ON (ce.cascade_id, ce.generation);

// ============================================
// STEP 2: Create TRIGGERED Relationship
// ============================================

// Verify TRIGGERED relationship doesn't exist in schema
// (This query checks if the relationship already exists)
MATCH ()-[r:TRIGGERED]->()
WITH count(r) AS existing_triggered_rels
RETURN
    CASE
        WHEN existing_triggered_rels = 0 THEN 'TRIGGERED relationship is new (safe to add)'
        ELSE 'TRIGGERED relationship exists (check for conflicts): ' + toString(existing_triggered_rels) + ' instances'
    END AS validation_result;

// Note: TRIGGERED relationship will be created dynamically during cascade simulation
// Relationship structure: (parent:CascadeEvent)-[:TRIGGERED {activation_time: datetime}]->(child:CascadeEvent)

// ============================================
// STEP 3: CascadeEvent Properties Schema
// ============================================

// Standard properties for CascadeEvent nodes:
// - id: Unique identifier (STRING, REQUIRED)
// - cascade_id: Group identifier for related cascade events (STRING, REQUIRED)
// - generation: Generation number in cascade tree (INTEGER, REQUIRED)
// - parent_event_id: Parent event ID for genealogy (STRING, NULLABLE)
// - timestamp: Event occurrence time (DATETIME, REQUIRED)
// - actor_id: Associated threat actor ID (STRING, REQUIRED)
// - technique_id: Associated technique ID (STRING, NULLABLE)
// - activation_threshold: Threshold that triggered activation (FLOAT, NULLABLE)
// - neighbor_influence: Fraction of neighbors that influenced (FLOAT, NULLABLE)
// - adopter_count: Number of adopters at this generation (INTEGER, DEFAULT 0)

// ============================================
// STEP 4: Integration with Granovetter Queries
// ============================================

// The existing Granovetter queries (lines 130-220 in 03_granovetter_threshold.cypher) will:
// 1. Create CascadeEvent nodes when actors adopt (ROUND 1 onwards)
// 2. Set parent_event_id to track genealogy
// 3. Create TRIGGERED relationships between parent and child events
// 4. Calculate velocity metrics using generation and timestamp

// Integration points in 03_granovetter_threshold.cypher:
// - Line 140-148: ROUND 1 cascade step -> CREATE CascadeEvent nodes
// - Line 150-171: ROUND 2-10 cascade steps -> CREATE CascadeEvent nodes with parent tracking
// - Line 339-365: Cascade velocity calculation -> USE CascadeEvent generation tracking

// ============================================
// STEP 5: Validation Queries
// ============================================

// Validate schema creation
CALL db.constraints() YIELD name, type
WHERE name CONTAINS 'cascade_event'
RETURN
    'Schema Validation' AS check_name,
    CASE
        WHEN count(*) >= 1 THEN 'PASS: CascadeEvent constraints created'
        ELSE 'FAIL: Missing CascadeEvent constraints'
    END AS result,
    collect(name) AS constraints;

// Validate indexes
CALL db.indexes() YIELD name, type, labelsOrTypes
WHERE 'CascadeEvent' IN labelsOrTypes
RETURN
    'Index Validation' AS check_name,
    CASE
        WHEN count(*) >= 4 THEN 'PASS: CascadeEvent indexes created'
        ELSE 'FAIL: Missing CascadeEvent indexes'
    END AS result,
    count(*) AS index_count,
    collect(name) AS index_names;

// ============================================
// SUMMARY
// ============================================

RETURN
    'GAP-ML-010 Schema Deployment' AS status,
    'CascadeEvent node type and TRIGGERED relationship ready' AS result,
    'Integration with Granovetter queries (03_granovetter_threshold.cypher)' AS integration,
    'Supports genealogy tracking, velocity calculation, and cascade tree queries' AS capabilities;
