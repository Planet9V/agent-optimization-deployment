# GAP-ML-012: Backtesting Framework

**File:** 12_GAP-ML-012_BACKTESTING.md
**Gap ID:** GAP-ML-012
**Created:** 2025-11-30
**Priority:** HIGH
**Phase:** 4 - Validation
**Effort:** XL (8+ weeks)
**Status:** NOT STARTED

---

## Problem Statement

**Current State:**
- Forward-only predictions
- No historical validation
- Unknown accuracy metrics
- Cannot calibrate models

**Desired State:**
- Backtest against known crises
- Calibration with historical data
- Confidence intervals on predictions
- Model accuracy benchmarks

---

## Technical Specification

### Historical Events for Validation

```yaml
cyber_incidents:
  - id: "WANNACRY-2017"
    name: "WannaCry Ransomware"
    date: "2017-05-12"
    type: "RANSOMWARE_EPIDEMIC"
    affected_countries: 150
    affected_systems: 230000
    economic_impact: 4000000000  # $4B
    propagation_time_hours: 48
    r0_observed: 2.8
    containment_method: "Kill switch + patching"

  - id: "NOTPETYA-2017"
    name: "NotPetya"
    date: "2017-06-27"
    type: "DESTRUCTIVE_MALWARE"
    affected_companies: ["Maersk", "Merck", "FedEx"]
    economic_impact: 10000000000  # $10B
    propagation_time_hours: 24
    r0_observed: 3.5
    containment_method: "Network isolation"

  - id: "SOLARWINDS-2020"
    name: "SolarWinds Supply Chain"
    date: "2020-12-13"
    type: "SUPPLY_CHAIN_COMPROMISE"
    affected_organizations: 18000
    dwell_time_months: 9
    detection_method: "FireEye investigation"
    cascade_type: "SUPPLY_CHAIN"

  - id: "COLONIAL-2021"
    name: "Colonial Pipeline"
    date: "2021-05-07"
    type: "RANSOMWARE_CRITICAL_INFRA"
    sector: "ENERGY"
    downtime_days: 6
    economic_impact: 4400000  # Ransom paid
    cascade_effects: ["Fuel shortage", "Price spike"]

  - id: "LOG4SHELL-2021"
    name: "Log4j/Log4Shell"
    date: "2021-12-09"
    type: "ZERO_DAY_EPIDEMIC"
    cve: "CVE-2021-44228"
    affected_systems: "Billions"
    exploitation_start_hours: 9
    r0_observed: 4.2

  - id: "MOVEIT-2023"
    name: "MOVEit Transfer"
    date: "2023-05-31"
    type: "ZERO_DAY_MASS_EXPLOITATION"
    cve: "CVE-2023-34362"
    affected_organizations: 2500
    affected_individuals: 66000000
    attack_group: "Cl0p"

economic_crises:
  - id: "GFC-2008"
    name: "Global Financial Crisis"
    date: "2008-09-15"
    trigger: "Lehman Brothers bankruptcy"
    ews_signals: ["Yield curve inversion", "Credit spread widening"]
    detection_lead_time_months: 6

  - id: "COVID-CRASH-2020"
    name: "COVID-19 Market Crash"
    date: "2020-03-09"
    trigger: "Pandemic + oil price war"
    market_decline: 0.34  # 34% from peak
```

### Backtesting Framework Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Backtesting Framework                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │  Historical  │         │  Model       │                 │
│  │  Data Store  │────────▶│  Runner      │                 │
│  │  (Time-series)│        │              │                 │
│  └──────────────┘         └──────┬───────┘                 │
│                                  │                          │
│                           ┌──────▼───────┐                 │
│                           │  Prediction  │                 │
│                           │  Engine      │                 │
│                           └──────┬───────┘                 │
│                                  │                          │
│         ┌────────────────────────┼────────────────────┐    │
│         │                        │                    │    │
│  ┌──────▼───────┐   ┌──────▼───────┐   ┌──────▼───────┐  │
│  │  Accuracy    │   │  Calibration │   │  Confidence  │  │
│  │  Metrics     │   │  Tuning      │   │  Intervals   │  │
│  └──────────────┘   └──────────────┘   └──────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Backtesting Implementation

```python
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class BacktestResult:
    event_id: str
    event_date: datetime
    prediction_date: datetime
    lead_time_days: int
    predicted_probability: float
    actual_occurred: bool
    prediction_correct: bool
    confidence_interval: Tuple[float, float]

class BacktestingFramework:
    """
    Backtest McKenney-Lacan predictions against historical events.
    """

    def __init__(self, historical_data: Dict, model):
        self.historical_data = historical_data
        self.model = model
        self.results: List[BacktestResult] = []

    def run_backtest(
        self,
        events: List[Dict],
        prediction_windows: List[int] = [7, 14, 30, 60, 90]
    ) -> Dict:
        """
        Run backtest for all events at multiple prediction windows.

        Args:
            events: List of historical events to predict
            prediction_windows: Days before event to make prediction

        Returns:
            Comprehensive accuracy metrics
        """
        for event in events:
            event_date = datetime.fromisoformat(event['date'])

            for window in prediction_windows:
                prediction_date = event_date - timedelta(days=window)

                # Get historical state at prediction_date
                historical_state = self._get_state_at_date(prediction_date)

                # Run model prediction
                prediction = self.model.predict(historical_state)

                # Record result
                result = BacktestResult(
                    event_id=event['id'],
                    event_date=event_date,
                    prediction_date=prediction_date,
                    lead_time_days=window,
                    predicted_probability=prediction['probability'],
                    actual_occurred=True,
                    prediction_correct=prediction['probability'] > 0.5,
                    confidence_interval=prediction['confidence_interval']
                )
                self.results.append(result)

        return self._calculate_metrics()

    def _calculate_metrics(self) -> Dict:
        """Calculate comprehensive accuracy metrics."""
        by_window = {}

        for window in [7, 14, 30, 60, 90]:
            window_results = [r for r in self.results if r.lead_time_days == window]

            if window_results:
                true_positives = sum(1 for r in window_results if r.prediction_correct)
                total = len(window_results)

                # Calculate metrics
                accuracy = true_positives / total
                avg_probability = np.mean([r.predicted_probability for r in window_results])

                # Brier score (lower is better)
                brier = np.mean([(r.predicted_probability - 1) ** 2 for r in window_results])

                # Calibration (predicted prob vs actual rate)
                calibration = avg_probability / accuracy if accuracy > 0 else float('inf')

                by_window[window] = {
                    'accuracy': accuracy,
                    'avg_probability': avg_probability,
                    'brier_score': brier,
                    'calibration_ratio': calibration,
                    'sample_size': total
                }

        return {
            'by_window': by_window,
            'overall_accuracy': np.mean([m['accuracy'] for m in by_window.values()]),
            'overall_brier': np.mean([m['brier_score'] for m in by_window.values()]),
            'best_window': min(by_window, key=lambda w: by_window[w]['brier_score']),
            'total_events': len(set(r.event_id for r in self.results))
        }

    def calibrate_model(self, metric: str = 'brier_score') -> Dict:
        """
        Find optimal model parameters through backtesting.

        Returns:
            Optimal parameters and performance improvement
        """
        # Grid search over model parameters
        param_grid = {
            'ising_temperature': [0.3, 0.5, 0.7, 1.0],
            'cascade_threshold': [0.2, 0.3, 0.4, 0.5],
            'ews_window': [14, 30, 60],
            'r0_network_factor': [0.8, 1.0, 1.2]
        }

        best_params = None
        best_score = float('inf')

        for temp in param_grid['ising_temperature']:
            for thresh in param_grid['cascade_threshold']:
                for window in param_grid['ews_window']:
                    for r0_factor in param_grid['r0_network_factor']:
                        # Update model parameters
                        self.model.set_params(
                            temperature=temp,
                            threshold=thresh,
                            ews_window=window,
                            r0_factor=r0_factor
                        )

                        # Run backtest
                        results = self.run_backtest(self.historical_data['events'])

                        if results[f'overall_{metric}'] < best_score:
                            best_score = results[f'overall_{metric}']
                            best_params = {
                                'temperature': temp,
                                'threshold': thresh,
                                'ews_window': window,
                                'r0_factor': r0_factor
                            }

        return {
            'best_params': best_params,
            'best_score': best_score,
            'improvement': f"{(1 - best_score / 0.25) * 100:.1f}%"  # vs random
        }
```

---

## Implementation Steps

### Step 1: Historical Data Collection (Week 1-3)
- [ ] Compile cyber incident database (2015-2024)
- [ ] Collect economic crisis data
- [ ] Build time-series snapshots for each event
- [ ] Validate data quality

### Step 2: Framework Implementation (Week 4-5)
- [ ] Implement BacktestingFramework class
- [ ] Create historical state reconstruction
- [ ] Build accuracy metric calculations
- [ ] Implement calibration grid search

### Step 3: Model Integration (Week 6-7)
- [ ] Connect Ising model to framework
- [ ] Connect cascade model to framework
- [ ] Connect EWS model to framework
- [ ] Connect R0 model to framework

### Step 4: Validation & Reporting (Week 8+)
- [ ] Run full backtests on all events
- [ ] Generate accuracy reports
- [ ] Calibrate model parameters
- [ ] Create confidence interval methodology
- [ ] Documentation

---

## Success Criteria

- [ ] Backtest against 10+ historical cyber incidents
- [ ] Backtest against 5+ economic crises
- [ ] Accuracy >70% at 30-day prediction window
- [ ] Brier score <0.2 (better than random)
- [ ] Calibrated model parameters stored

---

## Validation Events (Priority Order)

1. **WannaCry (2017)** - Epidemic R0 validation
2. **NotPetya (2017)** - Cascade validation
3. **SolarWinds (2020)** - Supply chain cascade
4. **Log4Shell (2021)** - Zero-day epidemic
5. **Colonial Pipeline (2021)** - Critical infrastructure
6. **MOVEit (2023)** - Mass exploitation
7. **GFC (2008)** - Economic bifurcation
8. **COVID Crash (2020)** - Black swan

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Insufficient historical data | High | Medium | Synthetic data generation |
| Overfitting to known events | High | Medium | Hold-out validation set |
| Survivorship bias | Medium | Medium | Include near-miss events |

---

## Dependencies

- All Phase 1-3 gaps complete
- Historical data collected
- Model implementations stable

---

## Memory Keys

- `gap-ml-012-events`: Historical event database
- `gap-ml-012-results`: Backtest results
- `gap-ml-012-calibration`: Calibrated parameters

---

## References

- Cyber Events: Public incident reports, news archives
- Economic Events: FRED data, market data archives
- EWS Theory: `mckenney-lacan-calculus-2025-11-28/Predictive_05_CRITICAL_SLOWING_DOWN_EWS.md`
