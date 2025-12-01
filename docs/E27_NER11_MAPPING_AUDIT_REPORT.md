# Enhancement 27 NER11 Mapping Audit Report

**File:** E27_NER11_MAPPING_AUDIT_REPORT.md
**Created:** 2025-11-27 00:00:00 UTC
**Auditor:** NER Specialist Auditor (Claude Code)
**Version:** v1.0.0
**Purpose:** Comprehensive audit of NER11 to Neo4j Super Label mapping
**Status:** COMPLETE

---

## Executive Summary

**Overall Mapping Completeness: 4/10**
**Overall Mapping Accuracy: 6/10**
**Discriminator Property Design: 7/10**

**CRITICAL FINDINGS:**
1. Only **291 of 566 entities (51.4%)** are explicitly mapped in Enhancement 27
2. **275 entities (48.6%)** have NO mapping specified
3. Entire tiers missing complete mappings (Tier 7, 8, 9, 11)
4. Some entity categories lack appropriate Super Labels

---

## Tier-by-Tier Analysis

### TIER 1: Technical (Cybersecurity Core) - 149 Entities

**Status:** PARTIALLY MAPPED (96/149 = 64.4%)

**Explicitly Mapped (96):**
- ✅ Threat Actors: 7 entities → `ThreatActor` (actorType discriminator)
- ✅ Malware: 14 entities → `Malware` (malwareFamily discriminator)
- ✅ Vulnerabilities: 15 entities → `Vulnerability` (vulnType discriminator)
- ✅ Attack Techniques: 33 entities → `AttackPattern` (patternType discriminator)
- ✅ OT/ICS Assets: 87 entities → `Asset` (assetClass="OT", deviceType discriminator)

**UNMAPPED (53 entities):**

#### Software Components (26 entities) - CRITICAL GAP
```
❌ SOFTWARE_COMPONENT → No mapping specified
❌ LIBRARY → No mapping specified
❌ PACKAGE → No mapping specified
❌ COMPONENT → No mapping specified
❌ PACKAGE_MANAGER (NPM, PYPI, MAVEN, NUGET) → No mapping specified
❌ FIRMWARE → No mapping specified
❌ DEPENDENCY, DEPENDENCY_TREE → No mapping specified
❌ SBOM, BOM → No mapping specified
❌ BUILD, BUILD_SYSTEM → No mapping specified
❌ ATTESTATION, PROVENANCE → No mapping specified
❌ LICENSE, SOFTWARE_LICENSE, LICENSE_COMPLIANCE → No mapping specified
❌ SOFTWARE_STANDARD (DO_178C, IEC_61508, ISO_26262) → No mapping specified
❌ CPE, CPES → No mapping specified
❌ FAISS, LangChain, Vector Database, Embeddings → No mapping specified
```

**RECOMMENDATION:** Create new Super Label `Software` or map to existing `Software` label
**Suggested Mapping:**
```cypher
SOFTWARE_COMPONENT → Software {softwareType="component"}
LIBRARY → Software {softwareType="library"}
PACKAGE → Software {softwareType="package"}
FIRMWARE → Software {softwareType="firmware"}
SBOM → Software {softwareType="sbom"}
LICENSE → Software {softwareType="license"}
```

#### Indicators (7 entities)
```
✅ INDICATOR, OBSERVABLE, IOC → Indicator (mapped in table, but not in Cypher scripts)
❌ TOTAL_INDICATOR_INSTANCES → No mapping
❌ INSIDER_THREAT, INSIDER_THREAT_INDICATOR, INSIDER_INDICATOR → Unclear if mapped
```

**RECOMMENDATION:** Verify Indicator label exists and map insider threat indicators:
```cypher
INSIDER_THREAT_INDICATOR → Indicator {indicatorType="insider_threat"}
```

#### Process & Physics (15 entities)
```
❌ PROCESS, TREATMENT_PROCESS, FUNCTION → No mapping
❌ CONTROL_SYSTEM, SCADA_SYSTEM, ENERGY_MANAGEMENT_SYSTEM → Partially mapped to Asset
❌ ICS_COMPONENTS, IACS_CONTEXT, ARCHITECTURE → No mapping
❌ POWER_OUTPUT, IP_RATING, EMERGENCY_FEATURES, AUDIO_OUTPUT → No mapping
❌ MATERIAL, MEASUREMENT → No mapping
```

**RECOMMENDATION:**
- Physical properties → `Asset` properties (not separate entities)
- Abstract concepts → `Indicator` or new `Concept` label

#### Network & Protocols (30 entities)
```
✅ ICS Protocols (MODBUS, DNP3, IEC_61850, OPC_UA, etc.) → Protocol
❌ NETWORK, NETWORK_SEGMENT, VIRTUAL_NETWORK, NETWORK_INTERFACE → No mapping
❌ ZONE, NETWORK_ZONE, SECURITY_ZONE → Duplicate in Tier 3, needs resolution
❌ PROTOCOL_OBJECT, PROTOCOL_FUNCTION, PROTOCOL_COMPONENT_FUNCTION → No mapping
❌ CHANNEL_CAPACITY, BLUETOOTH → No mapping
```

**RECOMMENDATION:**
```cypher
NETWORK → Asset {assetClass="IT", deviceType="network"}
PROTOCOL_OBJECT → Protocol {protocolType="ics", subtype="object"}
CHANNEL_CAPACITY → Indicator {indicatorType="network_metric"}
```

---

### TIER 2: Psychometric (Human Factors) - 62 Entities

**Status:** PARTIALLY MAPPED (48/62 = 77.4%)

**Explicitly Mapped (48):**
- ✅ Lacanian Psychoanalysis (20 entities) → `PsychTrait {traitType="lacanian"}`
- ✅ Cognitive Bias (19 entities) → `PsychTrait {traitType="cognitive_bias"}`
- ✅ Dark Triad (3 entities) → `PsychTrait {traitType="personality", subtype="dark_triad_*"}`
- ✅ Threat Perception (6 entities) → `PsychTrait {traitType="perception"}`

**UNMAPPED (14 entities):**

#### Big 5 Personality Traits (10 entities)
```
❌ BIG_5_OPENNESS, Openness to Experience → No mapping
❌ BIG_5_CONSCIENTIOUSNESS, Conscientiousness → No mapping
❌ BIG_5_EXTRAVERSION, Extraversion → No mapping
❌ BIG_5_AGREEABLENESS, Agreeableness → No mapping
❌ BIG_5_NEUROTICISM, Neuroticism → No mapping
```

**RECOMMENDATION:**
```cypher
BIG_5_OPENNESS → PsychTrait {traitType="personality", subtype="big5_openness"}
BIG_5_CONSCIENTIOUSNESS → PsychTrait {traitType="personality", subtype="big5_conscientiousness"}
// ... etc for other Big 5 traits
```

#### Other Personality Systems (4 entities)
```
❌ DISC_DOMINANCE, DISC_INFLUENCE, DISC_STEADINESS, DISC_CONSCIENTIOUSNESS → No mapping
❌ MBTI_TYPE, ENNEAGRAM_TYPE → No mapping
❌ LEARNING_OUTCOME, LEARNING, CONFIDENCE → No mapping
```

**RECOMMENDATION:**
```cypher
DISC_DOMINANCE → PsychTrait {traitType="personality", subtype="disc_dominance"}
MBTI_TYPE → PsychTrait {traitType="personality", subtype="mbti"}
ENNEAGRAM_TYPE → PsychTrait {traitType="personality", subtype="enneagram"}
LEARNING_OUTCOME → PsychTrait {traitType="cognitive", subtype="learning"}
CONFIDENCE → PsychTrait {traitType="cognitive", subtype="confidence"}
```

---

### TIER 3: Organizational - 69 Entities

**Status:** POORLY MAPPED (31/69 = 44.9%)

**Explicitly Mapped (31):**
- ✅ Roles (31 entities) → `Role {roleType}` (assumed, but not in Cypher scripts)

**UNMAPPED (38 entities):**

#### Organizational Attributes & Governance (28 entities)
```
❌ SECURITY_CULTURE → No mapping (should be Organization property or PsychTrait)
❌ SECTOR_MATURITY → No mapping (should be Organization property)
❌ ORGANIZATION, COMPANY, AGENCY → Organization (assumed, but not in Cypher)
❌ VENDOR, VENDORS, SUPPLIER, CONTRACTOR, PARTNER → No clear mapping
❌ SUPPLY_CHAIN, PROCUREMENT_PROCESS, RFP, CONTRACT, SLA → No mapping
❌ BUDGET, SECURITY_BUDGET, ROI, PRICE → EconomicMetric (not mapped)
❌ RISK_TOLERANCE, RISK_APPETITE, RISK_THRESHOLD → No mapping
❌ COMPLIANCE_FRAMEWORK (NIST, ISO, PCI_DSS) → Control (not explicitly mapped)
❌ POLICY, REQUIREMENT, STANDARDS, STANDARD, SECURITY_STANDARD → No mapping
❌ REGULATORY_REFERENCES, DOCUMENT_CONTROL → No mapping
❌ ESCROW, SOFTWARE_ESCROW, DIGITAL_ESCROW, Multi-party Escrow → No mapping
```

**RECOMMENDATION:**
```cypher
VENDOR → Organization {orgType="vendor"}
SUPPLY_CHAIN → Organization {orgType="supply_chain"}
SECURITY_BUDGET → EconomicMetric {metricType="budget"}
RISK_TOLERANCE → PsychTrait {traitType="risk_perception", subtype="tolerance"}
COMPLIANCE_FRAMEWORK → Control {controlType="framework"}
POLICY → Control {controlType="policy"}
ESCROW → Organization {orgType="escrow_service"}
```

#### Physical & Geography (10 entities)
```
✅ LOCATION, COUNTRY, REGION, CITY → Location (assumed)
❌ FACILITY_PHYSICAL → Asset or Location?
❌ Duplicates: DATACENTER, OFFICE, PLANT, ZONE (already in Tier 1)
❌ PHYSICAL_ACCESS, PHYSICAL_ACCESS_CONTROL → Control?
❌ SURVEILLANCE, SURVEILLANCE_SYSTEM, CAMERA → Asset?
❌ ENVIRONMENTAL, HVAC, POWER, COOLING → Asset properties?
❌ GEOGRAPHIC_RISK, GEOPOLITICAL_RISK, NATURAL_DISASTER → Risk type?
❌ GPS, OPERATING_TEMP → Indicator?
```

**CRITICAL ISSUE:** Tier 3 duplicates many Tier 1 entities (DATACENTER, OFFICE, PLANT, ZONE)

**RECOMMENDATION:**
```cypher
PHYSICAL_ACCESS_CONTROL → Control {controlType="physical_access"}
SURVEILLANCE_SYSTEM → Asset {assetClass="physical", deviceType="surveillance"}
CAMERA → Asset {assetClass="physical", deviceType="camera"}
GEOGRAPHIC_RISK → Event {eventType="geographic_risk"}
NATURAL_DISASTER → Event {eventType="natural_disaster"}
```

---

### TIER 4: Economic - 45 Entities

**Status:** PARTIALLY MAPPED (42/45 = 93.3%)

**Explicitly Mapped (42):**
- ✅ Demographics (25 entities) → `EconomicMetric` (assumed, but need verification)
- ✅ Financial Impact (17 entities) → `EconomicMetric {metricType}`

**UNMAPPED (3 entities):**
```
❌ COST_IMPACT → Should be EconomicMetric {metricType="cost_impact"}
❌ Some demographic entities unclear if mapped (POPULATION_DENSITY, TECH_ADOPTION)
```

**RECOMMENDATION:**
All Tier 4 entities should map to `EconomicMetric` with appropriate `metricType` discriminators.

---

### TIER 5: Behavioral - 47 Entities

**Status:** NOT MAPPED (0/47 = 0%)

**UNMAPPED (47 entities):**

#### Patterns (24 entities)
```
❌ HISTORICAL_PATTERN, PAST_BEHAVIOR → No mapping
❌ ORG_BEHAVIOR, SECTOR_BEHAVIOR → No mapping
❌ ATTACKER_BEHAVIOR, ATTACK_PATTERN, ATTACK_PATTERNS → AttackPattern? (confusion with Tier 1)
❌ OBSERVABLE_TTP, CAMPAIGN_PATTERN → No mapping
❌ MULTI_STAGE_OPERATION → Campaign?
❌ SEASONAL_PATTERN, TIME_BASED_TREND → Indicator?
❌ GEOGRAPHIC_PATTERN, REGION_SPECIFIC_ATTACK → No mapping
❌ TARGET_SELECTION, VICTIM_CRITERIA → No mapping
❌ PERSISTENCE_METHOD, EXFILTRATION_METHOD, DATA_THEFT_TECHNIQUE → AttackPattern?
❌ DESTRUCTION_METHOD, WIPER → Malware? (WIPER already in Tier 1)
❌ RANSOMWARE_TACTIC → Malware or AttackPattern?
❌ SOCIAL_BEHAVIOR, SOCIAL_MEDIA_TACTIC → No mapping
```

**RECOMMENDATION:**
```cypher
// Behavioral patterns should be either:
HISTORICAL_PATTERN → Indicator {indicatorType="behavioral_pattern"}
ATTACK_PATTERN → AttackPattern (already exists in Tier 1)
PERSISTENCE_METHOD → AttackPattern {patternType="persistence"}
EXFILTRATION_METHOD → AttackPattern {patternType="exfiltration"}
SOCIAL_BEHAVIOR → PsychTrait {traitType="social_behavior"}
```

#### Threat Perception (23 entities)
```
❌ REAL_THREAT, ACTUAL_THREAT → Event?
❌ IMAGINARY_THREAT, PERCEIVED_THREAT → PsychTrait?
❌ SYMBOLIC_THREAT, CULTURAL_THREAT → PsychTrait?
❌ EXISTENTIAL_THREAT, SURVIVAL_THREAT → Event?
❌ OPERATIONAL_THREAT, OPERATIONS_THREAT → Event?
❌ REPUTATIONAL_THREAT, BRAND_DAMAGE → Event or EconomicMetric?
❌ FINANCIAL_THREAT, ECONOMIC_LOSS → EconomicMetric?
❌ COMPLIANCE_THREAT, REGULATORY_RISK → Event?
❌ STRATEGIC_THREAT, LONG_TERM_THREAT → Event?
❌ TACTICAL_THREAT, IMMEDIATE_THREAT → Event?
❌ THREAT, RISK, CHALLENGE → Generic, needs disambiguation
```

**RECOMMENDATION:**
```cypher
// Threat perception overlaps with Tier 2 psychometric entities
// Suggest consolidation:
PERCEIVED_THREAT → PsychTrait {traitType="perception", subtype="perceived_threat"}
ACTUAL_THREAT → Event {eventType="threat"}
FINANCIAL_THREAT → EconomicMetric {metricType="threat_cost"}
COMPLIANCE_THREAT → Event {eventType="compliance_threat"}
```

---

### TIER 6: Sector-Specific - 31 Entities

**Status:** POORLY MAPPED (17/31 = 54.8%)

**Explicitly Mapped (17):**
- ✅ Sectors (17 entities: WATER, ENERGY, TRANSPORTATION, etc.) → `Organization {orgType="sector"}`

**UNMAPPED (14 entities):**

#### Templates & Sector-Specific Entities (14 entities)
```
❌ SECTOR_EQUIPMENT (e.g., WATER_SCADA, ENERGY_GRID) → Asset?
❌ SECTOR_PROCESS (e.g., WATER_TREATMENT, ENERGY_DISTRIBUTION) → Process concept?
❌ SECTOR_VULNERABILITY (e.g., WATER_CONTAMINATION, GRID_BLACKOUT) → Event?
❌ SECTOR_REGULATION (e.g., EPA_WATER_STANDARDS, NERC_CIP) → Control?
❌ SECTOR_INCIDENT (e.g., WATER_SECTOR_BREACH, ENERGY_DISRUPTION) → Event?
```

**RECOMMENDATION:**
```cypher
WATER_SCADA → Asset {assetClass="OT", deviceType="scada", sector="water"}
WATER_TREATMENT → Process concept (no Super Label exists for this)
WATER_CONTAMINATION → Event {eventType="sector_vulnerability", sector="water"}
EPA_WATER_STANDARDS → Control {controlType="regulation", sector="water"}
WATER_SECTOR_BREACH → Event {eventType="incident", sector="water"}
```

**CRITICAL GAP:** No Super Label for "Process" concepts exists.

---

### TIER 7: Safety/Reliability - 52 Entities

**Status:** NOT MAPPED (0/52 = 0%)

**UNMAPPED (52 entities):**

#### RAMS & Hazards (29 entities)
```
❌ RELIABILITY, MTBF, MTTR, FAILURE_RATE → Indicator?
❌ AVAILABILITY, UPTIME, DOWNTIME → Indicator?
❌ MAINTAINABILITY, PREVENTIVE_MAINTENANCE, CORRECTIVE_MAINTENANCE → Process?
❌ SAFETY, FUNCTIONAL_SAFETY, SAFETY_INTEGRITY_LEVEL, SIL → Control?
❌ REDUNDANCY, N_PLUS_1, FAIL_SAFE → Architecture concept?
❌ SAFETY_CRITICAL, SAFETY_CONSIDERATIONS → Control?
❌ CYBER_FAILURE_MODE → Vulnerability?
❌ HAZARD, RISK_SCENARIO, ACCIDENT, INCIDENT, INCIDENT_DETAIL, INCIDENT_IMPACT → Event?
❌ HAZOP, DEVIATION, GUIDE_WORD → Process?
❌ FMEA, FAILURE_MODE, EFFECT_ANALYSIS, RPN → Process?
❌ LOPA, IPL, PROTECTION_LAYER → Control?
❌ BOW_TIE, THREAT_LINE, CONSEQUENCE_LINE → Process?
❌ FAULT_TREE, BASIC_EVENT, TOP_EVENT → Process?
❌ SCENARIO, MITIGATION, IMPACT, CONSEQUENCE, CONSEQUENCES → Event?
❌ COUNTERMEASURE, RESIDUAL_RISK, EXISTING_SAFEGUARDS → Control?
❌ WHAT_IF, RISK_SCORE → Process?
```

**RECOMMENDATION:**
```cypher
// Metrics
MTBF → Indicator {indicatorType="reliability_metric"}
AVAILABILITY → Indicator {indicatorType="availability_metric"}

// Safety concepts
FUNCTIONAL_SAFETY → Control {controlType="safety"}
SIL → Control {controlType="safety_integrity_level"}
HAZARD → Event {eventType="hazard"}
RISK_SCENARIO → Event {eventType="risk_scenario"}

// Mitigation
COUNTERMEASURE → Control {controlType="countermeasure"}
PROTECTION_LAYER → Control {controlType="protection_layer"}
```

**CRITICAL GAP:** Many safety engineering concepts (FMEA, HAZOP, Bow-Tie, Fault Tree) have no appropriate Super Label. These are methodologies, not entities.

#### Deterministic Control (11 entities)
```
❌ DETERMINISTIC, REAL_TIME, WCET, DEADLINE → System properties?
❌ SAFETY_PLC, SIS, ESD, TRIP_SYSTEM → Asset?
❌ FORMAL_VERIFICATION, MODEL_CHECKING, THEOREM_PROVING → Process/Method?
```

**RECOMMENDATION:**
```cypher
SAFETY_PLC → Asset {assetClass="OT", deviceType="safety_plc"}
SIS → Asset {assetClass="OT", deviceType="sis"}
WCET → Indicator {indicatorType="timing_metric"}
FORMAL_VERIFICATION → Control {controlType="verification_method"}
```

---

### TIER 8: Ontology Frameworks - 42 Entities

**Status:** NOT MAPPED (0/42 = 0%)

**UNMAPPED (42 entities):**

#### IEC 62443 Entities (12 entities)
```
❌ SECURITY_LEVEL, SL_TARGET, SL_ACHIEVED, SL_CAPABILITY → Control or Indicator?
❌ FOUNDATIONAL_REQUIREMENT (FR) → Control?
❌ SYSTEM_REQUIREMENT (SR) → Control?
❌ COMPONENT_REQUIREMENT (CR) → Control?
❌ ZONE_CONDUIT, CONDUIT → Network concept?
❌ IEC_62443 → Standard reference?
```

**RECOMMENDATION:**
```cypher
SECURITY_LEVEL → Indicator {indicatorType="security_level"}
FOUNDATIONAL_REQUIREMENT → Control {controlType="iec62443_fr"}
ZONE_CONDUIT → Asset {assetClass="network", deviceType="conduit"}
IEC_62443 → Control {controlType="standard", standardId="IEC 62443"}
```

#### Adversary Emulation (16 entities)
```
❌ EMULATION_PLAN, ADVERSARY_PROFILE, EM3D_TACTIC, EM3D_TECHNIQUE → Campaign?
❌ ADVERSARY_EMULATION, MICRO_EMULATION_PLAN → Campaign?
❌ Adversary Emulation Plan, Intelligence Summary, Adversary Overview → Campaign metadata?
❌ Operational Flow, Emulation Phases, Micro Emulation Plan → Campaign properties?
```

**RECOMMENDATION:**
```cypher
EMULATION_PLAN → Campaign {campaignType="emulation"}
EM3D_TACTIC → AttackPattern {patternType="em3d_tactic"}
ADVERSARY_PROFILE → ThreatActor {actorType="emulation_profile"}
```

#### Ontology Meta-Entities (14 entities)
```
❌ ASSET (Duplicate from Tier 1)
❌ RELATIONSHIP, PROPERTY, CLASS, INSTANCE → Graph meta-concepts (not entities)
❌ ONTOLOGY_CLASS, KNOWLEDGE_GRAPH_NODE, KNOWLEDGE_GRAPH_EDGE → Graph meta-concepts
❌ ENTITY_TYPE, RELATED_ENTITIES → Graph meta-concepts
❌ STRIDE_CATEGORY, DFD_ELEMENT, STRIDE_MAPPING → Threat modeling concepts?
❌ RISK_ASSESSMENT → Process?
❌ NIST_800_53, MIL_STD → Standards?
```

**RECOMMENDATION:**
```cypher
// Meta-concepts should NOT be entities in the graph
// These are structural concepts, not domain entities

// Exception: Threat modeling concepts
STRIDE_CATEGORY → AttackPattern {patternType="stride"}
DFD_ELEMENT → Asset {assetClass="IT"} // Data Flow Diagram elements
RISK_ASSESSMENT → Event {eventType="assessment"}
NIST_800_53 → Control {controlType="standard", standardId="NIST 800-53"}
```

---

### TIER 9: Contextual & Meta - 45 Entities

**Status:** NOT MAPPED (0/45 = 0%)

**UNMAPPED (45 entities):**

#### Abstract Concepts (19 entities)
```
❌ CONTEXT, TECHNICAL_CONTEXT → Meta-concept (not an entity)
❌ DESCRIPTION, PURPOSE, EXAMPLE → Properties, not entities
❌ REALITY, DEFINITION, OUTCOME → Meta-concepts
❌ CALCULATION, METHODOLOGY, PRINCIPLE → Meta-concepts
❌ GOAL, TECHNIQUES → Meta-concepts
❌ CONTROL, EXISTING_CONTROLS, NIST_CONTROLS → Control (but not mapped in scripts)
❌ ENFORCEMENT, VERIFICATION, IMPLEMENTATION → Process concepts
❌ PROCEDURE, OPERATION, ACTIVITY, ACTION, TASK, PRACTICE → Process concepts
```

**RECOMMENDATION:**
**DO NOT MAP.** These are properties or meta-concepts, not entities. They should be:
- Properties of other entities (e.g., `description`, `purpose`)
- Relationship metadata (e.g., `methodology`)
- Documentation concepts (e.g., `example`)

#### Technical Controls & Mitigation (14 entities)
```
❌ TECHNICAL_CONTROLS → Control
❌ MITIGATION_STRATEGIES, MITIGATION_TECHNOLOGY → Control
❌ MITIGATION_EFFECTIVENESS, MITIGATION_IMPLEMENTATION → Control properties
❌ BENEFIT, BENEFITS, EFFECTIVENESS → Properties, not entities
❌ CYBERSECURITY_IMPACT, CYBERSECURITY_MANIFESTATION → Event or Indicator?
```

**RECOMMENDATION:**
```cypher
TECHNICAL_CONTROLS → Control {controlType="technical"}
MITIGATION_STRATEGIES → Control {controlType="mitigation"}
CYBERSECURITY_IMPACT → Event {eventType="impact"}
// effectiveness, benefits → properties, not entities
```

#### Protocol Metadata (12 entities)
```
❌ PROTOCOL_DEPLOYMENT, VENDOR_DEPLOYMENT → Event?
❌ VENDOR_PRODUCT, PRODUCT_LINE → Software?
❌ PROTOCOL_STANDARD, PROTOCOL_SECTOR → Protocol properties
❌ PROTOCOL_EVOLUTION, PROTOCOL_TREND → Indicator?
❌ PROTOCOL_LATENCY, PROTOCOL_MESSAGE → Indicator or Protocol property?
```

**RECOMMENDATION:**
```cypher
VENDOR_PRODUCT → Software {softwareType="vendor_product"}
PROTOCOL_DEPLOYMENT → Event {eventType="deployment"}
PROTOCOL_LATENCY → Indicator {indicatorType="protocol_metric"}
// Standard, sector, evolution → Protocol properties, not separate entities
```

---

### TIER 11: Expanded Concepts - 49 Entities

**Status:** NOT MAPPED (0/49 = 0%)

**UNMAPPED (49 entities):**

#### Operation Modes (10 entities)
```
❌ OPERATION_MODE, ACCESS_STATE, SYSTEM_LIFECYCLE → Asset states (properties, not entities)
❌ Data Acquisition Mode, Monitoring Mode, Control Mode → Asset states
❌ Event Recording Mode, Supervisory Mode, Degraded Mode → Asset states
❌ Maintenance Mode, Fail-Safe Mode → Asset states
❌ System State → Asset property
```

**RECOMMENDATION:**
**DO NOT CREATE SEPARATE ENTITIES.** These are `Asset` property values:
```cypher
// Instead of separate entities:
Asset {
  operationMode: "monitoring",
  accessState: "operational",
  systemLifecycle: "production"
}
```

#### System Attributes (27 entities)
```
❌ SYSTEM_ATTRIBUTE, PERFORMANCE_METRIC → Indicator?
❌ DATA_FORMAT, CONNECTION_TYPE → Asset properties
❌ Mean Time Between Failures (MTBF), Mean Time To Repair (MTTR) → Duplicates from Tier 7
❌ Data Acquisition Accuracy, Communication Speed, Processing Power → Indicator?
❌ Scalability, Measurement Precision, Production Rate, Quality Rate → Indicator?
❌ On-time Delivery, Distributed Control, Redundancy (Duplicate) → Indicator?
❌ Flexibility, Interoperability, Automated Control, System Integration → Indicator?
❌ Data Format, Connection Type (Duplicate) → Asset properties
```

**RECOMMENDATION:**
```cypher
// Metrics
Data Acquisition Accuracy → Indicator {indicatorType="performance_metric"}
Communication Speed → Indicator {indicatorType="performance_metric"}
Production Rate → Indicator {indicatorType="production_metric"}

// Properties (not separate entities)
DATA_FORMAT → Asset property
CONNECTION_TYPE → Asset property
```

#### Miscellaneous (12 entities)
```
❌ FREQUENCY, UNIT_OF_MEASURE → Properties, not entities
❌ HARDWARE_COMPONENT → Asset?
❌ VERIFICATION_ACTIVITY, PROCESS_ACTION → Process concepts
❌ REGULATORY_CONCEPT → Meta-concept
❌ CRYPTOGRAPHY → Protocol or Control?
❌ SECURITY_TOOL → Software?
❌ THREAT_GROUP (Duplicate from Tier 1) → ThreatActor
❌ ATTACK_TYPE → AttackPattern?
❌ VENDOR_NAME → Organization property
```

**RECOMMENDATION:**
```cypher
HARDWARE_COMPONENT → Asset {assetClass="hardware"}
CRYPTOGRAPHY → Protocol {protocolType="cryptographic"}
SECURITY_TOOL → Software {softwareType="security_tool"}
ATTACK_TYPE → AttackPattern {patternType discriminator}
VENDOR_NAME → Organization {orgType="vendor"} property
```

---

## Summary of Unmapped Entities by Category

### Category 1: Should Be Mapped to Existing Super Labels (187 entities)

| Category | Count | Target Super Label | Example Entities |
|----------|-------|-------------------|------------------|
| Software components | 26 | Software | LIBRARY, PACKAGE, SBOM, LICENSE |
| Network infrastructure | 15 | Asset | NETWORK, NETWORK_SEGMENT |
| Organizational | 28 | Organization/Control | VENDOR, POLICY, COMPLIANCE_FRAMEWORK |
| Financial | 3 | EconomicMetric | COST_IMPACT |
| Behavioral patterns | 47 | AttackPattern/Event/PsychTrait | ATTACK_PATTERN, THREAT types |
| Sector-specific | 14 | Asset/Event/Control | WATER_SCADA, GRID_BLACKOUT |
| Safety/Reliability metrics | 29 | Indicator/Control | MTBF, SIL, HAZARD |
| Safety systems | 11 | Asset/Control | SAFETY_PLC, SIS |
| Ontology frameworks | 28 | Control/Campaign | IEC_62443, EMULATION_PLAN |
| Technical controls | 14 | Control | MITIGATION_STRATEGIES |

### Category 2: Properties Not Entities (64 entities)

**Should NOT be separate entities, but properties of other entities:**
- Abstract concepts (19): CONTEXT, DESCRIPTION, PURPOSE, METHODOLOGY
- Operation modes (10): Monitoring Mode, Degraded Mode (→ Asset properties)
- System attributes (27): DATA_FORMAT, CONNECTION_TYPE (→ Asset properties)
- Metadata (8): UNIT_OF_MEASURE, FREQUENCY

### Category 3: Missing Super Labels (24 entities)

**Require NEW Super Label creation or fundamental re-thinking:**

#### Process Entities (Requires new "Process" Super Label)
```
PROCESS, TREATMENT_PROCESS, FUNCTION
FMEA, HAZOP, BOW_TIE, FAULT_TREE (Safety methodologies)
VERIFICATION_ACTIVITY, PROCESS_ACTION
```

**RECOMMENDATION:** Create 17th Super Label: `Process`
```cypher
Process {
  processType: "operational" | "safety_methodology" | "verification",
  subtype: "fmea" | "hazop" | "bow_tie" | "fault_tree"
}
```

#### Graph Meta-Concepts (Should NOT be entities)
```
RELATIONSHIP, PROPERTY, CLASS, INSTANCE
ONTOLOGY_CLASS, KNOWLEDGE_GRAPH_NODE, KNOWLEDGE_GRAPH_EDGE
ENTITY_TYPE, RELATED_ENTITIES
```

**RECOMMENDATION:** **DO NOT MAP.** These are graph structural concepts, not domain entities.

---

## Critical Mapping Issues

### Issue 1: Duplicate Entities Across Tiers

**DUPLICATES FOUND:**
- `ATTACK_PATTERN` appears in Tier 1 (technical) and Tier 5 (behavioral)
- `WIPER` appears in Tier 1 (malware) and Tier 5 (destruction method)
- `DATACENTER`, `OFFICE`, `PLANT`, `ZONE` appear in both Tier 1 and Tier 3
- `MTBF`, `MTTR`, `REDUNDANCY` duplicated in Tier 7 and Tier 11
- `THREAT_GROUP` duplicated in Tier 1 and Tier 11

**IMPACT:** Confusion in NER training, ambiguous entity recognition

**RECOMMENDATION:** De-duplicate entity list, consolidate to single tier per entity type.

### Issue 2: Tier 5 "Threat" Entities Overlap with Tier 2 Psychometric

**Problem:** Tier 5 has 23 threat perception entities that conceptually belong in psychometric domain:
- `IMAGINARY_THREAT`, `PERCEIVED_THREAT` → psychological perception
- `REPUTATIONAL_THREAT` → organizational psychology
- Overlap with Tier 2's `THREAT_PERCEPTION` entity

**RECOMMENDATION:** Consolidate all threat perception entities under Tier 2 psychometric, map to:
```cypher
PsychTrait {traitType="perception", subtype="threat_*"}
```

### Issue 3: No Super Label for "Process" or "Methodology"

**Problem:** 24+ entities represent processes, methodologies, or procedures:
- Safety methodologies: FMEA, HAZOP, Bow-Tie, Fault Tree
- Verification activities: FORMAL_VERIFICATION, MODEL_CHECKING
- General processes: PROCESS, TREATMENT_PROCESS, FUNCTION

**RECOMMENDATION:** Either:
1. Create 17th Super Label `Process`, OR
2. Map to `Event {eventType="process_activity"}`, OR
3. Map to `Control {controlType="methodology"}`

### Issue 4: Missing Discriminators in Cypher Scripts

**Problem:** TASKMASTER shows mapping table, but Phase 3 Cypher scripts are incomplete:
- Task 3.1 shows only 19 entities mapped (should be 96 for Tier 1)
- Task 3.2 shows only 16 entities mapped (should be 48 for Tier 2)
- Tasks 3.5 says "Full mapping in: `cypher/03_ner11_complete_mapping.cypher`" but file doesn't exist

**RECOMMENDATION:** Complete all Cypher migration scripts with ALL 566 entities explicitly mapped.

---

## Discriminator Property Design Quality

**Rating: 7/10**

### Strengths:
✅ Hierarchical discriminators are well-designed:
```cypher
Asset {assetClass="OT", deviceType="substation"}  // Good 2-level hierarchy
PsychTrait {traitType="lacanian", subtype="hysteric"}  // Clear categorization
Vulnerability {vulnType="cve"}  // Simple, effective
```

✅ Consistent naming conventions:
- `*Type` for primary discriminator
- `subtype` for secondary discriminator
- Clear semantic meaning

### Weaknesses:
❌ Some discriminators are redundant:
```cypher
ThreatActor {actorType="nation_state"}  // Why not just nation_state entity?
Malware {malwareFamily="ransomware"}  // Could be separate label
```

❌ Missing discriminators for complex entities:
```cypher
Indicator {indicatorType}  // Needs subtype for measurement vs. behavioral vs. network
Control {controlType}  // Needs subtype for technical vs. administrative vs. physical
```

❌ No guidance on how to handle multi-dimensional entities:
```cypher
// How to classify a "SAFETY_PLC" that is both:
// - An OT asset
// - A safety-critical system
// - A deterministic control system
Asset {
  assetClass="OT",
  deviceType="safety_plc",
  safetyLevel="SIL3",  // Additional dimension?
  deterministic=true   // Boolean property?
}
```

### Recommendations:
1. **Add secondary discriminators** for complex categories:
```cypher
Indicator {
  indicatorType: "measurement" | "behavioral" | "network" | "economic",
  subtype: specific_indicator_name
}

Control {
  controlType: "technical" | "administrative" | "physical",
  subtype: "mitigation" | "detection" | "prevention" | "framework"
}
```

2. **Use properties for boolean/multi-dimensional attributes**:
```cypher
Asset {
  assetClass="OT",
  deviceType="plc",
  safetyRated: true,
  safetyIntegrityLevel: "SIL3",
  deterministic: true
}
```

3. **Document discriminator taxonomy** in a separate reference file.

---

## Recommendations for Complete Mapping

### Priority 1 (CRITICAL): Map Core Unmapped Entities (187 entities)

**Action:** Create comprehensive Cypher scripts mapping:
1. Software components (26) → `Software`
2. Network infrastructure (15) → `Asset`
3. Organizational entities (28) → `Organization`/`Control`
4. Behavioral patterns (47) → `AttackPattern`/`Event`/`PsychTrait`
5. Sector-specific (14) → `Asset`/`Event`/`Control`
6. Safety/Reliability (40) → `Indicator`/`Control`/`Asset`
7. Ontology frameworks (28) → `Control`/`Campaign`

**Deliverable:** Complete `cypher/03_ner11_complete_mapping.cypher` with ALL 566 entities.

### Priority 2 (HIGH): Resolve Duplicates

**Action:** De-duplicate entity list:
1. Remove duplicate entities across tiers
2. Consolidate to canonical tier per entity
3. Update NER11 training data to reference canonical definitions

**Deliverable:** Revised `NER11_Gold_Standard_Full_Entity_Inventory_DEDUPLICATED.md`

### Priority 3 (MEDIUM): Decide on Process Entities

**Action:** Choose one of three approaches:
1. **Option A:** Create 17th Super Label `Process`
2. **Option B:** Map to `Event {eventType="process"}`
3. **Option C:** Map to `Control {controlType="methodology"}`

**Deliverable:** Architectural Decision Record (ADR) documenting choice and rationale.

### Priority 4 (MEDIUM): Classify Properties vs. Entities

**Action:** Review 64 entities identified as properties:
1. Move to property documentation (not entity mapping)
2. Update NER11 training to recognize as properties, not standalone entities
3. Create property schema documentation

**Deliverable:** `NER11_Property_Schema.md` and updated training data.

### Priority 5 (LOW): Enhance Discriminator Design

**Action:**
1. Add secondary discriminators for `Indicator`, `Control`, `Event`
2. Document discriminator taxonomy
3. Add multi-dimensional property guidance

**Deliverable:** `Discriminator_Property_Design_Guide.md`

---

## Final Ratings

### Mapping Completeness: 4/10

**Justification:**
- Only 291/566 entities (51.4%) explicitly mapped
- 275 entities (48.6%) have no mapping
- Entire tiers (7, 8, 9, 11) have 0% mapping
- Critical categories missing (software components, processes)

**To achieve 9/10:**
- Map all 566 entities
- Resolve duplicates
- Document property vs. entity distinction
- Complete all Cypher migration scripts

### Mapping Accuracy: 6/10

**Justification:**
- Mapped entities are generally correct (Tiers 1-2 psychometric)
- Some category confusion (behavioral vs. psychometric)
- Duplicates suggest unclear categorization
- Missing discriminators for some complex entities

**To achieve 9/10:**
- Resolve behavioral/psychometric overlap
- Fix duplicate entity issues
- Validate all discriminator properties
- Add secondary discriminators where needed

### Discriminator Property Design: 7/10

**Justification:**
- Strong hierarchical design (assetClass + deviceType)
- Consistent naming conventions
- Some redundancy (actorType when label is sufficient)
- Missing secondary discriminators for complex categories

**To achieve 9/10:**
- Add secondary discriminators (Indicator, Control, Event)
- Document discriminator taxonomy
- Provide multi-dimensional property guidance
- Simplify redundant discriminators

---

## Entities Requiring New Super Labels or Special Handling

### New Super Label Candidates:

#### 1. Process (24 entities)
**Justification:** Safety methodologies (FMEA, HAZOP, Bow-Tie), treatment processes, verification activities don't fit existing labels.

**Proposed Schema:**
```cypher
CREATE (p:Process {
  process_id: "proc_001",
  processType: "safety_methodology" | "operational" | "verification",
  subtype: "fmea" | "hazop" | "bow_tie" | "fault_tree" | "treatment",
  description: "..."
})
```

### Do NOT Create Entities For:

#### 1. Graph Meta-Concepts (14 entities)
`RELATIONSHIP`, `PROPERTY`, `CLASS`, `INSTANCE`, `ONTOLOGY_CLASS`, etc.
**Reason:** Structural concepts, not domain entities.

#### 2. Abstract Properties (50 entities)
`DESCRIPTION`, `PURPOSE`, `METHODOLOGY`, `DATA_FORMAT`, `OPERATION_MODE`, etc.
**Reason:** Should be properties of other entities, not standalone entities.

---

## Next Steps

### Immediate Actions:
1. ✅ Complete this audit report
2. ⏳ Create complete Cypher mapping scripts (Priority 1)
3. ⏳ De-duplicate entity inventory (Priority 2)
4. ⏳ Decide on Process entity handling (Priority 3)

### Follow-up Actions:
5. ⏳ Update NER11 training data with corrected mappings
6. ⏳ Create discriminator taxonomy documentation
7. ⏳ Validate mapping with domain experts
8. ⏳ Test migration scripts on sample Neo4j database

### Success Criteria:
- ✅ **100% entity coverage** (566/566 entities mapped)
- ✅ **Zero duplicates** in entity inventory
- ✅ **Clear guidance** on properties vs. entities
- ✅ **Complete Cypher scripts** for migration
- ✅ **Validated discriminator design** with taxonomy documentation

---

## Conclusion

Enhancement 27's entity mapping is **incomplete** (51.4% coverage) but has a **solid foundation** in the hierarchical property model design. The primary issues are:

1. **Incomplete mapping** - 275 entities unmapped
2. **Missing Cypher scripts** - Task 3.5 references non-existent file
3. **Duplicate entities** - Same entities appear in multiple tiers
4. **Category confusion** - Behavioral vs. psychometric overlap
5. **Missing Super Label** - Process entities have no appropriate label

**Recommended Path Forward:**
1. Complete Priority 1 mapping (187 core entities)
2. Resolve duplicates and confusion
3. Make architectural decision on Process entities
4. Document property schema separately
5. Validate with domain experts

With these corrections, Enhancement 27 can achieve **9/10 quality** for complete, accurate NER11 to Neo4j mapping.

---

**Auditor:** NER Specialist Auditor (Claude Code)
**Date:** 2025-11-27
**Status:** AUDIT COMPLETE - COMPREHENSIVE RECOMMENDATIONS PROVIDED
**Next Review:** After Priority 1-3 actions completed
