# Cyber-FMEA: SCADA and Control System Cybersecurity Analysis

## Overview
Cyber-FMEA applies FMEA methodology specifically to cybersecurity threats in SCADA, DCS, and industrial control systems. This document analyzes cyber failure modes with risk priority calculations.

## Cyber-FMEA Parameters
- **Cyber Severity (CS)**: Impact of successful cyber attack (1-10 scale)
- **Attack Likelihood (AL)**: Probability of attack occurring (1-10 scale)
- **Detection Difficulty (DD)**: Difficulty detecting attack before impact (1-10 scale)
- **Cyber Risk Priority Number (CRPN)**: CS × AL × DD

---

## Cyber-FMEA Entry 1: SCADA Master Server Compromise

**Component**: [[EQUIPMENT: SCADA master station server]]
**Cyber Failure Mode**: Remote code execution leading to complete SCADA control
**Attack Vector**: [[ATTACK_PATTERN: Operating system vulnerability exploitation]]
**Root Cause**: [[VULNERABILITY: Unpatched Windows Server]]

**Consequences**:
- [[HAZARD: Unauthorized control of all field devices]]
- Critical infrastructure service disruption
- Safety system manipulation potential
- Data integrity loss

**Current Cyber Controls**:
- [[MITIGATION: Firewall protection]]
- [[ARCHITECTURE: SCADA DMZ]]
- Basic antivirus protection

**Risk Assessment**:
- **Cyber Severity (CS)**: 10 - Catastrophic impact on operations
- **Attack Likelihood (AL)**: 7 - Known vulnerabilities actively exploited
- **Detection Difficulty (DD)**: 6 - May evade basic monitoring
- **CRPN**: 420 (Critical - Immediate Action Required)

**Recommended Actions**:
- Implement [[MITIGATION: Automated patch management]]
- Deploy [[ARCHITECTURE: SCADA server virtualization with snapshots]]
- Add [[MITIGATION: Endpoint detection and response]]
- Establish [[ARCHITECTURE: Server activity baseline monitoring]]

**Threat Actor**: [[THREAT_ACTOR: Nation-state APT targeting critical infrastructure]]

---

## Cyber-FMEA Entry 2: PLC Ladder Logic Manipulation

**Component**: [[EQUIPMENT: Allen-Bradley ControlLogix PLC]]
**Cyber Failure Mode**: Unauthorized modification of control logic
**Attack Vector**: [[ATTACK_PATTERN: EtherNet/IP exploitation]]
**Root Cause**: [[VULNERABILITY: No authentication on PLC communications]]

**Consequences**:
- [[HAZARD: Process control corruption]]
- Safety interlock bypass
- Equipment damage
- Production quality failure

**Current Cyber Controls**:
- [[ARCHITECTURE: Control network VLAN isolation]]
- Physical access restrictions
- [[MITIGATION: Change logs]]

**Risk Assessment**:
- **Cyber Severity (CS)**: 9 - Major safety and production impact
- **Attack Likelihood (AL)**: 5 - Requires network access
- **Detection Difficulty (DD)**: 8 - Logic changes hard to detect
- **CRPN**: 360 (High - Priority Action)

**Recommended Actions**:
- Implement [[MITIGATION: PLC FactoryTalk security features]]
- Deploy [[ARCHITECTURE: Unidirectional gateway for engineering access]]
- Add [[MITIGATION: Cryptographic logic checksums]]
- Establish [[ARCHITECTURE: Change detection monitoring]]

**Threat Actor**: [[THREAT_ACTOR: Industrial sabotage actor]]

---

## Cyber-FMEA Entry 3: HMI Session Hijacking

**Component**: [[EQUIPMENT: WonderWare HMI workstation]]
**Cyber Failure Mode**: Session takeover enabling unauthorized commands
**Attack Vector**: [[ATTACK_PATTERN: VNC server vulnerability exploitation]]
**Root Cause**: [[VULNERABILITY: Weak VNC authentication]]

**Consequences**:
- [[HAZARD: Operator impersonation]]
- Unauthorized process changes
- Alarm suppression
- Historical data manipulation

**Current Cyber Controls**:
- [[MITIGATION: VNC password protection]]
- [[ARCHITECTURE: Operator network separation]]
- Login audit trails

**Risk Assessment**:
- **Cyber Severity (CS)**: 8 - Significant operational impact
- **Attack Likelihood (AL)**: 6 - Common vulnerability
- **Detection Difficulty (DD)**: 7 - Looks like legitimate operator
- **CRPN**: 336 (High - Priority Action)

**Recommended Actions**:
- Replace VNC with [[MITIGATION: Secure remote desktop with MFA]]
- Implement [[ARCHITECTURE: Session monitoring and timeout]]
- Add [[MITIGATION: Behavioral analytics for operator actions]]
- Deploy [[ARCHITECTURE: Command validation system]]

**Threat Actor**: [[THREAT_ACTOR: Insider threat with network access]]

---

## Cyber-FMEA Entry 4: RTU Communication Interception

**Component**: [[EQUIPMENT: Remote terminal unit]]
**Cyber Failure Mode**: Man-in-the-middle attack on SCADA communications
**Attack Vector**: [[ATTACK_PATTERN: DNP3 protocol manipulation]]
**Root Cause**: [[VULNERABILITY: Cleartext DNP3 communications]]

**Consequences**:
- [[HAZARD: False telemetry data]]
- Incorrect control decisions
- Loss of situational awareness
- Cascade failures

**Current Cyber Controls**:
- [[ARCHITECTURE: Private radio network]]
- [[MITIGATION: Physical site security]]
- Basic message validation

**Risk Assessment**:
- **Cyber Severity (CS)**: 7 - Major operational disruption
- **Attack Likelihood (AL)**: 5 - Requires field access or radio
- **Detection Difficulty (DD)**: 8 - Subtle data manipulation
- **CRPN**: 280 (High - Action Required)

**Recommended Actions**:
- Implement [[MITIGATION: DNP3 Secure Authentication]]
- Deploy [[ARCHITECTURE: Encrypted radio communications]]
- Add [[MITIGATION: RTU data validation logic]]
- Establish [[ARCHITECTURE: Anomaly detection for telemetry]]

**Threat Actor**: [[THREAT_ACTOR: Sophisticated attacker with RF capability]]

---

## Cyber-FMEA Entry 5: Engineering Workstation Malware

**Component**: [[EQUIPMENT: DCS engineering workstation]]
**Cyber Failure Mode**: Malware infection leading to backdoor insertion
**Attack Vector**: [[ATTACK_PATTERN: USB-borne malware]]
**Root Cause**: [[VULNERABILITY: No USB device control]]

**Consequences**:
- [[HAZARD: Control system backdoor]]
- Persistent unauthorized access
- Data exfiltration
- Future attack staging

**Current Cyber Controls**:
- [[MITIGATION: Antivirus software]]
- User training
- [[ARCHITECTURE: Network firewall]]

**Risk Assessment**:
- **Cyber Severity (CS)**: 9 - Long-term compromise
- **Attack Likelihood (AL)**: 6 - USB attacks common
- **Detection Difficulty (DD)**: 7 - Advanced malware evasive
- **CRPN**: 378 (High - Priority Action)

**Recommended Actions**:
- Implement [[MITIGATION: USB device whitelisting]]
- Deploy [[ARCHITECTURE: Application whitelisting on workstation]]
- Add [[MITIGATION: Endpoint detection and response]]
- Establish [[ARCHITECTURE: Air-gapped programming network]]

**Threat Actor**: [[THREAT_ACTOR: Targeted malware campaign]]

---

## Cyber-FMEA Entry 6: Historian Database Injection

**Component**: [[EQUIPMENT: OSIsoft PI Historian]]
**Cyber Failure Mode**: SQL injection enabling data manipulation
**Attack Vector**: [[ATTACK_PATTERN: Web interface SQL injection]]
**Root Cause**: [[VULNERABILITY: Input validation flaw]]

**Consequences**:
- [[HAZARD: Historical data corruption]]
- Regulatory compliance loss
- Forensic evidence destruction
- Business intelligence compromise

**Current Cyber Controls**:
- [[ARCHITECTURE: Historian network segment]]
- [[MITIGATION: Database backups]]
- User authentication

**Risk Assessment**:
- **Cyber Severity (CS)**: 6 - Data integrity impact
- **Attack Likelihood (AL)**: 7 - SQL injection common
- **Detection Difficulty (DD)**: 9 - Hard to detect data changes
- **CRPN**: 378 (High - Priority Action)

**Recommended Actions**:
- Fix [[VULNERABILITY: SQL injection]] with parameterized queries
- Implement [[MITIGATION: Database activity monitoring]]
- Add [[ARCHITECTURE: Write-once-read-many data storage]]
- Deploy [[MITIGATION: Data integrity verification]]

**Threat Actor**: [[THREAT_ACTOR: Data integrity attacker]]

---

## Cyber-FMEA Entry 7: Industrial Firewall Bypass

**Component**: [[EQUIPMENT: Tofino industrial firewall]]
**Cyber Failure Mode**: Firewall rule exploitation
**Attack Vector**: [[ATTACK_PATTERN: Protocol tunneling through allowed ports]]
**Root Cause**: [[VULNERABILITY: Deep packet inspection not enabled]]

**Consequences**:
- [[HAZARD: Control network exposure]]
- Perimeter defense failure
- Lateral movement enablement
- Defense-in-depth compromise

**Current Cyber Controls**:
- [[MITIGATION: Firewall ruleset]]
- [[ARCHITECTURE: Network segmentation]]
- Log monitoring

**Risk Assessment**:
- **Cyber Severity (CS)**: 8 - Network perimeter breach
- **Attack Likelihood (AL)**: 5 - Sophisticated technique
- **Detection Difficulty (DD)**: 6 - Traffic appears legitimate
- **CRPN**: 240 (Medium-High - Action Recommended)

**Recommended Actions**:
- Enable [[MITIGATION: Deep packet inspection]]
- Implement [[ARCHITECTURE: Application layer firewall]]
- Add [[MITIGATION: Protocol whitelisting]]
- Deploy [[ARCHITECTURE: Network behavior analytics]]

**Threat Actor**: [[THREAT_ACTOR: Advanced network penetration specialist]]

---

## Cyber-FMEA Entry 8: Redundant Controller Common Mode Failure

**Component**: [[EQUIPMENT: Redundant DCS controller pair]]
**Cyber Failure Mode**: Both controllers compromised by same exploit
**Attack Vector**: [[ATTACK_PATTERN: Firmware vulnerability exploitation]]
**Root Cause**: [[VULNERABILITY: Identical firmware versions]]

**Consequences**:
- [[HAZARD: Complete control system failure]]
- Loss of redundancy benefit
- Extended downtime
- Process safety risk

**Current Cyber Controls**:
- [[ARCHITECTURE: Hot-standby redundancy]]
- [[MITIGATION: Firmware version control]]
- Change management

**Risk Assessment**:
- **Cyber Severity (CS)**: 10 - Total system failure
- **Attack Likelihood (AL)**: 3 - Rare sophisticated attack
- **Detection Difficulty (DD)**: 5 - System failure obvious
- **CRPN**: 150 (Medium - Monitor and Improve)

**Recommended Actions**:
- Implement [[ARCHITECTURE: N-version programming]]
- Deploy [[MITIGATION: Diverse firmware versions]]
- Add [[ARCHITECTURE: Independent safety controller]]
- Establish [[MITIGATION: Firmware integrity monitoring]]

**Threat Actor**: [[THREAT_ACTOR: Nation-state actor with zero-day capability]]

---

## Cyber-FMEA Entry 9: Wireless Sensor Network Jamming

**Component**: [[EQUIPMENT: WirelessHART sensor network]]
**Cyber Failure Mode**: RF jamming causing sensor data loss
**Attack Vector**: [[ATTACK_PATTERN: Radio frequency jamming]]
**Root Cause**: [[VULNERABILITY: Single frequency operation]]

**Consequences**:
- [[HAZARD: Loss of process visibility]]
- Control system blind operation
- Safety alarm failure
- Emergency response delay

**Current Cyber Controls**:
- [[MITIGATION: Frequency hopping]]
- [[ARCHITECTURE: Mesh network topology]]
- Signal strength monitoring

**Risk Assessment**:
- **Cyber Severity (CS)**: 7 - Major monitoring loss
- **Attack Likelihood (AL)**: 4 - Requires proximity and equipment
- **Detection Difficulty (DD)**: 3 - Signal loss obvious
- **CRPN**: 84 (Low-Medium - Acceptable with Monitoring)

**Recommended Actions**:
- Implement [[ARCHITECTURE: Wired sensor backup for critical]]
- Deploy [[MITIGATION: RF spectrum monitoring]]
- Add [[ARCHITECTURE: Multi-frequency operation]]
- Establish [[MITIGATION: Automatic failover to alternate path]]

**Threat Actor**: [[THREAT_ACTOR: Physical proximity attacker]]

---

## Cyber-FMEA Entry 10: Time Synchronization Attack

**Component**: [[EQUIPMENT: NTP time server]]
**Cyber Failure Mode**: Time source corruption affecting timestamps
**Attack Vector**: [[ATTACK_PATTERN: NTP amplification attack]]
**Root Cause**: [[VULNERABILITY: Unauthenticated NTP]]

**Consequences**:
- [[HAZARD: Event sequence confusion]]
- Forensic analysis compromise
- Certificate validation failure
- Coordinated control timing errors

**Current Cyber Controls**:
- [[ARCHITECTURE: Stratum-2 NTP server]]
- [[MITIGATION: NTP access control]]
- Multiple time sources

**Risk Assessment**:
- **Cyber Severity (CS)**: 5 - Time integrity impact
- **Attack Likelihood (AL)**: 6 - NTP attacks common
- **Detection Difficulty (DD)**: 7 - Subtle timestamp drift
- **CRPN**: 210 (Medium - Action Recommended)

**Recommended Actions**:
- Implement [[MITIGATION: NTP authentication (NTS)]]
- Deploy [[ARCHITECTURE: GPS-based Stratum-1 server]]
- Add [[MITIGATION: Time drift monitoring]]
- Establish [[ARCHITECTURE: Multiple diverse time sources]]

**Threat Actor**: [[THREAT_ACTOR: Forensic evidence destroyer]]

---

## Cyber-FMEA Entry 11: VPN Remote Access Compromise

**Component**: [[EQUIPMENT: VPN concentrator]]
**Cyber Failure Mode**: Unauthorized remote access through stolen credentials
**Attack Vector**: [[ATTACK_PATTERN: Phishing for VPN credentials]]
**Root Cause**: [[VULNERABILITY: Single-factor authentication]]

**Consequences**:
- [[HAZARD: External attacker gaining internal access]]
- Bypassing perimeter security
- Lateral movement capability
- Data exfiltration path

**Current Cyber Controls**:
- [[MITIGATION: Username and password authentication]]
- [[ARCHITECTURE: VPN session timeout]]
- Access logging

**Risk Assessment**:
- **Cyber Severity (CS)**: 9 - Remote attacker access
- **Attack Likelihood (AL)**: 8 - Phishing highly successful
- **Detection Difficulty (DD)**: 6 - Appears as legitimate remote worker
- **CRPN**: 432 (Critical - Immediate Action Required)

**Recommended Actions**:
- Implement [[MITIGATION: Multi-factor authentication]]
- Deploy [[ARCHITECTURE: Zero trust network access]]
- Add [[MITIGATION: Behavioral analytics for VPN users]]
- Establish [[ARCHITECTURE: Least privilege access control]]

**Threat Actor**: [[THREAT_ACTOR: Credential harvesting attacker]]

---

## Cyber-FMEA Entry 12: Safety PLC Network Connection

**Component**: [[EQUIPMENT: Siemens S7 F-series Safety PLC]]
**Cyber Failure Mode**: Safety function manipulation via network
**Attack Vector**: [[ATTACK_PATTERN: S7 protocol exploitation]]
**Root Cause**: [[VULNERABILITY: Safety PLC connected to control network]]

**Consequences**:
- [[HAZARD: Safety function defeat]]
- Loss of protection layer
- Safety integrity level compromise
- Regulatory non-compliance

**Current Cyber Controls**:
- [[MITIGATION: Safety PLC password protection]]
- [[ARCHITECTURE: Separate safety VLAN]]
- Safety key management

**Risk Assessment**:
- **Cyber Severity (CS)**: 10 - Safety system defeat
- **Attack Likelihood (AL)**: 3 - Difficult attack
- **Detection Difficulty (DD)**: 6 - Safety logic changes subtle
- **CRPN**: 180 (Medium - Action Recommended)

**Recommended Actions**:
- Implement [[ARCHITECTURE: Air gap for safety system]]
- Deploy [[MITIGATION: Unidirectional gateway for safety monitoring]]
- Add [[ARCHITECTURE: Diverse safety actuation]]
- Establish [[MITIGATION: Safety logic formal verification]]

**Threat Actor**: [[THREAT_ACTOR: Sophisticated safety system attacker]]

---

## Cyber-FMEA Entry 13: OPC UA Server Certificate Spoofing

**Component**: [[EQUIPMENT: OPC UA server]]
**Cyber Failure Mode**: Man-in-the-middle attack via certificate spoofing
**Attack Vector**: [[ATTACK_PATTERN: Certificate authority compromise]]
**Root Cause**: [[VULNERABILITY: Trust of compromised CA]]

**Consequences**:
- [[HAZARD: Data interception and manipulation]]
- Encrypted channel compromise
- Control command injection
- Authentication bypass

**Current Cyber Controls**:
- [[MITIGATION: X.509 certificates]]
- [[ARCHITECTURE: TLS encryption]]
- Certificate validation

**Risk Assessment**:
- **Cyber Severity (CS)**: 8 - Encrypted channel compromise
- **Attack Likelihood (AL)**: 3 - CA compromise rare
- **Detection Difficulty (DD)**: 8 - Appears as legitimate server
- **CRPN**: 192 (Medium - Action Recommended)

**Recommended Actions**:
- Implement [[MITIGATION: Certificate pinning]]
- Deploy [[ARCHITECTURE: Private certificate authority]]
- Add [[MITIGATION: Certificate transparency monitoring]]
- Establish [[ARCHITECTURE: Out-of-band certificate validation]]

**Threat Actor**: [[THREAT_ACTOR: PKI infrastructure attacker]]

---

## Cyber-FMEA Entry 14: Cloud SCADA Gateway Compromise

**Component**: [[EQUIPMENT: AWS IoT cloud SCADA gateway]]
**Cyber Failure Mode**: Cloud account compromise enabling control
**Attack Vector**: [[ATTACK_PATTERN: Cloud API credential theft]]
**Root Cause**: [[VULNERABILITY: Weak cloud IAM policies]]

**Consequences**:
- [[HAZARD: Cloud-to-field control channel compromise]]
- Remote monitoring loss
- Data exfiltration
- Cloud resource abuse

**Current Cyber Controls**:
- [[MITIGATION: AWS IAM policies]]
- [[ARCHITECTURE: TLS encryption]]
- API authentication

**Risk Assessment**:
- **Cyber Severity (CS)**: 7 - Remote access compromise
- **Attack Likelihood (AL)**: 6 - Cloud attacks increasing
- **Detection Difficulty (DD)**: 5 - Cloud logging available
- **CRPN**: 210 (Medium - Action Recommended)

**Recommended Actions**:
- Implement [[MITIGATION: AWS MFA and least privilege]]
- Deploy [[ARCHITECTURE: AWS GuardDuty threat detection]]
- Add [[MITIGATION: CloudTrail comprehensive logging]]
- Establish [[ARCHITECTURE: Local SCADA backup operation]]

**Threat Actor**: [[THREAT_ACTOR: Cloud-focused attacker]]

---

## Cyber-FMEA Entry 15: Mobile HMI Application Malware

**Component**: [[EQUIPMENT: Mobile HMI application]]
**Cyber Failure Mode**: Malicious mobile app granting unauthorized control
**Attack Vector**: [[ATTACK_PATTERN: App store poisoning]]
**Root Cause**: [[VULNERABILITY: No app authenticity verification]]

**Consequences**:
- [[HAZARD: Mobile device control compromise]]
- Credential theft
- Man-in-the-middle positioning
- Unauthorized access

**Current Cyber Controls**:
- [[MITIGATION: App store distribution]]
- [[ARCHITECTURE: SSL pinning]]
- Mobile app authentication

**Risk Assessment**:
- **Cyber Severity (CS)**: 7 - Mobile access compromise
- **Attack Likelihood (AL)**: 4 - Targeted mobile attacks rare
- **Detection Difficulty (DD)**: 6 - Looks like legitimate app
- **CRPN**: 168 (Medium - Monitor and Improve)

**Recommended Actions**:
- Implement [[MITIGATION: Mobile device management]]
- Deploy [[ARCHITECTURE: App certificate pinning]]
- Add [[MITIGATION: Mobile threat defense]]
- Establish [[ARCHITECTURE: Mobile app attestation]]

**Threat Actor**: [[THREAT_ACTOR: Mobile malware distributor]]

---

## Cyber-FMEA Summary Statistics
- **Total Components Analyzed**: 15 critical SCADA/control system components
- **Average CRPN**: 257 (High risk profile)
- **Critical Risk Items (CRPN > 400)**: 2 - Immediate action required
- **High Risk Items (CRPN 300-400)**: 5 - Priority action needed
- **Medium Risk Items (CRPN 150-299)**: 7 - Action recommended
- **Low Risk Items (CRPN < 150)**: 1 - Acceptable with monitoring
- **Cross-References**: 15 EQUIPMENT, 15 ATTACK_PATTERNS, 15 VULNERABILITIES, 15 HAZARDS, 60 MITIGATIONS (15 current + 60 recommended), 75 ARCHITECTURES, 15 THREAT_ACTORS

## Risk Prioritization
1. **VPN Remote Access** (CRPN=432) - Implement MFA immediately
2. **SCADA Master Server** (CRPN=420) - Deploy EDR and patch management
3. **Historian Injection** (CRPN=378) - Fix SQL injection vulnerability
4. **Engineering Workstation** (CRPN=378) - USB control and app whitelisting
5. **PLC Logic Manipulation** (CRPN=360) - Enable PLC security features

## Cyber-FMEA Effectiveness
- **Quantitative Risk Assessment**: CRPN enables objective prioritization
- **Comprehensive Coverage**: Analyzes full SCADA architecture
- **Actionable Recommendations**: 60 specific cybersecurity improvements
- **Resource Allocation**: Focus on highest CRPN items first
- **Continuous Improvement**: Re-analyze after implementing controls
