# E1-E12 Data Requirements & Ingestion Plan
## AEON Digital Twin - Cybersecurity Application Rationalization

**Version:** 1.0.0
**Created:** 2025-12-04
**Purpose:** Comprehensive data requirements for all Enhancement APIs (E1-E12) with ingestion prompts and sources
**Format:** E30-Compatible, AI/LLM-Optimized for automated processing

---

## DOCUMENT METADATA
```yaml
document_type: data_requirements_specification
version: 1.0.0
created: 2025-12-04T16:45:00Z
target_systems:
  graph_db: openspg-neo4j:7687
  vector_db: openspg-qdrant:6333
  api_server: ner11-gold-api:8000
embedding_model: sentence-transformers/all-MiniLM-L6-v2
embedding_dimensions: 384
ingestion_process: E30
customer_isolation: X-Customer-ID header
```

---

## EXECUTIVE SUMMARY

| Category | Count | Priority |
|----------|-------|----------|
| Enhancement APIs | 12 (E03-E12, E15) | ALL CRITICAL |
| Neo4j Entity Types | 45+ | HIGH |
| Qdrant Collections | 11 | HIGH |
| External Data Sources | 35+ | MEDIUM-HIGH |
| Kaggle Datasets | 15+ | MEDIUM |
| Perplexity Prompts | 25 | HIGH |

---

## SECTION 1: NEO4J GRAPH ENTITY REQUIREMENTS

### 1.1 Core Entity Types (Must Have)

```cypher
// E03 SBOM Analysis
(:SoftwareComponent {name, version, purl, cpe, component_type, license})
(:SBOM {name, format, generator_tool, target_system_id})
(:DependencyRelation {depth, scope})
(:SoftwareVulnerability {cve_id, cvss_score, epss_score, exploit_maturity})

// E04 Threat Intelligence
(:ThreatActor {name, aliases, country, motivation, sophistication})
(:ThreatCampaign {name, target_sectors, start_date, end_date})
(:IOC {ioc_type, value, confidence, first_seen, last_seen})
(:MITREMapping {technique_id, tactic, mapped_entity_type})
(:ThreatFeed {feed_url, feed_type, refresh_interval})

// E05 Risk Scoring
(:RiskScore {entity_type, entity_id, risk_score, risk_level})
(:AssetCriticality {asset_id, criticality_level, business_impact, data_classification})
(:ExposureScore {asset_id, attack_surface, open_ports, network_exposure})
(:RiskFactor {factor_name, value, weight})

// E06 Remediation
(:RemediationTask {task_id, vulnerability_id, cve_id, status, priority})
(:RemediationPlan {plan_id, total_tasks, completed_tasks, status})
(:RemediationAction {action_id, task_id, action_type, performed_by})
(:SLAPolicy {policy_id, severity_level, response_time_hours, resolution_time_hours})

// E07 Compliance Mapping
(:ComplianceControl {control_id, framework, title, description, control_family, priority})
(:FrameworkMapping {source_framework, target_framework, relationship_type, confidence})
(:ComplianceAssessment {assessment_id, control_id, status, compliance_score})
(:ComplianceEvidence {evidence_id, evidence_type, title, collection_date})
(:ComplianceGap {gap_id, gap_type, severity, remediation_plan})

// E08 Automated Scanning
(:ScanProfile {profile_id, name, scan_type, configuration, enabled})
(:ScanSchedule {schedule_id, frequency, cron_expression, last_run, next_run})
(:ScanJob {job_id, status, priority, progress, findings_count})
(:Finding {finding_id, severity, status, title, cve_ids, recommendation})
(:ScanTarget {target_id, target_type, address, last_scanned})

// E09 Alert Management
(:Alert {alert_id, title, severity, status, source, event_type, affected_assets})
(:AlertRule {rule_id, name, conditions, actions, triggered_count})
(:NotificationRule {notification_id, channels, severity_filter, recipients})
(:EscalationPolicy {policy_id, escalation_levels, severity_filter})
(:AlertCorrelation {correlation_id, correlation_type, confidence, root_cause_alert_id})

// E10 Economic Impact
(:CostRecord {cost_id, category, amount, currency, period})
(:Investment {investment_id, amount, expected_roi, actual_roi})
(:BusinessValue {value_id, metric_type, value, measurement_date})
(:ImpactScenario {scenario_id, scenario_type, probability, impact_amount})

// E11 Demographics
(:Employee {employee_id, name, department, role, hire_date, location})
(:OrganizationUnit {unit_id, name, parent_unit, level})
(:Role {role_id, title, department, security_clearance})
(:Skill {skill_id, name, category, proficiency_levels})
(:Team {team_id, name, function, size})

// E12 Prioritization
(:PriorityItem {item_id, entity_type, entity_id, priority_score, priority_band})
(:UrgencyFactor {factor_id, factor_type, value, weight})
(:RemediationEffort {effort_id, estimated_hours, complexity, resource_requirements})

// E15 Vendor Equipment
(:Vendor {vendor_id, name, country, risk_level, support_status})
(:EquipmentModel {model_id, vendor_id, model_name, category, eol_date})
(:SupportContract {contract_id, vendor_id, start_date, end_date, coverage_level})
(:MaintenanceWindow {window_id, equipment_id, start_time, duration, frequency})
```

### 1.2 Critical Relationships

```cypher
// SBOM Dependencies
(component1:SoftwareComponent)-[:DEPENDS_ON {depth, scope}]->(component2:SoftwareComponent)
(sbom:SBOM)-[:CONTAINS]->(component:SoftwareComponent)
(component:SoftwareComponent)-[:HAS_VULNERABILITY]->(vuln:SoftwareVulnerability)

// Threat Intelligence
(actor:ThreatActor)-[:CONDUCTS]->(campaign:ThreatCampaign)
(campaign:ThreatCampaign)-[:USES_TECHNIQUE]->(mitre:MITREMapping)
(campaign:ThreatCampaign)-[:PRODUCES]->(ioc:IOC)

// Risk & Remediation
(asset:Asset)-[:HAS_RISK_SCORE]->(risk:RiskScore)
(vuln:Vulnerability)-[:REQUIRES]->(task:RemediationTask)
(task:RemediationTask)-[:PART_OF]->(plan:RemediationPlan)

// Compliance
(control:ComplianceControl)-[:MAPS_TO]->(control2:ComplianceControl)
(control:ComplianceControl)-[:HAS_ASSESSMENT]->(assessment:ComplianceAssessment)
(gap:ComplianceGap)-[:RELATES_TO]->(control:ComplianceControl)

// Organization
(employee:Employee)-[:BELONGS_TO]->(unit:OrganizationUnit)
(employee:Employee)-[:HAS_ROLE]->(role:Role)
(employee:Employee)-[:HAS_SKILL]->(skill:Skill)

// Vendor Equipment
(equipment:EquipmentModel)-[:MANUFACTURED_BY]->(vendor:Vendor)
(equipment:EquipmentModel)-[:COVERED_BY]->(contract:SupportContract)
```

---

## SECTION 2: QDRANT VECTOR COLLECTIONS

### 2.1 Collection Specifications

| Collection Name | Dimensions | Entity Types | Embedding Source |
|-----------------|------------|--------------|------------------|
| `ner11_sbom` | 384 | sbom, software_component, vulnerability | component name + description |
| `ner11_threat_intel` | 384 | threat_actor, campaign, ioc, mitre | actor name + description |
| `ner11_risk_scoring` | 384 | risk_score, asset_criticality, exposure | entity name + factors |
| `ner11_remediation` | 384 | task, plan, action | task title + CVE + description |
| `ner11_compliance` | 384 | control, mapping, assessment, gap | control_number + title + desc |
| `ner11_scanning` | 384 | profile, job, finding, target | finding title + description |
| `ner11_alerts` | 384 | alert, rule, notification, escalation | alert title + event_type |
| `ner11_economic_impact` | 384 | cost, investment, business_value | category + description |
| `ner11_demographics` | 384 | employee, org_unit, role, skill | name + title + department |
| `ner11_prioritization` | 384 | priority_item, urgency_factor | entity + factors |
| `ner11_vendor_equipment` | 384 | vendor, equipment, contract | vendor + model + description |

### 2.2 Minimum Data Volume Requirements

```yaml
minimum_viable_data:
  ner11_sbom: 500 components, 50 SBOMs, 200 vulnerabilities
  ner11_threat_intel: 100 actors, 50 campaigns, 500 IOCs, 200 MITRE mappings
  ner11_risk_scoring: 200 risk scores, 100 assets
  ner11_remediation: 100 tasks, 20 plans
  ner11_compliance: 500 controls (NIST+ISO+SOC2), 100 mappings
  ner11_scanning: 20 profiles, 100 findings
  ner11_alerts: 50 rules, 200 alerts
  ner11_economic_impact: 100 cost records, 20 scenarios
  ner11_demographics: 100 employees, 20 org units, 30 roles
  ner11_prioritization: 50 priority items
  ner11_vendor_equipment: 50 vendors, 200 equipment models
```

---

## SECTION 3: EXTERNAL DATA SOURCES

### 3.1 Free/Open Sources (Priority: HIGH)

| Source | URL | Data Type | APIs Supported |
|--------|-----|-----------|----------------|
| NVD (National Vulnerability Database) | https://nvd.nist.gov | CVE, CVSS, CPE | E03, E05, E08 |
| CISA KEV Catalog | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | Known Exploited Vulns | E03, E05, E12 |
| EPSS (Exploit Prediction) | https://www.first.org/epss | Exploit probability | E03, E05, E12 |
| MITRE ATT&CK | https://attack.mitre.org | Techniques, Tactics | E04, E09 |
| MITRE ATT&CK for ICS | https://attack.mitre.org/techniques/ics/ | ICS Techniques | E04, E15 |
| NIST SP 800-53 | https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final | Security Controls | E07 |
| CIS Benchmarks | https://www.cisecurity.org/cis-benchmarks | Configuration Baselines | E07, E08 |
| OWASP | https://owasp.org | Web Security | E08 |
| OSV.dev | https://osv.dev | Open Source Vulns | E03 |
| deps.dev | https://deps.dev | Dependency Analysis | E03 |
| SPDX License List | https://spdx.org/licenses | License Definitions | E03 |
| ICS-CERT Advisories | https://www.cisa.gov/uscert/ics | ICS Vulnerabilities | E04, E15 |
| AlienVault OTX | https://otx.alienvault.com | Threat Intelligence | E04 |

### 3.2 Commercial/Enterprise Sources (Recommended)

| Source | Data Type | APIs Supported | Notes |
|--------|-----------|----------------|-------|
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

```yaml
kaggle_datasets:
  cybersecurity_vulnerabilities:
    - dataset: "uciml/cybersecurity-intrusion-detection"
      relevance: E04, E08, E09
      records: 25,000+

    - dataset: "joebeachcapital/cve-mitre-attck"
      relevance: E03, E04, E05
      records: 180,000+ CVEs

    - dataset: "bithikasharma1/cyber-security-attacks"
      relevance: E04, E09
      records: 25,000+

  threat_intelligence:
    - dataset: "mrwellsdavid/malware-detection"
      relevance: E04, E08
      records: 10,000+

    - dataset: "solarmainframe/ids-intrusion-csv"
      relevance: E04, E09
      records: 500,000+

  compliance_frameworks:
    - dataset: "wsj/compliance-controls"  # Search for similar
      relevance: E07

  economic_data:
    - dataset: "ibm/data-breach-report"  # Search variations
      relevance: E10

  workforce_demographics:
    - dataset: "kaggle/hr-analytics"
      relevance: E11
      records: 15,000+
```

### 4.2 Kaggle API Commands

```bash
# Setup (credentials at /home/jim/2_OXOT_Projects_Dev/.kaggle/kaggle.json)
export KAGGLE_CONFIG_DIR=/home/jim/2_OXOT_Projects_Dev/.kaggle

# Search for cybersecurity datasets
kaggle datasets list -s "cybersecurity vulnerability" --sort-by votes

# Download specific datasets
kaggle datasets download -d uciml/cybersecurity-intrusion-detection
kaggle datasets download -d joebeachcapital/cve-mitre-attck

# Search for threat intelligence
kaggle datasets list -s "threat intelligence malware" --sort-by votes

# Search for compliance
kaggle datasets list -s "security compliance controls" --sort-by votes
```

---

## SECTION 5: PERPLEXITY RESEARCH PROMPTS

### 5.1 Vulnerability & SBOM Data (E03, E05)

```
PROMPT_E03_01:
"Provide a comprehensive list of the top 100 most critical CVEs from 2023-2024
affecting enterprise software, including: CVE ID, CVSS score, EPSS score,
affected products (CPE), exploit availability, and recommended remediation.
Format as JSON array."

PROMPT_E03_02:
"What are the most common open-source software licenses and their risk
classifications for enterprise use? Include: license name, SPDX identifier,
copyleft status, commercial use restrictions, and compliance requirements.
Format as structured table."

PROMPT_E03_03:
"List the top 50 most vulnerable open-source packages in npm, PyPI, and Maven
ecosystems from 2024, with CVE counts, severity distributions, and dependency
chain risks."
```

### 5.2 Threat Intelligence (E04)

```
PROMPT_E04_01:
"Provide detailed profiles of the top 20 APT groups targeting critical
infrastructure in 2024, including: group name, aliases, attributed nation-state,
primary motivations, target sectors, known TTPs (MITRE ATT&CK IDs), and active
campaigns. Format as JSON."

PROMPT_E04_02:
"What are the most commonly used MITRE ATT&CK techniques in ransomware attacks
from 2023-2024? Include technique ID, tactic, description, detection methods,
and mitigation strategies."

PROMPT_E04_03:
"List current active threat campaigns targeting energy sector and industrial
control systems (ICS), including threat actor attribution, attack vectors,
indicators of compromise (IOCs), and timeline."
```

### 5.3 Compliance Frameworks (E07)

```
PROMPT_E07_01:
"Provide a complete mapping between NIST SP 800-53 Rev 5 controls and ISO 27001:2022
controls, including: NIST control ID, ISO control ID, relationship type
(equivalent, partial, related), and mapping confidence score."

PROMPT_E07_02:
"What are the mandatory security controls for NERC CIP compliance for energy
utilities? Include control ID, requirement description, evidence requirements,
and common audit findings."

PROMPT_E07_03:
"List the top 50 most commonly failed SOC 2 Type II audit controls with failure
reasons, remediation recommendations, and evidence requirements."
```

### 5.4 Risk & Economic Impact (E05, E10)

```
PROMPT_E05_01:
"What are industry-standard risk scoring methodologies for cybersecurity?
Include: methodology name, scoring factors, weight distributions, and
calculation formulas. Compare CVSS, FAIR, OWASP Risk Rating."

PROMPT_E10_01:
"Provide industry benchmarks for cybersecurity incident costs by sector
(healthcare, finance, energy, manufacturing) including: average breach cost,
cost per record, downtime costs, regulatory fines, and recovery time.
Source: IBM, Ponemon, Verizon DBIR 2024."

PROMPT_E10_02:
"What are the typical ROI metrics and calculation methods for cybersecurity
investments? Include: risk reduction percentage, incident prevention value,
compliance cost avoidance, and insurance premium reduction."
```

### 5.5 ICS/OT & Vendor Equipment (E15)

```
PROMPT_E15_01:
"List the top 50 ICS/SCADA vendors and their equipment categories with:
vendor name, headquarters country, primary product categories, known
vulnerabilities count, support lifecycle status, and CISA advisories."

PROMPT_E15_02:
"What industrial control system equipment has reached end-of-life (EOL) in
2023-2024? Include manufacturer, model, EOL date, replacement recommendations,
and security implications."

PROMPT_E15_03:
"Provide ICS-CERT advisories summary for 2024 including: advisory ID, affected
vendor, affected products, vulnerability type, CVSS score, and mitigation status."
```

### 5.6 Demographics & Workforce (E11)

```
PROMPT_E11_01:
"What are industry benchmarks for cybersecurity team structures and staffing
ratios by organization size? Include: team roles, FTE ratios, skill requirements,
and certification expectations."

PROMPT_E11_02:
"Provide typical organizational structures for cybersecurity departments in
Fortune 500 companies, including reporting lines, team compositions, and
role definitions."
```

---

## SECTION 6: E30 INGESTION FORMAT SPECIFICATIONS

### 6.1 Standard Entity Format

```json
{
  "entity_type": "string (e.g., ThreatActor, ComplianceControl)",
  "entity_id": "string (UUID or natural key)",
  "customer_id": "string (SYSTEM for baseline, customer_id for tenant)",
  "namespace": "string (optional)",
  "properties": {
    "field1": "value1",
    "field2": "value2"
  },
  "embedding_text": "string (text to generate 384-dim vector from)",
  "relationships": [
    {
      "type": "RELATIONSHIP_TYPE",
      "target_entity_type": "string",
      "target_entity_id": "string",
      "properties": {}
    }
  ],
  "metadata": {
    "source": "string (data source identifier)",
    "ingestion_date": "ISO8601 timestamp",
    "version": "string"
  }
}
```

### 6.2 Batch Ingestion Format

```json
{
  "batch_id": "string (UUID)",
  "batch_type": "baseline | customer | update",
  "customer_id": "SYSTEM | specific_customer",
  "target_collection": "ner11_collection_name",
  "entities": [
    { /* entity objects */ }
  ],
  "relationships": [
    { /* relationship objects for Neo4j */ }
  ],
  "processing_instructions": {
    "generate_embeddings": true,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "upsert_mode": "insert | update | upsert",
    "validate_schema": true
  }
}
```

### 6.3 Source-Specific Transformers

```yaml
data_transformers:
  nvd_cve:
    source_format: NVD JSON 2.0
    target_entity: SoftwareVulnerability
    field_mappings:
      cve.id: cve_id
      cve.metrics.cvssMetricV31[0].cvssData.baseScore: cvss_score
      cve.descriptions[0].value: description
    embedding_fields: [description, cve_id]

  mitre_attack:
    source_format: STIX 2.1 Bundle
    target_entity: MITREMapping
    field_mappings:
      external_references[0].external_id: technique_id
      kill_chain_phases[0].phase_name: tactic
      name: technique_name
      description: description
    embedding_fields: [technique_name, description]

  nist_800_53:
    source_format: OSCAL JSON
    target_entity: ComplianceControl
    field_mappings:
      id: control_id
      title: title
      parts[0].prose: description
    embedding_fields: [control_id, title, description]
```

---

## SECTION 7: DATA COLLECTION PRIORITY MATRIX

### 7.1 Phase 1: Critical Baseline (Week 1-2)

| Priority | Data Type | Source | APIs | Volume |
|----------|-----------|--------|------|--------|
| P0 | CVE/CVSS Data | NVD API | E03, E05, E08 | 200K+ CVEs |
| P0 | MITRE ATT&CK | STIX Bundle | E04, E09 | 600+ techniques |
| P0 | NIST 800-53 Controls | OSCAL | E07 | 1,100+ controls |
| P0 | CISA KEV | JSON Feed | E03, E05, E12 | 1,000+ vulns |
| P1 | ISO 27001 Controls | Manual/Commercial | E07 | 114 controls |
| P1 | CIS Benchmarks | CIS API | E07, E08 | 100+ benchmarks |

### 7.2 Phase 2: Enrichment Data (Week 3-4)

| Priority | Data Type | Source | APIs | Volume |
|----------|-----------|--------|------|--------|
| P1 | ICS-CERT Advisories | CISA Feed | E04, E15 | 500+ advisories |
| P1 | EPSS Scores | FIRST API | E03, E05, E12 | All CVEs |
| P2 | Threat Actor Profiles | MITRE Groups | E04 | 150+ actors |
| P2 | ICS Vendor Catalog | Manual Research | E15 | 100+ vendors |
| P2 | Industry Cost Benchmarks | Perplexity/Reports | E10 | Benchmark data |

### 7.3 Phase 3: Extended Data (Week 5+)

| Priority | Data Type | Source | APIs | Volume |
|----------|-----------|--------|------|--------|
| P2 | Kaggle Datasets | Kaggle API | Multiple | Variable |
| P2 | OSV.dev Vulnerabilities | OSV API | E03 | 100K+ vulns |
| P3 | Commercial Threat Feeds | AlienVault OTX | E04 | Ongoing |
| P3 | Compliance Evidence Templates | Manual | E07 | 50+ templates |

---

## SECTION 8: AUTOMATION SCRIPTS

### 8.1 Kaggle Data Download Script

```bash
#!/bin/bash
# File: scripts/download_kaggle_datasets.sh

export KAGGLE_CONFIG_DIR=/home/jim/2_OXOT_Projects_Dev/.kaggle
OUTPUT_DIR=/home/jim/2_OXOT_Projects_Dev/data/kaggle

mkdir -p $OUTPUT_DIR

# Cybersecurity datasets
kaggle datasets download -d uciml/cybersecurity-intrusion-detection -p $OUTPUT_DIR
kaggle datasets download -d mrwellsdavid/malware-detection -p $OUTPUT_DIR

# Search and list available
kaggle datasets list -s "cve vulnerability" --sort-by votes > $OUTPUT_DIR/cve_datasets.txt
kaggle datasets list -s "mitre attack" --sort-by votes > $OUTPUT_DIR/mitre_datasets.txt
kaggle datasets list -s "compliance security" --sort-by votes > $OUTPUT_DIR/compliance_datasets.txt
```

### 8.2 NVD CVE Download Script

```bash
#!/bin/bash
# File: scripts/download_nvd_cves.sh

OUTPUT_DIR=/home/jim/2_OXOT_Projects_Dev/data/nvd
mkdir -p $OUTPUT_DIR

# Download recent CVEs (last 120 days)
curl -o $OUTPUT_DIR/nvd_recent.json \
  "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=2000"

# Download CISA KEV
curl -o $OUTPUT_DIR/cisa_kev.json \
  "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

# Download EPSS scores
curl -o $OUTPUT_DIR/epss_scores.csv \
  "https://epss.cyentia.com/epss_scores-current.csv.gz"
```

### 8.3 MITRE ATT&CK Download Script

```bash
#!/bin/bash
# File: scripts/download_mitre_attack.sh

OUTPUT_DIR=/home/jim/2_OXOT_Projects_Dev/data/mitre
mkdir -p $OUTPUT_DIR

# Enterprise ATT&CK
curl -o $OUTPUT_DIR/enterprise-attack.json \
  "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

# ICS ATT&CK
curl -o $OUTPUT_DIR/ics-attack.json \
  "https://raw.githubusercontent.com/mitre/cti/master/ics-attack/ics-attack.json"

# Mobile ATT&CK
curl -o $OUTPUT_DIR/mobile-attack.json \
  "https://raw.githubusercontent.com/mitre/cti/master/mobile-attack/mobile-attack.json"
```

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
|-------------|------------|-----------|------------|
| E03 SBOM | `/api/v2/sbom` | 25 | ner11_sbom |
| E04 Threat Intel | `/api/v2/threat-intel` | 28 | ner11_threat_intel |
| E05 Risk Scoring | `/api/v2/risk-scoring` | 24 | ner11_risk_scoring |
| E06 Remediation | `/api/v2/remediation` | 22 | ner11_remediation |
| E07 Compliance | `/api/v2/compliance` | 26 | ner11_compliance |
| E08 Scanning | `/api/v2/scanning` | 24 | ner11_scanning |
| E09 Alerts | `/api/v2/alerts` | 28 | ner11_alerts |
| E10 Economic | `/api/v2/economic-impact` | 27 | ner11_economic_impact |
| E11 Demographics | `/api/v2/demographics` | 24 | ner11_demographics |
| E12 Prioritization | `/api/v2/prioritization` | 28 | ner11_prioritization |
| E15 Vendor | `/api/v2/vendor-equipment` | 25 | ner11_vendor_equipment |

### 10.2 Contact & Resources

- **Container API**: http://localhost:8000 (ner11-gold-api)
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **Neo4j Browser**: http://localhost:7474
- **Repository**: https://github.com/Planet9V/agent-optimization-deployment

---

**Document Status:** READY FOR INGESTION PLANNING
**Next Action:** Execute Phase 1 data collection scripts
**Estimated Completion:** 2-4 weeks for full baseline data
