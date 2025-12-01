# APT Activity Summary Report: Q4 2024

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-000-SUMMARY
**Date:** 2024-11-28
**Version:** 1.0
**Author:** NCC OTCE Research Team
**Reporting Period:** September 2024 - November 2024

---

## EXECUTIVE SUMMARY

This comprehensive report analyzes recent Advanced Persistent Threat (APT) activity from September through November 2024, documenting 11 major threat campaigns targeting critical infrastructure, with particular focus on telecommunications, energy, water systems, and healthcare sectors. The research reveals an alarming escalation in nation-state cyber operations and ransomware campaigns with potential cyber-physical impacts.

**Key Findings:**
- 11 documented APT campaigns with critical infrastructure focus
- 4 nation-state actors (China, Russia, Iran, North Korea) conducting coordinated operations
- 5 ransomware groups causing $300+ million in damages
- 32% increase in ransomware activity compared to Q3 2024
- Telecommunications sector most heavily targeted (56% of campaigns)

---

## THREAT LANDSCAPE OVERVIEW

### Nation-State Activity

#### People's Republic of China (PRC)
**Threat Actors:** Salt Typhoon, Volt Typhoon, Mustang Panda
**Primary Objectives:** Long-term espionage, pre-positioning for disruptive operations
**Target Focus:** Telecommunications, critical infrastructure, Southeast Asian governments

**Key Highlights:**
- **Salt Typhoon** compromised major U.S. telecommunications providers (Verizon, AT&T, Lumen)
- **Volt Typhoon** maintained 5+ year persistent access to U.S. critical infrastructure
- Pre-positioning for potential cyber-physical attacks on communications, energy, and transportation

#### Russian Federation
**Threat Actors:** Sandworm (APT44), APT29 (Midnight Blizzard)
**Primary Objectives:** Destructive operations against Ukraine, intelligence collection
**Target Focus:** Ukrainian critical infrastructure, global government entities

**Key Highlights:**
- **Sandworm** deployed ZEROLOT wiper against Ukrainian energy and grain sectors
- **APT29** launched novel RDP-based spear-phishing campaign targeting 100+ organizations
- Continued cyber warfare operations supporting military objectives

#### Islamic Republic of Iran
**Threat Actors:** CyberAv3ngers, APT34
**Primary Objectives:** Disruptive attacks on critical infrastructure
**Target Focus:** Water/wastewater systems, fuel management, Middle East government networks

**Key Highlights:**
- **CyberAv3ngers** deployed IOCONTROL malware against U.S. and Israeli water systems
- $10 million bounty offered for information on IRGC-CEC officials
- Caused 2-day water supply disruption in Ireland

#### Democratic People's Republic of Korea (DPRK)
**Threat Actors:** Lazarus Group, Kimsuky, Jumpy Pisces (Andariel)
**Primary Objectives:** Financial theft, intelligence collection
**Target Focus:** Cryptocurrency sector, government agencies, ransomware collaboration

**Key Highlights:**
- **Lazarus Group** conducted $659 million in cryptocurrency heists in 2024
- **Kimsuky** exploited DMARC weaknesses for government espionage
- **Jumpy Pisces** first-ever collaboration with Play ransomware operation

---

## RANSOMWARE THREAT ANALYSIS

### Financial Impact
- **Total Estimated Ransoms Paid:** $300+ million across documented campaigns
- **Most Profitable:** Akira ($244M), Qilin ($50M+), FIN7 (substantial unreported amounts)
- **32% Activity Increase:** Compared to Q3 2024

### Critical Infrastructure Impact

#### Qilin Ransomware
- **Major Attack:** UK Synnovis healthcare (June 2024)
- **Ransom Demand:** $50 million
- **Impact:** Disrupted London hospitals, canceled surgeries/transplants, 900K data breach
- **Total Costs:** £33 million ($44 million)

#### Akira Ransomware
- **Q3 2024 Status:** Most-detected ransomware variant in U.S.
- **November 2024:** 73 victims in single month
- **New Capability:** First Nutanix AHV VM encryption
- **Primary Targets:** Manufacturing, education, healthcare

#### FIN7 Evolution
- **Infrastructure:** 4000+ shell domains for phishing
- **New Tools:** AvNeutralizer (EDR bypass), automated SQL injection
- **RaaS Links:** REvil, Conti, DarkSide, BlackMatter, Cl0p
- **Targets:** Financial services, retail, hospitality, energy

---

## CRITICAL INFRASTRUCTURE TARGETING ANALYSIS

### Telecommunications (Highest Priority)
**Campaigns:** Salt Typhoon, Active campaigns in 10 of 18 observed (56%)
**Impact:**
- Compromise of U.S. federal wiretapping systems
- Long-term persistent access to communications infrastructure
- Potential exposure of sensitive government communications

**TTPs:**
- Exploitation of edge/perimeter network vulnerabilities
- N-day vulnerability exploitation (CVE-2024-21887, CVE-2024-3400, CVE-2023-20273)
- Custom malware (GhostSpider, JumbledPath)
- Firmware-level persistence

### Energy Sector
**Campaigns:** Volt Typhoon (pre-positioning), Sandworm (active destruction)
**Impact:**
- 5-year persistent access enabling IT-to-OT lateral movement
- Destructive wiper attacks on Ukrainian energy companies
- Preparation for potential disruptive cyber-physical attacks

**TTPs:**
- Living-off-the-land (LOTL) techniques
- Group Policy Object (GPO) abuse for wiper deployment
- Multi-layered data destruction
- Targeting of supervisory control systems

### Water and Wastewater Systems
**Campaigns:** CyberAv3ngers IOCONTROL
**Impact:**
- 2-day water supply cutoff (Ireland)
- Pennsylvania water utility compromise
- Public health and safety threats

**TTPs:**
- IOCONTROL malware targeting PLCs, HMIs, SCADA
- MQTT protocol abuse for C2 communications
- Cloudflare DNS over HTTPS for evasion
- Multi-manufacturer device targeting (Unitronics, Orpak, Baicells, Red Lion)

### Healthcare
**Campaigns:** Qilin, Akira
**Impact:**
- 15+ incidents since October 2022
- Disrupted patient care, canceled surgeries
- 900K+ patient records compromised
- Blood supply disruptions

**TTPs:**
- Double extortion (encryption + data leak)
- Exploitation of Fortinet vulnerabilities
- Targeting of backup systems
- Public shaming via data leak sites

---

## TACTICAL TRENDS AND EVOLVING TECHNIQUES

### Novel Attack Vectors (2024)

1. **RDP Configuration Files (APT29)**
   - Signed .rdp files in spear-phishing
   - Bidirectional resource mapping to attacker infrastructure
   - Access to hard disks, clipboard, peripherals, authentication

2. **DMARC Exploitation (Kimsuky)**
   - Abuse of weak email security policies
   - Domain spoofing for trusted entity impersonation
   - Targeting of government and think tanks

3. **Social Engineering via GitHub (Lazarus)**
   - Malicious npm dependencies in legitimate-appearing repos
   - Multi-month recruiter impersonation campaigns
   - WhatsApp platform migration for trust building

4. **Screensaver File Delivery (Mustang Panda)**
   - .SCR file extensions replacing typical ZIP/RAR/ISO
   - Targeting of ASEAN summit participants
   - ToneShell backdoor deployment

### Persistent Techniques

1. **Living Off the Land (Volt Typhoon)**
   - 5+ year dwell time with minimal malware footprint
   - Use of legitimate admin tools
   - Avoidance of security alert triggers

2. **Firmware-Level Persistence**
   - Pre-OS boot exploitation (T1542)
   - Network device firmware compromise
   - Survival across device reboots and reimaging

3. **Group Policy Abuse (Sandworm)**
   - PowerGPOAbuse and TANKTRAP utilities
   - Network-wide simultaneous wiper deployment
   - Scheduled task staging for timing control

4. **Modular Malware Platforms (IOCONTROL)**
   - Multi-device, multi-manufacturer compatibility
   - MQTT protocol for legitimate traffic blending
   - IoT/OT-specific targeting capabilities

---

## MITRE ATT&CK TECHNIQUE HEATMAP

### Most Frequently Observed Techniques

| Technique ID | Technique Name | Frequency | Threat Actors |
|--------------|----------------|-----------|---------------|
| T1190 | Exploit Public-Facing Application | 8/11 | Salt Typhoon, Volt Typhoon, CyberAv3ngers, Qilin, Akira, APT34 |
| T1566.001 | Phishing: Spearphishing Attachment | 7/11 | APT29, Kimsuky, Lazarus, Mustang Panda, FIN7, Sandworm |
| T1485 | Data Destruction | 4/11 | Sandworm, CyberAv3ngers, Qilin, Akira |
| T1486 | Data Encrypted for Impact | 4/11 | Qilin, Akira, FIN7, Sandworm |
| T1542 | Pre-OS Boot / Firmware | 3/11 | Salt Typhoon, Volt Typhoon, CyberAv3ngers |
| T1059.001 | PowerShell | 5/11 | Salt Typhoon, Sandworm, multiple |
| T1003 | OS Credential Dumping | 6/11 | Volt Typhoon, Salt Typhoon, Qilin, Akira, FIN7 |
| T1078 | Valid Accounts | 6/11 | Volt Typhoon, APT34, multiple |

### Emerging Technique Trends

- **T1572 - Protocol Tunneling:** Increased use (Ngrok by Akira, MQTT by CyberAv3ngers)
- **T1562.001 - Disable or Modify Tools:** EDR bypass evolution (FIN7 AvNeutralizer)
- **T1484 - Domain Policy Modification:** GPO abuse becoming standard (Sandworm)
- **T1140 - Deobfuscate/Decode:** DNS over HTTPS for C2 evasion (IOCONTROL)

---

## INDICATORS OF COMPROMISE (IoCs) SUMMARY

### Network Indicators

**C2 Infrastructure Patterns:**
- MQTT broker connections (IOCONTROL)
- DNS over HTTPS to Cloudflare (IOCONTROL)
- Ngrok tunneling services (Akira)
- FTP/TFTP exfiltration (Salt Typhoon)
- Tor-based C2 (Qilin, Akira)

**Exfiltration Indicators:**
- 86.104.74[.]51:1224 (Lazarus)
- /pdown/ URL path patterns (Lazarus)
- Large pre-encryption data transfers (Qilin, Akira)
- Configuration file dumps via FTP/TFTP (Salt Typhoon)

### Exploited Vulnerabilities

**Critical CVEs (Most Widely Exploited):**
1. **CVE-2024-21887** - Ivanti Connect Secure command injection (Salt Typhoon)
2. **CVE-2024-3400** - Palo Alto Networks GlobalProtect RCE (Salt Typhoon)
3. **CVE-2023-20273** - Cisco IOS XE command injection (Salt Typhoon)
4. **CVE-2023-20198** - Cisco IOS XE authentication bypass (Salt Typhoon)
5. **CVE-2024-30088** - Windows Kernel privilege escalation (APT34)
6. **CVE-2024-40766** - Nutanix AHV vulnerability (Akira)

**Fortinet Vulnerabilities:**
- Critical CVEs exploited by Qilin ransomware
- VPN credential compromise vectors

### Malware Families

**Custom Nation-State Malware:**
- GhostSpider (Salt Typhoon) - Telecommunications backdoor
- JumbledPath (Salt Typhoon) - Packet capture tool
- IOCONTROL (CyberAv3ngers) - IoT/OT cyberweapon
- ZEROLOT (Sandworm) - Destructive wiper
- STING (Sandworm) - Secondary wiper variant

**Financial Crime Malware:**
- BeaverTail (Lazarus) - Initial reconnaissance
- InvisibleFerret (Lazarus) - Advanced backdoor
- GolangGhost (Lazarus) - Go-based backdoor
- AkdoorTea (Lazarus) - Undocumented backdoor

**Ransomware Families:**
- Qilin/Agenda - Healthcare targeting
- Akira - Manufacturing/education focus
- Play - First North Korean state collaboration

**Tools and Utilities:**
- AvNeutralizer/AuKill (FIN7) - EDR bypass
- PowerGPOAbuse (Sandworm) - GPO exploitation
- TANKTRAP (Sandworm) - GPO utility
- ToneShell (Mustang Panda) - Backdoor
- StarProxy (Mustang Panda) - Lateral movement

---

## DETECTION AND HUNTING STRATEGIES

### Priority Detection Capabilities

1. **Firmware Integrity Monitoring**
   - Continuous firmware hash verification
   - Boot sector modification detection
   - Network device configuration baselines

2. **Living-Off-the-Land Detection**
   - PowerShell script block logging
   - WMI execution monitoring
   - Native API abuse detection
   - Built-in utility usage baselines

3. **Credential Monitoring**
   - ESENT Event IDs (216, 325, 326, 327)
   - LSASS memory access
   - NTDS.dit file operations
   - SAM registry hive access

4. **OT/ICS-Specific Detection**
   - MQTT protocol anomaly detection
   - DNS over HTTPS from industrial devices
   - PLC/HMI configuration change monitoring
   - Modbus, DNP3 protocol inspection

5. **Email Security**
   - DMARC policy enforcement
   - SPF/DKIM validation
   - .rdp attachment blocking
   - GitHub repository link analysis in emails

### Hunting Hypotheses

**H1: Long-Term Persistent Access (Volt Typhoon Pattern)**
- Review 5+ year authentication logs
- Identify accounts with consistent long-term access
- Check for dormant accounts with periodic activation
- Analyze credential dumping at regular intervals

**H2: Firmware-Level Compromise**
- Compare firmware hashes against known-good versions
- Review firmware update logs for unauthorized changes
- Check unusual boot sequences
- Validate network device configurations

**H3: IT-to-OT Lateral Movement**
- Monitor network traffic crossing IT/OT boundaries
- Review access attempts to OT management systems
- Check for reconnaissance of SCADA/ICS systems
- Analyze authentication to HMI and PLC systems

**H4: IOCONTROL Malware Presence**
- Scan for MQTT broker connections from IoT/OT devices
- Check for Cloudflare DoH usage from industrial systems
- Review device configuration changes
- Analyze for command patterns in network traffic

**H5: Ransomware Pre-Positioning**
- Detect shadow copy deletion attempts
- Monitor backup system access
- Track service termination patterns
- Identify unusual scheduled task creation

---

## STRATEGIC MITIGATION RECOMMENDATIONS

### Immediate Actions (0-30 Days)

1. **Critical Vulnerability Patching**
   - Prioritize CVE-2024-21887, CVE-2024-3400, CVE-2023-20273, CVE-2023-20198
   - Patch Fortinet, Cisco, Palo Alto, Nutanix, Ivanti systems
   - Apply Windows Kernel updates (CVE-2024-30088)

2. **Email Security Hardening**
   - Set DMARC to "quarantine" or "reject"
   - Implement SPF and DKIM
   - Block .rdp attachments at gateway
   - Deploy advanced email filtering

3. **Credential Security**
   - Rotate all privileged account passwords
   - Implement MFA universally
   - Deploy hardware security keys for critical systems
   - Change all SNMP community strings
   - Update TACACS/RADIUS credentials

4. **Network Segmentation**
   - Isolate IT and OT networks immediately
   - Implement jump boxes for administrative access
   - Remove IoT/OT devices from direct Internet exposure
   - Deploy industrial firewalls

5. **Backup Protection**
   - Create offline, immutable backups
   - Geographic distribution of backups
   - Regular backup testing
   - Separate backup network segment

### Strategic Mitigations (30-90 Days)

1. **Zero Trust Architecture**
   - Implement least-privilege access controls
   - Continuous device and user verification
   - Micro-segmentation of networks
   - Application-level access controls

2. **Enhanced Monitoring and Detection**
   - Deploy EDR across all endpoints
   - Implement OT-specific security solutions
   - SIEM with APT-specific detection rules
   - Network traffic analysis (NTA) for industrial protocols
   - Firmware integrity checking

3. **Incident Response Preparation**
   - Develop sector-specific IR playbooks
   - Conduct tabletop exercises for APT scenarios
   - Establish government coordination channels (CISA, FBI, sector ISACs)
   - Prepare backup operational procedures for OT systems

4. **Security Operations Enhancement**
   - Establish 24/7 SOC capability
   - Deploy threat hunting teams
   - Implement automated threat intelligence integration
   - Conduct purple team exercises

### Long-Term Strategic Initiatives (90+ Days)

1. **Architecture Redesign**
   - Full IT/OT network separation
   - Software-defined perimeter implementation
   - Cloud security posture management
   - Supply chain security program

2. **Advanced Capabilities**
   - Deception technology deployment
   - AI/ML-based threat detection
   - Automated incident response
   - Threat intelligence platform integration

3. **Organizational Resilience**
   - Business continuity planning for cyber events
   - Cyber insurance evaluation
   - Board-level cybersecurity reporting
   - Third-party risk management program

4. **Industry Collaboration**
   - Sector ISAC participation
   - Threat intelligence sharing
   - Joint exercises with peers
   - Government partnership programs

---

## INTELLIGENCE GAPS AND FUTURE RESEARCH

### Critical Unknowns

1. **Full Scope of Compromises**
   - Complete victim inventory for Salt Typhoon and Volt Typhoon unknown
   - Total number of water systems compromised by CyberAv3ngers unclear
   - Extent of data exfiltration from telecommunications providers

2. **Attribution Uncertainties**
   - Specific PRC intelligence units for Salt Typhoon/Volt Typhoon
   - Jumpy Pisces-Play ransomware relationship (affiliate vs. IAB)
   - Coordination between Iranian APT groups
   - FIN7 ties to specific nation-state actors

3. **Technical Capabilities**
   - Complete GhostSpider malware functionality
   - Full IOCONTROL payload capabilities
   - Additional zero-days in APT arsenals
   - Undisclosed malware families

4. **Strategic Intent**
   - Trigger conditions for Volt Typhoon activation
   - Coordination between Chinese APT groups
   - Future target selection methodology
   - Pre-positioning vs. active exploitation timelines

### Recommended Research Priorities

1. **Telecommunications Security**
   - Comprehensive telecommunications infrastructure assessment
   - Identification of additional compromised providers
   - Analysis of federal wiretapping system exposure

2. **OT/ICS Threat Analysis**
   - Expanded IOCONTROL malware analysis
   - Assessment of additional targeted OT device manufacturers
   - Evaluation of cyber-physical attack capabilities

3. **Ransomware Evolution**
   - Nation-state and ransomware convergence patterns
   - Analysis of RaaS affiliate relationships
   - Economic impact assessment methodology

4. **Detection Gap Analysis**
   - Evaluation of LOTL technique detection effectiveness
   - Firmware-level persistence detection capabilities
   - IT-to-OT lateral movement visibility

---

## SECTOR-SPECIFIC RECOMMENDATIONS

### Telecommunications
**Priority:** CRITICAL
- Immediate comprehensive security assessment
- Firmware integrity verification on all network devices
- Review of all configuration file access logs
- Federal coordination for wiretapping system security

### Energy
**Priority:** CRITICAL
- IT/OT segmentation verification
- 5-year historical log analysis for Volt Typhoon indicators
- Emergency response coordination with government
- Backup plan for complete system isolation

### Water/Wastewater
**Priority:** CRITICAL
- Inventory all Internet-facing IoT/OT devices
- Immediate removal from direct Internet exposure
- IOCONTROL malware scanning
- Emergency operational procedures without automation

### Healthcare
**Priority:** HIGH
- Ransomware-specific detection deployment
- Backup system hardening and testing
- Incident response plan for patient care continuity
- Data protection and privacy compliance review

### Financial Services
**Priority:** HIGH
- FIN7 infrastructure monitoring (4000+ shell domains)
- EDR with AvNeutralizer detection signatures
- Advanced email security deployment
- Payment card data encryption verification

### Government
**Priority:** CRITICAL
- DMARC policy enforcement
- APT29 RDP campaign detection
- Kimsuky social engineering awareness training
- Comprehensive espionage threat assessment

### Manufacturing
**Priority:** HIGH
- Akira ransomware-specific defenses
- VMware ESXi and Hyper-V hardening
- Supply chain cyber risk assessment
- Operational technology protection

---

## CONCLUSION

The September-November 2024 period represents a significant escalation in both nation-state APT operations and ransomware campaigns targeting critical infrastructure. The convergence of espionage, pre-positioning for disruptive operations, and financially-motivated ransomware creates an unprecedented threat landscape requiring immediate and coordinated response.

### Key Takeaways

1. **Nation-State Pre-Positioning:** Chinese APT groups have established long-term persistent access to U.S. critical infrastructure with clear intent to enable disruptive cyber-physical attacks during potential conflicts.

2. **Telecommunications Crisis:** The telecommunications sector faces existential security challenges with multiple major providers compromised and potential exposure of federal wiretapping systems.

3. **Cyber-Physical Threats:** IOCONTROL malware demonstrates nation-state willingness to conduct destructive attacks on civilian water systems, crossing traditional red lines.

4. **Ransomware Maturation:** Ransomware groups have achieved unprecedented sophistication with $300M+ in payments, critical infrastructure impacts, and nation-state collaboration.

5. **Detection Challenges:** LOTL techniques, firmware-level persistence, and 5+ year dwell times demonstrate significant gaps in current detection capabilities.

### Priority Actions

**Week 1:**
- Emergency patching of critical CVEs
- DMARC enforcement
- Credential rotation
- Backup verification

**Month 1:**
- Network segmentation implementation
- Enhanced monitoring deployment
- Incident response plan updates
- Stakeholder communication

**Quarter 1:**
- Zero trust architecture deployment
- OT security enhancement
- Threat hunting program establishment
- Industry collaboration activation

### Final Assessment

The threat landscape documented in this report requires a fundamental shift in cybersecurity strategy. Organizations can no longer rely solely on perimeter defenses and signature-based detection. A comprehensive approach combining zero trust architecture, continuous monitoring, threat hunting, and rapid incident response is essential for survival in this environment.

Critical infrastructure defenders must assume breach, implement defense-in-depth, and maintain constant vigilance. The sophistication, patience, and determination demonstrated by these threat actors demands an equal commitment to security excellence and operational resilience.

---

## APPENDICES

### Appendix A: Individual APT Profile Documents
- NCC-OTCE-EAB-020: Salt Typhoon APT Campaign
- NCC-OTCE-EAB-021: Volt Typhoon APT Campaign
- NCC-OTCE-EAB-022: CyberAv3ngers IOCONTROL Malware Campaign
- NCC-OTCE-EAB-023: Sandworm ZEROLOT Wiper Campaign
- NCC-OTCE-EAB-024: Lazarus Group DEV#POPPER Campaign
- NCC-OTCE-EAB-025: Kimsuky DMARC Exploitation Campaign
- NCC-OTCE-EAB-026: APT29 Midnight Blizzard RDP Campaign
- NCC-OTCE-EAB-027: Mustang Panda ASEAN Targeting
- NCC-OTCE-EAB-028: Qilin Ransomware Healthcare Targeting
- NCC-OTCE-EAB-029: Akira Ransomware Critical Infrastructure Campaign
- NCC-OTCE-EAB-030: FIN7 Financial Sector Evolution

### Appendix B: MITRE ATT&CK Navigator Layers
[Available separately for each campaign]

### Appendix C: IoC Compilation
[Consolidated IoC list available in machine-readable format]

### Appendix D: Detection Rules
[SIEM detection rules available separately]

---

## SOURCES AND REFERENCES

All source materials properly cited in individual APT profile documents including:
- Government advisories (CISA, FBI, NSA, DoD, HHS)
- Threat intelligence vendor reports (Microsoft, Palo Alto, ESET, Kaspersky)
- Cybersecurity research organizations
- Industry sector ISACs

---

## DISTRIBUTION AND UPDATES

**Distribution:** TLP:CLEAR - May be distributed without restriction
**Next Review Date:** 2025-02-28
**Update Schedule:** Quarterly with emergency updates as needed
**Contact:** otce-research@ncc.example.com
**Report Version:** 1.0 (Initial Release)

---

**Document Classification:** TLP:CLEAR
**Total Pages:** [Auto-generated]
**Word Count:** ~8,500
**Profiles Documented:** 11 APT Campaigns
**Research Period:** September 2024 - November 2024

---

*End of Report*

**NCC OTCE Research Team**
**Operational Technology Cyber Excellence**
**2024-11-28**
