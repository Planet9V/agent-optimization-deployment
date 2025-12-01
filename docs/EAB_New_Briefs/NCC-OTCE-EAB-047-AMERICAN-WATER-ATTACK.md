# NCC-OTCE-EAB-047: American Water Cyberattack - Water Infrastructure Targeting

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-047
**Date:** 2024-11-28
**Version:** 1.0
**Author:** NCC OTCE Research Team
**Campaign Period:** October 2024

---

## EXECUTIVE SUMMARY

On October 3, 2024, American Water Works Company—the largest regulated water and wastewater utility in the United States—detected unauthorized access to its computer networks, leading to a significant cybersecurity incident. The attack forced the company to take critical systems offline, disrupting billing operations while protecting water and wastewater services. This incident highlights the escalating cyber threats against water sector critical infrastructure and the urgent need for enhanced cybersecurity measures across utilities serving millions of Americans.

**Threat Level:** HIGH
**Primary Motivation:** Financial (Suspected Ransomware) / Data Theft
**Attribution:** Unknown (Under Investigation)
**Affected Population:** 14+ million customers across 14 states

---

## THREAT ACTOR PROFILE

### Attribution & Background
- **Attribution Confidence:** LOW (No public attribution as of November 2024)
- **Attack Discovery Date:** October 3, 2024
- **Public Disclosure:** October 8, 2024
- **Investigation Status:** Ongoing with FBI and third-party cybersecurity experts
- **Ransom Claim:** No ransomware group publicly claimed responsibility

### Target Profile

**American Water Works Company:**
- Largest regulated U.S. water and wastewater utility
- Serves more than 14 million people
- Operations in 14 states and 18 military installations
- 2024 Revenue: ~$4.3 billion
- Critical infrastructure designation under Presidential Policy Directive 21

### Potential Threat Actor Categories

**Scenario 1: Ransomware Group (Most Likely)**
- Typical targeting of large enterprises with revenue capacity
- Disruption of billing systems consistent with ransomware impact
- No immediate claim could indicate negotiation phase
- Attack timing (early October) aligns with ransomware campaign patterns

**Scenario 2: Nation-State Actor**
- Water infrastructure as critical national asset
- Pre-positioning for future disruptive operations
- Reconnaissance and network mapping
- Geopolitical tensions targeting U.S. critical infrastructure

**Scenario 3: Hacktivist Group**
- Ideological targeting of privatized water utilities
- Environmental activism motivation
- Public awareness campaigns
- Lower sophistication but opportunistic

---

## INCIDENT ANALYSIS

### Timeline of Events

**October 3, 2024 (Detection):**
- American Water discovers unauthorized computer access
- Incident response protocols activated
- Third-party cybersecurity experts engaged
- Law enforcement notification initiated

**October 3-7, 2024 (Response):**
- Protective system disconnections implemented
- MyWater customer portal taken offline
- Billing systems suspended
- Customer service impacts begin

**October 8, 2024 (Public Disclosure):**
- Company files 8-K form with SEC
- Public statement released to customers
- Media coverage begins
- Industry alerts issued

**October 10, 2024:**
- No attribution publicly identified
- Systems remain offline for security
- Investigation continues

**Mid-October 2024 (Recovery):**
- Systems gradually reconnected after security validation
- MyWater portal restoration begins
- Billing operations resume with delays

### Attack Impact Analysis

**Compromised Systems:**
- Corporate IT networks (confirmed)
- Customer billing systems (confirmed)
- MyWater online customer portal (taken offline)
- Extent of operational technology (OT) access unknown

**Protected Systems:**
- Water treatment and distribution (NO IMPACT - confirmed by company)
- Wastewater collection and treatment (NO IMPACT - confirmed)
- SCADA and industrial control systems (no public evidence of compromise)
- Physical safety systems maintained operations

**Operational Impacts:**
- Billing system disruption (weeks of delay)
- Customer portal unavailability
- Customer service delays
- Payment processing interruptions
- Credit reporting impact (late payment concerns)

**Financial Impact:**
- Direct incident response costs: $Millions (estimated)
- Third-party forensics and legal costs
- System restoration expenses
- Potential customer compensation
- Regulatory compliance costs
- Long-term cybersecurity investment requirements

---

## TACTICS, TECHNIQUES, AND PROCEDURES (TTPs)

**CRITICAL NOTE:** Specific TTPs have NOT been publicly disclosed. The following represents common attack vectors for water sector compromises based on industry patterns and CISA guidance.

### Likely Initial Access Vectors

**1. Phishing (High Probability)**
- Spear-phishing targeting employees with privileged access
- Malicious attachments or links
- Credential harvesting campaigns
- Business email compromise (BEC)

**2. Vulnerable Remote Access (Medium-High Probability)**
- Exploitation of VPN vulnerabilities
- Compromised Remote Desktop Protocol (RDP)
- Weak or stolen authentication credentials
- Lack of multi-factor authentication (MFA)

**3. Supply Chain Compromise (Medium Probability)**
- Third-party vendor access exploitation
- Managed service provider (MSP) compromise
- Software supply chain attack
- Contractor system compromise

**4. Exploitation of Public-Facing Applications (Low-Medium Probability)**
- Web application vulnerabilities
- Unpatched software systems
- SQL injection or similar web attacks
- API exploitation

### Suspected Attack Progression

**Stage 1: Initial Compromise**
- Credential theft or phishing success
- Establishment of initial foothold
- Reconnaissance and environment mapping

**Stage 2: Lateral Movement**
- Privilege escalation
- Internal network propagation
- Active Directory compromise
- Access to sensitive systems

**Stage 3: Data Access (Suspected)**
- Customer data exfiltration likely
- Billing system data access confirmed
- Employee information potential target
- Corporate financial data at risk

**Stage 4: Impact Delivery**
- System disruption (billing systems)
- Potential ransomware deployment (unconfirmed)
- Protective disconnections by company
- Service continuity prioritization

---

## MALWARE & TOOLS

**PUBLIC DISCLOSURE:** No specific malware samples, IoCs, or tool details have been publicly released.

**Potential Tool Categories (Based on Typical Water Sector Attacks):**

**Ransomware Families (If Applicable):**
- LockBit
- BlackCat/ALPHV
- Royal
- Akira
- BlackBasta

**Post-Exploitation Frameworks:**
- Cobalt Strike
- Metasploit
- Empire
- Sliver

**Credential Theft:**
- Mimikatz
- LaZagne
- ProcDump

**Network Tools:**
- Advanced IP Scanner
- Angry IP Scanner
- Port scanning utilities

---

## INDICATORS OF COMPROMISE (IoCs)

**CRITICAL LIMITATION:** American Water and investigating agencies have NOT released specific IoCs.

**General Detection Indicators for Water Sector:**

### Network Anomalies to Monitor

```
Unusual Authentication Patterns:
- Off-hours VPN connections
- Geographic anomalies in access
- Multiple failed login attempts
- Unusual account privilege escalations

Suspicious Network Traffic:
- Large data exfiltration to external IPs
- Connections to known malicious infrastructure
- Encrypted traffic to unusual destinations
- Internal lateral movement patterns

System Behavior:
- Unexpected system reboots
- Service disruptions without cause
- Unusual process executions
- Backup system access anomalies
```

---

## IMPACT ASSESSMENT

### Water Sector Implications

**Severity: CRITICAL for U.S. Water Infrastructure**

**1. Industry-Wide Vulnerability Exposure**
- American Water as largest U.S. utility creates precedent
- Demonstrates attackers view water sector as viable target
- Other water utilities lack cybersecurity resources
- 70% increase in water sector attacks (2023-2024)

**2. Customer Data at Risk**
- 14+ million customers potentially affected
- Personal information in billing systems
- Payment card data if stored
- Account credentials for customer portals
- Regulatory notification requirements (state breach laws)

**3. Operational Technology (OT) Threat**
- While water services continued, OT systems remain at risk
- IT/OT convergence creates pathways
- SCADA systems potential future targets
- Public health implications if treatment disrupted

**4. Economic Impact**
- Direct costs: Incident response, forensics, legal
- Indirect costs: Customer trust, regulatory scrutiny
- Insurance premium increases
- Cybersecurity investment requirements

### Broader Critical Infrastructure Impact

**Water Sector Targeting Trend:**
According to CISA, pro-Russia hacktivists have increasingly targeted industrial control systems (ICS) within water utilities, often exploiting:
- Default passwords
- Unsecured remote access points
- Weak cyber hygiene practices
- Lack of network segmentation

**Statistical Context:**
- 70% increase in water utility cyberattacks (2024 vs 2023)
- Water sector often lacks dedicated IT/cybersecurity staff
- Many small utilities have limited cybersecurity budgets
- Legacy SCADA systems with minimal security features

---

## MITRE ATT&CK MAPPING

**NOTE:** Specific techniques used in American Water attack not publicly disclosed. The following represents common water sector attack patterns.

| Tactic | Technique ID | Technique Name | Likelihood |
|--------|--------------|----------------|------------|
| Initial Access | T1566 | Phishing | High |
| Initial Access | T1078 | Valid Accounts | High |
| Initial Access | T1190 | Exploit Public-Facing Application | Medium |
| Execution | T1059 | Command and Scripting Interpreter | High |
| Persistence | T1136 | Create Account | Medium |
| Privilege Escalation | T1078 | Valid Accounts | High |
| Defense Evasion | T1562 | Impair Defenses | Medium |
| Credential Access | T1003 | OS Credential Dumping | High |
| Discovery | T1087 | Account Discovery | High |
| Discovery | T1083 | File and Directory Discovery | High |
| Lateral Movement | T1021 | Remote Services | High |
| Collection | T1005 | Data from Local System | High |
| Exfiltration | T1041 | Exfiltration Over C2 Channel | Medium |
| Impact | T1486 | Data Encrypted for Impact | Medium |
| Impact | T1499 | Endpoint Denial of Service | Low |

---

## DETECTION STRATEGIES

### For Water Utilities (General Guidance)

**1. Network Monitoring**
```
Critical Detections:
- Monitor all VPN/remote access for anomalies
- Baseline normal IT/OT network traffic
- Alert on IT-to-OT network crossings
- Detect unusual data exfiltration patterns
- Flag connections to known malicious IPs
```

**2. Endpoint Detection & Response (EDR)**
```
Key Alerts:
- Unusual process executions
- Credential dumping tool signatures
- Lateral movement indicators
- Privilege escalation attempts
- Suspicious PowerShell or command-line activity
```

**3. Authentication & Access**
```
Monitoring Focus:
- Failed login attempt spikes
- Successful logins from unusual locations
- Off-hours administrative access
- Unusual service account activity
- MFA bypass attempts
```

**4. OT/SCADA Monitoring**
```
Critical Alerts:
- Unauthorized access to HMI/SCADA
- Unexpected configuration changes
- Unusual command sequences to PLCs/RTUs
- IT network scanning of OT segments
- Firmware modification attempts
```

---

## MITIGATION RECOMMENDATIONS

### Immediate Actions for Water Utilities (Based on CISA Guidance)

**1. Secure Remote Access (CRITICAL - 24 Hours)**
- Enable multi-factor authentication (MFA) on ALL remote access
- Review and restrict VPN access to essential personnel only
- Change all VPN and remote access credentials
- Disable unnecessary remote access methods
- Implement IP whitelisting where possible

**2. Network Segmentation (HIGH PRIORITY - 48-72 Hours)**
- Isolate IT and OT networks with industrial firewalls
- Deploy data diodes or unidirectional gateways
- Restrict IT-to-OT communications to specific authorized paths
- Segment SCADA systems from corporate networks
- Create DMZ for external-facing services

**3. Access Control & Credential Management (CRITICAL - 1 Week)**
- Implement principle of least privilege
- Disable default accounts and passwords
- Deploy Privileged Access Management (PAM) solution
- Enforce strong password policies (15+ characters)
- Regular credential audits and rotations

**4. Backup & Recovery (CRITICAL - Ongoing)**
- Implement offline, immutable backups
- Test backup restoration procedures monthly
- Maintain separate backup credentials
- Store backups physically separate from network
- Document recovery procedures for OT systems

### Strategic Mitigations (30-90 Days)

**1. Security Operations**
- Deploy SIEM with water sector-specific use cases
- Establish 24/7 monitoring or managed security services
- Implement EDR across all IT endpoints
- Deploy OT-specific intrusion detection (Claroty, Nozomi, Dragos)
- Create incident response playbook for water utilities

**2. Vulnerability Management**
- Conduct comprehensive vulnerability assessments
- Prioritize patching of internet-facing systems
- Implement virtual patching for legacy OT systems
- Regular penetration testing (quarterly for critical systems)
- Supplier security assessments

**3. Security Architecture (IEC 62443)**
- Implement defense-in-depth layering
- Deploy industrial firewalls with deep packet inspection
- Create secure zones for OT environments
- Establish jump boxes for OT access
- Implement network access control (NAC)

**4. Personnel & Training**
- Mandatory cybersecurity awareness training
- Phishing simulation campaigns
- Tabletop exercises for cyber incidents
- Cross-training for manual operations during cyber events
- Incident reporting procedures and culture

**5. Regulatory Compliance**
- Ensure AWIA compliance (America's Water Infrastructure Act)
- Follow CISA water sector cybersecurity guidance
- Participate in WaterISAC information sharing
- Review state-specific cybersecurity requirements
- Develop required risk and resilience assessments

---

## HUNTING GUIDANCE

### Hunt Hypothesis 1: Compromised Remote Access
**Hypothesis:** Attackers may have gained access via VPN or remote access tools.
**Actions:**
- Review all VPN authentication logs for past 90 days
- Identify logins from unusual geographic locations
- Check for off-hours access by administrative accounts
- Investigate failed login patterns (potential brute force)

**Hunt Queries:**
```
VPN Logs: (auth_success=true AND (login_time NOT IN [business_hours] OR src_country NOT IN [USA]))
Auth Logs: failed_attempts > 10 in 1 hour
VPN Logs: session_duration > 8 hours OR concurrent_sessions > 1
```

### Hunt Hypothesis 2: Internal Reconnaissance
**Hypothesis:** Attackers conducted network discovery and enumeration.
**Actions:**
- Review network traffic for scanning activity
- Check for Active Directory enumeration tools
- Investigate SMB and file share access patterns
- Analyze DNS queries for unusual patterns

**Detection Logic:**
```
Network Logs: port_scan=true OR connection_attempts > 100/minute
Process Logs: process_name IN [nltest, net.exe, dsquery, ldapsearch]
File Access: mass_enumeration=true AND account NOT IN [backup_accounts]
```

### Hunt Hypothesis 3: Data Exfiltration
**Hypothesis:** Customer or corporate data was exfiltrated.
**Actions:**
- Analyze network traffic for large outbound transfers
- Check for connections to cloud storage services
- Review file access logs for sensitive data
- Investigate compression and staging activities

**Investigation Steps:**
```
NetFlow: outbound_bytes > 10GB AND dst NOT IN [known_partners]
Proxy Logs: URL CONTAINS [dropbox, mega, wetransfer, pastebin]
File System: archive_created=true AND file_size > 1GB
```

### Hunt Hypothesis 4: Persistence Mechanisms
**Hypothesis:** Attackers established persistent access for future operations.
**Actions:**
- Review scheduled tasks for unusual entries
- Check for new user account creations
- Investigate service installations
- Examine startup locations and registry modifications

**Hunt Queries:**
```
Event ID 4698: Scheduled task created
Event ID 4720: User account created
Event ID 7045: Service installed
Registry: modifications in Run, RunOnce keys
```

---

## LESSONS LEARNED & RECOMMENDATIONS

### Industry Takeaways

**1. Water Sector is a Target**
- American Water attack demonstrates attackers view water utilities as viable, profitable targets
- No utility is "too small" or "not a target"
- Cyber insurance may become mandatory and expensive

**2. IT/OT Segmentation is Critical**
- American Water's ability to protect water services while addressing IT compromise demonstrates value of segmentation
- Without proper segmentation, attack could have impacted treatment operations
- Legacy integration projects must prioritize security architecture

**3. Incident Response Readiness**
- American Water's rapid activation of IR protocols limited impact
- Tabletop exercises and playbooks are essential
- Third-party IR retainers accelerate response

**4. Transparency and Communication**
- Timely public disclosure maintains customer trust
- Regulatory compliance requires breach notifications
- Industry information sharing benefits all water utilities

---

## RESOURCES FOR WATER UTILITIES

### CISA Water Sector Resources
1. [WaterISAC - Water Information Sharing and Analysis Center](https://www.waterisac.org)
2. [CISA Water and Wastewater Sector Cybersecurity Resources](https://www.cisa.gov/topics/critical-infrastructure-security-and-resilience/critical-infrastructure-sectors/water-and-wastewater-systems-sector)
3. [CISA ICS Alert: Threat Actors Continue to Exploit OT/ICS Through Unsophisticated Means](https://www.cisa.gov/news-events/alerts/2024/09/25/threat-actors-continue-exploit-otics-through-unsophisticated-means)

### Regulatory Frameworks
1. **America's Water Infrastructure Act (AWIA) 2018**
   - Requires risk and resilience assessments
   - Emergency response plan requirements
   - Cybersecurity considerations mandatory

2. **NIST Cybersecurity Framework**
   - Identify, Protect, Detect, Respond, Recover
   - Tailored for water utilities

3. **IEC 62443 (Industrial Automation and Control Systems Security)**
   - OT security zones and conduits
   - Defense-in-depth implementation

---

## INTELLIGENCE GAPS

1. Specific threat actor identification and attribution
2. Initial access vector and compromise methodology
3. Extent of data exfiltration (customer records, corporate data)
4. Whether ransomware was deployed or threatened
5. Ransom demand amount if applicable
6. Full timeline of attacker presence in network
7. Specific vulnerabilities exploited
8. Tools and malware used in attack
9. Potential OT system reconnaissance or access attempts
10. Coordination with other water utility targeting campaigns

**Note:** American Water has not released detailed technical information, likely due to ongoing investigation and legal considerations. Updates expected as investigation concludes.

---

## REFERENCES

1. [CNBC: America's Largest Water Utility Hit by Cyberattack](https://www.cnbc.com/2024/10/08/american-water-largest-us-water-utility-cyberattack.html)
2. [TechTarget: The American Water Cyberattack - Explaining How It Happened](https://www.techtarget.com/whatis/feature/The-American-Water-cyberattack-Explaining-how-it-happened)
3. [WaterISAC: Incident Awareness - Major Water Utility Experiences Cyber Attack (Updated October 15, 2024)](https://www.waterisac.org/incident-awareness-major-water-utility-experiences-cyber-attack-update-october-15-2024)
4. [Infosecurity Magazine: American Water Hit by Cyber-Attack, Billing Systems Disrupted](https://www.infosecurity-magazine.com/news/american-water-cyberattack-billing/)
5. [Dark Reading: American Water Suffers Network Disruptions After Cyberattack](https://www.darkreading.com/cyberattacks-data-breaches/american-water-network-disruptions-cyberattack)
6. [Smart Water Magazine: Water Sector Cybersecurity in 2024 - High Stakes and Urgent Responses](https://smartwatermagazine.com/news/smart-water-magazine/water-sector-cybersecurity-2024-high-stakes-and-urgent-responses)
7. [CISA: Threat Actors Continue to Exploit OT/ICS Through Unsophisticated Means (Sept 25, 2024)](https://www.cisa.gov/news-events/alerts/2024/09/25/threat-actors-continue-exploit-otics-through-unsophisticated-means)

---

## CHANGE LOG

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-28 | Initial report creation | NCC OTCE Research Team |

---

**Distribution:** TLP:CLEAR - May be distributed without restriction
**Next Review Date:** 2025-01-28 (Updated as investigation details emerge)
**Contact:** otce-research@ncc.example.com
**Confidence Assessment:** MEDIUM - Limited public technical details; assessment based on company statements, industry analysis, and water sector attack patterns

---
*End of Report*
