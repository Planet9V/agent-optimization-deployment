# Enhancement E20: Data Sources for Personality-Team Fit Analysis

**File:** DATA_SOURCES.md
**Created:** 2025-11-26
**Version:** 1.0.0
**Purpose:** Comprehensive data source specifications for personality-based team optimization
**Status:** ACTIVE

---

## Overview

Personality-team fit analysis requires psychometric assessment data, team composition information, performance metrics for validation, and behavioral observation data. This document specifies required data sources, assessment instruments, schemas, and quality requirements.

---

## Table of Contents

1. [Psychometric Assessment Data](#1-psychometric-assessment-data)
2. [Team Composition Data](#2-team-composition-data)
3. [Performance Validation Data](#3-performance-validation-data)
4. [Behavioral Observation Data](#4-behavioral-observation-data)
5. [Turnover and Retention Data](#5-turnover-and-retention-data)
6. [Conflict and Interpersonal Data](#6-conflict-and-interpersonal-data)
7. [Training and Development Data](#7-training-and-development-data)
8. [Assessment Administration Procedures](#8-assessment-administration-procedures)
9. [Data Quality Requirements](#9-data-quality-requirements)
10. [Privacy and Ethical Compliance](#10-privacy-and-ethical-compliance)

---

## 1. Psychometric Assessment Data

### 1.1 Big Five Personality Assessment

**Purpose:** Measure core personality traits (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)

**Recommended Instruments:**

**NEO-PI-R (NEO Personality Inventory-Revised)**
- **Items:** 240 questions
- **Administration Time:** 40-50 minutes
- **Scoring:** Proprietary, requires licensed psychometric software
- **Reliability:** α > 0.85 for all five factors
- **Validity:** Extensive validation across cultures and populations
- **Cost:** ~$50-100 per assessment (includes scoring)
- **Source:** Psychological Assessment Resources (PAR)

**BFI-2 (Big Five Inventory-2)**
- **Items:** 60 questions
- **Administration Time:** 10-15 minutes
- **Scoring:** Free, open-source scoring algorithms available
- **Reliability:** α > 0.80 for all five factors
- **Validity:** Strong correlation with NEO-PI-R (r > 0.80)
- **Cost:** Free (research use), licensing for commercial use
- **Source:** Berkeley Personality Lab

**IPIP-NEO (International Personality Item Pool)**
- **Items:** 120 or 300 questions
- **Administration Time:** 20-45 minutes
- **Scoring:** Free, open-source
- **Reliability:** α > 0.75 for five factors
- **Validity:** Good convergence with NEO-PI-R
- **Cost:** Free
- **Source:** IPIP website (ipip.ori.org)

**Data Elements:**

```json
{
  "assessment_id": "ASSESS-BIG5-2025-042",
  "person_id": "CAND-2025-042",
  "assessment_date": "2025-11-26",
  "instrument": "BFI-2",
  "responses": [3, 4, 2, 5, 3, ...],  // 60 Likert scale responses (1-5)
  "scores": {
    "openness": {
      "raw_score": 38,
      "percentile": 45.2,
      "normalized": 0.452,
      "facets": {
        "intellectual_curiosity": 0.52,
        "aesthetic_sensitivity": 0.38,
        "creative_imagination": 0.47
      }
    },
    "conscientiousness": {
      "raw_score": 48,
      "percentile": 82.1,
      "normalized": 0.821,
      "facets": {
        "organization": 0.85,
        "productiveness": 0.80,
        "responsibility": 0.82
      }
    },
    "extraversion": {
      "raw_score": 25,
      "percentile": 28.3,
      "normalized": 0.283,
      "facets": {
        "sociability": 0.25,
        "assertiveness": 0.32,
        "energy_level": 0.28
      }
    },
    "agreeableness": {
      "raw_score": 42,
      "percentile": 65.0,
      "normalized": 0.650,
      "facets": {
        "compassion": 0.68,
        "respectfulness": 0.63,
        "trust": 0.64
      }
    },
    "neuroticism": {
      "raw_score": 18,
      "percentile": 22.0,
      "normalized": 0.220,
      "facets": {
        "anxiety": 0.20,
        "depression": 0.25,
        "emotional_volatility": 0.21
      }
    }
  },
  "administration_mode": "online_supervised",
  "completion_time_minutes": 14,
  "validity_checks": {
    "response_consistency": 0.92,
    "socially_desirable_responding": 0.15,
    "validity_flags": []
  }
}
```

**Population Norms (for percentile conversion):**

| Trait | Mean (Population) | SD (Population) | 50th Percentile Raw Score |
|-------|-------------------|-----------------|---------------------------|
| Openness | 35.2 | 7.8 | 35 |
| Conscientiousness | 38.6 | 8.2 | 39 |
| Extraversion | 32.4 | 8.5 | 32 |
| Agreeableness | 40.1 | 7.3 | 40 |
| Neuroticism | 28.5 | 9.1 | 29 |

### 1.2 Dark Triad Assessment

**Purpose:** Measure subclinical Machiavellianism, Narcissism, and Psychopathy for adversarial thinking roles

**Recommended Instruments:**

**Short Dark Triad (SD3)**
- **Items:** 27 questions (9 per trait)
- **Administration Time:** 5-10 minutes
- **Scoring:** Open-source, simple summation
- **Reliability:** α > 0.70 for all three traits
- **Validity:** Validated across cultures
- **Cost:** Free
- **Source:** Jones & Paulhus (2014)

**Dirty Dozen**
- **Items:** 12 questions (4 per trait)
- **Administration Time:** 3-5 minutes
- **Scoring:** Open-source
- **Reliability:** α > 0.65 (acceptable for screening)
- **Validity:** Moderate convergence with SD3
- **Cost:** Free
- **Source:** Jonason & Webster (2010)

**Data Elements:**

```json
{
  "assessment_id": "ASSESS-DT-2025-042",
  "person_id": "CAND-2025-042",
  "assessment_date": "2025-11-26",
  "instrument": "SD3",
  "responses": [2, 3, 4, 3, 2, 1, 3, 4, 3, ...],  // 27 Likert scale responses (1-5)
  "scores": {
    "machiavellianism": {
      "raw_score": 27,
      "percentile": 35.4,
      "normalized": 0.354,
      "interpretation": "Moderate strategic thinking, not manipulative"
    },
    "narcissism": {
      "raw_score": 24,
      "percentile": 30.2,
      "normalized": 0.302,
      "interpretation": "Healthy self-confidence, not grandiose"
    },
    "psychopathy": {
      "raw_score": 18,
      "percentile": 18.5,
      "normalized": 0.185,
      "interpretation": "Low callousness, empathetic"
    }
  },
  "ethical_flags": {
    "any_score_above_80th_percentile": false,
    "requires_oversight": false,
    "suitable_for_red_team": true,
    "suitable_for_leadership": true
  },
  "validity_checks": {
    "response_consistency": 0.88,
    "extreme_responding": false
  }
}
```

**Ethical Thresholds:**

| Dark Triad Trait | Acceptable Range (Percentile) | Oversight Required | Do Not Hire |
|------------------|-------------------------------|---------------------|-------------|
| Machiavellianism | 0-80th | >80th | >95th |
| Narcissism | 0-80th | >80th | >95th |
| Psychopathy | 0-60th | >60th | >80th |

**CRITICAL:** Psychopathy scores >80th percentile are disqualifying for all roles. Machiavellianism and Narcissism >80th require leadership approval and ethical oversight.

### 1.3 Cognitive Styles Assessment

**Purpose:** Measure cognitive preferences (Analytical, Creative, Pragmatic, Relational)

**Recommended Instruments:**

**Cognitive Style Indicator (CSI)**
- **Items:** 38 questions
- **Administration Time:** 10-15 minutes
- **Scoring:** Factor analysis (four factors)
- **Reliability:** α > 0.75 for all four styles
- **Cost:** ~$25-50 per assessment
- **Source:** Commercial vendors

**Thinking Styles Inventory (TSI)**
- **Items:** 104 questions
- **Administration Time:** 25-30 minutes
- **Scoring:** Proprietary
- **Reliability:** α > 0.80
- **Cost:** ~$75-100 per assessment

**Data Elements:**

```json
{
  "assessment_id": "ASSESS-COG-2025-042",
  "person_id": "CAND-2025-042",
  "assessment_date": "2025-11-26",
  "instrument": "CSI",
  "responses": [4, 3, 5, 2, 4, ...],  // 38 Likert scale responses
  "scores": {
    "analytical": {
      "factor_score": 1.25,
      "percentile": 85.3,
      "normalized": 0.853,
      "description": "Very high systematic, data-driven thinking"
    },
    "creative": {
      "factor_score": -0.45,
      "percentile": 38.2,
      "normalized": 0.382,
      "description": "Moderate-low creative, imaginative thinking"
    },
    "pragmatic": {
      "factor_score": 0.68,
      "percentile": 72.0,
      "normalized": 0.720,
      "description": "High results-oriented, efficient thinking"
    },
    "relational": {
      "factor_score": 0.12,
      "percentile": 48.5,
      "normalized": 0.485,
      "description": "Moderate people-focused, empathetic thinking"
    }
  },
  "cognitive_profile": "Analyst-Pragmatist (high analytical + pragmatic, moderate creative + relational)"
}
```

### 1.4 Behavioral Dimensions Assessment

**Purpose:** Measure work-relevant behaviors (Risk Tolerance, Stress Resilience, Attention to Detail, Autonomy)

**Assessment Methods:**

**Risk Propensity Scale**
- **Items:** 5 questions
- **Administration Time:** 3-5 minutes
- **Scoring:** Simple average
- **Reliability:** α > 0.70
- **Cost:** Free (academic research)

**Connor-Davidson Resilience Scale (CD-RISC)**
- **Items:** 25 questions
- **Administration Time:** 10 minutes
- **Scoring:** Summation
- **Reliability:** α > 0.89
- **Cost:** ~$40 per assessment
- **Source:** Commercial licensing

**Attention to Detail Questionnaire (Custom)**
- **Items:** 15 questions + behavioral simulation
- **Administration Time:** 20 minutes
- **Scoring:** Composite score
- **Reliability:** α > 0.75 (to be validated)

**Autonomy Preference Scale**
- **Items:** 10 questions
- **Administration Time:** 5 minutes
- **Scoring:** Average
- **Reliability:** α > 0.80

**Data Elements:**

```json
{
  "assessment_id": "ASSESS-BEH-2025-042",
  "person_id": "CAND-2025-042",
  "assessment_date": "2025-11-26",
  "scores": {
    "risk_tolerance": {
      "raw_score": 3.2,
      "percentile": 65.0,
      "normalized": 0.650,
      "interpretation": "Moderate risk tolerance, willing to act under some uncertainty"
    },
    "stress_resilience": {
      "raw_score": 82,
      "percentile": 88.4,
      "normalized": 0.884,
      "interpretation": "Very high stress resilience, thrives under pressure"
    },
    "attention_to_detail": {
      "questionnaire_score": 0.87,
      "simulation_accuracy": 0.95,
      "composite_score": 0.91,
      "percentile": 91.0,
      "normalized": 0.910,
      "interpretation": "Exceptional attention to detail, unlikely to miss critical information"
    },
    "autonomy": {
      "raw_score": 7.2,
      "percentile": 58.0,
      "normalized": 0.580,
      "interpretation": "Moderate autonomy preference, comfortable with both solo and collaborative work"
    }
  }
}
```

---

## 2. Team Composition Data

### Purpose
Current team membership, roles, and personality profiles for fit calculation

### Data Elements

```json
{
  "team_id": "TEAM-SOC-001",
  "team_name": "SOC Alpha Shift",
  "function": "Security Operations Center",
  "manager_id": "EMP-SEC-MGR-005",
  "created_date": "2022-08-15",
  "members": [
    {
      "person_id": "EMP-SEC-012",
      "name_anonymized": "SOC_Analyst_1",
      "role": "SOC Analyst L2",
      "hire_date": "2022-08-20",
      "tenure_months": 39,
      "personality_vector": [0.42, 0.79, 0.25, 0.62, 0.28, 0.36, 0.32, 0.21,
                             0.82, 0.40, 0.70, 0.48, 0.42, 0.85, 0.88, 0.60],
      "last_assessment_date": "2024-11-01",
      "performance_rating": 4.2
    },
    {
      "person_id": "EMP-SEC-015",
      "name_anonymized": "SOC_Analyst_2",
      "role": "SOC Analyst L2",
      "hire_date": "2023-01-10",
      "tenure_months": 34,
      "personality_vector": [0.38, 0.81, 0.33, 0.58, 0.20, 0.34, 0.28, 0.19,
                             0.85, 0.38, 0.72, 0.50, 0.45, 0.88, 0.91, 0.62],
      "last_assessment_date": "2024-11-05",
      "performance_rating": 4.5
    },
    ...
  ],
  "team_statistics": {
    "size": 7,
    "avg_tenure_months": 36.2,
    "turnover_rate_annual": 0.12,
    "avg_performance_rating": 4.3,
    "team_centroid": [0.42, 0.81, 0.28, 0.63, 0.27, 0.36, 0.32, 0.21,
                      0.83, 0.41, 0.71, 0.49, 0.43, 0.84, 0.89, 0.61],
    "diversity_index": 0.18,
    "avg_conflict_risk": 0.12
  }
}
```

### Data Sources

**Primary:**
- HR Information System (HRIS): Workday, SAP SuccessFactors, ADP
- Personality assessment database
- Organizational chart

**Access Methods:**

```python
# Example API call to HRIS
response = requests.get(
    "https://hris.company.com/api/v1/teams/TEAM-SOC-001/members",
    headers={"Authorization": f"Bearer {HRIS_TOKEN}"},
    params={"include_fields": "all"}
)

team_data = response.json()
```

---

## 3. Performance Validation Data

### Purpose
Validate that personality fit scores predict actual job performance

### Data Elements

```json
{
  "person_id": "EMP-SEC-012",
  "performance_period": "2024-H2",
  "metrics": {
    "manager_rating": 4.2,
    "peer_rating": 4.0,
    "self_rating": 3.8,
    "objective_metrics": {
      "alerts_triaged": 1247,
      "false_positive_rate": 0.08,
      "mean_time_to_triage_minutes": 12.5,
      "escalations_accurate": 0.94,
      "incidents_detected": 23,
      "overtime_hours": 15
    },
    "behavioral_metrics": {
      "attendance_rate": 0.98,
      "training_completion_rate": 1.00,
      "peer_collaboration_score": 4.1,
      "initiative_score": 3.9,
      "stress_incidents": 0
    }
  },
  "promotion_readiness": "Ready for L3 within 6 months",
  "attrition_risk": "Low",
  "notes": "Strong performer, detail-oriented, reliable. Opportunity: develop creative threat hunting skills."
}
```

### Validation Analysis

**Correlation Study:**
```python
def validate_fit_scores(team_members, performance_data):
    """
    Correlate fit scores with performance outcomes.
    """
    fit_scores = [m['fit_score_at_hire'] for m in team_members]
    performance_ratings = [p['metrics']['manager_rating'] for p in performance_data]

    correlation = np.corrcoef(fit_scores, performance_ratings)[0, 1]

    print(f"Fit Score vs Performance Correlation: r = {correlation:.3f}")

    # Expected: r > 0.50 for valid fit score model
    if correlation > 0.50:
        print("✓ Fit score is valid predictor of performance")
    else:
        print("⚠️ Fit score needs recalibration")

    return correlation
```

**Target Validity Metrics:**
- Correlation: r > 0.50 (fit score vs performance rating)
- Attrition: Employees with F_total < 0.5 have 2x higher attrition within 2 years
- Time-to-Productivity: Employees with F_total > 0.7 reach full productivity 30% faster

---

## 4. Behavioral Observation Data

### Purpose
Supplement psychometric assessments with real-world behavioral data

### Data Elements

**Structured Interview Data:**
```json
{
  "person_id": "CAND-2025-042",
  "interview_date": "2025-11-20",
  "interviewer_id": "EMP-SEC-MGR-005",
  "behavioral_indicators": {
    "attention_to_detail": {
      "observed": true,
      "examples": ["Candidate caught typo in our sample incident report", "Asked clarifying questions about edge cases"],
      "rating": 4.5
    },
    "stress_resilience": {
      "observed": true,
      "examples": ["Described handling 3 simultaneous P1 incidents calmly", "Positive affect during high-pressure scenario questions"],
      "rating": 4.8
    },
    "collaboration": {
      "observed": true,
      "examples": ["Emphasized team coordination in incident response stories", "Asked about team dynamics"],
      "rating": 4.2
    },
    "adversarial_thinking": {
      "observed": false,
      "examples": [],
      "rating": null
    }
  },
  "culture_fit": {
    "values_alignment": 4.5,
    "communication_style": "Clear, direct, friendly",
    "red_flags": []
  }
}
```

**Work Sample Data:**
```json
{
  "person_id": "CAND-2025-042",
  "work_sample_type": "Incident Triage Exercise",
  "completion_date": "2025-11-21",
  "performance": {
    "accuracy": 0.92,
    "speed": "15 minutes (target: 20)",
    "thoroughness": 4.7,
    "prioritization": 4.5,
    "documentation_quality": 4.8
  },
  "behavioral_observations": {
    "attention_to_detail": "Caught 3 subtle IOCs others missed",
    "stress_management": "Calm and methodical under time pressure",
    "communication": "Clear, concise writeup"
  }
}
```

---

## 5. Turnover and Retention Data

### Purpose
Identify personality predictors of attrition

### Data Elements

```json
{
  "person_id": "EMP-SEC-023",
  "hire_date": "2023-05-15",
  "termination_date": "2024-09-30",
  "tenure_months": 16.5,
  "termination_type": "Voluntary (resignation)",
  "exit_reason": "Burnout, seeking less stressful role",
  "personality_profile_at_hire": {
    "neuroticism": 0.72,
    "stress_resilience": 0.48,
    "fit_score": 0.52
  },
  "performance_trajectory": [
    {"period": "2023-H2", "rating": 3.8},
    {"period": "2024-H1", "rating": 3.2},
    {"period": "2024-H2", "rating": 2.9}
  ],
  "exit_interview_notes": "Candidate was high performer initially, but struggled with 24/7 shift stress. Personality assessment showed elevated Neuroticism (0.72), which we should have flagged as risk factor for SOC role.",
  "lessons_learned": "High Neuroticism (>0.6) is strong predictor of SOC burnout. Adjust fit score algorithm to penalize high N more heavily."
}
```

### Retention Analysis

```python
def analyze_turnover_by_personality(employees):
    """
    Identify personality predictors of turnover.
    """
    churned = [e for e in employees if e['termination_date'] is not None and e['tenure_months'] < 24]
    retained = [e for e in employees if e['tenure_months'] > 24]

    # Compare personality profiles
    churned_neuroticism = np.mean([e['personality_profile']['neuroticism'] for e in churned])
    retained_neuroticism = np.mean([e['personality_profile']['neuroticism'] for e in retained])

    print(f"Churned (< 2 years): Avg Neuroticism = {churned_neuroticism:.2f}")
    print(f"Retained (> 2 years): Avg Neuroticism = {retained_neuroticism:.2f}")

    # Expected finding: Churned employees have significantly higher Neuroticism
    if churned_neuroticism > retained_neuroticism + 0.15:
        print("⚠️ High Neuroticism is turnover risk factor")

    return churned_neuroticism, retained_neuroticism
```

---

## 6. Conflict and Interpersonal Data

### Purpose
Validate conflict prediction algorithms with real conflict incidents

### Data Elements

```json
{
  "conflict_id": "CONFLICT-2024-003",
  "date_reported": "2024-08-15",
  "team_id": "TEAM-IR-002",
  "parties_involved": ["EMP-SEC-034", "EMP-SEC-041"],
  "conflict_type": "Interpersonal (communication style clash)",
  "severity": "Moderate (affecting team productivity)",
  "description": "Team member A (high Extraversion) and Team member B (low Extraversion) have ongoing tension. A perceives B as unresponsive and withdrawn. B perceives A as intrusive and domineering.",
  "personality_profiles": {
    "EMP-SEC-034": {
      "extraversion": 0.85,
      "agreeableness": 0.45,
      "dark_triad": {"narcissism": 0.55}
    },
    "EMP-SEC-041": {
      "extraversion": 0.18,
      "agreeableness": 0.68,
      "neuroticism": 0.62
    }
  },
  "predicted_conflict_risk": 0.38,
  "actual_conflict": true,
  "resolution": {
    "method": "Mediation + communication style training",
    "resolved": true,
    "resolution_date": "2024-09-12",
    "outcome": "Both parties completed training, agreed on communication norms. Tension reduced."
  },
  "lessons_learned": "High Extraversion + Low Extraversion combinations require proactive communication norms. Consider this in team composition."
}
```

### Conflict Prediction Validation

```python
def validate_conflict_predictions(conflicts):
    """
    Measure accuracy of conflict risk predictions.
    """
    # True Positives: High predicted risk + actual conflict
    # False Positives: High predicted risk + no conflict
    # True Negatives: Low predicted risk + no conflict
    # False Negatives: Low predicted risk + actual conflict

    tp = sum([1 for c in conflicts if c['predicted_conflict_risk'] > 0.3 and c['actual_conflict']])
    fp = sum([1 for c in conflicts if c['predicted_conflict_risk'] > 0.3 and not c['actual_conflict']])
    tn = sum([1 for c in conflicts if c['predicted_conflict_risk'] <= 0.3 and not c['actual_conflict']])
    fn = sum([1 for c in conflicts if c['predicted_conflict_risk'] <= 0.3 and c['actual_conflict']])

    accuracy = (tp + tn) / (tp + fp + tn + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    print(f"Conflict Prediction Accuracy: {accuracy:.2%}")
    print(f"Precision: {precision:.2%}, Recall: {recall:.2%}")

    # Target: >70% accuracy, >60% precision, >60% recall
    return accuracy, precision, recall
```

---

## 7. Training and Development Data

### Purpose
Track skill development and personality evolution over time

### Data Elements

```json
{
  "person_id": "EMP-SEC-012",
  "training_history": [
    {
      "course_name": "Advanced Threat Hunting",
      "completion_date": "2024-06-15",
      "pre_assessment": {
        "creative_thinking": 0.42,
        "analytical_thinking": 0.85
      },
      "post_assessment": {
        "creative_thinking": 0.58,
        "analytical_thinking": 0.87
      },
      "skill_gain": {
        "creative_thinking": +0.16,
        "analytical_thinking": +0.02
      },
      "notes": "Training successfully increased creative thinking capability. Demonstrates trainability of cognitive styles."
    }
  ],
  "personality_evolution": [
    {"date": "2023-05-01", "neuroticism": 0.35, "stress_resilience": 0.78},
    {"date": "2024-05-01", "neuroticism": 0.32, "stress_resilience": 0.82},
    {"date": "2025-05-01", "neuroticism": 0.28, "stress_resilience": 0.88}
  ],
  "interpretation": "Neuroticism decreased over 2 years (0.35 → 0.28), stress resilience increased (0.78 → 0.88). Suggests experience and training can improve stress management even if Big Five is relatively stable."
}
```

---

## 8. Assessment Administration Procedures

### 8.1 Candidate Assessment Workflow

**Step 1: Consent and Disclosure (Week 0)**
- Inform candidate about assessments
- Obtain written consent
- Explain how results will be used
- Provide opt-out option (if legally required)

**Step 2: Assessment Battery Administration (Week 1)**
- Schedule 2-hour assessment session (can be split into multiple sessions)
- Administer online via secure platform (Qualtrics, SurveyMonkey, dedicated psychometric software)
- Include validity checks (response time, consistency, socially desirable responding)

**Assessment Order:**
1. Big Five (BFI-2): 15 minutes
2. Dark Triad (SD3): 10 minutes
3. Cognitive Styles (CSI): 15 minutes
4. Behavioral Dimensions: 20 minutes
5. Break: 10 minutes
6. Work Sample Exercise: 30 minutes
7. Structured Interview: 45 minutes

**Step 3: Scoring and Profiling (Week 1)**
- Agent 1 processes responses
- Generate 16-dimensional personality vector
- Flagethical concerns (Dark Triad >80th percentile)
- Prepare candidate feedback report

**Step 4: Feedback to Candidate (Week 2)**
- Provide candidate with assessment results
- Explain personality profile in neutral, non-judgmental terms
- Answer questions
- Obtain candidate's consent to share with hiring team

**Step 5: Hiring Team Review (Week 2)**
- Share personality profile with hiring manager only (not full HR records)
- Calculate fit scores
- Integrate with technical assessment results
- Make hiring decision

### 8.2 Employee Reassessment Workflow

**Frequency:** Annually or biannually

**Purpose:**
- Track personality evolution
- Validate initial assessments
- Update team fit calculations
- Identify training needs

**Abbreviated Assessment:**
- Big Five: BFI-2 (15 min)
- Dark Triad: Optional, only if role requires (SD3, 10 min)
- Behavioral: Stress resilience + Attention (10 min)
- Total: 35 minutes

---

## 9. Data Quality Requirements

### 9.1 Assessment Validity Checks

**Response Consistency:**
```python
def check_response_consistency(responses):
    """
    Flag inconsistent responding (e.g., "strongly agree" to opposite-worded items).
    """
    # Identify item pairs with opposite wording
    opposite_pairs = [(3, 15), (7, 22), (11, 28), ...]  # Item indices

    inconsistencies = 0
    for (item_a, item_b) in opposite_pairs:
        if abs(responses[item_a] + responses[item_b] - 6) > 2:  # Should sum to ~6 for 5-point scale
            inconsistencies += 1

    consistency_score = 1 - (inconsistencies / len(opposite_pairs))

    if consistency_score < 0.70:
        print("⚠️ Low response consistency, results may be invalid")

    return consistency_score
```

**Social Desirability:**
```python
def detect_socially_desirable_responding(responses, sd_items):
    """
    Detect tendency to present oneself in overly positive light.
    """
    # SD items are questions designed to detect faking good
    # e.g., "I have never told a lie" (almost no one can honestly say yes)

    sd_score = sum([responses[i] for i in sd_items]) / (len(sd_items) * 5)

    if sd_score > 0.75:
        print("⚠️ High social desirability responding, candidate may be faking good")

    return sd_score
```

**Response Time Validation:**
```python
def validate_response_time(completion_time_seconds, expected_time_seconds):
    """
    Flag suspiciously fast or slow completion.
    """
    ratio = completion_time_seconds / expected_time_seconds

    if ratio < 0.5:
        print("⚠️ Completed too fast, may not have read items carefully")
        return "FAST"
    elif ratio > 2.0:
        print("⚠️ Completed very slowly, possible interruptions or overthinking")
        return "SLOW"
    else:
        return "NORMAL"
```

### 9.2 Data Completeness Requirements

- [ ] >95% of assessment items completed (allow up to 5% missing for technical issues)
- [ ] All validity checks passed (consistency >0.70, SD <0.75, normal response time)
- [ ] Population norms available for percentile conversion
- [ ] Assessment administered in standardized conditions (no interruptions, quiet environment)
- [ ] Ethical consent obtained and documented

---

## 10. Privacy and Ethical Compliance

### 10.1 Data Privacy Requirements

**GDPR Compliance (EU):**
- [ ] Explicit consent obtained before assessment
- [ ] Right to access: Candidates can view their results
- [ ] Right to deletion: Candidates can request data deletion (after hiring decision finalized)
- [ ] Data minimization: Collect only personality data needed for role assessment
- [ ] Retention limits: Delete candidate data 1 year after hiring decision (unless hired)

**ADA Compliance (US):**
- [ ] Assessments are job-related and consistent with business necessity
- [ ] No medical/clinical diagnoses (Big Five and cognitive styles are OK, clinical psychology tests are NOT)
- [ ] Accommodations provided for disabilities (e.g., extra time, screen reader compatibility)

**EEOC Compliance (US):**
- [ ] Regular adverse impact analysis (do personality requirements disproportionately affect protected classes?)
- [ ] No disparate impact: If fit scores differ by race/gender/age, investigate and adjust criteria

### 10.2 Ethical Use Guidelines

**Prohibited Uses:**
- ❌ Using Dark Triad scores to label individuals as "bad" or "unethical"
- ❌ Sharing personality data beyond hiring manager and candidate
- ❌ Using personality as sole criterion (must integrate with technical assessment)
- ❌ Requiring assessment for non-security roles (scope limited to cybersecurity positions)
- ❌ Using clinical personality disorder assessments (MMPI, etc.)

**Permitted Uses:**
- ✅ Assessing role fit for security positions
- ✅ Identifying personality gaps in teams
- ✅ Recommending training based on personality
- ✅ Subclinical Dark Triad assessment for adversarial roles (with oversight)
- ✅ Providing feedback to candidates to support career development

### 10.3 Consent Form Template

```markdown
# Personality Assessment Consent Form

## Purpose
As part of our hiring process for cybersecurity roles, we use personality assessments to evaluate role fit and team dynamics. These assessments are NOT clinical evaluations and do NOT diagnose any psychological conditions.

## Assessments Included
- Big Five Personality (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
- Cognitive Styles (Analytical, Creative, Pragmatic, Relational)
- Behavioral Dimensions (Risk Tolerance, Stress Resilience, Attention to Detail, Autonomy)
- [If applicable] Dark Triad (Machiavellianism, Narcissism, Psychopathy) for adversarial thinking roles

## How Results Are Used
- Personality profile will be used to calculate fit score for specific role and team
- Results will be shared with hiring manager ONLY (not entered into HR permanent records)
- You will receive a copy of your results with interpretation
- Results are ONE factor among many (technical skills, experience, interview performance)

## Your Rights
- **Voluntary Participation:** You may decline to participate (note: some roles require assessment)
- **Access:** You may request a copy of your results at any time
- **Deletion:** You may request deletion of your data after hiring decision is finalized
- **Confidentiality:** Your results will not be shared beyond hiring team without your consent

## Data Retention
- If hired: Assessment data retained for duration of employment + 1 year
- If not hired: Assessment data deleted 1 year after hiring decision
- You may request earlier deletion at any time

## Consent
By signing below, I acknowledge that:
- I have read and understood this consent form
- I voluntarily agree to participate in personality assessments
- I understand how my results will be used
- I understand my rights regarding my assessment data

Signature: _________________________  Date: __________
Printed Name: _______________________
```

---

## Appendix: Assessment Instrument Comparison

| Instrument | Items | Time | Cost | Reliability | Validity | Recommendation |
|------------|-------|------|------|-------------|----------|----------------|
| **Big Five** |
| NEO-PI-R | 240 | 45 min | $50-100 | Excellent (α>0.85) | Excellent | Gold standard, but expensive |
| BFI-2 | 60 | 15 min | Free/$$ | Very Good (α>0.80) | Very Good | **Recommended** (best balance) |
| IPIP-NEO | 120 | 30 min | Free | Good (α>0.75) | Good | Budget option |
| **Dark Triad** |
| SD3 | 27 | 10 min | Free | Good (α>0.70) | Good | **Recommended** |
| Dirty Dozen | 12 | 5 min | Free | Acceptable (α>0.65) | Moderate | Quick screening only |
| **Cognitive Styles** |
| CSI | 38 | 15 min | $25-50 | Very Good (α>0.75) | Good | **Recommended** |
| TSI | 104 | 30 min | $75-100 | Excellent (α>0.80) | Very Good | Comprehensive but expensive |
| **Behavioral** |
| CD-RISC (Resilience) | 25 | 10 min | $40 | Excellent (α>0.89) | Excellent | **Recommended** for stress resilience |
| Risk Propensity | 5 | 3 min | Free | Good (α>0.70) | Good | **Recommended** (quick) |

**Recommended Assessment Battery:**
- Big Five: BFI-2 (15 min, free)
- Dark Triad: SD3 (10 min, free)
- Cognitive Styles: CSI (15 min, $25)
- Behavioral: CD-RISC + Risk Propensity (13 min, $40)
- **Total Time:** ~53 minutes
- **Total Cost:** ~$65 per candidate

---

**End of DATA_SOURCES.md**

*For theoretical foundation, see README.md*
*For implementation details, see TASKMASTER_TEAM_FIT_CALCULUS_v1.0.md*
