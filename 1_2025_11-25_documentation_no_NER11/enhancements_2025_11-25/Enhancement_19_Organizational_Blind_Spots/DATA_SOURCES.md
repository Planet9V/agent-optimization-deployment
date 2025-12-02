# Enhancement E19: Data Sources for Blind Spot Detection

**File:** DATA_SOURCES.md
**Created:** 2025-11-26
**Version:** 1.0.0
**Purpose:** Comprehensive data source specifications for organizational blind spot detection
**Status:** ACTIVE

---

## Overview

Organizational blind spot detection requires diverse data sources spanning technical security systems, organizational behavior, and external threat intelligence. This document specifies required data sources, access methods, schemas, and quality requirements.

---

## Table of Contents

1. [Incident Post-Mortems](#1-incident-post-mortems)
2. [Alert Fatigue Statistics](#2-alert-fatigue-statistics)
3. [Mean Time to Detect (MTTD) Data](#3-mean-time-to-detect-mttd-data)
4. [Organizational Communication Patterns](#4-organizational-communication-patterns)
5. [Security Tool Coverage Data](#5-security-tool-coverage-data)
6. [Team Expertise Assessments](#6-team-expertise-assessments)
7. [Budget Allocation Data](#7-budget-allocation-data)
8. [Threat Intelligence Feeds](#8-threat-intelligence-feeds)
9. [Penetration Test Results](#9-penetration-test-results)
10. [HR Training Records](#10-hr-training-records)
11. [Data Quality Requirements](#11-data-quality-requirements)
12. [Data Collection Procedures](#12-data-collection-procedures)

---

## 1. Incident Post-Mortems

### Purpose
Identify what was missed during incidents and why, revealing systematic blind spots in detection and response.

### Data Elements

**Required Fields:**
- `incident_id`: Unique identifier (e.g., "INC-2025-001")
- `incident_date`: Timestamp of incident occurrence
- `detection_date`: Timestamp when incident was detected
- `dwell_time_hours`: Time between occurrence and detection
- `severity`: Business impact score (0.0-1.0)
- `attack_vector`: Primary attack method (e.g., "phishing", "insider_threat", "ransomware")
- `security_dimension`: Which capability failed (from state space dimensions)
- `missed_indicators`: List of IOCs present but not detected
- `alert_dismissals`: Alerts that were generated but dismissed
- `root_cause`: Why detection failed
- `contributing_biases`: Cognitive biases identified in retrospective
- `structural_gaps`: Architecture/tool limitations that contributed
- `cultural_factors`: Organizational norms that contributed
- `lessons_learned`: Free-text analysis

**Optional but Valuable:**
- `attacker_sophistication`: Assessment of threat actor capability
- `initial_access_method`: How attacker first compromised environment
- `lateral_movement_path`: How attacker expanded access
- `exfiltration_method`: If applicable, how data was stolen
- `containment_time_hours`: Time to contain after detection
- `remediation_cost_usd`: Total cost of incident response and recovery

### Schema Example

```json
{
  "incident_id": "INC-2025-042",
  "incident_date": "2025-10-15T03:22:00Z",
  "detection_date": "2025-11-12T14:15:00Z",
  "dwell_time_hours": 675,
  "severity": 0.82,
  "attack_vector": "insider_threat_data_exfiltration",
  "security_dimension": "insider_threat",
  "missed_indicators": [
    "Unusual data access patterns (50x normal volume)",
    "After-hours database queries from non-technical user",
    "Large encrypted archive created on workstation",
    "Upload to personal cloud storage (100GB over 3 days)"
  ],
  "alert_dismissals": [
    {
      "alert_id": "DLP-2025-10-16-001",
      "alert_type": "data_loss_prevention",
      "dismissed_by": "analyst_jane_doe",
      "dismissed_reason": "User is trusted executive, assumed business need",
      "dismissed_date": "2025-10-16T09:30:00Z"
    }
  ],
  "root_cause": "Normalcy bias + authority bias: Trusted insider assumed benign",
  "contributing_biases": ["normalcy", "authority", "confirmation"],
  "structural_gaps": [
    "DLP alerts not integrated with UEBA",
    "No baseline for individual user data access patterns",
    "Manual alert review process with high workload"
  ],
  "cultural_factors": [
    "Strong trust culture discourages monitoring senior staff",
    "Fear of false accusations prevents escalation",
    "Security team lacks authority to question executives"
  ],
  "lessons_learned": "Need automated UEBA to flag anomalies regardless of user seniority. Cultural shift required to enable security oversight of all users.",
  "attacker_sophistication": "Low (insider with authorized access)",
  "initial_access_method": "Authorized access (employee)",
  "exfiltration_method": "Personal cloud storage (Dropbox)",
  "containment_time_hours": 2,
  "remediation_cost_usd": 1200000
}
```

### Data Sources

**Primary:**
- Incident response platform (e.g., ServiceNow, Jira, PagerDuty)
- Post-incident review documentation (Confluence, SharePoint)
- Tabletop exercise debriefs

**Secondary:**
- Legal/compliance incident reports
- Insurance claim documentation
- Executive briefing materials

### Access Methods

```python
# Example API call to incident response platform
import requests

response = requests.get(
    "https://incident-platform.company.com/api/v1/incidents",
    headers={"Authorization": f"Bearer {API_TOKEN}"},
    params={
        "start_date": "2023-01-01",
        "end_date": "2025-11-26",
        "include_fields": "all",
        "status": "closed"  # Only include fully analyzed incidents
    }
)

incidents = response.json()['incidents']
```

### Data Quality Checks

- [ ] At least 24 months of historical incidents (minimum statistical power)
- [ ] >80% of incidents have root cause analysis completed
- [ ] Cognitive bias identification in at least 50% of post-mortems
- [ ] Dwell time calculated for >90% of incidents
- [ ] Severity scores normalized (0.0-1.0 scale)

---

## 2. Alert Fatigue Statistics

### Purpose
Quantify alert dismissal patterns that indicate cognitive blind spots, especially confirmation bias and normalcy bias.

### Data Elements

**Required Fields:**
- `alert_id`: Unique identifier
- `alert_date`: Timestamp when alert was generated
- `alert_type`: Category (e.g., "malware", "anomaly", "dlp", "ids")
- `security_dimension`: Which capability generated alert
- `severity`: Alert priority (critical, high, medium, low)
- `dismissed`: Boolean (was alert dismissed without full investigation?)
- `dismissed_by`: Analyst who dismissed
- `dismissed_reason`: Free-text or category
- `dismissal_time_seconds`: How long before dismissal
- `actual_outcome`: Ground truth (true positive, false positive, unknown)
- `time_to_investigate_seconds`: If investigated, how long?

**Derived Metrics:**
- `false_positive_rate`: FP / (TP + FP)
- `true_positive_rate`: TP / (TP + FN)
- `alert_fatigue_score`: FP_rate / TP_rate

### Schema Example

```json
{
  "alert_id": "SIEM-2025-11-15-08234",
  "alert_date": "2025-11-15T22:45:12Z",
  "alert_type": "network_anomaly",
  "security_dimension": "network_traffic_anomalies",
  "severity": "medium",
  "dismissed": true,
  "dismissed_by": "analyst_john_smith",
  "dismissed_reason": "Similar alerts have been false positives this month",
  "dismissal_time_seconds": 45,
  "actual_outcome": "true_positive",  # Later discovered to be C2 beacon
  "time_to_investigate_seconds": null,
  "notes": "Alert dismissed due to alert fatigue. C2 communication continued for 18 days."
}
```

### Data Sources

**Primary:**
- SIEM platform (Splunk, Elastic, QRadar, etc.)
- SOAR platform (Demisto, Phantom, Swimlane)
- Ticketing system (ServiceNow, Jira)

**Secondary:**
- Analyst activity logs
- Alert tuning documentation
- False positive suppression rules

### Access Methods

```python
# Example SIEM query (Splunk SPL)
splunk_query = """
search index=security sourcetype=alert
| stats count by alert_type, severity, dismissed, dismissed_reason, actual_outcome
| eval alert_fatigue_score = false_positive_count / true_positive_count
| where alert_fatigue_score > 2.0
"""

# Example API call
response = requests.post(
    "https://siem.company.com/api/search",
    json={
        "query": splunk_query,
        "start_time": "2024-01-01T00:00:00Z",
        "end_time": "2025-11-26T23:59:59Z"
    },
    headers={"Authorization": f"Bearer {SIEM_TOKEN}"}
)
```

### Data Quality Checks

- [ ] At least 12 months of alert data (capture seasonal patterns)
- [ ] Dismissal reasons categorized (not just free-text)
- [ ] Ground truth (actual outcome) known for >50% of dismissed alerts
- [ ] Alert-to-incident linkage (can trace alerts to confirmed incidents)
- [ ] Analyst identity preserved (to identify bias patterns per analyst)

---

## 3. Mean Time to Detect (MTTD) Data

### Purpose
Compare organizational detection speed to industry baselines, identify dimensions with abnormally high MTTD (potential blind spots).

### Data Elements

**Required Fields:**
- `security_dimension`: Which capability was tested
- `attack_technique_id`: MITRE ATT&CK technique ID (e.g., "T1078")
- `attack_technique_name`: Human-readable name (e.g., "Valid Accounts")
- `incident_id`: If from real incident, link to post-mortem
- `simulated`: Boolean (red team exercise vs real attack)
- `compromise_time`: When attacker action occurred
- `detection_time`: When security team detected
- `mttd_hours`: Time difference
- `detection_method`: How detected (e.g., "SIEM alert", "user report", "forensics")
- `industry_baseline_mttd_hours`: Industry average for this technique

**Derived Metrics:**
- `mttd_ratio`: mttd_actual / mttd_industry_baseline (>1 = slower than industry)
- `detection_capability_score`: min(1.0, mttd_baseline / mttd_actual)

### Schema Example

```json
{
  "security_dimension": "lateral_movement",
  "attack_technique_id": "T1021.001",
  "attack_technique_name": "Remote Desktop Protocol",
  "incident_id": "INC-2025-023",
  "simulated": false,
  "compromise_time": "2025-08-10T14:22:00Z",
  "detection_time": "2025-09-05T09:15:00Z",
  "mttd_hours": 618.88,
  "detection_method": "forensic_investigation_after_ransomware",
  "industry_baseline_mttd_hours": 168,
  "mttd_ratio": 3.68,
  "detection_capability_score": 0.27,
  "notes": "Lateral movement via RDP completely undetected. Only discovered during ransomware forensics."
}
```

### Data Sources

**Primary:**
- Incident response data (dwell time calculations)
- Purple team / red team exercise reports
- Breach and Attack Simulation (BAS) platform results

**Secondary:**
- Industry reports: Mandiant M-Trends, Verizon DBIR, IBM Cost of Data Breach
- MITRE ATT&CK Evaluations
- Peer benchmarking data (if available via ISAC)

### Industry Baseline Data

| Attack Technique | Industry Median MTTD (hours) | Source |
|------------------|------------------------------|--------|
| Initial Access (Phishing) | 48 | Verizon DBIR 2024 |
| Lateral Movement | 168 | Mandiant M-Trends 2024 |
| Data Exfiltration | 336 | IBM Cost of Data Breach 2024 |
| Ransomware Deployment | 24 | Recorded Future 2024 |
| Insider Threat | 287 | Ponemon Insider Threat Cost 2024 |
| Cloud Misconfiguration | 720 | Palo Alto Unit 42 Cloud Threat Report |
| Supply Chain Compromise | 1440 | Various sources, high variance |

### Access Methods

```python
# Compute MTTD from incident data
def calculate_mttd(incidents):
    mttd_by_dimension = {}

    for incident in incidents:
        dimension = incident['security_dimension']
        dwell_time = incident['dwell_time_hours']

        if dimension not in mttd_by_dimension:
            mttd_by_dimension[dimension] = []

        mttd_by_dimension[dimension].append(dwell_time)

    # Compute statistics
    results = {}
    for dimension, dwell_times in mttd_by_dimension.items():
        results[dimension] = {
            'mean_mttd': np.mean(dwell_times),
            'median_mttd': np.median(dwell_times),
            'std_mttd': np.std(dwell_times),
            'p90_mttd': np.percentile(dwell_times, 90),
            'sample_size': len(dwell_times)
        }

    return results
```

### Data Quality Checks

- [ ] At least 10 data points per security dimension (statistical significance)
- [ ] Industry baseline sources cited and current (<2 years old)
- [ ] MTTD calculated from actual compromise time, not detection time
- [ ] Outliers investigated (MTTD > 3σ above mean)
- [ ] Red team exercise data validated by blue team confirmation

---

## 4. Organizational Communication Patterns

### Purpose
Identify blind spots through what is NOT discussed: topics avoided, threats never mentioned, dismissive language patterns.

### Data Elements

**Required Fields:**
- `communication_type`: "email", "slack", "meeting", "report"
- `date`: Timestamp
- `participants`: List of participants (anonymized if required)
- `security_topics_mentioned`: List of security topics discussed
- `security_topics_absent`: Topics notably absent given context
- `sentiment`: Sentiment analysis score per topic (-1 to +1)
- `discussion_depth`: Qualitative (shallow, moderate, deep)
- `dissent_expressed`: Boolean (was alternative view presented?)
- `decision_outcome`: If decision made, what was it?

**Text Analysis Metrics:**
- `topic_frequency`: Count of mentions per topic over time
- `topic_sentiment_trend`: Change in sentiment over time
- `dissent_rate`: Percentage of meetings with expressed dissent
- `groupthink_indicators`: Phrases like "we all agree", "obviously", "everyone knows"

### Schema Example

```json
{
  "communication_id": "MEETING-2025-11-10-SEC-REVIEW",
  "communication_type": "meeting",
  "date": "2025-11-10T14:00:00Z",
  "participants": ["CISO", "SOC_Manager", "IR_Lead", "Network_Architect"],
  "security_topics_mentioned": [
    "ransomware preparedness",
    "phishing training",
    "vulnerability patching"
  ],
  "security_topics_absent": [
    "insider threat",
    "supply chain security",
    "cloud misconfigurations"
  ],
  "sentiment": {
    "ransomware preparedness": 0.65,
    "phishing training": 0.80,
    "vulnerability patching": -0.30
  },
  "discussion_depth": "shallow",
  "dissent_expressed": false,
  "decision_outcome": "Continue current approach, no changes needed",
  "groupthink_indicators": [
    "CISO: 'I think we all agree our defenses are solid'",
    "SOC_Manager: 'Obviously we're doing well compared to peers'",
    "No one challenged consensus despite recent incident"
  ],
  "notes": "Insider threat and supply chain never discussed despite being in threat intel briefing. Possible blind spot."
}
```

### Data Sources

**Primary:**
- Meeting transcripts (Zoom, Teams, Google Meet recordings)
- Email archives (via eDiscovery tools, privacy-compliant)
- Slack/Teams channel logs (security-related channels)
- Security committee minutes

**Secondary:**
- Anonymous employee surveys about security culture
- Exit interview data (departing security staff observations)
- Whistleblower reports

### Access Methods

```python
# Natural Language Processing for topic extraction
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def extract_security_topics(meeting_transcripts):
    """
    Extract security topics discussed in meetings.
    """
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    doc_term_matrix = vectorizer.fit_transform(meeting_transcripts)

    lda = LatentDirichletAllocation(n_components=20, random_state=42)
    lda.fit(doc_term_matrix)

    # Extract topic keywords
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_keywords = [feature_names[i] for i in topic.argsort()[-10:]]
        topics.append(top_keywords)

    return topics

# Sentiment analysis per security topic
from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_security_sentiment(text, security_topics):
    """
    Analyze sentiment for each security topic mentioned.
    """
    sentiments = {}
    for topic in security_topics:
        # Extract sentences mentioning topic
        sentences = [sent for sent in text.split('.') if topic.lower() in sent.lower()]

        if sentences:
            results = sentiment_analyzer(sentences)
            avg_sentiment = np.mean([r['score'] if r['label'] == 'POSITIVE' else -r['score'] for r in results])
            sentiments[topic] = avg_sentiment

    return sentiments
```

### Data Quality Checks

- [ ] At least 12 months of communication data
- [ ] Sampling includes all security decision-making forums
- [ ] Privacy review completed (anonymization if required)
- [ ] Validation: Ground truth topics cross-referenced with incident data
- [ ] Inter-rater reliability for qualitative coding (dissent, depth) >0.8

---

## 5. Security Tool Coverage Data

### Purpose
Map which security dimensions have sensor/alert coverage and which are blind zones.

### Data Elements

**Required Fields:**
- `security_dimension`: Which capability is being covered
- `tool_name`: Security product name
- `tool_category`: "SIEM", "EDR", "IDS", "DLP", "UEBA", etc.
- `deployment_percentage`: What % of assets monitored (0.0-1.0)
- `alert_rules_count`: Number of detection rules for this dimension
- `last_alert_date`: Most recent alert generated (detect rule staleness)
- `true_positive_rate`: TP / (TP + FN) if known from testing
- `false_positive_rate`: FP / (TP + FP)
- `log_retention_days`: How long logs are kept
- `coverage_gaps`: List of assets/scenarios not covered

**Derived Metrics:**
- `effective_coverage`: deployment_percentage × (1 - false_positive_rate) × true_positive_rate

### Schema Example

```json
{
  "security_dimension": "endpoint_malware_detection",
  "tool_name": "CrowdStrike Falcon",
  "tool_category": "EDR",
  "deployment_percentage": 0.92,
  "alert_rules_count": 340,
  "last_alert_date": "2025-11-25T18:43:00Z",
  "true_positive_rate": 0.87,
  "false_positive_rate": 0.08,
  "log_retention_days": 90,
  "coverage_gaps": [
    "Linux servers (8% of endpoints not covered)",
    "IoT devices (no EDR deployment)",
    "Air-gapped systems (by design)"
  ],
  "effective_coverage": 0.78,
  "notes": "Strong coverage for Windows/Mac, weak for Linux and no IoT visibility."
}
```

### Data Sources

**Primary:**
- CMDB (asset inventory with security tool deployment status)
- Security tool admin consoles (CrowdStrike, Palo Alto, etc.)
- SIEM integration logs (which data sources are feeding in)

**Secondary:**
- Vulnerability scanner output (identify unmonitored assets)
- Network diagrams (identify unmonitored network segments)
- Cloud asset inventory (AWS Config, Azure Resource Graph)

### Access Methods

```python
# Query CMDB for tool deployment
def get_tool_coverage(cmdb_api, security_dimension):
    """
    Calculate what % of assets have security tool deployed.
    """
    all_assets = cmdb_api.get_assets(category=security_dimension)
    monitored_assets = [a for a in all_assets if a['security_tool_deployed']]

    coverage = len(monitored_assets) / len(all_assets) if all_assets else 0.0

    gaps = [a for a in all_assets if not a['security_tool_deployed']]

    return {
        'coverage_percentage': coverage,
        'monitored_count': len(monitored_assets),
        'total_count': len(all_assets),
        'coverage_gaps': [a['hostname'] for a in gaps]
    }

# Check SIEM for data source health
def check_siem_data_sources(siem_api):
    """
    Identify which expected log sources are not feeding SIEM.
    """
    expected_sources = ["firewall", "ids", "edr", "dns", "proxy", "ad", "vpn"]
    active_sources = siem_api.get_active_data_sources()

    missing_sources = set(expected_sources) - set(active_sources)

    return {
        'active_sources': active_sources,
        'missing_sources': list(missing_sources),
        'coverage_score': len(active_sources) / len(expected_sources)
    }
```

### Data Quality Checks

- [ ] Asset inventory is current (updated within 7 days)
- [ ] Tool deployment status validated (not just license count, actual deployment)
- [ ] Alert rules tested (not just rule count, but last triggered date)
- [ ] Coverage gaps documented with business justification
- [ ] Cloud assets included (not just on-prem)

---

## 6. Team Expertise Assessments

### Purpose
Quantify team capability in each security dimension to feed into psychometric function Ψ(x).

### Data Elements

**Required Fields:**
- `team_member_id`: Anonymized identifier
- `role`: Job title (e.g., "SOC Analyst L2", "Threat Hunter", "IR Specialist")
- `security_dimension`: Capability area
- `expertise_level`: Self-assessed or manager-assessed (0.0-1.0)
- `certifications`: Relevant certs (CISSP, GCIH, OSCP, etc.)
- `training_completion`: Courses completed in last 12 months
- `hands_on_experience_years`: Years working in this dimension
- `recent_performance`: Performance review scores
- `knowledge_test_score`: If applicable, score on technical assessment

**Derived Metrics:**
- `team_expertise_score(dimension)`: Average expertise across team members for dimension
- `expertise_coverage(dimension)`: What % of team has >0.5 expertise in dimension
- `single_point_of_failure_risk`: Is there only 1 expert in critical dimension?

### Schema Example

```json
{
  "team_member_id": "EMP-SEC-042",
  "role": "SOC Analyst L2",
  "security_dimensions": [
    {
      "dimension": "network_traffic_analysis",
      "expertise_level": 0.75,
      "self_assessed": 0.70,
      "manager_assessed": 0.80,
      "certifications": ["GCIH", "GCIA"],
      "training_completion": ["Wireshark Mastery", "IDS Tuning"],
      "hands_on_experience_years": 4.5,
      "knowledge_test_score": 0.82
    },
    {
      "dimension": "cloud_security",
      "expertise_level": 0.30,
      "self_assessed": 0.35,
      "manager_assessed": 0.25,
      "certifications": [],
      "training_completion": ["AWS Security Basics"],
      "hands_on_experience_years": 0.5,
      "knowledge_test_score": null
    }
  ]
}
```

### Data Sources

**Primary:**
- HR performance management system
- Training/LMS platform (Pluralsight, Udemy Business, etc.)
- Certification tracking database
- Technical assessment platforms (HackerRank, TryHackMe scores)

**Secondary:**
- Self-assessment surveys
- Peer reviews (360-degree feedback)
- Incident response performance metrics (time to triage, false positive rate)

### Access Methods

```python
# Calculate team expertise score per dimension
def calculate_team_expertise(team_data, security_dimension):
    """
    Compute aggregate team expertise for a security dimension.
    """
    experts = [m for m in team_data if security_dimension in m['security_dimensions']]

    if not experts:
        return {
            'team_expertise_score': 0.0,
            'coverage': 0.0,
            'single_point_of_failure': True,
            'risk': 'CRITICAL - No expertise in dimension'
        }

    expertise_levels = [m['security_dimensions'][security_dimension]['expertise_level'] for m in experts]

    return {
        'team_expertise_score': np.mean(expertise_levels),
        'coverage': len([e for e in expertise_levels if e > 0.5]) / len(team_data),
        'single_point_of_failure': len([e for e in expertise_levels if e > 0.7]) == 1,
        'expert_count': len(experts),
        'median_expertise': np.median(expertise_levels)
    }
```

### Data Quality Checks

- [ ] Expertise assessments updated within 6 months
- [ ] Both self and manager assessments available
- [ ] Certification data verified (not just self-reported)
- [ ] Performance metrics tied to actual incident response outcomes
- [ ] Coverage of all security dimensions (identify dimensions with zero expertise)

---

## 7. Budget Allocation Data

### Purpose
Investment level in each security dimension as a component of psychometric function and indicator of organizational prioritization.

### Data Elements

**Required Fields:**
- `fiscal_year`: Which budget period
- `security_dimension`: Capability area
- `budget_allocated_usd`: Total budget for this dimension
- `budget_spent_usd`: Actual spend (vs allocated)
- `budget_category`: "tools", "personnel", "training", "consulting", "other"
- `total_security_budget_usd`: For normalization
- `budget_change_yoy`: Year-over-year % change

**Derived Metrics:**
- `investment_fraction(dimension)`: budget(dimension) / total_security_budget
- `investment_intensity(dimension)`: budget(dimension) / (assets_covered × threat_level)

### Schema Example

```json
{
  "fiscal_year": 2025,
  "security_dimension": "cloud_security",
  "budget_allocated_usd": 450000,
  "budget_spent_usd": 387000,
  "budget_breakdown": {
    "tools": 250000,
    "personnel": 100000,
    "training": 25000,
    "consulting": 75000
  },
  "total_security_budget_usd": 5000000,
  "investment_fraction": 0.09,
  "budget_change_yoy": 0.35,
  "notes": "35% increase YoY reflects growing cloud adoption. However, still <10% of total security budget despite 60% of workloads in cloud."
}
```

### Data Sources

**Primary:**
- Finance/ERP system (SAP, Oracle, Workday)
- Procurement records (purchase orders, contracts)
- CISO budget planning documents

**Secondary:**
- Tool subscription invoices
- Headcount allocation by security function
- Training expenditure reports

### Access Methods

```python
# Analyze budget allocation patterns
def analyze_budget_allocation(budget_data):
    """
    Identify potential blind spots via underinvestment.
    """
    total_budget = sum([d['budget_allocated_usd'] for d in budget_data])

    allocation_analysis = []
    for dimension_budget in budget_data:
        dimension = dimension_budget['security_dimension']
        allocation_pct = dimension_budget['budget_allocated_usd'] / total_budget

        # Get threat level for this dimension from threat intel
        threat_level = get_threat_level(dimension)  # 0.0-1.0

        # Investment intensity: higher is better
        intensity = allocation_pct / threat_level if threat_level > 0 else 0.0

        allocation_analysis.append({
            'dimension': dimension,
            'allocation_pct': allocation_pct,
            'threat_level': threat_level,
            'investment_intensity': intensity,
            'potential_underinvestment': intensity < 0.1  # Threshold
        })

    return sorted(allocation_analysis, key=lambda x: x['investment_intensity'])
```

### Data Quality Checks

- [ ] Budget data complete for last 3 fiscal years (trend analysis)
- [ ] Allocation by dimension, not just total security budget
- [ ] Personnel costs allocated proportionally (not all to "general security")
- [ ] Tool costs mapped to specific dimensions (EDR = endpoint, SIEM = multiple)
- [ ] Budget vs spend variance <20% (indicates accurate planning)

---

## 8. Threat Intelligence Feeds

### Purpose
Understand attacker interest in each security dimension to compute Severity(x) = Threat(x) × [1 - Detection(x)] × Impact(x).

### Data Elements

**Required Fields:**
- `threat_id`: Unique identifier for threat report
- `date_published`: When threat intel published
- `threat_actor`: APT group or threat category
- `attack_vector`: Primary attack method
- `security_dimension`: Which capability targeted
- `frequency`: How often this attack observed (attacks/month)
- `trend`: Increasing, stable, decreasing
- `targeted_industries`: Sectors most targeted
- `targeted_geolocations`: Countries most targeted
- `sophistication`: Low, medium, high, APT-level
- `mitre_attack_techniques`: List of ATT&CK technique IDs

**Derived Metrics:**
- `attacker_interest_score(dimension)`: Frequency × Sophistication × Industry_Relevance

### Schema Example

```json
{
  "threat_id": "TI-2025-11-842",
  "date_published": "2025-11-20T00:00:00Z",
  "source": "Mandiant Threat Intelligence",
  "threat_actor": "APT29 (Cozy Bear)",
  "attack_vector": "supply_chain_compromise",
  "security_dimension": "supply_chain_security",
  "frequency_attacks_per_month": 12,
  "trend": "increasing",
  "targeted_industries": ["technology", "defense", "government"],
  "targeted_geolocations": ["USA", "UK", "Germany"],
  "sophistication": "APT-level",
  "mitre_attack_techniques": ["T1195.001", "T1195.002", "T1199"],
  "observed_tactics": [
    "Compromise software supply chain",
    "Inject malicious code into updates",
    "Establish persistent access via trusted vendor"
  ],
  "attacker_interest_score": 0.89,
  "notes": "Supply chain attacks increasing 40% YoY. High sophistication, targeting technology sector."
}
```

### Data Sources

**Primary:**
- Commercial threat intelligence feeds (Mandiant, CrowdStrike, Recorded Future)
- ISAC/ISAO feeds (relevant to industry)
- MITRE ATT&CK dataset
- CISA advisories

**Secondary:**
- Open-source intelligence (OSINT)
- Dark web monitoring
- Vulnerability databases (NVD, CVE)

### Access Methods

```python
# Aggregate threat intelligence by security dimension
def aggregate_threat_intel(threat_reports):
    """
    Compute attacker interest score for each security dimension.
    """
    threat_by_dimension = {}

    for report in threat_reports:
        dimension = report['security_dimension']

        if dimension not in threat_by_dimension:
            threat_by_dimension[dimension] = {
                'frequency_sum': 0,
                'sophistication_max': 0,
                'report_count': 0
            }

        # Convert sophistication to numeric
        soph_map = {'low': 0.3, 'medium': 0.6, 'high': 0.8, 'APT-level': 1.0}
        sophistication = soph_map.get(report['sophistication'], 0.5)

        threat_by_dimension[dimension]['frequency_sum'] += report['frequency_attacks_per_month']
        threat_by_dimension[dimension]['sophistication_max'] = max(
            threat_by_dimension[dimension]['sophistication_max'],
            sophistication
        )
        threat_by_dimension[dimension]['report_count'] += 1

    # Normalize to [0, 1] scale
    max_freq = max([d['frequency_sum'] for d in threat_by_dimension.values()])

    results = {}
    for dimension, data in threat_by_dimension.items():
        attacker_interest = (
            (data['frequency_sum'] / max_freq) * 0.5 +
            data['sophistication_max'] * 0.5
        )
        results[dimension] = {
            'attacker_interest_score': attacker_interest,
            'frequency_attacks_per_month': data['frequency_sum'],
            'sophistication': data['sophistication_max'],
            'report_count': data['report_count']
        }

    return results
```

### Data Quality Checks

- [ ] Threat intel feeds updated at least weekly
- [ ] Multiple sources aggregated (no single vendor dependency)
- [ ] Industry-specific threat intel included
- [ ] Historical trends available (12+ months)
- [ ] MITRE ATT&CK technique mapping validated

---

## 9. Penetration Test Results

### Purpose
Ground truth for detection capability: Did we actually detect red team in each dimension?

### Data Elements

**Required Fields:**
- `test_id`: Unique identifier
- `test_date`: When test was conducted
- `test_type`: "red_team", "purple_team", "breach_simulation", "vulnerability_assessment"
- `security_dimension`: Which capability was tested
- `mitre_attack_technique`: Technique ID tested
- `attack_succeeded`: Boolean (did attacker achieve objective?)
- `blue_team_detected`: Boolean (did defense detect?)
- `time_to_detect_hours`: If detected, how long?
- `detection_method`: How was it detected?
- `recommendations`: Findings and remediation advice

**Derived Metrics:**
- `detection_rate(dimension)`: (# detected) / (# attempted)
- `mttd_by_dimension`: Mean time to detect per dimension

### Schema Example

```json
{
  "test_id": "PENTEST-2025-Q3-001",
  "test_date": "2025-09-15",
  "test_type": "red_team",
  "security_dimension": "lateral_movement",
  "mitre_attack_technique": "T1021.001",
  "attack_technique_name": "Remote Desktop Protocol",
  "attack_succeeded": true,
  "blue_team_detected": false,
  "time_to_detect_hours": null,
  "detection_method": null,
  "red_team_notes": "Lateral movement via RDP from compromised workstation to Domain Controller. No alerts generated. Persistence established for 72 hours before deconfliction.",
  "blue_team_notes": "No detection. RDP traffic not monitored for anomalies. Recommendation: Implement UEBA for lateral movement detection.",
  "recommendations": [
    "Deploy UEBA to detect anomalous RDP sessions",
    "Enable RDP connection logging on all servers",
    "Alert on admin RDP from workstations",
    "Implement JEA/JIT for privileged access"
  ],
  "severity": "high",
  "detection_capability_score": 0.0
}
```

### Data Sources

**Primary:**
- Red team exercise reports
- Purple team collaboration notes
- Breach and Attack Simulation (BAS) platform results (SafeBreach, AttackIQ, Cymulate)

**Secondary:**
- Bug bounty submissions (for web applications)
- Adversary emulation frameworks (Caldera, Atomic Red Team)

### Access Methods

```python
# Calculate detection capability from pentest results
def calculate_detection_capability(pentest_results):
    """
    Compute detection capability per security dimension.
    """
    detection_by_dimension = {}

    for test in pentest_results:
        dimension = test['security_dimension']

        if dimension not in detection_by_dimension:
            detection_by_dimension[dimension] = {
                'total_attempts': 0,
                'detected_count': 0,
                'mttd_sum': 0,
                'mttd_count': 0
            }

        detection_by_dimension[dimension]['total_attempts'] += 1

        if test['blue_team_detected']:
            detection_by_dimension[dimension]['detected_count'] += 1

            if test['time_to_detect_hours']:
                detection_by_dimension[dimension]['mttd_sum'] += test['time_to_detect_hours']
                detection_by_dimension[dimension]['mttd_count'] += 1

    # Compute metrics
    results = {}
    for dimension, data in detection_by_dimension.items():
        detection_rate = data['detected_count'] / data['total_attempts'] if data['total_attempts'] > 0 else 0.0

        mean_mttd = data['mttd_sum'] / data['mttd_count'] if data['mttd_count'] > 0 else float('inf')

        results[dimension] = {
            'detection_rate': detection_rate,
            'mean_mttd_hours': mean_mttd,
            'detection_capability_score': detection_rate * (1.0 / (1 + mean_mttd / 24.0)),  # Normalize MTTD by 24hrs
            'sample_size': data['total_attempts']
        }

    return results
```

### Data Quality Checks

- [ ] Penetration tests conducted at least annually
- [ ] All security dimensions tested (not just perimeter)
- [ ] Both detected and undetected attacks documented
- [ ] MTTD measured accurately (compromise time vs detection time)
- [ ] Purple team deconfliction ensures blue team detection is real (not knowledge of test)

---

## 10. HR Training Records

### Purpose
Training completion rates as a component of team expertise and cultural readiness.

### Data Elements

**Required Fields:**
- `employee_id`: Anonymized identifier
- `training_course`: Course name
- `security_dimension`: Which capability does training address
- `completion_date`: When completed
- `assessment_score`: If applicable, test score
- `training_hours`: Duration
- `training_type`: "required", "optional", "certification_prep"

**Derived Metrics:**
- `training_completion_rate(dimension)`: % of team completed relevant training
- `training_currency(dimension)`: % of team trained in last 12 months

### Schema Example

```json
{
  "employee_id": "EMP-SEC-042",
  "training_course": "Insider Threat Detection",
  "security_dimension": "insider_threat",
  "completion_date": "2025-08-15",
  "assessment_score": 0.88,
  "training_hours": 8,
  "training_type": "required",
  "training_provider": "SANS",
  "months_since_completion": 3.5,
  "needs_refresher": false
}
```

### Data Sources

**Primary:**
- Learning Management System (LMS): Cornerstone, SAP SuccessFactors, Moodle
- Certification tracking database

### Access Methods

```python
# Calculate training coverage per dimension
def calculate_training_coverage(training_data, team_size):
    """
    Compute training completion rates per security dimension.
    """
    coverage_by_dimension = {}

    for record in training_data:
        dimension = record['security_dimension']

        if dimension not in coverage_by_dimension:
            coverage_by_dimension[dimension] = {
                'trained_employees': set(),
                'recently_trained': set()  # Last 12 months
            }

        coverage_by_dimension[dimension]['trained_employees'].add(record['employee_id'])

        if record['months_since_completion'] <= 12:
            coverage_by_dimension[dimension]['recently_trained'].add(record['employee_id'])

    results = {}
    for dimension, data in coverage_by_dimension.items():
        results[dimension] = {
            'training_completion_rate': len(data['trained_employees']) / team_size,
            'training_currency': len(data['recently_trained']) / team_size,
            'trained_count': len(data['trained_employees']),
            'recently_trained_count': len(data['recently_trained'])
        }

    return results
```

### Data Quality Checks

- [ ] Training records complete for all security team members
- [ ] Assessment scores recorded (not just completion checkboxes)
- [ ] Training mapped to security dimensions (not just generic "security awareness")
- [ ] Refresher training tracked (currency requirements)
- [ ] External certifications included (not just internal training)

---

## 11. Data Quality Requirements

### Overall Quality Standards

**Completeness:**
- [ ] >90% of required fields populated
- [ ] Missing data explicitly flagged (null vs unknown vs not applicable)
- [ ] Historical depth sufficient for trend analysis (typically 12-24 months)

**Accuracy:**
- [ ] Data validation rules applied (e.g., dwell_time > 0, severity ∈ [0,1])
- [ ] Cross-reference checks (incident IDs link to alerts, etc.)
- [ ] Outlier investigation (values >3σ from mean reviewed)

**Timeliness:**
- [ ] Real-time data updated within 24 hours
- [ ] Historical data refreshed at least monthly
- [ ] Data staleness explicitly indicated

**Consistency:**
- [ ] Normalized scales (0.0-1.0 for scores, hours for time)
- [ ] Standardized taxonomies (MITRE ATT&CK for techniques, etc.)
- [ ] Consistent security dimension definitions across data sources

### Data Quality Metrics

```python
def assess_data_quality(dataset, schema):
    """
    Compute data quality scores.
    """
    completeness = sum([1 for field in schema['required'] if field in dataset]) / len(schema['required'])

    # Check for outliers
    numeric_fields = [f for f in schema['numeric'] if f in dataset]
    outliers = []
    for field in numeric_fields:
        values = [d[field] for d in dataset if field in d]
        mean = np.mean(values)
        std = np.std(values)
        outliers.extend([v for v in values if abs(v - mean) > 3 * std])

    outlier_rate = len(outliers) / sum([len(dataset) for _ in numeric_fields]) if numeric_fields else 0.0

    # Check staleness
    if 'timestamp' in schema:
        latest_timestamp = max([d['timestamp'] for d in dataset if 'timestamp' in d])
        staleness_days = (datetime.now() - latest_timestamp).days
    else:
        staleness_days = None

    return {
        'completeness_score': completeness,
        'outlier_rate': outlier_rate,
        'staleness_days': staleness_days,
        'quality_score': completeness * (1 - outlier_rate) * (1 if staleness_days and staleness_days < 30 else 0.5)
    }
```

---

## 12. Data Collection Procedures

### Initial Data Collection Sprint (Week 1-2)

**Phase 1: Data Source Inventory**
- [ ] Identify all data systems (SIEM, ticketing, CMDB, HR, finance)
- [ ] Document API access methods or database connections
- [ ] Obtain necessary access credentials and permissions
- [ ] Validate data availability (can we actually query what we need?)

**Phase 2: Data Extraction**
- [ ] Write ETL scripts for each data source
- [ ] Extract last 24 months of data (or maximum available)
- [ ] Store raw data in staging area (data lake or warehouse)
- [ ] Document any limitations or gaps in extracted data

**Phase 3: Data Transformation**
- [ ] Normalize to common schemas (see schemas in sections above)
- [ ] Apply data quality checks and flag issues
- [ ] Enrich with external data (threat intel, industry baselines)
- [ ] Create master dataset for blind spot analysis

### Ongoing Data Refresh (Monthly)

**Automated Data Pipeline:**
```python
# Example Airflow DAG for monthly data refresh
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'security_analytics',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['security-team@company.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'blind_spot_data_refresh',
    default_args=default_args,
    description='Monthly refresh of blind spot detection data',
    schedule_interval='0 0 1 * *',  # First day of each month
    start_date=datetime(2025, 1, 1),
    catchup=False
)

def extract_incident_data():
    # Extract incident post-mortems from last month
    pass

def extract_alert_data():
    # Extract alert fatigue statistics
    pass

def extract_mttd_data():
    # Extract MTTD data from incidents and pentests
    pass

# Define tasks
extract_incidents = PythonOperator(task_id='extract_incidents', python_callable=extract_incident_data, dag=dag)
extract_alerts = PythonOperator(task_id='extract_alerts', python_callable=extract_alert_data, dag=dag)
extract_mttd = PythonOperator(task_id='extract_mttd', python_callable=extract_mttd_data, dag=dag)

# Task dependencies
[extract_incidents, extract_alerts, extract_mttd]  # Parallel extraction
```

### Privacy and Compliance Considerations

**Data Minimization:**
- Anonymize employee IDs where possible
- Aggregate communication data (don't store full transcripts without consent)
- Retain only necessary fields (avoid over-collection)

**Access Controls:**
- Restrict blind spot analysis data to security leadership + analysts
- Audit all data access for compliance
- Encrypt data at rest and in transit

**Legal Review:**
- Employee monitoring disclosures (if analyzing communications)
- Data retention policies alignment
- GDPR/CCPA compliance for personal data

---

## Appendix: Data Source Maturity Model

| Maturity Level | Characteristics | Data Quality | Blind Spot Detection Capability |
|----------------|----------------|--------------|--------------------------------|
| **Level 1: Ad-Hoc** | Manual data collection, spreadsheets, incomplete coverage | <50% | Cannot reliably detect blind spots |
| **Level 2: Defined** | Some automation, basic data quality checks, gaps documented | 50-70% | Can detect obvious structural blind spots |
| **Level 3: Managed** | Automated ETL, regular refreshes, quality monitoring | 70-85% | Can detect structural + technical blind spots |
| **Level 4: Optimized** | Real-time pipelines, comprehensive coverage, predictive analytics | 85-95% | Can detect structural + technical + cognitive blind spots |
| **Level 5: Continuous** | AI-driven data enrichment, self-healing pipelines, prescriptive remediation | >95% | Full blind spot detection + proactive remediation |

**Current State Assessment:**
- Evaluate organization's current maturity level
- Identify gaps preventing next level
- Create roadmap to achieve Level 4+ (required for comprehensive blind spot detection)

---

**End of DATA_SOURCES.md**

*For theoretical foundation, see README.md*
*For implementation details, see TASKMASTER_BLIND_SPOT_DETECTION_v1.0.md*
