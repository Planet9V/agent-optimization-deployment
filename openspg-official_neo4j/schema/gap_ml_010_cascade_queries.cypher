// ============================================
// GAP-ML-010: Cascade Event Genealogy Queries
// ============================================
// Purpose: Query and analyze cascade event trees with genealogy tracking
// Created: 2025-11-30
// Status: ACTIVE

// ============================================
// QUERY 1: CASCADE TREE VISUALIZATION
// ============================================
// Retrieves complete cascade tree from seed event to all descendants
// Parameters: $cascade_id (string) - Root cascade event ID

MATCH path = (seed:CascadeEvent {id: $cascade_id})-[:TRIGGERED*0..10]->(descendant:CascadeEvent)
RETURN
    path,
    seed.id AS seed_event_id,
    descendant.id AS descendant_id,
    descendant.generation AS generation,
    length(path) AS path_depth,
    [node IN nodes(path) | node.id] AS event_chain
ORDER BY generation, descendant.id;

// ============================================
// QUERY 2: CASCADE GENEALOGY WITH METADATA
// ============================================
// Retrieves cascade tree with full event metadata for analysis

MATCH path = (seed:CascadeEvent {cascade_id: $cascade_id})-[:TRIGGERED*0..10]->(descendant:CascadeEvent)
RETURN
    descendant.id AS event_id,
    descendant.generation AS generation,
    descendant.parent_event_id AS parent_id,
    descendant.actor_id AS actor,
    descendant.timestamp AS event_time,
    descendant.activation_threshold AS threshold,
    descendant.neighbor_influence AS influence,
    length(path) AS distance_from_seed
ORDER BY generation, event_time;

// ============================================
// QUERY 3: CASCADE VELOCITY CALCULATION
// ============================================
// Calculates velocity (activations per time unit) for each generation
// Uses existing Granovetter approach (line 339-365 of 03_granovetter_threshold.cypher)

MATCH (ce:CascadeEvent {cascade_id: $cascade_id})
WHERE ce.generation IS NOT NULL
WITH ce.generation AS generation,
     count(ce) AS activations_at_generation,
     min(ce.timestamp) AS gen_start_time,
     max(ce.timestamp) AS gen_end_time
ORDER BY generation
WITH generation,
     activations_at_generation,
     gen_start_time,
     gen_end_time,
     duration.inSeconds(gen_end_time, gen_start_time) AS gen_duration_seconds
WITH generation,
     activations_at_generation,
     CASE
         WHEN gen_duration_seconds > 0 THEN toFloat(activations_at_generation) / gen_duration_seconds
         ELSE toFloat(activations_at_generation)
     END AS velocity
RETURN
    generation,
    activations_at_generation AS new_activations,
    round(velocity * 100) / 100 AS velocity_per_second,
    CASE
        WHEN velocity > 10 THEN 'EXPLOSIVE PHASE'
        WHEN velocity > 5 THEN 'RAPID GROWTH'
        WHEN velocity > 2 THEN 'MODERATE GROWTH'
        WHEN velocity > 0 THEN 'SLOW GROWTH'
        ELSE 'SATURATION'
    END AS cascade_phase
ORDER BY generation;

// ============================================
// QUERY 4: PARENT-CHILD RELATIONSHIP ANALYSIS
// ============================================
// Analyzes parent-child influence patterns in cascade

MATCH (parent:CascadeEvent {cascade_id: $cascade_id})-[t:TRIGGERED]->(child:CascadeEvent)
RETURN
    parent.id AS parent_event,
    parent.generation AS parent_generation,
    parent.actor_id AS parent_actor,
    child.id AS child_event,
    child.generation AS child_generation,
    child.actor_id AS child_actor,
    child.activation_threshold AS child_threshold,
    child.neighbor_influence AS child_influence,
    t.activation_time AS trigger_time
ORDER BY parent_generation, child_generation;

// ============================================
// QUERY 5: CRITICAL INFLUENCERS (TIPPING POINTS)
// ============================================
// Identifies events that triggered the most children (cascade amplifiers)

MATCH (parent:CascadeEvent {cascade_id: $cascade_id})-[:TRIGGERED]->(child:CascadeEvent)
WITH parent,
     parent.id AS event_id,
     parent.generation AS generation,
     parent.actor_id AS actor,
     count(child) AS children_triggered
WHERE children_triggered > 0
RETURN
    event_id,
    generation,
    actor,
    children_triggered,
    CASE
        WHEN children_triggered >= 5 THEN 'CRITICAL TIPPING POINT'
        WHEN children_triggered >= 3 THEN 'SIGNIFICANT INFLUENCER'
        WHEN children_triggered >= 2 THEN 'MODERATE INFLUENCER'
        ELSE 'MINOR INFLUENCER'
    END AS influence_level
ORDER BY children_triggered DESC, generation
LIMIT 20;

// ============================================
// QUERY 6: CASCADE DEPTH ANALYSIS
// ============================================
// Measures maximum propagation depth from seed event

MATCH path = (seed:CascadeEvent {id: $cascade_id})-[:TRIGGERED*]->(leaf:CascadeEvent)
WHERE NOT EXISTS { (leaf)-[:TRIGGERED]->() }
WITH path, length(path) AS depth
RETURN
    max(depth) AS maximum_depth,
    min(depth) AS minimum_depth,
    avg(depth) AS average_depth,
    count(DISTINCT leaf) AS leaf_node_count,
    CASE
        WHEN max(depth) >= 8 THEN 'DEEP CASCADE (8+ levels)'
        WHEN max(depth) >= 5 THEN 'MODERATE CASCADE (5-7 levels)'
        WHEN max(depth) >= 3 THEN 'SHALLOW CASCADE (3-4 levels)'
        ELSE 'LIMITED CASCADE (<3 levels)'
    END AS cascade_depth_classification;

// ============================================
// QUERY 7: GENERATION DISTRIBUTION
// ============================================
// Shows distribution of events across generations

MATCH (ce:CascadeEvent {cascade_id: $cascade_id})
WITH ce.generation AS generation, count(ce) AS event_count
ORDER BY generation
RETURN
    generation,
    event_count,
    sum(event_count) OVER (ORDER BY generation) AS cumulative_events,
    round(toFloat(event_count) / sum(event_count) OVER () * 100) AS percentage_of_total
ORDER BY generation;

// ============================================
// QUERY 8: TEMPORAL CASCADE PROGRESSION
// ============================================
// Analyzes how cascade evolves over time

MATCH (ce:CascadeEvent {cascade_id: $cascade_id})
WITH ce.generation AS generation,
     min(ce.timestamp) AS generation_start,
     max(ce.timestamp) AS generation_end,
     count(ce) AS events_in_generation
ORDER BY generation
WITH generation,
     generation_start,
     generation_end,
     events_in_generation,
     duration.inSeconds(generation_start, generation_end) AS generation_duration_seconds,
     lag(max(generation_end)) OVER (ORDER BY generation) AS previous_generation_end
WITH generation,
     generation_start,
     generation_end,
     events_in_generation,
     generation_duration_seconds,
     CASE
         WHEN previous_generation_end IS NOT NULL
         THEN duration.inSeconds(previous_generation_end, generation_start)
         ELSE 0
     END AS inter_generation_gap_seconds
RETURN
    generation,
    generation_start,
    generation_end,
    events_in_generation,
    generation_duration_seconds AS gen_duration_sec,
    inter_generation_gap_seconds AS gap_from_previous_sec,
    CASE
        WHEN inter_generation_gap_seconds = 0 THEN 'SIMULTANEOUS'
        WHEN inter_generation_gap_seconds < 60 THEN 'RAPID (<1 min gap)'
        WHEN inter_generation_gap_seconds < 300 THEN 'MODERATE (1-5 min gap)'
        ELSE 'DELAYED (>5 min gap)'
    END AS propagation_speed
ORDER BY generation;

// ============================================
// QUERY 9: BRANCHING FACTOR ANALYSIS
// ============================================
// Calculates average branching factor (children per parent) at each generation

MATCH (parent:CascadeEvent {cascade_id: $cascade_id})-[:TRIGGERED]->(child:CascadeEvent)
WITH parent.generation AS generation, parent, count(child) AS children_count
WITH generation, avg(children_count) AS avg_branching, max(children_count) AS max_branching
ORDER BY generation
RETURN
    generation,
    round(avg_branching * 100) / 100 AS avg_branching_factor,
    max_branching AS max_branching_factor,
    CASE
        WHEN avg_branching >= 3 THEN 'EXPLOSIVE (avg 3+ children)'
        WHEN avg_branching >= 2 THEN 'RAPID (avg 2-3 children)'
        WHEN avg_branching >= 1 THEN 'STEADY (avg 1-2 children)'
        ELSE 'DECLINING (avg <1 child)'
    END AS cascade_growth_rate
ORDER BY generation;

// ============================================
// QUERY 10: FULL CASCADE SUMMARY
// ============================================
// Comprehensive cascade statistics for reporting

MATCH (ce:CascadeEvent {cascade_id: $cascade_id})
WITH ce
OPTIONAL MATCH path = (ce)-[:TRIGGERED*]->()
WITH ce, path,
     max(length(path)) AS max_depth,
     count(DISTINCT ce) AS total_events,
     min(ce.timestamp) AS cascade_start,
     max(ce.timestamp) AS cascade_end,
     max(ce.generation) AS max_generation
RETURN
    $cascade_id AS cascade_id,
    total_events,
    max_generation + 1 AS total_generations,
    max_depth AS maximum_propagation_depth,
    cascade_start,
    cascade_end,
    duration.inSeconds(cascade_start, cascade_end) AS total_duration_seconds,
    toFloat(total_events) / (max_generation + 1) AS avg_events_per_generation,
    CASE
        WHEN total_events >= 100 THEN 'MASSIVE CASCADE'
        WHEN total_events >= 50 THEN 'LARGE CASCADE'
        WHEN total_events >= 20 THEN 'MODERATE CASCADE'
        WHEN total_events >= 10 THEN 'SMALL CASCADE'
        ELSE 'MINIMAL CASCADE'
    END AS cascade_magnitude;

// ============================================
// EXAMPLE USAGE
// ============================================

// Example 1: Visualize cascade tree for specific event
// :param cascade_id => "CASCADE_2025_11_30_001"
// MATCH path = (seed:CascadeEvent {id: $cascade_id})-[:TRIGGERED*0..10]->(descendant:CascadeEvent)
// RETURN path;

// Example 2: Calculate velocity for cascade
// :param cascade_id => "CASCADE_2025_11_30_001"
// [Run QUERY 3: CASCADE VELOCITY CALCULATION]

// Example 3: Find critical influencers
// :param cascade_id => "CASCADE_2025_11_30_001"
// [Run QUERY 5: CRITICAL INFLUENCERS]

// ============================================
// SUMMARY
// ============================================

RETURN
    'GAP-ML-010 Cascade Query Library' AS status,
    '10 queries for cascade genealogy analysis' AS query_count,
    'Compatible with Granovetter threshold queries' AS integration,
    'Supports velocity, depth, branching, and temporal analysis' AS capabilities;
