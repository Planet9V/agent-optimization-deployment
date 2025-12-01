// ============================================
// EQUATION 1: Epidemic Threshold (R₀)
// ============================================
// R₀ = β/γ × λmax(A)
// where:
//   β = infection rate (influence strength)
//   γ = recovery rate (skepticism)
//   λmax(A) = largest eigenvalue of adjacency matrix
// Application: Will malware/belief spread in the network?

// ============================================
// STEP 1: Create Graph Projection for Pagerank (proxy for dominant eigenvalue)
// ============================================

// Drop existing projection if it exists
CALL gds.graph.exists('psychohistory_epidemic') YIELD exists
WITH exists WHERE exists
CALL gds.graph.drop('psychohistory_epidemic') YIELD graphName
RETURN 'Dropped existing graph: ' + graphName AS status
UNION
WITH 1 AS dummy WHERE NOT gds.graph.exists('psychohistory_epidemic')
RETURN 'No existing graph to drop' AS status;

// Create projection with Technique spreading through ICS_Asset via Vulnerability
CALL gds.graph.project(
    'psychohistory_epidemic',
    // Node projection
    ['Technique', 'ICS_Asset', 'Vulnerability', 'Threat_Actor', 'Campaign'],
    // Relationship projection with weights
    {
        EXPLOITS: {
            type: 'EXPLOITS',
            orientation: 'NATURAL',
            properties: {
                influence: {
                    property: 'severity_score',
                    defaultValue: 0.5
                }
            }
        },
        TARGETS: {
            type: 'TARGETS',
            orientation: 'NATURAL',
            properties: {
                influence: {
                    property: 'impact_score',
                    defaultValue: 0.5
                }
            }
        },
        HAS_VULNERABILITY: {
            type: 'HAS_VULNERABILITY',
            orientation: 'NATURAL',
            properties: {
                influence: {
                    property: 'exposure_score',
                    defaultValue: 0.5
                }
            }
        },
        USES_TECHNIQUE: {
            type: 'USES_TECHNIQUE',
            orientation: 'NATURAL',
            properties: {
                influence: {
                    property: 'proficiency',
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
// STEP 2: Calculate λmax (Dominant Eigenvalue) using PageRank as proxy
// ============================================

// PageRank approximates the dominant eigenvector
// The largest PageRank value is proportional to λmax
CALL gds.pageRank.stream('psychohistory_epidemic', {
    maxIterations: 100,
    dampingFactor: 0.85,
    relationshipWeightProperty: 'influence'
})
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS node, score
ORDER BY score DESC
LIMIT 1
WITH score AS max_pagerank, score * 10 AS lambda_max_estimate
RETURN
    'Dominant Eigenvalue (λmax) estimate: ' + toString(lambda_max_estimate) AS result,
    lambda_max_estimate,
    'Based on maximum PageRank: ' + toString(max_pagerank) AS note;

// ============================================
// STEP 3: Calculate R₀ for Different Scenarios
// ============================================

// Scenario 1: High influence, low skepticism (β=0.8, γ=0.2)
WITH 0.8 AS beta, 0.2 AS gamma
CALL gds.pageRank.stream('psychohistory_epidemic', {
    maxIterations: 100,
    dampingFactor: 0.85,
    relationshipWeightProperty: 'influence'
})
YIELD nodeId, score
WITH beta, gamma, score AS max_pagerank
ORDER BY max_pagerank DESC
LIMIT 1
WITH beta, gamma, max_pagerank * 10 AS lambda_max
WITH (beta / gamma) * lambda_max AS R0,
     beta, gamma, lambda_max
RETURN
    'SCENARIO 1: High Influence, Low Skepticism' AS scenario,
    R0,
    CASE
        WHEN R0 > 1 THEN 'EPIDEMIC WILL SPREAD (R₀ > 1)'
        ELSE 'EPIDEMIC WILL NOT SPREAD (R₀ < 1)'
    END AS prediction,
    beta AS infection_rate,
    gamma AS recovery_rate,
    lambda_max AS network_structure_factor
ORDER BY R0 DESC;

// Scenario 2: Moderate influence, moderate skepticism (β=0.5, γ=0.5)
WITH 0.5 AS beta, 0.5 AS gamma
CALL gds.pageRank.stream('psychohistory_epidemic', {
    maxIterations: 100,
    dampingFactor: 0.85,
    relationshipWeightProperty: 'influence'
})
YIELD nodeId, score
WITH beta, gamma, score AS max_pagerank
ORDER BY max_pagerank DESC
LIMIT 1
WITH beta, gamma, max_pagerank * 10 AS lambda_max
WITH (beta / gamma) * lambda_max AS R0,
     beta, gamma, lambda_max
RETURN
    'SCENARIO 2: Moderate Influence, Moderate Skepticism' AS scenario,
    R0,
    CASE
        WHEN R0 > 1 THEN 'EPIDEMIC WILL SPREAD (R₀ > 1)'
        ELSE 'EPIDEMIC WILL NOT SPREAD (R₀ < 1)'
    END AS prediction,
    beta AS infection_rate,
    gamma AS recovery_rate,
    lambda_max AS network_structure_factor;

// Scenario 3: Low influence, high skepticism (β=0.3, γ=0.7)
WITH 0.3 AS beta, 0.7 AS gamma
CALL gds.pageRank.stream('psychohistory_epidemic', {
    maxIterations: 100,
    dampingFactor: 0.85,
    relationshipWeightProperty: 'influence'
})
YIELD nodeId, score
WITH beta, gamma, score AS max_pagerank
ORDER BY max_pagerank DESC
LIMIT 1
WITH beta, gamma, max_pagerank * 10 AS lambda_max
WITH (beta / gamma) * lambda_max AS R0,
     beta, gamma, lambda_max
RETURN
    'SCENARIO 3: Low Influence, High Skepticism' AS scenario,
    R0,
    CASE
        WHEN R0 > 1 THEN 'EPIDEMIC WILL SPREAD (R₀ > 1)'
        ELSE 'EPIDEMIC WILL NOT SPREAD (R₀ < 1)'
    END AS prediction,
    beta AS infection_rate,
    gamma AS recovery_rate,
    lambda_max AS network_structure_factor;

// ============================================
// STEP 4: Identify Critical Nodes (Super-spreaders)
// ============================================

// Find nodes with highest epidemic potential
CALL gds.pageRank.stream('psychohistory_epidemic', {
    maxIterations: 100,
    dampingFactor: 0.85,
    relationshipWeightProperty: 'influence'
})
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS node, score
WHERE node:Technique OR node:Vulnerability OR node:Threat_Actor
WITH node, score,
     labels(node)[0] AS node_type,
     CASE
         WHEN node.name IS NOT NULL THEN node.name
         WHEN node.id IS NOT NULL THEN node.id
         ELSE 'Unknown'
     END AS node_name
ORDER BY score DESC
LIMIT 20
RETURN
    node_type,
    node_name,
    score AS epidemic_potential,
    CASE
        WHEN score > 0.05 THEN 'CRITICAL SUPER-SPREADER'
        WHEN score > 0.02 THEN 'HIGH INFLUENCE'
        WHEN score > 0.01 THEN 'MODERATE INFLUENCE'
        ELSE 'LOW INFLUENCE'
    END AS threat_level;

// ============================================
// STEP 5: Calculate Per-Node R₀ Contribution
// ============================================

// For each high-value node, calculate how much it contributes to R₀
WITH 0.7 AS beta, 0.3 AS gamma
CALL gds.pageRank.stream('psychohistory_epidemic', {
    maxIterations: 100,
    dampingFactor: 0.85,
    relationshipWeightProperty: 'influence'
})
YIELD nodeId, score
WITH beta, gamma, gds.util.asNode(nodeId) AS node, score
WHERE score > 0.01
WITH beta, gamma, node, score,
     labels(node)[0] AS node_type,
     CASE
         WHEN node.name IS NOT NULL THEN node.name
         WHEN node.id IS NOT NULL THEN node.id
         ELSE 'Unknown'
     END AS node_name,
     (beta / gamma) * (score * 10) AS node_R0
ORDER BY node_R0 DESC
LIMIT 50
RETURN
    node_type,
    node_name,
    node_R0,
    CASE
        WHEN node_R0 > 10 THEN 'EXTREME EPIDEMIC RISK'
        WHEN node_R0 > 5 THEN 'HIGH EPIDEMIC RISK'
        WHEN node_R0 > 2 THEN 'MODERATE EPIDEMIC RISK'
        WHEN node_R0 > 1 THEN 'LOW EPIDEMIC RISK'
        ELSE 'MINIMAL EPIDEMIC RISK'
    END AS risk_assessment,
    'Removing this node would reduce R₀ by ' + toString(round(node_R0 * 100) / 100) AS mitigation_impact;

// ============================================
// STEP 6: Network Vulnerability Analysis
// ============================================

// Calculate degree distribution to understand network structure
MATCH (n)
WHERE n:Technique OR n:Vulnerability OR n:ICS_Asset OR n:Threat_Actor
WITH n,
     labels(n)[0] AS node_type,
     size([(n)-[]->() | 1]) AS out_degree,
     size([(n)<-[]-() | 1]) AS in_degree
WITH node_type, out_degree + in_degree AS total_degree
RETURN
    node_type,
    avg(total_degree) AS avg_degree,
    max(total_degree) AS max_degree,
    min(total_degree) AS min_degree,
    stdev(total_degree) AS degree_variance,
    CASE
        WHEN stdev(total_degree) > avg(total_degree) THEN 'SCALE-FREE (High epidemic risk)'
        ELSE 'RANDOM (Lower epidemic risk)'
    END AS network_topology
ORDER BY avg_degree DESC;

// ============================================
// STEP 7: Validation Tests
// ============================================

// Test 1: Verify graph projection exists
CALL gds.graph.exists('psychohistory_epidemic') YIELD exists
RETURN
    'TEST 1: Graph Projection' AS test_name,
    CASE WHEN exists THEN 'PASS' ELSE 'FAIL' END AS result,
    exists AS graph_exists;

// Test 2: Verify node count > 0
CALL gds.graph.list('psychohistory_epidemic')
YIELD graphName, nodeCount, relationshipCount
RETURN
    'TEST 2: Graph Content' AS test_name,
    CASE WHEN nodeCount > 0 AND relationshipCount > 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    nodeCount AS nodes,
    relationshipCount AS relationships;

// Test 3: Verify R₀ calculation produces valid results
WITH 0.8 AS beta, 0.2 AS gamma
CALL gds.pageRank.stream('psychohistory_epidemic', {
    maxIterations: 100,
    dampingFactor: 0.85,
    relationshipWeightProperty: 'influence'
})
YIELD nodeId, score
WITH beta, gamma, max(score) AS max_pagerank
WITH (beta / gamma) * (max_pagerank * 10) AS R0
RETURN
    'TEST 3: R₀ Calculation' AS test_name,
    CASE WHEN R0 > 0 AND R0 < 1000 THEN 'PASS' ELSE 'FAIL' END AS result,
    R0 AS calculated_R0,
    CASE
        WHEN R0 > 1 THEN 'Epidemic threshold exceeded'
        ELSE 'Below epidemic threshold'
    END AS interpretation;

// ============================================
// STEP 8: Cleanup (Optional - run separately if needed)
// ============================================

// CALL gds.graph.drop('psychohistory_epidemic') YIELD graphName
// RETURN 'Dropped graph: ' + graphName AS cleanup_status;
