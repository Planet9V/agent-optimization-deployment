# NER10 Training Data Specification for Psychohistory
**File:** PSYCHOHISTORY_NER10_TRAINING_SPEC.md
**Created:** 2025-11-19
**Version:** v1.0.0
**Author:** System Architecture Designer
**Purpose:** Named Entity Recognition training data for psychological, organizational, and predictive intelligence entities
**Status:** ACTIVE

## Executive Summary

This specification defines how NER10 (Named Entity Recognition model) learns to extract psychological entities from text - organizational biases, threat actor motivations, symbolic vs real threats, emotional indicators, and predictive patterns. This enables automated extraction of psychohistory factors from threat intelligence reports, incident investigations, and organizational communications.

---

## 1. Psychological Entity Types

### 1.1 Cognitive Bias Entities

**Entity Type**: `COGNITIVE_BIAS`

**Description**: Psychological biases affecting security decision-making

**Subtypes**:
- `NORMALCY_BIAS`: "It won't happen to us"
- `AVAILABILITY_BIAS`: Recent events overweighted
- `CONFIRMATION_BIAS`: Only see supporting evidence
- `AUTHORITY_BIAS`: Defer to authority/vendor claims
- `RECENCY_BIAS`: Recent = more important
- `OPTIMISM_BIAS`: Underestimate risks
- `ANCHORING_BIAS`: First information dominates

**Training Examples**:

```json
{
  "exampleId": "NER10-BIAS-001",
  "text": "The CISO stated 'We've never been breached, so we don't need to prioritize ransomware defenses.'",

  "entities": [
    {
      "text": "CISO",
      "type": "ROLE",
      "start": 4,
      "end": 8
    },
    {
      "text": "We've never been breached",
      "type": "COGNITIVE_BIAS",
      "subtype": "NORMALCY_BIAS",
      "start": 18,
      "end": 43,
      "confidence": 0.92
    },
    {
      "text": "ransomware",
      "type": "THREAT_TYPE",
      "realityLevel": "REAL",  // Actual common threat
      "start": 75,
      "end": 85
    }
  ],

  "psychologicalLabels": {
    "cognitiveBias": "NORMALCY_BIAS",
    "defenseDisplacement": true,  // Ignoring real threat
    "likelyOutcome": "MISSED_REAL_THREAT",
    "riskLevel": 8.7
  },

  "historicalContext": {
    "sectorTrend": "INCREASING_RANSOMWARE_IN_SECTOR",
    "prediction": "ORGANIZATION_VULNERABLE_TO_RANSOMWARE"
  }
}
```

```json
{
  "exampleId": "NER10-BIAS-002",
  "text": "After the SolarWinds breach, the board insisted on nation-state APT defenses despite the organization being a small water utility.",

  "entities": [
    {
      "text": "SolarWinds breach",
      "type": "HISTORICAL_EVENT",
      "start": 10,
      "end": 27
    },
    {
      "text": "nation-state APT",
      "type": "THREAT_PERCEPTION",
      "realityLevel": "IMAGINARY",  // Unlikely for small utility
      "start": 58,
      "end": 74
    },
    {
      "text": "small water utility",
      "type": "ORGANIZATION_CONTEXT",
      "start": 111,
      "end": 130
    }
  ],

  "psychologicalLabels": {
    "cognitiveBias": "AVAILABILITY_BIAS",  // Recent prominent event
    "symbolicVsReal": "SYMBOLIC_FOCUS",  // Prestigious threat vs reality
    "resourceMisallocation": true,
    "missedThreats": ["RANSOMWARE", "INSIDER_THREAT"],
    "likelyOutcome": "INEFFECTIVE_DEFENSE"
  }
}
```

---

### 1.2 Threat Perception Entities

**Entity Type**: `THREAT_PERCEPTION`

**Description**: How organizations perceive threats (may differ from reality)

**Reality Levels**:
- `REAL`: Actual technical threat with evidence
- `IMAGINARY`: Feared/perceived threat (media-driven, FUD)
- `SYMBOLIC`: What organization says vs does

**Training Examples**:

```json
{
  "exampleId": "NER10-THREAT-001",
  "text": "The organization focused on sophisticated zero-day exploits, while unpatched CVEs from 2018 remained on critical systems.",

  "entities": [
    {
      "text": "sophisticated zero-day exploits",
      "type": "THREAT_PERCEPTION",
      "realityLevel": "IMAGINARY",  // Low probability, high fear
      "perceivedRisk": 9.5,
      "actualRisk": 2.8,
      "start": 29,
      "end": 60
    },
    {
      "text": "unpatched CVEs from 2018",
      "type": "THREAT_PERCEPTION",
      "realityLevel": "REAL",  // Known, exploitable
      "perceivedRisk": 4.0,
      "actualRisk": 8.7,
      "start": 68,
      "end": 92
    },
    {
      "text": "critical systems",
      "type": "ASSET_CRITICALITY",
      "criticality": 9.5,
      "start": 103,
      "end": 119
    }
  ],

  "psychologicalLabels": {
    "symbolicVsReal": "IMAGINARY_FOCUS",
    "resourceMisallocation": "SEVERE",
    "realThreatIgnored": true,
    "fearVsRealityGap": 6.7,
    "prediction": "BREACH_VIA_UNPATCHED_CVE"
  }
}
```

---

### 1.3 Organizational Emotion Entities

**Entity Type**: `EMOTION`

**Description**: Emotional states affecting security decisions

**Subtypes**:
- `ANXIETY`: General security anxiety
- `PANIC`: Acute fear response
- `DENIAL`: Threat denial
- `COMPLACENCY`: Overconfidence
- `FRUSTRATION`: Budget/resource frustration

**Training Examples**:

```json
{
  "exampleId": "NER10-EMOTION-001",
  "text": "The CISO expressed deep concern about nation-state threats, despite recent ransomware incidents affecting peer organizations.",

  "entities": [
    {
      "text": "CISO",
      "type": "ROLE",
      "start": 4,
      "end": 8
    },
    {
      "text": "deep concern",
      "type": "EMOTION",
      "subtype": "ANXIETY",
      "intensity": 0.8,
      "start": 19,
      "end": 31
    },
    {
      "text": "nation-state threats",
      "type": "THREAT_PERCEPTION",
      "realityLevel": "IMAGINARY",
      "start": 38,
      "end": 58
    },
    {
      "text": "ransomware incidents",
      "type": "THREAT_PERCEPTION",
      "realityLevel": "REAL",
      "ignored": true,
      "start": 75,
      "end": 95
    }
  ],

  "psychologicalLabels": {
    "emotionalState": "ANXIETY_MISDIRECTED",
    "anxietySource": "MEDIA_HYPE + BOARD_PRESSURE",
    "cognitiveBias": "AVAILABILITY_BIAS",
    "realThreatMissed": true,
    "prediction": "RANSOMWARE_BREACH_LIKELY"
  }
}
```

---

### 1.4 Attacker Motivation Entities

**Entity Type**: `ATTACKER_MOTIVATION`

**Description**: Psychological motivations of threat actors (MICE framework)

**Subtypes**:
- `MONEY`: Financial gain
- `IDEOLOGY`: Political/ideological
- `COMPROMISE`: Coercion/blackmail
- `EGO`: Prestige/recognition

**Training Examples**:

```json
{
  "exampleId": "NER10-MOTIVATION-001",
  "text": "APT29 targeting of water utilities aligns with geopolitical tensions and intelligence gathering objectives, not financial motivation.",

  "entities": [
    {
      "text": "APT29",
      "type": "THREAT_ACTOR",
      "start": 0,
      "end": 5
    },
    {
      "text": "water utilities",
      "type": "TARGET_SECTOR",
      "start": 19,
      "end": 34
    },
    {
      "text": "geopolitical tensions",
      "type": "GEOPOLITICAL_CONTEXT",
      "start": 51,
      "end": 72
    },
    {
      "text": "intelligence gathering",
      "type": "ATTACKER_MOTIVATION",
      "subtype": "IDEOLOGY",  // Geopolitical = ideological
      "confidence": 0.87,
      "start": 77,
      "end": 99
    },
    {
      "text": "not financial",
      "type": "MOTIVATION_EXCLUSION",
      "subtype": "MONEY",
      "start": 113,
      "end": 126
    }
  ],

  "psychologicalLabels": {
    "primaryMotivation": "GEOPOLITICAL_INTELLIGENCE",
    "miceBreakdown": {
      "money": 0.1,
      "ideology": 0.8,
      "compromise": 0.05,
      "ego": 0.05
    },
    "targetingLogic": "STRATEGIC_VALUE",
    "prediction": "LONG_TERM_PERSISTENT_CAMPAIGN"
  }
}
```

---

### 1.5 Organizational Defense Mechanism Entities

**Entity Type**: `DEFENSE_MECHANISM`

**Description**: Psychological defense mechanisms (Lacanian/Freudian)

**Subtypes**:
- `DENIAL`: Refuse to acknowledge threat
- `PROJECTION`: Blame external parties
- `RATIONALIZATION`: Justify inaction
- `SUBLIMATION`: Channel anxiety into less threatening activity

**Training Examples**:

```json
{
  "exampleId": "NER10-DEFENSE-001",
  "text": "The organization stated budget constraints prevented patching, while spending $2M on compliance documentation.",

  "entities": [
    {
      "text": "budget constraints",
      "type": "DEFENSE_MECHANISM",
      "subtype": "RATIONALIZATION",  // Excuse for inaction
      "start": 25,
      "end": 43
    },
    {
      "text": "prevented patching",
      "type": "ACTION_AVOIDANCE",
      "realAction": "TECHNICAL_SECURITY",
      "start": 44,
      "end": 62
    },
    {
      "text": "$2M on compliance documentation",
      "type": "DEFENSE_MECHANISM",
      "subtype": "SUBLIMATION",  // Anxiety channeled into symbolic activity
      "start": 80,
      "end": 111
    }
  ],

  "psychologicalLabels": {
    "defenseMechanism": "RATIONALIZATION + SUBLIMATION",
    "symbolicVsReal": {
      "symbolic": "COMPLIANCE_DOCUMENTATION",  // What they DO
      "real": "PATCHING_NEEDED",  // What's NEEDED
      "gap": 7.3
    },
    "anxietySource": "BREACH_FEAR",
    "symptom": "CHECKBOX_SECURITY",
    "prediction": "BREACH_VIA_UNPATCHED_SYSTEM"
  }
}
```

---

## 2. Organizational Culture Entities

### 2.1 Security Culture Maturity

**Entity Type**: `SECURITY_CULTURE`

**Description**: Organizational security culture indicators

**Maturity Levels**: 0-10 scale

**Training Examples**:

```json
{
  "exampleId": "NER10-CULTURE-001",
  "text": "Employees routinely click phishing links despite annual training. IT complains no one follows security policies.",

  "entities": [
    {
      "text": "routinely click phishing links",
      "type": "SECURITY_CULTURE",
      "indicator": "LOW_AWARENESS",
      "maturityScore": 2.3,
      "start": 10,
      "end": 40
    },
    {
      "text": "despite annual training",
      "type": "SECURITY_PROGRAM",
      "effectiveness": "LOW",
      "start": 41,
      "end": 64
    },
    {
      "text": "no one follows security policies",
      "type": "SECURITY_CULTURE",
      "indicator": "POOR_COMPLIANCE",
      "maturityScore": 1.8,
      "start": 80,
      "end": 112
    }
  ],

  "psychologicalLabels": {
    "culturalProfile": "SECURITY_IMMATURE",
    "dominantBehaviors": ["POLICY_AVOIDANCE", "LOW_AWARENESS"],
    "riskLevel": 8.7,
    "prediction": "HIGH_BREACH_PROBABILITY_VIA_PHISHING"
  }
}
```

---

## 3. Predictive Pattern Entities

### 3.1 Historical Behavioral Patterns

**Entity Type**: `HISTORICAL_PATTERN`

**Description**: Observed organizational behavior patterns

**Training Examples**:

```json
{
  "exampleId": "NER10-PATTERN-001",
  "text": "Water utilities historically patch critical CVEs in 180 days on average, compared to 7 days in financial sector.",

  "entities": [
    {
      "text": "Water utilities",
      "type": "SECTOR",
      "start": 0,
      "end": 15
    },
    {
      "text": "180 days",
      "type": "HISTORICAL_PATTERN",
      "metric": "PATCH_VELOCITY",
      "value": 180,
      "confidence": 0.92,
      "start": 57,
      "end": 65
    },
    {
      "text": "financial sector",
      "type": "SECTOR",
      "comparison": true,
      "start": 96,
      "end": 112
    },
    {
      "text": "7 days",
      "type": "HISTORICAL_PATTERN",
      "metric": "PATCH_VELOCITY",
      "value": 7,
      "start": 89,
      "end": 95
    }
  ],

  "psychologicalLabels": {
    "patternType": "SECTOR_PATCH_BEHAVIOR",
    "rootCauses": ["RISK_AVERSE_CULTURE", "CHANGE_CONTROL_RIGIDITY"],
    "predictiveAccuracy": 0.84,
    "prediction": "WATER_SECTOR_WILL_DELAY_PATCHING",
    "breachProbability": 0.78
  }
}
```

---

### 3.2 Future Threat Predictions

**Entity Type**: `FUTURE_THREAT_PREDICTION`

**Description**: Predicted future security events

**Training Examples**:

```json
{
  "exampleId": "NER10-PREDICTION-001",
  "text": "Based on historical patterns, a critical OpenSSL CVE is predicted for Q1 2026. Water sector organizations are expected to delay patching 180+ days, resulting in breaches.",

  "entities": [
    {
      "text": "critical OpenSSL CVE",
      "type": "FUTURE_THREAT_PREDICTION",
      "predictedDate": "2026-02-15",
      "confidence": 0.73,
      "start": 36,
      "end": 56
    },
    {
      "text": "Q1 2026",
      "type": "TIMEFRAME",
      "start": 74,
      "end": 81
    },
    {
      "text": "Water sector",
      "type": "SECTOR",
      "start": 83,
      "end": 95
    },
    {
      "text": "delay patching 180+ days",
      "type": "BEHAVIORAL_PREDICTION",
      "behavior": "DELAYED_PATCHING",
      "value": 180,
      "confidence": 0.78,
      "start": 123,
      "end": 147
    },
    {
      "text": "resulting in breaches",
      "type": "OUTCOME_PREDICTION",
      "outcome": "BREACH",
      "probability": 0.89,
      "start": 149,
      "end": 170
    }
  ],

  "psychologicalLabels": {
    "predictionType": "PSYCHOHISTORY",
    "basedOnPatterns": ["OPENSSL_CVE_CYCLE", "WATER_SECTOR_BEHAVIOR"],
    "interventionPossible": true,
    "proactiveMitigation": "PATCH_BEFORE_CVE_DISCLOSURE",
    "costAvoidance": 75000000  // $75M
  }
}
```

---

## 4. Complete Training Example - Comprehensive Annotation

### 4.1 Full Incident Report with Psychohistory

```json
{
  "exampleId": "NER10-COMPREHENSIVE-001",
  "text": "Post-incident analysis revealed that the CISO expressed concern about nation-state APTs in board meetings for the past year, while ignoring CISA warnings about ransomware threats. The organization had 47 unpatched critical CVEs on water treatment SCADA systems. When the ransomware attack occurred, the incident response team was surprised despite three prior CISA alerts and a peer organization breach two months earlier. The CISO later stated that budget constraints prevented patching, though $3M was spent on APT detection tools that year.",

  "entities": [
    // Roles
    {
      "text": "CISO",
      "type": "ROLE",
      "start": 41,
      "end": 45
    },

    // Emotions
    {
      "text": "concern",
      "type": "EMOTION",
      "subtype": "ANXIETY",
      "intensity": 0.7,
      "start": 57,
      "end": 64
    },

    // Threat Perceptions (Imaginary)
    {
      "text": "nation-state APTs",
      "type": "THREAT_PERCEPTION",
      "realityLevel": "IMAGINARY",
      "perceivedRisk": 9.5,
      "actualRisk": 3.2,
      "start": 71,
      "end": 88
    },

    // Threat Perceptions (Real, Ignored)
    {
      "text": "ransomware threats",
      "type": "THREAT_PERCEPTION",
      "realityLevel": "REAL",
      "perceivedRisk": 4.0,
      "actualRisk": 8.7,
      "ignored": true,
      "start": 159,
      "end": 177
    },

    // Technical Reality
    {
      "text": "47 unpatched critical CVEs",
      "type": "VULNERABILITY_STATE",
      "severity": "CRITICAL",
      "count": 47,
      "start": 199,
      "end": 225
    },

    // Asset Context
    {
      "text": "water treatment SCADA systems",
      "type": "ASSET",
      "criticality": 9.5,
      "start": 229,
      "end": 258
    },

    // Actual Incident
    {
      "text": "ransomware attack",
      "type": "SECURITY_INCIDENT",
      "incidentType": "RANSOMWARE",
      "start": 270,
      "end": 287
    },

    // Emotional Response
    {
      "text": "surprised",
      "type": "EMOTION",
      "subtype": "SHOCK",
      "start": 331,
      "end": 340
    },

    // Missed Warnings
    {
      "text": "three prior CISA alerts",
      "type": "MISSED_WARNING",
      "count": 3,
      "start": 349,
      "end": 372
    },

    // Defense Mechanisms
    {
      "text": "budget constraints prevented patching",
      "type": "DEFENSE_MECHANISM",
      "subtype": "RATIONALIZATION",
      "start": 443,
      "end": 480
    },

    // Symbolic vs Real (Resource Misallocation)
    {
      "text": "$3M was spent on APT detection tools",
      "type": "RESOURCE_ALLOCATION",
      "amount": 3000000,
      "target": "IMAGINARY_THREAT",
      "realNeed": "PATCHING",
      "start": 489,
      "end": 525
    }
  ],

  "psychologicalLabels": {
    // Primary Bias
    "cognitiveBias": "AVAILABILITY_BIAS + NORMALCY_BIAS",

    // Symbolic vs Real
    "symbolicVsReal": {
      "symbolic": "APT_DEFENSES",  // What they focused on
      "imaginary": "NATION_STATE_APT",  // What they feared
      "real": "RANSOMWARE",  // What actually happened
      "gap": 6.3
    },

    // Defense Mechanisms
    "defenseMechanisms": {
      "denial": ["RANSOMWARE_THREAT"],
      "projection": ["BUDGET_CONSTRAINTS"],
      "sublimation": ["APT_DETECTION_TOOLS"],
      "rationalization": ["BUDGET_EXCUSE"]
    },

    // Organizational Psychology
    "organizationalPsychology": {
      "culturalProfile": "RISK_AVERSE",
      "securityMaturity": 4.2,  // Low despite spending
      "complianceOverEffectiveness": true,
      "symbolicSecurity": true
    },

    // Predictability
    "wasThisPredictable": true,
    "predictionConfidence": 0.89,
    "warningsMissed": 3,
    "peerIncidentsIgnored": 1,

    // Root Causes
    "rootCauses": [
      "NORMALCY_BIAS",  // "Won't happen to us"
      "AVAILABILITY_BIAS",  // Recent APT news overweighted
      "RESOURCE_MISALLOCATION",  // $3M on wrong defenses
      "SYMBOLIC_VS_REAL_GAP",  // Focus on prestigious threats
      "MISSED_WARNINGS"  // Ignored CISA alerts
    ],

    // Outcome
    "actualOutcome": "BREACH_VIA_RANSOMWARE",
    "predictedOutcome": "BREACH_VIA_RANSOMWARE",
    "predictionAccuracy": 1.0,

    // Lessons
    "lessons": [
      "FOCUS_ON_REAL_THREATS_NOT_IMAGINARY",
      "HEED_WARNINGS_FROM_AUTHORITIES",
      "PATCH_MANAGEMENT_CRITICAL",
      "AVOID_SYMBOLIC_SECURITY",
      "RECOGNIZE_COGNITIVE_BIASES"
    ]
  },

  "historicalContext": {
    "sectorTrend": "INCREASING_RANSOMWARE_IN_WATER",
    "peerIncidents": 1,
    "cisaWarnings": 3,
    "timeToBreachAfterWarnings": 90  // days
  },

  "psychohistoryPrediction": {
    "thisBreach": {
      "wasPredictable": true,
      "probability": 0.89,
      "daysInAdvance": 90
    },
    "futureRisk": {
      "organizationLearned": false,  // Rationalization, not learning
      "likelyRepeatBreach": true,
      "probability": 0.78,
      "timeframe": 24  // months
    }
  }
}
```

---

## 5. NER10 Model Training Configuration

### 5.1 Entity Type Hierarchy

```yaml
EntityTypes:
  # Top-level psychological categories
  COGNITIVE_BIAS:
    subtypes: [NORMALCY, AVAILABILITY, CONFIRMATION, AUTHORITY, RECENCY, OPTIMISM, ANCHORING]

  THREAT_PERCEPTION:
    subtypes: [REAL, IMAGINARY, SYMBOLIC]

  EMOTION:
    subtypes: [ANXIETY, PANIC, DENIAL, COMPLACENCY, FRUSTRATION, SHOCK]

  ATTACKER_MOTIVATION:
    subtypes: [MONEY, IDEOLOGY, COMPROMISE, EGO]

  DEFENSE_MECHANISM:
    subtypes: [DENIAL, PROJECTION, RATIONALIZATION, SUBLIMATION]

  SECURITY_CULTURE:
    subtypes: [MATURE, DEVELOPING, IMMATURE]

  HISTORICAL_PATTERN:
    subtypes: [ORGANIZATIONAL_BEHAVIOR, SECTOR_BEHAVIOR, ATTACKER_BEHAVIOR]

  FUTURE_THREAT_PREDICTION:
    subtypes: [TECHNICAL, BEHAVIORAL, GEOPOLITICAL]
```

### 5.2 Training Data Requirements

**Minimum Training Examples per Entity Type**: 500

**Data Sources**:
1. Incident reports (anonymized)
2. Threat intelligence reports
3. Organizational security assessments
4. Post-incident analyses
5. Board meeting transcripts (anonymized)
6. CISO interviews
7. Security awareness surveys
8. Synthetic data (augmented)

**Annotation Quality Standards**:
- Inter-annotator agreement >0.85 (Cohen's kappa)
- Expert validation for psychological labels
- Privacy review for all organizational data
- Bias detection in training data

### 5.3 Model Evaluation Metrics

**Entity Recognition Metrics**:
- Precision: >0.90 for primary entities
- Recall: >0.85 for primary entities
- F1 Score: >0.87 for primary entities

**Psychological Label Accuracy**:
- Bias identification: >0.88 accuracy
- Symbolic vs Real classification: >0.85 accuracy
- Prediction validation: >0.75 accuracy (against outcomes)

---

## 6. Integration with Neo4j Psychohistory Schema

### 6.1 Entity to Node Mapping

```cypher
// After NER10 extracts entities, create Neo4j nodes

// Extract cognitive bias from text
MATCH (text:Document {documentId: "DOC-001"})
WHERE text.content CONTAINS "We've never been breached"

// NER10 identifies: NORMALCY_BIAS
CREATE (bias:CognitiveBias {
  biasId: "BIAS-" + randomUUID(),
  biasType: "NORMALCY_BIAS",
  extractedFrom: "DOC-001",
  textEvidence: "We've never been breached, so we don't need to prioritize ransomware",
  confidence: 0.92,
  detectedBy: "NER10",
  timestamp: datetime()
})

// Link to organization
MATCH (org:Organization {organizationId: "ORG-LADWP"})
MERGE (org)-[:HAS_BIAS {
  detectedDate: datetime(),
  severity: "HIGH",
  impactOnSecurity: "MISSED_REAL_THREATS"
}]->(bias)

// Link to organizational psychology
MATCH (org)-[:HAS_PSYCHOLOGY]->(psych:OrganizationPsychology)
SET psych.dominantBiases = CASE
  WHEN NOT "NORMALCY_BIAS" IN psych.dominantBiases
  THEN psych.dominantBiases + "NORMALCY_BIAS"
  ELSE psych.dominantBiases
END
```

---

## 7. Conclusion

This NER10 training specification enables automated extraction of psychological, organizational, and predictive intelligence from unstructured text. By training the model to recognize cognitive biases, defense mechanisms, symbolic vs real threats, and behavioral patterns, the system can continuously learn from incident reports, threat intelligence, and organizational communications to improve psychohistory predictions.

**Next Steps**:
1. Annotate 10,000+ training examples (500 per entity type)
2. Train initial NER10 model
3. Validate against held-out test set
4. Deploy for automated entity extraction
5. Integrate with Neo4j psychohistory schema
6. Continuous model refinement based on prediction outcomes

---

**Document Status**: ACTIVE - Ready for Implementation
**Next Review**: 2025-12-01
**Maintained By**: NER10 Training Team
