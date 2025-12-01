# NCC-OTCE-EAB-023: Sandworm ZEROLOT Wiper Campaign

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-023
**Date:** 2024-11-28
**Version:** 1.0
**Author:** NCC OTCE Research Team
**Campaign Period:** October 2024 - March 2025

---

## EXECUTIVE SUMMARY

Sandworm, Russia's notorious cyber sabotage unit (also tracked as APT44), has intensified destructive operations against Ukrainian organizations using a new wiper malware named ZEROLOT. The campaign represents a continuation of Russia's cyber warfare strategy targeting Ukraine's critical infrastructure, particularly energy and grain sectors.

**Threat Level:** CRITICAL
**Primary Motivation:** Destructive/Sabotage Operations
**Attribution:** Russian Federation - GRU Unit 74455
**Also Known As:** APT44, Voodoo Bear, IRIDIUM, Seashell Blizzard, IRON VIKING

---

## THREAT ACTOR PROFILE

### Attribution & Background
- **Nation-State Sponsor:** Russian Federation
- **Military Unit:** GRU Main Centre for Special Technologies (GTsST) Unit 74455
- **Active Since:** 2007
- **Historical Operations:** NotPetya (2017), Olympic Destroyer (2018), Ukraine power grid attacks (2015, 2016)

### Target Sectors
1. **Energy** (Primary - Ukrainian grid)
2. **Grain and Agriculture**
3. **Government Institutions**
4. **Logistics and Transportation**
5. **Universities and Education**

### Geographic Targeting
- Ukraine (Primary)
- NATO member states (Secondary)
- Critical infrastructure globally

---

## CAMPAIGN ANALYSIS (Oct 2024 - Mar 2025)

### ZEROLOT Deployment Timeline
- **October 2024:** Initial ZEROLOT deployments against Ukrainian energy companies
- **November 2024 - March 2025:** Sustained attacks across multiple sectors
- **April 2025:** Deployment of ZEROLOT and STING wipers against Ukrainian university

### Target Profile
- Energy sector organizations
- Grain production and distribution companies
- Logistics firms supporting grain exports
- Government agencies
- Educational institutions

---

## TACTICS, TECHNIQUES, AND PROCEDURES (TTPs)

### Initial Access
- **T1566.002:** Spearphishing with malicious attachments
- **T1190:** Exploitation of public-facing vulnerabilities including zero-days
- **T1195:** Supply chain compromise

### Lateral Movement and Deployment
- **T1484:** Group Policy abuse for wiper deployment
- PowerGPOAbuse and TANKTRAP utilities for GPO exploitation
- Active Directory Group Policy Objects (GPO) manipulation

### Persistence and Scheduling
- **T1053:** Scheduled tasks for staging malware
- Delayed execution for operational security
- Strategic timing to maximize impact

### Impact
- **T1485:** Data Destruction via ZEROLOT wiper
- **T1486:** Data Encrypted for Impact (historical ransomware operations)
- Multi-layered destruction: file-level corruption + partition structure destruction

---

## ZEROLOT WIPER ANALYSIS

### Technical Characteristics
1. **Multi-Layered Destruction**
   - File-level data corruption
   - Partition structure destruction
   - Boot sector targeting
   - Master Boot Record (MBR) overwriting

2. **Data-Zeroing Methods**
   - Systematic overwriting with zeros
   - Multiple pass operations
   - Metadata destruction
   - Recovery prevention techniques

3. **Deployment Mechanism**
   - Active Directory GPO abuse
   - Network-wide simultaneous deployment
   - Timed execution for maximum impact

### Associated Tools
- **ZEROLOT:** Primary wiper malware
- **STING:** Secondary wiper variant
- **TANKTRAP:** GPO abuse utility
- **PowerGPOAbuse:** Modified PowerShell GPO exploitation tool

---

## MITRE ATT&CK MAPPING

| Tactic | Technique ID | Technique Name |
|--------|--------------|----------------|
| Initial Access | T1566.002 | Phishing: Spearphishing Link |
| Initial Access | T1190 | Exploit Public-Facing Application |
| Initial Access | T1195 | Supply Chain Compromise |
| Execution | T1053 | Scheduled Task/Job |
| Persistence | T1053 | Scheduled Task/Job |
| Defense Evasion | T1484 | Domain Policy Modification |
| Lateral Movement | T1021.001 | Remote Desktop Protocol |
| Impact | T1485 | Data Destruction |
| Impact | T1490 | Inhibit System Recovery |

---

## INDICATORS OF COMPROMISE (IoCs)

### Malware Signatures
- ZEROLOT wiper file hashes
- STING wiper variants
- Modified PowerGPOAbuse scripts
- TANKTRAP utility signatures

### Behavioral Indicators
- Unusual GPO modifications
- Scheduled task creation targeting multiple systems
- Mass file deletion/corruption events
- Boot sector modification attempts
- Partition table alterations

### Network Indicators
- Lateral movement via RDP
- SMB traffic patterns consistent with wiper deployment
- Domain controller enumeration
- GPO replication anomalies

---

## DETECTION STRATEGIES

### GPO Monitoring
- Monitor Group Policy modifications
- Alert on unauthorized GPO creation
- Track GPO application to unusual OUs
- Detect PowerShell GPO cmdlet abuse

### Scheduled Task Detection
- Monitor scheduled task creation across the enterprise
- Alert on tasks with destructive payloads
- Track task scheduling from domain controllers
- Detect synchronized task execution

### Data Protection Monitoring
- Monitor for mass file modification events
- Detect rapid file deletion patterns
- Alert on boot sector access attempts
- Track partition table modifications

---

## MITIGATION RECOMMENDATIONS

### Immediate Actions
1. **GPO Hardening**
   - Audit all Group Policy Objects
   - Restrict GPO modification permissions
   - Enable GPO change logging
   - Implement least-privilege for GPO management

2. **Backup Strategy**
   - Implement immutable backups
   - Offline backup copies
   - Regular backup testing
   - Geographic backup distribution

3. **Network Segmentation**
   - Isolate critical systems
   - Implement jump boxes for administration
   - Restrict lateral movement paths

### Strategic Mitigations
1. **Active Directory Security**
   - Implement tiered administration model
   - Use dedicated admin workstations
   - Enable credential guard
   - Deploy LAPS for local admin passwords

2. **Detection and Response**
   - Deploy EDR with wiper-specific signatures
   - Implement SIEM with GPO monitoring rules
   - Enable advanced threat protection
   - Conduct regular threat hunting

3. **Resilience Planning**
   - Develop business continuity plans
   - Conduct disaster recovery exercises
   - Prepare for complete system rebuilds
   - Establish government coordination channels

---

## REFERENCES

1. [Immersive Labs - ZEROLOT Analysis: Inside Sandworm's Destructive New Wiper](https://www.immersivelabs.com/resources/blog/zerolot-analysis-inside-sandworms-destructive-new-wiper)
2. [ESET - APT Report: Russian Cyberattacks in Ukraine Intensify](https://www.eset.com/gr-en/about/newsroom/press-releases-1/eset-research-apt-report-russian-cyberattacks-in-ukraine-intensify-sandworm-unleashes-new-destructive-wiper-1/)
3. [Infosecurity Magazine - Sandworm Deploys New Wiper in Ukraine](https://www.infosecurity-magazine.com/news/russian-sandworm-new-wiper-ukraine/)
4. [The Record - Russia's Sandworm Deploying Wipers Against Ukraine Grain Industry](https://therecord.media/russia-sandworm-grain-wipers)
5. [Google Cloud - Unearthing APT44: Russia's Notorious Cyber Sabotage Unit](https://cloud.google.com/blog/topics/threat-intelligence/apt44-unearthing-sandworm)

---

## CHANGE LOG

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-28 | Initial report creation | NCC OTCE Research Team |

---

**Distribution:** TLP:CLEAR
**Next Review Date:** 2025-02-28
**Contact:** otce-research@ncc.example.com

---
*End of Report*
