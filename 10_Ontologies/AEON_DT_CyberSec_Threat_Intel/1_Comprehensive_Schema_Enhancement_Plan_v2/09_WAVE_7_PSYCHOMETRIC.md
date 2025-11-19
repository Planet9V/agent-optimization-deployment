# Wave 7: Psychometric Analysis and Behavioral Assessment Integration

**File**: 09_WAVE_7_PSYCHOMETRIC.md
**Created**: 2025-10-30
**Version**: v1.0.0
**Status**: ACTIVE
**Wave Duration**: 3 weeks
**Target Node Count**: ~350 nodes
**Dependencies**: Waves 1-6 (ATT&CK, Assets, CVE, ICS, UCO/STIX)

## 1. Wave Overview

### 1.1 Objectives

Wave 7 extends the AEON Digital Twin cybersecurity knowledge graph with psychometric analysis and behavioral assessment capabilities, focusing on understanding the human factors in cyber threats: insider threat psychology, social engineering susceptibility, attacker profiling, and organizational security culture measurement.

**Primary Goals**:
- Model psychological profiles of threat actors (motivations, personality traits, cognitive biases)
- Implement insider threat risk assessment frameworks (CERT Insider Threat indicators)
- Integrate social engineering susceptibility measurements
- Model organizational security culture and awareness metrics
- Connect psychological profiles to attack techniques and tactics
- Enable predictive behavioral risk modeling
- Support security awareness program effectiveness measurement

**Business Value**:
- Proactive insider threat detection based on behavioral indicators
- Targeted security awareness training based on susceptibility profiles
- Improved threat actor attribution through psychological profiling
- Data-driven security culture improvement programs
- Regulatory compliance (NIST SP 800-53 PS controls, ISO 27001 human resources security)
- Reduced human-factor cybersecurity incidents

### 1.2 Scope Definition

**In Scope**:

**Psychological Models**:
- Big Five personality traits (OCEAN model)
- Dark Triad personality traits (Machiavellianism, Narcissism, Psychopathy)
- Cognitive biases relevant to security (confirmation bias, authority bias, urgency bias)
- Motivation frameworks (MICE: Money, Ideology, Compromise, Ego)

**Insider Threat Models**:
- CERT Insider Threat indicators (technical, behavioral, organizational)
- Insider threat typology (malicious insider, negligent insider, compromised insider)
- Risk scoring models (likelihood × impact)

**Social Engineering**:
- Social engineering tactics (pretexting, phishing susceptibility, authority exploitation)
- Susceptibility assessment metrics
- Training effectiveness measurement

**Organizational Factors**:
- Security culture maturity models
- Security awareness assessment
- Organizational risk factors

**Out of Scope**:
- Clinical psychological diagnosis (not cybersecurity-focused)
- Detailed HR performance data (privacy concerns)
- Biometric/physiological data (future consideration)
- Real-time behavioral monitoring systems (ethical boundaries)

### 1.3 Dependencies

**Required Completed Waves**:
- Wave 1: Core MITRE ATT&CK (for technique-to-psychology mapping)
- Wave 2: Asset classification (for asset access risk modeling)
- Wave 6: UCO/STIX (for investigation case integration)

**External Frameworks**:
- CERT Insider Threat Indicators (CMU SEI)
- NIST SP 800-53 Personnel Security Controls
- ISO 27001:2022 Annex A.6 (People controls)
- MITRE ATT&CK Tactics mapped to psychological motivations
- OCEAN Big Five personality model
- Dark Triad personality assessment

**Ethical Considerations**:
- Privacy protection for user behavioral data
- Anonymization of personal identifiers
- Transparent use of psychological profiling
- Compliance with GDPR, CCPA for behavioral data
- Ethical AI/ML model usage for prediction

### 1.4 Success Metrics

**Quantitative Metrics**:
- 5 psychological profile types (Big Five, Dark Triad, etc.)
- 30+ insider threat indicators modeled
- 15+ social engineering tactics with susceptibility metrics
- 10+ security culture assessment dimensions
- 100+ behavioral indicator to ATT&CK technique mappings
- 50+ example psychological profiles created
- Query performance <500ms for behavioral risk scoring

**Qualitative Metrics**:
- Integration with threat actor profiling (Wave 6 STIX Threat Actor)
- Support for insider threat case investigations (Wave 6 UCO)
- Actionable security awareness training recommendations
- Organizational security culture trend analysis capabilities
- Privacy-preserving behavioral analysis

## 2. Complete Node Schemas

### 2.1 Psychological Profile Nodes

#### 2.1.1 Big Five Personality Profile

**Node Label**: `BigFive_Profile`

**Description**: Represents an individual's Big Five (OCEAN) personality traits relevant to cybersecurity risk.

**Properties**:
```cypher
{
  profile_id: String,            // Unique profile identifier (anonymized)
  profile_type: String,          // "BIG_FIVE_PERSONALITY"

  // Big Five dimensions (0.0-1.0 scale, 0.5 = neutral)
  openness: Float,               // Openness to Experience
  conscientiousness: Float,      // Conscientiousness
  extraversion: Float,           // Extraversion
  agreeableness: Float,          // Agreeableness
  neuroticism: Float,            // Neuroticism (Emotional Stability)

  // Cybersecurity risk indicators
  risk_taking_tendency: Float,   // 0.0-1.0 (derived from personality)
  rule_following_tendency: Float, // 0.0-1.0 (conscientiousness-based)
  social_susceptibility: Float,  // 0.0-1.0 (extraversion + agreeableness)
  stress_resilience: Float,      // 0.0-1.0 (neuroticism inverse)

  // Assessment metadata
  assessment_date: DateTime,
  assessment_method: String,     // "IPIP", "NEO-PI-R", "BFI", etc.
  assessment_confidence: Float,  // 0.0-1.0

  // Privacy protection
  is_anonymized: Boolean,        // Always true
  data_retention_expires: DateTime,

  // Context
  organizational_role: String,   // "Executive", "Engineer", "Administrator", etc.
  access_level: String,          // "HIGH", "MEDIUM", "LOW"
  years_in_role: Integer,

  // Metadata
  node_id: String,
  created_date: DateTime,
  last_updated: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create Big Five Personality Profile (anonymized example)
CREATE (p:BigFive_Profile {
  profile_id: "BIGFIVE-" + randomUUID(),
  profile_type: "BIG_FIVE_PERSONALITY",

  // Big Five scores (example: high risk profile)
  openness: 0.75,               // High openness (curious, experimental)
  conscientiousness: 0.30,      // Low conscientiousness (disorganized, impulsive)
  extraversion: 0.65,           // Moderate-high extraversion (social, talkative)
  agreeableness: 0.40,          // Low agreeableness (skeptical, competitive)
  neuroticism: 0.70,            // High neuroticism (emotionally reactive, stressed)

  // Derived cybersecurity risk indicators
  risk_taking_tendency: 0.72,   // High (low conscientiousness + high openness)
  rule_following_tendency: 0.30, // Low (low conscientiousness)
  social_susceptibility: 0.525,  // Moderate (extraversion + agreeableness / 2)
  stress_resilience: 0.30,      // Low (high neuroticism)

  assessment_date: datetime('2024-09-15T00:00:00Z'),
  assessment_method: "IPIP-NEO-120",
  assessment_confidence: 0.85,

  is_anonymized: true,
  data_retention_expires: datetime('2027-09-15T00:00:00Z'),  // 3 years

  organizational_role: "System Administrator",
  access_level: "HIGH",
  years_in_role: 4,

  node_id: randomUUID(),
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on profile ID
CREATE CONSTRAINT bigfive_profile_id_unique IF NOT EXISTS
FOR (p:BigFive_Profile) REQUIRE p.profile_id IS UNIQUE;

// Index on risk indicators for risk scoring
CREATE INDEX bigfive_risk_taking_idx IF NOT EXISTS
FOR (p:BigFive_Profile) ON (p.risk_taking_tendency);

CREATE INDEX bigfive_rule_following_idx IF NOT EXISTS
FOR (p:BigFive_Profile) ON (p.rule_following_tendency);

// Index on organizational role
CREATE INDEX bigfive_role_idx IF NOT EXISTS
FOR (p:BigFive_Profile) ON (p.organizational_role);

// Index on access level
CREATE INDEX bigfive_access_idx IF NOT EXISTS
FOR (p:BigFive_Profile) ON (p.access_level);
```

#### 2.1.2 Dark Triad Personality Profile

**Node Label**: `DarkTriad_Profile`

**Description**: Represents Dark Triad personality traits (Machiavellianism, Narcissism, Psychopathy) associated with malicious insider risk.

**Properties**:
```cypher
{
  profile_id: String,            // Unique profile identifier (anonymized)
  profile_type: String,          // "DARK_TRIAD_PERSONALITY"

  // Dark Triad dimensions (0.0-1.0 scale)
  machiavellianism: Float,       // Manipulative, strategic deception
  narcissism: Float,             // Grandiosity, entitlement, need for admiration
  psychopathy: Float,            // Impulsivity, thrill-seeking, lack of empathy

  // Composite scores
  dark_triad_composite: Float,   // Average of three dimensions
  malicious_insider_risk_score: Float, // 0.0-1.0 risk score

  // Behavioral indicators
  manipulative_tendency: Float,  // 0.0-1.0
  rule_violation_tendency: Float, // 0.0-1.0
  revenge_motivation: Float,     // 0.0-1.0
  entitlement_attitude: Float,   // 0.0-1.0

  // Assessment metadata
  assessment_date: DateTime,
  assessment_method: String,     // "SD3", "Dirty Dozen", etc.
  assessment_confidence: Float,

  // Privacy protection
  is_anonymized: Boolean,
  data_retention_expires: DateTime,

  // Context
  organizational_role: String,
  access_level: String,
  years_in_role: Integer,

  // Risk flags
  requires_monitoring: Boolean,
  requires_intervention: Boolean,

  // Metadata
  node_id: String,
  created_date: DateTime,
  last_updated: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create Dark Triad Profile (high-risk insider profile)
CREATE (dt:DarkTriad_Profile {
  profile_id: "DARKTRIAD-" + randomUUID(),
  profile_type: "DARK_TRIAD_PERSONALITY",

  // Dark Triad scores (elevated risk example)
  machiavellianism: 0.78,        // High manipulative tendency
  narcissism: 0.65,              // Moderate-high narcissism
  psychopathy: 0.55,             // Moderate psychopathy

  dark_triad_composite: 0.66,    // (0.78 + 0.65 + 0.55) / 3
  malicious_insider_risk_score: 0.75, // Elevated risk

  // Behavioral indicators
  manipulative_tendency: 0.78,
  rule_violation_tendency: 0.62,
  revenge_motivation: 0.58,
  entitlement_attitude: 0.70,

  assessment_date: datetime('2024-09-15T00:00:00Z'),
  assessment_method: "Short Dark Triad (SD3)",
  assessment_confidence: 0.80,

  is_anonymized: true,
  data_retention_expires: datetime('2027-09-15T00:00:00Z'),

  organizational_role: "Database Administrator",
  access_level: "HIGH",
  years_in_role: 6,

  requires_monitoring: true,
  requires_intervention: false,  // Monitoring only, no immediate action

  node_id: randomUUID(),
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on profile ID
CREATE CONSTRAINT dark_triad_profile_id_unique IF NOT EXISTS
FOR (dt:DarkTriad_Profile) REQUIRE dt.profile_id IS UNIQUE;

// Index on composite score for risk queries
CREATE INDEX dark_triad_composite_idx IF NOT EXISTS
FOR (dt:DarkTriad_Profile) ON (dt.dark_triad_composite);

// Index on malicious insider risk score
CREATE INDEX dark_triad_risk_score_idx IF NOT EXISTS
FOR (dt:DarkTriad_Profile) ON (dt.malicious_insider_risk_score);

// Index on monitoring flag
CREATE INDEX dark_triad_monitoring_idx IF NOT EXISTS
FOR (dt:DarkTriad_Profile) ON (dt.requires_monitoring);
```

#### 2.1.3 Cognitive Bias Profile

**Node Label**: `CognitiveBias_Profile`

**Description**: Represents susceptibility to cognitive biases that can be exploited in social engineering attacks.

**Properties**:
```cypher
{
  profile_id: String,            // Unique profile identifier
  profile_type: String,          // "COGNITIVE_BIAS_ASSESSMENT"

  // Bias susceptibility scores (0.0-1.0 scale)
  authority_bias: Float,         // Tendency to obey authority figures
  urgency_bias: Float,           // Susceptibility to time pressure tactics
  social_proof_bias: Float,      // Influenced by others' actions
  scarcity_bias: Float,          // Fear of missing out (FOMO)
  confirmation_bias: Float,      // Seeking information that confirms beliefs
  familiarity_bias: Float,       // Trusting familiar sources/brands
  reciprocity_bias: Float,       // Feeling obligated to return favors

  // Composite social engineering susceptibility
  social_engineering_susceptibility: Float, // 0.0-1.0 composite score

  // Phishing susceptibility breakdown
  phishing_susceptibility_email: Float,
  phishing_susceptibility_phone: Float,  // Vishing
  phishing_susceptibility_sms: Float,    // Smishing

  // Assessment metadata
  assessment_date: DateTime,
  assessment_method: String,     // "Simulated Phishing", "Behavioral Survey", etc.
  assessment_confidence: Float,

  // Historical performance
  phishing_simulations_received: Integer,
  phishing_simulations_clicked: Integer,
  phishing_simulations_reported: Integer,
  last_training_date: DateTime,

  // Privacy protection
  is_anonymized: Boolean,
  data_retention_expires: DateTime,

  // Context
  organizational_role: String,
  department: String,

  // Metadata
  node_id: String,
  created_date: DateTime,
  last_updated: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create Cognitive Bias Profile (high susceptibility example)
CREATE (cb:CognitiveBias_Profile {
  profile_id: "COGNITIVEBIAS-" + randomUUID(),
  profile_type: "COGNITIVE_BIAS_ASSESSMENT",

  // Bias susceptibility scores
  authority_bias: 0.82,          // High susceptibility to authority
  urgency_bias: 0.75,            // High susceptibility to urgency
  social_proof_bias: 0.68,       // Moderate-high social influence
  scarcity_bias: 0.60,           // Moderate FOMO susceptibility
  confirmation_bias: 0.55,       // Moderate confirmation bias
  familiarity_bias: 0.70,        // High trust in familiar brands
  reciprocity_bias: 0.65,        // Moderate reciprocity tendency

  // Composite score (weighted average)
  social_engineering_susceptibility: 0.68,

  // Phishing susceptibility
  phishing_susceptibility_email: 0.72,
  phishing_susceptibility_phone: 0.65,
  phishing_susceptibility_sms: 0.58,

  assessment_date: datetime('2024-10-01T00:00:00Z'),
  assessment_method: "Simulated Phishing Campaign + Behavioral Survey",
  assessment_confidence: 0.88,

  // Historical data (12-month period)
  phishing_simulations_received: 24,
  phishing_simulations_clicked: 8,   // 33% click rate (high risk)
  phishing_simulations_reported: 2,  // Low reporting rate
  last_training_date: datetime('2024-03-15T00:00:00Z'),  // 6 months ago

  is_anonymized: true,
  data_retention_expires: datetime('2027-10-01T00:00:00Z'),

  organizational_role: "Finance Manager",
  department: "Finance",

  node_id: randomUUID(),
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on profile ID
CREATE CONSTRAINT cognitive_bias_profile_id_unique IF NOT EXISTS
FOR (cb:CognitiveBias_Profile) REQUIRE cb.profile_id IS UNIQUE;

// Index on social engineering susceptibility
CREATE INDEX cognitive_bias_susceptibility_idx IF NOT EXISTS
FOR (cb:CognitiveBias_Profile) ON (cb.social_engineering_susceptibility);

// Index on phishing susceptibility
CREATE INDEX cognitive_bias_phishing_idx IF NOT EXISTS
FOR (cb:CognitiveBias_Profile) ON (cb.phishing_susceptibility_email);

// Index on department for organizational analysis
CREATE INDEX cognitive_bias_department_idx IF NOT EXISTS
FOR (cb:CognitiveBias_Profile) ON (cb.department);
```

### 2.2 Insider Threat Indicator Nodes

#### 2.2.1 CERT Insider Threat Indicator

**Node Label**: `InsiderThreat_Indicator`

**Description**: Represents specific behavioral, technical, or organizational indicators of insider threat based on CERT framework.

**Properties**:
```cypher
{
  indicator_id: String,          // Unique indicator identifier
  indicator_name: String,        // Indicator name
  indicator_category: String,    // TECHNICAL, BEHAVIORAL, ORGANIZATIONAL

  // Indicator details
  description: String,           // Detailed description
  severity: String,              // LOW, MEDIUM, HIGH, CRITICAL
  indicator_type: String,        // Specific type within category

  // Detection characteristics
  observability: String,         // EASY, MODERATE, DIFFICULT
  detection_methods: [String],   // How to detect this indicator
  data_sources: [String],        // Required data sources

  // Risk assessment
  false_positive_rate: String,   // LOW, MEDIUM, HIGH
  base_risk_score: Float,        // 0.0-1.0 intrinsic risk

  // Mitigation
  mitigation_strategies: [String],
  response_actions: [String],

  // Standards references
  cert_indicator_id: String,     // CERT framework reference
  nist_control_mappings: [String], // NIST SP 800-53 controls

  // Examples
  example_scenarios: [String],

  // Metadata
  node_id: String,
  created_date: DateTime,
  last_updated: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement (Example - Technical Indicator)**:
```cypher
// Create Insider Threat Indicator: Unauthorized Access Attempts
CREATE (iti:InsiderThreat_Indicator {
  indicator_id: "CERT-IT-TECH-001",
  indicator_name: "Repeated Unauthorized Access Attempts",
  indicator_category: "TECHNICAL",

  description: "Employee repeatedly attempts to access systems, files, or data beyond their authorized scope. Includes failed authentication attempts, privilege escalation attempts, and access to restricted resources.",
  severity: "HIGH",
  indicator_type: "Unauthorized Access Pattern",

  observability: "EASY",
  detection_methods: [
    "SIEM correlation rules for failed access attempts",
    "Access control log analysis",
    "Privilege escalation detection",
    "Data Loss Prevention (DLP) alerts"
  ],
  data_sources: [
    "Authentication logs",
    "Authorization logs",
    "File access logs",
    "Network access logs",
    "Database audit logs"
  ],

  false_positive_rate: "MEDIUM",
  base_risk_score: 0.75,

  mitigation_strategies: [
    "Implement least privilege access controls",
    "Real-time alerting for unauthorized access attempts",
    "Automated account lockout after threshold",
    "Regular access review and recertification",
    "User behavior analytics (UBA)"
  ],
  response_actions: [
    "Immediate investigation of access pattern",
    "Interview with employee",
    "Review of business justification for access",
    "Temporary access restriction if warranted",
    "Incident escalation if malicious intent suspected"
  ],

  cert_indicator_id: "CERT-Insider-Tech-Unauthorized-Access",
  nist_control_mappings: ["AC-2", "AC-3", "AC-6", "AU-2", "AU-6"],

  example_scenarios: [
    "Database administrator attempts to access HR salary database without authorization",
    "Developer tries to escalate privileges on production server",
    "Employee accesses competitor customer list outside job duties"
  ],

  node_id: randomUUID(),
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Complete Cypher CREATE Statement (Example - Behavioral Indicator)**:
```cypher
// Create Insider Threat Indicator: Disgruntlement
CREATE (itib:InsiderThreat_Indicator {
  indicator_id: "CERT-IT-BEHAV-001",
  indicator_name: "Employee Disgruntlement and Grievance",
  indicator_category: "BEHAVIORAL",

  description: "Employee exhibits signs of dissatisfaction, resentment, or grievance toward the organization. May include verbal complaints, negative attitude, conflict with management, or expressions of revenge.",
  severity: "MEDIUM",
  indicator_type: "Disgruntlement Pattern",

  observability: "MODERATE",
  detection_methods: [
    "HR grievance reports",
    "Manager behavioral observations",
    "Exit interview data",
    "Performance review comments",
    "Workplace conduct reports",
    "Internal communication monitoring (where legal and ethical)"
  ],
  data_sources: [
    "HR incident reports",
    "Performance management system",
    "Employee surveys",
    "Manager reports",
    "Peer feedback"
  ],

  false_positive_rate: "HIGH",
  base_risk_score: 0.55,

  mitigation_strategies: [
    "Proactive HR engagement and conflict resolution",
    "Employee assistance programs (EAP)",
    "Regular one-on-one manager check-ins",
    "Anonymous feedback channels",
    "Fair and transparent grievance procedures"
  ],
  response_actions: [
    "Confidential HR investigation",
    "Manager coaching and mediation",
    "Temporary increase in access monitoring (proportionate)",
    "Address root cause of grievance if legitimate",
    "Document all interactions"
  ],

  cert_indicator_id: "CERT-Insider-Behavioral-Disgruntlement",
  nist_control_mappings: ["PS-3", "PS-7", "PS-8"],

  example_scenarios: [
    "Employee repeatedly complains about unfair treatment after denied promotion",
    "IT admin makes threats about 'showing them' after negative performance review",
    "Developer expresses bitterness after being passed over for project lead"
  ],

  node_id: randomUUID(),
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Key CERT Insider Threat Indicators (Sample Set - 15 of 30+)**:
```cypher
// Create comprehensive set of insider threat indicators
UNWIND [
  // Technical Indicators
  {id: "CERT-IT-TECH-001", name: "Repeated Unauthorized Access Attempts", category: "TECHNICAL", severity: "HIGH"},
  {id: "CERT-IT-TECH-002", name: "Unusual Data Exfiltration", category: "TECHNICAL", severity: "CRITICAL"},
  {id: "CERT-IT-TECH-003", name: "Excessive Data Download", category: "TECHNICAL", severity: "HIGH"},
  {id: "CERT-IT-TECH-004", name: "Use of Unauthorized Software or Tools", category: "TECHNICAL", severity: "MEDIUM"},
  {id: "CERT-IT-TECH-005", name: "Abnormal Network Activity", category: "TECHNICAL", severity: "MEDIUM"},

  // Behavioral Indicators
  {id: "CERT-IT-BEHAV-001", name: "Employee Disgruntlement and Grievance", category: "BEHAVIORAL", severity: "MEDIUM"},
  {id: "CERT-IT-BEHAV-002", name: "Financial Distress", category: "BEHAVIORAL", severity: "MEDIUM"},
  {id: "CERT-IT-BEHAV-003", name: "Violation of Policies and Procedures", category: "BEHAVIORAL", severity: "MEDIUM"},
  {id: "CERT-IT-BEHAV-004", name: "Unauthorized External Communication", category: "BEHAVIORAL", severity: "HIGH"},
  {id: "CERT-IT-BEHAV-005", name: "Sudden Lifestyle Changes", category: "BEHAVIORAL", severity: "LOW"},

  // Organizational Indicators
  {id: "CERT-IT-ORG-001", name: "Inadequate Access Controls", category: "ORGANIZATIONAL", severity: "HIGH"},
  {id: "CERT-IT-ORG-002", name: "Poor Security Culture", category: "ORGANIZATIONAL", severity: "MEDIUM"},
  {id: "CERT-IT-ORG-003", name: "Lack of Monitoring and Auditing", category: "ORGANIZATIONAL", severity: "HIGH"},
  {id: "CERT-IT-ORG-004", name: "Insufficient Background Checks", category: "ORGANIZATIONAL", severity: "MEDIUM"},
  {id: "CERT-IT-ORG-005", name: "High Employee Turnover", category: "ORGANIZATIONAL", severity: "LOW"}
] AS indicator
CREATE (iti:InsiderThreat_Indicator {
  indicator_id: indicator.id,
  indicator_name: indicator.name,
  indicator_category: indicator.category,
  severity: indicator.severity,
  observability: CASE indicator.category
    WHEN "TECHNICAL" THEN "EASY"
    WHEN "BEHAVIORAL" THEN "MODERATE"
    ELSE "DIFFICULT"
  END,
  false_positive_rate: CASE indicator.category
    WHEN "TECHNICAL" THEN "LOW"
    WHEN "BEHAVIORAL" THEN "HIGH"
    ELSE "MEDIUM"
  END,
  base_risk_score: CASE indicator.severity
    WHEN "CRITICAL" THEN 0.9
    WHEN "HIGH" THEN 0.75
    WHEN "MEDIUM" THEN 0.5
    ELSE 0.25
  END,
  node_id: randomUUID(),
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on indicator ID
CREATE CONSTRAINT insider_threat_indicator_id_unique IF NOT EXISTS
FOR (iti:InsiderThreat_Indicator) REQUIRE iti.indicator_id IS UNIQUE;

// Index on category for filtering
CREATE INDEX insider_threat_category_idx IF NOT EXISTS
FOR (iti:InsiderThreat_Indicator) ON (iti.indicator_category);

// Index on severity
CREATE INDEX insider_threat_severity_idx IF NOT EXISTS
FOR (iti:InsiderThreat_Indicator) ON (iti.severity);

// Index on base risk score
CREATE INDEX insider_threat_risk_score_idx IF NOT EXISTS
FOR (iti:InsiderThreat_Indicator) ON (iti.base_risk_score);

// Full-text search on name and description
CREATE FULLTEXT INDEX insider_threat_fulltext IF NOT EXISTS
FOR (iti:InsiderThreat_Indicator) ON EACH [iti.indicator_name, iti.description];
```

### 2.3 Social Engineering Tactic Nodes

#### 2.3.1 Social Engineering Tactic

**Node Label**: `SocialEngineering_Tactic`

**Description**: Represents specific social engineering tactics used in cyber attacks.

**Properties**:
```cypher
{
  tactic_id: String,             // Unique tactic identifier
  tactic_name: String,           // Tactic name
  tactic_category: String,       // PHISHING, PRETEXTING, BAITING, QUID_PRO_QUO, TAILGATING

  // Tactic details
  description: String,
  attack_vector: String,         // EMAIL, PHONE, IN_PERSON, SMS, SOCIAL_MEDIA
  cognitive_biases_exploited: [String], // Which cognitive biases are leveraged

  // Effectiveness metrics
  success_rate_industry_avg: Float, // 0.0-1.0 (industry benchmark)
  detection_difficulty: String,  // EASY, MODERATE, HARD

  // Target characteristics
  high_risk_roles: [String],     // Roles most susceptible
  high_risk_departments: [String],

  // Mitigation
  training_approaches: [String],
  technical_controls: [String],

  // MITRE ATT&CK mapping
  mitre_technique_ids: [String], // Related ATT&CK techniques

  // Examples
  real_world_examples: [Map],

  // Metadata
  node_id: String,
  created_date: DateTime,
  last_updated: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement (Example - Spear Phishing)**:
```cypher
// Create Social Engineering Tactic: Spear Phishing
CREATE (set:SocialEngineering_Tactic {
  tactic_id: "SE-PHISH-001",
  tactic_name: "Spear Phishing",
  tactic_category: "PHISHING",

  description: "Targeted phishing attack using personalized information to appear legitimate. Attacker researches victim to craft convincing email referencing projects, colleagues, or interests. Often impersonates authority figure or trusted contact.",
  attack_vector: "EMAIL",
  cognitive_biases_exploited: [
    "Authority Bias",
    "Familiarity Bias",
    "Urgency Bias",
    "Social Proof Bias"
  ],

  success_rate_industry_avg: 0.45, // 45% click-through rate for spear phishing
  detection_difficulty: "HARD",

  high_risk_roles: [
    "Executive",
    "Finance Manager",
    "System Administrator",
    "HR Personnel",
    "Legal Counsel"
  ],
  high_risk_departments: [
    "Finance",
    "Executive",
    "Human Resources",
    "IT"
  ],

  training_approaches: [
    "Simulated spear phishing campaigns with personalized scenarios",
    "Email header analysis training",
    "Recognition of pretexting indicators",
    "Verification procedures for unusual requests",
    "Role-specific targeted training"
  ],
  technical_controls: [
    "Advanced email filtering with AI/ML anomaly detection",
    "DMARC/SPF/DKIM email authentication",
    "URL rewriting and sandbox analysis",
    "Banner warnings for external emails",
    "Multi-factor authentication for sensitive actions"
  ],

  mitre_technique_ids: ["T1566.001", "T1598.003"],  // Spearphishing Attachment, Spearphishing Link

  real_world_examples: [
    {
      campaign: "DNC 2016 Breach",
      description: "Russian APT28 used spear phishing targeting DNC officials with spoofed Google security alerts",
      year: 2016
    },
    {
      campaign: "RSA SecurID Breach",
      description: "Spear phishing emails with 'Recruitment Plan' Excel attachment delivered zero-day exploit",
      year: 2011
    }
  ],

  node_id: randomUUID(),
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Key Social Engineering Tactics (Sample Set - 10 of 15)**:
```cypher
// Create common social engineering tactics
UNWIND [
  {id: "SE-PHISH-001", name: "Spear Phishing", category: "PHISHING", vector: "EMAIL", success: 0.45},
  {id: "SE-PHISH-002", name: "Whaling (CEO Fraud)", category: "PHISHING", vector: "EMAIL", success: 0.38},
  {id: "SE-PHISH-003", name: "Smishing", category: "PHISHING", vector: "SMS", success: 0.35},
  {id: "SE-VISH-001", name: "Vishing (Voice Phishing)", category: "PHISHING", vector: "PHONE", success: 0.42},
  {id: "SE-PRET-001", name: "Pretexting", category: "PRETEXTING", vector: "PHONE", success: 0.52},
  {id: "SE-BAIT-001", name: "Baiting (USB Drop)", category: "BAITING", vector: "IN_PERSON", success: 0.48},
  {id: "SE-TAIL-001", name: "Tailgating", category: "TAILGATING", vector: "IN_PERSON", success: 0.60},
  {id: "SE-QUI-001", name: "Quid Pro Quo", category: "QUID_PRO_QUO", vector: "PHONE", success: 0.40},
  {id: "SE-SOCI-001", name: "Social Media Reconnaissance", category: "RECONNAISSANCE", vector: "SOCIAL_MEDIA", success: 0.85},
  {id: "SE-IMP-001", name: "Impersonation Attack", category: "IMPERSONATION", vector: "EMAIL", success: 0.50}
] AS tactic
CREATE (set:SocialEngineering_Tactic {
  tactic_id: tactic.id,
  tactic_name: tactic.name,
  tactic_category: tactic.category,
  attack_vector: tactic.vector,
  success_rate_industry_avg: tactic.success,
  detection_difficulty: CASE
    WHEN tactic.success > 0.5 THEN "HARD"
    WHEN tactic.success > 0.3 THEN "MODERATE"
    ELSE "EASY"
  END,
  node_id: randomUUID(),
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on tactic ID
CREATE CONSTRAINT social_engineering_tactic_id_unique IF NOT EXISTS
FOR (set:SocialEngineering_Tactic) REQUIRE set.tactic_id IS UNIQUE;

// Index on category
CREATE INDEX social_engineering_category_idx IF NOT EXISTS
FOR (set:SocialEngineering_Tactic) ON (set.tactic_category);

// Index on attack vector
CREATE INDEX social_engineering_vector_idx IF NOT EXISTS
FOR (set:SocialEngineering_Tactic) ON (set.attack_vector);

// Full-text search
CREATE FULLTEXT INDEX social_engineering_fulltext IF NOT EXISTS
FOR (set:SocialEngineering_Tactic) ON EACH [set.tactic_name, set.description];
```

### 2.4 Security Culture Assessment Nodes

#### 2.4.1 Organizational Security Culture

**Node Label**: `Security_Culture`

**Description**: Represents organizational security culture maturity and awareness metrics.

**Properties**:
```cypher
{
  assessment_id: String,         // Unique assessment identifier
  organization_unit: String,     // Department or division assessed
  assessment_date: DateTime,

  // Culture maturity dimensions (0.0-1.0 scale)
  security_awareness_level: Float,
  policy_compliance_level: Float,
  incident_reporting_culture: Float,
  security_training_effectiveness: Float,
  leadership_commitment: Float,
  employee_engagement: Float,

  // Composite maturity score
  security_culture_maturity: String, // "INITIAL", "DEVELOPING", "DEFINED", "MANAGED", "OPTIMIZING"
  overall_maturity_score: Float,     // 0.0-1.0

  // Risk indicators
  security_culture_risk_score: Float, // 0.0-1.0 (inverse of maturity)
  high_risk_areas: [String],

  // Assessment details
  assessment_method: String,     // Survey, audit, observation
  sample_size: Integer,
  response_rate: Float,

  // Trends
  previous_assessment_date: DateTime,
  previous_maturity_score: Float,
  trend: String,                 // "IMPROVING", "STABLE", "DECLINING"

  // Recommendations
  improvement_priorities: [String],
  action_plan: [Map],

  // Metadata
  node_id: String,
  created_by: String,
  created_date: DateTime,
  last_updated: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create Security Culture Assessment
CREATE (sc:Security_Culture {
  assessment_id: "SEC-CULTURE-2024-Q3",
  organization_unit: "Engineering Department",
  assessment_date: datetime('2024-09-30T00:00:00Z'),

  // Culture maturity dimensions
  security_awareness_level: 0.68,
  policy_compliance_level: 0.72,
  incident_reporting_culture: 0.55,  // Low - needs improvement
  security_training_effectiveness: 0.65,
  leadership_commitment: 0.78,
  employee_engagement: 0.60,

  // Composite maturity
  security_culture_maturity: "DEVELOPING",  // Level 2 of 5
  overall_maturity_score: 0.66,  // Average of dimensions

  security_culture_risk_score: 0.34,  // 1.0 - maturity_score
  high_risk_areas: [
    "Incident Reporting Culture",
    "Employee Engagement",
    "Security Training Effectiveness"
  ],

  assessment_method: "Anonymous Survey + Policy Audit + Incident Analysis",
  sample_size: 150,
  response_rate: 0.82,  // 82% response rate

  previous_assessment_date: datetime('2024-06-30T00:00:00Z'),
  previous_maturity_score: 0.62,
  trend: "IMPROVING",  // +0.04 improvement

  improvement_priorities: [
    "Implement 'no blame' incident reporting culture campaign",
    "Redesign security training with interactive scenarios",
    "Increase frequency of security awareness communications",
    "Establish security champion program for peer engagement"
  ],
  action_plan: [
    {
      priority: 1,
      action: "Launch incident reporting culture initiative",
      owner: "CISO",
      target_date: datetime('2024-11-01T00:00:00Z'),
      budget: 25000
    },
    {
      priority: 2,
      action: "Develop role-based security training modules",
      owner: "Security Awareness Manager",
      target_date: datetime('2024-12-15T00:00:00Z'),
      budget: 50000
    }
  ],

  node_id: randomUUID(),
  created_by: "Security Culture Assessment Team",
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on assessment ID
CREATE CONSTRAINT security_culture_id_unique IF NOT EXISTS
FOR (sc:Security_Culture) REQUIRE sc.assessment_id IS UNIQUE;

// Index on organization unit
CREATE INDEX security_culture_unit_idx IF NOT EXISTS
FOR (sc:Security_Culture) ON (sc.organization_unit);

// Index on maturity level
CREATE INDEX security_culture_maturity_idx IF NOT EXISTS
FOR (sc:Security_Culture) ON (sc.security_culture_maturity);

// Index on assessment date for time-series analysis
CREATE INDEX security_culture_date_idx IF NOT EXISTS
FOR (sc:Security_Culture) ON (sc.assessment_date);
```

## 3. Complete Relationship Schemas

### 3.1 Psychological Profile to Insider Threat Indicator

**Relationship Type**: `EXHIBITS_INDICATOR`

**Description**: Links psychological profiles to insider threat indicators they exhibit.

**Properties**:
```cypher
{
  relationship_id: String,
  indicator_presence: String,    // "OBSERVED", "SUSPECTED", "ABSENT"
  confidence: Float,             // 0.0-1.0
  observation_date: DateTime,
  severity_context: String,      // Contextual severity assessment
  created_date: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link Dark Triad profile to insider threat indicators
MATCH (dt:DarkTriad_Profile {profile_id: "DARKTRIAD-..."})
MATCH (iti:InsiderThreat_Indicator {indicator_id: "CERT-IT-TECH-001"})  // Unauthorized Access
CREATE (dt)-[r:EXHIBITS_INDICATOR {
  relationship_id: randomUUID(),
  indicator_presence: "OBSERVED",
  confidence: 0.85,
  observation_date: datetime('2024-10-15T00:00:00Z'),
  severity_context: "Multiple unauthorized access attempts to financial databases",
  created_date: datetime()
}]->(iti)
```

### 3.2 Cognitive Bias to Social Engineering Tactic

**Relationship Type**: `SUSCEPTIBLE_TO_TACTIC`

**Description**: Links cognitive bias profiles to social engineering tactics they are vulnerable to.

**Properties**:
```cypher
{
  relationship_id: String,
  susceptibility_score: Float,   // 0.0-1.0
  primary_bias_exploited: String,
  historical_failure_count: Integer, // Number of times fallen for this tactic
  created_date: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link cognitive bias profile to spear phishing susceptibility
MATCH (cb:CognitiveBias_Profile {profile_id: "COGNITIVEBIAS-..."})
MATCH (set:SocialEngineering_Tactic {tactic_id: "SE-PHISH-001"})  // Spear Phishing
CREATE (cb)-[r:SUSCEPTIBLE_TO_TACTIC {
  relationship_id: randomUUID(),
  susceptibility_score: 0.78,
  primary_bias_exploited: "Authority Bias",
  historical_failure_count: 3,  // Clicked on 3 simulated phishing emails
  created_date: datetime()
}]->(set)
```

### 3.3 Psychological Profile to ATT&CK Technique

**Relationship Type**: `PSYCHOLOGICALLY_MOTIVATED_FOR`

**Description**: Links psychological profiles to ATT&CK techniques they are psychologically predisposed to execute.

**Properties**:
```cypher
{
  relationship_id: String,
  motivation_strength: Float,    // 0.0-1.0
  psychological_drivers: [String],
  likelihood_multiplier: Float,  // Risk score multiplier
  created_date: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link Dark Triad profile to Data Exfiltration technique
MATCH (dt:DarkTriad_Profile {profile_id: "DARKTRIAD-..."})
MATCH (tech:Technique {technique_id: "T1048"})  // Exfiltration Over Alternative Protocol
CREATE (dt)-[r:PSYCHOLOGICALLY_MOTIVATED_FOR {
  relationship_id: randomUUID(),
  motivation_strength: 0.82,
  psychological_drivers: [
    "Revenge motivation (disgruntlement)",
    "Financial gain (opportunistic)",
    "Entitlement attitude (deserving)"
  ],
  likelihood_multiplier: 2.5,  // 2.5x higher risk than baseline
  created_date: datetime()
}]->(tech)
```

### 3.4 Security Culture to Insider Threat Indicator

**Relationship Type**: `ORGANIZATIONAL_RISK_FOR`

**Description**: Links organizational security culture assessment to insider threat indicators it creates vulnerability for.

**Properties**:
```cypher
{
  relationship_id: String,
  risk_contribution: Float,      // 0.0-1.0 (how much culture increases risk)
  root_cause_analysis: String,
  created_date: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link poor security culture to lack of monitoring indicator
MATCH (sc:Security_Culture {assessment_id: "SEC-CULTURE-2024-Q3"})
MATCH (iti:InsiderThreat_Indicator {indicator_id: "CERT-IT-ORG-003"})  // Lack of Monitoring
CREATE (sc)-[r:ORGANIZATIONAL_RISK_FOR {
  relationship_id: randomUUID(),
  risk_contribution: 0.65,
  root_cause_analysis: "Low security culture maturity (DEVELOPING level) creates environment where monitoring and auditing are deprioritized, enabling insider threat activity to go undetected",
  created_date: datetime()
}]->(iti)
```

### 3.5 Social Engineering Tactic to ATT&CK Technique

**Relationship Type**: `ENABLES_TECHNIQUE`

**Description**: Links social engineering tactics to ATT&CK techniques they enable.

**Properties**:
```cypher
{
  relationship_id: String,
  enablement_type: String,       // "INITIAL_ACCESS", "CREDENTIAL_THEFT", etc.
  success_probability: Float,    // 0.0-1.0
  created_date: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link spear phishing to credential access technique
MATCH (set:SocialEngineering_Tactic {tactic_id: "SE-PHISH-001"})
MATCH (tech:Technique {technique_id: "T1078"})  // Valid Accounts
CREATE (set)-[r:ENABLES_TECHNIQUE {
  relationship_id: randomUUID(),
  enablement_type: "CREDENTIAL_THEFT",
  success_probability: 0.42,  // 42% of spear phishing leads to credential compromise
  created_date: datetime()
}]->(tech)
```

### 3.6 Psychological Profile to UCO Investigation Case

**Relationship Type**: `SUBJECT_OF_INVESTIGATION`

**Description**: Links psychological profiles to investigation cases (privacy-preserving, anonymized).

**Properties**:
```cypher
{
  relationship_id: String,
  investigation_role: String,    // "SUSPECT", "VICTIM", "WITNESS"
  profile_relevance: String,     // Why profile is relevant
  created_date: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link Dark Triad profile to insider threat investigation
MATCH (dt:DarkTriad_Profile {profile_id: "DARKTRIAD-..."})
MATCH (case:UCO_InvestigationCase {case_id: "CASE-2024-002"})
CREATE (dt)-[r:SUBJECT_OF_INVESTIGATION {
  relationship_id: randomUUID(),
  investigation_role: "SUSPECT",
  profile_relevance: "High malicious insider risk score (0.75) combined with observed unauthorized access indicators led to investigation initiation",
  created_date: datetime()
}]->(case)
```

## 4. Integration Patterns

### 4.1 Risk Scoring: Composite Insider Threat Risk

**Objective**: Calculate comprehensive insider threat risk score combining psychological, behavioral, and technical factors.

**Risk Scoring Query**:
```cypher
// Calculate composite insider threat risk score for individual
MATCH (bigfive:BigFive_Profile {profile_id: "BIGFIVE-..."})
OPTIONAL MATCH (darktriad:DarkTriad_Profile {profile_id: "DARKTRIAD-..."})
WHERE darktriad.profile_id = bigfive.profile_id  // Same individual

OPTIONAL MATCH (bigfive)-[exhibits:EXHIBITS_INDICATOR]->(indicator:InsiderThreat_Indicator)
WHERE exhibits.indicator_presence = "OBSERVED"

OPTIONAL MATCH (bigfive)-[motivated:PSYCHOLOGICALLY_MOTIVATED_FOR]->(tech:Technique)

WITH
  bigfive,
  darktriad,
  // Personality risk contribution (40% weight)
  (COALESCE(bigfive.risk_taking_tendency, 0.5) * 0.15 +
   (1.0 - COALESCE(bigfive.rule_following_tendency, 0.5)) * 0.15 +
   COALESCE(darktriad.malicious_insider_risk_score, 0.0) * 0.10) AS personality_risk,

  // Behavioral indicators (40% weight)
  (count(DISTINCT indicator) * 0.05) AS indicator_count_risk,  // 0.05 per indicator, cap at 0.4
  (avg(COALESCE(exhibits.confidence, 0.5)) * 0.35) AS indicator_confidence_risk,

  // Technical motivation (20% weight)
  (count(DISTINCT motivated) * 0.02) AS motivation_count_risk,  // 0.02 per technique, cap at 0.2

  collect(DISTINCT indicator.indicator_name) AS observed_indicators,
  collect(DISTINCT tech.technique_id) AS motivated_techniques

WITH
  bigfive.profile_id AS profile_id,
  bigfive.organizational_role AS role,
  bigfive.access_level AS access_level,
  personality_risk + indicator_count_risk + indicator_confidence_risk + motivation_count_risk AS composite_risk_score,
  observed_indicators,
  motivated_techniques

RETURN
  profile_id,
  role,
  access_level,
  round(composite_risk_score, 3) AS insider_threat_risk_score,
  CASE
    WHEN composite_risk_score >= 0.75 THEN "CRITICAL"
    WHEN composite_risk_score >= 0.60 THEN "HIGH"
    WHEN composite_risk_score >= 0.40 THEN "MEDIUM"
    ELSE "LOW"
  END AS risk_level,
  observed_indicators,
  motivated_techniques
```

### 4.2 Social Engineering Vulnerability Assessment

**Objective**: Assess organizational vulnerability to specific social engineering tactics.

**Vulnerability Query**:
```cypher
// Assess department vulnerability to spear phishing
MATCH (cb:CognitiveBias_Profile)
WHERE cb.department = "Finance"

MATCH (cb)-[susceptible:SUSCEPTIBLE_TO_TACTIC]->(set:SocialEngineering_Tactic {tactic_id: "SE-PHISH-001"})

WITH
  cb.department AS department,
  count(cb) AS total_employees,
  avg(cb.social_engineering_susceptibility) AS avg_susceptibility,
  avg(cb.phishing_susceptibility_email) AS avg_phishing_susceptibility,
  sum(CASE WHEN cb.phishing_simulations_clicked > 3 THEN 1 ELSE 0 END) AS high_risk_individuals,
  avg(cb.phishing_simulations_clicked * 1.0 / cb.phishing_simulations_received) AS avg_click_rate

RETURN
  department,
  total_employees,
  round(avg_susceptibility, 3) AS department_avg_susceptibility,
  round(avg_phishing_susceptibility, 3) AS phishing_vulnerability,
  high_risk_individuals,
  round(avg_click_rate, 3) AS actual_click_rate,
  CASE
    WHEN avg_susceptibility >= 0.7 THEN "CRITICAL"
    WHEN avg_susceptibility >= 0.55 THEN "HIGH"
    WHEN avg_susceptibility >= 0.40 THEN "MEDIUM"
    ELSE "LOW"
  END AS department_risk_level
```

### 4.3 Security Culture Impact Analysis

**Objective**: Correlate security culture metrics with actual incident rates.

**Culture-Incident Correlation Query**:
```cypher
// Correlate security culture with insider threat incidents
MATCH (sc:Security_Culture {organization_unit: "Engineering Department"})
MATCH (case:UCO_InvestigationCase)
WHERE case.incident_start_time > sc.previous_assessment_date
  AND case.incident_start_time < sc.assessment_date
  AND case.case_classification CONTAINS "Insider"

WITH
  sc.organization_unit AS unit,
  sc.overall_maturity_score AS culture_maturity,
  sc.security_culture_maturity AS maturity_level,
  sc.incident_reporting_culture AS reporting_culture,
  count(case) AS incident_count,
  collect(case.case_name) AS incidents

RETURN
  unit,
  maturity_level,
  round(culture_maturity, 3) AS maturity_score,
  round(reporting_culture, 3) AS reporting_culture_score,
  incident_count,
  incidents,
  CASE
    WHEN incident_count = 0 THEN "Insufficient data (or excellent culture)"
    ELSE round((1.0 - culture_maturity) * incident_count, 2)
  END AS culture_risk_indicator
```

## 5. Validation Criteria

### 5.1 Data Completeness Validation

**Node Count Validation**:
```cypher
// Verify target node counts achieved
MATCH (bf:BigFive_Profile) WITH count(bf) AS bigfive_count
MATCH (dt:DarkTriad_Profile) WITH bigfive_count, count(dt) AS darktriad_count
MATCH (cb:CognitiveBias_Profile) WITH bigfive_count, darktriad_count, count(cb) AS cognitive_count
MATCH (iti:InsiderThreat_Indicator) WITH bigfive_count, darktriad_count, cognitive_count, count(iti) AS indicator_count
MATCH (set:SocialEngineering_Tactic) WITH bigfive_count, darktriad_count, cognitive_count, indicator_count, count(set) AS tactic_count
MATCH (sc:Security_Culture)
RETURN
  bigfive_count AS big_five_profiles,
  darktriad_count AS dark_triad_profiles,
  cognitive_count AS cognitive_bias_profiles,
  indicator_count AS insider_threat_indicators,
  tactic_count AS social_engineering_tactics,
  count(sc) AS security_culture_assessments,
  CASE
    WHEN indicator_count >= 30 AND
         tactic_count >= 15 AND
         bigfive_count >= 10 AND
         darktriad_count >= 10 AND
         cognitive_count >= 10
    THEN "PASS"
    ELSE "FAIL"
  END AS validation_status
```

### 5.2 Privacy and Ethics Validation

**Anonymization Validation**:
```cypher
// Verify all psychological profiles are anonymized
MATCH (profile)
WHERE profile:BigFive_Profile OR profile:DarkTriad_Profile OR profile:CognitiveBias_Profile
AND (profile.is_anonymized IS NULL OR profile.is_anonymized = false)
RETURN count(profile) AS non_anonymized_profiles
// Expected: 0
```

### 5.3 Integration Validation

**Mapping Coverage**:
```cypher
// Verify psychological indicators map to ATT&CK techniques
MATCH (iti:InsiderThreat_Indicator)
WITH count(iti) AS total_indicators
MATCH (iti:InsiderThreat_Indicator)-[:INDICATES_TECHNIQUE]->(tech:Technique)
RETURN
  total_indicators,
  count(DISTINCT iti) AS mapped_indicators,
  (count(DISTINCT iti) * 100.0 / total_indicators) AS mapping_percentage
// Expected: mapping_percentage >= 70%
```

## 6. Example Queries

### 6.1 High-Risk Insider Identification

**Query**: Identify employees with highest insider threat risk scores.

```cypher
// Identify top 10 highest-risk insiders
MATCH (bigfive:BigFive_Profile)
OPTIONAL MATCH (darktriad:DarkTriad_Profile {profile_id: bigfive.profile_id})
OPTIONAL MATCH (bigfive)-[exhibits:EXHIBITS_INDICATOR]->(indicator:InsiderThreat_Indicator)
WHERE exhibits.indicator_presence = "OBSERVED"

WITH
  bigfive,
  darktriad,
  count(DISTINCT indicator) AS indicator_count,
  collect(DISTINCT indicator.indicator_name) AS indicators,
  (COALESCE(bigfive.risk_taking_tendency, 0.5) * 0.15 +
   (1.0 - COALESCE(bigfive.rule_following_tendency, 0.5)) * 0.15 +
   COALESCE(darktriad.malicious_insider_risk_score, 0.0) * 0.10 +
   count(DISTINCT indicator) * 0.05) AS composite_risk

RETURN
  bigfive.profile_id AS profile_id,
  bigfive.organizational_role AS role,
  bigfive.access_level AS access_level,
  round(composite_risk, 3) AS risk_score,
  indicator_count AS observed_indicators_count,
  indicators AS observed_indicators,
  CASE
    WHEN composite_risk >= 0.75 THEN "CRITICAL - Immediate Review Required"
    WHEN composite_risk >= 0.60 THEN "HIGH - Enhanced Monitoring"
    WHEN composite_risk >= 0.40 THEN "MEDIUM - Routine Monitoring"
    ELSE "LOW - Standard Monitoring"
  END AS risk_classification
ORDER BY composite_risk DESC
LIMIT 10
```

### 6.2 Targeted Security Awareness Training Recommendations

**Query**: Generate personalized training recommendations based on psychological profiles.

```cypher
// Generate targeted training recommendations
MATCH (cb:CognitiveBias_Profile {department: "Finance"})
MATCH (cb)-[susceptible:SUSCEPTIBLE_TO_TACTIC]->(set:SocialEngineering_Tactic)
WHERE susceptible.susceptibility_score > 0.6

WITH
  cb.profile_id AS profile_id,
  cb.organizational_role AS role,
  collect({
    tactic: set.tactic_name,
    susceptibility: round(susceptible.susceptibility_score, 2),
    primary_bias: susceptible.primary_bias_exploited,
    training_approach: set.training_approaches[0]
  }) AS high_risk_tactics,
  cb.phishing_simulations_clicked * 1.0 / cb.phishing_simulations_received AS click_rate

RETURN
  profile_id,
  role,
  round(click_rate, 3) AS historical_click_rate,
  high_risk_tactics,
  CASE
    WHEN size(high_risk_tactics) >= 5 THEN "Comprehensive social engineering resilience training"
    WHEN size(high_risk_tactics) >= 3 THEN "Targeted phishing and pretexting training"
    WHEN size(high_risk_tactics) >= 1 THEN "Focused training on identified weaknesses"
    ELSE "Maintenance training - refresher course"
  END AS training_recommendation
ORDER BY size(high_risk_tactics) DESC, click_rate DESC
LIMIT 20
```

### 6.3 Security Culture Trend Analysis

**Query**: Analyze security culture improvement over time.

```cypher
// Security culture trend analysis by department
MATCH (sc:Security_Culture)
WHERE sc.assessment_date >= datetime('2024-01-01T00:00:00Z')
ORDER BY sc.organization_unit, sc.assessment_date ASC

WITH
  sc.organization_unit AS unit,
  collect({
    date: sc.assessment_date,
    maturity: sc.overall_maturity_score,
    maturity_level: sc.security_culture_maturity,
    incident_reporting: sc.incident_reporting_culture,
    training_effectiveness: sc.security_training_effectiveness
  }) AS assessments

WITH
  unit,
  assessments,
  assessments[0] AS first_assessment,
  assessments[size(assessments)-1] AS latest_assessment,
  latest_assessment.maturity - first_assessment.maturity AS maturity_change

RETURN
  unit AS department,
  first_assessment.date AS first_assessment_date,
  first_assessment.maturity_level AS starting_maturity,
  latest_assessment.date AS latest_assessment_date,
  latest_assessment.maturity_level AS current_maturity,
  round(maturity_change, 3) AS maturity_improvement,
  CASE
    WHEN maturity_change > 0.1 THEN "SIGNIFICANT IMPROVEMENT"
    WHEN maturity_change > 0.05 THEN "MODERATE IMPROVEMENT"
    WHEN maturity_change > -0.05 THEN "STABLE"
    WHEN maturity_change > -0.1 THEN "MODERATE DECLINE"
    ELSE "SIGNIFICANT DECLINE"
  END AS trend_assessment,
  latest_assessment.incident_reporting AS current_incident_reporting
ORDER BY maturity_change DESC
```

## 7. Wave 7 Implementation Checklist

### 7.1 Pre-Implementation

- [ ] Complete Waves 1-6 validation
- [ ] Backup Neo4j database
- [ ] Review ethical guidelines for behavioral data
- [ ] Consult legal/HR on privacy requirements
- [ ] Establish anonymization procedures
- [ ] Review CERT Insider Threat framework
- [ ] Review Big Five and Dark Triad assessment tools

### 7.2 Implementation Phase 1: Psychological Profiles (Week 1)

- [ ] Create BigFive_Profile nodes with full properties
- [ ] Create DarkTriad_Profile nodes
- [ ] Create CognitiveBias_Profile nodes
- [ ] Create all indexes and constraints
- [ ] Validate privacy protection (all anonymized)
- [ ] Create 50+ example profiles (anonymized test data)

### 7.3 Implementation Phase 2: Insider Threat & Social Engineering (Week 2)

- [ ] Create InsiderThreat_Indicator nodes (30+ indicators)
- [ ] Create SocialEngineering_Tactic nodes (15+ tactics)
- [ ] Create Security_Culture nodes (10+ assessments)
- [ ] Create all indexes and constraints
- [ ] Validate indicator completeness

### 7.4 Implementation Phase 3: Integration & Validation (Week 3)

- [ ] Create EXHIBITS_INDICATOR relationships (profile → indicator)
- [ ] Create SUSCEPTIBLE_TO_TACTIC relationships (bias → tactic)
- [ ] Create PSYCHOLOGICALLY_MOTIVATED_FOR relationships (profile → ATT&CK)
- [ ] Create ORGANIZATIONAL_RISK_FOR relationships (culture → indicator)
- [ ] Create ENABLES_TECHNIQUE relationships (tactic → ATT&CK)
- [ ] Test all example queries
- [ ] Run privacy validation (100% anonymized)
- [ ] Performance benchmarks (<500ms risk scoring)
- [ ] Generate Wave 7 completion report

## 8. Wave 7 Success Criteria Summary

**Quantitative Targets**:
- ✅ 5 psychological profile types implemented
- ✅ 30+ insider threat indicators modeled
- ✅ 15+ social engineering tactics created
- ✅ 10+ security culture assessments
- ✅ 100+ behavioral indicator to ATT&CK technique mappings
- ✅ 50+ example psychological profiles (anonymized)
- ✅ Query performance <500ms for risk scoring

**Qualitative Targets**:
- ✅ Integration with threat actor profiling (STIX Threat Actor)
- ✅ Support for insider threat investigations (UCO)
- ✅ Actionable security awareness training recommendations
- ✅ Organizational security culture trend analysis
- ✅ 100% privacy-preserving behavioral analysis (all anonymized)
- ✅ Ethical AI/ML model compliance

---

**Wave 7 Status**: Ready for implementation
**Dependencies**: Waves 1-6 completed
**Next Wave**: Wave 8 - IT Infrastructure & Physical Security Integration
**Document Version**: v1.0.0
**Last Updated**: 2025-10-30
