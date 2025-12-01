// =============================================================================
// GAP-ML-005: Test Existing EWS Queries
// =============================================================================
// File: src/ews-streaming/01_test_existing_queries.cypher
// Created: 2025-11-30
// Purpose: Verify existing EWS queries work against aeon-neo4j-dev
// Database: bolt://aeon-neo4j-dev:7687
// =============================================================================

// -----------------------------------------------------------------------------
// TEST 1: Verify APOC functions exist (from 05_autocorrelation_COMPUTED.cypher)
// -----------------------------------------------------------------------------
CALL apoc.help('psychohistory') YIELD name
RETURN name
ORDER BY name;

// Expected functions:
// - psychohistory.listMean
// - psychohistory.listVariance
// - psychohistory.lagOneAutocorrelation
// - psychohistory.criticalSlowingFromTimeSeries

// -----------------------------------------------------------------------------
// TEST 2: Create sample Actor nodes with EWS metrics (if not exist)
// -----------------------------------------------------------------------------
MERGE (a:Actor {id: 'ACTOR-TEST-001', name: 'Test Actor Stable'})
SET a.ews_variance = 0.2,
    a.ews_autocorrelation = 0.3,
    a.ews_critical_distance = 0.8,
    a.last_updated = datetime();

MERGE (a:Actor {id: 'ACTOR-TEST-002', name: 'Test Actor Warning'})
SET a.ews_variance = 0.6,
    a.ews_autocorrelation = 0.7,
    a.ews_critical_distance = 0.3,
    a.last_updated = datetime();

MERGE (a:Actor {id: 'ACTOR-TEST-003', name: 'Test Actor Critical'})
SET a.ews_variance = 0.9,
    a.ews_autocorrelation = 0.95,
    a.ews_critical_distance = 0.15,
    a.last_updated = datetime();

// -----------------------------------------------------------------------------
// TEST 3: EWS Threshold Query (from GAP-ML-005 spec line 104-114)
// -----------------------------------------------------------------------------
MATCH (a:Actor)
WHERE a.ews_variance > 0.8
   OR a.ews_autocorrelation > 0.9
   OR a.ews_critical_distance < 0.2
WITH a,
     CASE
       WHEN a.ews_critical_distance < 0.1 THEN 'CRITICAL'
       WHEN a.ews_critical_distance < 0.2 THEN 'HIGH'
       ELSE 'MEDIUM'
     END as severity
RETURN a.id,
       a.name,
       severity,
       a.ews_variance,
       a.ews_autocorrelation,
       a.ews_critical_distance
ORDER BY a.ews_critical_distance ASC;

// Expected: ACTOR-TEST-003 with CRITICAL or HIGH severity

// -----------------------------------------------------------------------------
// TEST 4: Compute Critical Slowing from Time Series
// -----------------------------------------------------------------------------
// Test with sample time series data
WITH [10.0, 10.2, 10.1, 10.5, 10.3, 10.8, 10.6, 11.0, 10.9, 11.2] AS stable_series,
     [10.0, 12.0, 8.0, 14.0, 6.0, 16.0, 4.0, 18.0, 2.0, 20.0] AS volatile_series

WITH stable_series, volatile_series,
     psychohistory.criticalSlowingFromTimeSeries(stable_series) AS stable_analysis,
     psychohistory.criticalSlowingFromTimeSeries(volatile_series) AS volatile_analysis

RETURN
  'Stable Series' AS series_type,
  stable_analysis.variance AS variance,
  stable_analysis.autocorrelation AS autocorr,
  stable_analysis.critical_slowing_indicator AS csi,
  stable_analysis.interpretation AS status

UNION ALL

WITH [10.0, 10.2, 10.1, 10.5, 10.3, 10.8, 10.6, 11.0, 10.9, 11.2] AS stable_series,
     [10.0, 12.0, 8.0, 14.0, 6.0, 16.0, 4.0, 18.0, 2.0, 20.0] AS volatile_series

WITH psychohistory.criticalSlowingFromTimeSeries(volatile_series) AS volatile_analysis

RETURN
  'Volatile Series' AS series_type,
  volatile_analysis.variance AS variance,
  volatile_analysis.autocorrelation AS autocorr,
  volatile_analysis.critical_slowing_indicator AS csi,
  volatile_analysis.interpretation AS status;

// Expected: volatile_series has higher CSI than stable_series

// -----------------------------------------------------------------------------
// TEST 5: Seldon Crisis Detection (from 05_seldon_crisis_detection.cypher)
// -----------------------------------------------------------------------------
MATCH (sc:SeldonCrisis)
MATCH (ci:CrisisIndicator)-[:INDICATES]->(sc)
WHERE ci.current_value IS NOT NULL
WITH sc, collect({
  name: ci.name,
  type: ci.type,
  threshold: ci.threshold,
  operator: ci.operator,
  current_value: ci.current_value,
  weight: ci.weight,
  triggered: CASE
    WHEN ci.operator = '>' AND ci.current_value > ci.threshold THEN true
    WHEN ci.operator = '<' AND ci.current_value < ci.threshold THEN true
    ELSE false
  END
}) as indicators
WITH sc, indicators,
     [i IN indicators WHERE i.triggered = true AND i.type = 'leading'] as leading_triggered,
     [i IN indicators WHERE i.triggered = true AND i.type = 'lagging'] as lagging_triggered
WITH sc, indicators, leading_triggered, lagging_triggered,
     reduce(s = 0.0, i IN leading_triggered | s + i.weight) as leading_score,
     reduce(s = 0.0, i IN lagging_triggered | s + i.weight) as lagging_score
RETURN sc.name as crisis,
       sc.intervention_window_months as intervention_months,
       sc.probability_baseline as baseline,
       leading_score as leading_indicator_score,
       lagging_score as lagging_indicator_score,
       sc.probability_baseline + (leading_score * 0.3) + (lagging_score * 0.5) as composite_probability,
       CASE
         WHEN sc.probability_baseline + (leading_score * 0.3) + (lagging_score * 0.5) > 0.8 THEN 'CRISIS_IMMINENT'
         WHEN sc.probability_baseline + (leading_score * 0.3) + (lagging_score * 0.5) > 0.6 THEN 'CRISIS_LIKELY'
         WHEN sc.probability_baseline + (leading_score * 0.3) + (lagging_score * 0.5) > 0.4 THEN 'ELEVATED_RISK'
         ELSE 'MONITORING'
       END as status,
       [i IN leading_triggered | i.name] as triggered_leading,
       [i IN lagging_triggered | i.name] as triggered_lagging
ORDER BY composite_probability DESC;

// -----------------------------------------------------------------------------
// TEST 6: Verify Actor EWS property indexes exist
// -----------------------------------------------------------------------------
CALL db.indexes() YIELD name, type, labelsOrTypes, properties
WHERE 'Actor' IN labelsOrTypes
  AND (
    'ews_variance' IN properties OR
    'ews_autocorrelation' IN properties OR
    'ews_critical_distance' IN properties
  )
RETURN name, type, properties;

// If indexes don't exist, create them:
// CREATE INDEX actor_ews_variance_idx IF NOT EXISTS FOR (a:Actor) ON (a.ews_variance);
// CREATE INDEX actor_ews_autocorr_idx IF NOT EXISTS FOR (a:Actor) ON (a.ews_autocorrelation);
// CREATE INDEX actor_ews_distance_idx IF NOT EXISTS FOR (a:Actor) ON (a.ews_critical_distance);

// =============================================================================
// END OF TEST QUERIES
// =============================================================================
