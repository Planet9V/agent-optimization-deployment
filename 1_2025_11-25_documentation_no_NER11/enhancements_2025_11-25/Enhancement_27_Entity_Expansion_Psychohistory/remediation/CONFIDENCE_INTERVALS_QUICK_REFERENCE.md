# Confidence Intervals Quick Reference Card

**Enhancement 27 - Psychohistory Functions**
**Status**: PRODUCTION READY ✓

---

## 📋 Function Overview

| # | Function | Use Case | Input | Output |
|---|----------|----------|-------|--------|
| 1 | `bootstrapCI` | General CI for any statistic | List of values | CI map |
| 2 | `autocorrelationCI` | Critical slowing detection | Autocorr coefficient | CI map |
| 3 | `cascadePredictionInterval` | Cascade event prediction | Probability, population | PI map |
| 4 | `epidemicR0CI` | Epidemic spread analysis | R₀ estimate | CI map |
| 5 | `propagateUncertaintyDelta` | Transform uncertainty | Value, variance, transform | CI map |
| 6 | `propagateUncertaintyMonteCarlo` | Complex model uncertainty | Parameters, equation | CI map |
| 7 | `predictWithUncertainty` | Integrated prediction | Equation, params, data | Prediction map |

---

## 🚀 Quick Start Examples

### Example 1: Bootstrap CI for Threat Severity
```cypher
MATCH (t:Threat)-[:HAS_SEVERITY]->(s:Severity)
WITH collect(toFloat(s.score)) AS severity_scores
RETURN psychohistory.bootstrapCI(
  severity_scores,
  'mean',      // statistic: 'mean', 'median', 'std', 'autocorr_lag1'
  1000,        // bootstrap iterations
  0.05         // alpha (0.05 = 95% CI)
) AS severity_ci;
```

**Returns**:
```json
{
  "lower_bound": 7.2,
  "upper_bound": 8.8,
  "confidence_level": 0.95,
  "method": "bootstrap_percentile",
  "reference": "Efron & Tibshirani (1993)",
  "n_bootstrap": 1000
}
```

---

### Example 2: Autocorrelation CI for Critical Slowing
```cypher
MATCH (e:Event)
WHERE e.timestamp > datetime() - duration({days: 90})
WITH e ORDER BY e.timestamp
WITH collect(toFloat(e.intensity)) AS timeseries
WITH psychohistory.autocorrelation(timeseries, 1) AS lag1_autocorr
RETURN psychohistory.autocorrelationCI(
  lag1_autocorr,
  size(timeseries),
  0.05
) AS critical_slowing_ci;
```

**Returns**:
```json
{
  "point_estimate": 0.65,
  "lower_bound": 0.48,
  "upper_bound": 0.77,
  "confidence_level": 0.95,
  "method": "fisher_z_transform",
  "reference": "Fisher (1921)",
  "n_samples": 90,
  "effective_df": 87
}
```

**Interpretation**: If lower_bound > 0.5, significant autocorrelation (critical slowing warning)

---

### Example 3: Cascade Prediction Interval
```cypher
MATCH (vuln:Vulnerability)
WHERE vuln.exploitability_score > 7.0
WITH count(vuln) AS vulnerable_pop
WITH 0.15 AS cascade_prob, vulnerable_pop  // From cascade equation
RETURN psychohistory.cascadePredictionInterval(
  cascade_prob,
  vulnerable_pop,
  0.05
) AS cascade_pi;
```

**Returns**:
```json
{
  "predicted_probability": 0.15,
  "predicted_count": 150,
  "lower_bound_probability": 0.12,
  "upper_bound_probability": 0.18,
  "lower_bound_count": 120,
  "upper_bound_count": 180,
  "population_size": 1000,
  "confidence_level": 0.95,
  "method": "agresti_coull_binomial",
  "interpretation": "We are 95% confident that between 120 and 180 entities will be affected in a population of 1000"
}
```

---

### Example 4: Epidemic R₀ CI
```cypher
MATCH (malware:Malware)-[:TRANSMITTED_TO]->(target)
WITH malware.transmission_rate AS beta,
     avg(malware.contacts_per_day) AS contacts,
     malware.infectious_period_days AS duration,
     count(target) AS n_obs
WITH beta * contacts * duration AS r0, n_obs
RETURN psychohistory.epidemicR0CI(r0, n_obs, 0.05) AS r0_ci;
```

**Returns**:
```json
{
  "point_estimate": 2.5,
  "lower_bound": 2.1,
  "upper_bound": 2.9,
  "confidence_level": 0.95,
  "method": "log_normal_approximation",
  "interpretation": "Epidemic growth certain (lower bound > 1)"
}
```

**Decision Rules**:
- `lower_bound > 1.0`: Epidemic growth certain → IMMEDIATE ACTION
- `upper_bound < 1.0`: Epidemic decay certain → MONITORING
- `r0 > 1 AND lower_bound < 1`: Growth likely but uncertain → PREPARE

---

### Example 5: Delta Method Uncertainty Propagation
```cypher
WITH 10.0 AS value, 4.0 AS variance
RETURN psychohistory.propagateUncertaintyDelta(
  value,
  variance,
  'log',    // transformation: 'log', 'exp', 'sqrt', 'square', 'inverse'
  0.05
) AS delta_ci;
```

**Returns**:
```json
{
  "original_value": 10.0,
  "original_variance": 4.0,
  "transformation": "log",
  "transformed_value": 2.30,
  "transformed_variance": 0.04,
  "transformed_se": 0.20,
  "lower_bound": 1.91,
  "upper_bound": 2.69,
  "confidence_level": 0.95,
  "method": "delta_method"
}
```

**Use Cases**: Transform R₀ to log scale, variance to std, rates to probabilities

---

### Example 6: Monte Carlo Uncertainty
```cypher
WITH {
  beta: {mean: 0.3, variance: 0.01},
  contacts: {mean: 5.0, variance: 1.0},
  duration: {mean: 7.0, variance: 0.5}
} AS params
RETURN psychohistory.propagateUncertaintyMonteCarlo(
  params,
  'epidemic_r0',
  5000,     // Monte Carlo simulations
  0.05
) AS mc_ci;
```

**Returns**:
```json
{
  "equation": "epidemic_r0",
  "mean_prediction": 10.5,
  "median_prediction": 10.4,
  "lower_bound": 8.7,
  "upper_bound": 12.3,
  "confidence_level": 0.95,
  "n_simulations": 5000,
  "method": "monte_carlo_propagation",
  "full_distribution_percentiles": {
    "p05": 8.9,
    "p25": 9.8,
    "p50": 10.4,
    "p75": 11.1,
    "p95": 12.1
  }
}
```

---

### Example 7: Integrated Prediction
```cypher
WITH {
  beta: 0.3,
  contacts: 5.0,
  duration: 7.0,
  n_observations: 100
} AS params
RETURN psychohistory.predictWithUncertainty(
  'epidemic_r0',
  params,
  [1.0, 2.0, 3.0, 4.0, 5.0],  // Historical data
  0.05
) AS prediction;
```

**Returns**:
```json
{
  "equation": "epidemic_r0",
  "point_prediction": 10.5,
  "confidence_interval": {
    "lower_bound": 9.45,
    "upper_bound": 11.55,
    "confidence_level": 0.95,
    "method": "simplified"
  },
  "uncertainty_quantified": true,
  "timestamp": "2025-11-28T...",
  "data_quality_score": "low"
}
```

---

## 🎯 Parameter Reference

### Common Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `alpha` | FLOAT | 0.01-0.10 | Significance level (0.05 = 95% CI) |
| `n_bootstrap` | INTEGER | 100-10000 | Bootstrap iterations (more = accurate) |
| `n_simulations` | INTEGER | 500-10000 | Monte Carlo draws |
| `statistic` | STRING | see below | Bootstrap statistic type |
| `transformation` | STRING | see below | Delta method transform |

### Statistic Types (bootstrapCI)
- `'mean'`: Average value
- `'median'`: Middle value (50th percentile)
- `'std'`: Standard deviation
- `'autocorr_lag1'`: Lag-1 autocorrelation

### Transformation Types (propagateUncertaintyDelta)
- `'log'`: Natural logarithm
- `'exp'`: Exponential
- `'sqrt'`: Square root
- `'square'`: Squaring
- `'inverse'`: Reciprocal (1/x)

### Equation Types (Monte Carlo)
- `'epidemic_r0'`: R₀ = β × contacts × duration
- `'cascade_probability'`: P = 1 - exp(-k × activation)
- `'critical_slowing_variance'`: Variance warning signal
- `'tipping_probability'`: Logistic tipping function

---

## 📊 Confidence Level Guide

| Alpha | Confidence Level | Z-Critical | Use Case |
|-------|-----------------|------------|----------|
| 0.10 | 90% | 1.645 | Exploratory analysis |
| 0.05 | 95% | 1.96 | Standard reporting |
| 0.01 | 99% | 2.576 | High-stakes decisions |

**Rule of Thumb**: Use 95% (alpha=0.05) for most applications

---

## ⚠️ Common Pitfalls

### 1. Small Sample Sizes
```cypher
// ❌ BAD: Too few data points
psychohistory.bootstrapCI([1.0, 2.0, 3.0], 'mean', 100, 0.05)
// Wide, unreliable CI

// ✓ GOOD: Adequate sample
psychohistory.bootstrapCI([...50+ values...], 'mean', 1000, 0.05)
// Narrow, reliable CI
```

**Minimum Samples**: 30 for meaningful CI, 100+ for reliable results

### 2. Too Few Bootstrap Iterations
```cypher
// ❌ BAD: Unstable estimates
psychohistory.bootstrapCI(values, 'mean', 50, 0.05)

// ✓ GOOD: Stable estimates
psychohistory.bootstrapCI(values, 'mean', 1000, 0.05)
```

**Recommended**: 500-1000 for bootstrap, 1000-5000 for Monte Carlo

### 3. Incorrect Alpha Interpretation
```cypher
// alpha = 0.05 means 95% confidence
// NOT 5% confidence!
// Lower alpha = higher confidence = wider intervals
```

---

## 🔬 Academic References

1. **Bootstrap**: Efron & Tibshirani (1993) - *An Introduction to the Bootstrap*
2. **Fisher Z**: Fisher (1921) - *Probable error of correlation coefficient*
3. **Binomial CI**: Agresti & Coull (1998) - *Binomial proportion intervals*
4. **Delta Method**: Barndorff-Nielsen & Cox (1994) - *Inference and Asymptotics*

---

## 📈 Performance Tips

### Optimization Strategies
```cypher
// 1. Use appropriate iteration counts
// Exploratory: 100-500 iterations
// Production: 1000-5000 iterations
// Publication: 5000-10000 iterations

// 2. Cache results for repeated queries
MATCH (analysis:Analysis {id: 'threat_severity_ci'})
RETURN analysis.cached_ci  // Reuse if recent

// 3. Batch multiple CI calculations
WITH threats, vulnerabilities, events
RETURN {
  threat_ci: psychohistory.bootstrapCI(...),
  vuln_ci: psychohistory.bootstrapCI(...),
  event_ci: psychohistory.bootstrapCI(...)
} AS all_cis
```

---

## 🛠️ Troubleshooting

### Issue: "Function not found"
**Solution**: Deploy functions using `deploy_confidence_intervals.sh`

### Issue: CI too wide
**Solutions**:
- Increase sample size
- Increase bootstrap iterations
- Check for outliers
- Consider different statistic

### Issue: CI asymmetric
**Explanation**: Normal for skewed distributions (not a bug!)
**Action**: Consider log transformation for right-skewed data

---

## ✅ Quality Checklist

Before deployment:
- [ ] Sample size ≥ 30
- [ ] Bootstrap iterations ≥ 1000
- [ ] Alpha appropriate (0.05 typical)
- [ ] Test query runs successfully
- [ ] Results interpretable
- [ ] Documentation updated

---

**Quick Reference Version**: 1.0
**Last Updated**: 2025-11-28
**Status**: PRODUCTION READY ✓
