# NCC-OTCE-EAB-021: Volt Typhoon APT Campaign

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-021
**Date:** 2024-11-28
**Version:** 1.0
**Author:** NCC OTCE Research Team
**Campaign Period:** Ongoing (5+ years) - Active Sept-Nov 2024

---

## EXECUTIVE SUMMARY

Volt Typhoon is a Chinese state-sponsored Advanced Persistent Threat (APT) group conducting long-term pre-positioning operations against U.S. critical infrastructure with the goal of enabling disruptive cyber-physical attacks. The group has maintained persistent access to victim IT environments for at least five years, demonstrating exceptional operational security and patience characteristic of nation-state actors preparing for potential conflict scenarios.

**Threat Level:** CRITICAL
**Primary Motivation:** Pre-positioning for Disruptive/Destructive Operations
**Attribution:** People's Republic of China (PRC)
**Operational Security:** Exceptionally High

---

## THREAT ACTOR PROFILE

### Attribution & Background
- **Nation-State Sponsor:** People's Republic of China
- **Active Since:** At least 2019 (5+ year dwell time observed)
- **Primary Objective:** Pre-positioning for potential disruptive attacks on critical infrastructure
- **Operational Focus:** Enabling lateral movement from IT to OT systems

### Target Sectors (U.S. Critical Infrastructure)
1. **Communications** (Primary)
2. **Energy** (Primary)
3. **Transportation Systems** (Primary)
4. **Water and Wastewater Systems** (Primary)
5. **Government Facilities**
6. **Critical Manufacturing**

### Geographic Targeting
- United States (Primary focus)
- U.S. territorial possessions
- Allied nations (Five Eyes intelligence sharing partners)

---

## CAMPAIGN ANALYSIS (2024 Activity)

### Campaign Overview
Volt Typhoon actors have compromised IT environments of multiple critical infrastructure organizations and are pre-positioning themselves on IT networks to enable lateral movement to OT assets. The ultimate goal is to disrupt critical infrastructure functions during potential geopolitical conflicts.

### 2024 Warnings and Advisories
- **March 19, 2024:** Five Eyes intelligence partners issue joint warning
- **February 2024:** U.S. government releases detailed advisory with IOCs
- **Ongoing:** Active compromises detected across multiple critical sectors

### Dwell Time
U.S. authoring agencies have observed indications of Volt Typhoon actors maintaining access and footholds within some victim IT environments for **at least five years**, demonstrating unprecedented patience and operational security.

---

## TACTICS, TECHNIQUES, AND PROCEDURES (TTPs)

### Living Off the Land (LOTL) Approach
Volt Typhoon's hallmark technique is extensive use of living-off-the-land (LOTL) methods, avoiding malware artifacts that would trigger security alerts. This approach allows the group to blend in with normal system administration activities.

### Pre-Compromise Reconnaissance
**Extensive OSINT and Network Mapping:**
- Learn target organization's network architecture
- Understand operational protocols
- Identify network topologies
- Map security measures
- Document typical user behaviors
- Identify key network and IT staff

### Initial Access
**Compromised Credentials:**
- Exploitation of valid accounts
- Credential harvesting from initial footholds
- No malware deployment in initial stages

**SOHO Router Infrastructure:**
- Compromise of small office/home office (SOHO) routers
- Repurpose compromised routers as backdoors into larger networks
- Use router infrastructure to remain undetected

### Persistence
**Long-Term Access Maintenance:**
- Maintain footholds for 5+ years
- Minimal operational activity to avoid detection
- Regular credential dumping at intervals
- Targeted log deletion to conceal actions

### Operational Security
**Timing and Behavior:**
- Abstain from using compromised credentials outside normal working hours
- Avoid triggering security alerts on abnormal account activities
- Targeted log deletion to conceal presence
- Silent network behavior following credential dumping

### Discovery
**Post-Credential Dumping:**
- Extensive discovery activities
- Environment mapping and enumeration
- No immediate data exfiltration
- Preparation for future disruptive operations

### Lateral Movement Strategy
**IT-to-OT Targeting:**
- Establish presence in IT environments
- Map pathways to OT systems
- Position for potential disruptive attacks on operational technology
- Target systems controlling physical processes

---

## MALWARE & TOOLS

### Living Off the Land Tools
Volt Typhoon primarily uses legitimate system administration tools:
- Windows built-in utilities
- PowerShell for scripting
- WMI for remote execution
- Native network tools
- Credential dumping tools (using LSASS, SAM, NTDS.dit)

### Infrastructure
**Compromised SOHO Routers:**
- Multiple router manufacturers targeted
- Routers repurposed as C2 infrastructure
- Provides operational anonymity
- Difficult attribution and detection

### Minimal Malware Footprint
Unlike traditional APT groups, Volt Typhoon avoids custom malware deployment in favor of LOTL techniques, making detection significantly more challenging.

---

## INDICATORS OF COMPROMISE (IoCs)

### Windows Event Logs - ESENT Application Logs
**Critical Event IDs to Monitor:**
- **Event ID 216:** Indicates potential NTDS.dit copying
- **Event ID 325:** Database operations
- **Event ID 326:** Database file operations
- **Event ID 327:** Database recovery operations

### Behavioral Indicators
1. **Credential Dumping at Regular Intervals**
   - Periodic access to LSASS memory
   - NTDS.dit file access
   - SAM registry hive access

2. **Silent Network Behavior**
   - No data exfiltration observed
   - Minimal network communications
   - Discovery activity without data theft

3. **Abnormal Account Usage**
   - Account activity outside normal hours (when operational security lapses)
   - Unusual authentication patterns
   - Lateral movement using valid credentials

4. **Log Manipulation**
   - Security log clearing
   - Targeted event log deletion
   - Audit policy modifications

### Network Indicators
- Connections to compromised SOHO routers
- Unusual RDP or SSH sessions
- Lateral movement patterns using Windows Admin Shares
- WMI or PowerShell remote execution

---

## IMPACT ASSESSMENT

### Critical Infrastructure at Risk
- **SEVERITY:** CRITICAL
- Potential for widespread disruption to essential services
- Risk of cyber-physical attacks on OT/ICS systems
- Capability to disrupt communications, energy, water, and transportation

### Pre-Positioning for Conflict
The primary concern is that Volt Typhoon is preparing the battlefield for potential future conflicts, positioning to:
- Disrupt critical services during geopolitical tensions
- Cause physical damage through OT system manipulation
- Create chaos and confusion during military operations
- Degrade U.S. response capabilities in conflict scenarios

### Long-Term Strategic Threat
Five-year dwell time indicates:
- Patience and strategic planning
- Investment in long-term operations
- Potential for deeply embedded access
- Difficulty in complete remediation

---

## MITRE ATT&CK MAPPING

| Tactic | Technique ID | Technique Name |
|--------|--------------|----------------|
| Reconnaissance | T1595 | Active Scanning |
| Resource Development | T1584 | Compromise Infrastructure (SOHO Routers) |
| Initial Access | T1078 | Valid Accounts |
| Execution | T1059.001 | PowerShell |
| Execution | T1047 | Windows Management Instrumentation |
| Persistence | T1078 | Valid Accounts |
| Defense Evasion | T1070.001 | Indicator Removal: Clear Windows Event Logs |
| Defense Evasion | T1070.006 | Indicator Removal: Timestomp |
| Credential Access | T1003.001 | OS Credential Dumping: LSASS Memory |
| Credential Access | T1003.002 | OS Credential Dumping: Security Account Manager |
| Credential Access | T1003.003 | OS Credential Dumping: NTDS |
| Discovery | T1087 | Account Discovery |
| Discovery | T1018 | Remote System Discovery |
| Discovery | T1082 | System Information Discovery |
| Lateral Movement | T1021.001 | Remote Services: Remote Desktop Protocol |
| Lateral Movement | T1021.002 | Remote Services: SMB/Windows Admin Shares |

---

## DETECTION STRATEGIES

### Log Analysis
1. **ESENT Application Logs**
   - Monitor Event IDs 216, 325, 326, 327
   - Alert on NTDS.dit access patterns
   - Track database file operations

2. **Security Event Logs**
   - Monitor Event ID 4624 (Account Logon)
   - Track Event ID 4672 (Special Privileges Assigned)
   - Alert on Event ID 1102 (Audit Log Cleared)

3. **PowerShell Logging**
   - Enable Script Block Logging
   - Monitor for encoded commands
   - Track PowerShell remoting sessions

### Behavioral Analytics
1. **Credential Usage Patterns**
   - Baseline normal account behavior
   - Detect usage outside typical hours
   - Alert on unusual authentication patterns

2. **Lateral Movement Detection**
   - Monitor Windows Admin Share access
   - Track RDP sessions
   - Detect unusual WMI execution

3. **LOTL Technique Detection**
   - Baseline legitimate admin tool usage
   - Detect abnormal built-in utility execution
   - Monitor for credential dumping tool execution

### Network Monitoring
1. **SOHO Router Communications**
   - Identify connections to known compromised routers
   - Monitor for unusual outbound connections
   - Track C2 communication patterns

2. **Internal Network Traffic**
   - Detect abnormal lateral movement
   - Monitor IT-to-OT network crossings
   - Alert on unusual protocol usage

---

## MITIGATION RECOMMENDATIONS

### Immediate Actions
1. **Credential Security**
   - Implement password rotation for all privileged accounts
   - Deploy multi-factor authentication (MFA) universally
   - Use hardware security keys for critical systems
   - Implement Privileged Access Management (PAM)

2. **Network Segmentation**
   - Isolate IT and OT networks
   - Implement zero-trust architecture
   - Deploy jump servers for administrative access
   - Restrict lateral movement pathways

3. **Enhanced Monitoring**
   - Enable comprehensive logging on all systems
   - Deploy EDR across all endpoints
   - Implement SIEM with Volt Typhoon-specific detection rules
   - Monitor ESENT and Security event logs continuously

4. **SOHO Router Security**
   - Inventory all remote access points
   - Replace or harden SOHO routers
   - Implement VPN solutions for remote access
   - Monitor for compromised router infrastructure

### Strategic Mitigations
1. **Assume Breach Mentality**
   - Conduct comprehensive threat hunting
   - Perform forensic analysis of critical systems
   - Review historical logs for compromise indicators
   - Plan for long-term remediation efforts

2. **IT/OT Protection**
   - Implement robust IT/OT segmentation
   - Deploy OT-specific security controls
   - Monitor IT-to-OT crossover points
   - Conduct OT security assessments

3. **Incident Response Preparation**
   - Develop critical infrastructure IR playbooks
   - Conduct tabletop exercises for cyber-physical attacks
   - Establish government coordination procedures
   - Prepare for long-term incident response

4. **Supply Chain Security**
   - Vet all remote access solutions
   - Secure SOHO and remote infrastructure
   - Implement vendor risk management
   - Monitor third-party access

---

## HUNTING GUIDANCE

### Hunt Hypothesis 1: Long-Term Persistent Access
**Hypothesis:** Volt Typhoon may have maintained access for extended periods.
**Actions:**
- Review authentication logs for accounts with long-term consistent access
- Analyze patterns of credential usage over months/years
- Identify accounts with unusual longevity or persistence
- Check for dormant accounts that periodically activate

### Hunt Hypothesis 2: Credential Dumping
**Hypothesis:** Actors have dumped credentials at regular intervals.
**Actions:**
- Review ESENT logs for Event IDs 216, 325, 326, 327
- Check for LSASS memory access patterns
- Audit NTDS.dit file access
- Review SAM registry hive access logs

### Hunt Hypothesis 3: LOTL Technique Usage
**Hypothesis:** Living-off-the-land tools are being used for malicious purposes.
**Actions:**
- Baseline legitimate administrative tool usage
- Identify outlier PowerShell, WMI, and built-in tool execution
- Check for encoded PowerShell commands
- Review process execution chains for suspicious patterns

### Hunt Hypothesis 4: IT-to-OT Lateral Movement Preparation
**Hypothesis:** Actors are mapping pathways from IT to OT systems.
**Actions:**
- Monitor network traffic crossing IT/OT boundaries
- Review access attempts to OT management systems
- Check for reconnaissance of industrial control systems
- Analyze authentication to HMI, SCADA, and PLC systems

---

## INTELLIGENCE GAPS

1. Full inventory of compromised organizations unknown
2. Extent of OT system reconnaissance unclear
3. Trigger conditions for activation of disruptive capabilities unknown
4. Complete toolset and malware capabilities may not be fully documented
5. Coordination with other PRC APT groups requires further analysis

---

## REFERENCES

1. [CISA Advisory AA24-038A - PRC State-Sponsored Actors Compromise U.S. Critical Infrastructure](https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a)
2. [Microsoft Security Blog - Volt Typhoon Living-Off-the-Land Techniques](https://www.microsoft.com/en-us/security/blog/2023/05/24/volt-typhoon-targets-us-critical-infrastructure-with-living-off-the-land-techniques/)
3. [Palo Alto Unit 42 - Volt Typhoon Threat Brief](https://unit42.paloaltonetworks.com/volt-typhoon-threat-brief/)
4. [U.S. Department of Defense - PRC Compromise of US Critical Infrastructure](https://media.defense.gov/2024/Feb/07/2003389935/-1/-1/0/CSA-PRC-Compromise-US-Critical-Infrastructure.PDF)
5. [CISA - Joint Fact Sheet for Leaders on Volt Typhoon](https://www.cisa.gov/news-events/alerts/2024/03/19/cisa-and-partners-release-joint-fact-sheet-leaders-prc-sponsored-volt-typhoon-cyber-activity)
6. [Picus Security - Volt Typhoon Living Off the Land](https://www.picussecurity.com/resource/blog/volt-typhoon-living-off-the-land-cyber-espionage)

---

## CHANGE LOG

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-28 | Initial report creation | NCC OTCE Research Team |

---

**Distribution:** TLP:CLEAR - May be distributed without restriction
**Next Review Date:** 2025-02-28
**Contact:** otce-research@ncc.example.com

---
*End of Report*
