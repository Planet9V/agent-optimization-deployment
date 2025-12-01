# GAP-ML-006: True Autocorrelation

**File:** 07_GAP-ML-006_AUTOCORRELATION.md
**Gap ID:** GAP-ML-006
**Created:** 2025-11-30
**Priority:** HIGH
**Phase:** 2 - Core Math
**Effort:** M (2-4 weeks)
**Status:** NOT STARTED

---

## Problem Statement

**Current State:**
- Single-point autocorrelation estimate only
- No true time-series windowing
- Limited historical data for calculation
- Approximated values reduce EWS accuracy

**Desired State:**
- Rolling window autocorrelation (lag-1 to lag-N)
- True ACF/PACF computation
- Integration with time-series database (TimescaleDB)
- Accurate EWS metrics for crisis prediction

---

## Technical Specification

### Autocorrelation Formula

```
ACF(k) = Σ(x_t - μ)(x_{t-k} - μ) / Σ(x_t - μ)²

Where:
- k = lag (typically 1 for EWS)
- x_t = value at time t
- μ = mean of the series
- ACF(1) → 1 as system approaches critical transition
```

### Time-Series Storage Schema

```sql
-- TimescaleDB hypertable for EWS metrics
CREATE TABLE ews_timeseries (
    entity_id VARCHAR(50) NOT NULL,
    entity_type VARCHAR(20) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,

    -- Raw metrics
    spin INTEGER,
    threshold FLOAT,
    volatility FLOAT,

    -- Calculated metrics (rolling)
    variance_7d FLOAT,
    variance_30d FLOAT,
    autocorrelation_lag1 FLOAT,
    autocorrelation_lag7 FLOAT,

    -- Metadata
    calculation_timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Convert to hypertable
SELECT create_hypertable('ews_timeseries', 'timestamp');

-- Continuous aggregate for ACF
CREATE MATERIALIZED VIEW ews_acf_hourly
WITH (timescaledb.continuous) AS
SELECT
    entity_id,
    time_bucket('1 hour', timestamp) AS bucket,
    avg(spin) as mean_spin,
    stddev(spin) as std_spin,
    count(*) as sample_count
FROM ews_timeseries
GROUP BY entity_id, bucket;
```

### Rolling ACF Calculation

```python
import numpy as np
from scipy import stats

def rolling_autocorrelation(series: np.ndarray, lag: int = 1, window: int = 30) -> np.ndarray:
    """
    Calculate rolling autocorrelation with specified lag.

    Args:
        series: Time series values
        lag: Lag for autocorrelation (default: 1)
        window: Rolling window size (default: 30 observations)

    Returns:
        Array of autocorrelation values
    """
    n = len(series)
    acf_values = np.full(n, np.nan)

    for i in range(window + lag, n):
        window_data = series[i - window:i]
        lagged_data = series[i - window - lag:i - lag]

        # Calculate ACF for this window
        if len(window_data) == len(lagged_data):
            mean_val = np.mean(window_data)
            numerator = np.sum((window_data - mean_val) * (lagged_data - mean_val))
            denominator = np.sum((window_data - mean_val) ** 2)

            if denominator > 0:
                acf_values[i] = numerator / denominator

    return acf_values


def calculate_ews_metrics(entity_id: str, lookback_days: int = 30) -> dict:
    """
    Calculate complete EWS metrics for an entity.
    """
    # Fetch time series from TimescaleDB
    series = fetch_timeseries(entity_id, lookback_days)

    return {
        'variance': np.var(series),
        'std_dev': np.std(series),
        'acf_lag1': rolling_autocorrelation(series, lag=1)[-1],
        'acf_lag7': rolling_autocorrelation(series, lag=7)[-1],
        'critical_slowing': np.var(series) * rolling_autocorrelation(series, lag=1)[-1],
        'trend': stats.linregress(range(len(series)), series).slope
    }
```

### Neo4j Integration Query

```cypher
// Update actor with calculated ACF from TimescaleDB
MATCH (a:Actor {id: $actor_id})
SET a.ews_autocorrelation = $acf_value,
    a.ews_variance = $variance_value,
    a.ews_calculation_timestamp = datetime(),
    a.ews_window_size = $window_size,
    a.ews_critical_slowing = $acf_value * $variance_value

// Query actors with high autocorrelation (approaching criticality)
MATCH (a:Actor)
WHERE a.ews_autocorrelation > 0.85
  AND a.ews_variance > 0.5
RETURN a.id, a.ews_autocorrelation, a.ews_variance,
       a.ews_critical_slowing as critical_slowing_index
ORDER BY critical_slowing_index DESC
```

---

## Implementation Steps

### Step 1: TimescaleDB Setup (Week 1)
- [ ] Install TimescaleDB extension
- [ ] Create ews_timeseries hypertable
- [ ] Create continuous aggregates
- [ ] Set up retention policy

### Step 2: ACF Calculation Service (Week 2)
- [ ] Implement rolling ACF function
- [ ] Create calculation scheduler (hourly)
- [ ] Build batch calculation for all entities
- [ ] Add PACF calculation

### Step 3: Neo4j Sync (Week 3)
- [ ] Create sync procedure TimescaleDB → Neo4j
- [ ] Update Cypher queries to use new ACF values
- [ ] Add ACF to EWS alert triggers

### Step 4: Validation (Week 4)
- [ ] Validate against known critical transitions
- [ ] Tune window sizes
- [ ] Performance optimization
- [ ] Documentation

---

## Success Criteria

- [ ] ACF calculated with true rolling window
- [ ] TimescaleDB storing historical metrics
- [ ] Sync to Neo4j within 5 minutes of calculation
- [ ] EWS alerts more accurate than single-point estimate
- [ ] Query performance <100ms

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| TimescaleDB resource usage | Medium | Medium | Retention policy, continuous aggregates |
| Sync lag | Low | Medium | Real-time triggers for critical entities |

---

## Dependencies

- TimescaleDB infrastructure
- Historical metric data (from GAP-ML-004)
- Neo4j EWS properties

---

## Memory Keys

- `gap-ml-006-formulas`: ACF calculation parameters
- `gap-ml-006-timescale`: TimescaleDB configuration

---

## References

- EWS Theory: `mckenney-lacan-calculus-2025-11-28/Predictive_05_CRITICAL_SLOWING_DOWN_EWS.md`
- Bifurcation: `mckenney-lacan-calculus-2025-11-28/Predictive_04_BIFURCATION_THEORY_CRISIS.md`
