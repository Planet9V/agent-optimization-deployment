# TRAINING_DATA_NER11_SPECIFICATION.md

**File:** TRAINING_DATA_NER11_SPECIFICATION.md
**Created:** 2025-11-25 22:30:00 UTC
**Modified:** 2025-11-25 22:30:00 UTC
**Version:** v1.0.0
**Author:** WAVE 4 Training Data Architecture
**Purpose:** Comprehensive NER11 entity and relationship specification with 18 core entities and 24 relationship types
**Status:** ACTIVE

---

## Executive Summary

NER11 (Named Entity Recognition - Generation 11) extends NER10 psychological intelligence with 18 primary entity types organized across 6 domains, connected through 24 relationship types. This specification defines the complete entity schema, relationship semantics, and training data requirements for extracting complex organizational, psychological, and threat intelligence patterns from cybersecurity documentation.

---

## 1. ENTITY DOMAIN ARCHITECTURE

### 1.1 Domain Overview

```
NER11 Entities (18 Total)
├─ PSYCHOLOGICAL ENTITIES (4)
│  ├─ COGNITIVE_BIAS
│  ├─ THREAT_PERCEPTION
│  ├─ DECISION_PATTERN
│  └─ ORGANIZATIONAL_STRESS
├─ ORGANIZATIONAL ENTITIES (4)
│  ├─ ORGANIZATION
│  ├─ ROLE
│  ├─ PROCESS
│  └─ CAPABILITY_GAP
├─ THREAT ENTITIES (4)
│  ├─ THREAT_ACTOR
│  ├─ ATTACK_VECTOR
│  ├─ VULNERABILITY
│  └─ IMPACT_TYPE
├─ INTELLIGENCE ENTITIES (3)
│  ├─ INDICATOR_OF_COMPROMISE
│  ├─ TACTICAL_PATTERN
│  └─ STRATEGIC_OBJECTIVE
├─ TEMPORAL ENTITIES (2)
│  ├─ HISTORICAL_EVENT
│  └─ PREDICTION_OUTCOME
└─ CONTEXTUAL ENTITIES (1)
   └─ EXTERNAL_FACTOR
```

---

## 2. PSYCHOLOGICAL ENTITIES (Domain 1)

### 2.1 COGNITIVE_BIAS

**Definition**: Systematic patterns in human judgment and decision-making that deviate from rational analysis.

**Subtypes** (10 primary):
- `NORMALCY_BIAS`: Assumption that conditions remain stable
- `AVAILABILITY_BIAS`: Recent/memorable events overweighted
- `CONFIRMATION_BIAS`: Seeking only supporting evidence
- `AUTHORITY_BIAS`: Deferring to authority figures
- `RECENCY_BIAS`: Recent events seem more important
- `OPTIMISM_BIAS`: Underestimating negative outcomes
- `ANCHORING_BIAS`: First information dominates judgment
- `HINDSIGHT_BIAS`: Believing past outcomes were predictable
- `GROUPTHINK_BIAS`: Conformity within team/organization
- `SUNK_COST_BIAS`: Continuing due to past investment

**Attributes**:
- `intensity` (0-10): Strength of bias influence
- `decision_domain`: Type of decision affected
- `awareness_level`: Does decision-maker recognize bias?
- `consequence_severity` (LOW|MEDIUM|HIGH|CRITICAL)

**Training Examples** (Min 50 per subtype):

```json
{
  "id": "NER11-BIAS-001",
  "text": "The security team dismissed cloud adoption risks, stating 'We've always been on-premises and haven't had major incidents.'",
  "entities": [
    {
      "text": "always been on-premises",
      "type": "COGNITIVE_BIAS",
      "subtype": "NORMALCY_BIAS",
      "intensity": 7,
      "start": 50,
      "end": 72,
      "confidence": 0.94
    }
  ]
}
```

### 2.2 THREAT_PERCEPTION

**Definition**: How organizations perceive threats vs. statistical/empirical threat reality.

**Subtypes** (6):
- `PERCEIVED_REAL`: Threat perceived as real, actually is real
- `PERCEIVED_IMAGINARY`: Threat perceived as real, actually rare/impossible
- `UNPERCEIVED_REAL`: Threat not perceived, actually is real threat
- `UNPERCEIVED_IMAGINARY`: Threat not perceived, correctly ignored
- `SEVERITY_OVERESTIMATED`: Real threat, severity over-assessed
- `SEVERITY_UNDERESTIMATED`: Real threat, severity under-assessed

**Attributes**:
- `threat_name`: What is being perceived
- `perception_source`: Media, vendor, internal analysis, etc.
- `organizational_context`: Sector, size, maturity level
- `alignment_to_reality` (0-100): % match with actual threat landscape

**Example**:
```json
{
  "id": "NER11-THREAT-PERC-001",
  "text": "After the SolarWinds breach, this small municipality spent $2M on nation-state APT defenses despite being low-value target.",
  "entities": [
    {
      "text": "nation-state APT defenses",
      "type": "THREAT_PERCEPTION",
      "subtype": "PERCEIVED_IMAGINARY",
      "organizational_context": "municipal_government",
      "alignment_to_reality": 15,
      "start": 70,
      "end": 95
    }
  ]
}
```

### 2.3 DECISION_PATTERN

**Definition**: Recurring patterns in how organizations make security decisions.

**Subtypes** (8):
- `REACTIVE_DECISION`: Response to incident or external pressure
- `PREVENTIVE_DECISION`: Proactive risk mitigation
- `COMPLIANCE_DRIVEN`: Motivated by regulatory requirement
- `VENDOR_INFLUENCED`: Shaped by vendor/consultant recommendations
- `COST_CONSTRAINED`: Limited by budget constraints
- `OPPORTUNITY_DRIVEN`: Motivated by capability expansion
- `CONSENSUS_BASED`: Result of organizational agreement
- `AUTHORITY_IMPOSED`: Imposed by senior leadership

**Attributes**:
- `decision_quality` (EXCELLENT|GOOD|ACCEPTABLE|POOR|HARMFUL)
- `decision_speed` (RUSHED|NORMAL|DELIBERATE|DELAYED)
- `stakeholder_involvement` (LOW|MEDIUM|HIGH)

### 2.4 ORGANIZATIONAL_STRESS

**Definition**: Indicators of organizational pressure, resource constraints, or operational strain affecting security posture.

**Subtypes** (6):
- `RESOURCE_STRAIN`: Insufficient personnel, budget, or tools
- `LEADERSHIP_CONFLICT`: Disagreement among decision-makers
- `SKILL_SHORTAGE`: Lack of technical expertise
- `PROCESS_BREAKDOWN`: Failure of established procedures
- `EXTERNAL_PRESSURE`: Regulatory, market, or competitive pressure
- `MORALE_DECLINE`: Team frustration or burnout

**Attributes**:
- `impact_on_security` (POSITIVE|NEUTRAL|NEGATIVE|CRITICAL)
- `duration` (ACUTE|CHRONIC)
- `visibility` (HIDDEN|ACKNOWLEDGED|PUBLIC)

---

## 3. ORGANIZATIONAL ENTITIES (Domain 2)

### 3.1 ORGANIZATION

**Definition**: Business entities responsible for security decisions and operations.

**Subtypes** (7):
- `PRIVATE_SECTOR`: Commercial business
- `GOVERNMENT_SECTOR`: Federal, state, local government
- `CRITICAL_INFRASTRUCTURE`: Energy, water, transportation, communications
- `HEALTHCARE`: Medical and pharmaceutical organizations
- `FINANCIAL_SERVICES`: Banks, insurance, investment firms
- `EDUCATION`: Universities and educational institutions
- `NGO`: Non-profit and mission-driven organizations

**Attributes**:
- `size` (ENTERPRISE|LARGE|MEDIUM|SMALL|MICRO)
- `maturity_level` (NASCENT|DEVELOPING|MATURE|ADVANCED)
- `compliance_framework` (NIST|ISO|SOC2|HIPAA|PCI|etc.)
- `financial_health` (STRONG|STABLE|STRESSED|CRITICAL)

**Example**:
```json
{
  "id": "NER11-ORG-001",
  "text": "Atlantic Electric, a regional power utility with 2,500 employees, operates generation and distribution across three states.",
  "entities": [
    {
      "text": "Atlantic Electric",
      "type": "ORGANIZATION",
      "subtype": "CRITICAL_INFRASTRUCTURE",
      "size": "LARGE",
      "maturity_level": "MATURE",
      "start": 0,
      "end": 15
    }
  ]
}
```

### 3.2 ROLE

**Definition**: Organizational positions and functions involved in security.

**Subtypes** (12):
- `CISO`: Chief Information Security Officer
- `CIO`: Chief Information Officer
- `CEO`: Chief Executive Officer
- `CFO`: Chief Financial Officer
- `SECURITY_ENGINEER`: Technical security specialist
- `SOC_ANALYST`: Security Operations Center analyst
- `SECURITY_ARCHITECT`: Security system design lead
- `COMPLIANCE_OFFICER`: Regulatory compliance responsibility
- `RISK_MANAGER`: Enterprise risk management
- `BOARD_MEMBER`: Governance board position
- `DEVELOPER`: Software development role
- `SYSTEM_ADMINISTRATOR`: IT operations and systems

**Attributes**:
- `influence_level` (LOW|MEDIUM|HIGH|CRITICAL)
- `technical_depth` (NONE|BASIC|INTERMEDIATE|EXPERT)
- `decision_authority` (NONE|ADVISORY|DECISION|APPROVAL)

### 3.3 PROCESS

**Definition**: Organizational procedures and operational workflows.

**Subtypes** (8):
- `INCIDENT_RESPONSE`: Breach detection and response procedures
- `VULNERABILITY_MANAGEMENT`: Scanning and patching processes
- `ACCESS_CONTROL`: Authentication and authorization workflows
- `CHANGE_MANAGEMENT`: System modification approval procedures
- `VENDOR_MANAGEMENT`: Third-party risk assessment
- `SECURITY_AWARENESS`: Training and education programs
- `AUDIT_COMPLIANCE`: Internal and external compliance checking
- `THREAT_INTELLIGENCE`: Threat monitoring and analysis

**Attributes**:
- `implementation_status` (PLANNED|PARTIAL|IMPLEMENTED|OPTIMIZED)
- `effectiveness` (0-100): Process effectiveness score
- `automation_level` (MANUAL|SEMI_AUTOMATED|FULLY_AUTOMATED)

### 3.4 CAPABILITY_GAP

**Definition**: Missing or deficient organizational capabilities affecting security.

**Subtypes** (9):
- `TECHNICAL_GAP`: Missing technology or technical capability
- `SKILLS_GAP`: Insufficient expertise or training
- `PROCESS_GAP`: Missing or broken procedure
- `VISIBILITY_GAP`: Lack of monitoring or awareness
- `COORDINATION_GAP`: Poor communication between teams
- `GOVERNANCE_GAP`: Lack of oversight or policy
- `VENDOR_GAP`: Inadequate third-party management
- `FUNDING_GAP`: Insufficient budget allocation
- `CULTURAL_GAP`: Organizational culture not supporting security

**Attributes**:
- `severity` (LOW|MEDIUM|HIGH|CRITICAL)
- `exploitability` (LOW|MEDIUM|HIGH): Can adversary exploit this gap?
- `remediation_cost` (LOW|MEDIUM|HIGH)
- `remediation_timeline` (MONTHS|QUARTERS|YEARS)

---

## 4. THREAT ENTITIES (Domain 3)

### 4.1 THREAT_ACTOR

**Definition**: Entities initiating or conducting attacks.

**Subtypes** (7):
- `NATION_STATE`: Government-sponsored APT groups
- `CYBERCRIMINAL`: Financially motivated threat actors
- `HACKTIVIST`: Ideologically motivated attackers
- `INSIDER_THREAT`: Malicious internal actors
- `COMPETITOR`: Business competitor conducting espionage
- `OPPORTUNIST`: Low-skill attackers of convenience
- `UNKNOWN`: Unattributed threat actors

**Attributes**:
- `sophistication` (LOW|MEDIUM|HIGH|VERY_HIGH)
- `target_preference` (SECTOR|FUNCTION|GEOGRAPHY|OPPORTUNISTIC)
- `motivation_primary` (FINANCIAL|POLITICAL|ESPIONAGE|DISRUPTION|IDEOLOGICAL)

### 4.2 ATTACK_VECTOR

**Definition**: Methods and pathways used to compromise systems.

**Subtypes** (12):
- `PHISHING`: Social engineering via email or messaging
- `CREDENTIAL_COMPROMISE`: Username/password theft or weakness
- `ZERO_DAY`: Unknown vulnerability exploitation
- `KNOWN_VULNERABILITY`: Exploiting disclosed CVE
- `SUPPLY_CHAIN`: Attack through vendor/third-party
- `INSIDER_PRIVILEGE`: Abusing legitimate access
- `NETWORK_LATERAL_MOVEMENT`: Horizontal network propagation
- `MALWARE_DELIVERY`: Trojan, worm, or virus infection
- `PHYSICAL_ACCESS`: On-site unauthorized access
- `CLOUD_MISCONFIGURATION`: Public cloud security error
- `API_EXPLOITATION`: Application interface compromise
- `WIRELESS_ATTACK`: Wifi or RF-based attack

**Attributes**:
- `prevention_difficulty` (EASY|MODERATE|DIFFICULT|VERY_DIFFICULT)
- `detection_difficulty` (EASY|MODERATE|DIFFICULT|VERY_DIFFICULT)
- `avg_time_to_exploit` (MINUTES|HOURS|DAYS|WEEKS)

### 4.3 VULNERABILITY

**Definition**: System weaknesses exploitable by threat actors.

**Subtypes** (6):
- `TECHNICAL_VULNERABILITY`: Code or configuration flaw
- `PROCESS_VULNERABILITY`: Procedure or workflow weakness
- `PEOPLE_VULNERABILITY`: Human/social engineering susceptibility
- `GOVERNANCE_VULNERABILITY`: Missing policy or oversight
- `THIRD_PARTY_VULNERABILITY`: Vendor or supply chain weakness
- `ARCHITECTURE_VULNERABILITY`: System design flaw

**Attributes**:
- `cve_id`: Associated CVE identifier if applicable
- `exploitability` (PROOF_OF_CONCEPT|HIGH|MEDIUM|LOW)
- `impact_severity` (CRITICAL|HIGH|MEDIUM|LOW)
- `patch_available` (TRUE|FALSE)
- `time_in_wild` (DAYS|WEEKS|MONTHS|YEARS)

### 4.4 IMPACT_TYPE

**Definition**: Consequences of security incidents.

**Subtypes** (8):
- `DATA_BREACH`: Unauthorized disclosure of sensitive data
- `SERVICE_DISRUPTION`: Availability/downtime impact
- `SYSTEM_COMPROMISE`: Unauthorized access to systems
- `FINANCIAL_LOSS`: Direct or indirect monetary damage
- `REPUTATIONAL_DAMAGE`: Brand and trust impact
- `REGULATORY_VIOLATION`: Compliance violation and penalties
- `OPERATIONAL_FAILURE`: Business process failure
- `SAFETY_IMPACT`: Risk to physical safety or life

**Attributes**:
- `affected_records` (COUNT): Number of individuals impacted
- `financial_impact_usd` (AMOUNT): Quantified financial loss
- `duration` (HOURS|DAYS|WEEKS|MONTHS): Incident duration
- `containment_speed` (MINUTES|HOURS|DAYS|WEEKS): Time to contain

---

## 5. INTELLIGENCE ENTITIES (Domain 4)

### 5.1 INDICATOR_OF_COMPROMISE (IOC)

**Definition**: Technical artifacts indicating system compromise.

**Subtypes** (6):
- `FILE_HASH`: MD5, SHA1, SHA256 of malicious file
- `IP_ADDRESS`: Attacker command & control infrastructure
- `DOMAIN_NAME`: Malicious domain infrastructure
- `EMAIL_ADDRESS`: Phishing or attacker communication
- `URL_PATH`: Malicious URL structure
- `REGISTRY_KEY`: Windows registry modification indicator

**Attributes**:
- `confidence` (LOW|MEDIUM|HIGH): Confidence in indicator validity
- `source`: Where indicator was obtained
- `first_observed`: When indicator first appeared
- `last_observed`: When indicator last seen

### 5.2 TACTICAL_PATTERN

**Definition**: MITRE ATT&CK framework tactical techniques observed.

**Subtypes** (13 - mapped to MITRE):
- `RECONNAISSANCE`: Information gathering
- `RESOURCE_DEVELOPMENT`: Tool and infrastructure setup
- `INITIAL_ACCESS`: Entry point establishment
- `EXECUTION`: Code execution techniques
- `PERSISTENCE`: Maintaining access mechanisms
- `PRIVILEGE_ESCALATION`: Rights elevation
- `DEFENSE_EVASION`: Avoiding detection
- `CREDENTIAL_ACCESS`: Stealing credentials
- `DISCOVERY`: Internal network reconnaissance
- `LATERAL_MOVEMENT`: Network propagation
- `COLLECTION`: Data gathering
- `COMMAND_AND_CONTROL`: Communication with attacker
- `EXFILTRATION`: Data extraction

**Attributes**:
- `technique_id`: MITRE ATT&CK technique identifier
- `frequency`: How often observed
- `sophistication_requirement` (LOW|MEDIUM|HIGH)

### 5.3 STRATEGIC_OBJECTIVE

**Definition**: Attacker's strategic intent or ultimate goal.

**Subtypes** (6):
- `FINANCIAL_THEFT`: Direct monetary extraction
- `INTELLECTUAL_PROPERTY`: Technology/knowledge theft
- `GEOPOLITICAL`: State-level political objectives
- `COMPETITIVE_ADVANTAGE`: Business intelligence gathering
- `DISRUPTION`: Operational or societal disruption
- `RESEARCH`: Data collection for research purposes

**Attributes**:
- `target_specificity` (INDISCRIMINATE|SECTOR|ORGANIZATION|INDIVIDUAL)
- `likelihood` (LOW|MEDIUM|HIGH): Probability goal is achievable
- `impact_if_achieved` (LOW|MEDIUM|HIGH|CRITICAL): Consequence if successful

---

## 6. TEMPORAL ENTITIES (Domain 5)

### 6.1 HISTORICAL_EVENT

**Definition**: Past security incidents, breaches, or regulatory events affecting threat landscape.

**Subtypes** (5):
- `MAJOR_BREACH`: High-profile security incident
- `REGULATORY_CHANGE`: Policy or compliance change
- `TECHNOLOGY_SHIFT`: Significant tech adoption/deprecation
- `MARKET_DISRUPTION`: Industry-wide change event
- `ATTACK_CAMPAIGN`: Sustained attacker operation

**Attributes**:
- `event_date`: When event occurred
- `affected_organizations`: Count or list of affected parties
- `industry_impact_score` (0-100): Wider impact assessment
- `lessons_learned`: Key takeaways from event

**Example**:
```json
{
  "id": "NER11-EVENT-001",
  "text": "The 2020 SolarWinds supply chain compromise affected 18,000+ organizations including government agencies.",
  "entities": [
    {
      "text": "2020 SolarWinds supply chain compromise",
      "type": "HISTORICAL_EVENT",
      "subtype": "MAJOR_BREACH",
      "event_date": "2020-12-08",
      "affected_organizations": 18000,
      "industry_impact_score": 95,
      "start": 4,
      "end": 42
    }
  ]
}
```

### 6.2 PREDICTION_OUTCOME

**Definition**: Forecasted or predicted consequences of identified risks.

**Subtypes** (4):
- `LIKELY_OUTCOME`: High probability consequence
- `POSSIBLE_OUTCOME`: Moderate probability consequence
- `WORST_CASE_SCENARIO`: Low probability but critical impact
- `BEST_CASE_SCENARIO`: Successful mitigation or prevention

**Attributes**:
- `probability` (0-100): Likelihood percentage
- `timeframe` (IMMEDIATE|SHORT_TERM|MEDIUM_TERM|LONG_TERM)
- `severity` (LOW|MEDIUM|HIGH|CRITICAL)
- `mitigation_difficulty` (EASY|MODERATE|DIFFICULT|VERY_DIFFICULT)

---

## 7. CONTEXTUAL ENTITIES (Domain 6)

### 7.1 EXTERNAL_FACTOR

**Definition**: External conditions or events affecting organizational security.

**Subtypes** (6):
- `REGULATORY_REQUIREMENT`: Compliance mandate
- `MARKET_CONDITION`: Competitive or economic factor
- `TECHNOLOGY_TREND`: Emerging technology adoption
- `GEOPOLITICAL_SITUATION`: Political or international context
- `PANDEMIC_CONDITION`: Public health emergency
- `NATURAL_DISASTER`: Environmental disruption event

**Attributes**:
- `influence_direction` (POSITIVE|NEGATIVE|NEUTRAL)
- `controllability` (CONTROLLABLE|PARTIALLY_CONTROLLABLE|UNCONTROLLABLE)
- `urgency` (LOW|MEDIUM|HIGH|CRITICAL)

---

## 8. RELATIONSHIP TYPES (24 Total)

### 8.1 Psychological Relationships (4)

| Relationship | Domain A | Domain B | Semantics | Example |
|--------------|----------|----------|-----------|---------|
| `INFLUENCES` | COGNITIVE_BIAS | DECISION_PATTERN | Bias shapes decision approach | Normalcy bias → reactive decisions |
| `MANIFESTS_AS` | ORGANIZATIONAL_STRESS | COGNITIVE_BIAS | Stress causes biased thinking | Leadership conflict → groupthink |
| `CREATES` | COGNITIVE_BIAS | THREAT_PERCEPTION | Bias distorts threat assessment | Anchoring → perceived threat |
| `CAUSES_NEGLECT` | COGNITIVE_BIAS | CAPABILITY_GAP | Bias prevents gap recognition | Optimism bias → ignoring skills gap |

### 8.2 Organizational Relationships (5)

| Relationship | Domain A | Domain B | Semantics | Example |
|--------------|----------|----------|-----------|---------|
| `RESPONSIBLE_FOR` | ROLE | PROCESS | Role owns/executes process | CISO responsible for incident response |
| `MANAGES` | ORGANIZATION | PROCESS | Organization implements process | Utility operates access control |
| `PERFORMS` | ROLE | DECISION_PATTERN | Role exhibits decision pattern | Security engineer makes reactive decisions |
| `ADDRESSES` | PROCESS | CAPABILITY_GAP | Process mitigates gap | Patch process reduces tech gap |
| `REVEALS` | PROCESS | VULNERABILITY | Process identifies weakness | Audit reveals governance gap |

### 8.3 Threat Relationships (6)

| Relationship | Domain A | Domain B | Semantics | Example |
|--------------|----------|----------|-----------|---------|
| `EXPLOITS` | THREAT_ACTOR | VULNERABILITY | Actor leverages weakness | Cybercriminal exploits phishing susceptibility |
| `EMPLOYS` | THREAT_ACTOR | ATTACK_VECTOR | Actor uses technique | Nation-state uses zero-day |
| `MANIFESTS` | ATTACK_VECTOR | TACTICAL_PATTERN | Vector corresponds to MITRE | Phishing relates to initial access |
| `CAUSES` | VULNERABILITY | IMPACT_TYPE | Vulnerability leads to impact | Unpatched server → data breach |
| `TARGETS` | THREAT_ACTOR | ORGANIZATION | Actor focuses on org type | Ransomware targets hospitals |
| `FOLLOWS_PATTERN` | THREAT_ACTOR | STRATEGIC_OBJECTIVE | Actor pursues goal type | State actor seeks IP theft |

### 8.4 Intelligence Relationships (4)

| Relationship | Domain A | Domain B | Semantics | Example |
|--------------|----------|----------|-----------|---------|
| `INDICATES_COMPROMISE` | INDICATOR_OF_COMPROMISE | ATTACK_VECTOR | IOC evidences technique | IP address indicates C2 connection |
| `EXHIBITS` | THREAT_ACTOR | TACTICAL_PATTERN | Actor demonstrates technique | APT28 uses lateral movement |
| `CORRELATES_WITH` | INDICATOR_OF_COMPROMISE | THREAT_ACTOR | IOC associated with actor | Hash appears in gang toolkit |
| `SUPPORTS_OBJECTIVE` | TACTICAL_PATTERN | STRATEGIC_OBJECTIVE | Technique advances goal | Data exfiltration supports IP theft |

### 8.5 Temporal Relationships (3)

| Relationship | Domain A | Domain B | Semantics | Example |
|--------------|----------|----------|-----------|---------|
| `INSPIRED` | HISTORICAL_EVENT | THREAT_PERCEPTION | Past event shapes threat view | SolarWinds → APT concerns |
| `PREDICTS` | THREAT_PERCEPTION | PREDICTION_OUTCOME | Perception infers consequence | Unperceived threat → breach prediction |
| `VALIDATES` | HISTORICAL_EVENT | PREDICTION_OUTCOME | Event confirms forecast | Supply chain attack confirms supply risk |

### 8.6 Contextual Relationships (2)

| Relationship | Domain A | Domain B | Semantics | Example |
|--------------|----------|----------|-----------|---------|
| `DRIVEN_BY` | DECISION_PATTERN | EXTERNAL_FACTOR | External factor influences decision | Regulatory change → compliance decision |
| `CONSTRAINED_BY` | ORGANIZATION | EXTERNAL_FACTOR | External factor limits options | Budget constraints → minimal security |

---

## 9. TRAINING DATA STRUCTURE

### 9.1 Minimum Training Data Requirements

```yaml
Training_Data_Structure:
  total_annotations: 5000  # Minimum annotations
  per_entity_type:
    COGNITIVE_BIAS: 400      # 40 examples × 10 subtypes
    THREAT_PERCEPTION: 200   # 20 examples × 6 subtypes
    DECISION_PATTERN: 250    # 25 examples × 8 subtypes
    ORGANIZATIONAL_STRESS: 150 # 15 examples × 6 subtypes
    ORGANIZATION: 300        # 30 examples × 7 subtypes
    ROLE: 300               # 25 examples × 12 subtypes
    PROCESS: 250            # 30 examples × 8 subtypes
    CAPABILITY_GAP: 300     # 30 examples × 9 subtypes
    THREAT_ACTOR: 250       # 30 examples × 7 subtypes
    ATTACK_VECTOR: 300      # 25 examples × 12 subtypes
    VULNERABILITY: 250      # 40 examples × 6 subtypes
    IMPACT_TYPE: 200        # 25 examples × 8 subtypes
    INDICATOR_OF_COMPROMISE: 200 # 30 examples × 6 subtypes
    TACTICAL_PATTERN: 250   # 20 examples × 13 subtypes
    STRATEGIC_OBJECTIVE: 150 # 25 examples × 6 subtypes
    HISTORICAL_EVENT: 200   # 40 examples × 5 subtypes
    PREDICTION_OUTCOME: 150 # 30 examples × 4 subtypes
    EXTERNAL_FACTOR: 100    # 15 examples × 6 subtypes

  relationship_annotations: 2000  # Minimum 24 types × 80+ examples each

  quality_standards:
    inter_annotator_agreement: "> 0.85 Cohen's Kappa"
    annotation_confidence_threshold: "> 0.80"
    example_diversity: "Multiple sectors, org sizes, threat types"
```

### 9.2 Annotation Format

```json
{
  "example_id": "NER11-TRAIN-2501",
  "text": "Full training text example...",
  "metadata": {
    "source_document": "Incident report from ABC Corp",
    "document_type": "incident_response",
    "sector": "financial_services",
    "organization_size": "ENTERPRISE",
    "date_created": "2025-11-25"
  },
  "entities": [
    {
      "text": "entity mention text",
      "type": "ENTITY_TYPE",
      "subtype": "ENTITY_SUBTYPE",
      "start": 45,
      "end": 67,
      "confidence": 0.92,
      "attributes": {
        "attribute_name": "attribute_value"
      }
    }
  ],
  "relationships": [
    {
      "head_entity_id": 0,
      "tail_entity_id": 1,
      "relationship_type": "RELATIONSHIP_NAME",
      "confidence": 0.88,
      "evidence_span": "text supporting relationship"
    }
  ],
  "annotator_notes": "Any special notes or ambiguities"
}
```

---

## 10. VALIDATION CRITERIA

### 10.1 Entity Validation

- **Boundary Accuracy**: Correct token/character start/end positions
- **Type Correctness**: Proper entity classification
- **Subtype Accuracy**: Correct subtype assignment where applicable
- **Attribute Completeness**: All required attributes present
- **Confidence Justification**: Confidence score matches evidence strength

### 10.2 Relationship Validation

- **Entity Existence**: Both entities present in document
- **Relationship Plausibility**: Relationship type matches entities
- **Evidence Quality**: Clear textual support for relationship
- **Directionality**: Correct relationship direction (where applicable)
- **No Hallucination**: Relationships not inferred from outside knowledge

---

## 11. PSYCHOHISTORY INTEGRATION

### 11.1 Predictive Pattern Recognition

```
COGNITIVE_BIAS → THREAT_PERCEPTION → DECISION_PATTERN → PREDICTION_OUTCOME

Example Chain:
NORMALCY_BIAS (entity)
  ├─ INFLUENCES (relationship)
  └─ REACTIVE_DECISION (entity)
      ├─ CREATES (relationship)
      └─ PERCEIVED_IMAGINARY (entity)
          ├─ PREDICTS (relationship)
          └─ MISSED_REAL_THREAT (prediction)
```

### 11.2 Organizational Vulnerability Chains

```
CAPABILITY_GAP → ORGANIZATIONAL_STRESS → THREAT_PERCEPTION → DECISION_PATTERN

Example:
SKILLS_GAP (entities)
  ├─ MANIFESTS_AS (relationship)
  └─ RESOURCE_STRAIN (entity)
      ├─ INFLUENCES (relationship)
      └─ REACTIVE_DECISION (entity)
          ├─ CAUSES_NEGLECT (relationship)
          └─ ADDITIONAL_SKILLS_GAP (entity) [Loop]
```

---

## 12. SECTOR-SPECIFIC ENTITY EMPHASIS

### 12.1 Critical Infrastructure
- High emphasis: ORGANIZATIONAL_STRESS, EXTERNAL_FACTOR, IMPACT_TYPE
- Common patterns: Regulatory-driven decisions, public safety impacts

### 12.2 Financial Services
- High emphasis: THREAT_ACTOR, STRATEGIC_OBJECTIVE (Financial theft), COMPLIANCE-driven
- Common patterns: Sophistication arms race, insider threat focus

### 12.3 Healthcare
- High emphasis: IMPACT_TYPE (safety/patient privacy), EXTERNAL_FACTOR (pandemic)
- Common patterns: Clinical operations prioritized over security, compliance-driven

### 12.4 Government
- High emphasis: THREAT_ACTOR (nation-state), STRATEGIC_OBJECTIVE (geopolitical)
- Common patterns: APT-focused, classified intelligence considerations

---

## 13. QUALITY ASSURANCE PROCESS

### 13.1 Multi-Stage Annotation

1. **Primary Annotation**: Initial entity and relationship identification
2. **Expert Review**: Domain expert validation (security practitioner)
3. **Inter-Annotator Agreement**: Cross-validation by independent annotator
4. **Conflict Resolution**: Discussion and consensus on disagreements
5. **Final Validation**: QA check for completeness and consistency

### 13.2 Metrics Tracking

- **Cohen's Kappa**: Inter-annotator agreement (target: > 0.85)
- **Precision**: Correctly identified entities vs. all identified
- **Recall**: Found entities vs. all entities in text
- **F1-Score**: Harmonic mean of precision and recall
- **Subtype Accuracy**: Correct subtype classification rate

---

## 14. NEXT STEPS

1. Collect 5,000+ annotated training examples
2. Implement annotation interface with quality controls
3. Train NER11 model with validation split
4. Evaluate against test set (20% held-out)
5. Iterate on low-performing entity/relationship types
6. Deploy in Psychohistory system for continuous learning

---

**End of NER11 Specification** (1,047 lines)
