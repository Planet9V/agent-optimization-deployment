# Enhancement E24: Data Sources for Cognitive Dissonance Breaking

**File:** DATA_SOURCES.md
**Created:** 2025-11-26 12:00:00 UTC
**Version:** v1.0.0
**Author:** Research Analysis Agent
**Purpose:** Data sources for detecting and resolving cybersecurity cognitive dissonance
**Status:** ACTIVE

## Executive Summary

Cognitive dissonance detection requires comparing stated beliefs (Symbolic order) against observed behaviors (Real order) and organizational self-perception (Imaginary order). This document catalogs data sources for extracting beliefs, behaviors, and outcomes, enabling systematic dissonance quantification and intervention tracking.

---

## 1. Stated Beliefs (Symbolic Order)

### Security Policy Documents

```yaml
Source_Type: Internal_Documents

Document_Types:
  - Information Security Policy (ISP)
  - Acceptable Use Policy (AUP)
  - Incident Response Plan (IRP)
  - Business Continuity Plan (BCP)
  - Risk Management Framework
  - Security Awareness Training Materials
  - Executive Security Presentations
  - Board-level Security Reports

Extraction_Methods:
  NLP_Parsing:
    - Named Entity Recognition (security commitments)
    - Policy statement extraction (SLAs, mandates)
    - Sentiment analysis (priority language)
    - Compliance framework mapping (NIST, ISO references)

  Manual_Review:
    - Executive summary analysis
    - Policy version history (drift over time)
    - Exception lists (where policy doesn't apply)

  Tools:
    - Apache Tika (PDF/DOCX text extraction)
    - spaCy (NLP processing)
    - PyPDF2 (structured PDF parsing)

Example_Commitments:
  Patch_Management: "Critical patches applied within 72 hours"
  Access_Control: "Least privilege principle enforced"
  MFA: "Multi-factor authentication required for all users"
  Training: "Annual security awareness training mandatory"
  Budget: "Security is a top organizational priority"
```

### Employee Surveys and Self-Reports

```yaml
Source_Type: Survey_Data

Survey_Types:
  Security_Awareness_Surveys:
    frequency: "Quarterly or post-training"
    questions:
      - "How important is cybersecurity to you? (1-10)"
      - "Do you feel confident recognizing phishing emails?"
      - "Would you report a suspicious email?"
    sample_size: "All employees"

  Culture_Assessments:
    frequency: "Annual"
    questions:
      - "Does leadership prioritize security?"
      - "Do you have time to follow security procedures?"
      - "Is security seen as blocker or enabler?"

  Phishing_Simulation_Self_Assessment:
    frequency: "Post-simulation"
    questions:
      - "Why did you click the phishing link?"
      - "What would you do differently next time?"

Collection_Methods:
  - SurveyMonkey, Google Forms
  - LMS (Learning Management System) post-training quizzes
  - Anonymous feedback tools (Officevibe, Culture Amp)

Analysis:
  - Self-reported confidence vs actual behavior correlation
  - Gap between stated importance and observed actions
  - Identify overconfident individuals (Dunning-Kruger indicators)
```

### Executive Statements and Communications

```yaml
Source_Type: Communications_Analysis

Communication_Channels:
  - CEO all-hands presentations
  - Annual reports (security sections)
  - Investor earnings calls (security mentions)
  - Internal security newsletters
  - Executive blog posts

Extraction_Methods:
  Rhetoric_Analysis:
    - Priority language ("critical", "top priority", "essential")
    - Frequency of security mentions
    - Positioning of security (first topic vs afterthought)
    - Concrete commitments vs vague platitudes

  Sentiment_Analysis:
    - Positive/negative tone around security
    - Defensive language (indicates prior incidents)
    - Aspirational vs realistic framing

  Tools:
    - VADER Sentiment Analysis
    - Transcript scraping (earnings call transcripts)
    - Email parsing (executive communication archives)

Example_Indicators:
  High_Priority_Signals:
    - "Security is our #1 priority this year"
    - "We're investing heavily in cybersecurity"
    - "Every employee is a security defender"

  Low_Priority_Signals:
    - No mention of security in annual report
    - Security mentioned only in context of compliance
    - Reactive language ("after the incident, we...")
```

---

## 2. Observed Behaviors (Real Order)

### Patch Management Logs

```yaml
Source_Type: System_Logs

Data_Sources:
  WSUS (Windows):
    location: "Windows Server Update Services database"
    data_points:
      - "Patch release date"
      - "Patch installation date"
      - "Systems patched vs total systems"
      - "Failed patch attempts"

  SCCM (System Center Configuration Manager):
    location: "SCCM reporting database"
    data_points:
      - "Compliance reports per system"
      - "Patch deployment timelines"
      - "Reboot delays"

  Linux_Patch_Management:
    tools: ["Landscape (Ubuntu)", "Satellite (Red Hat)", "Zypper (SUSE)"]
    data_points:
      - "Patch lag times"
      - "Unpatched CVEs by severity"

  Vulnerability_Scanners:
    tools: ["Nessus", "Qualys", "Rapid7"]
    data_points:
      - "Unpatched vulnerabilities by CVSS score"
      - "Time since CVE disclosure"
      - "Exploitability scores"

Metrics_Calculated:
  - Average patch lag (days between release and installation)
  - Patch compliance rate (% systems patched within SLA)
  - Never-patched systems percentage
  - Critical vulnerability exposure time

Integration:
  - API access to patch management systems
  - Scheduled reports (daily, weekly)
  - Alert integration (Slack, email for threshold breaches)
```

### Access Control Audits

```yaml
Source_Type: IAM_Logs

Data_Sources:
  Active_Directory (Windows):
    location: "AD audit logs"
    data_points:
      - "User accounts and group memberships"
      - "Admin rights assignments"
      - "Privileged access escalations"
      - "Stale accounts (no login > 90 days)"

  Azure_AD / Entra_ID:
    location: "Azure portal audit logs"
    data_points:
      - "MFA enrollment and usage"
      - "Conditional access policy effectiveness"
      - "Legacy authentication usage"

  LDAP (Linux/Unix):
    location: "LDAP directory"
    data_points:
      - "sudo privileges"
      - "Group-based access"

  Privileged_Access_Management:
    tools: ["CyberArk", "BeyondTrust", "Thycotic"]
    data_points:
      - "Privileged session recordings"
      - "Just-in-time access usage"
      - "Emergency access breakglass events"

Metrics_Calculated:
  - Admin rights percentage (users with admin vs total users)
  - MFA adoption rate
  - Stale account percentage
  - Least privilege compliance (over-provisioned accounts)
  - Password age and complexity compliance

Integration:
  - PowerShell scripts for AD querying
  - Azure CLI for cloud IAM
  - PAM system APIs
```

### User Behavior Analytics

```yaml
Source_Type: UBA_Logs

Data_Sources:
  SIEM_UBA_Modules:
    tools: ["Splunk UBA", "Exabeam", "Microsoft Sentinel"]
    data_points:
      - "Anomalous login patterns"
      - "Data exfiltration attempts"
      - "Unusual file access"
      - "Off-hours activity"

  Email_Security_Gateways:
    tools: ["Proofpoint", "Mimecast", "Barracuda"]
    data_points:
      - "Phishing simulation click rates"
      - "Real phishing click rates"
      - "Suspicious email reporting rates"
      - "Malicious attachment open rates"

  DLP (Data Loss Prevention):
    tools: ["Symantec DLP", "Forcepoint", "Digital Guardian"]
    data_points:
      - "Policy violations (intentional vs accidental)"
      - "Sensitive data transfers"
      - "USB usage violations"

  Endpoint_Detection:
    tools: ["CrowdStrike", "SentinelOne", "Microsoft Defender"]
    data_points:
      - "Malware detection and remediation"
      - "Policy compliance (encryption, firewall)"
      - "Unauthorized software installations"

Metrics_Calculated:
  - Risky user behavior frequency
  - Phishing click rate (simulated and real)
  - Policy violation rate
  - Time-to-report suspicious activity
  - Repeat offender identification

Integration:
  - SIEM API for behavior data
  - Email gateway reporting APIs
  - DLP alert webhooks
```

### Budget Allocation Data

```yaml
Source_Type: Financial_Systems

Data_Sources:
  ERP_Systems:
    tools: ["SAP", "Oracle Financials", "NetSuite"]
    data_points:
      - "Security budget by fiscal year"
      - "IT budget total"
      - "Revenue (for % calculations)"
      - "Budget growth year-over-year"

  Security_Tool_Spend:
    sources:
      - "Vendor invoices (subscriptions, licenses)"
      - "Procurement records"
      - "Cloud service bills (security services)"
    categories:
      - "Prevention tools (firewalls, AV)"
      - "Detection tools (SIEM, EDR)"
      - "Response tools (SOAR, forensics)"
      - "Training and awareness"
      - "Security personnel salaries"

  Benchmark_Data:
    sources:
      - "Gartner IT spending surveys"
      - "Forrester security budget benchmarks"
      - "SANS security spending surveys"
    use: "Compare actual spend to industry averages"

Metrics_Calculated:
  - Security budget as % of IT budget
  - Security budget as % of revenue
  - Per-employee security spend
  - Budget allocation by category (prevention/detection/response)
  - YoY budget growth rate

Integration:
  - ERP API access (finance team coordination)
  - Procurement system reports
  - Manual aggregation from invoices if necessary
```

### Incident Response Metrics

```yaml
Source_Type: Incident_Logs

Data_Sources:
  Ticketing_Systems:
    tools: ["ServiceNow", "Jira", "PagerDuty"]
    data_points:
      - "Incident open and close timestamps"
      - "Incident severity classifications"
      - "Mean time to detect (MTTD)"
      - "Mean time to respond (MTTR)"
      - "Escalation patterns"

  SIEM_Incident_Records:
    data_points:
      - "Alert generation time"
      - "Alert-to-incident promotion rate"
      - "False positive rates"

  Post-Incident_Reports:
    data_points:
      - "Root cause analysis findings"
      - "Lessons learned"
      - "Corrective actions (promised vs completed)"

Metrics_Calculated:
  - Average MTTD and MTTR
  - Incident frequency by type
  - Repeat incident rate (same root cause)
  - Promised corrective action completion rate

Integration:
  - Ticketing system APIs
  - SIEM reporting dashboards
  - Manual review of post-incident reports
```

---

## 3. Outcomes (Reality Check)

### Breach and Incident History

```yaml
Source_Type: Security_Incident_Data

Internal_Sources:
  - Incident response documentation
  - Forensics reports
  - Insurance claims (cyber insurance)

External_Sources:
  - HaveIBeenPwned (check organizational email domains)
  - Public breach disclosures (SEC filings, news)
  - Third-party risk assessments

Metrics:
  - Total breaches in past 5 years
  - Data records compromised
  - Downtime from incidents
  - Financial impact (direct costs + fines + reputation)

Analysis:
  - Correlation with dissonance dimensions
  - Preventable vs unpreventable incidents
  - Repeat root causes (dissonance manifestation)
```

### Audit Findings and Compliance Gaps

```yaml
Source_Type: Audit_Reports

Audit_Types:
  Internal_Audits:
    - IT general controls (ITGC)
    - Security policy compliance
    - Access control reviews

  External_Audits:
    - SOC 2 Type II reports
    - ISO 27001 certification audits
    - PCI-DSS assessments
    - HIPAA compliance audits

  Regulatory_Examinations:
    - FFIEC (financial institutions)
    - NERC CIP (energy sector)
    - GDPR assessments

Data_Extracted:
  - Number of findings by severity (critical, high, medium, low)
  - Repeat findings (year-over-year)
  - Remediation timelines (planned vs actual)
  - Management responses (acceptance, mitigation, transfer)

Dissonance_Indicators:
  - Persistent findings despite stated policy compliance
  - Management accepts risks contrary to stated priorities
  - Slow remediation (behavior inconsistent with urgency claims)
```

### Penetration Test Results

```yaml
Source_Type: Pentest_Reports

Test_Types:
  External_Pentests:
    - Internet-facing attack surface
    - Web application vulnerabilities
    - Network perimeter weaknesses

  Internal_Pentests:
    - Lateral movement ease
    - Privilege escalation paths
    - Access control effectiveness

  Social_Engineering_Tests:
    - Phishing success rates
    - Physical security bypasses
    - Phone-based pretexting

Data_Extracted:
  - Vulnerabilities found by severity
  - Time-to-compromise metrics
  - Common misconfigurations
  - Effectiveness of security controls

Dissonance_Indicators:
  - Easy compromises despite "strong security" claims
  - Controls not functioning as documented
  - Repeat vulnerabilities from prior tests
```

---

## 4. Cross-Referencing and Correlation

### Belief-Behavior-Outcome Mapping

```yaml
Correlation_Analysis:

  Patch_Management:
    stated_belief: "Policy: Patch within 72 hours"
    observed_behavior: "Avg lag: 45 days, 30% never patched"
    outcome: "3 breaches via unpatched CVEs in past 2 years"
    dissonance_score: 0.81 (critical)

  Access_Control:
    stated_belief: "Least privilege enforced"
    observed_behavior: "63% users have admin rights"
    outcome: "Lateral movement in pentest took < 30 minutes"
    dissonance_score: 0.72 (critical)

  Budget_Allocation:
    stated_belief: "Security is top priority"
    observed_behavior: "2% of IT budget, flat YoY"
    outcome: "Audit finding: inadequate security resources"
    dissonance_score: 0.68 (high)
```

---

## 5. Interview and Qualitative Data

### Stakeholder Interviews

```yaml
Interview_Subjects:
  - CISO and security leadership
  - IT operations managers
  - Developers and engineers
  - End users (sample)
  - Executive leadership (CEO, CFO, CTO)
  - Board members (if possible)

Interview_Topics:
  - Perceived security priorities
  - Barriers to security compliance
  - Resource constraints (real vs imagined)
  - Cultural attitudes toward security
  - Incident response experiences

Data_Collection:
  - Structured interview scripts
  - Semi-structured exploration
  - Anonymous feedback mechanisms (for honest responses)

Analysis:
  - Thematic coding (identify common barriers)
  - Sentiment analysis (frustration, apathy, engagement)
  - Cross-reference with quantitative dissonance data
```

---

## 6. Behavioral Economics and Psychology Data

### Cognitive Bias Indicators

```yaml
Data_Sources:
  Survey_Questions:
    Optimism_Bias:
      - "How likely is your organization to experience a breach in the next year?"
      - "How does that compare to industry average?"
      - (Unrealistically low = optimism bias)

    Present_Bias:
      - "Would you rather patch now (5 min downtime) or delay 1 week (no downtime)?"
      - (Majority choose delay = present bias)

    Loss_Aversion:
      - "Would you invest $100K to prevent $500K expected loss?"
      - (No = loss aversion, status quo bias)

  Behavioral_Observation:
    Hyperbolic_Discounting:
      - Compare immediate security actions vs delayed security investments
      - Pattern: Choose immediate convenience over future security

    Dunning-Kruger_Effect:
      - Self-assessed security competence vs actual test performance
      - Overconfidence = high self-assessment, low actual performance

Analysis_Methods:
  - Psychological surveys (adapted from behavioral econ literature)
  - A/B testing (framing effects on security decisions)
  - Implicit Association Tests (IAT) for security attitudes
```

---

## 7. Peer and Industry Benchmark Data

### Comparative Analysis

```yaml
Benchmark_Sources:
  Gartner_Peer_Insights:
    - Security spending by industry and company size
    - Security staffing ratios
    - Tool adoption rates

  SANS_Security_Surveys:
    - Incident response maturity
    - Training frequency and effectiveness
    - Patch management practices

  Verizon_DBIR (Data Breach Investigations Report):
    - Incident root causes by industry
    - Time-to-compromise statistics
    - Common attack vectors

  Ponemon_Institute_Studies:
    - Cost of data breach reports
    - Cybersecurity effectiveness studies
    - Security culture assessments

Use_Cases:
  Social_Proof_Interventions:
    - "Your patch compliance (42%) is below industry average (67%)"
    - "Competitors spend 3x more on security per employee"

  Reality_Checks:
    - "You claim 'best-in-class security' but rank bottom quartile on benchmarks"
```

---

## 8. Intervention Tracking Data

### Progress Measurement

```yaml
Before_After_Metrics:
  Dissonance_Scores:
    - Measure D_before (pre-intervention)
    - Measure D_after (post-intervention at 30, 90, 180 days)
    - Calculate ΔD = D_before - D_after

  Behavioral_Changes:
    - Patch compliance rate improvement
    - MFA adoption rate increase
    - Phishing click rate reduction
    - Budget allocation shifts

  Cultural_Indicators:
    - Security champion emergence (voluntary adoption)
    - Language shifts in meetings (security-positive rhetoric)
    - Policy updates (aligning Symbolic with Real)

Tracking_Tools:
  - Neo4j time-series data (temporal dissonance evolution)
  - Dashboards (Grafana, Tableau) showing progress
  - Automated alerts for stagnation or regression
```

---

## Data Integration Architecture

### ETL Pipeline

```yaml
Extract:
  - Policy document parsing (NLP)
  - System log ingestion (APIs, SIEM)
  - Survey data collection (forms, LMS)
  - Interview transcription (audio → text)

Transform:
  - Normalize belief statements to quantitative scores (0-1 scale)
  - Aggregate behavior metrics across systems
  - Calculate dissonance scores (|stated - actual|²)
  - Classify severity and type

Load:
  - Neo4j graph (organizations, dissonance patterns, interventions)
  - PostgreSQL (time-series metrics)
  - Document store (MongoDB for unstructured interview data)
```

### Data Quality and Ethics

```yaml
Quality_Assurance:
  - Cross-validate beliefs (multiple policy sources)
  - Audit behavior data accuracy (sample log checks)
  - Verify outcome data (independent audits)

Privacy_Protection:
  - Anonymize individual user data (aggregate only)
  - Secure storage (encryption at rest and in transit)
  - Access controls (need-to-know principle)

Ethical_Considerations:
  - Informed consent for surveys and interviews
  - Transparency about dissonance analysis purpose
  - No punitive use of individual behavior data
  - Focus on organizational improvement, not blame
```

---

## Conclusion

Detecting and resolving cognitive dissonance requires comprehensive data across beliefs (policies, statements), behaviors (logs, audits), and outcomes (incidents, audit findings). By systematically comparing stated intentions to observed actions and real-world results, we can quantify dissonance, identify root causes, and design targeted interventions.

**Key Principle:** Dissonance lives in the gaps. The more data sources, the more precisely we can map the gap between what organizations say (Symbolic) and what they do (Real).

---

**Data Source Summary Table:**

| Category | Primary Sources | Update Frequency | Integration Method |
|----------|----------------|------------------|-------------------|
| Stated Beliefs | Policies, surveys, executive comms | Annual/quarterly | NLP parsing, manual review |
| Observed Behaviors | Logs (patch, IAM, UBA), budgets | Real-time to monthly | API, scheduled reports |
| Outcomes | Incidents, audits, pentests | Incident-driven, annual | Manual aggregation, API |
| Benchmarks | Gartner, SANS, Verizon DBIR | Annual | Manual research, subscriptions |
| Interventions | Progress tracking, surveys | Weekly to monthly | Custom dashboards, Neo4j |

---

**References:**
1. Festinger, L. (1957). A Theory of Cognitive Dissonance. Stanford University Press.
2. Verizon. (2024). Data Breach Investigations Report. https://www.verizon.com/business/resources/reports/dbir/
3. IBM Security. (2024). Cost of a Data Breach Report. https://www.ibm.com/security/data-breach
4. Ponemon Institute. (2024). Cybersecurity Studies. https://www.ponemon.org/
5. SANS Institute. (2024). Security Surveys. https://www.sans.org/reading-room/

---

*Enhancement E24: Data Sources | v1.0.0 | Cognitive Dissonance Breaking Infrastructure*
