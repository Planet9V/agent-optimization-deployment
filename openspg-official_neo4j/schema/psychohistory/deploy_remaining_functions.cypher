// ============================================
// DEPLOY REMAINING PSYCHOHISTORY FUNCTIONS
// Target: 10+ total custom functions
// ============================================

// ============================================
// FUNCTION 7: Ising Dynamics - Opinion Formation
// ============================================
// Calculate opinion dynamics: dm/dt = -m + tanh(β(Jzm + h))
CALL apoc.custom.declareFunction(
    'psychohistory.isingDynamics(m FLOAT, beta FLOAT, J FLOAT, z FLOAT, h FLOAT) :: FLOAT',
    'RETURN -$m + tanh($beta * ($J * $z * $m + $h)) AS dm_dt'
);

// ============================================
// FUNCTION 8: Bifurcation Point Detection
// ============================================
// Calculate state change rate: dx/dt = μ + x²
CALL apoc.custom.declareFunction(
    'psychohistory.bifurcationRate(x FLOAT, mu FLOAT) :: FLOAT',
    'RETURN $mu + ($x * $x) AS dx_dt'
);

// ============================================
// FUNCTION 9: Bifurcation Distance
// ============================================
// Calculate distance from bifurcation point
CALL apoc.custom.declareFunction(
    'psychohistory.bifurcationDistance(mu FLOAT) :: FLOAT',
    'RETURN abs($mu) AS distance'
);

// ============================================
// FUNCTION 10: Recovery Rate (Critical Slowing)
// ============================================
// Calculate recovery rate: λ = -ln(1 - recovery_fraction) / time
CALL apoc.custom.declareFunction(
    'psychohistory.recoveryRate(recovery_fraction FLOAT, time_steps FLOAT) :: FLOAT',
    'RETURN CASE
        WHEN $recovery_fraction >= 1.0 THEN 0.0
        WHEN $recovery_fraction <= 0.0 THEN 0.0
        ELSE -log(1.0 - $recovery_fraction) / $time_steps
    END AS lambda'
);

// ============================================
// FUNCTION 11: Autocorrelation Coefficient
// ============================================
// Calculate autocorrelation: ρ(lag) = Cov(X_t, X_{t-lag}) / Var(X_t)
CALL apoc.custom.declareFunction(
    'psychohistory.autocorrelation(covariance FLOAT, variance FLOAT) :: FLOAT',
    'RETURN CASE
        WHEN $variance > 0 THEN $covariance / $variance
        ELSE 0.0
    END AS rho'
);

// ============================================
// FUNCTION 12: Variance Increase Ratio
// ============================================
// Calculate variance change for critical slowing detection
CALL apoc.custom.declareFunction(
    'psychohistory.varianceRatio(early_var FLOAT, late_var FLOAT) :: FLOAT',
    'RETURN CASE
        WHEN $early_var > 0 THEN ($late_var - $early_var) / $early_var
        ELSE 0.0
    END AS ratio'
);

// ============================================
// FUNCTION 13: Spectral Reddening Ratio
// ============================================
// Calculate low-frequency to high-frequency power ratio
CALL apoc.custom.declareFunction(
    'psychohistory.spectralRatio(lf_power FLOAT, hf_power FLOAT) :: FLOAT',
    'RETURN CASE
        WHEN $hf_power > 0 THEN $lf_power / $hf_power
        ELSE 0.0
    END AS spectral_ratio'
);

// ============================================
// FUNCTION 14: Composite Warning Score
// ============================================
// Combine multiple early warning signals
CALL apoc.custom.declareFunction(
    'psychohistory.compositeWarning(variance_score FLOAT, autocorr_score FLOAT) :: FLOAT',
    'RETURN ($variance_score + $autocorr_score) / 2.0 AS composite_score'
);

// ============================================
// FUNCTION 15: Opinion Cascade Probability
// ============================================
// Calculate probability of opinion cascade: P = 1 / (1 + exp(-k * delta_opinion))
CALL apoc.custom.declareFunction(
    'psychohistory.cascadeProbability(seed_opinion FLOAT, neighbor_opinion FLOAT, k FLOAT) :: FLOAT',
    'RETURN 1.0 / (1.0 + exp(-$k * ($seed_opinion - $neighbor_opinion))) AS probability'
);

// ============================================
// FUNCTION 16: Equilibrium State (Ising)
// ============================================
// Calculate equilibrium opinion state for given parameters
CALL apoc.custom.declareFunction(
    'psychohistory.equilibriumOpinion(beta FLOAT, J FLOAT, z FLOAT, h FLOAT) :: FLOAT',
    'RETURN tanh($beta * ($J * $z * 0.3 + $h)) AS equilibrium'
);

// ============================================
// VERIFICATION: List all functions
// ============================================
CALL apoc.custom.list()
YIELD name, description
RETURN name, description
ORDER BY name;
