# DATA_SOURCES.md - Enhancement E18 Data Sources
**File:** DATA_SOURCES.md
**Created:** 2025-11-26 00:00:00 UTC
**Modified:** 2025-11-26 00:00:00 UTC
**Version:** v1.0.0
**Author:** AEON FORGE System Architecture Designer
**Purpose:** Comprehensive data source catalog for Lacanian RSI triad and Borromean knot analysis
**Status:** ACTIVE

---

## 1. REAL REGISTER DATA SOURCES

### 1.1 Threat and Infrastructure Reality

**MITRE ATT&CK Coverage Data**
- **Source**: https://attack.mitre.org/
- **Access**: Public API, Navigator tool, local ATT&CK implementation
- **Purpose**: Map actual detection coverage against threat technique landscape
- **Extraction**:
  - Total techniques in ATT&CK Enterprise (∼800 techniques)
  - Techniques covered by deployed sensors (SIEM rules, EDR, NDR)
  - Gap analysis: Uncovered techniques
- **Key Metrics**:
  - Coverage percentage: `(Covered techniques / Total techniques) × 100`
  - High-risk gaps: Uncovered techniques with high prevalence
- **Usage in E18**: Real register health, threat coverage component

**Security Infrastructure Inventory**
- **Sources**:
  - Asset management systems (ServiceNow CMDB, Qualys Asset Inventory)
  - SIEM deployment data (Splunk deployment matrix, Elastic agent coverage)
  - EDR console (CrowdStrike Falcon Discover, SentinelOne coverage dashboard)
  - Network monitoring (Zeek sensor placement, Darktrace coverage map)
- **Access**: Organizational internal systems
- **Purpose**: Actual infrastructure capabilities vs requirements
- **Extraction**:
  - Total assets vs monitored assets (coverage percentage)
  - Sensor deployment density (agents per subnet, per OS type)
  - Technical debt indicators (outdated systems, unpatched vulnerabilities)
  - Tool sprawl (number of overlapping security tools)
- **Key Metrics**:
  - Infrastructure coverage: `(Monitored assets / Total assets)`
  - Technical debt score: `(Systems >5yrs old + Vulns CVSS>7 unpat ched >30d) / Total systems`
- **Usage in E18**: Real register infrastructure reality score

**Incident Response Database**
- **Sources**:
  - Internal IR case management (ServiceNow Security Incident Response, Jira)
  - SIEM incident database (Splunk Notable Events, Chronicle cases)
  - Post-incident review repository
- **Access**: Organizational internal
- **Purpose**: Actual security incidents (reality of breaches)
- **Extraction**:
  - Total incidents per period
  - Detection method distribution (proactive internal, external notification, user report)
  - Incident handling metrics (MTTD, MTTR, containment success)
  - Breach outcomes (data exfiltrated, systems compromised, business impact)
  - Actual threat actors encountered (attribution data)
  - Actual attack vectors used (initial access methods)
- **Key Metrics**:
  - Proactive detection rate: `(Internally detected / Total incidents)`
  - Incident handling effectiveness: `(Contained & remediated / Total incidents)`
  - Breach rate: `(Incidents with data loss / Total incidents)`
- **Usage in E18**: Real register incident reality, validation of threat model

**Budget and Resource Data**
- **Sources**:
  - Finance systems (security budget allocations)
  - HR systems (headcount, salaries, turnover data)
  - Procurement records (tool spending, contracts)
- **Access**: Finance and HR systems
- **Purpose**: Material constraints on security operations
- **Extraction**:
  - Security budget as % of IT budget (industry benchmark: 8-12%)
  - Security budget as % of revenue (industry benchmark: 0.5-1.0%)
  - Headcount adequacy: FTE per assets/users (benchmark: 0.5 FTE per 1000 employees)
  - Turnover rate (annual attrition percentage)
- **Key Metrics**:
  - Budget adequacy: `(Actual security budget / Industry benchmark budget)`
  - Headcount adequacy: `(Actual FTE / Required FTE per coverage requirements)`
- **Usage in E18**: Real register budget constraints, infrastructure reality

### 1.2 Actual Threat Landscape

**Threat Intelligence Feeds**
- **Sources**:
  - Commercial TI platforms (Recorded Future, ThreatConnect, Anomali)
  - Open-source feeds (AlienVault OTX, MISP, abuse.ch)
  - Government advisories (CISA alerts, NSA advisories, NCSC bulletins)
- **Access**: Subscription services, public feeds
- **Purpose**: Actual threats targeting the organization or industry
- **Extraction**:
  - Threat actors active in industry
  - TTPs observed in recent campaigns
  - Indicators of Compromise (IOCs) for correlation
  - Vulnerability exploits in the wild
- **Key Metrics**:
  - Threat actor count targeting industry
  - Average TTP sophistication level
  - Critical vulnerabilities actively exploited
- **Usage in E18**: Real register threat coverage, validation baseline for Imaginary register

**Vulnerability Scan Data**
- **Sources**:
  - Vulnerability scanners (Tenable Nessus, Qualys VMDR, Rapid7 InsightVM)
  - Application security testing (SAST, DAST results)
  - Cloud security posture management (Wiz, Orca, Prisma Cloud)
- **Access**: Internal vulnerability management systems
- **Purpose**: Actual exploitable weaknesses in infrastructure
- **Extraction**:
  - Total vulnerabilities by severity (Critical, High, Medium, Low)
  - Vulnerabilities with known exploits
  - Patch lag time (time from patch availability to deployment)
  - Vulnerability remediation rate
- **Key Metrics**:
  - Critical vulnerability backlog
  - Mean time to remediate (MTTR) for critical vulns
  - Exploitable vulnerability density: `(Vulns with exploits / Total assets)`
- **Usage in E18**: Real register technical debt component

---

## 2. SYMBOLIC REGISTER DATA SOURCES

### 2.1 Policies and Procedures

**Security Policy Repository**
- **Sources**:
  - Policy management systems (LogicManager, PolicyTech)
  - Document repositories (SharePoint, Confluence, Google Drive)
  - Compliance management platforms (ServiceNow GRC, Archer)
- **Access**: Organizational internal
- **Purpose**: Symbolic rules governing security operations
- **Extraction**:
  - Total policy count
  - Policy age distribution (last update dates)
  - Policy complexity (length, readability scores)
  - Policy-threat alignment (do policies address actual threats?)
  - Policy utilization (referenced in incidents, trainings, audits)
- **Key Metrics**:
  - Policy coverage of threats: `(Threats with policy coverage / Total threats)`
  - Policy utilization rate: `(Policies used in operations / Total policies)`
  - Bureaucratic bloat: `1 - Policy utilization rate`
- **Usage in E18**: Symbolic register policy effectiveness

**Standard Operating Procedures (SOPs)**
- **Sources**:
  - Runbook repositories (PagerDuty, Rundeck)
  - Incident response playbooks (SOAR platforms, internal wikis)
  - Change management procedures (ITIL process docs)
- **Access**: Organizational internal
- **Purpose**: Symbolic operational guidance
- **Extraction**:
  - SOP count by function (IR, vuln management, access control, etc.)
  - SOP usage frequency (how often procedures are followed)
  - SOP deviation rate (incidents handled off-script)
  - SOP update frequency (staleness)
- **Key Metrics**:
  - SOP adherence rate: `(Incidents following playbook / Total incidents)`
  - SOP freshness: `(SOPs updated <6 months / Total SOPs)`
- **Usage in E18**: Symbolic register organizational structure

**Compliance Framework Documentation**
- **Sources**:
  - Certification documentation (ISO 27001 ISMS, SOC 2 reports, PCI-DSS AOC)
  - Audit reports (internal audit, external audit findings)
  - Regulatory requirement mappings
- **Access**: Compliance team, audit documentation
- **Purpose**: Symbolic compliance structure
- **Extraction**:
  - Frameworks in use (NIST CSF, ISO 27001, SOC 2, PCI-DSS, HIPAA, etc.)
  - Compliance coverage (% of required controls implemented)
  - Audit findings (open vs closed)
  - Compliance effort (FTE dedicated to compliance)
- **Key Metrics**:
  - Compliance coverage: `(Implemented controls / Required controls)`
  - Compliance efficiency: `(Security value / Compliance effort)`
- **Usage in E18**: Symbolic register compliance coverage component

### 2.2 Communication and Language

**Team Communication Logs**
- **Sources**:
  - Slack/Teams channels (security team workspace)
  - Email archives (security distribution lists)
  - Meeting transcripts (recorded meetings, minutes)
  - Incident communication logs (war room chats, status updates)
- **Access**: Organizational internal, requires consent
- **Purpose**: Symbolic communication effectiveness
- **Extraction Methods**:
  - **Readability analysis**: Flesch Reading Ease, Gunning Fog Index
  - **Jargon density**: Technical terms per message
  - **Cross-functional communication**: Messages between departments
  - **Response time**: Time from message to reply
  - **Information propagation**: How quickly critical info spreads
- **Key Metrics**:
  - Average communication clarity: `(Sum of readability scores / Total messages)`
  - Cross-functional ratio: `(Cross-department messages / Total messages)`
  - Response efficiency: `1 / (1 + Avg response time / 4 hours)`
- **Usage in E18**: Symbolic register communication clarity

**Incident Classification Data**
- **Sources**:
  - SIEM incident categorization (Splunk ES Notable Event classification)
  - Ticketing system categories (ServiceNow incident categories)
  - ATT&CK technique tagging (incident-to-TTP mapping)
- **Access**: SIEM, ticketing systems
- **Purpose**: Symbolic language for describing threats
- **Extraction**:
  - Classification schema in use (custom vs standard)
  - Classification consistency (inter-rater reliability)
  - Language shared with stakeholders (business-understandable categories)
- **Key Metrics**:
  - Classification consistency: `(Incidents with consistent categorization / Total incidents)`
  - Shared language adoption: `(Stakeholders using security terminology correctly)`
- **Usage in E18**: Symbolic register language patterns

### 2.3 Organizational Structure

**Organizational Charts and Role Definitions**
- **Sources**:
  - HR systems (org chart data, job descriptions)
  - Workforce planning documents
  - RACI matrices (Responsible, Accountable, Consulted, Informed)
- **Access**: HR systems, internal documentation
- **Purpose**: Symbolic organizational hierarchy and role clarity
- **Extraction**:
  - Hierarchy depth (levels from CISO to analyst)
  - Span of control (direct reports per manager)
  - Role clarity (well-defined responsibilities vs ambiguous)
  - Reporting structure (single vs multiple managers)
- **Key Metrics**:
  - Role clarity score: `(Roles with clear responsibilities / Total roles)`
  - Hierarchy appropriateness: `1 - |Actual depth - Optimal depth| / Optimal depth`
  - Reporting clarity: `1 - (Reporting conflicts / Total roles)`
- **Usage in E18**: Symbolic register organizational structure score

---

## 3. IMAGINARY REGISTER DATA SOURCES

### 3.1 Team Self-Image and Identity

**Team Communications (Self-Referential Language)**
- **Sources**: Same as Symbolic communication logs, different analysis
- **Access**: Organizational internal, consent required
- **Purpose**: Extract team self-image and identity
- **Extraction Methods**:
  - **NLP for self-referential statements**: "We are...", "Our team...", "We're good at..."
  - **Strength/weakness identification**: What team claims to excel at vs struggle with
  - **Identity keywords**: "Elite", "reactive", "under-resourced", "proactive", etc.
  - **Comparative language**: Comparisons to other teams, industry, ideal state
- **Key Metrics**:
  - Self-image inflation: `Avg(Self-assessed capability - Actual capability)`
  - Identity consistency: Coherence of self-image across team members
- **Usage in E18**: Imaginary register self-image accuracy

**Employee Surveys and Culture Assessments**
- **Sources**:
  - Annual employee engagement surveys
  - Security team-specific pulse surveys
  - Culture assessment tools (Denison Organizational Culture Survey, OCAI)
  - Psychological safety assessments
- **Access**: HR systems, survey platforms
- **Purpose**: Team morale, aspirations, fears
- **Extraction**:
  - Morale score (job satisfaction, engagement)
  - Professional development aspirations
  - Fear indicators (job security anxiety, workload stress)
  - Team cohesion (collaboration quality, trust levels)
- **Key Metrics**:
  - Morale score: `Avg(Satisfaction + Engagement + Cohesion) / 3`
  - Aspiration realism: Comparison of stated goals to resource availability
  - Fear intensity: `Avg(Anxiety + Stress markers) / Max`
- **Usage in E18**: Imaginary register fear/morale analysis

**Exit Interview Data**
- **Sources**: HR exit interview database
- **Access**: HR systems (aggregate data, not individual)
- **Purpose**: Reality-check on morale claims, identify imaginary-reality gaps
- **Extraction**:
  - Turnover reasons (burnout, career growth, compensation, culture)
  - Team perception at departure (what did they think vs what surveys said)
  - Turnover rate by role and tenure
- **Key Metrics**:
  - Turnover rate: `(Departures / Avg headcount) × 100`
  - Morale reality check: `1 - (Turnover rate / 0.40)` (40% industry baseline)
- **Usage in E18**: Imaginary register morale validation

### 3.2 Aspirations and Perceptions

**Team Goal and Vision Statements**
- **Sources**:
  - Strategic planning documents
  - Team OKRs (Objectives and Key Results)
  - CISO vision presentations
  - Roadmap documents
- **Access**: Organizational internal
- **Purpose**: Team aspirations and desired future state
- **Extraction**:
  - Aspirational statements ("We want to become...", "Our goal is...")
  - Timeline for aspirations
  - Resource requirements for aspirations
  - Organizational support indicators
- **Key Metrics**:
  - Aspiration realism: `(Org support × Resource availability × Timeline realism)`
  - Realistic vs unrealistic aspiration ratio
- **Usage in E18**: Imaginary register aspiration realism

**Threat Perception Analysis**
- **Sources**:
  - Threat intelligence reports (written by team)
  - Executive briefings on threats
  - Team discussions about threats (Slack, meetings)
- **Access**: Organizational internal
- **Purpose**: Imagined threat landscape vs actual threats
- **Extraction**:
  - Imagined threats (what team talks about most)
  - Emphasis distribution (% of attention to each threat type)
  - Compare to actual incident data (from Real register)
- **Key Metrics**:
  - Threat perception alignment: `(Imagined threats ∩ Actual threats) / Actual threats`
  - Over-emphasis threats: Imagined threats not in actual incident data
  - Under-emphasis threats: Actual threats not in team's focus
- **Usage in E18**: Imaginary register threat perception alignment

**External Benchmarking Data**
- **Sources**:
  - Industry benchmarks (Gartner, Forrester, SANS)
  - Peer organization data (informal benchmarking, consortiums)
  - Maturity model assessments (NIST CSF maturity, CMMI)
- **Access**: Public reports, peer sharing, assessment services
- **Purpose**: Reality-check team self-assessments
- **Extraction**:
  - Benchmark capabilities for industry/size
  - Team self-assessment vs benchmark
  - Capability gaps
- **Key Metrics**:
  - Self-image accuracy: `1 - |Self-assessment - Benchmark| / Benchmark`
- **Usage in E18**: Imaginary register self-image accuracy validation

### 3.3 Organizational Perception of Security Team

**Executive and Board Communications**
- **Sources**:
  - Board meeting minutes (security discussions)
  - Executive emails and memos
  - Annual reports (cybersecurity risk disclosure)
  - Budget justification documents
- **Access**: Organizational confidential
- **Purpose**: How organization perceives security team
- **Extraction**:
  - Language about security team ("strong", "adequate", "under-resourced")
  - Budget allocation signals (% of IT budget)
  - Expectations placed on team (realistic vs unrealistic)
  - Blame vs support language post-incident
- **Key Metrics**:
  - Organizational perception sentiment: NLP sentiment analysis
  - Budget perception: `(Actual budget / IT budget) / Industry benchmark`
  - Stakeholder satisfaction (from next data source)
- **Usage in E18**: Imaginary register organizational perception component

**Stakeholder Feedback**
- **Sources**:
  - Internal customer satisfaction surveys
  - Feedback from business units on security services
  - Incident response effectiveness ratings
- **Access**: Survey platforms, feedback systems
- **Purpose**: External validation of team perception
- **Extraction**:
  - Satisfaction scores by service (IR, access mgmt, consulting)
  - Net Promoter Score (NPS) for security team
  - Qualitative feedback themes
- **Key Metrics**:
  - Stakeholder satisfaction: `Avg(Service satisfaction scores)`
- **Usage in E18**: Imaginary register organizational perception

---

## 4. BORROMEAN KNOT DYNAMICS DATA SOURCES

### 4.1 Register Interaction Tracking

**Historical Knot Health Data**
- **Sources**: E18 analysis database (time series from previous E18 runs)
- **Access**: Internal E18 system
- **Purpose**: Track knot stability over time, identify trends
- **Extraction**:
  - Time series of Real, Symbolic, Imaginary register health scores
  - Historical circulation integral values
  - Historical stability scores
  - Register failure events (if any)
- **Key Metrics**:
  - Trend slope: Linear regression on stability score over time
  - Time to failure extrapolation: `(Current stability - Failure threshold) / |Trend slope|`
- **Usage in E18**: Knot failure prediction (Agent 7), trend analysis

**Incident Impact on Registers**
- **Sources**: Incident database + post-incident assessments
- **Access**: Organizational internal
- **Purpose**: Observe how actual incidents (Real) affect Symbolic and Imaginary
- **Extraction**:
  - Post-incident policy changes (Real → Symbolic flow)
  - Post-incident team morale shifts (Real → Imaginary flow)
  - Policy adherence during incidents (Symbolic → Real flow)
  - Team identity narratives post-incident (Imaginary → Real flow)
- **Key Metrics**:
  - R·dS strength: `(Incidents leading to policy updates / Total incidents)`
  - Real impact on Imaginary: Sentiment analysis pre/post major incidents
- **Usage in E18**: Circulation integral calculation (Agent 4)

### 4.2 Team Topology and Interaction

**Team Member Profiles**
- **Sources**:
  - HR data (roles, tenure, certifications)
  - Individual performance reviews
  - Skills assessments
  - Project assignment history
- **Access**: HR systems, performance management systems
- **Purpose**: Map individual team member positions in RSI space
- **Extraction**:
  - Technical vs strategic role distribution
  - Hands-on (Real) vs policy (Symbolic) vs leadership (Imaginary) work
  - Cross-register engagement (who bridges registers?)
- **Key Metrics**:
  - Individual RSI vectors: `[Real engagement, Symbolic engagement, Imaginary engagement]`
  - RSI bridgers: Team members with balanced RSI vectors
  - Isolated members: Stuck in single register
- **Usage in E18**: Group topology modeling (Agent 5)

**Collaboration and Interaction Logs**
- **Sources**:
  - Slack/Teams direct messages and channel participation
  - Email interaction patterns (who talks to whom)
  - Meeting attendance and participation
  - Ticket collaboration (assignment, escalation, handoffs)
- **Access**: Communication platforms, collaboration tools
- **Purpose**: Map interaction topology across team
- **Extraction**:
  - Interaction frequency matrix (pairwise communication counts)
  - Interaction content classification (Real, Symbolic, or Imaginary topics)
  - Network topology (centralized, distributed, siloed)
- **Key Metrics**:
  - Network density: `(Actual connections / Possible connections)`
  - Topology type: Graph analysis (star, mesh, hierarchical)
  - RSI interaction distribution: % of interactions per register type
- **Usage in E18**: Group topology modeling (Agent 5)

### 4.3 Sinthome Detection

**Organizational Narratives and Stories**
- **Sources**:
  - Company founding documents
  - Security team origin stories
  - Major incident retrospectives
  - Team building event documentation
  - Internal newsletters, blogs
- **Access**: Organizational archives, internal communications
- **Purpose**: Identify founding traumas, cultural stories
- **Extraction**:
  - Founding events: "We were created because..."
  - Traumatic incidents: Major breaches that shaped team identity
  - Cultural mantras: Repeated slogans, values statements
  - Heroic narratives: Stories of team triumphs used for cohesion
- **Key Metrics**:
  - Story usage frequency: How often founding story is invoked
  - Emotional charge: Sentiment intensity around founding events
- **Usage in E18**: Sinthome identification (Agent 6), founding trauma detection

**Cultural Artifacts**
- **Sources**:
  - Team rituals (weekly sync structure, incident response traditions)
  - Shared tools and processes (the SIEM "everyone loves to hate")
  - Physical or virtual artifacts (team logos, Slack custom emojis, awards)
- **Access**: Observation, team member interviews
- **Purpose**: Identify material and cultural sinthomes
- **Extraction**:
  - Ritual frequency and participation
  - Tool dependency despite dissatisfaction
  - Artifact centrality to team identity
- **Key Metrics**:
  - Ritual adherence: `(Team members participating / Total team)`
  - Tool dependency: `(Critical processes relying on tool / Total processes)`
- **Usage in E18**: Sinthome identification (Agent 6), material sinthome

**Scapegoating and Blame Patterns**
- **Sources**: Team communications, incident postmortems
- **Access**: Communication logs, incident documentation
- **Purpose**: Detect pathological sinthomes (scapegoating)
- **Extraction**:
  - External blame language ("management doesn't...", "they never...")
  - Scapegoat identification (who/what is repeatedly blamed)
  - Frequency of blame vs learning language
- **Key Metrics**:
  - Scapegoating frequency: `(Blame statements / Total postmortem statements)`
  - Blame target consistency: Same entity repeatedly blamed
- **Usage in E18**: Sinthome identification (Agent 6), pathological sinthome detection

---

## 5. CONTEXTUAL AND VALIDATION DATA

### 5.1 Industry Benchmarks and Standards

**Security Maturity Benchmarks**
- **Sources**:
  - Gartner Security & Risk Management research
  - Forrester Wave reports
  - SANS Security Maturity Self-Assessment
  - NIST Cybersecurity Framework maturity levels
- **Access**: Public reports, subscription services
- **Purpose**: Reality-check team self-assessments and aspirations
- **Extraction**:
  - Industry maturity distribution (% of orgs at each level)
  - Capability benchmarks by industry vertical and org size
  - Investment benchmarks (budget, headcount)
- **Key Metrics**:
  - Maturity gap: `(Team self-assessed maturity - Actual benchmark maturity)`
  - Investment adequacy: `(Actual investment / Benchmark investment)`
- **Usage in E18**: Imaginary register self-image validation, aspiration realism

**Team Performance Benchmarks**
- **Sources**:
  - SANS SOC Survey
  - Ponemon Cost of a Data Breach Report
  - Verizon DBIR incident response statistics
  - Industry peer groups and consortiums
- **Access**: Public annual reports, peer sharing
- **Purpose**: Benchmark Real register performance
- **Extraction**:
  - Median MTTD/MTTR by industry
  - Average breach costs
  - Detection method distribution
  - Coverage percentages
- **Key Metrics**:
  - Performance percentile: Where team ranks vs peers
- **Usage in E18**: Real register reality-check, self-image validation

### 5.2 Historical Crisis and Resilience Data

**Major Incident History**
- **Sources**: Internal incident database (focus on "major incident" classification)
- **Access**: Organizational internal
- **Purpose**: Identify historical knot stress events
- **Extraction**:
  - Major incidents timeline
  - Team response effectiveness during crises
  - Post-incident team morale shifts
  - Organizational changes triggered by incidents (budget, headcount, policy)
- **Key Metrics**:
  - Crisis frequency: Major incidents per year
  - Crisis impact on registers: Pre/post incident register health deltas
  - Sinthome activation: Was sinthome invoked during crisis?
- **Usage in E18**: Historical knot resilience patterns, sinthome effectiveness validation

**Organizational Change Events**
- **Sources**:
  - Merger/acquisition history
  - Leadership transitions (CISO changes, executive turnover)
  - Major reorganizations
  - Budget cuts or expansions
- **Access**: Organizational HR and corporate communications
- **Purpose**: Identify external stressors on knot stability
- **Extraction**:
  - Change event timeline
  - Team stability during changes (turnover, morale)
  - Register impacts (e.g., merger disrupts Symbolic policies, budget cut hits Real infrastructure)
- **Key Metrics**:
  - Change resilience: Team knot stability before/after major changes
- **Usage in E18**: Knot failure prediction context, external stressor identification

---

## 6. DATA COLLECTION METHODOLOGY

### 6.1 Ethical Considerations

**Privacy and Consent**:
- **Team communications**: Aggregate analysis only, individual consent for qualitative studies
- **Employee surveys**: Anonymous aggregation, no individual identification
- **Performance data**: Team-level metrics, not individual performance evaluation
- **Purpose limitation**: Data used solely for team health and security improvement, not HR decisions

**Transparency**:
- Team informed of E18 analysis purpose and methods
- Results shared with team for validation
- Opportunity for team input on interpretations
- No punitive use of psychological insights

### 6.2 Data Quality Standards

**Source Credibility Tiers**:
- **Tier 1 (High)**: MITRE ATT&CK, official benchmark reports, audited financial data
- **Tier 2 (Moderate)**: Commercial TI, survey data, internal documentation
- **Tier 3 (Low)**: Self-reported assessments, anecdotal feedback

**Data Freshness Requirements**:
- **Real register**: < 7 days for threat/incident data, < 30 days for infrastructure
- **Symbolic register**: < 90 days for policies, < 30 days for communications
- **Imaginary register**: < 90 days for surveys, < 30 days for morale indicators
- **Knot dynamics**: < 30 days for all inputs (knot can shift rapidly)

**Validation Methods**:
- **Triangulation**: Cross-validate Imaginary (self-image) against Real (benchmarks) and Symbolic (policies)
- **Longitudinal**: Track register health over time to validate trends
- **Peer review**: External assessment to validate internal team perceptions

### 6.3 Data Integration Architecture

**Data Pipeline**:
1. **Collection**: Automated feeds (SIEM, MITRE, surveys), manual extraction (policies, narratives)
2. **Normalization**: Map to common schema (RealRegister, SymbolicRegister, ImaginaryRegister vectors)
3. **Storage**: Neo4j graph database + time-series database (InfluxDB, Prometheus)
4. **Analysis**: Agent swarm processing (per TASKMASTER)
5. **Validation**: Quality checks (Agent 10)
6. **Presentation**: Dashboards (Grafana), reports (Markdown), intervention roadmaps

**Update Frequency**:
- **Real-time**: SIEM incident creation, infrastructure alerts
- **Daily**: Threat intel feeds, communication analysis
- **Weekly**: Policy review, budget tracking
- **Monthly**: Surveys, morale assessments, knot health reports
- **Quarterly**: Comprehensive RSI reassessment, intervention effectiveness review

---

## 7. DATA SOURCE SUMMARY TABLE

| Category | Source | Update Frequency | Credibility | Primary Use |
|----------|--------|------------------|-------------|-------------|
| **Real Register - Threats** | MITRE ATT&CK Coverage | Daily | Tier 1 | Threat coverage, detection gaps |
| | Threat Intelligence Feeds | Daily | Tier 2 | Actual threat landscape |
| | Incident Response Database | Per incident | Tier 1 | Incident reality, breach rate |
| | Vulnerability Scan Data | Weekly | Tier 1 | Technical debt, exploitable weaknesses |
| **Real Register - Infrastructure** | Security Infrastructure Inventory | Monthly | Tier 1 | Coverage, technical debt |
| | Budget and Resource Data | Quarterly | Tier 1 | Material constraints |
| **Symbolic Register - Policies** | Security Policy Repository | Quarterly | Tier 1 | Policy effectiveness |
| | Standard Operating Procedures | Monthly | Tier 1 | Operational structure |
| | Compliance Framework Docs | Annually | Tier 1 | Compliance coverage |
| **Symbolic Register - Communication** | Team Communication Logs | Daily | Tier 2 | Communication clarity |
| | Incident Classification Data | Per incident | Tier 1 | Shared language |
| | Organizational Charts | Quarterly | Tier 1 | Role clarity, hierarchy |
| **Imaginary Register - Identity** | Team Communications (self-referential) | Daily | Tier 2 | Self-image, aspirations |
| | Employee Surveys | Quarterly | Tier 2 | Morale, fear, cohesion |
| | Exit Interview Data | Ongoing | Tier 2 | Morale validation, turnover |
| **Imaginary Register - Perceptions** | Team Goal/Vision Statements | Quarterly | Tier 2 | Aspiration realism |
| | Threat Perception Analysis | Weekly | Tier 2 | Imagined vs actual threats |
| | External Benchmarking Data | Annually | Tier 2 | Self-image validation |
| | Executive Communications | Monthly | Tier 1 | Organizational perception |
| | Stakeholder Feedback | Quarterly | Tier 2 | Perception validation |
| **Knot Dynamics** | Historical Knot Health Data | Monthly | Tier 1 | Trend analysis, prediction |
| | Incident Impact on Registers | Per incident | Tier 1 | Circulation measurement |
| | Team Member Profiles | Quarterly | Tier 1 | RSI topology |
| | Collaboration Logs | Daily | Tier 2 | Interaction topology |
| **Sinthome Detection** | Organizational Narratives | Ongoing | Tier 2 | Founding traumas, cultural stories |
| | Cultural Artifacts | Observation | Tier 3 | Material/ritual sinthomes |
| | Scapegoating Patterns | Daily | Tier 2 | Pathological sinthomes |
| **Validation** | Industry Benchmarks | Annually | Tier 2 | Reality-check |
| | Major Incident History | Historical | Tier 1 | Crisis resilience patterns |
| | Organizational Change Events | Historical | Tier 1 | External stressor context |

---

## 8. EXAMPLE DATA EXTRACTION SCRIPTS

### 8.1 Real Register: Threat Coverage Calculation

```python
import requests
import json

def calculate_threat_coverage(mitre_navigator_layers, deployed_sensors):
    """Calculate actual threat detection coverage vs MITRE ATT&CK."""

    # Load MITRE ATT&CK Enterprise
    attck_url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
    attck_data = requests.get(attck_url).json()

    # Total techniques
    total_techniques = [
        obj for obj in attck_data['objects']
        if obj['type'] == 'attack-pattern' and not obj.get('revoked') and not obj.get('deprecated')
    ]

    # Covered techniques (from Navigator layers or sensor mappings)
    covered_technique_ids = set()
    for layer in mitre_navigator_layers:
        for technique in layer['techniques']:
            if technique.get('enabled') or technique.get('score', 0) > 0:
                covered_technique_ids.add(technique['techniqueID'])

    # Also map deployed sensors to techniques
    sensor_technique_mapping = {
        'EDR': ['T1055', 'T1003', 'T1059', '...'],  # Process Injection, Credential Dumping, Command Execution
        'SIEM': ['T1078', 'T1098', '...'],  # Valid Accounts, Account Manipulation
        'NDR': ['T1071', 'T1041', '...'],  # Application Layer Protocol, Exfiltration
    }

    for sensor_type, techniques in sensor_technique_mapping.items():
        if sensor_type in deployed_sensors:
            covered_technique_ids.update(techniques)

    # Calculate coverage
    coverage_percentage = len(covered_technique_ids) / len(total_techniques) * 100

    return {
        'total_techniques': len(total_techniques),
        'covered_techniques': len(covered_technique_ids),
        'coverage_percentage': coverage_percentage,
        'uncovered_techniques': [t['external_references'][0]['external_id'] for t in total_techniques if t['external_references'][0]['external_id'] not in covered_technique_ids]
    }
```

### 8.2 Symbolic Register: Policy Effectiveness Analysis

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def analyze_policy_effectiveness(policy_docs, incident_descriptions):
    """Measure how well policies cover actual incident types."""

    # Extract policy text
    policy_texts = [policy['content'] for policy in policy_docs]

    # Extract incident descriptions
    incident_texts = [incident['description'] for incident in incident_descriptions]

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(max_features=500)
    policy_vectors = vectorizer.fit_transform(policy_texts)
    incident_vectors = vectorizer.transform(incident_texts)

    # Calculate policy-incident similarity
    similarity_matrix = cosine_similarity(incident_vectors, policy_vectors)

    # For each incident, find best matching policy
    policy_coverage = []
    for i, incident in enumerate(incident_descriptions):
        best_policy_idx = similarity_matrix[i].argmax()
        best_similarity = similarity_matrix[i][best_policy_idx]

        if best_similarity > 0.3:  # Threshold for "covered"
            policy_coverage.append({
                'incident_id': incident['id'],
                'covered_by_policy': policy_docs[best_policy_idx]['id'],
                'similarity': best_similarity
            })

    # Overall policy effectiveness
    effectiveness = len(policy_coverage) / len(incident_descriptions)

    return {
        'policy_effectiveness': effectiveness,
        'incidents_covered': len(policy_coverage),
        'total_incidents': len(incident_descriptions),
        'uncovered_incidents': [inc['id'] for inc in incident_descriptions if inc['id'] not in [pc['incident_id'] for pc in policy_coverage]]
    }
```

### 8.3 Imaginary Register: Self-Image Accuracy

```python
from transformers import pipeline

def analyze_self_image_accuracy(team_communications, benchmark_data):
    """Compare team self-assessments to external benchmarks."""

    # Extract self-assessments from communications
    sentiment_analyzer = pipeline("sentiment-analysis")

    self_assessments = {
        'detection_capability': [],
        'response_speed': [],
        'team_expertise': []
    }

    for msg in team_communications:
        # Look for self-assessment language
        if "we're good at" in msg['text'].lower() or "we excel at" in msg['text'].lower():
            # Simple extraction (in practice, use more sophisticated NLP)
            if "detect" in msg['text'].lower():
                sentiment = sentiment_analyzer(msg['text'])[0]
                self_assessments['detection_capability'].append(1.0 if sentiment['label'] == 'POSITIVE' else 0.3)

    # Average self-assessments
    avg_self_assessment = {
        capability: sum(scores)/len(scores) if scores else 0.5
        for capability, scores in self_assessments.items()
    }

    # Compare to benchmarks
    self_image_gaps = {}
    for capability, self_score in avg_self_assessment.items():
        benchmark_score = benchmark_data.get(capability, 0.5)
        gap = self_score - benchmark_score
        self_image_gaps[capability] = {
            'self_score': self_score,
            'benchmark_score': benchmark_score,
            'gap': gap,
            'assessment': 'overconfident' if gap > 0.2 else 'imposter_syndrome' if gap < -0.2 else 'accurate'
        }

    # Overall self-image accuracy
    avg_gap = sum([abs(g['gap']) for g in self_image_gaps.values()]) / len(self_image_gaps)
    self_image_accuracy = 1 - avg_gap

    return {
        'self_image_accuracy': self_image_accuracy,
        'capability_gaps': self_image_gaps
    }
```

---

## VERSION HISTORY
- v1.0.0 (2025-11-26): Initial comprehensive data source catalog for Enhancement E18

## REFERENCES
- MITRE ATT&CK: https://attack.mitre.org/
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- SANS SOC Survey: https://www.sans.org/security-resources/surveys/
- Gartner Security & Risk Management: https://www.gartner.com/en/information-technology/insights/security

---

*AEON FORGE ENHANCEMENT E18 DATA SOURCES | Comprehensive Data Catalog for RSI Borromean Knot Analysis*
*Updated: 2025-11-26 00:00:00 UTC | Status: OPERATIONAL*
