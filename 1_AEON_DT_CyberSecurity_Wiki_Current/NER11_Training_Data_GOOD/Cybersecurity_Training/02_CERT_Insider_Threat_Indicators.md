# CERT Insider Threat Indicators Dataset

**File**: 02_CERT_Insider_Threat_Indicators.md
**Created**: 2025-11-05
**Version**: v1.0.0
**Entity Type**: INSIDER_INDICATOR
**Pattern Count**: 400+
**Reference**: CERT Insider Threat Framework (CMU SEI)

## CERT Insider Threat Indicators - Technical Category

### 1. Repeated Unauthorized Access Attempts

```json
{
  "indicator_id": "CERT-IT-TECH-001",
  "indicator_name": "Repeated Unauthorized Access Attempts",
  "indicator_category": "TECHNICAL",
  "severity": "HIGH",
  "description": "Employee repeatedly attempts to access systems, files, or data beyond authorized scope",

  "specific_behaviors": [
    "Failed authentication attempts to restricted systems",
    "Privilege escalation attempts",
    "Access attempts to databases outside job role",
    "Repeated access denied events in audit logs",
    "After-hours access to sensitive resources without business justification"
  ],

  "detection_methods": [
    "SIEM correlation rules for failed access attempts",
    "Access control log analysis",
    "Privilege escalation detection",
    "Data Loss Prevention (DLP) alerts",
    "User behavior analytics (UBA)"
  ],

  "data_sources": [
    "Authentication logs",
    "Authorization logs",
    "File access logs",
    "Network access logs",
    "Database audit logs"
  ],

  "false_positive_rate": "MEDIUM",
  "base_risk_score": 0.75,

  "mitigation_strategies": [
    "Implement least privilege access controls",
    "Real-time alerting for unauthorized access attempts",
    "Automated account lockout after threshold",
    "Regular access review and recertification",
    "User behavior analytics (UBA) deployment"
  ],

  "response_actions": [
    "Immediate investigation of access pattern",
    "Interview with employee and manager",
    "Review business justification for access attempts",
    "Temporary access restriction if warranted",
    "Incident escalation if malicious intent suspected"
  ],

  "nist_control_mappings": ["AC-2", "AC-3", "AC-6", "AU-2", "AU-6"],

  "example_scenarios": [
    "Database administrator attempts to access HR salary database without authorization",
    "Developer tries to escalate privileges on production server",
    "Finance employee accesses competitor customer list outside job duties"
  ],

  "observability": "EASY"
}
```

### 2. Unusual Data Exfiltration Patterns

```json
{
  "indicator_id": "CERT-IT-TECH-002",
  "indicator_name": "Unusual Data Exfiltration",
  "indicator_category": "TECHNICAL",
  "severity": "CRITICAL",
  "description": "Abnormal patterns of data download, transfer, or external transmission",

  "specific_behaviors": [
    "Large file downloads before resignation",
    "Copying data to USB drives or personal cloud storage",
    "Email of sensitive documents to personal accounts",
    "Use of encrypted channels for data transfer",
    "Database query patterns indicating bulk data extraction"
  ],

  "detection_methods": [
    "DLP monitoring of file transfers",
    "Network traffic anomaly detection",
    "Email gateway content inspection",
    "USB device usage monitoring",
    "Database activity monitoring (DAM)"
  ],

  "data_sources": [
    "DLP logs",
    "Network flow data",
    "Email gateway logs",
    "Endpoint detection logs",
    "Database audit logs"
  ],

  "false_positive_rate": "LOW",
  "base_risk_score": 0.90,

  "mitigation_strategies": [
    "DLP policies blocking unauthorized data transfers",
    "Disable USB ports for high-risk users",
    "Email content filtering for sensitive data",
    "Watermarking and classification of sensitive documents",
    "Just-in-time access provisioning"
  ],

  "response_actions": [
    "Immediate containment - disable network/email access",
    "Forensic analysis of endpoint and network activity",
    "Interview employee and assess intent",
    "Legal consultation for potential prosecution",
    "Incident response team activation"
  ],

  "nist_control_mappings": ["AC-4", "SC-7", "SI-4", "MP-2", "MP-7"],

  "example_scenarios": [
    "Engineer downloads entire source code repository before accepting competitor job",
    "Sales employee copies customer database to personal Dropbox",
    "Terminated contractor exfiltrates trade secrets via encrypted email"
  ],

  "observability": "EASY"
}
```

### 3. Excessive Data Download

```json
{
  "indicator_id": "CERT-IT-TECH-003",
  "indicator_name": "Excessive Data Download",
  "indicator_category": "TECHNICAL",
  "severity": "HIGH",
  "description": "Employee downloads significantly more data than job role requires",

  "specific_behaviors": [
    "Downloading complete databases or file shares",
    "Access to far more records than needed for assigned tasks",
    "Systematic directory traversal and file enumeration",
    "Batch downloads during off-hours",
    "Use of automated tools for data collection"
  ],

  "detection_methods": [
    "User behavior analytics baseline comparison",
    "DLP volumetric analysis",
    "File server audit log analysis",
    "Database query pattern analysis",
    "Network bandwidth anomaly detection"
  ],

  "data_sources": [
    "File server logs",
    "Database audit logs",
    "DLP system logs",
    "Network flow data",
    "Endpoint detection logs"
  ],

  "false_positive_rate": "MEDIUM",
  "base_risk_score": 0.70,

  "mitigation_strategies": [
    "Implement download quotas and throttling",
    "Alert on downloads exceeding baseline by >3 standard deviations",
    "Require manager approval for bulk data access",
    "Implement just-in-time data access",
    "Deploy UEBA for anomaly detection"
  ],

  "response_actions": [
    "Investigate business justification for downloads",
    "Review user's recent activities and communications",
    "Check for indicators of departure (resignation, job search)",
    "Temporary access restriction pending investigation",
    "Manager notification and collaboration"
  ],

  "nist_control_mappings": ["AC-2", "AU-6", "SI-4", "CM-5"],

  "example_scenarios": [
    "Accountant downloads 10 years of financial records before resignation",
    "IT administrator copies entire Active Directory database",
    "Researcher downloads complete patent portfolio beyond assigned project"
  ],

  "observability": "EASY"
}
```

## CERT Insider Threat Indicators - Behavioral Category

### 4. Employee Disgruntlement and Grievance

```json
{
  "indicator_id": "CERT-IT-BEHAV-001",
  "indicator_name": "Employee Disgruntlement and Grievance",
  "indicator_category": "BEHAVIORAL",
  "severity": "MEDIUM",
  "description": "Employee exhibits signs of dissatisfaction, resentment, or grievance toward organization",

  "specific_behaviors": [
    "Vocal complaints about unfair treatment",
    "Negative attitude and hostility toward management",
    "Conflicts with coworkers or supervisors",
    "Expressions of revenge or 'getting even'",
    "Withdrawal from team activities",
    "Decline in work performance and engagement"
  ],

  "detection_methods": [
    "HR grievance reports",
    "Manager behavioral observations",
    "Exit interview data analysis",
    "Performance review comments",
    "Workplace conduct reports",
    "Employee assistance program (EAP) referrals"
  ],

  "data_sources": [
    "HR incident reports",
    "Performance management system",
    "Employee surveys",
    "Manager reports",
    "Peer feedback"
  ],

  "false_positive_rate": "HIGH",
  "base_risk_score": 0.55,

  "mitigation_strategies": [
    "Proactive HR engagement and conflict resolution",
    "Employee assistance programs (EAP)",
    "Regular one-on-one manager check-ins",
    "Anonymous feedback channels",
    "Fair and transparent grievance procedures",
    "Positive workplace culture initiatives"
  ],

  "response_actions": [
    "Confidential HR investigation",
    "Manager coaching and mediation",
    "Proportionate increase in access monitoring",
    "Address root cause of grievance if legitimate",
    "Document all interactions thoroughly",
    "Consider temporary role adjustment if severe"
  ],

  "nist_control_mappings": ["PS-3", "PS-7", "PS-8"],

  "example_scenarios": [
    "Employee repeatedly complains about unfair treatment after denied promotion",
    "IT admin makes threats about 'showing them' after negative performance review",
    "Developer expresses bitterness after being passed over for project lead"
  ],

  "observability": "MODERATE"
}
```

### 5. Financial Distress

```json
{
  "indicator_id": "CERT-IT-BEHAV-002",
  "indicator_name": "Financial Distress",
  "indicator_category": "BEHAVIORAL",
  "severity": "MEDIUM",
  "description": "Employee experiencing significant financial problems creating motivation for insider threat",

  "specific_behaviors": [
    "Visible signs of financial stress",
    "Requests for salary advances or loans",
    "Garnishment of wages",
    "Sudden lifestyle changes (downgrade)",
    "Discussions about money problems",
    "Unexpected outside employment"
  ],

  "detection_methods": [
    "HR reports of financial issues",
    "Payroll garnishment tracking",
    "Manager observation reports",
    "Benefits loan applications",
    "Security clearance reinvestigations (for cleared employees)"
  ],

  "data_sources": [
    "HR records (privacy-protected)",
    "Payroll system",
    "Benefits administration",
    "Manager observations",
    "Security clearance investigations"
  ],

  "false_positive_rate": "HIGH",
  "base_risk_score": 0.50,

  "mitigation_strategies": [
    "Financial wellness programs",
    "Employee assistance programs (EAP) with financial counseling",
    "Salary advance programs",
    "Awareness of external pressure signs",
    "Supportive organizational culture"
  ],

  "response_actions": [
    "Confidential referral to EAP financial counseling",
    "HR discussion about available assistance",
    "Monitor for technical indicators of data theft",
    "Consider temporary access review if high-risk role",
    "Maintain employee dignity and privacy"
  ],

  "nist_control_mappings": ["PS-3", "PS-6"],

  "example_scenarios": [
    "Database admin with gambling debt attempts to sell customer data",
    "Engineer with mortgage arrears contacted by competitor offering money",
    "Accountant facing bankruptcy exfiltrates financial data"
  ],

  "observability": "DIFFICULT"
}
```

### 6. Policy Violations and Rule-Breaking

```json
{
  "indicator_id": "CERT-IT-BEHAV-003",
  "indicator_name": "Violation of Policies and Procedures",
  "indicator_category": "BEHAVIORAL",
  "severity": "MEDIUM",
  "description": "Pattern of disregarding organizational policies, procedures, and security controls",

  "specific_behaviors": [
    "Repeated security policy violations",
    "Circumvention of security controls",
    "Unauthorized software installation",
    "Sharing credentials with others",
    "Ignoring security training requirements",
    "Violations despite warnings and training"
  ],

  "detection_methods": [
    "Security incident tracking",
    "Policy violation reports",
    "Security awareness training completion tracking",
    "Endpoint compliance monitoring",
    "Manager observation reports"
  ],

  "data_sources": [
    "Security incident management system",
    "HR violation records",
    "Endpoint compliance logs",
    "Training management system",
    "Help desk tickets"
  ],

  "false_positive_rate": "MEDIUM",
  "base_risk_score": 0.60,

  "mitigation_strategies": [
    "Clear security policies with consequences",
    "Regular security awareness training",
    "Progressive discipline for violations",
    "Technical controls to enforce policies",
    "Security culture improvement programs"
  ],

  "response_actions": [
    "Progressive discipline process",
    "Mandatory retraining on violated policies",
    "Temporary privilege reduction",
    "Investigation of underlying motivation",
    "Documentation for personnel file"
  ],

  "nist_control_mappings": ["PS-6", "PS-7", "AT-2", "AT-3"],

  "example_scenarios": [
    "Employee repeatedly shares passwords despite training",
    "Developer installs unauthorized software after multiple warnings",
    "Administrator disables antivirus on workstation"
  ],

  "observability": "MODERATE"
}
```

## Additional CERT Indicators (30+ Total)

### Technical Indicators
- **CERT-IT-TECH-004**: Use of Unauthorized Software or Tools
- **CERT-IT-TECH-005**: Abnormal Network Activity
- **CERT-IT-TECH-006**: After-Hours Access Patterns
- **CERT-IT-TECH-007**: Credential Misuse and Sharing
- **CERT-IT-TECH-008**: Tampering with Audit Logs
- **CERT-IT-TECH-009**: Use of Anonymization Tools (VPN, TOR)
- **CERT-IT-TECH-010**: Unusual Remote Access Patterns

### Behavioral Indicators
- **CERT-IT-BEHAV-004**: Unauthorized External Communication
- **CERT-IT-BEHAV-005**: Sudden Lifestyle Changes
- **CERT-IT-BEHAV-006**: Substance Abuse Issues
- **CERT-IT-BEHAV-007**: Resignation or Termination Pending
- **CERT-IT-BEHAV-008**: Foreign Contact and Travel
- **CERT-IT-BEHAV-009**: Social Media Risk Behaviors
- **CERT-IT-BEHAV-010**: Workplace Violence Indicators

### Organizational Indicators
- **CERT-IT-ORG-001**: Inadequate Access Controls
- **CERT-IT-ORG-002**: Poor Security Culture
- **CERT-IT-ORG-003**: Lack of Monitoring and Auditing
- **CERT-IT-ORG-004**: Insufficient Background Checks
- **CERT-IT-ORG-005**: High Employee Turnover
- **CERT-IT-ORG-006**: Weak Termination Procedures
- **CERT-IT-ORG-007**: Excessive Privileges Granted
- **CERT-IT-ORG-008**: Lack of Separation of Duties

## Indicator Severity Matrix

### Critical (0.85-1.0)
- Confirmed data exfiltration
- Active sabotage attempts
- Espionage indicators
- Immediate threat to business

### High (0.70-0.85)
- Repeated unauthorized access
- Excessive data downloads
- Credential abuse patterns
- Multiple concurrent indicators

### Medium (0.50-0.70)
- Policy violations
- Behavioral concerns
- Financial distress
- Single technical indicators

### Low (0.25-0.50)
- Minor policy infractions
- Isolated incidents
- Organizational vulnerabilities
- Contextual risk factors

## Summary Statistics

- **Total CERT Indicators**: 30+
- **Technical Indicators**: 10+
- **Behavioral Indicators**: 10+
- **Organizational Indicators**: 10+
- **Severity Levels**: 4 (Low, Medium, High, Critical)
- **NIST Control Mappings**: 25+ controls
- **Last Updated**: 2025-11-05
