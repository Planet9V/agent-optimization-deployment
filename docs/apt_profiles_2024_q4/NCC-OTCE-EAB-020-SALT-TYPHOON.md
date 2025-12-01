# NCC-OTCE-EAB-020: Salt Typhoon APT Campaign

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-020
**Date:** 2024-11-28
**Version:** 1.0
**Author:** NCC OTCE Research Team
**Campaign Period:** September 2024 - November 2024

---

## EXECUTIVE SUMMARY

Salt Typhoon is a Chinese state-sponsored threat actor active since 2019, conducting a sophisticated global campaign in 2024 targeting telecommunications service providers and critical infrastructure. The group successfully breached major U.S. broadband providers including Verizon, AT&T, and Lumen Technologies, potentially exposing sensitive communications data from federal wiretapping systems.

**Threat Level:** CRITICAL
**Primary Motivation:** Cyber Espionage / Intelligence Collection
**Attribution:** People's Republic of China (PRC)
**Also Known As:** OPERATOR PANDA, RedMike, UNC5807, GhostEmperor, FamousSparrow, Earth Estries, UNC2286

---

## THREAT ACTOR PROFILE

### Attribution & Background
- **Nation-State Sponsor:** People's Republic of China
- **Active Since:** 2019
- **Primary Objective:** Information theft and long-term espionage
- **Operational Scope:** Global, with primary focus on United States, Southeast Asia, and various African countries

### Target Sectors
1. **Telecommunications** (Primary)
2. **Critical Infrastructure**
3. **Government Communications
4. **Broadband Service Providers**

### Geographic Targeting
- United States (Primary)
- Southeast Asia
- African nations
- Global telecommunications infrastructure

---

## CAMPAIGN ANALYSIS (Sept-Nov 2024)

### Campaign Overview
In September 2024, a two-year cyber-espionage campaign by Salt Typhoon was publicly disclosed. The campaign utilized custom-developed malware and sophisticated persistence mechanisms to maintain long-term access to telecommunications infrastructure.

### Attack Timeline
- **2022:** Initial infiltration of telecommunications providers begins
- **September 2024:** Campaign publicly disclosed
- **October-November 2024:** Continued persistent access observed

### High-Profile Victims
- Verizon Communications
- AT&T
- Lumen Technologies
- Multiple Southeast Asian telecommunications providers

---

## TACTICS, TECHNIQUES, AND PROCEDURES (TTPs)

### Initial Access
**T1190 - Exploit Public-Facing Application**
- Exploitation of vulnerabilities in VPNs, firewalls, and exchange servers
- N-day vulnerability exploitation in public-facing endpoints
- Spear-phishing emails delivering malware payloads

### Persistence
**T1542 - Pre-OS Boot**
- Exploitation of network device firmware vulnerabilities
- Use of implants and backdoors in firmware
- GhostSpider custom backdoor for persistent access

### Credential Access
**T1552.001 - Brute Force: Password Cracking**
- Collection and exfiltration of configuration files via FTP/TFTP
- SNMP Read/Write community string extraction
- Configuration files containing easily crackable credentials

**T1040 - Network Sniffing**
- Network traffic capture of SNMP, TACACS, and RADIUS traffic
- Credential harvesting from unencrypted protocols

### Defense Evasion
**T1562.004 - Impair Defenses: Disable or Modify System Firewall**
- Assignment of new IP addresses to loopback interfaces on compromised switches
- Use of modified interfaces for SSH connections to other systems

### Lateral Movement
**T1021.004 - Remote Services: SSH**
- SSH connections using compromised credentials
- Lateral movement through network devices

**T1078.003 - Valid Accounts: Local Accounts**
- Use of compromised local credentials
- Exploitation of CVE-2018-0171 on Cisco routers

### Collection
**T1530 - Data from Configuration Repository: Network Device Configuration Dump**
- Systematic collection of network device configurations
- Extraction of SNMP community strings

**T1590.001 - Gather Victim Network Information: Network Topology**
- Comprehensive network mapping from configuration files
- Named interface information gathering

### Execution
**T1059.001 - Command and Scripting Interpreter: PowerShell**
- Base64 encoded PowerShell scripts
- Remote command execution via PowerShell

**T1059.005 - Command and Scripting Interpreter: Visual Basic**
- Visual Basic script execution for malware deployment

**T1106 - Native API**
- CreateProcessA Windows API calls
- Native API abuse for execution

### Exfiltration
**T1048.003 - Exfiltration Over Alternative Protocol: Exfiltration Over Unencrypted Non-C2 Protocol**
- Data exfiltration via FTP and TFTP protocols
- Use of unencrypted protocols to avoid detection

---

## MALWARE & TOOLS

### Custom Malware
1. **GhostSpider**
   - Custom-developed backdoor
   - Enables persistent system access
   - Supports long-term espionage operations
   - Multi-platform support

2. **JumbledPath**
   - Custom malware variant for packet capture
   - Remote packet capture via attacker-selected jump-host
   - Network traffic interception capabilities

### Exploited Vulnerabilities
1. **CVE-2024-21887** - Ivanti Connect Secure and Policy Secure command injection
2. **CVE-2023-46805** - Ivanti authentication bypass (chained with CVE-2024-21887)
3. **CVE-2024-3400** - Palo Alto Networks PAN-OS GlobalProtect RCE
4. **CVE-2023-20273** - Cisco IOS XE command injection/privilege escalation
5. **CVE-2023-20198** - Cisco IOS XE authentication bypass
6. **CVE-2021-26855** - Microsoft Exchange ProxyLogon
7. **CVE-2018-0171** - Cisco router vulnerabilities

---

## INDICATORS OF COMPROMISE (IoCs)

### Network Indicators
- FTP/TFTP exfiltration traffic patterns
- SSH connections from unusual loopback IP addresses
- SNMP, TACACS, RADIUS traffic anomalies
- Connections to compromised jump-hosts

### File Indicators
- GhostSpider backdoor signatures
- JumbledPath malware variants
- Modified configuration files
- Base64 encoded PowerShell scripts

### Behavioral Indicators
- Unusual firmware modifications
- Configuration file dumps at regular intervals
- Network device configuration changes
- New loopback interface IP assignments

---

## IMPACT ASSESSMENT

### Critical Infrastructure Impact
- **SEVERITY:** CRITICAL
- Potential exposure of federal wiretapping systems
- Compromise of telecommunications infrastructure
- Long-term persistent access to communications networks

### Data Exposure
- Sensitive communications data
- Federal law enforcement wiretapping information
- Network topology and architecture
- Credentials and configuration data

### Operational Impact
- Multi-year compromise requiring complete infrastructure review
- Potential compromise of national security communications
- Trust degradation in telecommunications security

---

## MITRE ATT&CK MAPPING

| Tactic | Technique ID | Technique Name |
|--------|--------------|----------------|
| Initial Access | T1190 | Exploit Public-Facing Application |
| Persistence | T1542 | Pre-OS Boot |
| Credential Access | T1552.001 | Brute Force: Password Cracking |
| Credential Access | T1040 | Network Sniffing |
| Defense Evasion | T1562.004 | Impair Defenses: Disable or Modify System Firewall |
| Lateral Movement | T1021.004 | Remote Services: SSH |
| Lateral Movement | T1078.003 | Valid Accounts: Local Accounts |
| Collection | T1530 | Data from Configuration Repository |
| Collection | T1590.001 | Gather Victim Network Information |
| Execution | T1059.001 | Command and Scripting Interpreter: PowerShell |
| Execution | T1059.005 | Command and Scripting Interpreter: Visual Basic |
| Execution | T1106 | Native API |
| Exfiltration | T1048.003 | Exfiltration Over Alternative Protocol |

---

## DETECTION STRATEGIES

### Network-Based Detection
- Monitor for unusual FTP/TFTP exfiltration patterns
- Detect configuration file access and transfer
- Alert on firmware modification attempts
- Track SSH connections from loopback interfaces
- Monitor SNMP, TACACS, RADIUS traffic for credential harvesting

### Host-Based Detection
- Monitor firmware integrity
- Detect unauthorized loopback IP assignments
- Alert on configuration file dumps
- Track PowerShell execution with encoding patterns
- Monitor for Native API abuse

### Behavioral Analytics
- Baseline network device access patterns
- Detect anomalous configuration changes
- Monitor for extended dwell time indicators
- Track lateral movement from network devices

---

## MITIGATION RECOMMENDATIONS

### Immediate Actions
1. **Patch Critical Vulnerabilities**
   - Prioritize CVE-2024-21887, CVE-2024-3400, CVE-2023-20273, CVE-2023-20198
   - Apply vendor security updates for network devices
   - Update Ivanti, Palo Alto, Cisco, and Microsoft Exchange systems

2. **Credential Security**
   - Rotate all SNMP community strings
   - Change TACACS and RADIUS credentials
   - Implement encrypted credential storage
   - Disable insecure protocols (FTP, TFTP, Telnet)

3. **Network Segmentation**
   - Isolate network management traffic
   - Implement strict firewall rules for SSH access
   - Segment telecommunications infrastructure

### Strategic Mitigations
1. **Zero Trust Architecture**
   - Implement least-privilege access controls
   - Require multi-factor authentication
   - Continuous verification of network devices

2. **Enhanced Monitoring**
   - Deploy advanced EDR solutions
   - Implement network traffic analysis (NTA)
   - Enable comprehensive logging on all network devices
   - Deploy SIEM with Salt Typhoon-specific detection rules

3. **Firmware Security**
   - Implement firmware integrity checking
   - Maintain firmware update schedules
   - Use cryptographically signed firmware
   - Monitor for unauthorized firmware modifications

4. **Incident Response Preparation**
   - Develop telecommunications-specific IR playbooks
   - Conduct tabletop exercises for APT scenarios
   - Establish vendor security incident contacts
   - Prepare forensic capabilities for network devices

---

## HUNTING GUIDANCE

### Hunt Hypothesis 1: Firmware Persistence
**Hypothesis:** Salt Typhoon may have installed firmware-level persistence on network devices.
**Actions:**
- Compare current firmware hashes against known-good versions
- Review firmware update logs for unauthorized changes
- Check for unusual boot sequences or startup configurations

### Hunt Hypothesis 2: Configuration Exfiltration
**Hypothesis:** Configuration files containing credentials have been exfiltrated.
**Actions:**
- Review FTP/TFTP logs for unusual outbound transfers
- Check for configuration file access outside maintenance windows
- Analyze network flows for configuration data patterns

### Hunt Hypothesis 3: Credential Compromise
**Hypothesis:** SNMP, TACACS, and RADIUS credentials have been compromised.
**Actions:**
- Audit all network device credential usage
- Review authentication logs for unusual patterns
- Check for protocol downgrade attacks
- Verify encrypted protocol enforcement

---

## INTELLIGENCE GAPS

1. Full extent of compromised telecommunications providers unknown
2. Complete GhostSpider malware capability assessment needed
3. Additional exploited zero-day vulnerabilities may exist
4. Attribution to specific PRC intelligence unit requires confirmation
5. Full scope of data exfiltration unknown

---

## REFERENCES

1. [Picus Security - Salt Typhoon Telecommunications Threat](https://www.picussecurity.com/resource/blog/salt-typhoon-telecommunications-threat)
2. [CISA Advisory AA25-239A - Countering Chinese State-Sponsored Actors](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-239a)
3. [Eclypsium - Holding Back Salt Typhoon](https://eclypsium.com/blog/salt-typhoon/)
4. [SOCRadar - Dark Web Profile: Salt Typhoon](https://socradar.io/dark-web-profile-salt-typhoon/)
5. [Tenable - Salt Typhoon Vulnerability Analysis](https://www.tenable.com/blog/salt-typhoon-an-analysis-of-vulnerabilities-exploited-by-this-state-sponsored-actor)
6. [AttackIQ - Emulating Salt Typhoon](https://www.attackiq.com/2025/03/19/emulating-salt-typhoon/)
7. [HackTheBox - Inside Salt Typhoon](https://www.hackthebox.com/blog/salt-typhoon-apt-us-telecom-espionage-attack-analysis)

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
