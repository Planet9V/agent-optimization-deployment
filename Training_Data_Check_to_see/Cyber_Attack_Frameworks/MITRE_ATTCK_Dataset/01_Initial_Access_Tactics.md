# MITRE ATT&CK: Initial Access Tactics

## Overview
Initial Access consists of techniques that use various entry vectors to gain their initial foothold within a network. Techniques used to gain a foothold include targeted spearphishing and exploiting weaknesses on public-facing web servers.

## Techniques

### T1190: Exploit Public-Facing Application
**Entity Type:** TECHNIQUE
**Tactic:** Initial Access
**Platform:** Windows, Linux, macOS, Network, Containers

**Description:**
Adversaries may attempt to exploit a weakness in an Internet-facing host or system to initially access a network. The weakness in the system can be a software bug, a temporary glitch, or a misconfiguration.

**Detection:**
- Monitor application logs for abnormal behavior
- Use vulnerability scanning to identify potential exploit targets
- Implement intrusion detection systems (IDS)
- Monitor for suspicious network traffic patterns

**Mitigation:**
- Regular patching and updates
- Web application firewalls (WAF)
- Network segmentation
- Least privilege access controls

**Related CWE:** CWE-1035 (2018 Top 10 A6:2017-Security Misconfiguration)
**Related CAPEC:** CAPEC-23 (File Content Injection), CAPEC-63 (Cross-Site Scripting)

**Procedure Examples:**
- **APT28:** Used CVE-2017-11882 to exploit Microsoft Office
- **APT41:** Exploited Citrix NetScaler/ADC, Cisco routers, and Zoho ManageEngine
- **Lazarus Group:** Exploited CVE-2019-0604 in SharePoint

### T1133: External Remote Services
**Entity Type:** TECHNIQUE
**Tactic:** Initial Access, Persistence
**Platform:** Windows, Linux, macOS

**Description:**
Remote services such as VPNs, Citrix, and other access mechanisms allow users to connect to internal enterprise network resources from external locations. Adversaries may use these services to gain initial access or persistence.

**Detection:**
- Monitor remote service authentication logs
- Detect unusual login patterns (time, location, frequency)
- Track failed authentication attempts
- Correlate with threat intelligence

**Mitigation:**
- Multi-factor authentication (MFA)
- Limit access to remote services
- Network segmentation
- Regular credential rotation

**Related CWE:** CWE-287 (Improper Authentication)
**Related CAPEC:** CAPEC-114 (Authentication Abuse)

**Procedure Examples:**
- **APT29:** Used compromised VPN credentials for initial access
- **FIN7:** Accessed victim networks through compromised RDP credentials
- **Wizard Spider:** Used stolen credentials to access VPN services

### T1189: Drive-by Compromise
**Entity Type:** TECHNIQUE
**Tactic:** Initial Access
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may gain access to a system through a user visiting a website over the normal course of browsing. The adversary's goal is to infect a legitimate website that may be visited by a specific community.

**Detection:**
- Web proxy logs analysis
- Browser security settings enforcement
- Network intrusion detection for exploit kits
- DNS monitoring for malicious domains

**Mitigation:**
- Browser hardening
- Application isolation and sandboxing
- Exploit protection
- Regular software updates

**Related CWE:** CWE-79 (Cross-site Scripting), CWE-94 (Code Injection)
**Related CAPEC:** CAPEC-63 (Cross-Site Scripting), CAPEC-242 (Code Injection)

**Procedure Examples:**
- **Darkhotel:** Used strategic web compromises against hotel WiFi networks
- **APT32:** Compromised high-profile Vietnamese websites
- **Turla:** Used watering hole attacks against government websites

### T1566: Phishing
**Entity Type:** TECHNIQUE
**Tactic:** Initial Access
**Platform:** Windows, macOS, Linux, Office 365, SaaS, Google Workspace

**Description:**
Adversaries may send phishing messages to gain access to victim systems. All forms of phishing are electronically delivered social engineering.

**Sub-techniques:**
- **T1566.001:** Spearphishing Attachment
- **T1566.002:** Spearphishing Link
- **T1566.003:** Spearphishing via Service

**Detection:**
- Email gateway analysis
- Anti-phishing tools
- User behavior analytics
- URL reputation checking
- File reputation analysis

**Mitigation:**
- Security awareness training
- Email authentication (SPF, DKIM, DMARC)
- Anti-spam and anti-malware filters
- Link and attachment sandboxing

**Related CWE:** CWE-1021 (Improper Restriction of Rendered UI Layers)
**Related CAPEC:** CAPEC-163 (Spear Phishing), CAPEC-98 (Phishing)

### T1566.001: Spearphishing Attachment
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1566
**Tactic:** Initial Access

**Description:**
Spearphishing with an attachment is a specific variant of spearphishing that uses malicious files attached to email. Adversaries may use this to gain initial access.

**File Types:**
- Microsoft Office documents with macros
- PDF files with exploits
- Archive files (ZIP, RAR) containing malware
- Executable files disguised as documents

**Procedure Examples:**
- **APT28:** Sent spearphishing emails with malicious attachments to targets
- **APT29:** Used spearphishing with COVID-19 themed lures
- **TA505:** Distributed Dridex banking trojan via malicious Excel documents

### T1566.002: Spearphishing Link
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1566
**Tactic:** Initial Access

**Description:**
Spearphishing with a link is a specific variant where adversaries include links in spearphishing emails to trick users into revealing information or downloading malware.

**Techniques:**
- Credential harvesting pages
- Drive-by download sites
- URL shorteners to obfuscate links
- Homograph attacks

**Procedure Examples:**
- **APT1:** Used spearphishing links to compromise targets
- **Magic Hound:** Sent emails with links to credential harvesting sites
- **TA542:** Distributed Emotet via phishing emails with malicious links

### T1566.003: Spearphishing via Service
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1566
**Tactic:** Initial Access

**Description:**
Adversaries may send spearphishing messages via third-party services to gain access. These services include social media, personal webmail, and other non-enterprise controlled services.

**Platforms:**
- LinkedIn messaging
- Twitter direct messages
- WhatsApp/Telegram
- Cloud collaboration tools (Slack, Teams)

**Procedure Examples:**
- **APT29:** Used Twitter direct messages for spearphishing
- **Lazarus Group:** Conducted spearphishing via LinkedIn
- **Kimsuky:** Used social media platforms for targeting

### T1091: Replication Through Removable Media
**Entity Type:** TECHNIQUE
**Tactic:** Initial Access, Lateral Movement
**Platform:** Windows

**Description:**
Adversaries may move onto systems by copying malware to removable media and taking advantage of Autorun features when the media is inserted into a system.

**Detection:**
- Monitor file creation on removable media
- Detect autorun.inf files
- Track USB device usage
- Monitor for suspicious executable files

**Mitigation:**
- Disable AutoRun/AutoPlay
- Block unauthorized USB devices
- Data loss prevention (DLP)
- Application whitelisting

**Related CWE:** CWE-274 (Improper Handling of Insufficient Privileges)
**Related CAPEC:** CAPEC-440 (Hardware Integrity Attack)

**Procedure Examples:**
- **Stuxnet:** Spread via USB drives using multiple zero-day exploits
- **Agent.btz:** Used removable drives to propagate through networks
- **Flame:** Replicated through USB drives in targeted environments

### T1195: Supply Chain Compromise
**Entity Type:** TECHNIQUE
**Tactic:** Initial Access
**Platform:** Windows, macOS, Linux

**Description:**
Adversaries may manipulate products or product delivery mechanisms prior to receipt by a final consumer for the purpose of data or system compromise.

**Sub-techniques:**
- **T1195.001:** Compromise Software Dependencies and Development Tools
- **T1195.002:** Compromise Software Supply Chain
- **T1195.003:** Compromise Hardware Supply Chain

**Detection:**
- Software composition analysis
- Binary analysis and verification
- Supply chain monitoring
- Code signing verification

**Mitigation:**
- Vulnerability scanning
- Update software regularly
- Audit supply chain
- Code signing requirements

**Related CWE:** CWE-494 (Download of Code Without Integrity Check)
**Related CAPEC:** CAPEC-437 (Supply Chain Attack), CAPEC-438 (Modification of Windows Service Configuration), CAPEC-439 (Manipulation of Opaque Client-based Data Tokens)

### T1199: Trusted Relationship
**Entity Type:** TECHNIQUE
**Tactic:** Initial Access
**Platform:** Windows, Linux, macOS, SaaS, Office 365, Google Workspace

**Description:**
Adversaries may breach or otherwise leverage organizations who have access to intended victims. Access through trusted third party relationship exploits an existing connection.

**Examples:**
- Managed service providers (MSPs)
- IT contractors
- Business partners
- Supply chain relationships

**Procedure Examples:**
- **APT29:** Compromised IT service provider to access downstream customers
- **CloudHopper:** Targeted MSPs to access their clients
- **NotPetya:** Spread through compromised accounting software update

**Related CWE:** CWE-923 (Improper Restriction of Communication Channel to Intended Endpoints)
**Related CAPEC:** CAPEC-437 (Supply Chain Attack)

### T1078: Valid Accounts
**Entity Type:** TECHNIQUE
**Tactic:** Initial Access, Persistence, Privilege Escalation, Defense Evasion
**Platform:** Windows, Linux, macOS, Network, Office 365, Azure AD, SaaS, Google Workspace

**Description:**
Adversaries may obtain and abuse credentials of existing accounts as a means of gaining Initial Access, Persistence, Privilege Escalation, or Defense Evasion.

**Sub-techniques:**
- **T1078.001:** Default Accounts
- **T1078.002:** Domain Accounts
- **T1078.003:** Local Accounts
- **T1078.004:** Cloud Accounts

**Detection:**
- Monitor account login behavior
- Correlate authentication logs
- Track unusual access patterns
- Implement user behavior analytics

**Mitigation:**
- Multi-factor authentication
- Privileged account management
- Password policies
- Account access reviews

**Related CWE:** CWE-798 (Use of Hard-coded Credentials), CWE-1188 (Initialization of a Resource with an Insecure Default)
**Related CAPEC:** CAPEC-70 (Try Common or Default Usernames and Passwords)

## Cross-References

### Relationship to Other Tactics
- **Persistence:** T1133, T1078
- **Privilege Escalation:** T1078
- **Defense Evasion:** T1078
- **Lateral Movement:** T1091

### ICS Considerations
Initial Access in ICS environments requires special attention:
- T1190 may target HMI interfaces
- T1133 may involve engineering workstation access
- T1199 may exploit vendor relationships
- Physical access concerns unique to operational technology

## Threat Actor Mapping
- **APT28:** T1190, T1133, T1566.001
- **APT29:** T1133, T1566.001, T1566.002, T1566.003, T1199
- **APT41:** T1190, T1078
- **Lazarus Group:** T1190, T1566.003
- **FIN7:** T1133, T1566.001

## Total Patterns in File: 250+
