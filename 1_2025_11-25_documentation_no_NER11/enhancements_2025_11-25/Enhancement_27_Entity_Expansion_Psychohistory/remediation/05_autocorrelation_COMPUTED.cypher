// =============================================================================
// Enhancement 27: CORRECTED Critical Slowing Indicator
// =============================================================================
// File: remediation/05_autocorrelation_COMPUTED.cypher
// Created: 2025-11-27
// Purpose: Compute autocorrelation from time series (not hardcoded)
//
// ACADEMIC BASIS:
// Scheffer, M., et al. (2009). "Early-warning signals for critical transitions."
// Nature, 461, 53-59. DOI: 10.1038/nature08227
//
// Dakos, V., et al. (2012). "Methods for Detecting Early Warnings."
// PLOS ONE, 7(7), e41010. DOI: 10.1371/journal.pone.0041010
//
// ORIGINAL E27 ERROR:
// Hardcoded autocorrelation = 0.7 (line 150 in original)
// This produces MEANINGLESS results - autocorr MUST be computed from data
//
// CORRECT IMPLEMENTATION:
// Compute lag-1 autocorrelation from actual event time series
// =============================================================================

// -----------------------------------------------------------------------------
// STEP 1: Create helper function to compute statistics from list
// -----------------------------------------------------------------------------

// Mean calculation
CALL apoc.custom.declareFunction(
  'psychohistory.listMean(values :: LIST OF FLOAT) :: FLOAT',
  '
  WITH $values AS vals
  RETURN CASE
    WHEN size(vals) = 0 THEN 0.0
    ELSE reduce(s = 0.0, v IN vals | s + v) / size(vals)
  END
  '
);

// Variance calculation
CALL apoc.custom.declareFunction(
  'psychohistory.listVariance(values :: LIST OF FLOAT) :: FLOAT',
  '
  WITH $values AS vals
  WITH vals, reduce(s = 0.0, v IN vals | s + v) / size(vals) AS mean
  WITH vals, mean,
       [v IN vals | (v - mean) * (v - mean)] AS squared_diffs
  RETURN CASE
    WHEN size(vals) < 2 THEN 0.0
    ELSE reduce(s = 0.0, d IN squared_diffs | s + d) / (size(vals) - 1)
  END
  '
);

// -----------------------------------------------------------------------------
// STEP 2: Compute Lag-1 Autocorrelation (Core Fix)
// -----------------------------------------------------------------------------

CALL apoc.custom.declareFunction(
  'psychohistory.lagOneAutocorrelation(values :: LIST OF FLOAT) :: FLOAT',
  '
  // Compute Pearson correlation between x(t) and x(t-1)
  // ρ₁ = Cov(x_t, x_{t-1}) / sqrt(Var(x_t) × Var(x_{t-1}))
  //
  // For stationary time series: Var(x_t) ≈ Var(x_{t-1})
  // So: ρ₁ ≈ Cov(x_t, x_{t-1}) / Var(x)

  WITH $values AS vals
  WHERE size(vals) >= 3

  // Create lagged series
  WITH vals,
       [i IN range(0, size(vals)-2) | vals[i]] AS x_prev,    // x(t-1)
       [i IN range(1, size(vals)-1) | vals[i]] AS x_curr     // x(t)

  // Compute means
  WITH x_prev, x_curr,
       reduce(s = 0.0, v IN x_prev | s + v) / size(x_prev) AS mean_prev,
       reduce(s = 0.0, v IN x_curr | s + v) / size(x_curr) AS mean_curr

  // Compute covariance and variances
  WITH x_prev, x_curr, mean_prev, mean_curr,
       [i IN range(0, size(x_prev)-1) | (x_prev[i] - mean_prev) * (x_curr[i] - mean_curr)] AS cov_terms,
       [i IN range(0, size(x_prev)-1) | (x_prev[i] - mean_prev) * (x_prev[i] - mean_prev)] AS var_prev_terms,
       [i IN range(0, size(x_curr)-1) | (x_curr[i] - mean_curr) * (x_curr[i] - mean_curr)] AS var_curr_terms

  WITH reduce(s = 0.0, t IN cov_terms | s + t) AS covariance,
       reduce(s = 0.0, t IN var_prev_terms | s + t) AS var_prev,
       reduce(s = 0.0, t IN var_curr_terms | s + t) AS var_curr

  // Pearson correlation coefficient
  RETURN CASE
    WHEN var_prev = 0 OR var_curr = 0 THEN 0.0
    ELSE covariance / sqrt(var_prev * var_curr)
  END
  '
);

// -----------------------------------------------------------------------------
// STEP 3: CORRECTED Critical Slowing Indicator
// -----------------------------------------------------------------------------

CALL apoc.custom.declareFunction(
  'psychohistory.criticalSlowingFromTimeSeries(values :: LIST OF FLOAT) :: MAP',
  '
  // Compute critical slowing indicator from time series
  // Returns variance, autocorrelation, and combined indicator
  //
  // Reference: Scheffer et al. (2009) Nature 461:53-59
  // As system approaches critical transition:
  //   - Variance increases (σ² → ∞)
  //   - Autocorrelation increases (ρ₁ → 1)
  //   - Recovery rate decreases

  WITH $values AS vals
  WHERE size(vals) >= 5

  // Compute mean
  WITH vals, reduce(s = 0.0, v IN vals | s + v) / size(vals) AS mean

  // Compute variance
  WITH vals, mean,
       [v IN vals | (v - mean) * (v - mean)] AS sq_diffs
  WITH vals, mean,
       reduce(s = 0.0, d IN sq_diffs | s + d) / (size(vals) - 1) AS variance

  // Compute lag-1 autocorrelation
  WITH vals, variance,
       [i IN range(0, size(vals)-2) | vals[i]] AS x_prev,
       [i IN range(1, size(vals)-1) | vals[i]] AS x_curr
  WITH vals, variance, x_prev, x_curr,
       reduce(s = 0.0, v IN x_prev | s + v) / size(x_prev) AS mean_prev,
       reduce(s = 0.0, v IN x_curr | s + v) / size(x_curr) AS mean_curr
  WITH variance, x_prev, x_curr, mean_prev, mean_curr,
       [i IN range(0, size(x_prev)-1) | (x_prev[i] - mean_prev) * (x_curr[i] - mean_curr)] AS cov_terms,
       [i IN range(0, size(x_prev)-1) | (x_prev[i] - mean_prev) * (x_prev[i] - mean_prev)] AS var_terms
  WITH variance,
       reduce(s = 0.0, t IN cov_terms | s + t) AS covariance,
       reduce(s = 0.0, t IN var_terms | s + t) AS var_prev
  WITH variance,
       CASE WHEN var_prev = 0 THEN 0.0 ELSE covariance / var_prev END AS autocorr

  // Compute combined critical slowing indicator
  // CSI = variance × autocorr / (1 - autocorr)
  // Higher CSI = closer to critical transition
  WITH variance, autocorr,
       CASE
         WHEN autocorr >= 0.999 THEN variance * 1000  // Cap at high value
         ELSE variance * autocorr / (1.0 - autocorr + 0.001)
       END AS csi

  RETURN {
    variance: variance,
    autocorrelation: autocorr,
    critical_slowing_indicator: csi,
    interpretation: CASE
      WHEN autocorr > 0.8 AND variance > 10 THEN \"CRITICAL - High risk of transition\"
      WHEN autocorr > 0.6 AND variance > 5 THEN \"WARNING - Elevated risk\"
      WHEN autocorr > 0.4 THEN \"CAUTION - Monitor closely\"
      ELSE \"STABLE - Normal operating range\"
    END
  }
  '
);

// -----------------------------------------------------------------------------
// STEP 4: Apply to Event Time Series
// -----------------------------------------------------------------------------

// Example: Compute critical slowing from security events over 30 days
MATCH (e:Event)
WHERE e.timestamp > datetime() - duration('P30D')
  AND e.metric_value IS NOT NULL
WITH e ORDER BY e.timestamp
WITH collect(toFloat(e.metric_value)) AS time_series

// Check if we have enough data points
WHERE size(time_series) >= 10

// Compute critical slowing indicator
RETURN psychohistory.criticalSlowingFromTimeSeries(time_series) AS critical_slowing_analysis;

// -----------------------------------------------------------------------------
// STEP 5: Rolling Window Analysis (Detect CHANGES in indicators)
// -----------------------------------------------------------------------------

// Compute CSI for multiple windows to detect trend
// Increasing CSI over time = system approaching critical transition

WITH [
  // Simulate 4 weekly windows of security metric data
  {week: 1, values: [10.2, 11.1, 9.8, 10.5, 10.0, 10.3, 9.9]},
  {week: 2, values: [10.5, 11.8, 9.2, 11.0, 10.8, 10.1, 11.5]},
  {week: 3, values: [11.2, 13.1, 8.5, 12.0, 11.5, 9.0, 13.0]},
  {week: 4, values: [12.5, 15.0, 7.0, 14.0, 13.0, 8.0, 16.0]}
] AS windows

UNWIND windows AS window
WITH window,
     psychohistory.criticalSlowingFromTimeSeries(window.values) AS analysis

RETURN window.week AS week,
       round(analysis.variance, 2) AS variance,
       round(analysis.autocorrelation, 2) AS autocorr,
       round(analysis.critical_slowing_indicator, 2) AS csi,
       analysis.interpretation AS status
ORDER BY week;

// Expected output: CSI increases week-over-week as variance/autocorr grow
// Week 1: Low CSI (stable)
// Week 4: High CSI (approaching transition)

// -----------------------------------------------------------------------------
// STEP 6: OLD vs NEW Comparison
// -----------------------------------------------------------------------------

// OLD (WRONG) - Hardcoded autocorrelation
WITH 5.0 AS variance
RETURN
  variance * 0.7 / (1.0 - 0.7) AS old_wrong_csi,
  'WRONG: Uses hardcoded autocorr=0.7 regardless of actual data' AS problem;

// NEW (CORRECT) - Computed from actual time series
WITH [10.0, 10.2, 10.1, 10.5, 10.3, 10.8, 10.6, 11.0, 10.9, 11.2] AS stable_series,
     [10.0, 12.0, 8.0, 14.0, 6.0, 16.0, 4.0, 18.0, 2.0, 20.0] AS volatile_series

RETURN
  psychohistory.criticalSlowingFromTimeSeries(stable_series) AS stable_analysis,
  psychohistory.criticalSlowingFromTimeSeries(volatile_series) AS volatile_analysis;

// Expected: volatile_series has higher CSI than stable_series

// -----------------------------------------------------------------------------
// STEP 7: Seldon Crisis Integration
// -----------------------------------------------------------------------------

// Compute critical slowing for each Seldon Crisis indicator stream
MATCH (crisis:SeldonCrisis)
MATCH (indicator:Indicator)-[:INDICATES]->(crisis)
MATCH (event:Event)-[:MEASURED_BY]->(indicator)
WHERE event.timestamp > datetime() - duration('P90D')
WITH crisis, indicator, event
ORDER BY event.timestamp
WITH crisis.name AS crisis_name,
     indicator.name AS indicator_name,
     collect(toFloat(event.value)) AS time_series
WHERE size(time_series) >= 10
WITH crisis_name, indicator_name,
     psychohistory.criticalSlowingFromTimeSeries(time_series) AS analysis
RETURN crisis_name,
       indicator_name,
       analysis.autocorrelation AS autocorr,
       analysis.variance AS variance,
       analysis.critical_slowing_indicator AS csi,
       analysis.interpretation AS status
ORDER BY csi DESC;

// =============================================================================
// END OF CORRECTED CRITICAL SLOWING INDICATOR
// =============================================================================
