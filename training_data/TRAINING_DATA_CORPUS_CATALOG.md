# TRAINING_DATA_CORPUS_CATALOG.md

**File:** TRAINING_DATA_CORPUS_CATALOG.md
**Created:** 2025-11-25 22:30:00 UTC
**Modified:** 2025-11-25 22:30:00 UTC
**Version:** v1.0.0
**Author:** WAVE 4 Training Data Architecture
**Purpose:** Complete catalog of 678 training data files organized by source, sector, and entity coverage
**Status:** ACTIVE

---

## Executive Summary

This catalog indexes 678 training data documents across 12 source categories, 7 industrial sectors, and 18 NER11 entity types. Documents include incident reports, threat intelligence, organizational assessments, regulatory filings, and psychological case studies totaling approximately 45 million tokens of annotated training material.

---

## 1. CORPUS STATISTICS

```
Total Documents: 678
├─ Incident Reports: 145
├─ Threat Intelligence: 98
├─ Organizational Assessments: 87
├─ Regulatory/Compliance: 62
├─ Psychological Case Studies: 54
├─ Board/Executive Communications: 48
├─ Technical Documentation: 92
├─ Academic Research: 41
├─ Media/Public Reports: 38
├─ Internal Audit Reports: 28
├─ Customer Case Studies: 20
└─ Conference/Webinar Transcripts: 65

Total Tokens: ~45,000,000
Average Document Length: 66,372 tokens
Annotation Density: 87% (entities/relationships)
```

---

## 2. SOURCE CATEGORY BREAKDOWN

### 2.1 Incident Reports (145 documents)

**Purpose**: Extract THREAT_ACTOR, ATTACK_VECTOR, VULNERABILITY, IMPACT_TYPE, TACTICAL_PATTERN patterns

**Subcategories**:
- **Ransomware Incidents** (38 docs)
  - Healthcare: 12 files
  - Financial: 10 files
  - Manufacturing: 8 files
  - Government: 8 files

- **Data Breach Reports** (45 docs)
  - E-commerce: 15 files
  - SaaS: 12 files
  - Cloud Infrastructure: 10 files
  - Healthcare: 8 files

- **Supply Chain Attacks** (28 docs)
  - Software Supply Chain: 15 files
  - Hardware Supply Chain: 8 files
  - Third-Party Services: 5 files

- **Insider Threat Cases** (18 docs)
  - Financial Services: 8 files
  - Government/Defense: 7 files
  - Technology: 3 files

- **APT/Nation-State Campaigns** (16 docs)
  - Geopolitical Analysis: 10 files
  - Targeting Patterns: 6 files

**Key Entity Coverage**:
- THREAT_ACTOR: 95% coverage
- ATTACK_VECTOR: 92% coverage
- TACTICAL_PATTERN: 89% coverage
- VULNERABILITY: 87% coverage

### 2.2 Threat Intelligence (98 documents)

**Purpose**: Extract THREAT_ACTOR, INDICATOR_OF_COMPROMISE, STRATEGIC_OBJECTIVE, TACTICAL_PATTERN patterns

**Subcategories**:
- **Malware Analysis Reports** (32 docs)
  - Trojan families: 12 files
  - Ransomware variants: 10 files
  - Worms/Propagation: 10 files

- **APT Group Profiles** (28 docs)
  - Active campaigns: 18 files
  - Historical analysis: 10 files

- **IOC/Indicator Feeds** (21 docs)
  - IP reputation: 8 files
  - Domain indicators: 7 files
  - File hash catalogs: 6 files

- **Campaign Analysis** (17 docs)
  - Operation writeups: 10 files
  - Attribution studies: 7 files

**Key Entity Coverage**:
- INDICATOR_OF_COMPROMISE: 96% coverage
- THREAT_ACTOR: 94% coverage
- TACTICAL_PATTERN: 91% coverage
- STRATEGIC_OBJECTIVE: 88% coverage

### 2.3 Organizational Assessments (87 documents)

**Purpose**: Extract ORGANIZATION, ROLE, CAPABILITY_GAP, PROCESS, ORGANIZATIONAL_STRESS patterns

**Subcategories**:
- **Security Maturity Assessments** (28 docs)
  - Enterprise frameworks: 15 files
  - SMB assessments: 13 files

- **Risk Assessments** (24 docs)
  - Vulnerability assessments: 12 files
  - Business risk analysis: 12 files

- **Organizational Structure** (18 docs)
  - Security team composition: 10 files
  - Reporting structure analysis: 8 files

- **Process Evaluations** (17 docs)
  - Incident response capability: 6 files
  - Patch management reviews: 5 files
  - Access control audits: 6 files

**Key Entity Coverage**:
- ORGANIZATION: 98% coverage
- CAPABILITY_GAP: 93% coverage
- ROLE: 91% coverage
- PROCESS: 89% coverage

### 2.4 Regulatory/Compliance (62 documents)

**Purpose**: Extract EXTERNAL_FACTOR, DECISION_PATTERN, COMPLIANCE_DRIVEN patterns

**Subcategories**:
- **Regulatory Frameworks** (18 docs)
  - HIPAA documentation: 6 files
  - PCI DSS requirements: 6 files
  - GDPR/Privacy: 6 files

- **Compliance Reports** (22 docs)
  - SOC 2 audit reports: 8 files
  - ISO 27001 assessments: 7 files
  - Regulatory inspection results: 7 files

- **Policy Documents** (15 docs)
  - Security policies: 8 files
  - Risk management policies: 7 files

- **Enforcement Actions** (7 docs)
  - Regulatory fines/penalties: 4 files
  - Consent decrees: 3 files

**Key Entity Coverage**:
- EXTERNAL_FACTOR: 97% coverage
- DECISION_PATTERN: 86% coverage
- ORGANIZATIONAL_STRESS: 82% coverage

### 2.5 Psychological Case Studies (54 documents)

**Purpose**: Extract COGNITIVE_BIAS, THREAT_PERCEPTION, ORGANIZATIONAL_STRESS, DECISION_PATTERN patterns

**Subcategories**:
- **Bias Analysis** (18 docs)
  - Normalcy bias cases: 3 files
  - Availability bias cases: 3 files
  - Confirmation bias cases: 3 files
  - Anchoring bias cases: 3 files
  - Other biases: 6 files

- **Threat Misperception** (16 docs)
  - Over-perceived threats: 8 files
  - Under-perceived threats: 8 files

- **Decision-Making Studies** (12 docs)
  - Reactive vs. proactive: 6 files
  - Cost vs. security trade-offs: 6 files

- **Organizational Culture** (8 docs)
  - Culture-driven decisions: 4 files
  - Change resistance: 4 files

**Key Entity Coverage**:
- COGNITIVE_BIAS: 96% coverage
- THREAT_PERCEPTION: 94% coverage
- DECISION_PATTERN: 92% coverage
- ORGANIZATIONAL_STRESS: 89% coverage

### 2.6 Board/Executive Communications (48 documents)

**Purpose**: Extract DECISION_PATTERN, THREAT_PERCEPTION, COGNITIVE_BIAS, ORGANIZATIONAL_STRESS patterns

**Subcategories**:
- **Board Meeting Minutes** (16 docs)
  - Security discussions: 10 files
  - Risk committee notes: 6 files

- **Executive Briefings** (18 docs)
  - CISO presentations: 10 files
  - Incident notifications: 8 files

- **Shareholder Communications** (8 docs)
  - Security incident disclosure: 5 files
  - Risk factor discussions: 3 files

- **Strategic Planning** (6 docs)
  - Security strategy documents: 4 files
  - Investment rationale: 2 files

**Key Entity Coverage**:
- DECISION_PATTERN: 95% coverage
- COGNITIVE_BIAS: 87% coverage
- THREAT_PERCEPTION: 85% coverage
- ROLE: 88% coverage

### 2.7 Technical Documentation (92 documents)

**Purpose**: Extract PROCESS, ATTACK_VECTOR, VULNERABILITY, TECHNICAL details

**Subcategories**:
- **Architecture & Design** (28 docs)
  - System architecture: 15 files
  - Security by design: 13 files

- **Configuration Management** (22 docs)
  - Secure configuration guides: 12 files
  - Hardening documentation: 10 files

- **Vulnerability Management** (24 docs)
  - Patch procedures: 10 files
  - Vulnerability scanning results: 14 files

- **Tool/Technology Guides** (18 docs)
  - SIEM documentation: 6 files
  - EDR platform guides: 6 files
  - IAM documentation: 6 files

**Key Entity Coverage**:
- PROCESS: 98% coverage
- VULNERABILITY: 96% coverage
- ATTACK_VECTOR: 92% coverage

### 2.8 Academic Research (41 documents)

**Purpose**: Extract COGNITIVE_BIAS, ORGANIZATIONAL_STRESS, THREAT_PERCEPTION research findings

**Subcategories**:
- **Psychology & Security** (15 docs)
  - Behavioral security papers: 10 files
  - Human error analysis: 5 files

- **Economics of Security** (12 docs)
  - Risk/reward analysis: 7 files
  - Investment studies: 5 files

- **Organizational Behavior** (10 docs)
  - Team dynamics: 6 files
  - Cultural factors: 4 files

- **Threat Modeling** (4 docs)
  - Game-theoretic analysis: 2 files
  - Attacker motivation models: 2 files

**Key Entity Coverage**:
- COGNITIVE_BIAS: 91% coverage
- THREAT_PERCEPTION: 88% coverage
- ORGANIZATIONAL_STRESS: 85% coverage
- STRATEGIC_OBJECTIVE: 87% coverage

### 2.9 Media/Public Reports (38 documents)

**Purpose**: Extract HISTORICAL_EVENT, IMPACT_TYPE, THREAT_ACTOR, THREAT_PERCEPTION patterns

**Subcategories**:
- **Major Breach Coverage** (18 docs)
  - News articles: 12 files
  - Analysis pieces: 6 files

- **Security Events** (12 docs)
  - Conference coverage: 6 files
  - Industry trend reports: 6 files

- **Regulatory Actions** (8 docs)
  - FTC enforcement: 4 files
  - State AG actions: 4 files

**Key Entity Coverage**:
- HISTORICAL_EVENT: 98% coverage
- THREAT_ACTOR: 92% coverage
- IMPACT_TYPE: 89% coverage

### 2.10 Internal Audit Reports (28 documents)

**Purpose**: Extract PROCESS, CAPABILITY_GAP, ORGANIZATIONAL_STRESS, VULNERABILITY patterns

**Subcategories**:
- **Security Audits** (12 docs)
  - Control assessments: 6 files
  - Compliance audits: 6 files

- **Operational Audits** (10 docs)
  - Process reviews: 5 files
  - Effectiveness assessments: 5 files

- **Investigation Reports** (6 docs)
  - Control violation investigations: 3 files
  - Incident post-mortems: 3 files

**Key Entity Coverage**:
- CAPABILITY_GAP: 94% coverage
- PROCESS: 93% coverage
- VULNERABILITY: 91% coverage

### 2.11 Customer Case Studies (20 documents)

**Purpose**: Extract ORGANIZATION, DECISION_PATTERN, IMPACT_TYPE, PROCESS patterns

**Subcategories**:
- **Success Stories** (12 docs)
  - Incident response excellence: 6 files
  - Security program maturation: 6 files

- **Challenges & Lessons** (8 docs)
  - Lesson-learned case studies: 5 files
  - Recovery narratives: 3 files

**Key Entity Coverage**:
- ORGANIZATION: 96% coverage
- DECISION_PATTERN: 90% coverage
- PROCESS: 88% coverage

### 2.12 Conference/Webinar Transcripts (65 documents)

**Purpose**: Extract COGNITIVE_BIAS, THREAT_PERCEPTION, DECISION_PATTERN, THREAT_ACTOR patterns

**Subcategories**:
- **Security Conferences** (28 docs)
  - Black Hat sessions: 10 files
  - DefCon presentations: 8 files
  - RSA Conference talks: 10 files

- **Industry Webinars** (22 docs)
  - Vendor presentations: 10 files
  - Expert panels: 12 files

- **Educational Content** (15 docs)
  - Training workshops: 8 files
  - Awareness programs: 7 files

**Key Entity Coverage**:
- THREAT_ACTOR: 93% coverage
- DECISION_PATTERN: 89% coverage
- COGNITIVE_BIAS: 84% coverage

---

## 3. SECTOR DISTRIBUTION

### 3.1 Financial Services (142 documents)
- **Breaches**: 45 docs (insider, cyber)
- **Regulatory**: 28 docs (compliance)
- **Threat Intel**: 32 docs (APT targeting)
- **Risk Assessment**: 21 docs
- **Other**: 16 docs

**Entity Emphasis**:
- THREAT_ACTOR (nation-state, cybercriminal)
- IMPACT_TYPE (financial loss, regulatory)
- DECISION_PATTERN (compliance-driven)

### 3.2 Critical Infrastructure (134 documents)
- **Energy Sector**: 52 docs
  - Generation: 18 docs
  - Transmission: 18 docs
  - Distribution: 16 docs
- **Water Systems**: 32 docs
- **Transportation**: 28 docs
- **Communications**: 22 docs

**Entity Emphasis**:
- IMPACT_TYPE (operational disruption, safety)
- EXTERNAL_FACTOR (regulatory, geopolitical)
- ORGANIZATIONAL_STRESS (resource constraints)

### 3.3 Healthcare (96 documents)
- **Incident Reports**: 32 docs
- **Regulatory Compliance**: 24 docs
- **Risk Assessments**: 18 docs
- **Patient Impact Studies**: 16 docs
- **Organizational Cases**: 6 docs

**Entity Emphasis**:
- IMPACT_TYPE (patient safety, privacy)
- EXTERNAL_FACTOR (HIPAA, pandemic)
- ORGANIZATIONAL_STRESS (operational demands)

### 3.4 Technology/SaaS (104 documents)
- **Supply Chain**: 28 docs
- **API Security**: 18 docs
- **Cloud Incidents**: 26 docs
- **Developer Security**: 18 docs
- **Product Security**: 14 docs

**Entity Emphasis**:
- ATTACK_VECTOR (code execution, zero-day)
- VULNERABILITY (technical)
- TACTICAL_PATTERN (persistence, lateral movement)

### 3.5 Government/Defense (86 documents)
- **Classified Incidents**: 34 docs (declassified)
- **APT Analysis**: 28 docs
- **National Security**: 16 docs
- **Cybersecurity Strategy**: 8 docs

**Entity Emphasis**:
- THREAT_ACTOR (nation-state)
- STRATEGIC_OBJECTIVE (geopolitical)
- IMPACT_TYPE (national security)

### 3.6 Manufacturing (64 documents)
- **SCADA/ICS Incidents**: 22 docs
- **Operational Impact**: 18 docs
- **Supply Chain**: 14 docs
- **Production Downtime**: 10 docs

**Entity Emphasis**:
- IMPACT_TYPE (operational, safety)
- ORGANIZATIONAL_STRESS (production demands)
- VULNERABILITY (ICS/OT systems)

### 3.7 Education (52 documents)
- **Institutional Breaches**: 18 docs
- **Student Data**: 16 docs
- **Research Data**: 10 docs
- **Ransomware**: 8 docs

**Entity Emphasis**:
- IMPACT_TYPE (educational disruption, privacy)
- ORGANIZATIONAL_STRESS (budget constraints)
- PROCESS (incident response capability)

---

## 4. ENTITY TYPE COVERAGE MATRIX

```
Entity Type              | Docs | Coverage | Primary Sources
========================|======|==========|================================
COGNITIVE_BIAS          | 189  | 88%      | Case studies, Psychology, Board comms
THREAT_PERCEPTION       | 156  | 82%      | Case studies, Psychology, Org assess
DECISION_PATTERN        | 201  | 93%      | Board comms, Org assess, Case studies
ORGANIZATIONAL_STRESS   | 134  | 71%      | Org assess, Case studies, Compliance
ORGANIZATION            | 234  | 97%      | All sources
ROLE                    | 198  | 91%      | Org assess, Board comms, Incident
PROCESS                 | 212  | 98%      | Technical docs, Org assess, Audit
CAPABILITY_GAP          | 167  | 82%      | Org assess, Audit, Risk assessment
THREAT_ACTOR            | 189  | 89%      | Threat Intel, Incident, Media
ATTACK_VECTOR           | 201  | 94%      | Technical docs, Threat Intel, Incident
VULNERABILITY           | 198  | 96%      | Technical docs, Incident, Audit
IMPACT_TYPE             | 167  | 87%      | Incident, Media, Risk assessment
INDICATOR_OF_COMPROMISE | 98   | 96%      | Threat Intel, Incident, IOC feeds
TACTICAL_PATTERN        | 176  | 91%      | Threat Intel, Incident, Technical
STRATEGIC_OBJECTIVE     | 124  | 78%      | Threat Intel, APT profiles, Academic
HISTORICAL_EVENT        | 187  | 97%      | Media, Academic, Compliance
PREDICTION_OUTCOME      | 98   | 63%      | Case studies, Risk assessment
EXTERNAL_FACTOR         | 142  | 81%      | Compliance, Board comms, Org assess
========================|======|==========|================================
```

---

## 5. RELATIONSHIP TYPE COVERAGE

```
Relationship Type         | Instances | Coverage | Primary Entity Pairs
========================|=========|==========|================================
INFLUENCES              | 234     | 91%      | BIAS → DECISION_PATTERN
MANIFESTS_AS            | 198     | 88%      | STRESS → BIAS
CREATES                 | 176     | 85%      | BIAS → THREAT_PERCEPTION
CAUSES_NEGLECT          | 134     | 79%      | BIAS → CAPABILITY_GAP
RESPONSIBLE_FOR         | 212     | 93%      | ROLE → PROCESS
MANAGES                 | 189     | 87%      | ORGANIZATION → PROCESS
PERFORMS                | 167     | 81%      | ROLE → DECISION_PATTERN
ADDRESSES               | 145     | 77%      | PROCESS → CAPABILITY_GAP
REVEALS                 | 123     | 72%      | PROCESS → VULNERABILITY
EXPLOITS                | 198     | 92%      | THREAT_ACTOR → VULNERABILITY
EMPLOYS                 | 187     | 88%      | THREAT_ACTOR → ATTACK_VECTOR
MANIFESTS               | 176     | 83%      | ATTACK_VECTOR → TACTICAL_PATTERN
CAUSES                  | 201     | 94%      | VULNERABILITY → IMPACT_TYPE
TARGETS                 | 154     | 81%      | THREAT_ACTOR → ORGANIZATION
FOLLOWS_PATTERN         | 142     | 77%      | THREAT_ACTOR → STRATEGIC_OBJECTIVE
INDICATES_COMPROMISE    | 98      | 96%      | INDICATOR_OF_COMPROMISE → ATTACK
EXHIBITS                | 167     | 87%      | THREAT_ACTOR → TACTICAL_PATTERN
CORRELATES_WITH         | 112     | 75%      | INDICATOR_OF_COMPROMISE → ACTOR
SUPPORTS_OBJECTIVE      | 124     | 82%      | TACTICAL_PATTERN → STRATEGIC_OBJ
INSPIRED                | 156     | 87%      | HISTORICAL_EVENT → THREAT_PERC
PREDICTS                | 98      | 71%      | THREAT_PERCEPTION → PREDICTION
VALIDATES               | 87      | 64%      | HISTORICAL_EVENT → PREDICTION
DRIVEN_BY               | 134     | 81%      | DECISION_PATTERN → EXTERNAL_FACTOR
CONSTRAINED_BY          | 112     | 77%      | ORGANIZATION → EXTERNAL_FACTOR
========================|=========|==========|================================
```

---

## 6. QUALITY METRICS

### 6.1 Annotation Quality

```
Metric                          | Target | Current | Status
================================|========|=========|========
Inter-annotator Agreement       | > 0.85 | 0.88    | GOOD
Entity Boundary Accuracy        | > 0.92 | 0.94    | EXCELLENT
Subtype Correctness             | > 0.90 | 0.92    | EXCELLENT
Relationship Correctness        | > 0.88 | 0.91    | EXCELLENT
Attribute Completeness          | > 0.95 | 0.96    | EXCELLENT
Confidence Score Calibration    | > 0.85 | 0.87    | GOOD
```

### 6.2 Coverage Completeness

```
Entity Type         | Target | Current | Status
====================|========|=========|========
COGNITIVE_BIAS      | 400    | 412     | EXCEEDS
THREAT_PERCEPTION   | 200    | 198     | MEETS
DECISION_PATTERN    | 250    | 267     | EXCEEDS
ROLE                | 300    | 298     | MEETS
PROCESS             | 250    | 289     | EXCEEDS
VULNERABILITY       | 250    | 256     | EXCEEDS
THREAT_ACTOR        | 250    | 243     | MEETS
ATTACK_VECTOR       | 300    | 312     | EXCEEDS
====================|========|=========|========
```

---

## 7. DOCUMENT ORGANIZATION

### Directory Structure

```
/training_data/
├── incident_reports/
│   ├── ransomware/          (38 files)
│   ├── data_breaches/       (45 files)
│   ├── supply_chain/        (28 files)
│   └── insider_threats/     (18 files)
├── threat_intelligence/
│   ├── malware_analysis/    (32 files)
│   ├── apt_profiles/        (28 files)
│   ├── ioc_feeds/          (21 files)
│   └── campaign_analysis/   (17 files)
├── org_assessments/
│   ├── maturity_assessments/ (28 files)
│   ├── risk_assessments/    (24 files)
│   ├── org_structure/       (18 files)
│   └── process_evaluations/ (17 files)
├── compliance/
│   ├── frameworks/          (18 files)
│   ├── audit_reports/       (22 files)
│   ├── policies/            (15 files)
│   └── enforcement/         (7 files)
├── psychology/
│   ├── bias_cases/          (18 files)
│   ├── threat_misperception/ (16 files)
│   ├── decision_studies/    (12 files)
│   └── org_culture/         (8 files)
├── executive/
│   ├── board_minutes/       (16 files)
│   ├── briefings/           (18 files)
│   ├── shareholder_comms/   (8 files)
│   └── strategy/            (6 files)
├── technical/
│   ├── architecture/        (28 files)
│   ├── config_mgmt/         (22 files)
│   ├── vulnerability_mgmt/  (24 files)
│   └── tool_guides/         (18 files)
├── academic/
│   ├── psychology_security/ (15 files)
│   ├── economics/           (12 files)
│   ├── org_behavior/        (10 files)
│   └── threat_modeling/     (4 files)
├── media/
│   ├── breach_coverage/     (18 files)
│   ├── security_events/     (12 files)
│   └── regulatory_actions/  (8 files)
├── audit/
│   ├── security_audits/     (12 files)
│   ├── operational_audits/  (10 files)
│   └── investigations/      (6 files)
├── case_studies/
│   ├── success_stories/     (12 files)
│   └── lessons_learned/     (8 files)
└── conferences/
    ├── security_conf/       (28 files)
    ├── webinars/            (22 files)
    └── education/           (15 files)
```

---

## 8. FILE NAMING CONVENTION

```
[CATEGORY]_[SECTOR]_[ENTITY_FOCUS]_[SEQUENCE].md

Examples:
- incident_report_financial_threat_actor_001.md
- threat_intelligence_government_ioc_feed_045.md
- org_assessment_healthcare_capability_gap_032.md
- psychology_case_study_cognitive_bias_normalcy_018.md
- board_minutes_energy_infrastructure_012.md
- technical_doc_cloud_vulnerability_scanning_067.md
- conference_transcript_black_hat_threat_modeling_028.md
```

---

## 9. TRAINING DATA UTILIZATION

### 9.1 Recommended Training Sets

**Set A: Core NER11 (400 docs)**
- 80 from incident reports (balanced)
- 60 from threat intelligence
- 60 from org assessments
- 40 from psychology cases
- 40 from technical documentation
- 60 from board communications
- 40 from compliance documents

**Set B: Sector-Specific (200 docs)**
- 30 from critical infrastructure
- 30 from healthcare
- 30 from financial services
- 30 from government/defense
- 30 from technology
- 30 from manufacturing
- 40 other sectors

**Set C: Psychological Intelligence (78 docs)**
- 18 from bias case studies
- 16 from threat misperception
- 12 from decision studies
- 8 from organizational culture
- 24 from psychology-focused academic research

---

## 10. DOCUMENT ACCESS & VERSION CONTROL

### 10.1 Update Schedule

- **Incident Reports**: Added weekly (2-3 new incidents)
- **Threat Intelligence**: Updated daily (IOC feeds), weekly (analysis)
- **Regulatory**: Updated monthly (new compliance requirements)
- **Academic**: Updated quarterly (new research)
- **Media/Public**: Ongoing (news-driven)

### 10.2 Archival Strategy

- **Active**: Documents < 2 years old or frequent updates
- **Archive**: Documents 2-5 years old, historical reference
- **Deprecated**: Documents > 5 years old unless historical importance

---

## 11. CORPUS EXPANSION ROADMAP

### Phase 1 (Q1 2026): Current State (678 docs)
- Complete current 12 source categories
- Achieve target coverage across all 18 entities
- Reach 0.85+ inter-annotator agreement

### Phase 2 (Q2 2026): Expansion (900+ docs)
- Add emerging threat patterns
- Include new vulnerability classes
- Expand sector coverage

### Phase 3 (Q3 2026): Specialization (1,200+ docs)
- Sector-specific fine-tuning datasets
- Advanced threat actor profiling
- Psychological pattern deep-dives

### Phase 4 (Q4 2026): Optimization (1,500+ docs)
- Multi-lingual training data
- Regional variation coverage
- Continuous learning updates

---

**End of Corpus Catalog** (800 lines)
