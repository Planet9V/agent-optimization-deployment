# GAP-ML-009: Economic Indicators Integration

**File:** 11_GAP-ML-009_ECONOMIC_INDICATORS.md
**Gap ID:** GAP-ML-009
**Created:** 2025-11-30
**Priority:** HIGH
**Phase:** 3 - Data Integration
**Effort:** L (4-6 weeks)
**Status:** NOT STARTED

---

## Problem Statement

**Current State:**
- No market data integration
- Cannot predict economic bifurcations
- No supply chain modeling
- Economic impact estimates are static

**Desired State:**
- Real-time market data feeds
- Economic Ising model (sentiment → magnetization)
- Supply chain cascade prediction
- Dynamic economic impact calculations

---

## Technical Specification

### Data Sources

```yaml
market_data:
  alpha_vantage:
    api_key: "${ALPHA_VANTAGE_API_KEY}"
    endpoints:
      - "TIME_SERIES_DAILY"
      - "SECTOR"
      - "ECONOMIC_INDICATORS"
    rate_limit: "5/min (free), 75/min (premium)"

  yahoo_finance:
    library: "yfinance"
    data:
      - "Stock prices"
      - "Sector ETFs"
      - "Volatility indices (VIX)"

  fred:
    api: "https://api.stlouisfed.org/fred"
    series:
      - "GDP"
      - "UNRATE"  # Unemployment
      - "CPIAUCSL"  # CPI
      - "T10Y2Y"  # Yield curve
      - "BAMLH0A0HYM2"  # High yield spread

supply_chain:
  sources:
    - "Flexport API"
    - "FreightWaves SONAR"
    - "ISM PMI reports"
```

### Economic Node Schema

```cypher
// Market Sector
CREATE (ms:MarketSector {
  id: 'XLK',  # Technology Select Sector SPDR
  name: 'Information Technology',
  gics_code: '45',

  // Market data
  current_price: 185.50,
  price_change_1d: 0.023,
  price_change_30d: 0.087,
  volume_avg_30d: 12500000,
  market_cap_total: 15000000000000,

  // Volatility metrics
  volatility_30d: 0.18,
  beta: 1.15,
  vix_correlation: 0.72,

  // Ising model parameters
  spin: 1,                    // Bullish = 1, Bearish = -1
  sentiment_score: 0.65,      // Aggregate sentiment
  momentum: 0.4,              // Rate of change
  external_field: 0.1,        // Fed policy, macro events

  // EWS metrics
  ews_variance: 0.12,
  ews_autocorrelation: 0.45,

  // Cyber relevance
  cyber_exposure_score: 0.85,  // How exposed to cyber risk
  breach_cost_multiplier: 2.3, // Relative cost vs average

  last_updated: datetime()
})

// Economic Indicator
CREATE (ei:EconomicIndicator {
  id: 'FRED_T10Y2Y',
  name: 'Treasury Yield Curve (10Y-2Y)',
  source: 'FRED',

  // Current value
  current_value: -0.12,
  previous_value: -0.08,
  change: -0.04,

  // Historical statistics
  mean_5y: 0.82,
  std_5y: 0.65,
  z_score: -1.45,

  // Recession indicator
  inversion_duration_days: 45,
  recession_probability: 0.35,

  // Bifurcation detection
  bifurcation_distance: 0.8,
  critical_threshold: -0.5,

  last_updated: datetime()
})

// Supply Chain Node
CREATE (sc:SupplyChainNode {
  id: 'SC-SEMICONDUCTOR',
  name: 'Semiconductor Supply Chain',
  type: 'CRITICAL_INFRASTRUCTURE',

  // Capacity metrics
  utilization_rate: 0.92,
  lead_time_weeks: 26,
  inventory_days: 45,

  // Risk metrics
  concentration_risk: 0.78,  // Taiwan dominance
  geopolitical_risk: 0.65,
  disruption_probability_30d: 0.15,

  // Economic impact
  downstream_gdp_impact: 0.08,  // 8% of US GDP depends on this
  cascade_multiplier: 3.2,       // Downstream amplification

  // Ising coupling to sectors
  coupling_technology: 0.95,
  coupling_automotive: 0.75,
  coupling_healthcare: 0.45
})
```

### Economic Bifurcation Detection

```python
import numpy as np
from typing import Dict, List, Tuple

class EconomicBifurcationDetector:
    """
    Detect approaching economic bifurcations using EWS metrics.
    """

    def __init__(self):
        # Thresholds calibrated from historical recessions
        self.variance_threshold = 2.0  # Z-score
        self.acf_threshold = 0.8
        self.yield_curve_threshold = -0.5

    def analyze_indicator(
        self,
        series: np.ndarray,
        window: int = 60  # 60 trading days
    ) -> Dict:
        """
        Analyze economic indicator for bifurcation signals.
        """
        recent = series[-window:]

        # Rolling variance (should increase before bifurcation)
        variance = np.var(recent)
        variance_history = [np.var(series[i:i+window]) for i in range(len(series)-window)]
        variance_z = (variance - np.mean(variance_history)) / np.std(variance_history)

        # Rolling autocorrelation (should approach 1)
        acf = np.corrcoef(recent[:-1], recent[1:])[0, 1]

        # Trend (slowing before bifurcation)
        trend = np.polyfit(range(len(recent)), recent, 1)[0]

        return {
            'variance': variance,
            'variance_z_score': variance_z,
            'autocorrelation': acf,
            'trend': trend,
            'critical_slowing': variance_z > 1.5 and acf > 0.7,
            'bifurcation_distance': self._estimate_distance(variance_z, acf),
            'recommendation': self._get_recommendation(variance_z, acf, trend)
        }

    def _estimate_distance(self, variance_z: float, acf: float) -> float:
        """Estimate distance to bifurcation point (0 = at bifurcation)."""
        # Weighted combination of EWS metrics
        return max(0, 1 - (0.5 * min(variance_z / 3, 1) + 0.5 * min(acf / 0.95, 1)))

    def calculate_recession_probability(
        self,
        yield_curve: float,
        unemployment_change: float,
        pmi: float
    ) -> Tuple[float, str]:
        """
        Calculate recession probability from multiple indicators.

        Uses simplified probit model based on historical data.
        """
        # Yield curve inversion is strongest signal
        yc_signal = 1 / (1 + np.exp(5 * yield_curve))  # Sigmoid

        # Unemployment increase
        ue_signal = 1 / (1 + np.exp(-10 * unemployment_change))

        # PMI below 50
        pmi_signal = 1 / (1 + np.exp(0.1 * (pmi - 50)))

        # Weighted combination
        probability = 0.5 * yc_signal + 0.3 * ue_signal + 0.2 * pmi_signal

        # Interpretation
        if probability < 0.2:
            interpretation = "LOW - Expansion likely to continue"
        elif probability < 0.4:
            interpretation = "MODERATE - Watch for deterioration"
        elif probability < 0.6:
            interpretation = "ELEVATED - Defensive positioning recommended"
        else:
            interpretation = "HIGH - Recession indicators flashing"

        return probability, interpretation
```

---

## Implementation Steps

### Step 1: Data Source Integration (Week 1-2)
- [ ] Set up Alpha Vantage API
- [ ] Set up FRED API integration
- [ ] Configure Yahoo Finance data pull
- [ ] Create data refresh scheduler

### Step 2: Schema Implementation (Week 3)
- [ ] Create MarketSector nodes
- [ ] Create EconomicIndicator nodes
- [ ] Create SupplyChainNode types
- [ ] Build sector-indicator relationships

### Step 3: Bifurcation Detection (Week 4)
- [ ] Implement EconomicBifurcationDetector
- [ ] Create recession probability model
- [ ] Add EWS metrics to indicators
- [ ] Build alert system

### Step 4: Integration & API (Week 5-6)
- [ ] Create economic query endpoints
- [ ] Build supply chain cascade API
- [ ] Connect to cyber impact calculations
- [ ] Documentation

---

## Success Criteria

- [ ] Real-time market data refreshing every 15 minutes
- [ ] FRED indicators updated daily
- [ ] Recession probability model operational
- [ ] Supply chain risk visible in dashboard
- [ ] Economic EWS integrated with cyber EWS

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| API rate limits | Medium | High | Caching, multiple sources |
| Data lag | Low | Medium | Accept T+1 for some sources |
| Model accuracy | Medium | Medium | Backtest against recessions |

---

## Dependencies

- API keys for market data providers
- FRED API access
- Phase 1 gaps complete

---

## Memory Keys

- `gap-ml-009-sources`: Data source configurations
- `gap-ml-009-models`: Economic model parameters

---

## References

- Bifurcation Theory: `mckenney-lacan-calculus-2025-11-28/Predictive_04_BIFURCATION_THEORY_CRISIS.md`
- Critical Slowing: `mckenney-lacan-calculus-2025-11-28/Predictive_05_CRITICAL_SLOWING_DOWN_EWS.md`
