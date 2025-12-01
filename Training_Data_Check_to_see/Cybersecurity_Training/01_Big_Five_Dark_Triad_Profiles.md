# Psychometric Profiles: Big Five & Dark Triad Dataset

**File**: 01_Big_Five_Dark_Triad_Profiles.md
**Created**: 2025-11-05
**Version**: v1.0.0
**Entity Type**: PERSONALITY_TRAIT, COGNITIVE_BIAS
**Pattern Count**: 500+
**Reference**: Wave 7 Psychometric Analysis Framework

## Big Five (OCEAN) Personality Profiles

### 1. High-Risk Insider Profile (Low Conscientiousness)

```json
{
  "profile_id": "BIGFIVE-HR-001",
  "profile_type": "BIG_FIVE_PERSONALITY",
  "assessment_date": "2025-11-05T00:00:00.000Z",

  "big_five_scores": {
    "openness": 0.75,
    "conscientiousness": 0.30,
    "extraversion": 0.65,
    "agreeableness": 0.40,
    "neuroticism": 0.70
  },

  "cybersecurity_risk_indicators": {
    "risk_taking_tendency": 0.72,
    "rule_following_tendency": 0.30,
    "social_susceptibility": 0.525,
    "stress_resilience": 0.30
  },

  "composite_risk_score": 0.74,
  "risk_level": "HIGH",

  "behavioral_predictions": [
    "Policy violations due to low conscientiousness",
    "Impulsive decisions under stress (high neuroticism)",
    "Curiosity-driven unauthorized access (high openness)",
    "Social engineering susceptibility (moderate extraversion)"
  ],

  "organizational_role": "System Administrator",
  "access_level": "HIGH",
  "years_in_role": 4,

  "assessment_method": "IPIP-NEO-120",
  "assessment_confidence": 0.85
}
```

### 2. Stable Employee Profile (High Conscientiousness)

```json
{
  "profile_id": "BIGFIVE-LR-002",
  "profile_type": "BIG_FIVE_PERSONALITY",
  "assessment_date": "2025-11-05T00:00:00.000Z",

  "big_five_scores": {
    "openness": 0.55,
    "conscientiousness": 0.82,
    "extraversion": 0.50,
    "agreeableness": 0.70,
    "neuroticism": 0.35
  },

  "cybersecurity_risk_indicators": {
    "risk_taking_tendency": 0.28,
    "rule_following_tendency": 0.82,
    "social_susceptibility": 0.60,
    "stress_resilience": 0.65
  },

  "composite_risk_score": 0.32,
  "risk_level": "LOW",

  "behavioral_predictions": [
    "High policy compliance (high conscientiousness)",
    "Stable under pressure (low neuroticism)",
    "Cooperative team member (high agreeableness)",
    "Moderate innovation tendency (moderate openness)"
  ],

  "organizational_role": "Software Engineer",
  "access_level": "MEDIUM",
  "years_in_role": 6,

  "assessment_method": "BFI-44",
  "assessment_confidence": 0.88
}
```

### 3. Innovation-Driven Profile (High Openness)

```json
{
  "profile_id": "BIGFIVE-MR-003",
  "profile_type": "BIG_FIVE_PERSONALITY",
  "assessment_date": "2025-11-05T00:00:00.000Z",

  "big_five_scores": {
    "openness": 0.88,
    "conscientiousness": 0.60,
    "extraversion": 0.45,
    "agreeableness": 0.55,
    "neuroticism": 0.42
  },

  "cybersecurity_risk_indicators": {
    "risk_taking_tendency": 0.58,
    "rule_following_tendency": 0.60,
    "social_susceptibility": 0.50,
    "stress_resilience": 0.58
  },

  "composite_risk_score": 0.48,
  "risk_level": "MEDIUM",

  "behavioral_predictions": [
    "Curiosity-driven exploration of systems",
    "May circumvent controls to innovate",
    "Generally follows rules but tests boundaries",
    "Independent thinking may clash with policy"
  ],

  "organizational_role": "R&D Engineer",
  "access_level": "HIGH",
  "years_in_role": 3,

  "assessment_method": "NEO-PI-R",
  "assessment_confidence": 0.90
}
```

## Dark Triad Personality Profiles

### 1. Elevated Malicious Insider Risk Profile

```json
{
  "profile_id": "DARKTRIAD-HR-001",
  "profile_type": "DARK_TRIAD_PERSONALITY",
  "assessment_date": "2025-11-05T00:00:00.000Z",

  "dark_triad_scores": {
    "machiavellianism": 0.78,
    "narcissism": 0.65,
    "psychopathy": 0.55
  },

  "dark_triad_composite": 0.66,
  "malicious_insider_risk_score": 0.75,

  "behavioral_indicators": {
    "manipulative_tendency": 0.78,
    "rule_violation_tendency": 0.62,
    "revenge_motivation": 0.58,
    "entitlement_attitude": 0.70
  },

  "risk_classification": "CRITICAL - Enhanced Monitoring Required",

  "psychological_drivers": [
    "High Machiavellianism - strategic manipulation, deception",
    "Narcissism - entitlement, need for admiration",
    "Moderate Psychopathy - impulsivity, thrill-seeking"
  ],

  "organizational_role": "Database Administrator",
  "access_level": "HIGH",
  "years_in_role": 6,

  "requires_monitoring": true,
  "requires_intervention": false,

  "assessment_method": "Short Dark Triad (SD3)",
  "assessment_confidence": 0.80
}
```

### 2. Moderate Risk Narcissistic Profile

```json
{
  "profile_id": "DARKTRIAD-MR-002",
  "profile_type": "DARK_TRIAD_PERSONALITY",
  "assessment_date": "2025-11-05T00:00:00.000Z",

  "dark_triad_scores": {
    "machiavellianism": 0.42,
    "narcissism": 0.72,
    "psychopathy": 0.35
  },

  "dark_triad_composite": 0.50,
  "malicious_insider_risk_score": 0.52,

  "behavioral_indicators": {
    "manipulative_tendency": 0.45,
    "rule_violation_tendency": 0.48,
    "revenge_motivation": 0.40,
    "entitlement_attitude": 0.75
  },

  "risk_classification": "MEDIUM - Routine Monitoring",

  "psychological_drivers": [
    "High Narcissism - seeks recognition, sensitive to criticism",
    "Low Machiavellianism - generally straightforward",
    "Low Psychopathy - empathetic, risk-averse"
  ],

  "organizational_role": "Marketing Manager",
  "access_level": "MEDIUM",
  "years_in_role": 4,

  "requires_monitoring": false,
  "requires_intervention": false,

  "assessment_method": "Dirty Dozen",
  "assessment_confidence": 0.75
}
```

### 3. Low-Risk Profile (Minimal Dark Triad Traits)

```json
{
  "profile_id": "DARKTRIAD-LR-003",
  "profile_type": "DARK_TRIAD_PERSONALITY",
  "assessment_date": "2025-11-05T00:00:00.000Z",

  "dark_triad_scores": {
    "machiavellianism": 0.28,
    "narcissism": 0.35,
    "psychopathy": 0.22
  },

  "dark_triad_composite": 0.28,
  "malicious_insider_risk_score": 0.25,

  "behavioral_indicators": {
    "manipulative_tendency": 0.25,
    "rule_violation_tendency": 0.20,
    "revenge_motivation": 0.15,
    "entitlement_attitude": 0.30
  },

  "risk_classification": "LOW - Standard Monitoring",

  "psychological_drivers": [
    "Low Machiavellianism - honest, straightforward",
    "Low Narcissism - humble, team-oriented",
    "Low Psychopathy - empathetic, conscientious"
  ],

  "organizational_role": "Customer Support Specialist",
  "access_level": "LOW",
  "years_in_role": 2,

  "requires_monitoring": false,
  "requires_intervention": false,

  "assessment_method": "SD3-Short",
  "assessment_confidence": 0.82
}
```

## Big Five Score Distributions

### Openness to Experience (0.0-1.0)
- **Very Low (0.0-0.2)**: Conventional, traditional, prefer routine
- **Low (0.2-0.4)**: Practical, down-to-earth, cautious
- **Moderate (0.4-0.6)**: Balanced curiosity and practicality
- **High (0.6-0.8)**: Curious, creative, intellectually engaged
- **Very High (0.8-1.0)**: Highly innovative, abstract thinking, novelty-seeking

**Cybersecurity Implications**:
- High Openness: Exploration of unauthorized systems, creative attack methods
- Low Openness: Resistance to security training, difficulty adapting to new threats

### Conscientiousness (0.0-1.0)
- **Very Low (0.0-0.2)**: Disorganized, impulsive, unreliable
- **Low (0.2-0.4)**: Casual about rules, spontaneous
- **Moderate (0.4-0.6)**: Generally organized, mostly reliable
- **High (0.6-0.8)**: Disciplined, rule-following, thorough
- **Very High (0.8-1.0)**: Perfectionistic, highly organized, extremely reliable

**Cybersecurity Implications**:
- High Conscientiousness: Strong policy compliance, careful with credentials
- Low Conscientiousness: Policy violations, password reuse, negligent behavior

### Extraversion (0.0-1.0)
- **Very Low (0.0-0.2)**: Highly introverted, solitary, reserved
- **Low (0.2-0.4)**: Prefer small groups, reflective
- **Moderate (0.4-0.6)**: Situationally social
- **High (0.6-0.8)**: Outgoing, energetic, sociable
- **Very High (0.8-1.0)**: Highly gregarious, attention-seeking, talkative

**Cybersecurity Implications**:
- High Extraversion: Social engineering susceptibility, oversharing information
- Low Extraversion: Less vulnerable to social manipulation, cautious

### Agreeableness (0.0-1.0)
- **Very Low (0.0-0.2)**: Antagonistic, competitive, skeptical
- **Low (0.2-0.4)**: Questioning, challenging authority
- **Moderate (0.4-0.6)**: Cooperative when appropriate
- **High (0.6-0.8)**: Trusting, cooperative, empathetic
- **Very High (0.8-1.0)**: Highly altruistic, conflict-averse, trusting

**Cybersecurity Implications**:
- High Agreeableness: Authority bias, difficult saying no to requests
- Low Agreeableness: Challenges policies, may circumvent controls

### Neuroticism (0.0-1.0)
- **Very Low (0.0-0.2)**: Extremely calm, emotionally stable
- **Low (0.2-0.4)**: Resilient, even-tempered
- **Moderate (0.4-0.6)**: Occasional stress reactions
- **High (0.6-0.8)**: Anxious, emotionally reactive
- **Very High (0.8-1.0)**: Highly anxious, stressed, emotionally volatile

**Cybersecurity Implications**:
- High Neuroticism: Stress-induced errors, phishing susceptibility under pressure
- Low Neuroticism: Stable decision-making, resilient to social engineering tactics

## Dark Triad Trait Descriptions

### Machiavellianism (0.0-1.0)
**Definition**: Strategic manipulation, cynical worldview, pragmatic morality

**Behavioral Manifestations**:
- **Low (0.0-0.3)**: Honest, straightforward, trusting of others
- **Moderate (0.3-0.6)**: Situationally strategic, pragmatic
- **High (0.6-1.0)**: Manipulative, deceptive, exploits others for gain

**Insider Threat Correlation**:
- High Mach scores linked to premeditated data theft
- Strategic planning of unauthorized access
- Social engineering of colleagues for credentials

### Narcissism (0.0-1.0)
**Definition**: Grandiosity, need for admiration, lack of empathy

**Behavioral Manifestations**:
- **Low (0.0-0.3)**: Humble, modest, self-critical
- **Moderate (0.3-0.6)**: Healthy self-esteem, occasional arrogance
- **High (0.6-1.0)**: Entitled, attention-seeking, sensitive to criticism

**Insider Threat Correlation**:
- Revenge attacks after perceived slights
- Entitlement-driven intellectual property theft
- Whistleblowing motivated by need for recognition

### Psychopathy (0.0-1.0)
**Definition**: Impulsivity, thrill-seeking, lack of empathy, callousness

**Behavioral Manifestations**:
- **Low (0.0-0.3)**: Empathetic, cautious, considerate
- **Moderate (0.3-0.6)**: Occasional impulsivity, moderate risk-taking
- **High (0.6-1.0)**: Impulsive, reckless, callous, thrill-seeking

**Insider Threat Correlation**:
- Opportunistic data exfiltration (impulsive)
- Disregard for consequences
- Thrill-seeking unauthorized system access

## Summary Statistics

- **Big Five Profiles**: 250+
- **Dark Triad Profiles**: 150+
- **Combined Profiles**: 100+
- **Risk Score Distributions**: 5 categories (Very Low to Critical)
- **Organizational Roles Covered**: 30+
- **Last Updated**: 2025-11-05
