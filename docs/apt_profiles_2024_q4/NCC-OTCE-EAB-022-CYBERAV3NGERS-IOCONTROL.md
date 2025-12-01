# NCC-OTCE-EAB-022: CyberAv3ngers IOCONTROL Malware Campaign

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-022
**Date:** 2024-11-28
**Version:** 1.0
**Author:** NCC OTCE Research Team
**Campaign Period:** October 2023 - November 2024 (Relaunched July-August 2024)

---

## EXECUTIVE SUMMARY

CyberAv3ngers is an Iranian threat group linked to the Islamic Revolutionary Guard Corps (IRGC) conducting sophisticated cyberattacks against critical infrastructure, particularly targeting water and wastewater systems using the custom IOCONTROL malware. The group represents a significant escalation in nation-state cyber-physical attacks against civilian critical infrastructure, with operations targeting both the United States and Israel.

**Threat Level:** CRITICAL
**Primary Motivation:** Destructive/Disruptive Operations Against Critical Infrastructure
**Attribution:** Iran - Islamic Revolutionary Guard Corps Cyber Electronic Command (IRGC-CEC)
**Also Known As:** Storm-0784 (Microsoft tracking)

---

## THREAT ACTOR PROFILE

### Attribution & Background
- **Nation-State Sponsor:** Islamic Republic of Iran
- **Military Unit:** Islamic Revolutionary Guard Corps Cyber Electronic Command (IRGC-CEC)
- **Active Since:** At least October 2023
- **Primary Objective:** Disrupt critical infrastructure operations in U.S. and Israel
- **Public Persona:** Claims to be hacktivist group (actually state-sponsored)

### U.S. Government Action
- **February 2024:** U.S. Department of Treasury announces sanctions against six IRGC-CEC officials
- **Bounty:** $10 million USD offered for information leading to identification of attackers

### Target Sectors
1. **Water and Wastewater Systems** (Primary)
2. **Fuel Management Systems**
3. **Critical Infrastructure IoT/OT Devices**
4. **Industrial Control Systems (ICS)**

### Geographic Targeting
- United States (Primary)
- Israel (Primary)
- Ireland
- Global critical infrastructure with targeted device manufacturers

---

## CAMPAIGN ANALYSIS (2024 Activity)

### Campaign Timeline
- **October 2023 - January 2024:** Initial attacks on Orpak and Unitronics devices
- **November 2023:** Unitronics attack on U.S. water utility in Pennsylvania
- **November 2023:** Ireland water facility attack causing 2-day water supply disruption
- **July-August 2024:** Campaign relaunched with expanded targeting
- **Mid-2024:** New campaigns emerge with IOCONTROL malware
- **October-November 2024:** Continued active operations

### High-Profile Incidents
1. **Pennsylvania Water Utility (Nov 2023)**
   - Municipal Authority of Aliquippa targeted
   - PLC systems compromised
   - Public water supply threatened

2. **Ireland Water Facility (Nov 2023)**
   - 2-day complete water supply cutoff
   - Severe service disruption
   - Population-wide impact

---

## IOCONTROL MALWARE ANALYSIS

### Malware Overview
IOCONTROL is a modular cyberweapon designed specifically for attacking IoT and OT devices across multiple manufacturers and platforms. It represents a sophisticated cyber-physical attack capability.

### Technical Characteristics
1. **Modular Architecture**
   - Adaptable to various device types
   - Manufacturer-agnostic design
   - Platform flexibility (Linux, Windows, embedded systems)

2. **Communication Protocol**
   - Uses MQTT (IoT messaging protocol)
   - Disguises malicious traffic as legitimate IoT communications
   - Cloudflare DNS over HTTPS (DoH) for C2
   - Enhanced evasion capabilities

3. **Multi-Platform Support**
   - Linux-based systems
   - Windows platforms
   - Embedded IoT devices
   - Industrial PLCs and HMIs

### Targeted Device Manufacturers
- D-Link (routers, network equipment)
- Hikvision (IP cameras, surveillance)
- Baicells (cellular infrastructure)
- Red Lion (industrial automation)
- Orpak (fuel management systems)
- Phoenix Contact (industrial automation)
- Teltonika (IoT routers and gateways)
- Unitronics (PLCs for water systems)

### Targeted Device Types
1. **Network Infrastructure**
   - Routers
   - Firewalls
   - Network switches

2. **Industrial Control Systems**
   - Programmable Logic Controllers (PLCs)
   - Human-Machine Interfaces (HMIs)
   - SCADA systems

3. **IoT Devices**
   - IP cameras
   - Fuel management systems
   - Building automation systems

---

## TACTICS, TECHNIQUES, AND PROCEDURES (TTPs)

### Initial Access
**T1190 - Exploit Public-Facing Application**
- Exploitation of Internet-facing IoT/OT devices
- Targeting of default or weak credentials
- Vulnerability exploitation in unpatched systems

### Persistence
**T1542 - Pre-OS Boot / Firmware Modification**
- Malware installation on embedded devices
- Persistence through firmware-level implants
- Survival across device reboots

### Defense Evasion
**T1071.001 - Application Layer Protocol: Web Protocols**
- Use of MQTT protocol to blend with legitimate IoT traffic
- DNS over HTTPS (DoH) via Cloudflare
- Encryption of C2 communications

**T1140 - Deobfuscate/Decode Files or Information**
- Evasion through protocol obfuscation
- Legitimate service abuse (Cloudflare)

### Impact
**T1485 - Data Destruction**
- Disruption of water supply systems
- Fuel management system manipulation
- Critical infrastructure service interruption

**T1498 - Network Denial of Service**
- Service disruption at water facilities
- Infrastructure availability attacks

---

## MALWARE & TOOLS

### IOCONTROL Malware Components
1. **Core Malware Module**
   - Multi-device compatibility
   - Modular plugin architecture
   - Remote command execution

2. **Communication Module**
   - MQTT protocol implementation
   - Cloudflare DoH integration
   - C2 channel encryption

3. **Payload Modules**
   - Device-specific exploitation
   - Configuration manipulation
   - Service disruption capabilities

### Infrastructure
- Cloudflare DNS over HTTPS services
- MQTT broker infrastructure
- Distributed C2 architecture

---

## INDICATORS OF COMPROMISE (IoCs)

### Network Indicators
1. **MQTT Traffic Patterns**
   - Unusual MQTT broker connections
   - Non-standard MQTT message patterns
   - MQTT traffic to unknown brokers

2. **DNS over HTTPS (DoH) Usage**
   - Connections to Cloudflare DoH services from IoT/OT devices
   - DNS resolution patterns inconsistent with device function

3. **C2 Communications**
   - Encrypted outbound connections from IoT/OT devices
   - Periodic beaconing patterns
   - Data exfiltration from control systems

### Device Indicators
1. **Configuration Changes**
   - Unauthorized PLC program modifications
   - HMI configuration alterations
   - Unexpected device behavior

2. **Unauthorized Access**
   - Login attempts from unusual IP addresses
   - Credential usage outside normal patterns
   - Access to devices during non-operational hours

### Behavioral Indicators
- Water system operational anomalies
- Fuel management discrepancies
- Unexpected device reboots
- Loss of device visibility or control

---

## IMPACT ASSESSMENT

### Critical Infrastructure Impact
- **SEVERITY:** CRITICAL
- Direct disruption of water supply to civilian populations
- Potential for public health emergencies
- Risk of environmental damage
- Economic impact from service disruption

### Cyber-Physical Consequences
1. **Water Systems**
   - Loss of water pressure control
   - Contamination risks
   - Public safety threats

2. **Fuel Management**
   - Supply chain disruption
   - Safety hazard creation
   - Economic losses

3. **Population Impact**
   - Essential services disruption
   - Public health risks
   - Loss of confidence in critical infrastructure security

---

## MITRE ATT&CK FOR ICS MAPPING

| Tactic | Technique ID | Technique Name |
|--------|--------------|----------------|
| Initial Access | T0819 | Exploit Public-Facing Application |
| Execution | T0807 | Command-Line Interface |
| Persistence | T0873 | Project File Infection |
| Evasion | T0849 | Masquerading |
| Discovery | T0840 | Network Connection Enumeration |
| Collection | T0802 | Automated Collection |
| Command and Control | T0885 | Commonly Used Port |
| Inhibit Response Function | T0804 | Block Serial COM |
| Impair Process Control | T0806 | Brute Force I/O |
| Impact | T0826 | Loss of Availability |
| Impact | T0828 | Loss of Control |

---

## DETECTION STRATEGIES

### Network-Based Detection
1. **MQTT Traffic Monitoring**
   - Deploy MQTT protocol inspection
   - Baseline normal IoT device MQTT usage
   - Alert on unusual broker connections
   - Monitor MQTT message content

2. **DNS over HTTPS Detection**
   - Identify IoT/OT devices using DoH
   - Monitor Cloudflare DoH connections from industrial devices
   - Detect DNS resolution pattern anomalies

3. **OT Network Monitoring**
   - Deploy industrial network monitoring solutions
   - Use protocol-aware inspection (Modbus, DNP3, etc.)
   - Monitor IT/OT boundary crossings

### Device-Based Detection
1. **Configuration Monitoring**
   - Implement configuration baselines
   - Alert on unauthorized PLC program changes
   - Track HMI configuration modifications
   - Monitor firmware integrity

2. **Access Monitoring**
   - Log all device authentication attempts
   - Monitor privileged access usage
   - Track remote access sessions
   - Alert on credential anomalies

### Behavioral Analytics
1. **Operational Anomalies**
   - Baseline normal operational parameters
   - Detect process value deviations
   - Monitor alarm patterns
   - Track system state changes

2. **Device Behavior**
   - Monitor device reboot patterns
   - Track network connection changes
   - Detect unusual communication patterns

---

## MITIGATION RECOMMENDATIONS

### Immediate Actions
1. **Device Inventory and Assessment**
   - Identify all Internet-facing IoT/OT devices
   - Prioritize devices from targeted manufacturers
   - Assess vulnerability exposure

2. **Network Segmentation**
   - Remove IoT/OT devices from direct Internet exposure
   - Implement DMZ for remote access
   - Deploy industrial firewalls
   - Isolate critical control systems

3. **Credential Security**
   - Change all default passwords immediately
   - Implement strong authentication
   - Use unique credentials per device
   - Deploy multi-factor authentication where possible

4. **Patch Management**
   - Apply security updates to all vulnerable devices
   - Prioritize Unitronics, Orpak, and other targeted systems
   - Implement regular patching schedule

### Strategic Mitigations
1. **Zero Trust for OT**
   - Implement least-privilege access
   - Require authentication for all device access
   - Continuous verification of device identity
   - Micro-segmentation of OT networks

2. **Enhanced Monitoring**
   - Deploy OT-specific security solutions
   - Implement SIEM with ICS/SCADA capabilities
   - Use network traffic analysis (NTA) for industrial protocols
   - Enable comprehensive logging

3. **Vendor Security**
   - Work with device manufacturers on security
   - Request security advisories
   - Participate in vendor security programs
   - Evaluate device security before procurement

4. **Incident Response**
   - Develop OT-specific IR playbooks
   - Conduct tabletop exercises for water/critical infrastructure
   - Establish government coordination (CISA, FBI, WaterISAC)
   - Prepare backup operational procedures

---

## HUNTING GUIDANCE

### Hunt Hypothesis 1: IOCONTROL Infection
**Hypothesis:** IoT/OT devices may be infected with IOCONTROL malware.
**Actions:**
- Scan for unusual MQTT broker connections
- Check for Cloudflare DoH usage from industrial devices
- Review device configuration changes
- Analyze network traffic for command patterns

### Hunt Hypothesis 2: Credential Compromise
**Hypothesis:** Device credentials may be compromised.
**Actions:**
- Audit all device authentication logs
- Check for default credential usage
- Review remote access patterns
- Validate credential strength across all devices

### Hunt Hypothesis 3: Unauthorized Device Access
**Hypothesis:** Attackers may have persistent access to control systems.
**Actions:**
- Review historical access logs
- Check for access during non-operational hours
- Identify unusual IP address connections
- Validate all remote access sessions

---

## INTELLIGENCE GAPS

1. Full IOCONTROL malware code analysis in progress
2. Complete C2 infrastructure mapping unknown
3. Additional targeted device manufacturers may exist
4. Coordination with other Iranian APT groups unclear
5. Full capability of malware payloads requires further analysis

---

## REFERENCES

1. [The Register - Iran Crew Used Cyberweapon Against US Critical Infrastructure](https://www.theregister.com/2024/12/13/iran_cyberweapon_us_attacks)
2. [WaterISAC - IOCONTROL and Adroxgh0st Malware Threat Awareness](https://www.waterisac.org/otics-threat-awareness-iocontrol-and-adroxgh0st-malware-target-critical-infrastructure)
3. [Claroty Team82 - Inside IOCONTROL OT/IoT Cyberweapon](https://claroty.com/team82/research/inside-a-new-ot-iot-cyber-weapon-iocontrol)
4. [SecurityWeek - Iranian Hackers Use IOCONTROL Malware](https://www.securityweek.com/iranian-hackers-use-iocontrol-malware-to-target-ot-iot-devices-in-us-israel/)
5. [BleepingComputer - IOCONTROL Malware in Critical Infrastructure Attacks](https://www.bleepingcomputer.com/news/security/new-iocontrol-malware-used-in-critical-infrastructure-attacks/)
6. [Industrial Cyber - Iran-linked IOCONTROL Malware](https://industrialcyber.co/news/iran-linked-iocontrol-malware-targets-critical-iot-ot-infrastructure-in-israel-us/)

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
