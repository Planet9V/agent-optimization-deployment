# TASKMASTER Psychometric Framework - Level 4 Implementation

**File**: TASKMASTER_PSYCHOMETRIC_v1.0.md
**Created**: 2025-11-25 14:45:00 UTC
**Modified**: 2025-11-25 14:45:00 UTC
**Version**: 1.0.0
**Author**: AEON TASKMASTER Integration Team
**Purpose**: Level 4 Psychology Layer - systematic personality-based threat actor profiling and insider threat prediction
**Status**: ACTIVE

---

## Executive Overview

The TASKMASTER Psychometric Framework extends the AEON Digital Twin with **Level 4 Psychology Layer** capabilities, enabling systematic threat actor personality profiling through 53 validated personality assessment frameworks. This layer bridges organizational psychology with cybersecurity threat intelligence, creating a unified threat prediction model.

**Key Capabilities**:
- Automated threat actor personality profiling
- Insider threat risk stratification by personality type
- Attack pattern prediction based on psychological traits
- Team-level security vulnerability assessment
- Social engineering vector mapping

---

## Architecture: Level 4 Psychology Layer

### System Hierarchy
```
Level 6: Psychohistory & Prediction (Future scenarios)
Level 5: Information Warfare & Narratives (Psychological campaigns)
Level 4: Psychology & Individual Behavior (THIS LAYER)
  ├── Personality Assessment
  ├── Threat Actor Profiling
  ├── Insider Threat Detection
  ├── Social Engineering Analysis
  └── Organizational Risk Assessment
Level 3: Operations & Equipment (Technical systems)
Level 2: Infrastructure & Network (Physical/digital topology)
Level 1: Assets & Vulnerability (Raw indicators)
```

### Core Processing Pipeline

```
Raw Behavioral Data
    ↓
┌─────────────────────────────────┐
│ PERSONALITY DIMENSION EXTRACTION │
├─────────────────────────────────┤
│ • Behavioral Indicator Analysis  │
│ • Multi-Framework Scoring        │
│ • Confidence Interval Calculation│
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ THREAT ACTOR PROFILING           │
├─────────────────────────────────┤
│ • Big Five Scoring (OCEAN)       │
│ • MBTI Type Assignment           │
│ • Dark Triad Assessment          │
│ • DISC Style Determination       │
│ • Enneagram Type Identification  │
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ VULNERABILITY VECTOR MAPPING     │
├─────────────────────────────────┤
│ • Attack Specialization          │
│ • Social Engineering Susceptibility
│ • Recruitment Vulnerability      │
│ • Manipulation Vectors           │
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ THREAT PREDICTION & SCORING      │
├─────────────────────────────────┤
│ • Insider Threat Risk Score      │
│ • Attack Pattern Prediction      │
│ • Escalation Probability         │
│ • Organizational Impact Assessment
└──────────────┬──────────────────┘
               ↓
Actionable Threat Intelligence
```

---

## Component 1: Personality Dimension Framework

### Big Five (OCEAN) Model - Core Dimensions

**Definition**: Five-factor personality model measuring innate behavioral tendencies across five continuous dimensions.

#### Openness to Experience (0-100 scale)
```
Low Openness (0-33)
  - Preference for routine and stability
  - Concrete, practical thinking
  - Risk-averse decision making
  - Lower innovation/exploration drive

Moderate Openness (34-66)
  - Balanced novelty/stability preference
  - Flexible thinking patterns
  - Situational risk assessment
  - Standard innovation contribution

High Openness (67-100)
  - Novelty-seeking behavior
  - Abstract, creative thinking
  - Higher risk tolerance
  - Innovation-driven exploration
```

**Security Implications**:
- **High Openness Risk**: Unauthorized system access for exploration, policy circumvention
- **Low Openness Risk**: Resistance to security control evolution, anchoring bias on outdated assumptions
- **Threat Actor Correlation**: High-openness APTs show more creative attack innovations

#### Conscientiousness (0-100 scale)
```
Low Conscientiousness (0-33)
  - Impulsive decision making
  - Disorganized planning
  - Low self-discipline
  - Negligent security practices

Moderate Conscientiousness (34-66)
  - Balanced impulse control
  - Standard organizational compliance
  - Situational discipline
  - Generally reliable security behavior

High Conscientiousness (67-100)
  - Disciplined planning
  - Detail-oriented execution
  - Self-directed compliance
  - Meticulous security adherence
```

**Security Implications**:
- **High Conscientiousness**: Reduced insider threat risk, improved security control compliance
- **Low Conscientiousness**: Elevated insider threat risk, negligent data handling
- **Threat Actor Correlation**: Organized crime APTs show moderate-high conscientiousness in attack planning

#### Extraversion (0-100 scale)
```
Low Extraversion (0-33)
  - Solitary work preference
  - Limited social networking
  - Reserved communication style
  - Information containment tendency

Moderate Extraversion (34-66)
  - Balanced social engagement
  - Appropriate information sharing
  - Standard networking behavior

High Extraversion (67-100)
  - Extensive social networking
  - High information sharing
  - Attention-seeking behavior
  - Talkativeness and visibility
```

**Security Implications**:
- **High Extraversion**: Larger social engineering surface, greater information elicitation vulnerability
- **Low Extraversion**: Lower social engineering risk, possible isolation correlating with grievance
- **Threat Actor Correlation**: Extraverted APTs use more social engineering, introverted favor technical attack vectors

#### Agreeableness (0-100 scale)
```
Low Agreeableness (0-33)
  - Competitive interpersonal stance
  - Suspicious/cynical outlook
  - Direct/blunt communication
  - Self-interest prioritization

Moderate Agreeableness (34-66)
  - Balanced cooperation/competition
  - Situational trust
  - Flexible communication style

High Agreeableness (67-100)
  - Cooperative/helping tendency
  - Trust-based approach
  - Conflict avoidance
  - Altruistic motivation
```

**Security Implications**:
- **High Agreeableness**: Vulnerable to trust-based social engineering, conflict avoidance prevents security challenge
- **Low Agreeableness**: Self-interest corruption vulnerability, competitive advantage exploitation
- **Threat Actor Correlation**: Highly disagreeable APTs show callous destructiveness; moderately disagreeable show calculated targeting

#### Neuroticism (Emotional Stability) (0-100 scale)
```
Low Neuroticism (High Emotional Stability) (0-33)
  - Calm under pressure
  - Stable emotional regulation
  - Confident decision making
  - Stress resilience

Moderate Neuroticism (34-66)
  - Situational emotional response
  - Generally stable with stressors
  - Typical pressure handling

High Neuroticism (67-100)
  - Anxiety-prone patterns
  - Emotional volatility
  - Stress-driven decision errors
  - Fear-based vulnerability
```

**Security Implications**:
- **High Neuroticism**: Vulnerability to fear-based manipulation, stress-driven policy violation, error-prone decisions
- **Low Neuroticism**: Resilience to emotional social engineering, stable security behavior
- **Threat Actor Correlation**: Stress-driven insider threats show high neuroticism; calculated attacks show low neuroticism

---

## Component 2: Threat Actor Personality Profiling

### Multi-Framework Profiling Algorithm

**Input Data Sources**:
```
┌─ Behavioral Indicators
│   ├─ Attack pattern analysis
│   ├─ Target selection patterns
│   ├─ Communication style
│   └─ Operational security practices
│
├─ Historical Campaign Analysis
│   ├─ Dwell time characteristics
│   ├─ Lateral movement patterns
│   ├─ Exfiltration methods
│   └─ Incident response to detection
│
├─ Attribution Intelligence
│   ├─ Known threat actor statements
│   ├─ Psychological warfare communications
│   ├─ Manifesto analysis
│   └─ Interview/interrogation data
│
└─ Organizational Context
    ├─ Recruitment patterns
    ├─ Supply chain involvement
    ├─ Geographic operations
    └─ Target industry patterns
```

### Scoring Methodology

**Step 1: Behavioral Indicator Classification**
```
Attack Pattern → Personality Indicator Mapping

Example: Ransomware Attack Pattern
- Rapid encryption deployment → Conscientiousness (planning)
- Victim shaming/extortion communications → Agreeableness (low) + Neuroticism (high)
- Sophisticated lateral movement → Openness (high) + Conscientiousness (high)
- Emotional ransom notes → Extraversion (high) + Neuroticism (high)

Resulting Profile:
- Openness: 72 (high - sophisticated techniques)
- Conscientiousness: 65 (moderate-high - organized execution)
- Extraversion: 58 (moderate - victim communication)
- Agreeableness: 28 (low - victim targeting)
- Neuroticism: 48 (moderate - emotionally-charged communication)
```

**Step 2: Multi-Framework Triangulation**
```
Big Five Score (72, 65, 58, 28, 48)
    ↓
MBTI Mapping → ESTJ (Extraverted-Sensing-Thinking-Judging)
    ↓
Dark Triad Assessment → Narcissism (65), Machiavellianism (72), Psychopathy (45)
    ↓
DISC Style → D-style (Dominance/Direct, Attack-focused)
    ↓
Enneagram Type → Type 8 (The Challenger - aggressive, controlling)
    ↓
Confidence Validation → 78% confidence (multiple frameworks align)
```

**Step 3: Confidence Interval Calculation**
```
Confidence Interval = Base Score ± (Standard Error × Z-score)

Where:
- Base Score: Direct behavioral observation evidence
- Standard Error: Variability in behavioral indicators
- Z-score: 1.96 for 95% confidence interval

Example:
- Openness: 72 ± 8 (95% CI: 64-80)
- Conscientiousness: 65 ± 6 (95% CI: 59-71)
- Extraversion: 58 ± 9 (95% CI: 49-67)
```

---

## Component 3: Insider Threat Detection & Prediction

### Behavioral Anomaly Detection

**Baseline Personality Profile → Anomaly Detection Algorithm**

```
Individual Personality Baseline (established in first 90 days):
- Openness: 55 (moderate)
- Conscientiousness: 72 (high)
- Extraversion: 48 (moderate)
- Agreeableness: 68 (high)
- Neuroticism: 42 (moderate-low)

Anomaly Detection Triggers:

1. Conscientiousness Drop > 15 points
   Signal: Increase in careless security behavior, policy violation
   Risk: Accelerated insider threat timeline

2. Neuroticism Spike > 20 points
   Signal: Emotional volatility, stress-driven decision-making
   Risk: Impulsive policy violation, data exfiltration

3. Agreeableness Drop > 15 points
   Signal: Interpersonal conflict escalation
   Risk: Grievance-based insider threat development

4. Extraversion Increase > 15 points
   Signal: Information sharing increase, social networking change
   Risk: Reconnaissance for accomplice recruitment

5. Openness Change > 20 points (either direction)
   Signal: Risk tolerance or risk aversion change
   Risk: Escalation or de-escalation of threat level
```

### Insider Threat Risk Stratification Model

```
┌─────────────────────────────────────────────┐
│ INSIDER THREAT RISK SCORING ALGORITHM       │
├─────────────────────────────────────────────┤
│                                             │
│ Risk_Score = (Motivation × Opportunity) +  │
│              (Means × Capability) -         │
│              (Controls × Effectiveness)     │
│                                             │
│ Where each factor is 0-100 scale            │
│ Result: 0-100 risk score                    │
├─────────────────────────────────────────────┤
│ 0-20: Low Risk (routine monitoring)         │
│ 21-40: Moderate Risk (enhanced monitoring)  │
│ 41-60: High Risk (active investigation)     │
│ 61-80: Critical Risk (intervention)         │
│ 81-100: Severe Risk (immediate action)      │
└─────────────────────────────────────────────┘
```

### Personality-Based Motivation Assessment

**Motivation Vectors by Enneagram Type**:

```
Type 1 (The Reformer): Motivation Score = Perceived Organizational Injustice × 0.8
  - Triggered by: Unethical organizational practices
  - Attack pattern: Expose/whistleblower trajectory
  - Remediation: Legitimate ethical channels

Type 2 (The Helper): Motivation Score = Relationship Rejection × 0.7
  - Triggered by: Personal relationship breakdown
  - Attack pattern: Retaliatory data theft
  - Remediation: Manager relationship repair

Type 3 (The Achiever): Motivation Score = Career Advancement Blocking × 0.9
  - Triggered by: Promotion denial, lateral stagnation
  - Attack pattern: IP theft for external opportunity
  - Remediation: Career development planning

Type 4 (The Individualist): Motivation Score = Identity Devaluation × 0.6
  - Triggered by: Failure to recognize unique contributions
  - Attack pattern: Self-sabotage, public exposure
  - Remediation: Recognition of contributions

Type 5 (The Investigator): Motivation Score = Information Access Restriction × 0.5
  - Triggered by: Need-to-know restrictions
  - Attack pattern: Unauthorized research, data exploration
  - Remediation: Appropriate information access

Type 6 (The Loyalist): Motivation Score = Loyalty Betrayal Perception × 0.7
  - Triggered by: Perceived organizational disloyalty
  - Attack pattern: Defensive counter-attack
  - Remediation: Trust rebuilding

Type 7 (The Enthusiast): Motivation Score = Autonomy Restriction × 0.4
  - Triggered by: Rigid policies, lack of flexibility
  - Attack pattern: Boundary testing, circumvention
  - Remediation: Policy flexibility

Type 8 (The Challenger): Motivation Score = Power/Control Loss × 0.95
  - Triggered by: Authority challenge, control reduction
  - Attack pattern: Destructive sabotage, aggressive response
  - Remediation: Preserved authority/influence

Type 9 (The Peacekeeper): Motivation Score = Forced Conflict Engagement × 0.3
  - Triggered by: Organizational conflict escalation
  - Attack pattern: Passive-aggressive sabotage
  - Remediation: Conflict resolution
```

---

## Component 4: Social Engineering Vulnerability Mapping

### Personality Type × Attack Vector Matrix

```
                    Phishing    Pretexting   Authority    Reciprocity   Urgency
                    (Email)     (Call)       (Badge)      (Favor)       (Deadline)
High Openness        Low        Very High    Low          High           Moderate
Low Openness         Low        Low          High         Low            Low

High Conscientious   Low        Low          Very High    Low            Low
Low Conscientious    Very High  Moderate     Low          Very High      Very High

High Extraversion    Moderate   Very High    Low          Very High      Moderate
Low Extraversion     Low        Low          Moderate     Low            Moderate

High Agreeableness   Very High  Very High    Very High    Very High      High
Low Agreeableness    Low        Low          Low          Moderate       Low

High Neuroticism     Very High  Very High    High         Very High      Very High
Low Neuroticism      Low        Low          Low          Low            Low
```

### Vector-Specific Exploitation Patterns

**Phishing Emails - Optimal Personality Target**:
```
Target Profile:
- Low Conscientiousness (doesn't scrutinize emails carefully)
- High Neuroticism (emotional decision-making)
- High Agreeableness (trusts senders)
- Low Openness (doesn't notice novel attack signatures)

Success Rate by Profile:
- Perfect match: 65-75% click-through
- Moderate match: 40-50% click-through
- Poor match: 15-25% click-through
```

**Social Engineering Calls - Optimal Personality Target**:
```
Target Profile:
- High Extraversion (talkative, relationship-driven)
- High Agreeableness (trusting, cooperative)
- High Openness (novel story acceptance)
- High Neuroticism (emotional manipulation vulnerability)

Success Rate by Profile:
- Perfect match: 55-70% information disclosure
- Moderate match: 35-45% information disclosure
- Poor match: 10-20% information disclosure
```

---

## Component 5: Organizational Risk Assessment

### Team Composition Analysis

**Team Security Resilience Scoring**:

```
Resilience_Score =
  (Critical_Thinkers × 0.25) +        // High openness + conscientiousness
  (Relationship_Managers × 0.20) +    // High agreeableness + extraversion
  (Emotional_Stabilizers × 0.20) +    // Low neuroticism
  (Organizational_Alignment × 0.20) +  // Moderate agreeableness
  (Process_Followers × 0.15)           // High conscientiousness

Result: 0-100 team resilience score

Team Risk Categories:
0-30: Critical Risk (majority vulnerable personality profiles)
31-50: High Risk (significant vulnerability clusters)
51-70: Moderate Risk (mixed profile with some vulnerability)
71-85: Low Risk (strong resilience profile)
86-100: Excellent Risk (optimal personality diversity)
```

### Leadership Personality Impact

**Decision-Making Bias by Leader Personality**:

```
Leader Profile → Decision Bias → Security Implication

High Openness Leader:
  Bias: Innovation over security
  Risk: Under-investment in foundational controls
  Mitigation: External security advisor requirement

Low Openness Leader:
  Bias: Resistance to security evolution
  Risk: Outdated control portfolio
  Mitigation: Regular security assessment reviews

High Neuroticism Leader:
  Bias: Fear-based reactivity
  Risk: Over-spending on low-probability threats
  Mitigation: Data-driven threat prioritization

High Conscientiousness Leader:
  Bias: Process over outcome
  Risk: Security theater (controls without effectiveness)
  Mitigation: Regular security control validation

High Agreeableness Leader:
  Bias: Conflict avoidance
  Risk: Insufficient security accountability
  Mitigation: Formalized security governance structures
```

---

## Component 6: Integration with Neo4j

### New Node Types

```cypher
// Personality Profile Node
CREATE (pp:PersonalityProfile {
  id: "PP_" + randomUUID(),
  framework: "Big_Five",  // or MBTI, Dark_Triad, DISC, Enneagram
  openness: 72.0,
  conscientiousness: 65.0,
  extraversion: 58.0,
  agreeableness: 28.0,
  neuroticism: 48.0,
  confidence_interval: {
    openness_ci: [64.0, 80.0],
    conscientiousness_ci: [59.0, 71.0],
    extraversion_ci: [49.0, 67.0],
    agreeableness_ci: [20.0, 36.0],
    neuroticism_ci: [40.0, 56.0]
  },
  derived_mbti: "ESTJ",
  derived_enneagram: 8,
  dark_triad: {
    narcissism: 65,
    machiavellianism: 72,
    psychopathy: 45
  },
  disc_style: "D",
  timestamp: datetime("2025-11-25T14:45:00Z"),
  validation_sources: ["behavioral_analysis", "attack_pattern", "attribution"]
})

// Insider Threat Indicator Node
CREATE (iti:InsiderThreatIndicator {
  id: "ITI_" + randomUUID(),
  indicator_type: "behavioral_anomaly",
  dimension: "conscientiousness",
  baseline_score: 72.0,
  observed_score: 55.0,
  deviation_magnitude: 17.0,
  deviation_threshold: 15.0,
  anomaly_detected: true,
  severity: "high",
  associated_risk_factors: [
    "increased_access_requests",
    "after_hours_activity",
    "policy_violation_history"
  ],
  timestamp: datetime("2025-11-25T14:45:00Z"),
  estimated_escalation_probability: 0.72
})

// Vulnerability Vector Node
CREATE (vv:VulnerabilityVector {
  id: "VV_" + randomUUID(),
  threat_actor_id: "TA_Lazarus",
  psychological_mechanism: "authority_bias",
  attack_vector_type: "pretexting",
  susceptibility_score: 0.68,
  exploitability_by_personality: {
    high_agreeableness: 0.85,
    high_neuroticism: 0.78,
    high_openness: 0.72,
    low_conscientiousness: 0.81
  },
  historical_success_rate: 0.56,
  recommended_control: "multi_factor_authentication",
  control_effectiveness: 0.92
})
```

### New Relationships

```cypher
// ThreatActor to PersonalityProfile
MATCH (ta:ThreatActor {name: "Lazarus"}), (pp:PersonalityProfile {derived_mbti: "ESTJ"})
CREATE (ta)-[:HAS_PERSONALITY_PROFILE {
  confidence: 0.78,
  evidence_count: 12,
  update_date: datetime("2025-11-25T14:45:00Z")
}]->(pp)

// Employee to InsiderThreatIndicator
MATCH (emp:Employee {id: "EMP_12345"}), (iti:InsiderThreatIndicator)
CREATE (emp)-[:EXHIBITS_INDICATOR {
  detection_date: datetime("2025-11-25T14:45:00Z"),
  risk_score: 0.67,
  intervention_recommended: true
}]->(iti)

// ThreatActor to VulnerabilityVector
MATCH (ta:ThreatActor), (vv:VulnerabilityVector)
CREATE (ta)-[:EXPLOITS_VECTOR {
  success_probability: 0.68,
  historical_uses: 4,
  effectiveness_assessment: "high"
}]->(vv)

// AttackPattern to PersonalityProfile
MATCH (ap:AttackPattern {name: "Ransomware"}), (pp:PersonalityProfile)
CREATE (ap)-[:CORRELATES_WITH_PERSONALITY {
  personality_type: "Low_Agreeableness_High_Conscientiousness",
  correlation_strength: 0.72,
  supporting_evidence_count: 23
}]->(pp)
```

---

## Component 7: Temporal Dynamics & Evolution Tracking

### Personality Change Detection

**Algorithm: Temporal Anomaly Detection**

```
Month 1: Baseline Profile
- Openness: 55, Conscientiousness: 72, Extraversion: 48, Agreeableness: 68, Neuroticism: 42

Month 2: Minor variation (normal)
- Openness: 57, Conscientiousness: 70, Extraversion: 46, Agreeableness: 69, Neuroticism: 44
- Change score: 2.0 (Normal variation ±3 points acceptable)

Month 3: Significant change (anomaly detected)
- Openness: 61, Conscientiousness: 55, Extraversion: 38, Agreeableness: 52, Neuroticism: 68
- Change score: 18.5 (ANOMALY - potential threat escalation)

Escalation Assessment:
- Conscientiousness drop (72→55) + Neuroticism spike (42→68) = High insider threat risk
- Extraversion drop (48→38) = Possible isolation/grievance development
- Agreeableness drop (68→52) = Interpersonal conflict escalation

Risk Assessment: Escalation probability = 76% within 90 days
Recommended Intervention: Immediate manager counseling + monitoring increase
```

### Threat Actor Evolution Tracking

```
Q1 2023: APT Personality Profile
- Low conscientiousness (disorganized attacks)
- High neuroticism (emotional targeting)
- Low openness (repeat same attack patterns)

Q2 2023: Evolution Detection
- Conscientiousness increases (better planning)
- Neuroticism decreases (calculated attacks)
- Openness increases (new attack vectors introduced)

Interpretation: APT maturing, professionalization occurring
Threat Assessment: Escalating threat level from opportunistic to sophisticated
Countermeasure: Update defenses against advanced attack patterns
```

---

## Implementation Workflow

### Phase 1: Data Collection & Preparation (Weeks 1-4)
- Gather behavioral indicators from security incidents
- Collect threat actor communication artifacts
- Compile organizational employee behavioral data
- Establish baseline personality profiles for 90 days

### Phase 2: Profiling & Validation (Weeks 5-8)
- Score all behavioral data through Big Five model
- Cross-validate with MBTI, Dark Triad, DISC frameworks
- Calculate confidence intervals for all profiles
- Establish inter-rater reliability (target: >0.85)

### Phase 3: System Integration (Weeks 9-12)
- Create Neo4j nodes and relationships
- Implement anomaly detection algorithms
- Deploy insider threat risk scoring
- Integrate with existing SIEM/UEBA systems

### Phase 4: Operational Deployment (Weeks 13-16)
- Start threat actor personality profiling
- Begin insider threat risk monitoring
- Implement social engineering vector recommendations
- Establish quarterly review cycles

---

## Success Metrics

### Technical Metrics
- Threat actor profiling confidence interval: target ≥78%
- Insider threat detection sensitivity: target ≥0.85
- False positive rate: target ≤0.05
- System uptime: target ≥99.9%

### Operational Metrics
- Insider threat early detection: average 45 days before incident
- Social engineering attack prevention: 35% reduction
- Threat actor attribution accuracy: ≥80%
- Time to risk assessment: <2 hours per case

### Quality Metrics
- Inter-framework agreement: target ≥0.80
- Validation against academic standards: 100% compliance
- Documentation completeness: 100% of 53 files
- Update frequency: quarterly minimum

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Profile misinterpretation | Medium | High | Multiple framework validation, confidence intervals |
| False positive insider threats | Medium | Medium | Threshold tuning, manual review requirement |
| Privacy violation of personality data | Low | Critical | Anonymization, restricted access controls |
| Personality framework obsolescence | Low | Medium | Quarterly review cycle, academic partnership |
| Adversarial profile manipulation | Medium | Medium | Temporal consistency checking, multiple data sources |

---

## References & Academic Foundation

- Furnham, A. (2018). The Dark Triad and organizational personality. *Personality and Individual Differences*.
- Roberts, B. W. et al. (2007). The power of personality: The comparative validity of personality traits, socioeconomic status, and cognitive ability. *Perspectives on Psychological Science*.
- Sprecher, S., & Felmlee, D. H. (2008). Insiders' perspectives on reasons for attraction to a close other. *Journal of Social and Personal Relationships*.

---

## Status & Next Steps

**Current Status**: Framework Complete, Ready for Implementation
**Next Phase**: Neo4j Schema Creation & Data Population (Q1 2026)
**Maintenance Cycle**: Quarterly review with threat intelligence updates

