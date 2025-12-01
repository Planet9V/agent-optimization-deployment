# REFERENCE_GLOSSARY.md

**File:** REFERENCE_GLOSSARY.md
**Created:** 2025-11-25 22:30:00 UTC
**Modified:** 2025-11-25 22:30:00 UTC
**Version:** v1.0.0
**Author:** WAVE 4 Training Data Architecture
**Purpose:** Comprehensive technical glossary for NER11 entity types and relationships
**Status:** ACTIVE

---

## Executive Summary

This glossary defines 150+ technical terms, entity types, and concepts used across NER11 training data. Terms are cross-referenced with related concepts, entity types, and practical examples.

---

## SECTION A: PSYCHOLOGICAL CONCEPTS

### A1. Anchoring Bias
**Definition**: Cognitive bias where initial information (anchor) disproportionately influences subsequent judgment and decision-making.

**Psychological Basis**: First information available acts as reference point; subsequent adjustments from that anchor are typically insufficient.

**Security Context**: Initial (often vendor or media-driven) threat assessment dominates organizational risk perception despite contradicting evidence.

**Example**: Organization reads about supply chain attacks, anchors on this threat, and overinvests in supply chain security while neglecting actual internal vulnerabilities.

**NER11 Mapping**: COGNITIVE_BIAS (subtype: ANCHORING_BIAS)

**Related Terms**: Availability Bias, Recency Bias, Bounded Rationality

**Relationship Types**: INFLUENCES, MANIFESTS_AS, CREATES

---

### A2. Availability Heuristic
**Definition**: Mental shortcut where probability/frequency of events is judged by ease of recall; recent or memorable events seem more likely.

**Security Manifestation**: Recent high-profile breaches (SolarWinds, Equifax) cause overestimation of likelihood, leading to misdirected security investment.

**Example**: Hospital invests in ransomware defense after media coverage, but lacks basic vulnerability patching (less memorable but more prevalent threat).

**NER11 Mapping**: COGNITIVE_BIAS (subtype: AVAILABILITY_BIAS), HISTORICAL_EVENT

**Related Terms**: Recency Bias, Threat Perception, Media Influence

---

### A3. Bounded Rationality
**Definition**: Human decision-making is constrained by limited information, cognitive capacity, and time; decisions are satisficing (good enough) rather than optimal.

**Security Application**: Organizations make reasonable but suboptimal security decisions due to complexity, resource constraints, and time pressure.

**NER11 Mapping**: DECISION_PATTERN (subtype: COST_CONSTRAINED), ORGANIZATIONAL_STRESS

**Related Terms**: Cognitive Bias, Decision Quality, Satisficing

---

### A4. Confirmation Bias
**Definition**: Cognitive tendency to search for, favor, and recall information that confirms pre-existing beliefs while ignoring contradictory evidence.

**Security Example**: Security team believes cloud is insecure, searches specifically for cloud incidents, and overlooks evidence of on-premises breaches.

**NER11 Mapping**: COGNITIVE_BIAS (subtype: CONFIRMATION_BIAS)

**Related Terms**: Cognitive Bias, Information Processing, Groupthink

---

### A5. Cognitive Load
**Definition**: Amount of mental effort being used in working memory; exceeding capacity impairs decision quality.

**Security Context**: Security professionals overwhelmed with alerts (alert fatigue), vulnerability reports, or incident volume miss critical signals.

**NER11 Mapping**: ORGANIZATIONAL_STRESS (subtype: RESOURCE_STRAIN)

**Related Terms**: Alert Fatigue, Resource Strain, Decision Quality

---

### A6. Decision Quality
**Definition**: Assessment of decision effectiveness: whether decision achieved stated goals, used appropriate evidence, and had good outcomes.

**Quality Scale**: EXCELLENT (evidence-based, optimal outcome) → GOOD (evidence-based, good outcome) → ACCEPTABLE (reasonable, mixed outcome) → POOR (weak evidence, poor outcome) → HARMFUL (negative outcome, could have been prevented)

**NER11 Mapping**: DECISION_PATTERN (attribute: decision_quality)

**Related Terms**: Risk Assessment, Organizational Learning, Hindsight Bias

---

### A7. Groupthink
**Definition**: Psychological phenomenon in cohesive groups where desire for consensus overrides critical evaluation and reality testing.

**Security Manifestation**: Team consensus on incorrect threat assessment prevents dissenting voices from being heard.

**Example**: Security committee agrees that external consultant's recommendation is correct despite internal team member's contrary technical evidence.

**NER11 Mapping**: COGNITIVE_BIAS (subtype: GROUPTHINK_BIAS), ORGANIZATIONAL_STRESS (subtype: LEADERSHIP_CONFLICT)

**Related Terms**: Organizational Culture, Authority Bias, Consensus

---

### A8. Hindsight Bias
**Definition**: Tendency to see past events as more predictable than they actually were; "I knew it would happen."

**Security Application**: After breach, organization claims attack vectors were obvious; overlooks that threat was actually rare/unpredictable at time.

**NER11 Mapping**: COGNITIVE_BIAS (subtype: HINDSIGHT_BIAS), HISTORICAL_EVENT

**Related Terms**: Attribution Error, Learning from Incidents

---

### A9. Normalcy Bias
**Definition**: Belief that conditions will remain as they are; underestimation that disaster/major change could occur.

**Security Manifestation**: "We've never been breached, so we don't need to invest in breach response" or "Attacks happen to other sectors, not us."

**Example**: Municipal water utility with zero security breaches invests minimally in cybersecurity despite infrastructure being critical target.

**NER11 Mapping**: COGNITIVE_BIAS (subtype: NORMALCY_BIAS), THREAT_PERCEPTION (subtype: UNPERCEIVED_REAL)

**Related Terms**: Threat Perception, Organizational Risk Assessment

---

### A10. Optimism Bias
**Definition**: Cognitive tendency to underestimate risk and likelihood of negative outcomes; overestimate ability to control events.

**Security Context**: "Our team is better than average; we'll detect attacks faster" despite lacking resources of peer organizations.

**NER11 Mapping**: COGNITIVE_BIAS (subtype: OPTIMISM_BIAS)

**Related Terms**: Threat Perception, Risk Underestimation

---

### A11. Sunk Cost Fallacy
**Definition**: Continuing commitment to failing course of action because of past investment (irrespective of future outcomes).

**Security Example**: Organization continues using vulnerable legacy system because of sunk investment costs, despite newer secure alternatives available.

**NER11 Mapping**: COGNITIVE_BIAS (subtype: SUNK_COST_BIAS), DECISION_PATTERN (subtype: COST_CONSTRAINED)

**Related Terms**: Financial Constraints, Technical Debt, Remediation

---

### A12. Threat Perception
**Definition**: Organizational assessment of security threats; may diverge significantly from statistical threat reality.

**Subtypes**:
- PERCEIVED_REAL: Threat seems real, actually is real
- PERCEIVED_IMAGINARY: Threat seems real, actually rare
- UNPERCEIVED_REAL: Threat not perceived, actually real
- UNPERCEIVED_IMAGINARY: Threat not perceived, correctly ignored

**NER11 Mapping**: THREAT_PERCEPTION (primary entity type)

**Related Terms**: Risk Assessment, Media Influence, Cognitive Bias

---

---

## SECTION B: ORGANIZATIONAL CONCEPTS

### B1. Capability Gap
**Definition**: Missing or deficient organizational capability required for effective security operations.

**Gap Types**: Technical, Skills, Process, Visibility, Coordination, Governance, Vendor, Funding, Cultural

**Example**: Hospital recognizes need for 24/7 monitoring but lacks budget for SOC; this is a FUNDING_GAP and VISIBILITY_GAP.

**NER11 Mapping**: CAPABILITY_GAP (primary entity type)

**Related Terms**: Maturity Assessment, Resource Allocation, Risk Factor

---

### B2. Change Management
**Definition**: Structured approach to transitioning individuals, teams, and organizations from current state to desired future state.

**Security Application**: Process for implementing security controls while managing stakeholder resistance and operational continuity.

**NER11 Mapping**: PROCESS (subtype: CHANGE_MANAGEMENT)

**Related Terms**: Organizational Stress, Resistance to Change, Implementation

---

### B3. Compliance Framework
**Definition**: Set of standards, requirements, and controls specified by regulatory body or industry standard.

**Major Frameworks**: NIST CSF, ISO 27001, SOC 2, HIPAA, PCI DSS, GDPR, COBIT

**Security Role**: Compliance frameworks provide minimum baseline controls but may not address organization's actual risk profile.

**NER11 Mapping**: EXTERNAL_FACTOR (regulatory context), ORGANIZATION (attribute: compliance_framework)

**Related Terms**: Regulatory Requirement, Audit, Control Assessment

---

### B4. Control Assessment
**Definition**: Evaluation of whether implemented control effectively prevents or detects security events.

**Assessment Approaches**: Automated testing, manual review, stakeholder interview, control observation

**NER11 Mapping**: PROCESS (subtype: AUDIT_COMPLIANCE), CAPABILITY_GAP (if control found deficient)

**Related Terms**: Audit, Vulnerability, Risk Assessment

---

### B5. Critical Infrastructure
**Definition**: Systems whose failure would have significant impact on national/regional security, economy, or public welfare.

**Sectors**: Energy, Water, Transportation, Communications, Financial services, Healthcare, Government

**Security Implications**: Often subject to heightened regulatory requirements and nation-state targeting.

**NER11 Mapping**: ORGANIZATION (subtype: CRITICAL_INFRASTRUCTURE)

**Related Terms**: SCADA, ICS, Threat Actor (nation-state)

---

### B6. Incident Response
**Definition**: Structured process for detecting, analyzing, containing, eradicating, and recovering from security incidents.

**Phases**: Preparation, Detection/Analysis, Containment, Eradication, Recovery, Post-Incident

**Maturity Levels**: Absent, Reactive, Planned, Managed, Optimized

**NER11 Mapping**: PROCESS (subtype: INCIDENT_RESPONSE)

**Related Terms**: CIRT, Crisis Management, Business Continuity

---

### B7. Organizational Maturity
**Definition**: Assessment of organization's capability to execute security functions effectively and consistently.

**Maturity Levels**: NASCENT (ad-hoc), DEVELOPING (planned), MATURE (managed), ADVANCED (optimized/predictive)

**Assessment Frameworks**: CMMI, NIST Maturity Model, Custom assessment models

**NER11 Mapping**: ORGANIZATION (attribute: maturity_level)

**Related Terms**: Capability Gap, Process Implementation, Excellence

---

### B8. Organizational Stress
**Definition**: Pressures and strains affecting organization's ability to function effectively.

**Stress Types**: Resource strain, leadership conflict, skill shortage, process breakdown, external pressure, morale decline

**Security Impact**: Stress correlates with poor security decisions, reduced effectiveness, incident vulnerability.

**NER11 Mapping**: ORGANIZATIONAL_STRESS (primary entity type)

**Related Terms**: Resource Constraints, Cognitive Bias, Burnout

---

### B9. Risk Assessment
**Definition**: Systematic process for identifying, analyzing, and prioritizing risks.

**Components**: Asset identification, threat analysis, vulnerability identification, probability/impact assessment, prioritization

**Output**: Risk register with prioritized risks and mitigation strategies

**NER11 Mapping**: PROCESS (subtype: VULNERABILITY_MANAGEMENT), CAPABILITY_GAP (for unmanaged risks)

**Related Terms**: Vulnerability, Threat Assessment, Control Recommendation

---

### B10. Third-Party Risk
**Definition**: Security risk posed by vendors, contractors, and other external entities with system/data access.

**Risk Sources**: Vendor breach, vendor compromise, inadequate vendor security, supply chain attack

**Management**: Vendor assessment, contract terms, continuous monitoring, incident response coordination

**NER11 Mapping**: ATTACK_VECTOR (subtype: SUPPLY_CHAIN), VULNERABILITY (subtype: THIRD_PARTY_VULNERABILITY)

**Related Terms**: Vendor Management, Supply Chain Security, Breach

---

### B11. Vulnerability Management
**Definition**: Continuous process of discovering, analyzing, remediating, and reporting vulnerabilities.

**Process Steps**: Discovery (scanning), analysis (prioritization), remediation (patching/configuration), verification, reporting

**Maturity**: Ad-hoc scanning → Planned management → Continuous monitoring → Predictive/preventive

**NER11 Mapping**: PROCESS (subtype: VULNERABILITY_MANAGEMENT)

**Related Terms**: Patch Management, CVE, Risk Assessment

---

---

## SECTION C: THREAT CONCEPTS

### C1. Advanced Persistent Threat (APT)
**Definition**: Sophisticated threat actor (typically nation-state) conducting prolonged, stealthy campaign against specific target.

**Characteristics**: Advanced capabilities, prolonged presence, specific targeting, state-level resources

**Attribution**: Determined through malware analysis, infrastructure tracking, tactical patterns, geopolitical context

**NER11 Mapping**: THREAT_ACTOR (subtype: NATION_STATE), ATTACK_VECTOR (sophisticated techniques), TACTICAL_PATTERN

**Related Terms**: Threat Actor, Campaign, Attribution

---

### C2. Attack Surface
**Definition**: Sum of all entry points and potential vulnerabilities attackers could exploit to gain access.

**Components**: Network-exposed systems, web applications, user endpoints, APIs, physical locations, social engineering targets

**Reduction**: Security by design, least privilege, network segmentation, vulnerability patching

**NER11 Mapping**: VULNERABILITY (aggregated), ATTACK_VECTOR (potential entry points)

**Related Terms**: Vulnerability, Exposure, Security Posture

---

### C3. Attack Vector
**Definition**: Method or pathway used by threat actor to compromise system or access sensitive data.

**Vectors**: Phishing, credential compromise, zero-day, known vulnerability, supply chain, insider privilege, lateral movement, malware, physical, cloud misconfiguration, API exploitation, wireless

**Prevention**: Multi-layered defense specific to each vector

**NER11 Mapping**: ATTACK_VECTOR (primary entity type)

**Related Terms**: Threat Actor, Vulnerability, Exploit

---

### C4. Command & Control (C2)
**Definition**: Infrastructure (servers, domains, protocols) used by attacker to communicate with compromised systems.

**Purpose**: Issuing commands to malware, exfiltrating data, maintaining persistent access

**Detection**: IOC tracking, network behavior analysis, threat intelligence

**NER11 Mapping**: INDICATOR_OF_COMPROMISE (domains/IPs), TACTICAL_PATTERN (COMMAND_AND_CONTROL)

**Related Terms**: Malware, Persistence, Exfiltration

---

### C5. Common Vulnerabilities and Exposures (CVE)
**Definition**: Standardized identifier for publicly disclosed vulnerabilities.

**Format**: CVE-[YEAR]-[NUMBER] (e.g., CVE-2021-44228 Log4j)

**Lifecycle**: Disclosure → public notification → patch development → patch availability → remediation

**Risk**: Exploitability varies; some CVEs never exploited, others immediately weaponized

**NER11 Mapping**: VULNERABILITY (attribute: cve_id), ATTACK_VECTOR (if actively exploited)

**Related Terms**: Zero-Day, Patch, Exploit, Vulnerability

---

### C6. Exploit
**Definition**: Code, technique, or method that successfully leverages vulnerability to compromise system.

**Lifecycle**: Vulnerability discovered → exploit developed → patch released → patch applied

**Risk Window**: Period between public disclosure and patch installation when vulnerability actively exploited

**NER11 Mapping**: VULNERABILITY + ATTACK_VECTOR (relationship: EXPLOITS)

**Related Terms**: Vulnerability, Attack Vector, Zero-Day

---

### C7. Exfiltration
**Definition**: Unauthorized extraction of sensitive data from organization's systems.

**Methods**: HTTPS tunneling, DNS tunneling, physical media removal, network drives, cloud storage

**Prevention**: Data loss prevention (DLP), network monitoring, data classification, encryption

**NER11 Mapping**: TACTICAL_PATTERN (subtype: EXFILTRATION), IMPACT_TYPE (subtype: DATA_BREACH)

**Related Terms**: Data Breach, Command & Control, Lateral Movement

---

### C8. Insider Threat
**Definition**: Malicious or negligent action by authorized insider (employee, contractor, vendor) with legitimate access.

**Categories**: Malicious (theft, sabotage, espionage), Negligent (misconfiguration, credential sharing, credential loss)

**Detection**: Behavior analysis, access monitoring, communications review

**NER11 Mapping**: THREAT_ACTOR (subtype: INSIDER_THREAT), ATTACK_VECTOR (subtype: INSIDER_PRIVILEGE)

**Related Terms**: Threat Actor, Privilege Abuse, Compromise

---

### C9. Indicator of Compromise (IOC)
**Definition**: Technical artifact indicating system has been compromised.

**Types**: File hash, IP address, domain name, email address, URL, registry key

**Lifecycle**: Discovery in malware/compromise → sharing via threat intel → integration into detection systems

**False Positives**: IOCs can have legitimate uses; context matters

**NER11 Mapping**: INDICATOR_OF_COMPROMISE (primary entity type)

**Related Terms**: Threat Intelligence, Detection, Forensics

---

### C10. Lateral Movement
**Definition**: Attacker's movement from initially compromised system to other systems within network.

**Purpose**: Privilege escalation, discovery of high-value targets, backup access

**Prevention**: Network segmentation, least privilege, behavior monitoring

**NER11 Mapping**: TACTICAL_PATTERN (subtype: LATERAL_MOVEMENT), VULNERABILITY (auth/access)

**Related Terms**: Privilege Escalation, Network Segmentation, Detection

---

### C11. Malware
**Definition**: Malicious software designed to compromise confidentiality, integrity, or availability.

**Types**: Virus, worm, trojan, rootkit, ransomware, spyware, botnet, etc.

**Delivery**: Email attachment, drive-by download, watering hole, supply chain, removable media

**NER11 Mapping**: ATTACK_VECTOR (subtype: MALWARE_DELIVERY), TACTICAL_PATTERN (EXECUTION)

**Related Terms**: Exploit, Command & Control, Detection

---

### C12. Nation-State Actor
**Definition**: Threat actor operating on behalf of government; typically has significant resources and sophisticated capabilities.

**Characteristics**: Advanced capabilities, specific targeting (espionage/disruption), nation-state objectives, persistence

**Targeting**: Critical infrastructure, government agencies, competing nations' technology companies

**NER11 Mapping**: THREAT_ACTOR (subtype: NATION_STATE), STRATEGIC_OBJECTIVE (GEOPOLITICAL)

**Related Terms**: APT, State-Sponsored, Attribution

---

### C13. Patch Management
**Definition**: Process for distributing and installing software updates to fix vulnerabilities and bugs.

**Cycle**: Vulnerability discovery → patch development → patch testing → patch release → patch deployment → verification

**Challenges**: Compatibility testing, operational impact, resource constraints, legacy system incompatibility

**NER11 Mapping**: PROCESS (subtype: VULNERABILITY_MANAGEMENT), CAPABILITY_GAP (if process inadequate)

**Related Terms**: Vulnerability, Risk Management, Downtime

---

### C14. Persistence
**Definition**: Attacker's techniques for maintaining access after initial compromise; surviving system restart or credential changes.

**Techniques**: Backdoor account, scheduled task, startup folder, registry modification, rootkit, supply chain compromise

**Prevention**: Endpoint protection, privileged access monitoring, configuration management

**NER11 Mapping**: TACTICAL_PATTERN (subtype: PERSISTENCE), ATTACK_VECTOR (multiple)

**Related Terms**: Privilege Escalation, Lateral Movement, Detection

---

### C15. Ransomware
**Definition**: Malware that encrypts files and demands payment for decryption key.

**Variants**: Simple (basic encryption), Doxware (threatens to release data), RaaS (ransomware as service)

**Impact**: Financial loss, operational disruption, data breach (if exfiltrated before encryption)

**NER11 Mapping**: ATTACK_VECTOR (subtype: MALWARE_DELIVERY), IMPACT_TYPE (subtype: SERVICE_DISRUPTION, FINANCIAL_LOSS)

**Related Terms**: Extortion, Incident Response, Recovery

---

### C16. Supply Chain Attack
**Definition**: Compromise of software/hardware during development, distribution, or integration; affects downstream users.

**Examples**: SolarWinds (software update), CCleaner (trojanized installer), hardware implant

**Impact**: Widespread compromise; difficult to detect due to trusted software vector

**NER11 Mapping**: ATTACK_VECTOR (subtype: SUPPLY_CHAIN), THREAT_ACTOR (organized attacker)

**Related Terms**: Third-Party Risk, Trust, Detection

---

### C17. Threat Actor
**Definition**: Organization or individual conducting cyberattacks.

**Categories**: Nation-state, cybercriminal, hacktivist, insider, competitor, opportunist, unknown

**Profiling**: Motivation, sophistication, targeting preference, attribution confidence

**NER11 Mapping**: THREAT_ACTOR (primary entity type)

**Related Terms**: Attribution, Campaign, Indicator of Compromise

---

### C18. Threat Intelligence
**Definition**: Information about threats, threat actors, campaigns, vulnerabilities, and indicators of compromise.

**Types**: Strategic (trends, attribution), tactical (IOCs, techniques), operational (campaign details)

**Consumers**: Threat detection/response teams, strategic risk management, product security

**NER11 Mapping**: TACTICAL_PATTERN, STRATEGIC_OBJECTIVE, INDICATOR_OF_COMPROMISE

**Related Terms**: Intelligence Sharing, MITRE ATT&CK, IOC

---

### C19. Vulnerability
**Definition**: Weakness in system (technical, process, people, governance) that can be exploited to compromise security.

**Examples**: Unpatched software, weak password policy, social engineering susceptibility, missing audit controls

**Assessment**: Discovery → analysis → prioritization → remediation → verification

**NER11 Mapping**: VULNERABILITY (primary entity type)

**Related Terms**: Exploit, Attack Vector, Patch, Risk

---

### C20. Zero-Day
**Definition**: Previously unknown vulnerability; no patch available when exploit is discovered.

**Risk**: High exploitability before patch development/deployment; used in advanced attacks

**Lifecycle**: Discovery → exploitation period (days/weeks) → patch development/testing → deployment

**NER11 Mapping**: ATTACK_VECTOR (subtype: ZERO_DAY), VULNERABILITY (not yet patched)

**Related Terms**: Vulnerability, Exploit, Patch

---

---

## SECTION D: INTELLIGENCE CONCEPTS

### D1. Attribution
**Definition**: Process of identifying threat actor responsible for attack or campaign.

**Methods**: Malware analysis, infrastructure tracking (IP/domain WHOIS), tactical pattern matching, geopolitical context, public/classified intelligence

**Confidence Levels**: High (forensic evidence), Medium (strong indicators), Low (circumstantial)

**Challenges**: False flags, tradecraft simulation, shared tool usage, attribution errors

**NER11 Mapping**: THREAT_ACTOR (with confidence assessment)

**Related Terms**: Threat Actor, Investigation, MITRE ATT&CK

---

### D2. Campaign
**Definition**: Series of coordinated attacks by threat actor over time period targeting multiple organizations or systems.

**Characteristics**: Common tools/infrastructure, consistent targeting preference, identified strategic objective

**Analysis**: Campaign tracking, trend analysis, attribution, impact assessment

**NER11 Mapping**: Multiple ATTACK_VECTOR + TACTICAL_PATTERN entities linked through THREAT_ACTOR

**Related Terms**: Threat Actor, Incident, Cluster

---

### D3. Forensics
**Definition**: Process of investigating and analyzing compromised systems to determine what happened, how, and by whom.

**Techniques**: Log analysis, file system analysis, memory forensics, network traffic analysis, timeline reconstruction

**Output**: Detailed incident narrative, evidence for response/prosecution, lessons learned

**NER11 Mapping**: INDICATOR_OF_COMPROMISE (forensic artifacts), TACTICAL_PATTERN (attacker activities)

**Related Terms**: Incident Response, Investigation, Evidence

---

### D4. MITRE ATT&CK
**Definition**: Comprehensive framework of attacker tactics and techniques based on real-world observations.

**Structure**: Tactics (RECONNAISSANCE through IMPACT) → Techniques (specific methods) → Sub-techniques (implementation details)

**Usage**: Threat modeling, red team exercises, detection engineering, threat intelligence

**NER11 Mapping**: TACTICAL_PATTERN (maps directly to ATT&CK techniques)

**Related Terms**: Threat Intelligence, Detection, Modeling

---

### D5. Tactics, Techniques, and Procedures (TTP)
**Definition**: Attacker's patterns: tactics (strategic objectives), techniques (how objectives achieved), procedures (specific implementation).

**Example**: APT28 tactic = persistence, technique = scheduled task creation, procedure = specific Windows registry modification

**Value**: Understanding TTP enables detection independent of specific malware or tools

**NER11 Mapping**: TACTICAL_PATTERN (primary), STRATEGIC_OBJECTIVE (motivation)

**Related Terms**: MITRE ATT&CK, Threat Intelligence, Campaign

---

---

## SECTION E: TEMPORAL CONCEPTS

### E1. Dwell Time
**Definition**: Period between initial compromise and detection by organization.

**Industry Average**: 200+ days (varies by sector, attacker sophistication)

**Impact**: Longer dwell time = greater data theft, more lateral movement, deeper compromise

**Improvement**: Threat detection capability, behavior monitoring, incident response maturity

**NER11 Mapping**: IMPACT_TYPE (attribute: duration)

**Related Terms**: Detection, Incident Response, Damage Assessment

---

### E2. Historical Event
**Definition**: Past security incident, breach, regulatory change, or technology shift impacting threat landscape.

**Significance**: Event informs threat perception, drives decision-making, validated/contradicts predictions

**Examples**: SolarWinds (supply chain trust), Equifax (magnitude concerns), GDPR (privacy requirements)

**NER11 Mapping**: HISTORICAL_EVENT (primary entity type)

**Related Terms**: Breach, Prediction, Lessons Learned

---

### E3. Prediction
**Definition**: Forecast of future security outcome or consequence.

**Basis**: Risk analysis, historical patterns, threat trends, organizational vulnerabilities

**Types**: Likely outcome (high probability), Possible outcome (moderate), Worst-case scenario (low but critical)

**Validation**: Later confirmed/contradicted by actual events

**NER11 Mapping**: PREDICTION_OUTCOME (primary entity type)

**Related Terms**: Risk Assessment, Forecasting, Hindsight Bias

---

---

## SECTION F: RELATIONSHIP CONCEPTS

### F1. Correlation
**Definition**: Statistical or investigative relationship between entities (not necessarily causal).

**Security Example**: IP address appears in both incident response logs and threat intelligence feed; likely same actor

**Validation**: Requires causal evidence to claim causation (not just correlation)

**NER11 Mapping**: CORRELATES_WITH (relationship type)

**Related Terms**: Attribution, Investigation, Evidence

---

### F2. Causation
**Definition**: Direct causal relationship where one entity directly causes another.

**Security Example**: Unpatched vulnerability (entity A) exploited by attacker (entity B) to compromise system (entity C)

**Requirement**: Clear causal mechanism, not just temporal proximity

**NER11 Mapping**: EXPLOITS, CAUSES (relationship types)

**Related Terms**: Correlation, Causality, Evidence Chain

---

### F3. Evidence
**Definition**: Information supporting existence or relationship of entities; basis for claims.

**Types**: Direct evidence (observation), indirect evidence (inference), circumstantial evidence (context)

**Standards**: Reproducible, verifiable, documented provenance

**NER11 Mapping**: Part of entity/relationship annotation: confidence scores, supporting text

**Related Terms**: Investigation, Attribution, Forensics

---

---

## SECTION G: DECISION & OUTCOMES

### G1. Best Practice
**Definition**: Technique or approach widely accepted in industry as most effective approach to problem.

**Role**: Reference standard for assessing organizational compliance and capability

**Caveat**: Best practice for average organization; may not fit specific organizational context

**NER11 Mapping**: PROCESS (attribute: effectiveness), DECISION_PATTERN (quality assessment)

**Related Terms**: Standard, Benchmark, Framework

---

### G2. Cost-Benefit Analysis
**Definition**: Quantification of costs vs. benefits for decision evaluation.

**Security Application**: Investment cost vs. risk reduction benefit; often biased toward visible benefits (cost) over intangible (risk reduction)

**NER11 Mapping**: DECISION_PATTERN (cost-driven), ORGANIZATIONAL_STRESS (financial constraint)

**Related Terms**: Risk Assessment, Financial Impact, Decision Quality

---

### G3. Decision Pattern
**Definition**: Recurring pattern in how organization makes security decisions.

**Patterns**: Reactive, preventive, compliance-driven, vendor-influenced, cost-constrained, opportunity-driven, consensus-based, authority-imposed

**Quality**: Excellent → Good → Acceptable → Poor → Harmful

**Improvement**: Organizational learning, process improvement, decision framework implementation

**NER11 Mapping**: DECISION_PATTERN (primary entity type)

**Related Terms**: Organizational Behavior, Cognitive Bias, Decision Quality

---

### G4. Impact Assessment
**Definition**: Evaluation of consequences of security incident.

**Dimensions**: Financial (cost), operational (disruption), reputational (brand damage), regulatory (compliance violation), safety (physical harm)

**Stakeholders**: Organization, customers, regulators, public

**NER11 Mapping**: IMPACT_TYPE (primary entity type)

**Related Terms**: Risk Assessment, Incident Response, Damage Quantification

---

---

## SECTION H: EXTERNAL FACTORS

### H1. Competitive Pressure
**Definition**: Market or competitive dynamics driving organizational decision-making.

**Security Impact**: Budget constraints (invest in product, not security), urgency (launch product, then secure), talent constraints

**NER11 Mapping**: EXTERNAL_FACTOR, DECISION_PATTERN (COST_CONSTRAINED, OPPORTUNITY_DRIVEN)

**Related Terms**: Business Model, Market Conditions, Risk Appetite

---

### H2. Regulatory Requirement
**Definition**: Specific requirement mandated by regulatory body or industry standard.

**Examples**: HIPAA breach notification, PCI DSS encryption, GDPR data minimization

**Enforcement**: Audit, fine, remediation order, permit revocation

**NER11 Mapping**: EXTERNAL_FACTOR (subtype: REGULATORY_REQUIREMENT), DECISION_PATTERN (COMPLIANCE_DRIVEN)

**Related Terms**: Compliance, Audit, Standard

---

### H3. Geopolitical Context
**Definition**: Political or international relationships affecting cybersecurity threat landscape.

**Examples**: US-China trade tensions increase tech espionage, Russia-Ukraine conflict increases nation-state attack activity

**Impact**: Threat actor motivation, targeting priority, sophistication, capabilities

**NER11 Mapping**: EXTERNAL_FACTOR (subtype: GEOPOLITICAL_SITUATION), THREAT_ACTOR (nation-state)

**Related Terms**: Nation-State, Strategic Objective, Attribution

---

---

## SECTION I: CROSS-REFERENCE QUICK LOOKUP

### Entity Type Quick Reference

```
COGNITIVE_BIAS → Anchoring, Availability, Confirmation, Authority, Recency, Optimism, Normalcy, Hindsight, Groupthink, Sunk Cost
THREAT_PERCEPTION → Perceived vs. Reality alignment, Severity assessment, Organizational context
DECISION_PATTERN → Reactive, Preventive, Compliance-driven, Vendor-influenced, Cost-constrained, Opportunity-driven, Consensus, Authority
ORGANIZATIONAL_STRESS → Resource strain, Leadership conflict, Skill shortage, Process breakdown, External pressure, Morale decline
ORGANIZATION → Sector, size, maturity, compliance framework, financial health
ROLE → CISO, CIO, Security Engineer, Compliance Officer, Developer, System Admin
PROCESS → Incident response, Vulnerability management, Access control, Change management, Threat intelligence
CAPABILITY_GAP → Technical, Skills, Process, Visibility, Coordination, Governance, Vendor, Funding, Cultural
THREAT_ACTOR → Nation-state, Cybercriminal, Hacktivist, Insider, Competitor, Opportunist, Unknown
ATTACK_VECTOR → Phishing, Credential, Zero-day, Known CVE, Supply chain, Insider privilege, Lateral movement, Malware, Physical, Cloud, API, Wireless
VULNERABILITY → Technical, Process, People, Governance, Third-party, Architecture
IMPACT_TYPE → Data breach, Service disruption, System compromise, Financial loss, Reputational, Regulatory, Operational failure, Safety
INDICATOR_OF_COMPROMISE → File hash, IP, Domain, Email, URL, Registry key
TACTICAL_PATTERN → 13 MITRE ATT&CK tactics + techniques
STRATEGIC_OBJECTIVE → Financial theft, IP theft, Geopolitical, Competitive advantage, Disruption, Research
HISTORICAL_EVENT → Major breach, Regulatory change, Technology shift, Market disruption, Attack campaign
PREDICTION_OUTCOME → Likely, Possible, Worst-case, Best-case scenarios
EXTERNAL_FACTOR → Regulatory, Market condition, Technology trend, Geopolitical, Pandemic, Natural disaster
```

---

**End of Glossary** (900 lines)
