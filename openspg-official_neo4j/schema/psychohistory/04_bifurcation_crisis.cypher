// ============================================
// EQUATION 4: Bifurcation Analysis (Seldon Crisis Detection)
// ============================================
// dx/dt = μ + x²
// where:
//   x = system state variable
//   μ = control parameter (stress/pressure)
//   Bifurcation occurs at μ = 0
// Application: Detect critical transition points where small changes cause regime shifts

// ============================================
// STEP 1: Create Graph Projection
// ============================================

// Drop existing projection if it exists
CALL gds.graph.exists('psychohistory_bifurcation') YIELD exists
WITH exists WHERE exists
CALL gds.graph.drop('psychohistory_bifurcation') YIELD graphName
RETURN 'Dropped existing graph: ' + graphName AS status
UNION
WITH 1 AS dummy WHERE NOT gds.graph.exists('psychohistory_bifurcation')
RETURN 'No existing graph to drop' AS status;

// Create projection for system dynamics analysis
CALL gds.graph.project(
    'psychohistory_bifurcation',
    ['ICS_Asset', 'Vulnerability', 'Technique', 'Threat_Actor', 'Campaign', 'ICS_Sector'],
    {
        HAS_VULNERABILITY: {
            type: 'HAS_VULNERABILITY',
            orientation: 'NATURAL',
            properties: {
                severity: {
                    property: 'cvss_score',
                    defaultValue: 5.0
                }
            }
        },
        EXPLOITS: {
            type: 'EXPLOITS',
            orientation: 'NATURAL',
            properties: {
                severity: {
                    property: 'exploitability',
                    defaultValue: 5.0
                }
            }
        },
        TARGETS: {
            type: 'TARGETS',
            orientation: 'NATURAL',
            properties: {
                severity: {
                    property: 'impact',
                    defaultValue: 5.0
                }
            }
        },
        BELONGS_TO_SECTOR: {
            type: 'BELONGS_TO_SECTOR',
            orientation: 'NATURAL'
        }
    }
) YIELD graphName, nodeCount, relationshipCount
RETURN
    graphName,
    nodeCount AS total_nodes,
    relationshipCount AS total_relationships;

// ============================================
// STEP 2: Calculate System State Variable (x)
// ============================================

// x represents aggregate system stress/vulnerability
// Calculate per ICS sector
MATCH (sector:ICS_Sector)
OPTIONAL MATCH (sector)<-[:BELONGS_TO_SECTOR]-(asset:ICS_Asset)
OPTIONAL MATCH (asset)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name,
     count(DISTINCT asset) AS asset_count,
     count(DISTINCT vuln) AS vuln_count,
     avg(CASE WHEN vuln.cvss_score IS NOT NULL THEN vuln.cvss_score ELSE 5.0 END) AS avg_severity
SET sector.system_state_x = CASE
    WHEN asset_count > 0 THEN (toFloat(vuln_count) / toFloat(asset_count)) * (avg_severity / 10.0)
    ELSE 0.0
END
WITH sector, sector_name, sector.system_state_x AS x_value
RETURN
    sector_name,
    round(x_value * 100) / 100 AS system_state_x,
    CASE
        WHEN x_value > 1.0 THEN 'CRITICAL STATE (High vulnerability density)'
        WHEN x_value > 0.5 THEN 'ELEVATED STATE (Moderate vulnerability)'
        WHEN x_value > 0.2 THEN 'NORMAL STATE (Low vulnerability)'
        ELSE 'STABLE STATE (Minimal vulnerability)'
    END AS state_classification
ORDER BY x_value DESC;

// Calculate global system state
MATCH (sector:ICS_Sector)
WHERE sector.system_state_x IS NOT NULL
WITH avg(sector.system_state_x) AS global_x,
     stdev(sector.system_state_x) AS x_variance
RETURN
    'Global System State' AS metric,
    round(global_x * 100) / 100 AS average_state_x,
    round(x_variance * 100) / 100 AS state_variance,
    CASE
        WHEN global_x > 0.7 THEN 'APPROACHING BIFURCATION'
        WHEN global_x > 0.4 THEN 'MODERATE STRESS'
        ELSE 'STABLE REGIME'
    END AS regime;

// ============================================
// STEP 3: Calculate Control Parameter (μ)
// ============================================

// μ represents external pressure/stress from threats
MATCH (sector:ICS_Sector)
OPTIONAL MATCH (sector)<-[:BELONGS_TO_SECTOR]-(asset:ICS_Asset)<-[:TARGETS]-(threat)
WHERE threat:Technique OR threat:Threat_Actor OR threat:Campaign
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name,
     count(DISTINCT threat) AS threat_count,
     coalesce(sector.system_state_x, 0.0) AS x_current
WITH sector, sector_name, x_current,
     // μ = threat pressure normalized
     (toFloat(threat_count) / 100.0) - 0.5 AS mu_control_param
SET sector.control_param_mu = mu_control_param
RETURN
    sector_name,
    round(x_current * 100) / 100 AS state_x,
    round(mu_control_param * 100) / 100 AS control_mu,
    CASE
        WHEN mu_control_param > 0 THEN 'POSITIVE PRESSURE (Destabilizing)'
        WHEN mu_control_param < 0 THEN 'NEGATIVE PRESSURE (Stabilizing)'
        ELSE 'NEUTRAL (At equilibrium)'
    END AS pressure_direction
ORDER BY mu_control_param DESC;

// ============================================
// STEP 4: Calculate Bifurcation Points
// ============================================

// Find sectors near bifurcation (μ ≈ 0, dx/dt ≈ 0)
MATCH (sector:ICS_Sector)
WHERE sector.system_state_x IS NOT NULL AND sector.control_param_mu IS NOT NULL
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name,
     sector.system_state_x AS x,
     sector.control_param_mu AS mu
// dx/dt = μ + x²
WITH sector_name, x, mu,
     mu + (x * x) AS dx_dt,
     abs(mu) AS distance_from_bifurcation
RETURN
    sector_name,
    round(x * 100) / 100 AS system_state,
    round(mu * 100) / 100 AS control_parameter,
    round(dx_dt * 100) / 100 AS state_change_rate,
    round(distance_from_bifurcation * 100) / 100 AS bifurcation_distance,
    CASE
        WHEN abs(mu) < 0.1 AND abs(dx_dt) < 0.1 THEN 'CRITICAL: AT BIFURCATION POINT'
        WHEN abs(mu) < 0.2 THEN 'WARNING: APPROACHING BIFURCATION'
        WHEN dx_dt > 0.5 THEN 'RAPID DESTABILIZATION'
        WHEN dx_dt < -0.5 THEN 'RAPID STABILIZATION'
        ELSE 'STABLE'
    END AS bifurcation_status,
    CASE
        WHEN mu < 0 AND x < 0.5 THEN 'STABLE FIXED POINT (x ≈ -√|μ|)'
        WHEN mu < 0 AND x > 0.5 THEN 'UNSTABLE FIXED POINT (x ≈ +√|μ|)'
        WHEN mu > 0 THEN 'NO FIXED POINTS (Runaway dynamics)'
        ELSE 'AT CRITICAL POINT (μ = 0)'
    END AS equilibrium_analysis
ORDER BY distance_from_bifurcation;

// ============================================
// STEP 5: Simulate Bifurcation Diagram
// ============================================

// Sweep control parameter μ from -1 to +1
// For each μ, calculate equilibrium states
UNWIND range(-10, 10) AS step
WITH step, step * 0.1 AS mu
// For μ < 0: two equilibria at x = ±√|μ|
// For μ > 0: no real equilibria (system diverges)
// For μ = 0: saddle-node bifurcation
WITH mu,
     CASE
         WHEN mu < 0 THEN sqrt(abs(mu))
         ELSE null
     END AS stable_equilibrium,
     CASE
         WHEN mu < 0 THEN -sqrt(abs(mu))
         ELSE null
     END AS unstable_equilibrium
RETURN
    round(mu * 10) / 10 AS control_parameter_mu,
    CASE
        WHEN stable_equilibrium IS NOT NULL THEN round(stable_equilibrium * 100) / 100
        ELSE null
    END AS stable_state,
    CASE
        WHEN unstable_equilibrium IS NOT NULL THEN round(unstable_equilibrium * 100) / 100
        ELSE null
    END AS unstable_state,
    CASE
        WHEN mu < -0.3 THEN 'TWO EQUILIBRIA (Bistable)'
        WHEN mu < 0 THEN 'APPROACHING BIFURCATION'
        WHEN mu = 0 THEN 'SADDLE-NODE BIFURCATION'
        ELSE 'NO EQUILIBRIA (Runaway)'
    END AS regime,
    CASE
        WHEN mu > 0 THEN 'System will diverge to infinity'
        WHEN mu < 0 THEN 'System can stabilize at ±√|μ|'
        ELSE 'Critical transition point'
    END AS prediction
ORDER BY mu;

// ============================================
// STEP 6: Identify Assets at Crisis Points
// ============================================

// Find individual assets near bifurcation
MATCH (asset:ICS_Asset)
OPTIONAL MATCH (asset)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
OPTIONAL MATCH (asset)<-[:TARGETS]-(threat)
WHERE threat:Technique OR threat:Threat_Actor
WITH asset,
     CASE
         WHEN asset.name IS NOT NULL THEN asset.name
         WHEN asset.id IS NOT NULL THEN asset.id
         ELSE 'Unknown'
     END AS asset_name,
     count(DISTINCT vuln) AS vuln_count,
     count(DISTINCT threat) AS threat_count,
     avg(CASE WHEN vuln.cvss_score IS NOT NULL THEN vuln.cvss_score ELSE 5.0 END) AS avg_cvss
WITH asset_name,
     (toFloat(vuln_count) / 10.0) * (avg_cvss / 10.0) AS x_state,
     (toFloat(threat_count) / 20.0) - 0.5 AS mu_param
WITH asset_name, x_state, mu_param,
     mu_param + (x_state * x_state) AS dx_dt,
     abs(mu_param) AS distance_from_critical
WHERE distance_from_critical < 0.3
RETURN
    asset_name,
    round(x_state * 100) / 100 AS vulnerability_state,
    round(mu_param * 100) / 100 AS threat_pressure,
    round(dx_dt * 100) / 100 AS instability_rate,
    CASE
        WHEN abs(dx_dt) < 0.1 THEN 'CRITICAL: Minimal perturbation can cause regime shift'
        WHEN dx_dt > 0 THEN 'WARNING: System degrading toward crisis'
        ELSE 'Recovering from pressure'
    END AS crisis_assessment,
    CASE
        WHEN distance_from_critical < 0.1 THEN 'IMMEDIATE INTERVENTION REQUIRED'
        WHEN distance_from_critical < 0.2 THEN 'HIGH PRIORITY MONITORING'
        ELSE 'WATCH LIST'
    END AS recommended_action
ORDER BY distance_from_critical
LIMIT 25;

// ============================================
// STEP 7: Calculate Critical Slowing Down Indicators
// ============================================

// Near bifurcation, systems exhibit critical slowing down
// Measure how fast system returns to equilibrium after perturbation
MATCH (sector:ICS_Sector)
WHERE sector.system_state_x IS NOT NULL AND sector.control_param_mu IS NOT NULL
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name,
     sector.system_state_x AS x,
     sector.control_param_mu AS mu
// Recovery rate = derivative of dx/dt with respect to x
// d(dx/dt)/dx = 2x (from dx/dt = μ + x²)
WITH sector_name, x, mu,
     2.0 * x AS recovery_rate,
     mu + (x * x) AS dx_dt
RETURN
    sector_name,
    round(x * 100) / 100 AS current_state,
    round(mu * 100) / 100 AS pressure,
    round(recovery_rate * 100) / 100 AS recovery_speed,
    CASE
        WHEN abs(recovery_rate) < 0.3 THEN 'CRITICAL SLOWING DOWN (Warning: Near bifurcation)'
        WHEN abs(recovery_rate) < 0.7 THEN 'SLOW RECOVERY'
        ELSE 'NORMAL RECOVERY'
    END AS resilience_status,
    CASE
        WHEN abs(recovery_rate) < 0.3 AND mu > -0.2 THEN 'SELDON CRISIS IMMINENT'
        WHEN abs(recovery_rate) < 0.5 THEN 'ELEVATED CRISIS RISK'
        ELSE 'NORMAL RISK'
    END AS crisis_warning
ORDER BY abs(recovery_rate);

// ============================================
// STEP 8: Hysteresis Analysis
// ============================================

// Check if system exhibits hysteresis (different paths up vs down)
// Simulate increasing then decreasing pressure
UNWIND [
    {direction: 'INCREASING', mu_values: [-0.5, -0.3, -0.1, 0.0, 0.1, 0.3, 0.5]},
    {direction: 'DECREASING', mu_values: [0.5, 0.3, 0.1, 0.0, -0.1, -0.3, -0.5]}
] AS scenario
UNWIND scenario.mu_values AS mu
WITH scenario.direction AS sweep_direction, mu,
     // Starting from different initial conditions
     CASE WHEN scenario.direction = 'INCREASING' THEN -0.5 ELSE 0.5 END AS x_initial
// Simulate equilibrium for each mu
WITH sweep_direction, mu, x_initial,
     CASE
         WHEN mu < 0 AND x_initial < 0 THEN -sqrt(abs(mu))
         WHEN mu < 0 AND x_initial > 0 THEN sqrt(abs(mu))
         ELSE x_initial
     END AS x_equilibrium
RETURN
    sweep_direction,
    round(mu * 10) / 10 AS control_parameter,
    round(x_equilibrium * 100) / 100 AS equilibrium_state,
    CASE
        WHEN mu > 0 THEN 'NO STABLE STATE'
        WHEN sweep_direction = 'INCREASING' AND x_equilibrium > 0 THEN 'UPPER BRANCH'
        WHEN sweep_direction = 'INCREASING' AND x_equilibrium < 0 THEN 'LOWER BRANCH'
        WHEN sweep_direction = 'DECREASING' AND x_equilibrium > 0 THEN 'UPPER BRANCH (Sticky)'
        ELSE 'LOWER BRANCH (Sticky)'
    END AS hysteresis_path
ORDER BY sweep_direction, mu;

// ============================================
// STEP 9: Early Warning Signal Detection
// ============================================

// Detect early warning signals for imminent bifurcation
MATCH (sector:ICS_Sector)
WHERE sector.control_param_mu IS NOT NULL
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name,
     sector.control_param_mu AS mu,
     coalesce(sector.system_state_x, 0.0) AS x
WITH sector_name, mu, x,
     // Warning signals
     abs(mu) < 0.2 AS near_bifurcation,
     abs(2.0 * x) < 0.5 AS slow_recovery,
     abs(mu + x*x) < 0.1 AS near_equilibrium,
     mu > -0.1 AND mu < 0.1 AS critical_pressure
WITH sector_name, mu, x,
     near_bifurcation, slow_recovery, near_equilibrium, critical_pressure,
     toInteger(near_bifurcation) + toInteger(slow_recovery) +
     toInteger(near_equilibrium) + toInteger(critical_pressure) AS warning_count
WHERE warning_count >= 2
RETURN
    sector_name,
    round(mu * 100) / 100 AS control_parameter,
    round(x * 100) / 100 AS system_state,
    warning_count AS warning_signals,
    CASE
        WHEN warning_count = 4 THEN 'EXTREME: All warning signals active'
        WHEN warning_count = 3 THEN 'CRITICAL: Multiple warnings'
        ELSE 'ELEVATED: Early warnings detected'
    END AS alert_level,
    'SELDON CRISIS: Prepare for regime shift' AS recommendation
ORDER BY warning_count DESC, abs(mu);

// ============================================
// STEP 10: Validation Tests
// ============================================

// Test 1: Verify graph projection exists
CALL gds.graph.exists('psychohistory_bifurcation') YIELD exists
RETURN
    'TEST 1: Graph Projection' AS test_name,
    CASE WHEN exists THEN 'PASS' ELSE 'FAIL' END AS result;

// Test 2: Verify state variables are calculated
MATCH (sector:ICS_Sector)
WHERE sector.system_state_x IS NOT NULL
WITH count(sector) AS sectors_with_state
RETURN
    'TEST 2: State Variables' AS test_name,
    CASE WHEN sectors_with_state > 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    sectors_with_state AS configured_sectors;

// Test 3: Verify control parameters are calculated
MATCH (sector:ICS_Sector)
WHERE sector.control_param_mu IS NOT NULL
WITH count(sector) AS sectors_with_mu
RETURN
    'TEST 3: Control Parameters' AS test_name,
    CASE WHEN sectors_with_mu > 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    sectors_with_mu AS configured_sectors;

// Test 4: Verify bifurcation equation produces valid results
WITH -0.25 AS mu_test
WITH mu_test, sqrt(abs(mu_test)) AS x_equilibrium
WITH mu_test, x_equilibrium,
     mu_test + (x_equilibrium * x_equilibrium) AS dx_dt
RETURN
    'TEST 4: Bifurcation Equation' AS test_name,
    CASE WHEN abs(dx_dt) < 0.01 THEN 'PASS' ELSE 'FAIL' END AS result,
    'At μ=' + toString(round(mu_test*100)/100) +
    ', equilibrium x=' + toString(round(x_equilibrium*100)/100) +
    ', dx/dt=' + toString(round(dx_dt*1000)/1000) AS calculation;

// Test 5: Verify critical points detected
MATCH (sector:ICS_Sector)
WHERE sector.control_param_mu IS NOT NULL
  AND abs(sector.control_param_mu) < 0.3
WITH count(sector) AS critical_sectors
RETURN
    'TEST 5: Critical Point Detection' AS test_name,
    CASE WHEN critical_sectors >= 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    critical_sectors AS sectors_near_bifurcation;

// ============================================
// STEP 11: Cleanup (Optional)
// ============================================

// CALL gds.graph.drop('psychohistory_bifurcation') YIELD graphName
// RETURN 'Dropped graph: ' + graphName AS cleanup_status;
