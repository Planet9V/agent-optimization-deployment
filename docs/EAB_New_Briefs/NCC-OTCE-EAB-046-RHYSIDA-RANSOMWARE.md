# NCC-OTCE-EAB-046: Rhysida Ransomware Critical Infrastructure Campaign

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-046
**Date:** 2024-11-28
**Version:** 1.0
**Author:** NCC OTCE Research Team
**Campaign Period:** May 2023 - December 2024 (Active)

---

## EXECUTIVE SUMMARY

Rhysida ransomware represents a persistent and evolving threat to critical infrastructure sectors, operating as a Ransomware-as-a-Service (RaaS) model since May 2023. In December 2024, CISA, FBI, and MS-ISAC released an updated advisory warning that Rhysida continues to compromise healthcare, education, manufacturing, information technology, and government organizations through double extortion tactics. The group targets "opportunities" across multiple critical sectors rather than focusing on specific industries, making all critical infrastructure vulnerable.

**Threat Level:** HIGH
**Primary Motivation:** Financial Gain / Data Extortion
**Attribution:** Ransomware-as-a-Service Operators (Multiple Affiliates)
**Operational Model:** RaaS with Double Extortion

---

## THREAT ACTOR PROFILE

### Attribution & Background
- **Group Type:** Ransomware-as-a-Service (RaaS) operation
- **Active Since:** May 2023
- **Business Model:** Profit-sharing between operators and affiliates
- **Primary Objective:** Financial extortion through data encryption and exfiltration
- **Operational Pattern:** Opportunistic targeting across multiple sectors

### Target Sectors (U.S. Critical Infrastructure)
1. **Healthcare and Public Health** (Primary)
2. **Education Facilities** (Primary)
3. **Manufacturing** (Primary)
4. **Information Technology** (Primary)
5. **Government Facilities** (Secondary)
6. **Energy** (Opportunistic)
7. **Water/Wastewater** (Opportunistic)

### Geographic Targeting
- United States (Primary)
- Canada
- Europe
- Global opportunistic targeting

---

## CAMPAIGN ANALYSIS (2024 Activity)

### Recent Activity - December 2024 Update

The FBI, CISA, and MS-ISAC released updated indicators of compromise and TTPs identified through investigations as recently as **December 2024**, indicating continued active operations.

### Attack Pattern Evolution

**Opportunistic Targeting:**
Rhysida threat actors are known to impact "targets of opportunity," meaning they exploit any vulnerable organizations they encounter rather than conducting extensive pre-attack reconnaissance on specific high-value targets.

**Double Extortion Model:**
1. Initial compromise and network infiltration
2. Data exfiltration before encryption
3. Deployment of encryption ransomware
4. Ransom demand for decryption key
5. Threat to publish stolen data if payment not received
6. Publication of data on dark web leak sites

### Ransomware-as-a-Service Operations

**Affiliate Model:**
- Core Rhysida operators provide:
  - Ransomware platform and infrastructure
  - Payment negotiation support
  - Data leak site hosting
  - Technical support for affiliates

- Affiliates conduct:
  - Target identification and reconnaissance
  - Initial access operations
  - Network compromise and lateral movement
  - Data exfiltration and encryption
  - Victim negotiations

**Profit Sharing:**
Typical RaaS arrangements involve 70-80% of ransom payments to affiliates, with 20-30% to operators.

---

## TACTICS, TECHNIQUES, AND PROCEDURES (TTPs)

### Initial Access

**Phishing Campaigns:**
- Spear-phishing emails with malicious attachments
- Social engineering to obtain credentials
- Credential harvesting via fake login pages

**Vulnerable Internet-Facing Services:**
- Exploitation of known vulnerabilities in VPN concentrators
- Compromise of Remote Desktop Protocol (RDP) systems
- Targeting of unpatched web applications

**Valid Accounts:**
- Purchased credentials from dark web markets
- Stolen credentials from previous breaches
- Compromised accounts via brute force attacks

### Execution & Persistence

**Scripting and Automation:**
- PowerShell scripts for automated deployment
- Batch file execution for lateral movement
- Command-line interface exploitation

**Persistence Mechanisms:**
- Creation of new user accounts
- Registry modifications for auto-start
- Scheduled task creation
- Service installation

### Defense Evasion

**Evasion Techniques:**
- Disabling antivirus and security software
- Clearing Windows Event Logs
- Deleting shadow copies to prevent recovery
- Obfuscation of malicious scripts

### Discovery & Reconnaissance

**Network Mapping:**
- Active Directory enumeration
- Network share discovery
- System information gathering
- Process and service enumeration

### Lateral Movement

**Internal Propagation:**
- SMB/Windows Admin Shares
- Remote Desktop Protocol (RDP)
- PsExec and other remote execution tools
- Valid domain credentials

### Data Exfiltration

**Exfiltration Methods:**
- File upload to attacker-controlled cloud storage
- FTP/SFTP to external servers
- Use of legitimate file-sharing services
- Compression and staging before exfiltration

### Impact - Encryption & Extortion

**Ransomware Deployment:**
- Encryption of critical files and databases
- Ransom note delivery to all systems
- Demand for cryptocurrency payment (typically Bitcoin)
- Countdown timer for data publication threat

---

## MALWARE & TOOLS

### Rhysida Ransomware Binary

**Technical Characteristics:**
- File extension: `.rhysida`
- Encryption algorithm: Strong encryption (AES + RSA likely)
- Ransom note filename: typically `CriticalBreachDetected.pdf` or similar
- Language: Compiled binary, possible C/C++

### Attacker Toolset

**Common Tools Observed:**
- **Cobalt Strike:** Post-exploitation framework
- **Mimikatz:** Credential dumping
- **PsExec:** Remote execution
- **Rclone:** Cloud storage exfiltration
- **FileZilla/WinSCP:** FTP exfiltration
- **Advanced IP Scanner:** Network discovery
- **BloodHound:** Active Directory mapping

### Infrastructure

**Command & Control:**
- TOR-based C2 communication
- Encrypted communication channels
- Proxy servers to mask origin

**Data Leak Site:**
- Dark web portal for publishing victim data
- Countdown timers creating urgency
- Sample data releases to prove authenticity

---

## INDICATORS OF COMPROMISE (IoCs)

### File System Indicators

**Ransomware Artifacts:**
```
File Extensions: .rhysida
Ransom Notes: CriticalBreachDetected.pdf, HOW_TO_RESTORE.txt
Dropped Files: Various batch scripts, PowerShell scripts
Executable Names: Variable per campaign
```

### Network Indicators

**Command & Control Communication:**
```
Protocol: HTTPS, TOR
Domains: Rotating .onion addresses
IPs: Frequently changing, often behind VPNs/proxies
Ports: 443 (HTTPS), 9050 (TOR), various RDP ports (3389, custom)
```

**Data Exfiltration Patterns:**
```
Large outbound transfers to cloud storage services
SFTP/FTP connections to suspicious external IPs
Unusual outbound traffic volumes during off-hours
Connections to file-sharing services (Mega, Dropbox, etc.)
```

### Behavioral Indicators

**Pre-Encryption Activity:**
1. Mass deletion of Volume Shadow Copies (`vssadmin delete shadows`)
2. Disabling of Windows Defender (`Set-MpPreference -DisableRealtimeMonitoring $true`)
3. Clearing of Security Event Logs (`wevtutil cl Security`)
4. Creation of new administrative accounts
5. Unusual logons to multiple systems in short timeframes

**Encryption Phase:**
1. Simultaneous encryption across multiple systems
2. CPU/disk usage spikes across network
3. File modification timestamps changing en masse
4. Appearance of ransom notes on all systems

---

## IMPACT ASSESSMENT

### Critical Infrastructure Risk

**Healthcare Sector:**
- **SEVERITY:** CRITICAL
- Disruption of patient care and medical operations
- Compromise of sensitive patient health information (PHI)
- HIPAA violations and regulatory consequences
- Potential for patient safety impacts during service outages

**Education Sector:**
- Disruption of educational services and administration
- Compromise of student and employee records
- FERPA violations
- Research data loss
- Financial impact from operational downtime

**Manufacturing:**
- Production line disruptions
- Loss of intellectual property and trade secrets
- Supply chain impacts
- OT environment potential exposure
- Economic losses from downtime

**Government Services:**
- Disruption of public services
- Compromise of citizen data
- Loss of public trust
- National security implications (classified data)

### Economic Impact

**Direct Costs:**
- Ransom payments (ranging from $50K to millions)
- Incident response and forensics costs
- System restoration and recovery
- Legal and regulatory compliance costs
- Credit monitoring for affected individuals

**Indirect Costs:**
- Business disruption and lost productivity
- Reputation damage and loss of customer trust
- Regulatory fines and penalties
- Increased insurance premiums
- Long-term business impacts

---

## MITRE ATT&CK MAPPING

| Tactic | Technique ID | Technique Name |
|--------|--------------|----------------|
| Initial Access | T1566 | Phishing |
| Initial Access | T1078 | Valid Accounts |
| Initial Access | T1190 | Exploit Public-Facing Application |
| Execution | T1059.001 | PowerShell |
| Execution | T1059.003 | Windows Command Shell |
| Persistence | T1136 | Create Account |
| Persistence | T1053.005 | Scheduled Task |
| Defense Evasion | T1562.001 | Disable or Modify Tools |
| Defense Evasion | T1070.001 | Clear Windows Event Logs |
| Defense Evasion | T1490 | Inhibit System Recovery |
| Credential Access | T1003.001 | LSASS Memory |
| Credential Access | T1003.002 | Security Account Manager |
| Discovery | T1087.002 | Domain Account Discovery |
| Discovery | T1083 | File and Directory Discovery |
| Discovery | T1135 | Network Share Discovery |
| Lateral Movement | T1021.001 | Remote Desktop Protocol |
| Lateral Movement | T1021.002 | SMB/Windows Admin Shares |
| Collection | T1005 | Data from Local System |
| Exfiltration | T1048 | Exfiltration Over Alternative Protocol |
| Exfiltration | T1567 | Exfiltration Over Web Service |
| Impact | T1486 | Data Encrypted for Impact |
| Impact | T1490 | Inhibit System Recovery |

---

## DETECTION STRATEGIES

### Endpoint Detection

**1. Behavioral Analytics**
```
Alerts:
- Mass file modification across file shares
- Shadow copy deletion commands
- Security tool disablement attempts
- Unusual account creation
- Credential dumping tool execution
```

**2. PowerShell Monitoring**
```
Detection Rules:
- Enable Script Block Logging
- Monitor for encoded commands
- Detect cmdlets: Set-MpPreference, wevtutil, vssadmin
- Alert on suspicious PowerShell network activity
```

**3. EDR Rules**
```
High-Value Detections:
- Mimikatz execution patterns
- Cobalt Strike beacons
- Rapid propagation across endpoints
- Encryption-related process behavior
```

### Network Detection

**1. Traffic Analysis**
```
Monitor for:
- Large data exfiltration to external IPs/cloud services
- TOR traffic (port 9050, .onion domains)
- RDP brute force attempts
- Lateral movement patterns (SMB, RDP)
- Command & Control beaconing
```

**2. Perimeter Monitoring**
```
Alert Conditions:
- Outbound connections to known Rhysida infrastructure
- Unusual data upload volumes
- Encrypted traffic to suspicious destinations
- Multiple failed VPN authentication attempts
```

### Log Analysis

**1. Windows Event Logs**
```
Critical Event IDs:
- 4688: Process creation (command-line logging)
- 4624/4625: Account logon success/failure
- 4672: Special privileges assigned to new logon
- 4720: User account created
- 1102: Audit log cleared
- 7045: Service installed
```

**2. SIEM Correlation**
```
Multi-stage Detection:
Stage 1: Initial compromise indicators
Stage 2: Lateral movement and escalation
Stage 3: Data exfiltration
Stage 4: Pre-encryption preparation
Stage 5: Encryption deployment
```

---

## MITIGATION RECOMMENDATIONS

### Immediate Actions (24-48 Hours)

**1. Secure Remote Access**
- Require phishing-resistant multi-factor authentication (MFA)
- Implement conditional access policies
- Disable unnecessary RDP exposure
- Deploy VPN with strong authentication

**2. Backup Protection**
- Implement offline/air-gapped backups
- Test backup restoration procedures
- Use immutable backup storage
- Maintain 3-2-1 backup strategy

**3. Endpoint Hardening**
- Deploy EDR across all systems
- Enable PowerShell logging and monitoring
- Disable unnecessary services (SMBv1, LLMNR, NetBIOS)
- Implement application whitelisting

**4. Network Segmentation**
- Isolate critical systems
- Implement micro-segmentation
- Restrict lateral movement pathways
- Deploy zero-trust architecture principles

### Strategic Mitigations (30-90 Days)

**1. Security Architecture**
- Implement Secure-by-Design principles (CISA recommendation)
- Deploy defense-in-depth layered security
- Establish jump servers for administrative access
- Create privileged access workstations (PAWs)

**2. Detection & Response**
- Deploy SIEM with Rhysida-specific use cases
- Implement 24/7 SOC monitoring
- Develop ransomware incident response playbooks
- Conduct tabletop exercises

**3. Vulnerability Management**
- Establish continuous vulnerability scanning
- Prioritize patching of internet-facing systems
- Implement virtual patching for legacy systems
- Conduct regular penetration testing

**4. User Awareness**
- Mandatory security awareness training
- Phishing simulation campaigns
- Incident reporting procedures
- Social engineering awareness

**5. Privileged Account Management**
- Implement PAM solution
- Enforce least privilege access
- Regular credential rotation
- Monitor privileged account usage

---

## HUNTING GUIDANCE

### Hunt Hypothesis 1: Initial Access via Phishing
**Hypothesis:** Users have received and potentially opened malicious emails.
**Actions:**
- Review email gateway logs for suspicious attachments
- Check for emails with common ransomware lures
- Investigate user-reported phishing attempts
- Analyze web proxy logs for credential harvesting sites

**Detection Queries:**
```
Email logs: attachment_type IN [.zip, .rar, .exe, .js, .vbs] AND sender_domain NOT IN [trusted_domains]
Proxy logs: URL CONTAINS [credential, login, verify, account] AND domain_age < 30_days
```

### Hunt Hypothesis 2: Credential Compromise
**Hypothesis:** Attackers have obtained valid credentials.
**Actions:**
- Review authentication logs for unusual login patterns
- Check for accounts logging in from multiple IPs/geolocations
- Investigate failed login attempts (potential brute force)
- Review VPN access from unusual sources

**Investigation Steps:**
```
Auth logs: successful_login AND (login_hour NOT IN [business_hours] OR login_country NOT IN [expected_countries])
AD logs: account_lockouts > threshold OR password_resets > baseline
VPN logs: login_source_geo != user_typical_location
```

### Hunt Hypothesis 3: Lateral Movement Preparation
**Hypothesis:** Attackers are conducting reconnaissance and mapping the network.
**Actions:**
- Review network traffic for scanning activity
- Check for BloodHound or AD enumeration tools
- Investigate unusual SMB/RDP connections
- Analyze process creation logs for reconnaissance tools

**Hunt Queries:**
```
Network logs: port_scan_detected=true OR SMB_connections > baseline
Process logs: process_name IN [bloodhound, sharphound, adfind, nltest, net.exe]
EDR: suspicious_enumeration=true OR AD_query_volume > threshold
```

### Hunt Hypothesis 4: Pre-Encryption Activity
**Hypothesis:** Attackers are preparing for ransomware deployment.
**Actions:**
- Monitor for shadow copy deletion commands
- Check for security tool disablement attempts
- Review for unusual account creations
- Investigate file staging and compression activity

**Detection Logic:**
```
Command logs: command CONTAINS [vssadmin delete, bcdedit, wbadmin delete, wevtutil cl]
PowerShell: cmdlet IN [Set-MpPreference, Disable-WindowsOptionalFeature]
File system: archive_creation=true AND file_size > 1GB AND destination=external
```

---

## RECOVERY GUIDANCE

### Do NOT Pay Ransom

CISA, FBI, and MS-ISAC strongly discourage paying ransoms:
- No guarantee of data recovery
- Funds criminal operations
- May encourage future attacks
- Potential sanctions violations

### Recovery Steps

**1. Isolation**
- Immediately disconnect infected systems from network
- Disable wireless and wired connections
- Power off affected systems if encryption in progress

**2. Assessment**
- Identify patient zero and infection vector
- Determine scope of compromise
- Assess data exfiltration extent
- Document all findings for legal/regulatory purposes

**3. Eradication**
- Remove attacker access and persistence mechanisms
- Reset all credentials (assume all compromised)
- Rebuild affected systems from clean images
- Patch all vulnerabilities exploited

**4. Restoration**
- Restore from clean, verified backups
- Validate data integrity before restoration
- Restore critical systems first
- Test functionality before returning to production

**5. Reporting**
- File reports with FBI, CISA, and local law enforcement
- Notify affected individuals (regulatory requirement)
- Coordinate with cyber insurance providers
- Document lessons learned

---

## INTELLIGENCE GAPS

1. Complete infrastructure mapping of Rhysida operators
2. Identification of all affiliate groups operating under Rhysida RaaS
3. Payment wallet tracking and cryptocurrency laundering methods
4. Full technical analysis of latest ransomware variants
5. Decryption capabilities or potential master key recovery
6. Attribution to specific nation-state or criminal organizations
7. Coordination with other ransomware groups

---

## REFERENCES

1. [CISA Advisory AA23-319A: Rhysida Ransomware (Updated December 2024)](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-319a)
2. [FBI, CISA, MS-ISAC Joint Advisory on Rhysida Ransomware](https://www.cisa.gov/news-events/alerts/2023/11/15/cisa-fbi-and-ms-isac-release-advisory-rhysida-ransomware)
3. [Trend Micro: Ransomware Spotlight - Rhysida](https://www.trendmicro.com/vinfo/us/security/news/ransomware-spotlight/ransomware-spotlight-rhysida)
4. [Industrial Cyber: FBI, CISA Release Advisory on Rhysida Ransomware Targeting Critical Sectors](https://industrialcyber.co/cisa/fbi-cisa-ms-isac-release-cybersecurity-advisory-on-emerging-rhysida-ransomware-targeting-critical-sectors/)
5. [Barracuda: Rhysida Ransomware Analysis](https://blog.barracuda.com/2024/05/09/rhysida-ransomware--the-creepy-crawling-criminal-hiding-in-the-d)

---

## CHANGE LOG

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-28 | Initial report creation | NCC OTCE Research Team |

---

**Distribution:** TLP:CLEAR - May be distributed without restriction
**Next Review Date:** 2025-02-28
**Contact:** otce-research@ncc.example.com
**Confidence Assessment:** HIGH - Based on official CISA/FBI advisory (AA23-319A updated December 2024)

---
*End of Report*
