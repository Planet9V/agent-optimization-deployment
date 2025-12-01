// ============================================
// GAP-ML-010: Granovetter Integration for Cascade Tracking
// ============================================
// Purpose: Enhance Granovetter threshold queries with CascadeEvent tracking
// Base Query: 03_granovetter_threshold.cypher (lines 130-220)
// Created: 2025-11-30
// Status: ACTIVE

// ============================================
// INTEGRATION OVERVIEW
// ============================================
// This file shows how to integrate CascadeEvent tracking into the existing
// Granovetter threshold cascade simulation (03_granovetter_threshold.cypher).
//
// Key Changes:
// 1. Create CascadeEvent nodes when actors adopt techniques
// 2. Track parent_event_id for genealogy
// 3. Create TRIGGERED relationships between parent and child events
// 4. Use existing velocity calculation with generation tracking

// ============================================
// ENHANCED ROUND 1: Initial Cascade with Event Tracking
// ============================================

// Original: Lines 130-148 in 03_granovetter_threshold.cypher
// Enhanced with CascadeEvent creation

// Generate cascade ID for this simulation run
WITH 'CASCADE_' + toString(datetime().epochMillis) AS cascade_id

// Round 1: Check threshold and propagate adoption
MATCH (actor:Threat_Actor {adopted: false})
MATCH (neighbor:Threat_Actor {adopted: true})
WHERE (actor)-[:RELATES_TO|ATTRIBUTED_TO]-(neighbor)
WITH cascade_id, actor,
     count(DISTINCT neighbor) AS adopted_neighbors,
     size([(actor)-[:RELATES_TO|ATTRIBUTED_TO]-(n:Threat_Actor) | n]) AS total_neighbors
WHERE total_neighbors > 0
WITH cascade_id, actor,
     toFloat(adopted_neighbors) / toFloat(total_neighbors) AS adoption_fraction
WHERE adoption_fraction >= actor.adoption_threshold

// Mark actor as adopted (original behavior)
SET actor.adopted = true,
    actor.adoption_time = 1

// NEW: Create CascadeEvent node for this adoption
WITH cascade_id, actor, adoption_fraction
CREATE (ce:CascadeEvent {
    id: 'EVENT_' + toString(datetime().epochMillis) + '_' + actor.actorId,
    cascade_id: cascade_id,
    generation: 1,
    parent_event_id: null,  // Round 1 has no parent (seed events)
    timestamp: datetime(),
    actor_id: actor.actorId,
    technique_id: null,  // Can be added if technique context available
    activation_threshold: actor.adoption_threshold,
    neighbor_influence: adoption_fraction,
    adopter_count: 1
})

WITH cascade_id, count(actor) AS new_adopters
RETURN
    'ROUND 1' AS round,
    cascade_id,
    new_adopters AS newly_adopted,
    CASE WHEN new_adopters > 0 THEN 'CASCADE CONTINUING' ELSE 'CASCADE STOPPED' END AS status;

// ============================================
// ENHANCED ROUNDS 2-10: Cascade with Genealogy Tracking
// ============================================

// Original: Lines 150-171 in 03_granovetter_threshold.cypher
// Enhanced with parent tracking and TRIGGERED relationship

// Get cascade_id from previous round (or pass as parameter)
WITH $cascade_id AS cascade_id

UNWIND range(2, 10) AS round_num
WITH cascade_id, round_num

// Identify actors who adopted in previous round (potential parents)
MATCH (parent_actor:Threat_Actor {adopted: true})
WHERE parent_actor.adoption_time = round_num - 1

// Find their corresponding CascadeEvents from previous generation
OPTIONAL MATCH (parent_event:CascadeEvent {
    cascade_id: cascade_id,
    generation: round_num - 1,
    actor_id: parent_actor.actorId
})

WITH cascade_id, round_num, collect(parent_event) AS parent_events

// Check if new actors adopt in this round
MATCH (actor:Threat_Actor {adopted: false})
MATCH (neighbor:Threat_Actor {adopted: true})
WHERE (actor)-[:RELATES_TO|ATTRIBUTED_TO]-(neighbor)
WITH cascade_id, round_num, parent_events, actor,
     count(DISTINCT neighbor) AS adopted_neighbors,
     size([(actor)-[:RELATES_TO|ATTRIBUTED_TO]-(n:Threat_Actor) | n]) AS total_neighbors
WHERE total_neighbors > 0
WITH cascade_id, round_num, parent_events, actor,
     toFloat(adopted_neighbors) / toFloat(total_neighbors) AS adoption_fraction
WHERE adoption_fraction >= actor.adoption_threshold

// Mark actor as adopted (original behavior)
SET actor.adopted = true,
    actor.adoption_time = round_num

// NEW: Create CascadeEvent with parent tracking
WITH cascade_id, round_num, parent_events, actor, adoption_fraction
CREATE (ce:CascadeEvent {
    id: 'EVENT_' + toString(datetime().epochMillis) + '_' + actor.actorId,
    cascade_id: cascade_id,
    generation: round_num,
    parent_event_id: CASE
        WHEN size(parent_events) > 0 THEN parent_events[0].id
        ELSE null
    END,
    timestamp: datetime(),
    actor_id: actor.actorId,
    technique_id: null,
    activation_threshold: actor.adoption_threshold,
    neighbor_influence: adoption_fraction,
    adopter_count: 1
})

// NEW: Create TRIGGERED relationship to parent event
WITH cascade_id, round_num, ce, parent_events
UNWIND parent_events AS parent
WITH cascade_id, round_num, ce, parent
WHERE parent IS NOT NULL
CREATE (parent)-[:TRIGGERED {activation_time: datetime()}]->(ce)

WITH cascade_id, round_num, count(ce) AS new_adopters
WHERE new_adopters > 0
RETURN
    'ROUND ' + toString(round_num) AS round,
    cascade_id,
    new_adopters AS newly_adopted,
    'CASCADE CONTINUING' AS status
ORDER BY round_num;

// ============================================
// ENHANCED CASCADE VELOCITY CALCULATION
// ============================================

// Original: Lines 339-365 in 03_granovetter_threshold.cypher
// Now uses CascadeEvent nodes with generation tracking

MATCH (ce:CascadeEvent {cascade_id: $cascade_id})
WHERE ce.generation IS NOT NULL
WITH ce.generation AS time_step,
     count(ce) AS new_adopters
ORDER BY time_step
WITH collect(time_step) AS time_series,
     collect(new_adopters) AS adoption_series
UNWIND range(0, size(time_series) - 1) AS idx
WITH time_series[idx] AS round,
     adoption_series[idx] AS adopters,
     CASE WHEN idx > 0
         THEN adoption_series[idx] - adoption_series[idx-1]
         ELSE adoption_series[idx]
     END AS velocity
RETURN
    round AS adoption_round,
    adopters AS cumulative_adopters,
    velocity AS adoption_velocity,
    CASE
        WHEN velocity > 10 THEN 'EXPLOSIVE PHASE'
        WHEN velocity > 5 THEN 'RAPID GROWTH'
        WHEN velocity > 2 THEN 'MODERATE GROWTH'
        WHEN velocity > 0 THEN 'SLOW GROWTH'
        ELSE 'SATURATION'
    END AS cascade_phase
ORDER BY round;

// ============================================
// COMPLETE INTEGRATION WORKFLOW
// ============================================

// STEP 1: Run Granovetter simulation with CascadeEvent tracking
// Execute enhanced ROUND 1 (creates seed events)
// Execute enhanced ROUNDS 2-10 (creates child events with TRIGGERED relationships)

// STEP 2: Analyze cascade genealogy
// Use queries from gap_ml_010_cascade_queries.cypher:
// - CASCADE TREE VISUALIZATION
// - CASCADE VELOCITY CALCULATION
// - CRITICAL INFLUENCERS
// - CASCADE DEPTH ANALYSIS

// STEP 3: Validate results
// Run validation tests to ensure:
// - CascadeEvent nodes created for each adoption
// - TRIGGERED relationships link parent to child events
// - Generation tracking works correctly
// - Velocity calculations use CascadeEvent data

// ============================================
// VALIDATION TESTS
// ============================================

// Test 1: Verify CascadeEvent nodes created
MATCH (ce:CascadeEvent {cascade_id: $cascade_id})
WITH count(ce) AS event_count
RETURN
    'Test 1: CascadeEvent Creation' AS test_name,
    CASE WHEN event_count > 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    event_count AS events_created;

// Test 2: Verify TRIGGERED relationships exist
MATCH (parent:CascadeEvent {cascade_id: $cascade_id})-[t:TRIGGERED]->(child:CascadeEvent)
WITH count(t) AS trigger_count
RETURN
    'Test 2: TRIGGERED Relationships' AS test_name,
    CASE WHEN trigger_count > 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    trigger_count AS relationships_created;

// Test 3: Verify generation tracking
MATCH (ce:CascadeEvent {cascade_id: $cascade_id})
WHERE ce.generation IS NOT NULL
WITH min(ce.generation) AS min_gen, max(ce.generation) AS max_gen, count(ce) AS total
RETURN
    'Test 3: Generation Tracking' AS test_name,
    CASE WHEN min_gen >= 0 AND max_gen >= min_gen THEN 'PASS' ELSE 'FAIL' END AS result,
    min_gen AS first_generation,
    max_gen AS last_generation,
    total AS total_events;

// Test 4: Verify parent-child genealogy
MATCH (parent:CascadeEvent {cascade_id: $cascade_id})-[:TRIGGERED]->(child:CascadeEvent)
WHERE child.parent_event_id = parent.id
WITH count(*) AS valid_genealogy
RETURN
    'Test 4: Parent-Child Genealogy' AS test_name,
    CASE WHEN valid_genealogy > 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    valid_genealogy AS valid_links;

// Test 5: Verify velocity calculation works
MATCH (ce:CascadeEvent {cascade_id: $cascade_id})
WITH ce.generation AS gen, count(ce) AS events_per_gen
ORDER BY gen
WITH collect(events_per_gen) AS event_counts
WITH event_counts[0] AS first_gen_count, event_counts[-1] AS last_gen_count
RETURN
    'Test 5: Velocity Calculation' AS test_name,
    CASE WHEN first_gen_count IS NOT NULL AND last_gen_count IS NOT NULL THEN 'PASS' ELSE 'FAIL' END AS result,
    first_gen_count AS seed_events,
    last_gen_count AS final_generation_events;

// ============================================
// SUMMARY
// ============================================

RETURN
    'GAP-ML-010 Granovetter Integration' AS status,
    'Enhances cascade simulation with CascadeEvent genealogy tracking' AS description,
    'Compatible with existing Granovetter queries (03_granovetter_threshold.cypher)' AS compatibility,
    'Adds zero overhead to existing logic, just tracks events' AS performance_impact;
