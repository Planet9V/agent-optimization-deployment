// ============================================
// EQUATION 3: Granovetter Threshold Model
// ============================================
// r(t+1) = N × F(r(t)/N)
// where:
//   r(t) = number of adopters at time t
//   N = total population
//   F = cumulative distribution function of thresholds
// Application: Attack technique adoption cascade in threat actor networks

// ============================================
// STEP 1: Create Graph Projection
// ============================================

// Drop existing projection if it exists
CALL gds.graph.exists('psychohistory_threshold') YIELD exists
WITH exists WHERE exists
CALL gds.graph.drop('psychohistory_threshold') YIELD graphName
RETURN 'Dropped existing graph: ' + graphName AS status
UNION
WITH 1 AS dummy WHERE NOT gds.graph.exists('psychohistory_threshold')
RETURN 'No existing graph to drop' AS status;

// Create projection for adoption cascades
CALL gds.graph.project(
    'psychohistory_threshold',
    ['Technique', 'Threat_Actor', 'Campaign', 'Tool', 'Tactic'],
    {
        USES_TECHNIQUE: {
            type: 'USES_TECHNIQUE',
            orientation: 'NATURAL'
        },
        ATTRIBUTED_TO: {
            type: 'ATTRIBUTED_TO',
            orientation: 'NATURAL'
        },
        USES_TOOL: {
            type: 'USES_TOOL',
            orientation: 'NATURAL'
        },
        RELATES_TO: {
            type: 'RELATES_TO',
            orientation: 'UNDIRECTED'
        }
    }
) YIELD graphName, nodeCount, relationshipCount
RETURN
    graphName,
    nodeCount AS total_nodes,
    relationshipCount AS total_relationships;

// ============================================
// STEP 2: Assign Adoption Thresholds
// ============================================

// Assign heterogeneous adoption thresholds to each actor
// Threshold = fraction of neighbors that must adopt before actor adopts
MATCH (actor:Threat_Actor)
WITH actor,
     // Sophisticated actors have lower thresholds (early adopters)
     // Less sophisticated actors have higher thresholds (late adopters)
     CASE
         WHEN actor.sophistication = 'high' OR actor.sophistication = 'advanced' THEN
             0.1 + (rand() * 0.2)  // Threshold: 0.1-0.3
         WHEN actor.sophistication = 'medium' OR actor.sophistication = 'moderate' THEN
             0.3 + (rand() * 0.3)  // Threshold: 0.3-0.6
         ELSE
             0.6 + (rand() * 0.3)  // Threshold: 0.6-0.9
     END AS threshold
SET actor.adoption_threshold = threshold,
    actor.adopted = false,
    actor.adoption_time = null
RETURN
    'Thresholds Assigned' AS status,
    count(actor) AS total_actors,
    avg(threshold) AS avg_threshold,
    min(threshold) AS min_threshold,
    max(threshold) AS max_threshold;

// Initialize techniques with adoption status
MATCH (tech:Technique)
SET tech.adopter_count = 0,
    tech.total_population = 0
RETURN
    'Techniques Initialized' AS status,
    count(tech) AS total_techniques;

// ============================================
// STEP 3: Calculate Population (N) per Technique
// ============================================

// For each technique, count potential adopters
MATCH (tech:Technique)
OPTIONAL MATCH (actor:Threat_Actor)
WITH tech, count(DISTINCT actor) AS N_population
SET tech.total_population = N_population
RETURN
    'Population Calculated' AS status,
    avg(N_population) AS avg_population_per_technique,
    max(N_population) AS max_population;

// ============================================
// STEP 4: Seed Initial Adopters
// ============================================

// Seed 5-10% of most sophisticated actors as initial adopters
MATCH (actor:Threat_Actor)
WHERE actor.sophistication IN ['high', 'advanced']
WITH actor
ORDER BY rand()
LIMIT toInteger(count(*) * 0.1)
SET actor.adopted = true,
    actor.adoption_time = 0
WITH count(actor) AS seed_count
RETURN
    'Initial Adopters Seeded' AS status,
    seed_count AS initial_adopters;

// Update technique adopter counts
MATCH (actor:Threat_Actor {adopted: true})-[:USES_TECHNIQUE]->(tech:Technique)
WITH tech, count(DISTINCT actor) AS adopters
SET tech.adopter_count = adopters
RETURN
    'Technique Counts Updated' AS status,
    sum(adopters) AS total_initial_adoptions;

// ============================================
// STEP 5: Simulate Cascade Dynamics (Multiple Rounds)
// ============================================

// Round 1: Check threshold and propagate adoption
MATCH (actor:Threat_Actor {adopted: false})
MATCH (neighbor:Threat_Actor {adopted: true})
WHERE (actor)-[:RELATES_TO|ATTRIBUTED_TO]-(neighbor)
WITH actor,
     count(DISTINCT neighbor) AS adopted_neighbors,
     size([(actor)-[:RELATES_TO|ATTRIBUTED_TO]-(n:Threat_Actor) | n]) AS total_neighbors
WHERE total_neighbors > 0
WITH actor,
     toFloat(adopted_neighbors) / toFloat(total_neighbors) AS adoption_fraction
WHERE adoption_fraction >= actor.adoption_threshold
SET actor.adopted = true,
    actor.adoption_time = 1
WITH count(actor) AS new_adopters
RETURN
    'ROUND 1' AS round,
    new_adopters AS newly_adopted,
    CASE WHEN new_adopters > 0 THEN 'CASCADE CONTINUING' ELSE 'CASCADE STOPPED' END AS status;

// Rounds 2-10: Continue cascade until no new adopters
UNWIND range(2, 10) AS round_num
WITH round_num
MATCH (actor:Threat_Actor {adopted: false})
MATCH (neighbor:Threat_Actor {adopted: true})
WHERE (actor)-[:RELATES_TO|ATTRIBUTED_TO]-(neighbor)
WITH round_num, actor,
     count(DISTINCT neighbor) AS adopted_neighbors,
     size([(actor)-[:RELATES_TO|ATTRIBUTED_TO]-(n:Threat_Actor) | n]) AS total_neighbors
WHERE total_neighbors > 0
WITH round_num, actor,
     toFloat(adopted_neighbors) / toFloat(total_neighbors) AS adoption_fraction
WHERE adoption_fraction >= actor.adoption_threshold
SET actor.adopted = true,
    actor.adoption_time = round_num
WITH round_num, count(actor) AS new_adopters
WHERE new_adopters > 0
RETURN
    'ROUND ' + toString(round_num) AS round,
    new_adopters AS newly_adopted,
    'CASCADE CONTINUING' AS status
ORDER BY round_num;

// ============================================
// STEP 6: Analyze Final Cascade Results
// ============================================

// Calculate final adoption statistics
MATCH (actor:Threat_Actor)
WITH count(actor) AS total_actors,
     count(CASE WHEN actor.adopted THEN 1 END) AS total_adopted
WITH total_actors, total_adopted,
     toFloat(total_adopted) / toFloat(total_actors) AS adoption_rate
RETURN
    'Final Cascade Results' AS analysis,
    total_actors AS population_N,
    total_adopted AS final_adopters_r,
    round(adoption_rate * 100) AS adoption_percentage,
    CASE
        WHEN adoption_rate > 0.7 THEN 'MASSIVE CASCADE (>70% adoption)'
        WHEN adoption_rate > 0.4 THEN 'MAJOR CASCADE (40-70% adoption)'
        WHEN adoption_rate > 0.2 THEN 'MODERATE CASCADE (20-40% adoption)'
        ELSE 'LIMITED CASCADE (<20% adoption)'
    END AS cascade_magnitude;

// ============================================
// STEP 7: Identify Critical Actors (Tipping Points)
// ============================================

// Find actors who caused largest cascades when they adopted
MATCH (actor:Threat_Actor {adopted: true})
WHERE actor.adoption_time IS NOT NULL AND actor.adoption_time > 0
MATCH (influenced:Threat_Actor {adopted: true})
WHERE influenced.adoption_time = actor.adoption_time + 1
AND (actor)-[:RELATES_TO|ATTRIBUTED_TO]-(influenced)
WITH actor,
     CASE
         WHEN actor.name IS NOT NULL THEN actor.name
         WHEN actor.id IS NOT NULL THEN actor.id
         ELSE 'Unknown'
     END AS actor_name,
     actor.adoption_time AS when_adopted,
     count(DISTINCT influenced) AS directly_influenced,
     actor.adoption_threshold AS threshold
RETURN
    actor_name,
    when_adopted AS adoption_round,
    threshold AS required_threshold,
    directly_influenced AS cascade_triggered,
    CASE
        WHEN directly_influenced > 5 THEN 'CRITICAL TIPPING POINT'
        WHEN directly_influenced > 2 THEN 'SIGNIFICANT INFLUENCER'
        ELSE 'MINOR INFLUENCER'
    END AS cascade_role
ORDER BY directly_influenced DESC
LIMIT 20;

// ============================================
// STEP 8: Threshold Distribution Analysis
// ============================================

// Analyze how threshold distribution affects cascade size
MATCH (actor:Threat_Actor)
WITH actor.adoption_threshold AS threshold,
     actor.adopted AS is_adopter
ORDER BY threshold
WITH threshold, is_adopter,
     // Calculate cumulative distribution F(threshold)
     sum(CASE WHEN is_adopter THEN 1 ELSE 0 END) AS cumulative_adopters,
     count(*) AS cumulative_population
WITH threshold,
     toFloat(cumulative_adopters) / toFloat(cumulative_population) AS F_threshold,
     cumulative_adopters,
     cumulative_population
WHERE threshold IS NOT NULL
RETURN
    round(threshold * 10) / 10 AS threshold_value,
    cumulative_adopters AS adopters_below_threshold,
    cumulative_population AS actors_below_threshold,
    round(F_threshold * 100) AS cumulative_adoption_pct,
    CASE
        WHEN F_threshold > 0.8 THEN 'CRITICAL MASS ACHIEVED'
        WHEN F_threshold > 0.5 THEN 'MAJORITY ADOPTION'
        WHEN F_threshold > 0.2 THEN 'EARLY ADOPTION PHASE'
        ELSE 'INITIAL SEEDING'
    END AS adoption_phase
ORDER BY threshold_value;

// ============================================
// STEP 9: Predict Technique Adoption Cascades
// ============================================

// For each technique, calculate r(t+1) = N × F(r(t)/N)
MATCH (tech:Technique)
OPTIONAL MATCH (actor:Threat_Actor {adopted: true})-[:USES_TECHNIQUE]->(tech)
WITH tech,
     CASE
         WHEN tech.name IS NOT NULL THEN tech.name
         WHEN tech.id IS NOT NULL THEN tech.id
         ELSE 'Unknown'
     END AS tech_name,
     count(DISTINCT actor) AS current_adopters,
     tech.total_population AS N_population
WHERE N_population > 0
WITH tech_name,
     current_adopters AS r_t,
     N_population AS N,
     toFloat(current_adopters) / toFloat(N_population) AS current_fraction
// Estimate F(r/N) using logistic function as approximation
WITH tech_name, r_t, N, current_fraction,
     1.0 / (1.0 + exp(-5.0 * (current_fraction - 0.5))) AS F_estimate
WITH tech_name, r_t, N, current_fraction,
     toInteger(N * F_estimate) AS r_t_plus_1,
     F_estimate
RETURN
    tech_name AS technique,
    r_t AS current_adopters,
    N AS total_population,
    round(current_fraction * 100) AS current_adoption_pct,
    r_t_plus_1 AS predicted_next_adopters,
    round((toFloat(r_t_plus_1 - r_t) / N) * 100) AS predicted_growth_pct,
    CASE
        WHEN r_t_plus_1 > r_t * 1.5 THEN 'EXPLOSIVE GROWTH'
        WHEN r_t_plus_1 > r_t * 1.1 THEN 'STEADY GROWTH'
        WHEN r_t_plus_1 > r_t THEN 'SLOW GROWTH'
        ELSE 'SATURATION/DECLINE'
    END AS growth_phase
ORDER BY predicted_growth_pct DESC
LIMIT 25;

// ============================================
// STEP 10: Identify Unstable Equilibria
// ============================================

// Find techniques at critical adoption levels where small changes cause large cascades
MATCH (tech:Technique)
OPTIONAL MATCH (actor:Threat_Actor)-[:USES_TECHNIQUE]->(tech)
WITH tech,
     CASE
         WHEN tech.name IS NOT NULL THEN tech.name
         WHEN tech.id IS NOT NULL THEN tech.id
         ELSE 'Unknown'
     END AS tech_name,
     count(DISTINCT CASE WHEN actor.adopted THEN actor END) AS adopters,
     count(DISTINCT actor) AS total_actors
WHERE total_actors > 5
WITH tech_name, adopters, total_actors,
     toFloat(adopters) / toFloat(total_actors) AS adoption_rate,
     // Critical region is around 30-70% adoption
     abs(0.5 - (toFloat(adopters) / toFloat(total_actors))) AS distance_from_critical
WHERE distance_from_critical < 0.3
RETURN
    tech_name,
    adopters,
    total_actors,
    round(adoption_rate * 100) AS adoption_pct,
    CASE
        WHEN adoption_rate > 0.5 THEN 'ABOVE CRITICAL POINT (Cascade likely)'
        ELSE 'BELOW CRITICAL POINT (Cascade vulnerable)'
    END AS equilibrium_state,
    CASE
        WHEN distance_from_critical < 0.1 THEN 'HIGHLY UNSTABLE'
        WHEN distance_from_critical < 0.2 THEN 'MODERATELY UNSTABLE'
        ELSE 'APPROACHING STABILITY'
    END AS stability
ORDER BY distance_from_critical
LIMIT 15;

// ============================================
// STEP 11: Calculate Cascade Velocity
// ============================================

// Analyze how fast adoption spreads over time
MATCH (actor:Threat_Actor {adopted: true})
WHERE actor.adoption_time IS NOT NULL
WITH actor.adoption_time AS time_step,
     count(actor) AS new_adopters
ORDER BY time_step
WITH collect(time_step) AS time_series,
     collect(new_adopters) AS adoption_series
UNWIND range(0, size(time_series) - 1) AS idx
WITH time_series[idx] AS round,
     adoption_series[idx] AS adopters,
     CASE WHEN idx > 0 THEN adoption_series[idx] - adoption_series[idx-1] ELSE adoption_series[idx] END AS velocity
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
// STEP 12: Validation Tests
// ============================================

// Test 1: Verify graph projection exists
CALL gds.graph.exists('psychohistory_threshold') YIELD exists
RETURN
    'TEST 1: Graph Projection' AS test_name,
    CASE WHEN exists THEN 'PASS' ELSE 'FAIL' END AS result;

// Test 2: Verify thresholds are assigned
MATCH (actor:Threat_Actor)
WHERE actor.adoption_threshold IS NOT NULL
WITH count(actor) AS actors_with_thresholds
RETURN
    'TEST 2: Threshold Assignment' AS test_name,
    CASE WHEN actors_with_thresholds > 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    actors_with_thresholds AS nodes_configured;

// Test 3: Verify cascade occurred
MATCH (actor:Threat_Actor {adopted: true})
WITH count(actor) AS total_adopted
RETURN
    'TEST 3: Cascade Simulation' AS test_name,
    CASE WHEN total_adopted > 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    total_adopted AS adopters;

// Test 4: Verify threshold values are in valid range
MATCH (actor:Threat_Actor)
WHERE actor.adoption_threshold IS NOT NULL
WITH min(actor.adoption_threshold) AS min_t, max(actor.adoption_threshold) AS max_t
RETURN
    'TEST 4: Threshold Value Range' AS test_name,
    CASE WHEN min_t >= 0.0 AND max_t <= 1.0 THEN 'PASS' ELSE 'FAIL' END AS result,
    round(min_t * 100) / 100 AS min_threshold,
    round(max_t * 100) / 100 AS max_threshold;

// Test 5: Verify adoption times are sequential
MATCH (actor:Threat_Actor {adopted: true})
WHERE actor.adoption_time IS NOT NULL
WITH min(actor.adoption_time) AS min_time, max(actor.adoption_time) AS max_time
RETURN
    'TEST 5: Temporal Consistency' AS test_name,
    CASE WHEN min_time >= 0 AND max_time >= min_time THEN 'PASS' ELSE 'FAIL' END AS result,
    min_time AS first_adoption_round,
    max_time AS final_adoption_round;

// ============================================
// STEP 13: Cleanup (Optional)
// ============================================

// CALL gds.graph.drop('psychohistory_threshold') YIELD graphName
// RETURN 'Dropped graph: ' + graphName AS cleanup_status;

// Reset adoption states for re-simulation
// MATCH (actor:Threat_Actor)
// REMOVE actor.adopted, actor.adoption_time, actor.adoption_threshold
// RETURN 'Reset adoption states' AS status;
