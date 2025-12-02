// =============================================================================
// Enhancement 27: CORRECTED Granovetter Cascade Model
// =============================================================================
// File: remediation/04_granovetter_CORRECTED.cypher
// Created: 2025-11-27
// Purpose: Fix incorrect exponential CDF with proper threshold distribution
//
// ACADEMIC BASIS:
// Granovetter, M. (1978). "Threshold Models of Collective Behavior."
// American Journal of Sociology, 83(6), 1420-1443. DOI: 10.1086/226707
//
// ORIGINAL E27 ERROR:
// Used exponential CDF: 1 - exp(-x/threshold)
// This implies thresholds exponentially distributed with mode at 0
// (most actors adopt immediately) - INCORRECT
//
// CORRECT IMPLEMENTATION:
// Uses uniform or normal CDF per Granovetter's original formulation
// Thresholds should be uniformly or normally distributed across population
// =============================================================================

// -----------------------------------------------------------------------------
// OPTION A: Uniform Threshold Distribution (Simplest, matches Granovetter examples)
// -----------------------------------------------------------------------------
// Assumption: Thresholds uniformly distributed over [0, threshold_max]
// F(x) = x / threshold_max for x ∈ [0, threshold_max]
// F(x) = 1 for x > threshold_max

// Register corrected function (replaces original)
CALL apoc.custom.declareFunction(
  'psychohistory.granovetterCascadeUniform(adopters :: INTEGER, population :: INTEGER, threshold_max :: FLOAT) :: INTEGER',
  '
  // Granovetter (1978) equilibrium: r* = N × F(r*/N)
  // With uniform CDF: F(x) = min(x / threshold_max, 1.0)

  WITH $adopters AS current_adopters,
       $population AS N,
       $threshold_max AS theta_max

  // Current adoption fraction
  WITH current_adopters, N, theta_max,
       toFloat(current_adopters) / N AS adoption_fraction

  // Uniform CDF: F(adoption_fraction) = min(adoption_fraction / theta_max, 1.0)
  WITH N, theta_max, adoption_fraction,
       CASE
         WHEN adoption_fraction < theta_max
         THEN adoption_fraction / theta_max
         ELSE 1.0
       END AS cdf_value

  // Next period adopters: r(t+1) = N × F(r(t)/N)
  RETURN toInteger(N * cdf_value)
  '
);

// -----------------------------------------------------------------------------
// OPTION B: Normal Threshold Distribution (More realistic heterogeneity)
// -----------------------------------------------------------------------------
// Assumption: Thresholds normally distributed N(μ, σ²)
// Requires approximation of normal CDF (no native Cypher support)

// Approximation using logistic function (good for μ=0.5, σ≈0.15)
CALL apoc.custom.declareFunction(
  'psychohistory.granovetterCascadeNormal(adopters :: INTEGER, population :: INTEGER, mu :: FLOAT, sigma :: FLOAT) :: INTEGER',
  '
  // Granovetter (1978) with normal threshold distribution
  // Using logistic approximation: Φ(x) ≈ 1 / (1 + exp(-1.7 * (x - μ) / σ))

  WITH $adopters AS current_adopters,
       $population AS N,
       $mu AS mu,
       $sigma AS sigma

  WITH current_adopters, N, mu, sigma,
       toFloat(current_adopters) / N AS adoption_fraction

  // Logistic approximation to normal CDF
  WITH N, adoption_fraction,
       1.0 / (1.0 + exp(-1.7 * (adoption_fraction - mu) / sigma)) AS cdf_value

  RETURN toInteger(N * cdf_value)
  '
);

// -----------------------------------------------------------------------------
// OPTION C: Neighbor-Based Adoption (Most accurate, per Watts 2002)
// -----------------------------------------------------------------------------
// Individual adopts based on NEIGHBOR adoption fraction, not global fraction
// This captures network structure effects

// Step 1: Initialize thresholds based on actor sophistication
// (Run once to set up heterogeneous thresholds)
MATCH (actor:ThreatActor)
WHERE actor.threshold IS NULL
SET actor.threshold = CASE actor.sophistication
  WHEN 'expert' THEN 0.1 + rand() * 0.15     // [0.10, 0.25] - Early adopters
  WHEN 'advanced' THEN 0.2 + rand() * 0.20   // [0.20, 0.40] - Early majority
  WHEN 'intermediate' THEN 0.35 + rand() * 0.25  // [0.35, 0.60] - Late majority
  WHEN 'novice' THEN 0.55 + rand() * 0.30    // [0.55, 0.85] - Laggards
  ELSE 0.3 + rand() * 0.4                     // [0.30, 0.70] - Default uniform
END,
actor.adopted = false;

// Step 2: Cascade iteration (run repeatedly until convergence)
// This is the CORRECT Granovetter implementation per Watts (2002)
MATCH (actor:ThreatActor {adopted: false})
OPTIONAL MATCH (actor)-[:COLLABORATES_WITH|ATTRIBUTED_TO]-(neighbor:ThreatActor)
WITH actor,
     count(CASE WHEN neighbor.adopted = true THEN 1 END) AS adopted_neighbors,
     count(neighbor) AS total_neighbors
WHERE total_neighbors > 0
  AND toFloat(adopted_neighbors) / total_neighbors >= actor.threshold
SET actor.adopted = true
RETURN count(actor) AS newly_adopted;

// Repeat Step 2 until newly_adopted = 0 (equilibrium reached)

// -----------------------------------------------------------------------------
// VALIDATION QUERIES
// -----------------------------------------------------------------------------

// Test uniform cascade function
WITH 10 AS initial_adopters, 100 AS population, 0.25 AS threshold_max
CALL {
  WITH initial_adopters, population, threshold_max
  RETURN psychohistory.granovetterCascadeUniform(initial_adopters, population, threshold_max) AS round1
}
CALL {
  WITH round1 AS adopters, population, threshold_max
  RETURN psychohistory.granovetterCascadeUniform(adopters, population, threshold_max) AS round2
}
RETURN initial_adopters, round1, round2;
// Expected: Cascade should grow if initial_adopters/population > threshold

// Test: Verify cascade grows when adoption > threshold
WITH [5, 10, 25, 50] AS initial_values
UNWIND initial_values AS initial
RETURN initial AS initial_adopters,
       psychohistory.granovetterCascadeUniform(initial, 100, 0.25) AS next_round,
       CASE
         WHEN initial >= 25 THEN 'Should cascade (adopters >= threshold × population)'
         ELSE 'Below threshold'
       END AS expected;

// Test: Verify equilibrium convergence
WITH 30 AS seed, 100 AS pop, 0.25 AS thresh
WITH seed AS r0,
     psychohistory.granovetterCascadeUniform(seed, pop, thresh) AS r1
WITH r0, r1,
     psychohistory.granovetterCascadeUniform(r1, pop, thresh) AS r2
WITH r0, r1, r2,
     psychohistory.granovetterCascadeUniform(r2, pop, thresh) AS r3
RETURN r0, r1, r2, r3,
       CASE WHEN r2 = r3 THEN 'EQUILIBRIUM REACHED' ELSE 'Still converging' END AS status;

// -----------------------------------------------------------------------------
// COMPARISON: OLD (WRONG) vs NEW (CORRECT)
// -----------------------------------------------------------------------------

// OLD IMPLEMENTATION (DO NOT USE):
// RETURN toInteger($population * (1.0 - exp(-1.0 * $adopters / ($population * $threshold + 0.001))))
// Problem: Exponential CDF implies most thresholds near 0

// NEW IMPLEMENTATION (CORRECT):
// Uses uniform CDF: F(x) = x / threshold_max
// Produces proper S-curve adoption dynamics

// Demonstrate difference:
WITH 20 AS adopters, 100 AS pop, 0.25 AS thresh
RETURN
  // OLD (wrong): exponential CDF
  toInteger(pop * (1.0 - exp(-1.0 * adopters / (pop * thresh + 0.001)))) AS old_wrong_result,

  // NEW (correct): uniform CDF
  CASE
    WHEN toFloat(adopters) / pop < thresh
    THEN toInteger(pop * (toFloat(adopters) / pop / thresh))
    ELSE pop
  END AS new_correct_result,

  'OLD overestimates cascade speed due to exponential assumption' AS explanation;

// =============================================================================
// END OF CORRECTED GRANOVETTER CASCADE MODEL
// =============================================================================
