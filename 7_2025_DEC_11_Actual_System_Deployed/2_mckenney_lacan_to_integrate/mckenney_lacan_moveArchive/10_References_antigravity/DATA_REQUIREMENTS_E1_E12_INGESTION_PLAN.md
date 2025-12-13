# E1-E12 Data Requirements & Ingestion Plan

## AEON Digital Twin \- Cybersecurity Application Rationalization

**Version:** 1.0.0 **Created:** 2025-12-04 **Purpose:** Comprehensive data requirements for all Enhancement APIs (E1-E12) with ingestion prompts and sources **Format:** E30-Compatible, AI/LLM-Optimized for automated processing

---

## DOCUMENT METADATA

document\_type: data\_requirements\_specification

version: 1.0.0

created: 2025-12-04T16:45:00Z

target\_systems:

  graph\_db: openspg-neo4j:7687

  vector\_db: openspg-qdrant:6333

  api\_server: ner11-gold-api:8000

embedding\_model: sentence-transformers/all-MiniLM-L6-v2

embedding\_dimensions: 384

ingestion\_process: E30

customer\_isolation: X-Customer-ID header

---

## EXECUTIVE SUMMARY

| Category | Count | Priority |
| :---- | :---- | :---- |
| Enhancement APIs | 12 (E03-E12, E15) | ALL CRITICAL |
| Neo4j Entity Types | 45+ | HIGH |
| Qdrant Collections | 11 | HIGH |
| External Data Sources | 35+ | MEDIUM-HIGH |
| Kaggle Datasets | 15+ | MEDIUM |
| Perplexity Prompts | 25 | HIGH |

---

## SECTION 1: NEO4J GRAPH ENTITY REQUIREMENTS

### 1.1 Core Entity Types (Must Have)

// E03 SBOM Analysis

(:SoftwareComponent {name, version, purl, cpe, component\_type, license})

(:SBOM {name, format, generator\_tool, target\_system\_id})

(:DependencyRelation {depth, scope})

(:SoftwareVulnerability {cve\_id, cvss\_score, epss\_score, exploit\_maturity})

// E04 Threat Intelligence

(:ThreatActor {name, aliases, country, motivation, sophistication})

(:ThreatCampaign {name, target\_sectors, start\_date, end\_date})

(:IOC {ioc\_type, value, confidence, first\_seen, last\_seen})

(:MITREMapping {technique\_id, tactic, mapped\_entity\_type})

(:ThreatFeed {feed\_url, feed\_type, refresh\_interval})

// E05 Risk Scoring

(:RiskScore {entity\_type, entity\_id, risk\_score, risk\_level})

(:AssetCriticality {asset\_id, criticality\_level, business\_impact, data\_classification})

(:ExposureScore {asset\_id, attack\_surface, open\_ports, network\_exposure})

(:RiskFactor {factor\_name, value, weight})

// E06 Remediation

(:RemediationTask {task\_id, vulnerability\_id, cve\_id, status, priority})

(:RemediationPlan {plan\_id, total\_tasks, completed\_tasks, status})

(:RemediationAction {action\_id, task\_id, action\_type, performed\_by})

(:SLAPolicy {policy\_id, severity\_level, response\_time\_hours, resolution\_time\_hours})

// E07 Compliance Mapping

(:ComplianceControl {control\_id, framework, title, description, control\_family, priority})

(:FrameworkMapping {source\_framework, target\_framework, relationship\_type, confidence})

(:ComplianceAssessment {assessment\_id, control\_id, status, compliance\_score})

(:ComplianceEvidence {evidence\_id, evidence\_type, title, collection\_date})

(:ComplianceGap {gap\_id, gap\_type, severity, remediation\_plan})

// E08 Automated Scanning

(:ScanProfile {profile\_id, name, scan\_type, configuration, enabled})

(:ScanSchedule {schedule\_id, frequency, cron\_expression, last\_run, next\_run})

(:ScanJob {job\_id, status, priority, progress, findings\_count})

(:Finding {finding\_id, severity, status, title, cve\_ids, recommendation})

(:ScanTarget {target\_id, target\_type, address, last\_scanned})

// E09 Alert Management

(:Alert {alert\_id, title, severity, status, source, event\_type, affected\_assets})

(:AlertRule {rule\_id, name, conditions, actions, triggered\_count})

(:NotificationRule {notification\_id, channels, severity\_filter, recipients})

(:EscalationPolicy {policy\_id, escalation\_levels, severity\_filter})

(:AlertCorrelation {correlation\_id, correlation\_type, confidence, root\_cause\_alert\_id})

// E10 Economic Impact

(:CostRecord {cost\_id, category, amount, currency, period})

(:Investment {investment\_id, amount, expected\_roi, actual\_roi})

(:BusinessValue {value\_id, metric\_type, value, measurement\_date})

(:ImpactScenario {scenario\_id, scenario\_type, probability, impact\_amount})

// E11 Demographics

(:Employee {employee\_id, name, department, role, hire\_date, location})

(:OrganizationUnit {unit\_id, name, parent\_unit, level})

(:Role {role\_id, title, department, security\_clearance})

(:Skill {skill\_id, name, category, proficiency\_levels})

(:Team {team\_id, name, function, size})

// E12 Prioritization

(:PriorityItem {item\_id, entity\_type, entity\_id, priority\_score, priority\_band})

(:UrgencyFactor {factor\_id, factor\_type, value, weight})

(:RemediationEffort {effort\_id, estimated\_hours, complexity, resource\_requirements})

// E15 Vendor Equipment

(:Vendor {vendor\_id, name, country, risk\_level, support\_status})

(:EquipmentModel {model\_id, vendor\_id, model\_name, category, eol\_date})

(:SupportContract {contract\_id, vendor\_id, start\_date, end\_date, coverage\_level})

(:MaintenanceWindow {window\_id, equipment\_id, start\_time, duration, frequency})

### 1.2 Critical Relationships

// SBOM Dependencies

(component1:SoftwareComponent)-\[:DEPENDS\_ON {depth, scope}\]-\>(component2:SoftwareComponent)

(sbom:SBOM)-\[:CONTAINS\]-\>(component:SoftwareComponent)

(component:SoftwareComponent)-\[:HAS\_VULNERABILITY\]-\>(vuln:SoftwareVulnerability)

// Threat Intelligence

(actor:ThreatActor)-\[:CONDUCTS\]-\>(campaign:ThreatCampaign)

(campaign:ThreatCampaign)-\[:USES\_TECHNIQUE\]-\>(mitre:MITREMapping)

(campaign:ThreatCampaign)-\[:PRODUCES\]-\>(ioc:IOC)

// Risk & Remediation

(asset:Asset)-\[:HAS\_RISK\_SCORE\]-\>(risk:RiskScore)

(vuln:Vulnerability)-\[:REQUIRES\]-\>(task:RemediationTask)

(task:RemediationTask)-\[:PART\_OF\]-\>(plan:RemediationPlan)

// Compliance

(control:ComplianceControl)-\[:MAPS\_TO\]-\>(control2:ComplianceControl)

(control:ComplianceControl)-\[:HAS\_ASSESSMENT\]-\>(assessment:ComplianceAssessment)

(gap:ComplianceGap)-\[:RELATES\_TO\]-\>(control:ComplianceControl)

// Organization

(employee:Employee)-\[:BELONGS\_TO\]-\>(unit:OrganizationUnit)

(employee:Employee)-\[:HAS\_ROLE\]-\>(role:Role)

(employee:Employee)-\[:HAS\_SKILL\]-\>(skill:Skill)

// Vendor Equipment

(equipment:EquipmentModel)-\[:MANUFACTURED\_BY\]-\>(vendor:Vendor)

(equipment:EquipmentModel)-\[:COVERED\_BY\]-\>(contract:SupportContract)

---

## SECTION 2: QDRANT VECTOR COLLECTIONS

### 2.1 Collection Specifications

| Collection Name | Dimensions | Entity Types | Embedding Source |
| :---- | :---- | :---- | :---- |
| `ner11_sbom` | 384 | sbom, software\_component, vulnerability | component name \+ description |
| `ner11_threat_intel` | 384 | threat\_actor, campaign, ioc, mitre | actor name \+ description |
| `ner11_risk_scoring` | 384 | risk\_score, asset\_criticality, exposure | entity name \+ factors |
| `ner11_remediation` | 384 | task, plan, action | task title \+ CVE \+ description |
| `ner11_compliance` | 384 | control, mapping, assessment, gap | control\_number \+ title \+ desc |
| `ner11_scanning` | 384 | profile, job, finding, target | finding title \+ description |
| `ner11_alerts` | 384 | alert, rule, notification, escalation | alert title \+ event\_type |
| `ner11_economic_impact` | 384 | cost, investment, business\_value | category \+ description |
| `ner11_demographics` | 384 | employee, org\_unit, role, skill | name \+ title \+ department |
| `ner11_prioritization` | 384 | priority\_item, urgency\_factor | entity \+ factors |
| `ner11_vendor_equipment` | 384 | vendor, equipment, contract | vendor \+ model \+ description |

### 2.2 Minimum Data Volume Requirements

minimum\_viable\_data:

  ner11\_sbom: 500 components, 50 SBOMs, 200 vulnerabilities

  ner11\_threat\_intel: 100 actors, 50 campaigns, 500 IOCs, 200 MITRE mappings

  ner11\_risk\_scoring: 200 risk scores, 100 assets

  ner11\_remediation: 100 tasks, 20 plans

  ner11\_compliance: 500 controls (NIST+ISO+SOC2), 100 mappings

  ner11\_scanning: 20 profiles, 100 findings

  ner11\_alerts: 50 rules, 200 alerts

  ner11\_economic\_impact: 100 cost records, 20 scenarios

  ner11\_demographics: 100 employees, 20 org units, 30 roles

  ner11\_prioritization: 50 priority items

  ner11\_vendor\_equipment: 50 vendors, 200 equipment models

---

## SECTION 3: EXTERNAL DATA SOURCES

### 3.1 Free/Open Sources (Priority: HIGH)

| Source | URL | Data Type | APIs Supported |
| :---- | :---- | :---- | :---- |
| NVD (National Vulnerability Database) | [https://nvd.nist.gov](https://nvd.nist.gov) | CVE, CVSS, CPE | E03, E05, E08 |
| CISA KEV Catalog | [https://www.cisa.gov/known-exploited-vulnerabilities-catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | Known Exploited Vulns | E03, E05, E12 |
| EPSS (Exploit Prediction) | [https://www.first.org/epss](https://www.first.org/epss) | Exploit probability | E03, E05, E12 |
| MITRE ATT\&CK | [https://attack.mitre.org](https://attack.mitre.org) | Techniques, Tactics | E04, E09 |
| MITRE ATT\&CK for ICS | [https://attack.mitre.org/techniques/ics/](https://attack.mitre.org/techniques/ics/) | ICS Techniques | E04, E15 |
| NIST SP 800-53 | [https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) | Security Controls | E07 |
| CIS Benchmarks | [https://www.cisecurity.org/cis-benchmarks](https://www.cisecurity.org/cis-benchmarks) | Configuration Baselines | E07, E08 |
| OWASP | [https://owasp.org](https://owasp.org) | Web Security | E08 |
| OSV.dev | [https://osv.dev](https://osv.dev) | Open Source Vulns | E03 |
| deps.dev | [https://deps.dev](https://deps.dev) | Dependency Analysis | E03 |
| SPDX License List | [https://spdx.org/licenses](https://spdx.org/licenses) | License Definitions | E03 |
| ICS-CERT Advisories | [https://www.cisa.gov/uscert/ics](https://www.cisa.gov/uscert/ics) | ICS Vulnerabilities | E04, E15 |
| AlienVault OTX | [https://otx.alienvault.com](https://otx.alienvault.com) | Threat Intelligence | E04 |

### 3.2 Commercial/Enterprise Sources (Recommended)

| Source | Data Type | APIs Supported | Notes |
| :---- | :---- | :---- | :---- |
| Qualys | Vulnerability Scans | E08, E05 | API integration |
| Nessus/Tenable | Vulnerability Scans | E08, E05 | Export capability |
| Shodan | Internet Exposure | E05, E08 | API key required |
| VirusTotal | IOC Analysis | E04 | API key required |
| ServiceNow | CMDB, ITSM | E06, E11 | REST API |
| Workday/SAP | HR Data | E11 | Enterprise only |
| Gartner/Forrester | Industry Benchmarks | E10 | Subscription |

---

## SECTION 4: KAGGLE DATASETS

### 4.1 Recommended Datasets

kaggle\_datasets:

  cybersecurity\_vulnerabilities:

    \- dataset: "uciml/cybersecurity-intrusion-detection"

      relevance: E04, E08, E09

      records: 25,000+

    \- dataset: "joebeachcapital/cve-mitre-attck"

      relevance: E03, E04, E05

      records: 180,000+ CVEs

    \- dataset: "bithikasharma1/cyber-security-attacks"

      relevance: E04, E09

      records: 25,000+

  threat\_intelligence:

    \- dataset: "mrwellsdavid/malware-detection"

      relevance: E04, E08

      records: 10,000+

    \- dataset: "solarmainframe/ids-intrusion-csv"

      relevance: E04, E09

      records: 500,000+

  compliance\_frameworks:

    \- dataset: "wsj/compliance-controls"  \# Search for similar

      relevance: E07

  economic\_data:

    \- dataset: "ibm/data-breach-report"  \# Search variations

      relevance: E10

  workforce\_demographics:

    \- dataset: "kaggle/hr-analytics"

      relevance: E11

      records: 15,000+

### 4.2 Kaggle API Commands

\# Setup (credentials at /home/jim/2\_OXOT\_Projects\_Dev/.kaggle/kaggle.json)

export KAGGLE\_CONFIG\_DIR=/home/jim/2\_OXOT\_Projects\_Dev/.kaggle

\# Search for cybersecurity datasets

kaggle datasets list \-s "cybersecurity vulnerability" \--sort-by votes

\# Download specific datasets

kaggle datasets download \-d uciml/cybersecurity-intrusion-detection

kaggle datasets download \-d joebeachcapital/cve-mitre-attck

\# Search for threat intelligence

kaggle datasets list \-s "threat intelligence malware" \--sort-by votes

\# Search for compliance

kaggle datasets list \-s "security compliance controls" \--sort-by votes

---

## SECTION 5: PERPLEXITY RESEARCH PROMPTS

### 5.1 Vulnerability & SBOM Data (E03, E05)

PROMPT\_E03\_01:

"Provide a comprehensive list of the top 100 most critical CVEs from 2023-2024

affecting enterprise software, including: CVE ID, CVSS score, EPSS score,

affected products (CPE), exploit availability, and recommended remediation.

Format as JSON array."

PROMPT\_E03\_02:

"What are the most common open-source software licenses and their risk

classifications for enterprise use? Include: license name, SPDX identifier,

copyleft status, commercial use restrictions, and compliance requirements.

Format as structured table."

PROMPT\_E03\_03:

"List the top 50 most vulnerable open-source packages in npm, PyPI, and Maven

ecosystems from 2024, with CVE counts, severity distributions, and dependency

chain risks."

### 5.2 Threat Intelligence (E04)

PROMPT\_E04\_01:

"Provide detailed profiles of the top 20 APT groups targeting critical

infrastructure in 2024, including: group name, aliases, attributed nation-state,

primary motivations, target sectors, known TTPs (MITRE ATT\&CK IDs), and active

campaigns. Format as JSON."

PROMPT\_E04\_02:

"What are the most commonly used MITRE ATT\&CK techniques in ransomware attacks

from 2023-2024? Include technique ID, tactic, description, detection methods,

and mitigation strategies."

PROMPT\_E04\_03:

"List current active threat campaigns targeting energy sector and industrial

control systems (ICS), including threat actor attribution, attack vectors,

indicators of compromise (IOCs), and timeline."

### 5.3 Compliance Frameworks (E07)

PROMPT\_E07\_01:

"Provide a complete mapping between NIST SP 800-53 Rev 5 controls and ISO 27001:2022

controls, including: NIST control ID, ISO control ID, relationship type

(equivalent, partial, related), and mapping confidence score."

PROMPT\_E07\_02:

"What are the mandatory security controls for NERC CIP compliance for energy

utilities? Include control ID, requirement description, evidence requirements,

and common audit findings."

PROMPT\_E07\_03:

"List the top 50 most commonly failed SOC 2 Type II audit controls with failure

reasons, remediation recommendations, and evidence requirements."

### 5.4 Risk & Economic Impact (E05, E10)

PROMPT\_E05\_01:

"What are industry-standard risk scoring methodologies for cybersecurity?

Include: methodology name, scoring factors, weight distributions, and

calculation formulas. Compare CVSS, FAIR, OWASP Risk Rating."

PROMPT\_E10\_01:

"Provide industry benchmarks for cybersecurity incident costs by sector

(healthcare, finance, energy, manufacturing) including: average breach cost,

cost per record, downtime costs, regulatory fines, and recovery time.

Source: IBM, Ponemon, Verizon DBIR 2024."

PROMPT\_E10\_02:

"What are the typical ROI metrics and calculation methods for cybersecurity

investments? Include: risk reduction percentage, incident prevention value,

compliance cost avoidance, and insurance premium reduction."

### 5.5 ICS/OT & Vendor Equipment (E15)

PROMPT\_E15\_01:

"List the top 50 ICS/SCADA vendors and their equipment categories with:

vendor name, headquarters country, primary product categories, known

vulnerabilities count, support lifecycle status, and CISA advisories."

PROMPT\_E15\_02:

"What industrial control system equipment has reached end-of-life (EOL) in

2023-2024? Include manufacturer, model, EOL date, replacement recommendations,

and security implications."

PROMPT\_E15\_03:

"Provide ICS-CERT advisories summary for 2024 including: advisory ID, affected

vendor, affected products, vulnerability type, CVSS score, and mitigation status."

### 5.6 Demographics & Workforce (E11)

PROMPT\_E11\_01:

"What are industry benchmarks for cybersecurity team structures and staffing

ratios by organization size? Include: team roles, FTE ratios, skill requirements,

and certification expectations."

PROMPT\_E11\_02:

"Provide typical organizational structures for cybersecurity departments in

Fortune 500 companies, including reporting lines, team compositions, and

role definitions."

---

## SECTION 6: E30 INGESTION FORMAT SPECIFICATIONS

### 6.1 Standard Entity Format

{

  "entity\_type": "string (e.g., ThreatActor, ComplianceControl)",

  "entity\_id": "string (UUID or natural key)",

  "customer\_id": "string (SYSTEM for baseline, customer\_id for tenant)",

  "namespace": "string (optional)",

  "properties": {

    "field1": "value1",

    "field2": "value2"

  },

  "embedding\_text": "string (text to generate 384-dim vector from)",

  "relationships": \[

    {

      "type": "RELATIONSHIP\_TYPE",

      "target\_entity\_type": "string",

      "target\_entity\_id": "string",

      "properties": {}

    }

  \],

  "metadata": {

    "source": "string (data source identifier)",

    "ingestion\_date": "ISO8601 timestamp",

    "version": "string"

  }

}

### 6.2 Batch Ingestion Format

{

  "batch\_id": "string (UUID)",

  "batch\_type": "baseline | customer | update",

  "customer\_id": "SYSTEM | specific\_customer",

  "target\_collection": "ner11\_collection\_name",

  "entities": \[

    { /\* entity objects \*/ }

  \],

  "relationships": \[

    { /\* relationship objects for Neo4j \*/ }

  \],

  "processing\_instructions": {

    "generate\_embeddings": true,

    "embedding\_model": "sentence-transformers/all-MiniLM-L6-v2",

    "upsert\_mode": "insert | update | upsert",

    "validate\_schema": true

  }

}

### 6.3 Source-Specific Transformers

data\_transformers:

  nvd\_cve:

    source\_format: NVD JSON 2.0

    target\_entity: SoftwareVulnerability

    field\_mappings:

      cve.id: cve\_id

      cve.metrics.cvssMetricV31\[0\].cvssData.baseScore: cvss\_score

      cve.descriptions\[0\].value: description

    embedding\_fields: \[description, cve\_id\]

  mitre\_attack:

    source\_format: STIX 2.1 Bundle

    target\_entity: MITREMapping

    field\_mappings:

      external\_references\[0\].external\_id: technique\_id

      kill\_chain\_phases\[0\].phase\_name: tactic

      name: technique\_name

      description: description

    embedding\_fields: \[technique\_name, description\]

  nist\_800\_53:

    source\_format: OSCAL JSON

    target\_entity: ComplianceControl

    field\_mappings:

      id: control\_id

      title: title

      parts\[0\].prose: description

    embedding\_fields: \[control\_id, title, description\]

---

## SECTION 7: DATA COLLECTION PRIORITY MATRIX

### 7.1 Phase 1: Critical Baseline (Week 1-2)

| Priority | Data Type | Source | APIs | Volume |
| :---- | :---- | :---- | :---- | :---- |
| P0 | CVE/CVSS Data | NVD API | E03, E05, E08 | 200K+ CVEs |
| P0 | MITRE ATT\&CK | STIX Bundle | E04, E09 | 600+ techniques |
| P0 | NIST 800-53 Controls | OSCAL | E07 | 1,100+ controls |
| P0 | CISA KEV | JSON Feed | E03, E05, E12 | 1,000+ vulns |
| P1 | ISO 27001 Controls | Manual/Commercial | E07 | 114 controls |
| P1 | CIS Benchmarks | CIS API | E07, E08 | 100+ benchmarks |

### 7.2 Phase 2: Enrichment Data (Week 3-4)

| Priority | Data Type | Source | APIs | Volume |
| :---- | :---- | :---- | :---- | :---- |
| P1 | ICS-CERT Advisories | CISA Feed | E04, E15 | 500+ advisories |
| P1 | EPSS Scores | FIRST API | E03, E05, E12 | All CVEs |
| P2 | Threat Actor Profiles | MITRE Groups | E04 | 150+ actors |
| P2 | ICS Vendor Catalog | Manual Research | E15 | 100+ vendors |
| P2 | Industry Cost Benchmarks | Perplexity/Reports | E10 | Benchmark data |

### 7.3 Phase 3: Extended Data (Week 5+)

| Priority | Data Type | Source | APIs | Volume |
| :---- | :---- | :---- | :---- | :---- |
| P2 | Kaggle Datasets | Kaggle API | Multiple | Variable |
| P2 | OSV.dev Vulnerabilities | OSV API | E03 | 100K+ vulns |
| P3 | Commercial Threat Feeds | AlienVault OTX | E04 | Ongoing |
| P3 | Compliance Evidence Templates | Manual | E07 | 50+ templates |

---

## SECTION 8: AUTOMATION SCRIPTS

### 8.1 Kaggle Data Download Script

\#\!/bin/bash

\# File: scripts/download\_kaggle\_datasets.sh

export KAGGLE\_CONFIG\_DIR=/home/jim/2\_OXOT\_Projects\_Dev/.kaggle

OUTPUT\_DIR=/home/jim/2\_OXOT\_Projects\_Dev/data/kaggle

mkdir \-p $OUTPUT\_DIR

\# Cybersecurity datasets

kaggle datasets download \-d uciml/cybersecurity-intrusion-detection \-p $OUTPUT\_DIR

kaggle datasets download \-d mrwellsdavid/malware-detection \-p $OUTPUT\_DIR

\# Search and list available

kaggle datasets list \-s "cve vulnerability" \--sort-by votes \> $OUTPUT\_DIR/cve\_datasets.txt

kaggle datasets list \-s "mitre attack" \--sort-by votes \> $OUTPUT\_DIR/mitre\_datasets.txt

kaggle datasets list \-s "compliance security" \--sort-by votes \> $OUTPUT\_DIR/compliance\_datasets.txt

### 8.2 NVD CVE Download Script

\#\!/bin/bash

\# File: scripts/download\_nvd\_cves.sh

OUTPUT\_DIR=/home/jim/2\_OXOT\_Projects\_Dev/data/nvd

mkdir \-p $OUTPUT\_DIR

\# Download recent CVEs (last 120 days)

curl \-o $OUTPUT\_DIR/nvd\_recent.json \\

  "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=2000"

\# Download CISA KEV

curl \-o $OUTPUT\_DIR/cisa\_kev.json \\

  "https://www.cisa.gov/sites/default/files/feeds/known\_exploited\_vulnerabilities.json"

\# Download EPSS scores

curl \-o $OUTPUT\_DIR/epss\_scores.csv \\

  "https://epss.cyentia.com/epss\_scores-current.csv.gz"

### 8.3 MITRE ATT\&CK Download Script

\#\!/bin/bash

\# File: scripts/download\_mitre\_attack.sh

OUTPUT\_DIR=/home/jim/2\_OXOT\_Projects\_Dev/data/mitre

mkdir \-p $OUTPUT\_DIR

\# Enterprise ATT\&CK

curl \-o $OUTPUT\_DIR/enterprise-attack.json \\

  "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

\# ICS ATT\&CK

curl \-o $OUTPUT\_DIR/ics-attack.json \\

  "https://raw.githubusercontent.com/mitre/cti/master/ics-attack/ics-attack.json"

\# Mobile ATT\&CK

curl \-o $OUTPUT\_DIR/mobile-attack.json \\

  "https://raw.githubusercontent.com/mitre/cti/master/mobile-attack/mobile-attack.json"

---

## SECTION 9: VALIDATION CHECKLIST

### 9.1 Pre-Ingestion Validation

- [ ] All entity types have valid JSON schemas  
- [ ] Embedding text fields are populated  
- [ ] Customer IDs are set (SYSTEM for baseline)  
- [ ] Relationship targets exist  
- [ ] Required fields are non-null  
- [ ] Date formats are ISO8601  
- [ ] UUIDs are valid format

### 9.2 Post-Ingestion Validation

- [ ] Qdrant collection record counts match expected  
- [ ] Neo4j node counts match expected  
- [ ] Relationship integrity verified  
- [ ] Embedding dimensions are 384  
- [ ] Semantic search returns relevant results  
- [ ] API endpoints return data  
- [ ] Customer isolation working (X-Customer-ID filtering)

---

## SECTION 10: APPENDIX

### 10.1 API Endpoint Summary

| Enhancement | API Prefix | Endpoints | Collection |
| :---- | :---- | :---- | :---- |
| E03 SBOM | `/api/v2/sbom` | 25 | ner11\_sbom |
| E04 Threat Intel | `/api/v2/threat-intel` | 28 | ner11\_threat\_intel |
| E05 Risk Scoring | `/api/v2/risk-scoring` | 24 | ner11\_risk\_scoring |
| E06 Remediation | `/api/v2/remediation` | 22 | ner11\_remediation |
| E07 Compliance | `/api/v2/compliance` | 26 | ner11\_compliance |
| E08 Scanning | `/api/v2/scanning` | 24 | ner11\_scanning |
| E09 Alerts | `/api/v2/alerts` | 28 | ner11\_alerts |
| E10 Economic | `/api/v2/economic-impact` | 27 | ner11\_economic\_impact |
| E11 Demographics | `/api/v2/demographics` | 24 | ner11\_demographics |
| E12 Prioritization | `/api/v2/prioritization` | 28 | ner11\_prioritization |
| E15 Vendor | `/api/v2/vendor-equipment` | 25 | ner11\_vendor\_equipment |

### 10.2 Contact & Resources

- **Container API**: [http://localhost:8000](http://localhost:8000) (ner11-gold-api)  
- **Qdrant Dashboard**: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)  
- **Neo4j Browser**: [http://localhost:7474](http://localhost:7474)  
- **Repository**: [https://github.com/Planet9V/agent-optimization-deployment](https://github.com/Planet9V/agent-optimization-deployment)

---

**Document Status:** READY FOR INGESTION PLANNING **Next Action:** Execute Phase 1 data collection scripts **Estimated Completion:** 2-4 weeks for full baseline data  
