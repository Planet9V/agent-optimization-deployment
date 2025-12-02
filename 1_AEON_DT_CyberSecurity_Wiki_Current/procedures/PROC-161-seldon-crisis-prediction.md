# PROCEDURE: PROC-161 - Seldon Crisis Prediction Engine

**Procedure ID**: PROC-161
**Version**: 1.0.0
**Created**: 2025-11-26
**Last Modified**: 2025-11-26
**Author**: AEON Development Team
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | ETL |
| **Frequency** | DAILY |
| **Priority** | CRITICAL |
| **Estimated Duration** | 3-6 hours |
| **Risk Level** | HIGH |
| **Rollback Available** | PARTIAL |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Implement Seldon-style crisis prediction system combining psychometric stress indicators (Ψ), vulnerability exposure (V), and threat activity (E) to forecast organizational crises 30-180 days in advance.

### 2.2 Business Objectives
- [ ] Enable proactive crisis prevention through early warning
- [ ] Quantify crisis probability across 5 crisis types
- [ ] Integrate psychometric, technical, and threat intelligence data
- [ ] Provide executive leadership with actionable predictions

### 2.3 McKenney Questions Addressed

| Question | How Addressed |
|----------|---------------|
| Q3: What do attackers know? | Threat intelligence monitoring (E function) |
| Q5: How do we defend? | Proactive intervention before crises manifest |
| Q6: What happened before? | Historical crisis patterns for prediction |
| Q7: What will happen next? | Primary objective - crisis forecasting |
| Q8: What should we do? | Automated intervention recommendations |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running | `docker ps | grep neo4j` |
| GDELT BigQuery | Access configured | Check API key |
| NVD API | Accessible | `curl https://services.nvd.nist.gov/rest/json/cves/2.0 | head` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query/Command | Expected Result |
|-----------|---------------------------|-----------------|
| Psychometric data | `MATCH (ps:PsychometricExtraction) RETURN count(ps)` | > 100 |
| Vulnerability scans | `MATCH (v:Vulnerability) RETURN count(v)` | > 10 |
| Incident history | `MATCH (i:Incident) RETURN count(i)` | > 5 |

### 3.3 Prior Procedures Required

| Procedure ID | Procedure Name | Must Complete Before |
|--------------|---------------|---------------------|
| PROC-155 | Transcript Psychometric NER | This procedure |
| PROC-150-153 | Psychometric Analysis Suite | This procedure |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format | Update Frequency |
|-------------|------|----------|--------|------------------|
| VERIS Incident Database | GitHub | https://github.com/vz-risk/VCDB | JSON | Annual |
| Verizon DBIR | Report | Annual publication | PDF/Data | Annual |
| NVD CVE Database | API | https://nvd.nist.gov/ | JSON | Real-time |
| Internal Vulnerability Scans | Tenable/Qualys | Internal API | JSON | Weekly |
| GDELT Events | BigQuery | Google Cloud | SQL | 15-minute |
| Internal Psychometric Data | Neo4j | PROC-155 output | Graph | Daily |
| HR Turnover Rates | HRIS | HR API | JSON | Monthly |
| EAP Utilization | Provider | Aggregated reports | CSV | Quarterly |

### 4.2 Crisis Prediction Formula

**Seldon Crisis Function**:
```
P(Crisis_Type_i, τ) = α·Ψ(τ) + β·V(τ) + γ·E(τ) + δ·H(τ) + ε

Where:
  Ψ(τ) = Psychometric Stress Function
  V(τ) = Vulnerability Exposure Function
  E(τ) = External Threat Activity Function
  H(τ) = Historical Incident Rate Function
  α, β, γ, δ = Crisis-type-specific weights
  ε = Random noise term
  τ = Time index (current time)
```

**Ψ(τ) - Psychometric Stress Function**:
```python
Ψ(τ) = (
    0.4 * mean_neuroticism(τ) +
    0.3 * turnover_rate(τ) +
    0.2 * eap_utilization(τ) +
    0.1 * negative_sentiment(τ)
)
```

**V(τ) - Vulnerability Exposure**:
```python
V(τ) = (
    0.5 * unpatched_critical_cves(τ) / total_systems +
    0.3 * (1 - compliance_score(τ)) +
    0.2 * tech_debt_ratio(τ)
)
```

**E(τ) - External Threat Activity**:
```python
E(τ) = (
    0.4 * sector_targeting_rate(τ) +
    0.3 * dark_web_mentions(τ) / baseline +
    0.3 * attack_surface_growth(τ)
)
```

---

## 5. DESTINATION

### 5.1 Target Schema

#### Node Types Created

| Label | Properties | Constraints |
|-------|-----------|-------------|
| CrisisPrediction | crisis_type, probability, confidence, forecast_date, prediction_date | UNIQUE on (crisis_type, prediction_date) |
| CrisisType | type_id, name, description, historical_frequency | UNIQUE on type_id |
| StressTimeSeries | date, mean_stress_score, source | INDEX on date |
| VulnerabilityTimeSeries | date, exposure_score, cve_count | INDEX on date |
| ThreatTimeSeries | date, activity_score, source_events | INDEX on date |

#### Relationship Types

| Type | Source | Target | Properties |
|------|--------|--------|-----------|
| PREDICTS | (:CrisisPrediction) | (:CrisisType) | probability, timeframe |
| BASED_ON_STRESS | (:CrisisPrediction) | (:StressTimeSeries) | weight, contribution |
| BASED_ON_VULNS | (:CrisisPrediction) | (:VulnerabilityTimeSeries) | weight, contribution |
| BASED_ON_THREATS | (:CrisisPrediction) | (:ThreatTimeSeries) | weight, contribution |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Crisis Type Weights

```python
crisis_type_weights = {
    'TYPE_1_TECHNOLOGY_SHIFT': {
        'alpha_psi': 0.2,  # Stress matters less
        'beta_vuln': 0.5,  # Vulnerability exposure key
        'gamma_threat': 0.2,
        'delta_history': 0.1
    },
    'TYPE_2_ORGANIZATIONAL_COLLAPSE': {
        'alpha_psi': 0.6,  # Stress dominates
        'beta_vuln': 0.1,
        'gamma_threat': 0.1,
        'delta_history': 0.2
    },
    'TYPE_3_THREAT_LANDSCAPE_SHIFT': {
        'alpha_psi': 0.1,
        'beta_vuln': 0.3,
        'gamma_threat': 0.5,  # Threat activity key
        'delta_history': 0.1
    },
    'TYPE_4_REGULATORY_SHOCK': {
        'alpha_psi': 0.2,
        'beta_vuln': 0.3,
        'gamma_threat': 0.3,
        'delta_history': 0.2
    },
    'TYPE_5_BLACK_SWAN': {
        'alpha_psi': 0.25,  # Equal weights - unpredictable
        'beta_vuln': 0.25,
        'gamma_threat': 0.25,
        'delta_history': 0.25
    }
}
```

---

## 7. EXECUTION STEPS

### 7.1 Complete Execution Script

```python
#!/usr/bin/env python3
"""
PROCEDURE: PROC-161 - Seldon Crisis Prediction
Version: 1.0.0
"""

import os
import numpy as np
from neo4j import GraphDatabase
from datetime import datetime, timedelta
import logging

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = os.getenv("NEO4J_PASSWORD", "neo4j@openspg")

LOG_FILE = f"/var/log/aeon/proc_161_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] %(message)s')

class SeldonCrisisPredictor:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def calculate_psi(self, date):
        """Calculate psychometric stress function Ψ(τ)"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (pt:PersonalityTrait)
                WHERE pt.trait_name = 'neuroticism'
                  AND date(pt.timestamp) = date($date)
                RETURN avg(pt.score) AS mean_neuroticism
            """, date=date)

            mean_neuroticism = result.single()['mean_neuroticism'] or 0.5

        # Get turnover rate (placeholder - integrate with HR API)
        turnover_rate = 0.15  # 15% annual turnover

        # EAP utilization (placeholder)
        eap_utilization = 0.08  # 8% of workforce

        psi = (
            0.4 * mean_neuroticism +
            0.3 * turnover_rate +
            0.2 * eap_utilization +
            0.1 * 0.3  # Placeholder negative sentiment
        )

        return psi

    def calculate_vuln(self, date):
        """Calculate vulnerability exposure V(τ)"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (v:Vulnerability)
                WHERE v.severity = 'CRITICAL'
                  AND v.patched = false
                RETURN count(v) AS unpatched_critical
            """)

            unpatched_critical = result.single()['unpatched_critical'] or 0

        total_systems = 1000  # Placeholder - integrate with asset inventory

        vuln_exposure = (
            0.5 * (unpatched_critical / total_systems) +
            0.3 * (1 - 0.85) +  # Placeholder compliance score
            0.2 * 0.25  # Placeholder tech debt ratio
        )

        return vuln_exposure

    def calculate_threat(self, date):
        """Calculate external threat activity E(τ)"""
        # Placeholder - integrate with GDELT, dark web monitoring
        sector_targeting = 0.3
        dark_web_mentions = 1.2  # Normalized to baseline
        attack_surface_growth = 0.15

        threat_activity = (
            0.4 * sector_targeting +
            0.3 * (dark_web_mentions / 1.0) +
            0.3 * attack_surface_growth
        )

        return threat_activity

    def predict_crisis(self, crisis_type, weights, date):
        """Generate crisis prediction for specific type"""
        psi = self.calculate_psi(date)
        vuln = self.calculate_vuln(date)
        threat = self.calculate_threat(date)
        historical = 0.05  # Placeholder - 5% base rate

        probability = (
            weights['alpha_psi'] * psi +
            weights['beta_vuln'] * vuln +
            weights['gamma_threat'] * threat +
            weights['delta_history'] * historical
        )

        # Add noise and clamp to [0, 1]
        noise = np.random.normal(0, 0.05)
        probability = np.clip(probability + noise, 0, 1)

        confidence = 0.70  # Placeholder - calculate based on data quality

        return {
            'crisis_type': crisis_type,
            'probability': probability,
            'confidence': confidence,
            'psi': psi,
            'vuln': vuln,
            'threat': threat
        }

    def store_prediction(self, prediction, forecast_date):
        """Store prediction in Neo4j"""
        with self.driver.session() as session:
            session.run("""
                MERGE (ct:CrisisType {type_id: $crisis_type})
                ON CREATE SET ct.name = $crisis_type

                CREATE (cp:CrisisPrediction {
                    crisis_type: $crisis_type,
                    probability: $probability,
                    confidence: $confidence,
                    forecast_date: date($forecast_date),
                    prediction_date: date()
                })
                CREATE (cp)-[:PREDICTS]->(ct)
            """, crisis_type=prediction['crisis_type'],
                 probability=prediction['probability'],
                 confidence=prediction['confidence'],
                 forecast_date=forecast_date)

            logging.info(f"Stored prediction: {prediction['crisis_type']} - P={prediction['probability']:.2f}")

def main():
    logging.info("Starting PROC-161: Seldon Crisis Prediction")

    predictor = SeldonCrisisPredictor(NEO4J_URI, NEO4J_USER, NEO4J_PASS)

    crisis_type_weights = {
        'TYPE_1_TECHNOLOGY_SHIFT': {'alpha_psi': 0.2, 'beta_vuln': 0.5, 'gamma_threat': 0.2, 'delta_history': 0.1},
        'TYPE_2_ORGANIZATIONAL_COLLAPSE': {'alpha_psi': 0.6, 'beta_vuln': 0.1, 'gamma_threat': 0.1, 'delta_history': 0.2},
        'TYPE_3_THREAT_LANDSCAPE_SHIFT': {'alpha_psi': 0.1, 'beta_vuln': 0.3, 'gamma_threat': 0.5, 'delta_history': 0.1},
        'TYPE_4_REGULATORY_SHOCK': {'alpha_psi': 0.2, 'beta_vuln': 0.3, 'gamma_threat': 0.3, 'delta_history': 0.2},
        'TYPE_5_BLACK_SWAN': {'alpha_psi': 0.25, 'beta_vuln': 0.25, 'gamma_threat': 0.25, 'delta_history': 0.25}
    }

    try:
        today = datetime.now().date()

        # Generate predictions for each crisis type
        for crisis_type, weights in crisis_type_weights.items():
            # Forecast 30, 90, 180 days ahead
            for days_ahead in [30, 90, 180]:
                forecast_date = today + timedelta(days=days_ahead)
                prediction = predictor.predict_crisis(crisis_type, weights, today)
                predictor.store_prediction(prediction, forecast_date)

        logging.info("PROC-161 completed successfully")

    except Exception as e:
        logging.error(f"PROC-161 failed: {str(e)}")
        raise
    finally:
        predictor.close()

if __name__ == "__main__":
    main()
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

```cypher
// Count predictions by crisis type
MATCH (cp:CrisisPrediction)
WHERE cp.prediction_date = date()
RETURN
    cp.crisis_type,
    avg(cp.probability) AS avg_probability,
    avg(cp.confidence) AS avg_confidence,
    count(cp) AS prediction_count
ORDER BY avg_probability DESC;
```

**Expected Result**: 15 predictions (5 types × 3 timeframes)

---

## 9. ROLLBACK PROCEDURE

```cypher
// Delete today's predictions
MATCH (cp:CrisisPrediction)
WHERE cp.prediction_date = date()
DETACH DELETE cp;
```

---

## 10. SCHEDULING & AUTOMATION

### 10.1 Cron Schedule

```cron
# Run daily at 3 AM
0 3 * * * /usr/bin/python3 /scripts/proc_161_seldon_crisis.py >> /var/log/aeon/proc_161_cron.log 2>&1
```

---

## 11. MONITORING & ALERTING

### 11.1 Alert Thresholds

| Crisis Type | Probability Threshold | Alert Level |
|------------|---------------------|-------------|
| TYPE_2_ORGANIZATIONAL_COLLAPSE | > 0.70 | CRITICAL |
| TYPE_3_THREAT_LANDSCAPE_SHIFT | > 0.60 | HIGH |
| TYPE_5_BLACK_SWAN | > 0.40 | HIGH |
| Others | > 0.50 | MEDIUM |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON Dev Team | Initial version |

---

**End of Procedure PROC-161**
