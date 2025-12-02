# NCC-OTCE-EAB-023-QILIN-SURGE-Enhanced.md

**Source**: NCC-OTCE-EAB-023-QILIN-SURGE-Enhanced.md.docx
**Converted**: Auto-converted from DOCX

---

EXPRESS ATTACK BRIEF 023

QILIN RANSOMWARE SURGE - 47.3% Attack Increase Critical Infrastructure

Classification: TLP:AMBER+STRICT
Date: August 7, 2025
Threat Level: CRITICAL
Campaign: Qilin RaaS Critical Infrastructure Targeting
Attribution: Qilin Ransomware Group (Agenda/Qilin)

🎯 EXECUTIVE SUMMARY

In June 2025, the Qilin ransomware group emerged as the most active ransomware threat globally, recording 81 victims and a staggering 47.3% surge in attacks. The group systematically exploits critical Fortinet vulnerabilities (CVE-2024-21762 and CVE-2024-55591) to target healthcare, professional services, and IT infrastructure with fully automated attack methodologies. This represents the most significant ransomware escalation of 2025, with healthcare organizations facing unprecedented risk.

Key Impact Metrics:

Monthly Victims: 81 organizations (June 2025)

Attack Surge: 47.3% increase over previous months

Total Historical Victims: 310+ since emergence

Healthcare Attacks: 24 attacks in first 5 months of 2025

Automation Level: Fully automated except victim selection

🌐 THREAT LANDSCAPE

Primary Threat Actor: Qilin Ransomware Group

Also Known As: Agenda ransomware

Operation Type: Ransomware-as-a-Service (RaaS)

Activity Since: 2022+ with major escalation in 2025

Specialization: Healthcare targeting, critical infrastructure attacks

Geographic Focus: Global, with current emphasis on Spanish-speaking countries

Business Model: Multi-layered extortion with data theft and encryption

Campaign Context

The June 2025 surge represents the most significant ransomware escalation of the year:

Healthcare Dominance: Leading ransomware threat to healthcare sector

Automation Evolution: Fully automated attack deployment

Critical Infrastructure: Systematic targeting of essential services

Global Expansion: Expanding from Spanish-speaking focus to worldwide

Vulnerability Weaponization: Rapid exploitation of Fortinet zero-days

🔍 ATTACK TIMELINE

Phase 1: Infrastructure Reconnaissance (May 2025)

Target Identification: Scanning for vulnerable Fortinet devices globally

Vulnerability Assessment: CVE-2024-21762 and CVE-2024-55591 exploitation

Victim Profiling: Healthcare and professional services prioritization

Attack Automation: Development of partially automated deployment systems

Phase 2: Mass Exploitation Campaign (June 1-15, 2025)

Initial Access: Exploitation of unpatched Fortinet systems

Privilege Escalation: Super-admin access through authentication bypass

Lateral Movement: Network reconnaissance and domain compromise

Data Exfiltration: Systematic collection of sensitive information

Phase 3: Ransomware Deployment (June 15-30, 2025)

Encryption Phase: Automated Qilin ransomware deployment

Multi-layered Extortion: Combination of encryption and data exposure threats

Ransom Demands: Variable pricing based on organization size and impact

Communication Establishment: Direct victim contact and negotiation

Phase 4: Peak Activity Achievement (June 30, 2025)

81 Confirmed Victims: Highest monthly total for any ransomware group

47.3% Surge: Unprecedented increase in ransomware activity

Global Recognition: Identified as most active ransomware threat

Continued Operations: Sustained high-level activity into July 2025

💥 IMPACT ASSESSMENT

Healthcare Sector Devastation

24 Healthcare Attacks: In first 5 months of 2025

Major Victims: The Health Trust (CA), Next Step Healthcare (MA), Central Texas Pediatric Orthopedics

NHS Impact: Synnovis pathology services still not fully recovered from 2024 attack

Patient Care Disruption: Critical medical services interrupted across multiple facilities

Professional Services & IT Sectors

Professional Services: 60 victims in June 2025 alone

Information Technology: 50 victims targeted for supply chain impact

Business Operations: Complete operational shutdown during encryption

Data Breach: Sensitive client and business data stolen and threatened with exposure

Critical Infrastructure Impact

Fortinet Infrastructure: Thousands of vulnerable devices globally

Network Security: VPN and firewall systems compromised

Remote Access: Critical business continuity systems disrupted

Supply Chain: IT service providers compromised, affecting downstream clients

🔧 TECHNICAL ANALYSIS

Exploited Vulnerabilities

CVE-2024-21762 (Critical)

Component: FortiOS/FortiProxy

Type: Out-of-bounds Write Vulnerability

CVSS Score: Critical (9.0+)

Impact: Remote code execution

Exploitation: Pre-authentication attack vector

Patch Status: Available but many systems unpatched

CVE-2024-55591 (Critical)

Component: FortiOS/FortiProxy

Type: Authentication Bypass Vulnerability

CVSS Score: Critical (9.0+)

Impact: Super-admin privilege escalation

Exploitation: Used in conjunction with CVE-2024-21762

Patch Status: Emergency patches released

Attack Methodology

Automated Scanning: Global identification of vulnerable Fortinet devices

Vulnerability Chaining: Combined exploitation of both CVEs for maximum access

Privilege Escalation: Super-admin access through authentication bypass

Network Compromise: Domain controller and critical system access

Data Harvesting: Systematic exfiltration before encryption

Ransomware Deployment: Automated Qilin payload distribution

Multi-layered Extortion: Combined encryption and data exposure threats

Technical Indicators

Attack Automation: Fully automated deployment with manual victim selection

Encryption Speed: Rapid network-wide encryption capabilities

Data Exfiltration: Pre-encryption data theft for extortion leverage

Communication: Dedicated negotiation portals and victim communication

Payment Processing: Cryptocurrency payment systems integration

🌍 GEOGRAPHIC IMPACT

Primary Impact Regions

Spanish-speaking Countries: Initial focus with highest concentration

North America: Major healthcare and professional services targeting

Europe: Healthcare systems and critical infrastructure attacks

Global Expansion: Campaign expanding worldwide from regional focus

Sector Distribution (June 2025)

Professional Goods & Services: 60 victims (74% of total attacks)

Healthcare: 52 victims (64% of attacks)

Information Technology: 50 victims (62% of attacks)

Cross-sector Impact: Multiple industries affected simultaneously

💰 BUSINESS IMPACT ANALYSIS

Direct Financial Impact

Ransom Payments: Variable demands based on organization size

Incident Response: $500K-$2M+ per incident for forensics and recovery

System Rebuilding: $1M-$5M+ for infrastructure replacement

Business Interruption: $100K-$1M+ per day of operational downtime

Healthcare Specific: Patient care delays, procedure cancellations, revenue loss

Healthcare Sector Impact

Patient Safety: Critical care delays and procedure cancellations

Medical Records: Patient health information compromised and encrypted

Regulatory Compliance: HIPAA violations and potential fines

Reputation Damage: Public trust erosion in healthcare cybersecurity

Long-term Recovery: Extended periods for full operational restoration

Long-term Strategic Impact

Fortinet Trust: Reduced confidence in Fortinet security products

Healthcare Targeting: Increased insurance premiums and security requirements

Automation Threat: Demonstration of successful fully automated attacks

Ransomware Evolution: New standard for attack sophistication and speed

🛡️ MITIGATION STRATEGIES

Immediate Actions (0-7 Days)

Emergency Patching: CVE-2024-21762 and CVE-2024-55591 patches applied immediately

Fortinet Device Audit: Complete inventory and security assessment

Network Segmentation: Critical systems isolated from compromised networks

Backup Verification: Offline backup integrity and restoration capability

Incident Response: Activation of ransomware response procedures

Short-term Actions (7-30 Days)

Enhanced Monitoring: Advanced threat detection for Qilin indicators

Vulnerability Management: Accelerated patching procedures implementation

Access Control: Multi-factor authentication on all critical systems

Staff Training: Ransomware awareness and response training

Communication Plans: Internal and external crisis communication procedures

Long-term Actions (30+ Days)

Security Architecture: Zero-trust implementation and network redesign

Vendor Security: Enhanced due diligence for all security vendors

Healthcare Specific: Enhanced patient data protection and medical device security

Automation Defense: AI-powered threat detection and response systems

Industry Collaboration: Healthcare sector threat intelligence sharing

📊 THREAT INTELLIGENCE

Qilin Ransomware Group Profile

Ransomware Family: Qilin/Agenda

First Observed: 2022

Total Victims: 310+ confirmed attacks

Primary Motivation: Financial gain through extortion

Target Sectors: Healthcare (primary), professional services, IT

Geographic Focus: Global with Spanish-speaking emphasis

Attack Sophistication

Automation Level: Fully automated except victim selection

Zero-day Usage: Rapid weaponization of newly disclosed vulnerabilities

Multi-layered Extortion: Data theft + encryption + public exposure threats

Payment Processing: Professional cryptocurrency payment systems

Customer Service: Dedicated victim communication and negotiation portals

June 2025 Campaign Statistics

81 Confirmed Victims: Highest monthly total for any ransomware group

47.3% Activity Surge: Unprecedented monthly increase

Automation Success: Demonstrated effectiveness of automated attacks

Global Reach: Expansion from regional to worldwide operations

Healthcare Dominance: Leading threat to healthcare sector

🎯 RECOMMENDATIONS

For Healthcare Organizations

Emergency Patching: Immediate Fortinet vulnerability remediation

Medical Device Security: Enhanced protection for IoT and medical devices

Patient Data Protection: Enhanced encryption and access controls

Backup Strategies: Air-gapped backups with rapid restoration capability

Regulatory Compliance: Enhanced HIPAA cybersecurity measures

For Professional Services

Client Data Protection: Enhanced data security and client communication

Business Continuity: Robust operational continuity planning

Vendor Management: Third-party risk assessment and monitoring

Incident Response: Rapid containment and client notification procedures

Insurance Coverage: Comprehensive cybersecurity insurance evaluation

For IT Service Providers

Supply Chain Security: Enhanced security for client service delivery

Multi-tenant Architecture: Isolation and segmentation for client protection

Threat Intelligence: Real-time monitoring for Qilin indicators

Client Communication: Proactive security advisory and warning systems

Incident Coordination: Multi-client incident response capabilities

📈 LESSONS LEARNED

Automation Threat Evolution

Speed Advantage: Automated attacks significantly faster than manual operations

Scale Achievement: Single group achieving unprecedented victim counts

Defense Challenges: Traditional security measures insufficient against automation

Detection Gaps: Automated attacks may evade human-centric detection systems

Critical Infrastructure Vulnerability

Single Point Failure: Critical vulnerabilities enabling mass exploitation

Patch Management: Urgent need for accelerated patch deployment procedures

Vendor Responsibility: Enhanced security development and rapid response requirements

Industry Coordination: Need for coordinated vulnerability disclosure and patching

Healthcare Sector Risk

Patient Safety: Direct impact on critical patient care services

Data Sensitivity: High-value target for both encryption and data theft

Recovery Complexity: Extended downtime affecting life-safety systems

Regulatory Impact: Significant compliance and legal consequences

🔗 REFERENCES & SOURCES

Primary Intelligence Sources

CYFIRMA Ransomware Tracking Report (June 2025)

DataBreaches.Net Qilin Analysis (July 2025)

CyberMaxx Healthcare Threat Assessment (2025)

BleepingComputer Technical Analysis

HIPAA Journal Healthcare Impact Report

Vulnerability Information

CVE-2024-21762 - Fortinet FortiOS Out-of-bounds Write

CVE-2024-55591 - Fortinet Authentication Bypass

Fortinet Security Advisory PSIRT-24-0147

CISA Known Exploited Vulnerabilities Catalog

Healthcare Impact Analysis

NHS Synnovis Attack Case Study (2024-2025)

Healthcare Cybersecurity Coordination Center Report

American Hospital Association Security Alert

Health-ISAC Threat Intelligence Bulletin

Technical Analysis

Cybersecurity News Technical Breakdown

SC Media Attack Campaign Analysis

AmpCus Cyber Shadow Intelligence Report

Varutra Threat Intelligence Assessment

Document Control:

Version: 1.0

Last Updated: August 7, 2025

Next Review: September 7, 2025

Distribution: TLP:AMBER+STRICT

Expiration: 90 days from publication

Emergency Contact Information:

Healthcare Incidents: Healthcare Cybersecurity Coordination Center

Critical Infrastructure: CISA Emergency Response

Technical Support: NCC Group Incident Response

Media Inquiries: Communications Department

This Express Attack Brief provides critical intelligence for healthcare and critical infrastructure protection. Healthcare organizations should treat this as an emergency security alert requiring immediate action.