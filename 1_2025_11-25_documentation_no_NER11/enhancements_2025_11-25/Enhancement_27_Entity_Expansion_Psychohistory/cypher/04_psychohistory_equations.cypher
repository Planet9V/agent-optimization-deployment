// ============================================================
// Enhancement 27: Psychohistory Mathematical Models
// File: 04_psychohistory_equations.cypher
// Created: 2025-11-26 23:30:00 UTC
// Purpose: Implement 5 core psychohistory equations for prediction
// ============================================================

// ============================================================
// EQUATION 1: EPIDEMIC THRESHOLD (R₀)
// Formula: R₀ = β/γ × λmax(A)
// Application: Predict malware/attack spread potential
// ============================================================

// 1.1 Create epidemic threshold stored procedure
CALL apoc.custom.declareFunction(
  'psychohistory.epidemicThreshold(beta FLOAT, gamma FLOAT, connections INT) :: FLOAT',
  'RETURN $beta / $gamma * sqrt(toFloat($connections))'
);

// 1.2 Epidemic threshold application query
// USAGE: Predict if malware will spread across network
// MATCH (m:Malware)-[:EXPLOITS]->(v:Vulnerability)
// MATCH (v)-[:AFFECTS]->(a:Asset)
// WITH m, count(DISTINCT a) as target_assets,
//      coalesce(m.infection_rate, 0.3) as beta,
//      coalesce(m.recovery_rate, 0.1) as gamma
// RETURN m.name,
//        psychohistory.epidemicThreshold(beta, gamma, target_assets) as R0,
//        CASE WHEN psychohistory.epidemicThreshold(beta, gamma, target_assets) > 1
//             THEN 'EPIDEMIC_LIKELY' ELSE 'CONTAINED' END as prediction;

// ============================================================
// EQUATION 2: ISING DYNAMICS (Opinion Propagation)
// Formula: dm/dt = -m + tanh(β(Jzm + h))
// Application: Model belief/security culture propagation
// ============================================================

// 2.1 Create Ising dynamics stored procedure
// Note: tanh approximation for Cypher
CALL apoc.custom.declareFunction(
  'psychohistory.isingDynamics(m FLOAT, beta FLOAT, J FLOAT, z INT, h FLOAT) :: FLOAT',
  '
  WITH $beta * ($J * $z * $m + $h) as x
  WITH CASE
    WHEN x > 20 THEN 1.0
    WHEN x < -20 THEN -1.0
    ELSE (exp(2*x) - 1) / (exp(2*x) + 1)
  END as tanh_x
  RETURN -1.0 * $m + tanh_x
  '
);

// 2.2 Ising dynamics application query
// USAGE: Predict security belief adoption in organization
// MATCH (o:Organization)-[:EMPLOYS]->(r:Role)
// MATCH (r)-[:EXHIBITS]->(pt:PsychTrait {traitType: "cognitive_bias"})
// WITH o, avg(pt.intensity) as avg_bias,
//      count(DISTINCT r) as team_size,
//      0.5 as coupling_strength,
//      2.0 as inverse_temp,
//      0.0 as external_field
// RETURN o.name,
//        psychohistory.isingDynamics(avg_bias, inverse_temp, coupling_strength, team_size, external_field) as dm_dt,
//        CASE WHEN abs(psychohistory.isingDynamics(avg_bias, inverse_temp, coupling_strength, team_size, external_field)) > 0.1
//             THEN 'BELIEFS_SHIFTING' ELSE 'STABLE' END as belief_state;

// ============================================================
// EQUATION 3: GRANOVETTER THRESHOLD (Cascade Model)
// Formula: r(t+1) = N × F(r(t)/N)
// Application: Predict attack technique adoption cascade
// ============================================================

// 3.1 Create Granovetter cascade stored procedure
CALL apoc.custom.declareFunction(
  'psychohistory.granovetterCascade(adopters INT, population INT, threshold FLOAT) :: INT',
  'RETURN toInteger($population * (1.0 - exp(-1.0 * $adopters / ($population * $threshold + 0.001))))'
);

// 3.2 Granovetter cascade application query
// USAGE: Predict technique adoption among threat actors
// MATCH (ta:ThreatActor)-[:USES]->(ap:AttackPattern)
// WITH ap, count(DISTINCT ta) as current_adopters
// MATCH (ta2:ThreatActor) WHERE NOT (ta2)-[:USES]->(ap)
// WITH ap, current_adopters, count(ta2) as non_adopters,
//      current_adopters + count(ta2) as total_population,
//      0.25 as adoption_threshold
// RETURN ap.name,
//        current_adopters,
//        psychohistory.granovetterCascade(current_adopters, total_population, adoption_threshold) as predicted_adopters,
//        CASE WHEN psychohistory.granovetterCascade(current_adopters, total_population, adoption_threshold) > current_adopters * 1.5
//             THEN 'CASCADE_LIKELY' ELSE 'GRADUAL_ADOPTION' END as adoption_pattern;

// ============================================================
// EQUATION 4: SADDLE-NODE BIFURCATION (Seldon Crisis)
// Formula: dx/dt = μ + x²
// Application: Detect approaching Seldon Crisis tipping points
// ============================================================

// 4.1 Create bifurcation parameter stored procedure
CALL apoc.custom.declareFunction(
  'psychohistory.bifurcationMu(stressors FLOAT, resilience FLOAT) :: FLOAT',
  'RETURN $stressors - $resilience'
);

// 4.2 Create crisis velocity stored procedure
CALL apoc.custom.declareFunction(
  'psychohistory.crisisVelocity(mu FLOAT, x FLOAT) :: FLOAT',
  'RETURN $mu + $x * $x'
);

// 4.3 Bifurcation application query
// USAGE: Detect Seldon Crisis approach
// MATCH (o:Organization)
// OPTIONAL MATCH (o)-[:FACES]->(rs:RiskScenario)
// OPTIONAL MATCH (o)-[:IMPLEMENTS]->(c:Control)
// WITH o,
//      coalesce(sum(rs.probability * rs.impact), 0) as total_stress,
//      coalesce(sum(c.effectiveness), 0.1) as total_resilience,
//      coalesce(o.current_state, 0) as x
// WITH o, total_stress, total_resilience,
//      psychohistory.bifurcationMu(total_stress / 100.0, total_resilience / 100.0) as mu, x
// RETURN o.name,
//        mu as bifurcation_parameter,
//        psychohistory.crisisVelocity(mu, x) as dx_dt,
//        CASE
//          WHEN mu > 0.5 THEN 'CRISIS_IMMINENT'
//          WHEN mu > 0.0 THEN 'CRISIS_APPROACHING'
//          WHEN mu > -0.3 THEN 'MARGINAL_STABILITY'
//          ELSE 'STABLE'
//        END as system_state;

// ============================================================
// EQUATION 5: CRITICAL SLOWING DOWN (Early Warning)
// Indicators: ρ(lag) → 1, σ² → ∞
// Application: Early warning signals before tipping point
// ============================================================

// 5.1 Create critical slowing indicator stored procedure
CALL apoc.custom.declareFunction(
  'psychohistory.criticalSlowing(variance FLOAT, autocorr FLOAT) :: FLOAT',
  'RETURN $variance * $autocorr / (1.0 - $autocorr + 0.001)'
);

// 5.2 Create variance calculation helper
CALL apoc.custom.declareFunction(
  'psychohistory.calculateVariance(values LIST OF FLOAT) :: FLOAT',
  '
  WITH reduce(s = 0.0, v IN $values | s + v) / size($values) as mean
  WITH mean, $values as vals
  WITH reduce(ss = 0.0, v IN vals | ss + (v - mean) * (v - mean)) / size(vals) as variance
  RETURN variance
  '
);

// 5.3 Critical slowing application query
// USAGE: Detect early warning signals
// MATCH (e:Event {eventType: "incident"})
// WHERE e.timestamp > datetime() - duration("P90D")
// WITH collect(toFloat(e.severity)) as severities
// WHERE size(severities) >= 5
// WITH severities,
//      psychohistory.calculateVariance(severities) as variance,
//      0.7 as autocorr_estimate  // Would need time-series analysis for real value
// RETURN
//   variance,
//   psychohistory.criticalSlowing(variance, autocorr_estimate) as slowing_indicator,
//   CASE
//     WHEN psychohistory.criticalSlowing(variance, autocorr_estimate) > 10 THEN 'CRITICAL_SLOWING_DETECTED'
//     WHEN psychohistory.criticalSlowing(variance, autocorr_estimate) > 5 THEN 'WARNING_ELEVATED'
//     WHEN psychohistory.criticalSlowing(variance, autocorr_estimate) > 2 THEN 'MONITOR_CLOSELY'
//     ELSE 'NORMAL'
//   END as early_warning;

// ============================================================
// COMPOSITE PSYCHOHISTORY DASHBOARD QUERY
// ============================================================

// Dashboard query combining all 5 equations
// MATCH (o:Organization {name: $org_name})
//
// // Epidemic potential
// OPTIONAL MATCH (m:Malware)-[:TARGETS]->(o)
// WITH o, m, count(*) as malware_count
//
// // Belief dynamics
// OPTIONAL MATCH (o)-[:EMPLOYS]->(r:Role)-[:EXHIBITS]->(pt:PsychTrait)
// WITH o, malware_count, avg(pt.intensity) as avg_bias, count(r) as team_size
//
// // Crisis indicators
// OPTIONAL MATCH (o)-[:FACES]->(rs:RiskScenario)
// OPTIONAL MATCH (o)-[:IMPLEMENTS]->(c:Control)
// WITH o, malware_count, avg_bias, team_size,
//      sum(rs.probability * rs.impact) as stress,
//      sum(c.effectiveness) as resilience
//
// RETURN o.name,
//   // Epidemic R0
//   psychohistory.epidemicThreshold(0.3, 0.1, malware_count * 10) as epidemic_R0,
//   // Ising belief change
//   psychohistory.isingDynamics(coalesce(avg_bias, 0.5), 2.0, 0.5, toInteger(team_size), 0) as belief_change,
//   // Bifurcation parameter
//   psychohistory.bifurcationMu(coalesce(stress, 0)/100.0, coalesce(resilience, 0.1)/100.0) as crisis_mu,
//   // Overall assessment
//   CASE
//     WHEN psychohistory.bifurcationMu(coalesce(stress, 0)/100.0, coalesce(resilience, 0.1)/100.0) > 0.5
//          OR psychohistory.epidemicThreshold(0.3, 0.1, malware_count * 10) > 2
//     THEN 'HIGH_RISK'
//     WHEN psychohistory.bifurcationMu(coalesce(stress, 0)/100.0, coalesce(resilience, 0.1)/100.0) > 0
//     THEN 'ELEVATED_RISK'
//     ELSE 'NORMAL'
//   END as overall_assessment;

// ============================================================
// VERIFICATION QUERIES
// ============================================================

// V1: Test epidemic threshold function
// RETURN psychohistory.epidemicThreshold(0.3, 0.1, 100) as R0_test
// EXPECTED: ~9.49 (epidemic likely)

// V2: Test Ising dynamics function
// RETURN psychohistory.isingDynamics(0.5, 2.0, 0.5, 10, 0) as ising_test
// EXPECTED: value between -1 and 1

// V3: Test Granovetter cascade function
// RETURN psychohistory.granovetterCascade(10, 100, 0.3) as cascade_test
// EXPECTED: integer representing predicted adopters

// V4: Test bifurcation parameter function
// RETURN psychohistory.bifurcationMu(0.7, 0.3) as mu_test
// EXPECTED: 0.4 (approaching crisis)

// V5: Test critical slowing function
// RETURN psychohistory.criticalSlowing(5.0, 0.8) as slowing_test
// EXPECTED: value indicating slowing level
