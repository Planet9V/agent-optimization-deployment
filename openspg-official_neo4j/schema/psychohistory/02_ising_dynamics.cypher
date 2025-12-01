// ============================================
// EQUATION 2: Ising Dynamics (Opinion Formation)
// ============================================
// dm/dt = -m + tanh(β(Jzm + h))
// where:
//   m = average opinion/state (-1 to +1)
//   J = coupling strength (peer influence)
//   z = average degree (network connectivity)
//   h = external field (propaganda/external influence)
//   β = inverse temperature (rationality parameter)
// Application: Opinion/belief propagation in adversary networks

// ============================================
// STEP 1: Create Graph Projection
// ============================================

// Drop existing projection if it exists
CALL gds.graph.exists('psychohistory_ising') YIELD exists
WITH exists WHERE exists
CALL gds.graph.drop('psychohistory_ising') YIELD graphName
RETURN 'Dropped existing graph: ' + graphName AS status
UNION
WITH 1 AS dummy WHERE NOT gds.graph.exists('psychohistory_ising')
RETURN 'No existing graph to drop' AS status;

// Create projection for opinion dynamics
CALL gds.graph.project(
    'psychohistory_ising',
    // Nodes: Actors, Campaigns, Techniques
    ['Threat_Actor', 'Campaign', 'Technique', 'Tactic'],
    // Relationships: influence networks
    {
        USES_TECHNIQUE: {
            type: 'USES_TECHNIQUE',
            orientation: 'UNDIRECTED',
            properties: {
                coupling: {
                    property: 'proficiency',
                    defaultValue: 0.5
                }
            }
        },
        ATTRIBUTED_TO: {
            type: 'ATTRIBUTED_TO',
            orientation: 'UNDIRECTED',
            properties: {
                coupling: {
                    property: 'confidence',
                    defaultValue: 0.5
                }
            }
        },
        PART_OF_CAMPAIGN: {
            type: 'PART_OF_CAMPAIGN',
            orientation: 'UNDIRECTED',
            properties: {
                coupling: {
                    property: 'association_strength',
                    defaultValue: 0.5
                }
            }
        },
        RELATES_TO: {
            type: 'RELATES_TO',
            orientation: 'UNDIRECTED',
            properties: {
                coupling: {
                    property: 'similarity',
                    defaultValue: 0.5
                }
            }
        }
    }
) YIELD graphName, nodeCount, relationshipCount
RETURN
    graphName,
    nodeCount AS total_nodes,
    relationshipCount AS total_relationships;

// ============================================
// STEP 2: Initialize Opinion States
// ============================================

// Assign initial opinion states to nodes
// +1 = pro-attack, -1 = defensive, 0 = neutral
MATCH (n)
WHERE n:Technique OR n:Threat_Actor OR n:Campaign OR n:Tactic
WITH n,
     labels(n)[0] AS node_type,
     CASE
         WHEN n:Threat_Actor THEN
             CASE
                 WHEN n.sophistication = 'high' OR n.sophistication = 'advanced' THEN 0.8
                 WHEN n.sophistication = 'medium' OR n.sophistication = 'moderate' THEN 0.3
                 ELSE -0.2
             END
         WHEN n:Campaign THEN
             CASE
                 WHEN n.active = true OR n.status = 'active' THEN 0.7
                 ELSE 0.0
             END
         WHEN n:Technique THEN
             CASE
                 WHEN n.prevalence = 'high' OR n.detection_difficulty = 'hard' THEN 0.6
                 WHEN n.prevalence = 'medium' THEN 0.2
                 ELSE -0.3
             END
         WHEN n:Tactic THEN 0.4
         ELSE 0.0
     END AS initial_opinion
SET n.opinion_state = initial_opinion
RETURN
    node_type,
    count(*) AS node_count,
    avg(initial_opinion) AS avg_initial_opinion,
    min(initial_opinion) AS min_opinion,
    max(initial_opinion) AS max_opinion;

// ============================================
// STEP 3: Calculate Network Parameters
// ============================================

// Calculate z (average degree) and coupling strength J
MATCH (n)
WHERE n:Technique OR n:Threat_Actor OR n:Campaign OR n:Tactic
WITH n,
     size([(n)-[]-() | 1]) AS degree
WITH avg(degree) AS z_avg_degree,
     stdev(degree) AS degree_variance,
     max(degree) AS max_degree,
     min(degree) AS min_degree
RETURN
    'Network Parameters' AS parameter_set,
    z_avg_degree AS z_average_connectivity,
    degree_variance,
    max_degree,
    min_degree,
    CASE
        WHEN degree_variance > z_avg_degree THEN 'SCALE-FREE: High influence concentration'
        ELSE 'RANDOM: Distributed influence'
    END AS network_type;

// ============================================
// STEP 4: Simulate Ising Dynamics (Multiple Iterations)
// ============================================

// Iteration 1: Calculate opinion update
// dm/dt = -m + tanh(β(Jzm + h))
WITH 1.5 AS beta, 0.8 AS J, 0.2 AS h
MATCH (n)
WHERE n:Technique OR n:Threat_Actor OR n:Campaign OR n:Tactic
WITH n, beta, J, h,
     size([(n)-[]-() | 1]) AS z_local,
     coalesce(n.opinion_state, 0.0) AS m_current
WITH n, beta, J, h, z_local, m_current,
     -m_current + tanh(beta * (J * z_local * m_current + h)) AS dm_dt
SET n.opinion_state = m_current + (dm_dt * 0.1)
WITH n,
     labels(n)[0] AS node_type,
     m_current AS old_opinion,
     n.opinion_state AS new_opinion,
     CASE
         WHEN n.name IS NOT NULL THEN n.name
         WHEN n.id IS NOT NULL THEN n.id
         ELSE 'Unknown'
     END AS node_name
WHERE abs(new_opinion - old_opinion) > 0.01
RETURN
    'ITERATION 1' AS iteration,
    node_type,
    node_name,
    round(old_opinion * 100) / 100 AS before,
    round(new_opinion * 100) / 100 AS after,
    round((new_opinion - old_opinion) * 100) / 100 AS opinion_change
ORDER BY abs(new_opinion - old_opinion) DESC
LIMIT 20;

// Run 5 more iterations to reach equilibrium
UNWIND range(2, 6) AS iteration
WITH iteration, 1.5 AS beta, 0.8 AS J, 0.2 AS h
MATCH (n)
WHERE n:Technique OR n:Threat_Actor OR n:Campaign OR n:Tactic
WITH n, iteration, beta, J, h,
     size([(n)-[]-() | 1]) AS z_local,
     coalesce(n.opinion_state, 0.0) AS m_current
WITH n, iteration, beta, J, h, z_local, m_current,
     -m_current + tanh(beta * (J * z_local * m_current + h)) AS dm_dt
SET n.opinion_state = m_current + (dm_dt * 0.1)
WITH iteration, avg(n.opinion_state) AS avg_opinion
RETURN
    'ITERATION ' + toString(iteration) AS step,
    round(avg_opinion * 1000) / 1000 AS average_network_opinion,
    CASE
        WHEN avg_opinion > 0.5 THEN 'CONSENSUS: Pro-attack'
        WHEN avg_opinion < -0.5 THEN 'CONSENSUS: Defensive'
        ELSE 'MIXED: No clear consensus'
    END AS network_state;

// ============================================
// STEP 5: Detect Opinion Clusters (Communities)
// ============================================

// Use Louvain to find communities with similar opinions
CALL gds.louvain.stream('psychohistory_ising', {
    relationshipWeightProperty: 'coupling',
    includeIntermediateCommunities: false
})
YIELD nodeId, communityId
WITH gds.util.asNode(nodeId) AS node, communityId
WHERE node.opinion_state IS NOT NULL
WITH communityId,
     collect(node) AS members,
     avg(node.opinion_state) AS community_opinion,
     count(node) AS community_size
WHERE community_size > 2
RETURN
    communityId AS cluster_id,
    community_size,
    round(community_opinion * 100) / 100 AS cluster_opinion,
    CASE
        WHEN community_opinion > 0.5 THEN 'AGGRESSIVE CLUSTER (Pro-attack)'
        WHEN community_opinion < -0.5 THEN 'DEFENSIVE CLUSTER (Risk-averse)'
        ELSE 'NEUTRAL CLUSTER (Mixed strategies)'
    END AS cluster_type,
    CASE
        WHEN community_size > 10 AND abs(community_opinion) > 0.5 THEN 'HIGH IMPACT'
        WHEN community_size > 5 THEN 'MODERATE IMPACT'
        ELSE 'LOW IMPACT'
    END AS strategic_importance
ORDER BY community_size * abs(community_opinion) DESC
LIMIT 15;

// ============================================
// STEP 6: Identify Opinion Leaders (Influencers)
// ============================================

// Find nodes with high degree AND strong opinions
MATCH (n)
WHERE n:Technique OR n:Threat_Actor OR n:Campaign
WITH n,
     labels(n)[0] AS node_type,
     CASE
         WHEN n.name IS NOT NULL THEN n.name
         WHEN n.id IS NOT NULL THEN n.id
         ELSE 'Unknown'
     END AS node_name,
     size([(n)-[]-() | 1]) AS degree,
     coalesce(n.opinion_state, 0.0) AS opinion
WHERE degree > 3 AND abs(opinion) > 0.3
WITH node_type, node_name, degree, opinion,
     degree * abs(opinion) AS influence_score
RETURN
    node_type,
    node_name,
    round(opinion * 100) / 100 AS opinion_state,
    degree AS connections,
    round(influence_score * 100) / 100 AS influence_power,
    CASE
        WHEN opinion > 0.5 THEN 'AGGRESSIVE INFLUENCER'
        WHEN opinion < -0.5 THEN 'DEFENSIVE INFLUENCER'
        ELSE 'NEUTRAL INFLUENCER'
    END AS influencer_type
ORDER BY influence_score DESC
LIMIT 25;

// ============================================
// STEP 7: Analyze External Field Effect (h)
// ============================================

// Test different external field strengths
UNWIND [
    {h: -0.5, scenario: 'Strong Defensive Propaganda'},
    {h: 0.0, scenario: 'No External Influence'},
    {h: 0.5, scenario: 'Strong Attack Propaganda'},
    {h: 1.0, scenario: 'Extreme Attack Propaganda'}
] AS test
WITH test.h AS h_value, test.scenario AS scenario,
     1.5 AS beta, 0.8 AS J, 5.0 AS z_avg
WITH scenario, h_value, beta, J, z_avg,
     tanh(beta * (J * z_avg * 0.3 + h_value)) AS equilibrium_opinion
RETURN
    scenario,
    h_value AS external_field,
    round(equilibrium_opinion * 100) / 100 AS predicted_consensus,
    CASE
        WHEN equilibrium_opinion > 0.7 THEN 'STRONG PRO-ATTACK CONSENSUS'
        WHEN equilibrium_opinion > 0.3 THEN 'MODERATE PRO-ATTACK BIAS'
        WHEN equilibrium_opinion > -0.3 THEN 'NEUTRAL/MIXED'
        WHEN equilibrium_opinion > -0.7 THEN 'MODERATE DEFENSIVE BIAS'
        ELSE 'STRONG DEFENSIVE CONSENSUS'
    END AS outcome
ORDER BY h_value;

// ============================================
// STEP 8: Calculate Phase Transition Point
// ============================================

// Find critical β where system transitions from disorder to order
UNWIND range(1, 50) AS step
WITH step, step * 0.1 AS beta, 0.8 AS J, 5.0 AS z_avg, 0.2 AS h
WITH beta, J, z_avg, h,
     tanh(beta * (J * z_avg * 0.5 + h)) AS m_plus,
     tanh(beta * (J * z_avg * (-0.5) + h)) AS m_minus
WITH beta,
     abs(m_plus - m_minus) AS order_parameter
RETURN
    round(beta * 10) / 10 AS beta_rationality,
    round(order_parameter * 100) / 100 AS polarization,
    CASE
        WHEN order_parameter > 0.8 THEN 'ORDERED PHASE (Strong consensus possible)'
        WHEN order_parameter > 0.4 THEN 'TRANSITION ZONE'
        ELSE 'DISORDERED PHASE (Weak consensus)'
    END AS phase
ORDER BY beta_rationality;

// ============================================
// STEP 9: Predict Opinion Cascade Probability
// ============================================

// Calculate probability of opinion cascade starting from high-influence nodes
MATCH (seed)
WHERE seed:Threat_Actor OR seed:Technique
WITH seed,
     labels(seed)[0] AS seed_type,
     CASE
         WHEN seed.name IS NOT NULL THEN seed.name
         WHEN seed.id IS NOT NULL THEN seed.id
         ELSE 'Unknown'
     END AS seed_name,
     coalesce(seed.opinion_state, 0.0) AS seed_opinion,
     size([(seed)-[]-() | 1]) AS seed_degree
WHERE seed_degree > 5 AND abs(seed_opinion) > 0.5
MATCH path = (seed)-[*1..3]-(influenced)
WHERE influenced:Technique OR influenced:Threat_Actor OR influenced:Campaign
WITH seed_type, seed_name, seed_opinion, seed_degree,
     count(DISTINCT influenced) AS potential_reach,
     avg(coalesce(influenced.opinion_state, 0.0)) AS avg_neighbor_opinion
WITH seed_type, seed_name, seed_opinion, seed_degree, potential_reach,
     avg_neighbor_opinion,
     1.0 / (1.0 + exp(-3.0 * (seed_opinion - avg_neighbor_opinion))) AS cascade_probability
RETURN
    seed_type,
    seed_name,
    round(seed_opinion * 100) / 100 AS initial_opinion,
    seed_degree AS direct_influence,
    potential_reach AS cascade_reach,
    round(cascade_probability * 100) / 100 AS cascade_probability,
    CASE
        WHEN cascade_probability > 0.7 THEN 'HIGH CASCADE RISK'
        WHEN cascade_probability > 0.4 THEN 'MODERATE CASCADE RISK'
        ELSE 'LOW CASCADE RISK'
    END AS cascade_risk
ORDER BY cascade_probability DESC
LIMIT 20;

// ============================================
// STEP 10: Validation Tests
// ============================================

// Test 1: Verify graph exists
CALL gds.graph.exists('psychohistory_ising') YIELD exists
RETURN
    'TEST 1: Graph Projection' AS test_name,
    CASE WHEN exists THEN 'PASS' ELSE 'FAIL' END AS result;

// Test 2: Verify opinion states are initialized
MATCH (n)
WHERE n:Technique OR n:Threat_Actor OR n:Campaign OR n:Tactic
WITH count(n) AS total, count(n.opinion_state) AS with_opinion
RETURN
    'TEST 2: Opinion Initialization' AS test_name,
    CASE WHEN with_opinion > 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    total AS total_nodes,
    with_opinion AS nodes_with_opinions;

// Test 3: Verify opinion values are in valid range [-1, 1]
MATCH (n)
WHERE n.opinion_state IS NOT NULL
WITH min(n.opinion_state) AS min_op, max(n.opinion_state) AS max_op
RETURN
    'TEST 3: Opinion Value Range' AS test_name,
    CASE WHEN min_op >= -1.5 AND max_op <= 1.5 THEN 'PASS' ELSE 'FAIL' END AS result,
    round(min_op * 100) / 100 AS min_opinion,
    round(max_op * 100) / 100 AS max_opinion;

// Test 4: Verify opinion dynamics converged
MATCH (n)
WHERE n.opinion_state IS NOT NULL
WITH avg(n.opinion_state) AS avg_opinion, stdev(n.opinion_state) AS opinion_variance
RETURN
    'TEST 4: Equilibrium Reached' AS test_name,
    CASE WHEN opinion_variance IS NOT NULL THEN 'PASS' ELSE 'FAIL' END AS result,
    round(avg_opinion * 100) / 100 AS average_opinion,
    round(opinion_variance * 100) / 100 AS variance;

// ============================================
// STEP 11: Cleanup (Optional)
// ============================================

// CALL gds.graph.drop('psychohistory_ising') YIELD graphName
// RETURN 'Dropped graph: ' + graphName AS cleanup_status;
