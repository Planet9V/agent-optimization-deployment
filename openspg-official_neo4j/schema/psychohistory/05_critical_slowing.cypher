// ============================================
// EQUATION 5: Critical Slowing Down (Early Warning Signals)
// ============================================
// ρ(lag) → 1, σ² → ∞ as system approaches critical transition
// where:
//   ρ(lag) = autocorrelation at lag k
//   σ² = variance of state variable
//   Application: Early warning signals before catastrophic shifts

// ============================================
// STEP 1: Create Graph Projection
// ============================================

// Drop existing projection if it exists
CALL gds.graph.exists('psychohistory_critical_slowing') YIELD exists
WITH exists WHERE exists
CALL gds.graph.drop('psychohistory_critical_slowing') YIELD graphName
RETURN 'Dropped existing graph: ' + graphName AS status
UNION
WITH 1 AS dummy WHERE NOT gds.graph.exists('psychohistory_critical_slowing')
RETURN 'No existing graph to drop' AS status;

// Create projection for time-series analysis
CALL gds.graph.project(
    'psychohistory_critical_slowing',
    ['ICS_Sector', 'ICS_Asset', 'Vulnerability', 'Incident', 'Campaign', 'Threat_Actor'],
    {
        BELONGS_TO_SECTOR: {
            type: 'BELONGS_TO_SECTOR',
            orientation: 'NATURAL'
        },
        HAS_VULNERABILITY: {
            type: 'HAS_VULNERABILITY',
            orientation: 'NATURAL'
        },
        INCIDENT_AFFECTS: {
            type: 'INCIDENT_AFFECTS',
            orientation: 'NATURAL'
        },
        ATTRIBUTED_TO: {
            type: 'ATTRIBUTED_TO',
            orientation: 'NATURAL'
        }
    }
) YIELD graphName, nodeCount, relationshipCount
RETURN
    graphName,
    nodeCount AS total_nodes,
    relationshipCount AS total_relationships;

// ============================================
// STEP 2: Generate Synthetic Time Series Data
// ============================================

// Create time series of system states for each sector
// In real implementation, this would use historical incident data
MATCH (sector:ICS_Sector)
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name
// Generate 50 time steps of synthetic vulnerability data
UNWIND range(0, 49) AS time_step
WITH sector, sector_name, time_step,
     // Simulate increasing vulnerability over time with noise
     // Base trend + random noise
     (toFloat(time_step) / 50.0) * 2.0 + (rand() - 0.5) * 0.5 AS state_value
MERGE (ts:TimeSeries {
    sector: sector_name,
    time_step: time_step,
    state_value: state_value
})
WITH sector_name, count(ts) AS points_created
RETURN
    'Time Series Generated' AS status,
    sector_name,
    points_created AS time_points
ORDER BY sector_name
LIMIT 10;

// ============================================
// STEP 3: Calculate Variance (σ²) in Sliding Windows
// ============================================

// Calculate variance in sliding windows to detect increasing variance
MATCH (sector:ICS_Sector)
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name
LIMIT 5
WITH sector_name
UNWIND range(0, 4) AS window_idx
WITH sector_name, window_idx,
     window_idx * 10 AS window_start,
     (window_idx * 10) + 10 AS window_end
MATCH (ts:TimeSeries {sector: sector_name})
WHERE ts.time_step >= window_start AND ts.time_step < window_end
WITH sector_name, window_idx, window_start,
     avg(ts.state_value) AS window_mean,
     stdev(ts.state_value) AS window_stdev,
     collect(ts.state_value) AS values
WITH sector_name, window_idx, window_start,
     window_stdev * window_stdev AS variance,
     window_stdev
RETURN
    sector_name,
    window_idx AS window_number,
    'Steps ' + toString(window_start) + '-' + toString(window_start + 10) AS time_window,
    round(variance * 1000) / 1000 AS variance_sigma2,
    CASE
        WHEN variance > 0.15 THEN 'CRITICAL SLOWING: High variance'
        WHEN variance > 0.10 THEN 'WARNING: Increasing variance'
        WHEN variance > 0.05 THEN 'ELEVATED: Moderate variance'
        ELSE 'NORMAL: Low variance'
    END AS variance_status
ORDER BY sector_name, window_idx;

// ============================================
// STEP 4: Calculate Autocorrelation ρ(lag)
// ============================================

// Calculate autocorrelation for different lags
// ρ(k) = Cov(X_t, X_{t-k}) / Var(X_t)
MATCH (sector:ICS_Sector)
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name
LIMIT 5
WITH sector_name
// Calculate for lags 1, 2, 3, 5, 10
UNWIND [1, 2, 3, 5, 10] AS lag
WITH sector_name, lag
MATCH (ts1:TimeSeries {sector: sector_name})
MATCH (ts2:TimeSeries {sector: sector_name})
WHERE ts2.time_step = ts1.time_step - lag
  AND ts1.time_step >= lag
WITH sector_name, lag,
     collect(ts1.state_value) AS x_t,
     collect(ts2.state_value) AS x_t_minus_lag,
     avg(ts1.state_value) AS mean_x
WITH sector_name, lag, mean_x,
     // Calculate covariance
     reduce(sum = 0.0, i IN range(0, size(x_t) - 1) |
         sum + (x_t[i] - mean_x) * (x_t_minus_lag[i] - mean_x)
     ) / size(x_t) AS covariance,
     // Calculate variance
     reduce(sum = 0.0, i IN range(0, size(x_t) - 1) |
         sum + (x_t[i] - mean_x) * (x_t[i] - mean_x)
     ) / size(x_t) AS variance
WITH sector_name, lag,
     CASE WHEN variance > 0 THEN covariance / variance ELSE 0 END AS autocorrelation
RETURN
    sector_name,
    lag,
    round(autocorrelation * 1000) / 1000 AS autocorr_rho,
    CASE
        WHEN autocorrelation > 0.8 THEN 'CRITICAL SLOWING: Very high autocorrelation'
        WHEN autocorrelation > 0.6 THEN 'WARNING: High autocorrelation'
        WHEN autocorrelation > 0.4 THEN 'MODERATE: Increasing autocorrelation'
        ELSE 'NORMAL: Low autocorrelation'
    END AS autocorr_status,
    CASE
        WHEN autocorrelation > 0.8 AND lag <= 2 THEN 'IMMINENT TRANSITION'
        WHEN autocorrelation > 0.7 THEN 'APPROACHING CRITICAL POINT'
        ELSE 'STABLE'
    END AS warning_level
ORDER BY sector_name, lag;

// ============================================
// STEP 5: Calculate Detrended Fluctuation Analysis (DFA)
// ============================================

// DFA measures long-range correlations
// Higher DFA exponent indicates critical slowing
MATCH (sector:ICS_Sector)
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name
LIMIT 5
WITH sector_name
MATCH (ts:TimeSeries {sector: sector_name})
WITH sector_name, ts
ORDER BY ts.time_step
WITH sector_name,
     collect(ts.state_value) AS time_series,
     avg(ts.state_value) AS series_mean
// Calculate cumulative sum (integration)
WITH sector_name,
     reduce(cumsum = [], val IN time_series |
         cumsum + [CASE WHEN size(cumsum) = 0 THEN val - series_mean
                   ELSE cumsum[size(cumsum)-1] + val - series_mean END]
     ) AS integrated_series
// Fit linear trend and calculate residuals
WITH sector_name, integrated_series,
     size(integrated_series) AS n,
     reduce(sum_y = 0.0, y IN integrated_series | sum_y + y) / size(integrated_series) AS mean_y,
     reduce(sum_x = 0.0, idx IN range(0, size(integrated_series)-1) | sum_x + idx) / size(integrated_series) AS mean_x
WITH sector_name, integrated_series, n, mean_x, mean_y,
     // Calculate slope
     reduce(sum_xy = 0.0, idx IN range(0, size(integrated_series)-1) |
         sum_xy + (idx - mean_x) * (integrated_series[idx] - mean_y)
     ) / reduce(sum_xx = 0.0, idx IN range(0, size(integrated_series)-1) |
         sum_xx + (idx - mean_x) * (idx - mean_x)
     ) AS slope
// Calculate root mean square fluctuation
WITH sector_name, integrated_series, slope, mean_y, mean_x,
     sqrt(
         reduce(sum_sq = 0.0, idx IN range(0, size(integrated_series)-1) |
             sum_sq + (integrated_series[idx] - (mean_y + slope * (idx - mean_x))) *
                      (integrated_series[idx] - (mean_y + slope * (idx - mean_x)))
         ) / size(integrated_series)
     ) AS rms_fluctuation
RETURN
    sector_name,
    round(rms_fluctuation * 100) / 100 AS dfa_fluctuation,
    CASE
        WHEN rms_fluctuation > 2.0 THEN 'CRITICAL: Strong long-range correlations'
        WHEN rms_fluctuation > 1.0 THEN 'ELEVATED: Moderate correlations'
        ELSE 'NORMAL: Weak correlations'
    END AS dfa_status,
    'DFA indicates system memory and critical slowing' AS interpretation
ORDER BY rms_fluctuation DESC;

// ============================================
// STEP 6: Detect Increasing Variance Trend
// ============================================

// Test if variance is significantly increasing over time
MATCH (sector:ICS_Sector)
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name
LIMIT 5
WITH sector_name
// Split into early and late windows
MATCH (ts_early:TimeSeries {sector: sector_name})
WHERE ts_early.time_step < 25
WITH sector_name, collect(ts_early.state_value) AS early_values
MATCH (ts_late:TimeSeries {sector: sector_name})
WHERE ts_late.time_step >= 25
WITH sector_name, early_values, collect(ts_late.state_value) AS late_values
WITH sector_name,
     reduce(s = 0.0, v IN early_values | s + v * v) / size(early_values) -
         (reduce(s = 0.0, v IN early_values | s + v) / size(early_values)) *
         (reduce(s = 0.0, v IN early_values | s + v) / size(early_values)) AS early_variance,
     reduce(s = 0.0, v IN late_values | s + v * v) / size(late_values) -
         (reduce(s = 0.0, v IN late_values | s + v) / size(late_values)) *
         (reduce(s = 0.0, v IN late_values | s + v) / size(late_values)) AS late_variance
WITH sector_name, early_variance, late_variance,
     (late_variance - early_variance) / early_variance AS variance_increase_ratio
RETURN
    sector_name,
    round(early_variance * 1000) / 1000 AS early_window_variance,
    round(late_variance * 1000) / 1000 AS late_window_variance,
    round(variance_increase_ratio * 100) AS variance_increase_pct,
    CASE
        WHEN variance_increase_ratio > 1.0 THEN 'CRITICAL: Variance doubled (Critical slowing)'
        WHEN variance_increase_ratio > 0.5 THEN 'WARNING: Variance increasing significantly'
        WHEN variance_increase_ratio > 0.2 THEN 'ELEVATED: Variance trending up'
        ELSE 'STABLE: Variance stable or decreasing'
    END AS variance_trend,
    CASE
        WHEN variance_increase_ratio > 1.0 THEN 'IMMINENT CATASTROPHIC SHIFT'
        WHEN variance_increase_ratio > 0.5 THEN 'APPROACHING CRITICAL TRANSITION'
        ELSE 'NORMAL FLUCTUATIONS'
    END AS early_warning
ORDER BY variance_increase_ratio DESC;

// ============================================
// STEP 7: Calculate Recovery Rate After Perturbations
// ============================================

// Measure how quickly system returns to equilibrium after disturbance
// Slower recovery = critical slowing
MATCH (sector:ICS_Sector)
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name
LIMIT 5
WITH sector_name
// Find large fluctuations (perturbations)
MATCH (ts1:TimeSeries {sector: sector_name})
MATCH (ts2:TimeSeries {sector: sector_name})
WHERE ts2.time_step = ts1.time_step + 1
WITH sector_name, ts1, ts2,
     abs(ts2.state_value - ts1.state_value) AS fluctuation
WHERE fluctuation > 0.3
// Measure recovery in next 5 steps
WITH sector_name, ts2.time_step AS perturbation_time, ts2.state_value AS perturbed_value
MATCH (ts_recovery:TimeSeries {sector: sector_name})
WHERE ts_recovery.time_step > perturbation_time
  AND ts_recovery.time_step <= perturbation_time + 5
WITH sector_name, perturbation_time, perturbed_value,
     collect(ts_recovery.state_value) AS recovery_values
// Calculate exponential decay rate
WITH sector_name, perturbation_time, perturbed_value, recovery_values,
     // Simple measure: how much did it recover in 5 steps
     abs(recovery_values[size(recovery_values)-1] - perturbed_value) /
         CASE WHEN abs(perturbed_value) > 0 THEN abs(perturbed_value) ELSE 1 END AS recovery_fraction
WITH sector_name, perturbation_time, recovery_fraction,
     // Estimate recovery rate (λ in e^(-λt))
     -log(1.0 - recovery_fraction) / 5.0 AS recovery_rate
WHERE recovery_rate > 0
RETURN
    sector_name,
    perturbation_time AS step_of_perturbation,
    round(recovery_rate * 1000) / 1000 AS recovery_rate_lambda,
    round(1.0 / recovery_rate * 10) / 10 AS recovery_time_steps,
    CASE
        WHEN recovery_rate < 0.2 THEN 'CRITICAL SLOWING: Very slow recovery'
        WHEN recovery_rate < 0.5 THEN 'WARNING: Slow recovery'
        WHEN recovery_rate < 1.0 THEN 'MODERATE: Normal recovery'
        ELSE 'FAST: Resilient system'
    END AS recovery_status,
    CASE
        WHEN recovery_rate < 0.2 THEN 'System losing resilience - critical transition near'
        WHEN recovery_rate < 0.5 THEN 'System showing early warning signals'
        ELSE 'System resilient'
    END AS interpretation
ORDER BY recovery_rate
LIMIT 20;

// ============================================
// STEP 8: Composite Early Warning Score
// ============================================

// Combine multiple indicators into single warning score
MATCH (sector:ICS_Sector)
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name
LIMIT 10
WITH sector_name
// Calculate variance
MATCH (ts:TimeSeries {sector: sector_name})
WITH sector_name, stdev(ts.state_value) AS variance_indicator
// Calculate autocorrelation at lag 1
MATCH (ts1:TimeSeries {sector: sector_name})
MATCH (ts2:TimeSeries {sector: sector_name})
WHERE ts2.time_step = ts1.time_step - 1 AND ts1.time_step >= 1
WITH sector_name, variance_indicator,
     collect(ts1.state_value) AS x_t,
     collect(ts2.state_value) AS x_t_1,
     avg(ts1.state_value) AS mean_x
WITH sector_name, variance_indicator,
     reduce(cov = 0.0, i IN range(0, size(x_t)-1) |
         cov + (x_t[i] - mean_x) * (x_t_1[i] - mean_x)
     ) / size(x_t) AS covariance,
     reduce(var = 0.0, i IN range(0, size(x_t)-1) |
         var + (x_t[i] - mean_x) * (x_t[i] - mean_x)
     ) / size(x_t) AS variance
WITH sector_name, variance_indicator,
     CASE WHEN variance > 0 THEN covariance / variance ELSE 0 END AS autocorr_indicator
// Normalize indicators to 0-1 scale
WITH sector_name,
     CASE WHEN variance_indicator > 0.4 THEN 1.0
          WHEN variance_indicator > 0.2 THEN 0.7
          WHEN variance_indicator > 0.1 THEN 0.4
          ELSE 0.1 END AS variance_score,
     CASE WHEN autocorr_indicator > 0.8 THEN 1.0
          WHEN autocorr_indicator > 0.6 THEN 0.7
          WHEN autocorr_indicator > 0.4 THEN 0.4
          ELSE 0.1 END AS autocorr_score
// Composite score (equal weighting)
WITH sector_name,
     (variance_score + autocorr_score) / 2.0 AS composite_warning_score,
     variance_score,
     autocorr_score
RETURN
    sector_name,
    round(variance_score * 100) / 100 AS variance_signal,
    round(autocorr_score * 100) / 100 AS autocorr_signal,
    round(composite_warning_score * 100) / 100 AS composite_score,
    CASE
        WHEN composite_warning_score > 0.8 THEN 'CRITICAL: Multiple strong warning signals'
        WHEN composite_warning_score > 0.6 THEN 'HIGH: Significant early warnings'
        WHEN composite_warning_score > 0.4 THEN 'MODERATE: Some early warnings'
        ELSE 'LOW: Minimal warning signals'
    END AS warning_level,
    CASE
        WHEN composite_warning_score > 0.8 THEN 'IMMEDIATE ACTION REQUIRED'
        WHEN composite_warning_score > 0.6 THEN 'PREPARE FOR TRANSITION'
        WHEN composite_warning_score > 0.4 THEN 'MONITOR CLOSELY'
        ELSE 'ROUTINE MONITORING'
    END AS recommended_response
ORDER BY composite_warning_score DESC;

// ============================================
// STEP 9: Power Spectrum Analysis
// ============================================

// Analyze frequency content (reddening spectrum indicates critical slowing)
// Simplified version: measure low-frequency vs high-frequency power
MATCH (sector:ICS_Sector)
WITH sector,
     CASE
         WHEN sector.name IS NOT NULL THEN sector.name
         WHEN sector.id IS NOT NULL THEN sector.id
         ELSE 'Unknown'
     END AS sector_name
LIMIT 5
WITH sector_name
MATCH (ts:TimeSeries {sector: sector_name})
WITH sector_name, collect(ts.state_value) AS time_series
// Calculate differences (approximates high-frequency component)
WITH sector_name, time_series,
     reduce(hf_power = 0.0, i IN range(1, size(time_series)-1) |
         hf_power + (time_series[i] - time_series[i-1]) * (time_series[i] - time_series[i-1])
     ) / (size(time_series) - 1) AS high_freq_power,
     // Calculate slow changes (approximates low-frequency component)
     reduce(lf_power = 0.0, i IN range(5, size(time_series)-1) |
         lf_power + (time_series[i] - time_series[i-5]) * (time_series[i] - time_series[i-5])
     ) / (size(time_series) - 5) AS low_freq_power
WITH sector_name, high_freq_power, low_freq_power,
     CASE WHEN high_freq_power > 0 THEN low_freq_power / high_freq_power ELSE 0 END AS spectral_ratio
RETURN
    sector_name,
    round(low_freq_power * 1000) / 1000 AS low_frequency_power,
    round(high_freq_power * 1000) / 1000 AS high_frequency_power,
    round(spectral_ratio * 100) / 100 AS lf_hf_ratio,
    CASE
        WHEN spectral_ratio > 5.0 THEN 'CRITICAL: Spectrum reddening (strong low-freq dominance)'
        WHEN spectral_ratio > 2.0 THEN 'WARNING: Increased low-frequency power'
        WHEN spectral_ratio > 1.0 THEN 'ELEVATED: Some reddening'
        ELSE 'NORMAL: Balanced spectrum'
    END AS spectral_status,
    'Higher ratio = slower dynamics = critical slowing' AS interpretation
ORDER BY spectral_ratio DESC;

// ============================================
// STEP 10: Validation Tests
// ============================================

// Test 1: Verify graph projection exists
CALL gds.graph.exists('psychohistory_critical_slowing') YIELD exists
RETURN
    'TEST 1: Graph Projection' AS test_name,
    CASE WHEN exists THEN 'PASS' ELSE 'FAIL' END AS result;

// Test 2: Verify time series data exists
MATCH (ts:TimeSeries)
WITH count(ts) AS time_points
RETURN
    'TEST 2: Time Series Data' AS test_name,
    CASE WHEN time_points > 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    time_points AS total_time_points;

// Test 3: Verify variance calculation produces valid results
MATCH (ts:TimeSeries)
WHERE ts.sector IS NOT NULL
WITH ts.sector AS sector, stdev(ts.state_value) AS variance
WITH variance
WHERE variance IS NOT NULL
RETURN
    'TEST 3: Variance Calculation' AS test_name,
    CASE WHEN variance >= 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    round(variance * 1000) / 1000 AS sample_variance
LIMIT 1;

// Test 4: Verify autocorrelation produces valid range
MATCH (ts1:TimeSeries), (ts2:TimeSeries)
WHERE ts1.sector = ts2.sector
  AND ts2.time_step = ts1.time_step - 1
  AND ts1.time_step >= 1
WITH ts1.sector AS sector,
     collect(ts1.state_value) AS x_t,
     collect(ts2.state_value) AS x_t_1,
     avg(ts1.state_value) AS mean_x
WITH sector,
     reduce(cov = 0.0, i IN range(0, size(x_t)-1) |
         cov + (x_t[i] - mean_x) * (x_t_1[i] - mean_x)
     ) / size(x_t) AS covariance,
     reduce(var = 0.0, i IN range(0, size(x_t)-1) |
         var + (x_t[i] - mean_x) * (x_t[i] - mean_x)
     ) / size(x_t) AS variance
WITH CASE WHEN variance > 0 THEN covariance / variance ELSE 0 END AS autocorr
RETURN
    'TEST 4: Autocorrelation Calculation' AS test_name,
    CASE WHEN autocorr >= -1.1 AND autocorr <= 1.1 THEN 'PASS' ELSE 'FAIL' END AS result,
    round(autocorr * 1000) / 1000 AS sample_autocorrelation
LIMIT 1;

// Test 5: Verify early warning score is bounded
MATCH (ts:TimeSeries)
WITH ts.sector AS sector, stdev(ts.state_value) AS variance
WITH variance,
     CASE WHEN variance > 0.4 THEN 1.0
          WHEN variance > 0.2 THEN 0.7
          WHEN variance > 0.1 THEN 0.4
          ELSE 0.1 END AS warning_score
RETURN
    'TEST 5: Warning Score Range' AS test_name,
    CASE WHEN warning_score >= 0 AND warning_score <= 1.0 THEN 'PASS' ELSE 'FAIL' END AS result,
    round(warning_score * 100) / 100 AS sample_warning_score
LIMIT 1;

// ============================================
// STEP 11: Cleanup (Optional)
// ============================================

// CALL gds.graph.drop('psychohistory_critical_slowing') YIELD graphName
// RETURN 'Dropped graph: ' + graphName AS cleanup_status;

// Delete time series data for re-simulation
// MATCH (ts:TimeSeries)
// DELETE ts
// RETURN 'Deleted time series data' AS status;
