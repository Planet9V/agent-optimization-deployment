// ═══════════════════════════════════════════════════════════════════════════════
// TEST QUERIES FOR CONFIDENCE INTERVAL FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════════
// File: test_confidence_intervals.cypher
// Created: 2025-11-28
// Purpose: Individual test queries for each CI function
// ═══════════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 1: psychohistory.bootstrapCI
// ═══════════════════════════════════════════════════════════════════════════════
// Tests bootstrap confidence interval for mean

WITH [7.2, 8.1, 6.5, 9.3, 7.8, 8.5, 7.1, 8.9, 7.6, 8.2] AS test_values
RETURN psychohistory.bootstrapCI(
  test_values,
  'mean',
  100,    // 100 bootstrap iterations
  0.05    // 95% confidence interval
) AS test1_bootstrap_mean_ci;

// Expected:
// - lower_bound: ~7.0-7.5
// - upper_bound: ~8.5-9.0
// - confidence_level: 0.95
// - method: 'bootstrap_percentile'

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 2: psychohistory.autocorrelationCI
// ═══════════════════════════════════════════════════════════════════════════════
// Tests Fisher Z-transformation confidence interval

RETURN psychohistory.autocorrelationCI(
  0.65,     // Observed autocorrelation
  50,       // Sample size
  0.05      // 95% CI
) AS test2_autocorr_ci;

// Expected:
// - point_estimate: 0.65
// - lower_bound: ~0.45-0.50
// - upper_bound: ~0.75-0.80
// - method: 'fisher_z_transform'
// - effective_df: 47

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 3: psychohistory.cascadePredictionInterval
// ═══════════════════════════════════════════════════════════════════════════════
// Tests Agresti-Coull binomial prediction interval

RETURN psychohistory.cascadePredictionInterval(
  0.25,     // 25% predicted cascade probability
  1000,     // Population of 1000 entities
  0.05      // 95% prediction interval
) AS test3_cascade_pi;

// Expected:
// - predicted_probability: 0.25
// - predicted_count: 250
// - lower_bound_count: ~220-230
// - upper_bound_count: ~270-280
// - method: 'agresti_coull_binomial'

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 4: psychohistory.epidemicR0CI
// ═══════════════════════════════════════════════════════════════════════════════
// Tests log-normal confidence interval for R₀

RETURN psychohistory.epidemicR0CI(
  2.5,      // R₀ = 2.5 (epidemic growth)
  100,      // 100 observations
  0.05      // 95% CI
) AS test4_r0_ci;

// Expected:
// - point_estimate: 2.5
// - lower_bound: ~2.0-2.2
// - upper_bound: ~2.8-3.2
// - interpretation: 'Epidemic growth certain (lower bound > 1)'

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 5: psychohistory.propagateUncertaintyDelta
// ═══════════════════════════════════════════════════════════════════════════════
// Tests delta method uncertainty propagation

RETURN psychohistory.propagateUncertaintyDelta(
  10.0,     // Point estimate
  4.0,      // Variance
  'log',    // Log transformation
  0.05      // 95% CI
) AS test5_delta_method;

// Expected:
// - original_value: 10.0
// - original_variance: 4.0
// - transformed_value: ~2.30 (ln(10))
// - transformed_variance: ~0.04 (derivative²×variance)
// - method: 'delta_method'

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 6: psychohistory.propagateUncertaintyMonteCarlo
// ═══════════════════════════════════════════════════════════════════════════════
// Tests Monte Carlo uncertainty propagation

WITH {
  beta: {mean: 0.3, variance: 0.01},
  contacts: {mean: 5.0, variance: 1.0},
  duration: {mean: 7.0, variance: 0.5}
} AS epidemic_params
RETURN psychohistory.propagateUncertaintyMonteCarlo(
  epidemic_params,
  'epidemic_r0',
  500,      // 500 Monte Carlo simulations
  0.05      // 95% CI
) AS test6_monte_carlo;

// Expected:
// - equation: 'epidemic_r0'
// - mean_prediction: ~10.5 (0.3 × 5.0 × 7.0)
// - lower_bound: ~8-9
// - upper_bound: ~12-13
// - method: 'monte_carlo_propagation'
// - full_distribution_percentiles: map with p05, p25, p50, p75, p95

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 7: psychohistory.predictWithUncertainty
// ═══════════════════════════════════════════════════════════════════════════════
// Tests integrated prediction with uncertainty

WITH {
  beta: 0.3,
  contacts: 5.0,
  duration: 7.0,
  n_observations: 100
} AS params
RETURN psychohistory.predictWithUncertainty(
  'epidemic_r0',
  params,
  [1.0, 2.0, 3.0, 4.0, 5.0],  // Dummy historical data
  0.05                         // 95% CI
) AS test7_predict_with_uncertainty;

// Expected:
// - equation: 'epidemic_r0'
// - point_prediction: 10.5 (0.3 × 5.0 × 7.0)
// - confidence_interval: map with lower_bound, upper_bound
// - uncertainty_quantified: true
// - data_quality_score: 'low' (only 5 data points)

// ═══════════════════════════════════════════════════════════════════════════════
// COMPREHENSIVE TEST: All functions in sequence
// ═══════════════════════════════════════════════════════════════════════════════

WITH {
  test_data: [7.2, 8.1, 6.5, 9.3, 7.8, 8.5, 7.1, 8.9, 7.6, 8.2],
  autocorr: 0.65,
  n_samples: 50,
  cascade_prob: 0.25,
  population: 1000,
  r0: 2.5,
  alpha: 0.05
} AS test_params

RETURN {
  test1_bootstrap: psychohistory.bootstrapCI(
    test_params.test_data,
    'mean',
    100,
    test_params.alpha
  ),
  test2_autocorr: psychohistory.autocorrelationCI(
    test_params.autocorr,
    test_params.n_samples,
    test_params.alpha
  ),
  test3_cascade: psychohistory.cascadePredictionInterval(
    test_params.cascade_prob,
    test_params.population,
    test_params.alpha
  ),
  test4_r0: psychohistory.epidemicR0CI(
    test_params.r0,
    100,
    test_params.alpha
  ),
  test5_delta: psychohistory.propagateUncertaintyDelta(
    10.0,
    4.0,
    'log',
    test_params.alpha
  ),
  test6_monte_carlo: psychohistory.propagateUncertaintyMonteCarlo(
    {
      beta: {mean: 0.3, variance: 0.01},
      contacts: {mean: 5.0, variance: 1.0},
      duration: {mean: 7.0, variance: 0.5}
    },
    'epidemic_r0',
    100,
    test_params.alpha
  ),
  test7_predict: psychohistory.predictWithUncertainty(
    'epidemic_r0',
    {beta: 0.3, contacts: 5.0, duration: 7.0, n_observations: 100},
    test_params.test_data,
    test_params.alpha
  )
} AS all_tests_results;

// ═══════════════════════════════════════════════════════════════════════════════
// VALIDATION QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

// Check that all functions exist
SHOW FUNCTIONS
WHERE name STARTS WITH 'psychohistory.'
  AND name IN [
    'psychohistory.bootstrapCI',
    'psychohistory.autocorrelationCI',
    'psychohistory.cascadePredictionInterval',
    'psychohistory.epidemicR0CI',
    'psychohistory.propagateUncertaintyDelta',
    'psychohistory.propagateUncertaintyMonteCarlo',
    'psychohistory.predictWithUncertainty'
  ]
RETURN name, signature, description
ORDER BY name;

// Expected: 7 functions returned

// ═══════════════════════════════════════════════════════════════════════════════
// END OF TEST QUERIES
// ═══════════════════════════════════════════════════════════════════════════════
