# Patch Management and Deployment Operations

## Overview
Patch management operations encompass vulnerability assessment, patch testing in staging environments, staged production rollout, rollback procedures, and compliance reporting ensuring systems remain secure against known vulnerabilities while minimizing disruption risk from untested updates or compatibility issues.

## Operational Procedures

### 1. Vulnerability Assessment and Prioritization
- **Vulnerability Scanning**: Weekly automated scans identify missing patches, misconfigurations, and known vulnerabilities (Nessus, Qualys, Rapid7)
- **CVSS Scoring**: Common Vulnerability Scoring System (0-10 scale) prioritizes remediation efforts; critical (9.0-10.0) patches deployed within 15 days per NIST guidance
- **Exploit Availability**: Public exploits or active exploitation (CISA KEV catalog) elevate priority; zero-day vulnerabilities trigger emergency patching
- **Asset Criticality**: Patch urgency multiplied by asset value/criticality; internet-facing systems and crown-jewel assets prioritized over isolated test systems

### 2. Patch Acquisition and Review
- **Vendor Security Bulletins**: Microsoft Patch Tuesday (2nd Tuesday monthly), Oracle Critical Patch Updates (quarterly), Adobe patches monitored via RSS and email
- **Patch Download**: Security updates downloaded from official vendor channels (WSUS, Red Hat Satellite, SCCM) preventing supply-chain compromises
- **Release Notes Review**: Patch descriptions analyzed for breaking changes, reboot requirements, and potential compatibility issues before deployment
- **CVE Mapping**: Patches mapped to specific CVE identifiers enabling tracking from vulnerability scan through remediation verification

### 3. Test Environment Validation
- **Non-Production Testing**: Patches deployed to dev/test environments mirroring production configurations detecting compatibility issues before production rollout
- **Application Testing**: QA teams perform smoke testing and regression testing validating patches don't break critical business applications
- **Performance Benchmarking**: System performance metrics (CPU, memory, response time) compared pre/post patching detecting performance regressions
- **Rollback Testing**: Patch uninstall procedures tested in lab validating rapid rollback capability if production issues encountered

### 4. Change Management and Approval
- **Change Advisory Board (CAB)**: Major patch deployments presented to CAB with risk assessment, testing results, and rollback plan
- **Standard Change Classification**: Pre-approved low-risk patches (security patches from major vendors) skip CAB approval enabling rapid deployment
- **Emergency Change Process**: Critical zero-day vulnerabilities use expedited approval; retrospective CAB review within 48 hours
- **Maintenance Windows**: Patches scheduled during approved maintenance windows; emergency patches may require out-of-window deployment with executive approval

### 5. Staged Production Deployment
- **Pilot Group Deployment**: Patches deployed to 5-10% of production fleet; monitored 24-48 hours for issues before broad rollout
- **Phased Rollout**: Gradual deployment across geographic regions or business units limits blast radius if issues emerge
- **Deployment Scheduling**: Non-critical systems patched during business hours enabling immediate support; critical systems patched during low-usage periods
- **Reboot Orchestration**: Clustered applications patched one node at a time maintaining service availability; servers rebooted sequentially not concurrently

### 6. Post-Deployment Verification
- **Compliance Scanning**: Vulnerability scans 48 hours post-deployment verify patches successfully installed and vulnerabilities remediated
- **Health Checks**: Automated monitoring verifies system services started successfully, applications responding, and no spike in error rates
- **User Feedback**: Help desk monitors for spike in incident tickets post-patching; clusters of issues trigger investigation and potential rollback
- **Patch Audit Reports**: Compliance reports demonstrate patching timeliness meeting regulatory requirements (PCI-DSS 30-day critical, NIST 15-day critical)

### 7. Rollback and Contingency Procedures
- **Pre-Patch Snapshots**: Virtual machine snapshots or system state backups taken before patching enabling rapid restore if failures occur
- **Patch Uninstallation**: Patches uninstalled via native tools (wusa /uninstall, yum history undo) when causing issues; verified in testing beforehand
- **Rollback Decision Criteria**: Predefined thresholds (>5% failed patches, critical application failures, >10% increase in support tickets) trigger rollback
- **Communication Plans**: Stakeholders notified of rollback decisions; post-incident review determines root cause and path forward for problematic patches

## System Integration Points

### Patch Management Platforms
- **WSUS (Windows Server Update Services)**: Microsoft's free patch distribution system; downloads patches once and distributes internally
- **SCCM (System Center Configuration Manager)**: Enterprise patch management with compliance reporting, staged deployments, and third-party patch support
- **Red Hat Satellite**: Centralized management for RHEL systems; patches, provisioning, and configuration management integrated
- **Ivanti Patch Management**: Multi-platform support (Windows, Linux, macOS, third-party apps) with automated testing and deployment workflows

### Vulnerability Management Integration
- **Vulnerability-to-Patch Mapping**: Nessus, Qualys vulnerability scan results automatically matched to required patches from vendors
- **Risk-Based Prioritization**: Tenable.io Risk-Based Vulnerability Management scores threats considering exploit availability and asset criticality
- **SLA Tracking**: Time-to-remediation tracked from vulnerability discovery through patch deployment verifying compliance with security policies
- **Exception Management**: Risks accepted with documented business justification when patches unavailable or cause compatibility issues

### IT Service Management (ITSM)
- **Automated Change Requests**: Patch deployment workflows automatically create change tickets in ServiceNow or Remedy with pre-populated details
- **Approval Workflows**: CAB members review and approve change requests via ITSM platform; automated deployment triggered upon approval
- **Incident Correlation**: Post-patching incidents linked to change records enabling impact analysis and root cause identification
- **Knowledge Base Integration**: Patch deployment procedures and known issues documented in KB articles referenced during changes

### Security Information and Event Management (SIEM)
- **Patch Event Logging**: Successful and failed patch installations logged to SIEM for security monitoring and compliance auditing
- **Anomaly Detection**: Unusual patching patterns (off-hours deployments, high failure rates) trigger security investigation
- **Compliance Dashboards**: Real-time view of patch compliance by system, organizational unit, and criticality for executive visibility
- **Threat Intelligence Correlation**: SIEM correlates CVEs with exploit attempts in logs prioritizing patches for actively exploited vulnerabilities

## Regulatory Compliance

### PCI-DSS Requirement 6.2
- **Critical Patch Timeline**: Vendor-released security patches classified as critical must be installed within 30 days of release
- **Monthly Patching Cadence**: Systems handling cardholder data require monthly patch reviews and deployments maintaining 30-day window
- **Risk Assessment for Delays**: Patches not installed within 30 days require documented risk assessment and compensating controls
- **Patch Testing Requirements**: Patches tested to determine impact on security configuration before production deployment

### NIST 800-53 SI-2 (Flaw Remediation)
- **15-Day Critical Patch Window**: NIST recommends critical vulnerabilities remediated within 15 days of patch availability for moderate/high impact systems
- **Automated Patch Verification**: Automated mechanisms used to determine if applicable patches installed and report status
- **Continuous Monitoring**: Ongoing vulnerability scanning and patch status monitoring detecting unpatched systems within 24-72 hours
- **Remediation Tracking**: Metrics track time from vulnerability discovery to patch deployment identifying process improvement opportunities

### HIPAA Security Rule
- **Risk Analysis Requirement**: Security risk analysis determines patching frequency and urgency based on ePHI exposure risk
- **Security Awareness Training**: Workforce trained on malware protection and importance of timely patching preventing breaches
- **Contingency Planning**: Patch deployment procedures integrated with disaster recovery and business continuity plans
- **Audit Controls**: Patch deployment activities logged for HIPAA compliance audits demonstrating due diligence in security maintenance

### FedRAMP Continuous Monitoring
- **30-Day High Vulnerability Remediation**: FedRAMP requires high-severity vulnerabilities remediated within 30 days of discovery
- **90-Day Moderate Vulnerability Remediation**: Moderate-severity vulnerabilities remediated within 90 days
- **Monthly Security Scanning**: Authorized monthly vulnerability scans required; false positives documented with evidence
- **Plan of Action and Milestones (POA&M)**: Vulnerabilities not yet remediated tracked in POA&M with target completion dates

## Equipment and Vendors

### Enterprise Patch Management
- **Microsoft SCCM/Intune**: Comprehensive endpoint management with patch distribution, OS deployment, and application management
- **Ivanti Patch for Windows/Linux**: Multi-platform patching with extensive third-party application support (Adobe, Java, browsers)
- **ManageEngine Patch Manager Plus**: Unified patching for Windows, macOS, Linux, and 850+ third-party applications
- **BMC TrueSight Patch Management**: Enterprise-scale patching integrated with ITSM for change/incident correlation

### Vulnerability Management Platforms
- **Tenable Nessus/Tenable.io**: Industry-standard vulnerability scanner with risk-based prioritization and compliance templates
- **Qualys VMDR**: Cloud-based vulnerability management with continuous monitoring and patch verification
- **Rapid7 InsightVM**: Vulnerability management with live dashboards, risk scoring, and remediation workflow automation
- **CrowdStrike Spotlight**: Vulnerability assessment integrated with EDR providing real-time visibility of unpatched endpoints

### Linux/Unix Patch Management
- **Red Hat Satellite**: Centralized management for RHEL systems with content lifecycle management and compliance reporting
- **SUSE Manager**: Similar to Satellite for SUSE Enterprise Linux; supports configuration management and patching orchestration
- **Ansible Automation Platform**: Infrastructure-as-code approach to patch deployment with idempotent playbooks and dynamic inventories
- **Uyuni (formerly SUSE Manager Open Source)**: Open-source systems management supporting RHEL, SLES, Ubuntu, and Debian patching

### Application and Third-Party Patching
- **Chocolatey for Business**: Package manager for Windows automating third-party application deployments and updates
- **Ninite Pro**: Automated third-party application patching for common software (browsers, Java, Adobe Reader, etc.)
- **PDQ Deploy**: Software deployment tool popular for third-party patching in Windows environments
- **Flexera App Portal**: Application lifecycle management with vulnerability detection and automated remediation workflows

## Performance Metrics

### Patch Compliance Metrics
- **Overall Patch Compliance Rate**: Percentage of systems fully patched per current baselines; target >95% for production, 100% for critical systems
- **Critical Vulnerability MTTР**: Mean Time to Patch critical vulnerabilities; target <15 days per NIST guidance
- **High Vulnerability MTTP**: Mean Time to Patch high vulnerabilities; target <30 days aligning with PCI-DSS requirements
- **Patch Age Distribution**: Histogram showing patch ages; concentration of old patches indicates systemic issues requiring process improvement

### Deployment Success Metrics
- **Patch Success Rate**: Percentage of patch deployments completing successfully without errors; target >95%
- **Reboot Success Rate**: Percentage of systems successfully rebooting post-patch; <95% indicates instability requiring investigation
- **Rollback Rate**: Percentage of patches requiring rollback due to issues; target <2% indicating effective testing procedures
- **Deployment Window Adherence**: Percentage of patches deployed within approved maintenance windows; 100% compliance required

### Operational Efficiency
- **Time in Test Environment**: Average days patches spend in testing before production deployment; balance thoroughness against exposure risk
- **Patching Automation Rate**: Percentage of patches deployed via automation vs. manual processes; >80% automation target
- **Mean Time to Deploy (MTTD)**: Average time from patch availability to production deployment; varies by severity (critical <15d, moderate <30d)
- **Patching Labor Hours**: Total staff hours per month spent on patching activities; reduction via automation reduces costs

### Risk Metrics
- **Unpatched Internet-Facing Assets**: Number of external-facing systems with known vulnerabilities; top priority for remediation
- **Actively Exploited Vulnerabilities**: Count of unpatched systems vulnerable to exploits in CISA KEV catalog; emergency remediation required
- **Critical Asset Patch Gap**: Number of crown-jewel systems missing critical patches; executive visibility and accountability
- **Patch-Related Incidents**: Monthly count of security incidents attributable to unpatched systems; KPI for security program effectiveness

---

**Document Control**
- **Version**: 1.0
- **Last Updated**: 2025-11-06
- **Regulatory References**: PCI-DSS v4.0 Requirement 6.2, NIST 800-53 SI-2, HIPAA Security Rule 164.308, FedRAMP Continuous Monitoring, CIS Controls v8
- **Review Cycle**: Quarterly
