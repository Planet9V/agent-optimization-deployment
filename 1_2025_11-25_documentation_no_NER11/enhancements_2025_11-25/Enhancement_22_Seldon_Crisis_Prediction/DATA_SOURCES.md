# Enhancement 22: Data Sources for Seldon Crisis Prediction

**File:** Enhancement_22_Seldon_Crisis_Prediction/DATA_SOURCES.md
**Created:** 2025-11-26
**Version:** v1.0.0
**Author:** AEON Development Team
**Purpose:** Comprehensive catalog of data sources for crisis prediction modeling
**Status:** ACTIVE

---

## Executive Summary

The Seldon Crisis Prediction Engine requires diverse data spanning psychometric indicators, technical vulnerabilities, threat intelligence, organizational dynamics, and external events. This document catalogs all required data sources with access methods, update frequencies, and integration patterns.

**Data Categories:**
1. Historical crisis incidents (training data)
2. Psychometric stress indicators (Ψ function)
3. Technical vulnerability data (V function)
4. Threat intelligence (E function)
5. Organizational health metrics
6. External event monitoring (geopolitical, regulatory, economic)

---

## 1. Historical Crisis Incident Databases

### 1.1 VERIS Community Database (VCDB)

**Source:** Verizon Enterprise Solutions
**URL:** https://github.com/vz-risk/VCDB
**Access:** Public (Creative Commons)
**Coverage:** 10,000+ cybersecurity incidents (2010-present)

**Data Fields:**
- Incident date and discovery timeline
- Attack vectors and actions (VERIS 4A framework)
- Asset types and confidentiality impacts
- Industry and organization size
- Root cause analysis (when available)

**Crisis Relevance:**
- Type 3 crises (threat landscape shifts)
- Black Swan events (outliers in incident distribution)
- Organizational collapse indicators (massive breaches leading to bankruptcies)

**Integration:**
```python
import json
import pandas as pd

# Load VCDB data
vcdb = []
for file in glob.glob("VCDB/data/json/**/*.json", recursive=True):
    with open(file) as f:
        vcdb.append(json.load(f))

df = pd.DataFrame(vcdb)
df['crisis_flag'] = df['impact.overall_rating'].apply(lambda x: x == 'Major')
```

**Update Frequency:** Annual releases (community-contributed)

---

### 1.2 Data Breach Investigation Report (DBIR)

**Source:** Verizon Business
**URL:** https://www.verizon.com/business/resources/reports/dbir/
**Access:** Public (annual report)
**Coverage:** Aggregated analysis of 100,000+ incidents/year

**Data Fields:**
- Annual trend analysis (attack patterns evolving)
- Industry-specific breakdowns
- Time-to-compromise and time-to-discovery metrics
- Organizational size impact analysis

**Crisis Relevance:**
- Type 3 crisis early warning (emerging attack patterns)
- Type 4 crisis correlation (regulatory changes post-breach)
- Baseline hazard rates by industry and org size

**Integration:**
```python
# Extract trend data from DBIR annual reports
dbir_trends = {
    2024: {'ransomware_incidents': 0.35, 'supply_chain': 0.08},
    2023: {'ransomware_incidents': 0.32, 'supply_chain': 0.05},
    # ...
}

# Calculate attack pattern acceleration
acceleration = (dbir_trends[2024]['supply_chain'] -
                dbir_trends[2023]['supply_chain']) /
                dbir_trends[2023]['supply_chain']
# 60% increase → Type 3 crisis indicator
```

**Update Frequency:** Annual (typically April/May release)

---

### 1.3 Privacy Rights Clearinghouse Data Breach Database

**Source:** Privacy Rights Clearinghouse (non-profit)
**URL:** https://privacyrights.org/data-breaches
**Access:** Public
**Coverage:** 9,000+ breaches since 2005 (US focus)

**Data Fields:**
- Breach date, organization name, industry
- Records compromised
- Breach type (hacking, insider, physical, etc.)
- State-level geographic data

**Crisis Relevance:**
- Type 2 crisis correlation (breaches often precede organizational collapse)
- Type 4 crisis trigger (breaches drive regulatory changes)
- Geographic clustering (regional crisis patterns)

**Integration:**
```python
# Identify organizational collapse post-breach
prc_data = pd.read_csv("prc_breaches.csv")
prc_data['org_collapsed'] = prc_data['organization'].apply(
    lambda x: check_bankruptcy_databases(x)  # Cross-reference with bankruptcy records
)

# Calculate P(collapse | major breach)
collapse_rate = prc_data[prc_data['records'] > 1e6]['org_collapsed'].mean()
```

**Update Frequency:** Continuous (weekly updates)

---

### 1.4 Internal Incident History

**Source:** Organizational SIEM, incident response platform
**Access:** Internal (security team)
**Coverage:** All detected incidents (including near-misses)

**Data Fields:**
- Full incident timeline (detection → containment → recovery)
- Responder stress indicators (from transcripts - NER11)
- Resource expenditure (person-hours, costs)
- Post-incident organizational changes (process, personnel, tech)

**Crisis Relevance:**
- Calibration data for organization-specific hazard rates
- Type 2 crisis indicators (personnel departures post-incident)
- Learning from near-misses (Black Swan precursors)

**Integration:**
```python
# Extract crisis precursor patterns
internal_incidents = query_siem("incident_type:security", date_range="5y")

# Identify pre-crisis stress accumulation
for incident in internal_incidents:
    transcript = incident['response_transcript']
    stress_scores = ner11_extractor.extract_stress(transcript)
    incident['mean_stress'] = np.mean(stress_scores)

# Cluster incidents into crisis-leading vs. handled
crisis_leading = ml_classifier.predict(internal_incidents)
```

**Update Frequency:** Real-time

---

## 2. Psychometric Stress Indicators (Ψ Data)

### 2.1 NER11 Transcript Extractions

**Source:** Enhancement 21 (Transcript Psychometric NER)
**Access:** Internal (generated from meeting transcripts, emails, chats)
**Coverage:** Continuous psychometric monitoring

**Data Fields:**
- Daily mean personality trait scores (OCEAN)
- Stress indicator frequencies (STRESS_INDICATOR entities)
- Communication pattern shifts (normal → aggressive)
- Group dynamics changes (role instability)

**Crisis Relevance:**
- Primary Ψ(τ) data source
- Early warning: Stress accumulation precedes crises by 30-90 days
- Type 2 crisis (organizational collapse) most sensitive to Ψ

**Integration:**
```python
# Calculate organizational stress time series
stress_timeseries = []
for date in date_range(start="2024-01-01", end="2025-11-26"):
    transcripts_today = get_transcripts(date)
    stress_entities = ner11_extractor.extract(
        transcripts_today,
        entity_type="STRESS_INDICATOR"
    )
    mean_stress = np.mean([e.intensity for e in stress_entities])
    stress_timeseries.append((date, mean_stress))

# Fit stress accumulation model
Ψ_t = cumulative_stress(stress_timeseries)
```

**Update Frequency:** Daily (batch processing overnight)

---

### 2.2 Personnel Turnover Rates

**Source:** HR information system (HRIS)
**Access:** Aggregate data (privacy-protected)
**Coverage:** Monthly turnover statistics

**Data Fields:**
- Voluntary vs. involuntary departures
- Department-level breakdowns (security team focus)
- Tenure distributions (experience loss)
- Exit interview themes (aggregated)

**Crisis Relevance:**
- Type 2 crisis (organizational collapse) primary indicator
- Ψ₃ component (turnover rate in stress function)
- Key person dependency tracking (bus factor)

**Integration:**
```python
# Calculate security team turnover rate
turnover_monthly = hr_system.query(
    department="Security",
    metric="turnover_rate",
    period="monthly"
)

# Identify crisis threshold
if turnover_monthly > THRESHOLD_TURNOVER:
    alert("Type 2 crisis probability elevated")
```

**Update Frequency:** Monthly

---

### 2.3 Employee Assistance Program (EAP) Utilization

**Source:** EAP provider (aggregated, anonymized)
**Access:** Aggregate statistics only
**Coverage:** Mental health resource usage

**Data Fields:**
- Utilization rate (% of employees using EAP)
- Presenting concerns (aggregated categories: stress, burnout, conflict)
- Trend over time

**Crisis Relevance:**
- Leading indicator of organizational stress (Ψ)
- Precedes turnover (people seek help before leaving)
- Privacy-protected but actionable

**Integration:**
```python
# Monitor EAP utilization trend
eap_rate = eap_provider.get_utilization_rate(org_id)

if eap_rate > historical_mean + 2*historical_std:
    alert("Organizational stress elevated (EAP spike)")
```

**Update Frequency:** Quarterly (privacy lag)

---

## 3. Technical Vulnerability Data (V Function)

### 3.1 National Vulnerability Database (NVD)

**Source:** NIST
**URL:** https://nvd.nist.gov/
**Access:** Public API
**Coverage:** 200,000+ CVEs (1999-present)

**Data Fields:**
- CVE ID, publication date, last modified date
- CVSS v3.1 scores (base, temporal, environmental)
- CWE categories (vulnerability types)
- CPE matches (affected products/versions)
- Exploit availability (references)

**Crisis Relevance:**
- V(τ) CVE exposure component
- Type 1 crisis (technology shift) when CVE trends shift
- Type 5 crisis (Black Swan) via zero-day disclosures

**Integration:**
```python
import requests

# Query NVD API for recent CVEs affecting organization
nvd_api = "https://services.nvd.nist.gov/rest/json/cves/2.0"
response = requests.get(nvd_api, params={'resultsPerPage': 100})

org_cves = [
    cve for cve in response.json()['vulnerabilities']
    if matches_org_tech_stack(cve)
]

# Calculate vulnerability exposure
CVE_exposure_t = sum(cve['cvss']['baseScore'] for cve in org_cves)
```

**Update Frequency:** Real-time (new CVEs published continuously)

---

### 3.2 Internal Vulnerability Scans

**Source:** Tenable, Qualys, Rapid7, or equivalent
**Access:** Internal
**Coverage:** All organizational assets

**Data Fields:**
- Asset inventory (servers, workstations, network devices)
- Vulnerability findings (CVEs + misconfigurations)
- Risk scores and exploitability ratings
- Patching status and historical trends

**Crisis Relevance:**
- Primary V(τ) data source (actual organizational exposure)
- Type 1 crisis (unpatched legacy systems reaching end-of-life)
- Type 3 crisis (vulnerable attack surface)

**Integration:**
```python
# Query vulnerability scanner API
vuln_scan = tenable.query(
    scan_date=datetime.today(),
    severity="Critical,High"
)

# Calculate unpatched CVE count
unpatched_cves = [
    v for v in vuln_scan
    if v['patch_available'] and not v['patch_applied']
]

if len(unpatched_cves) > THRESHOLD_UNPATCHED:
    alert("Type 1 crisis: Vulnerability accumulation")
```

**Update Frequency:** Weekly (full scans), daily (critical assets)

---

### 3.3 Configuration Compliance Scores

**Source:** CIS benchmark scans, AWS Config, Azure Policy
**Access:** Internal (cloud provider APIs)
**Coverage:** Infrastructure and cloud configurations

**Data Fields:**
- Compliance percentage (CIS benchmarks)
- Non-compliant configurations (specific findings)
- Drift detection (changes from baseline)
- Historical compliance trends

**Crisis Relevance:**
- V(τ) configuration weakness component
- Type 1 crisis (insecure defaults in new technologies)
- Type 5 crisis (configuration drift enabling breaches)

**Integration:**
```python
# Query cloud config compliance
aws_config = boto3.client('config')
compliance = aws_config.describe_compliance_by_config_rule()

compliance_score = sum(
    1 for rule in compliance['ComplianceByConfigRules']
    if rule['Compliance']['ComplianceType'] == 'COMPLIANT'
) / len(compliance['ComplianceByConfigRules'])

# Monitor for degradation
if compliance_score < THRESHOLD_COMPLIANCE:
    alert("Type 1 crisis: Configuration weakness")
```

**Update Frequency:** Daily (automated scans)

---

### 3.4 Technical Debt Assessments

**Source:** SonarQube, CodeClimate, manual architecture reviews
**Access:** Internal
**Coverage:** Codebase and infrastructure age/quality

**Data Fields:**
- Code quality metrics (maintainability index, cyclomatic complexity)
- Dependency age (libraries, frameworks, OS versions)
- Security-specific debt (use of deprecated crypto, hardcoded secrets)
- System age distributions

**Crisis Relevance:**
- V(τ) technical debt component
- Type 1 crisis (legacy systems unable to support modern security)
- Type 2 crisis (inability to retain talent due to outdated tech)

**Integration:**
```python
# Calculate tech debt score
sonarqube = SonarQubeAPI()
projects = sonarqube.get_all_projects()

tech_debt_hours = sum(
    proj['technical_debt'] for proj in projects
)

if tech_debt_hours > THRESHOLD_TECH_DEBT:
    alert("Type 1 crisis: Accumulated technical debt")
```

**Update Frequency:** Weekly (code commits), quarterly (architecture reviews)

---

## 4. Threat Intelligence (E Function)

### 4.1 OSINT Threat Feeds

**Source:** AlienVault OTX, Abuse.ch, VirusTotal, URLhaus
**URL:** Multiple public feeds
**Access:** Public (rate-limited APIs)

**Data Fields:**
- Indicators of Compromise (IoCs): IPs, domains, hashes
- Threat actor groups (APT naming)
- Campaign tracking (naming conventions)
- Malware families and variants

**Crisis Relevance:**
- E(τ) threat activity component
- Type 3 crisis (new campaigns targeting sector)
- Type 5 crisis (zero-day exploitation in wild)

**Integration:**
```python
# Aggregate threat feeds
threat_feeds = [
    'https://otx.alienvault.com/api/v1/pulses/subscribed',
    'https://urlhaus-api.abuse.ch/v1/urls/recent/',
    # ...
]

threat_activity_score = 0
for feed_url in threat_feeds:
    iocs = fetch_feed(feed_url)
    relevant_iocs = [
        ioc for ioc in iocs
        if matches_org_sector(ioc)
    ]
    threat_activity_score += len(relevant_iocs)

# Normalize to daily average
E_threat_t = threat_activity_score / historical_daily_avg
```

**Update Frequency:** Real-time (continuous ingestion)

---

### 4.2 Dark Web Monitoring

**Source:** Flashpoint, Recorded Future, DarkOwl, Intel471
**Access:** Commercial subscriptions
**Coverage:** Underground forums, marketplaces, messaging platforms

**Data Fields:**
- Mentions of organization name or sector
- Exploit sales and tool development
- Threat actor recruitment and capability development
- Ransomware group negotiations

**Crisis Relevance:**
- Type 3 crisis (pre-attack chatter)
- Type 5 crisis (zero-day trading)
- E(τ) threat activity component (leading indicator)

**Integration:**
```python
# Query dark web intelligence platform
flashpoint_api = FlashpointAPI()
mentions = flashpoint_api.search(
    query=f"org:{ORG_NAME} OR industry:{ORG_INDUSTRY}",
    date_range="last_30_days"
)

# Sentiment analysis (planning vs. bragging)
planning_mentions = [
    m for m in mentions
    if sentiment_classifier(m) == 'intent'
]

if len(planning_mentions) > THRESHOLD_MENTIONS:
    alert("Type 3 crisis: Elevated targeting intent")
```

**Update Frequency:** Daily (batch processing)

---

### 4.3 Attack Surface Monitoring

**Source:** Shodan, Censys, BinaryEdge
**URL:** https://shodan.io, https://censys.io
**Access:** API (paid plans for org-specific monitoring)

**Data Fields:**
- Internet-facing services (IPs, ports, services)
- SSL/TLS certificate tracking
- Subdomain discovery
- Exposed credentials and secrets

**Crisis Relevance:**
- E(τ) attack surface component
- Type 1 crisis (cloud migration expanding surface)
- Type 3 crisis (exposed services being scanned/exploited)

**Integration:**
```python
import shodan

api = shodan.Shodan(API_KEY)
results = api.search(f'org:"{ORG_NAME}"')

# Count internet-facing services
attack_surface_count = results['total']

# Monitor for unexpected increases
if attack_surface_count > historical_mean + 2*historical_std:
    alert("Type 3 crisis: Attack surface expansion")
```

**Update Frequency:** Weekly (full scans)

---

### 4.4 ISAC Threat Intelligence Sharing

**Source:** Financial Services ISAC, Healthcare ISAC, etc.
**Access:** Membership-based
**Coverage:** Sector-specific threat intelligence

**Data Fields:**
- Sector-targeted campaigns (APT groups)
- TTPs specific to industry
- IoCs shared by peer organizations
- Regulatory threat advisories

**Crisis Relevance:**
- Type 3 crisis (sector-wide threat escalation)
- Type 4 crisis (regulatory changes driven by breaches)
- Early warning from peer experiences

**Integration:**
```python
# Ingest ISAC feed via STIX/TAXII
from stix2 import TAXIICollectionSource

collection = TAXIICollectionSource(ISAC_TAXII_SERVER)
threat_reports = collection.query([
    Filter('type', '=', 'threat-actor'),
    Filter('sectors', 'contains', ORG_SECTOR)
])

# Assess relevance to organization
relevant_threats = [
    t for t in threat_reports
    if t.target_sectors contains ORG_SECTOR
]
```

**Update Frequency:** Daily (via automated feeds)

---

## 5. Organizational Health Metrics

### 5.1 Employee Surveys (Engagement, Satisfaction)

**Source:** Annual/quarterly employee engagement surveys
**Access:** HR (aggregated results)
**Coverage:** Organizational morale and culture

**Data Fields:**
- Engagement scores (Gallup Q12 or equivalent)
- Satisfaction ratings (job, management, resources)
- Burnout indicators (exhaustion, cynicism)
- Intent to leave (turnover predictors)

**Crisis Relevance:**
- Ψ(τ) stress function input
- Type 2 crisis (mass departures following low engagement)
- Leading indicator (12-18 month lag to crisis)

**Integration:**
```python
# Extract engagement trends
survey_results = hr_system.get_survey_results(department="Security")

engagement_score = survey_results['mean_engagement']

if engagement_score < THRESHOLD_ENGAGEMENT:
    alert("Type 2 crisis: Low engagement (turnover risk)")
```

**Update Frequency:** Quarterly or annually

---

### 5.2 Project Velocity Metrics

**Source:** Jira, GitHub, project management tools
**Access:** Internal
**Coverage:** Security team productivity

**Data Fields:**
- Sprint velocity (story points completed)
- Cycle time (idea → production)
- Bug backlog growth rate
- On-time project delivery percentage

**Crisis Relevance:**
- Ψ(τ) cognitive load indicator (declining velocity = stress)
- Type 1 crisis (inability to keep up with technology changes)
- Type 2 crisis (team dysfunction reducing productivity)

**Integration:**
```python
# Query project management API
jira = JiraAPI()
sprints = jira.get_sprints(team="Security", period="last_6_months")

velocity_trend = [s['completed_points'] for s in sprints]

# Detect decline
if recent_velocity < historical_velocity * 0.70:
    alert("Type 2 crisis: Productivity decline (stress/burnout)")
```

**Update Frequency:** Weekly (sprint cycles)

---

### 5.3 Bus Factor Analysis

**Source:** Code commits, documentation, on-call rotations
**Access:** Internal (git logs, wiki edits)
**Coverage:** Key person dependencies

**Data Fields:**
- Commit concentration (% of commits by top contributor)
- Documentation coverage (% of systems with docs)
- Cross-training status (people per critical system)
- On-call load distribution

**Crisis Relevance:**
- Type 2 crisis (key person departure crippling capabilities)
- Ψ(τ) stress concentration on few individuals
- Organizational fragility indicator

**Integration:**
```python
# Calculate bus factor for critical systems
git_log = subprocess.check_output(['git', 'log', '--format=%an']).decode()
commit_counts = Counter(git_log.split('\n'))

bus_factor = sum(1 for author, count in commit_counts.items()
                  if count > 0.20 * sum(commit_counts.values()))

if bus_factor < THRESHOLD_BUS_FACTOR:
    alert("Type 2 crisis: Key person dependency risk")
```

**Update Frequency:** Monthly

---

## 6. External Event Monitoring

### 6.1 Geopolitical Risk Tracking (GDELT)

**Source:** Global Database of Events, Language, and Tone
**URL:** https://www.gdeltproject.org/
**Access:** Public (BigQuery datasets)

**Data Fields:**
- Global events (conflicts, treaties, sanctions)
- Sentiment analysis (news tone)
- Actor relationships (country-country, organization-organization)
- Cyber conflict events

**Crisis Relevance:**
- Type 3 crisis (nation-state cyber operations escalation)
- Type 5 crisis (geopolitical black swans)
- E(τ) threat activity context

**Integration:**
```python
from google.cloud import bigquery

client = bigquery.Client()

query = """
SELECT EventCode, Actor1CountryCode, Actor2CountryCode, AvgTone
FROM `gdelt-bq.gdeltv2.events`
WHERE EventCode IN ('190', '191', '192')  # Cyber operations
  AND DATE(SQLDATE) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
"""

cyber_events = client.query(query).to_dataframe()

# Assess escalation risk
if cyber_events['EventCode'].value_counts()['192'] > THRESHOLD:
    alert("Type 3 crisis: Geopolitical cyber escalation")
```

**Update Frequency:** Daily (15-minute event lag)

---

### 6.2 Regulatory Pipeline Monitoring

**Source:** Congress.gov, state legislatures, Federal Register
**URL:** https://www.congress.gov/, https://www.federalregister.gov/
**Access:** Public

**Data Fields:**
- Bills introduced (keyword: cybersecurity, data privacy)
- Committee hearings scheduled
- Agency rulemaking (proposed rules, comment periods)
- State-level legislation tracking

**Crisis Relevance:**
- Type 4 crisis (regulatory shock)
- 2-3 year lead time for federal legislation
- 6-12 month lead time for state legislation

**Integration:**
```python
import requests

# Query Congress.gov API
congress_api = "https://api.congress.gov/v3/bill"
response = requests.get(congress_api, params={'q': 'cybersecurity'})

bills = response.json()['bills']
high_priority_bills = [
    b for b in bills
    if b['committees'][0]['name'] in ['Homeland Security', 'Energy and Commerce']
]

if len(high_priority_bills) > THRESHOLD_BILLS:
    alert("Type 4 crisis: Regulatory momentum building")
```

**Update Frequency:** Weekly

---

### 6.3 Economic Indicators

**Source:** Federal Reserve, Bureau of Labor Statistics
**URL:** https://fred.stlouisfed.org/
**Access:** Public (FRED API)

**Data Fields:**
- GDP growth rate
- Unemployment rate (cybersecurity sector)
- Interest rates (affects IT investment)
- Venture capital investment (cybersecurity startups)

**Crisis Relevance:**
- Type 1 crisis (funding availability for modernization)
- Type 2 crisis (talent market tightness driving turnover)
- Macro context for all crisis types

**Integration:**
```python
from fredapi import Fred

fred = Fred(api_key=FRED_API_KEY)
unemployment_cyber = fred.get_series('UNEMPLOYRATE_CYBER')  # hypothetical

if unemployment_cyber < 2.0:  # Very tight labor market
    alert("Type 2 crisis: Talent retention risk elevated")
```

**Update Frequency:** Monthly

---

### 6.4 Technology Trend Analysis

**Source:** Gartner Hype Cycle, arXiv papers, GitHub trending
**Access:** Mixed (Gartner subscription, arXiv public, GitHub public)

**Data Fields:**
- Emerging technologies (quantum, AI, etc.)
- Research publication trends (keyword frequency)
- Open-source project growth (stars, forks, commits)
- VC investment by technology area

**Crisis Relevance:**
- Type 1 crisis (technology shifts)
- 3-5 year lead time for early-stage technologies
- 1-2 year lead time for mature-stage technologies

**Integration:**
```python
import arxiv

# Query arXiv for quantum computing + cryptography papers
search = arxiv.Search(
    query="quantum AND (cryptography OR encryption)",
    max_results=1000,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

paper_count_recent = sum(
    1 for paper in search.results()
    if paper.published.year >= 2024
)

# Detect acceleration
if paper_count_recent > paper_count_2023 * 1.5:
    alert("Type 1 crisis: Quantum cryptography research accelerating")
```

**Update Frequency:** Monthly (trend aggregation)

---

## Data Integration Architecture

### Unified Crisis Data Lake

```
[Historical Incidents (VERIS, DBIR, PRC, Internal)]
            ↓
[Psychometric Stress (NER11, HR, EAP)]
            ↓
[Vulnerability Data (NVD, Scans, Compliance, Tech Debt)]
            ↓
[Threat Intelligence (OSINT, Dark Web, Attack Surface, ISAC)]
            ↓
[Organizational Health (Surveys, Velocity, Bus Factor)]
            ↓
[External Events (GDELT, Regulatory, Economic, Tech Trends)]
            ↓
        NEO4J CRISIS GRAPH
            ↓
    [Seldon Prediction Engine]
```

### Neo4j Data Model

```cypher
// Data source nodes
CREATE (ds:DataSource {
    name: "VERIS",
    type: "HISTORICAL_INCIDENTS",
    update_frequency: "ANNUAL",
    last_updated: datetime(),
    url: "https://github.com/vz-risk/VCDB"
})

// Time-series data nodes
CREATE (ts:TimeSeriesData {
    source: "NER11_STRESS",
    date: date("2025-11-26"),
    value: 0.68,
    component: "mean_neuroticism"
})

// Link to crisis predictions
CREATE (cp:CrisisPrediction)-[:USES_DATA]->(ts)
CREATE (cp)-[:USES_DATA]->(ds)
```

---

## Data Quality and Governance

### Quality Metrics

**Completeness:**
- % of required data sources available
- % of missing values per time series
- Target: ≥95% data availability

**Timeliness:**
- Lag between event and data ingestion
- Target: ≤24 hours for real-time sources

**Accuracy:**
- Validation against ground truth (where available)
- Target: ≥90% accuracy for critical indicators

### Governance Policies

**Data Retention:**
- Historical incidents: Permanent (research value)
- Psychometric data: 2 years (privacy compliance)
- Vulnerability scans: 1 year (operational need)
- Threat intelligence: 6 months (timeliness decay)

**Access Controls:**
- Public data: No restrictions
- Organizational data: Role-based access
- Individual psychometric data: Anonymized only
- Crisis predictions: Executive leadership only

---

## References

**Incident Databases:**
- VERIS Framework (2010). "Vocabulary for Event Recording and Incident Sharing."
- Verizon (2024). "Data Breach Investigations Report."

**Threat Intelligence:**
- Hutchins et al. (2011). "Intelligence-Driven Computer Network Defense."
- MITRE (2021). "ATT&CK Framework."

**Organizational Health:**
- Gallup (2013). "State of the American Workplace."
- Duhigg (2016). "What Google Learned From Its Quest to Build the Perfect Team."

---

**End of Enhancement 22 Data Sources**
**Next Steps:** Implement data ingestion pipelines and validate with historical crisis backtesting.
